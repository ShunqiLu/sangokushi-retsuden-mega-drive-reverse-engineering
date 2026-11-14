"""40 source WORDs, real low-WORD indexing/sign gate and low-BYTE projection."""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from tools.direct_code import direct_code as d

f = d.f
ROOT = d.ROOT
FORMAL_ROOT = ROOT / 'analysis/scene_audio_command_word_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/scene_audio_command_word_fields'
FORMAT = 'g5510-scene-audio-command-source-WORD-fields-v1'
START, END, COUNT = 0x10830, 0x10880, 40
EDITABLE_BYTES = END - START
GUARDS = (
    (0x1075A, 0x1075E, reference_value(__name__, 'GUARDS')),
    (0x10814, 0x10830, reference_value(__name__, 'GUARDS_2')),
    (0x10880, 0x10896, reference_value(__name__, 'GUARDS_3')),
    (0x808A, 0x80D0, reference_value(__name__, 'GUARDS_4')),
)
sha, dump, load_fields = f.sha, f.dump, f.load_json


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=f.ROM_SIZE, sha256=f.ROM_SHA),
                confidence='confirmed_source_encoding_probable_scene_audio_role',
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0)


def topology():
    return dict(id='rom_010830_scene_audio_command_WORDs', start=START, end=END,
                source_WORDs=COUNT, WORD_order='big', original_read_PC=0x1081C,
                selector_read_PC=0x10814, selector_bus_RAM=0xFF7026,
                result_write_PC=0x10820, result_bus_RAM=0xFFEFD0,
                editor_count_is_CPU_clamp=False)


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError('immutable canonical ROM bytes required')
    f.verify_rom(rom)
    for start, end, digest in GUARDS:
        if sha(rom[start:end]) != digest:
            raise ValueError('original consumer/caller/audio sender differs')
    if rom[0x1081A:0x10820] != bytes.fromhex('e348303b0012'):
        raise ValueError('original LSL.W1 and PC-indexed D0.W differ')
    if 0x1081E + int.from_bytes(rom[0x1081F:0x10820], 'big', signed=True) != START:
        raise ValueError('original PC-relative source differs')
    if rom[END:END + 4] != bytes.fromhex('4a78efd0'):
        raise ValueError('next original compiled boundary differs')


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(), table=dict(**topology(), WORDs=[
        int.from_bytes(rom[p:p + 2], 'big') for p in range(START, END, 2)]))


def blocks(rom, fields):
    verify_rom(rom)
    f.keys(fields, set(metadata()) | {'table'}, 'scene audio package')
    for key, value in metadata().items():
        f.same(fields[key], value, 'package.' + key)
    table = fields['table']
    fixed = topology()
    f.keys(table, set(fixed) | {'WORDs'}, 'source table')
    for key, value in fixed.items():
        f.same(table[key], value, 'table.' + key)
    words = table['WORDs']
    if type(words) is not list or len(words) != COUNT:
        raise ValueError('exact40 physical source WORDs required')
    data = b''.join(f.uint(value, 65535, 'complete source WORD').to_bytes(2, 'big') for value in words)
    return [dict(id=table['id'], start=START, end=END, data=data,
                 role='original_scene_audio_command_BE16_source_fields')]


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def selection(rom, fields, selector_WORD):
    """Value at10814; source/branch projection, never a live-RAM CPU wrapper.

    LSL.W1 wraps before sign extension. Source WORD sign controls BMI, while
    the unchanged audio sender queues only its low BYTE if eventually called.
    Mailbox/device/IRQ/stack acceptance is not executed or inferred here.
    """
    f.uint(selector_WORD, 65535, 'original FF7026 low WORD at read')
    image = rebuild(rom, fields)
    index = (selector_WORD << 1) & 65535
    signed = index - 65536 if index & 32768 else index
    logical = (START + signed) & 0xFFFFFFFF
    address = logical & 0xFFFFFF
    if address & 1 or address + 2 > len(image):
        raise ValueError('original WORD source read boundary')
    value = int.from_bytes(image[address:address + 2], 'big')
    negative = bool(value & 32768)
    return dict(selector_WORD=selector_WORD, shifted_D0_WORD=index, signed_index=signed,
                original_read_PC=0x1081C, source_logical_address=logical,
                source_bus_address=address, source_WORD=value,
                inside_editor_catalog=START <= address and address + 2 <= END,
                result_logical_RAM=0xFFFFEFD0, result_bus_RAM=0xFFEFD0,
                stored_WORD=value, BMI_taken=negative, conditional_audio_entry=None if negative else 0x808A,
                conditional_queue_BYTE=None if negative else value & 255,
                JSR_executed=False, mailbox_write_executed=False, complete_CPU_entry=False)


