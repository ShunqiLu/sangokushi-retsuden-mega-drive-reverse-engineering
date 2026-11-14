"""Use the existing transport schema/serializer as the sole cargo encoding.

This adds the already recovered24-byte table to the unified editable layout.
No new transport semantics, code owner or natural-domain claim is created.
"""
import argparse
from tools.direct_code import direct_code as d
from tools.transport_flow import transport_flow as old
f=d.f
ROOT=d.ROOT
DEFAULT_FIELDS=ROOT/'analysis/transport_cargo_build/generated/fields.json'
OUTPUT_ROOT=ROOT/'build/transport_cargo_build'
EDITABLE_BYTES=24
sha=f.sha;dump=f.dump;load_fields=f.load_json

def extract(rom):
    f.verify_rom(rom)
    fields=old.cargo_bundle(rom);blocks(rom,fields);return fields

def blocks(rom,fields):
    f.verify_rom(rom)
    expected=old.cargo_bundle(rom)
    f.keys(fields,set(expected),'original transport cargo')
    for key in ('format','source','resource'):f.same(fields[key],expected[key],'cargo.'+key)
    entries=fields['entries']
    if type(entries)is not list or len(entries)!=3:raise ValueError('three cargo choices required')
    for row,original in zip(entries,expected['entries']):
        f.keys(row,set(original),'cargo entry')
        for key in ('choice_index','record_type','label_zh'):f.same(row[key],original[key],'cargo.'+key)
    # Keep the established old editor range and exact sixBE32 values.
    data=old.serialize_cargo_bundle(fields)
    if len(data)!=EDITABLE_BYTES:raise ValueError('fixed cargo source width changed')
    return [dict(id='transport_cargo_table',start=old.CARGO_TABLE_START,
                 end=old.CARGO_TABLE_END,data=data,role='original_transport_gold_food_BE32')]

def rebuild(rom,fields):
    image=bytearray(rom)
    for b in blocks(rom,fields):image[b['start']:b['end']]=b['data']
    return bytes(image)

def render_bundle(rom):
    fields=extract(rom)
    return {'fields.json':dump(fields),'manifest.json':dump(dict(editable_bytes=24,
        fields_sha256=sha(dump(fields)),reused_codec='transport_flow.serialize_cargo_bundle',
        original_scope=[old.CARGO_TABLE_START,old.CARGO_TABLE_END],roundtrip_exact=rebuild(rom,fields)==rom,
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,
        label_zh_is_immutable_description_not_updated_UI_text=True))}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=('export','import','verify','promote'))
    p.add_argument('--fields',default=str(DEFAULT_FIELDS));p.add_argument('--output-root')
    args=p.parse_args(argv)
    target=None
    if args.command!='verify':
        target=DEFAULT_FIELDS.parent if args.command=='promote' else d.m.af.safe_path(args.output_root or '')
        if (target.exists() or (args.command!='promote' and
                (target==OUTPUT_ROOT or not target.is_relative_to(OUTPUT_ROOT)))):
            raise ValueError('fresh dedicated output required')
    rom=d.m.read(f.DEFAULT_ROM,f.ROM_SIZE)
    if args.command in ('export','promote'):bundle=render_bundle(rom)
    else:
        image=rebuild(rom,load_fields(d.m.read(args.fields)))
        if args.command=='verify':print(sha(image));return 0
        bundle={'rebuilt.bin':image}
    target.mkdir(parents=True)
    for name,data in bundle.items():
        with (target/name).open('xb') as stream:stream.write(data)
    print(str(target));return 0

if __name__=='__main__':raise SystemExit(main())
