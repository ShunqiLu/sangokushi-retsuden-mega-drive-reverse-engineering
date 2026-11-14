"""Conditional original0528 scene descriptor/copier source BYTE aliases.

Only559 unique source BYTE fragments have finite whole-prefix witnesses. No runtime
private receipt, CSV, ROM dump, helper injection or artificial return is used.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
from functools import lru_cache
import json
from pathlib import Path
import re
from tools.initial_map_source_alias_fields import codec as initial
from tools.camera_chunk_source_alias_fields import codec as camera

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE=initial.ROM_SIZE
ROM_SHA256=initial.ROM_SHA256
DEFAULT_ROM=initial.DEFAULT_ROM
OUTPUT_ROOT=ROOT/'build/scene_descriptor_source_alias_fields'
FORMAL_ROOT=ROOT/'analysis/scene_descriptor_source_alias_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
DEFAULT_BUNDLE=FORMAL_ROOT
FORMAT='g5510-conditional-scene-descriptor-and-fixed-copier-source-BYTE-fragments-v1'
MAX_JSON=16*1024*1024
MEMBERS=initial.MEMBERS
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
EDITABLE_BYTES,PHYSICAL_BLOCKS=559,128
SOURCE_SPANS=(
    (0xC3640,0xC3644),
    (0xF3182,0xF3191),
    (0xF3193,0xF3197),
    (0xF3199,0xF319C),
    (0xF319E,0xF319F),
    (0xF31A4,0xF31A5),
    (0xF31AA,0xF31AD),
    (0xF31B1,0xF31B9),
    (0xF31BB,0xF31C0),
    (0xF31C4,0xF31C5),
    (0xF31C6,0xF31C7),
    (0xF31C9,0xF31CA),
    (0xF31CB,0xF31CF),
    (0xF31D1,0xF31D5),
    (0xF31D7,0xF31D8),
    (0xF31D9,0xF31DB),
    (0xF31DC,0xF31E3),
    (0xF31E4,0xF31E6),
    (0xF31E7,0xF31E8),
    (0xF31EC,0xF31ED),
    (0xF31F4,0xF31F6),
    (0xF31FA,0xF3200),
    (0xF3204,0xF320E),
    (0xF3212,0xF3216),
    (0xF3217,0xF3219),
    (0xF321A,0xF321C),
    (0xF321D,0xF321F),
    (0xF3220,0xF3221),
    (0xF3223,0xF3227),
    (0xF322E,0xF3231),
    (0xF3235,0xF3236),
    (0xF323A,0xF323C),
    (0xF3240,0xF3242),
    (0xF3243,0xF3247),
    (0xF3406,0xF3408),
    (0xF340A,0xF340F),
    (0xF3423,0xF3424),
    (0xF342E,0xF342F),
    (0xF3434,0xF3436),
    (0xF343A,0xF343B),
    (0xF343D,0xF343E),
    (0xF3447,0xF3448),
    (0xF3453,0xF3457),
    (0xF3465,0xF3466),
    (0xF3469,0xF346A),
    (0xF346C,0xF346D),
    (0xF347E,0xF347F),
    (0xF3E05,0xF3E07),
    (0xF3E0D,0xF3E0E),
    (0xF3E0F,0xF3E10),
    (0xF3E12,0xF3E13),
    (0xF3E17,0xF3E18),
    (0xF3E30,0xF3E31),
    (0xF3E34,0xF3E37),
    (0xF3E4A,0xF3E4C),
    (0xF3E4D,0xF3E50),
    (0xF3E56,0xF3E57),
    (0xF3E5D,0xF3E5F),
    (0xF3E79,0xF3E7F),
    (0xF6016,0xF6017),
    (0xF601B,0xF601F),
    (0xF6024,0xF6028),
    (0xF602A,0xF602C),
    (0xF602F,0xF6039),
    (0xF603E,0xF603F),
    (0xF6041,0xF6044),
    (0xF6048,0xF6049),
    (0xF604B,0xF604C),
    (0xF604E,0xF604F),
    (0xF6050,0xF6051),
    (0xF6053,0xF6059),
    (0xF605B,0xF605E),
    (0xF6063,0xF6065),
    (0xF6068,0xF606A),
    (0xF606B,0xF606D),
    (0xF606F,0xF6072),
    (0xF6075,0xF6076),
    (0xF607A,0xF607F),
    (0xF6081,0xF6082),
    (0xF608A,0xF608C),
    (0xF6094,0xF6096),
    (0xF609A,0xF609B),
    (0xF609C,0xF60A0),
    (0xF60A3,0xF60A7),
    (0xF60AB,0xF60AC),
    (0xF60AD,0xF60AF),
    (0xF60B2,0xF60B4),
    (0xF60B5,0xF60B7),
    (0xF60B8,0xF60B9),
    (0xF60BA,0xF60BC),
    (0xF60C0,0xF60C2),
    (0xF60C3,0xF60C4),
    (0xF60C7,0xF60C9),
    (0xF60CA,0xF60CB),
    (0xF60CD,0xF60CE),
    (0xF60D3,0xF60D5),
    (0xF60DA,0xF60DB),
    (0xF60DF,0xF60E1),
    (0xF60E3,0xF60E7),
    (0xF60E9,0xF60EA),
    (0xF6101,0xF6102),
    (0xF6107,0xF6108),
    (0xF610C,0xF610E),
    (0xF6111,0xF6112),
    (0xF6116,0xF6117),
    (0xF611B,0xF611E),
    (0xF6123,0xF6127),
    (0xF6129,0xF612A),
    (0xF612C,0xF6130),
    (0xF6138,0xF6139),
    (0xF613E,0xF6140),
    (0xF6142,0xF6144),
    (0xF6147,0xF6148),
    (0xF6151,0xF6152),
    (0xF6156,0xF615B),
    (0xF615F,0xF6160),
    (0xF6161,0xF6163),
    (0xF616A,0xF616C),
    (0xF6172,0xF6174),
    (0xF6175,0xF6177),
    (0xF6178,0xF617A),
    (0xF6608,0xF6666),
    (0xF666A,0xF6684),
    (0xF6708,0xF670C),
    (0xF6710,0xF6716),
    (0xF671A,0xF672C),
    (0xF6730,0xF6740),
    (0xF6744,0xF67A8),
)
WITNESS_SELECTORS=(1997,2009,2015,2529,2568,4803,5256,5301,6874,7513,12536,12708,)
BODIES=(
    (0x528,0x548,reference_value(__name__, 'BODIES')),
    (0x6826,0x68A8,reference_value(__name__, 'BODIES_2')),
    (0x3076E,0x307E0,reference_value(__name__, 'BODIES_3')),
    (0x3E54,0x40B0,reference_value(__name__, 'BODIES_4')),
    (0x1A0,0x1BC,reference_value(__name__, 'BODIES_5')),
)
_INSTRUCTIONS=(
    (0x528,"46fc2700","move.w","#$2700, sr"),
    (0x52C,"4eb900006826","jsr","$6826.l"),
    (0x532,"4eb90003076e","jsr","$3076e.l"),
    (0x538,"31fc0200f612","move.w","#$200, $f612.w"),
    (0x53E,"4278f352","clr.w","$f352.w"),
    (0x542,"4eb900003e54","jsr","$3e54.l"),
    (0x3E54,"3038efd4","move.w","$efd4.w, d0"),
    (0x3E58,"e548","lsl.w","#$2, d0"),
    (0x3E5A,"247b00ec","movea.l","$3e48(pc, d0.w), a2"),
    (0x3E5E,"2052","movea.l","(a2), a0"),
    (0x3E60,"43f8f428","lea.l","$f428.w, a1"),
    (0x3E64,"610001c0","bsr.w","$4026"),
    (0x3E68,"206a0004","movea.l","$4(a2), a0"),
    (0x3E6C,"43f8f460","lea.l","$f460.w, a1"),
    (0x3E70,"610001f0","bsr.w","$4062"),
    (0x3E74,"206a0008","movea.l","$8(a2), a0"),
    (0x3E78,"43f8e640","lea.l","$e640.w, a1"),
    (0x3E7C,"303c0007","move.w","#$7, d0"),
    (0x3E80,"22d8","move.l","(a0)+, (a1)+"),
    (0x3E82,"51c8fffc","dbra","d0, $3e80"),
    (0x3E86,"206a000c","movea.l","$c(a2), a0"),
    (0x3E8A,"43f8e000","lea.l","$e000.w, a1"),
    (0x3E8E,"610001a2","bsr.w","$4032"),
    (0x3E92,"206a0010","movea.l","$10(a2), a0"),
    (0x3E96,"43f8e0a0","lea.l","$e0a0.w, a1"),
    (0x3E9A,"61000196","bsr.w","$4032"),
    (0x3E9E,"206a0014","movea.l","$14(a2), a0"),
    (0x3EA2,"43f8e140","lea.l","$e140.w, a1"),
    (0x3EA6,"6100018a","bsr.w","$4032"),
    (0x3EAA,"206a0018","movea.l","$18(a2), a0"),
    (0x3EAE,"43f8e1e0","lea.l","$e1e0.w, a1"),
    (0x3EB2,"6100017e","bsr.w","$4032"),
    (0x3EB6,"206a001c","movea.l","$1c(a2), a0"),
    (0x3EBA,"43f8e280","lea.l","$e280.w, a1"),
    (0x3EBE,"61000172","bsr.w","$4032"),
    (0x3EC2,"206a0020","movea.l","$20(a2), a0"),
    (0x3EC6,"43f8e320","lea.l","$e320.w, a1"),
    (0x3ECA,"61000166","bsr.w","$4032"),
    (0x3ECE,"206a0024","movea.l","$24(a2), a0"),
    (0x3ED2,"43f8e3c0","lea.l","$e3c0.w, a1"),
    (0x3ED6,"6100015a","bsr.w","$4032"),
    (0x3EDA,"206a0028","movea.l","$28(a2), a0"),
    (0x3EDE,"43f8e460","lea.l","$e460.w, a1"),
    (0x3EE2,"6100014e","bsr.w","$4032"),
    (0x3EE6,"206a002c","movea.l","$2c(a2), a0"),
    (0x3EEA,"43f8e500","lea.l","$e500.w, a1"),
    (0x3EEE,"61000142","bsr.w","$4032"),
    (0x3EF2,"206a0030","movea.l","$30(a2), a0"),
    (0x3EF6,"43f8e5a0","lea.l","$e5a0.w, a1"),
    (0x3EFA,"61000136","bsr.w","$4032"),
    (0x3EFE,"206a0034","movea.l","$34(a2), a0"),
    (0x3F02,"43f8b000","lea.l","$b000.w, a1"),
    (0x3F06,"61000136","bsr.w","$403e"),
    (0x3F0A,"206a0038","movea.l","$38(a2), a0"),
    (0x3F0E,"43f8b200","lea.l","$b200.w, a1"),
    (0x3F12,"6100012a","bsr.w","$403e"),
    (0x3F16,"206a003c","movea.l","$3c(a2), a0"),
    (0x3F1A,"43f8b400","lea.l","$b400.w, a1"),
    (0x3F1E,"6100011e","bsr.w","$403e"),
    (0x3F22,"206a0040","movea.l","$40(a2), a0"),
    (0x3F26,"43f8b600","lea.l","$b600.w, a1"),
    (0x3F2A,"61000112","bsr.w","$403e"),
    (0x3F2E,"206a0044","movea.l","$44(a2), a0"),
    (0x3F32,"43f8b800","lea.l","$b800.w, a1"),
    (0x3F36,"61000106","bsr.w","$403e"),
    (0x3F3A,"206a0048","movea.l","$48(a2), a0"),
    (0x3F3E,"43f8ba00","lea.l","$ba00.w, a1"),
    (0x3F42,"610000fa","bsr.w","$403e"),
    (0x3F46,"206a004c","movea.l","$4c(a2), a0"),
    (0x3F4A,"43f8bc00","lea.l","$bc00.w, a1"),
    (0x3F4E,"610000ee","bsr.w","$403e"),
    (0x3F52,"206a0050","movea.l","$50(a2), a0"),
    (0x3F56,"43f8be00","lea.l","$be00.w, a1"),
    (0x3F5A,"610000e2","bsr.w","$403e"),
    (0x3F5E,"206a0054","movea.l","$54(a2), a0"),
    (0x3F62,"43f8c000","lea.l","$c000.w, a1"),
    (0x3F66,"610000d6","bsr.w","$403e"),
    (0x3F6A,"206a0058","movea.l","$58(a2), a0"),
    (0x3F6E,"43f8c200","lea.l","$c200.w, a1"),
    (0x3F72,"610000d6","bsr.w","$404a"),
    (0x3F76,"206a005c","movea.l","$5c(a2), a0"),
    (0x3F7A,"43f8c300","lea.l","$c300.w, a1"),
    (0x3F7E,"610000ca","bsr.w","$404a"),
    (0x3F82,"206a0060","movea.l","$60(a2), a0"),
    (0x3F86,"43f8c400","lea.l","$c400.w, a1"),
    (0x3F8A,"610000be","bsr.w","$404a"),
    (0x3F8E,"206a0064","movea.l","$64(a2), a0"),
    (0x3F92,"43f8c500","lea.l","$c500.w, a1"),
    (0x3F96,"610000b2","bsr.w","$404a"),
    (0x3F9A,"206a0068","movea.l","$68(a2), a0"),
    (0x3F9E,"43f8c600","lea.l","$c600.w, a1"),
    (0x3FA2,"610000a6","bsr.w","$404a"),
    (0x3FA6,"206a006c","movea.l","$6c(a2), a0"),
    (0x3FAA,"43f8c700","lea.l","$c700.w, a1"),
    (0x3FAE,"6100009a","bsr.w","$404a"),
    (0x3FB2,"206a0070","movea.l","$70(a2), a0"),
    (0x3FB6,"43f8c800","lea.l","$c800.w, a1"),
    (0x3FBA,"6100009a","bsr.w","$4056"),
    (0x3FBE,"206a0074","movea.l","$74(a2), a0"),
    (0x3FC2,"43f8cc00","lea.l","$cc00.w, a1"),
    (0x3FC6,"61000082","bsr.w","$404a"),
    (0x3FCA,"206a0078","movea.l","$78(a2), a0"),
    (0x3FCE,"43f8e710","lea.l","$e710.w, a1"),
    (0x3FD2,"6100009a","bsr.w","$406e"),
    (0x3FD6,"4278e700","clr.w","$e700.w"),
    (0x3FDA,"41f8e818","lea.l","$e818.w, a0"),
    (0x3FDE,"303c0077","move.w","#$77, d0"),
    (0x3FE2,"20fcffffffff","move.l","#$ffffffff, (a0)+"),
    (0x3FE8,"51c8fff8","dbra","d0, $3fe2"),
    (0x3FEC,"206a007c","movea.l","$7c(a2), a0"),
    (0x3FF0,"43f8ea88","lea.l","$ea88.w, a1"),
    (0x3FF4,"61000084","bsr.w","$407a"),
    (0x3FF8,"206a0080","movea.l","$80(a2), a0"),
    (0x3FFC,"43f8f000","lea.l","$f000.w, a1"),
    (0x4000,"61000094","bsr.w","$4096"),
    (0x4004,"31fc00fff376","move.w","#$ff, $f376.w"),
    (0x400A,"31fc0000efd4","move.w","#$0, $efd4.w"),
    (0x4010,"31fcffff9f00","move.w","#$ffff, $9f00.w"),
    (0x4016,"303c00ff","move.w","#$ff, d0"),
    (0x401A,"41f8a150","lea.l","$a150.w, a0"),
    (0x401E,"4298","clr.l","(a0)+"),
    (0x4020,"51c8fffc","dbra","d0, $401e"),
    (0x4024,"4e75","rts",""),
    (0x4026,"303c0009","move.w","#$9, d0"),
    (0x402A,"22d8","move.l","(a0)+, (a1)+"),
    (0x402C,"51c8fffc","dbra","d0, $402a"),
    (0x4030,"4e75","rts",""),
    (0x4032,"303c0027","move.w","#$27, d0"),
    (0x4036,"22d8","move.l","(a0)+, (a1)+"),
    (0x4038,"51c8fffc","dbra","d0, $4036"),
    (0x403C,"4e75","rts",""),
    (0x403E,"303c007f","move.w","#$7f, d0"),
    (0x4042,"22d8","move.l","(a0)+, (a1)+"),
    (0x4044,"51c8fffc","dbra","d0, $4042"),
    (0x4048,"4e75","rts",""),
    (0x404A,"303c003f","move.w","#$3f, d0"),
    (0x404E,"22d8","move.l","(a0)+, (a1)+"),
    (0x4050,"51c8fffc","dbra","d0, $404e"),
    (0x4054,"4e75","rts",""),
    (0x4056,"303c00ff","move.w","#$ff, d0"),
    (0x405A,"22d8","move.l","(a0)+, (a1)+"),
    (0x405C,"51c8fffc","dbra","d0, $405a"),
    (0x4060,"4e75","rts",""),
    (0x4062,"303c0013","move.w","#$13, d0"),
    (0x4066,"22d8","move.l","(a0)+, (a1)+"),
    (0x4068,"51c8fffc","dbra","d0, $4066"),
    (0x406C,"4e75","rts",""),
    (0x406E,"303c0007","move.w","#$7, d0"),
    (0x4072,"22d8","move.l","(a0)+, (a1)+"),
    (0x4074,"51c8fffc","dbra","d0, $4072"),
    (0x4078,"4e75","rts",""),
    (0x407A,"303c00ff","move.w","#$ff, d0"),
    (0x407E,"12a80001","move.b","$1(a0), (a1)"),
    (0x4082,"13500001","move.b","(a0), $1(a1)"),
    (0x4086,"136800020002","move.b","$2(a0), $2(a1)"),
    (0x408C,"5648","addq.w","#$3, a0"),
    (0x408E,"5649","addq.w","#$3, a1"),
    (0x4090,"51c8ffec","dbra","d0, $407e"),
    (0x4094,"4e75","rts",""),
    (0x4096,"303c00ff","move.w","#$ff, d0"),
    (0x409A,"3218","move.w","(a0)+, d1"),
    (0x409C,"0c41ffff","cmpi.w","#$ffff, d1"),
    (0x40A0,"67000006","beq.w","$40a8"),
    (0x40A4,"044100b8","subi.w","#$b8, d1"),
    (0x40A8,"12c1","move.b","d1, (a1)+"),
    (0x40AA,"51c8ffee","dbra","d0, $409a"),
    (0x40AE,"4e75","rts",""),
    (0x6826,"41f900c00004","lea.l","$c00004.l, a0"),
    (0x682C,"43f900c00000","lea.l","$c00000.l, a1"),
    (0x6832,"45fa0074","lea.l","$68a8(pc), a2"),
    (0x6836,"7e12","moveq","#$12, d7"),
    (0x6838,"309a","move.w","(a2)+, (a0)"),
    (0x683A,"51cffffc","dbra","d7, $6838"),
    (0x683E,"31fa006af606","move.w","$68aa(pc), $f606.w"),
    (0x6844,"7000","moveq","#$0, d0"),
    (0x6846,"23fcc000000000c00004","move.l","#$c0000000, $c00004.l"),
    (0x6850,"3e3c003f","move.w","#$3f, d7"),
    (0x6854,"3280","move.w","d0, (a1)"),
    (0x6856,"51cffffc","dbra","d7, $6854"),
    (0x685A,"4df900c00004","lea.l","$c00004.l, a6"),
    (0x6860,"3cbc8f01","move.w","#$8f01, (a6)"),
    (0x6864,"3e38f606","move.w","$f606.w, d7"),
    (0x6868,"00070010","ori.b","#$10, d7"),
    (0x686C,"3c87","move.w","d7, (a6)"),
    (0x686E,"2cbc93ff94ff","move.l","#$93ff94ff, (a6)"),
    (0x6874,"3cbc9780","move.w","#$9780, (a6)"),
    (0x6878,"2cbc40000080","move.l","#$40000080, (a6)"),
    (0x687E,"33fc000000c00000","move.w","#$0, $c00000.l"),
    (0x6886,"3e16","move.w","(a6), d7"),
    (0x6888,"02470002","andi.w","#$2, d7"),
    (0x688C,"66f8","bne.b","$6886"),
    (0x688E,"4a3900ff3f00","tst.b","$ff3f00.l"),
    (0x6894,"6608","bne.b","$689e"),
    (0x6896,"33fc000000a11100","move.w","#$0, $a11100.l"),
    (0x689E,"3cb8f606","move.w","$f606.w, (a6)"),
    (0x68A2,"3cbc8f02","move.w","#$8f02, (a6)"),
    (0x68A6,"4e75","rts",""),
    (0x3076E,"31f900ff7024efd2","move.w","$ff7024.l, $efd2.w"),
    (0x30776,"303900ff7026","move.w","$ff7026.l, d0"),
    (0x3077C,"31c0efd4","move.w","d0, $efd4.w"),
    (0x30780,"31c0efe4","move.w","d0, $efe4.w"),
    (0x30784,"11fb005af374","move.b","$307e0(pc, d0.w), $f374.w"),
    (0x3078A,"4238f375","clr.b","$f375.w"),
    (0x3078E,"31f900ff7028efd6","move.w","$ff7028.l, $efd6.w"),
    (0x30796,"31f900ff702aefd8","move.w","$ff702a.l, $efd8.w"),
    (0x3079E,"31fc0080f67c","move.w","#$80, $f67c.w"),
    (0x307A4,"31fc0080f67e","move.w","#$80, $f67e.w"),
    (0x307AA,"303900ff7034","move.w","$ff7034.l, d0"),
    (0x307B0,"41f900ff702c","lea.l","$ff702c.l, a0"),
    (0x307B6,"43fa002c","lea.l","$307e4(pc), a1"),
    (0x307BA,"3238efd4","move.w","$efd4.w, d1"),
    (0x307BE,"e349","lsl.w","#$1, d1"),
    (0x307C0,"d278efd4","add.w","$efd4.w, d1"),
    (0x307C4,"e349","lsl.w","#$1, d1"),
    (0x307C6,"d278efd4","add.w","$efd4.w, d1"),
    (0x307CA,"e349","lsl.w","#$1, d1"),
    (0x307CC,"d2c1","adda.w","d1, a1"),
    (0x307CE,"45f8f67a","lea.l","$f67a.w, a2"),
    (0x307D2,"3218","move.w","(a0)+, d1"),
    (0x307D4,"e349","lsl.w","#$1, d1"),
    (0x307D6,"34f11000","move.w","(a1, d1.w), (a2)+"),
    (0x307DA,"51c8fff6","dbra","d0, $307d2"),
    (0x307DE,"4e75","rts",""),
)
_ROWS={p:dict(bytes=b,mnemonic=m,operand=o) for p,b,m,o in _INSTRUCTIONS}
MASK,sign,operands=camera.MASK,camera.sign,camera.operands
sha,dump,keys,same,uint,exact_list=camera.sha,camera.dump,camera.keys,camera.same,camera.uint,camera.exact_list
safe_path,read_bounded,put,load_fields=camera.safe_path,camera.read_bounded,camera.put,camera.load_fields
verify_rom=camera.verify_rom


def _controls(image):
    for a,z,h in BODIES:
        if sha(image[a:z])!=h:raise ValueError('original control or cart geometry differs:'+hex(a))


class _SceneReader(initial._InitialReader):
    def __init__(self,image,selector,budget,ram_before,status):
        super().__init__(image,{0x7026:selector},budget,ram_before,status)
        self.pc=0x0528;self.rows=_ROWS

    def ea(self,s,width,update=True):
        match=re.fullmatch(r'\$([0-9a-f]+)\(pc, ([da])([0-7])\.(w|l)\)',s)
        if match:
            index=(self.D if match[2]=='d' else self.A)[int(match[3])]
            return (int(match[1],16)+sign(index,2 if match[4]=='w' else 4))&0xFFFFFFFF
        return super().ea(s,width,update)

    def run(self):
        result='instrumentation_budget_exhausted_not_CPU_stop'
        try:
            while self.pc!=0x0548:
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
            result='actual_JSR_3E54_RTS_to_0548'
        except camera._ReadBoundary as e:result=str(e)
        return dict(result=result,conditional_ram_WORDs={f'{a:04X}':v for a,v in self.frame.items()},
                    entry_call_PC=0x0528,requested_normal_return_PC=0x0548,
                    actual_final_PC=self.pc,initial_SP=self.initial_sp,final_SP=self.A[7],
                    instruction_count=len(self.steps),actual_call_return_events=self.calls,
                    ordered_data_events=self.events,final_RAM_sha256=sha(self.ram),
                    source_events=[e for e in self.events if e['kind']=='read' and 'ROM' in e['memory']],
                    CPU=False,natural_frame=False,earlier_parent_UI_helpers_closed=False,
                    budget_is_instrumentation_only=True)


def source_view(image,selector_WORD,instruction_budget=50000,RAM_before=None,
                dma_status_WORD=0,include_prefix_events=False):
    """Live true0528 prefix, full initial RAM plus FF7026.W input.

    FF7034.W is read from the complete initial RAM snapshot (zero by default).
    It is not a host copy length. No EFD4/A2/helper index is supplied.
    Original source controls/pointers remain live on the edited whole image.
    """
    camera._image(image);_controls(image)
    selector=uint(selector_WORD,65535,'complete FF7026 WORD')
    budget=uint(instruction_budget,200000,'diagnostic instruction budget')
    if budget<1:raise ValueError('positive instruction budget required')
    status=uint(dma_status_WORD,65535,'full supplied DMA status WORD')
    if type(include_prefix_events) is not bool:raise ValueError('boolean include_prefix_events required')
    if RAM_before is not None and (type(RAM_before) is not bytes or len(RAM_before)!=65536):
        raise ValueError('complete immutable64KiB RAM bytes required')
    reader=_SceneReader(image,selector,budget,RAM_before,status)
    initial_ram=bytes(reader.ram)
    view=reader.run()
    events=view.pop('ordered_data_events')
    source=view.pop('source_events')
    descriptor_events=[e for e in events if 0x3E54<=e['PC']<0x40B0]
    view.update(selector_WORD=selector,source_events=source,
        ordered_descriptor_copier_events=descriptor_events,
        ordered_data_event_count=len(events),ordered_data_events_sha256=sha(dump(events)),
        conditional_MMIO_status_reads=[e for e in events if e.get('memory')==['conditional_VDP_status']*2],
        conditional_MMIO_write_count=sum(e['kind']=='write' and any('conditional_' in m for m in e.get('memory',[])) for e in events),
        final_registers=dict(D=list(reader.D),A=list(reader.A),
            SR=(reader.SR&0xFFE0)|(int(reader.X)<<4)|(int(reader.N)<<3)|(int(reader.Z)<<2)|(int(reader.V)<<1)|int(reader.C)),
        last_explicit_SR_write=reader.SR,final_CCR=dict(X=reader.X,N=reader.N,Z=reader.Z,V=reader.V,C=reader.C),
        initial_live_FF7034_WORD=int.from_bytes(initial_ram[0x7034:0x7036],'big'),
        RAM_before_sha256=sha(initial_ram),
        RAM_frame_default='zero64KiB plus FF7026 WORD' if RAM_before is None else 'complete supplied64KiB plus FF7026 WORD',
        DMA_status_WORD=status,prefix_memoized=False,
        complete_function_recovery=False,owner='unknown',natural_domain='unknown',
        earlier_0528_UI_state_closed=False,padding_or_free_space=False,
        hardware_profile='constant status at6886; actual VDP/Z80 writes recorded conditional sinks only',
        original_hardware_equivalence='unknown',source_read_budget_is_CPU_stop=False,
        cart_profile='24bit measured MAME ROM0..200000/204000..400000; SRAM excluded; beyond4MiB unknown',
        physical_source=sorted({p for e in source for p in e['physical_addresses'] if p is not None}))
    if include_prefix_events:view['ordered_data_events']=events
    return view



def _coalesce(positions):return camera._coalesce(sorted(positions))


def _source_role(PC):
    if PC==0x30784:return 'selector_BYTE_source'
    if PC==0x307D6:return 'parameter_WORD_source'
    if PC==0x3E5A:return 'scene_descriptor_pointer_LONG'
    if 0x3E5E<=PC<=0x3FF8 and _ROWS[PC]['mnemonic']=='movea.l':
        return 'scene_descriptor_member_LONG'
    if PC in (0x402A,0x4036,0x4042,0x404E,0x405A,0x4066,0x4072,0x3E80):
        return 'fixed_count_copy_LONG_source'
    if PC in (0x407E,0x4082,0x4086):return 'officer_triple_BYTE_source'
    if PC==0x409A:return 'location_conversion_WORD_source'
    raise ValueError('unrecognized admitted original source role:'+hex(PC))


@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom)
    wanted={p for a,z in SOURCE_SPANS for p in range(a,z)}
    found={}
    for index,selector in enumerate(WITNESS_SELECTORS):
        view=source_view(rom,selector)
        for event_index,event in enumerate(view['source_events']):
            for lane,p in enumerate(event['physical_addresses']):
                if p in wanted and p not in found:
                    role=_source_role(event['PC'])
                    found[p]=dict(address=p,selector_WORD=selector,frame_index=index,
                        read_PC=event['PC'],read_width=event['width'],source_address=event['address'],
                        bus_address=event['bus_address'],physical_unit_addresses=list(event['physical_addresses']),
                        unit_BYTE_lane=lane,source_role=role,canonical_read_value=event['value'],
                        source_event_index=event_index,original_boundary=view['result'],
                        original_boundary_PC=view['actual_final_PC'],true_prefix_entry_PC=0x0528,
                        true_JSR_3E54_PC=0x0542,actual_final_SP=view['final_SP'],
                        actual_instruction_count=view['instruction_count'])
    if set(found)!=wanted or len(found)!=EDITABLE_BYTES or len(_coalesce(found))!=PHYSICAL_BLOCKS:
        raise ValueError('true scene descriptor/copier conditional source scope differs')
    return tuple(found[p] for p in sorted(found))


def physical_positions(rom):
    verify_rom(rom)
    return tuple(row['address'] for row in _catalog(rom))


def witness(rom,address):
    verify_rom(rom);address=uint(address,ROM_SIZE-1,'source BYTE')
    for row in _catalog(rom):
        if row['address']==address:return load_fields(dump(row))
    raise ValueError('outside scene descriptor source physical authority')


def metadata(rom):
    positions=physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditional_original_scene_descriptor_copier_source_fragments',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        source_union_BYTES=EDITABLE_BYTES,source_union_sha256=sha(bytes(rom[p] for p in positions)),
        physical_blocks=PHYSICAL_BLOCKS,physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in _coalesce(positions)],
        raw_baseline=dict(layout_id=LAYOUT_ID,manifest_sha256=LAYOUT_SHA256,raw_BYTES=13739,resources=101),
        roles=dict(resource='scene_descriptor_and_fixed_count_copy_source_BYTE_fragments',
            BYTE_values='all0..255 original BYTE or lanes of live complete WORD/LONG reads',
            old_typed_neighbors='whole edited image live views only; never re-emitted',
            zero_values='original literal source values, not padding or free space',
            field_roles=sorted({row['source_role'] for row in _catalog(rom)})),
        evidence=dict(prefix_entry_PC=0x0528,first_JSR_PC=0x052C,first_helper=0x6826,
            prepare_JSR_PC=0x0532,prepare_helper=0x3076E,scene_JSR_PC=0x0542,scene_helper=0x3E54,
            requested_return_PC=0x0548,selector_original_read_PC=0x30776,
            live_selector_RAM_WORD=0xFF7026,live_list_count_RAM_WORD=0xFF7034,
            raw_parameters='30784 BYTE indexed signedWORD; 307D6 WORD via14*selector WORDwrap + signed doubled live list WORD',
            descriptor='3E5A LONG via3E48+s16(LSL.W2 selector), descriptor33 live LONG members at offsets0..80',
            copying='actual DBRA fixed counts; triple BYTE1/0/2 and WORD conversion preserve original order',
            late_state='400A really clears EFD4.W; EFE4 retains original selector when reached',
            status_read_PC=0x6886,conditional_status_WORD=0,witness_selectors=list(WITNESS_SELECTORS),
            controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES],
            complete_control_RTS_guards=True,data_and_pointers_live=True),
        editing_authority='single physical fullBYTE; all old descriptors, pointers, unit neighbors and aliases are live views only',
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,functions_added=0,
        complete_function_recovery=False,independent_CPU_comparison=False,
        earlier_0528_UI_state_closed=False,natural_selector_domain='unknown',allocation_or_resource_owner='unknown',
        canonical_frames='zero64KiB RAM+FF7026 WORD; D/A0, SPFFFFFD00, SR2500 before original0528 MOVE2700; busy-clear status0/sinks',
        canonical_boundaries='each finite frame preserves actual return or first odd/SRAM/unknown/ROMwrite boundary; no fake RTS',
        edited_gameplay_safety='unknown',padding_or_free_space_claimed=False,
        instrumentation_budget_is_original_CPU_stop=False,final_semantic_high_level_recovery=False)


def _fixed_fragment(row):
    return dict(address=row['address'],source_role=row['source_role'],
        read_width=row['read_width'],unit_BYTE_lane=row['unit_BYTE_lane'])


def extract(rom):
    return dict(**metadata(rom),source_BYTEs=[dict(**_fixed_fragment(row),BYTE=rom[row['address']])
        for row in _catalog(rom)])


def blocks(rom,fields):
    fixed=metadata(rom);keys(fields,set(fixed)|{'source_BYTEs'},'scene descriptor source package')
    for k,v in fixed.items():same(fields[k],v,'package.'+k)
    values={}
    for expected,row in zip(_catalog(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'source BYTEs')):
        keys(row,set(_fixed_fragment(expected))|{'BYTE'},'source BYTE fragment')
        for k,v in _fixed_fragment(expected).items():same(row[k],v,'fragment.'+k)
        values[expected['address']]=uint(row['BYTE'],255,'complete source BYTE')
    return [dict(id=f'rom_{a:06X}_scene_descriptor_copier_source_BYTEs',start=a,end=z,
        data=bytes(values[p] for p in range(a,z)),role='conditional_scene_descriptor_copier_source_BYTE_fragments')
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
        prefixItems=[obj(dict(**{k:fixed(v) for k,v in _fixed_fragment(row).items()},
            BYTE=dict(type='integer',minimum=0,maximum=255))) for row in _catalog(rom)])
    return dict(**obj(p),**{'$schema':'https://json-schema.org/draft/2020-12/schema'},
        description='559 unique full BYTE fragments of genuine conditionally read scene descriptor/copier units; no natural domain clamp.')


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('serialized complete ROM roundtrip differs')
    validation=dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
        limitations=['Constructed complete RAM0528 scene prefix; busy-clear status and recorded write sinks are explicit conditions.',
            'Old controls and all source descriptors/pointers/neighbors are live; edits may stop earlier.',
            'No allocation/owner/natural domain/full CPU/full function or semantic high-level claim.'])
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
