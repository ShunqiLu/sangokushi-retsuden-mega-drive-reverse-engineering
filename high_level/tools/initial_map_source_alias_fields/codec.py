"""Live conditional05B6 -> A1B2 initial-map RLE WORD source BYTE aliases.

Only nineteen independently witnessed physical fragments are editable. The
actual init/DMA/VDP prefix and complete WORD producer are executed; source data
remain live. Canonical witnesses stop at odd/unknown bus accesses, never a fake
return. This scoped compatibility reader is not a CPU or semantic game module.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
from functools import lru_cache
import json
from pathlib import Path
import re
from tools.camera_chunk_source_alias_fields import codec as camera
from tools.battle_deployment_parameters import codec as shared

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE=0x100000
ROM_SHA256=camera.ROM_SHA256
DEFAULT_ROM=camera.DEFAULT_ROM
OUTPUT_ROOT=ROOT/'build/initial_map_source_alias_fields'
FORMAL_ROOT=ROOT/'analysis/initial_map_source_alias_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
DEFAULT_BUNDLE=FORMAL_ROOT
FORMAT='g5510-conditional-initial-map-RLE-WORD-source-BYTE-fragment-v1'
EDITABLE_BYTES,PHYSICAL_BLOCKS=19,15
MAX_JSON=8*1024*1024
MEMBERS=camera.MEMBERS
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
SOURCE_SPANS=(
    (0xF41E3, 0xF41E4),
    (0xF41E7, 0xF41E9),
    (0xF4208, 0xF4209),
    (0xF420D, 0xF4210),
    (0xF4212, 0xF4213),
    (0xF4216, 0xF4217),
    (0xF4228, 0xF422A),
    (0xF4237, 0xF4238),
    (0xF423C, 0xF423D),
    (0xF4247, 0xF4248),
    (0xF4256, 0xF4257),
    (0xF4259, 0xF425A),
    (0xF425C, 0xF425D),
    (0xF425F, 0xF4260),
    (0xF4264, 0xF4265),
)
WITNESS_FRAMES=(
    {'F354':64960,'F356':59528},
    {'F354':64960,'F356':59688},
    {'F354':65120,'F356':59520},
)
BODIES=(
    (0x8112,0x812C,reference_value(__name__, 'BODIES')),
    (0x5B6, 0x5BC, reference_value(__name__, 'BODIES_2')),
    (0xA1B2, 0xA332, reference_value(__name__, 'BODIES_3')),
    (0x6826, 0x68A8, reference_value(__name__, 'BODIES_4')),
    (0x68CE, 0x6950, reference_value(__name__, 'BODIES_5')),
    (0xAD1C, 0xAE8A, reference_value(__name__, 'BODIES_6')),
    (0xAF6A,0xB210,reference_value(__name__, 'BODIES_7')),
    (0x1A0,0x1BC,reference_value(__name__, 'BODIES_8')),
)
_INITIAL_INSTRUCTIONS=(
    (0x8112, "43fa0018", "lea.l", "$812c(pc), a1"),
    (0x8116, "e748", "lsl.w", "#$3, d0"),
    (0x8118, "d2c0", "adda.w", "d0, a1"),
    (0x811A, "2459", "movea.l", "(a1)+, a2"),
    (0x811C, "3659", "movea.w", "(a1)+, a3"),
    (0x811E, "3e19", "move.w", "(a1)+, d7"),
    (0x8120, "26da", "move.l", "(a2)+, (a3)+"),
    (0x8122, "51cffffc", "dbra", "d7, $8120"),
    (0x8126, "5278f31e", "addq.w", "#$1, $f31e.w"),
    (0x812A, "4e75", "rts", ""),
    (0x5B6, "4eb90000a1b2", "jsr", "$a1b2.l"),
    (0x6826, "41f900c00004", "lea.l", "$c00004.l, a0"),
    (0x682C, "43f900c00000", "lea.l", "$c00000.l, a1"),
    (0x6832, "45fa0074", "lea.l", "$68a8(pc), a2"),
    (0x6836, "7e12", "moveq", "#$12, d7"),
    (0x6838, "309a", "move.w", "(a2)+, (a0)"),
    (0x683A, "51cffffc", "dbra", "d7, $6838"),
    (0x683E, "31fa006af606", "move.w", "$68aa(pc), $f606.w"),
    (0x6844, "7000", "moveq", "#$0, d0"),
    (0x6846, "23fcc000000000c00004", "move.l", "#$c0000000, $c00004.l"),
    (0x6850, "3e3c003f", "move.w", "#$3f, d7"),
    (0x6854, "3280", "move.w", "d0, (a1)"),
    (0x6856, "51cffffc", "dbra", "d7, $6854"),
    (0x685A, "4df900c00004", "lea.l", "$c00004.l, a6"),
    (0x6860, "3cbc8f01", "move.w", "#$8f01, (a6)"),
    (0x6864, "3e38f606", "move.w", "$f606.w, d7"),
    (0x6868, "00070010", "ori.b", "#$10, d7"),
    (0x686C, "3c87", "move.w", "d7, (a6)"),
    (0x686E, "2cbc93ff94ff", "move.l", "#$93ff94ff, (a6)"),
    (0x6874, "3cbc9780", "move.w", "#$9780, (a6)"),
    (0x6878, "2cbc40000080", "move.l", "#$40000080, (a6)"),
    (0x687E, "33fc000000c00000", "move.w", "#$0, $c00000.l"),
    (0x6886, "3e16", "move.w", "(a6), d7"),
    (0x6888, "02470002", "andi.w", "#$2, d7"),
    (0x688C, "66f8", "bne.b", "$6886"),
    (0x688E, "4a3900ff3f00", "tst.b", "$ff3f00.l"),
    (0x6894, "6608", "bne.b", "$689e"),
    (0x6896, "33fc000000a11100", "move.w", "#$0, $a11100.l"),
    (0x689E, "3cb8f606", "move.w", "$f606.w, (a6)"),
    (0x68A2, "3cbc8f02", "move.w", "#$8f02, (a6)"),
    (0x68A6, "4e75", "rts", ""),
    (0x68CE, "4df900c00004", "lea.l", "$c00004.l, a6"),
    (0x68D4, "3cbc8f01", "move.w", "#$8f01, (a6)"),
    (0x68D8, "3e38f606", "move.w", "$f606.w, d7"),
    (0x68DC, "00070010", "ori.b", "#$10, d7"),
    (0x68E0, "3c87", "move.w", "d7, (a6)"),
    (0x68E2, "2cbc93ff9447", "move.l", "#$93ff9447, (a6)"),
    (0x68E8, "3cbc9780", "move.w", "#$9780, (a6)"),
    (0x68EC, "2cbc78000082", "move.l", "#$78000082, (a6)"),
    (0x68F2, "33fc00f600c00000", "move.w", "#$f6, $c00000.l"),
    (0x68FA, "3e16", "move.w", "(a6), d7"),
    (0x68FC, "02470002", "andi.w", "#$2, d7"),
    (0x6900, "66f8", "bne.b", "$68fa"),
    (0x6902, "4a3900ff3f00", "tst.b", "$ff3f00.l"),
    (0x6908, "6608", "bne.b", "$6912"),
    (0x690A, "33fc000000a11100", "move.w", "#$0, $a11100.l"),
    (0x6912, "3cb8f606", "move.w", "$f606.w, (a6)"),
    (0x6916, "3cbc8f02", "move.w", "#$8f02, (a6)"),
    (0x691A, "23fc4000001000c00004", "move.l", "#$40000010, $c00004.l"),
    (0x6924, "23fc0000000000c00000", "move.l", "#$0, $c00000.l"),
    (0x692E, "21fc00000000f312", "move.l", "#$0, $f312.w"),
    (0x6936, "21fc00000000f316", "move.l", "#$0, $f316.w"),
    (0x693E, "4df8f800", "lea.l", "$f800.w, a6"),
    (0x6942, "7e00", "moveq", "#$0, d7"),
    (0x6944, "3c3c009f", "move.w", "#$9f, d6"),
    (0x6948, "2cc7", "move.l", "d7, (a6)+"),
    (0x694A, "51cefffc", "dbra", "d6, $6948"),
    (0x694E, "4e75", "rts", ""),
    (0xA1B2, "4eb900006826", "jsr", "$6826.l"),
    (0xA1B8, "4278efc8", "clr.w", "$efc8.w"),
    (0xA1BC, "4eb9000068ce", "jsr", "$68ce.l"),
    (0xA1C2, "33fc840700c00004", "move.w", "#$8407, $c00004.l"),
    (0xA1CA, "31f8f356f314", "move.w", "$f356.w, $f314.w"),
    (0xA1D0, "31f8f354f318", "move.w", "$f354.w, $f318.w"),
    (0xA1D6, "23fc4000000000c00004", "move.l", "#$40000000, $c00004.l"),
    (0xA1E0, "41f9000ce61e", "lea.l", "$ce61e.l, a0"),
    (0xA1E6, "43f9000ce49a", "lea.l", "$ce49a.l, a1"),
    (0xA1EC, "3039000d34c2", "move.w", "$d34c2.l, d0"),
    (0xA1F2, "4eb90000adfc", "jsr", "$adfc.l"),
    (0xA1F8, "31fc0001f37e", "move.w", "#$1, $f37e.w"),
    (0xA1FE, "41f9000d34ca", "lea.l", "$d34ca.l, a0"),
    (0xA204, "303c009f", "move.w", "#$9f, d0"),
    (0xA208, "23fc7800000100c00004", "move.l", "#$78000001, $c00004.l"),
    (0xA212, "23d800c00000", "move.l", "(a0)+, $c00000.l"),
    (0xA218, "51c8fff8", "dbra", "d0, $a212"),
    (0xA21C, "4278f322", "clr.w", "$f322.w"),
    (0xA220, "31fc0200f612", "move.w", "#$200, $f612.w"),
    (0xA226, "4240", "clr.w", "d0"),
    (0xA228, "31c0f312", "move.w", "d0, $f312.w"),
    (0xA22C, "31c0f316", "move.w", "d0, $f316.w"),
    (0xA230, "31c0f602", "move.w", "d0, $f602.w"),
    (0xA234, "11fc0002f31c", "move.b", "#$2, $f31c.w"),
    (0xA23A, "7001", "moveq", "#$1, d0"),
    (0xA23C, "4eb900008112", "jsr", "$8112.l"),
    (0xA242, "61000034", "bsr.w", "$a278"),
    (0xA246, "33fc8b0000c00004", "move.w", "#$8b00, $c00004.l"),
    (0xA24E, "4278f6c4", "clr.w", "$f6c4.w"),
    (0xA252, "3038f3a4", "move.w", "$f3a4.w, d0"),
    (0xA256, "02400001", "andi.w", "#$1, d0"),
    (0xA25A, "31c0f3a4", "move.w", "d0, $f3a4.w"),
    (0xA25E, "4eb9000052c2", "jsr", "$52c2.l"),
    (0xA264, "3038f606", "move.w", "$f606.w, d0"),
    (0xA268, "00000040", "ori.b", "#$40, d0"),
    (0xA26C, "33c000c00004", "move.w", "d0, $c00004.l"),
    (0xA272, "46fc2500", "move.w", "#$2500, sr"),
    (0xA276, "4e75", "rts", ""),
    (0xA278, "23fc4000000200c00004", "move.l", "#$40000002, $c00004.l"),
    (0xA282, "41f9000cfae2", "lea.l", "$cfae2.l, a0"),
    (0xA288, "43f9000cfa12", "lea.l", "$cfa12.l, a1"),
    (0xA28E, "3039000d34c4", "move.w", "$d34c4.l, d0"),
    (0xA294, "4eb90000adfc", "jsr", "$adfc.l"),
    (0xA29A, "23fc4000000100c00004", "move.l", "#$40000001, $c00004.l"),
    (0xA2A4, "41f9000d139e", "lea.l", "$d139e.l, a0"),
    (0xA2AA, "43f9000d12f6", "lea.l", "$d12f6.l, a1"),
    (0xA2B0, "3039000d34c8", "move.w", "$d34c8.l, d0"),
    (0xA2B6, "4eb90000adfc", "jsr", "$adfc.l"),
    (0xA2BC, "23fc6000000200c00004", "move.l", "#$60000002, $c00004.l"),
    (0xA2C6, "41f9000d1256", "lea.l", "$d1256.l, a0"),
    (0xA2CC, "3039000d34c6", "move.w", "$d34c6.l, d0"),
    (0xA2D2, "23d800c00000", "move.l", "(a0)+, $c00000.l"),
    (0xA2D8, "51c8fff8", "dbra", "d0, $a2d2"),
    (0xA2DC, "303c001c", "move.w", "#$1c, d0"),
    (0xA2E0, "3878f314", "movea.w", "$f314.w, a4"),
    (0xA2E4, "48e78008", "movem.l", "d0/a4, -(a7)"),
    (0xA2E8, "300c", "move.w", "a4, d0"),
    (0xA2EA, "3238f318", "move.w", "$f318.w, d1"),
    (0xA2EE, "41f90008155a", "lea.l", "$8155a.l, a0"),
    (0xA2F4, "4278f328", "clr.w", "$f328.w"),
    (0xA2F8, "4eb90000af6a", "jsr", "$af6a.l"),
    (0xA2FE, "4eb90000b054", "jsr", "$b054.l"),
    (0xA304, "0040e000", "ori.w", "#$e000, d0"),
    (0xA308, "41f8d000", "lea.l", "$d000.w, a0"),
    (0xA30C, "323c0029", "move.w", "#$29, d1"),
    (0xA310, "30c1", "move.w", "d1, (a0)+"),
    (0xA312, "30c0", "move.w", "d0, (a0)+"),
    (0xA314, "4eb90000b06e", "jsr", "$b06e.l"),
    (0xA31A, "4250", "clr.w", "(a0)"),
    (0xA31C, "41f8d000", "lea.l", "$d000.w, a0"),
    (0xA320, "4eb90000ad1c", "jsr", "$ad1c.l"),
    (0xA326, "4cdf1001", "movem.l", "(a7)+, d0/a4"),
    (0xA32A, "504c", "addq.w", "#$8, a4"),
    (0xA32C, "51c8ffb6", "dbra", "d0, $a2e4"),
    (0xA330, "4e75", "rts", ""),
    (0xAD1C, "4df900c00000", "lea.l", "$c00000.l, a6"),
    (0xAD22, "323c8f02", "move.w", "#$8f02, d1"),
    (0xAD26, "3018", "move.w", "(a0)+, d0"),
    (0xAD28, "6700009e", "beq.w", "$adc8"),
    (0xAD2C, "6b22", "bmi.b", "$ad50"),
    (0xAD2E, "7400", "moveq", "#$0, d2"),
    (0xAD30, "3418", "move.w", "(a0)+, d2"),
    (0xAD32, "4243", "clr.w", "d3"),
    (0xAD34, "0800000e", "btst.b", "#$e, d0"),
    (0xAD38, "6636", "bne.b", "$ad70"),
    (0xAD3A, "3602", "move.w", "d2, d3"),
    (0xAD3C, "0243007f", "andi.w", "#$7f, d3"),
    (0xAD40, "e24b", "lsr.w", "#$1, d3"),
    (0xAD42, "d640", "add.w", "d0, d3"),
    (0xAD44, "04430040", "subi.w", "#$40, d3"),
    (0xAD48, "6402", "bcc.b", "$ad4c"),
    (0xAD4A, "4243", "clr.w", "d3"),
    (0xAD4C, "9043", "sub.w", "d3, d0"),
    (0xAD4E, "6020", "bra.b", "$ad70"),
    (0xAD50, "323c8f80", "move.w", "#$8f80, d1"),
    (0xAD54, "02407fff", "andi.w", "#$7fff, d0"),
    (0xAD58, "7400", "moveq", "#$0, d2"),
    (0xAD5A, "3418", "move.w", "(a0)+, d2"),
    (0xAD5C, "3602", "move.w", "d2, d3"),
    (0xAD5E, "02431fff", "andi.w", "#$1fff, d3"),
    (0xAD62, "ee4b", "lsr.w", "#$7, d3"),
    (0xAD64, "d640", "add.w", "d0, d3"),
    (0xAD66, "04430040", "subi.w", "#$40, d3"),
    (0xAD6A, "6402", "bcc.b", "$ad6e"),
    (0xAD6C, "4243", "clr.w", "d3"),
    (0xAD6E, "9043", "sub.w", "d3, d0"),
    (0xAD70, "0240bfff", "andi.w", "#$bfff, d0"),
    (0xAD74, "5340", "subq.w", "#$1, d0"),
    (0xAD76, "33c100c00004", "move.w", "d1, $c00004.l"),
    (0xAD7C, "e58a", "lsl.l", "#$2, d2"),
    (0xAD7E, "e44a", "lsr.w", "#$2, d2"),
    (0xAD80, "00424000", "ori.w", "#$4000, d2"),
    (0xAD84, "4842", "swap", "d2"),
    (0xAD86, "23c200c00004", "move.l", "d2, $c00004.l"),
    (0xAD8C, "0c400008", "cmpi.w", "#$8, d0"),
    (0xAD90, "643e", "bcc.b", "$add0"),
    (0xAD92, "3c98", "move.w", "(a0)+, (a6)"),
    (0xAD94, "51c8fffc", "dbra", "d0, $ad92"),
    (0xAD98, "4a43", "tst.w", "d3"),
    (0xAD9A, "6780", "beq.b", "$ad1c"),
    (0xAD9C, "08010001", "btst.b", "#$1, d1"),
    (0xADA0, "6708", "beq.b", "$adaa"),
    (0xADA2, "0282ff80ffff", "andi.l", "#$ff80ffff, d2"),
    (0xADA8, "6006", "bra.b", "$adb0"),
    (0xADAA, "0282e07fffff", "andi.l", "#$e07fffff, d2"),
    (0xADB0, "5343", "subq.w", "#$1, d3"),
    (0xADB2, "23c200c00004", "move.l", "d2, $c00004.l"),
    (0xADB8, "0c430008", "cmpi.w", "#$8, d3"),
    (0xADBC, "6428", "bcc.b", "$ade6"),
    (0xADBE, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADC0, "51cbfff6", "dbra", "d3, $adb8"),
    (0xADC4, "6000ff56", "bra.w", "$ad1c"),
    (0xADC8, "33c100c00004", "move.w", "d1, $c00004.l"),
    (0xADCE, "4e75", "rts", ""),
    (0xADD0, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADD2, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADD4, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADD6, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADD8, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADDA, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADDC, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADDE, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADE0, "04400008", "subi.w", "#$8, d0"),
    (0xADE4, "60a6", "bra.b", "$ad8c"),
    (0xADE6, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADE8, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADEA, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADEC, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADEE, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADF0, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADF2, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADF4, "3c98", "move.w", "(a0)+, (a6)"),
    (0xADF6, "04430008", "subi.w", "#$8, d3"),
    (0xADFA, "60bc", "bra.b", "$adb8"),
    (0xADFC, "4202", "clr.b", "d2"),
    (0xADFE, "4df900c00000", "lea.l", "$c00000.l, a6"),
    (0xAE04, "4a02", "tst.b", "d2"),
    (0xAE06, "6706", "beq.b", "$ae0e"),
    (0xAE08, "321a", "move.w", "(a2)+, d1"),
    (0xAE0A, "5302", "subq.b", "#$1, d2"),
    (0xAE0C, "6004", "bra.b", "$ae12"),
    (0xAE0E, "3218", "move.w", "(a0)+, d1"),
    (0xAE10, "5340", "subq.w", "#$1, d0"),
    (0xAE12, "0c41fe00", "cmpi.w", "#$fe00, d1"),
    (0xAE16, "640c", "bcc.b", "$ae24"),
    (0xAE18, "3c81", "move.w", "d1, (a6)"),
    (0xAE1A, "4a02", "tst.b", "d2"),
    (0xAE1C, "66e6", "bne.b", "$ae04"),
    (0xAE1E, "4a40", "tst.w", "d0"),
    (0xAE20, "6ae2", "bpl.b", "$ae04"),
    (0xAE22, "4e75", "rts", ""),
    (0xAE24, "0c41ff00", "cmpi.w", "#$ff00, d1"),
    (0xAE28, "6420", "bcc.b", "$ae4a"),
    (0xAE2A, "024100ff", "andi.w", "#$ff, d1"),
    (0xAE2E, "e549", "lsl.w", "#$2, d1"),
    (0xAE30, "45f11000", "lea.l", "(a1, d1.w), a2"),
    (0xAE34, "0c52ff00", "cmpi.w", "#$ff00, (a2)"),
    (0xAE38, "640a", "bcc.b", "$ae44"),
    (0xAE3A, "0c52fe00", "cmpi.w", "#$fe00, (a2)"),
    (0xAE3E, "6504", "bcs.b", "$ae44"),
    (0xAE40, "3c92", "move.w", "(a2), (a6)"),
    (0xAE42, "60c0", "bra.b", "$ae04"),
    (0xAE44, "143c0002", "move.b", "#$2, d2"),
    (0xAE48, "60ba", "bra.b", "$ae04"),
    (0xAE4A, "024100ff", "andi.w", "#$ff, d1"),
    (0xAE4E, "4a02", "tst.b", "d2"),
    (0xAE50, "6706", "beq.b", "$ae58"),
    (0xAE52, "361a", "move.w", "(a2)+, d3"),
    (0xAE54, "5302", "subq.b", "#$1, d2"),
    (0xAE56, "6010", "bra.b", "$ae68"),
    (0xAE58, "3618", "move.w", "(a0)+, d3"),
    (0xAE5A, "5340", "subq.w", "#$1, d0"),
    (0xAE5C, "0c43ff00", "cmpi.w", "#$ff00, d3"),
    (0xAE60, "6406", "bcc.b", "$ae68"),
    (0xAE62, "0c43fe00", "cmpi.w", "#$fe00, d3"),
    (0xAE66, "6410", "bcc.b", "$ae78"),
    (0xAE68, "3c83", "move.w", "d3, (a6)"),
    (0xAE6A, "51c9fffc", "dbra", "d1, $ae68"),
    (0xAE6E, "4a02", "tst.b", "d2"),
    (0xAE70, "6692", "bne.b", "$ae04"),
    (0xAE72, "4a40", "tst.w", "d0"),
    (0xAE74, "6a8e", "bpl.b", "$ae04"),
    (0xAE76, "4e75", "rts", ""),
    (0xAE78, "024300ff", "andi.w", "#$ff, d3"),
    (0xAE7C, "e54b", "lsl.w", "#$2, d3"),
    (0xAE7E, "45f13000", "lea.l", "(a1, d3.w), a2"),
    (0xAE82, "361a", "move.w", "(a2)+, d3"),
    (0xAE84, "143c0001", "move.b", "#$1, d2"),
    (0xAE88, "60de", "bra.b", "$ae68"),
)
_ROWS=dict(camera._ROWS)
_ROWS.update({p:dict(bytes=b,mnemonic=m,operand=o) for p,b,m,o in _INITIAL_INSTRUCTIONS})
MASK,sign,operands=camera.MASK,camera.sign,camera.operands
sha,dump,keys,same,uint,exact_list=camera.sha,camera.dump,camera.keys,camera.same,camera.uint,camera.exact_list
safe_path,read_bounded,put,load_fields=camera.safe_path,camera.read_bounded,camera.put,camera.load_fields
verify_rom=camera.verify_rom


def _controls(image):
    for a,z,h in BODIES:
        if sha(image[a:z])!=h:raise ValueError('original control or cart geometry differs:'+hex(a))


class _StepCount:
    """Count real executed opcodes without duplicating a huge instruction trace."""
    def __init__(self):self.count=0;self.reached_A2DC=False;self.reached_A314=False
    def __len__(self):return self.count
    def append(self,row):
        self.count+=1
        self.reached_A2DC |= row['PC']==0xA2DC
        self.reached_A314 |= row['PC']==0xA314


class _InitialReader(camera._CameraReader):
    def __init__(self,image,frame,budget,ram_before,status):
        super().__init__(image,_ROWS,frame,budget,ram_before)
        self.pc=0x05B6;self.SR=0x2500;self.dma_status=status;self.steps=_StepCount()

    def ea(self,s,width,update=True):
        m=re.fullmatch(r'\$([0-9a-f]+)\(pc\)',s)
        # Resolved targets are backed by the fixed original encoded opcodes.
        if m:return int(m[1],16)
        return super().ea(s,width,update)

    def put(self,s,width,value):
        if s=='sr':
            self.SR=value&65535
            self.C=bool(value&1);self.V=bool(value&2);self.Z=bool(value&4)
            self.N=bool(value&8);self.X=bool(value&16)
            self.events.append(dict(kind='SR_write',PC=self.pc,width=2,value=self.SR,
                role='original_SR_write'))
        else:super().put(s,width,value)

    def read(self,address,width,role='data'):
        bus=address&0xFFFFFF
        if bus==0xC00004 and width==2 and self.pc in (0x6886,0x68FA):
            value=self.dma_status
            self.events.append(dict(kind='read',PC=self.pc,address=address&0xFFFFFFFF,
                bus_address=bus,width=2,bytes=value.to_bytes(2,'big').hex(),value=value,
                memory=['conditional_VDP_status']*2,physical_addresses=[None]*2,
                role='supplied_constant_status_WORD_DMA_bit2_test'))
            return value
        return super().read(address,width,role)

    def write(self,address,width,value,role='data'):
        bus=address&0xFFFFFF
        if (bus in (0xC00000,0xC00004) and width in (2,4)) or (bus==0xA11100 and width==2):
            self.events.append(dict(kind='write',PC=self.pc,address=address&0xFFFFFFFF,bus_address=bus,
                width=width,bytes=(value&MASK[width]).to_bytes(width,'big').hex(),value=value&MASK[width],
                memory=['conditional_VDP_sink' if bus in (0xC00000,0xC00004) else 'conditional_Z80_bus_control_sink']*width,
                role='actual_original_MMIO_write_recorded_no_hardware_claim'))
            return
        return super().write(address,width,value,role)

    def run(self):
        result='instrumentation_budget_exhausted_not_CPU_stop'
        try:
            while self.pc!=0x05BC:
                if len(self.steps)>=self.budget:raise camera._ReadBoundary(result)
                if self.pc not in self.rows:raise camera._ReadBoundary('not_pinned_original_PC:'+hex(self.pc))
                row=self.rows[self.pc];raw=bytes.fromhex(row['bytes'])
                assert self.image[self.pc:self.pc+len(raw)]==raw
                name,*size=row['mnemonic'].split('.');width={'b':1,'w':2,'l':4}.get(size[0] if size else '',0)
                ops=operands(row['operand']) if row['operand'] else []
                nextpc=self.pc+len(raw);step=dict(PC=self.pc,bytes=raw.hex(),mnemonic=row['mnemonic'],operand=row['operand'])
                self.steps.append(step)
                if name=='nop':pass
                elif name in ('jsr','bsr'):
                    target=self.target(ops[0]);self.A[7]=(self.A[7]-4)&0xFFFFFFFF
                    self.write(self.A[7],4,nextpc,'real_JSR_BSR_return_stack')
                    self.calls.append(dict(kind='call',PC=self.pc,target=target,return_PC=nextpc,SP=self.A[7]));nextpc=target
                elif name=='rts':
                    target=self.read(self.A[7],4,'real_RTS_return_stack');self.A[7]=(self.A[7]+4)&0xFFFFFFFF
                    self.calls.append(dict(kind='return',PC=self.pc,target=target,SP=self.A[7]));nextpc=target
                elif name=='dbra':
                    reg=int(ops[0][1:]);self.D[reg]=(self.D[reg]&0xFFFF0000)|((self.D[reg]-1)&65535)
                    if self.D[reg]&65535!=65535:nextpc=self.target(ops[1])
                elif name.startswith('b') and name not in ('btst','bclr'):
                    if self.condition(name):nextpc=self.target(ops[0])
                elif name=='move':
                    value=self.get(ops[0],width);self.put(ops[1],width,value)
                    if ops[1]!='sr':self.logic(value,width)
                elif name=='movea':
                    value=self.get(ops[0],width)
                    if width==2:value=sign(value,2)
                    self.A[int(ops[1][1:])]=value&0xFFFFFFFF
                elif name=='moveq':
                    value=sign(self.get(ops[0],1),1)&0xFFFFFFFF
                    self.D[int(ops[1][1:])]=value;self.logic(value,4)
                elif name=='lea':self.A[int(ops[1][1:])]=self.ea(ops[0],4,False)
                elif name=='movem':
                    if ops[1]=='-(a7)':
                        for kind,n in reversed(self.movem_regs(ops[0])):
                            self.A[7]=(self.A[7]-width)&0xFFFFFFFF
                            self.write(self.A[7],width,(self.D if kind=='d' else self.A)[n],'real_MOVEM_save')
                    elif ops[0]=='(a7)+':
                        for kind,n in self.movem_regs(ops[1]):
                            value=self.read(self.A[7],width,'real_MOVEM_restore');self.A[7]=(self.A[7]+width)&0xFFFFFFFF
                            (self.D if kind=='d' else self.A)[n]=value if width==4 else sign(value,2)&0xFFFFFFFF
                    else:raise camera._ReadBoundary('unsupported_original_MOVEM:'+row['operand'])
                elif name in ('clr','tst','ext','swap','neg'):
                    if name=='clr':value=0;self.put(ops[0],width,value);self.logic(value,width)
                    elif name=='tst':self.logic(self.get(ops[0],width),width)
                    elif name=='ext':
                        value=sign(self.get(ops[0],1 if width==2 else 2),1 if width==2 else 2)&MASK[width]
                        self.put(ops[0],width,value);self.logic(value,width)
                    elif name=='swap':
                        value=self.get(ops[0],4);value=((value<<16)|(value>>16))&0xFFFFFFFF
                        self.put(ops[0],4,value);self.logic(value,4)
                    else:
                        value=self.calc(0,self.get(ops[0],width),width,True);self.put(ops[0],width,value)
                elif name in ('lsr','lsl'):
                    count=self.get(ops[0],4);value=self.get(ops[1],width)
                    last=False
                    for _ in range(count):
                        if name=='lsr':last=bool(value&1);value>>=1
                        else:last=bool(value&(1<<(width*8-1)));value=(value<<1)&MASK[width]
                    self.put(ops[1],width,value);self.logic(value,width);self.C=last
                    if count:self.X=last
                elif name in ('addi','subi','add','sub','addq','subq','cmp','cmpi','adda'):
                    right=self.get(ops[0],width);left=self.get(ops[1],width)
                    if name=='adda' or name in ('addq','subq') and ops[1].startswith('a') and len(ops[1])==2:
                        reg=int(ops[1][1:]);v=sign(right,2) if width==2 else sign(right,4)
                        self.A[reg]=(self.A[reg]+(-v if name=='subq' else v))&0xFFFFFFFF
                    else:
                        oldX=self.X;v=self.calc(left,right,width,name.startswith('sub') or name.startswith('cmp'))
                        if name.startswith('cmp'):self.X=oldX
                        else:self.put(ops[1],width,v)
                elif name in ('andi','ori','or','and'):
                    right=self.get(ops[0],width);left=self.get(ops[1],width)
                    value=left&right if name.startswith('and') else left|right
                    self.put(ops[1],width,value);self.logic(value,width)
                elif name in ('mulu','divu'):
                    src=self.get(ops[0],2);n=int(ops[1][1:])
                    if name=='mulu':self.D[n]=(self.D[n]&65535)*src;self.logic(self.D[n],4)
                    else:
                        if not src:raise camera._ReadBoundary('original_DIVU_zero')
                        q,r=divmod(self.D[n],src)
                        if q>65535:self.V=True;self.C=False
                        else:self.D[n]=(r<<16)|q;self.logic(q,2)
                elif name in ('btst','bclr'):
                    bit=self.get(ops[0],4);w=4 if re.fullmatch(r'd[0-7]',ops[1]) else 1
                    bit%=32 if w==4 else 8;value=self.get(ops[1],w);self.Z=not bool(value&(1<<bit))
                    if name=='bclr':self.put(ops[1],w,value&~(1<<bit))
                else:raise camera._ReadBoundary('unsupported_original_opcode:'+row['mnemonic']+' '+row['operand'])
                self.pc=nextpc
            result='actual_JSR_A1B2_RTS_to_05BC'
        except camera._ReadBoundary as e:result=str(e)
        return dict(result=result,conditional_ram_WORDs={f'{a:04X}':v for a,v in self.frame.items()},
                    entry_call_PC=0x05B6,requested_normal_return_PC=0x05BC,
                    actual_final_PC=self.pc,initial_SP=self.initial_sp,final_SP=self.A[7],
                    instruction_count=len(self.steps),actual_call_return_events=self.calls,
                    ordered_data_events=self.events,final_RAM_sha256=sha(self.ram),
                    source_events=[e for e in self.events if e['kind']=='read' and 'ROM' in e['memory']],
                    CPU=False,natural_frame=False,earlier_parent_UI_helpers_closed=False,
                    budget_is_instrumentation_only=True)


def source_view(image, initial_coordinate_WORDs, instruction_budget=250000,
                RAM_before=None, dma_status_WORD=0, include_prefix_events=False):
    """Pure live original caller prefix; no host A5, helper or terrain index.

    Complete64KiB RAM defaults to zero; only F356/F354 are supplied WORDs.
    Constant status0 means DMA bit2 clear on the two actual status-read sites.
    Recorded VDP/Z80 writes are conditional sinks, not hardware equivalence.
    Complete events may be requested, but normal bundles keep compact evidence.
    """
    camera._image(image);_controls(image)
    keys(initial_coordinate_WORDs,{'F356','F354'},'complete initial coordinate WORD frame')
    frame={int(k,16):uint(v,65535,'initial.'+k) for k,v in initial_coordinate_WORDs.items()}
    budget=uint(instruction_budget,250000,'diagnostic original instruction budget')
    if budget<1:raise ValueError('positive instruction budget required')
    status=uint(dma_status_WORD,65535,'full supplied DMA status WORD')
    if type(include_prefix_events) is not bool:raise ValueError('boolean include_prefix_events required')
    if RAM_before is not None and (type(RAM_before) is not bytes or len(RAM_before)!=65536):
        raise ValueError('complete immutable64KiB RAM bytes required')
    reader=_InitialReader(image,frame,budget,RAM_before,status)
    initial_ram=bytes(reader.ram)
    view=reader.run()
    events=view.pop('ordered_data_events')
    # Retain all live decoder/directory data events; the large real helper
    # prefix is described by a deterministic digest and count, not duplicated.
    source=view.pop('source_events')
    decoder=[e for e in source if 0xAF6A<=e['PC']<0xB210]
    view.update(source_events=decoder,ordered_decoder_events=[e for e in events if 0xAF6A<=e['PC']<0xB210],
        ordered_data_event_count=len(events),ordered_data_events_sha256=sha(dump(events)),
        prefix_ROM_read_count=len(source)-len(decoder),
        conditional_MMIO_status_reads=[e for e in events if e.get('memory')==['conditional_VDP_status']*2],
        conditional_MMIO_write_count=sum(e['kind']=='write' and any('conditional_' in m for m in e.get('memory',[])) for e in events),
        reached_A2DC=reader.steps.reached_A2DC,reached_A314=reader.steps.reached_A314,
        final_registers=dict(D=list(reader.D),A=list(reader.A),
            SR=(reader.SR&0xFFE0)|(int(reader.X)<<4)|(int(reader.N)<<3)|(int(reader.Z)<<2)|(int(reader.V)<<1)|int(reader.C)),
        last_explicit_SR_write=reader.SR,
        final_CCR=dict(X=reader.X,N=reader.N,Z=reader.Z,V=reader.V,C=reader.C),
        RAM_before_sha256=sha(initial_ram),
        RAM_frame_default='zero64KiB plus F356/F354 WORDs' if RAM_before is None else 'complete supplied64KiB plus F356/F354 WORDs',
        DMA_status_WORD=status,complete_function_recovery=False,owner='unknown',natural_domain='unknown',
        parent_05B6_handler_state_closed=False,padding_or_free_space=False,
        hardware_profile='conditional constant status at6886/68FA; recorded VDP/Z80 write sinks only',
        original_hardware_equivalence='unknown',source_read_budget_is_CPU_stop=False,
        cart_profile='24bit measured MAME ROM0..200000/204000..400000; SRAM excluded; beyond4MiB unknown',
        physical_source=sorted({p for e in decoder for p in e['physical_addresses'] if p is not None}))
    if include_prefix_events:view['ordered_data_events']=events
    return view


def _coalesce(positions):return camera._coalesce(sorted(positions))


@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom)
    wanted={p for a,z in SOURCE_SPANS for p in range(a,z)}
    found={}
    for index,frame in enumerate(WITNESS_FRAMES):
        view=source_view(rom,frame)
        for event_index,event in enumerate(view['source_events']):
            for lane,p in enumerate(event['physical_addresses']):
                if p in wanted and p not in found:
                    if event['width']!=2 or event['PC'] not in (0xB116,0xB16A,0xB180,0xB1DE):
                        raise ValueError('original RLE WORD source role differs')
                    found[p]=dict(address=p,frame_index=index,initial_coordinate_WORDs=dict(frame),
                        read_PC=event['PC'],read_width=2,source_address=event['address'],
                        bus_address=event['bus_address'],physical_WORD_addresses=list(event['physical_addresses']),
                        WORD_BYTE_lane=lane,canonical_read_WORD=event['value'],
                        source_event_index=event_index,original_boundary=view['result'],
                        original_boundary_PC=view['actual_final_PC'],true_JSR_PC=0x05B6,
                        parent_05B6_handler_state_closed=False,actual_instruction_count=view['instruction_count'])
    if set(found)!=wanted or len(found)!=EDITABLE_BYTES or len(_coalesce(found))!=PHYSICAL_BLOCKS:
        raise ValueError('true initialization conditional source scope differs')
    return tuple(found[p] for p in sorted(found))


def physical_positions(rom):
    verify_rom(rom)
    return tuple(row['address'] for row in _catalog(rom))


def witness(rom,address):
    verify_rom(rom);address=uint(address,ROM_SIZE-1,'source BYTE')
    for row in _catalog(rom):
        if row['address']==address:return load_fields(dump(row))
    raise ValueError('outside initial-map physical authority')


def metadata(rom):
    positions=physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditional_original_RLE_WORD_source_BYTE_fragments',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        source_union_BYTES=EDITABLE_BYTES,source_union_sha256=sha(bytes(rom[p] for p in positions)),
        physical_blocks=PHYSICAL_BLOCKS,physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in _coalesce(positions)],
        raw_baseline=dict(layout_id=LAYOUT_ID,manifest_sha256=LAYOUT_SHA256,raw_BYTES=13758,resources=100),
        roles=dict(resource='initial_map_column_RLE_WORD_source_BYTE_fragments',
            original_WORD_read_PCs=[0xB116,0xB16A,0xB180,0xB1DE],
            BYTE_values='all0..255 high/low fragments of complete live WORDs',
            old_typed_WORD_neighbors='whole edited image live views only, never re-emitted',
            zero_WORD='literal WORD0 under original grammar, not padding'),
        evidence=dict(true_caller_PC=0x05B6,entry=0xA1B2,normal_return_PC=0x05BC,
            live_RAM_WORD_producers=[dict(PC=0xA1CA,source='F356',destination='F314',bytes='31f8f356f314'),
                dict(PC=0xA1D0,source='F354',destination='F318',bytes='31f8f354f318')],
            real_prefix='A242 BSR A278; real ADFC/VDP helpers then A2DC; A2F8 JSR AF6A; A314 JSR B06E',
            producer='fullWORD camera arithmetic, signed WORD operations and original unsigned DIVU/multiply/stride semantics',
            status_read_PCs=[0x6886,0x68FA],conditional_status_WORD=0,
            header=0x8155A,directory_lookup=0xAF6A,column_lookup=0xB0DE,
            witness_frames=[dict(f) for f in WITNESS_FRAMES],
            controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES],
            source_header_directory_column_RLE_data_live=True,diagnostic_frame_count=3),
        editing_authority='single physical fullBYTE; WORDs/other aliases are live source views only',
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,functions_added=0,
        complete_function_recovery=False,independent_CPU_comparison=False,
        parent_05B6_handler_state_closed=False,natural_coordinate_domain='unknown',allocation_or_atlas_owner='unknown',
        canonical_frames='zero64KiB RAM+F356/F354; D/A0, SPFFFFFD00, SR2500; status0 and recorded sinks',
        canonical_boundaries='all3 stop at actual odd/unknown bus access; rows_completed0; no manufactured RTS',
        edited_gameplay_safety='unknown',padding_or_free_space_claimed=False,
        instrumentation_budget_is_original_CPU_stop=False,final_semantic_high_level_recovery=False)


def extract(rom):
    return dict(**metadata(rom),source_BYTEs=[dict(address=p,RLE_WORD_address=p&~1,
        WORD_BYTE_lane='high' if not p&1 else 'low',BYTE=rom[p]) for p in physical_positions(rom)])


def blocks(rom,fields):
    fixed=metadata(rom);keys(fields,set(fixed)|{'source_BYTEs'},'initial map source package')
    for k,v in fixed.items():same(fields[k],v,'package.'+k)
    values={}
    for p,row in zip(physical_positions(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'source BYTEs')):
        keys(row,{'address','RLE_WORD_address','WORD_BYTE_lane','BYTE'},'source BYTE fragment')
        for k,v in dict(address=p,RLE_WORD_address=p&~1,WORD_BYTE_lane='high' if not p&1 else 'low').items():
            same(row[k],v,'fragment.'+k)
        values[p]=uint(row['BYTE'],255,'complete source BYTE')
    return [dict(id=f'rom_{a:06X}_initial_map_RLE_source_BYTEs',start=a,end=z,
        data=bytes(values[p] for p in range(a,z)),role='conditional_initial_map_RLE_WORD_source_BYTE_fragments')
        for a,z in _coalesce(physical_positions(rom))]


def rebuild(rom,fields):
    verify_rom(rom)
    image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)


def schema(rom):
    def obj(p):return dict(type='object',properties=p,required=list(p),additionalProperties=False)
    def fixed(v):
        if type(v) is dict:return obj({k:fixed(x) for k,x in v.items()})
        if type(v) is list:return dict(type='array',prefixItems=[fixed(x) for x in v],items=False,minItems=len(v),maxItems=len(v))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(v)],const=v)
    p={k:fixed(v) for k,v in metadata(rom).items()}
    p['source_BYTEs']=dict(type='array',minItems=EDITABLE_BYTES,maxItems=EDITABLE_BYTES,items=False,
        prefixItems=[obj(dict(address=fixed(a),RLE_WORD_address=fixed(a&~1),
            WORD_BYTE_lane=fixed('high' if not a&1 else 'low'),BYTE=dict(type='integer',minimum=0,maximum=255)))
            for a in physical_positions(rom)])
    return dict(**obj(p),**{'$schema':'https://json-schema.org/draft/2020-12/schema'},
        description='19 unique full BYTE fragments of original conditionally read live RLE WORDs; no natural domain clamp.')


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('serialized complete ROM roundtrip differs')
    validation=dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
        limitations=['Constructed full-RAM05B6 caller frame, actual DMA/VDP prefix under explicit status/sink profile.',
            'Old controls/header/directory/WORD neighbors are live; edits can stop earlier.',
            'No allocation/owner/natural domain/full CPU/function/row-return/final high-level claim.'])
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),'validation.json':dump(validation)}
    members['manifest.json']=dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,
        members={k:dict(bytes=len(v),sha256=sha(v)) for k,v in members.items()}))
    return members


def fresh_output(value,bundle=False):
    path=safe_path(value)
    for ancestor in (path,*path.parents):
        if ancestor.is_symlink() or getattr(ancestor,'is_junction',lambda:False)():
            raise ValueError('reparse output refused')
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError('dedicated fresh build output or exact fresh formal bundle required')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields');p.add_argument('--bundle');p.add_argument('--output')
    a=p.parse_args();target=None
    if a.command=='export':
        if a.output is None or a.fields is not None or a.bundle is not None:raise ValueError('export requires output only')
        target=fresh_output(a.output,True)
    elif a.command=='import':
        if a.output is None or a.bundle is not None:raise ValueError('import requires fresh .bin output')
        target=fresh_output(a.output)
        if target.suffix.lower()!='.bin':raise ValueError('fresh .bin output required')
    elif a.output is not None or a.fields is not None and a.bundle is not None:
        raise ValueError('verify takes fields or bundle and writes nothing')
    rom=read_bounded(a.rom,ROM_SIZE)
    if a.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={k:sha(v) for k,v in members.items()})
    elif a.command=='verify' and a.bundle is not None:
        path=safe_path(a.bundle)
        if not path.is_dir() or {p.name for p in path.iterdir()}!=MEMBERS:raise ValueError('exact four bundle members required')
        for name,data in render_bundle(rom).items():
            if read_bounded(path/name,MAX_JSON)!=data:raise ValueError('generated member drift:'+name)
        result=dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True)
    else:
        image=rebuild(rom,load_fields(read_bounded(a.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:put(target,image)
        result=dict(exact_canonical=image==rom,sha256=sha(image),editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
