"""Editable conditional command/parameter source aliases, not CPU execution.

Each new physical BYTE has one authority and an original supplied WORD/read-PC
witness. Read-only WORD views are reconstructed from the complete edited image;
the callback, later helper, stack and hardware are deliberately not executed.
"""
from __future__ import annotations

from tools.resource_reference import reference_value

import argparse
import json
from pathlib import Path

from tools.direct_code import direct_code as d
from tools.indexed_command_source_fields import codec as original

f, ROOT = d.f, d.ROOT
sha, dump, load_fields = f.sha, f.dump, f.load_json
FORMAT = "g5510-indexed-command-conditional-source-alias-fields-v1"
EDITABLE_BYTES = 1260
FORMAL_ROOT = ROOT / "analysis/indexed_command_source_alias_fields/generated"
DEFAULT_FIELDS = FORMAL_ROOT / "fields.json"
OUTPUT_ROOT = ROOT / "build/indexed_command_source_alias_fields"
MEMBERS = frozenset(("fields.json", "fields.schema.json", "validation.json", "manifest.json"))
LAYOUT_ID = reference_value(__name__, 'LAYOUT_ID')
LAYOUT_MANIFEST_SHA = reference_value(__name__, 'LAYOUT_MANIFEST_SHA')
OLD_CORE_SHA = reference_value(__name__, 'OLD_CORE_SHA')
BANK_SHA = {
    "m68k_bank00.s": reference_value(__name__, 'BANK_SHA'),
    "m68k_bank01.s": reference_value(__name__, 'BANK_SHA_2'),
    "m68k_bank02.s": reference_value(__name__, 'BANK_SHA_3'),
    "m68k_bank03.s": reference_value(__name__, 'BANK_SHA_4'),
    "m68k_bank04.s": reference_value(__name__, 'BANK_SHA_5'),
    "m68k_bank05.s": reference_value(__name__, 'BANK_SHA_6'),
    "m68k_bank06.s": reference_value(__name__, 'BANK_SHA_7'),
    "m68k_bank07.s": reference_value(__name__, 'BANK_SHA_8'),
    "m68k_bank08.s": reference_value(__name__, 'BANK_SHA_9'),
    "m68k_bank09.s": reference_value(__name__, 'BANK_SHA_10'),
    "m68k_bank0a.s": reference_value(__name__, 'BANK_SHA_11'),
    "m68k_bank0b.s": reference_value(__name__, 'BANK_SHA_12'),
    "m68k_bank0c.s": reference_value(__name__, 'BANK_SHA_13'),
    "m68k_bank0d.s": reference_value(__name__, 'BANK_SHA_14'),
    "m68k_bank0e.s": reference_value(__name__, 'BANK_SHA_15'),
    "m68k_bank0f.s": reference_value(__name__, 'BANK_SHA_16'),
}
SPANS = (
    (0x2A260, 0x2A26C), (0x2A294, 0x2A29A), (0x2A4A4, 0x2A4A6), (0x2A576, 0x2A5A0),
    (0x2AA5A, 0x2AA60), (0x31238, 0x3123C), (0x31278, 0x3127C), (0x312B8, 0x312BC),
    (0x31D94, 0x31D9E), (0x32660, 0x32662), (0x32670, 0x32672), (0x32680, 0x32682),
    (0x32690, 0x32692), (0x326A0, 0x326A2), (0x326B0, 0x326B2), (0x326C0, 0x326C2),
    (0x326D0, 0x326D2), (0x326E0, 0x326E2), (0x326F0, 0x326F2), (0x32700, 0x32702),
    (0x32710, 0x32712), (0x32720, 0x32722), (0x32730, 0x32732), (0x3321A, 0x3324C),
    (0x33764, 0x33770), (0x33D6C, 0x33D7C), (0x3563E, 0x35644), (0x35899, 0x3589A),
    (0x35947, 0x35948), (0x359E9, 0x359EA), (0x35A97, 0x35A98), (0x35B45, 0x35B46),
    (0x35BE7, 0x35BE8), (0x35C89, 0x35C8A), (0x35D03, 0x35D04), (0x35D85, 0x35D86),
    (0x35E07, 0x35E08), (0x35E81, 0x35E82), (0x35EFB, 0x35EFC), (0x35F75, 0x35F76),
    (0x35FF3, 0x35FF4), (0x36071, 0x36072), (0x360EB, 0x360EC), (0x3618D, 0x3618E),
    (0x3622F, 0x36230), (0x362D1, 0x362D2), (0x36373, 0x36374), (0x36415, 0x36416),
    (0x364B7, 0x364B8), (0x36559, 0x3655A), (0x365FB, 0x365FC), (0x3669D, 0x3669E),
    (0x3670F, 0x36710), (0x36781, 0x36782), (0x367F3, 0x367F4), (0x36865, 0x36866),
    (0x368D7, 0x368D8), (0x36949, 0x3694A), (0x369F7, 0x369F8), (0x36AA9, 0x36AAA),
    (0x36B5B, 0x36B5C), (0x36C0D, 0x36C0E), (0x36CB3, 0x36CB4), (0x36D59, 0x36D5A),
    (0x36DFF, 0x36E00), (0x36EA5, 0x36EA6), (0x36F47, 0x36F48), (0x36FE9, 0x36FEA),
    (0x37117, 0x37118), (0x37151, 0x37152), (0x3715B, 0x3715C), (0x371FD, 0x371FE),
    (0x3729F, 0x372A0), (0x372C1, 0x372C2), (0x37323, 0x37324), (0x37329, 0x3732A),
    (0x3732F, 0x37330), (0x37335, 0x37336), (0x3734F, 0x37350), (0x37369, 0x3736A),
    (0x37383, 0x37384), (0x374C5, 0x374C6), (0x374FB, 0x374FC), (0x37529, 0x3752A),
    (0x37583, 0x37584), (0x375ED, 0x375EE), (0x3761F, 0x37620), (0x376D5, 0x376D6),
    (0x37777, 0x37778), (0x377A9, 0x377AA), (0x3786F, 0x37870), (0x3792D, 0x3792E),
    (0x37957, 0x37958), (0x3798D, 0x3798E), (0x379BB, 0x379BC), (0x37A5D, 0x37A5E),
    (0x37B47, 0x37B48), (0x37C2D, 0x37C2E), (0x37D17, 0x37D18), (0x37DFD, 0x37DFE),
    (0x37EA7, 0x37EA8), (0x37F51, 0x37F52), (0x37F7B, 0x37F7C), (0x37FA5, 0x37FA6),
    (0x38047, 0x38048), (0x380ED, 0x380EE), (0x3810F, 0x38110), (0x381B1, 0x381B2),
    (0x38283, 0x38284), (0x382D5, 0x382D6), (0x38383, 0x38384), (0x38445, 0x38446),
    (0x384E7, 0x384E8), (0x3852D, 0x3852E), (0x385CF, 0x385D0), (0x385D9, 0x385DA),
    (0x38673, 0x38674), (0x386F9, 0x386FA), (0x38717, 0x38718), (0x387B9, 0x387BA),
    (0x38AF7, 0x38AF8), (0x38AFD, 0x38B00), (0x38B41, 0x38B42), (0x38B6B, 0x38B6C),
    (0x38F18, 0x38F38), (0x39198, 0x391D8), (0x39852, 0x39854), (0x39990, 0x39994),
    (0x39B08, 0x39B10), (0x39BB4, 0x39BC0), (0x39C14, 0x39C1C), (0x39C44, 0x39C4C),
    (0x39CEC, 0x39CF0), (0x39D6A, 0x39D7A), (0x39E1E, 0x39E26), (0x39F10, 0x39F18),
    (0x3A068, 0x3A06A), (0x3A1D8, 0x3A1E0), (0x3A432, 0x3A43E), (0x3A482, 0x3A48A),
    (0x3A4C6, 0x3A4CE), (0x3A50A, 0x3A512), (0x3A532, 0x3A536), (0x3A748, 0x3A74E),
    (0x3AA36, 0x3AA38), (0x3AC34, 0x3AC3C), (0x3B2AA, 0x3B2B0), (0x3B35C, 0x3B36C),
    (0x3B600, 0x3B614), (0x3BB04, 0x3BB10), (0x3BC6B, 0x3BC6C), (0x3BCCD, 0x3BCCE),
    (0x3BD2F, 0x3BD30), (0x3BD91, 0x3BD92), (0x3BDF3, 0x3BDF4), (0x3BE55, 0x3BE56),
    (0x3BEB7, 0x3BEB8), (0x3BF19, 0x3BF1A), (0x3BF7B, 0x3BF7C), (0x3BFBD, 0x3BFBE),
    (0x3BFFF, 0x3C000), (0x3C041, 0x3C042), (0x3C08F, 0x3C192), (0x3C725, 0x3C726),
    (0x3C72F, 0x3C730), (0x3C73D, 0x3C73E), (0x3C777, 0x3C778), (0x3C7B1, 0x3C7B2),
    (0x3C7EB, 0x3C7EC), (0x3C825, 0x3C826), (0x3C85F, 0x3C860), (0x3C899, 0x3C89A),
    (0x3C8AB, 0x3C8AC), (0x3C8B9, 0x3C8BA), (0x3C8C3, 0x3C8C4), (0x3C905, 0x3C906),
    (0x3C96F, 0x3C970), (0x3CEB9, 0x3CEBA), (0x3CF2F, 0x3CF30), (0x3CFA5, 0x3CFA6),
    (0x3D017, 0x3D018), (0x3D0A9, 0x3D0AA), (0x3D0C3, 0x3D0C4), (0x3D0DD, 0x3D0DE),
    (0x3D0F7, 0x3D0F8), (0x3D171, 0x3D172), (0x3D4CD, 0x3D4CE), (0x3D507, 0x3D508),
    (0x3D58D, 0x3D58E), (0x3D613, 0x3D614), (0x3D621, 0x3D622), (0x3D633, 0x3D634),
    (0x3D645, 0x3D646), (0x3D653, 0x3D654), (0x3D76E, 0x3D7DA), (0x3E082, 0x3E086),
    (0x3E297, 0x3E298), (0x3E38E, 0x3E396), (0x3E3DF, 0x3E42A), (0x3F16A, 0x3F172),
    (0x3F1C4, 0x3F1CC), (0x3F60B, 0x3F60C), (0x3F613, 0x3F614), (0x3F61B, 0x3F61C),
    (0x3F840, 0x3F844), (0x3FFA6, 0x3FFAA), (0x40959, 0x4095A), (0x4095F, 0x40960),
    (0x40965, 0x40966), (0x4096B, 0x4096C), (0x40971, 0x40972), (0x40977, 0x40978),
    (0x4097D, 0x4097E), (0x40983, 0x40984), (0x40989, 0x4098A), (0x4098F, 0x40990),
    (0x40995, 0x40996), (0x4099B, 0x4099C), (0x409A1, 0x409A2), (0x409A7, 0x409A8),
    (0x409AD, 0x409AE), (0x409B3, 0x409B4), (0x409B9, 0x409BA), (0x409BF, 0x409C0),
    (0x409C5, 0x409C6), (0x409CB, 0x409CC), (0x409D1, 0x409D2), (0x409D7, 0x409D8),
    (0x409DD, 0x409DE), (0x409E3, 0x409E4), (0x409E9, 0x409EA), (0x409EF, 0x409F0),
    (0x409F5, 0x409F6), (0x409FB, 0x409FC), (0x40A01, 0x40A02), (0x40A07, 0x40A08),
    (0x40A0D, 0x40A0E), (0x40A13, 0x40A14), (0x40A19, 0x40A1A), (0x40A1F, 0x40A20),
    (0x40A25, 0x40A26), (0x40A2B, 0x40A2C), (0x40A31, 0x40A32), (0x40A37, 0x40A38),
    (0x40A3D, 0x40A3E), (0x40A43, 0x40A44), (0x40A49, 0x40A4A), (0x40A4F, 0x40A50),
    (0x40A55, 0x40A56), (0x40A5B, 0x40A5C), (0x40A61, 0x40A62), (0x40A67, 0x40A68),
    (0x40A6D, 0x40A6E), (0x40A73, 0x40A74), (0x40A79, 0x40A7A), (0x40A7F, 0x40A80),
    (0x40A85, 0x40A86), (0x40A8B, 0x40A8C), (0x40A91, 0x40A92), (0x40A97, 0x40A98),
    (0x40A9D, 0x40A9E), (0x40AA3, 0x40AA4), (0x40AAD, 0x40AAE), (0x40AB7, 0x40AB8),
    (0x40AC1, 0x40AC2), (0x40ACB, 0x40ACC), (0x40AD5, 0x40AD6), (0x40ADF, 0x40AE0),
    (0x40AE9, 0x40AEA), (0x40AF3, 0x40AF4), (0x40AF9, 0x40AFA), (0x40AFF, 0x40B00),
    (0x40B05, 0x40B06), (0x40B0B, 0x40B0C), (0x40B11, 0x40B12), (0x40B17, 0x40B18),
    (0x40B1D, 0x40B1E), (0x40B23, 0x40B24), (0x40B29, 0x40B2A), (0x40B2F, 0x40B30),
    (0x40B35, 0x40B36), (0x40B3B, 0x40B3C), (0x40B41, 0x40B42), (0x40B47, 0x40B48),
    (0x40B4D, 0x40B4E), (0x40B53, 0x40B54), (0x40B59, 0x40B5A), (0x40B5F, 0x40B60),
    (0x40B65, 0x40B66), (0x40B6B, 0x40B6C), (0x40B71, 0x40B72), (0x40B77, 0x40B78),
    (0x40B7D, 0x40B7E), (0x40B83, 0x40B84), (0x40B89, 0x40B8A), (0x40B8F, 0x40B90),
    (0x40B95, 0x40B96), (0x40B9B, 0x40B9C), (0x40BA1, 0x40BA2), (0x40BA7, 0x40BA8),
    (0x40BAD, 0x40BAE), (0x40BB3, 0x40BB4), (0x40BB9, 0x40BBA), (0x40BBF, 0x40BC0),
    (0x40BC5, 0x40BC6), (0x40BCB, 0x40BCC), (0x40BD1, 0x40BD2), (0x40BD7, 0x40BD8),
    (0x40BDD, 0x40BDE), (0x40BE3, 0x40BE4), (0x40BE9, 0x40BEA), (0x40BEF, 0x40BF0),
    (0x40BF5, 0x40BF6), (0x40BFB, 0x40BFC), (0x40C01, 0x40C02), (0x40C07, 0x40C08),
    (0x40C0D, 0x40C0E), (0x40C13, 0x40C14), (0x40C19, 0x40C1A), (0x40C1F, 0x40C20),
    (0x40C25, 0x40C26), (0x40C2B, 0x40C2C), (0x40C31, 0x40C32), (0x40C37, 0x40C38),
    (0x40C3D, 0x40C3E), (0x40C43, 0x40C44), (0x40C4D, 0x40C4E), (0x40C57, 0x40C58),
    (0x40C61, 0x40C62), (0x40C6B, 0x40C6C), (0x40C75, 0x40C76), (0x40C7F, 0x40C80),
    (0x40C89, 0x40C8A), (0x40C93, 0x40C94), (0x415E7, 0x415E8), (0x417E3, 0x417E4),
    (0x417E9, 0x417EA), (0x417EF, 0x417F0), (0x417F5, 0x417F6), (0x41F02, 0x41F03),
    (0x41FEC, 0x41FF0), (0x473E3, 0x473E4), (0x492E7, 0x492E8),
)
# One descriptor per complete original producer/read prefix. Secondary readers
# use their own real PC; WORD-pair +2 is applied after signed EA formation.
READERS = tuple(dict(
    id=f"dispatch_{read:06X}", role="conditional_callback_offset_WORD",
    base=start, first_read_PC=read, second_read_PC=None, shift=1,
    fetch_PC=fetch, RAM_address=0xFFFF0000 | ram, BMI_before_SUBQ1=subtract,
    next_PC=call, next_kind="indexed_JSR_not_executed",
    callback_base=end,
) for start, end, read, call, fetch, ram, subtract in original.DISPATCH) + (
    dict(id="parameter_03B758", role="conditional_scalar_parameter_WORD",
         base=0x3B788, first_read_PC=0x3B758, second_read_PC=None, shift=1,
         fetch_PC=0x3B752, RAM_address=0xFFFF80DA, BMI_before_SUBQ1=False,
         next_PC=0x3B75C, next_kind="808A_JSR_not_executed"),
    dict(id="pair_03FCBA", role="conditional_parameter_WORD_pair",
         base=0x3FCC4, first_read_PC=0x3FCBA, second_read_PC=0x3FCBE, shift=2,
         fetch_PC=0x3FC9A, RAM_address=0xFFFF8132, BMI_before_SUBQ1=False,
         next_PC=0x3FCC2, next_kind="RTS_not_executed",
         alternate_RAM_address=0xFFFF812A, RAM_selection_PC=0x3FCAC),
    dict(id="pair_0415B0", role="conditional_parameter_WORD_pair",
         base=0x415E8, first_read_PC=0x415B0, second_read_PC=0x415B4, shift=2,
         fetch_PC=0x415AA, RAM_address=0xFFFF8158, BMI_before_SUBQ1=False,
         next_PC=0x415B8, next_kind="411A2_BSR_not_executed"),
    dict(id="pair_041616", role="conditional_parameter_WORD_pair_second_reader",
         base=0x415E8, first_read_PC=0x41616, second_read_PC=0x4161A, shift=2,
         fetch_PC=0x41610, RAM_address=0xFFFF8158, BMI_before_SUBQ1=False,
         next_PC=0x4161E, next_kind="411A2_BSR_not_executed"),
)


