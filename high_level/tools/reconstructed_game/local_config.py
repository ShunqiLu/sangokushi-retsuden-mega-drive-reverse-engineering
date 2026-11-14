"""Author one local v2 gameplay configuration without starting the game.

The edition supplies its own complete resource root and native build roots.
All other dependencies and finite settings are explicit existing user inputs;
no ROM, old workspace config path, device budget or save is inferred/copied.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path

from .config import (
    ConfigurationError, HIGH_LEVEL_FORMAT, _boolean, _frontend, _integer,
    _no_duplicate_keys, _object, _pcm_output, _text,
)
from .session_config import _no_reparse, _output_schema


MAX_SETTINGS_BYTES = 1_000_000
CONFIG_KEYS = ('format', 'project_root', 'm68k_native_root', 'sound_native_root',
    'sources', 'audio_root', 'chip_library', 'inputs', 'output', 'save',
    'frontend', 'pcm_output')


def _ordinary(path: Path, context: str) -> Path:
    if not isinstance(path, Path):
        raise ConfigurationError(context + ' requires an explicit Path')
    raw = str(path)
    if raw.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in raw[2:]:
        raise ConfigurationError(context + ': UNC/device/alternate-stream paths refused')
    absolute = path.absolute()
    _no_reparse(absolute, context)
    return absolute.resolve(strict=False)


def _inside(edition: Path, value: Path, context: str, *, kind=None, fresh=False) -> Path:
    if not isinstance(value, Path):
        raise ConfigurationError(context + ' requires an explicit Path')
    path = _ordinary(value if value.is_absolute() else edition / value, context)
    if path == edition or not path.is_relative_to(edition):
        raise ConfigurationError(context + ': path must stay inside this edition')
    if kind == 'file' and not path.is_file():
        raise ConfigurationError(context + ': an explicit existing file is required')
    if kind == 'directory' and not path.is_dir():
        raise ConfigurationError(context + ': an explicit existing directory is required')
    if fresh and (path.exists() or not path.parent.is_dir()):
        raise ConfigurationError(context + ': fresh destination with an existing parent required')
    return path


def _read_json(path: Path, maximum=MAX_SETTINGS_BYTES):
    if not path.is_file() or path.stat().st_size > maximum:
        raise ConfigurationError('bounded ordinary JSON input required: ' + str(path))
    def nonfinite(value):
        raise ConfigurationError('nonfinite JSON settings refused: ' + value)
    with path.open('rb') as stream:
        raw = stream.read(maximum + 1)
    if len(raw) > maximum:
        raise ConfigurationError('JSON input grew past its explicit limit')
    return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_no_duplicate_keys,
        parse_constant=nonfinite)


def _local_scene_manifest(edition):
    path = _inside(edition, Path('scene-sources.json'), 'local Scene manifest', kind='file')
    fields = _object(_read_json(path, 131072), ('format', 'roots'), 'local Scene manifest')
    if (fields['format'] != 'g5510-explicit-scene-source-roots-v1'
            or type(fields['roots']) is not list or len(fields['roots']) != 1):
        raise ConfigurationError('this edition requires its complete single local Scene root')
    row = _object(fields['roots'][0], ('path', 'ids'), 'local Scene root')
    ids = row['ids']
    if (row['path'] != '.' or type(ids) is not list or len(ids) != 128
            or any(type(ident) is not str or not ident for ident in ids)
            or len(set(ids)) != 128):
        raise ConfigurationError('local Scene root must be . with128 explicit unique IDs; no external roots')
    return path


def _relative(path, directory):
    return Path(os.path.relpath(path, directory)).as_posix()


def _save_fields(settings, edition, save_path):
    if 'save' not in settings:
        raise ConfigurationError('settings has no save contract; no medium or successful save is invented')
    value = settings['save']
    if type(value) is not dict:
        raise ConfigurationError('settings.save requires an explicit original path or initial_byte contract')
    fresh_medium = 'initial_byte' in value
    row = _object(value, ('initial_byte', 'readable', 'writable') if fresh_medium
        else ('path', 'readable', 'writable'), 'settings.save')
    _boolean(row['readable'], 'save.readable')
    _boolean(row['writable'], 'save.writable')
    if fresh_medium:
        if save_path is not None:
            raise ConfigurationError('an explicit initial_byte setting cannot also select --save-path')
        _integer(row['initial_byte'], 'save.initial_byte', 0, 255)
        return deepcopy(row), None
    if save_path is None:
        raise ConfigurationError('existing-save settings require an explicit --save-path; old path is not inherited')
    path = _inside(edition, save_path, 'save.path', kind='file')
    if path.stat().st_size != 8192:
        raise ConfigurationError('explicit existing save must contain exactly8192 bytes')
    return dict(path=str(path), readable=row['readable'], writable=row['writable']), path


def materialize_local_gameplay_config(edition_root: Path, settings_path: Path,
        output: Path, *, m68k_native_root: Path, sound_native_root: Path,
        chip_library: Path, hardware_inputs: Path, run_output: Path,
        frontend: str, save_path: Path | None = None) -> dict:
    """Write a fresh local config; retain finite settings and explicit save intent.

    Only metadata/settings are read. The normal load_runtime_config remains
    the loading authority: no native/source qualification, hardware parser,
    save contents, library ABI, Scene, device, build or game is run here.
    """
    edition = _ordinary(edition_root, 'edition_root')
    if not edition.is_dir() or not (edition / 'build').is_dir():
        raise ConfigurationError('existing edition root and its build directory required')
    if not isinstance(settings_path, Path):
        raise ConfigurationError('settings requires an explicit Path')
    settings_source = _ordinary(settings_path if settings_path.is_absolute()
        else edition / settings_path, 'settings')
    settings = _read_json(settings_source)
    if type(settings) is not dict or settings.get('format') != HIGH_LEVEL_FORMAT:
        raise ConfigurationError('explicit reviewed v2 runtime settings required')
    save, selected_save = _save_fields(settings, edition, save_path)
    _object(settings, CONFIG_KEYS, 'reviewed settings')
    for name in ('project_root', 'm68k_native_root', 'sound_native_root', 'sources',
            'audio_root', 'chip_library', 'inputs', 'output'):
        _text(settings[name], 'settings.' + name)
    _output_schema(settings)
    if frontend not in ('window', 'console'):
        raise ConfigurationError('explicit window or console frontend required')
    if frontend == 'console' and 'frame_plan' not in settings['frontend']:
        raise ConfigurationError('console requires the supplied complete finite frame_plan, not inferred events')
    config_path = _inside(edition, output, 'configuration output', fresh=True)
    runtime = _inside(edition, run_output, 'runtime output', fresh=True)
    build = edition / 'build'
    if (config_path.suffix != '.json' or not config_path.is_relative_to(build)
            or runtime == build or not runtime.is_relative_to(build)):
        raise ConfigurationError('configuration JSON and new runtime output must be inside this edition build')
    dependencies = {
        'm68k_native_root': _inside(edition, m68k_native_root, 'm68k_native_root', kind='directory'),
        'sound_native_root': _inside(edition, sound_native_root, 'sound_native_root', kind='directory'),
        'chip_library': _inside(edition, chip_library, 'chip_library', kind='file'),
        'inputs': _inside(edition, hardware_inputs, 'inputs', kind='file'),
        'sources': _local_scene_manifest(edition),
    }
    for name in ('m68k_native_root', 'sound_native_root'):
        if dependencies[name] == build or not dependencies[name].is_relative_to(build):
            raise ConfigurationError(name + ': select this edition own existing build subdirectory')
    diagnostic = runtime.with_name(runtime.name + '-diagnostics')
    _inside(edition, diagnostic, 'diagnostics output', fresh=True)
    result = deepcopy(settings)
    result.update(format=HIGH_LEVEL_FORMAT, project_root=str(edition), audio_root=str(edition),
        output=str(runtime), save=save, **{name: str(path) for name, path in dependencies.items()})
    result['frontend']['diagnostics_directory'] = str(diagnostic)
    destinations = [config_path, runtime, diagnostic]
    if result['pcm_output']['mode'] == 'wav':
        for name, suffix in (('fm_path', '-fm.wav'), ('psg_path', '-psg.wav')):
            path = runtime.with_name(runtime.name + suffix)
            _inside(edition, path, name, fresh=True)
            result['pcm_output'][name] = str(path)
            destinations.append(path)
    if len(set(destinations)) != len(destinations):
        raise ConfigurationError('derived destinations must be distinct')
    for destination in destinations:
        if any(destination.is_relative_to(dependencies[name])
                for name in ('m68k_native_root', 'sound_native_root')):
            raise ConfigurationError('outputs must not enter a native input authority')
    directory = config_path.parent
    for name in ('project_root', 'm68k_native_root', 'sound_native_root', 'sources',
            'audio_root', 'chip_library', 'inputs', 'output'):
        result[name] = _relative(Path(result[name]), directory)
    result['frontend']['diagnostics_directory'] = _relative(diagnostic, directory)
    if selected_save is not None:
        result['save']['path'] = _relative(selected_save, directory)
    if result['pcm_output']['mode'] == 'wav':
        for name in ('fm_path', 'psg_path'):
            result['pcm_output'][name] = _relative(Path(result['pcm_output'][name]), directory)
    # Reuse the normal parser's pure finite-plan/PCM validation; no App or
    # save backing is constructed and no library/hardware source is opened.
    _frontend(result['frontend'], directory, edition)
    _pcm_output(result['pcm_output'], directory, edition)
    raw = (json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    if len(raw) > MAX_SETTINGS_BYTES:
        raise ConfigurationError('authored configuration exceeds the explicit settings limit')
    with config_path.open('xb') as stream:
        stream.write(raw)
    return dict(format='g5510-local-gameplay-config-authoring-v1', output=str(config_path),
        bytes=len(raw), settings_source=str(settings_source), launch_cwd=str(edition),
        launch_argv=['python', '-B', '-X', 'utf8', '-m', 'tools.reconstructed_game',
            '--config', _relative(config_path, edition), '--frontend', frontend],
        local_source_root='.', original_settings_paths_inherited=False,
        finite_settings_or_save_permissions_changed=False, dependencies_copied=False,
        save_contents_read_or_created=False, native_or_game_or_tests_or_hash_run=False,
        dependency_or_full_game_qualification_claimed=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('edition-root', 'settings', 'output', 'm68k-native-root',
            'sound-native-root', 'chip-library', 'inputs', 'run-output'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--save-path', type=Path,
        help='explicit existing8192-byte local input; required only for settings with save.path')
    parser.add_argument('--frontend', choices=('window', 'console'), required=True)
    args = parser.parse_args(argv)
    try:
        result = materialize_local_gameplay_config(args.edition_root, args.settings, args.output,
            m68k_native_root=args.m68k_native_root, sound_native_root=args.sound_native_root,
            chip_library=args.chip_library, hardware_inputs=args.inputs, run_output=args.run_output,
            frontend=args.frontend, save_path=args.save_path)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, 'Local config authoring stopped: ' + str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
