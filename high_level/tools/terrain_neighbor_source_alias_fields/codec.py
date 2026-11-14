"""Original object-coordinate BYTE producers and gated neighbour-source aliases.

Only the accepted-87 raw intersection EFA30..F2EF0 is authored. Every source
BYTE has a fixed two-BYTE object input witness through the original selector
writer and first dispatcher call. Natural object coordinate domains, whole
functions and the purpose of the remaining zero area are not recovered here.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE = 0x100000
ROM_SHA256 = reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM = ROOT.parent / "work/original_g5510.bin"
OUTPUT_ROOT = ROOT / "build/terrain_neighbor_source_alias_fields"
FORMAL_ROOT = ROOT / "analysis/terrain_neighbor_source_alias_fields/generated"
DEFAULT_BUNDLE = FORMAL_ROOT
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
MAX_JSON = 16 * 1024 * 1024
FORMAT = "g5510-conditional-object-neighbour-source-BYTE-alias-v1"
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
EDITABLE_BYTES = 13504
START, END = 0x0EFA30, 0x0F2EF0
SOURCE_BASE = 0x0EE5F0
BLOCK_ID = "rom_0EFA30_object_neighbour_comparison_BYTE_aliases"
BASELINE_LAYOUT = reference_value(__name__, 'BASELINE_LAYOUT')
OBJECT_BASE = 0xFFFF9000
POINTER_RAM = 0x00FF382C
READS = ((0x034FD2,-72),(0x034FDC,-1),(0x034FE6,1),(0x034FF0,72))
BODIES = (
    (0x009E14,0x009E5E,reference_value(__name__, 'BODIES')),
    (0x034F26,0x034F7C,reference_value(__name__, 'BODIES_2')),
    (0x034F94,0x034FFA,reference_value(__name__, 'BODIES_3')),
)
INSTRUCTIONS = (
    (0x009E14,"41f89000"),(0x009E18,"3038f35e"),(0x009E1C,"5540"),(0x009E1E,"e848"),
    (0x009E20,"3238f360"),(0x009E24,"5541"),(0x009E26,"e849"),
    (0x009E28,"1410"),(0x009E2A,"672c"),(0x009E2C,"0202007f"),
    (0x009E30,"16280004"),(0x009E34,"b0280001"),(0x009E38,"6606"),
    (0x009E3A,"b2280002"),(0x009E3E,"670c"),(0x009E4C,"23c800ff382c"),
    (0x034F26,"6100000e"),(0x034F2A,"31fc0001f728"),(0x034F30,"61000032"),
    (0x034F36,"207900ff382c"),(0x034F42,"12280004"),(0x034F4A,"1010"),
    (0x034F4C,"0240000f"),(0x034F50,"5340"),(0x034F54,"1230000d"),
    (0x034F5A,"51c8fff6"),(0x034F64,"3038f728"),(0x034F68,"6b000010"),
    (0x034F6C,"5340"),(0x034F6E,"e348"),(0x034F70,"303b000a"),
    (0x034F74,"4ebb001e"),(0x034F94,"61000018"),(0x034FAE,"207900ff382c"),
    (0x034FB4,"4240"),(0x034FB6,"10280001"),(0x034FBA,"4241"),(0x034FBC,"12280002"),
    (0x034FC0,"3400"),(0x034FC2,"e74a"),(0x034FC4,"d440"),(0x034FC6,"e74a"),
    (0x034FC8,"d441"),(0x034FCA,"43f9000ee5f0"),(0x034FD0,"d2c2"),
    (0x034FD2,"0c290001ffb8"),(0x034FD8,"67000020"),
    (0x034FDC,"0c290001ffff"),(0x034FE2,"67000016"),
    (0x034FE6,"0c2900010001"),(0x034FEC,"6700000c"),
    (0x034FF0,"0c2900010048"),(0x034FF6,"66000066"),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
safe_path, read_bounded, put = shared.safe_path, shared.read_bounded, shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom) != ROM_SIZE or sha(rom) != ROM_SHA256:
        raise ValueError("canonical original ROM bytes, size and SHA-256 required")
    for start,end,digest in BODIES:
        if sha(rom[start:end]) != digest:
            raise ValueError("pinned original writer/caller/producer/reader differs")
    for address,raw in INSTRUCTIONS:
        if rom[address:address+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError("pinned original source opcode differs")
    if rom[0x034F7C:0x034F7E] != b"\0\0":
        raise ValueError("original first relative JSR offset differs")


def metadata():
    return dict(
        format=FORMAT, confidence="confirmed_conditional_source_encoding",
        resource_role="candidate_object_neighbour_comparison_BYTE_source_alias",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        physical_scope=dict(start=START,end=END,bytes=EDITABLE_BYTES,
                            one_physical_authority=True,each_BYTE_full_range_editable=True),
        raw_baseline=dict(layout_id=BASELINE_LAYOUT,raw_intersection_bytes=EDITABLE_BYTES,
                          contents_are_source_fields_not_padding=True),
        evidence=dict(
            original_ledger="analysis/code/phase3_indirect/generated/enhanced_map/instructions.csv",
            original_ledger_sha256=reference_value(__name__, 'metadata'),
            bodies=[dict(start=a,end=b,sha256=digest) for a,b,digest in BODIES],
            instructions=[dict(address=a,bytes=raw) for a,raw in INSTRUCTIONS],
            object_pointer_writer=dict(entry=0x009E14,object_list_RAM=OBJECT_BASE,
                cursor_WORD_RAM=[0xFFFFF35E,0xFFFFF360],cursor_WORD_formula="(coordinate_BYTE << 4) + 2",
                coordinate_match_BYTE_PCs=[0x009E34,0x009E3A],
                matching_first_nonzero_packet_header_BYTE=1,matching_packet_owner_BYTE=0,
                pointer_write_PC=0x009E4C,pointer_RAM=POINTER_RAM,pointer_value=OBJECT_BASE,
                constructed_frame_is_natural_state_proof=False),
            caller=dict(entry=0x034F26,list_prepare_call_PC=0x034F26,list_prepare_entry=0x034F36,
                state_write_PC=0x034F2A,initial_state_WORD=1,
                dispatcher_call_PC=0x034F30,dispatcher_entry=0x034F64,
                state_minus_one_WORD_PC=0x034F6C,WORD_shift_PC=0x034F6E,
                offset_WORD_read_PC=0x034F70,offset_WORD_PC_base=0x034F72,
                offset_WORD_displacement=0x000A,offset_WORD_address=0x034F7C,
                relative_JSR_PC=0x034F74,relative_JSR_PC_base=0x034F76,
                relative_JSR_displacement=0x001E,relative_target_base=0x034F94,
                original_offset_WORD=0,callback=0x034F94,
                callback_BSR_PC=0x034F94,read_entry=0x034FAE,
                dispatcher_loop_and_post_query_actions_simulated=False),
            two_BYTE_producers=dict(pointer_read_PC=0x034FAE,first_CLR_WORD_PC=0x034FB4,
                first_BYTE_read_PC=0x034FB6,first_packet_displacement=1,
                second_CLR_WORD_PC=0x034FBA,second_BYTE_read_PC=0x034FBC,second_packet_displacement=2,
                producer_width="two zero-extended BYTEs in low WORDs",
                both_BYTE_editable_domains=[0,255],both_BYTE_natural_domains="unknown",
                index_formula="(((((first.W << 3) & FFFF) + first.W) << 3) + second.W) & FFFF",
                source_LEA_PC=0x034FCA,source_base=SOURCE_BASE,ADDA_WORD_PC=0x034FD0,
                effective_address="EE5F0 + s16(index.W) + signed displacement",
                maximum_from_two_BYTE_producers=18615,index_is_arbitrary_user_parameter=False),
            ordered_reads=[dict(PC=pc,displacement=offset,width_BYTES=1,early_exit_equals_BYTE=1,
                                early_exit_target=0x034FFA) for pc,offset in READS],
            fourth_non_equal_branch_target=0x03505E,
            source_read_role="literal CMP.B BYTE against immediate1, not opaque zero blob",
            witness_mode="constructed actual object BYTE producers and initial caller path; no arbitrary HL/bank/index"),
        excluded_remaining_zero_range=dict(start=END,end=0x0F8000,bytes=20752,role="unknown"),
        main_terrain_owner_added=False,padding_or_reserve_classification=False,
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        edited_gameplay_safety="unknown",complete_function_recovery=False,
        actual_runtime_access_record=False,independent_CPU_comparison=False,
    )


def signed_WORD(value):
    return value-0x10000 if value & 0x8000 else value


def constructed_frame(first_BYTE,second_BYTE):
    """A matching first RAM9000 object; two input BYTEs, not an index injection."""
    uint(first_BYTE,255,"object coordinate +1 BYTE")
    uint(second_BYTE,255,"object coordinate +2 BYTE")
    packet = bytes((1,first_BYTE,second_BYTE,0,0,0,0,0,0,0,0,0,0,0))
    cursor_first = ((first_BYTE << 4)+2) & 0xFFFF
    cursor_second = ((second_BYTE << 4)+2) & 0xFFFF
    # Original SUBQ.W2 then LSR.W4; the BYTE comparisons match this packet.
    first_match = (((cursor_first-2)&0xFFFF) >> 4) & 255
    second_match = (((cursor_second-2)&0xFFFF) >> 4) & 255
    if not packet[0] or (first_match,second_match) != (packet[1],packet[2]):
        raise ValueError("constructed frame does not pass original writer matches")
    return dict(packet=packet,cursor_first_WORD=cursor_first,cursor_second_WORD=cursor_second,
                pointer_value=OBJECT_BASE,pointer_writer_PC=0x009E4C,initial_dispatch_state_WORD=1)


def source_view(image,first_BYTE,second_BYTE,source_BYTE_budget=4):
    """Narrow original first-call source projection, stopping at true early exits.

    This constructs the explicit matching RAM object/writer frame, performs
    the initial live relative dispatch lookup, then derives the source address
    from the two original BYTE reads. No subsequent function state is modeled.
    """
    if type(image) is not bytes or len(image) != ROM_SIZE:
        raise ValueError("source diagnostic requires a full edited ROM bytes image")
    uint(source_BYTE_budget,4,"diagnostic source BYTE budget")
    frame = constructed_frame(first_BYTE,second_BYTE)
    result = dict(first_coordinate_BYTE=first_BYTE,second_coordinate_BYTE=second_BYTE,
        cursor_first_WORD=frame['cursor_first_WORD'],cursor_second_WORD=frame['cursor_second_WORD'],
        pointer_writer_PC=0x009E4C,pointer_RAM=POINTER_RAM,object_pointer=OBJECT_BASE,
        caller_entry=0x034F26,initial_dispatch_state_WORD=1,source_reads=[],
        source_BYTE_budget=source_BYTE_budget,budget_is_original_CPU_limit=False,
        natural_read_admission=False,whole_CPU_or_function_model=False)
    for start,end,digest in BODIES:
        if sha(image[start:end]) != digest:
            return dict(**result,status="pinned_original_read_control_changed",boundary_address=start)
    table_address = 0x034F7C
    offset = int.from_bytes(image[table_address:table_address+2],"big")
    target = 0x034F94 + signed_WORD(offset)
    result['dispatch_source'] = dict(original_read_PC=0x034F70,address=table_address,
        width_BYTES=2,WORD=offset,JSR_PC=0x034F74,target_base=0x034F94,target=target)
    if target != 0x034F94:
        return dict(**result,status="unmodeled_live_relative_callback_target",boundary_address=target)
    # The exact initial packet has one officer and owner zero: 34F36 prepares
    # that one WORD list and its FFFF stop before 34F2A writes state one.
    result['object_producer_reads'] = [
        dict(PC=0x034F36,address=POINTER_RAM,width_BYTES=4,LONG=OBJECT_BASE),
        dict(PC=0x034F42,address=OBJECT_BASE+4,width_BYTES=1,BYTE=frame['packet'][4]),
        dict(PC=0x034F4A,address=OBJECT_BASE,width_BYTES=1,BYTE=frame['packet'][0]),
        dict(PC=0x034F54,address=OBJECT_BASE+13,width_BYTES=1,BYTE=frame['packet'][13]),
        dict(PC=0x034FAE,address=POINTER_RAM,width_BYTES=4,LONG=OBJECT_BASE),
        dict(PC=0x034FB6,address=OBJECT_BASE+1,width_BYTES=1,BYTE=frame['packet'][1]),
        dict(PC=0x034FBC,address=OBJECT_BASE+2,width_BYTES=1,BYTE=frame['packet'][2]),
    ]
    first = frame['packet'][1]
    second = frame['packet'][2]
    index = (first << 3) & 0xFFFF
    index = (index+first) & 0xFFFF
    index = (index << 3) & 0xFFFF
    index = (index+second) & 0xFFFF
    result['index_WORD'] = index
    result['signed_index'] = signed_WORD(index)
    result['center_source_address'] = SOURCE_BASE + signed_WORD(index)
    for pc,offset in READS:
        address = result['center_source_address'] + offset
        if len(result['source_reads']) >= source_BYTE_budget:
            return dict(**result,status="diagnostic_source_BYTE_budget_exhausted",boundary_address=address)
        if not 0 <= address < ROM_SIZE:
            return dict(**result,status="outside_supplied_ROM",boundary_address=address)
        value = image[address]
        result['source_reads'].append(dict(PC=pc,address=address,width_BYTES=1,BYTE=value,
            equals_one=value == 1,inside_edit_scope=START <= address < END))
        if value == 1:
            return dict(**result,status="early_exit_source_BYTE_equals_one",following_PC=0x034FFA)
    return dict(**result,status="four_source_BYTEs_read_none_equals_one",following_PC=0x03505E)


def witness(address):
    """Pinned producer BYTEs for each physical source; late reads remain gated."""
    uint(address,ROM_SIZE-1,"source BYTE address")
    if not START <= address < END:
        raise ValueError("witness address outside authored raw intersection")
    source_index = address-SOURCE_BASE
    if source_index <= 18543:
        center = source_index+72
        first = min(255,center//72)
        second = center-72*first
        pc,offset = READS[0]
    else:
        first = 255
        second = source_index-72-72*first
        pc,offset = READS[3]
    uint(first,255,"witness first object BYTE")
    uint(second,255,"witness second object BYTE")
    if SOURCE_BASE+signed_WORD((72*first+second)&0xFFFF)+offset != address:
        raise ValueError("per-BYTE witness address formula differs")
    return dict(first_coordinate_BYTE=first,second_coordinate_BYTE=second,
                original_read_PC=pc,signed_displacement=offset)


def target_view(image,address,source_BYTE_budget=4):
    w = witness(address)
    view = source_view(image,w['first_coordinate_BYTE'],w['second_coordinate_BYTE'],source_BYTE_budget)
    hits = [r for r in view['source_reads'] if r['address'] == address and r['PC'] == w['original_read_PC']]
    return dict(address=address,witness=w,target_reached=bool(hits),
                target_BYTE=hits[0]['BYTE'] if hits else None,source_projection=view)


def cell_fixed(address):
    return dict(address=address,witness=witness(address))


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(),comparison_source_BYTEs=[dict(**cell_fixed(a),BYTE=rom[a]) for a in range(START,END)])


def blocks(rom,fields):
    verify_rom(rom)
    fixed = metadata()
    keys(fields,set(fixed) | {'comparison_source_BYTEs'},"conditional source package")
    for key,value in fixed.items():
        same(fields[key],value,"package."+key)
    rows = exact_list(fields['comparison_source_BYTEs'],EDITABLE_BYTES,"ordered unique physical comparison BYTEs")
    data = bytearray()
    for address,row in zip(range(START,END),rows):
        pinned = cell_fixed(address)
        keys(row,set(pinned) | {'BYTE'},"comparison source BYTE")
        for key,value in pinned.items():
            same(row[key],value,"cell."+key)
        data.append(uint(row['BYTE'],255,"full comparison source BYTE"))
    return [dict(id=BLOCK_ID,start=START,end=END,data=bytes(data),
                 role="conditional_object_neighbour_CMP_BYTE_source_alias")]


def rebuild(rom,fields):
    image = bytearray(rom)
    for row in blocks(rom,fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def load_fields(data):
    if type(data) is not bytes or len(data) > MAX_JSON:
        raise ValueError("bounded UTF-8 field JSON bytes required")
    def pairs(items):
        result = {}
        for key,value in items:
            if key in result:
                raise ValueError("duplicate JSON key: "+key)
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError("nonfinite JSON number: "+value)
    try:
        return json.loads(data.decode('utf-8'),object_pairs_hook=pairs,parse_constant=nonfinite)
    except (UnicodeError,json.JSONDecodeError,RecursionError) as exc:
        raise ValueError("invalid bounded field JSON") from exc


def validate_witnesses(image):
    """Re-evaluate every actual gated path; edited fields may block late witnesses."""
    reached = 0
    blocked = []
    values = bytearray()
    for address in range(START,END):
        row = target_view(image,address)
        if row['target_reached']:
            reached += 1
            values.append(row['target_BYTE'])
        else:
            blocked.append(dict(address=address,status=row['source_projection']['status'],
                                prior_read_count=len(row['source_projection']['source_reads'])))
    return dict(physical_BYTE_count=EDITABLE_BYTES,target_BYTE_reads_reached=reached,
                target_BYTE_reads_not_reached=len(blocked),not_reached=blocked,
                reached_values_sha256=sha(bytes(values)),natural_domain_proved=False,
                edited_paths_rechecked=True)


def schema():
    def obj(properties):
        return dict(type="object",properties=properties,required=list(properties),additionalProperties=False)
    def fixed(value):
        if type(value) is dict:
            return obj({key:fixed(item) for key,item in value.items()})
        if type(value) is list:
            return dict(type="array",prefixItems=[fixed(item) for item in value],items=False,
                        minItems=len(value),maxItems=len(value))
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    byte = dict(type="integer",minimum=0,maximum=255)
    properties = {key:fixed(value) for key,value in metadata().items()}
    properties['comparison_source_BYTEs'] = dict(type="array",minItems=EDITABLE_BYTES,maxItems=EDITABLE_BYTES,
        items=obj(dict(address=dict(type="integer",minimum=START,maximum=END-1),BYTE=byte,
                       witness=obj(dict(first_coordinate_BYTE=byte,second_coordinate_BYTE=byte,
                           original_read_PC=dict(type="integer",enum=[READS[0][0],READS[3][0]]),
                           signed_displacement=dict(type="integer",enum=[-72,72]))))))
    return dict(**obj(properties),**{'$schema':'https://json-schema.org/draft/2020-12/schema'},
                description="Full comparison BYTEs; importer additionally pins every address/order/producer witness. No terrain-owner or padding claim.")


def render_bundle(rom):
    fields = extract(rom)
    serialized = dump(fields)
    image = rebuild(rom,load_fields(serialized))
    if image != rom:
        raise ValueError("serialized source BYTE whole-ROM roundtrip differs")
    witnesses = validate_witnesses(image)
    if witnesses['target_BYTE_reads_not_reached']:
        raise ValueError("canonical per-BYTE witness does not reach original source read")
    report = dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=1,
        whole_ROM_exact=True,whole_ROM_sha256=sha(image),canonical_witness_validation=witnesses,
        source_sha256=sha(rom[START:END]),canonical_zero_source_BYTEs=rom[START:END].count(0),
        examples=[target_view(rom,a) for a in (START,START+1,0x0F2E5F,0x0F2E60,END-1)])
    members={'fields.json':serialized,'fields.schema.json':dump(schema()),'validation.json':dump(report)}
    members['manifest.json']=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=1,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("dedicated neighbour-source build output or exact formal bundle required")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM))
    parser.add_argument('--fields')
    parser.add_argument('--bundle')
    parser.add_argument('--output')
    args=parser.parse_args(argv)
    target=None
    if args.command == 'export':
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError("export requires fresh output only")
        target=fresh_output(args.output,bundle=True)
    elif args.command == 'import':
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fields and fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower() != '.bin':
            raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.bundle is not None and args.fields is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command == 'export':
        members=render_bundle(rom)
        target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
    elif args.command == 'verify' and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON) != data:
                raise ValueError("canonical generated bundle drift: "+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=EDITABLE_BYTES,
                    whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON))
        image=rebuild(rom,fields)
        if target is not None:put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=EDITABLE_BYTES,
                    exact_canonical=image == rom,bytes=len(image),sha256=sha(image))
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
