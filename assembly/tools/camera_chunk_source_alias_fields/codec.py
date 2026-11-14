"""Lossless conditional camera/chunk RLE source BYTE fragments.

00110C really calls A01C. Its four live RAM WORDs, SUB/BPL/unsigned gates and
MOVEA.W produce A5; A0CC/A10C -> AF6A -> B0DE -> B106/B1DA consume the live
header, directory, container and RLE WORDs. The supplied RAM frame is conditional:
earlier 10DC UI helpers and natural state are not closed. Actual odd/unknown
bus boundaries are retained, not skipped, and no helper RTS is manufactured.
The original-opcode projection is a bounded format compatibility reader, not
a full CPU implementation or final semantic high-level gameplay module.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
from functools import lru_cache
import json
from pathlib import Path
import re
from tools.battle_deployment_parameters import codec as shared
from tools.indexed_transfer_source_alias_fields import codec as transfer

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE=0x100000
ROM_SHA256=reference_value(__name__, 'ROM_SHA256')
DEFAULT_ROM=ROOT.parent/'work/original_g5510.bin'
OUTPUT_ROOT=ROOT/'build/camera_chunk_source_alias_fields'
FORMAL_ROOT=ROOT/'analysis/camera_chunk_source_alias_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
DEFAULT_BUNDLE=FORMAL_ROOT
FORMAT='g5510-conditional-camera-column-RLE-WORD-source-BYTE-fragment-v1'
EDITABLE_BYTES, PHYSICAL_BLOCKS=403,139
MAX_JSON=8*1024*1024
MEMBERS=frozenset(('fields.json','fields.schema.json','validation.json','manifest.json'))
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
CAMERA_READ_BYTES=412
CAMERA_READ_SPANS=(
    (0xF3FD7, 0xF3FD8),
    (0xF3FD9, 0xF3FDA),
    (0xF3FDC, 0xF3FDE),
    (0xF3FE7, 0xF3FEB),
    (0xF3FED, 0xF3FEF),
    (0xF3FF0, 0xF3FF1),
    (0xF3FF7, 0xF3FF8),
    (0xF3FFE, 0xF3FFF),
    (0xF4000, 0xF4002),
    (0xF4005, 0xF4007),
    (0xF4008, 0xF4009),
    (0xF400B, 0xF400F),
    (0xF4012, 0xF4016),
    (0xF4018, 0xF4019),
    (0xF401E, 0xF4021),
    (0xF4023, 0xF4024),
    (0xF402A, 0xF402B),
    (0xF402F, 0xF4030),
    (0xF4033, 0xF4035),
    (0xF4036, 0xF4038),
    (0xF403E, 0xF403F),
    (0xF4040, 0xF4041),
    (0xF4045, 0xF4046),
    (0xF4047, 0xF4048),
    (0xF404F, 0xF4050),
    (0xF43DC, 0xF43DD),
    (0xF43DE, 0xF43E4),
    (0xF43E8, 0xF43EA),
    (0xF43EB, 0xF43EC),
    (0xF43EE, 0xF43F3),
    (0xF43F8, 0xF43FE),
    (0xF4400, 0xF4409),
    (0xF440B, 0xF440D),
    (0xF440F, 0xF4414),
    (0xF441C, 0xF441D),
    (0xF441F, 0xF4423),
    (0xF4425, 0xF4427),
    (0xF442C, 0xF442E),
    (0xF442F, 0xF4430),
    (0xF4432, 0xF4433),
    (0xF4435, 0xF4436),
    (0xF4437, 0xF443B),
    (0xF443F, 0xF4440),
    (0xF4441, 0xF4445),
    (0xF4447, 0xF4448),
    (0xF4449, 0xF4454),
    (0xF4455, 0xF4456),
    (0xF4458, 0xF445B),
    (0xF445C, 0xF445D),
    (0xF445F, 0xF4460),
    (0xF4462, 0xF4463),
    (0xF4468, 0xF446E),
    (0xF4470, 0xF4471),
    (0xF4476, 0xF447A),
    (0xF447B, 0xF447C),
    (0xF447E, 0xF4484),
    (0xF4488, 0xF4489),
    (0xF448B, 0xF448C),
    (0xF448D, 0xF448E),
    (0xF4490, 0xF449D),
    (0xF449F, 0xF44A0),
    (0xF44A3, 0xF44A4),
    (0xF44A8, 0xF44AD),
    (0xF44AE, 0xF44B0),
    (0xF44B1, 0xF44B7),
    (0xF44BD, 0xF44BE),
    (0xF44BF, 0xF44C3),
    (0xF44C5, 0xF44C7),
    (0xF44C9, 0xF44D0),
    (0xF44D2, 0xF44D3),
    (0xF44D7, 0xF44DC),
    (0xF44DE, 0xF44E3),
    (0xF44EA, 0xF44EB),
    (0xF44EC, 0xF44ED),
    (0xF44EF, 0xF44F4),
    (0xF44F8, 0xF44FF),
    (0xF4501, 0xF4502),
    (0xF4507, 0xF4508),
    (0xF450A, 0xF450B),
    (0xF450F, 0xF4511),
    (0xF4512, 0xF4516),
    (0xF4518, 0xF4519),
    (0xF4520, 0xF4523),
    (0xF4524, 0xF4526),
    (0xF4527, 0xF452A),
    (0xF452C, 0xF452D),
    (0xF4533, 0xF4534),
    (0xF4535, 0xF4537),
    (0xF453A, 0xF453B),
    (0xF453C, 0xF453D),
    (0xF4541, 0xF4546),
    (0xF4548, 0xF4549),
    (0xF4806, 0xF480F),
    (0xF4810, 0xF4812),
    (0xF4813, 0xF4816),
    (0xF4817, 0xF4819),
    (0xF481F, 0xF4827),
    (0xF482B, 0xF4836),
    (0xF4838, 0xF4839),
    (0xF483F, 0xF4841),
    (0xF4842, 0xF4843),
    (0xF4844, 0xF4846),
    (0xF484A, 0xF484B),
    (0xF484D, 0xF484E),
    (0xF4851, 0xF4858),
    (0xF485A, 0xF485F),
    (0xF4861, 0xF486E),
    (0xF486F, 0xF4870),
    (0xF4872, 0xF4873),
    (0xF4874, 0xF4882),
    (0xF4884, 0xF4887),
    (0xF488B, 0xF488C),
    (0xF488E, 0xF488F),
    (0xF4891, 0xF4892),
    (0xF4897, 0xF4899),
    (0xF489A, 0xF48A2),
    (0xF48A4, 0xF48AA),
    (0xF48AC, 0xF48B0),
    (0xF48B2, 0xF48B6),
    (0xF48BB, 0xF48BD),
    (0xF48BF, 0xF48C8),
    (0xF48CA, 0xF48D0),
    (0xF48D1, 0xF48D3),
    (0xF48D4, 0xF48D6),
    (0xF48DA, 0xF48DC),
    (0xF48DD, 0xF48DE),
    (0xF48E1, 0xF48E4),
    (0xF48E6, 0xF48E8),
    (0xF48EA, 0xF48EC),
    (0xF48ED, 0xF48F1),
    (0xF48F2, 0xF48F4),
    (0xF48F5, 0xF48F7),
    (0xF48F8, 0xF48FA),
    (0xF48FE, 0xF4900),
    (0xF4902, 0xF4904),
    (0xF4905, 0xF4907),
    (0xF4908, 0xF490F),
    (0xF4910, 0xF4912),
    (0xF4913, 0xF4916),
    (0xF491F, 0xF4921),
)
# Immutable constructed input WORDs, not serialized ROM bytes or natural states.
WITNESS_FRAMES=(
    {"F314":8,"F318":23840,"F35E":32,"F360":23872},
    {"F314":16,"F318":23680,"F35E":40,"F360":23712},
    {"F314":32,"F318":23840,"F35E":56,"F360":23872},
    {"F314":48,"F318":23840,"F35E":72,"F360":23872},
    {"F314":64,"F318":23840,"F35E":88,"F360":23872},
    {"F314":72,"F318":23680,"F35E":96,"F360":23712},
    {"F314":160,"F318":23840,"F35E":184,"F360":23872},
    {"F314":168,"F318":23680,"F35E":192,"F360":23712},
    {"F314":8,"F318":41600,"F35E":32,"F360":41632},
    {"F314":16,"F318":41760,"F35E":40,"F360":41792},
    {"F314":24,"F318":41600,"F35E":48,"F360":41632},
    {"F314":96,"F318":41760,"F35E":120,"F360":41792},
    {"F314":136,"F318":41760,"F35E":160,"F360":41792},
    {"F314":144,"F318":41600,"F35E":168,"F360":41632},
    {"F314":144,"F318":41760,"F35E":168,"F360":41792},
    {"F314":152,"F318":41600,"F35E":176,"F360":41632},
    {"F314":2144,"F318":64640,"F35E":2168,"F360":64672},
)
# These are original instruction/control guards, not additional emitted code.
BODIES=(
    (0x1A0, 0x1BC, reference_value(__name__, 'BODIES')),
    (0x110C, 0x1112, reference_value(__name__, 'BODIES_2')),
    (0xA01C, 0xA14E, reference_value(__name__, 'BODIES_3')),
    (0xAF6A, 0xB210, reference_value(__name__, 'BODIES_4')),
)
INSTRUCTIONS=(
    (0x110C, "4eb90000a01c", "jsr", "$a01c.l"),
    (0xA01C, "3038f35e", "move.w", "$f35e.w, d0"),
    (0xA020, "04400020", "subi.w", "#$20, d0"),
    (0xA024, "6a000004", "bpl.w", "$a02a"),
    (0xA028, "4240", "clr.w", "d0"),
    (0xA02A, "b078f314", "cmp.w", "$f314.w, d0"),
    (0xA02E, "64000012", "bcc.w", "$a042"),
    (0xA032, "31c0f314", "move.w", "d0, $f314.w"),
    (0xA036, "3a40", "movea.w", "d0, a5"),
    (0xA038, "4eba0092", "jsr", "$a0cc(pc)"),
    (0xA03C, "4e71", "nop", ""),
    (0xA03E, "60000034", "bra.w", "$a074"),
    (0xA042, "3038f35e", "move.w", "$f35e.w, d0"),
    (0xA046, "044000c0", "subi.w", "#$c0, d0"),
    (0xA04A, "6a000004", "bpl.w", "$a050"),
    (0xA04E, "4240", "clr.w", "d0"),
    (0xA050, "0c4003a0", "cmpi.w", "#$3a0, d0"),
    (0xA054, "63000006", "bls.w", "$a05c"),
    (0xA058, "303c03a0", "move.w", "#$3a0, d0"),
    (0xA05C, "b078f314", "cmp.w", "$f314.w, d0"),
    (0xA060, "63000012", "bls.w", "$a074"),
    (0xA064, "31c0f314", "move.w", "d0, $f314.w"),
    (0xA068, "064000e0", "addi.w", "#$e0, d0"),
    (0xA06C, "3a40", "movea.w", "d0, a5"),
    (0xA06E, "4eba005c", "jsr", "$a0cc(pc)"),
    (0xA072, "4e71", "nop", ""),
    (0xA074, "3038f360", "move.w", "$f360.w, d0"),
    (0xA078, "04400020", "subi.w", "#$20, d0"),
    (0xA07C, "6a02", "bpl.b", "$a080"),
    (0xA07E, "4240", "clr.w", "d0"),
    (0xA080, "b078f318", "cmp.w", "$f318.w, d0"),
    (0xA084, "64000012", "bcc.w", "$a098"),
    (0xA088, "31c0f318", "move.w", "d0, $f318.w"),
    (0xA08C, "3a40", "movea.w", "d0, a5"),
    (0xA08E, "4eba007c", "jsr", "$a10c(pc)"),
    (0xA092, "4e71", "nop", ""),
    (0xA094, "60000034", "bra.w", "$a0ca"),
    (0xA098, "3038f360", "move.w", "$f360.w, d0"),
    (0xA09C, "04400120", "subi.w", "#$120, d0"),
    (0xA0A0, "6a000004", "bpl.w", "$a0a6"),
    (0xA0A4, "4240", "clr.w", "d0"),
    (0xA0A6, "0c400340", "cmpi.w", "#$340, d0"),
    (0xA0AA, "63000006", "bls.w", "$a0b2"),
    (0xA0AE, "303c0340", "move.w", "#$340, d0"),
    (0xA0B2, "b078f318", "cmp.w", "$f318.w, d0"),
    (0xA0B6, "63000012", "bls.w", "$a0ca"),
    (0xA0BA, "31c0f318", "move.w", "d0, $f318.w"),
    (0xA0BE, "06400140", "addi.w", "#$140, d0"),
    (0xA0C2, "3a40", "movea.w", "d0, a5"),
    (0xA0C4, "4eba0046", "jsr", "$a10c(pc)"),
    (0xA0C8, "4e71", "nop", ""),
    (0xA0CA, "4e75", "rts", ""),
    (0xA0CC, "300d", "move.w", "a5, d0"),
    (0xA0CE, "3238f318", "move.w", "$f318.w, d1"),
    (0xA0D2, "41f90008155a", "lea.l", "$8155a.l, a0"),
    (0xA0D8, "4278f328", "clr.w", "$f328.w"),
    (0xA0DC, "4eb90000af6a", "jsr", "$af6a.l"),
    (0xA0E2, "4eb90000b054", "jsr", "$b054.l"),
    (0xA0E8, "0040e000", "ori.w", "#$e000, d0"),
    (0xA0EC, "41f8d100", "lea.l", "$d100.w, a0"),
    (0xA0F0, "d0f8f31a", "adda.w", "$f31a.w, a0"),
    (0xA0F4, "323c0029", "move.w", "#$29, d1"),
    (0xA0F8, "30c1", "move.w", "d1, (a0)+"),
    (0xA0FA, "30c0", "move.w", "d0, (a0)+"),
    (0xA0FC, "4eb90000b06e", "jsr", "$b06e.l"),
    (0xA102, "4250", "clr.w", "(a0)"),
    (0xA104, "06780056f31a", "addi.w", "#$56, $f31a.w"),
    (0xA10A, "4e75", "rts", ""),
    (0xA10C, "3038f314", "move.w", "$f314.w, d0"),
    (0xA110, "320d", "move.w", "a5, d1"),
    (0xA112, "41f90008155a", "lea.l", "$8155a.l, a0"),
    (0xA118, "31fc0001f328", "move.w", "#$1, $f328.w"),
    (0xA11E, "4eb90000af6a", "jsr", "$af6a.l"),
    (0xA124, "4eb90000b054", "jsr", "$b054.l"),
    (0xA12A, "0040e000", "ori.w", "#$e000, d0"),
    (0xA12E, "41f8d100", "lea.l", "$d100.w, a0"),
    (0xA132, "d0f8f31a", "adda.w", "$f31a.w, a0"),
    (0xA136, "323c801d", "move.w", "#$801d, d1"),
    (0xA13A, "30c1", "move.w", "d1, (a0)+"),
    (0xA13C, "30c0", "move.w", "d0, (a0)+"),
    (0xA13E, "4eb90000b0b2", "jsr", "$b0b2.l"),
    (0xA144, "4250", "clr.w", "(a0)"),
    (0xA146, "0678003ef31a", "addi.w", "#$3e, $f31a.w"),
    (0xA14C, "4e75", "rts", ""),
    (0xAF6A, "e648", "lsr.w", "#$3, d0"),
    (0xAF6C, "e649", "lsr.w", "#$3, d1"),
    (0xAF6E, "48e7c000", "movem.l", "d0-d1, -(a7)"),
    (0xAF72, "18280002", "move.b", "$2(a0), d4"),
    (0xAF76, "4884", "ext.w", "d4"),
    (0xAF78, "48c0", "ext.l", "d0"),
    (0xAF7A, "80c4", "divu.w", "d4, d0"),
    (0xAF7C, "2400", "move.l", "d0, d2"),
    (0xAF7E, "4842", "swap", "d2"),
    (0xAF80, "1a280003", "move.b", "$3(a0), d5"),
    (0xAF84, "4885", "ext.w", "d5"),
    (0xAF86, "48c1", "ext.l", "d1"),
    (0xAF88, "82c5", "divu.w", "d5, d1"),
    (0xAF8A, "2601", "move.l", "d1, d3"),
    (0xAF8C, "4843", "swap", "d3"),
    (0xAF8E, "28680004", "movea.l", "$4(a0), a4"),
    (0xAF92, "c0d0", "mulu.w", "(a0), d0"),
    (0xAF94, "d041", "add.w", "d1, d0"),
    (0xAF96, "e348", "lsl.w", "#$1, d0"),
    (0xAF98, "32300008", "move.w", "$8(a0, d0.w), d1"),
    (0xAF9C, "0c41ffff", "cmpi.w", "#$ffff, d1"),
    (0xAFA0, "6608", "bne.b", "$afaa"),
    (0xAFA2, "227cffffffff", "movea.l", "#$ffffffff, a1"),
    (0xAFA8, "600a", "bra.b", "$afb4"),
    (0xAFAA, "224c", "movea.l", "a4, a1"),
    (0xAFAC, "02810000ffff", "andi.l", "#$ffff, d1"),
    (0xAFB2, "d3c1", "adda.l", "d1, a1"),
    (0xAFB4, "4a78f328", "tst.w", "$f328.w"),
    (0xAFB8, "6656", "bne.b", "$b010"),
    (0xAFBA, "3230000a", "move.w", "$a(a0, d0.w), d1"),
    (0xAFBE, "6a08", "bpl.b", "$afc8"),
    (0xAFC0, "247cffffffff", "movea.l", "#$ffffffff, a2"),
    (0xAFC6, "600a", "bra.b", "$afd2"),
    (0xAFC8, "244c", "movea.l", "a4, a2"),
    (0xAFCA, "02810000ffff", "andi.l", "#$ffff, d1"),
    (0xAFD0, "d5c1", "adda.l", "d1, a2"),
    (0xAFD2, "3230000c", "move.w", "$c(a0, d0.w), d1"),
    (0xAFD6, "0c41ffff", "cmpi.w", "#$ffff, d1"),
    (0xAFDA, "6608", "bne.b", "$afe4"),
    (0xAFDC, "267cffffffff", "movea.l", "#$ffffffff, a3"),
    (0xAFE2, "600a", "bra.b", "$afee"),
    (0xAFE4, "264c", "movea.l", "a4, a3"),
    (0xAFE6, "02810000ffff", "andi.l", "#$ffff, d1"),
    (0xAFEC, "d7c1", "adda.l", "d1, a3"),
    (0xAFEE, "3230000e", "move.w", "$e(a0, d0.w), d1"),
    (0xAFF2, "0c41ffff", "cmpi.w", "#$ffff, d1"),
    (0xAFF6, "6608", "bne.b", "$b000"),
    (0xAFF8, "2a7cffffffff", "movea.l", "#$ffffffff, a5"),
    (0xAFFE, "600a", "bra.b", "$b00a"),
    (0xB000, "2a4c", "movea.l", "a4, a5"),
    (0xB002, "02810000ffff", "andi.l", "#$ffff, d1"),
    (0xB008, "dbc1", "adda.l", "d1, a5"),
    (0xB00A, "4cdf0003", "movem.l", "(a7)+, d0-d1"),
    (0xB00E, "4e75", "rts", ""),
    (0xB010, "d050", "add.w", "(a0), d0"),
    (0xB012, "d050", "add.w", "(a0), d0"),
    (0xB014, "32300008", "move.w", "$8(a0, d0.w), d1"),
    (0xB018, "0c41ffff", "cmpi.w", "#$ffff, d1"),
    (0xB01C, "6608", "bne.b", "$b026"),
    (0xB01E, "247cffffffff", "movea.l", "#$ffffffff, a2"),
    (0xB024, "600a", "bra.b", "$b030"),
    (0xB026, "244c", "movea.l", "a4, a2"),
    (0xB028, "02810000ffff", "andi.l", "#$ffff, d1"),
    (0xB02E, "d5c1", "adda.l", "d1, a2"),
    (0xB030, "d050", "add.w", "(a0), d0"),
    (0xB032, "d050", "add.w", "(a0), d0"),
    (0xB034, "32300008", "move.w", "$8(a0, d0.w), d1"),
    (0xB038, "0c41ffff", "cmpi.w", "#$ffff, d1"),
    (0xB03C, "6600000a", "bne.w", "$b048"),
    (0xB040, "267cffffffff", "movea.l", "#$ffffffff, a3"),
    (0xB046, "600a", "bra.b", "$b052"),
    (0xB048, "264c", "movea.l", "a4, a3"),
    (0xB04A, "02810000ffff", "andi.l", "#$ffff, d1"),
    (0xB050, "d7c1", "adda.l", "d1, a3"),
    (0xB052, "60b6", "bra.b", "$b00a"),
    (0xB054, "48c0", "ext.l", "d0"),
    (0xB056, "80fc0040", "divu.w", "#$40, d0"),
    (0xB05A, "4840", "swap", "d0"),
    (0xB05C, "c0fc0040", "mulu.w", "#$40, d0"),
    (0xB060, "48c1", "ext.l", "d1"),
    (0xB062, "82fc0040", "divu.w", "#$40, d1"),
    (0xB066, "4841", "swap", "d1"),
    (0xB068, "d041", "add.w", "d1, d0"),
    (0xB06A, "e348", "lsl.w", "#$1, d0"),
    (0xB06C, "4e75", "rts", ""),
    (0xB06E, "616e", "bsr.b", "$b0de"),
    (0xB070, "61000094", "bsr.w", "$b106"),
    (0xB074, "3005", "move.w", "d5, d0"),
    (0xB076, "9043", "sub.w", "d3, d0"),
    (0xB078, "30c6", "move.w", "d6, (a0)+"),
    (0xB07A, "5341", "subq.w", "#$1, d1"),
    (0xB07C, "6730", "beq.b", "$b0ae"),
    (0xB07E, "5340", "subq.w", "#$1, d0"),
    (0xB080, "671a", "beq.b", "$b09c"),
    (0xB082, "0c8700010000", "cmpi.l", "#$10000, d7"),
    (0xB088, "6406", "bcc.b", "$b090"),
    (0xB08A, "51cfffec", "dbra", "d7, $b078"),
    (0xB08E, "6006", "bra.b", "$b096"),
    (0xB090, "5246", "addq.w", "#$1, d6"),
    (0xB092, "51cfffe4", "dbra", "d7, $b078"),
    (0xB096, "61000142", "bsr.w", "$b1da"),
    (0xB09A, "60dc", "bra.b", "$b078"),
    (0xB09C, "224a", "movea.l", "a2, a1"),
    (0xB09E, "244b", "movea.l", "a3, a2"),
    (0xB0A0, "264d", "movea.l", "a5, a3"),
    (0xB0A2, "4243", "clr.w", "d3"),
    (0xB0A4, "3005", "move.w", "d5, d0"),
    (0xB0A6, "6136", "bsr.b", "$b0de"),
    (0xB0A8, "61000130", "bsr.w", "$b1da"),
    (0xB0AC, "60ca", "bra.b", "$b078"),
    (0xB0AE, "4250", "clr.w", "(a0)"),
    (0xB0B0, "4e75", "rts", ""),
    (0xB0B2, "02417fff", "andi.w", "#$7fff, d1"),
    (0xB0B6, "6126", "bsr.b", "$b0de"),
    (0xB0B8, "614c", "bsr.b", "$b106"),
    (0xB0BA, "30c6", "move.w", "d6, (a0)+"),
    (0xB0BC, "5341", "subq.w", "#$1, d1"),
    (0xB0BE, "671a", "beq.b", "$b0da"),
    (0xB0C0, "5242", "addq.w", "#$1, d2"),
    (0xB0C2, "b444", "cmp.w", "d4, d2"),
    (0xB0C4, "6706", "beq.b", "$b0cc"),
    (0xB0C6, "6116", "bsr.b", "$b0de"),
    (0xB0C8, "613c", "bsr.b", "$b106"),
    (0xB0CA, "60ee", "bra.b", "$b0ba"),
    (0xB0CC, "4242", "clr.w", "d2"),
    (0xB0CE, "224a", "movea.l", "a2, a1"),
    (0xB0D0, "244b", "movea.l", "a3, a2"),
    (0xB0D2, "3005", "move.w", "d5, d0"),
    (0xB0D4, "6108", "bsr.b", "$b0de"),
    (0xB0D6, "612e", "bsr.b", "$b106"),
    (0xB0D8, "60e0", "bra.b", "$b0ba"),
    (0xB0DA, "4250", "clr.w", "(a0)"),
    (0xB0DC, "4e75", "rts", ""),
    (0xB0DE, "48e7a080", "movem.l", "d0/d2/a0, -(a7)"),
    (0xB0E2, "2009", "move.l", "a1, d0"),
    (0xB0E4, "6a04", "bpl.b", "$b0ea"),
    (0xB0E6, "2849", "movea.l", "a1, a4"),
    (0xB0E8, "6016", "bra.b", "$b100"),
    (0xB0EA, "2051", "movea.l", "(a1), a0"),
    (0xB0EC, "3c05", "move.w", "d5, d6"),
    (0xB0EE, "e24e", "lsr.w", "#$1, d6"),
    (0xB0F0, "b646", "cmp.w", "d6, d3"),
    (0xB0F2, "6502", "bcs.b", "$b0f6"),
    (0xB0F4, "5242", "addq.w", "#$1, d2"),
    (0xB0F6, "e34a", "lsl.w", "#$1, d2"),
    (0xB0F8, "34312004", "move.w", "$4(a1, d2.w), d2"),
    (0xB0FC, "49f02000", "lea.l", "(a0, d2.w), a4"),
    (0xB100, "4cdf0105", "movem.l", "(a7)+, d0/d2/a0"),
    (0xB104, "4e75", "rts", ""),
    (0xB106, "2e0c", "move.l", "a4, d7"),
    (0xB108, "6b50", "bmi.b", "$b15a"),
    (0xB10A, "3c05", "move.w", "d5, d6"),
    (0xB10C, "e24e", "lsr.w", "#$1, d6"),
    (0xB10E, "b646", "cmp.w", "d6, d3"),
    (0xB110, "644e", "bcc.b", "$b160"),
    (0xB112, "3e03", "move.w", "d3, d7"),
    (0xB114, "5247", "addq.w", "#$1, d7"),
    (0xB116, "3c1c", "move.w", "(a4)+, d6"),
    (0xB118, "3006", "move.w", "d6, d0"),
    (0xB11A, "024007ff", "andi.w", "#$7ff, d0"),
    (0xB11E, "044006ff", "subi.w", "#$6ff, d0"),
    (0xB122, "6408", "bcc.b", "$b12c"),
    (0xB124, "5347", "subq.w", "#$1, d7"),
    (0xB126, "66ee", "bne.b", "$b116"),
    (0xB128, "7e00", "moveq", "#$0, d7"),
    (0xB12A, "4e75", "rts", ""),
    (0xB12C, "3c1c", "move.w", "(a4)+, d6"),
    (0xB12E, "02870000ffff", "andi.l", "#$ffff, d7"),
    (0xB134, "08000007", "btst.b", "#$7, d0"),
    (0xB138, "670a", "beq.b", "$b144"),
    (0xB13A, "08800007", "bclr.b", "#$7, d0"),
    (0xB13E, "008700010000", "ori.l", "#$10000, d7"),
    (0xB144, "9e40", "sub.w", "d0, d7"),
    (0xB146, "62ce", "bhi.b", "$b116"),
    (0xB148, "4447", "neg.w", "d7"),
    (0xB14A, "0c8700010000", "cmpi.l", "#$10000, d7"),
    (0xB150, "6506", "bcs.b", "$b158"),
    (0xB152, "9047", "sub.w", "d7, d0"),
    (0xB154, "5340", "subq.w", "#$1, d0"),
    (0xB156, "dc40", "add.w", "d0, d6"),
    (0xB158, "4e75", "rts", ""),
    (0xB15A, "4246", "clr.w", "d6"),
    (0xB15C, "7e40", "moveq", "#$40, d7"),
    (0xB15E, "4e75", "rts", ""),
    (0xB160, "3e05", "move.w", "d5, d7"),
    (0xB162, "5347", "subq.w", "#$1, d7"),
    (0xB164, "554c", "subq.w", "#$2, a4"),
    (0xB166, "be43", "cmp.w", "d3, d7"),
    (0xB168, "6712", "beq.b", "$b17c"),
    (0xB16A, "302cfffe", "move.w", "-$2(a4), d0"),
    (0xB16E, "024007ff", "andi.w", "#$7ff, d0"),
    (0xB172, "04400700", "subi.w", "#$700, d0"),
    (0xB176, "641c", "bcc.b", "$b194"),
    (0xB178, "5347", "subq.w", "#$1, d7"),
    (0xB17A, "60e8", "bra.b", "$b164"),
    (0xB17C, "4287", "clr.l", "d7"),
    (0xB17E, "3c14", "move.w", "(a4), d6"),
    (0xB180, "302cfffe", "move.w", "-$2(a4), d0"),
    (0xB184, "024007ff", "andi.w", "#$7ff, d0"),
    (0xB188, "04400780", "subi.w", "#$780, d0"),
    (0xB18C, "6502", "bcs.b", "$b190"),
    (0xB18E, "dc40", "add.w", "d0, d6"),
    (0xB190, "544c", "addq.w", "#$2, a4"),
    (0xB192, "4e75", "rts", ""),
    (0xB194, "02870000ffff", "andi.l", "#$ffff, d7"),
    (0xB19A, "08000007", "btst.b", "#$7, d0"),
    (0xB19E, "670a", "beq.b", "$b1aa"),
    (0xB1A0, "08800007", "bclr.b", "#$7, d0"),
    (0xB1A4, "008700010000", "ori.l", "#$10000, d7"),
    (0xB1AA, "9e40", "sub.w", "d0, d7"),
    (0xB1AC, "be43", "cmp.w", "d3, d7"),
    (0xB1AE, "6306", "bls.b", "$b1b6"),
    (0xB1B0, "554c", "subq.w", "#$2, a4"),
    (0xB1B2, "5347", "subq.w", "#$1, d7"),
    (0xB1B4, "60ae", "bra.b", "$b164"),
    (0xB1B6, "48e71000", "movem.l", "d3, -(a7)"),
    (0xB1BA, "9647", "sub.w", "d7, d3"),
    (0xB1BC, "3c00", "move.w", "d0, d6"),
    (0xB1BE, "9043", "sub.w", "d3, d0"),
    (0xB1C0, "3e00", "move.w", "d0, d7"),
    (0xB1C2, "4240", "clr.w", "d0"),
    (0xB1C4, "0c8700010000", "cmpi.l", "#$10000, d7"),
    (0xB1CA, "6504", "bcs.b", "$b1d0"),
    (0xB1CC, "9c47", "sub.w", "d7, d6"),
    (0xB1CE, "3006", "move.w", "d6, d0"),
    (0xB1D0, "d05c", "add.w", "(a4)+, d0"),
    (0xB1D2, "3c00", "move.w", "d0, d6"),
    (0xB1D4, "4cdf0008", "movem.l", "(a7)+, d3"),
    (0xB1D8, "4e75", "rts", ""),
    (0xB1DA, "2e09", "move.l", "a1, d7"),
    (0xB1DC, "6b2c", "bmi.b", "$b20a"),
    (0xB1DE, "3c1c", "move.w", "(a4)+, d6"),
    (0xB1E0, "3e06", "move.w", "d6, d7"),
    (0xB1E2, "024707ff", "andi.w", "#$7ff, d7"),
    (0xB1E6, "04470700", "subi.w", "#$700, d7"),
    (0xB1EA, "6404", "bcc.b", "$b1f0"),
    (0xB1EC, "4287", "clr.l", "d7"),
    (0xB1EE, "4e75", "rts", ""),
    (0xB1F0, "02870000ffff", "andi.l", "#$ffff, d7"),
    (0xB1F6, "08070007", "btst.b", "#$7, d7"),
    (0xB1FA, "670a", "beq.b", "$b206"),
    (0xB1FC, "08870007", "bclr.b", "#$7, d7"),
    (0xB200, "008700010000", "ori.l", "#$10000, d7"),
    (0xB206, "3c1c", "move.w", "(a4)+, d6"),
    (0xB208, "4e75", "rts", ""),
    (0xB20A, "4246", "clr.w", "d6"),
    (0xB20C, "7e40", "moveq", "#$40, d7"),
    (0xB20E, "4e75", "rts", ""),
)
_ROWS={pc:dict(bytes=raw,mnemonic=mnemonic,operand=operand) for pc,raw,mnemonic,operand in INSTRUCTIONS}
sha,dump=shared.sha,shared.dump
keys,same,uint,exact_list=shared.keys,shared.same,shared.uint,shared.exact_list
safe_path,read_bounded,put,load_fields=shared.safe_path,shared.read_bounded,shared.put,shared.load_fields


def _image(image):
    if type(image) is not bytes or len(image)!=ROM_SIZE:
        raise ValueError('complete immutable1MiB image bytes required')


def _controls(image):
    for a,z,h in BODIES:
        if sha(image[a:z])!=h:
            raise ValueError('original caller/controller/helper or mapper geometry changed')


def verify_rom(rom):
    _image(rom)
    if sha(rom)!=ROM_SHA256:
        raise ValueError('canonical original BIN SHA256 differs')
    _controls(rom)


MASK={1:255,2:65535,4:0xFFFFFFFF}


def sign(v,width):
    v &= MASK[width]
    return v-(1<<(width*8)) if v&(1<<(width*8-1)) else v


def operands(s):
    result=[];start=0;depth=0
    for i,c in enumerate(s):
        if c=='(':depth+=1
        elif c==')':depth-=1
        elif c==',' and not depth:
            result.append(s[start:i].strip());start=i+1
    result.append(s[start:].strip())
    return result


class _ReadBoundary(ValueError):pass


class _CameraReader:
    def __init__(self,image,rows,frame,instruction_budget=200000,ram_before=None):
        self.image=image;self.rows=rows;self.D=[0]*8;self.A=[0]*8
        self.ram=bytearray(65536) if ram_before is None else bytearray(ram_before);self.events=[];self.steps=[];self.calls=[]
        self.C=self.V=self.N=self.Z=False;self.X=False
        self.A[7]=0xFFFFFD00;self.initial_sp=self.A[7]
        for addr,value in frame.items():self.ram[addr:addr+2]=(value&65535).to_bytes(2,'big')
        self.frame=dict(frame);self.pc=0x110C;self.budget=instruction_budget

    def read(self,address,width,role='data'):
        address&=0xFFFFFFFF;bus=address&0xFFFFFF
        if width>1 and bus&1:raise _ReadBoundary('original_address_error:'+hex(address))
        physical=[];data=bytearray();memory=[]
        for a in range(bus,bus+width):
            if 0xFF0000<=a<0x1000000:
                data.append(self.ram[a-0xFF0000]);memory.append('RAM');physical.append(None)
            elif a<0x400000 and not 0x200000<=a<0x204000:
                p=a&0xFFFFF;data.append(self.image[p]);memory.append('ROM');physical.append(p)
            else:raise _ReadBoundary('unmodelled_original_bus:'+hex(a))
        value=int.from_bytes(data,'big')
        self.events.append(dict(kind='read',PC=self.pc,address=address,bus_address=bus,width=width,
                                bytes=data.hex(),value=value,memory=memory,physical_addresses=physical,role=role))
        return value

    def write(self,address,width,value,role='data'):
        address&=0xFFFFFFFF;bus=address&0xFFFFFF
        if width>1 and bus&1:raise _ReadBoundary('original_address_error:'+hex(address))
        if not 0xFF0000<=bus<=0x1000000-width:raise _ReadBoundary('unmodelled_original_write:'+hex(bus))
        data=(value&MASK[width]).to_bytes(width,'big')
        self.ram[bus-0xFF0000:bus-0xFF0000+width]=data
        self.events.append(dict(kind='write',PC=self.pc,address=address,bus_address=bus,width=width,
                                bytes=data.hex(),value=value&MASK[width],role=role,memory=['RAM']*width))

    def ea(self,s,width,update=True):
        m=re.fullmatch(r'\(a([0-7])\)\+',s)
        if m:
            n=int(m[1]);address=self.A[n]
            if update:self.A[n]=(address+(2 if n==7 and width==1 else width))&0xFFFFFFFF
            return address
        m=re.fullmatch(r'-\(a([0-7])\)',s)
        if m:
            n=int(m[1]);address=(self.A[n]-(2 if n==7 and width==1 else width))&0xFFFFFFFF
            if update:self.A[n]=address
            return address
        m=re.fullmatch(r'\(a([0-7])\)',s)
        if m:return self.A[int(m[1])]
        m=re.fullmatch(r'(-?\$[0-9a-f]+)?\(a([0-7])(?:, ([da])([0-7])\.(w|l))?\)',s)
        if m:
            displacement=0 if m[1] is None else int(m[1].replace('$','0x'),0)
            address=self.A[int(m[2])]+displacement
            if m[3]:
                index=(self.D if m[3]=='d' else self.A)[int(m[4])]
                address+=sign(index,2) if m[5]=='w' else sign(index,4)
            return address&0xFFFFFFFF
        m=re.fullmatch(r'\$([0-9a-f]+)\.(w|l)',s)
        if m:
            v=int(m[1],16);return (sign(v,2) if m[2]=='w' else v)&0xFFFFFFFF
        raise _ReadBoundary('unsupported_original_EA:'+s)

    def get(self,s,width):
        if s.startswith('#$'):return int(s[2:],16)&MASK[width]
        m=re.fullmatch(r'([da])([0-7])',s)
        if m:return (self.D if m[1]=='d' else self.A)[int(m[2])]&MASK[width]
        return self.read(self.ea(s,width),width)

    def put(self,s,width,value):
        m=re.fullmatch(r'([da])([0-7])',s)
        if m:
            regs=self.D if m[1]=='d' else self.A;n=int(m[2])
            regs[n]=((regs[n]&~MASK[width])|(value&MASK[width]))&0xFFFFFFFF
        else:self.write(self.ea(s,width),width,value)

    def logic(self,value,width):
        v=value&MASK[width];self.N=sign(v,width)<0;self.Z=v==0;self.V=self.C=False

    def calc(self,left,right,width,subtract=False):
        mask=MASK[width];left&=mask;right&=mask
        result=(left-right if subtract else left+right)&mask
        self.C=left<right if subtract else left+right>mask
        self.X=self.C;self.N=sign(result,width)<0;self.Z=result==0
        top=1<<(width*8-1)
        self.V=bool((left^right)&(left^result)&top) if subtract else bool((~(left^right))&(left^result)&top)
        return result

    def target(self,s):
        m=re.match(r'\$([0-9a-f]+)',s)
        if not m:raise _ReadBoundary('unsupported_original_target:'+s)
        return int(m[1],16)

    def condition(self,name):
        return {'bra':True,'beq':self.Z,'bne':not self.Z,'bcs':self.C,'bcc':not self.C,
                'bhi':not self.C and not self.Z,'bls':self.C or self.Z,
                'bpl':not self.N,'bmi':self.N,'bge':self.N==self.V,'blt':self.N!=self.V,
                'bgt':not self.Z and self.N==self.V,'ble':self.Z or self.N!=self.V}[name]

    def movem_regs(self,s):
        result=[]
        for part in s.split('/'):
            if '-' in part:
                a,b=part.split('-');assert a[0]==b[0]
                result.extend((a[0],n) for n in range(int(a[1:]),int(b[1:])+1))
            else:result.append((part[0],int(part[1:])))
        return result

    def run(self):
        result='instrumentation_budget_exhausted_not_CPU_stop'
        try:
            while self.pc!=0x1112:
                if len(self.steps)>=self.budget:raise _ReadBoundary(result)
                if self.pc not in self.rows:raise _ReadBoundary('not_pinned_original_PC:'+hex(self.pc))
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
                    value=self.get(ops[0],width);self.put(ops[1],width,value);self.logic(value,width)
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
                    else:raise _ReadBoundary('unsupported_original_MOVEM:'+row['operand'])
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
                        if not src:raise _ReadBoundary('original_DIVU_zero')
                        q,r=divmod(self.D[n],src)
                        if q>65535:self.V=True;self.C=False
                        else:self.D[n]=(r<<16)|q;self.logic(q,2)
                elif name in ('btst','bclr'):
                    bit=self.get(ops[0],4);w=4 if re.fullmatch(r'd[0-7]',ops[1]) else 1
                    bit%=32 if w==4 else 8;value=self.get(ops[1],w);self.Z=not bool(value&(1<<bit))
                    if name=='bclr':self.put(ops[1],w,value&~(1<<bit))
                else:raise _ReadBoundary('unsupported_original_opcode:'+row['mnemonic']+' '+row['operand'])
                self.pc=nextpc
            result='actual_JSR_A01C_RTS_to_1112'
        except _ReadBoundary as e:result=str(e)
        return dict(result=result,conditional_ram_WORDs={f'{a:04X}':v for a,v in self.frame.items()},
                    entry_call_PC=0x110C,requested_normal_return_PC=0x1112,
                    actual_final_PC=self.pc,initial_SP=self.initial_sp,final_SP=self.A[7],
                    instruction_count=len(self.steps),instructions=self.steps,actual_call_return_events=self.calls,
                    ordered_data_events=self.events,final_RAM_sha256=sha(self.ram),
                    source_events=[e for e in self.events if e['kind']=='read' and 'ROM' in e['memory']],
                    CPU=False,natural_frame=False,earlier_10DC_UI_helpers_closed=False,
                    budget_is_instrumentation_only=True)



def source_view(image, camera_WORDs, instruction_budget=200000, RAM_before=None):
    """Pure live original prefix from true110C JSR, not supplied A5/index.

    RAM_before is a complete64KiB constructed/live RAM snapshot, or zero RAM.
    Only the four explicit camera/current-edge WORDs replace those RAM fields.
    Odd data addresses, unmeasured bus accesses and instrumentation budgets
    preserve their actual stop: none is turned into an original CPU return.
    """
    _image(image);_controls(image)
    keys(camera_WORDs,{'F35E','F314','F318','F360'},'complete camera WORD frame')
    frame={int(k,16):uint(v,65535,'camera.'+k) for k,v in camera_WORDs.items()}
    budget=uint(instruction_budget,200000,'diagnostic original-instruction budget')
    if budget<1:raise ValueError('positive diagnostic instruction budget required')
    if RAM_before is not None and (type(RAM_before) is not bytes or len(RAM_before)!=65536):
        raise ValueError('complete immutable64KiB RAM bytes required')
    reader=_CameraReader(image,_ROWS,frame,budget,RAM_before)
    initial_ram=bytes(reader.ram)
    view=reader.run()
    view.update(complete_function_recovery=False,natural_domain='unknown',owner='unknown',
        padding_or_free_space=False,source_read_budget_is_CPU_stop=False,
        RAM_frame_default='zero64KiB plus four supplied WORDs' if RAM_before is None else 'complete supplied64KiB plus four WORDs',
        RAM_before_sha256=sha(initial_ram),physical_source=sorted({p for e in view['source_events'] for p in e['physical_addresses'] if p is not None}),
        original_JSR_PC=0x110C,original_normal_return_PC=0x1112,
        cart_profile='24bit bus; measured MAME0.289 ROM0..200000/204000..400000; SRAM aperture excluded; outside4M unknown')
    return view


def _coalesce(positions):
    result=[]
    for p in positions:
        if result and result[-1][1]==p:result[-1][1]=p+1
        else:result.append([p,p+1])
    return tuple(tuple(x) for x in result)


@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom)
    wanted={p for a,z in CAMERA_READ_SPANS for p in range(a,z)}
    if len(wanted)!=CAMERA_READ_BYTES:raise ValueError('camera original unique scope differs')
    found={}
    for index,frame in enumerate(WITNESS_FRAMES):
        view=source_view(rom,frame)
        for event_index,event in enumerate(view['source_events']):
            for lane,p in enumerate(event['physical_addresses']):
                if p in wanted and p not in found:
                    if event['width']!=2 or event['PC'] not in (0xB116,0xB16A,0xB180,0xB1DE):
                        raise ValueError('original RLE WORD read role differs')
                    found[p]=dict(address=p,frame_index=index,camera_WORDs=dict(frame),
                        read_PC=event['PC'],read_width=2,source_address=event['address'],
                        bus_address=event['bus_address'],physical_WORD_addresses=list(event['physical_addresses']),
                        WORD_BYTE_lane=lane,canonical_read_WORD=event['value'],
                        source_event_index=event_index,original_boundary=view['result'],
                        original_boundary_PC=view['actual_final_PC'],
                        true_JSR_PC=0x110C,earlier_10DC_UI_helpers_closed=False)
    if set(found)!=wanted:raise ValueError('original true camera prefix coverage differs')
    # Incoming transfer authority is unique: its9 overlap BYTEs stay read-only
    # views here. This neither changes nor prematurely accepts that other pack.
    other=set(transfer.physical_positions(rom))
    if len(wanted&other)!=9:raise ValueError('shared physical authority overlap differs')
    owned=sorted(wanted-other)
    if len(owned)!=EDITABLE_BYTES or len(_coalesce(owned))!=PHYSICAL_BLOCKS:
        raise ValueError('camera unique physical authority extent differs')
    return tuple(found[p] for p in owned)


def physical_positions(rom):
    verify_rom(rom)
    return tuple(row['address'] for row in _catalog(rom))


def witness(rom,address):
    verify_rom(rom);address=uint(address,ROM_SIZE-1,'source physical BYTE')
    for row in _catalog(rom):
        if row['address']==address:return load_fields(dump(row))
    raise ValueError('outside unique camera physical authority')


def metadata(rom):
    positions=physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditional_original_RLE_WORD_source_fragments',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        source_union_BYTES=EDITABLE_BYTES,source_union_sha256=sha(bytes(rom[p] for p in positions)),
        physical_blocks=PHYSICAL_BLOCKS,physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in _coalesce(positions)],
        raw_baseline=dict(layout_id=LAYOUT_ID,manifest_sha256=LAYOUT_SHA256,raw_BYTES=14239,
            original_camera_read_BYTES=412,shared_transfer_BYTEs_excluded=9,
            shared_authority='tools.indexed_transfer_source_alias_fields.physical_positions(rom)',
            incoming_transfer_and_camera_batch_accepted=False),
        roles=dict(resource='conditional_world_column_RLE_WORD_source_BYTE_fragments',
            original_WORD_read_PCs=[0xB116,0xB16A,0xB180,0xB1DE],
            BYTE_values='all0..255; stored as high/low fragment of a live complete WORD',
            old_typed_WORD_neighbors='live read view only; never emitted again',
            zero_WORD='literal tileWORD0 under original low11 grammar, not padding'),
        evidence=dict(caller_JSR_PC=0x110C,controller_entry=0xA01C,normal_return_PC=0x1112,
            horizontal_entry=0xA0CC,A0CA_role='RTS, not helper entry',vertical_entry=0xA10C,
            producer_RAM_WORDs=['F35E','F314','F318','F360'],producer='SUB.W/BPL and unsigned camera gates -> MOVEA.W A5',
            header=0x8155A,live_directory_lookup=0xAF6A,live_column_lookup=0xB0DE,
            header_fields='stride WORD; width/height BYTE sign-extended WORD; base LONG',
            container_fields='live BE32 base plus signed BE16 column offset',
            RLE_source='complete WORD low11 literal/first6FF/run/increment controls retained',
            witness_frames=[dict(f) for f in WITNESS_FRAMES],
            controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES],
            code_and_original_geometry_guards=True,source_header_directory_columns_not_cached=True),
        cart_profile=dict(bus_bits=24,measured_ROM_regions=[[0,0x200000],[0x204000,0x400000]],
            SRAM_not_ROM=[0x200000,0x204000],outside4M='unknown reject',original_hardware_equivalence='unknown',
            measurement_dump_dependency=False),
        editing_authority='single physical source BYTE; aliases and whole WORDs are only live views',
        owner_bytes_added=0,natural_domains_added=0,complete_domains_added=0,functions_added=0,
        complete_function_recovery=False,independent_CPU_comparison=False,
        original_earlier_10DC_UI_prefix='unknown; not executed by this conditional frame',
        canonical_reading_frames='all stop at actual odd/unknown bus boundaries; no synthetic RTS',
        natural_camera_domain='unknown',allocation_or_atlas_owner='unknown',
        padding_or_free_space_claimed=False,edited_gameplay_safety='unknown',
        instrumentation_budget_is_original_CPU_stop=False,
        final_semantic_high_level_recovery=False)


def extract(rom):
    return dict(**metadata(rom),source_BYTEs=[dict(address=p,RLE_WORD_address=p&~1,
        WORD_BYTE_lane='high' if not p&1 else 'low',BYTE=rom[p]) for p in physical_positions(rom)])


def blocks(rom,fields):
    fixed=metadata(rom);keys(fields,set(fixed)|{'source_BYTEs'},'camera source package')
    for k,v in fixed.items():same(fields[k],v,'package.'+k)
    values={}
    for p,row in zip(physical_positions(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'source BYTEs')):
        keys(row,{'address','RLE_WORD_address','WORD_BYTE_lane','BYTE'},'source BYTE fragment')
        for k,v in dict(address=p,RLE_WORD_address=p&~1,WORD_BYTE_lane='high' if not p&1 else 'low').items():
            same(row[k],v,'fragment.'+k)
        values[p]=uint(row['BYTE'],255,'complete source BYTE bits')
    return [dict(id=f'rom_{a:06X}_camera_column_RLE_source_BYTEs',start=a,end=z,
        data=bytes(values[p] for p in range(a,z)),role='conditional_camera_column_RLE_WORD_source_BYTE_fragments')
        for a,z in _coalesce(physical_positions(rom))]


def rebuild(rom,fields):
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
        description='403 unique full BYTE fragments of original live RLE WORDs; no natural camera or CPU catalog clamp.')


def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('serialized complete ROM roundtrip differs')
    validation=dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
        limitations=['Conditional true110C camera/controller prefix; earlier10DC UI helpers unknown.',
            'Source controls and old typed neighbours remain live, including9 transfer aliases.',
            'Edited runs can stop earlier; never force original source positions or fake RTS.',
            'No owner/allocation, natural domain, full CPU, full scene or final high-level claim.'])
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