def flags():
    return dict(CPU_executed=False, hardware_executed=False,
                true_call_RTS_executed=False, callback_executed=False,
                independent_CPU_comparison=False, complete_entry=False,
                natural_domain_complete=False)


def metadata():
    return dict(format=FORMAT,
                canonical_source=dict(size=f.ROM_SIZE, sha256=f.ROM_SHA),
                confidence="confirmed_conditional_source_reads_unknown_original_business_role",
                owner_bytes_added=0, natural_domains_added=0, complete_domains_added=0,
                executable_code_added=0, recovered_functions_added=0,
                unique_physical_source_authority=True,
                physical_catalog_is_CPU_clamp=False,
                raw_authority_snapshot=dict(layout_id=LAYOUT_ID,
                    manifest_sha256=LAYOUT_MANIFEST_SHA, resources=87,
                    raw_BYTES=42494, new_BYTES=EDITABLE_BYTES),
                producer_dependency=dict(path="tools/indexed_command_source_fields/codec.py",
                    sha256=OLD_CORE_SHA, original_instruction_guards_reused_not_emitted=True))


def verify_rom(rom):
    if type(rom) is not bytes:
        raise ValueError("immutable canonical ROM bytes required")
    original.verify_rom(rom)
    if sha(Path(original.__file__).read_bytes()) != OLD_CORE_SHA:
        raise ValueError("frozen original producer dependency differs")


