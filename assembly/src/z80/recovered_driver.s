; Z80 声音驱动。z80_ 标签标记逻辑地址，卡带偏移由地址布局指定。
.text
_start:
.org 0x0
z80_0000:
        di
z80_0000_end:
.org 0x1
z80_0001:
        di
z80_0001_end:
.org 0x2
z80_0002:
        im 1
z80_0002_end:
.org 0x4
z80_0004:
        jr z80_0053
z80_0004_end:
.org 0x8
z80_0008:
        ld a,($4000)
z80_0008_end:
.org 0xB
z80_000b:
        bit 7,a
z80_000b_end:
.org 0xD
z80_000d:
        jr nz,z80_0008
z80_000d_end:
.org 0xF
z80_000f:
        ret
z80_000f_end:
.org 0x10
z80_0010:
        bit 7,(ix+$01)
z80_0010_end:
.org 0x14
z80_0014:
        ret nz
z80_0014_end:
.org 0x15
z80_0015:
        jp $049e
z80_0015_end:
.org 0x18
z80_0018:
        jp $04ac
z80_0018_end:
.org 0x20
z80_0020:
        ld hl,($1c02)
z80_0020_end:
.org 0x23
z80_0023:
        ld b,$00
z80_0023_end:
.org 0x25
z80_0025:
        jp $0478
z80_0025_end:
.org 0x28
z80_0028:
        ld c,a
z80_0028_end:
.org 0x29
z80_0029:
        ld b,$00
z80_0029_end:
.org 0x2B
z80_002b:
        add hl,bc
z80_002b_end:
.org 0x2C
z80_002c:
        add hl,bc
z80_002c_end:
.org 0x2D
z80_002d:
        nop
z80_002d_end:
.org 0x2E
z80_002e:
        nop
z80_002e_end:
.org 0x2F
z80_002f:
        nop
z80_002f_end:
.org 0x30
z80_0030:
        ld a,(hl)
z80_0030_end:
.org 0x31
z80_0031:
        inc hl
z80_0031_end:
.org 0x32
z80_0032:
        ld h,(hl)
z80_0032_end:
.org 0x33
z80_0033:
        ld l,a
z80_0033_end:
.org 0x34
z80_0034:
        ret
z80_0034_end:
.org 0x38
z80_0038:
        push af
z80_0038_end:
.org 0x39
z80_0039:
        push bc
z80_0039_end:
.org 0x3A
z80_003a:
        push de
z80_003a_end:
.org 0x3B
z80_003b:
        push hl
z80_003b_end:
.org 0x3C
z80_003c:
        ld hl,$1fff
z80_003c_end:
.org 0x3F
z80_003f:
        ld a,(hl)
z80_003f_end:
.org 0x40
z80_0040:
        or a
z80_0040_end:
.org 0x41
z80_0041:
        jr z,z80_0046
z80_0041_end:
.org 0x43
z80_0043:
        dec (hl)
z80_0043_end:
.org 0x44
z80_0044:
        jr z80_004d
z80_0044_end:
.org 0x46
z80_0046:
        ld a,($1c07)
z80_0046_end:
.org 0x49
z80_0049:
        or a
z80_0049_end:
.org 0x4A
z80_004a:
        call z,$00e5
z80_004a_end:
.org 0x4D
z80_004d:
        pop hl
z80_004d_end:
.org 0x4E
z80_004e:
        pop de
z80_004e_end:
.org 0x4F
z80_004f:
        pop bc
z80_004f_end:
.org 0x50
z80_0050:
        pop af
z80_0050_end:
.org 0x51
z80_0051:
        ei
z80_0051_end:
.org 0x52
z80_0052:
        ret
z80_0052_end:
.org 0x53
z80_0053:
        ld sp,$1ffd
z80_0053_end:
.org 0x56
z80_0056:
        ld a,$03
z80_0056_end:
.org 0x58
z80_0058:
        ld ($1fff),a
z80_0058_end:
.org 0x5B
z80_005b:
        ei
z80_005b_end:
.org 0x5C
z80_005c:
        ld a,($1fff)
z80_005c_end:
.org 0x5F
z80_005f:
        or a
z80_005f_end:
.org 0x60
z80_0060:
        jp nz,$005b
z80_0060_end:
.org 0x63
z80_0063:
        call $07e7
z80_0063_end:
.org 0x66
z80_0066:
        call $070c
z80_0066_end:
.org 0x69
z80_0069:
        call $00b9
z80_0069_end:
.org 0x6C
z80_006c:
        call $00d3
z80_006c_end:
.org 0x6F
z80_006f:
        ei
z80_006f_end:
.org 0x70
z80_0070:
        call $087f
z80_0070_end:
.org 0x73
z80_0073:
        ld a,($1c07)
z80_0073_end:
.org 0x76
z80_0076:
        or a
z80_0076_end:
.org 0x77
z80_0077:
        jr z,z80_006f
z80_0077_end:
.org 0x79
z80_0079:
        di
z80_0079_end:
.org 0x7A
z80_007a:
        jp p,$00aa
z80_007a_end:
.org 0x7D
z80_007d:
        call $087f
z80_007d_end:
.org 0x80
z80_0080:
        ld a,($4000)
z80_0080_end:
.org 0x83
z80_0083:
        and $03
z80_0083_end:
.org 0x85
z80_0085:
        jr z,z80_006f
z80_0085_end:
.org 0x87
z80_0087:
        bit 1,a
z80_0087_end:
.org 0x89
z80_0089:
        jr z,z80_009b
z80_0089_end:
.org 0x8B
z80_008b:
        call $00d3
z80_008b_end:
.org 0x8E
z80_008e:
        ld hl,$009b
z80_008e_end:
.org 0x91
z80_0091:
        push hl
z80_0091_end:
.org 0x92
z80_0092:
        call $071f
z80_0092_end:
.org 0x95
z80_0095:
        call $050a
z80_0095_end:
.org 0x98
z80_0098:
        jp $010f
z80_0098_end:
.org 0x9B
z80_009b:
        ld a,($4000)
z80_009b_end:
.org 0x9E
z80_009e:
        bit 0,a
z80_009e_end:
.org 0xA0
z80_00a0:
        jr z,z80_006f
z80_00a0_end:
.org 0xA2
z80_00a2:
        call $00b9
z80_00a2_end:
.org 0xA5
z80_00a5:
        call $00e5
z80_00a5_end:
.org 0xA8
z80_00a8:
        jr z80_006f
z80_00a8_end:
.org 0xAA
z80_00aa:
        ld a,($4000)
z80_00aa_end:
.org 0xAD
z80_00ad:
        bit 1,a
z80_00ad_end:
.org 0xAF
z80_00af:
        jr z,z80_006f
z80_00af_end:
.org 0xB1
z80_00b1:
        call $00d3
z80_00b1_end:
.org 0xB4
z80_00b4:
        call $00e5
z80_00b4_end:
.org 0xB7
z80_00b7:
        jr z80_006f
z80_00b7_end:
.org 0xB9
z80_00b9:
        ld hl,($1c04)
z80_00b9_end:
.org 0xBC
z80_00bc:
        ld a,l
z80_00bc_end:
.org 0xBD
z80_00bd:
        and $03
z80_00bd_end:
.org 0xBF
z80_00bf:
        ld c,a
z80_00bf_end:
.org 0xC0
z80_00c0:
        ld a,$25
z80_00c0_end:
.org 0xC2
z80_00c2:
        rst $0018
z80_00c2_end:
.org 0xC3
z80_00c3:
        srl h
z80_00c3_end:
.org 0xC5
z80_00c5:
        rr l
z80_00c5_end:
.org 0xC7
z80_00c7:
        srl h
z80_00c7_end:
.org 0xC9
z80_00c9:
        rr l
z80_00c9_end:
.org 0xCB
z80_00cb:
        ld c,l
z80_00cb_end:
.org 0xCC
z80_00cc:
        ld a,$24
z80_00cc_end:
.org 0xCE
z80_00ce:
        rst $0018
z80_00ce_end:
.org 0xCF
z80_00cf:
        ld a,$1f
z80_00cf_end:
.org 0xD1
z80_00d1:
        jr z80_00dc
z80_00d1_end:
.org 0xD3
z80_00d3:
        ld a,($1c06)
z80_00d3_end:
.org 0xD6
z80_00d6:
        ld c,a
z80_00d6_end:
.org 0xD7
z80_00d7:
        ld a,$26
z80_00d7_end:
.org 0xD9
z80_00d9:
        rst $0018
z80_00d9_end:
.org 0xDA
z80_00da:
        ld a,$2f
z80_00da_end:
.org 0xDC
z80_00dc:
        ld hl,$1c12
z80_00dc_end:
.org 0xDF
z80_00df:
        or (hl)
z80_00df_end:
.org 0xE0
z80_00e0:
        ld c,a
z80_00e0_end:
.org 0xE1
z80_00e1:
        ld a,$27
z80_00e1_end:
.org 0xE3
z80_00e3:
        rst $0018
z80_00e3_end:
.org 0xE4
z80_00e4:
        ret
z80_00e4_end:
.org 0xE5
z80_00e5:
        call $071f
z80_00e5_end:
.org 0xE8
z80_00e8:
        call $0866
z80_00e8_end:
.org 0xEB
z80_00eb:
        call $079b
z80_00eb_end:
.org 0xEE
z80_00ee:
        call $050a
z80_00ee_end:
.org 0xF1
z80_00f1:
        ld a,($1c07)
z80_00f1_end:
.org 0xF4
z80_00f4:
        or a
z80_00f4_end:
.org 0xF5
z80_00f5:
        call p,$010f
z80_00f5_end:
.org 0xF8
z80_00f8:
        xor a
z80_00f8_end:
.org 0xF9
z80_00f9:
        ld ($1c19),a
z80_00f9_end:
.org 0xFC
z80_00fc:
        ld ix,$1c40
z80_00fc_end:
.org 0x100
z80_0100:
        bit 7,(ix+$00)
z80_0100_end:
.org 0x104
z80_0104:
        call nz,$0988
z80_0104_end:
.org 0x107
z80_0107:
        ld b,$09
z80_0107_end:
.org 0x109
z80_0109:
        ld ix,$1c70
z80_0109_end:
.org 0x10D
z80_010d:
        jr z80_0128
z80_010d_end:
.org 0x10F
z80_010f:
        ld a,$01
z80_010f_end:
.org 0x111
z80_0111:
        ld ($1c19),a
z80_0111_end:
.org 0x114
z80_0114:
        ld ix,$1e80
z80_0114_end:
.org 0x118
z80_0118:
        ld b,$06
z80_0118_end:
.org 0x11A
z80_011a:
        call $0128
z80_011a_end:
.org 0x11D
z80_011d:
        ld a,$80
z80_011d_end:
.org 0x11F
z80_011f:
        ld ($1c19),a
z80_011f_end:
.org 0x122
z80_0122:
        ld b,$02
z80_0122_end:
.org 0x124
z80_0124:
        ld ix,$1e20
z80_0124_end:
.org 0x128
z80_0128:
        push bc
z80_0128_end:
.org 0x129
z80_0129:
        bit 7,(ix+$00)
z80_0129_end:
.org 0x12D
z80_012d:
        call nz,$0139
z80_012d_end:
.org 0x130
z80_0130:
        ld de,$0030
z80_0130_end:
.org 0x133
z80_0133:
        add ix,de
z80_0133_end:
.org 0x135
z80_0135:
        pop bc
z80_0135_end:
.org 0x136
z80_0136:
        djnz z80_0128
z80_0136_end:
.org 0x138
z80_0138:
        ret
z80_0138_end:
.org 0x139
z80_0139:
        bit 7,(ix+$01)
z80_0139_end:
.org 0x13D
z80_013d:
        jp nz,$0f05
z80_013d_end:
.org 0x140
z80_0140:
        call $0304
z80_0140_end:
.org 0x143
z80_0143:
        jr nz,z80_015c
z80_0143_end:
.org 0x145
z80_0145:
        call $01d6
z80_0145_end:
.org 0x148
z80_0148:
        bit 4,(ix+$00)
z80_0148_end:
.org 0x14C
z80_014c:
        ret nz
z80_014c_end:
.org 0x14D
z80_014d:
        call $033b
z80_014d_end:
.org 0x150
z80_0150:
        call $0432
z80_0150_end:
.org 0x153
z80_0153:
        call $0366
z80_0153_end:
.org 0x156
z80_0156:
        call $017e
z80_0156_end:
.org 0x159
z80_0159:
        jp $040b
z80_0159_end:
.org 0x15C
z80_015c:
        call $02ee
z80_015c_end:
.org 0x15F
z80_015f:
        bit 4,(ix+$00)
z80_015f_end:
.org 0x163
z80_0163:
        ret nz
z80_0163_end:
.org 0x164
z80_0164:
        call $030c
z80_0164_end:
.org 0x167
z80_0167:
        ld a,(ix+$1e)
z80_0167_end:
.org 0x16A
z80_016a:
        or a
z80_016a_end:
.org 0x16B
z80_016b:
        jr z,z80_0173
z80_016b_end:
.org 0x16D
z80_016d:
        dec (ix+$1e)
z80_016d_end:
.org 0x170
z80_0170:
        jp z,$0428
z80_0170_end:
.org 0x173
z80_0173:
        call $0432
z80_0173_end:
.org 0x176
z80_0176:
        bit 6,(ix+$00)
z80_0176_end:
.org 0x17A
z80_017a:
        ret nz
z80_017a_end:
.org 0x17B
z80_017b:
        call $0366
z80_017b_end:
.org 0x17E
z80_017e:
        bit 2,(ix+$00)
z80_017e_end:
.org 0x182
z80_0182:
        ret nz
z80_0182_end:
.org 0x183
z80_0183:
        bit 0,(ix+$00)
z80_0183_end:
.org 0x187
z80_0187:
        jp nz,$0193
z80_0187_end:
.org 0x18A
z80_018a:
        ld a,$a4
z80_018a_end:
.org 0x18C
z80_018c:
        ld c,h
z80_018c_end:
.org 0x18D
z80_018d:
        rst $0010
z80_018d_end:
.org 0x18E
z80_018e:
        ld a,$a0
z80_018e_end:
.org 0x190
z80_0190:
        ld c,l
z80_0190_end:
.org 0x191
z80_0191:
        rst $0010
z80_0191_end:
.org 0x192
z80_0192:
        ret
z80_0192_end:
.org 0x193
z80_0193:
        ld a,(ix+$01)
z80_0193_end:
.org 0x196
z80_0196:
        cp $02
z80_0196_end:
.org 0x198
z80_0198:
        jr nz,z80_018a
z80_0198_end:
.org 0x19A
z80_019a:
        call $01c6
z80_019a_end:
.org 0x19D
z80_019d:
        exx
z80_019d_end:
.org 0x19E
z80_019e:
        ld hl,$01c2
z80_019e_end:
.org 0x1A1
z80_01a1:
        ld b,$04
z80_01a1_end:
.org 0x1A3
z80_01a3:
        ld a,(hl)
z80_01a3_end:
.org 0x1A4
z80_01a4:
        push af
z80_01a4_end:
.org 0x1A5
z80_01a5:
        inc hl
z80_01a5_end:
.org 0x1A6
z80_01a6:
        exx
z80_01a6_end:
.org 0x1A7
z80_01a7:
        ex de,hl
z80_01a7_end:
.org 0x1A8
z80_01a8:
        ld c,(hl)
z80_01a8_end:
.org 0x1A9
z80_01a9:
        inc hl
z80_01a9_end:
.org 0x1AA
z80_01aa:
        ld b,(hl)
z80_01aa_end:
.org 0x1AB
z80_01ab:
        inc hl
z80_01ab_end:
.org 0x1AC
z80_01ac:
        ex de,hl
z80_01ac_end:
.org 0x1AD
z80_01ad:
        ld l,(ix+$0d)
z80_01ad_end:
.org 0x1B0
z80_01b0:
        ld h,(ix+$0e)
z80_01b0_end:
.org 0x1B3
z80_01b3:
        add hl,bc
z80_01b3_end:
.org 0x1B4
z80_01b4:
        pop af
z80_01b4_end:
.org 0x1B5
z80_01b5:
        push af
z80_01b5_end:
.org 0x1B6
z80_01b6:
        ld c,h
z80_01b6_end:
.org 0x1B7
z80_01b7:
        rst $0018
z80_01b7_end:
.org 0x1B8
z80_01b8:
        pop af
z80_01b8_end:
.org 0x1B9
z80_01b9:
        sub $04
z80_01b9_end:
.org 0x1BB
z80_01bb:
        ld c,l
z80_01bb_end:
.org 0x1BC
z80_01bc:
        rst $0018
z80_01bc_end:
.org 0x1BD
z80_01bd:
        exx
z80_01bd_end:
.org 0x1BE
z80_01be:
        djnz z80_01a3
z80_01be_end:
.org 0x1C0
z80_01c0:
        exx
z80_01c0_end:
.org 0x1C1
z80_01c1:
        ret
z80_01c1_end:
.org 0x1C6
z80_01c6:
        ld de,$1c2a
z80_01c6_end:
.org 0x1C9
z80_01c9:
        ld a,($1c19)
z80_01c9_end:
.org 0x1CC
z80_01cc:
        or a
z80_01cc_end:
.org 0x1CD
z80_01cd:
        ret z
z80_01cd_end:
.org 0x1CE
z80_01ce:
        ld de,$1c1a
z80_01ce_end:
.org 0x1D1
z80_01d1:
        ret p
