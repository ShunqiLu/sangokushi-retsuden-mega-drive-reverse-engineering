"""Bounded JSON-line controls for one already-open normal application.

Waiting on stdin does not advance the game. Every advancing command supplies
complete physical pad snapshots and uses the existing finite frame owner;
this module neither creates hardware supplies nor interprets game state.
The normal CLI alone owns application cleanup on EOF, close or failure.
"""
from dataclasses import dataclass
import json
from pathlib import Path
import sys

from .config import (
    BUTTONS, ConfigurationError, FrontendConfig, _integer, _list,
    _no_duplicate_keys, _object, _pad,
)
from .frame_plan import FiniteFramePlan
from .session_config import _no_reparse


MAX_LINE_BYTES = 64 * 1024
MAX_FILENAME_CHARACTERS = 160
COMMAND_KEYS = {
    'advance': ('command', 'frames', 'pads'),
    'capture': ('command', 'file'),
    'observe': ('command',),
    'observe_palette': ('command',),
    'export_save': ('command', 'file'),
    'extend_frames': ('command', 'new_total'),
    'close': ('command',),
}


class ConsoleProtocolError(ValueError):
    """Rejected before a game/device operation; the next line may be read."""


@dataclass(frozen=True)
class ConsoleResult:
    exit_code: int
    commands_completed: int
    frames_completed: int
    reason: str


def _reply(stream, **fields):
    """One compact, immediately visible response; never emit Scene dumps."""
    stream.write(json.dumps(fields, ensure_ascii=False, allow_nan=False,
        separators=(',', ':')) + '\n')
    stream.flush()


def _nonfinite(value):
    raise ConsoleProtocolError('non-finite JSON numbers are not supported: ' + value)


def _decode_line(line):
    try:
        text = line.decode('utf-8') if isinstance(line, bytes) else line
        if type(text) is not str:
            raise ConsoleProtocolError('the input stream must return UTF-8 bytes or text')
        if len(text.encode('utf-8')) > MAX_LINE_BYTES:
            raise ConsoleProtocolError('one JSON line may contain at most 65536 UTF-8 bytes')
        value = json.loads(text, object_pairs_hook=_no_duplicate_keys,
            parse_constant=_nonfinite)
        if type(value) is not dict or type(value.get('command')) is not str:
            raise ConsoleProtocolError('one object with an explicit command is required')
        name = value['command']
        if name not in COMMAND_KEYS:
            raise ConsoleProtocolError('unknown command; allowed: ' + ', '.join(COMMAND_KEYS))
        return name, _object(value, COMMAND_KEYS[name], 'console.' + name)
    except (UnicodeError, ValueError, RecursionError) as error:
        if type(error) is ConsoleProtocolError:
            raise
        raise ConsoleProtocolError(str(error)) from error


def _pads(value, plan):
    """Validate every declared port before the first advancing operation."""
    from ..high_level_input.hardware_controller import PadButtons
    from ..high_level_video.integrated_scene_driver import PhysicalPadSnapshot
    rows = tuple(_pad(row, 'console.advance.pads[' + str(index) + ']')
        for index, row in enumerate(_list(value, 'console.advance.pads')))
    physical = tuple(PhysicalPadSnapshot(row.port,
        PadButtons(**{name: name in row.buttons for name in BUTTONS})) for row in rows)
    # The normal frame owner already defines the exact declared-port set and
    # fixed-versus-live input rule. This method validates, but applies nothing.
    return plan._physical_changes(physical)


def _artifact_name(value, *, png):
    if (type(value) is not str or not value or len(value) > MAX_FILENAME_CHARACTERS
            or value in ('.', '..') or value[-1:] in (' ', '.')
            or any(ord(character) < 32 or character in '<>:"/\\|?*' for character in value)):
        raise ConsoleProtocolError('file must be one simple new filename, without a path')
    device = value.split('.', 1)[0].upper()
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'CONIN$', 'CONOUT$'}
    reserved.update(prefix + suffix for prefix in ('COM', 'LPT')
        for suffix in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '¹', '²', '³'))
    if device in reserved or Path(value).name != value:
        raise ConsoleProtocolError('device names and path components are refused')
    if png and Path(value).suffix.casefold() != '.png':
        raise ConsoleProtocolError('capture requires an explicit .png filename')
    return value