def reader_by_id(reader_id):
    if type(reader_id) is not str:
        raise ValueError("one exact original reader ID required")
    matches = [row for row in READERS if row["id"] == reader_id]
    if len(matches) != 1:
        raise ValueError("unknown original reader ID")
    return matches[0]


def shifted_WORD(row, selector_WORD):
    value = f.uint(selector_WORD, 65535, "complete supplied original selector WORD")
    if row["BMI_before_SUBQ1"] and value & 32768:
        return None
    if row["BMI_before_SUBQ1"]:
        value = (value - 1) & 65535
    return (value << row["shift"]) & 65535


def source_unions():
    # Both halves of a WORD-pair complete before the next original instruction.
    return sorted(set((row["base"] - 32768, row["base"] + 32768)
                      for row in READERS))


def witness(address):
    f.uint(address, f.ROM_SIZE - 1, "physical new source BYTE")
    for row in READERS:
        base = row["base"]
        if base - 32768 <= address < base + 32768:
            window = address - ((address - base) % (1 << row["shift"]))
            if row["second_read_PC"] is not None and address - window >= 2:
                word_address, read_pc = window + 2, row["second_read_PC"]
            else:
                word_address, read_pc = window, row["first_read_PC"]
            selector = ((window - base) & 65535) >> row["shift"]
            if row["BMI_before_SUBQ1"]:
                selector = (selector + 1) & 32767
            return dict(reader_id=row["id"], selector_WORD=selector,
                        original_read_PC=read_pc, source_WORD_address=word_address,
                        byte_index=address - word_address)
    raise ValueError("source BYTE lacks an original producer/read witness")


