"""Lossless 01A818 helper fields; editable table extents are not CPU domains."""
from __future__ import annotations
import argparse
from pathlib import Path
import struct
from tools.graphics_build import graphics_build as gb

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_ROM=ROOT.parent/'work/original_g5510.bin'
DEFAULT_ASSETS=ROOT/'analysis/candidate_handler_tables/generated/assets.json'
FORMAT='g5510-candidate-handler-tables-v1'
EDITABLE_BYTES=52
TABLES=(('coefficient_words',0x1A1DC,2,18),('debit_pointers',0x1A808,4,4))
ANCHORS=(
    ('state_index',0x1A706,'3a38efd2e34dda78efd2e74d'),
    ('nonempty_increment',0x1A73C,'5845'),
    ('bit_increment',0x1A76C,'5845'),
    ('coefficient_reader',0x1A77A,'41fafa60c0f050004840d0705002'),
    ('debit_reader',0x1A7F4,'3038f6d6e548207b' '000c201090b8f39e20804e75'),
)
sha,dump=gb.sha,gb.dump


def verify_rom(rom):
    if type(rom) is not bytes:raise ValueError('immutable canonical ROM required')
    gb.af.verify_rom(rom)
    for name,pc,encoded in ANCHORS:
        raw=bytes.fromhex(encoded)
        if rom[pc:pc+len(raw)]!=raw:raise ValueError('original reader changed: '+name)


def extract(rom):
    verify_rom(rom)
    return {'schema_version':1,'format':FORMAT,**{
        key:list(struct.unpack_from('>'+str(count)+('H' if width==2 else 'I'),rom,start))
        for key,start,width,count in TABLES}}


def blocks(rom,assets):
    verify_rom(rom)
    gb.af._keys(assets,{'schema_version','format'}|{row[0] for row in TABLES},'handler source fields')
    if type(assets['schema_version']) is not int or assets['schema_version']!=1 or assets['format']!=FORMAT:
        raise ValueError('schema/format mismatch')
    rows=[]
    for key,start,width,count in TABLES:
        fields=gb.exact_list(assets[key],count,key)
        values=[gb.rf.integer(value,(1<<(8*width))-1,key) for value in fields]
        raw=struct.pack('>'+str(count)+('H' if width==2 else 'I'),*values)
        rows.append({'id':key,'start':start,'end':start+len(raw),'data':raw,
                     'role':'candidate_handler_'+('pointers' if width==4 else 'coefficient_words')})
    return rows


def rebuild(rom,assets):
    rows=blocks(rom,assets)
    image=bytearray(rom)
    for row in rows:image[row['start']:row['end']]=row['data']
    return bytes(image)


def image_check(image):
    if type(image) is not bytes or len(image)!=1048576:
        raise ValueError('explicit immutable 1 MiB source image required')


def signed_word(value):return value-65536 if value&0x8000 else value


def debit_lookup(image,bank_word):
    image_check(image);gb.rf.integer(bank_word,65535,'complete bank WORD')
    index=(bank_word<<2)&65535
    address=0x1A808+signed_word(index)
    pointer=int.from_bytes(image[address:address+4],'big')
    return {'bank_word':bank_word,'index_word':index,'source_address':address,
            'source_width':4,'source_value':pointer,'pointer_bus_address':pointer&0xFFFFFF,
            'inside_editor_allocation':0x1A808<=address and address+4<=0x1A818,
            'aligned_to_source_slot':(address-0x1A808)%4==0,'odd_pointer':bool(pointer&1)}


def coefficient_lookup(image,state_word,extra_pairs=0):
    """Pure same-state read projection, not a simulation of list/branch choices.

    extra_pairs=0/1/2 means zero/one/two executed ADDQ.W #4 operations.
    Actual CPU execution must decide those branches and perform both state reads.
    """
    image_check(image);gb.rf.integer(state_word,65535,'complete state WORD')
    gb.rf.integer(extra_pairs,2,'number of executed four-byte increments')
    index=(state_word<<1)&65535
    index=(index+state_word)&65535
    index=(index<<3)&65535
    for _ in range(extra_pairs):index=(index+4)&65535
    address=0x1A1DC+signed_word(index)
    return {'state_word':state_word,'extra_pairs':extra_pairs,'index_word':index,
            'source_address':address,'source_width':4,
            'multiplier_word':int.from_bytes(image[address:address+2],'big'),
            'addend_word':int.from_bytes(image[address+2:address+4],'big'),
            'inside_editor_allocation':0x1A1DC<=address and address+4<=0x1A200,
            'aligned_to_coefficient_pair':(address-0x1A1DC)%4==0,
            'assumes_same_value_for_both_state_reads':True,'branch_feasibility_claim':False}