def _diagnostics_root(app, config):
    """Create only the configured diagnostics leaf, never an arbitrary tree."""
    root = config.diagnostics_directory.absolute()
    build = (app.config.project_root / 'build').absolute()
    _no_reparse(build, 'console project build')
    _no_reparse(root, 'console diagnostics')
    root, build = root.resolve(), build.resolve(strict=True)
    if root == build or not root.is_relative_to(build) or not build.is_dir():
        raise ValueError('console diagnostics must stay inside the configured project build')
    if not root.exists():
        if not root.parent.is_dir():
            raise ValueError('the configured diagnostics parent must already exist')
        root.mkdir()
    _no_reparse(root, 'console diagnostics')
    if not root.is_dir():
        raise ValueError('the configured diagnostics destination must be a directory')
    return root


def _new_artifact(app, config, name):
    from ..high_level_rom.native import fresh_output
    root = _diagnostics_root(app, config)
    path = root / name
    if path.exists() or path.is_symlink():
        raise ConsoleProtocolError('the requested file already exists; choose a new filename')
    destination = fresh_output(path)
    if destination.parent != root:
        raise ConsoleProtocolError('the requested file escaped the diagnostics directory')
    return destination


def _prepare(name, row, plan, app, config):
    """Validate the entire command before applying its first game operation."""
    try:
        if name == 'advance':
            count = _integer(row['frames'], 'console.advance.frames', 1)
            if count > plan.spec.max_frames - plan.frames_completed:
                raise ConsoleProtocolError('advance exceeds the remaining declared frame limit')
            return dict(frames=count, pads=_pads(row['pads'], plan))
        if name in ('capture', 'export_save'):
            filename = _artifact_name(row['file'], png=name == 'capture')
            return dict(path=_new_artifact(app, config, filename))
        if name == 'extend_frames':
            total = _integer(row['new_total'], 'console.extend_frames.new_total', plan.spec.max_frames + 1)
            if not plan.exhausted:
                raise ConsoleProtocolError('only a successfully exhausted frame plan may be extended')
            return dict(new_total=total)
        return {}
    except (ConfigurationError, ConsoleProtocolError) as error:
        raise ConsoleProtocolError(str(error)) from error
    except ValueError as error:
        # _physical_changes and fresh_output are pure validation here. No
        # recovered software has been entered and no device has been advanced.
        raise ConsoleProtocolError(str(error)) from error


class _ExclusivePngTarget:
    """Let the real PNG writer use an already exclusively opened new file."""
    def __init__(self, stream):
        self.stream = stream

    def write_bytes(self, data):
        return self.stream.write(data)


def _capture(app, path):
    from ..graphics_vdp.graphics_assets import write_rgb_png
    frame = app.render()
    if len(frame.rgba) != frame.width * frame.height * 4:
        raise ValueError('the actual renderer returned an invalid RGBA extent')
    rgb = b''.join(frame.rgba[index:index + 3] for index in range(0, len(frame.rgba), 4))
    with path.open('xb') as stream:
        # write_rgb_png encodes the actual RGB pixels. Its narrow write_bytes
        # port is routed to this exclusive stream, not Path.write_bytes (which
        # would reopen/overwrite a filename after the initial safety check).
        write_rgb_png(_ExclusivePngTarget(stream), frame.width, frame.height, rgb)
    return dict(file=path.name, width=frame.width, height=frame.height,
        source='actual_live_VDP_renderer')


def _execute(name, prepared, plan, app):
    if name == 'advance':
        for _ in range(prepared['frames']):
            plan.step(pad_changes=prepared['pads'])
        return dict(frames_advanced=prepared['frames'])
    if name == 'capture':
        return _capture(app, prepared['path'])
    if name == 'observe':
        return dict(observation=app.observe())
    if name == 'observe_palette':
        return dict(observation=app.observe_palette())
    if name == 'export_save':
        path = app.export_save(prepared['path'])
        return dict(file=path.name, bytes=path.stat().st_size, valid_game_save_claimed=False)
    if name == 'extend_frames':
        previous = plan.spec.max_frames
        plan.extend_max_frames(prepared['new_total'])
        return dict(previous_max_frames=previous, device_or_PCM_budget_refilled=False)
    raise RuntimeError('only a fully validated non-close command may be executed')