def span_topology(span):
    start, end = span
    return dict(id=f"rom_{start:06X}_{end:06X}_command_source_alias",
                start=start, end=end,
                role="conditional_original_WORD_read_BYTEs_business_or_code_role_unknown")


def byte_topology(address):
    return dict(id=f"rom_{address:06X}_command_source_BYTE",
                address=address, **witness(address))


def extract(rom):
    verify_rom(rom)
    return dict(**metadata(), fragments=[
        dict(**span_topology(span),
             bytes=[dict(**byte_topology(address), value=rom[address])
                    for address in range(*span)])
        for span in SPANS])


def fixed(value, expected, mutable, label):
    f.keys(value, set(expected) | set(mutable), label)
    for key, item in expected.items():
        f.same(value[key], item, label + "." + key)


def blocks(rom, fields):
    verify_rom(rom)
    fixed(fields, metadata(), {"fragments"}, "command-source alias package")
    rows = fields["fragments"]
    if type(rows) is not list or len(rows) != len(SPANS):
        raise ValueError("fixed 343 physical source fragments required")
    encoded = []
    for row, span in zip(rows, SPANS):
        fixed(row, span_topology(span), {"bytes"}, "source fragment")
        values = row["bytes"]
        if type(values) is not list or len(values) != span[1] - span[0]:
            raise ValueError("fixed physical BYTE count differs")
        data = bytearray()
        for item, address in zip(values, range(*span)):
            fixed(item, byte_topology(address), {"value"}, "original witnessed source BYTE")
            data.append(f.uint(item["value"], 255, "complete editable source BYTE"))
        encoded.append(dict(id=row["id"], start=span[0], end=span[1],
                            data=bytes(data), role=row["role"]))
    if sum(len(row["data"]) for row in encoded) != EDITABLE_BYTES:
        raise ValueError("fixed 1260-BYTE source cost differs")
    if any(a["end"] > b["start"] for a, b in zip(encoded, encoded[1:])):
        raise ValueError("physical source fragment overlap")
    return encoded


