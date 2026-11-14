"""Editable original scene RLE source fragments with two actual caller witnesses.

Pure whole-image format projection, not replay of the captured IRQ/CPU prefix.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
from functools import lru_cache
import json
from pathlib import Path

from tools.conditional_scene_rle_source_fields import codec as rle

ROOT = Path(__file__).resolve().parents[2]
ROM_SIZE, ROM_SHA256, DEFAULT_ROM = rle.ROM_SIZE, rle.ROM_SHA256, rle.DEFAULT_ROM
OUTPUT_ROOT = ROOT / 'build/scene_gap_rle_source_fields'
FORMAL_ROOT = ROOT / 'analysis/scene_gap_rle_source_fields/generated'
DEFAULT_BUNDLE, DEFAULT_FIELDS = FORMAL_ROOT, FORMAL_ROOT / 'fields.json'
FORMAT = 'g5510-scene-gap-original-RLE-source-BYTE-fragments-v1'
EDITABLE_BYTES, PHYSICAL_BLOCKS = 542, 16
MAX_JSON, MEMBERS = 4 * 1024 * 1024, rle.MEMBERS
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256 = reference_value(__name__, 'LAYOUT_SHA256')
BANK_C_SHA256 = reference_value(__name__, 'BANK_C_SHA256')
SOURCE_SHA256 = reference_value(__name__, 'SOURCE_SHA256')
MAME_RECEIPT_SHA256 = reference_value(__name__, 'MAME_RECEIPT_SHA256')
SPANS = (
    (0xC143A,0xC145A),(0xC149A,0xC14BA),(0xC14DA,0xC14FA),
    (0xC15DA,0xC1612),(0xC1616,0xC161A),(0xC357C,0xC359A),
    (0xC35FA,0xC361A),(0xC363A,0xC363C),(0xC3644,0xC365A),
    (0xC36BA,0xC373A),(0xC37FA,0xC383C),(0xC6D3A,0xC6D5A),
    (0xC6D7A,0xC6D9A),(0xC93DA,0xC93FA),(0xCC9F2,0xCC9FA),(0xCCA1A,0xCCA1C),
)
SOURCE_POSITIONS = frozenset(p for a,z in SPANS for p in range(a,z))
WITNESS_SELECTORS = (0x0498,0x03F3)
# Selector, full LONG, consumed BYTEs, output WORDs, output bytes SHA-256,
# stream bytes SHA-256, actual source coverage. No ROM payload is embedded.
WITNESS_SPECS = (
    (0x0498,0x702C0800,43051,21878,
     reference_value(__name__, 'WITNESS_SPECS'),
     reference_value(__name__, 'WITNESS_SPECS_2'),532),
    (0x03F3,0x001C3639,129263,89501,
     reference_value(__name__, 'WITNESS_SPECS_3'),
     reference_value(__name__, 'WITNESS_SPECS_4'),324),
)
BODIES = rle.BODIES
sha, dump, keys, same, uint, exact_list = rle.sha, rle.dump, rle.keys, rle.same, rle.uint, rle.exact_list
safe_path, read_bounded, put, load_fields = rle.safe_path, rle.read_bounded, rle.put, rle.load_fields
verify_rom, lookup_address = rle.verify_rom, rle.lookup_address


def source_view(image,selector_WORD,source_BYTE_budget=200000,output_WORD_budget=200000):
    """Read live pointer, marker, packets and old aliases from the whole image.

    Every complete WORD is accepted by the lookup arithmetic; the two evidence
    selectors are not a CPU clamp. This does not replay their earlier callers.
    """
    result = rle.source_view(image,selector_WORD,source_BYTE_budget,output_WORD_budget)
    reached = {p for e in result['source_reads'] for p in e['physical_addresses']}
    result.update(managed_source_reached=sorted(SOURCE_POSITIONS & reached),
                  managed_source_BYTES=len(SOURCE_POSITIONS & reached),
                  managed_scope_is_not_consumer_stop=True)
    return result


@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom)
    found = {}
    for selector,pointer,count,words,word_sha,stream_sha,coverage in WITNESS_SPECS:
        view = source_view(rom,selector)
        if (view['status'] != 'original_marker_count_zero_terminator' or
            view['original_pointer_LONG'] != pointer or view['source_BYTE_count'] != count or
            view['next_source_address'] != pointer+count or view['output_WORD_count'] != words or
            view['output_WORD_bytes_sha256'] != word_sha or view['managed_source_BYTES'] != coverage or
            sha(bytes(e['BYTE'] for e in view['source_reads'])) != stream_sha):
            raise ValueError('canonical original RLE witness differs')
        for event in view['source_reads']:
            for p in event['physical_addresses']:
                if p in SOURCE_POSITIONS and p not in found:
                    found[p] = dict(address=p,selector_WORD=selector,read_PC=event['PC'],
                        source_event_ordinal=event['ordinal'],source_address=event['address'],
                        canonical_role=event['role'],canonical_BYTE=event['BYTE'])
    if set(found) != SOURCE_POSITIONS or len(found) != EDITABLE_BYTES:
        raise ValueError('two original witnesses do not cover fixed source authority')
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
    raise ValueError('outside fixed scene gap source authority')


def metadata(rom):
    physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditionally_consumed_original_RLE_source_BYTE_fragments',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),source_union_BYTES=EDITABLE_BYTES,
        source_union_sha256=SOURCE_SHA256,physical_blocks=PHYSICAL_BLOCKS,
        physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in SPANS],
        raw_baseline=dict(resources=107,raw_BYTES=9787,layout_id=LAYOUT_ID,
                          manifest_sha256=LAYOUT_SHA256,bank0c_sha256=BANK_C_SHA256),
        grammar=dict(marker='first source BYTE',literal='high != marker: low BYTE emits one BE16 WORD',
            repeat='high == marker: count BYTE0 stops; else high/low value then DBRA emits count+1 WORDs',
            width='BE32 pointer operand, then full source BYTE operands',termination_is_live=True,
            canonical_witnesses=[dict(selector_WORD=s,pointer_LONG=p,source_BYTEs=n,source_limit=p+n,
                output_WORDs=w,output_WORD_bytes_sha256=h,stream_sha256=g,managed_source_BYTEs=c)
                for s,p,n,w,h,g,c in WITNESS_SPECS],canonical_witness_overlap_BYTES=314),
        evidence=dict(original_caller_PC=0xDA4,original_callee=0x1072C,original_scene_JSR_PC=0x1077E,
            original_RLE_BSR_PC=0x3976E,original_reader=0x39658,pointer_read_PC=0x3976A,
            pointer_base=0x387BA,selector='full FF7026.W; ASL.W2 lowWORD wrap then signed WORD index',
            witness_selectors_WORD=list(WITNESS_SELECTORS),original_MAME_version='0.289',
            original_map_sha256=rle.MAP_SHA256,capture_receipt_sha256=MAME_RECEIPT_SHA256,
            capture_is_runtime_dependency=False,
            conditional_frame='12-second cold observed MAME RAM/D/A/SP retained; once FF7026.W selector, EFD6.W0, SR2700, PC DA4',
            real_prefix='DA4 JSR1072C; EFD6 gate; actual0900 request/VBlank481E/RTE;10814 music;10896;1077E JSR3969A;3976E BSR39658',
            music='0498 reads6B1A and actual808A/BUSACK sends lowBYTE1A;03F3 readsCC00 and original BMI skips808A',
            first_RLE_return='count0 stops;39698 actual RTS pops00039772; next observed operand PC39778',
            stack='cold SP00FFFE00; terminator SP00FFFDF2; first-return-frontier SP00FFFDF6; actual two WORD pops0003/9772',
            projection_extent='RLE grammar only; earlier prefix/device/IRQ/RTS CPU execution is capture evidence, not API replay',
            controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES],
            cart_header_start=rle.mapper.MAPPER_HEADER_START,cart_header_end=rle.mapper.MAPPER_HEADER_END,
            cart_header_hex=rle.mapper.MAPPER_HEADER_HEX),
        editing_authority='one complete0..255 BYTE per fixed raw address; derived canonical roles are not second authority',
        old_typed_neighbors='whole edited image read live, including pointers/marker/count/value; never re-emitted',
        data_projection_only=True,owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        functions_added=0,complete_CPU=False,natural_selector_domain='unknown',allocation_owner='unknown',
        original_hardware_equivalence='unknown',edited_gameplay_safety='unknown',padding_or_free_space=False,
        IRQ_callback_VDP_execution_recovered=False,final_semantic_high_level_recovery=False)


def extract(rom):
    return dict(**metadata(rom),source_BYTEs=[dict(address=p,BYTE=rom[p]) for p in physical_positions(rom)])


def blocks(rom,fields):
    fixed = metadata(rom)
    keys(fields,set(fixed)|{'source_BYTEs'},'scene gap RLE source package')
    for k,value in fixed.items():
        same(fields[k],value,'metadata.'+k)
    values = {}
    for p,row in zip(physical_positions(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'source BYTEs')):
        keys(row,{'address','BYTE'},'single source BYTE')
        same(row['address'],p,'source address')
        values[p] = uint(row['BYTE'],255,'complete source BYTE')
    return [dict(id=f'rom_{a:06X}_scene_gap_RLE_source_BYTEs',start=a,end=z,
                 data=bytes(values[p] for p in range(a,z)),role='conditional_scene_RLE_source_BYTE_fragments')
            for a,z in SPANS]


def rebuild(rom,fields):
    image = bytearray(rom)
    for row in blocks(rom,fields):
        image[row['start']:row['end']] = row['data']
    return bytes(image)


def schema(rom):
    def obj(p):
        return dict(type='object',properties=p,required=list(p),additionalProperties=False)
    def fixed(v):
        if type(v) is dict:return obj({k:fixed(x) for k,x in v.items()})
        if type(v) is list:return dict(type='array',prefixItems=[fixed(x) for x in v],items=False,minItems=len(v),maxItems=len(v))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(v)],const=v)
    props = {k:fixed(v) for k,v in metadata(rom).items()}
    props['source_BYTEs'] = dict(type='array',items=False,minItems=EDITABLE_BYTES,maxItems=EDITABLE_BYTES,
        prefixItems=[obj(dict(address=fixed(p),BYTE=dict(type='integer',minimum=0,maximum=255)))
                     for p in physical_positions(rom)])
    return dict(**obj(props),**{'$schema':'https://json-schema.org/draft/2020-12/schema'})


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom,load_fields(dump(fields)))
    if image != rom:raise ValueError('serialized whole-ROM roundtrip differs')
    report = dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
        source_roles_are_not_second_edit_authority=True,projection_does_not_replay_captured_interrupt_or_devices=True)
    members = {'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),'validation.json':dump(report)}
    members['manifest.json'] = dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path = safe_path(value)
    for ancestor in (path,*path.parents):
        if ancestor.is_symlink() or getattr(ancestor,'is_junction',lambda:False)():raise ValueError('reparse output refused')
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError('fresh dedicated build output or exact fresh formal bundle required')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output with existing parent required')
    return path


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields');p.add_argument('--bundle');p.add_argument('--output')
    a = p.parse_args(argv);target = None
    if a.command == 'export':
        if a.output is None or a.fields is not None or a.bundle is not None:raise ValueError('export requires fresh output only')
        target = fresh_output(a.output,True)
    elif a.command == 'import':
        if a.output is None or a.bundle is not None:raise ValueError('import requires fresh .bin output')
        target = fresh_output(a.output)
        if target.suffix.lower() != '.bin':raise ValueError('fresh .bin output required')
    elif a.output is not None or a.fields is not None and a.bundle is not None:raise ValueError('verify takes fields or bundle and writes nothing')
    rom = read_bounded(a.rom,ROM_SIZE)
    if a.command == 'export':
        members = render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result = dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={k:sha(v) for k,v in members.items()})
    elif a.command == 'verify' and a.bundle is not None:
        bundle = safe_path(a.bundle)
        if not bundle.is_dir() or {q.name for q in bundle.iterdir()} != MEMBERS:raise ValueError('exact four-member bundle required')
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON) != data:raise ValueError('canonical generated member drift:'+name)
        result = dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True)
    else:
        image = rebuild(rom,load_fields(read_bounded(a.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:put(target,image)
        result = dict(exact_canonical=image == rom,editable_bytes=EDITABLE_BYTES,sha256=sha(image))
    print(json.dumps(result,sort_keys=True));return 0


if __name__ == '__main__':raise SystemExit(main())