z80_01d1_end:
.org 0x1D2
z80_01d2:
        ld de,$1c22
z80_01d2_end:
.org 0x1D5
z80_01d5:
        ret
z80_01d5_end:
.org 0x1D6
z80_01d6:
        ld e,(ix+$03)
z80_01d6_end:
.org 0x1D9
z80_01d9:
        ld d,(ix+$04)
z80_01d9_end:
.org 0x1DC
z80_01dc:
        res 1,(ix+$00)
z80_01dc_end:
.org 0x1E0
z80_01e0:
        res 4,(ix+$00)
z80_01e0_end:
.org 0x1E4
z80_01e4:
        ld a,(de)
z80_01e4_end:
.org 0x1E5
z80_01e5:
        inc de
z80_01e5_end:
.org 0x1E6
z80_01e6:
        cp $e0
z80_01e6_end:
.org 0x1E8
z80_01e8:
        jp nc,$0b78
z80_01e8_end:
.org 0x1EB
z80_01eb:
        ex af,af'
z80_01eb_end:
.org 0x1EC
z80_01ec:
        call $0422
z80_01ec_end:
.org 0x1EF
z80_01ef:
        call $02a8
z80_01ef_end:
.org 0x1F2
z80_01f2:
        ex af,af'
z80_01f2_end:
.org 0x1F3
z80_01f3:
        bit 3,(ix+$00)
z80_01f3_end:
.org 0x1F7
z80_01f7:
        jp nz,$0250
z80_01f7_end:
.org 0x1FA
z80_01fa:
        or a
z80_01fa_end:
.org 0x1FB
z80_01fb:
        jp p,$0276
z80_01fb_end:
.org 0x1FE
z80_01fe:
        sub $81
z80_01fe_end:
.org 0x200
z80_0200:
        jp p,$0208
z80_0200_end:
.org 0x203
z80_0203:
        call $0fac
z80_0203_end:
.org 0x206
z80_0206:
        jr z80_0236
z80_0206_end:
.org 0x208
z80_0208:
        add a,(ix+$05)
z80_0208_end:
.org 0x20B
z80_020b:
        ld hl,$08e6
z80_020b_end:
.org 0x20E
z80_020e:
        push af
z80_020e_end:
.org 0x20F
z80_020f:
        rst $0028
z80_020f_end:
.org 0x210
z80_0210:
        pop af
z80_0210_end:
.org 0x211
z80_0211:
        bit 7,(ix+$01)
z80_0211_end:
.org 0x215
z80_0215:
        jr nz,z80_0230
z80_0215_end:
.org 0x217
z80_0217:
        push de
z80_0217_end:
.org 0x218
z80_0218:
        ld d,$08
z80_0218_end:
.org 0x21A
z80_021a:
        ld e,$0c
z80_021a_end:
.org 0x21C
z80_021c:
        ex af,af'
z80_021c_end:
.org 0x21D
z80_021d:
        xor a
z80_021d_end:
.org 0x21E
z80_021e:
        ex af,af'
z80_021e_end:
.org 0x21F
z80_021f:
        sub e
z80_021f_end:
.org 0x220
z80_0220:
        jr c,z80_0227
z80_0220_end:
.org 0x222
z80_0222:
        ex af,af'
z80_0222_end:
.org 0x223
z80_0223:
        add a,d
z80_0223_end:
.org 0x224
z80_0224:
        jr z80_021e
z80_0224_end:
.org 0x227
z80_0227:
        add a,e
z80_0227_end:
.org 0x228
z80_0228:
        ld hl,$0970
z80_0228_end:
.org 0x22B
z80_022b:
        rst $0028
z80_022b_end:
.org 0x22C
z80_022c:
        ex af,af'
z80_022c_end:
.org 0x22D
z80_022d:
        or h
z80_022d_end:
.org 0x22E
z80_022e:
        ld h,a
z80_022e_end:
.org 0x22F
z80_022f:
        pop de
z80_022f_end:
.org 0x230
z80_0230:
        ld (ix+$0d),l
z80_0230_end:
.org 0x233
z80_0233:
        ld (ix+$0e),h
z80_0233_end:
.org 0x236
z80_0236:
        bit 5,(ix+$00)
z80_0236_end:
.org 0x23A
z80_023a:
        jr nz,z80_0249
z80_023a_end:
.org 0x23C
z80_023c:
        ld a,(de)
z80_023c_end:
.org 0x23D
z80_023d:
        or a
z80_023d_end:
.org 0x23E
z80_023e:
        jp p,$0275
z80_023e_end:
.org 0x241
z80_0241:
        ld a,(ix+$0c)
z80_0241_end:
.org 0x244
z80_0244:
        ld (ix+$0b),a
z80_0244_end:
.org 0x247
z80_0247:
        jr z80_027c
z80_0247_end:
.org 0x249
z80_0249:
        ld a,(de)
z80_0249_end:
.org 0x24A
z80_024a:
        inc de
z80_024a_end:
.org 0x24B
z80_024b:
        ld (ix+$10),a
z80_024b_end:
.org 0x24E
z80_024e:
        jr z80_0274
z80_024e_end:
.org 0x250
z80_0250:
        ld h,a
z80_0250_end:
.org 0x251
z80_0251:
        ld a,(de)
z80_0251_end:
.org 0x252
z80_0252:
        inc de
z80_0252_end:
.org 0x253
z80_0253:
        ld l,a
z80_0253_end:
.org 0x254
z80_0254:
        or h
z80_0254_end:
.org 0x255
z80_0255:
        jr z,z80_0263
z80_0255_end:
.org 0x257
z80_0257:
        ld a,(ix+$05)
z80_0257_end:
.org 0x25A
z80_025a:
        ld b,$00
z80_025a_end:
.org 0x25C
z80_025c:
        or a
z80_025c_end:
.org 0x25D
z80_025d:
        jp p,$0261
z80_025d_end:
.org 0x260
z80_0260:
        dec b
z80_0260_end:
.org 0x261
z80_0261:
        ld c,a
z80_0261_end:
.org 0x262
z80_0262:
        add hl,bc
z80_0262_end:
.org 0x263
z80_0263:
        ld (ix+$0d),l
z80_0263_end:
.org 0x266
z80_0266:
        ld (ix+$0e),h
z80_0266_end:
.org 0x269
z80_0269:
        bit 5,(ix+$00)
z80_0269_end:
.org 0x26D
z80_026d:
        jr z,z80_0274
z80_026d_end:
.org 0x26F
z80_026f:
        ld a,(de)
z80_026f_end:
.org 0x270
z80_0270:
        inc de
z80_0270_end:
.org 0x271
z80_0271:
        ld (ix+$10),a
z80_0271_end:
.org 0x274
z80_0274:
        ld a,(de)
z80_0274_end:
.org 0x275
z80_0275:
        inc de
z80_0275_end:
.org 0x276
z80_0276:
        call $029e
z80_0276_end:
.org 0x279
z80_0279:
        ld (ix+$0c),a
z80_0279_end:
.org 0x27C
z80_027c:
        ld (ix+$03),e
z80_027c_end:
.org 0x27F
z80_027f:
        ld (ix+$04),d
z80_027f_end:
.org 0x282
z80_0282:
        ld a,(ix+$0c)
z80_0282_end:
.org 0x285
z80_0285:
        ld (ix+$0b),a
z80_0285_end:
.org 0x288
z80_0288:
        bit 1,(ix+$00)
z80_0288_end:
.org 0x28C
z80_028c:
        ret nz
z80_028c_end:
.org 0x28D
z80_028d:
        xor a
z80_028d_end:
.org 0x28E
z80_028e:
        ld (ix+$25),a
z80_028e_end:
.org 0x291
z80_0291:
        ld (ix+$22),a
z80_0291_end:
.org 0x294
z80_0294:
        ld a,(ix+$1f)
z80_0294_end:
.org 0x297
z80_0297:
        ld (ix+$1e),a
z80_0297_end:
.org 0x29A
z80_029a:
        ld (ix+$17),a
z80_029a_end:
.org 0x29D
z80_029d:
        ret
z80_029d_end:
.org 0x29E
z80_029e:
        ld b,(ix+$02)
z80_029e_end:
.org 0x2A1
z80_02a1:
        dec b
z80_02a1_end:
.org 0x2A2
z80_02a2:
        ret z
z80_02a2_end:
.org 0x2A3
z80_02a3:
        ld c,a
z80_02a3_end:
.org 0x2A4
z80_02a4:
        add a,c
z80_02a4_end:
.org 0x2A5
z80_02a5:
        djnz z80_02a4
z80_02a5_end:
.org 0x2A7
z80_02a7:
        ret
z80_02a7_end:
.org 0x2A8
z80_02a8:
        ld a,(ix+$11)
z80_02a8_end:
.org 0x2AB
z80_02ab:
        dec a
z80_02ab_end:
.org 0x2AC
z80_02ac:
        ret m
z80_02ac_end:
.org 0x2AD
z80_02ad:
        jr nz,z80_02ea
z80_02ad_end:
.org 0x2AF
z80_02af:
        bit 1,(ix+$00)
z80_02af_end:
.org 0x2B3
z80_02b3:
        ret nz
z80_02b3_end:
.org 0x2B4
z80_02b4:
        dec (ix+$16)
z80_02b4_end:
.org 0x2B7
z80_02b7:
        ret nz
z80_02b7_end:
.org 0x2B8
z80_02b8:
        exx
z80_02b8_end:
.org 0x2B9
z80_02b9:
        ld a,(ix+$15)
z80_02b9_end:
.org 0x2BC
z80_02bc:
        ld (ix+$16),a
z80_02bc_end:
.org 0x2BF
z80_02bf:
        ld a,(ix+$12)
z80_02bf_end:
.org 0x2C2
z80_02c2:
        ld hl,$02f6
z80_02c2_end:
.org 0x2C5
z80_02c5:
        rst $0028
z80_02c5_end:
.org 0x2C6
z80_02c6:
        ld e,(ix+$13)
z80_02c6_end:
.org 0x2C9
z80_02c9:
        inc (ix+$13)
z80_02c9_end:
.org 0x2CC
z80_02cc:
        ld a,(ix+$14)
z80_02cc_end:
.org 0x2CF
z80_02cf:
        dec a
z80_02cf_end:
.org 0x2D0
z80_02d0:
        cp e
z80_02d0_end:
.org 0x2D1
z80_02d1:
        jr nz,z80_02e1
z80_02d1_end:
.org 0x2D3
z80_02d3:
        dec (ix+$13)
z80_02d3_end:
.org 0x2D6
z80_02d6:
        ld a,(ix+$11)
z80_02d6_end:
.org 0x2D9
z80_02d9:
        cp $02
z80_02d9_end:
.org 0x2DB
z80_02db:
        jr z,z80_02e1
z80_02db_end:
.org 0x2DD
z80_02dd:
        ld (ix+$13),$00
z80_02dd_end:
.org 0x2E1
z80_02e1:
        ld d,$00
z80_02e1_end:
.org 0x2E3
z80_02e3:
        add hl,de
z80_02e3_end:
.org 0x2E4
z80_02e4:
        ex de,hl
z80_02e4_end:
.org 0x2E5
z80_02e5:
        call $0d70
z80_02e5_end:
.org 0x2E8
z80_02e8:
        exx
z80_02e8_end:
.org 0x2E9
z80_02e9:
        ret
z80_02e9_end:
.org 0x2EA
z80_02ea:
        xor a
z80_02ea_end:
.org 0x2EB
z80_02eb:
        ld (ix+$13),a
z80_02eb_end:
.org 0x2EE
z80_02ee:
        ld a,(ix+$11)
z80_02ee_end:
.org 0x2F1
z80_02f1:
        sub $02
z80_02f1_end:
.org 0x2F3
z80_02f3:
        ret m
z80_02f3_end:
.org 0x2F4
z80_02f4:
        jr z80_02b4
z80_02f4_end:
.org 0x304
z80_0304:
        ld a,(ix+$0b)
z80_0304_end:
.org 0x307
z80_0307:
        dec a
z80_0307_end:
.org 0x308
z80_0308:
        ld (ix+$0b),a
z80_0308_end:
.org 0x30B
z80_030b:
        ret
z80_030b_end:
.org 0x30C
z80_030c:
        ld a,(ix+$18)
z80_030c_end:
.org 0x30F
z80_030f:
        or a
z80_030f_end:
.org 0x310
z80_0310:
        ret z
z80_0310_end:
.org 0x311
z80_0311:
        ret m
z80_0311_end:
.org 0x312
z80_0312:
        dec a
z80_0312_end:
.org 0x313
z80_0313:
        ld c,$0a
z80_0313_end:
.org 0x315
z80_0315:
        rst $0020
z80_0315_end:
.org 0x316
z80_0316:
        rst $0028
z80_0316_end:
.org 0x317
z80_0317:
        call $0f7b
z80_0317_end:
.org 0x31A
z80_031a:
        ld h,(ix+$1d)
z80_031a_end:
.org 0x31D
z80_031d:
        ld l,(ix+$1c)
z80_031d_end:
.org 0x320
z80_0320:
        ld de,$04dd
z80_0320_end:
.org 0x323
z80_0323:
        ld b,$04
z80_0323_end:
.org 0x325
z80_0325:
        ld c,(ix+$19)
z80_0325_end:
.org 0x328
z80_0328:
        push af
z80_0328_end:
.org 0x329
z80_0329:
        sra c
z80_0329_end:
.org 0x32B
z80_032b:
        push bc
z80_032b_end:
.org 0x32C
z80_032c:
        jr nc,z80_0334
z80_032c_end:
.org 0x32E
z80_032e:
        add a,(hl)
z80_032e_end:
.org 0x32F
z80_032f:
        and $7f
z80_032f_end:
.org 0x331
z80_0331:
        ld c,a
z80_0331_end:
.org 0x332
z80_0332:
        ld a,(de)
z80_0332_end:
.org 0x333
z80_0333:
        rst $0010
z80_0333_end:
.org 0x334
z80_0334:
        pop bc
z80_0334_end:
.org 0x335
z80_0335:
        inc de
z80_0335_end:
.org 0x336
z80_0336:
        inc hl
z80_0336_end:
.org 0x337
z80_0337:
        pop af
z80_0337_end:
.org 0x338
z80_0338:
        djnz z80_0328
z80_0338_end:
.org 0x33A
z80_033a:
        ret
z80_033a_end:
.org 0x33B
z80_033b:
        bit 7,(ix+$07)
z80_033b_end:
.org 0x33F
z80_033f:
        ret z
z80_033f_end:
.org 0x340
z80_0340:
        bit 1,(ix+$00)
z80_0340_end:
.org 0x344
z80_0344:
        ret nz
z80_0344_end:
.org 0x345
z80_0345:
        ld e,(ix+$20)
z80_0345_end:
.org 0x348
z80_0348:
        ld d,(ix+$21)
z80_0348_end:
.org 0x34B
z80_034b:
        push ix
z80_034b_end:
.org 0x34D
z80_034d:
        pop hl
z80_034d_end:
.org 0x34E
z80_034e:
        ld b,$00
z80_034e_end:
.org 0x350
z80_0350:
        ld c,$24
z80_0350_end:
.org 0x352
z80_0352:
        add hl,bc
z80_0352_end:
.org 0x353
z80_0353:
        ex de,hl
z80_0353_end:
.org 0x354
z80_0354:
        ldi
z80_0354_end:
.org 0x356
z80_0356:
        ldi
z80_0356_end:
.org 0x358
z80_0358:
        ldi
z80_0358_end:
.org 0x35A
z80_035a:
        ld a,(hl)
z80_035a_end:
.org 0x35B
z80_035b:
        srl a
z80_035b_end:
.org 0x35D
z80_035d:
        ld (de),a
z80_035d_end:
.org 0x35E
z80_035e:
        xor a
z80_035e_end:
.org 0x35F
z80_035f:
        ld (ix+$22),a
z80_035f_end:
.org 0x362
z80_0362:
        ld (ix+$23),a
z80_0362_end:
.org 0x365
z80_0365:
        ret
z80_0365_end:
.org 0x366
z80_0366:
        ld a,(ix+$07)
z80_0366_end:
.org 0x369
z80_0369:
        or a
z80_0369_end:
.org 0x36A
z80_036a:
        ret z
z80_036a_end:
.org 0x36B
z80_036b:
        cp $80
z80_036b_end:
.org 0x36D
z80_036d:
        jr nz,z80_03b7
z80_036d_end:
.org 0x36F
z80_036f:
        dec (ix+$24)
z80_036f_end:
.org 0x372
z80_0372:
        ret nz
z80_0372_end:
.org 0x373
z80_0373:
        inc (ix+$24)
z80_0373_end:
.org 0x376
z80_0376:
        push hl
z80_0376_end:
.org 0x377
z80_0377:
        ld l,(ix+$22)
z80_0377_end:
.org 0x37A
z80_037a:
        ld h,(ix+$23)
z80_037a_end:
.org 0x37D
z80_037d:
        dec (ix+$25)
z80_037d_end:
.org 0x380
z80_0380:
        jr nz,z80_03a2
z80_0380_end:
.org 0x382
z80_0382:
        ld e,(ix+$20)
z80_0382_end:
.org 0x385
z80_0385:
        ld d,(ix+$21)
z80_0385_end:
.org 0x388
z80_0388:
        push de
z80_0388_end:
.org 0x389
z80_0389:
        pop iy
z80_0389_end:
.org 0x38B
z80_038b:
        ld a,(iy+$01)
