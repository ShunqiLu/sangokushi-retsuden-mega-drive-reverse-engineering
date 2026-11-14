'Build the two Z80 code images from explicit current logical source texts.\n\nThe caller supplies a fresh output child, dedicated output root and tool root.\nWhole admitted normalized AST snapshots are published in the exact format the\nexisting runtime source/COFF/image verifier consumes; no private research root\nor old native product is selected. Sparse gaps have no code coverage credit.\nOriginal-ROM comparison, behavior and final acceptance remain separate work.\n'
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Mapping

from ..high_level_rom import z80_coff as _z80_coff
from ..high_level_rom.z80_coff import MAX_OBJECT_SIZE


PROJECT_ROOT = Path(__file__).resolve().parents[2]




def _wsl_path(path: Path) -> str:
    resolved = path.resolve()
    if len(resolved.drive) != 2 or resolved.drive[1] != ':' or not resolved.is_absolute():
        raise ValueError('an absolute local Windows drive path is required')
    return '/mnt/' + resolved.drive[0].lower() + '/' + '/'.join(resolved.parts[1:])


def _unit_shape(unit: str, descriptor: Mapping) -> tuple[list[dict], int, dict[str, int]]:
    """Compatibility entry; the complete shape algorithm is owned by z80_coff."""
    return _z80_coff._unit_shape(unit, descriptor)


def verify_object(unit: str, descriptor: dict, object_data: bytes, image: bytes) -> dict:
    """Compatibility entry for the unchanged complete pure Z80 COFF validator."""
    return _z80_coff.verify_object(unit, descriptor, object_data, image)


def _fresh_audio_output(output: Path, output_root: Path, tool_root: Path) -> Path:
    """Accept only a fresh child of an explicit ordinary output authority."""
    import stat

    def ordinary_path(value, label, *, existing):
        if not isinstance(value, Path):
            raise ValueError('explicit pathlib.Path required: ' + label)
        raw = str(value)
        if raw.startswith(('\\\\', '//', '\\?\\', '\\.\\')) or ':' in raw[2:]:
            raise ValueError('UNC/device/alternate-stream path refused: ' + label)
        absolute = value.absolute()
        for ancestor in (absolute, *absolute.parents):
            reparse = (ancestor.is_symlink() or getattr(ancestor, 'is_junction', lambda: False)()
                or (ancestor.exists() and bool(getattr(ancestor.stat(), 'st_file_attributes', 0)
                    & stat.FILE_ATTRIBUTE_REPARSE_POINT)))
            if reparse:
                raise ValueError('path through reparse point refused: ' + label)
        return absolute.resolve(strict=existing)

    root = ordinary_path(output_root, 'output_root', existing=True)
    tools = ordinary_path(tool_root, 'tool_root', existing=True)
    if not root.is_dir() or root == Path(root.anchor) or root == PROJECT_ROOT.resolve():
        raise ValueError('an existing dedicated output-root directory, not a volume/project root, is required')
    if not tools.is_dir():
        raise ValueError('an existing explicit Z80 tool directory is required')
    candidate = output if output.is_absolute() else root / output
    result = ordinary_path(candidate, 'output', existing=False)
    if result.exists() or result == root or not result.is_relative_to(root):
        raise ValueError('an absent dedicated child of the explicit output root is required')
    if (result.is_relative_to(tools) or tools.is_relative_to(result)
            or result.is_relative_to((PROJECT_ROOT / 'tools').resolve())):
        raise ValueError('audio output must be separate from toolchain and project Python source directories')
    return result


def _normalized_audio_snapshots(sources: Mapping[str, str]) -> dict[str, str]:
    """Use the very same whole normalized ASTs required by the existing loader.

    This is a real compiler._admit call on the frozen logical inputs, not a
    filename projection, original snapshot copy or independent normalization.
    Generation retains its original admission too; neither check is bypassed.
    """
    import ast
    from .compiler import _admit

    trees, unused_count = _admit(sources)
    result = {}
    for name, tree in trees.items():
        if (type(name) is not str or Path(name).name != name or not name.endswith('.py')
                or type(tree) is not ast.Module):
            raise ValueError('complete named admitted audio module AST required')
        # The consumer parses these exact whole snapshots and compares its own
        # current admitted AST. No CodeType, opcode, old reference or result is
        # substituted for that complete source relation.
        result[name] = ast.unparse(tree) + '\n'
    if not result:
        raise ValueError('the complete nonempty admitted audio source set is required')
    return result


