"""Conditional source BYTEs read by the original city-neighbour caller.

The original F68A WORD selects two live ROM WORDs. Six true 17EBA calls
read the resulting neighbour addresses; their cost reads may map to RAM.
This is source encoding recovery, not natural city selection or atlas ownership.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
from bisect import bisect_left
from functools import lru_cache
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent/'work/original_g5510.bin'
OUTPUT_ROOT = ROOT/'build/city_neighbor_source_alias_fields'
FORMAL_ROOT = ROOT/'analysis/city_neighbor_source_alias_fields/generated'
DEFAULT_FIELDS = FORMAL_ROOT/'fields.json'
DEFAULT_BUNDLE = FORMAL_ROOT
FORMAT = 'g5510-city-ROM-coordinate-neighbour-source-BYTE-alias-v1'
EDITABLE_BYTES = 8247
PHYSICAL_BLOCKS = 2252
SOURCE_FIRST, SOURCE_LIMIT = 0xF2EF0, 0xF8000
SOURCE_BASE, PAIR_BASE, COST_BASE = 0xEE5F0, 0xD4AC6, 0x670A
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
MEMBERS = frozenset(('fields.json','fields.schema.json','validation.json','manifest.json'))
MAX_JSON = 8*1024*1024
CALLS = (0x17D5E,0x17D72,0x17D88,0x17D9E,0x17DB2,0x17DC8)
BODIES = (
    (0x17C8A,0x17CC6,reference_value(__name__, 'BODIES')),
    (0x17D3C,0x17DDC,reference_value(__name__, 'BODIES_2')),
    (0x17E3C,0x17EBA,reference_value(__name__, 'BODIES_3')),
    (0x17EBA,0x17EDE,reference_value(__name__, 'BODIES_4')),
)
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH = 'build/direct_code/layout/'+LAYOUT_ID+'/m68k_bank0f.s'
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
MAP_PATH = 'analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv'
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
load_fields = shared.load_fields
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def _s16(value):
    return value if value < 0x8000 else value-0x10000


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError('canonical complete ROM bytes, size and SHA-256 required')
    for start, end, digest in BODIES:
        if sha(rom[start:end]) != digest:
            raise ValueError('original caller/control/helper bytes differ')


def _coalesce(addresses):
    spans = []
    for address in addresses:
        if spans and spans[-1][1] == address:
            spans[-1][1] += 1
        else:
            spans.append([address,address+1])
    return tuple(tuple(row) for row in spans)


def _pair(image, selector_WORD):
    shifted = (selector_WORD << 2)&0xFFFF
    address = PAIR_BASE+_s16(shifted)
    x = int.from_bytes(image[address:address+2],'big')
    y = int.from_bytes(image[address+2:address+4],'big')
    return address, x, y


def _coordinates(x_WORD, y_WORD):
    """The six original caller WORD positions; no semantic coordinate clamp."""
    y, x = ((y_WORD >> 4)-1)&0xFFFF, ((x_WORD >> 4)-1)&0xFFFF
    yield y, x
    x = (x+1)&0xFFFF
    yield y, x
    y, x = (y+1)&0xFFFF, (x+1)&0xFFFF
    yield y, x
    y, x = (y+1)&0xFFFF, (x-1)&0xFFFF
    yield y, x
    x = (x-1)&0xFFFF
    yield y, x
    y, x = (y-1)&0xFFFF, (x-1)&0xFFFF
    yield y, x


@lru_cache(maxsize=2)
def _catalog(rom):
    """Immutable canonical witnesses, derived from original live ROM WORDs."""
    verify_rom(rom)
    selected = {}
    for selector in range(0x4000):
        _, x, y = _pair(rom,selector)
        for slot, (yw,xw) in enumerate(_coordinates(x,y)):
            address = SOURCE_BASE+_s16((72*yw+xw)&0xFFFF)
            if SOURCE_FIRST <= address < SOURCE_LIMIT:
                selected.setdefault(address,(selector,slot))
    rows = tuple((address,*selected[address]) for address in sorted(selected))
    if len(rows) != EDITABLE_BYTES or len(_coalesce(row[0] for row in rows)) != PHYSICAL_BLOCKS:
        raise ValueError('fixed original source witness union differs')
    if sha(bytes(rom[row[0]] for row in rows)) != SOURCE_SHA256:
        raise ValueError('original witnessed source BYTE digest differs')
    return rows


def physical_positions(rom):
    if type(rom) is not bytes:
        raise ValueError('canonical complete ROM bytes required')
    return tuple(row[0] for row in _catalog(rom))


def witness(rom, address):
    if type(rom) is not bytes:
        raise ValueError('canonical complete ROM bytes required')
    address = uint(address,ROM_SIZE-1,'physical source BYTE address')
    rows = _catalog(rom)
    slot_index = bisect_left(rows,(address,-1,-1))
    if slot_index == len(rows) or rows[slot_index][0] != address:
        raise ValueError('address outside the unique physical source scope')
    _, selector, slot = rows[slot_index]
    pair_address, x, y = _pair(rom,selector)
    return dict(address=address,selector_WORD=selector,
        selector_aliases=[selector+k*0x4000 for k in range(4)],callback_slot=slot,
        read_PC=0x17ECE,pair_address=pair_address,source_x_WORD=x,source_y_WORD=y)


def _read(image, ram, address, size, PC):
    """68000 WORD alignment and 32-bit CPU/24-bit bus ROM or RAM reads."""
    address &= 0xFFFFFFFF
    if size > 1 and address&1:
        raise ValueError('original WORD address error at '+f'{address:08X}')
    values, kinds = [], set()
    for displacement in range(size):
        bus = (address+displacement)&0xFFFFFF
        if bus < ROM_SIZE:
            values.append(image[bus]); kinds.add('ROM')
        elif 0xFF0000 <= bus <= 0xFFFFFF:
            values.append(ram[bus-0xFF0000]); kinds.add('RAM')
        else:
            raise ValueError('read outside supplied ROM/RAM at '+f'{bus:06X}')
    return dict(PC=PC,address=address,bus_address=address&0xFFFFFF,bytes=size,
        value=int.from_bytes(bytes(values),'big'),memory='/'.join(sorted(kinds)))


def _write(ram, address, value, size, PC):
    bus = address&0xFFFFFF
    if not 0xFF0000 <= bus <= 0x1000000-size or size > 1 and address&1:
        raise ValueError('original supplied-frame RAM write boundary')
    ram[bus-0xFF0000:bus-0xFF0000+size] = value.to_bytes(size,'big')
    return dict(PC=PC,address=address&0xFFFFFFFF,bus_address=bus,bytes=size,value=value)


def source_view(image, selector_WORD, source_BYTE_budget=6):
    """Constructed true caller prefix, stopping before unmodeled post-query work.