z80_038b_end:
.org 0x38E
z80_038e:
        ld (ix+$25),a
z80_038e_end:
.org 0x391
z80_0391:
        ld a,(ix+$26)
z80_0391_end:
.org 0x394
z80_0394:
        ld c,a
z80_0394_end:
.org 0x395
z80_0395:
        and $80
z80_0395_end:
.org 0x397
z80_0397:
        rlca
z80_0397_end:
.org 0x398
z80_0398:
        neg
z80_0398_end:
.org 0x39A
z80_039a:
        ld b,a
z80_039a_end:
.org 0x39B
z80_039b:
        add hl,bc
z80_039b_end:
.org 0x39C
z80_039c:
        ld (ix+$22),l
z80_039c_end:
.org 0x39F
z80_039f:
        ld (ix+$23),h
z80_039f_end:
.org 0x3A2
z80_03a2:
        pop bc
z80_03a2_end:
.org 0x3A3
z80_03a3:
        add hl,bc
z80_03a3_end:
.org 0x3A4
z80_03a4:
        dec (ix+$27)
z80_03a4_end:
.org 0x3A7
z80_03a7:
        ret nz
z80_03a7_end:
.org 0x3A8
z80_03a8:
        ld a,(iy+$03)
z80_03a8_end:
.org 0x3AB
z80_03ab:
        ld (ix+$27),a
z80_03ab_end:
.org 0x3AE
z80_03ae:
        ld a,(ix+$26)
z80_03ae_end:
.org 0x3B1
z80_03b1:
        neg
z80_03b1_end:
.org 0x3B3
z80_03b3:
        ld (ix+$26),a
z80_03b3_end:
.org 0x3B6
z80_03b6:
        ret
z80_03b6_end:
.org 0x3B7
z80_03b7:
        dec a
z80_03b7_end:
.org 0x3B8
z80_03b8:
        ex de,hl
z80_03b8_end:
.org 0x3B9
z80_03b9:
        ld c,$08
z80_03b9_end:
.org 0x3BB
z80_03bb:
        rst $0020
z80_03bb_end:
.org 0x3BC
z80_03bc:
        rst $0028
z80_03bc_end:
.org 0x3BD
z80_03bd:
        jr z80_03c2
z80_03bd_end:
.org 0x3BF
z80_03bf:
        ld (ix+$25),a
z80_03bf_end:
.org 0x3C2
z80_03c2:
        push hl
z80_03c2_end:
.org 0x3C3
z80_03c3:
        ld c,(ix+$25)
z80_03c3_end:
.org 0x3C6
z80_03c6:
        call $047d
z80_03c6_end:
.org 0x3C9
z80_03c9:
        pop hl
z80_03c9_end:
.org 0x3CA
z80_03ca:
        bit 7,a
z80_03ca_end:
.org 0x3CC
z80_03cc:
        jp z,$03fc
z80_03cc_end:
.org 0x3CF
z80_03cf:
        cp $82
z80_03cf_end:
.org 0x3D1
z80_03d1:
        jr z,z80_03e5
z80_03d1_end:
.org 0x3D3
z80_03d3:
        cp $80
z80_03d3_end:
.org 0x3D5
z80_03d5:
        jr z,z80_03e9
z80_03d5_end:
.org 0x3D7
z80_03d7:
        cp $84
z80_03d7_end:
.org 0x3D9
z80_03d9:
        jr z,z80_03ec
z80_03d9_end:
.org 0x3DB
z80_03db:
        ld h,$ff
z80_03db_end:
.org 0x3DD
z80_03dd:
        jr nc,z80_03fe
z80_03dd_end:
.org 0x3DF
z80_03df:
        set 6,(ix+$00)
z80_03df_end:
.org 0x3E3
z80_03e3:
        pop hl
z80_03e3_end:
.org 0x3E4
z80_03e4:
        ret
z80_03e4_end:
.org 0x3E5
z80_03e5:
        inc bc
z80_03e5_end:
.org 0x3E6
z80_03e6:
        ld a,(bc)
z80_03e6_end:
.org 0x3E7
z80_03e7:
        jr z80_03bf
z80_03e7_end:
.org 0x3E9
z80_03e9:
        xor a
z80_03e9_end:
.org 0x3EA
z80_03ea:
        jr z80_03bf
z80_03ea_end:
.org 0x3EC
z80_03ec:
        inc bc
z80_03ec_end:
.org 0x3ED
z80_03ed:
        ld a,(bc)
z80_03ed_end:
.org 0x3EE
z80_03ee:
        add a,(ix+$22)
z80_03ee_end:
.org 0x3F1
z80_03f1:
        ld (ix+$22),a
z80_03f1_end:
.org 0x3F4
z80_03f4:
        inc (ix+$25)
z80_03f4_end:
.org 0x3F7
z80_03f7:
        inc (ix+$25)
z80_03f7_end:
.org 0x3FA
z80_03fa:
        jr z80_03c2
z80_03fa_end:
.org 0x3FC
z80_03fc:
        ld h,$00
z80_03fc_end:
.org 0x3FE
z80_03fe:
        ld l,a
z80_03fe_end:
.org 0x3FF
z80_03ff:
        ld b,(ix+$22)
z80_03ff_end:
.org 0x402
z80_0402:
        inc b
z80_0402_end:
.org 0x403
z80_0403:
        ex de,hl
z80_0403_end:
.org 0x404
z80_0404:
        add hl,de
z80_0404_end:
.org 0x405
z80_0405:
        djnz z80_0404
z80_0405_end:
.org 0x407
z80_0407:
        inc (ix+$25)
z80_0407_end:
.org 0x40A
z80_040a:
        ret
z80_040a_end:
.org 0x40B
z80_040b:
        ld a,(ix+$0d)
z80_040b_end:
.org 0x40E
z80_040e:
        or (ix+$0e)
z80_040e_end:
.org 0x411
z80_0411:
        ret z
z80_0411_end:
.org 0x412
z80_0412:
        ld a,(ix+$00)
z80_0412_end:
.org 0x415
z80_0415:
        and $06
z80_0415_end:
.org 0x417
z80_0417:
        ret nz
z80_0417_end:
.org 0x418
z80_0418:
        ld a,(ix+$01)
z80_0418_end:
.org 0x41B
z80_041b:
        or $f0
z80_041b_end:
.org 0x41D
z80_041d:
        ld c,a
z80_041d_end:
.org 0x41E
z80_041e:
        ld a,$28
z80_041e_end:
.org 0x420
z80_0420:
        rst $0018
z80_0420_end:
.org 0x421
z80_0421:
        ret
z80_0421_end:
.org 0x422
z80_0422:
        ld a,(ix+$00)
z80_0422_end:
.org 0x425
z80_0425:
        and $06
z80_0425_end:
.org 0x427
z80_0427:
        ret nz
z80_0427_end:
.org 0x428
z80_0428:
        ld c,(ix+$01)
z80_0428_end:
.org 0x42B
z80_042b:
        bit 7,c
z80_042b_end:
.org 0x42D
z80_042d:
        ret nz
z80_042d_end:
.org 0x42E
z80_042e:
        ld a,$28
z80_042e_end:
.org 0x430
z80_0430:
        rst $0018
z80_0430_end:
.org 0x431
z80_0431:
        ret
z80_0431_end:
.org 0x432
z80_0432:
        ld b,$00
z80_0432_end:
.org 0x434
z80_0434:
        ld a,(ix+$10)
z80_0434_end:
.org 0x437
z80_0437:
        or a
z80_0437_end:
.org 0x438
z80_0438:
        jp p,$043c
z80_0438_end:
.org 0x43B
z80_043b:
        dec b
z80_043b_end:
.org 0x43C
z80_043c:
        ld h,(ix+$0e)
z80_043c_end:
.org 0x43F
z80_043f:
        ld l,(ix+$0d)
z80_043f_end:
.org 0x442
z80_0442:
        ld c,a
z80_0442_end:
.org 0x443
z80_0443:
        add hl,bc
z80_0443_end:
.org 0x444
z80_0444:
        bit 7,(ix+$01)
z80_0444_end:
.org 0x448
z80_0448:
        jr nz,z80_046c
z80_0448_end:
.org 0x44A
z80_044a:
        ex de,hl
z80_044a_end:
.org 0x44B
z80_044b:
        ld a,$07
z80_044b_end:
.org 0x44D
z80_044d:
        and d
z80_044d_end:
.org 0x44E
z80_044e:
        ld b,a
z80_044e_end:
.org 0x44F
z80_044f:
        ld c,e
z80_044f_end:
.org 0x450
z80_0450:
        or a
z80_0450_end:
.org 0x451
z80_0451:
        ld hl,$0283
z80_0451_end:
.org 0x454
z80_0454:
        sbc hl,bc
z80_0454_end:
.org 0x456
z80_0456:
        jr c,z80_045e
z80_0456_end:
.org 0x458
z80_0458:
        ld hl,$fa85
z80_0458_end:
.org 0x45B
z80_045b:
        add hl,de
z80_045b_end:
.org 0x45C
z80_045c:
        jr z80_046c
z80_045c_end:
.org 0x45E
z80_045e:
        or a
z80_045e_end:
.org 0x45F
z80_045f:
        ld hl,$0508
z80_045f_end:
.org 0x462
z80_0462:
        sbc hl,bc
z80_0462_end:
.org 0x464
z80_0464:
        jr nc,z80_046b
z80_0464_end:
.org 0x466
z80_0466:
        ld hl,$057c
z80_0466_end:
.org 0x469
z80_0469:
        add hl,de
z80_0469_end:
.org 0x46A
z80_046a:
        ex de,hl
z80_046a_end:
.org 0x46B
z80_046b:
        ex de,hl
z80_046b_end:
.org 0x46C
z80_046c:
        bit 5,(ix+$00)
z80_046c_end:
.org 0x470
z80_0470:
        ret z
z80_0470_end:
.org 0x471
z80_0471:
        ld (ix+$0e),h
z80_0471_end:
.org 0x474
z80_0474:
        ld (ix+$0d),l
z80_0474_end:
.org 0x477
z80_0477:
        ret
z80_0477_end:
.org 0x478
z80_0478:
        add hl,bc
z80_0478_end:
.org 0x479
z80_0479:
        ex af,af'
z80_0479_end:
.org 0x47A
z80_047a:
        rst $0030
z80_047a_end:
.org 0x47B
z80_047b:
        ex af,af'
z80_047b_end:
.org 0x47C
z80_047c:
        ret
z80_047c_end:
.org 0x47D
z80_047d:
        ld b,$00
z80_047d_end:
.org 0x47F
z80_047f:
        add hl,bc
z80_047f_end:
.org 0x480
z80_0480:
        ld c,l
z80_0480_end:
.org 0x481
z80_0481:
        ld b,h
z80_0481_end:
.org 0x482
z80_0482:
        ld a,(bc)
z80_0482_end:
.org 0x483
z80_0483:
        ret
z80_0483_end:
.org 0x484
z80_0484:
        ld hl,($1c37)
z80_0484_end:
.org 0x487
z80_0487:
        ld a,($1c19)
z80_0487_end:
.org 0x48A
z80_048a:
        or a
z80_048a_end:
.org 0x48B
z80_048b:
        jr z,z80_0493
z80_048b_end:
.org 0x48D
z80_048d:
        ld l,(ix+$2a)
z80_048d_end:
.org 0x490
z80_0490:
        ld h,(ix+$2b)
z80_0490_end:
.org 0x493
z80_0493:
        xor a
z80_0493_end:
.org 0x494
z80_0494:
        or b
z80_0494_end:
.org 0x495
z80_0495:
        jr z,z80_049d
z80_0495_end:
.org 0x497
z80_0497:
        ld de,$0019
z80_0497_end:
.org 0x49A
z80_049a:
        add hl,de
z80_049a_end:
.org 0x49B
z80_049b:
        djnz z80_049a
z80_049b_end:
.org 0x49D
z80_049d:
        ret
z80_049d_end:
.org 0x49E
z80_049e:
        bit 2,(ix+$01)
z80_049e_end:
.org 0x4A2
z80_04a2:
        jr nz,z80_04b5
z80_04a2_end:
.org 0x4A4
z80_04a4:
        bit 2,(ix+$00)
z80_04a4_end:
.org 0x4A8
z80_04a8:
        ret nz
z80_04a8_end:
.org 0x4A9
z80_04a9:
        add a,(ix+$01)
z80_04a9_end:
.org 0x4AC
z80_04ac:
        ld ($4000),a
z80_04ac_end:
.org 0x4AF
z80_04af:
        rst $0008
z80_04af_end:
.org 0x4B0
z80_04b0:
        ld a,c
z80_04b0_end:
.org 0x4B1
z80_04b1:
        ld ($4001),a
z80_04b1_end:
.org 0x4B4
z80_04b4:
        ret
z80_04b4_end:
.org 0x4B5
z80_04b5:
        bit 2,(ix+$00)
z80_04b5_end:
.org 0x4B9
z80_04b9:
        ret nz
z80_04b9_end:
.org 0x4BA
z80_04ba:
        add a,(ix+$01)
z80_04ba_end:
.org 0x4BD
z80_04bd:
        sub $04
z80_04bd_end:
.org 0x4BF
z80_04bf:
        ld ($4002),a
z80_04bf_end:
.org 0x4C2
z80_04c2:
        rst $0008
z80_04c2_end:
.org 0x4C3
z80_04c3:
        ld a,c
z80_04c3_end:
.org 0x4C4
z80_04c4:
        ld ($4003),a
z80_04c4_end:
.org 0x4C7
z80_04c7:
        ret
z80_04c7_end:
.org 0x4E5
z80_04e5:
        ld de,$04c8
z80_04e5_end:
.org 0x4E8
z80_04e8:
        ld c,(ix+$0a)
z80_04e8_end:
.org 0x4EB
z80_04eb:
        ld a,$b4
z80_04eb_end:
.org 0x4ED
z80_04ed:
        rst $0010
z80_04ed_end:
.org 0x4EE
z80_04ee:
        call $0504
z80_04ee_end:
.org 0x4F1
z80_04f1:
        ld (ix+$1b),a
z80_04f1_end:
.org 0x4F4
z80_04f4:
        ld b,$14
z80_04f4_end:
.org 0x4F6
z80_04f6:
        call $0504
z80_04f6_end:
.org 0x4F9
z80_04f9:
        djnz z80_04f6
z80_04f9_end:
.org 0x4FB
z80_04fb:
        ld (ix+$1c),l
z80_04fb_end:
.org 0x4FE
z80_04fe:
        ld (ix+$1d),h
z80_04fe_end:
.org 0x501
z80_0501:
        jp $0d8a
z80_0501_end:
.org 0x504
z80_0504:
        ld a,(de)
z80_0504_end:
.org 0x505
z80_0505:
        inc de
z80_0505_end:
.org 0x506
z80_0506:
        ld c,(hl)
z80_0506_end:
.org 0x507
z80_0507:
        inc hl
z80_0507_end:
.org 0x508
z80_0508:
        rst $0010
z80_0508_end:
.org 0x509
z80_0509:
        ret
z80_0509_end:
.org 0x50A
z80_050a:
        ld a,($1c09)
z80_050a_end:
.org 0x50D
z80_050d:
        bit 7,a
z80_050d_end:
.org 0x50F
z80_050f:
        jp z,$07e7
z80_050f_end:
.org 0x512
z80_0512:
        cp $a0
z80_0512_end:
.org 0x514
z80_0514:
        jp c,$0556
z80_0514_end:
.org 0x517
z80_0517:
        cp $b0
z80_0517_end:
.org 0x519
z80_0519:
        jp c,$0600
z80_0519_end:
.org 0x51C
z80_051c:
        cp $e0
z80_051c_end:
.org 0x51E
z80_051e:
        jp c,$05f7
z80_051e_end:
.org 0x521
z80_0521:
        cp $f9
z80_0521_end:
.org 0x523
z80_0523:
        jp nc,$07e7
z80_0523_end:
.org 0x526
z80_0526:
        sub $e0
z80_0526_end:
.org 0x528
z80_0528:
        ld hl,$052d
z80_0528_end:
.org 0x52B
z80_052b:
        rst $0028
z80_052b_end:
.org 0x52C
z80_052c:
        jp (hl)
z80_052c_end:
.org 0x535
z80_0535:
        ld ix,$1e20
z80_0535_end:
.org 0x539
z80_0539:
        ld b,$02
z80_0539_end:
.org 0x53B
z80_053b:
        ld a,$80
z80_053b_end:
.org 0x53D
z80_053d:
        ld ($1c19),a
z80_053d_end:
.org 0x540
z80_0540:
        push bc
z80_0540_end:
.org 0x541
z80_0541:
        bit 7,(ix+$00)
z80_0541_end:
.org 0x545
z80_0545:
        call nz,$0551
z80_0545_end:
.org 0x548
z80_0548:
        ld de,$0030
z80_0548_end:
.org 0x54B
z80_054b:
        add ix,de
z80_054b_end:
.org 0x54D
z80_054d:
        pop bc
z80_054d_end:
.org 0x54E
z80_054e:
        djnz z80_0540
z80_054e_end:
.org 0x550
z80_0550:
        ret
z80_0550_end:
.org 0x551
z80_0551:
        push hl
z80_0551_end:
.org 0x552
z80_0552:
        push hl
z80_0552_end:
.org 0x553
z80_0553:
        jp $0e27
z80_0553_end:
.org 0x556
z80_0556:
        sub $81
z80_0556_end:
.org 0x558
z80_0558:
        ret m
