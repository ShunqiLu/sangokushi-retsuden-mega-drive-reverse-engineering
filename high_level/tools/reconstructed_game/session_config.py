"""Explicit fresh output container for the normal application's same config.

Only destination paths are derived. All input paths keep the original config
directory as their authority, including v2 native roots and an existing save.
No source, device, save content, clock, event or execution budget is supplied.
The ordinary config parser still validates the complete resulting profile.
"""
from copy import deepcopy
from pathlib import Path
import stat

from .config import (
    ConfigurationError, FORMAT, HIGH_LEVEL_FORMAT, _object, _path, _text,
)


def _no_reparse(path, context):
    """Check the lexical path before resolution can hide a junction."""
    for member in (path, *path.parents):
        attributes = getattr(member.lstat(), 'st_file_attributes', 0) if member.exists() else 0
        if (member.is_symlink() or getattr(member, 'is_junction', lambda: False)()
                or attributes & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)):
            raise ConfigurationError(context + ' 不允许经过符号链接或目录联接：' + str(member))


def _session_destination(value, project):
    if not isinstance(value, Path):
        raise ConfigurationError('--session-output 必须是明确的新目录路径。')
    text = str(value)
    if text.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in text[2:]:
        raise ConfigurationError('--session-output 不允许 UNC、设备路径或备用数据流。')
    lexical = value.absolute()
    _no_reparse(lexical, '--session-output')
    candidate = lexical.resolve()
    build = project / 'build'
    _no_reparse(build, '工程 build')
    build = build.resolve(strict=True)
    if not build.is_dir() or candidate == build or not candidate.is_relative_to(build):
        raise ConfigurationError('--session-output 只能是当前工程 build 内明确的新子目录。')
    if candidate.exists() or not candidate.parent.is_dir():
        raise ConfigurationError('--session-output 必须尚不存在，且它的父目录必须已经存在：' + str(candidate))
    return candidate


def _output_schema(fields):
    """Reject malformed/unknown output fields before reserving any directory."""
    _text(fields['output'], 'output')
    frontend = fields['frontend']
    if type(frontend) is not dict or (('events' in frontend) == ('frame_plan' in frontend)):
        raise ConfigurationError('frontend 必须明确选择 events 或 frame_plan。')
    kind = 'events' if 'events' in frontend else 'frame_plan'
    _object(frontend, ('scale', 'timer_interval_ms', 'keymap', 'diagnostics_directory', kind), 'frontend')
    _text(frontend['diagnostics_directory'], 'frontend.diagnostics_directory')
    pcm = fields['pcm_output']
    if type(pcm) is not dict:
        raise ConfigurationError('pcm_output 必须显式指定 mode。')
    if pcm.get('mode') == 'discard':
        _object(pcm, ('mode',), 'pcm_output')
    elif pcm.get('mode') == 'speakers':
        _object(pcm, ('mode', 'fm_sample_rate_hz', 'psg_sample_rate_hz',
            'max_fm_frames', 'max_psg_frames', 'device_id', 'max_queued_ms'), 'pcm_output')
    elif pcm.get('mode') == 'wav':
        _object(pcm, ('mode', 'fm_path', 'psg_path', 'fm_sample_rate_hz',
            'psg_sample_rate_hz', 'max_fm_frames', 'max_psg_frames'), 'pcm_output')
        _text(pcm['fm_path'], 'pcm_output.fm_path')
        _text(pcm['psg_path'], 'pcm_output.psg_path')
    else:
        raise ConfigurationError('pcm_output.mode 只能显式为 discard、wav 或 speakers。')


def prepare_session_fields(fields, config_path: Path, session_output: Path):
    """Reserve one absent container and return an independently derived dict.

    Called only for an explicit normal-entry --session-output. It writes no
    JSON or media and never deletes a partial directory after a failure. The
    selected root contains runtime/, diagnostics/ and, in WAV mode, audio/.
    runtime and diagnostics remain absent for their original fresh owners;
    only audio's parent is created for the unchanged WAV-parent requirement.
    """
    if type(fields) is not dict or fields.get('format') not in (FORMAT, HIGH_LEVEL_FORMAT):
        raise ConfigurationError('session 输出需要完整的原 v1 或 v2 配置。')
    high_level = fields['format'] == HIGH_LEVEL_FORMAT
    keys = ('format', 'project_root', 'sound_native_root', 'sources', 'audio_root',
        'chip_library', 'inputs', 'output', 'save', 'frontend', 'pcm_output')
    _object(fields, keys + (('m68k_native_root',) if high_level else ()), '配置')
    _output_schema(fields)
    result = deepcopy(fields)
    directory = config_path.parent
    raw_project = Path(_text(fields['project_root'], 'project_root'))
    lexical_project = raw_project if raw_project.is_absolute() else directory / raw_project
    _no_reparse(lexical_project.absolute(), 'project_root')
    project = _path(fields['project_root'], directory, 'project_root', existing='directory')
    candidate = _session_destination(session_output, project)

    inputs = []
    result['project_root'] = str(project)
    for name, existing in (('sound_native_root', 'directory'), ('sources', 'file'),
            ('audio_root', 'directory'), ('chip_library', 'file'), ('inputs', 'file')):
        path = _path(fields[name], directory, name, existing=existing)
        result[name] = str(path)
        inputs.append((name, path))
    if high_level:
        path = _path(fields['m68k_native_root'], directory, 'm68k_native_root', existing='directory')
        result['m68k_native_root'] = str(path)
        inputs.append(('m68k_native_root', path))
    save = fields['save']
    if type(save) is not dict:
        raise ConfigurationError('save 必须是明确的外部介质配置。')
    fresh = 'initial_byte' in save
    _object(save, ('initial_byte', 'readable', 'writable') if fresh
        else ('path', 'readable', 'writable'), 'save')
    if not fresh:
        path = _path(save['path'], directory, 'save.path', existing='file')
        result['save']['path'] = str(path)
        inputs.append(('save.path', path))
    for name, path in inputs:
        if candidate == path or candidate.is_relative_to(path) or path.is_relative_to(candidate):
            raise ConfigurationError('--session-output 不能包含或位于任何配置输入 authority 内：' + name)

    if result['pcm_output']['mode'] == 'wav':
        original_fm = _path(fields['pcm_output']['fm_path'], directory, 'pcm_output.fm_path')
        original_psg = _path(fields['pcm_output']['psg_path'], directory, 'pcm_output.psg_path')
        if original_fm == original_psg:
            raise ConfigurationError('原配置 FM 与 PSG 输出不能是同一个文件。')
        result['pcm_output']['fm_path'] = str(candidate / 'audio' / 'fm.wav')
        result['pcm_output']['psg_path'] = str(candidate / 'audio' / 'psg.wav')
    result['output'] = str(candidate / 'runtime')
    result['frontend']['diagnostics_directory'] = str(candidate / 'diagnostics')
    try:
        # Exclusive mkdir handles a destination appearing after validation;
        # parents=True/exist_ok=True would silently broaden this authority.
        candidate.mkdir()
        if result['pcm_output']['mode'] == 'wav':
            (candidate / 'audio').mkdir()
    except OSError as error:
        raise ConfigurationError('不能独占创建新会话目录；已创建的部分保留，不覆盖或清理：'
            + str(candidate) + '；' + str(error)) from error
    return result
