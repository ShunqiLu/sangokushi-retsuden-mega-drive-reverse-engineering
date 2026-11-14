"""342 original source bytes read by four fixed-count UI record loops.

Three sprite-like templates have37 three-WORD records,222B. The20-row VDP
fill table contributes120B; its66B unread tail remains raw. Field roles are
confirmed by read order, broader visual meaning is candidate, not inferred.
"""
import argparse
import json
from pathlib import Path
from tools.vdp_word_streams import format as shared

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = shared.DEFAULT_ROM
FORMAL_ROOT = ROOT / 'analysis/ui_fixed_records/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/ui_fixed_records'
EDITABLE_BYTES = 342
FORMAT = 'candidate-fixed-UI-three-WORD-fields-v1'
SPECS = ((0x44D8, 13, 'interleaved_template_WORDs', 0x4400),
         (0x4526, 15, 'interleaved_template_WORDs', 0x444A),
         (0x4580, 9, 'interleaved_template_WORDs', 0x4480),
         (0xB66A, 20, 'VDP_command_rowcount_tile_WORDs', 0xB620))
GUARDS = ((0x4400, bytes.fromhex('41fa00d64e7130040240' '00ff3e3c000c32d832c032d832d8524051cffff44e75')),
          (0x4442, bytes.fromhex('08380005f321661e41fa00da4e713004024000ff3e3c000e32d832c032d832d8524051cffff4')),
          (0x4480, bytes.fromhex('41fa00fe4e7130040240' '00ff3e3c000832d832c032d832d85240524451cffff2')),
          (0xB620, bytes.fromhex('41fa00483e3c001370003018e588e44800404000484032182a80341861000022524226000683008000002a836100001206800004000051c9ffe051cfffcc4e7536023883544338834e75')))
sha, dump, load_fields = shared.sha, shared.dump, shared.load_json


def ident(start): return f'rom_{start:06X}_fixed_records'


def metadata():
    return dict(format=FORMAT, canonical_source=dict(size=shared.ROM_SIZE, sha256=shared.ROM_SHA),
                confidence='confirmed_fixed_read_encoding_candidate_UI_role', owner_bytes_added=0,
                natural_domains_added=0, complete_domains_added=0)


def topology(spec):
    start, count, kind, caller = spec
    return dict(id=ident(start), start=start, end=start + 6 * count, records=count,
                record_WORDs=3, kind=kind, original_source_LEA=caller)


def exact(value, count, label):
    if type(value) is not list or len(value) != count: raise ValueError(label + ': fixed allocation differs')
    return value


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != shared.ROM_SIZE or sha(rom) != shared.ROM_SHA:
        raise ValueError('canonical ROM identity required')
    for pc, raw in GUARDS:
        if rom[pc:pc + len(raw)] != raw: raise ValueError('original fixed-count consumer differs')


def extract(rom):
    verify_rom(rom); fields = metadata()
    fields['groups'] = [dict(**topology(spec), rows=[dict(source_WORD0=int.from_bytes(rom[p:p + 2], 'big'),
        source_WORD1=int.from_bytes(rom[p + 2:p + 4], 'big'), source_WORD2=int.from_bytes(rom[p + 4:p + 6], 'big'))
        for p in range(spec[0], spec[0] + spec[1] * 6, 6)]) for spec in SPECS]
    blocks(rom, fields); return fields


def blocks(rom, fields):
    verify_rom(rom); shared.keys(fields, set(metadata()) | {'groups'}, 'package')
    for key, value in metadata().items(): shared.same(fields[key], value, 'package.' + key)
    result = []
    for group, spec in zip(exact(fields['groups'], 4, 'groups'), SPECS):
        fixed = topology(spec); shared.keys(group, set(fixed) | {'rows'}, 'group')
        for key, value in fixed.items(): shared.same(group[key], value, 'group.' + key)
        data = bytearray()
        for row in exact(group['rows'], spec[1], 'three-WORD records'):
            shared.keys(row, {'source_WORD0', 'source_WORD1', 'source_WORD2'}, 'record')
            for key in ('source_WORD0', 'source_WORD1', 'source_WORD2'):
                data.extend(shared.uint(row[key], 65535, 'complete source WORD').to_bytes(2, 'big'))
        result.append(dict(id=group['id'], start=group['start'], end=group['end'], data=bytes(data), role=group['kind']))
    if sum(len(row['data']) for row in result) != EDITABLE_BYTES: raise ValueError('fixed342 source cost differs')
    return result


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields): image[row['start']:row['end']] = row['data']
    return bytes(image)