def rebuild(rom, fields):
    image = bytearray(rom)
    for row in blocks(rom, fields):
        image[row["start"]:row["end"]] = row["data"]
    return bytes(image)


def projected_event(kind, pc, logical, size, value):
    return dict(kind=kind, pc=pc, logical_address=logical & 0xFFFFFFFF,
                address=logical & 0xFFFFFF, size=size, value=value)


def prefix_view(image, reader_id, selector_WORD, *, F8144_WORD=0):
    """Original ordered source prefix only; no callback/stack/helper execution.

    F8144 is used only for the original 3FCA8 selected-A0 caller. This supplies
    the actual selector/read inputs, not an invented generic RAM address.
    """
    if type(image) is not bytes or len(image) != f.ROM_SIZE:
        raise ValueError("complete immutable edited image required")
    f.uint(F8144_WORD, 65535, "complete original A0-selection WORD")
    row = reader_by_id(reader_id)
    index = shifted_WORD(row, selector_WORD)
    events = []
    ram = row["RAM_address"]
    if "alternate_RAM_address" in row:
        events.append(projected_event("supplied_RAM_read_projection",
            row["RAM_selection_PC"], 0xFFFF8144, 2, F8144_WORD))
        if F8144_WORD:
            ram = row["alternate_RAM_address"]
    elif F8144_WORD:
        raise ValueError("A0-selection input applies only to original 3FCA8 caller")
    events.append(projected_event("supplied_RAM_read_projection",
        row["fetch_PC"], ram, 2, selector_WORD))
    result = dict(**flags(), reader_id=reader_id, selector_WORD=selector_WORD,
                  events=events, supplied_input_is_natural_domain=False)
    if index is None:
        return dict(**result, status="original_BMI_return_boundary",
                    source_read_performed=False)
    signed = original.signed_WORD(index)
    values = []
    for base, pc in ((row["base"], row["first_read_PC"]),
                     (row["base"] + 2, row["second_read_PC"])):
        if pc is None:
            continue
        logical = (base + signed) & 0xFFFFFFFF
        address = logical & 0xFFFFFF
        if logical & 1:
            return dict(**result, status="odd_WORD_source_boundary",
                        shifted_index_WORD=index, boundary_address=logical)
        if address + 2 > len(image):
            return dict(**result, status="unmapped_source_boundary",
                        shifted_index_WORD=index, boundary_address=logical)
        value = int.from_bytes(image[address:address + 2], "big")
        values.append(value)
        events.append(projected_event("source_read_projection", pc, logical, 2, value))
    result.update(shifted_index_WORD=index, signed_index=signed,
                  source_WORDs=values, source_read_performed=True,
                  next_original_PC=row["next_PC"])
    if "callback_base" in row:
        target = (row["callback_base"] + original.signed_WORD(values[0])) & 0xFFFFFFFF
        result.update(callback_target_LONG=target, callback_target_bus=target & 0xFFFFFF,
                      callback_target_is_odd=bool(target & 1))
    return dict(**result, status=row["next_kind"])


