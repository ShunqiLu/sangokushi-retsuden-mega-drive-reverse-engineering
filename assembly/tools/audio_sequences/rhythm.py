"""Typed embedded rhythm definitions and FM voices for canonical G-5510.

All Z80 addresses here are below 1000 and map through primary-copy origin
ROM 0069D2, not the secondary-copy/local-SFX origin 00699C.

These structures describe potential rhythm resources. A mask observed by a
static sequence walker can select a subset, conditional on the driver override
flag. Neither extraction nor ranges() says that all potential resources played.
"""
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
import struct
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "audio_formats"))
import audio_formats as audio


PRIMARY_ORIGIN = 0x69D2
FM_DESCRIPTOR_POINTERS = (0x0A80, 0x0AA2, 0x0AAE, 0x0AB7, 0x0ACB,
                          0x0AED, 0x0AC2, 0x0B0F, 0x0B34, 0x0B56)
PSG_DESCRIPTOR_POINTERS = (0x0A4A, 0x0A55)
VOICE_POINTERS = (0x0A89, 0x0AD4, 0x0AF6, 0x0B1B, 0x0B3D, 0x0B5F)
FM_SEQUENCE_POINTERS = (0x0A86, 0x0AA8, 0x0AB4, 0x0ABD, 0x0AD1,
                        0x0AF3, 0x0AC8, 0x0B15, 0x0B3A, 0x0B5C)
PSG_SEQUENCE_POINTERS = (0x0A50, 0x0A5B)
TABLES = (("psg_descriptors", 0x0A46, PSG_DESCRIPTOR_POINTERS),
          ("fm_descriptors", 0x0A60, FM_DESCRIPTOR_POINTERS),
          ("fm_voices", 0x0A74, VOICE_POINTERS))
PROVENANCE = {
    "layout_status": "confirmed",
    "selection_status": "not_evaluated_here",
    "allocation_status": "probable",
    "natural_playback_status": "unknown",
    "evidence": "Z80 098F-0A33 rhythm consumer, table pointers, 06C9 state initializer, 04E5/0D8A 25-byte voice consumer",
    "scope": "Potential descriptor/voice resources; selected subset requires explicit rhythm-mask evidence and override-bit condition",
}


def _address(z80: int) -> int:
    if type(z80) is not int or not 0 <= z80 < 0x1000:
        raise ValueError("rhythm address must be a primary-copy Z80 integer below 1000")
    return PRIMARY_ORIGIN + z80


def extract(rom: bytes) -> dict[str, Any]:
    """Return editable, lossless fields separately from canonical provenance."""
    audio.verify_rom(rom)
    tables = []
    for label, address, pointers in TABLES:
        actual = struct.unpack_from("<" + "H" * len(pointers), rom, _address(address))
        if actual != pointers:
            raise ValueError("rhythm pointer-table signature differs")
        tables.append({"id": label, "z80_address": address, "rom_offset": _address(address),
                       "pointers": list(actual)})
    headers = []
    for family, address in (("fm", 0x0A36), ("psg", 0x0A39)):
        flags, channel_id, multiplier = rom[_address(address):_address(address) + 3]
        headers.append({"family": family, "z80_address": address, "rom_offset": _address(address),
                        "flags": flags, "channel_id": channel_id, "duration_multiplier": multiplier})
    descriptors = []
    for family, pointers, sequences in (("fm", FM_DESCRIPTOR_POINTERS, FM_SEQUENCE_POINTERS),
                                        ("psg", PSG_DESCRIPTOR_POINTERS, PSG_SEQUENCE_POINTERS)):
        for index, (address, expected_sequence) in enumerate(zip(pointers, sequences), 1):
            sequence, transpose, attenuation, modulation, selector = struct.unpack_from("<H4B", rom, _address(address))
            if sequence != expected_sequence:
                raise ValueError("rhythm sequence-pointer signature differs")
            descriptors.append({"id": f"rhythm_{family}_{index:02d}", "family": family,
                                "index": index, "z80_address": address, "rom_offset": _address(address),
                                "fields": {"sequence_ptr": sequence, "transpose": transpose,
                                           "attenuation": attenuation, "modulation_selector": modulation,
                                           "voice_index" if family == "fm" else "envelope_selector": selector}})
    voices = [{"id": f"rhythm_voice_{index}", "z80_address": address, "rom_offset": _address(address),
               "fields": audio._record(rom[_address(address):_address(address) + 25], index)}
              for index, address in enumerate(VOICE_POINTERS)]
    return {"schema_version": 1, "format": "g5510-embedded-rhythm-definitions",
            "source": {"size": audio.ROM_SIZE, "sha256": audio.ROM_SHA256},
            "provenance": dict(PROVENANCE), "pointer_tables": tables,
            "channel_headers": headers, "descriptors": descriptors, "voice_records": voices}