def template_output(rom, fields, group_index, d4_WORD):
    """Pure interleaving projection; excludes gates/RAM writes/VDP lifetime."""
    blocks(rom, fields); index = shared.uint(group_index, 2, 'three-template editor index')
    d4 = shared.uint(d4_WORD, 65535, 'D4 WORD'); tile = d4 & 255; result = []
    for row in fields['groups'][index]['rows']:
        result.append([row['source_WORD0'], tile, row['source_WORD1'], row['source_WORD2']])
        tile = (tile + 1) & 65535
        if index == 2: d4 = (d4 + 1) & 65535
    return dict(output_WORD_records=result, final_D4_WORD=d4)


def render_bundle(rom):
    fields = extract(rom); image = rebuild(rom, load_fields(dump(fields)))
    if image != rom or image[0xB6E2:0xB724] != rom[0xB6E2:0xB724]: raise ValueError('exact roundtrip/unread preservation differs')
    report = dict(**metadata(), editable_bytes=342, template_bytes=222, VDP_fill_source_bytes=120,
        template_records=37, VDP_fill_records=20, full_WORD_fields=171, whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        original_consumer_guards=[dict(start=pc, end=pc + len(raw), bytes=raw.hex()) for pc, raw in GUARDS],
        template_read_order='sourceWORD0; generated D0.W; sourceWORD1; sourceWORD2',
        template_initial_D0='D4.W AND00FF; per-record ADDQ.W1 without remasking',
        VDP_fill_read_order='command WORD; vertical DBRA count WORD; tile WORD; original B660 outputs D2/D2+2 then D2+1/D2+3',
        VDP_fill_source_count='20 outer DBRA rows, each exactly3 WORD reads regardless of inner output count',
        unknown_intervals=[[0xB6E2, 0xB724]], unread_bytes_excluded=66,
        fields_are_complete_WORDs=True, independent_CPU_comparison=False, complete_renderer_reimplemented=False,
        edited_gameplay_safety='unknown')
    members = {'fields.json': dump(fields), 'validation.json': dump(report)}
    members['manifest.json'] = dump(dict(**metadata(), editable_bytes=342,
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value):
    path = shared.safe_path(value)
    if path != FORMAL_ROOT and (path == OUTPUT_ROOT or OUTPUT_ROOT not in path.parents):
        raise ValueError('output must be fresh formal directory or beneath build/ui_fixed_records')
    if path.exists() or not path.parent.is_dir(): raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=('export', 'import', 'verify')); p.add_argument('--rom', default=str(DEFAULT_ROM))
    p.add_argument('--fields', default=str(DEFAULT_FIELDS)); p.add_argument('--output'); args = p.parse_args(argv)
    target = None
    if args.command != 'verify':
        if args.output is None: raise ValueError('fresh output required')
        target = fresh_output(args.output)
        if args.command == 'import' and target.suffix.lower() != '.bin': raise ValueError('fresh .bin required')
    elif args.output is not None: raise ValueError('verify does not write')
    rom = shared.read_bounded(args.rom, shared.ROM_SIZE)
    if args.command == 'export':
        members = render_bundle(rom); target.mkdir()
        for name, data in members.items(): shared.put(target / name, data)
        result = dict(path=str(target), editable_bytes=342, members={name: sha(data) for name, data in members.items()})
    else:
        image = rebuild(rom, load_fields(shared.read_bounded(args.fields, shared.MAX_JSON)))
        if target is not None: shared.put(target, image)
        result = dict(path=None if target is None else str(target), exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True)); return 0


if __name__ == '__main__': raise SystemExit(main())