def inspect(rom,assets):
    image=rebuild(rom,assets)
    samples=(0,1,2,3,4,5,0x1555,0x3FFF,0x4000,0x7FFF,0x8000,0xFFFF)
    pointers=[debit_lookup(image,value) for value in samples]
    coefficients=[coefficient_lookup(image,value,extra) for value in samples for extra in (0,1,2)]
    warnings=[{'code':'odd_pointer_value','table':'debit_pointers','slot':slot}
              for slot,pointer in enumerate(assets['debit_pointers']) if pointer&1]
    return {'format':FORMAT,'canonical_exact':image==rom,'editable_bytes':52,'physical_fields':22,
            'changed_bytes':sum(a!=b for a,b in zip(image,rom)),'image_sha256':sha(image),
            'debit_source_projections':pointers,'coefficient_source_projections':coefficients,
            'coefficient_pairs':[assets['coefficient_words'][index:index+2] for index in range(0,18,2)],
            'warning_policy':'report_only_no_source_normalization','warnings':warnings,
            'complete_domain_claim':False,'natural_execution_claim':False,'build_integration_claim':False}


def schema():
    properties={'schema_version':{'type':'integer','const':1},'format':{'const':FORMAT}}
    for key,_,width,count in TABLES:
        properties[key]={'type':'array','minItems':count,'maxItems':count,
                         'items':{'type':'integer','minimum':0,'maximum':(1<<(8*width))-1}}
    return {'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object',
            'required':list(properties),'additionalProperties':False,'properties':properties,
            '$comment':'Runtime rejects bool/float integers, duplicate keys and nonfinite values. Source allocations are not CPU bounds.'}


def render_bundle(rom):
    assets=extract(rom)
    manifest={'format':FORMAT,'schema_version':1,'canonical_rom_sha256':sha(rom),
        'source_fields_sha256':sha(dump(assets)),'editable_bytes':52,'physical_blocks':2,'physical_fields':22,
        'owners':[],'ownership_bytes_added':0,'typed_build_bytes_added':0,'complete_domains_added':0,
        'status':'standalone_source_codec_pending_global_build_acceptance',
        'source_authority':'analysis/candidate_handler_tables/generated/assets.json',
        'allocations':[{'id':key,'start':start,'end':start+width*count,'width':width,'count':count,
                        'confidence':'probable','sha256':sha(rom[start:start+width*count])}
                       for key,start,width,count in TABLES],
        'reader_anchors':[{'id':name,'start':pc,'end':pc+len(raw)//2,'bytes':raw,
                           'confidence':'confirmed_original_bytes_only'} for name,pc,raw in ANCHORS],
        'boundaries':['This codec does not simulate the handler, lists, RAM aliases, stack, SR or interrupts.',
            'The36B coefficient shape does not bound all full-WORD state accesses.',
            'The debit index is full WORD shifted by2 with signed16 address displacement, not a clamped bank slot.',
            'Coefficient views assume identical values for both EFD2 reads and parameterize executed ADDQ.W instructions, not feasible branches.',
            'Original pointer values equal the separate1AFAC table, but1A808 is a distinct physical authority; edits must not mirror.',
            'Keep all32 pointer bits and18 independent unsigned WORD fields; no clamp, normalization or deduplication.',
            'No new natural execution, primary owner or complete domain follows from table shape or lossless rebuilding.']}
    description=('# Candidate01A818 helper source fields\n\n'
        'confirmed:52 bytes/22 scalars in two physical allocations; assets.json is the sole editable source.\n'
        'confirmed: nine coefficient pairs remain18 independent unsigned WORDs; four pointers retain32 bits.\n'
        'confirmed: debit full-WORD bank shift2 and coefficient WORD24*state plus executed4-byte increments use signed indexes.\n'
        'confirmed: projection views can read outside editor extents and never clamp selectors.\n'
        'confirmed: the separate1AFAC pointer source is not copied, edited or merged with this1A808 source.\n'
        'unknown: natural state/selector domain, both-read state changes, list feasibility and full execution effects.\n'
        'confirmed: standalone codec claims0 owner,0 integrated typed delta,0 complete domains.\n')
    return {'assets.json':dump(assets),'schema.json':dump(schema()),'manifest.json':dump(manifest),
            'views.json':dump(inspect(rom,assets)),'README.md':description.encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    for command in ('export','verify','import'):
        sub=commands.add_parser(command)
        sub.add_argument('--rom',type=Path,default=DEFAULT_ROM)
        if command!='export':sub.add_argument('--assets',type=Path,default=DEFAULT_ASSETS)
        if command!='verify':sub.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    read=lambda path:gb.af._read(gb.af.safe_path(path,regular_input=True),4*1024*1024)
    rom=read(args.rom);verify_rom(rom)
    if args.command=='export':bundle=render_bundle(rom);inputs=[args.rom]
    else:
        assets=gb.af.load_assets(read(args.assets));report=inspect(rom,assets)
        if args.command=='verify':print(dump(report).decode(),end='');return
        bundle={'rebuilt.bin':rebuild(rom,assets),'validation.json':dump(report)};inputs=[args.rom,args.assets]
    print(gb.publish(bundle,args.output,inputs))


if __name__=='__main__':main()