def preview(rom, fields, reader_id, selector_WORD, **kwargs):
    return prefix_view(rebuild(rom, fields), reader_id, selector_WORD, **kwargs)


def raw_guard(base):
    raw = d.raw_positions(base)
    actual = {address for address in raw
              if 0x10000 <= address < 0x60000
              and any(start <= address < end for start, end in source_unions())}
    expected = {address for span in SPANS for address in range(*span)}
    if len(raw) != 42494 or actual != expected:
        raise ValueError("fixed87 raw-only source authority intersection differs")
    return dict(guarded_raw_BYTES=len(expected), physical_blocks=len(SPANS),
                snapshot_raw_BYTES=len(raw), old_typed_overlap_BYTES=0,
                outside_10000_60000_BYTES=0)


def guard_snapshot():
    path = ROOT / "build/direct_code/layout" / LAYOUT_ID
    if sha(f.read_bounded(path / "manifest.json", f.MAX_JSON)) != LAYOUT_MANIFEST_SHA:
        raise ValueError("fixed87 manifest authority differs")
    base = {}
    for name, expected in BANK_SHA.items():
        data = f.read_bounded(path / name, f.MAX_JSON)
        if sha(data) != expected:
            raise ValueError("fixed87 raw bank differs: " + name)
        base[name] = data
    return raw_guard(base)