z80_0558_end:
.org 0x559
z80_0559:
        push af
z80_0559_end:
.org 0x55A
z80_055a:
        call $07e7
z80_055a_end:
.org 0x55D
z80_055d:
        pop af
z80_055d_end:
.org 0x55E
z80_055e:
        ld c,$04
z80_055e_end:
.org 0x560
z80_0560:
        rst $0020
z80_0560_end:
.org 0x561
z80_0561:
        rst $0028
z80_0561_end:
.org 0x562
z80_0562:
        push hl
z80_0562_end:
.org 0x563
z80_0563:
        push hl
z80_0563_end:
.org 0x564
z80_0564:
        rst $0030
z80_0564_end:
.org 0x565
z80_0565:
        ld ($1c37),hl
z80_0565_end:
.org 0x568
z80_0568:
        pop hl
z80_0568_end:
.org 0x569
z80_0569:
        pop iy
z80_0569_end:
.org 0x56B
z80_056b:
        ld a,(iy+$05)
z80_056b_end:
.org 0x56E
z80_056e:
        ld ($1c13),a
z80_056e_end:
.org 0x571
z80_0571:
        ld ($1c14),a
z80_0571_end:
.org 0x574
z80_0574:
        ld de,$0006
z80_0574_end:
.org 0x577
z80_0577:
        add hl,de
z80_0577_end:
.org 0x578
z80_0578:
        ld ($1c33),hl
z80_0578_end:
.org 0x57B
z80_057b:
        ld hl,$05e3
z80_057b_end:
.org 0x57E
z80_057e:
        ld ($1c35),hl
z80_057e_end:
.org 0x581
z80_0581:
        ld de,$1c40
z80_0581_end:
.org 0x584
z80_0584:
        ld b,(iy+$02)
z80_0584_end:
.org 0x587
z80_0587:
        ld a,(iy+$04)
z80_0587_end:
.org 0x58A
z80_058a:
        push bc
z80_058a_end:
.org 0x58B
z80_058b:
        ld hl,($1c35)
z80_058b_end:
.org 0x58E
z80_058e:
        ldi
z80_058e_end:
.org 0x590
z80_0590:
        ldi
z80_0590_end:
.org 0x592
z80_0592:
        ld (de),a
z80_0592_end:
.org 0x593
z80_0593:
        inc de
z80_0593_end:
.org 0x594
z80_0594:
        ld ($1c35),hl
z80_0594_end:
.org 0x597
z80_0597:
        ld hl,($1c33)
z80_0597_end:
.org 0x59A
z80_059a:
        ldi
z80_059a_end:
.org 0x59C
z80_059c:
        ldi
z80_059c_end:
.org 0x59E
z80_059e:
        ldi
z80_059e_end:
.org 0x5A0
z80_05a0:
        ldi
z80_05a0_end:
.org 0x5A2
z80_05a2:
        ld ($1c33),hl
z80_05a2_end:
.org 0x5A5
z80_05a5:
        call $06c2
z80_05a5_end:
.org 0x5A8
z80_05a8:
        pop bc
z80_05a8_end:
.org 0x5A9
z80_05a9:
        djnz z80_058a
z80_05a9_end:
.org 0x5AB
z80_05ab:
        ld a,(iy+$03)
z80_05ab_end:
.org 0x5AE
z80_05ae:
        or a
z80_05ae_end:
.org 0x5AF
z80_05af:
        jp z,$05dd
z80_05af_end:
.org 0x5B2
z80_05b2:
        ld b,a
z80_05b2_end:
.org 0x5B3
z80_05b3:
        ld hl,$05f1
z80_05b3_end:
.org 0x5B6
z80_05b6:
        ld ($1c35),hl
z80_05b6_end:
.org 0x5B9
z80_05b9:
        ld de,$1d90
z80_05b9_end:
.org 0x5BC
z80_05bc:
        ld a,(iy+$04)
z80_05bc_end:
.org 0x5BF
z80_05bf:
        push bc
z80_05bf_end:
.org 0x5C0
z80_05c0:
        ld hl,($1c35)
z80_05c0_end:
.org 0x5C3
z80_05c3:
        ldi
z80_05c3_end:
.org 0x5C5
z80_05c5:
        ldi
z80_05c5_end:
.org 0x5C7
z80_05c7:
        ld (de),a
z80_05c7_end:
.org 0x5C8
z80_05c8:
        inc de
z80_05c8_end:
.org 0x5C9
z80_05c9:
        ld ($1c35),hl
z80_05c9_end:
.org 0x5CC
z80_05cc:
        ld hl,($1c33)
z80_05cc_end:
.org 0x5CF
z80_05cf:
        ld bc,$0006
z80_05cf_end:
.org 0x5D2
z80_05d2:
        ldir
z80_05d2_end:
.org 0x5D4
z80_05d4:
        ld ($1c33),hl
z80_05d4_end:
.org 0x5D7
z80_05d7:
        call $06c9
z80_05d7_end:
.org 0x5DA
z80_05da:
        pop bc
z80_05da_end:
.org 0x5DB
z80_05db:
        djnz z80_05bf
z80_05db_end:
.org 0x5DD
z80_05dd:
        ld a,$80
z80_05dd_end:
.org 0x5DF
z80_05df:
        ld ($1c09),a
z80_05df_end:
.org 0x5E2
z80_05e2:
        ret
z80_05e2_end:
.org 0x5F7
z80_05f7:
        sub $d0
z80_05f7_end:
.org 0x5F9
z80_05f9:
        ex af,af'
z80_05f9_end:
.org 0x5FA
z80_05fa:
        ld a,$80
z80_05fa_end:
.org 0x5FC
z80_05fc:
        ld c,$02
z80_05fc_end:
.org 0x5FE
z80_05fe:
        jr z80_0606
z80_05fe_end:
.org 0x600
z80_0600:
        sub $a0
z80_0600_end:
.org 0x602
z80_0602:
        ex af,af'
z80_0602_end:
.org 0x603
z80_0603:
        xor a
z80_0603_end:
.org 0x604
z80_0604:
        ld c,$06
z80_0604_end:
.org 0x606
z80_0606:
        ld ($1c19),a
z80_0606_end:
.org 0x609
z80_0609:
        ex af,af'
z80_0609_end:
.org 0x60A
z80_060a:
        rst $0020
z80_060a_end:
.org 0x60B
z80_060b:
        rst $0028
z80_060b_end:
.org 0x60C
z80_060c:
        push hl
z80_060c_end:
.org 0x60D
z80_060d:
        rst $0030
z80_060d_end:
.org 0x60E
z80_060e:
        ld ($1c39),hl
z80_060e_end:
.org 0x611
z80_0611:
        xor a
z80_0611_end:
.org 0x612
z80_0612:
        ld ($1c15),a
z80_0612_end:
.org 0x615
z80_0615:
        pop hl
z80_0615_end:
.org 0x616
z80_0616:
        push hl
z80_0616_end:
.org 0x617
z80_0617:
        pop iy
z80_0617_end:
.org 0x619
z80_0619:
        ld a,(iy+$02)
z80_0619_end:
.org 0x61C
z80_061c:
        ld ($1c3b),a
z80_061c_end:
.org 0x61F
z80_061f:
        ld de,$0004
z80_061f_end:
.org 0x622
z80_0622:
        add hl,de
z80_0622_end:
.org 0x623
z80_0623:
        ld b,(iy+$03)
z80_0623_end:
.org 0x626
z80_0626:
        push bc
z80_0626_end:
.org 0x627
z80_0627:
        push hl
z80_0627_end:
.org 0x628
z80_0628:
        inc hl
z80_0628_end:
.org 0x629
z80_0629:
        ld c,(hl)
z80_0629_end:
.org 0x62A
z80_062a:
        call $0689
z80_062a_end:
.org 0x62D
z80_062d:
        set 2,(hl)
z80_062d_end:
.org 0x62F
z80_062f:
        push ix
z80_062f_end:
.org 0x631
z80_0631:
        ld a,($1c19)
z80_0631_end:
.org 0x634
z80_0634:
        or a
z80_0634_end:
.org 0x635
z80_0635:
        jr z,z80_063a
z80_0635_end:
.org 0x637
z80_0637:
        pop hl
z80_0637_end:
.org 0x638
z80_0638:
        push iy
z80_0638_end:
.org 0x63A
z80_063a:
        pop de
z80_063a_end:
.org 0x63B
z80_063b:
        pop hl
z80_063b_end:
.org 0x63C
z80_063c:
        ldi
z80_063c_end:
.org 0x63E
z80_063e:
        ld a,(de)
z80_063e_end:
.org 0x63F
z80_063f:
        cp $02
z80_063f_end:
.org 0x641
z80_0641:
        call z,$0811
z80_0641_end:
.org 0x644
z80_0644:
        ldi
z80_0644_end:
.org 0x646
z80_0646:
        ld a,($1c3b)
z80_0646_end:
.org 0x649
z80_0649:
        ld (de),a
z80_0649_end:
.org 0x64A
z80_064a:
        inc de
z80_064a_end:
.org 0x64B
z80_064b:
        ldi
z80_064b_end:
.org 0x64D
z80_064d:
        ldi
z80_064d_end:
.org 0x64F
z80_064f:
        ldi
z80_064f_end:
.org 0x651
z80_0651:
        ldi
z80_0651_end:
.org 0x653
z80_0653:
        call $06c2
z80_0653_end:
.org 0x656
z80_0656:
        bit 7,(ix+$00)
z80_0656_end:
.org 0x65A
z80_065a:
        jr z,z80_0668
z80_065a_end:
.org 0x65C
z80_065c:
        ld a,(ix+$01)
z80_065c_end:
.org 0x65F
z80_065f:
        cp (iy+$01)
z80_065f_end:
.org 0x662
z80_0662:
        jr nz,z80_0668
z80_0662_end:
.org 0x664
z80_0664:
        set 2,(iy+$00)
z80_0664_end:
.org 0x668
z80_0668:
        push hl
z80_0668_end:
.org 0x669
z80_0669:
        ld hl,($1c39)
z80_0669_end:
.org 0x66C
z80_066c:
        ld a,($1c19)
z80_066c_end:
.org 0x66F
z80_066f:
        or a
z80_066f_end:
.org 0x670
z80_0670:
        jr z,z80_0676
z80_0670_end:
.org 0x672
z80_0672:
        push iy
z80_0672_end:
.org 0x674
z80_0674:
        pop ix
z80_0674_end:
.org 0x676
z80_0676:
        ld (ix+$2a),l
z80_0676_end:
.org 0x679
z80_0679:
        ld (ix+$2b),h
z80_0679_end:
.org 0x67C
z80_067c:
        call $0422
z80_067c_end:
.org 0x67F
z80_067f:
        call $081d
z80_067f_end:
.org 0x682
z80_0682:
        pop hl
z80_0682_end:
.org 0x683
z80_0683:
        pop bc
z80_0683_end:
.org 0x684
z80_0684:
        djnz z80_0626
z80_0684_end:
.org 0x686
z80_0686:
        jp $05dd
z80_0686_end:
.org 0x689
z80_0689:
        bit 7,c
z80_0689_end:
.org 0x68B
z80_068b:
        jr nz,z80_0692
z80_068b_end:
.org 0x68D
z80_068d:
        ld a,c
z80_068d_end:
.org 0x68E
z80_068e:
        sub $02
z80_068e_end:
.org 0x690
z80_0690:
        jr z80_06a8
z80_0690_end:
.org 0x692
z80_0692:
        ld a,$1f
z80_0692_end:
.org 0x694
z80_0694:
        call $0fb5
z80_0694_end:
.org 0x697
z80_0697:
        ld a,$ff
z80_0697_end:
.org 0x699
z80_0699:
        ld ($7f11),a
z80_0699_end:
.org 0x69C
z80_069c:
        ld a,c
z80_069c_end:
.org 0x69D
z80_069d:
        srl a
z80_069d_end:
.org 0x69F
z80_069f:
        srl a
z80_069f_end:
.org 0x6A1
z80_06a1:
        srl a
z80_06a1_end:
.org 0x6A3
z80_06a3:
        srl a
z80_06a3_end:
.org 0x6A5
z80_06a5:
        srl a
z80_06a5_end:
.org 0x6A7
z80_06a7:
        inc a
z80_06a7_end:
.org 0x6A8
z80_06a8:
        ld ($1c32),a
z80_06a8_end:
.org 0x6AB
z80_06ab:
        push af
z80_06ab_end:
.org 0x6AC
z80_06ac:
        ld hl,$06ec
z80_06ac_end:
.org 0x6AF
z80_06af:
        rst $0028
z80_06af_end:
.org 0x6B0
z80_06b0:
        push hl
z80_06b0_end:
.org 0x6B1
z80_06b1:
        pop ix
z80_06b1_end:
.org 0x6B3
z80_06b3:
        pop af
z80_06b3_end:
.org 0x6B4
z80_06b4:
        push af
z80_06b4_end:
.org 0x6B5
z80_06b5:
        ld hl,$06dc
z80_06b5_end:
.org 0x6B8
z80_06b8:
        rst $0028
z80_06b8_end:
.org 0x6B9
z80_06b9:
        push hl
z80_06b9_end:
.org 0x6BA
z80_06ba:
        pop iy
z80_06ba_end:
.org 0x6BC
z80_06bc:
        pop af
z80_06bc_end:
.org 0x6BD
z80_06bd:
        ld hl,$06fc
z80_06bd_end:
.org 0x6C0
z80_06c0:
        rst $0028
z80_06c0_end:
.org 0x6C1
z80_06c1:
        ret
z80_06c1_end:
.org 0x6C2
z80_06c2:
        ex af,af'
z80_06c2_end:
.org 0x6C3
z80_06c3:
        xor a
z80_06c3_end:
.org 0x6C4
z80_06c4:
        ld (de),a
z80_06c4_end:
.org 0x6C5
z80_06c5:
        inc de
z80_06c5_end:
.org 0x6C6
z80_06c6:
        ld (de),a
z80_06c6_end:
.org 0x6C7
z80_06c7:
        inc de
z80_06c7_end:
.org 0x6C8
z80_06c8:
        ex af,af'
z80_06c8_end:
.org 0x6C9
z80_06c9:
        ex de,hl
z80_06c9_end:
.org 0x6CA
z80_06ca:
        ld (hl),$30
z80_06ca_end:
.org 0x6CC
z80_06cc:
        inc hl
z80_06cc_end:
.org 0x6CD
z80_06cd:
        ld (hl),$c0
z80_06cd_end:
.org 0x6CF
z80_06cf:
        inc hl
z80_06cf_end:
.org 0x6D0
z80_06d0:
        ld (hl),$01
z80_06d0_end:
.org 0x6D2
z80_06d2:
        ld b,$24
z80_06d2_end:
.org 0x6D4
z80_06d4:
        inc hl
z80_06d4_end:
.org 0x6D5
z80_06d5:
        ld (hl),$00
z80_06d5_end:
.org 0x6D7
z80_06d7:
        djnz z80_06d4
z80_06d7_end:
.org 0x6D9
z80_06d9:
        inc hl
z80_06d9_end:
.org 0x6DA
z80_06da:
        ex de,hl
z80_06da_end:
.org 0x6DB
z80_06db:
        ret
z80_06db_end:
.org 0x70C
z80_070c:
        ld a,($1c01)
z80_070c_end:
.org 0x70F
z80_070f:
        rlca
z80_070f_end:
.org 0x710
z80_0710:
        ld ($6000),a
z80_0710_end:
.org 0x713
z80_0713:
        ld b,$08
z80_0713_end:
.org 0x715
z80_0715:
        ld a,($1c00)
z80_0715_end:
.org 0x718
z80_0718:
        ld ($6000),a
z80_0718_end:
.org 0x71B
z80_071b:
        rrca
z80_071b_end:
.org 0x71C
z80_071c:
        djnz z80_0718
z80_071c_end:
.org 0x71E
z80_071e:
        ret
z80_071e_end:
.org 0x71F
z80_071f:
        ld hl,$1c10
z80_071f_end:
.org 0x722
z80_0722:
        ld a,(hl)
z80_0722_end:
.org 0x723
z80_0723:
        or a
z80_0723_end:
.org 0x724
z80_0724:
        ret z
z80_0724_end:
.org 0x725
z80_0725:
        jp m,$0730
z80_0725_end:
.org 0x728
z80_0728:
        pop de
z80_0728_end:
.org 0x729
z80_0729:
        dec a
z80_0729_end:
.org 0x72A
z80_072a:
        ret nz
z80_072a_end:
.org 0x72B
z80_072b:
        ld (hl),$02
z80_072b_end:
.org 0x72D
z80_072d:
        jp $0824
z80_072d_end:
.org 0x730
z80_0730:
        xor a
z80_0730_end:
.org 0x731
z80_0731:
        ld (hl),a
z80_0731_end:
.org 0x732
z80_0732:
        ld a,($1c0d)
z80_0732_end:
.org 0x735
z80_0735:
        or a
z80_0735_end:
.org 0x736
z80_0736:
        jp nz,$07e7
z80_0736_end:
.org 0x739
z80_0739:
        ld ix,$1c70
z80_0739_end:
.org 0x73D
z80_073d:
        ld b,$06
z80_073d_end:
.org 0x73F
z80_073f:
        ld a,($1c11)
z80_073f_end:
.org 0x742
z80_0742:
        or a
z80_0742_end:
.org 0x743
z80_0743:
        jr nz,z80_074b
