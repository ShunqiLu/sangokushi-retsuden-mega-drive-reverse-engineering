"""Lossless actor-state and budget tables; editor extents are not CPU bounds."""
from __future__ import annotations
import argparse
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from tools.graphics_build import graphics_build as gb

DEFAULT_ROM = ROOT.parent/'work/original_g5510.bin'
DEFAULT_ASSETS = ROOT/'analysis/candidate_action_tables/generated/assets.json'
FORMAT = 'g5510-candidate-action-tables-v1'
EDITABLE_BYTES = 84
TABLES = (
    ('state_offsets', 0x19B42, 2, 14),
    ('initial_list_pointers', 0x19C96, 4, 2),
    ('mark_list_pointers', 0x19E0E, 4, 2),
    ('action_message_words', 0x19EC2, 2, 6),
    ('budget_dispatch_offsets', 0x1AFA0, 2, 6),
    ('budget_pointers', 0x1AFAC, 4, 4),
)
ANCHORS = (
    ('state_reader', 0x19B2C, '3038f362e348303b000e4ebb0026'),
    ('initial_list_reader', 0x19CB4, '3038f6d6e348207b00da'),
    ('mark_list_reader', 0x19DE4, '3238f6d602410002' 'e34941fa001e4e7120701000'),
    ('message_reader', 0x19EA2, '3038f6d4e34841fa001830300000'),
    ('budget_dispatch_reader', 0x1AF80, '3038f6d4e348303b00184ebb0030'),
    ('budget_pointer_reader', 0x1AF8E, '3038f6d6e548207b00162010b0b8f39e4e75'),
)
sha, dump = gb.sha, gb.dump


