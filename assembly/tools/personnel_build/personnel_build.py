"""Typed build adapter; scenario_candidates.json remains the sole authority.

The legacy serializer supplies every scenario byte. An independent field
inventory checks those bytes and supplies the fixed external descriptor table.
No replacement asset JSON, raw-ROM fallback, relocated topology or new semantic
ownership is introduced.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

from tools.audio_formats import audio_formats as af
from tools.graphics_build import graphics_build as gb
from tools.personnel_flow import personnel_flow as flow

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = ROOT.parent / "work" / "original_g5510.bin"
DEFAULT_ASSETS = ROOT / "analysis/personnel_flow/generated/scenario_candidates.json"
GENERATED = ROOT / "analysis/personnel_build/generated"
POINTER_START, POINTER_END = 0x11080, 0x1108C
START, END = 0xAADE2, 0xAB8C4
SCENARIO_SPANS = ((0xAADE2,0xAB2C0),(0xAB2C0,0xAB65A),(0xAB65A,0xAB8C4))
EDITABLE_BYTES = 2798
SCENARIO_BYTES = 2786
FORMAT = "g5510-existing-personnel-authority-build-v1"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(value):
    return (json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()


def verify_rom(rom):
    if type(rom) is not bytes or len(rom)!=flow.CANONICAL_SIZE or sha(rom)!=flow.CANONICAL_SHA256:
        raise ValueError("personnel build base must be the original canonical 1 MiB BIN")


def read(path, maximum=8*1024*1024):
    return af._read(af.safe_path(path,regular_input=True),maximum)


def load_assets(path=None):
    if path is None:
        path=DEFAULT_ASSETS
    path=af.safe_path(path,regular_input=True)
    if path.suffix.lower()!=".json":
        raise ValueError("personnel authority must use a .json extension")
    value=af.load_assets(read(path))
    if type(value) is not dict:
        raise ValueError("personnel authority root must be an object")
    return value


def _numeric_types(supplied, baseline, path=""):
    """Reject bool/float aliases even in structural fields compared by legacy ==.

    Optional diagnostic metadata remains optional and non-authoritative, matching
    the established serializer. Extra metadata is not reinterpreted as bytes.
    """
    if type(baseline) is int:
        if type(supplied) is not int:
            raise ValueError("integer field required at "+path)
    elif isinstance(baseline,dict) and isinstance(supplied,dict):
        for key,value in baseline.items():
            if key in supplied:
                _numeric_types(supplied[key],value,path+"/"+key)
    elif isinstance(baseline,list) and isinstance(supplied,list):
        for index,(value,expected) in enumerate(zip(supplied,baseline)):
            _numeric_types(value,expected,path+"/"+str(index))


def _fixed(supplied, baseline, keys):
    for key in keys:
        if key in supplied and supplied[key]!=baseline[key]:
            raise ValueError("fixed personnel topology field differs: "+key)


def _topology(assets, baseline):
    if type(assets) is not dict:
        raise ValueError("personnel authority must be an object")
    scenarios=assets.get("scenarios")
    if type(scenarios) is not list or len(scenarios)!=3:
        raise ValueError("three ordered personnel scenarios required")
    pointer=assets.get("scenario_pointer_table")
    if pointer is not None:
        if type(pointer) is not dict:
            raise ValueError("scenario_pointer_table must be an object")
        for key,expected in (("rom_offset",POINTER_START),("count",3)):
            if key in pointer and (type(pointer[key]) is not int or pointer[key]!=expected):
                raise ValueError("fixed external pointer table differs")
    for supplied,expected in zip(scenarios,baseline):
        if type(supplied) is not dict:
            raise ValueError("scenario must be an object")
        _numeric_types(supplied,expected)
        _fixed(supplied,expected,("scenario_end","scenario_length","city_offset_table_rom_offset","city_rule_stream_rom_offset"))
        for rows,keys in (("force_year_lists",("rom_offset","terminator_rom_offset")),
                          ("city_rules",("rom_offset",))):
            values=supplied.get(rows)
            if type(values) is list:
                for row,reference in zip(values,expected[rows]):
                    if type(row) is dict:
                        _fixed(row,reference,keys)
    for section,keys in (("canonical_source",("size",)),("candidate_block",("start","end","length"))):
        value=assets.get(section)
        if type(value) is dict:
            for key in keys:
                if key in value and type(value[key]) is not int:
                    raise ValueError("integer topology value required: "+section+"/"+key)


def _inventory(assets, baseline):
    rows=[]
    def field(address,width,value,role,path,aliases=()):
        if type(value) is not int or not 0<=value<1<<(8*width):
            raise ValueError("raw field outside original source width: "+path)
        rows.append({"id":f"personnel_field_{address:06x}","start":address,"end":address+width,
                     "width_bytes":width,"value":value,"role":role,"source_paths":[path,*aliases]})
    for index,(scenario,expected) in enumerate(zip(assets["scenarios"],baseline)):
        base=f"/scenarios/{index}"
        start=expected["descriptor_rom_offset"]
        field(POINTER_START+4*index,4,scenario["descriptor_rom_offset"],"descriptor_pointer",base+"/descriptor_rom_offset")
        for slot,value in enumerate(scenario["descriptor_pointers"]):
            field(start+slot*4,4,value,"descriptor_pointer",base+f"/descriptor_pointers/{slot}")
        for slot,(force,known) in enumerate(zip(scenario["force_year_lists"],expected["force_year_lists"])):
            path=base+f"/force_year_lists/{slot}"
            for entry_index,entry in enumerate(force["entries"]):
                address=known["rom_offset"]+entry_index*4
                field(address,2,entry["year_threshold_raw"],"force_year_word",path+f"/entries/{entry_index}/year_threshold_raw")
                field(address+2,2,entry["officer_id"],"force_officer_word",path+f"/entries/{entry_index}/officer_id")
            if slot<3:
                field(known["terminator_rom_offset"],2,force["terminator_raw"],"force_terminator_word",path+"/terminator_raw")
        for slot,value in enumerate(scenario["city_offset_words"]):
            aliases=(base+"/force_year_lists/3/terminator_raw",) if slot==0 else ()
            field(expected["city_offset_table_rom_offset"]+slot*2,2,value,
                  "shared_force_terminator_city_offset" if slot==0 else "city_offset_word",
                  base+f"/city_offset_words/{slot}",aliases)
        for city_index,(city,known) in enumerate(zip(scenario["city_rules"],expected["city_rules"])):
            path=base+f"/city_rules/{city_index}"
            for entry_index,entry in enumerate(city["entries"]):
                address=known["rom_offset"]+entry_index*6
                for delta,key,role in ((0,"year_threshold_raw","city_year_word"),
                                       (2,"candidate_officer_id","city_officer_word"),
                                       (4,"qualifier_raw","qualifier_word")):
                    field(address+delta,2,entry[key],role,path+f"/entries/{entry_index}/{key}")
            field(known["rom_offset"]+len(city["entries"])*6,2,city["terminator_raw"],"city_terminator_word",path+"/terminator_raw")
    rows.sort(key=lambda row:row["start"])
    return rows


def _prepare(rom, assets):
    verify_rom(rom)
    if assets is None:
        assets=load_assets()
    baseline=flow.parse_candidate_scenarios(rom)
    try:
        _topology(assets,baseline)
        payload=flow.serialize_candidate_bundle(assets,rom)
        fields=_inventory(assets,baseline)
    except (KeyError,TypeError,IndexError,OverflowError) as exc:
        raise ValueError("malformed personnel authority structure") from exc
    # Independent field packing certifies every output byte from the serializer.
    # It never imports canonical ROM slices as a fallback for an authored field.
    expected_ranges=[(POINTER_START,POINTER_END),*SCENARIO_SPANS]
    result=[]
    for index,(start,end) in enumerate(expected_ranges):
        selected=[row for row in fields if start<=row["start"]<end]
        cursor=start
        for row in selected:
            if row["start"]!=cursor or row["end"]>end:
                raise ValueError("personnel field inventory gap/overlap")
            cursor=row["end"]
        if cursor!=end:
            raise ValueError("personnel field inventory does not fill the fixed region")
        independently_packed=b"".join(row["value"].to_bytes(row["width_bytes"],"big") for row in selected)
        data=independently_packed if index==0 else payload[start-START:end-START]
        if independently_packed!=data:
            raise ValueError("existing serializer differs from independent raw field packing")
        result.append({"id":"personnel_candidate_directory" if index==0 else f"personnel_scenario_{index-1}",
                       "start":start,"end":end,"role":"personnel_candidate_pointers" if index==0 else "personnel_candidate_words",
                       "data":data})
    if sum(len(row["data"]) for row in result)!=EDITABLE_BYTES:
        raise ValueError("personnel build extent changed")
    return assets,fields,result


def blocks(rom, assets=None):
    return _prepare(rom,assets)[2]


def field_inventory(rom, assets=None):
    return _prepare(rom,assets)[1]


def rebuild(rom, assets=None):
    image=bytearray(rom)
    for row in blocks(rom,assets):
        image[row["start"]:row["end"]]=row["data"]
    return bytes(image)


def inspect(rom, assets=None):
    values,fields,rows=_prepare(rom,assets)
    warnings=[]
    for index,scenario in enumerate(values["scenarios"]):
        for slot,force in enumerate(scenario["force_year_lists"]):
            for entry_index,entry in enumerate(force["entries"]):
                if entry["year_threshold_raw"]&0x8000:
                    warnings.append({"kind":"force_year_has_terminator_bit","scenario":index,"slot":slot,"entry":entry_index,
                        "scope":"legacy serializer accepts all u16; CPU/parser treats this year as a terminator"})
        diagnostic=scenario.get("shared_alias")
        alias=diagnostic.get("raw_word") if isinstance(diagnostic,dict) else None
        if alias is not None and alias!=scenario["city_offset_words"][0]:
            warnings.append({"kind":"diagnostic_shared_alias_raw_word_is_stale","scenario":index,
                "scope":"ignored legacy diagnostic metadata; emitted authority is city_offset_words[0] plus checked force terminator"})
    return {"canonical_exact":all(rom[row["start"]:row["end"]]==row["data"] for row in rows),
            "typed_bytes":EDITABLE_BYTES,"field_count":len(fields),"warnings":warnings,
            "edited_gameplay_or_natural_paths_verified":False}


def contract():
    return {"format":FORMAT,"confidence":"confirmed","authority":"analysis/personnel_flow/generated/scenario_candidates.json",
        "existing_format":flow.CANDIDATE_BUNDLE_FORMAT,"serializer":"tools.personnel_flow.personnel_flow.serialize_candidate_bundle",
        "new_editable_json_created":False,"fixed_block_count":4,"typed_bytes":EDITABLE_BYTES,
        "fields":{"force_year_word":"all u16 retained, including legacy terminator-bit acceptance with warning",
            "officer_words":"all u16; neither byte narrowing nor officer-domain clamp",
            "qualifier_word":"all u16; existing qualifier_kind/value must agree with raw",
            "city_year_word":"existing nonterminator constraint 0..7FFF",
            "terminators":"all u16 values with bit15 set; fourth force aliases city_offset_words[0]",
            "offsets_pointers":"existing fixed topology only; external three LONGs derived from existing scenario offsets"},
        "diagnostic_metadata":"hex labels, historical hashes/statistics and shared_alias.raw_word are not additional editable bytes",
        "json_boundary":"duplicate keys/non-finite constants rejected; strict integer types prevent bool/float aliasing",
        "new_ownership_bytes":0,"complete_domains_added":0,"natural_execution_added":False}


def manifest(rom, assets=None):
    values,fields,rows=_prepare(rom,assets)
    return {"format":FORMAT,"canonical_rom_sha256":sha(rom),"source_fields_sha256":sha(dump(values)),
        "authority":"analysis/personnel_flow/generated/scenario_candidates.json",
        "legacy_serializer_sha256":sha(read(Path(flow.__file__))),
        "typed_bytes":EDITABLE_BYTES,"scenario_bytes":SCENARIO_BYTES,"directory_bytes":12,
        "field_count":len(fields),"word_fields":sum(row["width_bytes"]==2 for row in fields),
        "long_fields":sum(row["width_bytes"]==4 for row in fields),"block_count":4,
        "already_owned_bytes":EDITABLE_BYTES,"new_ownership_bytes":0,"complete_domains_added":0,
        "blocks":[{**{key:row[key] for key in ("id","start","end","role")},"size":len(row["data"]),"sha256":sha(row["data"])} for row in rows],
        "shared_aliases":[row for row in fields if len(row["source_paths"])>1],
        "scope":"lossless existing-authority build; no new gameplay or natural-input proof",
        "inspection":inspect(rom,values)}


README = """# Existing personnel candidate authority: typed build adapter