def raw_guard(base):
    raw = d.raw_positions(base)
    if not set(range(START, END)) <= raw:
        raise ValueError('all80 source positions must remain sole raw authority')
    return dict(guarded_raw_bytes=80, layout_remaining_raw=len(raw), next_original_code_not_raw=END not in raw)


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError('serialized whole-ROM roundtrip differs')
    views = [selection(rom, fields, i) for i in range(COUNT)]
    source_union = {p for row in views for p in range(row['source_bus_address'], row['source_bus_address'] + 2)}
    if source_union != set(range(START, END)):
        raise ValueError('constructed physical source read union differs')
    report = dict(**metadata(), editable_bytes=80, full_BE16_source_fields=40,
        whole_ROM_exact=True, whole_ROM_sha256=sha(image), constructed_source_union_bytes=len(source_union),
        positive_audio_entries=sum(not row['BMI_taken'] for row in views), negative_skip_entries=sum(row['BMI_taken'] for row in views),
        source_table_sha256=sha(rom[START:END]), original_last_WORD=fields['table']['WORDs'][-1],
        next_original_PC=END, original_source_guards=[dict(start=a, end=z, sha256=h, physical_emit=False) for a, z, h in GUARDS],
        natural_input_domains='unknown', independent_CPU_comparison=False, complete_CPU_entry=False,
        prior_read_only_evidence=['analysis/audio_natural/SCOUT.md:sections1,4', 'analysis/audio_sequences/DRIVER_LIFETIME_SCOUT.md:section4'],
        prior_capture_scope='Existing no-injection saved-state-relative index7->009F route; not rerun or expanded here.',
        limitations=['40 editor slots are a physical allocation, never a CPU index clamp.',
            'Full source WORD sign controls BMI; the queue BYTE alone cannot describe branch behavior.',
            'FF7026 has a documented renderer BYTE alias; parameters are values at the original read.',
            'Sender bus grant/queue occupancy/IRQ/stack/Z80 acceptance and playback remain outside this field codec.',
            'Overreads remain reads of original neighboring bytes, not newly admitted fields.'])
    members = {'fields.json': dump(fields), 'validation.json': dump(report)}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=80,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value):
    path = f.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('fresh formal directory or dedicated build/scene_audio_command_word_fields required')
    if path.exists() or not path.parent.is_dir():
        raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('export', 'import', 'verify'))
    parser.add_argument('--rom', default=str(f.DEFAULT_ROM))
    parser.add_argument('--fields', default=str(DEFAULT_FIELDS))
    parser.add_argument('--output')
    args = parser.parse_args(argv)
    target = None
    if args.command != 'verify':
        if args.output is None:
            raise ValueError('fresh output required')
        target = fresh_output(args.output)
        if args.command == 'import' and target.suffix.lower() != '.bin':
            raise ValueError('fresh .bin required')
    elif args.output is not None:
        raise ValueError('verify does not write')
    rom = f.read_bounded(args.rom, f.ROM_SIZE)
    if args.command == 'export':
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            f.put(target / name, data)
        result = dict(path=str(target), editable_bytes=80, members={name: sha(data) for name, data in members.items()})
    else:
        image = rebuild(rom, load_fields(f.read_bounded(args.fields, f.MAX_JSON)))
        if target is not None:
            f.put(target, image)
        result = dict(path=None if target is None else str(target), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
