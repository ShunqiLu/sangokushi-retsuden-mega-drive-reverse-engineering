"""Lossless source tables; editor extents are not original CPU input bounds."""
from __future__ import annotations
import argparse
from pathlib import Path
import struct

from tools.graphics_build import graphics_build as gb

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=ROOT.parent/'work/original_g5510.bin'
DEFAULT_ASSETS=ROOT/'analysis/candidate_tables/generated/assets.json'
FORMAT='g5510-candidate-tables-v1'
EDITABLE_BYTES=258
sha,dump=gb.sha,gb.dump
DISPATCH={
    'filter':(0x17BB2,0x17BF0,'filter_dispatch_offsets',
              (0x17BBE,0x17C1A,0x17BF0,0x17C36,0x17C56,0x17C3C)),
    'action':(0x1A492,0x1A49E,'action_dispatch_offsets',
              (0x1A49E,0x1A49E,0x1A818,0x1A9B0,0x1AC26,0x1A818)),
}
NUMERIC_START,NUMERIC_END=0x30876,0x30960
ANCHORS={
    'filter_dispatch':(0x17B9A,'48e706003e38f6d4e34f3e3b700c4ebb70464cdf00604e75'),
    'action_dispatch':(0x1A47A,'33fcffff00ff70263038f6d4e348303b00084ebb00104e75'),
    'numeric_entry_and_scan':(0x3080E,'48e770804a8067000014610000169082650000085241544260f430014cdf010e4e750c800002358d651404800002358d243c000002fa323c017d6000002a42417401424341fa0022b090650000065c8860f62628fffa3428fffe90833202e24902820000ffff4e75'),
}