def verify_rom(rom):
    if type(rom) is not bytes: raise ValueError('immutable canonical ROM required')
    gb.af.verify_rom(rom)
    for name, pc, raw in ANCHORS:
        if rom[pc:pc+len(raw)//2] != bytes.fromhex(raw):
            raise ValueError('original reader changed: '+name)


def extract(rom):
    verify_rom(rom)
    return {'schema_version':1, 'format':FORMAT, **{
        key:list(struct.unpack_from('>'+str(count)+('H' if width==2 else 'I'), rom, start))
        for key,start,width,count in TABLES}}


def blocks(rom, assets):
    verify_rom(rom)
    gb.af._keys(assets, {'schema_version','format'} | {r[0] for r in TABLES}, 'action source fields')
    if type(assets['schema_version']) is not int or assets['schema_version'] != 1 or assets['format'] != FORMAT:
        raise ValueError('schema/format mismatch')
    result=[]
    for key,start,width,count in TABLES:
        fields=gb.exact_list(assets[key],count,key)
        values=[gb.rf.integer(value,(1 << (width*8))-1,key) for value in fields]
        data=struct.pack('>'+str(count)+('H' if width==2 else 'I'), *values)
        result.append({'id':key,'start':start,'end':start+len(data),'data':data,
                       'role':'candidate_action_'+('pointers' if width==4 else 'words')})
    return result


def rebuild(rom, assets):
    result=bytearray(rom)
    for row in blocks(rom, assets): result[row['start']:row['end']]=row['data']
    return bytes(result)


def s16(value):
    return value-65536 if value&32768 else value


def lookup(image, value, kind):
    gb.rf.integer(value,65535,'complete selector WORD')
    specs={key:(start,width,count) for key,start,width,count in TABLES}
    if type(kind) is not str or kind not in specs: raise ValueError('unknown source projection')
    start,width,count=specs[kind]
    shift=2 if kind=='budget_pointers' else 1
    index=((value & 2) << 1) if kind=='mark_list_pointers' else ((value << shift)&65535)
    address=start+s16(index)
    if type(image) is not bytes or len(image)!=1048576: raise ValueError('explicit immutable 1 MiB source image required')
    field=int.from_bytes(image[address:address+width],'big')
    result={'selector_word':value,'index_word':index,'source_address':address,'source_width':width,
        'source_value':field,'inside_editor_allocation':start<=address and address+width<=start+width*count,
        'aligned_to_source_slot':(address-start)%width==0}
    if kind in ('state_offsets','budget_dispatch_offsets'):
        base=0x19B5E if kind=='state_offsets' else 0x1AFBC
        result.update(logical_target=(base+s16(field))&0xFFFFFFFF, relative_base=base,
                      odd_target=bool((base+s16(field))&1))
    return result


def inspect(rom, assets):
    image=rebuild(rom,assets)
    inputs=(0,1,2,3,4,5,6,13,14,0x7FFF,0x8000,0xFFFF)
    views={key:[lookup(image,v,key) for v in inputs] for key,_,_,_ in TABLES}
    warnings=[]
    for key in ('state_offsets','budget_dispatch_offsets'):
        count=14 if key=='state_offsets' else 6
        for value in range(count):
            row=lookup(image,value,key)
            if row['odd_target']:
                warnings.append({'code':'odd_dispatch_target','table':key,'slot':value})
    for key in ('initial_list_pointers','mark_list_pointers','budget_pointers'):
        for slot,pointer in enumerate(assets[key]):
            if pointer&1: warnings.append({'code':'odd_pointer_value','table':key,'slot':slot})
    return {'format':FORMAT,'canonical_exact':image==rom,'editable_bytes':EDITABLE_BYTES,
        'changed_bytes':sum(a!=b for a,b in zip(image,rom)), 'image_sha256':sha(image),
        'full_word_projections':views,'warning_policy':'report_only_no_source_normalization','warnings':warnings,
        'complete_domain_claim':False,'natural_execution_claim':False,'build_integration_claim':False}


def schema():
    fields={'schema_version':{'type':'integer','const':1},'format':{'const':FORMAT}}
    for key,_,width,count in TABLES:
        fields[key]={'type':'array','minItems':count,'maxItems':count,
            'items':{'type':'integer','minimum':0,'maximum':(1 << (width*8))-1}}
    return {'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object',
        'additionalProperties':False,'required':list(fields),'properties':fields,
        '$comment':'Editor allocation is not a CPU selector bound. Runtime rejects bool/float integers, duplicate keys and nonfinite values.'}


def render_bundle(rom):
    assets=extract(rom)
    manifest={'format':FORMAT,'schema_version':1,'canonical_rom_sha256':sha(rom),
        'source_fields_sha256':sha(dump(assets)),'editable_bytes':84,'physical_blocks':6,'physical_fields':34,
        'owners':[],'ownership_bytes_added':0,'typed_build_bytes_added':0,'complete_domains_added':0,
        'status':'source_codec_pending_consumer_and_build_acceptance',
        'source_authority':'analysis/candidate_action_tables/generated/assets.json',
        'allocations':[{'id':key,'start':start,'end':start+width*count,'width':width,'count':count,
            'confidence':'probable','sha256':sha(rom[start:start+width*count])} for key,start,width,count in TABLES],
        'reader_anchors':[{'id':name,'start':pc,'end':pc+len(raw)//2,'bytes':raw,
            'confidence':'confirmed_original_bytes_only'} for name,pc,raw in ANCHORS],
        'boundaries':['No full CPU execution, natural selector domain or primary/build ownership follows from this field draft.',
            'The existing 01A492 action table remains in candidate_tables, with no duplicate authority.',
            'Initial-list, mark-list and budget pointer indexes use three distinct original WORD formulas.',
            'Pointers retain all32 bits and duplicate values remain distinct physical fields.',
            'Source projections omit actual shared RAM, stack and external-call effects.']}
    text=('# Actor-state and action-budget source fields\n\n'
        'confirmed: six separate physical allocations contain34 full-width fields in84 bytes.\n'
        'confirmed: assets.json is the single editable field source; the other files are derived.\n'
        'confirmed: state/message selectors are complete WORDs with wrap and signed indexes, not editor slot numbers.\n'
        'confirmed: initial-list bank indexing shifts WORD by1 without masking; bank1 reads a split LONG.\n'
        'confirmed: mark-list bank is AND2 then WORD shift1; budget bank is WORD shift2 without masking.\n'
        'confirmed: repeated pointers and offsets remain separate physical values. The existing01A492 table is not duplicated.\n'
        'confirmed: warnings do not normalize odd or out-of-domain pointer/offset source bits.\n'
        'unknown: natural input domains, actual call-stack/shared-RAM effects and edited-gameplay behavior.\n'
        'confirmed: no build integration, CPU owner or complete-domain claim follows from this standalone codec.\n')
    return {'assets.json':dump(assets),'schema.json':dump(schema()),'manifest.json':dump(manifest),
        'views.json':dump(inspect(rom,assets)),'README.md':text.encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import'))
    parser.add_argument('--rom',type=Path,default=DEFAULT_ROM)
    parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    read=lambda path:gb.af._read(gb.af.safe_path(path,regular_input=True),4*1024*1024)
    rom=read(args.rom);verify_rom(rom)
    if args.command=='export':bundle=render_bundle(rom);inputs=[args.rom]
    else:
        assets=gb.af.load_assets(read(args.assets));report=inspect(rom,assets)
        if args.command=='verify':print(dump(report).decode(),end='');return
        bundle={'rebuilt.bin':rebuild(rom,assets),'validation.json':dump(report)};inputs=[args.rom,args.assets]
    if args.output is None:raise ValueError('--output required')
    print(gb.publish(bundle,args.output,inputs))


if __name__=='__main__':main()