def _boundary(config, app, plan, error):
    """Use the normal frontend's small failure record, not a RAM snapshot."""
    from .frontend import _diagnostic
    try:
        root = _diagnostics_root(app, config)
        return _diagnostic(root, error=error, index=plan.frames_completed,
            event=None, total=plan.spec.max_frames, held_keys=(), stage='console')
    except Exception as diagnostic_error:
        error.add_note('Could not preserve console diagnostic: ' + str(diagnostic_error))
        return None


def run_console(app, config: FrontendConfig, *, input_stream=None, output_stream=None) -> ConsoleResult:
    """Control one retained App; return without closing or rebuilding it.

    The default input is stdin's bounded binary UTF-8 line stream. An injected
    stream may also return text. Every result is one flushed JSON line. Invalid
    preflight input can be corrected; any execution exception terminates this
    console without replay, leaving the normal CLI finally to release owners.
    """
    if (type(config) is not FrontendConfig or config is not app.config.frontend
            or config.frame_plan is None):
        raise ValueError('console requires the same explicit frontend.frame_plan; events are not converted')
    plan = FiniteFramePlan(app, config.frame_plan)
    source = getattr(sys.stdin, 'buffer', sys.stdin) if input_stream is None else input_stream
    destination = sys.stdout if output_stream is None else output_stream
    completed = 0
    _reply(destination, status='ready', frontend='console', commands=list(COMMAND_KEYS),
        max_line_bytes=MAX_LINE_BYTES, frames_completed=0, max_frames=plan.spec.max_frames,
        declared_ports=sorted({row.port for row in plan.spec.pad_changes} | set(plan.spec.live_pad_ports)),
        live_pad_ports=list(plan.spec.live_pad_ports),
        fixed_pad_snapshots=[dict(port=row.port, buttons=list(row.buttons))
            for row in plan.spec.pad_changes if row.port not in plan.spec.live_pad_ports])
    while True:
        try:
            line = source.readline(MAX_LINE_BYTES + 1)
        except KeyboardInterrupt:
            _reply(destination, status='closed', reason='interrupted', frames_completed=plan.frames_completed)
            return ConsoleResult(130, completed, plan.frames_completed, 'interrupted')
        if line in (b'', ''):
            _reply(destination, status='closed', reason='EOF', frames_completed=plan.frames_completed)
            return ConsoleResult(0, completed, plan.frames_completed, 'EOF')
        # Do not drain an unbounded invalid line or interpret its residual
        # fragments as fresh commands. The outer normal finally still closes.
        if len(line) > MAX_LINE_BYTES or (type(line) is str and len(line.encode('utf-8')) > MAX_LINE_BYTES):
            _reply(destination, status='protocol_error', error='line exceeds 65536 UTF-8 bytes; session stopped',
                frames_completed=plan.frames_completed)
            return ConsoleResult(1, completed, plan.frames_completed, 'input_line_limit')
        try:
            name, row = _decode_line(line)
            prepared = _prepare(name, row, plan, app, config)
        except ConsoleProtocolError as error:
            _reply(destination, status='protocol_error', error=str(error)[:2048],
                frames_completed=plan.frames_completed)
            continue
        if name == 'close':
            _reply(destination, status='closed', reason='close_command', frames_completed=plan.frames_completed)
            return ConsoleResult(0, completed + 1, plan.frames_completed, 'close_command')
        try:
            details = _execute(name, prepared, plan, app)
        except BaseException as error:
            diagnostic = _boundary(config, app, plan, error)
            _reply(destination, status='boundary', command=name, exception_type=type(error).__name__,
                error=str(error)[:2048], diagnostic=diagnostic, frames_completed=plan.frames_completed,
                max_frames=plan.spec.max_frames, prefix_reentered=False)
            return ConsoleResult(1, completed, plan.frames_completed, 'boundary')
        completed += 1
        _reply(destination, status='ok', command=name, frames_completed=plan.frames_completed,
            max_frames=plan.spec.max_frames, exhausted=plan.exhausted, **details)