def schema():
    def obj(properties):
        return dict(type="object", properties=properties, required=list(properties),
                    additionalProperties=False)
    def pinned(value):
        if type(value) is dict:
            return obj({key: pinned(item) for key, item in value.items()})
        if type(value) is list:
            return dict(type="array", prefixItems=[pinned(item) for item in value],
                        items=False, minItems=len(value), maxItems=len(value))
        return dict(type={str: "string", int: "integer", bool: "boolean"}[type(value)], const=value)
    rows = []
    for span in SPANS:
        bytes_schema = [obj({**{key: pinned(value) for key, value in byte_topology(address).items()},
            "value": dict(type="integer", minimum=0, maximum=255)})
            for address in range(*span)]
        rows.append(obj({**{key: pinned(value) for key, value in span_topology(span).items()},
            "bytes": dict(type="array", prefixItems=bytes_schema, items=False,
                          minItems=len(bytes_schema), maxItems=len(bytes_schema))}))
    result = obj({**{key: pinned(value) for key, value in metadata().items()},
        "fragments": dict(type="array", prefixItems=rows, items=False,
                          minItems=len(rows), maxItems=len(rows))})
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["description"] = "1260 complete conditional source BYTEs; immutable original input/read witnesses."
    return result


def render_bundle(rom):
    fields = extract(rom)
    image = rebuild(rom, load_fields(dump(fields)))
    if image != rom:
        raise ValueError("serialized whole-ROM roundtrip differs")
    proofs = []
    for span in SPANS:
        for address in range(*span):
            item = witness(address)
            view = prefix_view(image, item["reader_id"], item["selector_WORD"])
            event = next(event for event in view["events"]
                         if event["kind"] == "source_read_projection"
                         and event["pc"] == item["original_read_PC"])
            if (event["address"] != item["source_WORD_address"]
                or event["value"].to_bytes(2, "big")[item["byte_index"]] != image[address]):
                raise ValueError("per-BYTE original producer/read witness differs")
            proofs.append(dict(address=address, original_BYTE=image[address], **item))
    reader_counts = []
    for row in READERS:
        inputs = range(32768) if row["BMI_before_SUBQ1"] else range(65536)
        indices = {shifted_WORD(row, value) for value in inputs}
        expected = 32768 if row["shift"] == 1 else 16384
        if len(indices) != expected:
            raise ValueError("original guarded WORD-index domain differs")
        reader_counts.append(dict(**row, supplied_WORD_inputs=len(inputs),
            distinct_shifted_WORD_indices=len(indices),
            conditional_source_union=[row["base"] - 32768, row["base"] + 32768],
            natural_domain_complete=False))
    report = dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        physical_blocks=len(SPANS), whole_ROM_exact=True, whole_ROM_sha256=sha(image),
        **flags(), raw_guard=guard_snapshot(), every_new_BYTE_witness_count=len(proofs),
        new_BYTE_witnesses=proofs, original_producer_readers=reader_counts,
        guarded_original_code=[dict(start=start, end=end, sha256=digest, physical_emit=False)
                               for start, end, digest in original.GUARDS],
        source_unions=source_unions(), physical_source_low=SPANS[0][0],
        physical_source_high=SPANS[-1][1],
        original_guarded_prefix_examples=[prefix_view(image, "dispatch_034F70", value)
            for value in (0, 1, 0x4000, 0x4001, 0x7FFF, 0x8000, 0xFFFF)],
        limitations=[
            "These are source-consumption aliases, not recovered executable code, complete functions or natural callback domains.",
            "Six F728 producers preserve the original BMI before SUBQ.W1 and LSL.W1. Zero performs its prior-source read; high-bit selectors stop first.",
            "The 32768 accepted F728 WORDs still form every even low-WORD index after SUBQ1/LSL1; this is a constructed domain, not proven natural selection.",
            "All source WORDs retain both BYTEs and signed callback interpretation. Old typed neighbors are read live but emitted only by their old author.",
            "Parameter pairs shift in WORD then sign-extend; the second independent PC base adds2 after signed EA, not another wrapped selector.",
            "3FC96 caller selects actual A0=8132 or812A through live8144 before its source WORD fetch; neither the callback nor true RTS/stack is simulated.",
            "415A2 has earlier live reads/stack effects not modeled here; this diagnostic proves its supplied8158 source prefix only.",
            "Every new physical BYTE has a fixed original-input/read-PC witness and one fullbits editable authority, never a gaphex or zero-padding claim.",
            "The larger05CE22..05D5E4 and0246EE..024806 gaps have no witness from these readers and remain unknown."
        ])
    members = {"fields.json": dump(fields), "fields.schema.json": dump(schema()),
               "validation.json": dump(report)}
    members["manifest.json"] = dump(dict(**metadata(), editable_bytes=EDITABLE_BYTES,
        physical_blocks=len(SPANS),
        members={name: dict(bytes=len(data), sha256=sha(data)) for name, data in members.items()}))
    return members