No assets.json is generated here. The only editable source remains
analysis/personnel_flow/generated/scenario_candidates.json, serialized by the
existing personnel_flow serializer. Four fixed blocks occupy 2798 bytes:
11080..1108C (3 derived LONG directory entries) and AADE2..AB8C4 (3 scenarios).
An independent 1378-field inventory checks all 1357 WORDs and 21 LONGs; the
fourth force terminator shares city-offset slot0 and is emitted exactly once.

Complete officer/qualifier WORDs and negative terminator payloads are preserved.
The old force-year serializer accepts bit15 unlike its city-year serializer;
this adapter preserves that authoring range and reports the parser/CPU boundary,
not silently normalizing or rejecting previously allowed source words.
Fixed topology is not a CPU selector-domain proof. Existing diagnostic hashes,
hex labels/statistics and shared_alias.raw_word are not extra byte authorities.

Typed build reproduction adds zero semantic ownership and no runtime evidence.
The original JSON, serializer and ROM are read-only during export/verification.
"""


def fields_csv(rows):
    stream=io.StringIO(newline="")
    names=("id","start","end","width_bytes","value_hex","role","source_paths")
    writer=csv.DictWriter(stream,fieldnames=names,lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({**{key:row[key] for key in ("id","start","end","width_bytes","role")},
                         "value_hex":f"{row['value']:0{row['width_bytes']*2}X}",
                         "source_paths":" | ".join(row["source_paths"])})
    return stream.getvalue().encode()


def render_bundle(rom):
    values=load_assets()
    return {"manifest.json":dump(manifest(rom,values)),"fields.csv":fields_csv(field_inventory(rom,values)),
            "contract.json":dump(contract()),"README.md":README.encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("verify","export","import"))
    parser.add_argument("--rom",type=Path,default=DEFAULT_ROM)
    parser.add_argument("--assets",type=Path,default=DEFAULT_ASSETS)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    rom=read(args.rom,flow.CANONICAL_SIZE)
    values=load_assets(args.assets)
    if args.command=="verify":
        print(json.dumps(inspect(rom,values),sort_keys=True))
    else:
        if args.output is None:
            raise ValueError("fresh --output directory required")
        if args.command=="export":
            files={"manifest.json":dump(manifest(rom,values)),"fields.csv":fields_csv(field_inventory(rom,values)),
                   "contract.json":dump(contract()),"README.md":README.encode()}
        else:
            files={"rebuilt_personnel.bin":rebuild(rom,values)}
        gb.publish(files,args.output,[args.rom,args.assets,Path(flow.__file__),Path(__file__)])
        print(json.dumps({"files":len(files),"typed_bytes":EDITABLE_BYTES,"output":str(args.output)}))


if __name__=="__main__":
    main()
