"""Explicit standalone-assembly inputs; importing this module starts no game.

Paths are relative to the configuration file, not the current working folder.
Loading reads configuration/save bytes or explicitly initializes a new save
medium. The default creates no output directory; an explicit session-output
override reserves only its fresh container/audio parent. Neither mode
overwrites a supplied save or supplies hardware progress.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..high_level_storage.domain import SaveImage
    from .frame_plan import FramePlanSpec


class ConfigurationError(ValueError):
    """A human-readable configuration error, before game construction."""


BUTTONS = ('up', 'down', 'left', 'right', 'a', 'b', 'c', 'start')
FORMAT = 'g5510-reconstructed-game-config-v1'
HIGH_LEVEL_FORMAT = 'g5510-reconstructed-game-config-v2'


@dataclass(frozen=True)
class KeyBinding:
    key: str
    port: int
    button: str


@dataclass(frozen=True)
class PadSnapshot:
    port: int
    buttons: tuple[str, ...]


@dataclass(frozen=True)
class VideoSnapshot:
    status_without_dma: int
    hv: int | None
    open_bus: int | None


@dataclass(frozen=True)
class EventSpec:
    """One finite external event; irrelevant typed lanes stay None/empty."""
    kind: str
    level: int | None = None
    video: VideoSnapshot | None = None
    pad_changes: tuple[PadSnapshot, ...] = ()
    live_pad_ports: tuple[int, ...] = ()
    event: str | None = None
    timestamp: int | None = None
    clock_hz: int | None = None
    clocks: int | None = None


@dataclass(frozen=True)
class FrontendConfig:
    scale: int
    timer_interval_ms: int
    keymap: tuple[KeyBinding, ...]
    events: tuple[EventSpec, ...]
    diagnostics_directory: Path
    frame_plan: FramePlanSpec | None = None


@dataclass(frozen=True)
class PcmOutputConfig:
    mode: str
    fm_path: Path | None = None
    psg_path: Path | None = None
    fm_sample_rate_hz: int | None = None
    psg_sample_rate_hz: int | None = None
    max_fm_frames: int | None = None
    max_psg_frames: int | None = None
    device_id: int | None = None
    max_queued_ms: int | None = None


@dataclass(frozen=True)
class RuntimeConfig:
    project_root: Path
    sound_native_root: Path
    sources: Path
    audio_root: Path
    chip_library: Path
    inputs: Path
    output: Path
    save_image: SaveImage
    save_path: Path | None
    frontend: FrontendConfig
    pcm_output: PcmOutputConfig
    # v1 keeps its original explicit legacy source contract. Only v2 selects
    # a high-level build, before construction; None is not a failed-load retry.
    m68k_native_root: Path | None = None


def _object(value, keys, context):
    if type(value) is not dict or set(value) != set(keys):
        actual = set(value) if type(value) is dict else set()
        missing, extra = sorted(set(keys) - actual), sorted(actual - set(keys))
        raise ConfigurationError(f'{context} 字段不完整或存在未知字段；缺少={missing}，多余={extra}')
    return value


def _list(value, context):
    if type(value) is not list:
        raise ConfigurationError(f'{context} 必须是明确的有限列表。')
    return value


def _integer(value, context, low=0, high=None):
    if type(value) is not int or value < low or (high is not None and value > high):
        bound = f'{low}..{high}' if high is not None else f'>={low}'
        raise ConfigurationError(f'{context} 必须是整数（{bound}），不能使用布尔值或推测值。')
    return value


def _word_or_none(value, context):
    return None if value is None else _integer(value, context, 0, 65535)


def _boolean(value, context):
    if type(value) is not bool:
        raise ConfigurationError(f'{context} 必须显式填写 true 或 false。')
    return value


def _text(value, context):
    if type(value) is not str or not value.strip() or '\x00' in value:
        raise ConfigurationError(f'{context} 必须填写非空字符串。')
    return value


def _path(value, directory, context, *, existing=None):
    text = _text(value, context)
    path = Path(text)
    if not path.is_absolute():
        path = directory / path
    try:
        path = path.resolve(strict=existing is not None)
    except (OSError, RuntimeError) as error:
        raise ConfigurationError(f'{context} 路径不可用：{path}；{error}') from error
    if existing == 'file' and not path.is_file():
        raise ConfigurationError(f'{context} 必须指向现有文件：{path}')
    if existing == 'directory' and not path.is_dir():
        raise ConfigurationError(f'{context} 必须指向现有目录：{path}')
    return path


def _fresh_build_path(value, directory, project, context):
    path = _path(value, directory, context)
    build = (project / 'build').resolve()
    try:
        tail = path.relative_to(build)
    except ValueError as error:
        raise ConfigurationError(f'{context} 只能是工程 build 内的新路径：{path}') from error
    if not tail.parts or path.exists():
        raise ConfigurationError(f'{context} 必须是尚不存在的新路径，不能覆盖：{path}')
    return path


def _pad(value, context):
    row = _object(value, ('port', 'buttons'), context)
    port = _integer(row['port'], context + '.port', 0, 2)
    buttons = _list(row['buttons'], context + '.buttons')
    if any(type(name) is not str or name not in BUTTONS for name in buttons) or len(set(buttons)) != len(buttons):
        raise ConfigurationError(f'{context}.buttons 只允许不重复的 {BUTTONS}；[] 表示完整释放快照。')
    return PadSnapshot(port, tuple(buttons))


def _event(value, index):
    context = f'frontend.events[{index}]'
    if type(value) is not dict:
        raise ConfigurationError(context + ' 必须是事件对象。')
    kind = value.get('kind')
    if kind == 'irq':
        row = _object(value, ('kind', 'level', 'video', 'pad_changes', 'live_pad_ports'), context)
        level = _integer(row['level'], context + '.level', 4, 6)
        if level not in (4, 6):
            raise ConfigurationError(context + '.level 只支持已有原 level4/level6。')
        video = _object(row['video'], ('status_without_dma', 'hv', 'open_bus'), context + '.video')
        status = _integer(video['status_without_dma'], context + '.video.status_without_dma', 0, 65535)
        if status & 2:
            raise ConfigurationError(context + ' 不能外供 DMA busy 位；该位属于真实 VDP pending owner。')
        snapshot = VideoSnapshot(status, _word_or_none(video['hv'], context + '.video.hv'), _word_or_none(video['open_bus'], context + '.video.open_bus'))
        pads = tuple((_pad(item, context + f'.pad_changes[{n}]') for n, item in enumerate(_list(row['pad_changes'], context + '.pad_changes'))))
        if len({item.port for item in pads}) != len(pads):
            raise ConfigurationError(context + ' 同一事件不能重复指定物理端口快照。')
        ports = tuple((_integer(port, context + '.live_pad_ports', 0, 2) for port in _list(row['live_pad_ports'], context + '.live_pad_ports')))
        if len(set(ports)) != len(ports):
            raise ConfigurationError(context + '.live_pad_ports 不得重复。')
        return EventSpec(kind, level=level, video=snapshot, pad_changes=pads, live_pad_ports=ports)
    if kind == 'device':
        row = _object(value, ('kind', 'event'), context)
        event = row['event']
        if event not in ('vblank-end', 'vblank-start', 'sound-bus-acquire', 'vdp-dma'):
            raise ConfigurationError(context + ' 仅支持已有明确设备事件；DMA 必须消耗原有限供给。')
        return EventSpec(kind, event=event)
    if kind == 'audio_advance':
        _object(value, ('kind',), context)
        return EventSpec(kind)
    if kind == 'audio_im1':
        row = _object(value, ('kind', 'timestamp', 'clock_hz'), context)
        return EventSpec(kind, timestamp=_integer(row['timestamp'], context + '.timestamp'), clock_hz=_integer(row['clock_hz'], context + '.clock_hz', 1))
    if kind in ('fm_clocks', 'psg_clocks'):
        row = _object(value, ('kind', 'clocks'), context)
        return EventSpec(kind, clocks=_integer(row['clocks'], context + '.clocks', 1))
    raise ConfigurationError(context + f' 未知事件类型 {kind!r}；没有自动 IRQ、时钟或 ready 补充。')


def _frontend(value, directory, project):
    common = ('scale', 'timer_interval_ms', 'keymap', 'diagnostics_directory')
    if type(value) is not dict or (('events' in value) == ('frame_plan' in value)):
        raise ConfigurationError('frontend 必须在 events 与 frame_plan 中明确选择一个，不能同时填写或都省略。')
    mode = 'events' if 'events' in value else 'frame_plan'
    row = _object(value, common + (mode,), 'frontend')
    bindings = []
    for index, item in enumerate(_list(row['keymap'], 'frontend.keymap')):
        context = f'frontend.keymap[{index}]'
        key = _object(item, ('key', 'port', 'button'), context)
        button = _text(key['button'], context + '.button')
        if button not in BUTTONS:
            raise ConfigurationError(context + '.button 必须是明确的物理按键名。')
        bindings.append(KeyBinding(_text(key['key'], context + '.key'),
            _integer(key['port'], context + '.port', 0, 2), button))
    if len({item.key for item in bindings}) != len(bindings):
        raise ConfigurationError('frontend.keymap 中同一个键不能重复映射。')
    events, plan = (), None
    if mode == 'events':
        events = tuple(_event(item, index)
            for index, item in enumerate(_list(row['events'], 'frontend.events')))
        if not events:
            raise ConfigurationError('frontend.events 必须显式提供至少一个有限事件，不能自动生成计划。')
    else:
        from .frame_plan import parse_frame_plan
        plan = parse_frame_plan(row['frame_plan'])
    return FrontendConfig(_integer(row['scale'], 'frontend.scale', 1, 8),
        _integer(row['timer_interval_ms'], 'frontend.timer_interval_ms', 1),
        tuple(bindings), events,
        _fresh_build_path(row['diagnostics_directory'], directory, project, 'frontend.diagnostics_directory'),
        frame_plan=plan)


def _pcm_output(value, directory, project):
    if type(value) is not dict:
        raise ConfigurationError('pcm_output 必须显式指定 mode。')
    if value.get('mode') == 'discard':
        _object(value, ('mode',), 'pcm_output')
        return PcmOutputConfig('discard')
    if value.get('mode') == 'speakers':
        row = _object(value, ('mode', 'fm_sample_rate_hz', 'psg_sample_rate_hz',
            'max_fm_frames', 'max_psg_frames', 'device_id', 'max_queued_ms'), 'pcm_output')
        return PcmOutputConfig('speakers',
            fm_sample_rate_hz=_integer(row['fm_sample_rate_hz'], 'pcm_output.fm_sample_rate_hz', 1, 1_000_000),
            psg_sample_rate_hz=_integer(row['psg_sample_rate_hz'], 'pcm_output.psg_sample_rate_hz', 1, 1_000_000),
            max_fm_frames=_integer(row['max_fm_frames'], 'pcm_output.max_fm_frames', 1),
            max_psg_frames=_integer(row['max_psg_frames'], 'pcm_output.max_psg_frames', 1),
            device_id=_integer(row['device_id'], 'pcm_output.device_id', -1, 0xFFFFFFFE),
            max_queued_ms=_integer(row['max_queued_ms'], 'pcm_output.max_queued_ms', 1, 10_000))
    if value.get('mode') != 'wav':
        raise ConfigurationError('pcm_output.mode 只能显式为 discard、wav 或 speakers。')
    row = _object(value, ('mode', 'fm_path', 'psg_path', 'fm_sample_rate_hz',
        'psg_sample_rate_hz', 'max_fm_frames', 'max_psg_frames'), 'pcm_output')
    fm = _fresh_build_path(row['fm_path'], directory, project, 'pcm_output.fm_path')
    psg = _fresh_build_path(row['psg_path'], directory, project, 'pcm_output.psg_path')
    if fm == psg:
        raise ConfigurationError('FM 与 PSG 必须使用两个不同的新文件，不能互相覆盖。')
    if not fm.parent.is_dir() or not psg.parent.is_dir():
        raise ConfigurationError('WAV 的父目录必须已经存在；不能放进尚未创建的 output 目录。')
    return PcmOutputConfig('wav', fm, psg,
        _integer(row['fm_sample_rate_hz'], 'pcm_output.fm_sample_rate_hz', 1),
        _integer(row['psg_sample_rate_hz'], 'pcm_output.psg_sample_rate_hz', 1),
        _integer(row['max_fm_frames'], 'pcm_output.max_fm_frames', 1),
        _integer(row['max_psg_frames'], 'pcm_output.max_psg_frames', 1))


def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConfigurationError(f'配置存在重复字段 {key!r}，请保留一个明确值。')
        result[key] = value
    return result


def load_runtime_config(path: Path | str, *, session_output: Path | None = None) -> RuntimeConfig:
    """Read the same explicit profile/save, optionally reserve new output paths.

    With no session_output the original no-write behavior is unchanged. An
    explicit override reserves only its new container/audio parent; the same
    complete schema, path, fresh-output and save validation below still runs.
    No source loader, device or game is started by either mode.
    """
    config_path = Path(path).resolve()
    try:
        value = json.loads(config_path.read_text(encoding='utf-8-sig'), object_pairs_hook=_no_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ConfigurationError(f'无法读取配置 {config_path}：{error}') from error
    if type(value) is not dict or value.get('format') not in (FORMAT, HIGH_LEVEL_FORMAT):
        raise ConfigurationError(f'配置 format 必须为 {FORMAT} 或 {HIGH_LEVEL_FORMAT}。')
    high_level = value['format'] == HIGH_LEVEL_FORMAT
    keys = ('format', 'project_root', 'sound_native_root', 'sources', 'audio_root',
        'chip_library', 'inputs', 'output', 'save', 'frontend', 'pcm_output')
    row = _object(value, keys + (('m68k_native_root',) if high_level else ()), '配置')
    if session_output is not None:
        from .session_config import prepare_session_fields
        row = prepare_session_fields(row, config_path, session_output)
    directory = config_path.parent
    project = _path(row['project_root'], directory, 'project_root', existing='directory')
    native_root = (_path(row['m68k_native_root'], directory, 'm68k_native_root', existing='directory')
        if high_level else None)
    paths = {name: _path(row[name], directory, name, existing=kind) for name, kind in (
        ('sound_native_root', 'directory'), ('sources', 'file'), ('audio_root', 'directory'),
        ('chip_library', 'file'), ('inputs', 'file'))}
    output = _fresh_build_path(row['output'], directory, project, 'output')
    if type(row['save']) is not dict:
        raise ConfigurationError('save 必须明确选择已有文件 path 或新介质 initial_byte。')
    fresh_medium = 'initial_byte' in row['save']
    save = _object(row['save'],
        ('initial_byte', 'readable', 'writable') if fresh_medium else ('path', 'readable', 'writable'), 'save')
    save_path = None if fresh_medium else _path(save['path'], directory, 'save.path', existing='file')
    initial_byte = _integer(save['initial_byte'], 'save.initial_byte', 0, 255) if fresh_medium else None
    readable = _boolean(save['readable'], 'save.readable')
    writable = _boolean(save['writable'], 'save.writable')
    frontend = _frontend(row['frontend'], directory, project)
    pcm = _pcm_output(row['pcm_output'], directory, project)
    if fresh_medium:
        # An explicitly declared external cartridge medium, not a valid-save
        # result, inferred hardware reset default or host game-state repair.
        raw = bytes((initial_byte,)) * 8192
    else:
        try:
            with save_path.open('rb') as stream:
                raw = stream.read(8193)
        except OSError as error:
            raise ConfigurationError(f'无法读取显式存档 {save_path}：{error}') from error
        if len(raw) != 8192:
            raise ConfigurationError(f'存档必须恰好8192字节，当前读取{len(raw)}字节：{save_path}')
    # This sole deferred type import constructs only the explicit backing. It
    # does not create a Scene/chip, load program DATA or execute game code.
    from ..high_level_storage.domain import SaveImage
    image = SaveImage(bytearray(raw), readable=readable, writable=writable)
    return RuntimeConfig(project, paths['sound_native_root'], paths['sources'], paths['audio_root'],
        paths['chip_library'], paths['inputs'], output, image, save_path, frontend, pcm, native_root)