def fresh_output(value, *, bundle=False):
    path = f.safe_path(value)
    if not (path != OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path == FORMAL_ROOT):
        raise ValueError("fresh dedicated build output or exact formal bundle required")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("fresh output with existing parent required")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("export", "import", "verify"))
    parser.add_argument("--rom", default=str(f.DEFAULT_ROM))
    parser.add_argument("--fields")
    parser.add_argument("--bundle")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    target = None
    if args.command == "export":
        if args.output is None or args.fields is not None or args.bundle is not None:
            raise ValueError("export requires only fresh output")
        target = fresh_output(args.output, bundle=True)
    elif args.command == "import":
        if args.output is None or args.bundle is not None:
            raise ValueError("import requires fields and fresh output")
        target = fresh_output(args.output)
        if target.suffix.lower() != ".bin":
            raise ValueError("fresh .bin output required")
    elif args.output is not None or (args.fields is not None and args.bundle is not None):
        raise ValueError("verify accepts fields or bundle, without output")
    rom = f.read_bounded(args.rom, f.ROM_SIZE)
    if args.command == "export":
        members = render_bundle(rom)
        target.mkdir()
        for name, data in members.items():
            f.put(target / name, data)
        result = dict(path=str(target), editable_bytes=EDITABLE_BYTES,
                      members={name: sha(data) for name, data in members.items()})
    elif args.command == "verify" and args.bundle is not None:
        bundle = f.safe_path(args.bundle)
        if not bundle.is_dir() or {path.name for path in bundle.iterdir()} != MEMBERS:
            raise ValueError("exact four-member canonical bundle required")
        for name, data in render_bundle(rom).items():
            if f.read_bounded(bundle / name, f.MAX_JSON) != data:
                raise ValueError("canonical formal member drift: " + name)
        result = dict(path=str(bundle), verified=True, editable_bytes=EDITABLE_BYTES,
                      whole_ROM_exact=True, sha256=sha(rom))
    else:
        fields = load_fields(f.read_bounded(args.fields or DEFAULT_FIELDS, f.MAX_JSON))
        image = rebuild(rom, fields)
        if target is not None:
            f.put(target, image)
        result = dict(path=None if target is None else str(target), bytes=len(image),
                      editable_bytes=EDITABLE_BYTES, exact_canonical=image == rom, sha256=sha(image))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