def compile_sources(sources: Mapping[str, str], output: Path, tool_root: Path, *, output_root: Path) -> dict:
    """Build locally from explicit current sources and external tool/output roots.

    All original instruction/COFF/image checks are retained. The only source
    snapshots published are the actual admitted normalized modules expected by
    load_compiled_sound_copy_data, not the newer domain facade input texts.
    """
    from .compiler import generate
    from .target import UNITS

    if not isinstance(sources, Mapping):
        raise ValueError('explicit logical-module-to-source-text mapping required')
    logical_sources = dict(sources)
    # Admission/generation still precede every filesystem write/native child.
    # Freeze the same immutable source strings for both exact admission paths.
    generated = generate(logical_sources)
    if type(generated) is not dict or set(generated) != {'driver', 'startup'}:
        raise ValueError('both complete separate audio code images are required')
    snapshots = _normalized_audio_snapshots(logical_sources)
    output = _fresh_audio_output(output, output_root, tool_root)
    for unit, assembly in generated.items():
        _unit_shape(unit, UNITS[unit])
        if type(assembly) is not str or len(assembly) > 1_000_000:
            raise ValueError('bounded explicit generated assembly text required')
        assembly.encode('ascii')
    tool_root = tool_root.resolve(strict=True)
    output.mkdir(parents=True)
    for name, source in snapshots.items():
        with (output / ('source-' + name)).open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(source)
    receipt = {'commands': [], 'child_exits': [], 'actual_units': {}, 'parent_exit': None,
               'original_generation_input': False, 'opaque_opcode_payload': False,
               'complete_ROM': False, 'complete_CPU': False, 'jointly_closed': False,
               'new_matching_bytes': 0, 'new_strict_bytes': 0,
               'source_snapshot_format': 'g5510-admitted-normalized-audio-source-snapshots-v1',
               'logical_input_modules': sorted(logical_sources),
               'normalized_snapshot_modules': sorted(snapshots),
               'logical_input_count': len(logical_sources),
               'normalized_snapshot_count': len(snapshots),
               'source_snapshot_authority': 'complete actual compiler._admit ASTs from the same frozen logical inputs',
               'runtime_loader_contract': 'unchanged complete normalized source/COFF/image verification',
               'explicit_output_root': str(output_root.resolve(strict=True)),
               'prebuilt_machine_code_copied': False}
    try:
        for unit in ('driver', 'startup'):
            assembly, obj, image = output / (unit + '.s'), output / (unit + '.o'), output / (unit + '.bin')
            assembly.write_text(generated[unit], encoding='ascii', newline='\n')
            commands = [
                ['wsl.exe', '--exec', _wsl_path(tool_root / 'z80-unknown-coff-as'),
                 '-march=z80', '-o', _wsl_path(obj), _wsl_path(assembly)],
                ['wsl.exe', '--exec', _wsl_path(tool_root / 'z80-unknown-coff-objcopy'),
                 '-O', 'binary', '-j', '.text', _wsl_path(obj), _wsl_path(image)],
            ]
            for command in commands:
                process = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
                receipt['commands'].append({'command': command, 'exit_code': process.returncode,
                                            'stdout': process.stdout, 'stderr': process.stderr})
                receipt['child_exits'].append(process.returncode)
                if process.returncode:
                    raise RuntimeError(f'{unit} native child failed: {process.stderr}')
            receipt['actual_units'][unit] = verify_object(unit, UNITS[unit], obj.read_bytes(), image.read_bytes())
        receipt['generated_target_bytes'] = sum(row['instruction_bytes'] for row in receipt['actual_units'].values())
        receipt['parent_exit'] = 0
    except Exception as error:
        receipt['parent_exit'] = 1
        receipt['error'] = str(error)
        raise
    finally:
        (output / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return receipt


def main(argv=None) -> int:
    from .target import BUSINESS_MODULES

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', type=Path, required=True,
        help='explicit existing dedicated publication root; never a private-machine default')
    parser.add_argument('--output', type=Path, required=True,
        help='new child path; relative paths are resolved only against --output-root')
    parser.add_argument('--tool-root', type=Path, required=True,
        help='explicit existing Z80 GNU tools directory; no toolchain is downloaded or copied')
    args = parser.parse_args(argv)
    source_root = Path(__file__).resolve().parent
    sources = {name: (source_root / name).read_text(encoding='utf-8') for name in BUSINESS_MODULES}
    receipt = compile_sources(sources, args.output, args.tool_root, output_root=args.output_root)
    print(json.dumps({key: receipt[key] for key in ('child_exits', 'generated_target_bytes',
        'logical_input_count', 'normalized_snapshot_count', 'parent_exit')}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