z80_0743_end:
.org 0x745
z80_0745:
        bit 7,(ix+$00)
z80_0745_end:
.org 0x749
z80_0749:
        jr z,z80_0751
z80_0749_end:
.org 0x74B
z80_074b:
        ld c,(ix+$0a)
z80_074b_end:
.org 0x74E
z80_074e:
        ld a,$b4
z80_074e_end:
.org 0x750
z80_0750:
        rst $0010
z80_0750_end:
.org 0x751
z80_0751:
        ld de,$0030
z80_0751_end:
.org 0x754
z80_0754:
        add ix,de
z80_0754_end:
.org 0x756
z80_0756:
        djnz z80_073f
z80_0756_end:
.org 0x758
z80_0758:
        ld ix,$1e20
z80_0758_end:
.org 0x75C
z80_075c:
        ld b,$08
z80_075c_end:
.org 0x75E
z80_075e:
        bit 7,(ix+$00)
z80_075e_end:
.org 0x762
z80_0762:
        jr z,z80_0770
z80_0762_end:
.org 0x764
z80_0764:
        bit 7,(ix+$01)
z80_0764_end:
.org 0x768
z80_0768:
        jr nz,z80_0770
z80_0768_end:
.org 0x76A
z80_076a:
        ld c,(ix+$0a)
z80_076a_end:
.org 0x76D
z80_076d:
        ld a,$b4
z80_076d_end:
.org 0x76F
z80_076f:
        rst $0010
z80_076f_end:
.org 0x770
z80_0770:
        ld de,$0030
z80_0770_end:
.org 0x773
z80_0773:
        add ix,de
z80_0773_end:
.org 0x775
z80_0775:
        djnz z80_075e
z80_0775_end:
.org 0x777
z80_0777:
        ret
z80_0777_end:
.org 0x778
z80_0778:
        ld a,$28
z80_0778_end:
.org 0x77A
z80_077a:
        ld ($1c0d),a
z80_077a_end:
.org 0x77D
z80_077d:
        ld a,$06
z80_077d_end:
.org 0x77F
z80_077f:
        ld ($1c0f),a
z80_077f_end:
.org 0x782
z80_0782:
        ld ($1c0e),a
z80_0782_end:
.org 0x785
z80_0785:
        xor a
z80_0785_end:
.org 0x786
z80_0786:
        ld ($1c40),a
z80_0786_end:
.org 0x789
z80_0789:
        ld ($1d60),a
z80_0789_end:
.org 0x78C
z80_078c:
        ld ($1df0),a
z80_078c_end:
.org 0x78F
z80_078f:
        ld ($1d90),a
z80_078f_end:
.org 0x792
z80_0792:
        ld ($1dc0),a
z80_0792_end:
.org 0x795
z80_0795:
        call $084f
z80_0795_end:
.org 0x798
z80_0798:
        jp $05dd
z80_0798_end:
.org 0x79B
z80_079b:
        ld hl,$1c0d
z80_079b_end:
.org 0x79E
z80_079e:
        ld a,(hl)
z80_079e_end:
.org 0x79F
z80_079f:
        or a
z80_079f_end:
.org 0x7A0
z80_07a0:
        ret z
z80_07a0_end:
.org 0x7A1
z80_07a1:
        call m,$0785
z80_07a1_end:
.org 0x7A4
z80_07a4:
        res 7,(hl)
z80_07a4_end:
.org 0x7A6
z80_07a6:
        ld a,($1c0f)
z80_07a6_end:
.org 0x7A9
z80_07a9:
        dec a
z80_07a9_end:
.org 0x7AA
z80_07aa:
        jr z,z80_07b0
z80_07aa_end:
.org 0x7AC
z80_07ac:
        ld ($1c0f),a
z80_07ac_end:
.org 0x7AF
z80_07af:
        ret
z80_07af_end:
.org 0x7B0
z80_07b0:
        ld a,($1c0e)
z80_07b0_end:
.org 0x7B3
z80_07b3:
        ld ($1c0f),a
z80_07b3_end:
.org 0x7B6
z80_07b6:
        ld a,($1c0d)
z80_07b6_end:
.org 0x7B9
z80_07b9:
        dec a
z80_07b9_end:
.org 0x7BA
z80_07ba:
        ld ($1c0d),a
z80_07ba_end:
.org 0x7BD
z80_07bd:
        jr z,z80_07e7
z80_07bd_end:
.org 0x7BF
z80_07bf:
        ld ix,$1c40
z80_07bf_end:
.org 0x7C3
z80_07c3:
        ld b,$06
z80_07c3_end:
.org 0x7C5
z80_07c5:
        inc (ix+$06)
z80_07c5_end:
.org 0x7C8
z80_07c8:
        jp p,$07d0
z80_07c8_end:
.org 0x7CB
z80_07cb:
        dec (ix+$06)
z80_07cb_end:
.org 0x7CE
z80_07ce:
        jr z80_07df
z80_07ce_end:
.org 0x7D0
z80_07d0:
        bit 7,(ix+$00)
z80_07d0_end:
.org 0x7D4
z80_07d4:
        jr z,z80_07df
z80_07d4_end:
.org 0x7D6
z80_07d6:
        bit 2,(ix+$00)
z80_07d6_end:
.org 0x7DA
z80_07da:
        jr nz,z80_07df
z80_07da_end:
.org 0x7DC
z80_07dc:
        call $0d8a
z80_07dc_end:
.org 0x7DF
z80_07df:
        ld de,$0030
z80_07df_end:
.org 0x7E2
z80_07e2:
        add ix,de
z80_07e2_end:
.org 0x7E4
z80_07e4:
        djnz z80_07c5
z80_07e4_end:
.org 0x7E6
z80_07e6:
        ret
z80_07e6_end:
.org 0x7E7
z80_07e7:
        ld hl,$1c09
z80_07e7_end:
.org 0x7EA
z80_07ea:
        ld de,$1c0a
z80_07ea_end:
.org 0x7ED
z80_07ed:
        ld bc,$0396
z80_07ed_end:
.org 0x7F0
z80_07f0:
        ld (hl),$00
z80_07f0_end:
.org 0x7F2
z80_07f2:
        ldir
z80_07f2_end:
.org 0x7F4
z80_07f4:
        ld ix,$05e3
z80_07f4_end:
.org 0x7F8
z80_07f8:
        ld b,$06
z80_07f8_end:
.org 0x7FA
z80_07fa:
        push bc
z80_07fa_end:
.org 0x7FB
z80_07fb:
        call $08c8
z80_07fb_end:
.org 0x7FE
z80_07fe:
        call $081d
z80_07fe_end:
.org 0x801
z80_0801:
        inc ix
z80_0801_end:
.org 0x803
z80_0803:
        inc ix
z80_0803_end:
.org 0x805
z80_0805:
        pop bc
z80_0805_end:
.org 0x806
z80_0806:
        djnz z80_07fa
z80_0806_end:
.org 0x808
z80_0808:
        ld b,$07
z80_0808_end:
.org 0x80A
z80_080a:
        xor a
z80_080a_end:
.org 0x80B
z80_080b:
        ld ($1c0d),a
z80_080b_end:
.org 0x80E
z80_080e:
        call $084f
z80_080e_end:
.org 0x811
z80_0811:
        ld a,$0f
z80_0811_end:
.org 0x813
z80_0813:
        ld ($1c12),a
z80_0813_end:
.org 0x816
z80_0816:
        ld c,a
z80_0816_end:
.org 0x817
z80_0817:
        ld a,$27
z80_0817_end:
.org 0x819
z80_0819:
        rst $0018
z80_0819_end:
.org 0x81A
z80_081a:
        jp $05dd
z80_081a_end:
.org 0x81D
z80_081d:
        ld a,$90
z80_081d_end:
.org 0x81F
z80_081f:
        ld c,$00
z80_081f_end:
.org 0x821
z80_0821:
        jp $08dc
z80_0821_end:
.org 0x824
z80_0824:
        call $084f
z80_0824_end:
.org 0x827
z80_0827:
        push bc
z80_0827_end:
.org 0x828
z80_0828:
        push af
z80_0828_end:
.org 0x829
z80_0829:
        ld b,$03
z80_0829_end:
.org 0x82B
z80_082b:
        ld a,$b4
z80_082b_end:
.org 0x82D
z80_082d:
        ld c,$00
z80_082d_end:
.org 0x82F
z80_082f:
        push af
z80_082f_end:
.org 0x830
z80_0830:
        rst $0018
z80_0830_end:
.org 0x831
z80_0831:
        pop af
z80_0831_end:
.org 0x832
z80_0832:
        inc a
z80_0832_end:
.org 0x833
z80_0833:
        djnz z80_082f
z80_0833_end:
.org 0x835
z80_0835:
        ld b,$03
z80_0835_end:
.org 0x837
z80_0837:
        ld a,$b4
z80_0837_end:
.org 0x839
z80_0839:
        push af
z80_0839_end:
.org 0x83A
z80_083a:
        call $04bf
z80_083a_end:
.org 0x83D
z80_083d:
        pop af
z80_083d_end:
.org 0x83E
z80_083e:
        inc a
z80_083e_end:
.org 0x83F
z80_083f:
        djnz z80_0839
z80_083f_end:
.org 0x841
z80_0841:
        ld c,$00
z80_0841_end:
.org 0x843
z80_0843:
        ld b,$07
z80_0843_end:
.org 0x845
z80_0845:
        ld a,$28
z80_0845_end:
.org 0x847
z80_0847:
        push af
z80_0847_end:
.org 0x848
z80_0848:
        rst $0018
z80_0848_end:
.org 0x849
z80_0849:
        inc c
z80_0849_end:
.org 0x84A
z80_084a:
        pop af
z80_084a_end:
.org 0x84B
z80_084b:
        djnz z80_0847
z80_084b_end:
.org 0x84D
z80_084d:
        pop af
z80_084d_end:
.org 0x84E
z80_084e:
        pop bc
z80_084e_end:
.org 0x84F
z80_084f:
        push hl
z80_084f_end:
.org 0x850
z80_0850:
        push bc
z80_0850_end:
.org 0x851
z80_0851:
        ld hl,$0862
z80_0851_end:
.org 0x854
z80_0854:
        ld b,$04
z80_0854_end:
.org 0x856
z80_0856:
        ld a,(hl)
z80_0856_end:
.org 0x857
z80_0857:
        ld ($7f11),a
z80_0857_end:
.org 0x85A
z80_085a:
        inc hl
z80_085a_end:
.org 0x85B
z80_085b:
        djnz z80_0856
z80_085b_end:
.org 0x85D
z80_085d:
        pop bc
z80_085d_end:
.org 0x85E
z80_085e:
        pop hl
z80_085e_end:
.org 0x85F
z80_085f:
        jp $05dd
z80_085f_end:
.org 0x866
z80_0866:
        ld hl,$1c13
z80_0866_end:
.org 0x869
z80_0869:
        ld a,(hl)
z80_0869_end:
.org 0x86A
z80_086a:
        or a
z80_086a_end:
.org 0x86B
z80_086b:
        ret z
z80_086b_end:
.org 0x86C
z80_086c:
        dec (hl)
z80_086c_end:
.org 0x86D
z80_086d:
        ret nz
z80_086d_end:
.org 0x86E
z80_086e:
        ld a,($1c14)
z80_086e_end:
.org 0x871
z80_0871:
        ld (hl),a
z80_0871_end:
.org 0x872
z80_0872:
        ld hl,$1c4b
z80_0872_end:
.org 0x875
z80_0875:
        ld de,$0030
z80_0875_end:
.org 0x878
z80_0878:
        ld b,$0a
z80_0878_end:
.org 0x87A
z80_087a:
        inc (hl)
z80_087a_end:
.org 0x87B
z80_087b:
        add hl,de
z80_087b_end:
.org 0x87C
z80_087c:
        djnz z80_087a
z80_087c_end:
.org 0x87E
z80_087e:
        ret
z80_087e_end:
.org 0x87F
z80_087f:
        ld a,r
z80_087f_end:
.org 0x881
z80_0881:
        ld ($1c17),a
z80_0881_end:
.org 0x884
z80_0884:
        ld de,$1c0a
z80_0884_end:
.org 0x887
z80_0887:
        call $0893
z80_0887_end:
.org 0x88A
z80_088a:
        ld de,$1c0b
z80_088a_end:
.org 0x88D
z80_088d:
        call $0893
z80_088d_end:
.org 0x890
z80_0890:
        ld de,$1c0c
z80_0890_end:
.org 0x893
z80_0893:
        ld a,(de)
z80_0893_end:
.org 0x894
z80_0894:
        bit 7,a
z80_0894_end:
.org 0x896
z80_0896:
        ret z
z80_0896_end:
.org 0x897
z80_0897:
        sub $81
z80_0897_end:
.org 0x899
z80_0899:
        ld hl,($1c02)
z80_0899_end:
.org 0x89C
z80_089c:
        ld c,$00
z80_089c_end:
.org 0x89E
z80_089e:
        rst $0020
z80_089e_end:
.org 0x89F
z80_089f:
        ld c,a
z80_089f_end:
.org 0x8A0
z80_08a0:
        ld b,$00
z80_08a0_end:
.org 0x8A2
z80_08a2:
        add hl,bc
z80_08a2_end:
.org 0x8A3
z80_08a3:
        bit 7,(hl)
z80_08a3_end:
.org 0x8A5
z80_08a5:
        jr z,z80_08b5
z80_08a5_end:
.org 0x8A7
z80_08a7:
        ld a,(de)
z80_08a7_end:
.org 0x8A8
z80_08a8:
        ld ($1c09),a
z80_08a8_end:
.org 0x8AB
z80_08ab:
        xor a
z80_08ab_end:
.org 0x8AC
z80_08ac:
        ld hl,$1c0a
z80_08ac_end:
.org 0x8AF
z80_08af:
        ld (hl),a
z80_08af_end:
.org 0x8B0
z80_08b0:
        inc hl
z80_08b0_end:
.org 0x8B1
z80_08b1:
        ld (hl),a
z80_08b1_end:
.org 0x8B2
z80_08b2:
        inc hl
z80_08b2_end:
.org 0x8B3
z80_08b3:
        ld (hl),a
z80_08b3_end:
.org 0x8B4
z80_08b4:
        ret
z80_08b4_end:
.org 0x8B5
z80_08b5:
        ld a,($1c18)
z80_08b5_end:
.org 0x8B8
z80_08b8:
        cp (hl)
z80_08b8_end:
.org 0x8B9
z80_08b9:
        jr z,z80_08bd
z80_08b9_end:
.org 0x8BB
z80_08bb:
        jr nc,z80_08c5
z80_08bb_end:
.org 0x8BD
z80_08bd:
        ld a,(de)
z80_08bd_end:
.org 0x8BE
z80_08be:
        ld ($1c09),a
z80_08be_end:
.org 0x8C1
z80_08c1:
        ld a,(hl)
z80_08c1_end:
.org 0x8C2
z80_08c2:
        ld ($1c18),a
z80_08c2_end:
.org 0x8C5
z80_08c5:
        xor a
z80_08c5_end:
.org 0x8C6
z80_08c6:
        ld (de),a
z80_08c6_end:
.org 0x8C7
z80_08c7:
        ret
z80_08c7_end:
.org 0x8C8
z80_08c8:
        call $08d8
z80_08c8_end:
.org 0x8CB
z80_08cb:
        ld a,$40
z80_08cb_end:
.org 0x8CD
z80_08cd:
        ld c,$7f
z80_08cd_end:
.org 0x8CF
z80_08cf:
        call $08dc
z80_08cf_end:
.org 0x8D2
z80_08d2:
        ld c,(ix+$01)
z80_08d2_end:
.org 0x8D5
z80_08d5:
        jp $042e
z80_08d5_end:
.org 0x8D8
z80_08d8:
        ld a,$80
z80_08d8_end:
.org 0x8DA
z80_08da:
        ld c,$ff
z80_08da_end:
.org 0x8DC
z80_08dc:
        ld b,$04
z80_08dc_end:
.org 0x8DE
z80_08de:
        push af
z80_08de_end:
.org 0x8DF
z80_08df:
        rst $0010
z80_08df_end:
.org 0x8E0
z80_08e0:
        pop af
z80_08e0_end:
.org 0x8E1
z80_08e1:
        add a,$04
z80_08e1_end:
.org 0x8E3
z80_08e3:
        djnz z80_08de
z80_08e3_end:
.org 0x8E5
z80_08e5:
        ret
z80_08e5_end:
.org 0x988
z80_0988:
        call $0304
z80_0988_end:
.org 0x98B
z80_098b:
        call z,$098f
z80_098b_end:
.org 0x98E
z80_098e:
        ret
z80_098e_end:
.org 0x98F
z80_098f:
        ld e,(ix+$03)
z80_098f_end:
.org 0x992
z80_0992:
        ld d,(ix+$04)
z80_0992_end:
.org 0x995
z80_0995:
        ld a,(de)
z80_0995_end:
.org 0x996
z80_0996:
        inc de
z80_0996_end:
.org 0x997
z80_0997:
        cp $e0
z80_0997_end:
.org 0x999
z80_0999:
        jp nc,$0a3c
z80_0999_end:
.org 0x99C
z80_099c:
        or a
z80_099c_end:
.org 0x99D
z80_099d:
        jp m,$09a4
z80_099d_end:
.org 0x9A0
z80_09a0:
        dec de
z80_09a0_end:
.org 0x9A1
z80_09a1:
        ld a,(ix+$0d)