def verify_rom(rom):
    if type(rom) is not bytes:raise ValueError('immutable original ROM bytes required')
    gb.af.verify_rom(rom)
    for name,(address,raw) in ANCHORS.items():
        if rom[address:address+len(raw)//2]!=bytes.fromhex(raw):
            raise ValueError('original candidate-table reader changed: '+name)


def integer(value,bits,label):return gb.rf.integer(value,(1<<bits)-1,label)
def signed_word(value):return value-65536 if value&0x8000 else value


def extract(rom):
    verify_rom(rom)
    result={'schema_version':1,'format':FORMAT}
    for start,base,key,targets in DISPATCH.values():
        result[key]=list(struct.unpack_from('>6H',rom,start))
    result['numeric_records']=[{'threshold_long':threshold,'seed_word':seed}
        for threshold,seed in struct.iter_unpack('>IH',rom[NUMERIC_START:NUMERIC_END])]
    return result


def blocks(rom,assets):
    verify_rom(rom)
    gb.af._keys(assets,{'schema_version','format','filter_dispatch_offsets','action_dispatch_offsets','numeric_records'},'candidate source')
    if type(assets['schema_version']) is not int or assets['schema_version']!=1 or assets['format']!=FORMAT:
        raise ValueError('fixed schema/format changed')
    result=[]
    for start,base,key,targets in DISPATCH.values():
        words=[integer(v,16,key) for v in gb.exact_list(assets[key],6,key)]
        result.append({'id':key,'start':start,'end':start+12,'role':'candidate_dispatch_words','data':struct.pack('>6H',*words)})
    data=bytearray()
    for row in gb.exact_list(assets['numeric_records'],39,'numeric records'):
        gb.af._keys(row,{'threshold_long','seed_word'},'numeric record')
        data.extend(struct.pack('>IH',integer(row['threshold_long'],32,'full threshold LONG'),integer(row['seed_word'],16,'full seed WORD')))
    result.append({'id':'numeric_records','start':NUMERIC_START,'end':NUMERIC_END,'role':'numeric_threshold_seed_fields','data':bytes(data)})
    return sorted(result,key=lambda row:row['start'])


def rebuild(rom,assets):
    image=bytearray(rom)
    for row in blocks(rom,assets):image[row['start']:row['end']]=row['data']
    return bytes(image)


def _lookup(image,selector,which):
    integer(selector,16,'full selector WORD')
    if type(which) is not str or which not in DISPATCH:raise ValueError('unknown dispatch view')
    start,base,key,targets=DISPATCH[which]
    index=(selector<<1)&65535; address=start+signed_word(index)
    word=int.from_bytes(image[address:address+2],'big')
    target=(base+signed_word(word))&0xFFFFFFFF
    return {'selector_word':selector,'index_word':index,'source_address':address,'source_word':word,
        'signed_offset':signed_word(word),'logical_target':target,'bus_target':target&0xFFFFFF,
        'odd_target':bool(target&1),'inside_editor_table':start<=address<start+12,
        'target_in_known_handler_set':target in targets}


def dispatch_lookup(rom,assets,selector,which='filter'):
    """Immutable source-only address arithmetic, not shared-stack execution."""
    return _lookup(rebuild(rom,assets),selector,which)


def inspect(rom,assets):
    image=rebuild(rom,assets); warnings=[]
    views={name:[_lookup(image,value,name) for value in (0,1,2,3,4,5,6,7,0x7FFF,0x8000,0x8005,0xFFFF)] for name in DISPATCH}
    for name in DISPATCH:
        for row in views[name][:6]:
            if row['odd_target']:warnings.append({'code':'odd_dispatch_target','dispatch':name,'slot':row['selector_word']})
            if not row['target_in_known_handler_set']:warnings.append({'code':'target_outside_known_handler_set','dispatch':name,'slot':row['selector_word']})
    thresholds=[row['threshold_long'] for row in assets['numeric_records']]
    if any(a>=b for a,b in zip(thresholds,thresholds[1:])):
        warnings.append({'code':'non_increasing_thresholds','meaning':'Original scan is not bounded by the editor allocation.'})
    if thresholds[0]!=1 or thresholds[-1]!=0x2358D:
        warnings.append({'code':'changed_scan_endpoint','meaning':'Original zero fast-path and high-input cutoff are code immediates, not regenerated from table fields.'})
    return {'format':FORMAT,'canonical_exact':image==rom,'image_sha256':sha(image),
        'changed_bytes':sum(a!=b for a,b in zip(rom,image)),'editable_bytes':EDITABLE_BYTES,
        'warning_policy':'report_only_no_normalization','warnings':warnings,'dispatch_views':views,
        'last_seed_word':assets['numeric_records'][-1]['seed_word'],
        'complete_indirect_domains_added':0,'natural_selection_domain_complete':False,'edited_gameplay_validated':False}


def manifest(rom):
    assets=extract(rom); rows=blocks(rom,assets)
    # Read-set assertion is original-code conditional evidence. It does not
    # claim that every input or any selector lifetime has occurred naturally.
    owners=[]
    for name,start,end,confidence,role in (
        ('filter_dispatch_offsets',0x17BB2,0x17BBE,'confirmed','candidate_dispatch_words'),
        ('action_dispatch_offsets',0x1A492,0x1A49E,'confirmed','candidate_dispatch_words'),
        ('numeric_referenced_fields',NUMERIC_START,NUMERIC_END-2,'confirmed','numeric_threshold_seed_fields'),
        ('numeric_last_seed',NUMERIC_END-2,NUMERIC_END,'probable','numeric_seed_allocation')):
        owners.append({'id':name,'start':start,'end':end,'size':end-start,'confidence':confidence,
            'role':role,'sha256':sha(rom[start:end]),
            'scope':'Conditional original source-field interpretation, not natural input-domain or lifetime proof.'})
    return {'schema_version':1,'format':FORMAT,'canonical_rom_sha256':sha(rom),'source_fields_sha256':sha(dump(assets)),
        'editable_bytes':EDITABLE_BYTES,'build_block_count':3,'conditional_field_bytes':256,'probable_last_seed_bytes':2,
        'owners':owners,'consumer_anchors':[{'id':name,'start':start,'end':start+len(raw)//2,'bytes':raw,
            'sha256':sha(bytes.fromhex(raw)),'kind':'original_instruction_anchor'} for name,(start,raw) in ANCHORS.items()],
        'dispatch_tables':[{'id':name,'start':start,'end':start+12,'relative_base':base,'source_key':key,
            'known_targets_for_inputs_0_to_5':list(targets),'editor_entries':6,'original_cpu_has_local_six_entry_guard':False,
            'complete_target_domain':False} for name,(start,base,key,targets) in DISPATCH.items()],
        'numeric_read_contract':{'entry':0x3080E,'zero_input':'returns before any table read',
            'table_input_min':1,'table_input_max':0x2358C,'high_input_cutoff':0x2358D,
            'high_input_path':'uses code immediates, not the final table seed',
            'conditional_reference_start':NUMERIC_START,'conditional_reference_end':NUMERIC_END-2,
            'direct_helper_zero_input_alias':{'entry':0x30830,'start':0x30870,'end':0x30876,
                'meaning':'Bypasses complete-entry zero guard and reads prior instruction bytes; no duplicated editable table prefix.'}},
        'complete_indirect_domains_added':0,'runtime_validation_added':False,'natural_selection_domain_complete':False,
        'boundaries':['Full source WORDs/LONGs are accepted; warnings never normalize or restrict them to canonical values.',
            'The six-slot editor allocation does not bound original full-WORD dispatch arithmetic.',
            'Duplicate action targets at slots0/1 and2/5 retain independent physical source WORDs.',
            'NUMERIC last seed is preserved as a probable allocation field but is not read by the complete canonical entry.',
            'Changing table values may read outside the editor allocation, branch to odd addresses or fail to terminate.',
            'Source address projections omit shared RAM, stack, status-register and external-device behavior; independent CPU models supply that separate evidence.']}


def schema():
    word={'type':'integer','minimum':0,'maximum':65535}; long={'type':'integer','minimum':0,'maximum':4294967295}
    def obj(fields):return {'type':'object','additionalProperties':False,'required':list(fields),'properties':fields}
    def array(count,item):return {'type':'array','minItems':count,'maxItems':count,'items':item}
    return {'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Full-width candidate dispatch and numerical seed fields',
        **obj({'schema_version':{'type':'integer','const':1},'format':{'const':FORMAT},
            'filter_dispatch_offsets':array(6,word),'action_dispatch_offsets':array(6,word),
            'numeric_records':array(39,obj({'threshold_long':long,'seed_word':word}))}),
        '$comment':'Runtime rejects bool/float integers, duplicate keys and nonfinite values. Fixed source extents are editor topology only.'}


def render_bundle(rom):
    assets=extract(rom); info=manifest(rom)
    text=('# Candidate dispatch and numerical seed source fields\n\n'
        'confirmed: assets.json is the unique editable source; other artifacts are derived.\n\n'
        '- confirmed: two six-WORD dispatch tables and39 full LONG/WORD numeric records:258 physical bytes in three disjoint blocks.\n'
        '- confirmed: conditionally referenced source fields cover256B. The last2B seed remains probable, not a new confirmed owner.\n'
        '- confirmed: both dispatchers use WORD left shift, signed WORD source indexing and signed WORD target offsets without a six-slot CPU guard.\n'
        '- confirmed: second-table duplicate targets retain separate physical slots, never normalized aliases.\n'
        '- confirmed: complete numeric entry skips table reads for zero and inputs>=0x2358D; its high-input constants are separate code fields.\n'
        '- confirmed: direct numeric helper input0 reads previous instruction bytes at30870..30876; they are not a copied editable record.\n'
        '- unknown: natural full selector domains, edited gameplay validity, caller lifetimes and all possible dynamic aliases.\n'
        '- confirmed: no new natural runtime observation or complete indirect domain is claimed.\n')
    return {'assets.json':dump(assets),'schema.json':dump(schema()),'manifest.json':dump(info),
            'views.json':dump(inspect(rom,assets)),'README.md':text.encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','verify','import'))
    parser.add_argument('--rom',type=Path,default=DEFAULT_ROM);parser.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    read=lambda path:gb.af._read(gb.af.safe_path(path,regular_input=True),4*1024*1024)
    rom=read(args.rom);verify_rom(rom)
    if args.command=='export':bundle=render_bundle(rom);inputs=[args.rom]
    else:
        assets=gb.af.load_assets(read(args.assets)); report=inspect(rom,assets)
        if args.command=='verify':print(dump(report).decode(),end='');return
        bundle={'rebuilt.bin':rebuild(rom,assets),'validation.json':dump(report)};inputs=[args.rom,args.assets]
    if args.output is None:raise ValueError('--output required')
    print(gb.publish(bundle,args.output,inputs))


if __name__=='__main__':main()
