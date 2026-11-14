"""3150 source BYTEs, conditionally read as 126 original FM register records.

The fixed E2EB instrument base, real 25-BYTE loader and signed EF parameter
branches establish source aliases, not padding, playback safety or a natural
song-selector domain. All 21 register and four TL source BYTEs remain complete.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.battle_deployment_parameters import codec as shared

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE=0x100000
ROM_SHA256=reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM=ROOT.parent/"work/original_g5510.bin"
OUTPUT_ROOT=ROOT/"build/fm_instrument_alias_fields"
FORMAL_ROOT=ROOT/"analysis/fm_instrument_alias_fields/generated"
DEFAULT_BUNDLE=FORMAL_ROOT
DEFAULT_FIELDS=FORMAL_ROOT/"fields.json"
FORMAT="g5510-conditionally-read-FM-alias-register-BYTE-fields-v1"
MAX_JSON=1024*1024
MEMBERS=frozenset(("fields.json","fields.schema.json","validation.json","manifest.json"))
Z80_ROM_BASE=0x69D2
INSTRUMENT_Z80_BASE=0xE2EB
INSTRUMENT_ROM_BASE=0xFE2EB
START,END=0xFE31D,0xFEF6B
FIRST_INDEX,LAST_INDEX=2,127
RECORD_COUNT,RECORD_BYTES=126,25
EDITABLE_BYTES=3150
REGISTER_MAP=(0xB0,0x30,0x38,0x34,0x3C,0x50,0x58,0x54,0x5C,0x60,0x68,0x64,0x6C,
              0x70,0x78,0x74,0x7C,0x80,0x88,0x84,0x8C,0x40,0x48,0x44,0x4C)
MAP_PATH="analysis/audio/generated/instructions.csv"
MAP_SHA256=reference_value(__name__, 'MAP_SHA256')
OLD_FORMAT_PATH="tools/audio_formats/audio_formats.py"
OLD_FORMAT_SHA256=reference_value(__name__, 'OLD_FORMAT_SHA256')
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_PATH="build/direct_code/layout/"+LAYOUT_ID+"/m68k_bank0f.s"
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
CONSUMERS=(
    (0x69AA,0x69B7,reference_value(__name__, 'CONSUMERS')),
    (0x69F2,0x6A07,reference_value(__name__, 'CONSUMERS_2')),
    (0x6E56,0x6E70,reference_value(__name__, 'CONSUMERS_3')),
    (0x6E9A,0x6EB3,reference_value(__name__, 'CONSUMERS_4')),
    (0x6EB7,0x6EDC,reference_value(__name__, 'CONSUMERS_5')),
    (0x6F28,0x6F3D,reference_value(__name__, 'CONSUMERS_6')),
    (0x70DE,0x70F1,reference_value(__name__, 'CONSUMERS_7')),
    (0x76FF,0x7742,reference_value(__name__, 'CONSUMERS_8')),
    (0x775C,0x777B,reference_value(__name__, 'CONSUMERS_9')),
    (0xF827B,0xF827D,reference_value(__name__, 'CONSUMERS_10')),
    (0xFE21C,0xFE222,reference_value(__name__, 'CONSUMERS_11')),
)
INSTRUCTIONS=(
    (0x28,"4f"),(0x29,"0600"),(0x2B,"09"),(0x2C,"09"),(0x30,"7e"),(0x31,"23"),(0x32,"66"),(0x33,"6f"),
    (0x484,"2a371c"),(0x487,"3a191c"),(0x48A,"b7"),(0x48B,"2806"),(0x48D,"dd6e2a"),(0x490,"dd662b"),
    (0x493,"af"),(0x494,"b0"),(0x495,"2806"),(0x497,"111900"),(0x49A,"19"),(0x49B,"10fd"),
    (0x4EE,"cd0405"),(0x4F4,"0614"),(0x4F6,"cd0405"),(0x4F9,"10fb"),(0x4FB,"dd751c"),(0x4FE,"dd741d"),
    (0x504,"1a"),(0x506,"4e"),(0x507,"23"),(0x508,"d7"),
    (0x556,"d681"),(0x55E,"0e04"),(0x560,"e7"),(0x561,"ef"),(0x564,"f7"),(0x565,"22371c"),
    (0x70C,"3a011c"),(0x70F,"07"),(0x710,"320060"),(0x713,"0608"),(0x715,"3a001c"),(0x718,"320060"),(0x71B,"0f"),(0x71C,"10fa"),
    (0xD2D,"ddcb017e"),(0xD31,"2038"),(0xD36,"1a"),(0xD37,"dd7708"),(0xD3C,"1a"),(0xD3D,"dd770f"),
    (0xD41,"b7"),(0xD42,"f2600d"),(0xD46,"210080"),(0xD49,"0e04"),(0xD4B,"dd7e0f"),(0xD4E,"d681"),
    (0xD50,"cd2300"),(0xD53,"ef"),(0xD54,"f7"),(0xD55,"dd7e08"),(0xD58,"e67f"),(0xD5A,"47"),(0xD5B,"cd9304"),
    (0xD62,"47"),(0xD63,"cd8404"),(0xD66,"cde504"),
    (0xD8E,"dd6e1c"),(0xD91,"dd661d"),(0xD94,"0604"),(0xD96,"7e"),(0xD98,"f29e0d"),
    (0xD9B,"dd8606"),(0xD9E,"e67f"),(0xDA4,"23"),(0xDA5,"10ef"),
)
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
load_fields=shared.load_fields
safe_path,read_bounded,put=shared.safe_path,shared.read_bounded,shared.put


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=ROM_SIZE or sha(rom)!=ROM_SHA256:
        raise ValueError("canonical ROM bytes, size and SHA-256 required")
    for start,end,expected in CONSUMERS:
        if sha(rom[start:end])!=expected: raise ValueError("pinned original bank/header/loader source differs")


def metadata():
    return dict(format=FORMAT,confidence="candidate",source_confidence="confirmed",
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        physical_scope=dict(start=START,end=END,bytes=EDITABLE_BYTES,records=126,first_index=2,last_index=127,
            stride_BYTES=25,register_payload_BYTES=21,TL_source_BYTES=4),
        old_authority_aliases=dict(start=INSTRUMENT_ROM_BASE,end=START,records=2,bytes=50,emitted_again=False,
            source_sha256=reference_value(__name__, 'metadata'),
            format_source=dict(path=OLD_FORMAT_PATH,sha256=OLD_FORMAT_SHA256)),
        preserved_unknown_tail=dict(start=END,end=ROM_SIZE,bytes=ROM_SIZE-END,emitted=False,padding_claim=False,confidence="unknown"),
        evidence=dict(source="canonical Z80 consumer bytes, real music9F header, old CFG map and frozen raw layout",
            original_map=dict(path=MAP_PATH,sha256=MAP_SHA256,consumer_confidence="confirmed_static_CFG_not_executed_PC"),
            frozen_raw_layout=dict(id=LAYOUT_ID,path=LAYOUT_PATH,sha256=LAYOUT_SHA256,line=88952,bank=15,
                offset=0xE31D,length=0x1CE3,typed_BYTES_this_package=3150,remaining_unknown_BYTES=0x1095,old_typed_overlap_BYTES=0),
            consumers=[dict(start=s,end=e,bytes=e-s,sha256=h) for s,e,h in CONSUMERS],
            instructions=[dict(Z80_address=a,ROM_address=Z80_ROM_BASE+a,bytes=b,confidence="confirmed") for a,b in INSTRUCTIONS],
            music_definition=dict(command_BYTE=0x9F,index_after_SUB81=30,pointer_ROM_address=0xF827B,
                pointer_LE_WORD=0xE21C,header_ROM_start=0xFE21C,header_hex="ebe206030206",
                instrument_base_LE_WORD=INSTRUMENT_Z80_BASE,header_load_Z80=0x564,RAM_base_store_Z80=0x565,RAM_base_address=0x1C37),
            bank=dict(bank_value_9bits=0x01F,Z80_window_start=0x8000,Z80_window_end=0x10000,
                ROM_window_start=0xF8000,ROM_window_end=ROM_SIZE,overlay_ROM_start=0x69AA,overlay_Z80_start=0x1C00,
                original_overlay_hex="0f800080b400cb800000000000",serial_bank_writer_Z80=[0x710,0x718]),
            conditions=dict(FM_channel="IX+01 bit7 clear",positive_path="music9F base1C37 and 1C19=0",
                negative_path="external music selector second BYTE9F supplies its header E2EB base",
                actual_song_uses_all_aliases=False,all_source_contexts_exhausted=False),
            parameter=dict(source_BYTE_read_Z80=0xD36,sign_branch_Z80=0xD42,
                positive_index="parameter BYTE0..127",negative_index="parameter BYTE128..255 AND7F",
                negative_index_mask_Z80=0xD58,constructed_index_range=[0,127],old_two_record_CPU_clamp=False,
                stride_load_Z80=0x497,stride_BYTES=25,stride_loop_Z80=0x49A,DJNZ_Z80=0x49B,
                index_zero_skips_DJNZ_loop=True),
            register_source=dict(first_read_Z80=0x506,first_calls=1,additional_DJNZ_calls=20,
                saved_TL_pointer_Z80=[0x4FB,0x4FE],TL_read_Z80=0xD96,TL_count=4,TL_DJNZ_Z80=0xDA5,
                register_bases=list(REGISTER_MAP),register_payload_count=21,TL_source_count=4,
                TL_rule="if source bit7 set, ADD8 channel attenuation; then AND7F; original source BYTE not normalized"),
            last_alias=dict(index=127,Z80_start=0xEF52,Z80_end=0xEF6B,ROM_start=0xFEF52,ROM_end=END),
            original_tail_is_all_zero=True,zero_content_is_padding=False,field_union_is_conditional_not_natural=True),
        playback_safety="unknown",natural_song_selection="unknown",target_hardware_effects="unknown",
        independent_CPU_comparison=False,full_audio_or_RNG_algorithm=False)


def record_fixed(index):
    start=INSTRUMENT_ROM_BASE+25*index
    return dict(instrument_index=index,start=start,end=start+25,Z80_start=INSTRUMENT_Z80_BASE+25*index,
        Z80_end=INSTRUMENT_Z80_BASE+25*index+25)


def extract(rom):
    verify_rom(rom)
    fields=metadata()
    fields["records"]=[dict(**record_fixed(i),register_payload_BYTEs=list(rom[s:s+21]),
        total_level_source_BYTEs=list(rom[s+21:s+25])) for i in range(2,128) for s in (INSTRUMENT_ROM_BASE+25*i,)]
    return fields


def pinned(value,fixed,mutable,label):
    keys(value,set(fixed)|set(mutable),label)
    for key,expected in fixed.items(): same(value[key],expected,label+"."+key)


def blocks(rom,fields):
    verify_rom(rom)
    pinned(fields,metadata(),{"records"},"FM alias package")
    raw=bytearray()
    for row,index in zip(exact_list(fields["records"],126,"fixed FM source records"),range(2,128)):
        pinned(row,record_fixed(index),{"register_payload_BYTEs","total_level_source_BYTEs"},"FM source record")
        for key,count in (("register_payload_BYTEs",21),("total_level_source_BYTEs",4)):
            raw.extend(uint(byte,255,"complete FM source BYTE") for byte in exact_list(row[key],count,key))
    if len(raw)!=EDITABLE_BYTES or END-START!=EDITABLE_BYTES: raise ValueError("fixed 3150-byte source union differs")
    return [dict(id="rom_FE31D_conditional_FM_source_aliases",start=START,end=END,data=bytes(raw),role="conditional_25_BYTE_FM_register_source_aliases")]


def rebuild(rom,fields):
    encoded=blocks(rom,fields)
    image=bytearray(rom)
    for row in encoded: image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def lookup(image,parameter_BYTE):
    """Fixed E2EB-base source diagnostic, conditional on the documented context."""
    if type(image) is not bytes or len(image)!=ROM_SIZE: raise ValueError("lookup requires complete bytes image")
    parameter=uint(parameter_BYTE,255,"complete EF parameter BYTE")
    index=parameter if parameter<128 else parameter&127
    start=INSTRUMENT_ROM_BASE+25*index
    return dict(**record_fixed(index),parameter_BYTE=parameter,
        path="positive_current_music9F" if parameter<128 else "negative_external_music9F",
        register_payload_BYTEs=list(image[start:start+21]),total_level_source_BYTEs=list(image[start+21:start+25]),
        inside_edit_scope=index>=2,old_authority_alias=index<2)


def TL_preview(source_BYTE,attenuation_BYTE):
    source=uint(source_BYTE,255,"complete TL source BYTE")
    attenuation=uint(attenuation_BYTE,255,"complete channel attenuation BYTE")
    return ((source+attenuation)&255 if source&128 else source)&127


def schema():
    def obj(properties): return dict(type="object",properties=properties,required=list(properties),additionalProperties=False)
    def exact(items): return dict(type="array",prefixItems=items,items=False,minItems=len(items),maxItems=len(items))
    def fixed(value):
        if type(value) is dict: return obj({k:fixed(v) for k,v in value.items()})
        if type(value) is list: return exact([fixed(v) for v in value])
        return dict(type={str:"string",int:"integer",bool:"boolean"}[type(value)],const=value)
    def BYTEs(count): return dict(type="array",minItems=count,maxItems=count,items=dict(type="integer",minimum=0,maximum=255))
    result=obj({**{k:fixed(v) for k,v in metadata().items()},"records":exact([obj({**{k:fixed(v) for k,v in record_fixed(i).items()},
        "register_payload_BYTEs":BYTEs(21),"total_level_source_BYTEs":BYTEs(4)}) for i in range(2,128)])})
    result["$schema"]="https://json-schema.org/draft/2020-12/schema"
    result["description"]="126 conditional 25-BYTE FM source aliases; all BYTE bits editable, no TL normalization, natural-domain or padding claim."
    return result


def render_bundle(rom):
    fields=extract(rom)
    serialized=dump(fields)
    image=rebuild(rom,load_fields(serialized))
    if image!=rom: raise ValueError("serialized whole-ROM source roundtrip differs")
    encoded=blocks(rom,fields)
    report=dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=1,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),preview_is_editing_authority=False,
        parameter_alias_examples=[lookup(rom,i) for i in (0,1,2,127,128,129,130,255)],
        blocks=[{k:v for k,v in row.items() if k!="data"}|dict(bytes=len(row["data"]),sha256=sha(row["data"])) for row in encoded])
    members={"fields.json":serialized,"fields.schema.json":dump(schema()),"validation.json":dump(report)}
    members["manifest.json"]=dump(dict(**metadata(),editable_bytes=EDITABLE_BYTES,physical_blocks=1,
        members={name:dict(bytes=len(data),sha256=sha(data)) for name,data in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError("output must stay in fm_instrument_alias_fields build scope or exact formal bundle")
    if path.exists() or not path.parent.is_dir(): raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","import","verify"))
    parser.add_argument("--rom",default=str(DEFAULT_ROM))
    parser.add_argument("--fields")
    parser.add_argument("--bundle")
    parser.add_argument("--output")
    args=parser.parse_args(argv)
    target=None
    if args.command=="export":
        if args.output is None or args.fields is not None or args.bundle is not None: raise ValueError("export requires fresh output only")
        target=fresh_output(args.output,bundle=True)
    elif args.command=="import":
        if args.output is None or args.bundle is not None: raise ValueError("import requires fields and fresh output")
        target=fresh_output(args.output)
        if target.suffix.lower()!=".bin": raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify accepts fields or bundle and does not write")
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=="export":
        members=render_bundle(rom)
        target.mkdir()
        for name,data in members.items(): put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={name:sha(data) for name,data in members.items()})
    elif args.command=="verify" and args.bundle is not None:
        bundle=safe_path(args.bundle)
        if not bundle.is_dir() or {p.name for p in bundle.iterdir()}!=MEMBERS: raise ValueError("exact four-member bundle required")
        for name,data in render_bundle(rom).items():
            if read_bounded(bundle/name,MAX_JSON)!=data: raise ValueError("canonical bundle drift: "+name)
        result=dict(path=str(bundle),verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,whole_ROM_sha256=ROM_SHA256)
    else:
        fields=load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON))
        image=rebuild(rom,fields)
        if target is not None: put(target,image)
        result=dict(path=None if target is None else str(target),editable_bytes=EDITABLE_BYTES,
            bytes=len(image),exact_canonical=image==rom,sha256=sha(image))
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__=="__main__": raise SystemExit(main())