z80_09a1_end:
.org 0x9A4
z80_09a4:
        ld (ix+$0d),a
z80_09a4_end:
.org 0x9A7
z80_09a7:
        cp $80
z80_09a7_end:
.org 0x9A9
z80_09a9:
        jp z,$0a26
z80_09a9_end:
.org 0x9AC
z80_09ac:
        push de
z80_09ac_end:
.org 0x9AD
z80_09ad:
        ld hl,$1d60
z80_09ad_end:
.org 0x9B0
z80_09b0:
        bit 2,(hl)
z80_09b0_end:
.org 0x9B2
z80_09b2:
        jr nz,z80_09f8
z80_09b2_end:
.org 0x9B4
z80_09b4:
        and $0f
z80_09b4_end:
.org 0x9B6
z80_09b6:
        jr z,z80_09f8
z80_09b6_end:
.org 0x9B8
z80_09b8:
        ex af,af'
z80_09b8_end:
.org 0x9B9
z80_09b9:
        call $0422
z80_09b9_end:
.org 0x9BC
z80_09bc:
        ex af,af'
z80_09bc_end:
.org 0x9BD
z80_09bd:
        ld de,$0a36
z80_09bd_end:
.org 0x9C0
z80_09c0:
        ex de,hl
z80_09c0_end:
.org 0x9C1
z80_09c1:
        ldi
z80_09c1_end:
.org 0x9C3
z80_09c3:
        ldi
z80_09c3_end:
.org 0x9C5
z80_09c5:
        ldi
z80_09c5_end:
.org 0x9C7
z80_09c7:
        dec a
z80_09c7_end:
.org 0x9C8
z80_09c8:
        ld hl,$0a60
z80_09c8_end:
.org 0x9CB
z80_09cb:
        rst $0028
z80_09cb_end:
.org 0x9CC
z80_09cc:
        ld bc,$0006
z80_09cc_end:
.org 0x9CF
z80_09cf:
        ldir
z80_09cf_end:
.org 0x9D1
z80_09d1:
        call $06c9
z80_09d1_end:
.org 0x9D4
z80_09d4:
        ld hl,$1d65
z80_09d4_end:
.org 0x9D7
z80_09d7:
        ld a,(ix+$05)
z80_09d7_end:
.org 0x9DA
z80_09da:
        add a,(hl)
z80_09da_end:
.org 0x9DB
z80_09db:
        ld (hl),a
z80_09db_end:
.org 0x9DC
z80_09dc:
        ld a,($1d68)
z80_09dc_end:
.org 0x9DF
z80_09df:
        ld hl,$0a74
z80_09df_end:
.org 0x9E2
z80_09e2:
        rst $0028
z80_09e2_end:
.org 0x9E3
z80_09e3:
        ld a,($1d66)
z80_09e3_end:
.org 0x9E6
z80_09e6:
        ld e,(ix+$06)
z80_09e6_end:
.org 0x9E9
z80_09e9:
        push de
z80_09e9_end:
.org 0x9EA
z80_09ea:
        add a,e
z80_09ea_end:
.org 0x9EB
z80_09eb:
        ld (ix+$06),a
z80_09eb_end:
.org 0x9EE
z80_09ee:
        call $04e5
z80_09ee_end:
.org 0x9F1
z80_09f1:
        pop de
z80_09f1_end:
.org 0x9F2
z80_09f2:
        ld (ix+$06),e
z80_09f2_end:
.org 0x9F5
z80_09f5:
        call $0811
z80_09f5_end:
.org 0x9F8
z80_09f8:
        ld hl,$1df0
z80_09f8_end:
.org 0x9FB
z80_09fb:
        bit 2,(hl)
z80_09fb_end:
.org 0x9FD
z80_09fd:
        jr nz,z80_0a25
z80_09fd_end:
.org 0x9FF
z80_09ff:
        ld a,(ix+$0d)
z80_09ff_end:
.org 0xA02
z80_0a02:
        and $70
z80_0a02_end:
.org 0xA04
z80_0a04:
        jr z,z80_0a25
z80_0a04_end:
.org 0xA06
z80_0a06:
        ld de,$0a39
z80_0a06_end:
.org 0xA09
z80_0a09:
        ex de,hl
z80_0a09_end:
.org 0xA0A
z80_0a0a:
        ldi
z80_0a0a_end:
.org 0xA0C
z80_0a0c:
        ldi
z80_0a0c_end:
.org 0xA0E
z80_0a0e:
        ldi
z80_0a0e_end:
.org 0xA10
z80_0a10:
        srl a
z80_0a10_end:
.org 0xA12
z80_0a12:
        srl a
z80_0a12_end:
.org 0xA14
z80_0a14:
        srl a
z80_0a14_end:
.org 0xA16
z80_0a16:
        srl a
z80_0a16_end:
.org 0xA18
z80_0a18:
        dec a
z80_0a18_end:
.org 0xA19
z80_0a19:
        ld hl,$0a46
z80_0a19_end:
.org 0xA1C
z80_0a1c:
        rst $0028
z80_0a1c_end:
.org 0xA1D
z80_0a1d:
        ld bc,$0006
z80_0a1d_end:
.org 0xA20
z80_0a20:
        ldir
z80_0a20_end:
.org 0xA22
z80_0a22:
        call $06c9
z80_0a22_end:
.org 0xA25
z80_0a25:
        pop de
z80_0a25_end:
.org 0xA26
z80_0a26:
        ld a,(de)
z80_0a26_end:
.org 0xA27
z80_0a27:
        inc de
z80_0a27_end:
.org 0xA28
z80_0a28:
        or a
z80_0a28_end:
.org 0xA29
z80_0a29:
        jp p,$0276
z80_0a29_end:
.org 0xA2C
z80_0a2c:
        dec de
z80_0a2c_end:
.org 0xA2D
z80_0a2d:
        ld a,(ix+$0c)
z80_0a2d_end:
.org 0xA30
z80_0a30:
        ld (ix+$0b),a
z80_0a30_end:
.org 0xA33
z80_0a33:
        jp $027c
z80_0a33_end:
.org 0xA3C
z80_0a3c:
        ld hl,$0a42
z80_0a3c_end:
.org 0xA3F
z80_0a3f:
        jp $0b7b
z80_0a3f_end:
.org 0xB78
z80_0b78:
        ld hl,$0b84
z80_0b78_end:
.org 0xB7B
z80_0b7b:
        push hl
z80_0b7b_end:
.org 0xB7C
z80_0b7c:
        sub $e0
z80_0b7c_end:
.org 0xB7E
z80_0b7e:
        ld hl,$0b8f
z80_0b7e_end:
.org 0xB81
z80_0b81:
        rst $0028
z80_0b81_end:
.org 0xB82
z80_0b82:
        ld a,(de)
z80_0b82_end:
.org 0xB83
z80_0b83:
        jp (hl)
z80_0b83_end:
.org 0xB88
z80_0b88:
        ld hl,$0bcf
z80_0b88_end:
.org 0xB8B
z80_0b8b:
        rst $0028
z80_0b8b_end:
.org 0xB8C
z80_0b8c:
        inc de
z80_0b8c_end:
.org 0xB8D
z80_0b8d:
        ld a,(de)
z80_0b8d_end:
.org 0xB8E
z80_0b8e:
        jp (hl)
z80_0b8e_end:
.org 0xBDF
z80_0bdf:
        ld (ix+$18),$80
z80_0bdf_end:
.org 0xBE3
z80_0be3:
        ld (ix+$19),e
z80_0be3_end:
.org 0xBE6
z80_0be6:
        ld (ix+$1a),d
z80_0be6_end:
.org 0xBE9
z80_0be9:
        ld hl,$04e1
z80_0be9_end:
.org 0xBEC
z80_0bec:
        ld b,$04
z80_0bec_end:
.org 0xBEE
z80_0bee:
        ld a,(de)
z80_0bee_end:
.org 0xBEF
z80_0bef:
        inc de
z80_0bef_end:
.org 0xBF0
z80_0bf0:
        ld c,a
z80_0bf0_end:
.org 0xBF1
z80_0bf1:
        ld a,(hl)
z80_0bf1_end:
.org 0xBF2
z80_0bf2:
        inc hl
z80_0bf2_end:
.org 0xBF3
z80_0bf3:
        rst $0010
z80_0bf3_end:
.org 0xBF4
z80_0bf4:
        djnz z80_0bee
z80_0bf4_end:
.org 0xBF6
z80_0bf6:
        dec de
z80_0bf6_end:
.org 0xBF7
z80_0bf7:
        ret
z80_0bf7_end:
.org 0xBF8
z80_0bf8:
        exx
z80_0bf8_end:
.org 0xBF9
z80_0bf9:
        ld b,$0a
z80_0bf9_end:
.org 0xBFB
z80_0bfb:
        ld de,$0030
z80_0bfb_end:
.org 0xBFE
z80_0bfe:
        ld hl,$1c42
z80_0bfe_end:
.org 0xC01
z80_0c01:
        ld (hl),a
z80_0c01_end:
.org 0xC02
z80_0c02:
        add hl,de
z80_0c02_end:
.org 0xC03
z80_0c03:
        djnz z80_0c01
z80_0c03_end:
.org 0xC05
z80_0c05:
        exx
z80_0c05_end:
.org 0xC06
z80_0c06:
        ret
z80_0c06_end:
.org 0xC07
z80_0c07:
        ld ($1c07),a
z80_0c07_end:
.org 0xC0A
z80_0c0a:
        ret
z80_0c0a_end:
.org 0xC0B
z80_0c0b:
        ld hl,$1c04
z80_0c0b_end:
.org 0xC0E
z80_0c0e:
        ex de,hl
z80_0c0e_end:
.org 0xC0F
z80_0c0f:
        ldi
z80_0c0f_end:
.org 0xC11
z80_0c11:
        ldi
z80_0c11_end:
.org 0xC13
z80_0c13:
        ldi
z80_0c13_end:
.org 0xC15
z80_0c15:
        ex de,hl
z80_0c15_end:
.org 0xC16
z80_0c16:
        dec de
z80_0c16_end:
.org 0xC17
z80_0c17:
        ret
z80_0c17_end:
.org 0xC18
z80_0c18:
        ex de,hl
z80_0c18_end:
.org 0xC19
z80_0c19:
        ld c,(hl)
z80_0c19_end:
.org 0xC1A
z80_0c1a:
        inc hl
z80_0c1a_end:
.org 0xC1B
z80_0c1b:
        ld b,(hl)
z80_0c1b_end:
.org 0xC1C
z80_0c1c:
        inc hl
z80_0c1c_end:
.org 0xC1D
z80_0c1d:
        ex de,hl
z80_0c1d_end:
.org 0xC1E
z80_0c1e:
        ld hl,($1c04)
z80_0c1e_end:
.org 0xC21
z80_0c21:
        add hl,bc
z80_0c21_end:
.org 0xC22
z80_0c22:
        ld ($1c04),hl
z80_0c22_end:
.org 0xC25
z80_0c25:
        ld a,(de)
z80_0c25_end:
.org 0xC26
z80_0c26:
        ld hl,$1c06
z80_0c26_end:
.org 0xC29
z80_0c29:
        add a,(hl)
z80_0c29_end:
.org 0xC2A
z80_0c2a:
        ld (hl),a
z80_0c2a_end:
.org 0xC2B
z80_0c2b:
        ret
z80_0c2b_end:
.org 0xC2C
z80_0c2c:
        push ix
z80_0c2c_end:
.org 0xC2E
z80_0c2e:
        call $050d
z80_0c2e_end:
.org 0xC31
z80_0c31:
        pop ix
z80_0c31_end:
.org 0xC33
z80_0c33:
        ret
z80_0c33_end:
.org 0xC34
z80_0c34:
        ld ($1c11),a
z80_0c34_end:
.org 0xC37
z80_0c37:
        or a
z80_0c37_end:
.org 0xC38
z80_0c38:
        jr z,z80_0c57
z80_0c38_end:
.org 0xC3A
z80_0c3a:
        push ix
z80_0c3a_end:
.org 0xC3C
z80_0c3c:
        push de
z80_0c3c_end:
.org 0xC3D
z80_0c3d:
        ld ix,$1c40
z80_0c3d_end:
.org 0xC41
z80_0c41:
        ld b,$0a
z80_0c41_end:
.org 0xC43
z80_0c43:
        ld de,$0030
z80_0c43_end:
.org 0xC46
z80_0c46:
        res 7,(ix+$00)
z80_0c46_end:
.org 0xC4A
z80_0c4a:
        call $0428
z80_0c4a_end:
.org 0xC4D
z80_0c4d:
        add ix,de
z80_0c4d_end:
.org 0xC4F
z80_0c4f:
        djnz z80_0c46
z80_0c4f_end:
.org 0xC51
z80_0c51:
        pop de
z80_0c51_end:
.org 0xC52
z80_0c52:
        pop ix
z80_0c52_end:
.org 0xC54
z80_0c54:
        jp $084f
z80_0c54_end:
.org 0xC57
z80_0c57:
        push ix
z80_0c57_end:
.org 0xC59
z80_0c59:
        push de
z80_0c59_end:
.org 0xC5A
z80_0c5a:
        ld ix,$1c40
z80_0c5a_end:
.org 0xC5E
z80_0c5e:
        ld b,$0a
z80_0c5e_end:
.org 0xC60
z80_0c60:
        ld de,$0030
z80_0c60_end:
.org 0xC63
z80_0c63:
        set 7,(ix+$00)
z80_0c63_end:
.org 0xC67
z80_0c67:
        add ix,de
z80_0c67_end:
.org 0xC69
z80_0c69:
        djnz z80_0c63
z80_0c69_end:
.org 0xC6B
z80_0c6b:
        pop de
z80_0c6b_end:
.org 0xC6C
z80_0c6c:
        pop ix
z80_0c6c_end:
.org 0xC6E
z80_0c6e:
        ret
z80_0c6e_end:
.org 0xC6F
z80_0c6f:
        ex de,hl
z80_0c6f_end:
.org 0xC70
z80_0c70:
        ld e,(hl)
z80_0c70_end:
.org 0xC71
z80_0c71:
        inc hl
z80_0c71_end:
.org 0xC72
z80_0c72:
        ld d,(hl)
z80_0c72_end:
.org 0xC73
z80_0c73:
        inc hl
z80_0c73_end:
.org 0xC74
z80_0c74:
        ld c,(hl)
z80_0c74_end:
.org 0xC75
z80_0c75:
        ld b,$00
z80_0c75_end:
.org 0xC77
z80_0c77:
        inc hl
z80_0c77_end:
.org 0xC78
z80_0c78:
        ex de,hl
z80_0c78_end:
.org 0xC79
z80_0c79:
        ldir
z80_0c79_end:
.org 0xC7B
z80_0c7b:
        dec de
z80_0c7b_end:
.org 0xC7C
z80_0c7c:
        ret
z80_0c7c_end:
.org 0xC7D
z80_0c7d:
        ld (ix+$10),a
z80_0c7d_end:
.org 0xC80
z80_0c80:
        ret
z80_0c80_end:
.org 0xC81
z80_0c81:
        ld (ix+$18),a
z80_0c81_end:
.org 0xC84
z80_0c84:
        inc de
z80_0c84_end:
.org 0xC85
z80_0c85:
        ld a,(de)
z80_0c85_end:
.org 0xC86
z80_0c86:
        ld (ix+$19),a
z80_0c86_end:
.org 0xC89
z80_0c89:
        ret
z80_0c89_end:
.org 0xC8A
z80_0c8a:
        ld hl,$1c14
z80_0c8a_end:
.org 0xC8D
z80_0c8d:
        add a,(hl)
z80_0c8d_end:
.org 0xC8E
z80_0c8e:
        ld (hl),a
z80_0c8e_end:
.org 0xC8F
z80_0c8f:
        dec hl
z80_0c8f_end:
.org 0xC90
z80_0c90:
        ld (hl),a
z80_0c90_end:
.org 0xC91
z80_0c91:
        ret
z80_0c91_end:
.org 0xC92
z80_0c92:
        ld ($1c16),a
z80_0c92_end:
.org 0xC95
z80_0c95:
        ret
z80_0c95_end:
.org 0xC96
z80_0c96:
        bit 7,(ix+$01)
z80_0c96_end:
.org 0xC9A
z80_0c9a:
        ret z
z80_0c9a_end:
.org 0xC9B
z80_0c9b:
        res 4,(ix+$00)
z80_0c9b_end:
.org 0xC9F
z80_0c9f:
        dec (ix+$17)
z80_0c9f_end:
.org 0xCA2
z80_0ca2:
        add a,(ix+$06)
z80_0ca2_end:
.org 0xCA5
z80_0ca5:
        ld (ix+$06),a
z80_0ca5_end:
.org 0xCA8
z80_0ca8:
        ret
z80_0ca8_end:
.org 0xCA9
z80_0ca9:
        call $0cb3
z80_0ca9_end:
.org 0xCAC
z80_0cac:
        rst $0010
z80_0cac_end:
.org 0xCAD
z80_0cad:
        ret
z80_0cad_end:
.org 0xCAE
z80_0cae:
        call $0cb3
z80_0cae_end:
.org 0xCB1
z80_0cb1:
        rst $0018
z80_0cb1_end:
.org 0xCB2
z80_0cb2:
        ret
z80_0cb2_end:
.org 0xCB3
z80_0cb3:
        ex de,hl
z80_0cb3_end:
.org 0xCB4
z80_0cb4:
        ld a,(hl)
z80_0cb4_end:
.org 0xCB5
z80_0cb5:
        inc hl
