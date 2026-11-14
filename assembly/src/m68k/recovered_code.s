| 68000 主程序入口及固定地址的指令。每对标签标记一条指令的范围。
.cpu 68000
.section .text
_start:
.org 0x200
m68k_000200:
        nop
m68k_000200_end:
.org 0x202
m68k_000202:
        nop
m68k_000202_end:
.org 0x204
m68k_000204:
        bra.b (. + -4)
m68k_000204_end:
.org 0x206
m68k_000206:
        tst.l 0xa10008:l
m68k_000206_end:
.org 0x20C
m68k_00020c:
        bne.b (. + 8)
m68k_00020c_end:
.org 0x20E
m68k_00020e:
        tst.w 0xa1000c:l
m68k_00020e_end:
.org 0x214
m68k_000214:
        bne.b (. + 126)
m68k_000214_end:
.org 0x216
m68k_000216:
        lea.l 124(%pc),%a5
m68k_000216_end:
.org 0x21A
m68k_00021a:
        movem.w (%a5)+,%d5-%d7
m68k_00021a_end:
.org 0x21E
m68k_00021e:
        movem.l (%a5)+,%a0-%a4
m68k_00021e_end:
.org 0x222
m68k_000222:
        move.b -0x10ff(%a1),%d0
m68k_000222_end:
.org 0x226
m68k_000226:
        andi.b #0xf,%d0
m68k_000226_end:
.org 0x22A
m68k_00022a:
        beq.b (. + 10)
m68k_00022a_end:
.org 0x22C
m68k_00022c:
        move.l #0x53454741,0x2f00(%a1)
m68k_00022c_end:
.org 0x234
m68k_000234:
        move.w (%a4),%d0
m68k_000234_end:
.org 0x236
m68k_000236:
        moveq #0,%d0
m68k_000236_end:
.org 0x238
m68k_000238:
        movea.l %d0,%a6
m68k_000238_end:
.org 0x23A
m68k_00023a:
        move %a6,%usp
m68k_00023a_end:
.org 0x23C
m68k_00023c:
        moveq #23,%d1
m68k_00023c_end:
.org 0x23E
m68k_00023e:
        move.b (%a5)+,%d5
m68k_00023e_end:
.org 0x240
m68k_000240:
        move.w %d5,(%a4)
m68k_000240_end:
.org 0x242
m68k_000242:
        add.w %d7,%d5
m68k_000242_end:
.org 0x244
m68k_000244:
        dbra %d1,(. + -6)
m68k_000244_end:
.org 0x248
m68k_000248:
        move.l (%a5)+,(%a4)
m68k_000248_end:
.org 0x24A
m68k_00024a:
        move.w %d0,(%a3)
m68k_00024a_end:
.org 0x24C
m68k_00024c:
        move.w %d7,(%a1)
m68k_00024c_end:
.org 0x24E
m68k_00024e:
        move.w %d7,(%a2)
m68k_00024e_end:
.org 0x250
m68k_000250:
        btst.l %d0,(%a1)
m68k_000250_end:
.org 0x252
m68k_000252:
        bne.b (. + -2)
m68k_000252_end:
.org 0x254
m68k_000254:
        moveq #37,%d2
m68k_000254_end:
.org 0x256
m68k_000256:
        move.b (%a5)+,(%a0)+
m68k_000256_end:
.org 0x258
m68k_000258:
        dbra %d2,(. + -2)
m68k_000258_end:
.org 0x25C
m68k_00025c:
        move.w %d0,(%a2)
m68k_00025c_end:
.org 0x25E
m68k_00025e:
        move.w %d0,(%a1)
m68k_00025e_end:
.org 0x260
m68k_000260:
        move.w %d7,(%a2)
m68k_000260_end:
.org 0x262
m68k_000262:
        move.l %d0,-(%a6)
m68k_000262_end:
.org 0x264
m68k_000264:
        dbra %d6,(. + -2)
m68k_000264_end:
.org 0x268
m68k_000268:
        move.l (%a5)+,(%a4)
m68k_000268_end:
.org 0x26A
m68k_00026a:
        move.l (%a5)+,(%a4)
m68k_00026a_end:
.org 0x26C
m68k_00026c:
        moveq #31,%d3
m68k_00026c_end:
.org 0x26E
m68k_00026e:
        move.l %d0,(%a3)
m68k_00026e_end:
.org 0x270
m68k_000270:
        dbra %d3,(. + -2)
m68k_000270_end:
.org 0x274
m68k_000274:
        move.l (%a5)+,(%a4)
m68k_000274_end:
.org 0x276
m68k_000276:
        moveq #19,%d4
m68k_000276_end:
.org 0x278
m68k_000278:
        move.l %d0,(%a3)
m68k_000278_end:
.org 0x27A
m68k_00027a:
        dbra %d4,(. + -2)
m68k_00027a_end:
.org 0x27E
m68k_00027e:
        moveq #3,%d5
m68k_00027e_end:
.org 0x280
m68k_000280:
        move.b (%a5)+,0x11(%a3)
m68k_000280_end:
.org 0x284
m68k_000284:
        dbra %d5,(. + -4)
m68k_000284_end:
.org 0x288
m68k_000288:
        move.w %d0,(%a2)
m68k_000288_end:
.org 0x28A
m68k_00028a:
        movem.l (%a6),%d0-%d7/%a0-%a6
m68k_00028a_end:
.org 0x28E
m68k_00028e:
        move.w #0x2700,%sr
m68k_00028e_end:
.org 0x292
m68k_000292:
        bra.b (. + 110)
m68k_000292_end:
.org 0x300
m68k_000300:
        tst.w 0xc00004:l
m68k_000300_end:
.org 0x306
m68k_000306:
        lea.l 0xc00004:l,%a6
m68k_000306_end:
.org 0x30C
m68k_00030c:
        move.w (%a6),%d0
m68k_00030c_end:
.org 0x30E
m68k_00030e:
        andi.w #0x2,%d0
m68k_00030e_end:
.org 0x312
m68k_000312:
        bne.b (. + -6)
m68k_000312_end:
.org 0x314
m68k_000314:
        btst.b #0x6,0xa1000d:l
m68k_000314_end:
.org 0x31C
m68k_00031c:
        beq.b (. + 14)
m68k_00031c_end:
.org 0x31E
m68k_00031e:
        cmpi.l #0x696e6974,0xfffc:w
m68k_00031e_end:
.org 0x326
m68k_000326:
        beq.w (. + 72)
m68k_000326_end:
.org 0x32A
m68k_00032a:
        lea.l 0x1a4:w,%a0
m68k_00032a_end:
.org 0x32E
m68k_00032e:
        move.l (%a0),%d0
m68k_00032e_end:
.org 0x330
m68k_000330:
        addq.l #0x1,%d0
m68k_000330_end:
.org 0x332
m68k_000332:
        lea.l 0x200:w,%a0
m68k_000332_end:
.org 0x336
m68k_000336:
        sub.l %a0,%d0
m68k_000336_end:
.org 0x338
m68k_000338:
        asr.l #0x1,%d0
m68k_000338_end:
.org 0x33A
m68k_00033a:
        move.w %d0,%d2
m68k_00033a_end:
.org 0x33C
m68k_00033c:
        subq.w #0x1,%d2
m68k_00033c_end:
.org 0x33E
m68k_00033e:
        swap %d0
m68k_00033e_end:
.org 0x340
m68k_000340:
        moveq #0,%d1
m68k_000340_end:
.org 0x342
m68k_000342:
        add.w (%a0)+,%d1
m68k_000342_end:
.org 0x344
m68k_000344:
        dbra %d2,(. + -2)
m68k_000344_end:
.org 0x348
m68k_000348:
        dbra %d0,(. + -6)
m68k_000348_end:
.org 0x34C
m68k_00034c:
        lea.l 0x18e:w,%a0
m68k_00034c_end:
.org 0x350
m68k_000350:
        cmp.w (%a0),%d1
m68k_000350_end:
.org 0x352
m68k_000352:
        bne.w (. + 374)
m68k_000352_end:
.org 0x356
m68k_000356:
        lea.l 0xfe00:w,%a6
m68k_000356_end:
.org 0x35A
m68k_00035a:
        moveq #0,%d7
m68k_00035a_end:
.org 0x35C
m68k_00035c:
        move.w #0x7f,%d6
m68k_00035c_end:
.org 0x360
m68k_000360:
        move.l %d7,(%a6)+
m68k_000360_end:
.org 0x362
m68k_000362:
        dbra %d6,(. + -2)
m68k_000362_end:
.org 0x366
m68k_000366:
        move.l #0x696e6974,0xfffc:w
m68k_000366_end:
.org 0x36E
m68k_00036e:
        lea.l 0xff0000:l,%a6
m68k_00036e_end:
.org 0x374
m68k_000374:
        moveq #0,%d7
m68k_000374_end:
.org 0x376
m68k_000376:
        move.w #0x3f7f,%d6
m68k_000376_end:
.org 0x37A
m68k_00037a:
        move.l %d7,(%a6)+
m68k_00037a_end:
.org 0x37C
m68k_00037c:
        dbra %d6,(. + -2)
m68k_00037c_end:
.org 0x380
m68k_000380:
        lea.l 0xfffe00:l,%a7
m68k_000380_end:
.org 0x386
m68k_000386:
        jsr 0x6826:l
m68k_000386_end:
.org 0x38C
m68k_00038c:
        jsr 0x6950:l
m68k_00038c_end:
.org 0x392
m68k_000392:
        jsr 0x67b4:l
m68k_000392_end:
.org 0x398
m68k_000398:
        move.w #0x50,0xf30a:w
m68k_000398_end:
.org 0x39E
m68k_00039e:
        move.w #0xa0,0xf30c:w
m68k_00039e_end:
.org 0x3A4
m68k_0003a4:
        move.w #0x1800,0xf30e:w
m68k_0003a4_end:
.org 0x3AA
m68k_0003aa:
        move.w #0x2,0xefd8:w
m68k_0003aa_end:
.org 0x3B0
m68k_0003b0:
        move.w #0x1,0xaffe:w
m68k_0003b0_end:
.org 0x3B6
m68k_0003b6:
        move.w #0x4,0xf600:w
m68k_0003b6_end:
.org 0x3BC
m68k_0003bc:
        tst.w 0xf600:w
m68k_0003bc_end:
.org 0x3C0
m68k_0003c0:
        beq.b (. + -4)
m68k_0003c0_end:
.org 0x3C2
m68k_0003c2:
        move.w 0xf600:w,%d0
m68k_0003c2_end:
.org 0x3C6
m68k_0003c6:
        andi.w #0xfffc,%d0
m68k_0003c6_end:
.org 0x3CA
m68k_0003ca:
        jsr 8(%pc, %d0.w)
m68k_0003ca_end:
.org 0x3CE
m68k_0003ce:
        clr.w 0xf600:w
m68k_0003ce_end:
.org 0x3D2
m68k_0003d2:
        move.w #0x2500,%sr
m68k_0003d2_end:
.org 0x3D6
m68k_0003d6:
        bra.b (. + -26)
m68k_0003d6_end:
.org 0x3D8
m68k_0003d8:
        bra.w (. + 272)
m68k_0003d8_end:
.org 0x3E0
m68k_0003e0:
        bra.w (. + 13230)
m68k_0003e0_end:
.org 0x3FC
m68k_0003fc:
        bra.w (. + 528)
m68k_0003fc_end:
.org 0x404
m68k_000404:
        bra.w (. + 338)
m68k_000404_end:
.org 0x430
m68k_000430:
        bra.w (. + 996)
m68k_000430_end:
.org 0x434
m68k_000434:
        bra.w (. + 1194)
m68k_000434_end:
.org 0x448
m68k_000448:
        bra.w (. + 2022)
m68k_000448_end:
.org 0x450
m68k_000450:
        bra.w (. + 2112)
m68k_000450_end:
.org 0x498
m68k_000498:
        bra.w (. + 2344)
m68k_000498_end:
.org 0x4C8
m68k_0004c8:
        jsr 0x6826:l
m68k_0004c8_end:
.org 0x4CE
m68k_0004ce:
        move.l #0xc0000000,0xc00004:l
m68k_0004ce_end:
.org 0x4D8
m68k_0004d8:
        moveq #63,%d7
m68k_0004d8_end:
.org 0x4DA
m68k_0004da:
        move.w #0xe,0xc00000:l
m68k_0004da_end:
.org 0x4E2
m68k_0004e2:
        dbra %d7,(. + -8)
m68k_0004e2_end:
.org 0x4E6
m68k_0004e6:
        bra.b (. + 0)
m68k_0004e6_end:
.org 0x4E8
m68k_0004e8:
        jsr 0x93f0:l
m68k_0004e8_end:
.org 0x4EE
m68k_0004ee:
        rts
m68k_0004ee_end:
.org 0x556
m68k_000556:
        jsr 0xbaea:l
m68k_000556_end:
.org 0x55C
m68k_00055c:
        rts
m68k_00055c_end:
.org 0x60C
m68k_00060c:
        move.w #0x2700,%sr
m68k_00060c_end:
.org 0x610
m68k_000610:
        bsr.w (. + 122)
m68k_000610_end:
.org 0x614
m68k_000614:
        clr.w 0xf37e:w
m68k_000614_end:
.org 0x618
m68k_000618:
        move.l #0x60a00002,0xc00004:l
m68k_000618_end:
.org 0x622
m68k_000622:
        move.w #0x59f,%d0
m68k_000622_end:
.org 0x626
m68k_000626:
        move.l %d1,0xc00000:l
m68k_000626_end:
.org 0x62C
m68k_00062c:
        dbra %d0,(. + -6)
m68k_00062c_end:
.org 0x630
m68k_000630:
        tst.w 0xf6c4:w
m68k_000630_end:
.org 0x634
m68k_000634:
        bne.b (. + 52)
m68k_000634_end:
.org 0x636
m68k_000636:
        move.l #0x70000001,0xc00004:l
m68k_000636_end:
.org 0x640
m68k_000640:
        lea.l 0x89ddc:l,%a0
m68k_000640_end:
.org 0x646
m68k_000646:
        move.w #0x17,%d0
m68k_000646_end:
.org 0x64A
m68k_00064a:
        move.l (%a0)+,0xc00000:l
m68k_00064a_end:
.org 0x650
m68k_000650:
        dbra %d0,(. + -6)
m68k_000650_end:
.org 0x654
m68k_000654:
        lea.l 0x8a07c:l,%a0
m68k_000654_end:
.org 0x65A
m68k_00065a:
        move.w #0xf,%d0
m68k_00065a_end:
.org 0x65E
m68k_00065e:
        move.l (%a0)+,0xc00000:l
m68k_00065e_end:
.org 0x664
m68k_000664:
        dbra %d0,(. + -6)
m68k_000664_end:
.org 0x668
m68k_000668:
        bsr.w (. + 34)
m68k_000668_end:
.org 0x66C
m68k_00066c:
        lea.l 0xf516:w,%a0
m68k_00066c_end:
.org 0x670
m68k_000670:
        move.w #0x17,%d0
m68k_000670_end:
.org 0x674
m68k_000674:
        move.l %d1,(%a0)+
m68k_000674_end:
.org 0x676
m68k_000676:
        dbra %d0,(. + -2)
m68k_000676_end:
.org 0x67A
m68k_00067a:
        clr.w 0xf37a:w
m68k_00067a_end:
.org 0x67E
m68k_00067e:
        clr.w 0xf37c:w
m68k_00067e_end:
.org 0x682
m68k_000682:
        jsr 0xaf48:l
m68k_000682_end:
.org 0x688
m68k_000688:
        rts
m68k_000688_end:
.org 0x68A
m68k_00068a:
        move.w 0xf6c4:w,%d0
m68k_00068a_end:
.org 0x68E
m68k_00068e:
        lsl.w #0x2,%d0
m68k_00068e_end:
.org 0x690
m68k_000690:
        move.l 4(%pc, %d0.w),%d1
m68k_000690_end:
.org 0x694
m68k_000694:
        rts
m68k_000694_end:
.org 0x814
m68k_000814:
        move.w #0x2700,%sr
m68k_000814_end:
.org 0x818
m68k_000818:
        lea.l 0xd300:w,%a1
m68k_000818_end:
.org 0x81C
m68k_00081c:
        move.w #0x1f,%d0
m68k_00081c_end:
.org 0x820
m68k_000820:
        move.l #0x11111111,(%a1)+
m68k_000820_end:
.org 0x826
m68k_000826:
        dbra %d0,(. + -6)
m68k_000826_end:
.org 0x82A
m68k_00082a:
        move.w #0x1,%d0
m68k_00082a_end:
.org 0x82E
m68k_00082e:
        move.w #0x3,%d1
m68k_00082e_end:
.org 0x832
m68k_000832:
        move.w #0x2,%d3
m68k_000832_end:
.org 0x836
m68k_000836:
        lea.l 160(%pc),%a0
m68k_000836_end:
.org 0x83A
m68k_00083a:
        nop
m68k_00083a_end:
.org 0x83C
m68k_00083c:
        jsr 0xae8a:l
m68k_00083c_end:
.org 0x842
m68k_000842:
        move.l #0x50000000,0xc00004:l
m68k_000842_end:
.org 0x84C
m68k_00084c:
        lea.l 0xd300:w,%a0
m68k_00084c_end:
.org 0x850
m68k_000850:
        move.w #0xdf,%d0
m68k_000850_end:
.org 0x854
m68k_000854:
        move.l (%a0)+,0xc00000:l
m68k_000854_end:
.org 0x85A
m68k_00085a:
        dbra %d0,(. + -6)
m68k_00085a_end:
.org 0x85E
m68k_00085e:
        move.w #0x1,%d0
m68k_00085e_end:
.org 0x862
m68k_000862:
        move.w #0x3,%d1
m68k_000862_end:
.org 0x866
m68k_000866:
        jsr 0x506c:l
m68k_000866_end:
.org 0x86C
m68k_00086c:
        cmpi.w #0x27,0xf38c:w
m68k_00086c_end:
.org 0x872
m68k_000872:
        bne.b (. + 62)
m68k_000872_end:
.org 0x8B0
m68k_0008b0:
        cmpi.w #0xb1,0xf38c:w
m68k_0008b0_end:
.org 0x8B6
m68k_0008b6:
        beq.w (. + 14)
m68k_0008b6_end:
.org 0x8BA
m68k_0008ba:
        cmpi.w #0xba,0xf38c:w
m68k_0008ba_end:
.org 0x8C0
m68k_0008c0:
        bne.w (. + 10)
m68k_0008c0_end:
.org 0x8CA
m68k_0008ca:
        move.w #0x12,0xf362:w
m68k_0008ca_end:
.org 0x8D0
m68k_0008d0:
        jsr 0xaf48:l
m68k_0008d0_end:
.org 0x8D6
m68k_0008d6:
        rts
m68k_0008d6_end:
.org 0x8DE
m68k_0008de:
        jsr 0xdf6e:l
m68k_0008de_end:
.org 0x8E4
m68k_0008e4:
        rts
m68k_0008e4_end:
.org 0xC2E
m68k_000c2e:
        move.w #0x2700,%sr
m68k_000c2e_end:
.org 0xC32
m68k_000c32:
        move.w #0x1,%d0
m68k_000c32_end:
.org 0xC36
m68k_000c36:
        move.w #0x3,%d1
m68k_000c36_end:
.org 0xC3A
m68k_000c3a:
        jsr 0x506c:l
m68k_000c3a_end:
.org 0xC40
m68k_000c40:
        jsr 0xaf48:l
m68k_000c40_end:
.org 0xC46
m68k_000c46:
        clr.w 0xf37e:w
m68k_000c46_end:
.org 0xC4A
m68k_000c4a:
        rts
m68k_000c4a_end:
.org 0xC90
m68k_000c90:
        move.w #0x2700,%sr
m68k_000c90_end:
.org 0xC94
m68k_000c94:
        jsr 0x16acc:l
m68k_000c94_end:
.org 0xC9A
m68k_000c9a:
        jsr 0xaf48:l
m68k_000c9a_end:
.org 0xCA0
m68k_000ca0:
        rts
m68k_000ca0_end:
.org 0xDC0
m68k_000dc0:
        move.w 0xf6c4:w,0xefe0:w
m68k_000dc0_end:
.org 0xDC6
m68k_000dc6:
        jsr 0x1d57a:l
m68k_000dc6_end:
.org 0xDCC
m68k_000dcc:
        move.w #0x2,0xf6c4:w
m68k_000dcc_end:
.org 0xDD2
m68k_000dd2:
        clr.w 0xf31e:w
m68k_000dd2_end:
.org 0xDD6
m68k_000dd6:
        jsr 0x3d654:l
m68k_000dd6_end:
.org 0xDDC
m68k_000ddc:
        jsr 0x6826:l
m68k_000ddc_end:
.org 0xDE2
m68k_000de2:
        cmpi.w #0x1,0xffff8114:l
m68k_000de2_end:
.org 0xDEA
m68k_000dea:
        beq.w (. + 42)
m68k_000dea_end:
.org 0xDEE
m68k_000dee:
        jsr 0x188a6:l
m68k_000dee_end:
.org 0xDF4
m68k_000df4:
        tst.w 0xefe0:w
m68k_000df4_end:
.org 0xDF8
m68k_000df8:
        beq.w (. + 98)
m68k_000df8_end:
.org 0xDFC
m68k_000dfc:
        move.w #0x400,0xf612:w
m68k_000dfc_end:
.org 0xE02
m68k_000e02:
        clr.w 0xf362:w
m68k_000e02_end:
.org 0xE06
m68k_000e06:
        clr.w 0xf352:w
m68k_000e06_end:
.org 0xE0A
m68k_000e0a:
        move.w #0x1,0xf6c4:w
m68k_000e0a_end:
.org 0xE10
m68k_000e10:
        bra.w (. + 100)
m68k_000e10_end:
.org 0xE14
m68k_000e14:
        move.w #0x3,0xf6c4:w
m68k_000e14_end:
.org 0xE1A
m68k_000e1a:
        move.w #0x1,0xff70f4:l
m68k_000e1a_end:
.org 0xE22
m68k_000e22:
        jsr 0x26db4:l
m68k_000e22_end:
.org 0xE28
m68k_000e28:
        move.w #0x2700,%sr
m68k_000e28_end:
.org 0xE2C
m68k_000e2c:
        jsr 0x6826:l
m68k_000e2c_end:
.org 0xE32
m68k_000e32:
        jsr 0x18b00:l
m68k_000e32_end:
.org 0xE38
m68k_000e38:
        bcs.b (. + -108)
m68k_000e38_end:
.org 0xE3A
m68k_000e3a:
        jsr 0x1d598:l
m68k_000e3a_end:
.org 0xE40
m68k_000e40:
        tst.w 0xefe0:w
m68k_000e40_end:
.org 0xE44
m68k_000e44:
        beq.w (. + 22)
m68k_000e44_end:
.org 0xE48
m68k_000e48:
        move.w #0x400,0xf612:w
m68k_000e48_end:
.org 0xE4E
m68k_000e4e:
        clr.w 0xf362:w
m68k_000e4e_end:
.org 0xE52
m68k_000e52:
        clr.w 0xf352:w
m68k_000e52_end:
.org 0xE56
m68k_000e56:
        bra.w (. + 30)
m68k_000e56_end:
.org 0xE5A
m68k_000e5a:
        jsr 0x1d03c:l
m68k_000e5a_end:
.org 0xE60
m68k_000e60:
        move.w #0x0,0xf6c4:w
m68k_000e60_end:
.org 0xE66
m68k_000e66:
        move.w #0x200,0xf612:w
m68k_000e66_end:
.org 0xE6C
m68k_000e6c:
        clr.w 0xf352:w
m68k_000e6c_end:
.org 0xE70
m68k_000e70:
        clr.w 0xf764:w
m68k_000e70_end:
.org 0xE74
m68k_000e74:
        jsr 0x1d542:l
m68k_000e74_end:
.org 0xE7A
m68k_000e7a:
        rts
m68k_000e7a_end:
.org 0xF10
m68k_000f10:
        jsr 0x4890:l
m68k_000f10_end:
.org 0xF16
m68k_000f16:
        jsr 0x4998:l
m68k_000f16_end:
.org 0xF1C
m68k_000f1c:
        move.w 0xf606:w,%d0
m68k_000f1c_end:
.org 0xF20
m68k_000f20:
        ori.b #0x40,%d0
m68k_000f20_end:
.org 0xF24
m68k_000f24:
        move.w %d0,0xc00004:l
m68k_000f24_end:
.org 0xF2A
m68k_000f2a:
        jsr 0xa370:l
m68k_000f2a_end:
.org 0xF30
m68k_000f30:
        move.w 0xf612:w,%d0
m68k_000f30_end:
.org 0xF34
m68k_000f34:
        andi.w #0xff,%d0
m68k_000f34_end:
.org 0xF38
m68k_000f38:
        lsl.w #0x1,%d0
m68k_000f38_end:
.org 0xF3A
m68k_000f3a:
        move.w 60(%pc, %d0.w),%d0
m68k_000f3a_end:
.org 0xF3E
m68k_000f3e:
        lea.l 88(%pc),%a0
m68k_000f3e_end:
.org 0xF42
m68k_000f42:
        nop
m68k_000f42_end:
.org 0xF44
m68k_000f44:
        jsr (%a0, %d0.w)
m68k_000f44_end:
.org 0xF48
m68k_000f48:
        tst.w 0xf6c4:w
m68k_000f48_end:
.org 0xF4C
m68k_000f4c:
        bne.w (. + 42)
m68k_000f4c_end:
.org 0xF50
m68k_000f50:
        cmpi.w #0x200,0xf612:w
m68k_000f50_end:
.org 0xF56
m68k_000f56:
        bne.w (. + 14)
m68k_000f56_end:
.org 0xF64
m68k_000f64:
        jsr 0x15de6:l
m68k_000f64_end:
.org 0xF6A
m68k_000f6a:
        jsr 0x169aa:l
m68k_000f6a_end:
.org 0xF70
m68k_000f70:
        jsr 0x679fc:l
m68k_000f70_end:
.org 0xF76
m68k_000f76:
        rts
m68k_000f76_end:
.org 0x1264
m68k_001264:
        btst.b #0x3,0xf3a4:w
m68k_001264_end:
.org 0x126A
m68k_00126a:
        bne.w (. + 36)
m68k_00126a_end:
.org 0x126E
m68k_00126e:
        move.w #0x74,0xf600:w
m68k_00126e_end:
.org 0x1274
m68k_001274:
        jsr 0x5abc:l
m68k_001274_end:
.org 0x127A
m68k_00127a:
        bra.w (. + 20)
m68k_00127a_end:
.org 0x128E
m68k_00128e:
        rts
m68k_00128e_end:
.org 0x133A
m68k_00133a:
        clr.l 0xf39e:w
m68k_00133a_end:
.org 0x133E
m68k_00133e:
        clr.l 0xf3ba:w
m68k_00133e_end:
.org 0x1342
m68k_001342:
        rts
m68k_001342_end:
.org 0x1344
m68k_001344:
        btst.b #0x2,0xf321:w
m68k_001344_end:
.org 0x134A
m68k_00134a:
        bne.w (. + 70)
m68k_00134a_end:
.org 0x134E
m68k_00134e:
        btst.b #0x1,0xf31c:w
m68k_00134e_end:
.org 0x1354
m68k_001354:
        bne.w (. + 60)
m68k_001354_end:
.org 0x1390
m68k_001390:
        rts
m68k_001390_end:
.org 0x1406
m68k_001406:
        lea.l 0xf428:w,%a0
m68k_001406_end:
.org 0x140A
m68k_00140a:
        move.b (%a0)+,%d0
m68k_00140a_end:
.org 0x140C
m68k_00140c:
        cmp.b 0xf67b:w,%d0
m68k_00140c_end:
.org 0x1410
m68k_001410:
        beq.w (. + 20)
m68k_001410_end:
.org 0x1414
m68k_001414:
        cmp.b 0xf67d:w,%d0
m68k_001414_end:
.org 0x1418
m68k_001418:
        beq.w (. + 12)
m68k_001418_end:
.org 0x141C
m68k_00141c:
        cmp.b 0xf67f:w,%d0
m68k_00141c_end:
.org 0x1420
m68k_001420:
        bne.w (. + 30)
m68k_001420_end:
.org 0x143E
m68k_00143e:
        andi.w #0xfffe,%sr
m68k_00143e_end:
.org 0x1442
m68k_001442:
        rts
m68k_001442_end:
.org 0x1798
m68k_001798:
        jsr 0xd8ec:l
m68k_001798_end:
.org 0x179E
m68k_00179e:
        bsr.w (. + -1114)
m68k_00179e_end:
.org 0x17A2
m68k_0017a2:
        move.w 0xf362:w,%d0
m68k_0017a2_end:
.org 0x17A6
m68k_0017a6:
        lsl.w #0x1,%d0
m68k_0017a6_end:
.org 0x17A8
m68k_0017a8:
        move.w 40(%pc, %d0.w),%d0
m68k_0017a8_end:
.org 0x17AC
m68k_0017ac:
        jsr 76(%pc, %d0.w)
m68k_0017ac_end:
.org 0x17B0
m68k_0017b0:
        jsr 0xa3da:l
m68k_0017b0_end:
.org 0x17B6
m68k_0017b6:
        cmpi.w #0x6,0xf362:w
m68k_0017b6_end:
.org 0x17BC
m68k_0017bc:
        bne.w (. + 14)
m68k_0017bc_end:
.org 0x17CA
m68k_0017ca:
        jsr 0xa158:l
m68k_0017ca_end:
.org 0x17D0
m68k_0017d0:
        rts
m68k_0017d0_end:
.org 0x1BDC
m68k_001bdc:
        bsr.w (. + 54)
m68k_001bdc_end:
.org 0x1BE0
m68k_001be0:
        bcs.w (. + 48)
m68k_001be0_end:
.org 0x1BE4
m68k_001be4:
        move.w 0xf364:w,0xf392:w
m68k_001be4_end:
.org 0x1BEA
m68k_001bea:
        addq.w #0x1,0xf394:w
m68k_001bea_end:
.org 0x1BEE
m68k_001bee:
        move.w #0x208,0xf612:w
m68k_001bee_end:
.org 0x1BF4
m68k_001bf4:
        move.w #0x4,0xf362:w
m68k_001bf4_end:
.org 0x1BFA
m68k_001bfa:
        move.w #0x91,0xf38c:w
m68k_001bfa_end:
.org 0x1C00
m68k_001c00:
        clr.w 0xf576:w
m68k_001c00_end:
.org 0x1C04
m68k_001c04:
        move.w #0x82,0xf380:w
m68k_001c04_end:
.org 0x1C0A
m68k_001c0a:
        jsr 0x5abc:l
m68k_001c0a_end:
.org 0x1C10
m68k_001c10:
        rts
m68k_001c10_end:
.org 0x1C88
m68k_001c88:
        cmpi.w #0xb,0xf38c:w
m68k_001c88_end:
.org 0x1C8E
m68k_001c8e:
        bne.w (. + 22)
m68k_001c8e_end:
.org 0x1C92
m68k_001c92:
        move.w 0xf364:w,%d1
m68k_001c92_end:
.org 0x1C96
m68k_001c96:
        lsl.w #0x2,%d1
m68k_001c96_end:
.org 0x1C98
m68k_001c98:
        lea.l 0xcdfc:w,%a0
m68k_001c98_end:
.org 0x1C9C
m68k_001c9c:
        tst.b (%a0, %d1.w)
m68k_001c9c_end:
.org 0x1CA0
m68k_001ca0:
        bne.w (. + 74)
m68k_001ca0_end:
.org 0x1CA4
m68k_001ca4:
        andi.w #0xfffe,%sr
m68k_001ca4_end:
.org 0x1CA8
m68k_001ca8:
        rts
m68k_001ca8_end:
.org 0x1CAA
m68k_001caa:
        move.w #0x97,%d0
m68k_001caa_end:
.org 0x1CAE
m68k_001cae:
        jsr 0x676f2:l
m68k_001cae_end:
.org 0x1CB4
m68k_001cb4:
        ori.w #0x1,%sr
m68k_001cb4_end:
.org 0x1CB8
m68k_001cb8:
        rts
m68k_001cb8_end:
.org 0x1CBA
m68k_001cba:
        move.w #0xb9,%d0
m68k_001cba_end:
.org 0x1CBE
m68k_001cbe:
        jsr 0x676f2:l
m68k_001cbe_end:
.org 0x1CC4
m68k_001cc4:
        ori.w #0x1,%sr
m68k_001cc4_end:
.org 0x1CC8
m68k_001cc8:
        rts
m68k_001cc8_end:
.org 0x1CCA
m68k_001cca:
        move.w #0xaa,%d0
m68k_001cca_end:
.org 0x1CCE
m68k_001cce:
        jsr 0x676f2:l
m68k_001cce_end:
.org 0x1CD4
m68k_001cd4:
        ori.w #0x1,%sr
m68k_001cd4_end:
.org 0x1CD8
m68k_001cd8:
        rts
m68k_001cd8_end:
.org 0x1CEA
m68k_001cea:
        move.w #0xb8,%d0
m68k_001cea_end:
.org 0x1CEE
m68k_001cee:
        jsr 0x676f2:l
m68k_001cee_end:
.org 0x1CF4
m68k_001cf4:
        ori.w #0x1,%sr
m68k_001cf4_end:
.org 0x1CF8
m68k_001cf8:
        rts
m68k_001cf8_end:
.org 0x1D18
m68k_001d18:
        lea.l 0xd100:w,%a0
m68k_001d18_end:
.org 0x1D1C
m68k_001d1c:
        adda.w 0xf31a:w,%a0
m68k_001d1c_end:
.org 0x1D20
m68k_001d20:
        move.w #0x28,0x54(%a0)
m68k_001d20_end:
.org 0x1D26
m68k_001d26:
        move.w #0x28,(%a0)+
m68k_001d26_end:
.org 0x1D2A
m68k_001d2a:
        move.w 0xf36a:w,%d0
m68k_001d2a_end:
.org 0x1D2E
m68k_001d2e:
        lsl.w #0x8,%d0
m68k_001d2e_end:
.org 0x1D30
m68k_001d30:
        addi.w #0xc000,%d0
m68k_001d30_end:
.org 0x1D34
m68k_001d34:
        move.w %d0,0x54(%a0)
m68k_001d34_end:
.org 0x1D38
m68k_001d38:
        addi.w #0x80,0x54(%a0)
m68k_001d38_end:
.org 0x1D3E
m68k_001d3e:
        move.w %d0,(%a0)+
m68k_001d3e_end:
.org 0x1D40
m68k_001d40:
        move.w #0x27,%d0
m68k_001d40_end:
.org 0x1D44
m68k_001d44:
        move.w #0x8000,0x54(%a0)
m68k_001d44_end:
.org 0x1D4A
m68k_001d4a:
        move.w #0x8000,(%a0)+
m68k_001d4a_end:
.org 0x1D4E
m68k_001d4e:
        dbra %d0,(. + -10)
m68k_001d4e_end:
.org 0x1D52
m68k_001d52:
        clr.w 0x54(%a0)
m68k_001d52_end:
.org 0x1D56
m68k_001d56:
        addi.w #0xa8,0xf31a:w
m68k_001d56_end:
.org 0x1D5C
m68k_001d5c:
        rts
m68k_001d5c_end:
.org 0x2004
m68k_002004:
        tst.w 0xf652:w
m68k_002004_end:
.org 0x2008
m68k_002008:
        beq.w (. + 26)
m68k_002008_end:
.org 0x2022
m68k_002022:
        jsr 0x674ca:l
m68k_002022_end:
.org 0x2028
m68k_002028:
        rts
m68k_002028_end:
.org 0x202A
m68k_00202a:
        tst.w 0xf652:w
m68k_00202a_end:
.org 0x202E
m68k_00202e:
        beq.w (. + 20)
m68k_00202e_end:
.org 0x2042
m68k_002042:
        jsr 0x671b6:l
m68k_002042_end:
.org 0x2048
m68k_002048:
        rts
m68k_002048_end:
.org 0x2416
m68k_002416:
        move.w 0xf362:w,%d0
m68k_002416_end:
.org 0x241A
m68k_00241a:
        lsl.w #0x1,%d0
m68k_00241a_end:
.org 0x241C
m68k_00241c:
        move.w 26(%pc, %d0.w),%d0
m68k_00241c_end:
.org 0x2420
m68k_002420:
        jsr 110(%pc, %d0.w)
m68k_002420_end:
.org 0x2424
m68k_002424:
        jsr 0xd8ec:l
m68k_002424_end:
.org 0x242A
m68k_00242a:
        jsr 0xa158:l
m68k_00242a_end:
.org 0x2430
m68k_002430:
        jsr 0xa3da:l
m68k_002430_end:
.org 0x2436
m68k_002436:
        rts
m68k_002436_end:
.org 0x2490
m68k_002490:
        move.w 0xf380:w,%d0
m68k_002490_end:
.org 0x2494
m68k_002494:
        cmpi.w #0x60,%d0
m68k_002494_end:
.org 0x2498
m68k_002498:
        bcc.w (. + 104)
m68k_002498_end:
.org 0x249C
m68k_00249c:
        move.w 0xf3a4:w,%d1
m68k_00249c_end:
.org 0x24A0
m68k_0024a0:
        andi.w #0xe40,%d1
m68k_0024a0_end:
.org 0x24A4
m68k_0024a4:
        beq.w (. + 36)
m68k_0024a4_end:
.org 0x24A8
m68k_0024a8:
        move.w #0x7,0xf362:w
m68k_0024a8_end:
.org 0x24AE
m68k_0024ae:
        move.w #0x9,%d0
m68k_0024ae_end:
.org 0x24B2
m68k_0024b2:
        btst.b #0x6,0xf3a4:w
m68k_0024b2_end:
.org 0x24B8
m68k_0024b8:
        bne.w (. + 8)
m68k_0024b8_end:
.org 0x24C0
m68k_0024c0:
        move.w %d0,0xf36a:w
m68k_0024c0_end:
.org 0x24C4
m68k_0024c4:
        bra.w (. + 14)
m68k_0024c4_end:
.org 0x24C8
m68k_0024c8:
        lsl.w #0x1,%d0
m68k_0024c8_end:
.org 0x24CA
m68k_0024ca:
        move.w 8(%pc, %d0.w),%d0
m68k_0024ca_end:
.org 0x24CE
m68k_0024ce:
        jsr 12(%pc, %d0.w)
m68k_0024ce_end:
.org 0x24D2
m68k_0024d2:
        rts
m68k_0024d2_end:
.org 0x24F8
m68k_0024f8:
        jsr 0xbbda:l
m68k_0024f8_end:
.org 0x24FE
m68k_0024fe:
        rts
m68k_0024fe_end:
.org 0x2500
m68k_002500:
        cmpi.w #0xff,%d0
m68k_002500_end:
.org 0x2504
m68k_002504:
        bne.w (. + 58)
m68k_002504_end:
.org 0x2508
m68k_002508:
        move.w 0xf3a4:w,%d0
m68k_002508_end:
.org 0x250C
m68k_00250c:
        andi.w #0x3fff,%d0
m68k_00250c_end:
.org 0x2510
m68k_002510:
        bne.b (. + -104)
m68k_002510_end:
.org 0x2512
m68k_002512:
        move.w #0x208,0xf3c2:w
m68k_002512_end:
.org 0x2518
m68k_002518:
        move.w #0x208,0xf38a:w
m68k_002518_end:
.org 0x251E
m68k_00251e:
        move.w #0x3,0xf362:w
m68k_00251e_end:
.org 0x2524
m68k_002524:
        clr.w 0xf36a:w
m68k_002524_end:
.org 0x2528
m68k_002528:
        clr.w 0xf612:w
m68k_002528_end:
.org 0x252C
m68k_00252c:
        move.w #0x60,0xf600:w
m68k_00252c_end:
.org 0x2532
m68k_002532:
        bclr.b #0x3,0xf31c:w
m68k_002532_end:
.org 0x2538
m68k_002538:
        clr.w 0xf3a4:w
m68k_002538_end:
.org 0x253C
m68k_00253c:
        bra.b (. + -106)
m68k_00253c_end:
.org 0x253E
m68k_00253e:
        subi.w #0x60,%d0
m68k_00253e_end:
.org 0x2542
m68k_002542:
        lsl.w #0x1,%d0
m68k_002542_end:
.org 0x2544
m68k_002544:
        move.w 8(%pc, %d0.w),%d0
m68k_002544_end:
.org 0x2548
m68k_002548:
        jsr 110(%pc, %d0.w)
m68k_002548_end:
.org 0x254C
m68k_00254c:
        bra.b (. + -122)
m68k_00254c_end:
.org 0x26B6
m68k_0026b6:
        tst.w 0xf3a2:w
m68k_0026b6_end:
.org 0x26BA
m68k_0026ba:
        bne.w (. + 28)
m68k_0026ba_end:
.org 0x26BE
m68k_0026be:
        move.w 0xf392:w,0xf3a8:w
m68k_0026be_end:
.org 0x26C4
m68k_0026c4:
        move.w 0xf35e:w,0xf3aa:w
m68k_0026c4_end:
.org 0x26CA
m68k_0026ca:
        move.w 0xf360:w,0xf3ac:w
m68k_0026ca_end:
.org 0x26D0
m68k_0026d0:
        move.w 0xf364:w,0xf3ae:w
m68k_0026d0_end:
.org 0x26D6
m68k_0026d6:
        bra.w (. + -282)
m68k_0026d6_end:
.org 0x2856
m68k_002856:
        move.w 0xf3a4:w,%d1
m68k_002856_end:
.org 0x285A
m68k_00285a:
        andi.w #0x640,%d1
m68k_00285a_end:
.org 0x285E
m68k_00285e:
        beq.w (. + 36)
m68k_00285e_end:
.org 0x2882
m68k_002882:
        move.w #0x5c,0xf600:w
m68k_002882_end:
.org 0x2888
m68k_002888:
        move.w #0x1,0xf608:w
m68k_002888_end:
.org 0x288E
m68k_00288e:
        clr.w 0xf386:w
m68k_00288e_end:
.org 0x2892
m68k_002892:
        rts
m68k_002892_end:
.org 0x2A54
m68k_002a54:
        move.w #0x5,0xf39a:w
m68k_002a54_end:
.org 0x2A5A
m68k_002a5a:
        move.w #0x4c,0xf600:w
m68k_002a5a_end:
.org 0x2A60
m68k_002a60:
        bra.w (. + -1020)
m68k_002a60_end:
.org 0x2A64
m68k_002a64:
        move.w #0x1b,0xf362:w
m68k_002a64_end:
.org 0x2A6A
m68k_002a6a:
        move.l 0xf3e4:w,0xcfae:w
m68k_002a6a_end:
.org 0x2A70
m68k_002a70:
        rts
m68k_002a70_end:
.org 0x2E9C
m68k_002e9c:
        tst.w 0xf380:w
m68k_002e9c_end:
.org 0x2EA0
m68k_002ea0:
        bne.w (. + 14)
m68k_002ea0_end:
.org 0x2EAE
m68k_002eae:
        jsr 0xc138:l
m68k_002eae_end:
.org 0x2EB4
m68k_002eb4:
        jsr 0xbfa2:l
m68k_002eb4_end:
.org 0x2EBA
m68k_002eba:
        bra.w (. + 42)
m68k_002eba_end:
.org 0x2EE4
m68k_002ee4:
        rts
m68k_002ee4_end:
.org 0x2F10
m68k_002f10:
        jsr 0x662e4:l
m68k_002f10_end:
.org 0x2F16
m68k_002f16:
        bcs.w (. + 14)
m68k_002f16_end:
.org 0x2F1A
m68k_002f1a:
        jsr 0xbf5a:l
m68k_002f1a_end:
.org 0x2F20
m68k_002f20:
        bra.w (. + 28)
m68k_002f20_end:
.org 0x2F3C
m68k_002f3c:
        rts
m68k_002f3c_end:
.org 0x2F3E
m68k_002f3e:
        tst.w 0xf322:w
m68k_002f3e_end:
.org 0x2F42
m68k_002f42:
        bne.w (. + 34)
m68k_002f42_end:
.org 0x2F46
m68k_002f46:
        clr.w 0xf386:w
m68k_002f46_end:
.org 0x2F4A
m68k_002f4a:
        clr.w 0xf388:w
m68k_002f4a_end:
.org 0x2F4E
m68k_002f4e:
        jsr 0xc0b6:l
m68k_002f4e_end:
.org 0x2F54
m68k_002f54:
        move.w #0x3,0xf362:w
m68k_002f54_end:
.org 0x2F5A
m68k_002f5a:
        move.w #0x12,0xf36a:w
m68k_002f5a_end:
.org 0x2F60
m68k_002f60:
        bra.w (. + 14)
m68k_002f60_end:
.org 0x2F6E
m68k_002f6e:
        rts
m68k_002f6e_end:
.org 0x2FDC
m68k_002fdc:
        bsr.w (. + -4804)
m68k_002fdc_end:
.org 0x2FE0
m68k_002fe0:
        cmpi.w #0x63,0xf380:w
m68k_002fe0_end:
.org 0x2FE6
m68k_002fe6:
        beq.w (. + 24)
m68k_002fe6_end:
.org 0x2FEA
m68k_002fea:
        cmpi.w #0x60,0xf380:w
m68k_002fea_end:
.org 0x2FF0
m68k_002ff0:
        beq.w (. + 14)
m68k_002ff0_end:
.org 0x2FF4
m68k_002ff4:
        cmpi.w #0x84,0xf380:w
m68k_002ff4_end:
.org 0x2FFA
m68k_002ffa:
        bne.w (. + 10)
m68k_002ffa_end:
.org 0x3004
m68k_003004:
        subq.w #0x1,0xf36a:w
m68k_003004_end:
.org 0x3008
m68k_003008:
        bpl.w (. + 32)
m68k_003008_end:
.org 0x300C
m68k_00300c:
        clr.w 0xf362:w
m68k_00300c_end:
.org 0x3010
m68k_003010:
        clr.w 0xf36a:w
m68k_003010_end:
.org 0x3014
m68k_003014:
        move.w 0xf3a4:w,%d0
m68k_003014_end:
.org 0x3018
m68k_003018:
        andi.w #0x4000,%d0
m68k_003018_end:
.org 0x301C
m68k_00301c:
        beq.w (. + 8)
m68k_00301c_end:
.org 0x3020
m68k_003020:
        bset.l #0xf,%d0
m68k_003020_end:
.org 0x3024
m68k_003024:
        move.w %d0,0xf3a4:w
m68k_003024_end:
.org 0x3028
m68k_003028:
        cmpi.w #0x9,0xf36a:w
m68k_003028_end:
.org 0x302E
m68k_00302e:
        bls.w (. + 10)
m68k_00302e_end:
.org 0x3038
m68k_003038:
        rts
m68k_003038_end:
.org 0x304C
m68k_00304c:
        jsr 0x128e2:l
m68k_00304c_end:
.org 0x3052
m68k_003052:
        rts
m68k_003052_end:
.org 0x3242
m68k_003242:
        btst.b #0x0,0xf3a4:w
m68k_003242_end:
.org 0x3248
m68k_003248:
        bne.w (. + 50)
m68k_003248_end:
.org 0x324C
m68k_00324c:
        cmpi.w #0xb1,0xf38c:w
m68k_00324c_end:
.org 0x3252
m68k_003252:
        beq.w (. + 24)
m68k_003252_end:
.org 0x3256
m68k_003256:
        cmpi.w #0xba,0xf38c:w
m68k_003256_end:
.org 0x325C
m68k_00325c:
        beq.w (. + 14)
m68k_00325c_end:
.org 0x3260
m68k_003260:
        jsr 0x5abc:l
m68k_003260_end:
.org 0x3266
m68k_003266:
        bra.w (. + 10)
m68k_003266_end:
.org 0x3270
m68k_003270:
        jsr 0xc5c2:l
m68k_003270_end:
.org 0x3276
m68k_003276:
        bra.w (. + 10)
m68k_003276_end:
.org 0x327A
m68k_00327a:
        jsr 0xc6f6:l
m68k_00327a_end:
.org 0x3280
m68k_003280:
        rts
m68k_003280_end:
.org 0x3282
m68k_003282:
        move.w 0xf36a:w,%d0
m68k_003282_end:
.org 0x3286
m68k_003286:
        cmpi.w #0x4,%d0
m68k_003286_end:
.org 0x328A
m68k_00328a:
        bcc.w (. + 80)
m68k_00328a_end:
.org 0x328E
m68k_00328e:
        lea.l 0xd100:w,%a0
m68k_00328e_end:
.org 0x3292
m68k_003292:
        adda.w 0xf31a:w,%a0
m68k_003292_end:
.org 0x3296
m68k_003296:
        move.w #0x26,0x50(%a0)
m68k_003296_end:
.org 0x329C
m68k_00329c:
        move.w #0x26,(%a0)+
m68k_00329c_end:
.org 0x32A0
m68k_0032a0:
        lsl.w #0x8,%d0
m68k_0032a0_end:
.org 0x32A2
m68k_0032a2:
        move.w #0xcd82,%d1
m68k_0032a2_end:
.org 0x32A6
m68k_0032a6:
        sub.w %d0,%d1
m68k_0032a6_end:
.org 0x32A8
m68k_0032a8:
        move.w %d1,0x50(%a0)
m68k_0032a8_end:
.org 0x32AC
m68k_0032ac:
        subi.w #0x80,%d1
m68k_0032ac_end:
.org 0x32B0
m68k_0032b0:
        move.w %d1,(%a0)+
m68k_0032b0_end:
.org 0x32B2
m68k_0032b2:
        move.w #0x12,%d0
m68k_0032b2_end:
.org 0x32B6
m68k_0032b6:
        move.l #0x80008000,0x50(%a0)
m68k_0032b6_end:
.org 0x32BE
m68k_0032be:
        move.l #0x80008000,(%a0)+
m68k_0032be_end:
.org 0x32C4
m68k_0032c4:
        dbra %d0,(. + -14)
m68k_0032c4_end:
.org 0x32C8
m68k_0032c8:
        clr.w 0x50(%a0)
m68k_0032c8_end:
.org 0x32CC
m68k_0032cc:
        addi.w #0xa0,0xf31a:w
m68k_0032cc_end:
.org 0x32D2
m68k_0032d2:
        addq.w #0x1,0xf36a:w
m68k_0032d2_end:
.org 0x32D6
m68k_0032d6:
        bra.w (. + 52)
m68k_0032d6_end:
.org 0x32DA
m68k_0032da:
        move.w 0xf3c4:w,0xf362:w
m68k_0032da_end:
.org 0x32E0
m68k_0032e0:
        move.w 0xf3c2:w,0xf612:w
m68k_0032e0_end:
.org 0x32E6
m68k_0032e6:
        bclr.b #0x3,0xf31c:w
m68k_0032e6_end:
.org 0x32EC
m68k_0032ec:
        clr.w 0xf3a4:w
m68k_0032ec_end:
.org 0x32F0
m68k_0032f0:
        cmpi.w #0x208,0xf612:w
m68k_0032f0_end:
.org 0x32F6
m68k_0032f6:
        bne.w (. + 20)
m68k_0032f6_end:
.org 0x330A
m68k_00330a:
        rts
m68k_00330a_end:
.org 0x33E8
m68k_0033e8:
        btst.b #0x0,0xf3a4:w
m68k_0033e8_end:
.org 0x33EE
m68k_0033ee:
        bne.w (. + 38)
m68k_0033ee_end:
.org 0x33F2
m68k_0033f2:
        jsr 0x1306a:l
m68k_0033f2_end:
.org 0x33F8
m68k_0033f8:
        jsr 0x13188:l
m68k_0033f8_end:
.org 0x33FE
m68k_0033fe:
        jsr 0x1321c:l
m68k_0033fe_end:
.org 0x3404
m68k_003404:
        jsr 0x13270:l
m68k_003404_end:
.org 0x340A
m68k_00340a:
        jsr 0x676c4:l
m68k_00340a_end:
.org 0x3410
m68k_003410:
        bra.w (. + 16)
m68k_003410_end:
.org 0x3414
m68k_003414:
        jsr 0x1321c:l
m68k_003414_end:
.org 0x341A
m68k_00341a:
        jsr 0x132ae:l
m68k_00341a_end:
.org 0x3420
m68k_003420:
        rts
m68k_003420_end:
.org 0x3422
m68k_003422:
        jsr 0x13934:l
m68k_003422_end:
.org 0x3428
m68k_003428:
        jsr 0x1379a:l
m68k_003428_end:
.org 0x342E
m68k_00342e:
        rts
m68k_00342e_end:
.org 0x3460
m68k_003460:
        btst.b #0x0,0xf3a4:w
m68k_003460_end:
.org 0x3466
m68k_003466:
        bne.w (. + 20)
m68k_003466_end:
.org 0x346A
m68k_00346a:
        jsr 0xd270:l
m68k_00346a_end:
.org 0x3470
m68k_003470:
        jsr 0x676c4:l
m68k_003470_end:
.org 0x3476
m68k_003476:
        bra.w (. + 10)
m68k_003476_end:
.org 0x347A
m68k_00347a:
        jsr 0xd368:l
m68k_00347a_end:
.org 0x3480
m68k_003480:
        rts
m68k_003480_end:
.org 0x36F0
m68k_0036f0:
        jsr 0x16660:l
m68k_0036f0_end:
.org 0x36F6
m68k_0036f6:
        jsr 0xa3da:l
m68k_0036f6_end:
.org 0x36FC
m68k_0036fc:
        rts
m68k_0036fc_end:
.org 0x36FE
m68k_0036fe:
        jsr 0x312c8:l
m68k_0036fe_end:
.org 0x3704
m68k_003704:
        jsr 0xa3da:l
m68k_003704_end:
.org 0x370A
m68k_00370a:
        rts
m68k_00370a_end:
.org 0x378E
m68k_00378e:
        clr.w 0xf32e:w
m68k_00378e_end:
.org 0x3792
m68k_003792:
        move.w #0x2700,%sr
m68k_003792_end:
.org 0x3796
m68k_003796:
        move.w 0xf606:w,%d0
m68k_003796_end:
.org 0x379A
m68k_00379a:
        andi.b #0xbf,%d0
m68k_00379a_end:
.org 0x379E
m68k_00379e:
        move.w %d0,0xc00004:l
m68k_00379e_end:
.org 0x37A4
m68k_0037a4:
        clr.w %d0
m68k_0037a4_end:
.org 0x37A6
m68k_0037a6:
        move.w %d0,0xf312:w
m68k_0037a6_end:
.org 0x37AA
m68k_0037aa:
        move.w %d0,0xf314:w
m68k_0037aa_end:
.org 0x37AE
m68k_0037ae:
        move.w %d0,0xf316:w
m68k_0037ae_end:
.org 0x37B2
m68k_0037b2:
        move.w %d0,0xf318:w
m68k_0037b2_end:
.org 0x37B6
m68k_0037b6:
        jsr 0x68ce:l
m68k_0037b6_end:
.org 0x37BC
m68k_0037bc:
        jsr 0x6826:l
m68k_0037bc_end:
.org 0x37C2
m68k_0037c2:
        move.l #0x60000002,0xc00004:l
m68k_0037c2_end:
.org 0x37CC
m68k_0037cc:
        lea.l 0xc00000:l,%a5
m68k_0037cc_end:
.org 0x37D2
m68k_0037d2:
        move.w #0x0,%d6
m68k_0037d2_end:
.org 0x37D6
m68k_0037d6:
        move.w #0x1fff,%d7
m68k_0037d6_end:
.org 0x37DA
m68k_0037da:
        move.w %d6,(%a5)
m68k_0037da_end:
.org 0x37DC
m68k_0037dc:
        dbra %d7,(. + -2)
m68k_0037dc_end:
.org 0x37E0
m68k_0037e0:
        move.w #0x8f02,0xc00004:l
m68k_0037e0_end:
.org 0x37E8
m68k_0037e8:
        move.w #0x8230,0xc00004:l
m68k_0037e8_end:
.org 0x37F0
m68k_0037f0:
        move.w #0x8330,0xc00004:l
m68k_0037f0_end:
.org 0x37F8
m68k_0037f8:
        move.w #0x8407,0xc00004:l
m68k_0037f8_end:
.org 0x3800
m68k_003800:
        move.w #0x855c,0xc00004:l
m68k_003800_end:
.org 0x3808
m68k_003808:
        move.w #0x8700,0xc00004:l
m68k_003808_end:
.org 0x3810
m68k_003810:
        move.w #0x8b00,0xc00004:l
m68k_003810_end:
.org 0x3818
m68k_003818:
        move.w #0x8c81,0xc00004:l
m68k_003818_end:
.org 0x3820
m68k_003820:
        move.w #0x8d2f,0xc00004:l
m68k_003820_end:
.org 0x3828
m68k_003828:
        move.w #0x8f02,0xc00004:l
m68k_003828_end:
.org 0x3830
m68k_003830:
        move.w #0x9011,0xc00004:l
m68k_003830_end:
.org 0x3838
m68k_003838:
        move.w #0x9180,0xc00004:l
m68k_003838_end:
.org 0x3840
m68k_003840:
        move.w #0x9200,0xc00004:l
m68k_003840_end:
.org 0x3848
m68k_003848:
        lea.l 0x5d5e4:l,%a0
m68k_003848_end:
.org 0x384E
m68k_00384e:
        move.w #0x0,%d0
m68k_00384e_end:
.org 0x3852
m68k_003852:
        jsr 0x3ab52:l
m68k_003852_end:
.org 0x3858
m68k_003858:
        lea.l 0x5f137:l,%a0
m68k_003858_end:
.org 0x385E
m68k_00385e:
        move.w #0x2000,%d0
m68k_00385e_end:
.org 0x3862
m68k_003862:
        jsr 0x3ab52:l
m68k_003862_end:
.org 0x3868
m68k_003868:
        lea.l 0x60e6c:l,%a0
m68k_003868_end:
.org 0x386E
m68k_00386e:
        move.w #0x4000,%d0
m68k_00386e_end:
.org 0x3872
m68k_003872:
        jsr 0x3ab52:l
m68k_003872_end:
.org 0x3878
m68k_003878:
        lea.l 0x6254f:l,%a0
m68k_003878_end:
.org 0x387E
m68k_00387e:
        move.w #0x8000,%d0
m68k_00387e_end:
.org 0x3882
m68k_003882:
        jsr 0x3ab52:l
m68k_003882_end:
.org 0x3888
m68k_003888:
        lea.l 0x64340:l,%a0
m68k_003888_end:
.org 0x388E
m68k_00388e:
        move.w #0xa000,%d0
m68k_00388e_end:
.org 0x3892
m68k_003892:
        jsr 0x3ab52:l
m68k_003892_end:
.org 0x3898
m68k_003898:
        move.w #0x8f02,0xc00004:l
m68k_003898_end:
.org 0x38A0
m68k_0038a0:
        move.l #0x6e000001,0xc00004:l
m68k_0038a0_end:
.org 0x38AA
m68k_0038aa:
        lea.l 0xd374a:l,%a0
m68k_0038aa_end:
.org 0x38B0
m68k_0038b0:
        move.w #0x3ff,%d0
m68k_0038b0_end:
.org 0x38B4
m68k_0038b4:
        move.l (%a0)+,0xc00000:l
m68k_0038b4_end:
.org 0x38BA
m68k_0038ba:
        dbra %d0,(. + -6)
m68k_0038ba_end:
.org 0x38BE
m68k_0038be:
        lea.l 0x655f1:l,%a0
m68k_0038be_end:
.org 0x38C4
m68k_0038c4:
        lea.l 0xe000:l,%a1
m68k_0038c4_end:
.org 0x38CA
m68k_0038ca:
        move.l #0x80,%d5
m68k_0038ca_end:
.org 0x38D0
m68k_0038d0:
        move.w #0x20,%d6
m68k_0038d0_end:
.org 0x38D4
m68k_0038d4:
        jsr 0x3aab6:l
m68k_0038d4_end:
.org 0x38DA
m68k_0038da:
        lea.l 0x65df3:l,%a0
m68k_0038da_end:
.org 0x38E0
m68k_0038e0:
        lea.l 0xe040:l,%a1
m68k_0038e0_end:
.org 0x38E6
m68k_0038e6:
        move.l #0x80,%d5
m68k_0038e6_end:
.org 0x38EC
m68k_0038ec:
        jsr 0x3aace:l
m68k_0038ec_end:
.org 0x38F2
m68k_0038f2:
        moveq #17,%d0
m68k_0038f2_end:
.org 0x38F4
m68k_0038f4:
        jsr 0x3ab94:l
m68k_0038f4_end:
.org 0x38FA
m68k_0038fa:
        jsr 0x3aa8a:l
m68k_0038fa_end:
.org 0x3900
m68k_003900:
        move.w #0xffff,0x80ca:w
m68k_003900_end:
.org 0x3906
m68k_003906:
        move.w #0xffff,0x80cc:w
m68k_003906_end:
.org 0x390C
m68k_00390c:
        move.w #0xffff,0x80ce:w
m68k_00390c_end:
.org 0x3912
m68k_003912:
        move.w #0xffff,0x80d0:w
m68k_003912_end:
.org 0x3918
m68k_003918:
        moveq #1,%d0
m68k_003918_end:
.org 0x391A
m68k_00391a:
        jsr 0x3aa20:l
m68k_00391a_end:
.org 0x3920
m68k_003920:
        clr.b 0xf32b:w
m68k_003920_end:
.org 0x3924
m68k_003924:
        move.w #0x300,0xf612:w
m68k_003924_end:
.org 0x392A
m68k_00392a:
        cmpi.w #0x10,0xf600:w
m68k_00392a_end:
.org 0x3930
m68k_003930:
        beq.w (. + 20)
m68k_003930_end:
.org 0x3934
m68k_003934:
        move.b #0x81,%d0
m68k_003934_end:
.org 0x3938
m68k_003938:
        jsr 0x808a:l
m68k_003938_end:
.org 0x393E
m68k_00393e:
        move.w #0x3,0xf32c:w
m68k_00393e_end:
.org 0x3944
m68k_003944:
        move.w 0xf32c:w,%d2
m68k_003944_end:
.org 0x3948
m68k_003948:
        bsr.w (. + 184)
m68k_003948_end:
.org 0x394C
m68k_00394c:
        move.w #0x4,0xf608:w
m68k_00394c_end:
.org 0x3952
m68k_003952:
        move.w #0x2500,%sr
m68k_003952_end:
.org 0x3956
m68k_003956:
        rts
m68k_003956_end:
.org 0x3A00
m68k_003a00:
        movem.l %d0-%d3/%d5/%a0-%a2,-(%a7)
m68k_003a00_end:
.org 0x3A04
m68k_003a04:
        lea.l 56(%pc),%a0
m68k_003a04_end:
.org 0x3A08
m68k_003a08:
        nop
m68k_003a08_end:
.org 0x3A0A
m68k_003a0a:
        move.w #0x300,%d3
m68k_003a0a_end:
.org 0x3A0E
m68k_003a0e:
        move.w #0x6,%d5
m68k_003a0e_end:
.org 0x3A12
m68k_003a12:
        movea.l (%a0)+,%a1
m68k_003a12_end:
.org 0x3A14
m68k_003a14:
        lea.l 0xd100:w,%a2
m68k_003a14_end:
.org 0x3A18
m68k_003a18:
        move.w #0x20,%d0
m68k_003a18_end:
.org 0x3A1C
m68k_003a1c:
        move.w #0x20,%d1
m68k_003a1c_end:
.org 0x3A20
m68k_003a20:
        jsr 56(%pc)
m68k_003a20_end:
.org 0x3A24
m68k_003a24:
        nop
m68k_003a24_end:
.org 0x3A26
m68k_003a26:
        lea.l 0xd100:w,%a2
m68k_003a26_end:
.org 0x3A2A
m68k_003a2a:
        jsr 214(%pc)
m68k_003a2a_end:
.org 0x3A2E
m68k_003a2e:
        nop
m68k_003a2e_end:
.org 0x3A30
m68k_003a30:
        addi.w #0x10,%d3
m68k_003a30_end:
.org 0x3A34
m68k_003a34:
        dbra %d5,(. + -34)
m68k_003a34_end:
.org 0x3A38
m68k_003a38:
        movem.l (%a7)+,%d0-%d3/%d5/%a0-%a2
m68k_003a38_end:
.org 0x3A3C
m68k_003a3c:
        rts
m68k_003a3c_end:
.org 0x3A5A
m68k_003a5a:
        movem.l %d0-%d7/%a0-%a6,-(%a7)
m68k_003a5a_end:
.org 0x3A5E
m68k_003a5e:
        moveq #0,%d3
m68k_003a5e_end:
.org 0x3A60
m68k_003a60:
        move.w %d1,%d3
m68k_003a60_end:
.org 0x3A62
m68k_003a62:
        lsl.w #0x8,%d3
m68k_003a62_end:
.org 0x3A64
m68k_003a64:
        divu.w %d2,%d3
m68k_003a64_end:
.org 0x3A66
m68k_003a66:
        andi.l #0xffff,%d3
m68k_003a66_end:
.org 0x3A6C
m68k_003a6c:
        lsl.l #0x8,%d3
m68k_003a6c_end:
.org 0x3A6E
m68k_003a6e:
        move.w %d0,%d2
m68k_003a6e_end:
.org 0x3A70
m68k_003a70:
        moveq #0,%d4
m68k_003a70_end:
.org 0x3A72
m68k_003a72:
        move.w %d1,%d5
m68k_003a72_end:
.org 0x3A74
m68k_003a74:
        moveq #0,%d6
m68k_003a74_end:
.org 0x3A76
m68k_003a76:
        movea.l %a2,%a3
m68k_003a76_end:
.org 0x3A78
m68k_003a78:
        bsr.w (. + 42)
m68k_003a78_end:
.org 0x3A7C
m68k_003a7c:
        movem.l %d0/%d2,-(%a7)
m68k_003a7c_end:
.org 0x3A80
m68k_003a80:
        bsr.w (. + 64)
m68k_003a80_end:
.org 0x3A84
m68k_003a84:
        subq.w #0x8,%d5
m68k_003a84_end:
.org 0x3A86
m68k_003a86:
        bls.b (. + 8)
m68k_003a86_end:
.org 0x3A88
m68k_003a88:
        lea.l 0x80(%a3),%a3
m68k_003a88_end:
.org 0x3A8C
m68k_003a8c:
        bra.b (. + -12)
m68k_003a8c_end:
.org 0x3A8E
m68k_003a8e:
        movem.l (%a7)+,%d0/%d2
m68k_003a8e_end:
.org 0x3A92
m68k_003a92:
        add.l %d3,%d4
m68k_003a92_end:
.org 0x3A94
m68k_003a94:
        subq.w #0x1,%d2
m68k_003a94_end:
.org 0x3A96
m68k_003a96:
        beq.b (. + 6)
m68k_003a96_end:
.org 0x3A98
m68k_003a98:
        addq.w #0x4,%a2
m68k_003a98_end:
.org 0x3A9A
m68k_003a9a:
        bra.b (. + -40)
m68k_003a9a_end:
.org 0x3A9C
m68k_003a9c:
        movem.l (%a7)+,%d0-%d7/%a0-%a6
m68k_003a9c_end:
.org 0x3AA0
m68k_003aa0:
        rts
m68k_003aa0_end:
.org 0x3AA2
m68k_003aa2:
        move.w %d1,%d7
m68k_003aa2_end:
.org 0x3AA4
m68k_003aa4:
        lsr.w #0x3,%d7
m68k_003aa4_end:
.org 0x3AA6
m68k_003aa6:
        swap %d4
m68k_003aa6_end:
.org 0x3AA8
m68k_003aa8:
        cmp.w %d0,%d4
m68k_003aa8_end:
.org 0x3AAA
m68k_003aaa:
        bcc.b (. + 12)
m68k_003aaa_end:
.org 0x3AAC
m68k_003aac:
        mulu.w %d4,%d7
m68k_003aac_end:
.org 0x3AAE
m68k_003aae:
        swap %d4
m68k_003aae_end:
.org 0x3AB0
m68k_003ab0:
        lea.l (%a1, %d7.w),%a4
m68k_003ab0_end:
.org 0x3AB4
m68k_003ab4:
        rts
m68k_003ab4_end:
.org 0x3AB6
m68k_003ab6:
        movea.l #0xffffffff,%a4
m68k_003ab6_end:
.org 0x3ABC
m68k_003abc:
        swap %d4
m68k_003abc_end:
.org 0x3ABE
m68k_003abe:
        rts
m68k_003abe_end:
.org 0x3AC0
m68k_003ac0:
        move.l %a4,%d0
m68k_003ac0_end:
.org 0x3AC2
m68k_003ac2:
        bpl.b (. + 6)
m68k_003ac2_end:
.org 0x3AC4
m68k_003ac4:
        moveq #0,%d7
m68k_003ac4_end:
.org 0x3AC6
m68k_003ac6:
        bra.b (. + 56)
m68k_003ac6_end:
.org 0x3AC8
m68k_003ac8:
        move.l %d5,-(%a7)
m68k_003ac8_end:
.org 0x3ACA
m68k_003aca:
        move.w #0x7,%d0
m68k_003aca_end:
.org 0x3ACE
m68k_003ace:
        lsl.l #0x4,%d7
m68k_003ace_end:
.org 0x3AD0
m68k_003ad0:
        swap %d6
m68k_003ad0_end:
.org 0x3AD2
m68k_003ad2:
        cmp.w %d1,%d6
m68k_003ad2_end:
.org 0x3AD4
m68k_003ad4:
        bcs.b (. + 6)
m68k_003ad4_end:
.org 0x3AD6
m68k_003ad6:
        clr.b %d5
m68k_003ad6_end:
.org 0x3AD8
m68k_003ad8:
        bra.b (. + 28)
m68k_003ad8_end:
.org 0x3ADA
m68k_003ada:
        move.w %d0,-(%a7)
m68k_003ada_end:
.org 0x3ADC
m68k_003adc:
        move.w %d6,%d5
m68k_003adc_end:
.org 0x3ADE
m68k_003ade:
        lsr.w #0x3,%d5
m68k_003ade_end:
.org 0x3AE0
m68k_003ae0:
        move.b (%a4, %d5.w),%d5
m68k_003ae0_end:
.org 0x3AE4
m68k_003ae4:
        move.w %d6,%d0
m68k_003ae4_end:
.org 0x3AE6
m68k_003ae6:
        andi.w #0x7,%d0
m68k_003ae6_end:
.org 0x3AEA
m68k_003aea:
        btst.l %d0,%d5
m68k_003aea_end:
.org 0x3AEC
m68k_003aec:
        beq.b (. + 6)
m68k_003aec_end:
.org 0x3AEE
m68k_003aee:
        ori.w #0xf,%d7
m68k_003aee_end:
.org 0x3AF2
m68k_003af2:
        move.w (%a7)+,%d0
m68k_003af2_end:
.org 0x3AF4
m68k_003af4:
        swap %d6
m68k_003af4_end:
.org 0x3AF6
m68k_003af6:
        add.l %d3,%d6
m68k_003af6_end:
.org 0x3AF8
m68k_003af8:
        dbra %d0,(. + -42)
m68k_003af8_end:
.org 0x3AFC
m68k_003afc:
        move.l (%a7)+,%d5
m68k_003afc_end:
.org 0x3AFE
m68k_003afe:
        move.l %d7,(%a3)
m68k_003afe_end:
.org 0x3B00
m68k_003b00:
        rts
m68k_003b00_end:
.org 0x3B02
m68k_003b02:
        movem.l %d3/%d7/%a2,-(%a7)
m68k_003b02_end:
.org 0x3B06
m68k_003b06:
        lsl.l #0x7,%d3
m68k_003b06_end:
.org 0x3B08
m68k_003b08:
        andi.l #0x3ff80,%d3
m68k_003b08_end:
.org 0x3B0E
m68k_003b0e:
        lsr.w #0x2,%d3
m68k_003b0e_end:
.org 0x3B10
m68k_003b10:
        ori.w #0x4000,%d3
m68k_003b10_end:
.org 0x3B14
m68k_003b14:
        swap %d3
m68k_003b14_end:
.org 0x3B16
m68k_003b16:
        move.l %d3,0xc00004:l
m68k_003b16_end:
.org 0x3B1C
m68k_003b1c:
        move.w #0xff,%d7
m68k_003b1c_end:
.org 0x3B20
m68k_003b20:
        move.w (%a2)+,0xc00000:l
m68k_003b20_end:
.org 0x3B26
m68k_003b26:
        dbra %d7,(. + -6)
m68k_003b26_end:
.org 0x3B2A
m68k_003b2a:
        clr.w 0xd100:w
m68k_003b2a_end:
.org 0x3B2E
m68k_003b2e:
        movem.l (%a7)+,%d3/%d7/%a2
m68k_003b2e_end:
.org 0x3B32
m68k_003b32:
        rts
m68k_003b32_end:
.org 0x3B34
m68k_003b34:
        move.w 0xf316:w,%d0
m68k_003b34_end:
.org 0x3B38
m68k_003b38:
        neg.w %d0
m68k_003b38_end:
.org 0x3B3A
m68k_003b3a:
        move.w %d0,0xf318:w
m68k_003b3a_end:
.org 0x3B3E
m68k_003b3e:
        move.l #0x40000010,0xc00004:l
m68k_003b3e_end:
.org 0x3B48
m68k_003b48:
        move.l 0xf312:w,0xc00000:l
m68k_003b48_end:
.org 0x3B50
m68k_003b50:
        move.l #0x7c000002,0xc00004:l
m68k_003b50_end:
.org 0x3B5A
m68k_003b5a:
        move.l 0xf316:w,0xc00000:l
m68k_003b5a_end:
.org 0x3B62
m68k_003b62:
        rts
m68k_003b62_end:
.org 0x3CA6
m68k_003ca6:
        move.w #0x200,0xf612:w
m68k_003ca6_end:
.org 0x3CAC
m68k_003cac:
        clr.w 0xf352:w
m68k_003cac_end:
.org 0x3CB0
m68k_003cb0:
        move.w #0x160,0xf35e:w
m68k_003cb0_end:
.org 0x3CB6
m68k_003cb6:
        move.w #0x100,0xf360:w
m68k_003cb6_end:
.org 0x3CBC
m68k_003cbc:
        jsr 0x15be:l
m68k_003cbc_end:
.org 0x3CC2
m68k_003cc2:
        move.w #0x1f,%d0
m68k_003cc2_end:
.org 0x3CC6
m68k_003cc6:
        lea.l 0xfb00:w,%a0
m68k_003cc6_end:
.org 0x3CCA
m68k_003cca:
        lea.l 0xfb80:w,%a1
m68k_003cca_end:
.org 0x3CCE
m68k_003cce:
        move.w (%a0)+,(%a1)+
m68k_003cce_end:
.org 0x3CD0
m68k_003cd0:
        dbra %d0,(. + -2)
m68k_003cd0_end:
.org 0x3CD4
m68k_003cd4:
        move.w #0x7f,%d0
m68k_003cd4_end:
.org 0x3CD8
m68k_003cd8:
        lea.l 0xfb00:w,%a0
m68k_003cd8_end:
.org 0x3CDC
m68k_003cdc:
        clr.w (%a0)+
m68k_003cdc_end:
.org 0x3CDE
m68k_003cde:
        dbra %d0,(. + -2)
m68k_003cde_end:
.org 0x3CE2
m68k_003ce2:
        tst.w 0xf776:w
m68k_003ce2_end:
.org 0x3CE6
m68k_003ce6:
        bne.w (. + 14)
m68k_003ce6_end:
.org 0x3CEA
m68k_003cea:
        move.w #0xdc,0xf600:w
m68k_003cea_end:
.org 0x3CF0
m68k_003cf0:
        bra.w (. + 40)
m68k_003cf0_end:
.org 0x3CF4
m68k_003cf4:
        jsr 350(%pc)
m68k_003cf4_end:
.org 0x3CF8
m68k_003cf8:
        nop
m68k_003cf8_end:
.org 0x3CFA
m68k_003cfa:
        jsr 0x8a60:l
m68k_003cfa_end:
.org 0x3D00
m68k_003d00:
        move.w #0xff,0xf376:w
m68k_003d00_end:
.org 0x3D06
m68k_003d06:
        move.w #0xffff,0x9f00:w
m68k_003d06_end:
.org 0x3D0C
m68k_003d0c:
        move.w #0x2,0xf36c:w
m68k_003d0c_end:
.org 0x3D12
m68k_003d12:
        jsr 0x9390:l
m68k_003d12_end:
.org 0x3D18
m68k_003d18:
        move.w #0x85,0xf380:w
m68k_003d18_end:
.org 0x3D1E
m68k_003d1e:
        move.w #0x2700,%sr
m68k_003d1e_end:
.org 0x3D22
m68k_003d22:
        rts
m68k_003d22_end:
.org 0x3E54
m68k_003e54:
        move.w 0xefd4:w,%d0
m68k_003e54_end:
.org 0x3E58
m68k_003e58:
        lsl.w #0x2,%d0
m68k_003e58_end:
.org 0x3E5A
m68k_003e5a:
        movea.l -20(%pc, %d0.w),%a2
m68k_003e5a_end:
.org 0x3E5E
m68k_003e5e:
        movea.l (%a2),%a0
m68k_003e5e_end:
.org 0x3E60
m68k_003e60:
        lea.l 0xf428:w,%a1
m68k_003e60_end:
.org 0x3E64
m68k_003e64:
        bsr.w (. + 450)
m68k_003e64_end:
.org 0x3E68
m68k_003e68:
        movea.l 0x4(%a2),%a0
m68k_003e68_end:
.org 0x3E6C
m68k_003e6c:
        lea.l 0xf460:w,%a1
m68k_003e6c_end:
.org 0x3E70
m68k_003e70:
        bsr.w (. + 498)
m68k_003e70_end:
.org 0x3E74
m68k_003e74:
        movea.l 0x8(%a2),%a0
m68k_003e74_end:
.org 0x3E78
m68k_003e78:
        lea.l 0xe640:w,%a1
m68k_003e78_end:
.org 0x3E7C
m68k_003e7c:
        move.w #0x7,%d0
m68k_003e7c_end:
.org 0x3E80
m68k_003e80:
        move.l (%a0)+,(%a1)+
m68k_003e80_end:
.org 0x3E82
m68k_003e82:
        dbra %d0,(. + -2)
m68k_003e82_end:
.org 0x3E86
m68k_003e86:
        movea.l 0xc(%a2),%a0
m68k_003e86_end:
.org 0x3E8A
m68k_003e8a:
        lea.l 0xe000:w,%a1
m68k_003e8a_end:
.org 0x3E8E
m68k_003e8e:
        bsr.w (. + 420)
m68k_003e8e_end:
.org 0x3E92
m68k_003e92:
        movea.l 0x10(%a2),%a0
m68k_003e92_end:
.org 0x3E96
m68k_003e96:
        lea.l 0xe0a0:w,%a1
m68k_003e96_end:
.org 0x3E9A
m68k_003e9a:
        bsr.w (. + 408)
m68k_003e9a_end:
.org 0x3E9E
m68k_003e9e:
        movea.l 0x14(%a2),%a0
m68k_003e9e_end:
.org 0x3EA2
m68k_003ea2:
        lea.l 0xe140:w,%a1
m68k_003ea2_end:
.org 0x3EA6
m68k_003ea6:
        bsr.w (. + 396)
m68k_003ea6_end:
.org 0x3EAA
m68k_003eaa:
        movea.l 0x18(%a2),%a0
m68k_003eaa_end:
.org 0x3EAE
m68k_003eae:
        lea.l 0xe1e0:w,%a1
m68k_003eae_end:
.org 0x3EB2
m68k_003eb2:
        bsr.w (. + 384)
m68k_003eb2_end:
.org 0x3EB6
m68k_003eb6:
        movea.l 0x1c(%a2),%a0
m68k_003eb6_end:
.org 0x3EBA
m68k_003eba:
        lea.l 0xe280:w,%a1
m68k_003eba_end:
.org 0x3EBE
m68k_003ebe:
        bsr.w (. + 372)
m68k_003ebe_end:
.org 0x3EC2
m68k_003ec2:
        movea.l 0x20(%a2),%a0
m68k_003ec2_end:
.org 0x3EC6
m68k_003ec6:
        lea.l 0xe320:w,%a1
m68k_003ec6_end:
.org 0x3ECA
m68k_003eca:
        bsr.w (. + 360)
m68k_003eca_end:
.org 0x3ECE
m68k_003ece:
        movea.l 0x24(%a2),%a0
m68k_003ece_end:
.org 0x3ED2
m68k_003ed2:
        lea.l 0xe3c0:w,%a1
m68k_003ed2_end:
.org 0x3ED6
m68k_003ed6:
        bsr.w (. + 348)
m68k_003ed6_end:
.org 0x3EDA
m68k_003eda:
        movea.l 0x28(%a2),%a0
m68k_003eda_end:
.org 0x3EDE
m68k_003ede:
        lea.l 0xe460:w,%a1
m68k_003ede_end:
.org 0x3EE2
m68k_003ee2:
        bsr.w (. + 336)
m68k_003ee2_end:
.org 0x3EE6
m68k_003ee6:
        movea.l 0x2c(%a2),%a0
m68k_003ee6_end:
.org 0x3EEA
m68k_003eea:
        lea.l 0xe500:w,%a1
m68k_003eea_end:
.org 0x3EEE
m68k_003eee:
        bsr.w (. + 324)
m68k_003eee_end:
.org 0x3EF2
m68k_003ef2:
        movea.l 0x30(%a2),%a0
m68k_003ef2_end:
.org 0x3EF6
m68k_003ef6:
        lea.l 0xe5a0:w,%a1
m68k_003ef6_end:
.org 0x3EFA
m68k_003efa:
        bsr.w (. + 312)
m68k_003efa_end:
.org 0x3EFE
m68k_003efe:
        movea.l 0x34(%a2),%a0
m68k_003efe_end:
.org 0x3F02
m68k_003f02:
        lea.l 0xb000:w,%a1
m68k_003f02_end:
.org 0x3F06
m68k_003f06:
        bsr.w (. + 312)
m68k_003f06_end:
.org 0x3F0A
m68k_003f0a:
        movea.l 0x38(%a2),%a0
m68k_003f0a_end:
.org 0x3F0E
m68k_003f0e:
        lea.l 0xb200:w,%a1
m68k_003f0e_end:
.org 0x3F12
m68k_003f12:
        bsr.w (. + 300)
m68k_003f12_end:
.org 0x3F16
m68k_003f16:
        movea.l 0x3c(%a2),%a0
m68k_003f16_end:
.org 0x3F1A
m68k_003f1a:
        lea.l 0xb400:w,%a1
m68k_003f1a_end:
.org 0x3F1E
m68k_003f1e:
        bsr.w (. + 288)
m68k_003f1e_end:
.org 0x3F22
m68k_003f22:
        movea.l 0x40(%a2),%a0
m68k_003f22_end:
.org 0x3F26
m68k_003f26:
        lea.l 0xb600:w,%a1
m68k_003f26_end:
.org 0x3F2A
m68k_003f2a:
        bsr.w (. + 276)
m68k_003f2a_end:
.org 0x3F2E
m68k_003f2e:
        movea.l 0x44(%a2),%a0
m68k_003f2e_end:
.org 0x3F32
m68k_003f32:
        lea.l 0xb800:w,%a1
m68k_003f32_end:
.org 0x3F36
m68k_003f36:
        bsr.w (. + 264)
m68k_003f36_end:
.org 0x3F3A
m68k_003f3a:
        movea.l 0x48(%a2),%a0
m68k_003f3a_end:
.org 0x3F3E
m68k_003f3e:
        lea.l 0xba00:w,%a1
m68k_003f3e_end:
.org 0x3F42
m68k_003f42:
        bsr.w (. + 252)
m68k_003f42_end:
.org 0x3F46
m68k_003f46:
        movea.l 0x4c(%a2),%a0
m68k_003f46_end:
.org 0x3F4A
m68k_003f4a:
        lea.l 0xbc00:w,%a1
m68k_003f4a_end:
.org 0x3F4E
m68k_003f4e:
        bsr.w (. + 240)
m68k_003f4e_end:
.org 0x3F52
m68k_003f52:
        movea.l 0x50(%a2),%a0
m68k_003f52_end:
.org 0x3F56
m68k_003f56:
        lea.l 0xbe00:w,%a1
m68k_003f56_end:
.org 0x3F5A
m68k_003f5a:
        bsr.w (. + 228)
m68k_003f5a_end:
.org 0x3F5E
m68k_003f5e:
        movea.l 0x54(%a2),%a0
m68k_003f5e_end:
.org 0x3F62
m68k_003f62:
        lea.l 0xc000:w,%a1
m68k_003f62_end:
.org 0x3F66
m68k_003f66:
        bsr.w (. + 216)
m68k_003f66_end:
.org 0x3F6A
m68k_003f6a:
        movea.l 0x58(%a2),%a0
m68k_003f6a_end:
.org 0x3F6E
m68k_003f6e:
        lea.l 0xc200:w,%a1
m68k_003f6e_end:
.org 0x3F72
m68k_003f72:
        bsr.w (. + 216)
m68k_003f72_end:
.org 0x3F76
m68k_003f76:
        movea.l 0x5c(%a2),%a0
m68k_003f76_end:
.org 0x3F7A
m68k_003f7a:
        lea.l 0xc300:w,%a1
m68k_003f7a_end:
.org 0x3F7E
m68k_003f7e:
        bsr.w (. + 204)
m68k_003f7e_end:
.org 0x3F82
m68k_003f82:
        movea.l 0x60(%a2),%a0
m68k_003f82_end:
.org 0x3F86
m68k_003f86:
        lea.l 0xc400:w,%a1
m68k_003f86_end:
.org 0x3F8A
m68k_003f8a:
        bsr.w (. + 192)
m68k_003f8a_end:
.org 0x3F8E
m68k_003f8e:
        movea.l 0x64(%a2),%a0
m68k_003f8e_end:
.org 0x3F92
m68k_003f92:
        lea.l 0xc500:w,%a1
m68k_003f92_end:
.org 0x3F96
m68k_003f96:
        bsr.w (. + 180)
m68k_003f96_end:
.org 0x3F9A
m68k_003f9a:
        movea.l 0x68(%a2),%a0
m68k_003f9a_end:
.org 0x3F9E
m68k_003f9e:
        lea.l 0xc600:w,%a1
m68k_003f9e_end:
.org 0x3FA2
m68k_003fa2:
        bsr.w (. + 168)
m68k_003fa2_end:
.org 0x3FA6
m68k_003fa6:
        movea.l 0x6c(%a2),%a0
m68k_003fa6_end:
.org 0x3FAA
m68k_003faa:
        lea.l 0xc700:w,%a1
m68k_003faa_end:
.org 0x3FAE
m68k_003fae:
        bsr.w (. + 156)
m68k_003fae_end:
.org 0x3FB2
m68k_003fb2:
        movea.l 0x70(%a2),%a0
m68k_003fb2_end:
.org 0x3FB6
m68k_003fb6:
        lea.l 0xc800:w,%a1
m68k_003fb6_end:
.org 0x3FBA
m68k_003fba:
        bsr.w (. + 156)
m68k_003fba_end:
.org 0x3FBE
m68k_003fbe:
        movea.l 0x74(%a2),%a0
m68k_003fbe_end:
.org 0x3FC2
m68k_003fc2:
        lea.l 0xcc00:w,%a1
m68k_003fc2_end:
.org 0x3FC6
m68k_003fc6:
        bsr.w (. + 132)
m68k_003fc6_end:
.org 0x3FCA
m68k_003fca:
        movea.l 0x78(%a2),%a0
m68k_003fca_end:
.org 0x3FCE
m68k_003fce:
        lea.l 0xe710:w,%a1
m68k_003fce_end:
.org 0x3FD2
m68k_003fd2:
        bsr.w (. + 156)
m68k_003fd2_end:
.org 0x3FD6
m68k_003fd6:
        clr.w 0xe700:w
m68k_003fd6_end:
.org 0x3FDA
m68k_003fda:
        lea.l 0xe818:w,%a0
m68k_003fda_end:
.org 0x3FDE
m68k_003fde:
        move.w #0x77,%d0
m68k_003fde_end:
.org 0x3FE2
m68k_003fe2:
        move.l #0xffffffff,(%a0)+
m68k_003fe2_end:
.org 0x3FE8
m68k_003fe8:
        dbra %d0,(. + -6)
m68k_003fe8_end:
.org 0x3FEC
m68k_003fec:
        movea.l 0x7c(%a2),%a0
m68k_003fec_end:
.org 0x3FF0
m68k_003ff0:
        lea.l 0xea88:w,%a1
m68k_003ff0_end:
.org 0x3FF4
m68k_003ff4:
        bsr.w (. + 134)
m68k_003ff4_end:
.org 0x3FF8
m68k_003ff8:
        movea.l 0x80(%a2),%a0
m68k_003ff8_end:
.org 0x3FFC
m68k_003ffc:
        lea.l 0xf000:w,%a1
m68k_003ffc_end:
.org 0x4000
m68k_004000:
        bsr.w (. + 150)
m68k_004000_end:
.org 0x4004
m68k_004004:
        move.w #0xff,0xf376:w
m68k_004004_end:
.org 0x400A
m68k_00400a:
        move.w #0x0,0xefd4:w
m68k_00400a_end:
.org 0x4010
m68k_004010:
        move.w #0xffff,0x9f00:w
m68k_004010_end:
.org 0x4016
m68k_004016:
        move.w #0xff,%d0
m68k_004016_end:
.org 0x401A
m68k_00401a:
        lea.l 0xa150:w,%a0
m68k_00401a_end:
.org 0x401E
m68k_00401e:
        clr.l (%a0)+
m68k_00401e_end:
.org 0x4020
m68k_004020:
        dbra %d0,(. + -2)
m68k_004020_end:
.org 0x4024
m68k_004024:
        rts
m68k_004024_end:
.org 0x4026
m68k_004026:
        move.w #0x9,%d0
m68k_004026_end:
.org 0x402A
m68k_00402a:
        move.l (%a0)+,(%a1)+
m68k_00402a_end:
.org 0x402C
m68k_00402c:
        dbra %d0,(. + -2)
m68k_00402c_end:
.org 0x4030
m68k_004030:
        rts
m68k_004030_end:
.org 0x4032
m68k_004032:
        move.w #0x27,%d0
m68k_004032_end:
.org 0x4036
m68k_004036:
        move.l (%a0)+,(%a1)+
m68k_004036_end:
.org 0x4038
m68k_004038:
        dbra %d0,(. + -2)
m68k_004038_end:
.org 0x403C
m68k_00403c:
        rts
m68k_00403c_end:
.org 0x403E
m68k_00403e:
        move.w #0x7f,%d0
m68k_00403e_end:
.org 0x4042
m68k_004042:
        move.l (%a0)+,(%a1)+
m68k_004042_end:
.org 0x4044
m68k_004044:
        dbra %d0,(. + -2)
m68k_004044_end:
.org 0x4048
m68k_004048:
        rts
m68k_004048_end:
.org 0x404A
m68k_00404a:
        move.w #0x3f,%d0
m68k_00404a_end:
.org 0x404E
m68k_00404e:
        move.l (%a0)+,(%a1)+
m68k_00404e_end:
.org 0x4050
m68k_004050:
        dbra %d0,(. + -2)
m68k_004050_end:
.org 0x4054
m68k_004054:
        rts
m68k_004054_end:
.org 0x4056
m68k_004056:
        move.w #0xff,%d0
m68k_004056_end:
.org 0x405A
m68k_00405a:
        move.l (%a0)+,(%a1)+
m68k_00405a_end:
.org 0x405C
m68k_00405c:
        dbra %d0,(. + -2)
m68k_00405c_end:
.org 0x4060
m68k_004060:
        rts
m68k_004060_end:
.org 0x4062
m68k_004062:
        move.w #0x13,%d0
m68k_004062_end:
.org 0x4066
m68k_004066:
        move.l (%a0)+,(%a1)+
m68k_004066_end:
.org 0x4068
m68k_004068:
        dbra %d0,(. + -2)
m68k_004068_end:
.org 0x406C
m68k_00406c:
        rts
m68k_00406c_end:
.org 0x406E
m68k_00406e:
        move.w #0x7,%d0
m68k_00406e_end:
.org 0x4072
m68k_004072:
        move.l (%a0)+,(%a1)+
m68k_004072_end:
.org 0x4074
m68k_004074:
        dbra %d0,(. + -2)
m68k_004074_end:
.org 0x4078
m68k_004078:
        rts
m68k_004078_end:
.org 0x407A
m68k_00407a:
        move.w #0xff,%d0
m68k_00407a_end:
.org 0x407E
m68k_00407e:
        move.b 0x1(%a0),(%a1)
m68k_00407e_end:
.org 0x4082
m68k_004082:
        move.b (%a0),0x1(%a1)
m68k_004082_end:
.org 0x4086
m68k_004086:
        move.b 0x2(%a0),0x2(%a1)
m68k_004086_end:
.org 0x408C
m68k_00408c:
        addq.w #0x3,%a0
m68k_00408c_end:
.org 0x408E
m68k_00408e:
        addq.w #0x3,%a1
m68k_00408e_end:
.org 0x4090
m68k_004090:
        dbra %d0,(. + -18)
m68k_004090_end:
.org 0x4094
m68k_004094:
        rts
m68k_004094_end:
.org 0x4096
m68k_004096:
        move.w #0xff,%d0
m68k_004096_end:
.org 0x409A
m68k_00409a:
        move.w (%a0)+,%d1
m68k_00409a_end:
.org 0x409C
m68k_00409c:
        cmpi.w #0xffff,%d1
m68k_00409c_end:
.org 0x40A0
m68k_0040a0:
        beq.w (. + 8)
m68k_0040a0_end:
.org 0x40A4
m68k_0040a4:
        subi.w #0xb8,%d1
m68k_0040a4_end:
.org 0x40A8
m68k_0040a8:
        move.b %d1,(%a1)+
m68k_0040a8_end:
.org 0x40AA
m68k_0040aa:
        dbra %d0,(. + -16)
m68k_0040aa_end:
.org 0x40AE
m68k_0040ae:
        rts
m68k_0040ae_end:
.org 0x40B0
m68k_0040b0:
        move.w #0x60,%d0
m68k_0040b0_end:
.org 0x40B4
m68k_0040b4:
        dbra %d0,(. + 0)
m68k_0040b4_end:
.org 0x40B8
m68k_0040b8:
        jsr 0x4890:l
m68k_0040b8_end:
.org 0x40BE
m68k_0040be:
        lea.l 0xc00004:l,%a6
m68k_0040be_end:
.org 0x40C4
m68k_0040c4:
        move.w 0xf606:w,%d7
m68k_0040c4_end:
.org 0x40C8
m68k_0040c8:
        ori.b #0x10,%d7
m68k_0040c8_end:
.org 0x40CC
m68k_0040cc:
        move.w %d7,(%a6)
m68k_0040cc_end:
.org 0x40CE
m68k_0040ce:
        move.w #0x100,0xa11100:l
m68k_0040ce_end:
.org 0x40D6
m68k_0040d6:
        move.l #0x94009340,(%a6)
m68k_0040d6_end:
.org 0x40DC
m68k_0040dc:
        move.l #0x96fd9580,(%a6)
m68k_0040dc_end:
.org 0x40E2
m68k_0040e2:
        move.w #0x977f,(%a6)
m68k_0040e2_end:
.org 0x40E6
m68k_0040e6:
        move.w #0xc000,(%a6)
m68k_0040e6_end:
.org 0x40EA
m68k_0040ea:
        move.w #0x80,0xf620:w
m68k_0040ea_end:
.org 0x40F0
m68k_0040f0:
        move.w 0xf620:w,(%a6)
m68k_0040f0_end:
.org 0x40F4
m68k_0040f4:
        tst.b 0xffff3f00:l
m68k_0040f4_end:
.org 0x40FA
m68k_0040fa:
        bne.b (. + 10)
m68k_0040fa_end:
.org 0x40FC
m68k_0040fc:
        move.w #0x0,0xa11100:l
m68k_0040fc_end:
.org 0x4104
m68k_004104:
        move.w 0xf606:w,(%a6)
m68k_004104_end:
.org 0x4108
m68k_004108:
        bsr.w (. + -1492)
m68k_004108_end:
.org 0x410C
m68k_00410c:
        move.w 0xf606:w,%d0
m68k_00410c_end:
.org 0x4110
m68k_004110:
        ori.b #0x40,%d0
m68k_004110_end:
.org 0x4114
m68k_004114:
        move.w %d0,0xc00004:l
m68k_004114_end:
.org 0x411A
m68k_00411a:
        move.b 0xf603:w,%d0
m68k_00411a_end:
.org 0x411E
m68k_00411e:
        andi.w #0xf0,%d0
m68k_00411e_end:
.org 0x4122
m68k_004122:
        beq.w (. + 56)
m68k_004122_end:
.org 0x415A
m68k_00415a:
        move.w 0xf612:w,%d0
m68k_00415a_end:
.org 0x415E
m68k_00415e:
        andi.w #0xff,%d0
m68k_00415e_end:
.org 0x4162
m68k_004162:
        lsl.w #0x1,%d0
m68k_004162_end:
.org 0x4164
m68k_004164:
        move.w 8(%pc, %d0.w),%d0
m68k_004164_end:
.org 0x4168
m68k_004168:
        jsr 14(%pc, %d0.w)
m68k_004168_end:
.org 0x416C
m68k_00416c:
        rts
m68k_00416c_end:
.org 0x4178
m68k_004178:
        jsr 0x3a978:l
m68k_004178_end:
.org 0x417E
m68k_00417e:
        cmpi.w #0xa00,0xf32e:w
m68k_00417e_end:
.org 0x4184
m68k_004184:
        bcc.b (. + 10)
m68k_004184_end:
.org 0x4186
m68k_004186:
        addq.w #0x1,0xf32e:w
m68k_004186_end:
.org 0x418A
m68k_00418a:
        addq.w #0x1,0x8430:w
m68k_00418a_end:
.org 0x418E
m68k_00418e:
        tst.b 0xf32b:w
m68k_00418e_end:
.org 0x4192
m68k_004192:
        bne.w (. + 472)
m68k_004192_end:
.org 0x4196
m68k_004196:
        cmpi.w #0x340,0xf32e:w
m68k_004196_end:
.org 0x419C
m68k_00419c:
        bcc.w (. + 44)
m68k_00419c_end:
.org 0x41A0
m68k_0041a0:
        move.b 0xf603:w,%d0
m68k_0041a0_end:
.org 0x41A4
m68k_0041a4:
        andi.b #0x80,%d0
m68k_0041a4_end:
.org 0x41A8
m68k_0041a8:
        beq.w (. + 32)
m68k_0041a8_end:
.org 0x41C8
m68k_0041c8:
        tst.w 0x842e:w
m68k_0041c8_end:
.org 0x41CC
m68k_0041cc:
        bne.w (. + 78)
m68k_0041cc_end:
.org 0x41D0
m68k_0041d0:
        cmpi.w #0x500,0x8430:w
m68k_0041d0_end:
.org 0x41D6
m68k_0041d6:
        bne.w (. + 36)
m68k_0041d6_end:
.org 0x41FA
m68k_0041fa:
        cmpi.w #0x500,0x8430:w
m68k_0041fa_end:
.org 0x4200
m68k_004200:
        bcs.w (. + 26)
m68k_004200_end:
.org 0x421A
m68k_00421a:
        cmpi.w #0x300,0xf32e:w
m68k_00421a_end:
.org 0x4220
m68k_004220:
        bcc.w (. + 102)
m68k_004220_end:
.org 0x4224
m68k_004224:
        cmpi.w #0x280,0xf32e:w
m68k_004224_end:
.org 0x422A
m68k_00422a:
        bcc.w (. + 6)
m68k_00422a_end:
.org 0x422E
m68k_00422e:
        rts
m68k_00422e_end:
.org 0x4344
m68k_004344:
        tst.w 0x842e:w
m68k_004344_end:
.org 0x4348
m68k_004348:
        beq.b (. + 16)
m68k_004348_end:
.org 0x434A
m68k_00434a:
        bsr.w (. + 620)
m68k_00434a_end:
.org 0x434E
m68k_00434e:
        bsr.w (. + 178)
m68k_00434e_end:
.org 0x4352
m68k_004352:
        bsr.w (. + 206)
m68k_004352_end:
.org 0x4356
m68k_004356:
        bra.b (. + 18)
m68k_004356_end:
.org 0x4358
m68k_004358:
        bsr.w (. + 606)
m68k_004358_end:
.org 0x435C
m68k_00435c:
        bsr.w (. + 230)
m68k_00435c_end:
.org 0x4360
m68k_004360:
        bra.b (. + 8)
m68k_004360_end:
.org 0x4362
m68k_004362:
        move.l #0x0,(%a1)
m68k_004362_end:
.org 0x4368
m68k_004368:
        rts
m68k_004368_end:
.org 0x436A
m68k_00436a:
        btst.b #0x7,0x80c4:w
m68k_00436a_end:
.org 0x4370
m68k_004370:
        bne.w (. + -1738)
m68k_004370_end:
.org 0x4374
m68k_004374:
        bra.w (. + -478)
m68k_004374_end:
.org 0x4400
m68k_004400:
        lea.l 214(%pc),%a0
m68k_004400_end:
.org 0x4404
m68k_004404:
        nop
m68k_004404_end:
.org 0x4406
m68k_004406:
        move.w %d4,%d0
m68k_004406_end:
.org 0x4408
m68k_004408:
        andi.w #0xff,%d0
m68k_004408_end:
.org 0x440C
m68k_00440c:
        move.w #0xc,%d7
m68k_00440c_end:
.org 0x4410
m68k_004410:
        move.w (%a0)+,(%a1)+
m68k_004410_end:
.org 0x4412
m68k_004412:
        move.w %d0,(%a1)+
m68k_004412_end:
.org 0x4414
m68k_004414:
        move.w (%a0)+,(%a1)+
m68k_004414_end:
.org 0x4416
m68k_004416:
        move.w (%a0)+,(%a1)+
m68k_004416_end:
.org 0x4418
m68k_004418:
        addq.w #0x1,%d0
m68k_004418_end:
.org 0x441A
m68k_00441a:
        dbra %d7,(. + -10)
m68k_00441a_end:
.org 0x441E
m68k_00441e:
        rts
m68k_00441e_end:
.org 0x4420
m68k_004420:
        move.w #0x110,(%a1)
m68k_004420_end:
.org 0x4424
m68k_004424:
        tst.w 0x842a:w
m68k_004424_end:
.org 0x4428
m68k_004428:
        beq.b (. + 6)
m68k_004428_end:
.org 0x442A
m68k_00442a:
        move.w #0x120,(%a1)
m68k_00442a_end:
.org 0x442E
m68k_00442e:
        move.w #0x0,0x2(%a1)
m68k_00442e_end:
.org 0x4434
m68k_004434:
        move.w #0x6024,0x4(%a1)
m68k_004434_end:
.org 0x443A
m68k_00443a:
        move.w #0xf0,0x6(%a1)
m68k_00443a_end:
.org 0x4440
m68k_004440:
        rts
m68k_004440_end:
.org 0x45B6
m68k_0045b6:
        btst.b #0x7,0x80c4:w
m68k_0045b6_end:
.org 0x45BC
m68k_0045bc:
        beq.w (. + 150)
m68k_0045bc_end:
.org 0x45C0
m68k_0045c0:
        tst.w 0x842e:w
m68k_0045c0_end:
.org 0x45C4
m68k_0045c4:
        beq.b (. + 114)
m68k_0045c4_end:
.org 0x45C6
m68k_0045c6:
        jsr 0x90d8:l
m68k_0045c6_end:
.org 0x45CC
m68k_0045cc:
        bcs.w (. + 36)
m68k_0045cc_end:
.org 0x45D0
m68k_0045d0:
        btst.b #0x0,0xf603:w
m68k_0045d0_end:
.org 0x45D6
m68k_0045d6:
        bne.w (. + 14)
m68k_0045d6_end:
.org 0x45DA
m68k_0045da:
        btst.b #0x1,0xf603:w
m68k_0045da_end:
.org 0x45E0
m68k_0045e0:
        beq.w (. + 16)
m68k_0045e0_end:
.org 0x45E4
m68k_0045e4:
        eori.w #0x1,0x842a:w
m68k_0045e4_end:
.org 0x45EA
m68k_0045ea:
        andi.w #0x1,0x842a:w
m68k_0045ea_end:
.org 0x45F0
m68k_0045f0:
        clr.w 0xf776:w
m68k_0045f0_end:
.org 0x45F4
m68k_0045f4:
        tst.w 0x842a:w
m68k_0045f4_end:
.org 0x45F8
m68k_0045f8:
        beq.w (. + 10)
m68k_0045f8_end:
.org 0x45FC
m68k_0045fc:
        move.w #0x1,0xf776:w
m68k_0045fc_end:
.org 0x4602
m68k_004602:
        move.b 0xf603:w,%d0
m68k_004602_end:
.org 0x4606
m68k_004606:
        andi.b #0x80,%d0
m68k_004606_end:
.org 0x460A
m68k_00460a:
        beq.w (. + 72)
m68k_00460a_end:
.org 0x460E
m68k_00460e:
        move.b #0x1,0xf32b:w
m68k_00460e_end:
.org 0x4614
m68k_004614:
        move.w #0xffff,0x80ca:w
m68k_004614_end:
.org 0x461A
m68k_00461a:
        move.w #0xffff,0x80cc:w
m68k_00461a_end:
.org 0x4620
m68k_004620:
        move.w #0xffff,0x80ce:w
m68k_004620_end:
.org 0x4626
m68k_004626:
        move.w #0xffff,0x80d0:w
m68k_004626_end:
.org 0x462C
m68k_00462c:
        moveq #1,%d0
m68k_00462c_end:
.org 0x462E
m68k_00462e:
        jsr 0x3aa38:l
m68k_00462e_end:
.org 0x4634
m68k_004634:
        rts
m68k_004634_end:
.org 0x4636
m68k_004636:
        move.b 0xf603:w,%d0
m68k_004636_end:
.org 0x463A
m68k_00463a:
        andi.b #0x80,%d0
m68k_00463a_end:
.org 0x463E
m68k_00463e:
        beq.w (. + 20)
m68k_00463e_end:
.org 0x4642
m68k_004642:
        move.w #0x1,0x842e:w
m68k_004642_end:
.org 0x4648
m68k_004648:
        move.b #0xac,%d0
m68k_004648_end:
.org 0x464C
m68k_00464c:
        jsr 0x808a:l
m68k_00464c_end:
.org 0x4652
m68k_004652:
        rts
m68k_004652_end:
.org 0x481E
m68k_00481e:
        movem.l %d0-%d7/%a0-%a6,-(%a7)
m68k_00481e_end:
.org 0x4822
m68k_004822:
        tst.b 0xf612:w
m68k_004822_end:
.org 0x4826
m68k_004826:
        beq.b (. + 38)
m68k_004826_end:
.org 0x4828
m68k_004828:
        move.w 0xc00004:l,%d0
m68k_004828_end:
.org 0x482E
m68k_00482e:
        move.w 0xc00004:l,%d0
m68k_00482e_end:
.org 0x4834
m68k_004834:
        btst.l #0x3,%d0
m68k_004834_end:
.org 0x4838
m68k_004838:
        beq.b (. + 20)
m68k_004838_end:
.org 0x483A
m68k_00483a:
        move.w 0xf612:w,%d0
m68k_00483a_end:
.org 0x483E
m68k_00483e:
        lsr.w #0x6,%d0
m68k_00483e_end:
.org 0x4840
m68k_004840:
        andi.w #0xfffc,%d0
m68k_004840_end:
.org 0x4844
m68k_004844:
        jsr 14(%pc, %d0.w)
m68k_004844_end:
.org 0x4848
m68k_004848:
        addq.w #0x1,0xf320:w
m68k_004848_end:
.org 0x484C
m68k_00484c:
        jsr 0x83d4:l
m68k_00484c_end:
.org 0x4852
m68k_004852:
        movem.l (%a7)+,%d0-%d7/%a0-%a6
m68k_004852_end:
.org 0x4856
m68k_004856:
        rte
m68k_004856_end:
.org 0x4858
m68k_004858:
        bra.w (. + 382)
m68k_004858_end:
.org 0x485C
m68k_00485c:
        bra.w (. + -14668)
m68k_00485c_end:
.org 0x4860
m68k_004860:
        bra.w (. + -1968)
m68k_004860_end:
.org 0x486C
m68k_00486c:
        bra.w (. + 378)
m68k_00486c_end:
.org 0x4878
m68k_004878:
        bra.w (. + 444)
m68k_004878_end:
.org 0x4890
m68k_004890:
        jsr 0x67ca:l
m68k_004890_end:
.org 0x4896
m68k_004896:
        lea.l 0xc00004:l,%a6
m68k_004896_end:
.org 0x489C
m68k_00489c:
        move.w 0xf606:w,%d7
m68k_00489c_end:
.org 0x48A0
m68k_0048a0:
        ori.b #0x10,%d7
m68k_0048a0_end:
.org 0x48A4
m68k_0048a4:
        move.w %d7,(%a6)
m68k_0048a4_end:
.org 0x48A6
m68k_0048a6:
        move.w #0x100,0xa11100:l
m68k_0048a6_end:
.org 0x48AE
m68k_0048ae:
        move.l #0x94019340,(%a6)
m68k_0048ae_end:
.org 0x48B4
m68k_0048b4:
        move.l #0x96fc9500,(%a6)
m68k_0048b4_end:
.org 0x48BA
m68k_0048ba:
        move.w #0x977f,(%a6)
m68k_0048ba_end:
.org 0x48BE
m68k_0048be:
        move.w #0x7800,(%a6)
m68k_0048be_end:
.org 0x48C2
m68k_0048c2:
        move.w #0x82,0xf620:w
m68k_0048c2_end:
.org 0x48C8
m68k_0048c8:
        move.w 0xf620:w,(%a6)
m68k_0048c8_end:
.org 0x48CC
m68k_0048cc:
        tst.b 0xff3f00:l
m68k_0048cc_end:
.org 0x48D2
m68k_0048d2:
        bne.b (. + 10)
m68k_0048d2_end:
.org 0x48D4
m68k_0048d4:
        move.w #0x0,0xa11100:l
m68k_0048d4_end:
.org 0x48DC
m68k_0048dc:
        move.w 0xf606:w,(%a6)
m68k_0048dc_end:
.org 0x48E0
m68k_0048e0:
        tst.w 0xf31e:w
m68k_0048e0_end:
.org 0x48E4
m68k_0048e4:
        beq.w (. + 82)
m68k_0048e4_end:
.org 0x48E8
m68k_0048e8:
        lea.l 0xc00004:l,%a6
m68k_0048e8_end:
.org 0x48EE
m68k_0048ee:
        move.w 0xf606:w,%d7
m68k_0048ee_end:
.org 0x48F2
m68k_0048f2:
        ori.b #0x10,%d7
m68k_0048f2_end:
.org 0x48F6
m68k_0048f6:
        move.w %d7,(%a6)
m68k_0048f6_end:
.org 0x48F8
m68k_0048f8:
        move.w #0x100,0xa11100:l
m68k_0048f8_end:
.org 0x4900
m68k_004900:
        move.l #0x94009340,(%a6)
m68k_004900_end:
.org 0x4906
m68k_004906:
        move.l #0x96fd9580,(%a6)
m68k_004906_end:
.org 0x490C
m68k_00490c:
        move.w #0x977f,(%a6)
m68k_00490c_end:
.org 0x4910
m68k_004910:
        move.w #0xc000,(%a6)
m68k_004910_end:
.org 0x4914
m68k_004914:
        move.w #0x80,0xf620:w
m68k_004914_end:
.org 0x491A
m68k_00491a:
        move.w 0xf620:w,(%a6)
m68k_00491a_end:
.org 0x491E
m68k_00491e:
        tst.b 0xff3f00:l
m68k_00491e_end:
.org 0x4924
m68k_004924:
        bne.b (. + 10)
m68k_004924_end:
.org 0x4926
m68k_004926:
        move.w #0x0,0xa11100:l
m68k_004926_end:
.org 0x492E
m68k_00492e:
        move.w 0xf606:w,(%a6)
m68k_00492e_end:
.org 0x4932
m68k_004932:
        clr.w 0xf31e:w
m68k_004932_end:
.org 0x4936
m68k_004936:
        bsr.w (. + 224)
m68k_004936_end:
.org 0x493A
m68k_00493a:
        jsr 0xad06:l
m68k_00493a_end:
.org 0x4940
m68k_004940:
        rts
m68k_004940_end:
.org 0x4942
m68k_004942:
        lea.l 0xc00004:l,%a6
m68k_004942_end:
.org 0x4948
m68k_004948:
        move.w 0xf606:w,%d7
m68k_004948_end:
.org 0x494C
m68k_00494c:
        ori.b #0x10,%d7
m68k_00494c_end:
.org 0x4950
m68k_004950:
        move.w %d7,(%a6)
m68k_004950_end:
.org 0x4952
m68k_004952:
        move.w #0x100,0xa11100:l
m68k_004952_end:
.org 0x495A
m68k_00495a:
        move.l #0x94019340,(%a6)
m68k_00495a_end:
.org 0x4960
m68k_004960:
        move.l #0x96fc9500,(%a6)
m68k_004960_end:
.org 0x4966
m68k_004966:
        move.w #0x977f,(%a6)
m68k_004966_end:
.org 0x496A
m68k_00496a:
        move.w #0x7800,(%a6)
m68k_00496a_end:
.org 0x496E
m68k_00496e:
        move.w #0x82,0xf620:w
m68k_00496e_end:
.org 0x4974
m68k_004974:
        move.w 0xf620:w,(%a6)
m68k_004974_end:
.org 0x4978
m68k_004978:
        tst.b 0xff3f00:l
m68k_004978_end:
.org 0x497E
m68k_00497e:
        bne.b (. + 10)
m68k_00497e_end:
.org 0x4980
m68k_004980:
        move.w #0x0,0xa11100:l
m68k_004980_end:
.org 0x4988
m68k_004988:
        move.w 0xf606:w,(%a6)
m68k_004988_end:
.org 0x498C
m68k_00498c:
        bsr.w (. + 138)
m68k_00498c_end:
.org 0x4990
m68k_004990:
        jsr 0xad06:l
m68k_004990_end:
.org 0x4996
m68k_004996:
        rts
m68k_004996_end:
.org 0x4998
m68k_004998:
        move.l #0x7c000002,0xc00004:l
m68k_004998_end:
.org 0x49A2
m68k_0049a2:
        move.w 0xf316:w,%d0
m68k_0049a2_end:
.org 0x49A6
m68k_0049a6:
        neg.w %d0
m68k_0049a6_end:
.org 0x49A8
m68k_0049a8:
        move.w %d0,0xc00000:l
m68k_0049a8_end:
.org 0x49AE
m68k_0049ae:
        move.w 0xf318:w,%d0
m68k_0049ae_end:
.org 0x49B2
m68k_0049b2:
        neg.w %d0
m68k_0049b2_end:
.org 0x49B4
m68k_0049b4:
        move.w %d0,0xc00000:l
m68k_0049b4_end:
.org 0x49BA
m68k_0049ba:
        move.l #0x40000010,0xc00004:l
m68k_0049ba_end:
.org 0x49C4
m68k_0049c4:
        move.w 0xf312:w,0xc00000:l
m68k_0049c4_end:
.org 0x49CC
m68k_0049cc:
        move.w 0xf314:w,0xc00000:l
m68k_0049cc_end:
.org 0x49D4
m68k_0049d4:
        rts
m68k_0049d4_end:
.org 0x49D6
m68k_0049d6:
        jsr 0x9508:l
m68k_0049d6_end:
.org 0x49DC
m68k_0049dc:
        rts
m68k_0049dc_end:
.org 0x49E6
m68k_0049e6:
        jsr 0x3a536:l
m68k_0049e6_end:
.org 0x49EC
m68k_0049ec:
        jsr 0xa3da:l
m68k_0049ec_end:
.org 0x49F2
m68k_0049f2:
        rts
m68k_0049f2_end:
.org 0x4A16
m68k_004a16:
        clr.w 0xf300:w
m68k_004a16_end:
.org 0x4A1A
m68k_004a1a:
        clr.w 0xf800:w
m68k_004a1a_end:
.org 0x4A1E
m68k_004a1e:
        clr.w 0xf802:w
m68k_004a1e_end:
.org 0x4A22
m68k_004a22:
        clr.w 0xf806:w
m68k_004a22_end:
.org 0x4A26
m68k_004a26:
        nop
m68k_004a26_end:
.org 0x4A28
m68k_004a28:
        nop
m68k_004a28_end:
.org 0x4A2A
m68k_004a2a:
        rts
m68k_004a2a_end:
.org 0x4A34
m68k_004a34:
        bsr.w (. + -420)
m68k_004a34_end:
.org 0x4A38
m68k_004a38:
        move.w 0xf606:w,%d0
m68k_004a38_end:
.org 0x4A3C
m68k_004a3c:
        ori.b #0x40,%d0
m68k_004a3c_end:
.org 0x4A40
m68k_004a40:
        move.w %d0,0xc00004:l
m68k_004a40_end:
.org 0x4A46
m68k_004a46:
        clr.w 0xf612:w
m68k_004a46_end:
.org 0x4A4A
m68k_004a4a:
        rts
m68k_004a4a_end:
.org 0x4A4C
m68k_004a4c:
        move.w #0x2700,%sr
m68k_004a4c_end:
.org 0x4A50
m68k_004a50:
        bra.b (. + -4)
m68k_004a50_end:
.org 0x506C
m68k_00506c:
        cmpi.w #0x81,0xf38c:w
m68k_00506c_end:
.org 0x5072
m68k_005072:
        beq.w (. + 74)
m68k_005072_end:
.org 0x5076
m68k_005076:
        lea.l 0xd300:w,%a1
m68k_005076_end:
.org 0x507A
m68k_00507a:
        move.w 0xf36c:w,%d2
m68k_00507a_end:
.org 0x507E
m68k_00507e:
        lsl.w #0x1,%d2
m68k_00507e_end:
.org 0x5080
m68k_005080:
        move.w 60(%pc, %d2.w),%d2
m68k_005080_end:
.org 0x5084
m68k_005084:
        jsr 64(%pc, %d2.w)
m68k_005084_end:
.org 0x5088
m68k_005088:
        move.l #0x74000001,0xc00004:l
m68k_005088_end:
.org 0x5092
m68k_005092:
        lea.l 0xd300:w,%a1
m68k_005092_end:
.org 0x5096
m68k_005096:
        move.l (%a1)+,0xc00000:l
m68k_005096_end:
.org 0x509C
m68k_00509c:
        dbra %d4,(. + -6)
m68k_00509c_end:
.org 0x50A0
m68k_0050a0:
        move.l #0x76000001,0xc00004:l
m68k_0050a0_end:
.org 0x50AA
m68k_0050aa:
        move.w #0x7,%d3
m68k_0050aa_end:
.org 0x50AE
m68k_0050ae:
        move.l #0x11111111,0xc00000:l
m68k_0050ae_end:
.org 0x50B8
m68k_0050b8:
        dbra %d3,(. + -10)
m68k_0050b8_end:
.org 0x50BC
m68k_0050bc:
        rts
m68k_0050bc_end:
.org 0x50DC
m68k_0050dc:
        cmpi.w #0x20a,0xf612:w
m68k_0050dc_end:
.org 0x50E2
m68k_0050e2:
        beq.w (. + 82)
m68k_0050e2_end:
.org 0x50E6
m68k_0050e6:
        lea.l 0xc00000:l,%a6
m68k_0050e6_end:
.org 0x50EC
m68k_0050ec:
        lea.l 0xd300:w,%a1
m68k_0050ec_end:
.org 0x50F0
m68k_0050f0:
        move.w #0x1,%d2
m68k_0050f0_end:
.org 0x50F4
m68k_0050f4:
        clr.w %d3
m68k_0050f4_end:
.org 0x50F6
m68k_0050f6:
        clr.w %d4
m68k_0050f6_end:
.org 0x50F8
m68k_0050f8:
        clr.w %d6
m68k_0050f8_end:
.org 0x50FA
m68k_0050fa:
        lea.l 0xf578:w,%a2
m68k_0050fa_end:
.org 0x50FE
m68k_0050fe:
        clr.w %d5
m68k_0050fe_end:
.org 0x5100
m68k_005100:
        move.b (%a2)+,%d5
m68k_005100_end:
.org 0x5102
m68k_005102:
        lea.l 69(%pc),%a3
m68k_005102_end:
.org 0x5106
m68k_005106:
        move.b (%a3, %d5.w),%d5
m68k_005106_end:
.org 0x510A
m68k_00510a:
        ext.w %d5
m68k_00510a_end:
.org 0x510C
m68k_00510c:
        lsl.w #0x2,%d5
m68k_00510c_end:
.org 0x510E
m68k_00510e:
        lea.l 0x8a304:l,%a0
m68k_00510e_end:
.org 0x5114
m68k_005114:
        adda.w %d5,%a0
m68k_005114_end:
.org 0x5116
m68k_005116:
        move.w #0x1,%d3
m68k_005116_end:
.org 0x511A
m68k_00511a:
        jsr 0xae8a:l
m68k_00511a_end:
.org 0x5120
m68k_005120:
        addi.w #0x40,%d4
m68k_005120_end:
.org 0x5124
m68k_005124:
        addq.w #0x1,%d6
m68k_005124_end:
.org 0x5126
m68k_005126:
        dbra %d2,(. + -40)
m68k_005126_end:
.org 0x512A
m68k_00512a:
        move.w %d6,0xf390:w
m68k_00512a_end:
.org 0x512E
m68k_00512e:
        subq.w #0x1,%d4
m68k_00512e_end:
.org 0x5130
m68k_005130:
        bra.w (. + 24)
m68k_005130_end:
.org 0x5134
m68k_005134:
        lea.l 0x8a380:l,%a0
m68k_005134_end:
.org 0x513A
m68k_00513a:
        move.w #0x2,%d3
m68k_00513a_end:
.org 0x513E
m68k_00513e:
        jsr 0xae8a:l
m68k_00513e_end:
.org 0x5144
m68k_005144:
        move.w #0x5f,%d4
m68k_005144_end:
.org 0x5148
m68k_005148:
        rts
m68k_005148_end:
.org 0x5204
m68k_005204:
        lea.l 0x8a1fc:l,%a0
m68k_005204_end:
.org 0x520A
m68k_00520a:
        lea.l 0xd300:w,%a1
m68k_00520a_end:
.org 0x520E
m68k_00520e:
        move.w #0x1,%d3
m68k_00520e_end:
.org 0x5212
m68k_005212:
        jsr 0xae8a:l
m68k_005212_end:
.org 0x5218
m68k_005218:
        lea.l 0x8a200:l,%a0
m68k_005218_end:
.org 0x521E
m68k_00521e:
        move.w #0x9,%d3
m68k_00521e_end:
.org 0x5222
m68k_005222:
        jsr 0xae8a:l
m68k_005222_end:
.org 0x5228
m68k_005228:
        move.l #0x5a000000,0xc00004:l
m68k_005228_end:
.org 0x5232
m68k_005232:
        lea.l 0xd300:w,%a1
m68k_005232_end:
.org 0x5236
m68k_005236:
        move.w #0x17f,%d4
m68k_005236_end:
.org 0x523A
m68k_00523a:
        move.l (%a1)+,(%a6)
m68k_00523a_end:
.org 0x523C
m68k_00523c:
        dbra %d4,(. + -2)
m68k_00523c_end:
.org 0x5240
m68k_005240:
        rts
m68k_005240_end:
.org 0x52C2
m68k_0052c2:
        move.l #0x70000001,0xc00004:l
m68k_0052c2_end:
.org 0x52CC
m68k_0052cc:
        lea.l 0x89ddc:l,%a0
m68k_0052cc_end:
.org 0x52D2
m68k_0052d2:
        move.w #0x17,%d4
m68k_0052d2_end:
.org 0x52D6
m68k_0052d6:
        move.l (%a0)+,0xc00000:l
m68k_0052d6_end:
.org 0x52DC
m68k_0052dc:
        dbra %d4,(. + -6)
m68k_0052dc_end:
.org 0x52E0
m68k_0052e0:
        move.l #0x70a00001,0xc00004:l
m68k_0052e0_end:
.org 0x52EA
m68k_0052ea:
        lea.l 0x89f5c:l,%a0
m68k_0052ea_end:
.org 0x52F0
m68k_0052f0:
        move.w #0x7,%d4
m68k_0052f0_end:
.org 0x52F4
m68k_0052f4:
        move.l (%a0)+,0xc00000:l
m68k_0052f4_end:
.org 0x52FA
m68k_0052fa:
        dbra %d4,(. + -6)
m68k_0052fa_end:
.org 0x52FE
m68k_0052fe:
        move.l #0x72000001,0xc00004:l
m68k_0052fe_end:
.org 0x5308
m68k_005308:
        move.w #0x7,%d4
m68k_005308_end:
.org 0x530C
m68k_00530c:
        move.l #0x33333333,0xc00000:l
m68k_00530c_end:
.org 0x5316
m68k_005316:
        dbra %d4,(. + -10)
m68k_005316_end:
.org 0x531A
m68k_00531a:
        lea.l 0x8a0bc:l,%a0
m68k_00531a_end:
.org 0x5320
m68k_005320:
        move.w #0x7,%d4
m68k_005320_end:
.org 0x5324
m68k_005324:
        move.l (%a0)+,0xc00000:l
m68k_005324_end:
.org 0x532A
m68k_00532a:
        dbra %d4,(. + -6)
m68k_00532a_end:
.org 0x532E
m68k_00532e:
        rts
m68k_00532e_end:
.org 0x55B0
m68k_0055b0:
        lea.l 0x89efc:l,%a0
m68k_0055b0_end:
.org 0x55B6
m68k_0055b6:
        move.l #0x67a00001,0xc00004:l
m68k_0055b6_end:
.org 0x55C0
m68k_0055c0:
        move.w #0x17,%d0
m68k_0055c0_end:
.org 0x55C4
m68k_0055c4:
        move.l (%a0)+,0xc00000:l
m68k_0055c4_end:
.org 0x55CA
m68k_0055ca:
        dbra %d0,(. + -6)
m68k_0055ca_end:
.org 0x55CE
m68k_0055ce:
        rts
m68k_0055ce_end:
.org 0x5ABC
m68k_005abc:
        cmpi.w #0x81,0xf38c:w
m68k_005abc_end:
.org 0x5AC2
m68k_005ac2:
        beq.w (. + 34)
m68k_005ac2_end:
.org 0x5AC6
m68k_005ac6:
        move.l #0xc000000b,%d0
m68k_005ac6_end:
.org 0x5ACC
m68k_005acc:
        move.w #0x4,%d1
m68k_005acc_end:
.org 0x5AD0
m68k_005ad0:
        move.w 0xf36c:w,%d7
m68k_005ad0_end:
.org 0x5AD4
m68k_005ad4:
        lsl.w #0x1,%d7
m68k_005ad4_end:
.org 0x5AD6
m68k_005ad6:
        move.w 14(%pc, %d7.w),%d7
m68k_005ad6_end:
.org 0x5ADA
m68k_005ada:
        jsr 18(%pc, %d7.w)
m68k_005ada_end:
.org 0x5ADE
m68k_005ade:
        bset.b #0x3,0xf3a4:w
m68k_005ade_end:
.org 0x5AE4
m68k_005ae4:
        rts
m68k_005ae4_end:
.org 0x5B5C
m68k_005b5c:
        move.w #0xc084,%d2
m68k_005b5c_end:
.org 0x5B60
m68k_005b60:
        lea.l 170(%pc),%a0
m68k_005b60_end:
.org 0x5B64
m68k_005b64:
        cmpi.w #0x20a,0xf612:w
m68k_005b64_end:
.org 0x5B6A
m68k_005b6a:
        bne.w (. + 8)
m68k_005b6a_end:
.org 0x5B6E
m68k_005b6e:
        lea.l 248(%pc),%a0
m68k_005b6e_end:
.org 0x5B72
m68k_005b72:
        jsr 0x26bfa:l
m68k_005b72_end:
.org 0x5B78
m68k_005b78:
        ori.w #0x8080,0xf3a4:w
m68k_005b78_end:
.org 0x5B7E
m68k_005b7e:
        rts
m68k_005b7e_end:
.org 0x5CF8
m68k_005cf8:
        cmp.w %d2,%d5
m68k_005cf8_end:
.org 0x5CFA
m68k_005cfa:
        bcs.b (. + 10)
m68k_005cfa_end:
.org 0x5CFC
m68k_005cfc:
        cmp.w %d3,%d5
m68k_005cfc_end:
.org 0x5CFE
m68k_005cfe:
        bhi.b (. + 6)
m68k_005cfe_end:
.org 0x5D00
m68k_005d00:
        bra.b (. + 16)
m68k_005d00_end:
.org 0x5D02
m68k_005d02:
        addq.w #0x2,%a0
m68k_005d02_end:
.org 0x5D04
m68k_005d04:
        addq.w #0x1,%d4
m68k_005d04_end:
.org 0x5D06
m68k_005d06:
        cmpi.w #0x28,%d4
m68k_005d06_end:
.org 0x5D0A
m68k_005d0a:
        bcs.b (. + -30)
m68k_005d0a_end:
.org 0x5D0C
m68k_005d0c:
        move.w #0xffff,%d4
m68k_005d0c_end:
.org 0x5D10
m68k_005d10:
        tst.w %d4
m68k_005d10_end:
.org 0x5D12
m68k_005d12:
        bmi.w (. + 180)
m68k_005d12_end:
.org 0x5D16
m68k_005d16:
        clr.w %d0
m68k_005d16_end:
.org 0x5D18
m68k_005d18:
        lea.l 0xf428:w,%a0
m68k_005d18_end:
.org 0x5D1C
m68k_005d1c:
        move.b (%a0, %d4.w),%d0
m68k_005d1c_end:
.org 0x5D20
m68k_005d20:
        tst.w 0xf36c:w
m68k_005d20_end:
.org 0x5D24
m68k_005d24:
        beq.b (. + 80)
m68k_005d24_end:
.org 0x5D26
m68k_005d26:
        cmpi.w #0x6,0xf38c:w
m68k_005d26_end:
.org 0x5D2C
m68k_005d2c:
        beq.w (. + 154)
m68k_005d2c_end:
.org 0x5D30
m68k_005d30:
        cmpi.w #0xf,0xf38c:w
m68k_005d30_end:
.org 0x5D36
m68k_005d36:
        beq.w (. + 144)
m68k_005d36_end:
.org 0x5D3A
m68k_005d3a:
        cmpi.w #0x15,0xf38c:w
m68k_005d3a_end:
.org 0x5D40
m68k_005d40:
        beq.w (. + 134)
m68k_005d40_end:
.org 0x5D44
m68k_005d44:
        cmpi.w #0x64,0xf380:w
m68k_005d44_end:
.org 0x5D4A
m68k_005d4a:
        beq.b (. + 54)
m68k_005d4a_end:
.org 0x5D4C
m68k_005d4c:
        cmpi.w #0x77,0xf380:w
m68k_005d4c_end:
.org 0x5D52
m68k_005d52:
        beq.b (. + 46)
m68k_005d52_end:
.org 0x5D54
m68k_005d54:
        cmpi.w #0x75,0xf380:w
m68k_005d54_end:
.org 0x5D5A
m68k_005d5a:
        beq.b (. + 86)
m68k_005d5a_end:
.org 0x5D5C
m68k_005d5c:
        cmpi.w #0x63,0xf380:w
m68k_005d5c_end:
.org 0x5D62
m68k_005d62:
        bne.b (. + 18)
m68k_005d62_end:
.org 0x5D64
m68k_005d64:
        move.w 0xf3a8:w,%d1
m68k_005d64_end:
.org 0x5D68
m68k_005d68:
        subq.w #0x1,%d1
m68k_005d68_end:
.org 0x5D6A
m68k_005d6a:
        cmp.w %d1,%d4
m68k_005d6a_end:
.org 0x5D6C
m68k_005d6c:
        bne.b (. + 8)
m68k_005d6c_end:
.org 0x5D6E
m68k_005d6e:
        move.w #0xffff,%d4
m68k_005d6e_end:
.org 0x5D72
m68k_005d72:
        bra.b (. + 84)
m68k_005d72_end:
.org 0x5D74
m68k_005d74:
        cmp.w 0xf376:w,%d0
m68k_005d74_end:
.org 0x5D78
m68k_005d78:
        beq.b (. + 78)
m68k_005d78_end:
.org 0x5D7A
m68k_005d7a:
        bset.l #0xf,%d4
m68k_005d7a_end:
.org 0x5D7E
m68k_005d7e:
        bra.b (. + 72)
m68k_005d7e_end:
.org 0x5D80
m68k_005d80:
        cmpi.w #0x6,0xf38c:w
m68k_005d80_end:
.org 0x5D86
m68k_005d86:
        beq.w (. + 30)
m68k_005d86_end:
.org 0x5D8A
m68k_005d8a:
        cmpi.w #0xf,0xf38c:w
m68k_005d8a_end:
.org 0x5D90
m68k_005d90:
        beq.w (. + 20)
m68k_005d90_end:
.org 0x5D94
m68k_005d94:
        cmpi.w #0x15,0xf38c:w
m68k_005d94_end:
.org 0x5D9A
m68k_005d9a:
        beq.w (. + 10)
m68k_005d9a_end:
.org 0x5D9E
m68k_005d9e:
        cmpi.w #0x10,%d0
m68k_005d9e_end:
.org 0x5DA2
m68k_005da2:
        bcc.b (. + 8)
m68k_005da2_end:
.org 0x5DA4
m68k_005da4:
        cmp.w 0xf376:w,%d0
m68k_005da4_end:
.org 0x5DA8
m68k_005da8:
        bne.b (. + 30)
m68k_005da8_end:
.org 0x5DAA
m68k_005daa:
        bset.l #0xf,%d4
m68k_005daa_end:
.org 0x5DAE
m68k_005dae:
        bra.b (. + 24)
m68k_005dae_end:
.org 0x5DB0
m68k_005db0:
        move.w 0xf376:w,%d1
m68k_005db0_end:
.org 0x5DB4
m68k_005db4:
        lsl.w #0x1,%d1
m68k_005db4_end:
.org 0x5DB6
m68k_005db6:
        lea.l 0xe710:w,%a0
m68k_005db6_end:
.org 0x5DBA
m68k_005dba:
        move.w (%a0, %d1.w),%d1
m68k_005dba_end:
.org 0x5DBE
m68k_005dbe:
        btst.l %d0,%d1
m68k_005dbe_end:
.org 0x5DC0
m68k_005dc0:
        bne.b (. + 6)
m68k_005dc0_end:
.org 0x5DC2
m68k_005dc2:
        bset.l #0xf,%d4
m68k_005dc2_end:
.org 0x5DC6
m68k_005dc6:
        move.w %d4,0xf364:w
m68k_005dc6_end:
.org 0x5DCA
m68k_005dca:
        rts
m68k_005dca_end:
.org 0x5F48
m68k_005f48:
        lea.l 0xcc00:w,%a0
m68k_005f48_end:
.org 0x5F4C
m68k_005f4c:
        lea.l 0xf500:w,%a1
m68k_005f4c_end:
.org 0x5F50
m68k_005f50:
        clr.w %d1
m68k_005f50_end:
.org 0x5F52
m68k_005f52:
        clr.w %d3
m68k_005f52_end:
.org 0x5F54
m68k_005f54:
        move.w 0xf630:w,%d4
m68k_005f54_end:
.org 0x5F58
m68k_005f58:
        bmi.b (. + 6)
m68k_005f58_end:
.org 0x5F5A
m68k_005f5a:
        move.w %d4,(%a1)+
m68k_005f5a_end:
.org 0x5F5C
m68k_005f5c:
        addq.w #0x1,%d3
m68k_005f5c_end:
.org 0x5F5E
m68k_005f5e:
        move.b (%a0)+,%d2
m68k_005f5e_end:
.org 0x5F60
m68k_005f60:
        cmp.b %d0,%d2
m68k_005f60_end:
.org 0x5F62
m68k_005f62:
        bne.b (. + 12)
m68k_005f62_end:
.org 0x5F64
m68k_005f64:
        cmp.w 0xf630:w,%d1
m68k_005f64_end:
.org 0x5F68
m68k_005f68:
        beq.b (. + 6)
m68k_005f68_end:
.org 0x5F6A
m68k_005f6a:
        move.w %d1,(%a1)+
m68k_005f6a_end:
.org 0x5F6C
m68k_005f6c:
        addq.w #0x1,%d3
m68k_005f6c_end:
.org 0x5F6E
m68k_005f6e:
        addq.w #0x1,%d1
m68k_005f6e_end:
.org 0x5F70
m68k_005f70:
        cmpi.w #0x100,%d1
m68k_005f70_end:
.org 0x5F74
m68k_005f74:
        bcs.b (. + -22)
m68k_005f74_end:
.org 0x5F76
m68k_005f76:
        move.w #0xffff,(%a1)
m68k_005f76_end:
.org 0x5F7A
m68k_005f7a:
        rts
m68k_005f7a_end:
.org 0x6232
m68k_006232:
        jsr 0x135c4:l
m68k_006232_end:
.org 0x6238
m68k_006238:
        move.w #0x4c,0xf600:w
m68k_006238_end:
.org 0x623E
m68k_00623e:
        move.w 0xf378:w,%d0
m68k_00623e_end:
.org 0x6242
m68k_006242:
        lsl.w #0x1,%d0
m68k_006242_end:
.org 0x6244
m68k_006244:
        lea.l 0xf4fe:w,%a0
m68k_006244_end:
.org 0x6248
m68k_006248:
        move.w (%a0, %d0.w),%d0
m68k_006248_end:
.org 0x624C
m68k_00624c:
        lsl.w #0x2,%d0
m68k_00624c_end:
.org 0x624E
m68k_00624e:
        lea.l 0xc800:w,%a0
m68k_00624e_end:
.org 0x6252
m68k_006252:
        move.l (%a0, %d0.w),0xf3ee:w
m68k_006252_end:
.org 0x6258
m68k_006258:
        jsr 0x136f4:l
m68k_006258_end:
.org 0x625E
m68k_00625e:
        jsr 0x1374a:l
m68k_00625e_end:
.org 0x6264
m68k_006264:
        bra.b (. + 18)
m68k_006264_end:
.org 0x6518
m68k_006518:
        bsr.w (. + 268)
m68k_006518_end:
.org 0x651C
m68k_00651c:
        bsr.w (. + 70)
m68k_00651c_end:
.org 0x6520
m68k_006520:
        lea.l 0xff4000:l,%a5
m68k_006520_end:
.org 0x6526
m68k_006526:
        lea.l 0xff4800:l,%a6
m68k_006526_end:
.org 0x652C
m68k_00652c:
        move.b 0xf641:w,(%a5)
m68k_00652c_end:
.org 0x6530
m68k_006530:
        move.b 0xf643:w,0x1(%a5)
m68k_006530_end:
.org 0x6536
m68k_006536:
        move.b #0x1,0x2(%a5)
m68k_006536_end:
.org 0x653C
m68k_00653c:
        move.b #0xff,0x3(%a5)
m68k_00653c_end:
.org 0x6542
m68k_006542:
        clr.w %d5
m68k_006542_end:
.org 0x6544
m68k_006544:
        movea.l %a5,%a0
m68k_006544_end:
.org 0x6546
m68k_006546:
        movea.l %a6,%a1
m68k_006546_end:
.org 0x6548
m68k_006548:
        bsr.w (. + 262)
m68k_006548_end:
.org 0x654C
m68k_00654c:
        bcs.w (. + 10)
m68k_00654c_end:
.org 0x6550
m68k_006550:
        exg %a5,%a6
m68k_006550_end:
.org 0x6552
m68k_006552:
        addq.w #0x1,%d5
m68k_006552_end:
.org 0x6554
m68k_006554:
        bra.b (. + -16)
m68k_006554_end:
.org 0x6556
m68k_006556:
        addq.w #0x1,%d5
m68k_006556_end:
.org 0x6558
m68k_006558:
        move.w %d5,0xf644:w
m68k_006558_end:
.org 0x655C
m68k_00655c:
        bsr.w (. + 520)
m68k_00655c_end:
.org 0x6560
m68k_006560:
        rts
m68k_006560_end:
.org 0x6562
m68k_006562:
        lea.l 0xff0000:l,%a0
m68k_006562_end:
.org 0x6568
m68k_006568:
        lea.l 0xee5f0:l,%a1
m68k_006568_end:
.org 0x656E
m68k_00656e:
        lea.l 410(%pc),%a2
m68k_00656e_end:
.org 0x6572
m68k_006572:
        nop
m68k_006572_end:
.org 0x6574
m68k_006574:
        move.w #0x143f,%d0
m68k_006574_end:
.org 0x6578
m68k_006578:
        clr.w %d1
m68k_006578_end:
.org 0x657A
m68k_00657a:
        clr.w %d2
m68k_00657a_end:
.org 0x657C
m68k_00657c:
        move.b (%a1)+,%d1
m68k_00657c_end:
.org 0x657E
m68k_00657e:
        move.b (%a2, %d1.w),%d2
m68k_00657e_end:
.org 0x6582
m68k_006582:
        move.w %d2,(%a0)+
m68k_006582_end:
.org 0x6584
m68k_006584:
        dbra %d0,(. + -8)
m68k_006584_end:
.org 0x6588
m68k_006588:
        lea.l 0xff0000:l,%a0
m68k_006588_end:
.org 0x658E
m68k_00658e:
        lea.l 0xce00:w,%a1
m68k_00658e_end:
.org 0x6592
m68k_006592:
        move.w #0x27,%d0
m68k_006592_end:
.org 0x6596
m68k_006596:
        tst.b (%a1)
m68k_006596_end:
.org 0x6598
m68k_006598:
        beq.b (. + 38)
m68k_006598_end:
.org 0x659A
m68k_00659a:
        btst.b #0x4,(%a1)
m68k_00659a_end:
.org 0x659E
m68k_00659e:
        bne.b (. + 32)
m68k_00659e_end:
.org 0x65BE
m68k_0065be:
        addq.w #0x4,%a1
m68k_0065be_end:
.org 0x65C0
m68k_0065c0:
        dbra %d0,(. + -42)
m68k_0065c0_end:
.org 0x65C4
m68k_0065c4:
        lea.l 0x9000:w,%a1
m68k_0065c4_end:
.org 0x65C8
m68k_0065c8:
        move.b (%a1),%d0
m68k_0065c8_end:
.org 0x65CA
m68k_0065ca:
        andi.w #0xf,%d0
m68k_0065ca_end:
.org 0x65CE
m68k_0065ce:
        beq.b (. + 38)
m68k_0065ce_end:
.org 0x65F4
m68k_0065f4:
        lea.l 0xd4aca:l,%a1
m68k_0065f4_end:
.org 0x65FA
m68k_0065fa:
        move.w #0x27,%d0
m68k_0065fa_end:
.org 0x65FE
m68k_0065fe:
        move.w (%a1)+,%d1
m68k_0065fe_end:
.org 0x6600
m68k_006600:
        lsr.w #0x4,%d1
m68k_006600_end:
.org 0x6602
m68k_006602:
        move.w (%a1)+,%d2
m68k_006602_end:
.org 0x6604
m68k_006604:
        lsr.w #0x4,%d2
m68k_006604_end:
.org 0x6606
m68k_006606:
        move.w %d2,%d3
m68k_006606_end:
.org 0x6608
m68k_006608:
        lsl.w #0x3,%d2
m68k_006608_end:
.org 0x660A
m68k_00660a:
        add.w %d3,%d2
m68k_00660a_end:
.org 0x660C
m68k_00660c:
        lsl.w #0x3,%d2
m68k_00660c_end:
.org 0x660E
m68k_00660e:
        add.w %d1,%d2
m68k_00660e_end:
.org 0x6610
m68k_006610:
        lsl.w #0x1,%d2
m68k_006610_end:
.org 0x6612
m68k_006612:
        move.w #0xff,-0x2(%a0, %d2.w)
m68k_006612_end:
.org 0x6618
m68k_006618:
        move.w #0xff,(%a0, %d2.w)
m68k_006618_end:
.org 0x661E
m68k_00661e:
        dbra %d0,(. + -32)
m68k_00661e_end:
.org 0x6622
m68k_006622:
        rts
m68k_006622_end:
.org 0x6624
m68k_006624:
        move.w 0xf63c:w,%d0
m68k_006624_end:
.org 0x6628
m68k_006628:
        lsr.w #0x4,%d0
m68k_006628_end:
.org 0x662A
m68k_00662a:
        move.w %d0,0xf63c:w
m68k_00662a_end:
.org 0x662E
m68k_00662e:
        move.w 0xf63e:w,%d0
m68k_00662e_end:
.org 0x6632
m68k_006632:
        lsr.w #0x4,%d0
m68k_006632_end:
.org 0x6634
m68k_006634:
        move.w %d0,0xf63e:w
m68k_006634_end:
.org 0x6638
m68k_006638:
        move.w 0xf640:w,%d0
m68k_006638_end:
.org 0x663C
m68k_00663c:
        lsr.w #0x4,%d0
m68k_00663c_end:
.org 0x663E
m68k_00663e:
        move.w %d0,0xf640:w
m68k_00663e_end:
.org 0x6642
m68k_006642:
        move.w 0xf642:w,%d0
m68k_006642_end:
.org 0x6646
m68k_006646:
        lsr.w #0x4,%d0
m68k_006646_end:
.org 0x6648
m68k_006648:
        move.w %d0,0xf642:w
m68k_006648_end:
.org 0x664C
m68k_00664c:
        rts
m68k_00664c_end:
.org 0x664E
m68k_00664e:
        clr.w %d0
m68k_00664e_end:
.org 0x6650
m68k_006650:
        move.b (%a0)+,%d0
m68k_006650_end:
.org 0x6652
m68k_006652:
        clr.w %d1
m68k_006652_end:
.org 0x6654
m68k_006654:
        move.b (%a0)+,%d1
m68k_006654_end:
.org 0x6656
m68k_006656:
        move.b (%a0)+,%d2
m68k_006656_end:
.org 0x6658
m68k_006658:
        subq.b #0x1,%d2
m68k_006658_end:
.org 0x665A
m68k_00665a:
        beq.b (. + 12)
m68k_00665a_end:
.org 0x665C
m68k_00665c:
        move.b %d0,(%a1)+
m68k_00665c_end:
.org 0x665E
m68k_00665e:
        move.b %d1,(%a1)+
m68k_00665e_end:
.org 0x6660
m68k_006660:
        move.b %d2,(%a1)+
m68k_006660_end:
.org 0x6662
m68k_006662:
        bra.w (. + 82)
m68k_006662_end:
.org 0x6666
m68k_006666:
        subq.w #0x1,%d0
m68k_006666_end:
.org 0x6668
m68k_006668:
        bcs.b (. + 14)
m68k_006668_end:
.org 0x666A
m68k_00666a:
        move.w #0x3,%d3
m68k_00666a_end:
.org 0x666E
m68k_00666e:
        bsr.w (. + 84)
m68k_00666e_end:
.org 0x6672
m68k_006672:
        bcs.w (. + 78)
m68k_006672_end:
.org 0x6676
m68k_006676:
        addq.w #0x1,%d0
m68k_006676_end:
.org 0x6678
m68k_006678:
        subq.w #0x1,%d1
m68k_006678_end:
.org 0x667A
m68k_00667a:
        bcs.b (. + 14)
m68k_00667a_end:
.org 0x667C
m68k_00667c:
        move.w #0x2,%d3
m68k_00667c_end:
.org 0x6680
m68k_006680:
        bsr.w (. + 66)
m68k_006680_end:
.org 0x6684
m68k_006684:
        bcs.w (. + 60)
m68k_006684_end:
.org 0x6688
m68k_006688:
        addq.w #0x2,%d1
m68k_006688_end:
.org 0x668A
m68k_00668a:
        cmpi.w #0x48,%d1
m68k_00668a_end:
.org 0x668E
m68k_00668e:
        bcc.b (. + 14)
m68k_00668e_end:
.org 0x6690
m68k_006690:
        move.w #0x4,%d3
m68k_006690_end:
.org 0x6694
m68k_006694:
        bsr.w (. + 46)
m68k_006694_end:
.org 0x6698
m68k_006698:
        bcs.w (. + 40)
m68k_006698_end:
.org 0x669C
m68k_00669c:
        addq.w #0x1,%d0
m68k_00669c_end:
.org 0x669E
m68k_00669e:
        cmpi.w #0x48,%d0
m68k_00669e_end:
.org 0x66A2
m68k_0066a2:
        bcc.w (. + 18)
m68k_0066a2_end:
.org 0x66A6
m68k_0066a6:
        subq.w #0x1,%d1
m68k_0066a6_end:
.org 0x66A8
m68k_0066a8:
        move.w #0x1,%d3
m68k_0066a8_end:
.org 0x66AC
m68k_0066ac:
        bsr.w (. + 22)
m68k_0066ac_end:
.org 0x66B0
m68k_0066b0:
        bcs.w (. + 16)
m68k_0066b0_end:
.org 0x66B4
m68k_0066b4:
        tst.b (%a0)
m68k_0066b4_end:
.org 0x66B6
m68k_0066b6:
        bpl.b (. + -104)
m68k_0066b6_end:
.org 0x66B8
m68k_0066b8:
        move.b #0xff,(%a1)
m68k_0066b8_end:
.org 0x66BC
m68k_0066bc:
        andi.w #0xfffe,%sr
m68k_0066bc_end:
.org 0x66C0
m68k_0066c0:
        rts
m68k_0066c0_end:
.org 0x66C2
m68k_0066c2:
        bsr.w (. + 44)
m68k_0066c2_end:
.org 0x66C6
m68k_0066c6:
        bcs.w (. + 38)
m68k_0066c6_end:
.org 0x66CA
m68k_0066ca:
        bsr.w (. + 98)
m68k_0066ca_end:
.org 0x66CE
m68k_0066ce:
        tst.b %d2
m68k_0066ce_end:
.org 0x66D0
m68k_0066d0:
        bne.b (. + 24)
m68k_0066d0_end:
.org 0x66D2
m68k_0066d2:
        bsr.w (. + 118)
m68k_0066d2_end:
.org 0x66D6
m68k_0066d6:
        tst.b %d2
m68k_0066d6_end:
.org 0x66D8
m68k_0066d8:
        bmi.b (. + 16)
m68k_0066d8_end:
.org 0x66DA
m68k_0066da:
        move.b %d0,(%a1)+
m68k_0066da_end:
.org 0x66DC
m68k_0066dc:
        ext.w %d0
m68k_0066dc_end:
.org 0x66DE
m68k_0066de:
        move.b %d1,(%a1)+
m68k_0066de_end:
.org 0x66E0
m68k_0066e0:
        ext.w %d1
m68k_0066e0_end:
.org 0x66E2
m68k_0066e2:
        move.b %d2,(%a1)+
m68k_0066e2_end:
.org 0x66E4
m68k_0066e4:
        bsr.w (. + 44)
m68k_0066e4_end:
.org 0x66E8
m68k_0066e8:
        andi.w #0xfffe,%sr
m68k_0066e8_end:
.org 0x66EC
m68k_0066ec:
        rts
m68k_0066ec_end:
.org 0x66EE
m68k_0066ee:
        cmp.w 0xf63c:w,%d0
m68k_0066ee_end:
.org 0x66F2
m68k_0066f2:
        bne.b (. + 18)
m68k_0066f2_end:
.org 0x66F4
m68k_0066f4:
        cmp.w 0xf63e:w,%d1
m68k_0066f4_end:
.org 0x66F8
m68k_0066f8:
        bne.b (. + 12)
m68k_0066f8_end:
.org 0x66FA
m68k_0066fa:
        bsr.w (. + 22)
m68k_0066fa_end:
.org 0x66FE
m68k_0066fe:
        ori.w #0x1,%sr
m68k_0066fe_end:
.org 0x6702
m68k_006702:
        rts
m68k_006702_end:
.org 0x6704
m68k_006704:
        andi.w #0xfffe,%sr
m68k_006704_end:
.org 0x6708
m68k_006708:
        rts
m68k_006708_end:
.org 0x6710
m68k_006710:
        move.l %d0,-(%a7)
m68k_006710_end:
.org 0x6712
m68k_006712:
        move.w %d0,%d2
m68k_006712_end:
.org 0x6714
m68k_006714:
        lsl.w #0x3,%d2
m68k_006714_end:
.org 0x6716
m68k_006716:
        add.w %d2,%d0
m68k_006716_end:
.org 0x6718
m68k_006718:
        lsl.w #0x3,%d0
m68k_006718_end:
.org 0x671A
m68k_00671a:
        add.w %d1,%d0
m68k_00671a_end:
.org 0x671C
m68k_00671c:
        lsl.w #0x1,%d0
m68k_00671c_end:
.org 0x671E
m68k_00671e:
        lea.l 0xff0000:l,%a2
m68k_00671e_end:
.org 0x6724
m68k_006724:
        move.b %d3,(%a2, %d0.w)
m68k_006724_end:
.org 0x6728
m68k_006728:
        move.l (%a7)+,%d0
m68k_006728_end:
.org 0x672A
m68k_00672a:
        rts
m68k_00672a_end:
.org 0x672C
m68k_00672c:
        move.w %d0,-(%a7)
m68k_00672c_end:
.org 0x672E
m68k_00672e:
        move.w %d0,%d2
m68k_00672e_end:
.org 0x6730
m68k_006730:
        lsl.w #0x3,%d2
m68k_006730_end:
.org 0x6732
m68k_006732:
        add.w %d2,%d0
m68k_006732_end:
.org 0x6734
m68k_006734:
        lsl.w #0x3,%d0
m68k_006734_end:
.org 0x6736
m68k_006736:
        add.w %d1,%d0
m68k_006736_end:
.org 0x6738
m68k_006738:
        lsl.w #0x1,%d0
m68k_006738_end:
.org 0x673A
m68k_00673a:
        lea.l 0xff0000:l,%a2
m68k_00673a_end:
.org 0x6740
m68k_006740:
        move.b (%a2, %d0.w),%d2
m68k_006740_end:
.org 0x6744
m68k_006744:
        move.w (%a7)+,%d0
m68k_006744_end:
.org 0x6746
m68k_006746:
        rts
m68k_006746_end:
.org 0x6748
m68k_006748:
        move.w %d0,%d4
m68k_006748_end:
.org 0x674A
m68k_00674a:
        move.w %d4,%d2
m68k_00674a_end:
.org 0x674C
m68k_00674c:
        lsl.w #0x3,%d2
m68k_00674c_end:
.org 0x674E
m68k_00674e:
        add.w %d2,%d4
m68k_00674e_end:
.org 0x6750
m68k_006750:
        lsl.w #0x3,%d4
m68k_006750_end:
.org 0x6752
m68k_006752:
        add.w %d1,%d4
m68k_006752_end:
.org 0x6754
m68k_006754:
        lsl.w #0x1,%d4
m68k_006754_end:
.org 0x6756
m68k_006756:
        lea.l 0xff0000:l,%a2
m68k_006756_end:
.org 0x675C
m68k_00675c:
        clr.w %d2
m68k_00675c_end:
.org 0x675E
m68k_00675e:
        move.b 0x1(%a2, %d4.w),%d2
m68k_00675e_end:
.org 0x6762
m68k_006762:
        rts
m68k_006762_end:
.org 0x6764
m68k_006764:
        lea.l 0xff4000:l,%a0
m68k_006764_end:
.org 0x676A
m68k_00676a:
        move.w 0xf63c:w,%d0
m68k_00676a_end:
.org 0x676E
m68k_00676e:
        move.w 0xf63e:w,%d1
m68k_00676e_end:
.org 0x6772
m68k_006772:
        bsr.b (. + -70)
m68k_006772_end:
.org 0x6774
m68k_006774:
        move.b %d2,(%a0)+
m68k_006774_end:
.org 0x6776
m68k_006776:
        bsr.w (. + 24)
m68k_006776_end:
.org 0x677A
m68k_00677a:
        cmp.w 0xf640:w,%d0
m68k_00677a_end:
.org 0x677E
m68k_00677e:
        bne.b (. + 8)
m68k_00677e_end:
.org 0x6780
m68k_006780:
        cmp.w 0xf642:w,%d1
m68k_006780_end:
.org 0x6784
m68k_006784:
        beq.b (. + 4)
m68k_006784_end:
.org 0x6786
m68k_006786:
        bra.b (. + -20)
m68k_006786_end:
.org 0x6788
m68k_006788:
        move.b #0xff,(%a0)
m68k_006788_end:
.org 0x678C
m68k_00678c:
        rts
m68k_00678c_end:
.org 0x678E
m68k_00678e:
        subq.b #0x1,%d2
m68k_00678e_end:
.org 0x6790
m68k_006790:
        beq.w (. + 22)
m68k_006790_end:
.org 0x6794
m68k_006794:
        subq.b #0x1,%d2
m68k_006794_end:
.org 0x6796
m68k_006796:
        beq.w (. + 22)
m68k_006796_end:
.org 0x679A
m68k_00679a:
        subq.b #0x1,%d2
m68k_00679a_end:
.org 0x679C
m68k_00679c:
        beq.w (. + 20)
m68k_00679c_end:
.org 0x67A0
m68k_0067a0:
        subq.w #0x1,%d1
m68k_0067a0_end:
.org 0x67A2
m68k_0067a2:
        bra.w (. + 16)
m68k_0067a2_end:
.org 0x67B0
m68k_0067b0:
        addq.w #0x1,%d0
m68k_0067b0_end:
.org 0x67B2
m68k_0067b2:
        rts
m68k_0067b2_end:
.org 0x67B4
m68k_0067b4:
        moveq #64,%d0
m68k_0067b4_end:
.org 0x67B6
m68k_0067b6:
        move.b %d0,0xa10009:l
m68k_0067b6_end:
.org 0x67BC
m68k_0067bc:
        move.b %d0,0xa1000b:l
m68k_0067bc_end:
.org 0x67C2
m68k_0067c2:
        move.b %d0,0xa1000d:l
m68k_0067c2_end:
.org 0x67C8
m68k_0067c8:
        rts
m68k_0067c8_end:
.org 0x67CA
m68k_0067ca:
        move.w #0x100,0xa11100:l
m68k_0067ca_end:
.org 0x67D2
m68k_0067d2:
        btst.b #0x0,0xa11100:l
m68k_0067d2_end:
.org 0x67DA
m68k_0067da:
        bne.b (. + -8)
m68k_0067da_end:
.org 0x67DC
m68k_0067dc:
        bsr.b (. + 12)
m68k_0067dc_end:
.org 0x67DE
m68k_0067de:
        move.w #0x0,0xa11100:l
m68k_0067de_end:
.org 0x67E6
m68k_0067e6:
        rts
m68k_0067e6_end:
.org 0x67E8
m68k_0067e8:
        lea.l 0xf602:w,%a0
m68k_0067e8_end:
.org 0x67EC
m68k_0067ec:
        lea.l 0xa10003:l,%a1
m68k_0067ec_end:
.org 0x67F2
m68k_0067f2:
        bsr.b (. + 4)
m68k_0067f2_end:
.org 0x67F4
m68k_0067f4:
        addq.w #0x2,%a1
m68k_0067f4_end:
.org 0x67F6
m68k_0067f6:
        move.b #0x0,(%a1)
m68k_0067f6_end:
.org 0x67FA
m68k_0067fa:
        nop
m68k_0067fa_end:
.org 0x67FC
m68k_0067fc:
        nop
m68k_0067fc_end:
.org 0x67FE
m68k_0067fe:
        move.b (%a1),%d0
m68k_0067fe_end:
.org 0x6800
m68k_006800:
        lsl.b #0x2,%d0
m68k_006800_end:
.org 0x6802
m68k_006802:
        andi.b #0xc0,%d0
m68k_006802_end:
.org 0x6806
m68k_006806:
        move.b #0x40,(%a1)
m68k_006806_end:
.org 0x680A
m68k_00680a:
        nop
m68k_00680a_end:
.org 0x680C
m68k_00680c:
        nop
m68k_00680c_end:
.org 0x680E
m68k_00680e:
        move.b (%a1),%d1
m68k_00680e_end:
.org 0x6810
m68k_006810:
        andi.b #0x3f,%d1
m68k_006810_end:
.org 0x6814
m68k_006814:
        or.b %d1,%d0
m68k_006814_end:
.org 0x6816
m68k_006816:
        not.b %d0
m68k_006816_end:
.org 0x6818
m68k_006818:
        move.b %d0,%d1
m68k_006818_end:
.org 0x681A
m68k_00681a:
        move.b (%a0),%d2
m68k_00681a_end:
.org 0x681C
m68k_00681c:
        eor.b %d2,%d0
m68k_00681c_end:
.org 0x681E
m68k_00681e:
        move.b %d1,(%a0)+
m68k_00681e_end:
.org 0x6820
m68k_006820:
        and.b %d1,%d0
m68k_006820_end:
.org 0x6822
m68k_006822:
        move.b %d0,(%a0)+
m68k_006822_end:
.org 0x6824
m68k_006824:
        rts
m68k_006824_end:
.org 0x6826
m68k_006826:
        lea.l 0xc00004:l,%a0
m68k_006826_end:
.org 0x682C
m68k_00682c:
        lea.l 0xc00000:l,%a1
m68k_00682c_end:
.org 0x6832
m68k_006832:
        lea.l 116(%pc),%a2
m68k_006832_end:
.org 0x6836
m68k_006836:
        moveq #18,%d7
m68k_006836_end:
.org 0x6838
m68k_006838:
        move.w (%a2)+,(%a0)
m68k_006838_end:
.org 0x683A
m68k_00683a:
        dbra %d7,(. + -2)
m68k_00683a_end:
.org 0x683E
m68k_00683e:
        move.w 106(%pc),0xf606:w
m68k_00683e_end:
.org 0x6844
m68k_006844:
        moveq #0,%d0
m68k_006844_end:
.org 0x6846
m68k_006846:
        move.l #0xc0000000,0xc00004:l
m68k_006846_end:
.org 0x6850
m68k_006850:
        move.w #0x3f,%d7
m68k_006850_end:
.org 0x6854
m68k_006854:
        move.w %d0,(%a1)
m68k_006854_end:
.org 0x6856
m68k_006856:
        dbra %d7,(. + -2)
m68k_006856_end:
.org 0x685A
m68k_00685a:
        lea.l 0xc00004:l,%a6
m68k_00685a_end:
.org 0x6860
m68k_006860:
        move.w #0x8f01,(%a6)
m68k_006860_end:
.org 0x6864
m68k_006864:
        move.w 0xf606:w,%d7
m68k_006864_end:
.org 0x6868
m68k_006868:
        ori.b #0x10,%d7
m68k_006868_end:
.org 0x686C
m68k_00686c:
        move.w %d7,(%a6)
m68k_00686c_end:
.org 0x686E
m68k_00686e:
        move.l #0x93ff94ff,(%a6)
m68k_00686e_end:
.org 0x6874
m68k_006874:
        move.w #0x9780,(%a6)
m68k_006874_end:
.org 0x6878
m68k_006878:
        move.l #0x40000080,(%a6)
m68k_006878_end:
.org 0x687E
m68k_00687e:
        move.w #0x0,0xc00000:l
m68k_00687e_end:
.org 0x6886
m68k_006886:
        move.w (%a6),%d7
m68k_006886_end:
.org 0x6888
m68k_006888:
        andi.w #0x2,%d7
m68k_006888_end:
.org 0x688C
m68k_00688c:
        bne.b (. + -6)
m68k_00688c_end:
.org 0x688E
m68k_00688e:
        tst.b 0xff3f00:l
m68k_00688e_end:
.org 0x6894
m68k_006894:
        bne.b (. + 10)
m68k_006894_end:
.org 0x6896
m68k_006896:
        move.w #0x0,0xa11100:l
m68k_006896_end:
.org 0x689E
m68k_00689e:
        move.w 0xf606:w,(%a6)
m68k_00689e_end:
.org 0x68A2
m68k_0068a2:
        move.w #0x8f02,(%a6)
m68k_0068a2_end:
.org 0x68A6
m68k_0068a6:
        rts
m68k_0068a6_end:
.org 0x68CE
m68k_0068ce:
        lea.l 0xc00004:l,%a6
m68k_0068ce_end:
.org 0x68D4
m68k_0068d4:
        move.w #0x8f01,(%a6)
m68k_0068d4_end:
.org 0x68D8
m68k_0068d8:
        move.w 0xf606:w,%d7
m68k_0068d8_end:
.org 0x68DC
m68k_0068dc:
        ori.b #0x10,%d7
m68k_0068dc_end:
.org 0x68E0
m68k_0068e0:
        move.w %d7,(%a6)
m68k_0068e0_end:
.org 0x68E2
m68k_0068e2:
        move.l #0x93ff9447,(%a6)
m68k_0068e2_end:
.org 0x68E8
m68k_0068e8:
        move.w #0x9780,(%a6)
m68k_0068e8_end:
.org 0x68EC
m68k_0068ec:
        move.l #0x78000082,(%a6)
m68k_0068ec_end:
.org 0x68F2
m68k_0068f2:
        move.w #0xf6,0xc00000:l
m68k_0068f2_end:
.org 0x68FA
m68k_0068fa:
        move.w (%a6),%d7
m68k_0068fa_end:
.org 0x68FC
m68k_0068fc:
        andi.w #0x2,%d7
m68k_0068fc_end:
.org 0x6900
m68k_006900:
        bne.b (. + -6)
m68k_006900_end:
.org 0x6902
m68k_006902:
        tst.b 0xff3f00:l
m68k_006902_end:
.org 0x6908
m68k_006908:
        bne.b (. + 10)
m68k_006908_end:
.org 0x690A
m68k_00690a:
        move.w #0x0,0xa11100:l
m68k_00690a_end:
.org 0x6912
m68k_006912:
        move.w 0xf606:w,(%a6)
m68k_006912_end:
.org 0x6916
m68k_006916:
        move.w #0x8f02,(%a6)
m68k_006916_end:
.org 0x691A
m68k_00691a:
        move.l #0x40000010,0xc00004:l
m68k_00691a_end:
.org 0x6924
m68k_006924:
        move.l #0x0,0xc00000:l
m68k_006924_end:
.org 0x692E
m68k_00692e:
        move.l #0x0,0xf312:w
m68k_00692e_end:
.org 0x6936
m68k_006936:
        move.l #0x0,0xf316:w
m68k_006936_end:
.org 0x693E
m68k_00693e:
        lea.l 0xf800:w,%a6
m68k_00693e_end:
.org 0x6942
m68k_006942:
        moveq #0,%d7
m68k_006942_end:
.org 0x6944
m68k_006944:
        move.w #0x9f,%d6
m68k_006944_end:
.org 0x6948
m68k_006948:
        move.l %d7,(%a6)+
m68k_006948_end:
.org 0x694A
m68k_00694a:
        dbra %d6,(. + -2)
m68k_00694a_end:
.org 0x694E
m68k_00694e:
        rts
m68k_00694e_end:
.org 0x6950
m68k_006950:
        move.w #0x100,0xa11100:l
m68k_006950_end:
.org 0x6958
m68k_006958:
        bsr.w (. + 96)
m68k_006958_end:
.org 0x695C
m68k_00695c:
        btst.b #0x0,0xa11100:l
m68k_00695c_end:
.org 0x6964
m68k_006964:
        bne.b (. + -8)
m68k_006964_end:
.org 0x6966
m68k_006966:
        lea.l 106(%pc),%a0
m68k_006966_end:
.org 0x696A
m68k_00696a:
        nop
m68k_00696a_end:
.org 0x696C
m68k_00696c:
        lea.l 0xa00000:l,%a1
m68k_00696c_end:
.org 0x6972
m68k_006972:
        move.w #0xfff,%d0
m68k_006972_end:
.org 0x6976
m68k_006976:
        move.b (%a0)+,(%a1)+
m68k_006976_end:
.org 0x6978
m68k_006978:
        dbra %d0,(. + -2)
m68k_006978_end:
.org 0x697C
m68k_00697c:
        lea.l 4126(%pc),%a0
m68k_00697c_end:
.org 0x6980
m68k_006980:
        nop
m68k_006980_end:
.org 0x6982
m68k_006982:
        move.w #0xdff,%d0
m68k_006982_end:
.org 0x6986
m68k_006986:
        move.b (%a0)+,(%a1)+
m68k_006986_end:
.org 0x6988
m68k_006988:
        dbra %d0,(. + -2)
m68k_006988_end:
.org 0x698C
m68k_00698c:
        lea.l 28(%pc),%a0
m68k_00698c_end:
.org 0x6990
m68k_006990:
        lea.l 0xa01c00:l,%a1
m68k_006990_end:
.org 0x6996
m68k_006996:
        moveq #12,%d0
m68k_006996_end:
.org 0x6998
m68k_006998:
        move.b (%a0)+,(%a1)+
m68k_006998_end:
.org 0x699A
m68k_00699a:
        dbra %d0,(. + -2)
m68k_00699a_end:
.org 0x699E
m68k_00699e:
        bsr.b (. + 26)
m68k_00699e_end:
.org 0x69A0
m68k_0069a0:
        move.w #0x0,0xa11100:l
m68k_0069a0_end:
.org 0x69A8
m68k_0069a8:
        rts
m68k_0069a8_end:
.org 0x69B8
m68k_0069b8:
        move.w #0x0,0xa11200:l
m68k_0069b8_end:
.org 0x69C0
m68k_0069c0:
        nop
m68k_0069c0_end:
.org 0x69C2
m68k_0069c2:
        nop
m68k_0069c2_end:
.org 0x69C4
m68k_0069c4:
        nop
m68k_0069c4_end:
.org 0x69C6
m68k_0069c6:
        nop
m68k_0069c6_end:
.org 0x69C8
m68k_0069c8:
        move.w #0x100,0xa11200:l
m68k_0069c8_end:
.org 0x69D0
m68k_0069d0:
        rts
m68k_0069d0_end:
.org 0x879C
m68k_00879c:
        lea.l 0xe9f8:w,%a1
m68k_00879c_end:
.org 0x87A0
m68k_0087a0:
        bsr.w (. + 670)
m68k_0087a0_end:
.org 0x87A4
m68k_0087a4:
        lea.l 0xd300:w,%a1
m68k_0087a4_end:
.org 0x87A8
m68k_0087a8:
        move.w #0x6,%d0
m68k_0087a8_end:
.org 0x87AC
m68k_0087ac:
        move.w #0x1,%d1
m68k_0087ac_end:
.org 0x87B0
m68k_0087b0:
        move.w #0x10,%d2
m68k_0087b0_end:
.org 0x87B4
m68k_0087b4:
        bsr.w (. + 2678)
m68k_0087b4_end:
.org 0x87B8
m68k_0087b8:
        lea.l 0xd310:w,%a1
m68k_0087b8_end:
.org 0x87BC
m68k_0087bc:
        move.w #0x6,%d0
m68k_0087bc_end:
.org 0x87C0
m68k_0087c0:
        move.w #0x1,%d1
m68k_0087c0_end:
.org 0x87C4
m68k_0087c4:
        move.w #0x10,%d2
m68k_0087c4_end:
.org 0x87C8
m68k_0087c8:
        bsr.w (. + 2658)
m68k_0087c8_end:
.org 0x87CC
m68k_0087cc:
        lea.l 0xd320:w,%a1
m68k_0087cc_end:
.org 0x87D0
m68k_0087d0:
        move.w #0x8,%d0
m68k_0087d0_end:
.org 0x87D4
m68k_0087d4:
        move.w #0x1,%d1
m68k_0087d4_end:
.org 0x87D8
m68k_0087d8:
        move.w #0x10,%d2
m68k_0087d8_end:
.org 0x87DC
m68k_0087dc:
        bsr.w (. + 2638)
m68k_0087dc_end:
.org 0x87E0
m68k_0087e0:
        lea.l 0xd330:w,%a1
m68k_0087e0_end:
.org 0x87E4
m68k_0087e4:
        move.w #0x4,%d0
m68k_0087e4_end:
.org 0x87E8
m68k_0087e8:
        move.w #0x1,%d1
m68k_0087e8_end:
.org 0x87EC
m68k_0087ec:
        move.w #0x10,%d2
m68k_0087ec_end:
.org 0x87F0
m68k_0087f0:
        bsr.w (. + 2618)
m68k_0087f0_end:
.org 0x87F4
m68k_0087f4:
        lea.l 0xea38:w,%a1
m68k_0087f4_end:
.org 0x87F8
m68k_0087f8:
        move.w #0x1,%d0
m68k_0087f8_end:
.org 0x87FC
m68k_0087fc:
        move.w #0x1,%d1
m68k_0087fc_end:
.org 0x8800
m68k_008800:
        move.w #0x28,%d2
m68k_008800_end:
.org 0x8804
m68k_008804:
        bsr.w (. + 2598)
m68k_008804_end:
.org 0x8808
m68k_008808:
        lea.l 0xea88:w,%a1
m68k_008808_end:
.org 0x880C
m68k_00880c:
        move.w #0x2,%d0
m68k_00880c_end:
.org 0x8810
m68k_008810:
        move.w #0x1,%d1
m68k_008810_end:
.org 0x8814
m68k_008814:
        move.w #0x300,%d2
m68k_008814_end:
.org 0x8818
m68k_008818:
        bsr.w (. + 2578)
m68k_008818_end:
.org 0x881C
m68k_00881c:
        lea.l 0xed88:w,%a1
m68k_00881c_end:
.org 0x8820
m68k_008820:
        move.w #0x12,%d0
m68k_008820_end:
.org 0x8824
m68k_008824:
        move.w #0x4,%d1
m68k_008824_end:
.org 0x8828
m68k_008828:
        move.w #0x28,%d2
m68k_008828_end:
.org 0x882C
m68k_00882c:
        bsr.w (. + 2558)
m68k_00882c_end:
.org 0x8830
m68k_008830:
        lea.l 0xee28:w,%a1
m68k_008830_end:
.org 0x8834
m68k_008834:
        move.w #0x14,%d0
m68k_008834_end:
.org 0x8838
m68k_008838:
        move.w #0x4,%d1
m68k_008838_end:
.org 0x883C
m68k_00883c:
        move.w #0x28,%d2
m68k_00883c_end:
.org 0x8840
m68k_008840:
        bsr.w (. + 2538)
m68k_008840_end:
.org 0x8844
m68k_008844:
        lea.l 0xf590:w,%a1
m68k_008844_end:
.org 0x8848
m68k_008848:
        move.w #0x2,%d0
m68k_008848_end:
.org 0x884C
m68k_00884c:
        move.w #0x1,%d1
m68k_00884c_end:
.org 0x8850
m68k_008850:
        move.w #0x10,%d2
m68k_008850_end:
.org 0x8854
m68k_008854:
        bsr.w (. + 2518)
m68k_008854_end:
.org 0x8858
m68k_008858:
        bsr.w (. + 110)
m68k_008858_end:
.org 0x885C
m68k_00885c:
        bsr.w (. + 234)
m68k_00885c_end:
.org 0x8860
m68k_008860:
        bsr.w (. + 414)
m68k_008860_end:
.org 0x8864
m68k_008864:
        rts
m68k_008864_end:
.org 0x8866
m68k_008866:
        lea.l 0xa150:w,%a2
m68k_008866_end:
.org 0x886A
m68k_00886a:
        lea.l 0xd300:w,%a3
m68k_00886a_end:
.org 0x886E
m68k_00886e:
        lea.l 0xd500:w,%a4
m68k_00886e_end:
.org 0x8872
m68k_008872:
        move.w #0xff,%d0
m68k_008872_end:
.org 0x8876
m68k_008876:
        move.w (%a2)+,%d1
m68k_008876_end:
.org 0x8878
m68k_008878:
        lsr.w #0x7,%d1
m68k_008878_end:
.org 0x887A
m68k_00887a:
        move.w %d1,(%a3)+
m68k_00887a_end:
.org 0x887C
m68k_00887c:
        move.w (%a2)+,%d1
m68k_00887c_end:
.org 0x887E
m68k_00887e:
        lsr.w #0x7,%d1
m68k_00887e_end:
.org 0x8880
m68k_008880:
        move.w %d1,(%a4)+
m68k_008880_end:
.org 0x8882
m68k_008882:
        dbra %d0,(. + -12)
m68k_008882_end:
.org 0x8886
m68k_008886:
        rts
m68k_008886_end:
.org 0x8888
m68k_008888:
        lea.l 0xe818:w,%a1
m68k_008888_end:
.org 0x888C
m68k_00888c:
        lea.l 0xd300:w,%a2
m68k_00888c_end:
.org 0x8890
m68k_008890:
        move.w #0x27,%d0
m68k_008890_end:
.org 0x8894
m68k_008894:
        move.w (%a1)+,(%a2)
m68k_008894_end:
.org 0x8896
m68k_008896:
        move.w (%a1)+,0x50(%a2)
m68k_008896_end:
.org 0x889A
m68k_00889a:
        move.w (%a1)+,0xa0(%a2)
m68k_00889a_end:
.org 0x889E
m68k_00889e:
        move.w (%a1)+,%d1
m68k_00889e_end:
.org 0x88A0
m68k_0088a0:
        cmpi.w #0xffff,%d1
m68k_0088a0_end:
.org 0x88A4
m68k_0088a4:
        beq.w (. + 14)
m68k_0088a4_end:
.org 0x88A8
m68k_0088a8:
        andi.l #0xffff,%d1
m68k_0088a8_end:
.org 0x88AE
m68k_0088ae:
        divu.w #0x64,%d1
m68k_0088ae_end:
.org 0x88B2
m68k_0088b2:
        move.w %d1,0xf0(%a2)
m68k_0088b2_end:
.org 0x88B6
m68k_0088b6:
        move.w (%a1)+,0x140(%a2)
m68k_0088b6_end:
.org 0x88BA
m68k_0088ba:
        move.w (%a1)+,0x190(%a2)
m68k_0088ba_end:
.org 0x88BE
m68k_0088be:
        addq.w #0x2,%a2
m68k_0088be_end:
.org 0x88C0
m68k_0088c0:
        dbra %d0,(. + -44)
m68k_0088c0_end:
.org 0x88C4
m68k_0088c4:
        rts
m68k_0088c4_end:
.org 0x88C6
m68k_0088c6:
        lea.l 0xce00:w,%a1
m68k_0088c6_end:
.org 0x88CA
m68k_0088ca:
        clr.w %d3
m68k_0088ca_end:
.org 0x88CC
m68k_0088cc:
        clr.w %d4
m68k_0088cc_end:
.org 0x88CE
m68k_0088ce:
        move.w #0x27,%d0
m68k_0088ce_end:
.org 0x88D2
m68k_0088d2:
        moveq #0,%d7
m68k_0088d2_end:
.org 0x88D4
m68k_0088d4:
        move.b (%a1)+,%d7
m68k_0088d4_end:
.org 0x88D6
m68k_0088d6:
        andi.w #0x3,%d7
m68k_0088d6_end:
.org 0x88DA
m68k_0088da:
        lsl.w #0x7,%d7
m68k_0088da_end:
.org 0x88DC
m68k_0088dc:
        move.b (%a1)+,%d1
m68k_0088dc_end:
.org 0x88DE
m68k_0088de:
        andi.w #0x7f,%d1
m68k_0088de_end:
.org 0x88E2
m68k_0088e2:
        or.w %d1,%d7
m68k_0088e2_end:
.org 0x88E4
m68k_0088e4:
        lsl.w #0x7,%d7
m68k_0088e4_end:
.org 0x88E6
m68k_0088e6:
        move.b (%a1)+,%d1
m68k_0088e6_end:
.org 0x88E8
m68k_0088e8:
        andi.w #0x7f,%d1
m68k_0088e8_end:
.org 0x88EC
m68k_0088ec:
        or.w %d1,%d7
m68k_0088ec_end:
.org 0x88EE
m68k_0088ee:
        lsl.l #0x6,%d7
m68k_0088ee_end:
.org 0x88F0
m68k_0088f0:
        move.b (%a1)+,%d1
m68k_0088f0_end:
.org 0x88F2
m68k_0088f2:
        andi.w #0x3f,%d1
m68k_0088f2_end:
.org 0x88F6
m68k_0088f6:
        or.w %d1,%d7
m68k_0088f6_end:
.org 0x88F8
m68k_0088f8:
        lsl.l %d4,%d7
m68k_0088f8_end:
.org 0x88FA
m68k_0088fa:
        or.w %d3,%d7
m68k_0088fa_end:
.org 0x88FC
m68k_0088fc:
        addi.w #0x16,%d4
m68k_0088fc_end:
.org 0x8900
m68k_008900:
        cmpi.w #0x8,%d4
m68k_008900_end:
.org 0x8904
m68k_008904:
        bcs.w (. + 18)
m68k_008904_end:
.org 0x8908
m68k_008908:
        move.b %d7,(%a0)+
m68k_008908_end:
.org 0x890A
m68k_00890a:
        lea.l 0x1(%a0),%a0
m68k_00890a_end:
.org 0x890E
m68k_00890e:
        subi.w #0x8,%d4
m68k_00890e_end:
.org 0x8912
m68k_008912:
        lsr.l #0x8,%d7
m68k_008912_end:
.org 0x8914
m68k_008914:
        bra.b (. + -20)
m68k_008914_end:
.org 0x8916
m68k_008916:
        move.w %d7,%d3
m68k_008916_end:
.org 0x8918
m68k_008918:
        dbra %d0,(. + -70)
m68k_008918_end:
.org 0x891C
m68k_00891c:
        tst.w %d4
m68k_00891c_end:
.org 0x891E
m68k_00891e:
        beq.w (. + 10)
m68k_00891e_end:
.org 0x8928
m68k_008928:
        rts
m68k_008928_end:
.org 0x892A
m68k_00892a:
        lea.l 0xb800:w,%a1
m68k_00892a_end:
.org 0x892E
m68k_00892e:
        lea.l 0xd300:w,%a2
m68k_00892e_end:
.org 0x8932
m68k_008932:
        move.w #0xff,%d0
m68k_008932_end:
.org 0x8936
m68k_008936:
        moveq #0,%d1
m68k_008936_end:
.org 0x8938
m68k_008938:
        move.w (%a1)+,%d1
m68k_008938_end:
.org 0x893A
m68k_00893a:
        divu.w #0x5,%d1
m68k_00893a_end:
.org 0x893E
m68k_00893e:
        move.w %d1,(%a2)+
m68k_00893e_end:
.org 0x8940
m68k_008940:
        dbra %d0,(. + -10)
m68k_008940_end:
.org 0x8944
m68k_008944:
        rts
m68k_008944_end:
.org 0x8946
m68k_008946:
        lea.l 0x9000:w,%a1
m68k_008946_end:
.org 0x894A
m68k_00894a:
        moveq #0,%d3
m68k_00894a_end:
.org 0x894C
m68k_00894c:
        clr.w %d4
m68k_00894c_end:
.org 0x894E
m68k_00894e:
        move.b (%a1)+,%d0
m68k_00894e_end:
.org 0x8950
m68k_008950:
        andi.l #0xf,%d0
m68k_008950_end:
.org 0x8956
m68k_008956:
        move.w %d0,%d7
m68k_008956_end:
.org 0x8958
m68k_008958:
        move.w #0x4,%d1
m68k_008958_end:
.org 0x895C
m68k_00895c:
        bsr.w (. + 132)
m68k_00895c_end:
.org 0x8960
m68k_008960:
        tst.w %d7
m68k_008960_end:
.org 0x8962
m68k_008962:
        beq.w (. + 118)
m68k_008962_end:
.org 0x89D8
m68k_0089d8:
        move.b %d3,(%a0)+
m68k_0089d8_end:
.org 0x89DA
m68k_0089da:
        lea.l 0x1(%a0),%a0
m68k_0089da_end:
.org 0x89DE
m68k_0089de:
        rts
m68k_0089de_end:
.org 0x89E0
m68k_0089e0:
        lsl.l %d4,%d0
m68k_0089e0_end:
.org 0x89E2
m68k_0089e2:
        or.w %d3,%d0
m68k_0089e2_end:
.org 0x89E4
m68k_0089e4:
        add.w %d1,%d4
m68k_0089e4_end:
.org 0x89E6
m68k_0089e6:
        cmpi.w #0x8,%d4
m68k_0089e6_end:
.org 0x89EA
m68k_0089ea:
        bcs.w (. + 16)
m68k_0089ea_end:
.org 0x89FA
m68k_0089fa:
        move.w %d0,%d3
m68k_0089fa_end:
.org 0x89FC
m68k_0089fc:
        rts
m68k_0089fc_end:
.org 0x89FE
m68k_0089fe:
        bsr.w (. + 36)
m68k_0089fe_end:
.org 0x8A02
m68k_008a02:
        move.b %d1,0x20010d:l
m68k_008a02_end:
.org 0x8A08
m68k_008a08:
        lsr.l #0x8,%d1
m68k_008a08_end:
.org 0x8A0A
m68k_008a0a:
        move.b %d1,0x20010f:l
m68k_008a0a_end:
.org 0x8A10
m68k_008a10:
        lsr.l #0x8,%d1
m68k_008a10_end:
.org 0x8A12
m68k_008a12:
        move.b %d1,0x200111:l
m68k_008a12_end:
.org 0x8A18
m68k_008a18:
        lsr.w #0x8,%d1
m68k_008a18_end:
.org 0x8A1A
m68k_008a1a:
        move.b %d1,0x200113:l
m68k_008a1a_end:
.org 0x8A20
m68k_008a20:
        rts
m68k_008a20_end:
.org 0x8A22
m68k_008a22:
        lea.l 0x200115:l,%a0
m68k_008a22_end:
.org 0x8A28
m68k_008a28:
        move.w #0x1eec,%d0
m68k_008a28_end:
.org 0x8A2C
m68k_008a2c:
        moveq #0,%d1
m68k_008a2c_end:
.org 0x8A2E
m68k_008a2e:
        moveq #0,%d2
m68k_008a2e_end:
.org 0x8A30
m68k_008a30:
        move.b (%a0)+,%d2
m68k_008a30_end:
.org 0x8A32
m68k_008a32:
        add.l %d2,%d1
m68k_008a32_end:
.org 0x8A34
m68k_008a34:
        lea.l 0x1(%a0),%a0
m68k_008a34_end:
.org 0x8A38
m68k_008a38:
        dbra %d0,(. + -8)
m68k_008a38_end:
.org 0x8A3C
m68k_008a3c:
        rts
m68k_008a3c_end:
.org 0x8A3E
m68k_008a3e:
        lea.l 0xd300:w,%a2
m68k_008a3e_end:
.org 0x8A42
m68k_008a42:
        lea.l 0xd310:w,%a3
m68k_008a42_end:
.org 0x8A46
m68k_008a46:
        lea.l 0xd320:w,%a4
m68k_008a46_end:
.org 0x8A4A
m68k_008a4a:
        lea.l 0xd330:w,%a5
m68k_008a4a_end:
.org 0x8A4E
m68k_008a4e:
        move.w #0xf,%d0
m68k_008a4e_end:
.org 0x8A52
m68k_008a52:
        move.b (%a1)+,(%a2)+
m68k_008a52_end:
.org 0x8A54
m68k_008a54:
        move.b (%a1)+,(%a3)+
m68k_008a54_end:
.org 0x8A56
m68k_008a56:
        move.b (%a1)+,(%a4)+
m68k_008a56_end:
.org 0x8A58
m68k_008a58:
        move.b (%a1)+,(%a5)+
m68k_008a58_end:
.org 0x8A5A
m68k_008a5a:
        dbra %d0,(. + -8)
m68k_008a5a_end:
.org 0x8A5E
m68k_008a5e:
        rts
m68k_008a5e_end:
.org 0x8A60
m68k_008a60:
        bsr.w (. + 1656)
m68k_008a60_end:
.org 0x8A64
m68k_008a64:
        bcs.w (. + 1156)
m68k_008a64_end:
.org 0x8A68
m68k_008a68:
        clr.w 0xf67a:w
m68k_008a68_end:
.org 0x8A6C
m68k_008a6c:
        move.b 0x200115:l,0xf67b:w
m68k_008a6c_end:
.org 0x8A74
m68k_008a74:
        clr.w 0xf67c:w
m68k_008a74_end:
.org 0x8A78
m68k_008a78:
        move.b 0x200117:l,0xf67d:w
m68k_008a78_end:
.org 0x8A80
m68k_008a80:
        clr.w 0xf67e:w
m68k_008a80_end:
.org 0x8A84
m68k_008a84:
        move.b 0x200119:l,0xf67f:w
m68k_008a84_end:
.org 0x8A8C
m68k_008a8c:
        move.b 0x20011b:l,0xf374:w
m68k_008a8c_end:
.org 0x8A94
m68k_008a94:
        move.b 0x20011d:l,0xf375:w
m68k_008a94_end:
.org 0x8A9C
m68k_008a9c:
        clr.w 0xefd2:w
m68k_008a9c_end:
.org 0x8AA0
m68k_008aa0:
        move.b 0x20011f:l,0xefd3:w
m68k_008aa0_end:
.org 0x8AA8
m68k_008aa8:
        clr.w 0xefe4:w
m68k_008aa8_end:
.org 0x8AAC
m68k_008aac:
        move.b 0x200121:l,0xefe5:w
m68k_008aac_end:
.org 0x8AB4
m68k_008ab4:
        clr.w 0xefd6:w
m68k_008ab4_end:
.org 0x8AB8
m68k_008ab8:
        move.b 0x200123:l,0xefd7:w
m68k_008ab8_end:
.org 0x8AC0
m68k_008ac0:
        clr.w 0xefd8:w
m68k_008ac0_end:
.org 0x8AC4
m68k_008ac4:
        move.b 0x200125:l,0xefd9:w
m68k_008ac4_end:
.org 0x8ACC
m68k_008acc:
        movea.l #0x200127,%a0
m68k_008acc_end:
.org 0x8AD2
m68k_008ad2:
        lea.l 0xa000:w,%a1
m68k_008ad2_end:
.org 0x8AD6
m68k_008ad6:
        move.w #0x5,%d0
m68k_008ad6_end:
.org 0x8ADA
m68k_008ada:
        move.w #0x1,%d1
m68k_008ada_end:
.org 0x8ADE
m68k_008ade:
        move.w #0x28,%d2
m68k_008ade_end:
.org 0x8AE2
m68k_008ae2:
        bsr.w (. + 2108)
m68k_008ae2_end:
.org 0x8AE6
m68k_008ae6:
        lea.l 0xefaa:w,%a1
m68k_008ae6_end:
.org 0x8AEA
m68k_008aea:
        move.b (%a0)+,(%a1)+
m68k_008aea_end:
.org 0x8AEC
m68k_008aec:
        lea.l 0x1(%a0),%a0
m68k_008aec_end:
.org 0x8AF0
m68k_008af0:
        move.b (%a0)+,(%a1)+
m68k_008af0_end:
.org 0x8AF2
m68k_008af2:
        lea.l 0x1(%a0),%a0
m68k_008af2_end:
.org 0x8AF6
m68k_008af6:
        move.b (%a0)+,(%a1)+
m68k_008af6_end:
.org 0x8AF8
m68k_008af8:
        lea.l 0x1(%a0),%a0
m68k_008af8_end:
.org 0x8AFC
m68k_008afc:
        move.b (%a0)+,(%a1)+
m68k_008afc_end:
.org 0x8AFE
m68k_008afe:
        lea.l 0x1(%a0),%a0
m68k_008afe_end:
.org 0x8B02
m68k_008b02:
        move.b (%a0)+,(%a1)+
m68k_008b02_end:
.org 0x8B04
m68k_008b04:
        lea.l 0x1(%a0),%a0
m68k_008b04_end:
.org 0x8B08
m68k_008b08:
        lea.l 0xa028:w,%a1
m68k_008b08_end:
.org 0x8B0C
m68k_008b0c:
        move.w #0x8,%d0
m68k_008b0c_end:
.org 0x8B10
m68k_008b10:
        move.w #0x1,%d1
m68k_008b10_end:
.org 0x8B14
m68k_008b14:
        move.w #0x28,%d2
m68k_008b14_end:
.org 0x8B18
m68k_008b18:
        bsr.w (. + 2054)
m68k_008b18_end:
.org 0x8B1C
m68k_008b1c:
        lea.l 0xa050:w,%a1
m68k_008b1c_end:
.org 0x8B20
m68k_008b20:
        move.w #0x8,%d0
m68k_008b20_end:
.org 0x8B24
m68k_008b24:
        move.w #0x1,%d1
m68k_008b24_end:
.org 0x8B28
m68k_008b28:
        move.w #0x100,%d2
m68k_008b28_end:
.org 0x8B2C
m68k_008b2c:
        bsr.w (. + 2034)
m68k_008b2c_end:
.org 0x8B30
m68k_008b30:
        lea.l 0xd300:w,%a1
m68k_008b30_end:
.org 0x8B34
m68k_008b34:
        move.w #0x8,%d0
m68k_008b34_end:
.org 0x8B38
m68k_008b38:
        move.w #0x2,%d1
m68k_008b38_end:
.org 0x8B3C
m68k_008b3c:
        move.w #0x100,%d2
m68k_008b3c_end:
.org 0x8B40
m68k_008b40:
        bsr.w (. + 2014)
m68k_008b40_end:
.org 0x8B44
m68k_008b44:
        lea.l 0xd500:w,%a1
m68k_008b44_end:
.org 0x8B48
m68k_008b48:
        move.w #0x9,%d0
m68k_008b48_end:
.org 0x8B4C
m68k_008b4c:
        move.w #0x2,%d1
m68k_008b4c_end:
.org 0x8B50
m68k_008b50:
        move.w #0x100,%d2
m68k_008b50_end:
.org 0x8B54
m68k_008b54:
        bsr.w (. + 1994)
m68k_008b54_end:
.org 0x8B58
m68k_008b58:
        bsr.w (. + 914)
m68k_008b58_end:
.org 0x8B5C
m68k_008b5c:
        lea.l 0xb200:w,%a1
m68k_008b5c_end:
.org 0x8B60
m68k_008b60:
        move.w #0x8,%d0
m68k_008b60_end:
.org 0x8B64
m68k_008b64:
        move.w #0x2,%d1
m68k_008b64_end:
.org 0x8B68
m68k_008b68:
        move.w #0x100,%d2
m68k_008b68_end:
.org 0x8B6C
m68k_008b6c:
        bsr.w (. + 1970)
m68k_008b6c_end:
.org 0x8B70
m68k_008b70:
        lea.l 0xb400:w,%a1
m68k_008b70_end:
.org 0x8B74
m68k_008b74:
        move.w #0x8,%d0
m68k_008b74_end:
.org 0x8B78
m68k_008b78:
        move.w #0x2,%d1
m68k_008b78_end:
.org 0x8B7C
m68k_008b7c:
        move.w #0x100,%d2
m68k_008b7c_end:
.org 0x8B80
m68k_008b80:
        bsr.w (. + 1950)
m68k_008b80_end:
.org 0x8B84
m68k_008b84:
        lea.l 0xb600:w,%a1
m68k_008b84_end:
.org 0x8B88
m68k_008b88:
        move.w #0x8,%d0
m68k_008b88_end:
.org 0x8B8C
m68k_008b8c:
        move.w #0x2,%d1
m68k_008b8c_end:
.org 0x8B90
m68k_008b90:
        move.w #0x100,%d2
m68k_008b90_end:
.org 0x8B94
m68k_008b94:
        bsr.w (. + 1930)
m68k_008b94_end:
.org 0x8B98
m68k_008b98:
        lea.l 0xd300:w,%a1
m68k_008b98_end:
.org 0x8B9C
m68k_008b9c:
        move.w #0x5,%d0
m68k_008b9c_end:
.org 0x8BA0
m68k_008ba0:
        move.w #0x2,%d1
m68k_008ba0_end:
.org 0x8BA4
m68k_008ba4:
        move.w #0x100,%d2
m68k_008ba4_end:
.org 0x8BA8
m68k_008ba8:
        bsr.w (. + 1910)
m68k_008ba8_end:
.org 0x8BAC
m68k_008bac:
        bsr.w (. + 1136)
m68k_008bac_end:
.org 0x8BB0
m68k_008bb0:
        lea.l 0xc000:w,%a1
m68k_008bb0_end:
.org 0x8BB4
m68k_008bb4:
        move.w #0xa,%d0
m68k_008bb4_end:
.org 0x8BB8
m68k_008bb8:
        move.w #0x2,%d1
m68k_008bb8_end:
.org 0x8BBC
m68k_008bbc:
        move.w #0x100,%d2
m68k_008bbc_end:
.org 0x8BC0
m68k_008bc0:
        bsr.w (. + 1886)
m68k_008bc0_end:
.org 0x8BC4
m68k_008bc4:
        lea.l 0xbe00:w,%a1
m68k_008bc4_end:
.org 0x8BC8
m68k_008bc8:
        move.w #0xa,%d0
m68k_008bc8_end:
.org 0x8BCC
m68k_008bcc:
        move.w #0x2,%d1
m68k_008bcc_end:
.org 0x8BD0
m68k_008bd0:
        move.w #0x100,%d2
m68k_008bd0_end:
.org 0x8BD4
m68k_008bd4:
        bsr.w (. + 1866)
m68k_008bd4_end:
.org 0x8BD8
m68k_008bd8:
        lea.l 0xc200:w,%a1
m68k_008bd8_end:
.org 0x8BDC
m68k_008bdc:
        move.w #0x7,%d0
m68k_008bdc_end:
.org 0x8BE0
m68k_008be0:
        move.w #0x1,%d1
m68k_008be0_end:
.org 0x8BE4
m68k_008be4:
        move.w #0x100,%d2
m68k_008be4_end:
.org 0x8BE8
m68k_008be8:
        bsr.w (. + 1846)
m68k_008be8_end:
.org 0x8BEC
m68k_008bec:
        lea.l 0xc300:w,%a1
m68k_008bec_end:
.org 0x8BF0
m68k_008bf0:
        move.w #0x7,%d0
m68k_008bf0_end:
.org 0x8BF4
m68k_008bf4:
        move.w #0x1,%d1
m68k_008bf4_end:
.org 0x8BF8
m68k_008bf8:
        move.w #0x100,%d2
m68k_008bf8_end:
.org 0x8BFC
m68k_008bfc:
        bsr.w (. + 1826)
m68k_008bfc_end:
.org 0x8C00
m68k_008c00:
        lea.l 0xc400:w,%a1
m68k_008c00_end:
.org 0x8C04
m68k_008c04:
        move.w #0x5,%d0
m68k_008c04_end:
.org 0x8C08
m68k_008c08:
        move.w #0x1,%d1
m68k_008c08_end:
.org 0x8C0C
m68k_008c0c:
        move.w #0x100,%d2
m68k_008c0c_end:
.org 0x8C10
m68k_008c10:
        bsr.w (. + 1806)
m68k_008c10_end:
.org 0x8C14
m68k_008c14:
        lea.l 0xc500:w,%a1
m68k_008c14_end:
.org 0x8C18
m68k_008c18:
        move.w #0x7,%d0
m68k_008c18_end:
.org 0x8C1C
m68k_008c1c:
        move.w #0x1,%d1
m68k_008c1c_end:
.org 0x8C20
m68k_008c20:
        move.w #0x100,%d2
m68k_008c20_end:
.org 0x8C24
m68k_008c24:
        bsr.w (. + 1786)
m68k_008c24_end:
.org 0x8C28
m68k_008c28:
        lea.l 0xc700:w,%a1
m68k_008c28_end:
.org 0x8C2C
m68k_008c2c:
        move.w #0x5,%d0
m68k_008c2c_end:
.org 0x8C30
m68k_008c30:
        move.w #0x1,%d1
m68k_008c30_end:
.org 0x8C34
m68k_008c34:
        move.w #0x100,%d2
m68k_008c34_end:
.org 0x8C38
m68k_008c38:
        bsr.w (. + 1766)
m68k_008c38_end:
.org 0x8C3C
m68k_008c3c:
        lea.l 0xc800:w,%a1
m68k_008c3c_end:
.org 0x8C40
m68k_008c40:
        move.w #0xe,%d0
m68k_008c40_end:
.org 0x8C44
m68k_008c44:
        move.w #0x4,%d1
m68k_008c44_end:
.org 0x8C48
m68k_008c48:
        move.w #0x100,%d2
m68k_008c48_end:
.org 0x8C4C
m68k_008c4c:
        bsr.w (. + 1746)
m68k_008c4c_end:
.org 0x8C50
m68k_008c50:
        lea.l 0xcc00:w,%a1
m68k_008c50_end:
.org 0x8C54
m68k_008c54:
        move.w #0x8,%d0
m68k_008c54_end:
.org 0x8C58
m68k_008c58:
        move.w #0x1,%d1
m68k_008c58_end:
.org 0x8C5C
m68k_008c5c:
        move.w #0x100,%d2
m68k_008c5c_end:
.org 0x8C60
m68k_008c60:
        bsr.w (. + 1726)
m68k_008c60_end:
.org 0x8C64
m68k_008c64:
        lea.l 0xe000:w,%a1
m68k_008c64_end:
.org 0x8C68
m68k_008c68:
        move.w #0x14,%d0
m68k_008c68_end:
.org 0x8C6C
m68k_008c6c:
        move.w #0x4,%d1
m68k_008c6c_end:
.org 0x8C70
m68k_008c70:
        move.w #0x28,%d2
m68k_008c70_end:
.org 0x8C74
m68k_008c74:
        bsr.w (. + 1706)
m68k_008c74_end:
.org 0x8C78
m68k_008c78:
        lea.l 0xe0a0:w,%a1
m68k_008c78_end:
.org 0x8C7C
m68k_008c7c:
        move.w #0x14,%d0
m68k_008c7c_end:
.org 0x8C80
m68k_008c80:
        move.w #0x4,%d1
m68k_008c80_end:
.org 0x8C84
m68k_008c84:
        move.w #0x28,%d2
m68k_008c84_end:
.org 0x8C88
m68k_008c88:
        bsr.w (. + 1686)
m68k_008c88_end:
.org 0x8C8C
m68k_008c8c:
        lea.l 0xe140:w,%a1
m68k_008c8c_end:
.org 0x8C90
m68k_008c90:
        move.w #0xa,%d0
m68k_008c90_end:
.org 0x8C94
m68k_008c94:
        move.w #0x4,%d1
m68k_008c94_end:
.org 0x8C98
m68k_008c98:
        move.w #0x28,%d2
m68k_008c98_end:
.org 0x8C9C
m68k_008c9c:
        bsr.w (. + 1666)
m68k_008c9c_end:
.org 0x8CA0
m68k_008ca0:
        lea.l 0xe1e0:w,%a1
m68k_008ca0_end:
.org 0x8CA4
m68k_008ca4:
        move.w #0xa,%d0
m68k_008ca4_end:
.org 0x8CA8
m68k_008ca8:
        move.w #0x4,%d1
m68k_008ca8_end:
.org 0x8CAC
m68k_008cac:
        move.w #0x28,%d2
m68k_008cac_end:
.org 0x8CB0
m68k_008cb0:
        bsr.w (. + 1646)
m68k_008cb0_end:
.org 0x8CB4
m68k_008cb4:
        lea.l 0xe280:w,%a1
m68k_008cb4_end:
.org 0x8CB8
m68k_008cb8:
        move.w #0x7,%d0
m68k_008cb8_end:
.org 0x8CBC
m68k_008cbc:
        move.w #0x4,%d1
m68k_008cbc_end:
.org 0x8CC0
m68k_008cc0:
        move.w #0x28,%d2
m68k_008cc0_end:
.org 0x8CC4
m68k_008cc4:
        bsr.w (. + 1626)
m68k_008cc4_end:
.org 0x8CC8
m68k_008cc8:
        lea.l 0xe320:w,%a1
m68k_008cc8_end:
.org 0x8CCC
m68k_008ccc:
        move.w #0x7,%d0
m68k_008ccc_end:
.org 0x8CD0
m68k_008cd0:
        move.w #0x4,%d1
m68k_008cd0_end:
.org 0x8CD4
m68k_008cd4:
        move.w #0x28,%d2
m68k_008cd4_end:
.org 0x8CD8
m68k_008cd8:
        bsr.w (. + 1606)
m68k_008cd8_end:
.org 0x8CDC
m68k_008cdc:
        lea.l 0xe3c0:w,%a1
m68k_008cdc_end:
.org 0x8CE0
m68k_008ce0:
        move.w #0x7,%d0
m68k_008ce0_end:
.org 0x8CE4
m68k_008ce4:
        move.w #0x4,%d1
m68k_008ce4_end:
.org 0x8CE8
m68k_008ce8:
        move.w #0x28,%d2
m68k_008ce8_end:
.org 0x8CEC
m68k_008cec:
        bsr.w (. + 1586)
m68k_008cec_end:
.org 0x8CF0
m68k_008cf0:
        lea.l 0xe5a0:w,%a1
m68k_008cf0_end:
.org 0x8CF4
m68k_008cf4:
        move.w #0x7,%d0
m68k_008cf4_end:
.org 0x8CF8
m68k_008cf8:
        move.w #0x4,%d1
m68k_008cf8_end:
.org 0x8CFC
m68k_008cfc:
        move.w #0x28,%d2
m68k_008cfc_end:
.org 0x8D00
m68k_008d00:
        bsr.w (. + 1566)
m68k_008d00_end:
.org 0x8D04
m68k_008d04:
        lea.l 0xf428:w,%a1
m68k_008d04_end:
.org 0x8D08
m68k_008d08:
        move.w #0x4,%d0
m68k_008d08_end:
.org 0x8D0C
m68k_008d0c:
        move.w #0x1,%d1
m68k_008d0c_end:
.org 0x8D10
m68k_008d10:
        move.w #0x28,%d2
m68k_008d10_end:
.org 0x8D14
m68k_008d14:
        bsr.w (. + 1546)
m68k_008d14_end:
.org 0x8D18
m68k_008d18:
        bsr.w (. + 1132)
m68k_008d18_end:
.org 0x8D1C
m68k_008d1c:
        lea.l 0xe640:w,%a1
m68k_008d1c_end:
.org 0x8D20
m68k_008d20:
        move.w #0x9,%d0
m68k_008d20_end:
.org 0x8D24
m68k_008d24:
        move.w #0x2,%d1
m68k_008d24_end:
.org 0x8D28
m68k_008d28:
        move.w #0x10,%d2
m68k_008d28_end:
.org 0x8D2C
m68k_008d2c:
        bsr.w (. + 1522)
m68k_008d2c_end:
.org 0x8D30
m68k_008d30:
        bsr.w (. + 1048)
m68k_008d30_end:
.org 0x8D34
m68k_008d34:
        lea.l 0xf460:w,%a1
m68k_008d34_end:
.org 0x8D38
m68k_008d38:
        move.w #0x9,%d0
m68k_008d38_end:
.org 0x8D3C
m68k_008d3c:
        move.w #0x2,%d1
m68k_008d3c_end:
.org 0x8D40
m68k_008d40:
        move.w #0x28,%d2
m68k_008d40_end:
.org 0x8D44
m68k_008d44:
        bsr.w (. + 1498)
m68k_008d44_end:
.org 0x8D48
m68k_008d48:
        bsr.w (. + 1054)
m68k_008d48_end:
.org 0x8D4C
m68k_008d4c:
        lea.l 0xe660:w,%a1
m68k_008d4c_end:
.org 0x8D50
m68k_008d50:
        move.w #0x14,%d0
m68k_008d50_end:
.org 0x8D54
m68k_008d54:
        move.w #0x4,%d1
m68k_008d54_end:
.org 0x8D58
m68k_008d58:
        move.w #0x28,%d2
m68k_008d58_end:
.org 0x8D5C
m68k_008d5c:
        bsr.w (. + 1474)
m68k_008d5c_end:
.org 0x8D60
m68k_008d60:
        move.b (%a0)+,0xe700:w
m68k_008d60_end:
.org 0x8D64
m68k_008d64:
        lea.l 0x1(%a0),%a0
m68k_008d64_end:
.org 0x8D68
m68k_008d68:
        move.b (%a0)+,0xe701:w
m68k_008d68_end:
.org 0x8D6C
m68k_008d6c:
        lea.l 0x1(%a0),%a0
m68k_008d6c_end:
.org 0x8D70
m68k_008d70:
        lea.l 0xe710:w,%a1
m68k_008d70_end:
.org 0x8D74
m68k_008d74:
        move.w #0x1f,%d2
m68k_008d74_end:
.org 0x8D78
m68k_008d78:
        move.b (%a0)+,(%a1)+
m68k_008d78_end:
.org 0x8D7A
m68k_008d7a:
        lea.l 0x1(%a0),%a0
m68k_008d7a_end:
.org 0x8D7E
m68k_008d7e:
        dbra %d2,(. + -6)
m68k_008d7e_end:
.org 0x8D82
m68k_008d82:
        lea.l 0xe778:w,%a1
m68k_008d82_end:
.org 0x8D86
m68k_008d86:
        move.w #0x11,%d0
m68k_008d86_end:
.org 0x8D8A
m68k_008d8a:
        move.w #0x4,%d1
m68k_008d8a_end:
.org 0x8D8E
m68k_008d8e:
        move.w #0x28,%d2
m68k_008d8e_end:
.org 0x8D92
m68k_008d92:
        bsr.w (. + 1420)
m68k_008d92_end:
.org 0x8D96
m68k_008d96:
        lea.l 0xd300:w,%a1
m68k_008d96_end:
.org 0x8D9A
m68k_008d9a:
        move.w #0x9,%d0
m68k_008d9a_end:
.org 0x8D9E
m68k_008d9e:
        move.w #0x2,%d1
m68k_008d9e_end:
.org 0x8DA2
m68k_008da2:
        move.w #0x28,%d2
m68k_008da2_end:
.org 0x8DA6
m68k_008da6:
        bsr.w (. + 1400)
m68k_008da6_end:
.org 0x8DAA
m68k_008daa:
        lea.l 0xd350:w,%a1
m68k_008daa_end:
.org 0x8DAE
m68k_008dae:
        move.w #0xe,%d0
m68k_008dae_end:
.org 0x8DB2
m68k_008db2:
        move.w #0x2,%d1
m68k_008db2_end:
.org 0x8DB6
m68k_008db6:
        move.w #0x28,%d2
m68k_008db6_end:
.org 0x8DBA
m68k_008dba:
        bsr.w (. + 1380)
m68k_008dba_end:
.org 0x8DBE
m68k_008dbe:
        lea.l 0xd3a0:w,%a1
m68k_008dbe_end:
.org 0x8DC2
m68k_008dc2:
        move.w #0x9,%d0
m68k_008dc2_end:
.org 0x8DC6
m68k_008dc6:
        move.w #0x2,%d1
m68k_008dc6_end:
.org 0x8DCA
m68k_008dca:
        move.w #0x28,%d2
m68k_008dca_end:
.org 0x8DCE
m68k_008dce:
        bsr.w (. + 1360)
m68k_008dce_end:
.org 0x8DD2
m68k_008dd2:
        lea.l 0xd3f0:w,%a1
m68k_008dd2_end:
.org 0x8DD6
m68k_008dd6:
        move.w #0x7,%d0
m68k_008dd6_end:
.org 0x8DDA
m68k_008dda:
        move.w #0x2,%d1
m68k_008dda_end:
.org 0x8DDE
m68k_008dde:
        move.w #0x28,%d2
m68k_008dde_end:
.org 0x8DE2
m68k_008de2:
        bsr.w (. + 1340)
m68k_008de2_end:
.org 0x8DE6
m68k_008de6:
        lea.l 0xd440:w,%a1
m68k_008de6_end:
.org 0x8DEA
m68k_008dea:
        move.w #0x9,%d0
m68k_008dea_end:
.org 0x8DEE
m68k_008dee:
        move.w #0x2,%d1
m68k_008dee_end:
.org 0x8DF2
m68k_008df2:
        move.w #0x28,%d2
m68k_008df2_end:
.org 0x8DF6
m68k_008df6:
        bsr.w (. + 1320)
m68k_008df6_end:
.org 0x8DFA
m68k_008dfa:
        lea.l 0xd490:w,%a1
m68k_008dfa_end:
.org 0x8DFE
m68k_008dfe:
        move.w #0xa,%d0
m68k_008dfe_end:
.org 0x8E02
m68k_008e02:
        move.w #0x2,%d1
m68k_008e02_end:
.org 0x8E06
m68k_008e06:
        move.w #0x28,%d2
m68k_008e06_end:
.org 0x8E0A
m68k_008e0a:
        bsr.w (. + 1300)
m68k_008e0a_end:
.org 0x8E0E
m68k_008e0e:
        bsr.w (. + 254)
m68k_008e0e_end:
.org 0x8E12
m68k_008e12:
        lea.l 0xd300:w,%a1
m68k_008e12_end:
.org 0x8E16
m68k_008e16:
        move.w #0x6,%d0
m68k_008e16_end:
.org 0x8E1A
m68k_008e1a:
        move.w #0x1,%d1
m68k_008e1a_end:
.org 0x8E1E
m68k_008e1e:
        move.w #0x10,%d2
m68k_008e1e_end:
.org 0x8E22
m68k_008e22:
        bsr.w (. + 1276)
m68k_008e22_end:
.org 0x8E26
m68k_008e26:
        lea.l 0xd310:w,%a1
m68k_008e26_end:
.org 0x8E2A
m68k_008e2a:
        move.w #0x6,%d0
m68k_008e2a_end:
.org 0x8E2E
m68k_008e2e:
        move.w #0x1,%d1
m68k_008e2e_end:
.org 0x8E32
m68k_008e32:
        move.w #0x10,%d2
m68k_008e32_end:
.org 0x8E36
m68k_008e36:
        bsr.w (. + 1256)
m68k_008e36_end:
.org 0x8E3A
m68k_008e3a:
        lea.l 0xd320:w,%a1
m68k_008e3a_end:
.org 0x8E3E
m68k_008e3e:
        move.w #0x8,%d0
m68k_008e3e_end:
.org 0x8E42
m68k_008e42:
        move.w #0x1,%d1
m68k_008e42_end:
.org 0x8E46
m68k_008e46:
        move.w #0x10,%d2
m68k_008e46_end:
.org 0x8E4A
m68k_008e4a:
        bsr.w (. + 1236)
m68k_008e4a_end:
.org 0x8E4E
m68k_008e4e:
        lea.l 0xd330:w,%a1
m68k_008e4e_end:
.org 0x8E52
m68k_008e52:
        move.w #0x4,%d0
m68k_008e52_end:
.org 0x8E56
m68k_008e56:
        move.w #0x1,%d1
m68k_008e56_end:
.org 0x8E5A
m68k_008e5a:
        move.w #0x10,%d2
m68k_008e5a_end:
.org 0x8E5E
m68k_008e5e:
        bsr.w (. + 1216)
m68k_008e5e_end:
.org 0x8E62
m68k_008e62:
        lea.l 0xe9f8:w,%a1
m68k_008e62_end:
.org 0x8E66
m68k_008e66:
        bsr.w (. + 828)
m68k_008e66_end:
.org 0x8E6A
m68k_008e6a:
        lea.l 0xea38:w,%a1
m68k_008e6a_end:
.org 0x8E6E
m68k_008e6e:
        move.w #0x1,%d0
m68k_008e6e_end:
.org 0x8E72
m68k_008e72:
        move.w #0x1,%d1
m68k_008e72_end:
.org 0x8E76
m68k_008e76:
        move.w #0x28,%d2
m68k_008e76_end:
.org 0x8E7A
m68k_008e7a:
        bsr.w (. + 1188)
m68k_008e7a_end:
.org 0x8E7E
m68k_008e7e:
        lea.l 0xea88:w,%a1
m68k_008e7e_end:
.org 0x8E82
m68k_008e82:
        move.w #0x2,%d0
m68k_008e82_end:
.org 0x8E86
m68k_008e86:
        move.w #0x1,%d1
m68k_008e86_end:
.org 0x8E8A
m68k_008e8a:
        move.w #0x300,%d2
m68k_008e8a_end:
.org 0x8E8E
m68k_008e8e:
        bsr.w (. + 1168)
m68k_008e8e_end:
.org 0x8E92
m68k_008e92:
        lea.l 0xed88:w,%a1
m68k_008e92_end:
.org 0x8E96
m68k_008e96:
        move.w #0x12,%d0
m68k_008e96_end:
.org 0x8E9A
m68k_008e9a:
        move.w #0x4,%d1
m68k_008e9a_end:
.org 0x8E9E
m68k_008e9e:
        move.w #0x28,%d2
m68k_008e9e_end:
.org 0x8EA2
m68k_008ea2:
        bsr.w (. + 1148)
m68k_008ea2_end:
.org 0x8EA6
m68k_008ea6:
        lea.l 0xee28:w,%a1
m68k_008ea6_end:
.org 0x8EAA
m68k_008eaa:
        move.w #0x14,%d0
m68k_008eaa_end:
.org 0x8EAE
m68k_008eae:
        move.w #0x4,%d1
m68k_008eae_end:
.org 0x8EB2
m68k_008eb2:
        move.w #0x28,%d2
m68k_008eb2_end:
.org 0x8EB6
m68k_008eb6:
        bsr.w (. + 1128)
m68k_008eb6_end:
.org 0x8EBA
m68k_008eba:
        lea.l 0xf590:w,%a1
m68k_008eba_end:
.org 0x8EBE
m68k_008ebe:
        move.w #0x2,%d0
m68k_008ebe_end:
.org 0x8EC2
m68k_008ec2:
        move.w #0x1,%d1
m68k_008ec2_end:
.org 0x8EC6
m68k_008ec6:
        move.w #0x10,%d2
m68k_008ec6_end:
.org 0x8ECA
m68k_008eca:
        bsr.w (. + 1108)
m68k_008eca_end:
.org 0x8ECE
m68k_008ece:
        bsr.w (. + 230)
m68k_008ece_end:
.org 0x8ED2
m68k_008ed2:
        bsr.w (. + 356)
m68k_008ed2_end:
.org 0x8ED6
m68k_008ed6:
        move.w #0xffff,0xff3000:l
m68k_008ed6_end:
.org 0x8EDE
m68k_008ede:
        clr.w 0xf776:w
m68k_008ede_end:
.org 0x8EE2
m68k_008ee2:
        addq.w #0x1,0xaffe:w
m68k_008ee2_end:
.org 0x8EE6
m68k_008ee6:
        rts
m68k_008ee6_end:
.org 0x8EE8
m68k_008ee8:
        rts
m68k_008ee8_end:
.org 0x90D8
m68k_0090d8:
        cmpi.b #0x53,0x200105:l
m68k_0090d8_end:
.org 0x90E0
m68k_0090e0:
        bne.w (. + 98)
m68k_0090e0_end:
.org 0x90E4
m68k_0090e4:
        cmpi.b #0x45,0x200107:l
m68k_0090e4_end:
.org 0x90EC
m68k_0090ec:
        bne.w (. + 86)
m68k_0090ec_end:
.org 0x90F0
m68k_0090f0:
        cmpi.b #0x47,0x200109:l
m68k_0090f0_end:
.org 0x90F8
m68k_0090f8:
        bne.w (. + 74)
m68k_0090f8_end:
.org 0x90FC
m68k_0090fc:
        cmpi.b #0x41,0x20010b:l
m68k_0090fc_end:
.org 0x9104
m68k_009104:
        bne.w (. + 62)
m68k_009104_end:
.org 0x9108
m68k_009108:
        bsr.w (. + -1766)
m68k_009108_end:
.org 0x910C
m68k_00910c:
        cmp.b 0x20010d:l,%d1
m68k_00910c_end:
.org 0x9112
m68k_009112:
        bne.w (. + 48)
m68k_009112_end:
.org 0x9116
m68k_009116:
        lsr.l #0x8,%d1
m68k_009116_end:
.org 0x9118
m68k_009118:
        cmp.b 0x20010f:l,%d1
m68k_009118_end:
.org 0x911E
m68k_00911e:
        bne.w (. + 36)
m68k_00911e_end:
.org 0x9122
m68k_009122:
        lsr.l #0x8,%d1
m68k_009122_end:
.org 0x9124
m68k_009124:
        cmp.b 0x200111:l,%d1
m68k_009124_end:
.org 0x912A
m68k_00912a:
        bne.w (. + 24)
m68k_00912a_end:
.org 0x912E
m68k_00912e:
        lsr.w #0x8,%d1
m68k_00912e_end:
.org 0x9130
m68k_009130:
        cmp.b 0x200113:l,%d1
m68k_009130_end:
.org 0x9136
m68k_009136:
        bne.w (. + 12)
m68k_009136_end:
.org 0x913A
m68k_00913a:
        andi.w #0xfffe,%sr
m68k_00913a_end:
.org 0x913E
m68k_00913e:
        bra.w (. + 8)
m68k_00913e_end:
.org 0x9142
m68k_009142:
        ori.w #0x1,%sr
m68k_009142_end:
.org 0x9146
m68k_009146:
        rts
m68k_009146_end:
.org 0x922A
m68k_00922a:
        subq.w #0x1,%d2
m68k_00922a_end:
.org 0x922C
m68k_00922c:
        clr.w %d3
m68k_00922c_end:
.org 0x922E
m68k_00922e:
        clr.w %d4
m68k_00922e_end:
.org 0x9230
m68k_009230:
        lea.l 104(%pc),%a2
m68k_009230_end:
.org 0x9234
m68k_009234:
        move.w %d0,%d5
m68k_009234_end:
.org 0x9236
m68k_009236:
        lsl.w #0x2,%d5
m68k_009236_end:
.org 0x9238
m68k_009238:
        move.l (%a2, %d5.w),%d5
m68k_009238_end:
.org 0x923C
m68k_00923c:
        moveq #0,%d7
m68k_00923c_end:
.org 0x923E
m68k_00923e:
        move.w %d1,%d6
m68k_00923e_end:
.org 0x9240
m68k_009240:
        tst.w %d6
m68k_009240_end:
.org 0x9242
m68k_009242:
        beq.w (. + 40)
m68k_009242_end:
.org 0x9246
m68k_009246:
        cmpi.w #0x4,%d6
m68k_009246_end:
.org 0x924A
m68k_00924a:
        beq.w (. + 30)
m68k_00924a_end:
.org 0x924E
m68k_00924e:
        cmpi.w #0x2,%d6
m68k_00924e_end:
.org 0x9252
m68k_009252:
        bcc.w (. + 12)
m68k_009252_end:
.org 0x9256
m68k_009256:
        lsl.l #0x8,%d7
m68k_009256_end:
.org 0x9258
m68k_009258:
        move.b (%a1)+,%d7
m68k_009258_end:
.org 0x925A
m68k_00925a:
        bra.w (. + 16)
m68k_00925a_end:
.org 0x925E
m68k_00925e:
        swap %d7
m68k_00925e_end:
.org 0x9260
m68k_009260:
        move.w (%a1)+,%d7
m68k_009260_end:
.org 0x9262
m68k_009262:
        subi.w #0x2,%d6
m68k_009262_end:
.org 0x9266
m68k_009266:
        bra.b (. + -38)
m68k_009266_end:
.org 0x9268
m68k_009268:
        move.l (%a1)+,%d7
m68k_009268_end:
.org 0x926A
m68k_00926a:
        and.l %d5,%d7
m68k_00926a_end:
.org 0x926C
m68k_00926c:
        lsl.l %d4,%d7
m68k_00926c_end:
.org 0x926E
m68k_00926e:
        or.b %d3,%d7
m68k_00926e_end:
.org 0x9270
m68k_009270:
        add.w %d0,%d4
m68k_009270_end:
.org 0x9272
m68k_009272:
        cmpi.w #0x8,%d4
m68k_009272_end:
.org 0x9276
m68k_009276:
        bcs.w (. + 18)
m68k_009276_end:
.org 0x927A
m68k_00927a:
        move.b %d7,(%a0)+
m68k_00927a_end:
.org 0x927C
m68k_00927c:
        lsr.l #0x8,%d7
m68k_00927c_end:
.org 0x927E
m68k_00927e:
        lea.l 0x1(%a0),%a0
m68k_00927e_end:
.org 0x9282
m68k_009282:
        subi.w #0x8,%d4
m68k_009282_end:
.org 0x9286
m68k_009286:
        bra.b (. + -20)
m68k_009286_end:
.org 0x9288
m68k_009288:
        move.w %d7,%d3
m68k_009288_end:
.org 0x928A
m68k_00928a:
        dbra %d2,(. + -78)
m68k_00928a_end:
.org 0x928E
m68k_00928e:
        tst.w %d3
m68k_00928e_end:
.org 0x9290
m68k_009290:
        beq.w (. + 8)
m68k_009290_end:
.org 0x9298
m68k_009298:
        rts
m68k_009298_end:
.org 0x931E
m68k_00931e:
        subq.w #0x1,%d2
m68k_00931e_end:
.org 0x9320
m68k_009320:
        clr.w %d3
m68k_009320_end:
.org 0x9322
m68k_009322:
        clr.w %d4
m68k_009322_end:
.org 0x9324
m68k_009324:
        lea.l -140(%pc),%a2
m68k_009324_end:
.org 0x9328
m68k_009328:
        move.w %d0,%d5
m68k_009328_end:
.org 0x932A
m68k_00932a:
        lsl.w #0x2,%d5
m68k_00932a_end:
.org 0x932C
m68k_00932c:
        move.l (%a2, %d5.w),%d5
m68k_00932c_end:
.org 0x9330
m68k_009330:
        move.b %d3,%d7
m68k_009330_end:
.org 0x9332
m68k_009332:
        cmp.w %d0,%d4
m68k_009332_end:
.org 0x9334
m68k_009334:
        bcc.w (. + 18)
m68k_009334_end:
.org 0x9338
m68k_009338:
        ror.l #0x8,%d7
m68k_009338_end:
.org 0x933A
m68k_00933a:
        move.b (%a0)+,%d7
m68k_00933a_end:
.org 0x933C
m68k_00933c:
        lea.l 0x1(%a0),%a0
m68k_00933c_end:
.org 0x9340
m68k_009340:
        addi.w #0x8,%d4
m68k_009340_end:
.org 0x9344
m68k_009344:
        bra.b (. + -18)
m68k_009344_end:
.org 0x9346
m68k_009346:
        move.w %d7,%d3
m68k_009346_end:
.org 0x9348
m68k_009348:
        cmpi.w #0x8,%d4
m68k_009348_end:
.org 0x934C
m68k_00934c:
        bhi.w (. + 16)
m68k_00934c_end:
.org 0x9350
m68k_009350:
        move.w #0x8,%d6
m68k_009350_end:
.org 0x9354
m68k_009354:
        sub.w %d4,%d6
m68k_009354_end:
.org 0x9356
m68k_009356:
        lsr.w %d6,%d7
m68k_009356_end:
.org 0x9358
m68k_009358:
        bra.w (. + 30)
m68k_009358_end:
.org 0x935C
m68k_00935c:
        ror.l #0x8,%d7
m68k_00935c_end:
.org 0x935E
m68k_00935e:
        move.w #0x20,%d6
m68k_00935e_end:
.org 0x9362
m68k_009362:
        sub.w %d4,%d6
m68k_009362_end:
.org 0x9364
m68k_009364:
        cmpi.w #0x8,%d6
m68k_009364_end:
.org 0x9368
m68k_009368:
        bls.w (. + 12)
m68k_009368_end:
.org 0x936C
m68k_00936c:
        lsr.l #0x8,%d7
m68k_00936c_end:
.org 0x936E
m68k_00936e:
        subi.w #0x8,%d6
m68k_00936e_end:
.org 0x9372
m68k_009372:
        bra.b (. + -14)
m68k_009372_end:
.org 0x9374
m68k_009374:
        lsr.l %d6,%d7
m68k_009374_end:
.org 0x9376
m68k_009376:
        and.l %d5,%d7
m68k_009376_end:
.org 0x9378
m68k_009378:
        move.w %d1,%d6
m68k_009378_end:
.org 0x937A
m68k_00937a:
        subq.w #0x1,%d6
m68k_00937a_end:
.org 0x937C
m68k_00937c:
        move.b %d7,(%a1, %d6.w)
m68k_00937c_end:
.org 0x9380
m68k_009380:
        lsr.l #0x8,%d7
m68k_009380_end:
.org 0x9382
m68k_009382:
        dbra %d6,(. + -6)
m68k_009382_end:
.org 0x9386
m68k_009386:
        adda.w %d1,%a1
m68k_009386_end:
.org 0x9388
m68k_009388:
        sub.w %d0,%d4
m68k_009388_end:
.org 0x938A
m68k_00938a:
        dbra %d2,(. + -90)
m68k_00938a_end:
.org 0x938E
m68k_00938e:
        rts
m68k_00938e_end:
.org 0x9390
m68k_009390:
        lea.l 0xc600:w,%a0
m68k_009390_end:
.org 0x9394
m68k_009394:
        lea.l 0xc000:w,%a1
m68k_009394_end:
.org 0x9398
m68k_009398:
        lea.l 0xbe00:w,%a2
m68k_009398_end:
.org 0x939C
m68k_00939c:
        move.w #0xff,%d0
m68k_00939c_end:
.org 0x93A0
m68k_0093a0:
        move.w (%a1)+,%d1
m68k_0093a0_end:
.org 0x93A2
m68k_0093a2:
        add.w (%a2)+,%d1
m68k_0093a2_end:
.org 0x93A4
m68k_0093a4:
        move.w #0x1,%d2
m68k_0093a4_end:
.org 0x93A8
m68k_0093a8:
        lea.l 20(%pc),%a3
m68k_0093a8_end:
.org 0x93AC
m68k_0093ac:
        cmp.w (%a3)+,%d1
m68k_0093ac_end:
.org 0x93AE
m68k_0093ae:
        bcs.w (. + 8)
m68k_0093ae_end:
.org 0x93B2
m68k_0093b2:
        addq.w #0x1,%d2
m68k_0093b2_end:
.org 0x93B4
m68k_0093b4:
        bra.b (. + -8)
m68k_0093b4_end:
.org 0x93B6
m68k_0093b6:
        move.b %d2,(%a0)+
m68k_0093b6_end:
.org 0x93B8
m68k_0093b8:
        dbra %d0,(. + -24)
m68k_0093b8_end:
.org 0x93BC
m68k_0093bc:
        rts
m68k_0093bc_end:
.org 0x93F0
m68k_0093f0:
        move.w #0x2700,%sr
m68k_0093f0_end:
.org 0x93F4
m68k_0093f4:
        move.w 0xf606:w,%d0
m68k_0093f4_end:
.org 0x93F8
m68k_0093f8:
        andi.b #0xbf,%d0
m68k_0093f8_end:
.org 0x93FC
m68k_0093fc:
        move.w %d0,0xc00004:l
m68k_0093fc_end:
.org 0x9402
m68k_009402:
        jsr 0x68ce:l
m68k_009402_end:
.org 0x9408
m68k_009408:
        move.l #0x40000000,0xc00004:l
m68k_009408_end:
.org 0x9412
m68k_009412:
        lea.l 322(%pc),%a0
m68k_009412_end:
.org 0x9416
m68k_009416:
        move.w #0x1b7,%d0
m68k_009416_end:
.org 0x941A
m68k_00941a:
        move.l (%a0)+,0xc00000:l
m68k_00941a_end:
.org 0x9420
m68k_009420:
        dbra %d0,(. + -6)
m68k_009420_end:
.org 0x9424
m68k_009424:
        moveq #11,%d5
m68k_009424_end:
.org 0x9426
m68k_009426:
        moveq #3,%d6
m68k_009426_end:
.org 0x9428
m68k_009428:
        move.w #0x8001,%d4
m68k_009428_end:
.org 0x942C
m68k_00942c:
        move.l #0x461c0003,%d0
m68k_00942c_end:
.org 0x9432
m68k_009432:
        move.w %d5,%d7
m68k_009432_end:
.org 0x9434
m68k_009434:
        move.l %d0,0xc00004:l
m68k_009434_end:
.org 0x943A
m68k_00943a:
        move.w %d4,0xc00000:l
m68k_00943a_end:
.org 0x9440
m68k_009440:
        addq.w #0x1,%d4
m68k_009440_end:
.org 0x9442
m68k_009442:
        dbra %d7,(. + -8)
m68k_009442_end:
.org 0x9446
m68k_009446:
        addi.l #0x800000,%d0
m68k_009446_end:
.org 0x944C
m68k_00944c:
        dbra %d6,(. + -26)
m68k_00944c_end:
.org 0x9450
m68k_009450:
        btst.b #0x7,0xa10001:l
m68k_009450_end:
.org 0x9458
m68k_009458:
        beq.w (. + 38)
m68k_009458_end:
.org 0x947E
m68k_00947e:
        moveq #0,%d0
m68k_00947e_end:
.org 0x9480
m68k_009480:
        jsr 0x8112:l
m68k_009480_end:
.org 0x9486
m68k_009486:
        move.w #0x28,0xf618:w
m68k_009486_end:
.org 0x948C
m68k_00948c:
        move.w #0x12c,0xf608:w
m68k_00948c_end:
.org 0x9492
m68k_009492:
        move.w #0x2500,%sr
m68k_009492_end:
.org 0x9496
m68k_009496:
        move.w #0x100,0xf612:w
m68k_009496_end:
.org 0x949C
m68k_00949c:
        rts
m68k_00949c_end:
.org 0x949E
m68k_00949e:
        subq.w #0x1,0xf61a:w
m68k_00949e_end:
.org 0x94A2
m68k_0094a2:
        bpl.b (. + 38)
m68k_0094a2_end:
.org 0x94A4
m68k_0094a4:
        move.w #0x3,0xf61a:w
m68k_0094a4_end:
.org 0x94AA
m68k_0094aa:
        move.w 0xf618:w,%d0
m68k_0094aa_end:
.org 0x94AE
m68k_0094ae:
        bmi.b (. + 26)
m68k_0094ae_end:
.org 0x94B0
m68k_0094b0:
        subq.w #0x2,0xf618:w
m68k_0094b0_end:
.org 0x94B4
m68k_0094b4:
        lea.l 20(%pc, %d0.w),%a0
m68k_0094b4_end:
.org 0x94B8
m68k_0094b8:
        lea.l 0xfb04:w,%a1
m68k_0094b8_end:
.org 0x94BC
m68k_0094bc:
        moveq #10,%d0
m68k_0094bc_end:
.org 0x94BE
m68k_0094be:
        move.w (%a0)+,(%a1)+
m68k_0094be_end:
.org 0x94C0
m68k_0094c0:
        dbra %d0,(. + -2)
m68k_0094c0_end:
.org 0x94C4
m68k_0094c4:
        addq.w #0x1,0xf31e:w
m68k_0094c4_end:
.org 0x94C8
m68k_0094c8:
        rts
m68k_0094c8_end:
.org 0x9508
m68k_009508:
        move.w #0x80,%d0
m68k_009508_end:
.org 0x950C
m68k_00950c:
        dbra %d0,(. + 0)
m68k_00950c_end:
.org 0x9510
m68k_009510:
        jsr 0x4890:l
m68k_009510_end:
.org 0x9516
m68k_009516:
        jsr 0x4998:l
m68k_009516_end:
.org 0x951C
m68k_00951c:
        tst.w 0xf608:w
m68k_00951c_end:
.org 0x9520
m68k_009520:
        beq.w (. + 8)
m68k_009520_end:
.org 0x9524
m68k_009524:
        subq.w #0x1,0xf608:w
m68k_009524_end:
.org 0x9528
m68k_009528:
        move.w 0xf606:w,%d0
m68k_009528_end:
.org 0x952C
m68k_00952c:
        ori.b #0x40,%d0
m68k_00952c_end:
.org 0x9530
m68k_009530:
        move.w %d0,0xc00004:l
m68k_009530_end:
.org 0x9536
m68k_009536:
        bsr.w (. + -152)
m68k_009536_end:
.org 0x953A
m68k_00953a:
        tst.w 0xf608:w
m68k_00953a_end:
.org 0x953E
m68k_00953e:
        beq.b (. + 12)
m68k_00953e_end:
.org 0x9540
m68k_009540:
        btst.b #0x7,0xf603:w
m68k_009540_end:
.org 0x9546
m68k_009546:
        bne.b (. + 4)
m68k_009546_end:
.org 0x9548
m68k_009548:
        rts
m68k_009548_end:
.org 0x954A
m68k_00954a:
        move.w #0xc,0xf600:w
m68k_00954a_end:
.org 0x9550
m68k_009550:
        clr.w 0xf776:w
m68k_009550_end:
.org 0x9554
m68k_009554:
        rts
m68k_009554_end:
.org 0x9C7A
m68k_009c7a:
        jsr 0x5cc8:l
m68k_009c7a_end:
.org 0x9C80
m68k_009c80:
        cmpi.w #0xffff,%d4
m68k_009c80_end:
.org 0x9C84
m68k_009c84:
        beq.w (. + 132)
m68k_009c84_end:
.org 0x9C88
m68k_009c88:
        lea.l 0xea38:w,%a0
m68k_009c88_end:
.org 0x9C8C
m68k_009c8c:
        move.w 0xf364:w,%d0
m68k_009c8c_end:
.org 0x9C90
m68k_009c90:
        andi.w #0x3f,%d0
m68k_009c90_end:
.org 0x9C94
m68k_009c94:
        tst.b (%a0, %d0.w)
m68k_009c94_end:
.org 0x9C98
m68k_009c98:
        bne.w (. + 64)
m68k_009c98_end:
.org 0x9C9C
m68k_009c9c:
        bset.b #0x3,0xf31c:w
m68k_009c9c_end:
.org 0x9CA2
m68k_009ca2:
        bset.b #0x1,0xf31c:w
m68k_009ca2_end:
.org 0x9CA8
m68k_009ca8:
        bclr.b #0x2,0xf31c:w
m68k_009ca8_end:
.org 0x9CAE
m68k_009cae:
        clr.w 0xff3938:l
m68k_009cae_end:
.org 0x9CB4
m68k_009cb4:
        move.w #0x1,0xf38e:w
m68k_009cb4_end:
.org 0x9CBA
m68k_009cba:
        addi.w #0x1,0xf364:w
m68k_009cba_end:
.org 0x9CC0
m68k_009cc0:
        move.w #0x205,0xf612:w
m68k_009cc0_end:
.org 0x9CC6
m68k_009cc6:
        bclr.b #0x0,0xf3a5:w
m68k_009cc6_end:
.org 0x9CCC
m68k_009ccc:
        clr.w 0xf378:w
m68k_009ccc_end:
.org 0x9CD0
m68k_009cd0:
        clr.w 0xf658:w
m68k_009cd0_end:
.org 0x9CD4
m68k_009cd4:
        bra.w (. + 318)
m68k_009cd4_end:
.org 0x9CD8
m68k_009cd8:
        move.w #0xc5,%d0
m68k_009cd8_end:
.org 0x9CDC
m68k_009cdc:
        lea.l 0xf428:w,%a0
m68k_009cdc_end:
.org 0x9CE0
m68k_009ce0:
        move.w 0xf364:w,%d1
m68k_009ce0_end:
.org 0x9CE4
m68k_009ce4:
        andi.w #0x3f,%d1
m68k_009ce4_end:
.org 0x9CE8
m68k_009ce8:
        move.b (%a0, %d1.w),%d1
m68k_009ce8_end:
.org 0x9CEC
m68k_009cec:
        cmp.w 0xf376:w,%d1
m68k_009cec_end:
.org 0x9CF0
m68k_009cf0:
        beq.w (. + 8)
m68k_009cf0_end:
.org 0x9CF4
m68k_009cf4:
        move.w #0x8f,%d0
m68k_009cf4_end:
.org 0x9CF8
m68k_009cf8:
        move.w #0x20f,0xf612:w
m68k_009cf8_end:
.org 0x9CFE
m68k_009cfe:
        jsr 0x676f2:l
m68k_009cfe_end:
.org 0x9D04
m68k_009d04:
        bra.w (. + 270)
m68k_009d04_end:
.org 0x9D08
m68k_009d08:
        bsr.w (. + 268)
m68k_009d08_end:
.org 0xA0CC
m68k_00a0cc:
        move.w %a5,%d0
m68k_00a0cc_end:
.org 0xA0CE
m68k_00a0ce:
        move.w 0xf318:w,%d1
m68k_00a0ce_end:
.org 0xA0D2
m68k_00a0d2:
        lea.l 0x8155a:l,%a0
m68k_00a0d2_end:
.org 0xA0D8
m68k_00a0d8:
        clr.w 0xf328:w
m68k_00a0d8_end:
.org 0xA0DC
m68k_00a0dc:
        jsr 0xaf6a:l
m68k_00a0dc_end:
.org 0xA0E2
m68k_00a0e2:
        jsr 0xb054:l
m68k_00a0e2_end:
.org 0xA0E8
m68k_00a0e8:
        ori.w #0xe000,%d0
m68k_00a0e8_end:
.org 0xA0EC
m68k_00a0ec:
        lea.l 0xd100:w,%a0
m68k_00a0ec_end:
.org 0xA0F0
m68k_00a0f0:
        adda.w 0xf31a:w,%a0
m68k_00a0f0_end:
.org 0xA0F4
m68k_00a0f4:
        move.w #0x29,%d1
m68k_00a0f4_end:
.org 0xA0F8
m68k_00a0f8:
        move.w %d1,(%a0)+
m68k_00a0f8_end:
.org 0xA0FA
m68k_00a0fa:
        move.w %d0,(%a0)+
m68k_00a0fa_end:
.org 0xA0FC
m68k_00a0fc:
        jsr 0xb06e:l
m68k_00a0fc_end:
.org 0xA102
m68k_00a102:
        clr.w (%a0)
m68k_00a102_end:
.org 0xA104
m68k_00a104:
        addi.w #0x56,0xf31a:w
m68k_00a104_end:
.org 0xA10A
m68k_00a10a:
        rts
m68k_00a10a_end:
.org 0xA10C
m68k_00a10c:
        move.w 0xf314:w,%d0
m68k_00a10c_end:
.org 0xA110
m68k_00a110:
        move.w %a5,%d1
m68k_00a110_end:
.org 0xA112
m68k_00a112:
        lea.l 0x8155a:l,%a0
m68k_00a112_end:
.org 0xA118
m68k_00a118:
        move.w #0x1,0xf328:w
m68k_00a118_end:
.org 0xA11E
m68k_00a11e:
        jsr 0xaf6a:l
m68k_00a11e_end:
.org 0xA124
m68k_00a124:
        jsr 0xb054:l
m68k_00a124_end:
.org 0xA12A
m68k_00a12a:
        ori.w #0xe000,%d0
m68k_00a12a_end:
.org 0xA12E
m68k_00a12e:
        lea.l 0xd100:w,%a0
m68k_00a12e_end:
.org 0xA132
m68k_00a132:
        adda.w 0xf31a:w,%a0
m68k_00a132_end:
.org 0xA136
m68k_00a136:
        move.w #0x801d,%d1
m68k_00a136_end:
.org 0xA13A
m68k_00a13a:
        move.w %d1,(%a0)+
m68k_00a13a_end:
.org 0xA13C
m68k_00a13c:
        move.w %d0,(%a0)+
m68k_00a13c_end:
.org 0xA13E
m68k_00a13e:
        jsr 0xb0b2:l
m68k_00a13e_end:
.org 0xA144
m68k_00a144:
        clr.w (%a0)
m68k_00a144_end:
.org 0xA146
m68k_00a146:
        addi.w #0x3e,0xf31a:w
m68k_00a146_end:
.org 0xA14C
m68k_00a14c:
        rts
m68k_00a14c_end:
.org 0xA158
m68k_00a158:
        move.w 0xf376:w,%d0
m68k_00a158_end:
.org 0xA15C
m68k_00a15c:
        cmp.w 0xf67a:w,%d0
m68k_00a15c_end:
.org 0xA160
m68k_00a160:
        beq.w (. + 20)
m68k_00a160_end:
.org 0xA164
m68k_00a164:
        cmp.w 0xf67c:w,%d0
m68k_00a164_end:
.org 0xA168
m68k_00a168:
        beq.w (. + 12)
m68k_00a168_end:
.org 0xA16C
m68k_00a16c:
        cmp.w 0xf67e:w,%d0
m68k_00a16c_end:
.org 0xA170
m68k_00a170:
        bne.w (. + 38)
m68k_00a170_end:
.org 0xA174
m68k_00a174:
        lea.l 34(%pc),%a0
m68k_00a174_end:
.org 0xA178
m68k_00a178:
        nop
m68k_00a178_end:
.org 0xA17A
m68k_00a17a:
        move.w 0xf35e:w,%d0
m68k_00a17a_end:
.org 0xA17E
m68k_00a17e:
        move.w 0xf360:w,%d1
m68k_00a17e_end:
.org 0xA182
m68k_00a182:
        clr.w %d2
m68k_00a182_end:
.org 0xA184
m68k_00a184:
        move.w 0xf314:w,0xf60a:w
m68k_00a184_end:
.org 0xA18A
m68k_00a18a:
        move.w 0xf318:w,0xf60e:w
m68k_00a18a_end:
.org 0xA190
m68k_00a190:
        jsr 0xac10:l
m68k_00a190_end:
.org 0xA196
m68k_00a196:
        rts
m68k_00a196_end:
.org 0xA370
m68k_00a370:
        cmpi.w #0x209,0xf612:w
m68k_00a370_end:
.org 0xA376
m68k_00a376:
        bne.w (. + 14)
m68k_00a376_end:
.org 0xA384
m68k_00a384:
        cmpi.w #0x207,0xf612:w
m68k_00a384_end:
.org 0xA38A
m68k_00a38a:
        bne.w (. + 22)
m68k_00a38a_end:
.org 0xA3A0
m68k_00a3a0:
        move.w 0xf376:w,%d0
m68k_00a3a0_end:
.org 0xA3A4
m68k_00a3a4:
        cmp.w 0xf67c:w,%d0
m68k_00a3a4_end:
.org 0xA3A8
m68k_00a3a8:
        beq.w (. + 24)
m68k_00a3a8_end:
.org 0xA3AC
m68k_00a3ac:
        cmp.w 0xf67e:w,%d0
m68k_00a3ac_end:
.org 0xA3B0
m68k_00a3b0:
        beq.w (. + 16)
m68k_00a3b0_end:
.org 0xA3B4
m68k_00a3b4:
        cmp.w 0xf67a:w,%d0
m68k_00a3b4_end:
.org 0xA3B8
m68k_00a3b8:
        bne.w (. + 18)
m68k_00a3b8_end:
.org 0xA3BC
m68k_00a3bc:
        bra.w (. + 28)
m68k_00a3bc_end:
.org 0xA3CA
m68k_00a3ca:
        move.w 0xf604:w,%d0
m68k_00a3ca_end:
.org 0xA3CE
m68k_00a3ce:
        or.w %d0,0xf602:w
m68k_00a3ce_end:
.org 0xA3D2
m68k_00a3d2:
        move.w 0xf602:w,0xf604:w
m68k_00a3d2_end:
.org 0xA3D8
m68k_00a3d8:
        rts
m68k_00a3d8_end:
.org 0xA3DA
m68k_00a3da:
        lea.l 0xfb00:w,%a0
m68k_00a3da_end:
.org 0xA3DE
m68k_00a3de:
        cmpi.w #0x20,0xf352:w
m68k_00a3de_end:
.org 0xA3E4
m68k_00a3e4:
        bcc.w (. + 8)
m68k_00a3e4_end:
.org 0xA3EC
m68k_00a3ec:
        move.w 0xef7a:w,%d0
m68k_00a3ec_end:
.org 0xA3F0
m68k_00a3f0:
        move.w 0xef7c:w,%d1
m68k_00a3f0_end:
.org 0xA3F4
m68k_00a3f4:
        addq.w #0x1,%d1
m68k_00a3f4_end:
.org 0xA3F6
m68k_00a3f6:
        cmpi.w #0x6,%d1
m68k_00a3f6_end:
.org 0xA3FA
m68k_00a3fa:
        bcs.w (. + 46)
m68k_00a3fa_end:
.org 0xA3FE
m68k_00a3fe:
        clr.w %d1
m68k_00a3fe_end:
.org 0xA400
m68k_00a400:
        addq.w #0x1,%d0
m68k_00a400_end:
.org 0xA402
m68k_00a402:
        cmpi.w #0xa,%d0
m68k_00a402_end:
.org 0xA406
m68k_00a406:
        bcs.w (. + 6)
m68k_00a406_end:
.org 0xA40A
m68k_00a40a:
        clr.w %d0
m68k_00a40a_end:
.org 0xA40C
m68k_00a40c:
        move.w %d0,0xef7a:w
m68k_00a40c_end:
.org 0xA410
m68k_00a410:
        lsl.w #0x2,%d0
m68k_00a410_end:
.org 0xA412
m68k_00a412:
        lea.l 26(%pc),%a1
m68k_00a412_end:
.org 0xA416
m68k_00a416:
        move.w (%a1, %d0.w),0x32(%a0)
m68k_00a416_end:
.org 0xA41C
m68k_00a41c:
        move.w 0x2(%a1, %d0.w),0x38(%a0)
m68k_00a41c_end:
.org 0xA422
m68k_00a422:
        move.w #0x1,0xf31e:w
m68k_00a422_end:
.org 0xA428
m68k_00a428:
        move.w %d1,0xef7c:w
m68k_00a428_end:
.org 0xA42C
m68k_00a42c:
        rts
m68k_00a42c_end:
.org 0xAC08
m68k_00ac08:
        clr.w 0xf60a:w
m68k_00ac08_end:
.org 0xAC0C
m68k_00ac0c:
        clr.w 0xf60e:w
m68k_00ac0c_end:
.org 0xAC10
m68k_00ac10:
        move.w #0x70,0xf302:w
m68k_00ac10_end:
.org 0xAC16
m68k_00ac16:
        move.w #0x160,0xf304:w
m68k_00ac16_end:
.org 0xAC1C
m68k_00ac1c:
        move.w #0x70,0xf306:w
m68k_00ac1c_end:
.org 0xAC22
m68k_00ac22:
        move.w #0x1c0,0xf308:w
m68k_00ac22_end:
.org 0xAC28
m68k_00ac28:
        movem.l %d3-%d7/%a1,-(%a7)
m68k_00ac28_end:
.org 0xAC2C
m68k_00ac2c:
        cmpi.b #0x50,0xf300:w
m68k_00ac2c_end:
.org 0xAC32
m68k_00ac32:
        bcc.w (. + 206)
m68k_00ac32_end:
.org 0xAC36
m68k_00ac36:
        andi.w #0xf800,%d2
m68k_00ac36_end:
.org 0xAC3A
m68k_00ac3a:
        move.w %d0,%d3
m68k_00ac3a_end:
.org 0xAC3C
m68k_00ac3c:
        sub.w 0xf60a:w,%d3
m68k_00ac3c_end:
.org 0xAC40
m68k_00ac40:
        addi.w #0x80,%d3
m68k_00ac40_end:
.org 0xAC44
m68k_00ac44:
        move.w %d1,%d4
m68k_00ac44_end:
.org 0xAC46
m68k_00ac46:
        sub.w 0xf60e:w,%d4
m68k_00ac46_end:
.org 0xAC4A
m68k_00ac4a:
        addi.w #0x80,%d4
m68k_00ac4a_end:
.org 0xAC4E
m68k_00ac4e:
        clr.w %d5
m68k_00ac4e_end:
.org 0xAC50
m68k_00ac50:
        move.b 0xf300:w,%d5
m68k_00ac50_end:
.org 0xAC54
m68k_00ac54:
        lsl.w #0x3,%d5
m68k_00ac54_end:
.org 0xAC56
m68k_00ac56:
        lea.l 0xf800:w,%a1
m68k_00ac56_end:
.org 0xAC5A
m68k_00ac5a:
        lea.l (%a1, %d5.w),%a1
m68k_00ac5a_end:
.org 0xAC5E
m68k_00ac5e:
        move.w (%a0),%d5
m68k_00ac5e_end:
.org 0xAC60
m68k_00ac60:
        cmpi.w #0x8000,%d5
m68k_00ac60_end:
.org 0xAC64
m68k_00ac64:
        beq.w (. + 156)
m68k_00ac64_end:
.org 0xAC68
m68k_00ac68:
        btst.l #0xc,%d2
m68k_00ac68_end:
.org 0xAC6C
m68k_00ac6c:
        beq.b (. + 30)
m68k_00ac6c_end:
.org 0xAC8A
m68k_00ac8a:
        add.w %d3,%d5
m68k_00ac8a_end:
.org 0xAC8C
m68k_00ac8c:
        cmp.w 0xf302:w,%d5
m68k_00ac8c_end:
.org 0xAC90
m68k_00ac90:
        bcs.b (. + 100)
m68k_00ac90_end:
.org 0xAC92
m68k_00ac92:
        cmp.w 0xf304:w,%d5
m68k_00ac92_end:
.org 0xAC96
m68k_00ac96:
        bcc.b (. + 94)
m68k_00ac96_end:
.org 0xAC98
m68k_00ac98:
        move.w %d5,(%a1)
m68k_00ac98_end:
.org 0xAC9A
m68k_00ac9a:
        moveq #0,%d5
m68k_00ac9a_end:
.org 0xAC9C
m68k_00ac9c:
        move.w 0x4(%a0),%d5
m68k_00ac9c_end:
.org 0xACA0
m68k_00aca0:
        lsl.l #0x4,%d5
m68k_00aca0_end:
.org 0xACA2
m68k_00aca2:
        asr.w #0x4,%d5
m68k_00aca2_end:
.org 0xACA4
m68k_00aca4:
        move.l %d5,%d6
m68k_00aca4_end:
.org 0xACA6
m68k_00aca6:
        btst.l #0xb,%d2
m68k_00aca6_end:
.org 0xACAA
m68k_00acaa:
        beq.b (. + 20)
m68k_00acaa_end:
.org 0xACBE
m68k_00acbe:
        add.w %d4,%d5
m68k_00acbe_end:
.org 0xACC0
m68k_00acc0:
        cmp.w 0xf306:w,%d5
m68k_00acc0_end:
.org 0xACC4
m68k_00acc4:
        bcs.b (. + 48)
m68k_00acc4_end:
.org 0xACC6
m68k_00acc6:
        cmp.w 0xf308:w,%d5
m68k_00acc6_end:
.org 0xACCA
m68k_00acca:
        bcc.b (. + 42)
m68k_00acca_end:
.org 0xACCC
m68k_00accc:
        move.w %d5,0x6(%a1)
m68k_00accc_end:
.org 0xACD0
m68k_00acd0:
        swap %d6
m68k_00acd0_end:
.org 0xACD2
m68k_00acd2:
        lsl.w #0x8,%d6
m68k_00acd2_end:
.org 0xACD4
m68k_00acd4:
        move.w %d6,0x2(%a1)
m68k_00acd4_end:
.org 0xACD8
m68k_00acd8:
        tst.b 0xf300:w
m68k_00acd8_end:
.org 0xACDC
m68k_00acdc:
        beq.b (. + 8)
m68k_00acdc_end:
.org 0xACDE
m68k_00acde:
        move.b 0xf300:w,-0x5(%a1)
m68k_00acde_end:
.org 0xACE4
m68k_00ace4:
        addq.b #0x1,0xf300:w
m68k_00ace4_end:
.org 0xACE8
m68k_00ace8:
        move.w 0x2(%a0),%d5
m68k_00ace8_end:
.org 0xACEC
m68k_00acec:
        eor.w %d2,%d5
m68k_00acec_end:
.org 0xACEE
m68k_00acee:
        move.w %d5,0x4(%a1)
m68k_00acee_end:
.org 0xACF2
m68k_00acf2:
        addq.l #0x8,%a1
m68k_00acf2_end:
.org 0xACF4
m68k_00acf4:
        addq.l #0x6,%a0
m68k_00acf4_end:
.org 0xACF6
m68k_00acf6:
        cmpi.b #0x50,0xf300:w
m68k_00acf6_end:
.org 0xACFC
m68k_00acfc:
        bcs.w (. + -158)
m68k_00acfc_end:
.org 0xAD00
m68k_00ad00:
        movem.l (%a7)+,%d3-%d7/%a1
m68k_00ad00_end:
.org 0xAD04
m68k_00ad04:
        rts
m68k_00ad04_end:
.org 0xAD06
m68k_00ad06:
        tst.w 0xd100:w
m68k_00ad06_end:
.org 0xAD0A
m68k_00ad0a:
        beq.b (. + 8)
m68k_00ad0a_end:
.org 0xAD0C
m68k_00ad0c:
        lea.l 0xd100:w,%a0
m68k_00ad0c_end:
.org 0xAD10
m68k_00ad10:
        bsr.b (. + 12)
m68k_00ad10_end:
.org 0xAD12
m68k_00ad12:
        clr.w 0xf31a:w
m68k_00ad12_end:
.org 0xAD16
m68k_00ad16:
        clr.w 0xd100:w
m68k_00ad16_end:
.org 0xAD1A
m68k_00ad1a:
        rts
m68k_00ad1a_end:
.org 0xAD1C
m68k_00ad1c:
        lea.l 0xc00000:l,%a6
m68k_00ad1c_end:
.org 0xAD22
m68k_00ad22:
        move.w #0x8f02,%d1
m68k_00ad22_end:
.org 0xAD26
m68k_00ad26:
        move.w (%a0)+,%d0
m68k_00ad26_end:
.org 0xAD28
m68k_00ad28:
        beq.w (. + 160)
m68k_00ad28_end:
.org 0xAD2C
m68k_00ad2c:
        bmi.b (. + 36)
m68k_00ad2c_end:
.org 0xAD2E
m68k_00ad2e:
        moveq #0,%d2
m68k_00ad2e_end:
.org 0xAD30
m68k_00ad30:
        move.w (%a0)+,%d2
m68k_00ad30_end:
.org 0xAD32
m68k_00ad32:
        clr.w %d3
m68k_00ad32_end:
.org 0xAD34
m68k_00ad34:
        btst.l #0xe,%d0
m68k_00ad34_end:
.org 0xAD38
m68k_00ad38:
        bne.b (. + 56)
m68k_00ad38_end:
.org 0xAD3A
m68k_00ad3a:
        move.w %d2,%d3
m68k_00ad3a_end:
.org 0xAD3C
m68k_00ad3c:
        andi.w #0x7f,%d3
m68k_00ad3c_end:
.org 0xAD40
m68k_00ad40:
        lsr.w #0x1,%d3
m68k_00ad40_end:
.org 0xAD42
m68k_00ad42:
        add.w %d0,%d3
m68k_00ad42_end:
.org 0xAD44
m68k_00ad44:
        subi.w #0x40,%d3
m68k_00ad44_end:
.org 0xAD48
m68k_00ad48:
        bcc.b (. + 4)
m68k_00ad48_end:
.org 0xAD4A
m68k_00ad4a:
        clr.w %d3
m68k_00ad4a_end:
.org 0xAD4C
m68k_00ad4c:
        sub.w %d3,%d0
m68k_00ad4c_end:
.org 0xAD4E
m68k_00ad4e:
        bra.b (. + 34)
m68k_00ad4e_end:
.org 0xAD50
m68k_00ad50:
        move.w #0x8f80,%d1
m68k_00ad50_end:
.org 0xAD54
m68k_00ad54:
        andi.w #0x7fff,%d0
m68k_00ad54_end:
.org 0xAD58
m68k_00ad58:
        moveq #0,%d2
m68k_00ad58_end:
.org 0xAD5A
m68k_00ad5a:
        move.w (%a0)+,%d2
m68k_00ad5a_end:
.org 0xAD5C
m68k_00ad5c:
        move.w %d2,%d3
m68k_00ad5c_end:
.org 0xAD5E
m68k_00ad5e:
        andi.w #0x1fff,%d3
m68k_00ad5e_end:
.org 0xAD62
m68k_00ad62:
        lsr.w #0x7,%d3
m68k_00ad62_end:
.org 0xAD64
m68k_00ad64:
        add.w %d0,%d3
m68k_00ad64_end:
.org 0xAD66
m68k_00ad66:
        subi.w #0x40,%d3
m68k_00ad66_end:
.org 0xAD6A
m68k_00ad6a:
        bcc.b (. + 4)
m68k_00ad6a_end:
.org 0xAD6C
m68k_00ad6c:
        clr.w %d3
m68k_00ad6c_end:
.org 0xAD6E
m68k_00ad6e:
        sub.w %d3,%d0
m68k_00ad6e_end:
.org 0xAD70
m68k_00ad70:
        andi.w #0xbfff,%d0
m68k_00ad70_end:
.org 0xAD74
m68k_00ad74:
        subq.w #0x1,%d0
m68k_00ad74_end:
.org 0xAD76
m68k_00ad76:
        move.w %d1,0xc00004:l
m68k_00ad76_end:
.org 0xAD7C
m68k_00ad7c:
        lsl.l #0x2,%d2
m68k_00ad7c_end:
.org 0xAD7E
m68k_00ad7e:
        lsr.w #0x2,%d2
m68k_00ad7e_end:
.org 0xAD80
m68k_00ad80:
        ori.w #0x4000,%d2
m68k_00ad80_end:
.org 0xAD84
m68k_00ad84:
        swap %d2
m68k_00ad84_end:
.org 0xAD86
m68k_00ad86:
        move.l %d2,0xc00004:l
m68k_00ad86_end:
.org 0xAD8C
m68k_00ad8c:
        cmpi.w #0x8,%d0
m68k_00ad8c_end:
.org 0xAD90
m68k_00ad90:
        bcc.b (. + 64)
m68k_00ad90_end:
.org 0xAD92
m68k_00ad92:
        move.w (%a0)+,(%a6)
m68k_00ad92_end:
.org 0xAD94
m68k_00ad94:
        dbra %d0,(. + -2)
m68k_00ad94_end:
.org 0xAD98
m68k_00ad98:
        tst.w %d3
m68k_00ad98_end:
.org 0xAD9A
m68k_00ad9a:
        beq.b (. + -126)
m68k_00ad9a_end:
.org 0xAD9C
m68k_00ad9c:
        btst.l #0x1,%d1
m68k_00ad9c_end:
.org 0xADA0
m68k_00ada0:
        beq.b (. + 10)
m68k_00ada0_end:
.org 0xADA2
m68k_00ada2:
        andi.l #0xff80ffff,%d2
m68k_00ada2_end:
.org 0xADA8
m68k_00ada8:
        bra.b (. + 8)
m68k_00ada8_end:
.org 0xADAA
m68k_00adaa:
        andi.l #0xe07fffff,%d2
m68k_00adaa_end:
.org 0xADB0
m68k_00adb0:
        subq.w #0x1,%d3
m68k_00adb0_end:
.org 0xADB2
m68k_00adb2:
        move.l %d2,0xc00004:l
m68k_00adb2_end:
.org 0xADB8
m68k_00adb8:
        cmpi.w #0x8,%d3
m68k_00adb8_end:
.org 0xADBC
m68k_00adbc:
        bcc.b (. + 42)
m68k_00adbc_end:
.org 0xADBE
m68k_00adbe:
        move.w (%a0)+,(%a6)
m68k_00adbe_end:
.org 0xADC0
m68k_00adc0:
        dbra %d3,(. + -8)
m68k_00adc0_end:
.org 0xADC4
m68k_00adc4:
        bra.w (. + -168)
m68k_00adc4_end:
.org 0xADC8
m68k_00adc8:
        move.w %d1,0xc00004:l
m68k_00adc8_end:
.org 0xADCE
m68k_00adce:
        rts
m68k_00adce_end:
.org 0xADD0
m68k_00add0:
        move.w (%a0)+,(%a6)
m68k_00add0_end:
.org 0xADD2
m68k_00add2:
        move.w (%a0)+,(%a6)
m68k_00add2_end:
.org 0xADD4
m68k_00add4:
        move.w (%a0)+,(%a6)
m68k_00add4_end:
.org 0xADD6
m68k_00add6:
        move.w (%a0)+,(%a6)
m68k_00add6_end:
.org 0xADD8
m68k_00add8:
        move.w (%a0)+,(%a6)
m68k_00add8_end:
.org 0xADDA
m68k_00adda:
        move.w (%a0)+,(%a6)
m68k_00adda_end:
.org 0xADDC
m68k_00addc:
        move.w (%a0)+,(%a6)
m68k_00addc_end:
.org 0xADDE
m68k_00adde:
        move.w (%a0)+,(%a6)
m68k_00adde_end:
.org 0xADE0
m68k_00ade0:
        subi.w #0x8,%d0
m68k_00ade0_end:
.org 0xADE4
m68k_00ade4:
        bra.b (. + -88)
m68k_00ade4_end:
.org 0xADE6
m68k_00ade6:
        move.w (%a0)+,(%a6)
m68k_00ade6_end:
.org 0xADE8
m68k_00ade8:
        move.w (%a0)+,(%a6)
m68k_00ade8_end:
.org 0xADEA
m68k_00adea:
        move.w (%a0)+,(%a6)
m68k_00adea_end:
.org 0xADEC
m68k_00adec:
        move.w (%a0)+,(%a6)
m68k_00adec_end:
.org 0xADEE
m68k_00adee:
        move.w (%a0)+,(%a6)
m68k_00adee_end:
.org 0xADF0
m68k_00adf0:
        move.w (%a0)+,(%a6)
m68k_00adf0_end:
.org 0xADF2
m68k_00adf2:
        move.w (%a0)+,(%a6)
m68k_00adf2_end:
.org 0xADF4
m68k_00adf4:
        move.w (%a0)+,(%a6)
m68k_00adf4_end:
.org 0xADF6
m68k_00adf6:
        subi.w #0x8,%d3
m68k_00adf6_end:
.org 0xADFA
m68k_00adfa:
        bra.b (. + -66)
m68k_00adfa_end:
.org 0xAE8A
m68k_00ae8a:
        movem.l %d4-%d7/%a2,-(%a7)
m68k_00ae8a_end:
.org 0xAE8E
m68k_00ae8e:
        move.w (%a0)+,%d4
m68k_00ae8e_end:
.org 0xAE90
m68k_00ae90:
        bmi.b (. + 72)
m68k_00ae90_end:
.org 0xAE92
m68k_00ae92:
        move.w %d4,%d5
m68k_00ae92_end:
.org 0xAE94
m68k_00ae94:
        andi.w #0xff00,%d5
m68k_00ae94_end:
.org 0xAE98
m68k_00ae98:
        lsl.w #0x3,%d5
m68k_00ae98_end:
.org 0xAE9A
m68k_00ae9a:
        andi.w #0xff,%d4
m68k_00ae9a_end:
.org 0xAE9E
m68k_00ae9e:
        lsl.w #0x5,%d4
m68k_00ae9e_end:
.org 0xAEA0
m68k_00aea0:
        or.w %d5,%d4
m68k_00aea0_end:
.org 0xAEA2
m68k_00aea2:
        andi.l #0xffff,%d4
m68k_00aea2_end:
.org 0xAEA8
m68k_00aea8:
        lea.l 0x8159c:l,%a2
m68k_00aea8_end:
.org 0xAEAE
m68k_00aeae:
        lea.l (%a2, %d4.l),%a2
m68k_00aeae_end:
.org 0xAEB2
m68k_00aeb2:
        move.w #0xf,%d5
m68k_00aeb2_end:
.org 0xAEB6
m68k_00aeb6:
        bsr.w (. + 78)
m68k_00aeb6_end:
.org 0xAEBA
m68k_00aeba:
        move.l %d7,(%a1)
m68k_00aeba_end:
.org 0xAEBC
m68k_00aebc:
        bsr.w (. + 72)
m68k_00aebc_end:
.org 0xAEC0
m68k_00aec0:
        move.l %d7,0x40(%a1)
m68k_00aec0_end:
.org 0xAEC4
m68k_00aec4:
        addq.l #0x4,%a1
m68k_00aec4_end:
.org 0xAEC6
m68k_00aec6:
        dbra %d5,(. + -16)
m68k_00aec6_end:
.org 0xAECA
m68k_00aeca:
        adda.w #0x40,%a1
m68k_00aeca_end:
.org 0xAECE
m68k_00aece:
        dbra %d3,(. + -64)
m68k_00aece_end:
.org 0xAED2
m68k_00aed2:
        movem.l (%a7)+,%d4-%d7/%a2
m68k_00aed2_end:
.org 0xAED6
m68k_00aed6:
        rts
m68k_00aed6_end:
.org 0xAF04
m68k_00af04:
        moveq #0,%d7
m68k_00af04_end:
.org 0xAF06
m68k_00af06:
        move.b (%a2)+,%d6
m68k_00af06_end:
.org 0xAF08
m68k_00af08:
        move.w #0x7,%d4
m68k_00af08_end:
.org 0xAF0C
m68k_00af0c:
        lsl.l #0x4,%d7
m68k_00af0c_end:
.org 0xAF0E
m68k_00af0e:
        roxl.b #0x1,%d6
m68k_00af0e_end:
.org 0xAF10
m68k_00af10:
        bcc.b (. + 6)
m68k_00af10_end:
.org 0xAF12
m68k_00af12:
        or.b %d1,%d7
m68k_00af12_end:
.org 0xAF14
m68k_00af14:
        bra.b (. + 4)
m68k_00af14_end:
.org 0xAF16
m68k_00af16:
        or.b %d0,%d7
m68k_00af16_end:
.org 0xAF18
m68k_00af18:
        dbra %d4,(. + -12)
m68k_00af18_end:
.org 0xAF1C
m68k_00af1c:
        rts
m68k_00af1c_end:
.org 0xAF48
m68k_00af48:
        nop
m68k_00af48_end:
.org 0xAF4A
m68k_00af4a:
        nop
m68k_00af4a_end:
.org 0xAF4C
m68k_00af4c:
        move.w 0xc00004:l,%d0
m68k_00af4c_end:
.org 0xAF52
m68k_00af52:
        btst.l #0x3,%d0
m68k_00af52_end:
.org 0xAF56
m68k_00af56:
        bne.b (. + -10)
m68k_00af56_end:
.org 0xAF58
m68k_00af58:
        nop
m68k_00af58_end:
.org 0xAF5A
m68k_00af5a:
        nop
m68k_00af5a_end:
.org 0xAF5C
m68k_00af5c:
        move.w 0xc00004:l,%d0
m68k_00af5c_end:
.org 0xAF62
m68k_00af62:
        btst.l #0x3,%d0
m68k_00af62_end:
.org 0xAF66
m68k_00af66:
        beq.b (. + -10)
m68k_00af66_end:
.org 0xAF68
m68k_00af68:
        rts
m68k_00af68_end:
.org 0xAF6A
m68k_00af6a:
        lsr.w #0x3,%d0
m68k_00af6a_end:
.org 0xAF6C
m68k_00af6c:
        lsr.w #0x3,%d1
m68k_00af6c_end:
.org 0xAF6E
m68k_00af6e:
        movem.l %d0-%d1,-(%a7)
m68k_00af6e_end:
.org 0xAF72
m68k_00af72:
        move.b 0x2(%a0),%d4
m68k_00af72_end:
.org 0xAF76
m68k_00af76:
        ext.w %d4
m68k_00af76_end:
.org 0xAF78
m68k_00af78:
        ext.l %d0
m68k_00af78_end:
.org 0xAF7A
m68k_00af7a:
        divu.w %d4,%d0
m68k_00af7a_end:
.org 0xAF7C
m68k_00af7c:
        move.l %d0,%d2
m68k_00af7c_end:
.org 0xAF7E
m68k_00af7e:
        swap %d2
m68k_00af7e_end:
.org 0xAF80
m68k_00af80:
        move.b 0x3(%a0),%d5
m68k_00af80_end:
.org 0xAF84
m68k_00af84:
        ext.w %d5
m68k_00af84_end:
.org 0xAF86
m68k_00af86:
        ext.l %d1
m68k_00af86_end:
.org 0xAF88
m68k_00af88:
        divu.w %d5,%d1
m68k_00af88_end:
.org 0xAF8A
m68k_00af8a:
        move.l %d1,%d3
m68k_00af8a_end:
.org 0xAF8C
m68k_00af8c:
        swap %d3
m68k_00af8c_end:
.org 0xAF8E
m68k_00af8e:
        movea.l 0x4(%a0),%a4
m68k_00af8e_end:
.org 0xAF92
m68k_00af92:
        mulu.w (%a0),%d0
m68k_00af92_end:
.org 0xAF94
m68k_00af94:
        add.w %d1,%d0
m68k_00af94_end:
.org 0xAF96
m68k_00af96:
        lsl.w #0x1,%d0
m68k_00af96_end:
.org 0xAF98
m68k_00af98:
        move.w 0x8(%a0, %d0.w),%d1
m68k_00af98_end:
.org 0xAF9C
m68k_00af9c:
        cmpi.w #0xffff,%d1
m68k_00af9c_end:
.org 0xAFA0
m68k_00afa0:
        bne.b (. + 10)
m68k_00afa0_end:
.org 0xAFAA
m68k_00afaa:
        movea.l %a4,%a1
m68k_00afaa_end:
.org 0xAFAC
m68k_00afac:
        andi.l #0xffff,%d1
m68k_00afac_end:
.org 0xAFB2
m68k_00afb2:
        adda.l %d1,%a1
m68k_00afb2_end:
.org 0xAFB4
m68k_00afb4:
        tst.w 0xf328:w
m68k_00afb4_end:
.org 0xAFB8
m68k_00afb8:
        bne.b (. + 88)
m68k_00afb8_end:
.org 0xAFBA
m68k_00afba:
        move.w 0xa(%a0, %d0.w),%d1
m68k_00afba_end:
.org 0xAFBE
m68k_00afbe:
        bpl.b (. + 10)
m68k_00afbe_end:
.org 0xAFC8
m68k_00afc8:
        movea.l %a4,%a2
m68k_00afc8_end:
.org 0xAFCA
m68k_00afca:
        andi.l #0xffff,%d1
m68k_00afca_end:
.org 0xAFD0
m68k_00afd0:
        adda.l %d1,%a2
m68k_00afd0_end:
.org 0xAFD2
m68k_00afd2:
        move.w 0xc(%a0, %d0.w),%d1
m68k_00afd2_end:
.org 0xAFD6
m68k_00afd6:
        cmpi.w #0xffff,%d1
m68k_00afd6_end:
.org 0xAFDA
m68k_00afda:
        bne.b (. + 10)
m68k_00afda_end:
.org 0xAFE4
m68k_00afe4:
        movea.l %a4,%a3
m68k_00afe4_end:
.org 0xAFE6
m68k_00afe6:
        andi.l #0xffff,%d1
m68k_00afe6_end:
.org 0xAFEC
m68k_00afec:
        adda.l %d1,%a3
m68k_00afec_end:
.org 0xAFEE
m68k_00afee:
        move.w 0xe(%a0, %d0.w),%d1
m68k_00afee_end:
.org 0xAFF2
m68k_00aff2:
        cmpi.w #0xffff,%d1
m68k_00aff2_end:
.org 0xAFF6
m68k_00aff6:
        bne.b (. + 10)
m68k_00aff6_end:
.org 0xB000
m68k_00b000:
        movea.l %a4,%a5
m68k_00b000_end:
.org 0xB002
m68k_00b002:
        andi.l #0xffff,%d1
m68k_00b002_end:
.org 0xB008
m68k_00b008:
        adda.l %d1,%a5
m68k_00b008_end:
.org 0xB00A
m68k_00b00a:
        movem.l (%a7)+,%d0-%d1
m68k_00b00a_end:
.org 0xB00E
m68k_00b00e:
        rts
m68k_00b00e_end:
.org 0xB010
m68k_00b010:
        add.w (%a0),%d0
m68k_00b010_end:
.org 0xB012
m68k_00b012:
        add.w (%a0),%d0
m68k_00b012_end:
.org 0xB014
m68k_00b014:
        move.w 0x8(%a0, %d0.w),%d1
m68k_00b014_end:
.org 0xB018
m68k_00b018:
        cmpi.w #0xffff,%d1
m68k_00b018_end:
.org 0xB01C
m68k_00b01c:
        bne.b (. + 10)
m68k_00b01c_end:
.org 0xB026
m68k_00b026:
        movea.l %a4,%a2
m68k_00b026_end:
.org 0xB028
m68k_00b028:
        andi.l #0xffff,%d1
m68k_00b028_end:
.org 0xB02E
m68k_00b02e:
        adda.l %d1,%a2
m68k_00b02e_end:
.org 0xB030
m68k_00b030:
        add.w (%a0),%d0
m68k_00b030_end:
.org 0xB032
m68k_00b032:
        add.w (%a0),%d0
m68k_00b032_end:
.org 0xB034
m68k_00b034:
        move.w 0x8(%a0, %d0.w),%d1
m68k_00b034_end:
.org 0xB038
m68k_00b038:
        cmpi.w #0xffff,%d1
m68k_00b038_end:
.org 0xB03C
m68k_00b03c:
        bne.w (. + 12)
m68k_00b03c_end:
.org 0xB048
m68k_00b048:
        movea.l %a4,%a3
m68k_00b048_end:
.org 0xB04A
m68k_00b04a:
        andi.l #0xffff,%d1
m68k_00b04a_end:
.org 0xB050
m68k_00b050:
        adda.l %d1,%a3
m68k_00b050_end:
.org 0xB052
m68k_00b052:
        bra.b (. + -72)
m68k_00b052_end:
.org 0xB054
m68k_00b054:
        ext.l %d0
m68k_00b054_end:
.org 0xB056
m68k_00b056:
        divu.w #0x40,%d0
m68k_00b056_end:
.org 0xB05A
m68k_00b05a:
        swap %d0
m68k_00b05a_end:
.org 0xB05C
m68k_00b05c:
        mulu.w #0x40,%d0
m68k_00b05c_end:
.org 0xB060
m68k_00b060:
        ext.l %d1
m68k_00b060_end:
.org 0xB062
m68k_00b062:
        divu.w #0x40,%d1
m68k_00b062_end:
.org 0xB066
m68k_00b066:
        swap %d1
m68k_00b066_end:
.org 0xB068
m68k_00b068:
        add.w %d1,%d0
m68k_00b068_end:
.org 0xB06A
m68k_00b06a:
        lsl.w #0x1,%d0
m68k_00b06a_end:
.org 0xB06C
m68k_00b06c:
        rts
m68k_00b06c_end:
.org 0xB06E
m68k_00b06e:
        bsr.b (. + 112)
m68k_00b06e_end:
.org 0xB070
m68k_00b070:
        bsr.w (. + 150)
m68k_00b070_end:
.org 0xB074
m68k_00b074:
        move.w %d5,%d0
m68k_00b074_end:
.org 0xB076
m68k_00b076:
        sub.w %d3,%d0
m68k_00b076_end:
.org 0xB078
m68k_00b078:
        move.w %d6,(%a0)+
m68k_00b078_end:
.org 0xB07A
m68k_00b07a:
        subq.w #0x1,%d1
m68k_00b07a_end:
.org 0xB07C
m68k_00b07c:
        beq.b (. + 50)
m68k_00b07c_end:
.org 0xB07E
m68k_00b07e:
        subq.w #0x1,%d0
m68k_00b07e_end:
.org 0xB080
m68k_00b080:
        beq.b (. + 28)
m68k_00b080_end:
.org 0xB082
m68k_00b082:
        cmpi.l #0x10000,%d7
m68k_00b082_end:
.org 0xB088
m68k_00b088:
        bcc.b (. + 8)
m68k_00b088_end:
.org 0xB08A
m68k_00b08a:
        dbra %d7,(. + -18)
m68k_00b08a_end:
.org 0xB08E
m68k_00b08e:
        bra.b (. + 8)
m68k_00b08e_end:
.org 0xB090
m68k_00b090:
        addq.w #0x1,%d6
m68k_00b090_end:
.org 0xB092
m68k_00b092:
        dbra %d7,(. + -26)
m68k_00b092_end:
.org 0xB096
m68k_00b096:
        bsr.w (. + 324)
m68k_00b096_end:
.org 0xB09A
m68k_00b09a:
        bra.b (. + -34)
m68k_00b09a_end:
.org 0xB09C
m68k_00b09c:
        movea.l %a2,%a1
m68k_00b09c_end:
.org 0xB09E
m68k_00b09e:
        movea.l %a3,%a2
m68k_00b09e_end:
.org 0xB0A0
m68k_00b0a0:
        movea.l %a5,%a3
m68k_00b0a0_end:
.org 0xB0A2
m68k_00b0a2:
        clr.w %d3
m68k_00b0a2_end:
.org 0xB0A4
m68k_00b0a4:
        move.w %d5,%d0
m68k_00b0a4_end:
.org 0xB0A6
m68k_00b0a6:
        bsr.b (. + 56)
m68k_00b0a6_end:
.org 0xB0A8
m68k_00b0a8:
        bsr.w (. + 306)
m68k_00b0a8_end:
.org 0xB0AC
m68k_00b0ac:
        bra.b (. + -52)
m68k_00b0ac_end:
.org 0xB0AE
m68k_00b0ae:
        clr.w (%a0)
m68k_00b0ae_end:
.org 0xB0B0
m68k_00b0b0:
        rts
m68k_00b0b0_end:
.org 0xB0B2
m68k_00b0b2:
        andi.w #0x7fff,%d1
m68k_00b0b2_end:
.org 0xB0B6
m68k_00b0b6:
        bsr.b (. + 40)
m68k_00b0b6_end:
.org 0xB0B8
m68k_00b0b8:
        bsr.b (. + 78)
m68k_00b0b8_end:
.org 0xB0BA
m68k_00b0ba:
        move.w %d6,(%a0)+
m68k_00b0ba_end:
.org 0xB0BC
m68k_00b0bc:
        subq.w #0x1,%d1
m68k_00b0bc_end:
.org 0xB0BE
m68k_00b0be:
        beq.b (. + 28)
m68k_00b0be_end:
.org 0xB0C0
m68k_00b0c0:
        addq.w #0x1,%d2
m68k_00b0c0_end:
.org 0xB0C2
m68k_00b0c2:
        cmp.w %d4,%d2
m68k_00b0c2_end:
.org 0xB0C4
m68k_00b0c4:
        beq.b (. + 8)
m68k_00b0c4_end:
.org 0xB0C6
m68k_00b0c6:
        bsr.b (. + 24)
m68k_00b0c6_end:
.org 0xB0C8
m68k_00b0c8:
        bsr.b (. + 62)
m68k_00b0c8_end:
.org 0xB0CA
m68k_00b0ca:
        bra.b (. + -16)
m68k_00b0ca_end:
.org 0xB0CC
m68k_00b0cc:
        clr.w %d2
m68k_00b0cc_end:
.org 0xB0CE
m68k_00b0ce:
        movea.l %a2,%a1
m68k_00b0ce_end:
.org 0xB0D0
m68k_00b0d0:
        movea.l %a3,%a2
m68k_00b0d0_end:
.org 0xB0D2
m68k_00b0d2:
        move.w %d5,%d0
m68k_00b0d2_end:
.org 0xB0D4
m68k_00b0d4:
        bsr.b (. + 10)
m68k_00b0d4_end:
.org 0xB0D6
m68k_00b0d6:
        bsr.b (. + 48)
m68k_00b0d6_end:
.org 0xB0D8
m68k_00b0d8:
        bra.b (. + -30)
m68k_00b0d8_end:
.org 0xB0DA
m68k_00b0da:
        clr.w (%a0)
m68k_00b0da_end:
.org 0xB0DC
m68k_00b0dc:
        rts
m68k_00b0dc_end:
.org 0xB0DE
m68k_00b0de:
        movem.l %d0/%d2/%a0,-(%a7)
m68k_00b0de_end:
.org 0xB0E2
m68k_00b0e2:
        move.l %a1,%d0
m68k_00b0e2_end:
.org 0xB0E4
m68k_00b0e4:
        bpl.b (. + 6)
m68k_00b0e4_end:
.org 0xB0EA
m68k_00b0ea:
        movea.l (%a1),%a0
m68k_00b0ea_end:
.org 0xB0EC
m68k_00b0ec:
        move.w %d5,%d6
m68k_00b0ec_end:
.org 0xB0EE
m68k_00b0ee:
        lsr.w #0x1,%d6
m68k_00b0ee_end:
.org 0xB0F0
m68k_00b0f0:
        cmp.w %d6,%d3
m68k_00b0f0_end:
.org 0xB0F2
m68k_00b0f2:
        bcs.b (. + 4)
m68k_00b0f2_end:
.org 0xB0F4
m68k_00b0f4:
        addq.w #0x1,%d2
m68k_00b0f4_end:
.org 0xB0F6
m68k_00b0f6:
        lsl.w #0x1,%d2
m68k_00b0f6_end:
.org 0xB0F8
m68k_00b0f8:
        move.w 0x4(%a1, %d2.w),%d2
m68k_00b0f8_end:
.org 0xB0FC
m68k_00b0fc:
        lea.l (%a0, %d2.w),%a4
m68k_00b0fc_end:
.org 0xB100
m68k_00b100:
        movem.l (%a7)+,%d0/%d2/%a0
m68k_00b100_end:
.org 0xB104
m68k_00b104:
        rts
m68k_00b104_end:
.org 0xB106
m68k_00b106:
        move.l %a4,%d7
m68k_00b106_end:
.org 0xB108
m68k_00b108:
        bmi.b (. + 82)
m68k_00b108_end:
.org 0xB10A
m68k_00b10a:
        move.w %d5,%d6
m68k_00b10a_end:
.org 0xB10C
m68k_00b10c:
        lsr.w #0x1,%d6
m68k_00b10c_end:
.org 0xB10E
m68k_00b10e:
        cmp.w %d6,%d3
m68k_00b10e_end:
.org 0xB110
m68k_00b110:
        bcc.b (. + 80)
m68k_00b110_end:
.org 0xB112
m68k_00b112:
        move.w %d3,%d7
m68k_00b112_end:
.org 0xB114
m68k_00b114:
        addq.w #0x1,%d7
m68k_00b114_end:
.org 0xB116
m68k_00b116:
        move.w (%a4)+,%d6
m68k_00b116_end:
.org 0xB118
m68k_00b118:
        move.w %d6,%d0
m68k_00b118_end:
.org 0xB11A
m68k_00b11a:
        andi.w #0x7ff,%d0
m68k_00b11a_end:
.org 0xB11E
m68k_00b11e:
        subi.w #0x6ff,%d0
m68k_00b11e_end:
.org 0xB122
m68k_00b122:
        bcc.b (. + 10)
m68k_00b122_end:
.org 0xB124
m68k_00b124:
        subq.w #0x1,%d7
m68k_00b124_end:
.org 0xB126
m68k_00b126:
        bne.b (. + -16)
m68k_00b126_end:
.org 0xB128
m68k_00b128:
        moveq #0,%d7
m68k_00b128_end:
.org 0xB12A
m68k_00b12a:
        rts
m68k_00b12a_end:
.org 0xB12C
m68k_00b12c:
        move.w (%a4)+,%d6
m68k_00b12c_end:
.org 0xB12E
m68k_00b12e:
        andi.l #0xffff,%d7
m68k_00b12e_end:
.org 0xB134
m68k_00b134:
        btst.l #0x7,%d0
m68k_00b134_end:
.org 0xB138
m68k_00b138:
        beq.b (. + 12)
m68k_00b138_end:
.org 0xB13A
m68k_00b13a:
        bclr.l #0x7,%d0
m68k_00b13a_end:
.org 0xB13E
m68k_00b13e:
        ori.l #0x10000,%d7
m68k_00b13e_end:
.org 0xB144
m68k_00b144:
        sub.w %d0,%d7
m68k_00b144_end:
.org 0xB146
m68k_00b146:
        bhi.b (. + -48)
m68k_00b146_end:
.org 0xB148
m68k_00b148:
        neg.w %d7
m68k_00b148_end:
.org 0xB14A
m68k_00b14a:
        cmpi.l #0x10000,%d7
m68k_00b14a_end:
.org 0xB150
m68k_00b150:
        bcs.b (. + 8)
m68k_00b150_end:
.org 0xB152
m68k_00b152:
        sub.w %d7,%d0
m68k_00b152_end:
.org 0xB154
m68k_00b154:
        subq.w #0x1,%d0
m68k_00b154_end:
.org 0xB156
m68k_00b156:
        add.w %d0,%d6
m68k_00b156_end:
.org 0xB158
m68k_00b158:
        rts
m68k_00b158_end:
.org 0xB160
m68k_00b160:
        move.w %d5,%d7
m68k_00b160_end:
.org 0xB162
m68k_00b162:
        subq.w #0x1,%d7
m68k_00b162_end:
.org 0xB164
m68k_00b164:
        subq.w #0x2,%a4
m68k_00b164_end:
.org 0xB166
m68k_00b166:
        cmp.w %d3,%d7
m68k_00b166_end:
.org 0xB168
m68k_00b168:
        beq.b (. + 20)
m68k_00b168_end:
.org 0xB16A
m68k_00b16a:
        move.w -0x2(%a4),%d0
m68k_00b16a_end:
.org 0xB16E
m68k_00b16e:
        andi.w #0x7ff,%d0
m68k_00b16e_end:
.org 0xB172
m68k_00b172:
        subi.w #0x700,%d0
m68k_00b172_end:
.org 0xB176
m68k_00b176:
        bcc.b (. + 30)
m68k_00b176_end:
.org 0xB178
m68k_00b178:
        subq.w #0x1,%d7
m68k_00b178_end:
.org 0xB17A
m68k_00b17a:
        bra.b (. + -22)
m68k_00b17a_end:
.org 0xB17C
m68k_00b17c:
        clr.l %d7
m68k_00b17c_end:
.org 0xB17E
m68k_00b17e:
        move.w (%a4),%d6
m68k_00b17e_end:
.org 0xB180
m68k_00b180:
        move.w -0x2(%a4),%d0
m68k_00b180_end:
.org 0xB184
m68k_00b184:
        andi.w #0x7ff,%d0
m68k_00b184_end:
.org 0xB188
m68k_00b188:
        subi.w #0x780,%d0
m68k_00b188_end:
.org 0xB18C
m68k_00b18c:
        bcs.b (. + 4)
m68k_00b18c_end:
.org 0xB18E
m68k_00b18e:
        add.w %d0,%d6
m68k_00b18e_end:
.org 0xB190
m68k_00b190:
        addq.w #0x2,%a4
m68k_00b190_end:
.org 0xB192
m68k_00b192:
        rts
m68k_00b192_end:
.org 0xB194
m68k_00b194:
        andi.l #0xffff,%d7
m68k_00b194_end:
.org 0xB19A
m68k_00b19a:
        btst.l #0x7,%d0
m68k_00b19a_end:
.org 0xB19E
m68k_00b19e:
        beq.b (. + 12)
m68k_00b19e_end:
.org 0xB1A0
m68k_00b1a0:
        bclr.l #0x7,%d0
m68k_00b1a0_end:
.org 0xB1A4
m68k_00b1a4:
        ori.l #0x10000,%d7
m68k_00b1a4_end:
.org 0xB1AA
m68k_00b1aa:
        sub.w %d0,%d7
m68k_00b1aa_end:
.org 0xB1AC
m68k_00b1ac:
        cmp.w %d3,%d7
m68k_00b1ac_end:
.org 0xB1AE
m68k_00b1ae:
        bls.b (. + 8)
m68k_00b1ae_end:
.org 0xB1B0
m68k_00b1b0:
        subq.w #0x2,%a4
m68k_00b1b0_end:
.org 0xB1B2
m68k_00b1b2:
        subq.w #0x1,%d7
m68k_00b1b2_end:
.org 0xB1B4
m68k_00b1b4:
        bra.b (. + -80)
m68k_00b1b4_end:
.org 0xB1B6
m68k_00b1b6:
        movem.l %d3,-(%a7)
m68k_00b1b6_end:
.org 0xB1BA
m68k_00b1ba:
        sub.w %d7,%d3
m68k_00b1ba_end:
.org 0xB1BC
m68k_00b1bc:
        move.w %d0,%d6
m68k_00b1bc_end:
.org 0xB1BE
m68k_00b1be:
        sub.w %d3,%d0
m68k_00b1be_end:
.org 0xB1C0
m68k_00b1c0:
        move.w %d0,%d7
m68k_00b1c0_end:
.org 0xB1C2
m68k_00b1c2:
        clr.w %d0
m68k_00b1c2_end:
.org 0xB1C4
m68k_00b1c4:
        cmpi.l #0x10000,%d7
m68k_00b1c4_end:
.org 0xB1CA
m68k_00b1ca:
        bcs.b (. + 6)
m68k_00b1ca_end:
.org 0xB1CC
m68k_00b1cc:
        sub.w %d7,%d6
m68k_00b1cc_end:
.org 0xB1CE
m68k_00b1ce:
        move.w %d6,%d0
m68k_00b1ce_end:
.org 0xB1D0
m68k_00b1d0:
        add.w (%a4)+,%d0
m68k_00b1d0_end:
.org 0xB1D2
m68k_00b1d2:
        move.w %d0,%d6
m68k_00b1d2_end:
.org 0xB1D4
m68k_00b1d4:
        movem.l (%a7)+,%d3
m68k_00b1d4_end:
.org 0xB1D8
m68k_00b1d8:
        rts
m68k_00b1d8_end:
.org 0xB1DA
m68k_00b1da:
        move.l %a1,%d7
m68k_00b1da_end:
.org 0xB1DC
m68k_00b1dc:
        bmi.b (. + 46)
m68k_00b1dc_end:
.org 0xB1DE
m68k_00b1de:
        move.w (%a4)+,%d6
m68k_00b1de_end:
.org 0xB1E0
m68k_00b1e0:
        move.w %d6,%d7
m68k_00b1e0_end:
.org 0xB1E2
m68k_00b1e2:
        andi.w #0x7ff,%d7
m68k_00b1e2_end:
.org 0xB1E6
m68k_00b1e6:
        subi.w #0x700,%d7
m68k_00b1e6_end:
.org 0xB1EA
m68k_00b1ea:
        bcc.b (. + 6)
m68k_00b1ea_end:
.org 0xB1EC
m68k_00b1ec:
        clr.l %d7
m68k_00b1ec_end:
.org 0xB1EE
m68k_00b1ee:
        rts
m68k_00b1ee_end:
.org 0xB1F0
m68k_00b1f0:
        andi.l #0xffff,%d7
m68k_00b1f0_end:
.org 0xB1F6
m68k_00b1f6:
        btst.l #0x7,%d7
m68k_00b1f6_end:
.org 0xB1FA
m68k_00b1fa:
        beq.b (. + 12)
m68k_00b1fa_end:
.org 0xB1FC
m68k_00b1fc:
        bclr.l #0x7,%d7
m68k_00b1fc_end:
.org 0xB200
m68k_00b200:
        ori.l #0x10000,%d7
m68k_00b200_end:
.org 0xB206
m68k_00b206:
        move.w (%a4)+,%d6
m68k_00b206_end:
.org 0xB208
m68k_00b208:
        rts
m68k_00b208_end:
.org 0xBAEA
m68k_00baea:
        move.w #0x2700,%sr
m68k_00baea_end:
.org 0xBAEE
m68k_00baee:
        lea.l 0xc00000:l,%a6
m68k_00baee_end:
.org 0xBAF4
m68k_00baf4:
        move.w #0x1,%d0
m68k_00baf4_end:
.org 0xBAF8
m68k_00baf8:
        move.w #0x3,%d1
m68k_00baf8_end:
.org 0xBAFC
m68k_00bafc:
        bsr.w (. + 42)
m68k_00bafc_end:
.org 0xBB00
m68k_00bb00:
        bsr.w (. + -26876)
m68k_00bb00_end:
.org 0xBB04
m68k_00bb04:
        bsr.w (. + -26690)
m68k_00bb04_end:
.org 0xBB08
m68k_00bb08:
        bsr.w (. + -25944)
m68k_00bb08_end:
.org 0xBB0C
m68k_00bb0c:
        move.w #0x208,0xf612:w
m68k_00bb0c_end:
.org 0xBB12
m68k_00bb12:
        clr.w 0xf362:w
m68k_00bb12_end:
.org 0xBB16
m68k_00bb16:
        clr.w 0xf36a:w
m68k_00bb16_end:
.org 0xBB1A
m68k_00bb1a:
        clr.w 0xf394:w
m68k_00bb1a_end:
.org 0xBB1E
m68k_00bb1e:
        jsr 0xaf48:l
m68k_00bb1e_end:
.org 0xBB24
m68k_00bb24:
        rts
m68k_00bb24_end:
.org 0xBB26
m68k_00bb26:
        move.w #0x1f,%d2
m68k_00bb26_end:
.org 0xBB2A
m68k_00bb2a:
        lea.l 0xd300:w,%a0
m68k_00bb2a_end:
.org 0xBB2E
m68k_00bb2e:
        move.l #0x11111111,(%a0)+
m68k_00bb2e_end:
.org 0xBB34
m68k_00bb34:
        dbra %d2,(. + -6)
m68k_00bb34_end:
.org 0xBB38
m68k_00bb38:
        move.w 0xf38c:w,%d7
m68k_00bb38_end:
.org 0xBB3C
m68k_00bb3c:
        lea.l 0x92878:l,%a1
m68k_00bb3c_end:
.org 0xBB42
m68k_00bb42:
        movea.l (%a1),%a2
m68k_00bb42_end:
.org 0xBB44
m68k_00bb44:
        lsl.w #0x1,%d7
m68k_00bb44_end:
.org 0xBB46
m68k_00bb46:
        move.w 0x4(%a1, %d7.w),%d7
m68k_00bb46_end:
.org 0xBB4A
m68k_00bb4a:
        adda.w %d7,%a2
m68k_00bb4a_end:
.org 0xBB4C
m68k_00bb4c:
        clr.w %d7
m68k_00bb4c_end:
.org 0xBB4E
m68k_00bb4e:
        move.b 0x1(%a2),%d7
m68k_00bb4e_end:
.org 0xBB52
m68k_00bb52:
        move.w %d7,0xf380:w
m68k_00bb52_end:
.org 0xBB56
m68k_00bb56:
        cmpi.w #0x60,%d7
m68k_00bb56_end:
.org 0xBB5A
m68k_00bb5a:
        bcc.w (. + 68)
m68k_00bb5a_end:
.org 0xBB5E
m68k_00bb5e:
        move.w %d7,%d6
m68k_00bb5e_end:
.org 0xBB60
m68k_00bb60:
        lsl.w #0x1,%d7
m68k_00bb60_end:
.org 0xBB62
m68k_00bb62:
        add.w %d6,%d7
m68k_00bb62_end:
.org 0xBB64
m68k_00bb64:
        lsl.w #0x1,%d7
m68k_00bb64_end:
.org 0xBB66
m68k_00bb66:
        lea.l 56(%pc),%a1
m68k_00bb66_end:
.org 0xBB6A
m68k_00bb6a:
        movea.l (%a1, %d7.w),%a0
m68k_00bb6a_end:
.org 0xBB6E
m68k_00bb6e:
        move.w 0x4(%a1, %d7.w),%d3
m68k_00bb6e_end:
.org 0xBB72
m68k_00bb72:
        move.w %d3,%d7
m68k_00bb72_end:
.org 0xBB74
m68k_00bb74:
        lea.l 0xd380:w,%a1
m68k_00bb74_end:
.org 0xBB78
m68k_00bb78:
        jsr 0xae8a:l
m68k_00bb78_end:
.org 0xBB7E
m68k_00bb7e:
        move.l #0x40200000,0xc00004:l
m68k_00bb7e_end:
.org 0xBB88
m68k_00bb88:
        clr.w 0xf37e:w
m68k_00bb88_end:
.org 0xBB8C
m68k_00bb8c:
        lea.l 0xd300:w,%a0
m68k_00bb8c_end:
.org 0xBB90
m68k_00bb90:
        addq.w #0x1,%d7
m68k_00bb90_end:
.org 0xBB92
m68k_00bb92:
        lsl.w #0x5,%d7
m68k_00bb92_end:
.org 0xBB94
m68k_00bb94:
        addi.w #0x1f,%d7
m68k_00bb94_end:
.org 0xBB98
m68k_00bb98:
        move.l (%a0)+,(%a6)
m68k_00bb98_end:
.org 0xBB9A
m68k_00bb9a:
        dbra %d7,(. + -2)
m68k_00bb9a_end:
.org 0xBB9E
m68k_00bb9e:
        rts
m68k_00bb9e_end:
.org 0xBBDA
m68k_00bbda:
        lea.l 0xd100:w,%a0
m68k_00bbda_end:
.org 0xBBDE
m68k_00bbde:
        adda.w 0xf31a:w,%a0
m68k_00bbde_end:
.org 0xBBE2
m68k_00bbe2:
        move.w 0xf36a:w,%d0
m68k_00bbe2_end:
.org 0xBBE6
m68k_00bbe6:
        lsl.w #0x1,%d0
m68k_00bbe6_end:
.org 0xBBE8
m68k_00bbe8:
        move.w 12(%pc, %d0.w),%d0
m68k_00bbe8_end:
.org 0xBBEC
m68k_00bbec:
        lea.l 54(%pc),%a1
m68k_00bbec_end:
.org 0xBBF0
m68k_00bbf0:
        jsr (%a1, %d0.w)
m68k_00bbf0_end:
.org 0xBBF4
m68k_00bbf4:
        rts
m68k_00bbf4_end:
.org 0xBC24
m68k_00bc24:
        move.w #0x10,(%a0)+
m68k_00bc24_end:
.org 0xBC28
m68k_00bc28:
        move.w #0xc318,(%a0)+
m68k_00bc28_end:
.org 0xBC2C
m68k_00bc2c:
        move.w #0xc380,(%a0)+
m68k_00bc2c_end:
.org 0xBC30
m68k_00bc30:
        move.w #0xd,%d0
m68k_00bc30_end:
.org 0xBC34
m68k_00bc34:
        move.w #0xc381,(%a0)+
m68k_00bc34_end:
.org 0xBC38
m68k_00bc38:
        dbra %d0,(. + -4)
m68k_00bc38_end:
.org 0xBC3C
m68k_00bc3c:
        move.w #0xcb80,(%a0)+
m68k_00bc3c_end:
.org 0xBC40
m68k_00bc40:
        clr.w (%a0)
m68k_00bc40_end:
.org 0xBC42
m68k_00bc42:
        addq.w #0x1,0xf36a:w
m68k_00bc42_end:
.org 0xBC46
m68k_00bc46:
        addi.w #0x18,0xf31a:w
m68k_00bc46_end:
.org 0xBC4C
m68k_00bc4c:
        rts
m68k_00bc4c_end:
.org 0xBC4E
m68k_00bc4e:
        move.w #0x10,0x24(%a0)
m68k_00bc4e_end:
.org 0xBC54
m68k_00bc54:
        move.w #0x10,(%a0)+
m68k_00bc54_end:
.org 0xBC58
m68k_00bc58:
        move.w 0xf36a:w,%d0
m68k_00bc58_end:
.org 0xBC5C
m68k_00bc5c:
        subq.w #0x1,%d0
m68k_00bc5c_end:
.org 0xBC5E
m68k_00bc5e:
        move.w %d0,%d1
m68k_00bc5e_end:
.org 0xBC60
m68k_00bc60:
        lsl.w #0x1,%d0
m68k_00bc60_end:
.org 0xBC62
m68k_00bc62:
        add.w %d1,%d0
m68k_00bc62_end:
.org 0xBC64
m68k_00bc64:
        lsl.w #0x7,%d0
m68k_00bc64_end:
.org 0xBC66
m68k_00bc66:
        addi.w #0xc418,%d0
m68k_00bc66_end:
.org 0xBC6A
m68k_00bc6a:
        move.w %d0,0x24(%a0)
m68k_00bc6a_end:
.org 0xBC6E
m68k_00bc6e:
        subi.w #0x80,%d0
m68k_00bc6e_end:
.org 0xBC72
m68k_00bc72:
        move.w %d0,(%a0)+
m68k_00bc72_end:
.org 0xBC74
m68k_00bc74:
        move.w #0xc382,0x24(%a0)
m68k_00bc74_end:
.org 0xBC7A
m68k_00bc7a:
        move.w #0xc382,(%a0)+
m68k_00bc7a_end:
.org 0xBC7E
m68k_00bc7e:
        move.w 0xf36a:w,%d0
m68k_00bc7e_end:
.org 0xBC82
m68k_00bc82:
        subq.w #0x1,%d0
m68k_00bc82_end:
.org 0xBC84
m68k_00bc84:
        move.w %d0,%d1
m68k_00bc84_end:
.org 0xBC86
m68k_00bc86:
        lsl.w #0x1,%d0
m68k_00bc86_end:
.org 0xBC88
m68k_00bc88:
        add.w %d1,%d0
m68k_00bc88_end:
.org 0xBC8A
m68k_00bc8a:
        lsl.w #0x3,%d0
m68k_00bc8a_end:
.org 0xBC8C
m68k_00bc8c:
        addi.w #0xc005,%d0
m68k_00bc8c_end:
.org 0xBC90
m68k_00bc90:
        bsr.w (. + 74)
m68k_00bc90_end:
.org 0xBC94
m68k_00bc94:
        bsr.w (. + 70)
m68k_00bc94_end:
.org 0xBC98
m68k_00bc98:
        move.w #0xc001,0x24(%a0)
m68k_00bc98_end:
.org 0xBC9E
m68k_00bc9e:
        move.w #0xc001,(%a0)+
m68k_00bc9e_end:
.org 0xBCA2
m68k_00bca2:
        bsr.w (. + 56)
m68k_00bca2_end:
.org 0xBCA6
m68k_00bca6:
        bsr.w (. + 52)
m68k_00bca6_end:
.org 0xBCAA
m68k_00bcaa:
        move.w #0xc001,0x24(%a0)
m68k_00bcaa_end:
.org 0xBCB0
m68k_00bcb0:
        move.w #0xc001,(%a0)+
m68k_00bcb0_end:
.org 0xBCB4
m68k_00bcb4:
        bsr.w (. + 38)
m68k_00bcb4_end:
.org 0xBCB8
m68k_00bcb8:
        bsr.w (. + 34)
m68k_00bcb8_end:
.org 0xBCBC
m68k_00bcbc:
        move.w #0xcb82,0x24(%a0)
m68k_00bcbc_end:
.org 0xBCC2
m68k_00bcc2:
        move.w #0xcb82,(%a0)+
m68k_00bcc2_end:
.org 0xBCC6
m68k_00bcc6:
        clr.w 0x24(%a0)
m68k_00bcc6_end:
.org 0xBCCA
m68k_00bcca:
        adda.w #0x24,%a0
m68k_00bcca_end:
.org 0xBCCE
m68k_00bcce:
        addq.w #0x1,0xf36a:w
m68k_00bcce_end:
.org 0xBCD2
m68k_00bcd2:
        addi.w #0x30,0xf31a:w
m68k_00bcd2_end:
.org 0xBCD8
m68k_00bcd8:
        rts
m68k_00bcd8_end:
.org 0xBCDA
m68k_00bcda:
        move.w %d0,(%a0)
m68k_00bcda_end:
.org 0xBCDC
m68k_00bcdc:
        addq.w #0x1,%d0
m68k_00bcdc_end:
.org 0xBCDE
m68k_00bcde:
        move.w %d0,0x24(%a0)
m68k_00bcde_end:
.org 0xBCE2
m68k_00bce2:
        addq.w #0x1,%d0
m68k_00bce2_end:
.org 0xBCE4
m68k_00bce4:
        move.w %d0,0x2(%a0)
m68k_00bce4_end:
.org 0xBCE8
m68k_00bce8:
        addq.w #0x1,%d0
m68k_00bce8_end:
.org 0xBCEA
m68k_00bcea:
        move.w %d0,0x26(%a0)
m68k_00bcea_end:
.org 0xBCEE
m68k_00bcee:
        addq.w #0x1,%d0
m68k_00bcee_end:
.org 0xBCF0
m68k_00bcf0:
        addq.w #0x4,%a0
m68k_00bcf0_end:
.org 0xBCF2
m68k_00bcf2:
        rts
m68k_00bcf2_end:
.org 0xBCF4
m68k_00bcf4:
        move.w #0x10,(%a0)+
m68k_00bcf4_end:
.org 0xBCF8
m68k_00bcf8:
        move.w 0xf36a:w,%d0
m68k_00bcf8_end:
.org 0xBCFC
m68k_00bcfc:
        subq.w #0x1,%d0
m68k_00bcfc_end:
.org 0xBCFE
m68k_00bcfe:
        move.w %d0,%d1
m68k_00bcfe_end:
.org 0xBD00
m68k_00bd00:
        lsl.w #0x1,%d0
m68k_00bd00_end:
.org 0xBD02
m68k_00bd02:
        add.w %d1,%d0
m68k_00bd02_end:
.org 0xBD04
m68k_00bd04:
        lsl.w #0x7,%d0
m68k_00bd04_end:
.org 0xBD06
m68k_00bd06:
        addi.w #0xc318,%d0
m68k_00bd06_end:
.org 0xBD0A
m68k_00bd0a:
        move.w %d0,(%a0)+
m68k_00bd0a_end:
.org 0xBD0C
m68k_00bd0c:
        move.w #0xd380,(%a0)+
m68k_00bd0c_end:
.org 0xBD10
m68k_00bd10:
        move.w #0xd,%d0
m68k_00bd10_end:
.org 0xBD14
m68k_00bd14:
        move.w #0xd381,(%a0)+
m68k_00bd14_end:
.org 0xBD18
m68k_00bd18:
        dbra %d0,(. + -4)
m68k_00bd18_end:
.org 0xBD1C
m68k_00bd1c:
        move.w #0xdb80,(%a0)+
m68k_00bd1c_end:
.org 0xBD20
m68k_00bd20:
        clr.w (%a0)
m68k_00bd20_end:
.org 0xBD22
m68k_00bd22:
        addi.w #0x24,0xf31a:w
m68k_00bd22_end:
.org 0xBD28
m68k_00bd28:
        move.w 0xf380:w,%d0
m68k_00bd28_end:
.org 0xBD2C
m68k_00bd2c:
        lsl.w #0x2,%d0
m68k_00bd2c_end:
.org 0xBD2E
m68k_00bd2e:
        move.w 54(%pc, %d0.w),0xf382:w
m68k_00bd2e_end:
.org 0xBD34
m68k_00bd34:
        move.w 50(%pc, %d0.w),0xf384:w
m68k_00bd34_end:
.org 0xBD3A
m68k_00bd3a:
        bsr.w (. + 234)
m68k_00bd3a_end:
.org 0xBD3E
m68k_00bd3e:
        addq.w #0x1,0xf362:w
m68k_00bd3e_end:
.org 0xBD42
m68k_00bd42:
        move.w 0xf3a4:w,%d0
m68k_00bd42_end:
.org 0xBD46
m68k_00bd46:
        bclr.l #0xd,%d0
m68k_00bd46_end:
.org 0xBD4A
m68k_00bd4a:
        move.w %d0,0xf3a4:w
m68k_00bd4a_end:
.org 0xBD4E
m68k_00bd4e:
        tst.w 0xf38c:w
m68k_00bd4e_end:
.org 0xBD52
m68k_00bd52:
        bne.b (. + 6)
m68k_00bd52_end:
.org 0xBD58
m68k_00bd58:
        ori.w #0x8100,0xf3a4:w
m68k_00bd58_end:
.org 0xBD5E
m68k_00bd5e:
        jsr 0x676c4:l
m68k_00bd5e_end:
.org 0xBD64
m68k_00bd64:
        rts
m68k_00bd64_end:
.org 0xBD76
m68k_00bd76:
        move.w #0x10,0x48(%a0)
m68k_00bd76_end:
.org 0xBD7C
m68k_00bd7c:
        move.w #0x10,0x24(%a0)
m68k_00bd7c_end:
.org 0xBD82
m68k_00bd82:
        move.w #0x10,(%a0)+
m68k_00bd82_end:
.org 0xBD86
m68k_00bd86:
        move.w 0xf36a:w,%d0
m68k_00bd86_end:
.org 0xBD8A
m68k_00bd8a:
        subq.w #0x1,%d0
m68k_00bd8a_end:
.org 0xBD8C
m68k_00bd8c:
        move.w %d0,%d1
m68k_00bd8c_end:
.org 0xBD8E
m68k_00bd8e:
        lsl.w #0x1,%d0
m68k_00bd8e_end:
.org 0xBD90
m68k_00bd90:
        add.w %d1,%d0
m68k_00bd90_end:
.org 0xBD92
m68k_00bd92:
        lsl.w #0x7,%d0
m68k_00bd92_end:
.org 0xBD94
m68k_00bd94:
        addi.w #0xc498,%d0
m68k_00bd94_end:
.org 0xBD98
m68k_00bd98:
        move.w %d0,0x48(%a0)
m68k_00bd98_end:
.org 0xBD9C
m68k_00bd9c:
        subi.w #0x80,%d0
m68k_00bd9c_end:
.org 0xBDA0
m68k_00bda0:
        move.w %d0,0x24(%a0)
m68k_00bda0_end:
.org 0xBDA4
m68k_00bda4:
        subi.w #0x80,%d0
m68k_00bda4_end:
.org 0xBDA8
m68k_00bda8:
        move.w %d0,(%a0)+
m68k_00bda8_end:
.org 0xBDAA
m68k_00bdaa:
        move.w #0xc382,0x48(%a0)
m68k_00bdaa_end:
.org 0xBDB0
m68k_00bdb0:
        move.w #0xc382,0x24(%a0)
m68k_00bdb0_end:
.org 0xBDB6
m68k_00bdb6:
        move.w #0xc382,(%a0)+
m68k_00bdb6_end:
.org 0xBDBA
m68k_00bdba:
        move.w #0xd,%d0
m68k_00bdba_end:
.org 0xBDBE
m68k_00bdbe:
        clr.w %d1
m68k_00bdbe_end:
.org 0xBDC0
m68k_00bdc0:
        move.w #0xc001,0x48(%a0, %d1.w)
m68k_00bdc0_end:
.org 0xBDC6
m68k_00bdc6:
        addq.w #0x2,%d1
m68k_00bdc6_end:
.org 0xBDC8
m68k_00bdc8:
        dbra %d0,(. + -8)
m68k_00bdc8_end:
.org 0xBDCC
m68k_00bdcc:
        move.w 0xf36a:w,%d0
m68k_00bdcc_end:
.org 0xBDD0
m68k_00bdd0:
        subq.w #0x1,%d0
m68k_00bdd0_end:
.org 0xBDD2
m68k_00bdd2:
        move.w %d0,%d1
m68k_00bdd2_end:
.org 0xBDD4
m68k_00bdd4:
        lsl.w #0x1,%d0
m68k_00bdd4_end:
.org 0xBDD6
m68k_00bdd6:
        add.w %d1,%d0
m68k_00bdd6_end:
.org 0xBDD8
m68k_00bdd8:
        lsl.w #0x3,%d0
m68k_00bdd8_end:
.org 0xBDDA
m68k_00bdda:
        addi.w #0xc005,%d0
m68k_00bdda_end:
.org 0xBDDE
m68k_00bdde:
        bsr.w (. + -260)
m68k_00bdde_end:
.org 0xBDE2
m68k_00bde2:
        bsr.w (. + -264)
m68k_00bde2_end:
.org 0xBDE6
m68k_00bde6:
        move.w #0xc001,0x24(%a0)
m68k_00bde6_end:
.org 0xBDEC
m68k_00bdec:
        move.w #0xc001,(%a0)+
m68k_00bdec_end:
.org 0xBDF0
m68k_00bdf0:
        bsr.w (. + -278)
m68k_00bdf0_end:
.org 0xBDF4
m68k_00bdf4:
        bsr.w (. + -282)
m68k_00bdf4_end:
.org 0xBDF8
m68k_00bdf8:
        move.w #0xc001,0x24(%a0)
m68k_00bdf8_end:
.org 0xBDFE
m68k_00bdfe:
        move.w #0xc001,(%a0)+
m68k_00bdfe_end:
.org 0xBE02
m68k_00be02:
        bsr.w (. + -296)
m68k_00be02_end:
.org 0xBE06
m68k_00be06:
        bsr.w (. + -300)
m68k_00be06_end:
.org 0xBE0A
m68k_00be0a:
        move.w #0xcb82,0x48(%a0)
m68k_00be0a_end:
.org 0xBE10
m68k_00be10:
        move.w #0xcb82,0x24(%a0)
m68k_00be10_end:
.org 0xBE16
m68k_00be16:
        move.w #0xcb82,(%a0)+
m68k_00be16_end:
.org 0xBE1A
m68k_00be1a:
        clr.w 0x48(%a0)
m68k_00be1a_end:
.org 0xBE1E
m68k_00be1e:
        addq.w #0x1,0xf36a:w
m68k_00be1e_end:
.org 0xBE22
m68k_00be22:
        rts
m68k_00be22_end:
.org 0xBE24
m68k_00be24:
        move.w 0xf396:w,%d0
m68k_00be24_end:
.org 0xBE28
m68k_00be28:
        clr.w %d1
m68k_00be28_end:
.org 0xBE2A
m68k_00be2a:
        move.w 0xf384:w,%d2
m68k_00be2a_end:
.org 0xBE2E
m68k_00be2e:
        addq.w #0x1,%d2
m68k_00be2e_end:
.org 0xBE30
m68k_00be30:
        sub.w %d2,%d0
m68k_00be30_end:
.org 0xBE32
m68k_00be32:
        bcs.b (. + 6)
m68k_00be32_end:
.org 0xBE38
m68k_00be38:
        add.w %d2,%d0
m68k_00be38_end:
.org 0xBE3A
m68k_00be3a:
        move.w %d0,0xf388:w
m68k_00be3a_end:
.org 0xBE3E
m68k_00be3e:
        move.w %d1,0xf386:w
m68k_00be3e_end:
.org 0xBE42
m68k_00be42:
        rts
m68k_00be42_end:
.org 0xBEE6
m68k_00bee6:
        lea.l 0xd100:w,%a0
m68k_00bee6_end:
.org 0xBEEA
m68k_00beea:
        adda.w 0xf31a:w,%a0
m68k_00beea_end:
.org 0xBEEE
m68k_00beee:
        move.w #0x1a,(%a0)+
m68k_00beee_end:
.org 0xBEF2
m68k_00bef2:
        move.w 0xf36a:w,%d0
m68k_00bef2_end:
.org 0xBEF6
m68k_00bef6:
        lsl.w #0x7,%d0
m68k_00bef6_end:
.org 0xBEF8
m68k_00bef8:
        move.w #0xc904,%d1
m68k_00bef8_end:
.org 0xBEFC
m68k_00befc:
        sub.w %d0,%d1
m68k_00befc_end:
.org 0xBEFE
m68k_00befe:
        move.w %d1,(%a0)+
m68k_00befe_end:
.org 0xBF00
m68k_00bf00:
        move.w #0x1a,%d0
m68k_00bf00_end:
.org 0xBF04
m68k_00bf04:
        clr.w (%a0)+
m68k_00bf04_end:
.org 0xBF06
m68k_00bf06:
        dbra %d0,(. + -2)
m68k_00bf06_end:
.org 0xBF0A
m68k_00bf0a:
        addi.w #0x38,0xf31a:w
m68k_00bf0a_end:
.org 0xBF10
m68k_00bf10:
        btst.b #0x2,0xf38f:w
m68k_00bf10_end:
.org 0xBF16
m68k_00bf16:
        beq.w (. + 34)
m68k_00bf16_end:
.org 0xBF38
m68k_00bf38:
        rts
m68k_00bf38_end:
.org 0xBF5A
m68k_00bf5a:
        cmpi.w #0x12,0xf36a:w
m68k_00bf5a_end:
.org 0xBF60
m68k_00bf60:
        bcs.b (. + 50)
m68k_00bf60_end:
.org 0xBF62
m68k_00bf62:
        clr.w 0xf3a2:w
m68k_00bf62_end:
.org 0xBF66
m68k_00bf66:
        move.w 0xf38c:w,%d0
m68k_00bf66_end:
.org 0xBF6A
m68k_00bf6a:
        lea.l 0x92878:l,%a1
m68k_00bf6a_end:
.org 0xBF70
m68k_00bf70:
        movea.l (%a1),%a0
m68k_00bf70_end:
.org 0xBF72
m68k_00bf72:
        lsl.w #0x1,%d0
m68k_00bf72_end:
.org 0xBF74
m68k_00bf74:
        move.w 0x4(%a1, %d0.w),%d0
m68k_00bf74_end:
.org 0xBF78
m68k_00bf78:
        adda.w %d0,%a0
m68k_00bf78_end:
.org 0xBF7A
m68k_00bf7a:
        move.b 0x1(%a0),0xf381:w
m68k_00bf7a_end:
.org 0xBF80
m68k_00bf80:
        move.w #0x30,0xf600:w
m68k_00bf80_end:
.org 0xBF86
m68k_00bf86:
        clr.w 0xf396:w
m68k_00bf86_end:
.org 0xBF8A
m68k_00bf8a:
        andi.w #0xfeda,0xf3a4:w
m68k_00bf8a_end:
.org 0xBF90
m68k_00bf90:
        bra.b (. + 16)
m68k_00bf90_end:
.org 0xBF92
m68k_00bf92:
        jsr -174(%pc)
m68k_00bf92_end:
.org 0xBF96
m68k_00bf96:
        addq.w #0x1,0xf36a:w
m68k_00bf96_end:
.org 0xBF9A
m68k_00bf9a:
        bclr.b #0x0,0xf3a5:w
m68k_00bf9a_end:
.org 0xBFA0
m68k_00bfa0:
        rts
m68k_00bfa0_end:
.org 0xBFA2
m68k_00bfa2:
        move.b 0xf602:w,%d0
m68k_00bfa2_end:
.org 0xBFA6
m68k_00bfa6:
        andi.w #0xf,%d0
m68k_00bfa6_end:
.org 0xBFAA
m68k_00bfaa:
        bne.b (. + 10)
m68k_00bfaa_end:
.org 0xBFAC
m68k_00bfac:
        move.w #0x1,0xf608:w
m68k_00bfac_end:
.org 0xBFB2
m68k_00bfb2:
        bra.b (. + 98)
m68k_00bfb2_end:
.org 0xBFB4
m68k_00bfb4:
        subq.w #0x1,0xf608:w
m68k_00bfb4_end:
.org 0xBFB8
m68k_00bfb8:
        bne.b (. + 92)
m68k_00bfb8_end:
.org 0xBFBA
m68k_00bfba:
        move.w #0x10,0xf608:w
m68k_00bfba_end:
.org 0xBFC0
m68k_00bfc0:
        btst.l #0x0,%d0
m68k_00bfc0_end:
.org 0xBFC4
m68k_00bfc4:
        bne.b (. + 68)
m68k_00bfc4_end:
.org 0xBFC6
m68k_00bfc6:
        btst.l #0x1,%d0
m68k_00bfc6_end:
.org 0xBFCA
m68k_00bfca:
        bne.b (. + 42)
m68k_00bfca_end:
.org 0xBFF4
m68k_00bff4:
        addq.w #0x1,0xf386:w
m68k_00bff4_end:
.org 0xBFF8
m68k_00bff8:
        move.w 0xf386:w,%d1
m68k_00bff8_end:
.org 0xBFFC
m68k_00bffc:
        cmp.w 0xf382:w,%d1
m68k_00bffc_end:
.org 0xC000
m68k_00c000:
        bls.b (. + 20)
m68k_00c000_end:
.org 0xC014
m68k_00c014:
        cmpi.w #0x3,0xf380:w
m68k_00c014_end:
.org 0xC01A
m68k_00c01a:
        beq.b (. + 10)
m68k_00c01a_end:
.org 0xC024
m68k_00c024:
        cmpi.w #0x2,0xf386:w
m68k_00c024_end:
.org 0xC02A
m68k_00c02a:
        bcs.b (. + 8)
m68k_00c02a_end:
.org 0xC02C
m68k_00c02c:
        move.w #0x1,0xf388:w
m68k_00c02c_end:
.org 0xC032
m68k_00c032:
        move.w 0xf602:w,%d0
m68k_00c032_end:
.org 0xC036
m68k_00c036:
        btst.l #0x4,%d0
m68k_00c036_end:
.org 0xC03A
m68k_00c03a:
        beq.b (. + 64)
m68k_00c03a_end:
.org 0xC07A
m68k_00c07a:
        tst.w 0xcfd2:w
m68k_00c07a_end:
.org 0xC07E
m68k_00c07e:
        beq.w (. + 28)
m68k_00c07e_end:
.org 0xC082
m68k_00c082:
        subq.w #0x1,0xcfd2:w
m68k_00c082_end:
.org 0xC086
m68k_00c086:
        cmpi.w #0x8,0xcfd2:w
m68k_00c086_end:
.org 0xC08C
m68k_00c08c:
        bls.w (. + 40)
m68k_00c08c_end:
.org 0xC09A
m68k_00c09a:
        move.w 0xf602:w,%d0
m68k_00c09a_end:
.org 0xC09E
m68k_00c09e:
        btst.l #0x5,%d0
m68k_00c09e_end:
.org 0xC0A2
m68k_00c0a2:
        beq.b (. + 18)
m68k_00c0a2_end:
.org 0xC0A4
m68k_00c0a4:
        jsr 16(%pc)
m68k_00c0a4_end:
.org 0xC0A8
m68k_00c0a8:
        nop
m68k_00c0a8_end:
.org 0xC0AA
m68k_00c0aa:
        bcs.b (. + -66)
m68k_00c0aa_end:
.org 0xC0AC
m68k_00c0ac:
        addq.w #0x2,0xf362:w
m68k_00c0ac_end:
.org 0xC0B0
m68k_00c0b0:
        clr.w 0xf36a:w
m68k_00c0b0_end:
.org 0xC0B4
m68k_00c0b4:
        rts
m68k_00c0b4_end:
.org 0xC0B6
m68k_00c0b6:
        move.w #0x8,0xcfd2:w
m68k_00c0b6_end:
.org 0xC0BC
m68k_00c0bc:
        move.w 0xf388:w,%d0
m68k_00c0bc_end:
.org 0xC0C0
m68k_00c0c0:
        move.w 0xf384:w,%d1
m68k_00c0c0_end:
.org 0xC0C4
m68k_00c0c4:
        addq.w #0x1,%d1
m68k_00c0c4_end:
.org 0xC0C6
m68k_00c0c6:
        move.w 0xf386:w,%d2
m68k_00c0c6_end:
.org 0xC0CA
m68k_00c0ca:
        beq.b (. + 10)
m68k_00c0ca_end:
.org 0xC0CC
m68k_00c0cc:
        subq.w #0x1,%d2
m68k_00c0cc_end:
.org 0xC0CE
m68k_00c0ce:
        add.w %d1,%d0
m68k_00c0ce_end:
.org 0xC0D0
m68k_00c0d0:
        dbra %d2,(. + -2)
m68k_00c0d0_end:
.org 0xC0D4
m68k_00c0d4:
        lea.l 0x92878:l,%a1
m68k_00c0d4_end:
.org 0xC0DA
m68k_00c0da:
        move.w 0xf38c:w,%d1
m68k_00c0da_end:
.org 0xC0DE
m68k_00c0de:
        lsl.w #0x1,%d1
m68k_00c0de_end:
.org 0xC0E0
m68k_00c0e0:
        movea.l (%a1),%a2
m68k_00c0e0_end:
.org 0xC0E2
m68k_00c0e2:
        move.w 0x4(%a1, %d1.w),%d1
m68k_00c0e2_end:
.org 0xC0E6
m68k_00c0e6:
        adda.w %d1,%a2
m68k_00c0e6_end:
.org 0xC0E8
m68k_00c0e8:
        move.b 0x2(%a2, %d0.w),%d0
m68k_00c0e8_end:
.org 0xC0EC
m68k_00c0ec:
        cmpi.b #0xff,%d0
m68k_00c0ec_end:
.org 0xC0F0
m68k_00c0f0:
        beq.b (. + 40)
m68k_00c0f0_end:
.org 0xC0F2
m68k_00c0f2:
        move.w 0xf576:w,%d2
m68k_00c0f2_end:
.org 0xC0F6
m68k_00c0f6:
        lea.l 0xf578:w,%a3
m68k_00c0f6_end:
.org 0xC0FA
m68k_00c0fa:
        move.b %d0,(%a3, %d2.w)
m68k_00c0fa_end:
.org 0xC0FE
m68k_00c0fe:
        addq.w #0x1,0xf576:w
m68k_00c0fe_end:
.org 0xC102
m68k_00c102:
        move.w %d0,0xf38c:w
m68k_00c102_end:
.org 0xC106
m68k_00c106:
        move.w #0xac,%d0
m68k_00c106_end:
.org 0xC10A
m68k_00c10a:
        jsr 0x808a:l
m68k_00c10a_end:
.org 0xC110
m68k_00c110:
        andi.w #0xfffe,%sr
m68k_00c110_end:
.org 0xC114
m68k_00c114:
        bra.w (. + 8)
m68k_00c114_end:
.org 0xC11C
m68k_00c11c:
        rts
m68k_00c11c_end:
.org 0xC11E
m68k_00c11e:
        clr.w %d0
m68k_00c11e_end:
.org 0xC120
m68k_00c120:
        move.b 0xf578:w,%d0
m68k_00c120_end:
.org 0xC124
m68k_00c124:
        move.w %d0,0xf38c:w
m68k_00c124_end:
.org 0xC128
m68k_00c128:
        move.w #0x1,0xf576:w
m68k_00c128_end:
.org 0xC12E
m68k_00c12e:
        clr.l 0xf39e:w
m68k_00c12e_end:
.org 0xC132
m68k_00c132:
        clr.l 0xf3ba:w
m68k_00c132_end:
.org 0xC136
m68k_00c136:
        rts
m68k_00c136_end:
.org 0xC138
m68k_00c138:
        btst.b #0x5,0xf603:w
m68k_00c138_end:
.org 0xC13E
m68k_00c13e:
        bne.w (. + 90)
m68k_00c13e_end:
.org 0xC142
m68k_00c142:
        move.b 0xf602:w,%d0
m68k_00c142_end:
.org 0xC146
m68k_00c146:
        andi.w #0xc,%d0
m68k_00c146_end:
.org 0xC14A
m68k_00c14a:
        bne.w (. + 32)
m68k_00c14a_end:
.org 0xC14E
m68k_00c14e:
        tst.w 0xf382:w
m68k_00c14e_end:
.org 0xC152
m68k_00c152:
        beq.w (. + 16)
m68k_00c152_end:
.org 0xC156
m68k_00c156:
        move.b 0xf602:w,%d0
m68k_00c156_end:
.org 0xC15A
m68k_00c15a:
        andi.w #0x3,%d0
m68k_00c15a_end:
.org 0xC15E
m68k_00c15e:
        bne.w (. + 12)
m68k_00c15e_end:
.org 0xC162
m68k_00c162:
        btst.b #0x3,0xf321:w
m68k_00c162_end:
.org 0xC168
m68k_00c168:
        bne.b (. + 48)
m68k_00c168_end:
.org 0xC16A
m68k_00c16a:
        lea.l 46(%pc),%a0
m68k_00c16a_end:
.org 0xC16E
m68k_00c16e:
        nop
m68k_00c16e_end:
.org 0xC170
m68k_00c170:
        move.w 0xf386:w,%d0
m68k_00c170_end:
.org 0xC174
m68k_00c174:
        move.w %d0,%d1
m68k_00c174_end:
.org 0xC176
m68k_00c176:
        lsl.w #0x1,%d0
m68k_00c176_end:
.org 0xC178
m68k_00c178:
        add.w %d1,%d0
m68k_00c178_end:
.org 0xC17A
m68k_00c17a:
        lsl.w #0x3,%d0
m68k_00c17a_end:
.org 0xC17C
m68k_00c17c:
        addi.w #0x30,%d0
m68k_00c17c_end:
.org 0xC180
m68k_00c180:
        move.w 0xf388:w,%d1
m68k_00c180_end:
.org 0xC184
m68k_00c184:
        move.w %d1,%d2
m68k_00c184_end:
.org 0xC186
m68k_00c186:
        lsl.w #0x2,%d1
m68k_00c186_end:
.org 0xC188
m68k_00c188:
        add.w %d2,%d1
m68k_00c188_end:
.org 0xC18A
m68k_00c18a:
        lsl.w #0x3,%d1
m68k_00c18a_end:
.org 0xC18C
m68k_00c18c:
        addi.w #0x60,%d1
m68k_00c18c_end:
.org 0xC190
m68k_00c190:
        clr.w %d2
m68k_00c190_end:
.org 0xC192
m68k_00c192:
        jmp 0xac08:l
m68k_00c192_end:
.org 0xC198
m68k_00c198:
        rts
m68k_00c198_end:
.org 0xC5C2
m68k_00c5c2:
        lea.l 0xd100:w,%a0
m68k_00c5c2_end:
.org 0xC5C6
m68k_00c5c6:
        adda.w 0xf31a:w,%a0
m68k_00c5c6_end:
.org 0xC5CA
m68k_00c5ca:
        bsr.b (. + 34)
m68k_00c5ca_end:
.org 0xC5CC
m68k_00c5cc:
        bsr.b (. + 62)
m68k_00c5cc_end:
.org 0xC5CE
m68k_00c5ce:
        bsr.w (. + 170)
m68k_00c5ce_end:
.org 0xC5D2
m68k_00c5d2:
        bsr.w (. + 236)
m68k_00c5d2_end:
.org 0xC5D6
m68k_00c5d6:
        clr.w (%a0)
m68k_00c5d6_end:
.org 0xC5D8
m68k_00c5d8:
        addi.w #0x8c,0xf31a:w
m68k_00c5d8_end:
.org 0xC5DE
m68k_00c5de:
        bset.b #0x0,0xf3a4:w
m68k_00c5de_end:
.org 0xC5E4
m68k_00c5e4:
        jsr 0x676c4:l
m68k_00c5e4_end:
.org 0xC5EA
m68k_00c5ea:
        rts
m68k_00c5ea_end:
.org 0xC5EC
m68k_00c5ec:
        move.w #0x8,(%a0)+
m68k_00c5ec_end:
.org 0xC5F0
m68k_00c5f0:
        move.w #0xc422,(%a0)+
m68k_00c5f0_end:
.org 0xC5F4
m68k_00c5f4:
        move.w #0xc380,(%a0)+
m68k_00c5f4_end:
.org 0xC5F8
m68k_00c5f8:
        move.w #0x5,%d0
m68k_00c5f8_end:
.org 0xC5FC
m68k_00c5fc:
        move.w #0xc381,(%a0)+
m68k_00c5fc_end:
.org 0xC600
m68k_00c600:
        dbra %d0,(. + -4)
m68k_00c600_end:
.org 0xC604
m68k_00c604:
        move.w #0xcb80,(%a0)+
m68k_00c604_end:
.org 0xC608
m68k_00c608:
        rts
m68k_00c608_end:
.org 0xC60A
m68k_00c60a:
        move.w #0x8,0x14(%a0)
m68k_00c60a_end:
.org 0xC610
m68k_00c610:
        move.w #0x8,(%a0)+
m68k_00c610_end:
.org 0xC614
m68k_00c614:
        move.w #0xc522,0x14(%a0)
m68k_00c614_end:
.org 0xC61A
m68k_00c61a:
        move.w #0xc4a2,(%a0)+
m68k_00c61a_end:
.org 0xC61E
m68k_00c61e:
        move.w #0xc382,0x14(%a0)
m68k_00c61e_end:
.org 0xC624
m68k_00c624:
        move.w #0xc382,(%a0)+
m68k_00c624_end:
.org 0xC628
m68k_00c628:
        move.w #0xc080,%d0
m68k_00c628_end:
.org 0xC62C
m68k_00c62c:
        bsr.w (. + 176)
m68k_00c62c_end:
.org 0xC630
m68k_00c630:
        move.w #0xc088,%d0
m68k_00c630_end:
.org 0xC634
m68k_00c634:
        bsr.w (. + 168)
m68k_00c634_end:
.org 0xC638
m68k_00c638:
        move.w #0xc080,0x14(%a0)
m68k_00c638_end:
.org 0xC63E
m68k_00c63e:
        move.w #0xc080,(%a0)+
m68k_00c63e_end:
.org 0xC642
m68k_00c642:
        move.w #0xc080,0x14(%a0)
m68k_00c642_end:
.org 0xC648
m68k_00c648:
        move.w #0xc080,(%a0)+
m68k_00c648_end:
.org 0xC64C
m68k_00c64c:
        move.w #0xcb82,0x14(%a0)
m68k_00c64c_end:
.org 0xC652
m68k_00c652:
        move.w #0xcb82,(%a0)+
m68k_00c652_end:
.org 0xC656
m68k_00c656:
        adda.w #0x14,%a0
m68k_00c656_end:
.org 0xC65A
m68k_00c65a:
        move.w #0x8,(%a0)+
m68k_00c65a_end:
.org 0xC65E
m68k_00c65e:
        move.w #0xc5a2,(%a0)+
m68k_00c65e_end:
.org 0xC662
m68k_00c662:
        move.w #0xc382,(%a0)+
m68k_00c662_end:
.org 0xC666
m68k_00c666:
        move.w #0x5,%d0
m68k_00c666_end:
.org 0xC66A
m68k_00c66a:
        move.w #0xc080,(%a0)+
m68k_00c66a_end:
.org 0xC66E
m68k_00c66e:
        dbra %d0,(. + -4)
m68k_00c66e_end:
.org 0xC672
m68k_00c672:
        move.w #0xcb82,(%a0)+
m68k_00c672_end:
.org 0xC676
m68k_00c676:
        rts
m68k_00c676_end:
.org 0xC678
m68k_00c678:
        move.w #0x8,0x14(%a0)
m68k_00c678_end:
.org 0xC67E
m68k_00c67e:
        move.w #0x8,(%a0)+
m68k_00c67e_end:
.org 0xC682
m68k_00c682:
        move.w #0xc6a2,0x14(%a0)
m68k_00c682_end:
.org 0xC688
m68k_00c688:
        move.w #0xc622,(%a0)+
m68k_00c688_end:
.org 0xC68C
m68k_00c68c:
        move.w #0xc382,0x14(%a0)
m68k_00c68c_end:
.org 0xC692
m68k_00c692:
        move.w #0xc382,(%a0)+
m68k_00c692_end:
.org 0xC696
m68k_00c696:
        move.w #0xc080,%d0
m68k_00c696_end:
.org 0xC69A
m68k_00c69a:
        bsr.w (. + 66)
m68k_00c69a_end:
.org 0xC69E
m68k_00c69e:
        move.w #0xc08c,%d0
m68k_00c69e_end:
.org 0xC6A2
m68k_00c6a2:
        bsr.w (. + 58)
m68k_00c6a2_end:
.org 0xC6A6
m68k_00c6a6:
        move.w #0xc080,%d0
m68k_00c6a6_end:
.org 0xC6AA
m68k_00c6aa:
        bsr.w (. + 50)
m68k_00c6aa_end:
.org 0xC6AE
m68k_00c6ae:
        move.w #0xcb82,0x14(%a0)
m68k_00c6ae_end:
.org 0xC6B4
m68k_00c6b4:
        move.w #0xcb82,(%a0)+
m68k_00c6b4_end:
.org 0xC6B8
m68k_00c6b8:
        adda.w #0x14,%a0
m68k_00c6b8_end:
.org 0xC6BC
m68k_00c6bc:
        rts
m68k_00c6bc_end:
.org 0xC6BE
m68k_00c6be:
        move.w #0x8,(%a0)+
m68k_00c6be_end:
.org 0xC6C2
m68k_00c6c2:
        move.w #0xc722,(%a0)+
m68k_00c6c2_end:
.org 0xC6C6
m68k_00c6c6:
        move.w #0xd380,(%a0)+
m68k_00c6c6_end:
.org 0xC6CA
m68k_00c6ca:
        move.w #0x5,%d0
m68k_00c6ca_end:
.org 0xC6CE
m68k_00c6ce:
        move.w #0xd381,(%a0)+
m68k_00c6ce_end:
.org 0xC6D2
m68k_00c6d2:
        dbra %d0,(. + -4)
m68k_00c6d2_end:
.org 0xC6D6
m68k_00c6d6:
        move.w #0xdb80,(%a0)+
m68k_00c6d6_end:
.org 0xC6DA
m68k_00c6da:
        rts
m68k_00c6da_end:
.org 0xC6DC
m68k_00c6dc:
        move.w %d0,%d1
m68k_00c6dc_end:
.org 0xC6DE
m68k_00c6de:
        move.w %d1,(%a0)
m68k_00c6de_end:
.org 0xC6E0
m68k_00c6e0:
        addq.w #0x1,%d1
m68k_00c6e0_end:
.org 0xC6E2
m68k_00c6e2:
        move.w %d1,0x14(%a0)
m68k_00c6e2_end:
.org 0xC6E6
m68k_00c6e6:
        addq.w #0x1,%d1
m68k_00c6e6_end:
.org 0xC6E8
m68k_00c6e8:
        addq.w #0x2,%a0
m68k_00c6e8_end:
.org 0xC6EA
m68k_00c6ea:
        move.w %d1,(%a0)
m68k_00c6ea_end:
.org 0xC6EC
m68k_00c6ec:
        addq.w #0x1,%d1
m68k_00c6ec_end:
.org 0xC6EE
m68k_00c6ee:
        move.w %d1,0x14(%a0)
m68k_00c6ee_end:
.org 0xC6F2
m68k_00c6f2:
        addq.w #0x2,%a0
m68k_00c6f2_end:
.org 0xC6F4
m68k_00c6f4:
        rts
m68k_00c6f4_end:
.org 0xC6F6
m68k_00c6f6:
        bsr.w (. + 110)
m68k_00c6f6_end:
.org 0xC6FA
m68k_00c6fa:
        bsr.w (. + 150)
m68k_00c6fa_end:
.org 0xC6FE
m68k_00c6fe:
        btst.b #0x4,0xf603:w
m68k_00c6fe_end:
.org 0xC704
m68k_00c704:
        beq.b (. + 56)
m68k_00c704_end:
.org 0xC73C
m68k_00c73c:
        btst.b #0x5,0xf603:w
m68k_00c73c_end:
.org 0xC742
m68k_00c742:
        beq.b (. + 32)
m68k_00c742_end:
.org 0xC744
m68k_00c744:
        clr.w 0xf384:w
m68k_00c744_end:
.org 0xC748
m68k_00c748:
        clr.w 0xf388:w
m68k_00c748_end:
.org 0xC74C
m68k_00c74c:
        bsr.w (. + -1686)
m68k_00c74c_end:
.org 0xC750
m68k_00c750:
        bcs.b (. + -74)
m68k_00c750_end:
.org 0xC752
m68k_00c752:
        move.w #0x3,0xf362:w
m68k_00c752_end:
.org 0xC758
m68k_00c758:
        move.w #0x12,0xf36a:w
m68k_00c758_end:
.org 0xC75E
m68k_00c75e:
        bsr.w (. + 212)
m68k_00c75e_end:
.org 0xC762
m68k_00c762:
        rts
m68k_00c762_end:
.org 0xC764
m68k_00c764:
        btst.b #0x1,0xf602:w
m68k_00c764_end:
.org 0xC76A
m68k_00c76a:
        bne.b (. + 10)
m68k_00c76a_end:
.org 0xC76C
m68k_00c76c:
        btst.b #0x0,0xf602:w
m68k_00c76c_end:
.org 0xC772
m68k_00c772:
        beq.b (. + 22)
m68k_00c772_end:
.org 0xC788
m68k_00c788:
        move.w #0x1,0xf608:w
m68k_00c788_end:
.org 0xC78E
m68k_00c78e:
        rts
m68k_00c78e_end:
.org 0xC790
m68k_00c790:
        btst.b #0x5,0xf603:w
m68k_00c790_end:
.org 0xC796
m68k_00c796:
        bne.w (. + 56)
m68k_00c796_end:
.org 0xC79A
m68k_00c79a:
        move.b 0xf602:w,%d0
m68k_00c79a_end:
.org 0xC79E
m68k_00c79e:
        andi.w #0x3,%d0
m68k_00c79e_end:
.org 0xC7A2
m68k_00c7a2:
        bne.w (. + 12)
m68k_00c7a2_end:
.org 0xC7A6
m68k_00c7a6:
        btst.b #0x3,0xf321:w
m68k_00c7a6_end:
.org 0xC7AC
m68k_00c7ac:
        bne.b (. + 34)
m68k_00c7ac_end:
.org 0xC7AE
m68k_00c7ae:
        lea.l 32(%pc),%a0
m68k_00c7ae_end:
.org 0xC7B2
m68k_00c7b2:
        nop
m68k_00c7b2_end:
.org 0xC7B4
m68k_00c7b4:
        move.w #0x40,%d0
m68k_00c7b4_end:
.org 0xC7B8
m68k_00c7b8:
        tst.w 0xf386:w
m68k_00c7b8_end:
.org 0xC7BC
m68k_00c7bc:
        beq.b (. + 6)
m68k_00c7bc_end:
.org 0xC7C2
m68k_00c7c2:
        move.w #0x88,%d1
m68k_00c7c2_end:
.org 0xC7C6
m68k_00c7c6:
        clr.w %d2
m68k_00c7c6_end:
.org 0xC7C8
m68k_00c7c8:
        jsr 0xac08:l
m68k_00c7c8_end:
.org 0xC7CE
m68k_00c7ce:
        rts
m68k_00c7ce_end:
.org 0xC832
m68k_00c832:
        lea.l 0xd100:w,%a0
m68k_00c832_end:
.org 0xC836
m68k_00c836:
        adda.w 0xf31a:w,%a0
m68k_00c836_end:
.org 0xC83A
m68k_00c83a:
        move.w #0x8,0x78(%a0)
m68k_00c83a_end:
.org 0xC840
m68k_00c840:
        move.w #0x8,0x64(%a0)
m68k_00c840_end:
.org 0xC846
m68k_00c846:
        move.w #0x8,0x50(%a0)
m68k_00c846_end:
.org 0xC84C
m68k_00c84c:
        move.w #0x8,0x3c(%a0)
m68k_00c84c_end:
.org 0xC852
m68k_00c852:
        move.w #0x8,0x28(%a0)
m68k_00c852_end:
.org 0xC858
m68k_00c858:
        move.w #0x8,0x14(%a0)
m68k_00c858_end:
.org 0xC85E
m68k_00c85e:
        move.w #0x8,(%a0)+
m68k_00c85e_end:
.org 0xC862
m68k_00c862:
        move.w #0xc722,0x78(%a0)
m68k_00c862_end:
.org 0xC868
m68k_00c868:
        move.w #0xc6a2,0x64(%a0)
m68k_00c868_end:
.org 0xC86E
m68k_00c86e:
        move.w #0xc622,0x50(%a0)
m68k_00c86e_end:
.org 0xC874
m68k_00c874:
        move.w #0xc5a2,0x3c(%a0)
m68k_00c874_end:
.org 0xC87A
m68k_00c87a:
        move.w #0xc522,0x28(%a0)
m68k_00c87a_end:
.org 0xC880
m68k_00c880:
        move.w #0xc4a2,0x14(%a0)
m68k_00c880_end:
.org 0xC886
m68k_00c886:
        move.w #0xc422,(%a0)+
m68k_00c886_end:
.org 0xC88A
m68k_00c88a:
        move.w #0x7,%d0
m68k_00c88a_end:
.org 0xC88E
m68k_00c88e:
        clr.w 0x78(%a0)
m68k_00c88e_end:
.org 0xC892
m68k_00c892:
        clr.w 0x64(%a0)
m68k_00c892_end:
.org 0xC896
m68k_00c896:
        clr.w 0x50(%a0)
m68k_00c896_end:
.org 0xC89A
m68k_00c89a:
        clr.w 0x3c(%a0)
m68k_00c89a_end:
.org 0xC89E
m68k_00c89e:
        clr.w 0x28(%a0)
m68k_00c89e_end:
.org 0xC8A2
m68k_00c8a2:
        clr.w 0x14(%a0)
m68k_00c8a2_end:
.org 0xC8A6
m68k_00c8a6:
        clr.w (%a0)+
m68k_00c8a6_end:
.org 0xC8A8
m68k_00c8a8:
        dbra %d0,(. + -26)
m68k_00c8a8_end:
.org 0xC8AC
m68k_00c8ac:
        clr.w 0x78(%a0)
m68k_00c8ac_end:
.org 0xC8B0
m68k_00c8b0:
        addi.w #0x8c,0xf31a:w
m68k_00c8b0_end:
.org 0xC8B6
m68k_00c8b6:
        rts
m68k_00c8b6_end:
.org 0xD270
m68k_00d270:
        lea.l 88(%pc),%a0
m68k_00d270_end:
.org 0xD274
m68k_00d274:
        move.w 0xef64:w,%d0
m68k_00d274_end:
.org 0xD278
m68k_00d278:
        lsl.w #0x2,%d0
m68k_00d278_end:
.org 0xD27A
m68k_00d27a:
        move.l (%a0, %d0.w),0xef6a:w
m68k_00d27a_end:
.org 0xD280
m68k_00d280:
        move.w 0xef66:w,%d0
m68k_00d280_end:
.org 0xD284
m68k_00d284:
        lsl.w #0x2,%d0
m68k_00d284_end:
.org 0xD286
m68k_00d286:
        move.l 0xc(%a0, %d0.w),0xef6e:w
m68k_00d286_end:
.org 0xD28C
m68k_00d28c:
        move.w 0xef68:w,%d0
m68k_00d28c_end:
.org 0xD290
m68k_00d290:
        lsl.w #0x2,%d0
m68k_00d290_end:
.org 0xD292
m68k_00d292:
        move.l 0x18(%a0, %d0.w),0xef72:w
m68k_00d292_end:
.org 0xD298
m68k_00d298:
        move.l #0xc000000e,%d0
m68k_00d298_end:
.org 0xD29E
m68k_00d29e:
        move.w #0xa,%d1
m68k_00d29e_end:
.org 0xD2A2
m68k_00d2a2:
        move.w #0xc41a,%d2
m68k_00d2a2_end:
.org 0xD2A6
m68k_00d2a6:
        lea.l 70(%pc),%a0
m68k_00d2a6_end:
.org 0xD2AA
m68k_00d2aa:
        move.w #0xc386,0xf692:w
m68k_00d2aa_end:
.org 0xD2B0
m68k_00d2b0:
        move.w #0xc0a1,0xef76:w
m68k_00d2b0_end:
.org 0xD2B6
m68k_00d2b6:
        jsr 0x26bfa:l
m68k_00d2b6_end:
.org 0xD2BC
m68k_00d2bc:
        bset.b #0x0,0xf3a4:w
m68k_00d2bc_end:
.org 0xD2C2
m68k_00d2c2:
        move.w #0xf0,0xf600:w
m68k_00d2c2_end:
.org 0xD2C8
m68k_00d2c8:
        rts
m68k_00d2c8_end:
.org 0xD368
m68k_00d368:
        bsr.w (. + 10)
m68k_00d368_end:
.org 0xD36C
m68k_00d36c:
        bsr.w (. + 302)
m68k_00d36c_end:
.org 0xD370
m68k_00d370:
        rts
m68k_00d370_end:
.org 0xD372
m68k_00d372:
        move.b 0xf602:w,%d0
m68k_00d372_end:
.org 0xD376
m68k_00d376:
        andi.w #0x3,%d0
m68k_00d376_end:
.org 0xD37A
m68k_00d37a:
        beq.b (. + 58)
m68k_00d37a_end:
.org 0xD37C
m68k_00d37c:
        subq.w #0x1,0xf608:w
m68k_00d37c_end:
.org 0xD380
m68k_00d380:
        bne.w (. + 164)
m68k_00d380_end:
.org 0xD384
m68k_00d384:
        move.w #0xc,0xf608:w
m68k_00d384_end:
.org 0xD38A
m68k_00d38a:
        btst.l #0x1,%d0
m68k_00d38a_end:
.org 0xD38E
m68k_00d38e:
        bne.b (. + 20)
m68k_00d38e_end:
.org 0xD390
m68k_00d390:
        subq.w #0x1,0xf3f0:w
m68k_00d390_end:
.org 0xD394
m68k_00d394:
        bpl.w (. + 144)
m68k_00d394_end:
.org 0xD398
m68k_00d398:
        move.w #0x2,0xf3f0:w
m68k_00d398_end:
.org 0xD39E
m68k_00d39e:
        bra.w (. + 134)
m68k_00d39e_end:
.org 0xD3A2
m68k_00d3a2:
        addq.w #0x1,0xf3f0:w
m68k_00d3a2_end:
.org 0xD3A6
m68k_00d3a6:
        cmpi.w #0x3,0xf3f0:w
m68k_00d3a6_end:
.org 0xD3AC
m68k_00d3ac:
        bcs.b (. + 120)
m68k_00d3ac_end:
.org 0xD3AE
m68k_00d3ae:
        clr.w 0xf3f0:w
m68k_00d3ae_end:
.org 0xD3B2
m68k_00d3b2:
        bra.b (. + 114)
m68k_00d3b2_end:
.org 0xD3B4
m68k_00d3b4:
        move.w 0xf602:w,%d0
m68k_00d3b4_end:
.org 0xD3B8
m68k_00d3b8:
        andi.w #0xc,%d0
m68k_00d3b8_end:
.org 0xD3BC
m68k_00d3bc:
        beq.w (. + 98)
m68k_00d3bc_end:
.org 0xD3C0
m68k_00d3c0:
        subq.w #0x1,0xf608:w
m68k_00d3c0_end:
.org 0xD3C4
m68k_00d3c4:
        bne.w (. + 96)
m68k_00d3c4_end:
.org 0xD3C8
m68k_00d3c8:
        move.w #0xc,0xf608:w
m68k_00d3c8_end:
.org 0xD3CE
m68k_00d3ce:
        lea.l 0xef64:w,%a0
m68k_00d3ce_end:
.org 0xD3D2
m68k_00d3d2:
        lea.l 0xefb2:w,%a1
m68k_00d3d2_end:
.org 0xD3D6
m68k_00d3d6:
        move.w 0xf3f0:w,%d1
m68k_00d3d6_end:
.org 0xD3DA
m68k_00d3da:
        lsl.w #0x1,%d1
m68k_00d3da_end:
.org 0xD3DC
m68k_00d3dc:
        move.w (%a0, %d1.w),%d2
m68k_00d3dc_end:
.org 0xD3E0
m68k_00d3e0:
        move.w (%a1, %d1.w),%d3
m68k_00d3e0_end:
.org 0xD3E4
m68k_00d3e4:
        btst.l #0x3,%d0
m68k_00d3e4_end:
.org 0xD3E8
m68k_00d3e8:
        bne.w (. + 26)
m68k_00d3e8_end:
.org 0xD3EC
m68k_00d3ec:
        subq.w #0x1,%d2
m68k_00d3ec_end:
.org 0xD3EE
m68k_00d3ee:
        bpl.w (. + 8)
m68k_00d3ee_end:
.org 0xD3F2
m68k_00d3f2:
        move.w #0x2,%d2
m68k_00d3f2_end:
.org 0xD3F6
m68k_00d3f6:
        btst.l %d2,%d3
m68k_00d3f6_end:
.org 0xD3F8
m68k_00d3f8:
        beq.b (. + -12)
m68k_00d3f8_end:
.org 0xD3FA
m68k_00d3fa:
        move.w %d2,(%a0, %d1.w)
m68k_00d3fa_end:
.org 0xD3FE
m68k_00d3fe:
        bra.w (. + 24)
m68k_00d3fe_end:
.org 0xD402
m68k_00d402:
        addq.w #0x1,%d2
m68k_00d402_end:
.org 0xD404
m68k_00d404:
        cmpi.w #0x3,%d2
m68k_00d404_end:
.org 0xD408
m68k_00d408:
        bcs.w (. + 6)
m68k_00d408_end:
.org 0xD40C
m68k_00d40c:
        clr.w %d2
m68k_00d40c_end:
.org 0xD40E
m68k_00d40e:
        btst.l %d2,%d3
m68k_00d40e_end:
.org 0xD410
m68k_00d410:
        beq.b (. + -14)
m68k_00d410_end:
.org 0xD412
m68k_00d412:
        move.w %d2,(%a0, %d1.w)
m68k_00d412_end:
.org 0xD416
m68k_00d416:
        bsr.w (. + -422)
m68k_00d416_end:
.org 0xD41A
m68k_00d41a:
        bra.w (. + 126)
m68k_00d41a_end:
.org 0xD41E
m68k_00d41e:
        move.w #0x1,0xf608:w
m68k_00d41e_end:
.org 0xD424
m68k_00d424:
        tst.w 0xcfd2:w
m68k_00d424_end:
.org 0xD428
m68k_00d428:
        beq.w (. + 28)
m68k_00d428_end:
.org 0xD42C
m68k_00d42c:
        subq.w #0x1,0xcfd2:w
m68k_00d42c_end:
.org 0xD430
m68k_00d430:
        cmpi.w #0x8,0xcfd2:w
m68k_00d430_end:
.org 0xD436
m68k_00d436:
        bls.w (. + 74)
m68k_00d436_end:
.org 0xD43A
m68k_00d43a:
        move.w #0x8,0xcfd2:w
m68k_00d43a_end:
.org 0xD440
m68k_00d440:
        bra.w (. + 64)
m68k_00d440_end:
.org 0xD444
m68k_00d444:
        btst.b #0x5,0xf603:w
m68k_00d444_end:
.org 0xD44A
m68k_00d44a:
        beq.b (. + 54)
m68k_00d44a_end:
.org 0xD44C
m68k_00d44c:
        move.w 0xf3f0:w,%d0
m68k_00d44c_end:
.org 0xD450
m68k_00d450:
        lsl.w #0x2,%d0
m68k_00d450_end:
.org 0xD452
m68k_00d452:
        lea.l 0xef6a:w,%a0
m68k_00d452_end:
.org 0xD456
m68k_00d456:
        move.l (%a0, %d0.w),%d0
m68k_00d456_end:
.org 0xD45A
m68k_00d45a:
        move.w 0xf364:w,%d1
m68k_00d45a_end:
.org 0xD45E
m68k_00d45e:
        lsl.w #0x2,%d1
m68k_00d45e_end:
.org 0xD460
m68k_00d460:
        lea.l 0xdffc:w,%a0
m68k_00d460_end:
.org 0xD464
m68k_00d464:
        cmp.l (%a0, %d1.w),%d0
m68k_00d464_end:
.org 0xD468
m68k_00d468:
        bhi.b (. + 48)
m68k_00d468_end:
.org 0xD46A
m68k_00d46a:
        bsr.w (. + 188)
m68k_00d46a_end:
.org 0xD46E
m68k_00d46e:
        jsr -5050(%pc)
m68k_00d46e_end:
.org 0xD472
m68k_00d472:
        move.w #0x3,0xf362:w
m68k_00d472_end:
.org 0xD478
m68k_00d478:
        move.w #0x12,0xf36a:w
m68k_00d478_end:
.org 0xD47E
m68k_00d47e:
        bra.b (. + 26)
m68k_00d47e_end:
.org 0xD480
m68k_00d480:
        btst.b #0x4,0xf603:w
m68k_00d480_end:
.org 0xD486
m68k_00d486:
        beq.b (. + 18)
m68k_00d486_end:
.org 0xD488
m68k_00d488:
        bsr.w (. + 158)
m68k_00d488_end:
.org 0xD48C
m68k_00d48c:
        move.w #0x2,0xf362:w
m68k_00d48c_end:
.org 0xD492
m68k_00d492:
        move.w #0x12,0xf36a:w
m68k_00d492_end:
.org 0xD498
m68k_00d498:
        rts
m68k_00d498_end:
.org 0xD8EC
m68k_00d8ec:
        btst.b #0x2,0xf3a5:w
m68k_00d8ec_end:
.org 0xD8F2
m68k_00d8f2:
        beq.b (. + 44)
m68k_00d8f2_end:
.org 0xD91E
m68k_00d91e:
        rts
m68k_00d91e_end:
.org 0xDF6E
m68k_00df6e:
        move.w #0x2700,%sr
m68k_00df6e_end:
.org 0xDF72
m68k_00df72:
        clr.w 0xef78:w
m68k_00df72_end:
.org 0xDF76
m68k_00df76:
        move.w #0xffff,0xff7026:l
m68k_00df76_end:
.org 0xDF7E
m68k_00df7e:
        cmpi.w #0x2,0xf36c:w
m68k_00df7e_end:
.org 0xDF84
m68k_00df84:
        beq.w (. + 204)
m68k_00df84_end:
.org 0xDF88
m68k_00df88:
        cmpi.w #0x3,0xf36c:w
m68k_00df88_end:
.org 0xDF8E
m68k_00df8e:
        beq.w (. + 194)
m68k_00df8e_end:
.org 0xDF92
m68k_00df92:
        cmpi.w #0x11,0xf65a:w
m68k_00df92_end:
.org 0xDF98
m68k_00df98:
        beq.w (. + 184)
m68k_00df98_end:
.org 0xDF9C
m68k_00df9c:
        cmpi.b #0x6,0xf579:w
m68k_00df9c_end:
.org 0xDFA2
m68k_00dfa2:
        beq.w (. + 30)
m68k_00dfa2_end:
.org 0xDFA6
m68k_00dfa6:
        cmpi.b #0xf,0xf579:w
m68k_00dfa6_end:
.org 0xDFAC
m68k_00dfac:
        beq.w (. + 20)
m68k_00dfac_end:
.org 0xDFB0
m68k_00dfb0:
        cmpi.b #0x15,0xf579:w
m68k_00dfb0_end:
.org 0xDFB6
m68k_00dfb6:
        beq.w (. + 10)
m68k_00dfb6_end:
.org 0xDFBA
m68k_00dfba:
        move.w #0x1,0xf650:w
m68k_00dfba_end:
.org 0xDFC0
m68k_00dfc0:
        clr.w %d0
m68k_00dfc0_end:
.org 0xDFC2
m68k_00dfc2:
        move.b 0xf579:w,%d0
m68k_00dfc2_end:
.org 0xDFC6
m68k_00dfc6:
        subq.w #0x4,%d0
m68k_00dfc6_end:
.org 0xDFC8
m68k_00dfc8:
        lsl.w #0x1,%d0
m68k_00dfc8_end:
.org 0xDFCA
m68k_00dfca:
        move.w 88(%pc, %d0.w),%d0
m68k_00dfca_end:
.org 0xDFCE
m68k_00dfce:
        lea.l 286(%pc),%a0
m68k_00dfce_end:
.org 0xDFD2
m68k_00dfd2:
        nop
m68k_00dfd2_end:
.org 0xDFD4
m68k_00dfd4:
        jsr (%a0, %d0.w)
m68k_00dfd4_end:
.org 0xDFD8
m68k_00dfd8:
        jsr 0x1406:l
m68k_00dfd8_end:
.org 0xDFDE
m68k_00dfde:
        bcs.w (. + 56)
m68k_00dfde_end:
.org 0xDFE2
m68k_00dfe2:
        cmpi.b #0xff,0xf579:w
m68k_00dfe2_end:
.org 0xDFE8
m68k_00dfe8:
        beq.w (. + 40)
m68k_00dfe8_end:
.org 0xDFEC
m68k_00dfec:
        cmpi.w #0x28,0xf600:w
m68k_00dfec_end:
.org 0xDFF2
m68k_00dff2:
        bne.b (. + 8)
m68k_00dff2_end:
.org 0xDFF4
m68k_00dff4:
        jmp 0x60c:l
m68k_00dff4_end:
.org 0xDFFA
m68k_00dffa:
        move.w 0xf38a:w,0xf612:w
m68k_00dffa_end:
.org 0xE000
m68k_00e000:
        jsr 0xc11e:l
m68k_00e000_end:
.org 0xE006
m68k_00e006:
        jsr 0x133a:l
m68k_00e006_end:
.org 0xE00C
m68k_00e00c:
        bra.w (. + 16)
m68k_00e00c_end:
.org 0xE010
m68k_00e010:
        jmp 0x3096e:l
m68k_00e010_end:
.org 0xE016
m68k_00e016:
        jmp 0x6701e:l
m68k_00e016_end:
.org 0xE01C
m68k_00e01c:
        jsr 0xaf48:l
m68k_00e01c_end:
.org 0xE022
m68k_00e022:
        rts
m68k_00e022_end:
.org 0xE0EE
m68k_00e0ee:
        move.w 0xf364:w,%d0
m68k_00e0ee_end:
.org 0xE0F2
m68k_00e0f2:
        lsl.w #0x1,%d0
m68k_00e0f2_end:
.org 0xE0F4
m68k_00e0f4:
        add.w 0xf364:w,%d0
m68k_00e0f4_end:
.org 0xE0F8
m68k_00e0f8:
        lsl.w #0x2,%d0
m68k_00e0f8_end:
.org 0xE0FA
m68k_00e0fa:
        lea.l 0xe80c:w,%a0
m68k_00e0fa_end:
.org 0xE0FE
m68k_00e0fe:
        lea.l 0xcd00:w,%a1
m68k_00e0fe_end:
.org 0xE102
m68k_00e102:
        move.w (%a0, %d0.w),%d1
m68k_00e102_end:
.org 0xE106
m68k_00e106:
        bmi.b (. + 18)
m68k_00e106_end:
.org 0xE108
m68k_00e108:
        clr.b (%a1, %d1.w)
m68k_00e108_end:
.org 0xE10C
m68k_00e10c:
        move.w #0xffff,(%a0, %d0.w)
m68k_00e10c_end:
.org 0xE112
m68k_00e112:
        cmp.w 0xf3a6:w,%d1
m68k_00e112_end:
.org 0xE116
m68k_00e116:
        beq.b (. + 28)
m68k_00e116_end:
.org 0xE118
m68k_00e118:
        move.w 0xf3a6:w,(%a0, %d0.w)
m68k_00e118_end:
.org 0xE11E
m68k_00e11e:
        move.w 0xf3a0:w,0x2(%a0, %d0.w)
m68k_00e11e_end:
.org 0xE124
m68k_00e124:
        move.w 0xf3a6:w,%d0
m68k_00e124_end:
.org 0xE128
m68k_00e128:
        lea.l 0xcd00:w,%a0
m68k_00e128_end:
.org 0xE12C
m68k_00e12c:
        move.b #0x2,(%a0, %d0.w)
m68k_00e12c_end:
.org 0xE132
m68k_00e132:
        rts
m68k_00e132_end:
.org 0xE134
m68k_00e134:
        move.w 0xf3ae:w,%d1
m68k_00e134_end:
.org 0xE138
m68k_00e138:
        lsl.w #0x2,%d1
m68k_00e138_end:
.org 0xE13A
m68k_00e13a:
        lea.l 0xdffc:w,%a0
m68k_00e13a_end:
.org 0xE13E
m68k_00e13e:
        move.l (%a0, %d1.w),%d2
m68k_00e13e_end:
.org 0xE142
m68k_00e142:
        sub.l 0xf39e:w,%d2
m68k_00e142_end:
.org 0xE146
m68k_00e146:
        bcs.w (. + 174)
m68k_00e146_end:
.org 0xE14A
m68k_00e14a:
        move.l %d2,(%a0, %d1.w)
m68k_00e14a_end:
.org 0xE14E
m68k_00e14e:
        move.w 0xf3a6:w,%d0
m68k_00e14e_end:
.org 0xE152
m68k_00e152:
        lea.l 0xcc00:w,%a0
m68k_00e152_end:
.org 0xE156
m68k_00e156:
        move.w 0xf364:w,%d1
m68k_00e156_end:
.org 0xE15A
m68k_00e15a:
        move.b %d1,(%a0, %d0.w)
m68k_00e15a_end:
.org 0xE15E
m68k_00e15e:
        lea.l 0xcd00:w,%a0
m68k_00e15e_end:
.org 0xE162
m68k_00e162:
        move.b #0x1,(%a0, %d0.w)
m68k_00e162_end:
.org 0xE168
m68k_00e168:
        lea.l 0xe45c:w,%a1
m68k_00e168_end:
.org 0xE16C
m68k_00e16c:
        lsl.w #0x2,%d1
m68k_00e16c_end:
.org 0xE16E
m68k_00e16e:
        addq.l #0x1,(%a1, %d1.w)
m68k_00e16e_end:
.org 0xE172
m68k_00e172:
        move.w 0xf3ae:w,%d1
m68k_00e172_end:
.org 0xE176
m68k_00e176:
        lsl.w #0x2,%d1
m68k_00e176_end:
.org 0xE178
m68k_00e178:
        subq.l #0x1,(%a1, %d1.w)
m68k_00e178_end:
.org 0xE17C
m68k_00e17c:
        move.w 0xf3ae:w,%d0
m68k_00e17c_end:
.org 0xE180
m68k_00e180:
        lsl.w #0x1,%d0
m68k_00e180_end:
.org 0xE182
m68k_00e182:
        lea.l 0xf45e:w,%a0
m68k_00e182_end:
.org 0xE186
m68k_00e186:
        move.w (%a0, %d0.w),%d1
m68k_00e186_end:
.org 0xE18A
m68k_00e18a:
        cmp.w 0xf3a6:w,%d1
m68k_00e18a_end:
.org 0xE18E
m68k_00e18e:
        bne.b (. + 60)
m68k_00e18e_end:
.org 0xE190
m68k_00e190:
        move.w #0xffff,0xf630:w
m68k_00e190_end:
.org 0xE196
m68k_00e196:
        move.w 0xf3ae:w,%d0
m68k_00e196_end:
.org 0xE19A
m68k_00e19a:
        jsr 0x5f48:l
m68k_00e19a_end:
.org 0xE1A0
m68k_00e1a0:
        move.w 0xf3ae:w,%d0
m68k_00e1a0_end:
.org 0xE1A4
m68k_00e1a4:
        bsr.w (. + 82)
m68k_00e1a4_end:
.org 0xE1A8
m68k_00e1a8:
        move.w 0xf376:w,%d0
m68k_00e1a8_end:
.org 0xE1AC
m68k_00e1ac:
        lsl.w #0x1,%d0
m68k_00e1ac_end:
.org 0xE1AE
m68k_00e1ae:
        lea.l 0xe640:w,%a0
m68k_00e1ae_end:
.org 0xE1B2
m68k_00e1b2:
        move.w (%a0, %d0.w),%d1
m68k_00e1b2_end:
.org 0xE1B6
m68k_00e1b6:
        cmp.w 0xf3a6:w,%d1
m68k_00e1b6_end:
.org 0xE1BA
m68k_00e1ba:
        bne.b (. + 16)
m68k_00e1ba_end:
.org 0xE1BC
m68k_00e1bc:
        move.w 0xf364:w,%d0
m68k_00e1bc_end:
.org 0xE1C0
m68k_00e1c0:
        lsl.w #0x1,%d0
m68k_00e1c0_end:
.org 0xE1C2
m68k_00e1c2:
        lea.l 0xf45e:w,%a0
m68k_00e1c2_end:
.org 0xE1C6
m68k_00e1c6:
        move.w %d1,(%a0, %d0.w)
m68k_00e1c6_end:
.org 0xE1CA
m68k_00e1ca:
        move.w 0xf38a:w,0xf612:w
m68k_00e1ca_end:
.org 0xE1D0
m68k_00e1d0:
        move.w #0x20,0xf362:w
m68k_00e1d0_end:
.org 0xE1D6
m68k_00e1d6:
        move.w #0xe,%d0
m68k_00e1d6_end:
.org 0xE1DA
m68k_00e1da:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00e1da_end:
.org 0xE1E0
m68k_00e1e0:
        jsr 0x676f2:l
m68k_00e1e0_end:
.org 0xE1E6
m68k_00e1e6:
        move.w #0x1,0xf652:w
m68k_00e1e6_end:
.org 0xE1EC
m68k_00e1ec:
        move.w #0x1a,0xff7026:l
m68k_00e1ec_end:
.org 0xE1F4
m68k_00e1f4:
        rts
m68k_00e1f4_end:
.org 0xE1F6
m68k_00e1f6:
        movem.l %d1-%d5/%a0-%a2,-(%a7)
m68k_00e1f6_end:
.org 0xE1FA
m68k_00e1fa:
        lea.l 0xf500:w,%a0
m68k_00e1fa_end:
.org 0xE1FE
m68k_00e1fe:
        move.w (%a0)+,%d4
m68k_00e1fe_end:
.org 0xE200
m68k_00e200:
        bmi.w (. + 50)
m68k_00e200_end:
.org 0xE204
m68k_00e204:
        bsr.w (. + 104)
m68k_00e204_end:
.org 0xE208
m68k_00e208:
        bcs.w (. + 82)
m68k_00e208_end:
.org 0xE20C
m68k_00e20c:
        andi.w #0xff,%d4
m68k_00e20c_end:
.org 0xE210
m68k_00e210:
        lea.l 0xc300:w,%a1
m68k_00e210_end:
.org 0xE214
m68k_00e214:
        move.w %d4,%d3
m68k_00e214_end:
.org 0xE216
m68k_00e216:
        move.b (%a1, %d3.w),%d1
m68k_00e216_end:
.org 0xE21A
m68k_00e21a:
        move.b %d1,%d2
m68k_00e21a_end:
.org 0xE21C
m68k_00e21c:
        move.w (%a0)+,%d3
m68k_00e21c_end:
.org 0xE21E
m68k_00e21e:
        bmi.b (. + 60)
m68k_00e21e_end:
.org 0xE220
m68k_00e220:
        andi.w #0xff,%d3
m68k_00e220_end:
.org 0xE224
m68k_00e224:
        move.b (%a1, %d3.w),%d1
m68k_00e224_end:
.org 0xE228
m68k_00e228:
        cmp.b %d2,%d1
m68k_00e228_end:
.org 0xE22A
m68k_00e22a:
        bls.b (. + -14)
m68k_00e22a_end:
.org 0xE22C
m68k_00e22c:
        move.w %d3,%d4
m68k_00e22c_end:
.org 0xE22E
m68k_00e22e:
        move.b %d1,%d2
m68k_00e22e_end:
.org 0xE230
m68k_00e230:
        bra.b (. + -20)
m68k_00e230_end:
.org 0xE232
m68k_00e232:
        lea.l 0xf427:w,%a0
m68k_00e232_end:
.org 0xE236
m68k_00e236:
        move.b #0xff,(%a0, %d0.w)
m68k_00e236_end:
.org 0xE23C
m68k_00e23c:
        lea.l 0xe80c:w,%a0
m68k_00e23c_end:
.org 0xE240
m68k_00e240:
        move.w %d0,%d1
m68k_00e240_end:
.org 0xE242
m68k_00e242:
        lsl.w #0x1,%d1
m68k_00e242_end:
.org 0xE244
m68k_00e244:
        add.w %d0,%d1
m68k_00e244_end:
.org 0xE246
m68k_00e246:
        lsl.w #0x2,%d1
m68k_00e246_end:
.org 0xE248
m68k_00e248:
        move.w #0xffff,(%a0, %d1.w)
m68k_00e248_end:
.org 0xE24E
m68k_00e24e:
        move.w #0xffff,0x4(%a0, %d1.w)
m68k_00e24e_end:
.org 0xE254
m68k_00e254:
        move.w #0xffff,0x8(%a0, %d1.w)
m68k_00e254_end:
.org 0xE25A
m68k_00e25a:
        lsl.w #0x1,%d0
m68k_00e25a_end:
.org 0xE25C
m68k_00e25c:
        lea.l 0xf45e:w,%a0
m68k_00e25c_end:
.org 0xE260
m68k_00e260:
        move.w %d4,(%a0, %d0.w)
m68k_00e260_end:
.org 0xE264
m68k_00e264:
        move.w %d4,%d0
m68k_00e264_end:
.org 0xE266
m68k_00e266:
        movem.l (%a7)+,%d1-%d5/%a0-%a2
m68k_00e266_end:
.org 0xE26A
m68k_00e26a:
        rts
m68k_00e26a_end:
.org 0xE26C
m68k_00e26c:
        lea.l 0xf427:w,%a2
m68k_00e26c_end:
.org 0xE270
m68k_00e270:
        clr.w %d5
m68k_00e270_end:
.org 0xE272
m68k_00e272:
        move.b (%a2, %d0.w),%d5
m68k_00e272_end:
.org 0xE276
m68k_00e276:
        lsl.w #0x1,%d5
m68k_00e276_end:
.org 0xE278
m68k_00e278:
        lea.l 0xe640:w,%a2
m68k_00e278_end:
.org 0xE27C
m68k_00e27c:
        move.w (%a2, %d5.w),%d5
m68k_00e27c_end:
.org 0xE280
m68k_00e280:
        lea.l 0xf500:w,%a2
m68k_00e280_end:
.org 0xE284
m68k_00e284:
        tst.w (%a2)
m68k_00e284_end:
.org 0xE286
m68k_00e286:
        bmi.w (. + 18)
m68k_00e286_end:
.org 0xE28A
m68k_00e28a:
        cmp.w (%a2)+,%d5
m68k_00e28a_end:
.org 0xE28C
m68k_00e28c:
        bne.b (. + -8)
m68k_00e28c_end:
.org 0xE28E
m68k_00e28e:
        move.w %d5,%d4
m68k_00e28e_end:
.org 0xE290
m68k_00e290:
        ori.w #0x1,%sr
m68k_00e290_end:
.org 0xE294
m68k_00e294:
        bra.w (. + 8)
m68k_00e294_end:
.org 0xE298
m68k_00e298:
        andi.w #0xfffe,%sr
m68k_00e298_end:
.org 0xE29C
m68k_00e29c:
        rts
m68k_00e29c_end:
.org 0xE29E
m68k_00e29e:
        lea.l 0xf590:w,%a0
m68k_00e29e_end:
.org 0xE2A2
m68k_00e2a2:
        addq.b #0x1,(%a0, %d0.w)
m68k_00e2a2_end:
.org 0xE2A6
m68k_00e2a6:
        cmpi.b #0x4,(%a0, %d0.w)
m68k_00e2a6_end:
.org 0xE2AC
m68k_00e2ac:
        bls.b (. + 32)
m68k_00e2ac_end:
.org 0xE2AE
m68k_00e2ae:
        move.w %d0,%d1
m68k_00e2ae_end:
.org 0xE2B0
m68k_00e2b0:
        lsl.w #0x1,%d1
m68k_00e2b0_end:
.org 0xE2B2
m68k_00e2b2:
        lea.l 0xe640:w,%a0
m68k_00e2b2_end:
.org 0xE2B6
m68k_00e2b6:
        move.w #0xffff,(%a0, %d1.w)
m68k_00e2b6_end:
.org 0xE2BC
m68k_00e2bc:
        move.w %d0,0xf64c:w
m68k_00e2bc_end:
.org 0xE2C0
m68k_00e2c0:
        bsr.w (. + 206)
m68k_00e2c0_end:
.org 0xE2C4
m68k_00e2c4:
        bsr.w (. + 286)
m68k_00e2c4_end:
.org 0xE2C8
m68k_00e2c8:
        bra.w (. + 196)
m68k_00e2c8_end:
.org 0xE2CC
m68k_00e2cc:
        move.w %d0,%d1
m68k_00e2cc_end:
.org 0xE2CE
m68k_00e2ce:
        lsl.w #0x1,%d1
m68k_00e2ce_end:
.org 0xE2D0
m68k_00e2d0:
        lea.l 0xe640:w,%a0
m68k_00e2d0_end:
.org 0xE2D4
m68k_00e2d4:
        move.w (%a0, %d1.w),%d2
m68k_00e2d4_end:
.org 0xE2D8
m68k_00e2d8:
        lea.l 0xcc00:w,%a1
m68k_00e2d8_end:
.org 0xE2DC
m68k_00e2dc:
        move.b (%a1, %d2.w),%d3
m68k_00e2dc_end:
.org 0xE2E0
m68k_00e2e0:
        move.b #0xff,(%a1, %d2.w)
m68k_00e2e0_end:
.org 0xE2E6
m68k_00e2e6:
        move.w %d0,-(%a7)
m68k_00e2e6_end:
.org 0xE2E8
m68k_00e2e8:
        ext.w %d3
m68k_00e2e8_end:
.org 0xE2EA
m68k_00e2ea:
        move.w %d3,%d0
m68k_00e2ea_end:
.org 0xE2EC
m68k_00e2ec:
        move.w #0xffff,0xf630:w
m68k_00e2ec_end:
.org 0xE2F2
m68k_00e2f2:
        jsr 0x5f48:l
m68k_00e2f2_end:
.org 0xE2F8
m68k_00e2f8:
        bsr.w (. + -258)
m68k_00e2f8_end:
.org 0xE2FC
m68k_00e2fc:
        move.w (%a7)+,%d0
m68k_00e2fc_end:
.org 0xE2FE
m68k_00e2fe:
        lea.l 0xf450:w,%a0
m68k_00e2fe_end:
.org 0xE302
m68k_00e302:
        lea.l 0xf5a0:w,%a1
m68k_00e302_end:
.org 0xE306
m68k_00e306:
        move.w #0x27,%d1
m68k_00e306_end:
.org 0xE30A
m68k_00e30a:
        cmp.b -(%a0),%d0
m68k_00e30a_end:
.org 0xE30C
m68k_00e30c:
        bne.b (. + 4)
m68k_00e30c_end:
.org 0xE30E
m68k_00e30e:
        move.b %d1,(%a1)+
m68k_00e30e_end:
.org 0xE310
m68k_00e310:
        dbra %d1,(. + -6)
m68k_00e310_end:
.org 0xE314
m68k_00e314:
        move.b #0xff,(%a1)
m68k_00e314_end:
.org 0xE318
m68k_00e318:
        lea.l 0xcd00:w,%a0
m68k_00e318_end:
.org 0xE31C
m68k_00e31c:
        move.w #0xff,%d1
m68k_00e31c_end:
.org 0xE320
m68k_00e320:
        clr.l %d5
m68k_00e320_end:
.org 0xE322
m68k_00e322:
        lea.l 0xf5a0:w,%a1
m68k_00e322_end:
.org 0xE326
m68k_00e326:
        move.b -(%a0),%d2
m68k_00e326_end:
.org 0xE328
m68k_00e328:
        beq.b (. + 56)
m68k_00e328_end:
.org 0xE32A
m68k_00e32a:
        bmi.b (. + 54)
m68k_00e32a_end:
.org 0xE32C
m68k_00e32c:
        subq.b #0x1,%d2
m68k_00e32c_end:
.org 0xE32E
m68k_00e32e:
        move.b (%a1)+,%d3
m68k_00e32e_end:
.org 0xE330
m68k_00e330:
        bmi.b (. + 48)
m68k_00e330_end:
.org 0xE332
m68k_00e332:
        cmp.b %d2,%d3
m68k_00e332_end:
.org 0xE334
m68k_00e334:
        beq.b (. + 6)
m68k_00e334_end:
.org 0xE336
m68k_00e336:
        bcs.b (. + 42)
m68k_00e336_end:
.org 0xE338
m68k_00e338:
        bra.b (. + -10)
m68k_00e338_end:
.org 0xE33A
m68k_00e33a:
        move.w %d1,%d6
m68k_00e33a_end:
.org 0xE33C
m68k_00e33c:
        lsl.w #0x1,%d6
m68k_00e33c_end:
.org 0xE33E
m68k_00e33e:
        lea.l 0xc000:w,%a2
m68k_00e33e_end:
.org 0xE342
m68k_00e342:
        moveq #0,%d7
m68k_00e342_end:
.org 0xE344
m68k_00e344:
        move.w (%a2, %d6.w),%d7
m68k_00e344_end:
.org 0xE348
m68k_00e348:
        lea.l 0xbe00:w,%a2
m68k_00e348_end:
.org 0xE34C
m68k_00e34c:
        add.w (%a2, %d6.w),%d7
m68k_00e34c_end:
.org 0xE350
m68k_00e350:
        bcc.b (. + 8)
m68k_00e350_end:
.org 0xE352
m68k_00e352:
        addi.l #0x10000,%d7
m68k_00e352_end:
.org 0xE358
m68k_00e358:
        cmp.l %d5,%d7
m68k_00e358_end:
.org 0xE35A
m68k_00e35a:
        bls.b (. + 6)
m68k_00e35a_end:
.org 0xE35C
m68k_00e35c:
        move.l %d7,%d5
m68k_00e35c_end:
.org 0xE35E
m68k_00e35e:
        move.w %d1,%d4
m68k_00e35e_end:
.org 0xE360
m68k_00e360:
        dbra %d1,(. + -62)
m68k_00e360_end:
.org 0xE364
m68k_00e364:
        move.w %d0,%d1
m68k_00e364_end:
.org 0xE366
m68k_00e366:
        lsl.w #0x1,%d1
m68k_00e366_end:
.org 0xE368
m68k_00e368:
        lea.l 0xe640:w,%a0
m68k_00e368_end:
.org 0xE36C
m68k_00e36c:
        move.w %d4,(%a0, %d1.w)
m68k_00e36c_end:
.org 0xE370
m68k_00e370:
        lea.l 0xcc00:w,%a0
m68k_00e370_end:
.org 0xE374
m68k_00e374:
        move.b (%a0, %d4.w),%d1
m68k_00e374_end:
.org 0xE378
m68k_00e378:
        ext.w %d1
m68k_00e378_end:
.org 0xE37A
m68k_00e37a:
        lsl.w #0x1,%d1
m68k_00e37a_end:
.org 0xE37C
m68k_00e37c:
        lea.l 0xf45e:w,%a0
m68k_00e37c_end:
.org 0xE380
m68k_00e380:
        move.w %d4,(%a0, %d1.w)
m68k_00e380_end:
.org 0xE384
m68k_00e384:
        lea.l 0xc300:w,%a0
m68k_00e384_end:
.org 0xE388
m68k_00e388:
        clr.b (%a0, %d4.w)
m68k_00e388_end:
.org 0xE38C
m68k_00e38c:
        rts
m68k_00e38c_end:
.org 0xE38E
m68k_00e38e:
        movem.l %d0-%d2/%a0-%a1,-(%a7)
m68k_00e38e_end:
.org 0xE392
m68k_00e392:
        move.w 0xf64c:w,%d0
m68k_00e392_end:
.org 0xE396
m68k_00e396:
        lea.l 0xf450:w,%a0
m68k_00e396_end:
.org 0xE39A
m68k_00e39a:
        lea.l 0xf5a0:w,%a1
m68k_00e39a_end:
.org 0xE39E
m68k_00e39e:
        move.w #0x27,%d1
m68k_00e39e_end:
.org 0xE3A2
m68k_00e3a2:
        cmp.b -(%a0),%d0
m68k_00e3a2_end:
.org 0xE3A4
m68k_00e3a4:
        bne.b (. + 4)
m68k_00e3a4_end:
.org 0xE3A6
m68k_00e3a6:
        move.b %d1,(%a1)+
m68k_00e3a6_end:
.org 0xE3A8
m68k_00e3a8:
        dbra %d1,(. + -6)
m68k_00e3a8_end:
.org 0xE3AC
m68k_00e3ac:
        move.b #0xff,(%a1)
m68k_00e3ac_end:
.org 0xE3B0
m68k_00e3b0:
        lea.l 0xcc00:w,%a0
m68k_00e3b0_end:
.org 0xE3B4
m68k_00e3b4:
        move.w #0xff,%d0
m68k_00e3b4_end:
.org 0xE3B8
m68k_00e3b8:
        lea.l 0xf5a0:w,%a1
m68k_00e3b8_end:
.org 0xE3BC
m68k_00e3bc:
        move.b (%a0)+,%d2
m68k_00e3bc_end:
.org 0xE3BE
m68k_00e3be:
        beq.b (. + 22)
m68k_00e3be_end:
.org 0xE3C0
m68k_00e3c0:
        bmi.b (. + 20)
m68k_00e3c0_end:
.org 0xE3C2
m68k_00e3c2:
        subq.b #0x1,%d2
m68k_00e3c2_end:
.org 0xE3C4
m68k_00e3c4:
        move.b (%a1)+,%d1
m68k_00e3c4_end:
.org 0xE3C6
m68k_00e3c6:
        bmi.b (. + 14)
m68k_00e3c6_end:
.org 0xE3C8
m68k_00e3c8:
        cmp.b %d2,%d1
m68k_00e3c8_end:
.org 0xE3CA
m68k_00e3ca:
        beq.b (. + 6)
m68k_00e3ca_end:
.org 0xE3CC
m68k_00e3cc:
        bcs.b (. + 8)
m68k_00e3cc_end:
.org 0xE3CE
m68k_00e3ce:
        bra.b (. + -10)
m68k_00e3ce_end:
.org 0xE3D0
m68k_00e3d0:
        ori.b #0x80,(%a0)
m68k_00e3d0_end:
.org 0xE3D4
m68k_00e3d4:
        adda.w #0x1,%a0
m68k_00e3d4_end:
.org 0xE3D8
m68k_00e3d8:
        dbra %d0,(. + -32)
m68k_00e3d8_end:
.org 0xE3DC
m68k_00e3dc:
        movem.l (%a7)+,%d0-%d2/%a0-%a1
m68k_00e3dc_end:
.org 0xE3E0
m68k_00e3e0:
        rts
m68k_00e3e0_end:
.org 0xE3E2
m68k_00e3e2:
        lea.l 0xf5a0:w,%a0
m68k_00e3e2_end:
.org 0xE3E6
m68k_00e3e6:
        lea.l 0xcc00:w,%a1
m68k_00e3e6_end:
.org 0xE3EA
m68k_00e3ea:
        clr.w %d0
m68k_00e3ea_end:
.org 0xE3EC
m68k_00e3ec:
        move.b (%a0)+,%d0
m68k_00e3ec_end:
.org 0xE3EE
m68k_00e3ee:
        bmi.b (. + 8)
m68k_00e3ee_end:
.org 0xE3F0
m68k_00e3f0:
        clr.b (%a0, %d0.w)
m68k_00e3f0_end:
.org 0xE3F4
m68k_00e3f4:
        bra.b (. + -8)
m68k_00e3f4_end:
.org 0xE3F6
m68k_00e3f6:
        rts
m68k_00e3f6_end:
.org 0xE3F8
m68k_00e3f8:
        rts
m68k_00e3f8_end:
.org 0xE3FA
m68k_00e3fa:
        move.w 0xf364:w,%d0
m68k_00e3fa_end:
.org 0xE3FE
m68k_00e3fe:
        lsl.w #0x1,%d0
m68k_00e3fe_end:
.org 0xE400
m68k_00e400:
        add.w 0xf364:w,%d0
m68k_00e400_end:
.org 0xE404
m68k_00e404:
        lsl.w #0x2,%d0
m68k_00e404_end:
.org 0xE406
m68k_00e406:
        lea.l 0xe80c:w,%a0
m68k_00e406_end:
.org 0xE40A
m68k_00e40a:
        lea.l 0xcd00:w,%a1
m68k_00e40a_end:
.org 0xE40E
m68k_00e40e:
        move.w 0x4(%a0, %d0.w),%d1
m68k_00e40e_end:
.org 0xE412
m68k_00e412:
        bmi.b (. + 18)
m68k_00e412_end:
.org 0xE414
m68k_00e414:
        clr.b (%a1, %d1.w)
m68k_00e414_end:
.org 0xE418
m68k_00e418:
        move.w #0xffff,0x4(%a0, %d0.w)
m68k_00e418_end:
.org 0xE41E
m68k_00e41e:
        cmp.w 0xf3a6:w,%d1
m68k_00e41e_end:
.org 0xE422
m68k_00e422:
        beq.b (. + 28)
m68k_00e422_end:
.org 0xE424
m68k_00e424:
        move.w 0xf3a6:w,0x4(%a0, %d0.w)
m68k_00e424_end:
.org 0xE42A
m68k_00e42a:
        move.w 0xf3a0:w,0x6(%a0, %d0.w)
m68k_00e42a_end:
.org 0xE430
m68k_00e430:
        move.w 0xf3a6:w,%d0
m68k_00e430_end:
.org 0xE434
m68k_00e434:
        lea.l 0xcd00:w,%a0
m68k_00e434_end:
.org 0xE438
m68k_00e438:
        move.b #0x3,(%a0, %d0.w)
m68k_00e438_end:
.org 0xE43E
m68k_00e43e:
        rts
m68k_00e43e_end:
.org 0xE440
m68k_00e440:
        move.b 0xf57b:w,%d0
m68k_00e440_end:
.org 0xE444
m68k_00e444:
        cmpi.b #0x29,%d0
m68k_00e444_end:
.org 0xE448
m68k_00e448:
        bne.b (. + 8)
m68k_00e448_end:
.org 0xE44A
m68k_00e44a:
        bsr.w (. + 24)
m68k_00e44a_end:
.org 0xE44E
m68k_00e44e:
        bra.b (. + 18)
m68k_00e44e_end:
.org 0xE450
m68k_00e450:
        cmpi.b #0x7d,%d0
m68k_00e450_end:
.org 0xE454
m68k_00e454:
        bne.b (. + 8)
m68k_00e454_end:
.org 0xE456
m68k_00e456:
        bsr.w (. + 78)
m68k_00e456_end:
.org 0xE45A
m68k_00e45a:
        bra.b (. + 6)
m68k_00e45a_end:
.org 0xE45C
m68k_00e45c:
        bsr.w (. + 180)
m68k_00e45c_end:
.org 0xE460
m68k_00e460:
        rts
m68k_00e460_end:
.org 0xE462
m68k_00e462:
        cmpi.w #0x80,0xf38c:w
m68k_00e462_end:
.org 0xE468
m68k_00e468:
        beq.w (. + 58)
m68k_00e468_end:
.org 0xE46C
m68k_00e46c:
        move.w 0xf392:w,%d0
m68k_00e46c_end:
.org 0xE470
m68k_00e470:
        lsl.w #0x1,%d0
m68k_00e470_end:
.org 0xE472
m68k_00e472:
        lea.l 0xf45e:w,%a0
m68k_00e472_end:
.org 0xE476
m68k_00e476:
        move.w 0xf3a6:w,(%a0, %d0.w)
m68k_00e476_end:
.org 0xE47C
m68k_00e47c:
        move.w #0x208,0xf612:w
m68k_00e47c_end:
.org 0xE482
m68k_00e482:
        move.w #0x28,0xf362:w
m68k_00e482_end:
.org 0xE488
m68k_00e488:
        move.w #0x16,0xf3fe:w
m68k_00e488_end:
.org 0xE48E
m68k_00e48e:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00e48e_end:
.org 0xE494
m68k_00e494:
        move.w #0x1,0xf774:w
m68k_00e494_end:
.org 0xE49A
m68k_00e49a:
        move.w #0x14,0xff7026:l
m68k_00e49a_end:
.org 0xE4A2
m68k_00e4a2:
        rts
m68k_00e4a2_end:
.org 0xE4A4
m68k_00e4a4:
        cmpi.w #0x82,0xf38c:w
m68k_00e4a4_end:
.org 0xE4AA
m68k_00e4aa:
        beq.w (. + 100)
m68k_00e4aa_end:
.org 0xE4AE
m68k_00e4ae:
        move.w 0xf3a6:w,%d0
m68k_00e4ae_end:
.org 0xE4B2
m68k_00e4b2:
        lea.l 0xc700:w,%a0
m68k_00e4b2_end:
.org 0xE4B6
m68k_00e4b6:
        move.w #0x208,0xf612:w
m68k_00e4b6_end:
.org 0xE4BC
m68k_00e4bc:
        move.w #0x20,0xf362:w
m68k_00e4bc_end:
.org 0xE4C2
m68k_00e4c2:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00e4c2_end:
.org 0xE4C8
m68k_00e4c8:
        btst.b #0x4,(%a0, %d0.w)
m68k_00e4c8_end:
.org 0xE4CE
m68k_00e4ce:
        bne.w (. + 32)
m68k_00e4ce_end:
.org 0xE4D2
m68k_00e4d2:
        ori.b #0x10,(%a0, %d0.w)
m68k_00e4d2_end:
.org 0xE4D8
m68k_00e4d8:
        move.w #0x14,0xff7026:l
m68k_00e4d8_end:
.org 0xE4E0
m68k_00e4e0:
        move.w #0x28,0xf362:w
m68k_00e4e0_end:
.org 0xE4E6
m68k_00e4e6:
        move.w #0x18,%d0
m68k_00e4e6_end:
.org 0xE4EA
m68k_00e4ea:
        bra.w (. + 20)
m68k_00e4ea_end:
.org 0xE4EE
m68k_00e4ee:
        move.w #0x1,0xf608:w
m68k_00e4ee_end:
.org 0xE4F4
m68k_00e4f4:
        move.w #0x1f,0xf362:w
m68k_00e4f4_end:
.org 0xE4FA
m68k_00e4fa:
        move.w #0xad,%d0
m68k_00e4fa_end:
.org 0xE4FE
m68k_00e4fe:
        move.w %d0,0xf3fe:w
m68k_00e4fe_end:
.org 0xE502
m68k_00e502:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00e502_end:
.org 0xE508
m68k_00e508:
        move.w #0x1,0xf774:w
m68k_00e508_end:
.org 0xE50E
m68k_00e50e:
        rts
m68k_00e50e_end:
.org 0xE510
m68k_00e510:
        cmpi.w #0x84,0xf38c:w
m68k_00e510_end:
.org 0xE516
m68k_00e516:
        beq.b (. + -116)
m68k_00e516_end:
.org 0xE518
m68k_00e518:
        move.w 0xf3a6:w,%d0
m68k_00e518_end:
.org 0xE51C
m68k_00e51c:
        move.w 0xf3b4:w,%d1
m68k_00e51c_end:
.org 0xE520
m68k_00e520:
        lea.l 0xf580:w,%a0
m68k_00e520_end:
.org 0xE524
m68k_00e524:
        move.b #0x5,%d2
m68k_00e524_end:
.org 0xE528
m68k_00e528:
        sub.b (%a0, %d1.w),%d2
m68k_00e528_end:
.org 0xE52C
m68k_00e52c:
        lea.l 0xc700:w,%a0
m68k_00e52c_end:
.org 0xE530
m68k_00e530:
        move.b (%a0, %d0.w),%d3
m68k_00e530_end:
.org 0xE534
m68k_00e534:
        andi.w #0x10,%d3
m68k_00e534_end:
.org 0xE538
m68k_00e538:
        or.w %d2,%d3
m68k_00e538_end:
.org 0xE53A
m68k_00e53a:
        move.w %d0,%d2
m68k_00e53a_end:
.org 0xE53C
m68k_00e53c:
        lsl.w #0x1,%d2
m68k_00e53c_end:
.org 0xE53E
m68k_00e53e:
        lea.l 0xc000:w,%a1
m68k_00e53e_end:
.org 0xE542
m68k_00e542:
        move.w (%a1, %d2.w),%d4
m68k_00e542_end:
.org 0xE546
m68k_00e546:
        lea.l 0xbe00:w,%a1
m68k_00e546_end:
.org 0xE54A
m68k_00e54a:
        cmp.w (%a1, %d2.w),%d4
m68k_00e54a_end:
.org 0xE54E
m68k_00e54e:
        bcc.w (. + 8)
m68k_00e54e_end:
.org 0xE552
m68k_00e552:
        bset.l #0x3,%d3
m68k_00e552_end:
.org 0xE556
m68k_00e556:
        move.b %d3,(%a0, %d0.w)
m68k_00e556_end:
.org 0xE55A
m68k_00e55a:
        move.w #0x28,0xf362:w
m68k_00e55a_end:
.org 0xE560
m68k_00e560:
        move.w #0x17,0xf3fe:w
m68k_00e560_end:
.org 0xE566
m68k_00e566:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00e566_end:
.org 0xE56C
m68k_00e56c:
        move.w #0x1,0xf774:w
m68k_00e56c_end:
.org 0xE572
m68k_00e572:
        move.w #0x14,0xff7026:l
m68k_00e572_end:
.org 0xE57A
m68k_00e57a:
        rts
m68k_00e57a_end:
.org 0xE57C
m68k_00e57c:
        lea.l 0xe3bc:w,%a0
m68k_00e57c_end:
.org 0xE580
m68k_00e580:
        move.w 0xf392:w,%d0
m68k_00e580_end:
.org 0xE584
m68k_00e584:
        lsl.w #0x2,%d0
m68k_00e584_end:
.org 0xE586
m68k_00e586:
        clr.w (%a0, %d0.w)
m68k_00e586_end:
.org 0xE58A
m68k_00e58a:
        move.w 0xf3b6:w,0x2(%a0, %d0.w)
m68k_00e58a_end:
.org 0xE590
m68k_00e590:
        rts
m68k_00e590_end:
.org 0xE592
m68k_00e592:
        bsr.w (. + 376)
m68k_00e592_end:
.org 0xE596
m68k_00e596:
        lea.l 0xc300:w,%a0
m68k_00e596_end:
.org 0xE59A
m68k_00e59a:
        move.w 0xf630:w,%d0
m68k_00e59a_end:
.org 0xE59E
m68k_00e59e:
        cmp.w 0xf3a6:w,%d0
m68k_00e59e_end:
.org 0xE5A2
m68k_00e5a2:
        beq.b (. + 18)
m68k_00e5a2_end:
.org 0xE5A4
m68k_00e5a4:
        cmp.w 0xf634:w,%d0
m68k_00e5a4_end:
.org 0xE5A8
m68k_00e5a8:
        beq.b (. + 12)
m68k_00e5a8_end:
.org 0xE5AA
m68k_00e5aa:
        move.b (%a0, %d0.w),%d0
m68k_00e5aa_end:
.org 0xE5AE
m68k_00e5ae:
        ext.w %d0
m68k_00e5ae_end:
.org 0xE5B0
m68k_00e5b0:
        bra.w (. + 8)
m68k_00e5b0_end:
.org 0xE5B4
m68k_00e5b4:
        move.w #0x64,%d0
m68k_00e5b4_end:
.org 0xE5B8
m68k_00e5b8:
        move.w 0xf3a6:w,%d1
m68k_00e5b8_end:
.org 0xE5BC
m68k_00e5bc:
        move.b (%a0, %d1.w),%d1
m68k_00e5bc_end:
.org 0xE5C0
m68k_00e5c0:
        ext.w %d1
m68k_00e5c0_end:
.org 0xE5C2
m68k_00e5c2:
        bsr.w (. + 348)
m68k_00e5c2_end:
.org 0xE5C6
m68k_00e5c6:
        move.l 0xf39e:w,%d3
m68k_00e5c6_end:
.org 0xE5CA
m68k_00e5ca:
        lsl.l #0x1,%d3
m68k_00e5ca_end:
.org 0xE5CC
m68k_00e5cc:
        move.w 0xf3a6:w,%d4
m68k_00e5cc_end:
.org 0xE5D0
m68k_00e5d0:
        lsl.w #0x1,%d4
m68k_00e5d0_end:
.org 0xE5D2
m68k_00e5d2:
        lea.l 0xb600:w,%a0
m68k_00e5d2_end:
.org 0xE5D6
m68k_00e5d6:
        move.w (%a0, %d4.w),%d5
m68k_00e5d6_end:
.org 0xE5DA
m68k_00e5da:
        mulu.w #0xa,%d5
m68k_00e5da_end:
.org 0xE5DE
m68k_00e5de:
        add.l %d5,%d3
m68k_00e5de_end:
.org 0xE5E0
m68k_00e5e0:
        lea.l 0xbe00:w,%a0
m68k_00e5e0_end:
.org 0xE5E4
m68k_00e5e4:
        move.w (%a0, %d4.w),%d4
m68k_00e5e4_end:
.org 0xE5E8
m68k_00e5e8:
        mulu.w #0x5,%d4
m68k_00e5e8_end:
.org 0xE5EC
m68k_00e5ec:
        add.l %d4,%d3
m68k_00e5ec_end:
.org 0xE5EE
m68k_00e5ee:
        move.w 0xf3a6:w,%d4
m68k_00e5ee_end:
.org 0xE5F2
m68k_00e5f2:
        lea.l 0xc200:w,%a0
m68k_00e5f2_end:
.org 0xE5F6
m68k_00e5f6:
        clr.w %d7
m68k_00e5f6_end:
.org 0xE5F8
m68k_00e5f8:
        move.b (%a0, %d4.w),%d7
m68k_00e5f8_end:
.org 0xE5FC
m68k_00e5fc:
        cmpi.w #0x1e,%d7
m68k_00e5fc_end:
.org 0xE600
m68k_00e600:
        bhi.b (. + 4)
m68k_00e600_end:
.org 0xE602
m68k_00e602:
        lsr.w #0x1,%d3
m68k_00e602_end:
.org 0xE604
m68k_00e604:
        moveq #0,%d4
m68k_00e604_end:
.org 0xE606
m68k_00e606:
        move.w 0xf61c:w,%d4
m68k_00e606_end:
.org 0xE60A
m68k_00e60a:
        move.l %d4,%d5
m68k_00e60a_end:
.org 0xE60C
m68k_00e60c:
        lsl.l #0x1,%d4
m68k_00e60c_end:
.org 0xE60E
m68k_00e60e:
        add.l %d5,%d4
m68k_00e60e_end:
.org 0xE610
m68k_00e610:
        swap %d4
m68k_00e610_end:
.org 0xE612
m68k_00e612:
        add.w %d2,%d4
m68k_00e612_end:
.org 0xE614
m68k_00e614:
        mulu.w %d7,%d4
m68k_00e614_end:
.org 0xE616
m68k_00e616:
        move.w %d3,%d5
m68k_00e616_end:
.org 0xE618
m68k_00e618:
        mulu.w %d4,%d5
m68k_00e618_end:
.org 0xE61A
m68k_00e61a:
        swap %d3
m68k_00e61a_end:
.org 0xE61C
m68k_00e61c:
        mulu.w %d4,%d3
m68k_00e61c_end:
.org 0xE61E
m68k_00e61e:
        swap %d3
m68k_00e61e_end:
.org 0xE620
m68k_00e620:
        add.l %d5,%d3
m68k_00e620_end:
.org 0xE622
m68k_00e622:
        divu.w #0x2710,%d3
m68k_00e622_end:
.org 0xE626
m68k_00e626:
        andi.l #0xffff,%d3
m68k_00e626_end:
.org 0xE62C
m68k_00e62c:
        divu.w #0x3c,%d3
m68k_00e62c_end:
.org 0xE630
m68k_00e630:
        clr.w 0xf3c8:w
m68k_00e630_end:
.org 0xE634
m68k_00e634:
        move.w %d3,0xf3ca:w
m68k_00e634_end:
.org 0xE638
m68k_00e638:
        move.w 0xf3a6:w,%d0
m68k_00e638_end:
.org 0xE63C
m68k_00e63c:
        lea.l 0xc300:w,%a0
m68k_00e63c_end:
.org 0xE640
m68k_00e640:
        move.b (%a0, %d0.w),%d1
m68k_00e640_end:
.org 0xE644
m68k_00e644:
        ext.w %d1
m68k_00e644_end:
.org 0xE646
m68k_00e646:
        add.w %d3,%d1
m68k_00e646_end:
.org 0xE648
m68k_00e648:
        cmpi.w #0x64,%d1
m68k_00e648_end:
.org 0xE64C
m68k_00e64c:
        bls.b (. + 16)
m68k_00e64c_end:
.org 0xE64E
m68k_00e64e:
        move.w %d1,%d2
m68k_00e64e_end:
.org 0xE650
m68k_00e650:
        subi.w #0x64,%d2
m68k_00e650_end:
.org 0xE654
m68k_00e654:
        sub.w %d2,0xf3ca:w
m68k_00e654_end:
.org 0xE658
m68k_00e658:
        move.w #0x64,%d1
m68k_00e658_end:
.org 0xE65C
m68k_00e65c:
        move.b %d1,(%a0, %d0.w)
m68k_00e65c_end:
.org 0xE660
m68k_00e660:
        move.w 0xf630:w,%d0
m68k_00e660_end:
.org 0xE664
m68k_00e664:
        cmp.w 0xf3a6:w,%d0
m68k_00e664_end:
.org 0xE668
m68k_00e668:
        bne.w (. + 8)
m68k_00e668_end:
.org 0xE66C
m68k_00e66c:
        move.w 0xf634:w,%d0
m68k_00e66c_end:
.org 0xE670
m68k_00e670:
        lea.l 0xc200:w,%a0
m68k_00e670_end:
.org 0xE674
m68k_00e674:
        move.b (%a0, %d0.w),%d1
m68k_00e674_end:
.org 0xE678
m68k_00e678:
        addq.b #0x1,%d1
m68k_00e678_end:
.org 0xE67A
m68k_00e67a:
        cmpi.b #0x64,%d1
m68k_00e67a_end:
.org 0xE67E
m68k_00e67e:
        bls.w (. + 8)
m68k_00e67e_end:
.org 0xE682
m68k_00e682:
        move.b #0x64,%d1
m68k_00e682_end:
.org 0xE686
m68k_00e686:
        move.b %d1,(%a0, %d0.w)
m68k_00e686_end:
.org 0xE68A
m68k_00e68a:
        lsl.w #0x1,%d0
m68k_00e68a_end:
.org 0xE68C
m68k_00e68c:
        lea.l 0xbe00:w,%a0
m68k_00e68c_end:
.org 0xE690
m68k_00e690:
        lsr.w #0x1,%d3
m68k_00e690_end:
.org 0xE692
m68k_00e692:
        add.w (%a0, %d0.w),%d3
m68k_00e692_end:
.org 0xE696
m68k_00e696:
        cmpi.w #0x3e7,%d3
m68k_00e696_end:
.org 0xE69A
m68k_00e69a:
        bls.w (. + 8)
m68k_00e69a_end:
.org 0xE69E
m68k_00e69e:
        move.w #0x3e7,%d3
m68k_00e69e_end:
.org 0xE6A2
m68k_00e6a2:
        move.w %d3,(%a0, %d0.w)
m68k_00e6a2_end:
.org 0xE6A6
m68k_00e6a6:
        lea.l 0xcd00:w,%a0
m68k_00e6a6_end:
.org 0xE6AA
m68k_00e6aa:
        move.w 0xf3a6:w,%d0
m68k_00e6aa_end:
.org 0xE6AE
m68k_00e6ae:
        move.b #0x1,(%a0, %d0.w)
m68k_00e6ae_end:
.org 0xE6B4
m68k_00e6b4:
        move.w 0xf376:w,%d0
m68k_00e6b4_end:
.org 0xE6B8
m68k_00e6b8:
        cmp.w 0xf67a:w,%d0
m68k_00e6b8_end:
.org 0xE6BC
m68k_00e6bc:
        beq.w (. + 20)
m68k_00e6bc_end:
.org 0xE6C0
m68k_00e6c0:
        cmp.w 0xf67c:w,%d0
m68k_00e6c0_end:
.org 0xE6C4
m68k_00e6c4:
        beq.w (. + 12)
m68k_00e6c4_end:
.org 0xE6C8
m68k_00e6c8:
        cmp.w 0xf67e:w,%d0
m68k_00e6c8_end:
.org 0xE6CC
m68k_00e6cc:
        bne.w (. + 60)
m68k_00e6cc_end:
.org 0xE6D0
m68k_00e6d0:
        move.w #0x16,0xff7026:l
m68k_00e6d0_end:
.org 0xE6D8
m68k_00e6d8:
        tst.w 0xf3ca:w
m68k_00e6d8_end:
.org 0xE6DC
m68k_00e6dc:
        beq.w (. + 12)
m68k_00e6dc_end:
.org 0xE6E0
m68k_00e6e0:
        move.w #0xa7,%d0
m68k_00e6e0_end:
.org 0xE6E4
m68k_00e6e4:
        bra.w (. + 8)
m68k_00e6e4_end:
.org 0xE6E8
m68k_00e6e8:
        move.w #0xa8,%d0
m68k_00e6e8_end:
.org 0xE6EC
m68k_00e6ec:
        move.w %d0,0xf3fe:w
m68k_00e6ec_end:
.org 0xE6F0
m68k_00e6f0:
        move.w 0xf38a:w,0xf612:w
m68k_00e6f0_end:
.org 0xE6F6
m68k_00e6f6:
        move.w 0xf38a:w,0xf612:w
m68k_00e6f6_end:
.org 0xE6FC
m68k_00e6fc:
        move.w #0x28,0xf362:w
m68k_00e6fc_end:
.org 0xE702
m68k_00e702:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00e702_end:
.org 0xE708
m68k_00e708:
        rts
m68k_00e708_end:
.org 0xE70A
m68k_00e70a:
        move.w 0xf392:w,%d0
m68k_00e70a_end:
.org 0xE70E
m68k_00e70e:
        lsl.w #0x2,%d0
m68k_00e70e_end:
.org 0xE710
m68k_00e710:
        lea.l 0xdffc:w,%a0
m68k_00e710_end:
.org 0xE714
m68k_00e714:
        move.l 0xf39e:w,%d1
m68k_00e714_end:
.org 0xE718
m68k_00e718:
        sub.l %d1,(%a0, %d0.w)
m68k_00e718_end:
.org 0xE71C
m68k_00e71c:
        rts
m68k_00e71c_end:
.org 0xE71E
m68k_00e71e:
        clr.w %d3
m68k_00e71e_end:
.org 0xE720
m68k_00e720:
        cmpi.w #0x14,%d1
m68k_00e720_end:
.org 0xE724
m68k_00e724:
        bcs.b (. + 36)
m68k_00e724_end:
.org 0xE726
m68k_00e726:
        move.w #0x5,%d3
m68k_00e726_end:
.org 0xE72A
m68k_00e72a:
        cmpi.w #0x28,%d1
m68k_00e72a_end:
.org 0xE72E
m68k_00e72e:
        bcs.b (. + 26)
m68k_00e72e_end:
.org 0xE730
m68k_00e730:
        move.w #0xa,%d3
m68k_00e730_end:
.org 0xE734
m68k_00e734:
        cmpi.w #0x3c,%d1
m68k_00e734_end:
.org 0xE738
m68k_00e738:
        bcs.b (. + 16)
m68k_00e738_end:
.org 0xE73A
m68k_00e73a:
        move.w #0xf,%d3
m68k_00e73a_end:
.org 0xE73E
m68k_00e73e:
        cmpi.w #0x50,%d1
m68k_00e73e_end:
.org 0xE742
m68k_00e742:
        bcs.b (. + 6)
m68k_00e742_end:
.org 0xE744
m68k_00e744:
        move.w #0x14,%d3
m68k_00e744_end:
.org 0xE748
m68k_00e748:
        cmpi.w #0x14,%d0
m68k_00e748_end:
.org 0xE74C
m68k_00e74c:
        bcs.b (. + 28)
m68k_00e74c_end:
.org 0xE74E
m68k_00e74e:
        addq.w #0x1,%d3
m68k_00e74e_end:
.org 0xE750
m68k_00e750:
        cmpi.w #0x28,%d0
m68k_00e750_end:
.org 0xE754
m68k_00e754:
        bcs.b (. + 20)
m68k_00e754_end:
.org 0xE756
m68k_00e756:
        addq.w #0x1,%d3
m68k_00e756_end:
.org 0xE758
m68k_00e758:
        cmpi.w #0x3c,%d0
m68k_00e758_end:
.org 0xE75C
m68k_00e75c:
        bcs.b (. + 12)
m68k_00e75c_end:
.org 0xE75E
m68k_00e75e:
        addq.w #0x1,%d3
m68k_00e75e_end:
.org 0xE760
m68k_00e760:
        cmpi.w #0x50,%d0
m68k_00e760_end:
.org 0xE764
m68k_00e764:
        bcs.b (. + 4)
m68k_00e764_end:
.org 0xE766
m68k_00e766:
        addq.w #0x1,%d3
m68k_00e766_end:
.org 0xE768
m68k_00e768:
        lea.l 12(%pc),%a0
m68k_00e768_end:
.org 0xE76C
m68k_00e76c:
        nop
m68k_00e76c_end:
.org 0xE76E
m68k_00e76e:
        move.b (%a0, %d3.w),%d2
m68k_00e76e_end:
.org 0xE772
m68k_00e772:
        ext.w %d2
m68k_00e772_end:
.org 0xE774
m68k_00e774:
        rts
m68k_00e774_end:
.org 0xE790
m68k_00e790:
        bsr.w (. + 32)
m68k_00e790_end:
.org 0xE794
m68k_00e794:
        move.w #0x208,0xf612:w
m68k_00e794_end:
.org 0xE79A
m68k_00e79a:
        move.w #0x28,0xf362:w
m68k_00e79a_end:
.org 0xE7A0
m68k_00e7a0:
        move.w #0x1b,0xf3fe:w
m68k_00e7a0_end:
.org 0xE7A6
m68k_00e7a6:
        move.w #0xa,0xff7026:l
m68k_00e7a6_end:
.org 0xE7AE
m68k_00e7ae:
        rts
m68k_00e7ae_end:
.org 0xE7B0
m68k_00e7b0:
        move.w 0xf3a8:w,%d0
m68k_00e7b0_end:
.org 0xE7B4
m68k_00e7b4:
        lsl.w #0x2,%d0
m68k_00e7b4_end:
.org 0xE7B6
m68k_00e7b6:
        lea.l 0xcdfc:w,%a0
m68k_00e7b6_end:
.org 0xE7BA
m68k_00e7ba:
        move.w 0xf688:w,%d1
m68k_00e7ba_end:
.org 0xE7BE
m68k_00e7be:
        addq.w #0x1,%d1
m68k_00e7be_end:
.org 0xE7C0
m68k_00e7c0:
        ori.b #0x10,%d1
m68k_00e7c0_end:
.org 0xE7C4
m68k_00e7c4:
        move.b %d1,(%a0, %d0.w)
m68k_00e7c4_end:
.org 0xE7C8
m68k_00e7c8:
        lea.l 0xd4ac6:l,%a1
m68k_00e7c8_end:
.org 0xE7CE
m68k_00e7ce:
        move.w 0xf3a8:w,%d1
m68k_00e7ce_end:
.org 0xE7D2
m68k_00e7d2:
        lsl.w #0x2,%d1
m68k_00e7d2_end:
.org 0xE7D4
m68k_00e7d4:
        move.w 0x2(%a1, %d1.w),%d2
m68k_00e7d4_end:
.org 0xE7D8
m68k_00e7d8:
        lsr.w #0x4,%d2
m68k_00e7d8_end:
.org 0xE7DA
m68k_00e7da:
        move.b %d2,0x1(%a0, %d0.w)
m68k_00e7da_end:
.org 0xE7DE
m68k_00e7de:
        move.w (%a1, %d1.w),%d2
m68k_00e7de_end:
.org 0xE7E2
m68k_00e7e2:
        lsr.w #0x4,%d2
m68k_00e7e2_end:
.org 0xE7E4
m68k_00e7e4:
        move.b %d2,0x2(%a0, %d0.w)
m68k_00e7e4_end:
.org 0xE7E8
m68k_00e7e8:
        move.b 0xf393:w,0x3(%a0, %d0.w)
m68k_00e7e8_end:
.org 0xE7EE
m68k_00e7ee:
        move.w 0xf3a8:w,%d1
m68k_00e7ee_end:
.org 0xE7F2
m68k_00e7f2:
        lsl.w #0x2,%d1
m68k_00e7f2_end:
.org 0xE7F4
m68k_00e7f4:
        lea.l 0xdffc:w,%a1
m68k_00e7f4_end:
.org 0xE7F8
m68k_00e7f8:
        lea.l 0xe09c:w,%a2
m68k_00e7f8_end:
.org 0xE7FC
m68k_00e7fc:
        move.w 0xf688:w,%d0
m68k_00e7fc_end:
.org 0xE800
m68k_00e800:
        lsl.w #0x3,%d0
m68k_00e800_end:
.org 0xE802
m68k_00e802:
        lea.l 0x13b68:l,%a0
m68k_00e802_end:
.org 0xE808
m68k_00e808:
        move.l (%a1, %d1.w),%d2
m68k_00e808_end:
.org 0xE80C
m68k_00e80c:
        sub.l (%a0, %d0.w),%d2
m68k_00e80c_end:
.org 0xE810
m68k_00e810:
        move.l %d2,(%a1, %d1.w)
m68k_00e810_end:
.org 0xE814
m68k_00e814:
        move.l (%a2, %d1.w),%d2
m68k_00e814_end:
.org 0xE818
m68k_00e818:
        sub.l 0x4(%a0, %d0.w),%d2
m68k_00e818_end:
.org 0xE81C
m68k_00e81c:
        move.l %d2,(%a2, %d1.w)
m68k_00e81c_end:
.org 0xE820
m68k_00e820:
        rts
m68k_00e820_end:
.org 0xE822
m68k_00e822:
        bsr.w (. + 12)
m68k_00e822_end:
.org 0xE826
m68k_00e826:
        move.b #0xff,0xf579:w
m68k_00e826_end:
.org 0xE82C
m68k_00e82c:
        rts
m68k_00e82c_end:
.org 0xE82E
m68k_00e82e:
        lea.l 0xcc00:w,%a0
m68k_00e82e_end:
.org 0xE832
m68k_00e832:
        lea.l 0xf427:w,%a1
m68k_00e832_end:
.org 0xE836
m68k_00e836:
        lea.l 0xcd00:w,%a2
m68k_00e836_end:
.org 0xE83A
m68k_00e83a:
        lea.l 0xb200:w,%a3
m68k_00e83a_end:
.org 0xE83E
m68k_00e83e:
        lea.l 0xb000:w,%a4
m68k_00e83e_end:
.org 0xE842
m68k_00e842:
        lea.l 0xea38:w,%a5
m68k_00e842_end:
.org 0xE846
m68k_00e846:
        move.w #0xff,%d0
m68k_00e846_end:
.org 0xE84A
m68k_00e84a:
        move.w 0xf376:w,%d7
m68k_00e84a_end:
.org 0xE84E
m68k_00e84e:
        clr.w %d1
m68k_00e84e_end:
.org 0xE850
m68k_00e850:
        move.b (%a0, %d0.w),%d1
m68k_00e850_end:
.org 0xE854
m68k_00e854:
        cmpi.b #0x28,%d1
m68k_00e854_end:
.org 0xE858
m68k_00e858:
        bhi.w (. + 66)
m68k_00e858_end:
.org 0xE85C
m68k_00e85c:
        tst.b (%a5, %d1.w)
m68k_00e85c_end:
.org 0xE860
m68k_00e860:
        bne.w (. + 58)
m68k_00e860_end:
.org 0xE864
m68k_00e864:
        cmp.b (%a1, %d1.w),%d7
m68k_00e864_end:
.org 0xE868
m68k_00e868:
        bne.w (. + 50)
m68k_00e868_end:
.org 0xE86C
m68k_00e86c:
        tst.b (%a2, %d0.w)
m68k_00e86c_end:
.org 0xE870
m68k_00e870:
        bne.w (. + 42)
m68k_00e870_end:
.org 0xE874
m68k_00e874:
        move.w %d0,%d1
m68k_00e874_end:
.org 0xE876
m68k_00e876:
        lsl.w #0x1,%d1
m68k_00e876_end:
.org 0xE878
m68k_00e878:
        move.w (%a4, %d1.w),%d2
m68k_00e878_end:
.org 0xE87C
m68k_00e87c:
        mulu.w #0xf,%d2
m68k_00e87c_end:
.org 0xE880
m68k_00e880:
        divu.w #0x64,%d2
m68k_00e880_end:
.org 0xE884
m68k_00e884:
        move.w (%a3, %d1.w),%d3
m68k_00e884_end:
.org 0xE888
m68k_00e888:
        add.w %d2,%d3
m68k_00e888_end:
.org 0xE88A
m68k_00e88a:
        cmp.w (%a4, %d1.w),%d3
m68k_00e88a_end:
.org 0xE88E
m68k_00e88e:
        bls.w (. + 8)
m68k_00e88e_end:
.org 0xE892
m68k_00e892:
        move.w (%a4, %d1.w),%d3
m68k_00e892_end:
.org 0xE896
m68k_00e896:
        move.w %d3,(%a3, %d1.w)
m68k_00e896_end:
.org 0xE89A
m68k_00e89a:
        dbra %d0,(. + -76)
m68k_00e89a_end:
.org 0xE89E
m68k_00e89e:
        rts
m68k_00e89e_end:
.org 0xE8A0
m68k_00e8a0:
        lea.l 0xea34:w,%a0
m68k_00e8a0_end:
.org 0xE8A4
m68k_00e8a4:
        lea.l 0xf427:w,%a1
m68k_00e8a4_end:
.org 0xE8A8
m68k_00e8a8:
        move.w #0xf,%d0
m68k_00e8a8_end:
.org 0xE8AC
m68k_00e8ac:
        clr.w %d3
m68k_00e8ac_end:
.org 0xE8AE
m68k_00e8ae:
        move.b (%a0),%d3
m68k_00e8ae_end:
.org 0xE8B0
m68k_00e8b0:
        beq.b (. + 46)
m68k_00e8b0_end:
.org 0xE8DE
m68k_00e8de:
        subq.l #0x4,%a0
m68k_00e8de_end:
.org 0xE8E0
m68k_00e8e0:
        dbra %d0,(. + -52)
m68k_00e8e0_end:
.org 0xE8E4
m68k_00e8e4:
        rts
m68k_00e8e4_end:
.org 0xE8E6
m68k_00e8e6:
        cmpi.b #0x38,0xf57b:w
m68k_00e8e6_end:
.org 0xE8EC
m68k_00e8ec:
        beq.w (. + 332)
m68k_00e8ec_end:
.org 0xE8F0
m68k_00e8f0:
        move.w 0xf392:w,%d0
m68k_00e8f0_end:
.org 0xE8F4
m68k_00e8f4:
        lsl.w #0x2,%d0
m68k_00e8f4_end:
.org 0xE8F6
m68k_00e8f6:
        lea.l 0xdffc:w,%a0
m68k_00e8f6_end:
.org 0xE8FA
m68k_00e8fa:
        move.l 0xf39e:w,%d1
m68k_00e8fa_end:
.org 0xE8FE
m68k_00e8fe:
        sub.l %d1,(%a0, %d0.w)
m68k_00e8fe_end:
.org 0xE902
m68k_00e902:
        lea.l 0xe09c:w,%a0
m68k_00e902_end:
.org 0xE906
m68k_00e906:
        move.l 0xf3ba:w,%d1
m68k_00e906_end:
.org 0xE90A
m68k_00e90a:
        sub.l %d1,(%a0, %d0.w)
m68k_00e90a_end:
.org 0xE90E
m68k_00e90e:
        move.w 0xf3a0:w,%d0
m68k_00e90e_end:
.org 0xE912
m68k_00e912:
        add.w 0xe774:w,%d0
m68k_00e912_end:
.org 0xE916
m68k_00e916:
        moveq #0,%d1
m68k_00e916_end:
.org 0xE918
m68k_00e918:
        move.w 0xefd2:w,%d2
m68k_00e918_end:
.org 0xE91C
m68k_00e91c:
        lsl.w #0x2,%d2
m68k_00e91c_end:
.org 0xE91E
m68k_00e91e:
        lea.l -2494(%pc),%a0
m68k_00e91e_end:
.org 0xE922
m68k_00e922:
        move.w (%a0, %d2.w),%d1
m68k_00e922_end:
.org 0xE926
m68k_00e926:
        move.w 0xf61c:w,%d1
m68k_00e926_end:
.org 0xE92A
m68k_00e92a:
        swap %d1
m68k_00e92a_end:
.org 0xE92C
m68k_00e92c:
        add.w 0x2(%a0, %d2.w),%d1
m68k_00e92c_end:
.org 0xE930
m68k_00e930:
        mulu.w %d1,%d0
m68k_00e930_end:
.org 0xE932
m68k_00e932:
        move.w 0xf376:w,%d1
m68k_00e932_end:
.org 0xE936
m68k_00e936:
        lsl.w #0x1,%d1
m68k_00e936_end:
.org 0xE938
m68k_00e938:
        lea.l 0xe640:w,%a0
m68k_00e938_end:
.org 0xE93C
m68k_00e93c:
        move.w (%a0, %d1.w),%d2
m68k_00e93c_end:
.org 0xE940
m68k_00e940:
        lea.l 0xc200:w,%a1
m68k_00e940_end:
.org 0xE944
m68k_00e944:
        clr.w %d3
m68k_00e944_end:
.org 0xE946
m68k_00e946:
        move.b (%a1, %d2.w),%d3
m68k_00e946_end:
.org 0xE94A
m68k_00e94a:
        move.w #0x78,%d1
m68k_00e94a_end:
.org 0xE94E
m68k_00e94e:
        sub.w %d3,%d1
m68k_00e94e_end:
.org 0xE950
m68k_00e950:
        move.w %d1,%d2
m68k_00e950_end:
.org 0xE952
m68k_00e952:
        lsl.w #0x1,%d1
m68k_00e952_end:
.org 0xE954
m68k_00e954:
        add.w %d2,%d1
m68k_00e954_end:
.org 0xE956
m68k_00e956:
        lsl.w #0x3,%d1
m68k_00e956_end:
.org 0xE958
m68k_00e958:
        add.w %d2,%d1
m68k_00e958_end:
.org 0xE95A
m68k_00e95a:
        lsl.w #0x2,%d1
m68k_00e95a_end:
.org 0xE95C
m68k_00e95c:
        divu.w %d1,%d0
m68k_00e95c_end:
.org 0xE95E
m68k_00e95e:
        cmpi.w #0xa,%d0
m68k_00e95e_end:
.org 0xE962
m68k_00e962:
        bcs.b (. + 80)
m68k_00e962_end:
.org 0xE964
m68k_00e964:
        bsr.w (. + 690)
m68k_00e964_end:
.org 0xE968
m68k_00e968:
        move.w #0x27,0xf3fe:w
m68k_00e968_end:
.org 0xE96E
m68k_00e96e:
        jsr 0x83d4:l
m68k_00e96e_end:
.org 0xE974
m68k_00e974:
        moveq #0,%d0
m68k_00e974_end:
.org 0xE976
m68k_00e976:
        move.w 0xf61c:w,%d0
m68k_00e976_end:
.org 0xE97A
m68k_00e97a:
        move.l %d0,%d1
m68k_00e97a_end:
.org 0xE97C
m68k_00e97c:
        lsl.l #0x1,%d0
m68k_00e97c_end:
.org 0xE97E
m68k_00e97e:
        add.l %d1,%d0
m68k_00e97e_end:
.org 0xE980
m68k_00e980:
        lsl.l #0x1,%d0
m68k_00e980_end:
.org 0xE982
m68k_00e982:
        swap %d0
m68k_00e982_end:
.org 0xE984
m68k_00e984:
        addq.w #0x5,%d0
m68k_00e984_end:
.org 0xE986
m68k_00e986:
        move.w 0xf376:w,%d1
m68k_00e986_end:
.org 0xE98A
m68k_00e98a:
        lsl.w #0x1,%d1
m68k_00e98a_end:
.org 0xE98C
m68k_00e98c:
        lea.l 0xe640:w,%a0
m68k_00e98c_end:
.org 0xE990
m68k_00e990:
        move.w (%a0, %d1.w),%d1
m68k_00e990_end:
.org 0xE994
m68k_00e994:
        lsl.w #0x1,%d1
m68k_00e994_end:
.org 0xE996
m68k_00e996:
        lea.l 0xbe00:w,%a0
m68k_00e996_end:
.org 0xE99A
m68k_00e99a:
        add.w (%a0, %d1.w),%d0
m68k_00e99a_end:
.org 0xE99E
m68k_00e99e:
        cmpi.w #0x3e7,%d0
m68k_00e99e_end:
.org 0xE9A2
m68k_00e9a2:
        bls.w (. + 8)
m68k_00e9a2_end:
.org 0xE9A6
m68k_00e9a6:
        move.w #0x3e7,%d0
m68k_00e9a6_end:
.org 0xE9AA
m68k_00e9aa:
        move.w %d0,(%a0, %d1.w)
m68k_00e9aa_end:
.org 0xE9AE
m68k_00e9ae:
        bra.w (. + 114)
m68k_00e9ae_end:
.org 0xE9B2
m68k_00e9b2:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00e9b2_end:
.org 0xE9B8
m68k_00e9b8:
        move.w #0x29,0xf3fe:w
m68k_00e9b8_end:
.org 0xE9BE
m68k_00e9be:
        jsr 0x83d4:l
m68k_00e9be_end:
.org 0xE9C4
m68k_00e9c4:
        moveq #0,%d2
m68k_00e9c4_end:
.org 0xE9C6
m68k_00e9c6:
        move.w 0xf61c:w,%d2
m68k_00e9c6_end:
.org 0xE9CA
m68k_00e9ca:
        move.l %d2,%d1
m68k_00e9ca_end:
.org 0xE9CC
m68k_00e9cc:
        lsl.l #0x1,%d2
m68k_00e9cc_end:
.org 0xE9CE
m68k_00e9ce:
        add.l %d1,%d2
m68k_00e9ce_end:
.org 0xE9D0
m68k_00e9d0:
        swap %d2
m68k_00e9d0_end:
.org 0xE9D2
m68k_00e9d2:
        addq.w #0x1,%d2
m68k_00e9d2_end:
.org 0xE9D4
m68k_00e9d4:
        jsr 0x83d4:l
m68k_00e9d4_end:
.org 0xE9DA
m68k_00e9da:
        andi.l #0xffff,%d0
m68k_00e9da_end:
.org 0xE9E0
m68k_00e9e0:
        move.l %d0,%d1
m68k_00e9e0_end:
.org 0xE9E2
m68k_00e9e2:
        lsl.l #0x1,%d0
m68k_00e9e2_end:
.org 0xE9E4
m68k_00e9e4:
        add.l %d1,%d0
m68k_00e9e4_end:
.org 0xE9E6
m68k_00e9e6:
        swap %d0
m68k_00e9e6_end:
.org 0xE9E8
m68k_00e9e8:
        move.w 0xf376:w,%d1
m68k_00e9e8_end:
.org 0xE9EC
m68k_00e9ec:
        lsl.w #0x1,%d1
m68k_00e9ec_end:
.org 0xE9EE
m68k_00e9ee:
        lea.l 0xe640:w,%a0
m68k_00e9ee_end:
.org 0xE9F2
m68k_00e9f2:
        move.w (%a0, %d1.w),%d1
m68k_00e9f2_end:
.org 0xE9F6
m68k_00e9f6:
        lea.l 0xc200:w,%a0
m68k_00e9f6_end:
.org 0xE9FA
m68k_00e9fa:
        sub.b %d0,(%a0, %d1.w)
m68k_00e9fa_end:
.org 0xE9FE
m68k_00e9fe:
        bcc.w (. + 8)
m68k_00e9fe_end:
.org 0xEA02
m68k_00ea02:
        clr.b (%a0, %d1.w)
m68k_00ea02_end:
.org 0xEA06
m68k_00ea06:
        lsl.w #0x1,%d1
m68k_00ea06_end:
.org 0xEA08
m68k_00ea08:
        lea.l 0xbe00:w,%a0
m68k_00ea08_end:
.org 0xEA0C
m68k_00ea0c:
        add.w (%a0, %d1.w),%d2
m68k_00ea0c_end:
.org 0xEA10
m68k_00ea10:
        cmpi.w #0x3e7,%d2
m68k_00ea10_end:
.org 0xEA14
m68k_00ea14:
        bls.w (. + 8)
m68k_00ea14_end:
.org 0xEA18
m68k_00ea18:
        move.w #0x3e7,%d2
m68k_00ea18_end:
.org 0xEA1C
m68k_00ea1c:
        move.w %d2,(%a0, %d1.w)
m68k_00ea1c_end:
.org 0xEA20
m68k_00ea20:
        move.w #0xe,0xff7026:l
m68k_00ea20_end:
.org 0xEA28
m68k_00ea28:
        move.w #0x208,0xf38a:w
m68k_00ea28_end:
.org 0xEA2E
m68k_00ea2e:
        move.w #0x28,0xf362:w
m68k_00ea2e_end:
.org 0xEA34
m68k_00ea34:
        bra.w (. + 474)
m68k_00ea34_end:
.org 0xEA38
m68k_00ea38:
        move.w 0xf3a6:w,%d0
m68k_00ea38_end:
.org 0xEA3C
m68k_00ea3c:
        lea.l 0xc700:w,%a0
m68k_00ea3c_end:
.org 0xEA40
m68k_00ea40:
        move.b (%a0, %d0.w),%d1
m68k_00ea40_end:
.org 0xEA44
m68k_00ea44:
        andi.b #0x7,%d1
m68k_00ea44_end:
.org 0xEA48
m68k_00ea48:
        ext.w %d1
m68k_00ea48_end:
.org 0xEA4A
m68k_00ea4a:
        move.w %d1,%d3
m68k_00ea4a_end:
.org 0xEA4C
m68k_00ea4c:
        addq.w #0x2,%d3
m68k_00ea4c_end:
.org 0xEA4E
m68k_00ea4e:
        lea.l 524(%pc),%a0
m68k_00ea4e_end:
.org 0xEA52
m68k_00ea52:
        nop
m68k_00ea52_end:
.org 0xEA54
m68k_00ea54:
        move.b (%a0, %d1.w),%d2
m68k_00ea54_end:
.org 0xEA58
m68k_00ea58:
        ext.w %d2
m68k_00ea58_end:
.org 0xEA5A
m68k_00ea5a:
        moveq #0,%d1
m68k_00ea5a_end:
.org 0xEA5C
m68k_00ea5c:
        move.w 0xf61c:w,%d1
m68k_00ea5c_end:
.org 0xEA60
m68k_00ea60:
        mulu.w %d3,%d1
m68k_00ea60_end:
.org 0xEA62
m68k_00ea62:
        swap %d1
m68k_00ea62_end:
.org 0xEA64
m68k_00ea64:
        add.w %d2,%d1
m68k_00ea64_end:
.org 0xEA66
m68k_00ea66:
        lsl.w #0x1,%d0
m68k_00ea66_end:
.org 0xEA68
m68k_00ea68:
        lea.l 0xb600:w,%a0
m68k_00ea68_end:
.org 0xEA6C
m68k_00ea6c:
        move.w (%a0, %d0.w),%d2
m68k_00ea6c_end:
.org 0xEA70
m68k_00ea70:
        mulu.w %d2,%d1
m68k_00ea70_end:
.org 0xEA72
m68k_00ea72:
        move.w 0xf376:w,%d0
m68k_00ea72_end:
.org 0xEA76
m68k_00ea76:
        lsl.w #0x1,%d0
m68k_00ea76_end:
.org 0xEA78
m68k_00ea78:
        lea.l 0xe640:w,%a0
m68k_00ea78_end:
.org 0xEA7C
m68k_00ea7c:
        move.w (%a0, %d0.w),%d2
m68k_00ea7c_end:
.org 0xEA80
m68k_00ea80:
        lea.l 0xc200:w,%a0
m68k_00ea80_end:
.org 0xEA84
m68k_00ea84:
        clr.w %d3
m68k_00ea84_end:
.org 0xEA86
m68k_00ea86:
        move.b (%a0, %d2.w),%d3
m68k_00ea86_end:
.org 0xEA8A
m68k_00ea8a:
        move.w #0x78,%d2
m68k_00ea8a_end:
.org 0xEA8E
m68k_00ea8e:
        sub.w %d3,%d2
m68k_00ea8e_end:
.org 0xEA90
m68k_00ea90:
        divu.w %d2,%d1
m68k_00ea90_end:
.org 0xEA92
m68k_00ea92:
        cmpi.w #0xa,%d1
m68k_00ea92_end:
.org 0xEA96
m68k_00ea96:
        bcs.w (. + 144)
m68k_00ea96_end:
.org 0xEA9A
m68k_00ea9a:
        bsr.w (. + 380)
m68k_00ea9a_end:
.org 0xEA9E
m68k_00ea9e:
        move.w #0x26,0xf3fe:w
m68k_00ea9e_end:
.org 0xEAA4
m68k_00eaa4:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00eaa4_end:
.org 0xEAAA
m68k_00eaaa:
        jsr 0x83d4:l
m68k_00eaaa_end:
.org 0xEAB0
m68k_00eab0:
        moveq #0,%d0
m68k_00eab0_end:
.org 0xEAB2
m68k_00eab2:
        move.w 0xf61c:w,%d0
m68k_00eab2_end:
.org 0xEAB6
m68k_00eab6:
        move.l %d0,%d1
m68k_00eab6_end:
.org 0xEAB8
m68k_00eab8:
        lsl.l #0x1,%d0
m68k_00eab8_end:
.org 0xEABA
m68k_00eaba:
        add.l %d1,%d0
m68k_00eaba_end:
.org 0xEABC
m68k_00eabc:
        lsl.l #0x1,%d0
m68k_00eabc_end:
.org 0xEABE
m68k_00eabe:
        swap %d0
m68k_00eabe_end:
.org 0xEAC0
m68k_00eac0:
        addq.w #0x5,%d0
m68k_00eac0_end:
.org 0xEAC2
m68k_00eac2:
        move.w 0xf376:w,%d1
m68k_00eac2_end:
.org 0xEAC6
m68k_00eac6:
        lsl.w #0x1,%d1
m68k_00eac6_end:
.org 0xEAC8
m68k_00eac8:
        lea.l 0xe640:w,%a0
m68k_00eac8_end:
.org 0xEACC
m68k_00eacc:
        move.w (%a0, %d1.w),%d2
m68k_00eacc_end:
.org 0xEAD0
m68k_00ead0:
        lsl.w #0x1,%d2
m68k_00ead0_end:
.org 0xEAD2
m68k_00ead2:
        lea.l 0xbe00:w,%a0
m68k_00ead2_end:
.org 0xEAD6
m68k_00ead6:
        add.w (%a0, %d2.w),%d0
m68k_00ead6_end:
.org 0xEADA
m68k_00eada:
        cmpi.w #0x3e7,%d0
m68k_00eada_end:
.org 0xEADE
m68k_00eade:
        bls.w (. + 8)
m68k_00eade_end:
.org 0xEAE2
m68k_00eae2:
        move.w #0x3e7,%d0
m68k_00eae2_end:
.org 0xEAE6
m68k_00eae6:
        move.w %d0,(%a0, %d2.w)
m68k_00eae6_end:
.org 0xEAEA
m68k_00eaea:
        jsr 0x83d4:l
m68k_00eaea_end:
.org 0xEAF0
m68k_00eaf0:
        moveq #0,%d0
m68k_00eaf0_end:
.org 0xEAF2
m68k_00eaf2:
        move.w 0xf61c:w,%d0
m68k_00eaf2_end:
.org 0xEAF6
m68k_00eaf6:
        move.l %d0,%d1
m68k_00eaf6_end:
.org 0xEAF8
m68k_00eaf8:
        lsl.l #0x1,%d0
m68k_00eaf8_end:
.org 0xEAFA
m68k_00eafa:
        add.l %d1,%d0
m68k_00eafa_end:
.org 0xEAFC
m68k_00eafc:
        lsl.l #0x1,%d0
m68k_00eafc_end:
.org 0xEAFE
m68k_00eafe:
        swap %d0
m68k_00eafe_end:
.org 0xEB00
m68k_00eb00:
        addi.w #0xa,%d0
m68k_00eb00_end:
.org 0xEB04
m68k_00eb04:
        move.w 0xf3a6:w,%d2
m68k_00eb04_end:
.org 0xEB08
m68k_00eb08:
        lsl.w #0x1,%d2
m68k_00eb08_end:
.org 0xEB0A
m68k_00eb0a:
        lea.l 0xbe00:w,%a0
m68k_00eb0a_end:
.org 0xEB0E
m68k_00eb0e:
        add.w (%a0, %d2.w),%d0
m68k_00eb0e_end:
.org 0xEB12
m68k_00eb12:
        cmpi.w #0x3e7,%d0
m68k_00eb12_end:
.org 0xEB16
m68k_00eb16:
        bls.w (. + 8)
m68k_00eb16_end:
.org 0xEB1A
m68k_00eb1a:
        move.w #0x3e7,%d0
m68k_00eb1a_end:
.org 0xEB1E
m68k_00eb1e:
        move.w %d0,(%a0, %d2.w)
m68k_00eb1e_end:
.org 0xEB22
m68k_00eb22:
        bra.w (. + 158)
m68k_00eb22_end:
.org 0xEB26
m68k_00eb26:
        move.w #0x28,0xf3fe:w
m68k_00eb26_end:
.org 0xEB2C
m68k_00eb2c:
        jsr 0x83d4:l
m68k_00eb2c_end:
.org 0xEB32
m68k_00eb32:
        moveq #0,%d2
m68k_00eb32_end:
.org 0xEB34
m68k_00eb34:
        move.w 0xf61c:w,%d2
m68k_00eb34_end:
.org 0xEB38
m68k_00eb38:
        move.l %d2,%d1
m68k_00eb38_end:
.org 0xEB3A
m68k_00eb3a:
        lsl.l #0x1,%d2
m68k_00eb3a_end:
.org 0xEB3C
m68k_00eb3c:
        add.l %d1,%d2
m68k_00eb3c_end:
.org 0xEB3E
m68k_00eb3e:
        swap %d2
m68k_00eb3e_end:
.org 0xEB40
m68k_00eb40:
        addq.w #0x1,%d2
m68k_00eb40_end:
.org 0xEB42
m68k_00eb42:
        move.w 0xf376:w,%d1
m68k_00eb42_end:
.org 0xEB46
m68k_00eb46:
        lsl.w #0x1,%d1
m68k_00eb46_end:
.org 0xEB48
m68k_00eb48:
        lea.l 0xe640:w,%a0
m68k_00eb48_end:
.org 0xEB4C
m68k_00eb4c:
        move.w (%a0, %d1.w),%d0
m68k_00eb4c_end:
.org 0xEB50
m68k_00eb50:
        lsl.w #0x1,%d0
m68k_00eb50_end:
.org 0xEB52
m68k_00eb52:
        lea.l 0xbe00:w,%a0
m68k_00eb52_end:
.org 0xEB56
m68k_00eb56:
        add.w (%a0, %d0.w),%d2
m68k_00eb56_end:
.org 0xEB5A
m68k_00eb5a:
        cmpi.w #0x3e7,%d2
m68k_00eb5a_end:
.org 0xEB5E
m68k_00eb5e:
        bls.w (. + 8)
m68k_00eb5e_end:
.org 0xEB62
m68k_00eb62:
        move.w #0x3e7,%d2
m68k_00eb62_end:
.org 0xEB66
m68k_00eb66:
        move.w %d2,(%a0, %d0.w)
m68k_00eb66_end:
.org 0xEB6A
m68k_00eb6a:
        jsr 0x83d4:l
m68k_00eb6a_end:
.org 0xEB70
m68k_00eb70:
        moveq #0,%d2
m68k_00eb70_end:
.org 0xEB72
m68k_00eb72:
        move.w 0xf61c:w,%d2
m68k_00eb72_end:
.org 0xEB76
m68k_00eb76:
        move.l %d2,%d1
m68k_00eb76_end:
.org 0xEB78
m68k_00eb78:
        lsl.l #0x1,%d2
m68k_00eb78_end:
.org 0xEB7A
m68k_00eb7a:
        add.l %d1,%d2
m68k_00eb7a_end:
.org 0xEB7C
m68k_00eb7c:
        swap %d2
m68k_00eb7c_end:
.org 0xEB7E
m68k_00eb7e:
        addq.w #0x1,%d2
m68k_00eb7e_end:
.org 0xEB80
m68k_00eb80:
        jsr 0x83d4:l
m68k_00eb80_end:
.org 0xEB86
m68k_00eb86:
        moveq #0,%d3
m68k_00eb86_end:
.org 0xEB88
m68k_00eb88:
        move.w 0xf61c:w,%d3
m68k_00eb88_end:
.org 0xEB8C
m68k_00eb8c:
        move.l %d3,%d1
m68k_00eb8c_end:
.org 0xEB8E
m68k_00eb8e:
        lsl.l #0x1,%d3
m68k_00eb8e_end:
.org 0xEB90
m68k_00eb90:
        add.l %d1,%d3
m68k_00eb90_end:
.org 0xEB92
m68k_00eb92:
        swap %d3
m68k_00eb92_end:
.org 0xEB94
m68k_00eb94:
        move.w 0xf3a6:w,%d1
m68k_00eb94_end:
.org 0xEB98
m68k_00eb98:
        lea.l 0xc200:w,%a0
m68k_00eb98_end:
.org 0xEB9C
m68k_00eb9c:
        sub.b %d3,(%a0, %d1.w)
m68k_00eb9c_end:
.org 0xEBA0
m68k_00eba0:
        bcc.b (. + 6)
m68k_00eba0_end:
.org 0xEBA2
m68k_00eba2:
        clr.b (%a0, %d1.w)
m68k_00eba2_end:
.org 0xEBA6
m68k_00eba6:
        lsl.w #0x1,%d1
m68k_00eba6_end:
.org 0xEBA8
m68k_00eba8:
        lea.l 0xbe00:w,%a0
m68k_00eba8_end:
.org 0xEBAC
m68k_00ebac:
        add.w (%a0, %d1.w),%d2
m68k_00ebac_end:
.org 0xEBB0
m68k_00ebb0:
        cmpi.w #0x3e7,%d2
m68k_00ebb0_end:
.org 0xEBB4
m68k_00ebb4:
        bls.w (. + 8)
m68k_00ebb4_end:
.org 0xEBB8
m68k_00ebb8:
        move.w #0x3e7,%d2
m68k_00ebb8_end:
.org 0xEBBC
m68k_00ebbc:
        move.w %d2,(%a0, %d1.w)
m68k_00ebbc_end:
.org 0xEBC0
m68k_00ebc0:
        move.w 0xf376:w,%d0
m68k_00ebc0_end:
.org 0xEBC4
m68k_00ebc4:
        cmp.w 0xf67a:w,%d0
m68k_00ebc4_end:
.org 0xEBC8
m68k_00ebc8:
        beq.w (. + 20)
m68k_00ebc8_end:
.org 0xEBCC
m68k_00ebcc:
        cmp.w 0xf67c:w,%d0
m68k_00ebcc_end:
.org 0xEBD0
m68k_00ebd0:
        beq.w (. + 12)
m68k_00ebd0_end:
.org 0xEBD4
m68k_00ebd4:
        cmp.w 0xf67e:w,%d0
m68k_00ebd4_end:
.org 0xEBD8
m68k_00ebd8:
        bne.w (. + 54)
m68k_00ebd8_end:
.org 0xEBDC
m68k_00ebdc:
        move.w #0xc,0xff7026:l
m68k_00ebdc_end:
.org 0xEBE4
m68k_00ebe4:
        move.w #0x208,0xf612:w
m68k_00ebe4_end:
.org 0xEBEA
m68k_00ebea:
        move.w #0x28,0xf362:w
m68k_00ebea_end:
.org 0xEBF0
m68k_00ebf0:
        move.w #0x25,%d0
m68k_00ebf0_end:
.org 0xEBF4
m68k_00ebf4:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00ebf4_end:
.org 0xEBFA
m68k_00ebfa:
        jsr 0x676f2:l
m68k_00ebfa_end:
.org 0xEC00
m68k_00ec00:
        move.w 0xf3a6:w,%d0
m68k_00ec00_end:
.org 0xEC04
m68k_00ec04:
        lea.l 0xcd00:w,%a0
m68k_00ec04_end:
.org 0xEC08
m68k_00ec08:
        move.b #0x1,(%a0, %d0.w)
m68k_00ec08_end:
.org 0xEC0E
m68k_00ec0e:
        move.w #0x78,0xf608:w
m68k_00ec0e_end:
.org 0xEC14
m68k_00ec14:
        rts
m68k_00ec14_end:
.org 0xEC16
m68k_00ec16:
        move.w 0xf3e0:w,%d0
m68k_00ec16_end:
.org 0xEC1A
m68k_00ec1a:
        lsl.w #0x1,%d0
m68k_00ec1a_end:
.org 0xEC1C
m68k_00ec1c:
        lea.l 0xe730:w,%a0
m68k_00ec1c_end:
.org 0xEC20
m68k_00ec20:
        move.w (%a0, %d0.w),%d1
m68k_00ec20_end:
.org 0xEC24
m68k_00ec24:
        move.w 0xf376:w,%d0
m68k_00ec24_end:
.org 0xEC28
m68k_00ec28:
        lsl.w #0x1,%d0
m68k_00ec28_end:
.org 0xEC2A
m68k_00ec2a:
        lea.l 0xe710:w,%a0
m68k_00ec2a_end:
.org 0xEC2E
m68k_00ec2e:
        move.w (%a0, %d0.w),%d2
m68k_00ec2e_end:
.org 0xEC32
m68k_00ec32:
        bset.l %d1,%d2
m68k_00ec32_end:
.org 0xEC34
m68k_00ec34:
        move.w %d2,(%a0, %d0.w)
m68k_00ec34_end:
.org 0xEC38
m68k_00ec38:
        move.w 0xf3e0:w,%d0
m68k_00ec38_end:
.org 0xEC3C
m68k_00ec3c:
        lsl.w #0x1,%d0
m68k_00ec3c_end:
.org 0xEC3E
m68k_00ec3e:
        lea.l 0xe730:w,%a0
m68k_00ec3e_end:
.org 0xEC42
m68k_00ec42:
        move.w (%a0, %d0.w),%d0
m68k_00ec42_end:
.org 0xEC46
m68k_00ec46:
        lsl.w #0x1,%d0
m68k_00ec46_end:
.org 0xEC48
m68k_00ec48:
        move.w 0xf376:w,%d1
m68k_00ec48_end:
.org 0xEC4C
m68k_00ec4c:
        lea.l 0xe710:w,%a0
m68k_00ec4c_end:
.org 0xEC50
m68k_00ec50:
        move.w (%a0, %d0.w),%d2
m68k_00ec50_end:
.org 0xEC54
m68k_00ec54:
        bset.l %d1,%d2
m68k_00ec54_end:
.org 0xEC56
m68k_00ec56:
        move.w %d2,(%a0, %d0.w)
m68k_00ec56_end:
.org 0xEC5A
m68k_00ec5a:
        rts
m68k_00ec5a_end:
.org 0xEC62
m68k_00ec62:
        cmpi.w #0x6a,0xf38c:w
m68k_00ec62_end:
.org 0xEC68
m68k_00ec68:
        beq.w (. + 202)
m68k_00ec68_end:
.org 0xEC6C
m68k_00ec6c:
        move.w 0xf392:w,%d0
m68k_00ec6c_end:
.org 0xEC70
m68k_00ec70:
        lsl.w #0x1,%d0
m68k_00ec70_end:
.org 0xEC72
m68k_00ec72:
        lea.l 0xf460:w,%a0
m68k_00ec72_end:
.org 0xEC76
m68k_00ec76:
        move.w (%a0, %d0.w),%d1
m68k_00ec76_end:
.org 0xEC7A
m68k_00ec7a:
        lea.l 0xc200:w,%a1
m68k_00ec7a_end:
.org 0xEC7E
m68k_00ec7e:
        move.b (%a1, %d1.w),%d2
m68k_00ec7e_end:
.org 0xEC82
m68k_00ec82:
        ext.w %d2
m68k_00ec82_end:
.org 0xEC84
m68k_00ec84:
        lsl.w #0x1,%d0
m68k_00ec84_end:
.org 0xEC86
m68k_00ec86:
        lea.l 0xdffc:w,%a0
m68k_00ec86_end:
.org 0xEC8A
m68k_00ec8a:
        move.l (%a0, %d0.w),%d1
m68k_00ec8a_end:
.org 0xEC8E
m68k_00ec8e:
        move.w %d1,%d3
m68k_00ec8e_end:
.org 0xEC90
m68k_00ec90:
        mulu.w %d2,%d3
m68k_00ec90_end:
.org 0xEC92
m68k_00ec92:
        swap %d1
m68k_00ec92_end:
.org 0xEC94
m68k_00ec94:
        mulu.w %d2,%d1
m68k_00ec94_end:
.org 0xEC96
m68k_00ec96:
        swap %d1
m68k_00ec96_end:
.org 0xEC98
m68k_00ec98:
        add.l %d3,%d1
m68k_00ec98_end:
.org 0xEC9A
m68k_00ec9a:
        moveq #0,%d0
m68k_00ec9a_end:
.org 0xEC9C
m68k_00ec9c:
        move.w 0xf61c:w,%d0
m68k_00ec9c_end:
.org 0xECA0
m68k_00eca0:
        move.l %d0,%d2
m68k_00eca0_end:
.org 0xECA2
m68k_00eca2:
        lsl.l #0x1,%d0
m68k_00eca2_end:
.org 0xECA4
m68k_00eca4:
        add.l %d2,%d0
m68k_00eca4_end:
.org 0xECA6
m68k_00eca6:
        lsl.l #0x1,%d0
m68k_00eca6_end:
.org 0xECA8
m68k_00eca8:
        swap %d0
m68k_00eca8_end:
.org 0xECAA
m68k_00ecaa:
        addq.w #0x7,%d0
m68k_00ecaa_end:
.org 0xECAC
m68k_00ecac:
        move.w %d1,%d2
m68k_00ecac_end:
.org 0xECAE
m68k_00ecae:
        mulu.w %d0,%d2
m68k_00ecae_end:
.org 0xECB0
m68k_00ecb0:
        swap %d1
m68k_00ecb0_end:
.org 0xECB2
m68k_00ecb2:
        mulu.w %d0,%d1
m68k_00ecb2_end:
.org 0xECB4
m68k_00ecb4:
        swap %d1
m68k_00ecb4_end:
.org 0xECB6
m68k_00ecb6:
        add.l %d2,%d1
m68k_00ecb6_end:
.org 0xECB8
m68k_00ecb8:
        move.l 0xf39e:w,%d0
m68k_00ecb8_end:
.org 0xECBC
m68k_00ecbc:
        move.w %d0,%d2
m68k_00ecbc_end:
.org 0xECBE
m68k_00ecbe:
        mulu.w #0xc8,%d2
m68k_00ecbe_end:
.org 0xECC2
m68k_00ecc2:
        swap %d0
m68k_00ecc2_end:
.org 0xECC4
m68k_00ecc4:
        mulu.w #0xc8,%d0
m68k_00ecc4_end:
.org 0xECC8
m68k_00ecc8:
        swap %d0
m68k_00ecc8_end:
.org 0xECCA
m68k_00ecca:
        add.l %d0,%d2
m68k_00ecca_end:
.org 0xECCC
m68k_00eccc:
        jsr 0x35760:l
m68k_00eccc_end:
.org 0xECD2
m68k_00ecd2:
        cmpi.w #0xa,%d1
m68k_00ecd2_end:
.org 0xECD6
m68k_00ecd6:
        bcs.b (. + 76)
m68k_00ecd6_end:
.org 0xECD8
m68k_00ecd8:
        move.w 0xf376:w,%d0
m68k_00ecd8_end:
.org 0xECDC
m68k_00ecdc:
        move.w 0xe700:w,%d1
m68k_00ecdc_end:
.org 0xECE0
m68k_00ece0:
        bset.l %d0,%d1
m68k_00ece0_end:
.org 0xECE2
m68k_00ece2:
        move.w %d1,0xe700:w
m68k_00ece2_end:
.org 0xECE6
m68k_00ece6:
        lsl.w #0x2,%d0
m68k_00ece6_end:
.org 0xECE8
m68k_00ece8:
        lea.l 0xe9f8:w,%a0
m68k_00ece8_end:
.org 0xECEC
m68k_00ecec:
        move.b 0xf393:w,(%a0, %d0.w)
m68k_00ecec_end:
.org 0xECF2
m68k_00ecf2:
        move.w 0xf392:w,%d0
m68k_00ecf2_end:
.org 0xECF6
m68k_00ecf6:
        lsl.w #0x2,%d0
m68k_00ecf6_end:
.org 0xECF8
m68k_00ecf8:
        lea.l 0xdffc:w,%a0
m68k_00ecf8_end:
.org 0xECFC
m68k_00ecfc:
        move.l (%a0, %d0.w),%d1
m68k_00ecfc_end:
.org 0xED00
m68k_00ed00:
        sub.l 0xf39e:w,%d1
m68k_00ed00_end:
.org 0xED04
m68k_00ed04:
        move.l %d1,(%a0, %d0.w)
m68k_00ed04_end:
.org 0xED08
m68k_00ed08:
        move.w #0x10,0xff7026:l
m68k_00ed08_end:
.org 0xED10
m68k_00ed10:
        bsr.w (. + 6684)
m68k_00ed10_end:
.org 0xED14
m68k_00ed14:
        move.w #0x2f,0xf740:w
m68k_00ed14_end:
.org 0xED1A
m68k_00ed1a:
        clr.w 0xf386:w
m68k_00ed1a_end:
.org 0xED1E
m68k_00ed1e:
        bra.w (. + 154)
m68k_00ed1e_end:
.org 0xED22
m68k_00ed22:
        move.w #0x1,0xf386:w
m68k_00ed22_end:
.org 0xED28
m68k_00ed28:
        move.w #0x2e,0xf740:w
m68k_00ed28_end:
.org 0xED2E
m68k_00ed2e:
        bra.w (. + 138)
m68k_00ed2e_end:
.org 0xED32
m68k_00ed32:
        move.w 0xf576:w,%d0
m68k_00ed32_end:
.org 0xED36
m68k_00ed36:
        lea.l 0xf578:w,%a0
m68k_00ed36_end:
.org 0xED3A
m68k_00ed3a:
        cmpi.b #0x3f,-0x2(%a0, %d0.w)
m68k_00ed3a_end:
.org 0xED40
m68k_00ed40:
        beq.b (. + 100)
m68k_00ed40_end:
.org 0xED42
m68k_00ed42:
        move.w 0xf376:w,%d0
m68k_00ed42_end:
.org 0xED46
m68k_00ed46:
        lsl.w #0x2,%d0
m68k_00ed46_end:
.org 0xED48
m68k_00ed48:
        lea.l 0xe9f8:w,%a0
m68k_00ed48_end:
.org 0xED4C
m68k_00ed4c:
        move.b 0xf393:w,0x1(%a0, %d0.w)
m68k_00ed4c_end:
.org 0xED52
m68k_00ed52:
        move.w 0xf374:w,0x2(%a0, %d0.w)
m68k_00ed52_end:
.org 0xED58
m68k_00ed58:
        move.w 0xf392:w,%d0
m68k_00ed58_end:
.org 0xED5C
m68k_00ed5c:
        lsl.w #0x2,%d0
m68k_00ed5c_end:
.org 0xED5E
m68k_00ed5e:
        lea.l 0xdffc:w,%a0
m68k_00ed5e_end:
.org 0xED62
m68k_00ed62:
        move.l (%a0, %d0.w),%d1
m68k_00ed62_end:
.org 0xED66
m68k_00ed66:
        add.l 0xf39e:w,%d1
m68k_00ed66_end:
.org 0xED6A
m68k_00ed6a:
        cmpi.l #0xf423f,%d1
m68k_00ed6a_end:
.org 0xED70
m68k_00ed70:
        bls.b (. + 8)
m68k_00ed70_end:
.org 0xED72
m68k_00ed72:
        move.l #0xf423f,%d1
m68k_00ed72_end:
.org 0xED78
m68k_00ed78:
        move.l %d1,(%a0, %d0.w)
m68k_00ed78_end:
.org 0xED7C
m68k_00ed7c:
        lea.l 0xe65c:w,%a0
m68k_00ed7c_end:
.org 0xED80
m68k_00ed80:
        move.l 0xf39e:w,(%a0, %d0.w)
m68k_00ed80_end:
.org 0xED86
m68k_00ed86:
        move.w #0x20,0xf362:w
m68k_00ed86_end:
.org 0xED8C
m68k_00ed8c:
        move.w #0x208,0xf612:w
m68k_00ed8c_end:
.org 0xED92
m68k_00ed92:
        move.w #0x31,%d0
m68k_00ed92_end:
.org 0xED96
m68k_00ed96:
        move.w 0xf392:w,0xf646:w
m68k_00ed96_end:
.org 0xED9C
m68k_00ed9c:
        jsr 0x676f2:l
m68k_00ed9c_end:
.org 0xEDA2
m68k_00eda2:
        bra.b (. + 48)
m68k_00eda2_end:
.org 0xEDA4
m68k_00eda4:
        move.w #0x3,0xf362:w
m68k_00eda4_end:
.org 0xEDAA
m68k_00edaa:
        move.w #0x208,0xf38a:w
m68k_00edaa_end:
.org 0xEDB0
m68k_00edb0:
        clr.w 0xf36a:w
m68k_00edb0_end:
.org 0xEDB4
m68k_00edb4:
        bra.w (. + 30)
m68k_00edb4_end:
.org 0xEDB8
m68k_00edb8:
        move.w #0x21,0xf362:w
m68k_00edb8_end:
.org 0xEDBE
m68k_00edbe:
        move.w #0x208,0xf612:w
m68k_00edbe_end:
.org 0xEDC4
m68k_00edc4:
        clr.w 0xf384:w
m68k_00edc4_end:
.org 0xEDC8
m68k_00edc8:
        move.w 0xf740:w,%d0
m68k_00edc8_end:
.org 0xEDCC
m68k_00edcc:
        jsr 0x676f2:l
m68k_00edcc_end:
.org 0xEDD2
m68k_00edd2:
        rts
m68k_00edd2_end:
.org 0xEDD4
m68k_00edd4:
        rts
m68k_00edd4_end:
.org 0xEDD6
m68k_00edd6:
        move.w 0xf3a6:w,%d0
m68k_00edd6_end:
.org 0xEDDA
m68k_00edda:
        lea.l 0xcd00:w,%a0
m68k_00edda_end:
.org 0xEDDE
m68k_00edde:
        move.b #0x1,(%a0, %d0.w)
m68k_00edde_end:
.org 0xEDE4
m68k_00ede4:
        move.b 0xf57a:w,%d0
m68k_00ede4_end:
.org 0xEDE8
m68k_00ede8:
        cmpi.b #0x5c,%d0
m68k_00ede8_end:
.org 0xEDEC
m68k_00edec:
        bne.b (. + 14)
m68k_00edec_end:
.org 0xEDEE
m68k_00edee:
        bsr.w (. + 40)
m68k_00edee_end:
.org 0xEDF2
m68k_00edf2:
        clr.w 0xff7026:l
m68k_00edf2_end:
.org 0xEDF8
m68k_00edf8:
        bra.b (. + 18)
m68k_00edf8_end:
.org 0xEDFA
m68k_00edfa:
        cmpi.b #0x61,%d0
m68k_00edfa_end:
.org 0xEDFE
m68k_00edfe:
        bne.b (. + 8)
m68k_00edfe_end:
.org 0xEE00
m68k_00ee00:
        bsr.w (. + 536)
m68k_00ee00_end:
.org 0xEE04
m68k_00ee04:
        bra.b (. + 6)
m68k_00ee04_end:
.org 0xEE06
m68k_00ee06:
        bsr.w (. + 2418)
m68k_00ee06_end:
.org 0xEE0A
m68k_00ee0a:
        rts
m68k_00ee0a_end:
.org 0xEE16
m68k_00ee16:
        clr.l 0xf3c8:w
m68k_00ee16_end:
.org 0xEE1A
m68k_00ee1a:
        lea.l 0xcc00:w,%a0
m68k_00ee1a_end:
.org 0xEE1E
m68k_00ee1e:
        move.w 0xf3f2:w,%d0
m68k_00ee1e_end:
.org 0xEE22
m68k_00ee22:
        move.b (%a0, %d0.w),%d0
m68k_00ee22_end:
.org 0xEE26
m68k_00ee26:
        lea.l 0xf427:w,%a0
m68k_00ee26_end:
.org 0xEE2A
m68k_00ee2a:
        move.b (%a0, %d0.w),%d0
m68k_00ee2a_end:
.org 0xEE2E
m68k_00ee2e:
        lea.l 0xe640:w,%a0
m68k_00ee2e_end:
.org 0xEE32
m68k_00ee32:
        lsl.w #0x1,%d0
m68k_00ee32_end:
.org 0xEE34
m68k_00ee34:
        move.w (%a0, %d0.w),%d0
m68k_00ee34_end:
.org 0xEE38
m68k_00ee38:
        cmp.w 0xf3f2:w,%d0
m68k_00ee38_end:
.org 0xEE3C
m68k_00ee3c:
        beq.w (. + 204)
m68k_00ee3c_end:
.org 0xEE40
m68k_00ee40:
        move.w 0xf3f2:w,%d0
m68k_00ee40_end:
.org 0xEE44
m68k_00ee44:
        lea.l 0xc300:w,%a0
m68k_00ee44_end:
.org 0xEE48
m68k_00ee48:
        move.b (%a0, %d0.w),%d1
m68k_00ee48_end:
.org 0xEE4C
m68k_00ee4c:
        beq.w (. + 188)
m68k_00ee4c_end:
.org 0xEE50
m68k_00ee50:
        ext.w %d1
m68k_00ee50_end:
.org 0xEE52
m68k_00ee52:
        subi.w #0x32,%d1
m68k_00ee52_end:
.org 0xEE56
m68k_00ee56:
        bcc.b (. + 4)
m68k_00ee56_end:
.org 0xEE58
m68k_00ee58:
        neg.w %d1
m68k_00ee58_end:
.org 0xEE5A
m68k_00ee5a:
        move.w #0x3c,%d2
m68k_00ee5a_end:
.org 0xEE5E
m68k_00ee5e:
        sub.w %d1,%d2
m68k_00ee5e_end:
.org 0xEE60
m68k_00ee60:
        move.w 0xf3a6:w,%d1
m68k_00ee60_end:
.org 0xEE64
m68k_00ee64:
        lea.l 0xc700:w,%a1
m68k_00ee64_end:
.org 0xEE68
m68k_00ee68:
        move.b (%a1, %d1.w),%d3
m68k_00ee68_end:
.org 0xEE6C
m68k_00ee6c:
        andi.w #0x7,%d3
m68k_00ee6c_end:
.org 0xEE70
m68k_00ee70:
        move.b -97(%pc, %d3.w),%d3
m68k_00ee70_end:
.org 0xEE74
m68k_00ee74:
        moveq #0,%d4
m68k_00ee74_end:
.org 0xEE76
m68k_00ee76:
        move.w 0xf61c:w,%d4
m68k_00ee76_end:
.org 0xEE7A
m68k_00ee7a:
        move.l %d4,%d5
m68k_00ee7a_end:
.org 0xEE7C
m68k_00ee7c:
        lsl.l #0x2,%d4
m68k_00ee7c_end:
.org 0xEE7E
m68k_00ee7e:
        add.l %d5,%d4
m68k_00ee7e_end:
.org 0xEE80
m68k_00ee80:
        lsl.l #0x2,%d4
m68k_00ee80_end:
.org 0xEE82
m68k_00ee82:
        swap %d4
m68k_00ee82_end:
.org 0xEE84
m68k_00ee84:
        add.w %d3,%d4
m68k_00ee84_end:
.org 0xEE86
m68k_00ee86:
        lsl.w #0x1,%d1
m68k_00ee86_end:
.org 0xEE88
m68k_00ee88:
        lea.l 0xb600:w,%a0
m68k_00ee88_end:
.org 0xEE8C
m68k_00ee8c:
        move.w (%a0, %d1.w),%d3
m68k_00ee8c_end:
.org 0xEE90
m68k_00ee90:
        add.w %d4,%d3
m68k_00ee90_end:
.org 0xEE92
m68k_00ee92:
        move.w 0xf3f2:w,%d0
m68k_00ee92_end:
.org 0xEE96
m68k_00ee96:
        lea.l 0xc700:w,%a0
m68k_00ee96_end:
.org 0xEE9A
m68k_00ee9a:
        move.b (%a0, %d0.w),%d1
m68k_00ee9a_end:
.org 0xEE9E
m68k_00ee9e:
        andi.w #0x7,%d1
m68k_00ee9e_end:
.org 0xEEA2
m68k_00eea2:
        lea.l -152(%pc),%a1
m68k_00eea2_end:
.org 0xEEA6
m68k_00eea6:
        move.b (%a1, %d1.w),%d4
m68k_00eea6_end:
.org 0xEEAA
m68k_00eeaa:
        lsl.w #0x1,%d0
m68k_00eeaa_end:
.org 0xEEAC
m68k_00eeac:
        lea.l 0xb600:w,%a1
m68k_00eeac_end:
.org 0xEEB0
m68k_00eeb0:
        add.w (%a1, %d0.w),%d4
m68k_00eeb0_end:
.org 0xEEB4
m68k_00eeb4:
        sub.w %d4,%d3
m68k_00eeb4_end:
.org 0xEEB6
m68k_00eeb6:
        bcs.w (. + 82)
m68k_00eeb6_end:
.org 0xEEBA
m68k_00eeba:
        muls.w %d3,%d2
m68k_00eeba_end:
.org 0xEEBC
m68k_00eebc:
        lea.l -4022(%pc),%a1
m68k_00eebc_end:
.org 0xEEC0
m68k_00eec0:
        move.w 0xefd2:w,%d3
m68k_00eec0_end:
.org 0xEEC4
m68k_00eec4:
        lsl.w #0x1,%d3
m68k_00eec4_end:
.org 0xEEC6
m68k_00eec6:
        divu.w (%a1, %d3.w),%d2
m68k_00eec6_end:
.org 0xEECA
m68k_00eeca:
        tst.w %d2
m68k_00eeca_end:
.org 0xEECC
m68k_00eecc:
        beq.w (. + 60)
m68k_00eecc_end:
.org 0xEED0
m68k_00eed0:
        cmpi.w #0x28,%d2
m68k_00eed0_end:
.org 0xEED4
m68k_00eed4:
        bls.b (. + 6)
m68k_00eed4_end:
.org 0xEED6
m68k_00eed6:
        move.w #0x28,%d2
m68k_00eed6_end:
.org 0xEEDA
m68k_00eeda:
        clr.w 0xf3c8:w
m68k_00eeda_end:
.org 0xEEDE
m68k_00eede:
        move.w %d2,0xf3ca:w
m68k_00eede_end:
.org 0xEEE2
m68k_00eee2:
        move.w 0xf3f2:w,%d0
m68k_00eee2_end:
.org 0xEEE6
m68k_00eee6:
        lea.l 0xc300:w,%a0
m68k_00eee6_end:
.org 0xEEEA
m68k_00eeea:
        sub.b %d2,(%a0, %d0.w)
m68k_00eeea_end:
.org 0xEEEE
m68k_00eeee:
        bcc.b (. + 6)
m68k_00eeee_end:
.org 0xEEF0
m68k_00eef0:
        clr.b (%a0, %d0.w)
m68k_00eef0_end:
.org 0xEEF4
m68k_00eef4:
        bsr.w (. + 108)
m68k_00eef4_end:
.org 0xEEF8
m68k_00eef8:
        move.w 0xf3f2:w,0xf3d2:w
m68k_00eef8_end:
.org 0xEEFE
m68k_00eefe:
        move.w #0x39,0xf3fe:w
m68k_00eefe_end:
.org 0xEF04
m68k_00ef04:
        bra.w (. + 22)
m68k_00ef04_end:
.org 0xEF08
m68k_00ef08:
        bsr.w (. + 120)
m68k_00ef08_end:
.org 0xEF0C
m68k_00ef0c:
        bsr.w (. + 152)
m68k_00ef0c_end:
.org 0xEF10
m68k_00ef10:
        bsr.w (. + 210)
m68k_00ef10_end:
.org 0xEF14
m68k_00ef14:
        move.w #0x3a,0xf3fe:w
m68k_00ef14_end:
.org 0xEF1A
m68k_00ef1a:
        move.w 0xf376:w,%d0
m68k_00ef1a_end:
.org 0xEF1E
m68k_00ef1e:
        cmp.w 0xf67a:w,%d0
m68k_00ef1e_end:
.org 0xEF22
m68k_00ef22:
        beq.w (. + 20)
m68k_00ef22_end:
.org 0xEF26
m68k_00ef26:
        cmp.w 0xf67c:w,%d0
m68k_00ef26_end:
.org 0xEF2A
m68k_00ef2a:
        beq.w (. + 12)
m68k_00ef2a_end:
.org 0xEF2E
m68k_00ef2e:
        cmp.w 0xf67e:w,%d0
m68k_00ef2e_end:
.org 0xEF32
m68k_00ef32:
        bne.w (. + 44)
m68k_00ef32_end:
.org 0xEF36
m68k_00ef36:
        move.w #0x208,0xf38a:w
m68k_00ef36_end:
.org 0xEF3C
m68k_00ef3c:
        move.w #0x28,0xf362:w
m68k_00ef3c_end:
.org 0xEF42
m68k_00ef42:
        move.w #0x78,0xf608:w
m68k_00ef42_end:
.org 0xEF48
m68k_00ef48:
        move.w #0x208,0xf612:w
m68k_00ef48_end:
.org 0xEF4E
m68k_00ef4e:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00ef4e_end:
.org 0xEF54
m68k_00ef54:
        move.w #0x9,%d0
m68k_00ef54_end:
.org 0xEF58
m68k_00ef58:
        jsr 0x676f2:l
m68k_00ef58_end:
.org 0xEF5E
m68k_00ef5e:
        rts
m68k_00ef5e_end:
.org 0xEF60
m68k_00ef60:
        move.w 0xf3a6:w,%d0
m68k_00ef60_end:
.org 0xEF64
m68k_00ef64:
        lsl.w #0x1,%d0
m68k_00ef64_end:
.org 0xEF66
m68k_00ef66:
        lea.l 0xbe00:w,%a0
m68k_00ef66_end:
.org 0xEF6A
m68k_00ef6a:
        add.w %d2,(%a0, %d0.w)
m68k_00ef6a_end:
.org 0xEF6E
m68k_00ef6e:
        cmpi.w #0x3e7,(%a0, %d0.w)
m68k_00ef6e_end:
.org 0xEF74
m68k_00ef74:
        bls.w (. + 10)
m68k_00ef74_end:
.org 0xEF78
m68k_00ef78:
        move.w #0x3e7,(%a0, %d0.w)
m68k_00ef78_end:
.org 0xEF7E
m68k_00ef7e:
        rts
m68k_00ef7e_end:
.org 0xEF80
m68k_00ef80:
        jsr 0x83d4:l
m68k_00ef80_end:
.org 0xEF86
m68k_00ef86:
        andi.l #0xffff,%d0
m68k_00ef86_end:
.org 0xEF8C
m68k_00ef8c:
        lsl.l #0x2,%d0
m68k_00ef8c_end:
.org 0xEF8E
m68k_00ef8e:
        swap %d0
m68k_00ef8e_end:
.org 0xEF90
m68k_00ef90:
        move.w 0xf3a6:w,%d1
m68k_00ef90_end:
.org 0xEF94
m68k_00ef94:
        lea.l 0xc200:w,%a0
m68k_00ef94_end:
.org 0xEF98
m68k_00ef98:
        sub.b %d0,(%a0, %d1.w)
m68k_00ef98_end:
.org 0xEF9C
m68k_00ef9c:
        bcc.b (. + 6)
m68k_00ef9c_end:
.org 0xEF9E
m68k_00ef9e:
        clr.b (%a0, %d1.w)
m68k_00ef9e_end:
.org 0xEFA2
m68k_00efa2:
        rts
m68k_00efa2_end:
.org 0xEFA4
m68k_00efa4:
        jsr 0x83d4:l
m68k_00efa4_end:
.org 0xEFAA
m68k_00efaa:
        andi.l #0xffff,%d0
m68k_00efaa_end:
.org 0xEFB0
m68k_00efb0:
        move.l %d0,%d1
m68k_00efb0_end:
.org 0xEFB2
m68k_00efb2:
        lsl.l #0x1,%d0
m68k_00efb2_end:
.org 0xEFB4
m68k_00efb4:
        add.l %d1,%d0
m68k_00efb4_end:
.org 0xEFB6
m68k_00efb6:
        swap %d0
m68k_00efb6_end:
.org 0xEFB8
m68k_00efb8:
        move.w 0xf392:w,%d1
m68k_00efb8_end:
.org 0xEFBC
m68k_00efbc:
        lea.l 0xf427:w,%a0
m68k_00efbc_end:
.org 0xEFC0
m68k_00efc0:
        move.b (%a0, %d1.w),%d1
m68k_00efc0_end:
.org 0xEFC4
m68k_00efc4:
        andi.w #0xf,%d1
m68k_00efc4_end:
.org 0xEFC8
m68k_00efc8:
        lsl.w #0x1,%d1
m68k_00efc8_end:
.org 0xEFCA
m68k_00efca:
        lea.l 0xe640:w,%a0
m68k_00efca_end:
.org 0xEFCE
m68k_00efce:
        move.w (%a0, %d1.w),%d1
m68k_00efce_end:
.org 0xEFD2
m68k_00efd2:
        lea.l 0xc200:w,%a0
m68k_00efd2_end:
.org 0xEFD6
m68k_00efd6:
        sub.b %d0,(%a0, %d1.w)
m68k_00efd6_end:
.org 0xEFDA
m68k_00efda:
        bcc.b (. + 6)
m68k_00efda_end:
.org 0xEFDC
m68k_00efdc:
        clr.b (%a0, %d1.w)
m68k_00efdc_end:
.org 0xEFE0
m68k_00efe0:
        rts
m68k_00efe0_end:
.org 0xEFE2
m68k_00efe2:
        jsr 0x83d4:l
m68k_00efe2_end:
.org 0xEFE8
m68k_00efe8:
        moveq #0,%d0
m68k_00efe8_end:
.org 0xEFEA
m68k_00efea:
        move.w 0xf61c:w,%d0
m68k_00efea_end:
.org 0xEFEE
m68k_00efee:
        move.l %d0,%d1
m68k_00efee_end:
.org 0xEFF0
m68k_00eff0:
        lsl.l #0x1,%d0
m68k_00eff0_end:
.org 0xEFF2
m68k_00eff2:
        add.l %d1,%d0
m68k_00eff2_end:
.org 0xEFF4
m68k_00eff4:
        swap %d0
m68k_00eff4_end:
.org 0xEFF6
m68k_00eff6:
        addi.w #0x1,%d0
m68k_00eff6_end:
.org 0xEFFA
m68k_00effa:
        move.w 0xf3a6:w,%d1
m68k_00effa_end:
.org 0xEFFE
m68k_00effe:
        lsl.w #0x1,%d1
m68k_00effe_end:
.org 0xF000
m68k_00f000:
        lea.l 0xbe00:w,%a0
m68k_00f000_end:
.org 0xF004
m68k_00f004:
        add.w %d0,(%a0, %d1.w)
m68k_00f004_end:
.org 0xF008
m68k_00f008:
        cmpi.w #0x3e7,(%a0, %d1.w)
m68k_00f008_end:
.org 0xF00E
m68k_00f00e:
        bls.b (. + 8)
m68k_00f00e_end:
.org 0xF010
m68k_00f010:
        move.w #0x3e7,(%a0, %d1.w)
m68k_00f010_end:
.org 0xF016
m68k_00f016:
        rts
m68k_00f016_end:
.org 0xF018
m68k_00f018:
        bsr.w (. + 20)
m68k_00f018_end:
.org 0xF01C
m68k_00f01c:
        tst.w %d0
m68k_00f01c_end:
.org 0xF01E
m68k_00f01e:
        bne.b (. + 8)
m68k_00f01e_end:
.org 0xF020
m68k_00f020:
        bsr.w (. + 104)
m68k_00f020_end:
.org 0xF024
m68k_00f024:
        bra.b (. + 6)
m68k_00f024_end:
.org 0xF026
m68k_00f026:
        bsr.w (. + 360)
m68k_00f026_end:
.org 0xF02A
m68k_00f02a:
        rts
m68k_00f02a_end:
.org 0xF02C
m68k_00f02c:
        move.w 0xf3a8:w,%d0
m68k_00f02c_end:
.org 0xF030
m68k_00f030:
        move.w %d0,%d1
m68k_00f030_end:
.org 0xF032
m68k_00f032:
        lsl.w #0x1,%d1
m68k_00f032_end:
.org 0xF034
m68k_00f034:
        lea.l 0xf45e:w,%a0
m68k_00f034_end:
.org 0xF038
m68k_00f038:
        move.w (%a0, %d1.w),0xf630:w
m68k_00f038_end:
.org 0xF03E
m68k_00f03e:
        jsr 0x5f48:l
m68k_00f03e_end:
.org 0xF044
m68k_00f044:
        cmpi.w #0x1,%d3
m68k_00f044_end:
.org 0xF048
m68k_00f048:
        beq.b (. + 50)
m68k_00f048_end:
.org 0xF04A
m68k_00f04a:
        jsr 0x83d4:l
m68k_00f04a_end:
.org 0xF050
m68k_00f050:
        andi.l #0xffff,%d0
m68k_00f050_end:
.org 0xF056
m68k_00f056:
        move.l %d0,%d1
m68k_00f056_end:
.org 0xF058
m68k_00f058:
        lsl.l #0x1,%d0
m68k_00f058_end:
.org 0xF05A
m68k_00f05a:
        add.l %d1,%d0
m68k_00f05a_end:
.org 0xF05C
m68k_00f05c:
        lsl.l #0x3,%d0
m68k_00f05c_end:
.org 0xF05E
m68k_00f05e:
        add.l %d1,%d0
m68k_00f05e_end:
.org 0xF060
m68k_00f060:
        lsl.l #0x3,%d0
m68k_00f060_end:
.org 0xF062
m68k_00f062:
        swap %d0
m68k_00f062_end:
.org 0xF064
m68k_00f064:
        move.w 0xf3a6:w,%d1
m68k_00f064_end:
.org 0xF068
m68k_00f068:
        lsl.w #0x1,%d1
m68k_00f068_end:
.org 0xF06A
m68k_00f06a:
        lea.l 0xb600:w,%a0
m68k_00f06a_end:
.org 0xF06E
m68k_00f06e:
        move.w (%a0, %d1.w),%d1
m68k_00f06e_end:
.org 0xF072
m68k_00f072:
        add.w %d0,%d1
m68k_00f072_end:
.org 0xF074
m68k_00f074:
        cmpi.w #0xb4,%d1
m68k_00f074_end:
.org 0xF078
m68k_00f078:
        bhi.b (. + 6)
m68k_00f078_end:
.org 0xF07A
m68k_00f07a:
        clr.w %d0
m68k_00f07a_end:
.org 0xF07C
m68k_00f07c:
        bra.b (. + 6)
m68k_00f07c_end:
.org 0xF07E
m68k_00f07e:
        move.w #0x1,%d0
m68k_00f07e_end:
.org 0xF082
m68k_00f082:
        move.w %d0,0xf64a:w
m68k_00f082_end:
.org 0xF086
m68k_00f086:
        rts
m68k_00f086_end:
.org 0xF088
m68k_00f088:
        jsr 0x83d4:l
m68k_00f088_end:
.org 0xF08E
m68k_00f08e:
        andi.l #0xffff,%d0
m68k_00f08e_end:
.org 0xF094
m68k_00f094:
        move.l %d0,%d1
m68k_00f094_end:
.org 0xF096
m68k_00f096:
        lsl.l #0x2,%d0
m68k_00f096_end:
.org 0xF098
m68k_00f098:
        add.l %d1,%d0
m68k_00f098_end:
.org 0xF09A
m68k_00f09a:
        lsl.l #0x2,%d0
m68k_00f09a_end:
.org 0xF09C
m68k_00f09c:
        add.l %d1,%d0
m68k_00f09c_end:
.org 0xF09E
m68k_00f09e:
        swap %d0
m68k_00f09e_end:
.org 0xF0A0
m68k_00f0a0:
        addi.w #0x14,%d0
m68k_00f0a0_end:
.org 0xF0A4
m68k_00f0a4:
        move.w 0xf3a6:w,%d1
m68k_00f0a4_end:
.org 0xF0A8
m68k_00f0a8:
        lsl.w #0x1,%d1
m68k_00f0a8_end:
.org 0xF0AA
m68k_00f0aa:
        lea.l 0xb600:w,%a0
m68k_00f0aa_end:
.org 0xF0AE
m68k_00f0ae:
        move.w (%a0, %d1.w),%d2
m68k_00f0ae_end:
.org 0xF0B2
m68k_00f0b2:
        mulu.w %d0,%d2
m68k_00f0b2_end:
.org 0xF0B4
m68k_00f0b4:
        move.w 0xf392:w,%d0
m68k_00f0b4_end:
.org 0xF0B8
m68k_00f0b8:
        lsl.w #0x2,%d0
m68k_00f0b8_end:
.org 0xF0BA
m68k_00f0ba:
        lea.l 0xdffc:w,%a0
m68k_00f0ba_end:
.org 0xF0BE
m68k_00f0be:
        move.l (%a0, %d0.w),%d1
m68k_00f0be_end:
.org 0xF0C2
m68k_00f0c2:
        sub.l %d2,%d1
m68k_00f0c2_end:
.org 0xF0C4
m68k_00f0c4:
        bcs.b (. + 78)
m68k_00f0c4_end:
.org 0xF0C6
m68k_00f0c6:
        move.l %d1,(%a0, %d0.w)
m68k_00f0c6_end:
.org 0xF0CA
m68k_00f0ca:
        bsr.w (. + 360)
m68k_00f0ca_end:
.org 0xF0CE
m68k_00f0ce:
        move.w 0xf3f2:w,%d1
m68k_00f0ce_end:
.org 0xF0D2
m68k_00f0d2:
        lsl.w #0x1,%d1
m68k_00f0d2_end:
.org 0xF0D4
m68k_00f0d4:
        lea.l 0xb400:w,%a0
m68k_00f0d4_end:
.org 0xF0D8
m68k_00f0d8:
        add.w (%a0, %d1.w),%d0
m68k_00f0d8_end:
.org 0xF0DC
m68k_00f0dc:
        lea.l 0xc000:w,%a0
m68k_00f0dc_end:
.org 0xF0E0
m68k_00f0e0:
        add.w (%a0, %d1.w),%d0
m68k_00f0e0_end:
.org 0xF0E4
m68k_00f0e4:
        lea.l 0xb600:w,%a0
m68k_00f0e4_end:
.org 0xF0E8
m68k_00f0e8:
        add.w (%a0, %d1.w),%d0
m68k_00f0e8_end:
.org 0xF0EC
m68k_00f0ec:
        divu.w %d0,%d2
m68k_00f0ec_end:
.org 0xF0EE
m68k_00f0ee:
        cmpi.w #0x64,%d2
m68k_00f0ee_end:
.org 0xF0F2
m68k_00f0f2:
        bcc.b (. + 64)
m68k_00f0f2_end:
.org 0xF0F4
m68k_00f0f4:
        jsr 0x83d4:l
m68k_00f0f4_end:
.org 0xF0FA
m68k_00f0fa:
        moveq #0,%d0
m68k_00f0fa_end:
.org 0xF0FC
m68k_00f0fc:
        move.w 0xf61c:w,%d0
m68k_00f0fc_end:
.org 0xF100
m68k_00f100:
        move.l %d0,%d1
m68k_00f100_end:
.org 0xF102
m68k_00f102:
        lsl.l #0x1,%d0
m68k_00f102_end:
.org 0xF104
m68k_00f104:
        add.l %d1,%d0
m68k_00f104_end:
.org 0xF106
m68k_00f106:
        lsl.l #0x3,%d0
m68k_00f106_end:
.org 0xF108
m68k_00f108:
        add.l %d1,%d0
m68k_00f108_end:
.org 0xF10A
m68k_00f10a:
        lsl.l #0x2,%d0
m68k_00f10a_end:
.org 0xF10C
m68k_00f10c:
        swap %d0
m68k_00f10c_end:
.org 0xF10E
m68k_00f10e:
        cmp.w %d2,%d0
m68k_00f10e_end:
.org 0xF110
m68k_00f110:
        bls.b (. + 34)
m68k_00f110_end:
.org 0xF112
m68k_00f112:
        bsr.w (. + 380)
m68k_00f112_end:
.org 0xF116
m68k_00f116:
        bsr.w (. + 440)
m68k_00f116_end:
.org 0xF11A
m68k_00f11a:
        bsr.w (. + 506)
m68k_00f11a_end:
.org 0xF11E
m68k_00f11e:
        move.w #0x43,0xf3fe:w
m68k_00f11e_end:
.org 0xF124
m68k_00f124:
        move.w #0x1f,0xf362:w
m68k_00f124_end:
.org 0xF12A
m68k_00f12a:
        move.w #0x78,0xf608:w
m68k_00f12a_end:
.org 0xF130
m68k_00f130:
        bra.b (. + 30)
m68k_00f130_end:
.org 0xF132
m68k_00f132:
        bsr.w (. + 538)
m68k_00f132_end:
.org 0xF136
m68k_00f136:
        bsr.w (. + 1216)
m68k_00f136_end:
.org 0xF13A
m68k_00f13a:
        move.w #0x44,0xf3fe:w
m68k_00f13a_end:
.org 0xF140
m68k_00f140:
        move.w #0x2,0xff7026:l
m68k_00f140_end:
.org 0xF148
m68k_00f148:
        move.w #0x28,0xf362:w
m68k_00f148_end:
.org 0xF14E
m68k_00f14e:
        move.w 0xf376:w,%d0
m68k_00f14e_end:
.org 0xF152
m68k_00f152:
        cmp.w 0xf67a:w,%d0
m68k_00f152_end:
.org 0xF156
m68k_00f156:
        beq.w (. + 20)
m68k_00f156_end:
.org 0xF15A
m68k_00f15a:
        cmp.w 0xf67c:w,%d0
m68k_00f15a_end:
.org 0xF15E
m68k_00f15e:
        beq.w (. + 12)
m68k_00f15e_end:
.org 0xF162
m68k_00f162:
        cmp.w 0xf67e:w,%d0
m68k_00f162_end:
.org 0xF166
m68k_00f166:
        bne.w (. + 38)
m68k_00f166_end:
.org 0xF16A
m68k_00f16a:
        move.w #0x208,0xf612:w
m68k_00f16a_end:
.org 0xF170
m68k_00f170:
        move.w #0x41,%d0
m68k_00f170_end:
.org 0xF174
m68k_00f174:
        move.w 0xf3f2:w,0xf3d2:w
m68k_00f174_end:
.org 0xF17A
m68k_00f17a:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00f17a_end:
.org 0xF180
m68k_00f180:
        jsr 0x676f2:l
m68k_00f180_end:
.org 0xF186
m68k_00f186:
        move.w #0x78,0xf608:w
m68k_00f186_end:
.org 0xF18C
m68k_00f18c:
        rts
m68k_00f18c_end:
.org 0xF18E
m68k_00f18e:
        bsr.w (. + 1186)
m68k_00f18e_end:
.org 0xF192
m68k_00f192:
        tst.w %d0
m68k_00f192_end:
.org 0xF194
m68k_00f194:
        bne.w (. + 48)
m68k_00f194_end:
.org 0xF198
m68k_00f198:
        bsr.w (. + 1302)
m68k_00f198_end:
.org 0xF19C
m68k_00f19c:
        tst.w %d0
m68k_00f19c_end:
.org 0xF19E
m68k_00f19e:
        bne.b (. + 64)
m68k_00f19e_end:
.org 0xF1A0
m68k_00f1a0:
        move.w #0x78,0xf608:w
m68k_00f1a0_end:
.org 0xF1A6
m68k_00f1a6:
        move.w #0x1f,0xf362:w
m68k_00f1a6_end:
.org 0xF1AC
m68k_00f1ac:
        move.w #0x43,0xf3fe:w
m68k_00f1ac_end:
.org 0xF1B2
m68k_00f1b2:
        bsr.w (. + 962)
m68k_00f1b2_end:
.org 0xF1B6
m68k_00f1b6:
        bsr.w (. + 216)
m68k_00f1b6_end:
.org 0xF1BA
m68k_00f1ba:
        bsr.w (. + 276)
m68k_00f1ba_end:
.org 0xF1BE
m68k_00f1be:
        bsr.w (. + 342)
m68k_00f1be_end:
.org 0xF1C2
m68k_00f1c2:
        bra.b (. + 56)
m68k_00f1c2_end:
.org 0xF1C4
m68k_00f1c4:
        bsr.w (. + 452)
m68k_00f1c4_end:
.org 0xF1C8
m68k_00f1c8:
        bsr.w (. + 510)
m68k_00f1c8_end:
.org 0xF1CC
m68k_00f1cc:
        bsr.w (. + 328)
m68k_00f1cc_end:
.org 0xF1D0
m68k_00f1d0:
        move.w #0x1f,0xf362:w
m68k_00f1d0_end:
.org 0xF1D6
m68k_00f1d6:
        move.w #0x43,0xf3fe:w
m68k_00f1d6_end:
.org 0xF1DC
m68k_00f1dc:
        bra.b (. + 30)
m68k_00f1dc_end:
.org 0xF1DE
m68k_00f1de:
        bsr.w (. + 366)
m68k_00f1de_end:
.org 0xF1E2
m68k_00f1e2:
        bsr.w (. + 1044)
m68k_00f1e2_end:
.org 0xF1E6
m68k_00f1e6:
        move.w #0x44,0xf3fe:w
m68k_00f1e6_end:
.org 0xF1EC
m68k_00f1ec:
        move.w #0x28,0xf362:w
m68k_00f1ec_end:
.org 0xF1F2
m68k_00f1f2:
        move.w #0x2,0xff7026:l
m68k_00f1f2_end:
.org 0xF1FA
m68k_00f1fa:
        move.w #0x208,0xf612:w
m68k_00f1fa_end:
.org 0xF200
m68k_00f200:
        move.w #0x42,%d0
m68k_00f200_end:
.org 0xF204
m68k_00f204:
        cmpi.w #0xce,0xf3fe:w
m68k_00f204_end:
.org 0xF20A
m68k_00f20a:
        beq.w (. + 14)
m68k_00f20a_end:
.org 0xF20E
m68k_00f20e:
        move.w 0xf3f2:w,0xf3d2:w
m68k_00f20e_end:
.org 0xF214
m68k_00f214:
        bra.w (. + 10)
m68k_00f214_end:
.org 0xF218
m68k_00f218:
        move.w 0xf372:w,0xf3d2:w
m68k_00f218_end:
.org 0xF21E
m68k_00f21e:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00f21e_end:
.org 0xF224
m68k_00f224:
        jsr 0x676f2:l
m68k_00f224_end:
.org 0xF22A
m68k_00f22a:
        move.w #0x78,0xf608:w
m68k_00f22a_end:
.org 0xF230
m68k_00f230:
        rts
m68k_00f230_end:
.org 0xF232
m68k_00f232:
        move.w %d2,-(%a7)
m68k_00f232_end:
.org 0xF234
m68k_00f234:
        move.w 0xefd2:w,%d2
m68k_00f234_end:
.org 0xF238
m68k_00f238:
        lsl.w #0x1,%d2
m68k_00f238_end:
.org 0xF23A
m68k_00f23a:
        add.w 0xefd2:w,%d2
m68k_00f23a_end:
.org 0xF23E
m68k_00f23e:
        lsl.w #0x4,%d2
m68k_00f23e_end:
.org 0xF240
m68k_00f240:
        move.w 0xf392:w,%d0
m68k_00f240_end:
.org 0xF244
m68k_00f244:
        lea.l 0xf427:w,%a0
m68k_00f244_end:
.org 0xF248
m68k_00f248:
        move.b (%a0, %d0.w),%d1
m68k_00f248_end:
.org 0xF24C
m68k_00f24c:
        ext.w %d1
m68k_00f24c_end:
.org 0xF24E
m68k_00f24e:
        lsl.w #0x1,%d1
m68k_00f24e_end:
.org 0xF250
m68k_00f250:
        lea.l 0xe640:w,%a0
m68k_00f250_end:
.org 0xF254
m68k_00f254:
        move.w (%a0, %d1.w),%d1
m68k_00f254_end:
.org 0xF258
m68k_00f258:
        cmp.w 0xf3a6:w,%d1
m68k_00f258_end:
.org 0xF25C
m68k_00f25c:
        beq.b (. + 26)
m68k_00f25c_end:
.org 0xF25E
m68k_00f25e:
        addq.w #0x4,%d2
m68k_00f25e_end:
.org 0xF260
m68k_00f260:
        move.w 0xf392:w,%d0
m68k_00f260_end:
.org 0xF264
m68k_00f264:
        lsl.w #0x1,%d0
m68k_00f264_end:
.org 0xF266
m68k_00f266:
        lea.l 0xf45e:w,%a0
m68k_00f266_end:
.org 0xF26A
m68k_00f26a:
        move.w (%a0, %d0.w),%d0
m68k_00f26a_end:
.org 0xF26E
m68k_00f26e:
        cmp.w 0xf3a6:w,%d0
m68k_00f26e_end:
.org 0xF272
m68k_00f272:
        beq.b (. + 4)
m68k_00f272_end:
.org 0xF274
m68k_00f274:
        addq.w #0x4,%d2
m68k_00f274_end:
.org 0xF276
m68k_00f276:
        jsr 0x83d4:l
m68k_00f276_end:
.org 0xF27C
m68k_00f27c:
        lea.l -4964(%pc),%a0
m68k_00f27c_end:
.org 0xF280
m68k_00f280:
        mulu.w (%a0, %d2.w),%d0
m68k_00f280_end:
.org 0xF284
m68k_00f284:
        swap %d0
m68k_00f284_end:
.org 0xF286
m68k_00f286:
        add.w 0x2(%a0, %d2.w),%d0
m68k_00f286_end:
.org 0xF28A
m68k_00f28a:
        move.w (%a7)+,%d2
m68k_00f28a_end:
.org 0xF28C
m68k_00f28c:
        rts
m68k_00f28c_end:
.org 0xF28E
m68k_00f28e:
        jsr 0x83d4:l
m68k_00f28e_end:
.org 0xF294
m68k_00f294:
        andi.l #0xffff,%d0
m68k_00f294_end:
.org 0xF29A
m68k_00f29a:
        move.l %d0,%d1
m68k_00f29a_end:
.org 0xF29C
m68k_00f29c:
        lsl.l #0x2,%d0
m68k_00f29c_end:
.org 0xF29E
m68k_00f29e:
        add.l %d1,%d0
m68k_00f29e_end:
.org 0xF2A0
m68k_00f2a0:
        lsl.l #0x1,%d0
m68k_00f2a0_end:
.org 0xF2A2
m68k_00f2a2:
        add.l %d1,%d0
m68k_00f2a2_end:
.org 0xF2A4
m68k_00f2a4:
        swap %d0
m68k_00f2a4_end:
.org 0xF2A6
m68k_00f2a6:
        addi.w #0xa,%d0
m68k_00f2a6_end:
.org 0xF2AA
m68k_00f2aa:
        move.w 0xf3a6:w,%d1
m68k_00f2aa_end:
.org 0xF2AE
m68k_00f2ae:
        lea.l 0xc200:w,%a0
m68k_00f2ae_end:
.org 0xF2B2
m68k_00f2b2:
        move.b (%a0, %d1.w),%d2
m68k_00f2b2_end:
.org 0xF2B6
m68k_00f2b6:
        beq.b (. + 22)
m68k_00f2b6_end:
.org 0xF2B8
m68k_00f2b8:
        ext.w %d2
m68k_00f2b8_end:
.org 0xF2BA
m68k_00f2ba:
        mulu.w %d0,%d2
m68k_00f2ba_end:
.org 0xF2BC
m68k_00f2bc:
        divu.w #0x64,%d2
m68k_00f2bc_end:
.org 0xF2C0
m68k_00f2c0:
        sub.b %d2,(%a0, %d1.w)
m68k_00f2c0_end:
.org 0xF2C4
m68k_00f2c4:
        bcc.w (. + 8)
m68k_00f2c4_end:
.org 0xF2C8
m68k_00f2c8:
        clr.b (%a0, %d1.w)
m68k_00f2c8_end:
.org 0xF2CC
m68k_00f2cc:
        rts
m68k_00f2cc_end:
.org 0xF2CE
m68k_00f2ce:
        jsr 0x83d4:l
m68k_00f2ce_end:
.org 0xF2D4
m68k_00f2d4:
        andi.l #0xffff,%d0
m68k_00f2d4_end:
.org 0xF2DA
m68k_00f2da:
        move.l %d0,%d1
m68k_00f2da_end:
.org 0xF2DC
m68k_00f2dc:
        lsl.l #0x1,%d0
m68k_00f2dc_end:
.org 0xF2DE
m68k_00f2de:
        add.l %d1,%d0
m68k_00f2de_end:
.org 0xF2E0
m68k_00f2e0:
        lsl.l #0x1,%d0
m68k_00f2e0_end:
.org 0xF2E2
m68k_00f2e2:
        swap %d0
m68k_00f2e2_end:
.org 0xF2E4
m68k_00f2e4:
        addq.w #0x5,%d0
m68k_00f2e4_end:
.org 0xF2E6
m68k_00f2e6:
        move.w 0xf376:w,%d1
m68k_00f2e6_end:
.org 0xF2EA
m68k_00f2ea:
        lsl.w #0x1,%d1
m68k_00f2ea_end:
.org 0xF2EC
m68k_00f2ec:
        lea.l 0xe640:w,%a0
m68k_00f2ec_end:
.org 0xF2F0
m68k_00f2f0:
        move.w (%a0, %d1.w),%d1
m68k_00f2f0_end:
.org 0xF2F4
m68k_00f2f4:
        lea.l 0xc200:w,%a0
m68k_00f2f4_end:
.org 0xF2F8
m68k_00f2f8:
        move.b (%a0, %d1.w),%d2
m68k_00f2f8_end:
.org 0xF2FC
m68k_00f2fc:
        beq.b (. + 22)
m68k_00f2fc_end:
.org 0xF2FE
m68k_00f2fe:
        ext.w %d2
m68k_00f2fe_end:
.org 0xF300
m68k_00f300:
        mulu.w %d0,%d2
m68k_00f300_end:
.org 0xF302
m68k_00f302:
        divu.w #0x64,%d2
m68k_00f302_end:
.org 0xF306
m68k_00f306:
        sub.b %d2,(%a0, %d1.w)
m68k_00f306_end:
.org 0xF30A
m68k_00f30a:
        bcc.w (. + 8)
m68k_00f30a_end:
.org 0xF30E
m68k_00f30e:
        clr.b (%a0, %d1.w)
m68k_00f30e_end:
.org 0xF312
m68k_00f312:
        rts
m68k_00f312_end:
.org 0xF314
m68k_00f314:
        jsr 0x83d4:l
m68k_00f314_end:
.org 0xF31A
m68k_00f31a:
        andi.l #0xffff,%d0
m68k_00f31a_end:
.org 0xF320
m68k_00f320:
        move.l %d0,%d1
m68k_00f320_end:
.org 0xF322
m68k_00f322:
        lsl.l #0x1,%d0
m68k_00f322_end:
.org 0xF324
m68k_00f324:
        add.l %d1,%d0
m68k_00f324_end:
.org 0xF326
m68k_00f326:
        swap %d0
m68k_00f326_end:
.org 0xF328
m68k_00f328:
        addi.w #0x1,%d0
m68k_00f328_end:
.org 0xF32C
m68k_00f32c:
        move.w 0xf3a6:w,%d1
m68k_00f32c_end:
.org 0xF330
m68k_00f330:
        lsl.w #0x1,%d1
m68k_00f330_end:
.org 0xF332
m68k_00f332:
        lea.l 0xc000:w,%a0
m68k_00f332_end:
.org 0xF336
m68k_00f336:
        move.w (%a0, %d1.w),%d2
m68k_00f336_end:
.org 0xF33A
m68k_00f33a:
        add.w %d0,%d2
m68k_00f33a_end:
.org 0xF33C
m68k_00f33c:
        cmpi.w #0x3e7,%d2
m68k_00f33c_end:
.org 0xF340
m68k_00f340:
        bls.b (. + 6)
m68k_00f340_end:
.org 0xF342
m68k_00f342:
        move.w #0x3e7,%d2
m68k_00f342_end:
.org 0xF346
m68k_00f346:
        move.w %d2,(%a0, %d1.w)
m68k_00f346_end:
.org 0xF34A
m68k_00f34a:
        rts
m68k_00f34a_end:
.org 0xF34C
m68k_00f34c:
        move.w 0xf3a8:w,%d0
m68k_00f34c_end:
.org 0xF350
m68k_00f350:
        bsr.w (. + 2714)
m68k_00f350_end:
.org 0xF354
m68k_00f354:
        cmp.w 0xf3f2:w,%d0
m68k_00f354_end:
.org 0xF358
m68k_00f358:
        bne.b (. + 8)
m68k_00f358_end:
.org 0xF35A
m68k_00f35a:
        bsr.w (. + 176)
m68k_00f35a_end:
.org 0xF35E
m68k_00f35e:
        bra.b (. + 26)
m68k_00f35e_end:
.org 0xF360
m68k_00f360:
        move.w 0xf3a8:w,%d0
m68k_00f360_end:
.org 0xF364
m68k_00f364:
        lsl.w #0x1,%d0
m68k_00f364_end:
.org 0xF366
m68k_00f366:
        lea.l 0xf45e:w,%a0
m68k_00f366_end:
.org 0xF36A
m68k_00f36a:
        move.w (%a0, %d0.w),%d0
m68k_00f36a_end:
.org 0xF36E
m68k_00f36e:
        cmp.w 0xf3f2:w,%d0
m68k_00f36e_end:
.org 0xF372
m68k_00f372:
        bne.b (. + 6)
m68k_00f372_end:
.org 0xF374
m68k_00f374:
        bsr.w (. + 370)
m68k_00f374_end:
.org 0xF378
m68k_00f378:
        move.w 0xf3f2:w,%d0
m68k_00f378_end:
.org 0xF37C
m68k_00f37c:
        lea.l 0xcc00:w,%a0
m68k_00f37c_end:
.org 0xF380
m68k_00f380:
        move.b #0xff,(%a0, %d0.w)
m68k_00f380_end:
.org 0xF386
m68k_00f386:
        rts
m68k_00f386_end:
.org 0xF388
m68k_00f388:
        jsr 0x83d4:l
m68k_00f388_end:
.org 0xF38E
m68k_00f38e:
        andi.l #0xffff,%d0
m68k_00f38e_end:
.org 0xF394
m68k_00f394:
        move.l %d0,%d1
m68k_00f394_end:
.org 0xF396
m68k_00f396:
        lsl.l #0x1,%d0
m68k_00f396_end:
.org 0xF398
m68k_00f398:
        add.l %d1,%d0
m68k_00f398_end:
.org 0xF39A
m68k_00f39a:
        lsl.l #0x1,%d0
m68k_00f39a_end:
.org 0xF39C
m68k_00f39c:
        swap %d0
m68k_00f39c_end:
.org 0xF39E
m68k_00f39e:
        addi.w #0x5,%d0
m68k_00f39e_end:
.org 0xF3A2
m68k_00f3a2:
        move.w 0xf3a6:w,%d1
m68k_00f3a2_end:
.org 0xF3A6
m68k_00f3a6:
        lea.l 0xc200:w,%a0
m68k_00f3a6_end:
.org 0xF3AA
m68k_00f3aa:
        move.b (%a0, %d1.w),%d2
m68k_00f3aa_end:
.org 0xF3AE
m68k_00f3ae:
        beq.b (. + 22)
m68k_00f3ae_end:
.org 0xF3B0
m68k_00f3b0:
        ext.w %d2
m68k_00f3b0_end:
.org 0xF3B2
m68k_00f3b2:
        mulu.w %d0,%d2
m68k_00f3b2_end:
.org 0xF3B4
m68k_00f3b4:
        divu.w #0x64,%d2
m68k_00f3b4_end:
.org 0xF3B8
m68k_00f3b8:
        sub.b %d2,(%a0, %d1.w)
m68k_00f3b8_end:
.org 0xF3BC
m68k_00f3bc:
        bcc.w (. + 8)
m68k_00f3bc_end:
.org 0xF3C0
m68k_00f3c0:
        clr.b (%a0, %d1.w)
m68k_00f3c0_end:
.org 0xF3C4
m68k_00f3c4:
        rts
m68k_00f3c4_end:
.org 0xF3C6
m68k_00f3c6:
        jsr 0x83d4:l
m68k_00f3c6_end:
.org 0xF3CC
m68k_00f3cc:
        andi.l #0xffff,%d0
m68k_00f3cc_end:
.org 0xF3D2
m68k_00f3d2:
        move.l %d0,%d1
m68k_00f3d2_end:
.org 0xF3D4
m68k_00f3d4:
        lsl.l #0x1,%d0
m68k_00f3d4_end:
.org 0xF3D6
m68k_00f3d6:
        add.l %d1,%d0
m68k_00f3d6_end:
.org 0xF3D8
m68k_00f3d8:
        lsl.l #0x1,%d0
m68k_00f3d8_end:
.org 0xF3DA
m68k_00f3da:
        swap %d0
m68k_00f3da_end:
.org 0xF3DC
m68k_00f3dc:
        move.w 0xf376:w,%d1
m68k_00f3dc_end:
.org 0xF3E0
m68k_00f3e0:
        lsl.w #0x1,%d1
m68k_00f3e0_end:
.org 0xF3E2
m68k_00f3e2:
        lea.l 0xe640:w,%a0
m68k_00f3e2_end:
.org 0xF3E6
m68k_00f3e6:
        move.w (%a0, %d1.w),%d1
m68k_00f3e6_end:
.org 0xF3EA
m68k_00f3ea:
        lea.l 0xc200:w,%a0
m68k_00f3ea_end:
.org 0xF3EE
m68k_00f3ee:
        move.b (%a0, %d1.w),%d2
m68k_00f3ee_end:
.org 0xF3F2
m68k_00f3f2:
        beq.b (. + 22)
m68k_00f3f2_end:
.org 0xF3F4
m68k_00f3f4:
        ext.w %d2
m68k_00f3f4_end:
.org 0xF3F6
m68k_00f3f6:
        mulu.w %d0,%d2
m68k_00f3f6_end:
.org 0xF3F8
m68k_00f3f8:
        divu.w #0x64,%d2
m68k_00f3f8_end:
.org 0xF3FC
m68k_00f3fc:
        sub.b %d2,(%a0, %d1.w)
m68k_00f3fc_end:
.org 0xF400
m68k_00f400:
        bcc.w (. + 8)
m68k_00f400_end:
.org 0xF404
m68k_00f404:
        clr.b (%a0, %d1.w)
m68k_00f404_end:
.org 0xF408
m68k_00f408:
        rts
m68k_00f408_end:
.org 0xF40A
m68k_00f40a:
        tst.w 0xf64a:w
m68k_00f40a_end:
.org 0xF40E
m68k_00f40e:
        beq.w (. + 196)
m68k_00f40e_end:
.org 0xF412
m68k_00f412:
        move.w 0xf372:w,%d0
m68k_00f412_end:
.org 0xF416
m68k_00f416:
        lea.l 0xc700:w,%a0
m68k_00f416_end:
.org 0xF41A
m68k_00f41a:
        move.b (%a0, %d0.w),%d0
m68k_00f41a_end:
.org 0xF41E
m68k_00f41e:
        andi.w #0xf,%d0
m68k_00f41e_end:
.org 0xF422
m68k_00f422:
        beq.b (. + 88)
m68k_00f422_end:
.org 0xF424
m68k_00f424:
        cmpi.b #0x2,%d0
m68k_00f424_end:
.org 0xF428
m68k_00f428:
        bls.w (. + 136)
m68k_00f428_end:
.org 0xF42C
m68k_00f42c:
        move.w 0xf3a8:w,%d0
m68k_00f42c_end:
.org 0xF430
m68k_00f430:
        lea.l 0xf427:w,%a0
m68k_00f430_end:
.org 0xF434
m68k_00f434:
        move.b (%a0, %d0.w),%d1
m68k_00f434_end:
.org 0xF438
m68k_00f438:
        ext.w %d1
m68k_00f438_end:
.org 0xF43A
m68k_00f43a:
        lsl.w #0x1,%d1
m68k_00f43a_end:
.org 0xF43C
m68k_00f43c:
        lea.l 0xe640:w,%a0
m68k_00f43c_end:
.org 0xF440
m68k_00f440:
        move.w 0xf372:w,(%a0, %d1.w)
m68k_00f440_end:
.org 0xF446
m68k_00f446:
        lsl.w #0x1,%d0
m68k_00f446_end:
.org 0xF448
m68k_00f448:
        lea.l 0xf45e:w,%a0
m68k_00f448_end:
.org 0xF44C
m68k_00f44c:
        move.w 0xf372:w,(%a0, %d0.w)
m68k_00f44c_end:
.org 0xF452
m68k_00f452:
        lsr.w #0x1,%d1
m68k_00f452_end:
.org 0xF454
m68k_00f454:
        addq.b #0x1,(%a0, %d1.w)
m68k_00f454_end:
.org 0xF458
m68k_00f458:
        cmpi.w #0x4,(%a0, %d1.w)
m68k_00f458_end:
.org 0xF45E
m68k_00f45e:
        bne.w (. + 134)
m68k_00f45e_end:
.org 0xF462
m68k_00f462:
        lea.l 0xe640:w,%a0
m68k_00f462_end:
.org 0xF466
m68k_00f466:
        lsl.w #0x1,%d1
m68k_00f466_end:
.org 0xF468
m68k_00f468:
        move.w #0xffff,(%a0, %d1.w)
m68k_00f468_end:
.org 0xF46E
m68k_00f46e:
        lsr.w #0x1,%d1
m68k_00f46e_end:
.org 0xF470
m68k_00f470:
        move.w %d1,0xf64c:w
m68k_00f470_end:
.org 0xF474
m68k_00f474:
        bsr.w (. + -4326)
m68k_00f474_end:
.org 0xF478
m68k_00f478:
        bra.b (. + 108)
m68k_00f478_end:
.org 0xF47A
m68k_00f47a:
        jsr 0x83d4:l
m68k_00f47a_end:
.org 0xF480
m68k_00f480:
        moveq #0,%d0
m68k_00f480_end:
.org 0xF482
m68k_00f482:
        move.w 0xf61c:w,%d0
m68k_00f482_end:
.org 0xF486
m68k_00f486:
        move.l %d0,%d1
m68k_00f486_end:
.org 0xF488
m68k_00f488:
        lsl.l #0x1,%d0
m68k_00f488_end:
.org 0xF48A
m68k_00f48a:
        add.l %d1,%d0
m68k_00f48a_end:
.org 0xF48C
m68k_00f48c:
        lsl.l #0x3,%d0
m68k_00f48c_end:
.org 0xF48E
m68k_00f48e:
        add.l %d1,%d0
m68k_00f48e_end:
.org 0xF490
m68k_00f490:
        lsl.l #0x2,%d0
m68k_00f490_end:
.org 0xF492
m68k_00f492:
        swap %d0
m68k_00f492_end:
.org 0xF494
m68k_00f494:
        cmpi.w #0x46,%d0
m68k_00f494_end:
.org 0xF498
m68k_00f498:
        bhi.b (. + 18)
m68k_00f498_end:
.org 0xF49A
m68k_00f49a:
        move.w 0xf372:w,%d0
m68k_00f49a_end:
.org 0xF49E
m68k_00f49e:
        lea.l 0xcc00:w,%a0
m68k_00f49e_end:
.org 0xF4A2
m68k_00f4a2:
        move.b #0xff,(%a0, %d0.w)
m68k_00f4a2_end:
.org 0xF4A8
m68k_00f4a8:
        bra.b (. + 42)
m68k_00f4a8_end:
.org 0xF4AA
m68k_00f4aa:
        bsr.w (. + 98)
m68k_00f4aa_end:
.org 0xF4AE
m68k_00f4ae:
        bra.b (. + 36)
m68k_00f4ae_end:
.org 0xF4B0
m68k_00f4b0:
        jsr 0x83d4:l
m68k_00f4b0_end:
.org 0xF4B6
m68k_00f4b6:
        moveq #0,%d0
m68k_00f4b6_end:
.org 0xF4B8
m68k_00f4b8:
        move.w 0xf61c:w,%d0
m68k_00f4b8_end:
.org 0xF4BC
m68k_00f4bc:
        move.l %d0,%d1
m68k_00f4bc_end:
.org 0xF4BE
m68k_00f4be:
        lsl.l #0x1,%d0
m68k_00f4be_end:
.org 0xF4C0
m68k_00f4c0:
        add.l %d1,%d0
m68k_00f4c0_end:
.org 0xF4C2
m68k_00f4c2:
        lsl.l #0x3,%d0
m68k_00f4c2_end:
.org 0xF4C4
m68k_00f4c4:
        add.l %d1,%d0
m68k_00f4c4_end:
.org 0xF4C6
m68k_00f4c6:
        lsl.l #0x2,%d0
m68k_00f4c6_end:
.org 0xF4C8
m68k_00f4c8:
        swap %d0
m68k_00f4c8_end:
.org 0xF4CA
m68k_00f4ca:
        cmpi.w #0x1e,%d0
m68k_00f4ca_end:
.org 0xF4CE
m68k_00f4ce:
        bhi.b (. + -36)
m68k_00f4ce_end:
.org 0xF4D0
m68k_00f4d0:
        bra.b (. + -54)
m68k_00f4d0_end:
.org 0xF4D2
m68k_00f4d2:
        move.w 0xf3a8:w,%d0
m68k_00f4d2_end:
.org 0xF4D6
m68k_00f4d6:
        lea.l 0xf427:w,%a0
m68k_00f4d6_end:
.org 0xF4DA
m68k_00f4da:
        move.b (%a0, %d0.w),%d0
m68k_00f4da_end:
.org 0xF4DE
m68k_00f4de:
        ext.w %d0
m68k_00f4de_end:
.org 0xF4E0
m68k_00f4e0:
        jsr -4676(%pc)
m68k_00f4e0_end:
.org 0xF4E4
m68k_00f4e4:
        rts
m68k_00f4e4_end:
.org 0xF4E6
m68k_00f4e6:
        move.w 0xf3f2:w,%d1
m68k_00f4e6_end:
.org 0xF4EA
m68k_00f4ea:
        lea.l 0xcc00:w,%a0
m68k_00f4ea_end:
.org 0xF4EE
m68k_00f4ee:
        move.b (%a0, %d1.w),%d0
m68k_00f4ee_end:
.org 0xF4F2
m68k_00f4f2:
        move.b #0xff,(%a0, %d1.w)
m68k_00f4f2_end:
.org 0xF4F8
m68k_00f4f8:
        ext.w %d0
m68k_00f4f8_end:
.org 0xF4FA
m68k_00f4fa:
        move.w #0xffff,0xf630:w
m68k_00f4fa_end:
.org 0xF500
m68k_00f500:
        jsr 0x5f48:l
m68k_00f500_end:
.org 0xF506
m68k_00f506:
        bsr.w (. + -4880)
m68k_00f506_end:
.org 0xF50A
m68k_00f50a:
        rts
m68k_00f50a_end:
.org 0xF50C
m68k_00f50c:
        move.w 0xf3a6:w,%d0
m68k_00f50c_end:
.org 0xF510
m68k_00f510:
        lea.l 0xcc00:w,%a0
m68k_00f510_end:
.org 0xF514
m68k_00f514:
        move.b (%a0, %d0.w),%d0
m68k_00f514_end:
.org 0xF518
m68k_00f518:
        ext.w %d0
m68k_00f518_end:
.org 0xF51A
m68k_00f51a:
        move.w %d0,%d1
m68k_00f51a_end:
.org 0xF51C
m68k_00f51c:
        lsl.w #0x1,%d1
m68k_00f51c_end:
.org 0xF51E
m68k_00f51e:
        lea.l 0xf630:w,%a0
m68k_00f51e_end:
.org 0xF522
m68k_00f522:
        move.w (%a0, %d1.w),0xf630:w
m68k_00f522_end:
.org 0xF528
m68k_00f528:
        jsr 0x5f48:l
m68k_00f528_end:
.org 0xF52E
m68k_00f52e:
        cmpi.w #0xa,%d3
m68k_00f52e_end:
.org 0xF532
m68k_00f532:
        bcc.b (. + 50)
m68k_00f532_end:
.org 0xF534
m68k_00f534:
        jsr 0x83d4:l
m68k_00f534_end:
.org 0xF53A
m68k_00f53a:
        moveq #0,%d0
m68k_00f53a_end:
.org 0xF53C
m68k_00f53c:
        move.w 0xf61c:w,%d0
m68k_00f53c_end:
.org 0xF540
m68k_00f540:
        move.l %d0,%d1
m68k_00f540_end:
.org 0xF542
m68k_00f542:
        lsl.l #0x1,%d0
m68k_00f542_end:
.org 0xF544
m68k_00f544:
        add.l %d1,%d0
m68k_00f544_end:
.org 0xF546
m68k_00f546:
        lsl.l #0x3,%d0
m68k_00f546_end:
.org 0xF548
m68k_00f548:
        add.l %d1,%d0
m68k_00f548_end:
.org 0xF54A
m68k_00f54a:
        lsl.l #0x2,%d0
m68k_00f54a_end:
.org 0xF54C
m68k_00f54c:
        swap %d0
m68k_00f54c_end:
.org 0xF54E
m68k_00f54e:
        cmpi.w #0x1e,%d0
m68k_00f54e_end:
.org 0xF552
m68k_00f552:
        bhi.b (. + 18)
m68k_00f552_end:
.org 0xF554
m68k_00f554:
        move.w 0xf372:w,%d0
m68k_00f554_end:
.org 0xF558
m68k_00f558:
        lea.l 0xcc00:w,%a0
m68k_00f558_end:
.org 0xF55C
m68k_00f55c:
        move.b 0xf392:w,(%a0, %d0.w)
m68k_00f55c_end:
.org 0xF562
m68k_00f562:
        bra.b (. + 16)
m68k_00f562_end:
.org 0xF564
m68k_00f564:
        move.w 0xf372:w,%d0
m68k_00f564_end:
.org 0xF568
m68k_00f568:
        lea.l 0xcc00:w,%a0
m68k_00f568_end:
.org 0xF56C
m68k_00f56c:
        ori.b #0x80,(%a0, %d0.w)
m68k_00f56c_end:
.org 0xF572
m68k_00f572:
        rts
m68k_00f572_end:
.org 0xF574
m68k_00f574:
        move.w 0xf372:w,%d0
m68k_00f574_end:
.org 0xF578
m68k_00f578:
        lea.l 0xc700:w,%a0
m68k_00f578_end:
.org 0xF57C
m68k_00f57c:
        move.b (%a0, %d0.w),%d0
m68k_00f57c_end:
.org 0xF580
m68k_00f580:
        andi.b #0x7,%d0
m68k_00f580_end:
.org 0xF584
m68k_00f584:
        cmpi.b #0x3,%d0
m68k_00f584_end:
.org 0xF588
m68k_00f588:
        bcc.b (. + 44)
m68k_00f588_end:
.org 0xF58A
m68k_00f58a:
        jsr 0x83d4:l
m68k_00f58a_end:
.org 0xF590
m68k_00f590:
        andi.l #0xffff,%d0
m68k_00f590_end:
.org 0xF596
m68k_00f596:
        move.l %d0,%d1
m68k_00f596_end:
.org 0xF598
m68k_00f598:
        lsl.l #0x1,%d0
m68k_00f598_end:
.org 0xF59A
m68k_00f59a:
        add.l %d1,%d0
m68k_00f59a_end:
.org 0xF59C
m68k_00f59c:
        lsl.l #0x3,%d0
m68k_00f59c_end:
.org 0xF59E
m68k_00f59e:
        add.l %d1,%d0
m68k_00f59e_end:
.org 0xF5A0
m68k_00f5a0:
        lsl.l #0x2,%d0
m68k_00f5a0_end:
.org 0xF5A2
m68k_00f5a2:
        swap %d0
m68k_00f5a2_end:
.org 0xF5A4
m68k_00f5a4:
        cmpi.w #0x32,%d0
m68k_00f5a4_end:
.org 0xF5A8
m68k_00f5a8:
        bls.b (. + 12)
m68k_00f5a8_end:
.org 0xF5AA
m68k_00f5aa:
        bsr.w (. + 12)
m68k_00f5aa_end:
.org 0xF5AE
m68k_00f5ae:
        move.w #0xce,0xf3fe:w
m68k_00f5ae_end:
.org 0xF5B4
m68k_00f5b4:
        rts
m68k_00f5b4_end:
.org 0xF5B6
m68k_00f5b6:
        move.w 0xf372:w,%d0
m68k_00f5b6_end:
.org 0xF5BA
m68k_00f5ba:
        lea.l 0xcc00:w,%a0
m68k_00f5ba_end:
.org 0xF5BE
m68k_00f5be:
        move.b (%a0, %d0.w),%d1
m68k_00f5be_end:
.org 0xF5C2
m68k_00f5c2:
        move.b #0xff,(%a0, %d0.w)
m68k_00f5c2_end:
.org 0xF5C8
m68k_00f5c8:
        andi.w #0x3f,%d1
m68k_00f5c8_end:
.org 0xF5CC
m68k_00f5cc:
        move.w %d1,%d2
m68k_00f5cc_end:
.org 0xF5CE
m68k_00f5ce:
        lsl.w #0x1,%d2
m68k_00f5ce_end:
.org 0xF5D0
m68k_00f5d0:
        lea.l 0xf45e:w,%a0
m68k_00f5d0_end:
.org 0xF5D4
m68k_00f5d4:
        cmp.w (%a0, %d2.w),%d0
m68k_00f5d4_end:
.org 0xF5D8
m68k_00f5d8:
        bne.w (. + 28)
m68k_00f5d8_end:
.org 0xF5DC
m68k_00f5dc:
        move.w 0xf3a8:w,%d0
m68k_00f5dc_end:
.org 0xF5E0
m68k_00f5e0:
        move.w %d0,-(%a7)
m68k_00f5e0_end:
.org 0xF5E2
m68k_00f5e2:
        move.w #0xffff,0xf630:w
m68k_00f5e2_end:
.org 0xF5E8
m68k_00f5e8:
        jsr 0x5f48:l
m68k_00f5e8_end:
.org 0xF5EE
m68k_00f5ee:
        move.w (%a7)+,%d0
m68k_00f5ee_end:
.org 0xF5F0
m68k_00f5f0:
        jsr -5116(%pc)
m68k_00f5f0_end:
.org 0xF5F4
m68k_00f5f4:
        rts
m68k_00f5f4_end:
.org 0xF5F6
m68k_00f5f6:
        jsr 0x83d4:l
m68k_00f5f6_end:
.org 0xF5FC
m68k_00f5fc:
        moveq #0,%d0
m68k_00f5fc_end:
.org 0xF5FE
m68k_00f5fe:
        move.w 0xf61c:w,%d0
m68k_00f5fe_end:
.org 0xF602
m68k_00f602:
        move.l %d0,%d1
m68k_00f602_end:
.org 0xF604
m68k_00f604:
        lsl.l #0x2,%d0
m68k_00f604_end:
.org 0xF606
m68k_00f606:
        add.l %d1,%d0
m68k_00f606_end:
.org 0xF608
m68k_00f608:
        lsl.l #0x1,%d0
m68k_00f608_end:
.org 0xF60A
m68k_00f60a:
        swap %d0
m68k_00f60a_end:
.org 0xF60C
m68k_00f60c:
        addi.w #0xa,%d0
m68k_00f60c_end:
.org 0xF610
m68k_00f610:
        move.w 0xf3a6:w,%d1
m68k_00f610_end:
.org 0xF614
m68k_00f614:
        lsl.w #0x1,%d1
m68k_00f614_end:
.org 0xF616
m68k_00f616:
        lea.l 0xc000:w,%a0
m68k_00f616_end:
.org 0xF61A
m68k_00f61a:
        move.w (%a0, %d1.w),%d2
m68k_00f61a_end:
.org 0xF61E
m68k_00f61e:
        add.w %d0,%d2
m68k_00f61e_end:
.org 0xF620
m68k_00f620:
        cmpi.w #0x3e7,%d2
m68k_00f620_end:
.org 0xF624
m68k_00f624:
        bls.b (. + 6)
m68k_00f624_end:
.org 0xF626
m68k_00f626:
        move.w #0x3e7,%d2
m68k_00f626_end:
.org 0xF62A
m68k_00f62a:
        move.w %d2,(%a0, %d1.w)
m68k_00f62a_end:
.org 0xF62E
m68k_00f62e:
        rts
m68k_00f62e_end:
.org 0xF630
m68k_00f630:
        move.w 0xf3a8:w,%d0
m68k_00f630_end:
.org 0xF634
m68k_00f634:
        lea.l 0xf427:w,%a0
m68k_00f634_end:
.org 0xF638
m68k_00f638:
        move.b (%a0, %d0.w),%d0
m68k_00f638_end:
.org 0xF63C
m68k_00f63c:
        ext.w %d0
m68k_00f63c_end:
.org 0xF63E
m68k_00f63e:
        lsl.w #0x1,%d0
m68k_00f63e_end:
.org 0xF640
m68k_00f640:
        lea.l 0xe640:w,%a0
m68k_00f640_end:
.org 0xF644
m68k_00f644:
        move.w (%a0, %d0.w),0xf62e:w
m68k_00f644_end:
.org 0xF64A
m68k_00f64a:
        lea.l 0xf500:w,%a0
m68k_00f64a_end:
.org 0xF64E
m68k_00f64e:
        move.w #0xffff,%d2
m68k_00f64e_end:
.org 0xF652
m68k_00f652:
        move.w #0xff,%d3
m68k_00f652_end:
.org 0xF656
m68k_00f656:
        lea.l 0xc300:w,%a1
m68k_00f656_end:
.org 0xF65A
m68k_00f65a:
        move.w (%a0)+,%d0
m68k_00f65a_end:
.org 0xF65C
m68k_00f65c:
        bmi.b (. + 28)
m68k_00f65c_end:
.org 0xF65E
m68k_00f65e:
        cmp.w 0xf3f2:w,%d0
m68k_00f65e_end:
.org 0xF662
m68k_00f662:
        beq.b (. + -8)
m68k_00f662_end:
.org 0xF664
m68k_00f664:
        cmp.w 0xf62e:w,%d0
m68k_00f664_end:
.org 0xF668
m68k_00f668:
        beq.b (. + -14)
m68k_00f668_end:
.org 0xF66A
m68k_00f66a:
        cmp.b (%a1, %d0.w),%d3
m68k_00f66a_end:
.org 0xF66E
m68k_00f66e:
        bls.b (. + -20)
m68k_00f66e_end:
.org 0xF670
m68k_00f670:
        move.b (%a1, %d0.w),%d3
m68k_00f670_end:
.org 0xF674
m68k_00f674:
        move.w %d0,%d2
m68k_00f674_end:
.org 0xF676
m68k_00f676:
        bra.b (. + -28)
m68k_00f676_end:
.org 0xF678
m68k_00f678:
        tst.w %d2
m68k_00f678_end:
.org 0xF67A
m68k_00f67a:
        bmi.w (. + 38)
m68k_00f67a_end:
.org 0xF67E
m68k_00f67e:
        addi.w #0x1e,%d3
m68k_00f67e_end:
.org 0xF682
m68k_00f682:
        jsr 0x83d4:l
m68k_00f682_end:
.org 0xF688
m68k_00f688:
        andi.l #0xffff,%d0
m68k_00f688_end:
.org 0xF68E
m68k_00f68e:
        move.l %d0,%d1
m68k_00f68e_end:
.org 0xF690
m68k_00f690:
        lsl.l #0x1,%d0
m68k_00f690_end:
.org 0xF692
m68k_00f692:
        add.l %d1,%d0
m68k_00f692_end:
.org 0xF694
m68k_00f694:
        lsl.l #0x3,%d0
m68k_00f694_end:
.org 0xF696
m68k_00f696:
        add.l %d1,%d0
m68k_00f696_end:
.org 0xF698
m68k_00f698:
        lsl.l #0x2,%d0
m68k_00f698_end:
.org 0xF69A
m68k_00f69a:
        swap %d0
m68k_00f69a_end:
.org 0xF69C
m68k_00f69c:
        cmp.w %d3,%d0
m68k_00f69c_end:
.org 0xF69E
m68k_00f69e:
        bhi.b (. + 8)
m68k_00f69e_end:
.org 0xF6A0
m68k_00f6a0:
        move.w #0x1,%d0
m68k_00f6a0_end:
.org 0xF6A4
m68k_00f6a4:
        bra.b (. + 8)
m68k_00f6a4_end:
.org 0xF6A6
m68k_00f6a6:
        clr.w %d0
m68k_00f6a6_end:
.org 0xF6A8
m68k_00f6a8:
        move.w %d2,0xf372:w
m68k_00f6a8_end:
.org 0xF6AC
m68k_00f6ac:
        rts
m68k_00f6ac_end:
.org 0xF6AE
m68k_00f6ae:
        move.w 0xf372:w,%d0
m68k_00f6ae_end:
.org 0xF6B2
m68k_00f6b2:
        lsl.w #0x1,%d0
m68k_00f6b2_end:
.org 0xF6B4
m68k_00f6b4:
        lea.l 0xb400:w,%a0
m68k_00f6b4_end:
.org 0xF6B8
m68k_00f6b8:
        move.w (%a0, %d0.w),%d2
m68k_00f6b8_end:
.org 0xF6BC
m68k_00f6bc:
        lea.l 0xc000:w,%a0
m68k_00f6bc_end:
.org 0xF6C0
m68k_00f6c0:
        add.w (%a0, %d0.w),%d2
m68k_00f6c0_end:
.org 0xF6C4
m68k_00f6c4:
        lea.l 0xb600:w,%a0
m68k_00f6c4_end:
.org 0xF6C8
m68k_00f6c8:
        add.w (%a0, %d0.w),%d2
m68k_00f6c8_end:
.org 0xF6CC
m68k_00f6cc:
        bsr.w (. + 80)
m68k_00f6cc_end:
.org 0xF6D0
m68k_00f6d0:
        move.w 0xf3f2:w,%d1
m68k_00f6d0_end:
.org 0xF6D4
m68k_00f6d4:
        lsl.w #0x1,%d1
m68k_00f6d4_end:
.org 0xF6D6
m68k_00f6d6:
        lea.l 0xb400:w,%a0
m68k_00f6d6_end:
.org 0xF6DA
m68k_00f6da:
        add.w (%a0, %d1.w),%d0
m68k_00f6da_end:
.org 0xF6DE
m68k_00f6de:
        lea.l 0xc000:w,%a0
m68k_00f6de_end:
.org 0xF6E2
m68k_00f6e2:
        add.w (%a0, %d1.w),%d0
m68k_00f6e2_end:
.org 0xF6E6
m68k_00f6e6:
        lea.l 0xb600:w,%a0
m68k_00f6e6_end:
.org 0xF6EA
m68k_00f6ea:
        add.w (%a0, %d1.w),%d0
m68k_00f6ea_end:
.org 0xF6EE
m68k_00f6ee:
        mulu.w #0x64,%d2
m68k_00f6ee_end:
.org 0xF6F2
m68k_00f6f2:
        divu.w %d0,%d2
m68k_00f6f2_end:
.org 0xF6F4
m68k_00f6f4:
        jsr 0x83d4:l
m68k_00f6f4_end:
.org 0xF6FA
m68k_00f6fa:
        moveq #0,%d0
m68k_00f6fa_end:
.org 0xF6FC
m68k_00f6fc:
        move.w 0xf61c:w,%d0
m68k_00f6fc_end:
.org 0xF700
m68k_00f700:
        move.l %d0,%d1
m68k_00f700_end:
.org 0xF702
m68k_00f702:
        lsl.l #0x1,%d0
m68k_00f702_end:
.org 0xF704
m68k_00f704:
        add.l %d1,%d0
m68k_00f704_end:
.org 0xF706
m68k_00f706:
        lsl.l #0x3,%d0
m68k_00f706_end:
.org 0xF708
m68k_00f708:
        add.l %d1,%d0
m68k_00f708_end:
.org 0xF70A
m68k_00f70a:
        lsl.l #0x2,%d0
m68k_00f70a_end:
.org 0xF70C
m68k_00f70c:
        swap %d0
m68k_00f70c_end:
.org 0xF70E
m68k_00f70e:
        cmp.w %d2,%d0
m68k_00f70e_end:
.org 0xF710
m68k_00f710:
        bls.b (. + 6)
m68k_00f710_end:
.org 0xF712
m68k_00f712:
        clr.w %d0
m68k_00f712_end:
.org 0xF714
m68k_00f714:
        bra.b (. + 6)
m68k_00f714_end:
.org 0xF716
m68k_00f716:
        move.w #0x1,%d0
m68k_00f716_end:
.org 0xF71A
m68k_00f71a:
        rts
m68k_00f71a_end:
.org 0xF71C
m68k_00f71c:
        move.w %d2,-(%a7)
m68k_00f71c_end:
.org 0xF71E
m68k_00f71e:
        move.w 0xefd2:w,%d2
m68k_00f71e_end:
.org 0xF722
m68k_00f722:
        lsl.w #0x1,%d2
m68k_00f722_end:
.org 0xF724
m68k_00f724:
        add.w 0xefd2:w,%d2
m68k_00f724_end:
.org 0xF728
m68k_00f728:
        lsl.w #0x3,%d2
m68k_00f728_end:
.org 0xF72A
m68k_00f72a:
        move.w 0xf3a8:w,%d0
m68k_00f72a_end:
.org 0xF72E
m68k_00f72e:
        lea.l 0xf427:w,%a0
m68k_00f72e_end:
.org 0xF732
m68k_00f732:
        move.b (%a0, %d0.w),%d0
m68k_00f732_end:
.org 0xF736
m68k_00f736:
        ext.w %d0
m68k_00f736_end:
.org 0xF738
m68k_00f738:
        lsl.w #0x1,%d0
m68k_00f738_end:
.org 0xF73A
m68k_00f73a:
        lea.l 0xe640:w,%a0
m68k_00f73a_end:
.org 0xF73E
m68k_00f73e:
        move.w (%a0, %d0.w),%d0
m68k_00f73e_end:
.org 0xF742
m68k_00f742:
        cmp.w 0xf3f2:w,%d0
m68k_00f742_end:
.org 0xF746
m68k_00f746:
        beq.b (. + 26)
m68k_00f746_end:
.org 0xF748
m68k_00f748:
        addq.w #0x4,%d2
m68k_00f748_end:
.org 0xF74A
m68k_00f74a:
        move.w 0xf3a8:w,%d0
m68k_00f74a_end:
.org 0xF74E
m68k_00f74e:
        lsl.w #0x1,%d0
m68k_00f74e_end:
.org 0xF750
m68k_00f750:
        lea.l 0xf45e:w,%a0
m68k_00f750_end:
.org 0xF754
m68k_00f754:
        move.w (%a0, %d0.w),%d0
m68k_00f754_end:
.org 0xF758
m68k_00f758:
        cmp.w 0xf3f2:w,%d0
m68k_00f758_end:
.org 0xF75C
m68k_00f75c:
        beq.b (. + 4)
m68k_00f75c_end:
.org 0xF75E
m68k_00f75e:
        addq.w #0x4,%d2
m68k_00f75e_end:
.org 0xF760
m68k_00f760:
        jsr 0x83d4:l
m68k_00f760_end:
.org 0xF766
m68k_00f766:
        lea.l -6186(%pc),%a0
m68k_00f766_end:
.org 0xF76A
m68k_00f76a:
        mulu.w (%a0, %d2.w),%d0
m68k_00f76a_end:
.org 0xF76E
m68k_00f76e:
        swap %d0
m68k_00f76e_end:
.org 0xF770
m68k_00f770:
        add.w 0x2(%a0, %d2.w),%d0
m68k_00f770_end:
.org 0xF774
m68k_00f774:
        move.w (%a7)+,%d2
m68k_00f774_end:
.org 0xF776
m68k_00f776:
        rts
m68k_00f776_end:
.org 0xF778
m68k_00f778:
        bsr.w (. + 98)
m68k_00f778_end:
.org 0xF77C
m68k_00f77c:
        bsr.w (. + 176)
m68k_00f77c_end:
.org 0xF780
m68k_00f780:
        bsr.w (. + 864)
m68k_00f780_end:
.org 0xF784
m68k_00f784:
        cmp.w %d3,%d0
m68k_00f784_end:
.org 0xF786
m68k_00f786:
        bcs.b (. + 26)
m68k_00f786_end:
.org 0xF788
m68k_00f788:
        move.w #0x3a,0xf3fe:w
m68k_00f788_end:
.org 0xF78E
m68k_00f78e:
        bsr.w (. + 264)
m68k_00f78e_end:
.org 0xF792
m68k_00f792:
        move.w #0x78,0xf608:w
m68k_00f792_end:
.org 0xF798
m68k_00f798:
        move.w #0x1f,0xf362:w
m68k_00f798_end:
.org 0xF79E
m68k_00f79e:
        bra.b (. + 30)
m68k_00f79e_end:
.org 0xF7A0
m68k_00f7a0:
        move.w #0x3c,0xf3fe:w
m68k_00f7a0_end:
.org 0xF7A6
m68k_00f7a6:
        bsr.w (. + 490)
m68k_00f7a6_end:
.org 0xF7AA
m68k_00f7aa:
        bsr.w (. + 550)
m68k_00f7aa_end:
.org 0xF7AE
m68k_00f7ae:
        move.w #0x3,0xff7026:l
m68k_00f7ae_end:
.org 0xF7B6
m68k_00f7b6:
        move.w #0x28,0xf362:w
m68k_00f7b6_end:
.org 0xF7BC
m68k_00f7bc:
        move.w #0x208,0xf612:w
m68k_00f7bc_end:
.org 0xF7C2
m68k_00f7c2:
        move.w #0x9,%d0
m68k_00f7c2_end:
.org 0xF7C6
m68k_00f7c6:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00f7c6_end:
.org 0xF7CC
m68k_00f7cc:
        jsr 0x676f2:l
m68k_00f7cc_end:
.org 0xF7D2
m68k_00f7d2:
        move.w #0x78,0xf608:w
m68k_00f7d2_end:
.org 0xF7D8
m68k_00f7d8:
        rts
m68k_00f7d8_end:
.org 0xF7DA
m68k_00f7da:
        move.w 0xf3a6:w,%d0
m68k_00f7da_end:
.org 0xF7DE
m68k_00f7de:
        lsl.w #0x1,%d0
m68k_00f7de_end:
.org 0xF7E0
m68k_00f7e0:
        lea.l 0xc000:w,%a0
m68k_00f7e0_end:
.org 0xF7E4
m68k_00f7e4:
        moveq #0,%d2
m68k_00f7e4_end:
.org 0xF7E6
m68k_00f7e6:
        move.w (%a0, %d0.w),%d2
m68k_00f7e6_end:
.org 0xF7EA
m68k_00f7ea:
        divu.w #0xa,%d2
m68k_00f7ea_end:
.org 0xF7EE
m68k_00f7ee:
        lea.l 0xb600:w,%a0
m68k_00f7ee_end:
.org 0xF7F2
m68k_00f7f2:
        add.w (%a0, %d0.w),%d2
m68k_00f7f2_end:
.org 0xF7F6
m68k_00f7f6:
        jsr 0x83d4:l
m68k_00f7f6_end:
.org 0xF7FC
m68k_00f7fc:
        lea.l -6384(%pc),%a0
m68k_00f7fc_end:
.org 0xF800
m68k_00f800:
        move.w 0xefd2:w,%d1
m68k_00f800_end:
.org 0xF804
m68k_00f804:
        lsl.w #0x2,%d1
m68k_00f804_end:
.org 0xF806
m68k_00f806:
        mulu.w (%a0, %d1.w),%d0
m68k_00f806_end:
.org 0xF80A
m68k_00f80a:
        swap %d0
m68k_00f80a_end:
.org 0xF80C
m68k_00f80c:
        add.w 0x2(%a0, %d1.w),%d0
m68k_00f80c_end:
.org 0xF810
m68k_00f810:
        add.w %d0,%d2
m68k_00f810_end:
.org 0xF812
m68k_00f812:
        move.w 0xf3a8:w,%d0
m68k_00f812_end:
.org 0xF816
m68k_00f816:
        lsl.w #0x1,%d0
m68k_00f816_end:
.org 0xF818
m68k_00f818:
        lea.l 0xf45e:w,%a0
m68k_00f818_end:
.org 0xF81C
m68k_00f81c:
        move.w (%a0, %d0.w),%d0
m68k_00f81c_end:
.org 0xF820
m68k_00f820:
        lsl.w #0x1,%d0
m68k_00f820_end:
.org 0xF822
m68k_00f822:
        lea.l 0xb600:w,%a0
m68k_00f822_end:
.org 0xF826
m68k_00f826:
        sub.w (%a0, %d0.w),%d2
m68k_00f826_end:
.org 0xF82A
m68k_00f82a:
        rts
m68k_00f82a_end:
.org 0xF82C
m68k_00f82c:
        clr.w %d3
m68k_00f82c_end:
.org 0xF82E
m68k_00f82e:
        clr.w %d4
m68k_00f82e_end:
.org 0xF830
m68k_00f830:
        tst.w %d2
m68k_00f830_end:
.org 0xF832
m68k_00f832:
        beq.b (. + 98)
m68k_00f832_end:
.org 0xF834
m68k_00f834:
        bmi.b (. + 96)
m68k_00f834_end:
.org 0xF836
m68k_00f836:
        move.w #0xa,%d3
m68k_00f836_end:
.org 0xF83A
m68k_00f83a:
        addq.w #0x1,%d4
m68k_00f83a_end:
.org 0xF83C
m68k_00f83c:
        cmpi.w #0x32,%d2
m68k_00f83c_end:
.org 0xF840
m68k_00f840:
        bls.b (. + 84)
m68k_00f840_end:
.org 0xF842
m68k_00f842:
        move.w #0x1e,%d3
m68k_00f842_end:
.org 0xF846
m68k_00f846:
        addq.w #0x1,%d4
m68k_00f846_end:
.org 0xF848
m68k_00f848:
        cmpi.w #0x64,%d2
m68k_00f848_end:
.org 0xF84C
m68k_00f84c:
        bls.b (. + 72)
m68k_00f84c_end:
.org 0xF84E
m68k_00f84e:
        move.w #0x32,%d3
m68k_00f84e_end:
.org 0xF852
m68k_00f852:
        addq.w #0x1,%d4
m68k_00f852_end:
.org 0xF854
m68k_00f854:
        cmpi.w #0x96,%d2
m68k_00f854_end:
.org 0xF858
m68k_00f858:
        bls.b (. + 60)
m68k_00f858_end:
.org 0xF85A
m68k_00f85a:
        move.w #0x3c,%d3
m68k_00f85a_end:
.org 0xF85E
m68k_00f85e:
        addq.w #0x1,%d4
m68k_00f85e_end:
.org 0xF860
m68k_00f860:
        cmpi.w #0xc8,%d2
m68k_00f860_end:
.org 0xF864
m68k_00f864:
        bls.b (. + 48)
m68k_00f864_end:
.org 0xF866
m68k_00f866:
        move.w #0x46,%d3
m68k_00f866_end:
.org 0xF86A
m68k_00f86a:
        addq.w #0x1,%d4
m68k_00f86a_end:
.org 0xF86C
m68k_00f86c:
        cmpi.w #0xfa,%d2
m68k_00f86c_end:
.org 0xF870
m68k_00f870:
        bls.b (. + 36)
m68k_00f870_end:
.org 0xF872
m68k_00f872:
        move.w #0x50,%d3
m68k_00f872_end:
.org 0xF876
m68k_00f876:
        addq.w #0x1,%d4
m68k_00f876_end:
.org 0xF878
m68k_00f878:
        cmpi.w #0x12c,%d2
m68k_00f878_end:
.org 0xF87C
m68k_00f87c:
        bls.b (. + 24)
m68k_00f87c_end:
.org 0xF87E
m68k_00f87e:
        move.w #0x50,%d3
m68k_00f87e_end:
.org 0xF882
m68k_00f882:
        addq.w #0x1,%d4
m68k_00f882_end:
.org 0xF884
m68k_00f884:
        cmpi.w #0x15e,%d2
m68k_00f884_end:
.org 0xF888
m68k_00f888:
        bls.b (. + 12)
m68k_00f888_end:
.org 0xF88A
m68k_00f88a:
        move.w #0x55,%d3
m68k_00f88a_end:
.org 0xF88E
m68k_00f88e:
        addq.w #0x1,%d4
m68k_00f88e_end:
.org 0xF890
m68k_00f890:
        move.w #0x15f,%d2
m68k_00f890_end:
.org 0xF894
m68k_00f894:
        rts
m68k_00f894_end:
.org 0xF896
m68k_00f896:
        move.w 0xf3a6:w,%d0
m68k_00f896_end:
.org 0xF89A
m68k_00f89a:
        lea.l 0xe640:w,%a0
m68k_00f89a_end:
.org 0xF89E
m68k_00f89e:
        move.w #0x15,%d3
m68k_00f89e_end:
.org 0xF8A2
m68k_00f8a2:
        cmp.w (%a0)+,%d0
m68k_00f8a2_end:
.org 0xF8A4
m68k_00f8a4:
        beq.w (. + 190)
m68k_00f8a4_end:
.org 0xF8A8
m68k_00f8a8:
        dbra %d3,(. + -6)
m68k_00f8a8_end:
.org 0xF8AC
m68k_00f8ac:
        move.w 0xf3a6:w,%d0
m68k_00f8ac_end:
.org 0xF8B0
m68k_00f8b0:
        lsl.w #0x1,%d0
m68k_00f8b0_end:
.org 0xF8B2
m68k_00f8b2:
        lea.l 0xb400:w,%a0
m68k_00f8b2_end:
.org 0xF8B6
m68k_00f8b6:
        move.w (%a0, %d0.w),%d3
m68k_00f8b6_end:
.org 0xF8BA
m68k_00f8ba:
        lsr.w #0x1,%d3
m68k_00f8ba_end:
.org 0xF8BC
m68k_00f8bc:
        bsr.w (. + 548)
m68k_00f8bc_end:
.org 0xF8C0
m68k_00f8c0:
        cmp.w %d3,%d0
m68k_00f8c0_end:
.org 0xF8C2
m68k_00f8c2:
        bcs.w (. + 160)
m68k_00f8c2_end:
.org 0xF8C6
m68k_00f8c6:
        move.w 0xf3a8:w,%d0
m68k_00f8c6_end:
.org 0xF8CA
m68k_00f8ca:
        move.w #0xffff,0xf630:w
m68k_00f8ca_end:
.org 0xF8D0
m68k_00f8d0:
        jsr 0x5f48:l
m68k_00f8d0_end:
.org 0xF8D6
m68k_00f8d6:
        cmpi.w #0xa,%d3
m68k_00f8d6_end:
.org 0xF8DA
m68k_00f8da:
        bcc.b (. + 62)
m68k_00f8da_end:
.org 0xF8DC
m68k_00f8dc:
        move.w 0xf3a6:w,%d0
m68k_00f8dc_end:
.org 0xF8E0
m68k_00f8e0:
        lea.l 0xc300:w,%a0
m68k_00f8e0_end:
.org 0xF8E4
m68k_00f8e4:
        clr.w %d1
m68k_00f8e4_end:
.org 0xF8E6
m68k_00f8e6:
        move.b (%a0, %d0.w),%d1
m68k_00f8e6_end:
.org 0xF8EA
m68k_00f8ea:
        move.w #0x64,%d2
m68k_00f8ea_end:
.org 0xF8EE
m68k_00f8ee:
        sub.w %d1,%d2
m68k_00f8ee_end:
.org 0xF8F0
m68k_00f8f0:
        move.w 0xf3a8:w,%d1
m68k_00f8f0_end:
.org 0xF8F4
m68k_00f8f4:
        lsl.w #0x1,%d1
m68k_00f8f4_end:
.org 0xF8F6
m68k_00f8f6:
        lea.l 0xf45e:w,%a0
m68k_00f8f6_end:
.org 0xF8FA
m68k_00f8fa:
        move.w (%a0, %d1.w),%d1
m68k_00f8fa_end:
.org 0xF8FE
m68k_00f8fe:
        clr.w %d0
m68k_00f8fe_end:
.org 0xF900
m68k_00f900:
        lea.l 0xc200:w,%a0
m68k_00f900_end:
.org 0xF904
m68k_00f904:
        move.b (%a0, %d1.w),%d0
m68k_00f904_end:
.org 0xF908
m68k_00f908:
        add.w %d0,%d2
m68k_00f908_end:
.org 0xF90A
m68k_00f90a:
        cmpi.w #0x64,%d2
m68k_00f90a_end:
.org 0xF90E
m68k_00f90e:
        bcc.b (. + 80)
m68k_00f90e_end:
.org 0xF910
m68k_00f910:
        bsr.w (. + 464)
m68k_00f910_end:
.org 0xF914
m68k_00f914:
        cmp.w %d2,%d0
m68k_00f914_end:
.org 0xF916
m68k_00f916:
        bcs.b (. + 72)
m68k_00f916_end:
.org 0xF918
m68k_00f918:
        move.w #0x5d,0xf3fe:w
m68k_00f918_end:
.org 0xF91E
m68k_00f91e:
        move.w 0xf3a6:w,%d0
m68k_00f91e_end:
.org 0xF922
m68k_00f922:
        lea.l 0xcc00:w,%a0
m68k_00f922_end:
.org 0xF926
m68k_00f926:
        move.b #0xff,(%a0, %d0.w)
m68k_00f926_end:
.org 0xF92C
m68k_00f92c:
        lea.l 0xf45e:w,%a0
m68k_00f92c_end:
.org 0xF930
m68k_00f930:
        move.w 0xf392:w,%d0
m68k_00f930_end:
.org 0xF934
m68k_00f934:
        lsl.w #0x1,%d0
m68k_00f934_end:
.org 0xF936
m68k_00f936:
        move.w 0xf3a6:w,%d1
m68k_00f936_end:
.org 0xF93A
m68k_00f93a:
        cmp.w (%a0, %d0.w),%d1
m68k_00f93a_end:
.org 0xF93E
m68k_00f93e:
        bne.w (. + 80)
m68k_00f93e_end:
.org 0xF942
m68k_00f942:
        move.w 0xf392:w,%d0
m68k_00f942_end:
.org 0xF946
m68k_00f946:
        move.w #0xffff,0xf630:w
m68k_00f946_end:
.org 0xF94C
m68k_00f94c:
        jsr 0x5f48:l
m68k_00f94c_end:
.org 0xF952
m68k_00f952:
        move.w 0xf392:w,%d0
m68k_00f952_end:
.org 0xF956
m68k_00f956:
        jsr -5986(%pc)
m68k_00f956_end:
.org 0xF95A
m68k_00f95a:
        bra.w (. + 52)
m68k_00f95a_end:
.org 0xF95E
m68k_00f95e:
        bra.w (. + 48)
m68k_00f95e_end:
.org 0xF962
m68k_00f962:
        tst.w %d2
m68k_00f962_end:
.org 0xF964
m68k_00f964:
        bmi.b (. + 42)
m68k_00f964_end:
.org 0xF966
m68k_00f966:
        andi.l #0xffff,%d2
m68k_00f966_end:
.org 0xF96C
m68k_00f96c:
        divu.w #0xa,%d2
m68k_00f96c_end:
.org 0xF970
m68k_00f970:
        move.w 0xf3a6:w,%d0
m68k_00f970_end:
.org 0xF974
m68k_00f974:
        lsl.w #0x1,%d0
m68k_00f974_end:
.org 0xF976
m68k_00f976:
        lea.l 0xc000:w,%a0
m68k_00f976_end:
.org 0xF97A
m68k_00f97a:
        move.w (%a0, %d0.w),%d3
m68k_00f97a_end:
.org 0xF97E
m68k_00f97e:
        add.w %d2,%d3
m68k_00f97e_end:
.org 0xF980
m68k_00f980:
        cmpi.w #0x3e7,%d3
m68k_00f980_end:
.org 0xF984
m68k_00f984:
        bls.b (. + 6)
m68k_00f984_end:
.org 0xF986
m68k_00f986:
        move.w #0x3e7,%d3
m68k_00f986_end:
.org 0xF98A
m68k_00f98a:
        move.w %d3,(%a0, %d0.w)
m68k_00f98a_end:
.org 0xF98E
m68k_00f98e:
        rts
m68k_00f98e_end:
.org 0xF990
m68k_00f990:
        move.w 0xf3a6:w,%d0
m68k_00f990_end:
.org 0xF994
m68k_00f994:
        lsl.w #0x1,%d0
m68k_00f994_end:
.org 0xF996
m68k_00f996:
        andi.l #0xffff,%d2
m68k_00f996_end:
.org 0xF99C
m68k_00f99c:
        divu.w #0xa,%d2
m68k_00f99c_end:
.org 0xF9A0
m68k_00f9a0:
        lea.l 0xbe00:w,%a0
m68k_00f9a0_end:
.org 0xF9A4
m68k_00f9a4:
        add.w %d2,(%a0, %d0.w)
m68k_00f9a4_end:
.org 0xF9A8
m68k_00f9a8:
        cmpi.w #0x3e7,(%a0, %d0.w)
m68k_00f9a8_end:
.org 0xF9AE
m68k_00f9ae:
        bls.b (. + 8)
m68k_00f9ae_end:
.org 0xF9B0
m68k_00f9b0:
        move.w #0x3e7,(%a0, %d0.w)
m68k_00f9b0_end:
.org 0xF9B6
m68k_00f9b6:
        lsr.w #0x1,%d2
m68k_00f9b6_end:
.org 0xF9B8
m68k_00f9b8:
        lea.l 0xc000:w,%a0
m68k_00f9b8_end:
.org 0xF9BC
m68k_00f9bc:
        add.w %d2,(%a0, %d0.w)
m68k_00f9bc_end:
.org 0xF9C0
m68k_00f9c0:
        cmpi.w #0x3e7,(%a0, %d0.w)
m68k_00f9c0_end:
.org 0xF9C6
m68k_00f9c6:
        bls.b (. + 8)
m68k_00f9c6_end:
.org 0xF9C8
m68k_00f9c8:
        move.w #0x3e7,(%a0, %d0.w)
m68k_00f9c8_end:
.org 0xF9CE
m68k_00f9ce:
        rts
m68k_00f9ce_end:
.org 0xF9D0
m68k_00f9d0:
        tst.w %d4
m68k_00f9d0_end:
.org 0xF9D2
m68k_00f9d2:
        beq.b (. + 22)
m68k_00f9d2_end:
.org 0xF9D4
m68k_00f9d4:
        move.w 0xf3a8:w,%d2
m68k_00f9d4_end:
.org 0xF9D8
m68k_00f9d8:
        subq.w #0x1,%d2
m68k_00f9d8_end:
.org 0xF9DA
m68k_00f9da:
        lsl.w #0x2,%d2
m68k_00f9da_end:
.org 0xF9DC
m68k_00f9dc:
        bsr.w (. + 14)
m68k_00f9dc_end:
.org 0xF9E0
m68k_00f9e0:
        bsr.w (. + 90)
m68k_00f9e0_end:
.org 0xF9E4
m68k_00f9e4:
        bsr.w (. + 166)
m68k_00f9e4_end:
.org 0xF9E8
m68k_00f9e8:
        rts
m68k_00f9e8_end:
.org 0xF9EA
m68k_00f9ea:
        move.w %d4,%d5
m68k_00f9ea_end:
.org 0xF9EC
m68k_00f9ec:
        lsl.w #0x2,%d5
m68k_00f9ec_end:
.org 0xF9EE
m68k_00f9ee:
        lea.l 38(%pc),%a0
m68k_00f9ee_end:
.org 0xF9F2
m68k_00f9f2:
        move.w (%a0, %d5.w),%d6
m68k_00f9f2_end:
.org 0xF9F6
m68k_00f9f6:
        jsr 0x83d4:l
m68k_00f9f6_end:
.org 0xF9FC
m68k_00f9fc:
        mulu.w %d6,%d0
m68k_00f9fc_end:
.org 0xF9FE
m68k_00f9fe:
        swap %d0
m68k_00f9fe_end:
.org 0xFA00
m68k_00fa00:
        add.w 0x2(%a0, %d5.w),%d0
m68k_00fa00_end:
.org 0xFA04
m68k_00fa04:
        lea.l 0xe0a0:w,%a0
m68k_00fa04_end:
.org 0xFA08
m68k_00fa08:
        move.l (%a0, %d2.w),%d1
m68k_00fa08_end:
.org 0xFA0C
m68k_00fa0c:
        move.l %d1,%d3
m68k_00fa0c_end:
.org 0xFA0E
m68k_00fa0e:
        divu.w #0x64,%d3
m68k_00fa0e_end:
.org 0xFA12
m68k_00fa12:
        mulu.w %d0,%d3
m68k_00fa12_end:
.org 0xFA3A
m68k_00fa3a:
        move.w %d4,%d5
m68k_00fa3a_end:
.org 0xFA3C
m68k_00fa3c:
        lsl.w #0x2,%d5
m68k_00fa3c_end:
.org 0xFA3E
m68k_00fa3e:
        lea.l 38(%pc),%a0
m68k_00fa3e_end:
.org 0xFA42
m68k_00fa42:
        move.w (%a0, %d5.w),%d6
m68k_00fa42_end:
.org 0xFA46
m68k_00fa46:
        jsr 0x83d4:l
m68k_00fa46_end:
.org 0xFA4C
m68k_00fa4c:
        mulu.w %d6,%d0
m68k_00fa4c_end:
.org 0xFA4E
m68k_00fa4e:
        swap %d0
m68k_00fa4e_end:
.org 0xFA50
m68k_00fa50:
        add.w 0x2(%a0, %d5.w),%d0
m68k_00fa50_end:
.org 0xFA54
m68k_00fa54:
        lea.l 0xe000:w,%a0
m68k_00fa54_end:
.org 0xFA58
m68k_00fa58:
        move.l (%a0, %d2.w),%d1
m68k_00fa58_end:
.org 0xFA5C
m68k_00fa5c:
        move.l %d1,%d3
m68k_00fa5c_end:
.org 0xFA5E
m68k_00fa5e:
        divu.w #0x64,%d3
m68k_00fa5e_end:
.org 0xFA62
m68k_00fa62:
        mulu.w %d0,%d3
m68k_00fa62_end:
.org 0xFA8A
m68k_00fa8a:
        move.w %d4,%d5
m68k_00fa8a_end:
.org 0xFA8C
m68k_00fa8c:
        lsl.w #0x2,%d5
m68k_00fa8c_end:
.org 0xFA8E
m68k_00fa8e:
        lea.l 44(%pc),%a0
m68k_00fa8e_end:
.org 0xFA92
m68k_00fa92:
        move.w (%a0, %d5.w),%d6
m68k_00fa92_end:
.org 0xFA96
m68k_00fa96:
        jsr 0x83d4:l
m68k_00fa96_end:
.org 0xFA9C
m68k_00fa9c:
        mulu.w %d6,%d0
m68k_00fa9c_end:
.org 0xFA9E
m68k_00fa9e:
        swap %d0
m68k_00fa9e_end:
.org 0xFAA0
m68k_00faa0:
        add.w 0x2(%a0, %d5.w),%d0
m68k_00faa0_end:
.org 0xFAA4
m68k_00faa4:
        lea.l 0xe1e0:w,%a0
m68k_00faa4_end:
.org 0xFAA8
m68k_00faa8:
        move.l (%a0, %d2.w),%d1
m68k_00faa8_end:
.org 0xFAAC
m68k_00faac:
        move.w %d1,%d3
m68k_00faac_end:
.org 0xFAAE
m68k_00faae:
        mulu.w %d0,%d3
m68k_00faae_end:
.org 0xFAB0
m68k_00fab0:
        divu.w #0x64,%d3
m68k_00fab0_end:
.org 0xFAB4
m68k_00fab4:
        andi.l #0xffff,%d3
m68k_00fab4_end:
.org 0xFAE0
m68k_00fae0:
        jsr 0x83d4:l
m68k_00fae0_end:
.org 0xFAE6
m68k_00fae6:
        andi.l #0xffff,%d0
m68k_00fae6_end:
.org 0xFAEC
m68k_00faec:
        move.l %d0,%d1
m68k_00faec_end:
.org 0xFAEE
m68k_00faee:
        lsl.l #0x1,%d0
m68k_00faee_end:
.org 0xFAF0
m68k_00faf0:
        add.l %d1,%d0
m68k_00faf0_end:
.org 0xFAF2
m68k_00faf2:
        lsl.l #0x3,%d0
m68k_00faf2_end:
.org 0xFAF4
m68k_00faf4:
        add.l %d1,%d0
m68k_00faf4_end:
.org 0xFAF6
m68k_00faf6:
        lsl.l #0x2,%d0
m68k_00faf6_end:
.org 0xFAF8
m68k_00faf8:
        swap %d0
m68k_00faf8_end:
.org 0xFAFA
m68k_00fafa:
        rts
m68k_00fafa_end:
.org 0xFAFC
m68k_00fafc:
        tst.w 0xf386:w
m68k_00fafc_end:
.org 0xFB00
m68k_00fb00:
        bne.w (. + 168)
m68k_00fb00_end:
.org 0xFB04
m68k_00fb04:
        move.w 0xf376:w,%d0
m68k_00fb04_end:
.org 0xFB08
m68k_00fb08:
        lsl.w #0x2,%d0
m68k_00fb08_end:
.org 0xFB0A
m68k_00fb0a:
        lea.l 0xe9f8:w,%a1
m68k_00fb0a_end:
.org 0xFB0E
m68k_00fb0e:
        clr.w %d1
m68k_00fb0e_end:
.org 0xFB10
m68k_00fb10:
        move.b 0x1(%a1, %d0.w),%d1
m68k_00fb10_end:
.org 0xFB14
m68k_00fb14:
        lsl.w #0x2,%d1
m68k_00fb14_end:
.org 0xFB16
m68k_00fb16:
        lea.l 0xe65c:w,%a0
m68k_00fb16_end:
.org 0xFB1A
m68k_00fb1a:
        move.l (%a0, %d1.w),%d1
m68k_00fb1a_end:
.org 0xFB1E
m68k_00fb1e:
        bsr.w (. + 140)
m68k_00fb1e_end:
.org 0xFB22
m68k_00fb22:
        clr.w %d2
m68k_00fb22_end:
.org 0xFB24
m68k_00fb24:
        move.b 0x1(%a1, %d0.w),%d2
m68k_00fb24_end:
.org 0xFB28
m68k_00fb28:
        lsl.w #0x2,%d2
m68k_00fb28_end:
.org 0xFB2A
m68k_00fb2a:
        lea.l 0xdffc:w,%a2
m68k_00fb2a_end:
.org 0xFB2E
m68k_00fb2e:
        move.l (%a2, %d2.w),%d3
m68k_00fb2e_end:
.org 0xFB32
m68k_00fb32:
        sub.l %d1,%d3
m68k_00fb32_end:
.org 0xFB34
m68k_00fb34:
        bcs.w (. + 94)
m68k_00fb34_end:
.org 0xFB38
m68k_00fb38:
        move.l %d3,(%a2, %d2.w)
m68k_00fb38_end:
.org 0xFB3C
m68k_00fb3c:
        lea.l 0xe65c:w,%a3
m68k_00fb3c_end:
.org 0xFB40
m68k_00fb40:
        clr.l (%a3, %d2.w)
m68k_00fb40_end:
.org 0xFB44
m68k_00fb44:
        clr.w %d2
m68k_00fb44_end:
.org 0xFB46
m68k_00fb46:
        move.b (%a1, %d0.w),%d2
m68k_00fb46_end:
.org 0xFB4A
m68k_00fb4a:
        lsl.w #0x2,%d2
m68k_00fb4a_end:
.org 0xFB4C
m68k_00fb4c:
        move.l (%a2, %d2.w),%d3
m68k_00fb4c_end:
.org 0xFB50
m68k_00fb50:
        add.l %d1,%d3
m68k_00fb50_end:
.org 0xFB52
m68k_00fb52:
        cmpi.l #0xf423f,%d3
m68k_00fb52_end:
.org 0xFB58
m68k_00fb58:
        bls.b (. + 8)
m68k_00fb58_end:
.org 0xFB5A
m68k_00fb5a:
        move.l #0xf423f,%d3
m68k_00fb5a_end:
.org 0xFB60
m68k_00fb60:
        move.l %d3,(%a2, %d2.w)
m68k_00fb60_end:
.org 0xFB64
m68k_00fb64:
        clr.l (%a1, %d0.w)
m68k_00fb64_end:
.org 0xFB68
m68k_00fb68:
        move.w 0xe700:w,%d0
m68k_00fb68_end:
.org 0xFB6C
m68k_00fb6c:
        move.w 0xf376:w,%d1
m68k_00fb6c_end:
.org 0xFB70
m68k_00fb70:
        bclr.l %d1,%d0
m68k_00fb70_end:
.org 0xFB72
m68k_00fb72:
        move.w %d0,0xe700:w
m68k_00fb72_end:
.org 0xFB76
m68k_00fb76:
        move.w #0x28,0xf362:w
m68k_00fb76_end:
.org 0xFB7C
m68k_00fb7c:
        move.w #0x208,0xf612:w
m68k_00fb7c_end:
.org 0xFB82
m68k_00fb82:
        move.w #0x35,0xf3fe:w
m68k_00fb82_end:
.org 0xFB88
m68k_00fb88:
        move.w #0x12,0xff7026:l
m68k_00fb88_end:
.org 0xFB90
m68k_00fb90:
        bra.b (. + 24)
m68k_00fb90_end:
.org 0xFB92
m68k_00fb92:
        move.w #0x20,0xf362:w
m68k_00fb92_end:
.org 0xFB98
m68k_00fb98:
        move.w #0x208,0xf612:w
m68k_00fb98_end:
.org 0xFB9E
m68k_00fb9e:
        move.w #0xbd,%d0
m68k_00fb9e_end:
.org 0xFBA2
m68k_00fba2:
        jsr 0x676f2:l
m68k_00fba2_end:
.org 0xFBA8
m68k_00fba8:
        rts
m68k_00fba8_end:
.org 0xFBAA
m68k_00fbaa:
        move.b 0xf374:w,%d2
m68k_00fbaa_end:
.org 0xFBAE
m68k_00fbae:
        sub.b 0x2(%a1, %d0.w),%d2
m68k_00fbae_end:
.org 0xFBB2
m68k_00fbb2:
        ext.w %d2
m68k_00fbb2_end:
.org 0xFBB4
m68k_00fbb4:
        move.w %d2,%d3
m68k_00fbb4_end:
.org 0xFBB6
m68k_00fbb6:
        lsl.w #0x1,%d2
m68k_00fbb6_end:
.org 0xFBB8
m68k_00fbb8:
        add.w %d3,%d2
m68k_00fbb8_end:
.org 0xFBBA
m68k_00fbba:
        lsl.w #0x2,%d2
m68k_00fbba_end:
.org 0xFBBC
m68k_00fbbc:
        move.b 0xf375:w,%d3
m68k_00fbbc_end:
.org 0xFBC0
m68k_00fbc0:
        sub.b 0x3(%a1, %d0.w),%d3
m68k_00fbc0_end:
.org 0xFBC4
m68k_00fbc4:
        ext.w %d3
m68k_00fbc4_end:
.org 0xFBC6
m68k_00fbc6:
        add.w %d3,%d2
m68k_00fbc6_end:
.org 0xFBC8
m68k_00fbc8:
        beq.w (. + 38)
m68k_00fbc8_end:
.org 0xFBCC
m68k_00fbcc:
        move.w %d2,%d3
m68k_00fbcc_end:
.org 0xFBCE
m68k_00fbce:
        lsl.w #0x2,%d2
m68k_00fbce_end:
.org 0xFBD0
m68k_00fbd0:
        add.w %d3,%d2
m68k_00fbd0_end:
.org 0xFBD2
m68k_00fbd2:
        move.w %d2,%d3
m68k_00fbd2_end:
.org 0xFBD4
m68k_00fbd4:
        mulu.w %d1,%d3
m68k_00fbd4_end:
.org 0xFBD6
m68k_00fbd6:
        swap %d1
m68k_00fbd6_end:
.org 0xFBD8
m68k_00fbd8:
        mulu.w %d1,%d2
m68k_00fbd8_end:
.org 0xFBDA
m68k_00fbda:
        swap %d1
m68k_00fbda_end:
.org 0xFBDC
m68k_00fbdc:
        swap %d2
m68k_00fbdc_end:
.org 0xFBDE
m68k_00fbde:
        add.l %d3,%d2
m68k_00fbde_end:
.org 0xFBE0
m68k_00fbe0:
        move.l %d1,%d3
m68k_00fbe0_end:
.org 0xFBE2
m68k_00fbe2:
        move.l %d2,%d1
m68k_00fbe2_end:
.org 0xFBE4
m68k_00fbe4:
        moveq #100,%d2
m68k_00fbe4_end:
.org 0xFBE6
m68k_00fbe6:
        jsr 0x35760:l
m68k_00fbe6_end:
.org 0xFBEC
m68k_00fbec:
        add.l %d3,%d1
m68k_00fbec_end:
.org 0xFBEE
m68k_00fbee:
        rts
m68k_00fbee_end:
.org 0xFBF4
m68k_00fbf4:
        move.w 0xf392:w,%d0
m68k_00fbf4_end:
.org 0xFBF8
m68k_00fbf8:
        lea.l 0xdffc:w,%a0
m68k_00fbf8_end:
.org 0xFBFC
m68k_00fbfc:
        lsl.w #0x2,%d0
m68k_00fbfc_end:
.org 0xFBFE
m68k_00fbfe:
        move.l (%a0, %d0.w),%d1
m68k_00fbfe_end:
.org 0xFC02
m68k_00fc02:
        sub.l 0xf39e:w,%d1
m68k_00fc02_end:
.org 0xFC06
m68k_00fc06:
        move.l %d1,(%a0, %d0.w)
m68k_00fc06_end:
.org 0xFC0A
m68k_00fc0a:
        lea.l 0xe774:w,%a0
m68k_00fc0a_end:
.org 0xFC0E
m68k_00fc0e:
        move.l 0xf3e4:w,(%a0, %d0.w)
m68k_00fc0e_end:
.org 0xFC14
m68k_00fc14:
        rts
m68k_00fc14_end:
.org 0xFC16
m68k_00fc16:
        move.w 0xf3f0:w,%d0
m68k_00fc16_end:
.org 0xFC1A
m68k_00fc1a:
        lsl.w #0x2,%d0
m68k_00fc1a_end:
.org 0xFC1C
m68k_00fc1c:
        lea.l 0xef6a:w,%a0
m68k_00fc1c_end:
.org 0xFC20
m68k_00fc20:
        move.l (%a0, %d0.w),%d1
m68k_00fc20_end:
.org 0xFC24
m68k_00fc24:
        move.w 0xf392:w,%d2
m68k_00fc24_end:
.org 0xFC28
m68k_00fc28:
        lsl.w #0x2,%d2
m68k_00fc28_end:
.org 0xFC2A
m68k_00fc2a:
        lea.l 0xdffc:w,%a1
m68k_00fc2a_end:
.org 0xFC2E
m68k_00fc2e:
        sub.l %d1,(%a1, %d2.w)
m68k_00fc2e_end:
.org 0xFC32
m68k_00fc32:
        lea.l 0xea88:w,%a0
m68k_00fc32_end:
.org 0xFC36
m68k_00fc36:
        move.w 0xf3a6:w,%d0
m68k_00fc36_end:
.org 0xFC3A
m68k_00fc3a:
        lsl.w #0x1,%d0
m68k_00fc3a_end:
.org 0xFC3C
m68k_00fc3c:
        add.w 0xf3a6:w,%d0
m68k_00fc3c_end:
.org 0xFC40
m68k_00fc40:
        add.w 0xf3f0:w,%d0
m68k_00fc40_end:
.org 0xFC44
m68k_00fc44:
        move.w 0xf3f0:w,%d1
m68k_00fc44_end:
.org 0xFC48
m68k_00fc48:
        lsl.w #0x1,%d1
m68k_00fc48_end:
.org 0xFC4A
m68k_00fc4a:
        lea.l 0xef64:w,%a1
m68k_00fc4a_end:
.org 0xFC4E
m68k_00fc4e:
        move.w (%a1, %d1.w),%d2
m68k_00fc4e_end:
.org 0xFC52
m68k_00fc52:
        addq.w #0x1,%d2
m68k_00fc52_end:
.org 0xFC54
m68k_00fc54:
        move.b %d2,(%a0, %d0.w)
m68k_00fc54_end:
.org 0xFC58
m68k_00fc58:
        move.w 0xf38a:w,0xf612:w
m68k_00fc58_end:
.org 0xFC5E
m68k_00fc5e:
        move.w #0x28,0xf362:w
m68k_00fc5e_end:
.org 0xFC64
m68k_00fc64:
        move.w #0x62,0xf3fe:w
m68k_00fc64_end:
.org 0xFC6A
m68k_00fc6a:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00fc6a_end:
.org 0xFC70
m68k_00fc70:
        move.w #0x1,0xf774:w
m68k_00fc70_end:
.org 0xFC76
m68k_00fc76:
        move.w #0x9,0xff7026:l
m68k_00fc76_end:
.org 0xFC7E
m68k_00fc7e:
        rts
m68k_00fc7e_end:
.org 0xFC82
m68k_00fc82:
        cmpi.b #0x21,0xf57a:w
m68k_00fc82_end:
.org 0xFC88
m68k_00fc88:
        bne.b (. + 10)
m68k_00fc88_end:
.org 0xFC8A
m68k_00fc8a:
        jsr 0x10a58:l
m68k_00fc8a_end:
.org 0xFC90
m68k_00fc90:
        bra.b (. + 6)
m68k_00fc90_end:
.org 0xFC92
m68k_00fc92:
        bsr.w (. + 5402)
m68k_00fc92_end:
.org 0xFC96
m68k_00fc96:
        rts
m68k_00fc96_end:
.org 0xFC98
m68k_00fc98:
        move.w 0xf3a6:w,%d0
m68k_00fc98_end:
.org 0xFC9C
m68k_00fc9c:
        lea.l 0xcd00:w,%a0
m68k_00fc9c_end:
.org 0xFCA0
m68k_00fca0:
        move.b #0x4,(%a0, %d0.w)
m68k_00fca0_end:
.org 0xFCA6
m68k_00fca6:
        move.w 0xf392:w,%d0
m68k_00fca6_end:
.org 0xFCAA
m68k_00fcaa:
        lsl.w #0x1,%d0
m68k_00fcaa_end:
.org 0xFCAC
m68k_00fcac:
        add.w 0xf392:w,%d0
m68k_00fcac_end:
.org 0xFCB0
m68k_00fcb0:
        lsl.w #0x2,%d0
m68k_00fcb0_end:
.org 0xFCB2
m68k_00fcb2:
        lea.l 0xe80c:w,%a0
m68k_00fcb2_end:
.org 0xFCB6
m68k_00fcb6:
        lea.l 0xcd00:w,%a1
m68k_00fcb6_end:
.org 0xFCBA
m68k_00fcba:
        move.w 0x8(%a0, %d0.w),%d1
m68k_00fcba_end:
.org 0xFCBE
m68k_00fcbe:
        bmi.b (. + 18)
m68k_00fcbe_end:
.org 0xFCC0
m68k_00fcc0:
        clr.b (%a1, %d1.w)
m68k_00fcc0_end:
.org 0xFCC4
m68k_00fcc4:
        move.w #0xffff,0x8(%a0, %d0.w)
m68k_00fcc4_end:
.org 0xFCCA
m68k_00fcca:
        cmp.w 0xf3a6:w,%d1
m68k_00fcca_end:
.org 0xFCCE
m68k_00fcce:
        beq.b (. + 32)
m68k_00fcce_end:
.org 0xFCD0
m68k_00fcd0:
        move.w 0xf3a6:w,0x8(%a0, %d0.w)
m68k_00fcd0_end:
.org 0xFCD6
m68k_00fcd6:
        move.l 0xf39e:w,%d1
m68k_00fcd6_end:
.org 0xFCDA
m68k_00fcda:
        divu.w #0x64,%d1
m68k_00fcda_end:
.org 0xFCDE
m68k_00fcde:
        move.w %d1,0xa(%a0, %d0.w)
m68k_00fcde_end:
.org 0xFCE2
m68k_00fce2:
        move.w #0x7,0xff7026:l
m68k_00fce2_end:
.org 0xFCEA
m68k_00fcea:
        bsr.w (. + 2626)
m68k_00fcea_end:
.org 0xFCEE
m68k_00fcee:
        rts
m68k_00fcee_end:
.org 0xFCF0
m68k_00fcf0:
        bra.w (. + -5326)
m68k_00fcf0_end:
.org 0xFCF4
m68k_00fcf4:
        jsr 0x83d4:l
m68k_00fcf4_end:
.org 0xFCFA
m68k_00fcfa:
        move.w 0xf3a6:w,%d0
m68k_00fcfa_end:
.org 0xFCFE
m68k_00fcfe:
        lsl.w #0x2,%d0
m68k_00fcfe_end:
.org 0xFD00
m68k_00fd00:
        lea.l 0xc800:w,%a0
m68k_00fd00_end:
.org 0xFD04
m68k_00fd04:
        move.l (%a0, %d0.w),%d1
m68k_00fd04_end:
.org 0xFD08
m68k_00fd08:
        divu.w #0xa,%d1
m68k_00fd08_end:
.org 0xFD0C
m68k_00fd0c:
        andi.l #0xffff,%d1
m68k_00fd0c_end:
.org 0xFD12
m68k_00fd12:
        move.w 0xf392:w,%d3
m68k_00fd12_end:
.org 0xFD16
m68k_00fd16:
        lsl.w #0x2,%d3
m68k_00fd16_end:
.org 0xFD18
m68k_00fd18:
        lea.l 0xdffc:w,%a0
m68k_00fd18_end:
.org 0xFD1C
m68k_00fd1c:
        move.l (%a0, %d3.w),%d2
m68k_00fd1c_end:
.org 0xFD20
m68k_00fd20:
        sub.l %d1,%d2
m68k_00fd20_end:
.org 0xFD22
m68k_00fd22:
        bcs.w (. + 94)
m68k_00fd22_end:
.org 0xFD26
m68k_00fd26:
        move.l %d2,(%a0, %d3.w)
m68k_00fd26_end:
.org 0xFD2A
m68k_00fd2a:
        lsr.w #0x1,%d0
m68k_00fd2a_end:
.org 0xFD2C
m68k_00fd2c:
        lea.l 0xb400:w,%a0
m68k_00fd2c_end:
.org 0xFD30
m68k_00fd30:
        move.w (%a0, %d0.w),%d2
m68k_00fd30_end:
.org 0xFD34
m68k_00fd34:
        move.w %d2,%d1
m68k_00fd34_end:
.org 0xFD36
m68k_00fd36:
        lsl.w #0x2,%d2
m68k_00fd36_end:
.org 0xFD38
m68k_00fd38:
        add.w %d1,%d2
m68k_00fd38_end:
.org 0xFD3A
m68k_00fd3a:
        lea.l 0xc000:w,%a0
m68k_00fd3a_end:
.org 0xFD3E
m68k_00fd3e:
        add.w (%a0, %d0.w),%d2
m68k_00fd3e_end:
.org 0xFD42
m68k_00fd42:
        moveq #0,%d1
m68k_00fd42_end:
.org 0xFD44
m68k_00fd44:
        move.w 0xf61c:w,%d1
m68k_00fd44_end:
.org 0xFD48
m68k_00fd48:
        lsl.l #0x2,%d1
m68k_00fd48_end:
.org 0xFD4A
m68k_00fd4a:
        swap %d1
m68k_00fd4a_end:
.org 0xFD4C
m68k_00fd4c:
        addi.w #0x8,%d1
m68k_00fd4c_end:
.org 0xFD50
m68k_00fd50:
        mulu.w %d1,%d2
m68k_00fd50_end:
.org 0xFD52
m68k_00fd52:
        divu.w #0x3e8,%d2
m68k_00fd52_end:
.org 0xFD56
m68k_00fd56:
        lsr.w #0x1,%d0
m68k_00fd56_end:
.org 0xFD58
m68k_00fd58:
        lea.l 0xc500:w,%a0
m68k_00fd58_end:
.org 0xFD5C
m68k_00fd5c:
        clr.w %d1
m68k_00fd5c_end:
.org 0xFD5E
m68k_00fd5e:
        move.b (%a0, %d0.w),%d1
m68k_00fd5e_end:
.org 0xFD62
m68k_00fd62:
        add.w %d2,%d1
m68k_00fd62_end:
.org 0xFD64
m68k_00fd64:
        cmpi.w #0x64,%d1
m68k_00fd64_end:
.org 0xFD68
m68k_00fd68:
        bls.b (. + 14)
m68k_00fd68_end:
.org 0xFD6A
m68k_00fd6a:
        move.w #0x64,%d3
m68k_00fd6a_end:
.org 0xFD6E
m68k_00fd6e:
        sub.w %d1,%d3
m68k_00fd6e_end:
.org 0xFD70
m68k_00fd70:
        sub.w %d3,%d2
m68k_00fd70_end:
.org 0xFD72
m68k_00fd72:
        move.w #0x64,%d1
m68k_00fd72_end:
.org 0xFD76
m68k_00fd76:
        move.b %d1,(%a0, %d0.w)
m68k_00fd76_end:
.org 0xFD7A
m68k_00fd7a:
        bsr.w (. + 86)
m68k_00fd7a_end:
.org 0xFD7E
m68k_00fd7e:
        bra.b (. + 32)
m68k_00fd7e_end:
.org 0xFD80
m68k_00fd80:
        move.w #0x208,0xf612:w
m68k_00fd80_end:
.org 0xFD86
m68k_00fd86:
        move.w #0x23,0xf362:w
m68k_00fd86_end:
.org 0xFD8C
m68k_00fd8c:
        move.w #0xbd,%d0
m68k_00fd8c_end:
.org 0xFD90
m68k_00fd90:
        jsr 0x676f2:l
m68k_00fd90_end:
.org 0xFD96
m68k_00fd96:
        move.w #0x78,0xf608:w
m68k_00fd96_end:
.org 0xFD9C
m68k_00fd9c:
        bra.b (. + 50)
m68k_00fd9c_end:
.org 0xFD9E
m68k_00fd9e:
        ext.l %d2
m68k_00fd9e_end:
.org 0xFDA0
m68k_00fda0:
        move.l %d2,0xf3c8:w
m68k_00fda0_end:
.org 0xFDA4
m68k_00fda4:
        move.w #0x208,0xf612:w
m68k_00fda4_end:
.org 0xFDAA
m68k_00fdaa:
        move.w #0x20,0xf362:w
m68k_00fdaa_end:
.org 0xFDB0
m68k_00fdb0:
        move.w #0x66,%d0
m68k_00fdb0_end:
.org 0xFDB4
m68k_00fdb4:
        move.w 0xf3a6:w,0xf3d0:w
m68k_00fdb4_end:
.org 0xFDBA
m68k_00fdba:
        jsr 0x676f2:l
m68k_00fdba_end:
.org 0xFDC0
m68k_00fdc0:
        move.w 0xf3a6:w,%d0
m68k_00fdc0_end:
.org 0xFDC4
m68k_00fdc4:
        lea.l 0xcd00:w,%a0
m68k_00fdc4_end:
.org 0xFDC8
m68k_00fdc8:
        move.b #0x1,(%a0, %d0.w)
m68k_00fdc8_end:
.org 0xFDCE
m68k_00fdce:
        rts
m68k_00fdce_end:
.org 0xFDD0
m68k_00fdd0:
        lsl.w #0x1,%d0
m68k_00fdd0_end:
.org 0xFDD2
m68k_00fdd2:
        lea.l 0xc000:w,%a0
m68k_00fdd2_end:
.org 0xFDD6
m68k_00fdd6:
        add.w %d2,(%a0, %d0.w)
m68k_00fdd6_end:
.org 0xFDDA
m68k_00fdda:
        cmpi.w #0x3e7,(%a0, %d0.w)
m68k_00fdda_end:
.org 0xFDE0
m68k_00fde0:
        bls.b (. + 8)
m68k_00fde0_end:
.org 0xFDE2
m68k_00fde2:
        move.w #0x3e7,(%a0, %d0.w)
m68k_00fde2_end:
.org 0xFDE8
m68k_00fde8:
        rts
m68k_00fde8_end:
.org 0x102B6
m68k_0102b6:
        cmpi.b #0xa9,0xf57b:w
m68k_0102b6_end:
.org 0x102BC
m68k_0102bc:
        beq.w (. + 152)
m68k_0102bc_end:
.org 0x102C0
m68k_0102c0:
        movea.l 0xff382c:l,%a0
m68k_0102c0_end:
.org 0x102C6
m68k_0102c6:
        bset.b #0x4,(%a0)
m68k_0102c6_end:
.org 0x102CA
m68k_0102ca:
        move.b 0x5(%a0),%d0
m68k_0102ca_end:
.org 0x102CE
m68k_0102ce:
        lsl.w #0x8,%d0
m68k_0102ce_end:
.org 0x102D0
m68k_0102d0:
        move.b 0x6(%a0),%d0
m68k_0102d0_end:
.org 0x102D4
m68k_0102d4:
        lsl.l #0x8,%d0
m68k_0102d4_end:
.org 0x102D6
m68k_0102d6:
        move.b 0x7(%a0),%d0
m68k_0102d6_end:
.org 0x102DA
m68k_0102da:
        lsl.l #0x8,%d0
m68k_0102da_end:
.org 0x102DC
m68k_0102dc:
        move.b 0x8(%a0),%d0
m68k_0102dc_end:
.org 0x102E0
m68k_0102e0:
        move.w 0xf3f0:w,%d1
m68k_0102e0_end:
.org 0x102E4
m68k_0102e4:
        lsl.w #0x2,%d1
m68k_0102e4_end:
.org 0x102E6
m68k_0102e6:
        lea.l 0xef6a:w,%a1
m68k_0102e6_end:
.org 0x102EA
m68k_0102ea:
        sub.l (%a1, %d1.w),%d0
m68k_0102ea_end:
.org 0x102EE
m68k_0102ee:
        move.b %d0,0x8(%a0)
m68k_0102ee_end:
.org 0x102F2
m68k_0102f2:
        lsr.l #0x8,%d0
m68k_0102f2_end:
.org 0x102F4
m68k_0102f4:
        move.b %d0,0x7(%a0)
m68k_0102f4_end:
.org 0x102F8
m68k_0102f8:
        lsr.l #0x8,%d0
m68k_0102f8_end:
.org 0x102FA
m68k_0102fa:
        move.b %d0,0x6(%a0)
m68k_0102fa_end:
.org 0x102FE
m68k_0102fe:
        lsr.w #0x8,%d0
m68k_0102fe_end:
.org 0x10300
m68k_010300:
        move.b %d0,0x5(%a0)
m68k_010300_end:
.org 0x10304
m68k_010304:
        lea.l 0xea88:w,%a0
m68k_010304_end:
.org 0x10308
m68k_010308:
        move.w 0xf3a6:w,%d0
m68k_010308_end:
.org 0x1030C
m68k_01030c:
        lsl.w #0x1,%d0
m68k_01030c_end:
.org 0x1030E
m68k_01030e:
        add.w 0xf3a6:w,%d0
m68k_01030e_end:
.org 0x10312
m68k_010312:
        add.w 0xf3f0:w,%d0
m68k_010312_end:
.org 0x10316
m68k_010316:
        move.w 0xf3f0:w,%d1
m68k_010316_end:
.org 0x1031A
m68k_01031a:
        lsl.w #0x1,%d1
m68k_01031a_end:
.org 0x1031C
m68k_01031c:
        lea.l 0xef64:w,%a1
m68k_01031c_end:
.org 0x10320
m68k_010320:
        move.w (%a1, %d1.w),%d1
m68k_010320_end:
.org 0x10324
m68k_010324:
        addq.w #0x1,%d1
m68k_010324_end:
.org 0x10326
m68k_010326:
        move.b %d1,(%a0, %d0.w)
m68k_010326_end:
.org 0x1032A
m68k_01032a:
        move.w #0x208,0xf612:w
m68k_01032a_end:
.org 0x10330
m68k_010330:
        move.w #0x28,0xf362:w
m68k_010330_end:
.org 0x10336
m68k_010336:
        move.w #0x9,0xff7026:l
m68k_010336_end:
.org 0x1033E
m68k_01033e:
        move.w #0x62,0xf3fe:w
m68k_01033e_end:
.org 0x10344
m68k_010344:
        move.w 0xf3a6:w,0xf3d0:w
m68k_010344_end:
.org 0x1034A
m68k_01034a:
        move.w #0x1,0xf774:w
m68k_01034a_end:
.org 0x10350
m68k_010350:
        bra.w (. + 150)
m68k_010350_end:
.org 0x1072C
m68k_01072c:
        tst.w 0xefd6:w
m68k_01072c_end:
.org 0x10730
m68k_010730:
        bne.w (. + 204)
m68k_010730_end:
.org 0x10734
m68k_010734:
        move.w 0xf612:w,-(%a7)
m68k_010734_end:
.org 0x10738
m68k_010738:
        bclr.b #0x2,0xf3a5:w
m68k_010738_end:
.org 0x1073E
m68k_01073e:
        jsr 0x4a16:l
m68k_01073e_end:
.org 0x10744
m68k_010744:
        move.w #0x900,0xf612:w
m68k_010744_end:
.org 0x1074A
m68k_01074a:
        jsr 0xaf48:l
m68k_01074a_end:
.org 0x10750
m68k_010750:
        jsr 0x83c8:l
m68k_010750_end:
.org 0x10756
m68k_010756:
        move.w #0x2700,%sr
m68k_010756_end:
.org 0x1075A
m68k_01075a:
        bsr.w (. + 186)
m68k_01075a_end:
.org 0x1075E
m68k_01075e:
        move.l #0x40840003,0xc00004:l
m68k_01075e_end:
.org 0x10768
m68k_010768:
        move.w #0x5,%d0
m68k_010768_end:
.org 0x1076C
m68k_01076c:
        move.l #0x0,0xc00000:l
m68k_01076c_end:
.org 0x10776
m68k_010776:
        dbra %d0,(. + -10)
m68k_010776_end:
.org 0x1077A
m68k_01077a:
        bsr.w (. + 284)
m68k_01077a_end:
.org 0x1077E
m68k_01077e:
        jsr 0x3969a:l
m68k_01077e_end:
.org 0x10784
m68k_010784:
        move.w #0x2700,%sr
m68k_010784_end:
.org 0x10788
m68k_010788:
        bsr.w (. + 592)
m68k_010788_end:
.org 0x1078C
m68k_01078c:
        move.w #0xffff,0xff7026:l
m68k_01078c_end:
.org 0x10794
m68k_010794:
        move.l #0x40200000,0xc00004:l
m68k_010794_end:
.org 0x1079E
m68k_01079e:
        move.w #0x7,%d0
m68k_01079e_end:
.org 0x107A2
m68k_0107a2:
        move.l #0x11111111,0xc00000:l
m68k_0107a2_end:
.org 0x107AC
m68k_0107ac:
        dbra %d0,(. + -10)
m68k_0107ac_end:
.org 0x107B0
m68k_0107b0:
        clr.w 0xf37e:w
m68k_0107b0_end:
.org 0x107B4
m68k_0107b4:
        move.w (%a7)+,0xf612:w
m68k_0107b4_end:
.org 0x107B8
m68k_0107b8:
        bclr.b #0x3,0xf3a4:w
m68k_0107b8_end:
.org 0x107BE
m68k_0107be:
        clr.l 0xefc8:w
m68k_0107be_end:
.org 0x107C2
m68k_0107c2:
        clr.l 0xefcc:w
m68k_0107c2_end:
.org 0x107C6
m68k_0107c6:
        move.l #0x78000002,0xc00004:l
m68k_0107c6_end:
.org 0x107D0
m68k_0107d0:
        move.l #0x0,0xc00000:l
m68k_0107d0_end:
.org 0x107DA
m68k_0107da:
        move.l #0x0,0xc00000:l
m68k_0107da_end:
.org 0x107E4
m68k_0107e4:
        bsr.w (. + 156)
m68k_0107e4_end:
.org 0x107E8
m68k_0107e8:
        cmpi.w #0x1,0xf6c4:w
m68k_0107e8_end:
.org 0x107EE
m68k_0107ee:
        bne.w (. + 36)
m68k_0107ee_end:
.org 0x10812
m68k_010812:
        rts
m68k_010812_end:
.org 0x10814
m68k_010814:
        move.w 0xff7026:l,%d0
m68k_010814_end:
.org 0x1081A
m68k_01081a:
        lsl.w #0x1,%d0
m68k_01081a_end:
.org 0x1081C
m68k_01081c:
        move.w 18(%pc, %d0.w),%d0
m68k_01081c_end:
.org 0x10820
m68k_010820:
        move.w %d0,0xefd0:w
m68k_010820_end:
.org 0x10824
m68k_010824:
        bmi.w (. + 10)
m68k_010824_end:
.org 0x10828
m68k_010828:
        jsr 0x808a:l
m68k_010828_end:
.org 0x1082E
m68k_01082e:
        rts
m68k_01082e_end:
.org 0x10880
m68k_010880:
        tst.w 0xefd0:w
m68k_010880_end:
.org 0x10884
m68k_010884:
        bmi.w (. + 16)
m68k_010884_end:
.org 0x10888
m68k_010888:
        clr.w %d0
m68k_010888_end:
.org 0x1088A
m68k_01088a:
        move.b 0xf764:w,%d0
m68k_01088a_end:
.org 0x1088E
m68k_01088e:
        jsr 0x808a:l
m68k_01088e_end:
.org 0x10894
m68k_010894:
        rts
m68k_010894_end:
.org 0x10896
m68k_010896:
        move.l #0x72000001,0xc00004:l
m68k_010896_end:
.org 0x108A0
m68k_0108a0:
        move.w #0x7,%d0
m68k_0108a0_end:
.org 0x108A4
m68k_0108a4:
        move.l #0x33333333,0xc00000:l
m68k_0108a4_end:
.org 0x108AE
m68k_0108ae:
        dbra %d0,(. + -10)
m68k_0108ae_end:
.org 0x108B2
m68k_0108b2:
        lea.l 0x8a0bc:l,%a0
m68k_0108b2_end:
.org 0x108B8
m68k_0108b8:
        move.w #0x3f,%d0
m68k_0108b8_end:
.org 0x108BC
m68k_0108bc:
        move.l (%a0)+,0xc00000:l
m68k_0108bc_end:
.org 0x108C2
m68k_0108c2:
        dbra %d0,(. + -6)
m68k_0108c2_end:
.org 0x108C6
m68k_0108c6:
        move.l #0x41040003,%d0
m68k_0108c6_end:
.org 0x108CC
m68k_0108cc:
        bsr.w (. + 22)
m68k_0108cc_end:
.org 0x108D0
m68k_0108d0:
        move.w #0x9,%d2
m68k_0108d0_end:
.org 0x108D4
m68k_0108d4:
        bsr.w (. + 106)
m68k_0108d4_end:
.org 0x108D8
m68k_0108d8:
        dbra %d2,(. + -4)
m68k_0108d8_end:
.org 0x108DC
m68k_0108dc:
        bsr.w (. + 150)
m68k_0108dc_end:
.org 0x108E0
m68k_0108e0:
        rts
m68k_0108e0_end:
.org 0x108E2
m68k_0108e2:
        move.l %d0,0xc00004:l
m68k_0108e2_end:
.org 0x108E8
m68k_0108e8:
        move.w #0xc391,0xc00000:l
m68k_0108e8_end:
.org 0x108F0
m68k_0108f0:
        move.w #0x8,%d1
m68k_0108f0_end:
.org 0x108F4
m68k_0108f4:
        move.l #0xc392c392,0xc00000:l
m68k_0108f4_end:
.org 0x108FE
m68k_0108fe:
        dbra %d1,(. + -10)
m68k_0108fe_end:
.org 0x10902
m68k_010902:
        move.w #0xcb97,0xc00000:l
m68k_010902_end:
.org 0x1090A
m68k_01090a:
        addi.l #0x800000,%d0
m68k_01090a_end:
.org 0x10910
m68k_010910:
        move.l %d0,0xc00004:l
m68k_010910_end:
.org 0x10916
m68k_010916:
        move.l #0xc393c394,0xc00000:l
m68k_010916_end:
.org 0x10920
m68k_010920:
        move.w #0x7,%d1
m68k_010920_end:
.org 0x10924
m68k_010924:
        move.l #0xc395c395,0xc00000:l
m68k_010924_end:
.org 0x1092E
m68k_01092e:
        dbra %d1,(. + -10)
m68k_01092e_end:
.org 0x10932
m68k_010932:
        move.l #0xcb98db93,0xc00000:l
m68k_010932_end:
.org 0x1093C
m68k_01093c:
        rts
m68k_01093c_end:
.org 0x1093E
m68k_01093e:
        addi.l #0x800000,%d0
m68k_01093e_end:
.org 0x10944
m68k_010944:
        move.l %d0,0xc00004:l
m68k_010944_end:
.org 0x1094A
m68k_01094a:
        move.l #0xc393c396,0xc00000:l
m68k_01094a_end:
.org 0x10954
m68k_010954:
        move.w #0x7,%d1
m68k_010954_end:
.org 0x10958
m68k_010958:
        move.l #0x43904390,0xc00000:l
m68k_010958_end:
.org 0x10962
m68k_010962:
        dbra %d1,(. + -10)
m68k_010962_end:
.org 0x10966
m68k_010966:
        move.l #0xdb96db93,0xc00000:l
m68k_010966_end:
.org 0x10970
m68k_010970:
        rts
m68k_010970_end:
.org 0x10972
m68k_010972:
        addi.l #0x800000,%d0
m68k_010972_end:
.org 0x10978
m68k_010978:
        move.l %d0,0xc00004:l
m68k_010978_end:
.org 0x1097E
m68k_01097e:
        move.l #0xc393d398,0xc00000:l
m68k_01097e_end:
.org 0x10988
m68k_010988:
        move.w #0x7,%d1
m68k_010988_end:
.org 0x1098C
m68k_01098c:
        move.l #0xdb95db95,0xc00000:l
m68k_01098c_end:
.org 0x10996
m68k_010996:
        dbra %d1,(. + -10)
m68k_010996_end:
.org 0x1099A
m68k_01099a:
        move.l #0xdb94db93,0xc00000:l
m68k_01099a_end:
.org 0x109A4
m68k_0109a4:
        addi.l #0x800000,%d0
m68k_0109a4_end:
.org 0x109AA
m68k_0109aa:
        move.l %d0,0xc00004:l
m68k_0109aa_end:
.org 0x109B0
m68k_0109b0:
        move.l #0xd397db92,0xc00000:l
m68k_0109b0_end:
.org 0x109BA
m68k_0109ba:
        move.w #0x7,%d1
m68k_0109ba_end:
.org 0x109BE
m68k_0109be:
        move.l #0xdb92db92,0xc00000:l
m68k_0109be_end:
.org 0x109C8
m68k_0109c8:
        dbra %d1,(. + -10)
m68k_0109c8_end:
.org 0x109CC
m68k_0109cc:
        move.l #0xdb92db91,0xc00000:l
m68k_0109cc_end:
.org 0x109D6
m68k_0109d6:
        rts
m68k_0109d6_end:
.org 0x109D8
m68k_0109d8:
        move.l #0x41040003,%d0
m68k_0109d8_end:
.org 0x109DE
m68k_0109de:
        move.w #0xd,%d1
m68k_0109de_end:
.org 0x109E2
m68k_0109e2:
        move.l %d0,0xc00004:l
m68k_0109e2_end:
.org 0x109E8
m68k_0109e8:
        move.w #0x9,%d2
m68k_0109e8_end:
.org 0x109EC
m68k_0109ec:
        move.l #0x0,0xc00000:l
m68k_0109ec_end:
.org 0x109F6
m68k_0109f6:
        dbra %d2,(. + -10)
m68k_0109f6_end:
.org 0x109FA
m68k_0109fa:
        addi.l #0x800000,%d0
m68k_0109fa_end:
.org 0x10A00
m68k_010a00:
        dbra %d1,(. + -30)
m68k_010a00_end:
.org 0x10A04
m68k_010a04:
        rts
m68k_010a04_end:
.org 0x10A58
m68k_010a58:
        cmpi.w #0x6e,0xf38c:w
m68k_010a58_end:
.org 0x10A5E
m68k_010a5e:
        beq.w (. + 1154)
m68k_010a5e_end:
.org 0x10A62
m68k_010a62:
        cmpi.w #0x72,0xf38c:w
m68k_010a62_end:
.org 0x10A68
m68k_010a68:
        beq.w (. + 1204)
m68k_010a68_end:
.org 0x10A6C
m68k_010a6c:
        cmpi.w #0x73,0xf38c:w
m68k_010a6c_end:
.org 0x10A72
m68k_010a72:
        beq.w (. + 1222)
m68k_010a72_end:
.org 0x10A76
m68k_010a76:
        lea.l 0xcd00:w,%a0
m68k_010a76_end:
.org 0x10A7A
m68k_010a7a:
        move.w 0xf3a6:w,%d0
m68k_010a7a_end:
.org 0x10A7E
m68k_010a7e:
        move.b #0x1,(%a0, %d0.w)
m68k_010a7e_end:
.org 0x10A84
m68k_010a84:
        move.w 0xf392:w,%d0
m68k_010a84_end:
.org 0x10A88
m68k_010a88:
        move.w 0xf3a6:w,%d1
m68k_010a88_end:
.org 0x10A8C
m68k_010a8c:
        bsr.w (. + 1536)
m68k_010a8c_end:
.org 0x10A90
m68k_010a90:
        move.w %d0,%d7
m68k_010a90_end:
.org 0x10A92
m68k_010a92:
        beq.b (. + 16)
m68k_010a92_end:
.org 0x10A94
m68k_010a94:
        bsr.w (. + 20)
m68k_010a94_end:
.org 0x10A98
m68k_010a98:
        bsr.w (. + 70)
m68k_010a98_end:
.org 0x10A9C
m68k_010a9c:
        bsr.w (. + 472)
m68k_010a9c_end:
.org 0x10AA0
m68k_010aa0:
        bra.b (. + 6)
m68k_010aa0_end:
.org 0x10AA2
m68k_010aa2:
        bsr.w (. + 626)
m68k_010aa2_end:
.org 0x10AA6
m68k_010aa6:
        rts
m68k_010aa6_end:
.org 0x10AA8
m68k_010aa8:
        move.w 0xf3a6:w,%d0
m68k_010aa8_end:
.org 0x10AAC
m68k_010aac:
        lea.l 0xc200:w,%a0
m68k_010aac_end:
.org 0x10AB0
m68k_010ab0:
        clr.w %d2
m68k_010ab0_end:
.org 0x10AB2
m68k_010ab2:
        move.b (%a0, %d0.w),%d2
m68k_010ab2_end:
.org 0x10AB6
m68k_010ab6:
        lsl.w #0x1,%d0
m68k_010ab6_end:
.org 0x10AB8
m68k_010ab8:
        lea.l 0xb600:w,%a0
m68k_010ab8_end:
.org 0x10ABC
m68k_010abc:
        add.w (%a0, %d0.w),%d2
m68k_010abc_end:
.org 0x10AC0
m68k_010ac0:
        jsr 0x83d4:l
m68k_010ac0_end:
.org 0x10AC6
m68k_010ac6:
        move.w 0xefd2:w,%d1
m68k_010ac6_end:
.org 0x10ACA
m68k_010aca:
        lsl.w #0x2,%d1
m68k_010aca_end:
.org 0x10ACC
m68k_010acc:
        lea.l -130(%pc),%a0
m68k_010acc_end:
.org 0x10AD0
m68k_010ad0:
        mulu.w (%a0, %d1.w),%d0
m68k_010ad0_end:
.org 0x10AD4
m68k_010ad4:
        swap %d0
m68k_010ad4_end:
.org 0x10AD6
m68k_010ad6:
        add.w 0x2(%a0, %d1.w),%d0
m68k_010ad6_end:
.org 0x10ADA
m68k_010ada:
        add.w %d0,%d2
m68k_010ada_end:
.org 0x10ADC
m68k_010adc:
        rts
m68k_010adc_end:
.org 0x10ADE
m68k_010ade:
        clr.w %d3
m68k_010ade_end:
.org 0x10AE0
m68k_010ae0:
        cmpi.w #0x32,%d2
m68k_010ae0_end:
.org 0x10AE4
m68k_010ae4:
        bls.b (. + 46)
m68k_010ae4_end:
.org 0x10AE6
m68k_010ae6:
        addq.w #0x1,%d3
m68k_010ae6_end:
.org 0x10AE8
m68k_010ae8:
        cmpi.w #0x64,%d2
m68k_010ae8_end:
.org 0x10AEC
m68k_010aec:
        bls.w (. + 38)
m68k_010aec_end:
.org 0x10AF0
m68k_010af0:
        addq.w #0x1,%d3
m68k_010af0_end:
.org 0x10AF2
m68k_010af2:
        cmpi.w #0x96,%d2
m68k_010af2_end:
.org 0x10AF6
m68k_010af6:
        bls.b (. + 28)
m68k_010af6_end:
.org 0x10AF8
m68k_010af8:
        addq.w #0x1,%d3
m68k_010af8_end:
.org 0x10AFA
m68k_010afa:
        cmpi.w #0xc8,%d2
m68k_010afa_end:
.org 0x10AFE
m68k_010afe:
        bls.b (. + 20)
m68k_010afe_end:
.org 0x10B00
m68k_010b00:
        addq.w #0x1,%d3
m68k_010b00_end:
.org 0x10B02
m68k_010b02:
        cmpi.w #0xfa,%d2
m68k_010b02_end:
.org 0x10B06
m68k_010b06:
        bls.b (. + 12)
m68k_010b06_end:
.org 0x10B08
m68k_010b08:
        addq.w #0x1,%d3
m68k_010b08_end:
.org 0x10B0A
m68k_010b0a:
        cmpi.w #0x12c,%d2
m68k_010b0a_end:
.org 0x10B0E
m68k_010b0e:
        bls.b (. + 4)
m68k_010b0e_end:
.org 0x10B10
m68k_010b10:
        addq.w #0x1,%d3
m68k_010b10_end:
.org 0x10B12
m68k_010b12:
        move.w %d3,%d4
m68k_010b12_end:
.org 0x10B14
m68k_010b14:
        lsl.w #0x1,%d3
m68k_010b14_end:
.org 0x10B16
m68k_010b16:
        add.w %d4,%d3
m68k_010b16_end:
.org 0x10B18
m68k_010b18:
        lsl.w #0x4,%d3
m68k_010b18_end:
.org 0x10B1A
m68k_010b1a:
        lea.l 8(%pc),%a0
m68k_010b1a_end:
.org 0x10B1E
m68k_010b1e:
        nop
m68k_010b1e_end:
.org 0x10B20
m68k_010b20:
        adda.w %d3,%a0
m68k_010b20_end:
.org 0x10B22
m68k_010b22:
        rts
m68k_010b22_end:
.org 0x10C74
m68k_010c74:
        move.w %d7,%d6
m68k_010c74_end:
.org 0x10C76
m68k_010c76:
        andi.w #0x7fff,%d6
m68k_010c76_end:
.org 0x10C7A
m68k_010c7a:
        jsr 0x83d4:l
m68k_010c7a_end:
.org 0x10C80
m68k_010c80:
        andi.l #0xffff,%d0
m68k_010c80_end:
.org 0x10C86
m68k_010c86:
        mulu.w %d6,%d0
m68k_010c86_end:
.org 0x10C88
m68k_010c88:
        swap %d0
m68k_010c88_end:
.org 0x10C8A
m68k_010c8a:
        lsl.w #0x1,%d0
m68k_010c8a_end:
.org 0x10C8C
m68k_010c8c:
        lea.l 0xef24:w,%a1
m68k_010c8c_end:
.org 0x10C90
m68k_010c90:
        move.w (%a1, %d0.w),%d0
m68k_010c90_end:
.org 0x10C94
m68k_010c94:
        move.w %d0,0xf3f2:w
m68k_010c94_end:
.org 0x10C98
m68k_010c98:
        lsl.w #0x1,%d0
m68k_010c98_end:
.org 0x10C9A
m68k_010c9a:
        lea.l 0xb600:w,%a1
m68k_010c9a_end:
.org 0x10C9E
m68k_010c9e:
        move.w (%a1, %d0.w),%d0
m68k_010c9e_end:
.org 0x10CA2
m68k_010ca2:
        clr.w %d2
m68k_010ca2_end:
.org 0x10CA4
m68k_010ca4:
        cmpi.w #0x1e,%d0
m68k_010ca4_end:
.org 0x10CA8
m68k_010ca8:
        bls.b (. + 36)
m68k_010ca8_end:
.org 0x10CAA
m68k_010caa:
        addq.w #0x1,%d2
m68k_010caa_end:
.org 0x10CAC
m68k_010cac:
        cmpi.w #0x3c,%d0
m68k_010cac_end:
.org 0x10CB0
m68k_010cb0:
        bls.b (. + 28)
m68k_010cb0_end:
.org 0x10CB2
m68k_010cb2:
        addq.w #0x1,%d2
m68k_010cb2_end:
.org 0x10CB4
m68k_010cb4:
        cmpi.w #0x50,%d0
m68k_010cb4_end:
.org 0x10CB8
m68k_010cb8:
        bls.b (. + 20)
m68k_010cb8_end:
.org 0x10CBA
m68k_010cba:
        addq.w #0x1,%d2
m68k_010cba_end:
.org 0x10CBC
m68k_010cbc:
        cmpi.w #0x5a,%d0
m68k_010cbc_end:
.org 0x10CC0
m68k_010cc0:
        bls.b (. + 12)
m68k_010cc0_end:
.org 0x10CC2
m68k_010cc2:
        addq.w #0x1,%d2
m68k_010cc2_end:
.org 0x10CC4
m68k_010cc4:
        cmpi.w #0x64,%d0
m68k_010cc4_end:
.org 0x10CC8
m68k_010cc8:
        bls.b (. + 4)
m68k_010cc8_end:
.org 0x10CCA
m68k_010cca:
        addq.w #0x1,%d2
m68k_010cca_end:
.org 0x10CCC
m68k_010ccc:
        lsl.w #0x3,%d2
m68k_010ccc_end:
.org 0x10CCE
m68k_010cce:
        jsr 0x83d4:l
m68k_010cce_end:
.org 0x10CD4
m68k_010cd4:
        moveq #0,%d0
m68k_010cd4_end:
.org 0x10CD6
m68k_010cd6:
        move.w 0xf61c:w,%d0
m68k_010cd6_end:
.org 0x10CDA
m68k_010cda:
        lsl.l #0x2,%d0
m68k_010cda_end:
.org 0x10CDC
m68k_010cdc:
        swap %d0
m68k_010cdc_end:
.org 0x10CDE
m68k_010cde:
        lsl.w #0x1,%d0
m68k_010cde_end:
.org 0x10CE0
m68k_010ce0:
        add.w %d0,%d2
m68k_010ce0_end:
.org 0x10CE2
m68k_010ce2:
        move.w (%a0, %d2.w),%d0
m68k_010ce2_end:
.org 0x10CE6
m68k_010ce6:
        move.w 0xf376:w,%d2
m68k_010ce6_end:
.org 0x10CEA
m68k_010cea:
        cmp.w 0xf67a:w,%d2
m68k_010cea_end:
.org 0x10CEE
m68k_010cee:
        beq.w (. + 20)
m68k_010cee_end:
.org 0x10CF2
m68k_010cf2:
        cmp.w 0xf67c:w,%d2
m68k_010cf2_end:
.org 0x10CF6
m68k_010cf6:
        beq.w (. + 12)
m68k_010cf6_end:
.org 0x10CFA
m68k_010cfa:
        cmp.w 0xf67e:w,%d2
m68k_010cfa_end:
.org 0x10CFE
m68k_010cfe:
        bne.w (. + 12)
m68k_010cfe_end:
.org 0x10D02
m68k_010d02:
        move.w 8(%pc, %d0.w),%d0
m68k_010d02_end:
.org 0x10D06
m68k_010d06:
        jsr 12(%pc, %d0.w)
m68k_010d06_end:
.org 0x10D0A
m68k_010d0a:
        rts
m68k_010d0a_end:
.org 0x10D14
m68k_010d14:
        bsr.w (. + 254)
m68k_010d14_end:
.org 0x10D18
m68k_010d18:
        move.w #0x208,0xf612:w
m68k_010d18_end:
.org 0x10D1E
m68k_010d1e:
        move.w #0x20,0xf362:w
m68k_010d1e_end:
.org 0x10D24
m68k_010d24:
        move.w #0x4d,%d0
m68k_010d24_end:
.org 0x10D28
m68k_010d28:
        move.w 0xf3a6:w,0xf3d0:w
m68k_010d28_end:
.org 0x10D2E
m68k_010d2e:
        jsr 0x676f2:l
m68k_010d2e_end:
.org 0x10D34
m68k_010d34:
        rts
m68k_010d34_end:
.org 0x10D64
m68k_010d64:
        move.w 0xf392:w,%d0
m68k_010d64_end:
.org 0x10D68
m68k_010d68:
        move.w #0xffff,0xf630:w
m68k_010d68_end:
.org 0x10D6E
m68k_010d6e:
        jsr 0x5f48:l
m68k_010d6e_end:
.org 0x10D74
m68k_010d74:
        cmpi.w #0xa,%d3
m68k_010d74_end:
.org 0x10D78
m68k_010d78:
        bcc.b (. + -100)
m68k_010d78_end:
.org 0x10D7A
m68k_010d7a:
        bsr.w (. + 310)
m68k_010d7a_end:
.org 0x10D7E
m68k_010d7e:
        move.w #0x208,0xf612:w
m68k_010d7e_end:
.org 0x10D84
m68k_010d84:
        move.w #0x21,0xf362:w
m68k_010d84_end:
.org 0x10D8A
m68k_010d8a:
        move.w #0x4f,%d0
m68k_010d8a_end:
.org 0x10D8E
m68k_010d8e:
        move.w 0xf3a6:w,0xf3d0:w
m68k_010d8e_end:
.org 0x10D94
m68k_010d94:
        move.w 0xf3f2:w,0xf3d2:w
m68k_010d94_end:
.org 0x10D9A
m68k_010d9a:
        jsr 0x676f2:l
m68k_010d9a_end:
.org 0x10DA0
m68k_010da0:
        clr.w 0xf386:w
m68k_010da0_end:
.org 0x10DA4
m68k_010da4:
        clr.w 0xf384:w
m68k_010da4_end:
.org 0x10DA8
m68k_010da8:
        move.w 0xf3f2:w,0xf3a6:w
m68k_010da8_end:
.org 0x10DAE
m68k_010dae:
        clr.w 0xf64e:w
m68k_010dae_end:
.org 0x10DB2
m68k_010db2:
        rts
m68k_010db2_end:
.org 0x10DB4
m68k_010db4:
        move.w 0xf392:w,%d0
m68k_010db4_end:
.org 0x10DB8
m68k_010db8:
        lea.l 0xf45e:w,%a0
m68k_010db8_end:
.org 0x10DBC
m68k_010dbc:
        move.w %d0,%d1
m68k_010dbc_end:
.org 0x10DBE
m68k_010dbe:
        lsl.w #0x1,%d1
m68k_010dbe_end:
.org 0x10DC0
m68k_010dc0:
        move.w (%a0, %d1.w),0xf630:w
m68k_010dc0_end:
.org 0x10DC6
m68k_010dc6:
        jsr 0x5f48:l
m68k_010dc6_end:
.org 0x10DCC
m68k_010dcc:
        cmpi.w #0xa,%d3
m68k_010dcc_end:
.org 0x10DD0
m68k_010dd0:
        bcc.w (. + -188)
m68k_010dd0_end:
.org 0x10DD4
m68k_010dd4:
        bsr.w (. + 182)
m68k_010dd4_end:
.org 0x10DD8
m68k_010dd8:
        move.w #0x208,0xf612:w
m68k_010dd8_end:
.org 0x10DDE
m68k_010dde:
        move.w #0x21,0xf362:w
m68k_010dde_end:
.org 0x10DE4
m68k_010de4:
        move.w #0x4f,%d0
m68k_010de4_end:
.org 0x10DE8
m68k_010de8:
        move.w 0xf3a6:w,0xf3d0:w
m68k_010de8_end:
.org 0x10DEE
m68k_010dee:
        move.w 0xf3f2:w,0xf3d2:w
m68k_010dee_end:
.org 0x10DF4
m68k_010df4:
        jsr 0x676f2:l
m68k_010df4_end:
.org 0x10DFA
m68k_010dfa:
        move.w #0x1,0xf386:w
m68k_010dfa_end:
.org 0x10E00
m68k_010e00:
        clr.w 0xf384:w
m68k_010e00_end:
.org 0x10E04
m68k_010e04:
        move.w 0xf3f2:w,0xf3a6:w
m68k_010e04_end:
.org 0x10E0A
m68k_010e0a:
        move.w #0x1,0xf64e:w
m68k_010e0a_end:
.org 0x10E10
m68k_010e10:
        rts
m68k_010e10_end:
.org 0x10E12
m68k_010e12:
        jsr 0x83d4:l
m68k_010e12_end:
.org 0x10E18
m68k_010e18:
        moveq #0,%d0
m68k_010e18_end:
.org 0x10E1A
m68k_010e1a:
        move.w 0xf61c:w,%d0
m68k_010e1a_end:
.org 0x10E1E
m68k_010e1e:
        move.l %d0,%d1
m68k_010e1e_end:
.org 0x10E20
m68k_010e20:
        lsl.l #0x1,%d0
m68k_010e20_end:
.org 0x10E22
m68k_010e22:
        add.l %d1,%d0
m68k_010e22_end:
.org 0x10E24
m68k_010e24:
        swap %d0
m68k_010e24_end:
.org 0x10E26
m68k_010e26:
        addq.w #0x1,%d0
m68k_010e26_end:
.org 0x10E28
m68k_010e28:
        move.w 0xf3a6:w,%d1
m68k_010e28_end:
.org 0x10E2C
m68k_010e2c:
        lsl.w #0x1,%d1
m68k_010e2c_end:
.org 0x10E2E
m68k_010e2e:
        lea.l 0xc000:w,%a0
m68k_010e2e_end:
.org 0x10E32
m68k_010e32:
        add.w %d0,(%a0, %d1.w)
m68k_010e32_end:
.org 0x10E36
m68k_010e36:
        rts
m68k_010e36_end:
.org 0x10E8A
m68k_010e8a:
        jsr 0x83d4:l
m68k_010e8a_end:
.org 0x10E90
m68k_010e90:
        moveq #0,%d0
m68k_010e90_end:
.org 0x10E92
m68k_010e92:
        move.w 0xf61c:w,%d0
m68k_010e92_end:
.org 0x10E96
m68k_010e96:
        move.l %d0,%d1
m68k_010e96_end:
.org 0x10E98
m68k_010e98:
        lsl.l #0x2,%d0
m68k_010e98_end:
.org 0x10E9A
m68k_010e9a:
        add.l %d1,%d0
m68k_010e9a_end:
.org 0x10E9C
m68k_010e9c:
        swap %d0
m68k_010e9c_end:
.org 0x10E9E
m68k_010e9e:
        addq.w #0x1,%d0
m68k_010e9e_end:
.org 0x10EA0
m68k_010ea0:
        move.w 0xf3a6:w,%d1
m68k_010ea0_end:
.org 0x10EA4
m68k_010ea4:
        lsl.w #0x2,%d1
m68k_010ea4_end:
.org 0x10EA6
m68k_010ea6:
        lea.l 0xbe00:w,%a0
m68k_010ea6_end:
.org 0x10EAA
m68k_010eaa:
        add.w %d0,(%a0, %d1.w)
m68k_010eaa_end:
.org 0x10EAE
m68k_010eae:
        rts
m68k_010eae_end:
.org 0x10EB0
m68k_010eb0:
        jsr 0x83d4:l
m68k_010eb0_end:
.org 0x10EB6
m68k_010eb6:
        moveq #0,%d0
m68k_010eb6_end:
.org 0x10EB8
m68k_010eb8:
        move.w 0xf61c:w,%d0
m68k_010eb8_end:
.org 0x10EBC
m68k_010ebc:
        move.l %d0,%d1
m68k_010ebc_end:
.org 0x10EBE
m68k_010ebe:
        lsl.l #0x2,%d0
m68k_010ebe_end:
.org 0x10EC0
m68k_010ec0:
        add.l %d1,%d0
m68k_010ec0_end:
.org 0x10EC2
m68k_010ec2:
        swap %d0
m68k_010ec2_end:
.org 0x10EC4
m68k_010ec4:
        addq.w #0x5,%d0
m68k_010ec4_end:
.org 0x10EC6
m68k_010ec6:
        move.w 0xf3a6:w,%d1
m68k_010ec6_end:
.org 0x10ECA
m68k_010eca:
        lsl.w #0x1,%d1
m68k_010eca_end:
.org 0x10ECC
m68k_010ecc:
        lea.l 0xbe00:w,%a0
m68k_010ecc_end:
.org 0x10ED0
m68k_010ed0:
        add.w (%a0, %d1.w),%d0
m68k_010ed0_end:
.org 0x10ED4
m68k_010ed4:
        bcc.b (. + 6)
m68k_010ed4_end:
.org 0x10ED6
m68k_010ed6:
        move.w #0xffff,%d0
m68k_010ed6_end:
.org 0x10EDA
m68k_010eda:
        move.w %d0,(%a0, %d1.w)
m68k_010eda_end:
.org 0x10EDE
m68k_010ede:
        rts
m68k_010ede_end:
.org 0x1108C
m68k_01108c:
        movem.l %d2-%d5/%a0-%a3,-(%a7)
m68k_01108c_end:
.org 0x11090
m68k_011090:
        move.w 0xefe4:w,%d3
m68k_011090_end:
.org 0x11094
m68k_011094:
        lsl.w #0x2,%d3
m68k_011094_end:
.org 0x11096
m68k_011096:
        movea.l -24(%pc, %d3.w),%a6
m68k_011096_end:
.org 0x1109A
m68k_01109a:
        clr.w %d2
m68k_01109a_end:
.org 0x1109C
m68k_01109c:
        lea.l 0xcc00:w,%a1
m68k_01109c_end:
.org 0x110A0
m68k_0110a0:
        clr.w %d3
m68k_0110a0_end:
.org 0x110A2
m68k_0110a2:
        move.b (%a1, %d1.w),%d3
m68k_0110a2_end:
.org 0x110A6
m68k_0110a6:
        lea.l 0xf427:w,%a1
m68k_0110a6_end:
.org 0x110AA
m68k_0110aa:
        move.b (%a1, %d3.w),%d3
m68k_0110aa_end:
.org 0x110AE
m68k_0110ae:
        lea.l 0xef24:w,%a0
m68k_0110ae_end:
.org 0x110B2
m68k_0110b2:
        bsr.w (. + 28)
m68k_0110b2_end:
.org 0x110B6
m68k_0110b6:
        tst.w %d2
m68k_0110b6_end:
.org 0x110B8
m68k_0110b8:
        bmi.b (. + 10)
m68k_0110b8_end:
.org 0x110BA
m68k_0110ba:
        bsr.w (. + 104)
m68k_0110ba_end:
.org 0x110BE
m68k_0110be:
        bsr.w (. + 200)
m68k_0110be_end:
.org 0x110C2
m68k_0110c2:
        move.w #0xffff,(%a0)
m68k_0110c2_end:
.org 0x110C6
m68k_0110c6:
        move.w %d2,%d0
m68k_0110c6_end:
.org 0x110C8
m68k_0110c8:
        movem.l (%a7)+,%d2-%d5/%a0-%a3
m68k_0110c8_end:
.org 0x110CC
m68k_0110cc:
        rts
m68k_0110cc_end:
.org 0x110CE
m68k_0110ce:
        cmpi.w #0x1,%d3
m68k_0110ce_end:
.org 0x110D2
m68k_0110d2:
        beq.b (. + 24)
m68k_0110d2_end:
.org 0x110D4
m68k_0110d4:
        cmpi.w #0x5,%d3
m68k_0110d4_end:
.org 0x110D8
m68k_0110d8:
        beq.b (. + 22)
m68k_0110d8_end:
.org 0x110DA
m68k_0110da:
        cmpi.w #0xa,%d3
m68k_0110da_end:
.org 0x110DE
m68k_0110de:
        beq.b (. + 22)
m68k_0110de_end:
.org 0x110E0
m68k_0110e0:
        cmpi.w #0x2,%d3
m68k_0110e0_end:
.org 0x110E4
m68k_0110e4:
        beq.b (. + 22)
m68k_0110e4_end:
.org 0x110E6
m68k_0110e6:
        bra.w (. + 58)
m68k_0110e6_end:
.org 0x110EA
m68k_0110ea:
        movea.l (%a6),%a1
m68k_0110ea_end:
.org 0x110EC
m68k_0110ec:
        bra.b (. + 18)
m68k_0110ec_end:
.org 0x110EE
m68k_0110ee:
        movea.l 0x4(%a6),%a1
m68k_0110ee_end:
.org 0x110F2
m68k_0110f2:
        bra.b (. + 12)
m68k_0110f2_end:
.org 0x110F4
m68k_0110f4:
        movea.l 0x8(%a6),%a1
m68k_0110f4_end:
.org 0x110F8
m68k_0110f8:
        bra.b (. + 6)
m68k_0110f8_end:
.org 0x110FA
m68k_0110fa:
        movea.l 0xc(%a6),%a1
m68k_0110fa_end:
.org 0x110FE
m68k_0110fe:
        lea.l 0xcc00:w,%a2
m68k_0110fe_end:
.org 0x11102
m68k_011102:
        move.w (%a1)+,%d4
m68k_011102_end:
.org 0x11104
m68k_011104:
        bmi.b (. + 28)
m68k_011104_end:
.org 0x11106
m68k_011106:
        cmp.b 0xf374:w,%d4
m68k_011106_end:
.org 0x1110A
m68k_01110a:
        bhi.b (. + 18)
m68k_01110a_end:
.org 0x1110C
m68k_01110c:
        move.w (%a1),%d4
m68k_01110c_end:
.org 0x1110E
m68k_01110e:
        tst.b (%a2, %d4.w)
m68k_01110e_end:
.org 0x11112
m68k_011112:
        bne.b (. + 10)
m68k_011112_end:
.org 0x11114
m68k_011114:
        move.w %d4,(%a0)+
m68k_011114_end:
.org 0x11116
m68k_011116:
        ori.w #0x8000,%d2
m68k_011116_end:
.org 0x1111A
m68k_01111a:
        addq.w #0x1,%d2
m68k_01111a_end:
.org 0x1111C
m68k_01111c:
        addq.w #0x2,%a1
m68k_01111c_end:
.org 0x1111E
m68k_01111e:
        bra.b (. + -28)
m68k_01111e_end:
.org 0x11120
m68k_011120:
        rts
m68k_011120_end:
.org 0x11122
m68k_011122:
        movea.l 0x10(%a6),%a1
m68k_011122_end:
.org 0x11126
m68k_011126:
        move.w %d0,%d4
m68k_011126_end:
.org 0x11128
m68k_011128:
        lsl.w #0x1,%d4
m68k_011128_end:
.org 0x1112A
m68k_01112a:
        move.w (%a1, %d4.w),%d4
m68k_01112a_end:
.org 0x1112E
m68k_01112e:
        movea.l 0x14(%a6),%a1
m68k_01112e_end:
.org 0x11132
m68k_011132:
        adda.w %d4,%a1
m68k_011132_end:
.org 0x11134
m68k_011134:
        lea.l 0xcc00:w,%a2
m68k_011134_end:
.org 0x11138
m68k_011138:
        lea.l 0xf427:w,%a3
m68k_011138_end:
.org 0x1113C
m68k_01113c:
        move.w (%a1)+,%d4
m68k_01113c_end:
.org 0x1113E
m68k_01113e:
        bmi.b (. + 70)
m68k_01113e_end:
.org 0x11140
m68k_011140:
        cmp.b 0xf374:w,%d4
m68k_011140_end:
.org 0x11144
m68k_011144:
        bhi.b (. + 64)
m68k_011144_end:
.org 0x11146
m68k_011146:
        move.w (%a1)+,%d4
m68k_011146_end:
.org 0x11148
m68k_011148:
        bmi.b (. + 56)
m68k_011148_end:
.org 0x1114A
m68k_01114a:
        cmpi.w #0xde,%d4
m68k_01114a_end:
.org 0x1114E
m68k_01114e:
        bne.b (. + 10)
m68k_01114e_end:
.org 0x11150
m68k_011150:
        cmpi.b #0x5,0xf374:w
m68k_011150_end:
.org 0x11156
m68k_011156:
        bhi.b (. + 42)
m68k_011156_end:
.org 0x11158
m68k_011158:
        tst.b (%a2, %d4.w)
m68k_011158_end:
.org 0x1115C
m68k_01115c:
        bne.b (. + 36)
m68k_01115c_end:
.org 0x1115E
m68k_01115e:
        move.w (%a1),%d5
m68k_01115e_end:
.org 0x11160
m68k_011160:
        bmi.b (. + 28)
m68k_011160_end:
.org 0x11162
m68k_011162:
        btst.l #0xe,%d5
m68k_011162_end:
.org 0x11166
m68k_011166:
        bne.b (. + 18)
m68k_011166_end:
.org 0x11168
m68k_011168:
        move.b (%a2, %d5.w),%d5
m68k_011168_end:
.org 0x1116C
m68k_01116c:
        andi.w #0xff,%d5
m68k_01116c_end:
.org 0x11170
m68k_011170:
        cmp.b (%a3, %d5.w),%d3
m68k_011170_end:
.org 0x11174
m68k_011174:
        bne.b (. + 12)
m68k_011174_end:
.org 0x11176
m68k_011176:
        bra.b (. + 6)
m68k_011176_end:
.org 0x11178
m68k_011178:
        cmp.b %d3,%d5
m68k_011178_end:
.org 0x1117A
m68k_01117a:
        bne.b (. + 6)
m68k_01117a_end:
.org 0x1117C
m68k_01117c:
        move.w %d4,(%a0)+
m68k_01117c_end:
.org 0x1117E
m68k_01117e:
        addq.w #0x1,%d2
m68k_01117e_end:
.org 0x11180
m68k_011180:
        addq.w #0x2,%a1
m68k_011180_end:
.org 0x11182
m68k_011182:
        bra.b (. + -70)
m68k_011182_end:
.org 0x11184
m68k_011184:
        rts
m68k_011184_end:
.org 0x11186
m68k_011186:
        lea.l 0xcc00:w,%a1
m68k_011186_end:
.org 0x1118A
m68k_01118a:
        move.w #0xff,%d3
m68k_01118a_end:
.org 0x1118E
m68k_01118e:
        move.b (%a1, %d3.w),%d4
m68k_01118e_end:
.org 0x11192
m68k_011192:
        bpl.b (. + 14)
m68k_011192_end:
.org 0x11194
m68k_011194:
        andi.w #0x7f,%d4
m68k_011194_end:
.org 0x11198
m68k_011198:
        cmp.w %d0,%d4
m68k_011198_end:
.org 0x1119A
m68k_01119a:
        bne.b (. + 6)
m68k_01119a_end:
.org 0x1119C
m68k_01119c:
        move.w %d3,(%a0)+
m68k_01119c_end:
.org 0x1119E
m68k_01119e:
        addq.w #0x1,%d2
m68k_01119e_end:
.org 0x111A0
m68k_0111a0:
        dbra %d3,(. + -18)
m68k_0111a0_end:
.org 0x111A4
m68k_0111a4:
        rts
m68k_0111a4_end:
.org 0x111AC
m68k_0111ac:
        cmpi.b #0x4a,0xf57d:w
m68k_0111ac_end:
.org 0x111B2
m68k_0111b2:
        bne.b (. + 8)
m68k_0111b2_end:
.org 0x111B4
m68k_0111b4:
        bsr.w (. + 12)
m68k_0111b4_end:
.org 0x111B8
m68k_0111b8:
        bra.b (. + 6)
m68k_0111b8_end:
.org 0x111BA
m68k_0111ba:
        bsr.w (. + 1120)
m68k_0111ba_end:
.org 0x111BE
m68k_0111be:
        rts
m68k_0111be_end:
.org 0x111C0
m68k_0111c0:
        cmpi.w #0x77,0xf38c:w
m68k_0111c0_end:
.org 0x111C6
m68k_0111c6:
        beq.w (. + 302)
m68k_0111c6_end:
.org 0x111CA
m68k_0111ca:
        move.w 0xf392:w,%d0
m68k_0111ca_end:
.org 0x111CE
m68k_0111ce:
        lsl.w #0x2,%d0
m68k_0111ce_end:
.org 0x111D0
m68k_0111d0:
        lea.l 0xdffc:w,%a0
m68k_0111d0_end:
.org 0x111D4
m68k_0111d4:
        move.l 0xf39e:w,%d1
m68k_0111d4_end:
.org 0x111D8
m68k_0111d8:
        sub.l %d1,(%a0, %d0.w)
m68k_0111d8_end:
.org 0x111DC
m68k_0111dc:
        lea.l 0xe09c:w,%a0
m68k_0111dc_end:
.org 0x111E0
m68k_0111e0:
        move.l 0xf3ba:w,%d1
m68k_0111e0_end:
.org 0x111E4
m68k_0111e4:
        sub.l %d1,(%a0, %d0.w)
m68k_0111e4_end:
.org 0x111E8
m68k_0111e8:
        move.w 0xf3a8:w,%d0
m68k_0111e8_end:
.org 0x111EC
m68k_0111ec:
        lea.l 0xf427:w,%a0
m68k_0111ec_end:
.org 0x111F0
m68k_0111f0:
        clr.w %d1
m68k_0111f0_end:
.org 0x111F2
m68k_0111f2:
        move.b (%a0, %d0.w),%d1
m68k_0111f2_end:
.org 0x111F6
m68k_0111f6:
        lsl.w #0x1,%d1
m68k_0111f6_end:
.org 0x111F8
m68k_0111f8:
        lea.l 0xe640:w,%a0
m68k_0111f8_end:
.org 0x111FC
m68k_0111fc:
        move.w (%a0, %d1.w),%d0
m68k_0111fc_end:
.org 0x11200
m68k_011200:
        cmp.w 0xf3a6:w,%d0
m68k_011200_end:
.org 0x11204
m68k_011204:
        beq.w (. + 110)
m68k_011204_end:
.org 0x11208
m68k_011208:
        move.l 0xf39e:w,%d2
m68k_011208_end:
.org 0x1120C
m68k_01120c:
        add.l 0xf3ba:w,%d2
m68k_01120c_end:
.org 0x11210
m68k_011210:
        move.w 0xf392:w,%d0
m68k_011210_end:
.org 0x11214
m68k_011214:
        lea.l 0xf427:w,%a0
m68k_011214_end:
.org 0x11218
m68k_011218:
        move.b (%a0, %d0.w),%d0
m68k_011218_end:
.org 0x1121C
m68k_01121c:
        lsl.w #0x1,%d0
m68k_01121c_end:
.org 0x1121E
m68k_01121e:
        lea.l 0xe640:w,%a0
m68k_01121e_end:
.org 0x11222
m68k_011222:
        move.w (%a0, %d0.w),%d0
m68k_011222_end:
.org 0x11226
m68k_011226:
        lea.l 0xc200:w,%a0
m68k_011226_end:
.org 0x1122A
m68k_01122a:
        clr.w %d3
m68k_01122a_end:
.org 0x1122C
m68k_01122c:
        move.b (%a0, %d0.w),%d3
m68k_01122c_end:
.org 0x11230
m68k_011230:
        move.w %d2,%d0
m68k_011230_end:
.org 0x11232
m68k_011232:
        mulu.w %d3,%d0
m68k_011232_end:
.org 0x11234
m68k_011234:
        swap %d2
m68k_011234_end:
.org 0x11236
m68k_011236:
        mulu.w %d3,%d2
m68k_011236_end:
.org 0x11238
m68k_011238:
        swap %d2
m68k_011238_end:
.org 0x1123A
m68k_01123a:
        add.l %d0,%d2
m68k_01123a_end:
.org 0x1123C
m68k_01123c:
        move.w 0xf3a6:w,%d0
m68k_01123c_end:
.org 0x11240
m68k_011240:
        lea.l 0xc300:w,%a0
m68k_011240_end:
.org 0x11244
m68k_011244:
        clr.w %d3
m68k_011244_end:
.org 0x11246
m68k_011246:
        move.b (%a0, %d0.w),%d3
m68k_011246_end:
.org 0x1124A
m68k_01124a:
        mulu.w %d3,%d3
m68k_01124a_end:
.org 0x1124C
m68k_01124c:
        lea.l 0xc200:w,%a0
m68k_01124c_end:
.org 0x11250
m68k_011250:
        clr.w %d4
m68k_011250_end:
.org 0x11252
m68k_011252:
        move.b (%a0, %d0.w),%d4
m68k_011252_end:
.org 0x11256
m68k_011256:
        mulu.w %d4,%d3
m68k_011256_end:
.org 0x11258
m68k_011258:
        bsr.w (. + 186)
m68k_011258_end:
.org 0x1125C
m68k_01125c:
        move.w %d3,%d1
m68k_01125c_end:
.org 0x1125E
m68k_01125e:
        mulu.w %d0,%d1
m68k_01125e_end:
.org 0x11260
m68k_011260:
        swap %d3
m68k_011260_end:
.org 0x11262
m68k_011262:
        andi.l #0xffff,%d3
m68k_011262_end:
.org 0x11268
m68k_011268:
        mulu.w %d0,%d3
m68k_011268_end:
.org 0x1126A
m68k_01126a:
        swap %d3
m68k_01126a_end:
.org 0x1126C
m68k_01126c:
        add.l %d1,%d3
m68k_01126c_end:
.org 0x1126E
m68k_01126e:
        cmp.l %d3,%d2
m68k_01126e_end:
.org 0x11270
m68k_011270:
        bcc.b (. + 42)
m68k_011270_end:
.org 0x11272
m68k_011272:
        bsr.w (. + 330)
m68k_011272_end:
.org 0x11276
m68k_011276:
        bsr.w (. + 384)
m68k_011276_end:
.org 0x1127A
m68k_01127a:
        move.w #0x208,0xf612:w
m68k_01127a_end:
.org 0x11280
m68k_011280:
        move.w #0x20,0xf362:w
m68k_011280_end:
.org 0x11286
m68k_011286:
        move.w #0x5b,%d0
m68k_011286_end:
.org 0x1128A
m68k_01128a:
        move.w 0xf3a6:w,0xf3d0:w
m68k_01128a_end:
.org 0x11290
m68k_011290:
        jsr 0x676f2:l
m68k_011290_end:
.org 0x11296
m68k_011296:
        bra.w (. + 122)
m68k_011296_end:
.org 0x1129A
m68k_01129a:
        bsr.w (. + 404)
m68k_01129a_end:
.org 0x1129E
m68k_01129e:
        move.w 0xf3a6:w,%d0
m68k_01129e_end:
.org 0x112A2
m68k_0112a2:
        bsr.w (. + 452)
m68k_0112a2_end:
.org 0x112A6
m68k_0112a6:
        move.w #0x208,0xf612:w
m68k_0112a6_end:
.org 0x112AC
m68k_0112ac:
        move.w #0x28,0xf362:w
m68k_0112ac_end:
.org 0x112B2
m68k_0112b2:
        move.w #0x5a,0xf3fe:w
m68k_0112b2_end:
.org 0x112B8
m68k_0112b8:
        move.w 0xf3a6:w,0xf3d2:w
m68k_0112b8_end:
.org 0x112BE
m68k_0112be:
        move.w 0xf3f2:w,-(%a7)
m68k_0112be_end:
.org 0x112C2
m68k_0112c2:
        lea.l 0xe640:w,%a0
m68k_0112c2_end:
.org 0x112C6
m68k_0112c6:
        move.w 0xf376:w,%d0
m68k_0112c6_end:
.org 0x112CA
m68k_0112ca:
        lsl.w #0x1,%d0
m68k_0112ca_end:
.org 0x112CC
m68k_0112cc:
        move.w (%a0, %d0.w),0xf3f2:w
m68k_0112cc_end:
.org 0x112D2
m68k_0112d2:
        jsr 0x208ce:l
m68k_0112d2_end:
.org 0x112D8
m68k_0112d8:
        move.w (%a7)+,0xf3f2:w
m68k_0112d8_end:
.org 0x112DC
m68k_0112dc:
        move.w #0xe,0xff7026:l
m68k_0112dc_end:
.org 0x112E4
m68k_0112e4:
        clr.w 0xf386:w
m68k_0112e4_end:
.org 0x112E8
m68k_0112e8:
        clr.w 0xf384:w
m68k_0112e8_end:
.org 0x112EC
m68k_0112ec:
        clr.w 0xf64e:w
m68k_0112ec_end:
.org 0x112F0
m68k_0112f0:
        bra.w (. + 32)
m68k_0112f0_end:
.org 0x112F4
m68k_0112f4:
        move.w #0x208,0xf612:w
m68k_0112f4_end:
.org 0x112FA
m68k_0112fa:
        move.w #0x20,0xf362:w
m68k_0112fa_end:
.org 0x11300
m68k_011300:
        move.w #0x55,%d0
m68k_011300_end:
.org 0x11304
m68k_011304:
        jsr 0x676f2:l
m68k_011304_end:
.org 0x1130A
m68k_01130a:
        move.w #0x1,0xf652:w
m68k_01130a_end:
.org 0x11310
m68k_011310:
        rts
m68k_011310_end:
.org 0x11312
m68k_011312:
        jsr 0x83d4:l
m68k_011312_end:
.org 0x11318
m68k_011318:
        move.w 0xf3a6:w,%d0
m68k_011318_end:
.org 0x1131C
m68k_01131c:
        lea.l 0xc300:w,%a0
m68k_01131c_end:
.org 0x11320
m68k_011320:
        move.b (%a0, %d0.w),%d4
m68k_011320_end:
.org 0x11324
m68k_011324:
        clr.w %d1
m68k_011324_end:
.org 0x11326
m68k_011326:
        cmpi.b #0x1e,%d4
m68k_011326_end:
.org 0x1132A
m68k_01132a:
        bls.b (. + 36)
m68k_01132a_end:
.org 0x1132C
m68k_01132c:
        addq.w #0x1,%d1
m68k_01132c_end:
.org 0x1132E
m68k_01132e:
        cmpi.b #0x32,%d4
m68k_01132e_end:
.org 0x11332
m68k_011332:
        bls.b (. + 28)
m68k_011332_end:
.org 0x11334
m68k_011334:
        addq.w #0x1,%d1
m68k_011334_end:
.org 0x11336
m68k_011336:
        cmpi.b #0x46,%d4
m68k_011336_end:
.org 0x1133A
m68k_01133a:
        bls.b (. + 20)
m68k_01133a_end:
.org 0x1133C
m68k_01133c:
        addq.w #0x1,%d1
m68k_01133c_end:
.org 0x1133E
m68k_01133e:
        cmpi.b #0x50,%d4
m68k_01133e_end:
.org 0x11342
m68k_011342:
        bls.b (. + 12)
m68k_011342_end:
.org 0x11344
m68k_011344:
        addq.w #0x1,%d1
m68k_011344_end:
.org 0x11346
m68k_011346:
        cmpi.b #0x5a,%d4
m68k_011346_end:
.org 0x1134A
m68k_01134a:
        bls.b (. + 4)
m68k_01134a_end:
.org 0x1134C
m68k_01134c:
        addq.w #0x1,%d1
m68k_01134c_end:
.org 0x1134E
m68k_01134e:
        move.w %d1,%d4
m68k_01134e_end:
.org 0x11350
m68k_011350:
        lsl.w #0x2,%d4
m68k_011350_end:
.org 0x11352
m68k_011352:
        add.w %d4,%d1
m68k_011352_end:
.org 0x11354
m68k_011354:
        lea.l 0xc700:w,%a0
m68k_011354_end:
.org 0x11358
m68k_011358:
        move.b (%a0, %d0.w),%d4
m68k_011358_end:
.org 0x1135C
m68k_01135c:
        andi.w #0x7,%d4
m68k_01135c_end:
.org 0x11360
m68k_011360:
        add.w %d1,%d4
m68k_011360_end:
.org 0x11362
m68k_011362:
        lsl.w #0x1,%d4
m68k_011362_end:
.org 0x11364
m68k_011364:
        lea.l 26(%pc),%a0
m68k_011364_end:
.org 0x11368
m68k_011368:
        nop
m68k_011368_end:
.org 0x1136A
m68k_01136a:
        clr.w %d0
m68k_01136a_end:
.org 0x1136C
m68k_01136c:
        move.b (%a0, %d4.w),%d0
m68k_01136c_end:
.org 0x11370
m68k_011370:
        mulu.w 0xf61c:w,%d0
m68k_011370_end:
.org 0x11374
m68k_011374:
        swap %d0
m68k_011374_end:
.org 0x11376
m68k_011376:
        clr.w %d1
m68k_011376_end:
.org 0x11378
m68k_011378:
        move.b 0x1(%a0, %d4.w),%d1
m68k_011378_end:
.org 0x1137C
m68k_01137c:
        add.w %d1,%d0
m68k_01137c_end:
.org 0x1137E
m68k_01137e:
        rts
m68k_01137e_end:
.org 0x113BC
m68k_0113bc:
        jsr 0x83d4:l
m68k_0113bc_end:
.org 0x113C2
m68k_0113c2:
        andi.l #0xffff,%d0
m68k_0113c2_end:
.org 0x113C8
m68k_0113c8:
        move.l %d0,%d1
m68k_0113c8_end:
.org 0x113CA
m68k_0113ca:
        lsl.l #0x1,%d0
m68k_0113ca_end:
.org 0x113CC
m68k_0113cc:
        add.l %d1,%d0
m68k_0113cc_end:
.org 0x113CE
m68k_0113ce:
        add.l %d1,%d0
m68k_0113ce_end:
.org 0x113D0
m68k_0113d0:
        swap %d0
m68k_0113d0_end:
.org 0x113D2
m68k_0113d2:
        move.w 0xf376:w,%d1
m68k_0113d2_end:
.org 0x113D6
m68k_0113d6:
        lsl.w #0x1,%d1
m68k_0113d6_end:
.org 0x113D8
m68k_0113d8:
        lea.l 0xe640:w,%a0
m68k_0113d8_end:
.org 0x113DC
m68k_0113dc:
        move.w (%a0, %d1.w),%d1
m68k_0113dc_end:
.org 0x113E0
m68k_0113e0:
        clr.w %d2
m68k_0113e0_end:
.org 0x113E2
m68k_0113e2:
        lea.l 0xc200:w,%a0
m68k_0113e2_end:
.org 0x113E6
m68k_0113e6:
        move.b (%a0, %d1.w),%d2
m68k_0113e6_end:
.org 0x113EA
m68k_0113ea:
        mulu.w %d0,%d2
m68k_0113ea_end:
.org 0x113EC
m68k_0113ec:
        divu.w #0x64,%d2
m68k_0113ec_end:
.org 0x113F0
m68k_0113f0:
        sub.b %d2,(%a0, %d1.w)
m68k_0113f0_end:
.org 0x113F4
m68k_0113f4:
        rts
m68k_0113f4_end:
.org 0x113F6
m68k_0113f6:
        jsr 0x83d4:l
m68k_0113f6_end:
.org 0x113FC
m68k_0113fc:
        moveq #0,%d0
m68k_0113fc_end:
.org 0x113FE
m68k_0113fe:
        move.w 0xf61c:w,%d0
m68k_0113fe_end:
.org 0x11402
m68k_011402:
        move.l %d0,%d1
m68k_011402_end:
.org 0x11404
m68k_011404:
        lsl.l #0x1,%d0
m68k_011404_end:
.org 0x11406
m68k_011406:
        add.l %d1,%d0
m68k_011406_end:
.org 0x11408
m68k_011408:
        swap %d0
m68k_011408_end:
.org 0x1140A
m68k_01140a:
        addq.w #0x1,%d0
m68k_01140a_end:
.org 0x1140C
m68k_01140c:
        move.w 0xf376:w,%d1
m68k_01140c_end:
.org 0x11410
m68k_011410:
        lsl.w #0x1,%d1
m68k_011410_end:
.org 0x11412
m68k_011412:
        lea.l 0xe640:w,%a0
m68k_011412_end:
.org 0x11416
m68k_011416:
        move.w (%a0, %d1.w),%d1
m68k_011416_end:
.org 0x1141A
m68k_01141a:
        lsl.w #0x1,%d1
m68k_01141a_end:
.org 0x1141C
m68k_01141c:
        lea.l 0xbe00:w,%a0
m68k_01141c_end:
.org 0x11420
m68k_011420:
        add.w %d0,(%a0, %d1.w)
m68k_011420_end:
.org 0x11424
m68k_011424:
        bcc.b (. + 8)
m68k_011424_end:
.org 0x11426
m68k_011426:
        move.w #0xffff,(%a0, %d1.w)
m68k_011426_end:
.org 0x1142C
m68k_01142c:
        rts
m68k_01142c_end:
.org 0x1142E
m68k_01142e:
        jsr 0x83d4:l
m68k_01142e_end:
.org 0x11434
m68k_011434:
        andi.l #0xffff,%d0
m68k_011434_end:
.org 0x1143A
m68k_01143a:
        move.l %d0,%d1
m68k_01143a_end:
.org 0x1143C
m68k_01143c:
        lsl.l #0x2,%d0
m68k_01143c_end:
.org 0x1143E
m68k_01143e:
        add.l %d1,%d0
m68k_01143e_end:
.org 0x11440
m68k_011440:
        swap %d0
m68k_011440_end:
.org 0x11442
m68k_011442:
        addq.w #0x1,%d0
m68k_011442_end:
.org 0x11444
m68k_011444:
        move.w 0xf376:w,%d1
m68k_011444_end:
.org 0x11448
m68k_011448:
        lsl.w #0x1,%d1
m68k_011448_end:
.org 0x1144A
m68k_01144a:
        lea.l 0xe640:w,%a0
m68k_01144a_end:
.org 0x1144E
m68k_01144e:
        move.w (%a0, %d1.w),%d1
m68k_01144e_end:
.org 0x11452
m68k_011452:
        lsl.w #0x1,%d1
m68k_011452_end:
.org 0x11454
m68k_011454:
        lea.l 0xbe00:w,%a0
m68k_011454_end:
.org 0x11458
m68k_011458:
        add.w %d0,(%a0, %d1.w)
m68k_011458_end:
.org 0x1145C
m68k_01145c:
        bcc.b (. + 8)
m68k_01145c_end:
.org 0x1145E
m68k_01145e:
        move.w #0xffff,(%a0, %d1.w)
m68k_01145e_end:
.org 0x11464
m68k_011464:
        rts
m68k_011464_end:
.org 0x11466
m68k_011466:
        move.w 0xf3a8:w,%d1
m68k_011466_end:
.org 0x1146A
m68k_01146a:
        lsl.w #0x1,%d1
m68k_01146a_end:
.org 0x1146C
m68k_01146c:
        add.w 0xf3a8:w,%d1
m68k_01146c_end:
.org 0x11470
m68k_011470:
        lsl.w #0x2,%d1
m68k_011470_end:
.org 0x11472
m68k_011472:
        lea.l 0xe80c:w,%a0
m68k_011472_end:
.org 0x11476
m68k_011476:
        cmp.w (%a0, %d1.w),%d0
m68k_011476_end:
.org 0x1147A
m68k_01147a:
        bne.w (. + 14)
m68k_01147a_end:
.org 0x1147E
m68k_01147e:
        move.w #0xffff,(%a0, %d1.w)
m68k_01147e_end:
.org 0x11484
m68k_011484:
        bra.w (. + 36)
m68k_011484_end:
.org 0x11488
m68k_011488:
        cmp.w 0x4(%a0, %d1.w),%d0
m68k_011488_end:
.org 0x1148C
m68k_01148c:
        bne.w (. + 14)
m68k_01148c_end:
.org 0x11490
m68k_011490:
        move.w #0xffff,0x4(%a0, %d1.w)
m68k_011490_end:
.org 0x11496
m68k_011496:
        bra.w (. + 18)
m68k_011496_end:
.org 0x1149A
m68k_01149a:
        cmp.w 0x8(%a0, %d1.w),%d0
m68k_01149a_end:
.org 0x1149E
m68k_01149e:
        bne.w (. + 10)
m68k_01149e_end:
.org 0x114A2
m68k_0114a2:
        move.w #0xffff,0x8(%a0, %d1.w)
m68k_0114a2_end:
.org 0x114A8
m68k_0114a8:
        move.w 0xf3a8:w,%d1
m68k_0114a8_end:
.org 0x114AC
m68k_0114ac:
        lsl.w #0x1,%d1
m68k_0114ac_end:
.org 0x114AE
m68k_0114ae:
        lea.l 0xf45e:w,%a0
m68k_0114ae_end:
.org 0x114B2
m68k_0114b2:
        move.w (%a0, %d1.w),%d1
m68k_0114b2_end:
.org 0x114B6
m68k_0114b6:
        cmp.w %d0,%d1
m68k_0114b6_end:
.org 0x114B8
m68k_0114b8:
        beq.b (. + 14)
m68k_0114b8_end:
.org 0x114BA
m68k_0114ba:
        lea.l 0xcc00:w,%a0
m68k_0114ba_end:
.org 0x114BE
m68k_0114be:
        move.b 0xf393:w,(%a0, %d0.w)
m68k_0114be_end:
.org 0x114C4
m68k_0114c4:
        bra.b (. + 128)
m68k_0114c4_end:
.org 0x114C6
m68k_0114c6:
        move.w %d0,-(%a7)
m68k_0114c6_end:
.org 0x114C8
m68k_0114c8:
        move.w %d0,0xf630:w
m68k_0114c8_end:
.org 0x114CC
m68k_0114cc:
        move.w 0xf3a8:w,%d0
m68k_0114cc_end:
.org 0x114D0
m68k_0114d0:
        jsr 0x5f48:l
m68k_0114d0_end:
.org 0x114D6
m68k_0114d6:
        move.w (%a7)+,%d0
m68k_0114d6_end:
.org 0x114D8
m68k_0114d8:
        cmpi.w #0x1,%d3
m68k_0114d8_end:
.org 0x114DC
m68k_0114dc:
        beq.b (. + 70)
m68k_0114dc_end:
.org 0x114DE
m68k_0114de:
        lea.l 0xf500:w,%a0
m68k_0114de_end:
.org 0x114E2
m68k_0114e2:
        lea.l 0xc300:w,%a1
m68k_0114e2_end:
.org 0x114E6
m68k_0114e6:
        clr.w %d1
m68k_0114e6_end:
.org 0x114E8
m68k_0114e8:
        clr.w %d2
m68k_0114e8_end:
.org 0x114EA
m68k_0114ea:
        move.w (%a0)+,%d4
m68k_0114ea_end:
.org 0x114EC
m68k_0114ec:
        bmi.b (. + 10)
m68k_0114ec_end:
.org 0x114EE
m68k_0114ee:
        move.b (%a1, %d4.w),%d1
m68k_0114ee_end:
.org 0x114F2
m68k_0114f2:
        add.w %d1,%d2
m68k_0114f2_end:
.org 0x114F4
m68k_0114f4:
        bra.b (. + -10)
m68k_0114f4_end:
.org 0x114F6
m68k_0114f6:
        ext.l %d2
m68k_0114f6_end:
.org 0x114F8
m68k_0114f8:
        divu.w %d3,%d2
m68k_0114f8_end:
.org 0x114FA
m68k_0114fa:
        cmpi.w #0x23,%d2
m68k_0114fa_end:
.org 0x114FE
m68k_0114fe:
        bls.b (. + 36)
m68k_0114fe_end:
.org 0x11500
m68k_011500:
        lea.l 0xcc00:w,%a0
m68k_011500_end:
.org 0x11504
m68k_011504:
        move.b 0xf393:w,(%a0, %d0.w)
m68k_011504_end:
.org 0x1150A
m68k_01150a:
        move.w 0xf3a8:w,%d0
m68k_01150a_end:
.org 0x1150E
m68k_01150e:
        move.w #0xffff,0xf630:w
m68k_01150e_end:
.org 0x11514
m68k_011514:
        jsr 0x5f48:l
m68k_011514_end:
.org 0x1151A
m68k_01151a:
        jsr 0xe1f6:l
m68k_01151a_end:
.org 0x11520
m68k_011520:
        bra.b (. + 36)
m68k_011520_end:
.org 0x11522
m68k_011522:
        move.w 0xf3a8:w,%d0
m68k_011522_end:
.org 0x11526
m68k_011526:
        lea.l 0xf427:w,%a0
m68k_011526_end:
.org 0x1152A
m68k_01152a:
        move.b (%a0, %d0.w),%d1
m68k_01152a_end:
.org 0x1152E
m68k_01152e:
        move.b 0xf377:w,(%a0, %d0.w)
m68k_01152e_end:
.org 0x11534
m68k_011534:
        bsr.w (. + 84)
m68k_011534_end:
.org 0x11538
m68k_011538:
        bsr.w (. + 14)
m68k_011538_end:
.org 0x1153C
m68k_01153c:
        bsr.w (. + 40)
m68k_01153c_end:
.org 0x11540
m68k_011540:
        bsr.w (. + 124)
m68k_011540_end:
.org 0x11544
m68k_011544:
        rts
m68k_011544_end:
.org 0x1161A
m68k_01161a:
        cmpi.w #0x79,0xf38c:w
m68k_01161a_end:
.org 0x11620
m68k_011620:
        beq.w (. + 252)
m68k_011620_end:
.org 0x11624
m68k_011624:
        lea.l 0xcd00:w,%a0
m68k_011624_end:
.org 0x11628
m68k_011628:
        move.w 0xf3a6:w,%d0
m68k_011628_end:
.org 0x1162C
m68k_01162c:
        move.b #0x1,(%a0, %d0.w)
m68k_01162c_end:
.org 0x11632
m68k_011632:
        move.w 0xf3a8:w,%d0
m68k_011632_end:
.org 0x11636
m68k_011636:
        lea.l 0xf427:w,%a0
m68k_011636_end:
.org 0x1163A
m68k_01163a:
        clr.w %d1
m68k_01163a_end:
.org 0x1163C
m68k_01163c:
        move.b (%a0, %d0.w),%d1
m68k_01163c_end:
.org 0x11640
m68k_011640:
        lsl.w #0x1,%d1
m68k_011640_end:
.org 0x11642
m68k_011642:
        lea.l 0xe640:w,%a0
m68k_011642_end:
.org 0x11646
m68k_011646:
        move.w (%a0, %d1.w),%d0
m68k_011646_end:
.org 0x1164A
m68k_01164a:
        cmp.w 0xf3f2:w,%d0
m68k_01164a_end:
.org 0x1164E
m68k_01164e:
        beq.w (. + 12)
m68k_01164e_end:
.org 0x11652
m68k_011652:
        bsr.w (. + 232)
m68k_011652_end:
.org 0x11656
m68k_011656:
        cmp.l %d0,%d2
m68k_011656_end:
.org 0x11658
m68k_011658:
        bcc.b (. + 74)
m68k_011658_end:
.org 0x1165A
m68k_01165a:
        bsr.w (. + 538)
m68k_01165a_end:
.org 0x1165E
m68k_01165e:
        bsr.w (. + 630)
m68k_01165e_end:
.org 0x11662
m68k_011662:
        bsr.w (. + -678)
m68k_011662_end:
.org 0x11666
m68k_011666:
        move.w 0xf376:w,%d0
m68k_011666_end:
.org 0x1166A
m68k_01166a:
        cmp.w 0xf67a:w,%d0
m68k_01166a_end:
.org 0x1166E
m68k_01166e:
        beq.w (. + 20)
m68k_01166e_end:
.org 0x11672
m68k_011672:
        cmp.w 0xf67c:w,%d0
m68k_011672_end:
.org 0x11676
m68k_011676:
        beq.w (. + 12)
m68k_011676_end:
.org 0x1167A
m68k_01167a:
        cmp.w 0xf67e:w,%d0
m68k_01167a_end:
.org 0x1167E
m68k_01167e:
        bne.w (. + 186)
m68k_01167e_end:
.org 0x11682
m68k_011682:
        move.w #0x208,0xf612:w
m68k_011682_end:
.org 0x11688
m68k_011688:
        move.w #0x20,0xf362:w
m68k_011688_end:
.org 0x1168E
m68k_01168e:
        move.w #0x53,%d0
m68k_01168e_end:
.org 0x11692
m68k_011692:
        move.w 0xf3a6:w,0xf3d0:w
m68k_011692_end:
.org 0x11698
m68k_011698:
        jsr 0x676f2:l
m68k_011698_end:
.org 0x1169E
m68k_01169e:
        bra.w (. + 154)
m68k_01169e_end:
.org 0x116A2
m68k_0116a2:
        bsr.w (. + 512)
m68k_0116a2_end:
.org 0x116A6
m68k_0116a6:
        move.w 0xf3f2:w,%d0
m68k_0116a6_end:
.org 0x116AA
m68k_0116aa:
        bsr.w (. + -580)
m68k_0116aa_end:
.org 0x116AE
m68k_0116ae:
        move.w 0xf376:w,%d0
m68k_0116ae_end:
.org 0x116B2
m68k_0116b2:
        cmp.w 0xf67a:w,%d0
m68k_0116b2_end:
.org 0x116B6
m68k_0116b6:
        beq.w (. + 20)
m68k_0116b6_end:
.org 0x116BA
m68k_0116ba:
        cmp.w 0xf67c:w,%d0
m68k_0116ba_end:
.org 0x116BE
m68k_0116be:
        beq.w (. + 12)
m68k_0116be_end:
.org 0x116C2
m68k_0116c2:
        cmp.w 0xf67e:w,%d0
m68k_0116c2_end:
.org 0x116C6
m68k_0116c6:
        bne.w (. + 114)
m68k_0116c6_end:
.org 0x116CA
m68k_0116ca:
        move.w #0x208,0xf612:w
m68k_0116ca_end:
.org 0x116D0
m68k_0116d0:
        move.w #0x28,0xf362:w
m68k_0116d0_end:
.org 0x116D6
m68k_0116d6:
        move.w #0x5c,0xf3fe:w
m68k_0116d6_end:
.org 0x116DC
m68k_0116dc:
        move.w 0xf3f2:w,0xf3d2:w
m68k_0116dc_end:
.org 0x116E2
m68k_0116e2:
        move.w 0xf3a6:w,0xf3d0:w
m68k_0116e2_end:
.org 0x116E8
m68k_0116e8:
        move.w #0xc,0xff7026:l
m68k_0116e8_end:
.org 0x116F0
m68k_0116f0:
        clr.w 0xf386:w
m68k_0116f0_end:
.org 0x116F4
m68k_0116f4:
        clr.w 0xf384:w
m68k_0116f4_end:
.org 0x116F8
m68k_0116f8:
        move.w 0xf3f2:w,0xf3a6:w
m68k_0116f8_end:
.org 0x116FE
m68k_0116fe:
        clr.w 0xf64e:w
m68k_0116fe_end:
.org 0x11702
m68k_011702:
        lea.l 0xe640:w,%a0
m68k_011702_end:
.org 0x11706
m68k_011706:
        move.w 0xf376:w,%d0
m68k_011706_end:
.org 0x1170A
m68k_01170a:
        lsl.w #0x1,%d0
m68k_01170a_end:
.org 0x1170C
m68k_01170c:
        move.w (%a0, %d0.w),0xf3f2:w
m68k_01170c_end:
.org 0x11712
m68k_011712:
        jsr 0x208ce:l
m68k_011712_end:
.org 0x11718
m68k_011718:
        bra.w (. + 32)
m68k_011718_end:
.org 0x1171C
m68k_01171c:
        move.w #0x208,0xf612:w
m68k_01171c_end:
.org 0x11722
m68k_011722:
        move.w #0x20,0xf362:w
m68k_011722_end:
.org 0x11728
m68k_011728:
        move.w #0x55,%d0
m68k_011728_end:
.org 0x1172C
m68k_01172c:
        jsr 0x676f2:l
m68k_01172c_end:
.org 0x11732
m68k_011732:
        move.w #0x1,0xf652:w
m68k_011732_end:
.org 0x11738
m68k_011738:
        rts
m68k_011738_end:
.org 0x1173A
m68k_01173a:
        move.w 0xf3f2:w,%d0
m68k_01173a_end:
.org 0x1173E
m68k_01173e:
        lea.l 0xc300:w,%a0
m68k_01173e_end:
.org 0x11742
m68k_011742:
        clr.w %d1
m68k_011742_end:
.org 0x11744
m68k_011744:
        move.b (%a0, %d0.w),%d1
m68k_011744_end:
.org 0x11748
m68k_011748:
        move.w #0x64,%d2
m68k_011748_end:
.org 0x1174C
m68k_01174c:
        sub.w %d1,%d2
m68k_01174c_end:
.org 0x1174E
m68k_01174e:
        move.w 0xf376:w,%d0
m68k_01174e_end:
.org 0x11752
m68k_011752:
        lsl.w #0x1,%d0
m68k_011752_end:
.org 0x11754
m68k_011754:
        lea.l 0xe640:w,%a0
m68k_011754_end:
.org 0x11758
m68k_011758:
        move.w (%a0, %d0.w),%d0
m68k_011758_end:
.org 0x1175C
m68k_01175c:
        lea.l 0xc200:w,%a0
m68k_01175c_end:
.org 0x11760
m68k_011760:
        clr.w %d1
m68k_011760_end:
.org 0x11762
m68k_011762:
        move.b (%a0, %d0.w),%d1
m68k_011762_end:
.org 0x11766
m68k_011766:
        mulu.w %d1,%d2
m68k_011766_end:
.org 0x11768
m68k_011768:
        move.w 0xf3a6:w,%d0
m68k_011768_end:
.org 0x1176C
m68k_01176c:
        clr.w %d1
m68k_01176c_end:
.org 0x1176E
m68k_01176e:
        move.b (%a0, %d0.w),%d1
m68k_01176e_end:
.org 0x11772
m68k_011772:
        mulu.w %d1,%d2
m68k_011772_end:
.org 0x11774
m68k_011774:
        lsl.w #0x1,%d0
m68k_011774_end:
.org 0x11776
m68k_011776:
        lea.l 0xb600:w,%a0
m68k_011776_end:
.org 0x1177A
m68k_01177a:
        move.w (%a0, %d0.w),%d1
m68k_01177a_end:
.org 0x1177E
m68k_01177e:
        move.w %d2,%d0
m68k_01177e_end:
.org 0x11780
m68k_011780:
        mulu.w %d1,%d0
m68k_011780_end:
.org 0x11782
m68k_011782:
        swap %d2
m68k_011782_end:
.org 0x11784
m68k_011784:
        mulu.w %d1,%d2
m68k_011784_end:
.org 0x11786
m68k_011786:
        swap %d2
m68k_011786_end:
.org 0x11788
m68k_011788:
        add.l %d0,%d2
m68k_011788_end:
.org 0x1178A
m68k_01178a:
        bsr.w (. + 102)
m68k_01178a_end:
.org 0x1178E
m68k_01178e:
        move.w %d2,%d0
m68k_01178e_end:
.org 0x11790
m68k_011790:
        mulu.w %d1,%d0
m68k_011790_end:
.org 0x11792
m68k_011792:
        swap %d2
m68k_011792_end:
.org 0x11794
m68k_011794:
        mulu.w %d1,%d2
m68k_011794_end:
.org 0x11796
m68k_011796:
        swap %d2
m68k_011796_end:
.org 0x11798
m68k_011798:
        add.l %d0,%d2
m68k_011798_end:
.org 0x1179A
m68k_01179a:
        move.w 0xf3f2:w,%d0
m68k_01179a_end:
.org 0x1179E
m68k_01179e:
        lea.l 0xc200:w,%a0
m68k_01179e_end:
.org 0x117A2
m68k_0117a2:
        clr.w %d1
m68k_0117a2_end:
.org 0x117A4
m68k_0117a4:
        move.b (%a0, %d0.w),%d1
m68k_0117a4_end:
.org 0x117A8
m68k_0117a8:
        move.w 0xf3a8:w,%d3
m68k_0117a8_end:
.org 0x117AC
m68k_0117ac:
        lea.l 0xf427:w,%a1
m68k_0117ac_end:
.org 0x117B0
m68k_0117b0:
        clr.w %d4
m68k_0117b0_end:
.org 0x117B2
m68k_0117b2:
        move.b (%a1, %d3.w),%d4
m68k_0117b2_end:
.org 0x117B6
m68k_0117b6:
        lsl.w #0x1,%d4
m68k_0117b6_end:
.org 0x117B8
m68k_0117b8:
        lea.l 0xe640:w,%a1
m68k_0117b8_end:
.org 0x117BC
m68k_0117bc:
        move.w (%a1, %d4.w),%d4
m68k_0117bc_end:
.org 0x117C0
m68k_0117c0:
        clr.w %d3
m68k_0117c0_end:
.org 0x117C2
m68k_0117c2:
        move.b (%a0, %d4.w),%d3
m68k_0117c2_end:
.org 0x117C6
m68k_0117c6:
        mulu.w %d3,%d1
m68k_0117c6_end:
.org 0x117C8
m68k_0117c8:
        lsl.w #0x1,%d0
m68k_0117c8_end:
.org 0x117CA
m68k_0117ca:
        lea.l 0xb600:w,%a0
m68k_0117ca_end:
.org 0x117CE
m68k_0117ce:
        move.w (%a0, %d0.w),%d0
m68k_0117ce_end:
.org 0x117D2
m68k_0117d2:
        mulu.w %d0,%d1
m68k_0117d2_end:
.org 0x117D4
m68k_0117d4:
        move.w 0xefd2:w,%d3
m68k_0117d4_end:
.org 0x117D8
m68k_0117d8:
        lsl.w #0x1,%d3
m68k_0117d8_end:
.org 0x117DA
m68k_0117da:
        lea.l -1590(%pc),%a0
m68k_0117da_end:
.org 0x117DE
m68k_0117de:
        move.w (%a0, %d3.w),%d3
m68k_0117de_end:
.org 0x117E2
m68k_0117e2:
        move.w %d1,%d0
m68k_0117e2_end:
.org 0x117E4
m68k_0117e4:
        mulu.w %d3,%d0
m68k_0117e4_end:
.org 0x117E6
m68k_0117e6:
        swap %d1
m68k_0117e6_end:
.org 0x117E8
m68k_0117e8:
        mulu.w %d3,%d1
m68k_0117e8_end:
.org 0x117EA
m68k_0117ea:
        swap %d1
m68k_0117ea_end:
.org 0x117EC
m68k_0117ec:
        add.l %d1,%d0
m68k_0117ec_end:
.org 0x117EE
m68k_0117ee:
        rts
m68k_0117ee_end:
.org 0x117F0
m68k_0117f0:
        jsr 0x83d4:l
m68k_0117f0_end:
.org 0x117F6
m68k_0117f6:
        move.w 0xf3a6:w,%d0
m68k_0117f6_end:
.org 0x117FA
m68k_0117fa:
        move.w #0x4,%d1
m68k_0117fa_end:
.org 0x117FE
m68k_0117fe:
        lea.l 0xc700:w,%a0
m68k_0117fe_end:
.org 0x11802
m68k_011802:
        move.b (%a0, %d0.w),%d0
m68k_011802_end:
.org 0x11806
m68k_011806:
        andi.w #0x7,%d0
m68k_011806_end:
.org 0x1180A
m68k_01180a:
        sub.w %d0,%d1
m68k_01180a_end:
.org 0x1180C
m68k_01180c:
        move.w %d1,%d0
m68k_01180c_end:
.org 0x1180E
m68k_01180e:
        lsl.w #0x2,%d0
m68k_01180e_end:
.org 0x11810
m68k_011810:
        add.w %d1,%d0
m68k_011810_end:
.org 0x11812
m68k_011812:
        move.w 0xf3f2:w,%d1
m68k_011812_end:
.org 0x11816
m68k_011816:
        move.w #0x4,%d3
m68k_011816_end:
.org 0x1181A
m68k_01181a:
        move.b (%a0, %d1.w),%d4
m68k_01181a_end:
.org 0x1181E
m68k_01181e:
        andi.w #0x7,%d4
m68k_01181e_end:
.org 0x11822
m68k_011822:
        sub.b %d4,%d3
m68k_011822_end:
.org 0x11824
m68k_011824:
        add.w %d3,%d0
m68k_011824_end:
.org 0x11826
m68k_011826:
        lsl.w #0x1,%d0
m68k_011826_end:
.org 0x11828
m68k_011828:
        lea.l 24(%pc),%a1
m68k_011828_end:
.org 0x1182C
m68k_01182c:
        clr.w %d1
m68k_01182c_end:
.org 0x1182E
m68k_01182e:
        move.b (%a1, %d0.w),%d1
m68k_01182e_end:
.org 0x11832
m68k_011832:
        mulu.w 0xf61c:w,%d1
m68k_011832_end:
.org 0x11836
m68k_011836:
        swap %d1
m68k_011836_end:
.org 0x11838
m68k_011838:
        clr.w %d3
m68k_011838_end:
.org 0x1183A
m68k_01183a:
        move.b 0x1(%a1, %d0.w),%d3
m68k_01183a_end:
.org 0x1183E
m68k_01183e:
        add.w %d3,%d1
m68k_01183e_end:
.org 0x11840
m68k_011840:
        rts
m68k_011840_end:
.org 0x11874
m68k_011874:
        jsr 0x83d4:l
m68k_011874_end:
.org 0x1187A
m68k_01187a:
        moveq #0,%d0
m68k_01187a_end:
.org 0x1187C
m68k_01187c:
        move.w 0xf61c:w,%d0
m68k_01187c_end:
.org 0x11880
m68k_011880:
        move.l %d0,%d1
m68k_011880_end:
.org 0x11882
m68k_011882:
        lsl.l #0x1,%d0
m68k_011882_end:
.org 0x11884
m68k_011884:
        add.l %d1,%d0
m68k_011884_end:
.org 0x11886
m68k_011886:
        swap %d0
m68k_011886_end:
.org 0x11888
m68k_011888:
        addq.w #0x1,%d0
m68k_011888_end:
.org 0x1188A
m68k_01188a:
        move.w 0xf3a6:w,%d1
m68k_01188a_end:
.org 0x1188E
m68k_01188e:
        lsl.w #0x1,%d1
m68k_01188e_end:
.org 0x11890
m68k_011890:
        lea.l 0xbe00:w,%a0
m68k_011890_end:
.org 0x11894
m68k_011894:
        add.w %d0,(%a0, %d1.w)
m68k_011894_end:
.org 0x11898
m68k_011898:
        bcc.b (. + 8)
m68k_011898_end:
.org 0x1189A
m68k_01189a:
        move.w #0xffff,(%a0, %d1.w)
m68k_01189a_end:
.org 0x118A0
m68k_0118a0:
        rts
m68k_0118a0_end:
.org 0x118A2
m68k_0118a2:
        jsr 0x83d4:l
m68k_0118a2_end:
.org 0x118A8
m68k_0118a8:
        andi.l #0xffff,%d0
m68k_0118a8_end:
.org 0x118AE
m68k_0118ae:
        move.l %d0,%d1
m68k_0118ae_end:
.org 0x118B0
m68k_0118b0:
        lsl.l #0x1,%d0
m68k_0118b0_end:
.org 0x118B2
m68k_0118b2:
        add.l %d1,%d0
m68k_0118b2_end:
.org 0x118B4
m68k_0118b4:
        lsl.l #0x1,%d0
m68k_0118b4_end:
.org 0x118B6
m68k_0118b6:
        swap %d0
m68k_0118b6_end:
.org 0x118B8
m68k_0118b8:
        addi.w #0x5,%d0
m68k_0118b8_end:
.org 0x118BC
m68k_0118bc:
        move.w 0xf3a6:w,%d1
m68k_0118bc_end:
.org 0x118C0
m68k_0118c0:
        lsl.w #0x1,%d1
m68k_0118c0_end:
.org 0x118C2
m68k_0118c2:
        lea.l 0xbe00:w,%a0
m68k_0118c2_end:
.org 0x118C6
m68k_0118c6:
        add.w %d0,(%a0, %d1.w)
m68k_0118c6_end:
.org 0x118CA
m68k_0118ca:
        bcc.b (. + 8)
m68k_0118ca_end:
.org 0x118CC
m68k_0118cc:
        move.w #0xffff,(%a0, %d1.w)
m68k_0118cc_end:
.org 0x118D2
m68k_0118d2:
        rts
m68k_0118d2_end:
.org 0x118D4
m68k_0118d4:
        jsr 0x83d4:l
m68k_0118d4_end:
.org 0x118DA
m68k_0118da:
        andi.l #0xffff,%d0
m68k_0118da_end:
.org 0x118E0
m68k_0118e0:
        move.l %d0,%d1
m68k_0118e0_end:
.org 0x118E2
m68k_0118e2:
        lsl.l #0x2,%d0
m68k_0118e2_end:
.org 0x118E4
m68k_0118e4:
        add.l %d1,%d0
m68k_0118e4_end:
.org 0x118E6
m68k_0118e6:
        lsl.l #0x1,%d0
m68k_0118e6_end:
.org 0x118E8
m68k_0118e8:
        add.l %d1,%d0
m68k_0118e8_end:
.org 0x118EA
m68k_0118ea:
        swap %d0
m68k_0118ea_end:
.org 0x118EC
m68k_0118ec:
        lea.l 0xc200:w,%a0
m68k_0118ec_end:
.org 0x118F0
m68k_0118f0:
        clr.w %d1
m68k_0118f0_end:
.org 0x118F2
m68k_0118f2:
        move.w 0xf3a6:w,%d2
m68k_0118f2_end:
.org 0x118F6
m68k_0118f6:
        move.b (%a0, %d2.w),%d1
m68k_0118f6_end:
.org 0x118FA
m68k_0118fa:
        mulu.w %d0,%d1
m68k_0118fa_end:
.org 0x118FC
m68k_0118fc:
        divu.w #0x64,%d1
m68k_0118fc_end:
.org 0x11900
m68k_011900:
        sub.b %d1,(%a0, %d2.w)
m68k_011900_end:
.org 0x11904
m68k_011904:
        bcc.w (. + 8)
m68k_011904_end:
.org 0x11908
m68k_011908:
        clr.b (%a0, %d2.w)
m68k_011908_end:
.org 0x1190C
m68k_01190c:
        rts
m68k_01190c_end:
.org 0x1190E
m68k_01190e:
        bsr.w (. + 156)
m68k_01190e_end:
.org 0x11912
m68k_011912:
        bsr.w (. + 952)
m68k_011912_end:
.org 0x11916
m68k_011916:
        lea.l 0xd300:w,%a1
m68k_011916_end:
.org 0x1191A
m68k_01191a:
        move.w #0x1f,%d3
m68k_01191a_end:
.org 0x1191E
m68k_01191e:
        move.l #0x11111111,(%a1)+
m68k_01191e_end:
.org 0x11924
m68k_011924:
        dbra %d3,(. + -6)
m68k_011924_end:
.org 0x11928
m68k_011928:
        lea.l 122(%pc),%a0
m68k_011928_end:
.org 0x1192C
m68k_01192c:
        nop
m68k_01192c_end:
.org 0x1192E
m68k_01192e:
        move.w #0x1,%d0
m68k_01192e_end:
.org 0x11932
m68k_011932:
        move.w #0x3,%d1
m68k_011932_end:
.org 0x11936
m68k_011936:
        move.w #0x2,%d3
m68k_011936_end:
.org 0x1193A
m68k_01193a:
        jsr 0xae8a:l
m68k_01193a_end:
.org 0x11940
m68k_011940:
        move.l #0x40200000,0xc00004:l
m68k_011940_end:
.org 0x1194A
m68k_01194a:
        lea.l 0xd300:w,%a1
m68k_01194a_end:
.org 0x1194E
m68k_01194e:
        move.w #0x7f,%d3
m68k_01194e_end:
.org 0x11952
m68k_011952:
        move.l (%a1)+,0xc00000:l
m68k_011952_end:
.org 0x11958
m68k_011958:
        dbra %d3,(. + -6)
m68k_011958_end:
.org 0x1195C
m68k_01195c:
        jsr 0x55b0:l
m68k_01195c_end:
.org 0x11962
m68k_011962:
        move.w #0xc,0xf362:w
m68k_011962_end:
.org 0x11968
m68k_011968:
        jsr 0x30a74:l
m68k_011968_end:
.org 0x1196E
m68k_01196e:
        tst.w 0xf386:w
m68k_01196e_end:
.org 0x11972
m68k_011972:
        bne.w (. + 10)
m68k_011972_end:
.org 0x11976
m68k_011976:
        jsr 0x83fa:l
m68k_011976_end:
.org 0x1197C
m68k_01197c:
        move.w #0x208,0xf612:w
m68k_01197c_end:
.org 0x11982
m68k_011982:
        move.w #0x13,0xf362:w
m68k_011982_end:
.org 0x11988
m68k_011988:
        clr.w 0xf36a:w
m68k_011988_end:
.org 0x1198C
m68k_01198c:
        move.w #0x20a,0xf3c2:w
m68k_01198c_end:
.org 0x11992
m68k_011992:
        clr.w 0xf3c4:w
m68k_011992_end:
.org 0x11996
m68k_011996:
        clr.w 0xcea0:w
m68k_011996_end:
.org 0x1199A
m68k_01199a:
        move.w #0xffff,0xff3000:l
m68k_01199a_end:
.org 0x119A2
m68k_0119a2:
        rts
m68k_0119a2_end:
.org 0x119AA
m68k_0119aa:
        clr.w 0xf364:w
m68k_0119aa_end:
.org 0x119AE
m68k_0119ae:
        lea.l 0xcc00:w,%a6
m68k_0119ae_end:
.org 0x119B2
m68k_0119b2:
        lea.l 0xcd00:w,%a5
m68k_0119b2_end:
.org 0x119B6
m68k_0119b6:
        addq.w #0x1,0xf364:w
m68k_0119b6_end:
.org 0x119BA
m68k_0119ba:
        bsr.w (. + 22)
m68k_0119ba_end:
.org 0x119BE
m68k_0119be:
        bsr.w (. + 234)
m68k_0119be_end:
.org 0x119C2
m68k_0119c2:
        bsr.w (. + 516)
m68k_0119c2_end:
.org 0x119C6
m68k_0119c6:
        cmpi.w #0x28,0xf364:w
m68k_0119c6_end:
.org 0x119CC
m68k_0119cc:
        bcs.b (. + -22)
m68k_0119cc_end:
.org 0x119CE
m68k_0119ce:
        rts
m68k_0119ce_end:
.org 0x119D0
m68k_0119d0:
        move.w 0xf364:w,%d0
m68k_0119d0_end:
.org 0x119D4
m68k_0119d4:
        lsl.w #0x1,%d0
m68k_0119d4_end:
.org 0x119D6
m68k_0119d6:
        add.w 0xf364:w,%d0
m68k_0119d6_end:
.org 0x119DA
m68k_0119da:
        lsl.w #0x2,%d0
m68k_0119da_end:
.org 0x119DC
m68k_0119dc:
        lea.l 0xe80c:w,%a0
m68k_0119dc_end:
.org 0x119E0
m68k_0119e0:
        movem.w (%a0, %d0.w),%d2-%d3
m68k_0119e0_end:
.org 0x119E6
m68k_0119e6:
        tst.w %d2
m68k_0119e6_end:
.org 0x119E8
m68k_0119e8:
        bmi.w (. + 166)
m68k_0119e8_end:
.org 0x119EC
m68k_0119ec:
        move.b (%a6, %d2.w),%d4
m68k_0119ec_end:
.org 0x119F0
m68k_0119f0:
        cmp.b 0xf365:w,%d4
m68k_0119f0_end:
.org 0x119F4
m68k_0119f4:
        bne.w (. + 168)
m68k_0119f4_end:
.org 0x119F8
m68k_0119f8:
        move.w 0xf364:w,%d1
m68k_0119f8_end:
.org 0x119FC
m68k_0119fc:
        lsl.w #0x2,%d1
m68k_0119fc_end:
.org 0x119FE
m68k_0119fe:
        lea.l 0xdffc:w,%a1
m68k_0119fe_end:
.org 0x11A02
m68k_011a02:
        move.l (%a1, %d1.w),%d4
m68k_011a02_end:
.org 0x11A06
m68k_011a06:
        sub.l %d3,%d4
m68k_011a06_end:
.org 0x11A08
m68k_011a08:
        bcs.w (. + 136)
m68k_011a08_end:
.org 0x11A0C
m68k_011a0c:
        move.l %d4,(%a1, %d1.w)
m68k_011a0c_end:
.org 0x11A10
m68k_011a10:
        move.l %d3,%d4
m68k_011a10_end:
.org 0x11A12
m68k_011a12:
        divu.w #0x5,%d4
m68k_011a12_end:
.org 0x11A16
m68k_011a16:
        move.w %d2,%d1
m68k_011a16_end:
.org 0x11A18
m68k_011a18:
        lsl.w #0x1,%d1
m68k_011a18_end:
.org 0x11A1A
m68k_011a1a:
        lea.l 0xb600:w,%a0
m68k_011a1a_end:
.org 0x11A1E
m68k_011a1e:
        add.w (%a0, %d1.w),%d4
m68k_011a1e_end:
.org 0x11A22
m68k_011a22:
        lea.l 0xbe00:w,%a0
m68k_011a22_end:
.org 0x11A26
m68k_011a26:
        move.w (%a0, %d1.w),%d1
m68k_011a26_end:
.org 0x11A2A
m68k_011a2a:
        lsr.w #0x1,%d1
m68k_011a2a_end:
.org 0x11A2C
m68k_011a2c:
        add.w %d1,%d4
m68k_011a2c_end:
.org 0x11A2E
m68k_011a2e:
        jsr 0x83d4:l
m68k_011a2e_end:
.org 0x11A34
m68k_011a34:
        andi.l #0xffff,%d0
m68k_011a34_end:
.org 0x11A3A
m68k_011a3a:
        move.l %d0,%d1
m68k_011a3a_end:
.org 0x11A3C
m68k_011a3c:
        lsl.l #0x1,%d0
m68k_011a3c_end:
.org 0x11A3E
m68k_011a3e:
        add.l %d1,%d0
m68k_011a3e_end:
.org 0x11A40
m68k_011a40:
        lsl.l #0x1,%d0
m68k_011a40_end:
.org 0x11A42
m68k_011a42:
        swap %d0
m68k_011a42_end:
.org 0x11A44
m68k_011a44:
        addi.w #0xa,%d0
m68k_011a44_end:
.org 0x11A48
m68k_011a48:
        mulu.w %d0,%d4
m68k_011a48_end:
.org 0x11A4A
m68k_011a4a:
        divu.w #0x3e8,%d4
m68k_011a4a_end:
.org 0x11A4E
m68k_011a4e:
        ext.l %d4
m68k_011a4e_end:
.org 0x11A50
m68k_011a50:
        move.w 0xf364:w,%d1
m68k_011a50_end:
.org 0x11A54
m68k_011a54:
        lsl.w #0x2,%d1
m68k_011a54_end:
.org 0x11A56
m68k_011a56:
        lea.l 0xe1dc:w,%a0
m68k_011a56_end:
.org 0x11A5A
m68k_011a5a:
        move.l (%a0, %d1.w),%d3
m68k_011a5a_end:
.org 0x11A5E
m68k_011a5e:
        add.l %d4,%d3
m68k_011a5e_end:
.org 0x11A60
m68k_011a60:
        cmpi.l #0x3e7,%d3
m68k_011a60_end:
.org 0x11A66
m68k_011a66:
        bls.w (. + 8)
m68k_011a66_end:
.org 0x11A6A
m68k_011a6a:
        move.w #0x3e7,%d3
m68k_011a6a_end:
.org 0x11A6E
m68k_011a6e:
        move.l %d3,(%a0, %d1.w)
m68k_011a6e_end:
.org 0x11A72
m68k_011a72:
        lsl.l #0x1,%d2
m68k_011a72_end:
.org 0x11A74
m68k_011a74:
        lea.l 0xbe00:w,%a0
m68k_011a74_end:
.org 0x11A78
m68k_011a78:
        move.w (%a0, %d2.w),%d0
m68k_011a78_end:
.org 0x11A7C
m68k_011a7c:
        add.w %d4,%d0
m68k_011a7c_end:
.org 0x11A7E
m68k_011a7e:
        cmpi.w #0x3e7,%d0
m68k_011a7e_end:
.org 0x11A82
m68k_011a82:
        bls.w (. + 8)
m68k_011a82_end:
.org 0x11A86
m68k_011a86:
        move.w #0x3e7,%d0
m68k_011a86_end:
.org 0x11A8A
m68k_011a8a:
        move.w %d0,(%a0, %d2.w)
m68k_011a8a_end:
.org 0x11A8E
m68k_011a8e:
        rts
m68k_011a8e_end:
.org 0x11A90
m68k_011a90:
        move.w #0xffff,(%a0, %d0.w)
m68k_011a90_end:
.org 0x11A96
m68k_011a96:
        clr.b (%a5, %d2.w)
m68k_011a96_end:
.org 0x11A9A
m68k_011a9a:
        bra.b (. + -12)
m68k_011a9a_end:
.org 0x11A9C
m68k_011a9c:
        move.w #0xffff,(%a0, %d0.w)
m68k_011a9c_end:
.org 0x11AA2
m68k_011aa2:
        clr.b (%a5, %d2.w)
m68k_011aa2_end:
.org 0x11AA6
m68k_011aa6:
        bra.b (. + -24)
m68k_011aa6_end:
.org 0x11AA8
m68k_011aa8:
        move.w 0xf364:w,%d0
m68k_011aa8_end:
.org 0x11AAC
m68k_011aac:
        lsl.w #0x1,%d0
m68k_011aac_end:
.org 0x11AAE
m68k_011aae:
        add.w 0xf364:w,%d0
m68k_011aae_end:
.org 0x11AB2
m68k_011ab2:
        lsl.w #0x2,%d0
m68k_011ab2_end:
.org 0x11AB4
m68k_011ab4:
        lea.l 0xe810:w,%a0
m68k_011ab4_end:
.org 0x11AB8
m68k_011ab8:
        movem.w (%a0, %d0.w),%d2-%d3
m68k_011ab8_end:
.org 0x11ABE
m68k_011abe:
        tst.w %d2
m68k_011abe_end:
.org 0x11AC0
m68k_011ac0:
        bmi.w (. + 236)
m68k_011ac0_end:
.org 0x11AC4
m68k_011ac4:
        move.b (%a6, %d2.w),%d4
m68k_011ac4_end:
.org 0x11AC8
m68k_011ac8:
        cmp.b 0xf365:w,%d4
m68k_011ac8_end:
.org 0x11ACC
m68k_011acc:
        bne.w (. + 238)
m68k_011acc_end:
.org 0x11AD0
m68k_011ad0:
        move.w 0xf364:w,%d1
m68k_011ad0_end:
.org 0x11AD4
m68k_011ad4:
        lsl.w #0x2,%d1
m68k_011ad4_end:
.org 0x11AD6
m68k_011ad6:
        lea.l 0xdffc:w,%a1
m68k_011ad6_end:
.org 0x11ADA
m68k_011ada:
        move.l (%a1, %d1.w),%d4
m68k_011ada_end:
.org 0x11ADE
m68k_011ade:
        sub.l %d3,%d4
m68k_011ade_end:
.org 0x11AE0
m68k_011ae0:
        bcs.w (. + 206)
m68k_011ae0_end:
.org 0x11AE4
m68k_011ae4:
        move.l %d4,(%a1, %d1.w)
m68k_011ae4_end:
.org 0x11AE8
m68k_011ae8:
        move.l %d3,%d4
m68k_011ae8_end:
.org 0x11AEA
m68k_011aea:
        divu.w #0x5,%d4
m68k_011aea_end:
.org 0x11AEE
m68k_011aee:
        move.w %d2,%d1
m68k_011aee_end:
.org 0x11AF0
m68k_011af0:
        lsl.w #0x1,%d1
m68k_011af0_end:
.org 0x11AF2
m68k_011af2:
        lea.l 0xb600:w,%a0
m68k_011af2_end:
.org 0x11AF6
m68k_011af6:
        add.w (%a0, %d1.w),%d4
m68k_011af6_end:
.org 0x11AFA
m68k_011afa:
        lea.l 0xbe00:w,%a0
m68k_011afa_end:
.org 0x11AFE
m68k_011afe:
        move.w (%a0, %d1.w),%d1
m68k_011afe_end:
.org 0x11B02
m68k_011b02:
        lsr.w #0x1,%d1
m68k_011b02_end:
.org 0x11B04
m68k_011b04:
        add.w %d1,%d4
m68k_011b04_end:
.org 0x11B06
m68k_011b06:
        jsr 0x83d4:l
m68k_011b06_end:
.org 0x11B0C
m68k_011b0c:
        andi.l #0xffff,%d0
m68k_011b0c_end:
.org 0x11B12
m68k_011b12:
        lsl.l #0x2,%d0
m68k_011b12_end:
.org 0x11B14
m68k_011b14:
        swap %d0
m68k_011b14_end:
.org 0x11B16
m68k_011b16:
        move.w #0x8,%d5
m68k_011b16_end:
.org 0x11B1A
m68k_011b1a:
        move.w 0xf364:w,%d6
m68k_011b1a_end:
.org 0x11B1E
m68k_011b1e:
        lsl.w #0x2,%d6
m68k_011b1e_end:
.org 0x11B20
m68k_011b20:
        lea.l 0xe31c:w,%a1
m68k_011b20_end:
.org 0x11B24
m68k_011b24:
        cmpi.l #0x50,(%a1, %d6.w)
m68k_011b24_end:
.org 0x11B2C
m68k_011b2c:
        bcs.b (. + 6)
m68k_011b2c_end:
.org 0x11B2E
m68k_011b2e:
        move.w #0x2,%d5
m68k_011b2e_end:
.org 0x11B32
m68k_011b32:
        add.w %d5,%d0
m68k_011b32_end:
.org 0x11B34
m68k_011b34:
        mulu.w %d0,%d4
m68k_011b34_end:
.org 0x11B36
m68k_011b36:
        lea.l 0xc200:w,%a0
m68k_011b36_end:
.org 0x11B3A
m68k_011b3a:
        clr.w %d0
m68k_011b3a_end:
.org 0x11B3C
m68k_011b3c:
        move.b (%a0, %d2.w),%d0
m68k_011b3c_end:
.org 0x11B40
m68k_011b40:
        move.w %d4,%d1
m68k_011b40_end:
.org 0x11B42
m68k_011b42:
        mulu.w %d0,%d1
m68k_011b42_end:
.org 0x11B44
m68k_011b44:
        swap %d4
m68k_011b44_end:
.org 0x11B46
m68k_011b46:
        mulu.w %d0,%d4
m68k_011b46_end:
.org 0x11B48
m68k_011b48:
        swap %d4
m68k_011b48_end:
.org 0x11B4A
m68k_011b4a:
        add.l %d1,%d4
m68k_011b4a_end:
.org 0x11B4C
m68k_011b4c:
        divu.w #0xea60,%d4
m68k_011b4c_end:
.org 0x11B50
m68k_011b50:
        ext.l %d4
m68k_011b50_end:
.org 0x11B52
m68k_011b52:
        move.w 0xf364:w,%d1
m68k_011b52_end:
.org 0x11B56
m68k_011b56:
        lsl.w #0x2,%d1
m68k_011b56_end:
.org 0x11B58
m68k_011b58:
        lea.l 0xe31c:w,%a0
m68k_011b58_end:
.org 0x11B5C
m68k_011b5c:
        move.l (%a0, %d1.w),%d0
m68k_011b5c_end:
.org 0x11B60
m68k_011b60:
        add.l %d4,%d0
m68k_011b60_end:
.org 0x11B62
m68k_011b62:
        cmpi.w #0x64,%d0
m68k_011b62_end:
.org 0x11B66
m68k_011b66:
        bls.b (. + 6)
m68k_011b66_end:
.org 0x11B68
m68k_011b68:
        move.w #0x64,%d0
m68k_011b68_end:
.org 0x11B6C
m68k_011b6c:
        move.l %d0,(%a0, %d1.w)
m68k_011b6c_end:
.org 0x11B70
m68k_011b70:
        lsl.l #0x1,%d2
m68k_011b70_end:
.org 0x11B72
m68k_011b72:
        lea.l 0xbe00:w,%a0
m68k_011b72_end:
.org 0x11B76
m68k_011b76:
        move.w (%a0, %d2.w),%d0
m68k_011b76_end:
.org 0x11B7A
m68k_011b7a:
        add.w %d4,%d0
m68k_011b7a_end:
.org 0x11B7C
m68k_011b7c:
        cmpi.w #0x3e7,%d0
m68k_011b7c_end:
.org 0x11B80
m68k_011b80:
        bls.w (. + 8)
m68k_011b80_end:
.org 0x11B84
m68k_011b84:
        move.w #0x3e7,%d0
m68k_011b84_end:
.org 0x11B88
m68k_011b88:
        move.w %d0,(%a0, %d2.w)
m68k_011b88_end:
.org 0x11B8C
m68k_011b8c:
        cmpi.w #0x5,%d4
m68k_011b8c_end:
.org 0x11B90
m68k_011b90:
        bcs.w (. + 28)
m68k_011b90_end:
.org 0x11B94
m68k_011b94:
        lea.l 0xc200:w,%a0
m68k_011b94_end:
.org 0x11B98
m68k_011b98:
        lsr.w #0x1,%d2
m68k_011b98_end:
.org 0x11B9A
m68k_011b9a:
        move.b (%a0, %d2.w),%d0
m68k_011b9a_end:
.org 0x11B9E
m68k_011b9e:
        addq.w #0x1,%d0
m68k_011b9e_end:
.org 0x11BA0
m68k_011ba0:
        cmpi.w #0x64,%d0
m68k_011ba0_end:
.org 0x11BA4
m68k_011ba4:
        bhi.w (. + 8)
m68k_011ba4_end:
.org 0x11BA8
m68k_011ba8:
        move.b %d0,(%a0, %d2.w)
m68k_011ba8_end:
.org 0x11BAC
m68k_011bac:
        rts
m68k_011bac_end:
.org 0x11BAE
m68k_011bae:
        move.w #0xffff,(%a0, %d0.w)
m68k_011bae_end:
.org 0x11BB4
m68k_011bb4:
        clr.b (%a5, %d2.w)
m68k_011bb4_end:
.org 0x11BB8
m68k_011bb8:
        bra.b (. + -12)
m68k_011bb8_end:
.org 0x11BBA
m68k_011bba:
        move.w #0xffff,(%a0, %d0.w)
m68k_011bba_end:
.org 0x11BC0
m68k_011bc0:
        clr.b (%a5, %d2.w)
m68k_011bc0_end:
.org 0x11BC4
m68k_011bc4:
        bra.b (. + -24)
m68k_011bc4_end:
.org 0x11BC6
m68k_011bc6:
        move.w 0xf364:w,%d0
m68k_011bc6_end:
.org 0x11BCA
m68k_011bca:
        lsl.w #0x1,%d0
m68k_011bca_end:
.org 0x11BCC
m68k_011bcc:
        add.w 0xf364:w,%d0
m68k_011bcc_end:
.org 0x11BD0
m68k_011bd0:
        lsl.w #0x2,%d0
m68k_011bd0_end:
.org 0x11BD2
m68k_011bd2:
        lea.l 0xe814:w,%a0
m68k_011bd2_end:
.org 0x11BD6
m68k_011bd6:
        movem.w (%a0, %d0.w),%d2-%d3
m68k_011bd6_end:
.org 0x11BDC
m68k_011bdc:
        tst.w %d2
m68k_011bdc_end:
.org 0x11BDE
m68k_011bde:
        bmi.w (. + 148)
m68k_011bde_end:
.org 0x11BE2
m68k_011be2:
        move.b (%a6, %d2.w),%d4
m68k_011be2_end:
.org 0x11BE6
m68k_011be6:
        cmp.b 0xf365:w,%d4
m68k_011be6_end:
.org 0x11BEA
m68k_011bea:
        bne.w (. + 150)
m68k_011bea_end:
.org 0x11BEE
m68k_011bee:
        mulu.w #0x64,%d3
m68k_011bee_end:
.org 0x11BF2
m68k_011bf2:
        move.w 0xf364:w,%d1
m68k_011bf2_end:
.org 0x11BF6
m68k_011bf6:
        lsl.w #0x2,%d1
m68k_011bf6_end:
.org 0x11BF8
m68k_011bf8:
        lea.l 0xdffc:w,%a1
m68k_011bf8_end:
.org 0x11BFC
m68k_011bfc:
        move.l (%a1, %d1.w),%d4
m68k_011bfc_end:
.org 0x11C00
m68k_011c00:
        sub.l %d3,%d4
m68k_011c00_end:
.org 0x11C02
m68k_011c02:
        bcs.w (. + 114)
m68k_011c02_end:
.org 0x11C06
m68k_011c06:
        move.l %d4,(%a1, %d1.w)
m68k_011c06_end:
.org 0x11C0A
m68k_011c0a:
        divu.w #0x32,%d3
m68k_011c0a_end:
.org 0x11C0E
m68k_011c0e:
        move.w %d2,%d1
m68k_011c0e_end:
.org 0x11C10
m68k_011c10:
        lsl.w #0x1,%d1
m68k_011c10_end:
.org 0x11C12
m68k_011c12:
        lea.l 0xb600:w,%a0
m68k_011c12_end:
.org 0x11C16
m68k_011c16:
        add.w (%a0, %d1.w),%d3
m68k_011c16_end:
.org 0x11C1A
m68k_011c1a:
        lea.l 0xbe00:w,%a0
m68k_011c1a_end:
.org 0x11C1E
m68k_011c1e:
        move.w (%a0, %d1.w),%d4
m68k_011c1e_end:
.org 0x11C22
m68k_011c22:
        lsr.w #0x2,%d4
m68k_011c22_end:
.org 0x11C24
m68k_011c24:
        add.w %d4,%d3
m68k_011c24_end:
.org 0x11C26
m68k_011c26:
        lea.l 0xc000:w,%a0
m68k_011c26_end:
.org 0x11C2A
m68k_011c2a:
        move.w (%a0, %d1.w),%d4
m68k_011c2a_end:
.org 0x11C2E
m68k_011c2e:
        lsr.w #0x2,%d4
m68k_011c2e_end:
.org 0x11C30
m68k_011c30:
        add.w %d4,%d3
m68k_011c30_end:
.org 0x11C32
m68k_011c32:
        jsr 0x83d4:l
m68k_011c32_end:
.org 0x11C38
m68k_011c38:
        andi.l #0xffff,%d0
m68k_011c38_end:
.org 0x11C3E
m68k_011c3e:
        move.l %d0,%d1
m68k_011c3e_end:
.org 0x11C40
m68k_011c40:
        lsl.l #0x1,%d0
m68k_011c40_end:
.org 0x11C42
m68k_011c42:
        add.l %d1,%d0
m68k_011c42_end:
.org 0x11C44
m68k_011c44:
        swap %d0
m68k_011c44_end:
.org 0x11C46
m68k_011c46:
        addq.w #0x6,%d0
m68k_011c46_end:
.org 0x11C48
m68k_011c48:
        mulu.w %d0,%d3
m68k_011c48_end:
.org 0x11C4A
m68k_011c4a:
        divu.w #0x3e8,%d3
m68k_011c4a_end:
.org 0x11C4E
m68k_011c4e:
        move.w 0xf364:w,%d0
m68k_011c4e_end:
.org 0x11C52
m68k_011c52:
        lsl.w #0x2,%d0
m68k_011c52_end:
.org 0x11C54
m68k_011c54:
        lea.l 0xe59c:w,%a0
m68k_011c54_end:
.org 0x11C58
m68k_011c58:
        move.w 0x2(%a0, %d0.w),%d7
m68k_011c58_end:
.org 0x11C5C
m68k_011c5c:
        add.w %d3,%d7
m68k_011c5c_end:
.org 0x11C5E
m68k_011c5e:
        cmpi.w #0x64,%d7
m68k_011c5e_end:
.org 0x11C62
m68k_011c62:
        bls.w (. + 8)
m68k_011c62_end:
.org 0x11C66
m68k_011c66:
        move.w #0x64,%d7
m68k_011c66_end:
.org 0x11C6A
m68k_011c6a:
        move.w %d7,0x2(%a0, %d0.w)
m68k_011c6a_end:
.org 0x11C6E
m68k_011c6e:
        bsr.w (. + 30)
m68k_011c6e_end:
.org 0x11C72
m68k_011c72:
        rts
m68k_011c72_end:
.org 0x11C74
m68k_011c74:
        move.w #0xffff,(%a0, %d0.w)
m68k_011c74_end:
.org 0x11C7A
m68k_011c7a:
        clr.b (%a5, %d2.w)
m68k_011c7a_end:
.org 0x11C7E
m68k_011c7e:
        bra.b (. + -12)
m68k_011c7e_end:
.org 0x11C80
m68k_011c80:
        move.w #0xffff,(%a0, %d0.w)
m68k_011c80_end:
.org 0x11C86
m68k_011c86:
        clr.b (%a5, %d2.w)
m68k_011c86_end:
.org 0x11C8A
m68k_011c8a:
        bra.b (. + -24)
m68k_011c8a_end:
.org 0x11C8C
m68k_011c8c:
        move.w %d0,-(%a7)
m68k_011c8c_end:
.org 0x11C8E
m68k_011c8e:
        lsl.w #0x1,%d2
m68k_011c8e_end:
.org 0x11C90
m68k_011c90:
        lsl.w #0x1,%d3
m68k_011c90_end:
.org 0x11C92
m68k_011c92:
        lea.l 0xbe00:w,%a0
m68k_011c92_end:
.org 0x11C96
m68k_011c96:
        move.w (%a0, %d2.w),%d0
m68k_011c96_end:
.org 0x11C9A
m68k_011c9a:
        add.w %d3,%d0
m68k_011c9a_end:
.org 0x11C9C
m68k_011c9c:
        cmpi.w #0x3e7,%d0
m68k_011c9c_end:
.org 0x11CA0
m68k_011ca0:
        bls.w (. + 8)
m68k_011ca0_end:
.org 0x11CA4
m68k_011ca4:
        move.w #0x3e7,%d0
m68k_011ca4_end:
.org 0x11CA8
m68k_011ca8:
        move.w %d0,(%a0, %d2.w)
m68k_011ca8_end:
.org 0x11CAC
m68k_011cac:
        lea.l 0xc000:w,%a0
m68k_011cac_end:
.org 0x11CB0
m68k_011cb0:
        move.w (%a0, %d2.w),%d0
m68k_011cb0_end:
.org 0x11CB4
m68k_011cb4:
        add.w %d3,%d0
m68k_011cb4_end:
.org 0x11CB6
m68k_011cb6:
        cmpi.w #0x3e7,%d0
m68k_011cb6_end:
.org 0x11CBA
m68k_011cba:
        bls.w (. + 8)
m68k_011cba_end:
.org 0x11CBE
m68k_011cbe:
        move.w #0x3e7,%d0
m68k_011cbe_end:
.org 0x11CC2
m68k_011cc2:
        move.w %d0,(%a0, %d2.w)
m68k_011cc2_end:
.org 0x11CC6
m68k_011cc6:
        move.w (%a7)+,%d0
m68k_011cc6_end:
.org 0x11CC8
m68k_011cc8:
        rts
m68k_011cc8_end:
.org 0x11CCA
m68k_011cca:
        lea.l 0xcd00:w,%a0
m68k_011cca_end:
.org 0x11CCE
m68k_011cce:
        move.w #0xff,%d0
m68k_011cce_end:
.org 0x11CD2
m68k_011cd2:
        cmpi.b #0x1,(%a0)
m68k_011cd2_end:
.org 0x11CD6
m68k_011cd6:
        bne.b (. + 4)
m68k_011cd6_end:
.org 0x11CD8
m68k_011cd8:
        clr.b (%a0)
m68k_011cd8_end:
.org 0x11CDA
m68k_011cda:
        addq.w #0x1,%a0
m68k_011cda_end:
.org 0x11CDC
m68k_011cdc:
        dbra %d0,(. + -10)
m68k_011cdc_end:
.org 0x11CE0
m68k_011ce0:
        lea.l 0xea38:w,%a0
m68k_011ce0_end:
.org 0x11CE4
m68k_011ce4:
        move.w #0x27,%d0
m68k_011ce4_end:
.org 0x11CE8
m68k_011ce8:
        bclr.b #0x1,(%a0)+
m68k_011ce8_end:
.org 0x11CEC
m68k_011cec:
        dbra %d0,(. + -4)
m68k_011cec_end:
.org 0x11CF0
m68k_011cf0:
        rts
m68k_011cf0_end:
.org 0x1270A
m68k_01270a:
        clr.w %d3
m68k_01270a_end:
.org 0x1270C
m68k_01270c:
        clr.w %d4
m68k_01270c_end:
.org 0x1270E
m68k_01270e:
        subi.l #0x186a0,%d0
m68k_01270e_end:
.org 0x12714
m68k_012714:
        bcs.b (. + 6)
m68k_012714_end:
.org 0x1271A
m68k_01271a:
        addi.l #0x186a0,%d0
m68k_01271a_end:
.org 0x12720
m68k_012720:
        tst.w %d3
m68k_012720_end:
.org 0x12722
m68k_012722:
        bne.b (. + 6)
m68k_012722_end:
.org 0x12724
m68k_012724:
        move.w %d2,(%a6)+
m68k_012724_end:
.org 0x12726
m68k_012726:
        bra.b (. + 14)
m68k_012726_end:
.org 0x12734
m68k_012734:
        move.w #0x2710,%d3
m68k_012734_end:
.org 0x12738
m68k_012738:
        bsr.w (. + 40)
m68k_012738_end:
.org 0x1273C
m68k_01273c:
        move.w #0x3e8,%d3
m68k_01273c_end:
.org 0x12740
m68k_012740:
        bsr.w (. + 32)
m68k_012740_end:
.org 0x12744
m68k_012744:
        move.w #0x64,%d3
m68k_012744_end:
.org 0x12748
m68k_012748:
        bsr.w (. + 24)
m68k_012748_end:
.org 0x1274C
m68k_01274c:
        move.w #0xa,%d3
m68k_01274c_end:
.org 0x12750
m68k_012750:
        bsr.w (. + 16)
m68k_012750_end:
.org 0x12754
m68k_012754:
        clr.w %d5
m68k_012754_end:
.org 0x12756
m68k_012756:
        move.b 42(%pc, %d0.w),%d5
m68k_012756_end:
.org 0x1275A
m68k_01275a:
        add.w %d1,%d5
m68k_01275a_end:
.org 0x1275C
m68k_01275c:
        move.w %d5,(%a6)+
m68k_01275c_end:
.org 0x1275E
m68k_01275e:
        rts
m68k_01275e_end:
.org 0x12760
m68k_012760:
        clr.w %d5
m68k_012760_end:
.org 0x12762
m68k_012762:
        divu.w %d3,%d0
m68k_012762_end:
.org 0x12764
m68k_012764:
        tst.w %d4
m68k_012764_end:
.org 0x12766
m68k_012766:
        bne.b (. + 6)
m68k_012766_end:
.org 0x12768
m68k_012768:
        tst.w %d0
m68k_012768_end:
.org 0x1276A
m68k_01276a:
        beq.b (. + 16)
m68k_01276a_end:
.org 0x1276C
m68k_01276c:
        move.b 20(%pc, %d0.w),%d5
m68k_01276c_end:
.org 0x12770
m68k_012770:
        add.w %d1,%d5
m68k_012770_end:
.org 0x12772
m68k_012772:
        move.w %d5,(%a6)+
m68k_012772_end:
.org 0x12774
m68k_012774:
        move.w #0x1,%d4
m68k_012774_end:
.org 0x12778
m68k_012778:
        bra.b (. + 4)
m68k_012778_end:
.org 0x1277A
m68k_01277a:
        move.w %d2,(%a6)+
m68k_01277a_end:
.org 0x1277C
m68k_01277c:
        clr.w %d0
m68k_01277c_end:
.org 0x1277E
m68k_01277e:
        swap %d0
m68k_01277e_end:
.org 0x12780
m68k_012780:
        rts
m68k_012780_end:
.org 0x128E2
m68k_0128e2:
        bsr.w (. + 74)
m68k_0128e2_end:
.org 0x128E6
m68k_0128e6:
        bsr.w (. + 154)
m68k_0128e6_end:
.org 0x128EA
m68k_0128ea:
        bsr.w (. + 356)
m68k_0128ea_end:
.org 0x128EE
m68k_0128ee:
        btst.b #0x5,0xf603:w
m68k_0128ee_end:
.org 0x128F4
m68k_0128f4:
        beq.b (. + 28)
m68k_0128f4_end:
.org 0x128F6
m68k_0128f6:
        move.l 0xf3f4:w,0xf39e:w
m68k_0128f6_end:
.org 0x128FC
m68k_0128fc:
        tst.l 0xf3f4:w
m68k_0128fc_end:
.org 0x12900
m68k_012900:
        beq.b (. + 42)
m68k_012900_end:
.org 0x12902
m68k_012902:
        move.w #0x208,0xf612:w
m68k_012902_end:
.org 0x12908
m68k_012908:
        move.w #0x4,0xf362:w
m68k_012908_end:
.org 0x1290E
m68k_01290e:
        bra.b (. + 28)
m68k_01290e_end:
.org 0x12910
m68k_012910:
        btst.b #0x4,0xf603:w
m68k_012910_end:
.org 0x12916
m68k_012916:
        beq.b (. + 20)
m68k_012916_end:
.org 0x1292A
m68k_01292a:
        rts
m68k_01292a_end:
.org 0x1292C
m68k_01292c:
        lea.l 0xd100:w,%a0
m68k_01292c_end:
.org 0x12930
m68k_012930:
        adda.w 0xf31a:w,%a0
m68k_012930_end:
.org 0x12934
m68k_012934:
        move.w #0x6,(%a0)+
m68k_012934_end:
.org 0x12938
m68k_012938:
        move.w #0xc440,(%a0)+
m68k_012938_end:
.org 0x1293C
m68k_01293c:
        move.l 0xf3f4:w,%d0
m68k_01293c_end:
.org 0x12940
m68k_012940:
        move.w #0xc386,%d1
m68k_012940_end:
.org 0x12944
m68k_012944:
        clr.w %d2
m68k_012944_end:
.org 0x12946
m68k_012946:
        lea.l 0xef0c:w,%a6
m68k_012946_end:
.org 0x1294A
m68k_01294a:
        jsr 0x1270a:l
m68k_01294a_end:
.org 0x12950
m68k_012950:
        move.w #0x5,%d0
m68k_012950_end:
.org 0x12954
m68k_012954:
        lea.l 0xef0c:w,%a1
m68k_012954_end:
.org 0x12958
m68k_012958:
        clr.w %d2
m68k_012958_end:
.org 0x1295A
m68k_01295a:
        move.w (%a1)+,%d1
m68k_01295a_end:
.org 0x1295C
m68k_01295c:
        bne.b (. + 18)
m68k_01295c_end:
.org 0x1295E
m68k_01295e:
        cmp.w 0xf39a:w,%d2
m68k_01295e_end:
.org 0x12962
m68k_012962:
        bcs.b (. + 8)
m68k_012962_end:
.org 0x12964
m68k_012964:
        move.w #0xc386,%d1
m68k_012964_end:
.org 0x12968
m68k_012968:
        bra.b (. + 6)
m68k_012968_end:
.org 0x1296A
m68k_01296a:
        move.w #0xc001,%d1
m68k_01296a_end:
.org 0x1296E
m68k_01296e:
        move.w %d1,(%a0)+
m68k_01296e_end:
.org 0x12970
m68k_012970:
        addq.w #0x1,%d2
m68k_012970_end:
.org 0x12972
m68k_012972:
        dbra %d0,(. + -24)
m68k_012972_end:
.org 0x12976
m68k_012976:
        clr.w (%a0)
m68k_012976_end:
.org 0x12978
m68k_012978:
        addi.w #0x10,0xf31a:w
m68k_012978_end:
.org 0x1297E
m68k_01297e:
        rts
m68k_01297e_end:
.org 0x12980
m68k_012980:
        move.b 0xf602:w,%d0
m68k_012980_end:
.org 0x12984
m68k_012984:
        andi.w #0xc,%d0
m68k_012984_end:
.org 0x12988
m68k_012988:
        beq.w (. + 36)
m68k_012988_end:
.org 0x129AC
m68k_0129ac:
        move.b 0xf602:w,%d0
m68k_0129ac_end:
.org 0x129B0
m68k_0129b0:
        andi.w #0x3,%d0
m68k_0129b0_end:
.org 0x129B4
m68k_0129b4:
        beq.b (. + 34)
m68k_0129b4_end:
.org 0x129B6
m68k_0129b6:
        subq.w #0x1,0xf608:w
m68k_0129b6_end:
.org 0x129BA
m68k_0129ba:
        bne.w (. + 34)
m68k_0129ba_end:
.org 0x129BE
m68k_0129be:
        move.w #0xc,0xf608:w
m68k_0129be_end:
.org 0x129C4
m68k_0129c4:
        btst.l #0x1,%d0
m68k_0129c4_end:
.org 0x129C8
m68k_0129c8:
        bne.b (. + 8)
m68k_0129c8_end:
.org 0x129CA
m68k_0129ca:
        bsr.w (. + 66)
m68k_0129ca_end:
.org 0x129CE
m68k_0129ce:
        bra.b (. + 14)
m68k_0129ce_end:
.org 0x129D6
m68k_0129d6:
        move.w #0x1,0xf608:w
m68k_0129d6_end:
.org 0x129DC
m68k_0129dc:
        rts
m68k_0129dc_end:
.org 0x12A0C
m68k_012a0c:
        move.w 0xf39a:w,%d1
m68k_012a0c_end:
.org 0x12A10
m68k_012a10:
        lsl.w #0x2,%d1
m68k_012a10_end:
.org 0x12A12
m68k_012a12:
        lea.l 2616(%pc),%a0
m68k_012a12_end:
.org 0x12A16
m68k_012a16:
        nop
m68k_012a16_end:
.org 0x12A18
m68k_012a18:
        move.l (%a0, %d1.w),%d1
m68k_012a18_end:
.org 0x12A1C
m68k_012a1c:
        add.l 0xf3f4:w,%d1
m68k_012a1c_end:
.org 0x12A20
m68k_012a20:
        cmp.l 0xf3f8:w,%d1
m68k_012a20_end:
.org 0x12A24
m68k_012a24:
        bhi.w (. + 8)
m68k_012a24_end:
.org 0x12A28
m68k_012a28:
        move.l %d1,0xf3f4:w
m68k_012a28_end:
.org 0x12A2C
m68k_012a2c:
        rts
m68k_012a2c_end:
.org 0x12A4E
m68k_012a4e:
        cmpi.w #0x18,0xf39c:w
m68k_012a4e_end:
.org 0x12A54
m68k_012a54:
        bcs.b (. + 8)
m68k_012a54_end:
.org 0x12A56
m68k_012a56:
        move.w #0x18,0xf39c:w
m68k_012a56_end:
.org 0x12A5C
m68k_012a5c:
        move.w 0xf602:w,%d0
m68k_012a5c_end:
.org 0x12A60
m68k_012a60:
        andi.w #0x30,%d0
m68k_012a60_end:
.org 0x12A64
m68k_012a64:
        bne.w (. + 42)
m68k_012a64_end:
.org 0x12A68
m68k_012a68:
        subq.w #0x1,0xf39c:w
m68k_012a68_end:
.org 0x12A6C
m68k_012a6c:
        cmpi.w #0xc,0xf39c:w
m68k_012a6c_end:
.org 0x12A72
m68k_012a72:
        bcs.b (. + 28)
m68k_012a72_end:
.org 0x12A74
m68k_012a74:
        lea.l 26(%pc),%a0
m68k_012a74_end:
.org 0x12A78
m68k_012a78:
        move.w #0x40,%d0
m68k_012a78_end:
.org 0x12A7C
m68k_012a7c:
        move.w 0xf39a:w,%d1
m68k_012a7c_end:
.org 0x12A80
m68k_012a80:
        lsl.w #0x3,%d1
m68k_012a80_end:
.org 0x12A82
m68k_012a82:
        addi.w #0x100,%d1
m68k_012a82_end:
.org 0x12A86
m68k_012a86:
        clr.w %d2
m68k_012a86_end:
.org 0x12A88
m68k_012a88:
        jsr 0xac08:l
m68k_012a88_end:
.org 0x12A8E
m68k_012a8e:
        rts
m68k_012a8e_end:
.org 0x13188
m68k_013188:
        clr.l 0xf3e4:w
m68k_013188_end:
.org 0x1318C
m68k_01318c:
        clr.l 0xf39e:w
m68k_01318c_end:
.org 0x13190
m68k_013190:
        move.w #0x3,0xf39a:w
m68k_013190_end:
.org 0x13196
m68k_013196:
        move.w 0xf364:w,%d0
m68k_013196_end:
.org 0x1319A
m68k_01319a:
        lsl.w #0x2,%d0
m68k_01319a_end:
.org 0x1319C
m68k_01319c:
        lea.l 0xdffc:w,%a0
m68k_01319c_end:
.org 0x131A0
m68k_0131a0:
        move.l (%a0, %d0.w),0xf3e8:w
m68k_0131a0_end:
.org 0x131A6
m68k_0131a6:
        move.l 0xf3e8:w,%d2
m68k_0131a6_end:
.org 0x131AA
m68k_0131aa:
        divu.w #0x64,%d2
m68k_0131aa_end:
.org 0x131AE
m68k_0131ae:
        lea.l 0xe13c:w,%a1
m68k_0131ae_end:
.org 0x131B2
m68k_0131b2:
        move.l (%a1, %d0.w),%d3
m68k_0131b2_end:
.org 0x131B6
m68k_0131b6:
        move.l %d3,%d4
m68k_0131b6_end:
.org 0x131B8
m68k_0131b8:
        mulu.w #0xa,%d3
m68k_0131b8_end:
.org 0x131BC
m68k_0131bc:
        swap %d4
m68k_0131bc_end:
.org 0x131BE
m68k_0131be:
        mulu.w #0xa,%d4
m68k_0131be_end:
.org 0x131C2
m68k_0131c2:
        swap %d4
m68k_0131c2_end:
.org 0x131C4
m68k_0131c4:
        add.l %d4,%d3
m68k_0131c4_end:
.org 0x131C6
m68k_0131c6:
        lea.l 0xe774:w,%a1
m68k_0131c6_end:
.org 0x131CA
m68k_0131ca:
        move.l #0x186a0,%d4
m68k_0131ca_end:
.org 0x131D0
m68k_0131d0:
        sub.l (%a1, %d0.w),%d4
m68k_0131d0_end:
.org 0x131D4
m68k_0131d4:
        divu.w #0x64,%d4
m68k_0131d4_end:
.org 0x131D8
m68k_0131d8:
        andi.l #0xffff,%d4
m68k_0131d8_end:
.org 0x131DE
m68k_0131de:
        cmp.l %d3,%d4
m68k_0131de_end:
.org 0x131E0
m68k_0131e0:
        bcc.w (. + 6)
m68k_0131e0_end:
.org 0x131E4
m68k_0131e4:
        move.l %d4,%d3
m68k_0131e4_end:
.org 0x131E6
m68k_0131e6:
        andi.l #0xffff,%d2
m68k_0131e6_end:
.org 0x131EC
m68k_0131ec:
        cmp.l %d3,%d2
m68k_0131ec_end:
.org 0x131EE
m68k_0131ee:
        bls.b (. + 12)
m68k_0131ee_end:
.org 0x131F0
m68k_0131f0:
        move.w %d3,%d2
m68k_0131f0_end:
.org 0x131F2
m68k_0131f2:
        mulu.w #0x64,%d3
m68k_0131f2_end:
.org 0x131F6
m68k_0131f6:
        move.l %d3,0xf3e8:w
m68k_0131f6_end:
.org 0x131FA
m68k_0131fa:
        move.w #0x3,%d1
m68k_0131fa_end:
.org 0x131FE
m68k_0131fe:
        cmpi.w #0xa,%d2
m68k_0131fe_end:
.org 0x13202
m68k_013202:
        bcs.b (. + 20)
m68k_013202_end:
.org 0x13204
m68k_013204:
        subq.w #0x1,%d1
m68k_013204_end:
.org 0x13206
m68k_013206:
        cmpi.w #0x64,%d2
m68k_013206_end:
.org 0x1320A
m68k_01320a:
        bcs.b (. + 12)
m68k_01320a_end:
.org 0x1320C
m68k_01320c:
        subq.w #0x1,%d1
m68k_01320c_end:
.org 0x1320E
m68k_01320e:
        cmpi.w #0x3e8,%d2
m68k_01320e_end:
.org 0x13212
m68k_013212:
        bcs.b (. + 4)
m68k_013212_end:
.org 0x13214
m68k_013214:
        subq.w #0x1,%d1
m68k_013214_end:
.org 0x13216
m68k_013216:
        move.w %d1,0xf3ec:w
m68k_013216_end:
.org 0x1321A
m68k_01321a:
        rts
m68k_01321a_end:
.org 0x132AE
m68k_0132ae:
        bsr.w (. + 610)
m68k_0132ae_end:
.org 0x132B2
m68k_0132b2:
        move.b 0xf602:w,%d0
m68k_0132b2_end:
.org 0x132B6
m68k_0132b6:
        andi.w #0xc,%d0
m68k_0132b6_end:
.org 0x132BA
m68k_0132ba:
        beq.w (. + 74)
m68k_0132ba_end:
.org 0x132BE
m68k_0132be:
        subq.w #0x1,0xf608:w
m68k_0132be_end:
.org 0x132C2
m68k_0132c2:
        bne.w (. + 214)
m68k_0132c2_end:
.org 0x132C6
m68k_0132c6:
        move.w #0xc,0xf608:w
m68k_0132c6_end:
.org 0x132CC
m68k_0132cc:
        btst.l #0x3,%d0
m68k_0132cc_end:
.org 0x132D0
m68k_0132d0:
        bne.b (. + 28)
m68k_0132d0_end:
.org 0x132D2
m68k_0132d2:
        move.w 0xf39a:w,%d0
m68k_0132d2_end:
.org 0x132D6
m68k_0132d6:
        subq.w #0x1,%d0
m68k_0132d6_end:
.org 0x132D8
m68k_0132d8:
        bmi.w (. + 186)
m68k_0132d8_end:
.org 0x132DC
m68k_0132dc:
        cmp.w 0xf3ec:w,%d0
m68k_0132dc_end:
.org 0x132E0
m68k_0132e0:
        bcs.w (. + 178)
m68k_0132e0_end:
.org 0x132E4
m68k_0132e4:
        move.w %d0,0xf39a:w
m68k_0132e4_end:
.org 0x132E8
m68k_0132e8:
        bra.w (. + 176)
m68k_0132e8_end:
.org 0x132EC
m68k_0132ec:
        move.w 0xf39a:w,%d0
m68k_0132ec_end:
.org 0x132F0
m68k_0132f0:
        addi.w #0x1,%d0
m68k_0132f0_end:
.org 0x132F4
m68k_0132f4:
        cmpi.w #0x3,%d0
m68k_0132f4_end:
.org 0x132F8
m68k_0132f8:
        bhi.w (. + 154)
m68k_0132f8_end:
.org 0x132FC
m68k_0132fc:
        move.w %d0,0xf39a:w
m68k_0132fc_end:
.org 0x13300
m68k_013300:
        bra.w (. + 152)
m68k_013300_end:
.org 0x13304
m68k_013304:
        move.b 0xf602:w,%d0
m68k_013304_end:
.org 0x13308
m68k_013308:
        andi.w #0x3,%d0
m68k_013308_end:
.org 0x1330C
m68k_01330c:
        beq.w (. + 134)
m68k_01330c_end:
.org 0x13310
m68k_013310:
        subq.w #0x1,0xf608:w
m68k_013310_end:
.org 0x13314
m68k_013314:
        bne.w (. + 132)
m68k_013314_end:
.org 0x13318
m68k_013318:
        move.w #0xc,0xf608:w
m68k_013318_end:
.org 0x1331E
m68k_01331e:
        btst.l #0x1,%d0
m68k_01331e_end:
.org 0x13322
m68k_013322:
        bne.b (. + 62)
m68k_013322_end:
.org 0x13324
m68k_013324:
        move.w 0xf39a:w,%d0
m68k_013324_end:
.org 0x13328
m68k_013328:
        lsl.w #0x1,%d0
m68k_013328_end:
.org 0x1332A
m68k_01332a:
        lea.l 0xef00:w,%a0
m68k_01332a_end:
.org 0x1332E
m68k_01332e:
        move.w (%a0, %d0.w),%d1
m68k_01332e_end:
.org 0x13332
m68k_013332:
        lea.l 248(%pc),%a0
m68k_013332_end:
.org 0x13336
m68k_013336:
        nop
m68k_013336_end:
.org 0x13338
m68k_013338:
        lsl.w #0x1,%d0
m68k_013338_end:
.org 0x1333A
m68k_01333a:
        move.l (%a0, %d0.w),%d1
m68k_01333a_end:
.org 0x1333E
m68k_01333e:
        add.l 0xf39e:w,%d1
m68k_01333e_end:
.org 0x13342
m68k_013342:
        cmp.l 0xf3e8:w,%d1
m68k_013342_end:
.org 0x13346
m68k_013346:
        bhi.w (. + 76)
m68k_013346_end:
.org 0x1334A
m68k_01334a:
        move.l %d1,0xf39e:w
m68k_01334a_end:
.org 0x1334E
m68k_01334e:
        lea.l 252(%pc),%a0
m68k_01334e_end:
.org 0x13352
m68k_013352:
        nop
m68k_013352_end:
.org 0x13354
m68k_013354:
        move.l (%a0, %d0.w),%d1
m68k_013354_end:
.org 0x13358
m68k_013358:
        add.l %d1,0xf3e4:w
m68k_013358_end:
.org 0x1335C
m68k_01335c:
        bra.w (. + 48)
m68k_01335c_end:
.org 0x13360
m68k_013360:
        move.w 0xf39a:w,%d0
m68k_013360_end:
.org 0x13364
m68k_013364:
        lsl.w #0x2,%d0
m68k_013364_end:
.org 0x13366
m68k_013366:
        lea.l 196(%pc),%a0
m68k_013366_end:
.org 0x1336A
m68k_01336a:
        nop
m68k_01336a_end:
.org 0x1336C
m68k_01336c:
        move.l (%a0, %d0.w),%d1
m68k_01336c_end:
.org 0x13370
m68k_013370:
        move.l 0xf39e:w,%d2
m68k_013370_end:
.org 0x13374
m68k_013374:
        sub.l %d1,%d2
m68k_013374_end:
.org 0x13376
m68k_013376:
        bcs.w (. + 28)
m68k_013376_end:
.org 0x1337A
m68k_01337a:
        move.l %d2,0xf39e:w
m68k_01337a_end:
.org 0x1337E
m68k_01337e:
        lea.l 204(%pc),%a0
m68k_01337e_end:
.org 0x13382
m68k_013382:
        nop
m68k_013382_end:
.org 0x13384
m68k_013384:
        move.l (%a0, %d0.w),%d1
m68k_013384_end:
.org 0x13388
m68k_013388:
        sub.l %d1,0xf3e4:w
m68k_013388_end:
.org 0x1338C
m68k_01338c:
        bsr.w (. + -284)
m68k_01338c_end:
.org 0x13390
m68k_013390:
        bra.b (. + 8)
m68k_013390_end:
.org 0x13392
m68k_013392:
        move.w #0x1,0xf608:w
m68k_013392_end:
.org 0x13398
m68k_013398:
        move.w 0xf602:w,%d0
m68k_013398_end:
.org 0x1339C
m68k_01339c:
        btst.l #0x5,%d0
m68k_01339c_end:
.org 0x133A0
m68k_0133a0:
        beq.b (. + 116)
m68k_0133a0_end:
.org 0x133A2
m68k_0133a2:
        move.w 0xf392:w,%d0
m68k_0133a2_end:
.org 0x133A6
m68k_0133a6:
        lsl.w #0x2,%d0
m68k_0133a6_end:
.org 0x133A8
m68k_0133a8:
        lea.l 0xe774:w,%a0
m68k_0133a8_end:
.org 0x133AC
m68k_0133ac:
        move.l 0xf3e4:w,0xcfce:w
m68k_0133ac_end:
.org 0x133B2
m68k_0133b2:
        move.l (%a0, %d0.w),%d1
m68k_0133b2_end:
.org 0x133B6
m68k_0133b6:
        add.l %d1,0xf3e4:w
m68k_0133b6_end:
.org 0x133BA
m68k_0133ba:
        cmpi.l #0xf423f,0xf3e4:w
m68k_0133ba_end:
.org 0x133C2
m68k_0133c2:
        bls.b (. + 10)
m68k_0133c2_end:
.org 0x133C4
m68k_0133c4:
        move.l #0xf423f,0xf3e4:w
m68k_0133c4_end:
.org 0x133CC
m68k_0133cc:
        jsr 0xc0b6:l
m68k_0133cc_end:
.org 0x133D2
m68k_0133d2:
        move.w #0x3,0xf362:w
m68k_0133d2_end:
.org 0x133D8
m68k_0133d8:
        move.w #0x12,0xf36a:w
m68k_0133d8_end:
.org 0x133DE
m68k_0133de:
        move.l 0xcfce:w,%d0
m68k_0133de_end:
.org 0x133E2
m68k_0133e2:
        addi.l #0x1f4,%d0
m68k_0133e2_end:
.org 0x133E8
m68k_0133e8:
        divu.w #0x3e8,%d0
m68k_0133e8_end:
.org 0x133EC
m68k_0133ec:
        andi.l #0xffff,%d0
m68k_0133ec_end:
.org 0x133F2
m68k_0133f2:
        move.w 0xf392:w,%d1
m68k_0133f2_end:
.org 0x133F6
m68k_0133f6:
        lsl.w #0x2,%d1
m68k_0133f6_end:
.org 0x133F8
m68k_0133f8:
        lea.l 0xe13c:w,%a0
m68k_0133f8_end:
.org 0x133FC
m68k_0133fc:
        sub.l %d0,(%a0, %d1.w)
m68k_0133fc_end:
.org 0x13400
m68k_013400:
        move.w #0x15,0xff7026:l
m68k_013400_end:
.org 0x13408
m68k_013408:
        move.w #0xc0,0xf600:w
m68k_013408_end:
.org 0x1340E
m68k_01340e:
        bsr.w (. + 110)
m68k_01340e_end:
.org 0x13412
m68k_013412:
        bra.b (. + 24)
m68k_013412_end:
.org 0x13414
m68k_013414:
        btst.l #0x4,%d0
m68k_013414_end:
.org 0x13418
m68k_013418:
        beq.b (. + 18)
m68k_013418_end:
.org 0x1341A
m68k_01341a:
        bsr.w (. + 292)
m68k_01341a_end:
.org 0x1341E
m68k_01341e:
        move.w #0x2,0xf362:w
m68k_01341e_end:
.org 0x13424
m68k_013424:
        move.w #0x12,0xf36a:w
m68k_013424_end:
.org 0x1342A
m68k_01342a:
        rts
m68k_01342a_end:
.org 0x1379A
m68k_01379a:
        move.b 0xf602:w,%d0
m68k_01379a_end:
.org 0x1379E
m68k_01379e:
        andi.w #0xc,%d0
m68k_01379e_end:
.org 0x137A2
m68k_0137a2:
        beq.b (. + 84)
m68k_0137a2_end:
.org 0x137A4
m68k_0137a4:
        subq.w #0x1,0xf608:w
m68k_0137a4_end:
.org 0x137A8
m68k_0137a8:
        bne.w (. + 390)
m68k_0137a8_end:
.org 0x137AC
m68k_0137ac:
        move.w #0xc,0xf608:w
m68k_0137ac_end:
.org 0x137B2
m68k_0137b2:
        btst.l #0x3,%d0
m68k_0137b2_end:
.org 0x137B6
m68k_0137b6:
        bne.b (. + 42)
m68k_0137b6_end:
.org 0x137B8
m68k_0137b8:
        move.w 0xf39a:w,%d1
m68k_0137b8_end:
.org 0x137BC
m68k_0137bc:
        subq.w #0x1,%d1
m68k_0137bc_end:
.org 0x137BE
m68k_0137be:
        lsl.w #0x1,%d1
m68k_0137be_end:
.org 0x137C0
m68k_0137c0:
        lea.l 0xef0c:w,%a0
m68k_0137c0_end:
.org 0x137C4
m68k_0137c4:
        cmpi.w #0xc001,(%a0, %d1.w)
m68k_0137c4_end:
.org 0x137CA
m68k_0137ca:
        bne.b (. + 14)
m68k_0137ca_end:
.org 0x137CC
m68k_0137cc:
        lea.l 0xef00:w,%a0
m68k_0137cc_end:
.org 0x137D0
m68k_0137d0:
        tst.w (%a0, %d1.w)
m68k_0137d0_end:
.org 0x137D4
m68k_0137d4:
        beq.w (. + 206)
m68k_0137d4_end:
.org 0x137D8
m68k_0137d8:
        subq.w #0x1,0xf39a:w
m68k_0137d8_end:
.org 0x137DC
m68k_0137dc:
        bra.w (. + 338)
m68k_0137dc_end:
.org 0x137E0
m68k_0137e0:
        move.w 0xf39a:w,%d1
m68k_0137e0_end:
.org 0x137E4
m68k_0137e4:
        addq.w #0x1,%d1
m68k_0137e4_end:
.org 0x137E6
m68k_0137e6:
        cmpi.w #0x6,%d1
m68k_0137e6_end:
.org 0x137EA
m68k_0137ea:
        bcc.w (. + 184)
m68k_0137ea_end:
.org 0x137EE
m68k_0137ee:
        move.w %d1,0xf39a:w
m68k_0137ee_end:
.org 0x137F2
m68k_0137f2:
        bra.w (. + 316)
m68k_0137f2_end:
.org 0x137F6
m68k_0137f6:
        move.b 0xf602:w,%d0
m68k_0137f6_end:
.org 0x137FA
m68k_0137fa:
        andi.w #0x3,%d0
m68k_0137fa_end:
.org 0x137FE
m68k_0137fe:
        beq.w (. + 164)
m68k_0137fe_end:
.org 0x13802
m68k_013802:
        subq.w #0x1,0xf608:w
m68k_013802_end:
.org 0x13806
m68k_013806:
        bne.w (. + 296)
m68k_013806_end:
.org 0x1380A
m68k_01380a:
        move.w #0xc,0xf608:w
m68k_01380a_end:
.org 0x13810
m68k_013810:
        btst.l #0x1,%d0
m68k_013810_end:
.org 0x13814
m68k_013814:
        bne.b (. + 80)
m68k_013814_end:
.org 0x13816
m68k_013816:
        move.w 0xf39a:w,%d0
m68k_013816_end:
.org 0x1381A
m68k_01381a:
        lsl.w #0x1,%d0
m68k_01381a_end:
.org 0x1381C
m68k_01381c:
        lsl.w #0x1,%d0
m68k_01381c_end:
.org 0x1381E
m68k_01381e:
        lea.l -980(%pc),%a0
m68k_01381e_end:
.org 0x13822
m68k_013822:
        move.l (%a0, %d0.w),%d1
m68k_013822_end:
.org 0x13826
m68k_013826:
        move.l 0xcfae:w,%d2
m68k_013826_end:
.org 0x1382A
m68k_01382a:
        sub.l %d1,%d2
m68k_01382a_end:
.org 0x1382C
m68k_01382c:
        bcs.w (. + 118)
m68k_01382c_end:
.org 0x13830
m68k_013830:
        move.w 0xf378:w,%d4
m68k_013830_end:
.org 0x13834
m68k_013834:
        lea.l 0xf4fe:w,%a1
m68k_013834_end:
.org 0x13838
m68k_013838:
        lsl.w #0x1,%d4
m68k_013838_end:
.org 0x1383A
m68k_01383a:
        move.w (%a1, %d4.w),%d4
m68k_01383a_end:
.org 0x1383E
m68k_01383e:
        lsl.w #0x1,%d4
m68k_01383e_end:
.org 0x13840
m68k_013840:
        lea.l 0xb800:w,%a1
m68k_013840_end:
.org 0x13844
m68k_013844:
        move.w (%a1, %d4.w),%d4
m68k_013844_end:
.org 0x13848
m68k_013848:
        mulu.w #0x64,%d4
m68k_013848_end:
.org 0x1384C
m68k_01384c:
        move.l 0xf3ee:w,%d3
m68k_01384c_end:
.org 0x13850
m68k_013850:
        add.l %d1,%d3
m68k_013850_end:
.org 0x13852
m68k_013852:
        cmp.l %d4,%d3
m68k_013852_end:
.org 0x13854
m68k_013854:
        bhi.w (. + 78)
m68k_013854_end:
.org 0x13858
m68k_013858:
        move.l %d2,0xcfae:w
m68k_013858_end:
.org 0x1385C
m68k_01385c:
        move.l %d3,0xf3ee:w
m68k_01385c_end:
.org 0x13860
m68k_013860:
        bra.w (. + 58)
m68k_013860_end:
.org 0x13864
m68k_013864:
        move.w 0xf39a:w,%d0
m68k_013864_end:
.org 0x13868
m68k_013868:
        lsl.w #0x1,%d0
m68k_013868_end:
.org 0x1386A
m68k_01386a:
        lsl.w #0x1,%d0
m68k_01386a_end:
.org 0x1386C
m68k_01386c:
        lea.l -1058(%pc),%a0
m68k_01386c_end:
.org 0x13870
m68k_013870:
        move.l (%a0, %d0.w),%d1
m68k_013870_end:
.org 0x13874
m68k_013874:
        move.l 0xf3ee:w,%d2
m68k_013874_end:
.org 0x13878
m68k_013878:
        sub.l %d1,%d2
m68k_013878_end:
.org 0x1387A
m68k_01387a:
        bcs.w (. + 40)
m68k_01387a_end:
.org 0x1387E
m68k_01387e:
        move.l 0xcfae:w,%d3
m68k_01387e_end:
.org 0x13882
m68k_013882:
        add.l %d1,%d3
m68k_013882_end:
.org 0x13884
m68k_013884:
        cmpi.l #0xf423f,%d3
m68k_013884_end:
.org 0x1388A
m68k_01388a:
        bhi.w (. + 24)
m68k_01388a_end:
.org 0x1388E
m68k_01388e:
        move.l %d2,0xf3ee:w
m68k_01388e_end:
.org 0x13892
m68k_013892:
        move.l %d3,0xcfae:w
m68k_013892_end:
.org 0x13896
m68k_013896:
        bra.w (. + 4)
m68k_013896_end:
.org 0x1389A
m68k_01389a:
        bsr.w (. + -336)
m68k_01389a_end:
.org 0x1389E
m68k_01389e:
        bra.w (. + 144)
m68k_01389e_end:
.org 0x138A2
m68k_0138a2:
        move.w #0x1,0xf608:w
m68k_0138a2_end:
.org 0x138A8
m68k_0138a8:
        btst.b #0x4,0xf603:w
m68k_0138a8_end:
.org 0x138AE
m68k_0138ae:
        bne.b (. + 74)
m68k_0138ae_end:
.org 0x138B0
m68k_0138b0:
        btst.b #0x5,0xf603:w
m68k_0138b0_end:
.org 0x138B6
m68k_0138b6:
        beq.b (. + 120)
m68k_0138b6_end:
.org 0x138B8
m68k_0138b8:
        move.w #0xac,%d0
m68k_0138b8_end:
.org 0x138BC
m68k_0138bc:
        jsr 0x808a:l
m68k_0138bc_end:
.org 0x138C2
m68k_0138c2:
        move.w 0xf378:w,%d0
m68k_0138c2_end:
.org 0x138C6
m68k_0138c6:
        lsl.w #0x1,%d0
m68k_0138c6_end:
.org 0x138C8
m68k_0138c8:
        lea.l 0xf4fe:w,%a0
m68k_0138c8_end:
.org 0x138CC
m68k_0138cc:
        move.w (%a0, %d0.w),%d0
m68k_0138cc_end:
.org 0x138D0
m68k_0138d0:
        lsl.w #0x2,%d0
m68k_0138d0_end:
.org 0x138D2
m68k_0138d2:
        lea.l 0xc800:w,%a0
m68k_0138d2_end:
.org 0x138D6
m68k_0138d6:
        move.l 0xf3ee:w,(%a0, %d0.w)
m68k_0138d6_end:
.org 0x138DC
m68k_0138dc:
        move.l 0xcfae:w,0xf3e4:w
m68k_0138dc_end:
.org 0x138E2
m68k_0138e2:
        move.w #0x208,0xf612:w
m68k_0138e2_end:
.org 0x138E8
m68k_0138e8:
        move.w #0x2,0xf362:w
m68k_0138e8_end:
.org 0x138EE
m68k_0138ee:
        move.w #0x12,0xf36a:w
m68k_0138ee_end:
.org 0x138F4
m68k_0138f4:
        bra.w (. + 58)
m68k_0138f4_end:
.org 0x138F8
m68k_0138f8:
        move.w 0xf378:w,%d0
m68k_0138f8_end:
.org 0x138FC
m68k_0138fc:
        lsl.w #0x1,%d0
m68k_0138fc_end:
.org 0x138FE
m68k_0138fe:
        lea.l 0xf4fe:w,%a0
m68k_0138fe_end:
.org 0x13902
m68k_013902:
        move.w (%a0, %d0.w),%d0
m68k_013902_end:
.org 0x13906
m68k_013906:
        lsl.w #0x2,%d0
m68k_013906_end:
.org 0x13908
m68k_013908:
        lea.l 0xc800:w,%a0
m68k_013908_end:
.org 0x1390C
m68k_01390c:
        move.l (%a0, %d0.w),0xf3ee:w
m68k_01390c_end:
.org 0x13912
m68k_013912:
        move.l 0xf3e4:w,0xcfae:w
m68k_013912_end:
.org 0x13918
m68k_013918:
        move.w #0x208,0xf612:w
m68k_013918_end:
.org 0x1391E
m68k_01391e:
        move.w #0x2,0xf362:w
m68k_01391e_end:
.org 0x13924
m68k_013924:
        move.w #0x12,0xf36a:w
m68k_013924_end:
.org 0x1392A
m68k_01392a:
        bsr.w (. + -480)
m68k_01392a_end:
.org 0x1392E
m68k_01392e:
        bsr.w (. + -570)
m68k_01392e_end:
.org 0x13932
m68k_013932:
        rts
m68k_013932_end:
.org 0x13AB6
m68k_013ab6:
        bsr.w (. + 208)
m68k_013ab6_end:
.org 0x13ABA
m68k_013aba:
        bsr.w (. + 288)
m68k_013aba_end:
.org 0x13ABE
m68k_013abe:
        tst.w 0xcfd2:w
m68k_013abe_end:
.org 0x13AC2
m68k_013ac2:
        beq.w (. + 28)
m68k_013ac2_end:
.org 0x13AC6
m68k_013ac6:
        subq.w #0x1,0xcfd2:w
m68k_013ac6_end:
.org 0x13ACA
m68k_013aca:
        cmpi.w #0x8,0xcfd2:w
m68k_013aca_end:
.org 0x13AD0
m68k_013ad0:
        bcs.w (. + 118)
m68k_013ad0_end:
.org 0x13AD4
m68k_013ad4:
        move.w #0x8,0xcfd2:w
m68k_013ad4_end:
.org 0x13ADA
m68k_013ada:
        bra.w (. + 108)
m68k_013ada_end:
.org 0x13ADE
m68k_013ade:
        btst.b #0x5,0xf603:w
m68k_013ade_end:
.org 0x13AE4
m68k_013ae4:
        beq.b (. + 98)
m68k_013ae4_end:
.org 0x13AE6
m68k_013ae6:
        lea.l 0xdffc:w,%a0
m68k_013ae6_end:
.org 0x13AEA
m68k_013aea:
        lea.l 0xe09c:w,%a1
m68k_013aea_end:
.org 0x13AEE
m68k_013aee:
        move.w 0xf364:w,%d0
m68k_013aee_end:
.org 0x13AF2
m68k_013af2:
        lsl.w #0x2,%d0
m68k_013af2_end:
.org 0x13AF4
m68k_013af4:
        move.l (%a0, %d0.w),%d2
m68k_013af4_end:
.org 0x13AF8
m68k_013af8:
        move.l (%a1, %d0.w),%d3
m68k_013af8_end:
.org 0x13AFC
m68k_013afc:
        lea.l 106(%pc),%a2
m68k_013afc_end:
.org 0x13B00
m68k_013b00:
        nop
m68k_013b00_end:
.org 0x13B02
m68k_013b02:
        move.w 0xf688:w,%d1
m68k_013b02_end:
.org 0x13B06
m68k_013b06:
        lsl.w #0x3,%d1
m68k_013b06_end:
.org 0x13B08
m68k_013b08:
        move.w #0xbd,%d0
m68k_013b08_end:
.org 0x13B0C
m68k_013b0c:
        move.l (%a2, %d1.w),0xf39e:w
m68k_013b0c_end:
.org 0x13B12
m68k_013b12:
        cmp.l 0xf39e:w,%d2
m68k_013b12_end:
.org 0x13B16
m68k_013b16:
        bcs.b (. + 40)
m68k_013b16_end:
.org 0x13B18
m68k_013b18:
        move.w #0xc7,%d0
m68k_013b18_end:
.org 0x13B1C
m68k_013b1c:
        move.l 0x4(%a2, %d1.w),0xf3ba:w
m68k_013b1c_end:
.org 0x13B22
m68k_013b22:
        cmp.l 0xf3ba:w,%d3
m68k_013b22_end:
.org 0x13B26
m68k_013b26:
        bcs.b (. + 24)
m68k_013b26_end:
.org 0x13B28
m68k_013b28:
        jsr 0xc0b6:l
m68k_013b28_end:
.org 0x13B2E
m68k_013b2e:
        move.w #0x3,0xf362:w
m68k_013b2e_end:
.org 0x13B34
m68k_013b34:
        move.w #0x12,0xf36a:w
m68k_013b34_end:
.org 0x13B3A
m68k_013b3a:
        bra.w (. + 44)
m68k_013b3a_end:
.org 0x13B3E
m68k_013b3e:
        jsr 0x676f2:l
m68k_013b3e_end:
.org 0x13B44
m68k_013b44:
        bra.b (. + 34)
m68k_013b44_end:
.org 0x13B46
m68k_013b46:
        btst.b #0x4,0xf603:w
m68k_013b46_end:
.org 0x13B4C
m68k_013b4c:
        beq.w (. + 26)
m68k_013b4c_end:
.org 0x13B50
m68k_013b50:
        move.w #0x208,0xf612:w
m68k_013b50_end:
.org 0x13B56
m68k_013b56:
        move.w #0x2,0xf362:w
m68k_013b56_end:
.org 0x13B5C
m68k_013b5c:
        move.w #0x12,0xf36a:w
m68k_013b5c_end:
.org 0x13B62
m68k_013b62:
        bsr.w (. + 284)
m68k_013b62_end:
.org 0x13B66
m68k_013b66:
        rts
m68k_013b66_end:
.org 0x14294
m68k_014294:
        lsr.w #0x4,%d0
m68k_014294_end:
.org 0x14296
m68k_014296:
        lsr.w #0x4,%d1
m68k_014296_end:
.org 0x14298
m68k_014298:
        bsr.w (. + 10)
m68k_014298_end:
.org 0x1429C
m68k_01429c:
        lsl.w #0x4,%d0
m68k_01429c_end:
.org 0x1429E
m68k_01429e:
        lsl.w #0x4,%d1
m68k_01429e_end:
.org 0x142A0
m68k_0142a0:
        rts
m68k_0142a0_end:
.org 0x142A2
m68k_0142a2:
        move.l %d0,-(%a7)
m68k_0142a2_end:
.org 0x142A4
m68k_0142a4:
        move.w %d0,%d2
m68k_0142a4_end:
.org 0x142A6
m68k_0142a6:
        lsl.w #0x3,%d2
m68k_0142a6_end:
.org 0x142A8
m68k_0142a8:
        add.w %d2,%d0
m68k_0142a8_end:
.org 0x142AA
m68k_0142aa:
        lsl.w #0x3,%d0
m68k_0142aa_end:
.org 0x142AC
m68k_0142ac:
        add.w %d1,%d0
m68k_0142ac_end:
.org 0x142AE
m68k_0142ae:
        lea.l 0xee5f0:l,%a2
m68k_0142ae_end:
.org 0x142B4
m68k_0142b4:
        clr.w %d2
m68k_0142b4_end:
.org 0x142B6
m68k_0142b6:
        move.b (%a2, %d0.w),%d2
m68k_0142b6_end:
.org 0x142BA
m68k_0142ba:
        lea.l 0x670a:l,%a2
m68k_0142ba_end:
.org 0x142C0
m68k_0142c0:
        clr.w %d3
m68k_0142c0_end:
.org 0x142C2
m68k_0142c2:
        move.b (%a2, %d2.w),%d3
m68k_0142c2_end:
.org 0x142C6
m68k_0142c6:
        move.l (%a7)+,%d0
m68k_0142c6_end:
.org 0x142C8
m68k_0142c8:
        rts
m68k_0142c8_end:
.org 0x14D64
m68k_014d64:
        clr.w %d4
m68k_014d64_end:
.org 0x14D66
m68k_014d66:
        move.w 0xf314:w,%d3
m68k_014d66_end:
.org 0x14D6A
m68k_014d6a:
        cmp.w %d1,%d3
m68k_014d6a_end:
.org 0x14D6C
m68k_014d6c:
        beq.b (. + 90)
m68k_014d6c_end:
.org 0x14D6E
m68k_014d6e:
        bhi.b (. + 56)
m68k_014d6e_end:
.org 0x14D70
m68k_014d70:
        cmpi.w #0x3a0,%d3
m68k_014d70_end:
.org 0x14D74
m68k_014d74:
        beq.w (. + 82)
m68k_014d74_end:
.org 0x14D78
m68k_014d78:
        addq.w #0x3,%d3
m68k_014d78_end:
.org 0x14D7A
m68k_014d7a:
        cmp.w %d1,%d3
m68k_014d7a_end:
.org 0x14D7C
m68k_014d7c:
        bls.b (. + 4)
m68k_014d7c_end:
.org 0x14D7E
m68k_014d7e:
        move.w %d1,%d3
m68k_014d7e_end:
.org 0x14D80
m68k_014d80:
        cmpi.w #0x3a0,%d3
m68k_014d80_end:
.org 0x14D84
m68k_014d84:
        bls.b (. + 6)
m68k_014d84_end:
.org 0x14D8A
m68k_014d8a:
        move.w %d3,0xf314:w
m68k_014d8a_end:
.org 0x14D8E
m68k_014d8e:
        addq.w #0x1,%d4
m68k_014d8e_end:
.org 0x14D90
m68k_014d90:
        addi.w #0xe0,%d3
m68k_014d90_end:
.org 0x14D94
m68k_014d94:
        movea.w %d3,%a5
m68k_014d94_end:
.org 0x14D96
m68k_014d96:
        move.w %d4,-(%a7)
m68k_014d96_end:
.org 0x14D98
m68k_014d98:
        move.w %d2,-(%a7)
m68k_014d98_end:
.org 0x14D9A
m68k_014d9a:
        jsr 0xa0cc:l
m68k_014d9a_end:
.org 0x14DA0
m68k_014da0:
        move.w (%a7)+,%d2
m68k_014da0_end:
.org 0x14DA2
m68k_014da2:
        move.w (%a7)+,%d4
m68k_014da2_end:
.org 0x14DA4
m68k_014da4:
        bra.b (. + 34)
m68k_014da4_end:
.org 0x14DC6
m68k_014dc6:
        move.w 0xf318:w,%d3
m68k_014dc6_end:
.org 0x14DCA
m68k_014dca:
        cmp.w %d2,%d3
m68k_014dca_end:
.org 0x14DCC
m68k_014dcc:
        beq.b (. + 82)
m68k_014dcc_end:
.org 0x14DCE
m68k_014dce:
        bhi.b (. + 52)
m68k_014dce_end:
.org 0x14DD0
m68k_014dd0:
        cmpi.w #0x340,%d3
m68k_014dd0_end:
.org 0x14DD4
m68k_014dd4:
        beq.b (. + 74)
m68k_014dd4_end:
.org 0x14DD6
m68k_014dd6:
        addq.w #0x4,%d3
m68k_014dd6_end:
.org 0x14DD8
m68k_014dd8:
        cmp.w %d2,%d3
m68k_014dd8_end:
.org 0x14DDA
m68k_014dda:
        bls.b (. + 4)
m68k_014dda_end:
.org 0x14DDE
m68k_014dde:
        cmpi.w #0x340,%d3
m68k_014dde_end:
.org 0x14DE2
m68k_014de2:
        bls.b (. + 6)
m68k_014de2_end:
.org 0x14DE8
m68k_014de8:
        move.w %d3,0xf318:w
m68k_014de8_end:
.org 0x14DEC
m68k_014dec:
        addq.w #0x1,%d4
m68k_014dec_end:
.org 0x14DEE
m68k_014dee:
        addi.w #0x140,%d3
m68k_014dee_end:
.org 0x14DF2
m68k_014df2:
        movea.w %d3,%a5
m68k_014df2_end:
.org 0x14DF4
m68k_014df4:
        move.w %d4,-(%a7)
m68k_014df4_end:
.org 0x14DF6
m68k_014df6:
        jsr 0xa10c:l
m68k_014df6_end:
.org 0x14DFC
m68k_014dfc:
        move.w (%a7)+,%d4
m68k_014dfc_end:
.org 0x14DFE
m68k_014dfe:
        bra.w (. + 32)
m68k_014dfe_end:
.org 0x14E02
m68k_014e02:
        subq.w #0x4,%d3
m68k_014e02_end:
.org 0x14E04
m68k_014e04:
        bcs.b (. + 6)
m68k_014e04_end:
.org 0x14E06
m68k_014e06:
        cmp.w %d2,%d3
m68k_014e06_end:
.org 0x14E08
m68k_014e08:
        bcc.b (. + 4)
m68k_014e08_end:
.org 0x14E0A
m68k_014e0a:
        move.w %d2,%d3
m68k_014e0a_end:
.org 0x14E0C
m68k_014e0c:
        move.w %d3,0xf318:w
m68k_014e0c_end:
.org 0x14E10
m68k_014e10:
        addq.w #0x1,%d4
m68k_014e10_end:
.org 0x14E12
m68k_014e12:
        movea.w %d3,%a5
m68k_014e12_end:
.org 0x14E14
m68k_014e14:
        move.w %d4,-(%a7)
m68k_014e14_end:
.org 0x14E16
m68k_014e16:
        jsr 0xa10c:l
m68k_014e16_end:
.org 0x14E1C
m68k_014e1c:
        move.w (%a7)+,%d4
m68k_014e1c_end:
.org 0x14E1E
m68k_014e1e:
        rts
m68k_014e1e_end:
.org 0x15DE6
m68k_015de6:
        lea.l 0x9000:w,%a2
m68k_015de6_end:
.org 0x15DEA
m68k_015dea:
        move.b (%a2),%d4
m68k_015dea_end:
.org 0x15DEC
m68k_015dec:
        beq.w (. + 76)
m68k_015dec_end:
.org 0x15E38
m68k_015e38:
        bsr.w (. + 228)
m68k_015e38_end:
.org 0x15E3C
m68k_015e3c:
        rts
m68k_015e3c_end:
.org 0x15F1C
m68k_015f1c:
        lea.l 0x9f00:w,%a1
m68k_015f1c_end:
.org 0x15F20
m68k_015f20:
        move.w (%a1)+,%d0
m68k_015f20_end:
.org 0x15F22
m68k_015f22:
        bmi.b (. + 70)
m68k_015f22_end:
.org 0x15F68
m68k_015f68:
        rts
m68k_015f68_end:
.org 0x16660
m68k_016660:
        move.w 0xf362:w,%d0
m68k_016660_end:
.org 0x16664
m68k_016664:
        lsl.w #0x1,%d0
m68k_016664_end:
.org 0x16666
m68k_016666:
        move.w 8(%pc, %d0.w),%d0
m68k_016666_end:
.org 0x1666A
m68k_01666a:
        jsr 12(%pc, %d0.w)
m68k_01666a_end:
.org 0x1666E
m68k_01666e:
        rts
m68k_01666e_end:
.org 0x16678
m68k_016678:
        jsr 0x662e4:l
m68k_016678_end:
.org 0x1667E
m68k_01667e:
        bcs.w (. + 122)
m68k_01667e_end:
.org 0x16682
m68k_016682:
        btst.b #0x6,0xf3a4:w
m68k_016682_end:
.org 0x16688
m68k_016688:
        bne.w (. + 132)
m68k_016688_end:
.org 0x1668C
m68k_01668c:
        cmpi.w #0x28,0xcea0:w
m68k_01668c_end:
.org 0x16692
m68k_016692:
        bcc.w (. + 32)
m68k_016692_end:
.org 0x16696
m68k_016696:
        lea.l 0xce00:w,%a0
m68k_016696_end:
.org 0x1669A
m68k_01669a:
        move.w 0xcea0:w,%d0
m68k_01669a_end:
.org 0x1669E
m68k_01669e:
        lsl.w #0x2,%d0
m68k_01669e_end:
.org 0x166A0
m68k_0166a0:
        tst.b (%a0, %d0.w)
m68k_0166a0_end:
.org 0x166A4
m68k_0166a4:
        bne.b (. + 74)
m68k_0166a4_end:
.org 0x166A6
m68k_0166a6:
        addq.w #0x1,0xcea0:w
m68k_0166a6_end:
.org 0x166AA
m68k_0166aa:
        cmpi.w #0x28,0xcea0:w
m68k_0166aa_end:
.org 0x166B0
m68k_0166b0:
        bcs.b (. + -22)
m68k_0166b0_end:
.org 0x166B2
m68k_0166b2:
        move.w #0x2,0xf36c:w
m68k_0166b2_end:
.org 0x166B8
m68k_0166b8:
        move.w #0x201,0xf612:w
m68k_0166b8_end:
.org 0x166BE
m68k_0166be:
        move.w #0xfffe,0xf376:w
m68k_0166be_end:
.org 0x166C4
m68k_0166c4:
        addq.b #0x1,0xf375:w
m68k_0166c4_end:
.org 0x166C8
m68k_0166c8:
        cmpi.b #0xc,0xf375:w
m68k_0166c8_end:
.org 0x166CE
m68k_0166ce:
        bcs.b (. + 10)
m68k_0166ce_end:
.org 0x166D0
m68k_0166d0:
        addq.b #0x1,0xf374:w
m68k_0166d0_end:
.org 0x166D4
m68k_0166d4:
        clr.b 0xf375:w
m68k_0166d4_end:
.org 0x166D8
m68k_0166d8:
        move.w #0x80,0xf600:w
m68k_0166d8_end:
.org 0x166DE
m68k_0166de:
        move.w #0x85,0xf380:w
m68k_0166de_end:
.org 0x166E4
m68k_0166e4:
        jsr 0x5c98:l
m68k_0166e4_end:
.org 0x166EA
m68k_0166ea:
        bra.w (. + 64)
m68k_0166ea_end:
.org 0x166EE
m68k_0166ee:
        move.w #0x7c,0xf600:w
m68k_0166ee_end:
.org 0x166F4
m68k_0166f4:
        bra.w (. + 54)
m68k_0166f4_end:
.org 0x166F8
m68k_0166f8:
        move.w #0x3,0xf362:w
m68k_0166f8_end:
.org 0x166FE
m68k_0166fe:
        move.w #0x9c,%d0
m68k_0166fe_end:
.org 0x16702
m68k_016702:
        jsr 0x676f2:l
m68k_016702_end:
.org 0x16708
m68k_016708:
        bra.w (. + 34)
m68k_016708_end:
.org 0x1670C
m68k_01670c:
        move.l #0xc0000026,%d0
m68k_01670c_end:
.org 0x16712
m68k_016712:
        move.w #0x7,%d1
m68k_016712_end:
.org 0x16716
m68k_016716:
        move.w #0xca02,%d2
m68k_016716_end:
.org 0x1671A
m68k_01671a:
        lea.l 16(%pc),%a0
m68k_01671a_end:
.org 0x1671E
m68k_01671e:
        jsr 0x26bfa:l
m68k_01671e_end:
.org 0x16724
m68k_016724:
        bclr.b #0x6,0xf3a4:w
m68k_016724_end:
.org 0x1672A
m68k_01672a:
        rts
m68k_01672a_end:
.org 0x16748
m68k_016748:
        jsr 0x1264:l
m68k_016748_end:
.org 0x1674E
m68k_01674e:
        move.w 0xcea0:w,%d0
m68k_01674e_end:
.org 0x16752
m68k_016752:
        lsl.w #0x2,%d0
m68k_016752_end:
.org 0x16754
m68k_016754:
        lea.l 0xce00:w,%a0
m68k_016754_end:
.org 0x16758
m68k_016758:
        clr.w %d1
m68k_016758_end:
.org 0x1675A
m68k_01675a:
        move.b 0x1(%a0, %d0.w),%d1
m68k_01675a_end:
.org 0x1675E
m68k_01675e:
        lsl.w #0x4,%d1
m68k_01675e_end:
.org 0x16760
m68k_016760:
        move.w %d1,0xcea4:w
m68k_016760_end:
.org 0x16764
m68k_016764:
        move.w %d1,0xcea8:w
m68k_016764_end:
.org 0x16768
m68k_016768:
        subi.w #0x70,%d1
m68k_016768_end:
.org 0x1676C
m68k_01676c:
        bcc.b (. + 4)
m68k_01676c_end:
.org 0x1676E
m68k_01676e:
        clr.w %d1
m68k_01676e_end:
.org 0x16770
m68k_016770:
        clr.w %d2
m68k_016770_end:
.org 0x16772
m68k_016772:
        move.b 0x2(%a0, %d0.w),%d2
m68k_016772_end:
.org 0x16776
m68k_016776:
        lsl.w #0x4,%d2
m68k_016776_end:
.org 0x16778
m68k_016778:
        move.w %d2,0xcea6:w
m68k_016778_end:
.org 0x1677C
m68k_01677c:
        move.w %d2,0xceaa:w
m68k_01677c_end:
.org 0x16780
m68k_016780:
        subi.w #0xa0,%d2
m68k_016780_end:
.org 0x16784
m68k_016784:
        bcc.b (. + 4)
m68k_016784_end:
.org 0x16786
m68k_016786:
        clr.w %d2
m68k_016786_end:
.org 0x16788
m68k_016788:
        jsr 0x14d64:l
m68k_016788_end:
.org 0x1678E
m68k_01678e:
        tst.w %d4
m68k_01678e_end:
.org 0x16790
m68k_016790:
        bne.b (. + 6)
m68k_016790_end:
.org 0x16792
m68k_016792:
        addq.w #0x1,0xf362:w
m68k_016792_end:
.org 0x16796
m68k_016796:
        rts
m68k_016796_end:
.org 0x16798
m68k_016798:
        move.w 0xcea0:w,%d0
m68k_016798_end:
.org 0x1679C
m68k_01679c:
        lsl.w #0x2,%d0
m68k_01679c_end:
.org 0x1679E
m68k_01679e:
        lea.l 0xce00:w,%a6
m68k_01679e_end:
.org 0x167A2
m68k_0167a2:
        adda.w %d0,%a6
m68k_0167a2_end:
.org 0x167A4
m68k_0167a4:
        andi.b #0x83,(%a6)
m68k_0167a4_end:
.org 0x167A8
m68k_0167a8:
        move.w 0xcea4:w,%d0
m68k_0167a8_end:
.org 0x167AC
m68k_0167ac:
        andi.w #0xf,%d0
m68k_0167ac_end:
.org 0x167B0
m68k_0167b0:
        bne.b (. + 104)
m68k_0167b0_end:
.org 0x167B2
m68k_0167b2:
        move.w 0xcea6:w,%d0
m68k_0167b2_end:
.org 0x167B6
m68k_0167b6:
        andi.w #0xf,%d0
m68k_0167b6_end:
.org 0x167BA
m68k_0167ba:
        bne.b (. + 94)
m68k_0167ba_end:
.org 0x167BC
m68k_0167bc:
        move.w 0xcea4:w,%d0
m68k_0167bc_end:
.org 0x167C0
m68k_0167c0:
        lsr.w #0x4,%d0
m68k_0167c0_end:
.org 0x167C2
m68k_0167c2:
        move.b %d0,0x1(%a6)
m68k_0167c2_end:
.org 0x167C6
m68k_0167c6:
        move.w 0xcea6:w,%d0
m68k_0167c6_end:
.org 0x167CA
m68k_0167ca:
        lsr.w #0x4,%d0
m68k_0167ca_end:
.org 0x167CC
m68k_0167cc:
        move.b %d0,0x2(%a6)
m68k_0167cc_end:
.org 0x167D0
m68k_0167d0:
        bsr.w (. + 164)
m68k_0167d0_end:
.org 0x167D4
m68k_0167d4:
        bcs.w (. + 56)
m68k_0167d4_end:
.org 0x167D8
m68k_0167d8:
        bsr.w (. + 330)
m68k_0167d8_end:
.org 0x167DC
m68k_0167dc:
        bcs.w (. + 48)
m68k_0167dc_end:
.org 0x167E0
m68k_0167e0:
        bsr.w (. + 358)
m68k_0167e0_end:
.org 0x167E4
m68k_0167e4:
        bcs.w (. + 40)
m68k_0167e4_end:
.org 0x167E8
m68k_0167e8:
        move.w 0xcea4:w,%d0
m68k_0167e8_end:
.org 0x167EC
m68k_0167ec:
        move.w 0xcea6:w,%d1
m68k_0167ec_end:
.org 0x167F0
m68k_0167f0:
        jsr 0x14294:l
m68k_0167f0_end:
.org 0x167F6
m68k_0167f6:
        cmpi.b #0x4,%d2
m68k_0167f6_end:
.org 0x167FA
m68k_0167fa:
        beq.w (. + 30)
m68k_0167fa_end:
.org 0x167FE
m68k_0167fe:
        move.w #0xa4,%d0
m68k_0167fe_end:
.org 0x16802
m68k_016802:
        jsr 0x808a:l
m68k_016802_end:
.org 0x16808
m68k_016808:
        bra.w (. + 16)
m68k_016808_end:
.org 0x1680C
m68k_01680c:
        addq.w #0x1,0xcea0:w
m68k_01680c_end:
.org 0x16810
m68k_016810:
        clr.w 0xf362:w
m68k_016810_end:
.org 0x16814
m68k_016814:
        bra.w (. + 94)
m68k_016814_end:
.org 0x16818
m68k_016818:
        move.w 0xcea4:w,%d0
m68k_016818_end:
.org 0x1681C
m68k_01681c:
        cmp.w 0xcea8:w,%d0
m68k_01681c_end:
.org 0x16820
m68k_016820:
        beq.w (. + 24)
m68k_016820_end:
.org 0x16824
m68k_016824:
        bcs.w (. + 12)
m68k_016824_end:
.org 0x16828
m68k_016828:
        subq.w #0x1,0xcea4:w
m68k_016828_end:
.org 0x1682C
m68k_01682c:
        bra.w (. + 40)
m68k_01682c_end:
.org 0x16830
m68k_016830:
        addq.w #0x1,0xcea4:w
m68k_016830_end:
.org 0x16834
m68k_016834:
        bra.w (. + 32)
m68k_016834_end:
.org 0x16838
m68k_016838:
        move.w 0xcea6:w,%d0
m68k_016838_end:
.org 0x1683C
m68k_01683c:
        cmp.w 0xceaa:w,%d0
m68k_01683c_end:
.org 0x16840
m68k_016840:
        bhi.b (. + 12)
m68k_016840_end:
.org 0x16842
m68k_016842:
        addq.w #0x1,0xcea6:w
m68k_016842_end:
.org 0x16846
m68k_016846:
        ori.b #0x80,(%a6)
m68k_016846_end:
.org 0x1684A
m68k_01684a:
        bra.b (. + 10)
m68k_01684a_end:
.org 0x1684C
m68k_01684c:
        andi.b #0x7f,(%a6)
m68k_01684c_end:
.org 0x16850
m68k_016850:
        subq.w #0x1,0xcea6:w
m68k_016850_end:
.org 0x16854
m68k_016854:
        move.w 0xcea4:w,%d1
m68k_016854_end:
.org 0x16858
m68k_016858:
        subi.w #0x68,%d1
m68k_016858_end:
.org 0x1685C
m68k_01685c:
        bcc.b (. + 4)
m68k_01685c_end:
.org 0x1685E
m68k_01685e:
        clr.w %d1
m68k_01685e_end:
.org 0x16860
m68k_016860:
        move.w 0xcea6:w,%d2
m68k_016860_end:
.org 0x16864
m68k_016864:
        subi.w #0x98,%d2
m68k_016864_end:
.org 0x16868
m68k_016868:
        bcc.b (. + 4)
m68k_016868_end:
.org 0x1686A
m68k_01686a:
        clr.w %d2
m68k_01686a_end:
.org 0x1686C
m68k_01686c:
        jsr 0x14d64:l
m68k_01686c_end:
.org 0x16872
m68k_016872:
        rts
m68k_016872_end:
.org 0x16874
m68k_016874:
        lea.l 0xff4000:l,%a0
m68k_016874_end:
.org 0x1687A
m68k_01687a:
        adda.w 0xceac:w,%a0
m68k_01687a_end:
.org 0x1687E
m68k_01687e:
        addq.w #0x1,0xceac:w
m68k_01687e_end:
.org 0x16882
m68k_016882:
        tst.b 0x1(%a0)
m68k_016882_end:
.org 0x16886
m68k_016886:
        bmi.b (. + 64)
m68k_016886_end:
.org 0x16888
m68k_016888:
        move.b (%a0),%d0
m68k_016888_end:
.org 0x1688A
m68k_01688a:
        subq.b #0x1,%d0
m68k_01688a_end:
.org 0x1688C
m68k_01688c:
        beq.b (. + 18)
m68k_01688c_end:
.org 0x1688E
m68k_01688e:
        subq.b #0x1,%d0
m68k_01688e_end:
.org 0x16890
m68k_016890:
        beq.b (. + 22)
m68k_016890_end:
.org 0x16892
m68k_016892:
        subq.b #0x1,%d0
m68k_016892_end:
.org 0x16894
m68k_016894:
        beq.b (. + 28)
m68k_016894_end:
.org 0x16896
m68k_016896:
        clr.w %d0
m68k_016896_end:
.org 0x16898
m68k_016898:
        move.w #0xfff0,%d1
m68k_016898_end:
.org 0x1689C
m68k_01689c:
        bra.b (. + 26)
m68k_01689c_end:
.org 0x1689E
m68k_01689e:
        move.w #0xfff0,%d0
m68k_01689e_end:
.org 0x168A2
m68k_0168a2:
        clr.w %d1
m68k_0168a2_end:
.org 0x168A4
m68k_0168a4:
        bra.b (. + 18)
m68k_0168a4_end:
.org 0x168A6
m68k_0168a6:
        clr.w %d0
m68k_0168a6_end:
.org 0x168A8
m68k_0168a8:
        move.w #0x10,%d1
m68k_0168a8_end:
.org 0x168AC
m68k_0168ac:
        bra.w (. + 10)
m68k_0168ac_end:
.org 0x168B0
m68k_0168b0:
        move.w #0x10,%d0
m68k_0168b0_end:
.org 0x168B4
m68k_0168b4:
        clr.w %d1
m68k_0168b4_end:
.org 0x168B6
m68k_0168b6:
        add.w %d0,0xcea8:w
m68k_0168b6_end:
.org 0x168BA
m68k_0168ba:
        add.w %d1,0xceaa:w
m68k_0168ba_end:
.org 0x168BE
m68k_0168be:
        andi.w #0xfffe,%sr
m68k_0168be_end:
.org 0x168C2
m68k_0168c2:
        bra.w (. + 94)
m68k_0168c2_end:
.org 0x168C6
m68k_0168c6:
        clr.w %d2
m68k_0168c6_end:
.org 0x168C8
m68k_0168c8:
        move.b (%a6),%d2
m68k_0168c8_end:
.org 0x168CA
m68k_0168ca:
        andi.w #0x3,%d2
m68k_0168ca_end:
.org 0x168CE
m68k_0168ce:
        lsl.w #0x3,%d2
m68k_0168ce_end:
.org 0x168D0
m68k_0168d0:
        clr.w %d1
m68k_0168d0_end:
.org 0x168D2
m68k_0168d2:
        move.b 0x3(%a6),%d1
m68k_0168d2_end:
.org 0x168D6
m68k_0168d6:
        lsl.w #0x2,%d1
m68k_0168d6_end:
.org 0x168D8
m68k_0168d8:
        lea.l 0x13b60:l,%a1
m68k_0168d8_end:
.org 0x168DE
m68k_0168de:
        move.l (%a1, %d2.w),%d3
m68k_0168de_end:
.org 0x168E2
m68k_0168e2:
        lea.l 0xdffc:w,%a2
m68k_0168e2_end:
.org 0x168E6
m68k_0168e6:
        add.l (%a2, %d1.w),%d3
m68k_0168e6_end:
.org 0x168EA
m68k_0168ea:
        cmpi.l #0xf423f,%d3
m68k_0168ea_end:
.org 0x168F0
m68k_0168f0:
        bls.b (. + 8)
m68k_0168f0_end:
.org 0x168F2
m68k_0168f2:
        move.l #0xf423f,%d3
m68k_0168f2_end:
.org 0x168F8
m68k_0168f8:
        move.l %d3,(%a2, %d1.w)
m68k_0168f8_end:
.org 0x168FC
m68k_0168fc:
        move.l 0x4(%a1, %d2.w),%d3
m68k_0168fc_end:
.org 0x16900
m68k_016900:
        lea.l 0xe09c:w,%a2
m68k_016900_end:
.org 0x16904
m68k_016904:
        add.l (%a2, %d1.w),%d3
m68k_016904_end:
.org 0x16908
m68k_016908:
        cmpi.l #0xf423f,%d3
m68k_016908_end:
.org 0x1690E
m68k_01690e:
        bls.b (. + 8)
m68k_01690e_end:
.org 0x16910
m68k_016910:
        move.l #0xf423f,%d3
m68k_016910_end:
.org 0x16916
m68k_016916:
        move.l %d3,(%a2, %d1.w)
m68k_016916_end:
.org 0x1691A
m68k_01691a:
        clr.b (%a6)
m68k_01691a_end:
.org 0x1691C
m68k_01691c:
        ori.w #0x1,%sr
m68k_01691c_end:
.org 0x16920
m68k_016920:
        rts
m68k_016920_end:
.org 0x16922
m68k_016922:
        move.w 0xcea8:w,%d0
m68k_016922_end:
.org 0x16926
m68k_016926:
        move.w 0xceaa:w,%d1
m68k_016926_end:
.org 0x1692A
m68k_01692a:
        jsr 0x14294:l
m68k_01692a_end:
.org 0x16930
m68k_016930:
        tst.w %d3
m68k_016930_end:
.org 0x16932
m68k_016932:
        bmi.b (. + 14)
m68k_016932_end:
.org 0x16934
m68k_016934:
        sub.w %d3,0xcea2:w
m68k_016934_end:
.org 0x16938
m68k_016938:
        bcc.b (. + 8)
m68k_016938_end:
.org 0x1693A
m68k_01693a:
        ori.w #0x1,%sr
m68k_01693a_end:
.org 0x1693E
m68k_01693e:
        bra.b (. + 6)
m68k_01693e_end:
.org 0x16940
m68k_016940:
        andi.w #0xfffe,%sr
m68k_016940_end:
.org 0x16944
m68k_016944:
        rts
m68k_016944_end:
.org 0x16946
m68k_016946:
        move.w 0xcea8:w,%d0
m68k_016946_end:
.org 0x1694A
m68k_01694a:
        lsr.w #0x4,%d0
m68k_01694a_end:
.org 0x1694C
m68k_01694c:
        move.w 0xceaa:w,%d1
m68k_01694c_end:
.org 0x16950
m68k_016950:
        lsr.w #0x4,%d1
m68k_016950_end:
.org 0x16952
m68k_016952:
        lea.l 0xce00:w,%a0
m68k_016952_end:
.org 0x16956
m68k_016956:
        move.w #0x27,%d2
m68k_016956_end:
.org 0x1695A
m68k_01695a:
        tst.b (%a0)
m68k_01695a_end:
.org 0x1695C
m68k_01695c:
        beq.b (. + 24)
m68k_01695c_end:
.org 0x1695E
m68k_01695e:
        btst.b #0x4,(%a0)
m68k_01695e_end:
.org 0x16962
m68k_016962:
        bne.b (. + 18)
m68k_016962_end:
.org 0x16964
m68k_016964:
        cmp.b 0x1(%a0),%d0
m68k_016964_end:
.org 0x16968
m68k_016968:
        bne.b (. + 12)
m68k_016968_end:
.org 0x1696A
m68k_01696a:
        cmp.b 0x2(%a0),%d1
m68k_01696a_end:
.org 0x1696E
m68k_01696e:
        bne.b (. + 6)
m68k_01696e_end:
.org 0x16970
m68k_016970:
        bra.w (. + 52)
m68k_016970_end:
.org 0x16974
m68k_016974:
        addq.w #0x4,%a0
m68k_016974_end:
.org 0x16976
m68k_016976:
        dbra %d2,(. + -28)
m68k_016976_end:
.org 0x1697A
m68k_01697a:
        lea.l 0x9000:w,%a0
m68k_01697a_end:
.org 0x1697E
m68k_01697e:
        move.b (%a0),%d2
m68k_01697e_end:
.org 0x16980
m68k_016980:
        andi.w #0xf,%d2
m68k_016980_end:
.org 0x16984
m68k_016984:
        beq.b (. + 24)
m68k_016984_end:
.org 0x16986
m68k_016986:
        cmp.b 0x1(%a0),%d0
m68k_016986_end:
.org 0x1698A
m68k_01698a:
        bne.b (. + 12)
m68k_01698a_end:
.org 0x1698C
m68k_01698c:
        cmp.b 0x2(%a0),%d1
m68k_01698c_end:
.org 0x16990
m68k_016990:
        bne.b (. + 6)
m68k_016990_end:
.org 0x16992
m68k_016992:
        bra.w (. + 18)
m68k_016992_end:
.org 0x16996
m68k_016996:
        lea.l 0xd(%a0, %d2.w),%a0
m68k_016996_end:
.org 0x1699A
m68k_01699a:
        bra.b (. + -28)
m68k_01699a_end:
.org 0x1699C
m68k_01699c:
        andi.w #0xfffe,%sr
m68k_01699c_end:
.org 0x169A0
m68k_0169a0:
        bra.w (. + 8)
m68k_0169a0_end:
.org 0x169A4
m68k_0169a4:
        ori.w #0x1,%sr
m68k_0169a4_end:
.org 0x169A8
m68k_0169a8:
        rts
m68k_0169a8_end:
.org 0x169AA
m68k_0169aa:
        lea.l 0xce9c:w,%a2
m68k_0169aa_end:
.org 0x169AE
m68k_0169ae:
        move.w #0x27,%d3
m68k_0169ae_end:
.org 0x169B2
m68k_0169b2:
        tst.b (%a2)
m68k_0169b2_end:
.org 0x169B4
m68k_0169b4:
        beq.b (. + 72)
m68k_0169b4_end:
.org 0x169B6
m68k_0169b6:
        btst.b #0x4,(%a2)
m68k_0169b6_end:
.org 0x169BA
m68k_0169ba:
        bne.b (. + 66)
m68k_0169ba_end:
.org 0x169BC
m68k_0169bc:
        clr.w %d0
m68k_0169bc_end:
.org 0x169BE
m68k_0169be:
        move.b 0x1(%a2),%d0
m68k_0169be_end:
.org 0x169C2
m68k_0169c2:
        lsl.w #0x4,%d0
m68k_0169c2_end:
.org 0x169C4
m68k_0169c4:
        move.w %d0,%d2
m68k_0169c4_end:
.org 0x169C6
m68k_0169c6:
        addi.w #0x10,%d2
m68k_0169c6_end:
.org 0x169CA
m68k_0169ca:
        sub.w 0xf314:w,%d2
m68k_0169ca_end:
.org 0x169CE
m68k_0169ce:
        bcs.w (. + 46)
m68k_0169ce_end:
.org 0x169D2
m68k_0169d2:
        cmpi.w #0xf0,%d2
m68k_0169d2_end:
.org 0x169D6
m68k_0169d6:
        bhi.w (. + 38)
m68k_0169d6_end:
.org 0x169DA
m68k_0169da:
        clr.w %d1
m68k_0169da_end:
.org 0x169DC
m68k_0169dc:
        move.b 0x2(%a2),%d1
m68k_0169dc_end:
.org 0x169E0
m68k_0169e0:
        lsl.w #0x4,%d1
m68k_0169e0_end:
.org 0x169E2
m68k_0169e2:
        move.w %d1,%d2
m68k_0169e2_end:
.org 0x169E4
m68k_0169e4:
        addi.w #0x10,%d2
m68k_0169e4_end:
.org 0x169E8
m68k_0169e8:
        sub.w 0xf318:w,%d2
m68k_0169e8_end:
.org 0x169EC
m68k_0169ec:
        bcs.w (. + 16)
m68k_0169ec_end:
.org 0x169F0
m68k_0169f0:
        cmpi.w #0x150,%d2
m68k_0169f0_end:
.org 0x169F4
m68k_0169f4:
        bhi.w (. + 8)
m68k_0169f4_end:
.org 0x169F8
m68k_0169f8:
        bsr.w (. + 12)
m68k_0169f8_end:
.org 0x169FC
m68k_0169fc:
        subq.w #0x4,%a2
m68k_0169fc_end:
.org 0x169FE
m68k_0169fe:
        dbra %d3,(. + -76)
m68k_0169fe_end:
.org 0x16A02
m68k_016a02:
        rts
m68k_016a02_end:
.org 0x16A04
m68k_016a04:
        move.l %d3,-(%a7)
m68k_016a04_end:
.org 0x16A06
m68k_016a06:
        cmpi.w #0x20a,0xf612:w
m68k_016a06_end:
.org 0x16A0C
m68k_016a0c:
        bne.b (. + 24)
m68k_016a0c_end:
.org 0x16A0E
m68k_016a0e:
        cmpi.w #0x2,0xf362:w
m68k_016a0e_end:
.org 0x16A14
m68k_016a14:
        bne.b (. + 16)
m68k_016a14_end:
.org 0x16A16
m68k_016a16:
        cmp.w 0xcea0:w,%d3
m68k_016a16_end:
.org 0x16A1A
m68k_016a1a:
        bne.b (. + 10)
m68k_016a1a_end:
.org 0x16A1C
m68k_016a1c:
        move.w 0xcea4:w,%d0
m68k_016a1c_end:
.org 0x16A20
m68k_016a20:
        move.w 0xcea6:w,%d1
m68k_016a20_end:
.org 0x16A24
m68k_016a24:
        lea.l 82(%pc),%a0
m68k_016a24_end:
.org 0x16A28
m68k_016a28:
        nop
m68k_016a28_end:
.org 0x16A2A
m68k_016a2a:
        btst.b #0x4,0xf321:w
m68k_016a2a_end:
.org 0x16A30
m68k_016a30:
        bne.w (. + 8)
m68k_016a30_end:
.org 0x16A34
m68k_016a34:
        adda.w #0x8,%a0
m68k_016a34_end:
.org 0x16A38
m68k_016a38:
        movem.l %d0-%d1/%a0/%a2,-(%a7)
m68k_016a38_end:
.org 0x16A3C
m68k_016a3c:
        addq.w #0x8,%d0
m68k_016a3c_end:
.org 0x16A3E
m68k_016a3e:
        addq.w #0x8,%d1
m68k_016a3e_end:
.org 0x16A40
m68k_016a40:
        bsr.w (. + -10156)
m68k_016a40_end:
.org 0x16A44
m68k_016a44:
        movem.l (%a7)+,%d0-%d1/%a0/%a2
m68k_016a44_end:
.org 0x16A48
m68k_016a48:
        cmpi.w #0x4,%d2
m68k_016a48_end:
.org 0x16A4C
m68k_016a4c:
        bne.w (. + 8)
m68k_016a4c_end:
.org 0x16A54
m68k_016a54:
        addq.w #0x8,%d1
m68k_016a54_end:
.org 0x16A56
m68k_016a56:
        clr.w %d2
m68k_016a56_end:
.org 0x16A58
m68k_016a58:
        tst.b (%a2)
m68k_016a58_end:
.org 0x16A5A
m68k_016a5a:
        bpl.w (. + 8)
m68k_016a5a_end:
.org 0x16A62
m68k_016a62:
        move.w 0xf314:w,0xf60a:w
m68k_016a62_end:
.org 0x16A68
m68k_016a68:
        move.w 0xf318:w,0xf60e:w
m68k_016a68_end:
.org 0x16A6E
m68k_016a6e:
        jsr 0xac10:l
m68k_016a6e_end:
.org 0x16A74
m68k_016a74:
        move.l (%a7)+,%d3
m68k_016a74_end:
.org 0x16A76
m68k_016a76:
        rts
m68k_016a76_end:
.org 0x16ACC
m68k_016acc:
        move.w 0xcea0:w,%d0
m68k_016acc_end:
.org 0x16AD0
m68k_016ad0:
        lsl.w #0x2,%d0
m68k_016ad0_end:
.org 0x16AD2
m68k_016ad2:
        lea.l 0xce00:w,%a0
m68k_016ad2_end:
.org 0x16AD6
m68k_016ad6:
        move.w #0xf,%d1
m68k_016ad6_end:
.org 0x16ADA
m68k_016ada:
        move.b (%a0, %d0.w),%d2
m68k_016ada_end:
.org 0x16ADE
m68k_016ade:
        andi.w #0x3,%d2
m68k_016ade_end:
.org 0x16AE2
m68k_016ae2:
        cmpi.b #0x3,%d2
m68k_016ae2_end:
.org 0x16AE6
m68k_016ae6:
        bne.b (. + 6)
m68k_016ae6_end:
.org 0x16AE8
m68k_016ae8:
        move.w #0xa,%d1
m68k_016ae8_end:
.org 0x16AEC
m68k_016aec:
        move.w %d1,0xcea2:w
m68k_016aec_end:
.org 0x16AF0
m68k_016af0:
        clr.w %d1
m68k_016af0_end:
.org 0x16AF2
m68k_016af2:
        move.b 0x1(%a0, %d0.w),%d1
m68k_016af2_end:
.org 0x16AF6
m68k_016af6:
        lsl.w #0x4,%d1
m68k_016af6_end:
.org 0x16AF8
m68k_016af8:
        move.w %d1,0xf63c:w
m68k_016af8_end:
.org 0x16AFC
m68k_016afc:
        clr.w %d1
m68k_016afc_end:
.org 0x16AFE
m68k_016afe:
        move.b 0x2(%a0, %d0.w),%d1
m68k_016afe_end:
.org 0x16B02
m68k_016b02:
        lsl.w #0x4,%d1
m68k_016b02_end:
.org 0x16B04
m68k_016b04:
        move.w %d1,0xf63e:w
m68k_016b04_end:
.org 0x16B08
m68k_016b08:
        clr.w %d1
m68k_016b08_end:
.org 0x16B0A
m68k_016b0a:
        move.b 0x3(%a0, %d0.w),%d1
m68k_016b0a_end:
.org 0x16B0E
m68k_016b0e:
        lsl.w #0x2,%d1
m68k_016b0e_end:
.org 0x16B10
m68k_016b10:
        lea.l 0xd4ac6:l,%a0
m68k_016b10_end:
.org 0x16B16
m68k_016b16:
        move.w 0x2(%a0, %d1.w),0xf640:w
m68k_016b16_end:
.org 0x16B1C
m68k_016b1c:
        move.w (%a0, %d1.w),0xf642:w
m68k_016b1c_end:
.org 0x16B22
m68k_016b22:
        jsr 0x6518:l
m68k_016b22_end:
.org 0x16B28
m68k_016b28:
        move.w #0x20a,0xf612:w
m68k_016b28_end:
.org 0x16B2E
m68k_016b2e:
        move.w #0x1,0xf362:w
m68k_016b2e_end:
.org 0x16B34
m68k_016b34:
        clr.w 0xceac:w
m68k_016b34_end:
.org 0x16B38
m68k_016b38:
        rts
m68k_016b38_end:
.org 0x16C72
m68k_016c72:
        lea.l 0xe1e0:w,%a1
m68k_016c72_end:
.org 0x16C76
m68k_016c76:
        lea.l 0xe3c0:w,%a2
m68k_016c76_end:
.org 0x16C7A
m68k_016c7a:
        lea.l 0xe140:w,%a5
m68k_016c7a_end:
.org 0x16C7E
m68k_016c7e:
        mulu.w 0x2(%a2, %d1.w),%d7
m68k_016c7e_end:
.org 0x16C82
m68k_016c82:
        mulu.w 0x2(%a1, %d1.w),%d7
m68k_016c82_end:
.org 0x16C86
m68k_016c86:
        divu.w #0x3a98,%d7
m68k_016c86_end:
.org 0x16C8A
m68k_016c8a:
        move.l (%a5, %d1.w),%d3
m68k_016c8a_end:
.org 0x16C8E
m68k_016c8e:
        andi.l #0xffff,%d3
m68k_016c8e_end:
.org 0x16C94
m68k_016c94:
        mulu.w %d7,%d3
m68k_016c94_end:
.org 0x16C96
m68k_016c96:
        rts
m68k_016c96_end:
.org 0x188A6
m68k_0188a6:
        lea.l 0xc500:w,%a0
m68k_0188a6_end:
.org 0x188AA
m68k_0188aa:
        lea.l 0xb200:w,%a1
m68k_0188aa_end:
.org 0x188AE
m68k_0188ae:
        lea.l 0xc800:w,%a2
m68k_0188ae_end:
.org 0x188B2
m68k_0188b2:
        lea.l 0xc000:w,%a3
m68k_0188b2_end:
.org 0x188B6
m68k_0188b6:
        lea.l 0xbe00:w,%a4
m68k_0188b6_end:
.org 0x188BA
m68k_0188ba:
        move.w 0xffff80e0:l,%d0
m68k_0188ba_end:
.org 0x188C0
m68k_0188c0:
        move.b 0xffff8101:l,%d2
m68k_0188c0_end:
.org 0x188C6
m68k_0188c6:
        cmpi.w #0x4,0xffff8114:l
m68k_0188c6_end:
.org 0x188CE
m68k_0188ce:
        bne.w (. + 38)
m68k_0188ce_end:
.org 0x188D2
m68k_0188d2:
        move.w %d0,-(%a7)
m68k_0188d2_end:
.org 0x188D4
m68k_0188d4:
        jsr 0x83d4:l
m68k_0188d4_end:
.org 0x188DA
m68k_0188da:
        andi.l #0xffff,%d0
m68k_0188da_end:
.org 0x188E0
m68k_0188e0:
        move.l %d0,%d1
m68k_0188e0_end:
.org 0x188E2
m68k_0188e2:
        lsl.l #0x1,%d0
m68k_0188e2_end:
.org 0x188E4
m68k_0188e4:
        add.w %d1,%d0
m68k_0188e4_end:
.org 0x188E6
m68k_0188e6:
        swap %d0
m68k_0188e6_end:
.org 0x188E8
m68k_0188e8:
        addq.w #0x1,%d0
m68k_0188e8_end:
.org 0x188EA
m68k_0188ea:
        sub.w %d0,%d2
m68k_0188ea_end:
.org 0x188EC
m68k_0188ec:
        bcc.w (. + 6)
m68k_0188ec_end:
.org 0x188F0
m68k_0188f0:
        clr.w %d2
m68k_0188f0_end:
.org 0x188F2
m68k_0188f2:
        move.w (%a7)+,%d0
m68k_0188f2_end:
.org 0x188F4
m68k_0188f4:
        move.b %d2,(%a0, %d0.w)
m68k_0188f4_end:
.org 0x188F8
m68k_0188f8:
        lsl.w #0x1,%d0
m68k_0188f8_end:
.org 0x188FA
m68k_0188fa:
        move.w 0xffff810c:l,(%a1, %d0.w)
m68k_0188fa_end:
.org 0x18902
m68k_018902:
        bne.w (. + 24)
m68k_018902_end:
.org 0x18906
m68k_018906:
        move.w 0xffff80e2:l,%d1
m68k_018906_end:
.org 0x1890C
m68k_01890c:
        bsr.w (. + 200)
m68k_01890c_end:
.org 0x18910
m68k_018910:
        move.w 0xffff80e0:l,%d1
m68k_018910_end:
.org 0x18916
m68k_018916:
        bsr.w (. + 318)
m68k_018916_end:
.org 0x1891A
m68k_01891a:
        move.w 0xffff80e2:l,%d0
m68k_01891a_end:
.org 0x18920
m68k_018920:
        move.b 0xffff8103:l,%d2
m68k_018920_end:
.org 0x18926
m68k_018926:
        cmpi.w #0x5,0xffff8114:l
m68k_018926_end:
.org 0x1892E
m68k_01892e:
        bne.w (. + 38)
m68k_01892e_end:
.org 0x18932
m68k_018932:
        move.w %d0,-(%a7)
m68k_018932_end:
.org 0x18934
m68k_018934:
        jsr 0x83d4:l
m68k_018934_end:
.org 0x1893A
m68k_01893a:
        andi.l #0xffff,%d0
m68k_01893a_end:
.org 0x18940
m68k_018940:
        move.l %d0,%d1
m68k_018940_end:
.org 0x18942
m68k_018942:
        lsl.l #0x1,%d0
m68k_018942_end:
.org 0x18944
m68k_018944:
        add.w %d1,%d0
m68k_018944_end:
.org 0x18946
m68k_018946:
        swap %d0
m68k_018946_end:
.org 0x18948
m68k_018948:
        addq.w #0x1,%d0
m68k_018948_end:
.org 0x1894A
m68k_01894a:
        sub.w %d0,%d2
m68k_01894a_end:
.org 0x1894C
m68k_01894c:
        bcc.w (. + 6)
m68k_01894c_end:
.org 0x18950
m68k_018950:
        clr.w %d2
m68k_018950_end:
.org 0x18952
m68k_018952:
        move.w (%a7)+,%d0
m68k_018952_end:
.org 0x18954
m68k_018954:
        move.b %d2,(%a0, %d0.w)
m68k_018954_end:
.org 0x18958
m68k_018958:
        lsl.w #0x1,%d0
m68k_018958_end:
.org 0x1895A
m68k_01895a:
        move.w 0xffff810e:l,(%a1, %d0.w)
m68k_01895a_end:
.org 0x18962
m68k_018962:
        bne.w (. + 24)
m68k_018962_end:
.org 0x18966
m68k_018966:
        move.w 0xffff80e0:l,%d1
m68k_018966_end:
.org 0x1896C
m68k_01896c:
        bsr.w (. + 104)
m68k_01896c_end:
.org 0x18970
m68k_018970:
        move.w 0xffff80e2:l,%d1
m68k_018970_end:
.org 0x18976
m68k_018976:
        bsr.w (. + 222)
m68k_018976_end:
.org 0x1897A
m68k_01897a:
        move.w 0xffff80e0:l,%d6
m68k_01897a_end:
.org 0x18980
m68k_018980:
        move.w 0xffff80e2:l,%d7
m68k_018980_end:
.org 0x18986
m68k_018986:
        move.w %d6,%d0
m68k_018986_end:
.org 0x18988
m68k_018988:
        lsl.w #0x2,%d0
m68k_018988_end:
.org 0x1898A
m68k_01898a:
        move.w 0x2(%a2, %d0.w),%d2
m68k_01898a_end:
.org 0x1898E
m68k_01898e:
        sub.w 0xffff8118:l,%d2
m68k_01898e_end:
.org 0x18994
m68k_018994:
        bcc.w (. + 6)
m68k_018994_end:
.org 0x18998
m68k_018998:
        clr.w %d2
m68k_018998_end:
.org 0x1899A
m68k_01899a:
        move.w %d7,%d0
m68k_01899a_end:
.org 0x1899C
m68k_01899c:
        bsr.w (. + 146)
m68k_01899c_end:
.org 0x189A0
m68k_0189a0:
        move.w %d7,%d0
m68k_0189a0_end:
.org 0x189A2
m68k_0189a2:
        lsl.w #0x2,%d0
m68k_0189a2_end:
.org 0x189A4
m68k_0189a4:
        move.w 0x2(%a2, %d0.w),%d2
m68k_0189a4_end:
.org 0x189A8
m68k_0189a8:
        sub.w 0xffff811a:l,%d2
m68k_0189a8_end:
.org 0x189AE
m68k_0189ae:
        bcc.w (. + 6)
m68k_0189ae_end:
.org 0x189B2
m68k_0189b2:
        clr.w %d2
m68k_0189b2_end:
.org 0x189B4
m68k_0189b4:
        move.w %d6,%d0
m68k_0189b4_end:
.org 0x189B6
m68k_0189b6:
        bsr.w (. + 120)
m68k_0189b6_end:
.org 0x189BA
m68k_0189ba:
        lsl.w #0x2,%d6
m68k_0189ba_end:
.org 0x189BC
m68k_0189bc:
        lsl.w #0x2,%d7
m68k_0189bc_end:
.org 0x189BE
m68k_0189be:
        move.w 0xffff8118:l,0x2(%a2, %d6.w)
m68k_0189be_end:
.org 0x189C6
m68k_0189c6:
        move.w 0xffff811a:l,0x2(%a2, %d7.w)
m68k_0189c6_end:
.org 0x189CE
m68k_0189ce:
        bsr.w (. + 198)
m68k_0189ce_end:
.org 0x189D2
m68k_0189d2:
        rts
m68k_0189d2_end:
.org 0x18B00
m68k_018b00:
        lea.l 0xff7050:l,%a0
m68k_018b00_end:
.org 0x18B06
m68k_018b06:
        lea.l 0xff70a0:l,%a1
m68k_018b06_end:
.org 0x18B0C
m68k_018b0c:
        lea.l 0xff70f0:l,%a2
m68k_018b0c_end:
.org 0x18B12
m68k_018b12:
        lea.l 0xff70f1:l,%a3
m68k_018b12_end:
.org 0x18B18
m68k_018b18:
        move.w 0xff706a:l,%d0
m68k_018b18_end:
.org 0x18B1E
m68k_018b1e:
        cmp.w 0xffff80e0:l,%d0
m68k_018b1e_end:
.org 0x18B24
m68k_018b24:
        beq.w (. + 8)
m68k_018b24_end:
.org 0x18B28
m68k_018b28:
        exg %a0,%a1
m68k_018b28_end:
.org 0x18B2A
m68k_018b2a:
        exg %a2,%a3
m68k_018b2a_end:
.org 0x18B2C
m68k_018b2c:
        move.w 0x1c(%a0),0xffff810c:l
m68k_018b2c_end:
.org 0x18B34
m68k_018b34:
        move.w 0x1c(%a1),0xffff810e:l
m68k_018b34_end:
.org 0x18B3C
m68k_018b3c:
        move.w 0xff706a:l,%d0
m68k_018b3c_end:
.org 0x18B42
m68k_018b42:
        move.w 0xff70ba:l,%d1
m68k_018b42_end:
.org 0x18B48
m68k_018b48:
        move.b 0xff70f0:l,%d2
m68k_018b48_end:
.org 0x18B4E
m68k_018b4e:
        beq.w (. + 8)
m68k_018b4e_end:
.org 0x18B52
m68k_018b52:
        bsr.w (. + 66)
m68k_018b52_end:
.org 0x18B56
m68k_018b56:
        exg %d0,%d1
m68k_018b56_end:
.org 0x18B58
m68k_018b58:
        move.b 0xff70f1:l,%d2
m68k_018b58_end:
.org 0x18B5E
m68k_018b5e:
        beq.w (. + 8)
m68k_018b5e_end:
.org 0x18B62
m68k_018b62:
        bsr.w (. + 50)
m68k_018b62_end:
.org 0x18B66
m68k_018b66:
        cmpi.b #0x1,0xff70f0:l
m68k_018b66_end:
.org 0x18B6E
m68k_018b6e:
        beq.w (. + 32)
m68k_018b6e_end:
.org 0x18B72
m68k_018b72:
        cmpi.b #0x1,0xff70f1:l
m68k_018b72_end:
.org 0x18B7A
m68k_018b7a:
        beq.w (. + 20)
m68k_018b7a_end:
.org 0x18B7E
m68k_018b7e:
        bsr.w (. + 216)
m68k_018b7e_end:
.org 0x18B82
m68k_018b82:
        jsr -734(%pc)
m68k_018b82_end:
.org 0x18B86
m68k_018b86:
        andi.w #0xfffe,%sr
m68k_018b86_end:
.org 0x18B8A
m68k_018b8a:
        bra.w (. + 8)
m68k_018b8a_end:
.org 0x18B8E
m68k_018b8e:
        ori.w #0x1,%sr
m68k_018b8e_end:
.org 0x18B92
m68k_018b92:
        rts
m68k_018b92_end:
.org 0x18CB4
m68k_018cb4:
        jsr 0x4890:l
m68k_018cb4_end:
.org 0x18CBA
m68k_018cba:
        jsr 0x4998:l
m68k_018cba_end:
.org 0x18CC0
m68k_018cc0:
        move.w 0xf606:w,%d0
m68k_018cc0_end:
.org 0x18CC4
m68k_018cc4:
        ori.b #0x40,%d0
m68k_018cc4_end:
.org 0x18CC8
m68k_018cc8:
        move.w %d0,0xc00004:l
m68k_018cc8_end:
.org 0x18CCE
m68k_018cce:
        bsr.w (. + 5280)
m68k_018cce_end:
.org 0x18CD2
m68k_018cd2:
        move.w 0xf612:w,%d0
m68k_018cd2_end:
.org 0x18CD6
m68k_018cd6:
        andi.w #0xff,%d0
m68k_018cd6_end:
.org 0x18CDA
m68k_018cda:
        lsl.w #0x1,%d0
m68k_018cda_end:
.org 0x18CDC
m68k_018cdc:
        move.w 44(%pc, %d0.w),%d0
m68k_018cdc_end:
.org 0x18CE0
m68k_018ce0:
        jsr 82(%pc, %d0.w)
m68k_018ce0_end:
.org 0x18CE4
m68k_018ce4:
        jsr 0x1b0c2:l
m68k_018ce4_end:
.org 0x18CEA
m68k_018cea:
        cmpi.w #0x1,0xf6c4:w
m68k_018cea_end:
.org 0x18CF0
m68k_018cf0:
        bne.w (. + 24)
m68k_018cf0_end:
.org 0x18CF4
m68k_018cf4:
        cmpi.w #0x400,0xf612:w
m68k_018cf4_end:
.org 0x18CFA
m68k_018cfa:
        beq.b (. + 8)
m68k_018cfa_end:
.org 0x18CFC
m68k_018cfc:
        jsr 0x1a2b8:l
m68k_018cfc_end:
.org 0x18D02
m68k_018d02:
        jsr 0x1a200:l
m68k_018d02_end:
.org 0x18D08
m68k_018d08:
        rts
m68k_018d08_end:
.org 0x18EB0
m68k_018eb0:
        bsr.w (. + 104)
m68k_018eb0_end:
.org 0x18EB4
m68k_018eb4:
        bsr.w (. + 178)
m68k_018eb4_end:
.org 0x18EB8
m68k_018eb8:
        bsr.w (. + 324)
m68k_018eb8_end:
.org 0x18EBC
m68k_018ebc:
        bsr.w (. + 348)
m68k_018ebc_end:
.org 0x18EC0
m68k_018ec0:
        move.w #0xffff,0xa5f8:w
m68k_018ec0_end:
.org 0x18EC6
m68k_018ec6:
        addq.w #0x1,0xf612:w
m68k_018ec6_end:
.org 0x18ECA
m68k_018eca:
        clr.w 0xf362:w
m68k_018eca_end:
.org 0x18ECE
m68k_018ece:
        move.w #0x402,0xf38a:w
m68k_018ece_end:
.org 0x18ED4
m68k_018ed4:
        lea.l 0xab8c4:l,%a0
m68k_018ed4_end:
.org 0x18EDA
m68k_018eda:
        move.l %a0,0xf6c0:w
m68k_018eda_end:
.org 0x18EDE
m68k_018ede:
        move.w #0x2,0xf6d6:w
m68k_018ede_end:
.org 0x18EE4
m68k_018ee4:
        clr.w 0xf36a:w
m68k_018ee4_end:
.org 0x18EE8
m68k_018ee8:
        move.w 0xf68e:w,%d0
m68k_018ee8_end:
.org 0x18EEC
m68k_018eec:
        cmp.w 0xf67a:w,%d0
m68k_018eec_end:
.org 0x18EF0
m68k_018ef0:
        beq.w (. + 26)
m68k_018ef0_end:
.org 0x18EF4
m68k_018ef4:
        cmp.w 0xf67c:w,%d0
m68k_018ef4_end:
.org 0x18EF8
m68k_018ef8:
        beq.w (. + 18)
m68k_018ef8_end:
.org 0x18EFC
m68k_018efc:
        cmp.w 0xf67e:w,%d0
m68k_018efc_end:
.org 0x18F00
m68k_018f00:
        beq.w (. + 10)
m68k_018f00_end:
.org 0x18F04
m68k_018f04:
        move.w #0xb8,0xf600:w
m68k_018f04_end:
.org 0x18F0A
m68k_018f0a:
        jsr 0x1a2b8:l
m68k_018f0a_end:
.org 0x18F10
m68k_018f10:
        jsr 0xa3da:l
m68k_018f10_end:
.org 0x18F16
m68k_018f16:
        rts
m68k_018f16_end:
.org 0x18F18
m68k_018f18:
        lea.l 0xcd00:w,%a0
m68k_018f18_end:
.org 0x18F1C
m68k_018f1c:
        lea.l 0xa5a4:w,%a1
m68k_018f1c_end:
.org 0x18F20
m68k_018f20:
        lea.l 0xf427:w,%a2
m68k_018f20_end:
.org 0x18F24
m68k_018f24:
        move.w 0xf68a:w,%d0
m68k_018f24_end:
.org 0x18F28
m68k_018f28:
        clr.w %d4
m68k_018f28_end:
.org 0x18F2A
m68k_018f2a:
        move.b (%a2, %d0.w),%d4
m68k_018f2a_end:
.org 0x18F2E
m68k_018f2e:
        move.w %d4,0xf68e:w
m68k_018f2e_end:
.org 0x18F32
m68k_018f32:
        lea.l 0xf45e:w,%a2
m68k_018f32_end:
.org 0x18F36
m68k_018f36:
        lsl.w #0x1,%d0
m68k_018f36_end:
.org 0x18F38
m68k_018f38:
        move.w (%a2, %d0.w),%d4
m68k_018f38_end:
.org 0x18F3C
m68k_018f3c:
        move.w %d4,(%a1)+
m68k_018f3c_end:
.org 0x18F3E
m68k_018f3e:
        lsr.w #0x1,%d0
m68k_018f3e_end:
.org 0x18F40
m68k_018f40:
        move.w #0xff,%d1
m68k_018f40_end:
.org 0x18F44
m68k_018f44:
        clr.w %d3
m68k_018f44_end:
.org 0x18F46
m68k_018f46:
        move.b -(%a0),%d2
m68k_018f46_end:
.org 0x18F48
m68k_018f48:
        cmp.b %d0,%d2
m68k_018f48_end:
.org 0x18F4A
m68k_018f4a:
        bne.w (. + 14)
m68k_018f4a_end:
.org 0x18F4E
m68k_018f4e:
        cmp.w %d4,%d1
m68k_018f4e_end:
.org 0x18F50
m68k_018f50:
        beq.w (. + 8)
m68k_018f50_end:
.org 0x18F54
m68k_018f54:
        move.w %d1,(%a1)+
m68k_018f54_end:
.org 0x18F56
m68k_018f56:
        addq.w #0x1,%d3
m68k_018f56_end:
.org 0x18F58
m68k_018f58:
        dbra %d1,(. + -18)
m68k_018f58_end:
.org 0x18F5C
m68k_018f5c:
        move.w #0xffff,(%a1)
m68k_018f5c_end:
.org 0x18F60
m68k_018f60:
        move.w %d3,0xf6a8:w
m68k_018f60_end:
.org 0x18F64
m68k_018f64:
        rts
m68k_018f64_end:
.org 0x18F66
m68k_018f66:
        lea.l 0xa150:w,%a0
m68k_018f66_end:
.org 0x18F6A
m68k_018f6a:
        lea.l 0xa550:w,%a1
m68k_018f6a_end:
.org 0x18F6E
m68k_018f6e:
        move.w 0xf68a:w,%d0
m68k_018f6e_end:
.org 0x18F72
m68k_018f72:
        move.w #0xff,%d2
m68k_018f72_end:
.org 0x18F76
m68k_018f76:
        move.b -(%a0),%d3
m68k_018f76_end:
.org 0x18F78
m68k_018f78:
        cmp.b %d0,%d3
m68k_018f78_end:
.org 0x18F7A
m68k_018f7a:
        beq.w (. + 8)
m68k_018f7a_end:
.org 0x18F7E
m68k_018f7e:
        dbra %d2,(. + -8)
m68k_018f7e_end:
.org 0x18F82
m68k_018f82:
        lea.l 0xcc00:w,%a2
m68k_018f82_end:
.org 0x18F86
m68k_018f86:
        clr.w %d1
m68k_018f86_end:
.org 0x18F88
m68k_018f88:
        move.b (%a2, %d2.w),%d1
m68k_018f88_end:
.org 0x18F8C
m68k_018f8c:
        andi.w #0x3f,%d1
m68k_018f8c_end:
.org 0x18F90
m68k_018f90:
        cmpi.w #0x28,%d1
m68k_018f90_end:
.org 0x18F94
m68k_018f94:
        bls.w (. + 14)
m68k_018f94_end:
.org 0x18F98
m68k_018f98:
        subi.w #0x29,%d1
m68k_018f98_end:
.org 0x18F9C
m68k_018f9c:
        move.w %d1,%d4
m68k_018f9c_end:
.org 0x18F9E
m68k_018f9e:
        bra.w (. + 14)
m68k_018f9e_end:
.org 0x18FA2
m68k_018fa2:
        lea.l 0xf427:w,%a2
m68k_018fa2_end:
.org 0x18FA6
m68k_018fa6:
        clr.w %d4
m68k_018fa6_end:
.org 0x18FA8
m68k_018fa8:
        move.b (%a2, %d1.w),%d4
m68k_018fa8_end:
.org 0x18FAC
m68k_018fac:
        move.w %d4,0xf68c:w
m68k_018fac_end:
.org 0x18FB0
m68k_018fb0:
        lsl.w #0x1,%d4
m68k_018fb0_end:
.org 0x18FB2
m68k_018fb2:
        lea.l 0xe640:w,%a2
m68k_018fb2_end:
.org 0x18FB6
m68k_018fb6:
        move.w (%a2, %d4.w),%d4
m68k_018fb6_end:
.org 0x18FBA
m68k_018fba:
        clr.w %d1
m68k_018fba_end:
.org 0x18FBC
m68k_018fbc:
        lea.l 0xa050:w,%a2
m68k_018fbc_end:
.org 0x18FC0
m68k_018fc0:
        cmp.b (%a2, %d4.w),%d0
m68k_018fc0_end:
.org 0x18FC4
m68k_018fc4:
        bne.w (. + 8)
m68k_018fc4_end:
.org 0x18FC8
m68k_018fc8:
        move.w %d4,(%a1)+
m68k_018fc8_end:
.org 0x18FCA
m68k_018fca:
        addq.w #0x1,%d1
m68k_018fca_end:
.org 0x18FCC
m68k_018fcc:
        cmp.w %d4,%d2
m68k_018fcc_end:
.org 0x18FCE
m68k_018fce:
        beq.w (. + 8)
m68k_018fce_end:
.org 0x18FD2
m68k_018fd2:
        move.w %d2,(%a1)+
m68k_018fd2_end:
.org 0x18FD4
m68k_018fd4:
        addq.w #0x1,%d1
m68k_018fd4_end:
.org 0x18FD6
m68k_018fd6:
        subq.w #0x1,%d2
m68k_018fd6_end:
.org 0x18FD8
m68k_018fd8:
        bcs.w (. + 26)
m68k_018fd8_end:
.org 0x18FDC
m68k_018fdc:
        move.b -(%a0),%d3
m68k_018fdc_end:
.org 0x18FDE
m68k_018fde:
        cmp.b %d0,%d3
m68k_018fde_end:
.org 0x18FE0
m68k_018fe0:
        bne.w (. + 14)
m68k_018fe0_end:
.org 0x18FE4
m68k_018fe4:
        cmp.w %d4,%d2
m68k_018fe4_end:
.org 0x18FE6
m68k_018fe6:
        beq.w (. + 8)
m68k_018fe6_end:
.org 0x18FEA
m68k_018fea:
        move.w %d2,(%a1)+
m68k_018fea_end:
.org 0x18FEC
m68k_018fec:
        addq.w #0x1,%d1
m68k_018fec_end:
.org 0x18FEE
m68k_018fee:
        dbra %d2,(. + -18)
m68k_018fee_end:
.org 0x18FF2
m68k_018ff2:
        move.w #0xffff,(%a1)
m68k_018ff2_end:
.org 0x18FF6
m68k_018ff6:
        move.w %d1,0xf6a6:w
m68k_018ff6_end:
.org 0x18FFA
m68k_018ffa:
        rts
m68k_018ffa_end:
.org 0x18FFC
m68k_018ffc:
        lea.l 0xdffc:w,%a0
m68k_018ffc_end:
.org 0x19000
m68k_019000:
        move.w 0xf68a:w,%d0
m68k_019000_end:
.org 0x19004
m68k_019004:
        lsl.w #0x2,%d0
m68k_019004_end:
.org 0x19006
m68k_019006:
        move.l (%a0, %d0.w),0xf69a:w
m68k_019006_end:
.org 0x1900C
m68k_01900c:
        lea.l 0xe09c:w,%a0
m68k_01900c_end:
.org 0x19010
m68k_019010:
        move.l (%a0, %d0.w),0xf6a2:w
m68k_019010_end:
.org 0x19016
m68k_019016:
        rts
m68k_019016_end:
.org 0x19018
m68k_019018:
        lea.l 0xed84:w,%a0
m68k_019018_end:
.org 0x1901C
m68k_01901c:
        move.w 0xf68a:w,%d0
m68k_01901c_end:
.org 0x19020
m68k_019020:
        lsl.w #0x2,%d0
m68k_019020_end:
.org 0x19022
m68k_019022:
        move.l (%a0, %d0.w),0xf696:w
m68k_019022_end:
.org 0x19028
m68k_019028:
        lea.l 0xee24:w,%a0
m68k_019028_end:
.org 0x1902C
m68k_01902c:
        move.l (%a0, %d0.w),0xf69e:w
m68k_01902c_end:
.org 0x19032
m68k_019032:
        rts
m68k_019032_end:
.org 0x19034
m68k_019034:
        btst.b #0x5,0xf603:w
m68k_019034_end:
.org 0x1903A
m68k_01903a:
        beq.w (. + 66)
m68k_01903a_end:
.org 0x1903E
m68k_01903e:
        addq.w #0x1,0xf362:w
m68k_01903e_end:
.org 0x19042
m68k_019042:
        bchg.b #0x1,0xf6d7:w
m68k_019042_end:
.org 0x19048
m68k_019048:
        move.w #0xc1,%d0
m68k_019048_end:
.org 0x1904C
m68k_01904c:
        jsr 0x676f2:l
m68k_01904c_end:
.org 0x19052
m68k_019052:
        move.w 0xf67c:w,%d0
m68k_019052_end:
.org 0x19056
m68k_019056:
        lsl.w #0x1,%d0
m68k_019056_end:
.org 0x19058
m68k_019058:
        lea.l 0xe640:w,%a0
m68k_019058_end:
.org 0x1905C
m68k_01905c:
        move.w (%a0, %d0.w),0xf3d0:w
m68k_01905c_end:
.org 0x19062
m68k_019062:
        btst.b #0x1,0xf6d7:w
m68k_019062_end:
.org 0x19068
m68k_019068:
        bne.w (. + 14)
m68k_019068_end:
.org 0x1906C
m68k_01906c:
        move.w 0xf67c:w,0xf68c:w
m68k_01906c_end:
.org 0x19072
m68k_019072:
        bra.w (. + 10)
m68k_019072_end:
.org 0x19674
m68k_019674:
        jsr 0x1ef7a:l
m68k_019674_end:
.org 0x1967A
m68k_01967a:
        jsr 0xa3da:l
m68k_01967a_end:
.org 0x19680
m68k_019680:
        rts
m68k_019680_end:
.org 0x19F0C
m68k_019f0c:
        jsr 0x1e22e:l
m68k_019f0c_end:
.org 0x19F12
m68k_019f12:
        jsr 0xa3da:l
m68k_019f12_end:
.org 0x19F18
m68k_019f18:
        rts
m68k_019f18_end:
.org 0x1D57A
m68k_01d57a:
        lea.l 0xe640:w,%a0
m68k_01d57a_end:
.org 0x1D57E
m68k_01d57e:
        lea.l 0xc300:w,%a1
m68k_01d57e_end:
.org 0x1D582
m68k_01d582:
        move.w #0xf,%d0
m68k_01d582_end:
.org 0x1D586
m68k_01d586:
        move.w (%a0)+,%d1
m68k_01d586_end:
.org 0x1D588
m68k_01d588:
        bmi.w (. + 10)
m68k_01d588_end:
.org 0x1D58C
m68k_01d58c:
        move.b #0x64,(%a1, %d1.w)
m68k_01d58c_end:
.org 0x1D592
m68k_01d592:
        dbra %d0,(. + -12)
m68k_01d592_end:
.org 0x1D596
m68k_01d596:
        rts
m68k_01d596_end:
.org 0x1DCAA
m68k_01dcaa:
        move.w %d7,%d1
m68k_01dcaa_end:
.org 0x1DCAC
m68k_01dcac:
        lsl.w #0x2,%d1
m68k_01dcac_end:
.org 0x1DCAE
m68k_01dcae:
        lea.l 0xa150:w,%a1
m68k_01dcae_end:
.org 0x1DCB2
m68k_01dcb2:
        move.w (%a1, %d1.w),%d5
m68k_01dcb2_end:
.org 0x1DCB6
m68k_01dcb6:
        move.w 0x2(%a1, %d1.w),%d6
m68k_01dcb6_end:
.org 0x1DCBA
m68k_01dcba:
        clr.w %d2
m68k_01dcba_end:
.org 0x1DCBC
m68k_01dcbc:
        lea.l 0xff2c00:l,%a0
m68k_01dcbc_end:
.org 0x1DCC2
m68k_01dcc2:
        move.w (%a0, %d1.w),%d3
m68k_01dcc2_end:
.org 0x1DCC6
m68k_01dcc6:
        lsl.w #0x7,%d3
m68k_01dcc6_end:
.org 0x1DCC8
m68k_01dcc8:
        sub.w %d5,%d3
m68k_01dcc8_end:
.org 0x1DCCA
m68k_01dcca:
        bcc.b (. + 8)
m68k_01dcca_end:
.org 0x1DCCC
m68k_01dccc:
        neg.w %d3
m68k_01dccc_end:
.org 0x1DCCE
m68k_01dcce:
        bset.l #0x0,%d2
m68k_01dcce_end:
.org 0x1DCD2
m68k_01dcd2:
        addi.w #0x40,%d3
m68k_01dcd2_end:
.org 0x1DCD6
m68k_01dcd6:
        lsr.w #0x7,%d3
m68k_01dcd6_end:
.org 0x1DCD8
m68k_01dcd8:
        move.w 0x2(%a0, %d1.w),%d4
m68k_01dcd8_end:
.org 0x1DCDC
m68k_01dcdc:
        lsl.w #0x7,%d4
m68k_01dcdc_end:
.org 0x1DCDE
m68k_01dcde:
        sub.w %d6,%d4
m68k_01dcde_end:
.org 0x1DCE0
m68k_01dce0:
        bcc.b (. + 8)
m68k_01dce0_end:
.org 0x1DCE2
m68k_01dce2:
        neg.w %d4
m68k_01dce2_end:
.org 0x1DCE4
m68k_01dce4:
        bset.l #0x1,%d2
m68k_01dce4_end:
.org 0x1DCE8
m68k_01dce8:
        addi.w #0x40,%d4
m68k_01dce8_end:
.org 0x1DCEC
m68k_01dcec:
        lsr.w #0x7,%d4
m68k_01dcec_end:
.org 0x1DCEE
m68k_01dcee:
        move.w %d3,%d0
m68k_01dcee_end:
.org 0x1DCF0
m68k_01dcf0:
        mulu.w %d0,%d0
m68k_01dcf0_end:
.org 0x1DCF2
m68k_01dcf2:
        move.w %d4,%d1
m68k_01dcf2_end:
.org 0x1DCF4
m68k_01dcf4:
        mulu.w %d1,%d1
m68k_01dcf4_end:
.org 0x1DCF6
m68k_01dcf6:
        add.l %d1,%d0
m68k_01dcf6_end:
.org 0x1DCF8
m68k_01dcf8:
        jsr 0x3080e:l
m68k_01dcf8_end:
.org 0x1DCFE
m68k_01dcfe:
        andi.l #0xffff,%d0
m68k_01dcfe_end:
.org 0x1DD04
m68k_01dd04:
        beq.w (. + 110)
m68k_01dd04_end:
.org 0x1DD08
m68k_01dd08:
        lsl.l #0x7,%d0
m68k_01dd08_end:
.org 0x1DD0A
m68k_01dd0a:
        lea.l 0xc400:w,%a0
m68k_01dd0a_end:
.org 0x1DD0E
m68k_01dd0e:
        clr.w %d1
m68k_01dd0e_end:
.org 0x1DD10
m68k_01dd10:
        move.b (%a0, %d7.w),%d1
m68k_01dd10_end:
.org 0x1DD14
m68k_01dd14:
        divu.w %d1,%d0
m68k_01dd14_end:
.org 0x1DD16
m68k_01dd16:
        andi.l #0xffff,%d3
m68k_01dd16_end:
.org 0x1DD1C
m68k_01dd1c:
        lsl.l #0x7,%d3
m68k_01dd1c_end:
.org 0x1DD1E
m68k_01dd1e:
        beq.w (. + 16)
m68k_01dd1e_end:
.org 0x1DD22
m68k_01dd22:
        divu.w %d0,%d3
m68k_01dd22_end:
.org 0x1DD24
m68k_01dd24:
        btst.l #0x0,%d2
m68k_01dd24_end:
.org 0x1DD28
m68k_01dd28:
        beq.w (. + 6)
m68k_01dd28_end:
.org 0x1DD2C
m68k_01dd2c:
        neg.w %d3
m68k_01dd2c_end:
.org 0x1DD2E
m68k_01dd2e:
        andi.l #0xffff,%d4
m68k_01dd2e_end:
.org 0x1DD34
m68k_01dd34:
        lsl.l #0x7,%d4
m68k_01dd34_end:
.org 0x1DD36
m68k_01dd36:
        beq.w (. + 16)
m68k_01dd36_end:
.org 0x1DD3A
m68k_01dd3a:
        divu.w %d0,%d4
m68k_01dd3a_end:
.org 0x1DD3C
m68k_01dd3c:
        btst.l #0x1,%d2
m68k_01dd3c_end:
.org 0x1DD40
m68k_01dd40:
        beq.w (. + 6)
m68k_01dd40_end:
.org 0x1DD44
m68k_01dd44:
        neg.w %d4
m68k_01dd44_end:
.org 0x1DD46
m68k_01dd46:
        lea.l 0xa960:w,%a0
m68k_01dd46_end:
.org 0x1DD4A
m68k_01dd4a:
        lsl.w #0x2,%d7
m68k_01dd4a_end:
.org 0x1DD4C
m68k_01dd4c:
        move.w 0xf70a:w,%d5
m68k_01dd4c_end:
.org 0x1DD50
m68k_01dd50:
        andi.w #0x3,%d5
m68k_01dd50_end:
.org 0x1DD54
m68k_01dd54:
        beq.w (. + 20)
m68k_01dd54_end:
.org 0x1DD58
m68k_01dd58:
        move.w %d3,%d6
m68k_01dd58_end:
.org 0x1DD5A
m68k_01dd5a:
        asl.w %d5,%d6
m68k_01dd5a_end:
.org 0x1DD5C
m68k_01dd5c:
        asr.w #0x3,%d6
m68k_01dd5c_end:
.org 0x1DD5E
m68k_01dd5e:
        add.w %d6,%d3
m68k_01dd5e_end:
.org 0x1DD60
m68k_01dd60:
        move.w %d4,%d6
m68k_01dd60_end:
.org 0x1DD62
m68k_01dd62:
        asl.w %d5,%d6
m68k_01dd62_end:
.org 0x1DD64
m68k_01dd64:
        asr.w #0x3,%d6
m68k_01dd64_end:
.org 0x1DD66
m68k_01dd66:
        add.w %d6,%d4
m68k_01dd66_end:
.org 0x1DD68
m68k_01dd68:
        move.w %d3,(%a0, %d7.w)
m68k_01dd68_end:
.org 0x1DD6C
m68k_01dd6c:
        move.w %d4,0x2(%a0, %d7.w)
m68k_01dd6c_end:
.org 0x1DD70
m68k_01dd70:
        rts
m68k_01dd70_end:
.org 0x1DD72
m68k_01dd72:
        clr.w %d3
m68k_01dd72_end:
.org 0x1DD74
m68k_01dd74:
        clr.w %d4
m68k_01dd74_end:
.org 0x1DD76
m68k_01dd76:
        lea.l 0xae28:w,%a5
m68k_01dd76_end:
.org 0x1DD7A
m68k_01dd7a:
        clr.b (%a5, %d7.w)
m68k_01dd7a_end:
.org 0x1DD7E
m68k_01dd7e:
        bra.b (. + -56)
m68k_01dd7e_end:
.org 0x1DD80
m68k_01dd80:
        move.w 0xf68a:w,%d0
m68k_01dd80_end:
.org 0x1DD84
m68k_01dd84:
        lsl.w #0x3,%d0
m68k_01dd84_end:
.org 0x1DD86
m68k_01dd86:
        lea.l 0xae1b2:l,%a6
m68k_01dd86_end:
.org 0x1DD8C
m68k_01dd8c:
        adda.w %d0,%a6
m68k_01dd8c_end:
.org 0x1DD8E
m68k_01dd8e:
        lea.l 0xa150:w,%a1
m68k_01dd8e_end:
.org 0x1DD92
m68k_01dd92:
        lea.l 0xa960:w,%a2
m68k_01dd92_end:
.org 0x1DD96
m68k_01dd96:
        lea.l 0xae28:w,%a3
m68k_01dd96_end:
.org 0x1DD9A
m68k_01dd9a:
        lea.l 0xff2c00:l,%a4
m68k_01dd9a_end:
.org 0x1DDA0
m68k_01dda0:
        bclr.l #0x1f,%d4
m68k_01dda0_end:
.org 0x1DDA4
m68k_01dda4:
        lea.l 0xa550:w,%a0
m68k_01dda4_end:
.org 0x1DDA8
m68k_01dda8:
        bsr.w (. + 22)
m68k_01dda8_end:
.org 0x1DDAC
m68k_01ddac:
        bset.l #0x1f,%d4
m68k_01ddac_end:
.org 0x1DDB0
m68k_01ddb0:
        lea.l 0xa5a4:w,%a0
m68k_01ddb0_end:
.org 0x1DDB4
m68k_01ddb4:
        bsr.w (. + 10)
m68k_01ddb4_end:
.org 0x1DDB8
m68k_01ddb8:
        bsr.w (. + 814)
m68k_01ddb8_end:
.org 0x1DDBC
m68k_01ddbc:
        rts
m68k_01ddbc_end:
.org 0x1DDBE
m68k_01ddbe:
        clr.w %d3
m68k_01ddbe_end:
.org 0x1DDC0
m68k_01ddc0:
        move.w (%a0)+,%d0
m68k_01ddc0_end:
.org 0x1DDC2
m68k_01ddc2:
        bmi.b (. + 114)
m68k_01ddc2_end:
.org 0x1DDC4
m68k_01ddc4:
        andi.w #0xff,%d0
m68k_01ddc4_end:
.org 0x1DDC8
m68k_01ddc8:
        cmpi.b #0x1,(%a3, %d0.w)
m68k_01ddc8_end:
.org 0x1DDCE
m68k_01ddce:
        bne.b (. + -14)
m68k_01ddce_end:
.org 0x1DDD0
m68k_01ddd0:
        lea.l 0xceae:w,%a5
m68k_01ddd0_end:
.org 0x1DDD4
m68k_01ddd4:
        tst.b (%a5, %d0.w)
m68k_01ddd4_end:
.org 0x1DDD8
m68k_01ddd8:
        beq.b (. + 4)
m68k_01ddd8_end:
.org 0x1DDDA
m68k_01ddda:
        bra.b (. + -26)
m68k_01ddda_end:
.org 0x1DDDC
m68k_01dddc:
        lsl.w #0x2,%d0
m68k_01dddc_end:
.org 0x1DDDE
m68k_01ddde:
        move.w (%a1, %d0.w),%d1
m68k_01ddde_end:
.org 0x1DDE2
m68k_01dde2:
        move.w 0x2(%a1, %d0.w),%d2
m68k_01dde2_end:
.org 0x1DDE6
m68k_01dde6:
        move.w (%a2, %d0.w),%d6
m68k_01dde6_end:
.org 0x1DDEA
m68k_01ddea:
        move.w 0x2(%a2, %d0.w),%d7
m68k_01ddea_end:
.org 0x1DDEE
m68k_01ddee:
        bsr.w (. + 608)
m68k_01ddee_end:
.org 0x1DDF2
m68k_01ddf2:
        cmpi.w #0x6,%d4
m68k_01ddf2_end:
.org 0x1DDF6
m68k_01ddf6:
        beq.w (. + 64)
m68k_01ddf6_end:
.org 0x1DDFA
m68k_01ddfa:
        add.w %d6,%d1
m68k_01ddfa_end:
.org 0x1DDFC
m68k_01ddfc:
        cmpi.w #0x400,%d1
m68k_01ddfc_end:
.org 0x1DE00
m68k_01de00:
        bcs.w (. + 48)
m68k_01de00_end:
.org 0x1DE04
m68k_01de04:
        cmpi.w #0x6c00,%d1
m68k_01de04_end:
.org 0x1DE08
m68k_01de08:
        bhi.w (. + 40)
m68k_01de08_end:
.org 0x1DE0C
m68k_01de0c:
        add.w %d7,%d2
m68k_01de0c_end:
.org 0x1DE0E
m68k_01de0e:
        cmpi.w #0x400,%d2
m68k_01de0e_end:
.org 0x1DE12
m68k_01de12:
        bcs.b (. + 30)
m68k_01de12_end:
.org 0x1DE14
m68k_01de14:
        cmpi.w #0x9c00,%d2
m68k_01de14_end:
.org 0x1DE18
m68k_01de18:
        bhi.w (. + 24)
m68k_01de18_end:
.org 0x1DE1C
m68k_01de1c:
        move.w %d1,(%a1, %d0.w)
m68k_01de1c_end:
.org 0x1DE20
m68k_01de20:
        move.w %d2,0x2(%a1, %d0.w)
m68k_01de20_end:
.org 0x1DE24
m68k_01de24:
        bsr.w (. + 252)
m68k_01de24_end:
.org 0x1DE28
m68k_01de28:
        bcs.w (. + 8)
m68k_01de28_end:
.org 0x1DE2C
m68k_01de2c:
        bsr.w (. + 176)
m68k_01de2c_end:
.org 0x1DE30
m68k_01de30:
        addq.w #0x1,%d3
m68k_01de30_end:
.org 0x1DE32
m68k_01de32:
        bra.b (. + -114)
m68k_01de32_end:
.org 0x1DE34
m68k_01de34:
        rts
m68k_01de34_end:
.org 0x1DE36
m68k_01de36:
        bsr.w (. + 118)
m68k_01de36_end:
.org 0x1DE3A
m68k_01de3a:
        tst.w %d6
m68k_01de3a_end:
.org 0x1DE3C
m68k_01de3c:
        bmi.b (. + 34)
m68k_01de3c_end:
.org 0x1DE3E
m68k_01de3e:
        tst.w %d7
m68k_01de3e_end:
.org 0x1DE40
m68k_01de40:
        bmi.b (. + 14)
m68k_01de40_end:
.org 0x1DE42
m68k_01de42:
        move.w #0x1,%d1
m68k_01de42_end:
.org 0x1DE46
m68k_01de46:
        cmp.w %d7,%d6
m68k_01de46_end:
.org 0x1DE48
m68k_01de48:
        bcs.b (. + 48)
m68k_01de48_end:
.org 0x1DE4A
m68k_01de4a:
        addq.w #0x1,%d1
m68k_01de4a_end:
.org 0x1DE4C
m68k_01de4c:
        bra.b (. + 44)
m68k_01de4c_end:
.org 0x1DE4E
m68k_01de4e:
        move.w #0x2,%d1
m68k_01de4e_end:
.org 0x1DE52
m68k_01de52:
        neg.w %d7
m68k_01de52_end:
.org 0x1DE54
m68k_01de54:
        cmp.w %d7,%d6
m68k_01de54_end:
.org 0x1DE56
m68k_01de56:
        bcc.b (. + 34)
m68k_01de56_end:
.org 0x1DE58
m68k_01de58:
        addq.w #0x1,%d1
m68k_01de58_end:
.org 0x1DE5A
m68k_01de5a:
        bra.w (. + 30)
m68k_01de5a_end:
.org 0x1DE5E
m68k_01de5e:
        tst.w %d7
m68k_01de5e_end:
.org 0x1DE60
m68k_01de60:
        bmi.b (. + 14)
m68k_01de60_end:
.org 0x1DE62
m68k_01de62:
        clr.w %d1
m68k_01de62_end:
.org 0x1DE64
m68k_01de64:
        neg.w %d6
m68k_01de64_end:
.org 0x1DE66
m68k_01de66:
        cmp.w %d7,%d6
m68k_01de66_end:
.org 0x1DE68
m68k_01de68:
        bcc.b (. + 16)
m68k_01de68_end:
.org 0x1DE6A
m68k_01de6a:
        addq.w #0x1,%d1
m68k_01de6a_end:
.org 0x1DE6C
m68k_01de6c:
        bra.b (. + 12)
m68k_01de6c_end:
.org 0x1DE6E
m68k_01de6e:
        clr.w %d1
m68k_01de6e_end:
.org 0x1DE70
m68k_01de70:
        cmp.w %d7,%d6
m68k_01de70_end:
.org 0x1DE72
m68k_01de72:
        bls.b (. + 6)
m68k_01de72_end:
.org 0x1DE74
m68k_01de74:
        move.w #0x3,%d1
m68k_01de74_end:
.org 0x1DE78
m68k_01de78:
        move.w 0xf68a:w,%d2
m68k_01de78_end:
.org 0x1DE7C
m68k_01de7c:
        lsl.w #0x3,%d2
m68k_01de7c_end:
.org 0x1DE7E
m68k_01de7e:
        lea.l 0xae1b2:l,%a5
m68k_01de7e_end:
.org 0x1DE84
m68k_01de84:
        move.w (%a5, %d2.w),%d5
m68k_01de84_end:
.org 0x1DE88
m68k_01de88:
        addi.w #0xf80,%d5
m68k_01de88_end:
.org 0x1DE8C
m68k_01de8c:
        move.w 0x4(%a5, %d2.w),%d6
m68k_01de8c_end:
.org 0x1DE90
m68k_01de90:
        addi.w #0xf80,%d6
m68k_01de90_end:
.org 0x1DE94
m68k_01de94:
        lsl.w #0x2,%d1
m68k_01de94_end:
.org 0x1DE96
m68k_01de96:
        lea.l -664(%pc),%a5
m68k_01de96_end:
.org 0x1DE9A
m68k_01de9a:
        add.w (%a5, %d1.w),%d5
m68k_01de9a_end:
.org 0x1DE9E
m68k_01de9e:
        move.w %d5,(%a1, %d0.w)
m68k_01de9e_end:
.org 0x1DEA2
m68k_01dea2:
        add.w 0x2(%a5, %d1.w),%d6
m68k_01dea2_end:
.org 0x1DEA6
m68k_01dea6:
        move.w %d6,0x2(%a1, %d0.w)
m68k_01dea6_end:
.org 0x1DEAA
m68k_01deaa:
        bra.b (. + -122)
m68k_01deaa_end:
.org 0x1DEAC
m68k_01deac:
        movem.l %d1/%a0-%a1,-(%a7)
m68k_01deac_end:
.org 0x1DEB0
m68k_01deb0:
        lea.l 0xff2c00:l,%a0
m68k_01deb0_end:
.org 0x1DEB6
m68k_01deb6:
        lea.l 0xae2f6:l,%a1
m68k_01deb6_end:
.org 0x1DEBC
m68k_01debc:
        move.w 0xf68a:w,%d1
m68k_01debc_end:
.org 0x1DEC0
m68k_01dec0:
        lsl.w #0x2,%d1
m68k_01dec0_end:
.org 0x1DEC2
m68k_01dec2:
        move.w (%a0, %d0.w),%d6
m68k_01dec2_end:
.org 0x1DEC6
m68k_01dec6:
        lsl.w #0x7,%d6
m68k_01dec6_end:
.org 0x1DEC8
m68k_01dec8:
        sub.w (%a1, %d1.w),%d6
m68k_01dec8_end:
.org 0x1DECC
m68k_01decc:
        move.w 0x2(%a0, %d0.w),%d7
m68k_01decc_end:
.org 0x1DED0
m68k_01ded0:
        lsl.w #0x7,%d7
m68k_01ded0_end:
.org 0x1DED2
m68k_01ded2:
        sub.w 0x2(%a1, %d1.w),%d7
m68k_01ded2_end:
.org 0x1DED6
m68k_01ded6:
        movem.l (%a7)+,%d1/%a0-%a1
m68k_01ded6_end:
.org 0x1DEDA
m68k_01deda:
        rts
m68k_01deda_end:
.org 0x1DEDC
m68k_01dedc:
        lsr.w #0x7,%d1
m68k_01dedc_end:
.org 0x1DEDE
m68k_01dede:
        sub.w (%a4, %d0.w),%d1
m68k_01dede_end:
.org 0x1DEE2
m68k_01dee2:
        addi.w #0x1,%d1
m68k_01dee2_end:
.org 0x1DEE6
m68k_01dee6:
        cmpi.w #0x2,%d1
m68k_01dee6_end:
.org 0x1DEEA
m68k_01deea:
        bhi.w (. + 52)
m68k_01deea_end:
.org 0x1DEEE
m68k_01deee:
        lsr.w #0x7,%d2
m68k_01deee_end:
.org 0x1DEF0
m68k_01def0:
        sub.w 0x2(%a4, %d0.w),%d2
m68k_01def0_end:
.org 0x1DEF4
m68k_01def4:
        addi.w #0x1,%d2
m68k_01def4_end:
.org 0x1DEF8
m68k_01def8:
        cmpi.w #0x2,%d2
m68k_01def8_end:
.org 0x1DEFC
m68k_01defc:
        bhi.b (. + 34)
m68k_01defc_end:
.org 0x1DEFE
m68k_01defe:
        move.w (%a4, %d0.w),%d1
m68k_01defe_end:
.org 0x1DF02
m68k_01df02:
        lsl.w #0x7,%d1
m68k_01df02_end:
.org 0x1DF04
m68k_01df04:
        move.w %d1,(%a1, %d0.w)
m68k_01df04_end:
.org 0x1DF08
m68k_01df08:
        move.w 0x2(%a4, %d0.w),%d2
m68k_01df08_end:
.org 0x1DF0C
m68k_01df0c:
        lsl.w #0x7,%d2
m68k_01df0c_end:
.org 0x1DF0E
m68k_01df0e:
        move.w %d2,0x2(%a1, %d0.w)
m68k_01df0e_end:
.org 0x1DF12
m68k_01df12:
        clr.l (%a2, %d0.w)
m68k_01df12_end:
.org 0x1DF16
m68k_01df16:
        lsr.w #0x2,%d0
m68k_01df16_end:
.org 0x1DF18
m68k_01df18:
        clr.b (%a3, %d0.w)
m68k_01df18_end:
.org 0x1DF1C
m68k_01df1c:
        lsl.w #0x2,%d0
m68k_01df1c_end:
.org 0x1DF1E
m68k_01df1e:
        rts
m68k_01df1e_end:
.org 0x1DF20
m68k_01df20:
        cmp.w (%a6),%d1
m68k_01df20_end:
.org 0x1DF22
m68k_01df22:
        bls.b (. + 56)
m68k_01df22_end:
.org 0x1DF24
m68k_01df24:
        cmp.w 0x2(%a6),%d1
m68k_01df24_end:
.org 0x1DF28
m68k_01df28:
        bcc.w (. + 50)
m68k_01df28_end:
.org 0x1DF2C
m68k_01df2c:
        cmp.w 0x4(%a6),%d2
m68k_01df2c_end:
.org 0x1DF30
m68k_01df30:
        bls.b (. + 42)
m68k_01df30_end:
.org 0x1DF32
m68k_01df32:
        cmp.w 0x6(%a6),%d2
m68k_01df32_end:
.org 0x1DF36
m68k_01df36:
        bcc.w (. + 36)
m68k_01df36_end:
.org 0x1DF3A
m68k_01df3a:
        bsr.w (. + 140)
m68k_01df3a_end:
.org 0x1DF3E
m68k_01df3e:
        tst.l %d4
m68k_01df3e_end:
.org 0x1DF40
m68k_01df40:
        bpl.b (. + 6)
m68k_01df40_end:
.org 0x1DF42
m68k_01df42:
        bsr.w (. + 30)
m68k_01df42_end:
.org 0x1DF46
m68k_01df46:
        clr.l (%a2, %d0.w)
m68k_01df46_end:
.org 0x1DF4A
m68k_01df4a:
        lsr.w #0x2,%d0
m68k_01df4a_end:
.org 0x1DF4C
m68k_01df4c:
        clr.b (%a3, %d0.w)
m68k_01df4c_end:
.org 0x1DF50
m68k_01df50:
        lsl.w #0x2,%d0
m68k_01df50_end:
.org 0x1DF52
m68k_01df52:
        ori.w #0x1,%sr
m68k_01df52_end:
.org 0x1DF56
m68k_01df56:
        bra.w (. + 8)
m68k_01df56_end:
.org 0x1DF5A
m68k_01df5a:
        andi.w #0xfffe,%sr
m68k_01df5a_end:
.org 0x1DF5E
m68k_01df5e:
        rts
m68k_01df5e_end:
.org 0x1DFC6
m68k_01dfc6:
        movem.l %d3-%d6,-(%a7)
m68k_01dfc6_end:
.org 0x1DFCA
m68k_01dfca:
        move.w %d1,%d3
m68k_01dfca_end:
.org 0x1DFCC
m68k_01dfcc:
        sub.w (%a6),%d3
m68k_01dfcc_end:
.org 0x1DFCE
m68k_01dfce:
        bcs.w (. + 42)
m68k_01dfce_end:
.org 0x1DFD2
m68k_01dfd2:
        cmpi.w #0x3100,%d3
m68k_01dfd2_end:
.org 0x1DFD6
m68k_01dfd6:
        bhi.w (. + 34)
m68k_01dfd6_end:
.org 0x1DFDA
m68k_01dfda:
        cmpi.w #0xf80,%d3
m68k_01dfda_end:
.org 0x1DFDE
m68k_01dfde:
        bhi.w (. + 10)
m68k_01dfde_end:
.org 0x1DFE2
m68k_01dfe2:
        move.w (%a6),%d4
m68k_01dfe2_end:
.org 0x1DFE4
m68k_01dfe4:
        bra.w (. + 24)
m68k_01dfe4_end:
.org 0x1DFE8
m68k_01dfe8:
        move.w #0x1f00,%d4
m68k_01dfe8_end:
.org 0x1DFEC
m68k_01dfec:
        sub.w %d3,%d4
m68k_01dfec_end:
.org 0x1DFEE
m68k_01dfee:
        move.w %d4,%d3
m68k_01dfee_end:
.org 0x1DFF0
m68k_01dff0:
        move.w 0x2(%a6),%d4
m68k_01dff0_end:
.org 0x1DFF4
m68k_01dff4:
        bra.w (. + 8)
m68k_01dff4_end:
.org 0x1DFF8
m68k_01dff8:
        move.w #0xffff,%d3
m68k_01dff8_end:
.org 0x1DFFC
m68k_01dffc:
        move.w %d2,%d5
m68k_01dffc_end:
.org 0x1DFFE
m68k_01dffe:
        sub.w 0x4(%a6),%d5
m68k_01dffe_end:
.org 0x1E002
m68k_01e002:
        bcs.w (. + 44)
m68k_01e002_end:
.org 0x1E006
m68k_01e006:
        cmpi.w #0x1f00,%d5
m68k_01e006_end:
.org 0x1E00A
m68k_01e00a:
        bhi.w (. + 36)
m68k_01e00a_end:
.org 0x1E00E
m68k_01e00e:
        cmpi.w #0xf80,%d5
m68k_01e00e_end:
.org 0x1E012
m68k_01e012:
        bhi.w (. + 12)
m68k_01e012_end:
.org 0x1E016
m68k_01e016:
        move.w 0x4(%a6),%d6
m68k_01e016_end:
.org 0x1E01A
m68k_01e01a:
        bra.w (. + 24)
m68k_01e01a_end:
.org 0x1E01E
m68k_01e01e:
        move.w #0x1f00,%d6
m68k_01e01e_end:
.org 0x1E022
m68k_01e022:
        sub.w %d5,%d6
m68k_01e022_end:
.org 0x1E024
m68k_01e024:
        move.w %d6,%d5
m68k_01e024_end:
.org 0x1E026
m68k_01e026:
        move.w 0x6(%a6),%d6
m68k_01e026_end:
.org 0x1E02A
m68k_01e02a:
        bra.w (. + 8)
m68k_01e02a_end:
.org 0x1E02E
m68k_01e02e:
        move.w #0xffff,%d5
m68k_01e02e_end:
.org 0x1E032
m68k_01e032:
        cmp.w %d3,%d5
m68k_01e032_end:
.org 0x1E034
m68k_01e034:
        bhi.w (. + 14)
m68k_01e034_end:
.org 0x1E038
m68k_01e038:
        move.w %d6,%d2
m68k_01e038_end:
.org 0x1E03A
m68k_01e03a:
        move.w %d2,0x2(%a1, %d0.w)
m68k_01e03a_end:
.org 0x1E03E
m68k_01e03e:
        bra.w (. + 10)
m68k_01e03e_end:
.org 0x1E042
m68k_01e042:
        move.w %d4,%d1
m68k_01e042_end:
.org 0x1E044
m68k_01e044:
        move.w %d4,(%a1, %d0.w)
m68k_01e044_end:
.org 0x1E048
m68k_01e048:
        movem.l (%a7)+,%d3-%d6
m68k_01e048_end:
.org 0x1E04C
m68k_01e04c:
        rts
m68k_01e04c_end:
.org 0x1E198
m68k_01e198:
        lea.l 0xad60:w,%a1
m68k_01e198_end:
.org 0x1E19C
m68k_01e19c:
        lea.l 0xa150:w,%a2
m68k_01e19c_end:
.org 0x1E1A0
m68k_01e1a0:
        lea.l 0xceae:w,%a4
m68k_01e1a0_end:
.org 0x1E1A4
m68k_01e1a4:
        lea.l 0xa550:w,%a0
m68k_01e1a4_end:
.org 0x1E1A8
m68k_01e1a8:
        bsr.w (. + 10)
m68k_01e1a8_end:
.org 0x1E1AC
m68k_01e1ac:
        move.w #0xffff,(%a1)
m68k_01e1ac_end:
.org 0x1E1B0
m68k_01e1b0:
        rts
m68k_01e1b0_end:
.org 0x1E1B2
m68k_01e1b2:
        move.w (%a0)+,%d0
m68k_01e1b2_end:
.org 0x1E1B4
m68k_01e1b4:
        bmi.w (. + 68)
m68k_01e1b4_end:
.org 0x1E1B8
m68k_01e1b8:
        andi.w #0xff,%d0
m68k_01e1b8_end:
.org 0x1E1BC
m68k_01e1bc:
        cmpi.b #0x55,(%a4, %d0.w)
m68k_01e1bc_end:
.org 0x1E1C2
m68k_01e1c2:
        bcc.b (. + -16)
m68k_01e1c2_end:
.org 0x1E1C4
m68k_01e1c4:
        move.w %d0,%d1
m68k_01e1c4_end:
.org 0x1E1C6
m68k_01e1c6:
        lsl.w #0x2,%d1
m68k_01e1c6_end:
.org 0x1E1C8
m68k_01e1c8:
        move.w (%a2, %d1.w),%d2
m68k_01e1c8_end:
.org 0x1E1CC
m68k_01e1cc:
        move.w %d2,%d3
m68k_01e1cc_end:
.org 0x1E1CE
m68k_01e1ce:
        subi.w #0x800,%d2
m68k_01e1ce_end:
.org 0x1E1D2
m68k_01e1d2:
        bcc.b (. + 4)
m68k_01e1d2_end:
.org 0x1E1D4
m68k_01e1d4:
        clr.w %d2
m68k_01e1d4_end:
.org 0x1E1D6
m68k_01e1d6:
        addi.w #0x800,%d3
m68k_01e1d6_end:
.org 0x1E1DA
m68k_01e1da:
        move.w 0x2(%a2, %d1.w),%d4
m68k_01e1da_end:
.org 0x1E1DE
m68k_01e1de:
        move.w %d4,%d5
m68k_01e1de_end:
.org 0x1E1E0
m68k_01e1e0:
        subi.w #0x800,%d4
m68k_01e1e0_end:
.org 0x1E1E4
m68k_01e1e4:
        bcc.b (. + 4)
m68k_01e1e4_end:
.org 0x1E1E6
m68k_01e1e6:
        clr.w %d4
m68k_01e1e6_end:
.org 0x1E1E8
m68k_01e1e8:
        addi.w #0x800,%d5
m68k_01e1e8_end:
.org 0x1E1EC
m68k_01e1ec:
        lsl.w #0x8,%d0
m68k_01e1ec_end:
.org 0x1E1EE
m68k_01e1ee:
        lea.l 0xa5a4:w,%a3
m68k_01e1ee_end:
.org 0x1E1F2
m68k_01e1f2:
        bsr.w (. + 8)
m68k_01e1f2_end:
.org 0x1E1F6
m68k_01e1f6:
        bra.b (. + -68)
m68k_01e1f6_end:
.org 0x1E1F8
m68k_01e1f8:
        rts
m68k_01e1f8_end:
.org 0x1E1FA
m68k_01e1fa:
        move.w (%a3)+,%d1
m68k_01e1fa_end:
.org 0x1E1FC
m68k_01e1fc:
        bmi.b (. + 48)
m68k_01e1fc_end:
.org 0x1E1FE
m68k_01e1fe:
        andi.w #0xff,%d1
m68k_01e1fe_end:
.org 0x1E202
m68k_01e202:
        cmpi.b #0x55,(%a4, %d1.w)
m68k_01e202_end:
.org 0x1E208
m68k_01e208:
        bcc.b (. + -14)
m68k_01e208_end:
.org 0x1E20A
m68k_01e20a:
        move.w %d1,%d6
m68k_01e20a_end:
.org 0x1E20C
m68k_01e20c:
        lsl.w #0x2,%d6
m68k_01e20c_end:
.org 0x1E20E
m68k_01e20e:
        move.w (%a2, %d6.w),%d7
m68k_01e20e_end:
.org 0x1E212
m68k_01e212:
        cmp.w %d2,%d7
m68k_01e212_end:
.org 0x1E214
m68k_01e214:
        bcs.b (. + -26)
m68k_01e214_end:
.org 0x1E216
m68k_01e216:
        cmp.w %d3,%d7
m68k_01e216_end:
.org 0x1E218
m68k_01e218:
        bhi.b (. + -30)
m68k_01e218_end:
.org 0x1E21A
m68k_01e21a:
        move.w 0x2(%a2, %d6.w),%d7
m68k_01e21a_end:
.org 0x1E21E
m68k_01e21e:
        cmp.w %d4,%d7
m68k_01e21e_end:
.org 0x1E220
m68k_01e220:
        bcs.b (. + -38)
m68k_01e220_end:
.org 0x1E222
m68k_01e222:
        cmp.w %d5,%d7
m68k_01e222_end:
.org 0x1E224
m68k_01e224:
        bhi.b (. + -42)
m68k_01e224_end:
.org 0x1E226
m68k_01e226:
        move.b %d1,%d0
m68k_01e226_end:
.org 0x1E228
m68k_01e228:
        move.w %d0,(%a1)+
m68k_01e228_end:
.org 0x1E22A
m68k_01e22a:
        bra.b (. + -48)
m68k_01e22a_end:
.org 0x1E22C
m68k_01e22c:
        rts
m68k_01e22c_end:
.org 0x1E22E
m68k_01e22e:
        move.w 0xf362:w,%d0
m68k_01e22e_end:
.org 0x1E232
m68k_01e232:
        lsl.w #0x1,%d0
m68k_01e232_end:
.org 0x1E234
m68k_01e234:
        move.w 8(%pc, %d0.w),%d0
m68k_01e234_end:
.org 0x1E238
m68k_01e238:
        jsr 18(%pc, %d0.w)
m68k_01e238_end:
.org 0x1E23C
m68k_01e23c:
        rts
m68k_01e23c_end:
.org 0x1E24C
m68k_01e24c:
        lea.l 0xa550:w,%a0
m68k_01e24c_end:
.org 0x1E250
m68k_01e250:
        lea.l 0xa5f8:w,%a1
m68k_01e250_end:
.org 0x1E254
m68k_01e254:
        move.w 0xf68a:w,%d0
m68k_01e254_end:
.org 0x1E258
m68k_01e258:
        lsl.w #0x3,%d0
m68k_01e258_end:
.org 0x1E25A
m68k_01e25a:
        lea.l 0xae1b2:l,%a2
m68k_01e25a_end:
.org 0x1E260
m68k_01e260:
        move.w (%a2, %d0.w),%d1
m68k_01e260_end:
.org 0x1E264
m68k_01e264:
        move.w 0x2(%a2, %d0.w),%d2
m68k_01e264_end:
.org 0x1E268
m68k_01e268:
        move.w 0x4(%a2, %d0.w),%d3
m68k_01e268_end:
.org 0x1E26C
m68k_01e26c:
        move.w 0x6(%a2, %d0.w),%d4
m68k_01e26c_end:
.org 0x1E270
m68k_01e270:
        lea.l 0xa150:w,%a2
m68k_01e270_end:
.org 0x1E274
m68k_01e274:
        lea.l 0xff3cc2:l,%a3
m68k_01e274_end:
.org 0x1E27A
m68k_01e27a:
        move.w (%a0)+,%d0
m68k_01e27a_end:
.org 0x1E27C
m68k_01e27c:
        bmi.b (. + 46)
m68k_01e27c_end:
.org 0x1E27E
m68k_01e27e:
        cmpi.w #0x100,%d0
m68k_01e27e_end:
.org 0x1E282
m68k_01e282:
        bcc.b (. + -8)
m68k_01e282_end:
.org 0x1E284
m68k_01e284:
        move.w %d0,%d5
m68k_01e284_end:
.org 0x1E286
m68k_01e286:
        lsl.w #0x2,%d5
m68k_01e286_end:
.org 0x1E288
m68k_01e288:
        cmp.w (%a2, %d5.w),%d1
m68k_01e288_end:
.org 0x1E28C
m68k_01e28c:
        bhi.b (. + -18)
m68k_01e28c_end:
.org 0x1E28E
m68k_01e28e:
        cmp.w (%a2, %d5.w),%d2
m68k_01e28e_end:
.org 0x1E292
m68k_01e292:
        bcs.b (. + -24)
m68k_01e292_end:
.org 0x1E294
m68k_01e294:
        cmp.w 0x2(%a2, %d5.w),%d3
m68k_01e294_end:
.org 0x1E298
m68k_01e298:
        bhi.b (. + -30)
m68k_01e298_end:
.org 0x1E29A
m68k_01e29a:
        cmp.w 0x2(%a2, %d5.w),%d4
m68k_01e29a_end:
.org 0x1E29E
m68k_01e29e:
        bcs.b (. + -36)
m68k_01e29e_end:
.org 0x1E2A0
m68k_01e2a0:
        tst.b (%a3, %d0.w)
m68k_01e2a0_end:
.org 0x1E2A4
m68k_01e2a4:
        bne.b (. + -42)
m68k_01e2a4_end:
.org 0x1E2A6
m68k_01e2a6:
        move.w %d0,(%a1)+
m68k_01e2a6_end:
.org 0x1E2A8
m68k_01e2a8:
        bra.b (. + -46)
m68k_01e2a8_end:
.org 0x1E2AA
m68k_01e2aa:
        move.w #0xffff,(%a1)
m68k_01e2aa_end:
.org 0x1E2AE
m68k_01e2ae:
        tst.w 0xa5f8:w
m68k_01e2ae_end:
.org 0x1E2B2
m68k_01e2b2:
        bmi.b (. + 28)
m68k_01e2b2_end:
.org 0x1E2B4
m68k_01e2b4:
        move.w 0xf612:w,0xf38a:w
m68k_01e2b4_end:
.org 0x1E2BA
m68k_01e2ba:
        move.w #0x2,0xf3b0:w
m68k_01e2ba_end:
.org 0x1E2C0
m68k_01e2c0:
        move.w #0x40a,0xf612:w
m68k_01e2c0_end:
.org 0x1E2C6
m68k_01e2c6:
        clr.w 0xf362:w
m68k_01e2c6_end:
.org 0x1E2CA
m68k_01e2ca:
        bra.w (. + 22)
m68k_01e2ca_end:
.org 0x1E2CE
m68k_01e2ce:
        addq.w #0x1,0xf362:w
m68k_01e2ce_end:
.org 0x1E2D2
m68k_01e2d2:
        move.w #0x139,%d0
m68k_01e2d2_end:
.org 0x1E2D6
m68k_01e2d6:
        move.w %d0,0xaf80:w
m68k_01e2d6_end:
.org 0x1E2DA
m68k_01e2da:
        jsr 0x676f2:l
m68k_01e2da_end:
.org 0x1E2E0
m68k_01e2e0:
        rts
m68k_01e2e0_end:
.org 0x1E2E2
m68k_01e2e2:
        move.b 0xf602:w,%d0
m68k_01e2e2_end:
.org 0x1E2E6
m68k_01e2e6:
        andi.w #0x30,%d0
m68k_01e2e6_end:
.org 0x1E2EA
m68k_01e2ea:
        beq.b (. + 12)
m68k_01e2ea_end:
.org 0x1E2EC
m68k_01e2ec:
        move.w #0x408,0xf612:w
m68k_01e2ec_end:
.org 0x1E2F2
m68k_01e2f2:
        clr.w 0xf362:w
m68k_01e2f2_end:
.org 0x1E2F6
m68k_01e2f6:
        rts
m68k_01e2f6_end:
.org 0x1E2F8
m68k_01e2f8:
        tst.w 0xf3a6:w
m68k_01e2f8_end:
.org 0x1E2FC
m68k_01e2fc:
        bmi.w (. + 108)
m68k_01e2fc_end:
.org 0x1E300
m68k_01e300:
        move.w #0x1,0xf6f6:w
m68k_01e300_end:
.org 0x1E306
m68k_01e306:
        move.w #0xffff,0xa5f8:w
m68k_01e306_end:
.org 0x1E30C
m68k_01e30c:
        bsr.w (. + 278)
m68k_01e30c_end:
.org 0x1E310
m68k_01e310:
        bcc.b (. + 60)
m68k_01e310_end:
.org 0x1E312
m68k_01e312:
        move.w 0xf3a6:w,0xf3f2:w
m68k_01e312_end:
.org 0x1E318
m68k_01e318:
        bsr.w (. + 332)
m68k_01e318_end:
.org 0x1E31C
m68k_01e31c:
        move.w %d6,0xf706:w
m68k_01e31c_end:
.org 0x1E320
m68k_01e320:
        bmi.w (. + 44)
m68k_01e320_end:
.org 0x1E324
m68k_01e324:
        addq.w #0x1,0xf362:w
m68k_01e324_end:
.org 0x1E328
m68k_01e328:
        move.w 0xf3f2:w,0xf702:w
m68k_01e328_end:
.org 0x1E32E
m68k_01e32e:
        move.w 0xf702:w,0xf3d0:w
m68k_01e32e_end:
.org 0x1E334
m68k_01e334:
        move.w 0xf706:w,0xf3d2:w
m68k_01e334_end:
.org 0x1E33A
m68k_01e33a:
        move.w #0x114,%d0
m68k_01e33a_end:
.org 0x1E33E
m68k_01e33e:
        move.w %d0,0xaf80:w
m68k_01e33e_end:
.org 0x1E342
m68k_01e342:
        jsr 0x676f2:l
m68k_01e342_end:
.org 0x1E348
m68k_01e348:
        bra.w (. + 42)
m68k_01e348_end:
.org 0x1E34C
m68k_01e34c:
        addq.w #0x2,0xf362:w
m68k_01e34c_end:
.org 0x1E350
m68k_01e350:
        move.w 0xf3a6:w,0xf3d0:w
m68k_01e350_end:
.org 0x1E356
m68k_01e356:
        move.w #0x112,%d0
m68k_01e356_end:
.org 0x1E35A
m68k_01e35a:
        move.w %d0,0xaf80:w
m68k_01e35a_end:
.org 0x1E35E
m68k_01e35e:
        jsr 0x676f2:l
m68k_01e35e_end:
.org 0x1E364
m68k_01e364:
        bra.w (. + 14)
m68k_01e364_end:
.org 0x1E368
m68k_01e368:
        move.w #0x408,0xf612:w
m68k_01e368_end:
.org 0x1E36E
m68k_01e36e:
        clr.w 0xf362:w
m68k_01e36e_end:
.org 0x1E372
m68k_01e372:
        rts
m68k_01e372_end:
.org 0x1E374
m68k_01e374:
        move.b 0xf602:w,%d0
m68k_01e374_end:
.org 0x1E378
m68k_01e378:
        andi.w #0x30,%d0
m68k_01e378_end:
.org 0x1E37C
m68k_01e37c:
        beq.b (. + 28)
m68k_01e37c_end:
.org 0x1E37E
m68k_01e37e:
        move.w #0x2,0xf772:w
m68k_01e37e_end:
.org 0x1E384
m68k_01e384:
        move.w #0x407,0xf612:w
m68k_01e384_end:
.org 0x1E38A
m68k_01e38a:
        move.w #0x3,0xf362:w
m68k_01e38a_end:
.org 0x1E390
m68k_01e390:
        clr.w 0xf352:w
m68k_01e390_end:
.org 0x1E394
m68k_01e394:
        bsr.w (. + 6)
m68k_01e394_end:
.org 0x1E398
m68k_01e398:
        rts
m68k_01e398_end:
.org 0x1E39A
m68k_01e39a:
        lea.l 0xa550:w,%a0
m68k_01e39a_end:
.org 0x1E39E
m68k_01e39e:
        move.w 0xf3f2:w,%d0
m68k_01e39e_end:
.org 0x1E3A2
m68k_01e3a2:
        move.w (%a0)+,%d1
m68k_01e3a2_end:
.org 0x1E3A4
m68k_01e3a4:
        andi.w #0xff,%d1
m68k_01e3a4_end:
.org 0x1E3A8
m68k_01e3a8:
        cmp.w %d0,%d1
m68k_01e3a8_end:
.org 0x1E3AA
m68k_01e3aa:
        bne.b (. + -8)
m68k_01e3aa_end:
.org 0x1E3AC
m68k_01e3ac:
        bset.b #0x6,-0x2(%a0)
m68k_01e3ac_end:
.org 0x1E3B2
m68k_01e3b2:
        rts
m68k_01e3b2_end:
.org 0x1E3B4
m68k_01e3b4:
        move.b 0xf602:w,%d0
m68k_01e3b4_end:
.org 0x1E3B8
m68k_01e3b8:
        andi.w #0x30,%d0
m68k_01e3b8_end:
.org 0x1E3BC
m68k_01e3bc:
        beq.w (. + 28)
m68k_01e3bc_end:
.org 0x1E3C0
m68k_01e3c0:
        move.w 0xf3a6:w,0xf3f2:w
m68k_01e3c0_end:
.org 0x1E3C6
m68k_01e3c6:
        bsr.w (. + 158)
m68k_01e3c6_end:
.org 0x1E3CA
m68k_01e3ca:
        move.w %d6,0xf3a6:w
m68k_01e3ca_end:
.org 0x1E3CE
m68k_01e3ce:
        move.w #0xa4,0xf600:w
m68k_01e3ce_end:
.org 0x1E3D4
m68k_01e3d4:
        addq.w #0x1,0xf362:w
m68k_01e3d4_end:
.org 0x1E3D8
m68k_01e3d8:
        rts
m68k_01e3d8_end:
.org 0x1E3DA
m68k_01e3da:
        addq.w #0x1,0xf362:w
m68k_01e3da_end:
.org 0x1E3DE
m68k_01e3de:
        move.w 0xf68a:w,%d0
m68k_01e3de_end:
.org 0x1E3E2
m68k_01e3e2:
        lsl.w #0x2,%d0
m68k_01e3e2_end:
.org 0x1E3E4
m68k_01e3e4:
        lea.l 0xe59c:w,%a0
m68k_01e3e4_end:
.org 0x1E3E8
m68k_01e3e8:
        move.l (%a0, %d0.w),0xf3c8:w
m68k_01e3e8_end:
.org 0x1E3EE
m68k_01e3ee:
        move.w #0x113,%d0
m68k_01e3ee_end:
.org 0x1E3F2
m68k_01e3f2:
        move.w %d0,0xaf80:w
m68k_01e3f2_end:
.org 0x1E3F6
m68k_01e3f6:
        jsr 0x676f2:l
m68k_01e3f6_end:
.org 0x1E3FC
m68k_01e3fc:
        move.w 0xf3f2:w,0xf3a6:w
m68k_01e3fc_end:
.org 0x1E402
m68k_01e402:
        jsr 0x1e5d2:l
m68k_01e402_end:
.org 0x1E408
m68k_01e408:
        rts
m68k_01e408_end:
.org 0x1E40A
m68k_01e40a:
        move.b 0xf602:w,%d0
m68k_01e40a_end:
.org 0x1E40E
m68k_01e40e:
        andi.w #0x30,%d0
m68k_01e40e_end:
.org 0x1E412
m68k_01e412:
        beq.w (. + 14)
m68k_01e412_end:
.org 0x1E416
m68k_01e416:
        move.w #0x408,0xf612:w
m68k_01e416_end:
.org 0x1E41C
m68k_01e41c:
        clr.w 0xf362:w
m68k_01e41c_end:
.org 0x1E420
m68k_01e420:
        rts
m68k_01e420_end:
.org 0x1E422
m68k_01e422:
        jsr 0x83d4:l
m68k_01e422_end:
.org 0x1E428
m68k_01e428:
        move.w 0xf68a:w,%d0
m68k_01e428_end:
.org 0x1E42C
m68k_01e42c:
        lsl.w #0x2,%d0
m68k_01e42c_end:
.org 0x1E42E
m68k_01e42e:
        lea.l 0xe59c:w,%a0
m68k_01e42e_end:
.org 0x1E432
m68k_01e432:
        move.w 0x2(%a0, %d0.w),%d0
m68k_01e432_end:
.org 0x1E436
m68k_01e436:
        cmpi.w #0x1e,%d0
m68k_01e436_end:
.org 0x1E43A
m68k_01e43a:
        bcc.b (. + 36)
m68k_01e43a_end:
.org 0x1E43C
m68k_01e43c:
        moveq #0,%d1
m68k_01e43c_end:
.org 0x1E43E
m68k_01e43e:
        move.w 0xf61c:w,%d1
m68k_01e43e_end:
.org 0x1E442
m68k_01e442:
        move.l %d1,%d2
m68k_01e442_end:
.org 0x1E444
m68k_01e444:
        lsl.l #0x1,%d1
m68k_01e444_end:
.org 0x1E446
m68k_01e446:
        add.l %d2,%d1
m68k_01e446_end:
.org 0x1E448
m68k_01e448:
        lsl.l #0x3,%d1
m68k_01e448_end:
.org 0x1E44A
m68k_01e44a:
        add.l %d2,%d1
m68k_01e44a_end:
.org 0x1E44C
m68k_01e44c:
        lsl.l #0x2,%d1
m68k_01e44c_end:
.org 0x1E44E
m68k_01e44e:
        swap %d1
m68k_01e44e_end:
.org 0x1E450
m68k_01e450:
        cmp.w %d0,%d1
m68k_01e450_end:
.org 0x1E452
m68k_01e452:
        bcs.w (. + 12)
m68k_01e452_end:
.org 0x1E456
m68k_01e456:
        ori.w #0x1,%sr
m68k_01e456_end:
.org 0x1E45A
m68k_01e45a:
        bra.w (. + 8)
m68k_01e45a_end:
.org 0x1E45E
m68k_01e45e:
        andi.w #0xfffe,%sr
m68k_01e45e_end:
.org 0x1E462
m68k_01e462:
        rts
m68k_01e462_end:
.org 0x1E464
m68k_01e464:
        jsr 0x1a438:l
m68k_01e464_end:
.org 0x1E46A
m68k_01e46a:
        lea.l 0xa5a4:w,%a1
m68k_01e46a_end:
.org 0x1E46E
m68k_01e46e:
        lea.l 0xa150:w,%a2
m68k_01e46e_end:
.org 0x1E472
m68k_01e472:
        move.w 0xf3f2:w,%d0
m68k_01e472_end:
.org 0x1E476
m68k_01e476:
        lsl.w #0x2,%d0
m68k_01e476_end:
.org 0x1E478
m68k_01e478:
        move.w (%a2, %d0.w),%d3
m68k_01e478_end:
.org 0x1E47C
m68k_01e47c:
        lsr.w #0x7,%d3
m68k_01e47c_end:
.org 0x1E47E
m68k_01e47e:
        move.w 0x2(%a2, %d0.w),%d4
m68k_01e47e_end:
.org 0x1E482
m68k_01e482:
        lsr.w #0x7,%d4
m68k_01e482_end:
.org 0x1E484
m68k_01e484:
        move.w #0xffff,%d5
m68k_01e484_end:
.org 0x1E488
m68k_01e488:
        move.w #0x8000,%d6
m68k_01e488_end:
.org 0x1E48C
m68k_01e48c:
        move.w (%a1)+,%d7
m68k_01e48c_end:
.org 0x1E48E
m68k_01e48e:
        bmi.w (. + 82)
m68k_01e48e_end:
.org 0x1E492
m68k_01e492:
        andi.w #0xff,%d7
m68k_01e492_end:
.org 0x1E496
m68k_01e496:
        lsl.w #0x2,%d7
m68k_01e496_end:
.org 0x1E498
m68k_01e498:
        move.w (%a2, %d7.w),%d1
m68k_01e498_end:
.org 0x1E49C
m68k_01e49c:
        lsr.w #0x7,%d1
m68k_01e49c_end:
.org 0x1E49E
m68k_01e49e:
        move.w 0x2(%a2, %d7.w),%d2
m68k_01e49e_end:
.org 0x1E4A2
m68k_01e4a2:
        lsr.w #0x7,%d2
m68k_01e4a2_end:
.org 0x1E4A4
m68k_01e4a4:
        jsr 0x1a44e:l
m68k_01e4a4_end:
.org 0x1E4AA
m68k_01e4aa:
        cmpi.b #0x6,%d0
m68k_01e4aa_end:
.org 0x1E4AE
m68k_01e4ae:
        bne.b (. + -34)
m68k_01e4ae_end:
.org 0x1E4B0
m68k_01e4b0:
        sub.w %d3,%d1
m68k_01e4b0_end:
.org 0x1E4B2
m68k_01e4b2:
        bcc.b (. + 4)
m68k_01e4b2_end:
.org 0x1E4B4
m68k_01e4b4:
        neg.w %d1
m68k_01e4b4_end:
.org 0x1E4B6
m68k_01e4b6:
        mulu.w %d1,%d1
m68k_01e4b6_end:
.org 0x1E4B8
m68k_01e4b8:
        sub.w %d4,%d2
m68k_01e4b8_end:
.org 0x1E4BA
m68k_01e4ba:
        bcc.b (. + 4)
m68k_01e4ba_end:
.org 0x1E4BC
m68k_01e4bc:
        neg.w %d2
m68k_01e4bc_end:
.org 0x1E4BE
m68k_01e4be:
        mulu.w %d2,%d2
m68k_01e4be_end:
.org 0x1E4C0
m68k_01e4c0:
        move.l %d1,%d0
m68k_01e4c0_end:
.org 0x1E4C2
m68k_01e4c2:
        add.l %d2,%d0
m68k_01e4c2_end:
.org 0x1E4C4
m68k_01e4c4:
        jsr 0x3080e:l
m68k_01e4c4_end:
.org 0x1E4CA
m68k_01e4ca:
        cmp.w %d5,%d0
m68k_01e4ca_end:
.org 0x1E4CC
m68k_01e4cc:
        bcs.b (. + 12)
m68k_01e4cc_end:
.org 0x1E4CE
m68k_01e4ce:
        bne.b (. + -66)
m68k_01e4ce_end:
.org 0x1E4D0
m68k_01e4d0:
        btst.b #0x0,0xf321:w
m68k_01e4d0_end:
.org 0x1E4D6
m68k_01e4d6:
        bne.b (. + -74)
m68k_01e4d6_end:
.org 0x1E4D8
m68k_01e4d8:
        move.w %d0,%d5
m68k_01e4d8_end:
.org 0x1E4DA
m68k_01e4da:
        lsr.w #0x2,%d7
m68k_01e4da_end:
.org 0x1E4DC
m68k_01e4dc:
        move.w %d7,%d6
m68k_01e4dc_end:
.org 0x1E4DE
m68k_01e4de:
        bra.b (. + -82)
m68k_01e4de_end:
.org 0x1E4E0
m68k_01e4e0:
        rts
m68k_01e4e0_end:
.org 0x1E5D2
m68k_01e5d2:
        move.w 0xf6d6:w,%d0
m68k_01e5d2_end:
.org 0x1E5D6
m68k_01e5d6:
        andi.w #0x2,%d0
m68k_01e5d6_end:
.org 0x1E5DA
m68k_01e5da:
        lsl.w #0x1,%d0
m68k_01e5da_end:
.org 0x1E5DC
m68k_01e5dc:
        movea.l 24(%pc, %d0.w),%a0
m68k_01e5dc_end:
.org 0x1E5E0
m68k_01e5e0:
        move.w 0xf3a6:w,%d0
m68k_01e5e0_end:
.org 0x1E5E4
m68k_01e5e4:
        clr.w %d1
m68k_01e5e4_end:
.org 0x1E5E6
m68k_01e5e6:
        addq.w #0x1,%d1
m68k_01e5e6_end:
.org 0x1E5E8
m68k_01e5e8:
        cmp.w (%a0)+,%d0
m68k_01e5e8_end:
.org 0x1E5EA
m68k_01e5ea:
        bne.b (. + -4)
m68k_01e5ea_end:
.org 0x1E5EC
m68k_01e5ec:
        ori.w #0x4000,-0x2(%a0)
m68k_01e5ec_end:
.org 0x1E5F2
m68k_01e5f2:
        subq.w #0x1,%d1
m68k_01e5f2_end:
.org 0x1E5F4
m68k_01e5f4:
        rts
m68k_01e5f4_end:
.org 0x1EF7A
m68k_01ef7a:
        move.w 0xf362:w,%d0
m68k_01ef7a_end:
.org 0x1EF7E
m68k_01ef7e:
        lsl.w #0x1,%d0
m68k_01ef7e_end:
.org 0x1EF80
m68k_01ef80:
        move.w 8(%pc, %d0.w),%d0
m68k_01ef80_end:
.org 0x1EF84
m68k_01ef84:
        jsr 18(%pc, %d0.w)
m68k_01ef84_end:
.org 0x1EF88
m68k_01ef88:
        rts
m68k_01ef88_end:
.org 0x1EF98
m68k_01ef98:
        move.w 0xf320:w,%d0
m68k_01ef98_end:
.org 0x1EF9C
m68k_01ef9c:
        andi.w #0x3,%d0
m68k_01ef9c_end:
.org 0x1EFA0
m68k_01efa0:
        bne.w (. + 14)
m68k_01efa0_end:
.org 0x1EFA4
m68k_01efa4:
        jsr 0x662e4:l
m68k_01efa4_end:
.org 0x1EFAA
m68k_01efaa:
        bcs.w (. + 258)
m68k_01efaa_end:
.org 0x1EFAE
m68k_01efae:
        jsr 0x1dd80:l
m68k_01efae_end:
.org 0x1EFB4
m68k_01efb4:
        jsr 0x1e0fe:l
m68k_01efb4_end:
.org 0x1EFBA
m68k_01efba:
        jsr 0x1e198:l
m68k_01efba_end:
.org 0x1EFC0
m68k_01efc0:
        cmpi.w #0xffff,0xad60:w
m68k_01efc0_end:
.org 0x1EFC6
m68k_01efc6:
        bne.w (. + 170)
m68k_01efc6_end:
.org 0x1EFCA
m68k_01efca:
        move.w 0xf68c:w,%d0
m68k_01efca_end:
.org 0x1EFCE
m68k_01efce:
        move.w 0xf68e:w,%d1
m68k_01efce_end:
.org 0x1EFD2
m68k_01efd2:
        btst.b #0x6,0xf603:w
m68k_01efd2_end:
.org 0x1EFD8
m68k_01efd8:
        bne.w (. + 12)
m68k_01efd8_end:
.org 0x1EFDC
m68k_01efdc:
        btst.b #0x6,0xf605:w
m68k_01efdc_end:
.org 0x1EFE2
m68k_01efe2:
        beq.b (. + 66)
m68k_01efe2_end:
.org 0x1EFE4
m68k_01efe4:
        bsr.w (. + 706)
m68k_01efe4_end:
.org 0x1EFE8
m68k_01efe8:
        bcs.w (. + 60)
m68k_01efe8_end:
.org 0x1EFEC
m68k_01efec:
        move.w #0xad,%d0
m68k_01efec_end:
.org 0x1EFF0
m68k_01eff0:
        jsr 0x808a:l
m68k_01eff0_end:
.org 0x1EFF6
m68k_01eff6:
        move.w 0xf612:w,0xf38a:w
m68k_01eff6_end:
.org 0x1EFFC
m68k_01effc:
        move.w 0xf362:w,0xf3b0:w
m68k_01effc_end:
.org 0x1F002
m68k_01f002:
        move.w #0x402,0xf612:w
m68k_01f002_end:
.org 0x1F008
m68k_01f008:
        move.w #0x88,0xf600:w
m68k_01f008_end:
.org 0x1F00E
m68k_01f00e:
        lea.l 0xab8c4:l,%a0
m68k_01f00e_end:
.org 0x1F014
m68k_01f014:
        move.l %a0,0xf6c0:w
m68k_01f014_end:
.org 0x1F018
m68k_01f018:
        clr.w 0xf36a:w
m68k_01f018_end:
.org 0x1F01C
m68k_01f01c:
        clr.w 0xf362:w
m68k_01f01c_end:
.org 0x1F020
m68k_01f020:
        bra.w (. + 266)
m68k_01f020_end:
.org 0x1F024
m68k_01f024:
        btst.b #0x5,0xf603:w
m68k_01f024_end:
.org 0x1F02A
m68k_01f02a:
        bne.w (. + 14)
m68k_01f02a_end:
.org 0x1F02E
m68k_01f02e:
        btst.b #0x5,0xf605:w
m68k_01f02e_end:
.org 0x1F034
m68k_01f034:
        beq.w (. + 68)
m68k_01f034_end:
.org 0x1F038
m68k_01f038:
        bsr.w (. + 286)
m68k_01f038_end:
.org 0x1F03C
m68k_01f03c:
        bcs.w (. + 60)
m68k_01f03c_end:
.org 0x1F040
m68k_01f040:
        move.w 0xf6d6:w,%d0
m68k_01f040_end:
.org 0x1F044
m68k_01f044:
        andi.w #0x3,%d0
m68k_01f044_end:
.org 0x1F048
m68k_01f048:
        btst.l %d0,0xf6f8:w
m68k_01f048_end:
.org 0x1F04C
m68k_01f04c:
        bne.w (. + 222)
m68k_01f04c_end:
.org 0x1F050
m68k_01f050:
        move.w #0xac,%d0
m68k_01f050_end:
.org 0x1F054
m68k_01f054:
        jsr 0x808a:l
m68k_01f054_end:
.org 0x1F05A
m68k_01f05a:
        move.w #0x408,0xf612:w
m68k_01f05a_end:
.org 0x1F060
m68k_01f060:
        clr.w 0xf362:w
m68k_01f060_end:
.org 0x1F064
m68k_01f064:
        clr.w 0xf6f6:w
m68k_01f064_end:
.org 0x1F068
m68k_01f068:
        clr.w 0xf6d4:w
m68k_01f068_end:
.org 0x1F06C
m68k_01f06c:
        bra.w (. + 194)
m68k_01f06c_end:
.org 0x1F070
m68k_01f070:
        addq.w #0x1,0xf362:w
m68k_01f070_end:
.org 0x1F074
m68k_01f074:
        bra.w (. + 182)
m68k_01f074_end:
.org 0x1F078
m68k_01f078:
        bsr.w (. + 720)
m68k_01f078_end:
.org 0x1F07C
m68k_01f07c:
        andi.w #0x3,%d0
m68k_01f07c_end:
.org 0x1F080
m68k_01f080:
        beq.b (. + 104)
m68k_01f080_end:
.org 0x1F082
m68k_01f082:
        btst.l #0x1,%d0
m68k_01f082_end:
.org 0x1F086
m68k_01f086:
        bne.w (. + 22)
m68k_01f086_end:
.org 0x1F08A
m68k_01f08a:
        cmpi.w #0x3,0xf70a:w
m68k_01f08a_end:
.org 0x1F090
m68k_01f090:
        bcc.w (. + 154)
m68k_01f090_end:
.org 0x1F094
m68k_01f094:
        addq.w #0x1,0xf70a:w
m68k_01f094_end:
.org 0x1F098
m68k_01f098:
        bra.w (. + 146)
m68k_01f098_end:
.org 0x1F09C
m68k_01f09c:
        tst.w 0xf70a:w
m68k_01f09c_end:
.org 0x1F0A0
m68k_01f0a0:
        beq.w (. + 138)
m68k_01f0a0_end:
.org 0x1F0A4
m68k_01f0a4:
        subq.w #0x1,0xf70a:w
m68k_01f0a4_end:
.org 0x1F0A8
m68k_01f0a8:
        bra.w (. + 130)
m68k_01f0a8_end:
.org 0x1F0AC
m68k_01f0ac:
        move.w #0x4,0xf362:w
m68k_01f0ac_end:
.org 0x1F0B2
m68k_01f0b2:
        move.w #0x9c,%d0
m68k_01f0b2_end:
.org 0x1F0B6
m68k_01f0b6:
        jsr 0x676f2:l
m68k_01f0b6_end:
.org 0x1F0BC
m68k_01f0bc:
        move.w 0xef78:w,%d0
m68k_01f0bc_end:
.org 0x1F0C0
m68k_01f0c0:
        lea.l 0xcc00:w,%a0
m68k_01f0c0_end:
.org 0x1F0C4
m68k_01f0c4:
        move.b (%a0, %d0.w),%d0
m68k_01f0c4_end:
.org 0x1F0C8
m68k_01f0c8:
        andi.w #0x3f,%d0
m68k_01f0c8_end:
.org 0x1F0CC
m68k_01f0cc:
        lea.l 0xf427:w,%a0
m68k_01f0cc_end:
.org 0x1F0D0
m68k_01f0d0:
        move.b (%a0, %d0.w),%d0
m68k_01f0d0_end:
.org 0x1F0D4
m68k_01f0d4:
        clr.w %d1
m68k_01f0d4_end:
.org 0x1F0D6
m68k_01f0d6:
        cmp.w 0xf68c:w,%d0
m68k_01f0d6_end:
.org 0x1F0DA
m68k_01f0da:
        beq.w (. + 8)
m68k_01f0da_end:
.org 0x1F0DE
m68k_01f0de:
        bset.l #0x1,%d1
m68k_01f0de_end:
.org 0x1F0E2
m68k_01f0e2:
        move.w %d1,0xf6d6:w
m68k_01f0e2_end:
.org 0x1F0E6
m68k_01f0e6:
        beq.b (. + 68)
m68k_01f0e6_end:
.org 0x1F0E8
m68k_01f0e8:
        btst.b #0x7,0xf603:w
m68k_01f0e8_end:
.org 0x1F0EE
m68k_01f0ee:
        bne.w (. + 14)
m68k_01f0ee_end:
.org 0x1F0F2
m68k_01f0f2:
        btst.b #0x7,0xf605:w
m68k_01f0f2_end:
.org 0x1F0F8
m68k_01f0f8:
        beq.w (. + 50)
m68k_01f0f8_end:
.org 0x1F0FC
m68k_01f0fc:
        bsr.w (. + 264)
m68k_01f0fc_end:
.org 0x1F100
m68k_01f100:
        bcs.w (. + 42)
m68k_01f100_end:
.org 0x1F104
m68k_01f104:
        move.w #0xac,%d0
m68k_01f104_end:
.org 0x1F108
m68k_01f108:
        jsr 0x808a:l
m68k_01f108_end:
.org 0x1F10E
m68k_01f10e:
        move.w #0x412,0xf612:w
m68k_01f10e_end:
.org 0x1F114
m68k_01f114:
        clr.w 0xf362:w
m68k_01f114_end:
.org 0x1F118
m68k_01f118:
        move.w #0x4,0xf6d2:w
m68k_01f118_end:
.org 0x1F11E
m68k_01f11e:
        move.w #0x68,0xf35e:w
m68k_01f11e_end:
.org 0x1F124
m68k_01f124:
        move.w #0x98,0xf360:w
m68k_01f124_end:
.org 0x1F12A
m68k_01f12a:
        bsr.w (. + 2344)
m68k_01f12a_end:
.org 0x1F12E
m68k_01f12e:
        bsr.w (. + 14)
m68k_01f12e_end:
.org 0x1F132
m68k_01f132:
        bsr.w (. + 4016)
m68k_01f132_end:
.org 0x1F136
m68k_01f136:
        bsr.w (. + 3922)
m68k_01f136_end:
.org 0x1F13A
m68k_01f13a:
        rts
m68k_01f13a_end:
.org 0x1F3C4
m68k_01f3c4:
        bsr.w (. + 154)
m68k_01f3c4_end:
.org 0x1F3C8
m68k_01f3c8:
        cmpi.w #0xffff,0xa5f8:w
m68k_01f3c8_end:
.org 0x1F3CE
m68k_01f3ce:
        beq.w (. + 92)
m68k_01f3ce_end:
.org 0x1F3D2
m68k_01f3d2:
        tst.w 0xf766:w
m68k_01f3d2_end:
.org 0x1F3D6
m68k_01f3d6:
        bpl.w (. + 92)
m68k_01f3d6_end:
.org 0x1F3DA
m68k_01f3da:
        addq.w #0x1,0xf362:w
m68k_01f3da_end:
.org 0x1F3DE
m68k_01f3de:
        move.w 0xf702:w,%d0
m68k_01f3de_end:
.org 0x1F3E2
m68k_01f3e2:
        move.w 0xf706:w,%d1
m68k_01f3e2_end:
.org 0x1F3E6
m68k_01f3e6:
        move.w 0xf68c:w,%d2
m68k_01f3e6_end:
.org 0x1F3EA
m68k_01f3ea:
        cmp.w 0xf67a:w,%d2
m68k_01f3ea_end:
.org 0x1F3EE
m68k_01f3ee:
        beq.w (. + 22)
m68k_01f3ee_end:
.org 0x1F3F2
m68k_01f3f2:
        cmp.w 0xf67c:w,%d2
m68k_01f3f2_end:
.org 0x1F3F6
m68k_01f3f6:
        beq.w (. + 14)
m68k_01f3f6_end:
.org 0x1F3FA
m68k_01f3fa:
        cmp.w 0xf67e:w,%d2
m68k_01f3fa_end:
.org 0x1F3FE
m68k_01f3fe:
        beq.w (. + 6)
m68k_01f3fe_end:
.org 0x1F402
m68k_01f402:
        exg %d0,%d1
m68k_01f402_end:
.org 0x1F404
m68k_01f404:
        move.w %d0,0xf3d0:w
m68k_01f404_end:
.org 0x1F408
m68k_01f408:
        move.w %d1,0xf3d2:w
m68k_01f408_end:
.org 0x1F40C
m68k_01f40c:
        move.w #0x114,%d0
m68k_01f40c_end:
.org 0x1F410
m68k_01f410:
        move.w %d0,0xaf80:w
m68k_01f410_end:
.org 0x1F414
m68k_01f414:
        jsr 0x676f2:l
m68k_01f414_end:
.org 0x1F41A
m68k_01f41a:
        move.w #0xffff,0xf704:w
m68k_01f41a_end:
.org 0x1F420
m68k_01f420:
        move.w #0xffff,0xf708:w
m68k_01f420_end:
.org 0x1F426
m68k_01f426:
        bra.w (. + 54)
m68k_01f426_end:
.org 0x1F42A
m68k_01f42a:
        clr.w 0xf362:w
m68k_01f42a_end:
.org 0x1F42E
m68k_01f42e:
        bra.w (. + 46)
m68k_01f42e_end:
.org 0x1F432
m68k_01f432:
        btst.b #0x6,0xf766:w
m68k_01f432_end:
.org 0x1F438
m68k_01f438:
        bne.w (. + 16)
m68k_01f438_end:
.org 0x1F43C
m68k_01f43c:
        bsr.w (. + 370)
m68k_01f43c_end:
.org 0x1F440
m68k_01f440:
        move.w #0x131,%d0
m68k_01f440_end:
.org 0x1F444
m68k_01f444:
        bra.w (. + 8)
m68k_01f444_end:
.org 0x1F448
m68k_01f448:
        move.w #0x132,%d0
m68k_01f448_end:
.org 0x1F44C
m68k_01f44c:
        move.w #0x6,0xf362:w
m68k_01f44c_end:
.org 0x1F452
m68k_01f452:
        jsr 0x676f2:l
m68k_01f452_end:
.org 0x1F458
m68k_01f458:
        bsr.w (. + 550)
m68k_01f458_end:
.org 0x1F45C
m68k_01f45c:
        rts
m68k_01f45c_end:
.org 0x1F45E
m68k_01f45e:
        jsr 0x83d4:l
m68k_01f45e_end:
.org 0x1F464
m68k_01f464:
        lea.l 0xad60:w,%a0
m68k_01f464_end:
.org 0x1F468
m68k_01f468:
        lea.l 0xa5f8:w,%a1
m68k_01f468_end:
.org 0x1F46C
m68k_01f46c:
        lea.l 0xff3bc2:l,%a2
m68k_01f46c_end:
.org 0x1F472
m68k_01f472:
        move.w (%a0)+,%d0
m68k_01f472_end:
.org 0x1F474
m68k_01f474:
        beq.b (. + -2)
m68k_01f474_end:
.org 0x1F476
m68k_01f476:
        cmpi.w #0xffff,%d0
m68k_01f476_end:
.org 0x1F47A
m68k_01f47a:
        beq.w (. + 42)
m68k_01f47a_end:
.org 0x1F47E
m68k_01f47e:
        clr.w %d1
m68k_01f47e_end:
.org 0x1F480
m68k_01f480:
        move.b %d0,%d1
m68k_01f480_end:
.org 0x1F482
m68k_01f482:
        lsr.w #0x8,%d0
m68k_01f482_end:
.org 0x1F484
m68k_01f484:
        move.w %d0,0xf702:w
m68k_01f484_end:
.org 0x1F488
m68k_01f488:
        move.w %d0,%d2
m68k_01f488_end:
.org 0x1F48A
m68k_01f48a:
        move.w %d1,%d3
m68k_01f48a_end:
.org 0x1F48C
m68k_01f48c:
        bsr.w (. + 30)
m68k_01f48c_end:
.org 0x1F490
m68k_01f490:
        move.w %d0,(%a1)+
m68k_01f490_end:
.org 0x1F492
m68k_01f492:
        move.w %d1,0xf706:w
m68k_01f492_end:
.org 0x1F496
m68k_01f496:
        move.w %d1,%d2
m68k_01f496_end:
.org 0x1F498
m68k_01f498:
        move.w %d0,%d3
m68k_01f498_end:
.org 0x1F49A
m68k_01f49a:
        bsr.w (. + 16)
m68k_01f49a_end:
.org 0x1F49E
m68k_01f49e:
        move.w %d1,(%a1)+
m68k_01f49e_end:
.org 0x1F4A0
m68k_01f4a0:
        clr.w -0x2(%a0)
m68k_01f4a0_end:
.org 0x1F4A4
m68k_01f4a4:
        move.w #0xffff,(%a1)
m68k_01f4a4_end:
.org 0x1F4A8
m68k_01f4a8:
        rts
m68k_01f4a8_end:
.org 0x1F4AA
m68k_01f4aa:
        tst.b (%a2, %d2.w)
m68k_01f4aa_end:
.org 0x1F4AE
m68k_01f4ae:
        beq.w (. + 88)
m68k_01f4ae_end:
.org 0x1F4B2
m68k_01f4b2:
        move.w %d2,0xf766:w
m68k_01f4b2_end:
.org 0x1F4B6
m68k_01f4b6:
        move.w %d3,0xf3d0:w
m68k_01f4b6_end:
.org 0x1F4BA
m68k_01f4ba:
        moveq #0,%d4
m68k_01f4ba_end:
.org 0x1F4BC
m68k_01f4bc:
        move.w 0xf61c:w,%d4
m68k_01f4bc_end:
.org 0x1F4C0
m68k_01f4c0:
        mulu.w #0x64,%d4
m68k_01f4c0_end:
.org 0x1F4C4
m68k_01f4c4:
        swap %d4
m68k_01f4c4_end:
.org 0x1F4C6
m68k_01f4c6:
        lea.l 0xb600:w,%a3
m68k_01f4c6_end:
.org 0x1F4CA
m68k_01f4ca:
        lsl.w #0x1,%d3
m68k_01f4ca_end:
.org 0x1F4CC
m68k_01f4cc:
        move.w (%a3, %d3.w),%d5
m68k_01f4cc_end:
.org 0x1F4D0
m68k_01f4d0:
        lsr.w #0x1,%d5
m68k_01f4d0_end:
.org 0x1F4D2
m68k_01f4d2:
        cmp.w %d5,%d4
m68k_01f4d2_end:
.org 0x1F4D4
m68k_01f4d4:
        bhi.w (. + 42)
m68k_01f4d4_end:
.org 0x1F4D8
m68k_01f4d8:
        clr.b (%a2, %d2.w)
m68k_01f4d8_end:
.org 0x1F4DC
m68k_01f4dc:
        movem.l %d0-%d1,-(%a7)
m68k_01f4dc_end:
.org 0x1F4E0
m68k_01f4e0:
        bsr.w (. + 50)
m68k_01f4e0_end:
.org 0x1F4E4
m68k_01f4e4:
        bsr.w (. + 154)
m68k_01f4e4_end:
.org 0x1F4E8
m68k_01f4e8:
        lea.l 0xff3cc2:l,%a3
m68k_01f4e8_end:
.org 0x1F4EE
m68k_01f4ee:
        move.b #0xb4,(%a3, %d2.w)
m68k_01f4ee_end:
.org 0x1F4F4
m68k_01f4f4:
        movem.l (%a7)+,%d0-%d1
m68k_01f4f4_end:
.org 0x1F4F8
m68k_01f4f8:
        bset.b #0x6,0xf766:w
m68k_01f4f8_end:
.org 0x1F4FE
m68k_01f4fe:
        ori.w #0x1,%sr
m68k_01f4fe_end:
.org 0x1F502
m68k_01f502:
        bra.w (. + 14)
m68k_01f502_end:
.org 0x1F506
m68k_01f506:
        move.w #0xffff,0xf766:w
m68k_01f506_end:
.org 0x1F50C
m68k_01f50c:
        andi.w #0xfffe,%sr
m68k_01f50c_end:
.org 0x1F510
m68k_01f510:
        rts
m68k_01f510_end:
.org 0x1F6A0
m68k_01f6a0:
        bsr.w (. + 32)
m68k_01f6a0_end:
.org 0x1F6A4
m68k_01f6a4:
        beq.b (. + 26)
m68k_01f6a4_end:
.org 0x1F6A6
m68k_01f6a6:
        addq.w #0x1,0xf362:w
m68k_01f6a6_end:
.org 0x1F6AA
m68k_01f6aa:
        move.w #0x1,0xf772:w
m68k_01f6aa_end:
.org 0x1F6B0
m68k_01f6b0:
        clr.w 0xf352:w
m68k_01f6b0_end:
.org 0x1F6B4
m68k_01f6b4:
        move.w #0xac,%d0
m68k_01f6b4_end:
.org 0x1F6B8
m68k_01f6b8:
        jsr 0x808a:l
m68k_01f6b8_end:
.org 0x1F6BE
m68k_01f6be:
        rts
m68k_01f6be_end:
.org 0x1F6C0
m68k_01f6c0:
        clr.w %d2
m68k_01f6c0_end:
.org 0x1F6C2
m68k_01f6c2:
        move.w 0xf68c:w,%d0
m68k_01f6c2_end:
.org 0x1F6C6
m68k_01f6c6:
        move.w 0xf68e:w,%d1
m68k_01f6c6_end:
.org 0x1F6CA
m68k_01f6ca:
        cmp.w 0xf67a:w,%d0
m68k_01f6ca_end:
.org 0x1F6CE
m68k_01f6ce:
        beq.w (. + 44)
m68k_01f6ce_end:
.org 0x1F6D2
m68k_01f6d2:
        cmp.w 0xf67a:w,%d1
m68k_01f6d2_end:
.org 0x1F6D6
m68k_01f6d6:
        beq.w (. + 36)
m68k_01f6d6_end:
.org 0x1F6DA
m68k_01f6da:
        cmp.w 0xf67c:w,%d0
m68k_01f6da_end:
.org 0x1F6DE
m68k_01f6de:
        beq.w (. + 12)
m68k_01f6de_end:
.org 0x1F6E2
m68k_01f6e2:
        cmp.w 0xf67c:w,%d1
m68k_01f6e2_end:
.org 0x1F6E6
m68k_01f6e6:
        bne.w (. + 24)
m68k_01f6e6_end:
.org 0x1F6EA
m68k_01f6ea:
        cmp.w 0xf67e:w,%d0
m68k_01f6ea_end:
.org 0x1F6EE
m68k_01f6ee:
        beq.w (. + 12)
m68k_01f6ee_end:
.org 0x1F6F2
m68k_01f6f2:
        cmp.w 0xf67e:w,%d1
m68k_01f6f2_end:
.org 0x1F6F6
m68k_01f6f6:
        bne.w (. + 8)
m68k_01f6f6_end:
.org 0x1F6FA
m68k_01f6fa:
        move.w 0xf602:w,%d2
m68k_01f6fa_end:
.org 0x1F6FE
m68k_01f6fe:
        cmp.w 0xf67c:w,%d0
m68k_01f6fe_end:
.org 0x1F702
m68k_01f702:
        beq.w (. + 28)
m68k_01f702_end:
.org 0x1F706
m68k_01f706:
        cmp.w 0xf67c:w,%d1
m68k_01f706_end:
.org 0x1F70A
m68k_01f70a:
        beq.w (. + 20)
m68k_01f70a_end:
.org 0x1F70E
m68k_01f70e:
        cmp.w 0xf67e:w,%d0
m68k_01f70e_end:
.org 0x1F712
m68k_01f712:
        beq.w (. + 12)
m68k_01f712_end:
.org 0x1F716
m68k_01f716:
        cmp.w 0xf67e:w,%d1
m68k_01f716_end:
.org 0x1F71A
m68k_01f71a:
        bne.w (. + 8)
m68k_01f71a_end:
.org 0x1F71E
m68k_01f71e:
        or.w 0xf604:w,%d2
m68k_01f71e_end:
.org 0x1F722
m68k_01f722:
        btst.l #0x5,%d2
m68k_01f722_end:
.org 0x1F726
m68k_01f726:
        rts
m68k_01f726_end:
.org 0x1F728
m68k_01f728:
        cmpi.w #0x10,0xf352:w
m68k_01f728_end:
.org 0x1F72E
m68k_01f72e:
        bcc.w (. + 42)
m68k_01f72e_end:
.org 0x1F732
m68k_01f732:
        move.w 0xf352:w,%d0
m68k_01f732_end:
.org 0x1F736
m68k_01f736:
        move.w #0x40,%d1
m68k_01f736_end:
.org 0x1F73A
m68k_01f73a:
        lea.l 0xfb80:w,%a0
m68k_01f73a_end:
.org 0x1F73E
m68k_01f73e:
        jsr 0xdea6:l
m68k_01f73e_end:
.org 0x1F744
m68k_01f744:
        move.w 0xf320:w,%d0
m68k_01f744_end:
.org 0x1F748
m68k_01f748:
        andi.w #0x1,%d0
m68k_01f748_end:
.org 0x1F74C
m68k_01f74c:
        bne.w (. + 52)
m68k_01f74c_end:
.org 0x1F750
m68k_01f750:
        addq.w #0x1,0xf352:w
m68k_01f750_end:
.org 0x1F754
m68k_01f754:
        bra.w (. + 44)
m68k_01f754_end:
.org 0x1F758
m68k_01f758:
        move.w #0x410,0xf38a:w
m68k_01f758_end:
.org 0x1F75E
m68k_01f75e:
        clr.w 0xf3b0:w
m68k_01f75e_end:
.org 0x1F762
m68k_01f762:
        move.w #0x7ff,%d0
m68k_01f762_end:
.org 0x1F766
m68k_01f766:
        lea.l 0xff7000:l,%a0
m68k_01f766_end:
.org 0x1F76C
m68k_01f76c:
        clr.l (%a0)+
m68k_01f76c_end:
.org 0x1F76E
m68k_01f76e:
        dbra %d0,(. + -2)
m68k_01f76e_end:
.org 0x1F772
m68k_01f772:
        bsr.w (. + 16)
m68k_01f772_end:
.org 0x1F776
m68k_01f776:
        clr.w 0xf612:w
m68k_01f776_end:
.org 0x1F77A
m68k_01f77a:
        move.w #0xc4,0xf600:w
m68k_01f77a_end:
.org 0x1F780
m68k_01f780:
        rts
m68k_01f780_end:
.org 0x1F782
m68k_01f782:
        bsr.w (. + 410)
m68k_01f782_end:
.org 0x1F786
m68k_01f786:
        jsr 254(%pc)
m68k_01f786_end:
.org 0x1F78A
m68k_01f78a:
        nop
m68k_01f78a_end:
.org 0x1F78C
m68k_01f78c:
        move.b %d0,0xffff80db:l
m68k_01f78c_end:
.org 0x1F792
m68k_01f792:
        move.w 0xf68e:w,%d0
m68k_01f792_end:
.org 0x1F796
m68k_01f796:
        move.w 0xf68c:w,%d1
m68k_01f796_end:
.org 0x1F79A
m68k_01f79a:
        move.w 0xf706:w,%d6
m68k_01f79a_end:
.org 0x1F79E
m68k_01f79e:
        move.w 0xf702:w,%d7
m68k_01f79e_end:
.org 0x1F7A2
m68k_01f7a2:
        tst.w 0xffff8124:l
m68k_01f7a2_end:
.org 0x1F7A8
m68k_01f7a8:
        beq.w (. + 8)
m68k_01f7a8_end:
.org 0x1F7AC
m68k_01f7ac:
        exg %d0,%d1
m68k_01f7ac_end:
.org 0x1F7AE
m68k_01f7ae:
        exg %d6,%d7
m68k_01f7ae_end:
.org 0x1F7B0
m68k_01f7b0:
        lea.l 0xc300:w,%a1
m68k_01f7b0_end:
.org 0x1F7B4
m68k_01f7b4:
        lea.l 0xe640:w,%a0
m68k_01f7b4_end:
.org 0x1F7B8
m68k_01f7b8:
        lsl.w #0x1,%d0
m68k_01f7b8_end:
.org 0x1F7BA
m68k_01f7ba:
        move.w (%a0, %d0.w),%d2
m68k_01f7ba_end:
.org 0x1F7BE
m68k_01f7be:
        move.w %d2,0xffff80dc:l
m68k_01f7be_end:
.org 0x1F7C4
m68k_01f7c4:
        move.b #0x64,(%a1, %d2.w)
m68k_01f7c4_end:
.org 0x1F7CA
m68k_01f7ca:
        lsl.w #0x1,%d1
m68k_01f7ca_end:
.org 0x1F7CC
m68k_01f7cc:
        move.w (%a0, %d1.w),%d2
m68k_01f7cc_end:
.org 0x1F7D0
m68k_01f7d0:
        move.w %d2,0xffff80de:l
m68k_01f7d0_end:
.org 0x1F7D6
m68k_01f7d6:
        move.b #0x64,(%a1, %d2.w)
m68k_01f7d6_end:
.org 0x1F7DC
m68k_01f7dc:
        lea.l 0xc800:w,%a0
m68k_01f7dc_end:
.org 0x1F7E0
m68k_01f7e0:
        lea.l 0xc500:w,%a1
m68k_01f7e0_end:
.org 0x1F7E4
m68k_01f7e4:
        lea.l 0xb400:w,%a2
m68k_01f7e4_end:
.org 0x1F7E8
m68k_01f7e8:
        lea.l 0xb200:w,%a3
m68k_01f7e8_end:
.org 0x1F7EC
m68k_01f7ec:
        lea.l 0xc000:w,%a4
m68k_01f7ec_end:
.org 0x1F7F0
m68k_01f7f0:
        lea.l 0xea88:w,%a5
m68k_01f7f0_end:
.org 0x1F7F4
m68k_01f7f4:
        move.w %d6,0xffff80e0:l
m68k_01f7f4_end:
.org 0x1F7FA
m68k_01f7fa:
        move.b (%a1, %d6.w),0xffff8101:l
m68k_01f7fa_end:
.org 0x1F802
m68k_01f802:
        move.w %d6,%d0
m68k_01f802_end:
.org 0x1F804
m68k_01f804:
        bsr.w (. + 208)
m68k_01f804_end:
.org 0x1F808
m68k_01f808:
        move.w %d3,0xffff8108:l
m68k_01f808_end:
.org 0x1F80E
m68k_01f80e:
        lsl.w #0x1,%d6
m68k_01f80e_end:
.org 0x1F810
m68k_01f810:
        move.w (%a2, %d6.w),0xffff8104:l
m68k_01f810_end:
.org 0x1F818
m68k_01f818:
        move.w (%a3, %d6.w),0xffff810c:l
m68k_01f818_end:
.org 0x1F820
m68k_01f820:
        move.w (%a4, %d6.w),0xffff8110:l
m68k_01f820_end:
.org 0x1F828
m68k_01f828:
        lsl.w #0x1,%d6
m68k_01f828_end:
.org 0x1F82A
m68k_01f82a:
        move.w 0x2(%a0, %d6.w),0xffff80e4:l
m68k_01f82a_end:
.org 0x1F832
m68k_01f832:
        move.w %d7,0xffff80e2:l
m68k_01f832_end:
.org 0x1F838
m68k_01f838:
        move.b (%a1, %d7.w),0xffff8103:l
m68k_01f838_end:
.org 0x1F840
m68k_01f840:
        move.w %d7,%d0
m68k_01f840_end:
.org 0x1F842
m68k_01f842:
        bsr.w (. + 146)
m68k_01f842_end:
.org 0x1F846
m68k_01f846:
        move.w %d3,0xffff810a:l
m68k_01f846_end:
.org 0x1F84C
m68k_01f84c:
        lsl.w #0x1,%d7
m68k_01f84c_end:
.org 0x1F84E
m68k_01f84e:
        move.w (%a2, %d7.w),0xffff8106:l
m68k_01f84e_end:
.org 0x1F856
m68k_01f856:
        move.w (%a3, %d7.w),0xffff810e:l
m68k_01f856_end:
.org 0x1F85E
m68k_01f85e:
        move.w (%a4, %d7.w),0xffff8112:l
m68k_01f85e_end:
.org 0x1F866
m68k_01f866:
        lsl.w #0x1,%d7
m68k_01f866_end:
.org 0x1F868
m68k_01f868:
        move.w 0x2(%a0, %d7.w),0xffff80e6:l
m68k_01f868_end:
.org 0x1F870
m68k_01f870:
        lea.l 0xa654:w,%a0
m68k_01f870_end:
.org 0x1F874
m68k_01f874:
        move.w 0xf702:w,%d0
m68k_01f874_end:
.org 0x1F878
m68k_01f878:
        clr.b (%a0, %d0.w)
m68k_01f878_end:
.org 0x1F87C
m68k_01f87c:
        move.w 0xf706:w,%d0
m68k_01f87c_end:
.org 0x1F880
m68k_01f880:
        clr.b (%a0, %d0.w)
m68k_01f880_end:
.org 0x1F884
m68k_01f884:
        rts
m68k_01f884_end:
.org 0x26BFA
m68k_026bfa:
        lea.l 0xd100:w,%a1
m68k_026bfa_end:
.org 0x26BFE
m68k_026bfe:
        adda.w 0xf31a:w,%a1
m68k_026bfe_end:
.org 0x26C02
m68k_026c02:
        move.w %d1,%d7
m68k_026c02_end:
.org 0x26C04
m68k_026c04:
        subq.w #0x1,%d7
m68k_026c04_end:
.org 0x26C06
m68k_026c06:
        move.w %d0,(%a1)+
m68k_026c06_end:
.org 0x26C08
m68k_026c08:
        move.w %d2,(%a1)+
m68k_026c08_end:
.org 0x26C0A
m68k_026c0a:
        addi.w #0x80,%d2
m68k_026c0a_end:
.org 0x26C0E
m68k_026c0e:
        move.w %d0,%d3
m68k_026c0e_end:
.org 0x26C10
m68k_026c10:
        move.w (%a0)+,%d4
m68k_026c10_end:
.org 0x26C12
m68k_026c12:
        bmi.b (. + 16)
m68k_026c12_end:
.org 0x26C14
m68k_026c14:
        swap %d0
m68k_026c14_end:
.org 0x26C16
m68k_026c16:
        or.w %d0,%d4
m68k_026c16_end:
.org 0x26C18
m68k_026c18:
        move.w %d4,(%a1)+
m68k_026c18_end:
.org 0x26C1A
m68k_026c1a:
        swap %d0
m68k_026c1a_end:
.org 0x26C1C
m68k_026c1c:
        subq.w #0x1,%d3
m68k_026c1c_end:
.org 0x26C1E
m68k_026c1e:
        bra.w (. + 24)
m68k_026c1e_end:
.org 0x26C22
m68k_026c22:
        move.w %d4,%d5
m68k_026c22_end:
.org 0x26C24
m68k_026c24:
        andi.w #0x7fff,%d4
m68k_026c24_end:
.org 0x26C28
m68k_026c28:
        lsr.w #0x7,%d4
m68k_026c28_end:
.org 0x26C2A
m68k_026c2a:
        bclr.l #0x0,%d4
m68k_026c2a_end:
.org 0x26C2E
m68k_026c2e:
        move.w 28(%pc, %d4.w),%d4
m68k_026c2e_end:
.org 0x26C32
m68k_026c32:
        jsr 36(%pc, %d4.w)
m68k_026c32_end:
.org 0x26C36
m68k_026c36:
        tst.w %d3
m68k_026c36_end:
.org 0x26C38
m68k_026c38:
        bne.b (. + -40)
m68k_026c38_end:
.org 0x26C3A
m68k_026c3a:
        dbra %d7,(. + -52)
m68k_026c3a_end:
.org 0x26C3E
m68k_026c3e:
        clr.w (%a1)
m68k_026c3e_end:
.org 0x26C40
m68k_026c40:
        addq.w #0x2,%d0
m68k_026c40_end:
.org 0x26C42
m68k_026c42:
        mulu.w %d1,%d0
m68k_026c42_end:
.org 0x26C44
m68k_026c44:
        lsl.w #0x1,%d0
m68k_026c44_end:
.org 0x26C46
m68k_026c46:
        add.w %d0,0xf31a:w
m68k_026c46_end:
.org 0x26C4A
m68k_026c4a:
        rts
m68k_026c4a_end:
.org 0x26C58
m68k_026c58:
        andi.w #0xff,%d5
m68k_026c58_end:
.org 0x26C5C
m68k_026c5c:
        swap %d0
m68k_026c5c_end:
.org 0x26C5E
m68k_026c5e:
        move.w (%a0)+,%d4
m68k_026c5e_end:
.org 0x26C60
m68k_026c60:
        or.w %d0,%d4
m68k_026c60_end:
.org 0x26C62
m68k_026c62:
        move.w %d5,%d6
m68k_026c62_end:
.org 0x26C64
m68k_026c64:
        subq.w #0x1,%d6
m68k_026c64_end:
.org 0x26C66
m68k_026c66:
        move.w %d4,(%a1)+
m68k_026c66_end:
.org 0x26C68
m68k_026c68:
        dbra %d6,(. + -2)
m68k_026c68_end:
.org 0x26C6C
m68k_026c6c:
        sub.w %d5,%d3
m68k_026c6c_end:
.org 0x26C6E
m68k_026c6e:
        swap %d0
m68k_026c6e_end:
.org 0x26C70
m68k_026c70:
        rts
m68k_026c70_end:
.org 0x26C72
m68k_026c72:
        andi.w #0xff,%d5
m68k_026c72_end:
.org 0x26C76
m68k_026c76:
        swap %d0
m68k_026c76_end:
.org 0x26C78
m68k_026c78:
        move.w (%a0)+,%d4
m68k_026c78_end:
.org 0x26C7A
m68k_026c7a:
        or.w %d0,%d4
m68k_026c7a_end:
.org 0x26C7C
m68k_026c7c:
        move.w %d5,%d6
m68k_026c7c_end:
.org 0x26C7E
m68k_026c7e:
        subq.w #0x1,%d6
m68k_026c7e_end:
.org 0x26C80
m68k_026c80:
        move.w %d4,(%a1)+
m68k_026c80_end:
.org 0x26C82
m68k_026c82:
        addq.w #0x2,%d4
m68k_026c82_end:
.org 0x26C84
m68k_026c84:
        dbra %d6,(. + -4)
m68k_026c84_end:
.org 0x26C88
m68k_026c88:
        sub.w %d5,%d3
m68k_026c88_end:
.org 0x26C8A
m68k_026c8a:
        swap %d0
m68k_026c8a_end:
.org 0x26C8C
m68k_026c8c:
        rts
m68k_026c8c_end:
.org 0x26DB4
m68k_026db4:
        move.w #0x2700,%sr
m68k_026db4_end:
.org 0x26DB8
m68k_026db8:
        move.w 0xf606:w,%d0
m68k_026db8_end:
.org 0x26DBC
m68k_026dbc:
        andi.b #0xbf,%d0
m68k_026dbc_end:
.org 0x26DC0
m68k_026dc0:
        move.w %d0,0xc00004:l
m68k_026dc0_end:
.org 0x26DC6
m68k_026dc6:
        clr.w 0xf612:w
m68k_026dc6_end:
.org 0x26DCA
m68k_026dca:
        jsr 0x68ce:l
m68k_026dca_end:
.org 0x26DD0
m68k_026dd0:
        move.w #0x8338,0xc00004:l
m68k_026dd0_end:
.org 0x26DD8
m68k_026dd8:
        move.w #0x8238,0xc00004:l
m68k_026dd8_end:
.org 0x26DE0
m68k_026de0:
        move.w #0x8407,0xc00004:l
m68k_026de0_end:
.org 0x26DE8
m68k_026de8:
        move.w #0x856c,0xc00004:l
m68k_026de8_end:
.org 0x26DF0
m68k_026df0:
        move.w #0x8d37,0xc00004:l
m68k_026df0_end:
.org 0x26DF8
m68k_026df8:
        move.w #0x9294,0xc00004:l
m68k_026df8_end:
.org 0x26E00
m68k_026e00:
        move.w #0x8b03,0xc00004:l
m68k_026e00_end:
.org 0x26E08
m68k_026e08:
        move.l #0x400000,0xff705e:l
m68k_026e08_end:
.org 0x26E12
m68k_026e12:
        move.w #0x8800,0xff7068:l
m68k_026e12_end:
.org 0x26E1A
m68k_026e1a:
        move.w #0x1,0xff7052:l
m68k_026e1a_end:
.org 0x26E22
m68k_026e22:
        move.l #0x1000000,0xff70ae:l
m68k_026e22_end:
.org 0x26E2C
m68k_026e2c:
        move.w #0xa000,0xff70b8:l
m68k_026e2c_end:
.org 0x26E34
m68k_026e34:
        move.w #0x1,0xff70a2:l
m68k_026e34_end:
.org 0x26E3C
m68k_026e3c:
        clr.w 0xff70f0:l
m68k_026e3c_end:
.org 0x26E42
m68k_026e42:
        clr.w 0xff70f6:l
m68k_026e42_end:
.org 0x26E48
m68k_026e48:
        clr.w 0xff70f8:l
m68k_026e48_end:
.org 0x26E4E
m68k_026e4e:
        moveq #0,%d4
m68k_026e4e_end:
.org 0x26E50
m68k_026e50:
        lea.l 0xea88:w,%a5
m68k_026e50_end:
.org 0x26E54
m68k_026e54:
        move.w 0xff706a:l,%d4
m68k_026e54_end:
.org 0x26E5A
m68k_026e5a:
        mulu.w #0x3,%d4
m68k_026e5a_end:
.org 0x26E5E
m68k_026e5e:
        adda.w %d4,%a5
m68k_026e5e_end:
.org 0x26E60
m68k_026e60:
        move.b (%a5)+,0xff707b:l
m68k_026e60_end:
.org 0x26E66
m68k_026e66:
        move.b (%a5)+,0xff707d:l
m68k_026e66_end:
.org 0x26E6C
m68k_026e6c:
        move.b (%a5),0xff707f:l
m68k_026e6c_end:
.org 0x26E72
m68k_026e72:
        moveq #0,%d4
m68k_026e72_end:
.org 0x26E74
m68k_026e74:
        lea.l 0xea88:w,%a5
m68k_026e74_end:
.org 0x26E78
m68k_026e78:
        move.w 0xff70ba:l,%d4
m68k_026e78_end:
.org 0x26E7E
m68k_026e7e:
        mulu.w #0x3,%d4
m68k_026e7e_end:
.org 0x26E82
m68k_026e82:
        adda.w %d4,%a5
m68k_026e82_end:
.org 0x26E84
m68k_026e84:
        move.b (%a5)+,0xff70cb:l
m68k_026e84_end:
.org 0x26E8A
m68k_026e8a:
        move.b (%a5)+,0xff70cd:l
m68k_026e8a_end:
.org 0x26E90
m68k_026e90:
        move.b (%a5),0xff70cf:l
m68k_026e90_end:
.org 0x26E96
m68k_026e96:
        move.l #0x40000000,0xc00004:l
m68k_026e96_end:
.org 0x26EA0
m68k_026ea0:
        lea.l 0x6c3b4:l,%a0
m68k_026ea0_end:
.org 0x26EA6
m68k_026ea6:
        lea.l 0xc00000:l,%a6
m68k_026ea6_end:
.org 0x26EAC
m68k_026eac:
        move.w #0x2fff,%d0
m68k_026eac_end:
.org 0x26EB0
m68k_026eb0:
        move.l (%a0)+,(%a6)
m68k_026eb0_end:
.org 0x26EB2
m68k_026eb2:
        dbra %d0,(. + -2)
m68k_026eb2_end:
.org 0x26EB6
m68k_026eb6:
        move.l #0x40000003,0xc00004:l
m68k_026eb6_end:
.org 0x26EC0
m68k_026ec0:
        lea.l 0x89ddc:l,%a0
m68k_026ec0_end:
.org 0x26EC6
m68k_026ec6:
        move.w #0x1f,%d0
m68k_026ec6_end:
.org 0x26ECA
m68k_026eca:
        move.l (%a0)+,(%a6)
m68k_026eca_end:
.org 0x26ECC
m68k_026ecc:
        dbra %d0,(. + -2)
m68k_026ecc_end:
.org 0x26ED0
m68k_026ed0:
        lea.l 0x8a426:l,%a0
m68k_026ed0_end:
.org 0x26ED6
m68k_026ed6:
        lea.l 0xd300:w,%a1
m68k_026ed6_end:
.org 0x26EDA
m68k_026eda:
        move.w #0x1,%d0
m68k_026eda_end:
.org 0x26EDE
m68k_026ede:
        move.w #0x2,%d1
m68k_026ede_end:
.org 0x26EE2
m68k_026ee2:
        move.w #0x9,%d3
m68k_026ee2_end:
.org 0x26EE6
m68k_026ee6:
        jsr 0xaf1e:l
m68k_026ee6_end:
.org 0x26EEC
m68k_026eec:
        lea.l 0xd300:w,%a0
m68k_026eec_end:
.org 0x26EF0
m68k_026ef0:
        move.w #0x4f,%d0
m68k_026ef0_end:
.org 0x26EF4
m68k_026ef4:
        move.l (%a0)+,(%a6)
m68k_026ef4_end:
.org 0x26EF6
m68k_026ef6:
        dbra %d0,(. + -2)
m68k_026ef6_end:
.org 0x26EFA
m68k_026efa:
        move.l #0x50000003,0xc00004:l
m68k_026efa_end:
.org 0x26F04
m68k_026f04:
        lea.l 0x783b4:l,%a0
m68k_026f04_end:
.org 0x26F0A
m68k_026f0a:
        move.w #0x2f,%d0
m68k_026f0a_end:
.org 0x26F0E
m68k_026f0e:
        move.l (%a0)+,(%a6)
m68k_026f0e_end:
.org 0x26F10
m68k_026f10:
        dbra %d0,(. + -2)
m68k_026f10_end:
.org 0x26F14
m68k_026f14:
        move.l #0x42000003,0xc00004:l
m68k_026f14_end:
.org 0x26F1E
m68k_026f1e:
        move.w 0xff706a:l,%d7
m68k_026f1e_end:
.org 0x26F24
m68k_026f24:
        move.w #0x1,%d0
m68k_026f24_end:
.org 0x26F28
m68k_026f28:
        move.w #0x2,%d1
m68k_026f28_end:
.org 0x26F2C
m68k_026f2c:
        bsr.w (. + 3568)
m68k_026f2c_end:
.org 0x26F30
m68k_026f30:
        move.w 0xff70ba:l,%d7
m68k_026f30_end:
.org 0x26F36
m68k_026f36:
        move.w #0x1,%d0
m68k_026f36_end:
.org 0x26F3A
m68k_026f3a:
        move.w #0x2,%d1
m68k_026f3a_end:
.org 0x26F3E
m68k_026f3e:
        bsr.w (. + 3550)
m68k_026f3e_end:
.org 0x26F42
m68k_026f42:
        lea.l 6518(%pc),%a0
m68k_026f42_end:
.org 0x26F46
m68k_026f46:
        nop
m68k_026f46_end:
.org 0x26F48
m68k_026f48:
        move.w #0x1,%d0
m68k_026f48_end:
.org 0x26F4C
m68k_026f4c:
        move.w #0x2,%d1
m68k_026f4c_end:
.org 0x26F50
m68k_026f50:
        move.w #0x1,%d3
m68k_026f50_end:
.org 0x26F54
m68k_026f54:
        bsr.w (. + 3586)
m68k_026f54_end:
.org 0x26F58
m68k_026f58:
        bsr.w (. + 3614)
m68k_026f58_end:
.org 0x26F5C
m68k_026f5c:
        lea.l 4386(%pc),%a0
m68k_026f5c_end:
.org 0x26F60
m68k_026f60:
        nop
m68k_026f60_end:
.org 0x26F62
m68k_026f62:
        lea.l 0xfb00:w,%a1
m68k_026f62_end:
.org 0x26F66
m68k_026f66:
        move.w #0x1f,%d0
m68k_026f66_end:
.org 0x26F6A
m68k_026f6a:
        move.l (%a0)+,(%a1)+
m68k_026f6a_end:
.org 0x26F6C
m68k_026f6c:
        dbra %d0,(. + -2)
m68k_026f6c_end:
.org 0x26F70
m68k_026f70:
        move.w #0x1,0xf31e:w
m68k_026f70_end:
.org 0x26F76
m68k_026f76:
        lea.l 0x78474:l,%a0
m68k_026f76_end:
.org 0x26F7C
m68k_026f7c:
        cmpi.w #0x3,0xff70f2:l
m68k_026f7c_end:
.org 0x26F84
m68k_026f84:
        bne.w (. + 10)
m68k_026f84_end:
.org 0x26F88
m68k_026f88:
        lea.l 0x78656:l,%a0
m68k_026f88_end:
.org 0x26F8E
m68k_026f8e:
        lea.l 0xff6000:l,%a1
m68k_026f8e_end:
.org 0x26F94
m68k_026f94:
        move.w #0x500,%d0
m68k_026f94_end:
.org 0x26F98
m68k_026f98:
        bsr.w (. + 4218)
m68k_026f98_end:
.org 0x26F9C
m68k_026f9c:
        move.l #0x60000003,0xc00004:l
m68k_026f9c_end:
.org 0x26FA6
m68k_026fa6:
        lea.l 0xff6000:l,%a0
m68k_026fa6_end:
.org 0x26FAC
m68k_026fac:
        move.w #0x4ff,%d0
m68k_026fac_end:
.org 0x26FB0
m68k_026fb0:
        move.w (%a0)+,(%a6)
m68k_026fb0_end:
.org 0x26FB2
m68k_026fb2:
        dbra %d0,(. + -2)
m68k_026fb2_end:
.org 0x26FB6
m68k_026fb6:
        lea.l 0x7883e:l,%a0
m68k_026fb6_end:
.org 0x26FBC
m68k_026fbc:
        lea.l 0xff6000:l,%a1
m68k_026fbc_end:
.org 0x26FC2
m68k_026fc2:
        move.w #0x500,%d0
m68k_026fc2_end:
.org 0x26FC6
m68k_026fc6:
        bsr.w (. + 4172)
m68k_026fc6_end:
.org 0x26FCA
m68k_026fca:
        move.l #0x70000003,0xc00004:l
m68k_026fca_end:
.org 0x26FD4
m68k_026fd4:
        lea.l 0xff6000:l,%a0
m68k_026fd4_end:
.org 0x26FDA
m68k_026fda:
        move.w #0x4ff,%d0
m68k_026fda_end:
.org 0x26FDE
m68k_026fde:
        move.w (%a0)+,(%a6)
m68k_026fde_end:
.org 0x26FE0
m68k_026fe0:
        dbra %d0,(. + -2)
m68k_026fe0_end:
.org 0x26FE4
m68k_026fe4:
        move.w #0x603,0xf694:w
m68k_026fe4_end:
.org 0x26FEA
m68k_026fea:
        move.w #0x604,0xf692:w
m68k_026fea_end:
.org 0x26FF0
m68k_026ff0:
        lea.l 4398(%pc),%a0
m68k_026ff0_end:
.org 0x26FF4
m68k_026ff4:
        nop
m68k_026ff4_end:
.org 0x26FF6
m68k_026ff6:
        move.l #0x60000028,%d0
m68k_026ff6_end:
.org 0x26FFC
m68k_026ffc:
        move.w #0x3,%d1
m68k_026ffc_end:
.org 0x27000
m68k_027000:
        move.w #0xea00,%d2
m68k_027000_end:
.org 0x27004
m68k_027004:
        jsr 0x26bfa:l
m68k_027004_end:
.org 0x2700A
m68k_02700a:
        jsr 0xad06:l
m68k_02700a_end:
.org 0x27010
m68k_027010:
        lea.l 4450(%pc),%a0
m68k_027010_end:
.org 0x27014
m68k_027014:
        nop
m68k_027014_end:
.org 0x27016
m68k_027016:
        move.l #0x60000028,%d0
m68k_027016_end:
.org 0x2701C
m68k_02701c:
        move.w #0x5,%d1
m68k_02701c_end:
.org 0x27020
m68k_027020:
        move.w #0xeb80,%d2
m68k_027020_end:
.org 0x27024
m68k_027024:
        jsr 0x26bfa:l
m68k_027024_end:
.org 0x2702A
m68k_02702a:
        cmpi.b #0x3,0xff700a:l
m68k_02702a_end:
.org 0x27032
m68k_027032:
        beq.w (. + 38)
m68k_027032_end:
.org 0x27036
m68k_027036:
        move.w #0xc600,0xff700c:l
m68k_027036_end:
.org 0x2703E
m68k_02703e:
        move.l #0x288be,0xff700e:l
m68k_02703e_end:
.org 0x27048
m68k_027048:
        move.w #0x1,0xff7014:l
m68k_027048_end:
.org 0x27050
m68k_027050:
        move.w #0x2,0xff7016:l
m68k_027050_end:
.org 0x27058
m68k_027058:
        jsr -724(%pc)
m68k_027058_end:
.org 0x2705C
m68k_02705c:
        move.w #0x2500,%sr
m68k_02705c_end:
.org 0x27368
m68k_027368:
        lea.l 0xff7050:l,%a0
m68k_027368_end:
.org 0x2736E
m68k_02736e:
        lea.l 0xff70a0:l,%a1
m68k_02736e_end:
.org 0x27374
m68k_027374:
        bsr.w (. + 1650)
m68k_027374_end:
.org 0x27378
m68k_027378:
        move.w %d0,0xff7050:l
m68k_027378_end:
.org 0x2737E
m68k_02737e:
        cmpi.b #0x3,0xff700a:l
m68k_02737e_end:
.org 0x27386
m68k_027386:
        bne.b (. + 12)
m68k_027386_end:
.org 0x27388
m68k_027388:
        bsr.w (. + 12050)
m68k_027388_end:
.org 0x2738C
m68k_02738c:
        move.w %d0,0xff7050:l
m68k_02738c_end:
.org 0x27392
m68k_027392:
        bsr.w (. + 6152)
m68k_027392_end:
.org 0x27396
m68k_027396:
        lea.l 0xff70a0:l,%a0
m68k_027396_end:
.org 0x2739C
m68k_02739c:
        lea.l 0xff7050:l,%a1
m68k_02739c_end:
.org 0x273A2
m68k_0273a2:
        bsr.w (. + 1646)
m68k_0273a2_end:
.org 0x273A6
m68k_0273a6:
        move.w %d0,0xff70a0:l
m68k_0273a6_end:
.org 0x273AC
m68k_0273ac:
        cmpi.b #0x3,0xff700b:l
m68k_0273ac_end:
.org 0x273B4
m68k_0273b4:
        bne.b (. + 12)
m68k_0273b4_end:
.org 0x273B6
m68k_0273b6:
        bsr.w (. + 12004)
m68k_0273b6_end:
.org 0x273BA
m68k_0273ba:
        move.w %d0,0xff70a0:l
m68k_0273ba_end:
.org 0x273C0
m68k_0273c0:
        bsr.w (. + 6106)
m68k_0273c0_end:
.org 0x28012
m68k_028012:
        movem.l %d0/%a1,-(%a7)
m68k_028012_end:
.org 0x28016
m68k_028016:
        bsr.b (. + 8)
m68k_028016_end:
.org 0x28018
m68k_028018:
        movem.l (%a7)+,%d0/%a1
m68k_028018_end:
.org 0x2801C
m68k_02801c:
        addq.w #0x1,%a1
m68k_02801c_end:
.org 0x2801E
m68k_02801e:
        tst.w %d0
m68k_02801e_end:
.org 0x28020
m68k_028020:
        bne.b (. + 4)
m68k_028020_end:
.org 0x28022
m68k_028022:
        rts
m68k_028022_end:
.org 0x28024
m68k_028024:
        clr.w %d1
m68k_028024_end:
.org 0x28026
m68k_028026:
        move.b (%a0)+,%d1
m68k_028026_end:
.org 0x28028
m68k_028028:
        bmi.b (. + 14)
m68k_028028_end:
.org 0x2802A
m68k_02802a:
        move.b (%a0)+,(%a1)
m68k_02802a_end:
.org 0x2802C
m68k_02802c:
        addq.w #0x2,%a1
m68k_02802c_end:
.org 0x2802E
m68k_02802e:
        subq.w #0x1,%d0
m68k_02802e_end:
.org 0x28030
m68k_028030:
        dbra %d1,(. + -6)
m68k_028030_end:
.org 0x28034
m68k_028034:
        bra.b (. + -22)
m68k_028034_end:
.org 0x28036
m68k_028036:
        btst.l #0x6,%d1
m68k_028036_end:
.org 0x2803A
m68k_02803a:
        bne.b (. + 20)
m68k_02803a_end:
.org 0x2803C
m68k_02803c:
        andi.w #0x3f,%d1
m68k_02803c_end:
.org 0x28040
m68k_028040:
        move.b (%a0)+,%d2
m68k_028040_end:
.org 0x28042
m68k_028042:
        move.b %d2,(%a1)
m68k_028042_end:
.org 0x28044
m68k_028044:
        addq.w #0x2,%a1
m68k_028044_end:
.org 0x28046
m68k_028046:
        subq.w #0x1,%d0
m68k_028046_end:
.org 0x28048
m68k_028048:
        dbra %d1,(. + -6)
m68k_028048_end:
.org 0x2804C
m68k_02804c:
        bra.b (. + -46)
m68k_02804c_end:
.org 0x2804E
m68k_02804e:
        btst.l #0x5,%d1
m68k_02804e_end:
.org 0x28052
m68k_028052:
        bne.b (. + 26)
m68k_028052_end:
.org 0x28054
m68k_028054:
        andi.w #0x1f,%d1
m68k_028054_end:
.org 0x28058
m68k_028058:
        move.b (%a0)+,%d2
m68k_028058_end:
.org 0x2805A
m68k_02805a:
        move.b (%a0)+,%d3
m68k_02805a_end:
.org 0x2805C
m68k_02805c:
        move.b %d2,(%a1)
m68k_02805c_end:
.org 0x2805E
m68k_02805e:
        addq.w #0x2,%a1
m68k_02805e_end:
.org 0x28060
m68k_028060:
        move.b %d3,(%a1)
m68k_028060_end:
.org 0x28062
m68k_028062:
        addq.w #0x2,%a1
m68k_028062_end:
.org 0x28064
m68k_028064:
        subq.w #0x2,%d0
m68k_028064_end:
.org 0x28066
m68k_028066:
        dbra %d1,(. + -10)
m68k_028066_end:
.org 0x2806A
m68k_02806a:
        bra.b (. + -76)
m68k_02806a_end:
.org 0x2806C
m68k_02806c:
        andi.w #0x1f,%d1
m68k_02806c_end:
.org 0x28070
m68k_028070:
        move.b (%a0)+,%d2
m68k_028070_end:
.org 0x28072
m68k_028072:
        move.b %d2,(%a1)
m68k_028072_end:
.org 0x28074
m68k_028074:
        addq.w #0x2,%a1
m68k_028074_end:
.org 0x28076
m68k_028076:
        subq.w #0x1,%d0
m68k_028076_end:
.org 0x28078
m68k_028078:
        addq.w #0x1,%d2
m68k_028078_end:
.org 0x2807A
m68k_02807a:
        dbra %d1,(. + -8)
m68k_02807a_end:
.org 0x2807E
m68k_02807e:
        bra.b (. + -96)
m68k_02807e_end:
.org 0x28B9A
m68k_028b9a:
        tst.w 0x8(%a0)
m68k_028b9a_end:
.org 0x28B9E
m68k_028b9e:
        beq.b (. + 6)
m68k_028b9e_end:
.org 0x28BA0
m68k_028ba0:
        subq.w #0x1,0x8(%a0)
m68k_028ba0_end:
.org 0x28BA4
m68k_028ba4:
        tst.w 0xa(%a0)
m68k_028ba4_end:
.org 0x28BA8
m68k_028ba8:
        beq.b (. + 6)
m68k_028ba8_end:
.org 0x28BAA
m68k_028baa:
        subq.w #0x1,0xa(%a0)
m68k_028baa_end:
.org 0x28BAE
m68k_028bae:
        tst.w 0x26(%a0)
m68k_028bae_end:
.org 0x28BB2
m68k_028bb2:
        beq.b (. + 6)
m68k_028bb2_end:
.org 0x28BB4
m68k_028bb4:
        subq.w #0x1,0x26(%a0)
m68k_028bb4_end:
.org 0x28BB8
m68k_028bb8:
        tst.w 0x28(%a0)
m68k_028bb8_end:
.org 0x28BBC
m68k_028bbc:
        beq.b (. + 6)
m68k_028bbc_end:
.org 0x28BBE
m68k_028bbe:
        subq.w #0x1,0x28(%a0)
m68k_028bbe_end:
.org 0x28BC2
m68k_028bc2:
        move.w 0x28(%a0),%d1
m68k_028bc2_end:
.org 0x28BC6
m68k_028bc6:
        beq.b (. + 46)
m68k_028bc6_end:
.org 0x28BC8
m68k_028bc8:
        lea.l -2890(%pc),%a2
m68k_028bc8_end:
.org 0x28BCC
m68k_028bcc:
        lea.l 0xfb00:w,%a3
m68k_028bcc_end:
.org 0x28BD0
m68k_028bd0:
        cmpa.l #0xff7050,%a0
m68k_028bd0_end:
.org 0x28BD6
m68k_028bd6:
        beq.b (. + 10)
m68k_028bd6_end:
.org 0x28BD8
m68k_028bd8:
        lea.l -2874(%pc),%a2
m68k_028bd8_end:
.org 0x28BDC
m68k_028bdc:
        lea.l 0xfb20:w,%a3
m68k_028bdc_end:
.org 0x28BE0
m68k_028be0:
        move.w #0x7,%d7
m68k_028be0_end:
.org 0x28BE4
m68k_028be4:
        andi.w #0x1,%d1
m68k_028be4_end:
.org 0x28BE8
m68k_028be8:
        bne.b (. + 6)
m68k_028be8_end:
.org 0x28BEA
m68k_028bea:
        lea.l -2780(%pc),%a2
m68k_028bea_end:
.org 0x28BEE
m68k_028bee:
        move.w (%a2)+,(%a3)+
m68k_028bee_end:
.org 0x28BF0
m68k_028bf0:
        dbra %d7,(. + -2)
m68k_028bf0_end:
.org 0x28BF4
m68k_028bf4:
        move.w (%a0),%d0
m68k_028bf4_end:
.org 0x28BF6
m68k_028bf6:
        tst.w 0x2(%a0)
m68k_028bf6_end:
.org 0x28BFA
m68k_028bfa:
        bmi.b (. + 78)
m68k_028bfa_end:
.org 0x28BFC
m68k_028bfc:
        clr.w %d1
m68k_028bfc_end:
.org 0x28BFE
m68k_028bfe:
        btst.l #0x8,%d0
m68k_028bfe_end:
.org 0x28C02
m68k_028c02:
        bne.b (. + 12)
m68k_028c02_end:
.org 0x28C04
m68k_028c04:
        addq.w #0x1,%d1
m68k_028c04_end:
.org 0x28C06
m68k_028c06:
        btst.l #0x9,%d0
m68k_028c06_end:
.org 0x28C0A
m68k_028c0a:
        beq.b (. + 4)
m68k_028c0a_end:
.org 0x28C0C
m68k_028c0c:
        addq.w #0x1,%d1
m68k_028c0c_end:
.org 0x28C0E
m68k_028c0e:
        move.b %d1,0x3(%a0)
m68k_028c0e_end:
.org 0x28C12
m68k_028c12:
        btst.l #0x4,%d0
m68k_028c12_end:
.org 0x28C16
m68k_028c16:
        beq.b (. + 26)
m68k_028c16_end:
.org 0x28C18
m68k_028c18:
        bset.b #0x7,0x2(%a0)
m68k_028c18_end:
.org 0x28C1E
m68k_028c1e:
        bclr.b #0x6,0x2(%a0)
m68k_028c1e_end:
.org 0x28C24
m68k_028c24:
        clr.w 0x4(%a0)
m68k_028c24_end:
.org 0x28C28
m68k_028c28:
        move.w 0x16(%a0),0x8(%a0)
m68k_028c28_end:
.org 0x28C2E
m68k_028c2e:
        bra.b (. + 26)
m68k_028c2e_end:
.org 0x28C30
m68k_028c30:
        andi.w #0x3fff,0x2(%a0)
m68k_028c30_end:
.org 0x28C36
m68k_028c36:
        btst.l #0xd,%d0
m68k_028c36_end:
.org 0x28C3A
m68k_028c3a:
        beq.w (. + 340)
m68k_028c3a_end:
.org 0x28C3E
m68k_028c3e:
        bset.b #0x6,0x2(%a0)
m68k_028c3e_end:
.org 0x28C44
m68k_028c44:
        bra.w (. + 330)
m68k_028c44_end:
.org 0x28C48
m68k_028c48:
        move.w 0x4(%a0),%d0
m68k_028c48_end:
.org 0x28C4C
m68k_028c4c:
        tst.w 0x8(%a0)
m68k_028c4c_end:
.org 0x28C50
m68k_028c50:
        bne.w (. + 318)
m68k_028c50_end:
.org 0x28C54
m68k_028c54:
        cmpi.w #0x4,%d0
m68k_028c54_end:
.org 0x28C58
m68k_028c58:
        bne.w (. + 284)
m68k_028c58_end:
.org 0x28C5C
m68k_028c5c:
        bsr.w (. + 5586)
m68k_028c5c_end:
.org 0x28C60
m68k_028c60:
        bcc.w (. + 276)
m68k_028c60_end:
.org 0x28C64
m68k_028c64:
        btst.b #0x6,0x2(%a1)
m68k_028c64_end:
.org 0x28C6A
m68k_028c6a:
        beq.b (. + 44)
m68k_028c6a_end:
.org 0x28C6C
m68k_028c6c:
        move.w 0x2(%a0),%d1
m68k_028c6c_end:
.org 0x28C70
m68k_028c70:
        move.w 0x2(%a1),%d2
m68k_028c70_end:
.org 0x28C74
m68k_028c74:
        andi.w #0x3,%d1
m68k_028c74_end:
.org 0x28C78
m68k_028c78:
        andi.w #0x3,%d2
m68k_028c78_end:
.org 0x28C7C
m68k_028c7c:
        cmp.w %d1,%d2
m68k_028c7c_end:
.org 0x28C7E
m68k_028c7e:
        bne.b (. + 24)
m68k_028c7e_end:
.org 0x28C80
m68k_028c80:
        movem.w %d0-%d1,-(%a7)
m68k_028c80_end:
.org 0x28C84
m68k_028c84:
        move.w #0xa0,%d0
m68k_028c84_end:
.org 0x28C88
m68k_028c88:
        jsr 0x808a:l
m68k_028c88_end:
.org 0x28C8E
m68k_028c8e:
        movem.w (%a7)+,%d0-%d1
m68k_028c8e_end:
.org 0x28C92
m68k_028c92:
        bra.w (. + 226)
m68k_028c92_end:
.org 0x28C96
m68k_028c96:
        movem.w %d0-%d1,-(%a7)
m68k_028c96_end:
.org 0x28C9A
m68k_028c9a:
        move.w #0xa7,%d0
m68k_028c9a_end:
.org 0x28C9E
m68k_028c9e:
        jsr 0x808a:l
m68k_028c9e_end:
.org 0x28CA4
m68k_028ca4:
        move.w #0x3c,0x26(%a1)
m68k_028ca4_end:
.org 0x28CAA
m68k_028caa:
        jsr 0x83d4:l
m68k_028caa_end:
.org 0x28CB0
m68k_028cb0:
        andi.w #0x7,%d0
m68k_028cb0_end:
.org 0x28CB4
m68k_028cb4:
        cmpi.w #0x6,%d0
m68k_028cb4_end:
.org 0x28CB8
m68k_028cb8:
        bcs.b (. + 4)
m68k_028cb8_end:
.org 0x28CBA
m68k_028cba:
        subq.w #0x4,%d0
m68k_028cba_end:
.org 0x28CBC
m68k_028cbc:
        move.w %d0,%d7
m68k_028cbc_end:
.org 0x28CBE
m68k_028cbe:
        move.w 0x1e(%a0),%d0
m68k_028cbe_end:
.org 0x28CC2
m68k_028cc2:
        lea.l 110(%pc),%a2
m68k_028cc2_end:
.org 0x28CC6
m68k_028cc6:
        bsr.w (. + 714)
m68k_028cc6_end:
.org 0x28CCA
m68k_028cca:
        add.w 114(%pc, %d1.w),%d7
m68k_028cca_end:
.org 0x28CCE
m68k_028cce:
        move.w 0x1e(%a0),%d0
m68k_028cce_end:
.org 0x28CD2
m68k_028cd2:
        move.w 0xc(%a0),%d1
m68k_028cd2_end:
.org 0x28CD6
m68k_028cd6:
        tst.w %d1
m68k_028cd6_end:
.org 0x28CD8
m68k_028cd8:
        bne.w (. + 18)
m68k_028cd8_end:
.org 0x28CDC
m68k_028cdc:
        move.w 0x2c(%a0),%d2
m68k_028cdc_end:
.org 0x28CE0
m68k_028ce0:
        asl.w #0x1,%d2
m68k_028ce0_end:
.org 0x28CE2
m68k_028ce2:
        add.w 102(%pc, %d2.w),%d0
m68k_028ce2_end:
.org 0x28CE6
m68k_028ce6:
        bra.w (. + 36)
m68k_028ce6_end:
.org 0x28CEA
m68k_028cea:
        cmpi.w #0x1,%d1
m68k_028cea_end:
.org 0x28CEE
m68k_028cee:
        bhi.w (. + 18)
m68k_028cee_end:
.org 0x28CF2
m68k_028cf2:
        move.w 0x2a(%a0),%d2
m68k_028cf2_end:
.org 0x28CF6
m68k_028cf6:
        asl.w #0x1,%d2
m68k_028cf6_end:
.org 0x28CF8
m68k_028cf8:
        add.w 88(%pc, %d2.w),%d0
m68k_028cf8_end:
.org 0x28CFC
m68k_028cfc:
        bra.w (. + 14)
m68k_028cfc_end:
.org 0x28D00
m68k_028d00:
        move.w 0x2e(%a0),%d2
m68k_028d00_end:
.org 0x28D04
m68k_028d04:
        asl.w #0x1,%d2
m68k_028d04_end:
.org 0x28D06
m68k_028d06:
        add.w 82(%pc, %d2.w),%d0
m68k_028d06_end:
.org 0x28D0A
m68k_028d0a:
        mulu.w %d0,%d7
m68k_028d0a_end:
.org 0x28D0C
m68k_028d0c:
        move.w 0x2(%a0),%d2
m68k_028d0c_end:
.org 0x28D10
m68k_028d10:
        andi.w #0x3,%d2
m68k_028d10_end:
.org 0x28D14
m68k_028d14:
        asl.w #0x1,%d2
m68k_028d14_end:
.org 0x28D16
m68k_028d16:
        divu.w 86(%pc, %d2.w),%d7
m68k_028d16_end:
.org 0x28D1A
m68k_028d1a:
        movem.w (%a7)+,%d0-%d1
m68k_028d1a_end:
.org 0x28D1E
m68k_028d1e:
        tst.w 0x1c(%a0)
m68k_028d1e_end:
.org 0x28D22
m68k_028d22:
        beq.w (. + 82)
m68k_028d22_end:
.org 0x28D26
m68k_028d26:
        sub.w %d7,0x1c(%a1)
m68k_028d26_end:
.org 0x28D2A
m68k_028d2a:
        bpl.b (. + 74)
m68k_028d2a_end:
.org 0x28D2C
m68k_028d2c:
        clr.w 0x1c(%a1)
m68k_028d2c_end:
.org 0x28D30
m68k_028d30:
        bra.b (. + 68)
m68k_028d30_end:
.org 0x28D74
m68k_028d74:
        move.w #0x4,0x8(%a0)
m68k_028d74_end:
.org 0x28F90
m68k_028f90:
        move.w #0xfffe,%d1
m68k_028f90_end:
.org 0x28F94
m68k_028f94:
        addq.w #0x2,%d1
m68k_028f94_end:
.org 0x28F96
m68k_028f96:
        cmp.w (%a2)+,%d0
m68k_028f96_end:
.org 0x28F98
m68k_028f98:
        bcc.b (. + -4)
m68k_028f98_end:
.org 0x28F9A
m68k_028f9a:
        rts
m68k_028f9a_end:
.org 0x3096E
m68k_03096e:
        bsr.w (. + 1464)
m68k_03096e_end:
.org 0x30972
m68k_030972:
        move.w 0xf376:w,%d0
m68k_030972_end:
.org 0x30976
m68k_030976:
        bmi.w (. + 44)
m68k_030976_end:
.org 0x3097A
m68k_03097a:
        cmp.w 0xf67a:w,%d0
m68k_03097a_end:
.org 0x3097E
m68k_03097e:
        beq.w (. + 44)
m68k_03097e_end:
.org 0x30982
m68k_030982:
        cmp.w 0xf67c:w,%d0
m68k_030982_end:
.org 0x30986
m68k_030986:
        beq.w (. + 36)
m68k_030986_end:
.org 0x3098A
m68k_03098a:
        cmp.w 0xf67e:w,%d0
m68k_03098a_end:
.org 0x3098E
m68k_03098e:
        beq.w (. + 28)
m68k_03098e_end:
.org 0x30992
m68k_030992:
        move.w #0x2,0xf362:w
m68k_030992_end:
.org 0x30998
m68k_030998:
        bsr.w (. + 220)
m68k_030998_end:
.org 0x3099C
m68k_03099c:
        bsr.w (. + 1550)
m68k_03099c_end:
.org 0x309A0
m68k_0309a0:
        bra.b (. + -50)
m68k_0309a0_end:
.org 0x309A2
m68k_0309a2:
        bsr.w (. + 2116)
m68k_0309a2_end:
.org 0x309A6
m68k_0309a6:
        bra.w (. + 50)
m68k_0309a6_end:
.org 0x309D8
m68k_0309d8:
        jsr 0xaf48:l
m68k_0309d8_end:
.org 0x309DE
m68k_0309de:
        rts
m68k_0309de_end:
.org 0x30A74
m68k_030a74:
        move.w 0xf612:w,-(%a7)
m68k_030a74_end:
.org 0x30A78
m68k_030a78:
        move.w 0xf362:w,-(%a7)
m68k_030a78_end:
.org 0x30A7C
m68k_030a7c:
        move.w #0x20b,0xf612:w
m68k_030a7c_end:
.org 0x30A82
m68k_030a82:
        clr.w 0xf600:w
m68k_030a82_end:
.org 0x30A86
m68k_030a86:
        jsr 0xaf48:l
m68k_030a86_end:
.org 0x30A8C
m68k_030a8c:
        move.w #0x2500,%sr
m68k_030a8c_end:
.org 0x30A90
m68k_030a90:
        tst.w 0xf600:w
m68k_030a90_end:
.org 0x30A94
m68k_030a94:
        beq.b (. + -4)
m68k_030a94_end:
.org 0x30A96
m68k_030a96:
        cmpi.w #0x28,0xf600:w
m68k_030a96_end:
.org 0x30A9C
m68k_030a9c:
        bne.w (. + 20)
m68k_030a9c_end:
.org 0x30AA0
m68k_030aa0:
        jsr 0x60c:l
m68k_030aa0_end:
.org 0x30AA6
m68k_030aa6:
        clr.w 0xf600:w
m68k_030aa6_end:
.org 0x30AAA
m68k_030aaa:
        move.w #0x2500,%sr
m68k_030aaa_end:
.org 0x30AAE
m68k_030aae:
        bra.b (. + -30)
m68k_030aae_end:
.org 0x30AB0
m68k_030ab0:
        move.w #0x2700,%sr
m68k_030ab0_end:
.org 0x30AB4
m68k_030ab4:
        move.w (%a7)+,0xf362:w
m68k_030ab4_end:
.org 0x30AB8
m68k_030ab8:
        move.w (%a7)+,0xf612:w
m68k_030ab8_end:
.org 0x30ABC
m68k_030abc:
        rts
m68k_030abc_end:
.org 0x30F26
m68k_030f26:
        move.w 0xf724:w,%d0
m68k_030f26_end:
.org 0x30F2A
m68k_030f2a:
        lea.l 0xf714:w,%a0
m68k_030f2a_end:
.org 0x30F2E
m68k_030f2e:
        lea.l 0xe640:w,%a1
m68k_030f2e_end:
.org 0x30F32
m68k_030f32:
        move.b (%a0, %d0.w),%d1
m68k_030f32_end:
.org 0x30F36
m68k_030f36:
        ext.w %d1
m68k_030f36_end:
.org 0x30F38
m68k_030f38:
        bmi.b (. + 14)
m68k_030f38_end:
.org 0x30F3A
m68k_030f3a:
        addq.w #0x1,%d0
m68k_030f3a_end:
.org 0x30F3C
m68k_030f3c:
        lsl.w #0x1,%d1
m68k_030f3c_end:
.org 0x30F3E
m68k_030f3e:
        tst.w (%a1, %d1.w)
m68k_030f3e_end:
.org 0x30F42
m68k_030f42:
        bmi.b (. + -16)
m68k_030f42_end:
.org 0x30F44
m68k_030f44:
        lsr.w #0x1,%d1
m68k_030f44_end:
.org 0x30F46
m68k_030f46:
        move.w %d0,0xf724:w
m68k_030f46_end:
.org 0x30F4A
m68k_030f4a:
        move.w %d1,0xf376:w
m68k_030f4a_end:
.org 0x30F4E
m68k_030f4e:
        clr.w 0xf364:w
m68k_030f4e_end:
.org 0x30F52
m68k_030f52:
        rts
m68k_030f52_end:
.org 0x30FAA
m68k_030faa:
        bsr.w (. + 358)
m68k_030faa_end:
.org 0x30FAE
m68k_030fae:
        bsr.w (. + 198)
m68k_030fae_end:
.org 0x30FB2
m68k_030fb2:
        tst.w 0xf364:w
m68k_030fb2_end:
.org 0x30FB6
m68k_030fb6:
        bmi.w (. + 34)
m68k_030fb6_end:
.org 0x30FBA
m68k_030fba:
        bsr.w (. + 450)
m68k_030fba_end:
.org 0x30FBE
m68k_030fbe:
        bsr.w (. + 488)
m68k_030fbe_end:
.org 0x30FC2
m68k_030fc2:
        move.w #0x1,0xf728:w
m68k_030fc2_end:
.org 0x30FC8
m68k_030fc8:
        move.w 0xf726:w,%d0
m68k_030fc8_end:
.org 0x30FCC
m68k_030fcc:
        lsl.w #0x1,%d0
m68k_030fcc_end:
.org 0x30FCE
m68k_030fce:
        move.w 54(%pc, %d0.w),%d0
m68k_030fce_end:
.org 0x30FD2
m68k_030fd2:
        jsr 56(%pc, %d0.w)
m68k_030fd2_end:
.org 0x30FD6
m68k_030fd6:
        bra.b (. + -40)
m68k_030fd6_end:
.org 0x30FD8
m68k_030fd8:
        jsr 0xe82e:l
m68k_030fd8_end:
.org 0x30FDE
m68k_030fde:
        bsr.w (. + 12)
m68k_030fde_end:
.org 0x30FE2
m68k_030fe2:
        jsr 0x662e4:l
m68k_030fe2_end:
.org 0x30FE8
m68k_030fe8:
        rts
m68k_030fe8_end:
.org 0x30FEA
m68k_030fea:
        lea.l 0xcd00:w,%a0
m68k_030fea_end:
.org 0x30FEE
m68k_030fee:
        move.w #0xff,%d0
m68k_030fee_end:
.org 0x30FF2
m68k_030ff2:
        move.b (%a0)+,%d1
m68k_030ff2_end:
.org 0x30FF4
m68k_030ff4:
        cmpi.b #0x2,%d1
m68k_030ff4_end:
.org 0x30FF8
m68k_030ff8:
        bcc.w (. + 8)
m68k_030ff8_end:
.org 0x30FFC
m68k_030ffc:
        clr.b -0x1(%a0)
m68k_030ffc_end:
.org 0x31000
m68k_031000:
        dbra %d0,(. + -14)
m68k_031000_end:
.org 0x31004
m68k_031004:
        rts
m68k_031004_end:
.org 0x3100C
m68k_03100c:
        jsr 0x31a0c:l
m68k_03100c_end:
.org 0x31012
m68k_031012:
        rts
m68k_031012_end:
.org 0x3101C
m68k_03101c:
        jsr 0x33040:l
m68k_03101c_end:
.org 0x31022
m68k_031022:
        rts
m68k_031022_end:
.org 0x31074
m68k_031074:
        lea.l 0xf427:w,%a0
m68k_031074_end:
.org 0x31078
m68k_031078:
        lea.l 0xea37:w,%a1
m68k_031078_end:
.org 0x3107C
m68k_03107c:
        move.w 0xf364:w,%d0
m68k_03107c_end:
.org 0x31080
m68k_031080:
        addq.w #0x1,%d0
m68k_031080_end:
.org 0x31082
m68k_031082:
        move.w 0xf376:w,%d2
m68k_031082_end:
.org 0x31086
m68k_031086:
        cmpi.w #0x28,%d0
m68k_031086_end:
.org 0x3108A
m68k_03108a:
        bhi.w (. + 26)
m68k_03108a_end:
.org 0x3108E
m68k_03108e:
        tst.b (%a1, %d0.w)
m68k_03108e_end:
.org 0x31092
m68k_031092:
        bne.w (. + 14)
m68k_031092_end:
.org 0x31096
m68k_031096:
        move.b (%a0, %d0.w),%d1
m68k_031096_end:
.org 0x3109A
m68k_03109a:
        cmp.b %d2,%d1
m68k_03109a_end:
.org 0x3109C
m68k_03109c:
        beq.w (. + 12)
m68k_03109c_end:
.org 0x310A0
m68k_0310a0:
        addq.w #0x1,%d0
m68k_0310a0_end:
.org 0x310A2
m68k_0310a2:
        bra.b (. + -28)
m68k_0310a2_end:
.org 0x310A4
m68k_0310a4:
        move.w #0xffff,%d0
m68k_0310a4_end:
.org 0x310A8
m68k_0310a8:
        move.w %d0,0xf364:w
m68k_0310a8_end:
.org 0x310AC
m68k_0310ac:
        rts
m68k_0310ac_end:
.org 0x31110
m68k_031110:
        jsr 0x83d4:l
m68k_031110_end:
.org 0x31116
m68k_031116:
        lea.l 228(%pc),%a0
m68k_031116_end:
.org 0x3111A
m68k_03111a:
        nop
m68k_03111a_end:
.org 0x3111C
m68k_03111c:
        move.w 0xefd2:w,%d0
m68k_03111c_end:
.org 0x31120
m68k_031120:
        lsl.w #0x6,%d0
m68k_031120_end:
.org 0x31122
m68k_031122:
        adda.w %d0,%a0
m68k_031122_end:
.org 0x31124
m68k_031124:
        move.w 0xf376:w,%d0
m68k_031124_end:
.org 0x31128
m68k_031128:
        lsl.w #0x2,%d0
m68k_031128_end:
.org 0x3112A
m68k_03112a:
        moveq #0,%d1
m68k_03112a_end:
.org 0x3112C
m68k_03112c:
        move.w 0xf61c:w,%d1
m68k_03112c_end:
.org 0x31130
m68k_031130:
        lsl.l #0x4,%d1
m68k_031130_end:
.org 0x31132
m68k_031132:
        swap %d1
m68k_031132_end:
.org 0x31134
m68k_031134:
        clr.w %d2
m68k_031134_end:
.org 0x31136
m68k_031136:
        cmp.w (%a0, %d0.w),%d1
m68k_031136_end:
.org 0x3113A
m68k_03113a:
        bcs.w (. + 16)
m68k_03113a_end:
.org 0x3113E
m68k_03113e:
        addq.w #0x4,%d2
m68k_03113e_end:
.org 0x31140
m68k_031140:
        cmp.w 0x2(%a0, %d0.w),%d1
m68k_031140_end:
.org 0x31144
m68k_031144:
        bcs.w (. + 6)
m68k_031144_end:
.org 0x3114A
m68k_03114a:
        jsr 0x83d4:l
m68k_03114a_end:
.org 0x31150
m68k_031150:
        lea.l 362(%pc),%a2
m68k_031150_end:
.org 0x31154
m68k_031154:
        nop
m68k_031154_end:
.org 0x31156
m68k_031156:
        andi.l #0xffff,%d0
m68k_031156_end:
.org 0x3115C
m68k_03115c:
        lsl.l #0x3,%d0
m68k_03115c_end:
.org 0x3115E
m68k_03115e:
        swap %d0
m68k_03115e_end:
.org 0x31160
m68k_031160:
        clr.w %d1
m68k_031160_end:
.org 0x31162
m68k_031162:
        cmp.w (%a2, %d2.w),%d0
m68k_031162_end:
.org 0x31166
m68k_031166:
        bcs.w (. + 16)
m68k_031166_end:
.org 0x3116A
m68k_03116a:
        addq.w #0x1,%d1
m68k_03116a_end:
.org 0x3116C
m68k_03116c:
        cmp.w 0x2(%a2, %d2.w),%d0
m68k_03116c_end:
.org 0x31170
m68k_031170:
        bcs.w (. + 6)
m68k_031170_end:
.org 0x31174
m68k_031174:
        addq.w #0x1,%d1
m68k_031174_end:
.org 0x31176
m68k_031176:
        move.w %d1,0xf726:w
m68k_031176_end:
.org 0x3117A
m68k_03117a:
        rts
m68k_03117a_end:
.org 0x3117C
m68k_03117c:
        lea.l 0xe80c:w,%a0
m68k_03117c_end:
.org 0x31180
m68k_031180:
        move.w 0xf364:w,%d0
m68k_031180_end:
.org 0x31184
m68k_031184:
        lsl.w #0x1,%d0
m68k_031184_end:
.org 0x31186
m68k_031186:
        add.w 0xf364:w,%d0
m68k_031186_end:
.org 0x3118A
m68k_03118a:
        lsl.w #0x2,%d0
m68k_03118a_end:
.org 0x3118C
m68k_03118c:
        move.l #0xffffffff,(%a0, %d0.w)
m68k_03118c_end:
.org 0x31194
m68k_031194:
        move.l #0xffffffff,0x4(%a0, %d0.w)
m68k_031194_end:
.org 0x3119C
m68k_03119c:
        move.l #0xffffffff,0x8(%a0, %d0.w)
m68k_03119c_end:
.org 0x311A4
m68k_0311a4:
        rts
m68k_0311a4_end:
.org 0x311A6
m68k_0311a6:
        lea.l 0xf72a:w,%a0
m68k_0311a6_end:
.org 0x311AA
m68k_0311aa:
        lea.l 0xcc00:w,%a1
m68k_0311aa_end:
.org 0x311AE
m68k_0311ae:
        lea.l 0xcd00:w,%a2
m68k_0311ae_end:
.org 0x311B2
m68k_0311b2:
        move.w 0xf364:w,%d0
m68k_0311b2_end:
.org 0x311B6
m68k_0311b6:
        clr.w %d4
m68k_0311b6_end:
.org 0x311B8
m68k_0311b8:
        move.w #0xff,%d1
m68k_0311b8_end:
.org 0x311BC
m68k_0311bc:
        move.b (%a1, %d1.w),%d2
m68k_0311bc_end:
.org 0x311C0
m68k_0311c0:
        cmp.w %d0,%d2
m68k_0311c0_end:
.org 0x311C2
m68k_0311c2:
        bne.w (. + 22)
m68k_0311c2_end:
.org 0x311C6
m68k_0311c6:
        move.w %d1,%d3
m68k_0311c6_end:
.org 0x311C8
m68k_0311c8:
        tst.b (%a2, %d3.w)
m68k_0311c8_end:
.org 0x311CC
m68k_0311cc:
        beq.w (. + 8)
m68k_0311cc_end:
.org 0x311D0
m68k_0311d0:
        bset.l #0xe,%d3
m68k_0311d0_end:
.org 0x311D4
m68k_0311d4:
        move.w %d3,(%a0)+
m68k_0311d4_end:
.org 0x311D6
m68k_0311d6:
        addq.w #0x1,%d4
m68k_0311d6_end:
.org 0x311D8
m68k_0311d8:
        dbra %d1,(. + -28)
m68k_0311d8_end:
.org 0x311DC
m68k_0311dc:
        move.w #0xffff,(%a0)
m68k_0311dc_end:
.org 0x311E0
m68k_0311e0:
        move.w %d4,0xf762:w
m68k_0311e0_end:
.org 0x311E4
m68k_0311e4:
        rts
m68k_0311e4_end:
.org 0x311E6
m68k_0311e6:
        jsr 0xe8a0:l
m68k_0311e6_end:
.org 0x311EC
m68k_0311ec:
        jsr 0x1190e:l
m68k_0311ec_end:
.org 0x311F2
m68k_0311f2:
        move.w #0x1,0xf36c:w
m68k_0311f2_end:
.org 0x311F8
m68k_0311f8:
        rts
m68k_0311f8_end:
.org 0x312C8
m68k_0312c8:
        move.w 0xf362:w,%d0
m68k_0312c8_end:
.org 0x312CC
m68k_0312cc:
        lsl.w #0x1,%d0
m68k_0312cc_end:
.org 0x312CE
m68k_0312ce:
        move.w 8(%pc, %d0.w),%d0
m68k_0312ce_end:
.org 0x312D2
m68k_0312d2:
        jsr 36(%pc, %d0.w)
m68k_0312d2_end:
.org 0x312D6
m68k_0312d6:
        rts
m68k_0312d6_end:
.org 0x31328
m68k_031328:
        addq.w #0x1,0xf362:w
m68k_031328_end:
.org 0x3132C
m68k_03132c:
        move.w #0x9e,%d0
m68k_03132c_end:
.org 0x31330
m68k_031330:
        jsr 0x676f2:l
m68k_031330_end:
.org 0x31336
m68k_031336:
        rts
m68k_031336_end:
.org 0x31338
m68k_031338:
        move.w #0xb0,0xf600:w
m68k_031338_end:
.org 0x3133E
m68k_03133e:
        rts
m68k_03133e_end:
.org 0x317DC
m68k_0317dc:
        move.b 0xf602:w,%d0
m68k_0317dc_end:
.org 0x317E0
m68k_0317e0:
        andi.w #0x3,%d0
m68k_0317e0_end:
.org 0x317E4
m68k_0317e4:
        beq.w (. + 28)
m68k_0317e4_end:
.org 0x31800
m68k_031800:
        move.w #0x1,0xf608:w
m68k_031800_end:
.org 0x31806
m68k_031806:
        rts
m68k_031806_end:
.org 0x31808
m68k_031808:
        btst.b #0x5,0xf603:w
m68k_031808_end:
.org 0x3180E
m68k_03180e:
        bne.w (. + 58)
m68k_03180e_end:
.org 0x31812
m68k_031812:
        move.b 0xf602:w,%d0
m68k_031812_end:
.org 0x31816
m68k_031816:
        andi.w #0x3,%d0
m68k_031816_end:
.org 0x3181A
m68k_03181a:
        bne.w (. + 14)
m68k_03181a_end:
.org 0x3181E
m68k_03181e:
        btst.b #0x3,0xf321:w
m68k_03181e_end:
.org 0x31824
m68k_031824:
        bne.w (. + 36)
m68k_031824_end:
.org 0x31828
m68k_031828:
        lea.l 32(%pc),%a0
m68k_031828_end:
.org 0x3182C
m68k_03182c:
        move.w 0xf386:w,%d0
m68k_03182c_end:
.org 0x31830
m68k_031830:
        lsl.w #0x1,%d0
m68k_031830_end:
.org 0x31832
m68k_031832:
        add.w 0xf386:w,%d0
m68k_031832_end:
.org 0x31836
m68k_031836:
        lsl.w #0x3,%d0
m68k_031836_end:
.org 0x31838
m68k_031838:
        addi.w #0x40,%d0
m68k_031838_end:
.org 0x3183C
m68k_03183c:
        move.w #0x80,%d1
m68k_03183c_end:
.org 0x31840
m68k_031840:
        clr.w %d2
m68k_031840_end:
.org 0x31842
m68k_031842:
        jsr 0xac08:l
m68k_031842_end:
.org 0x31848
m68k_031848:
        rts
m68k_031848_end:
.org 0x3191E
m68k_03191e:
        lea.l 24(%pc),%a0
m68k_03191e_end:
.org 0x31922
m68k_031922:
        move.l #0xc0000008,%d0
m68k_031922_end:
.org 0x31928
m68k_031928:
        move.w #0x7,%d1
m68k_031928_end:
.org 0x3192C
m68k_03192c:
        move.w #0xc420,%d2
m68k_03192c_end:
.org 0x31930
m68k_031930:
        jsr 0x26bfa:l
m68k_031930_end:
.org 0x31936
m68k_031936:
        rts
m68k_031936_end:
.org 0x31954
m68k_031954:
        addq.w #0x1,0xf362:w
m68k_031954_end:
.org 0x31958
m68k_031958:
        move.w #0xa9,%d0
m68k_031958_end:
.org 0x3195C
m68k_03195c:
        jsr 0x676f2:l
m68k_03195c_end:
.org 0x31962
m68k_031962:
        rts
m68k_031962_end:
.org 0x31964
m68k_031964:
        lea.l -588(%pc),%a0
m68k_031964_end:
.org 0x31968
m68k_031968:
        move.l #0xc0000008,%d0
m68k_031968_end:
.org 0x3196E
m68k_03196e:
        move.w #0x7,%d1
m68k_03196e_end:
.org 0x31972
m68k_031972:
        move.w #0xc420,%d2
m68k_031972_end:
.org 0x31976
m68k_031976:
        jsr 0x26bfa:l
m68k_031976_end:
.org 0x3197C
m68k_03197c:
        clr.w 0xf386:w
m68k_03197c_end:
.org 0x31980
m68k_031980:
        addq.w #0x1,0xf362:w
m68k_031980_end:
.org 0x31984
m68k_031984:
        move.w #0x8,0xcfd2:w
m68k_031984_end:
.org 0x3198A
m68k_03198a:
        rts
m68k_03198a_end:
.org 0x3198C
m68k_03198c:
        bsr.w (. + -432)
m68k_03198c_end:
.org 0x31990
m68k_031990:
        bsr.w (. + -392)
m68k_031990_end:
.org 0x31994
m68k_031994:
        tst.w 0xcfd2:w
m68k_031994_end:
.org 0x31998
m68k_031998:
        beq.w (. + 28)
m68k_031998_end:
.org 0x3199C
m68k_03199c:
        subq.w #0x1,0xcfd2:w
m68k_03199c_end:
.org 0x319A0
m68k_0319a0:
        cmpi.w #0x8,0xcfd2:w
m68k_0319a0_end:
.org 0x319A6
m68k_0319a6:
        bls.w (. + 44)
m68k_0319a6_end:
.org 0x319B4
m68k_0319b4:
        btst.b #0x5,0xf603:w
m68k_0319b4_end:
.org 0x319BA
m68k_0319ba:
        beq.w (. + 24)
m68k_0319ba_end:
.org 0x319BE
m68k_0319be:
        move.w #0xb0,0xf600:w
m68k_0319be_end:
.org 0x319C4
m68k_0319c4:
        move.w #0xac,%d0
m68k_0319c4_end:
.org 0x319C8
m68k_0319c8:
        jsr 0x808a:l
m68k_0319c8_end:
.org 0x319CE
m68k_0319ce:
        bsr.w (. + -176)
m68k_0319ce_end:
.org 0x319D2
m68k_0319d2:
        rts
m68k_0319d2_end:
.org 0x31A0C
m68k_031a0c:
        move.w 0xf728:w,%d0
m68k_031a0c_end:
.org 0x31A10
m68k_031a10:
        bmi.w (. + 18)
m68k_031a10_end:
.org 0x31A14
m68k_031a14:
        subq.w #0x1,%d0
m68k_031a14_end:
.org 0x31A16
m68k_031a16:
        lsl.w #0x1,%d0
m68k_031a16_end:
.org 0x31A18
m68k_031a18:
        move.w 10(%pc, %d0.w),%d0
m68k_031a18_end:
.org 0x31A1C
m68k_031a1c:
        jsr 36(%pc, %d0.w)
m68k_031a1c_end:
.org 0x31A20
m68k_031a20:
        bra.b (. + -20)
m68k_031a20_end:
.org 0x31A22
m68k_031a22:
        rts
m68k_031a22_end:
.org 0x31A42
m68k_031a42:
        move.w 0xf364:w,%d0
m68k_031a42_end:
.org 0x31A46
m68k_031a46:
        bsr.w (. + 42)
m68k_031a46_end:
.org 0x31A4A
m68k_031a4a:
        tst.w %d5
m68k_031a4a_end:
.org 0x31A4C
m68k_031a4c:
        bmi.w (. + 28)
m68k_031a4c_end:
.org 0x31A50
m68k_031a50:
        move.w 0xf364:w,%d2
m68k_031a50_end:
.org 0x31A54
m68k_031a54:
        bsr.w (. + 98)
m68k_031a54_end:
.org 0x31A58
m68k_031a58:
        cmp.l %d1,%d4
m68k_031a58_end:
.org 0x31A5A
m68k_031a5a:
        bcc.w (. + 14)
m68k_031a5a_end:
.org 0x31A5E
m68k_031a5e:
        move.w #0x3,0xf728:w
m68k_031a5e_end:
.org 0x31A64
m68k_031a64:
        bra.w (. + 10)
m68k_031a64_end:
.org 0x31A68
m68k_031a68:
        move.w #0x2,0xf728:w
m68k_031a68_end:
.org 0x31A6E
m68k_031a6e:
        rts
m68k_031a6e_end:
.org 0x31A70
m68k_031a70:
        movem.l %d0/%d2-%d4/%a0-%a2,-(%a7)
m68k_031a70_end:
.org 0x31A74
m68k_031a74:
        lea.l 0xd4bda:l,%a0
m68k_031a74_end:
.org 0x31A7A
m68k_031a7a:
        lea.l 0xea37:w,%a2
m68k_031a7a_end:
.org 0x31A7E
m68k_031a7e:
        lsl.w #0x3,%d0
m68k_031a7e_end:
.org 0x31A80
m68k_031a80:
        adda.w %d0,%a0
m68k_031a80_end:
.org 0x31A82
m68k_031a82:
        move.w 0xf376:w,%d3
m68k_031a82_end:
.org 0x31A86
m68k_031a86:
        lea.l 0xf427:w,%a1
m68k_031a86_end:
.org 0x31A8A
m68k_031a8a:
        clr.w %d1
m68k_031a8a_end:
.org 0x31A8C
m68k_031a8c:
        move.w #0xffff,%d5
m68k_031a8c_end:
.org 0x31A90
m68k_031a90:
        clr.w %d2
m68k_031a90_end:
.org 0x31A92
m68k_031a92:
        move.b (%a0)+,%d2
m68k_031a92_end:
.org 0x31A94
m68k_031a94:
        bmi.b (. + 28)
m68k_031a94_end:
.org 0x31A96
m68k_031a96:
        tst.b (%a2, %d2.w)
m68k_031a96_end:
.org 0x31A9A
m68k_031a9a:
        bne.b (. + -10)
m68k_031a9a_end:
.org 0x31A9C
m68k_031a9c:
        cmp.b (%a1, %d2.w),%d3
m68k_031a9c_end:
.org 0x31AA0
m68k_031aa0:
        beq.b (. + -16)
m68k_031aa0_end:
.org 0x31AA2
m68k_031aa2:
        bsr.w (. + 20)
m68k_031aa2_end:
.org 0x31AA6
m68k_031aa6:
        cmp.w %d1,%d4
m68k_031aa6_end:
.org 0x31AA8
m68k_031aa8:
        bls.b (. + -24)
m68k_031aa8_end:
.org 0x31AAA
m68k_031aaa:
        move.w %d4,%d1
m68k_031aaa_end:
.org 0x31AAC
m68k_031aac:
        move.w %d2,%d5
m68k_031aac_end:
.org 0x31AAE
m68k_031aae:
        bra.b (. + -30)
m68k_031aae_end:
.org 0x31AB0
m68k_031ab0:
        movem.l (%a7)+,%d0/%d2-%d4/%a0-%a2
m68k_031ab0_end:
.org 0x31AB4
m68k_031ab4:
        rts
m68k_031ab4_end:
.org 0x31AB6
m68k_031ab6:
        movem.l %d6-%d7/%a3,-(%a7)
m68k_031ab6_end:
.org 0x31ABA
m68k_031aba:
        lea.l 0xcc00:w,%a3
m68k_031aba_end:
.org 0x31ABE
m68k_031abe:
        move.w #0xff,%d6
m68k_031abe_end:
.org 0x31AC2
m68k_031ac2:
        clr.w %d4
m68k_031ac2_end:
.org 0x31AC4
m68k_031ac4:
        cmp.b (%a3, %d6.w),%d2
m68k_031ac4_end:
.org 0x31AC8
m68k_031ac8:
        bne.w (. + 6)
m68k_031ac8_end:
.org 0x31ACC
m68k_031acc:
        addq.w #0x1,%d4
m68k_031acc_end:
.org 0x31ACE
m68k_031ace:
        dbra %d6,(. + -10)
m68k_031ace_end:
.org 0x31AD2
m68k_031ad2:
        movem.l (%a7)+,%d6-%d7/%a3
m68k_031ad2_end:
.org 0x31AD6
m68k_031ad6:
        rts
m68k_031ad6_end:
.org 0x31AD8
m68k_031ad8:
        bsr.w (. + 26)
m68k_031ad8_end:
.org 0x31ADC
m68k_031adc:
        bcc.w (. + 14)
m68k_031adc_end:
.org 0x31AEA
m68k_031aea:
        move.w #0x8,0xf728:w
m68k_031aea_end:
.org 0x31AF0
m68k_031af0:
        rts
m68k_031af0_end:
.org 0x31AF2
m68k_031af2:
        lea.l 0xd4ac6:l,%a0
m68k_031af2_end:
.org 0x31AF8
m68k_031af8:
        move.w 0xf364:w,%d0
m68k_031af8_end:
.org 0x31AFC
m68k_031afc:
        lsl.w #0x2,%d0
m68k_031afc_end:
.org 0x31AFE
m68k_031afe:
        move.w 0x2(%a0, %d0.w),%d1
m68k_031afe_end:
.org 0x31B02
m68k_031b02:
        lsr.w #0x4,%d1
m68k_031b02_end:
.org 0x31B04
m68k_031b04:
        move.w %d1,%d2
m68k_031b04_end:
.org 0x31B06
m68k_031b06:
        subi.w #0x5,%d1
m68k_031b06_end:
.org 0x31B0A
m68k_031b0a:
        bcc.w (. + 6)
m68k_031b0a_end:
.org 0x31B10
m68k_031b10:
        addi.w #0x5,%d2
m68k_031b10_end:
.org 0x31B14
m68k_031b14:
        move.w (%a0, %d0.w),%d3
m68k_031b14_end:
.org 0x31B18
m68k_031b18:
        move.w %d3,%d4
m68k_031b18_end:
.org 0x31B1A
m68k_031b1a:
        subi.w #0x5,%d3
m68k_031b1a_end:
.org 0x31B1E
m68k_031b1e:
        bcc.w (. + 6)
m68k_031b1e_end:
.org 0x31B24
m68k_031b24:
        addi.w #0x5,%d4
m68k_031b24_end:
.org 0x31B28
m68k_031b28:
        lea.l 0x9000:w,%a0
m68k_031b28_end:
.org 0x31B2C
m68k_031b2c:
        move.b (%a0),%d0
m68k_031b2c_end:
.org 0x31B2E
m68k_031b2e:
        andi.w #0xf,%d0
m68k_031b2e_end:
.org 0x31B32
m68k_031b32:
        beq.w (. + 50)
m68k_031b32_end:
.org 0x31B64
m68k_031b64:
        andi.w #0xfffe,%sr
m68k_031b64_end:
.org 0x31B68
m68k_031b68:
        rts
m68k_031b68_end:
.org 0x31B6A
m68k_031b6a:
        bsr.w (. + 60)
m68k_031b6a_end:
.org 0x31B6E
m68k_031b6e:
        cmpi.w #0x32,%d1
m68k_031b6e_end:
.org 0x31B72
m68k_031b72:
        bls.w (. + 34)
m68k_031b72_end:
.org 0x31B76
m68k_031b76:
        cmpi.w #0x47,%d1
m68k_031b76_end:
.org 0x31B7A
m68k_031b7a:
        bcc.w (. + 36)
m68k_031b7a_end:
.org 0x31B94
m68k_031b94:
        move.w #0x9,0xf728:w
m68k_031b94_end:
.org 0x31B9A
m68k_031b9a:
        bra.w (. + 10)
m68k_031b9a_end:
.org 0x31B9E
m68k_031b9e:
        move.w #0x4,0xf728:w
m68k_031b9e_end:
.org 0x31BA4
m68k_031ba4:
        rts
m68k_031ba4_end:
.org 0x31BA6
m68k_031ba6:
        lea.l 0xf72a:w,%a0
m68k_031ba6_end:
.org 0x31BAA
m68k_031baa:
        lea.l 0xc300:w,%a1
m68k_031baa_end:
.org 0x31BAE
m68k_031bae:
        move.w #0xff,%d1
m68k_031bae_end:
.org 0x31BB2
m68k_031bb2:
        clr.w %d2
m68k_031bb2_end:
.org 0x31BB4
m68k_031bb4:
        move.w (%a0)+,%d4
m68k_031bb4_end:
.org 0x31BB6
m68k_031bb6:
        bmi.w (. + 18)
m68k_031bb6_end:
.org 0x31BBA
m68k_031bba:
        move.b (%a1, %d4.w),%d2
m68k_031bba_end:
.org 0x31BBE
m68k_031bbe:
        beq.b (. + -10)
m68k_031bbe_end:
.org 0x31BC0
m68k_031bc0:
        cmp.w %d1,%d2
m68k_031bc0_end:
.org 0x31BC2
m68k_031bc2:
        bcc.b (. + -14)
m68k_031bc2_end:
.org 0x31BC4
m68k_031bc4:
        move.w %d2,%d1
m68k_031bc4_end:
.org 0x31BC6
m68k_031bc6:
        bra.b (. + -18)
m68k_031bc6_end:
.org 0x31BC8
m68k_031bc8:
        rts
m68k_031bc8_end:
.org 0x31BCA
m68k_031bca:
        bsr.w (. + 34)
m68k_031bca_end:
.org 0x31BCE
m68k_031bce:
        bcs.w (. + 22)
m68k_031bce_end:
.org 0x31BD2
m68k_031bd2:
        bsr.w (. + 116)
m68k_031bd2_end:
.org 0x31BD6
m68k_031bd6:
        bcs.w (. + 14)
m68k_031bd6_end:
.org 0x31BDA
m68k_031bda:
        move.w #0x5,0xf728:w
m68k_031bda_end:
.org 0x31BE0
m68k_031be0:
        bra.w (. + 10)
m68k_031be0_end:
.org 0x31BE4
m68k_031be4:
        move.w #0xa,0xf728:w
m68k_031be4_end:
.org 0x31BEA
m68k_031bea:
        rts
m68k_031bea_end:
.org 0x31BEC
m68k_031bec:
        lea.l 0xf72a:w,%a0
m68k_031bec_end:
.org 0x31BF0
m68k_031bf0:
        lea.l 0xc700:w,%a1
m68k_031bf0_end:
.org 0x31BF4
m68k_031bf4:
        lea.l 0xc600:w,%a2
m68k_031bf4_end:
.org 0x31BF8
m68k_031bf8:
        clr.w %d1
m68k_031bf8_end:
.org 0x31BFA
m68k_031bfa:
        move.w (%a0)+,%d0
m68k_031bfa_end:
.org 0x31BFC
m68k_031bfc:
        bmi.w (. + 68)
m68k_031bfc_end:
.org 0x31C00
m68k_031c00:
        move.b (%a2, %d0.w),%d1
m68k_031c00_end:
.org 0x31C04
m68k_031c04:
        clr.w %d2
m68k_031c04_end:
.org 0x31C06
m68k_031c06:
        cmpi.w #0x5,%d1
m68k_031c06_end:
.org 0x31C0A
m68k_031c0a:
        bcs.b (. + -16)
m68k_031c0a_end:
.org 0x31C0C
m68k_031c0c:
        addq.w #0x1,%d2
m68k_031c0c_end:
.org 0x31C0E
m68k_031c0e:
        cmpi.w #0xa,%d1
m68k_031c0e_end:
.org 0x31C12
m68k_031c12:
        bcs.w (. + 26)
m68k_031c12_end:
.org 0x31C16
m68k_031c16:
        addq.w #0x1,%d2
m68k_031c16_end:
.org 0x31C18
m68k_031c18:
        cmpi.w #0xf,%d1
m68k_031c18_end:
.org 0x31C1C
m68k_031c1c:
        bcs.w (. + 16)
m68k_031c1c_end:
.org 0x31C20
m68k_031c20:
        addq.w #0x1,%d2
m68k_031c20_end:
.org 0x31C22
m68k_031c22:
        cmpi.w #0x14,%d1
m68k_031c22_end:
.org 0x31C26
m68k_031c26:
        bcs.w (. + 6)
m68k_031c26_end:
.org 0x31C2C
m68k_031c2c:
        move.b (%a1, %d0.w),%d3
m68k_031c2c_end:
.org 0x31C30
m68k_031c30:
        andi.w #0x7,%d3
m68k_031c30_end:
.org 0x31C34
m68k_031c34:
        cmp.w %d2,%d3
m68k_031c34_end:
.org 0x31C36
m68k_031c36:
        bcc.b (. + -60)
m68k_031c36_end:
.org 0x31C38
m68k_031c38:
        ori.w #0x1,%sr
m68k_031c38_end:
.org 0x31C3C
m68k_031c3c:
        bra.w (. + 8)
m68k_031c3c_end:
.org 0x31C40
m68k_031c40:
        andi.w #0xfffe,%sr
m68k_031c40_end:
.org 0x31C44
m68k_031c44:
        rts
m68k_031c44_end:
.org 0x31C46
m68k_031c46:
        lea.l 0xf72a:w,%a0
m68k_031c46_end:
.org 0x31C4A
m68k_031c4a:
        lea.l 0xc700:w,%a1
m68k_031c4a_end:
.org 0x31C4E
m68k_031c4e:
        lea.l 0xb600:w,%a2
m68k_031c4e_end:
.org 0x31C52
m68k_031c52:
        lea.l 0xc000:w,%a3
m68k_031c52_end:
.org 0x31C56
m68k_031c56:
        move.w (%a0)+,%d0
m68k_031c56_end:
.org 0x31C58
m68k_031c58:
        bmi.b (. + 46)
m68k_031c58_end:
.org 0x31C5A
m68k_031c5a:
        btst.b #0x4,(%a1, %d0.w)
m68k_031c5a_end:
.org 0x31C60
m68k_031c60:
        bne.b (. + -10)
m68k_031c60_end:
.org 0x31C62
m68k_031c62:
        lsl.w #0x1,%d0
m68k_031c62_end:
.org 0x31C64
m68k_031c64:
        move.w (%a2, %d0.w),%d1
m68k_031c64_end:
.org 0x31C68
m68k_031c68:
        cmpi.w #0x64,%d1
m68k_031c68_end:
.org 0x31C6C
m68k_031c6c:
        bcc.w (. + 18)
m68k_031c6c_end:
.org 0x31C70
m68k_031c70:
        cmpi.w #0x5f,%d1
m68k_031c70_end:
.org 0x31C74
m68k_031c74:
        bcs.b (. + -30)
m68k_031c74_end:
.org 0x31C86
m68k_031c86:
        andi.w #0xfffe,%sr
m68k_031c86_end:
.org 0x31C8A
m68k_031c8a:
        rts
m68k_031c8a_end:
.org 0x31C8C
m68k_031c8c:
        lea.l 0xe31c:w,%a0
m68k_031c8c_end:
.org 0x31C90
m68k_031c90:
        move.w 0xf364:w,%d0
m68k_031c90_end:
.org 0x31C94
m68k_031c94:
        lsl.w #0x2,%d0
m68k_031c94_end:
.org 0x31C96
m68k_031c96:
        move.w 0x2(%a0, %d0.w),%d1
m68k_031c96_end:
.org 0x31C9A
m68k_031c9a:
        cmpi.w #0x32,%d1
m68k_031c9a_end:
.org 0x31C9E
m68k_031c9e:
        bls.w (. + 30)
m68k_031c9e_end:
.org 0x31CA2
m68k_031ca2:
        cmpi.w #0x42,%d1
m68k_031ca2_end:
.org 0x31CA6
m68k_031ca6:
        bcc.w (. + 32)
m68k_031ca6_end:
.org 0x31CAA
m68k_031caa:
        jsr 0x83d4:l
m68k_031caa_end:
.org 0x31CB0
m68k_031cb0:
        andi.w #0x7,%d0
m68k_031cb0_end:
.org 0x31CB4
m68k_031cb4:
        cmpi.w #0x5,%d0
m68k_031cb4_end:
.org 0x31CB8
m68k_031cb8:
        bcc.w (. + 14)
m68k_031cb8_end:
.org 0x31CBC
m68k_031cbc:
        move.w #0xb,0xf728:w
m68k_031cbc_end:
.org 0x31CC2
m68k_031cc2:
        bra.w (. + 10)
m68k_031cc2_end:
.org 0x31CC6
m68k_031cc6:
        move.w #0x6,0xf728:w
m68k_031cc6_end:
.org 0x31CCC
m68k_031ccc:
        rts
m68k_031ccc_end:
.org 0x31CCE
m68k_031cce:
        jsr 0x83d4:l
m68k_031cce_end:
.org 0x31CD4
m68k_031cd4:
        bsr.w (. + 122)
m68k_031cd4_end:
.org 0x31CD8
m68k_031cd8:
        bsr.w (. + 148)
m68k_031cd8_end:
.org 0x31CDC
m68k_031cdc:
        move.w 0xf61c:w,%d0
m68k_031cdc_end:
.org 0x31CE0
m68k_031ce0:
        move.l %d4,%d5
m68k_031ce0_end:
.org 0x31CE2
m68k_031ce2:
        lsl.l #0x1,%d5
m68k_031ce2_end:
.org 0x31CE4
m68k_031ce4:
        cmp.l %d5,%d3
m68k_031ce4_end:
.org 0x31CE6
m68k_031ce6:
        bcs.w (. + 86)
m68k_031ce6_end:
.org 0x31CEA
m68k_031cea:
        add.l %d4,%d5
m68k_031cea_end:
.org 0x31CEC
m68k_031cec:
        cmp.l %d5,%d3
m68k_031cec_end:
.org 0x31CEE
m68k_031cee:
        bcc.w (. + 20)
m68k_031cee_end:
.org 0x31D02
m68k_031d02:
        lsl.l #0x1,%d4
m68k_031d02_end:
.org 0x31D04
m68k_031d04:
        add.l %d4,%d5
m68k_031d04_end:
.org 0x31D06
m68k_031d06:
        cmp.l %d5,%d3
m68k_031d06_end:
.org 0x31D08
m68k_031d08:
        bcc.w (. + 20)
m68k_031d08_end:
.org 0x31D0C
m68k_031d0c:
        andi.w #0x3,%d0
m68k_031d0c_end:
.org 0x31D10
m68k_031d10:
        cmpi.w #0x3,%d0
m68k_031d10_end:
.org 0x31D14
m68k_031d14:
        bcs.w (. + 40)
m68k_031d14_end:
.org 0x31D1C
m68k_031d1c:
        lsl.l #0x1,%d5
m68k_031d1c_end:
.org 0x31D1E
m68k_031d1e:
        cmp.l %d5,%d3
m68k_031d1e_end:
.org 0x31D20
m68k_031d20:
        bcc.w (. + 16)
m68k_031d20_end:
.org 0x31D24
m68k_031d24:
        btst.l #0x0,%d0
m68k_031d24_end:
.org 0x31D28
m68k_031d28:
        bne.w (. + 20)
m68k_031d28_end:
.org 0x31D30
m68k_031d30:
        andi.w #0x7,%d0
m68k_031d30_end:
.org 0x31D34
m68k_031d34:
        cmpi.w #0x3,%d0
m68k_031d34_end:
.org 0x31D38
m68k_031d38:
        bcc.w (. + 14)
m68k_031d38_end:
.org 0x31D3C
m68k_031d3c:
        move.w #0xc,0xf728:w
m68k_031d3c_end:
.org 0x31D42
m68k_031d42:
        bra.w (. + 10)
m68k_031d42_end:
.org 0x31D46
m68k_031d46:
        move.w #0x7,0xf728:w
m68k_031d46_end:
.org 0x31D4C
m68k_031d4c:
        rts
m68k_031d4c_end:
.org 0x31D4E
m68k_031d4e:
        move.w 0xf364:w,%d0
m68k_031d4e_end:
.org 0x31D52
m68k_031d52:
        subq.w #0x1,%d0
m68k_031d52_end:
.org 0x31D54
m68k_031d54:
        lea.l 0xe280:w,%a0
m68k_031d54_end:
.org 0x31D58
m68k_031d58:
        move.w %d0,%d1
m68k_031d58_end:
.org 0x31D5A
m68k_031d5a:
        lsl.w #0x2,%d1
m68k_031d5a_end:
.org 0x31D5C
m68k_031d5c:
        move.w #0x64,%d7
m68k_031d5c_end:
.org 0x31D60
m68k_031d60:
        sub.w 0x2(%a0, %d1.w),%d7
m68k_031d60_end:
.org 0x31D64
m68k_031d64:
        jsr 0x16c72:l
m68k_031d64_end:
.org 0x31D6A
m68k_031d6a:
        rts
m68k_031d6a_end:
.org 0x31D6C
m68k_031d6c:
        lea.l 0xf72a:w,%a0
m68k_031d6c_end:
.org 0x31D70
m68k_031d70:
        lea.l 0xc700:w,%a1
m68k_031d70_end:
.org 0x31D74
m68k_031d74:
        clr.w %d4
m68k_031d74_end:
.org 0x31D76
m68k_031d76:
        move.w (%a0)+,%d0
m68k_031d76_end:
.org 0x31D78
m68k_031d78:
        bmi.w (. + 20)
m68k_031d78_end:
.org 0x31D7C
m68k_031d7c:
        move.b (%a1, %d0.w),%d5
m68k_031d7c_end:
.org 0x31D80
m68k_031d80:
        andi.w #0x7,%d5
m68k_031d80_end:
.org 0x31D84
m68k_031d84:
        lsl.w #0x1,%d5
m68k_031d84_end:
.org 0x31D86
m68k_031d86:
        add.w 12(%pc, %d5.w),%d4
m68k_031d86_end:
.org 0x31D8A
m68k_031d8a:
        bra.b (. + -20)
m68k_031d8a_end:
.org 0x31D8C
m68k_031d8c:
        andi.l #0xffff,%d4
m68k_031d8c_end:
.org 0x31D92
m68k_031d92:
        rts
m68k_031d92_end:
.org 0x31D9E
m68k_031d9e:
        bsr.w (. + 78)
m68k_031d9e_end:
.org 0x31DA2
m68k_031da2:
        lea.l 0xe09c:w,%a0
m68k_031da2_end:
.org 0x31DA6
m68k_031da6:
        move.w 0xf364:w,%d2
m68k_031da6_end:
.org 0x31DAA
m68k_031daa:
        lsl.w #0x2,%d2
m68k_031daa_end:
.org 0x31DAC
m68k_031dac:
        move.l (%a0, %d2.w),%d2
m68k_031dac_end:
.org 0x31DB0
m68k_031db0:
        andi.l #0xffff,%d0
m68k_031db0_end:
.org 0x31DB6
m68k_031db6:
        move.l %d0,%d1
m68k_031db6_end:
.org 0x31DB8
m68k_031db8:
        lsl.l #0x1,%d0
m68k_031db8_end:
.org 0x31DBA
m68k_031dba:
        add.l %d1,%d0
m68k_031dba_end:
.org 0x31DBC
m68k_031dbc:
        cmp.l %d0,%d2
m68k_031dbc_end:
.org 0x31DBE
m68k_031dbe:
        bcs.w (. + 28)
m68k_031dbe_end:
.org 0x31DC2
m68k_031dc2:
        lsl.l #0x2,%d1
m68k_031dc2_end:
.org 0x31DC4
m68k_031dc4:
        add.l %d1,%d0
m68k_031dc4_end:
.org 0x31DC6
m68k_031dc6:
        cmp.l %d0,%d2
m68k_031dc6_end:
.org 0x31DC8
m68k_031dc8:
        bcc.w (. + 28)
m68k_031dc8_end:
.org 0x31DCC
m68k_031dcc:
        jsr 0x83d4:l
m68k_031dcc_end:
.org 0x31DD2
m68k_031dd2:
        btst.l #0x1,%d0
m68k_031dd2_end:
.org 0x31DD6
m68k_031dd6:
        bne.w (. + 14)
m68k_031dd6_end:
.org 0x31DDA
m68k_031dda:
        move.w #0xe,0xf728:w
m68k_031dda_end:
.org 0x31DE0
m68k_031de0:
        bra.w (. + 10)
m68k_031de0_end:
.org 0x31DE4
m68k_031de4:
        move.w #0xd,0xf728:w
m68k_031de4_end:
.org 0x31DEA
m68k_031dea:
        rts
m68k_031dea_end:
.org 0x31DEC
m68k_031dec:
        lea.l 0xf72a:w,%a0
m68k_031dec_end:
.org 0x31DF0
m68k_031df0:
        lea.l 0xc800:w,%a1
m68k_031df0_end:
.org 0x31DF4
m68k_031df4:
        moveq #0,%d0
m68k_031df4_end:
.org 0x31DF6
m68k_031df6:
        move.w (%a0)+,%d1
m68k_031df6_end:
.org 0x31DF8
m68k_031df8:
        bmi.w (. + 18)
m68k_031df8_end:
.org 0x31DFC
m68k_031dfc:
        lsl.w #0x2,%d1
m68k_031dfc_end:
.org 0x31DFE
m68k_031dfe:
        add.l (%a1, %d1.w),%d0
m68k_031dfe_end:
.org 0x31E02
m68k_031e02:
        addi.l #0x64,%d0
m68k_031e02_end:
.org 0x31E08
m68k_031e08:
        bra.b (. + -18)
m68k_031e08_end:
.org 0x31E0A
m68k_031e0a:
        divu.w #0x32,%d0
m68k_031e0a_end:
.org 0x31E0E
m68k_031e0e:
        move.w %d0,%d1
m68k_031e0e_end:
.org 0x31E10
m68k_031e10:
        lsl.w #0x1,%d0
m68k_031e10_end:
.org 0x31E12
m68k_031e12:
        add.w %d1,%d0
m68k_031e12_end:
.org 0x31E14
m68k_031e14:
        rts
m68k_031e14_end:
.org 0x31E16
m68k_031e16:
        move.w 0xf364:w,%d2
m68k_031e16_end:
.org 0x31E1A
m68k_031e1a:
        bsr.w (. + -868)
m68k_031e1a_end:
.org 0x31E1E
m68k_031e1e:
        cmpi.w #0x1,%d4
m68k_031e1e_end:
.org 0x31E22
m68k_031e22:
        beq.w (. + 68)
m68k_031e22_end:
.org 0x31E26
m68k_031e26:
        bsr.w (. + 72)
m68k_031e26_end:
.org 0x31E2A
m68k_031e2a:
        tst.w 0xf3a6:w
m68k_031e2a_end:
.org 0x31E2E
m68k_031e2e:
        bmi.w (. + 56)
m68k_031e2e_end:
.org 0x31E32
m68k_031e32:
        bsr.w (. + 110)
m68k_031e32_end:
.org 0x31E36
m68k_031e36:
        tst.w 0xf392:w
m68k_031e36_end:
.org 0x31E3A
m68k_031e3a:
        beq.w (. + 44)
m68k_031e3a_end:
.org 0x31E3E
m68k_031e3e:
        lea.l 0xcd00:w,%a0
m68k_031e3e_end:
.org 0x31E42
m68k_031e42:
        move.w 0xf3a6:w,%d0
m68k_031e42_end:
.org 0x31E46
m68k_031e46:
        move.b #0x1,(%a0, %d0.w)
m68k_031e46_end:
.org 0x31E4C
m68k_031e4c:
        lea.l 0xcc00:w,%a0
m68k_031e4c_end:
.org 0x31E50
m68k_031e50:
        move.w 0xf3a6:w,%d0
m68k_031e50_end:
.org 0x31E54
m68k_031e54:
        move.b 0xf393:w,(%a0, %d0.w)
m68k_031e54_end:
.org 0x31E5A
m68k_031e5a:
        bsr.w (. + 164)
m68k_031e5a_end:
.org 0x31E5E
m68k_031e5e:
        bsr.w (. + 220)
m68k_031e5e_end:
.org 0x31E62
m68k_031e62:
        bsr.w (. + 236)
m68k_031e62_end:
.org 0x31E66
m68k_031e66:
        move.w #0x3,0xf728:w
m68k_031e66_end:
.org 0x31E6C
m68k_031e6c:
        rts
m68k_031e6c_end:
.org 0x31E6E
m68k_031e6e:
        lea.l 0xf72a:w,%a0
m68k_031e6e_end:
.org 0x31E72
m68k_031e72:
        lea.l 0xb400:w,%a1
m68k_031e72_end:
.org 0x31E76
m68k_031e76:
        clr.w %d1
m68k_031e76_end:
.org 0x31E78
m68k_031e78:
        move.w #0xffff,0xf3a6:w
m68k_031e78_end:
.org 0x31E7E
m68k_031e7e:
        move.w (%a0)+,%d0
m68k_031e7e_end:
.org 0x31E80
m68k_031e80:
        bmi.w (. + 30)
m68k_031e80_end:
.org 0x31E84
m68k_031e84:
        btst.l #0xe,%d0
m68k_031e84_end:
.org 0x31E88
m68k_031e88:
        bne.b (. + -10)
m68k_031e88_end:
.org 0x31E8A
m68k_031e8a:
        lsl.w #0x1,%d0
m68k_031e8a_end:
.org 0x31E8C
m68k_031e8c:
        move.w (%a1, %d0.w),%d2
m68k_031e8c_end:
.org 0x31E90
m68k_031e90:
        cmp.w %d1,%d2
m68k_031e90_end:
.org 0x31E92
m68k_031e92:
        bls.b (. + -20)
m68k_031e92_end:
.org 0x31E94
m68k_031e94:
        move.w %d2,%d1
m68k_031e94_end:
.org 0x31E96
m68k_031e96:
        lsr.w #0x1,%d0
m68k_031e96_end:
.org 0x31E98
m68k_031e98:
        move.w %d0,0xf3a6:w
m68k_031e98_end:
.org 0x31E9C
m68k_031e9c:
        bra.b (. + -30)
m68k_031e9c_end:
.org 0x31E9E
m68k_031e9e:
        rts
m68k_031e9e_end:
.org 0x31EA0
m68k_031ea0:
        move.w 0xf376:w,%d6
m68k_031ea0_end:
.org 0x31EA4
m68k_031ea4:
        lea.l 0xf450:w,%a0
m68k_031ea4_end:
.org 0x31EA8
m68k_031ea8:
        lea.l 0xea37:w,%a1
m68k_031ea8_end:
.org 0x31EAC
m68k_031eac:
        clr.w %d7
m68k_031eac_end:
.org 0x31EAE
m68k_031eae:
        clr.w %d3
m68k_031eae_end:
.org 0x31EB0
m68k_031eb0:
        clr.w 0xf392:w
m68k_031eb0_end:
.org 0x31EB4
m68k_031eb4:
        move.w #0x28,%d0
m68k_031eb4_end:
.org 0x31EB8
m68k_031eb8:
        cmp.b -(%a0),%d6
m68k_031eb8_end:
.org 0x31EBA
m68k_031eba:
        bne.w (. + 62)
m68k_031eba_end:
.org 0x31EBE
m68k_031ebe:
        tst.b (%a1, %d0.w)
m68k_031ebe_end:
.org 0x31EC2
m68k_031ec2:
        bne.w (. + 54)
m68k_031ec2_end:
.org 0x31EC6
m68k_031ec6:
        cmp.w 0xf364:w,%d0
m68k_031ec6_end:
.org 0x31ECA
m68k_031eca:
        beq.w (. + 46)
m68k_031eca_end:
.org 0x31ECE
m68k_031ece:
        move.w %d0,%d2
m68k_031ece_end:
.org 0x31ED0
m68k_031ed0:
        bsr.w (. + -1050)
m68k_031ed0_end:
.org 0x31ED4
m68k_031ed4:
        cmpi.w #0xa,%d4
m68k_031ed4_end:
.org 0x31ED8
m68k_031ed8:
        bcc.w (. + 32)
m68k_031ed8_end:
.org 0x31EDC
m68k_031edc:
        bsr.w (. + -1132)
m68k_031edc_end:
.org 0x31EE0
m68k_031ee0:
        cmp.w %d7,%d1
m68k_031ee0_end:
.org 0x31EE2
m68k_031ee2:
        bcs.w (. + 22)
m68k_031ee2_end:
.org 0x31EE6
m68k_031ee6:
        bne.w (. + 10)
m68k_031ee6_end:
.org 0x31EF0
m68k_031ef0:
        move.w %d4,%d3
m68k_031ef0_end:
.org 0x31EF2
m68k_031ef2:
        move.w %d1,%d7
m68k_031ef2_end:
.org 0x31EF4
m68k_031ef4:
        move.w %d0,0xf392:w
m68k_031ef4_end:
.org 0x31EF8
m68k_031ef8:
        subq.w #0x1,%d0
m68k_031ef8_end:
.org 0x31EFA
m68k_031efa:
        bne.b (. + -66)
m68k_031efa_end:
.org 0x31EFC
m68k_031efc:
        rts
m68k_031efc_end:
.org 0x31EFE
m68k_031efe:
        lea.l 0xf45e:w,%a0
m68k_031efe_end:
.org 0x31F02
m68k_031f02:
        move.w 0xf364:w,%d0
m68k_031f02_end:
.org 0x31F06
m68k_031f06:
        lsl.w #0x1,%d0
m68k_031f06_end:
.org 0x31F08
m68k_031f08:
        move.w (%a0, %d0.w),%d0
m68k_031f08_end:
.org 0x31F0C
m68k_031f0c:
        cmp.w 0xf3a6:w,%d0
m68k_031f0c_end:
.org 0x31F10
m68k_031f10:
        bne.w (. + 40)
m68k_031f10_end:
.org 0x31F38
m68k_031f38:
        rts
m68k_031f38_end:
.org 0x31F3A
m68k_031f3a:
        lea.l 0xf72a:w,%a0
m68k_031f3a_end:
.org 0x31F3E
m68k_031f3e:
        move.w 0xf3a6:w,%d0
m68k_031f3e_end:
.org 0x31F42
m68k_031f42:
        cmp.w (%a0)+,%d0
m68k_031f42_end:
.org 0x31F44
m68k_031f44:
        bne.b (. + -2)
m68k_031f44_end:
.org 0x31F46
m68k_031f46:
        move.w (%a0)+,-0x4(%a0)
m68k_031f46_end:
.org 0x31F4A
m68k_031f4a:
        bpl.b (. + -4)
m68k_031f4a_end:
.org 0x31F4C
m68k_031f4c:
        rts
m68k_031f4c_end:
.org 0x31F4E
m68k_031f4e:
        movem.l %d0/%a0,-(%a7)
m68k_031f4e_end:
.org 0x31F52
m68k_031f52:
        lea.l 0xe640:w,%a0
m68k_031f52_end:
.org 0x31F56
m68k_031f56:
        move.w 0xf376:w,%d0
m68k_031f56_end:
.org 0x31F5A
m68k_031f5a:
        lsl.w #0x1,%d0
m68k_031f5a_end:
.org 0x31F5C
m68k_031f5c:
        move.w (%a0, %d0.w),%d0
m68k_031f5c_end:
.org 0x31F60
m68k_031f60:
        cmp.w 0xf3a6:w,%d0
m68k_031f60_end:
.org 0x31F64
m68k_031f64:
        bne.w (. + 20)
m68k_031f64_end:
.org 0x31F78
m68k_031f78:
        movem.l (%a7)+,%d0/%a0
m68k_031f78_end:
.org 0x31F7C
m68k_031f7c:
        rts
m68k_031f7c_end:
.org 0x31F7E
m68k_031f7e:
        lea.l 0xe640:w,%a1
m68k_031f7e_end:
.org 0x31F82
m68k_031f82:
        move.w 0xf376:w,%d0
m68k_031f82_end:
.org 0x31F86
m68k_031f86:
        lsl.w #0x1,%d0
m68k_031f86_end:
.org 0x31F88
m68k_031f88:
        move.w (%a1, %d0.w),0xf634:w
m68k_031f88_end:
.org 0x31F8E
m68k_031f8e:
        lea.l 0xf45e:w,%a1
m68k_031f8e_end:
.org 0x31F92
m68k_031f92:
        move.w 0xf364:w,%d0
m68k_031f92_end:
.org 0x31F96
m68k_031f96:
        lsl.w #0x1,%d0
m68k_031f96_end:
.org 0x31F98
m68k_031f98:
        move.w (%a1, %d0.w),0xf630:w
m68k_031f98_end:
.org 0x31F9E
m68k_031f9e:
        bsr.w (. + 88)
m68k_031f9e_end:
.org 0x31FA2
m68k_031fa2:
        tst.w 0xf3a6:w
m68k_031fa2_end:
.org 0x31FA6
m68k_031fa6:
        bmi.w (. + 72)
m68k_031fa6_end:
.org 0x31FAA
m68k_031faa:
        move.w 0xf630:w,%d0
m68k_031faa_end:
.org 0x31FAE
m68k_031fae:
        cmp.w 0xf3a6:w,%d0
m68k_031fae_end:
.org 0x31FB2
m68k_031fb2:
        bne.w (. + 8)
m68k_031fb2_end:
.org 0x31FB6
m68k_031fb6:
        move.w 0xf634:w,%d0
m68k_031fb6_end:
.org 0x31FBA
m68k_031fba:
        lea.l 0xcd00:w,%a0
m68k_031fba_end:
.org 0x31FBE
m68k_031fbe:
        tst.b (%a0, %d0.w)
m68k_031fbe_end:
.org 0x31FC2
m68k_031fc2:
        bne.w (. + 44)
m68k_031fc2_end:
.org 0x31FC6
m68k_031fc6:
        move.b #0x1,(%a0, %d0.w)
m68k_031fc6_end:
.org 0x31FCC
m68k_031fcc:
        bsr.w (. + 212)
m68k_031fcc_end:
.org 0x31FD0
m68k_031fd0:
        move.w 0xf3a6:w,%d0
m68k_031fd0_end:
.org 0x31FD4
m68k_031fd4:
        move.b #0x1,(%a0, %d0.w)
m68k_031fd4_end:
.org 0x31FDA
m68k_031fda:
        bsr.w (. + 198)
m68k_031fda_end:
.org 0x31FDE
m68k_031fde:
        bsr.w (. + 126)
m68k_031fde_end:
.org 0x31FE2
m68k_031fe2:
        move.w 0xf364:w,0xf392:w
m68k_031fe2_end:
.org 0x31FE8
m68k_031fe8:
        jsr 0xe592:l
m68k_031fe8_end:
.org 0x31FEE
m68k_031fee:
        move.w #0x4,0xf728:w
m68k_031fee_end:
.org 0x31FF4
m68k_031ff4:
        rts
m68k_031ff4_end:
.org 0x31FF6
m68k_031ff6:
        lea.l 0xf72a:w,%a0
m68k_031ff6_end:
.org 0x31FFA
m68k_031ffa:
        lea.l 0xc300:w,%a1
m68k_031ffa_end:
.org 0x31FFE
m68k_031ffe:
        move.w #0xff,%d1
m68k_031ffe_end:
.org 0x32002
m68k_032002:
        move.w #0xffff,%d2
m68k_032002_end:
.org 0x32006
m68k_032006:
        clr.w %d3
m68k_032006_end:
.org 0x32008
m68k_032008:
        move.w #0xffff,%d4
m68k_032008_end:
.org 0x3200C
m68k_03200c:
        move.w (%a0)+,%d0
m68k_03200c_end:
.org 0x3200E
m68k_03200e:
        bmi.w (. + 42)
m68k_03200e_end:
.org 0x32012
m68k_032012:
        btst.l #0xe,%d0
m68k_032012_end:
.org 0x32016
m68k_032016:
        bne.b (. + -10)
m68k_032016_end:
.org 0x32018
m68k_032018:
        move.b (%a1, %d0.w),%d5
m68k_032018_end:
.org 0x3201C
m68k_03201c:
        cmpi.b #0x28,%d5
m68k_03201c_end:
.org 0x32020
m68k_032020:
        bcs.w (. + 14)
m68k_032020_end:
.org 0x32024
m68k_032024:
        cmp.b %d1,%d5
m68k_032024_end:
.org 0x32026
m68k_032026:
        bcc.b (. + -26)
m68k_032026_end:
.org 0x32028
m68k_032028:
        move.b %d5,%d1
m68k_032028_end:
.org 0x3202A
m68k_03202a:
        move.w %d0,%d2
m68k_03202a_end:
.org 0x3202C
m68k_03202c:
        bra.b (. + -32)
m68k_03202c_end:
.org 0x32038
m68k_032038:
        cmpi.b #0x50,%d1
m68k_032038_end:
.org 0x3203C
m68k_03203c:
        bhi.w (. + 12)
m68k_03203c_end:
.org 0x32048
m68k_032048:
        tst.w %d3
m68k_032048_end:
.org 0x3204A
m68k_03204a:
        beq.w (. + 12)
m68k_03204a_end:
.org 0x32056
m68k_032056:
        move.w %d2,0xf3a6:w
m68k_032056_end:
.org 0x3205A
m68k_03205a:
        rts
m68k_03205a_end:
.org 0x3205C
m68k_03205c:
        jsr 0x83d4:l
m68k_03205c_end:
.org 0x32062
m68k_032062:
        andi.l #0xffff,%d0
m68k_032062_end:
.org 0x32068
m68k_032068:
        move.l %d0,%d1
m68k_032068_end:
.org 0x3206A
m68k_03206a:
        lsl.l #0x1,%d0
m68k_03206a_end:
.org 0x3206C
m68k_03206c:
        add.l %d1,%d0
m68k_03206c_end:
.org 0x3206E
m68k_03206e:
        lsl.l #0x2,%d0
m68k_03206e_end:
.org 0x32070
m68k_032070:
        add.l %d1,%d0
m68k_032070_end:
.org 0x32072
m68k_032072:
        swap %d0
m68k_032072_end:
.org 0x32074
m68k_032074:
        addi.w #0xa,%d0
m68k_032074_end:
.org 0x32078
m68k_032078:
        lea.l 0xdffc:w,%a0
m68k_032078_end:
.org 0x3207C
m68k_03207c:
        move.w 0xf364:w,%d1
m68k_03207c_end:
.org 0x32080
m68k_032080:
        lsl.w #0x2,%d1
m68k_032080_end:
.org 0x32082
m68k_032082:
        move.l (%a0, %d1.w),%d1
m68k_032082_end:
.org 0x32086
m68k_032086:
        move.w %d1,%d2
m68k_032086_end:
.org 0x32088
m68k_032088:
        mulu.w %d0,%d2
m68k_032088_end:
.org 0x3208A
m68k_03208a:
        swap %d1
m68k_03208a_end:
.org 0x3208C
m68k_03208c:
        mulu.w %d0,%d1
m68k_03208c_end:
.org 0x3208E
m68k_03208e:
        swap %d1
m68k_03208e_end:
.org 0x32090
m68k_032090:
        add.l %d2,%d1
m68k_032090_end:
.org 0x32092
m68k_032092:
        moveq #100,%d2
m68k_032092_end:
.org 0x32094
m68k_032094:
        jsr 0x35760:l
m68k_032094_end:
.org 0x3209A
m68k_03209a:
        move.l %d1,0xf39e:w
m68k_03209a_end:
.org 0x3209E
m68k_03209e:
        rts
m68k_03209e_end:
.org 0x320A0
m68k_0320a0:
        movem.l %a0,-(%a7)
m68k_0320a0_end:
.org 0x320A4
m68k_0320a4:
        lea.l 0xf72a:w,%a0
m68k_0320a4_end:
.org 0x320A8
m68k_0320a8:
        move.w (%a0)+,%d1
m68k_0320a8_end:
.org 0x320AA
m68k_0320aa:
        bmi.w (. + 16)
m68k_0320aa_end:
.org 0x320AE
m68k_0320ae:
        cmp.w %d0,%d1
m68k_0320ae_end:
.org 0x320B0
m68k_0320b0:
        bne.b (. + -8)
m68k_0320b0_end:
.org 0x320B2
m68k_0320b2:
        bset.l #0xe,%d1
m68k_0320b2_end:
.org 0x320B6
m68k_0320b6:
        move.w %d1,-0x2(%a0)
m68k_0320b6_end:
.org 0x320BA
m68k_0320ba:
        movem.l (%a7)+,%a0
m68k_0320ba_end:
.org 0x320BE
m68k_0320be:
        rts
m68k_0320be_end:
.org 0x320C0
m68k_0320c0:
        bsr.w (. + 20)
m68k_0320c0_end:
.org 0x320C4
m68k_0320c4:
        bsr.w (. + 122)
m68k_0320c4_end:
.org 0x320C8
m68k_0320c8:
        bsr.w (. + 202)
m68k_0320c8_end:
.org 0x320CC
m68k_0320cc:
        move.w #0x5,0xf728:w
m68k_0320cc_end:
.org 0x320D2
m68k_0320d2:
        rts
m68k_0320d2_end:
.org 0x320D4
m68k_0320d4:
        lea.l 0xf45e:w,%a4
m68k_0320d4_end:
.org 0x320D8
m68k_0320d8:
        move.w 0xf364:w,%d7
m68k_0320d8_end:
.org 0x320DC
m68k_0320dc:
        lsl.w #0x1,%d7
m68k_0320dc_end:
.org 0x320DE
m68k_0320de:
        move.w (%a4, %d7.w),%d0
m68k_0320de_end:
.org 0x320E2
m68k_0320e2:
        lea.l 0xe640:w,%a5
m68k_0320e2_end:
.org 0x320E6
m68k_0320e6:
        move.w 0xf376:w,%d1
m68k_0320e6_end:
.org 0x320EA
m68k_0320ea:
        lsl.w #0x1,%d1
m68k_0320ea_end:
.org 0x320EC
m68k_0320ec:
        cmp.w (%a5, %d1.w),%d0
m68k_0320ec_end:
.org 0x320F0
m68k_0320f0:
        beq.w (. + 76)
m68k_0320f0_end:
.org 0x320F4
m68k_0320f4:
        lea.l 0xf72a:w,%a0
m68k_0320f4_end:
.org 0x320F8
m68k_0320f8:
        lea.l 0xb600:w,%a1
m68k_0320f8_end:
.org 0x320FC
m68k_0320fc:
        lea.l 0xb400:w,%a2
m68k_0320fc_end:
.org 0x32100
m68k_032100:
        lea.l 0xc300:w,%a3
m68k_032100_end:
.org 0x32104
m68k_032104:
        clr.w %d0
m68k_032104_end:
.org 0x32106
m68k_032106:
        move.w #0xffff,%d1
m68k_032106_end:
.org 0x3210A
m68k_03210a:
        move.w (%a0)+,%d2
m68k_03210a_end:
.org 0x3210C
m68k_03210c:
        bmi.w (. + 38)
m68k_03210c_end:
.org 0x32110
m68k_032110:
        andi.w #0xff,%d2
m68k_032110_end:
.org 0x32114
m68k_032114:
        cmpi.b #0x5a,(%a3, %d2.w)
m68k_032114_end:
.org 0x3211A
m68k_03211a:
        bcs.b (. + -16)
m68k_03211a_end:
.org 0x3211C
m68k_03211c:
        move.w %d2,%d4
m68k_03211c_end:
.org 0x3211E
m68k_03211e:
        lsl.w #0x1,%d4
m68k_03211e_end:
.org 0x32120
m68k_032120:
        move.w (%a1, %d4.w),%d3
m68k_032120_end:
.org 0x32124
m68k_032124:
        add.w (%a2, %d4.w),%d3
m68k_032124_end:
.org 0x32128
m68k_032128:
        cmp.w %d0,%d3
m68k_032128_end:
.org 0x3212A
m68k_03212a:
        bls.b (. + -32)
m68k_03212a_end:
.org 0x3212C
m68k_03212c:
        move.w %d3,%d0
m68k_03212c_end:
.org 0x3212E
m68k_03212e:
        move.w %d2,%d1
m68k_03212e_end:
.org 0x32130
m68k_032130:
        bra.b (. + -38)
m68k_032130_end:
.org 0x32132
m68k_032132:
        tst.w %d1
m68k_032132_end:
.org 0x32134
m68k_032134:
        bmi.w (. + 8)
m68k_032134_end:
.org 0x32138
m68k_032138:
        move.w %d1,(%a4, %d7.w)
m68k_032138_end:
.org 0x3213C
m68k_03213c:
        rts
m68k_03213c_end:
.org 0x3213E
m68k_03213e:
        lea.l 0xf72a:w,%a0
m68k_03213e_end:
.org 0x32142
m68k_032142:
        lea.l 0xb600:w,%a1
m68k_032142_end:
.org 0x32146
m68k_032146:
        lea.l 0xc000:w,%a2
m68k_032146_end:
.org 0x3214A
m68k_03214a:
        clr.w %d0
m68k_03214a_end:
.org 0x3214C
m68k_03214c:
        move.w #0xffff,%d1
m68k_03214c_end:
.org 0x32150
m68k_032150:
        move.w (%a0)+,%d2
m68k_032150_end:
.org 0x32152
m68k_032152:
        bmi.b (. + 46)
m68k_032152_end:
.org 0x32154
m68k_032154:
        andi.w #0xff,%d2
m68k_032154_end:
.org 0x32158
m68k_032158:
        move.w %d2,%d3
m68k_032158_end:
.org 0x3215A
m68k_03215a:
        lsl.w #0x1,%d3
m68k_03215a_end:
.org 0x3215C
m68k_03215c:
        move.w (%a1, %d3.w),%d4
m68k_03215c_end:
.org 0x32160
m68k_032160:
        cmpi.w #0x64,%d4
m68k_032160_end:
.org 0x32164
m68k_032164:
        bcc.w (. + 18)
m68k_032164_end:
.org 0x32168
m68k_032168:
        cmpi.w #0x5f,%d4
m68k_032168_end:
.org 0x3216C
m68k_03216c:
        bcs.b (. + -28)
m68k_03216c_end:
.org 0x32180
m68k_032180:
        tst.w %d1
m68k_032180_end:
.org 0x32182
m68k_032182:
        bmi.w (. + 14)
m68k_032182_end:
.org 0x32190
m68k_032190:
        rts
m68k_032190_end:
.org 0x32192
m68k_032192:
        lea.l 0xf72a:w,%a0
m68k_032192_end:
.org 0x32196
m68k_032196:
        lea.l 0xc700:w,%a1
m68k_032196_end:
.org 0x3219A
m68k_03219a:
        lea.l 0xc600:w,%a2
m68k_03219a_end:
.org 0x3219E
m68k_03219e:
        lea.l 0xc000:w,%a3
m68k_03219e_end:
.org 0x321A2
m68k_0321a2:
        lea.l 0xbe00:w,%a4
m68k_0321a2_end:
.org 0x321A6
m68k_0321a6:
        move.w (%a0)+,%d0
m68k_0321a6_end:
.org 0x321A8
m68k_0321a8:
        bmi.w (. + 102)
m68k_0321a8_end:
.org 0x321AC
m68k_0321ac:
        andi.w #0xff,%d0
m68k_0321ac_end:
.org 0x321B0
m68k_0321b0:
        clr.w %d1
m68k_0321b0_end:
.org 0x321B2
m68k_0321b2:
        move.b (%a2, %d0.w),%d2
m68k_0321b2_end:
.org 0x321B6
m68k_0321b6:
        cmpi.b #0x5,%d2
m68k_0321b6_end:
.org 0x321BA
m68k_0321ba:
        bcs.w (. + 36)
m68k_0321ba_end:
.org 0x321BE
m68k_0321be:
        addq.w #0x1,%d1
m68k_0321be_end:
.org 0x321C0
m68k_0321c0:
        cmpi.b #0xa,%d2
m68k_0321c0_end:
.org 0x321C4
m68k_0321c4:
        bcs.w (. + 26)
m68k_0321c4_end:
.org 0x321DE
m68k_0321de:
        move.b (%a0, %d0.w),%d2
m68k_0321de_end:
.org 0x321E2
m68k_0321e2:
        andi.w #0x7,%d2
m68k_0321e2_end:
.org 0x321E6
m68k_0321e6:
        cmp.b %d1,%d2
m68k_0321e6_end:
.org 0x321E8
m68k_0321e8:
        bcc.b (. + -66)
m68k_0321e8_end:
.org 0x321EA
m68k_0321ea:
        move.w %d0,%d2
m68k_0321ea_end:
.org 0x321EC
m68k_0321ec:
        lsl.w #0x1,%d2
m68k_0321ec_end:
.org 0x321EE
m68k_0321ee:
        move.w (%a3, %d2.w),%d3
m68k_0321ee_end:
.org 0x321F2
m68k_0321f2:
        cmp.w (%a4, %d2.w),%d3
m68k_0321f2_end:
.org 0x321F6
m68k_0321f6:
        bcc.w (. + 8)
m68k_0321f6_end:
.org 0x321FE
m68k_0321fe:
        move.b (%a1, %d0.w),%d2
m68k_0321fe_end:
.org 0x32202
m68k_032202:
        andi.b #0x10,%d2
m68k_032202_end:
.org 0x32206
m68k_032206:
        or.b %d1,%d2
m68k_032206_end:
.org 0x32208
m68k_032208:
        move.b %d2,(%a1, %d0.w)
m68k_032208_end:
.org 0x3220C
m68k_03220c:
        bra.b (. + -102)
m68k_03220c_end:
.org 0x3220E
m68k_03220e:
        rts
m68k_03220e_end:
.org 0x32210
m68k_032210:
        bsr.w (. + 80)
m68k_032210_end:
.org 0x32214
m68k_032214:
        tst.w %d1
m68k_032214_end:
.org 0x32216
m68k_032216:
        bmi.w (. + 66)
m68k_032216_end:
.org 0x3221A
m68k_03221a:
        move.w %d1,0xf3a6:w
m68k_03221a_end:
.org 0x3221E
m68k_03221e:
        bsr.w (. + 126)
m68k_03221e_end:
.org 0x32222
m68k_032222:
        tst.l 0xf39e:w
m68k_032222_end:
.org 0x32226
m68k_032226:
        beq.w (. + 50)
m68k_032226_end:
.org 0x3222A
m68k_03222a:
        lea.l 0xcd00:w,%a0
m68k_03222a_end:
.org 0x3222E
m68k_03222e:
        move.w 0xf3a6:w,%d0
m68k_03222e_end:
.org 0x32232
m68k_032232:
        move.b #0x1,(%a0, %d0.w)
m68k_032232_end:
.org 0x32238
m68k_032238:
        bsr.w (. + -408)
m68k_032238_end:
.org 0x3223C
m68k_03223c:
        lea.l 0xe80c:w,%a0
m68k_03223c_end:
.org 0x32240
m68k_032240:
        move.w 0xf364:w,%d0
m68k_032240_end:
.org 0x32244
m68k_032244:
        lsl.w #0x1,%d0
m68k_032244_end:
.org 0x32246
m68k_032246:
        add.w 0xf364:w,%d0
m68k_032246_end:
.org 0x3224A
m68k_03224a:
        lsl.w #0x2,%d0
m68k_03224a_end:
.org 0x3224C
m68k_03224c:
        move.w 0xf3a6:w,0x4(%a0, %d0.w)
m68k_03224c_end:
.org 0x32252
m68k_032252:
        move.w 0xf3a0:w,0x6(%a0, %d0.w)
m68k_032252_end:
.org 0x32258
m68k_032258:
        move.w #0x6,0xf728:w
m68k_032258_end:
.org 0x3225E
m68k_03225e:
        rts
m68k_03225e_end:
.org 0x32260
m68k_032260:
        lea.l 0xf72a:w,%a0
m68k_032260_end:
.org 0x32264
m68k_032264:
        lea.l 0xb600:w,%a1
m68k_032264_end:
.org 0x32268
m68k_032268:
        lea.l 0xc200:w,%a2
m68k_032268_end:
.org 0x3226C
m68k_03226c:
        clr.w %d0
m68k_03226c_end:
.org 0x3226E
m68k_03226e:
        move.w #0xffff,%d1
m68k_03226e_end:
.org 0x32272
m68k_032272:
        move.w (%a0)+,%d2
m68k_032272_end:
.org 0x32274
m68k_032274:
        bmi.w (. + 38)
m68k_032274_end:
.org 0x32278
m68k_032278:
        btst.l #0xe,%d2
m68k_032278_end:
.org 0x3227C
m68k_03227c:
        bne.b (. + -10)
m68k_03227c_end:
.org 0x3227E
m68k_03227e:
        andi.w #0xff,%d2
m68k_03227e_end:
.org 0x32282
m68k_032282:
        clr.w %d4
m68k_032282_end:
.org 0x32284
m68k_032284:
        move.b (%a2, %d2.w),%d4
m68k_032284_end:
.org 0x32288
m68k_032288:
        move.w %d2,%d3
m68k_032288_end:
.org 0x3228A
m68k_03228a:
        lsl.w #0x1,%d3
m68k_03228a_end:
.org 0x3228C
m68k_03228c:
        add.w (%a1, %d3.w),%d4
m68k_03228c_end:
.org 0x32290
m68k_032290:
        cmp.w %d0,%d4
m68k_032290_end:
.org 0x32292
m68k_032292:
        bls.b (. + -32)
m68k_032292_end:
.org 0x32294
m68k_032294:
        move.w %d4,%d0
m68k_032294_end:
.org 0x32296
m68k_032296:
        move.w %d2,%d1
m68k_032296_end:
.org 0x32298
m68k_032298:
        bra.b (. + -38)
m68k_032298_end:
.org 0x3229A
m68k_03229a:
        rts
m68k_03229a_end:
.org 0x3229C
m68k_03229c:
        jsr 0x83d4:l
m68k_03229c_end:
.org 0x322A2
m68k_0322a2:
        andi.l #0xffff,%d0
m68k_0322a2_end:
.org 0x322A8
m68k_0322a8:
        move.l %d0,%d1
m68k_0322a8_end:
.org 0x322AA
m68k_0322aa:
        lsl.l #0x2,%d0
m68k_0322aa_end:
.org 0x322AC
m68k_0322ac:
        add.l %d1,%d0
m68k_0322ac_end:
.org 0x322AE
m68k_0322ae:
        lsl.l #0x2,%d0
m68k_0322ae_end:
.org 0x322B0
m68k_0322b0:
        add.l %d1,%d0
m68k_0322b0_end:
.org 0x322B2
m68k_0322b2:
        swap %d0
m68k_0322b2_end:
.org 0x322B4
m68k_0322b4:
        addi.w #0x14,%d0
m68k_0322b4_end:
.org 0x322B8
m68k_0322b8:
        lea.l 0xdffc:w,%a0
m68k_0322b8_end:
.org 0x322BC
m68k_0322bc:
        move.w 0xf364:w,%d1
m68k_0322bc_end:
.org 0x322C0
m68k_0322c0:
        lsl.w #0x2,%d1
m68k_0322c0_end:
.org 0x322C2
m68k_0322c2:
        move.l (%a0, %d1.w),%d1
m68k_0322c2_end:
.org 0x322C6
m68k_0322c6:
        move.w %d1,%d2
m68k_0322c6_end:
.org 0x322C8
m68k_0322c8:
        mulu.w %d0,%d2
m68k_0322c8_end:
.org 0x322CA
m68k_0322ca:
        swap %d1
m68k_0322ca_end:
.org 0x322CC
m68k_0322cc:
        mulu.w %d0,%d1
m68k_0322cc_end:
.org 0x322CE
m68k_0322ce:
        swap %d1
m68k_0322ce_end:
.org 0x322D0
m68k_0322d0:
        add.l %d2,%d1
m68k_0322d0_end:
.org 0x322D2
m68k_0322d2:
        moveq #100,%d2
m68k_0322d2_end:
.org 0x322D4
m68k_0322d4:
        jsr 0x35760:l
m68k_0322d4_end:
.org 0x322DA
m68k_0322da:
        cmpi.l #0x270f,%d1
m68k_0322da_end:
.org 0x322E0
m68k_0322e0:
        bls.w (. + 10)
m68k_0322e0_end:
.org 0x322E4
m68k_0322e4:
        move.l #0x270f,%d1
m68k_0322e4_end:
.org 0x322EA
m68k_0322ea:
        move.l %d1,0xf39e:w
m68k_0322ea_end:
.org 0x322EE
m68k_0322ee:
        rts
m68k_0322ee_end:
.org 0x322F0
m68k_0322f0:
        bsr.w (. + 80)
m68k_0322f0_end:
.org 0x322F4
m68k_0322f4:
        tst.w %d1
m68k_0322f4_end:
.org 0x322F6
m68k_0322f6:
        bmi.w (. + 66)
m68k_0322f6_end:
.org 0x322FA
m68k_0322fa:
        move.w %d1,0xf3a6:w
m68k_0322fa_end:
.org 0x322FE
m68k_0322fe:
        bsr.w (. + 112)
m68k_0322fe_end:
.org 0x32302
m68k_032302:
        tst.l 0xf39e:w
m68k_032302_end:
.org 0x32306
m68k_032306:
        beq.w (. + 50)
m68k_032306_end:
.org 0x3230A
m68k_03230a:
        lea.l 0xcd00:w,%a0
m68k_03230a_end:
.org 0x3230E
m68k_03230e:
        move.w 0xf3a6:w,%d0
m68k_03230e_end:
.org 0x32312
m68k_032312:
        move.b #0x1,(%a0, %d0.w)
m68k_032312_end:
.org 0x32318
m68k_032318:
        bsr.w (. + -632)
m68k_032318_end:
.org 0x3231C
m68k_03231c:
        lea.l 0xe80c:w,%a0
m68k_03231c_end:
.org 0x32320
m68k_032320:
        move.w 0xf364:w,%d0
m68k_032320_end:
.org 0x32324
m68k_032324:
        lsl.w #0x1,%d0
m68k_032324_end:
.org 0x32326
m68k_032326:
        add.w 0xf364:w,%d0
m68k_032326_end:
.org 0x3232A
m68k_03232a:
        lsl.w #0x2,%d0
m68k_03232a_end:
.org 0x3232C
m68k_03232c:
        move.w 0xf3a6:w,(%a0, %d0.w)
m68k_03232c_end:
.org 0x32332
m68k_032332:
        move.w 0xf3a0:w,0x2(%a0, %d0.w)
m68k_032332_end:
.org 0x32338
m68k_032338:
        move.w #0x7,0xf728:w
m68k_032338_end:
.org 0x3233E
m68k_03233e:
        rts
m68k_03233e_end:
.org 0x32340
m68k_032340:
        lea.l 0xf72a:w,%a0
m68k_032340_end:
.org 0x32344
m68k_032344:
        lea.l 0xb600:w,%a1
m68k_032344_end:
.org 0x32348
m68k_032348:
        clr.w %d0
m68k_032348_end:
.org 0x3234A
m68k_03234a:
        move.w #0xffff,%d1
m68k_03234a_end:
.org 0x3234E
m68k_03234e:
        move.w (%a0)+,%d2
m68k_03234e_end:
.org 0x32350
m68k_032350:
        bmi.w (. + 28)
m68k_032350_end:
.org 0x32354
m68k_032354:
        btst.l #0xe,%d2
m68k_032354_end:
.org 0x32358
m68k_032358:
        bne.b (. + -10)
m68k_032358_end:
.org 0x3235A
m68k_03235a:
        move.w %d2,%d3
m68k_03235a_end:
.org 0x3235C
m68k_03235c:
        lsl.w #0x1,%d3
m68k_03235c_end:
.org 0x3235E
m68k_03235e:
        move.w (%a1, %d3.w),%d4
m68k_03235e_end:
.org 0x32362
m68k_032362:
        cmp.w %d0,%d4
m68k_032362_end:
.org 0x32364
m68k_032364:
        bls.b (. + -22)
m68k_032364_end:
.org 0x32366
m68k_032366:
        move.w %d4,%d0
m68k_032366_end:
.org 0x32368
m68k_032368:
        move.w %d2,%d1
m68k_032368_end:
.org 0x3236A
m68k_03236a:
        bra.b (. + -28)
m68k_03236a_end:
.org 0x3236C
m68k_03236c:
        rts
m68k_03236c_end:
.org 0x3236E
m68k_03236e:
        jsr 0x83d4:l
m68k_03236e_end:
.org 0x32374
m68k_032374:
        andi.l #0xffff,%d0
m68k_032374_end:
.org 0x3237A
m68k_03237a:
        move.l %d0,%d1
m68k_03237a_end:
.org 0x3237C
m68k_03237c:
        lsl.l #0x2,%d0
m68k_03237c_end:
.org 0x3237E
m68k_03237e:
        add.l %d1,%d0
m68k_03237e_end:
.org 0x32380
m68k_032380:
        lsl.l #0x2,%d0
m68k_032380_end:
.org 0x32382
m68k_032382:
        add.l %d1,%d0
m68k_032382_end:
.org 0x32384
m68k_032384:
        swap %d0
m68k_032384_end:
.org 0x32386
m68k_032386:
        addi.w #0x1e,%d0
m68k_032386_end:
.org 0x3238A
m68k_03238a:
        lea.l 0xdffc:w,%a0
m68k_03238a_end:
.org 0x3238E
m68k_03238e:
        move.w 0xf364:w,%d0
m68k_03238e_end:
.org 0x32392
m68k_032392:
        lsl.w #0x2,%d0
m68k_032392_end:
.org 0x32394
m68k_032394:
        move.l (%a0, %d0.w),%d1
m68k_032394_end:
.org 0x32398
m68k_032398:
        move.w %d1,%d2
m68k_032398_end:
.org 0x3239A
m68k_03239a:
        mulu.w %d0,%d2
m68k_03239a_end:
.org 0x3239C
m68k_03239c:
        swap %d1
m68k_03239c_end:
.org 0x3239E
m68k_03239e:
        mulu.w %d0,%d1
m68k_03239e_end:
.org 0x323A0
m68k_0323a0:
        swap %d1
m68k_0323a0_end:
.org 0x323A2
m68k_0323a2:
        add.l %d2,%d1
m68k_0323a2_end:
.org 0x323A4
m68k_0323a4:
        moveq #100,%d2
m68k_0323a4_end:
.org 0x323A6
m68k_0323a6:
        jsr 0x35760:l
m68k_0323a6_end:
.org 0x323AC
m68k_0323ac:
        cmpi.l #0x270f,%d1
m68k_0323ac_end:
.org 0x323B2
m68k_0323b2:
        bls.w (. + 10)
m68k_0323b2_end:
.org 0x323B6
m68k_0323b6:
        move.l #0x270f,%d1
m68k_0323b6_end:
.org 0x323BC
m68k_0323bc:
        move.l %d1,0xf39e:w
m68k_0323bc_end:
.org 0x323C0
m68k_0323c0:
        rts
m68k_0323c0_end:
.org 0x323C2
m68k_0323c2:
        lea.l 0xcdfc:w,%a0
m68k_0323c2_end:
.org 0x323C6
m68k_0323c6:
        move.w 0xf364:w,%d0
m68k_0323c6_end:
.org 0x323CA
m68k_0323ca:
        lsl.w #0x2,%d0
m68k_0323ca_end:
.org 0x323CC
m68k_0323cc:
        tst.b (%a0, %d0.w)
m68k_0323cc_end:
.org 0x323D0
m68k_0323d0:
        bne.w (. + 44)
m68k_0323d0_end:
.org 0x323D4
m68k_0323d4:
        bsr.w (. + 48)
m68k_0323d4_end:
.org 0x323D8
m68k_0323d8:
        tst.w %d0
m68k_0323d8_end:
.org 0x323DA
m68k_0323da:
        bmi.w (. + 34)
m68k_0323da_end:
.org 0x323DE
m68k_0323de:
        move.w %d0,0xf688:w
m68k_0323de_end:
.org 0x323E2
m68k_0323e2:
        bsr.w (. + 104)
m68k_0323e2_end:
.org 0x323E6
m68k_0323e6:
        tst.w %d4
m68k_0323e6_end:
.org 0x323E8
m68k_0323e8:
        bmi.w (. + 20)
m68k_0323e8_end:
.org 0x323EC
m68k_0323ec:
        move.w %d4,0xf392:w
m68k_0323ec_end:
.org 0x323F0
m68k_0323f0:
        move.w 0xf364:w,0xf3a8:w
m68k_0323f0_end:
.org 0x323F6
m68k_0323f6:
        jsr 0xe7b0:l
m68k_0323f6_end:
.org 0x323FC
m68k_0323fc:
        move.w #0xe,0xf728:w
m68k_0323fc_end:
.org 0x32402
m68k_032402:
        rts
m68k_032402_end:
.org 0x32404
m68k_032404:
        move.w #0xffff,%d0
m68k_032404_end:
.org 0x32408
m68k_032408:
        lea.l 0xdffc:w,%a0
m68k_032408_end:
.org 0x3240C
m68k_03240c:
        lea.l 0xe09c:w,%a1
m68k_03240c_end:
.org 0x32410
m68k_032410:
        move.w 0xf364:w,%d1
m68k_032410_end:
.org 0x32414
m68k_032414:
        lsl.w #0x2,%d1
m68k_032414_end:
.org 0x32416
m68k_032416:
        cmpi.l #0x4e20,(%a0, %d1.w)
m68k_032416_end:
.org 0x3241E
m68k_03241e:
        bcs.w (. + 26)
m68k_03241e_end:
.org 0x32422
m68k_032422:
        clr.w %d0
m68k_032422_end:
.org 0x32424
m68k_032424:
        cmpi.l #0x4e20,(%a1, %d1.w)
m68k_032424_end:
.org 0x3242C
m68k_03242c:
        bcs.w (. + 28)
m68k_03242c_end:
.org 0x32430
m68k_032430:
        move.w #0x2,%d0
m68k_032430_end:
.org 0x32434
m68k_032434:
        bra.w (. + 20)
m68k_032434_end:
.org 0x32438
m68k_032438:
        cmpi.l #0x4e20,(%a1, %d1.w)
m68k_032438_end:
.org 0x32440
m68k_032440:
        bcs.w (. + 8)
m68k_032440_end:
.org 0x32444
m68k_032444:
        move.w #0x1,%d0
m68k_032444_end:
.org 0x32448
m68k_032448:
        rts
m68k_032448_end:
.org 0x3244A
m68k_03244a:
        move.w 0xf376:w,%d0
m68k_03244a_end:
.org 0x3244E
m68k_03244e:
        move.w 0xf364:w,%d1
m68k_03244e_end:
.org 0x32452
m68k_032452:
        lea.l 0xc800:w,%a0
m68k_032452_end:
.org 0x32456
m68k_032456:
        lea.l 0xdffc:w,%a1
m68k_032456_end:
.org 0x3245A
m68k_03245a:
        lea.l 0xe09c:w,%a2
m68k_03245a_end:
.org 0x3245E
m68k_03245e:
        lea.l 0xea37:w,%a4
m68k_03245e_end:
.org 0x32462
m68k_032462:
        moveq #-1,%d2
m68k_032462_end:
.org 0x32464
m68k_032464:
        move.w #0xffff,%d4
m68k_032464_end:
.org 0x32468
m68k_032468:
        lea.l 0xf450:w,%a3
m68k_032468_end:
.org 0x3246C
m68k_03246c:
        move.w #0x28,%d3
m68k_03246c_end:
.org 0x32470
m68k_032470:
        cmp.b -(%a3),%d0
m68k_032470_end:
.org 0x32472
m68k_032472:
        bne.w (. + 52)
m68k_032472_end:
.org 0x32476
m68k_032476:
        tst.b (%a4, %d3.w)
m68k_032476_end:
.org 0x3247A
m68k_03247a:
        bne.w (. + 44)
m68k_03247a_end:
.org 0x3247E
m68k_03247e:
        cmp.w %d1,%d3
m68k_03247e_end:
.org 0x32480
m68k_032480:
        beq.w (. + 38)
m68k_032480_end:
.org 0x32484
m68k_032484:
        bsr.w (. + 40)
m68k_032484_end:
.org 0x32488
m68k_032488:
        move.w %d3,%d5
m68k_032488_end:
.org 0x3248A
m68k_03248a:
        lsl.w #0x2,%d5
m68k_03248a_end:
.org 0x3248C
m68k_03248c:
        cmp.l (%a2, %d5.w),%d6
m68k_03248c_end:
.org 0x32490
m68k_032490:
        bls.w (. + 22)
m68k_032490_end:
.org 0x32494
m68k_032494:
        move.l (%a1, %d5.w),%d7
m68k_032494_end:
.org 0x32498
m68k_032498:
        add.l (%a2, %d5.w),%d7
m68k_032498_end:
.org 0x3249C
m68k_03249c:
        cmp.l %d2,%d7
m68k_03249c_end:
.org 0x3249E
m68k_03249e:
        bcc.w (. + 8)
m68k_03249e_end:
.org 0x324A2
m68k_0324a2:
        move.l %d7,%d2
m68k_0324a2_end:
.org 0x324A4
m68k_0324a4:
        move.w %d3,%d4
m68k_0324a4_end:
.org 0x324A6
m68k_0324a6:
        subq.w #0x1,%d3
m68k_0324a6_end:
.org 0x324A8
m68k_0324a8:
        bne.b (. + -56)
m68k_0324a8_end:
.org 0x324AA
m68k_0324aa:
        rts
m68k_0324aa_end:
.org 0x324AC
m68k_0324ac:
        movem.l %d4,-(%a7)
m68k_0324ac_end:
.org 0x324B0
m68k_0324b0:
        lea.l 0xcd00:w,%a4
m68k_0324b0_end:
.org 0x324B4
m68k_0324b4:
        move.w #0xff,%d5
m68k_0324b4_end:
.org 0x324B8
m68k_0324b8:
        moveq #0,%d6
m68k_0324b8_end:
.org 0x324BA
m68k_0324ba:
        move.b -(%a4),%d7
m68k_0324ba_end:
.org 0x324BC
m68k_0324bc:
        andi.w #0x3f,%d7
m68k_0324bc_end:
.org 0x324C0
m68k_0324c0:
        cmp.w %d3,%d7
m68k_0324c0_end:
.org 0x324C2
m68k_0324c2:
        bne.w (. + 18)
m68k_0324c2_end:
.org 0x324C6
m68k_0324c6:
        move.w %d5,%d4
m68k_0324c6_end:
.org 0x324C8
m68k_0324c8:
        lsl.w #0x2,%d4
m68k_0324c8_end:
.org 0x324CA
m68k_0324ca:
        add.l (%a0, %d4.w),%d6
m68k_0324ca_end:
.org 0x324CE
m68k_0324ce:
        addi.l #0x64,%d6
m68k_0324ce_end:
.org 0x324D4
m68k_0324d4:
        dbra %d5,(. + -26)
m68k_0324d4_end:
.org 0x324D8
m68k_0324d8:
        divu.w #0xa,%d6
m68k_0324d8_end:
.org 0x324DC
m68k_0324dc:
        andi.l #0xffff,%d6
m68k_0324dc_end:
.org 0x324E2
m68k_0324e2:
        move.l %d6,%d4
m68k_0324e2_end:
.org 0x324E4
m68k_0324e4:
        lsl.l #0x3,%d6
m68k_0324e4_end:
.org 0x324E6
m68k_0324e6:
        add.l %d4,%d6
m68k_0324e6_end:
.org 0x324E8
m68k_0324e8:
        movem.l (%a7)+,%d4
m68k_0324e8_end:
.org 0x324EC
m68k_0324ec:
        rts
m68k_0324ec_end:
.org 0x324EE
m68k_0324ee:
        bsr.w (. + 12)
m68k_0324ee_end:
.org 0x324F2
m68k_0324f2:
        move.w #0xf,0xf728:w
m68k_0324f2_end:
.org 0x324F8
m68k_0324f8:
        rts
m68k_0324f8_end:
.org 0x324FA
m68k_0324fa:
        jsr 0x83d4:l
m68k_0324fa_end:
.org 0x32500
m68k_032500:
        lea.l 0x311fc:l,%a0
m68k_032500_end:
.org 0x32506
m68k_032506:
        move.w 0xf376:w,%d0
m68k_032506_end:
.org 0x3250A
m68k_03250a:
        lsl.w #0x2,%d0
m68k_03250a_end:
.org 0x3250C
m68k_03250c:
        move.w (%a0, %d0.w),%d1
m68k_03250c_end:
.org 0x32510
m68k_032510:
        subq.w #0x5,%d1
m68k_032510_end:
.org 0x32512
m68k_032512:
        cmpi.w #0x3,%d1
m68k_032512_end:
.org 0x32516
m68k_032516:
        bls.w (. + 8)
m68k_032516_end:
.org 0x3251A
m68k_03251a:
        move.w #0x3,%d1
m68k_03251a_end:
.org 0x3251E
m68k_03251e:
        move.w %d1,%d2
m68k_03251e_end:
.org 0x32520
m68k_032520:
        lsl.w #0x2,%d1
m68k_032520_end:
.org 0x32522
m68k_032522:
        add.w %d2,%d1
m68k_032522_end:
.org 0x32524
m68k_032524:
        move.w #0x37,%d2
m68k_032524_end:
.org 0x32528
m68k_032528:
        sub.w %d1,%d2
m68k_032528_end:
.org 0x3252A
m68k_03252a:
        moveq #0,%d0
m68k_03252a_end:
.org 0x3252C
m68k_03252c:
        move.w 0xf61c:w,%d0
m68k_03252c_end:
.org 0x32530
m68k_032530:
        move.l %d0,%d1
m68k_032530_end:
.org 0x32532
m68k_032532:
        lsl.l #0x2,%d0
m68k_032532_end:
.org 0x32534
m68k_032534:
        add.l %d1,%d0
m68k_032534_end:
.org 0x32536
m68k_032536:
        lsl.l #0x1,%d0
m68k_032536_end:
.org 0x32538
m68k_032538:
        swap %d0
m68k_032538_end:
.org 0x3253A
m68k_03253a:
        add.w %d0,%d2
m68k_03253a_end:
.org 0x3253C
m68k_03253c:
        lea.l 0xe3bc:w,%a0
m68k_03253c_end:
.org 0x32540
m68k_032540:
        lea.l 0xe31c:w,%a1
m68k_032540_end:
.org 0x32544
m68k_032544:
        move.w 0xf364:w,%d0
m68k_032544_end:
.org 0x32548
m68k_032548:
        lsl.w #0x2,%d0
m68k_032548_end:
.org 0x3254A
m68k_03254a:
        cmpi.l #0x28,(%a1, %d0.w)
m68k_03254a_end:
.org 0x32552
m68k_032552:
        bcc.w (. + 8)
m68k_032552_end:
.org 0x3255A
m68k_03255a:
        ext.l %d2
m68k_03255a_end:
.org 0x3255C
m68k_03255c:
        move.l %d2,(%a0, %d0.w)
m68k_03255c_end:
.org 0x32560
m68k_032560:
        rts
m68k_032560_end:
.org 0x32562
m68k_032562:
        move.w #0xffff,0xf728:w
m68k_032562_end:
.org 0x32568
m68k_032568:
        rts
m68k_032568_end:
.org 0x3256A
m68k_03256a:
        move.w 0xf728:w,%d0
m68k_03256a_end:
.org 0x3256E
m68k_03256e:
        bmi.w (. + 18)
m68k_03256e_end:
.org 0x32572
m68k_032572:
        subq.w #0x1,%d0
m68k_032572_end:
.org 0x32574
m68k_032574:
        lsl.w #0x1,%d0
m68k_032574_end:
.org 0x32576
m68k_032576:
        move.w 10(%pc, %d0.w),%d0
m68k_032576_end:
.org 0x3257A
m68k_03257a:
        jsr 22(%pc, %d0.w)
m68k_03257a_end:
.org 0x3257E
m68k_03257e:
        bra.b (. + -20)
m68k_03257e_end:
.org 0x32580
m68k_032580:
        rts
m68k_032580_end:
.org 0x32DCE
m68k_032dce:
        move.w 0xe730:w,%d0
m68k_032dce_end:
.org 0x32DD2
m68k_032dd2:
        cmp.w 0xf67a:w,%d0
m68k_032dd2_end:
.org 0x32DD6
m68k_032dd6:
        beq.w (. + 136)
m68k_032dd6_end:
.org 0x32DDA
m68k_032dda:
        cmp.w 0xf67c:w,%d0
m68k_032dda_end:
.org 0x32DDE
m68k_032dde:
        beq.w (. + 128)
m68k_032dde_end:
.org 0x32DE2
m68k_032de2:
        cmp.w 0xf67e:w,%d0
m68k_032de2_end:
.org 0x32DE6
m68k_032de6:
        beq.w (. + 120)
m68k_032de6_end:
.org 0x32DEA
m68k_032dea:
        bsr.w (. + 136)
m68k_032dea_end:
.org 0x32DEE
m68k_032dee:
        move.w %d1,0xf3a6:w
m68k_032dee_end:
.org 0x32DF2
m68k_032df2:
        bmi.w (. + 120)
m68k_032df2_end:
.org 0x32DF6
m68k_032df6:
        move.w 0xf364:w,0xf392:w
m68k_032df6_end:
.org 0x32DFC
m68k_032dfc:
        jsr 0xea38:l
m68k_032dfc_end:
.org 0x32E02
m68k_032e02:
        lea.l 0xcd00:w,%a0
m68k_032e02_end:
.org 0x32E06
m68k_032e06:
        move.w 0xf3a6:w,%d0
m68k_032e06_end:
.org 0x32E0A
m68k_032e0a:
        move.b #0x1,(%a0, %d0.w)
m68k_032e0a_end:
.org 0x32E10
m68k_032e10:
        bsr.w (. + -3440)
m68k_032e10_end:
.org 0x32E14
m68k_032e14:
        lea.l 0xe710:w,%a0
m68k_032e14_end:
.org 0x32E18
m68k_032e18:
        move.w 0xf376:w,%d0
m68k_032e18_end:
.org 0x32E1C
m68k_032e1c:
        lsl.w #0x1,%d0
m68k_032e1c_end:
.org 0x32E1E
m68k_032e1e:
        move.w (%a0, %d0.w),%d0
m68k_032e1e_end:
.org 0x32E22
m68k_032e22:
        move.w 0xe730:w,%d1
m68k_032e22_end:
.org 0x32E26
m68k_032e26:
        btst.l %d1,%d0
m68k_032e26_end:
.org 0x32E28
m68k_032e28:
        beq.w (. + 66)
m68k_032e28_end:
.org 0x32E2C
m68k_032e2c:
        lea.l 0xe640:w,%a0
m68k_032e2c_end:
.org 0x32E30
m68k_032e30:
        move.w 0xf376:w,%d0
m68k_032e30_end:
.org 0x32E34
m68k_032e34:
        lsl.w #0x1,%d0
m68k_032e34_end:
.org 0x32E36
m68k_032e36:
        move.w (%a0, %d0.w),%d0
m68k_032e36_end:
.org 0x32E3A
m68k_032e3a:
        move.w %d0,0xf3d0:w
m68k_032e3a_end:
.org 0x32E3E
m68k_032e3e:
        move.w 0xe730:w,%d0
m68k_032e3e_end:
.org 0x32E42
m68k_032e42:
        lsl.w #0x1,%d0
m68k_032e42_end:
.org 0x32E44
m68k_032e44:
        move.w (%a0, %d0.w),%d0
m68k_032e44_end:
.org 0x32E48
m68k_032e48:
        move.w %d0,0xf3d2:w
m68k_032e48_end:
.org 0x32E4C
m68k_032e4c:
        move.w #0xa3,0xf740:w
m68k_032e4c_end:
.org 0x32E52
m68k_032e52:
        clr.w 0xf362:w
m68k_032e52_end:
.org 0x32E56
m68k_032e56:
        bsr.w (. + -9186)
m68k_032e56_end:
.org 0x32E5A
m68k_032e5a:
        bra.w (. + 16)
m68k_032e5a_end:
.org 0x32E5E
m68k_032e5e:
        bsr.w (. + 66)
m68k_032e5e_end:
.org 0x32E62
m68k_032e62:
        bcs.w (. + 8)
m68k_032e62_end:
.org 0x32E66
m68k_032e66:
        bsr.w (. + 352)
m68k_032e66_end:
.org 0x32E6A
m68k_032e6a:
        move.w #0x2,0xf728:w
m68k_032e6a_end:
.org 0x32E70
m68k_032e70:
        rts
m68k_032e70_end:
.org 0x32E72
m68k_032e72:
        lea.l 0xf72a:w,%a0
m68k_032e72_end:
.org 0x32E76
m68k_032e76:
        lea.l 0xb600:w,%a1
m68k_032e76_end:
.org 0x32E7A
m68k_032e7a:
        clr.w %d0
m68k_032e7a_end:
.org 0x32E7C
m68k_032e7c:
        move.w #0xffff,%d1
m68k_032e7c_end:
.org 0x32E80
m68k_032e80:
        move.w (%a0)+,%d2
m68k_032e80_end:
.org 0x32E82
m68k_032e82:
        bmi.w (. + 28)
m68k_032e82_end:
.org 0x32E86
m68k_032e86:
        btst.l #0xe,%d2
m68k_032e86_end:
.org 0x32E8A
m68k_032e8a:
        bne.b (. + -10)
m68k_032e8a_end:
.org 0x32E8C
m68k_032e8c:
        move.w %d2,%d3
m68k_032e8c_end:
.org 0x32E8E
m68k_032e8e:
        lsl.w #0x1,%d3
m68k_032e8e_end:
.org 0x32E90
m68k_032e90:
        move.w (%a1, %d3.w),%d3
m68k_032e90_end:
.org 0x32E94
m68k_032e94:
        cmp.w %d0,%d3
m68k_032e94_end:
.org 0x32E96
m68k_032e96:
        bls.b (. + -22)
m68k_032e96_end:
.org 0x32E98
m68k_032e98:
        move.w %d3,%d0
m68k_032e98_end:
.org 0x32E9A
m68k_032e9a:
        move.w %d2,%d1
m68k_032e9a_end:
.org 0x32E9C
m68k_032e9c:
        bra.b (. + -28)
m68k_032e9c_end:
.org 0x32E9E
m68k_032e9e:
        rts
m68k_032e9e_end:
.org 0x32EA0
m68k_032ea0:
        jsr 0x83d4:l
m68k_032ea0_end:
.org 0x32EA6
m68k_032ea6:
        move.w 0xf364:w,%d0
m68k_032ea6_end:
.org 0x32EAA
m68k_032eaa:
        lsl.w #0x2,%d0
m68k_032eaa_end:
.org 0x32EAC
m68k_032eac:
        lea.l 0xdffc:w,%a0
m68k_032eac_end:
.org 0x32EB0
m68k_032eb0:
        lea.l 0xe09c:w,%a1
m68k_032eb0_end:
.org 0x32EB4
m68k_032eb4:
        clr.w %d2
m68k_032eb4_end:
.org 0x32EB6
m68k_032eb6:
        move.l (%a0, %d0.w),%d1
m68k_032eb6_end:
.org 0x32EBA
m68k_032eba:
        cmp.l (%a1, %d0.w),%d1
m68k_032eba_end:
.org 0x32EBE
m68k_032ebe:
        bcc.w (. + 10)
m68k_032ebe_end:
.org 0x32EC2
m68k_032ec2:
        move.l (%a1, %d0.w),%d1
m68k_032ec2_end:
.org 0x32EC6
m68k_032ec6:
        addq.w #0x1,%d2
m68k_032ec6_end:
.org 0x32EC8
m68k_032ec8:
        cmpi.l #0x1388,%d1
m68k_032ec8_end:
.org 0x32ECE
m68k_032ece:
        bcc.w (. + 90)
m68k_032ece_end:
.org 0x32ED2
m68k_032ed2:
        bsr.b (. + -96)
m68k_032ed2_end:
.org 0x32ED4
m68k_032ed4:
        tst.w %d1
m68k_032ed4_end:
.org 0x32ED6
m68k_032ed6:
        bmi.w (. + 234)
m68k_032ed6_end:
.org 0x32EDA
m68k_032eda:
        move.w 0xf376:w,%d0
m68k_032eda_end:
.org 0x32EDE
m68k_032ede:
        lsl.w #0x1,%d0
m68k_032ede_end:
.org 0x32EE0
m68k_032ee0:
        lea.l 0xe640:w,%a0
m68k_032ee0_end:
.org 0x32EE4
m68k_032ee4:
        move.w (%a0, %d0.w),%d0
m68k_032ee4_end:
.org 0x32EE8
m68k_032ee8:
        move.w %d0,0xf3d0:w
m68k_032ee8_end:
.org 0x32EEC
m68k_032eec:
        move.w 0xf376:w,-(%a7)
m68k_032eec_end:
.org 0x32EF0
m68k_032ef0:
        move.w #0x81,0xf740:w
m68k_032ef0_end:
.org 0x32EF6
m68k_032ef6:
        move.w 0xe730:w,0xf376:w
m68k_032ef6_end:
.org 0x32EFC
m68k_032efc:
        clr.w 0xf362:w
m68k_032efc_end:
.org 0x32F00
m68k_032f00:
        bsr.w (. + -9356)
m68k_032f00_end:
.org 0x32F04
m68k_032f04:
        move.w (%a7)+,0xf376:w
m68k_032f04_end:
.org 0x32F08
m68k_032f08:
        clr.l 0xf3c8:w
m68k_032f08_end:
.org 0x32F0C
m68k_032f0c:
        move.w #0x84,0xf740:w
m68k_032f0c_end:
.org 0x32F12
m68k_032f12:
        lea.l 0xcd00:w,%a0
m68k_032f12_end:
.org 0x32F16
m68k_032f16:
        move.w 0xf3d2:w,%d0
m68k_032f16_end:
.org 0x32F1A
m68k_032f1a:
        move.b #0x1,(%a0, %d0.w)
m68k_032f1a_end:
.org 0x32F20
m68k_032f20:
        bsr.w (. + -3712)
m68k_032f20_end:
.org 0x32F24
m68k_032f24:
        bra.w (. + 148)
m68k_032f24_end:
.org 0x32F28
m68k_032f28:
        move.w 0xf376:w,%d0
m68k_032f28_end:
.org 0x32F2C
m68k_032f2c:
        lsl.w #0x1,%d0
m68k_032f2c_end:
.org 0x32F2E
m68k_032f2e:
        lea.l 0xe640:w,%a0
m68k_032f2e_end:
.org 0x32F32
m68k_032f32:
        move.w (%a0, %d0.w),%d0
m68k_032f32_end:
.org 0x32F36
m68k_032f36:
        move.w %d0,0xf3d0:w
m68k_032f36_end:
.org 0x32F3A
m68k_032f3a:
        move.w %d2,-(%a7)
m68k_032f3a_end:
.org 0x32F3C
m68k_032f3c:
        move.w 0xf376:w,-(%a7)
m68k_032f3c_end:
.org 0x32F40
m68k_032f40:
        move.w #0x81,0xf740:w
m68k_032f40_end:
.org 0x32F46
m68k_032f46:
        move.w 0xe730:w,0xf376:w
m68k_032f46_end:
.org 0x32F4C
m68k_032f4c:
        clr.w 0xf362:w
m68k_032f4c_end:
.org 0x32F50
m68k_032f50:
        bsr.w (. + -9436)
m68k_032f50_end:
.org 0x32F54
m68k_032f54:
        move.w (%a7)+,0xf376:w
m68k_032f54_end:
.org 0x32F58
m68k_032f58:
        move.w (%a7)+,%d2
m68k_032f58_end:
.org 0x32F5A
m68k_032f5a:
        moveq #0,%d1
m68k_032f5a_end:
.org 0x32F5C
m68k_032f5c:
        move.w 0xf61c:w,%d1
m68k_032f5c_end:
.org 0x32F60
m68k_032f60:
        move.l %d1,%d0
m68k_032f60_end:
.org 0x32F62
m68k_032f62:
        lsl.w #0x2,%d1
m68k_032f62_end:
.org 0x32F64
m68k_032f64:
        add.l %d0,%d1
m68k_032f64_end:
.org 0x32F66
m68k_032f66:
        lsl.l #0x2,%d1
m68k_032f66_end:
.org 0x32F68
m68k_032f68:
        add.l %d0,%d1
m68k_032f68_end:
.org 0x32F6A
m68k_032f6a:
        swap %d1
m68k_032f6a_end:
.org 0x32F6C
m68k_032f6c:
        addi.w #0xa,%d1
m68k_032f6c_end:
.org 0x32F70
m68k_032f70:
        mulu.w #0x64,%d1
m68k_032f70_end:
.org 0x32F74
m68k_032f74:
        move.w 0xf364:w,%d0
m68k_032f74_end:
.org 0x32F78
m68k_032f78:
        lsl.w #0x2,%d0
m68k_032f78_end:
.org 0x32F7A
m68k_032f7a:
        move.l %d1,0xf3c8:w
m68k_032f7a_end:
.org 0x32F7E
m68k_032f7e:
        move.w %d2,0xf742:w
m68k_032f7e_end:
.org 0x32F82
m68k_032f82:
        bne.w (. + 22)
m68k_032f82_end:
.org 0x32F86
m68k_032f86:
        lea.l 0xdffc:w,%a0
m68k_032f86_end:
.org 0x32F8A
m68k_032f8a:
        sub.l %d1,(%a0, %d0.w)
m68k_032f8a_end:
.org 0x32F8E
m68k_032f8e:
        move.w #0x82,0xf740:w
m68k_032f8e_end:
.org 0x32F94
m68k_032f94:
        bra.w (. + 18)
m68k_032f94_end:
.org 0x32F98
m68k_032f98:
        lea.l 0xe09f:w,%a0
m68k_032f98_end:
.org 0x32F9C
m68k_032f9c:
        sub.l %d1,(%a1, %d0.w)
m68k_032f9c_end:
.org 0x32FA0
m68k_032fa0:
        move.w #0x83,0xf740:w
m68k_032fa0_end:
.org 0x32FA6
m68k_032fa6:
        move.w 0xf376:w,%d0
m68k_032fa6_end:
.org 0x32FAA
m68k_032faa:
        lsl.w #0x1,%d0
m68k_032faa_end:
.org 0x32FAC
m68k_032fac:
        lea.l 0xe640:w,%a0
m68k_032fac_end:
.org 0x32FB0
m68k_032fb0:
        move.w (%a0, %d0.w),%d0
m68k_032fb0_end:
.org 0x32FB4
m68k_032fb4:
        move.w %d0,0xf3d0:w
m68k_032fb4_end:
.org 0x32FB8
m68k_032fb8:
        andi.w #0xfffe,%sr
m68k_032fb8_end:
.org 0x32FBC
m68k_032fbc:
        bra.w (. + 8)
m68k_032fbc_end:
.org 0x32FC0
m68k_032fc0:
        ori.w #0x1,%sr
m68k_032fc0_end:
.org 0x32FC4
m68k_032fc4:
        rts
m68k_032fc4_end:
.org 0x33040
m68k_033040:
        move.w 0xf728:w,%d0
m68k_033040_end:
.org 0x33044
m68k_033044:
        bmi.w (. + 18)
m68k_033044_end:
.org 0x33048
m68k_033048:
        subq.w #0x1,%d0
m68k_033048_end:
.org 0x3304A
m68k_03304a:
        lsl.w #0x1,%d0
m68k_03304a_end:
.org 0x3304C
m68k_03304c:
        move.w 10(%pc, %d0.w),%d0
m68k_03304c_end:
.org 0x33050
m68k_033050:
        jsr 28(%pc, %d0.w)
m68k_033050_end:
.org 0x33054
m68k_033054:
        bra.b (. + -20)
m68k_033054_end:
.org 0x33056
m68k_033056:
        rts
m68k_033056_end:
.org 0x3306E
m68k_03306e:
        bsr.w (. + 94)
m68k_03306e_end:
.org 0x33072
m68k_033072:
        cmpi.w #0xa,%d0
m68k_033072_end:
.org 0x33076
m68k_033076:
        bcc.w (. + 78)
m68k_033076_end:
.org 0x3307A
m68k_03307a:
        cmpi.w #0x1,%d0
m68k_03307a_end:
.org 0x3307E
m68k_03307e:
        beq.w (. + 70)
m68k_03307e_end:
.org 0x33082
m68k_033082:
        bsr.w (. + 92)
m68k_033082_end:
.org 0x33086
m68k_033086:
        tst.w %d1
m68k_033086_end:
.org 0x33088
m68k_033088:
        bmi.w (. + 60)
m68k_033088_end:
.org 0x3308C
m68k_03308c:
        move.w %d1,0xf3a6:w
m68k_03308c_end:
.org 0x33090
m68k_033090:
        move.w 0xf364:w,%d0
m68k_033090_end:
.org 0x33094
m68k_033094:
        jsr 0x1108c:l
m68k_033094_end:
.org 0x3309A
m68k_03309a:
        move.w %d0,%d7
m68k_03309a_end:
.org 0x3309C
m68k_03309c:
        beq.w (. + 40)
m68k_03309c_end:
.org 0x330C4
m68k_0330c4:
        move.w #0x2,0xf728:w
m68k_0330c4_end:
.org 0x330CA
m68k_0330ca:
        rts
m68k_0330ca_end:
.org 0x330CC
m68k_0330cc:
        lea.l 0xf72a:w,%a0
m68k_0330cc_end:
.org 0x330D0
m68k_0330d0:
        clr.w %d0
m68k_0330d0_end:
.org 0x330D2
m68k_0330d2:
        tst.w (%a0)+
m68k_0330d2_end:
.org 0x330D4
m68k_0330d4:
        bmi.w (. + 8)
m68k_0330d4_end:
.org 0x330D8
m68k_0330d8:
        addq.w #0x1,%d0
m68k_0330d8_end:
.org 0x330DA
m68k_0330da:
        bra.b (. + -8)
m68k_0330da_end:
.org 0x330DC
m68k_0330dc:
        rts
m68k_0330dc_end:
.org 0x330DE
m68k_0330de:
        lea.l 0xf72a:w,%a0
m68k_0330de_end:
.org 0x330E2
m68k_0330e2:
        lea.l 0xb600:w,%a1
m68k_0330e2_end:
.org 0x330E6
m68k_0330e6:
        clr.w %d0
m68k_0330e6_end:
.org 0x330E8
m68k_0330e8:
        move.w #0xffff,%d1
m68k_0330e8_end:
.org 0x330EC
m68k_0330ec:
        move.w (%a0)+,%d2
m68k_0330ec_end:
.org 0x330EE
m68k_0330ee:
        bmi.w (. + 22)
m68k_0330ee_end:
.org 0x330F2
m68k_0330f2:
        move.w %d2,%d3
m68k_0330f2_end:
.org 0x330F4
m68k_0330f4:
        lsl.w #0x1,%d3
m68k_0330f4_end:
.org 0x330F6
m68k_0330f6:
        move.w (%a1, %d3.w),%d3
m68k_0330f6_end:
.org 0x330FA
m68k_0330fa:
        cmp.w %d0,%d3
m68k_0330fa_end:
.org 0x330FC
m68k_0330fc:
        bls.b (. + -16)
m68k_0330fc_end:
.org 0x330FE
m68k_0330fe:
        move.w %d3,%d0
m68k_0330fe_end:
.org 0x33100
m68k_033100:
        move.w %d2,%d1
m68k_033100_end:
.org 0x33102
m68k_033102:
        bra.b (. + -22)
m68k_033102_end:
.org 0x33104
m68k_033104:
        rts
m68k_033104_end:
.org 0x33106
m68k_033106:
        move.w 0xf364:w,%d0
m68k_033106_end:
.org 0x3310A
m68k_03310a:
        move.w #0xffff,0xf630:w
m68k_03310a_end:
.org 0x33110
m68k_033110:
        jsr 0x5f48:l
m68k_033110_end:
.org 0x33116
m68k_033116:
        cmpi.w #0xa,%d3
m68k_033116_end:
.org 0x3311A
m68k_03311a:
        bcc.w (. + 62)
m68k_03311a_end:
.org 0x3311E
m68k_03311e:
        bsr.w (. + 66)
m68k_03311e_end:
.org 0x33122
m68k_033122:
        tst.w %d2
m68k_033122_end:
.org 0x33124
m68k_033124:
        bmi.w (. + 52)
m68k_033124_end:
.org 0x33158
m68k_033158:
        move.w #0x3,0xf728:w
m68k_033158_end:
.org 0x3315E
m68k_03315e:
        rts
m68k_03315e_end:
.org 0x33160
m68k_033160:
        lea.l 0xd4bda:l,%a0
m68k_033160_end:
.org 0x33166
m68k_033166:
        move.w 0xf364:w,%d0
m68k_033166_end:
.org 0x3316A
m68k_03316a:
        lsl.w #0x3,%d0
m68k_03316a_end:
.org 0x3316C
m68k_03316c:
        adda.w %d0,%a0
m68k_03316c_end:
.org 0x3316E
m68k_03316e:
        move.w 0xf376:w,%d7
m68k_03316e_end:
.org 0x33172
m68k_033172:
        lea.l 0xb400:w,%a1
m68k_033172_end:
.org 0x33176
m68k_033176:
        lea.l 0xb600:w,%a2
m68k_033176_end:
.org 0x3317A
m68k_03317a:
        lea.l 0xc300:w,%a3
m68k_03317a_end:
.org 0x3317E
m68k_03317e:
        lea.l 0xf427:w,%a5
m68k_03317e_end:
.org 0x33182
m68k_033182:
        lea.l 0xea37:w,%a6
m68k_033182_end:
.org 0x33186
m68k_033186:
        clr.w %d0
m68k_033186_end:
.org 0x33188
m68k_033188:
        clr.w %d1
m68k_033188_end:
.org 0x3318A
m68k_03318a:
        move.w #0xffff,%d2
m68k_03318a_end:
.org 0x3318E
m68k_03318e:
        move.w #0xffff,%d3
m68k_03318e_end:
.org 0x33192
m68k_033192:
        move.b (%a0)+,%d0
m68k_033192_end:
.org 0x33194
m68k_033194:
        bmi.w (. + 22)
m68k_033194_end:
.org 0x33198
m68k_033198:
        tst.b (%a6, %d0.w)
m68k_033198_end:
.org 0x3319C
m68k_03319c:
        bne.b (. + -10)
m68k_03319c_end:
.org 0x3319E
m68k_03319e:
        cmp.b (%a5, %d0.w),%d7
m68k_03319e_end:
.org 0x331A2
m68k_0331a2:
        beq.b (. + -16)
m68k_0331a2_end:
.org 0x331A4
m68k_0331a4:
        bsr.w (. + 24)
m68k_0331a4_end:
.org 0x331A8
m68k_0331a8:
        bra.b (. + -22)
m68k_0331a8_end:
.org 0x331AA
m68k_0331aa:
        move.w %d2,%d4
m68k_0331aa_end:
.org 0x331AC
m68k_0331ac:
        bmi.w (. + 14)
m68k_0331ac_end:
.org 0x331BA
m68k_0331ba:
        rts
m68k_0331ba_end:
.org 0x331BC
m68k_0331bc:
        movem.l %d7/%a5,-(%a7)
m68k_0331bc_end:
.org 0x331C0
m68k_0331c0:
        lea.l 0xf427:w,%a5
m68k_0331c0_end:
.org 0x331C4
m68k_0331c4:
        clr.w %d7
m68k_0331c4_end:
.org 0x331C6
m68k_0331c6:
        move.b (%a5, %d0.w),%d7
m68k_0331c6_end:
.org 0x331CA
m68k_0331ca:
        bmi.w (. + 74)
m68k_0331ca_end:
.org 0x331CE
m68k_0331ce:
        lsl.w #0x1,%d7
m68k_0331ce_end:
.org 0x331D0
m68k_0331d0:
        lea.l 0xe640:w,%a5
m68k_0331d0_end:
.org 0x331D4
m68k_0331d4:
        move.w (%a5, %d7.w),%d7
m68k_0331d4_end:
.org 0x331D8
m68k_0331d8:
        lea.l 0xcc00:w,%a4
m68k_0331d8_end:
.org 0x331DC
m68k_0331dc:
        move.w #0xff,%d4
m68k_0331dc_end:
.org 0x331E0
m68k_0331e0:
        cmp.b (%a4, %d4.w),%d0
m68k_0331e0_end:
.org 0x331E4
m68k_0331e4:
        bne.w (. + 44)
m68k_0331e4_end:
.org 0x331E8
m68k_0331e8:
        cmp.b %d7,%d4
m68k_0331e8_end:
.org 0x331EA
m68k_0331ea:
        beq.w (. + 38)
m68k_0331ea_end:
.org 0x331EE
m68k_0331ee:
        cmpi.b #0x41,(%a3, %d4.w)
m68k_0331ee_end:
.org 0x331F4
m68k_0331f4:
        bhi.w (. + 28)
m68k_0331f4_end:
.org 0x33210
m68k_033210:
        dbra %d4,(. + -48)
m68k_033210_end:
.org 0x33214
m68k_033214:
        movem.l (%a7)+,%d7/%a5
m68k_033214_end:
.org 0x33218
m68k_033218:
        rts
m68k_033218_end:
.org 0x3324C
m68k_03324c:
        lea.l 0xdffc:w,%a0
m68k_03324c_end:
.org 0x33250
m68k_033250:
        move.w 0xf364:w,%d0
m68k_033250_end:
.org 0x33254
m68k_033254:
        lsl.w #0x2,%d0
m68k_033254_end:
.org 0x33256
m68k_033256:
        cmpi.l #0x2710,(%a0, %d0.w)
m68k_033256_end:
.org 0x3325E
m68k_03325e:
        bcs.w (. + 14)
m68k_03325e_end:
.org 0x33262
m68k_033262:
        move.w #0x7,0xf728:w
m68k_033262_end:
.org 0x33268
m68k_033268:
        bra.w (. + 10)
m68k_033268_end:
.org 0x33272
m68k_033272:
        rts
m68k_033272_end:
.org 0x33274
m68k_033274:
        bsr.w (. + 30)
m68k_033274_end:
.org 0x33278
m68k_033278:
        cmpi.w #0x50,%d0
m68k_033278_end:
.org 0x3327C
m68k_03327c:
        bcc.w (. + 14)
m68k_03327c_end:
.org 0x33280
m68k_033280:
        move.w #0x8,0xf728:w
m68k_033280_end:
.org 0x33286
m68k_033286:
        bra.w (. + 10)
m68k_033286_end:
.org 0x33290
m68k_033290:
        rts
m68k_033290_end:
.org 0x33292
m68k_033292:
        lea.l 0xf72a:w,%a0
m68k_033292_end:
.org 0x33296
m68k_033296:
        lea.l 0xc500:w,%a1
m68k_033296_end:
.org 0x3329A
m68k_03329a:
        move.w #0xffff,%d0
m68k_03329a_end:
.org 0x3329E
m68k_03329e:
        move.w #0xffff,%d1
m68k_03329e_end:
.org 0x332A2
m68k_0332a2:
        clr.w %d3
m68k_0332a2_end:
.org 0x332A4
m68k_0332a4:
        move.w (%a0)+,%d2
m68k_0332a4_end:
.org 0x332A6
m68k_0332a6:
        bmi.w (. + 24)
m68k_0332a6_end:
.org 0x332AA
m68k_0332aa:
        btst.l #0xe,%d2
m68k_0332aa_end:
.org 0x332AE
m68k_0332ae:
        bne.b (. + -10)
m68k_0332ae_end:
.org 0x332B0
m68k_0332b0:
        move.b (%a1, %d2.w),%d3
m68k_0332b0_end:
.org 0x332B4
m68k_0332b4:
        cmp.w %d0,%d3
m68k_0332b4_end:
.org 0x332B6
m68k_0332b6:
        bcc.b (. + -18)
m68k_0332b6_end:
.org 0x332B8
m68k_0332b8:
        move.w %d3,%d0
m68k_0332b8_end:
.org 0x332BA
m68k_0332ba:
        move.w %d2,%d1
m68k_0332ba_end:
.org 0x332BC
m68k_0332bc:
        bra.b (. + -24)
m68k_0332bc_end:
.org 0x332BE
m68k_0332be:
        rts
m68k_0332be_end:
.org 0x3346A
m68k_03346a:
        lea.l 0xe59c:w,%a0
m68k_03346a_end:
.org 0x3346E
m68k_03346e:
        move.w 0xf364:w,%d0
m68k_03346e_end:
.org 0x33472
m68k_033472:
        lsl.w #0x2,%d0
m68k_033472_end:
.org 0x33474
m68k_033474:
        cmpi.w #0x64,(%a0, %d0.w)
m68k_033474_end:
.org 0x3347A
m68k_03347a:
        bcc.w (. + 72)
m68k_03347a_end:
.org 0x3347E
m68k_03347e:
        bsr.w (. + 76)
m68k_03347e_end:
.org 0x33482
m68k_033482:
        move.w %d1,0xf3a6:w
m68k_033482_end:
.org 0x33486
m68k_033486:
        bmi.w (. + 60)
m68k_033486_end:
.org 0x3348A
m68k_03348a:
        bsr.w (. + 110)
m68k_03348a_end:
.org 0x3348E
m68k_03348e:
        lea.l 0xe80c:w,%a0
m68k_03348e_end:
.org 0x33492
m68k_033492:
        move.w 0xf364:w,%d0
m68k_033492_end:
.org 0x33496
m68k_033496:
        lsl.w #0x1,%d0
m68k_033496_end:
.org 0x33498
m68k_033498:
        add.w 0xf364:w,%d0
m68k_033498_end:
.org 0x3349C
m68k_03349c:
        lsl.w #0x2,%d0
m68k_03349c_end:
.org 0x3349E
m68k_03349e:
        move.w 0xf3a6:w,0x8(%a0, %d0.w)
m68k_03349e_end:
.org 0x334A4
m68k_0334a4:
        move.l 0xf39e:w,%d1
m68k_0334a4_end:
.org 0x334A8
m68k_0334a8:
        divu.w #0x64,%d1
m68k_0334a8_end:
.org 0x334AC
m68k_0334ac:
        move.w %d1,0xa(%a0, %d0.w)
m68k_0334ac_end:
.org 0x334B0
m68k_0334b0:
        move.w 0xf3a6:w,%d0
m68k_0334b0_end:
.org 0x334B4
m68k_0334b4:
        lea.l 0xcd00:w,%a0
m68k_0334b4_end:
.org 0x334B8
m68k_0334b8:
        move.b #0x1,(%a0, %d0.w)
m68k_0334b8_end:
.org 0x334BE
m68k_0334be:
        bsr.w (. + -5150)
m68k_0334be_end:
.org 0x334C2
m68k_0334c2:
        move.w #0x4,0xf728:w
m68k_0334c2_end:
.org 0x334C8
m68k_0334c8:
        rts
m68k_0334c8_end:
.org 0x334CA
m68k_0334ca:
        lea.l 0xf72a:w,%a0
m68k_0334ca_end:
.org 0x334CE
m68k_0334ce:
        lea.l 0xb600:w,%a1
m68k_0334ce_end:
.org 0x334D2
m68k_0334d2:
        clr.w %d0
m68k_0334d2_end:
.org 0x334D4
m68k_0334d4:
        move.w #0xffff,%d1
m68k_0334d4_end:
.org 0x334D8
m68k_0334d8:
        move.w (%a0)+,%d2
m68k_0334d8_end:
.org 0x334DA
m68k_0334da:
        bmi.w (. + 28)
m68k_0334da_end:
.org 0x334DE
m68k_0334de:
        btst.l #0xe,%d2
m68k_0334de_end:
.org 0x334E2
m68k_0334e2:
        bne.b (. + -10)
m68k_0334e2_end:
.org 0x334E4
m68k_0334e4:
        move.w %d2,%d3
m68k_0334e4_end:
.org 0x334E6
m68k_0334e6:
        lsl.w #0x1,%d3
m68k_0334e6_end:
.org 0x334E8
m68k_0334e8:
        move.w (%a1, %d3.w),%d3
m68k_0334e8_end:
.org 0x334EC
m68k_0334ec:
        cmp.w %d0,%d3
m68k_0334ec_end:
.org 0x334EE
m68k_0334ee:
        bls.b (. + -22)
m68k_0334ee_end:
.org 0x334F0
m68k_0334f0:
        move.w %d3,%d0
m68k_0334f0_end:
.org 0x334F2
m68k_0334f2:
        move.w %d2,%d1
m68k_0334f2_end:
.org 0x334F4
m68k_0334f4:
        bra.b (. + -28)
m68k_0334f4_end:
.org 0x334F6
m68k_0334f6:
        rts
m68k_0334f6_end:
.org 0x334F8
m68k_0334f8:
        lea.l 0xdffc:w,%a0
m68k_0334f8_end:
.org 0x334FC
m68k_0334fc:
        move.w 0xf364:w,%d0
m68k_0334fc_end:
.org 0x33500
m68k_033500:
        lsl.w #0x2,%d0
m68k_033500_end:
.org 0x33502
m68k_033502:
        move.l (%a0, %d0.w),%d1
m68k_033502_end:
.org 0x33506
m68k_033506:
        moveq #3,%d2
m68k_033506_end:
.org 0x33508
m68k_033508:
        jsr 0x35760:l
m68k_033508_end:
.org 0x3350E
m68k_03350e:
        cmpi.l #0x1869f,%d1
m68k_03350e_end:
.org 0x33514
m68k_033514:
        bls.w (. + 10)
m68k_033514_end:
.org 0x33518
m68k_033518:
        move.l #0x1869f,%d1
m68k_033518_end:
.org 0x3351E
m68k_03351e:
        move.l %d1,0xf39e:w
m68k_03351e_end:
.org 0x33522
m68k_033522:
        rts
m68k_033522_end:
.org 0x33524
m68k_033524:
        bsr.w (. + 80)
m68k_033524_end:
.org 0x33528
m68k_033528:
        move.w %d1,0xf3a6:w
m68k_033528_end:
.org 0x3352C
m68k_03352c:
        bmi.w (. + 64)
m68k_03352c_end:
.org 0x33530
m68k_033530:
        bsr.w (. + 126)
m68k_033530_end:
.org 0x33534
m68k_033534:
        lea.l 0xdffc:w,%a0
m68k_033534_end:
.org 0x33538
m68k_033538:
        move.w 0xf364:w,%d0
m68k_033538_end:
.org 0x3353C
m68k_03353c:
        lsl.w #0x2,%d0
m68k_03353c_end:
.org 0x3353E
m68k_03353e:
        move.l (%a0, %d0.w),%d1
m68k_03353e_end:
.org 0x33542
m68k_033542:
        move.l %d1,%d2
m68k_033542_end:
.org 0x33544
m68k_033544:
        lsr.l #0x1,%d2
m68k_033544_end:
.org 0x33546
m68k_033546:
        cmp.l 0xf39e:w,%d2
m68k_033546_end:
.org 0x3354A
m68k_03354a:
        bcs.w (. + 34)
m68k_03354a_end:
.org 0x3354E
m68k_03354e:
        sub.l 0xf39e:w,%d1
m68k_03354e_end:
.org 0x33552
m68k_033552:
        move.l %d1,(%a0, %d0.w)
m68k_033552_end:
.org 0x33556
m68k_033556:
        bsr.w (. + 114)
m68k_033556_end:
.org 0x3355A
m68k_03355a:
        move.w 0xf3a6:w,%d0
m68k_03355a_end:
.org 0x3355E
m68k_03355e:
        lea.l 0xcd00:w,%a0
m68k_03355e_end:
.org 0x33562
m68k_033562:
        move.b #0x1,(%a0, %d0.w)
m68k_033562_end:
.org 0x33568
m68k_033568:
        bsr.w (. + -5320)
m68k_033568_end:
.org 0x3356C
m68k_03356c:
        move.w #0x9,0xf728:w
m68k_03356c_end:
.org 0x33572
m68k_033572:
        rts
m68k_033572_end:
.org 0x33574
m68k_033574:
        lea.l 0xf72a:w,%a0
m68k_033574_end:
.org 0x33578
m68k_033578:
        lea.l 0xc500:w,%a1
m68k_033578_end:
.org 0x3357C
m68k_03357c:
        lea.l 0xc800:w,%a2
m68k_03357c_end:
.org 0x33580
m68k_033580:
        move.w #0xffff,%d0
m68k_033580_end:
.org 0x33584
m68k_033584:
        move.w #0xffff,%d1
m68k_033584_end:
.org 0x33588
m68k_033588:
        move.w (%a0)+,%d2
m68k_033588_end:
.org 0x3358A
m68k_03358a:
        bmi.w (. + 34)
m68k_03358a_end:
.org 0x3358E
m68k_03358e:
        btst.l #0xe,%d2
m68k_03358e_end:
.org 0x33592
m68k_033592:
        bne.b (. + -10)
m68k_033592_end:
.org 0x33594
m68k_033594:
        move.w %d2,%d3
m68k_033594_end:
.org 0x33596
m68k_033596:
        lsl.w #0x2,%d3
m68k_033596_end:
.org 0x33598
m68k_033598:
        tst.l (%a2, %d3.w)
m68k_033598_end:
.org 0x3359C
m68k_03359c:
        beq.b (. + -20)
m68k_03359c_end:
.org 0x3359E
m68k_03359e:
        move.b (%a1, %d2.w),%d3
m68k_03359e_end:
.org 0x335A2
m68k_0335a2:
        cmp.b %d0,%d3
m68k_0335a2_end:
.org 0x335A4
m68k_0335a4:
        bcc.b (. + -28)
m68k_0335a4_end:
.org 0x335A6
m68k_0335a6:
        move.b %d3,%d0
m68k_0335a6_end:
.org 0x335A8
m68k_0335a8:
        move.w %d2,%d1
m68k_0335a8_end:
.org 0x335AA
m68k_0335aa:
        bra.b (. + -34)
m68k_0335aa_end:
.org 0x335AC
m68k_0335ac:
        rts
m68k_0335ac_end:
.org 0x335AE
m68k_0335ae:
        lea.l 0xc800:w,%a0
m68k_0335ae_end:
.org 0x335B2
m68k_0335b2:
        move.w 0xf3a6:w,%d0
m68k_0335b2_end:
.org 0x335B6
m68k_0335b6:
        lsl.w #0x2,%d0
m68k_0335b6_end:
.org 0x335B8
m68k_0335b8:
        move.l (%a0, %d0.w),%d1
m68k_0335b8_end:
.org 0x335BC
m68k_0335bc:
        divu.w #0xa,%d1
m68k_0335bc_end:
.org 0x335C0
m68k_0335c0:
        ext.l %d1
m68k_0335c0_end:
.org 0x335C2
m68k_0335c2:
        move.l %d1,0xf39e:w
m68k_0335c2_end:
.org 0x335C6
m68k_0335c6:
        rts
m68k_0335c6_end:
.org 0x335C8
m68k_0335c8:
        jsr 0x83d4:l
m68k_0335c8_end:
.org 0x335CE
m68k_0335ce:
        move.w 0xf3a6:w,%d0
m68k_0335ce_end:
.org 0x335D2
m68k_0335d2:
        lsl.w #0x1,%d0
m68k_0335d2_end:
.org 0x335D4
m68k_0335d4:
        lea.l 0xb400:w,%a0
m68k_0335d4_end:
.org 0x335D8
m68k_0335d8:
        move.w (%a0, %d0.w),%d2
m68k_0335d8_end:
.org 0x335DC
m68k_0335dc:
        move.w %d2,%d1
m68k_0335dc_end:
.org 0x335DE
m68k_0335de:
        lsl.w #0x2,%d2
m68k_0335de_end:
.org 0x335E0
m68k_0335e0:
        add.w %d1,%d2
m68k_0335e0_end:
.org 0x335E2
m68k_0335e2:
        lea.l 0xc000:w,%a0
m68k_0335e2_end:
.org 0x335E6
m68k_0335e6:
        add.w (%a0, %d0.w),%d2
m68k_0335e6_end:
.org 0x335EA
m68k_0335ea:
        moveq #0,%d1
m68k_0335ea_end:
.org 0x335EC
m68k_0335ec:
        move.w 0xf61c:w,%d1
m68k_0335ec_end:
.org 0x335F0
m68k_0335f0:
        lsl.l #0x3,%d1
m68k_0335f0_end:
.org 0x335F2
m68k_0335f2:
        swap %d1
m68k_0335f2_end:
.org 0x335F4
m68k_0335f4:
        addi.w #0x8,%d1
m68k_0335f4_end:
.org 0x335F8
m68k_0335f8:
        mulu.w %d1,%d2
m68k_0335f8_end:
.org 0x335FA
m68k_0335fa:
        divu.w #0x3e8,%d2
m68k_0335fa_end:
.org 0x335FE
m68k_0335fe:
        lsr.w #0x1,%d0
m68k_0335fe_end:
.org 0x33600
m68k_033600:
        lea.l 0xc500:w,%a0
m68k_033600_end:
.org 0x33604
m68k_033604:
        clr.w %d1
m68k_033604_end:
.org 0x33606
m68k_033606:
        move.b (%a0, %d0.w),%d1
m68k_033606_end:
.org 0x3360A
m68k_03360a:
        add.w %d2,%d1
m68k_03360a_end:
.org 0x3360C
m68k_03360c:
        cmpi.w #0x64,%d1
m68k_03360c_end:
.org 0x33610
m68k_033610:
        bls.b (. + 14)
m68k_033610_end:
.org 0x3361E
m68k_03361e:
        move.b %d1,(%a0, %d0.w)
m68k_03361e_end:
.org 0x33622
m68k_033622:
        lsl.w #0x1,%d0
m68k_033622_end:
.org 0x33624
m68k_033624:
        lea.l 0xc000:w,%a0
m68k_033624_end:
.org 0x33628
m68k_033628:
        add.w %d2,(%a0, %d0.w)
m68k_033628_end:
.org 0x3362C
m68k_03362c:
        cmpi.w #0x3e7,(%a0, %d0.w)
m68k_03362c_end:
.org 0x33632
m68k_033632:
        bls.b (. + 8)
m68k_033632_end:
.org 0x3363A
m68k_03363a:
        rts
m68k_03363a_end:
.org 0x3363C
m68k_03363c:
        move.w 0xf364:w,%d0
m68k_03363c_end:
.org 0x33640
m68k_033640:
        lsl.w #0x1,%d0
m68k_033640_end:
.org 0x33642
m68k_033642:
        lea.l 0xf45e:w,%a0
m68k_033642_end:
.org 0x33646
m68k_033646:
        move.w (%a0, %d0.w),%d0
m68k_033646_end:
.org 0x3364A
m68k_03364a:
        lea.l 0xcd00:w,%a0
m68k_03364a_end:
.org 0x3364E
m68k_03364e:
        tst.b (%a0, %d0.w)
m68k_03364e_end:
.org 0x33652
m68k_033652:
        bne.w (. + 12)
m68k_033652_end:
.org 0x3365E
m68k_03365e:
        move.w #0xa,0xf728:w
m68k_03365e_end:
.org 0x33664
m68k_033664:
        rts
m68k_033664_end:
.org 0x33666
m68k_033666:
        lea.l 0xf72a:w,%a0
m68k_033666_end:
.org 0x3366A
m68k_03366a:
        lea.l 0xb400:w,%a1
m68k_03366a_end:
.org 0x3366E
m68k_03366e:
        lea.l 0xd300:w,%a2
m68k_03366e_end:
.org 0x33672
m68k_033672:
        clr.w %d0
m68k_033672_end:
.org 0x33674
m68k_033674:
        move.w (%a0)+,%d1
m68k_033674_end:
.org 0x33676
m68k_033676:
        bmi.w (. + 18)
m68k_033676_end:
.org 0x3367A
m68k_03367a:
        andi.w #0xff,%d1
m68k_03367a_end:
.org 0x3367E
m68k_03367e:
        lsl.w #0x1,%d1
m68k_03367e_end:
.org 0x33680
m68k_033680:
        move.w (%a1, %d1.w),(%a2)+
m68k_033680_end:
.org 0x33684
m68k_033684:
        addq.w #0x1,%d0
m68k_033684_end:
.org 0x33686
m68k_033686:
        bra.b (. + -18)
m68k_033686_end:
.org 0x33688
m68k_033688:
        cmpi.w #0x1,%d0
m68k_033688_end:
.org 0x3368C
m68k_03368c:
        beq.w (. + 72)
m68k_03368c_end:
.org 0x33690
m68k_033690:
        lsl.w #0x1,%d0
m68k_033690_end:
.org 0x33692
m68k_033692:
        lea.l 0xd300:w,%a2
m68k_033692_end:
.org 0x33696
m68k_033696:
        lea.l 0xf72a:w,%a0
m68k_033696_end:
.org 0x3369A
m68k_03369a:
        move.w #0x2,%d1
m68k_03369a_end:
.org 0x3369E
m68k_03369e:
        move.w -0x2(%a2, %d1.w),%d2
m68k_03369e_end:
.org 0x336A2
m68k_0336a2:
        cmp.w (%a2, %d1.w),%d2
m68k_0336a2_end:
.org 0x336A6
m68k_0336a6:
        bcc.w (. + 32)
m68k_0336a6_end:
.org 0x336C6
m68k_0336c6:
        addq.w #0x2,%d1
m68k_0336c6_end:
.org 0x336C8
m68k_0336c8:
        cmp.w %d0,%d1
m68k_0336c8_end:
.org 0x336CA
m68k_0336ca:
        bcs.b (. + -44)
m68k_0336ca_end:
.org 0x336CC
m68k_0336cc:
        subq.w #0x2,%d0
m68k_0336cc_end:
.org 0x336CE
m68k_0336ce:
        cmpi.w #0x2,%d0
m68k_0336ce_end:
.org 0x336D2
m68k_0336d2:
        bhi.b (. + -56)
m68k_0336d2_end:
.org 0x336D4
m68k_0336d4:
        rts
m68k_0336d4_end:
.org 0x336D6
m68k_0336d6:
        lea.l 0xf72a:w,%a0
m68k_0336d6_end:
.org 0x336DA
m68k_0336da:
        lea.l 0xb400:w,%a1
m68k_0336da_end:
.org 0x336DE
m68k_0336de:
        lea.l 0xdffc:w,%a2
m68k_0336de_end:
.org 0x336E2
m68k_0336e2:
        move.w 0xf364:w,%d0
m68k_0336e2_end:
.org 0x336E6
m68k_0336e6:
        lsl.w #0x2,%d0
m68k_0336e6_end:
.org 0x336E8
m68k_0336e8:
        move.l (%a2, %d0.w),%d1
m68k_0336e8_end:
.org 0x336EC
m68k_0336ec:
        lea.l 0xea88:w,%a4
m68k_0336ec_end:
.org 0x336F0
m68k_0336f0:
        move.w (%a0)+,%d2
m68k_0336f0_end:
.org 0x336F2
m68k_0336f2:
        bmi.w (. + 108)
m68k_0336f2_end:
.org 0x336F6
m68k_0336f6:
        andi.w #0xff,%d2
m68k_0336f6_end:
.org 0x336FA
m68k_0336fa:
        lsl.w #0x1,%d2
m68k_0336fa_end:
.org 0x336FC
m68k_0336fc:
        move.w (%a1, %d2.w),%d3
m68k_0336fc_end:
.org 0x33700
m68k_033700:
        clr.w %d4
m68k_033700_end:
.org 0x33702
m68k_033702:
        cmpi.w #0x64,%d3
m68k_033702_end:
.org 0x33706
m68k_033706:
        bcc.w (. + 16)
m68k_033706_end:
.org 0x3370A
m68k_03370a:
        addq.w #0x4,%d4
m68k_03370a_end:
.org 0x3370C
m68k_03370c:
        cmpi.w #0x3c,%d3
m68k_03370c_end:
.org 0x33710
m68k_033710:
        bcc.w (. + 6)
m68k_033710_end:
.org 0x33714
m68k_033714:
        addq.w #0x4,%d4
m68k_033714_end:
.org 0x33716
m68k_033716:
        lea.l 76(%pc),%a3
m68k_033716_end:
.org 0x3371A
m68k_03371a:
        nop
m68k_03371a_end:
.org 0x3371C
m68k_03371c:
        adda.w %d4,%a3
m68k_03371c_end:
.org 0x3371E
m68k_03371e:
        move.w %d2,%d3
m68k_03371e_end:
.org 0x33720
m68k_033720:
        lsr.w #0x1,%d3
m68k_033720_end:
.org 0x33722
m68k_033722:
        add.w %d2,%d3
m68k_033722_end:
.org 0x33724
m68k_033724:
        clr.w %d4
m68k_033724_end:
.org 0x33726
m68k_033726:
        move.b (%a3)+,%d4
m68k_033726_end:
.org 0x33728
m68k_033728:
        bmi.b (. + -56)
m68k_033728_end:
.org 0x3372A
m68k_03372a:
        move.w %d4,%d7
m68k_03372a_end:
.org 0x3372C
m68k_03372c:
        add.w %d3,%d7
m68k_03372c_end:
.org 0x3372E
m68k_03372e:
        move.b (%a4, %d7.w),%d5
m68k_03372e_end:
.org 0x33732
m68k_033732:
        cmpi.w #0x3,%d5
m68k_033732_end:
.org 0x33736
m68k_033736:
        bcc.b (. + -18)
m68k_033736_end:
.org 0x33738
m68k_033738:
        move.w %d4,%d6
m68k_033738_end:
.org 0x3373A
m68k_03373a:
        lsl.w #0x1,%d6
m68k_03373a_end:
.org 0x3373C
m68k_03373c:
        add.w %d4,%d6
m68k_03373c_end:
.org 0x3373E
m68k_03373e:
        add.w %d5,%d6
m68k_03373e_end:
.org 0x33740
m68k_033740:
        addq.w #0x1,%d5
m68k_033740_end:
.org 0x33742
m68k_033742:
        lsl.w #0x2,%d6
m68k_033742_end:
.org 0x33744
m68k_033744:
        lea.l 0xd2ca:l,%a5
m68k_033744_end:
.org 0x3374A
m68k_03374a:
        move.l (%a5, %d6.w),%d6
m68k_03374a_end:
.org 0x3374E
m68k_03374e:
        move.l %d1,%d7
m68k_03374e_end:
.org 0x33750
m68k_033750:
        lsr.l #0x2,%d7
m68k_033750_end:
.org 0x33752
m68k_033752:
        cmp.l %d7,%d6
m68k_033752_end:
.org 0x33754
m68k_033754:
        bhi.b (. + -100)
m68k_033754_end:
.org 0x33756
m68k_033756:
        sub.l %d6,%d1
m68k_033756_end:
.org 0x33758
m68k_033758:
        move.b %d5,(%a4, %d4.w)
m68k_033758_end:
.org 0x3375C
m68k_03375c:
        bra.b (. + -108)
m68k_03375c_end:
.org 0x3375E
m68k_03375e:
        move.l %d1,(%a2, %d0.w)
m68k_03375e_end:
.org 0x33762
m68k_033762:
        rts
m68k_033762_end:
.org 0x33770
m68k_033770:
        bsr.w (. + 32)
m68k_033770_end:
.org 0x33774
m68k_033774:
        bcs.w (. + 20)
m68k_033774_end:
.org 0x33778
m68k_033778:
        bsr.w (. + -274)
m68k_033778_end:
.org 0x3377C
m68k_03377c:
        bsr.w (. + 74)
m68k_03377c_end:
.org 0x33780
m68k_033780:
        bcs.w (. + 8)
m68k_033780_end:
.org 0x33784
m68k_033784:
        bsr.w (. + 170)
m68k_033784_end:
.org 0x33788
m68k_033788:
        move.w #0xb,0xf728:w
m68k_033788_end:
.org 0x3378E
m68k_03378e:
        rts
m68k_03378e_end:
.org 0x33790
m68k_033790:
        lea.l 0xf72a:w,%a0
m68k_033790_end:
.org 0x33794
m68k_033794:
        lea.l 0xc800:w,%a1
m68k_033794_end:
.org 0x33798
m68k_033798:
        lea.l 0xb800:w,%a2
m68k_033798_end:
.org 0x3379C
m68k_03379c:
        move.w (%a0)+,%d0
m68k_03379c_end:
.org 0x3379E
m68k_03379e:
        bmi.w (. + 34)
m68k_03379e_end:
.org 0x337A2
m68k_0337a2:
        andi.w #0xff,%d0
m68k_0337a2_end:
.org 0x337A6
m68k_0337a6:
        lsl.w #0x1,%d0
m68k_0337a6_end:
.org 0x337A8
m68k_0337a8:
        move.w (%a2, %d0.w),%d1
m68k_0337a8_end:
.org 0x337AC
m68k_0337ac:
        mulu.w #0x64,%d1
m68k_0337ac_end:
.org 0x337B0
m68k_0337b0:
        lsl.w #0x1,%d0
m68k_0337b0_end:
.org 0x337B2
m68k_0337b2:
        cmp.l (%a0, %d0.w),%d1
m68k_0337b2_end:
.org 0x337B6
m68k_0337b6:
        bls.b (. + -26)
m68k_0337b6_end:
.org 0x337B8
m68k_0337b8:
        andi.w #0xfffe,%sr
m68k_0337b8_end:
.org 0x337BC
m68k_0337bc:
        bra.w (. + 8)
m68k_0337bc_end:
.org 0x337C4
m68k_0337c4:
        rts
m68k_0337c4_end:
.org 0x337C6
m68k_0337c6:
        lea.l 0xe774:w,%a0
m68k_0337c6_end:
.org 0x337CA
m68k_0337ca:
        move.w 0xf364:w,%d0
m68k_0337ca_end:
.org 0x337CE
m68k_0337ce:
        lsl.w #0x2,%d0
m68k_0337ce_end:
.org 0x337D0
m68k_0337d0:
        move.l (%a0, %d0.w),%d1
m68k_0337d0_end:
.org 0x337D4
m68k_0337d4:
        beq.w (. + 68)
m68k_0337d4_end:
.org 0x33818
m68k_033818:
        move.l %d1,(%a0, %d0.w)
m68k_033818_end:
.org 0x3381C
m68k_03381c:
        andi.w #0xfffe,%sr
m68k_03381c_end:
.org 0x33820
m68k_033820:
        bra.w (. + 12)
m68k_033820_end:
.org 0x3382C
m68k_03382c:
        rts
m68k_03382c_end:
.org 0x3382E
m68k_03382e:
        lea.l 0xf72a:w,%a0
m68k_03382e_end:
.org 0x33832
m68k_033832:
        lea.l 0xb800:w,%a3
m68k_033832_end:
.org 0x33836
m68k_033836:
        lea.l 0xdffc:w,%a1
m68k_033836_end:
.org 0x3383A
m68k_03383a:
        move.w 0xf364:w,%d0
m68k_03383a_end:
.org 0x3383E
m68k_03383e:
        lsl.w #0x2,%d0
m68k_03383e_end:
.org 0x33840
m68k_033840:
        move.l (%a1, %d0.w),%d3
m68k_033840_end:
.org 0x33844
m68k_033844:
        cmpi.l #0xbb8,%d3
m68k_033844_end:
.org 0x3384A
m68k_03384a:
        bcs.w (. + 110)
m68k_03384a_end:
.org 0x3384E
m68k_03384e:
        move.l %d3,%d1
m68k_03384e_end:
.org 0x33850
m68k_033850:
        divu.w #0xc8,%d1
m68k_033850_end:
.org 0x33854
m68k_033854:
        move.w %d1,%d4
m68k_033854_end:
.org 0x33856
m68k_033856:
        beq.w (. + 84)
m68k_033856_end:
.org 0x3385A
m68k_03385a:
        mulu.w #0x64,%d4
m68k_03385a_end:
.org 0x3385E
m68k_03385e:
        cmpi.l #0x186a0,%d4
m68k_03385e_end:
.org 0x33864
m68k_033864:
        bls.w (. + 14)
m68k_033864_end:
.org 0x33872
m68k_033872:
        mulu.w #0x64,%d1
m68k_033872_end:
.org 0x33876
m68k_033876:
        sub.l %d1,%d3
m68k_033876_end:
.org 0x33878
m68k_033878:
        move.l %d3,(%a1, %d0.w)
m68k_033878_end:
.org 0x3387C
m68k_03387c:
        lea.l 0xc800:w,%a2
m68k_03387c_end:
.org 0x33880
m68k_033880:
        move.w (%a0)+,%d0
m68k_033880_end:
.org 0x33882
m68k_033882:
        bmi.w (. + 40)
m68k_033882_end:
.org 0x33886
m68k_033886:
        andi.w #0xff,%d0
m68k_033886_end:
.org 0x3388A
m68k_03388a:
        lsl.w #0x1,%d0
m68k_03388a_end:
.org 0x3388C
m68k_03388c:
        move.w (%a3, %d0.w),%d1
m68k_03388c_end:
.org 0x33890
m68k_033890:
        mulu.w #0x64,%d1
m68k_033890_end:
.org 0x33894
m68k_033894:
        lsl.w #0x1,%d0
m68k_033894_end:
.org 0x33896
m68k_033896:
        sub.l (%a2, %d0.w),%d1
m68k_033896_end:
.org 0x3389A
m68k_03389a:
        cmp.l %d4,%d1
m68k_03389a_end:
.org 0x3389C
m68k_03389c:
        bls.w (. + 6)
m68k_03389c_end:
.org 0x338A2
m68k_0338a2:
        add.l %d1,(%a2, %d0.w)
m68k_0338a2_end:
.org 0x338A6
m68k_0338a6:
        sub.l %d1,%d4
m68k_0338a6_end:
.org 0x338A8
m68k_0338a8:
        bne.b (. + -40)
m68k_0338a8_end:
.org 0x338AA
m68k_0338aa:
        lea.l 0xe774:w,%a0
m68k_0338aa_end:
.org 0x338AE
m68k_0338ae:
        move.w 0xf364:w,%d0
m68k_0338ae_end:
.org 0x338B2
m68k_0338b2:
        lsl.w #0x2,%d0
m68k_0338b2_end:
.org 0x338B4
m68k_0338b4:
        move.l %d4,(%a0, %d0.w)
m68k_0338b4_end:
.org 0x338B8
m68k_0338b8:
        rts
m68k_0338b8_end:
.org 0x338BA
m68k_0338ba:
        move.w #0xffff,0xf728:w
m68k_0338ba_end:
.org 0x338C0
m68k_0338c0:
        rts
m68k_0338c0_end:
.org 0x35760
m68k_035760:
        tst.l %d2
m68k_035760_end:
.org 0x35762
m68k_035762:
        bpl.b (. + 10)
m68k_035762_end:
.org 0x3576C
m68k_03576c:
        tst.l %d1
m68k_03576c_end:
.org 0x3576E
m68k_03576e:
        bpl.b (. + 12)
m68k_03576e_end:
.org 0x3577A
m68k_03577a:
        cmpi.l #0xffff,%d2
m68k_03577a_end:
.org 0x35780
m68k_035780:
        bls.b (. + 90)
m68k_035780_end:
.org 0x357DA
m68k_0357da:
        movem.w %d1/%d3,-(%a7)
m68k_0357da_end:
.org 0x357DE
m68k_0357de:
        clr.w %d1
m68k_0357de_end:
.org 0x357E0
m68k_0357e0:
        swap %d1
m68k_0357e0_end:
.org 0x357E2
m68k_0357e2:
        divu.w %d2,%d1
m68k_0357e2_end:
.org 0x357E4
m68k_0357e4:
        move.w %d1,%d3
m68k_0357e4_end:
.org 0x357E6
m68k_0357e6:
        move.w (%a7)+,%d1
m68k_0357e6_end:
.org 0x357E8
m68k_0357e8:
        divu.w %d2,%d1
m68k_0357e8_end:
.org 0x357EA
m68k_0357ea:
        swap %d1
m68k_0357ea_end:
.org 0x357EC
m68k_0357ec:
        moveq #0,%d2
m68k_0357ec_end:
.org 0x357EE
m68k_0357ee:
        move.w %d1,%d2
m68k_0357ee_end:
.org 0x357F0
m68k_0357f0:
        move.w %d3,%d1
m68k_0357f0_end:
.org 0x357F2
m68k_0357f2:
        swap %d1
m68k_0357f2_end:
.org 0x357F4
m68k_0357f4:
        move.w (%a7)+,%d3
m68k_0357f4_end:
.org 0x357F6
m68k_0357f6:
        rts
m68k_0357f6_end:
.org 0x39658
m68k_039658:
        move.w #0x8f02,0xc00004:l
m68k_039658_end:
.org 0x39660
m68k_039660:
        bsr.w (. + 7248)
m68k_039660_end:
.org 0x39664
m68k_039664:
        move.b (%a0)+,%d1
m68k_039664_end:
.org 0x39666
m68k_039666:
        move.b (%a0)+,%d2
m68k_039666_end:
.org 0x39668
m68k_039668:
        cmp.b %d2,%d1
m68k_039668_end:
.org 0x3966A
m68k_03966a:
        beq.w (. + 18)
m68k_03966a_end:
.org 0x3966E
m68k_03966e:
        move.b (%a0)+,%d4
m68k_03966e_end:
.org 0x39670
m68k_039670:
        asl.w #0x8,%d2
m68k_039670_end:
.org 0x39672
m68k_039672:
        move.b %d4,%d2
m68k_039672_end:
.org 0x39674
m68k_039674:
        move.w %d2,0xc00000:l
m68k_039674_end:
.org 0x3967A
m68k_03967a:
        bra.b (. + -20)
m68k_03967a_end:
.org 0x3967C
m68k_03967c:
        moveq #0,%d3
m68k_03967c_end:
.org 0x3967E
m68k_03967e:
        move.b (%a0)+,%d3
m68k_03967e_end:
.org 0x39680
m68k_039680:
        beq.w (. + 24)
m68k_039680_end:
.org 0x39684
m68k_039684:
        move.b (%a0)+,%d4
m68k_039684_end:
.org 0x39686
m68k_039686:
        move.b (%a0)+,%d2
m68k_039686_end:
.org 0x39688
m68k_039688:
        asl.w #0x8,%d4
m68k_039688_end:
.org 0x3968A
m68k_03968a:
        move.b %d2,%d4
m68k_03968a_end:
.org 0x3968C
m68k_03968c:
        move.w %d4,0xc00000:l
m68k_03968c_end:
.org 0x39692
m68k_039692:
        dbra %d3,(. + -6)
m68k_039692_end:
.org 0x39696
m68k_039696:
        bra.b (. + -48)
m68k_039696_end:
.org 0x39698
m68k_039698:
        rts
m68k_039698_end:
.org 0x3969A
m68k_03969a:
        move.w #0x2700,%sr
m68k_03969a_end:
.org 0x3969E
m68k_03969e:
        clr.w 0xf612:w
m68k_03969e_end:
.org 0x396A2
m68k_0396a2:
        jsr 4282(%pc)
m68k_0396a2_end:
.org 0x396A6
m68k_0396a6:
        nop
m68k_0396a6_end:
.org 0x396A8
m68k_0396a8:
        clr.l 0xff702e:l
m68k_0396a8_end:
.org 0x396AE
m68k_0396ae:
        clr.l 0xff703a:l
m68k_0396ae_end:
.org 0x396B4
m68k_0396b4:
        clr.w 0xff7000:l
m68k_0396b4_end:
.org 0x396BA
m68k_0396ba:
        clr.w 0xff7004:l
m68k_0396ba_end:
.org 0x396C0
m68k_0396c0:
        clr.w 0xff703e:l
m68k_0396c0_end:
.org 0x396C6
m68k_0396c6:
        clr.w 0xff7036:l
m68k_0396c6_end:
.org 0x396CC
m68k_0396cc:
        clr.w 0xff7044:l
m68k_0396cc_end:
.org 0x396D2
m68k_0396d2:
        clr.w 0xff703c:l
m68k_0396d2_end:
.org 0x396D8
m68k_0396d8:
        cmpi.w #0x18,0xff7026:l
m68k_0396d8_end:
.org 0x396E0
m68k_0396e0:
        bne.w (. + 24)
m68k_0396e0_end:
.org 0x396F8
m68k_0396f8:
        cmpi.w #0x1c,0xff7026:l
m68k_0396f8_end:
.org 0x39700
m68k_039700:
        beq.b (. + -28)
m68k_039700_end:
.org 0x39702
m68k_039702:
        move.w #0x90,0xff7032:l
m68k_039702_end:
.org 0x3970A
m68k_03970a:
        move.w #0x60,0xff7034:l
m68k_03970a_end:
.org 0x39712
m68k_039712:
        move.w 0xff7026:l,%d0
m68k_039712_end:
.org 0x39718
m68k_039718:
        asl.w #0x1,%d0
m68k_039718_end:
.org 0x3971A
m68k_03971a:
        lea.l -2964(%pc),%a0
m68k_03971a_end:
.org 0x3971E
m68k_03971e:
        lea.l -2888(%pc),%a1
m68k_03971e_end:
.org 0x39722
m68k_039722:
        move.w (%a0, %d0.w),%d1
m68k_039722_end:
.org 0x39726
m68k_039726:
        move.w (%a1, %d0.w),%d2
m68k_039726_end:
.org 0x3972A
m68k_03972a:
        move.w %d1,0xff7028:l
m68k_03972a_end:
.org 0x39730
m68k_039730:
        move.w %d2,0xff702a:l
m68k_039730_end:
.org 0x39736
m68k_039736:
        move.w 0xff7026:l,%d0
m68k_039736_end:
.org 0x3973C
m68k_03973c:
        lea.l -2286(%pc),%a0
m68k_03973c_end:
.org 0x39740
m68k_039740:
        move.b (%a0, %d0.w),%d1
m68k_039740_end:
.org 0x39744
m68k_039744:
        move.b %d1,0xff702c:l
m68k_039744_end:
.org 0x3974A
m68k_03974a:
        move.w #0x0,%d0
m68k_03974a_end:
.org 0x3974E
m68k_03974e:
        cmpi.w #0xa,0xff7026:l
m68k_03974e_end:
.org 0x39756
m68k_039756:
        bne.w (. + 8)
m68k_039756_end:
.org 0x3975E
m68k_03975e:
        move.w 0xff7026:l,%d3
m68k_03975e_end:
.org 0x39764
m68k_039764:
        asl.w #0x2,%d3
m68k_039764_end:
.org 0x39766
m68k_039766:
        lea.l -4014(%pc),%a1
m68k_039766_end:
.org 0x3976A
m68k_03976a:
        movea.l (%a1, %d3.w),%a0
m68k_03976a_end:
.org 0x3976E
m68k_03976e:
        bsr.w (. + -278)
m68k_03976e_end:
.org 0x39772
m68k_039772:
        move.w 0xff7026:l,%d0
m68k_039772_end:
.org 0x39778
m68k_039778:
        lea.l -3552(%pc),%a6
m68k_039778_end:
.org 0x3977C
m68k_03977c:
        move.b (%a6, %d0.w),%d1
m68k_03977c_end:
.org 0x39780
m68k_039780:
        cmpi.b #0x1,%d1
m68k_039780_end:
.org 0x39784
m68k_039784:
        bne.w (. + 30)
m68k_039784_end:
.org 0x397A2
m68k_0397a2:
        move.w 0xff7026:l,%d3
m68k_0397a2_end:
.org 0x397A8
m68k_0397a8:
        asl.w #0x2,%d3
m68k_0397a8_end:
.org 0x397AA
m68k_0397aa:
        lea.l -3762(%pc),%a1
m68k_0397aa_end:
.org 0x397AE
m68k_0397ae:
        movea.l (%a1, %d3.w),%a0
m68k_0397ae_end:
.org 0x397B2
m68k_0397b2:
        lea.l 0xfb00:w,%a1
m68k_0397b2_end:
.org 0x397B6
m68k_0397b6:
        moveq #7,%d0
m68k_0397b6_end:
.org 0x397B8
m68k_0397b8:
        move.l (%a0)+,(%a1)+
m68k_0397b8_end:
.org 0x397BA
m68k_0397ba:
        dbra %d0,(. + -2)
m68k_0397ba_end:
.org 0x397BE
m68k_0397be:
        bra.w (. + 4)
m68k_0397be_end:
.org 0x397C2
m68k_0397c2:
        clr.l %d0
m68k_0397c2_end:
.org 0x397C4
m68k_0397c4:
        move.w #0x2500,%sr
m68k_0397c4_end:
.org 0x397C8
m68k_0397c8:
        move.w #0x600,0xf612:w
m68k_0397c8_end:
.org 0x397CE
m68k_0397ce:
        tst.b 0xf612:w
m68k_0397ce_end:
.org 0x397D2
m68k_0397d2:
        bne.b (. + -4)
m68k_0397d2_end:
.org 0x397D4
m68k_0397d4:
        addi.w #0x1,0xff703e:l
m68k_0397d4_end:
.org 0x397DC
m68k_0397dc:
        clr.l %d0
m68k_0397dc_end:
.org 0x397DE
m68k_0397de:
        move.w 0xff7026:l,%d0
m68k_0397de_end:
.org 0x397E4
m68k_0397e4:
        asl.w #0x1,%d0
m68k_0397e4_end:
.org 0x397E6
m68k_0397e6:
        clr.l %d1
m68k_0397e6_end:
.org 0x397E8
m68k_0397e8:
        lea.l -3624(%pc),%a0
m68k_0397e8_end:
.org 0x397EC
m68k_0397ec:
        move.w (%a0, %d0.w),%d1
m68k_0397ec_end:
.org 0x397F0
m68k_0397f0:
        cmp.w 0xff703e:l,%d1
m68k_0397f0_end:
.org 0x397F6
m68k_0397f6:
        bne.w (. + 6)
m68k_0397f6_end:
.org 0x397FA
m68k_0397fa:
        rts
m68k_0397fa_end:
.org 0x397FC
m68k_0397fc:
        bsr.w (. + 3890)
m68k_0397fc_end:
.org 0x39800
m68k_039800:
        moveq #0,%d0
m68k_039800_end:
.org 0x39802
m68k_039802:
        cmpi.w #0xa,0xff7026:l
m68k_039802_end:
.org 0x3980A
m68k_03980a:
        bcc.w (. + 668)
m68k_03980a_end:
.org 0x3980E
m68k_03980e:
        move.w 0xf320:w,%d0
m68k_03980e_end:
.org 0x39812
m68k_039812:
        andi.w #0x7,%d0
m68k_039812_end:
.org 0x39816
m68k_039816:
        bne.w (. + 10)
m68k_039816_end:
.org 0x3981A
m68k_03981a:
        addq.w #0x1,0xff7004:l
m68k_03981a_end:
.org 0x39820
m68k_039820:
        moveq #0,%d1
m68k_039820_end:
.org 0x39822
m68k_039822:
        move.w 0xff7026:l,%d3
m68k_039822_end:
.org 0x39828
m68k_039828:
        asl.w #0x2,%d3
m68k_039828_end:
.org 0x3982A
m68k_03982a:
        lea.l -3610(%pc),%a1
m68k_03982a_end:
.org 0x3982E
m68k_03982e:
        movea.l (%a1, %d3.w),%a0
m68k_03982e_end:
.org 0x39832
m68k_039832:
        clr.l %d0
m68k_039832_end:
.org 0x39834
m68k_039834:
        move.w 0xff7004:l,%d0
m68k_039834_end:
.org 0x3983A
m68k_03983a:
        adda.w %d0,%a0
m68k_03983a_end:
.org 0x3983C
m68k_03983c:
        move.b (%a0),%d1
m68k_03983c_end:
.org 0x3983E
m68k_03983e:
        bpl.w (. + 22)
m68k_03983e_end:
.org 0x39842
m68k_039842:
        clr.l %d0
m68k_039842_end:
.org 0x39844
m68k_039844:
        adda.w #0x1,%a0
m68k_039844_end:
.org 0x39848
m68k_039848:
        move.b (%a0),%d1
m68k_039848_end:
.org 0x3984A
m68k_03984a:
        move.w %d1,0xff7004:l
m68k_03984a_end:
.org 0x39850
m68k_039850:
        bra.b (. + -48)
m68k_039850_end:
.org 0x39854
m68k_039854:
        cmpi.w #0x5,0xff7026:l
m68k_039854_end:
.org 0x3985C
m68k_03985c:
        beq.w (. + 192)
m68k_03985c_end:
.org 0x39860
m68k_039860:
        cmpi.w #0x1,0xff7026:l
m68k_039860_end:
.org 0x39868
m68k_039868:
        bne.w (. + 36)
m68k_039868_end:
.org 0x3988C
m68k_03988c:
        movem.w %d1,-(%a7)
m68k_03988c_end:
.org 0x39890
m68k_039890:
        jsr 326(%pc)
m68k_039890_end:
.org 0x39894
m68k_039894:
        nop
m68k_039894_end:
.org 0x39896
m68k_039896:
        clr.l %d0
m68k_039896_end:
.org 0x39898
m68k_039898:
        move.w 0xff7026:l,%d3
m68k_039898_end:
.org 0x3989E
m68k_03989e:
        asl.w #0x2,%d3
m68k_03989e_end:
.org 0x398A0
m68k_0398a0:
        lea.l -3194(%pc),%a6
m68k_0398a0_end:
.org 0x398A4
m68k_0398a4:
        movea.l (%a6, %d3.w),%a1
m68k_0398a4_end:
.org 0x398A8
m68k_0398a8:
        asl.w #0x2,%d1
m68k_0398a8_end:
.org 0x398AA
m68k_0398aa:
        adda.w %d1,%a1
m68k_0398aa_end:
.org 0x398AC
m68k_0398ac:
        movea.l (%a1),%a0
m68k_0398ac_end:
.org 0x398AE
m68k_0398ae:
        move.w 0xff7028:l,%d0
m68k_0398ae_end:
.org 0x398B4
m68k_0398b4:
        move.w 0xff702a:l,%d1
m68k_0398b4_end:
.org 0x398BA
m68k_0398ba:
        moveq #4,%d2
m68k_0398ba_end:
.org 0x398BC
m68k_0398bc:
        moveq #0,%d3
m68k_0398bc_end:
.org 0x398BE
m68k_0398be:
        moveq #0,%d4
m68k_0398be_end:
.org 0x398C0
m68k_0398c0:
        jsr 3294(%pc)
m68k_0398c0_end:
.org 0x398C4
m68k_0398c4:
        nop
m68k_0398c4_end:
.org 0x398C6
m68k_0398c6:
        movem.w (%a7)+,%d1
m68k_0398c6_end:
.org 0x398CA
m68k_0398ca:
        move.w 0xff7026:l,%d0
m68k_0398ca_end:
.org 0x398D0
m68k_0398d0:
        lea.l -3896(%pc),%a6
m68k_0398d0_end:
.org 0x398D4
m68k_0398d4:
        move.b (%a6, %d0.w),%d2
m68k_0398d4_end:
.org 0x398D8
m68k_0398d8:
        cmpi.b #0x1,%d2
m68k_0398d8_end:
.org 0x398DC
m68k_0398dc:
        bne.w (. + 56)
m68k_0398dc_end:
.org 0x39914
m68k_039914:
        bsr.w (. + 3642)
m68k_039914_end:
.org 0x39918
m68k_039918:
        bra.w (. + -336)
m68k_039918_end:
.org 0x399D8
m68k_0399d8:
        movem.w %d1,-(%a7)
m68k_0399d8_end:
.org 0x399DC
m68k_0399dc:
        move.w 0xf320:w,%d6
m68k_0399dc_end:
.org 0x399E0
m68k_0399e0:
        andi.w #0x7,%d6
m68k_0399e0_end:
.org 0x399E4
m68k_0399e4:
        bne.w (. + 88)
m68k_0399e4_end:
.org 0x399E8
m68k_0399e8:
        tst.b 0xff702c:l
m68k_0399e8_end:
.org 0x399EE
m68k_0399ee:
        beq.w (. + 78)
m68k_0399ee_end:
.org 0x39A3C
m68k_039a3c:
        movem.w (%a7)+,%d1
m68k_039a3c_end:
.org 0x39A40
m68k_039a40:
        rts
m68k_039a40_end:
.org 0x3A536
m68k_03a536:
        jsr 0x67ca:l
m68k_03a536_end:
.org 0x3A53C
m68k_03a53c:
        jsr 0x4942:l
m68k_03a53c_end:
.org 0x3A542
m68k_03a542:
        lea.l 0xc00004:l,%a6
m68k_03a542_end:
.org 0x3A548
m68k_03a548:
        move.w 0xf606:w,%d7
m68k_03a548_end:
.org 0x3A54C
m68k_03a54c:
        ori.b #0x10,%d7
m68k_03a54c_end:
.org 0x3A550
m68k_03a550:
        move.w %d7,(%a6)
m68k_03a550_end:
.org 0x3A552
m68k_03a552:
        move.w #0x100,0xa11100:l
m68k_03a552_end:
.org 0x3A55A
m68k_03a55a:
        move.l #0x94009340,(%a6)
m68k_03a55a_end:
.org 0x3A560
m68k_03a560:
        move.l #0x96fd9580,(%a6)
m68k_03a560_end:
.org 0x3A566
m68k_03a566:
        move.w #0x977f,(%a6)
m68k_03a566_end:
.org 0x3A56A
m68k_03a56a:
        move.w #0xc000,(%a6)
m68k_03a56a_end:
.org 0x3A56E
m68k_03a56e:
        move.w #0x80,0xf620:w
m68k_03a56e_end:
.org 0x3A574
m68k_03a574:
        move.w 0xf620:w,(%a6)
m68k_03a574_end:
.org 0x3A578
m68k_03a578:
        tst.b 0xffff3f00:l
m68k_03a578_end:
.org 0x3A57E
m68k_03a57e:
        bne.b (. + 10)
m68k_03a57e_end:
.org 0x3A580
m68k_03a580:
        move.w #0x0,0xa11100:l
m68k_03a580_end:
.org 0x3A588
m68k_03a588:
        move.w 0xf606:w,(%a6)
m68k_03a588_end:
.org 0x3A58C
m68k_03a58c:
        clr.w 0xf612:w
m68k_03a58c_end:
.org 0x3A590
m68k_03a590:
        move.w 0xf606:w,%d0
m68k_03a590_end:
.org 0x3A594
m68k_03a594:
        ori.b #0x40,%d0
m68k_03a594_end:
.org 0x3A598
m68k_03a598:
        move.w %d0,0xc00004:l
m68k_03a598_end:
.org 0x3A59E
m68k_03a59e:
        rts
m68k_03a59e_end:
.org 0x3A5A0
m68k_03a5a0:
        movem.l %d5-%d6/%a1,-(%a7)
m68k_03a5a0_end:
.org 0x3A5A4
m68k_03a5a4:
        cmpi.b #0x80,0xf300:w
m68k_03a5a4_end:
.org 0x3A5AA
m68k_03a5aa:
        bcc.w (. + 358)
m68k_03a5aa_end:
.org 0x3A5AE
m68k_03a5ae:
        andi.l #0xffff,%d4
m68k_03a5ae_end:
.org 0x3A5B4
m68k_03a5b4:
        move.w %d2,%d7
m68k_03a5b4_end:
.org 0x3A5B6
m68k_03a5b6:
        andi.w #0xfff8,%d2
m68k_03a5b6_end:
.org 0x3A5BA
m68k_03a5ba:
        andi.w #0x7,%d7
m68k_03a5ba_end:
.org 0x3A5BE
m68k_03a5be:
        asl.w #0x2,%d7
m68k_03a5be_end:
.org 0x3A5C0
m68k_03a5c0:
        addi.w #0x80,%d0
m68k_03a5c0_end:
.org 0x3A5C4
m68k_03a5c4:
        bmi.w (. + 332)
m68k_03a5c4_end:
.org 0x3A5C8
m68k_03a5c8:
        btst.l #0x5,%d2
m68k_03a5c8_end:
.org 0x3A5CC
m68k_03a5cc:
        beq.b (. + 6)
m68k_03a5cc_end:
.org 0x3A5D2
m68k_03a5d2:
        addi.w #0x80,%d1
m68k_03a5d2_end:
.org 0x3A5D6
m68k_03a5d6:
        btst.l #0x4,%d2
m68k_03a5d6_end:
.org 0x3A5DA
m68k_03a5da:
        beq.b (. + 6)
m68k_03a5da_end:
.org 0x3A5E0
m68k_03a5e0:
        clr.w %d5
m68k_03a5e0_end:
.org 0x3A5E2
m68k_03a5e2:
        move.b 0xf300:w,%d5
m68k_03a5e2_end:
.org 0x3A5E6
m68k_03a5e6:
        lsl.w #0x3,%d5
m68k_03a5e6_end:
.org 0x3A5E8
m68k_03a5e8:
        lea.l 0xf800:w,%a1
m68k_03a5e8_end:
.org 0x3A5EC
m68k_03a5ec:
        lea.l 0xff7006:l,%a2
m68k_03a5ec_end:
.org 0x3A5F2
m68k_03a5f2:
        lea.l (%a1, %d5.w),%a1
m68k_03a5f2_end:
.org 0x3A5F6
m68k_03a5f6:
        move.w %d0,%d6
m68k_03a5f6_end:
.org 0x3A5F8
m68k_03a5f8:
        clr.w 0xff7030:l
m68k_03a5f8_end:
.org 0x3A5FE
m68k_03a5fe:
        moveq #0,%d5
m68k_03a5fe_end:
.org 0x3A600
m68k_03a600:
        move.b (%a0),%d5
m68k_03a600_end:
.org 0x3A602
m68k_03a602:
        cmpi.b #0x80,%d5
m68k_03a602_end:
.org 0x3A606
m68k_03a606:
        beq.w (. + 266)
m68k_03a606_end:
.org 0x3A60A
m68k_03a60a:
        movem.l %d0-%d7/%a0-%a3,-(%a7)
m68k_03a60a_end:
.org 0x3A60E
m68k_03a60e:
        move.w 0xff7028:l,%d0
m68k_03a60e_end:
.org 0x3A614
m68k_03a614:
        btst.l #0x7,%d5
m68k_03a614_end:
.org 0x3A618
m68k_03a618:
        bne.w (. + 10)
m68k_03a618_end:
.org 0x3A61C
m68k_03a61c:
        add.w %d5,%d0
m68k_03a61c_end:
.org 0x3A61E
m68k_03a61e:
        bra.w (. + 8)
m68k_03a61e_end:
.org 0x3A622
m68k_03a622:
        neg.b %d5
m68k_03a622_end:
.org 0x3A624
m68k_03a624:
        sub.w %d5,%d0
m68k_03a624_end:
.org 0x3A626
m68k_03a626:
        cmpi.w #0x10,%d0
m68k_03a626_end:
.org 0x3A62A
m68k_03a62a:
        bcs.w (. + 236)
m68k_03a62a_end:
.org 0x3A62E
m68k_03a62e:
        cmpi.w #0x70,%d0
m68k_03a62e_end:
.org 0x3A632
m68k_03a632:
        bhi.w (. + 228)
m68k_03a632_end:
.org 0x3A636
m68k_03a636:
        movem.l (%a7)+,%d0-%d7/%a0-%a3
m68k_03a636_end:
.org 0x3A63A
m68k_03a63a:
        tst.w 0xff7030:l
m68k_03a63a_end:
.org 0x3A640
m68k_03a640:
        bne.w (. + 196)
m68k_03a640_end:
.org 0x3A644
m68k_03a644:
        btst.l #0x5,%d2
m68k_03a644_end:
.org 0x3A648
m68k_03a648:
        beq.w (. + 6)
m68k_03a648_end:
.org 0x3A64E
m68k_03a64e:
        btst.l #0x7,%d5
m68k_03a64e_end:
.org 0x3A652
m68k_03a652:
        beq.b (. + 8)
m68k_03a652_end:
.org 0x3A654
m68k_03a654:
        neg.b %d5
m68k_03a654_end:
.org 0x3A656
m68k_03a656:
        sub.w %d5,%d6
m68k_03a656_end:
.org 0x3A658
m68k_03a658:
        bra.b (. + 4)
m68k_03a658_end:
.org 0x3A65A
m68k_03a65a:
        add.w %d5,%d6
m68k_03a65a_end:
.org 0x3A65C
m68k_03a65c:
        move.w %d6,(%a1)
m68k_03a65c_end:
.org 0x3A65E
m68k_03a65e:
        move.w %d1,%d6
m68k_03a65e_end:
.org 0x3A660
m68k_03a660:
        move.b 0x3(%a0),%d5
m68k_03a660_end:
.org 0x3A664
m68k_03a664:
        clr.w 0xff7030:l
m68k_03a664_end:
.org 0x3A66A
m68k_03a66a:
        movem.l %d0-%d7/%a0-%a3,-(%a7)
m68k_03a66a_end:
.org 0x3A66E
m68k_03a66e:
        move.w 0xff702a:l,%d0
m68k_03a66e_end:
.org 0x3A674
m68k_03a674:
        btst.l #0x7,%d5
m68k_03a674_end:
.org 0x3A678
m68k_03a678:
        bne.w (. + 10)
m68k_03a678_end:
.org 0x3A67C
m68k_03a67c:
        add.w %d5,%d0
m68k_03a67c_end:
.org 0x3A67E
m68k_03a67e:
        bra.w (. + 8)
m68k_03a67e_end:
.org 0x3A682
m68k_03a682:
        neg.b %d5
m68k_03a682_end:
.org 0x3A684
m68k_03a684:
        sub.w %d5,%d0
m68k_03a684_end:
.org 0x3A686
m68k_03a686:
        cmpi.w #0x10,%d0
m68k_03a686_end:
.org 0x3A68A
m68k_03a68a:
        bcs.w (. + 152)
m68k_03a68a_end:
.org 0x3A68E
m68k_03a68e:
        cmpi.w #0xa0,%d0
m68k_03a68e_end:
.org 0x3A692
m68k_03a692:
        bhi.w (. + 144)
m68k_03a692_end:
.org 0x3A696
m68k_03a696:
        movem.l (%a7)+,%d0-%d7/%a0-%a3
m68k_03a696_end:
.org 0x3A69A
m68k_03a69a:
        tst.w 0xff7030:l
m68k_03a69a_end:
.org 0x3A6A0
m68k_03a6a0:
        bne.w (. + 100)
m68k_03a6a0_end:
.org 0x3A6A4
m68k_03a6a4:
        btst.l #0x4,%d2
m68k_03a6a4_end:
.org 0x3A6A8
m68k_03a6a8:
        beq.b (. + 4)
m68k_03a6a8_end:
.org 0x3A6AC
m68k_03a6ac:
        btst.l #0x7,%d5
m68k_03a6ac_end:
.org 0x3A6B0
m68k_03a6b0:
        beq.b (. + 8)
m68k_03a6b0_end:
.org 0x3A6B2
m68k_03a6b2:
        neg.b %d5
m68k_03a6b2_end:
.org 0x3A6B4
m68k_03a6b4:
        sub.w %d5,%d6
m68k_03a6b4_end:
.org 0x3A6B6
m68k_03a6b6:
        bra.b (. + 4)
m68k_03a6b6_end:
.org 0x3A6B8
m68k_03a6b8:
        add.w %d5,%d6
m68k_03a6b8_end:
.org 0x3A6BA
m68k_03a6ba:
        move.w %d6,0x6(%a1)
m68k_03a6ba_end:
.org 0x3A6BE
m68k_03a6be:
        move.b 0x1(%a0),0x2(%a1)
m68k_03a6be_end:
.org 0x3A6C4
m68k_03a6c4:
        tst.l (%a2, %d7.w)
m68k_03a6c4_end:
.org 0x3A6C8
m68k_03a6c8:
        bne.w (. + 16)
m68k_03a6c8_end:
.org 0x3A6CC
m68k_03a6cc:
        move.l %a1,(%a2, %d7.w)
m68k_03a6cc_end:
.org 0x3A6D0
m68k_03a6d0:
        move.b 0xf300:w,0x20(%a2, %d7.w)
m68k_03a6d0_end:
.org 0x3A6D6
m68k_03a6d6:
        bra.b (. + 12)
m68k_03a6d6_end:
.org 0x3A6D8
m68k_03a6d8:
        movea.l 0x40(%a2, %d7.w),%a3
m68k_03a6d8_end:
.org 0x3A6DC
m68k_03a6dc:
        move.b 0xf300:w,0x3(%a3)
m68k_03a6dc_end:
.org 0x3A6E2
m68k_03a6e2:
        move.l %a1,0x40(%a2, %d7.w)
m68k_03a6e2_end:
.org 0x3A6E6
m68k_03a6e6:
        addq.b #0x1,0xf300:w
m68k_03a6e6_end:
.org 0x3A6EA
m68k_03a6ea:
        move.b 0x1(%a0),%d5
m68k_03a6ea_end:
.org 0x3A6EE
m68k_03a6ee:
        andi.w #0xf0,%d5
m68k_03a6ee_end:
.org 0x3A6F2
m68k_03a6f2:
        add.b %d3,%d5
m68k_03a6f2_end:
.org 0x3A6F4
m68k_03a6f4:
        eor.w %d2,%d5
m68k_03a6f4_end:
.org 0x3A6F6
m68k_03a6f6:
        asl.w #0x7,%d5
m68k_03a6f6_end:
.org 0x3A6F8
m68k_03a6f8:
        or.b 0x2(%a0),%d5
m68k_03a6f8_end:
.org 0x3A6FC
m68k_03a6fc:
        add.w %d4,%d5
m68k_03a6fc_end:
.org 0x3A6FE
m68k_03a6fe:
        move.w %d5,0x4(%a1)
m68k_03a6fe_end:
.org 0x3A702
m68k_03a702:
        addq.l #0x8,%a1
m68k_03a702_end:
.org 0x3A704
m68k_03a704:
        addq.l #0x4,%a0
m68k_03a704_end:
.org 0x3A706
m68k_03a706:
        cmpi.b #0x80,0xf300:w
m68k_03a706_end:
.org 0x3A70C
m68k_03a70c:
        bcs.w (. + -278)
m68k_03a70c_end:
.org 0x3A710
m68k_03a710:
        movem.l (%a7)+,%d5-%d6/%a1
m68k_03a710_end:
.org 0x3A714
m68k_03a714:
        rts
m68k_03a714_end:
.org 0x3A72E
m68k_03a72e:
        subi.w #0x40,%d0
m68k_03a72e_end:
.org 0x3A732
m68k_03a732:
        subi.w #0x40,%d1
m68k_03a732_end:
.org 0x3A736
m68k_03a736:
        moveq #0,%d2
m68k_03a736_end:
.org 0x3A738
m68k_03a738:
        moveq #0,%d3
m68k_03a738_end:
.org 0x3A73A
m68k_03a73a:
        move.w #0x0,%d4
m68k_03a73a_end:
.org 0x3A73E
m68k_03a73e:
        lea.l 8(%pc),%a0
m68k_03a73e_end:
.org 0x3A742
m68k_03a742:
        nop
m68k_03a742_end:
.org 0x3A744
m68k_03a744:
        jmp -422(%pc)
m68k_03a744_end:
.org 0x3A74E
m68k_03a74e:
        moveq #28,%d0
m68k_03a74e_end:
.org 0x3A750
m68k_03a750:
        moveq #0,%d1
m68k_03a750_end:
.org 0x3A752
m68k_03a752:
        lea.l 0xff7006:l,%a0
m68k_03a752_end:
.org 0x3A758
m68k_03a758:
        bsr.b (. + 52)
m68k_03a758_end:
.org 0x3A75A
m68k_03a75a:
        subq.w #0x4,%d0
m68k_03a75a_end:
.org 0x3A75C
m68k_03a75c:
        bpl.b (. + -4)
m68k_03a75c_end:
.org 0x3A75E
m68k_03a75e:
        lea.l 0xff7006:l,%a0
m68k_03a75e_end:
.org 0x3A764
m68k_03a764:
        moveq #0,%d0
m68k_03a764_end:
.org 0x3A766
m68k_03a766:
        move.l %d0,(%a0)
m68k_03a766_end:
.org 0x3A768
m68k_03a768:
        move.l %d0,0x4(%a0)
m68k_03a768_end:
.org 0x3A76C
m68k_03a76c:
        move.l %d0,0x8(%a0)
m68k_03a76c_end:
.org 0x3A770
m68k_03a770:
        move.l %d0,0xc(%a0)
m68k_03a770_end:
.org 0x3A774
m68k_03a774:
        move.l %d0,0x10(%a0)
m68k_03a774_end:
.org 0x3A778
m68k_03a778:
        move.l %d0,0x14(%a0)
m68k_03a778_end:
.org 0x3A77C
m68k_03a77c:
        move.l %d0,0x18(%a0)
m68k_03a77c_end:
.org 0x3A780
m68k_03a780:
        move.l %d0,0x1c(%a0)
m68k_03a780_end:
.org 0x3A784
m68k_03a784:
        move.b #0x0,0xf300:w
m68k_03a784_end:
.org 0x3A78A
m68k_03a78a:
        rts
m68k_03a78a_end:
.org 0x3A78C
m68k_03a78c:
        tst.l (%a0, %d0.w)
m68k_03a78c_end:
.org 0x3A790
m68k_03a790:
        beq.w (. + 16)
m68k_03a790_end:
.org 0x3A794
m68k_03a794:
        movea.l 0x40(%a0, %d0.w),%a1
m68k_03a794_end:
.org 0x3A798
m68k_03a798:
        move.b %d1,0x3(%a1)
m68k_03a798_end:
.org 0x3A79C
m68k_03a79c:
        move.b 0x20(%a0, %d0.w),%d1
m68k_03a79c_end:
.org 0x3A7A0
m68k_03a7a0:
        rts
m68k_03a7a0_end:
.org 0x3A978
m68k_03a978:
        move.w 0x80c4:w,%d0
m68k_03a978_end:
.org 0x3A97C
m68k_03a97c:
        bmi.w (. + 60)
m68k_03a97c_end:
.org 0x3A980
m68k_03a980:
        subq.w #0x1,0x80c6:w
m68k_03a980_end:
.org 0x3A984
m68k_03a984:
        bpl.w (. + 52)
m68k_03a984_end:
.org 0x3A988
m68k_03a988:
        andi.w #0xff,%d0
m68k_03a988_end:
.org 0x3A98C
m68k_03a98c:
        move.w %d0,0x80c6:w
m68k_03a98c_end:
.org 0x3A990
m68k_03a990:
        cmpi.b #0x0,0x80c4:w
m68k_03a990_end:
.org 0x3A996
m68k_03a996:
        beq.b (. + 20)
m68k_03a996_end:
.org 0x3A9AA
m68k_03a9aa:
        subq.w #0x1,0x80c8:w
m68k_03a9aa_end:
.org 0x3A9AE
m68k_03a9ae:
        bpl.w (. + 12)
m68k_03a9ae_end:
.org 0x3A9B2
m68k_03a9b2:
        move.w #0xffff,0x80c4:w
m68k_03a9b2_end:
.org 0x3A9B8
m68k_03a9b8:
        rts
m68k_03a9b8_end:
.org 0x3A9BA
m68k_03a9ba:
        move.w 0x80c8:w,%d0
m68k_03a9ba_end:
.org 0x3A9BE
m68k_03a9be:
        andi.w #0xe,%d0
m68k_03a9be_end:
.org 0x3A9C2
m68k_03a9c2:
        move.w %d0,0x8000:w
m68k_03a9c2_end:
.org 0x3A9C6
m68k_03a9c6:
        lea.l 0xfb00:w,%a0
m68k_03a9c6_end:
.org 0x3A9CA
m68k_03a9ca:
        lea.l 0xfb80:w,%a1
m68k_03a9ca_end:
.org 0x3A9CE
m68k_03a9ce:
        lea.l 0x80ca:w,%a2
m68k_03a9ce_end:
.org 0x3A9D2
m68k_03a9d2:
        moveq #0,%d2
m68k_03a9d2_end:
.org 0x3A9D4
m68k_03a9d4:
        moveq #0,%d7
m68k_03a9d4_end:
.org 0x3A9D6
m68k_03a9d6:
        moveq #31,%d1
m68k_03a9d6_end:
.org 0x3A9D8
m68k_03a9d8:
        move.l (%a2, %d7.w),%d6
m68k_03a9d8_end:
.org 0x3A9DC
m68k_03a9dc:
        lsr.l #0x1,%d6
m68k_03a9dc_end:
.org 0x3A9DE
m68k_03a9de:
        bcc.w (. + 28)
m68k_03a9de_end:
.org 0x3A9E2
m68k_03a9e2:
        clr.w %d5
m68k_03a9e2_end:
.org 0x3A9E4
m68k_03a9e4:
        move.w (%a1, %d2.w),%d3
m68k_03a9e4_end:
.org 0x3A9E8
m68k_03a9e8:
        bsr.w (. + 34)
m68k_03a9e8_end:
.org 0x3A9EC
m68k_03a9ec:
        bsr.w (. + 30)
m68k_03a9ec_end:
.org 0x3A9F0
m68k_03a9f0:
        bsr.w (. + 26)
m68k_03a9f0_end:
.org 0x3A9F4
m68k_03a9f4:
        ror.w #0x4,%d5
m68k_03a9f4_end:
.org 0x3A9F6
m68k_03a9f6:
        move.w %d5,(%a0, %d2.w)
m68k_03a9f6_end:
.org 0x3A9FA
m68k_03a9fa:
        addq.w #0x2,%d2
m68k_03a9fa_end:
.org 0x3A9FC
m68k_03a9fc:
        dbra %d1,(. + -32)
m68k_03a9fc_end:
.org 0x3AA00
m68k_03aa00:
        addq.w #0x4,%d7
m68k_03aa00_end:
.org 0x3AA02
m68k_03aa02:
        cmpi.w #0x8,%d7
m68k_03aa02_end:
.org 0x3AA06
m68k_03aa06:
        bcs.b (. + -48)
m68k_03aa06_end:
.org 0x3AA08
m68k_03aa08:
        rts
m68k_03aa08_end:
.org 0x3AA0A
m68k_03aa0a:
        move.b %d3,%d4
m68k_03aa0a_end:
.org 0x3AA0C
m68k_03aa0c:
        andi.w #0xe,%d4
m68k_03aa0c_end:
.org 0x3AA10
m68k_03aa10:
        sub.b 0x8001:w,%d4
m68k_03aa10_end:
.org 0x3AA14
m68k_03aa14:
        bcc.b (. + 4)
m68k_03aa14_end:
.org 0x3AA16
m68k_03aa16:
        moveq #0,%d4
m68k_03aa16_end:
.org 0x3AA18
m68k_03aa18:
        or.w %d4,%d5
m68k_03aa18_end:
.org 0x3AA1A
m68k_03aa1a:
        ror.w #0x4,%d5
m68k_03aa1a_end:
.org 0x3AA1C
m68k_03aa1c:
        lsr.w #0x4,%d3
m68k_03aa1c_end:
.org 0x3AA1E
m68k_03aa1e:
        rts
m68k_03aa1e_end:
.org 0x3AA20
m68k_03aa20:
        andi.w #0xff,%d0
m68k_03aa20_end:
.org 0x3AA24
m68k_03aa24:
        move.w %d0,0x80c4:w
m68k_03aa24_end:
.org 0x3AA28
m68k_03aa28:
        move.w #0x0,0x80c6:w
m68k_03aa28_end:
.org 0x3AA2E
m68k_03aa2e:
        move.w #0xf,0x80c8:w
m68k_03aa2e_end:
.org 0x3AA34
m68k_03aa34:
        rts
m68k_03aa34_end:
.org 0x3AA8A
m68k_03aa8a:
        moveq #31,%d1
m68k_03aa8a_end:
.org 0x3AA8C
m68k_03aa8c:
        lea.l 0xfb00:w,%a0
m68k_03aa8c_end:
.org 0x3AA90
m68k_03aa90:
        lea.l 0xfb80:w,%a1
m68k_03aa90_end:
.org 0x3AA94
m68k_03aa94:
        move.l (%a0),(%a1)+
m68k_03aa94_end:
.org 0x3AA96
m68k_03aa96:
        clr.l (%a0)+
m68k_03aa96_end:
.org 0x3AA98
m68k_03aa98:
        dbra %d1,(. + -4)
m68k_03aa98_end:
.org 0x3AA9C
m68k_03aa9c:
        rts
m68k_03aa9c_end:
.org 0x3AAB6
m68k_03aab6:
        clr.w 0x8000:w
m68k_03aab6_end:
.org 0x3AABA
m68k_03aaba:
        move.w #0x1,0x8002:w
m68k_03aaba_end:
.org 0x3AAC0
m68k_03aac0:
        bra.b (. + 26)
m68k_03aac0_end:
.org 0x3AACE
m68k_03aace:
        clr.w 0x8000:w
m68k_03aace_end:
.org 0x3AAD2
m68k_03aad2:
        move.w #0x20,%d6
m68k_03aad2_end:
.org 0x3AAD6
m68k_03aad6:
        clr.w 0x8002:w
m68k_03aad6_end:
.org 0x3AADA
m68k_03aada:
        move.w #0x8f02,0xc00004:l
m68k_03aada_end:
.org 0x3AAE2
m68k_03aae2:
        move.w %a1,%d0
m68k_03aae2_end:
.org 0x3AAE4
m68k_03aae4:
        bsr.w (. + 1996)
m68k_03aae4_end:
.org 0x3AAE8
m68k_03aae8:
        moveq #0,%d4
m68k_03aae8_end:
.org 0x3AAEA
m68k_03aaea:
        tst.w 0x8002:w
m68k_03aaea_end:
.org 0x3AAEE
m68k_03aaee:
        bne.b (. + 4)
m68k_03aaee_end:
.org 0x3AAF0
m68k_03aaf0:
        move.b (%a0)+,%d1
m68k_03aaf0_end:
.org 0x3AAF2
m68k_03aaf2:
        move.b (%a0)+,%d2
m68k_03aaf2_end:
.org 0x3AAF4
m68k_03aaf4:
        tst.w 0x8002:w
m68k_03aaf4_end:
.org 0x3AAF8
m68k_03aaf8:
        bne.b (. + 8)
m68k_03aaf8_end:
.org 0x3AAFA
m68k_03aafa:
        cmp.b %d2,%d1
m68k_03aafa_end:
.org 0x3AAFC
m68k_03aafc:
        beq.w (. + 22)
m68k_03aafc_end:
.org 0x3AB00
m68k_03ab00:
        asl.w #0x8,%d2
m68k_03ab00_end:
.org 0x3AB02
m68k_03ab02:
        move.b (%a0)+,%d2
m68k_03ab02_end:
.org 0x3AB04
m68k_03ab04:
        or.w 0x8000:w,%d2
m68k_03ab04_end:
.org 0x3AB08
m68k_03ab08:
        move.w %d2,0xc00000:l
m68k_03ab08_end:
.org 0x3AB0E
m68k_03ab0e:
        bsr.b (. + 36)
m68k_03ab0e_end:
.org 0x3AB10
m68k_03ab10:
        bra.b (. + -30)
m68k_03ab10_end:
.org 0x3AB12
m68k_03ab12:
        moveq #0,%d3
m68k_03ab12_end:
.org 0x3AB14
m68k_03ab14:
        move.b (%a0)+,%d3
m68k_03ab14_end:
.org 0x3AB16
m68k_03ab16:
        beq.w (. + 58)
m68k_03ab16_end:
.org 0x3AB1A
m68k_03ab1a:
        move.b (%a0)+,%d2
m68k_03ab1a_end:
.org 0x3AB1C
m68k_03ab1c:
        asl.w #0x8,%d2
m68k_03ab1c_end:
.org 0x3AB1E
m68k_03ab1e:
        move.b (%a0)+,%d2
m68k_03ab1e_end:
.org 0x3AB20
m68k_03ab20:
        or.w 0x8000:w,%d2
m68k_03ab20_end:
.org 0x3AB24
m68k_03ab24:
        move.w %d2,0xc00000:l
m68k_03ab24_end:
.org 0x3AB2A
m68k_03ab2a:
        bsr.b (. + 8)
m68k_03ab2a_end:
.org 0x3AB2C
m68k_03ab2c:
        dbra %d3,(. + -12)
m68k_03ab2c_end:
.org 0x3AB30
m68k_03ab30:
        bra.b (. + -62)
m68k_03ab30_end:
.org 0x3AB32
m68k_03ab32:
        addq.w #0x1,%d4
m68k_03ab32_end:
.org 0x3AB34
m68k_03ab34:
        cmpi.b #0x20,%d4
m68k_03ab34_end:
.org 0x3AB38
m68k_03ab38:
        bcs.w (. + 24)
m68k_03ab38_end:
.org 0x3AB3C
m68k_03ab3c:
        subq.w #0x1,%d6
m68k_03ab3c_end:
.org 0x3AB3E
m68k_03ab3e:
        bne.b (. + 8)
m68k_03ab3e_end:
.org 0x3AB40
m68k_03ab40:
        movem.l (%a7)+,%d0
m68k_03ab40_end:
.org 0x3AB44
m68k_03ab44:
        rts
m68k_03ab44_end:
.org 0x3AB46
m68k_03ab46:
        adda.l %d5,%a1
m68k_03ab46_end:
.org 0x3AB48
m68k_03ab48:
        move.w %a1,%d0
m68k_03ab48_end:
.org 0x3AB4A
m68k_03ab4a:
        bsr.w (. + 1894)
m68k_03ab4a_end:
.org 0x3AB4E
m68k_03ab4e:
        moveq #0,%d4
m68k_03ab4e_end:
.org 0x3AB50
m68k_03ab50:
        rts
m68k_03ab50_end:
.org 0x3AB52
m68k_03ab52:
        move.w #0x8f02,0xc00004:l
m68k_03ab52_end:
.org 0x3AB5A
m68k_03ab5a:
        bsr.w (. + 1878)
m68k_03ab5a_end:
.org 0x3AB5E
m68k_03ab5e:
        move.b (%a0)+,%d1
m68k_03ab5e_end:
.org 0x3AB60
m68k_03ab60:
        move.b (%a0)+,%d2
m68k_03ab60_end:
.org 0x3AB62
m68k_03ab62:
        cmp.b %d2,%d1
m68k_03ab62_end:
.org 0x3AB64
m68k_03ab64:
        beq.w (. + 18)
m68k_03ab64_end:
.org 0x3AB68
m68k_03ab68:
        move.b (%a0)+,%d4
m68k_03ab68_end:
.org 0x3AB6A
m68k_03ab6a:
        asl.w #0x8,%d4
m68k_03ab6a_end:
.org 0x3AB6C
m68k_03ab6c:
        move.b %d2,%d4
m68k_03ab6c_end:
.org 0x3AB6E
m68k_03ab6e:
        move.w %d4,0xc00000:l
m68k_03ab6e_end:
.org 0x3AB74
m68k_03ab74:
        bra.b (. + -20)
m68k_03ab74_end:
.org 0x3AB76
m68k_03ab76:
        moveq #0,%d3
m68k_03ab76_end:
.org 0x3AB78
m68k_03ab78:
        move.b (%a0)+,%d3
m68k_03ab78_end:
.org 0x3AB7A
m68k_03ab7a:
        beq.w (. + 24)
m68k_03ab7a_end:
.org 0x3AB7E
m68k_03ab7e:
        move.b (%a0)+,%d2
m68k_03ab7e_end:
.org 0x3AB80
m68k_03ab80:
        move.b (%a0)+,%d4
m68k_03ab80_end:
.org 0x3AB82
m68k_03ab82:
        asl.w #0x8,%d4
m68k_03ab82_end:
.org 0x3AB84
m68k_03ab84:
        move.b %d2,%d4
m68k_03ab84_end:
.org 0x3AB86
m68k_03ab86:
        move.w %d4,0xc00000:l
m68k_03ab86_end:
.org 0x3AB8C
m68k_03ab8c:
        dbra %d3,(. + -6)
m68k_03ab8c_end:
.org 0x3AB90
m68k_03ab90:
        bra.b (. + -48)
m68k_03ab90_end:
.org 0x3AB92
m68k_03ab92:
        rts
m68k_03ab92_end:
.org 0x3AB94
m68k_03ab94:
        lea.l 22(%pc),%a1
m68k_03ab94_end:
.org 0x3AB98
m68k_03ab98:
        nop
m68k_03ab98_end:
.org 0x3AB9A
m68k_03ab9a:
        lsl.w #0x3,%d0
m68k_03ab9a_end:
.org 0x3AB9C
m68k_03ab9c:
        adda.w %d0,%a1
m68k_03ab9c_end:
.org 0x3AB9E
m68k_03ab9e:
        movea.l (%a1)+,%a2
m68k_03ab9e_end:
.org 0x3ABA0
m68k_03aba0:
        movea.w (%a1)+,%a3
m68k_03aba0_end:
.org 0x3ABA2
m68k_03aba2:
        move.w (%a1)+,%d7
m68k_03aba2_end:
.org 0x3ABA4
m68k_03aba4:
        move.l (%a2)+,(%a3)+
m68k_03aba4_end:
.org 0x3ABA6
m68k_03aba6:
        dbra %d7,(. + -2)
m68k_03aba6_end:
.org 0x3ABAA
m68k_03abaa:
        rts
m68k_03abaa_end:
.org 0x3B2B0
m68k_03b2b0:
        movem.l %d1,-(%a7)
m68k_03b2b0_end:
.org 0x3B2B4
m68k_03b2b4:
        andi.l #0xffff,%d0
m68k_03b2b4_end:
.org 0x3B2BA
m68k_03b2ba:
        move.l %d0,%d1
m68k_03b2ba_end:
.org 0x3B2BC
m68k_03b2bc:
        andi.w #0x3fff,%d0
m68k_03b2bc_end:
.org 0x3B2C0
m68k_03b2c0:
        ori.w #0x4000,%d0
m68k_03b2c0_end:
.org 0x3B2C4
m68k_03b2c4:
        swap %d0
m68k_03b2c4_end:
.org 0x3B2C6
m68k_03b2c6:
        lsr.w #0x8,%d1
m68k_03b2c6_end:
.org 0x3B2C8
m68k_03b2c8:
        lsr.w #0x6,%d1
m68k_03b2c8_end:
.org 0x3B2CA
m68k_03b2ca:
        or.l %d1,%d0
m68k_03b2ca_end:
.org 0x3B2CC
m68k_03b2cc:
        move.l %d0,0xc00004:l
m68k_03b2cc_end:
.org 0x3B2D2
m68k_03b2d2:
        movem.l (%a7)+,%d1
m68k_03b2d2_end:
.org 0x3B2D6
m68k_03b2d6:
        rts
m68k_03b2d6_end:
.org 0x3D654
m68k_03d654:
        move.w #0x2700,%sr
m68k_03d654_end:
.org 0x3D658
m68k_03d658:
        move.w 0xf606:w,%d0
m68k_03d658_end:
.org 0x3D65C
m68k_03d65c:
        andi.b #0xbf,%d0
m68k_03d65c_end:
.org 0x3D660
m68k_03d660:
        move.w %d0,0xc00004:l
m68k_03d660_end:
.org 0x3D666
m68k_03d666:
        jsr 0x68ce:l
m68k_03d666_end:
.org 0x3D66C
m68k_03d66c:
        move.w #0x2,0xf6c4:w
m68k_03d66c_end:
.org 0x3D820
m68k_03d820:
        cmpi.w #0x3,0x813a:w
m68k_03d820_end:
.org 0x3D826
m68k_03d826:
        bne.b (. + 36)
m68k_03d826_end:
.org 0x3D828
m68k_03d828:
        cmpi.w #0x3,0x813c:w
m68k_03d828_end:
.org 0x3D82E
m68k_03d82e:
        bne.b (. + 28)
m68k_03d82e_end:
.org 0x3D830
m68k_03d830:
        move.w #0x1,0x8114:w
m68k_03d830_end:
.org 0x3D836
m68k_03d836:
        move.w #0x2700,%sr
m68k_03d836_end:
.org 0x3D83A
m68k_03d83a:
        move.w 0xf606:w,%d0
m68k_03d83a_end:
.org 0x3D83E
m68k_03d83e:
        andi.b #0xbf,%d0
m68k_03d83e_end:
.org 0x3D842
m68k_03d842:
        move.w %d0,0xc00004:l
m68k_03d842_end:
.org 0x3D848
m68k_03d848:
        rts
m68k_03d848_end:
.org 0x3DD14
m68k_03dd14:
        tst.b 0x80da:w
m68k_03dd14_end:
.org 0x3DD18
m68k_03dd18:
        beq.b (. + 26)
m68k_03dd18_end:
.org 0x3DD1A
m68k_03dd1a:
        cmpi.b #0x3,0x80da:w
m68k_03dd1a_end:
.org 0x3DD20
m68k_03dd20:
        beq.w (. + 18)
m68k_03dd20_end:
.org 0x3DD24
m68k_03dd24:
        cmpi.b #0x1,0x80da:w
m68k_03dd24_end:
.org 0x3DD2A
m68k_03dd2a:
        bne.w (. + 380)
m68k_03dd2a_end:
.org 0x3DD2E
m68k_03dd2e:
        bra.w (. + 376)
m68k_03dd2e_end:
.org 0x3DD32
m68k_03dd32:
        lea.l 0xc700:w,%a0
m68k_03dd32_end:
.org 0x3DD36
m68k_03dd36:
        moveq #0,%d1
m68k_03dd36_end:
.org 0x3DD38
m68k_03dd38:
        move.w 0x80e0:w,%d0
m68k_03dd38_end:
.org 0x3DD3C
m68k_03dd3c:
        move.b (%a0, %d0.w),%d1
m68k_03dd3c_end:
.org 0x3DD40
m68k_03dd40:
        andi.w #0x3,%d1
m68k_03dd40_end:
.org 0x3DD44
m68k_03dd44:
        move.w 0x80e2:w,%d0
m68k_03dd44_end:
.org 0x3DD48
m68k_03dd48:
        move.b (%a0, %d0.w),%d0
m68k_03dd48_end:
.org 0x3DD4C
m68k_03dd4c:
        andi.w #0x3,%d0
m68k_03dd4c_end:
.org 0x3DD50
m68k_03dd50:
        sub.b %d0,%d1
m68k_03dd50_end:
.org 0x3DD52
m68k_03dd52:
        addq.w #0x1,%d1
m68k_03dd52_end:
.org 0x3DD54
m68k_03dd54:
        cmpi.w #0x2,%d1
m68k_03dd54_end:
.org 0x3DD58
m68k_03dd58:
        bhi.w (. + 204)
m68k_03dd58_end:
.org 0x3DD5C
m68k_03dd5c:
        move.w 0x810e:w,%d0
m68k_03dd5c_end:
.org 0x3DD60
m68k_03dd60:
        addi.w #0xa,%d0
m68k_03dd60_end:
.org 0x3DD64
m68k_03dd64:
        cmp.w 0x810c:w,%d0
m68k_03dd64_end:
.org 0x3DD68
m68k_03dd68:
        bcs.w (. + 188)
m68k_03dd68_end:
.org 0x3DD6C
m68k_03dd6c:
        move.w 0x8106:w,%d0
m68k_03dd6c_end:
.org 0x3DD70
m68k_03dd70:
        addi.w #0x14,%d0
m68k_03dd70_end:
.org 0x3DD74
m68k_03dd74:
        cmp.w 0x8104:w,%d0
m68k_03dd74_end:
.org 0x3DD78
m68k_03dd78:
        bcs.w (. + 172)
m68k_03dd78_end:
.org 0x3DD7C
m68k_03dd7c:
        move.w 0x80e6:w,%d0
m68k_03dd7c_end:
.org 0x3DD80
m68k_03dd80:
        cmp.w 0x80e4:w,%d0
m68k_03dd80_end:
.org 0x3DD84
m68k_03dd84:
        bcc.w (. + 160)
m68k_03dd84_end:
.org 0x3DD88
m68k_03dd88:
        jsr -9832(%pc)
m68k_03dd88_end:
.org 0x3DD8C
m68k_03dd8c:
        andi.w #0x3,%d0
m68k_03dd8c_end:
.org 0x3DD90
m68k_03dd90:
        bne.w (. + 148)
m68k_03dd90_end:
.org 0x3DF26
m68k_03df26:
        btst.b #0x5,0x811f:w
m68k_03df26_end:
.org 0x3DF2C
m68k_03df2c:
        beq.w (. + 808)
m68k_03df2c_end:
.org 0x3DF30
m68k_03df30:
        move.w #0xac,%d0
m68k_03df30_end:
.org 0x3DF34
m68k_03df34:
        jsr 0x808a:l
m68k_03df34_end:
.org 0x3DF3A
m68k_03df3a:
        tst.w 0x8142:w
m68k_03df3a_end:
.org 0x3DF3E
m68k_03df3e:
        bne.w (. + 632)
m68k_03df3e_end:
.org 0x3DF42
m68k_03df42:
        cmpi.b #0x1,0x80da:w
m68k_03df42_end:
.org 0x3DF48
m68k_03df48:
        beq.w (. + 492)
m68k_03df48_end:
.org 0x3DF4C
m68k_03df4c:
        cmpi.b #0x2,0x80da:w
m68k_03df4c_end:
.org 0x3DF52
m68k_03df52:
        beq.w (. + 482)
m68k_03df52_end:
.org 0x3DF56
m68k_03df56:
        move.w #0x2700,%sr
m68k_03df56_end:
.org 0x3DF5A
m68k_03df5a:
        moveq #0,%d1
m68k_03df5a_end:
.org 0x3DF5C
m68k_03df5c:
        moveq #0,%d2
m68k_03df5c_end:
.org 0x3DF5E
m68k_03df5e:
        lea.l 0xc700:w,%a0
m68k_03df5e_end:
.org 0x3DF62
m68k_03df62:
        move.w 0x80e0:w,%d0
m68k_03df62_end:
.org 0x3DF66
m68k_03df66:
        move.b (%a0, %d0.w),%d0
m68k_03df66_end:
.org 0x3DF6A
m68k_03df6a:
        andi.w #0x3,%d0
m68k_03df6a_end:
.org 0x3DF6E
m68k_03df6e:
        moveq #5,%d1
m68k_03df6e_end:
.org 0x3DF70
m68k_03df70:
        sub.b %d0,%d1
m68k_03df70_end:
.org 0x3DF72
m68k_03df72:
        move.w 0x80e2:w,%d0
m68k_03df72_end:
.org 0x3DF76
m68k_03df76:
        move.b (%a0, %d0.w),%d0
m68k_03df76_end:
.org 0x3DF7A
m68k_03df7a:
        moveq #5,%d2
m68k_03df7a_end:
.org 0x3DF7C
m68k_03df7c:
        sub.b %d0,%d2
m68k_03df7c_end:
.org 0x3DF7E
m68k_03df7e:
        move.w 0x8104:w,%d0
m68k_03df7e_end:
.org 0x3DF82
m68k_03df82:
        mulu.w %d0,%d1
m68k_03df82_end:
.org 0x3DF84
m68k_03df84:
        mulu.w #0x64,%d1
m68k_03df84_end:
.org 0x3DF88
m68k_03df88:
        jsr -10344(%pc)
m68k_03df88_end:
.org 0x3DF8C
m68k_03df8c:
        andi.w #0x1f,%d0
m68k_03df8c_end:
.org 0x3DF90
m68k_03df90:
        addi.w #0x14,%d0
m68k_03df90_end:
.org 0x3DF94
m68k_03df94:
        add.w 0x8106:w,%d0
m68k_03df94_end:
.org 0x3DF98
m68k_03df98:
        mulu.w %d0,%d2
m68k_03df98_end:
.org 0x3DF9A
m68k_03df9a:
        divu.w %d2,%d1
m68k_03df9a_end:
.org 0x3DF9C
m68k_03df9c:
        cmpi.w #0x64,%d1
m68k_03df9c_end:
.org 0x3DFA0
m68k_03dfa0:
        bhi.w (. + 46)
m68k_03dfa0_end:
.org 0x3DFA4
m68k_03dfa4:
        jsr -10372(%pc)
m68k_03dfa4_end:
.org 0x3DFA8
m68k_03dfa8:
        andi.w #0x7f,%d0
m68k_03dfa8_end:
.org 0x3DFAC
m68k_03dfac:
        cmpi.w #0x64,%d0
m68k_03dfac_end:
.org 0x3DFB0
m68k_03dfb0:
        bhi.b (. + -12)
m68k_03dfb0_end:
.org 0x3DFB2
m68k_03dfb2:
        cmp.w %d1,%d0
m68k_03dfb2_end:
.org 0x3DFB4
m68k_03dfb4:
        bhi.w (. + 210)
m68k_03dfb4_end:
.org 0x3DFB8
m68k_03dfb8:
        jsr -10392(%pc)
m68k_03dfb8_end:
.org 0x3DFBC
m68k_03dfbc:
        move.w 0xefd2:w,%d1
m68k_03dfbc_end:
.org 0x3DFC0
m68k_03dfc0:
        lea.l 192(%pc),%a0
m68k_03dfc0_end:
.org 0x3DFC4
m68k_03dfc4:
        nop
m68k_03dfc4_end:
.org 0x3DFC6
m68k_03dfc6:
        and.b (%a0, %d1.w),%d0
m68k_03dfc6_end:
.org 0x3DFCA
m68k_03dfca:
        bne.w (. + 188)
m68k_03dfca_end:
.org 0x3F0DE
m68k_03f0de:
        bsr.w (. + 2046)
m68k_03f0de_end:
.org 0x3F0E2
m68k_03f0e2:
        move.w #0xffff,0x80ca:w
m68k_03f0e2_end:
.org 0x3F0E8
m68k_03f0e8:
        move.w #0xffff,0x80cc:w
m68k_03f0e8_end:
.org 0x3F0EE
m68k_03f0ee:
        move.w #0xffff,0x80ce:w
m68k_03f0ee_end:
.org 0x3F0F4
m68k_03f0f4:
        move.w #0xffff,0x80d0:w
m68k_03f0f4_end:
.org 0x3F0FA
m68k_03f0fa:
        moveq #1,%d0
m68k_03f0fa_end:
.org 0x3F0FC
m68k_03f0fc:
        jsr -18118(%pc)
m68k_03f0fc_end:
.org 0x3F100
m68k_03f100:
        addq.w #0x1,0x813c:w
m68k_03f100_end:
.org 0x3F104
m68k_03f104:
        clr.w 0xff70f2:l
m68k_03f104_end:
.org 0x3F10A
m68k_03f10a:
        move.b 0x80db:w,0xff70f3:l
m68k_03f10a_end:
.org 0x3F112
m68k_03f112:
        tst.w 0x8124:w
m68k_03f112_end:
.org 0x3F116
m68k_03f116:
        bne.b (. + 92)
m68k_03f116_end:
.org 0x3F118
m68k_03f118:
        move.w 0x80dc:w,0xff7070:l
m68k_03f118_end:
.org 0x3F120
m68k_03f120:
        move.w 0x80e0:w,0xff706a:l
m68k_03f120_end:
.org 0x3F128
m68k_03f128:
        move.w 0x8178:w,0xff706c:l
m68k_03f128_end:
.org 0x3F130
m68k_03f130:
        move.w 0x8104:w,0xff706e:l
m68k_03f130_end:
.org 0x3F138
m68k_03f138:
        move.w 0x80de:w,0xff70c0:l
m68k_03f138_end:
.org 0x3F140
m68k_03f140:
        move.w 0x80e2:w,0xff70ba:l
m68k_03f140_end:
.org 0x3F148
m68k_03f148:
        move.w 0x8278:w,0xff70bc:l
m68k_03f148_end:
.org 0x3F150
m68k_03f150:
        move.w 0x8106:w,0xff70be:l
m68k_03f150_end:
.org 0x3F158
m68k_03f158:
        moveq #0,%d0
m68k_03f158_end:
.org 0x3F15A
m68k_03f15a:
        move.b 0x80da:w,%d0
m68k_03f15a_end:
.org 0x3F15E
m68k_03f15e:
        asl.w #0x1,%d0
m68k_03f15e_end:
.org 0x3F160
m68k_03f160:
        move.w 8(%pc, %d0.w),0xff700a:l
m68k_03f160_end:
.org 0x3F168
m68k_03f168:
        rts
m68k_03f168_end:
.org 0x3F172
m68k_03f172:
        move.w 0x80de:w,0xff7070:l
m68k_03f172_end:
.org 0x3F17A
m68k_03f17a:
        move.w 0x80e2:w,0xff706a:l
m68k_03f17a_end:
.org 0x3F182
m68k_03f182:
        move.w 0x8278:w,0xff706c:l
m68k_03f182_end:
.org 0x3F18A
m68k_03f18a:
        move.w 0x8106:w,0xff706e:l
m68k_03f18a_end:
.org 0x3F192
m68k_03f192:
        move.w 0x80dc:w,0xff70c0:l
m68k_03f192_end:
.org 0x3F19A
m68k_03f19a:
        move.w 0x80e0:w,0xff70ba:l
m68k_03f19a_end:
.org 0x3F1A2
m68k_03f1a2:
        move.w 0x8178:w,0xff70bc:l
m68k_03f1a2_end:
.org 0x3F1AA
m68k_03f1aa:
        move.w 0x8104:w,0xff70be:l
m68k_03f1aa_end:
.org 0x3F1B2
m68k_03f1b2:
        moveq #0,%d0
m68k_03f1b2_end:
.org 0x3F1B4
m68k_03f1b4:
        move.b 0x80da:w,%d0
m68k_03f1b4_end:
.org 0x3F1B8
m68k_03f1b8:
        asl.w #0x1,%d0
m68k_03f1b8_end:
.org 0x3F1BA
m68k_03f1ba:
        move.w 8(%pc, %d0.w),0xff700a:l
m68k_03f1ba_end:
.org 0x3F1C2
m68k_03f1c2:
        rts
m68k_03f1c2_end:
.org 0x3F4C2
m68k_03f4c2:
        moveq #0,%d0
m68k_03f4c2_end:
.org 0x3F4C4
m68k_03f4c4:
        moveq #0,%d1
m68k_03f4c4_end:
.org 0x3F4C6
m68k_03f4c6:
        move.w 0x80e4:w,%d0
m68k_03f4c6_end:
.org 0x3F4CA
m68k_03f4ca:
        move.w 0x80e8:w,%d1
m68k_03f4ca_end:
.org 0x3F4CE
m68k_03f4ce:
        bne.w (. + 10)
m68k_03f4ce_end:
.org 0x3F4D2
m68k_03f4d2:
        addq.w #0x1,0x80e8:w
m68k_03f4d2_end:
.org 0x3F4D6
m68k_03f4d6:
        bra.b (. + -20)
m68k_03f4d6_end:
.org 0x3F4D8
m68k_03f4d8:
        cmpi.w #0xf,%d1
m68k_03f4d8_end:
.org 0x3F4DC
m68k_03f4dc:
        bls.w (. + 10)
m68k_03f4dc_end:
.org 0x3F4E0
m68k_03f4e0:
        subq.w #0x1,0x80e8:w
m68k_03f4e0_end:
.org 0x3F4E4
m68k_03f4e4:
        bra.b (. + -34)
m68k_03f4e4_end:
.org 0x3F4E6
m68k_03f4e6:
        divu.w %d1,%d0
m68k_03f4e6_end:
.org 0x3F4E8
m68k_03f4e8:
        cmpi.w #0x3e8,%d0
m68k_03f4e8_end:
.org 0x3F4EC
m68k_03f4ec:
        bls.w (. + 10)
m68k_03f4ec_end:
.org 0x3F4F0
m68k_03f4f0:
        addq.w #0x1,0x80e8:w
m68k_03f4f0_end:
.org 0x3F4F4
m68k_03f4f4:
        bra.b (. + -50)
m68k_03f4f4_end:
.org 0x3F4F6
m68k_03f4f6:
        cmpi.w #0x64,%d0
m68k_03f4f6_end:
.org 0x3F4FA
m68k_03f4fa:
        bhi.w (. + 18)
m68k_03f4fa_end:
.org 0x3F4FE
m68k_03f4fe:
        cmpi.w #0x1,0x80e8:w
m68k_03f4fe_end:
.org 0x3F504
m68k_03f504:
        bls.b (. + 8)
m68k_03f504_end:
.org 0x3F506
m68k_03f506:
        subq.w #0x1,0x80e8:w
m68k_03f506_end:
.org 0x3F50A
m68k_03f50a:
        bra.b (. + -72)
m68k_03f50a_end:
.org 0x3F50C
m68k_03f50c:
        move.w %d0,0x80ec:w
m68k_03f50c_end:
.org 0x3F510
m68k_03f510:
        swap %d0
m68k_03f510_end:
.org 0x3F512
m68k_03f512:
        move.w %d0,0x80f0:w
m68k_03f512_end:
.org 0x3F516
m68k_03f516:
        rts
m68k_03f516_end:
.org 0x4162E
m68k_04162e:
        cmpi.b #0x0,0x1(%a6)
m68k_04162e_end:
.org 0x41634
m68k_041634:
        beq.b (. + 114)
m68k_041634_end:
.org 0x41636
m68k_041636:
        cmpi.b #0x1,0x1(%a6)
m68k_041636_end:
.org 0x4163C
m68k_04163c:
        beq.b (. + 62)
m68k_04163c_end:
.org 0x4163E
m68k_04163e:
        cmpi.b #0x2,0x1(%a6)
m68k_04163e_end:
.org 0x41644
m68k_041644:
        beq.b (. + 10)
m68k_041644_end:
.org 0x41646
m68k_041646:
        move.w 0xc(%a6),%d1
m68k_041646_end:
.org 0x4164A
m68k_04164a:
        bra.w (. + 132)
m68k_04164a_end:
.org 0x4164E
m68k_04164e:
        move.w 0xe(%a6),%d0
m68k_04164e_end:
.org 0x41652
m68k_041652:
        move.w 0xc(%a6),%d1
m68k_041652_end:
.org 0x41656
m68k_041656:
        mulu.w %d0,%d1
m68k_041656_end:
.org 0x41658
m68k_041658:
        divu.w #0x64,%d1
m68k_041658_end:
.org 0x4165C
m68k_04165c:
        movem.l %d1,-(%a7)
m68k_04165c_end:
.org 0x41660
m68k_041660:
        jsr -24384(%pc)
m68k_041660_end:
.org 0x41664
m68k_041664:
        andi.w #0x1f,%d0
m68k_041664_end:
.org 0x41668
m68k_041668:
        addi.w #0x78,%d0
m68k_041668_end:
.org 0x4166C
m68k_04166c:
        movem.l (%a7)+,%d1
m68k_04166c_end:
.org 0x41670
m68k_041670:
        mulu.w %d0,%d1
m68k_041670_end:
.org 0x41672
m68k_041672:
        divu.w #0x64,%d1
m68k_041672_end:
.org 0x41676
m68k_041676:
        bra.w (. + 88)
m68k_041676_end:
.org 0x4167A
m68k_04167a:
        move.w 0xe(%a6),%d0
m68k_04167a_end:
.org 0x4167E
m68k_04167e:
        move.w 0xc(%a6),%d1
m68k_04167e_end:
.org 0x41682
m68k_041682:
        mulu.w %d0,%d1
m68k_041682_end:
.org 0x41684
m68k_041684:
        divu.w #0x64,%d1
m68k_041684_end:
.org 0x41688
m68k_041688:
        movem.l %d1,-(%a7)
m68k_041688_end:
.org 0x4168C
m68k_04168c:
        jsr -24428(%pc)
m68k_04168c_end:
.org 0x41690
m68k_041690:
        andi.w #0x1f,%d0
m68k_041690_end:
.org 0x41694
m68k_041694:
        addi.w #0x50,%d0
m68k_041694_end:
.org 0x41698
m68k_041698:
        movem.l (%a7)+,%d1
m68k_041698_end:
.org 0x4169C
m68k_04169c:
        mulu.w %d0,%d1
m68k_04169c_end:
.org 0x4169E
m68k_04169e:
        divu.w #0x64,%d1
m68k_04169e_end:
.org 0x416A2
m68k_0416a2:
        bra.w (. + 44)
m68k_0416a2_end:
.org 0x416A6
m68k_0416a6:
        move.w 0xe(%a6),%d0
m68k_0416a6_end:
.org 0x416AA
m68k_0416aa:
        move.w 0xc(%a6),%d1
m68k_0416aa_end:
.org 0x416AE
m68k_0416ae:
        mulu.w %d0,%d1
m68k_0416ae_end:
.org 0x416B0
m68k_0416b0:
        divu.w #0x64,%d1
m68k_0416b0_end:
.org 0x416B4
m68k_0416b4:
        movem.l %d1,-(%a7)
m68k_0416b4_end:
.org 0x416B8
m68k_0416b8:
        jsr -24472(%pc)
m68k_0416b8_end:
.org 0x416BC
m68k_0416bc:
        andi.w #0x1f,%d0
m68k_0416bc_end:
.org 0x416C0
m68k_0416c0:
        addi.w #0x3c,%d0
m68k_0416c0_end:
.org 0x416C4
m68k_0416c4:
        movem.l (%a7)+,%d1
m68k_0416c4_end:
.org 0x416C8
m68k_0416c8:
        mulu.w %d0,%d1
m68k_0416c8_end:
.org 0x416CA
m68k_0416ca:
        divu.w #0x64,%d1
m68k_0416ca_end:
.org 0x41738
m68k_041738:
        move.w 0xe(%a6),%d0
m68k_041738_end:
.org 0x4173C
m68k_04173c:
        move.w 0xc(%a6),%d1
m68k_04173c_end:
.org 0x41740
m68k_041740:
        mulu.w %d0,%d1
m68k_041740_end:
.org 0x41742
m68k_041742:
        divu.w #0x64,%d1
m68k_041742_end:
.org 0x41746
m68k_041746:
        movem.l %d1,-(%a7)
m68k_041746_end:
.org 0x4174A
m68k_04174a:
        jsr -24618(%pc)
m68k_04174a_end:
.org 0x4174E
m68k_04174e:
        andi.w #0x1f,%d0
m68k_04174e_end:
.org 0x41752
m68k_041752:
        addi.w #0x50,%d0
m68k_041752_end:
.org 0x41756
m68k_041756:
        movem.l (%a7)+,%d1
m68k_041756_end:
.org 0x4175A
m68k_04175a:
        mulu.w %d0,%d1
m68k_04175a_end:
.org 0x4175C
m68k_04175c:
        divu.w #0x64,%d1
m68k_04175c_end:
.org 0x41760
m68k_041760:
        bsr.w (. + -146)
m68k_041760_end:
.org 0x41764
m68k_041764:
        bra.w (. + -552)
m68k_041764_end:
.org 0x417F6
m68k_0417f6:
        move.w #0xff,%d0
m68k_0417f6_end:
.org 0x417FA
m68k_0417fa:
        lea.l 0x816a:w,%a6
m68k_0417fa_end:
.org 0x417FE
m68k_0417fe:
        clr.w (%a6)+
m68k_0417fe_end:
.org 0x41800
m68k_041800:
        dbra %d0,(. + -2)
m68k_041800_end:
.org 0x41804
m68k_041804:
        cmpi.b #0x1,0x80da:w
m68k_041804_end:
.org 0x4180A
m68k_04180a:
        beq.w (. + 528)
m68k_04180a_end:
.org 0x4180E
m68k_04180e:
        cmpi.b #0x2,0x80da:w
m68k_04180e_end:
.org 0x41814
m68k_041814:
        beq.w (. + 518)
m68k_041814_end:
.org 0x41818
m68k_041818:
        clr.w 0x80e8:w
m68k_041818_end:
.org 0x4181C
m68k_04181c:
        clr.w 0x80f4:w
m68k_04181c_end:
.org 0x41820
m68k_041820:
        clr.w 0x80f6:w
m68k_041820_end:
.org 0x41824
m68k_041824:
        clr.w 0x80f8:w
m68k_041824_end:
.org 0x41828
m68k_041828:
        tst.w 0x80e4:w
m68k_041828_end:
.org 0x4182C
m68k_04182c:
        beq.w (. + 286)
m68k_04182c_end:
.org 0x41830
m68k_041830:
        move.w #0x1,0x80e8:w
m68k_041830_end:
.org 0x41836
m68k_041836:
        cmpi.w #0x64,0x80e4:w
m68k_041836_end:
.org 0x4183C
m68k_04183c:
        bcs.w (. + 108)
m68k_04183c_end:
.org 0x41840
m68k_041840:
        cmpi.w #0x5dc,0x80e4:w
m68k_041840_end:
.org 0x41846
m68k_041846:
        bcc.b (. + 26)
m68k_041846_end:
.org 0x41848
m68k_041848:
        jsr -24872(%pc)
m68k_041848_end:
.org 0x4184C
m68k_04184c:
        andi.w #0xf,%d0
m68k_04184c_end:
.org 0x41850
m68k_041850:
        cmpi.w #0x9,%d0
m68k_041850_end:
.org 0x41854
m68k_041854:
        bhi.b (. + -12)
m68k_041854_end:
.org 0x41856
m68k_041856:
        addq.w #0x1,%d0
m68k_041856_end:
.org 0x41858
m68k_041858:
        move.w %d0,0x80e8:w
m68k_041858_end:
.org 0x4185C
m68k_04185c:
        bra.w (. + 76)
m68k_04185c_end:
.org 0x41860
m68k_041860:
        cmpi.w #0x1388,0x80e4:w
m68k_041860_end:
.org 0x41866
m68k_041866:
        bcc.b (. + 26)
m68k_041866_end:
.org 0x41868
m68k_041868:
        jsr -24904(%pc)
m68k_041868_end:
.org 0x4186C
m68k_04186c:
        andi.w #0xf,%d0
m68k_04186c_end:
.org 0x41870
m68k_041870:
        cmpi.w #0x5,%d0
m68k_041870_end:
.org 0x41874
m68k_041874:
        bhi.b (. + -12)
m68k_041874_end:
.org 0x41876
m68k_041876:
        addq.w #0x5,%d0
m68k_041876_end:
.org 0x41878
m68k_041878:
        move.w %d0,0x80e8:w
m68k_041878_end:
.org 0x4187C
m68k_04187c:
        bra.w (. + 44)
m68k_04187c_end:
.org 0x41880
m68k_041880:
        move.w #0xf,0x80e8:w
m68k_041880_end:
.org 0x41886
m68k_041886:
        cmpi.w #0x2710,0x80e4:w
m68k_041886_end:
.org 0x4188C
m68k_04188c:
        bcc.b (. + 28)
m68k_04188c_end:
.org 0x4188E
m68k_04188e:
        jsr -24942(%pc)
m68k_04188e_end:
.org 0x41892
m68k_041892:
        andi.w #0xf,%d0
m68k_041892_end:
.org 0x41896
m68k_041896:
        cmpi.w #0x5,%d0
m68k_041896_end:
.org 0x4189A
m68k_04189a:
        bhi.b (. + -12)
m68k_04189a_end:
.org 0x4189C
m68k_04189c:
        addi.w #0xa,%d0
m68k_04189c_end:
.org 0x418A0
m68k_0418a0:
        move.w %d0,0x80e8:w
m68k_0418a0_end:
.org 0x418A4
m68k_0418a4:
        bra.w (. + 4)
m68k_0418a4_end:
.org 0x418A8
m68k_0418a8:
        bsr.w (. + -9190)
m68k_0418a8_end:
.org 0x662E4
m68k_0662e4:
        lea.l 0xc000:w,%a0
m68k_0662e4_end:
.org 0x662E8
m68k_0662e8:
        lea.l 0xbe00:w,%a1
m68k_0662e8_end:
.org 0x662EC
m68k_0662ec:
        lea.l 0xc600:w,%a2
m68k_0662ec_end:
.org 0x662F0
m68k_0662f0:
        lea.l 390(%pc),%a3
m68k_0662f0_end:
.org 0x662F4
m68k_0662f4:
        nop
m68k_0662f4_end:
.org 0x662F6
m68k_0662f6:
        lea.l 0xcc00:w,%a6
m68k_0662f6_end:
.org 0x662FA
m68k_0662fa:
        clr.w 0xef78:w
m68k_0662fa_end:
.org 0x662FE
m68k_0662fe:
        move.w 0xef78:w,%d0
m68k_0662fe_end:
.org 0x66302
m68k_066302:
        cmpi.w #0x100,%d0
m68k_066302_end:
.org 0x66306
m68k_066306:
        bcc.w (. + 94)
m68k_066306_end:
.org 0x6630A
m68k_06630a:
        cmpi.b #0xff,(%a6, %d0.w)
m68k_06630a_end:
.org 0x66310
m68k_066310:
        beq.w (. + 30)
m68k_066310_end:
.org 0x66314
m68k_066314:
        clr.w %d2
m68k_066314_end:
.org 0x66316
m68k_066316:
        move.b (%a2, %d0.w),%d2
m68k_066316_end:
.org 0x6631A
m68k_06631a:
        lsl.w #0x1,%d2
m68k_06631a_end:
.org 0x6631C
m68k_06631c:
        lsl.w #0x1,%d0
m68k_06631c_end:
.org 0x6631E
m68k_06631e:
        move.w (%a0, %d0.w),%d1
m68k_06631e_end:
.org 0x66322
m68k_066322:
        add.w (%a1, %d0.w),%d1
m68k_066322_end:
.org 0x66326
m68k_066326:
        cmp.w (%a3, %d2.w),%d1
m68k_066326_end:
.org 0x6632A
m68k_06632a:
        bcc.w (. + 10)
m68k_06632a_end:
.org 0x6632E
m68k_06632e:
        addq.w #0x1,0xef78:w
m68k_06632e_end:
.org 0x66332
m68k_066332:
        bra.b (. + -52)
m68k_066332_end:
.org 0x66334
m68k_066334:
        bsr.w (. + 60)
m68k_066334_end:
.org 0x66338
m68k_066338:
        bsr.w (. + 106)
m68k_066338_end:
.org 0x6633C
m68k_06633c:
        bsr.w (. + 152)
m68k_06633c_end:
.org 0x66340
m68k_066340:
        bsr.w (. + 206)
m68k_066340_end:
.org 0x66344
m68k_066344:
        addq.b #0x1,(%a2, %d0.w)
m68k_066344_end:
.org 0x66348
m68k_066348:
        bsr.w (. + 242)
m68k_066348_end:
.org 0x6634C
m68k_06634c:
        bcc.b (. + -78)
m68k_06634c_end:
.org 0x66364
m68k_066364:
        move.w #0x1,0xcfcc:w
m68k_066364_end:
.org 0x6636A
m68k_06636a:
        andi.w #0xfffe,%sr
m68k_06636a_end:
.org 0x6636E
m68k_06636e:
        rts
m68k_06636e_end:
.org 0x66370
m68k_066370:
        lea.l 0xb400:w,%a4
m68k_066370_end:
.org 0x66374
m68k_066374:
        move.w (%a0, %d0.w),%d1
m68k_066374_end:
.org 0x66378
m68k_066378:
        move.w %d1,%d2
m68k_066378_end:
.org 0x6637A
m68k_06637a:
        lsl.w #0x1,%d1
m68k_06637a_end:
.org 0x6637C
m68k_06637c:
        add.w %d2,%d1
m68k_06637c_end:
.org 0x6637E
m68k_06637e:
        add.w (%a1, %d0.w),%d2
m68k_06637e_end:
.org 0x66382
m68k_066382:
        andi.l #0xffff,%d1
m68k_066382_end:
.org 0x66388
m68k_066388:
        divu.w %d2,%d1
m68k_066388_end:
.org 0x6638A
m68k_06638a:
        move.w (%a4, %d0.w),%d2
m68k_06638a_end:
.org 0x6638E
m68k_06638e:
        add.w %d1,%d2
m68k_06638e_end:
.org 0x66390
m68k_066390:
        cmpi.w #0xff,%d2
m68k_066390_end:
.org 0x66394
m68k_066394:
        bls.w (. + 8)
m68k_066394_end:
.org 0x6639C
m68k_06639c:
        move.w %d2,(%a4, %d0.w)
m68k_06639c_end:
.org 0x663A0
m68k_0663a0:
        rts
m68k_0663a0_end:
.org 0x663A2
m68k_0663a2:
        lea.l 0xb600:w,%a4
m68k_0663a2_end:
.org 0x663A6
m68k_0663a6:
        move.w (%a1, %d0.w),%d1
m68k_0663a6_end:
.org 0x663AA
m68k_0663aa:
        move.w %d1,%d2
m68k_0663aa_end:
.org 0x663AC
m68k_0663ac:
        lsl.w #0x1,%d1
m68k_0663ac_end:
.org 0x663AE
m68k_0663ae:
        add.w %d2,%d1
m68k_0663ae_end:
.org 0x663B0
m68k_0663b0:
        add.w (%a0, %d0.w),%d2
m68k_0663b0_end:
.org 0x663B4
m68k_0663b4:
        andi.l #0xffff,%d1
m68k_0663b4_end:
.org 0x663BA
m68k_0663ba:
        divu.w %d2,%d1
m68k_0663ba_end:
.org 0x663BC
m68k_0663bc:
        move.w (%a4, %d0.w),%d2
m68k_0663bc_end:
.org 0x663C0
m68k_0663c0:
        add.w %d1,%d2
m68k_0663c0_end:
.org 0x663C2
m68k_0663c2:
        cmpi.w #0xff,%d2
m68k_0663c2_end:
.org 0x663C6
m68k_0663c6:
        bls.w (. + 8)
m68k_0663c6_end:
.org 0x663CE
m68k_0663ce:
        move.w %d2,(%a4, %d0.w)
m68k_0663ce_end:
.org 0x663D2
m68k_0663d2:
        rts
m68k_0663d2_end:
.org 0x663D4
m68k_0663d4:
        move.w %d0,-(%a7)
m68k_0663d4_end:
.org 0x663D6
m68k_0663d6:
        jsr 0x83d4:l
m68k_0663d6_end:
.org 0x663DC
m68k_0663dc:
        andi.l #0xffff,%d0
m68k_0663dc_end:
.org 0x663E2
m68k_0663e2:
        move.l %d0,%d1
m68k_0663e2_end:
.org 0x663E4
m68k_0663e4:
        lsl.l #0x1,%d1
m68k_0663e4_end:
.org 0x663E6
m68k_0663e6:
        add.l %d0,%d1
m68k_0663e6_end:
.org 0x663E8
m68k_0663e8:
        swap %d1
m68k_0663e8_end:
.org 0x663EA
m68k_0663ea:
        move.w (%a7)+,%d0
m68k_0663ea_end:
.org 0x663EC
m68k_0663ec:
        move.w %d1,%d2
m68k_0663ec_end:
.org 0x663EE
m68k_0663ee:
        lsl.w #0x2,%d1
m68k_0663ee_end:
.org 0x663F0
m68k_0663f0:
        add.w %d2,%d1
m68k_0663f0_end:
.org 0x663F2
m68k_0663f2:
        lea.l 0xb800:w,%a4
m68k_0663f2_end:
.org 0x663F6
m68k_0663f6:
        move.w (%a4, %d0.w),%d2
m68k_0663f6_end:
.org 0x663FA
m68k_0663fa:
        add.w %d1,%d2
m68k_0663fa_end:
.org 0x663FC
m68k_0663fc:
        cmpi.w #0x96,%d2
m68k_0663fc_end:
.org 0x66400
m68k_066400:
        bls.w (. + 8)
m68k_066400_end:
.org 0x66408
m68k_066408:
        move.w %d2,(%a4, %d0.w)
m68k_066408_end:
.org 0x6640C
m68k_06640c:
        rts
m68k_06640c_end:
.org 0x6640E
m68k_06640e:
        lsr.w #0x1,%d0
m68k_06640e_end:
.org 0x66410
m68k_066410:
        lea.l 0xc400:w,%a4
m68k_066410_end:
.org 0x66414
m68k_066414:
        cmpi.b #0x14,(%a4, %d0.w)
m68k_066414_end:
.org 0x6641A
m68k_06641a:
        bcc.w (. + 30)
m68k_06641a_end:
.org 0x6641E
m68k_06641e:
        move.w %d0,-(%a7)
m68k_06641e_end:
.org 0x66420
m68k_066420:
        jsr 0x83d4:l
m68k_066420_end:
.org 0x66426
m68k_066426:
        move.w (%a7)+,%d0
m68k_066426_end:
.org 0x66428
m68k_066428:
        move.w 0xf61c:w,%d1
m68k_066428_end:
.org 0x6642C
m68k_06642c:
        btst.l #0x4,%d1
m68k_06642c_end:
.org 0x66430
m68k_066430:
        beq.w (. + 8)
m68k_066430_end:
.org 0x66434
m68k_066434:
        addq.b #0x1,(%a4, %d0.w)
m68k_066434_end:
.org 0x66438
m68k_066438:
        rts
m68k_066438_end:
.org 0x6643A
m68k_06643a:
        lea.l 0xcc00:w,%a4
m68k_06643a_end:
.org 0x6643E
m68k_06643e:
        lea.l 0xf427:w,%a5
m68k_06643e_end:
.org 0x66442
m68k_066442:
        move.b (%a4, %d0.w),%d1
m68k_066442_end:
.org 0x66446
m68k_066446:
        bmi.w (. + 36)
m68k_066446_end:
.org 0x6644A
m68k_06644a:
        andi.w #0x3f,%d1
m68k_06644a_end:
.org 0x6644E
m68k_06644e:
        move.b (%a5, %d1.w),%d1
m68k_06644e_end:
.org 0x66452
m68k_066452:
        cmp.b 0xf67b:w,%d1
m68k_066452_end:
.org 0x66456
m68k_066456:
        beq.w (. + 28)
m68k_066456_end:
.org 0x6645A
m68k_06645a:
        cmp.b 0xf67d:w,%d1
m68k_06645a_end:
.org 0x6645E
m68k_06645e:
        beq.w (. + 20)
m68k_06645e_end:
.org 0x66462
m68k_066462:
        cmp.b 0xf67f:w,%d1
m68k_066462_end:
.org 0x66466
m68k_066466:
        beq.w (. + 12)
m68k_066466_end:
.org 0x6646A
m68k_06646a:
        andi.w #0xfffe,%sr
m68k_06646a_end:
.org 0x6646E
m68k_06646e:
        bra.w (. + 8)
m68k_06646e_end:
.org 0x66476
m68k_066476:
        rts
m68k_066476_end:
.org 0x671B6
m68k_0671b6:
        subq.w #0x1,0xefda:w
m68k_0671b6_end:
.org 0x671BA
m68k_0671ba:
        bne.w (. + 124)
m68k_0671ba_end:
.org 0x671BE
m68k_0671be:
        move.w 0xefd8:w,%d0
m68k_0671be_end:
.org 0x671C2
m68k_0671c2:
        lsl.w #0x1,%d0
m68k_0671c2_end:
.org 0x671C4
m68k_0671c4:
        move.w -22(%pc, %d0.w),0xefda:w
m68k_0671c4_end:
.org 0x671CA
m68k_0671ca:
        movea.l 0xf3be:w,%a0
m68k_0671ca_end:
.org 0x671CE
m68k_0671ce:
        addq.l #0x2,0xf3be:w
m68k_0671ce_end:
.org 0x671D2
m68k_0671d2:
        move.w (%a0),%d0
m68k_0671d2_end:
.org 0x671D4
m68k_0671d4:
        move.w %d0,0xf77c:w
m68k_0671d4_end:
.org 0x671D8
m68k_0671d8:
        beq.b (. + 50)
m68k_0671d8_end:
.org 0x671DA
m68k_0671da:
        bmi.b (. + 80)
m68k_0671da_end:
.org 0x671DC
m68k_0671dc:
        lea.l 0xd100:w,%a0
m68k_0671dc_end:
.org 0x671E0
m68k_0671e0:
        adda.w 0xf31a:w,%a0
m68k_0671e0_end:
.org 0x671E4
m68k_0671e4:
        bsr.w (. + 368)
m68k_0671e4_end:
.org 0x671E8
m68k_0671e8:
        bsr.w (. + 420)
m68k_0671e8_end:
.org 0x671EC
m68k_0671ec:
        addi.w #0x12,0xf37c:w
m68k_0671ec_end:
.org 0x671F2
m68k_0671f2:
        cmpi.w #0x120,0xf37c:w
m68k_0671f2_end:
.org 0x671F8
m68k_0671f8:
        bcs.w (. + 62)
m68k_0671f8_end:
.org 0x6722A
m68k_06722a:
        andi.w #0xff,%d0
m68k_06722a_end:
.org 0x6722E
m68k_06722e:
        move.w 8(%pc, %d0.w),%d0
m68k_06722e_end:
.org 0x67232
m68k_067232:
        jmp 26(%pc, %d0.w)
m68k_067232_end:
.org 0x67236
m68k_067236:
        rts
m68k_067236_end:
.org 0x6724E
m68k_06724e:
        move.w 0xf3c2:w,0xf612:w
m68k_06724e_end:
.org 0x67254
m68k_067254:
        move.w 0xf3c4:w,0xf362:w
m68k_067254_end:
.org 0x6725A
m68k_06725a:
        rts
m68k_06725a_end:
.org 0x6725C
m68k_06725c:
        eori.w #0x1,0xf37a:w
m68k_06725c_end:
.org 0x67262
m68k_067262:
        clr.w 0xf37c:w
m68k_067262_end:
.org 0x67266
m68k_067266:
        rts
m68k_067266_end:
.org 0x672A6
m68k_0672a6:
        move.w %d0,%d1
m68k_0672a6_end:
.org 0x672A8
m68k_0672a8:
        lsl.w #0x1,%d0
m68k_0672a8_end:
.org 0x672AA
m68k_0672aa:
        add.w %d1,%d0
m68k_0672aa_end:
.org 0x672AC
m68k_0672ac:
        lsl.w #0x1,%d0
m68k_0672ac_end:
.org 0x672AE
m68k_0672ae:
        lea.l 0x8a504:l,%a0
m68k_0672ae_end:
.org 0x672B4
m68k_0672b4:
        adda.w %d0,%a0
m68k_0672b4_end:
.org 0x672B6
m68k_0672b6:
        lea.l 0xd300:w,%a1
m68k_0672b6_end:
.org 0x672BA
m68k_0672ba:
        move.w #0x2,%d0
m68k_0672ba_end:
.org 0x672BE
m68k_0672be:
        move.w (%a0)+,%d1
m68k_0672be_end:
.org 0x672C0
m68k_0672c0:
        ori.w #0x4000,%d1
m68k_0672c0_end:
.org 0x672C4
m68k_0672c4:
        move.w %d1,(%a1)+
m68k_0672c4_end:
.org 0x672C6
m68k_0672c6:
        dbra %d0,(. + -8)
m68k_0672c6_end:
.org 0x672CA
m68k_0672ca:
        move.w #0x800c,(%a1)
m68k_0672ca_end:
.org 0x672CE
m68k_0672ce:
        cmpi.w #0x403f,-(%a1)
m68k_0672ce_end:
.org 0x672D2
m68k_0672d2:
        beq.b (. + -8)
m68k_0672d2_end:
.org 0x672D4
m68k_0672d4:
        move.l 0xf3be:w,0xf3d4:w
m68k_0672d4_end:
.org 0x672DA
m68k_0672da:
        move.l #0xffffd300,0xf3be:w
m68k_0672da_end:
.org 0x672E2
m68k_0672e2:
        bra.w (. + -300)
m68k_0672e2_end:
.org 0x672EC
m68k_0672ec:
        move.l 0xf3d4:w,0xf3be:w
m68k_0672ec_end:
.org 0x672F2
m68k_0672f2:
        bra.w (. + -316)
m68k_0672f2_end:
.org 0x672F6
m68k_0672f6:
        move.w 0xf376:w,%d0
m68k_0672f6_end:
.org 0x672FA
m68k_0672fa:
        lsl.w #0x1,%d0
m68k_0672fa_end:
.org 0x672FC
m68k_0672fc:
        lea.l 0xe640:w,%a0
m68k_0672fc_end:
.org 0x67300
m68k_067300:
        move.w (%a0, %d0.w),%d0
m68k_067300_end:
.org 0x67304
m68k_067304:
        bra.b (. + -94)
m68k_067304_end:
.org 0x67354
m68k_067354:
        move.w #0x4060,%d1
m68k_067354_end:
.org 0x67358
m68k_067358:
        tst.w 0xf37a:w
m68k_067358_end:
.org 0x6735C
m68k_06735c:
        beq.b (. + 6)
m68k_06735c_end:
.org 0x6735E
m68k_06735e:
        move.w #0x4090,%d1
m68k_06735e_end:
.org 0x67362
m68k_067362:
        move.w %d1,(%a0)+
m68k_067362_end:
.org 0x67364
m68k_067364:
        move.w 0xf37c:w,%d1
m68k_067364_end:
.org 0x67368
m68k_067368:
        andi.w #0xfff8,%d1
m68k_067368_end:
.org 0x6736C
m68k_06736c:
        move.w %d1,%d2
m68k_06736c_end:
.org 0x6736E
m68k_06736e:
        add.w %d2,%d1
m68k_06736e_end:
.org 0x67370
m68k_067370:
        tst.w 0xf37a:w
m68k_067370_end:
.org 0x67374
m68k_067374:
        beq.b (. + 4)
m68k_067374_end:
.org 0x67376
m68k_067376:
        add.w %d2,%d1
m68k_067376_end:
.org 0x67378
m68k_067378:
        lsl.w #0x2,%d1
m68k_067378_end:
.org 0x6737A
m68k_06737a:
        addi.w #0xa0a0,%d1
m68k_06737a_end:
.org 0x6737E
m68k_06737e:
        tst.w 0xf37a:w
m68k_06737e_end:
.org 0x67382
m68k_067382:
        beq.b (. + 6)
m68k_067382_end:
.org 0x67384
m68k_067384:
        addi.w #0x900,%d1
m68k_067384_end:
.org 0x67388
m68k_067388:
        move.w %d1,(%a0)+
m68k_067388_end:
.org 0x6738A
m68k_06738a:
        rts
m68k_06738a_end:
.org 0x6738C
m68k_06738c:
        move.w %d0,%d1
m68k_06738c_end:
.org 0x6738E
m68k_06738e:
        andi.w #0xff00,%d1
m68k_06738e_end:
.org 0x67392
m68k_067392:
        lsl.w #0x3,%d1
m68k_067392_end:
.org 0x67394
m68k_067394:
        andi.w #0xff,%d0
m68k_067394_end:
.org 0x67398
m68k_067398:
        lsl.w #0x5,%d0
m68k_067398_end:
.org 0x6739A
m68k_06739a:
        or.w %d1,%d0
m68k_06739a_end:
.org 0x6739C
m68k_06739c:
        lea.l 0x8159c:l,%a2
m68k_06739c_end:
.org 0x673A2
m68k_0673a2:
        lea.l (%a2, %d0.w),%a2
m68k_0673a2_end:
.org 0x673A6
m68k_0673a6:
        move.w #0x40,%d2
m68k_0673a6_end:
.org 0x673AA
m68k_0673aa:
        lea.l 0xf516:w,%a1
m68k_0673aa_end:
.org 0x673AE
m68k_0673ae:
        tst.w 0xf37a:w
m68k_0673ae_end:
.org 0x673B2
m68k_0673b2:
        beq.b (. + 28)
m68k_0673b2_end:
.org 0x673B4
m68k_0673b4:
        move.w #0x60,%d2
m68k_0673b4_end:
.org 0x673B8
m68k_0673b8:
        move.w #0x3,%d1
m68k_0673b8_end:
.org 0x673BC
m68k_0673bc:
        bsr.w (. + 210)
m68k_0673bc_end:
.org 0x673C0
m68k_0673c0:
        move.l %d5,0xc0(%a0)
m68k_0673c0_end:
.org 0x673C4
m68k_0673c4:
        move.l %d5,0x60(%a0)
m68k_0673c4_end:
.org 0x673C8
m68k_0673c8:
        move.l %d5,(%a0)+
m68k_0673c8_end:
.org 0x673CA
m68k_0673ca:
        dbra %d1,(. + -14)
m68k_0673ca_end:
.org 0x673CE
m68k_0673ce:
        move.w %d2,%d3
m68k_0673ce_end:
.org 0x673D0
m68k_0673d0:
        lsl.w #0x1,%d3
m68k_0673d0_end:
.org 0x673D2
m68k_0673d2:
        add.w %d3,0xf31a:w
m68k_0673d2_end:
.org 0x673D6
m68k_0673d6:
        add.w %d2,0xf31a:w
m68k_0673d6_end:
.org 0x673DA
m68k_0673da:
        addi.w #0x4,0xf31a:w
m68k_0673da_end:
.org 0x673E0
m68k_0673e0:
        swap %d2
m68k_0673e0_end:
.org 0x673E2
m68k_0673e2:
        swap %d3
m68k_0673e2_end:
.org 0x673E4
m68k_0673e4:
        move.w #0xf,%d2
m68k_0673e4_end:
.org 0x673E8
m68k_0673e8:
        move.w 0xf37c:w,%d3
m68k_0673e8_end:
.org 0x673EC
m68k_0673ec:
        andi.w #0x7,%d3
m68k_0673ec_end:
.org 0x673F0
m68k_0673f0:
        bsr.w (. + 122)
m68k_0673f0_end:
.org 0x673F4
m68k_0673f4:
        jsr 0xaf04:l
m68k_0673f4_end:
.org 0x673FA
m68k_0673fa:
        move.l %d7,-(%a7)
m68k_0673fa_end:
.org 0x673FC
m68k_0673fc:
        jsr 0xaf04:l
m68k_0673fc_end:
.org 0x67402
m68k_067402:
        move.l (%a7)+,%d4
m68k_067402_end:
.org 0x67404
m68k_067404:
        bsr.w (. + 138)
m68k_067404_end:
.org 0x67408
m68k_067408:
        move.w %d3,%d6
m68k_067408_end:
.org 0x6740A
m68k_06740a:
        beq.b (. + 34)
m68k_06740a_end:
.org 0x6740C
m68k_06740c:
        lsl.w #0x2,%d6
m68k_06740c_end:
.org 0x6740E
m68k_06740e:
        subq.w #0x1,%d6
m68k_06740e_end:
.org 0x67410
m68k_067410:
        clr.w %d0
m68k_067410_end:
.org 0x67412
m68k_067412:
        andi.w #0xffef,%sr
m68k_067412_end:
.org 0x67416
m68k_067416:
        roxr.l #0x1,%d4
m68k_067416_end:
.org 0x67418
m68k_067418:
        roxr.l #0x1,%d7
m68k_067418_end:
.org 0x6741A
m68k_06741a:
        roxr.l #0x1,%d5
m68k_06741a_end:
.org 0x6741C
m68k_06741c:
        ori.w #0x10,%sr
m68k_06741c_end:
.org 0x67420
m68k_067420:
        roxr.l #0x1,%d0
m68k_067420_end:
.org 0x67422
m68k_067422:
        dbra %d6,(. + -16)
m68k_067422_end:
.org 0x67426
m68k_067426:
        move.l (%a1),%d1
m68k_067426_end:
.org 0x67428
m68k_067428:
        and.l %d0,%d1
m68k_067428_end:
.org 0x6742A
m68k_06742a:
        or.l %d1,%d4
m68k_06742a_end:
.org 0x6742C
m68k_06742c:
        swap %d2
m68k_06742c_end:
.org 0x6742E
m68k_06742e:
        swap %d3
m68k_06742e_end:
.org 0x67430
m68k_067430:
        move.l %d5,(%a0, %d3.w)
m68k_067430_end:
.org 0x67434
m68k_067434:
        move.l %d7,(%a0, %d2.w)
m68k_067434_end:
.org 0x67438
m68k_067438:
        move.l %d4,(%a0)+
m68k_067438_end:
.org 0x6743A
m68k_06743a:
        move.l %d5,(%a1)+
m68k_06743a_end:
.org 0x6743C
m68k_06743c:
        swap %d2
m68k_06743c_end:
.org 0x6743E
m68k_06743e:
        swap %d3
m68k_06743e_end:
.org 0x67440
m68k_067440:
        dbra %d2,(. + -80)
m68k_067440_end:
.org 0x67444
m68k_067444:
        swap %d2
m68k_067444_end:
.org 0x67446
m68k_067446:
        swap %d3
m68k_067446_end:
.org 0x67448
m68k_067448:
        tst.w 0xf37a:w
m68k_067448_end:
.org 0x6744C
m68k_06744c:
        beq.b (. + 24)
m68k_06744c_end:
.org 0x6744E
m68k_06744e:
        move.w #0x3,%d1
m68k_06744e_end:
.org 0x67452
m68k_067452:
        bsr.w (. + 60)
m68k_067452_end:
.org 0x67456
m68k_067456:
        move.l %d5,(%a0, %d3.w)
m68k_067456_end:
.org 0x6745A
m68k_06745a:
        move.l %d5,(%a0, %d2.w)
m68k_06745a_end:
.org 0x6745E
m68k_06745e:
        move.l %d5,(%a0)+
m68k_06745e_end:
.org 0x67460
m68k_067460:
        dbra %d1,(. + -14)
m68k_067460_end:
.org 0x67464
m68k_067464:
        clr.w (%a0, %d3.w)
m68k_067464_end:
.org 0x67468
m68k_067468:
        rts
m68k_067468_end:
.org 0x6746A
m68k_06746a:
        move.w 0xf6c4:w,%d0
m68k_06746a_end:
.org 0x6746E
m68k_06746e:
        lsl.w #0x2,%d0
m68k_06746e_end:
.org 0x67470
m68k_067470:
        lea.l 12(%pc),%a3
m68k_067470_end:
.org 0x67474
m68k_067474:
        nop
m68k_067474_end:
.org 0x67476
m68k_067476:
        movem.w (%a3, %d0.w),%d0-%d1
m68k_067476_end:
.org 0x6747C
m68k_06747c:
        rts
m68k_06747c_end:
.org 0x6748E
m68k_06748e:
        move.w 0xf6c4:w,%d5
m68k_06748e_end:
.org 0x67492
m68k_067492:
        lsl.w #0x2,%d5
m68k_067492_end:
.org 0x67494
m68k_067494:
        move.l 4(%pc, %d5.w),%d5
m68k_067494_end:
.org 0x67498
m68k_067498:
        rts
m68k_067498_end:
.org 0x674CA
m68k_0674ca:
        lea.l 0xd100:w,%a0
m68k_0674ca_end:
.org 0x674CE
m68k_0674ce:
        adda.w 0xf31a:w,%a0
m68k_0674ce_end:
.org 0x674D2
m68k_0674d2:
        bsr.w (. + 56)
m68k_0674d2_end:
.org 0x674D6
m68k_0674d6:
        move.w 0xf36a:w,%d0
m68k_0674d6_end:
.org 0x674DA
m68k_0674da:
        lsl.w #0x1,%d0
m68k_0674da_end:
.org 0x674DC
m68k_0674dc:
        move.w 36(%pc, %d0.w),%d0
m68k_0674dc_end:
.org 0x674E0
m68k_0674e0:
        jsr 60(%pc, %d0.w)
m68k_0674e0_end:
.org 0x674E4
m68k_0674e4:
        addq.w #0x1,0xf36a:w
m68k_0674e4_end:
.org 0x674E8
m68k_0674e8:
        move.w 0xf36a:w,%d0
m68k_0674e8_end:
.org 0x674EC
m68k_0674ec:
        cmpi.w #0x4,%d0
m68k_0674ec_end:
.org 0x674F0
m68k_0674f0:
        bcs.b (. + 16)
m68k_0674f0_end:
.org 0x674F2
m68k_0674f2:
        addq.w #0x1,0xf362:w
m68k_0674f2_end:
.org 0x674F6
m68k_0674f6:
        clr.w 0xf36a:w
m68k_0674f6_end:
.org 0x674FA
m68k_0674fa:
        bset.b #0x6,0xf3a4:w
m68k_0674fa_end:
.org 0x67500
m68k_067500:
        rts
m68k_067500_end:
.org 0x6750A
m68k_06750a:
        move.w 0xf6c4:w,%d0
m68k_06750a_end:
.org 0x6750E
m68k_06750e:
        lsl.w #0x1,%d0
m68k_06750e_end:
.org 0x67510
m68k_067510:
        move.w 4(%pc, %d0.w),%d2
m68k_067510_end:
.org 0x67514
m68k_067514:
        rts
m68k_067514_end:
.org 0x6751E
m68k_06751e:
        move.w #0x26,(%a0)+
m68k_06751e_end:
.org 0x67522
m68k_067522:
        move.w #0xca02,(%a0)+
m68k_067522_end:
.org 0x67526
m68k_067526:
        move.w #0x380,%d3
m68k_067526_end:
.org 0x6752A
m68k_06752a:
        or.w %d2,%d3
m68k_06752a_end:
.org 0x6752C
m68k_06752c:
        move.w %d3,(%a0)+
m68k_06752c_end:
.org 0x6752E
m68k_06752e:
        move.w #0x23,%d0
m68k_06752e_end:
.org 0x67532
m68k_067532:
        move.w #0x381,%d3
m68k_067532_end:
.org 0x67536
m68k_067536:
        or.w %d2,%d3
m68k_067536_end:
.org 0x67538
m68k_067538:
        move.w %d3,(%a0)+
m68k_067538_end:
.org 0x6753A
m68k_06753a:
        dbra %d0,(. + -2)
m68k_06753a_end:
.org 0x6753E
m68k_06753e:
        move.w #0xb80,%d3
m68k_06753e_end:
.org 0x67542
m68k_067542:
        or.w %d2,%d3
m68k_067542_end:
.org 0x67544
m68k_067544:
        move.w %d3,(%a0)+
m68k_067544_end:
.org 0x67546
m68k_067546:
        clr.w (%a0)
m68k_067546_end:
.org 0x67548
m68k_067548:
        addi.w #0x50,0xf31a:w
m68k_067548_end:
.org 0x6754E
m68k_06754e:
        btst.b #0x2,0xf3a4:w
m68k_06754e_end:
.org 0x67554
m68k_067554:
        beq.b (. + 90)
m68k_067554_end:
.org 0x675AE
m68k_0675ae:
        rts
m68k_0675ae_end:
.org 0x675B0
m68k_0675b0:
        move.w #0x26,0x50(%a0)
m68k_0675b0_end:
.org 0x675B6
m68k_0675b6:
        move.w #0x26,(%a0)+
m68k_0675b6_end:
.org 0x675BA
m68k_0675ba:
        move.w #0xcb02,0x50(%a0)
m68k_0675ba_end:
.org 0x675C0
m68k_0675c0:
        move.w #0xca82,(%a0)+
m68k_0675c0_end:
.org 0x675C4
m68k_0675c4:
        move.w #0x382,%d3
m68k_0675c4_end:
.org 0x675C8
m68k_0675c8:
        or.w %d2,%d3
m68k_0675c8_end:
.org 0x675CA
m68k_0675ca:
        move.w %d3,0x50(%a0)
m68k_0675ca_end:
.org 0x675CE
m68k_0675ce:
        move.w #0x382,%d3
m68k_0675ce_end:
.org 0x675D2
m68k_0675d2:
        or.w %d2,%d3
m68k_0675d2_end:
.org 0x675D4
m68k_0675d4:
        move.w %d3,(%a0)+
m68k_0675d4_end:
.org 0x675D6
m68k_0675d6:
        move.w #0x505,%d1
m68k_0675d6_end:
.org 0x675DA
m68k_0675da:
        or.w %d2,%d1
m68k_0675da_end:
.org 0x675DC
m68k_0675dc:
        move.w #0x23,%d0
m68k_0675dc_end:
.org 0x675E0
m68k_0675e0:
        move.w %d1,(%a0)
m68k_0675e0_end:
.org 0x675E2
m68k_0675e2:
        addq.w #0x1,%d1
m68k_0675e2_end:
.org 0x675E4
m68k_0675e4:
        move.w %d1,0x50(%a0)
m68k_0675e4_end:
.org 0x675E8
m68k_0675e8:
        addq.w #0x1,%d1
m68k_0675e8_end:
.org 0x675EA
m68k_0675ea:
        addq.w #0x2,%a0
m68k_0675ea_end:
.org 0x675EC
m68k_0675ec:
        dbra %d0,(. + -12)
m68k_0675ec_end:
.org 0x675F0
m68k_0675f0:
        move.w #0xb82,%d3
m68k_0675f0_end:
.org 0x675F4
m68k_0675f4:
        or.w %d2,%d3
m68k_0675f4_end:
.org 0x675F6
m68k_0675f6:
        move.w %d3,0x50(%a0)
m68k_0675f6_end:
.org 0x675FA
m68k_0675fa:
        move.w #0xb82,%d3
m68k_0675fa_end:
.org 0x675FE
m68k_0675fe:
        or.w %d2,%d3
m68k_0675fe_end:
.org 0x67600
m68k_067600:
        move.w %d3,(%a0)+
m68k_067600_end:
.org 0x67602
m68k_067602:
        clr.w 0x50(%a0)
m68k_067602_end:
.org 0x67606
m68k_067606:
        addi.w #0xa0,0xf31a:w
m68k_067606_end:
.org 0x6760C
m68k_06760c:
        rts
m68k_06760c_end:
.org 0x6760E
m68k_06760e:
        move.w #0x26,0xa0(%a0)
m68k_06760e_end:
.org 0x67614
m68k_067614:
        move.w #0x26,0x50(%a0)
m68k_067614_end:
.org 0x6761A
m68k_06761a:
        move.w #0x26,(%a0)+
m68k_06761a_end:
.org 0x6761E
m68k_06761e:
        move.w #0xcc82,0xa0(%a0)
m68k_06761e_end:
.org 0x67624
m68k_067624:
        move.w #0xcc02,0x50(%a0)
m68k_067624_end:
.org 0x6762A
m68k_06762a:
        move.w #0xcb82,(%a0)+
m68k_06762a_end:
.org 0x6762E
m68k_06762e:
        move.w #0x382,%d3
m68k_06762e_end:
.org 0x67632
m68k_067632:
        or.w %d2,%d3
m68k_067632_end:
.org 0x67634
m68k_067634:
        move.w %d3,0xa0(%a0)
m68k_067634_end:
.org 0x67638
m68k_067638:
        move.w #0x382,%d3
m68k_067638_end:
.org 0x6763C
m68k_06763c:
        or.w %d2,%d3
m68k_06763c_end:
.org 0x6763E
m68k_06763e:
        move.w %d3,0x50(%a0)
m68k_06763e_end:
.org 0x67642
m68k_067642:
        move.w #0x382,%d3
m68k_067642_end:
.org 0x67646
m68k_067646:
        or.w %d2,%d3
m68k_067646_end:
.org 0x67648
m68k_067648:
        move.w %d3,(%a0)+
m68k_067648_end:
.org 0x6764A
m68k_06764a:
        move.w #0x54d,%d1
m68k_06764a_end:
.org 0x6764E
m68k_06764e:
        or.w %d2,%d1
m68k_06764e_end:
.org 0x67650
m68k_067650:
        move.w #0x23,%d0
m68k_067650_end:
.org 0x67654
m68k_067654:
        move.w %d1,(%a0)
m68k_067654_end:
.org 0x67656
m68k_067656:
        addq.w #0x1,%d1
m68k_067656_end:
.org 0x67658
m68k_067658:
        move.w %d1,0x50(%a0)
m68k_067658_end:
.org 0x6765C
m68k_06765c:
        addq.w #0x1,%d1
m68k_06765c_end:
.org 0x6765E
m68k_06765e:
        move.w %d1,0xa0(%a0)
m68k_06765e_end:
.org 0x67662
m68k_067662:
        addq.w #0x1,%d1
m68k_067662_end:
.org 0x67664
m68k_067664:
        addq.w #0x2,%a0
m68k_067664_end:
.org 0x67666
m68k_067666:
        dbra %d0,(. + -18)
m68k_067666_end:
.org 0x6766A
m68k_06766a:
        move.w #0xb82,%d3
m68k_06766a_end:
.org 0x6766E
m68k_06766e:
        or.w %d2,%d3
m68k_06766e_end:
.org 0x67670
m68k_067670:
        move.w %d3,0xa0(%a0)
m68k_067670_end:
.org 0x67674
m68k_067674:
        move.w #0xb82,%d3
m68k_067674_end:
.org 0x67678
m68k_067678:
        or.w %d2,%d3
m68k_067678_end:
.org 0x6767A
m68k_06767a:
        move.w %d3,0x50(%a0)
m68k_06767a_end:
.org 0x6767E
m68k_06767e:
        move.w #0xb82,%d3
m68k_06767e_end:
.org 0x67682
m68k_067682:
        or.w %d2,%d3
m68k_067682_end:
.org 0x67684
m68k_067684:
        move.w %d3,(%a0)+
m68k_067684_end:
.org 0x67686
m68k_067686:
        clr.w 0xa0(%a0)
m68k_067686_end:
.org 0x6768A
m68k_06768a:
        addi.w #0xf0,0xf31a:w
m68k_06768a_end:
.org 0x67690
m68k_067690:
        rts
m68k_067690_end:
.org 0x67692
m68k_067692:
        move.w #0x26,(%a0)+
m68k_067692_end:
.org 0x67696
m68k_067696:
        move.w #0xcd02,(%a0)+
m68k_067696_end:
.org 0x6769A
m68k_06769a:
        move.w #0x1380,%d3
m68k_06769a_end:
.org 0x6769E
m68k_06769e:
        or.w %d2,%d3
m68k_06769e_end:
.org 0x676A0
m68k_0676a0:
        move.w %d3,(%a0)+
m68k_0676a0_end:
.org 0x676A2
m68k_0676a2:
        move.w #0x23,%d0
m68k_0676a2_end:
.org 0x676A6
m68k_0676a6:
        move.w #0x1381,%d3
m68k_0676a6_end:
.org 0x676AA
m68k_0676aa:
        or.w %d2,%d3
m68k_0676aa_end:
.org 0x676AC
m68k_0676ac:
        move.w %d3,(%a0)+
m68k_0676ac_end:
.org 0x676AE
m68k_0676ae:
        dbra %d0,(. + -2)
m68k_0676ae_end:
.org 0x676B2
m68k_0676b2:
        move.w #0x1b80,%d3
m68k_0676b2_end:
.org 0x676B6
m68k_0676b6:
        or.w %d2,%d3
m68k_0676b6_end:
.org 0x676B8
m68k_0676b8:
        move.w %d3,(%a0)+
m68k_0676b8_end:
.org 0x676BA
m68k_0676ba:
        clr.w (%a0)
m68k_0676ba_end:
.org 0x676BC
m68k_0676bc:
        addi.w #0x50,0xf31a:w
m68k_0676bc_end:
.org 0x676C2
m68k_0676c2:
        rts
m68k_0676c2_end:
.org 0x676C4
m68k_0676c4:
        move.w 0xf380:w,%d0
m68k_0676c4_end:
.org 0x676C8
m68k_0676c8:
        cmpi.w #0x60,%d0
m68k_0676c8_end:
.org 0x676CC
m68k_0676cc:
        bcc.b (. + 18)
m68k_0676cc_end:
.org 0x676CE
m68k_0676ce:
        lsl.w #0x1,%d0
m68k_0676ce_end:
.org 0x676D0
m68k_0676d0:
        move.w 4(%pc, %d0.w),%d0
m68k_0676d0_end:
.org 0x676D4
m68k_0676d4:
        bra.b (. + 30)
m68k_0676d4_end:
.org 0x676DE
m68k_0676de:
        subi.w #0x60,%d0
m68k_0676de_end:
.org 0x676E2
m68k_0676e2:
        lsl.w #0x1,%d0
m68k_0676e2_end:
.org 0x676E4
m68k_0676e4:
        move.w 102(%pc, %d0.w),%d0
m68k_0676e4_end:
.org 0x676E8
m68k_0676e8:
        lea.l 200(%pc),%a0
m68k_0676e8_end:
.org 0x676EC
m68k_0676ec:
        nop
m68k_0676ec_end:
.org 0x676EE
m68k_0676ee:
        jsr (%a0, %d0.w)
m68k_0676ee_end:
.org 0x676F2
m68k_0676f2:
        tst.w %d0
m68k_0676f2_end:
.org 0x676F4
m68k_0676f4:
        bmi.b (. + 50)
m68k_0676f4_end:
.org 0x676F6
m68k_0676f6:
        clr.w 0xf652:w
m68k_0676f6_end:
.org 0x676FA
m68k_0676fa:
        bsr.w (. + 728)
m68k_0676fa_end:
.org 0x676FE
m68k_0676fe:
        move.l %a0,0xf3be:w
m68k_0676fe_end:
.org 0x67702
m68k_067702:
        move.w 0xf612:w,0xf3c2:w
m68k_067702_end:
.org 0x67708
m68k_067708:
        move.w 0xf362:w,0xf3c4:w
m68k_067708_end:
.org 0x6770E
m68k_06770e:
        clr.w 0xf36a:w
m68k_06770e_end:
.org 0x67712
m68k_067712:
        clr.w 0xf3c6:w
m68k_067712_end:
.org 0x67716
m68k_067716:
        move.w #0x28,0xf600:w
m68k_067716_end:
.org 0x6771C
m68k_06771c:
        bsr.w (. + 12)
m68k_06771c_end:
.org 0x67720
m68k_067720:
        move.w #0x1,0xefda:w
m68k_067720_end:
.org 0x67726
m68k_067726:
        rts
m68k_067726_end:
.org 0x67728
m68k_067728:
        move.w 0xf6c4:w,%d0
m68k_067728_end:
.org 0x6772C
m68k_06772c:
        lsl.w #0x2,%d0
m68k_06772c_end:
.org 0x6772E
m68k_06772e:
        move.w 12(%pc, %d0.w),0xf612:w
m68k_06772e_end:
.org 0x67734
m68k_067734:
        move.w 8(%pc, %d0.w),0xf362:w
m68k_067734_end:
.org 0x6773A
m68k_06773a:
        rts
m68k_06773a_end:
.org 0x677F0
m68k_0677f0:
        move.w 0xf38c:w,%d1
m68k_0677f0_end:
.org 0x677F4
m68k_0677f4:
        move.w (%a0)+,%d2
m68k_0677f4_end:
.org 0x677F6
m68k_0677f6:
        bmi.b (. + 10)
m68k_0677f6_end:
.org 0x677F8
m68k_0677f8:
        cmp.w %d2,%d1
m68k_0677f8_end:
.org 0x677FA
m68k_0677fa:
        beq.b (. + 6)
m68k_0677fa_end:
.org 0x677FC
m68k_0677fc:
        addq.w #0x2,%a0
m68k_0677fc_end:
.org 0x677FE
m68k_0677fe:
        bra.b (. + -10)
m68k_0677fe_end:
.org 0x67800
m68k_067800:
        move.w (%a0),%d0
m68k_067800_end:
.org 0x67802
m68k_067802:
        rts
m68k_067802_end:
.org 0x678DC
m68k_0678dc:
        lea.l 14(%pc),%a0
m68k_0678dc_end:
.org 0x678E0
m68k_0678e0:
        bsr.w (. + -240)
m68k_0678e0_end:
.org 0x678E4
m68k_0678e4:
        move.l 0xf39e:w,0xf3c8:w
m68k_0678e4_end:
.org 0x678EA
m68k_0678ea:
        rts
m68k_0678ea_end:
.org 0x679D2
m68k_0679d2:
        movea.l 0x92c4a:l,%a1
m68k_0679d2_end:
.org 0x679D8
m68k_0679d8:
        move.w %d0,%d1
m68k_0679d8_end:
.org 0x679DA
m68k_0679da:
        lsr.w #0x8,%d1
m68k_0679da_end:
.org 0x679DC
m68k_0679dc:
        lsl.w #0x1,%d1
m68k_0679dc_end:
.org 0x679DE
m68k_0679de:
        lea.l 0x92c4e:l,%a0
m68k_0679de_end:
.org 0x679E4
m68k_0679e4:
        move.w (%a0, %d1.w),%d1
m68k_0679e4_end:
.org 0x679E8
m68k_0679e8:
        adda.w %d1,%a1
m68k_0679e8_end:
.org 0x679EA
m68k_0679ea:
        movea.l (%a1),%a0
m68k_0679ea_end:
.org 0x679EC
m68k_0679ec:
        move.w %d0,%d1
m68k_0679ec_end:
.org 0x679EE
m68k_0679ee:
        andi.w #0xff,%d1
m68k_0679ee_end:
.org 0x679F2
m68k_0679f2:
        lsl.w #0x1,%d1
m68k_0679f2_end:
.org 0x679F4
m68k_0679f4:
        move.w 0x4(%a1, %d1.w),%d1
m68k_0679f4_end:
.org 0x679F8
m68k_0679f8:
        adda.w %d1,%a0
m68k_0679f8_end:
.org 0x679FA
m68k_0679fa:
        rts
m68k_0679fa_end:
.org 0x679FC
m68k_0679fc:
        cmpi.w #0x200,0xf612:w
m68k_0679fc_end:
.org 0x67A02
m68k_067a02:
        bne.w (. + 14)
m68k_067a02_end:
.org 0x67A10
m68k_067a10:
        tst.w 0xefc8:w
m68k_067a10_end:
.org 0x67A14
m68k_067a14:
        bne.w (. + 34)
m68k_067a14_end:
.org 0x67A18
m68k_067a18:
        move.w #0x2700,%sr
m68k_067a18_end:
.org 0x67A1C
m68k_067a1c:
        lea.l 626(%pc),%a0
m68k_067a1c_end:
.org 0x67A20
m68k_067a20:
        nop
m68k_067a20_end:
.org 0x67A22
m68k_067a22:
        move.w #0x2000,%d0
m68k_067a22_end:
.org 0x67A26
m68k_067a26:
        jsr 0x3ab52:l
m68k_067a26_end:
.org 0x67A2C
m68k_067a2c:
        move.w #0x2500,%sr
m68k_067a2c_end:
.org 0x67A30
m68k_067a30:
        move.w #0x1,0xefc8:w
m68k_067a30_end:
.org 0x67A36
m68k_067a36:
        cmpi.w #0x20,0xf352:w
m68k_067a36_end:
.org 0x67A3C
m68k_067a3c:
        bne.b (. + 52)
m68k_067a3c_end:
.org 0x67A3E
m68k_067a3e:
        move.w #0x0,0xfb50:w
m68k_067a3e_end:
.org 0x67A44
m68k_067a44:
        move.w #0xe40,0xfb52:w
m68k_067a44_end:
.org 0x67A4A
m68k_067a4a:
        move.w #0xaee,0xfb54:w
m68k_067a4a_end:
.org 0x67A50
m68k_067a50:
        move.w #0xa0e,0xfb56:w
m68k_067a50_end:
.org 0x67A56
m68k_067a56:
        move.w #0x2e0,0xfb58:w
m68k_067a56_end:
.org 0x67A5C
m68k_067a5c:
        move.w #0xce,0xfb5a:w
m68k_067a5c_end:
.org 0x67A62
m68k_067a62:
        move.w #0xea0,0xfb5c:w
m68k_067a62_end:
.org 0x67A68
m68k_067a68:
        move.w #0x0,0xfb5e:w
m68k_067a68_end:
.org 0x67A6E
m68k_067a6e:
        bra.b (. + 50)
m68k_067a6e_end:
.org 0x67AA0
m68k_067aa0:
        moveq #0,%d0
m68k_067aa0_end:
.org 0x67AA2
m68k_067aa2:
        movem.l %d0,-(%a7)
m68k_067aa2_end:
.org 0x67AA6
m68k_067aa6:
        moveq #0,%d1
m68k_067aa6_end:
.org 0x67AA8
m68k_067aa8:
        lea.l 0xf428:w,%a0
m68k_067aa8_end:
.org 0x67AAC
m68k_067aac:
        move.b (%a0, %d0.w),%d1
m68k_067aac_end:
.org 0x67AB0
m68k_067ab0:
        cmpi.b #0xff,%d1
m68k_067ab0_end:
.org 0x67AB4
m68k_067ab4:
        beq.b (. + 78)
m68k_067ab4_end:
.org 0x67AB6
m68k_067ab6:
        asl.w #0x1,%d1
m68k_067ab6_end:
.org 0x67AB8
m68k_067ab8:
        movem.l %d0,-(%a7)
m68k_067ab8_end:
.org 0x67ABC
m68k_067abc:
        move.w 0xf320:w,%d0
m68k_067abc_end:
.org 0x67AC0
m68k_067ac0:
        lsr.w #0x3,%d0
m68k_067ac0_end:
.org 0x67AC2
m68k_067ac2:
        andi.w #0x1,%d0
m68k_067ac2_end:
.org 0x67AC6
m68k_067ac6:
        add.w %d0,%d1
m68k_067ac6_end:
.org 0x67AC8
m68k_067ac8:
        asl.w #0x2,%d1
m68k_067ac8_end:
.org 0x67ACA
m68k_067aca:
        lea.l 68(%pc),%a1
m68k_067aca_end:
.org 0x67ACE
m68k_067ace:
        nop
m68k_067ace_end:
.org 0x67AD0
m68k_067ad0:
        movea.l (%a1, %d1.w),%a0
m68k_067ad0_end:
.org 0x67AD4
m68k_067ad4:
        movem.l (%a7)+,%d0
m68k_067ad4_end:
.org 0x67AD8
m68k_067ad8:
        move.w %d0,%d2
m68k_067ad8_end:
.org 0x67ADA
m68k_067ada:
        asl.w #0x2,%d2
m68k_067ada_end:
.org 0x67ADC
m68k_067adc:
        lea.l 0xd4aca:l,%a1
m68k_067adc_end:
.org 0x67AE2
m68k_067ae2:
        move.w 0x2(%a1, %d2.w),%d0
m68k_067ae2_end:
.org 0x67AE6
m68k_067ae6:
        subi.w #0x10,%d0
m68k_067ae6_end:
.org 0x67AEA
m68k_067aea:
        move.w (%a1, %d2.w),%d1
m68k_067aea_end:
.org 0x67AEE
m68k_067aee:
        clr.w %d2
m68k_067aee_end:
.org 0x67AF0
m68k_067af0:
        move.w 0xf314:w,0xf60a:w
m68k_067af0_end:
.org 0x67AF6
m68k_067af6:
        move.w 0xf318:w,0xf60e:w
m68k_067af6_end:
.org 0x67AFC
m68k_067afc:
        jsr 0xac10:l
m68k_067afc_end:
.org 0x67B02
m68k_067b02:
        movem.l (%a7)+,%d0
m68k_067b02_end:
.org 0x67B06
m68k_067b06:
        addq.w #0x1,%d0
m68k_067b06_end:
.org 0x67B08
m68k_067b08:
        cmpi.w #0x28,%d0
m68k_067b08_end:
.org 0x67B0C
m68k_067b0c:
        bcs.b (. + -106)
m68k_067b0c_end:
.org 0x67B0E
m68k_067b0e:
        rts
m68k_067b0e_end:
