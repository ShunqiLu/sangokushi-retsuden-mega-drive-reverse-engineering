"""165 actual source bytes with separate growth, animation and battle contracts.

Full-width literals are editable; immutable source diagnostics are not CPU or
natural-state execution. Physical catalogs never replace original guards.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared
from tools.ui_cursor_sprite_templates import codec as sprite

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / 'work/original_g5510.bin'
FORMAL_ROOT = ROOT / 'analysis/parameter_ui_word_sources/generated'
DEFAULT_FIELDS = FORMAL_ROOT / 'fields.json'
OUTPUT_ROOT = ROOT / 'build/parameter_ui_word_sources'
FORMAT = 'g5510-growth-animation-battle-source-fields-v1'
EDITABLE_BYTES = 165
MAX_JSON = 1024 * 1024
MEMBERS = frozenset(('fields.json', 'fields.schema.json', 'validation.json', 'manifest.json'))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
# Physical roles and scalar widths; each source is independently named.
SPECS = (
    ('growth_class_threshold_WORDs', 0x93BE, 0x93F0, 2),
    ('animation_coordinate_WORDs', 0xA42E, 0xA456, 2),
    ('sprite_coordinate_bias_WORDs', 0x1D012, 0x1D022, 2),
    ('prepared_origin_sprite_WORDs', 0x1D022, 0x1D03C, 2),
    ('battle_counter_RAM_pointer_LONGs', 0x3F5F8, 0x3F604, 4),
    ('battle_class_limit_BYTEs_0', 0x3F604, 0x3F60B, 1),
    ('battle_class_limit_BYTEs_1', 0x3F60C, 0x3F613, 1),
    ('battle_class_limit_BYTEs_2', 0x3F614, 0x3F61B, 1),
)
SPANS = tuple((start, end) for _, start, end, _ in SPECS)
GUARDS = (
    (0x9390, 0x93BE, reference_value(__name__, 'GUARDS')),
    (0xA3EC, 0xA42E, reference_value(__name__, 'GUARDS_2')),
    (0x1CFC6, 0x1D012, reference_value(__name__, 'GUARDS_3')),
    (0x3F54C, 0x3F5D0, reference_value(__name__, 'GUARDS_4')),
    (0xAC28, 0xAD06, reference_value(__name__, 'GUARDS_5')),
)
sha, dump = shared.sha, shared.dump
load_fields, read_bounded, put = shared.load_fields, shared.read_bounded, shared.put


def image_bytes(image):
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError('complete immutable image bytes required')


def verify_rom(rom):
    image_bytes(rom)
    if sha(rom) != ROM_SHA256:
        raise ValueError('canonical ROM SHA required')
    for start, end, expected in GUARDS:
        if sha(rom[start:end]) != expected:
            raise ValueError('complete original source consumer differs')


def metadata():
    return dict(format=FORMAT, source_confidence='confirmed', confidence='candidate',
        canonical_source=dict(size=ROM_SIZE, sha256=ROM_SHA256),
        owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
        evidence=dict(raw_layout=LAYOUT_ID, original_consumers=[dict(start=s, end=e, sha256=h) for s,e,h in GUARDS],
            growth=dict(CMP_WORD_postincrement=0x93AC, unsigned_BCS=0x93AE,
                initial_class_WORD=1, class_increment=0x93B2, output_low_BYTE=0x93B6,
                original_sum_WORD='u16(C000.W+BE00.W)', outer_DBRA_WORD=255,
                physical25_thresholds_not_scan_stop=True),
            animation=dict(index_shift=0xA410, reads=[0xA416,0xA41C],
                index_formula='s16(u16(selected_WORD<<2)); second displacement2 after sign extension',
                original_post_increment_unsigned_10_reset=0xA402, physical10_pairs_not_input_clamp=True),
            prepared_sprite=dict(bias_reads=[0x1CFEA,0x1CFF6], bias_index_formula='s16(u16(EFC6_WORD<<1))',
                true_entry=0xAC28, true_JSR=0x1D00A, source=0x1D022,
                D2_cleared=0x1CFFC, camera_copies=[0x1CFFE,0x1D004],
                D3_D4_origins='AC3A..AC50: u16(D0/D1-current_camera_WORD+0080); source view accepts already computed results',
                origin_preparation_PCs=[0xAC3A,0xAC3C,0xAC40,0xAC44,0xAC46,0xAC4A],
                AC28_skips='camera clearing and initial clip-bound setup only, not origin calculation',
                local_read_witness=dict(D3_WORD=128,D4_WORD=128,F300_BYTE=0,
                    supplied_clip_RAM_WORDs=dict(F302=0x70,F304=0x160,F306=0x70,F308=0x1C0),
                    these_bounds_not_initialized_by_AC28=True),
                physical4_records_and_first8000_term=True),
            battle=dict(pointer_reads=[0x3F558,0x3F5C6], pointer_index_formula='s16(u16(8144_WORD<<2))',
                pointers_are_RAM_addresses_not_followed=True, class_BYTE_read=0x3F5AA,
                class_index_formula='s16(u16(u16(8144_WORD<<3)+supplied_class0_to6))',
                class_producer_range=[0x3F55C,0x3F59A], class_upper_bounds=[100,200,300,400,500,600],
                BYTE_values_retained_full=True, excluded_unused_row_BYTEs=[0x3F60B,0x3F613,0x3F61B])),
        business_names_and_natural_selector_domains='unknown', edited_gameplay_safety='unknown',
        independent_CPU_comparison=False, complete_RAM_CCR_stack_bus='not modeled')


def group_fixed(index):
    role, start, end, width = SPECS[index]
    return dict(id=f'rom_{start:06X}_{role}', index=index, role=role,
        start=start, end=end, width_BYTES=width, count=(end-start)//width)


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(), sources=[dict(**group_fixed(i),
        values=[int.from_bytes(rom[p:p+width], 'big') for p in range(start,end,width)])
        for i,(_,start,end,width) in enumerate(SPECS)])


def pinned(row, expected, mutable, label):
    shared.keys(row, set(expected)|set(mutable), label)
    for key, value in expected.items():
        shared.same(row[key], value, label+'.'+key)


def blocks(rom, fields):
    verify_rom(rom)
    pinned(fields, metadata(), {'sources'}, 'source package')
    result=[]
    for i, row in enumerate(shared.exact_list(fields['sources'], len(SPECS), 'physical source groups')):
        fixed=group_fixed(i); pinned(row, fixed, {'values'}, 'physical source')
        width=fixed['width_BYTES']
        values=[shared.uint(v, (1<<(width*8))-1, 'full original scalar')
            for v in shared.exact_list(row['values'], fixed['count'], 'scalar count')]
        if i==3 and (values[-1]!=0x8000 or any(values[p]==0x8000 for p in range(0,12,3))):
            raise ValueError('four records and first8000 X term must remain fixed')
        data=b''.join(v.to_bytes(width,'big') for v in values)
        result.append(dict(id=fixed['id'],start=fixed['start'],end=fixed['end'],data=data,role=fixed['role']))
    if sum(len(r['data']) for r in result)!=EDITABLE_BYTES:
        raise ValueError('exact165-byte cost required')
    return result


def rebuild(rom, fields):
    image=bytearray(rom)
    for row in blocks(rom,fields): image[row['start']:row['end']]=row['data']
    return bytes(image)


def s16(value): return value-65536 if value&0x8000 else value


def read_source(image, address, width):
    if width>1 and address&1:
        raise ValueError('odd original WORD/LONG source boundary')
    if not 0<=address<=ROM_SIZE-width:
        return dict(status='outside_ROM_source_boundary',address=address,width_BYTES=width)
    return dict(status='source_read',address=address,width_BYTES=width,
        value=int.from_bytes(image[address:address+width],'big'),read_addresses=list(range(address,address+width)))


def growth_source_view(image, sum_WORD, scan_budget=256):
    image_bytes(image); value=shared.uint(sum_WORD,65535,'already summed WORD')
    budget=shared.uint(scan_budget,ROM_SIZE//2,'diagnostic scan budget')
    if not budget: raise ValueError('positive scan budget required')
    p=0x93BE; level=1; reads=[]
    for _ in range(budget):
        row=read_source(image,p,2); reads.append(row)
        if row['status']!='source_read': return dict(status=row['status'],reads=reads)
        p+=2
        if value<row['value']:
            return dict(status='original_unsigned_BCS',reads=reads,class_WORD=level,class_BYTE=level&255)
        level=(level+1)&65535
    return dict(status='external_scan_budget',reads=reads,next_source=p,next_class_WORD=level,budget_is_CPU_stop=False)


def animation_source_view(image, selected_WORD):
    image_bytes(image); value=shared.uint(selected_WORD,65535,'already selected animation WORD')
    offset=s16((value<<2)&65535)
    return [read_source(image,0xA42E+offset+d,2) for d in (0,2)]


def bias_source_view(image, EFC6_WORD):
    image_bytes(image); value=shared.uint(EFC6_WORD,65535,'already fetched EFC6 WORD')
    offset=s16((value<<1)&65535)
    return [read_source(image,0x1D012+offset+d,2) for d in (0,2)]


def prepared_sprite_source_view(image, D3_WORD=128, D4_WORD=128, sprite_count_BYTE=0, record_budget=256):
    """D2=0, computed origins and supplied standard clip RAM bounds only.

    AC28 does not initialize F302/F304/F306/F308. The reused narrow helper
    assumes their disclosed 70/160/70/1C0 values, not generic live AC28 state.
    """
    return sprite.source_view(image,0x1D022,D3_WORD,D4_WORD,sprite_count_BYTE,record_budget=record_budget)


def battle_source_view(image, type_WORD, class0_to6):
    image_bytes(image); kind=shared.uint(type_WORD,65535,'already fetched8144 WORD')
    classification=shared.uint(class0_to6,6,'original formed class0..6')
    return dict(pointer=read_source(image,0x3F5F8+s16((kind<<2)&65535),4),
        limit=read_source(image,0x3F604+s16(((kind<<3)+classification)&65535),1),
        RAM_targets_followed=False, catalog_is_CPU_clamp=False)


def constructed_read_union(rom):
    reads=[]
    reads.extend(growth_source_view(rom,2499)['reads'])
    for index in range(10): reads.extend(animation_source_view(rom,index))
    for index in (0,2,4,6): reads.extend(bias_source_view(rom,index))
    for event in prepared_sprite_source_view(rom)['read_events']:
        reads.append(dict(read_addresses=list(range(event['address'],event['address']+2))))
    for kind in range(3):
        for classification in range(7):
            view=battle_source_view(rom,kind,classification);reads.extend((view['pointer'],view['limit']))
    return {p for row in reads for p in row.get('read_addresses',[])}


def schema(rom):
    def walk(value):
        if type(value) is dict:
            props={k:walk(v) for k,v in value.items()}
            return dict(type='object',properties=props,required=list(props),additionalProperties=False)
        if type(value) is list:
            return dict(type='array',prefixItems=[walk(v) for v in value],items=False,minItems=len(value),maxItems=len(value))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    result=walk(extract(rom))
    for i, spec in enumerate(SPECS):
        width=spec[3];items=[dict(type='integer',minimum=0,maximum=(1<<(8*width))-1) for _ in range((spec[2]-spec[1])//width)]
        if i==3:
            items[-1]=dict(type='integer',const=0x8000)
            for p in range(0,12,3): items[p]['not']=dict(const=0x8000)
        result['properties']['sources']['prefixItems'][i]['properties']['values']['prefixItems']=items
    result['$schema']='https://json-schema.org/draft/2020-12/schema'
    return result


def render_bundle(rom):
    fields=extract(rom);rows=blocks(rom,fields);image=rebuild(rom,load_fields(dump(fields)))
    expected={p for s,e in SPANS for p in range(s,e)}
    if image!=rom or constructed_read_union(rom)!=expected or len(expected)!=165:
        raise ValueError('serialized exact ROM or original read union differs')
    report=dict(**metadata(),editable_bytes=165,physical_blocks=len(SPECS),
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),constructed_source_read_union_BYTES=165,
        sprite_witness=prepared_sprite_source_view(rom),
        blocks=[{k:v for k,v in r.items() if k!='data'}|dict(bytes=len(r['data']),sha256=sha(r['data'])) for r in rows])
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=165,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value, formal=False):
    path=shared.safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (formal and path==FORMAL_ROOT):
        raise ValueError('dedicated fresh output or exact formal directory required')
    if path.exists() or not path.parent.is_dir(): raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields')
    parser.add_argument('--bundle');parser.add_argument('--output')
    args=parser.parse_args(argv);target=None
    if args.command=='export':
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError('fresh export output only')
        target=fresh_output(args.output,formal=True)
    elif args.command=='import':
        if args.output is None or args.bundle is not None: raise ValueError('fresh import output required')
        target=fresh_output(args.output)
        if target.suffix.lower()!='.bin': raise ValueError('fresh .bin required')
    elif args.output is not None or (args.fields is not None and args.bundle is not None): raise ValueError('verify is read-only')
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items(): put(target/name,data)
        result=dict(path=str(target),editable_bytes=165,members={name:sha(data) for name,data in members.items()})
    elif args.command=='verify' and args.bundle is not None:
        bundle=shared.safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS: raise ValueError('exact four member bundle required')
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data: raise ValueError('canonical bundle drift:'+name)
        result=dict(verified=True,editable_bytes=165,whole_ROM_exact=True,sha256=ROM_SHA256)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=165,exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__': raise SystemExit(main())