z80_0cb5_end:
.org 0xCB6
z80_0cb6:
        ld c,(hl)
z80_0cb6_end:
.org 0xCB7
z80_0cb7:
        ex de,hl
z80_0cb7_end:
.org 0xCB8
z80_0cb8:
        ret
z80_0cb8_end:
.org 0xCB9
z80_0cb9:
        ld (ix+$20),e
z80_0cb9_end:
.org 0xCBC
z80_0cbc:
        ld (ix+$21),d
z80_0cbc_end:
.org 0xCBF
z80_0cbf:
        ld (ix+$07),$80
z80_0cbf_end:
.org 0xCC3
z80_0cc3:
        inc de
z80_0cc3_end:
.org 0xCC4
z80_0cc4:
        inc de
z80_0cc4_end:
.org 0xCC5
z80_0cc5:
        inc de
z80_0cc5_end:
.org 0xCC6
z80_0cc6:
        ret
z80_0cc6_end:
.org 0xCC7
z80_0cc7:
        call $08c8
z80_0cc7_end:
.org 0xCCA
z80_0cca:
        jp $0e27
z80_0cca_end:
.org 0xCCD
z80_0ccd:
        call $029e
z80_0ccd_end:
.org 0xCD0
z80_0cd0:
        ld (ix+$1e),a
z80_0cd0_end:
.org 0xCD3
z80_0cd3:
        ld (ix+$1f),a
z80_0cd3_end:
.org 0xCD6
z80_0cd6:
        ret
z80_0cd6_end:
.org 0xCD7
z80_0cd7:
        push ix
z80_0cd7_end:
.org 0xCD9
z80_0cd9:
        pop hl
z80_0cd9_end:
.org 0xCDA
z80_0cda:
        ld bc,$0011
z80_0cda_end:
.org 0xCDD
z80_0cdd:
        add hl,bc
z80_0cdd_end:
.org 0xCDE
z80_0cde:
        ex de,hl
z80_0cde_end:
.org 0xCDF
z80_0cdf:
        ld bc,$0005
z80_0cdf_end:
.org 0xCE2
z80_0ce2:
        ldir
z80_0ce2_end:
.org 0xCE4
z80_0ce4:
        ld a,$01
z80_0ce4_end:
.org 0xCE6
z80_0ce6:
        ld (de),a
z80_0ce6_end:
.org 0xCE7
z80_0ce7:
        ex de,hl
z80_0ce7_end:
.org 0xCE8
z80_0ce8:
        dec de
z80_0ce8_end:
.org 0xCE9
z80_0ce9:
        ret
z80_0ce9_end:
.org 0xCEA
z80_0cea:
        set 1,(ix+$00)
z80_0cea_end:
.org 0xCEE
z80_0cee:
        dec de
z80_0cee_end:
.org 0xCEF
z80_0cef:
        ret
z80_0cef_end:
.org 0xCF0
z80_0cf0:
        ld a,(ix+$01)
z80_0cf0_end:
.org 0xCF3
z80_0cf3:
        cp $02
z80_0cf3_end:
.org 0xCF5
z80_0cf5:
        jr nz,z80_0d21
z80_0cf5_end:
.org 0xCF7
z80_0cf7:
        set 0,(ix+$00)
z80_0cf7_end:
.org 0xCFB
z80_0cfb:
        exx
z80_0cfb_end:
.org 0xCFC
z80_0cfc:
        call $01c6
z80_0cfc_end:
.org 0xCFF
z80_0cff:
        ld b,$04
z80_0cff_end:
.org 0xD01
z80_0d01:
        push bc
z80_0d01_end:
.org 0xD02
z80_0d02:
        exx
z80_0d02_end:
.org 0xD03
z80_0d03:
        ld a,(de)
z80_0d03_end:
.org 0xD04
z80_0d04:
        inc de
z80_0d04_end:
.org 0xD05
z80_0d05:
        exx
z80_0d05_end:
.org 0xD06
z80_0d06:
        ld hl,$0d25
z80_0d06_end:
.org 0xD09
z80_0d09:
        add a,a
z80_0d09_end:
.org 0xD0A
z80_0d0a:
        ld c,a
z80_0d0a_end:
.org 0xD0B
z80_0d0b:
        ld b,$00
z80_0d0b_end:
.org 0xD0D
z80_0d0d:
        add hl,bc
z80_0d0d_end:
.org 0xD0E
z80_0d0e:
        ldi
z80_0d0e_end:
.org 0xD10
z80_0d10:
        ldi
z80_0d10_end:
.org 0xD12
z80_0d12:
        pop bc
z80_0d12_end:
.org 0xD13
z80_0d13:
        djnz z80_0d01
z80_0d13_end:
.org 0xD15
z80_0d15:
        exx
z80_0d15_end:
.org 0xD16
z80_0d16:
        dec de
z80_0d16_end:
.org 0xD17
z80_0d17:
        ld a,$4f
z80_0d17_end:
.org 0xD19
z80_0d19:
        ld ($1c12),a
z80_0d19_end:
.org 0xD1C
z80_0d1c:
        ld c,a
z80_0d1c_end:
.org 0xD1D
z80_0d1d:
        ld a,$27
z80_0d1d_end:
.org 0xD1F
z80_0d1f:
        rst $0018
z80_0d1f_end:
.org 0xD20
z80_0d20:
        ret
z80_0d20_end:
.org 0xD21
z80_0d21:
        inc de
z80_0d21_end:
.org 0xD22
z80_0d22:
        inc de
z80_0d22_end:
.org 0xD23
z80_0d23:
        inc de
z80_0d23_end:
.org 0xD24
z80_0d24:
        ret
z80_0d24_end:
.org 0xD2D
z80_0d2d:
        bit 7,(ix+$01)
z80_0d2d_end:
.org 0xD31
z80_0d31:
        jr nz,z80_0d6b
z80_0d31_end:
.org 0xD33
z80_0d33:
        call $08d8
z80_0d33_end:
.org 0xD36
z80_0d36:
        ld a,(de)
z80_0d36_end:
.org 0xD37
z80_0d37:
        ld (ix+$08),a
z80_0d37_end:
.org 0xD3A
z80_0d3a:
        push af
z80_0d3a_end:
.org 0xD3B
z80_0d3b:
        inc de
z80_0d3b_end:
.org 0xD3C
z80_0d3c:
        ld a,(de)
z80_0d3c_end:
.org 0xD3D
z80_0d3d:
        ld (ix+$0f),a
z80_0d3d_end:
.org 0xD40
z80_0d40:
        pop af
z80_0d40_end:
.org 0xD41
z80_0d41:
        or a
z80_0d41_end:
.org 0xD42
z80_0d42:
        jp p,$0d60
z80_0d42_end:
.org 0xD45
z80_0d45:
        push de
z80_0d45_end:
.org 0xD46
z80_0d46:
        ld hl,$8000
z80_0d46_end:
.org 0xD49
z80_0d49:
        ld c,$04
z80_0d49_end:
.org 0xD4B
z80_0d4b:
        ld a,(ix+$0f)
z80_0d4b_end:
.org 0xD4E
z80_0d4e:
        sub $81
z80_0d4e_end:
.org 0xD50
z80_0d50:
        call $0023
z80_0d50_end:
.org 0xD53
z80_0d53:
        rst $0028
z80_0d53_end:
.org 0xD54
z80_0d54:
        rst $0030
z80_0d54_end:
.org 0xD55
z80_0d55:
        ld a,(ix+$08)
z80_0d55_end:
.org 0xD58
z80_0d58:
        and $7f
z80_0d58_end:
.org 0xD5A
z80_0d5a:
        ld b,a
z80_0d5a_end:
.org 0xD5B
z80_0d5b:
        call $0493
z80_0d5b_end:
.org 0xD5E
z80_0d5e:
        jr z80_0d66
z80_0d5e_end:
.org 0xD60
z80_0d60:
        dec de
z80_0d60_end:
.org 0xD61
z80_0d61:
        push de
z80_0d61_end:
.org 0xD62
z80_0d62:
        ld b,a
z80_0d62_end:
.org 0xD63
z80_0d63:
        call $0484
z80_0d63_end:
.org 0xD66
z80_0d66:
        call $04e5
z80_0d66_end:
.org 0xD69
z80_0d69:
        pop de
z80_0d69_end:
.org 0xD6A
z80_0d6a:
        ret
z80_0d6a_end:
.org 0xD6B
z80_0d6b:
        ld a,(de)
z80_0d6b_end:
.org 0xD6C
z80_0d6c:
        or a
z80_0d6c_end:
.org 0xD6D
z80_0d6d:
        ret p
z80_0d6d_end:
.org 0xD6E
z80_0d6e:
        inc de
z80_0d6e_end:
.org 0xD6F
z80_0d6f:
        ret
z80_0d6f_end:
.org 0xD70
z80_0d70:
        ld c,$3f
z80_0d70_end:
.org 0xD72
z80_0d72:
        ld a,(ix+$0a)
z80_0d72_end:
.org 0xD75
z80_0d75:
        and c
z80_0d75_end:
.org 0xD76
z80_0d76:
        ex de,hl
z80_0d76_end:
.org 0xD77
z80_0d77:
        or (hl)
z80_0d77_end:
.org 0xD78
z80_0d78:
        ld (ix+$0a),a
z80_0d78_end:
.org 0xD7B
z80_0d7b:
        ld c,a
z80_0d7b_end:
.org 0xD7C
z80_0d7c:
        ld a,$b4
z80_0d7c_end:
.org 0xD7E
z80_0d7e:
        rst $0010
z80_0d7e_end:
.org 0xD7F
z80_0d7f:
        ex de,hl
z80_0d7f_end:
.org 0xD80
z80_0d80:
        ret
z80_0d80_end:
.org 0xD81
z80_0d81:
        ld c,a
z80_0d81_end:
.org 0xD82
z80_0d82:
        ld a,$22
z80_0d82_end:
.org 0xD84
z80_0d84:
        rst $0018
z80_0d84_end:
.org 0xD85
z80_0d85:
        inc de
z80_0d85_end:
.org 0xD86
z80_0d86:
        ld c,$c0
z80_0d86_end:
.org 0xD88
z80_0d88:
        jr z80_0d72
z80_0d88_end:
.org 0xD8A
z80_0d8a:
        exx
z80_0d8a_end:
.org 0xD8B
z80_0d8b:
        ld de,$04dd
z80_0d8b_end:
.org 0xD8E
z80_0d8e:
        ld l,(ix+$1c)
z80_0d8e_end:
.org 0xD91
z80_0d91:
        ld h,(ix+$1d)
z80_0d91_end:
.org 0xD94
z80_0d94:
        ld b,$04
z80_0d94_end:
.org 0xD96
z80_0d96:
        ld a,(hl)
z80_0d96_end:
.org 0xD97
z80_0d97:
        or a
z80_0d97_end:
.org 0xD98
z80_0d98:
        jp p,$0d9e
z80_0d98_end:
.org 0xD9B
z80_0d9b:
        add a,(ix+$06)
z80_0d9b_end:
.org 0xD9E
z80_0d9e:
        and $7f
z80_0d9e_end:
.org 0xDA0
z80_0da0:
        ld c,a
z80_0da0_end:
.org 0xDA1
z80_0da1:
        ld a,(de)
z80_0da1_end:
.org 0xDA2
z80_0da2:
        rst $0010
z80_0da2_end:
.org 0xDA3
z80_0da3:
        inc de
z80_0da3_end:
.org 0xDA4
z80_0da4:
        inc hl
z80_0da4_end:
.org 0xDA5
z80_0da5:
        djnz z80_0d96
z80_0da5_end:
.org 0xDA7
z80_0da7:
        exx
z80_0da7_end:
.org 0xDA8
z80_0da8:
        ret
z80_0da8_end:
.org 0xDA9
z80_0da9:
        inc de
z80_0da9_end:
.org 0xDAA
z80_0daa:
        add a,(ix+$06)
z80_0daa_end:
.org 0xDAD
z80_0dad:
        ld (ix+$06),a
z80_0dad_end:
.org 0xDB0
z80_0db0:
        ld a,(de)
z80_0db0_end:
.org 0xDB1
z80_0db1:
        bit 7,(ix+$01)
z80_0db1_end:
.org 0xDB5
z80_0db5:
        ret nz
z80_0db5_end:
.org 0xDB6
z80_0db6:
        add a,(ix+$06)
z80_0db6_end:
.org 0xDB9
z80_0db9:
        ld (ix+$06),a
z80_0db9_end:
.org 0xDBC
z80_0dbc:
        jr z80_0d8a
z80_0dbc_end:
.org 0xDBE
z80_0dbe:
        add a,(ix+$05)
z80_0dbe_end:
.org 0xDC1
z80_0dc1:
        ld (ix+$05),a
z80_0dc1_end:
.org 0xDC4
z80_0dc4:
        ret
z80_0dc4_end:
.org 0xDC5
z80_0dc5:
        ld (ix+$02),a
z80_0dc5_end:
.org 0xDC8
z80_0dc8:
        ret
z80_0dc8_end:
.org 0xDC9
z80_0dc9:
        bit 2,(ix+$01)
z80_0dc9_end:
.org 0xDCD
z80_0dcd:
        ret nz
z80_0dcd_end:
.org 0xDCE
z80_0dce:
        ld a,$df
z80_0dce_end:
.org 0xDD0
z80_0dd0:
        ld ($7f11),a
z80_0dd0_end:
.org 0xDD3
z80_0dd3:
        ld a,(de)
z80_0dd3_end:
.org 0xDD4
z80_0dd4:
        ld (ix+$1a),a
z80_0dd4_end:
.org 0xDD7
z80_0dd7:
        set 0,(ix+$00)
z80_0dd7_end:
.org 0xDDB
z80_0ddb:
        or a
z80_0ddb_end:
.org 0xDDC
z80_0ddc:
        jr nz,z80_0de4
z80_0ddc_end:
.org 0xDDE
z80_0dde:
        res 0,(ix+$00)
z80_0dde_end:
.org 0xDE2
z80_0de2:
        ld a,$ff
z80_0de2_end:
.org 0xDE4
z80_0de4:
        ld ($7f11),a
z80_0de4_end:
.org 0xDE7
z80_0de7:
        ret
z80_0de7_end:
.org 0xDE8
z80_0de8:
        bit 7,(ix+$01)
z80_0de8_end:
.org 0xDEC
z80_0dec:
        ret z
z80_0dec_end:
.org 0xDED
z80_0ded:
        ld (ix+$08),a
z80_0ded_end:
.org 0xDF0
z80_0df0:
        ret
z80_0df0_end:
.org 0xDF1
z80_0df1:
        inc de
z80_0df1_end:
.org 0xDF2
z80_0df2:
        bit 7,(ix+$01)
z80_0df2_end:
.org 0xDF6
z80_0df6:
        jr nz,z80_0df9
z80_0df6_end:
.org 0xDF8
z80_0df8:
        ld a,(de)
z80_0df8_end:
.org 0xDF9
z80_0df9:
        ld (ix+$07),a
z80_0df9_end:
.org 0xDFC
z80_0dfc:
        ret
z80_0dfc_end:
.org 0xDFD
z80_0dfd:
        ex de,hl
z80_0dfd_end:
.org 0xDFE
z80_0dfe:
        ld e,(hl)
z80_0dfe_end:
.org 0xDFF
z80_0dff:
        inc hl
z80_0dff_end:
.org 0xE00
z80_0e00:
        ld d,(hl)
z80_0e00_end:
.org 0xE01
z80_0e01:
        dec de
z80_0e01_end:
.org 0xE02
z80_0e02:
        ret
z80_0e02_end:
.org 0xE03
z80_0e03:
        cp $01
z80_0e03_end:
.org 0xE05
z80_0e05:
        jr nz,z80_0e0c
z80_0e05_end:
.org 0xE07
z80_0e07:
        set 5,(ix+$00)
z80_0e07_end:
.org 0xE0B
z80_0e0b:
        ret
z80_0e0b_end:
.org 0xE0C
z80_0e0c:
        res 1,(ix+$00)
z80_0e0c_end:
.org 0xE10
z80_0e10:
        res 5,(ix+$00)
z80_0e10_end:
.org 0xE14
z80_0e14:
        xor a
z80_0e14_end:
.org 0xE15
z80_0e15:
        ld (ix+$10),a
z80_0e15_end:
.org 0xE18
z80_0e18:
        ret
z80_0e18_end:
.org 0xE19
z80_0e19:
        cp $01
z80_0e19_end:
.org 0xE1B
z80_0e1b:
        jr nz,z80_0e22
z80_0e1b_end:
.org 0xE1D
z80_0e1d:
        set 3,(ix+$00)
z80_0e1d_end:
.org 0xE21
z80_0e21:
        ret
z80_0e21_end:
.org 0xE22
z80_0e22:
        res 3,(ix+$00)
z80_0e22_end:
.org 0xE26
z80_0e26:
        ret
z80_0e26_end:
.org 0xE27
z80_0e27:
        res 7,(ix+$00)
z80_0e27_end:
.org 0xE2B
z80_0e2b:
        ld a,$1f
z80_0e2b_end:
.org 0xE2D
z80_0e2d:
        ld ($1c15),a
z80_0e2d_end:
.org 0xE30
z80_0e30:
        call $0422
z80_0e30_end:
.org 0xE33
z80_0e33:
        ld c,(ix+$01)
z80_0e33_end:
.org 0xE36
z80_0e36:
        push ix
