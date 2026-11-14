"""Lossless conditional original scene RLE source BYTE fragments.

The data projection reads the complete edited image, not a MAME dump. It does
not replay a CPU, IRQ, callback, device, or natural game-state construction.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared
from tools.cart_mirrored_tile_source_alias_fields import codec as mapper

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE, ROM_SHA256, DEFAULT_ROM = shared.ROM_SIZE, shared.ROM_SHA256, shared.DEFAULT_ROM
OUTPUT_ROOT = ROOT / 'build/conditional_scene_rle_source_fields'
FORMAL_ROOT = ROOT / 'analysis/conditional_scene_rle_source_fields/generated'
DEFAULT_BUNDLE, DEFAULT_FIELDS = FORMAL_ROOT, FORMAL_ROOT / 'fields.json'
FORMAT = 'g5510-conditional-original-scene-RLE-source-BYTE-fragments-v1'
EDITABLE_BYTES, PHYSICAL_BLOCKS = 958, 11
MAX_JSON = shared.MAX_JSON
MEMBERS = shared.MEMBERS
WITNESS_SELECTOR = 0x0F96
SOURCE_FIRST, SOURCE_LIMIT = 0xC383C, 0xC641F
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
STREAM_SHA256 = reference_value(__name__, 'STREAM_SHA256')
OUTPUT_WORD_SHA256 = reference_value(__name__, 'OUTPUT_WORD_SHA256')
SPANS = ((0xC383C,0xC387A),(0xC389A,0xC38BA),(0xC3C7A,0xC3D5A),
         (0xC3D7A,0xC3D9A),(0xC3DBA,0xC3E1A),(0xC3E7A,0xC3F3A),
         (0xC3F5A,0xC3F7A),(0xC55FA,0xC569A),(0xC591A,0xC593A),
         (0xC613A,0xC615A),(0xC617A,0xC61BA))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
BANK_C_SHA256 = reference_value(__name__, 'BANK_C_SHA256')
MAP_SHA256 = reference_value(__name__, 'MAP_SHA256')
MAME_RECEIPT_SHA256 = reference_value(__name__, 'MAME_RECEIPT_SHA256')
MAME_IRQ_STACK_RECEIPT_SHA256 = reference_value(__name__, 'MAME_IRQ_STACK_RECEIPT_SHA256')
# Exact original envelopes are evidence guards, not a CPU path implementation.
# 3969A..39772 is explicitly the prefix through the first RLE call, not the
# complete later scene loop. Helpers end at their original RTS where applicable.
BODIES = (
    (0xD94,0xDAA,reference_value(__name__, 'BODIES')),
    (0x1072C,0x10830,reference_value(__name__, 'BODIES_2')),
    (0x10896,0x109D8,reference_value(__name__, 'BODIES_3')),
    (0xAF48,0xAF6A,reference_value(__name__, 'BODIES_4')),
    (0x83C8,0x83FA,reference_value(__name__, 'BODIES_5')),
    (0x481E,0x4A4C,reference_value(__name__, 'BODIES_6')),
    (0x67CA,0x6826,reference_value(__name__, 'BODIES_7')),
    (0x808A,0x80D0,reference_value(__name__, 'BODIES_8')),
    (0x39658,0x3969A,reference_value(__name__, 'BODIES_9')),
    (0x3969A,0x39772,reference_value(__name__, 'BODIES_10')),
    (0x3B2B0,0x3B2D8,reference_value(__name__, 'BODIES_11')),
    (0x3A75E,0x3A78C,reference_value(__name__, 'BODIES_12')),
)
sha, dump = shared.sha, shared.dump
keys, same, uint, exact_list = shared.keys, shared.same, shared.uint, shared.exact_list
safe_path, read_bounded, put, load_fields = shared.safe_path, shared.read_bounded, shared.put, shared.load_fields
cart_read = mapper.cart_read


def _controls(image):
    mapper._image(image)
    for start,end,digest in BODIES:
        if sha(image[start:end]) != digest:
            raise ValueError('original caller/control/helper bytes changed')


def verify_rom(rom):
    _controls(rom)
    if sha(rom) != ROM_SHA256:
        raise ValueError('canonical original ROM SHA-256 required')


def lookup_address(selector_WORD):
    selector = uint(selector_WORD,65535,'complete scene selector WORD')
    offset = (selector << 2) & 0xFFFF
    return 0x387BA + (offset-0x10000 if offset & 0x8000 else offset)


def source_view(image, selector_WORD, source_BYTE_budget=200000, output_WORD_budget=200000):
    """Live original grammar projection; no original IRQ/callback/CPU replay.

    BYTE budgets bound instrumentation only. Repeat writes are represented as
    ordered counted WORD runs, not millions of reconstructed CPU iterations.
    Any edited marker/count/pointer/neighbor can alter framing or the boundary.
    """
    _controls(image)
    selector = uint(selector_WORD,65535,'complete scene selector WORD')
    source_budget = uint(source_BYTE_budget,200000,'diagnostic source BYTE budget')
    output_budget = uint(output_WORD_budget,200000,'diagnostic emitted WORD budget')
    events,runs = [],[]
    pointer_event, marker, at = None,None,None
    status, boundary = 'diagnostic_source_BYTE_budget_exhausted',None
    output_count,literal_packets,repeat_packets = 0,0,0
    output_hash = hashlib.sha256()
    address = lookup_address(selector)
    try:
        pointer_event = cart_read(image,address,4,0x3976A)
    except ValueError as exc:
        status,boundary = 'mapping_read_boundary',dict(PC=0x3976A,address=address,width=4,reason=str(exc))
    else:
        at = pointer_event['value']
        class Stop(Exception):
            pass
        def read(PC,role):
            nonlocal at,status,boundary
            if len(events) >= source_budget:
                status = 'diagnostic_source_BYTE_budget_exhausted'
                raise Stop
            try:
                event = cart_read(image,at,1,PC)
            except ValueError as exc:
                status,boundary = 'mapping_read_boundary',dict(PC=PC,address=at,width=1,reason=str(exc))
                raise Stop
            event.update(ordinal=len(events),role=role,BYTE=event['value'])
            events.append(event)
            at = (at+1) & 0xFFFFFFFF
            return event['value']
        try:
            marker = read(0x39664,'marker')
            while True:
                high_event = len(events)
                high = read(0x39666,'marker_or_literal_high')
                if high != marker:
                    events[high_event]['role'] = 'literal_high'
                    low = read(0x3966E,'literal_low')
                    word,count,PC,kind = (high << 8) | low,1,0x39674,'literal'
                    literal_packets += 1
                else:
                    events[high_event]['role'] = 'repeat_marker'
                    count = read(0x3967E,'repeat_count')
                    if count == 0:
                        events[high_event]['role'] = 'terminator_marker'
                        events[-1]['role'] = 'terminator_count_zero'
                        status = 'original_marker_count_zero_terminator'
                        break
                    high_value = read(0x39684,'value_high')
                    low = read(0x39686,'value_low')
                    word,count,PC,kind = (high_value << 8) | low,count+1,0x3968C,'repeat'
                    repeat_packets += 1
                emitted = min(count,output_budget-output_count)
                runs.append(dict(PC=PC,kind=kind,WORD=word,original_count=count,
                                 emitted_count=emitted,first_output_WORD=output_count,
                                 source_event_first=high_event,source_event_limit=len(events)))
                output_hash.update(word.to_bytes(2,'big') * emitted)
                output_count += emitted
                if emitted != count:
                    status,boundary = 'diagnostic_output_WORD_budget_exhausted',dict(
                        PC=PC,pending_repeat_WORDs=count-emitted,original_count=count)
                    break
        except Stop:
            pass
    return dict(selector_WORD=selector,lookup_address=address,pointer_read=pointer_event,
        original_pointer_LONG=None if pointer_event is None else pointer_event['value'],
        marker_BYTE=marker,status=status,boundary=boundary,source_reads=events,
        source_BYTE_count=len(events),next_source_address=at,output_runs=runs,
        output_WORD_count=output_count,output_WORD_bytes_sha256=output_hash.hexdigest(),
        literal_packets=literal_packets,repeat_packets=repeat_packets,
        framing_is_live=True,catalog_is_CPU_clamp=False,
        VDP_callback_executed=False,IRQ_or_CPU_replayed=False,
        data_projection_only=True,complete_CPU=False,natural_domain='unknown',owner='unknown',
        instrumentation_budgets_are_CPU_stop=False,
        cart_profile='measured MAME0.289 24bit ROM apertures0..200000/204000..400000; SRAM/outside rejected')


@lru_cache(maxsize=2)
def _catalog(rom):
    view = source_view(rom,WITNESS_SELECTOR)
    if (view['status'] != 'original_marker_count_zero_terminator' or
        view['source_BYTE_count'] != 11235 or view['next_source_address'] != SOURCE_LIMIT or
        view['output_WORD_count'] != 181359 or view['output_WORD_bytes_sha256'] != OUTPUT_WORD_SHA256):
        raise ValueError('canonical original RLE grammar witness differs')
    wanted = {p for start,end in SPANS for p in range(start,end)}
    found = {}
    for event in view['source_reads']:
        for p in event['physical_addresses']:
            if p in wanted:
                found[p] = dict(address=p,selector_WORD=WITNESS_SELECTOR,read_PC=event['PC'],
                                source_event_ordinal=event['ordinal'],source_address=event['address'],
                                canonical_role=event['role'],canonical_BYTE=event['BYTE'])
    if set(found) != wanted or len(found) != EDITABLE_BYTES:
        raise ValueError('fixed raw sole source BYTE authority differs')
    if sha(bytes(rom[p] for p in sorted(found))) != SOURCE_SHA256:
        raise ValueError('fixed source BYTE SHA-256 differs')
    return tuple(found[p] for p in sorted(found))


def physical_positions(rom):
    verify_rom(rom)
    return tuple(row['address'] for row in _catalog(rom))


def witness(rom,address):
    verify_rom(rom)
    p = uint(address,ROM_SIZE-1,'source physical BYTE address')
    for row in _catalog(rom):
        if row['address'] == p:
            return load_fields(dump(row))
    raise ValueError('outside fixed conditional RLE physical source authority')


def metadata(rom):
    physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditionally_consumed_original_RLE_source_BYTE_fragments',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),source_union_BYTES=EDITABLE_BYTES,
        source_union_sha256=SOURCE_SHA256,physical_blocks=PHYSICAL_BLOCKS,
        physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in SPANS],
        raw_baseline=dict(resources=102,raw_BYTES=13180,layout_id=LAYOUT_ID,
                          manifest_sha256=LAYOUT_SHA256,bank0c_sha256=BANK_C_SHA256),
        grammar=dict(marker='first source BYTE',literal='high != marker: next low BYTE emits one BE16 WORD',
                     repeat='high == marker: count BYTE0 stops; otherwise value high/low then DBRA emits count+1 WORDs',
                     width='all source operands are BYTE; pointer table operand is BE32 LONG',
                     termination_is_live=True,canonical_source_first=SOURCE_FIRST,
                     canonical_source_limit=SOURCE_LIMIT,canonical_consumed_BYTEs=11235,
                     canonical_stream_sha256=STREAM_SHA256,canonical_output_WORDs=181359,
                     canonical_output_WORD_bytes_sha256=OUTPUT_WORD_SHA256),
        evidence=dict(original_caller_PC=0xDA4,original_scene_JSR_PC=0x1077E,
                      original_RLE_BSR_PC=0x3976E,original_reader=0x39658,
                      selector='complete FF7026.W; ASL.W2 wraps lowWORD then signed index',
                      pointer_read_PC=0x3976A,pointer_base=0x387BA,witness_selector_WORD=WITNESS_SELECTOR,
                      canonical_pointer_address=0x3C612,canonical_pointer_LONG=SOURCE_FIRST,
                      native_map_sha256=MAP_SHA256,original_MAME_version='0.289',
                      independent_capture_receipt_sha256=MAME_RECEIPT_SHA256,
                      independent_IRQ_stack_receipt_sha256=MAME_IRQ_STACK_RECEIPT_SHA256,
                      capture_is_runtime_dependency=False,
                      real_IRQ_evidence='DA4→1072C→0900 original IRQ/RTE→1077E→3976E captured conditionally',
                      controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES],
                      consumer_3969A_pin_extent='prefix only through first3976E call; later loop not executed by projection',
                      cart_header_start=mapper.MAPPER_HEADER_START,cart_header_end=mapper.MAPPER_HEADER_END,
                      cart_header_hex=mapper.MAPPER_HEADER_HEX),
        editing_authority='one complete0..255 BYTE per fixed raw address; canonical roles are derived witnesses only',
        old_typed_neighbors='read live from whole edited image; never re-emitted',
        data_projection_only=True,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        functions_added=0,complete_CPU=False,natural_selector_domain='unknown',allocation_owner='unknown',
        original_hardware_equivalence='unknown',edited_gameplay_safety='unknown',padding_or_free_space=False,
        IRQ_callback_VDP_execution_recovered=False,final_semantic_high_level_recovery=False)


def extract(rom):
    return dict(**metadata(rom),source_BYTEs=[dict(address=p,BYTE=rom[p]) for p in physical_positions(rom)])


def blocks(rom,fields):
    fixed = metadata(rom)
    keys(fields,set(fixed)|{'source_BYTEs'},'conditional RLE source package')
    for k,value in fixed.items():
        same(fields[k],value,'metadata.'+k)
    values = {}
    for p,row in zip(physical_positions(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'source BYTEs')):
        keys(row,{'address','BYTE'},'single source BYTE')
        same(row['address'],p,'source address')
        values[p] = uint(row['BYTE'],255,'complete source BYTE')
    return [dict(id=f'rom_{a:06X}_conditional_scene_RLE_source_BYTEs',start=a,end=z,
                 data=bytes(values[p] for p in range(a,z)),role='conditional_scene_RLE_source_BYTE_fragments')
            for a,z in SPANS]


def rebuild(rom,fields):
    encoded = blocks(rom,fields)
    image = bytearray(rom)
    for row in encoded:
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def schema(rom):
    def obj(p):
        return dict(type='object',properties=p,required=list(p),additionalProperties=False)
    def fixed(v):
        if type(v) is dict:
            return obj({k:fixed(x) for k,x in v.items()})
        if type(v) is list:
            return dict(type='array',prefixItems=[fixed(x) for x in v],items=False,minItems=len(v),maxItems=len(v))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(v)],const=v)
    props = {k:fixed(v) for k,v in metadata(rom).items()}
    props['source_BYTEs'] = dict(type='array',items=False,minItems=EDITABLE_BYTES,maxItems=EDITABLE_BYTES,
        prefixItems=[obj(dict(address=fixed(p),BYTE=dict(type='integer',minimum=0,maximum=255)))
                     for p in physical_positions(rom)])
    return dict(**obj(props),**{'$schema':'https://json-schema.org/draft/2020-12/schema'})


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom,load_fields(dump(fields)))
    if image != rom:
        raise ValueError('serialized whole-ROM roundtrip differs')
    report = dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
                  whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
                  source_roles_are_not_second_edit_authority=True,
                  projection_does_not_replay_captured_interrupt_or_devices=True)
    members = {'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),
               'validation.json':dump(report)}
    members['manifest.json'] = dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path = safe_path(value)
    for ancestor in (path,*path.parents):
        if ancestor.is_symlink() or getattr(ancestor,'is_junction',lambda:False)():
            raise ValueError('reparse output refused')
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError('fresh dedicated build output or exact fresh formal bundle required')
    if path.exists() or not path.parent.is_dir():
        raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields');p.add_argument('--bundle');p.add_argument('--output')
    a = p.parse_args(argv)
    target = None
    if a.command == 'export':
        if a.output is None or a.fields is not None or a.bundle is not None:
            raise ValueError('export requires fresh output only')
        target = fresh_output(a.output,True)
    elif a.command == 'import':
        if a.output is None or a.bundle is not None:
            raise ValueError('import requires fresh .bin output')
        target = fresh_output(a.output)
        if target.suffix.lower() != '.bin':
            raise ValueError('fresh .bin output required')
    elif a.output is not None or a.fields is not None and a.bundle is not None:
        raise ValueError('verify takes fields or bundle and writes nothing')
    rom = read_bounded(a.rom,ROM_SIZE)
    if a.command == 'export':
        members = render_bundle(rom)
        target.mkdir()
        for name,data in members.items():
            put(target/name,data)
        result = dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={k:sha(v) for k,v in members.items()})
    elif a.command == 'verify' and a.bundle is not None:
        bundle = safe_path(a.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()} != MEMBERS:
            raise ValueError('exact four-member bundle required')
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON) != data:
                raise ValueError('canonical generated member drift:'+name)
        result = dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True)
    else:
        image = rebuild(rom,load_fields(read_bounded(a.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:
            put(target,image)
        result = dict(exact_canonical=image == rom,editable_bytes=EDITABLE_BYTES,sha256=sha(image))
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