F6D6.W=1 makes the real 17E3C count helper return D6.W=1. F6EA.W=FFFF
takes the original 17CA8 BMI to the true 17CC2 BSR. The complete RAM frame
otherwise starts at zero, with F68A.W supplied. These are conditional states,
not evidence that the natural game produces every selector.
"""
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError('diagnostic requires a complete edited bytes image')
    selector = uint(selector_WORD,0xFFFF,'complete supplied F68A WORD')
    budget = uint(source_BYTE_budget,6,'diagnostic source BYTE budget')
    for start, end, digest in BODIES:
        if sha(image[start:end]) != digest:
            raise ValueError('original control bytes changed; source reachability is not proven')
    ram = bytearray(0x10000)
    ram[0xF68A:0xF68C] = selector.to_bytes(2,'big')
    ram[0xF6D6:0xF6D8] = b'\x00\x01'
    ram[0xF6EA:0xF6EC] = b'\xFF\xFF'
    writes = [_write(ram,0xFFFFFE7C,0x17C8E,4,0x17C8A)]
    result = dict(selector_WORD=selector,source_BYTES=0,source_reads=[],cost_reads=[],
        RAM_writes=writes,caller_entry=0x17C8A,true_BSR_PC=0x17CC2,
        count_helper_D6_WORD=1,packet_gate_WORD=0xFFFF,source_BYTE_budget=budget,
        budget_is_original_CPU_stop=False,natural_domain='unknown',complete_CPU=False,
        source_values_are_not_cost_indices=True)
    pointer = int.from_bytes(image[0x17C7E:0x17C82],'big')
    result['live_old_pointer'] = dict(PC=0x17CA0,address=0x17C7E,BE32=pointer)
    try:
        result['live_old_pointer_WORD'] = _read(image,ram,pointer,2,0x17CA4)
    except ValueError as error:
        return dict(**result,status='old_pointer_read_boundary',boundary=str(error))
    writes.append(_write(ram,0xFFFFFE7C,0x17CC6,4,0x17CC2))
    pair_address, x, y = _pair(image,selector)
    result.update(pair_address=pair_address,source_x_WORD=x,source_y_WORD=y,
        pair_read_PCs=[0x17D4E,0x17D54],pair_source_WORDs_are_live=True)
    list_address, count = 0xFFFFA954, 0
    for slot, ((yw,xw), pc) in enumerate(zip(_coordinates(x,y),CALLS)):
        if len(result['source_reads']) >= budget:
            result.update(source_BYTES=len(result['source_reads']),D3_WORD=count)
            return dict(**result,status='diagnostic_source_BYTE_budget_exhausted',boundary_PC=pc)
        writes.append(_write(ram,0xFFFFFE78,pc+4,4,pc))
        index = (72*yw+xw)&0xFFFF
        source = _read(image,ram,SOURCE_BASE+_s16(index),1,0x17ECE)
        source.update(BYTE=source.pop('value'),callback_slot=slot,index_WORD=index,
            derived_y_WORD=yw,derived_x_WORD=xw,true_JSR_PC=pc,
            inside_fixed96_raw_zero_span=SOURCE_FIRST <= source['address'] < SOURCE_LIMIT)
        result['source_reads'].append(source)
        # The extension WORD 4000 is used by both original MOVE.Bs: D4.W.
        cost = _read(image,ram,(COST_BASE+_s16(index))&0xFFFFFFFF,1,0x17ED8)
        cost.update(BYTE=cost.pop('value'),callback_slot=slot,index_WORD=index,
            overwrites_source_BYTE_in_D2=True)
        result['cost_reads'].append(cost)
        if not cost['BYTE']&0x80:
            value = ((yw&0xFF)<<8)|(xw&0xFF)
            writes.append(_write(ram,list_address,value,2,pc+14))
            list_address += 2
            count = (count+1)&0xFFFF
    result.update(source_BYTES=len(result['source_reads']),D3_WORD=count,
        final_source_prefix_PC=0x17DDA,return_from_query_caller_PC=0x17CC6,
        post_query_17DDC_work_simulated=False)
    return dict(**result,status='six_original_source_queries_completed')


def metadata(rom):
    positions = physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditional_source_encoding',
        resource_role='candidate_city_neighbour_literal_BYTE_source_alias',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),source_union_BYTES=EDITABLE_BYTES,
        source_union_sha256=SOURCE_SHA256,physical_blocks=PHYSICAL_BLOCKS,
        physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in _coalesce(positions)],
        raw_baseline=dict(layout_id=LAYOUT_ID,raw_BYTES=22576,
            source_all_fixed_raw=True,bank_path=LAYOUT_PATH,bank_sha256=LAYOUT_SHA256),
        evidence=dict(original_map=dict(path=MAP_PATH,sha256=MAP_SHA256),
            controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES],
            caller=dict(entry=0x17C8A,count_BSR_PC=0x17C8A,count_entry=0x17E3C,
                F6D6_WORD=1,F6EA_WORD=65535,true_query_BSR_PC=0x17CC2,query_entry=0x17D3C,
                old_pointer_read_PC=0x17CA0,old_pointer_address=0x17C7E,
                pointer_data_live_not_pinned_as_code=True),
            pair=dict(input_RAM_WORD=0xFFFFF68A,shift_WORD_PC=0x17D46,base=PAIR_BASE,
                read_PCs=[0x17D4E,0x17D54],source_WORDs_complete_big_endian=True,
                formula='D4AC6 + s16((F68A.W << 2) & FFFF)',source_WORD_shift=4),
            queries=dict(true_JSR_PCs=list(CALLS),entry=0x17EBA,source_read_PC=0x17ECE,
                source_base=SOURCE_BASE,cost_read_PC=0x17ED8,cost_base=COST_BASE,
                both_effective_addresses_use_D4_WORD=True,index_formula='s16((72*y.W+x.W)&FFFF)',
                RAM_cost_is_normal_read_not_CPU_stop=True,cost_BYTE_only_gates_list_append=True,
                cost_overwrites_source_BYTE_before_return=True,native_source_queries=6,
                distinct_pair_starts=16384,complete_supplied_WORD_inputs=65536,
                canonical_source_read_union_BYTES=35875),
            frame=dict(RAM_BYTES=65536,initial_zero_except_declared_fields_and_original_stack_writes=True,
                initial_SP=0xFFFFFE80,append_RAM=0xFFFFA954,natural_state_proof=False)),
        editing_authority='one complete physical BYTE; old WORD/pointer/cost sources remain live read-only views',
        padding_or_free_space_claimed=False,owner_bytes_added=0,natural_domains_added=0,
        complete_domains_added=0,complete_function_recovery=False,independent_CPU_comparison=False,
        primary_terrain_role='unknown',natural_city_selector_domain='unknown',edited_gameplay_safety='unknown')


def extract(rom):
    result = metadata(rom)
    result['source_BYTEs'] = [dict(address=a,BYTE=rom[a]) for a in physical_positions(rom)]
    return result


def blocks(rom, fields):
    fixed = metadata(rom)
    keys(fields,set(fixed)|{'source_BYTEs'},'city neighbour source package')
    for key, value in fixed.items():
        same(fields[key],value,'package.'+key)
    addresses = physical_positions(rom)
    data = {}
    for address, row in zip(addresses,exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'physical source BYTEs')):
        keys(row,{'address','BYTE'},'source BYTE')
        same(row['address'],address,'source address/order')
        data[address] = uint(row['BYTE'],255,'full source BYTE bits')
    return [dict(id=f'rom_{a:06X}_city_neighbour_source_BYTEs',start=a,end=z,
        data=bytes(data[p] for p in range(a,z)),role='candidate_conditional_city_neighbour_source_BYTE_alias')
        for a,z in _coalesce(addresses)]


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom,fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def schema(rom):
    def obj(properties):
        return dict(type='object',properties=properties,required=list(properties),additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({key:fixed(item) for key,item in value.items()})
        if type(value) is list:
            return dict(type='array',prefixItems=[fixed(item) for item in value],items=False,
                minItems=len(value),maxItems=len(value))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    properties = {key:fixed(value) for key,value in metadata(rom).items()}
    properties['source_BYTEs'] = dict(type='array',minItems=EDITABLE_BYTES,maxItems=EDITABLE_BYTES,
        items=obj(dict(address=dict(type='integer',minimum=SOURCE_FIRST,maximum=SOURCE_LIMIT-1),
            BYTE=dict(type='integer',minimum=0,maximum=255))))
    return dict(**obj(properties),**{'$schema':'https://json-schema.org/draft/2020-12/schema'},
        description='Witnessed city-neighbour BYTE aliases. Exact addresses/order enforced by importer; no padding/natural-domain admission.')


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom,load_fields(dump(fields)))
    if image != rom:
        raise ValueError('whole-ROM serialized source roundtrip differs')
    witnesses = []
    for address, selector, slot in _catalog(rom):
        pair, x, y = _pair(rom,selector)
        witnesses.append(dict(address=address,selector_WORD=selector,callback_slot=slot,
            true_JSR_PC=CALLS[slot],read_PC=0x17ECE,pair_address=pair,source_x_WORD=x,source_y_WORD=y))
    report = dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),all_physical_BYTES_witnessed=True,
        canonical_BYTE_witnesses=witnesses,independent_full_CPU=False,
        limitations=['Constructed complete RAM/city selectors are not natural game state proof.',
            'Both original indexed MOVE.Bs use D4.W; source BYTE is not the cost index.',
            'Negative cost CPU addresses are normal 24-bit mapped RAM, not a stop.',
            'Old pointer and coordinate WORDs are live; changed controls fail closed.',
            'Post-query 17DDC work and complete upstream UI lifetime are not simulated.'])
    members = {'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),'validation.json':dump(report)}
    members['manifest.json'] = dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    if any(len(data) > MAX_JSON for data in members.values()):
        raise ValueError('generated source bundle exceeds declared JSON bound')
    return members


def fresh_output(value, bundle=False):
    path = safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError('dedicated build output or exact fresh formal bundle required')
    if path.exists() or not path.parent.is_dir():
        raise ValueError('fresh output and existing parent required')
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM))
    parser.add_argument('--fields')
    parser.add_argument('--bundle')
    parser.add_argument('--output')
    args = parser.parse_args(argv)
    target = None
    if args.command == 'export':
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError('export requires output only')
        target = fresh_output(args.output,bundle=True)
    elif args.command == 'import':
        if args.output is None or args.bundle is not None:
            raise ValueError('import requires fresh .bin output')
        target = fresh_output(args.output)
        if target.suffix.lower() != '.bin':
            raise ValueError('fresh .bin required')
    elif args.output is not None or args.fields is not None and args.bundle is not None:
        raise ValueError('verify writes nothing and takes fields or bundle')
    rom = read_bounded(args.rom,ROM_SIZE)
    if args.command == 'export':
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            put(target/name,data)
        result = dict(path=str(target),editable_bytes=EDITABLE_BYTES)
    elif args.command == 'verify' and args.bundle is not None:
        path = safe_path(args.bundle)
        if not path.is_dir() or {p.name for p in path.iterdir()} != MEMBERS:
            raise ValueError('exact four bundle members required')
        for name, data in render_bundle(rom).items():
            if read_bounded(path/name,MAX_JSON) != data:
                raise ValueError('generated member drift: '+name)
        result = dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True)
    else:
        image = rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:
            put(target,image)
        result = dict(exact_canonical=image == rom,sha256=sha(image),editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