z80_0e36_end:
.org 0xE38
z80_0e38:
        call $0689
z80_0e38_end:
.org 0xE3B
z80_0e3b:
        ld a,($1c19)
z80_0e3b_end:
.org 0xE3E
z80_0e3e:
        or a
z80_0e3e_end:
.org 0xE3F
z80_0e3f:
        jr z,z80_0eaa
z80_0e3f_end:
.org 0xE41
z80_0e41:
        xor a
z80_0e41_end:
.org 0xE42
z80_0e42:
        ld ($1c18),a
z80_0e42_end:
.org 0xE45
z80_0e45:
        bit 7,(iy+$00)
z80_0e45_end:
.org 0xE49
z80_0e49:
        jr z,z80_0e5d
z80_0e49_end:
.org 0xE4B
z80_0e4b:
        ld a,(ix+$01)
z80_0e4b_end:
.org 0xE4E
z80_0e4e:
        cp (iy+$01)
z80_0e4e_end:
.org 0xE51
z80_0e51:
        jr nz,z80_0e5d
z80_0e51_end:
.org 0xE53
z80_0e53:
        push iy
z80_0e53_end:
.org 0xE55
z80_0e55:
        ld l,(iy+$2a)
z80_0e55_end:
.org 0xE58
z80_0e58:
        ld h,(iy+$2b)
z80_0e58_end:
.org 0xE5B
z80_0e5b:
        jr z80_0e61
z80_0e5b_end:
.org 0xE5D
z80_0e5d:
        push hl
z80_0e5d_end:
.org 0xE5E
z80_0e5e:
        ld hl,($1c37)
z80_0e5e_end:
.org 0xE61
z80_0e61:
        pop ix
z80_0e61_end:
.org 0xE63
z80_0e63:
        res 2,(ix+$00)
z80_0e63_end:
.org 0xE67
z80_0e67:
        bit 7,(ix+$01)
z80_0e67_end:
.org 0xE6B
z80_0e6b:
        jr nz,z80_0eaf
z80_0e6b_end:
.org 0xE6D
z80_0e6d:
        bit 7,(ix+$00)
z80_0e6d_end:
.org 0xE71
z80_0e71:
        jr z,z80_0eaa
z80_0e71_end:
.org 0xE73
z80_0e73:
        ld a,$02
z80_0e73_end:
.org 0xE75
z80_0e75:
        cp (ix+$01)
z80_0e75_end:
.org 0xE78
z80_0e78:
        jr nz,z80_0e87
z80_0e78_end:
.org 0xE7A
z80_0e7a:
        ld a,$4f
z80_0e7a_end:
.org 0xE7C
z80_0e7c:
        bit 0,(ix+$00)
z80_0e7c_end:
.org 0xE80
z80_0e80:
        jr nz,z80_0e84
z80_0e80_end:
.org 0xE82
z80_0e82:
        and $0f
z80_0e82_end:
.org 0xE84
z80_0e84:
        call $0d19
z80_0e84_end:
.org 0xE87
z80_0e87:
        ld a,(ix+$08)
z80_0e87_end:
.org 0xE8A
z80_0e8a:
        or a
z80_0e8a_end:
.org 0xE8B
z80_0e8b:
        jp p,$0e93
z80_0e8b_end:
.org 0xE8E
z80_0e8e:
        call $0d45
z80_0e8e_end:
.org 0xE91
z80_0e91:
        jr z80_0ea7
z80_0e91_end:
.org 0xE93
z80_0e93:
        ld b,a
z80_0e93_end:
.org 0xE94
z80_0e94:
        call $0493
z80_0e94_end:
.org 0xE97
z80_0e97:
        call $04e5
z80_0e97_end:
.org 0xE9A
z80_0e9a:
        ld a,(ix+$18)
z80_0e9a_end:
.org 0xE9D
z80_0e9d:
        or a
z80_0e9d_end:
.org 0xE9E
z80_0e9e:
        jp p,$0eaa
z80_0e9e_end:
.org 0xEA1
z80_0ea1:
        ld e,(ix+$19)
z80_0ea1_end:
.org 0xEA4
z80_0ea4:
        ld d,(ix+$1a)
z80_0ea4_end:
.org 0xEA7
z80_0ea7:
        call $0be9
z80_0ea7_end:
.org 0xEAA
z80_0eaa:
        pop ix
z80_0eaa_end:
.org 0xEAC
z80_0eac:
        pop hl
z80_0eac_end:
.org 0xEAD
z80_0ead:
        pop hl
z80_0ead_end:
.org 0xEAE
z80_0eae:
        ret
z80_0eae_end:
.org 0xEAF
z80_0eaf:
        bit 0,(ix+$00)
z80_0eaf_end:
.org 0xEB3
z80_0eb3:
        jr z,z80_0eaa
z80_0eb3_end:
.org 0xEB5
z80_0eb5:
        ld a,(ix+$1a)
z80_0eb5_end:
.org 0xEB8
z80_0eb8:
        or a
z80_0eb8_end:
.org 0xEB9
z80_0eb9:
        jp p,$0ebf
z80_0eb9_end:
.org 0xEBC
z80_0ebc:
        ld ($7f11),a
z80_0ebc_end:
.org 0xEBF
z80_0ebf:
        jr z80_0eaa
z80_0ebf_end:
.org 0xEC1
z80_0ec1:
        ld c,a
z80_0ec1_end:
.org 0xEC2
z80_0ec2:
        inc de
z80_0ec2_end:
.org 0xEC3
z80_0ec3:
        ld a,(de)
z80_0ec3_end:
.org 0xEC4
z80_0ec4:
        ld b,a
z80_0ec4_end:
.org 0xEC5
z80_0ec5:
        push bc
z80_0ec5_end:
.org 0xEC6
z80_0ec6:
        push ix
z80_0ec6_end:
.org 0xEC8
z80_0ec8:
        pop hl
z80_0ec8_end:
.org 0xEC9
z80_0ec9:
        dec (ix+$09)
z80_0ec9_end:
.org 0xECC
z80_0ecc:
        ld c,(ix+$09)
z80_0ecc_end:
.org 0xECF
z80_0ecf:
        dec (ix+$09)
z80_0ecf_end:
.org 0xED2
z80_0ed2:
        ld b,$00
z80_0ed2_end:
.org 0xED4
z80_0ed4:
        add hl,bc
z80_0ed4_end:
.org 0xED5
z80_0ed5:
        ld (hl),d
z80_0ed5_end:
.org 0xED6
z80_0ed6:
        dec hl
z80_0ed6_end:
.org 0xED7
z80_0ed7:
        ld (hl),e
z80_0ed7_end:
.org 0xED8
z80_0ed8:
        pop de
z80_0ed8_end:
.org 0xED9
z80_0ed9:
        dec de
z80_0ed9_end:
.org 0xEDA
z80_0eda:
        ret
z80_0eda_end:
.org 0xEDB
z80_0edb:
        push ix
z80_0edb_end:
.org 0xEDD
z80_0edd:
        pop hl
z80_0edd_end:
.org 0xEDE
z80_0ede:
        ld c,(ix+$09)
z80_0ede_end:
.org 0xEE1
z80_0ee1:
        ld b,$00
z80_0ee1_end:
.org 0xEE3
z80_0ee3:
        add hl,bc
z80_0ee3_end:
.org 0xEE4
z80_0ee4:
        ld e,(hl)
z80_0ee4_end:
.org 0xEE5
z80_0ee5:
        inc hl
z80_0ee5_end:
.org 0xEE6
z80_0ee6:
        ld d,(hl)
z80_0ee6_end:
.org 0xEE7
z80_0ee7:
        inc (ix+$09)
z80_0ee7_end:
.org 0xEEA
z80_0eea:
        inc (ix+$09)
z80_0eea_end:
.org 0xEED
z80_0eed:
        ret
z80_0eed_end:
.org 0xEEE
z80_0eee:
        inc de
z80_0eee_end:
.org 0xEEF
z80_0eef:
        add a,$28
z80_0eef_end:
.org 0xEF1
z80_0ef1:
        ld c,a
z80_0ef1_end:
.org 0xEF2
z80_0ef2:
        ld b,$00
z80_0ef2_end:
.org 0xEF4
z80_0ef4:
        push ix
z80_0ef4_end:
.org 0xEF6
z80_0ef6:
        pop hl
z80_0ef6_end:
.org 0xEF7
z80_0ef7:
        add hl,bc
z80_0ef7_end:
.org 0xEF8
z80_0ef8:
        ld a,(hl)
z80_0ef8_end:
.org 0xEF9
z80_0ef9:
        or a
z80_0ef9_end:
.org 0xEFA
z80_0efa:
        jr nz,z80_0efe
z80_0efa_end:
.org 0xEFC
z80_0efc:
        ld a,(de)
z80_0efc_end:
.org 0xEFD
z80_0efd:
        ld (hl),a
z80_0efd_end:
.org 0xEFE
z80_0efe:
        inc de
z80_0efe_end:
.org 0xEFF
z80_0eff:
        dec (hl)
z80_0eff_end:
.org 0xF00
z80_0f00:
        jp nz,$0dfd
z80_0f00_end:
.org 0xF03
z80_0f03:
        inc de
z80_0f03_end:
.org 0xF04
z80_0f04:
        ret
z80_0f04_end:
.org 0xF05
z80_0f05:
        call $0304
z80_0f05_end:
.org 0xF08
z80_0f08:
        jr nz,z80_0f17
z80_0f08_end:
.org 0xF0A
z80_0f0a:
        call $01d6
z80_0f0a_end:
.org 0xF0D
z80_0f0d:
        bit 4,(ix+$00)
z80_0f0d_end:
.org 0xF11
z80_0f11:
        ret nz
z80_0f11_end:
.org 0xF12
z80_0f12:
        call $033b
z80_0f12_end:
.org 0xF15
z80_0f15:
        jr z80_0f23
z80_0f15_end:
.org 0xF17
z80_0f17:
        ld a,(ix+$1e)
z80_0f17_end:
.org 0xF1A
z80_0f1a:
        or a
z80_0f1a_end:
.org 0xF1B
z80_0f1b:
        jr z,z80_0f23
z80_0f1b_end:
.org 0xF1D
z80_0f1d:
        dec (ix+$1e)
z80_0f1d_end:
.org 0xF20
z80_0f20:
        jp z,$0fac
z80_0f20_end:
.org 0xF23
z80_0f23:
        call $0432
z80_0f23_end:
.org 0xF26
z80_0f26:
        call $0366
z80_0f26_end:
.org 0xF29
z80_0f29:
        bit 2,(ix+$00)
z80_0f29_end:
.org 0xF2D
z80_0f2d:
        ret nz
z80_0f2d_end:
.org 0xF2E
z80_0f2e:
        ld c,(ix+$01)
z80_0f2e_end:
.org 0xF31
z80_0f31:
        ld a,l
z80_0f31_end:
.org 0xF32
z80_0f32:
        and $0f
z80_0f32_end:
.org 0xF34
z80_0f34:
        or c
z80_0f34_end:
.org 0xF35
z80_0f35:
        ld ($7f11),a
z80_0f35_end:
.org 0xF38
z80_0f38:
        ld a,l
z80_0f38_end:
.org 0xF39
z80_0f39:
        and $f0
z80_0f39_end:
.org 0xF3B
z80_0f3b:
        or h
z80_0f3b_end:
.org 0xF3C
z80_0f3c:
        rrca
z80_0f3c_end:
.org 0xF3D
z80_0f3d:
        rrca
z80_0f3d_end:
.org 0xF3E
z80_0f3e:
        rrca
z80_0f3e_end:
.org 0xF3F
z80_0f3f:
        rrca
z80_0f3f_end:
.org 0xF40
z80_0f40:
        ld ($7f11),a
z80_0f40_end:
.org 0xF43
z80_0f43:
        ld a,(ix+$08)
z80_0f43_end:
.org 0xF46
z80_0f46:
        or a
z80_0f46_end:
.org 0xF47
z80_0f47:
        ld c,$00
z80_0f47_end:
.org 0xF49
z80_0f49:
        jr z,z80_0f54
z80_0f49_end:
.org 0xF4B
z80_0f4b:
        dec a
z80_0f4b_end:
.org 0xF4C
z80_0f4c:
        ld c,$0a
z80_0f4c_end:
.org 0xF4E
z80_0f4e:
        rst $0020
z80_0f4e_end:
.org 0xF4F
z80_0f4f:
        rst $0028
z80_0f4f_end:
.org 0xF50
z80_0f50:
        call $0f7b
z80_0f50_end:
.org 0xF53
z80_0f53:
        ld c,a
z80_0f53_end:
.org 0xF54
z80_0f54:
        bit 4,(ix+$00)
z80_0f54_end:
.org 0xF58
z80_0f58:
        ret nz
z80_0f58_end:
.org 0xF59
z80_0f59:
        ld a,(ix+$06)
z80_0f59_end:
.org 0xF5C
z80_0f5c:
        add a,c
z80_0f5c_end:
.org 0xF5D
z80_0f5d:
        bit 4,a
z80_0f5d_end:
.org 0xF5F
z80_0f5f:
        jr z,z80_0f63
z80_0f5f_end:
.org 0xF61
z80_0f61:
        ld a,$0f
z80_0f61_end:
.org 0xF63
z80_0f63:
        or (ix+$01)
z80_0f63_end:
.org 0xF66
z80_0f66:
        add a,$10
z80_0f66_end:
.org 0xF68
z80_0f68:
        bit 0,(ix+$00)
z80_0f68_end:
.org 0xF6C
z80_0f6c:
        jr nz,z80_0f72
z80_0f6c_end:
.org 0xF6E
z80_0f6e:
        ld ($7f11),a
z80_0f6e_end:
.org 0xF71
z80_0f71:
        ret
z80_0f71_end:
.org 0xF72
z80_0f72:
        add a,$20
z80_0f72_end:
.org 0xF74
z80_0f74:
        ld ($7f11),a
z80_0f74_end:
.org 0xF77
z80_0f77:
        ret
z80_0f77_end:
.org 0xF78
z80_0f78:
        ld (ix+$17),a
z80_0f78_end:
.org 0xF7B
z80_0f7b:
        push hl
z80_0f7b_end:
.org 0xF7C
z80_0f7c:
        ld c,(ix+$17)
z80_0f7c_end:
.org 0xF7F
z80_0f7f:
        call $047d
z80_0f7f_end:
.org 0xF82
z80_0f82:
        pop hl
z80_0f82_end:
.org 0xF83
z80_0f83:
        bit 7,a
z80_0f83_end:
.org 0xF85
z80_0f85:
        jr z,z80_0fa8
z80_0f85_end:
.org 0xF87
z80_0f87:
        cp $83
z80_0f87_end:
.org 0xF89
z80_0f89:
        jr z,z80_0f97
z80_0f89_end:
.org 0xF8B
z80_0f8b:
        cp $81
z80_0f8b_end:
.org 0xF8D
z80_0f8d:
        jr z,z80_0fa2
z80_0f8d_end:
.org 0xF8F
z80_0f8f:
        cp $80
z80_0f8f_end:
.org 0xF91
z80_0f91:
        jr z,z80_0f9f
z80_0f91_end:
.org 0xF93
z80_0f93:
        inc bc
z80_0f93_end:
.org 0xF94
z80_0f94:
        ld a,(bc)
z80_0f94_end:
.org 0xF95
z80_0f95:
        jr z80_0f78
z80_0f95_end:
.org 0xF97
z80_0f97:
        set 4,(ix+$00)
z80_0f97_end:
.org 0xF9B
z80_0f9b:
        pop hl
z80_0f9b_end:
.org 0xF9C
z80_0f9c:
        jp $0fac
z80_0f9c_end:
.org 0xF9F
z80_0f9f:
        xor a
z80_0f9f_end:
.org 0xFA0
z80_0fa0:
        jr z80_0f78
z80_0fa0_end:
.org 0xFA2
z80_0fa2:
        pop hl
z80_0fa2_end:
.org 0xFA3
z80_0fa3:
        set 4,(ix+$00)
z80_0fa3_end:
.org 0xFA7
z80_0fa7:
        ret
z80_0fa7_end:
.org 0xFA8
z80_0fa8:
        inc (ix+$17)
z80_0fa8_end:
.org 0xFAB
z80_0fab:
        ret
z80_0fab_end:
.org 0xFAC
z80_0fac:
        set 4,(ix+$00)
z80_0fac_end:
.org 0xFB0
z80_0fb0:
        bit 2,(ix+$00)
z80_0fb0_end:
.org 0xFB4
z80_0fb4:
        ret nz
z80_0fb4_end:
.org 0xFB5
z80_0fb5:
        ld a,$1f
z80_0fb5_end:
.org 0xFB7
z80_0fb7:
        add a,(ix+$01)
z80_0fb7_end:
.org 0xFBA
z80_0fba:
        or a
z80_0fba_end:
.org 0xFBB
z80_0fbb:
        ret p
z80_0fbb_end:
.org 0xFBC
z80_0fbc:
        ld ($7f11),a
z80_0fbc_end:
.org 0xFBF
z80_0fbf:
        bit 0,(ix+$00)
z80_0fbf_end:
.org 0xFC3
z80_0fc3:
        ret z
z80_0fc3_end:
.org 0xFC4
z80_0fc4:
        ld a,$ff
z80_0fc4_end:
.org 0xFC6
z80_0fc6:
        ld ($7f11),a
z80_0fc6_end:
.org 0xFC9
z80_0fc9:
        ret
z80_0fc9_end:
