"""Lossless source BYTEs from a conditional real scene-object motion caller.

The original 3D810 call builds its object list before the live 40C94 selection
and 416F8 motion branch. Both motion and subsequent ordinary sprite reads stay
live. This source projection is not a recovered gameplay/CPU implementation.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
from functools import lru_cache
import json
from pathlib import Path
import re
from tools.scene_object_source_alias_fields import codec as obj

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE,ROM_SHA256,DEFAULT_ROM=obj.ROM_SIZE,obj.ROM_SHA256,obj.DEFAULT_ROM
OUTPUT_ROOT=ROOT/'build/object_motion_source_alias_fields'
FORMAL_ROOT=ROOT/'analysis/object_motion_source_alias_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
FORMAT='g5510-conditional-object-motion-compact-sprite-source-BYTEs-v1'
MAX_JSON=16*1024*1024
MEMBERS=obj.MEMBERS
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
EDITABLE_BYTES,PHYSICAL_BLOCKS=1343,490
WITNESS_STATES=(13165,10039,10110,14122,10089,4295,9964,9997,8311,14800,5634,9391,8077,3450,)
SOURCE_SPANS=(
    (0xCCA1C,0xCCA5A),
    (0xF303C,0xF3042),
    (0xF3044,0xF3052),
    (0xF3053,0xF3055),
    (0xF3056,0xF3057),
    (0xF3059,0xF305F),
    (0xF3060,0xF3062),
    (0xF3063,0xF3067),
    (0xF3069,0xF3072),
    (0xF3073,0xF3075),
    (0xF3076,0xF3077),
    (0xF307E,0xF3080),
    (0xF3081,0xF3083),
    (0xF3085,0xF3089),
    (0xF308A,0xF308C),
    (0xF308F,0xF3091),
    (0xF3093,0xF309B),
    (0xF309D,0xF309E),
    (0xF309F,0xF30A0),
    (0xF30A2,0xF30A8),
    (0xF30AA,0xF30AE),
    (0xF30AF,0xF30B1),
    (0xF30B2,0xF30BB),
    (0xF30BD,0xF30C2),
    (0xF30C4,0xF30C6),
    (0xF30C9,0xF30CA),
    (0xF30CB,0xF30CD),
    (0xF30CE,0xF30D2),
    (0xF30D5,0xF30D7),
    (0xF30DC,0xF30DF),
    (0xF30E2,0xF30E7),
    (0xF30E9,0xF30EA),
    (0xF30EB,0xF30F7),
    (0xF30F9,0xF30FC),
    (0xF3100,0xF3107),
    (0xF3109,0xF310E),
    (0xF310F,0xF3111),
    (0xF3112,0xF3113),
    (0xF3115,0xF311D),
    (0xF3124,0xF3126),
    (0xF3128,0xF3129),
    (0xF312B,0xF3130),
    (0xF3132,0xF314E),
    (0xF314F,0xF3151),
    (0xF3152,0xF3157),
    (0xF315B,0xF315E),
    (0xF3161,0xF3165),
    (0xF316B,0xF316F),
    (0xF3172,0xF317C),
    (0xF32DF,0xF32E0),
    (0xF32E4,0xF32E8),
    (0xF32EA,0xF32EB),
    (0xF32ED,0xF32EF),
    (0xF32F3,0xF32F7),
    (0xF3306,0xF330B),
    (0xF330D,0xF330F),
    (0xF331B,0xF331E),
    (0xF3325,0xF3327),
    (0xF3328,0xF3329),
    (0xF332B,0xF332C),
    (0xF332D,0xF3330),
    (0xF3333,0xF3335),
    (0xF333D,0xF333E),
    (0xF3340,0xF3341),
    (0xF334D,0xF334F),
    (0xF3353,0xF3355),
    (0xF3357,0xF3359),
    (0xF335A,0xF335D),
    (0xF335E,0xF335F),
    (0xF3363,0xF3365),
    (0xF3367,0xF3368),
    (0xF336B,0xF3370),
    (0xF3374,0xF3377),
    (0xF337B,0xF337E),
    (0xF3394,0xF3396),
    (0xF339E,0xF339F),
    (0xF33A4,0xF33A6),
    (0xF33AB,0xF33AE),
    (0xF33B6,0xF33B7),
    (0xF33B8,0xF33B9),
    (0xF33BD,0xF33BF),
    (0xF33C3,0xF33C6),
    (0xF33DC,0xF33DE),
    (0xF33E8,0xF33E9),
    (0xF33EB,0xF33EC),
    (0xF33F3,0xF33F5),
    (0xF3483,0xF3485),
    (0xF349B,0xF349F),
    (0xF34AF,0xF34B0),
    (0xF34B3,0xF34B4),
    (0xF34B5,0xF34B6),
    (0xF34BD,0xF34BF),
    (0xF34C5,0xF34C7),
    (0xF34CD,0xF34CF),
    (0xF34D3,0xF34D4),
    (0xF34E3,0xF34E6),
    (0xF34F3,0xF34F4),
    (0xF34F9,0xF34FA),
    (0xF34FC,0xF34FE),
    (0xF3500,0xF3501),
    (0xF3504,0xF3508),
    (0xF350D,0xF350F),
    (0xF3513,0xF3515),
    (0xF3517,0xF351A),
    (0xF351E,0xF351F),
    (0xF3524,0xF3525),
    (0xF4052,0xF4053),
    (0xF4054,0xF4055),
    (0xF4057,0xF4058),
    (0xF405A,0xF405C),
    (0xF405F,0xF4060),
    (0xF4065,0xF4066),
    (0xF4067,0xF406A),
    (0xF406D,0xF406F),
    (0xF4071,0xF4072),
    (0xF4075,0xF4076),
    (0xF4078,0xF407A),
    (0xF407D,0xF4080),
    (0xF4083,0xF4085),
    (0xF4087,0xF4088),
    (0xF40A0,0xF40A2),
    (0xF40AF,0xF40B1),
    (0xF40BF,0xF40C0),
    (0xF40C2,0xF40C6),
    (0xF40C8,0xF40CA),
    (0xF40CD,0xF40D0),
    (0xF40D9,0xF40DA),
    (0xF40E3,0xF40E4),
    (0xF40EA,0xF40EC),
    (0xF40F5,0xF40F6),
    (0xF40FF,0xF4100),
    (0xF4108,0xF410B),
    (0xF410E,0xF4110),
    (0xF4112,0xF4116),
    (0xF411B,0xF411C),
    (0xF4126,0xF4128),
    (0xF412C,0xF412D),
    (0xF412F,0xF4132),
    (0xF4134,0xF4135),
    (0xF4138,0xF4139),
    (0xF413F,0xF4141),
    (0xF4145,0xF4146),
    (0xF4153,0xF4155),
    (0xF4158,0xF415C),
    (0xF415F,0xF4160),
    (0xF4164,0xF4166),
    (0xF4167,0xF4168),
    (0xF416A,0xF416B),
    (0xF4172,0xF4174),
    (0xF4178,0xF4179),
    (0xF417A,0xF417C),
    (0xF427C,0xF427D),
    (0xF427E,0xF4281),
    (0xF4282,0xF4284),
    (0xF4288,0xF4289),
    (0xF428E,0xF428F),
    (0xF429F,0xF42A1),
    (0xF42A2,0xF42A4),
    (0xF42A6,0xF42A7),
    (0xF42A8,0xF42A9),
    (0xF42AA,0xF42AC),
    (0xF42AD,0xF42AE),
    (0xF42BE,0xF42BF),
    (0xF42C5,0xF42CA),
    (0xF42CC,0xF42CD),
    (0xF42CE,0xF42CF),
    (0xF42D1,0xF42D2),
    (0xF42DD,0xF42DE),
    (0xF42E2,0xF42E3),
    (0xF42E9,0xF42ED),
    (0xF42F1,0xF42F2),
    (0xF42F4,0xF42F6),
    (0xF430D,0xF4316),
    (0xF4318,0xF431A),
    (0xF431E,0xF431F),
    (0xF4326,0xF4328),
    (0xF4329,0xF432B),
    (0xF432D,0xF432E),
    (0xF4330,0xF4335),
    (0xF4337,0xF4338),
    (0xF433A,0xF433F),
    (0xF4343,0xF4346),
    (0xF4348,0xF4349),
    (0xF434D,0xF434F),
    (0xF4354,0xF4356),
    (0xF4358,0xF4363),
    (0xF4365,0xF4368),
    (0xF436D,0xF436E),
    (0xF4370,0xF4374),
    (0xF4377,0xF4379),
    (0xF437B,0xF437C),
    (0xF437D,0xF437E),
    (0xF4381,0xF4388),
    (0xF438A,0xF4392),
    (0xF4395,0xF4398),
    (0xF439A,0xF439D),
    (0xF439E,0xF43A0),
    (0xF43A2,0xF43AC),
    (0xF43AE,0xF43C0),
    (0xF43C1,0xF43C3),
    (0xF43C4,0xF43C5),
    (0xF43C7,0xF43CF),
    (0xF43D6,0xF43DA),
    (0xF43DB,0xF43DC),
    (0xF454A,0xF454B),
    (0xF454D,0xF454E),
    (0xF4550,0xF4551),
    (0xF4553,0xF4554),
    (0xF455A,0xF455D),
    (0xF455E,0xF4560),
    (0xF4566,0xF4568),
    (0xF4569,0xF456C),
    (0xF456E,0xF456F),
    (0xF4571,0xF4573),
    (0xF4577,0xF4578),
    (0xF457A,0xF457C),
    (0xF4580,0xF4582),
    (0xF4583,0xF4584),
    (0xF458E,0xF458F),
    (0xF4591,0xF4594),
    (0xF4A24,0xF4A26),
    (0xF4A28,0xF4A2A),
    (0xF4A2C,0xF4A31),
    (0xF4A33,0xF4A39),
    (0xF4A40,0xF4A42),
    (0xF4A43,0xF4A47),
    (0xF4A4A,0xF4A4B),
    (0xF4A55,0xF4A57),
    (0xF4A58,0xF4A5F),
    (0xF4A66,0xF4A67),
    (0xF4A69,0xF4A71),
    (0xF4A72,0xF4A74),
    (0xF4A75,0xF4A76),
    (0xF4A78,0xF4A7F),
    (0xF4A81,0xF4A83),
    (0xF4A85,0xF4A88),
    (0xF4A8C,0xF4A8E),
    (0xF4A90,0xF4A92),
    (0xF4A94,0xF4A95),
    (0xF4A9F,0xF4AA7),
    (0xF4AAC,0xF4ABA),
    (0xF4ABC,0xF4ABD),
    (0xF4ABF,0xF4AC0),
    (0xF4AC2,0xF4AC6),
    (0xF4AC7,0xF4AC9),
    (0xF4ACB,0xF4AD1),
    (0xF4AD2,0xF4AD4),
    (0xF4AD6,0xF4AD8),
    (0xF4ADB,0xF4ADC),
    (0xF4AE5,0xF4AE6),
    (0xF4AE8,0xF4AEE),
    (0xF4AEF,0xF4AF1),
    (0xF4AF5,0xF4AFC),
    (0xF4AFE,0xF4B00),
    (0xF4B05,0xF4B06),
    (0xF4B0B,0xF4B0F),
    (0xF4B11,0xF4B1A),
    (0xF4B1C,0xF4B1E),
    (0xF4B24,0xF4B25),
    (0xF4B29,0xF4B2A),
    (0xF4B2C,0xF4B2D),
    (0xF4B31,0xF4B37),
    (0xF4B3D,0xF4B43),
    (0xF4B44,0xF4B46),
    (0xF4B48,0xF4B49),
    (0xF4B55,0xF4B5C),
    (0xF4B5E,0xF4B5F),
    (0xF4B61,0xF4B64),
    (0xF4B74,0xF4B75),
    (0xF4B79,0xF4B7A),
    (0xF4B7C,0xF4B7F),
    (0xF4B81,0xF4B82),
    (0xF4B84,0xF4B85),
    (0xF4B87,0xF4B8B),
    (0xF4B8E,0xF4B90),
    (0xF4B94,0xF4B95),
    (0xF4B9E,0xF4BA3),
    (0xF4BA4,0xF4BA6),
    (0xF4BA7,0xF4BA9),
    (0xF4BAA,0xF4BAB),
    (0xF4BAC,0xF4BAE),
    (0xF4BB4,0xF4BB5),
    (0xF4BB7,0xF4BB8),
    (0xF4BBA,0xF4BBC),
    (0xF4BBD,0xF4BBE),
    (0xF4BC2,0xF4BC3),
    (0xF4BC5,0xF4BC6),
    (0xF4BC7,0xF4BC8),
    (0xF4BCA,0xF4BCC),
    (0xF4BCD,0xF4BCF),
    (0xF4BD0,0xF4BD1),
    (0xF4BD3,0xF4BD5),
    (0xF4BD6,0xF4BDE),
    (0xF4BE1,0xF4BE2),
    (0xF4BE6,0xF4BEC),
    (0xF4BEE,0xF4BEF),
    (0xF4BF1,0xF4BF4),
    (0xF4BFB,0xF4BFC),
    (0xF4BFE,0xF4BFF),
    (0xF4C04,0xF4C06),
    (0xF4C0C,0xF4C0D),
    (0xF4C13,0xF4C15),
    (0xF4C19,0xF4C1B),
    (0xF4C1D,0xF4C27),
    (0xF4C29,0xF4C2B),
    (0xF4C2D,0xF4C3C),
    (0xF4C42,0xF4C43),
    (0xF4C44,0xF4C45),
    (0xF4C4B,0xF4C4D),
    (0xF4C4E,0xF4C4F),
    (0xF4C55,0xF4C57),
    (0xF4F2F,0xF4F30),
    (0xF4F34,0xF4F35),
    (0xF4F40,0xF4F43),
    (0xF4F44,0xF4F46),
    (0xF4F49,0xF4F4A),
    (0xF4F4B,0xF4F4F),
    (0xF4F53,0xF4F55),
    (0xF4F5C,0xF4F5D),
    (0xF4F5F,0xF4F60),
    (0xF4F64,0xF4F65),
    (0xF4F66,0xF4F68),
    (0xF4F69,0xF4F6A),
    (0xF4F70,0xF4F74),
    (0xF4F7D,0xF4F7E),
    (0xF4F87,0xF4F89),
    (0xF4F8B,0xF4F8C),
    (0xF4F92,0xF4F97),
    (0xF4F9B,0xF4F9C),
    (0xF4F9D,0xF4F9E),
    (0xF4FA0,0xF4FA1),
    (0xF4FA3,0xF4FA6),
    (0xF4FAA,0xF4FAC),
    (0xF4FAD,0xF4FAE),
    (0xF4FB2,0xF4FB4),
    (0xF4FB7,0xF4FC0),
    (0xF4FC4,0xF4FC7),
    (0xF4FC9,0xF4FCA),
    (0xF4FD1,0xF4FD3),
    (0xF4FD4,0xF4FD5),
    (0xF4FDD,0xF4FDE),
    (0xF4FE2,0xF4FE5),
    (0xF4FEA,0xF4FEE),
    (0xF4FF0,0xF4FF1),
    (0xF4FF4,0xF4FF6),
    (0xF4FF7,0xF4FF9),
    (0xF4FFC,0xF5009),
    (0xF500B,0xF500F),
    (0xF5017,0xF5019),
    (0xF501B,0xF501C),
    (0xF501D,0xF501E),
    (0xF5024,0xF5025),
    (0xF5027,0xF5028),
    (0xF5029,0xF5036),
    (0xF503A,0xF503B),
    (0xF503D,0xF503E),
    (0xF5042,0xF5044),
    (0xF5045,0xF5050),
    (0xF5052,0xF5056),
    (0xF5057,0xF5059),
    (0xF505A,0xF505F),
    (0xF5061,0xF5065),
    (0xF60ED,0xF60F0),
    (0xF60F4,0xF60F5),
    (0xF60F8,0xF60FD),
    (0xF6185,0xF6186),
    (0xF6188,0xF618A),
    (0xF618C,0xF618E),
    (0xF6192,0xF6193),
    (0xF6197,0xF6198),
    (0xF619C,0xF619D),
    (0xF619F,0xF61A4),
    (0xF61A5,0xF61A7),
    (0xF61AC,0xF61AD),
    (0xF61B4,0xF61B6),
    (0xF61BC,0xF61C0),
    (0xF61CD,0xF61D0),
    (0xF61D3,0xF61D4),
    (0xF61D6,0xF61D9),
    (0xF61DE,0xF61DF),
    (0xF61E1,0xF61E4),
    (0xF61E6,0xF61E7),
    (0xF61E8,0xF61EA),
    (0xF61EC,0xF61ED),
    (0xF61F3,0xF61F4),
    (0xF61F6,0xF61F7),
    (0xF61F9,0xF61FA),
    (0xF61FE,0xF61FF),
    (0xF6202,0xF6204),
    (0xF6206,0xF6207),
    (0xF6210,0xF6212),
    (0xF6214,0xF6217),
    (0xF6219,0xF621A),
    (0xF621D,0xF621F),
    (0xF6222,0xF6223),
    (0xF6224,0xF6225),
    (0xF6228,0xF6229),
    (0xF622A,0xF622B),
    (0xF622F,0xF6231),
    (0xF6232,0xF6234),
    (0xF6237,0xF6238),
    (0xF623A,0xF623B),
    (0xF623C,0xF623D),
    (0xF623F,0xF6240),
    (0xF6244,0xF6246),
    (0xF6247,0xF6249),
    (0xF624A,0xF624B),
    (0xF624C,0xF624E),
    (0xF6253,0xF6259),
    (0xF625B,0xF6260),
    (0xF6263,0xF6264),
    (0xF6268,0xF6269),
    (0xF626B,0xF626C),
    (0xF626E,0xF626F),
    (0xF6273,0xF6275),
    (0xF6276,0xF6279),
    (0xF627D,0xF627F),
    (0xF6284,0xF6285),
    (0xF6288,0xF628A),
    (0xF628B,0xF628C),
    (0xF6291,0xF6294),
    (0xF6296,0xF6298),
    (0xF629A,0xF62A0),
    (0xF62A1,0xF62A2),
    (0xF62A6,0xF62A8),
    (0xF62A9,0xF62AA),
    (0xF62AE,0xF62AF),
    (0xF62B2,0xF62B3),
    (0xF62B9,0xF62BB),
    (0xF62BD,0xF62C0),
    (0xF62D2,0xF62D4),
    (0xF62D6,0xF62D7),
    (0xF62D8,0xF62DA),
    (0xF62DC,0xF62DE),
    (0xF62E0,0xF62E2),
    (0xF62E3,0xF62E9),
    (0xF62ED,0xF62EE),
    (0xF62EF,0xF62F1),
    (0xF62F3,0xF62F4),
    (0xF62F9,0xF62FA),
    (0xF62FC,0xF62FD),
    (0xF62FF,0xF6300),
    (0xF6304,0xF6306),
    (0xF630D,0xF630E),
    (0xF6318,0xF6319),
    (0xF631F,0xF6320),
    (0xF6322,0xF6324),
    (0xF6326,0xF6328),
    (0xF632B,0xF6330),
    (0xF6331,0xF6332),
    (0xF6336,0xF633A),
    (0xF633D,0xF633E),
    (0xF6340,0xF6341),
    (0xF6342,0xF6343),
    (0xF6348,0xF634F),
    (0xF635C,0xF635D),
    (0xF635F,0xF6360),
    (0xF636C,0xF636E),
    (0xF6371,0xF6372),
    (0xF6375,0xF6379),
    (0xF637B,0xF6385),
    (0xF6389,0xF6396),
    (0xF63A0,0xF63A2),
    (0xF63A3,0xF63A4),
    (0xF63AE,0xF63AF),
    (0xF63B3,0xF63B4),
    (0xF63B8,0xF63B9),
    (0xF63BB,0xF63BC),
    (0xF63BE,0xF63C1),
    (0xF63C3,0xF63C4),
    (0xF63C7,0xF63D9),
    (0xF63DB,0xF63DF),
    (0xF63EA,0xF63EB),
    (0xF63F3,0xF63F5),
    (0xF63F7,0xF63F8),
    (0xF63FC,0xF63FD),
    (0xF6401,0xF6402),
    (0xF6405,0xF6406),
    (0xF6407,0xF6408),
    (0xF640A,0xF640B),
    (0xF640D,0xF640E),
    (0xF6410,0xF6412),
    (0xF6414,0xF641A),
    (0xF641F,0xF6420),
    (0xF6421,0xF6423),
    (0xF6424,0xF6427),
    (0xF642A,0xF642C),
    (0xF6430,0xF6434),
    (0xF643A,0xF643B),
    (0xF643E,0xF643F),
)
NEW_BODIES=(
    (0x40C94,0x40D7C,reference_value(__name__, 'NEW_BODIES')),
    (0x416F8,0x417CE,reference_value(__name__, 'NEW_BODIES_2')),
)
BODIES=obj.BODIES+NEW_BODIES
_ADDITIONAL_INSTRUCTIONS=(
    (0x40C94,"bdfcffff826a","cmpa.l","#$ffff826a, a6"),
    (0x40C9A,"6510","bcs.b","$40cac"),
    (0x40C9C,"4bf8826a","lea.l","$826a.w, a5"),
    (0x40CA0,"0c780002814c","cmpi.w","#$2, $814c.w"),
    (0x40CA6,"660000d2","bne.w","$40d7a"),
    (0x40CAA,"600e","bra.b","$40cba"),
    (0x40CAC,"4bf8816a","lea.l","$816a.w, a5"),
    (0x40CB0,"0c780001814c","cmpi.w","#$1, $814c.w"),
    (0x40CB6,"660000c2","bne.w","$40d7a"),
    (0x40CBA,"3016","move.w","(a6), d0"),
    (0x40CBC,"0240007f","andi.w","#$7f, d0"),
    (0x40CC0,"b078814e","cmp.w","$814e.w, d0"),
    (0x40CC4,"660000b4","bne.w","$40d7a"),
    (0x40CC8,"7000","moveq","#$0, d0"),
    (0x40CCA,"30388150","move.w","$8150.w, d0"),
    (0x40CCE,"e940","asl.w","#$4, d0"),
    (0x40CD0,"3040","movea.w","d0, a0"),
    (0x40CD2,"d1cd","adda.l","a5, a0"),
    (0x40CD4,"b1ce","cmpa.l","a6, a0"),
    (0x40CD6,"660000a2","bne.w","$40d7a"),
    (0x40CDA,"4a788152","tst.w","$8152.w"),
    (0x40CDE,"6664","bne.b","$40d44"),
    (0x40CE0,"31fc00018152","move.w","#$1, $8152.w"),
    (0x40CE6,"0c6e02000002","cmpi.w","#$200, $2(a6)"),
    (0x40CEC,"64000088","bcc.w","$40d76"),
    (0x40CF0,"4ebaaa30","jsr","$3b722(pc)"),
    (0x40CF4,"02400003","andi.w","#$3, d0"),
    (0x40CF8,"6704","beq.b","$40cfe"),
    (0x40CFA,"610004d0","bsr.w","$411cc"),
    (0x40CFE,"61000028","bsr.w","$40d28"),
    (0x40D02,"31c0815a","move.w","d0, $815a.w"),
    (0x40D06,"e540","asl.w","#$2, d0"),
    (0x40D08,"4efb0002","jmp","$40d0c(pc, d0.w)"),
    (0x40D0C,"6000006e","bra.w","$40d7c"),
    (0x40D10,"600000e4","bra.w","$40df6"),
    (0x40D14,"60000150","bra.w","$40e66"),
    (0x40D18,"600001a6","bra.w","$40ec0"),
    (0x40D1C,"6000ff8e","bra.w","$40cac"),
    (0x40D20,"600001f8","bra.w","$40f1a"),
    (0x40D24,"600003ea","bra.w","$41110"),
    (0x40D28,"7000","moveq","#$0, d0"),
    (0x40D2A,"102e0001","move.b","$1(a6), d0"),
    (0x40D2E,"bdfcffff826a","cmpa.l","#$ffff826a, a6"),
    (0x40D34,"6502","bcs.b","$40d38"),
    (0x40D36,"5840","addq.w","#$4, d0"),
    (0x40D38,"e340","asl.w","#$1, d0"),
    (0x40D3A,"41f8812a","lea.l","$812a.w, a0"),
    (0x40D3E,"30300000","move.w","(a0, d0.w), d0"),
    (0x40D42,"4e75","rts",""),
    (0x40D44,"3038815a","move.w","$815a.w, d0"),
    (0x40D48,"e540","asl.w","#$2, d0"),
    (0x40D4A,"4efb0002","jmp","$40d4e(pc, d0.w)"),
    (0x40D4E,"60000066","bra.w","$40db6"),
    (0x40D52,"600000de","bra.w","$40e32"),
    (0x40D56,"60000134","bra.w","$40e8c"),
    (0x40D5A,"6000018a","bra.w","$40ee6"),
    (0x40D5E,"60000016","bra.w","$40d76"),
    (0x40D62,"6000021a","bra.w","$40f7e"),
    (0x40D66,"60000216","bra.w","$40f7e"),
    (0x40D6A,"60000212","bra.w","$40f7e"),
    (0x40D6E,"600007b4","bra.w","$41524"),
    (0x40D72,"60000984","bra.w","$416f8"),
    (0x416F8,"2a78815c","movea.l","$815c.w, a5"),
    (0x416FC,"30388164","move.w","$8164.w, d0"),
    (0x41700,"b06d0002","cmp.w","$2(a5), d0"),
    (0x41704,"6662","bne.b","$41768"),
    (0x41706,"30388166","move.w","$8166.w, d0"),
    (0x4170A,"b06d0004","cmp.w","$4(a5), d0"),
    (0x4170E,"6658","bne.b","$41768"),
    (0x41710,"4a788168","tst.w","$8168.w"),
    (0x41714,"660a","bne.b","$41720"),
    (0x41716,"303c00aa","move.w","#$aa, d0"),
    (0x4171A,"4eb90000808a","jsr","$808a.l"),
    (0x41720,"52788168","addq.w","#$1, $8168.w"),
    (0x41724,"30388168","move.w","$8168.w, d0"),
    (0x41728,"7210","moveq","#$10, d1"),
    (0x4172A,"4a78840a","tst.w","$840a.w"),
    (0x4172E,"6702","beq.b","$41732"),
    (0x41730,"7210","moveq","#$10, d1"),
    (0x41732,"b041","cmp.w","d1, d0"),
    (0x41734,"6500fed2","bcs.w","$41608"),
    (0x41738,"302e000e","move.w","$e(a6), d0"),
    (0x4173C,"322e000c","move.w","$c(a6), d1"),
    (0x41740,"c2c0","mulu.w","d0, d1"),
    (0x41742,"82fc0064","divu.w","#$64, d1"),
    (0x41746,"48e74000","movem.l","d1, -(a7)"),
    (0x4174A,"4eba9fd6","jsr","$3b722(pc)"),
    (0x4174E,"0240001f","andi.w","#$1f, d0"),
    (0x41752,"06400050","addi.w","#$50, d0"),
    (0x41756,"4cdf0002","movem.l","(a7)+, d1"),
    (0x4175A,"c2c0","mulu.w","d0, d1"),
    (0x4175C,"82fc0064","divu.w","#$64, d1"),
    (0x41760,"6100ff6c","bsr.w","$416ce"),
    (0x41764,"6000fdd6","bra.w","$4153c"),
    (0x41768,"7004","moveq","#$4, d0"),
    (0x4176A,"4a78840a","tst.w","$840a.w"),
    (0x4176E,"6702","beq.b","$41772"),
    (0x41770,"7008","moveq","#$8, d0"),
    (0x41772,"4a6e0008","tst.w","$8(a6)"),
    (0x41776,"66000008","bne.w","$41780"),
    (0x4177A,"d1788164","add.w","d0, $8164.w"),
    (0x4177E,"602e","bra.b","$417ae"),
    (0x41780,"0c6e00010008","cmpi.w","#$1, $8(a6)"),
    (0x41786,"66000008","bne.w","$41790"),
    (0x4178A,"91788164","sub.w","d0, $8164.w"),
    (0x4178E,"601e","bra.b","$417ae"),
    (0x41790,"0c6e00020008","cmpi.w","#$2, $8(a6)"),
    (0x41796,"66000008","bne.w","$417a0"),
    (0x4179A,"d1788166","add.w","d0, $8166.w"),
    (0x4179E,"600e","bra.b","$417ae"),
    (0x417A0,"0c6e00030008","cmpi.w","#$3, $8(a6)"),
    (0x417A6,"66000006","bne.w","$417ae"),
    (0x417AA,"91788166","sub.w","d0, $8166.w"),
    (0x417AE,"302e0008","move.w","$8(a6), d0"),
    (0x417B2,"e540","asl.w","#$2, d0"),
    (0x417B4,"207b0018","movea.l","$417ce(pc, d0.w), a0"),
    (0x417B8,"30388164","move.w","$8164.w, d0"),
    (0x417BC,"32388166","move.w","$8166.w, d1"),
    (0x417C0,"343c0004","move.w","#$4, d2"),
    (0x417C4,"7600","moveq","#$0, d3"),
    (0x417C6,"383c0300","move.w","#$300, d4"),
    (0x417CA,"4efa9970","jmp","$3b13c(pc)"),
    (0x40D76,"42788152","clr.w","$8152.w"),
    (0x40D7A,"4e75","rts",""),
)
_ROWS={**obj._ROWS,**{p:dict(bytes=b,mnemonic=m,operand=o) for p,b,m,o in _ADDITIONAL_INSTRUCTIONS}}
camera=obj.camera
sha,dump,keys,same,uint,exact_list=obj.sha,obj.dump,obj.keys,obj.same,obj.uint,obj.exact_list
safe_path,read_bounded,put,load_fields=obj.safe_path,obj.read_bounded,obj.put,obj.load_fields
verify_rom=obj.verify_rom
ROLES=obj.ROLES

def default_RAM():
    """Complete disclosed conditional initial RAM, not a natural state claim."""
    ram=bytearray(65536)
    for address,value in ((0x816A,0x8000),(0x814C,1),(0x8152,1),(0x815A,9),(0x826C,1)):
        ram[address:address+2]=value.to_bytes(2,'big')
    ram[0x815C:0x8160]=(0xFFFF826A).to_bytes(4,'big')
    return bytes(ram)

def _controls(image):
    for a,z,h in BODIES:
        if sha(image[a:z])!=h:
            raise ValueError('original object/motion/SAT control or cart geometry differs:'+hex(a))

class _MotionReader(obj._ObjectReader):
    """Reuse the reviewed operand engine; add original indexed JMP addressing."""
    def __init__(self,image,state,budget,ram_before):
        super().__init__(image,state,budget,default_RAM() if ram_before is None else ram_before)
        self.rows=_ROWS

    def target(self,s):
        if re.fullmatch(r'\$[0-9a-f]+\(pc, [da][0-7]\.[wl]\)',s):
            return self.ea(s,4,False)
        return super().target(s)

def source_view(image,state_WORD,instruction_budget=50000,RAM_before=None,include_prefix_events=False):
    """Execute real 3D810 call with complete RAM and full object+8 WORD.

    FF8172.W is set once in the initial snapshot. No source pointer, A6,
    object list, helper index, fake return, IRQ or mid-execution repair is used.
    Original gates may bypass motion, hit unpinned helpers, or fault normally.
    """
    camera._image(image);_controls(image)
    state=uint(state_WORD,65535,'complete object+8 WORD')
    budget=uint(instruction_budget,200000,'instrumentation instruction budget')
    if budget<1:raise ValueError('positive instruction budget required')
    if type(include_prefix_events) is not bool:raise ValueError('boolean event inclusion required')
    if RAM_before is not None and (type(RAM_before) is not bytes or len(RAM_before)!=65536):
        raise ValueError('complete immutable64KiB RAM bytes required')
    reader=_MotionReader(image,state,budget,RAM_before);before=bytes(reader.ram)
    view=reader.run();events=view.pop('ordered_data_events');source=view.pop('source_events')
    stage=None
    for event in source:
        if event['PC']==0x417B4:stage='motion_417B4_directory'
        elif event['PC'] in (0x40460,0x4046C,0x404AA):stage='subsequent_ordinary_404AA_directory'
        event['selection_stage']=stage
    physical=sorted({p for e in source for p in e['physical_addresses'] if p is not None})
    ccr=dict(X=reader.X,N=reader.N,Z=reader.Z,V=reader.V,C=reader.C)
    view.update(state_WORD=state,source_events=source,physical_source=physical,
        managed_source_reached=sorted(set(physical)&{p for a,z in SOURCE_SPANS for p in range(a,z)}),
        ordered_data_event_count=len(events),ordered_data_events_sha256=sha(dump(events)),
        RAM_before_sha256=sha(before),prefix_memoized=False,
        RAM_frame_default='completezero64KiB + FF816A.W8000/814C.W1/8152.W1/815A.W9/815C.LFFFF826A/826C.W1 + FF8172.W input'
            if RAM_before is None else 'complete supplied64KiB + FF8172.W input',
        final_registers=dict(D=list(reader.D),A=list(reader.A),
            SR=(reader.SR&0xFFE0)|(int(reader.X)<<4)|(int(reader.N)<<3)|(int(reader.Z)<<2)|(int(reader.V)<<1)|int(reader.C)),
        last_explicit_SR_write=reader.SR,final_CCR=ccr,
        complete_function_recovery=False,allocation_owner='unknown',natural_domain='unknown',
        natural_815C_pointer_and_fullWORD_state='unknown',
        earlier_3D810_battle_state_closed=False,original_hardware_equivalence='unknown',
        source_read_budget_is_CPU_stop=False,padding_or_free_space=False,
        cart_profile='measured MAME24bit: ROMmirror0..200000/204000..400000; SRAMexcluded; beyond4MiBunknown',
        operand_diagnostics_not_complete_exception_frame=True)
    if include_prefix_events:view['ordered_data_events']=events
    return view

def _coalesce(positions):return camera._coalesce(sorted(positions))

@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom);wanted={p for a,z in SOURCE_SPANS for p in range(a,z)};found={}
    for state in WITNESS_STATES:
        view=source_view(rom,state)
        if view['result']!='actual_JSR_4033C_RTS_to_3D814' or view['final_SP']!=0xFFFFFD00:
            raise ValueError('canonical conditional object caller no longer returns')
        for order,event in enumerate(view['source_events']):
            for lane,p in enumerate(event['physical_addresses']):
                if p in wanted and p not in found:
                    if event['PC'] not in ROLES or event['width']!=1:
                        raise ValueError('unknown admitted sprite source role')
                    found[p]=dict(address=p,state_WORD=state,read_PC=event['PC'],
                        source_role=ROLES[event['PC']],selection_stage=event['selection_stage'],
                        read_width=1,source_address=event['address'],bus_address=event['bus_address'],
                        unit_BYTE_lane=lane,source_event_index=order,canonical_read_value=event['value'],
                        true_caller_PC=0x3D810,generated_list_helper=0x4040A,
                        actual_render_JSR=0x40354,selection_call_PC=0x4044C,
                        original_return_PC=0x3D814,actual_final_SP=view['final_SP'])
    if set(found)!=wanted or len(found)!=EDITABLE_BYTES or len(_coalesce(found))!=PHYSICAL_BLOCKS:
        raise ValueError('canonical conditional motion source scope differs')
    return tuple(found[p] for p in sorted(found))

def physical_positions(rom):
    verify_rom(rom);return tuple(r['address'] for r in _catalog(rom))

def witness(rom,address):
    verify_rom(rom);address=uint(address,ROM_SIZE-1,'source BYTE address')
    for row in _catalog(rom):
        if row['address']==address:return load_fields(dump(row))
    raise ValueError('outside physical motion source authority')

def metadata(rom):
    positions=physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditional_original_object_motion_and_SAT_source_reads',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        source_union_BYTES=EDITABLE_BYTES,source_union_sha256=sha(bytes(rom[p] for p in positions)),
        physical_blocks=PHYSICAL_BLOCKS,physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in SOURCE_SPANS],
        raw_baseline=dict(layout_id=LAYOUT_ID,manifest_sha256=LAYOUT_SHA256,raw_BYTES=11525,resources=104),
        roles=dict(resource='live_motion_and_subsequent_compact_sprite_source_components',
            BYTE_values='full0..255; first80h marker/X, Y, size/attribute and tilelow keepallbits',
            zero_values='actual conditional source BYTEs, not padding/free space',
            source_stages=sorted({r['selection_stage'] for r in _catalog(rom)}),
            field_roles=sorted({r['source_role'] for r in _catalog(rom)}),
            shared_fields='all old typed sources and aliases live-read only; never re-emitted'),
        evidence=dict(real_entry_call_PC=0x3D810,call_target=0x4033C,list_producer=0x4040A,
            list='31descending X>>4 bins of32 RAMobjects/16Bstride; BTST.B7; actualLONG listwrites and trailingCLRL',
            object_start_RAM=0xFF816A,object_end_RAM=0xFF836A,rendered_object_JSR=0x40354,
            original_motion_call_PC=0x4044C,motion_selection=0x40C94,
            selection_gates='813E.W0;814C.W1;object.W&7F==814E.W;8150.W<<4 matchesactualA6;8152.W!=0;815A.W9',
            indexed_JMP='40D44 live815A.W→ASL.W2→40D4A PCindexedJMP40D4E+s16→40D72 BRA416F8',
            live_target_pointer='416F8 reads815C.L;416FC live8164.W vs41700 target2(A5).W; true BNE41768 in defaultframe',
            original_movement='840A.W selectsstep4/8;object+8 exact0/1/2/3 updates8164/8166 WORD±step; otherWORD unchanged',
            live_motion_directory='417AE full8(A6).W→ASL.W2→417B4 liveLONG417CE+s16(shiftedWORD)',
            SAT_tail_PC=0x417CA,SAT_entry=0x3B13C,
            continuation='SATrealRTS→40450; then40452 ordinaryselection/404AApointer/407D4attr live; outer40380→40408RTS→3D814',
            source_gates='F300 BYTE unsigned<50h; signedXclipping; first80hBYTE; 50h(80decimal)capacity aftereachrecord',
            read_order='XBYTE then YBYTE(+3), sizeBYTE(+1), repeatedattributeBYTE(+1), tilelowBYTE(+2)',
            actual_canonical_return=0x3D814,witness_states=list(WITNESS_STATES),
            whole_code_controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES],
            complete_control_RTS_guards=True),
        conditional_frame='completezero64KiB +816A.W8000/814C.W1/8152.W1/815A.W9/815C.LFFFF826A/826C.W1/8172.Winput; D/A0 exceptSPFFFFFD00; SR2500/CCR0',
        input_contract='fullRAM supplied once, FF8172.W parameter once; noA6/source/list/helperindex injection ormidRAMrepair',
        canonical_scope=dict(BYTEs=1343,bankC=62,bankF=1281,Ffront=1281,Ftail=0,baseline_raw_subset=True),
        natural_object_status='unknown; prior observeddirectionwriters0..3 do not establishfullWORD naturalproducer',
        natural_815C_RAM_pointer='unknown; completeconditionalRAM suppliesan in-arraytarget; targetactive/naturalframe notclaimed',
        allocation_or_resource_owner='unknown',owner_bytes_added=0,functions_added=0,natural_domains_added=0,
        complete_domains_added=0,complete_function_recovery=False,independent_CPU_comparison=False,
        earlier_3D810_UI_state_closed=False,edited_gameplay_safety='unknown',
        padding_or_free_space_claimed=False,instrumentation_budget_is_original_CPU_stop=False,
        final_semantic_high_level_recovery=False,
        diagnostic_scope='ordered successfuloperand reads/writes and actualcalls only; failedread notcounted; stoppedpostincrement registers maydiffer fromsuccessfirstreference; notcompletebuscycle/exceptionframe')

def _fixed(row):
    return {k:row[k] for k in ('address','source_role','selection_stage','read_width','unit_BYTE_lane')}

def extract(rom):
    return dict(**metadata(rom),source_BYTEs=[dict(**_fixed(r),BYTE=rom[r['address']]) for r in _catalog(rom)])

def blocks(rom,fields):
    fixed=metadata(rom);keys(fields,set(fixed)|{'source_BYTEs'},'motion source package')
    for k,v in fixed.items():same(fields[k],v,'package.'+k)
    values={}
    for expected,row in zip(_catalog(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'literal source BYTEs')):
        keys(row,set(_fixed(expected))|{'BYTE'},'sprite source component')
        for k,v in _fixed(expected).items():same(row[k],v,'source.'+k)
        values[expected['address']]=uint(row['BYTE'],255,'complete source BYTE')
    return [dict(id=f'rom_{a:06X}_motion_compact_source_BYTEs',start=a,end=z,
        data=bytes(values[p] for p in range(a,z)),role='conditional_object_motion_sprite_source_BYTEs')
        for a,z in SOURCE_SPANS]

def rebuild(rom,fields):
    verify_rom(rom);image=bytearray(rom)
    for row in blocks(rom,fields):image[row['start']:row['end']]=row['data']
    return bytes(image)

def schema(rom):
    def object_schema(p):return dict(type='object',properties=p,required=list(p),additionalProperties=False)
    def fixed(value):
        if type(value) is dict:return object_schema({k:fixed(v) for k,v in value.items()})
        if type(value) is list:return dict(type='array',prefixItems=[fixed(v) for v in value],items=False,minItems=len(value),maxItems=len(value))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(value)],const=value)
    props={k:fixed(v) for k,v in metadata(rom).items()}
    props['source_BYTEs']=dict(type='array',minItems=EDITABLE_BYTES,maxItems=EDITABLE_BYTES,items=False,
        prefixItems=[object_schema(dict(**{k:fixed(v) for k,v in _fixed(r).items()},BYTE=dict(type='integer',minimum=0,maximum=255))) for r in _catalog(rom)])
    return dict(**object_schema(props),**{'$schema':'https://json-schema.org/draft/2020-12/schema'},
        description='1343 single-authority conditional sprite source BYTEs; catalog is not a CPU clamp.')

def render_bundle(rom):
    fields=extract(rom);image=rebuild(rom,load_fields(dump(fields)))
    if image!=rom:raise ValueError('wholeROM serialized roundtrip differs')
    validation=dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
        limitations=['Disclosed completeRAM caller frame; natural815C/fullWORD and ownerunknown.',
            'Motion and subsequent ordinary sprite sources are read live fromwholeeditedimage.',
            'Original gates/first80h/capacity canstop or leave thepinnedconditionalpath; nofakeRTS/IRQ/RAMrepair/fullCPU.'])
    members={'fields.json':dump(fields),'fields.schema.json':dump(schema(rom)),'validation.json':dump(validation)}
    members['manifest.json']=dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,
        members={k:dict(bytes=len(v),sha256=sha(v)) for k,v in members.items()}))
    return members

def fresh_output(value,bundle=False):
    path=safe_path(value)
    for ancestor in (path,*path.parents):
        if ancestor.is_symlink() or getattr(ancestor,'is_junction',lambda:False)():raise ValueError('reparse output refused')
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError('dedicated fresh build output or exact fresh formal bundle required')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('export','import','verify'))
    parser.add_argument('--rom',default=str(DEFAULT_ROM));parser.add_argument('--fields')
    parser.add_argument('--bundle');parser.add_argument('--output')
    args=parser.parse_args(argv);target=None
    if args.command=='export':
        if args.output is None or args.fields is not None or args.bundle is not None:raise ValueError('export needsoutputonly')
        target=fresh_output(args.output,True)
    elif args.command=='import':
        if args.output is None or args.bundle is not None:raise ValueError('import needsfreshBIN')
        target=fresh_output(args.output)
        if target.suffix.lower()!='.bin':raise ValueError('freshBIN required')
    elif args.output is not None or args.fields is not None and args.bundle is not None:
        raise ValueError('verify acceptsfieldsorbundle and writesnothing')
    rom=read_bounded(args.rom,ROM_SIZE)
    if args.command=='export':
        members=render_bundle(rom);target.mkdir()
        for name,data in members.items():put(target/name,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={k:sha(v) for k,v in members.items()})
    elif args.command=='verify' and args.bundle is not None:
        path=safe_path(args.bundle)
        if not path.is_dir() or {p.name for p in path.iterdir()}!=MEMBERS:raise ValueError('exactfourmembers required')
        for name,data in render_bundle(rom).items():
            if read_bounded(path/name,MAX_JSON)!=data:raise ValueError('bundle drift:'+name)
        result=dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True)
    else:
        image=rebuild(rom,load_fields(read_bounded(args.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:put(target,image)
        result=dict(exact_canonical=image==rom,sha256=sha(image),editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