def _encoded(rom: bytes, assets: Any) -> list[tuple[int, bytes, str, str]]:
    baseline = extract(rom)
    audio._keys(assets, baseline, "rhythm")
    for key in ("schema_version", "format", "source", "provenance", "pointer_tables"):
        audio._same(assets[key], baseline[key], "rhythm." + key)
    writes = []
    for table in baseline["pointer_tables"]:
        writes.append((table["rom_offset"], struct.pack("<" + "H" * len(table["pointers"]), *table["pointers"]),
                       "rhythm_pointer_table", table["id"]))
    audio._list_shape(assets["channel_headers"], baseline["channel_headers"], "channel_headers")
    for value, ref in zip(assets["channel_headers"], baseline["channel_headers"]):
        audio._keys(value, ref, "channel_header")
        for key in set(ref) - {"duration_multiplier"}:
            audio._same(value[key], ref[key], "channel_header." + key)
        raw = bytes((value["flags"], value["channel_id"],
                     audio._integer(value["duration_multiplier"], 255, "duration_multiplier")))
        writes.append((ref["rom_offset"], raw, "rhythm_channel_header", "rhythm_" + ref["family"] + "_header"))
    audio._list_shape(assets["descriptors"], baseline["descriptors"], "descriptors")
    for value, ref in zip(assets["descriptors"], baseline["descriptors"]):
        audio._keys(value, ref, "descriptor")
        for key in set(ref) - {"fields"}:
            audio._same(value[key], ref[key], "descriptor." + key)
        fields = value["fields"]
        audio._keys(fields, ref["fields"], "descriptor.fields")
        # Sequence relocation/aliasing is owned by the full sequence package,
        # not this fixed embedded-structure importer.
        audio._same(fields["sequence_ptr"], ref["fields"]["sequence_ptr"], "sequence_ptr")
        selector_key = "voice_index" if ref["family"] == "fm" else "envelope_selector"
        selector = audio._integer(fields[selector_key], 5 if ref["family"] == "fm" else 255, selector_key)
        raw = struct.pack("<H4B", fields["sequence_ptr"],
                          audio._integer(fields["transpose"], 255, "transpose"),
                          audio._integer(fields["attenuation"], 255, "attenuation"),
                          audio._integer(fields["modulation_selector"], 255, "modulation_selector"), selector)
        writes.append((ref["rom_offset"], raw, "rhythm_descriptor", ref["id"]))
    audio._list_shape(assets["voice_records"], baseline["voice_records"], "voice_records")
    for value, ref in zip(assets["voice_records"], baseline["voice_records"]):
        audio._keys(value, ref, "voice_record")
        for key in set(ref) - {"fields"}:
            audio._same(value[key], ref[key], "voice_record." + key)
        raw = audio._encode_record(value["fields"], ref["fields"], ref["id"])
        writes.append((ref["rom_offset"], raw, "rhythm_fm_voice_25", ref["id"]))
    writes.sort()
    for previous, current in zip(writes, writes[1:]):
        if previous[0] + len(previous[1]) > current[0]:
            raise ValueError("rhythm structure ranges overlap")
    if any(start < 0 or start + len(raw) > len(rom) for start, raw, _, _ in writes):
        raise ValueError("rhythm structure exceeds ROM")
    return writes


def rebuild(rom: bytes, assets: Any) -> bytes:
    """Rebuild only 264 supported bytes; all stream/other ROM bytes are kept."""
    result = bytearray(rom)
    for start, raw, _, _ in _encoded(rom, assets):
        result[start:start + len(raw)] = raw
    return bytes(result)


def ranges(rom: bytes) -> list[dict[str, Any]]:
    """Potential typed ranges, NOT automatic confirmed-owner declarations."""
    return [{"start": start, "end": start + len(raw), "kind": kind, "label": label,
             "confidence": "probable", "layout_status": "confirmed",
             "selection_status": "not_evaluated_here", "natural_playback_status": "unknown",
             "evidence": PROVENANCE["evidence"]}
            for start, raw, kind, label in _encoded(rom, extract(rom))]


def selection_for_masks(rom: bytes, assets: Any, masks: Iterable[int]) -> dict[str, Any]:
    """Resolve explicit mask inputs against validated (possibly edited) fields.

    The caller supplies static/parser/runtime evidence separately. This models
    resources potentially loaded if the relevant destination bit2 is clear;
    it does not observe that condition and does not claim natural playback.
    """
    _encoded(rom, assets)
    if not isinstance(masks, Iterable) or isinstance(masks, (str, bytes, bytearray, dict)):
        raise ValueError("masks must be an iterable of integer rhythm masks")
    selected = []
    unknown = []
    for ordinal, mask in enumerate(masks):
        if ordinal >= 65536:
            raise ValueError("mask input exceeds the bounded lookup limit")
        if type(mask) is not int or not (mask == 0 or 0x80 <= mask < 0xE0):
            raise ValueError("mask must be initial zero or a non-command rhythm token 80..DF")
        if mask in (0, 0x80):
            continue
        for family, index, maximum in (("fm", mask & 15, 10), ("psg", (mask & 0x70) >> 4, 2)):
            if not index:
                continue
            if index > maximum:
                unknown.append({"input_ordinal": ordinal, "mask": mask, "family": family,
                                "index": index, "status": "unknown", "reason": "index exceeds typed pointer-table prefix"})
                continue
            descriptor = next(d for d in assets["descriptors"] if d["family"] == family and d["index"] == index)
            selected.append({"input_ordinal": ordinal, "mask": mask, "family": family,
                             "descriptor_id": descriptor["id"], "sequence_z80": descriptor["fields"]["sequence_ptr"],
                             "voice_id": f"rhythm_voice_{descriptor['fields']['voice_index']}" if family == "fm" else None,
                             "status": "confirmed", "scope": "conditional resource lookup only",
                             "condition": "corresponding runtime destination flag bit2 is clear",
                             "natural_playback_status": "unknown"})
    return {"scope": "explicit supplied masks; no inferred or natural playback observation",
            "selected": selected, "unknown": unknown}
