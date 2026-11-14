| 嵌套分派表覆盖的例程，入口地址见对应布局。
.cpu 68000
.section .text
_start:
.org 0x2268
m68k_002268:
        cmpi.w #0x10,0xf352:w
m68k_002268_end:
.org 0x226E
m68k_00226e:
        bcc.w (. + 42)
m68k_00226e_end:
.org 0x2272
m68k_002272:
        move.w 0xf352:w,%d0
m68k_002272_end:
.org 0x2276
m68k_002276:
        move.w #0x40,%d1
m68k_002276_end:
.org 0x227A
m68k_00227a:
        lea.l 0xfb80:w,%a0
m68k_00227a_end:
.org 0x227E
m68k_00227e:
        jsr 0xdea6:l
m68k_00227e_end:
.org 0x2284
m68k_002284:
        addq.w #0x1,0xf352:w
m68k_002284_end:
.org 0x2288
m68k_002288:
        tst.w 0xf77a:w
m68k_002288_end:
.org 0x228C
m68k_00228c:
        beq.w (. + 78)
m68k_00228c_end:
.org 0x2290
m68k_002290:
        bsr.w (. + 358)
m68k_002290_end:
.org 0x2294
m68k_002294:
        bra.w (. + 70)
m68k_002294_end:
.org 0x2298
m68k_002298:
        bne.w (. + 14)
m68k_002298_end:
.org 0x229C
m68k_00229c:
        move.w #0x24,0xf600:w
m68k_00229c_end:
.org 0x22A2
m68k_0022a2:
        bra.w (. + 56)
m68k_0022a2_end:
.org 0x22A6
m68k_0022a6:
        cmpi.w #0x21,0xf352:w
m68k_0022a6_end:
.org 0x22AC
m68k_0022ac:
        bcc.w (. + 38)
m68k_0022ac_end:
.org 0x22B0
m68k_0022b0:
        move.w #0x20,%d0
m68k_0022b0_end:
.org 0x22B4
m68k_0022b4:
        sub.w 0xf352:w,%d0
m68k_0022b4_end:
.org 0x22B8
m68k_0022b8:
        move.w #0x40,%d1
m68k_0022b8_end:
.org 0x22BC
m68k_0022bc:
        lea.l 0xfb80:w,%a0
m68k_0022bc_end:
.org 0x22C0
m68k_0022c0:
        jsr 0xdea6:l
m68k_0022c0_end:
.org 0x22C6
m68k_0022c6:
        addq.w #0x1,0xf352:w
m68k_0022c6_end:
.org 0x22CA
m68k_0022ca:
        bsr.w (. + 300)
m68k_0022ca_end:
.org 0x22CE
m68k_0022ce:
        bra.w (. + 12)
m68k_0022ce_end:
.org 0x22D2
m68k_0022d2:
        addq.w #0x1,0xf362:w
m68k_0022d2_end:
.org 0x22D6
m68k_0022d6:
        bsr.w (. + 288)
m68k_0022d6_end:
.org 0x22DA
m68k_0022da:
        rts
m68k_0022da_end:
.org 0x22DC
m68k_0022dc:
        clr.w 0xefde:w
m68k_0022dc_end:
.org 0x22E0
m68k_0022e0:
        tst.w 0xf36c:w
m68k_0022e0_end:
.org 0x22E4
m68k_0022e4:
        bne.w (. + 26)
m68k_0022e4_end:
.org 0x22E8
m68k_0022e8:
        move.w 0xf602:w,%d0
m68k_0022e8_end:
.org 0x22EC
m68k_0022ec:
        andi.w #0x60,%d0
m68k_0022ec_end:
.org 0x22F0
m68k_0022f0:
        beq.w (. + 14)
m68k_0022f0_end:
.org 0x22F4
m68k_0022f4:
        move.w #0x1,0xefde:w
m68k_0022f4_end:
.org 0x22FA
m68k_0022fa:
        bra.w (. + 14)
m68k_0022fa_end:
.org 0x22FE
m68k_0022fe:
        btst.b #0x4,0xf603:w
m68k_0022fe_end:
.org 0x2304
m68k_002304:
        beq.w (. + 54)
m68k_002304_end:
.org 0x2308
m68k_002308:
        bsr.w (. + 164)
m68k_002308_end:
.org 0x230C
m68k_00230c:
        move.w #0x200,%d0
m68k_00230c_end:
.org 0x2310
m68k_002310:
        cmpi.w #0x1,0xefe0:w
m68k_002310_end:
.org 0x2316
m68k_002316:
        bne.w (. + 16)
m68k_002316_end:
.org 0x231A
m68k_00231a:
        move.w #0x400,%d0
m68k_00231a_end:
.org 0x231E
m68k_00231e:
        clr.w 0xf362:w
m68k_00231e_end:
.org 0x2322
m68k_002322:
        subq.w #0x1,0xf378:w
m68k_002322_end:
.org 0x2326
m68k_002326:
        move.w %d0,0xf612:w
m68k_002326_end:
.org 0x232A
m68k_00232a:
        clr.w 0xf352:w
m68k_00232a_end:
.org 0x232E
m68k_00232e:
        bsr.w (. + 200)
m68k_00232e_end:
.org 0x2332
m68k_002332:
        clr.w 0xf3de:w
m68k_002332_end:
.org 0x2336
m68k_002336:
        bra.w (. + 116)
m68k_002336_end:
.org 0x233A
m68k_00233a:
        move.w #0x1,0xf77a:w
m68k_00233a_end:
.org 0x2340
m68k_002340:
        bsr.w (. + 182)
m68k_002340_end:
.org 0x2344
m68k_002344:
        cmpi.w #0x1,0xf636:w
m68k_002344_end:
.org 0x234A
m68k_00234a:
        beq.w (. + 96)
m68k_00234a_end:
.org 0x234E
m68k_00234e:
        btst.b #0x0,0xf603:w
m68k_00234e_end:
.org 0x2354
m68k_002354:
        bne.w (. + 36)
m68k_002354_end:
.org 0x2358
m68k_002358:
        btst.b #0x1,0xf603:w
m68k_002358_end:
.org 0x235E
m68k_00235e:
        beq.w (. + 76)
m68k_00235e_end:
.org 0x2362
m68k_002362:
        move.w 0xf378:w,%d0
m68k_002362_end:
.org 0x2366
m68k_002366:
        addq.w #0x1,%d0
m68k_002366_end:
.org 0x2368
m68k_002368:
        cmp.w 0xf636:w,%d0
m68k_002368_end:
.org 0x236C
m68k_00236c:
        bls.w (. + 26)
m68k_00236c_end:
.org 0x2370
m68k_002370:
        move.w #0x1,%d0
m68k_002370_end:
.org 0x2374
m68k_002374:
        bra.w (. + 18)
m68k_002374_end:
.org 0x2378
m68k_002378:
        move.w 0xf378:w,%d0
m68k_002378_end:
.org 0x237C
m68k_00237c:
        subq.w #0x1,%d0
m68k_00237c_end:
.org 0x237E
m68k_00237e:
        bne.w (. + 8)
m68k_00237e_end:
.org 0x2382
m68k_002382:
        move.w 0xf636:w,%d0
m68k_002382_end:
.org 0x2386
m68k_002386:
        move.w %d0,0xf378:w
m68k_002386_end:
.org 0x238A
m68k_00238a:
        lsl.w #0x1,%d0
m68k_00238a_end:
.org 0x238C
m68k_00238c:
        lea.l 0xf4fe:w,%a0
m68k_00238c_end:
.org 0x2390
m68k_002390:
        move.w (%a0, %d0.w),%d0
m68k_002390_end:
.org 0x2394
m68k_002394:
        andi.w #0xff,%d0
m68k_002394_end:
.org 0x2398
m68k_002398:
        move.w %d0,0xf372:w
m68k_002398_end:
.org 0x239C
m68k_00239c:
        move.w #0x207,0xf612:w
m68k_00239c_end:
.org 0x23A2
m68k_0023a2:
        clr.w 0xf362:w
m68k_0023a2_end:
.org 0x23A6
m68k_0023a6:
        clr.w 0xf352:w
m68k_0023a6_end:
.org 0x23AA
m68k_0023aa:
        rts
m68k_0023aa_end:
.org 0x23AC
m68k_0023ac:
        move.w 0xf378:w,%d0
m68k_0023ac_end:
.org 0x23B0
m68k_0023b0:
        subi.w #0x3,%d0
m68k_0023b0_end:
.org 0x23B4
m68k_0023b4:
        bpl.w (. + 6)
m68k_0023b4_end:
.org 0x23B8
m68k_0023b8:
        clr.w %d0
m68k_0023b8_end:
.org 0x23BA
m68k_0023ba:
        move.w #0x7,%d1
m68k_0023ba_end:
.org 0x23BE
m68k_0023be:
        tst.w 0xf6c4:w
m68k_0023be_end:
.org 0x23C2
m68k_0023c2:
        bne.w (. + 22)
m68k_0023c2_end:
.org 0x23C6
m68k_0023c6:
        tst.w 0xf36c:w
m68k_0023c6_end:
.org 0x23CA
m68k_0023ca:
        bne.w (. + 14)
m68k_0023ca_end:
.org 0x23CE
m68k_0023ce:
        btst.b #0x6,0xf3a4:w
m68k_0023ce_end:
.org 0x23D4
m68k_0023d4:
        beq.w (. + 8)
m68k_0023d4_end:
.org 0x23D8
m68k_0023d8:
        move.w #0x5,%d1
m68k_0023d8_end:
.org 0x23DC
m68k_0023dc:
        move.w 0xf636:w,%d2
m68k_0023dc_end:
.org 0x23E0
m68k_0023e0:
        sub.w %d1,%d2
m68k_0023e0_end:
.org 0x23E2
m68k_0023e2:
        bpl.w (. + 6)
m68k_0023e2_end:
.org 0x23E6
m68k_0023e6:
        clr.w %d2
m68k_0023e6_end:
.org 0x23E8
m68k_0023e8:
        cmp.w %d2,%d0
m68k_0023e8_end:
.org 0x23EA
m68k_0023ea:
        bls.w (. + 6)
m68k_0023ea_end:
.org 0x23EE
m68k_0023ee:
        move.w %d2,%d0
m68k_0023ee_end:
.org 0x23F0
m68k_0023f0:
        move.w %d0,0xf658:w
m68k_0023f0_end:
.org 0x23F4
m68k_0023f4:
        rts
m68k_0023f4_end:
.org 0x5864
m68k_005864:
        move.w #0xc308,%d3
m68k_005864_end:
.org 0x5884
m68k_005884:
        move.w #0xc314,%d3
m68k_005884_end:
.org 0x5888
m68k_005888:
        bra.b (. + -32)
m68k_005888_end:
.org 0x588A
m68k_00588a:
        lea.l 0x1e(%a0),%a6
m68k_00588a_end:
.org 0x588E
m68k_00588e:
        move.w #0xc001,(%a6)+
m68k_00588e_end:
.org 0x5892
m68k_005892:
        lea.l 0xe65c:w,%a1
m68k_005892_end:
.org 0x5896
m68k_005896:
        clr.w %d7
m68k_005896_end:
.org 0x5898
m68k_005898:
        bsr.w (. + 76)
m68k_005898_end:
.org 0x589C
m68k_00589c:
        bsr.w (. + 128)
m68k_00589c_end:
.org 0x58A0
m68k_0058a0:
        rts
m68k_0058a0_end:
.org 0x58A2
m68k_0058a2:
        lea.l 0x1e(%a0),%a6
m68k_0058a2_end:
.org 0x58A6
m68k_0058a6:
        move.w #0xc001,(%a6)+
m68k_0058a6_end:
.org 0x58AA
m68k_0058aa:
        lea.l 0xdffc:w,%a1
m68k_0058aa_end:
.org 0x58AE
m68k_0058ae:
        clr.w %d7
m68k_0058ae_end:
.org 0x58B0
m68k_0058b0:
        bsr.w (. + 52)
m68k_0058b0_end:
.org 0x58B4
m68k_0058b4:
        bsr.w (. + 104)
m68k_0058b4_end:
.org 0x58B8
m68k_0058b8:
        rts
m68k_0058b8_end:
.org 0x58BA
m68k_0058ba:
        tst.b 0xf62e:w
m68k_0058ba_end:
.org 0x58BE
m68k_0058be:
        bpl.b (. + 38)
m68k_0058be_end:
.org 0x58C0
m68k_0058c0:
        clr.w %d0
m68k_0058c0_end:
.org 0x58C2
m68k_0058c2:
        clr.w %d1
m68k_0058c2_end:
.org 0x58C4
m68k_0058c4:
        move.b 24(%pc, %d6.w),%d0
m68k_0058c4_end:
.org 0x58C8
m68k_0058c8:
        move.b 21(%pc, %d6.w),%d1
m68k_0058c8_end:
.org 0x58CC
m68k_0058cc:
        move.w #0xc001,(%a6)+
m68k_0058cc_end:
.org 0x58D0
m68k_0058d0:
        dbra %d0,(. + -4)
m68k_0058d0_end:
.org 0x58D4
m68k_0058d4:
        move.w #0xc385,(%a6)+
m68k_0058d4_end:
.org 0x58D8
m68k_0058d8:
        dbra %d1,(. + -4)
m68k_0058d8_end:
.org 0x58DC
m68k_0058dc:
        rts
m68k_0058dc_end:
.org 0x58E4
m68k_0058e4:
        move.w 0xf364:w,%d0
m68k_0058e4_end:
.org 0x58E8
m68k_0058e8:
        lsl.w #0x2,%d0
m68k_0058e8_end:
.org 0x58EA
m68k_0058ea:
        move.l (%a1, %d0.w),%d0
m68k_0058ea_end:
.org 0x58EE
m68k_0058ee:
        move.w #0xc386,%d1
m68k_0058ee_end:
.org 0x58F2
m68k_0058f2:
        move.w #0xc001,%d2
m68k_0058f2_end:
.org 0x58F6
m68k_0058f6:
        clr.w %d4
m68k_0058f6_end:
.org 0x58F8
m68k_0058f8:
        jsr 4(%pc, %d7.w)
m68k_0058f8_end:
.org 0x58FC
m68k_0058fc:
        rts
m68k_0058fc_end:
.org 0x591C
m68k_00591c:
        move.w #0x6,%d0
m68k_00591c_end:
.org 0x5920
m68k_005920:
        move.w #0xc001,(%a0)+
m68k_005920_end:
.org 0x5924
m68k_005924:
        dbra %d0,(. + -4)
m68k_005924_end:
.org 0x5928
m68k_005928:
        rts
m68k_005928_end:
.org 0x592A
m68k_00592a:
        lea.l 0x1e(%a0),%a6
m68k_00592a_end:
.org 0x592E
m68k_00592e:
        move.w #0xc001,(%a6)+
m68k_00592e_end:
.org 0x5932
m68k_005932:
        lea.l 0xe09c:w,%a1
m68k_005932_end:
.org 0x5936
m68k_005936:
        clr.w %d7
m68k_005936_end:
.org 0x5938
m68k_005938:
        bsr.b (. + -84)
m68k_005938_end:
.org 0x593A
m68k_00593a:
        bra.b (. + -30)
m68k_00593a_end:
.org 0x593C
m68k_00593c:
        lea.l 0x1e(%a0),%a6
m68k_00593c_end:
.org 0x5940
m68k_005940:
        lea.l 0xe13c:w,%a1
m68k_005940_end:
.org 0x5944
m68k_005944:
        move.w #0x8,%d7
m68k_005944_end:
.org 0x5948
m68k_005948:
        bsr.b (. + -100)
m68k_005948_end:
.org 0x594A
m68k_00594a:
        move.w #0xc386,(%a6)+
m68k_00594a_end:
.org 0x594E
m68k_00594e:
        move.w #0xc386,(%a6)+
m68k_00594e_end:
.org 0x5952
m68k_005952:
        move.w #0xc386,(%a6)+
m68k_005952_end:
.org 0x5956
m68k_005956:
        bra.b (. + -58)
m68k_005956_end:
.org 0x5958
m68k_005958:
        lea.l 0x1e(%a0),%a6
m68k_005958_end:
.org 0x595C
m68k_00595c:
        move.w #0xc001,(%a6)+
m68k_00595c_end:
.org 0x5960
m68k_005960:
        lea.l 0xe3bc:w,%a1
m68k_005960_end:
.org 0x5964
m68k_005964:
        clr.w %d7
m68k_005964_end:
.org 0x5966
m68k_005966:
        bsr.w (. + -130)
m68k_005966_end:
.org 0x596A
m68k_00596a:
        bra.b (. + -78)
m68k_00596a_end:
.org 0x596C
m68k_00596c:
        lea.l 0x1e(%a0),%a6
m68k_00596c_end:
.org 0x5970
m68k_005970:
        move.w #0xc001,(%a6)+
m68k_005970_end:
.org 0x5974
m68k_005974:
        lea.l 0xe45c:w,%a1
m68k_005974_end:
.org 0x5978
m68k_005978:
        clr.w %d7
m68k_005978_end:
.org 0x597A
m68k_00597a:
        clr.w %d6
m68k_00597a_end:
.org 0x597C
m68k_00597c:
        bsr.w (. + -194)
m68k_00597c_end:
.org 0x5980
m68k_005980:
        bra.b (. + -100)
m68k_005980_end:
.org 0x5982
m68k_005982:
        lea.l 0x1e(%a0),%a6
m68k_005982_end:
.org 0x5986
m68k_005986:
        move.w #0xc001,(%a6)+
m68k_005986_end:
.org 0x598A
m68k_00598a:
        lea.l 0xe4fc:w,%a1
m68k_00598a_end:
.org 0x598E
m68k_00598e:
        clr.w %d7
m68k_00598e_end:
.org 0x5990
m68k_005990:
        move.w #0x4,%d6
m68k_005990_end:
.org 0x5994
m68k_005994:
        bsr.w (. + -218)
m68k_005994_end:
.org 0x5998
m68k_005998:
        bra.b (. + -124)
m68k_005998_end:
.org 0x599A
m68k_00599a:
        move.w #0xc001,%d3
m68k_00599a_end:
.org 0x599E
m68k_00599e:
        bsr.w (. + 140)
m68k_00599e_end:
.org 0x59A2
m68k_0059a2:
        lea.l 0x1e(%a0),%a6
m68k_0059a2_end:
.org 0x59A6
m68k_0059a6:
        lea.l 0xe1dc:w,%a1
m68k_0059a6_end:
.org 0x59AA
m68k_0059aa:
        move.w #0x4,%d7
m68k_0059aa_end:
.org 0x59AE
m68k_0059ae:
        bsr.w (. + -202)
m68k_0059ae_end:
.org 0x59B2
m68k_0059b2:
        move.w #0x4,%d0
m68k_0059b2_end:
.org 0x59B6
m68k_0059b6:
        move.w #0xc001,(%a0)+
m68k_0059b6_end:
.org 0x59BA
m68k_0059ba:
        dbra %d0,(. + -4)
m68k_0059ba_end:
.org 0x59BE
m68k_0059be:
        rts
m68k_0059be_end:
.org 0x59D8
m68k_0059d8:
        move.w #0xc05d,%d3
m68k_0059d8_end:
.org 0x59DC
m68k_0059dc:
        bsr.w (. + 78)
m68k_0059dc_end:
.org 0x59E0
m68k_0059e0:
        lea.l 0x1e(%a0),%a6
m68k_0059e0_end:
.org 0x59E4
m68k_0059e4:
        lea.l 0xe27c:w,%a1
m68k_0059e4_end:
.org 0x59E8
m68k_0059e8:
        move.w #0x4,%d7
m68k_0059e8_end:
.org 0x59EC
m68k_0059ec:
        bsr.w (. + -264)
m68k_0059ec_end:
.org 0x59F0
m68k_0059f0:
        bra.b (. + -62)
m68k_0059f0_end:
.org 0x59F2
m68k_0059f2:
        move.w #0xc025,%d3
m68k_0059f2_end:
.org 0x59F6
m68k_0059f6:
        bsr.w (. + 52)
m68k_0059f6_end:
.org 0x59FA
m68k_0059fa:
        lea.l 0x1e(%a0),%a6
m68k_0059fa_end:
.org 0x59FE
m68k_0059fe:
        lea.l 0xe31c:w,%a1
m68k_0059fe_end:
.org 0x5A02
m68k_005a02:
        move.w #0x4,%d7
m68k_005a02_end:
.org 0x5A06
m68k_005a06:
        move.w #0x2,%d6
m68k_005a06_end:
.org 0x5A0A
m68k_005a0a:
        bsr.w (. + -336)
m68k_005a0a_end:
.org 0x5A0E
m68k_005a0e:
        bra.b (. + -92)
m68k_005a0e_end:
.org 0x5A10
m68k_005a10:
        move.w #0xc031,%d3
m68k_005a10_end:
.org 0x5A14
m68k_005a14:
        bsr.w (. + 22)
m68k_005a14_end:
.org 0x5A18
m68k_005a18:
        lea.l 0x1e(%a0),%a6
m68k_005a18_end:
.org 0x5A1C
m68k_005a1c:
        lea.l 0xe59c:w,%a1
m68k_005a1c_end:
.org 0x5A20
m68k_005a20:
        move.w #0x4,%d7
m68k_005a20_end:
.org 0x5A24
m68k_005a24:
        bsr.w (. + -320)
m68k_005a24_end:
.org 0x5A28
m68k_005a28:
        bra.b (. + -118)
m68k_005a28_end:
.org 0xAAB4
m68k_00aab4:
        move.w #0x2,%d2
m68k_00aab4_end:
.org 0xAAB8
m68k_00aab8:
        lea.l 0xe1dc:w,%a1
m68k_00aab8_end:
.org 0xAABC
m68k_00aabc:
        move.w #0x483,(%a0)+
m68k_00aabc_end:
.org 0xAAC0
m68k_00aac0:
        dbra %d2,(. + -4)
m68k_00aac0_end:
.org 0xAAC4
m68k_00aac4:
        move.w %d0,%d2
m68k_00aac4_end:
.org 0xAAC6
m68k_00aac6:
        lsl.w #0x2,%d2
m68k_00aac6_end:
.org 0xAAC8
m68k_00aac8:
        move.l (%a1, %d2.w),%d0
m68k_00aac8_end:
.org 0xAACC
m68k_00aacc:
        move.w #0x400,%d1
m68k_00aacc_end:
.org 0xAAD0
m68k_00aad0:
        move.w #0x483,%d2
m68k_00aad0_end:
.org 0xAAD4
m68k_00aad4:
        movea.l %a0,%a6
m68k_00aad4_end:
.org 0xAAD6
m68k_00aad6:
        clr.w %d4
m68k_00aad6_end:
.org 0xAAD8
m68k_00aad8:
        jsr 0x12744:l
m68k_00aad8_end:
.org 0xAADE
m68k_00aade:
        movea.l %a6,%a0
m68k_00aade_end:
.org 0xAAE0
m68k_00aae0:
        rts
m68k_00aae0_end:
.org 0xAAE2
m68k_00aae2:
        move.w #0x3,%d2
m68k_00aae2_end:
.org 0xAAE6
m68k_00aae6:
        lea.l 0xe45c:w,%a1
m68k_00aae6_end:
.org 0xAAEA
m68k_00aaea:
        move.w #0x483,(%a0)+
m68k_00aaea_end:
.org 0xAAEE
m68k_00aaee:
        dbra %d2,(. + -4)
m68k_00aaee_end:
.org 0xAAF2
m68k_00aaf2:
        move.w %d0,%d2
m68k_00aaf2_end:
.org 0xAAF4
m68k_00aaf4:
        lsl.w #0x2,%d2
m68k_00aaf4_end:
.org 0xAAF6
m68k_00aaf6:
        move.l (%a1, %d2.w),%d0
m68k_00aaf6_end:
.org 0xAAFA
m68k_00aafa:
        move.w #0x400,%d1
m68k_00aafa_end:
.org 0xAAFE
m68k_00aafe:
        move.w #0x483,%d2
m68k_00aafe_end:
.org 0xAB02
m68k_00ab02:
        movea.l %a0,%a6
m68k_00ab02_end:
.org 0xAB04
m68k_00ab04:
        clr.w %d4
m68k_00ab04_end:
.org 0xAB06
m68k_00ab06:
        jsr 0x1274c:l
m68k_00ab06_end:
.org 0xAB0C
m68k_00ab0c:
        movea.l %a6,%a0
m68k_00ab0c_end:
.org 0xAB0E
m68k_00ab0e:
        rts
m68k_00ab0e_end:
.org 0xAB2A
m68k_00ab2a:
        move.w #0x2,%d2
m68k_00ab2a_end:
.org 0xAB2E
m68k_00ab2e:
        lea.l 0xe31c:w,%a1
m68k_00ab2e_end:
.org 0xAB32
m68k_00ab32:
        bra.b (. + -118)
m68k_00ab32_end:
.org 0xAB34
m68k_00ab34:
        move.w #0x2,%d2
m68k_00ab34_end:
.org 0xAB38
m68k_00ab38:
        lea.l 0xe3bc:w,%a1
m68k_00ab38_end:
.org 0xAB3C
m68k_00ab3c:
        bra.w (. + -128)
m68k_00ab3c_end:
.org 0x1009C
m68k_01009c:
        subq.b #0x1,%d1
m68k_01009c_end:
.org 0x1009E
m68k_01009e:
        rts
m68k_01009e_end:
.org 0x100A0
m68k_0100a0:
        addi.b #0x1,%d2
m68k_0100a0_end:
.org 0x100A4
m68k_0100a4:
        rts
m68k_0100a4_end:
.org 0x100A6
m68k_0100a6:
        addi.b #0x1,%d1
m68k_0100a6_end:
.org 0x100AA
m68k_0100aa:
        rts
m68k_0100aa_end:
.org 0x100AC
m68k_0100ac:
        subi.b #0x1,%d2
m68k_0100ac_end:
.org 0x100B0
m68k_0100b0:
        rts
m68k_0100b0_end:
.org 0x100B2
m68k_0100b2:
        subi.b #0x1,%d1
m68k_0100b2_end:
.org 0x100B6
m68k_0100b6:
        addi.b #0x1,%d2
m68k_0100b6_end:
.org 0x100BA
m68k_0100ba:
        rts
m68k_0100ba_end:
.org 0x100BC
m68k_0100bc:
        addi.b #0x1,%d1
m68k_0100bc_end:
.org 0x100C0
m68k_0100c0:
        addi.b #0x1,%d2
m68k_0100c0_end:
.org 0x100C4
m68k_0100c4:
        rts
m68k_0100c4_end:
.org 0x100C6
m68k_0100c6:
        addi.b #0x1,%d1
m68k_0100c6_end:
.org 0x100CA
m68k_0100ca:
        subi.b #0x1,%d2
m68k_0100ca_end:
.org 0x100CE
m68k_0100ce:
        rts
m68k_0100ce_end:
.org 0x100D0
m68k_0100d0:
        subi.b #0x1,%d1
m68k_0100d0_end:
.org 0x100D4
m68k_0100d4:
        subi.b #0x1,%d2
m68k_0100d4_end:
.org 0x100D8
m68k_0100d8:
        rts
m68k_0100d8_end:
.org 0x12102
m68k_012102:
        bsr.w (. + 10)
m68k_012102_end:
.org 0x12106
m68k_012106:
        bsr.w (. + 278)
m68k_012106_end:
.org 0x1210A
m68k_01210a:
        rts
m68k_01210a_end:
.org 0x1210C
m68k_01210c:
        move.b 0xf602:w,%d0
m68k_01210c_end:
.org 0x12110
m68k_012110:
        andi.w #0x3,%d0
m68k_012110_end:
.org 0x12114
m68k_012114:
        beq.b (. + 58)
m68k_012114_end:
.org 0x12116
m68k_012116:
        subq.w #0x1,0xf608:w
m68k_012116_end:
.org 0x1211A
m68k_01211a:
        bne.w (. + 164)
m68k_01211a_end:
.org 0x1211E
m68k_01211e:
        move.w #0x10,0xf608:w
m68k_01211e_end:
.org 0x12124
m68k_012124:
        btst.l #0x1,%d0
m68k_012124_end:
.org 0x12128
m68k_012128:
        bne.b (. + 20)
m68k_012128_end:
.org 0x1212A
m68k_01212a:
        subq.w #0x1,0xf3f0:w
m68k_01212a_end:
.org 0x1212E
m68k_01212e:
        bpl.w (. + 144)
m68k_01212e_end:
.org 0x12132
m68k_012132:
        move.w #0x2,0xf3f0:w
m68k_012132_end:
.org 0x12138
m68k_012138:
        bra.w (. + 134)
m68k_012138_end:
.org 0x1213C
m68k_01213c:
        addq.w #0x1,0xf3f0:w
m68k_01213c_end:
.org 0x12140
m68k_012140:
        cmpi.w #0x3,0xf3f0:w
m68k_012140_end:
.org 0x12146
m68k_012146:
        bcs.b (. + 120)
m68k_012146_end:
.org 0x12148
m68k_012148:
        clr.w 0xf3f0:w
m68k_012148_end:
.org 0x1214C
m68k_01214c:
        bra.b (. + 114)
m68k_01214c_end:
.org 0x1214E
m68k_01214e:
        move.w 0xf602:w,%d0
m68k_01214e_end:
.org 0x12152
m68k_012152:
        andi.w #0xc,%d0
m68k_012152_end:
.org 0x12156
m68k_012156:
        beq.w (. + 98)
m68k_012156_end:
.org 0x1215A
m68k_01215a:
        subq.w #0x1,0xf608:w
m68k_01215a_end:
.org 0x1215E
m68k_01215e:
        bne.w (. + 96)
m68k_01215e_end:
.org 0x12162
m68k_012162:
        move.w #0xc,0xf608:w
m68k_012162_end:
.org 0x12168
m68k_012168:
        lea.l 0xef64:w,%a0
m68k_012168_end:
.org 0x1216C
m68k_01216c:
        lea.l 0xefb2:w,%a1
m68k_01216c_end:
.org 0x12170
m68k_012170:
        move.w 0xf3f0:w,%d1
m68k_012170_end:
.org 0x12174
m68k_012174:
        lsl.w #0x1,%d1
m68k_012174_end:
.org 0x12176
m68k_012176:
        move.w (%a0, %d1.w),%d2
m68k_012176_end:
.org 0x1217A
m68k_01217a:
        move.w (%a1, %d1.w),%d3
m68k_01217a_end:
.org 0x1217E
m68k_01217e:
        btst.l #0x3,%d0
m68k_01217e_end:
.org 0x12182
m68k_012182:
        bne.w (. + 26)
m68k_012182_end:
.org 0x12186
m68k_012186:
        subq.w #0x1,%d2
m68k_012186_end:
.org 0x12188
m68k_012188:
        bcc.w (. + 8)
m68k_012188_end:
.org 0x1218C
m68k_01218c:
        move.w #0x2,%d2
m68k_01218c_end:
.org 0x12190
m68k_012190:
        btst.l %d2,%d3
m68k_012190_end:
.org 0x12192
m68k_012192:
        beq.b (. + -12)
m68k_012192_end:
.org 0x12194
m68k_012194:
        move.w %d2,(%a0, %d1.w)
m68k_012194_end:
.org 0x12198
m68k_012198:
        bra.w (. + 24)
m68k_012198_end:
.org 0x1219C
m68k_01219c:
        addq.w #0x1,%d2
m68k_01219c_end:
.org 0x1219E
m68k_01219e:
        cmpi.w #0x3,%d2
m68k_01219e_end:
.org 0x121A2
m68k_0121a2:
        bcs.w (. + 6)
m68k_0121a2_end:
.org 0x121A6
m68k_0121a6:
        clr.w %d2
m68k_0121a6_end:
.org 0x121A8
m68k_0121a8:
        btst.l %d2,%d3
m68k_0121a8_end:
.org 0x121AA
m68k_0121aa:
        beq.b (. + -14)
m68k_0121aa_end:
.org 0x121AC
m68k_0121ac:
        move.w %d2,(%a0, %d1.w)
m68k_0121ac_end:
.org 0x121B0
m68k_0121b0:
        bsr.w (. + -660)
m68k_0121b0_end:
.org 0x121B4
m68k_0121b4:
        bra.w (. + 102)
m68k_0121b4_end:
.org 0x121B8
m68k_0121b8:
        move.w #0x1,0xf608:w
m68k_0121b8_end:
.org 0x121BE
m68k_0121be:
        btst.b #0x5,0xf603:w
m68k_0121be_end:
.org 0x121C4
m68k_0121c4:
        beq.b (. + 56)
m68k_0121c4_end:
.org 0x121C6
m68k_0121c6:
        move.w 0xf3f0:w,%d0
m68k_0121c6_end:
.org 0x121CA
m68k_0121ca:
        lsl.w #0x2,%d0
m68k_0121ca_end:
.org 0x121CC
m68k_0121cc:
        lea.l 0xef6a:w,%a0
m68k_0121cc_end:
.org 0x121D0
m68k_0121d0:
        move.l (%a0, %d0.w),%d0
m68k_0121d0_end:
.org 0x121D4
m68k_0121d4:
        cmp.l 0xf3f8:w,%d0
m68k_0121d4_end:
.org 0x121D8
m68k_0121d8:
        bhi.b (. + 66)
m68k_0121d8_end:
.org 0x121DA
m68k_0121da:
        clr.w 0xf386:w
m68k_0121da_end:
.org 0x121DE
m68k_0121de:
        jsr 0xc0b6:l
m68k_0121de_end:
.org 0x121E4
m68k_0121e4:
        move.w #0x208,0xf612:w
m68k_0121e4_end:
.org 0x121EA
m68k_0121ea:
        move.w #0x3,0xf362:w
m68k_0121ea_end:
.org 0x121F0
m68k_0121f0:
        move.w #0x12,0xf36a:w
m68k_0121f0_end:
.org 0x121F6
m68k_0121f6:
        bsr.w (. + 156)
m68k_0121f6_end:
.org 0x121FA
m68k_0121fa:
        bra.b (. + 32)
m68k_0121fa_end:
.org 0x121FC
m68k_0121fc:
        btst.b #0x4,0xf603:w
m68k_0121fc_end:
.org 0x12202
m68k_012202:
        beq.b (. + 24)
m68k_012202_end:
.org 0x12204
m68k_012204:
        move.w #0x208,0xf612:w
m68k_012204_end:
.org 0x1220A
m68k_01220a:
        move.w #0x2,0xf362:w
m68k_01220a_end:
.org 0x12210
m68k_012210:
        move.w #0x12,0xf36a:w
m68k_012210_end:
.org 0x12216
m68k_012216:
        bsr.w (. + 124)
m68k_012216_end:
.org 0x1221A
m68k_01221a:
        rts
m68k_01221a_end:
.org 0x1221C
m68k_01221c:
        btst.b #0x3,0xf321:w
m68k_01221c_end:
.org 0x12222
m68k_012222:
        bne.b (. + 36)
m68k_012222_end:
.org 0x12224
m68k_012224:
        lea.l 34(%pc),%a0
m68k_012224_end:
.org 0x12228
m68k_012228:
        nop
m68k_012228_end:
.org 0x1222A
m68k_01222a:
        move.w 0xf3f0:w,%d0
m68k_01222a_end:
.org 0x1222E
m68k_01222e:
        lsl.w #0x1,%d0
m68k_01222e_end:
.org 0x12230
m68k_012230:
        add.w 0xf3f0:w,%d0
m68k_012230_end:
.org 0x12234
m68k_012234:
        lsl.w #0x3,%d0
m68k_012234_end:
.org 0x12236
m68k_012236:
        addi.w #0x38,%d0
m68k_012236_end:
.org 0x1223A
m68k_01223a:
        move.w #0xc8,%d1
m68k_01223a_end:
.org 0x1223E
m68k_01223e:
        clr.w %d2
m68k_01223e_end:
.org 0x12240
m68k_012240:
        jsr 0xac08:l
m68k_012240_end:
.org 0x12246
m68k_012246:
        rts
m68k_012246_end:
.org 0x12292
m68k_012292:
        lea.l 0xd100:w,%a0
m68k_012292_end:
.org 0x12296
m68k_012296:
        adda.w 0xf31a:w,%a0
m68k_012296_end:
.org 0x1229A
m68k_01229a:
        move.w #0xd,0x5a(%a0)
m68k_01229a_end:
.org 0x122A0
m68k_0122a0:
        move.w #0xd,0x3c(%a0)
m68k_0122a0_end:
.org 0x122A6
m68k_0122a6:
        move.w #0xd,0x1e(%a0)
m68k_0122a6_end:
.org 0x122AC
m68k_0122ac:
        move.w #0xd,(%a0)+
m68k_0122ac_end:
.org 0x122B0
m68k_0122b0:
        move.w #0xc234,0x5a(%a0)
m68k_0122b0_end:
.org 0x122B6
m68k_0122b6:
        move.w #0xc1b4,0x3c(%a0)
m68k_0122b6_end:
.org 0x122BC
m68k_0122bc:
        move.w #0xc134,0x1e(%a0)
m68k_0122bc_end:
.org 0x122C2
m68k_0122c2:
        move.w #0xc0b4,(%a0)+
m68k_0122c2_end:
.org 0x122C6
m68k_0122c6:
        move.w #0xc,%d0
m68k_0122c6_end:
.org 0x122CA
m68k_0122ca:
        move.w #0x8000,0x5a(%a0)
m68k_0122ca_end:
.org 0x122D0
m68k_0122d0:
        move.w #0x8000,0x3c(%a0)
m68k_0122d0_end:
.org 0x122D6
m68k_0122d6:
        move.w #0x8000,0x1e(%a0)
m68k_0122d6_end:
.org 0x122DC
m68k_0122dc:
        move.w #0x8000,(%a0)+
m68k_0122dc_end:
.org 0x122E0
m68k_0122e0:
        dbra %d0,(. + -22)
m68k_0122e0_end:
.org 0x122E4
m68k_0122e4:
        adda.w #0x5a,%a0
m68k_0122e4_end:
.org 0x122E8
m68k_0122e8:
        move.w #0x9,%d0
m68k_0122e8_end:
.org 0x122EC
m68k_0122ec:
        move.w #0xc3b2,%d1
m68k_0122ec_end:
.org 0x122F0
m68k_0122f0:
        move.w #0xe,(%a0)+
m68k_0122f0_end:
.org 0x122F4
m68k_0122f4:
        move.w %d1,(%a0)+
m68k_0122f4_end:
.org 0x122F6
m68k_0122f6:
        addi.w #0x80,%d1
m68k_0122f6_end:
.org 0x122FA
m68k_0122fa:
        move.w #0xd,%d2
m68k_0122fa_end:
.org 0x122FE
m68k_0122fe:
        move.w #0x8000,(%a0)+
m68k_0122fe_end:
.org 0x12302
m68k_012302:
        dbra %d2,(. + -4)
m68k_012302_end:
.org 0x12306
m68k_012306:
        dbra %d0,(. + -22)
m68k_012306_end:
.org 0x1230A
m68k_01230a:
        clr.w (%a0)
m68k_01230a_end:
.org 0x1230C
m68k_01230c:
        addi.w #0x1b8,0xf31a:w
m68k_01230c_end:
.org 0x12312
m68k_012312:
        rts
m68k_012312_end:
.org 0x12418
m68k_012418:
        move.b 0xf602:w,%d0
m68k_012418_end:
.org 0x1241C
m68k_01241c:
        andi.w #0xc,%d0
m68k_01241c_end:
.org 0x12420
m68k_012420:
        beq.b (. + 80)
m68k_012420_end:
.org 0x12422
m68k_012422:
        subq.w #0x1,0xf608:w
m68k_012422_end:
.org 0x12426
m68k_012426:
        bne.w (. + 212)
m68k_012426_end:
.org 0x1242A
m68k_01242a:
        move.w #0xc,0xf608:w
m68k_01242a_end:
.org 0x12430
m68k_012430:
        btst.l #0x3,%d0
m68k_012430_end:
.org 0x12434
m68k_012434:
        bne.b (. + 38)
m68k_012434_end:
.org 0x12436
m68k_012436:
        move.w #0x5,%d1
m68k_012436_end:
.org 0x1243A
m68k_01243a:
        sub.w 0xf39a:w,%d1
m68k_01243a_end:
.org 0x1243E
m68k_01243e:
        lsl.w #0x2,%d1
m68k_01243e_end:
.org 0x12440
m68k_012440:
        lea.l 190(%pc),%a0
m68k_012440_end:
.org 0x12444
m68k_012444:
        nop
m68k_012444_end:
.org 0x12446
m68k_012446:
        move.l (%a0, %d1.w),%d2
m68k_012446_end:
.org 0x1244A
m68k_01244a:
        cmp.l 0xf3f8:w,%d2
m68k_01244a_end:
.org 0x1244E
m68k_01244e:
        bhi.w (. + 172)
m68k_01244e_end:
.org 0x12452
m68k_012452:
        subq.w #0x1,0xf39a:w
m68k_012452_end:
.org 0x12456
m68k_012456:
        bra.w (. + 160)
m68k_012456_end:
.org 0x1245A
m68k_01245a:
        move.w 0xf39a:w,%d1
m68k_01245a_end:
.org 0x1245E
m68k_01245e:
        addq.w #0x1,%d1
m68k_01245e_end:
.org 0x12460
m68k_012460:
        cmpi.w #0x5,%d1
m68k_012460_end:
.org 0x12464
m68k_012464:
        bhi.w (. + 150)
m68k_012464_end:
.org 0x12468
m68k_012468:
        move.w %d1,0xf39a:w
m68k_012468_end:
.org 0x1246C
m68k_01246c:
        bra.w (. + 138)
m68k_01246c_end:
.org 0x12470
m68k_012470:
        move.b 0xf602:w,%d0
m68k_012470_end:
.org 0x12474
m68k_012474:
        andi.w #0x3,%d0
m68k_012474_end:
.org 0x12478
m68k_012478:
        beq.b (. + 120)
m68k_012478_end:
.org 0x1247A
m68k_01247a:
        subq.w #0x1,0xf608:w
m68k_01247a_end:
.org 0x1247E
m68k_01247e:
        bne.w (. + 124)
m68k_01247e_end:
.org 0x12482
m68k_012482:
        move.w #0xc,0xf608:w
m68k_012482_end:
.org 0x12488
m68k_012488:
        btst.l #0x1,%d0
m68k_012488_end:
.org 0x1248C
m68k_01248c:
        bne.b (. + 50)
m68k_01248c_end:
.org 0x1248E
m68k_01248e:
        move.w #0x5,%d0
m68k_01248e_end:
.org 0x12492
m68k_012492:
        sub.w 0xf39a:w,%d0
m68k_012492_end:
.org 0x12496
m68k_012496:
        lsl.w #0x2,%d0
m68k_012496_end:
.org 0x12498
m68k_012498:
        lea.l 98(%pc),%a0
m68k_012498_end:
.org 0x1249C
m68k_01249c:
        move.l (%a0, %d0.w),%d1
m68k_01249c_end:
.org 0x124A0
m68k_0124a0:
        add.l 0xf3f4:w,%d1
m68k_0124a0_end:
.org 0x124A4
m68k_0124a4:
        cmp.l 0xf3f8:w,%d1
m68k_0124a4_end:
.org 0x124A8
m68k_0124a8:
        bhi.w (. + 82)
m68k_0124a8_end:
.org 0x124AC
m68k_0124ac:
        move.l %d1,0xf3f4:w
m68k_0124ac_end:
.org 0x124B0
m68k_0124b0:
        lea.l 98(%pc),%a0
m68k_0124b0_end:
.org 0x124B4
m68k_0124b4:
        move.l (%a0, %d0.w),%d1
m68k_0124b4_end:
.org 0x124B8
m68k_0124b8:
        add.l %d1,0xf3ba:w
m68k_0124b8_end:
.org 0x124BC
m68k_0124bc:
        bra.b (. + 58)
m68k_0124bc_end:
.org 0x124BE
m68k_0124be:
        move.w #0x5,%d0
m68k_0124be_end:
.org 0x124C2
m68k_0124c2:
        sub.w 0xf39a:w,%d0
m68k_0124c2_end:
.org 0x124C6
m68k_0124c6:
        lsl.w #0x2,%d0
m68k_0124c6_end:
.org 0x124C8
m68k_0124c8:
        lea.l 50(%pc),%a0
m68k_0124c8_end:
.org 0x124CC
m68k_0124cc:
        move.l (%a0, %d0.w),%d1
m68k_0124cc_end:
.org 0x124D0
m68k_0124d0:
        move.l 0xf3f4:w,%d2
m68k_0124d0_end:
.org 0x124D4
m68k_0124d4:
        sub.l %d1,%d2
m68k_0124d4_end:
.org 0x124D6
m68k_0124d6:
        bcs.w (. + 36)
m68k_0124d6_end:
.org 0x124DA
m68k_0124da:
        move.l %d2,0xf3f4:w
m68k_0124da_end:
.org 0x124DE
m68k_0124de:
        lea.l 52(%pc),%a0
m68k_0124de_end:
.org 0x124E2
m68k_0124e2:
        nop
m68k_0124e2_end:
.org 0x124E4
m68k_0124e4:
        move.l (%a0, %d0.w),%d1
m68k_0124e4_end:
.org 0x124E8
m68k_0124e8:
        sub.l %d1,0xf3ba:w
m68k_0124e8_end:
.org 0x124EC
m68k_0124ec:
        bra.w (. + 10)
m68k_0124ec_end:
.org 0x124F0
m68k_0124f0:
        move.w #0x1,0xf608:w
m68k_0124f0_end:
.org 0x124F6
m68k_0124f6:
        bsr.w (. + 54)
m68k_0124f6_end:
.org 0x124FA
m68k_0124fa:
        rts
m68k_0124fa_end:
.org 0x1252C
m68k_01252c:
        lea.l 0xd100:w,%a0
m68k_01252c_end:
.org 0x12530
m68k_012530:
        adda.w 0xf31a:w,%a0
m68k_012530_end:
.org 0x12534
m68k_012534:
        move.l 0xf3ba:w,%d0
m68k_012534_end:
.org 0x12538
m68k_012538:
        move.w #0xc386,%d1
m68k_012538_end:
.org 0x1253C
m68k_01253c:
        move.w #0xc001,%d2
m68k_01253c_end:
.org 0x12540
m68k_012540:
        lea.l 0xef00:w,%a6
m68k_012540_end:
.org 0x12544
m68k_012544:
        jsr 0x1270a:l
m68k_012544_end:
.org 0x1254A
m68k_01254a:
        move.w #0x6,(%a0)+
m68k_01254a_end:
.org 0x1254E
m68k_01254e:
        move.w #0xc6ba,(%a0)+
m68k_01254e_end:
.org 0x12552
m68k_012552:
        lea.l 0xef00:w,%a1
m68k_012552_end:
.org 0x12556
m68k_012556:
        move.w #0x5,%d0
m68k_012556_end:
.org 0x1255A
m68k_01255a:
        clr.w %d1
m68k_01255a_end:
.org 0x1255C
m68k_01255c:
        move.w (%a1)+,%d2
m68k_01255c_end:
.org 0x1255E
m68k_01255e:
        cmpi.w #0xc001,%d2
m68k_01255e_end:
.org 0x12562
m68k_012562:
        bne.b (. + 12)
m68k_012562_end:
.org 0x12564
m68k_012564:
        cmp.w 0xf39a:w,%d1
m68k_012564_end:
.org 0x12568
m68k_012568:
        bcs.b (. + 6)
m68k_012568_end:
.org 0x1256A
m68k_01256a:
        move.w #0xc386,%d2
m68k_01256a_end:
.org 0x1256E
m68k_01256e:
        move.w %d2,(%a0)+
m68k_01256e_end:
.org 0x12570
m68k_012570:
        addq.w #0x1,%d1
m68k_012570_end:
.org 0x12572
m68k_012572:
        dbra %d0,(. + -22)
m68k_012572_end:
.org 0x12576
m68k_012576:
        move.l 0xf3f4:w,%d0
m68k_012576_end:
.org 0x1257A
m68k_01257a:
        move.w #0xc386,%d1
m68k_01257a_end:
.org 0x1257E
m68k_01257e:
        move.w #0xc001,%d2
m68k_01257e_end:
.org 0x12582
m68k_012582:
        lea.l 0xef00:w,%a6
m68k_012582_end:
.org 0x12586
m68k_012586:
        jsr 0x1270a:l
m68k_012586_end:
.org 0x1258C
m68k_01258c:
        move.w #0x6,(%a0)+
m68k_01258c_end:
.org 0x12590
m68k_012590:
        move.w #0xc7ba,(%a0)+
m68k_012590_end:
.org 0x12594
m68k_012594:
        lea.l 0xef00:w,%a1
m68k_012594_end:
.org 0x12598
m68k_012598:
        move.w #0x5,%d0
m68k_012598_end:
.org 0x1259C
m68k_01259c:
        move.w (%a1)+,(%a0)+
m68k_01259c_end:
.org 0x1259E
m68k_01259e:
        dbra %d0,(. + -2)
m68k_01259e_end:
.org 0x125A2
m68k_0125a2:
        clr.w (%a0)
m68k_0125a2_end:
.org 0x125A4
m68k_0125a4:
        addi.w #0x20,0xf31a:w
m68k_0125a4_end:
.org 0x125AA
m68k_0125aa:
        rts
m68k_0125aa_end:
.org 0x125AC
m68k_0125ac:
        btst.b #0x4,0xf321:w
m68k_0125ac_end:
.org 0x125B2
m68k_0125b2:
        bne.b (. + 28)
m68k_0125b2_end:
.org 0x125B4
m68k_0125b4:
        lea.l 26(%pc),%a0
m68k_0125b4_end:
.org 0x125B8
m68k_0125b8:
        move.w #0x68,%d0
m68k_0125b8_end:
.org 0x125BC
m68k_0125bc:
        move.w 0xf39a:w,%d1
m68k_0125bc_end:
.org 0x125C0
m68k_0125c0:
        lsl.w #0x3,%d1
m68k_0125c0_end:
.org 0x125C2
m68k_0125c2:
        addi.w #0xe8,%d1
m68k_0125c2_end:
.org 0x125C6
m68k_0125c6:
        clr.w %d2
m68k_0125c6_end:
.org 0x125C8
m68k_0125c8:
        jsr 0xac08:l
m68k_0125c8_end:
.org 0x125CE
m68k_0125ce:
        rts
m68k_0125ce_end:
.org 0x13D7A
m68k_013d7a:
        cmpi.w #0x9,0xf36a:w
m68k_013d7a_end:
.org 0x13D80
m68k_013d80:
        bcs.b (. + 40)
m68k_013d80_end:
.org 0x13D82
m68k_013d82:
        addq.w #0x1,0xf362:w
m68k_013d82_end:
.org 0x13D86
m68k_013d86:
        move.w #0x6c,0xf600:w
m68k_013d86_end:
.org 0x13D8C
m68k_013d8c:
        clr.l 0xf3ba:w
m68k_013d8c_end:
.org 0x13D90
m68k_013d90:
        clr.w 0xf670:w
m68k_013d90_end:
.org 0x13D94
m68k_013d94:
        move.w #0x2,0xf39a:w
m68k_013d94_end:
.org 0x13D9A
m68k_013d9a:
        jsr 0x5694:l
m68k_013d9a_end:
.org 0x13DA0
m68k_013da0:
        ori.w #0x8c0,0xf3a4:w
m68k_013da0_end:
.org 0x13DA6
m68k_013da6:
        bra.b (. + 68)
m68k_013da6_end:
.org 0x13DA8
m68k_013da8:
        lea.l 0xd100:w,%a0
m68k_013da8_end:
.org 0x13DAC
m68k_013dac:
        adda.w 0xf31a:w,%a0
m68k_013dac_end:
.org 0x13DB0
m68k_013db0:
        move.w #0xd,0x1e(%a0)
m68k_013db0_end:
.org 0x13DB6
m68k_013db6:
        move.w #0xd,(%a0)+
m68k_013db6_end:
.org 0x13DBA
m68k_013dba:
        move.w 0xf36a:w,%d0
m68k_013dba_end:
.org 0x13DBE
m68k_013dbe:
        lsl.w #0x8,%d0
m68k_013dbe_end:
.org 0x13DC0
m68k_013dc0:
        move.w #0xc934,%d1
m68k_013dc0_end:
.org 0x13DC4
m68k_013dc4:
        sub.w %d0,%d1
m68k_013dc4_end:
.org 0x13DC6
m68k_013dc6:
        move.w %d1,0x1e(%a0)
m68k_013dc6_end:
.org 0x13DCA
m68k_013dca:
        subi.w #0x80,%d1
m68k_013dca_end:
.org 0x13DCE
m68k_013dce:
        move.w %d1,(%a0)+
m68k_013dce_end:
.org 0x13DD0
m68k_013dd0:
        move.w #0xc,%d0
m68k_013dd0_end:
.org 0x13DD4
m68k_013dd4:
        move.w #0x8000,0x1e(%a0)
m68k_013dd4_end:
.org 0x13DDA
m68k_013dda:
        move.w #0x8000,(%a0)+
m68k_013dda_end:
.org 0x13DDE
m68k_013dde:
        dbra %d0,(. + -10)
m68k_013dde_end:
.org 0x13DE2
m68k_013de2:
        clr.w 0x1e(%a0)
m68k_013de2_end:
.org 0x13DE6
m68k_013de6:
        addq.w #0x1,0xf36a:w
m68k_013de6_end:
.org 0x13DEA
m68k_013dea:
        jsr 0xa158:l
m68k_013dea_end:
.org 0x13DF0
m68k_013df0:
        bsr.w (. + 6)
m68k_013df0_end:
.org 0x13DF4
m68k_013df4:
        rts
m68k_013df4_end:
.org 0x13DF6
m68k_013df6:
        lea.l 0xf500:w,%a0
m68k_013df6_end:
.org 0x13DFA
m68k_013dfa:
        lea.l 0xc800:w,%a1
m68k_013dfa_end:
.org 0x13DFE
m68k_013dfe:
        moveq #0,%d0
m68k_013dfe_end:
.org 0x13E00
m68k_013e00:
        move.w (%a0)+,%d1
m68k_013e00_end:
.org 0x13E02
m68k_013e02:
        bmi.w (. + 24)
m68k_013e02_end:
.org 0x13E06
m68k_013e06:
        btst.l #0xe,%d1
m68k_013e06_end:
.org 0x13E0A
m68k_013e0a:
        beq.b (. + -10)
m68k_013e0a_end:
.org 0x13E0C
m68k_013e0c:
        lsl.w #0x2,%d1
m68k_013e0c_end:
.org 0x13E0E
m68k_013e0e:
        add.l (%a1, %d1.w),%d0
m68k_013e0e_end:
.org 0x13E12
m68k_013e12:
        addi.l #0x64,%d0
m68k_013e12_end:
.org 0x13E18
m68k_013e18:
        bra.b (. + -24)
m68k_013e18_end:
.org 0x13E1A
m68k_013e1a:
        divu.w #0x64,%d0
m68k_013e1a_end:
.org 0x13E1E
m68k_013e1e:
        bne.w (. + 8)
m68k_013e1e_end:
.org 0x13E22
m68k_013e22:
        move.w #0x1,%d0
m68k_013e22_end:
.org 0x13E26
m68k_013e26:
        andi.l #0xffff,%d0
m68k_013e26_end:
.org 0x13E2C
m68k_013e2c:
        move.l %d0,0xf74e:w
m68k_013e2c_end:
.org 0x13E30
m68k_013e30:
        mulu.w #0xa,%d0
m68k_013e30_end:
.org 0x13E34
m68k_013e34:
        move.l %d0,0xf752:w
m68k_013e34_end:
.org 0x13E38
m68k_013e38:
        mulu.w #0xa,%d0
m68k_013e38_end:
.org 0x13E3C
m68k_013e3c:
        move.l %d0,0xf756:w
m68k_013e3c_end:
.org 0x13E40
m68k_013e40:
        rts
m68k_013e40_end:
.org 0x13E42
m68k_013e42:
        bsr.w (. + 80)
m68k_013e42_end:
.org 0x13E46
m68k_013e46:
        bsr.w (. + 294)
m68k_013e46_end:
.org 0x13E4A
m68k_013e4a:
        bsr.w (. + 9098)
m68k_013e4a_end:
.org 0x13E4E
m68k_013e4e:
        bsr.w (. + 348)
m68k_013e4e_end:
.org 0x13E52
m68k_013e52:
        btst.b #0x5,0xf602:w
m68k_013e52_end:
.org 0x13E58
m68k_013e58:
        beq.b (. + 20)
m68k_013e58_end:
.org 0x13E5A
m68k_013e5a:
        move.w #0x208,0xf612:w
m68k_013e5a_end:
.org 0x13E60
m68k_013e60:
        move.w #0x4,0xf362:w
m68k_013e60_end:
.org 0x13E66
m68k_013e66:
        bsr.w (. + 382)
m68k_013e66_end:
.org 0x13E6A
m68k_013e6a:
        bra.b (. + 32)
m68k_013e6a_end:
.org 0x13E6C
m68k_013e6c:
        btst.b #0x4,0xf602:w
m68k_013e6c_end:
.org 0x13E72
m68k_013e72:
        beq.b (. + 24)
m68k_013e72_end:
.org 0x13E74
m68k_013e74:
        move.w #0x208,0xf612:w
m68k_013e74_end:
.org 0x13E7A
m68k_013e7a:
        move.w #0x2,0xf362:w
m68k_013e7a_end:
.org 0x13E80
m68k_013e80:
        move.w #0x12,0xf36a:w
m68k_013e80_end:
.org 0x13E86
m68k_013e86:
        bsr.w (. + 8908)
m68k_013e86_end:
.org 0x13E8A
m68k_013e8a:
        jsr 0xa158:l
m68k_013e8a_end:
.org 0x13E90
m68k_013e90:
        rts
m68k_013e90_end:
.org 0x13E92
m68k_013e92:
        move.b 0xf602:w,%d0
m68k_013e92_end:
.org 0x13E96
m68k_013e96:
        andi.w #0xc,%d0
m68k_013e96_end:
.org 0x13E9A
m68k_013e9a:
        beq.b (. + 78)
m68k_013e9a_end:
.org 0x13E9C
m68k_013e9c:
        subq.w #0x1,0xf608:w
m68k_013e9c_end:
.org 0x13EA0
m68k_013ea0:
        bne.w (. + 196)
m68k_013ea0_end:
.org 0x13EA4
m68k_013ea4:
        move.w #0xc,0xf608:w
m68k_013ea4_end:
.org 0x13EAA
m68k_013eaa:
        btst.l #0x3,%d0
m68k_013eaa_end:
.org 0x13EAE
m68k_013eae:
        bne.b (. + 44)
m68k_013eae_end:
.org 0x13EB0
m68k_013eb0:
        tst.w 0xf39a:w
m68k_013eb0_end:
.org 0x13EB4
m68k_013eb4:
        beq.w (. + 176)
m68k_013eb4_end:
.org 0x13EB8
m68k_013eb8:
        move.w #0x1,%d0
m68k_013eb8_end:
.org 0x13EBC
m68k_013ebc:
        sub.w 0xf39a:w,%d0
m68k_013ebc_end:
.org 0x13EC0
m68k_013ec0:
        lsl.w #0x2,%d0
m68k_013ec0_end:
.org 0x13EC2
m68k_013ec2:
        lea.l 0xf752:w,%a0
m68k_013ec2_end:
.org 0x13EC6
m68k_013ec6:
        move.l (%a0, %d0.w),%d0
m68k_013ec6_end:
.org 0x13ECA
m68k_013eca:
        cmp.l 0xf3f8:w,%d0
m68k_013eca_end:
.org 0x13ECE
m68k_013ece:
        bhi.w (. + 150)
m68k_013ece_end:
.org 0x13ED2
m68k_013ed2:
        subq.w #0x1,0xf39a:w
m68k_013ed2_end:
.org 0x13ED6
m68k_013ed6:
        bra.w (. + 142)
m68k_013ed6_end:
.org 0x13EDA
m68k_013eda:
        cmpi.w #0x2,0xf39a:w
m68k_013eda_end:
.org 0x13EE0
m68k_013ee0:
        bcc.w (. + 132)
m68k_013ee0_end:
.org 0x13EE4
m68k_013ee4:
        addq.w #0x1,0xf39a:w
m68k_013ee4_end:
.org 0x13EE8
m68k_013ee8:
        move.b 0xf602:w,%d0
m68k_013ee8_end:
.org 0x13EEC
m68k_013eec:
        andi.b #0x3,%d0
m68k_013eec_end:
.org 0x13EF0
m68k_013ef0:
        beq.b (. + 110)
m68k_013ef0_end:
.org 0x13EF2
m68k_013ef2:
        subq.w #0x1,0xf608:w
m68k_013ef2_end:
.org 0x13EF6
m68k_013ef6:
        bne.w (. + 110)
m68k_013ef6_end:
.org 0x13EFA
m68k_013efa:
        move.w #0xc,0xf608:w
m68k_013efa_end:
.org 0x13F00
m68k_013f00:
        move.w #0x2,%d1
m68k_013f00_end:
.org 0x13F04
m68k_013f04:
        sub.w 0xf39a:w,%d1
m68k_013f04_end:
.org 0x13F08
m68k_013f08:
        lsl.w #0x2,%d1
m68k_013f08_end:
.org 0x13F0A
m68k_013f0a:
        lea.l 0xf74e:w,%a0
m68k_013f0a_end:
.org 0x13F0E
m68k_013f0e:
        move.l (%a0, %d1.w),%d2
m68k_013f0e_end:
.org 0x13F12
m68k_013f12:
        lsr.w #0x1,%d1
m68k_013f12_end:
.org 0x13F14
m68k_013f14:
        move.w 80(%pc, %d1.w),%d4
m68k_013f14_end:
.org 0x13F18
m68k_013f18:
        btst.l #0x1,%d0
m68k_013f18_end:
.org 0x13F1C
m68k_013f1c:
        bne.w (. + 44)
m68k_013f1c_end:
.org 0x13F20
m68k_013f20:
        move.l 0xf3ba:w,%d3
m68k_013f20_end:
.org 0x13F24
m68k_013f24:
        add.l %d2,%d3
m68k_013f24_end:
.org 0x13F26
m68k_013f26:
        cmp.l 0xf3f8:w,%d3
m68k_013f26_end:
.org 0x13F2A
m68k_013f2a:
        bhi.w (. + 58)
m68k_013f2a_end:
.org 0x13F2E
m68k_013f2e:
        move.w 0xf670:w,%d5
m68k_013f2e_end:
.org 0x13F32
m68k_013f32:
        add.w %d4,%d5
m68k_013f32_end:
.org 0x13F34
m68k_013f34:
        cmpi.w #0x3e8,%d5
m68k_013f34_end:
.org 0x13F38
m68k_013f38:
        bcc.w (. + 44)
m68k_013f38_end:
.org 0x13F3C
m68k_013f3c:
        move.l %d3,0xf3ba:w
m68k_013f3c_end:
.org 0x13F40
m68k_013f40:
        move.w %d5,0xf670:w
m68k_013f40_end:
.org 0x13F44
m68k_013f44:
        bra.w (. + 32)
m68k_013f44_end:
.org 0x13F48
m68k_013f48:
        move.l 0xf3ba:w,%d3
m68k_013f48_end:
.org 0x13F4C
m68k_013f4c:
        sub.l %d2,%d3
m68k_013f4c_end:
.org 0x13F4E
m68k_013f4e:
        bcs.w (. + 22)
m68k_013f4e_end:
.org 0x13F52
m68k_013f52:
        move.l %d3,0xf3ba:w
m68k_013f52_end:
.org 0x13F56
m68k_013f56:
        sub.w %d4,0xf670:w
m68k_013f56_end:
.org 0x13F5A
m68k_013f5a:
        bra.w (. + 10)
m68k_013f5a_end:
.org 0x13F5E
m68k_013f5e:
        move.w #0x1,0xf608:w
m68k_013f5e_end:
.org 0x13F64
m68k_013f64:
        rts
m68k_013f64_end:
.org 0x13F6C
m68k_013f6c:
        lea.l 0xd100:w,%a0
m68k_013f6c_end:
.org 0x13F70
m68k_013f70:
        adda.w 0xf31a:w,%a0
m68k_013f70_end:
.org 0x13F74
m68k_013f74:
        move.l 0xf3ba:w,%d0
m68k_013f74_end:
.org 0x13F78
m68k_013f78:
        move.w #0xc386,%d1
m68k_013f78_end:
.org 0x13F7C
m68k_013f7c:
        move.w #0xc001,%d2
m68k_013f7c_end:
.org 0x13F80
m68k_013f80:
        lea.l 0xd300:w,%a6
m68k_013f80_end:
.org 0x13F84
m68k_013f84:
        jsr 0x1270a:l
m68k_013f84_end:
.org 0x13F8A
m68k_013f8a:
        move.w #0x6,(%a0)+
m68k_013f8a_end:
.org 0x13F8E
m68k_013f8e:
        move.w #0xc6ac,(%a0)+
m68k_013f8e_end:
.org 0x13F92
m68k_013f92:
        lea.l 0xd300:w,%a1
m68k_013f92_end:
.org 0x13F96
m68k_013f96:
        move.w #0x5,%d0
m68k_013f96_end:
.org 0x13F9A
m68k_013f9a:
        move.w (%a1)+,(%a0)+
m68k_013f9a_end:
.org 0x13F9C
m68k_013f9c:
        dbra %d0,(. + -2)
m68k_013f9c_end:
.org 0x13FA0
m68k_013fa0:
        clr.w (%a0)
m68k_013fa0_end:
.org 0x13FA2
m68k_013fa2:
        addi.w #0x10,0xf31a:w
m68k_013fa2_end:
.org 0x13FA8
m68k_013fa8:
        rts
m68k_013fa8_end:
.org 0x13FAA
m68k_013faa:
        move.w 0xf602:w,%d0
m68k_013faa_end:
.org 0x13FAE
m68k_013fae:
        andi.w #0x30,%d0
m68k_013fae_end:
.org 0x13FB2
m68k_013fb2:
        bne.w (. + 40)
m68k_013fb2_end:
.org 0x13FB6
m68k_013fb6:
        btst.b #0x3,0xf321:w
m68k_013fb6_end:
.org 0x13FBC
m68k_013fbc:
        bne.w (. + 30)
m68k_013fbc_end:
.org 0x13FC0
m68k_013fc0:
        lea.l 26(%pc),%a0
m68k_013fc0_end:
.org 0x13FC4
m68k_013fc4:
        move.w #0x58,%d0
m68k_013fc4_end:
.org 0x13FC8
m68k_013fc8:
        move.w 0xf39a:w,%d1
m68k_013fc8_end:
.org 0x13FCC
m68k_013fcc:
        lsl.w #0x3,%d1
m68k_013fcc_end:
.org 0x13FCE
m68k_013fce:
        addi.w #0xa8,%d1
m68k_013fce_end:
.org 0x13FD2
m68k_013fd2:
        clr.w %d2
m68k_013fd2_end:
.org 0x13FD4
m68k_013fd4:
        jsr 0xac08:l
m68k_013fd4_end:
.org 0x13FDA
m68k_013fda:
        rts
m68k_013fda_end:
.org 0x13FE4
m68k_013fe4:
        lea.l 0xf500:w,%a0
m68k_013fe4_end:
.org 0x13FE8
m68k_013fe8:
        lea.l 0xc400:w,%a1
m68k_013fe8_end:
.org 0x13FEC
m68k_013fec:
        clr.l %d0
m68k_013fec_end:
.org 0x13FEE
m68k_013fee:
        clr.w %d1
m68k_013fee_end:
.org 0x13FF0
m68k_013ff0:
        move.w 0xf364:w,%d2
m68k_013ff0_end:
.org 0x13FF4
m68k_013ff4:
        lsl.w #0x2,%d2
m68k_013ff4_end:
.org 0x13FF6
m68k_013ff6:
        lea.l 0xd4ac6:l,%a5
m68k_013ff6_end:
.org 0x13FFC
m68k_013ffc:
        move.w 0x2(%a5, %d2.w),%d3
m68k_013ffc_end:
.org 0x14000
m68k_014000:
        andi.w #0xfff0,%d3
m68k_014000_end:
.org 0x14004
m68k_014004:
        move.w %d3,0xff3822:l
m68k_014004_end:
.org 0x1400A
m68k_01400a:
        lsl.w #0x4,%d3
m68k_01400a_end:
.org 0x1400C
m68k_01400c:
        andi.w #0xff00,%d3
m68k_01400c_end:
.org 0x14010
m68k_014010:
        move.w (%a5, %d2.w),%d4
m68k_014010_end:
.org 0x14014
m68k_014014:
        andi.w #0xfff0,%d4
m68k_014014_end:
.org 0x14018
m68k_014018:
        move.w %d4,0xff3824:l
m68k_014018_end:
.org 0x1401E
m68k_01401e:
        lsr.w #0x4,%d4
m68k_01401e_end:
.org 0x14020
m68k_014020:
        or.w %d3,%d4
m68k_014020_end:
.org 0x14022
m68k_014022:
        move.w %d4,0xff3828:l
m68k_014022_end:
.org 0x14028
m68k_014028:
        move.w (%a0)+,%d2
m68k_014028_end:
.org 0x1402A
m68k_01402a:
        bmi.b (. + 24)
m68k_01402a_end:
.org 0x1402C
m68k_01402c:
        cmpi.w #0x4000,%d2
m68k_01402c_end:
.org 0x14030
m68k_014030:
        bcs.b (. + -8)
m68k_014030_end:
.org 0x14032
m68k_014032:
        addq.w #0x1,%d1
m68k_014032_end:
.org 0x14034
m68k_014034:
        andi.w #0xff,%d2
m68k_014034_end:
.org 0x14038
m68k_014038:
        clr.w %d3
m68k_014038_end:
.org 0x1403A
m68k_01403a:
        move.b (%a1, %d2.w),%d3
m68k_01403a_end:
.org 0x1403E
m68k_01403e:
        add.w %d3,%d0
m68k_01403e_end:
.org 0x14040
m68k_014040:
        bra.b (. + -24)
m68k_014040_end:
.org 0x14042
m68k_014042:
        move.w %d1,0xff382a:l
m68k_014042_end:
.org 0x14048
m68k_014048:
        divu.w %d1,%d0
m68k_014048_end:
.org 0x1404A
m68k_01404a:
        move.w %d0,0xf672:w
m68k_01404a_end:
.org 0x1404E
m68k_01404e:
        rts
m68k_01404e_end:
.org 0x14050
m68k_014050:
        btst.b #0x6,0xf3a4:w
m68k_014050_end:
.org 0x14056
m68k_014056:
        beq.b (. + 78)
m68k_014056_end:
.org 0x14058
m68k_014058:
        jsr 0xa158:l
m68k_014058_end:
.org 0x1405E
m68k_01405e:
        btst.b #0x5,0xf603:w
m68k_01405e_end:
.org 0x14064
m68k_014064:
        beq.b (. + 34)
m68k_014064_end:
.org 0x14066
m68k_014066:
        move.w 0xf612:w,0xf3c2:w
m68k_014066_end:
.org 0x1406C
m68k_01406c:
        move.w 0xf362:w,0xf3c4:w
m68k_01406c_end:
.org 0x14072
m68k_014072:
        move.w #0x208,0xf612:w
m68k_014072_end:
.org 0x14078
m68k_014078:
        move.w #0x13,0xf362:w
m68k_014078_end:
.org 0x1407E
m68k_01407e:
        clr.w 0xf36a:w
m68k_01407e_end:
.org 0x14082
m68k_014082:
        bra.w (. + 130)
m68k_014082_end:
.org 0x14086
m68k_014086:
        btst.b #0x4,0xf603:w
m68k_014086_end:
.org 0x1408C
m68k_01408c:
        beq.b (. + 120)
m68k_01408c_end:
.org 0x1408E
m68k_01408e:
        move.w #0x208,0xf612:w
m68k_01408e_end:
.org 0x14094
m68k_014094:
        move.w #0x2,0xf362:w
m68k_014094_end:
.org 0x1409A
m68k_01409a:
        move.w #0x12,0xf36a:w
m68k_01409a_end:
.org 0x140A0
m68k_0140a0:
        bra.w (. + 100)
m68k_0140a0_end:
.org 0x140A4
m68k_0140a4:
        jsr 0x1264:l
m68k_0140a4_end:
.org 0x140AA
m68k_0140aa:
        bsr.w (. + 118)
m68k_0140aa_end:
.org 0x140AE
m68k_0140ae:
        bsr.w (. + 188)
m68k_0140ae_end:
.org 0x140B2
m68k_0140b2:
        bsr.w (. + 690)
m68k_0140b2_end:
.org 0x140B6
m68k_0140b6:
        btst.b #0x4,0xf603:w
m68k_0140b6_end:
.org 0x140BC
m68k_0140bc:
        beq.b (. + 8)
m68k_0140bc_end:
.org 0x140BE
m68k_0140be:
        bsr.w (. + 530)
m68k_0140be_end:
.org 0x140C2
m68k_0140c2:
        bra.b (. + 66)
m68k_0140c2_end:
.org 0x140C4
m68k_0140c4:
        btst.b #0x5,0xf603:w
m68k_0140c4_end:
.org 0x140CA
m68k_0140ca:
        beq.b (. + 58)
m68k_0140ca_end:
.org 0x140CC
m68k_0140cc:
        tst.w 0xff3820:l
m68k_0140cc_end:
.org 0x140D2
m68k_0140d2:
        beq.b (. + 50)
m68k_0140d2_end:
.org 0x140D4
m68k_0140d4:
        move.w #0x208,0xf612:w
m68k_0140d4_end:
.org 0x140DA
m68k_0140da:
        move.w #0x4,0xf362:w
m68k_0140da_end:
.org 0x140E0
m68k_0140e0:
        lea.l 0xff3800:l,%a0
m68k_0140e0_end:
.org 0x140E6
m68k_0140e6:
        move.w 0xff3820:l,%d0
m68k_0140e6_end:
.org 0x140EC
m68k_0140ec:
        clr.b (%a0, %d0.w)
m68k_0140ec_end:
.org 0x140F0
m68k_0140f0:
        move.w 0xff3822:l,0xf35e:w
m68k_0140f0_end:
.org 0x140F8
m68k_0140f8:
        move.w 0xff3824:l,0xf360:w
m68k_0140f8_end:
.org 0x14100
m68k_014100:
        bsr.w (. + 6)
m68k_014100_end:
.org 0x14104
m68k_014104:
        rts
m68k_014104_end:
.org 0x14106
m68k_014106:
        lea.l 0x9f00:w,%a0
m68k_014106_end:
.org 0x1410A
m68k_01410a:
        tst.w (%a0)+
m68k_01410a_end:
.org 0x1410C
m68k_01410c:
        bpl.b (. + -2)
m68k_01410c_end:
.org 0x1410E
m68k_01410e:
        move.w 0xf35e:w,-0x2(%a0)
m68k_01410e_end:
.org 0x14114
m68k_014114:
        move.w 0xf360:w,(%a0)
m68k_014114_end:
.org 0x14118
m68k_014118:
        move.w #0xffff,0x2(%a0)
m68k_014118_end:
.org 0x1411E
m68k_01411e:
        rts
m68k_01411e_end:
.org 0x14120
m68k_014120:
        btst.b #0x2,0xf321:w
m68k_014120_end:
.org 0x14126
m68k_014126:
        bne.b (. + 40)
m68k_014126_end:
.org 0x14128
m68k_014128:
        lea.l 38(%pc),%a0
m68k_014128_end:
.org 0x1412C
m68k_01412c:
        nop
m68k_01412c_end:
.org 0x1412E
m68k_01412e:
        move.w 0xff3822:l,%d0
m68k_01412e_end:
.org 0x14134
m68k_014134:
        move.w 0xff3824:l,%d1
m68k_014134_end:
.org 0x1413A
m68k_01413a:
        clr.w %d2
m68k_01413a_end:
.org 0x1413C
m68k_01413c:
        move.w 0xf314:w,0xf60a:w
m68k_01413c_end:
.org 0x14142
m68k_014142:
        move.w 0xf318:w,0xf60e:w
m68k_014142_end:
.org 0x14148
m68k_014148:
        jsr 0xac10:l
m68k_014148_end:
.org 0x1414E
m68k_01414e:
        rts
m68k_01414e_end:
.org 0x1416A
m68k_01416a:
        move.w 0xf602:w,%d4
m68k_01416a_end:
.org 0x1416E
m68k_01416e:
        btst.l #0x0,%d4
m68k_01416e_end:
.org 0x14172
m68k_014172:
        beq.b (. + 60)
m68k_014172_end:
.org 0x14174
m68k_014174:
        move.w 0xff3822:l,%d0
m68k_014174_end:
.org 0x1417A
m68k_01417a:
        beq.w (. + 280)
m68k_01417a_end:
.org 0x1417E
m68k_01417e:
        subi.w #0x10,%d0
m68k_01417e_end:
.org 0x14182
m68k_014182:
        move.w 0xff3824:l,%d1
m68k_014182_end:
.org 0x14188
m68k_014188:
        bsr.w (. + 322)
m68k_014188_end:
.org 0x1418C
m68k_01418c:
        tst.w %d3
m68k_01418c_end:
.org 0x1418E
m68k_01418e:
        bmi.w (. + 260)
m68k_01418e_end:
.org 0x14192
m68k_014192:
        move.w 0xf674:w,%d4
m68k_014192_end:
.org 0x14196
m68k_014196:
        sub.w %d3,%d4
m68k_014196_end:
.org 0x14198
m68k_014198:
        bcs.w (. + 250)
m68k_014198_end:
.org 0x1419C
m68k_01419c:
        move.w %d4,0xf674:w
m68k_01419c_end:
.org 0x141A0
m68k_0141a0:
        move.w %d0,0xff3822:l
m68k_0141a0_end:
.org 0x141A6
m68k_0141a6:
        move.w #0x1,%d1
m68k_0141a6_end:
.org 0x141AA
m68k_0141aa:
        bra.w (. + 210)
m68k_0141aa_end:
.org 0x141AE
m68k_0141ae:
        btst.l #0x3,%d4
m68k_0141ae_end:
.org 0x141B2
m68k_0141b2:
        beq.b (. + 68)
m68k_0141b2_end:
.org 0x141B4
m68k_0141b4:
        cmpi.w #0x450,0xff3824:l
m68k_0141b4_end:
.org 0x141BC
m68k_0141bc:
        bcc.w (. + 214)
m68k_0141bc_end:
.org 0x141C0
m68k_0141c0:
        move.w 0xff3822:l,%d0
m68k_0141c0_end:
.org 0x141C6
m68k_0141c6:
        move.w 0xff3824:l,%d1
m68k_0141c6_end:
.org 0x141CC
m68k_0141cc:
        addi.w #0x10,%d1
m68k_0141cc_end:
.org 0x141D0
m68k_0141d0:
        bsr.w (. + 250)
m68k_0141d0_end:
.org 0x141D4
m68k_0141d4:
        tst.w %d3
m68k_0141d4_end:
.org 0x141D6
m68k_0141d6:
        bmi.w (. + 188)
m68k_0141d6_end:
.org 0x141DA
m68k_0141da:
        move.w 0xf674:w,%d4
m68k_0141da_end:
.org 0x141DE
m68k_0141de:
        sub.w %d3,%d4
m68k_0141de_end:
.org 0x141E0
m68k_0141e0:
        bcs.w (. + 178)
m68k_0141e0_end:
.org 0x141E4
m68k_0141e4:
        move.w %d4,0xf674:w
m68k_0141e4_end:
.org 0x141E8
m68k_0141e8:
        move.w %d1,0xff3824:l
m68k_0141e8_end:
.org 0x141EE
m68k_0141ee:
        move.w #0x2,%d1
m68k_0141ee_end:
.org 0x141F2
m68k_0141f2:
        bra.w (. + 138)
m68k_0141f2_end:
.org 0x141F6
m68k_0141f6:
        btst.l #0x1,%d4
m68k_0141f6_end:
.org 0x141FA
m68k_0141fa:
        beq.b (. + 68)
m68k_0141fa_end:
.org 0x141FC
m68k_0141fc:
        cmpi.w #0x470,0xff3822:l
m68k_0141fc_end:
.org 0x14204
m68k_014204:
        bcc.w (. + 142)
m68k_014204_end:
.org 0x14208
m68k_014208:
        move.w 0xff3822:l,%d0
m68k_014208_end:
.org 0x1420E
m68k_01420e:
        addi.w #0x10,%d0
m68k_01420e_end:
.org 0x14212
m68k_014212:
        move.w 0xff3824:l,%d1
m68k_014212_end:
.org 0x14218
m68k_014218:
        bsr.w (. + 178)
m68k_014218_end:
.org 0x1421C
m68k_01421c:
        tst.w %d3
m68k_01421c_end:
.org 0x1421E
m68k_01421e:
        bmi.w (. + 116)
m68k_01421e_end:
.org 0x14222
m68k_014222:
        move.w 0xf674:w,%d4
m68k_014222_end:
.org 0x14226
m68k_014226:
        sub.w %d3,%d4
m68k_014226_end:
.org 0x14228
m68k_014228:
        bcs.w (. + 106)
m68k_014228_end:
.org 0x1422C
m68k_01422c:
        move.w %d4,0xf674:w
m68k_01422c_end:
.org 0x14230
m68k_014230:
        move.w %d0,0xff3822:l
m68k_014230_end:
.org 0x14236
m68k_014236:
        move.w #0x3,%d1
m68k_014236_end:
.org 0x1423A
m68k_01423a:
        bra.w (. + 66)
m68k_01423a_end:
.org 0x1423E
m68k_01423e:
        btst.l #0x2,%d4
m68k_01423e_end:
.org 0x14242
m68k_014242:
        beq.w (. + 80)
m68k_014242_end:
.org 0x14246
m68k_014246:
        move.w 0xff3824:l,%d1
m68k_014246_end:
.org 0x1424C
m68k_01424c:
        beq.w (. + 70)
m68k_01424c_end:
.org 0x14250
m68k_014250:
        subi.w #0x10,%d1
m68k_014250_end:
.org 0x14254
m68k_014254:
        move.w 0xff3822:l,%d0
m68k_014254_end:
.org 0x1425A
m68k_01425a:
        bsr.w (. + 112)
m68k_01425a_end:
.org 0x1425E
m68k_01425e:
        tst.w %d3
m68k_01425e_end:
.org 0x14260
m68k_014260:
        bmi.w (. + 50)
m68k_014260_end:
.org 0x14264
m68k_014264:
        move.w 0xf674:w,%d4
m68k_014264_end:
.org 0x14268
m68k_014268:
        sub.w %d3,%d4
m68k_014268_end:
.org 0x1426A
m68k_01426a:
        bcs.w (. + 40)
m68k_01426a_end:
.org 0x1426E
m68k_01426e:
        move.w %d4,0xf674:w
m68k_01426e_end:
.org 0x14272
m68k_014272:
        move.w %d1,0xff3824:l
m68k_014272_end:
.org 0x14278
m68k_014278:
        move.w #0x4,%d1
m68k_014278_end:
.org 0x1427C
m68k_01427c:
        lea.l 0xff3800:l,%a0
m68k_01427c_end:
.org 0x14282
m68k_014282:
        move.w 0xff3820:l,%d0
m68k_014282_end:
.org 0x14288
m68k_014288:
        move.b %d1,(%a0, %d0.w)
m68k_014288_end:
.org 0x1428C
m68k_01428c:
        addq.w #0x1,0xff3820:l
m68k_01428c_end:
.org 0x14292
m68k_014292:
        rts
m68k_014292_end:
.org 0x142CA
m68k_0142ca:
        bsr.b (. + -54)
m68k_0142ca_end:
.org 0x142CC
m68k_0142cc:
        tst.w %d3
m68k_0142cc_end:
.org 0x142CE
m68k_0142ce:
        rts
m68k_0142ce_end:
.org 0x142D0
m68k_0142d0:
        tst.w 0xff3820:l
m68k_0142d0_end:
.org 0x142D6
m68k_0142d6:
        beq.b (. + 56)
m68k_0142d6_end:
.org 0x142D8
m68k_0142d8:
        move.w 0xff3822:l,%d0
m68k_0142d8_end:
.org 0x142DE
m68k_0142de:
        move.w 0xff3824:l,%d1
m68k_0142de_end:
.org 0x142E4
m68k_0142e4:
        bsr.b (. + -80)
m68k_0142e4_end:
.org 0x142E6
m68k_0142e6:
        add.w %d3,0xf674:w
m68k_0142e6_end:
.org 0x142EA
m68k_0142ea:
        lea.l 0xff3800:l,%a0
m68k_0142ea_end:
.org 0x142F0
m68k_0142f0:
        subq.w #0x1,0xff3820:l
m68k_0142f0_end:
.org 0x142F6
m68k_0142f6:
        move.w 0xff3820:l,%d0
m68k_0142f6_end:
.org 0x142FC
m68k_0142fc:
        clr.w %d1
m68k_0142fc_end:
.org 0x142FE
m68k_0142fe:
        move.b (%a0, %d0.w),%d1
m68k_0142fe_end:
.org 0x14302
m68k_014302:
        lsl.w #0x1,%d1
m68k_014302_end:
.org 0x14304
m68k_014304:
        move.w 44(%pc, %d1.w),%d1
m68k_014304_end:
.org 0x14308
m68k_014308:
        jsr 50(%pc, %d1.w)
m68k_014308_end:
.org 0x1430C
m68k_01430c:
        bra.b (. + 38)
m68k_01430c_end:
.org 0x1430E
m68k_01430e:
        move.w #0x208,0xf612:w
m68k_01430e_end:
.org 0x14314
m68k_014314:
        move.w #0x2,0xf362:w
m68k_014314_end:
.org 0x1431A
m68k_01431a:
        move.w #0x12,0xf36a:w
m68k_01431a_end:
.org 0x14320
m68k_014320:
        tst.w 0xf65a:w
m68k_014320_end:
.org 0x14324
m68k_014324:
        bne.b (. + 14)
m68k_014324_end:
.org 0x14326
m68k_014326:
        jsr 0x5694:l
m68k_014326_end:
.org 0x1432C
m68k_01432c:
        jsr 0x5abc:l
m68k_01432c_end:
.org 0x14332
m68k_014332:
        rts
m68k_014332_end:
.org 0x14364
m68k_014364:
        move.w 0xff3822:l,%d0
m68k_014364_end:
.org 0x1436A
m68k_01436a:
        sub.w 0xf314:w,%d0
m68k_01436a_end:
.org 0x1436E
m68k_01436e:
        bcs.b (. + 8)
m68k_01436e_end:
.org 0x14370
m68k_014370:
        cmpi.w #0x60,%d0
m68k_014370_end:
.org 0x14374
m68k_014374:
        bcc.b (. + 30)
m68k_014374_end:
.org 0x14376
m68k_014376:
        move.w 0xf314:w,%d0
m68k_014376_end:
.org 0x1437A
m68k_01437a:
        beq.b (. + 62)
m68k_01437a_end:
.org 0x1437C
m68k_01437c:
        subq.w #0x1,%d0
m68k_01437c_end:
.org 0x1437E
m68k_01437e:
        bcc.b (. + 4)
m68k_01437e_end:
.org 0x14380
m68k_014380:
        clr.w %d0
m68k_014380_end:
.org 0x14382
m68k_014382:
        move.w %d0,0xf314:w
m68k_014382_end:
.org 0x14386
m68k_014386:
        movea.w %d0,%a5
m68k_014386_end:
.org 0x14388
m68k_014388:
        jsr 0xa0cc:l
m68k_014388_end:
.org 0x1438E
m68k_01438e:
        bra.w (. + 42)
m68k_01438e_end:
.org 0x14392
m68k_014392:
        cmpi.w #0x80,%d0
m68k_014392_end:
.org 0x14396
m68k_014396:
        bcs.b (. + 34)
m68k_014396_end:
.org 0x14398
m68k_014398:
        move.w 0xf314:w,%d0
m68k_014398_end:
.org 0x1439C
m68k_01439c:
        addq.w #0x1,%d0
m68k_01439c_end:
.org 0x1439E
m68k_01439e:
        cmpi.w #0x3a0,%d0
m68k_01439e_end:
.org 0x143A2
m68k_0143a2:
        bls.b (. + 6)
m68k_0143a2_end:
.org 0x143A4
m68k_0143a4:
        move.w #0x3a0,%d0
m68k_0143a4_end:
.org 0x143A8
m68k_0143a8:
        move.w %d0,0xf314:w
m68k_0143a8_end:
.org 0x143AC
m68k_0143ac:
        addi.w #0xe0,%d0
m68k_0143ac_end:
.org 0x143B0
m68k_0143b0:
        movea.w %d0,%a5
m68k_0143b0_end:
.org 0x143B2
m68k_0143b2:
        jsr 0xa0cc:l
m68k_0143b2_end:
.org 0x143B8
m68k_0143b8:
        move.w 0xff3824:l,%d0
m68k_0143b8_end:
.org 0x143BE
m68k_0143be:
        sub.w 0xf318:w,%d0
m68k_0143be_end:
.org 0x143C2
m68k_0143c2:
        bcs.b (. + 8)
m68k_0143c2_end:
.org 0x143C4
m68k_0143c4:
        cmpi.w #0x60,%d0
m68k_0143c4_end:
.org 0x143C8
m68k_0143c8:
        bhi.b (. + 28)
m68k_0143c8_end:
.org 0x143CA
m68k_0143ca:
        move.w 0xf318:w,%d0
m68k_0143ca_end:
.org 0x143CE
m68k_0143ce:
        subq.w #0x1,%d0
m68k_0143ce_end:
.org 0x143D0
m68k_0143d0:
        bcc.b (. + 4)
m68k_0143d0_end:
.org 0x143D2
m68k_0143d2:
        clr.w %d0
m68k_0143d2_end:
.org 0x143D4
m68k_0143d4:
        move.w %d0,0xf318:w
m68k_0143d4_end:
.org 0x143D8
m68k_0143d8:
        movea.w %d0,%a5
m68k_0143d8_end:
.org 0x143DA
m68k_0143da:
        jsr 0xa10c:l
m68k_0143da_end:
.org 0x143E0
m68k_0143e0:
        bra.w (. + 44)
m68k_0143e0_end:
.org 0x143E4
m68k_0143e4:
        cmpi.w #0xe0,%d0
m68k_0143e4_end:
.org 0x143E8
m68k_0143e8:
        bcs.b (. + 36)
m68k_0143e8_end:
.org 0x143EA
m68k_0143ea:
        move.w 0xf318:w,%d0
m68k_0143ea_end:
.org 0x143EE
m68k_0143ee:
        addi.w #0x1,%d0
m68k_0143ee_end:
.org 0x143F2
m68k_0143f2:
        cmpi.w #0x340,%d0
m68k_0143f2_end:
.org 0x143F6
m68k_0143f6:
        bls.b (. + 6)
m68k_0143f6_end:
.org 0x143F8
m68k_0143f8:
        move.w #0x340,%d0
m68k_0143f8_end:
.org 0x143FC
m68k_0143fc:
        move.w %d0,0xf318:w
m68k_0143fc_end:
.org 0x14400
m68k_014400:
        addi.w #0x140,%d0
m68k_014400_end:
.org 0x14404
m68k_014404:
        movea.w %d0,%a5
m68k_014404_end:
.org 0x14406
m68k_014406:
        jsr 0xa10c:l
m68k_014406_end:
.org 0x1440C
m68k_01440c:
        rts
m68k_01440c_end:
.org 0x1440E
m68k_01440e:
        btst.b #0x3,0xf3a4:w
m68k_01440e_end:
.org 0x14414
m68k_014414:
        bne.b (. + 54)
m68k_014414_end:
.org 0x14416
m68k_014416:
        bsr.w (. + 7766)
m68k_014416_end:
.org 0x1441A
m68k_01441a:
        cmpi.w #0x2,0xf36c:w
m68k_01441a_end:
.org 0x14420
m68k_014420:
        bne.w (. + 108)
m68k_014420_end:
.org 0x14424
m68k_014424:
        movea.l 0xff382c:l,%a0
m68k_014424_end:
.org 0x1442A
m68k_01442a:
        move.b 0x4(%a0),%d0
m68k_01442a_end:
.org 0x1442E
m68k_01442e:
        cmp.b 0xf377:w,%d0
m68k_01442e_end:
.org 0x14432
m68k_014432:
        bne.w (. + 90)
m68k_014432_end:
.org 0x14436
m68k_014436:
        move.b (%a0),%d0
m68k_014436_end:
.org 0x14438
m68k_014438:
        andi.w #0x7f,%d0
m68k_014438_end:
.org 0x1443C
m68k_01443c:
        cmpi.w #0x10,%d0
m68k_01443c_end:
.org 0x14440
m68k_014440:
        bcc.w (. + 76)
m68k_014440_end:
.org 0x14444
m68k_014444:
        bsr.w (. + 80)
m68k_014444_end:
.org 0x14448
m68k_014448:
        bra.b (. + 68)
m68k_014448_end:
.org 0x1444A
m68k_01444a:
        addq.w #0x1,0xf362:w
m68k_01444a_end:
.org 0x1444E
m68k_01444e:
        move.w #0x8,0xcfd2:w
m68k_01444e_end:
.org 0x14454
m68k_014454:
        cmpi.w #0x2,0xf36c:w
m68k_014454_end:
.org 0x1445A
m68k_01445a:
        bne.w (. + 50)
m68k_01445a_end:
.org 0x1445E
m68k_01445e:
        movea.l 0xff382c:l,%a0
m68k_01445e_end:
.org 0x14464
m68k_014464:
        move.b 0x4(%a0),%d0
m68k_014464_end:
.org 0x14468
m68k_014468:
        cmp.b 0xf377:w,%d0
m68k_014468_end:
.org 0x1446C
m68k_01446c:
        bne.w (. + 32)
m68k_01446c_end:
.org 0x14470
m68k_014470:
        move.b (%a0),%d0
m68k_014470_end:
.org 0x14472
m68k_014472:
        andi.w #0x7f,%d0
m68k_014472_end:
.org 0x14476
m68k_014476:
        cmpi.w #0x10,%d0
m68k_014476_end:
.org 0x1447A
m68k_01447a:
        bcc.w (. + 18)
m68k_01447a_end:
.org 0x1447E
m68k_01447e:
        bsr.w (. + 246)
m68k_01447e_end:
.org 0x14482
m68k_014482:
        move.w #0x3,%d0
m68k_014482_end:
.org 0x14486
m68k_014486:
        jsr 0x676f2:l
m68k_014486_end:
.org 0x1448C
m68k_01448c:
        jsr 0xa158:l
m68k_01448c_end:
.org 0x14492
m68k_014492:
        rts
m68k_014492_end:
.org 0x14494
m68k_014494:
        lea.l 0xd100:w,%a0
m68k_014494_end:
.org 0x14498
m68k_014498:
        adda.w 0xf31a:w,%a0
m68k_014498_end:
.org 0x1449C
m68k_01449c:
        move.w #0x6,(%a0)+
m68k_01449c_end:
.org 0x144A0
m68k_0144a0:
        move.w #0xc322,(%a0)+
m68k_0144a0_end:
.org 0x144A4
m68k_0144a4:
        move.w #0xc380,(%a0)+
m68k_0144a4_end:
.org 0x144A8
m68k_0144a8:
        move.w #0xc381,(%a0)+
m68k_0144a8_end:
.org 0x144AC
m68k_0144ac:
        move.w #0xc381,(%a0)+
m68k_0144ac_end:
.org 0x144B0
m68k_0144b0:
        move.w #0xc381,(%a0)+
m68k_0144b0_end:
.org 0x144B4
m68k_0144b4:
        move.w #0xc381,(%a0)+
m68k_0144b4_end:
.org 0x144B8
m68k_0144b8:
        move.w #0xcb80,(%a0)+
m68k_0144b8_end:
.org 0x144BC
m68k_0144bc:
        lea.l 0xff3930:l,%a1
m68k_0144bc_end:
.org 0x144C2
m68k_0144c2:
        move.w #0xc3a2,%d2
m68k_0144c2_end:
.org 0x144C6
m68k_0144c6:
        move.w #0x6,0x10(%a0)
m68k_0144c6_end:
.org 0x144CC
m68k_0144cc:
        move.w #0x6,(%a0)+
m68k_0144cc_end:
.org 0x144D0
m68k_0144d0:
        move.w %d2,(%a0)
m68k_0144d0_end:
.org 0x144D2
m68k_0144d2:
        addi.w #0x80,%d2
m68k_0144d2_end:
.org 0x144D6
m68k_0144d6:
        move.w %d2,0x10(%a0)
m68k_0144d6_end:
.org 0x144DA
m68k_0144da:
        addi.w #0x80,%d2
m68k_0144da_end:
.org 0x144DE
m68k_0144de:
        addq.w #0x2,%a0
m68k_0144de_end:
.org 0x144E0
m68k_0144e0:
        move.w #0xc382,0x10(%a0)
m68k_0144e0_end:
.org 0x144E6
m68k_0144e6:
        move.w #0xc382,(%a0)+
m68k_0144e6_end:
.org 0x144EA
m68k_0144ea:
        clr.w %d0
m68k_0144ea_end:
.org 0x144EC
m68k_0144ec:
        move.b (%a1)+,%d0
m68k_0144ec_end:
.org 0x144EE
m68k_0144ee:
        lsl.w #0x3,%d0
m68k_0144ee_end:
.org 0x144F0
m68k_0144f0:
        addi.w #0xc019,%d0
m68k_0144f0_end:
.org 0x144F4
m68k_0144f4:
        move.w #0x3,%d1
m68k_0144f4_end:
.org 0x144F8
m68k_0144f8:
        bsr.w (. + 106)
m68k_0144f8_end:
.org 0x144FC
m68k_0144fc:
        move.w #0xcb82,0x10(%a0)
m68k_0144fc_end:
.org 0x14502
m68k_014502:
        move.w #0xcb82,(%a0)+
m68k_014502_end:
.org 0x14506
m68k_014506:
        adda.w #0x10,%a0
m68k_014506_end:
.org 0x1450A
m68k_01450a:
        addi.w #0x10,0xf31a:w
m68k_01450a_end:
.org 0x14510
m68k_014510:
        tst.b (%a1)
m68k_014510_end:
.org 0x14512
m68k_014512:
        bmi.b (. + 40)
m68k_014512_end:
.org 0x14514
m68k_014514:
        move.w #0x6,(%a0)+
m68k_014514_end:
.org 0x14518
m68k_014518:
        move.w %d2,(%a0)+
m68k_014518_end:
.org 0x1451A
m68k_01451a:
        addi.w #0x80,%d2
m68k_01451a_end:
.org 0x1451E
m68k_01451e:
        move.w #0xc382,(%a0)+
m68k_01451e_end:
.org 0x14522
m68k_014522:
        move.w #0x3,%d0
m68k_014522_end:
.org 0x14526
m68k_014526:
        move.w #0xc001,(%a0)+
m68k_014526_end:
.org 0x1452A
m68k_01452a:
        dbra %d0,(. + -4)
m68k_01452a_end:
.org 0x1452E
m68k_01452e:
        move.w #0xcb82,(%a0)+
m68k_01452e_end:
.org 0x14532
m68k_014532:
        addi.w #0x10,0xf31a:w
m68k_014532_end:
.org 0x14538
m68k_014538:
        bra.b (. + -114)
m68k_014538_end:
.org 0x1453A
m68k_01453a:
        move.w #0x6,(%a0)+
m68k_01453a_end:
.org 0x1453E
m68k_01453e:
        move.w %d2,(%a0)+
m68k_01453e_end:
.org 0x14540
m68k_014540:
        move.w #0xd380,(%a0)+
m68k_014540_end:
.org 0x14544
m68k_014544:
        move.w #0xd381,(%a0)+
m68k_014544_end:
.org 0x14548
m68k_014548:
        move.w #0xd381,(%a0)+
m68k_014548_end:
.org 0x1454C
m68k_01454c:
        move.w #0xd381,(%a0)+
m68k_01454c_end:
.org 0x14550
m68k_014550:
        move.w #0xd381,(%a0)+
m68k_014550_end:
.org 0x14554
m68k_014554:
        move.w #0xdb80,(%a0)+
m68k_014554_end:
.org 0x14558
m68k_014558:
        clr.w (%a0)
m68k_014558_end:
.org 0x1455A
m68k_01455a:
        addi.w #0x20,0xf31a:w
m68k_01455a_end:
.org 0x14560
m68k_014560:
        rts
m68k_014560_end:
.org 0x14562
m68k_014562:
        move.w %d0,(%a0)
m68k_014562_end:
.org 0x14564
m68k_014564:
        addq.w #0x1,%d0
m68k_014564_end:
.org 0x14566
m68k_014566:
        move.w %d0,0x10(%a0)
m68k_014566_end:
.org 0x1456A
m68k_01456a:
        addq.w #0x1,%d0
m68k_01456a_end:
.org 0x1456C
m68k_01456c:
        addq.w #0x2,%a0
m68k_01456c_end:
.org 0x1456E
m68k_01456e:
        dbra %d1,(. + -12)
m68k_01456e_end:
.org 0x14572
m68k_014572:
        rts
m68k_014572_end:
.org 0x1478A
m68k_01478a:
        cmpi.w #0x2,0xf36c:w
m68k_01478a_end:
.org 0x14790
m68k_014790:
        bne.w (. + 206)
m68k_014790_end:
.org 0x14794
m68k_014794:
        movea.l 0xff382c:l,%a0
m68k_014794_end:
.org 0x1479A
m68k_01479a:
        move.b 0x4(%a0),%d0
m68k_01479a_end:
.org 0x1479E
m68k_01479e:
        cmp.b 0xf377:w,%d0
m68k_01479e_end:
.org 0x147A2
m68k_0147a2:
        bne.w (. + 188)
m68k_0147a2_end:
.org 0x147A6
m68k_0147a6:
        move.b (%a0),%d0
m68k_0147a6_end:
.org 0x147A8
m68k_0147a8:
        andi.w #0x7f,%d0
m68k_0147a8_end:
.org 0x147AC
m68k_0147ac:
        cmpi.w #0x10,%d0
m68k_0147ac_end:
.org 0x147B0
m68k_0147b0:
        bcc.w (. + 174)
m68k_0147b0_end:
.org 0x147B4
m68k_0147b4:
        bsr.w (. + 240)
m68k_0147b4_end:
.org 0x147B8
m68k_0147b8:
        bsr.w (. + 348)
m68k_0147b8_end:
.org 0x147BC
m68k_0147bc:
        tst.w 0xcfd2:w
m68k_0147bc_end:
.org 0x147C0
m68k_0147c0:
        beq.w (. + 28)
m68k_0147c0_end:
.org 0x147C4
m68k_0147c4:
        subq.w #0x1,0xcfd2:w
m68k_0147c4_end:
.org 0x147C8
m68k_0147c8:
        cmpi.w #0x8,0xcfd2:w
m68k_0147c8_end:
.org 0x147CE
m68k_0147ce:
        bls.w (. + 144)
m68k_0147ce_end:
.org 0x147D2
m68k_0147d2:
        move.w #0x8,0xcfd2:w
m68k_0147d2_end:
.org 0x147D8
m68k_0147d8:
        bra.w (. + 134)
m68k_0147d8_end:
.org 0x147DC
m68k_0147dc:
        btst.b #0x5,0xf603:w
m68k_0147dc_end:
.org 0x147E2
m68k_0147e2:
        beq.b (. + 124)
m68k_0147e2_end:
.org 0x147E4
m68k_0147e4:
        move.w 0xf676:w,%d0
m68k_0147e4_end:
.org 0x147E8
m68k_0147e8:
        lea.l 0xff3930:l,%a0
m68k_0147e8_end:
.org 0x147EE
m68k_0147ee:
        clr.w %d1
m68k_0147ee_end:
.org 0x147F0
m68k_0147f0:
        move.b (%a0, %d0.w),%d1
m68k_0147f0_end:
.org 0x147F4
m68k_0147f4:
        move.w %d1,0xf386:w
m68k_0147f4_end:
.org 0x147F8
m68k_0147f8:
        clr.w 0xf388:w
m68k_0147f8_end:
.org 0x147FC
m68k_0147fc:
        clr.w 0xf384:w
m68k_0147fc_end:
.org 0x14800
m68k_014800:
        addq.w #0x1,%d1
m68k_014800_end:
.org 0x14802
m68k_014802:
        move.w %d1,0xf65a:w
m68k_014802_end:
.org 0x14806
m68k_014806:
        cmpi.w #0x2,%d1
m68k_014806_end:
.org 0x1480A
m68k_01480a:
        bne.b (. + 8)
m68k_01480a_end:
.org 0x1480C
m68k_01480c:
        bsr.w (. + 472)
m68k_01480c_end:
.org 0x14810
m68k_014810:
        bcs.b (. + 78)
m68k_014810_end:
.org 0x14812
m68k_014812:
        jsr 0xc0b6:l
m68k_014812_end:
.org 0x14818
m68k_014818:
        move.w #0x208,0xf612:w
m68k_014818_end:
.org 0x1481E
m68k_01481e:
        move.w #0x3,0xf362:w
m68k_01481e_end:
.org 0x14824
m68k_014824:
        move.w #0x12,0xf36a:w
m68k_014824_end:
.org 0x1482A
m68k_01482a:
        movea.l 0xff382c:l,%a0
m68k_01482a_end:
.org 0x14830
m68k_014830:
        clr.w %d0
m68k_014830_end:
.org 0x14832
m68k_014832:
        move.b 0x1(%a0),%d0
m68k_014832_end:
.org 0x14836
m68k_014836:
        lsl.w #0x4,%d0
m68k_014836_end:
.org 0x14838
m68k_014838:
        move.w %d0,0xff3822:l
m68k_014838_end:
.org 0x1483E
m68k_01483e:
        clr.w %d0
m68k_01483e_end:
.org 0x14840
m68k_014840:
        move.b 0x2(%a0),%d0
m68k_014840_end:
.org 0x14844
m68k_014844:
        lsl.w #0x4,%d0
m68k_014844_end:
.org 0x14846
m68k_014846:
        move.w %d0,0xff3824:l
m68k_014846_end:
.org 0x1484C
m68k_01484c:
        clr.w %d0
m68k_01484c_end:
.org 0x1484E
m68k_01484e:
        move.b 0x3(%a0),%d0
m68k_01484e_end:
.org 0x14852
m68k_014852:
        move.w %d0,0xf672:w
m68k_014852_end:
.org 0x14856
m68k_014856:
        move.w #0x74,0xf600:w
m68k_014856_end:
.org 0x1485C
m68k_01485c:
        bra.b (. + 64)
m68k_01485c_end:
.org 0x1485E
m68k_01485e:
        btst.b #0x4,0xf603:w
m68k_01485e_end:
.org 0x14864
m68k_014864:
        beq.b (. + 56)
m68k_014864_end:
.org 0x14866
m68k_014866:
        cmpi.w #0x2,0xf36c:w
m68k_014866_end:
.org 0x1486C
m68k_01486c:
        bne.w (. + 30)
m68k_01486c_end:
.org 0x14870
m68k_014870:
        move.w #0x208,0xf612:w
m68k_014870_end:
.org 0x14876
m68k_014876:
        move.w #0x2,0xf362:w
m68k_014876_end:
.org 0x1487C
m68k_01487c:
        move.w #0x12,0xf36a:w
m68k_01487c_end:
.org 0x14882
m68k_014882:
        clr.w 0xf65a:w
m68k_014882_end:
.org 0x14886
m68k_014886:
        bra.w (. + 22)
m68k_014886_end:
.org 0x1488A
m68k_01488a:
        move.w #0x206,0xf612:w
m68k_01488a_end:
.org 0x14890
m68k_014890:
        move.w #0x7,0xf362:w
m68k_014890_end:
.org 0x14896
m68k_014896:
        move.w #0xd,0xf36a:w
m68k_014896_end:
.org 0x1489C
m68k_01489c:
        jsr 0xa158:l
m68k_01489c_end:
.org 0x148A2
m68k_0148a2:
        rts
m68k_0148a2_end:
.org 0x148A4
m68k_0148a4:
        move.b 0xf602:w,%d0
m68k_0148a4_end:
.org 0x148A8
m68k_0148a8:
        andi.w #0x3,%d0
m68k_0148a8_end:
.org 0x148AC
m68k_0148ac:
        beq.b (. + 96)
m68k_0148ac_end:
.org 0x148AE
m68k_0148ae:
        subi.w #0x1,0xf608:w
m68k_0148ae_end:
.org 0x148B4
m68k_0148b4:
        bne.b (. + 94)
m68k_0148b4_end:
.org 0x148B6
m68k_0148b6:
        move.w #0xc,0xf608:w
m68k_0148b6_end:
.org 0x148BC
m68k_0148bc:
        btst.l #0x1,%d0
m68k_0148bc_end:
.org 0x148C0
m68k_0148c0:
        bne.b (. + 44)
m68k_0148c0_end:
.org 0x148C2
m68k_0148c2:
        tst.w 0xf676:w
m68k_0148c2_end:
.org 0x148C6
m68k_0148c6:
        bne.b (. + 30)
m68k_0148c6_end:
.org 0x148C8
m68k_0148c8:
        lea.l 0xff3930:l,%a0
m68k_0148c8_end:
.org 0x148CE
m68k_0148ce:
        clr.w %d0
m68k_0148ce_end:
.org 0x148D0
m68k_0148d0:
        tst.b 0x1(%a0, %d0.w)
m68k_0148d0_end:
.org 0x148D4
m68k_0148d4:
        bmi.w (. + 8)
m68k_0148d4_end:
.org 0x148D8
m68k_0148d8:
        addq.w #0x1,%d0
m68k_0148d8_end:
.org 0x148DA
m68k_0148da:
        bra.b (. + -10)
m68k_0148da_end:
.org 0x148DC
m68k_0148dc:
        move.w %d0,0xf676:w
m68k_0148dc_end:
.org 0x148E0
m68k_0148e0:
        bra.w (. + 50)
m68k_0148e0_end:
.org 0x148E4
m68k_0148e4:
        subq.w #0x1,0xf676:w
m68k_0148e4_end:
.org 0x148E8
m68k_0148e8:
        bra.w (. + 42)
m68k_0148e8_end:
.org 0x148EC
m68k_0148ec:
        move.w 0xf676:w,%d0
m68k_0148ec_end:
.org 0x148F0
m68k_0148f0:
        addq.w #0x1,%d0
m68k_0148f0_end:
.org 0x148F2
m68k_0148f2:
        lea.l 0xff3930:l,%a0
m68k_0148f2_end:
.org 0x148F8
m68k_0148f8:
        tst.b (%a0, %d0.w)
m68k_0148f8_end:
.org 0x148FC
m68k_0148fc:
        bpl.b (. + 10)
m68k_0148fc_end:
.org 0x148FE
m68k_0148fe:
        clr.w 0xf676:w
m68k_0148fe_end:
.org 0x14902
m68k_014902:
        bra.w (. + 16)
m68k_014902_end:
.org 0x14906
m68k_014906:
        move.w %d0,0xf676:w
m68k_014906_end:
.org 0x1490A
m68k_01490a:
        bra.b (. + 8)
m68k_01490a_end:
.org 0x1490C
m68k_01490c:
        move.w #0x1,0xf608:w
m68k_01490c_end:
.org 0x14912
m68k_014912:
        rts
m68k_014912_end:
.org 0x14914
m68k_014914:
        btst.b #0x5,0xf603:w
m68k_014914_end:
.org 0x1491A
m68k_01491a:
        bne.w (. + 58)
m68k_01491a_end:
.org 0x1491E
m68k_01491e:
        move.b 0xf602:w,%d0
m68k_01491e_end:
.org 0x14922
m68k_014922:
        andi.w #0x3,%d0
m68k_014922_end:
.org 0x14926
m68k_014926:
        bne.w (. + 12)
m68k_014926_end:
.org 0x1492A
m68k_01492a:
        btst.b #0x3,0xf321:w
m68k_01492a_end:
.org 0x14930
m68k_014930:
        bne.b (. + 36)
m68k_014930_end:
.org 0x14932
m68k_014932:
        lea.l 34(%pc),%a0
m68k_014932_end:
.org 0x14936
m68k_014936:
        nop
m68k_014936_end:
.org 0x14938
m68k_014938:
        move.w 0xf676:w,%d0
m68k_014938_end:
.org 0x1493C
m68k_01493c:
        move.w %d0,%d1
m68k_01493c_end:
.org 0x1493E
m68k_01493e:
        lsl.w #0x1,%d0
m68k_01493e_end:
.org 0x14940
m68k_014940:
        add.w %d1,%d0
m68k_014940_end:
.org 0x14942
m68k_014942:
        lsl.w #0x3,%d0
m68k_014942_end:
.org 0x14944
m68k_014944:
        addi.w #0x30,%d0
m68k_014944_end:
.org 0x14948
m68k_014948:
        move.w #0x88,%d1
m68k_014948_end:
.org 0x1494C
m68k_01494c:
        clr.w %d2
m68k_01494c_end:
.org 0x1494E
m68k_01494e:
        jsr 0xac08:l
m68k_01494e_end:
.org 0x14954
m68k_014954:
        rts
m68k_014954_end:
.org 0x149E4
m68k_0149e4:
        clr.w %d0
m68k_0149e4_end:
.org 0x149E6
m68k_0149e6:
        movea.l 0xff382c:l,%a0
m68k_0149e6_end:
.org 0x149EC
m68k_0149ec:
        clr.w %d1
m68k_0149ec_end:
.org 0x149EE
m68k_0149ee:
        move.b 0x1(%a0),%d1
m68k_0149ee_end:
.org 0x149F2
m68k_0149f2:
        clr.w %d4
m68k_0149f2_end:
.org 0x149F4
m68k_0149f4:
        move.b 0x2(%a0),%d4
m68k_0149f4_end:
.org 0x149F8
m68k_0149f8:
        move.b %d1,%d2
m68k_0149f8_end:
.org 0x149FA
m68k_0149fa:
        move.b %d1,%d3
m68k_0149fa_end:
.org 0x149FC
m68k_0149fc:
        subq.b #0x1,%d2
m68k_0149fc_end:
.org 0x149FE
m68k_0149fe:
        addq.b #0x1,%d3
m68k_0149fe_end:
.org 0x14A00
m68k_014a00:
        move.b %d4,%d5
m68k_014a00_end:
.org 0x14A02
m68k_014a02:
        move.b %d4,%d6
m68k_014a02_end:
.org 0x14A04
m68k_014a04:
        subq.b #0x1,%d5
m68k_014a04_end:
.org 0x14A06
m68k_014a06:
        addq.b #0x1,%d6
m68k_014a06_end:
.org 0x14A08
m68k_014a08:
        lea.l 0x9000:w,%a0
m68k_014a08_end:
.org 0x14A0C
m68k_014a0c:
        move.b (%a0),%d7
m68k_014a0c_end:
.org 0x14A0E
m68k_014a0e:
        andi.w #0xf,%d7
m68k_014a0e_end:
.org 0x14A12
m68k_014a12:
        beq.b (. + 32)
m68k_014a12_end:
.org 0x14A14
m68k_014a14:
        cmp.b 0x1(%a0),%d1
m68k_014a14_end:
.org 0x14A18
m68k_014a18:
        beq.w (. + 238)
m68k_014a18_end:
.org 0x14A1C
m68k_014a1c:
        cmp.b 0x1(%a0),%d2
m68k_014a1c_end:
.org 0x14A20
m68k_014a20:
        beq.w (. + 256)
m68k_014a20_end:
.org 0x14A24
m68k_014a24:
        cmp.b 0x1(%a0),%d3
m68k_014a24_end:
.org 0x14A28
m68k_014a28:
        beq.w (. + 286)
m68k_014a28_end:
.org 0x14A2C
m68k_014a2c:
        lea.l 0xd(%a0, %d7.w),%a0
m68k_014a2c_end:
.org 0x14A30
m68k_014a30:
        bra.b (. + -36)
m68k_014a30_end:
.org 0x14A32
m68k_014a32:
        cmpi.b #0xff,%d0
m68k_014a32_end:
.org 0x14A36
m68k_014a36:
        beq.w (. + 202)
m68k_014a36_end:
.org 0x14A3A
m68k_014a3a:
        move.w %d1,%d2
m68k_014a3a_end:
.org 0x14A3C
m68k_014a3c:
        move.w %d2,%d3
m68k_014a3c_end:
.org 0x14A3E
m68k_014a3e:
        lsl.w #0x3,%d3
m68k_014a3e_end:
.org 0x14A40
m68k_014a40:
        add.w %d3,%d2
m68k_014a40_end:
.org 0x14A42
m68k_014a42:
        lsl.w #0x3,%d2
m68k_014a42_end:
.org 0x14A44
m68k_014a44:
        add.w %d4,%d2
m68k_014a44_end:
.org 0x14A46
m68k_014a46:
        lea.l 0xee5f0:l,%a2
m68k_014a46_end:
.org 0x14A4C
m68k_014a4c:
        adda.w %d2,%a2
m68k_014a4c_end:
.org 0x14A4E
m68k_014a4e:
        lea.l 0x670a:l,%a1
m68k_014a4e_end:
.org 0x14A54
m68k_014a54:
        clr.w %d7
m68k_014a54_end:
.org 0x14A56
m68k_014a56:
        tst.b %d1
m68k_014a56_end:
.org 0x14A58
m68k_014a58:
        bne.b (. + 8)
m68k_014a58_end:
.org 0x14A5A
m68k_014a5a:
        ori.b #0x91,%d0
m68k_014a5a_end:
.org 0x14A5E
m68k_014a5e:
        bra.b (. + 44)
m68k_014a5e_end:
.org 0x14A60
m68k_014a60:
        move.b -0x49(%a2),%d7
m68k_014a60_end:
.org 0x14A64
m68k_014a64:
        tst.b (%a1, %d7.w)
m68k_014a64_end:
.org 0x14A68
m68k_014a68:
        bpl.b (. + 6)
m68k_014a68_end:
.org 0x14A6A
m68k_014a6a:
        bset.l #0x7,%d0
m68k_014a6a_end:
.org 0x14A6E
m68k_014a6e:
        move.b -0x48(%a2),%d7
m68k_014a6e_end:
.org 0x14A72
m68k_014a72:
        tst.b (%a1, %d7.w)
m68k_014a72_end:
.org 0x14A76
m68k_014a76:
        bpl.b (. + 6)
m68k_014a76_end:
.org 0x14A78
m68k_014a78:
        bset.l #0x0,%d0
m68k_014a78_end:
.org 0x14A7C
m68k_014a7c:
        move.b -0x47(%a2),%d7
m68k_014a7c_end:
.org 0x14A80
m68k_014a80:
        tst.b (%a1, %d7.w)
m68k_014a80_end:
.org 0x14A84
m68k_014a84:
        bpl.b (. + 6)
m68k_014a84_end:
.org 0x14A86
m68k_014a86:
        bset.l #0x4,%d0
m68k_014a86_end:
.org 0x14A8A
m68k_014a8a:
        move.b -0x1(%a2),%d7
m68k_014a8a_end:
.org 0x14A8E
m68k_014a8e:
        tst.b (%a1, %d7.w)
m68k_014a8e_end:
.org 0x14A92
m68k_014a92:
        bpl.b (. + 6)
m68k_014a92_end:
.org 0x14A94
m68k_014a94:
        bset.l #0x3,%d0
m68k_014a94_end:
.org 0x14A98
m68k_014a98:
        move.b 0x1(%a2),%d7
m68k_014a98_end:
.org 0x14A9C
m68k_014a9c:
        tst.b (%a1, %d7.w)
m68k_014a9c_end:
.org 0x14AA0
m68k_014aa0:
        bpl.b (. + 6)
m68k_014aa0_end:
.org 0x14AA2
m68k_014aa2:
        bset.l #0x1,%d0
m68k_014aa2_end:
.org 0x14AA6
m68k_014aa6:
        cmpi.b #0x47,%d1
m68k_014aa6_end:
.org 0x14AAA
m68k_014aaa:
        bcs.b (. + 8)
m68k_014aaa_end:
.org 0x14AAC
m68k_014aac:
        ori.b #0x64,%d0
m68k_014aac_end:
.org 0x14AB0
m68k_014ab0:
        bra.b (. + 44)
m68k_014ab0_end:
.org 0x14AB2
m68k_014ab2:
        move.b 0x47(%a2),%d7
m68k_014ab2_end:
.org 0x14AB6
m68k_014ab6:
        tst.b (%a1, %d7.w)
m68k_014ab6_end:
.org 0x14ABA
m68k_014aba:
        bpl.b (. + 6)
m68k_014aba_end:
.org 0x14ABC
m68k_014abc:
        bset.l #0x6,%d0
m68k_014abc_end:
.org 0x14AC0
m68k_014ac0:
        move.b 0x48(%a2),%d7
m68k_014ac0_end:
.org 0x14AC4
m68k_014ac4:
        tst.b (%a1, %d7.w)
m68k_014ac4_end:
.org 0x14AC8
m68k_014ac8:
        bpl.b (. + 6)
m68k_014ac8_end:
.org 0x14ACA
m68k_014aca:
        bset.l #0x2,%d0
m68k_014aca_end:
.org 0x14ACE
m68k_014ace:
        move.b 0x49(%a2),%d7
m68k_014ace_end:
.org 0x14AD2
m68k_014ad2:
        tst.b (%a1, %d7.w)
m68k_014ad2_end:
.org 0x14AD6
m68k_014ad6:
        bpl.b (. + 6)
m68k_014ad6_end:
.org 0x14AD8
m68k_014ad8:
        bset.l #0x5,%d0
m68k_014ad8_end:
.org 0x14ADC
m68k_014adc:
        tst.b %d4
m68k_014adc_end:
.org 0x14ADE
m68k_014ade:
        bne.b (. + 8)
m68k_014ade_end:
.org 0x14AE0
m68k_014ae0:
        ori.w #0xc8,%d0
m68k_014ae0_end:
.org 0x14AE4
m68k_014ae4:
        bra.b (. + 12)
m68k_014ae4_end:
.org 0x14AE6
m68k_014ae6:
        cmpi.b #0x47,%d4
m68k_014ae6_end:
.org 0x14AEA
m68k_014aea:
        bcs.b (. + 6)
m68k_014aea_end:
.org 0x14AEC
m68k_014aec:
        ori.b #0x32,%d0
m68k_014aec_end:
.org 0x14AF0
m68k_014af0:
        move.w %d0,0xf678:w
m68k_014af0_end:
.org 0x14AF4
m68k_014af4:
        cmpi.b #0xff,%d0
m68k_014af4_end:
.org 0x14AF8
m68k_014af8:
        beq.b (. + 8)
m68k_014af8_end:
.org 0x14AFA
m68k_014afa:
        andi.w #0xfffe,%sr
m68k_014afa_end:
.org 0x14AFE
m68k_014afe:
        bra.b (. + 6)
m68k_014afe_end:
.org 0x14B00
m68k_014b00:
        ori.w #0x1,%sr
m68k_014b00_end:
.org 0x14B04
m68k_014b04:
        rts
m68k_014b04_end:
.org 0x14B06
m68k_014b06:
        cmp.b 0x2(%a0),%d5
m68k_014b06_end:
.org 0x14B0A
m68k_014b0a:
        beq.b (. + 14)
m68k_014b0a_end:
.org 0x14B0C
m68k_014b0c:
        cmp.b 0x2(%a0),%d6
m68k_014b0c_end:
.org 0x14B10
m68k_014b10:
        bne.b (. + 12)
m68k_014b10_end:
.org 0x14B12
m68k_014b12:
        bset.l #0x1,%d0
m68k_014b12_end:
.org 0x14B16
m68k_014b16:
        bra.b (. + 6)
m68k_014b16_end:
.org 0x14B18
m68k_014b18:
        bset.l #0x3,%d0
m68k_014b18_end:
.org 0x14B1C
m68k_014b1c:
        bra.w (. + -240)
m68k_014b1c_end:
.org 0x14B20
m68k_014b20:
        cmp.b 0x2(%a0),%d4
m68k_014b20_end:
.org 0x14B24
m68k_014b24:
        beq.b (. + 20)
m68k_014b24_end:
.org 0x14B26
m68k_014b26:
        cmp.b 0x2(%a0),%d5
m68k_014b26_end:
.org 0x14B2A
m68k_014b2a:
        beq.b (. + 20)
m68k_014b2a_end:
.org 0x14B2C
m68k_014b2c:
        cmp.b 0x2(%a0),%d6
m68k_014b2c_end:
.org 0x14B30
m68k_014b30:
        bne.b (. + 18)
m68k_014b30_end:
.org 0x14B32
m68k_014b32:
        bset.l #0x4,%d0
m68k_014b32_end:
.org 0x14B36
m68k_014b36:
        bra.b (. + 12)
m68k_014b36_end:
.org 0x14B38
m68k_014b38:
        bset.l #0x0,%d0
m68k_014b38_end:
.org 0x14B3C
m68k_014b3c:
        bra.b (. + 6)
m68k_014b3c_end:
.org 0x14B3E
m68k_014b3e:
        bset.l #0x7,%d0
m68k_014b3e_end:
.org 0x14B42
m68k_014b42:
        bra.w (. + -278)
m68k_014b42_end:
.org 0x14B46
m68k_014b46:
        cmp.b 0x2(%a0),%d4
m68k_014b46_end:
.org 0x14B4A
m68k_014b4a:
        beq.b (. + 20)
m68k_014b4a_end:
.org 0x14B4C
m68k_014b4c:
        cmp.b 0x2(%a0),%d5
m68k_014b4c_end:
.org 0x14B50
m68k_014b50:
        beq.b (. + 20)
m68k_014b50_end:
.org 0x14B52
m68k_014b52:
        cmp.b 0x2(%a0),%d6
m68k_014b52_end:
.org 0x14B56
m68k_014b56:
        bne.b (. + 18)
m68k_014b56_end:
.org 0x14B58
m68k_014b58:
        bset.l #0x5,%d0
m68k_014b58_end:
.org 0x14B5C
m68k_014b5c:
        bra.b (. + 12)
m68k_014b5c_end:
.org 0x14B5E
m68k_014b5e:
        bset.l #0x2,%d0
m68k_014b5e_end:
.org 0x14B62
m68k_014b62:
        bra.b (. + 6)
m68k_014b62_end:
.org 0x14B64
m68k_014b64:
        bset.l #0x6,%d0
m68k_014b64_end:
.org 0x14B68
m68k_014b68:
        bra.w (. + -316)
m68k_014b68_end:
.org 0x14B6C
m68k_014b6c:
        tst.w 0xcfcc:w
m68k_014b6c_end:
.org 0x14B70
m68k_014b70:
        bne.w (. + 14)
m68k_014b70_end:
.org 0x14B74
m68k_014b74:
        jsr 0x662e4:l
m68k_014b74_end:
.org 0x14B7A
m68k_014b7a:
        bcs.w (. + 228)
m68k_014b7a_end:
.org 0x14B7E
m68k_014b7e:
        jsr 0x11ee:l
m68k_014b7e_end:
.org 0x14B84
m68k_014b84:
        bcs.w (. + 236)
m68k_014b84_end:
.org 0x14B88
m68k_014b88:
        lea.l 0xff39b2:l,%a0
m68k_014b88_end:
.org 0x14B8E
m68k_014b8e:
        adda.w 0xff3bb2:l,%a0
m68k_014b8e_end:
.org 0x14B94
m68k_014b94:
        tst.b (%a0)
m68k_014b94_end:
.org 0x14B96
m68k_014b96:
        beq.w (. + 10)
m68k_014b96_end:
.org 0x14B9A
m68k_014b9a:
        jsr 0x1264:l
m68k_014b9a_end:
.org 0x14BA0
m68k_014ba0:
        lea.l 0xff39b2:l,%a0
m68k_014ba0_end:
.org 0x14BA6
m68k_014ba6:
        adda.w 0xff3bb2:l,%a0
m68k_014ba6_end:
.org 0x14BAC
m68k_014bac:
        tst.b (%a0)
m68k_014bac_end:
.org 0x14BAE
m68k_014bae:
        beq.w (. + 106)
m68k_014bae_end:
.org 0x14BB2
m68k_014bb2:
        clr.w %d0
m68k_014bb2_end:
.org 0x14BB4
m68k_014bb4:
        move.b 0x1(%a0),%d0
m68k_014bb4_end:
.org 0x14BB8
m68k_014bb8:
        move.w %d0,0xff3bb4:l
m68k_014bb8_end:
.org 0x14BBE
m68k_014bbe:
        bsr.w (. + 230)
m68k_014bbe_end:
.org 0x14BC2
m68k_014bc2:
        bsr.w (. + 606)
m68k_014bc2_end:
.org 0x14BC6
m68k_014bc6:
        bcs.b (. + -72)
m68k_014bc6_end:
.org 0x14BC8
m68k_014bc8:
        bsr.w (. + 412)
m68k_014bc8_end:
.org 0x14BCC
m68k_014bcc:
        tst.w %d4
m68k_014bcc_end:
.org 0x14BCE
m68k_014bce:
        bne.w (. + 172)
m68k_014bce_end:
.org 0x14BD2
m68k_014bd2:
        lea.l 0xff3000:l,%a0
m68k_014bd2_end:
.org 0x14BD8
m68k_014bd8:
        clr.w %d0
m68k_014bd8_end:
.org 0x14BDA
m68k_014bda:
        addq.w #0x1,%a0
m68k_014bda_end:
.org 0x14BDC
m68k_014bdc:
        addq.w #0x3,%d0
m68k_014bdc_end:
.org 0x14BDE
m68k_014bde:
        move.b (%a0)+,%d1
m68k_014bde_end:
.org 0x14BE0
m68k_014be0:
        cmp.b 0xff3bb5:l,%d1
m68k_014be0_end:
.org 0x14BE6
m68k_014be6:
        beq.b (. + 12)
m68k_014be6_end:
.org 0x14BE8
m68k_014be8:
        addq.w #0x1,%a0
m68k_014be8_end:
.org 0x14BEA
m68k_014bea:
        addq.w #0x1,%d0
m68k_014bea_end:
.org 0x14BEC
m68k_014bec:
        tst.b (%a0)+
m68k_014bec_end:
.org 0x14BEE
m68k_014bee:
        bne.b (. + -4)
m68k_014bee_end:
.org 0x14BF0
m68k_014bf0:
        bra.b (. + -22)
m68k_014bf0_end:
.org 0x14BF2
m68k_014bf2:
        move.w %d0,0xff3826:l
m68k_014bf2_end:
.org 0x14BF8
m68k_014bf8:
        addq.w #0x1,0xf362:w
m68k_014bf8_end:
.org 0x14BFC
m68k_014bfc:
        tst.l 0xff382c:l
m68k_014bfc_end:
.org 0x14C02
m68k_014c02:
        beq.w (. + 120)
m68k_014c02_end:
.org 0x14C06
m68k_014c06:
        movea.l 0xff382c:l,%a0
m68k_014c06_end:
.org 0x14C0C
m68k_014c0c:
        bclr.b #0x5,(%a0)
m68k_014c0c_end:
.org 0x14C10
m68k_014c10:
        bset.b #0x4,(%a0)
m68k_014c10_end:
.org 0x14C14
m68k_014c14:
        bra.w (. + 102)
m68k_014c14_end:
.org 0x14C18
m68k_014c18:
        move.b #0xff,0xff3000:l
m68k_014c18_end:
.org 0x14C20
m68k_014c20:
        move.w #0x201,0xf612:w
m68k_014c20_end:
.org 0x14C26
m68k_014c26:
        clr.w 0xff3826:l
m68k_014c26_end:
.org 0x14C2C
m68k_014c2c:
        clr.w 0xf36c:w
m68k_014c2c_end:
.org 0x14C30
m68k_014c30:
        move.w #0xffff,0xf376:w
m68k_014c30_end:
.org 0x14C36
m68k_014c36:
        addq.b #0x1,0xf375:w
m68k_014c36_end:
.org 0x14C3A
m68k_014c3a:
        cmpi.b #0xc,0xf375:w
m68k_014c3a_end:
.org 0x14C40
m68k_014c40:
        bcs.b (. + 10)
m68k_014c40_end:
.org 0x14C42
m68k_014c42:
        addq.b #0x1,0xf374:w
m68k_014c42_end:
.org 0x14C46
m68k_014c46:
        clr.b 0xf375:w
m68k_014c46_end:
.org 0x14C4A
m68k_014c4a:
        move.w #0x80,0xf600:w
m68k_014c4a_end:
.org 0x14C50
m68k_014c50:
        bsr.w (. + 44)
m68k_014c50_end:
.org 0x14C54
m68k_014c54:
        move.w #0xffff,0xf376:w
m68k_014c54_end:
.org 0x14C5A
m68k_014c5a:
        bra.w (. + 32)
m68k_014c5a_end:
.org 0x14C5E
m68k_014c5e:
        move.w #0xb,0xf362:w
m68k_014c5e_end:
.org 0x14C64
m68k_014c64:
        move.w #0x9c,%d0
m68k_014c64_end:
.org 0x14C68
m68k_014c68:
        jsr 0x676f2:l
m68k_014c68_end:
.org 0x14C6E
m68k_014c6e:
        bra.b (. + 12)
m68k_014c6e_end:
.org 0x14C70
m68k_014c70:
        move.w #0x20c,0xf612:w
m68k_014c70_end:
.org 0x14C76
m68k_014c76:
        clr.w 0xf362:w
m68k_014c76_end:
.org 0x14C7A
m68k_014c7a:
        rts
m68k_014c7a_end:
.org 0x14C7C
m68k_014c7c:
        move.w 0xf314:w,0xf356:w
m68k_014c7c_end:
.org 0x14C82
m68k_014c82:
        move.w 0xf318:w,0xf354:w
m68k_014c82_end:
.org 0x14C88
m68k_014c88:
        lea.l 0x9000:w,%a0
m68k_014c88_end:
.org 0x14C8C
m68k_014c8c:
        move.b (%a0),%d0
m68k_014c8c_end:
.org 0x14C8E
m68k_014c8e:
        bclr.l #0x4,%d0
m68k_014c8e_end:
.org 0x14C92
m68k_014c92:
        move.b %d0,(%a0)
m68k_014c92_end:
.org 0x14C94
m68k_014c94:
        andi.w #0xf,%d0
m68k_014c94_end:
.org 0x14C98
m68k_014c98:
        beq.w (. + 10)
m68k_014c98_end:
.org 0x14C9C
m68k_014c9c:
        lea.l 0xd(%a0, %d0.w),%a0
m68k_014c9c_end:
.org 0x14CA0
m68k_014ca0:
        bra.b (. + -20)
m68k_014ca0_end:
.org 0x14CA2
m68k_014ca2:
        rts
m68k_014ca2_end:
.org 0x14CA4
m68k_014ca4:
        bsr.w (. + 144)
m68k_014ca4_end:
.org 0x14CA8
m68k_014ca8:
        bcs.w (. + 80)
m68k_014ca8_end:
.org 0x14CAC
m68k_014cac:
        lea.l 0x9000:w,%a1
m68k_014cac_end:
.org 0x14CB0
m68k_014cb0:
        cmp.b 0xd(%a1),%d0
m68k_014cb0_end:
.org 0x14CB4
m68k_014cb4:
        beq.b (. + 14)
m68k_014cb4_end:
.org 0x14CB6
m68k_014cb6:
        move.b (%a1),%d1
m68k_014cb6_end:
.org 0x14CB8
m68k_014cb8:
        andi.w #0xf,%d1
m68k_014cb8_end:
.org 0x14CBC
m68k_014cbc:
        lea.l 0xd(%a1, %d1.w),%a1
m68k_014cbc_end:
.org 0x14CC0
m68k_014cc0:
        bra.b (. + -16)
m68k_014cc0_end:
.org 0x14CC2
m68k_014cc2:
        move.l %a1,0xff382c:l
m68k_014cc2_end:
.org 0x14CC8
m68k_014cc8:
        clr.w %d1
m68k_014cc8_end:
.org 0x14CCA
m68k_014cca:
        move.b 0x1(%a1),%d1
m68k_014cca_end:
.org 0x14CCE
m68k_014cce:
        lsl.w #0x4,%d1
m68k_014cce_end:
.org 0x14CD0
m68k_014cd0:
        move.w %d1,0xff3bb6:l
m68k_014cd0_end:
.org 0x14CD6
m68k_014cd6:
        subi.w #0x68,%d1
m68k_014cd6_end:
.org 0x14CDA
m68k_014cda:
        bcc.b (. + 4)
m68k_014cda_end:
.org 0x14CDC
m68k_014cdc:
        clr.w %d1
m68k_014cdc_end:
.org 0x14CDE
m68k_014cde:
        clr.w %d2
m68k_014cde_end:
.org 0x14CE0
m68k_014ce0:
        move.b 0x2(%a1),%d2
m68k_014ce0_end:
.org 0x14CE4
m68k_014ce4:
        lsl.w #0x4,%d2
m68k_014ce4_end:
.org 0x14CE6
m68k_014ce6:
        move.w %d2,0xff3bb8:l
m68k_014ce6_end:
.org 0x14CEC
m68k_014cec:
        subi.w #0x98,%d2
m68k_014cec_end:
.org 0x14CF0
m68k_014cf0:
        bcc.b (. + 4)
m68k_014cf0_end:
.org 0x14CF2
m68k_014cf2:
        clr.w %d2
m68k_014cf2_end:
.org 0x14CF4
m68k_014cf4:
        bra.w (. + 62)
m68k_014cf4_end:
.org 0x14CF8
m68k_014cf8:
        clr.w 0xf772:w
m68k_014cf8_end:
.org 0x14CFC
m68k_014cfc:
        clr.w %d1
m68k_014cfc_end:
.org 0x14CFE
m68k_014cfe:
        move.b (%a1),%d1
m68k_014cfe_end:
.org 0x14D00
m68k_014d00:
        move.w %d1,0xf68a:w
m68k_014d00_end:
.org 0x14D04
m68k_014d04:
        cmpi.w #0x32,%d1
m68k_014d04_end:
.org 0x14D08
m68k_014d08:
        beq.b (. + -92)
m68k_014d08_end:
.org 0x14D0A
m68k_014d0a:
        lea.l 0xd4ac6:l,%a1
m68k_014d0a_end:
.org 0x14D10
m68k_014d10:
        lsl.w #0x2,%d1
m68k_014d10_end:
.org 0x14D12
m68k_014d12:
        move.w (%a1, %d1.w),%d2
m68k_014d12_end:
.org 0x14D16
m68k_014d16:
        move.w 0x2(%a1, %d1.w),%d1
m68k_014d16_end:
.org 0x14D1A
m68k_014d1a:
        subi.w #0x68,%d1
m68k_014d1a_end:
.org 0x14D1E
m68k_014d1e:
        bcc.w (. + 6)
m68k_014d1e_end:
.org 0x14D22
m68k_014d22:
        clr.w %d1
m68k_014d22_end:
.org 0x14D24
m68k_014d24:
        subi.w #0x98,%d2
m68k_014d24_end:
.org 0x14D28
m68k_014d28:
        bcc.b (. + 4)
m68k_014d28_end:
.org 0x14D2A
m68k_014d2a:
        clr.w %d2
m68k_014d2a_end:
.org 0x14D2C
m68k_014d2c:
        clr.l 0xff382c:l
m68k_014d2c_end:
.org 0x14D32
m68k_014d32:
        rts
m68k_014d32_end:
.org 0x14D34
m68k_014d34:
        lea.l 0xff3000:l,%a1
m68k_014d34_end:
.org 0x14D3A
m68k_014d3a:
        addq.w #0x1,%a1
m68k_014d3a_end:
.org 0x14D3C
m68k_014d3c:
        cmp.b (%a1)+,%d0
m68k_014d3c_end:
.org 0x14D3E
m68k_014d3e:
        beq.w (. + 10)
m68k_014d3e_end:
.org 0x14D42
m68k_014d42:
        tst.b (%a1)+
m68k_014d42_end:
.org 0x14D44
m68k_014d44:
        bne.b (. + -2)
m68k_014d44_end:
.org 0x14D46
m68k_014d46:
        bra.b (. + -12)
m68k_014d46_end:
.org 0x14D48
m68k_014d48:
        addq.w #0x1,%a1
m68k_014d48_end:
.org 0x14D4A
m68k_014d4a:
        tst.b (%a1)+
m68k_014d4a_end:
.org 0x14D4C
m68k_014d4c:
        bpl.w (. + 12)
m68k_014d4c_end:
.org 0x14D50
m68k_014d50:
        ori.w #0x1,%sr
m68k_014d50_end:
.org 0x14D54
m68k_014d54:
        bra.w (. + 14)
m68k_014d54_end:
.org 0x14D58
m68k_014d58:
        move.w #0xffff,0xf68a:w
m68k_014d58_end:
.org 0x14D5E
m68k_014d5e:
        andi.w #0xfffe,%sr
m68k_014d5e_end:
.org 0x14D62
m68k_014d62:
        rts
m68k_014d62_end:
.org 0x14E20
m68k_014e20:
        cmpi.w #0x32,0xf68a:w
m68k_014e20_end:
.org 0x14E26
m68k_014e26:
        bne.w (. + 44)
m68k_014e26_end:
.org 0x14E2A
m68k_014e2a:
        movea.l 0xff382c:l,%a0
m68k_014e2a_end:
.org 0x14E30
m68k_014e30:
        movem.l %d1-%d2,-(%a7)
m68k_014e30_end:
.org 0x14E34
m68k_014e34:
        jsr 0x1cea0:l
m68k_014e34_end:
.org 0x14E3A
m68k_014e3a:
        movem.l (%a7)+,%d1-%d2
m68k_014e3a_end:
.org 0x14E3E
m68k_014e3e:
        tst.w %d0
m68k_014e3e_end:
.org 0x14E40
m68k_014e40:
        bne.w (. + 18)
m68k_014e40_end:
.org 0x14E44
m68k_014e44:
        addq.w #0x2,0xff3bb2:l
m68k_014e44_end:
.org 0x14E4A
m68k_014e4a:
        ori.w #0x1,%sr
m68k_014e4a_end:
.org 0x14E4E
m68k_014e4e:
        bra.w (. + 8)
m68k_014e4e_end:
.org 0x14E52
m68k_014e52:
        andi.w #0xfffe,%sr
m68k_014e52_end:
.org 0x14E56
m68k_014e56:
        rts
m68k_014e56_end:
.org 0x14E58
m68k_014e58:
        clr.w 0xcfcc:w
m68k_014e58_end:
.org 0x14E5C
m68k_014e5c:
        tst.w 0xf68a:w
m68k_014e5c_end:
.org 0x14E60
m68k_014e60:
        bpl.w (. + 428)
m68k_014e60_end:
.org 0x14E64
m68k_014e64:
        move.w 0xff3bb6:l,%d0
m68k_014e64_end:
.org 0x14E6A
m68k_014e6a:
        andi.w #0xf,%d0
m68k_014e6a_end:
.org 0x14E6E
m68k_014e6e:
        bne.b (. + 124)
m68k_014e6e_end:
.org 0x14E70
m68k_014e70:
        move.w 0xff3bb8:l,%d0
m68k_014e70_end:
.org 0x14E76
m68k_014e76:
        andi.w #0xf,%d0
m68k_014e76_end:
.org 0x14E7A
m68k_014e7a:
        bne.b (. + 112)
m68k_014e7a_end:
.org 0x14E7C
m68k_014e7c:
        movea.l 0xff382c:l,%a0
m68k_014e7c_end:
.org 0x14E82
m68k_014e82:
        move.w 0xff3bb6:l,%d0
m68k_014e82_end:
.org 0x14E88
m68k_014e88:
        lsr.w #0x4,%d0
m68k_014e88_end:
.org 0x14E8A
m68k_014e8a:
        move.b %d0,0x1(%a0)
m68k_014e8a_end:
.org 0x14E8E
m68k_014e8e:
        move.w 0xff3bb8:l,%d0
m68k_014e8e_end:
.org 0x14E94
m68k_014e94:
        lsr.w #0x4,%d0
m68k_014e94_end:
.org 0x14E96
m68k_014e96:
        move.b %d0,0x2(%a0)
m68k_014e96_end:
.org 0x14E9A
m68k_014e9a:
        lea.l 0xff3000:l,%a0
m68k_014e9a_end:
.org 0x14EA0
m68k_014ea0:
        adda.w 0xff3826:l,%a0
m68k_014ea0_end:
.org 0x14EA6
m68k_014ea6:
        move.b (%a0),%d0
m68k_014ea6_end:
.org 0x14EA8
m68k_014ea8:
        beq.w (. + 174)
m68k_014ea8_end:
.org 0x14EAC
m68k_014eac:
        bsr.w (. + 562)
m68k_014eac_end:
.org 0x14EB0
m68k_014eb0:
        bsr.w (. + 1038)
m68k_014eb0_end:
.org 0x14EB4
m68k_014eb4:
        bcs.w (. + 162)
m68k_014eb4_end:
.org 0x14EB8
m68k_014eb8:
        addq.w #0x1,0xff3826:l
m68k_014eb8_end:
.org 0x14EBE
m68k_014ebe:
        bsr.w (. + 2860)
m68k_014ebe_end:
.org 0x14EC2
m68k_014ec2:
        movea.l 0xff382c:l,%a0
m68k_014ec2_end:
.org 0x14EC8
m68k_014ec8:
        clr.w %d0
m68k_014ec8_end:
.org 0x14ECA
m68k_014eca:
        move.b 0x1(%a0),%d0
m68k_014eca_end:
.org 0x14ECE
m68k_014ece:
        clr.w %d1
m68k_014ece_end:
.org 0x14ED0
m68k_014ed0:
        move.b 0x2(%a0),%d1
m68k_014ed0_end:
.org 0x14ED4
m68k_014ed4:
        bsr.w (. + -3122)
m68k_014ed4_end:
.org 0x14ED8
m68k_014ed8:
        cmpi.b #0x4,%d2
m68k_014ed8_end:
.org 0x14EDC
m68k_014edc:
        beq.w (. + 14)
m68k_014edc_end:
.org 0x14EE0
m68k_014ee0:
        move.w #0xa4,%d0
m68k_014ee0_end:
.org 0x14EE4
m68k_014ee4:
        jsr 0x808a:l
m68k_014ee4_end:
.org 0x14EEA
m68k_014eea:
        move.w 0xff3bb6:l,%d0
m68k_014eea_end:
.org 0x14EF0
m68k_014ef0:
        cmp.w 0xff3bba:l,%d0
m68k_014ef0_end:
.org 0x14EF6
m68k_014ef6:
        beq.b (. + 20)
m68k_014ef6_end:
.org 0x14EF8
m68k_014ef8:
        bhi.b (. + 12)
m68k_014ef8_end:
.org 0x14EFA
m68k_014efa:
        addi.w #0x1,0xff3bb6:l
m68k_014efa_end:
.org 0x14F02
m68k_014f02:
        bra.b (. + 8)
m68k_014f02_end:
.org 0x14F04
m68k_014f04:
        subq.w #0x1,0xff3bb6:l
m68k_014f04_end:
.org 0x14F0A
m68k_014f0a:
        move.w 0xff3bb8:l,%d0
m68k_014f0a_end:
.org 0x14F10
m68k_014f10:
        cmp.w 0xff3bbc:l,%d0
m68k_014f10_end:
.org 0x14F16
m68k_014f16:
        beq.b (. + 20)
m68k_014f16_end:
.org 0x14F18
m68k_014f18:
        bhi.b (. + 12)
m68k_014f18_end:
.org 0x14F1A
m68k_014f1a:
        addq.w #0x1,0xff3bb8:l
m68k_014f1a_end:
.org 0x14F20
m68k_014f20:
        bra.w (. + 10)
m68k_014f20_end:
.org 0x14F24
m68k_014f24:
        subq.w #0x1,0xff3bb8:l
m68k_014f24_end:
.org 0x14F2A
m68k_014f2a:
        move.w 0xff3bb6:l,%d1
m68k_014f2a_end:
.org 0x14F30
m68k_014f30:
        subi.w #0x68,%d1
m68k_014f30_end:
.org 0x14F34
m68k_014f34:
        bcc.b (. + 4)
m68k_014f34_end:
.org 0x14F36
m68k_014f36:
        clr.w %d1
m68k_014f36_end:
.org 0x14F38
m68k_014f38:
        move.w 0xff3bb8:l,%d2
m68k_014f38_end:
.org 0x14F3E
m68k_014f3e:
        subi.w #0x98,%d2
m68k_014f3e_end:
.org 0x14F42
m68k_014f42:
        bcc.b (. + 4)
m68k_014f42_end:
.org 0x14F44
m68k_014f44:
        clr.w %d2
m68k_014f44_end:
.org 0x14F46
m68k_014f46:
        bsr.w (. + -482)
m68k_014f46_end:
.org 0x14F4A
m68k_014f4a:
        bsr.w (. + 1082)
m68k_014f4a_end:
.org 0x14F4E
m68k_014f4e:
        bcs.w (. + 8)
m68k_014f4e_end:
.org 0x14F52
m68k_014f52:
        bra.w (. + 394)
m68k_014f52_end:
.org 0x14F56
m68k_014f56:
        movea.l 0xff382c:l,%a0
m68k_014f56_end:
.org 0x14F5C
m68k_014f5c:
        move.w 0xff3bb6:l,%d0
m68k_014f5c_end:
.org 0x14F62
m68k_014f62:
        lsr.w #0x4,%d0
m68k_014f62_end:
.org 0x14F64
m68k_014f64:
        move.b %d0,0x1(%a0)
m68k_014f64_end:
.org 0x14F68
m68k_014f68:
        move.w 0xff3bb8:l,%d0
m68k_014f68_end:
.org 0x14F6E
m68k_014f6e:
        lsr.w #0x4,%d0
m68k_014f6e_end:
.org 0x14F70
m68k_014f70:
        move.b %d0,0x2(%a0)
m68k_014f70_end:
.org 0x14F74
m68k_014f74:
        movea.l 0xff382c:l,%a0
m68k_014f74_end:
.org 0x14F7A
m68k_014f7a:
        bclr.b #0x6,(%a0)
m68k_014f7a_end:
.org 0x14F7E
m68k_014f7e:
        bsr.w (. + 432)
m68k_014f7e_end:
.org 0x14F82
m68k_014f82:
        addq.w #0x2,0xff3bb2:l
m68k_014f82_end:
.org 0x14F88
m68k_014f88:
        clr.w %d1
m68k_014f88_end:
.org 0x14F8A
m68k_014f8a:
        move.b 0x4(%a0),%d1
m68k_014f8a_end:
.org 0x14F8E
m68k_014f8e:
        move.w %d1,0xf376:w
m68k_014f8e_end:
.org 0x14F92
m68k_014f92:
        jsr 0x13dc:l
m68k_014f92_end:
.org 0x14F98
m68k_014f98:
        bcs.w (. + 54)
m68k_014f98_end:
.org 0x14F9C
m68k_014f9c:
        move.w #0xffff,0xf376:w
m68k_014f9c_end:
.org 0x14FA2
m68k_014fa2:
        jsr 0x1cea0:l
m68k_014fa2_end:
.org 0x14FA8
m68k_014fa8:
        tst.w %d0
m68k_014fa8_end:
.org 0x14FAA
m68k_014faa:
        beq.w (. + 36)
m68k_014faa_end:
.org 0x14FAE
m68k_014fae:
        move.w #0x14,0xf65a:w
m68k_014fae_end:
.org 0x14FB4
m68k_014fb4:
        move.w #0xb9,0xf38c:w
m68k_014fb4_end:
.org 0x14FBA
m68k_014fba:
        move.w #0x208,0xf612:w
m68k_014fba_end:
.org 0x14FC0
m68k_014fc0:
        move.w #0x4,0xf362:w
m68k_014fc0_end:
.org 0x14FC6
m68k_014fc6:
        clr.w 0xf576:w
m68k_014fc6_end:
.org 0x14FCA
m68k_014fca:
        bra.w (. + 274)
m68k_014fca_end:
.org 0x14FCE
m68k_014fce:
        bsr.w (. + 1444)
m68k_014fce_end:
.org 0x14FD2
m68k_014fd2:
        bcs.w (. + 266)
m68k_014fd2_end:
.org 0x14FD6
m68k_014fd6:
        subq.w #0x1,0xf362:w
m68k_014fd6_end:
.org 0x14FDA
m68k_014fda:
        tst.l 0xff382c:l
m68k_014fda_end:
.org 0x14FE0
m68k_014fe0:
        beq.w (. + 252)
m68k_014fe0_end:
.org 0x14FE4
m68k_014fe4:
        movea.l 0xff382c:l,%a0
m68k_014fe4_end:
.org 0x14FEA
m68k_014fea:
        clr.w %d1
m68k_014fea_end:
.org 0x14FEC
m68k_014fec:
        move.b 0x4(%a0),%d1
m68k_014fec_end:
.org 0x14FF0
m68k_014ff0:
        move.w %d1,0xf376:w
m68k_014ff0_end:
.org 0x14FF4
m68k_014ff4:
        jsr 0x13dc:l
m68k_014ff4_end:
.org 0x14FFA
m68k_014ffa:
        bcc.w (. + 14)
m68k_014ffa_end:
.org 0x14FFE
m68k_014ffe:
        move.w #0xb4,0xf600:w
m68k_014ffe_end:
.org 0x15004
m68k_015004:
        bra.w (. + 216)
m68k_015004_end:
.org 0x15008
m68k_015008:
        bra.w (. + 212)
m68k_015008_end:
.org 0x1500C
m68k_01500c:
        cmpi.w #0x32,0xf68a:w
m68k_01500c_end:
.org 0x15012
m68k_015012:
        beq.w (. + 160)
m68k_015012_end:
.org 0x15016
m68k_015016:
        move.w #0xffff,0xa5f8:w
m68k_015016_end:
.org 0x1501C
m68k_01501c:
        move.w #0x400,0xf612:w
m68k_01501c_end:
.org 0x15022
m68k_015022:
        clr.w 0xf362:w
m68k_015022_end:
.org 0x15026
m68k_015026:
        clr.w 0xf352:w
m68k_015026_end:
.org 0x1502A
m68k_01502a:
        move.w #0x1f,%d0
m68k_01502a_end:
.org 0x1502E
m68k_01502e:
        lea.l 0xfb00:w,%a0
m68k_01502e_end:
.org 0x15032
m68k_015032:
        lea.l 0xfb80:w,%a1
m68k_015032_end:
.org 0x15036
m68k_015036:
        move.w (%a0)+,(%a1)+
m68k_015036_end:
.org 0x15038
m68k_015038:
        dbra %d0,(. + -2)
m68k_015038_end:
.org 0x1503C
m68k_01503c:
        move.w #0xffff,0xa550:w
m68k_01503c_end:
.org 0x15042
m68k_015042:
        move.w #0xffff,0xa5a4:w
m68k_015042_end:
.org 0x15048
m68k_015048:
        clr.w 0xf36a:w
m68k_015048_end:
.org 0x1504C
m68k_01504c:
        addq.w #0x2,0xff3bb2:l
m68k_01504c_end:
.org 0x15052
m68k_015052:
        jsr 0x1b098:l
m68k_015052_end:
.org 0x15058
m68k_015058:
        move.w 0xf68a:w,%d0
m68k_015058_end:
.org 0x1505C
m68k_01505c:
        lea.l 0xf427:w,%a0
m68k_01505c_end:
.org 0x15060
m68k_015060:
        move.b (%a0, %d0.w),%d0
m68k_015060_end:
.org 0x15064
m68k_015064:
        cmp.b 0xf67b:w,%d0
m68k_015064_end:
.org 0x15068
m68k_015068:
        beq.w (. + 20)
m68k_015068_end:
.org 0x1506C
m68k_01506c:
        cmp.b 0xf67d:w,%d0
m68k_01506c_end:
.org 0x15070
m68k_015070:
        beq.w (. + 12)
m68k_015070_end:
.org 0x15074
m68k_015074:
        cmp.b 0xf67f:w,%d0
m68k_015074_end:
.org 0x15078
m68k_015078:
        bne.w (. + 100)
m68k_015078_end:
.org 0x1507C
m68k_01507c:
        move.w #0x209,0xf612:w
m68k_01507c_end:
.org 0x15082
m68k_015082:
        move.w #0xe,0xf362:w
m68k_015082_end:
.org 0x15088
m68k_015088:
        andi.w #0xf,%d0
m68k_015088_end:
.org 0x1508C
m68k_01508c:
        move.w %d0,0xf376:w
m68k_01508c_end:
.org 0x15090
m68k_015090:
        move.w 0xf68a:w,%d1
m68k_015090_end:
.org 0x15094
m68k_015094:
        move.w %d1,0xf646:w
m68k_015094_end:
.org 0x15098
m68k_015098:
        move.w #0x94,%d0
m68k_015098_end:
.org 0x1509C
m68k_01509c:
        lea.l 0x9fff:w,%a0
m68k_01509c_end:
.org 0x150A0
m68k_0150a0:
        tst.b (%a0, %d1.w)
m68k_0150a0_end:
.org 0x150A4
m68k_0150a4:
        bne.w (. + 56)
m68k_0150a4_end:
.org 0x150A8
m68k_0150a8:
        jsr 0x676f2:l
m68k_0150a8_end:
.org 0x150AE
m68k_0150ae:
        bra.w (. + 46)
m68k_0150ae_end:
.org 0x150B2
m68k_0150b2:
        jsr 0x1cea0:l
m68k_0150b2_end:
.org 0x150B8
m68k_0150b8:
        tst.w %d0
m68k_0150b8_end:
.org 0x150BA
m68k_0150ba:
        beq.w (. + -356)
m68k_0150ba_end:
.org 0x150BE
m68k_0150be:
        move.w #0x13,0xf65a:w
m68k_0150be_end:
.org 0x150C4
m68k_0150c4:
        move.w #0xb4,0xf38c:w
m68k_0150c4_end:
.org 0x150CA
m68k_0150ca:
        move.w #0x208,0xf612:w
m68k_0150ca_end:
.org 0x150D0
m68k_0150d0:
        move.w #0x4,0xf362:w
m68k_0150d0_end:
.org 0x150D6
m68k_0150d6:
        addq.w #0x2,0xff3bb2:l
m68k_0150d6_end:
.org 0x150DC
m68k_0150dc:
        rts
m68k_0150dc_end:
.org 0x150DE
m68k_0150de:
        move.w 0xff3bb6:l,%d1
m68k_0150de_end:
.org 0x150E4
m68k_0150e4:
        move.w 0xff3bb8:l,%d2
m68k_0150e4_end:
.org 0x150EA
m68k_0150ea:
        subq.w #0x1,%d0
m68k_0150ea_end:
.org 0x150EC
m68k_0150ec:
        bne.b (. + 8)
m68k_0150ec_end:
.org 0x150EE
m68k_0150ee:
        subi.w #0x10,%d1
m68k_0150ee_end:
.org 0x150F2
m68k_0150f2:
        bra.b (. + 46)
m68k_0150f2_end:
.org 0x150F4
m68k_0150f4:
        subq.w #0x1,%d0
m68k_0150f4_end:
.org 0x150F6
m68k_0150f6:
        bne.b (. + 18)
m68k_0150f6_end:
.org 0x150F8
m68k_0150f8:
        addi.w #0x10,%d2
m68k_0150f8_end:
.org 0x150FC
m68k_0150fc:
        movea.l 0xff382c:l,%a1
m68k_0150fc_end:
.org 0x15102
m68k_015102:
        bset.b #0x7,(%a1)
m68k_015102_end:
.org 0x15106
m68k_015106:
        bra.b (. + 26)
m68k_015106_end:
.org 0x15108
m68k_015108:
        subq.w #0x1,%d0
m68k_015108_end:
.org 0x1510A
m68k_01510a:
        bne.b (. + 8)
m68k_01510a_end:
.org 0x1510C
m68k_01510c:
        addi.w #0x10,%d1
m68k_01510c_end:
.org 0x15110
m68k_015110:
        bra.b (. + 16)
m68k_015110_end:
.org 0x15112
m68k_015112:
        subi.w #0x10,%d2
m68k_015112_end:
.org 0x15116
m68k_015116:
        movea.l 0xff382c:l,%a1
m68k_015116_end:
.org 0x1511C
m68k_01511c:
        bclr.b #0x7,(%a1)
m68k_01511c_end:
.org 0x15120
m68k_015120:
        move.w %d1,0xff3bba:l
m68k_015120_end:
.org 0x15126
m68k_015126:
        move.w %d2,0xff3bbc:l
m68k_015126_end:
.org 0x1512C
m68k_01512c:
        rts
m68k_01512c_end:
.org 0x1512E
m68k_01512e:
        movea.l 0xff382c:l,%a0
m68k_01512e_end:
.org 0x15134
m68k_015134:
        move.b 0x1(%a0),%d1
m68k_015134_end:
.org 0x15138
m68k_015138:
        move.b 0x2(%a0),%d2
m68k_015138_end:
.org 0x1513C
m68k_01513c:
        move.b 0x4(%a0),%d3
m68k_01513c_end:
.org 0x15140
m68k_015140:
        lea.l 0x9000:w,%a1
m68k_015140_end:
.org 0x15144
m68k_015144:
        move.b (%a1),%d0
m68k_015144_end:
.org 0x15146
m68k_015146:
        btst.l #0x6,%d0
m68k_015146_end:
.org 0x1514A
m68k_01514a:
        bne.b (. + 42)
m68k_01514a_end:
.org 0x1514C
m68k_01514c:
        andi.w #0xf,%d0
m68k_01514c_end:
.org 0x15150
m68k_015150:
        beq.b (. + 46)
m68k_015150_end:
.org 0x15152
m68k_015152:
        cmpa.l %a0,%a1
m68k_015152_end:
.org 0x15154
m68k_015154:
        beq.b (. + 32)
m68k_015154_end:
.org 0x15156
m68k_015156:
        cmp.b 0x1(%a1),%d1
m68k_015156_end:
.org 0x1515A
m68k_01515a:
        bne.b (. + 26)
m68k_01515a_end:
.org 0x1515C
m68k_01515c:
        cmp.b 0x2(%a1),%d2
m68k_01515c_end:
.org 0x15160
m68k_015160:
        bne.b (. + 20)
m68k_015160_end:
.org 0x15162
m68k_015162:
        cmp.b 0x4(%a1),%d3
m68k_015162_end:
.org 0x15166
m68k_015166:
        bne.b (. + 14)
m68k_015166_end:
.org 0x15168
m68k_015168:
        cmpa.l %a0,%a1
m68k_015168_end:
.org 0x1516A
m68k_01516a:
        bhi.b (. + 4)
m68k_01516a_end:
.org 0x1516C
m68k_01516c:
        exg %a0,%a1
m68k_01516c_end:
.org 0x1516E
m68k_01516e:
        bsr.w (. + 24)
m68k_01516e_end:
.org 0x15172
m68k_015172:
        bra.b (. + 12)
m68k_015172_end:
.org 0x15174
m68k_015174:
        andi.w #0xf,%d0
m68k_015174_end:
.org 0x15178
m68k_015178:
        lea.l 0xd(%a1, %d0.w),%a1
m68k_015178_end:
.org 0x1517C
m68k_01517c:
        bra.b (. + -56)
m68k_01517c_end:
.org 0x1517E
m68k_01517e:
        move.l %a0,0xff382c:l
m68k_01517e_end:
.org 0x15184
m68k_015184:
        rts
m68k_015184_end:
.org 0x15186
m68k_015186:
        move.b (%a1),%d0
m68k_015186_end:
.org 0x15188
m68k_015188:
        andi.w #0xf,%d0
m68k_015188_end:
.org 0x1518C
m68k_01518c:
        move.b (%a0),%d1
m68k_01518c_end:
.org 0x1518E
m68k_01518e:
        andi.w #0xf,%d1
m68k_01518e_end:
.org 0x15192
m68k_015192:
        move.w %d1,%d2
m68k_015192_end:
.org 0x15194
m68k_015194:
        add.w %d0,%d1
m68k_015194_end:
.org 0x15196
m68k_015196:
        move.b %d1,(%a0)
m68k_015196_end:
.org 0x15198
m68k_015198:
        addi.w #0xd,%d2
m68k_015198_end:
.org 0x1519C
m68k_01519c:
        lea.l (%a0, %d2.w),%a4
m68k_01519c_end:
.org 0x151A0
m68k_0151a0:
        move.b 0x5(%a0),%d2
m68k_0151a0_end:
.org 0x151A4
m68k_0151a4:
        lsl.w #0x8,%d2
m68k_0151a4_end:
.org 0x151A6
m68k_0151a6:
        move.b 0x6(%a0),%d2
m68k_0151a6_end:
.org 0x151AA
m68k_0151aa:
        lsl.l #0x8,%d2
m68k_0151aa_end:
.org 0x151AC
m68k_0151ac:
        move.b 0x7(%a0),%d2
m68k_0151ac_end:
.org 0x151B0
m68k_0151b0:
        lsl.l #0x8,%d2
m68k_0151b0_end:
.org 0x151B2
m68k_0151b2:
        move.b 0x8(%a0),%d2
m68k_0151b2_end:
.org 0x151B6
m68k_0151b6:
        move.b 0x5(%a1),%d3
m68k_0151b6_end:
.org 0x151BA
m68k_0151ba:
        lsl.w #0x8,%d3
m68k_0151ba_end:
.org 0x151BC
m68k_0151bc:
        move.b 0x6(%a1),%d3
m68k_0151bc_end:
.org 0x151C0
m68k_0151c0:
        lsl.l #0x8,%d3
m68k_0151c0_end:
.org 0x151C2
m68k_0151c2:
        move.b 0x7(%a1),%d3
m68k_0151c2_end:
.org 0x151C6
m68k_0151c6:
        lsl.l #0x8,%d3
m68k_0151c6_end:
.org 0x151C8
m68k_0151c8:
        move.b 0x8(%a1),%d3
m68k_0151c8_end:
.org 0x151CC
m68k_0151cc:
        add.l %d3,%d2
m68k_0151cc_end:
.org 0x151CE
m68k_0151ce:
        cmpi.l #0xf423f,%d2
m68k_0151ce_end:
.org 0x151D4
m68k_0151d4:
        bls.b (. + 8)
m68k_0151d4_end:
.org 0x151D6
m68k_0151d6:
        move.l #0xf423f,%d2
m68k_0151d6_end:
.org 0x151DC
m68k_0151dc:
        move.b %d2,0x8(%a0)
m68k_0151dc_end:
.org 0x151E0
m68k_0151e0:
        lsr.l #0x8,%d2
m68k_0151e0_end:
.org 0x151E2
m68k_0151e2:
        move.b %d2,0x7(%a0)
m68k_0151e2_end:
.org 0x151E6
m68k_0151e6:
        lsr.l #0x8,%d2
m68k_0151e6_end:
.org 0x151E8
m68k_0151e8:
        move.b %d2,0x6(%a0)
m68k_0151e8_end:
.org 0x151EC
m68k_0151ec:
        lsr.w #0x8,%d2
m68k_0151ec_end:
.org 0x151EE
m68k_0151ee:
        move.b %d2,0x5(%a0)
m68k_0151ee_end:
.org 0x151F2
m68k_0151f2:
        move.b 0x9(%a0),%d2
m68k_0151f2_end:
.org 0x151F6
m68k_0151f6:
        lsl.w #0x8,%d2
m68k_0151f6_end:
.org 0x151F8
m68k_0151f8:
        move.b 0xa(%a0),%d2
m68k_0151f8_end:
.org 0x151FC
m68k_0151fc:
        lsl.l #0x8,%d2
m68k_0151fc_end:
.org 0x151FE
m68k_0151fe:
        move.b 0xb(%a0),%d2
m68k_0151fe_end:
.org 0x15202
m68k_015202:
        lsl.l #0x8,%d2
m68k_015202_end:
.org 0x15204
m68k_015204:
        move.b 0xc(%a0),%d2
m68k_015204_end:
.org 0x15208
m68k_015208:
        move.b 0x9(%a1),%d3
m68k_015208_end:
.org 0x1520C
m68k_01520c:
        lsl.w #0x8,%d3
m68k_01520c_end:
.org 0x1520E
m68k_01520e:
        move.b 0xa(%a1),%d3
m68k_01520e_end:
.org 0x15212
m68k_015212:
        lsl.l #0x8,%d3
m68k_015212_end:
.org 0x15214
m68k_015214:
        move.b 0xb(%a1),%d3
m68k_015214_end:
.org 0x15218
m68k_015218:
        lsl.l #0x8,%d3
m68k_015218_end:
.org 0x1521A
m68k_01521a:
        move.b 0xc(%a1),%d3
m68k_01521a_end:
.org 0x1521E
m68k_01521e:
        add.l %d2,%d3
m68k_01521e_end:
.org 0x15220
m68k_015220:
        cmpi.l #0xf423f,%d3
m68k_015220_end:
.org 0x15226
m68k_015226:
        bls.b (. + 8)
m68k_015226_end:
.org 0x15228
m68k_015228:
        move.l #0xf423f,%d3
m68k_015228_end:
.org 0x1522E
m68k_01522e:
        move.b %d3,0xc(%a0)
m68k_01522e_end:
.org 0x15232
m68k_015232:
        lsr.l #0x8,%d3
m68k_015232_end:
.org 0x15234
m68k_015234:
        move.b %d3,0xb(%a0)
m68k_015234_end:
.org 0x15238
m68k_015238:
        lsr.l #0x8,%d3
m68k_015238_end:
.org 0x1523A
m68k_01523a:
        move.b %d3,0xa(%a0)
m68k_01523a_end:
.org 0x1523E
m68k_01523e:
        lsr.w #0x8,%d3
m68k_01523e_end:
.org 0x15240
m68k_015240:
        move.b %d3,0x9(%a0)
m68k_015240_end:
.org 0x15244
m68k_015244:
        clr.w %d1
m68k_015244_end:
.org 0x15246
m68k_015246:
        lea.l 0xf65c:w,%a2
m68k_015246_end:
.org 0x1524A
m68k_01524a:
        move.b 0xd(%a1, %d1.w),(%a2)+
m68k_01524a_end:
.org 0x1524E
m68k_01524e:
        addq.w #0x1,%d1
m68k_01524e_end:
.org 0x15250
m68k_015250:
        cmp.w %d0,%d1
m68k_015250_end:
.org 0x15252
m68k_015252:
        bcs.b (. + -8)
m68k_015252_end:
.org 0x15254
m68k_015254:
        move.w %d0,%d1
m68k_015254_end:
.org 0x15256
m68k_015256:
        addi.w #0xd,%d1
m68k_015256_end:
.org 0x1525A
m68k_01525a:
        lea.l (%a1, %d1.w),%a2
m68k_01525a_end:
.org 0x1525E
m68k_01525e:
        lea.l (%a1, %d0.w),%a3
m68k_01525e_end:
.org 0x15262
m68k_015262:
        lea.l (%a1),%a5
m68k_015262_end:
.org 0x15264
m68k_015264:
        movea.l %a3,%a1
m68k_015264_end:
.org 0x15266
m68k_015266:
        cmpa.l %a5,%a4
m68k_015266_end:
.org 0x15268
m68k_015268:
        beq.b (. + 8)
m68k_015268_end:
.org 0x1526A
m68k_01526a:
        move.b -(%a5),-(%a3)
m68k_01526a_end:
.org 0x1526C
m68k_01526c:
        cmpa.l %a5,%a4
m68k_01526c_end:
.org 0x1526E
m68k_01526e:
        bcs.b (. + -4)
m68k_01526e_end:
.org 0x15270
m68k_015270:
        lea.l 0xf65c:w,%a6
m68k_015270_end:
.org 0x15274
m68k_015274:
        subq.w #0x1,%d0
m68k_015274_end:
.org 0x15276
m68k_015276:
        move.b (%a6)+,(%a4)+
m68k_015276_end:
.org 0x15278
m68k_015278:
        dbra %d0,(. + -2)
m68k_015278_end:
.org 0x1527C
m68k_01527c:
        move.b (%a2),%d0
m68k_01527c_end:
.org 0x1527E
m68k_01527e:
        andi.w #0xf,%d0
m68k_01527e_end:
.org 0x15282
m68k_015282:
        beq.b (. + 14)
m68k_015282_end:
.org 0x15284
m68k_015284:
        addi.w #0xc,%d0
m68k_015284_end:
.org 0x15288
m68k_015288:
        move.b (%a2)+,(%a1)+
m68k_015288_end:
.org 0x1528A
m68k_01528a:
        dbra %d0,(. + -2)
m68k_01528a_end:
.org 0x1528E
m68k_01528e:
        bra.b (. + -18)
m68k_01528e_end:
.org 0x15290
m68k_015290:
        clr.b (%a1)
m68k_015290_end:
.org 0x15292
m68k_015292:
        lea.l 0xd(%a0),%a1
m68k_015292_end:
.org 0x15296
m68k_015296:
        lea.l 0xc400:w,%a2
m68k_015296_end:
.org 0x1529A
m68k_01529a:
        moveq #0,%d0
m68k_01529a_end:
.org 0x1529C
m68k_01529c:
        clr.w %d1
m68k_01529c_end:
.org 0x1529E
m68k_01529e:
        move.b (%a0),%d2
m68k_01529e_end:
.org 0x152A0
m68k_0152a0:
        andi.w #0xf,%d2
m68k_0152a0_end:
.org 0x152A4
m68k_0152a4:
        move.w %d2,%d3
m68k_0152a4_end:
.org 0x152A6
m68k_0152a6:
        subq.w #0x1,%d3
m68k_0152a6_end:
.org 0x152A8
m68k_0152a8:
        move.b (%a1)+,%d1
m68k_0152a8_end:
.org 0x152AA
m68k_0152aa:
        clr.w %d4
m68k_0152aa_end:
.org 0x152AC
m68k_0152ac:
        move.b (%a2, %d1.w),%d4
m68k_0152ac_end:
.org 0x152B0
m68k_0152b0:
        add.w %d4,%d0
m68k_0152b0_end:
.org 0x152B2
m68k_0152b2:
        dbra %d3,(. + -10)
m68k_0152b2_end:
.org 0x152B6
m68k_0152b6:
        divu.w %d2,%d0
m68k_0152b6_end:
.org 0x152B8
m68k_0152b8:
        move.b %d0,0x3(%a0)
m68k_0152b8_end:
.org 0x152BC
m68k_0152bc:
        rts
m68k_0152bc_end:
.org 0x152BE
m68k_0152be:
        move.w 0xff3bba:l,%d0
m68k_0152be_end:
.org 0x152C4
m68k_0152c4:
        lsr.w #0x4,%d0
m68k_0152c4_end:
.org 0x152C6
m68k_0152c6:
        move.w 0xff3bbc:l,%d1
m68k_0152c6_end:
.org 0x152CC
m68k_0152cc:
        lsr.w #0x4,%d1
m68k_0152cc_end:
.org 0x152CE
m68k_0152ce:
        movea.l 0xff382c:l,%a0
m68k_0152ce_end:
.org 0x152D4
m68k_0152d4:
        move.b (%a0),%d2
m68k_0152d4_end:
.org 0x152D6
m68k_0152d6:
        andi.w #0xf,%d2
m68k_0152d6_end:
.org 0x152DA
m68k_0152da:
        move.b 0x4(%a0),%d4
m68k_0152da_end:
.org 0x152DE
m68k_0152de:
        lea.l 0x9000:w,%a1
m68k_0152de_end:
.org 0x152E2
m68k_0152e2:
        move.b (%a1),%d3
m68k_0152e2_end:
.org 0x152E4
m68k_0152e4:
        andi.w #0xf,%d3
m68k_0152e4_end:
.org 0x152E8
m68k_0152e8:
        beq.b (. + 66)
m68k_0152e8_end:
.org 0x152EA
m68k_0152ea:
        cmp.b 0x1(%a1),%d0
m68k_0152ea_end:
.org 0x152EE
m68k_0152ee:
        bne.b (. + 52)
m68k_0152ee_end:
.org 0x152F0
m68k_0152f0:
        cmp.b 0x2(%a1),%d1
m68k_0152f0_end:
.org 0x152F4
m68k_0152f4:
        bne.b (. + 46)
m68k_0152f4_end:
.org 0x152F6
m68k_0152f6:
        cmp.b 0x4(%a1),%d4
m68k_0152f6_end:
.org 0x152FA
m68k_0152fa:
        bne.w (. + 132)
m68k_0152fa_end:
.org 0x152FE
m68k_0152fe:
        lea.l 0xff3000:l,%a2
m68k_0152fe_end:
.org 0x15304
m68k_015304:
        adda.w 0xff3826:l,%a2
m68k_015304_end:
.org 0x1530A
m68k_01530a:
        tst.b 0x1(%a2)
m68k_01530a_end:
.org 0x1530E
m68k_01530e:
        bne.w (. + 106)
m68k_01530e_end:
.org 0x15312
m68k_015312:
        move.w %d3,%d4
m68k_015312_end:
.org 0x15314
m68k_015314:
        add.w %d2,%d4
m68k_015314_end:
.org 0x15316
m68k_015316:
        cmpi.w #0xa,%d4
m68k_015316_end:
.org 0x1531A
m68k_01531a:
        bhi.w (. + 100)
m68k_01531a_end:
.org 0x1531E
m68k_01531e:
        bra.w (. + 90)
m68k_01531e_end:
.org 0x15322
m68k_015322:
        addi.w #0xd,%d3
m68k_015322_end:
.org 0x15326
m68k_015326:
        adda.w %d3,%a1
m68k_015326_end:
.org 0x15328
m68k_015328:
        bra.b (. + -70)
m68k_015328_end:
.org 0x1532A
m68k_01532a:
        lea.l 0xce9c:w,%a1
m68k_01532a_end:
.org 0x1532E
m68k_01532e:
        move.w #0x27,%d2
m68k_01532e_end:
.org 0x15332
m68k_015332:
        tst.b (%a1)
m68k_015332_end:
.org 0x15334
m68k_015334:
        beq.b (. + 14)
m68k_015334_end:
.org 0x15336
m68k_015336:
        cmp.b 0x1(%a1),%d0
m68k_015336_end:
.org 0x1533A
m68k_01533a:
        bne.b (. + 8)
m68k_01533a_end:
.org 0x1533C
m68k_01533c:
        cmp.b 0x2(%a1),%d1
m68k_01533c_end:
.org 0x15340
m68k_015340:
        beq.b (. + 12)
m68k_015340_end:
.org 0x15342
m68k_015342:
        subq.w #0x4,%a1
m68k_015342_end:
.org 0x15344
m68k_015344:
        dbra %d2,(. + -18)
m68k_015344_end:
.org 0x15348
m68k_015348:
        bra.w (. + 48)
m68k_015348_end:
.org 0x1534C
m68k_01534c:
        lea.l 0xe710:w,%a3
m68k_01534c_end:
.org 0x15350
m68k_015350:
        move.w %d4,%d7
m68k_015350_end:
.org 0x15352
m68k_015352:
        lsl.w #0x1,%d7
m68k_015352_end:
.org 0x15354
m68k_015354:
        move.w (%a3, %d7.w),%d7
m68k_015354_end:
.org 0x15358
m68k_015358:
        lea.l 0xf428:w,%a3
m68k_015358_end:
.org 0x1535C
m68k_01535c:
        move.b (%a3, %d2.w),%d3
m68k_01535c_end:
.org 0x15360
m68k_015360:
        cmp.b %d3,%d4
m68k_015360_end:
.org 0x15362
m68k_015362:
        beq.w (. + 28)
m68k_015362_end:
.org 0x15366
m68k_015366:
        ext.w %d3
m68k_015366_end:
.org 0x15368
m68k_015368:
        btst.l %d3,%d7
m68k_015368_end:
.org 0x1536A
m68k_01536a:
        bne.w (. + 20)
m68k_01536a_end:
.org 0x1536E
m68k_01536e:
        movea.l %a1,%a0
m68k_01536e_end:
.org 0x15370
m68k_015370:
        bsr.w (. + 344)
m68k_015370_end:
.org 0x15374
m68k_015374:
        bra.w (. + 10)
m68k_015374_end:
.org 0x15378
m68k_015378:
        andi.w #0xfffe,%sr
m68k_015378_end:
.org 0x1537C
m68k_01537c:
        bra.b (. + 6)
m68k_01537c_end:
.org 0x1537E
m68k_01537e:
        ori.w #0x1,%sr
m68k_01537e_end:
.org 0x15382
m68k_015382:
        rts
m68k_015382_end:
.org 0x15384
m68k_015384:
        move.w 0xff3bb6:l,%d0
m68k_015384_end:
.org 0x1538A
m68k_01538a:
        andi.w #0xf,%d0
m68k_01538a_end:
.org 0x1538E
m68k_01538e:
        bne.w (. + 308)
m68k_01538e_end:
.org 0x15392
m68k_015392:
        move.w 0xff3bb8:l,%d1
m68k_015392_end:
.org 0x15398
m68k_015398:
        andi.w #0xf,%d1
m68k_015398_end:
.org 0x1539C
m68k_01539c:
        bne.w (. + 294)
m68k_01539c_end:
.org 0x153A0
m68k_0153a0:
        move.w 0xff3bb6:l,%d0
m68k_0153a0_end:
.org 0x153A6
m68k_0153a6:
        lsr.w #0x4,%d0
m68k_0153a6_end:
.org 0x153A8
m68k_0153a8:
        move.w %d0,%d1
m68k_0153a8_end:
.org 0x153AA
m68k_0153aa:
        subq.w #0x1,%d1
m68k_0153aa_end:
.org 0x153AC
m68k_0153ac:
        move.w %d0,%d2
m68k_0153ac_end:
.org 0x153AE
m68k_0153ae:
        addq.w #0x1,%d2
m68k_0153ae_end:
.org 0x153B0
m68k_0153b0:
        move.w 0xff3bb8:l,%d3
m68k_0153b0_end:
.org 0x153B6
m68k_0153b6:
        lsr.w #0x4,%d3
m68k_0153b6_end:
.org 0x153B8
m68k_0153b8:
        move.w %d3,%d4
m68k_0153b8_end:
.org 0x153BA
m68k_0153ba:
        subq.w #0x1,%d4
m68k_0153ba_end:
.org 0x153BC
m68k_0153bc:
        move.w %d3,%d5
m68k_0153bc_end:
.org 0x153BE
m68k_0153be:
        addq.w #0x1,%d5
m68k_0153be_end:
.org 0x153C0
m68k_0153c0:
        lea.l 0xe710:w,%a0
m68k_0153c0_end:
.org 0x153C4
m68k_0153c4:
        movea.l 0xff382c:l,%a2
m68k_0153c4_end:
.org 0x153CA
m68k_0153ca:
        clr.w %d6
m68k_0153ca_end:
.org 0x153CC
m68k_0153cc:
        move.b 0x4(%a2),%d6
m68k_0153cc_end:
.org 0x153D0
m68k_0153d0:
        move.w %d6,0xff3bbe:l
m68k_0153d0_end:
.org 0x153D6
m68k_0153d6:
        lsl.w #0x1,%d6
m68k_0153d6_end:
.org 0x153D8
m68k_0153d8:
        move.w (%a0, %d6.w),%d6
m68k_0153d8_end:
.org 0x153DC
m68k_0153dc:
        move.w %d6,0xff3bc0:l
m68k_0153dc_end:
.org 0x153E2
m68k_0153e2:
        lea.l 0x9000:w,%a0
m68k_0153e2_end:
.org 0x153E6
m68k_0153e6:
        move.b (%a0),%d7
m68k_0153e6_end:
.org 0x153E8
m68k_0153e8:
        andi.w #0xf,%d7
m68k_0153e8_end:
.org 0x153EC
m68k_0153ec:
        beq.w (. + 98)
m68k_0153ec_end:
.org 0x153F0
m68k_0153f0:
        btst.b #0x5,(%a0)
m68k_0153f0_end:
.org 0x153F4
m68k_0153f4:
        bne.w (. + 78)
m68k_0153f4_end:
.org 0x153F8
m68k_0153f8:
        clr.w %d7
m68k_0153f8_end:
.org 0x153FA
m68k_0153fa:
        move.b 0x4(%a0),%d7
m68k_0153fa_end:
.org 0x153FE
m68k_0153fe:
        cmp.b 0xff3bbf:l,%d7
m68k_0153fe_end:
.org 0x15404
m68k_015404:
        beq.b (. + 62)
m68k_015404_end:
.org 0x15406
m68k_015406:
        move.w 0xff3bc0:l,%d6
m68k_015406_end:
.org 0x1540C
m68k_01540c:
        btst.l %d7,%d6
m68k_01540c_end:
.org 0x1540E
m68k_01540e:
        bne.b (. + 52)
m68k_01540e_end:
.org 0x15410
m68k_015410:
        cmp.b 0x1(%a0),%d1
m68k_015410_end:
.org 0x15414
m68k_015414:
        bne.b (. + 10)
m68k_015414_end:
.org 0x15416
m68k_015416:
        cmp.b 0x2(%a0),%d3
m68k_015416_end:
.org 0x1541A
m68k_01541a:
        beq.w (. + 162)
m68k_01541a_end:
.org 0x1541E
m68k_01541e:
        cmp.b 0x1(%a0),%d0
m68k_01541e_end:
.org 0x15422
m68k_015422:
        bne.b (. + 18)
m68k_015422_end:
.org 0x15424
m68k_015424:
        cmp.b 0x2(%a0),%d4
m68k_015424_end:
.org 0x15428
m68k_015428:
        beq.w (. + 148)
m68k_015428_end:
.org 0x1542C
m68k_01542c:
        cmp.b 0x2(%a0),%d5
m68k_01542c_end:
.org 0x15430
m68k_015430:
        beq.w (. + 140)
m68k_015430_end:
.org 0x15434
m68k_015434:
        cmp.b 0x1(%a0),%d2
m68k_015434_end:
.org 0x15438
m68k_015438:
        bne.b (. + 10)
m68k_015438_end:
.org 0x1543A
m68k_01543a:
        cmp.b 0x2(%a0),%d3
m68k_01543a_end:
.org 0x1543E
m68k_01543e:
        beq.w (. + 126)
m68k_01543e_end:
.org 0x15442
m68k_015442:
        move.b (%a0),%d7
m68k_015442_end:
.org 0x15444
m68k_015444:
        andi.w #0xf,%d7
m68k_015444_end:
.org 0x15448
m68k_015448:
        lea.l 0xd(%a0, %d7.w),%a0
m68k_015448_end:
.org 0x1544C
m68k_01544c:
        bra.b (. + -102)
m68k_01544c_end:
.org 0x1544E
m68k_01544e:
        lea.l 0xce9c:w,%a0
m68k_01544e_end:
.org 0x15452
m68k_015452:
        lea.l 0xf428:w,%a1
m68k_015452_end:
.org 0x15456
m68k_015456:
        swap %d0
m68k_015456_end:
.org 0x15458
m68k_015458:
        move.w #0x27,%d0
m68k_015458_end:
.org 0x1545C
m68k_01545c:
        tst.b (%a0)
m68k_01545c_end:
.org 0x1545E
m68k_01545e:
        beq.w (. + 80)
m68k_01545e_end:
.org 0x15462
m68k_015462:
        clr.w %d7
m68k_015462_end:
.org 0x15464
m68k_015464:
        move.b (%a1, %d0.w),%d7
m68k_015464_end:
.org 0x15468
m68k_015468:
        cmp.b 0xff3bbf:l,%d7
m68k_015468_end:
.org 0x1546E
m68k_01546e:
        beq.b (. + 64)
m68k_01546e_end:
.org 0x15470
m68k_015470:
        move.w 0xff3bc0:l,%d6
m68k_015470_end:
.org 0x15476
m68k_015476:
        btst.l %d7,%d6
m68k_015476_end:
.org 0x15478
m68k_015478:
        bne.b (. + 54)
m68k_015478_end:
.org 0x1547A
m68k_01547a:
        swap %d0
m68k_01547a_end:
.org 0x1547C
m68k_01547c:
        cmp.b 0x1(%a0),%d1
m68k_01547c_end:
.org 0x15480
m68k_015480:
        bne.b (. + 8)
m68k_015480_end:
.org 0x15482
m68k_015482:
        cmp.b 0x2(%a0),%d3
m68k_015482_end:
.org 0x15486
m68k_015486:
        beq.b (. + 50)
m68k_015486_end:
.org 0x15488
m68k_015488:
        cmp.b 0x1(%a0),%d0
m68k_015488_end:
.org 0x1548C
m68k_01548c:
        bne.b (. + 18)
m68k_01548c_end:
.org 0x1548E
m68k_01548e:
        cmp.b 0x2(%a0),%d5
m68k_01548e_end:
.org 0x15492
m68k_015492:
        beq.w (. + 38)
m68k_015492_end:
.org 0x15496
m68k_015496:
        cmp.b 0x2(%a0),%d4
m68k_015496_end:
.org 0x1549A
m68k_01549a:
        beq.w (. + 30)
m68k_01549a_end:
.org 0x1549E
m68k_01549e:
        cmp.b 0x1(%a0),%d2
m68k_01549e_end:
.org 0x154A2
m68k_0154a2:
        bne.b (. + 10)
m68k_0154a2_end:
.org 0x154A4
m68k_0154a4:
        cmp.b 0x2(%a0),%d3
m68k_0154a4_end:
.org 0x154A8
m68k_0154a8:
        beq.w (. + 16)
m68k_0154a8_end:
.org 0x154AC
m68k_0154ac:
        swap %d0
m68k_0154ac_end:
.org 0x154AE
m68k_0154ae:
        subq.w #0x4,%a0
m68k_0154ae_end:
.org 0x154B0
m68k_0154b0:
        dbra %d0,(. + -84)
m68k_0154b0_end:
.org 0x154B4
m68k_0154b4:
        bra.w (. + 14)
m68k_0154b4_end:
.org 0x154B8
m68k_0154b8:
        bsr.w (. + 16)
m68k_0154b8_end:
.org 0x154BC
m68k_0154bc:
        ori.w #0x1,%sr
m68k_0154bc_end:
.org 0x154C0
m68k_0154c0:
        bra.b (. + 6)
m68k_0154c0_end:
.org 0x154C2
m68k_0154c2:
        andi.w #0xfffe,%sr
m68k_0154c2_end:
.org 0x154C6
m68k_0154c6:
        rts
m68k_0154c6_end:
.org 0x154C8
m68k_0154c8:
        movea.l 0xff382c:l,%a1
m68k_0154c8_end:
.org 0x154CE
m68k_0154ce:
        move.b (%a0),%d0
m68k_0154ce_end:
.org 0x154D0
m68k_0154d0:
        andi.w #0x3,%d0
m68k_0154d0_end:
.org 0x154D4
m68k_0154d4:
        cmpi.b #0x2,%d0
m68k_0154d4_end:
.org 0x154D8
m68k_0154d8:
        beq.b (. + 86)
m68k_0154d8_end:
.org 0x154DA
m68k_0154da:
        move.b 0x5(%a1),%d1
m68k_0154da_end:
.org 0x154DE
m68k_0154de:
        lsl.w #0x8,%d1
m68k_0154de_end:
.org 0x154E0
m68k_0154e0:
        move.b 0x6(%a1),%d1
m68k_0154e0_end:
.org 0x154E4
m68k_0154e4:
        lsl.l #0x8,%d1
m68k_0154e4_end:
.org 0x154E6
m68k_0154e6:
        move.b 0x7(%a1),%d1
m68k_0154e6_end:
.org 0x154EA
m68k_0154ea:
        lsl.l #0x8,%d1
m68k_0154ea_end:
.org 0x154EC
m68k_0154ec:
        move.b 0x8(%a1),%d1
m68k_0154ec_end:
.org 0x154F0
m68k_0154f0:
        addi.l #0x2710,%d1
m68k_0154f0_end:
.org 0x154F6
m68k_0154f6:
        cmpi.l #0xf423f,%d1
m68k_0154f6_end:
.org 0x154FC
m68k_0154fc:
        bls.b (. + 8)
m68k_0154fc_end:
.org 0x154FE
m68k_0154fe:
        move.l #0xf423f,%d1
m68k_0154fe_end:
.org 0x15504
m68k_015504:
        move.b %d1,0x8(%a1)
m68k_015504_end:
.org 0x15508
m68k_015508:
        lsr.l #0x8,%d1
m68k_015508_end:
.org 0x1550A
m68k_01550a:
        move.b %d1,0x7(%a1)
m68k_01550a_end:
.org 0x1550E
m68k_01550e:
        lsr.l #0x8,%d1
m68k_01550e_end:
.org 0x15510
m68k_015510:
        move.b %d1,0x6(%a1)
m68k_015510_end:
.org 0x15514
m68k_015514:
        lsr.w #0x8,%d1
m68k_015514_end:
.org 0x15516
m68k_015516:
        move.b %d1,0x5(%a1)
m68k_015516_end:
.org 0x1551A
m68k_01551a:
        cmpi.b #0x3,%d0
m68k_01551a_end:
.org 0x1551E
m68k_01551e:
        beq.b (. + 6)
m68k_01551e_end:
.org 0x15520
m68k_015520:
        clr.b (%a0)
m68k_015520_end:
.org 0x15522
m68k_015522:
        bra.b (. + 78)
m68k_015522_end:
.org 0x15524
m68k_015524:
        andi.b #0x80,(%a0)
m68k_015524_end:
.org 0x15528
m68k_015528:
        ori.b #0x2,(%a0)
m68k_015528_end:
.org 0x1552C
m68k_01552c:
        bra.b (. + 68)
m68k_01552c_end:
.org 0x1552E
m68k_01552e:
        move.b 0x9(%a1),%d1
m68k_01552e_end:
.org 0x15532
m68k_015532:
        lsl.w #0x8,%d1
m68k_015532_end:
.org 0x15534
m68k_015534:
        move.b 0xa(%a1),%d1
m68k_015534_end:
.org 0x15538
m68k_015538:
        lsl.l #0x8,%d1
m68k_015538_end:
.org 0x1553A
m68k_01553a:
        move.b 0xb(%a1),%d1
m68k_01553a_end:
.org 0x1553E
m68k_01553e:
        lsl.l #0x8,%d1
m68k_01553e_end:
.org 0x15540
m68k_015540:
        move.b 0xc(%a1),%d1
m68k_015540_end:
.org 0x15544
m68k_015544:
        addi.l #0x2710,%d1
m68k_015544_end:
.org 0x1554A
m68k_01554a:
        cmpi.l #0xf423f,%d1
m68k_01554a_end:
.org 0x15550
m68k_015550:
        bls.b (. + 8)
m68k_015550_end:
.org 0x15552
m68k_015552:
        move.l #0x1869f,%d1
m68k_015552_end:
.org 0x15558
m68k_015558:
        move.b %d1,0xc(%a1)
m68k_015558_end:
.org 0x1555C
m68k_01555c:
        lsr.l #0x8,%d1
m68k_01555c_end:
.org 0x1555E
m68k_01555e:
        move.b %d1,0xb(%a1)
m68k_01555e_end:
.org 0x15562
m68k_015562:
        lsr.l #0x8,%d1
m68k_015562_end:
.org 0x15564
m68k_015564:
        move.b %d1,0xa(%a1)
m68k_015564_end:
.org 0x15568
m68k_015568:
        lsr.w #0x8,%d1
m68k_015568_end:
.org 0x1556A
m68k_01556a:
        move.b %d1,0x9(%a1)
m68k_01556a_end:
.org 0x1556E
m68k_01556e:
        clr.b (%a0)
m68k_01556e_end:
.org 0x15570
m68k_015570:
        rts
m68k_015570_end:
.org 0x15572
m68k_015572:
        movea.l 0xff382c:l,%a1
m68k_015572_end:
.org 0x15578
m68k_015578:
        bsr.w (. + 3932)
m68k_015578_end:
.org 0x1557C
m68k_01557c:
        tst.b %d0
m68k_01557c_end:
.org 0x1557E
m68k_01557e:
        bpl.w (. + 28)
m68k_01557e_end:
.org 0x15582
m68k_015582:
        move.b 0x4(%a1),%d0
m68k_015582_end:
.org 0x15586
m68k_015586:
        lea.l 0xf428:w,%a0
m68k_015586_end:
.org 0x1558A
m68k_01558a:
        move.b %d0,(%a0, %d4.w)
m68k_01558a_end:
.org 0x1558E
m68k_01558e:
        bsr.w (. + 492)
m68k_01558e_end:
.org 0x15592
m68k_015592:
        bsr.w (. + 558)
m68k_015592_end:
.org 0x15596
m68k_015596:
        bra.w (. + 12)
m68k_015596_end:
.org 0x1559A
m68k_01559a:
        cmp.b 0x4(%a1),%d0
m68k_01559a_end:
.org 0x1559E
m68k_01559e:
        bne.w (. + 202)
m68k_01559e_end:
.org 0x155A2
m68k_0155a2:
        move.w %d4,%d0
m68k_0155a2_end:
.org 0x155A4
m68k_0155a4:
        move.w %d4,-(%a7)
m68k_0155a4_end:
.org 0x155A6
m68k_0155a6:
        addq.w #0x1,%d0
m68k_0155a6_end:
.org 0x155A8
m68k_0155a8:
        move.w %d0,0xf364:w
m68k_0155a8_end:
.org 0x155AC
m68k_0155ac:
        move.w #0xffff,0xf630:w
m68k_0155ac_end:
.org 0x155B2
m68k_0155b2:
        jsr 0x5f48:l
m68k_0155b2_end:
.org 0x155B8
m68k_0155b8:
        move.w (%a7)+,%d4
m68k_0155b8_end:
.org 0x155BA
m68k_0155ba:
        cmpi.w #0xa,%d3
m68k_0155ba_end:
.org 0x155BE
m68k_0155be:
        bcc.w (. + 150)
m68k_0155be_end:
.org 0x155C2
m68k_0155c2:
        movea.l 0xff382c:l,%a0
m68k_0155c2_end:
.org 0x155C8
m68k_0155c8:
        move.b 0x4(%a0),0xf377:w
m68k_0155c8_end:
.org 0x155CE
m68k_0155ce:
        move.b (%a0),%d1
m68k_0155ce_end:
.org 0x155D0
m68k_0155d0:
        andi.w #0xf,%d1
m68k_0155d0_end:
.org 0x155D4
m68k_0155d4:
        add.w %d1,%d3
m68k_0155d4_end:
.org 0x155D6
m68k_0155d6:
        cmpi.w #0xa,%d3
m68k_0155d6_end:
.org 0x155DA
m68k_0155da:
        bhi.w (. + 60)
m68k_0155da_end:
.org 0x155DE
m68k_0155de:
        bsr.w (. + 210)
m68k_0155de_end:
.org 0x155E2
m68k_0155e2:
        bsr.w (. + 314)
m68k_0155e2_end:
.org 0x155E6
m68k_0155e6:
        bsr.w (. + 370)
m68k_0155e6_end:
.org 0x155EA
m68k_0155ea:
        lea.l 0xf45e:w,%a0
m68k_0155ea_end:
.org 0x155EE
m68k_0155ee:
        move.w 0xf364:w,%d0
m68k_0155ee_end:
.org 0x155F2
m68k_0155f2:
        lsl.w #0x1,%d0
m68k_0155f2_end:
.org 0x155F4
m68k_0155f4:
        tst.w (%a0, %d0.w)
m68k_0155f4_end:
.org 0x155F8
m68k_0155f8:
        bpl.w (. + 92)
m68k_0155f8_end:
.org 0x155FC
m68k_0155fc:
        move.w 0xf364:w,%d0
m68k_0155fc_end:
.org 0x15600
m68k_015600:
        move.w #0xffff,0xf630:w
m68k_015600_end:
.org 0x15606
m68k_015606:
        jsr 0x5f48:l
m68k_015606_end:
.org 0x1560C
m68k_01560c:
        jsr 0xe1f6:l
m68k_01560c_end:
.org 0x15612
m68k_015612:
        bra.w (. + 66)
m68k_015612_end:
.org 0x15616
m68k_015616:
        move.b 0x4(%a0),%d0
m68k_015616_end:
.org 0x1561A
m68k_01561a:
        cmp.b 0xf67b:w,%d0
m68k_01561a_end:
.org 0x1561E
m68k_01561e:
        beq.w (. + 20)
m68k_01561e_end:
.org 0x15622
m68k_015622:
        cmp.b 0xf67d:w,%d0
m68k_015622_end:
.org 0x15626
m68k_015626:
        beq.w (. + 12)
m68k_015626_end:
.org 0x1562A
m68k_01562a:
        cmp.b 0xf67f:w,%d0
m68k_01562a_end:
.org 0x1562E
m68k_01562e:
        bne.w (. + 46)
m68k_01562e_end:
.org 0x15632
m68k_015632:
        bsr.w (. + 826)
m68k_015632_end:
.org 0x15636
m68k_015636:
        move.w %d0,0xf364:w
m68k_015636_end:
.org 0x1563A
m68k_01563a:
        subi.w #0xa,%d3
m68k_01563a_end:
.org 0x1563E
m68k_01563e:
        sub.w %d3,%d1
m68k_01563e_end:
.org 0x15640
m68k_015640:
        beq.w (. + 20)
m68k_015640_end:
.org 0x15644
m68k_015644:
        move.w %d1,0xf686:w
m68k_015644_end:
.org 0x15648
m68k_015648:
        addq.w #0x1,0xf362:w
m68k_015648_end:
.org 0x1564C
m68k_01564c:
        ori.w #0x1,%sr
m68k_01564c_end:
.org 0x15650
m68k_015650:
        bra.w (. + 94)
m68k_015650_end:
.org 0x15654
m68k_015654:
        andi.w #0xfffe,%sr
m68k_015654_end:
.org 0x15658
m68k_015658:
        bra.w (. + 86)
m68k_015658_end:
.org 0x1565C
m68k_01565c:
        bsr.w (. + 380)
m68k_01565c_end:
.org 0x15660
m68k_015660:
        andi.w #0xfffe,%sr
m68k_015660_end:
.org 0x15664
m68k_015664:
        bra.w (. + 74)
m68k_015664_end:
.org 0x15668
m68k_015668:
        cmpi.w #0x10,%d0
m68k_015668_end:
.org 0x1566C
m68k_01566c:
        beq.w (. + 66)
m68k_01566c_end:
.org 0x15670
m68k_015670:
        clr.w 0xf376:w
m68k_015670_end:
.org 0x15674
m68k_015674:
        move.b 0x4(%a1),0xf377:w
m68k_015674_end:
.org 0x1567A
m68k_01567a:
        move.w 0xf376:w,%d0
m68k_01567a_end:
.org 0x1567E
m68k_01567e:
        cmp.w 0xf67a:w,%d0
m68k_01567e_end:
.org 0x15682
m68k_015682:
        beq.w (. + 18)
m68k_015682_end:
.org 0x15686
m68k_015686:
        cmp.w 0xf67c:w,%d0
m68k_015686_end:
.org 0x1568A
m68k_01568a:
        beq.w (. + 10)
m68k_01568a_end:
.org 0x1568E
m68k_01568e:
        cmp.w 0xf67e:w,%d0
m68k_01568e_end:
.org 0x15692
m68k_015692:
        bne.b (. + -62)
m68k_015692_end:
.org 0x15694
m68k_015694:
        lea.l 0xea37:w,%a1
m68k_015694_end:
.org 0x15698
m68k_015698:
        move.w 0xf392:w,%d0
m68k_015698_end:
.org 0x1569C
m68k_01569c:
        btst.b #0x1,(%a1, %d0.w)
m68k_01569c_end:
.org 0x156A2
m68k_0156a2:
        bne.b (. + -78)
m68k_0156a2_end:
.org 0x156A4
m68k_0156a4:
        move.w #0xc,0xf362:w
m68k_0156a4_end:
.org 0x156AA
m68k_0156aa:
        ori.w #0x1,%sr
m68k_0156aa_end:
.org 0x156AE
m68k_0156ae:
        rts
m68k_0156ae_end:
.org 0x156B0
m68k_0156b0:
        move.w %d0,%d4
m68k_0156b0_end:
.org 0x156B2
m68k_0156b2:
        lsl.w #0x2,%d4
m68k_0156b2_end:
.org 0x156B4
m68k_0156b4:
        lea.l 0xdffc:w,%a4
m68k_0156b4_end:
.org 0x156B8
m68k_0156b8:
        move.b 0x5(%a0),%d5
m68k_0156b8_end:
.org 0x156BC
m68k_0156bc:
        lsl.w #0x8,%d5
m68k_0156bc_end:
.org 0x156BE
m68k_0156be:
        move.b 0x6(%a0),%d5
m68k_0156be_end:
.org 0x156C2
m68k_0156c2:
        lsl.l #0x8,%d5
m68k_0156c2_end:
.org 0x156C4
m68k_0156c4:
        move.b 0x7(%a0),%d5
m68k_0156c4_end:
.org 0x156C8
m68k_0156c8:
        lsl.l #0x8,%d5
m68k_0156c8_end:
.org 0x156CA
m68k_0156ca:
        move.b 0x8(%a0),%d5
m68k_0156ca_end:
.org 0x156CE
m68k_0156ce:
        add.l (%a4, %d4.w),%d5
m68k_0156ce_end:
.org 0x156D2
m68k_0156d2:
        bcs.b (. + 10)
m68k_0156d2_end:
.org 0x156D4
m68k_0156d4:
        cmpi.l #0xf423f,%d5
m68k_0156d4_end:
.org 0x156DA
m68k_0156da:
        bls.b (. + 8)
m68k_0156da_end:
.org 0x156DC
m68k_0156dc:
        move.l #0xf423f,%d5
m68k_0156dc_end:
.org 0x156E2
m68k_0156e2:
        move.l %d5,(%a4, %d4.w)
m68k_0156e2_end:
.org 0x156E6
m68k_0156e6:
        move.b 0x9(%a0),%d5
m68k_0156e6_end:
.org 0x156EA
m68k_0156ea:
        lsl.w #0x8,%d5
m68k_0156ea_end:
.org 0x156EC
m68k_0156ec:
        move.b 0xa(%a0),%d5
m68k_0156ec_end:
.org 0x156F0
m68k_0156f0:
        lsl.l #0x8,%d5
m68k_0156f0_end:
.org 0x156F2
m68k_0156f2:
        move.b 0xb(%a0),%d5
m68k_0156f2_end:
.org 0x156F6
m68k_0156f6:
        lsl.l #0x8,%d5
m68k_0156f6_end:
.org 0x156F8
m68k_0156f8:
        move.b 0xc(%a0),%d5
m68k_0156f8_end:
.org 0x156FC
m68k_0156fc:
        lea.l 0xe09c:w,%a4
m68k_0156fc_end:
.org 0x15700
m68k_015700:
        add.l (%a4, %d4.w),%d5
m68k_015700_end:
.org 0x15704
m68k_015704:
        bcs.w (. + 12)
m68k_015704_end:
.org 0x15708
m68k_015708:
        cmpi.l #0xf423f,%d5
m68k_015708_end:
.org 0x1570E
m68k_01570e:
        bls.b (. + 8)
m68k_01570e_end:
.org 0x15710
m68k_015710:
        move.l #0xf423f,%d5
m68k_015710_end:
.org 0x15716
m68k_015716:
        move.l %d5,(%a4, %d4.w)
m68k_015716_end:
.org 0x1571A
m68k_01571a:
        rts
m68k_01571a_end:
.org 0x1571C
m68k_01571c:
        lea.l 0xcc00:w,%a1
m68k_01571c_end:
.org 0x15720
m68k_015720:
        lea.l (%a0),%a3
m68k_015720_end:
.org 0x15722
m68k_015722:
        adda.w #0xd,%a3
m68k_015722_end:
.org 0x15726
m68k_015726:
        move.w %d1,%d3
m68k_015726_end:
.org 0x15728
m68k_015728:
        subq.w #0x1,%d3
m68k_015728_end:
.org 0x1572A
m68k_01572a:
        clr.w %d2
m68k_01572a_end:
.org 0x1572C
m68k_01572c:
        clr.w %d4
m68k_01572c_end:
.org 0x1572E
m68k_01572e:
        move.b 0x4(%a0),%d4
m68k_01572e_end:
.org 0x15732
m68k_015732:
        lsl.w #0x1,%d4
m68k_015732_end:
.org 0x15734
m68k_015734:
        lea.l 0xe640:w,%a2
m68k_015734_end:
.org 0x15738
m68k_015738:
        move.w (%a2, %d4.w),%d4
m68k_015738_end:
.org 0x1573C
m68k_01573c:
        lea.l 0xf45e:w,%a2
m68k_01573c_end:
.org 0x15740
m68k_015740:
        move.b (%a3)+,%d2
m68k_015740_end:
.org 0x15742
m68k_015742:
        move.b %d0,(%a1, %d2.w)
m68k_015742_end:
.org 0x15746
m68k_015746:
        cmp.b %d2,%d4
m68k_015746_end:
.org 0x15748
m68k_015748:
        bne.b (. + 10)
m68k_015748_end:
.org 0x1574A
m68k_01574a:
        move.w %d0,%d2
m68k_01574a_end:
.org 0x1574C
m68k_01574c:
        lsl.w #0x1,%d2
m68k_01574c_end:
.org 0x1574E
m68k_01574e:
        move.w %d4,(%a2, %d2.w)
m68k_01574e_end:
.org 0x15752
m68k_015752:
        dbra %d3,(. + -18)
m68k_015752_end:
.org 0x15756
m68k_015756:
        rts
m68k_015756_end:
.org 0x15758
m68k_015758:
        lea.l 0xd(%a0, %d1.w),%a1
m68k_015758_end:
.org 0x1575C
m68k_01575c:
        move.b (%a1),%d0
m68k_01575c_end:
.org 0x1575E
m68k_01575e:
        andi.w #0xf,%d0
m68k_01575e_end:
.org 0x15762
m68k_015762:
        beq.b (. + 14)
m68k_015762_end:
.org 0x15764
m68k_015764:
        addi.w #0xc,%d0
m68k_015764_end:
.org 0x15768
m68k_015768:
        move.b (%a1)+,(%a0)+
m68k_015768_end:
.org 0x1576A
m68k_01576a:
        dbra %d0,(. + -2)
m68k_01576a_end:
.org 0x1576E
m68k_01576e:
        bra.b (. + -18)
m68k_01576e_end:
.org 0x15770
m68k_015770:
        clr.b (%a0)
m68k_015770_end:
.org 0x15772
m68k_015772:
        clr.l 0xff382c:l
m68k_015772_end:
.org 0x15778
m68k_015778:
        rts
m68k_015778_end:
.org 0x1577A
m68k_01577a:
        movem.l %d0-%d2/%d4/%a0,-(%a7)
m68k_01577a_end:
.org 0x1577E
m68k_01577e:
        lea.l 0xe640:w,%a0
m68k_01577e_end:
.org 0x15782
m68k_015782:
        lsl.w #0x1,%d0
m68k_015782_end:
.org 0x15784
m68k_015784:
        move.w (%a0, %d0.w),%d0
m68k_015784_end:
.org 0x15788
m68k_015788:
        lea.l 0xc200:w,%a0
m68k_015788_end:
.org 0x1578C
m68k_01578c:
        clr.w %d2
m68k_01578c_end:
.org 0x1578E
m68k_01578e:
        move.b (%a0, %d0.w),%d2
m68k_01578e_end:
.org 0x15792
m68k_015792:
        jsr 0x83d4:l
m68k_015792_end:
.org 0x15798
m68k_015798:
        andi.l #0xffff,%d0
m68k_015798_end:
.org 0x1579E
m68k_01579e:
        move.l %d0,%d1
m68k_01579e_end:
.org 0x157A0
m68k_0157a0:
        lsl.l #0x1,%d0
m68k_0157a0_end:
.org 0x157A2
m68k_0157a2:
        add.l %d1,%d0
m68k_0157a2_end:
.org 0x157A4
m68k_0157a4:
        swap %d0
m68k_0157a4_end:
.org 0x157A6
m68k_0157a6:
        addi.w #0x6,%d0
m68k_0157a6_end:
.org 0x157AA
m68k_0157aa:
        mulu.w %d0,%d2
m68k_0157aa_end:
.org 0x157AC
m68k_0157ac:
        divu.w #0xa,%d2
m68k_0157ac_end:
.org 0x157B0
m68k_0157b0:
        lea.l 0xe320:w,%a0
m68k_0157b0_end:
.org 0x157B4
m68k_0157b4:
        lsl.w #0x2,%d4
m68k_0157b4_end:
.org 0x157B6
m68k_0157b6:
        move.w %d2,0x2(%a0, %d4.w)
m68k_0157b6_end:
.org 0x157BA
m68k_0157ba:
        movem.l (%a7)+,%d0-%d2/%d4/%a0
m68k_0157ba_end:
.org 0x157BE
m68k_0157be:
        rts
m68k_0157be_end:
.org 0x157C0
m68k_0157c0:
        movem.l %d0/%a0,-(%a7)
m68k_0157c0_end:
.org 0x157C4
m68k_0157c4:
        lea.l 0xe774:w,%a0
m68k_0157c4_end:
.org 0x157C8
m68k_0157c8:
        move.w 0xf392:w,%d0
m68k_0157c8_end:
.org 0x157CC
m68k_0157cc:
        lsl.w #0x2,%d0
m68k_0157cc_end:
.org 0x157CE
m68k_0157ce:
        clr.l (%a0, %d0.w)
m68k_0157ce_end:
.org 0x157D2
m68k_0157d2:
        movem.l (%a7)+,%d0/%a0
m68k_0157d2_end:
.org 0x157D6
m68k_0157d6:
        rts
m68k_0157d6_end:
.org 0x157D8
m68k_0157d8:
        addq.w #0x1,%d4
m68k_0157d8_end:
.org 0x157DA
m68k_0157da:
        bsr.w (. + 26)
m68k_0157da_end:
.org 0x157DE
m68k_0157de:
        bsr.w (. + 54)
m68k_0157de_end:
.org 0x157E2
m68k_0157e2:
        bsr.w (. + 118)
m68k_0157e2_end:
.org 0x157E6
m68k_0157e6:
        bsr.w (. + 186)
m68k_0157e6_end:
.org 0x157EA
m68k_0157ea:
        bsr.w (. + 234)
m68k_0157ea_end:
.org 0x157EE
m68k_0157ee:
        bsr.w (. + 340)
m68k_0157ee_end:
.org 0x157F2
m68k_0157f2:
        rts
m68k_0157f2_end:
.org 0x157F4
m68k_0157f4:
        lea.l 0xd300:w,%a1
m68k_0157f4_end:
.org 0x157F8
m68k_0157f8:
        move.b (%a0),%d0
m68k_0157f8_end:
.org 0x157FA
m68k_0157fa:
        andi.w #0xf,%d0
m68k_0157fa_end:
.org 0x157FE
m68k_0157fe:
        move.w %d0,%d1
m68k_0157fe_end:
.org 0x15800
m68k_015800:
        subq.w #0x1,%d1
m68k_015800_end:
.org 0x15802
m68k_015802:
        clr.w %d2
m68k_015802_end:
.org 0x15804
m68k_015804:
        move.b 0xd(%a0, %d1.w),%d2
m68k_015804_end:
.org 0x15808
m68k_015808:
        move.w %d2,(%a1)+
m68k_015808_end:
.org 0x1580A
m68k_01580a:
        dbra %d1,(. + -6)
m68k_01580a_end:
.org 0x1580E
m68k_01580e:
        move.w #0xffff,(%a1)
m68k_01580e_end:
.org 0x15812
m68k_015812:
        rts
m68k_015812_end:
.org 0x15814
m68k_015814:
        clr.w %d1
m68k_015814_end:
.org 0x15816
m68k_015816:
        move.b 0x4(%a0),%d1
m68k_015816_end:
.org 0x1581A
m68k_01581a:
        lsl.w #0x1,%d1
m68k_01581a_end:
.org 0x1581C
m68k_01581c:
        lea.l 0xe640:w,%a1
m68k_01581c_end:
.org 0x15820
m68k_015820:
        move.w (%a1, %d1.w),%d1
m68k_015820_end:
.org 0x15824
m68k_015824:
        lea.l 0xd300:w,%a1
m68k_015824_end:
.org 0x15828
m68k_015828:
        lea.l 0xd316:w,%a2
m68k_015828_end:
.org 0x1582C
m68k_01582c:
        lea.l 0xd32c:w,%a3
m68k_01582c_end:
.org 0x15830
m68k_015830:
        move.w (%a1)+,%d2
m68k_015830_end:
.org 0x15832
m68k_015832:
        bmi.w (. + 32)
m68k_015832_end:
.org 0x15836
m68k_015836:
        cmp.w %d1,%d2
m68k_015836_end:
.org 0x15838
m68k_015838:
        bne.b (. + -8)
m68k_015838_end:
.org 0x1583A
m68k_01583a:
        move.w %d1,(%a2)+
m68k_01583a_end:
.org 0x1583C
m68k_01583c:
        move.w #0x64,(%a3)+
m68k_01583c_end:
.org 0x15840
m68k_015840:
        move.w (%a1)+,-0x4(%a1)
m68k_015840_end:
.org 0x15844
m68k_015844:
        bpl.b (. + -4)
m68k_015844_end:
.org 0x15846
m68k_015846:
        move.w %d4,%d2
m68k_015846_end:
.org 0x15848
m68k_015848:
        lsl.w #0x1,%d2
m68k_015848_end:
.org 0x1584A
m68k_01584a:
        lea.l 0xf45e:w,%a1
m68k_01584a_end:
.org 0x1584E
m68k_01584e:
        move.w %d1,(%a1, %d2.w)
m68k_01584e_end:
.org 0x15852
m68k_015852:
        move.w #0xffff,(%a2)
m68k_015852_end:
.org 0x15856
m68k_015856:
        rts
m68k_015856_end:
.org 0x15858
m68k_015858:
        lea.l 0xd300:w,%a1
m68k_015858_end:
.org 0x1585C
m68k_01585c:
        lea.l 0xc300:w,%a4
m68k_01585c_end:
.org 0x15860
m68k_015860:
        clr.w %d2
m68k_015860_end:
.org 0x15862
m68k_015862:
        move.w (%a1)+,%d1
m68k_015862_end:
.org 0x15864
m68k_015864:
        bmi.w (. + 58)
m68k_015864_end:
.org 0x15868
m68k_015868:
        move.b (%a4, %d1.w),%d2
m68k_015868_end:
.org 0x1586C
m68k_01586c:
        lea.l 0xd316:w,%a2
m68k_01586c_end:
.org 0x15870
m68k_015870:
        lea.l 0xd32c:w,%a3
m68k_015870_end:
.org 0x15874
m68k_015874:
        tst.w (%a2)
m68k_015874_end:
.org 0x15876
m68k_015876:
        bmi.w (. + 16)
m68k_015876_end:
.org 0x1587A
m68k_01587a:
        cmp.w (%a3),%d2
m68k_01587a_end:
.org 0x1587C
m68k_01587c:
        bhi.w (. + 10)
m68k_01587c_end:
.org 0x15880
m68k_015880:
        addq.w #0x2,%a2
m68k_015880_end:
.org 0x15882
m68k_015882:
        addq.w #0x2,%a3
m68k_015882_end:
.org 0x15884
m68k_015884:
        bra.b (. + -16)
m68k_015884_end:
.org 0x15886
m68k_015886:
        move.w (%a2),%d5
m68k_015886_end:
.org 0x15888
m68k_015888:
        move.w (%a3),%d6
m68k_015888_end:
.org 0x1588A
m68k_01588a:
        move.w %d1,(%a2)+
m68k_01588a_end:
.org 0x1588C
m68k_01588c:
        move.w %d2,(%a3)+
m68k_01588c_end:
.org 0x1588E
m68k_01588e:
        move.w %d5,%d1
m68k_01588e_end:
.org 0x15890
m68k_015890:
        bmi.w (. + 8)
m68k_015890_end:
.org 0x15894
m68k_015894:
        move.w %d6,%d2
m68k_015894_end:
.org 0x15896
m68k_015896:
        bra.b (. + -16)
m68k_015896_end:
.org 0x15898
m68k_015898:
        move.w #0xffff,(%a2)
m68k_015898_end:
.org 0x1589C
m68k_01589c:
        bra.b (. + -58)
m68k_01589c_end:
.org 0x1589E
m68k_01589e:
        rts
m68k_01589e_end:
.org 0x158A0
m68k_0158a0:
        move.b (%a0),%d0
m68k_0158a0_end:
.org 0x158A2
m68k_0158a2:
        andi.w #0xf,%d0
m68k_0158a2_end:
.org 0x158A6
m68k_0158a6:
        subi.w #0x9,%d3
m68k_0158a6_end:
.org 0x158AA
m68k_0158aa:
        sub.w %d3,%d0
m68k_0158aa_end:
.org 0x158AC
m68k_0158ac:
        lea.l 0xd316:w,%a1
m68k_0158ac_end:
.org 0x158B0
m68k_0158b0:
        lea.l 0xcc00:w,%a2
m68k_0158b0_end:
.org 0x158B4
m68k_0158b4:
        move.w (%a1)+,%d1
m68k_0158b4_end:
.org 0x158B6
m68k_0158b6:
        move.b %d4,(%a2, %d1.w)
m68k_0158b6_end:
.org 0x158BA
m68k_0158ba:
        dbra %d0,(. + -6)
m68k_0158ba_end:
.org 0x158BE
m68k_0158be:
        bset.l #0x7,%d4
m68k_0158be_end:
.org 0x158C2
m68k_0158c2:
        move.w (%a1)+,%d1
m68k_0158c2_end:
.org 0x158C4
m68k_0158c4:
        bmi.w (. + 10)
m68k_0158c4_end:
.org 0x158C8
m68k_0158c8:
        move.b %d4,(%a2, %d1.w)
m68k_0158c8_end:
.org 0x158CC
m68k_0158cc:
        bra.b (. + -10)
m68k_0158cc_end:
.org 0x158CE
m68k_0158ce:
        bclr.l #0x7,%d4
m68k_0158ce_end:
.org 0x158D2
m68k_0158d2:
        rts
m68k_0158d2_end:
.org 0x158D4
m68k_0158d4:
        move.w %d4,%d1
m68k_0158d4_end:
.org 0x158D6
m68k_0158d6:
        lsl.w #0x2,%d1
m68k_0158d6_end:
.org 0x158D8
m68k_0158d8:
        move.b 0x5(%a0),%d0
m68k_0158d8_end:
.org 0x158DC
m68k_0158dc:
        lsl.w #0x8,%d0
m68k_0158dc_end:
.org 0x158DE
m68k_0158de:
        move.b 0x6(%a0),%d0
m68k_0158de_end:
.org 0x158E2
m68k_0158e2:
        lsl.l #0x8,%d0
m68k_0158e2_end:
.org 0x158E4
m68k_0158e4:
        move.b 0x7(%a0),%d0
m68k_0158e4_end:
.org 0x158E8
m68k_0158e8:
        lsl.l #0x8,%d0
m68k_0158e8_end:
.org 0x158EA
m68k_0158ea:
        move.b 0x8(%a0),%d0
m68k_0158ea_end:
.org 0x158EE
m68k_0158ee:
        lea.l 0xdffc:w,%a1
m68k_0158ee_end:
.org 0x158F2
m68k_0158f2:
        move.l (%a1, %d1.w),%d2
m68k_0158f2_end:
.org 0x158F6
m68k_0158f6:
        add.l %d0,%d2
m68k_0158f6_end:
.org 0x158F8
m68k_0158f8:
        cmpi.l #0xf423f,%d2
m68k_0158f8_end:
.org 0x158FE
m68k_0158fe:
        bls.w (. + 10)
m68k_0158fe_end:
.org 0x15902
m68k_015902:
        move.l #0xf423f,%d2
m68k_015902_end:
.org 0x15908
m68k_015908:
        move.l %d2,(%a1, %d1.w)
m68k_015908_end:
.org 0x1590C
m68k_01590c:
        move.b 0x9(%a0),%d0
m68k_01590c_end:
.org 0x15910
m68k_015910:
        lsl.w #0x8,%d0
m68k_015910_end:
.org 0x15912
m68k_015912:
        move.b 0xa(%a0),%d0
m68k_015912_end:
.org 0x15916
m68k_015916:
        lsl.l #0x8,%d0
m68k_015916_end:
.org 0x15918
m68k_015918:
        move.b 0xb(%a0),%d0
m68k_015918_end:
.org 0x1591C
m68k_01591c:
        lsl.l #0x8,%d0
m68k_01591c_end:
.org 0x1591E
m68k_01591e:
        move.b 0xc(%a0),%d0
m68k_01591e_end:
.org 0x15922
m68k_015922:
        lea.l 0xe09c:w,%a1
m68k_015922_end:
.org 0x15926
m68k_015926:
        move.l (%a1, %d1.w),%d2
m68k_015926_end:
.org 0x1592A
m68k_01592a:
        add.l %d0,%d2
m68k_01592a_end:
.org 0x1592C
m68k_01592c:
        cmpi.l #0xf423f,%d2
m68k_01592c_end:
.org 0x15932
m68k_015932:
        bls.w (. + 10)
m68k_015932_end:
.org 0x15936
m68k_015936:
        move.l #0xf423f,%d2
m68k_015936_end:
.org 0x1593C
m68k_01593c:
        move.l %d2,(%a1, %d1.w)
m68k_01593c_end:
.org 0x15940
m68k_015940:
        rts
m68k_015940_end:
.org 0x15942
m68k_015942:
        move.b (%a0),%d0
m68k_015942_end:
.org 0x15944
m68k_015944:
        andi.w #0xf,%d0
m68k_015944_end:
.org 0x15948
m68k_015948:
        lea.l 0xd(%a0, %d0.w),%a1
m68k_015948_end:
.org 0x1594C
m68k_01594c:
        move.b (%a1),%d0
m68k_01594c_end:
.org 0x1594E
m68k_01594e:
        andi.w #0xf,%d0
m68k_01594e_end:
.org 0x15952
m68k_015952:
        beq.w (. + 16)
m68k_015952_end:
.org 0x15956
m68k_015956:
        addi.w #0xc,%d0
m68k_015956_end:
.org 0x1595A
m68k_01595a:
        move.b (%a1)+,(%a0)+
m68k_01595a_end:
.org 0x1595C
m68k_01595c:
        dbra %d0,(. + -2)
m68k_01595c_end:
.org 0x15960
m68k_015960:
        bra.b (. + -20)
m68k_015960_end:
.org 0x15962
m68k_015962:
        clr.b (%a0)
m68k_015962_end:
.org 0x15964
m68k_015964:
        clr.l 0xff382c:l
m68k_015964_end:
.org 0x1596A
m68k_01596a:
        rts
m68k_01596a_end:
.org 0x1596C
m68k_01596c:
        movem.l %d0-%d2/%a1,-(%a7)
m68k_01596c_end:
.org 0x15970
m68k_015970:
        move.b (%a0),%d0
m68k_015970_end:
.org 0x15972
m68k_015972:
        andi.w #0xf,%d0
m68k_015972_end:
.org 0x15976
m68k_015976:
        subq.w #0x1,%d0
m68k_015976_end:
.org 0x15978
m68k_015978:
        clr.w %d1
m68k_015978_end:
.org 0x1597A
m68k_01597a:
        move.b 0x4(%a0),%d1
m68k_01597a_end:
.org 0x1597E
m68k_01597e:
        lsl.w #0x1,%d1
m68k_01597e_end:
.org 0x15980
m68k_015980:
        lea.l 0xe640:w,%a1
m68k_015980_end:
.org 0x15984
m68k_015984:
        move.w (%a1, %d1.w),%d1
m68k_015984_end:
.org 0x15988
m68k_015988:
        clr.w %d2
m68k_015988_end:
.org 0x1598A
m68k_01598a:
        cmp.b 0xd(%a0, %d2.w),%d1
m68k_01598a_end:
.org 0x1598E
m68k_01598e:
        beq.w (. + 20)
m68k_01598e_end:
.org 0x15992
m68k_015992:
        addq.w #0x1,%d2
m68k_015992_end:
.org 0x15994
m68k_015994:
        cmp.w %d0,%d2
m68k_015994_end:
.org 0x15996
m68k_015996:
        bcs.b (. + -12)
m68k_015996_end:
.org 0x15998
m68k_015998:
        bra.w (. + 76)
m68k_015998_end:
.org 0x1599C
m68k_01599c:
        move.b 0xd(%a0, %d2.w),0xc(%a0, %d2.w)
m68k_01599c_end:
.org 0x159A2
m68k_0159a2:
        addq.w #0x1,%d2
m68k_0159a2_end:
.org 0x159A4
m68k_0159a4:
        cmp.w %d0,%d2
m68k_0159a4_end:
.org 0x159A6
m68k_0159a6:
        bcs.b (. + -10)
m68k_0159a6_end:
.org 0x159A8
m68k_0159a8:
        move.b 0xd(%a0, %d2.w),%d0
m68k_0159a8_end:
.org 0x159AC
m68k_0159ac:
        andi.w #0xf,%d0
m68k_0159ac_end:
.org 0x159B0
m68k_0159b0:
        beq.w (. + 22)
m68k_0159b0_end:
.org 0x159B4
m68k_0159b4:
        addi.w #0xc,%d0
m68k_0159b4_end:
.org 0x159B8
m68k_0159b8:
        move.b 0xd(%a0, %d2.w),0xc(%a0, %d2.w)
m68k_0159b8_end:
.org 0x159BE
m68k_0159be:
        addq.w #0x1,%d2
m68k_0159be_end:
.org 0x159C0
m68k_0159c0:
        dbra %d0,(. + -8)
m68k_0159c0_end:
.org 0x159C4
m68k_0159c4:
        bra.b (. + -28)
m68k_0159c4_end:
.org 0x159C6
m68k_0159c6:
        clr.b 0xc(%a0, %d2.w)
m68k_0159c6_end:
.org 0x159CA
m68k_0159ca:
        subq.b #0x1,(%a0)
m68k_0159ca_end:
.org 0x159CC
m68k_0159cc:
        lea.l 0xcc00:w,%a1
m68k_0159cc_end:
.org 0x159D0
m68k_0159d0:
        move.b %d4,%d2
m68k_0159d0_end:
.org 0x159D2
m68k_0159d2:
        addq.w #0x1,%d2
m68k_0159d2_end:
.org 0x159D4
m68k_0159d4:
        move.b %d2,(%a1, %d1.w)
m68k_0159d4_end:
.org 0x159D8
m68k_0159d8:
        lsl.w #0x1,%d2
m68k_0159d8_end:
.org 0x159DA
m68k_0159da:
        lea.l 0xf45e:w,%a1
m68k_0159da_end:
.org 0x159DE
m68k_0159de:
        move.w %d1,(%a1, %d2.w)
m68k_0159de_end:
.org 0x159E2
m68k_0159e2:
        addq.w #0x1,%d3
m68k_0159e2_end:
.org 0x159E4
m68k_0159e4:
        movem.l (%a7)+,%d0-%d2/%a1
m68k_0159e4_end:
.org 0x159E8
m68k_0159e8:
        rts
m68k_0159e8_end:
.org 0x159EA
m68k_0159ea:
        movea.l 0xff382c:l,%a0
m68k_0159ea_end:
.org 0x159F0
m68k_0159f0:
        move.b (%a0),%d0
m68k_0159f0_end:
.org 0x159F2
m68k_0159f2:
        andi.w #0xf,%d0
m68k_0159f2_end:
.org 0x159F6
m68k_0159f6:
        subq.w #0x1,%d0
m68k_0159f6_end:
.org 0x159F8
m68k_0159f8:
        lea.l 0xc000:w,%a1
m68k_0159f8_end:
.org 0x159FC
m68k_0159fc:
        lea.l 0xd(%a0),%a0
m68k_0159fc_end:
.org 0x15A00
m68k_015a00:
        clr.w %d1
m68k_015a00_end:
.org 0x15A02
m68k_015a02:
        move.b (%a0)+,%d1
m68k_015a02_end:
.org 0x15A04
m68k_015a04:
        lsl.w #0x1,%d1
m68k_015a04_end:
.org 0x15A06
m68k_015a06:
        cmpi.w #0x3e7,(%a1, %d1.w)
m68k_015a06_end:
.org 0x15A0C
m68k_015a0c:
        bcc.b (. + 8)
m68k_015a0c_end:
.org 0x15A0E
m68k_015a0e:
        addi.w #0x1,(%a1, %d1.w)
m68k_015a0e_end:
.org 0x15A14
m68k_015a14:
        dbra %d0,(. + -20)
m68k_015a14_end:
.org 0x15A18
m68k_015a18:
        rts
m68k_015a18_end:
.org 0x15A1A
m68k_015a1a:
        movea.l 0xff382c:l,%a0
m68k_015a1a_end:
.org 0x15A20
m68k_015a20:
        move.b (%a0),%d0
m68k_015a20_end:
.org 0x15A22
m68k_015a22:
        andi.w #0xf,%d0
m68k_015a22_end:
.org 0x15A26
m68k_015a26:
        move.w %d0,0xf636:w
m68k_015a26_end:
.org 0x15A2A
m68k_015a2a:
        subq.w #0x1,%d0
m68k_015a2a_end:
.org 0x15A2C
m68k_015a2c:
        adda.w #0xd,%a0
m68k_015a2c_end:
.org 0x15A30
m68k_015a30:
        lea.l 0xf500:w,%a1
m68k_015a30_end:
.org 0x15A34
m68k_015a34:
        clr.w %d1
m68k_015a34_end:
.org 0x15A36
m68k_015a36:
        move.b (%a0)+,%d1
m68k_015a36_end:
.org 0x15A38
m68k_015a38:
        move.w %d1,(%a1)+
m68k_015a38_end:
.org 0x15A3A
m68k_015a3a:
        dbra %d0,(. + -4)
m68k_015a3a_end:
.org 0x15A3E
m68k_015a3e:
        move.w #0xffff,(%a1)
m68k_015a3e_end:
.org 0x15A42
m68k_015a42:
        move.w #0x10,0xf65a:w
m68k_015a42_end:
.org 0x15A48
m68k_015a48:
        clr.w 0xf684:w
m68k_015a48_end:
.org 0x15A4C
m68k_015a4c:
        move.w #0xa0,0xf38c:w
m68k_015a4c_end:
.org 0x15A52
m68k_015a52:
        move.w #0x208,0xf612:w
m68k_015a52_end:
.org 0x15A58
m68k_015a58:
        move.w #0x4,0xf362:w
m68k_015a58_end:
.org 0x15A5E
m68k_015a5e:
        rts
m68k_015a5e_end:
.org 0x15A60
m68k_015a60:
        bsr.w (. + 108)
m68k_015a60_end:
.org 0x15A64
m68k_015a64:
        bsr.w (. + 134)
m68k_015a64_end:
.org 0x15A68
m68k_015a68:
        tst.w 0xcfd2:w
m68k_015a68_end:
.org 0x15A6C
m68k_015a6c:
        beq.w (. + 28)
m68k_015a6c_end:
.org 0x15A70
m68k_015a70:
        subq.w #0x1,0xcfd2:w
m68k_015a70_end:
.org 0x15A74
m68k_015a74:
        cmpi.w #0x8,0xcfd2:w
m68k_015a74_end:
.org 0x15A7A
m68k_015a7a:
        bls.w (. + 48)
m68k_015a7a_end:
.org 0x15A7E
m68k_015a7e:
        move.w #0x8,0xcfd2:w
m68k_015a7e_end:
.org 0x15A84
m68k_015a84:
        bra.w (. + 38)
m68k_015a84_end:
.org 0x15A88
m68k_015a88:
        btst.b #0x5,0xf603:w
m68k_015a88_end:
.org 0x15A8E
m68k_015a8e:
        beq.b (. + 28)
m68k_015a8e_end:
.org 0x15A90
m68k_015a90:
        jsr 0xc0b6:l
m68k_015a90_end:
.org 0x15A96
m68k_015a96:
        move.w #0x208,0xf612:w
m68k_015a96_end:
.org 0x15A9C
m68k_015a9c:
        move.w #0x3,0xf362:w
m68k_015a9c_end:
.org 0x15AA2
m68k_015aa2:
        move.w #0x12,0xf36a:w
m68k_015aa2_end:
.org 0x15AA8
m68k_015aa8:
        bra.b (. + 28)
m68k_015aa8_end:
.org 0x15AAA
m68k_015aaa:
        btst.b #0x4,0xf603:w
m68k_015aaa_end:
.org 0x15AB0
m68k_015ab0:
        beq.b (. + 20)
m68k_015ab0_end:
.org 0x15AB2
m68k_015ab2:
        move.w #0x208,0xf612:w
m68k_015ab2_end:
.org 0x15AB8
m68k_015ab8:
        move.w #0x2,0xf362:w
m68k_015ab8_end:
.org 0x15ABE
m68k_015abe:
        move.w #0x12,0xf36a:w
m68k_015abe_end:
.org 0x15AC4
m68k_015ac4:
        jsr 0xa158:l
m68k_015ac4_end:
.org 0x15ACA
m68k_015aca:
        rts
m68k_015aca_end:
.org 0x15ACC
m68k_015acc:
        move.b 0xf603:w,%d0
m68k_015acc_end:
.org 0x15AD0
m68k_015ad0:
        andi.w #0x3,%d0
m68k_015ad0_end:
.org 0x15AD4
m68k_015ad4:
        beq.b (. + 20)
m68k_015ad4_end:
.org 0x15AD6
m68k_015ad6:
        btst.l #0x1,%d0
m68k_015ad6_end:
.org 0x15ADA
m68k_015ada:
        bne.b (. + 8)
m68k_015ada_end:
.org 0x15ADC
m68k_015adc:
        clr.w 0xf386:w
m68k_015adc_end:
.org 0x15AE0
m68k_015ae0:
        bra.b (. + 8)
m68k_015ae0_end:
.org 0x15AE2
m68k_015ae2:
        move.w #0x1,0xf386:w
m68k_015ae2_end:
.org 0x15AE8
m68k_015ae8:
        rts
m68k_015ae8_end:
.org 0x15AEA
m68k_015aea:
        btst.b #0x5,0xf603:w
m68k_015aea_end:
.org 0x15AF0
m68k_015af0:
        bne.w (. + 58)
m68k_015af0_end:
.org 0x15AF4
m68k_015af4:
        move.b 0xf602:w,%d0
m68k_015af4_end:
.org 0x15AF8
m68k_015af8:
        andi.w #0x3,%d0
m68k_015af8_end:
.org 0x15AFC
m68k_015afc:
        bne.w (. + 12)
m68k_015afc_end:
.org 0x15B00
m68k_015b00:
        btst.b #0x3,0xf321:w
m68k_015b00_end:
.org 0x15B06
m68k_015b06:
        bne.b (. + 36)
m68k_015b06_end:
.org 0x15B08
m68k_015b08:
        lea.l 34(%pc),%a0
m68k_015b08_end:
.org 0x15B0C
m68k_015b0c:
        nop
m68k_015b0c_end:
.org 0x15B0E
m68k_015b0e:
        move.w 0xf386:w,%d0
m68k_015b0e_end:
.org 0x15B12
m68k_015b12:
        lsl.w #0x1,%d0
m68k_015b12_end:
.org 0x15B14
m68k_015b14:
        add.w 0xf386:w,%d0
m68k_015b14_end:
.org 0x15B18
m68k_015b18:
        lsl.w #0x3,%d0
m68k_015b18_end:
.org 0x15B1A
m68k_015b1a:
        addi.w #0x40,%d0
m68k_015b1a_end:
.org 0x15B1E
m68k_015b1e:
        move.w #0x88,%d1
m68k_015b1e_end:
.org 0x15B22
m68k_015b22:
        clr.w %d2
m68k_015b22_end:
.org 0x15B24
m68k_015b24:
        jsr 0xac08:l
m68k_015b24_end:
.org 0x15B2A
m68k_015b2a:
        rts
m68k_015b2a_end:
.org 0x15B76
m68k_015b76:
        bsr.w (. + -14964)
m68k_015b76_end:
.org 0x15B7A
m68k_015b7a:
        bsr.b (. + -114)
m68k_015b7a_end:
.org 0x15B7C
m68k_015b7c:
        rts
m68k_015b7c_end:
.org 0x15B7E
m68k_015b7e:
        jsr 0x12418:l
m68k_015b7e_end:
.org 0x15B84
m68k_015b84:
        jsr 0x125ac:l
m68k_015b84_end:
.org 0x15B8A
m68k_015b8a:
        btst.b #0x5,0xf603:w
m68k_015b8a_end:
.org 0x15B90
m68k_015b90:
        beq.b (. + 34)
m68k_015b90_end:
.org 0x15B92
m68k_015b92:
        clr.w 0xf386:w
m68k_015b92_end:
.org 0x15B96
m68k_015b96:
        jsr 0xc0b6:l
m68k_015b96_end:
.org 0x15B9C
m68k_015b9c:
        move.w #0x208,0xf612:w
m68k_015b9c_end:
.org 0x15BA2
m68k_015ba2:
        move.w #0x3,0xf362:w
m68k_015ba2_end:
.org 0x15BA8
m68k_015ba8:
        move.w #0x12,0xf36a:w
m68k_015ba8_end:
.org 0x15BAE
m68k_015bae:
        bsr.w (. + 34)
m68k_015bae_end:
.org 0x15BB2
m68k_015bb2:
        btst.b #0x4,0xf603:w
m68k_015bb2_end:
.org 0x15BB8
m68k_015bb8:
        beq.b (. + 24)
m68k_015bb8_end:
.org 0x15BBA
m68k_015bba:
        move.w #0x208,0xf612:w
m68k_015bba_end:
.org 0x15BC0
m68k_015bc0:
        move.w #0x2,0xf362:w
m68k_015bc0_end:
.org 0x15BC6
m68k_015bc6:
        move.w #0x12,0xf36a:w
m68k_015bc6_end:
.org 0x15BCC
m68k_015bcc:
        bsr.w (. + -14650)
m68k_015bcc_end:
.org 0x15BD0
m68k_015bd0:
        rts
m68k_015bd0_end:
.org 0x15C1A
m68k_015c1a:
        move.w 0xf3d0:w,%d0
m68k_015c1a_end:
.org 0x15C1E
m68k_015c1e:
        lea.l 0xcc00:w,%a0
m68k_015c1e_end:
.org 0x15C22
m68k_015c22:
        clr.w %d1
m68k_015c22_end:
.org 0x15C24
m68k_015c24:
        move.b (%a0, %d0.w),%d1
m68k_015c24_end:
.org 0x15C28
m68k_015c28:
        lea.l 0xf428:w,%a0
m68k_015c28_end:
.org 0x15C2C
m68k_015c2c:
        move.b (%a0, %d1.w),%d1
m68k_015c2c_end:
.org 0x15C30
m68k_015c30:
        move.w 0xf602:w,%d0
m68k_015c30_end:
.org 0x15C34
m68k_015c34:
        btst.l #0x5,%d0
m68k_015c34_end:
.org 0x15C38
m68k_015c38:
        beq.w (. + 40)
m68k_015c38_end:
.org 0x15C3C
m68k_015c3c:
        move.l #0xc0000026,%d0
m68k_015c3c_end:
.org 0x15C42
m68k_015c42:
        move.w #0x7,%d1
m68k_015c42_end:
.org 0x15C46
m68k_015c46:
        move.w #0xca02,%d2
m68k_015c46_end:
.org 0x15C4A
m68k_015c4a:
        lea.l 22(%pc),%a0
m68k_015c4a_end:
.org 0x15C4E
m68k_015c4e:
        jsr 0x26bfa:l
m68k_015c4e_end:
.org 0x15C54
m68k_015c54:
        bclr.b #0x6,0xf3a4:w
m68k_015c54_end:
.org 0x15C5A
m68k_015c5a:
        move.w #0x5,0xf362:w
m68k_015c5a_end:
.org 0x15C60
m68k_015c60:
        rts
m68k_015c60_end:
.org 0x15C7E
m68k_015c7e:
        movea.l 0xff382c:l,%a0
m68k_015c7e_end:
.org 0x15C84
m68k_015c84:
        move.b (%a0),%d0
m68k_015c84_end:
.org 0x15C86
m68k_015c86:
        andi.w #0xf,%d0
m68k_015c86_end:
.org 0x15C8A
m68k_015c8a:
        move.w %d0,0xf636:w
m68k_015c8a_end:
.org 0x15C8E
m68k_015c8e:
        subq.w #0x1,%d0
m68k_015c8e_end:
.org 0x15C90
m68k_015c90:
        adda.w #0xd,%a0
m68k_015c90_end:
.org 0x15C94
m68k_015c94:
        lea.l 0xf500:w,%a1
m68k_015c94_end:
.org 0x15C98
m68k_015c98:
        clr.w %d1
m68k_015c98_end:
.org 0x15C9A
m68k_015c9a:
        move.b (%a0)+,%d1
m68k_015c9a_end:
.org 0x15C9C
m68k_015c9c:
        move.w %d1,(%a1)+
m68k_015c9c_end:
.org 0x15C9E
m68k_015c9e:
        dbra %d0,(. + -4)
m68k_015c9e_end:
.org 0x15CA2
m68k_015ca2:
        move.w #0xffff,(%a1)
m68k_015ca2_end:
.org 0x15CA6
m68k_015ca6:
        move.w #0x12,0xf65a:w
m68k_015ca6_end:
.org 0x15CAC
m68k_015cac:
        clr.w 0xf684:w
m68k_015cac_end:
.org 0x15CB0
m68k_015cb0:
        move.w #0xb0,0xf38c:w
m68k_015cb0_end:
.org 0x15CB6
m68k_015cb6:
        move.w #0x208,0xf612:w
m68k_015cb6_end:
.org 0x15CBC
m68k_015cbc:
        move.w #0x4,0xf362:w
m68k_015cbc_end:
.org 0x15CC2
m68k_015cc2:
        rts
m68k_015cc2_end:
.org 0x15CC4
m68k_015cc4:
        bsr.w (. + 80)
m68k_015cc4_end:
.org 0x15CC8
m68k_015cc8:
        bcs.w (. + 74)
m68k_015cc8_end:
.org 0x15CCC
m68k_015ccc:
        cmpi.w #0x10,0xf352:w
m68k_015ccc_end:
.org 0x15CD2
m68k_015cd2:
        bcc.w (. + 42)
m68k_015cd2_end:
.org 0x15CD6
m68k_015cd6:
        move.w 0xf352:w,%d0
m68k_015cd6_end:
.org 0x15CDA
m68k_015cda:
        move.w #0x40,%d1
m68k_015cda_end:
.org 0x15CDE
m68k_015cde:
        lea.l 0xfb80:w,%a0
m68k_015cde_end:
.org 0x15CE2
m68k_015ce2:
        jsr 0xdea6:l
m68k_015ce2_end:
.org 0x15CE8
m68k_015ce8:
        move.w 0xf320:w,%d0
m68k_015ce8_end:
.org 0x15CEC
m68k_015cec:
        andi.w #0x1,%d0
m68k_015cec_end:
.org 0x15CF0
m68k_015cf0:
        bne.w (. + 34)
m68k_015cf0_end:
.org 0x15CF4
m68k_015cf4:
        addq.w #0x1,0xf352:w
m68k_015cf4_end:
.org 0x15CF8
m68k_015cf8:
        bra.w (. + 26)
m68k_015cf8_end:
.org 0x15CFC
m68k_015cfc:
        move.w 0xf314:w,0xf356:w
m68k_015cfc_end:
.org 0x15D02
m68k_015d02:
        move.w 0xf318:w,0xf354:w
m68k_015d02_end:
.org 0x15D08
m68k_015d08:
        clr.w 0xf612:w
m68k_015d08_end:
.org 0x15D0C
m68k_015d0c:
        move.w #0xc4,0xf600:w
m68k_015d0c_end:
.org 0x15D12
m68k_015d12:
        rts
m68k_015d12_end:
.org 0x15D14
m68k_015d14:
        tst.w 0xf352:w
m68k_015d14_end:
.org 0x15D18
m68k_015d18:
        bne.w (. + 114)
m68k_015d18_end:
.org 0x15D1C
m68k_015d1c:
        movea.l 0xff382c:l,%a0
m68k_015d1c_end:
.org 0x15D22
m68k_015d22:
        clr.w %d0
m68k_015d22_end:
.org 0x15D24
m68k_015d24:
        move.b 0x4(%a0),%d0
m68k_015d24_end:
.org 0x15D28
m68k_015d28:
        cmp.w 0xf67c:w,%d0
m68k_015d28_end:
.org 0x15D2C
m68k_015d2c:
        beq.w (. + 12)
m68k_015d2c_end:
.org 0x15D30
m68k_015d30:
        cmp.w 0xf67e:w,%d0
m68k_015d30_end:
.org 0x15D34
m68k_015d34:
        bne.w (. + 86)
m68k_015d34_end:
.org 0x15D38
m68k_015d38:
        lea.l 0xefbe:w,%a0
m68k_015d38_end:
.org 0x15D3C
m68k_015d3c:
        adda.w 0xefc6:w,%a0
m68k_015d3c_end:
.org 0x15D40
m68k_015d40:
        move.w (%a0),%d0
m68k_015d40_end:
.org 0x15D42
m68k_015d42:
        lea.l 0x9000:w,%a0
m68k_015d42_end:
.org 0x15D46
m68k_015d46:
        clr.w %d1
m68k_015d46_end:
.org 0x15D48
m68k_015d48:
        move.b 0x4(%a0, %d0.w),%d1
m68k_015d48_end:
.org 0x15D4C
m68k_015d4c:
        cmp.w 0xf67c:w,%d1
m68k_015d4c_end:
.org 0x15D50
m68k_015d50:
        beq.w (. + 12)
m68k_015d50_end:
.org 0x15D54
m68k_015d54:
        cmp.w 0xf67e:w,%d1
m68k_015d54_end:
.org 0x15D58
m68k_015d58:
        bne.w (. + 50)
m68k_015d58_end:
.org 0x15D5C
m68k_015d5c:
        move.w #0xf,0xf362:w
m68k_015d5c_end:
.org 0x15D62
m68k_015d62:
        move.w 0xf67e:w,%d0
m68k_015d62_end:
.org 0x15D66
m68k_015d66:
        lsl.w #0x1,%d0
m68k_015d66_end:
.org 0x15D68
m68k_015d68:
        lea.l 0xe640:w,%a0
m68k_015d68_end:
.org 0x15D6C
m68k_015d6c:
        move.w (%a0, %d0.w),0xf3d0:w
m68k_015d6c_end:
.org 0x15D72
m68k_015d72:
        move.w #0xc0,%d0
m68k_015d72_end:
.org 0x15D76
m68k_015d76:
        jsr 0x676f2:l
m68k_015d76_end:
.org 0x15D7C
m68k_015d7c:
        move.w #0xfffe,0xf376:w
m68k_015d7c_end:
.org 0x15D82
m68k_015d82:
        ori.w #0x1,%sr
m68k_015d82_end:
.org 0x15D86
m68k_015d86:
        bra.w (. + 8)
m68k_015d86_end:
.org 0x15D8A
m68k_015d8a:
        andi.w #0xfffe,%sr
m68k_015d8a_end:
.org 0x15D8E
m68k_015d8e:
        rts
m68k_015d8e_end:
.org 0x15D90
m68k_015d90:
        btst.b #0x5,0xf603:w
m68k_015d90_end:
.org 0x15D96
m68k_015d96:
        beq.w (. + 14)
m68k_015d96_end:
.org 0x15D9A
m68k_015d9a:
        move.w #0x400,0xf612:w
m68k_015d9a_end:
.org 0x15DA0
m68k_015da0:
        clr.w 0xf362:w
m68k_015da0_end:
.org 0x15DA4
m68k_015da4:
        rts
m68k_015da4_end:
.org 0x15DA6
m68k_015da6:
        btst.b #0x5,0xf603:w
m68k_015da6_end:
.org 0x15DAC
m68k_015dac:
        beq.w (. + 34)
m68k_015dac_end:
.org 0x15DB0
m68k_015db0:
        addq.w #0x1,0xf362:w
m68k_015db0_end:
.org 0x15DB4
m68k_015db4:
        move.w 0xf67c:w,%d0
m68k_015db4_end:
.org 0x15DB8
m68k_015db8:
        lsl.w #0x1,%d0
m68k_015db8_end:
.org 0x15DBA
m68k_015dba:
        lea.l 0xe640:w,%a0
m68k_015dba_end:
.org 0x15DBE
m68k_015dbe:
        move.w (%a0, %d0.w),0xf3d0:w
m68k_015dbe_end:
.org 0x15DC4
m68k_015dc4:
        move.w #0xc1,%d0
m68k_015dc4_end:
.org 0x15DC8
m68k_015dc8:
        jsr 0x676f2:l
m68k_015dc8_end:
.org 0x15DCE
m68k_015dce:
        rts
m68k_015dce_end:
.org 0x15DD0
m68k_015dd0:
        btst.b #0x5,0xf605:w
m68k_015dd0_end:
.org 0x15DD6
m68k_015dd6:
        beq.w (. + 14)
m68k_015dd6_end:
.org 0x15DDA
m68k_015dda:
        move.w #0xd,0xf362:w
m68k_015dda_end:
.org 0x15DE0
m68k_015de0:
        addq.w #0x1,0xf352:w
m68k_015de0_end:
.org 0x15DE4
m68k_015de4:
        rts
m68k_015de4_end:
.org 0x16152
m68k_016152:
        lea.l 0xd100:w,%a0
m68k_016152_end:
.org 0x16156
m68k_016156:
        adda.w 0xf31a:w,%a0
m68k_016156_end:
.org 0x1615A
m68k_01615a:
        move.w #0xe,0xa0(%a0)
m68k_01615a_end:
.org 0x16160
m68k_016160:
        move.w #0xe,0x80(%a0)
m68k_016160_end:
.org 0x16166
m68k_016166:
        move.w #0xe,0x60(%a0)
m68k_016166_end:
.org 0x1616C
m68k_01616c:
        move.w #0xe,0x40(%a0)
m68k_01616c_end:
.org 0x16172
m68k_016172:
        move.w #0xe,0x20(%a0)
m68k_016172_end:
.org 0x16178
m68k_016178:
        move.w #0xe,(%a0)+
m68k_016178_end:
.org 0x1617C
m68k_01617c:
        move.w #0xc71e,0xa0(%a0)
m68k_01617c_end:
.org 0x16182
m68k_016182:
        move.w #0xc69e,0x80(%a0)
m68k_016182_end:
.org 0x16188
m68k_016188:
        move.w #0xc61e,0x60(%a0)
m68k_016188_end:
.org 0x1618E
m68k_01618e:
        move.w #0xc59e,0x40(%a0)
m68k_01618e_end:
.org 0x16194
m68k_016194:
        move.w #0xc51e,0x20(%a0)
m68k_016194_end:
.org 0x1619A
m68k_01619a:
        move.w #0xc49e,(%a0)+
m68k_01619a_end:
.org 0x1619E
m68k_01619e:
        move.w #0xd,%d0
m68k_01619e_end:
.org 0x161A2
m68k_0161a2:
        move.w #0x8000,0xa0(%a0)
m68k_0161a2_end:
.org 0x161A8
m68k_0161a8:
        move.w #0x8000,0x80(%a0)
m68k_0161a8_end:
.org 0x161AE
m68k_0161ae:
        move.w #0x8000,0x60(%a0)
m68k_0161ae_end:
.org 0x161B4
m68k_0161b4:
        move.w #0x8000,0x40(%a0)
m68k_0161b4_end:
.org 0x161BA
m68k_0161ba:
        move.w #0x8000,0x20(%a0)
m68k_0161ba_end:
.org 0x161C0
m68k_0161c0:
        move.w #0x8000,(%a0)+
m68k_0161c0_end:
.org 0x161C4
m68k_0161c4:
        dbra %d0,(. + -34)
m68k_0161c4_end:
.org 0x161C8
m68k_0161c8:
        clr.w 0xa0(%a0)
m68k_0161c8_end:
.org 0x161CC
m68k_0161cc:
        addi.w #0xc0,0xf31a:w
m68k_0161cc_end:
.org 0x161D2
m68k_0161d2:
        rts
m68k_0161d2_end:
.org 0x18848
m68k_018848:
        move.w 0xf636:w,%d0
m68k_018848_end:
.org 0x1884C
m68k_01884c:
        sub.w 0xf684:w,%d0
m68k_01884c_end:
.org 0x18850
m68k_018850:
        add.w 0xf712:w,%d0
m68k_018850_end:
.org 0x18854
m68k_018854:
        cmpi.w #0xa,%d0
m68k_018854_end:
.org 0x18858
m68k_018858:
        bls.w (. + 42)
m68k_018858_end:
.org 0x1885C
m68k_01885c:
        lea.l 0xaf56:w,%a0
m68k_01885c_end:
.org 0x18860
m68k_018860:
        move.w 0xf378:w,%d0
m68k_018860_end:
.org 0x18864
m68k_018864:
        cmp.w 0xf636:w,%d0
m68k_018864_end:
.org 0x18868
m68k_018868:
        bcs.w (. + 6)
m68k_018868_end:
.org 0x1886C
m68k_01886c:
        clr.w %d0
m68k_01886c_end:
.org 0x1886E
m68k_01886e:
        move.w %d0,%d2
m68k_01886e_end:
.org 0x18870
m68k_018870:
        lsl.w #0x1,%d2
m68k_018870_end:
.org 0x18872
m68k_018872:
        move.w (%a0, %d2.w),%d1
m68k_018872_end:
.org 0x18876
m68k_018876:
        btst.l #0xe,%d1
m68k_018876_end:
.org 0x1887A
m68k_01887a:
        beq.w (. + 12)
m68k_01887a_end:
.org 0x1887E
m68k_01887e:
        addq.w #0x1,%d0
m68k_01887e_end:
.org 0x18880
m68k_018880:
        bra.b (. + -28)
m68k_018880_end:
.org 0x18882
m68k_018882:
        move.w 0xf636:w,%d0
m68k_018882_end:
.org 0x18886
m68k_018886:
        move.w %d0,0xf378:w
m68k_018886_end:
.org 0x1888A
m68k_01888a:
        subq.w #0x2,%d0
m68k_01888a_end:
.org 0x1888C
m68k_01888c:
        bcc.w (. + 6)
m68k_01888c_end:
.org 0x18890
m68k_018890:
        clr.w %d0
m68k_018890_end:
.org 0x18892
m68k_018892:
        move.w 0xf636:w,%d1
m68k_018892_end:
.org 0x18896
m68k_018896:
        subq.w #0x4,%d1
m68k_018896_end:
.org 0x18898
m68k_018898:
        cmp.w %d1,%d0
m68k_018898_end:
.org 0x1889A
m68k_01889a:
        bls.w (. + 6)
m68k_01889a_end:
.org 0x1889E
m68k_01889e:
        move.w %d1,%d0
m68k_01889e_end:
.org 0x188A0
m68k_0188a0:
        move.w %d0,0xf658:w
m68k_0188a0_end:
.org 0x188A4
m68k_0188a4:
        rts
m68k_0188a4_end:
.org 0x18D72
m68k_018d72:
        bsr.w (. + 4912)
m68k_018d72_end:
.org 0x18D76
m68k_018d76:
        bcs.w (. + 312)
m68k_018d76_end:
.org 0x18D7A
m68k_018d7a:
        cmpi.w #0x10,0xf352:w
m68k_018d7a_end:
.org 0x18D80
m68k_018d80:
        bcc.b (. + 80)
m68k_018d80_end:
.org 0x18D82
m68k_018d82:
        move.w 0xf352:w,%d0
m68k_018d82_end:
.org 0x18D86
m68k_018d86:
        move.w #0x40,%d1
m68k_018d86_end:
.org 0x18D8A
m68k_018d8a:
        lea.l 0xfb80:w,%a0
m68k_018d8a_end:
.org 0x18D8E
m68k_018d8e:
        jsr 0xdea6:l
m68k_018d8e_end:
.org 0x18D94
m68k_018d94:
        tst.w 0xf77a:w
m68k_018d94_end:
.org 0x18D98
m68k_018d98:
        beq.w (. + 10)
m68k_018d98_end:
.org 0x18D9C
m68k_018d9c:
        jsr 0x23f6:l
m68k_018d9c_end:
.org 0x18DA2
m68k_018da2:
        move.w 0xf320:w,%d0
m68k_018da2_end:
.org 0x18DA6
m68k_018da6:
        andi.w #0x1,%d0
m68k_018da6_end:
.org 0x18DAA
m68k_018daa:
        bne.w (. + 260)
m68k_018daa_end:
.org 0x18DAE
m68k_018dae:
        addq.w #0x1,0xf352:w
m68k_018dae_end:
.org 0x18DB2
m68k_018db2:
        tst.w 0xf6c4:w
m68k_018db2_end:
.org 0x18DB6
m68k_018db6:
        bne.w (. + 248)
m68k_018db6_end:
.org 0x18DBA
m68k_018dba:
        jsr 0x15de6:l
m68k_018dba_end:
.org 0x18DC0
m68k_018dc0:
        jsr 0x169aa:l
m68k_018dc0_end:
.org 0x18DC6
m68k_018dc6:
        jsr 0x679fc:l
m68k_018dc6_end:
.org 0x18DCC
m68k_018dcc:
        bra.w (. + 226)
m68k_018dcc_end:
.org 0x18DD0
m68k_018dd0:
        bne.b (. + 20)
m68k_018dd0_end:
.org 0x18DD2
m68k_018dd2:
        move.w #0x84,0xf600:w
m68k_018dd2_end:
.org 0x18DD8
m68k_018dd8:
        addq.w #0x1,0xf352:w
m68k_018dd8_end:
.org 0x18DDC
m68k_018ddc:
        clr.w 0xf77a:w
m68k_018ddc_end:
.org 0x18DE0
m68k_018de0:
        bra.w (. + 206)
m68k_018de0_end:
.org 0x18DE4
m68k_018de4:
        jsr 0x1a2b8:l
m68k_018de4_end:
.org 0x18DEA
m68k_018dea:
        jsr 0xa3da:l
m68k_018dea_end:
.org 0x18DF0
m68k_018df0:
        move.w #0x1f,%d0
m68k_018df0_end:
.org 0x18DF4
m68k_018df4:
        sub.w 0xf352:w,%d0
m68k_018df4_end:
.org 0x18DF8
m68k_018df8:
        move.w #0x40,%d1
m68k_018df8_end:
.org 0x18DFC
m68k_018dfc:
        lea.l 0xfb80:w,%a0
m68k_018dfc_end:
.org 0x18E00
m68k_018e00:
        jsr 0xdea6:l
m68k_018e00_end:
.org 0x18E06
m68k_018e06:
        move.w 0xf320:w,%d0
m68k_018e06_end:
.org 0x18E0A
m68k_018e0a:
        andi.w #0x1,%d0
m68k_018e0a_end:
.org 0x18E0E
m68k_018e0e:
        bne.w (. + 160)
m68k_018e0e_end:
.org 0x18E12
m68k_018e12:
        addq.w #0x1,0xf352:w
m68k_018e12_end:
.org 0x18E16
m68k_018e16:
        cmpi.w #0x20,0xf352:w
m68k_018e16_end:
.org 0x18E1C
m68k_018e1c:
        bcs.w (. + 146)
m68k_018e1c_end:
.org 0x18E20
m68k_018e20:
        btst.b #0x0,0xf3a5:w
m68k_018e20_end:
.org 0x18E26
m68k_018e26:
        bne.w (. + 20)
m68k_018e26_end:
.org 0x18E2A
m68k_018e2a:
        tst.w 0xf772:w
m68k_018e2a_end:
.org 0x18E2E
m68k_018e2e:
        bne.w (. + 78)
m68k_018e2e_end:
.org 0x18E32
m68k_018e32:
        addq.w #0x1,0xf362:w
m68k_018e32_end:
.org 0x18E36
m68k_018e36:
        bra.w (. + 60)
m68k_018e36_end:
.org 0x18E3A
m68k_018e3a:
        cmpi.w #0x4,0xf6d2:w
m68k_018e3a_end:
.org 0x18E40
m68k_018e40:
        beq.w (. + 34)
m68k_018e40_end:
.org 0x18E44
m68k_018e44:
        move.w #0x405,0xf612:w
m68k_018e44_end:
.org 0x18E4A
m68k_018e4a:
        clr.w 0xf362:w
m68k_018e4a_end:
.org 0x18E4E
m68k_018e4e:
        move.w 0xaf80:w,%d0
m68k_018e4e_end:
.org 0x18E52
m68k_018e52:
        jsr 0x676f2:l
m68k_018e52_end:
.org 0x18E58
m68k_018e58:
        bclr.b #0x0,0xf3a5:w
m68k_018e58_end:
.org 0x18E5E
m68k_018e5e:
        bra.w (. + 20)
m68k_018e5e_end:
.org 0x18E62
m68k_018e62:
        move.w #0x412,0xf612:w
m68k_018e62_end:
.org 0x18E68
m68k_018e68:
        clr.w 0xf362:w
m68k_018e68_end:
.org 0x18E6C
m68k_018e6c:
        bclr.b #0x0,0xf3a5:w
m68k_018e6c_end:
.org 0x18E72
m68k_018e72:
        jsr 0x1a25e:l
m68k_018e72_end:
.org 0x18E78
m68k_018e78:
        bra.w (. + 54)
m68k_018e78_end:
.org 0x18E7C
m68k_018e7c:
        jsr 0x1a25e:l
m68k_018e7c_end:
.org 0x18E82
m68k_018e82:
        clr.w 0xf3a4:w
m68k_018e82_end:
.org 0x18E86
m68k_018e86:
        cmpi.w #0x2,0xf772:w
m68k_018e86_end:
.org 0x18E8C
m68k_018e8c:
        beq.w (. + 18)
m68k_018e8c_end:
.org 0x18E90
m68k_018e90:
        move.w #0x410,0xf612:w
m68k_018e90_end:
.org 0x18E96
m68k_018e96:
        clr.w 0xf362:w
m68k_018e96_end:
.org 0x18E9A
m68k_018e9a:
        bra.w (. + 20)
m68k_018e9a_end:
.org 0x18E9E
m68k_018e9e:
        move.w #0x408,0xf612:w
m68k_018e9e_end:
.org 0x18EA4
m68k_018ea4:
        clr.w 0xf362:w
m68k_018ea4_end:
.org 0x18EA8
m68k_018ea8:
        jsr 0x20088:l
m68k_018ea8_end:
.org 0x18EAE
m68k_018eae:
        rts
m68k_018eae_end:
.org 0x19084
m68k_019084:
        btst.b #0x5,0xf603:w
m68k_019084_end:
.org 0x1908A
m68k_01908a:
        beq.w (. + 12)
m68k_01908a_end:
.org 0x1908E
m68k_01908e:
        clr.w 0xf362:w
m68k_01908e_end:
.org 0x19092
m68k_019092:
        addq.w #0x1,0xf352:w
m68k_019092_end:
.org 0x19096
m68k_019096:
        jsr 0x679fc:l
m68k_019096_end:
.org 0x1909C
m68k_01909c:
        rts
m68k_01909c_end:
.org 0x190C6
m68k_0190c6:
        cmpi.w #0xa,0xf36a:w
m68k_0190c6_end:
.org 0x190CC
m68k_0190cc:
        bcc.b (. + 14)
m68k_0190cc_end:
.org 0x190CE
m68k_0190ce:
        bsr.w (. + 32)
m68k_0190ce_end:
.org 0x190D2
m68k_0190d2:
        addq.w #0x1,0xf36a:w
m68k_0190d2_end:
.org 0x190D6
m68k_0190d6:
        bra.w (. + 22)
m68k_0190d6_end:
.org 0x190DA
m68k_0190da:
        move.w 0xf602:w,%d0
m68k_0190da_end:
.org 0x190DE
m68k_0190de:
        andi.w #0x70,%d0
m68k_0190de_end:
.org 0x190E2
m68k_0190e2:
        beq.b (. + 10)
m68k_0190e2_end:
.org 0x190E4
m68k_0190e4:
        clr.w 0xf36a:w
m68k_0190e4_end:
.org 0x190E8
m68k_0190e8:
        addq.w #0x1,0xf362:w
m68k_0190e8_end:
.org 0x190EC
m68k_0190ec:
        rts
m68k_0190ec_end:
.org 0x190EE
m68k_0190ee:
        movea.l 0xf6c0:w,%a0
m68k_0190ee_end:
.org 0x190F2
m68k_0190f2:
        move.l #0xc0000019,%d0
m68k_0190f2_end:
.org 0x190F8
m68k_0190f8:
        move.w #0x2,%d1
m68k_0190f8_end:
.org 0x190FC
m68k_0190fc:
        move.w 0xf36a:w,%d2
m68k_0190fc_end:
.org 0x19100
m68k_019100:
        lsl.w #0x8,%d2
m68k_019100_end:
.org 0x19102
m68k_019102:
        addi.w #0xc08e,%d2
m68k_019102_end:
.org 0x19106
m68k_019106:
        move.w #0xc386,0xf692:w
m68k_019106_end:
.org 0x1910C
m68k_01910c:
        move.w #0xc401,0xf694:w
m68k_01910c_end:
.org 0x19112
m68k_019112:
        jsr 0x26bfa:l
m68k_019112_end:
.org 0x19118
m68k_019118:
        move.l %a0,0xf6c0:w
m68k_019118_end:
.org 0x1911C
m68k_01911c:
        rts
m68k_01911c_end:
.org 0x1911E
m68k_01911e:
        jsr 30(%pc)
m68k_01911e_end:
.org 0x19122
m68k_019122:
        nop
m68k_019122_end:
.org 0x19124
m68k_019124:
        addq.w #0x1,0xf36a:w
m68k_019124_end:
.org 0x19128
m68k_019128:
        cmpi.w #0xa,0xf36a:w
m68k_019128_end:
.org 0x1912E
m68k_01912e:
        bcs.b (. + 14)
m68k_01912e_end:
.org 0x19130
m68k_019130:
        move.w 0xf38a:w,0xf612:w
m68k_019130_end:
.org 0x19136
m68k_019136:
        move.w 0xf3b0:w,0xf362:w
m68k_019136_end:
.org 0x1913C
m68k_01913c:
        rts
m68k_01913c_end:
.org 0x1913E
m68k_01913e:
        lea.l 0xaba0e:l,%a0
m68k_01913e_end:
.org 0x19144
m68k_019144:
        move.l #0xc0000019,%d0
m68k_019144_end:
.org 0x1914A
m68k_01914a:
        move.w #0x2,%d1
m68k_01914a_end:
.org 0x1914E
m68k_01914e:
        move.w 0xf36a:w,%d3
m68k_01914e_end:
.org 0x19152
m68k_019152:
        lsl.w #0x8,%d3
m68k_019152_end:
.org 0x19154
m68k_019154:
        move.w #0xc98e,%d2
m68k_019154_end:
.org 0x19158
m68k_019158:
        sub.w %d3,%d2
m68k_019158_end:
.org 0x1915A
m68k_01915a:
        jsr 0x26bfa:l
m68k_01915a_end:
.org 0x19160
m68k_019160:
        rts
m68k_019160_end:
.org 0x192C0
m68k_0192c0:
        move.l #0x40b40003,0xc00004:l
m68k_0192c0_end:
.org 0x192CA
m68k_0192ca:
        move.l #0xc000c380,0xc00000:l
m68k_0192ca_end:
.org 0x192D4
m68k_0192d4:
        move.w #0x3,%d0
m68k_0192d4_end:
.org 0x192D8
m68k_0192d8:
        move.l #0xc381c381,0xc00000:l
m68k_0192d8_end:
.org 0x192E2
m68k_0192e2:
        dbra %d0,(. + -10)
m68k_0192e2_end:
.org 0x192E6
m68k_0192e6:
        move.l #0xcb80c000,0xc00000:l
m68k_0192e6_end:
.org 0x192F0
m68k_0192f0:
        move.w #0xc000,0xc00000:l
m68k_0192f0_end:
.org 0x192F8
m68k_0192f8:
        move.l #0x41340003,0xc00004:l
m68k_0192f8_end:
.org 0x19302
m68k_019302:
        move.l #0xc000c382,0xc00000:l
m68k_019302_end:
.org 0x1930C
m68k_01930c:
        move.w #0x3,%d0
m68k_01930c_end:
.org 0x19310
m68k_019310:
        move.l #0xc001c001,0xc00000:l
m68k_019310_end:
.org 0x1931A
m68k_01931a:
        dbra %d0,(. + -10)
m68k_01931a_end:
.org 0x1931E
m68k_01931e:
        move.l #0xcb82c000,0xc00000:l
m68k_01931e_end:
.org 0x19328
m68k_019328:
        addq.w #0x1,0xf362:w
m68k_019328_end:
.org 0x1932C
m68k_01932c:
        move.w #0x40,0xf600:w
m68k_01932c_end:
.org 0x19332
m68k_019332:
        clr.w 0xf36a:w
m68k_019332_end:
.org 0x19336
m68k_019336:
        clr.w 0xf656:w
m68k_019336_end:
.org 0x1933A
m68k_01933a:
        rts
m68k_01933a_end:
.org 0x1933C
m68k_01933c:
        tst.w 0xf600:w
m68k_01933c_end:
.org 0x19340
m68k_019340:
        bne.w (. + 16)
m68k_019340_end:
.org 0x19344
m68k_019344:
        jsr 0x5f7c:l
m68k_019344_end:
.org 0x1934A
m68k_01934a:
        move.w #0x8,0xcfd2:w
m68k_01934a_end:
.org 0x19350
m68k_019350:
        rts
m68k_019350_end:
.org 0x19352
m68k_019352:
        bsr.w (. + 270)
m68k_019352_end:
.org 0x19356
m68k_019356:
        bsr.w (. + 388)
m68k_019356_end:
.org 0x1935A
m68k_01935a:
        lea.l 0xf500:w,%a0
m68k_01935a_end:
.org 0x1935E
m68k_01935e:
        move.w 0xf378:w,%d0
m68k_01935e_end:
.org 0x19362
m68k_019362:
        lsl.w #0x1,%d0
m68k_019362_end:
.org 0x19364
m68k_019364:
        move.w (%a0, %d0.w),%d0
m68k_019364_end:
.org 0x19368
m68k_019368:
        andi.w #0xff,%d0
m68k_019368_end:
.org 0x1936C
m68k_01936c:
        move.w %d0,0xa5f8:w
m68k_01936c_end:
.org 0x19370
m68k_019370:
        move.w #0xffff,0xa5fa:w
m68k_019370_end:
.org 0x19376
m68k_019376:
        tst.w 0xcfd2:w
m68k_019376_end:
.org 0x1937A
m68k_01937a:
        beq.w (. + 28)
m68k_01937a_end:
.org 0x1937E
m68k_01937e:
        subq.w #0x1,0xcfd2:w
m68k_01937e_end:
.org 0x19382
m68k_019382:
        cmpi.w #0x8,0xcfd2:w
m68k_019382_end:
.org 0x19388
m68k_019388:
        bls.w (. + 98)
m68k_019388_end:
.org 0x1938C
m68k_01938c:
        move.w #0x8,0xcfd2:w
m68k_01938c_end:
.org 0x19392
m68k_019392:
        bra.w (. + 88)
m68k_019392_end:
.org 0x19396
m68k_019396:
        btst.b #0x5,0xf603:w
m68k_019396_end:
.org 0x1939C
m68k_01939c:
        beq.b (. + 78)
m68k_01939c_end:
.org 0x1939E
m68k_01939e:
        move.w #0xac,%d0
m68k_01939e_end:
.org 0x193A2
m68k_0193a2:
        jsr 0x808a:l
m68k_0193a2_end:
.org 0x193A8
m68k_0193a8:
        move.w 0xf378:w,%d0
m68k_0193a8_end:
.org 0x193AC
m68k_0193ac:
        lsl.w #0x1,%d0
m68k_0193ac_end:
.org 0x193AE
m68k_0193ae:
        lea.l 0xf500:w,%a0
m68k_0193ae_end:
.org 0x193B2
m68k_0193b2:
        cmpi.w #0x4000,(%a0, %d0.w)
m68k_0193b2_end:
.org 0x193B8
m68k_0193b8:
        bcc.w (. + 166)
m68k_0193b8_end:
.org 0x193BC
m68k_0193bc:
        cmpi.w #0x3,0xf6d2:w
m68k_0193bc_end:
.org 0x193C2
m68k_0193c2:
        beq.w (. + 20)
m68k_0193c2_end:
.org 0x193C6
m68k_0193c6:
        move.w 0xf38a:w,0xf612:w
m68k_0193c6_end:
.org 0x193CC
m68k_0193cc:
        move.w 0xf3b0:w,0xf362:w
m68k_0193cc_end:
.org 0x193D2
m68k_0193d2:
        bra.w (. + 140)
m68k_0193d2_end:
.org 0x193D6
m68k_0193d6:
        move.w (%a0, %d0.w),0xf3a6:w
m68k_0193d6_end:
.org 0x193DC
m68k_0193dc:
        clr.w 0xf36a:w
m68k_0193dc_end:
.org 0x193E0
m68k_0193e0:
        move.w #0x406,0xf612:w
m68k_0193e0_end:
.org 0x193E6
m68k_0193e6:
        bra.w (. + 120)
m68k_0193e6_end:
.org 0x193EA
m68k_0193ea:
        cmpi.w #0x2,0xf6d2:w
m68k_0193ea_end:
.org 0x193F0
m68k_0193f0:
        bne.b (. + 20)
m68k_0193f0_end:
.org 0x193F2
m68k_0193f2:
        btst.b #0x4,0xf603:w
m68k_0193f2_end:
.org 0x193F8
m68k_0193f8:
        beq.w (. + 52)
m68k_0193f8_end:
.org 0x193FC
m68k_0193fc:
        bsr.w (. + 390)
m68k_0193fc_end:
.org 0x19400
m68k_019400:
        bra.w (. + 94)
m68k_019400_end:
.org 0x19404
m68k_019404:
        cmpi.w #0x3,0xf6d2:w
m68k_019404_end:
.org 0x1940A
m68k_01940a:
        bne.w (. + 34)
m68k_01940a_end:
.org 0x1940E
m68k_01940e:
        btst.b #0x4,0xf603:w
m68k_01940e_end:
.org 0x19414
m68k_019414:
        beq.w (. + 24)
m68k_019414_end:
.org 0x19418
m68k_019418:
        clr.w 0xf36a:w
m68k_019418_end:
.org 0x1941C
m68k_01941c:
        move.w #0x406,0xf612:w
m68k_01941c_end:
.org 0x19422
m68k_019422:
        move.w #0x4,0xf6d2:w
m68k_019422_end:
.org 0x19428
m68k_019428:
        bra.w (. + 54)
m68k_019428_end:
.org 0x1942C
m68k_01942c:
        btst.b #0x6,0xf603:w
m68k_01942c_end:
.org 0x19432
m68k_019432:
        beq.w (. + 44)
m68k_019432_end:
.org 0x19436
m68k_019436:
        move.w #0x207,0xf612:w
m68k_019436_end:
.org 0x1943C
m68k_01943c:
        clr.w 0xf362:w
m68k_01943c_end:
.org 0x19440
m68k_019440:
        clr.w 0xf352:w
m68k_019440_end:
.org 0x19444
m68k_019444:
        move.w 0xf378:w,%d0
m68k_019444_end:
.org 0x19448
m68k_019448:
        lsl.w #0x1,%d0
m68k_019448_end:
.org 0x1944A
m68k_01944a:
        lea.l 0xf500:w,%a0
m68k_01944a_end:
.org 0x1944E
m68k_01944e:
        move.w (%a0, %d0.w),%d0
m68k_01944e_end:
.org 0x19452
m68k_019452:
        andi.w #0xff,%d0
m68k_019452_end:
.org 0x19456
m68k_019456:
        move.w %d0,0xf372:w
m68k_019456_end:
.org 0x1945A
m68k_01945a:
        addq.w #0x1,0xf378:w
m68k_01945a_end:
.org 0x1945E
m68k_01945e:
        rts
m68k_01945e_end:
.org 0x19460
m68k_019460:
        move.b 0xf602:w,%d0
m68k_019460_end:
.org 0x19464
m68k_019464:
        andi.w #0x3,%d0
m68k_019464_end:
.org 0x19468
m68k_019468:
        beq.w (. + 106)
m68k_019468_end:
.org 0x1946C
m68k_01946c:
        subq.w #0x1,0xf608:w
m68k_01946c_end:
.org 0x19470
m68k_019470:
        bne.w (. + 104)
m68k_019470_end:
.org 0x19474
m68k_019474:
        move.w #0xc,0xf608:w
m68k_019474_end:
.org 0x1947A
m68k_01947a:
        btst.l #0x1,%d0
m68k_01947a_end:
.org 0x1947E
m68k_01947e:
        bne.b (. + 18)
m68k_01947e_end:
.org 0x19480
m68k_019480:
        tst.w 0xf378:w
m68k_019480_end:
.org 0x19484
m68k_019484:
        beq.w (. + 84)
m68k_019484_end:
.org 0x19488
m68k_019488:
        subq.w #0x1,0xf378:w
m68k_019488_end:
.org 0x1948C
m68k_01948c:
        bra.w (. + 22)
m68k_01948c_end:
.org 0x19490
m68k_019490:
        move.w 0xf378:w,%d0
m68k_019490_end:
.org 0x19494
m68k_019494:
        addq.w #0x1,%d0
m68k_019494_end:
.org 0x19496
m68k_019496:
        cmp.w 0xf636:w,%d0
m68k_019496_end:
.org 0x1949A
m68k_01949a:
        bcc.w (. + 62)
m68k_01949a_end:
.org 0x1949E
m68k_01949e:
        move.w %d0,0xf378:w
m68k_01949e_end:
.org 0x194A2
m68k_0194a2:
        move.w 0xf378:w,%d0
m68k_0194a2_end:
.org 0x194A6
m68k_0194a6:
        subi.w #0x2,%d0
m68k_0194a6_end:
.org 0x194AA
m68k_0194aa:
        bcc.b (. + 4)
m68k_0194aa_end:
.org 0x194AC
m68k_0194ac:
        clr.w %d0
m68k_0194ac_end:
.org 0x194AE
m68k_0194ae:
        move.w 0xf636:w,%d1
m68k_0194ae_end:
.org 0x194B2
m68k_0194b2:
        subi.w #0x5,%d1
m68k_0194b2_end:
.org 0x194B6
m68k_0194b6:
        bcc.b (. + 4)
m68k_0194b6_end:
.org 0x194B8
m68k_0194b8:
        clr.w %d1
m68k_0194b8_end:
.org 0x194BA
m68k_0194ba:
        cmp.w %d1,%d0
m68k_0194ba_end:
.org 0x194BC
m68k_0194bc:
        bls.b (. + 4)
m68k_0194bc_end:
.org 0x194BE
m68k_0194be:
        move.w %d1,%d0
m68k_0194be_end:
.org 0x194C0
m68k_0194c0:
        cmp.w 0xf658:w,%d0
m68k_0194c0_end:
.org 0x194C4
m68k_0194c4:
        beq.b (. + 20)
m68k_0194c4_end:
.org 0x194C6
m68k_0194c6:
        move.w %d0,0xf658:w
m68k_0194c6_end:
.org 0x194CA
m68k_0194ca:
        clr.w 0xf362:w
m68k_0194ca_end:
.org 0x194CE
m68k_0194ce:
        bra.w (. + 10)
m68k_0194ce_end:
.org 0x194D2
m68k_0194d2:
        move.w #0x1,0xf608:w
m68k_0194d2_end:
.org 0x194D8
m68k_0194d8:
        rts
m68k_0194d8_end:
.org 0x194DA
m68k_0194da:
        btst.b #0x5,0xf603:w
m68k_0194da_end:
.org 0x194E0
m68k_0194e0:
        bne.w (. + 62)
m68k_0194e0_end:
.org 0x194E4
m68k_0194e4:
        move.b 0xf602:w,%d0
m68k_0194e4_end:
.org 0x194E8
m68k_0194e8:
        andi.w #0x3,%d0
m68k_0194e8_end:
.org 0x194EC
m68k_0194ec:
        bne.w (. + 14)
m68k_0194ec_end:
.org 0x194F0
m68k_0194f0:
        btst.b #0x3,0xf321:w
m68k_0194f0_end:
.org 0x194F6
m68k_0194f6:
        bne.w (. + 40)
m68k_0194f6_end:
.org 0x19582
m68k_019582:
        move.w 0xf378:w,%d0
m68k_019582_end:
.org 0x19586
m68k_019586:
        lsl.w #0x1,%d0
m68k_019586_end:
.org 0x19588
m68k_019588:
        lea.l 0xf500:w,%a0
m68k_019588_end:
.org 0x1958C
m68k_01958c:
        move.w (%a0, %d0.w),%d1
m68k_01958c_end:
.org 0x19590
m68k_019590:
        cmpi.w #0x4000,%d1
m68k_019590_end:
.org 0x19594
m68k_019594:
        bcs.w (. + 88)
m68k_019594_end:
.org 0x19598
m68k_019598:
        andi.w #0xff,%d1
m68k_019598_end:
.org 0x1959C
m68k_01959c:
        move.w %d1,(%a0, %d0.w)
m68k_01959c_end:
.org 0x195A0
m68k_0195a0:
        lsl.w #0x2,%d1
m68k_0195a0_end:
.org 0x195A2
m68k_0195a2:
        lea.l 0xa150:w,%a1
m68k_0195a2_end:
.org 0x195A6
m68k_0195a6:
        move.w (%a1, %d1.w),%d2
m68k_0195a6_end:
.org 0x195AA
m68k_0195aa:
        lsr.w #0x7,%d2
m68k_0195aa_end:
.org 0x195AC
m68k_0195ac:
        move.w 0x2(%a1, %d1.w),%d3
m68k_0195ac_end:
.org 0x195B0
m68k_0195b0:
        lsr.w #0x7,%d3
m68k_0195b0_end:
.org 0x195B2
m68k_0195b2:
        clr.l (%a1, %d1.w)
m68k_0195b2_end:
.org 0x195B6
m68k_0195b6:
        move.w #0x401,0xf612:w
m68k_0195b6_end:
.org 0x195BC
m68k_0195bc:
        move.w #0x5,0xf362:w
m68k_0195bc_end:
.org 0x195C2
m68k_0195c2:
        clr.w 0xf36a:w
m68k_0195c2_end:
.org 0x195C6
m68k_0195c6:
        lsr.w #0x3,%d2
m68k_0195c6_end:
.org 0x195C8
m68k_0195c8:
        ori.w #0x80,%d2
m68k_0195c8_end:
.org 0x195CC
m68k_0195cc:
        lsr.w #0x3,%d3
m68k_0195cc_end:
.org 0x195CE
m68k_0195ce:
        lea.l 0xafaa:w,%a0
m68k_0195ce_end:
.org 0x195D2
m68k_0195d2:
        cmp.b (%a0)+,%d2
m68k_0195d2_end:
.org 0x195D4
m68k_0195d4:
        bne.b (. + 10)
m68k_0195d4_end:
.org 0x195D6
m68k_0195d6:
        cmp.b (%a0)+,%d3
m68k_0195d6_end:
.org 0x195D8
m68k_0195d8:
        bne.b (. + -6)
m68k_0195d8_end:
.org 0x195DA
m68k_0195da:
        bra.w (. + 8)
m68k_0195da_end:
.org 0x195DE
m68k_0195de:
        addq.w #0x1,%a0
m68k_0195de_end:
.org 0x195E0
m68k_0195e0:
        bra.b (. + -14)
m68k_0195e0_end:
.org 0x195E2
m68k_0195e2:
        andi.b #0x7f,-0x2(%a0)
m68k_0195e2_end:
.org 0x195E8
m68k_0195e8:
        addq.w #0x1,0xf6d0:w
m68k_0195e8_end:
.org 0x195EC
m68k_0195ec:
        rts
m68k_0195ec_end:
.org 0x196A6
m68k_0196a6:
        jsr 0x20088:l
m68k_0196a6_end:
.org 0x196AC
m68k_0196ac:
        cmpi.w #0x408,0xf612:w
m68k_0196ac_end:
.org 0x196B2
m68k_0196b2:
        bne.w (. + 26)
m68k_0196b2_end:
.org 0x196B6
m68k_0196b6:
        clr.w 0xf36a:w
m68k_0196b6_end:
.org 0x196BA
m68k_0196ba:
        move.w #0x8c,0xf600:w
m68k_0196ba_end:
.org 0x196C0
m68k_0196c0:
        addq.w #0x1,0xf362:w
m68k_0196c0_end:
.org 0x196C4
m68k_0196c4:
        move.l #0xaba7e,0xf6c0:w
m68k_0196c4_end:
.org 0x196CC
m68k_0196cc:
        rts
m68k_0196cc_end:
.org 0x196CE
m68k_0196ce:
        addq.w #0x1,0xf362:w
m68k_0196ce_end:
.org 0x196D2
m68k_0196d2:
        move.w #0x103,%d0
m68k_0196d2_end:
.org 0x196D6
m68k_0196d6:
        move.w %d0,0xaf80:w
m68k_0196d6_end:
.org 0x196DA
m68k_0196da:
        jsr 0x676f2:l
m68k_0196da_end:
.org 0x196E0
m68k_0196e0:
        rts
m68k_0196e0_end:
.org 0x196E2
m68k_0196e2:
        cmpi.w #0xa,0xf36a:w
m68k_0196e2_end:
.org 0x196E8
m68k_0196e8:
        bcs.b (. + 16)
m68k_0196e8_end:
.org 0x196EA
m68k_0196ea:
        addq.w #0x1,0xf362:w
m68k_0196ea_end:
.org 0x196EE
m68k_0196ee:
        move.w #0x8,0xcfd2:w
m68k_0196ee_end:
.org 0x196F4
m68k_0196f4:
        bra.w (. + 70)
m68k_0196f4_end:
.org 0x196F8
m68k_0196f8:
        btst.b #0x1,0xf6d7:w
m68k_0196f8_end:
.org 0x196FE
m68k_0196fe:
        beq.w (. + 22)
m68k_0196fe_end:
.org 0x19702
m68k_019702:
        cmpi.w #0x4,0xf36a:w
m68k_019702_end:
.org 0x19708
m68k_019708:
        bne.w (. + 12)
m68k_019708_end:
.org 0x1970C
m68k_01970c:
        addi.l #0x18,0xf6c0:w
m68k_01970c_end:
.org 0x19714
m68k_019714:
        movea.l 0xf6c0:w,%a0
m68k_019714_end:
.org 0x19718
m68k_019718:
        move.l #0xc0000006,%d0
m68k_019718_end:
.org 0x1971E
m68k_01971e:
        move.w #0x2,%d1
m68k_01971e_end:
.org 0x19722
m68k_019722:
        move.w 0xf36a:w,%d2
m68k_019722_end:
.org 0x19726
m68k_019726:
        lsl.w #0x8,%d2
m68k_019726_end:
.org 0x19728
m68k_019728:
        addi.w #0xc040,%d2
m68k_019728_end:
.org 0x1972C
m68k_01972c:
        jsr 0x26bfa:l
m68k_01972c_end:
.org 0x19732
m68k_019732:
        move.l %a0,0xf6c0:w
m68k_019732_end:
.org 0x19736
m68k_019736:
        addq.w #0x1,0xf36a:w
m68k_019736_end:
.org 0x1973A
m68k_01973a:
        rts
m68k_01973a_end:
.org 0x1973C
m68k_01973c:
        bsr.w (. + 126)
m68k_01973c_end:
.org 0x19740
m68k_019740:
        bsr.w (. + 230)
m68k_019740_end:
.org 0x19744
m68k_019744:
        tst.w 0xcfd2:w
m68k_019744_end:
.org 0x19748
m68k_019748:
        beq.w (. + 28)
m68k_019748_end:
.org 0x1974C
m68k_01974c:
        subq.w #0x1,0xcfd2:w
m68k_01974c_end:
.org 0x19750
m68k_019750:
        cmpi.w #0x8,0xcfd2:w
m68k_019750_end:
.org 0x19756
m68k_019756:
        bls.w (. + 58)
m68k_019756_end:
.org 0x1975A
m68k_01975a:
        move.w #0x8,0xcfd2:w
m68k_01975a_end:
.org 0x19760
m68k_019760:
        bra.w (. + 48)
m68k_019760_end:
.org 0x19764
m68k_019764:
        btst.b #0x5,0xf603:w
m68k_019764_end:
.org 0x1976A
m68k_01976a:
        beq.w (. + 38)
m68k_01976a_end:
.org 0x1976E
m68k_01976e:
        move.w #0xac,%d0
m68k_01976e_end:
.org 0x19772
m68k_019772:
        jsr 0x808a:l
m68k_019772_end:
.org 0x19778
m68k_019778:
        addq.w #0x1,0xf362:w
m68k_019778_end:
.org 0x1977C
m68k_01977c:
        move.w 0xf612:w,0xf38a:w
m68k_01977c_end:
.org 0x19782
m68k_019782:
        move.w #0x6,0xf3b0:w
m68k_019782_end:
.org 0x19788
m68k_019788:
        clr.w 0xf36a:w
m68k_019788_end:
.org 0x1978C
m68k_01978c:
        bra.w (. + 44)
m68k_01978c_end:
.org 0x19790
m68k_019790:
        btst.b #0x4,0xf603:w
m68k_019790_end:
.org 0x19796
m68k_019796:
        beq.b (. + 34)
m68k_019796_end:
.org 0x19798
m68k_019798:
        tst.w 0xf6f6:w
m68k_019798_end:
.org 0x1979C
m68k_01979c:
        bne.b (. + 28)
m68k_01979c_end:
.org 0x1979E
m68k_01979e:
        addq.w #0x1,0xf362:w
m68k_01979e_end:
.org 0x197A2
m68k_0197a2:
        move.w 0xf612:w,0xf38a:w
m68k_0197a2_end:
.org 0x197A8
m68k_0197a8:
        move.w #0x5,0xf3b0:w
m68k_0197a8_end:
.org 0x197AE
m68k_0197ae:
        clr.w 0xf36a:w
m68k_0197ae_end:
.org 0x197B2
m68k_0197b2:
        move.w #0xffff,0xa5f8:w
m68k_0197b2_end:
.org 0x197B8
m68k_0197b8:
        rts
m68k_0197b8_end:
.org 0x197BA
m68k_0197ba:
        move.b 0xf602:w,%d0
m68k_0197ba_end:
.org 0x197BE
m68k_0197be:
        andi.w #0x3,%d0
m68k_0197be_end:
.org 0x197C2
m68k_0197c2:
        beq.b (. + 92)
m68k_0197c2_end:
.org 0x197C4
m68k_0197c4:
        subq.w #0x1,0xf608:w
m68k_0197c4_end:
.org 0x197C8
m68k_0197c8:
        bne.w (. + 92)
m68k_0197c8_end:
.org 0x197CC
m68k_0197cc:
        move.w #0xc,0xf608:w
m68k_0197cc_end:
.org 0x197D2
m68k_0197d2:
        btst.l #0x1,%d0
m68k_0197d2_end:
.org 0x197D6
m68k_0197d6:
        bne.w (. + 36)
m68k_0197d6_end:
.org 0x197DA
m68k_0197da:
        subq.w #0x1,0xf6d4:w
m68k_0197da_end:
.org 0x197DE
m68k_0197de:
        bcc.w (. + 70)
m68k_0197de_end:
.org 0x197E2
m68k_0197e2:
        move.w #0x5,%d0
m68k_0197e2_end:
.org 0x197E6
m68k_0197e6:
        btst.b #0x1,0xf6d7:w
m68k_0197e6_end:
.org 0x197EC
m68k_0197ec:
        beq.w (. + 6)
m68k_0197ec_end:
.org 0x197F0
m68k_0197f0:
        subq.w #0x1,%d0
m68k_0197f0_end:
.org 0x197F2
m68k_0197f2:
        move.w %d0,0xf6d4:w
m68k_0197f2_end:
.org 0x197F6
m68k_0197f6:
        bra.w (. + 46)
m68k_0197f6_end:
.org 0x197FA
m68k_0197fa:
        addq.w #0x1,0xf6d4:w
m68k_0197fa_end:
.org 0x197FE
m68k_0197fe:
        move.w #0x5,%d0
m68k_0197fe_end:
.org 0x19802
m68k_019802:
        btst.b #0x1,0xf6d7:w
m68k_019802_end:
.org 0x19808
m68k_019808:
        beq.w (. + 6)
m68k_019808_end:
.org 0x1980C
m68k_01980c:
        subq.w #0x1,%d0
m68k_01980c_end:
.org 0x1980E
m68k_01980e:
        cmp.w 0xf6d4:w,%d0
m68k_01980e_end:
.org 0x19812
m68k_019812:
        bcc.w (. + 18)
m68k_019812_end:
.org 0x19816
m68k_019816:
        clr.w 0xf6d4:w
m68k_019816_end:
.org 0x1981A
m68k_01981a:
        bra.w (. + 10)
m68k_01981a_end:
.org 0x1981E
m68k_01981e:
        move.w #0x1,0xf608:w
m68k_01981e_end:
.org 0x19824
m68k_019824:
        rts
m68k_019824_end:
.org 0x198B4
m68k_0198b4:
        cmpi.w #0xa,0xf36a:w
m68k_0198b4_end:
.org 0x198BA
m68k_0198ba:
        bcs.b (. + 24)
m68k_0198ba_end:
.org 0x198BC
m68k_0198bc:
        move.w 0xf38a:w,0xf612:w
m68k_0198bc_end:
.org 0x198C2
m68k_0198c2:
        move.w 0xf3b0:w,0xf362:w
m68k_0198c2_end:
.org 0x198C8
m68k_0198c8:
        jsr 0x1a25e:l
m68k_0198c8_end:
.org 0x198CE
m68k_0198ce:
        bra.w (. + 8)
m68k_0198ce_end:
.org 0x198D2
m68k_0198d2:
        bsr.w (. + 6)
m68k_0198d2_end:
.org 0x198D6
m68k_0198d6:
        rts
m68k_0198d6_end:
.org 0x198D8
m68k_0198d8:
        move.w 0xf36a:w,%d0
m68k_0198d8_end:
.org 0x198DC
m68k_0198dc:
        lsl.w #0x8,%d0
m68k_0198dc_end:
.org 0x198DE
m68k_0198de:
        move.w #0xc940,%d2
m68k_0198de_end:
.org 0x198E2
m68k_0198e2:
        sub.w %d0,%d2
m68k_0198e2_end:
.org 0x198E4
m68k_0198e4:
        move.l #0xc0000006,%d0
m68k_0198e4_end:
.org 0x198EA
m68k_0198ea:
        move.w #0x2,%d1
m68k_0198ea_end:
.org 0x198EE
m68k_0198ee:
        lea.l 16(%pc),%a0
m68k_0198ee_end:
.org 0x198F2
m68k_0198f2:
        nop
m68k_0198f2_end:
.org 0x198F4
m68k_0198f4:
        jsr 0x26bfa:l
m68k_0198f4_end:
.org 0x198FA
m68k_0198fa:
        addq.w #0x1,0xf36a:w
m68k_0198fa_end:
.org 0x198FE
m68k_0198fe:
        rts
m68k_0198fe_end:
.org 0x19908
m68k_019908:
        move.w #0x407,0xf3c2:w
m68k_019908_end:
.org 0x1990E
m68k_01990e:
        clr.w 0xf3c4:w
m68k_01990e_end:
.org 0x19912
m68k_019912:
        move.w #0x404,0xf612:w
m68k_019912_end:
.org 0x19918
m68k_019918:
        clr.w 0xf362:w
m68k_019918_end:
.org 0x1991C
m68k_01991c:
        clr.w 0xf36a:w
m68k_01991c_end:
.org 0x19920
m68k_019920:
        rts
m68k_019920_end:
.org 0x19922
m68k_019922:
        move.w 0xf6d4:w,%d0
m68k_019922_end:
.org 0x19926
m68k_019926:
        btst.b #0x1,0xf6d7:w
m68k_019926_end:
.org 0x1992C
m68k_01992c:
        beq.b (. + 10)
m68k_01992c_end:
.org 0x1992E
m68k_01992e:
        cmpi.w #0x2,%d0
m68k_01992e_end:
.org 0x19932
m68k_019932:
        bcs.b (. + 4)
m68k_019932_end:
.org 0x19934
m68k_019934:
        addq.w #0x1,%d0
m68k_019934_end:
.org 0x19936
m68k_019936:
        lsl.w #0x1,%d0
m68k_019936_end:
.org 0x19938
m68k_019938:
        move.w 10(%pc, %d0.w),0xf612:w
m68k_019938_end:
.org 0x1993E
m68k_01993e:
        clr.w 0xf362:w
m68k_01993e_end:
.org 0x19942
m68k_019942:
        rts
m68k_019942_end:
.org 0x1997A
m68k_01997a:
        addq.w #0x1,0xf362:w
m68k_01997a_end:
.org 0x1997E
m68k_01997e:
        move.w #0x104,%d0
m68k_01997e_end:
.org 0x19982
m68k_019982:
        move.w %d0,0xaf80:w
m68k_019982_end:
.org 0x19986
m68k_019986:
        jsr 0x676f2:l
m68k_019986_end:
.org 0x1998C
m68k_01998c:
        move.w #0x68,0xf35e:w
m68k_01998c_end:
.org 0x19992
m68k_019992:
        move.w #0x98,0xf360:w
m68k_019992_end:
.org 0x19998
m68k_019998:
        move.w #0x8000,0xf3a6:w
m68k_019998_end:
.org 0x1999E
m68k_01999e:
        rts
m68k_01999e_end:
.org 0x199A0
m68k_0199a0:
        bsr.w (. + 21078)
m68k_0199a0_end:
.org 0x199A4
m68k_0199a4:
        move.w #0x8000,0xf3a6:w
m68k_0199a4_end:
.org 0x199AA
m68k_0199aa:
        move.b 0xf602:w,%d0
m68k_0199aa_end:
.org 0x199AE
m68k_0199ae:
        andi.w #0x2f,%d0
m68k_0199ae_end:
.org 0x199B2
m68k_0199b2:
        beq.b (. + 16)
m68k_0199b2_end:
.org 0x199B4
m68k_0199b4:
        move.w #0x2,0xf3c4:w
m68k_0199b4_end:
.org 0x199BA
m68k_0199ba:
        bsr.w (. + 20266)
m68k_0199ba_end:
.org 0x199BE
m68k_0199be:
        bra.w (. + 26)
m68k_0199be_end:
.org 0x199C2
m68k_0199c2:
        btst.b #0x4,0xf603:w
m68k_0199c2_end:
.org 0x199C8
m68k_0199c8:
        beq.w (. + 16)
m68k_0199c8_end:
.org 0x199CC
m68k_0199cc:
        move.w 0xf38a:w,0xf612:w
m68k_0199cc_end:
.org 0x199D2
m68k_0199d2:
        move.w 0xf3b0:w,0xf362:w
m68k_0199d2_end:
.org 0x199D8
m68k_0199d8:
        rts
m68k_0199d8_end:
.org 0x199DA
m68k_0199da:
        bsr.w (. + 20870)
m68k_0199da_end:
.org 0x199DE
m68k_0199de:
        bsr.w (. + 21016)
m68k_0199de_end:
.org 0x199E2
m68k_0199e2:
        btst.b #0x5,0xf603:w
m68k_0199e2_end:
.org 0x199E8
m68k_0199e8:
        beq.b (. + 100)
m68k_0199e8_end:
.org 0x199EA
m68k_0199ea:
        bsr.w (. + 186)
m68k_0199ea_end:
.org 0x199EE
m68k_0199ee:
        cmpi.w #0xffff,0xf500:w
m68k_0199ee_end:
.org 0x199F4
m68k_0199f4:
        beq.w (. + 174)
m68k_0199f4_end:
.org 0x199F8
m68k_0199f8:
        move.w #0xac,%d0
m68k_0199f8_end:
.org 0x199FC
m68k_0199fc:
        jsr 0x808a:l
m68k_0199fc_end:
.org 0x19A02
m68k_019a02:
        cmpi.w #0xffff,0xf502:w
m68k_019a02_end:
.org 0x19A08
m68k_019a08:
        beq.w (. + 154)
m68k_019a08_end:
.org 0x19A0C
m68k_019a0c:
        move.w #0x405,0xf612:w
m68k_019a0c_end:
.org 0x19A12
m68k_019a12:
        clr.w 0xf362:w
m68k_019a12_end:
.org 0x19A16
m68k_019a16:
        clr.w 0xf36a:w
m68k_019a16_end:
.org 0x19A1A
m68k_019a1a:
        clr.w 0xf656:w
m68k_019a1a_end:
.org 0x19A1E
m68k_019a1e:
        clr.w 0xf378:w
m68k_019a1e_end:
.org 0x19A22
m68k_019a22:
        clr.w 0xf658:w
m68k_019a22_end:
.org 0x19A26
m68k_019a26:
        move.w #0x3,0xf6d2:w
m68k_019a26_end:
.org 0x19A2C
m68k_019a2c:
        move.w #0x104,%d0
m68k_019a2c_end:
.org 0x19A30
m68k_019a30:
        cmpi.w #0x412,0xf38a:w
m68k_019a30_end:
.org 0x19A36
m68k_019a36:
        bne.w (. + 8)
m68k_019a36_end:
.org 0x19A3A
m68k_019a3a:
        move.w #0x141,%d0
m68k_019a3a_end:
.org 0x19A3E
m68k_019a3e:
        move.w %d0,0xaf80:w
m68k_019a3e_end:
.org 0x19A42
m68k_019a42:
        jsr 0x676f2:l
m68k_019a42_end:
.org 0x19A48
m68k_019a48:
        bra.w (. + 90)
m68k_019a48_end:
.org 0x19A4C
m68k_019a4c:
        btst.b #0x4,0xf603:w
m68k_019a4c_end:
.org 0x19A52
m68k_019a52:
        beq.b (. + 20)
m68k_019a52_end:
.org 0x19A54
m68k_019a54:
        move.w #0x8000,0xf3a6:w
m68k_019a54_end:
.org 0x19A5A
m68k_019a5a:
        move.w 0xf38a:w,0xf612:w
m68k_019a5a_end:
.org 0x19A60
m68k_019a60:
        move.w 0xf3b0:w,0xf362:w
m68k_019a60_end:
.org 0x19A66
m68k_019a66:
        cmpi.w #0x4,0xf6d2:w
m68k_019a66_end:
.org 0x19A6C
m68k_019a6c:
        beq.w (. + 14)
m68k_019a6c_end:
.org 0x19A70
m68k_019a70:
        cmpi.w #0x3,0xf6d2:w
m68k_019a70_end:
.org 0x19A76
m68k_019a76:
        bne.w (. + 44)
m68k_019a76_end:
.org 0x19A7A
m68k_019a7a:
        btst.b #0x7,0xf603:w
m68k_019a7a_end:
.org 0x19A80
m68k_019a80:
        beq.w (. + 34)
m68k_019a80_end:
.org 0x19A84
m68k_019a84:
        move.w #0xac,%d0
m68k_019a84_end:
.org 0x19A88
m68k_019a88:
        jsr 0x808a:l
m68k_019a88_end:
.org 0x19A8E
m68k_019a8e:
        move.w #0x407,0xf612:w
m68k_019a8e_end:
.org 0x19A94
m68k_019a94:
        clr.w 0xf362:w
m68k_019a94_end:
.org 0x19A98
m68k_019a98:
        move.w #0xffff,0xa5f8:w
m68k_019a98_end:
.org 0x19A9E
m68k_019a9e:
        clr.w 0xf6d2:w
m68k_019a9e_end:
.org 0x19AA2
m68k_019aa2:
        rts
m68k_019aa2_end:
.org 0x19AA4
m68k_019aa4:
        lea.l 0xa5f8:w,%a0
m68k_019aa4_end:
.org 0x19AA8
m68k_019aa8:
        lea.l 0xa150:w,%a1
m68k_019aa8_end:
.org 0x19AAC
m68k_019aac:
        lea.l 0xf500:w,%a2
m68k_019aac_end:
.org 0x19AB0
m68k_019ab0:
        clr.w 0xf636:w
m68k_019ab0_end:
.org 0x19AB4
m68k_019ab4:
        move.w 0xf35e:w,%d1
m68k_019ab4_end:
.org 0x19AB8
m68k_019ab8:
        move.w %d1,%d2
m68k_019ab8_end:
.org 0x19ABA
m68k_019aba:
        addi.w #0x10,%d2
m68k_019aba_end:
.org 0x19ABE
m68k_019abe:
        move.w 0xf360:w,%d3
m68k_019abe_end:
.org 0x19AC2
m68k_019ac2:
        move.w %d3,%d4
m68k_019ac2_end:
.org 0x19AC4
m68k_019ac4:
        addi.w #0x10,%d4
m68k_019ac4_end:
.org 0x19AC8
m68k_019ac8:
        move.w (%a0)+,%d0
m68k_019ac8_end:
.org 0x19ACA
m68k_019aca:
        bmi.b (. + 44)
m68k_019aca_end:
.org 0x19ACC
m68k_019acc:
        lsl.w #0x2,%d0
m68k_019acc_end:
.org 0x19ACE
m68k_019ace:
        move.w (%a1, %d0.w),%d5
m68k_019ace_end:
.org 0x19AD2
m68k_019ad2:
        lsr.w #0x7,%d5
m68k_019ad2_end:
.org 0x19AD4
m68k_019ad4:
        cmp.w %d1,%d5
m68k_019ad4_end:
.org 0x19AD6
m68k_019ad6:
        bcs.b (. + -14)
m68k_019ad6_end:
.org 0x19AD8
m68k_019ad8:
        cmp.w %d2,%d5
m68k_019ad8_end:
.org 0x19ADA
m68k_019ada:
        bcc.b (. + -18)
m68k_019ada_end:
.org 0x19ADC
m68k_019adc:
        move.w 0x2(%a1, %d0.w),%d5
m68k_019adc_end:
.org 0x19AE0
m68k_019ae0:
        lsr.w #0x7,%d5
m68k_019ae0_end:
.org 0x19AE2
m68k_019ae2:
        cmp.w %d3,%d5
m68k_019ae2_end:
.org 0x19AE4
m68k_019ae4:
        bcs.b (. + -28)
m68k_019ae4_end:
.org 0x19AE6
m68k_019ae6:
        cmp.w %d4,%d5
m68k_019ae6_end:
.org 0x19AE8
m68k_019ae8:
        bcc.b (. + -32)
m68k_019ae8_end:
.org 0x19AEA
m68k_019aea:
        lsr.w #0x2,%d0
m68k_019aea_end:
.org 0x19AEC
m68k_019aec:
        move.w %d0,(%a2)+
m68k_019aec_end:
.org 0x19AEE
m68k_019aee:
        addi.w #0x1,0xf636:w
m68k_019aee_end:
.org 0x19AF4
m68k_019af4:
        bra.b (. + -44)
m68k_019af4_end:
.org 0x19AF6
m68k_019af6:
        move.w #0xffff,(%a2)
m68k_019af6_end:
.org 0x19AFA
m68k_019afa:
        move.w 0xf500:w,%d0
m68k_019afa_end:
.org 0x19AFE
m68k_019afe:
        move.w %d0,0xf3a6:w
m68k_019afe_end:
.org 0x19B02
m68k_019b02:
        tst.w %d0
m68k_019b02_end:
.org 0x19B04
m68k_019b04:
        bmi.w (. + 38)
m68k_019b04_end:
.org 0x19B08
m68k_019b08:
        lea.l 0xa5f8:w,%a0
m68k_019b08_end:
.org 0x19B0C
m68k_019b0c:
        lea.l 0xafca:w,%a1
m68k_019b0c_end:
.org 0x19B10
m68k_019b10:
        move.w (%a0)+,(%a1)+
m68k_019b10_end:
.org 0x19B12
m68k_019b12:
        bpl.b (. + -2)
m68k_019b12_end:
.org 0x19B14
m68k_019b14:
        move.w %d0,0xa5f8:w
m68k_019b14_end:
.org 0x19B18
m68k_019b18:
        move.w #0xffff,0xa5fa:w
m68k_019b18_end:
.org 0x19B1E
m68k_019b1e:
        move.w 0xf38a:w,0xf612:w
m68k_019b1e_end:
.org 0x19B24
m68k_019b24:
        move.w 0xf3b0:w,0xf362:w
m68k_019b24_end:
.org 0x19B2A
m68k_019b2a:
        rts
m68k_019b2a_end:
.org 0x19FC2
m68k_019fc2:
        addq.w #0x1,0xf362:w
m68k_019fc2_end:
.org 0x19FC6
m68k_019fc6:
        move.w 0xf740:w,%d0
m68k_019fc6_end:
.org 0x19FCA
m68k_019fca:
        jsr 0x676f2:l
m68k_019fca_end:
.org 0x19FD0
m68k_019fd0:
        move.w #0x12c,0xf608:w
m68k_019fd0_end:
.org 0x19FD6
m68k_019fd6:
        rts
m68k_019fd6_end:
.org 0x19FD8
m68k_019fd8:
        subq.w #0x1,0xf608:w
m68k_019fd8_end:
.org 0x19FDC
m68k_019fdc:
        beq.w (. + 14)
m68k_019fdc_end:
.org 0x19FE0
m68k_019fe0:
        btst.b #0x5,0xf603:w
m68k_019fe0_end:
.org 0x19FE6
m68k_019fe6:
        beq.w (. + 30)
m68k_019fe6_end:
.org 0x19FEA
m68k_019fea:
        move.w 0xf612:w,0xf3c2:w
m68k_019fea_end:
.org 0x19FF0
m68k_019ff0:
        move.w #0x2,0xf3c4:w
m68k_019ff0_end:
.org 0x19FF6
m68k_019ff6:
        move.w #0x404,0xf612:w
m68k_019ff6_end:
.org 0x19FFC
m68k_019ffc:
        clr.w 0xf36a:w
m68k_019ffc_end:
.org 0x1A000
m68k_01a000:
        clr.w 0xf6d2:w
m68k_01a000_end:
.org 0x1A004
m68k_01a004:
        rts
m68k_01a004_end:
.org 0x1A006
m68k_01a006:
        move.w #0xb8,0xf600:w
m68k_01a006_end:
.org 0x1A00C
m68k_01a00c:
        rts
m68k_01a00c_end:
.org 0x1A0A2
m68k_01a0a2:
        tst.w 0xf6c4:w
m68k_01a0a2_end:
.org 0x1A0A6
m68k_01a0a6:
        bne.w (. + 194)
m68k_01a0a6_end:
.org 0x1A0AA
m68k_01a0aa:
        tst.w 0xf352:w
m68k_01a0aa_end:
.org 0x1A0AE
m68k_01a0ae:
        bne.w (. + 186)
m68k_01a0ae_end:
.org 0x1A0B2
m68k_01a0b2:
        move.w 0xf68a:w,%d0
m68k_01a0b2_end:
.org 0x1A0B6
m68k_01a0b6:
        lea.l 0xf427:w,%a0
m68k_01a0b6_end:
.org 0x1A0BA
m68k_01a0ba:
        move.b (%a0, %d0.w),%d1
m68k_01a0ba_end:
.org 0x1A0BE
m68k_01a0be:
        cmp.w 0xf67c:w,%d1
m68k_01a0be_end:
.org 0x1A0C2
m68k_01a0c2:
        beq.w (. + 12)
m68k_01a0c2_end:
.org 0x1A0C6
m68k_01a0c6:
        cmp.w 0xf67e:w,%d1
m68k_01a0c6_end:
.org 0x1A0CA
m68k_01a0ca:
        bne.w (. + 158)
m68k_01a0ca_end:
.org 0x1A0CE
m68k_01a0ce:
        lea.l 0xa050:w,%a0
m68k_01a0ce_end:
.org 0x1A0D2
m68k_01a0d2:
        move.w #0xff,%d1
m68k_01a0d2_end:
.org 0x1A0D6
m68k_01a0d6:
        cmp.b (%a0, %d1.w),%d0
m68k_01a0d6_end:
.org 0x1A0DA
m68k_01a0da:
        beq.w (. + 8)
m68k_01a0da_end:
.org 0x1A0DE
m68k_01a0de:
        dbra %d1,(. + -8)
m68k_01a0de_end:
.org 0x1A0E2
m68k_01a0e2:
        lea.l 0xcc00:w,%a0
m68k_01a0e2_end:
.org 0x1A0E6
m68k_01a0e6:
        move.b (%a0, %d1.w),%d1
m68k_01a0e6_end:
.org 0x1A0EA
m68k_01a0ea:
        andi.w #0x3f,%d1
m68k_01a0ea_end:
.org 0x1A0EE
m68k_01a0ee:
        cmpi.w #0x28,%d1
m68k_01a0ee_end:
.org 0x1A0F2
m68k_01a0f2:
        bls.w (. + 12)
m68k_01a0f2_end:
.org 0x1A0F6
m68k_01a0f6:
        subi.w #0x29,%d1
m68k_01a0f6_end:
.org 0x1A0FA
m68k_01a0fa:
        bra.w (. + 12)
m68k_01a0fa_end:
.org 0x1A0FE
m68k_01a0fe:
        lea.l 0xf427:w,%a0
m68k_01a0fe_end:
.org 0x1A102
m68k_01a102:
        move.b (%a0, %d1.w),%d1
m68k_01a102_end:
.org 0x1A106
m68k_01a106:
        cmp.w 0xf67c:w,%d1
m68k_01a106_end:
.org 0x1A10A
m68k_01a10a:
        beq.w (. + 12)
m68k_01a10a_end:
.org 0x1A10E
m68k_01a10e:
        cmp.w 0xf67e:w,%d1
m68k_01a10e_end:
.org 0x1A112
m68k_01a112:
        bne.w (. + 86)
m68k_01a112_end:
.org 0x1A116
m68k_01a116:
        move.w 0xf67e:w,%d0
m68k_01a116_end:
.org 0x1A11A
m68k_01a11a:
        lsl.w #0x1,%d0
m68k_01a11a_end:
.org 0x1A11C
m68k_01a11c:
        lea.l 0xe640:w,%a0
m68k_01a11c_end:
.org 0x1A120
m68k_01a120:
        move.w (%a0, %d0.w),0xf3d0:w
m68k_01a120_end:
.org 0x1A126
m68k_01a126:
        move.w #0x2,0xf362:w
m68k_01a126_end:
.org 0x1A12C
m68k_01a12c:
        move.w #0xc0,%d0
m68k_01a12c_end:
.org 0x1A130
m68k_01a130:
        jsr 0x676f2:l
m68k_01a130_end:
.org 0x1A136
m68k_01a136:
        clr.w 0xf6d6:w
m68k_01a136_end:
.org 0x1A13A
m68k_01a13a:
        lea.l 0xf427:w,%a0
m68k_01a13a_end:
.org 0x1A13E
m68k_01a13e:
        move.w 0xf68a:w,%d0
m68k_01a13e_end:
.org 0x1A142
m68k_01a142:
        move.b (%a0, %d0.w),%d0
m68k_01a142_end:
.org 0x1A146
m68k_01a146:
        cmp.w 0xf67e:w,%d0
m68k_01a146_end:
.org 0x1A14A
m68k_01a14a:
        bne.w (. + 18)
m68k_01a14a_end:
.org 0x1A14E
m68k_01a14e:
        move.w #0x2,0xf6d6:w
m68k_01a14e_end:
.org 0x1A154
m68k_01a154:
        move.w %d0,0xf68e:w
m68k_01a154_end:
.org 0x1A158
m68k_01a158:
        bra.w (. + 8)
m68k_01a158_end:
.org 0x1A15C
m68k_01a15c:
        move.w %d0,0xf68c:w
m68k_01a15c_end:
.org 0x1A160
m68k_01a160:
        ori.w #0x1,%sr
m68k_01a160_end:
.org 0x1A164
m68k_01a164:
        bra.w (. + 8)
m68k_01a164_end:
.org 0x1A168
m68k_01a168:
        andi.w #0xfffe,%sr
m68k_01a168_end:
.org 0x1A16C
m68k_01a16c:
        rts
m68k_01a16c_end:
.org 0x1A3F4
m68k_01a3f4:
        btst.b #0x4,0xf321:w
m68k_01a3f4_end:
.org 0x1A3FA
m68k_01a3fa:
        bne.b (. + 52)
m68k_01a3fa_end:
.org 0x1A3FC
m68k_01a3fc:
        lea.l 0xafaa:w,%a2
m68k_01a3fc_end:
.org 0x1A400
m68k_01a400:
        move.w #0xf,%d4
m68k_01a400_end:
.org 0x1A404
m68k_01a404:
        clr.w %d0
m68k_01a404_end:
.org 0x1A406
m68k_01a406:
        move.b (%a2)+,%d0
m68k_01a406_end:
.org 0x1A408
m68k_01a408:
        beq.w (. + 32)
m68k_01a408_end:
.org 0x1A40C
m68k_01a40c:
        bmi.w (. + 28)
m68k_01a40c_end:
.org 0x1A410
m68k_01a410:
        lsl.w #0x3,%d0
m68k_01a410_end:
.org 0x1A412
m68k_01a412:
        clr.w %d1
m68k_01a412_end:
.org 0x1A414
m68k_01a414:
        move.b (%a2)+,%d1
m68k_01a414_end:
.org 0x1A416
m68k_01a416:
        lsl.w #0x3,%d1
m68k_01a416_end:
.org 0x1A418
m68k_01a418:
        clr.w %d2
m68k_01a418_end:
.org 0x1A41A
m68k_01a41a:
        lea.l 20(%pc),%a0
m68k_01a41a_end:
.org 0x1A41E
m68k_01a41e:
        jsr 0xac08:l
m68k_01a41e_end:
.org 0x1A424
m68k_01a424:
        bra.w (. + 6)
m68k_01a424_end:
.org 0x1A428
m68k_01a428:
        addq.w #0x1,%a2
m68k_01a428_end:
.org 0x1A42A
m68k_01a42a:
        dbra %d4,(. + -38)
m68k_01a42a_end:
.org 0x1A42E
m68k_01a42e:
        rts
m68k_01a42e_end:
.org 0x1B098
m68k_01b098:
        lea.l 0xa050:w,%a0
m68k_01b098_end:
.org 0x1B09C
m68k_01b09c:
        move.w 0xf68a:w,%d0
m68k_01b09c_end:
.org 0x1B0A0
m68k_01b0a0:
        lea.l 0xa550:w,%a1
m68k_01b0a0_end:
.org 0x1B0A4
m68k_01b0a4:
        bsr.w (. + 14)
m68k_01b0a4_end:
.org 0x1B0A8
m68k_01b0a8:
        lea.l 0xa5a4:w,%a1
m68k_01b0a8_end:
.org 0x1B0AC
m68k_01b0ac:
        bsr.w (. + 6)
m68k_01b0ac_end:
.org 0x1B0B0
m68k_01b0b0:
        rts
m68k_01b0b0_end:
.org 0x1B0B2
m68k_01b0b2:
        move.w (%a1)+,%d1
m68k_01b0b2_end:
.org 0x1B0B4
m68k_01b0b4:
        bmi.b (. + 12)
m68k_01b0b4_end:
.org 0x1B0B6
m68k_01b0b6:
        andi.w #0xff,%d1
m68k_01b0b6_end:
.org 0x1B0BA
m68k_01b0ba:
        move.b %d0,(%a0, %d1.w)
m68k_01b0ba_end:
.org 0x1B0BE
m68k_01b0be:
        bra.b (. + -12)
m68k_01b0be_end:
.org 0x1B0C0
m68k_01b0c0:
        rts
m68k_01b0c0_end:
.org 0x1D658
m68k_01d658:
        move.w 0xf612:w,0xf38a:w
m68k_01d658_end:
.org 0x1D65E
m68k_01d65e:
        move.w #0x1,0xf3b0:w
m68k_01d65e_end:
.org 0x1D664
m68k_01d664:
        move.w #0x40a,0xf612:w
m68k_01d664_end:
.org 0x1D66A
m68k_01d66a:
        clr.w 0xf362:w
m68k_01d66a_end:
.org 0x1D66E
m68k_01d66e:
        move.w 0xf6d6:w,%d0
m68k_01d66e_end:
.org 0x1D672
m68k_01d672:
        andi.w #0x2,%d0
m68k_01d672_end:
.org 0x1D676
m68k_01d676:
        lsl.w #0x1,%d0
m68k_01d676_end:
.org 0x1D678
m68k_01d678:
        movea.l 42(%pc, %d0.w),%a0
m68k_01d678_end:
.org 0x1D67C
m68k_01d67c:
        lea.l 0xa5f8:w,%a1
m68k_01d67c_end:
.org 0x1D680
m68k_01d680:
        lea.l 0xa754:w,%a2
m68k_01d680_end:
.org 0x1D684
m68k_01d684:
        lea.l 0xff3cc2:l,%a3
m68k_01d684_end:
.org 0x1D68A
m68k_01d68a:
        move.w (%a0)+,%d0
m68k_01d68a_end:
.org 0x1D68C
m68k_01d68c:
        bmi.b (. + 18)
m68k_01d68c_end:
.org 0x1D68E
m68k_01d68e:
        cmpi.w #0x100,%d0
m68k_01d68e_end:
.org 0x1D692
m68k_01d692:
        bcc.b (. + -8)
m68k_01d692_end:
.org 0x1D694
m68k_01d694:
        tst.b (%a3, %d0.w)
m68k_01d694_end:
.org 0x1D698
m68k_01d698:
        bne.b (. + -14)
m68k_01d698_end:
.org 0x1D69A
m68k_01d69a:
        move.w %d0,(%a1)+
m68k_01d69a_end:
.org 0x1D69C
m68k_01d69c:
        bra.b (. + -18)
m68k_01d69c_end:
.org 0x1D69E
m68k_01d69e:
        move.w #0xffff,(%a1)+
m68k_01d69e_end:
.org 0x1D6A2
m68k_01d6a2:
        rts
m68k_01d6a2_end:
.org 0x1D6AC
m68k_01d6ac:
        move.w #0x98,0xf600:w
m68k_01d6ac_end:
.org 0x1D6B2
m68k_01d6b2:
        addq.w #0x1,0xf362:w
m68k_01d6b2_end:
.org 0x1D6B6
m68k_01d6b6:
        rts
m68k_01d6b6_end:
.org 0x1D6B8
m68k_01d6b8:
        move.w 0xf6d6:w,%d0
m68k_01d6b8_end:
.org 0x1D6BC
m68k_01d6bc:
        lsl.w #0x1,%d0
m68k_01d6bc_end:
.org 0x1D6BE
m68k_01d6be:
        lea.l 0xf6e8:w,%a0
m68k_01d6be_end:
.org 0x1D6C2
m68k_01d6c2:
        tst.w (%a0, %d0.w)
m68k_01d6c2_end:
.org 0x1D6C6
m68k_01d6c6:
        bpl.b (. + 36)
m68k_01d6c6_end:
.org 0x1D6C8
m68k_01d6c8:
        addq.w #0x1,0xf362:w
m68k_01d6c8_end:
.org 0x1D6CC
m68k_01d6cc:
        move.w 0xf3a6:w,0xf3d0:w
m68k_01d6cc_end:
.org 0x1D6D2
m68k_01d6d2:
        move.w #0x110,%d0
m68k_01d6d2_end:
.org 0x1D6D6
m68k_01d6d6:
        move.w %d0,0xaf80:w
m68k_01d6d6_end:
.org 0x1D6DA
m68k_01d6da:
        jsr 0x676f2:l
m68k_01d6da_end:
.org 0x1D6E0
m68k_01d6e0:
        move.w #0x1,0xf652:w
m68k_01d6e0_end:
.org 0x1D6E6
m68k_01d6e6:
        bra.w (. + 8)
m68k_01d6e6_end:
.org 0x1D6EA
m68k_01d6ea:
        addq.w #0x2,0xf362:w
m68k_01d6ea_end:
.org 0x1D6EE
m68k_01d6ee:
        rts
m68k_01d6ee_end:
.org 0x1D6F0
m68k_01d6f0:
        move.b 0xf602:w,%d0
m68k_01d6f0_end:
.org 0x1D6F4
m68k_01d6f4:
        andi.w #0x30,%d0
m68k_01d6f4_end:
.org 0x1D6F8
m68k_01d6f8:
        beq.b (. + 12)
m68k_01d6f8_end:
.org 0x1D6FA
m68k_01d6fa:
        move.w #0x408,0xf612:w
m68k_01d6fa_end:
.org 0x1D700
m68k_01d700:
        clr.w 0xf362:w
m68k_01d700_end:
.org 0x1D704
m68k_01d704:
        rts
m68k_01d704_end:
.org 0x1D706
m68k_01d706:
        tst.w 0xf3a6:w
m68k_01d706_end:
.org 0x1D70A
m68k_01d70a:
        bpl.b (. + 20)
m68k_01d70a_end:
.org 0x1D70C
m68k_01d70c:
        move.w #0x408,0xf612:w
m68k_01d70c_end:
.org 0x1D712
m68k_01d712:
        clr.w 0xf362:w
m68k_01d712_end:
.org 0x1D716
m68k_01d716:
        clr.w 0xf36a:w
m68k_01d716_end:
.org 0x1D71A
m68k_01d71a:
        bra.w (. + 34)
m68k_01d71a_end:
.org 0x1D71E
m68k_01d71e:
        addq.w #0x1,0xf362:w
m68k_01d71e_end:
.org 0x1D722
m68k_01d722:
        move.w 0xf3a6:w,0xf3d0:w
m68k_01d722_end:
.org 0x1D728
m68k_01d728:
        move.w #0x10e,%d0
m68k_01d728_end:
.org 0x1D72C
m68k_01d72c:
        move.w %d0,0xaf80:w
m68k_01d72c_end:
.org 0x1D730
m68k_01d730:
        jsr 0x676f2:l
m68k_01d730_end:
.org 0x1D736
m68k_01d736:
        move.w #0x1,0xf652:w
m68k_01d736_end:
.org 0x1D73C
m68k_01d73c:
        rts
m68k_01d73c_end:
.org 0x1D73E
m68k_01d73e:
        move.l #0xc0000008,%d0
m68k_01d73e_end:
.org 0x1D744
m68k_01d744:
        move.w #0x7,%d1
m68k_01d744_end:
.org 0x1D748
m68k_01d748:
        move.w #0xc4a2,%d2
m68k_01d748_end:
.org 0x1D74C
m68k_01d74c:
        lea.l 0xabbc2:l,%a0
m68k_01d74c_end:
.org 0x1D752
m68k_01d752:
        jsr 0x26bfa:l
m68k_01d752_end:
.org 0x1D758
m68k_01d758:
        clr.w 0xf6d4:w
m68k_01d758_end:
.org 0x1D75C
m68k_01d75c:
        move.w #0x9c,0xf600:w
m68k_01d75c_end:
.org 0x1D762
m68k_01d762:
        addq.w #0x1,0xf362:w
m68k_01d762_end:
.org 0x1D766
m68k_01d766:
        move.w #0x8,0xcfd2:w
m68k_01d766_end:
.org 0x1D76C
m68k_01d76c:
        rts
m68k_01d76c_end:
.org 0x1D76E
m68k_01d76e:
        bsr.w (. + 88)
m68k_01d76e_end:
.org 0x1D772
m68k_01d772:
        bsr.w (. + 122)
m68k_01d772_end:
.org 0x1D776
m68k_01d776:
        tst.w 0xcfd2:w
m68k_01d776_end:
.org 0x1D77A
m68k_01d77a:
        beq.w (. + 28)
m68k_01d77a_end:
.org 0x1D77E
m68k_01d77e:
        subq.w #0x1,0xcfd2:w
m68k_01d77e_end:
.org 0x1D782
m68k_01d782:
        cmpi.w #0x8,0xcfd2:w
m68k_01d782_end:
.org 0x1D788
m68k_01d788:
        bls.w (. + 42)
m68k_01d788_end:
.org 0x1D78C
m68k_01d78c:
        move.w #0x8,0xcfd2:w
m68k_01d78c_end:
.org 0x1D792
m68k_01d792:
        bra.w (. + 32)
m68k_01d792_end:
.org 0x1D796
m68k_01d796:
        btst.b #0x5,0xf603:w
m68k_01d796_end:
.org 0x1D79C
m68k_01d79c:
        beq.w (. + 22)
m68k_01d79c_end:
.org 0x1D7A0
m68k_01d7a0:
        move.w #0xac,%d0
m68k_01d7a0_end:
.org 0x1D7A4
m68k_01d7a4:
        jsr 0x808a:l
m68k_01d7a4_end:
.org 0x1D7AA
m68k_01d7aa:
        addq.w #0x1,0xf362:w
m68k_01d7aa_end:
.org 0x1D7AE
m68k_01d7ae:
        bra.w (. + 22)
m68k_01d7ae_end:
.org 0x1D7B2
m68k_01d7b2:
        btst.b #0x4,0xf603:w
m68k_01d7b2_end:
.org 0x1D7B8
m68k_01d7b8:
        beq.b (. + 12)
m68k_01d7b8_end:
.org 0x1D7BA
m68k_01d7ba:
        move.w #0x1,0xf6d4:w
m68k_01d7ba_end:
.org 0x1D7C0
m68k_01d7c0:
        addq.w #0x1,0xf362:w
m68k_01d7c0_end:
.org 0x1D7C4
m68k_01d7c4:
        rts
m68k_01d7c4_end:
.org 0x1D7C6
m68k_01d7c6:
        move.b 0xf602:w,%d0
m68k_01d7c6_end:
.org 0x1D7CA
m68k_01d7ca:
        andi.w #0x3,%d0
m68k_01d7ca_end:
.org 0x1D7CE
m68k_01d7ce:
        beq.b (. + 22)
m68k_01d7ce_end:
.org 0x1D7D0
m68k_01d7d0:
        subq.w #0x1,0xf608:w
m68k_01d7d0_end:
.org 0x1D7D4
m68k_01d7d4:
        bne.b (. + 22)
m68k_01d7d4_end:
.org 0x1D7D6
m68k_01d7d6:
        move.w #0xc,0xf608:w
m68k_01d7d6_end:
.org 0x1D7DC
m68k_01d7dc:
        eori.w #0x1,0xf6d4:w
m68k_01d7dc_end:
.org 0x1D7E2
m68k_01d7e2:
        bra.b (. + 8)
m68k_01d7e2_end:
.org 0x1D7E4
m68k_01d7e4:
        move.w #0x1,0xf608:w
m68k_01d7e4_end:
.org 0x1D7EA
m68k_01d7ea:
        rts
m68k_01d7ea_end:
.org 0x1D7EC
m68k_01d7ec:
        btst.b #0x5,0xf603:w
m68k_01d7ec_end:
.org 0x1D7F2
m68k_01d7f2:
        bne.w (. + 58)
m68k_01d7f2_end:
.org 0x1D7F6
m68k_01d7f6:
        move.b 0xf602:w,%d0
m68k_01d7f6_end:
.org 0x1D7FA
m68k_01d7fa:
        andi.w #0x3,%d0
m68k_01d7fa_end:
.org 0x1D7FE
m68k_01d7fe:
        bne.w (. + 12)
m68k_01d7fe_end:
.org 0x1D802
m68k_01d802:
        btst.b #0x3,0xf321:w
m68k_01d802_end:
.org 0x1D808
m68k_01d808:
        bne.b (. + 36)
m68k_01d808_end:
.org 0x1D80A
m68k_01d80a:
        lea.l 34(%pc),%a0
m68k_01d80a_end:
.org 0x1D80E
m68k_01d80e:
        nop
m68k_01d80e_end:
.org 0x1D810
m68k_01d810:
        move.w 0xf6d4:w,%d0
m68k_01d810_end:
.org 0x1D814
m68k_01d814:
        move.w %d0,%d1
m68k_01d814_end:
.org 0x1D816
m68k_01d816:
        lsl.w #0x1,%d0
m68k_01d816_end:
.org 0x1D818
m68k_01d818:
        add.w %d1,%d0
m68k_01d818_end:
.org 0x1D81A
m68k_01d81a:
        lsl.w #0x3,%d0
m68k_01d81a_end:
.org 0x1D81C
m68k_01d81c:
        addi.w #0x48,%d0
m68k_01d81c_end:
.org 0x1D820
m68k_01d820:
        move.w #0x88,%d1
m68k_01d820_end:
.org 0x1D824
m68k_01d824:
        clr.w %d2
m68k_01d824_end:
.org 0x1D826
m68k_01d826:
        jsr 0xac08:l
m68k_01d826_end:
.org 0x1D82C
m68k_01d82c:
        rts
m68k_01d82c_end:
.org 0x1D890
m68k_01d890:
        move.l #0xc0000008,%d0
m68k_01d890_end:
.org 0x1D896
m68k_01d896:
        move.w #0x7,%d1
m68k_01d896_end:
.org 0x1D89A
m68k_01d89a:
        move.w #0xc4a2,%d2
m68k_01d89a_end:
.org 0x1D89E
m68k_01d89e:
        lea.l 0xabc02:l,%a0
m68k_01d89e_end:
.org 0x1D8A4
m68k_01d8a4:
        jsr 0x26bfa:l
m68k_01d8a4_end:
.org 0x1D8AA
m68k_01d8aa:
        tst.w 0xf6d4:w
m68k_01d8aa_end:
.org 0x1D8AE
m68k_01d8ae:
        bne.w (. + 38)
m68k_01d8ae_end:
.org 0x1D8B2
m68k_01d8b2:
        addq.w #0x1,0xf362:w
m68k_01d8b2_end:
.org 0x1D8B6
m68k_01d8b6:
        move.w 0xf3a6:w,0xf3d0:w
m68k_01d8b6_end:
.org 0x1D8BC
m68k_01d8bc:
        move.w #0x10f,%d0
m68k_01d8bc_end:
.org 0x1D8C0
m68k_01d8c0:
        move.w %d0,0xaf80:w
m68k_01d8c0_end:
.org 0x1D8C4
m68k_01d8c4:
        jsr 0x676f2:l
m68k_01d8c4_end:
.org 0x1D8CA
m68k_01d8ca:
        move.w #0x1,0xf652:w
m68k_01d8ca_end:
.org 0x1D8D0
m68k_01d8d0:
        bra.w (. + 14)
m68k_01d8d0_end:
.org 0x1D8D4
m68k_01d8d4:
        move.w #0x408,0xf612:w
m68k_01d8d4_end:
.org 0x1D8DA
m68k_01d8da:
        clr.w 0xf362:w
m68k_01d8da_end:
.org 0x1D8DE
m68k_01d8de:
        rts
m68k_01d8de_end:
.org 0x1D8E0
m68k_01d8e0:
        move.b 0xf602:w,%d0
m68k_01d8e0_end:
.org 0x1D8E4
m68k_01d8e4:
        andi.w #0x60,%d0
m68k_01d8e4_end:
.org 0x1D8E8
m68k_01d8e8:
        beq.w (. + 48)
m68k_01d8e8_end:
.org 0x1D8EC
m68k_01d8ec:
        move.w #0xa0,0xf600:w
m68k_01d8ec_end:
.org 0x1D8F2
m68k_01d8f2:
        addq.w #0x1,0xf362:w
m68k_01d8f2_end:
.org 0x1D8F6
m68k_01d8f6:
        lea.l 34(%pc),%a0
m68k_01d8f6_end:
.org 0x1D8FA
m68k_01d8fa:
        move.l #0xc0000026,%d0
m68k_01d8fa_end:
.org 0x1D900
m68k_01d900:
        move.w #0x7,%d1
m68k_01d900_end:
.org 0x1D904
m68k_01d904:
        move.w #0xca02,%d2
m68k_01d904_end:
.org 0x1D908
m68k_01d908:
        jsr 0x26bfa:l
m68k_01d908_end:
.org 0x1D90E
m68k_01d90e:
        bclr.b #0x6,0xf3a4:w
m68k_01d90e_end:
.org 0x1D914
m68k_01d914:
        bsr.w (. + -18182)
m68k_01d914_end:
.org 0x1D918
m68k_01d918:
        rts
m68k_01d918_end:
.org 0x1D936
m68k_01d936:
        bsr.w (. + 24)
m68k_01d936_end:
.org 0x1D93A
m68k_01d93a:
        move.w #0x1,0xf6f6:w
m68k_01d93a_end:
.org 0x1D940
m68k_01d940:
        lea.l 0xa050:w,%a0
m68k_01d940_end:
.org 0x1D944
m68k_01d944:
        move.w 0xf3a6:w,%d0
m68k_01d944_end:
.org 0x1D948
m68k_01d948:
        clr.b (%a0, %d0.w)
m68k_01d948_end:
.org 0x1D94C
m68k_01d94c:
        rts
m68k_01d94c_end:
.org 0x1D94E
m68k_01d94e:
        move.w 0xf68a:w,%d0
m68k_01d94e_end:
.org 0x1D952
m68k_01d952:
        btst.b #0x1,0xf6d7:w
m68k_01d952_end:
.org 0x1D958
m68k_01d958:
        bne.w (. + 22)
m68k_01d958_end:
.org 0x1D95C
m68k_01d95c:
        lea.l 0xa027:w,%a0
m68k_01d95c_end:
.org 0x1D960
m68k_01d960:
        clr.w %d1
m68k_01d960_end:
.org 0x1D962
m68k_01d962:
        move.b (%a0, %d0.w),%d1
m68k_01d962_end:
.org 0x1D966
m68k_01d966:
        lea.l 0xa550:w,%a0
m68k_01d966_end:
.org 0x1D96A
m68k_01d96a:
        bra.w (. + 18)
m68k_01d96a_end:
.org 0x1D96E
m68k_01d96e:
        lea.l 0xf45e:w,%a0
m68k_01d96e_end:
.org 0x1D972
m68k_01d972:
        lsl.w #0x1,%d0
m68k_01d972_end:
.org 0x1D974
m68k_01d974:
        move.w (%a0, %d0.w),%d1
m68k_01d974_end:
.org 0x1D978
m68k_01d978:
        lea.l 0xa5a4:w,%a0
m68k_01d978_end:
.org 0x1D97C
m68k_01d97c:
        move.w (%a0)+,%d0
m68k_01d97c_end:
.org 0x1D97E
m68k_01d97e:
        bmi.w (. + 18)
m68k_01d97e_end:
.org 0x1D982
m68k_01d982:
        cmp.w %d1,%d0
m68k_01d982_end:
.org 0x1D984
m68k_01d984:
        bne.b (. + -8)
m68k_01d984_end:
.org 0x1D986
m68k_01d986:
        move.w #0x408,0xf612:w
m68k_01d986_end:
.org 0x1D98C
m68k_01d98c:
        bra.w (. + 10)
m68k_01d98c_end:
.org 0x1D990
m68k_01d990:
        move.w #0x407,0xf612:w
m68k_01d990_end:
.org 0x1D996
m68k_01d996:
        clr.w 0xf362:w
m68k_01d996_end:
.org 0x1D99A
m68k_01d99a:
        rts
m68k_01d99a_end:
.org 0x1D9BE
m68k_01d9be:
        move.w 0xf612:w,0xf38a:w
m68k_01d9be_end:
.org 0x1D9C4
m68k_01d9c4:
        move.w #0x1,0xf3b0:w
m68k_01d9c4_end:
.org 0x1D9CA
m68k_01d9ca:
        move.w #0x40a,0xf612:w
m68k_01d9ca_end:
.org 0x1D9D0
m68k_01d9d0:
        clr.w 0xf362:w
m68k_01d9d0_end:
.org 0x1D9D4
m68k_01d9d4:
        move.w 0xf6d6:w,%d0
m68k_01d9d4_end:
.org 0x1D9D8
m68k_01d9d8:
        andi.w #0x2,%d0
m68k_01d9d8_end:
.org 0x1D9DC
m68k_01d9dc:
        lsl.w #0x1,%d0
m68k_01d9dc_end:
.org 0x1D9DE
m68k_01d9de:
        movea.l -42(%pc, %d0.w),%a0
m68k_01d9de_end:
.org 0x1D9E2
m68k_01d9e2:
        lea.l 0xa5f8:w,%a1
m68k_01d9e2_end:
.org 0x1D9E6
m68k_01d9e6:
        lea.l 0xa654:w,%a2
m68k_01d9e6_end:
.org 0x1D9EA
m68k_01d9ea:
        lea.l 0xff3cc2:l,%a3
m68k_01d9ea_end:
.org 0x1D9F0
m68k_01d9f0:
        move.w (%a0)+,%d0
m68k_01d9f0_end:
.org 0x1D9F2
m68k_01d9f2:
        bmi.b (. + 24)
m68k_01d9f2_end:
.org 0x1D9F4
m68k_01d9f4:
        cmpi.w #0x100,%d0
m68k_01d9f4_end:
.org 0x1D9F8
m68k_01d9f8:
        bcc.b (. + -8)
m68k_01d9f8_end:
.org 0x1D9FA
m68k_01d9fa:
        tst.b (%a2, %d0.w)
m68k_01d9fa_end:
.org 0x1D9FE
m68k_01d9fe:
        bne.b (. + -14)
m68k_01d9fe_end:
.org 0x1DA00
m68k_01da00:
        tst.b (%a3, %d0.w)
m68k_01da00_end:
.org 0x1DA04
m68k_01da04:
        bne.b (. + -20)
m68k_01da04_end:
.org 0x1DA06
m68k_01da06:
        move.w %d0,(%a1)+
m68k_01da06_end:
.org 0x1DA08
m68k_01da08:
        bra.b (. + -24)
m68k_01da08_end:
.org 0x1DA0A
m68k_01da0a:
        move.w #0xffff,(%a1)+
m68k_01da0a_end:
.org 0x1DA0E
m68k_01da0e:
        rts
m68k_01da0e_end:
.org 0x1DA10
m68k_01da10:
        tst.w 0xf3a6:w
m68k_01da10_end:
.org 0x1DA14
m68k_01da14:
        bmi.w (. + 38)
m68k_01da14_end:
.org 0x1DA18
m68k_01da18:
        addq.w #0x1,0xf362:w
m68k_01da18_end:
.org 0x1DA1C
m68k_01da1c:
        move.w 0xf3a6:w,0xf3d0:w
m68k_01da1c_end:
.org 0x1DA22
m68k_01da22:
        move.w #0x105,%d0
m68k_01da22_end:
.org 0x1DA26
m68k_01da26:
        move.w %d0,0xaf80:w
m68k_01da26_end:
.org 0x1DA2A
m68k_01da2a:
        jsr 0x676f2:l
m68k_01da2a_end:
.org 0x1DA30
m68k_01da30:
        move.w #0x1,0xf652:w
m68k_01da30_end:
.org 0x1DA36
m68k_01da36:
        bra.w (. + 20)
m68k_01da36_end:
.org 0x1DA3A
m68k_01da3a:
        move.w #0x408,0xf612:w
m68k_01da3a_end:
.org 0x1DA40
m68k_01da40:
        clr.w 0xf362:w
m68k_01da40_end:
.org 0x1DA44
m68k_01da44:
        move.w #0xffff,0xa5f8:w
m68k_01da44_end:
.org 0x1DA4A
m68k_01da4a:
        rts
m68k_01da4a_end:
.org 0x1DA4C
m68k_01da4c:
        move.b 0xf602:w,%d0
m68k_01da4c_end:
.org 0x1DA50
m68k_01da50:
        andi.w #0x2f,%d0
m68k_01da50_end:
.org 0x1DA54
m68k_01da54:
        beq.w (. + 24)
m68k_01da54_end:
.org 0x1DA58
m68k_01da58:
        move.w 0xf612:w,0xf3c2:w
m68k_01da58_end:
.org 0x1DA5E
m68k_01da5e:
        move.w #0x3,0xf3c4:w
m68k_01da5e_end:
.org 0x1DA64
m68k_01da64:
        bsr.w (. + 3712)
m68k_01da64_end:
.org 0x1DA68
m68k_01da68:
        bra.w (. + 18)
m68k_01da68_end:
.org 0x1DA6C
m68k_01da6c:
        btst.b #0x4,0xf603:w
m68k_01da6c_end:
.org 0x1DA72
m68k_01da72:
        beq.w (. + 8)
m68k_01da72_end:
.org 0x1DA76
m68k_01da76:
        clr.w 0xf362:w
m68k_01da76_end:
.org 0x1DA7A
m68k_01da7a:
        rts
m68k_01da7a_end:
.org 0x1DAD0
m68k_01dad0:
        bsr.w (. + 4240)
m68k_01dad0_end:
.org 0x1DAD4
m68k_01dad4:
        bsr.w (. + 4386)
m68k_01dad4_end:
.org 0x1DAD8
m68k_01dad8:
        btst.b #0x5,0xf603:w
m68k_01dad8_end:
.org 0x1DADE
m68k_01dade:
        beq.w (. + 48)
m68k_01dade_end:
.org 0x1DAE2
m68k_01dae2:
        move.w #0xac,%d0
m68k_01dae2_end:
.org 0x1DAE6
m68k_01dae6:
        jsr 0x808a:l
m68k_01dae6_end:
.org 0x1DAEC
m68k_01daec:
        move.w #0xffff,0xa5f8:w
m68k_01daec_end:
.org 0x1DAF2
m68k_01daf2:
        bsr.w (. + 50)
m68k_01daf2_end:
.org 0x1DAF6
m68k_01daf6:
        bsr.w (. + 362)
m68k_01daf6_end:
.org 0x1DAFA
m68k_01dafa:
        move.w #0x408,0xf612:w
m68k_01dafa_end:
.org 0x1DB00
m68k_01db00:
        clr.w 0xf362:w
m68k_01db00_end:
.org 0x1DB04
m68k_01db04:
        move.w #0x1,0xf6f6:w
m68k_01db04_end:
.org 0x1DB0A
m68k_01db0a:
        bra.w (. + 24)
m68k_01db0a_end:
.org 0x1DB0E
m68k_01db0e:
        btst.b #0x4,0xf603:w
m68k_01db0e_end:
.org 0x1DB14
m68k_01db14:
        beq.w (. + 14)
m68k_01db14_end:
.org 0x1DB18
m68k_01db18:
        move.w #0xffff,0xa5f8:w
m68k_01db18_end:
.org 0x1DB1E
m68k_01db1e:
        clr.w 0xf362:w
m68k_01db1e_end:
.org 0x1DB22
m68k_01db22:
        rts
m68k_01db22_end:
.org 0x1DB24
m68k_01db24:
        lea.l 0xff2c00:l,%a5
m68k_01db24_end:
.org 0x1DB2A
m68k_01db2a:
        move.w 0xf3a6:w,%d0
m68k_01db2a_end:
.org 0x1DB2E
m68k_01db2e:
        lsl.w #0x2,%d0
m68k_01db2e_end:
.org 0x1DB30
m68k_01db30:
        move.w 0xf35e:w,%d2
m68k_01db30_end:
.org 0x1DB34
m68k_01db34:
        addi.w #0x8,%d2
m68k_01db34_end:
.org 0x1DB38
m68k_01db38:
        move.w %d2,(%a5, %d0.w)
m68k_01db38_end:
.org 0x1DB3C
m68k_01db3c:
        move.w 0xf360:w,%d2
m68k_01db3c_end:
.org 0x1DB40
m68k_01db40:
        addi.w #0x8,%d2
m68k_01db40_end:
.org 0x1DB44
m68k_01db44:
        move.w %d2,0x2(%a5, %d0.w)
m68k_01db44_end:
.org 0x1DB48
m68k_01db48:
        jsr 0x1a438:l
m68k_01db48_end:
.org 0x1DB4E
m68k_01db4e:
        lea.l 0xa150:w,%a1
m68k_01db4e_end:
.org 0x1DB52
m68k_01db52:
        move.w (%a1, %d0.w),%d1
m68k_01db52_end:
.org 0x1DB56
m68k_01db56:
        lsr.w #0x7,%d1
m68k_01db56_end:
.org 0x1DB58
m68k_01db58:
        move.w 0x2(%a1, %d0.w),%d2
m68k_01db58_end:
.org 0x1DB5C
m68k_01db5c:
        lsr.w #0x7,%d2
m68k_01db5c_end:
.org 0x1DB5E
m68k_01db5e:
        jsr 0x1a44e:l
m68k_01db5e_end:
.org 0x1DB64
m68k_01db64:
        cmpi.b #0x6,%d0
m68k_01db64_end:
.org 0x1DB68
m68k_01db68:
        beq.w (. + 20)
m68k_01db68_end:
.org 0x1DB6C
m68k_01db6c:
        move.w 0xf3a6:w,%d7
m68k_01db6c_end:
.org 0x1DB70
m68k_01db70:
        bsr.w (. + 314)
m68k_01db70_end:
.org 0x1DB74
m68k_01db74:
        andi.w #0xfffe,%sr
m68k_01db74_end:
.org 0x1DB78
m68k_01db78:
        bra.w (. + 56)
m68k_01db78_end:
.org 0x1DB7C
m68k_01db7c:
        move.w 0xf68a:w,%d0
m68k_01db7c_end:
.org 0x1DB80
m68k_01db80:
        lsl.w #0x3,%d0
m68k_01db80_end:
.org 0x1DB82
m68k_01db82:
        lea.l 0xae1b2:l,%a0
m68k_01db82_end:
.org 0x1DB88
m68k_01db88:
        move.w (%a0, %d0.w),%d5
m68k_01db88_end:
.org 0x1DB8C
m68k_01db8c:
        addi.w #0xf80,%d5
m68k_01db8c_end:
.org 0x1DB90
m68k_01db90:
        move.w 0x4(%a0, %d0.w),%d6
m68k_01db90_end:
.org 0x1DB94
m68k_01db94:
        addi.w #0xf80,%d6
m68k_01db94_end:
.org 0x1DB98
m68k_01db98:
        movem.l %d5-%d6,-(%a7)
m68k_01db98_end:
.org 0x1DB9C
m68k_01db9c:
        move.w 0xf3a6:w,%d1
m68k_01db9c_end:
.org 0x1DBA0
m68k_01dba0:
        move.w %d1,%d7
m68k_01dba0_end:
.org 0x1DBA2
m68k_01dba2:
        lsl.w #0x2,%d1
m68k_01dba2_end:
.org 0x1DBA4
m68k_01dba4:
        bsr.w (. + 278)
m68k_01dba4_end:
.org 0x1DBA8
m68k_01dba8:
        movem.l (%a7)+,%d5-%d6
m68k_01dba8_end:
.org 0x1DBAC
m68k_01dbac:
        bsr.w (. + 6)
m68k_01dbac_end:
.org 0x1DBB0
m68k_01dbb0:
        rts
m68k_01dbb0_end:
.org 0x1DBB2
m68k_01dbb2:
        tst.w %d3
m68k_01dbb2_end:
.org 0x1DBB4
m68k_01dbb4:
        bmi.b (. + 34)
m68k_01dbb4_end:
.org 0x1DBB6
m68k_01dbb6:
        tst.w %d4
m68k_01dbb6_end:
.org 0x1DBB8
m68k_01dbb8:
        bmi.b (. + 14)
m68k_01dbb8_end:
.org 0x1DBBA
m68k_01dbba:
        move.w #0x1,%d0
m68k_01dbba_end:
.org 0x1DBBE
m68k_01dbbe:
        cmp.w %d4,%d3
m68k_01dbbe_end:
.org 0x1DBC0
m68k_01dbc0:
        bcs.b (. + 48)
m68k_01dbc0_end:
.org 0x1DBC2
m68k_01dbc2:
        addq.w #0x1,%d0
m68k_01dbc2_end:
.org 0x1DBC4
m68k_01dbc4:
        bra.b (. + 44)
m68k_01dbc4_end:
.org 0x1DBC6
m68k_01dbc6:
        move.w #0x2,%d0
m68k_01dbc6_end:
.org 0x1DBCA
m68k_01dbca:
        neg.w %d4
m68k_01dbca_end:
.org 0x1DBCC
m68k_01dbcc:
        cmp.w %d4,%d3
m68k_01dbcc_end:
.org 0x1DBCE
m68k_01dbce:
        bcc.b (. + 34)
m68k_01dbce_end:
.org 0x1DBD0
m68k_01dbd0:
        addq.w #0x1,%d0
m68k_01dbd0_end:
.org 0x1DBD2
m68k_01dbd2:
        bra.w (. + 30)
m68k_01dbd2_end:
.org 0x1DBD6
m68k_01dbd6:
        tst.w %d4
m68k_01dbd6_end:
.org 0x1DBD8
m68k_01dbd8:
        bmi.b (. + 14)
m68k_01dbd8_end:
.org 0x1DBDA
m68k_01dbda:
        clr.w %d0
m68k_01dbda_end:
.org 0x1DBDC
m68k_01dbdc:
        neg.w %d3
m68k_01dbdc_end:
.org 0x1DBDE
m68k_01dbde:
        cmp.w %d4,%d3
m68k_01dbde_end:
.org 0x1DBE0
m68k_01dbe0:
        bcc.b (. + 16)
m68k_01dbe0_end:
.org 0x1DBE2
m68k_01dbe2:
        addq.w #0x1,%d0
m68k_01dbe2_end:
.org 0x1DBE4
m68k_01dbe4:
        bra.b (. + 12)
m68k_01dbe4_end:
.org 0x1DBE6
m68k_01dbe6:
        clr.w %d0
m68k_01dbe6_end:
.org 0x1DBE8
m68k_01dbe8:
        cmp.w %d4,%d3
m68k_01dbe8_end:
.org 0x1DBEA
m68k_01dbea:
        bls.b (. + 6)
m68k_01dbea_end:
.org 0x1DBEC
m68k_01dbec:
        move.w #0x3,%d0
m68k_01dbec_end:
.org 0x1DBF0
m68k_01dbf0:
        lsl.w #0x2,%d0
m68k_01dbf0_end:
.org 0x1DBF2
m68k_01dbf2:
        lea.l 12(%pc),%a0
m68k_01dbf2_end:
.org 0x1DBF6
m68k_01dbf6:
        add.w (%a0, %d0.w),%d5
m68k_01dbf6_end:
.org 0x1DBFA
m68k_01dbfa:
        add.w 0x2(%a0, %d0.w),%d6
m68k_01dbfa_end:
.org 0x1DBFE
m68k_01dbfe:
        rts
m68k_01dbfe_end:
.org 0x1DC60
m68k_01dc60:
        move.w 0xf3a6:w,%d0
m68k_01dc60_end:
.org 0x1DC64
m68k_01dc64:
        move.w 0xf6d6:w,%d1
m68k_01dc64_end:
.org 0x1DC68
m68k_01dc68:
        andi.w #0x2,%d1
m68k_01dc68_end:
.org 0x1DC6C
m68k_01dc6c:
        lsl.w #0x1,%d1
m68k_01dc6c_end:
.org 0x1DC6E
m68k_01dc6e:
        movea.l -24(%pc, %d1.w),%a6
m68k_01dc6e_end:
.org 0x1DC72
m68k_01dc72:
        lea.l 0xae28:w,%a4
m68k_01dc72_end:
.org 0x1DC76
m68k_01dc76:
        move.w (%a6)+,%d1
m68k_01dc76_end:
.org 0x1DC78
m68k_01dc78:
        cmp.w %d0,%d1
m68k_01dc78_end:
.org 0x1DC7A
m68k_01dc7a:
        bne.b (. + -4)
m68k_01dc7a_end:
.org 0x1DC7C
m68k_01dc7c:
        ori.w #0x4000,-0x2(%a6)
m68k_01dc7c_end:
.org 0x1DC82
m68k_01dc82:
        move.b #0x1,(%a4, %d1.w)
m68k_01dc82_end:
.org 0x1DC88
m68k_01dc88:
        lea.l 0xff3bc2:l,%a0
m68k_01dc88_end:
.org 0x1DC8E
m68k_01dc8e:
        clr.b (%a0, %d0.w)
m68k_01dc8e_end:
.org 0x1DC92
m68k_01dc92:
        rts
m68k_01dc92_end:
.org 0x1DC94
m68k_01dc94:
        btst.b #0x5,0xf603:w
m68k_01dc94_end:
.org 0x1DC9A
m68k_01dc9a:
        beq.w (. + 14)
m68k_01dc9a_end:
.org 0x1DC9E
m68k_01dc9e:
        move.w #0x408,0xf612:w
m68k_01dc9e_end:
.org 0x1DCA4
m68k_01dca4:
        clr.w 0xf362:w
m68k_01dca4_end:
.org 0x1DCA8
m68k_01dca8:
        rts
m68k_01dca8_end:
.org 0x1E4F8
m68k_01e4f8:
        move.w 0xf6d6:w,%d0
m68k_01e4f8_end:
.org 0x1E4FC
m68k_01e4fc:
        andi.w #0x2,%d0
m68k_01e4fc_end:
.org 0x1E500
m68k_01e500:
        lsl.w #0x1,%d0
m68k_01e500_end:
.org 0x1E502
m68k_01e502:
        movea.l 98(%pc, %d0.w),%a0
m68k_01e502_end:
.org 0x1E506
m68k_01e506:
        lea.l 0xa5f8:w,%a1
m68k_01e506_end:
.org 0x1E50A
m68k_01e50a:
        lea.l 0xa654:w,%a2
m68k_01e50a_end:
.org 0x1E50E
m68k_01e50e:
        lea.l 0xff3cc2:l,%a3
m68k_01e50e_end:
.org 0x1E514
m68k_01e514:
        move.w (%a0)+,%d0
m68k_01e514_end:
.org 0x1E516
m68k_01e516:
        bmi.b (. + 24)
m68k_01e516_end:
.org 0x1E518
m68k_01e518:
        cmpi.w #0x100,%d0
m68k_01e518_end:
.org 0x1E51C
m68k_01e51c:
        bcc.b (. + -8)
m68k_01e51c_end:
.org 0x1E51E
m68k_01e51e:
        tst.b (%a2, %d0.w)
m68k_01e51e_end:
.org 0x1E522
m68k_01e522:
        bmi.b (. + -14)
m68k_01e522_end:
.org 0x1E524
m68k_01e524:
        tst.b (%a3, %d0.w)
m68k_01e524_end:
.org 0x1E528
m68k_01e528:
        bne.b (. + -20)
m68k_01e528_end:
.org 0x1E52A
m68k_01e52a:
        move.w %d0,(%a1)+
m68k_01e52a_end:
.org 0x1E52C
m68k_01e52c:
        bra.b (. + -24)
m68k_01e52c_end:
.org 0x1E52E
m68k_01e52e:
        move.w #0xffff,(%a1)
m68k_01e52e_end:
.org 0x1E532
m68k_01e532:
        move.w #0x40a,0xf612:w
m68k_01e532_end:
.org 0x1E538
m68k_01e538:
        move.w #0x1,0xf362:w
m68k_01e538_end:
.org 0x1E53E
m68k_01e53e:
        move.w #0x40c,0xf38a:w
m68k_01e53e_end:
.org 0x1E544
m68k_01e544:
        move.w #0x1,0xf3b0:w
m68k_01e544_end:
.org 0x1E54A
m68k_01e54a:
        move.w #0x104,%d0
m68k_01e54a_end:
.org 0x1E54E
m68k_01e54e:
        move.w %d0,0xaf80:w
m68k_01e54e_end:
.org 0x1E552
m68k_01e552:
        jsr 0x676f2:l
m68k_01e552_end:
.org 0x1E558
m68k_01e558:
        move.w #0x68,0xf35e:w
m68k_01e558_end:
.org 0x1E55E
m68k_01e55e:
        move.w #0x98,0xf360:w
m68k_01e55e_end:
.org 0x1E564
m68k_01e564:
        rts
m68k_01e564_end:
.org 0x1E56E
m68k_01e56e:
        tst.w 0xf3a6:w
m68k_01e56e_end:
.org 0x1E572
m68k_01e572:
        bmi.w (. + 38)
m68k_01e572_end:
.org 0x1E576
m68k_01e576:
        addq.w #0x1,0xf362:w
m68k_01e576_end:
.org 0x1E57A
m68k_01e57a:
        move.w 0xf3a6:w,0xf3d0:w
m68k_01e57a_end:
.org 0x1E580
m68k_01e580:
        move.w #0x111,%d0
m68k_01e580_end:
.org 0x1E584
m68k_01e584:
        move.w %d0,0xaf80:w
m68k_01e584_end:
.org 0x1E588
m68k_01e588:
        jsr 0x676f2:l
m68k_01e588_end:
.org 0x1E58E
m68k_01e58e:
        move.w #0x1,0xf652:w
m68k_01e58e_end:
.org 0x1E594
m68k_01e594:
        bra.w (. + 14)
m68k_01e594_end:
.org 0x1E598
m68k_01e598:
        move.w #0x408,0xf612:w
m68k_01e598_end:
.org 0x1E59E
m68k_01e59e:
        clr.w 0xf362:w
m68k_01e59e_end:
.org 0x1E5A2
m68k_01e5a2:
        rts
m68k_01e5a2_end:
.org 0x1E5A4
m68k_01e5a4:
        btst.b #0x5,0xf603:w
m68k_01e5a4_end:
.org 0x1E5AA
m68k_01e5aa:
        beq.w (. + 38)
m68k_01e5aa_end:
.org 0x1E5AE
m68k_01e5ae:
        bsr.w (. + 36)
m68k_01e5ae_end:
.org 0x1E5B2
m68k_01e5b2:
        bsr.w (. + 76)
m68k_01e5b2_end:
.org 0x1E5B6
m68k_01e5b6:
        bsr.w (. + 86)
m68k_01e5b6_end:
.org 0x1E5BA
m68k_01e5ba:
        move.w #0x408,0xf612:w
m68k_01e5ba_end:
.org 0x1E5C0
m68k_01e5c0:
        clr.w 0xf362:w
m68k_01e5c0_end:
.org 0x1E5C4
m68k_01e5c4:
        move.w #0x1,0xf6f6:w
m68k_01e5c4_end:
.org 0x1E5CA
m68k_01e5ca:
        move.w #0xffff,0xa5f8:w
m68k_01e5ca_end:
.org 0x1E5D0
m68k_01e5d0:
        rts
m68k_01e5d0_end:
.org 0x1E5FE
m68k_01e5fe:
        move.w 0xf3a6:w,%d0
m68k_01e5fe_end:
.org 0x1E602
m68k_01e602:
        lea.l 0xae28:w,%a0
m68k_01e602_end:
.org 0x1E606
m68k_01e606:
        clr.b (%a0, %d0.w)
m68k_01e606_end:
.org 0x1E60A
m68k_01e60a:
        rts
m68k_01e60a_end:
.org 0x1E60C
m68k_01e60c:
        jsr 0x1a438:l
m68k_01e60c_end:
.org 0x1E612
m68k_01e612:
        move.w 0xf3a6:w,%d0
m68k_01e612_end:
.org 0x1E616
m68k_01e616:
        lsl.w #0x2,%d0
m68k_01e616_end:
.org 0x1E618
m68k_01e618:
        lea.l 0xc800:w,%a1
m68k_01e618_end:
.org 0x1E61C
m68k_01e61c:
        cmpi.l #0x1388,(%a1, %d0.w)
m68k_01e61c_end:
.org 0x1E624
m68k_01e624:
        bhi.w (. + 58)
m68k_01e624_end:
.org 0x1E628
m68k_01e628:
        lea.l 0xa150:w,%a1
m68k_01e628_end:
.org 0x1E62C
m68k_01e62c:
        move.w (%a1, %d0.w),%d1
m68k_01e62c_end:
.org 0x1E630
m68k_01e630:
        lsr.w #0x7,%d1
m68k_01e630_end:
.org 0x1E632
m68k_01e632:
        move.w 0x2(%a1, %d0.w),%d2
m68k_01e632_end:
.org 0x1E636
m68k_01e636:
        lsr.w #0x7,%d2
m68k_01e636_end:
.org 0x1E638
m68k_01e638:
        jsr 0x1a44e:l
m68k_01e638_end:
.org 0x1E63E
m68k_01e63e:
        cmpi.b #0x3,%d0
m68k_01e63e_end:
.org 0x1E642
m68k_01e642:
        beq.w (. + 12)
m68k_01e642_end:
.org 0x1E646
m68k_01e646:
        cmpi.b #0x8,%d0
m68k_01e646_end:
.org 0x1E64A
m68k_01e64a:
        bne.w (. + 20)
m68k_01e64a_end:
.org 0x1E64E
m68k_01e64e:
        move.w 0xf3a6:w,%d0
m68k_01e64e_end:
.org 0x1E652
m68k_01e652:
        lea.l 0xff3bc2:l,%a0
m68k_01e652_end:
.org 0x1E658
m68k_01e658:
        move.b #0x1,(%a0, %d0.w)
m68k_01e658_end:
.org 0x1E65E
m68k_01e65e:
        rts
m68k_01e65e_end:
.org 0x1E690
m68k_01e690:
        move.w #0xffff,0xa57a:w
m68k_01e690_end:
.org 0x1E696
m68k_01e696:
        move.w #0xffff,0xa5ce:w
m68k_01e696_end:
.org 0x1E69C
m68k_01e69c:
        move.w 0xf612:w,0xf38a:w
m68k_01e69c_end:
.org 0x1E6A2
m68k_01e6a2:
        move.w #0x1,0xf3b0:w
m68k_01e6a2_end:
.org 0x1E6A8
m68k_01e6a8:
        btst.b #0x1,0xf6d7:w
m68k_01e6a8_end:
.org 0x1E6AE
m68k_01e6ae:
        beq.w (. + 10)
m68k_01e6ae_end:
.org 0x1E6B2
m68k_01e6b2:
        move.w #0xa,0xf3b0:w
m68k_01e6b2_end:
.org 0x1E6B8
m68k_01e6b8:
        move.w #0x402,0xf612:w
m68k_01e6b8_end:
.org 0x1E6BE
m68k_01e6be:
        clr.w 0xf362:w
m68k_01e6be_end:
.org 0x1E6C2
m68k_01e6c2:
        move.w #0x88,0xf600:w
m68k_01e6c2_end:
.org 0x1E6C8
m68k_01e6c8:
        bsr.w (. + 14)
m68k_01e6c8_end:
.org 0x1E6CC
m68k_01e6cc:
        bsr.w (. + 398)
m68k_01e6cc_end:
.org 0x1E6D0
m68k_01e6d0:
        bsr.w (. + 90)
m68k_01e6d0_end:
.org 0x1E6D4
m68k_01e6d4:
        rts
m68k_01e6d4_end:
.org 0x1E6D6
m68k_01e6d6:
        movem.l %d1/%a1,-(%a7)
m68k_01e6d6_end:
.org 0x1E6DA
m68k_01e6da:
        move.w 0xf68a:w,%d0
m68k_01e6da_end:
.org 0x1E6DE
m68k_01e6de:
        lsl.w #0x1,%d0
m68k_01e6de_end:
.org 0x1E6E0
m68k_01e6e0:
        add.w 0xf68a:w,%d0
m68k_01e6e0_end:
.org 0x1E6E4
m68k_01e6e4:
        lsl.w #0x2,%d0
m68k_01e6e4_end:
.org 0x1E6E6
m68k_01e6e6:
        lea.l 0xe80c:w,%a0
m68k_01e6e6_end:
.org 0x1E6EA
m68k_01e6ea:
        lea.l 0xcd00:w,%a1
m68k_01e6ea_end:
.org 0x1E6EE
m68k_01e6ee:
        move.w (%a0, %d0.w),%d1
m68k_01e6ee_end:
.org 0x1E6F2
m68k_01e6f2:
        bmi.w (. + 14)
m68k_01e6f2_end:
.org 0x1E6F6
m68k_01e6f6:
        clr.b (%a1, %d1.w)
m68k_01e6f6_end:
.org 0x1E6FA
m68k_01e6fa:
        move.w #0xffff,(%a0, %d0.w)
m68k_01e6fa_end:
.org 0x1E700
m68k_01e700:
        move.w 0x4(%a0, %d0.w),%d1
m68k_01e700_end:
.org 0x1E704
m68k_01e704:
        bmi.w (. + 14)
m68k_01e704_end:
.org 0x1E708
m68k_01e708:
        clr.b (%a1, %d1.w)
m68k_01e708_end:
.org 0x1E70C
m68k_01e70c:
        move.w #0xffff,0x4(%a0, %d0.w)
m68k_01e70c_end:
.org 0x1E712
m68k_01e712:
        move.w 0x8(%a0, %d0.w),%d1
m68k_01e712_end:
.org 0x1E716
m68k_01e716:
        bmi.w (. + 14)
m68k_01e716_end:
.org 0x1E71A
m68k_01e71a:
        clr.b (%a1, %d1.w)
m68k_01e71a_end:
.org 0x1E71E
m68k_01e71e:
        move.w #0xffff,0x8(%a0, %d0.w)
m68k_01e71e_end:
.org 0x1E724
m68k_01e724:
        movem.l (%a7)+,%d1/%a1
m68k_01e724_end:
.org 0x1E728
m68k_01e728:
        rts
m68k_01e728_end:
.org 0x1E72A
m68k_01e72a:
        lea.l 0xe710:w,%a0
m68k_01e72a_end:
.org 0x1E72E
m68k_01e72e:
        move.w 0xf68c:w,%d0
m68k_01e72e_end:
.org 0x1E732
m68k_01e732:
        lsl.w #0x1,%d0
m68k_01e732_end:
.org 0x1E734
m68k_01e734:
        move.w 0xf68e:w,%d1
m68k_01e734_end:
.org 0x1E738
m68k_01e738:
        move.w (%a0, %d0.w),%d2
m68k_01e738_end:
.org 0x1E73C
m68k_01e73c:
        btst.l %d1,%d2
m68k_01e73c_end:
.org 0x1E73E
m68k_01e73e:
        beq.w (. + 100)
m68k_01e73e_end:
.org 0x1E742
m68k_01e742:
        bclr.l %d1,%d2
m68k_01e742_end:
.org 0x1E744
m68k_01e744:
        move.w %d2,(%a0, %d0.w)
m68k_01e744_end:
.org 0x1E748
m68k_01e748:
        bsr.w (. + 92)
m68k_01e748_end:
.org 0x1E74C
m68k_01e74c:
        lsr.w #0x1,%d0
m68k_01e74c_end:
.org 0x1E74E
m68k_01e74e:
        lsl.w #0x1,%d1
m68k_01e74e_end:
.org 0x1E750
m68k_01e750:
        move.w (%a0, %d1.w),%d2
m68k_01e750_end:
.org 0x1E754
m68k_01e754:
        bclr.l %d0,%d2
m68k_01e754_end:
.org 0x1E756
m68k_01e756:
        move.w %d2,(%a0, %d1.w)
m68k_01e756_end:
.org 0x1E75A
m68k_01e75a:
        lsr.w #0x1,%d1
m68k_01e75a_end:
.org 0x1E75C
m68k_01e75c:
        lea.l 0xe9f8:w,%a0
m68k_01e75c_end:
.org 0x1E760
m68k_01e760:
        lea.l 0xf427:w,%a1
m68k_01e760_end:
.org 0x1E764
m68k_01e764:
        lea.l 0xe65c:w,%a2
m68k_01e764_end:
.org 0x1E768
m68k_01e768:
        bsr.w (. + 6)
m68k_01e768_end:
.org 0x1E76C
m68k_01e76c:
        exg %d0,%d1
m68k_01e76c_end:
.org 0x1E76E
m68k_01e76e:
        move.w %d0,%d2
m68k_01e76e_end:
.org 0x1E770
m68k_01e770:
        move.w %d1,%d3
m68k_01e770_end:
.org 0x1E772
m68k_01e772:
        lsl.w #0x2,%d2
m68k_01e772_end:
.org 0x1E774
m68k_01e774:
        clr.w %d4
m68k_01e774_end:
.org 0x1E776
m68k_01e776:
        move.b (%a0, %d2.w),%d4
m68k_01e776_end:
.org 0x1E77A
m68k_01e77a:
        beq.w (. + 40)
m68k_01e77a_end:
.org 0x1E77E
m68k_01e77e:
        cmp.b (%a1, %d4.w),%d3
m68k_01e77e_end:
.org 0x1E782
m68k_01e782:
        bne.w (. + 32)
m68k_01e782_end:
.org 0x1E786
m68k_01e786:
        clr.w %d4
m68k_01e786_end:
.org 0x1E788
m68k_01e788:
        move.b 0x1(%a0, %d2.w),%d4
m68k_01e788_end:
.org 0x1E78C
m68k_01e78c:
        lsl.w #0x2,%d4
m68k_01e78c_end:
.org 0x1E78E
m68k_01e78e:
        clr.l (%a2, %d4.w)
m68k_01e78e_end:
.org 0x1E792
m68k_01e792:
        clr.l (%a0, %d2.w)
m68k_01e792_end:
.org 0x1E796
m68k_01e796:
        move.w 0xe700:w,%d4
m68k_01e796_end:
.org 0x1E79A
m68k_01e79a:
        lsr.w #0x2,%d2
m68k_01e79a_end:
.org 0x1E79C
m68k_01e79c:
        bclr.l %d2,%d4
m68k_01e79c_end:
.org 0x1E79E
m68k_01e79e:
        move.w %d4,0xe700:w
m68k_01e79e_end:
.org 0x1E7A2
m68k_01e7a2:
        rts
m68k_01e7a2_end:
.org 0x1E7A4
m68k_01e7a4:
        movem.l %d0-%d1/%a0,-(%a7)
m68k_01e7a4_end:
.org 0x1E7A8
m68k_01e7a8:
        jsr 0x83d4:l
m68k_01e7a8_end:
.org 0x1E7AE
m68k_01e7ae:
        andi.l #0xffff,%d0
m68k_01e7ae_end:
.org 0x1E7B4
m68k_01e7b4:
        move.l %d0,%d1
m68k_01e7b4_end:
.org 0x1E7B6
m68k_01e7b6:
        lsl.l #0x1,%d0
m68k_01e7b6_end:
.org 0x1E7B8
m68k_01e7b8:
        add.l %d1,%d0
m68k_01e7b8_end:
.org 0x1E7BA
m68k_01e7ba:
        lsl.l #0x1,%d0
m68k_01e7ba_end:
.org 0x1E7BC
m68k_01e7bc:
        swap %d0
m68k_01e7bc_end:
.org 0x1E7BE
m68k_01e7be:
        addq.w #0x5,%d0
m68k_01e7be_end:
.org 0x1E7C0
m68k_01e7c0:
        lea.l 0xe640:w,%a0
m68k_01e7c0_end:
.org 0x1E7C4
m68k_01e7c4:
        move.w 0xf68c:w,%d1
m68k_01e7c4_end:
.org 0x1E7C8
m68k_01e7c8:
        lsl.w #0x1,%d1
m68k_01e7c8_end:
.org 0x1E7CA
m68k_01e7ca:
        move.w (%a0, %d1.w),%d1
m68k_01e7ca_end:
.org 0x1E7CE
m68k_01e7ce:
        lea.l 0xc200:w,%a0
m68k_01e7ce_end:
.org 0x1E7D2
m68k_01e7d2:
        sub.b %d0,(%a0, %d1.w)
m68k_01e7d2_end:
.org 0x1E7D6
m68k_01e7d6:
        bcc.w (. + 8)
m68k_01e7d6_end:
.org 0x1E7DA
m68k_01e7da:
        clr.b (%a0, %d1.w)
m68k_01e7da_end:
.org 0x1E7DE
m68k_01e7de:
        movem.l (%a7)+,%d0-%d1/%a0
m68k_01e7de_end:
.org 0x1E7E2
m68k_01e7e2:
        rts
m68k_01e7e2_end:
.org 0x1E7E4
m68k_01e7e4:
        lea.l 0x9fff:w,%a0
m68k_01e7e4_end:
.org 0x1E7E8
m68k_01e7e8:
        move.w 0xf68a:w,%d0
m68k_01e7e8_end:
.org 0x1E7EC
m68k_01e7ec:
        tst.b (%a0, %d0.w)
m68k_01e7ec_end:
.org 0x1E7F0
m68k_01e7f0:
        bne.w (. + 92)
m68k_01e7f0_end:
.org 0x1E7F4
m68k_01e7f4:
        lea.l 0xefaa:w,%a0
m68k_01e7f4_end:
.org 0x1E7F8
m68k_01e7f8:
        subq.w #0x1,%d0
m68k_01e7f8_end:
.org 0x1E7FA
m68k_01e7fa:
        move.w %d0,%d1
m68k_01e7fa_end:
.org 0x1E7FC
m68k_01e7fc:
        lsr.w #0x3,%d0
m68k_01e7fc_end:
.org 0x1E7FE
m68k_01e7fe:
        btst.l %d1,(%a0, %d0.w)
m68k_01e7fe_end:
.org 0x1E802
m68k_01e802:
        bne.w (. + 74)
m68k_01e802_end:
.org 0x1E806
m68k_01e806:
        move.w 0xf68c:w,%d0
m68k_01e806_end:
.org 0x1E80A
m68k_01e80a:
        cmp.w 0xf67a:w,%d0
m68k_01e80a_end:
.org 0x1E80E
m68k_01e80e:
        beq.w (. + 36)
m68k_01e80e_end:
.org 0x1E812
m68k_01e812:
        cmp.w 0xf67c:w,%d0
m68k_01e812_end:
.org 0x1E816
m68k_01e816:
        beq.w (. + 28)
m68k_01e816_end:
.org 0x1E81A
m68k_01e81a:
        cmp.w 0xf67e:w,%d0
m68k_01e81a_end:
.org 0x1E81E
m68k_01e81e:
        beq.w (. + 20)
m68k_01e81e_end:
.org 0x1E822
m68k_01e822:
        move.w #0xf,0xf362:w
m68k_01e822_end:
.org 0x1E828
m68k_01e828:
        move.w #0xb8,0xf600:w
m68k_01e828_end:
.org 0x1E82E
m68k_01e82e:
        bra.w (. + 42)
m68k_01e82e_end:
.org 0x1E832
m68k_01e832:
        addq.w #0x1,0xf362:w
m68k_01e832_end:
.org 0x1E836
m68k_01e836:
        move.w #0x100,%d0
m68k_01e836_end:
.org 0x1E83A
m68k_01e83a:
        move.w %d0,0xaf80:w
m68k_01e83a_end:
.org 0x1E83E
m68k_01e83e:
        jsr 0x676f2:l
m68k_01e83e_end:
.org 0x1E844
m68k_01e844:
        clr.w 0xf6c6:w
m68k_01e844_end:
.org 0x1E848
m68k_01e848:
        bra.w (. + 16)
m68k_01e848_end:
.org 0x1E84C
m68k_01e84c:
        move.w #0xd8,0xf600:w
m68k_01e84c_end:
.org 0x1E852
m68k_01e852:
        move.w #0xf,0xf362:w
m68k_01e852_end:
.org 0x1E858
m68k_01e858:
        rts
m68k_01e858_end:
.org 0x1E85A
m68k_01e85a:
        lea.l 0xa654:w,%a0
m68k_01e85a_end:
.org 0x1E85E
m68k_01e85e:
        lea.l 0xa754:w,%a1
m68k_01e85e_end:
.org 0x1E862
m68k_01e862:
        lea.l 0xae28:w,%a2
m68k_01e862_end:
.org 0x1E866
m68k_01e866:
        lea.l 0xceae:w,%a3
m68k_01e866_end:
.org 0x1E86A
m68k_01e86a:
        move.w #0x3f,%d0
m68k_01e86a_end:
.org 0x1E86E
m68k_01e86e:
        clr.l (%a0)+
m68k_01e86e_end:
.org 0x1E870
m68k_01e870:
        clr.l (%a1)+
m68k_01e870_end:
.org 0x1E872
m68k_01e872:
        clr.l (%a2)+
m68k_01e872_end:
.org 0x1E874
m68k_01e874:
        clr.l (%a3)+
m68k_01e874_end:
.org 0x1E876
m68k_01e876:
        dbra %d0,(. + -8)
m68k_01e876_end:
.org 0x1E87A
m68k_01e87a:
        move.w #0xffff,0xf6e8:w
m68k_01e87a_end:
.org 0x1E880
m68k_01e880:
        move.w #0xffff,0xf6ea:w
m68k_01e880_end:
.org 0x1E886
m68k_01e886:
        move.w #0xffff,0xf6ec:w
m68k_01e886_end:
.org 0x1E88C
m68k_01e88c:
        move.w #0xffff,0xf6ee:w
m68k_01e88c_end:
.org 0x1E892
m68k_01e892:
        clr.w 0xf6c8:w
m68k_01e892_end:
.org 0x1E896
m68k_01e896:
        clr.w 0xf6f8:w
m68k_01e896_end:
.org 0x1E89A
m68k_01e89a:
        rts
m68k_01e89a_end:
.org 0x1E89C
m68k_01e89c:
        btst.b #0x5,0xf603:w
m68k_01e89c_end:
.org 0x1E8A2
m68k_01e8a2:
        beq.b (. + 34)
m68k_01e8a2_end:
.org 0x1E8A4
m68k_01e8a4:
        move.w 0xf612:w,0xf3c2:w
m68k_01e8a4_end:
.org 0x1E8AA
m68k_01e8aa:
        move.w #0x3,0xf3c4:w
m68k_01e8aa_end:
.org 0x1E8B0
m68k_01e8b0:
        bsr.w (. + 22)
m68k_01e8b0_end:
.org 0x1E8B4
m68k_01e8b4:
        move.w #0x68,0xf35e:w
m68k_01e8b4_end:
.org 0x1E8BA
m68k_01e8ba:
        move.w #0x98,0xf360:w
m68k_01e8ba_end:
.org 0x1E8C0
m68k_01e8c0:
        bsr.w (. + 36)
m68k_01e8c0_end:
.org 0x1E8C4
m68k_01e8c4:
        rts
m68k_01e8c4_end:
.org 0x1E8C6
m68k_01e8c6:
        move.w 0xf68a:w,%d0
m68k_01e8c6_end:
.org 0x1E8CA
m68k_01e8ca:
        lsl.w #0x5,%d0
m68k_01e8ca_end:
.org 0x1E8CC
m68k_01e8cc:
        lea.l 0xabdaa:l,%a0
m68k_01e8cc_end:
.org 0x1E8D2
m68k_01e8d2:
        adda.w %d0,%a0
m68k_01e8d2_end:
.org 0x1E8D4
m68k_01e8d4:
        lea.l 0xafaa:w,%a1
m68k_01e8d4_end:
.org 0x1E8D8
m68k_01e8d8:
        move.w #0xf,%d1
m68k_01e8d8_end:
.org 0x1E8DC
m68k_01e8dc:
        move.w (%a0)+,(%a1)+
m68k_01e8dc_end:
.org 0x1E8DE
m68k_01e8de:
        dbra %d1,(. + -2)
m68k_01e8de_end:
.org 0x1E8E2
m68k_01e8e2:
        rts
m68k_01e8e2_end:
.org 0x1E8E4
m68k_01e8e4:
        move.w #0x404,0xf612:w
m68k_01e8e4_end:
.org 0x1E8EA
m68k_01e8ea:
        clr.w 0xf36a:w
m68k_01e8ea_end:
.org 0x1E8EE
m68k_01e8ee:
        rts
m68k_01e8ee_end:
.org 0x1E8F0
m68k_01e8f0:
        bsr.w (. + 624)
m68k_01e8f0_end:
.org 0x1E8F4
m68k_01e8f4:
        bsr.w (. + 770)
m68k_01e8f4_end:
.org 0x1E8F8
m68k_01e8f8:
        jsr 0x1a3f4:l
m68k_01e8f8_end:
.org 0x1E8FE
m68k_01e8fe:
        btst.b #0x5,0xf603:w
m68k_01e8fe_end:
.org 0x1E904
m68k_01e904:
        beq.w (. + 152)
m68k_01e904_end:
.org 0x1E908
m68k_01e908:
        bsr.w (. + 150)
m68k_01e908_end:
.org 0x1E90C
m68k_01e90c:
        bcs.w (. + 144)
m68k_01e90c_end:
.org 0x1E910
m68k_01e910:
        move.w #0xac,%d0
m68k_01e910_end:
.org 0x1E914
m68k_01e914:
        jsr 0x808a:l
m68k_01e914_end:
.org 0x1E91A
m68k_01e91a:
        lea.l 0xe640:w,%a0
m68k_01e91a_end:
.org 0x1E91E
m68k_01e91e:
        move.w 0xf68c:w,%d0
m68k_01e91e_end:
.org 0x1E922
m68k_01e922:
        lsl.w #0x1,%d0
m68k_01e922_end:
.org 0x1E924
m68k_01e924:
        move.w (%a0, %d0.w),%d0
m68k_01e924_end:
.org 0x1E928
m68k_01e928:
        cmp.w 0xa550:w,%d0
m68k_01e928_end:
.org 0x1E92C
m68k_01e92c:
        bne.w (. + 24)
m68k_01e92c_end:
.org 0x1E930
m68k_01e930:
        clr.w 0xf378:w
m68k_01e930_end:
.org 0x1E934
m68k_01e934:
        clr.w 0xf658:w
m68k_01e934_end:
.org 0x1E938
m68k_01e938:
        addq.w #0x1,0xf362:w
m68k_01e938_end:
.org 0x1E93C
m68k_01e93c:
        move.w %d0,0xf500:w
m68k_01e93c_end:
.org 0x1E940
m68k_01e940:
        bra.w (. + 92)
m68k_01e940_end:
.org 0x1E944
m68k_01e944:
        clr.w 0xf378:w
m68k_01e944_end:
.org 0x1E948
m68k_01e948:
        clr.w 0xf658:w
m68k_01e948_end:
.org 0x1E94C
m68k_01e94c:
        move.w 0xf612:w,0xf38a:w
m68k_01e94c_end:
.org 0x1E952
m68k_01e952:
        move.w #0x4,0xf3b0:w
m68k_01e952_end:
.org 0x1E958
m68k_01e958:
        move.w #0x405,0xf612:w
m68k_01e958_end:
.org 0x1E95E
m68k_01e95e:
        clr.w 0xf362:w
m68k_01e95e_end:
.org 0x1E962
m68k_01e962:
        lea.l 0xa550:w,%a0
m68k_01e962_end:
.org 0x1E966
m68k_01e966:
        lea.l 0xf500:w,%a1
m68k_01e966_end:
.org 0x1E96A
m68k_01e96a:
        clr.w %d0
m68k_01e96a_end:
.org 0x1E96C
m68k_01e96c:
        move.w (%a0)+,(%a1)+
m68k_01e96c_end:
.org 0x1E96E
m68k_01e96e:
        bmi.b (. + 6)
m68k_01e96e_end:
.org 0x1E970
m68k_01e970:
        addq.w #0x1,%d0
m68k_01e970_end:
.org 0x1E972
m68k_01e972:
        bra.b (. + -6)
m68k_01e972_end:
.org 0x1E974
m68k_01e974:
        move.w %d0,0xf636:w
m68k_01e974_end:
.org 0x1E978
m68k_01e978:
        clr.w 0xf36a:w
m68k_01e978_end:
.org 0x1E97C
m68k_01e97c:
        clr.w 0xf362:w
m68k_01e97c_end:
.org 0x1E980
m68k_01e980:
        clr.w 0xf656:w
m68k_01e980_end:
.org 0x1E984
m68k_01e984:
        clr.w 0xf378:w
m68k_01e984_end:
.org 0x1E988
m68k_01e988:
        move.w #0x101,%d0
m68k_01e988_end:
.org 0x1E98C
m68k_01e98c:
        move.w %d0,0xaf80:w
m68k_01e98c_end:
.org 0x1E990
m68k_01e990:
        jsr 0x676f2:l
m68k_01e990_end:
.org 0x1E996
m68k_01e996:
        move.w #0x1,0xf6d2:w
m68k_01e996_end:
.org 0x1E99C
m68k_01e99c:
        rts
m68k_01e99c_end:
.org 0x1E99E
m68k_01e99e:
        move.w 0xf35e:w,%d0
m68k_01e99e_end:
.org 0x1E9A2
m68k_01e9a2:
        addi.w #0xc,%d0
m68k_01e9a2_end:
.org 0x1E9A6
m68k_01e9a6:
        lsr.w #0x3,%d0
m68k_01e9a6_end:
.org 0x1E9A8
m68k_01e9a8:
        move.w %d0,%d1
m68k_01e9a8_end:
.org 0x1E9AA
m68k_01e9aa:
        subq.w #0x1,%d0
m68k_01e9aa_end:
.org 0x1E9AC
m68k_01e9ac:
        move.w 0xf360:w,%d2
m68k_01e9ac_end:
.org 0x1E9B0
m68k_01e9b0:
        addi.w #0xc,%d2
m68k_01e9b0_end:
.org 0x1E9B4
m68k_01e9b4:
        lsr.w #0x3,%d2
m68k_01e9b4_end:
.org 0x1E9B6
m68k_01e9b6:
        move.w %d2,%d3
m68k_01e9b6_end:
.org 0x1E9B8
m68k_01e9b8:
        subq.w #0x1,%d2
m68k_01e9b8_end:
.org 0x1E9BA
m68k_01e9ba:
        lea.l 0xafaa:w,%a0
m68k_01e9ba_end:
.org 0x1E9BE
m68k_01e9be:
        clr.w %d4
m68k_01e9be_end:
.org 0x1E9C0
m68k_01e9c0:
        cmp.b (%a0),%d0
m68k_01e9c0_end:
.org 0x1E9C2
m68k_01e9c2:
        beq.w (. + 10)
m68k_01e9c2_end:
.org 0x1E9C6
m68k_01e9c6:
        cmp.b (%a0),%d1
m68k_01e9c6_end:
.org 0x1E9C8
m68k_01e9c8:
        bne.w (. + 20)
m68k_01e9c8_end:
.org 0x1E9CC
m68k_01e9cc:
        cmp.b 0x1(%a0),%d2
m68k_01e9cc_end:
.org 0x1E9D0
m68k_01e9d0:
        beq.w (. + 26)
m68k_01e9d0_end:
.org 0x1E9D4
m68k_01e9d4:
        cmp.b 0x1(%a0),%d3
m68k_01e9d4_end:
.org 0x1E9D8
m68k_01e9d8:
        beq.w (. + 18)
m68k_01e9d8_end:
.org 0x1E9DC
m68k_01e9dc:
        addq.w #0x2,%a0
m68k_01e9dc_end:
.org 0x1E9DE
m68k_01e9de:
        addq.w #0x1,%d4
m68k_01e9de_end:
.org 0x1E9E0
m68k_01e9e0:
        cmpi.w #0x10,%d4
m68k_01e9e0_end:
.org 0x1E9E4
m68k_01e9e4:
        bcs.b (. + -36)
m68k_01e9e4_end:
.org 0x1E9E6
m68k_01e9e6:
        bra.w (. + 32)
m68k_01e9e6_end:
.org 0x1E9EA
m68k_01e9ea:
        ori.b #0x80,(%a0)
m68k_01e9ea_end:
.org 0x1E9EE
m68k_01e9ee:
        lea.l 0x9fff:w,%a2
m68k_01e9ee_end:
.org 0x1E9F2
m68k_01e9f2:
        move.w 0xf68a:w,%d0
m68k_01e9f2_end:
.org 0x1E9F6
m68k_01e9f6:
        move.b %d4,(%a2, %d0.w)
m68k_01e9f6_end:
.org 0x1E9FA
m68k_01e9fa:
        addq.b #0x1,(%a2, %d0.w)
m68k_01e9fa_end:
.org 0x1E9FE
m68k_01e9fe:
        andi.w #0xfffe,%sr
m68k_01e9fe_end:
.org 0x1EA02
m68k_01ea02:
        bra.w (. + 8)
m68k_01ea02_end:
.org 0x1EA06
m68k_01ea06:
        ori.w #0x1,%sr
m68k_01ea06_end:
.org 0x1EA0A
m68k_01ea0a:
        rts
m68k_01ea0a_end:
.org 0x1EA0C
m68k_01ea0c:
        move.w 0xf68a:w,%d1
m68k_01ea0c_end:
.org 0x1EA10
m68k_01ea10:
        lea.l 0xa027:w,%a0
m68k_01ea10_end:
.org 0x1EA14
m68k_01ea14:
        move.w 0xf378:w,%d0
m68k_01ea14_end:
.org 0x1EA18
m68k_01ea18:
        lsl.w #0x1,%d0
m68k_01ea18_end:
.org 0x1EA1A
m68k_01ea1a:
        lea.l 0xf500:w,%a1
m68k_01ea1a_end:
.org 0x1EA1E
m68k_01ea1e:
        move.w (%a1, %d0.w),%d0
m68k_01ea1e_end:
.org 0x1EA22
m68k_01ea22:
        move.b %d0,(%a0, %d1.w)
m68k_01ea22_end:
.org 0x1EA26
m68k_01ea26:
        move.w 0xf68a:w,%d2
m68k_01ea26_end:
.org 0x1EA2A
m68k_01ea2a:
        lea.l 0x9fff:w,%a0
m68k_01ea2a_end:
.org 0x1EA2E
m68k_01ea2e:
        clr.w %d1
m68k_01ea2e_end:
.org 0x1EA30
m68k_01ea30:
        move.b (%a0, %d2.w),%d1
m68k_01ea30_end:
.org 0x1EA34
m68k_01ea34:
        lsl.w #0x1,%d1
m68k_01ea34_end:
.org 0x1EA36
m68k_01ea36:
        lsl.w #0x5,%d2
m68k_01ea36_end:
.org 0x1EA38
m68k_01ea38:
        add.w %d1,%d2
m68k_01ea38_end:
.org 0x1EA3A
m68k_01ea3a:
        move.w %d0,%d3
m68k_01ea3a_end:
.org 0x1EA3C
m68k_01ea3c:
        lsl.w #0x2,%d3
m68k_01ea3c_end:
.org 0x1EA3E
m68k_01ea3e:
        lea.l 0xa150:w,%a2
m68k_01ea3e_end:
.org 0x1EA42
m68k_01ea42:
        lea.l 0xabda8:l,%a1
m68k_01ea42_end:
.org 0x1EA48
m68k_01ea48:
        clr.w %d1
m68k_01ea48_end:
.org 0x1EA4A
m68k_01ea4a:
        move.b (%a1, %d2.w),%d1
m68k_01ea4a_end:
.org 0x1EA4E
m68k_01ea4e:
        lsl.w #0x3,%d1
m68k_01ea4e_end:
.org 0x1EA50
m68k_01ea50:
        lsl.w #0x7,%d1
m68k_01ea50_end:
.org 0x1EA52
m68k_01ea52:
        move.w %d1,(%a2, %d3.w)
m68k_01ea52_end:
.org 0x1EA56
m68k_01ea56:
        clr.w %d1
m68k_01ea56_end:
.org 0x1EA58
m68k_01ea58:
        move.b 0x1(%a1, %d2.w),%d1
m68k_01ea58_end:
.org 0x1EA5C
m68k_01ea5c:
        lsl.w #0x3,%d1
m68k_01ea5c_end:
.org 0x1EA5E
m68k_01ea5e:
        lsl.w #0x7,%d1
m68k_01ea5e_end:
.org 0x1EA60
m68k_01ea60:
        move.w %d1,0x2(%a2, %d3.w)
m68k_01ea60_end:
.org 0x1EA64
m68k_01ea64:
        lea.l 0xf500:w,%a0
m68k_01ea64_end:
.org 0x1EA68
m68k_01ea68:
        lea.l 0xa550:w,%a1
m68k_01ea68_end:
.org 0x1EA6C
m68k_01ea6c:
        clr.w %d1
m68k_01ea6c_end:
.org 0x1EA6E
m68k_01ea6e:
        move.w (%a1)+,%d2
m68k_01ea6e_end:
.org 0x1EA70
m68k_01ea70:
        bmi.b (. + 12)
m68k_01ea70_end:
.org 0x1EA72
m68k_01ea72:
        cmp.w %d0,%d2
m68k_01ea72_end:
.org 0x1EA74
m68k_01ea74:
        beq.b (. + -6)
m68k_01ea74_end:
.org 0x1EA76
m68k_01ea76:
        move.w %d2,(%a0)+
m68k_01ea76_end:
.org 0x1EA78
m68k_01ea78:
        addq.w #0x1,%d1
m68k_01ea78_end:
.org 0x1EA7A
m68k_01ea7a:
        bra.b (. + -12)
m68k_01ea7a_end:
.org 0x1EA7C
m68k_01ea7c:
        move.w #0xffff,(%a0)+
m68k_01ea7c_end:
.org 0x1EA80
m68k_01ea80:
        tst.w %d1
m68k_01ea80_end:
.org 0x1EA82
m68k_01ea82:
        beq.w (. + 46)
m68k_01ea82_end:
.org 0x1EA86
m68k_01ea86:
        move.w %d1,0xf636:w
m68k_01ea86_end:
.org 0x1EA8A
m68k_01ea8a:
        move.w %d1,0xf6d0:w
m68k_01ea8a_end:
.org 0x1EA8E
m68k_01ea8e:
        move.w 0xf612:w,0xf38a:w
m68k_01ea8e_end:
.org 0x1EA94
m68k_01ea94:
        move.w #0x5,0xf3b0:w
m68k_01ea94_end:
.org 0x1EA9A
m68k_01ea9a:
        move.w #0x406,0xf612:w
m68k_01ea9a_end:
.org 0x1EAA0
m68k_01eaa0:
        clr.w 0xf36a:w
m68k_01eaa0_end:
.org 0x1EAA4
m68k_01eaa4:
        clr.w 0xf378:w
m68k_01eaa4_end:
.org 0x1EAA8
m68k_01eaa8:
        clr.w 0xf658:w
m68k_01eaa8_end:
.org 0x1EAAC
m68k_01eaac:
        bra.w (. + 26)
m68k_01eaac_end:
.org 0x1EAB0
m68k_01eab0:
        move.w 0xf612:w,0xf38a:w
m68k_01eab0_end:
.org 0x1EAB6
m68k_01eab6:
        move.w #0xf,0xf3b0:w
m68k_01eab6_end:
.org 0x1EABC
m68k_01eabc:
        move.w #0x406,0xf612:w
m68k_01eabc_end:
.org 0x1EAC2
m68k_01eac2:
        clr.w 0xf36a:w
m68k_01eac2_end:
.org 0x1EAC6
m68k_01eac6:
        rts
m68k_01eac6_end:
.org 0x1EAC8
m68k_01eac8:
        move.w 0xf612:w,0xf38a:w
m68k_01eac8_end:
.org 0x1EACE
m68k_01eace:
        move.w #0x6,0xf3b0:w
m68k_01eace_end:
.org 0x1EAD4
m68k_01ead4:
        move.w #0x405,0xf612:w
m68k_01ead4_end:
.org 0x1EADA
m68k_01eada:
        clr.w 0xf362:w
m68k_01eada_end:
.org 0x1EADE
m68k_01eade:
        move.w #0x102,%d0
m68k_01eade_end:
.org 0x1EAE2
m68k_01eae2:
        move.w %d0,0xaf80:w
m68k_01eae2_end:
.org 0x1EAE6
m68k_01eae6:
        jsr 0x676f2:l
m68k_01eae6_end:
.org 0x1EAEC
m68k_01eaec:
        move.w #0x2,0xf6d2:w
m68k_01eaec_end:
.org 0x1EAF2
m68k_01eaf2:
        rts
m68k_01eaf2_end:
.org 0x1EAF4
m68k_01eaf4:
        move.w 0xf378:w,%d0
m68k_01eaf4_end:
.org 0x1EAF8
m68k_01eaf8:
        lsl.w #0x1,%d0
m68k_01eaf8_end:
.org 0x1EAFA
m68k_01eafa:
        lea.l 0xf500:w,%a1
m68k_01eafa_end:
.org 0x1EAFE
m68k_01eafe:
        move.w (%a1, %d0.w),%d1
m68k_01eafe_end:
.org 0x1EB02
m68k_01eb02:
        move.w %d0,0xf6ce:w
m68k_01eb02_end:
.org 0x1EB06
m68k_01eb06:
        move.w 0xf612:w,0xf38a:w
m68k_01eb06_end:
.org 0x1EB0C
m68k_01eb0c:
        move.w #0x7,0xf3b0:w
m68k_01eb0c_end:
.org 0x1EB12
m68k_01eb12:
        move.w #0x406,0xf612:w
m68k_01eb12_end:
.org 0x1EB18
m68k_01eb18:
        clr.w 0xf36a:w
m68k_01eb18_end:
.org 0x1EB1C
m68k_01eb1c:
        rts
m68k_01eb1c_end:
.org 0x1EB1E
m68k_01eb1e:
        move.w 0xf612:w,0xf3c2:w
m68k_01eb1e_end:
.org 0x1EB24
m68k_01eb24:
        move.w #0x8,0xf3c4:w
m68k_01eb24_end:
.org 0x1EB2A
m68k_01eb2a:
        bsr.w (. + -582)
m68k_01eb2a_end:
.org 0x1EB2E
m68k_01eb2e:
        rts
m68k_01eb2e_end:
.org 0x1EB30
m68k_01eb30:
        bsr.w (. + 48)
m68k_01eb30_end:
.org 0x1EB34
m68k_01eb34:
        bsr.w (. + 194)
m68k_01eb34_end:
.org 0x1EB38
m68k_01eb38:
        jsr 0x1a3f4:l
m68k_01eb38_end:
.org 0x1EB3E
m68k_01eb3e:
        btst.b #0x5,0xf603:w
m68k_01eb3e_end:
.org 0x1EB44
m68k_01eb44:
        beq.b (. + 8)
m68k_01eb44_end:
.org 0x1EB46
m68k_01eb46:
        bsr.w (. + 236)
m68k_01eb46_end:
.org 0x1EB4A
m68k_01eb4a:
        bra.b (. + 20)
m68k_01eb4a_end:
.org 0x1EB4C
m68k_01eb4c:
        btst.b #0x4,0xf603:w
m68k_01eb4c_end:
.org 0x1EB52
m68k_01eb52:
        beq.b (. + 12)
m68k_01eb52_end:
.org 0x1EB54
m68k_01eb54:
        move.w #0x5,0xf362:w
m68k_01eb54_end:
.org 0x1EB5A
m68k_01eb5a:
        clr.w 0xf36a:w
m68k_01eb5a_end:
.org 0x1EB5E
m68k_01eb5e:
        rts
m68k_01eb5e_end:
.org 0x1EB60
m68k_01eb60:
        move.b 0xf602:w,%d0
m68k_01eb60_end:
.org 0x1EB64
m68k_01eb64:
        andi.w #0xf,%d0
m68k_01eb64_end:
.org 0x1EB68
m68k_01eb68:
        beq.w (. + 140)
m68k_01eb68_end:
.org 0x1EB6C
m68k_01eb6c:
        btst.l #0x0,%d0
m68k_01eb6c_end:
.org 0x1EB70
m68k_01eb70:
        beq.w (. + 26)
m68k_01eb70_end:
.org 0x1EB74
m68k_01eb74:
        tst.w 0xf35e:w
m68k_01eb74_end:
.org 0x1EB78
m68k_01eb78:
        beq.b (. + 54)
m68k_01eb78_end:
.org 0x1EB7A
m68k_01eb7a:
        subq.w #0x2,0xf35e:w
m68k_01eb7a_end:
.org 0x1EB7E
m68k_01eb7e:
        bcc.w (. + 48)
m68k_01eb7e_end:
.org 0x1EB82
m68k_01eb82:
        clr.w 0xf35e:w
m68k_01eb82_end:
.org 0x1EB86
m68k_01eb86:
        bra.w (. + 40)
m68k_01eb86_end:
.org 0x1EB8A
m68k_01eb8a:
        btst.l #0x1,%d0
m68k_01eb8a_end:
.org 0x1EB8E
m68k_01eb8e:
        beq.w (. + 32)
m68k_01eb8e_end:
.org 0x1EB92
m68k_01eb92:
        cmpi.w #0xd0,0xf35e:w
m68k_01eb92_end:
.org 0x1EB98
m68k_01eb98:
        bcc.w (. + 22)
m68k_01eb98_end:
.org 0x1EB9C
m68k_01eb9c:
        addq.w #0x2,0xf35e:w
m68k_01eb9c_end:
.org 0x1EBA0
m68k_01eba0:
        cmpi.w #0xd0,0xf35e:w
m68k_01eba0_end:
.org 0x1EBA6
m68k_01eba6:
        bls.b (. + 8)
m68k_01eba6_end:
.org 0x1EBA8
m68k_01eba8:
        move.w #0xd0,0xf35e:w
m68k_01eba8_end:
.org 0x1EBAE
m68k_01ebae:
        btst.l #0x2,%d0
m68k_01ebae_end:
.org 0x1EBB2
m68k_01ebb2:
        beq.w (. + 28)
m68k_01ebb2_end:
.org 0x1EBB6
m68k_01ebb6:
        tst.w 0xf360:w
m68k_01ebb6_end:
.org 0x1EBBA
m68k_01ebba:
        beq.w (. + 58)
m68k_01ebba_end:
.org 0x1EBBE
m68k_01ebbe:
        subq.w #0x3,0xf360:w
m68k_01ebbe_end:
.org 0x1EBC2
m68k_01ebc2:
        bcc.w (. + 50)
m68k_01ebc2_end:
.org 0x1EBC6
m68k_01ebc6:
        clr.w 0xf360:w
m68k_01ebc6_end:
.org 0x1EBCA
m68k_01ebca:
        bra.w (. + 42)
m68k_01ebca_end:
.org 0x1EBCE
m68k_01ebce:
        btst.l #0x3,%d0
m68k_01ebce_end:
.org 0x1EBD2
m68k_01ebd2:
        beq.w (. + 34)
m68k_01ebd2_end:
.org 0x1EBD6
m68k_01ebd6:
        cmpi.w #0x130,0xf360:w
m68k_01ebd6_end:
.org 0x1EBDC
m68k_01ebdc:
        bcc.w (. + 24)
m68k_01ebdc_end:
.org 0x1EBE0
m68k_01ebe0:
        addq.w #0x3,0xf360:w
m68k_01ebe0_end:
.org 0x1EBE4
m68k_01ebe4:
        cmpi.w #0x130,0xf360:w
m68k_01ebe4_end:
.org 0x1EBEA
m68k_01ebea:
        bls.w (. + 10)
m68k_01ebea_end:
.org 0x1EBEE
m68k_01ebee:
        move.w #0x130,0xf360:w
m68k_01ebee_end:
.org 0x1EBF4
m68k_01ebf4:
        rts
m68k_01ebf4_end:
.org 0x1EBF6
m68k_01ebf6:
        btst.b #0x3,0xf321:w
m68k_01ebf6_end:
.org 0x1EBFC
m68k_01ebfc:
        bne.w (. + 26)
m68k_01ebfc_end:
.org 0x1EC00
m68k_01ec00:
        move.w 0xf35e:w,%d0
m68k_01ec00_end:
.org 0x1EC04
m68k_01ec04:
        move.w 0xf360:w,%d1
m68k_01ec04_end:
.org 0x1EC08
m68k_01ec08:
        clr.w %d2
m68k_01ec08_end:
.org 0x1EC0A
m68k_01ec0a:
        lea.l 12(%pc),%a0
m68k_01ec0a_end:
.org 0x1EC0E
m68k_01ec0e:
        nop
m68k_01ec0e_end:
.org 0x1EC10
m68k_01ec10:
        jsr 0xac08:l
m68k_01ec10_end:
.org 0x1EC16
m68k_01ec16:
        rts
m68k_01ec16_end:
.org 0x1EC32
m68k_01ec32:
        move.w 0xf35e:w,%d0
m68k_01ec32_end:
.org 0x1EC36
m68k_01ec36:
        addi.w #0xc,%d0
m68k_01ec36_end:
.org 0x1EC3A
m68k_01ec3a:
        lsr.w #0x3,%d0
m68k_01ec3a_end:
.org 0x1EC3C
m68k_01ec3c:
        move.w %d0,%d1
m68k_01ec3c_end:
.org 0x1EC3E
m68k_01ec3e:
        subq.w #0x1,%d0
m68k_01ec3e_end:
.org 0x1EC40
m68k_01ec40:
        beq.w (. + 164)
m68k_01ec40_end:
.org 0x1EC44
m68k_01ec44:
        move.w 0xf360:w,%d2
m68k_01ec44_end:
.org 0x1EC48
m68k_01ec48:
        addi.w #0xc,%d2
m68k_01ec48_end:
.org 0x1EC4C
m68k_01ec4c:
        lsr.w #0x3,%d2
m68k_01ec4c_end:
.org 0x1EC4E
m68k_01ec4e:
        move.w %d2,%d3
m68k_01ec4e_end:
.org 0x1EC50
m68k_01ec50:
        subq.w #0x1,%d2
m68k_01ec50_end:
.org 0x1EC52
m68k_01ec52:
        beq.w (. + 146)
m68k_01ec52_end:
.org 0x1EC56
m68k_01ec56:
        lea.l 0xafaa:w,%a0
m68k_01ec56_end:
.org 0x1EC5A
m68k_01ec5a:
        clr.w %d4
m68k_01ec5a_end:
.org 0x1EC5C
m68k_01ec5c:
        cmp.b (%a0),%d0
m68k_01ec5c_end:
.org 0x1EC5E
m68k_01ec5e:
        beq.w (. + 10)
m68k_01ec5e_end:
.org 0x1EC62
m68k_01ec62:
        cmp.b (%a0),%d1
m68k_01ec62_end:
.org 0x1EC64
m68k_01ec64:
        bne.w (. + 20)
m68k_01ec64_end:
.org 0x1EC68
m68k_01ec68:
        cmp.b 0x1(%a0),%d2
m68k_01ec68_end:
.org 0x1EC6C
m68k_01ec6c:
        beq.w (. + 26)
m68k_01ec6c_end:
.org 0x1EC70
m68k_01ec70:
        cmp.b 0x1(%a0),%d3
m68k_01ec70_end:
.org 0x1EC74
m68k_01ec74:
        beq.w (. + 18)
m68k_01ec74_end:
.org 0x1EC78
m68k_01ec78:
        addq.w #0x2,%a0
m68k_01ec78_end:
.org 0x1EC7A
m68k_01ec7a:
        addq.w #0x1,%d4
m68k_01ec7a_end:
.org 0x1EC7C
m68k_01ec7c:
        cmpi.w #0x10,%d4
m68k_01ec7c_end:
.org 0x1EC80
m68k_01ec80:
        bcs.b (. + -36)
m68k_01ec80_end:
.org 0x1EC82
m68k_01ec82:
        bra.w (. + 98)
m68k_01ec82_end:
.org 0x1EC86
m68k_01ec86:
        ori.b #0x80,(%a0)
m68k_01ec86_end:
.org 0x1EC8A
m68k_01ec8a:
        lea.l 0xf500:w,%a1
m68k_01ec8a_end:
.org 0x1EC8E
m68k_01ec8e:
        move.w 0xf378:w,%d3
m68k_01ec8e_end:
.org 0x1EC92
m68k_01ec92:
        lsl.w #0x1,%d3
m68k_01ec92_end:
.org 0x1EC94
m68k_01ec94:
        move.w (%a1, %d3.w),%d4
m68k_01ec94_end:
.org 0x1EC98
m68k_01ec98:
        ori.w #0x4000,(%a1, %d3.w)
m68k_01ec98_end:
.org 0x1EC9E
m68k_01ec9e:
        lea.l 0xa150:w,%a2
m68k_01ec9e_end:
.org 0x1ECA2
m68k_01eca2:
        lsl.w #0x2,%d4
m68k_01eca2_end:
.org 0x1ECA4
m68k_01eca4:
        move.b (%a0),%d0
m68k_01eca4_end:
.org 0x1ECA6
m68k_01eca6:
        andi.w #0x7f,%d0
m68k_01eca6_end:
.org 0x1ECAA
m68k_01ecaa:
        lsl.w #0x3,%d0
m68k_01ecaa_end:
.org 0x1ECAC
m68k_01ecac:
        lsl.w #0x7,%d0
m68k_01ecac_end:
.org 0x1ECAE
m68k_01ecae:
        move.w %d0,(%a2, %d4.w)
m68k_01ecae_end:
.org 0x1ECB2
m68k_01ecb2:
        clr.w %d0
m68k_01ecb2_end:
.org 0x1ECB4
m68k_01ecb4:
        move.b 0x1(%a0),%d0
m68k_01ecb4_end:
.org 0x1ECB8
m68k_01ecb8:
        lsl.w #0x3,%d0
m68k_01ecb8_end:
.org 0x1ECBA
m68k_01ecba:
        lsl.w #0x7,%d0
m68k_01ecba_end:
.org 0x1ECBC
m68k_01ecbc:
        move.w %d0,0x2(%a2, %d4.w)
m68k_01ecbc_end:
.org 0x1ECC0
m68k_01ecc0:
        move.w #0xac,%d0
m68k_01ecc0_end:
.org 0x1ECC4
m68k_01ecc4:
        jsr 0x808a:l
m68k_01ecc4_end:
.org 0x1ECCA
m68k_01ecca:
        subq.w #0x1,0xf6d0:w
m68k_01ecca_end:
.org 0x1ECCE
m68k_01ecce:
        beq.b (. + 16)
m68k_01ecce_end:
.org 0x1ECD0
m68k_01ecd0:
        clr.w 0xf36a:w
m68k_01ecd0_end:
.org 0x1ECD4
m68k_01ecd4:
        move.w #0x5,0xf362:w
m68k_01ecd4_end:
.org 0x1ECDA
m68k_01ecda:
        bra.w (. + 10)
m68k_01ecda_end:
.org 0x1ECDE
m68k_01ecde:
        move.w #0xf,0xf362:w
m68k_01ecde_end:
.org 0x1ECE4
m68k_01ece4:
        rts
m68k_01ece4_end:
.org 0x1ECE6
m68k_01ece6:
        btst.b #0x5,0xf603:w
m68k_01ece6_end:
.org 0x1ECEC
m68k_01ecec:
        beq.b (. + 8)
m68k_01ecec_end:
.org 0x1ECEE
m68k_01ecee:
        move.w #0xf,0xf362:w
m68k_01ecee_end:
.org 0x1ECF4
m68k_01ecf4:
        rts
m68k_01ecf4_end:
.org 0x1ECF6
m68k_01ecf6:
        lea.l 0x9fff:w,%a0
m68k_01ecf6_end:
.org 0x1ECFA
m68k_01ecfa:
        move.w 0xf68a:w,%d0
m68k_01ecfa_end:
.org 0x1ECFE
m68k_01ecfe:
        tst.b (%a0, %d0.w)
m68k_01ecfe_end:
.org 0x1ED02
m68k_01ed02:
        bne.w (. + 52)
m68k_01ed02_end:
.org 0x1ED06
m68k_01ed06:
        bsr.w (. + 62)
m68k_01ed06_end:
.org 0x1ED0A
m68k_01ed0a:
        bsr.w (. + 110)
m68k_01ed0a_end:
.org 0x1ED0E
m68k_01ed0e:
        bsr.w (. + 140)
m68k_01ed0e_end:
.org 0x1ED12
m68k_01ed12:
        move.w #0x68,0xf35e:w
m68k_01ed12_end:
.org 0x1ED18
m68k_01ed18:
        move.w #0x98,0xf360:w
m68k_01ed18_end:
.org 0x1ED1E
m68k_01ed1e:
        addq.w #0x1,0xf362:w
m68k_01ed1e_end:
.org 0x1ED22
m68k_01ed22:
        clr.w 0xf378:w
m68k_01ed22_end:
.org 0x1ED26
m68k_01ed26:
        clr.w 0xf658:w
m68k_01ed26_end:
.org 0x1ED2A
m68k_01ed2a:
        tst.w 0xf6d0:w
m68k_01ed2a_end:
.org 0x1ED2E
m68k_01ed2e:
        beq.w (. + 458)
m68k_01ed2e_end:
.org 0x1ED32
m68k_01ed32:
        bra.w (. + 16)
m68k_01ed32_end:
.org 0x1ED36
m68k_01ed36:
        move.w #0xd8,0xf600:w
m68k_01ed36_end:
.org 0x1ED3C
m68k_01ed3c:
        move.w #0xf,0xf362:w
m68k_01ed3c_end:
.org 0x1ED42
m68k_01ed42:
        rts
m68k_01ed42_end:
.org 0x1ED44
m68k_01ed44:
        lea.l 0xac2aa:l,%a0
m68k_01ed44_end:
.org 0x1ED4A
m68k_01ed4a:
        move.w 0xf68a:w,%d0
m68k_01ed4a_end:
.org 0x1ED4E
m68k_01ed4e:
        lsl.w #0x5,%d0
m68k_01ed4e_end:
.org 0x1ED50
m68k_01ed50:
        lea.l 0xa150:w,%a1
m68k_01ed50_end:
.org 0x1ED54
m68k_01ed54:
        move.w 0xa5a4:w,%d1
m68k_01ed54_end:
.org 0x1ED58
m68k_01ed58:
        lsl.w #0x2,%d1
m68k_01ed58_end:
.org 0x1ED5A
m68k_01ed5a:
        clr.w %d2
m68k_01ed5a_end:
.org 0x1ED5C
m68k_01ed5c:
        move.b (%a0, %d0.w),%d2
m68k_01ed5c_end:
.org 0x1ED60
m68k_01ed60:
        lsl.w #0x3,%d2
m68k_01ed60_end:
.org 0x1ED62
m68k_01ed62:
        lsl.w #0x7,%d2
m68k_01ed62_end:
.org 0x1ED64
m68k_01ed64:
        move.w %d2,(%a1, %d1.w)
m68k_01ed64_end:
.org 0x1ED68
m68k_01ed68:
        clr.w %d2
m68k_01ed68_end:
.org 0x1ED6A
m68k_01ed6a:
        move.b 0x1(%a0, %d0.w),%d2
m68k_01ed6a_end:
.org 0x1ED6E
m68k_01ed6e:
        lsl.w #0x3,%d2
m68k_01ed6e_end:
.org 0x1ED70
m68k_01ed70:
        lsl.w #0x7,%d2
m68k_01ed70_end:
.org 0x1ED72
m68k_01ed72:
        move.w %d2,0x2(%a1, %d1.w)
m68k_01ed72_end:
.org 0x1ED76
m68k_01ed76:
        rts
m68k_01ed76_end:
.org 0x1ED78
m68k_01ed78:
        lea.l 0xf500:w,%a0
m68k_01ed78_end:
.org 0x1ED7C
m68k_01ed7c:
        lea.l 0xa5a6:w,%a1
m68k_01ed7c_end:
.org 0x1ED80
m68k_01ed80:
        clr.w %d1
m68k_01ed80_end:
.org 0x1ED82
m68k_01ed82:
        move.w (%a1)+,%d2
m68k_01ed82_end:
.org 0x1ED84
m68k_01ed84:
        bmi.b (. + 8)
m68k_01ed84_end:
.org 0x1ED86
m68k_01ed86:
        move.w %d2,(%a0)+
m68k_01ed86_end:
.org 0x1ED88
m68k_01ed88:
        addq.w #0x1,%d1
m68k_01ed88_end:
.org 0x1ED8A
m68k_01ed8a:
        bra.b (. + -8)
m68k_01ed8a_end:
.org 0x1ED8C
m68k_01ed8c:
        move.w #0xffff,(%a0)+
m68k_01ed8c_end:
.org 0x1ED90
m68k_01ed90:
        move.w %d1,0xf636:w
m68k_01ed90_end:
.org 0x1ED94
m68k_01ed94:
        move.w %d1,0xf6d0:w
m68k_01ed94_end:
.org 0x1ED98
m68k_01ed98:
        rts
m68k_01ed98_end:
.org 0x1ED9A
m68k_01ed9a:
        lea.l 0xac2ac:l,%a0
m68k_01ed9a_end:
.org 0x1EDA0
m68k_01eda0:
        move.w 0xf68a:w,%d0
m68k_01eda0_end:
.org 0x1EDA4
m68k_01eda4:
        lsl.w #0x5,%d0
m68k_01eda4_end:
.org 0x1EDA6
m68k_01eda6:
        adda.w %d0,%a0
m68k_01eda6_end:
.org 0x1EDA8
m68k_01eda8:
        lea.l 0xafaa:w,%a1
m68k_01eda8_end:
.org 0x1EDAC
m68k_01edac:
        move.w #0xffff,(%a1)+
m68k_01edac_end:
.org 0x1EDB0
m68k_01edb0:
        move.w #0xe,%d0
m68k_01edb0_end:
.org 0x1EDB4
m68k_01edb4:
        move.w (%a0)+,(%a1)+
m68k_01edb4_end:
.org 0x1EDB6
m68k_01edb6:
        dbra %d0,(. + -2)
m68k_01edb6_end:
.org 0x1EDBA
m68k_01edba:
        rts
m68k_01edba_end:
.org 0x1EDBC
m68k_01edbc:
        move.w 0xf612:w,0xf38a:w
m68k_01edbc_end:
.org 0x1EDC2
m68k_01edc2:
        move.w #0xc,0xf3b0:w
m68k_01edc2_end:
.org 0x1EDC8
m68k_01edc8:
        move.w #0x405,0xf612:w
m68k_01edc8_end:
.org 0x1EDCE
m68k_01edce:
        clr.w 0xf362:w
m68k_01edce_end:
.org 0x1EDD2
m68k_01edd2:
        move.w #0x102,%d0
m68k_01edd2_end:
.org 0x1EDD6
m68k_01edd6:
        move.w %d0,0xaf80:w
m68k_01edd6_end:
.org 0x1EDDA
m68k_01edda:
        jsr 0x676f2:l
m68k_01edda_end:
.org 0x1EDE0
m68k_01ede0:
        move.w #0x2,0xf6d2:w
m68k_01ede0_end:
.org 0x1EDE6
m68k_01ede6:
        rts
m68k_01ede6_end:
.org 0x1EDE8
m68k_01ede8:
        move.w 0xf378:w,%d0
m68k_01ede8_end:
.org 0x1EDEC
m68k_01edec:
        lsl.w #0x1,%d0
m68k_01edec_end:
.org 0x1EDEE
m68k_01edee:
        lea.l 0xf500:w,%a1
m68k_01edee_end:
.org 0x1EDF2
m68k_01edf2:
        move.w (%a1, %d0.w),%d1
m68k_01edf2_end:
.org 0x1EDF6
m68k_01edf6:
        move.w %d0,0xf6ce:w
m68k_01edf6_end:
.org 0x1EDFA
m68k_01edfa:
        move.w 0xf612:w,0xf38a:w
m68k_01edfa_end:
.org 0x1EE00
m68k_01ee00:
        move.w #0xd,0xf3b0:w
m68k_01ee00_end:
.org 0x1EE06
m68k_01ee06:
        move.w #0x406,0xf612:w
m68k_01ee06_end:
.org 0x1EE0C
m68k_01ee0c:
        clr.w 0xf36a:w
m68k_01ee0c_end:
.org 0x1EE10
m68k_01ee10:
        rts
m68k_01ee10_end:
.org 0x1EE12
m68k_01ee12:
        move.w 0xf612:w,0xf3c2:w
m68k_01ee12_end:
.org 0x1EE18
m68k_01ee18:
        move.w #0xe,0xf3c4:w
m68k_01ee18_end:
.org 0x1EE1E
m68k_01ee1e:
        bsr.w (. + -1338)
m68k_01ee1e_end:
.org 0x1EE22
m68k_01ee22:
        rts
m68k_01ee22_end:
.org 0x1EE24
m68k_01ee24:
        bsr.w (. + -708)
m68k_01ee24_end:
.org 0x1EE28
m68k_01ee28:
        bsr.w (. + -562)
m68k_01ee28_end:
.org 0x1EE2C
m68k_01ee2c:
        jsr 0x1a3f4:l
m68k_01ee2c_end:
.org 0x1EE32
m68k_01ee32:
        btst.b #0x5,0xf603:w
m68k_01ee32_end:
.org 0x1EE38
m68k_01ee38:
        beq.b (. + 8)
m68k_01ee38_end:
.org 0x1EE3A
m68k_01ee3a:
        bsr.w (. + 26)
m68k_01ee3a_end:
.org 0x1EE3E
m68k_01ee3e:
        bra.b (. + 20)
m68k_01ee3e_end:
.org 0x1EE40
m68k_01ee40:
        btst.b #0x4,0xf603:w
m68k_01ee40_end:
.org 0x1EE46
m68k_01ee46:
        beq.b (. + 12)
m68k_01ee46_end:
.org 0x1EE48
m68k_01ee48:
        move.w #0xb,0xf362:w
m68k_01ee48_end:
.org 0x1EE4E
m68k_01ee4e:
        clr.w 0xf36a:w
m68k_01ee4e_end:
.org 0x1EE52
m68k_01ee52:
        rts
m68k_01ee52_end:
.org 0x1EE54
m68k_01ee54:
        move.w 0xf35e:w,%d0
m68k_01ee54_end:
.org 0x1EE58
m68k_01ee58:
        addi.w #0xc,%d0
m68k_01ee58_end:
.org 0x1EE5C
m68k_01ee5c:
        lsr.w #0x3,%d0
m68k_01ee5c_end:
.org 0x1EE5E
m68k_01ee5e:
        move.w %d0,%d1
m68k_01ee5e_end:
.org 0x1EE60
m68k_01ee60:
        subq.w #0x1,%d0
m68k_01ee60_end:
.org 0x1EE62
m68k_01ee62:
        move.w 0xf360:w,%d2
m68k_01ee62_end:
.org 0x1EE66
m68k_01ee66:
        addi.w #0xc,%d2
m68k_01ee66_end:
.org 0x1EE6A
m68k_01ee6a:
        lsr.w #0x3,%d2
m68k_01ee6a_end:
.org 0x1EE6C
m68k_01ee6c:
        move.w %d2,%d3
m68k_01ee6c_end:
.org 0x1EE6E
m68k_01ee6e:
        subq.w #0x1,%d2
m68k_01ee6e_end:
.org 0x1EE70
m68k_01ee70:
        lea.l 0xafaa:w,%a0
m68k_01ee70_end:
.org 0x1EE74
m68k_01ee74:
        clr.w %d4
m68k_01ee74_end:
.org 0x1EE76
m68k_01ee76:
        cmp.b (%a0),%d0
m68k_01ee76_end:
.org 0x1EE78
m68k_01ee78:
        beq.w (. + 10)
m68k_01ee78_end:
.org 0x1EE7C
m68k_01ee7c:
        cmp.b (%a0),%d1
m68k_01ee7c_end:
.org 0x1EE7E
m68k_01ee7e:
        bne.w (. + 20)
m68k_01ee7e_end:
.org 0x1EE82
m68k_01ee82:
        cmp.b 0x1(%a0),%d2
m68k_01ee82_end:
.org 0x1EE86
m68k_01ee86:
        beq.w (. + 26)
m68k_01ee86_end:
.org 0x1EE8A
m68k_01ee8a:
        cmp.b 0x1(%a0),%d3
m68k_01ee8a_end:
.org 0x1EE8E
m68k_01ee8e:
        beq.w (. + 18)
m68k_01ee8e_end:
.org 0x1EE92
m68k_01ee92:
        addq.w #0x2,%a0
m68k_01ee92_end:
.org 0x1EE94
m68k_01ee94:
        addq.w #0x1,%d4
m68k_01ee94_end:
.org 0x1EE96
m68k_01ee96:
        cmpi.w #0x10,%d4
m68k_01ee96_end:
.org 0x1EE9A
m68k_01ee9a:
        bcs.b (. + -36)
m68k_01ee9a_end:
.org 0x1EE9C
m68k_01ee9c:
        bra.w (. + 152)
m68k_01ee9c_end:
.org 0x1EEA0
m68k_01eea0:
        ori.b #0x80,(%a0)
m68k_01eea0_end:
.org 0x1EEA4
m68k_01eea4:
        lea.l 0xf500:w,%a1
m68k_01eea4_end:
.org 0x1EEA8
m68k_01eea8:
        move.w 0xf378:w,%d3
m68k_01eea8_end:
.org 0x1EEAC
m68k_01eeac:
        lsl.w #0x1,%d3
m68k_01eeac_end:
.org 0x1EEAE
m68k_01eeae:
        move.w (%a1, %d3.w),%d4
m68k_01eeae_end:
.org 0x1EEB2
m68k_01eeb2:
        ori.w #0x4000,(%a1, %d3.w)
m68k_01eeb2_end:
.org 0x1EEB8
m68k_01eeb8:
        lea.l 0xa150:w,%a2
m68k_01eeb8_end:
.org 0x1EEBC
m68k_01eebc:
        lsl.w #0x2,%d4
m68k_01eebc_end:
.org 0x1EEBE
m68k_01eebe:
        move.b (%a0),%d0
m68k_01eebe_end:
.org 0x1EEC0
m68k_01eec0:
        andi.w #0x7f,%d0
m68k_01eec0_end:
.org 0x1EEC4
m68k_01eec4:
        lsl.w #0x3,%d0
m68k_01eec4_end:
.org 0x1EEC6
m68k_01eec6:
        lsl.w #0x7,%d0
m68k_01eec6_end:
.org 0x1EEC8
m68k_01eec8:
        move.w %d0,(%a2, %d4.w)
m68k_01eec8_end:
.org 0x1EECC
m68k_01eecc:
        clr.w %d0
m68k_01eecc_end:
.org 0x1EECE
m68k_01eece:
        move.b 0x1(%a0),%d0
m68k_01eece_end:
.org 0x1EED2
m68k_01eed2:
        lsl.w #0x3,%d0
m68k_01eed2_end:
.org 0x1EED4
m68k_01eed4:
        lsl.w #0x7,%d0
m68k_01eed4_end:
.org 0x1EED6
m68k_01eed6:
        move.w %d0,0x2(%a2, %d4.w)
m68k_01eed6_end:
.org 0x1EEDA
m68k_01eeda:
        move.w #0xac,%d0
m68k_01eeda_end:
.org 0x1EEDE
m68k_01eede:
        jsr 0x808a:l
m68k_01eede_end:
.org 0x1EEE4
m68k_01eee4:
        subq.w #0x1,0xf6d0:w
m68k_01eee4_end:
.org 0x1EEE8
m68k_01eee8:
        beq.b (. + 16)
m68k_01eee8_end:
.org 0x1EEEA
m68k_01eeea:
        clr.w 0xf36a:w
m68k_01eeea_end:
.org 0x1EEEE
m68k_01eeee:
        move.w #0xb,0xf362:w
m68k_01eeee_end:
.org 0x1EEF4
m68k_01eef4:
        bra.w (. + 64)
m68k_01eef4_end:
.org 0x1EEF8
m68k_01eef8:
        clr.w 0xf6d6:w
m68k_01eef8_end:
.org 0x1EEFC
m68k_01eefc:
        move.w #0xffff,0xa5f8:w
m68k_01eefc_end:
.org 0x1EF02
m68k_01ef02:
        move.w 0xf68c:w,%d0
m68k_01ef02_end:
.org 0x1EF06
m68k_01ef06:
        cmp.w 0xf67a:w,%d0
m68k_01ef06_end:
.org 0x1EF0A
m68k_01ef0a:
        beq.w (. + 36)
m68k_01ef0a_end:
.org 0x1EF0E
m68k_01ef0e:
        cmp.w 0xf67c:w,%d0
m68k_01ef0e_end:
.org 0x1EF12
m68k_01ef12:
        beq.w (. + 28)
m68k_01ef12_end:
.org 0x1EF16
m68k_01ef16:
        cmp.w 0xf67e:w,%d0
m68k_01ef16_end:
.org 0x1EF1A
m68k_01ef1a:
        beq.w (. + 20)
m68k_01ef1a_end:
.org 0x1EF1E
m68k_01ef1e:
        move.w #0xf,0xf362:w
m68k_01ef1e_end:
.org 0x1EF24
m68k_01ef24:
        move.w #0xb8,0xf600:w
m68k_01ef24_end:
.org 0x1EF2A
m68k_01ef2a:
        bra.w (. + 10)
m68k_01ef2a_end:
.org 0x1EF2E
m68k_01ef2e:
        move.w #0x1,0xf362:w
m68k_01ef2e_end:
.org 0x1EF34
m68k_01ef34:
        rts
m68k_01ef34_end:
.org 0x1EF36
m68k_01ef36:
        clr.w 0xf6d6:w
m68k_01ef36_end:
.org 0x1EF3A
m68k_01ef3a:
        move.w 0xf68c:w,%d0
m68k_01ef3a_end:
.org 0x1EF3E
m68k_01ef3e:
        cmp.w 0xf67a:w,%d0
m68k_01ef3e_end:
.org 0x1EF42
m68k_01ef42:
        beq.w (. + 20)
m68k_01ef42_end:
.org 0x1EF46
m68k_01ef46:
        cmp.w 0xf67c:w,%d0
m68k_01ef46_end:
.org 0x1EF4A
m68k_01ef4a:
        beq.w (. + 12)
m68k_01ef4a_end:
.org 0x1EF4E
m68k_01ef4e:
        cmp.w 0xf67e:w,%d0
m68k_01ef4e_end:
.org 0x1EF52
m68k_01ef52:
        bne.w (. + 18)
m68k_01ef52_end:
.org 0x1EF56
m68k_01ef56:
        move.w #0x408,0xf612:w
m68k_01ef56_end:
.org 0x1EF5C
m68k_01ef5c:
        clr.w 0xf362:w
m68k_01ef5c_end:
.org 0x1EF60
m68k_01ef60:
        bra.w (. + 14)
m68k_01ef60_end:
.org 0x1EF64
m68k_01ef64:
        move.w #0x407,0xf612:w
m68k_01ef64_end:
.org 0x1EF6A
m68k_01ef6a:
        clr.w 0xf362:w
m68k_01ef6a_end:
.org 0x1EF6E
m68k_01ef6e:
        move.w #0xbc,0xf600:w
m68k_01ef6e_end:
.org 0x1EF74
m68k_01ef74:
        clr.w 0xf6d4:w
m68k_01ef74_end:
.org 0x1EF78
m68k_01ef78:
        rts
m68k_01ef78_end:
.org 0x1FB08
m68k_01fb08:
        addq.w #0x1,0xf362:w
m68k_01fb08_end:
.org 0x1FB0C
m68k_01fb0c:
        bsr.w (. + 6)
m68k_01fb0c_end:
.org 0x1FB10
m68k_01fb10:
        rts
m68k_01fb10_end:
.org 0x1FB12
m68k_01fb12:
        move.w 0xffff8114:l,%d0
m68k_01fb12_end:
.org 0x1FB18
m68k_01fb18:
        cmpi.w #0x2,%d0
m68k_01fb18_end:
.org 0x1FB1C
m68k_01fb1c:
        beq.w (. + 38)
m68k_01fb1c_end:
.org 0x1FB20
m68k_01fb20:
        cmpi.w #0x5,%d0
m68k_01fb20_end:
.org 0x1FB24
m68k_01fb24:
        beq.w (. + 30)
m68k_01fb24_end:
.org 0x1FB28
m68k_01fb28:
        cmpi.w #0x6,%d0
m68k_01fb28_end:
.org 0x1FB2C
m68k_01fb2c:
        beq.w (. + 50)
m68k_01fb2c_end:
.org 0x1FB30
m68k_01fb30:
        cmpi.w #0x7,%d0
m68k_01fb30_end:
.org 0x1FB34
m68k_01fb34:
        beq.w (. + 42)
m68k_01fb34_end:
.org 0x1FB38
m68k_01fb38:
        move.w 0xffff80e2:l,%d0
m68k_01fb38_end:
.org 0x1FB3E
m68k_01fb3e:
        bra.w (. + 10)
m68k_01fb3e_end:
.org 0x1FB42
m68k_01fb42:
        move.w 0xffff80e0:l,%d0
m68k_01fb42_end:
.org 0x1FB48
m68k_01fb48:
        clr.w 0xf6d6:w
m68k_01fb48_end:
.org 0x1FB4C
m68k_01fb4c:
        cmp.w 0xf702:w,%d0
m68k_01fb4c_end:
.org 0x1FB50
m68k_01fb50:
        bne.w (. + 20)
m68k_01fb50_end:
.org 0x1FB54
m68k_01fb54:
        move.w #0x2,0xf6d6:w
m68k_01fb54_end:
.org 0x1FB5A
m68k_01fb5a:
        bra.w (. + 10)
m68k_01fb5a_end:
.org 0x1FB5E
m68k_01fb5e:
        move.w #0x5,0xf362:w
m68k_01fb5e_end:
.org 0x1FB64
m68k_01fb64:
        rts
m68k_01fb64_end:
.org 0x1FB66
m68k_01fb66:
        lea.l 0xf702:w,%a0
m68k_01fb66_end:
.org 0x1FB6A
m68k_01fb6a:
        lea.l 0xf706:w,%a1
m68k_01fb6a_end:
.org 0x1FB6E
m68k_01fb6e:
        move.w 0xf68e:w,%d1
m68k_01fb6e_end:
.org 0x1FB72
m68k_01fb72:
        btst.b #0x1,0xf6d7:w
m68k_01fb72_end:
.org 0x1FB78
m68k_01fb78:
        bne.w (. + 10)
m68k_01fb78_end:
.org 0x1FB7C
m68k_01fb7c:
        exg %a0,%a1
m68k_01fb7c_end:
.org 0x1FB7E
m68k_01fb7e:
        move.w 0xf68c:w,%d1
m68k_01fb7e_end:
.org 0x1FB82
m68k_01fb82:
        lea.l 0xceae:w,%a2
m68k_01fb82_end:
.org 0x1FB86
m68k_01fb86:
        move.w (%a0),%d0
m68k_01fb86_end:
.org 0x1FB88
m68k_01fb88:
        move.b #0x64,(%a2, %d0.w)
m68k_01fb88_end:
.org 0x1FB8E
m68k_01fb8e:
        bsr.w (. + 194)
m68k_01fb8e_end:
.org 0x1FB92
m68k_01fb92:
        bcs.w (. + 50)
m68k_01fb92_end:
.org 0x1FB96
m68k_01fb96:
        bsr.w (. + 232)
m68k_01fb96_end:
.org 0x1FB9A
m68k_01fb9a:
        bcs.w (. + 42)
m68k_01fb9a_end:
.org 0x1FB9E
m68k_01fb9e:
        bsr.w (. + 268)
m68k_01fb9e_end:
.org 0x1FBA2
m68k_01fba2:
        cmp.w 0xf67a:w,%d1
m68k_01fba2_end:
.org 0x1FBA6
m68k_01fba6:
        beq.w (. + 40)
m68k_01fba6_end:
.org 0x1FBAA
m68k_01fbaa:
        cmp.w 0xf67c:w,%d1
m68k_01fbaa_end:
.org 0x1FBAE
m68k_01fbae:
        beq.w (. + 32)
m68k_01fbae_end:
.org 0x1FBB2
m68k_01fbb2:
        cmp.w 0xf67e:w,%d1
m68k_01fbb2_end:
.org 0x1FBB6
m68k_01fbb6:
        beq.w (. + 24)
m68k_01fbb6_end:
.org 0x1FBBA
m68k_01fbba:
        move.w (%a1),%d0
m68k_01fbba_end:
.org 0x1FBBC
m68k_01fbbc:
        bsr.w (. + 24)
m68k_01fbbc_end:
.org 0x1FBC0
m68k_01fbc0:
        bsr.w (. + 458)
m68k_01fbc0_end:
.org 0x1FBC4
m68k_01fbc4:
        move.w #0x5,0xf362:w
m68k_01fbc4_end:
.org 0x1FBCA
m68k_01fbca:
        bra.w (. + 8)
m68k_01fbca_end:
.org 0x1FBCE
m68k_01fbce:
        addq.w #0x1,0xf362:w
m68k_01fbce_end:
.org 0x1FBD2
m68k_01fbd2:
        rts
m68k_01fbd2_end:
.org 0x1FBD4
m68k_01fbd4:
        cmp.w 0xf702:w,%d0
m68k_01fbd4_end:
.org 0x1FBD8
m68k_01fbd8:
        bne.w (. + 12)
m68k_01fbd8_end:
.org 0x1FBDC
m68k_01fbdc:
        move.w 0xf706:w,%d1
m68k_01fbdc_end:
.org 0x1FBE0
m68k_01fbe0:
        bra.w (. + 8)
m68k_01fbe0_end:
.org 0x1FBE4
m68k_01fbe4:
        move.w 0xf702:w,%d1
m68k_01fbe4_end:
.org 0x1FBE8
m68k_01fbe8:
        lea.l 0xa150:w,%a2
m68k_01fbe8_end:
.org 0x1FBEC
m68k_01fbec:
        move.w %d0,%d2
m68k_01fbec_end:
.org 0x1FBEE
m68k_01fbee:
        lsl.w #0x2,%d1
m68k_01fbee_end:
.org 0x1FBF0
m68k_01fbf0:
        lsl.w #0x2,%d2
m68k_01fbf0_end:
.org 0x1FBF2
m68k_01fbf2:
        clr.w %d3
m68k_01fbf2_end:
.org 0x1FBF4
m68k_01fbf4:
        move.w (%a2, %d2.w),%d4
m68k_01fbf4_end:
.org 0x1FBF8
m68k_01fbf8:
        sub.w (%a2, %d1.w),%d4
m68k_01fbf8_end:
.org 0x1FBFC
m68k_01fbfc:
        bcc.w (. + 10)
m68k_01fbfc_end:
.org 0x1FC00
m68k_01fc00:
        neg.w %d4
m68k_01fc00_end:
.org 0x1FC02
m68k_01fc02:
        bset.l #0x0,%d3
m68k_01fc02_end:
.org 0x1FC06
m68k_01fc06:
        subi.w #0x900,%d4
m68k_01fc06_end:
.org 0x1FC0A
m68k_01fc0a:
        bcc.w (. + 68)
m68k_01fc0a_end:
.org 0x1FC0E
m68k_01fc0e:
        move.w 0x2(%a2, %d2.w),%d5
m68k_01fc0e_end:
.org 0x1FC12
m68k_01fc12:
        sub.w 0x2(%a2, %d1.w),%d5
m68k_01fc12_end:
.org 0x1FC16
m68k_01fc16:
        bcc.w (. + 10)
m68k_01fc16_end:
.org 0x1FC1A
m68k_01fc1a:
        neg.w %d5
m68k_01fc1a_end:
.org 0x1FC1C
m68k_01fc1c:
        bset.l #0x1,%d3
m68k_01fc1c_end:
.org 0x1FC20
m68k_01fc20:
        subi.w #0x900,%d5
m68k_01fc20_end:
.org 0x1FC24
m68k_01fc24:
        bcc.w (. + 42)
m68k_01fc24_end:
.org 0x1FC28
m68k_01fc28:
        cmp.w %d4,%d5
m68k_01fc28_end:
.org 0x1FC2A
m68k_01fc2a:
        bhi.w (. + 22)
m68k_01fc2a_end:
.org 0x1FC2E
m68k_01fc2e:
        btst.l #0x0,%d3
m68k_01fc2e_end:
.org 0x1FC32
m68k_01fc32:
        bne.w (. + 6)
m68k_01fc32_end:
.org 0x1FC36
m68k_01fc36:
        neg.w %d4
m68k_01fc36_end:
.org 0x1FC38
m68k_01fc38:
        add.w %d4,(%a2, %d2.w)
m68k_01fc38_end:
.org 0x1FC3C
m68k_01fc3c:
        bra.w (. + 18)
m68k_01fc3c_end:
.org 0x1FC40
m68k_01fc40:
        btst.l #0x1,%d3
m68k_01fc40_end:
.org 0x1FC44
m68k_01fc44:
        bne.w (. + 6)
m68k_01fc44_end:
.org 0x1FC48
m68k_01fc48:
        neg.w %d5
m68k_01fc48_end:
.org 0x1FC4A
m68k_01fc4a:
        add.w %d5,0x2(%a2, %d2.w)
m68k_01fc4a_end:
.org 0x1FC4E
m68k_01fc4e:
        rts
m68k_01fc4e_end:
.org 0x1FC50
m68k_01fc50:
        lea.l 0xcc00:w,%a0
m68k_01fc50_end:
.org 0x1FC54
m68k_01fc54:
        move.w 0xf702:w,%d0
m68k_01fc54_end:
.org 0x1FC58
m68k_01fc58:
        cmpi.b #0xff,(%a0, %d0.w)
m68k_01fc58_end:
.org 0x1FC5E
m68k_01fc5e:
        beq.w (. + 26)
m68k_01fc5e_end:
.org 0x1FC62
m68k_01fc62:
        move.w 0xf706:w,%d0
m68k_01fc62_end:
.org 0x1FC66
m68k_01fc66:
        cmpi.b #0xff,(%a0, %d0.w)
m68k_01fc66_end:
.org 0x1FC6C
m68k_01fc6c:
        beq.w (. + 12)
m68k_01fc6c_end:
.org 0x1FC70
m68k_01fc70:
        andi.w #0xfffe,%sr
m68k_01fc70_end:
.org 0x1FC74
m68k_01fc74:
        bra.w (. + 8)
m68k_01fc74_end:
.org 0x1FC78
m68k_01fc78:
        ori.w #0x1,%sr
m68k_01fc78_end:
.org 0x1FC7C
m68k_01fc7c:
        rts
m68k_01fc7c_end:
.org 0x1FC7E
m68k_01fc7e:
        move.w (%a1),%d2
m68k_01fc7e_end:
.org 0x1FC80
m68k_01fc80:
        lea.l 0xa5a4:w,%a2
m68k_01fc80_end:
.org 0x1FC84
m68k_01fc84:
        btst.b #0x1,0xf6d7:w
m68k_01fc84_end:
.org 0x1FC8A
m68k_01fc8a:
        bne.w (. + 8)
m68k_01fc8a_end:
.org 0x1FC8E
m68k_01fc8e:
        lea.l 0xa550:w,%a2
m68k_01fc8e_end:
.org 0x1FC92
m68k_01fc92:
        move.w (%a2)+,%d3
m68k_01fc92_end:
.org 0x1FC94
m68k_01fc94:
        bmi.w (. + 16)
m68k_01fc94_end:
.org 0x1FC98
m68k_01fc98:
        cmp.w %d2,%d3
m68k_01fc98_end:
.org 0x1FC9A
m68k_01fc9a:
        bne.b (. + -8)
m68k_01fc9a_end:
.org 0x1FC9C
m68k_01fc9c:
        andi.w #0xfffe,%sr
m68k_01fc9c_end:
.org 0x1FCA0
m68k_01fca0:
        bra.w (. + 8)
m68k_01fca0_end:
.org 0x1FCA4
m68k_01fca4:
        ori.w #0x1,%sr
m68k_01fca4_end:
.org 0x1FCA8
m68k_01fca8:
        rts
m68k_01fca8_end:
.org 0x1FCAA
m68k_01fcaa:
        movem.l %d0-%d6/%a0-%a1,-(%a7)
m68k_01fcaa_end:
.org 0x1FCAE
m68k_01fcae:
        lea.l 0xa150:w,%a0
m68k_01fcae_end:
.org 0x1FCB2
m68k_01fcb2:
        move.w 0xf702:w,%d0
m68k_01fcb2_end:
.org 0x1FCB6
m68k_01fcb6:
        move.w 0xf706:w,%d1
m68k_01fcb6_end:
.org 0x1FCBA
m68k_01fcba:
        btst.b #0x1,0xf6d7:w
m68k_01fcba_end:
.org 0x1FCC0
m68k_01fcc0:
        beq.w (. + 6)
m68k_01fcc0_end:
.org 0x1FCC4
m68k_01fcc4:
        exg %d0,%d1
m68k_01fcc4_end:
.org 0x1FCC6
m68k_01fcc6:
        lsl.w #0x2,%d0
m68k_01fcc6_end:
.org 0x1FCC8
m68k_01fcc8:
        lsl.w #0x2,%d1
m68k_01fcc8_end:
.org 0x1FCCA
m68k_01fcca:
        move.w (%a0, %d0.w),%d2
m68k_01fcca_end:
.org 0x1FCCE
m68k_01fcce:
        sub.w (%a0, %d1.w),%d2
m68k_01fcce_end:
.org 0x1FCD2
m68k_01fcd2:
        bcs.w (. + 22)
m68k_01fcd2_end:
.org 0x1FCD6
m68k_01fcd6:
        move.w #0x800,%d3
m68k_01fcd6_end:
.org 0x1FCDA
m68k_01fcda:
        sub.w %d2,%d3
m68k_01fcda_end:
.org 0x1FCDC
m68k_01fcdc:
        bcc.w (. + 6)
m68k_01fcdc_end:
.org 0x1FCE0
m68k_01fce0:
        clr.w %d3
m68k_01fce0_end:
.org 0x1FCE2
m68k_01fce2:
        move.w %d3,%d5
m68k_01fce2_end:
.org 0x1FCE4
m68k_01fce4:
        bra.w (. + 20)
m68k_01fce4_end:
.org 0x1FCE8
m68k_01fce8:
        subi.w #0xf800,%d2
m68k_01fce8_end:
.org 0x1FCEC
m68k_01fcec:
        bcc.w (. + 6)
m68k_01fcec_end:
.org 0x1FCF0
m68k_01fcf0:
        clr.w %d2
m68k_01fcf0_end:
.org 0x1FCF2
m68k_01fcf2:
        move.w %d2,%d3
m68k_01fcf2_end:
.org 0x1FCF4
m68k_01fcf4:
        move.w %d2,%d5
m68k_01fcf4_end:
.org 0x1FCF6
m68k_01fcf6:
        neg.w %d5
m68k_01fcf6_end:
.org 0x1FCF8
m68k_01fcf8:
        move.w 0x2(%a0, %d0.w),%d2
m68k_01fcf8_end:
.org 0x1FCFC
m68k_01fcfc:
        sub.w 0x2(%a0, %d1.w),%d2
m68k_01fcfc_end:
.org 0x1FD00
m68k_01fd00:
        bcs.w (. + 22)
m68k_01fd00_end:
.org 0x1FD04
m68k_01fd04:
        move.w #0x800,%d4
m68k_01fd04_end:
.org 0x1FD08
m68k_01fd08:
        sub.w %d2,%d4
m68k_01fd08_end:
.org 0x1FD0A
m68k_01fd0a:
        bcc.w (. + 6)
m68k_01fd0a_end:
.org 0x1FD0E
m68k_01fd0e:
        clr.w %d4
m68k_01fd0e_end:
.org 0x1FD10
m68k_01fd10:
        move.w %d4,%d6
m68k_01fd10_end:
.org 0x1FD12
m68k_01fd12:
        bra.w (. + 22)
m68k_01fd12_end:
.org 0x1FD16
m68k_01fd16:
        subi.w #0xf800,%d2
m68k_01fd16_end:
.org 0x1FD1A
m68k_01fd1a:
        bcc.w (. + 8)
m68k_01fd1a_end:
.org 0x1FD1E
m68k_01fd1e:
        andi.w #0xfffe,%sr
m68k_01fd1e_end:
.org 0x1FD22
m68k_01fd22:
        move.w %d2,%d4
m68k_01fd22_end:
.org 0x1FD24
m68k_01fd24:
        move.w %d2,%d6
m68k_01fd24_end:
.org 0x1FD26
m68k_01fd26:
        neg.w %d6
m68k_01fd26_end:
.org 0x1FD28
m68k_01fd28:
        cmp.w %d3,%d4
m68k_01fd28_end:
.org 0x1FD2A
m68k_01fd2a:
        bcs.w (. + 20)
m68k_01fd2a_end:
.org 0x1FD2E
m68k_01fd2e:
        move.w (%a0, %d0.w),%d2
m68k_01fd2e_end:
.org 0x1FD32
m68k_01fd32:
        add.w %d5,%d2
m68k_01fd32_end:
.org 0x1FD34
m68k_01fd34:
        move.w %d2,%d3
m68k_01fd34_end:
.org 0x1FD36
m68k_01fd36:
        move.w 0x2(%a0, %d0.w),%d4
m68k_01fd36_end:
.org 0x1FD3A
m68k_01fd3a:
        bra.w (. + 16)
m68k_01fd3a_end:
.org 0x1FD3E
m68k_01fd3e:
        move.w (%a0, %d0.w),%d3
m68k_01fd3e_end:
.org 0x1FD42
m68k_01fd42:
        move.w 0x2(%a0, %d0.w),%d2
m68k_01fd42_end:
.org 0x1FD46
m68k_01fd46:
        add.w %d6,%d2
m68k_01fd46_end:
.org 0x1FD48
m68k_01fd48:
        move.w %d2,%d4
m68k_01fd48_end:
.org 0x1FD4A
m68k_01fd4a:
        lea.l 0xae1b2:l,%a1
m68k_01fd4a_end:
.org 0x1FD50
m68k_01fd50:
        move.w 0xf68a:w,%d2
m68k_01fd50_end:
.org 0x1FD54
m68k_01fd54:
        lsl.w #0x3,%d2
m68k_01fd54_end:
.org 0x1FD56
m68k_01fd56:
        cmp.w (%a1, %d2.w),%d3
m68k_01fd56_end:
.org 0x1FD5A
m68k_01fd5a:
        bls.w (. + 34)
m68k_01fd5a_end:
.org 0x1FD5E
m68k_01fd5e:
        cmp.w 0x2(%a1, %d2.w),%d3
m68k_01fd5e_end:
.org 0x1FD62
m68k_01fd62:
        bcc.w (. + 26)
m68k_01fd62_end:
.org 0x1FD66
m68k_01fd66:
        cmp.w 0x4(%a1, %d2.w),%d4
m68k_01fd66_end:
.org 0x1FD6A
m68k_01fd6a:
        bls.w (. + 18)
m68k_01fd6a_end:
.org 0x1FD6E
m68k_01fd6e:
        cmp.w 0x6(%a1, %d2.w),%d4
m68k_01fd6e_end:
.org 0x1FD72
m68k_01fd72:
        bcc.w (. + 10)
m68k_01fd72_end:
.org 0x1FD76
m68k_01fd76:
        exg %d0,%d1
m68k_01fd76_end:
.org 0x1FD78
m68k_01fd78:
        bra.w (. + -174)
m68k_01fd78_end:
.org 0x1FD7C
m68k_01fd7c:
        move.w %d3,(%a0, %d0.w)
m68k_01fd7c_end:
.org 0x1FD80
m68k_01fd80:
        move.w %d4,0x2(%a0, %d0.w)
m68k_01fd80_end:
.org 0x1FD84
m68k_01fd84:
        movem.l (%a7)+,%d0-%d6/%a0-%a1
m68k_01fd84_end:
.org 0x1FD88
m68k_01fd88:
        rts
m68k_01fd88_end:
.org 0x1FD8A
m68k_01fd8a:
        move.w %d0,%d1
m68k_01fd8a_end:
.org 0x1FD8C
m68k_01fd8c:
        lsl.w #0x2,%d1
m68k_01fd8c_end:
.org 0x1FD8E
m68k_01fd8e:
        lea.l 0xa150:w,%a2
m68k_01fd8e_end:
.org 0x1FD92
m68k_01fd92:
        move.w (%a2, %d1.w),%d2
m68k_01fd92_end:
.org 0x1FD96
m68k_01fd96:
        move.w 0x2(%a2, %d1.w),%d3
m68k_01fd96_end:
.org 0x1FD9A
m68k_01fd9a:
        lea.l 0xa960:w,%a2
m68k_01fd9a_end:
.org 0x1FD9E
m68k_01fd9e:
        lea.l 0xff2c00:l,%a3
m68k_01fd9e_end:
.org 0x1FDA4
m68k_01fda4:
        move.w (%a2, %d1.w),%d4
m68k_01fda4_end:
.org 0x1FDA8
m68k_01fda8:
        or.w 0x2(%a2, %d1.w),%d4
m68k_01fda8_end:
.org 0x1FDAC
m68k_01fdac:
        beq.w (. + 128)
m68k_01fdac_end:
.org 0x1FDB0
m68k_01fdb0:
        move.w (%a2, %d1.w),%d4
m68k_01fdb0_end:
.org 0x1FDB4
m68k_01fdb4:
        neg.w %d4
m68k_01fdb4_end:
.org 0x1FDB6
m68k_01fdb6:
        muls.w #0x4b0,%d4
m68k_01fdb6_end:
.org 0x1FDBA
m68k_01fdba:
        bmi.w (. + 26)
m68k_01fdba_end:
.org 0x1FDBE
m68k_01fdbe:
        add.w %d4,%d2
m68k_01fdbe_end:
.org 0x1FDC0
m68k_01fdc0:
        bcs.w (. + 12)
m68k_01fdc0_end:
.org 0x1FDC4
m68k_01fdc4:
        cmpi.w #0x6400,%d2
m68k_01fdc4_end:
.org 0x1FDC8
m68k_01fdc8:
        bls.w (. + 30)
m68k_01fdc8_end:
.org 0x1FDCC
m68k_01fdcc:
        move.w #0x6400,%d2
m68k_01fdcc_end:
.org 0x1FDD0
m68k_01fdd0:
        bra.w (. + 22)
m68k_01fdd0_end:
.org 0x1FDD4
m68k_01fdd4:
        add.w %d4,%d2
m68k_01fdd4_end:
.org 0x1FDD6
m68k_01fdd6:
        bcc.w (. + 12)
m68k_01fdd6_end:
.org 0x1FDDA
m68k_01fdda:
        cmpi.w #0xc00,%d2
m68k_01fdda_end:
.org 0x1FDDE
m68k_01fdde:
        bcc.w (. + 8)
m68k_01fdde_end:
.org 0x1FDE2
m68k_01fde2:
        move.w #0xc00,%d2
m68k_01fde2_end:
.org 0x1FDE6
m68k_01fde6:
        lsr.w #0x7,%d2
m68k_01fde6_end:
.org 0x1FDE8
m68k_01fde8:
        move.w %d2,(%a3, %d1.w)
m68k_01fde8_end:
.org 0x1FDEC
m68k_01fdec:
        move.w 0x2(%a2, %d1.w),%d4
m68k_01fdec_end:
.org 0x1FDF0
m68k_01fdf0:
        neg.w %d4
m68k_01fdf0_end:
.org 0x1FDF2
m68k_01fdf2:
        muls.w #0x4b0,%d4
m68k_01fdf2_end:
.org 0x1FDF6
m68k_01fdf6:
        bmi.w (. + 26)
m68k_01fdf6_end:
.org 0x1FDFA
m68k_01fdfa:
        add.w %d4,%d3
m68k_01fdfa_end:
.org 0x1FDFC
m68k_01fdfc:
        bcs.w (. + 12)
m68k_01fdfc_end:
.org 0x1FE00
m68k_01fe00:
        cmpi.w #0x9400,%d3
m68k_01fe00_end:
.org 0x1FE04
m68k_01fe04:
        bls.w (. + 30)
m68k_01fe04_end:
.org 0x1FE08
m68k_01fe08:
        move.w #0x9400,%d3
m68k_01fe08_end:
.org 0x1FE0C
m68k_01fe0c:
        bra.w (. + 22)
m68k_01fe0c_end:
.org 0x1FE10
m68k_01fe10:
        add.w %d4,%d3
m68k_01fe10_end:
.org 0x1FE12
m68k_01fe12:
        bcc.w (. + 12)
m68k_01fe12_end:
.org 0x1FE16
m68k_01fe16:
        cmpi.w #0xc00,%d3
m68k_01fe16_end:
.org 0x1FE1A
m68k_01fe1a:
        bcc.w (. + 8)
m68k_01fe1a_end:
.org 0x1FE1E
m68k_01fe1e:
        move.w #0xc00,%d3
m68k_01fe1e_end:
.org 0x1FE22
m68k_01fe22:
        lsr.w #0x7,%d3
m68k_01fe22_end:
.org 0x1FE24
m68k_01fe24:
        move.w %d3,0x2(%a3, %d1.w)
m68k_01fe24_end:
.org 0x1FE28
m68k_01fe28:
        bra.w (. + 146)
m68k_01fe28_end:
.org 0x1FE2C
m68k_01fe2c:
        cmp.w 0xf702:w,%d0
m68k_01fe2c_end:
.org 0x1FE30
m68k_01fe30:
        beq.w (. + 12)
m68k_01fe30_end:
.org 0x1FE34
m68k_01fe34:
        move.w 0xf702:w,%d4
m68k_01fe34_end:
.org 0x1FE38
m68k_01fe38:
        bra.w (. + 8)
m68k_01fe38_end:
.org 0x1FE3C
m68k_01fe3c:
        move.w 0xf706:w,%d4
m68k_01fe3c_end:
.org 0x1FE40
m68k_01fe40:
        lea.l 0xa150:w,%a4
m68k_01fe40_end:
.org 0x1FE44
m68k_01fe44:
        lsl.w #0x2,%d4
m68k_01fe44_end:
.org 0x1FE46
m68k_01fe46:
        cmp.w (%a4, %d4.w),%d2
m68k_01fe46_end:
.org 0x1FE4A
m68k_01fe4a:
        bhi.w (. + 28)
m68k_01fe4a_end:
.org 0x1FE4E
m68k_01fe4e:
        subi.w #0x20d0,%d2
m68k_01fe4e_end:
.org 0x1FE52
m68k_01fe52:
        bcs.w (. + 12)
m68k_01fe52_end:
.org 0x1FE56
m68k_01fe56:
        cmpi.w #0xc00,%d2
m68k_01fe56_end:
.org 0x1FE5A
m68k_01fe5a:
        bhi.w (. + 32)
m68k_01fe5a_end:
.org 0x1FE5E
m68k_01fe5e:
        move.w #0xc00,%d2
m68k_01fe5e_end:
.org 0x1FE62
m68k_01fe62:
        bra.w (. + 24)
m68k_01fe62_end:
.org 0x1FE66
m68k_01fe66:
        addi.w #0x20d0,%d2
m68k_01fe66_end:
.org 0x1FE6A
m68k_01fe6a:
        bcs.w (. + 12)
m68k_01fe6a_end:
.org 0x1FE6E
m68k_01fe6e:
        cmpi.w #0x6400,%d2
m68k_01fe6e_end:
.org 0x1FE72
m68k_01fe72:
        bcs.w (. + 8)
m68k_01fe72_end:
.org 0x1FE76
m68k_01fe76:
        move.w #0x6400,%d2
m68k_01fe76_end:
.org 0x1FE7A
m68k_01fe7a:
        lsr.w #0x7,%d2
m68k_01fe7a_end:
.org 0x1FE7C
m68k_01fe7c:
        move.w %d2,(%a3, %d1.w)
m68k_01fe7c_end:
.org 0x1FE80
m68k_01fe80:
        cmp.w 0x2(%a4, %d4.w),%d3
m68k_01fe80_end:
.org 0x1FE84
m68k_01fe84:
        bhi.w (. + 28)
m68k_01fe84_end:
.org 0x1FE88
m68k_01fe88:
        subi.w #0x20d0,%d3
m68k_01fe88_end:
.org 0x1FE8C
m68k_01fe8c:
        bcs.w (. + 12)
m68k_01fe8c_end:
.org 0x1FE90
m68k_01fe90:
        cmpi.w #0xc00,%d3
m68k_01fe90_end:
.org 0x1FE94
m68k_01fe94:
        bcc.w (. + 32)
m68k_01fe94_end:
.org 0x1FE98
m68k_01fe98:
        move.w #0xc00,%d3
m68k_01fe98_end:
.org 0x1FE9C
m68k_01fe9c:
        bra.w (. + 24)
m68k_01fe9c_end:
.org 0x1FEA0
m68k_01fea0:
        addi.w #0x20d0,%d3
m68k_01fea0_end:
.org 0x1FEA4
m68k_01fea4:
        bcs.w (. + 12)
m68k_01fea4_end:
.org 0x1FEA8
m68k_01fea8:
        cmpi.w #0x9400,%d3
m68k_01fea8_end:
.org 0x1FEAC
m68k_01feac:
        bls.w (. + 8)
m68k_01feac_end:
.org 0x1FEB0
m68k_01feb0:
        move.w #0x9400,%d3
m68k_01feb0_end:
.org 0x1FEB4
m68k_01feb4:
        lsr.w #0x7,%d3
m68k_01feb4_end:
.org 0x1FEB6
m68k_01feb6:
        move.w %d3,0x2(%a3, %d1.w)
m68k_01feb6_end:
.org 0x1FEBA
m68k_01feba:
        lea.l 0xff3dc2:l,%a2
m68k_01feba_end:
.org 0x1FEC0
m68k_01fec0:
        move.b #0x2,(%a2, %d0.w)
m68k_01fec0_end:
.org 0x1FEC6
m68k_01fec6:
        lea.l 0xae28:w,%a2
m68k_01fec6_end:
.org 0x1FECA
m68k_01feca:
        move.b #0x1,(%a2, %d0.w)
m68k_01feca_end:
.org 0x1FED0
m68k_01fed0:
        move.w %d0,%d7
m68k_01fed0_end:
.org 0x1FED2
m68k_01fed2:
        jsr 0x1dcaa:l
m68k_01fed2_end:
.org 0x1FED8
m68k_01fed8:
        rts
m68k_01fed8_end:
.org 0x1FEDA
m68k_01feda:
        move.w 0xf702:w,%d0
m68k_01feda_end:
.org 0x1FEDE
m68k_01fede:
        btst.b #0x1,0xf6d7:w
m68k_01fede_end:
.org 0x1FEE4
m68k_01fee4:
        beq.b (. + 6)
m68k_01fee4_end:
.org 0x1FEE6
m68k_01fee6:
        move.w 0xf706:w,%d0
m68k_01fee6_end:
.org 0x1FEEA
m68k_01feea:
        move.w %d0,0xf3a6:w
m68k_01feea_end:
.org 0x1FEEE
m68k_01feee:
        move.w %d0,0xa5f8:w
m68k_01feee_end:
.org 0x1FEF2
m68k_01fef2:
        move.w #0xffff,0xa5fa:w
m68k_01fef2_end:
.org 0x1FEF8
m68k_01fef8:
        lea.l 0xa150:w,%a0
m68k_01fef8_end:
.org 0x1FEFC
m68k_01fefc:
        lsl.w #0x2,%d0
m68k_01fefc_end:
.org 0x1FEFE
m68k_01fefe:
        move.w (%a0, %d0.w),%d1
m68k_01fefe_end:
.org 0x1FF02
m68k_01ff02:
        lsr.w #0x7,%d1
m68k_01ff02_end:
.org 0x1FF04
m68k_01ff04:
        subi.w #0x8,%d1
m68k_01ff04_end:
.org 0x1FF08
m68k_01ff08:
        move.w %d1,0xf35e:w
m68k_01ff08_end:
.org 0x1FF0C
m68k_01ff0c:
        move.w 0x2(%a0, %d0.w),%d1
m68k_01ff0c_end:
.org 0x1FF10
m68k_01ff10:
        lsr.w #0x7,%d1
m68k_01ff10_end:
.org 0x1FF12
m68k_01ff12:
        subi.w #0x8,%d1
m68k_01ff12_end:
.org 0x1FF16
m68k_01ff16:
        move.w %d1,0xf360:w
m68k_01ff16_end:
.org 0x1FF1A
m68k_01ff1a:
        addq.w #0x1,0xf362:w
m68k_01ff1a_end:
.org 0x1FF1E
m68k_01ff1e:
        move.w 0xf3a6:w,0xf3d0:w
m68k_01ff1e_end:
.org 0x1FF24
m68k_01ff24:
        move.w #0x118,%d0
m68k_01ff24_end:
.org 0x1FF28
m68k_01ff28:
        move.w %d0,0xaf80:w
m68k_01ff28_end:
.org 0x1FF2C
m68k_01ff2c:
        jsr 0x676f2:l
m68k_01ff2c_end:
.org 0x1FF32
m68k_01ff32:
        move.w #0x1,0xf652:w
m68k_01ff32_end:
.org 0x1FF38
m68k_01ff38:
        rts
m68k_01ff38_end:
.org 0x1FF3A
m68k_01ff3a:
        move.b 0xf602:w,%d0
m68k_01ff3a_end:
.org 0x1FF3E
m68k_01ff3e:
        andi.w #0x2f,%d0
m68k_01ff3e_end:
.org 0x1FF42
m68k_01ff42:
        beq.b (. + 28)
m68k_01ff42_end:
.org 0x1FF44
m68k_01ff44:
        move.w 0xf612:w,0xf3c2:w
m68k_01ff44_end:
.org 0x1FF4A
m68k_01ff4a:
        move.w #0x4,0xf3c4:w
m68k_01ff4a_end:
.org 0x1FF50
m68k_01ff50:
        move.w #0x404,0xf612:w
m68k_01ff50_end:
.org 0x1FF56
m68k_01ff56:
        clr.w 0xf362:w
m68k_01ff56_end:
.org 0x1FF5A
m68k_01ff5a:
        clr.w 0xf36a:w
m68k_01ff5a_end:
.org 0x1FF5E
m68k_01ff5e:
        rts
m68k_01ff5e_end:
.org 0x1FF60
m68k_01ff60:
        bsr.w (. + -5120)
m68k_01ff60_end:
.org 0x1FF64
m68k_01ff64:
        bsr.w (. + -4974)
m68k_01ff64_end:
.org 0x1FF68
m68k_01ff68:
        btst.b #0x5,0xf603:w
m68k_01ff68_end:
.org 0x1FF6E
m68k_01ff6e:
        beq.w (. + 32)
m68k_01ff6e_end:
.org 0x1FF72
m68k_01ff72:
        move.w #0xffff,0xa5f8:w
m68k_01ff72_end:
.org 0x1FF78
m68k_01ff78:
        bsr.w (. + -9300)
m68k_01ff78_end:
.org 0x1FF7C
m68k_01ff7c:
        lea.l 0xae28:w,%a0
m68k_01ff7c_end:
.org 0x1FF80
m68k_01ff80:
        move.w 0xf3a6:w,%d0
m68k_01ff80_end:
.org 0x1FF84
m68k_01ff84:
        move.b #0x1,(%a0, %d0.w)
m68k_01ff84_end:
.org 0x1FF8A
m68k_01ff8a:
        addq.w #0x1,0xf362:w
m68k_01ff8a_end:
.org 0x1FF8E
m68k_01ff8e:
        rts
m68k_01ff8e_end:
.org 0x1FF90
m68k_01ff90:
        bsr.w (. + 32)
m68k_01ff90_end:
.org 0x1FF94
m68k_01ff94:
        move.w #0x407,0xf3c2:w
m68k_01ff94_end:
.org 0x1FF9A
m68k_01ff9a:
        move.w #0x1,0xf3c4:w
m68k_01ff9a_end:
.org 0x1FFA0
m68k_01ffa0:
        move.w #0x404,0xf612:w
m68k_01ffa0_end:
.org 0x1FFA6
m68k_01ffa6:
        clr.w 0xf362:w
m68k_01ffa6_end:
.org 0x1FFAA
m68k_01ffaa:
        clr.w 0xf36a:w
m68k_01ffaa_end:
.org 0x1FFAE
m68k_01ffae:
        rts
m68k_01ffae_end:
.org 0x1FFB0
m68k_01ffb0:
        move.w 0xf702:w,%d0
m68k_01ffb0_end:
.org 0x1FFB4
m68k_01ffb4:
        bsr.w (. + 14)
m68k_01ffb4_end:
.org 0x1FFB8
m68k_01ffb8:
        move.w 0xf706:w,%d0
m68k_01ffb8_end:
.org 0x1FFBC
m68k_01ffbc:
        bsr.w (. + 36)
m68k_01ffbc_end:
.org 0x1FFC0
m68k_01ffc0:
        rts
m68k_01ffc0_end:
.org 0x1FFC2
m68k_01ffc2:
        lea.l 0xad60:w,%a0
m68k_01ffc2_end:
.org 0x1FFC6
m68k_01ffc6:
        move.w (%a0)+,%d1
m68k_01ffc6_end:
.org 0x1FFC8
m68k_01ffc8:
        beq.b (. + -2)
m68k_01ffc8_end:
.org 0x1FFCA
m68k_01ffca:
        cmpi.w #0xffff,%d1
m68k_01ffca_end:
.org 0x1FFCE
m68k_01ffce:
        beq.w (. + 16)
m68k_01ffce_end:
.org 0x1FFD2
m68k_01ffd2:
        lsr.w #0x8,%d1
m68k_01ffd2_end:
.org 0x1FFD4
m68k_01ffd4:
        cmp.w %d0,%d1
m68k_01ffd4_end:
.org 0x1FFD6
m68k_01ffd6:
        bne.b (. + -16)
m68k_01ffd6_end:
.org 0x1FFD8
m68k_01ffd8:
        clr.w -0x2(%a0)
m68k_01ffd8_end:
.org 0x1FFDC
m68k_01ffdc:
        bra.b (. + -22)
m68k_01ffdc_end:
.org 0x1FFDE
m68k_01ffde:
        rts
m68k_01ffde_end:
.org 0x1FFE0
m68k_01ffe0:
        lea.l 0xad60:w,%a0
m68k_01ffe0_end:
.org 0x1FFE4
m68k_01ffe4:
        move.w (%a0)+,%d1
m68k_01ffe4_end:
.org 0x1FFE6
m68k_01ffe6:
        beq.b (. + -2)
m68k_01ffe6_end:
.org 0x1FFE8
m68k_01ffe8:
        cmpi.w #0xffff,%d1
m68k_01ffe8_end:
.org 0x1FFEC
m68k_01ffec:
        beq.w (. + 18)
m68k_01ffec_end:
.org 0x1FFF0
m68k_01fff0:
        andi.w #0xff,%d1
m68k_01fff0_end:
.org 0x1FFF4
m68k_01fff4:
        cmp.w %d0,%d1
m68k_01fff4_end:
.org 0x1FFF6
m68k_01fff6:
        bne.b (. + -18)
m68k_01fff6_end:
.org 0x1FFF8
m68k_01fff8:
        clr.w -0x2(%a0)
m68k_01fff8_end:
.org 0x1FFFC
m68k_01fffc:
        bra.b (. + -24)
m68k_01fffc_end:
.org 0x1FFFE
m68k_01fffe:
        rts
m68k_01fffe_end:
.org 0x20014
m68k_020014:
        lea.l 0xa5f8:w,%a0
m68k_020014_end:
.org 0x20018
m68k_020018:
        lea.l 0xa550:w,%a1
m68k_020018_end:
.org 0x2001C
m68k_02001c:
        move.w (%a1)+,%d0
m68k_02001c_end:
.org 0x2001E
m68k_02001e:
        bmi.w (. + 8)
m68k_02001e_end:
.org 0x20022
m68k_020022:
        move.w %d0,(%a0)+
m68k_020022_end:
.org 0x20024
m68k_020024:
        bra.b (. + -8)
m68k_020024_end:
.org 0x20026
m68k_020026:
        lea.l 0xa5a4:w,%a1
m68k_020026_end:
.org 0x2002A
m68k_02002a:
        move.w (%a1)+,(%a0)+
m68k_02002a_end:
.org 0x2002C
m68k_02002c:
        bpl.b (. + -2)
m68k_02002c_end:
.org 0x2002E
m68k_02002e:
        move.w 0xf612:w,0xf38a:w
m68k_02002e_end:
.org 0x20034
m68k_020034:
        move.w #0x1,0xf3b0:w
m68k_020034_end:
.org 0x2003A
m68k_02003a:
        move.w #0x40a,0xf612:w
m68k_02003a_end:
.org 0x20040
m68k_020040:
        move.w #0x2,0xf362:w
m68k_020040_end:
.org 0x20046
m68k_020046:
        rts
m68k_020046_end:
.org 0x20048
m68k_020048:
        tst.w 0xf3a6:w
m68k_020048_end:
.org 0x2004C
m68k_02004c:
        bmi.w (. + 56)
m68k_02004c_end:
.org 0x20050
m68k_020050:
        move.w 0xf3a6:w,0xf500:w
m68k_020050_end:
.org 0x20056
m68k_020056:
        move.w 0xf3a6:w,0xf372:w
m68k_020056_end:
.org 0x2005C
m68k_02005c:
        move.w #0xffff,0xf502:w
m68k_02005c_end:
.org 0x20062
m68k_020062:
        move.w #0x1,0xf636:w
m68k_020062_end:
.org 0x20068
m68k_020068:
        move.w #0x4,0xf6d2:w
m68k_020068_end:
.org 0x2006E
m68k_02006e:
        move.w #0x207,0xf612:w
m68k_02006e_end:
.org 0x20074
m68k_020074:
        clr.w 0xf362:w
m68k_020074_end:
.org 0x20078
m68k_020078:
        clr.w 0xf352:w
m68k_020078_end:
.org 0x2007C
m68k_02007c:
        clr.w 0xf378:w
m68k_02007c_end:
.org 0x20080
m68k_020080:
        bra.w (. + 6)
m68k_020080_end:
.org 0x20084
m68k_020084:
        bra.b (. + -112)
m68k_020084_end:
.org 0x20086
m68k_020086:
        rts
m68k_020086_end:
.org 0x2025A
m68k_02025a:
        bsr.w (. + 394)
m68k_02025a_end:
.org 0x2025E
m68k_02025e:
        bsr.w (. + 460)
m68k_02025e_end:
.org 0x20262
m68k_020262:
        move.w 0xf68c:w,%d0
m68k_020262_end:
.org 0x20266
m68k_020266:
        btst.b #0x1,0xf6d7:w
m68k_020266_end:
.org 0x2026C
m68k_02026c:
        beq.w (. + 8)
m68k_02026c_end:
.org 0x20270
m68k_020270:
        move.w 0xf68e:w,%d0
m68k_020270_end:
.org 0x20274
m68k_020274:
        cmp.w 0xf67a:w,%d0
m68k_020274_end:
.org 0x20278
m68k_020278:
        beq.w (. + 34)
m68k_020278_end:
.org 0x2027C
m68k_02027c:
        cmp.w 0xf67c:w,%d0
m68k_02027c_end:
.org 0x20280
m68k_020280:
        beq.w (. + 26)
m68k_020280_end:
.org 0x20284
m68k_020284:
        cmp.w 0xf67e:w,%d0
m68k_020284_end:
.org 0x20288
m68k_020288:
        beq.w (. + 18)
m68k_020288_end:
.org 0x2028C
m68k_02028c:
        move.w #0x87,%d0
m68k_02028c_end:
.org 0x20290
m68k_020290:
        jsr 0x808a:l
m68k_020290_end:
.org 0x20296
m68k_020296:
        bra.w (. + 98)
m68k_020296_end:
.org 0x2029A
m68k_02029a:
        move.w #0x89,%d0
m68k_02029a_end:
.org 0x2029E
m68k_02029e:
        jsr 0x808a:l
m68k_02029e_end:
.org 0x202A4
m68k_0202a4:
        move.w #0xffff,0xaf28:w
m68k_0202a4_end:
.org 0x202AA
m68k_0202aa:
        move.w #0xffff,0xef80:w
m68k_0202aa_end:
.org 0x202B0
m68k_0202b0:
        bsr.w (. + 84)
m68k_0202b0_end:
.org 0x202B4
m68k_0202b4:
        tst.w 0xf500:w
m68k_0202b4_end:
.org 0x202B8
m68k_0202b8:
        bmi.b (. + 54)
m68k_0202b8_end:
.org 0x202BA
m68k_0202ba:
        move.w #0x1,0xf3b0:w
m68k_0202ba_end:
.org 0x202C0
m68k_0202c0:
        move.w 0xf612:w,0xf38a:w
m68k_0202c0_end:
.org 0x202C6
m68k_0202c6:
        move.w #0x405,0xf612:w
m68k_0202c6_end:
.org 0x202CC
m68k_0202cc:
        clr.w 0xf362:w
m68k_0202cc_end:
.org 0x202D0
m68k_0202d0:
        clr.w 0xf378:w
m68k_0202d0_end:
.org 0x202D4
m68k_0202d4:
        clr.w 0xf658:w
m68k_0202d4_end:
.org 0x202D8
m68k_0202d8:
        clr.w 0xf6d2:w
m68k_0202d8_end:
.org 0x202DC
m68k_0202dc:
        move.w #0x11c,%d0
m68k_0202dc_end:
.org 0x202E0
m68k_0202e0:
        move.w %d0,0xaf80:w
m68k_0202e0_end:
.org 0x202E4
m68k_0202e4:
        jsr 0x676f2:l
m68k_0202e4_end:
.org 0x202EA
m68k_0202ea:
        bra.w (. + 24)
m68k_0202ea_end:
.org 0x202EE
m68k_0202ee:
        move.w #0xe,0xf362:w
m68k_0202ee_end:
.org 0x202F4
m68k_0202f4:
        bra.w (. + 14)
m68k_0202f4_end:
.org 0x202F8
m68k_0202f8:
        bsr.w (. + 98)
m68k_0202f8_end:
.org 0x202FC
m68k_0202fc:
        move.w #0x5,0xf362:w
m68k_0202fc_end:
.org 0x20302
m68k_020302:
        rts
m68k_020302_end:
.org 0x20304
m68k_020304:
        lea.l 0xf500:w,%a0
m68k_020304_end:
.org 0x20308
m68k_020308:
        clr.w %d1
m68k_020308_end:
.org 0x2030A
m68k_02030a:
        btst.b #0x1,0xf6d7:w
m68k_02030a_end:
.org 0x20310
m68k_020310:
        bne.b (. + 14)
m68k_020310_end:
.org 0x20312
m68k_020312:
        lea.l 0xa5a4:w,%a1
m68k_020312_end:
.org 0x20316
m68k_020316:
        lea.l 0xa57a:w,%a2
m68k_020316_end:
.org 0x2031A
m68k_02031a:
        bra.w (. + 12)
m68k_02031a_end:
.org 0x2031E
m68k_02031e:
        lea.l 0xa550:w,%a1
m68k_02031e_end:
.org 0x20322
m68k_020322:
        lea.l 0xa5ce:w,%a2
m68k_020322_end:
.org 0x20326
m68k_020326:
        move.w (%a1)+,%d0
m68k_020326_end:
.org 0x20328
m68k_020328:
        bmi.b (. + 12)
m68k_020328_end:
.org 0x2032A
m68k_02032a:
        andi.w #0xff,%d0
m68k_02032a_end:
.org 0x2032E
m68k_02032e:
        move.w %d0,(%a0)+
m68k_02032e_end:
.org 0x20330
m68k_020330:
        addq.w #0x1,%d1
m68k_020330_end:
.org 0x20332
m68k_020332:
        bra.b (. + -12)
m68k_020332_end:
.org 0x20334
m68k_020334:
        cmpi.w #0xa,%d1
m68k_020334_end:
.org 0x20338
m68k_020338:
        bcc.w (. + 24)
m68k_020338_end:
.org 0x2033C
m68k_02033c:
        move.w (%a2)+,%d0
m68k_02033c_end:
.org 0x2033E
m68k_02033e:
        bmi.w (. + 18)
m68k_02033e_end:
.org 0x20342
m68k_020342:
        andi.w #0xff,%d0
m68k_020342_end:
.org 0x20346
m68k_020346:
        move.w %d0,(%a0)+
m68k_020346_end:
.org 0x20348
m68k_020348:
        addq.w #0x1,%d1
m68k_020348_end:
.org 0x2034A
m68k_02034a:
        cmpi.w #0xa,%d1
m68k_02034a_end:
.org 0x2034E
m68k_02034e:
        bcs.b (. + -18)
m68k_02034e_end:
.org 0x20350
m68k_020350:
        move.w %d1,0xf636:w
m68k_020350_end:
.org 0x20354
m68k_020354:
        move.w #0xffff,(%a0)
m68k_020354_end:
.org 0x20358
m68k_020358:
        rts
m68k_020358_end:
.org 0x2035A
m68k_02035a:
        lea.l 0xaf28:w,%a0
m68k_02035a_end:
.org 0x2035E
m68k_02035e:
        lea.l 0xa5a4:w,%a1
m68k_02035e_end:
.org 0x20362
m68k_020362:
        lea.l 0xa57a:w,%a2
m68k_020362_end:
.org 0x20366
m68k_020366:
        move.w 0xf68c:w,%d0
m68k_020366_end:
.org 0x2036A
m68k_02036a:
        move.w 0xf68e:w,%d1
m68k_02036a_end:
.org 0x2036E
m68k_02036e:
        btst.b #0x1,0xf6d7:w
m68k_02036e_end:
.org 0x20374
m68k_020374:
        beq.w (. + 14)
m68k_020374_end:
.org 0x20378
m68k_020378:
        lea.l 0xa550:w,%a1
m68k_020378_end:
.org 0x2037C
m68k_02037c:
        lea.l 0xa5ce:w,%a2
m68k_02037c_end:
.org 0x20380
m68k_020380:
        exg %d0,%d1
m68k_020380_end:
.org 0x20382
m68k_020382:
        lea.l 0xe640:w,%a3
m68k_020382_end:
.org 0x20386
m68k_020386:
        lsl.w #0x1,%d0
m68k_020386_end:
.org 0x20388
m68k_020388:
        move.w (%a3, %d0.w),0xf3f2:w
m68k_020388_end:
.org 0x2038E
m68k_02038e:
        lsl.w #0x1,%d1
m68k_02038e_end:
.org 0x20390
m68k_020390:
        move.w (%a3, %d1.w),%d1
m68k_020390_end:
.org 0x20394
m68k_020394:
        movea.l %a1,%a3
m68k_020394_end:
.org 0x20396
m68k_020396:
        movea.l %a2,%a4
m68k_020396_end:
.org 0x20398
m68k_020398:
        move.w (%a1)+,%d0
m68k_020398_end:
.org 0x2039A
m68k_02039a:
        bmi.w (. + 38)
m68k_02039a_end:
.org 0x2039E
m68k_02039e:
        andi.w #0xff,%d0
m68k_02039e_end:
.org 0x203A2
m68k_0203a2:
        cmp.w %d1,%d0
m68k_0203a2_end:
.org 0x203A4
m68k_0203a4:
        beq.w (. + 16)
m68k_0203a4_end:
.org 0x203A8
m68k_0203a8:
        move.w %d0,0xf3a6:w
m68k_0203a8_end:
.org 0x203AC
m68k_0203ac:
        move.w %d0,(%a0)+
m68k_0203ac_end:
.org 0x203AE
m68k_0203ae:
        bsr.w (. + 1312)
m68k_0203ae_end:
.org 0x203B2
m68k_0203b2:
        bra.b (. + -26)
m68k_0203b2_end:
.org 0x203B4
m68k_0203b4:
        lea.l 0xcc00:w,%a5
m68k_0203b4_end:
.org 0x203B8
m68k_0203b8:
        move.b #0xff,(%a5, %d1.w)
m68k_0203b8_end:
.org 0x203BE
m68k_0203be:
        bra.b (. + -38)
m68k_0203be_end:
.org 0x203C0
m68k_0203c0:
        move.w (%a2)+,%d0
m68k_0203c0_end:
.org 0x203C2
m68k_0203c2:
        bmi.w (. + 20)
m68k_0203c2_end:
.org 0x203C6
m68k_0203c6:
        andi.w #0xff,%d0
m68k_0203c6_end:
.org 0x203CA
m68k_0203ca:
        move.w %d0,(%a0)+
m68k_0203ca_end:
.org 0x203CC
m68k_0203cc:
        move.w %d0,0xf3a6:w
m68k_0203cc_end:
.org 0x203D0
m68k_0203d0:
        bsr.w (. + 1278)
m68k_0203d0_end:
.org 0x203D4
m68k_0203d4:
        bra.b (. + -20)
m68k_0203d4_end:
.org 0x203D6
m68k_0203d6:
        move.w #0xffff,(%a0)
m68k_0203d6_end:
.org 0x203DA
m68k_0203da:
        move.w #0xffff,(%a3)
m68k_0203da_end:
.org 0x203DE
m68k_0203de:
        move.w #0xffff,(%a4)
m68k_0203de_end:
.org 0x203E2
m68k_0203e2:
        rts
m68k_0203e2_end:
.org 0x203E4
m68k_0203e4:
        lea.l 0xcc00:w,%a0
m68k_0203e4_end:
.org 0x203E8
m68k_0203e8:
        lea.l 0xa150:w,%a3
m68k_0203e8_end:
.org 0x203EC
m68k_0203ec:
        move.w 0xf68a:w,%d0
m68k_0203ec_end:
.org 0x203F0
m68k_0203f0:
        lea.l 0xa550:w,%a1
m68k_0203f0_end:
.org 0x203F4
m68k_0203f4:
        bsr.w (. + 30)
m68k_0203f4_end:
.org 0x203F8
m68k_0203f8:
        lea.l 0xa57a:w,%a1
m68k_0203f8_end:
.org 0x203FC
m68k_0203fc:
        bsr.w (. + 22)
m68k_0203fc_end:
.org 0x20400
m68k_020400:
        lea.l 0xa5a4:w,%a1
m68k_020400_end:
.org 0x20404
m68k_020404:
        bsr.w (. + 14)
m68k_020404_end:
.org 0x20408
m68k_020408:
        lea.l 0xa5ce:w,%a1
m68k_020408_end:
.org 0x2040C
m68k_02040c:
        bsr.w (. + 6)
m68k_02040c_end:
.org 0x20410
m68k_020410:
        rts
m68k_020410_end:
.org 0x20412
m68k_020412:
        move.w (%a1)+,%d1
m68k_020412_end:
.org 0x20414
m68k_020414:
        bmi.w (. + 20)
m68k_020414_end:
.org 0x20418
m68k_020418:
        andi.w #0xff,%d1
m68k_020418_end:
.org 0x2041C
m68k_02041c:
        move.b %d0,(%a0, %d1.w)
m68k_02041c_end:
.org 0x20420
m68k_020420:
        lsl.w #0x2,%d1
m68k_020420_end:
.org 0x20422
m68k_020422:
        clr.l (%a3, %d1.w)
m68k_020422_end:
.org 0x20426
m68k_020426:
        bra.b (. + -20)
m68k_020426_end:
.org 0x20428
m68k_020428:
        rts
m68k_020428_end:
.org 0x2042A
m68k_02042a:
        lea.l 0xf696:w,%a0
m68k_02042a_end:
.org 0x2042E
m68k_02042e:
        lea.l 0xf69a:w,%a1
m68k_02042e_end:
.org 0x20432
m68k_020432:
        lea.l 0xf69e:w,%a2
m68k_020432_end:
.org 0x20436
m68k_020436:
        lea.l 0xf6a2:w,%a3
m68k_020436_end:
.org 0x2043A
m68k_02043a:
        btst.b #0x1,0xf6d7:w
m68k_02043a_end:
.org 0x20440
m68k_020440:
        beq.w (. + 8)
m68k_020440_end:
.org 0x20444
m68k_020444:
        exg %a0,%a1
m68k_020444_end:
.org 0x20446
m68k_020446:
        exg %a2,%a3
m68k_020446_end:
.org 0x20448
m68k_020448:
        move.l (%a0),%d0
m68k_020448_end:
.org 0x2044A
m68k_02044a:
        add.l (%a1),%d0
m68k_02044a_end:
.org 0x2044C
m68k_02044c:
        cmpi.l #0xf423f,%d0
m68k_02044c_end:
.org 0x20452
m68k_020452:
        bls.w (. + 10)
m68k_020452_end:
.org 0x20456
m68k_020456:
        move.l #0xf423f,%d0
m68k_020456_end:
.org 0x2045C
m68k_02045c:
        move.l %d0,(%a0)
m68k_02045c_end:
.org 0x2045E
m68k_02045e:
        clr.l (%a1)
m68k_02045e_end:
.org 0x20460
m68k_020460:
        move.l (%a2),%d0
m68k_020460_end:
.org 0x20462
m68k_020462:
        add.l (%a3),%d0
m68k_020462_end:
.org 0x20464
m68k_020464:
        cmpi.l #0xf423f,%d0
m68k_020464_end:
.org 0x2046A
m68k_02046a:
        bls.w (. + 10)
m68k_02046a_end:
.org 0x2046E
m68k_02046e:
        move.l #0xf423f,%d0
m68k_02046e_end:
.org 0x20474
m68k_020474:
        move.l %d0,(%a2)
m68k_020474_end:
.org 0x20476
m68k_020476:
        clr.l (%a3)
m68k_020476_end:
.org 0x20478
m68k_020478:
        rts
m68k_020478_end:
.org 0x2047A
m68k_02047a:
        tst.w 0xf600:w
m68k_02047a_end:
.org 0x2047E
m68k_02047e:
        bne.w (. + 52)
m68k_02047e_end:
.org 0x20482
m68k_020482:
        jsr 0x194fa:l
m68k_020482_end:
.org 0x20488
m68k_020488:
        lea.l 0xabc1e:l,%a0
m68k_020488_end:
.org 0x2048E
m68k_02048e:
        move.l #0xc0000006,%d0
m68k_02048e_end:
.org 0x20494
m68k_020494:
        move.w #0xa,%d1
m68k_020494_end:
.org 0x20498
m68k_020498:
        move.w #0xc3a2,%d2
m68k_020498_end:
.org 0x2049C
m68k_02049c:
        jsr 0x26bfa:l
m68k_02049c_end:
.org 0x204A2
m68k_0204a2:
        move.w #0xa8,0xf600:w
m68k_0204a2_end:
.org 0x204A8
m68k_0204a8:
        addq.w #0x1,0xf362:w
m68k_0204a8_end:
.org 0x204AC
m68k_0204ac:
        move.w #0x8,0xcfd2:w
m68k_0204ac_end:
.org 0x204B2
m68k_0204b2:
        rts
m68k_0204b2_end:
.org 0x204B4
m68k_0204b4:
        jsr 0x194fa:l
m68k_0204b4_end:
.org 0x204BA
m68k_0204ba:
        tst.w 0xcfd2:w
m68k_0204ba_end:
.org 0x204BE
m68k_0204be:
        beq.w (. + 28)
m68k_0204be_end:
.org 0x204C2
m68k_0204c2:
        subq.w #0x1,0xcfd2:w
m68k_0204c2_end:
.org 0x204C6
m68k_0204c6:
        cmpi.w #0x8,0xcfd2:w
m68k_0204c6_end:
.org 0x204CC
m68k_0204cc:
        bls.w (. + 88)
m68k_0204cc_end:
.org 0x204D0
m68k_0204d0:
        move.w #0x8,0xcfd2:w
m68k_0204d0_end:
.org 0x204D6
m68k_0204d6:
        bra.w (. + 78)
m68k_0204d6_end:
.org 0x204DA
m68k_0204da:
        btst.b #0x5,0xf603:w
m68k_0204da_end:
.org 0x204E0
m68k_0204e0:
        beq.b (. + 68)
m68k_0204e0_end:
.org 0x204E2
m68k_0204e2:
        move.w #0xac,%d0
m68k_0204e2_end:
.org 0x204E6
m68k_0204e6:
        jsr 0x808a:l
m68k_0204e6_end:
.org 0x204EC
m68k_0204ec:
        addq.w #0x1,0xf362:w
m68k_0204ec_end:
.org 0x204F0
m68k_0204f0:
        move.w 0xf362:w,0xf3b0:w
m68k_0204f0_end:
.org 0x204F6
m68k_0204f6:
        move.w 0xf612:w,0xf38a:w
m68k_0204f6_end:
.org 0x204FC
m68k_0204fc:
        move.w #0x406,0xf612:w
m68k_0204fc_end:
.org 0x20502
m68k_020502:
        clr.w 0xf36a:w
m68k_020502_end:
.org 0x20506
m68k_020506:
        lea.l 42(%pc),%a0
m68k_020506_end:
.org 0x2050A
m68k_02050a:
        move.l #0xc0000006,%d0
m68k_02050a_end:
.org 0x20510
m68k_020510:
        move.w #0xa,%d1
m68k_020510_end:
.org 0x20514
m68k_020514:
        move.w #0xc3a2,%d2
m68k_020514_end:
.org 0x20518
m68k_020518:
        jsr 0x26bfa:l
m68k_020518_end:
.org 0x2051E
m68k_02051e:
        jmp 16(%pc)
m68k_02051e_end:
.org 0x20524
m68k_020524:
        jsr 52(%pc)
m68k_020524_end:
.org 0x20528
m68k_020528:
        nop
m68k_020528_end:
.org 0x2052A
m68k_02052a:
        jsr 216(%pc)
m68k_02052a_end:
.org 0x2052E
m68k_02052e:
        nop
m68k_02052e_end:
.org 0x20530
m68k_020530:
        rts
m68k_020530_end:
.org 0x2055A
m68k_02055a:
        bsr.w (. + 102)
m68k_02055a_end:
.org 0x2055E
m68k_02055e:
        bcs.w (. + 92)
m68k_02055e_end:
.org 0x20562
m68k_020562:
        move.b 0xf602:w,%d0
m68k_020562_end:
.org 0x20566
m68k_020566:
        andi.w #0x3,%d0
m68k_020566_end:
.org 0x2056A
m68k_02056a:
        beq.b (. + 70)
m68k_02056a_end:
.org 0x2056C
m68k_02056c:
        subq.w #0x1,0xf608:w
m68k_02056c_end:
.org 0x20570
m68k_020570:
        bne.b (. + 78)
m68k_020570_end:
.org 0x20572
m68k_020572:
        move.w #0xc,0xf608:w
m68k_020572_end:
.org 0x20578
m68k_020578:
        btst.l #0x1,%d0
m68k_020578_end:
.org 0x2057C
m68k_02057c:
        bne.b (. + 28)
m68k_02057c_end:
.org 0x2057E
m68k_02057e:
        tst.w 0xf710:w
m68k_02057e_end:
.org 0x20582
m68k_020582:
        beq.w (. + 12)
m68k_020582_end:
.org 0x20586
m68k_020586:
        subq.w #0x1,0xf710:w
m68k_020586_end:
.org 0x2058A
m68k_02058a:
        bra.w (. + 52)
m68k_02058a_end:
.org 0x2058E
m68k_02058e:
        move.w #0x2,0xf710:w
m68k_02058e_end:
.org 0x20594
m68k_020594:
        bra.w (. + 42)
m68k_020594_end:
.org 0x20598
m68k_020598:
        cmpi.w #0x2,0xf710:w
m68k_020598_end:
.org 0x2059E
m68k_02059e:
        bcc.b (. + 10)
m68k_02059e_end:
.org 0x205A0
m68k_0205a0:
        addq.w #0x1,0xf710:w
m68k_0205a0_end:
.org 0x205A4
m68k_0205a4:
        bra.w (. + 26)
m68k_0205a4_end:
.org 0x205A8
m68k_0205a8:
        clr.w 0xf710:w
m68k_0205a8_end:
.org 0x205AC
m68k_0205ac:
        bra.w (. + 18)
m68k_0205ac_end:
.org 0x205B0
m68k_0205b0:
        move.w #0x1,0xf608:w
m68k_0205b0_end:
.org 0x205B6
m68k_0205b6:
        bra.w (. + 8)
m68k_0205b6_end:
.org 0x205BA
m68k_0205ba:
        clr.w 0xf710:w
m68k_0205ba_end:
.org 0x205BE
m68k_0205be:
        rts
m68k_0205be_end:
.org 0x205C0
m68k_0205c0:
        lea.l 0xf500:w,%a0
m68k_0205c0_end:
.org 0x205C4
m68k_0205c4:
        move.w 0xf378:w,%d0
m68k_0205c4_end:
.org 0x205C8
m68k_0205c8:
        add.w 0xf658:w,%d0
m68k_0205c8_end:
.org 0x205CC
m68k_0205cc:
        lsl.w #0x1,%d0
m68k_0205cc_end:
.org 0x205CE
m68k_0205ce:
        move.w (%a0, %d0.w),%d0
m68k_0205ce_end:
.org 0x205D2
m68k_0205d2:
        andi.w #0xff,%d0
m68k_0205d2_end:
.org 0x205D6
m68k_0205d6:
        lea.l 0xe640:w,%a0
m68k_0205d6_end:
.org 0x205DA
m68k_0205da:
        move.w 0xf68c:w,%d1
m68k_0205da_end:
.org 0x205DE
m68k_0205de:
        lsl.w #0x1,%d1
m68k_0205de_end:
.org 0x205E0
m68k_0205e0:
        cmp.w (%a0, %d1.w),%d0
m68k_0205e0_end:
.org 0x205E4
m68k_0205e4:
        beq.w (. + 26)
m68k_0205e4_end:
.org 0x205E8
m68k_0205e8:
        move.w 0xf68e:w,%d1
m68k_0205e8_end:
.org 0x205EC
m68k_0205ec:
        lsl.w #0x1,%d1
m68k_0205ec_end:
.org 0x205EE
m68k_0205ee:
        cmp.w (%a0, %d1.w),%d0
m68k_0205ee_end:
.org 0x205F2
m68k_0205f2:
        beq.w (. + 12)
m68k_0205f2_end:
.org 0x205F6
m68k_0205f6:
        andi.w #0xfffe,%sr
m68k_0205f6_end:
.org 0x205FA
m68k_0205fa:
        bra.w (. + 8)
m68k_0205fa_end:
.org 0x205FE
m68k_0205fe:
        ori.w #0x1,%sr
m68k_0205fe_end:
.org 0x20602
m68k_020602:
        rts
m68k_020602_end:
.org 0x20604
m68k_020604:
        btst.b #0x5,0xf603:w
m68k_020604_end:
.org 0x2060A
m68k_02060a:
        bne.w (. + 56)
m68k_02060a_end:
.org 0x2060E
m68k_02060e:
        move.b 0xf602:w,%d0
m68k_02060e_end:
.org 0x20612
m68k_020612:
        andi.w #0x3,%d0
m68k_020612_end:
.org 0x20616
m68k_020616:
        bne.w (. + 12)
m68k_020616_end:
.org 0x2061A
m68k_02061a:
        btst.b #0x3,0xf321:w
m68k_02061a_end:
.org 0x20620
m68k_020620:
        bne.b (. + 34)
m68k_020620_end:
.org 0x20622
m68k_020622:
        lea.l 32(%pc),%a0
m68k_020622_end:
.org 0x20626
m68k_020626:
        move.w 0xf710:w,%d0
m68k_020626_end:
.org 0x2062A
m68k_02062a:
        lsl.w #0x1,%d0
m68k_02062a_end:
.org 0x2062C
m68k_02062c:
        add.w 0xf710:w,%d0
m68k_02062c_end:
.org 0x20630
m68k_020630:
        lsl.w #0x3,%d0
m68k_020630_end:
.org 0x20632
m68k_020632:
        addi.w #0x38,%d0
m68k_020632_end:
.org 0x20636
m68k_020636:
        move.w #0x88,%d1
m68k_020636_end:
.org 0x2063A
m68k_02063a:
        clr.w %d2
m68k_02063a_end:
.org 0x2063C
m68k_02063c:
        jsr 0xac08:l
m68k_02063c_end:
.org 0x20642
m68k_020642:
        rts
m68k_020642_end:
.org 0x2068E
m68k_02068e:
        lea.l 0xf500:w,%a0
m68k_02068e_end:
.org 0x20692
m68k_020692:
        move.w 0xf378:w,%d0
m68k_020692_end:
.org 0x20696
m68k_020696:
        lsl.w #0x1,%d0
m68k_020696_end:
.org 0x20698
m68k_020698:
        move.w (%a0, %d0.w),0xf3a6:w
m68k_020698_end:
.org 0x2069E
m68k_02069e:
        addq.w #0x1,0xf362:w
m68k_02069e_end:
.org 0x206A2
m68k_0206a2:
        move.w 0xf710:w,%d0
m68k_0206a2_end:
.org 0x206A6
m68k_0206a6:
        lsl.w #0x1,%d0
m68k_0206a6_end:
.org 0x206A8
m68k_0206a8:
        move.w 8(%pc, %d0.w),%d0
m68k_0206a8_end:
.org 0x206AC
m68k_0206ac:
        jsr 10(%pc, %d0.w)
m68k_0206ac_end:
.org 0x206B0
m68k_0206b0:
        rts
m68k_0206b0_end:
.org 0x20930
m68k_020930:
        btst.b #0x5,0xf603:w
m68k_020930_end:
.org 0x20936
m68k_020936:
        beq.b (. + 64)
m68k_020936_end:
.org 0x20938
m68k_020938:
        bsr.w (. + -1588)
m68k_020938_end:
.org 0x2093C
m68k_02093c:
        tst.w 0xf500:w
m68k_02093c_end:
.org 0x20940
m68k_020940:
        bmi.b (. + 48)
m68k_020940_end:
.org 0x20942
m68k_020942:
        move.w #0x1,0xf3b0:w
m68k_020942_end:
.org 0x20948
m68k_020948:
        move.w 0xf612:w,0xf38a:w
m68k_020948_end:
.org 0x2094E
m68k_02094e:
        move.w #0x405,0xf612:w
m68k_02094e_end:
.org 0x20954
m68k_020954:
        clr.w 0xf362:w
m68k_020954_end:
.org 0x20958
m68k_020958:
        clr.w 0xf378:w
m68k_020958_end:
.org 0x2095C
m68k_02095c:
        clr.w 0xf658:w
m68k_02095c_end:
.org 0x20960
m68k_020960:
        move.w #0x11c,%d0
m68k_020960_end:
.org 0x20964
m68k_020964:
        move.w %d0,0xaf80:w
m68k_020964_end:
.org 0x20968
m68k_020968:
        jsr 0x676f2:l
m68k_020968_end:
.org 0x2096E
m68k_02096e:
        bra.b (. + 8)
m68k_02096e_end:
.org 0x20970
m68k_020970:
        move.w #0xe,0xf362:w
m68k_020970_end:
.org 0x20976
m68k_020976:
        rts
m68k_020976_end:
.org 0x20978
m68k_020978:
        lea.l 0xaf28:w,%a0
m68k_020978_end:
.org 0x2097C
m68k_02097c:
        lea.l 0xcc00:w,%a1
m68k_02097c_end:
.org 0x20980
m68k_020980:
        move.w 0xf68a:w,%d0
m68k_020980_end:
.org 0x20984
m68k_020984:
        move.w (%a0)+,%d1
m68k_020984_end:
.org 0x20986
m68k_020986:
        bmi.w (. + 14)
m68k_020986_end:
.org 0x2098A
m68k_02098a:
        andi.w #0xff,%d1
m68k_02098a_end:
.org 0x2098E
m68k_02098e:
        move.b %d0,(%a1, %d1.w)
m68k_02098e_end:
.org 0x20992
m68k_020992:
        bra.b (. + -14)
m68k_020992_end:
.org 0x20994
m68k_020994:
        addq.w #0x1,0xf362:w
m68k_020994_end:
.org 0x20998
m68k_020998:
        bsr.w (. + 6)
m68k_020998_end:
.org 0x2099C
m68k_02099c:
        rts
m68k_02099c_end:
.org 0x2099E
m68k_02099e:
        lea.l 0xaf28:w,%a0
m68k_02099e_end:
.org 0x209A2
m68k_0209a2:
        move.w 0xf68c:w,%d0
m68k_0209a2_end:
.org 0x209A6
m68k_0209a6:
        btst.b #0x1,0xf6d7:w
m68k_0209a6_end:
.org 0x209AC
m68k_0209ac:
        bne.w (. + 8)
m68k_0209ac_end:
.org 0x209B0
m68k_0209b0:
        move.w 0xf68e:w,%d0
m68k_0209b0_end:
.org 0x209B4
m68k_0209b4:
        lsl.w #0x1,%d0
m68k_0209b4_end:
.org 0x209B6
m68k_0209b6:
        lea.l 0xe640:w,%a1
m68k_0209b6_end:
.org 0x209BA
m68k_0209ba:
        move.w (%a1, %d0.w),%d1
m68k_0209ba_end:
.org 0x209BE
m68k_0209be:
        move.w (%a0)+,%d2
m68k_0209be_end:
.org 0x209C0
m68k_0209c0:
        bmi.w (. + 28)
m68k_0209c0_end:
.org 0x209C4
m68k_0209c4:
        andi.w #0xff,%d2
m68k_0209c4_end:
.org 0x209C8
m68k_0209c8:
        cmp.w %d1,%d2
m68k_0209c8_end:
.org 0x209CA
m68k_0209ca:
        bne.b (. + -12)
m68k_0209ca_end:
.org 0x209CC
m68k_0209cc:
        lea.l 0xcc00:w,%a1
m68k_0209cc_end:
.org 0x209D0
m68k_0209d0:
        move.b #0xff,(%a1, %d1.w)
m68k_0209d0_end:
.org 0x209D6
m68k_0209d6:
        move.w (%a0)+,-0x4(%a0)
m68k_0209d6_end:
.org 0x209DA
m68k_0209da:
        bpl.b (. + -4)
m68k_0209da_end:
.org 0x209DC
m68k_0209dc:
        rts
m68k_0209dc_end:
.org 0x209DE
m68k_0209de:
        bsr.w (. + 10)
m68k_0209de_end:
.org 0x209E2
m68k_0209e2:
        addq.w #0x1,0xf362:w
m68k_0209e2_end:
.org 0x209E6
m68k_0209e6:
        rts
m68k_0209e6_end:
.org 0x209E8
m68k_0209e8:
        lea.l 0xa550:w,%a0
m68k_0209e8_end:
.org 0x209EC
m68k_0209ec:
        lea.l 0xa57a:w,%a1
m68k_0209ec_end:
.org 0x209F0
m68k_0209f0:
        move.w 0xf68c:w,%d0
m68k_0209f0_end:
.org 0x209F4
m68k_0209f4:
        btst.b #0x1,0xf6d7:w
m68k_0209f4_end:
.org 0x209FA
m68k_0209fa:
        beq.w (. + 16)
m68k_0209fa_end:
.org 0x209FE
m68k_0209fe:
        lea.l 0xa5a4:w,%a0
m68k_0209fe_end:
.org 0x20A02
m68k_020a02:
        lea.l 0xa5ce:w,%a1
m68k_020a02_end:
.org 0x20A06
m68k_020a06:
        move.w 0xf68e:w,%d0
m68k_020a06_end:
.org 0x20A0A
m68k_020a0a:
        lea.l 0xe640:w,%a2
m68k_020a0a_end:
.org 0x20A0E
m68k_020a0e:
        lsl.w #0x1,%d0
m68k_020a0e_end:
.org 0x20A10
m68k_020a10:
        move.w (%a2, %d0.w),%d2
m68k_020a10_end:
.org 0x20A14
m68k_020a14:
        lea.l 0xf45e:w,%a2
m68k_020a14_end:
.org 0x20A18
m68k_020a18:
        move.w 0xf68a:w,%d0
m68k_020a18_end:
.org 0x20A1C
m68k_020a1c:
        lsl.w #0x1,%d0
m68k_020a1c_end:
.org 0x20A1E
m68k_020a1e:
        move.w (%a2, %d0.w),%d3
m68k_020a1e_end:
.org 0x20A22
m68k_020a22:
        lea.l 0xaf28:w,%a2
m68k_020a22_end:
.org 0x20A26
m68k_020a26:
        lea.l 0xaf56:w,%a3
m68k_020a26_end:
.org 0x20A2A
m68k_020a2a:
        clr.w %d4
m68k_020a2a_end:
.org 0x20A2C
m68k_020a2c:
        clr.w %d5
m68k_020a2c_end:
.org 0x20A2E
m68k_020a2e:
        move.w (%a2)+,%d0
m68k_020a2e_end:
.org 0x20A30
m68k_020a30:
        bmi.w (. + 24)
m68k_020a30_end:
.org 0x20A34
m68k_020a34:
        andi.w #0xff,%d0
m68k_020a34_end:
.org 0x20A38
m68k_020a38:
        addq.w #0x1,%d4
m68k_020a38_end:
.org 0x20A3A
m68k_020a3a:
        cmp.w %d3,%d0
m68k_020a3a_end:
.org 0x20A3C
m68k_020a3c:
        beq.b (. + -14)
m68k_020a3c_end:
.org 0x20A3E
m68k_020a3e:
        bset.l #0xe,%d0
m68k_020a3e_end:
.org 0x20A42
m68k_020a42:
        move.w %d0,(%a3)+
m68k_020a42_end:
.org 0x20A44
m68k_020a44:
        addq.w #0x1,%d5
m68k_020a44_end:
.org 0x20A46
m68k_020a46:
        bra.b (. + -24)
m68k_020a46_end:
.org 0x20A48
m68k_020a48:
        move.w (%a0)+,%d0
m68k_020a48_end:
.org 0x20A4A
m68k_020a4a:
        bmi.w (. + 28)
m68k_020a4a_end:
.org 0x20A4E
m68k_020a4e:
        andi.w #0xff,%d0
m68k_020a4e_end:
.org 0x20A52
m68k_020a52:
        addq.w #0x1,%d4
m68k_020a52_end:
.org 0x20A54
m68k_020a54:
        cmp.w %d2,%d0
m68k_020a54_end:
.org 0x20A56
m68k_020a56:
        beq.b (. + -14)
m68k_020a56_end:
.org 0x20A58
m68k_020a58:
        cmp.w %d3,%d0
m68k_020a58_end:
.org 0x20A5A
m68k_020a5a:
        beq.b (. + -18)
m68k_020a5a_end:
.org 0x20A5C
m68k_020a5c:
        bset.l #0xe,%d0
m68k_020a5c_end:
.org 0x20A60
m68k_020a60:
        move.w %d0,(%a3)+
m68k_020a60_end:
.org 0x20A62
m68k_020a62:
        addq.w #0x1,%d5
m68k_020a62_end:
.org 0x20A64
m68k_020a64:
        bra.b (. + -28)
m68k_020a64_end:
.org 0x20A66
m68k_020a66:
        move.w (%a1)+,%d0
m68k_020a66_end:
.org 0x20A68
m68k_020a68:
        bmi.w (. + 28)
m68k_020a68_end:
.org 0x20A6C
m68k_020a6c:
        andi.w #0xff,%d0
m68k_020a6c_end:
.org 0x20A70
m68k_020a70:
        addq.w #0x1,%d4
m68k_020a70_end:
.org 0x20A72
m68k_020a72:
        cmp.w %d2,%d0
m68k_020a72_end:
.org 0x20A74
m68k_020a74:
        beq.b (. + -14)
m68k_020a74_end:
.org 0x20A76
m68k_020a76:
        cmp.w %d3,%d0
m68k_020a76_end:
.org 0x20A78
m68k_020a78:
        beq.b (. + -18)
m68k_020a78_end:
.org 0x20A7A
m68k_020a7a:
        bset.l #0xe,%d0
m68k_020a7a_end:
.org 0x20A7E
m68k_020a7e:
        move.w %d0,(%a3)+
m68k_020a7e_end:
.org 0x20A80
m68k_020a80:
        addq.w #0x1,%d5
m68k_020a80_end:
.org 0x20A82
m68k_020a82:
        bra.b (. + -28)
m68k_020a82_end:
.org 0x20A84
m68k_020a84:
        cmpi.w #0xa,%d4
m68k_020a84_end:
.org 0x20A88
m68k_020a88:
        bhi.w (. + 14)
m68k_020a88_end:
.org 0x20A8C
m68k_020a8c:
        move.w #0xffff,0xaf56:w
m68k_020a8c_end:
.org 0x20A92
m68k_020a92:
        bra.w (. + 8)
m68k_020a92_end:
.org 0x20A96
m68k_020a96:
        bsr.w (. + 6)
m68k_020a96_end:
.org 0x20A9A
m68k_020a9a:
        rts
m68k_020a9a_end:
.org 0x20A9C
m68k_020a9c:
        lea.l 0xc300:w,%a0
m68k_020a9c_end:
.org 0x20AA0
m68k_020aa0:
        subq.w #0x2,%d5
m68k_020aa0_end:
.org 0x20AA2
m68k_020aa2:
        move.w %d5,%d0
m68k_020aa2_end:
.org 0x20AA4
m68k_020aa4:
        lea.l 0xaf56:w,%a1
m68k_020aa4_end:
.org 0x20AA8
m68k_020aa8:
        move.w (%a1)+,%d1
m68k_020aa8_end:
.org 0x20AAA
m68k_020aaa:
        andi.w #0xff,%d1
m68k_020aaa_end:
.org 0x20AAE
m68k_020aae:
        move.b (%a0, %d1.w),%d3
m68k_020aae_end:
.org 0x20AB2
m68k_020ab2:
        move.w (%a1),%d2
m68k_020ab2_end:
.org 0x20AB4
m68k_020ab4:
        andi.w #0xff,%d2
m68k_020ab4_end:
.org 0x20AB8
m68k_020ab8:
        cmp.b (%a0, %d2.w),%d3
m68k_020ab8_end:
.org 0x20ABC
m68k_020abc:
        bls.w (. + 10)
m68k_020abc_end:
.org 0x20AC0
m68k_020ac0:
        move.w (%a1),-0x2(%a1)
m68k_020ac0_end:
.org 0x20AC4
m68k_020ac4:
        move.w %d1,(%a1)
m68k_020ac4_end:
.org 0x20AC6
m68k_020ac6:
        dbra %d0,(. + -30)
m68k_020ac6_end:
.org 0x20ACA
m68k_020aca:
        subq.w #0x1,%d5
m68k_020aca_end:
.org 0x20ACC
m68k_020acc:
        bne.b (. + -42)
m68k_020acc_end:
.org 0x20ACE
m68k_020ace:
        lea.l 0xaf56:w,%a3
m68k_020ace_end:
.org 0x20AD2
m68k_020ad2:
        subi.w #0xa,%d4
m68k_020ad2_end:
.org 0x20AD6
m68k_020ad6:
        lsl.w #0x1,%d4
m68k_020ad6_end:
.org 0x20AD8
m68k_020ad8:
        move.w #0xffff,(%a3, %d4.w)
m68k_020ad8_end:
.org 0x20ADE
m68k_020ade:
        rts
m68k_020ade_end:
.org 0x20AE0
m68k_020ae0:
        bsr.w (. + 12)
m68k_020ae0_end:
.org 0x20AE4
m68k_020ae4:
        move.w #0x1c,0xf362:w
m68k_020ae4_end:
.org 0x20AEA
m68k_020aea:
        rts
m68k_020aea_end:
.org 0x20AEC
m68k_020aec:
        tst.w 0xaf56:w
m68k_020aec_end:
.org 0x20AF0
m68k_020af0:
        bmi.w (. + 36)
m68k_020af0_end:
.org 0x20AF4
m68k_020af4:
        move.w 0xf68a:w,%d0
m68k_020af4_end:
.org 0x20AF8
m68k_020af8:
        bset.l #0x7,%d0
m68k_020af8_end:
.org 0x20AFC
m68k_020afc:
        lea.l 0xaf56:w,%a0
m68k_020afc_end:
.org 0x20B00
m68k_020b00:
        lea.l 0xcc00:w,%a1
m68k_020b00_end:
.org 0x20B04
m68k_020b04:
        move.w (%a0)+,%d1
m68k_020b04_end:
.org 0x20B06
m68k_020b06:
        bmi.w (. + 14)
m68k_020b06_end:
.org 0x20B0A
m68k_020b0a:
        andi.w #0xff,%d1
m68k_020b0a_end:
.org 0x20B0E
m68k_020b0e:
        move.b %d0,(%a1, %d1.w)
m68k_020b0e_end:
.org 0x20B12
m68k_020b12:
        bra.b (. + -14)
m68k_020b12_end:
.org 0x20B14
m68k_020b14:
        rts
m68k_020b14_end:
.org 0x20B16
m68k_020b16:
        rts
m68k_020b16_end:
.org 0x20B18
m68k_020b18:
        rts
m68k_020b18_end:
.org 0x20B1A
m68k_020b1a:
        move.b 0xf602:w,%d0
m68k_020b1a_end:
.org 0x20B1E
m68k_020b1e:
        andi.w #0xc,%d0
m68k_020b1e_end:
.org 0x20B22
m68k_020b22:
        beq.w (. + 70)
m68k_020b22_end:
.org 0x20B26
m68k_020b26:
        subq.w #0x1,0xf608:w
m68k_020b26_end:
.org 0x20B2A
m68k_020b2a:
        bne.w (. + 150)
m68k_020b2a_end:
.org 0x20B2E
m68k_020b2e:
        move.w #0xc,0xf608:w
m68k_020b2e_end:
.org 0x20B34
m68k_020b34:
        btst.l #0x3,%d0
m68k_020b34_end:
.org 0x20B38
m68k_020b38:
        bne.w (. + 30)
m68k_020b38_end:
.org 0x20B3C
m68k_020b3c:
        move.w 0xf39a:w,%d0
m68k_020b3c_end:
.org 0x20B40
m68k_020b40:
        subq.w #0x1,%d0
m68k_020b40_end:
.org 0x20B42
m68k_020b42:
        bcs.w (. + 126)
m68k_020b42_end:
.org 0x20B46
m68k_020b46:
        cmp.w 0xf3ec:w,%d0
m68k_020b46_end:
.org 0x20B4A
m68k_020b4a:
        bcs.w (. + 118)
m68k_020b4a_end:
.org 0x20B4E
m68k_020b4e:
        move.w %d0,0xf39a:w
m68k_020b4e_end:
.org 0x20B52
m68k_020b52:
        bra.w (. + 110)
m68k_020b52_end:
.org 0x20B56
m68k_020b56:
        cmpi.w #0x5,0xf39a:w
m68k_020b56_end:
.org 0x20B5C
m68k_020b5c:
        bcc.w (. + 100)
m68k_020b5c_end:
.org 0x20B60
m68k_020b60:
        addq.w #0x1,0xf39a:w
m68k_020b60_end:
.org 0x20B64
m68k_020b64:
        bra.w (. + 92)
m68k_020b64_end:
.org 0x20B68
m68k_020b68:
        move.b 0xf602:w,%d0
m68k_020b68_end:
.org 0x20B6C
m68k_020b6c:
        andi.w #0x3,%d0
m68k_020b6c_end:
.org 0x20B70
m68k_020b70:
        beq.b (. + 74)
m68k_020b70_end:
.org 0x20B72
m68k_020b72:
        subq.w #0x1,0xf608:w
m68k_020b72_end:
.org 0x20B76
m68k_020b76:
        bne.w (. + 74)
m68k_020b76_end:
.org 0x20B7A
m68k_020b7a:
        move.w #0xc,0xf608:w
m68k_020b7a_end:
.org 0x20B80
m68k_020b80:
        btst.l #0x1,%d0
m68k_020b80_end:
.org 0x20B84
m68k_020b84:
        bne.b (. + 30)
m68k_020b84_end:
.org 0x20B86
m68k_020b86:
        move.l 0xf39e:w,%d0
m68k_020b86_end:
.org 0x20B8A
m68k_020b8a:
        move.w 0xf39a:w,%d1
m68k_020b8a_end:
.org 0x20B8E
m68k_020b8e:
        lsl.w #0x2,%d1
m68k_020b8e_end:
.org 0x20B90
m68k_020b90:
        add.l 48(%pc, %d1.w),%d0
m68k_020b90_end:
.org 0x20B94
m68k_020b94:
        cmp.l 0xf3f4:w,%d0
m68k_020b94_end:
.org 0x20B98
m68k_020b98:
        bhi.b (. + 40)
m68k_020b98_end:
.org 0x20B9A
m68k_020b9a:
        move.l %d0,0xf39e:w
m68k_020b9a_end:
.org 0x20B9E
m68k_020b9e:
        bra.w (. + 34)
m68k_020b9e_end:
.org 0x20BA2
m68k_020ba2:
        move.l 0xf39e:w,%d0
m68k_020ba2_end:
.org 0x20BA6
m68k_020ba6:
        move.w 0xf39a:w,%d1
m68k_020ba6_end:
.org 0x20BAA
m68k_020baa:
        lsl.w #0x2,%d1
m68k_020baa_end:
.org 0x20BAC
m68k_020bac:
        sub.l 20(%pc, %d1.w),%d0
m68k_020bac_end:
.org 0x20BB0
m68k_020bb0:
        bcs.w (. + 16)
m68k_020bb0_end:
.org 0x20BB4
m68k_020bb4:
        move.l %d0,0xf39e:w
m68k_020bb4_end:
.org 0x20BB8
m68k_020bb8:
        bra.b (. + 8)
m68k_020bb8_end:
.org 0x20BBA
m68k_020bba:
        move.w #0x1,0xf608:w
m68k_020bba_end:
.org 0x20BC0
m68k_020bc0:
        rts
m68k_020bc0_end:
.org 0x20BDA
m68k_020bda:
        move.l 0xf39e:w,%d0
m68k_020bda_end:
.org 0x20BDE
m68k_020bde:
        move.w #0xc386,%d1
m68k_020bde_end:
.org 0x20BE2
m68k_020be2:
        clr.w %d2
m68k_020be2_end:
.org 0x20BE4
m68k_020be4:
        lea.l 0xd300:w,%a6
m68k_020be4_end:
.org 0x20BE8
m68k_020be8:
        jsr 0x1270a:l
m68k_020be8_end:
.org 0x20BEE
m68k_020bee:
        lea.l 0xd100:w,%a0
m68k_020bee_end:
.org 0x20BF2
m68k_020bf2:
        adda.w 0xf31a:w,%a0
m68k_020bf2_end:
.org 0x20BF6
m68k_020bf6:
        move.w #0x6,(%a0)+
m68k_020bf6_end:
.org 0x20BFA
m68k_020bfa:
        move.w #0xc624,(%a0)+
m68k_020bfa_end:
.org 0x20BFE
m68k_020bfe:
        lea.l 0xd300:w,%a1
m68k_020bfe_end:
.org 0x20C02
m68k_020c02:
        clr.w %d0
m68k_020c02_end:
.org 0x20C04
m68k_020c04:
        move.w #0x5,%d1
m68k_020c04_end:
.org 0x20C08
m68k_020c08:
        move.w (%a1)+,%d2
m68k_020c08_end:
.org 0x20C0A
m68k_020c0a:
        bne.b (. + 20)
m68k_020c0a_end:
.org 0x20C0C
m68k_020c0c:
        cmp.w 0xf39a:w,%d0
m68k_020c0c_end:
.org 0x20C10
m68k_020c10:
        bcc.b (. + 10)
m68k_020c10_end:
.org 0x20C12
m68k_020c12:
        move.w #0xc001,%d2
m68k_020c12_end:
.org 0x20C16
m68k_020c16:
        bra.w (. + 8)
m68k_020c16_end:
.org 0x20C1A
m68k_020c1a:
        move.w #0xc386,%d2
m68k_020c1a_end:
.org 0x20C1E
m68k_020c1e:
        move.w %d2,(%a0)+
m68k_020c1e_end:
.org 0x20C20
m68k_020c20:
        addq.w #0x1,%d0
m68k_020c20_end:
.org 0x20C22
m68k_020c22:
        dbra %d1,(. + -26)
m68k_020c22_end:
.org 0x20C26
m68k_020c26:
        clr.w (%a0)
m68k_020c26_end:
.org 0x20C28
m68k_020c28:
        addi.w #0x10,0xf31a:w
m68k_020c28_end:
.org 0x20C2E
m68k_020c2e:
        rts
m68k_020c2e_end:
.org 0x20C30
m68k_020c30:
        btst.b #0x4,0xf321:w
m68k_020c30_end:
.org 0x20C36
m68k_020c36:
        bne.b (. + 28)
m68k_020c36_end:
.org 0x20C38
m68k_020c38:
        lea.l 26(%pc),%a0
m68k_020c38_end:
.org 0x20C3C
m68k_020c3c:
        move.w #0x60,%d0
m68k_020c3c_end:
.org 0x20C40
m68k_020c40:
        move.w 0xf39a:w,%d1
m68k_020c40_end:
.org 0x20C44
m68k_020c44:
        lsl.w #0x3,%d1
m68k_020c44_end:
.org 0x20C46
m68k_020c46:
        addi.w #0x90,%d1
m68k_020c46_end:
.org 0x20C4A
m68k_020c4a:
        clr.w %d2
m68k_020c4a_end:
.org 0x20C4C
m68k_020c4c:
        jsr 0xac08:l
m68k_020c4c_end:
.org 0x20C52
m68k_020c52:
        rts
m68k_020c52_end:
.org 0x20C5C
m68k_020c5c:
        rts
m68k_020c5c_end:
.org 0x20C5E
m68k_020c5e:
        move.b 0xf602:w,%d0
m68k_020c5e_end:
.org 0x20C62
m68k_020c62:
        andi.w #0xc,%d0
m68k_020c62_end:
.org 0x20C66
m68k_020c66:
        beq.b (. + 66)
m68k_020c66_end:
.org 0x20C68
m68k_020c68:
        subq.w #0x1,0xf608:w
m68k_020c68_end:
.org 0x20C6C
m68k_020c6c:
        bne.w (. + 148)
m68k_020c6c_end:
.org 0x20C70
m68k_020c70:
        move.w #0xc,0xf608:w
m68k_020c70_end:
.org 0x20C76
m68k_020c76:
        btst.l #0x3,%d0
m68k_020c76_end:
.org 0x20C7A
m68k_020c7a:
        bne.b (. + 28)
m68k_020c7a_end:
.org 0x20C7C
m68k_020c7c:
        move.w 0xf4f0:w,%d0
m68k_020c7c_end:
.org 0x20C80
m68k_020c80:
        subq.w #0x1,%d0
m68k_020c80_end:
.org 0x20C82
m68k_020c82:
        bcs.w (. + 126)
m68k_020c82_end:
.org 0x20C86
m68k_020c86:
        cmp.w 0xf4f2:w,%d0
m68k_020c86_end:
.org 0x20C8A
m68k_020c8a:
        bcs.w (. + 118)
m68k_020c8a_end:
.org 0x20C8E
m68k_020c8e:
        move.w %d0,0xf4f0:w
m68k_020c8e_end:
.org 0x20C92
m68k_020c92:
        bra.w (. + 110)
m68k_020c92_end:
.org 0x20C96
m68k_020c96:
        cmpi.w #0x5,0xf4f0:w
m68k_020c96_end:
.org 0x20C9C
m68k_020c9c:
        bcc.w (. + 100)
m68k_020c9c_end:
.org 0x20CA0
m68k_020ca0:
        addq.w #0x1,0xf4f0:w
m68k_020ca0_end:
.org 0x20CA4
m68k_020ca4:
        bra.w (. + 92)
m68k_020ca4_end:
.org 0x20CA8
m68k_020ca8:
        move.b 0xf602:w,%d0
m68k_020ca8_end:
.org 0x20CAC
m68k_020cac:
        andi.w #0x3,%d0
m68k_020cac_end:
.org 0x20CB0
m68k_020cb0:
        beq.b (. + 74)
m68k_020cb0_end:
.org 0x20CB2
m68k_020cb2:
        subq.w #0x1,0xf608:w
m68k_020cb2_end:
.org 0x20CB6
m68k_020cb6:
        bne.w (. + 74)
m68k_020cb6_end:
.org 0x20CBA
m68k_020cba:
        move.w #0xc,0xf608:w
m68k_020cba_end:
.org 0x20CC0
m68k_020cc0:
        btst.l #0x1,%d0
m68k_020cc0_end:
.org 0x20CC4
m68k_020cc4:
        bne.b (. + 30)
m68k_020cc4_end:
.org 0x20CC6
m68k_020cc6:
        move.l 0xf3ba:w,%d0
m68k_020cc6_end:
.org 0x20CCA
m68k_020cca:
        move.w 0xf4f0:w,%d1
m68k_020cca_end:
.org 0x20CCE
m68k_020cce:
        lsl.w #0x2,%d1
m68k_020cce_end:
.org 0x20CD0
m68k_020cd0:
        add.l 48(%pc, %d1.w),%d0
m68k_020cd0_end:
.org 0x20CD4
m68k_020cd4:
        cmp.l 0xf3f8:w,%d0
m68k_020cd4_end:
.org 0x20CD8
m68k_020cd8:
        bhi.b (. + 40)
m68k_020cd8_end:
.org 0x20CDA
m68k_020cda:
        move.l %d0,0xf3ba:w
m68k_020cda_end:
.org 0x20CDE
m68k_020cde:
        bra.w (. + 34)
m68k_020cde_end:
.org 0x20CE2
m68k_020ce2:
        move.l 0xf3ba:w,%d0
m68k_020ce2_end:
.org 0x20CE6
m68k_020ce6:
        move.w 0xf4f0:w,%d1
m68k_020ce6_end:
.org 0x20CEA
m68k_020cea:
        lsl.w #0x2,%d1
m68k_020cea_end:
.org 0x20CEC
m68k_020cec:
        sub.l 20(%pc, %d1.w),%d0
m68k_020cec_end:
.org 0x20CF0
m68k_020cf0:
        bcs.w (. + 16)
m68k_020cf0_end:
.org 0x20CF4
m68k_020cf4:
        move.l %d0,0xf3ba:w
m68k_020cf4_end:
.org 0x20CF8
m68k_020cf8:
        bra.b (. + 8)
m68k_020cf8_end:
.org 0x20CFA
m68k_020cfa:
        move.w #0x1,0xf608:w
m68k_020cfa_end:
.org 0x20D00
m68k_020d00:
        rts
m68k_020d00_end:
.org 0x20D1A
m68k_020d1a:
        move.l 0xf3ba:w,%d0
m68k_020d1a_end:
.org 0x20D1E
m68k_020d1e:
        move.w #0xc386,%d1
m68k_020d1e_end:
.org 0x20D22
m68k_020d22:
        clr.w %d2
m68k_020d22_end:
.org 0x20D24
m68k_020d24:
        lea.l 0xd300:w,%a6
m68k_020d24_end:
.org 0x20D28
m68k_020d28:
        jsr 0x1270a:l
m68k_020d28_end:
.org 0x20D2E
m68k_020d2e:
        lea.l 0xd100:w,%a0
m68k_020d2e_end:
.org 0x20D32
m68k_020d32:
        adda.w 0xf31a:w,%a0
m68k_020d32_end:
.org 0x20D36
m68k_020d36:
        move.w #0x6,(%a0)+
m68k_020d36_end:
.org 0x20D3A
m68k_020d3a:
        move.w #0xc7a4,(%a0)+
m68k_020d3a_end:
.org 0x20D3E
m68k_020d3e:
        lea.l 0xd300:w,%a1
m68k_020d3e_end:
.org 0x20D42
m68k_020d42:
        clr.w %d0
m68k_020d42_end:
.org 0x20D44
m68k_020d44:
        move.w #0x5,%d1
m68k_020d44_end:
.org 0x20D48
m68k_020d48:
        move.w (%a1)+,%d2
m68k_020d48_end:
.org 0x20D4A
m68k_020d4a:
        bne.b (. + 20)
m68k_020d4a_end:
.org 0x20D4C
m68k_020d4c:
        cmp.w 0xf4f0:w,%d0
m68k_020d4c_end:
.org 0x20D50
m68k_020d50:
        bcc.b (. + 10)
m68k_020d50_end:
.org 0x20D52
m68k_020d52:
        move.w #0xc001,%d2
m68k_020d52_end:
.org 0x20D56
m68k_020d56:
        bra.w (. + 8)
m68k_020d56_end:
.org 0x20D5A
m68k_020d5a:
        move.w #0xc386,%d2
m68k_020d5a_end:
.org 0x20D5E
m68k_020d5e:
        move.w %d2,(%a0)+
m68k_020d5e_end:
.org 0x20D60
m68k_020d60:
        addq.w #0x1,%d0
m68k_020d60_end:
.org 0x20D62
m68k_020d62:
        dbra %d1,(. + -26)
m68k_020d62_end:
.org 0x20D66
m68k_020d66:
        clr.w (%a0)
m68k_020d66_end:
.org 0x20D68
m68k_020d68:
        addi.w #0x10,0xf31a:w
m68k_020d68_end:
.org 0x20D6E
m68k_020d6e:
        rts
m68k_020d6e_end:
.org 0x20D70
m68k_020d70:
        btst.b #0x4,0xf321:w
m68k_020d70_end:
.org 0x20D76
m68k_020d76:
        bne.b (. + 28)
m68k_020d76_end:
.org 0x20D78
m68k_020d78:
        lea.l 26(%pc),%a0
m68k_020d78_end:
.org 0x20D7C
m68k_020d7c:
        move.w #0x78,%d0
m68k_020d7c_end:
.org 0x20D80
m68k_020d80:
        move.w 0xf4f0:w,%d1
m68k_020d80_end:
.org 0x20D84
m68k_020d84:
        lsl.w #0x3,%d1
m68k_020d84_end:
.org 0x20D86
m68k_020d86:
        addi.w #0x90,%d1
m68k_020d86_end:
.org 0x20D8A
m68k_020d8a:
        clr.w %d2
m68k_020d8a_end:
.org 0x20D8C
m68k_020d8c:
        jsr 0xac08:l
m68k_020d8c_end:
.org 0x20D92
m68k_020d92:
        rts
m68k_020d92_end:
.org 0x20D9C
m68k_020d9c:
        rts
m68k_020d9c_end:
.org 0x20D9E
m68k_020d9e:
        rts
m68k_020d9e_end:
.org 0x20DA0
m68k_020da0:
        rts
m68k_020da0_end:
.org 0x20DBE
m68k_020dbe:
        addq.w #0x1,0xf362:w
m68k_020dbe_end:
.org 0x20DC2
m68k_020dc2:
        btst.b #0x1,0xf6d7:w
m68k_020dc2_end:
.org 0x20DC8
m68k_020dc8:
        bne.b (. + 12)
m68k_020dc8_end:
.org 0x20DCA
m68k_020dca:
        move.l 0xf69e:w,%d0
m68k_020dca_end:
.org 0x20DCE
m68k_020dce:
        add.l 0xf696:w,%d0
m68k_020dce_end:
.org 0x20DD2
m68k_020dd2:
        bra.b (. + 10)
m68k_020dd2_end:
.org 0x20DD4
m68k_020dd4:
        move.l 0xf69a:w,%d0
m68k_020dd4_end:
.org 0x20DD8
m68k_020dd8:
        add.l 0xf6a2:w,%d0
m68k_020dd8_end:
.org 0x20DDC
m68k_020ddc:
        move.l %d0,0xaff4:w
m68k_020ddc_end:
.org 0x20DE0
m68k_020de0:
        rts
m68k_020de0_end:
.org 0x20DE2
m68k_020de2:
        lea.l 0xf500:w,%a1
m68k_020de2_end:
.org 0x20DE6
m68k_020de6:
        btst.b #0x1,0xf6d7:w
m68k_020de6_end:
.org 0x20DEC
m68k_020dec:
        bne.b (. + 14)
m68k_020dec_end:
.org 0x20DEE
m68k_020dee:
        lea.l 0xa550:w,%a0
m68k_020dee_end:
.org 0x20DF2
m68k_020df2:
        move.w 0xf68c:w,%d1
m68k_020df2_end:
.org 0x20DF6
m68k_020df6:
        bra.w (. + 12)
m68k_020df6_end:
.org 0x20DFA
m68k_020dfa:
        lea.l 0xa5a4:w,%a0
m68k_020dfa_end:
.org 0x20DFE
m68k_020dfe:
        move.w 0xf68e:w,%d1
m68k_020dfe_end:
.org 0x20E02
m68k_020e02:
        lea.l 0xe640:w,%a2
m68k_020e02_end:
.org 0x20E06
m68k_020e06:
        lsl.w #0x1,%d1
m68k_020e06_end:
.org 0x20E08
m68k_020e08:
        move.w (%a2, %d1.w),%d1
m68k_020e08_end:
.org 0x20E0C
m68k_020e0c:
        clr.w %d0
m68k_020e0c_end:
.org 0x20E0E
m68k_020e0e:
        move.w (%a0)+,%d2
m68k_020e0e_end:
.org 0x20E10
m68k_020e10:
        bmi.b (. + 16)
m68k_020e10_end:
.org 0x20E12
m68k_020e12:
        andi.w #0xff,%d2
m68k_020e12_end:
.org 0x20E16
m68k_020e16:
        cmp.w %d2,%d1
m68k_020e16_end:
.org 0x20E18
m68k_020e18:
        beq.b (. + -10)
m68k_020e18_end:
.org 0x20E1A
m68k_020e1a:
        move.w %d2,(%a1)+
m68k_020e1a_end:
.org 0x20E1C
m68k_020e1c:
        addq.w #0x1,%d0
m68k_020e1c_end:
.org 0x20E1E
m68k_020e1e:
        bra.b (. + -16)
m68k_020e1e_end:
.org 0x20E20
m68k_020e20:
        move.w #0xffff,(%a1)
m68k_020e20_end:
.org 0x20E24
m68k_020e24:
        move.w %d0,0xf636:w
m68k_020e24_end:
.org 0x20E28
m68k_020e28:
        clr.w 0xf658:w
m68k_020e28_end:
.org 0x20E2C
m68k_020e2c:
        clr.w 0xf378:w
m68k_020e2c_end:
.org 0x20E30
m68k_020e30:
        tst.w 0xf500:w
m68k_020e30_end:
.org 0x20E34
m68k_020e34:
        bpl.w (. + 14)
m68k_020e34_end:
.org 0x20E38
m68k_020e38:
        move.w #0x17,0xf362:w
m68k_020e38_end:
.org 0x20E3E
m68k_020e3e:
        bra.w (. + 48)
m68k_020e3e_end:
.org 0x20E42
m68k_020e42:
        addq.w #0x1,0xf362:w
m68k_020e42_end:
.org 0x20E46
m68k_020e46:
        move.w 0xf362:w,0xf3b0:w
m68k_020e46_end:
.org 0x20E4C
m68k_020e4c:
        move.w 0xf612:w,0xf38a:w
m68k_020e4c_end:
.org 0x20E52
m68k_020e52:
        move.w #0x405,0xf612:w
m68k_020e52_end:
.org 0x20E58
m68k_020e58:
        clr.w 0xf362:w
m68k_020e58_end:
.org 0x20E5C
m68k_020e5c:
        clr.w 0xf6d2:w
m68k_020e5c_end:
.org 0x20E60
m68k_020e60:
        move.w #0x123,%d0
m68k_020e60_end:
.org 0x20E64
m68k_020e64:
        move.w %d0,0xaf80:w
m68k_020e64_end:
.org 0x20E68
m68k_020e68:
        jsr 0x676f2:l
m68k_020e68_end:
.org 0x20E6E
m68k_020e6e:
        rts
m68k_020e6e_end:
.org 0x20E70
m68k_020e70:
        bsr.w (. + -31094)
m68k_020e70_end:
.org 0x20E74
m68k_020e74:
        move.w #0xc386,0xf692:w
m68k_020e74_end:
.org 0x20E7A
m68k_020e7a:
        move.w #0xc001,0xf694:w
m68k_020e7a_end:
.org 0x20E80
m68k_020e80:
        move.w #0x1,%d0
m68k_020e80_end:
.org 0x20E84
m68k_020e84:
        move.w #0x3,%d1
m68k_020e84_end:
.org 0x20E88
m68k_020e88:
        move.w #0x1,%d3
m68k_020e88_end:
.org 0x20E8C
m68k_020e8c:
        lea.l 0xabc6e:l,%a0
m68k_020e8c_end:
.org 0x20E92
m68k_020e92:
        lea.l 0xd300:w,%a1
m68k_020e92_end:
.org 0x20E96
m68k_020e96:
        jsr 0xae8a:l
m68k_020e96_end:
.org 0x20E9C
m68k_020e9c:
        move.l #0x40a00002,0xc00004:l
m68k_020e9c_end:
.org 0x20EA6
m68k_020ea6:
        lea.l 0xd300:w,%a1
m68k_020ea6_end:
.org 0x20EAA
m68k_020eaa:
        move.w #0x3f,%d3
m68k_020eaa_end:
.org 0x20EAE
m68k_020eae:
        move.l (%a1)+,0xc00000:l
m68k_020eae_end:
.org 0x20EB4
m68k_020eb4:
        dbra %d3,(. + -6)
m68k_020eb4_end:
.org 0x20EB8
m68k_020eb8:
        addq.w #0x1,0xf362:w
m68k_020eb8_end:
.org 0x20EBC
m68k_020ebc:
        rts
m68k_020ebc_end:
.org 0x20EBE
m68k_020ebe:
        bsr.w (. + -31172)
m68k_020ebe_end:
.org 0x20EC2
m68k_020ec2:
        btst.b #0x1,0xf6d7:w
m68k_020ec2_end:
.org 0x20EC8
m68k_020ec8:
        bne.b (. + 18)
m68k_020ec8_end:
.org 0x20ECA
m68k_020eca:
        move.l 0xf696:w,0xf3f4:w
m68k_020eca_end:
.org 0x20ED0
m68k_020ed0:
        move.l 0xf69e:w,0xf3f8:w
m68k_020ed0_end:
.org 0x20ED6
m68k_020ed6:
        bra.w (. + 16)
m68k_020ed6_end:
.org 0x20EDA
m68k_020eda:
        move.l 0xf69a:w,0xf3f4:w
m68k_020eda_end:
.org 0x20EE0
m68k_020ee0:
        move.l 0xf6a2:w,0xf3f8:w
m68k_020ee0_end:
.org 0x20EE6
m68k_020ee6:
        lea.l 0xabc72:l,%a0
m68k_020ee6_end:
.org 0x20EEC
m68k_020eec:
        move.l #0xc000000c,%d0
m68k_020eec_end:
.org 0x20EF2
m68k_020ef2:
        move.w #0x6,%d1
m68k_020ef2_end:
.org 0x20EF6
m68k_020ef6:
        move.w #0xc19c,%d2
m68k_020ef6_end:
.org 0x20EFA
m68k_020efa:
        jsr 0x26bfa:l
m68k_020efa_end:
.org 0x20F00
m68k_020f00:
        clr.l 0xf39e:w
m68k_020f00_end:
.org 0x20F04
m68k_020f04:
        clr.l 0xf3ba:w
m68k_020f04_end:
.org 0x20F08
m68k_020f08:
        lea.l 0xabcbe:l,%a0
m68k_020f08_end:
.org 0x20F0E
m68k_020f0e:
        move.l #0xc000000c,%d0
m68k_020f0e_end:
.org 0x20F14
m68k_020f14:
        move.w #0x7,%d1
m68k_020f14_end:
.org 0x20F18
m68k_020f18:
        move.w #0xc51c,%d2
m68k_020f18_end:
.org 0x20F1C
m68k_020f1c:
        jsr 0x26bfa:l
m68k_020f1c_end:
.org 0x20F22
m68k_020f22:
        move.l 0xf3f4:w,%d0
m68k_020f22_end:
.org 0x20F26
m68k_020f26:
        bsr.w (. + 54)
m68k_020f26_end:
.org 0x20F2A
m68k_020f2a:
        move.w %d0,0xf3ec:w
m68k_020f2a_end:
.org 0x20F2E
m68k_020f2e:
        move.l 0xf3f8:w,%d0
m68k_020f2e_end:
.org 0x20F32
m68k_020f32:
        bsr.w (. + 42)
m68k_020f32_end:
.org 0x20F36
m68k_020f36:
        move.w %d0,0xf4f2:w
m68k_020f36_end:
.org 0x20F3A
m68k_020f3a:
        move.w #0x5,0xf39a:w
m68k_020f3a_end:
.org 0x20F40
m68k_020f40:
        move.w #0x5,0xf4f0:w
m68k_020f40_end:
.org 0x20F46
m68k_020f46:
        addq.w #0x1,0xf362:w
m68k_020f46_end:
.org 0x20F4A
m68k_020f4a:
        move.w 0xf378:w,%d0
m68k_020f4a_end:
.org 0x20F4E
m68k_020f4e:
        lsl.w #0x1,%d0
m68k_020f4e_end:
.org 0x20F50
m68k_020f50:
        lea.l 0xf500:w,%a0
m68k_020f50_end:
.org 0x20F54
m68k_020f54:
        move.w (%a0, %d0.w),0xf3a6:w
m68k_020f54_end:
.org 0x20F5A
m68k_020f5a:
        rts
m68k_020f5a_end:
.org 0x20F5C
m68k_020f5c:
        clr.w %d1
m68k_020f5c_end:
.org 0x20F5E
m68k_020f5e:
        cmpi.l #0xa,%d0
m68k_020f5e_end:
.org 0x20F64
m68k_020f64:
        bcs.b (. + 44)
m68k_020f64_end:
.org 0x20F66
m68k_020f66:
        addq.w #0x1,%d1
m68k_020f66_end:
.org 0x20F68
m68k_020f68:
        cmpi.l #0x64,%d0
m68k_020f68_end:
.org 0x20F6E
m68k_020f6e:
        bcs.b (. + 34)
m68k_020f6e_end:
.org 0x20F70
m68k_020f70:
        addq.w #0x1,%d1
m68k_020f70_end:
.org 0x20F72
m68k_020f72:
        cmpi.l #0x3e8,%d0
m68k_020f72_end:
.org 0x20F78
m68k_020f78:
        bcs.b (. + 24)
m68k_020f78_end:
.org 0x20F7A
m68k_020f7a:
        addq.w #0x1,%d1
m68k_020f7a_end:
.org 0x20F7C
m68k_020f7c:
        cmpi.l #0x2710,%d0
m68k_020f7c_end:
.org 0x20F82
m68k_020f82:
        bcs.b (. + 14)
m68k_020f82_end:
.org 0x20F84
m68k_020f84:
        addq.w #0x1,%d1
m68k_020f84_end:
.org 0x20F86
m68k_020f86:
        cmpi.l #0x186a0,%d0
m68k_020f86_end:
.org 0x20F8C
m68k_020f8c:
        bcs.b (. + 4)
m68k_020f8c_end:
.org 0x20F8E
m68k_020f8e:
        addq.w #0x1,%d1
m68k_020f8e_end:
.org 0x20F90
m68k_020f90:
        move.w #0x5,%d0
m68k_020f90_end:
.org 0x20F94
m68k_020f94:
        sub.w %d1,%d0
m68k_020f94_end:
.org 0x20F96
m68k_020f96:
        rts
m68k_020f96_end:
.org 0x20F98
m68k_020f98:
        bsr.w (. + -31390)
m68k_020f98_end:
.org 0x20F9C
m68k_020f9c:
        bsr.w (. + -1154)
m68k_020f9c_end:
.org 0x20FA0
m68k_020fa0:
        bsr.w (. + -966)
m68k_020fa0_end:
.org 0x20FA4
m68k_020fa4:
        bsr.w (. + -884)
m68k_020fa4_end:
.org 0x20FA8
m68k_020fa8:
        btst.b #0x5,0xf603:w
m68k_020fa8_end:
.org 0x20FAE
m68k_020fae:
        beq.b (. + 18)
m68k_020fae_end:
.org 0x20FB0
m68k_020fb0:
        move.w #0xac,%d0
m68k_020fb0_end:
.org 0x20FB4
m68k_020fb4:
        jsr 0x808a:l
m68k_020fb4_end:
.org 0x20FBA
m68k_020fba:
        addq.w #0x1,0xf362:w
m68k_020fba_end:
.org 0x20FBE
m68k_020fbe:
        bra.b (. + 34)
m68k_020fbe_end:
.org 0x20FC0
m68k_020fc0:
        btst.b #0x4,0xf603:w
m68k_020fc0_end:
.org 0x20FC6
m68k_020fc6:
        beq.b (. + 26)
m68k_020fc6_end:
.org 0x20FC8
m68k_020fc8:
        move.w 0xf612:w,0xf38a:w
m68k_020fc8_end:
.org 0x20FCE
m68k_020fce:
        move.w #0x10,0xf3b0:w
m68k_020fce_end:
.org 0x20FD4
m68k_020fd4:
        move.w #0x405,0xf612:w
m68k_020fd4_end:
.org 0x20FDA
m68k_020fda:
        move.w #0x2,0xf362:w
m68k_020fda_end:
.org 0x20FE0
m68k_020fe0:
        rts
m68k_020fe0_end:
.org 0x20FE2
m68k_020fe2:
        bsr.w (. + -31464)
m68k_020fe2_end:
.org 0x20FE6
m68k_020fe6:
        bsr.w (. + -904)
m68k_020fe6_end:
.org 0x20FEA
m68k_020fea:
        bsr.w (. + -720)
m68k_020fea_end:
.org 0x20FEE
m68k_020fee:
        bsr.w (. + -638)
m68k_020fee_end:
.org 0x20FF2
m68k_020ff2:
        btst.b #0x5,0xf603:w
m68k_020ff2_end:
.org 0x20FF8
m68k_020ff8:
        beq.b (. + 18)
m68k_020ff8_end:
.org 0x20FFA
m68k_020ffa:
        move.w #0xac,%d0
m68k_020ffa_end:
.org 0x20FFE
m68k_020ffe:
        jsr 0x808a:l
m68k_020ffe_end:
.org 0x21004
m68k_021004:
        addq.w #0x1,0xf362:w
m68k_021004_end:
.org 0x21008
m68k_021008:
        bra.b (. + 14)
m68k_021008_end:
.org 0x2100A
m68k_02100a:
        btst.b #0x4,0xf603:w
m68k_02100a_end:
.org 0x21010
m68k_021010:
        beq.b (. + 6)
m68k_021010_end:
.org 0x21012
m68k_021012:
        subq.w #0x1,0xf362:w
m68k_021012_end:
.org 0x21016
m68k_021016:
        rts
m68k_021016_end:
.org 0x21018
m68k_021018:
        bsr.w (. + 84)
m68k_021018_end:
.org 0x2101C
m68k_02101c:
        bsr.w (. + 268)
m68k_02101c_end:
.org 0x21020
m68k_021020:
        bsr.w (. + 310)
m68k_021020_end:
.org 0x21024
m68k_021024:
        lea.l -644(%pc),%a0
m68k_021024_end:
.org 0x21028
m68k_021028:
        move.l #0xc000000c,%d0
m68k_021028_end:
.org 0x2102E
m68k_02102e:
        move.w #0x6,%d1
m68k_02102e_end:
.org 0x21032
m68k_021032:
        move.w #0xc19c,%d2
m68k_021032_end:
.org 0x21036
m68k_021036:
        jsr 0x26bfa:l
m68k_021036_end:
.org 0x2103C
m68k_02103c:
        lea.l -668(%pc),%a0
m68k_02103c_end:
.org 0x21040
m68k_021040:
        move.l #0xc000000c,%d0
m68k_021040_end:
.org 0x21046
m68k_021046:
        move.w #0x7,%d1
m68k_021046_end:
.org 0x2104A
m68k_02104a:
        move.w #0xc51c,%d2
m68k_02104a_end:
.org 0x2104E
m68k_02104e:
        jsr 0x26bfa:l
m68k_02104e_end:
.org 0x21054
m68k_021054:
        move.w 0xf612:w,0xf38a:w
m68k_021054_end:
.org 0x2105A
m68k_02105a:
        move.w #0x15,0xf3b0:w
m68k_02105a_end:
.org 0x21060
m68k_021060:
        move.w #0x406,0xf612:w
m68k_021060_end:
.org 0x21066
m68k_021066:
        clr.w 0xf36a:w
m68k_021066_end:
.org 0x2106A
m68k_02106a:
        rts
m68k_02106a_end:
.org 0x2106C
m68k_02106c:
        lea.l 0xc300:w,%a1
m68k_02106c_end:
.org 0x21070
m68k_021070:
        move.w 0xf3a6:w,%d7
m68k_021070_end:
.org 0x21074
m68k_021074:
        cmpi.b #0x5a,(%a1, %d7.w)
m68k_021074_end:
.org 0x2107A
m68k_02107a:
        bcc.w (. + 152)
m68k_02107a_end:
.org 0x2107E
m68k_02107e:
        lea.l 0xc700:w,%a0
m68k_02107e_end:
.org 0x21082
m68k_021082:
        clr.w %d0
m68k_021082_end:
.org 0x21084
m68k_021084:
        move.b (%a0, %d7.w),%d0
m68k_021084_end:
.org 0x21088
m68k_021088:
        andi.w #0x7,%d0
m68k_021088_end:
.org 0x2108C
m68k_02108c:
        lsl.w #0x1,%d0
m68k_02108c_end:
.org 0x2108E
m68k_02108e:
        lea.l 132(%pc),%a2
m68k_02108e_end:
.org 0x21092
m68k_021092:
        nop
m68k_021092_end:
.org 0x21094
m68k_021094:
        move.w (%a2, %d0.w),%d0
m68k_021094_end:
.org 0x21098
m68k_021098:
        move.l 0xaff4:w,%d1
m68k_021098_end:
.org 0x2109C
m68k_02109c:
        divu.w %d0,%d1
m68k_02109c_end:
.org 0x2109E
m68k_02109e:
        move.l 0xf39e:w,%d2
m68k_02109e_end:
.org 0x210A2
m68k_0210a2:
        add.l 0xf3ba:w,%d2
m68k_0210a2_end:
.org 0x210A6
m68k_0210a6:
        mulu.w #0xa,%d2
m68k_0210a6_end:
.org 0x210AA
m68k_0210aa:
        divu.w %d1,%d2
m68k_0210aa_end:
.org 0x210AC
m68k_0210ac:
        jsr 0x83d4:l
m68k_0210ac_end:
.org 0x210B2
m68k_0210b2:
        andi.l #0xffff,%d0
m68k_0210b2_end:
.org 0x210B8
m68k_0210b8:
        move.l %d0,%d1
m68k_0210b8_end:
.org 0x210BA
m68k_0210ba:
        lsl.l #0x1,%d0
m68k_0210ba_end:
.org 0x210BC
m68k_0210bc:
        add.l %d1,%d0
m68k_0210bc_end:
.org 0x210BE
m68k_0210be:
        lsl.l #0x1,%d0
m68k_0210be_end:
.org 0x210C0
m68k_0210c0:
        swap %d0
m68k_0210c0_end:
.org 0x210C2
m68k_0210c2:
        clr.w %d1
m68k_0210c2_end:
.org 0x210C4
m68k_0210c4:
        cmpi.w #0x5,%d2
m68k_0210c4_end:
.org 0x210C8
m68k_0210c8:
        bls.w (. + 36)
m68k_0210c8_end:
.org 0x210CC
m68k_0210cc:
        addq.w #0x2,%d1
m68k_0210cc_end:
.org 0x210CE
m68k_0210ce:
        cmpi.w #0x8,%d2
m68k_0210ce_end:
.org 0x210D2
m68k_0210d2:
        bls.w (. + 26)
m68k_0210d2_end:
.org 0x210D6
m68k_0210d6:
        addq.w #0x2,%d1
m68k_0210d6_end:
.org 0x210D8
m68k_0210d8:
        cmpi.w #0xc,%d2
m68k_0210d8_end:
.org 0x210DC
m68k_0210dc:
        bls.w (. + 16)
m68k_0210dc_end:
.org 0x210E0
m68k_0210e0:
        addq.w #0x2,%d1
m68k_0210e0_end:
.org 0x210E2
m68k_0210e2:
        cmpi.w #0xf,%d2
m68k_0210e2_end:
.org 0x210E6
m68k_0210e6:
        bls.w (. + 6)
m68k_0210e6_end:
.org 0x210EA
m68k_0210ea:
        addq.w #0x2,%d1
m68k_0210ea_end:
.org 0x210EC
m68k_0210ec:
        move.w 48(%pc, %d1.w),%d1
m68k_0210ec_end:
.org 0x210F0
m68k_0210f0:
        beq.w (. + 34)
m68k_0210f0_end:
.org 0x210F4
m68k_0210f4:
        add.w %d0,%d1
m68k_0210f4_end:
.org 0x210F6
m68k_0210f6:
        clr.w %d2
m68k_0210f6_end:
.org 0x210F8
m68k_0210f8:
        move.b (%a1, %d7.w),%d2
m68k_0210f8_end:
.org 0x210FC
m68k_0210fc:
        add.w %d1,%d2
m68k_0210fc_end:
.org 0x210FE
m68k_0210fe:
        bpl.w (. + 6)
m68k_0210fe_end:
.org 0x21102
m68k_021102:
        clr.w %d2
m68k_021102_end:
.org 0x21104
m68k_021104:
        cmpi.w #0x64,%d2
m68k_021104_end:
.org 0x21108
m68k_021108:
        bls.b (. + 6)
m68k_021108_end:
.org 0x2110A
m68k_02110a:
        move.w #0x64,%d2
m68k_02110a_end:
.org 0x2110E
m68k_02110e:
        move.b %d2,(%a1, %d7.w)
m68k_02110e_end:
.org 0x21112
m68k_021112:
        rts
m68k_021112_end:
.org 0x21128
m68k_021128:
        btst.b #0x1,0xf6d7:w
m68k_021128_end:
.org 0x2112E
m68k_02112e:
        bne.b (. + 14)
m68k_02112e_end:
.org 0x21130
m68k_021130:
        lea.l 0xf696:w,%a0
m68k_021130_end:
.org 0x21134
m68k_021134:
        lea.l 0xf69e:w,%a1
m68k_021134_end:
.org 0x21138
m68k_021138:
        bra.w (. + 12)
m68k_021138_end:
.org 0x2113C
m68k_02113c:
        lea.l 0xf69a:w,%a0
m68k_02113c_end:
.org 0x21140
m68k_021140:
        lea.l 0xf6a2:w,%a1
m68k_021140_end:
.org 0x21144
m68k_021144:
        move.l (%a0),%d0
m68k_021144_end:
.org 0x21146
m68k_021146:
        sub.l 0xf39e:w,%d0
m68k_021146_end:
.org 0x2114A
m68k_02114a:
        move.l %d0,(%a0)
m68k_02114a_end:
.org 0x2114C
m68k_02114c:
        move.l (%a1),%d0
m68k_02114c_end:
.org 0x2114E
m68k_02114e:
        sub.l 0xf3ba:w,%d0
m68k_02114e_end:
.org 0x21152
m68k_021152:
        move.l %d0,(%a1)
m68k_021152_end:
.org 0x21154
m68k_021154:
        rts
m68k_021154_end:
.org 0x21156
m68k_021156:
        move.w 0xf3a6:w,%d0
m68k_021156_end:
.org 0x2115A
m68k_02115a:
        lea.l 0xf500:w,%a0
m68k_02115a_end:
.org 0x2115E
m68k_02115e:
        move.w (%a0)+,%d1
m68k_02115e_end:
.org 0x21160
m68k_021160:
        andi.w #0xff,%d1
m68k_021160_end:
.org 0x21164
m68k_021164:
        cmp.w %d0,%d1
m68k_021164_end:
.org 0x21166
m68k_021166:
        bne.b (. + -8)
m68k_021166_end:
.org 0x21168
m68k_021168:
        move.w (%a0)+,-0x4(%a0)
m68k_021168_end:
.org 0x2116C
m68k_02116c:
        bpl.b (. + -4)
m68k_02116c_end:
.org 0x2116E
m68k_02116e:
        subq.w #0x1,0xf636:w
m68k_02116e_end:
.org 0x21172
m68k_021172:
        rts
m68k_021172_end:
.org 0x21174
m68k_021174:
        addq.w #0x1,0xf362:w
m68k_021174_end:
.org 0x21178
m68k_021178:
        move.w 0xf3a6:w,0xf3d0:w
m68k_021178_end:
.org 0x2117E
m68k_02117e:
        move.w #0x124,%d0
m68k_02117e_end:
.org 0x21182
m68k_021182:
        move.w %d0,0xaf80:w
m68k_021182_end:
.org 0x21186
m68k_021186:
        jsr 0x676f2:l
m68k_021186_end:
.org 0x2118C
m68k_02118c:
        move.w #0x1,0xf652:w
m68k_02118c_end:
.org 0x21192
m68k_021192:
        rts
m68k_021192_end:
.org 0x21194
m68k_021194:
        btst.b #0x5,0xf603:w
m68k_021194_end:
.org 0x2119A
m68k_02119a:
        beq.w (. + 62)
m68k_02119a_end:
.org 0x2119E
m68k_02119e:
        tst.w 0xf500:w
m68k_02119e_end:
.org 0x211A2
m68k_0211a2:
        bmi.b (. + 50)
m68k_0211a2_end:
.org 0x211A4
m68k_0211a4:
        move.w 0xf612:w,0xf38a:w
m68k_0211a4_end:
.org 0x211AA
m68k_0211aa:
        move.w #0x10,0xf3b0:w
m68k_0211aa_end:
.org 0x211B0
m68k_0211b0:
        clr.w 0xf378:w
m68k_0211b0_end:
.org 0x211B4
m68k_0211b4:
        clr.w 0xf658:w
m68k_0211b4_end:
.org 0x211B8
m68k_0211b8:
        move.w #0x405,0xf612:w
m68k_0211b8_end:
.org 0x211BE
m68k_0211be:
        clr.w 0xf362:w
m68k_0211be_end:
.org 0x211C2
m68k_0211c2:
        move.w #0x123,%d0
m68k_0211c2_end:
.org 0x211C6
m68k_0211c6:
        move.w %d0,0xaf80:w
m68k_0211c6_end:
.org 0x211CA
m68k_0211ca:
        jsr 0x676f2:l
m68k_0211ca_end:
.org 0x211D0
m68k_0211d0:
        bra.w (. + 8)
m68k_0211d0_end:
.org 0x211D4
m68k_0211d4:
        addq.w #0x1,0xf362:w
m68k_0211d4_end:
.org 0x211D8
m68k_0211d8:
        rts
m68k_0211d8_end:
.org 0x211DA
m68k_0211da:
        bsr.w (. + 74)
m68k_0211da_end:
.org 0x211DE
m68k_0211de:
        move.w %d1,%d0
m68k_0211de_end:
.org 0x211E0
m68k_0211e0:
        add.w %d3,%d0
m68k_0211e0_end:
.org 0x211E2
m68k_0211e2:
        cmpi.w #0xa,%d0
m68k_0211e2_end:
.org 0x211E6
m68k_0211e6:
        bls.w (. + 54)
m68k_0211e6_end:
.org 0x211EA
m68k_0211ea:
        move.w %d1,0xf636:w
m68k_0211ea_end:
.org 0x211EE
m68k_0211ee:
        move.w %d3,0xf712:w
m68k_0211ee_end:
.org 0x211F2
m68k_0211f2:
        addq.w #0x1,0xf362:w
m68k_0211f2_end:
.org 0x211F6
m68k_0211f6:
        clr.w 0xf378:w
m68k_0211f6_end:
.org 0x211FA
m68k_0211fa:
        clr.w 0xf658:w
m68k_0211fa_end:
.org 0x211FE
m68k_0211fe:
        move.l #0xabd12,0xf6c0:w
m68k_0211fe_end:
.org 0x21206
m68k_021206:
        clr.w 0xf36a:w
m68k_021206_end:
.org 0x2120A
m68k_02120a:
        bsr.w (. + 132)
m68k_02120a_end:
.org 0x2120E
m68k_02120e:
        move.w %d0,0xaf80:w
m68k_02120e_end:
.org 0x21212
m68k_021212:
        jsr 0x676f2:l
m68k_021212_end:
.org 0x21218
m68k_021218:
        bra.w (. + 10)
m68k_021218_end:
.org 0x2121C
m68k_02121c:
        move.w #0x1c,0xf362:w
m68k_02121c_end:
.org 0x21222
m68k_021222:
        rts
m68k_021222_end:
.org 0x21224
m68k_021224:
        btst.b #0x1,0xf6d7:w
m68k_021224_end:
.org 0x2122A
m68k_02122a:
        bne.b (. + 18)
m68k_02122a_end:
.org 0x2122C
m68k_02122c:
        lea.l 0xa550:w,%a0
m68k_02122c_end:
.org 0x21230
m68k_021230:
        lea.l 0xa5ce:w,%a3
m68k_021230_end:
.org 0x21234
m68k_021234:
        move.w 0xf68c:w,%d2
m68k_021234_end:
.org 0x21238
m68k_021238:
        bra.w (. + 16)
m68k_021238_end:
.org 0x2123C
m68k_02123c:
        lea.l 0xa5a4:w,%a0
m68k_02123c_end:
.org 0x21240
m68k_021240:
        lea.l 0xa57a:w,%a3
m68k_021240_end:
.org 0x21244
m68k_021244:
        move.w 0xf68e:w,%d2
m68k_021244_end:
.org 0x21248
m68k_021248:
        lsl.w #0x1,%d2
m68k_021248_end:
.org 0x2124A
m68k_02124a:
        lea.l 0xe640:w,%a2
m68k_02124a_end:
.org 0x2124E
m68k_02124e:
        move.w (%a2, %d2.w),%d2
m68k_02124e_end:
.org 0x21252
m68k_021252:
        lea.l 0xaf56:w,%a1
m68k_021252_end:
.org 0x21256
m68k_021256:
        clr.w %d1
m68k_021256_end:
.org 0x21258
m68k_021258:
        clr.w %d3
m68k_021258_end:
.org 0x2125A
m68k_02125a:
        move.w (%a0)+,%d0
m68k_02125a_end:
.org 0x2125C
m68k_02125c:
        bmi.b (. + 20)
m68k_02125c_end:
.org 0x2125E
m68k_02125e:
        andi.w #0xff,%d0
m68k_02125e_end:
.org 0x21262
m68k_021262:
        cmp.w %d2,%d0
m68k_021262_end:
.org 0x21264
m68k_021264:
        beq.b (. + 8)
m68k_021264_end:
.org 0x21266
m68k_021266:
        addq.w #0x1,%d1
m68k_021266_end:
.org 0x21268
m68k_021268:
        move.w %d0,(%a1)+
m68k_021268_end:
.org 0x2126A
m68k_02126a:
        bra.b (. + -16)
m68k_02126a_end:
.org 0x2126C
m68k_02126c:
        addq.w #0x1,%d3
m68k_02126c_end:
.org 0x2126E
m68k_02126e:
        bra.b (. + -20)
m68k_02126e_end:
.org 0x21270
m68k_021270:
        lea.l 0xaf28:w,%a0
m68k_021270_end:
.org 0x21274
m68k_021274:
        move.w (%a0)+,%d0
m68k_021274_end:
.org 0x21276
m68k_021276:
        bmi.b (. + 12)
m68k_021276_end:
.org 0x21278
m68k_021278:
        andi.w #0xff,%d0
m68k_021278_end:
.org 0x2127C
m68k_02127c:
        move.w %d0,(%a1)+
m68k_02127c_end:
.org 0x2127E
m68k_02127e:
        addq.w #0x1,%d1
m68k_02127e_end:
.org 0x21280
m68k_021280:
        bra.b (. + -12)
m68k_021280_end:
.org 0x21282
m68k_021282:
        move.w (%a3)+,(%a1)+
m68k_021282_end:
.org 0x21284
m68k_021284:
        bmi.w (. + 8)
m68k_021284_end:
.org 0x21288
m68k_021288:
        addq.w #0x1,%d1
m68k_021288_end:
.org 0x2128A
m68k_02128a:
        bra.b (. + -8)
m68k_02128a_end:
.org 0x2128C
m68k_02128c:
        rts
m68k_02128c_end:
.org 0x2128E
m68k_02128e:
        btst.b #0x1,0xf6d7:w
m68k_02128e_end:
.org 0x21294
m68k_021294:
        bne.w (. + 12)
m68k_021294_end:
.org 0x21298
m68k_021298:
        move.w 0xf68c:w,%d0
m68k_021298_end:
.org 0x2129C
m68k_02129c:
        bra.w (. + 8)
m68k_02129c_end:
.org 0x212A0
m68k_0212a0:
        move.w 0xf68e:w,%d0
m68k_0212a0_end:
.org 0x212A4
m68k_0212a4:
        move.w 0xf68a:w,%d1
m68k_0212a4_end:
.org 0x212A8
m68k_0212a8:
        lea.l 0xf428:w,%a0
m68k_0212a8_end:
.org 0x212AC
m68k_0212ac:
        move.w #0x27,%d2
m68k_0212ac_end:
.org 0x212B0
m68k_0212b0:
        move.b (%a0, %d2.w),%d3
m68k_0212b0_end:
.org 0x212B4
m68k_0212b4:
        cmp.b %d0,%d3
m68k_0212b4_end:
.org 0x212B6
m68k_0212b6:
        bne.w (. + 10)
m68k_0212b6_end:
.org 0x212BA
m68k_0212ba:
        cmp.b %d1,%d2
m68k_0212ba_end:
.org 0x212BC
m68k_0212bc:
        bne.w (. + 20)
m68k_0212bc_end:
.org 0x212C0
m68k_0212c0:
        dbra %d2,(. + -16)
m68k_0212c0_end:
.org 0x212C4
m68k_0212c4:
        move.w #0x125,%d0
m68k_0212c4_end:
.org 0x212C8
m68k_0212c8:
        ori.w #0x1,%sr
m68k_0212c8_end:
.org 0x212CC
m68k_0212cc:
        bra.w (. + 12)
m68k_0212cc_end:
.org 0x212D0
m68k_0212d0:
        move.w #0x125,%d0
m68k_0212d0_end:
.org 0x212D4
m68k_0212d4:
        andi.w #0xfffe,%sr
m68k_0212d4_end:
.org 0x212D8
m68k_0212d8:
        rts
m68k_0212d8_end:
.org 0x212DA
m68k_0212da:
        cmpi.w #0x9,0xf36a:w
m68k_0212da_end:
.org 0x212E0
m68k_0212e0:
        bcc.w (. + 60)
m68k_0212e0_end:
.org 0x212E4
m68k_0212e4:
        tst.w 0xf36a:w
m68k_0212e4_end:
.org 0x212E8
m68k_0212e8:
        bne.w (. + 10)
m68k_0212e8_end:
.org 0x212EC
m68k_0212ec:
        move.w #0xac,0xf600:w
m68k_0212ec_end:
.org 0x212F2
m68k_0212f2:
        movea.l 0xf6c0:w,%a0
m68k_0212f2_end:
.org 0x212F6
m68k_0212f6:
        move.l #0xc000000a,%d0
m68k_0212f6_end:
.org 0x212FC
m68k_0212fc:
        move.w #0x2,%d1
m68k_0212fc_end:
.org 0x21300
m68k_021300:
        move.w 0xf36a:w,%d2
m68k_021300_end:
.org 0x21304
m68k_021304:
        lsl.w #0x8,%d2
m68k_021304_end:
.org 0x21306
m68k_021306:
        addi.w #0xc0b6,%d2
m68k_021306_end:
.org 0x2130A
m68k_02130a:
        jsr 0x26bfa:l
m68k_02130a_end:
.org 0x21310
m68k_021310:
        move.l %a0,0xf6c0:w
m68k_021310_end:
.org 0x21314
m68k_021314:
        addq.w #0x1,0xf36a:w
m68k_021314_end:
.org 0x21318
m68k_021318:
        bra.w (. + 12)
m68k_021318_end:
.org 0x2131C
m68k_02131c:
        addq.w #0x1,0xf362:w
m68k_02131c_end:
.org 0x21320
m68k_021320:
        clr.w 0xf684:w
m68k_021320_end:
.org 0x21324
m68k_021324:
        rts
m68k_021324_end:
.org 0x21326
m68k_021326:
        bsr.w (. + 138)
m68k_021326_end:
.org 0x2132A
m68k_02132a:
        bsr.w (. + 258)
m68k_02132a_end:
.org 0x2132E
m68k_02132e:
        btst.b #0x5,0xf603:w
m68k_02132e_end:
.org 0x21334
m68k_021334:
        beq.w (. + 122)
m68k_021334_end:
.org 0x21338
m68k_021338:
        move.w #0xac,%d0
m68k_021338_end:
.org 0x2133C
m68k_02133c:
        jsr 0x808a:l
m68k_02133c_end:
.org 0x21342
m68k_021342:
        move.w 0xf378:w,%d0
m68k_021342_end:
.org 0x21346
m68k_021346:
        cmp.w 0xf636:w,%d0
m68k_021346_end:
.org 0x2134A
m68k_02134a:
        beq.w (. + 76)
m68k_02134a_end:
.org 0x2134E
m68k_02134e:
        move.w #0xac,0xf600:w
m68k_02134e_end:
.org 0x21354
m68k_021354:
        lsl.w #0x1,%d0
m68k_021354_end:
.org 0x21356
m68k_021356:
        lea.l 0xaf56:w,%a0
m68k_021356_end:
.org 0x2135A
m68k_02135a:
        move.w (%a0, %d0.w),%d1
m68k_02135a_end:
.org 0x2135E
m68k_02135e:
        bchg.l #0xe,%d1
m68k_02135e_end:
.org 0x21362
m68k_021362:
        bne.w (. + 40)
m68k_021362_end:
.org 0x21366
m68k_021366:
        cmpi.w #0xa,0xf684:w
m68k_021366_end:
.org 0x2136C
m68k_02136c:
        bcc.w (. + 22)
m68k_02136c_end:
.org 0x21370
m68k_021370:
        addq.w #0x1,0xf684:w
m68k_021370_end:
.org 0x21374
m68k_021374:
        move.w %d1,(%a0, %d0.w)
m68k_021374_end:
.org 0x21378
m68k_021378:
        jsr 0x18848:l
m68k_021378_end:
.org 0x2137E
m68k_02137e:
        bra.w (. + 48)
m68k_02137e_end:
.org 0x21382
m68k_021382:
        bchg.l #0xe,%d1
m68k_021382_end:
.org 0x21386
m68k_021386:
        bra.w (. + 40)
m68k_021386_end:
.org 0x2138A
m68k_02138a:
        subq.w #0x1,0xf684:w
m68k_02138a_end:
.org 0x2138E
m68k_02138e:
        move.w %d1,(%a0, %d0.w)
m68k_02138e_end:
.org 0x21392
m68k_021392:
        bra.w (. + 28)
m68k_021392_end:
.org 0x21396
m68k_021396:
        move.w 0xf636:w,%d0
m68k_021396_end:
.org 0x2139A
m68k_02139a:
        sub.w 0xf684:w,%d0
m68k_02139a_end:
.org 0x2139E
m68k_02139e:
        add.w 0xf712:w,%d0
m68k_02139e_end:
.org 0x213A2
m68k_0213a2:
        cmpi.w #0xa,%d0
m68k_0213a2_end:
.org 0x213A6
m68k_0213a6:
        bhi.w (. + 8)
m68k_0213a6_end:
.org 0x213AA
m68k_0213aa:
        addq.w #0x1,0xf362:w
m68k_0213aa_end:
.org 0x213AE
m68k_0213ae:
        rts
m68k_0213ae_end:
.org 0x213B0
m68k_0213b0:
        move.b 0xf602:w,%d0
m68k_0213b0_end:
.org 0x213B4
m68k_0213b4:
        andi.w #0x3,%d0
m68k_0213b4_end:
.org 0x213B8
m68k_0213b8:
        beq.w (. + 108)
m68k_0213b8_end:
.org 0x213BC
m68k_0213bc:
        subq.w #0x1,0xf608:w
m68k_0213bc_end:
.org 0x213C0
m68k_0213c0:
        bne.w (. + 106)
m68k_0213c0_end:
.org 0x213C4
m68k_0213c4:
        move.w #0xc,0xf608:w
m68k_0213c4_end:
.org 0x213CA
m68k_0213ca:
        btst.l #0x1,%d0
m68k_0213ca_end:
.org 0x213CE
m68k_0213ce:
        bne.w (. + 20)
m68k_0213ce_end:
.org 0x213D2
m68k_0213d2:
        tst.w 0xf378:w
m68k_0213d2_end:
.org 0x213D6
m68k_0213d6:
        beq.w (. + 84)
m68k_0213d6_end:
.org 0x213DA
m68k_0213da:
        subq.w #0x1,0xf378:w
m68k_0213da_end:
.org 0x213DE
m68k_0213de:
        bra.w (. + 20)
m68k_0213de_end:
.org 0x213E2
m68k_0213e2:
        move.w 0xf378:w,%d0
m68k_0213e2_end:
.org 0x213E6
m68k_0213e6:
        cmp.w 0xf636:w,%d0
m68k_0213e6_end:
.org 0x213EA
m68k_0213ea:
        beq.w (. + 64)
m68k_0213ea_end:
.org 0x213EE
m68k_0213ee:
        addq.w #0x1,0xf378:w
m68k_0213ee_end:
.org 0x213F2
m68k_0213f2:
        move.w 0xf378:w,%d0
m68k_0213f2_end:
.org 0x213F6
m68k_0213f6:
        subq.w #0x2,%d0
m68k_0213f6_end:
.org 0x213F8
m68k_0213f8:
        bcc.b (. + 4)
m68k_0213f8_end:
.org 0x213FA
m68k_0213fa:
        clr.w %d0
m68k_0213fa_end:
.org 0x213FC
m68k_0213fc:
        move.w 0xf636:w,%d1
m68k_0213fc_end:
.org 0x21400
m68k_021400:
        subq.w #0x4,%d1
m68k_021400_end:
.org 0x21402
m68k_021402:
        bcc.w (. + 6)
m68k_021402_end:
.org 0x21406
m68k_021406:
        clr.w %d1
m68k_021406_end:
.org 0x21408
m68k_021408:
        cmp.w %d1,%d0
m68k_021408_end:
.org 0x2140A
m68k_02140a:
        bls.w (. + 6)
m68k_02140a_end:
.org 0x2140E
m68k_02140e:
        move.w %d1,%d0
m68k_02140e_end:
.org 0x21410
m68k_021410:
        cmp.w 0xf658:w,%d0
m68k_021410_end:
.org 0x21414
m68k_021414:
        beq.b (. + 22)
m68k_021414_end:
.org 0x21416
m68k_021416:
        move.w %d0,0xf658:w
m68k_021416_end:
.org 0x2141A
m68k_02141a:
        move.w #0xac,0xf600:w
m68k_02141a_end:
.org 0x21420
m68k_021420:
        bra.w (. + 10)
m68k_021420_end:
.org 0x21424
m68k_021424:
        move.w #0x1,0xf608:w
m68k_021424_end:
.org 0x2142A
m68k_02142a:
        rts
m68k_02142a_end:
.org 0x2142C
m68k_02142c:
        move.b 0xf602:w,%d0
m68k_02142c_end:
.org 0x21430
m68k_021430:
        andi.w #0x3,%d0
m68k_021430_end:
.org 0x21434
m68k_021434:
        bne.w (. + 14)
m68k_021434_end:
.org 0x21438
m68k_021438:
        btst.b #0x3,0xf321:w
m68k_021438_end:
.org 0x2143E
m68k_02143e:
        bne.w (. + 42)
m68k_02143e_end:
.org 0x21442
m68k_021442:
        lea.l 38(%pc),%a0
m68k_021442_end:
.org 0x21446
m68k_021446:
        nop
m68k_021446_end:
.org 0x21448
m68k_021448:
        move.w 0xf378:w,%d0
m68k_021448_end:
.org 0x2144C
m68k_02144c:
        sub.w 0xf658:w,%d0
m68k_02144c_end:
.org 0x21450
m68k_021450:
        move.w %d0,%d2
m68k_021450_end:
.org 0x21452
m68k_021452:
        lsl.w #0x1,%d0
m68k_021452_end:
.org 0x21454
m68k_021454:
        add.w %d2,%d0
m68k_021454_end:
.org 0x21456
m68k_021456:
        lsl.w #0x3,%d0
m68k_021456_end:
.org 0x21458
m68k_021458:
        addi.w #0x10,%d0
m68k_021458_end:
.org 0x2145C
m68k_02145c:
        move.w #0xe0,%d1
m68k_02145c_end:
.org 0x21460
m68k_021460:
        clr.w %d2
m68k_021460_end:
.org 0x21462
m68k_021462:
        jsr 0xac08:l
m68k_021462_end:
.org 0x21468
m68k_021468:
        rts
m68k_021468_end:
.org 0x214CC
m68k_0214cc:
        bsr.w (. + -574)
m68k_0214cc_end:
.org 0x214D0
m68k_0214d0:
        bcs.w (. + 62)
m68k_0214d0_end:
.org 0x214D4
m68k_0214d4:
        bsr.w (. + 64)
m68k_0214d4_end:
.org 0x214D8
m68k_0214d8:
        bsr.w (. + 238)
m68k_0214d8_end:
.org 0x214DC
m68k_0214dc:
        addq.w #0x1,0xf362:w
m68k_0214dc_end:
.org 0x214E0
m68k_0214e0:
        lea.l 0xaf56:w,%a0
m68k_0214e0_end:
.org 0x214E4
m68k_0214e4:
        move.w (%a0)+,%d0
m68k_0214e4_end:
.org 0x214E6
m68k_0214e6:
        btst.l #0xe,%d0
m68k_0214e6_end:
.org 0x214EA
m68k_0214ea:
        beq.b (. + -6)
m68k_0214ea_end:
.org 0x214EC
m68k_0214ec:
        andi.w #0xff,%d0
m68k_0214ec_end:
.org 0x214F0
m68k_0214f0:
        move.w %d0,0xf3d0:w
m68k_0214f0_end:
.org 0x214F4
m68k_0214f4:
        move.w 0xf612:w,0xf38a:w
m68k_0214f4_end:
.org 0x214FA
m68k_0214fa:
        move.w #0x1e,0xf3b0:w
m68k_0214fa_end:
.org 0x21500
m68k_021500:
        move.w #0x406,0xf612:w
m68k_021500_end:
.org 0x21506
m68k_021506:
        clr.w 0xf36a:w
m68k_021506_end:
.org 0x2150A
m68k_02150a:
        bra.w (. + 8)
m68k_02150a_end:
.org 0x2150E
m68k_02150e:
        bsr.w (. + 144)
m68k_02150e_end:
.org 0x21512
m68k_021512:
        rts
m68k_021512_end:
.org 0x2159E
m68k_02159e:
        lea.l 0xaf56:w,%a0
m68k_02159e_end:
.org 0x215A2
m68k_0215a2:
        lea.l 0xcc00:w,%a1
m68k_0215a2_end:
.org 0x215A6
m68k_0215a6:
        move.w 0xf68a:w,%d0
m68k_0215a6_end:
.org 0x215AA
m68k_0215aa:
        bset.l #0x7,%d0
m68k_0215aa_end:
.org 0x215AE
m68k_0215ae:
        move.w (%a0)+,%d1
m68k_0215ae_end:
.org 0x215B0
m68k_0215b0:
        bmi.w (. + 20)
m68k_0215b0_end:
.org 0x215B4
m68k_0215b4:
        btst.l #0xe,%d1
m68k_0215b4_end:
.org 0x215B8
m68k_0215b8:
        beq.b (. + -10)
m68k_0215b8_end:
.org 0x215BA
m68k_0215ba:
        andi.w #0xff,%d1
m68k_0215ba_end:
.org 0x215BE
m68k_0215be:
        move.b %d0,(%a1, %d1.w)
m68k_0215be_end:
.org 0x215C2
m68k_0215c2:
        bra.b (. + -20)
m68k_0215c2_end:
.org 0x215C4
m68k_0215c4:
        rts
m68k_0215c4_end:
.org 0x215C6
m68k_0215c6:
        btst.b #0x1,0xf6d7:w
m68k_0215c6_end:
.org 0x215CC
m68k_0215cc:
        bne.w (. + 16)
m68k_0215cc_end:
.org 0x215D0
m68k_0215d0:
        move.l 0xf696:w,%d0
m68k_0215d0_end:
.org 0x215D4
m68k_0215d4:
        move.l 0xf69e:w,%d1
m68k_0215d4_end:
.org 0x215D8
m68k_0215d8:
        bra.w (. + 12)
m68k_0215d8_end:
.org 0x215DC
m68k_0215dc:
        move.l 0xf69a:w,%d0
m68k_0215dc_end:
.org 0x215E0
m68k_0215e0:
        move.l 0xf6a2:w,%d1
m68k_0215e0_end:
.org 0x215E4
m68k_0215e4:
        lsr.l #0x1,%d0
m68k_0215e4_end:
.org 0x215E6
m68k_0215e6:
        lsr.l #0x1,%d1
m68k_0215e6_end:
.org 0x215E8
m68k_0215e8:
        lea.l 0xc800:w,%a1
m68k_0215e8_end:
.org 0x215EC
m68k_0215ec:
        moveq #0,%d2
m68k_0215ec_end:
.org 0x215EE
m68k_0215ee:
        clr.w %d3
m68k_0215ee_end:
.org 0x215F0
m68k_0215f0:
        move.b (%a0),%d3
m68k_0215f0_end:
.org 0x215F2
m68k_0215f2:
        subq.w #0x1,%d3
m68k_0215f2_end:
.org 0x215F4
m68k_0215f4:
        clr.w %d4
m68k_0215f4_end:
.org 0x215F6
m68k_0215f6:
        move.b 0xd(%a0, %d3.w),%d4
m68k_0215f6_end:
.org 0x215FA
m68k_0215fa:
        lsl.w #0x2,%d4
m68k_0215fa_end:
.org 0x215FC
m68k_0215fc:
        add.l (%a1, %d4.w),%d2
m68k_0215fc_end:
.org 0x21600
m68k_021600:
        addi.l #0x64,%d2
m68k_021600_end:
.org 0x21606
m68k_021606:
        dbra %d3,(. + -18)
m68k_021606_end:
.org 0x2160A
m68k_02160a:
        divu.w #0xa,%d2
m68k_02160a_end:
.org 0x2160E
m68k_02160e:
        andi.l #0xffff,%d2
m68k_02160e_end:
.org 0x21614
m68k_021614:
        move.l %d2,%d3
m68k_021614_end:
.org 0x21616
m68k_021616:
        lsl.l #0x1,%d2
m68k_021616_end:
.org 0x21618
m68k_021618:
        add.l %d3,%d2
m68k_021618_end:
.org 0x2161A
m68k_02161a:
        lsl.l #0x1,%d2
m68k_02161a_end:
.org 0x2161C
m68k_02161c:
        move.w %d2,%d3
m68k_02161c_end:
.org 0x2161E
m68k_02161e:
        cmp.w %d0,%d2
m68k_02161e_end:
.org 0x21620
m68k_021620:
        bls.w (. + 14)
m68k_021620_end:
.org 0x21624
m68k_021624:
        move.l %d0,%d2
m68k_021624_end:
.org 0x21626
m68k_021626:
        lsr.l #0x3,%d2
m68k_021626_end:
.org 0x21628
m68k_021628:
        move.l %d2,%d0
m68k_021628_end:
.org 0x2162A
m68k_02162a:
        lsl.l #0x1,%d2
m68k_02162a_end:
.org 0x2162C
m68k_02162c:
        add.l %d0,%d2
m68k_02162c_end:
.org 0x2162E
m68k_02162e:
        cmp.w %d1,%d3
m68k_02162e_end:
.org 0x21630
m68k_021630:
        bls.w (. + 14)
m68k_021630_end:
.org 0x21634
m68k_021634:
        move.l %d1,%d3
m68k_021634_end:
.org 0x21636
m68k_021636:
        lsr.l #0x3,%d3
m68k_021636_end:
.org 0x21638
m68k_021638:
        move.l %d3,%d0
m68k_021638_end:
.org 0x2163A
m68k_02163a:
        lsl.l #0x1,%d3
m68k_02163a_end:
.org 0x2163C
m68k_02163c:
        add.l %d0,%d3
m68k_02163c_end:
.org 0x2163E
m68k_02163e:
        move.l %d2,%d0
m68k_02163e_end:
.org 0x21640
m68k_021640:
        move.b %d0,0x8(%a0)
m68k_021640_end:
.org 0x21644
m68k_021644:
        lsr.l #0x8,%d0
m68k_021644_end:
.org 0x21646
m68k_021646:
        move.b %d0,0x7(%a0)
m68k_021646_end:
.org 0x2164A
m68k_02164a:
        lsr.l #0x8,%d0
m68k_02164a_end:
.org 0x2164C
m68k_02164c:
        move.b %d0,0x6(%a0)
m68k_02164c_end:
.org 0x21650
m68k_021650:
        lsr.w #0x8,%d0
m68k_021650_end:
.org 0x21652
m68k_021652:
        move.b %d0,0x5(%a0)
m68k_021652_end:
.org 0x21656
m68k_021656:
        move.l %d3,%d0
m68k_021656_end:
.org 0x21658
m68k_021658:
        move.b %d0,0xc(%a0)
m68k_021658_end:
.org 0x2165C
m68k_02165c:
        lsr.l #0x8,%d0
m68k_02165c_end:
.org 0x2165E
m68k_02165e:
        move.b %d0,0xb(%a0)
m68k_02165e_end:
.org 0x21662
m68k_021662:
        lsr.l #0x8,%d0
m68k_021662_end:
.org 0x21664
m68k_021664:
        move.b %d0,0xa(%a0)
m68k_021664_end:
.org 0x21668
m68k_021668:
        lsr.w #0x8,%d0
m68k_021668_end:
.org 0x2166A
m68k_02166a:
        move.b %d0,0x9(%a0)
m68k_02166a_end:
.org 0x2166E
m68k_02166e:
        btst.b #0x1,0xf6d7:w
m68k_02166e_end:
.org 0x21674
m68k_021674:
        bne.w (. + 28)
m68k_021674_end:
.org 0x21678
m68k_021678:
        move.l 0xf696:w,%d0
m68k_021678_end:
.org 0x2167C
m68k_02167c:
        sub.l %d2,%d0
m68k_02167c_end:
.org 0x2167E
m68k_02167e:
        move.l %d0,0xf696:w
m68k_02167e_end:
.org 0x21682
m68k_021682:
        move.l 0xf69e:w,%d0
m68k_021682_end:
.org 0x21686
m68k_021686:
        sub.l %d3,%d0
m68k_021686_end:
.org 0x21688
m68k_021688:
        move.l %d0,0xf69e:w
m68k_021688_end:
.org 0x2168C
m68k_02168c:
        bra.w (. + 24)
m68k_02168c_end:
.org 0x21690
m68k_021690:
        move.l 0xf69a:w,%d0
m68k_021690_end:
.org 0x21694
m68k_021694:
        sub.l %d2,%d0
m68k_021694_end:
.org 0x21696
m68k_021696:
        move.l %d0,0xf69a:w
m68k_021696_end:
.org 0x2169A
m68k_02169a:
        move.l 0xf6a2:w,%d0
m68k_02169a_end:
.org 0x2169E
m68k_02169e:
        sub.l %d3,%d0
m68k_02169e_end:
.org 0x216A0
m68k_0216a0:
        move.l %d0,0xf6a2:w
m68k_0216a0_end:
.org 0x216A4
m68k_0216a4:
        rts
m68k_0216a4_end:
.org 0x216A6
m68k_0216a6:
        btst.b #0x5,0xf603:w
m68k_0216a6_end:
.org 0x216AC
m68k_0216ac:
        beq.w (. + 12)
m68k_0216ac_end:
.org 0x216B0
m68k_0216b0:
        bsr.w (. + 2474)
m68k_0216b0_end:
.org 0x216B4
m68k_0216b4:
        addq.w #0x1,0xf362:w
m68k_0216b4_end:
.org 0x216B8
m68k_0216b8:
        rts
m68k_0216b8_end:
.org 0x216BA
m68k_0216ba:
        addq.w #0x1,0xf362:w
m68k_0216ba_end:
.org 0x216BE
m68k_0216be:
        lea.l 0xf427:w,%a0
m68k_0216be_end:
.org 0x216C2
m68k_0216c2:
        move.w 0xf68a:w,%d2
m68k_0216c2_end:
.org 0x216C6
m68k_0216c6:
        btst.b #0x1,0xf6d7:w
m68k_0216c6_end:
.org 0x216CC
m68k_0216cc:
        bne.w (. + 16)
m68k_0216cc_end:
.org 0x216D0
m68k_0216d0:
        move.w 0xf68c:w,%d0
m68k_0216d0_end:
.org 0x216D4
m68k_0216d4:
        move.w 0xf68e:w,%d1
m68k_0216d4_end:
.org 0x216D8
m68k_0216d8:
        bra.w (. + 12)
m68k_0216d8_end:
.org 0x216DC
m68k_0216dc:
        move.w 0xf68e:w,%d0
m68k_0216dc_end:
.org 0x216E0
m68k_0216e0:
        move.w 0xf68c:w,%d1
m68k_0216e0_end:
.org 0x216E4
m68k_0216e4:
        move.b %d0,(%a0, %d2.w)
m68k_0216e4_end:
.org 0x216E8
m68k_0216e8:
        move.w %d0,0xf376:w
m68k_0216e8_end:
.org 0x216EC
m68k_0216ec:
        lea.l 0xe640:w,%a0
m68k_0216ec_end:
.org 0x216F0
m68k_0216f0:
        lsl.w #0x1,%d1
m68k_0216f0_end:
.org 0x216F2
m68k_0216f2:
        move.w (%a0, %d1.w),0xf3d0:w
m68k_0216f2_end:
.org 0x216F8
m68k_0216f8:
        move.w 0xf68a:w,0xf646:w
m68k_0216f8_end:
.org 0x216FE
m68k_0216fe:
        move.w #0x127,%d0
m68k_0216fe_end:
.org 0x21702
m68k_021702:
        move.w %d0,0xaf80:w
m68k_021702_end:
.org 0x21706
m68k_021706:
        jsr 0x676f2:l
m68k_021706_end:
.org 0x2170C
m68k_02170c:
        jsr 0x2215e:l
m68k_02170c_end:
.org 0x21712
m68k_021712:
        jsr 60(%pc)
m68k_021712_end:
.org 0x21716
m68k_021716:
        nop
m68k_021716_end:
.org 0x21718
m68k_021718:
        bsr.w (. + 18)
m68k_021718_end:
.org 0x2171C
m68k_02171c:
        lea.l 0xea37:w,%a0
m68k_02171c_end:
.org 0x21720
m68k_021720:
        move.w 0xf68a:w,%d0
m68k_021720_end:
.org 0x21724
m68k_021724:
        clr.b (%a0, %d0.w)
m68k_021724_end:
.org 0x21728
m68k_021728:
        rts
m68k_021728_end:
.org 0x2172A
m68k_02172a:
        lea.l 0xa150:w,%a0
m68k_02172a_end:
.org 0x2172E
m68k_02172e:
        lea.l 0xcc00:w,%a1
m68k_02172e_end:
.org 0x21732
m68k_021732:
        move.w #0xff,%d0
m68k_021732_end:
.org 0x21736
m68k_021736:
        move.w 0xf68a:w,%d1
m68k_021736_end:
.org 0x2173A
m68k_02173a:
        cmp.b (%a0, %d0.w),%d1
m68k_02173a_end:
.org 0x2173E
m68k_02173e:
        bne.w (. + 12)
m68k_02173e_end:
.org 0x21742
m68k_021742:
        move.w %d0,%d2
m68k_021742_end:
.org 0x21744
m68k_021744:
        lsl.w #0x2,%d2
m68k_021744_end:
.org 0x21746
m68k_021746:
        clr.l (%a0, %d2.w)
m68k_021746_end:
.org 0x2174A
m68k_02174a:
        dbra %d0,(. + -16)
m68k_02174a_end:
.org 0x2174E
m68k_02174e:
        rts
m68k_02174e_end:
.org 0x21750
m68k_021750:
        btst.b #0x1,0xf6d7:w
m68k_021750_end:
.org 0x21756
m68k_021756:
        bne.w (. + 18)
m68k_021756_end:
.org 0x2175A
m68k_02175a:
        lea.l 0xe774:w,%a0
m68k_02175a_end:
.org 0x2175E
m68k_02175e:
        move.w 0xf68a:w,%d0
m68k_02175e_end:
.org 0x21762
m68k_021762:
        lsl.w #0x2,%d0
m68k_021762_end:
.org 0x21764
m68k_021764:
        clr.l (%a0, %d0.w)
m68k_021764_end:
.org 0x21768
m68k_021768:
        rts
m68k_021768_end:
.org 0x2176A
m68k_02176a:
        btst.b #0x5,0xf603:w
m68k_02176a_end:
.org 0x21770
m68k_021770:
        beq.w (. + 86)
m68k_021770_end:
.org 0x21774
m68k_021774:
        bsr.w (. + 2340)
m68k_021774_end:
.org 0x21778
m68k_021778:
        bsr.w (. + 2498)
m68k_021778_end:
.org 0x2177C
m68k_02177c:
        bsr.w (. + 76)
m68k_02177c_end:
.org 0x21780
m68k_021780:
        bsr.w (. + 212)
m68k_021780_end:
.org 0x21784
m68k_021784:
        bsr.w (. + 394)
m68k_021784_end:
.org 0x21788
m68k_021788:
        move.w #0x200,0xf612:w
m68k_021788_end:
.org 0x2178E
m68k_02178e:
        clr.w 0xf362:w
m68k_02178e_end:
.org 0x21792
m68k_021792:
        clr.w 0xf352:w
m68k_021792_end:
.org 0x21796
m68k_021796:
        move.w #0xffff,0xf376:w
m68k_021796_end:
.org 0x2179C
m68k_02179c:
        move.b 0xf68d:w,0xa622:w
m68k_02179c_end:
.org 0x217A2
m68k_0217a2:
        move.b 0xf68f:w,0xa623:w
m68k_0217a2_end:
.org 0x217A8
m68k_0217a8:
        lea.l 0x9fff:w,%a0
m68k_0217a8_end:
.org 0x217AC
m68k_0217ac:
        move.w 0xf68a:w,%d0
m68k_0217ac_end:
.org 0x217B0
m68k_0217b0:
        clr.b (%a0, %d0.w)
m68k_0217b0_end:
.org 0x217B4
m68k_0217b4:
        subq.w #0x1,%d0
m68k_0217b4_end:
.org 0x217B6
m68k_0217b6:
        move.w %d0,%d1
m68k_0217b6_end:
.org 0x217B8
m68k_0217b8:
        lsr.w #0x3,%d1
m68k_0217b8_end:
.org 0x217BA
m68k_0217ba:
        andi.w #0x7,%d0
m68k_0217ba_end:
.org 0x217BE
m68k_0217be:
        lea.l 0xefaa:w,%a0
m68k_0217be_end:
.org 0x217C2
m68k_0217c2:
        bclr.b %d0,(%a0, %d1.w)
m68k_0217c2_end:
.org 0x217C6
m68k_0217c6:
        rts
m68k_0217c6_end:
.org 0x21854
m68k_021854:
        lea.l 0xf45e:w,%a0
m68k_021854_end:
.org 0x21858
m68k_021858:
        move.w 0xf68a:w,%d0
m68k_021858_end:
.org 0x2185C
m68k_02185c:
        lsl.w #0x1,%d0
m68k_02185c_end:
.org 0x2185E
m68k_02185e:
        move.w 0xf68c:w,%d1
m68k_02185e_end:
.org 0x21862
m68k_021862:
        btst.b #0x1,0xf6d7:w
m68k_021862_end:
.org 0x21868
m68k_021868:
        beq.w (. + 8)
m68k_021868_end:
.org 0x2186C
m68k_02186c:
        move.w 0xf68e:w,%d1
m68k_02186c_end:
.org 0x21870
m68k_021870:
        lsl.w #0x1,%d1
m68k_021870_end:
.org 0x21872
m68k_021872:
        lea.l 0xe640:w,%a1
m68k_021872_end:
.org 0x21876
m68k_021876:
        move.w (%a1, %d1.w),%d1
m68k_021876_end:
.org 0x2187A
m68k_02187a:
        lea.l 0xcc00:w,%a1
m68k_02187a_end:
.org 0x2187E
m68k_02187e:
        move.b (%a1, %d1.w),%d2
m68k_02187e_end:
.org 0x21882
m68k_021882:
        cmp.b 0xf68b:w,%d2
m68k_021882_end:
.org 0x21886
m68k_021886:
        bne.w (. + 12)
m68k_021886_end:
.org 0x2188A
m68k_02188a:
        move.w %d1,(%a0, %d0.w)
m68k_02188a_end:
.org 0x2188E
m68k_02188e:
        bra.w (. + 34)
m68k_02188e_end:
.org 0x21892
m68k_021892:
        move.w (%a0, %d0.w),%d2
m68k_021892_end:
.org 0x21896
m68k_021896:
        move.b (%a1, %d2.w),%d2
m68k_021896_end:
.org 0x2189A
m68k_02189a:
        cmp.b 0xf68b:w,%d2
m68k_02189a_end:
.org 0x2189E
m68k_02189e:
        bne.w (. + 14)
m68k_02189e_end:
.org 0x218A2
m68k_0218a2:
        btst.b #0x1,0xf6d7:w
m68k_0218a2_end:
.org 0x218A8
m68k_0218a8:
        bne.w (. + 8)
m68k_0218a8_end:
.org 0x218AC
m68k_0218ac:
        bsr.w (. + 6)
m68k_0218ac_end:
.org 0x218B0
m68k_0218b0:
        rts
m68k_0218b0_end:
.org 0x218B2
m68k_0218b2:
        movem.l %d4/%a3,-(%a7)
m68k_0218b2_end:
.org 0x218B6
m68k_0218b6:
        lea.l 0xcc00:w,%a3
m68k_0218b6_end:
.org 0x218BA
m68k_0218ba:
        move.w 0xf68a:w,%d4
m68k_0218ba_end:
.org 0x218BE
m68k_0218be:
        clr.w %d1
m68k_0218be_end:
.org 0x218C0
m68k_0218c0:
        lea.l 0xc300:w,%a1
m68k_0218c0_end:
.org 0x218C4
m68k_0218c4:
        lea.l 0xa550:w,%a2
m68k_0218c4_end:
.org 0x218C8
m68k_0218c8:
        bsr.w (. + 38)
m68k_0218c8_end:
.org 0x218CC
m68k_0218cc:
        lea.l 0xa57a:w,%a2
m68k_0218cc_end:
.org 0x218D0
m68k_0218d0:
        bsr.w (. + 30)
m68k_0218d0_end:
.org 0x218D4
m68k_0218d4:
        lea.l 0xa5a4:w,%a2
m68k_0218d4_end:
.org 0x218D8
m68k_0218d8:
        bsr.w (. + 22)
m68k_0218d8_end:
.org 0x218DC
m68k_0218dc:
        lea.l 0xa5ce:w,%a2
m68k_0218dc_end:
.org 0x218E0
m68k_0218e0:
        bsr.w (. + 14)
m68k_0218e0_end:
.org 0x218E4
m68k_0218e4:
        move.w %d2,(%a0, %d0.w)
m68k_0218e4_end:
.org 0x218E8
m68k_0218e8:
        movem.l (%a7)+,%d4/%a3
m68k_0218e8_end:
.org 0x218EC
m68k_0218ec:
        rts
m68k_0218ec_end:
.org 0x218EE
m68k_0218ee:
        move.w (%a2)+,%d3
m68k_0218ee_end:
.org 0x218F0
m68k_0218f0:
        bmi.w (. + 28)
m68k_0218f0_end:
.org 0x218F4
m68k_0218f4:
        andi.w #0xff,%d3
m68k_0218f4_end:
.org 0x218F8
m68k_0218f8:
        cmp.b (%a3, %d3.w),%d4
m68k_0218f8_end:
.org 0x218FC
m68k_0218fc:
        bne.b (. + -14)
m68k_0218fc_end:
.org 0x218FE
m68k_0218fe:
        cmp.b (%a1, %d3.w),%d1
m68k_0218fe_end:
.org 0x21902
m68k_021902:
        bcc.b (. + -20)
m68k_021902_end:
.org 0x21904
m68k_021904:
        move.b (%a1, %d3.w),%d1
m68k_021904_end:
.org 0x21908
m68k_021908:
        move.w %d3,%d2
m68k_021908_end:
.org 0x2190A
m68k_02190a:
        bra.b (. + -28)
m68k_02190a_end:
.org 0x2190C
m68k_02190c:
        rts
m68k_02190c_end:
.org 0x2190E
m68k_02190e:
        lea.l 0xa150:w,%a0
m68k_02190e_end:
.org 0x21912
m68k_021912:
        lea.l 0xcc00:w,%a1
m68k_021912_end:
.org 0x21916
m68k_021916:
        move.w 0xf68a:w,%d0
m68k_021916_end:
.org 0x2191A
m68k_02191a:
        move.w #0xff,%d1
m68k_02191a_end:
.org 0x2191E
m68k_02191e:
        move.b (%a1, %d1.w),%d2
m68k_02191e_end:
.org 0x21922
m68k_021922:
        andi.w #0x3f,%d2
m68k_021922_end:
.org 0x21926
m68k_021926:
        cmp.w %d0,%d2
m68k_021926_end:
.org 0x21928
m68k_021928:
        bne.w (. + 12)
m68k_021928_end:
.org 0x2192C
m68k_02192c:
        move.w %d1,%d2
m68k_02192c_end:
.org 0x2192E
m68k_02192e:
        lsl.w #0x2,%d2
m68k_02192e_end:
.org 0x21930
m68k_021930:
        clr.l (%a0, %d2.w)
m68k_021930_end:
.org 0x21934
m68k_021934:
        dbra %d1,(. + -22)
m68k_021934_end:
.org 0x21938
m68k_021938:
        move.w 0xf68a:w,%d0
m68k_021938_end:
.org 0x2193C
m68k_02193c:
        lsl.w #0x2,%d0
m68k_02193c_end:
.org 0x2193E
m68k_02193e:
        lea.l 0xed84:w,%a0
m68k_02193e_end:
.org 0x21942
m68k_021942:
        clr.l (%a0, %d0.w)
m68k_021942_end:
.org 0x21946
m68k_021946:
        lea.l 0xee24:w,%a0
m68k_021946_end:
.org 0x2194A
m68k_02194a:
        clr.l (%a0, %d0.w)
m68k_02194a_end:
.org 0x2194E
m68k_02194e:
        rts
m68k_02194e_end:
.org 0x21950
m68k_021950:
        move.w #0x1b,0xf362:w
m68k_021950_end:
.org 0x21956
m68k_021956:
        move.w #0x126,%d0
m68k_021956_end:
.org 0x2195A
m68k_02195a:
        move.w %d0,0xaf80:w
m68k_02195a_end:
.org 0x2195E
m68k_02195e:
        jsr 0x676f2:l
m68k_02195e_end:
.org 0x21964
m68k_021964:
        move.w #0x1,0xf652:w
m68k_021964_end:
.org 0x2196A
m68k_02196a:
        rts
m68k_02196a_end:
.org 0x219AA
m68k_0219aa:
        addq.w #0x1,0xf362:w
m68k_0219aa_end:
.org 0x219AE
m68k_0219ae:
        move.w #0x138,%d0
m68k_0219ae_end:
.org 0x219B2
m68k_0219b2:
        jsr 0x676f2:l
m68k_0219b2_end:
.org 0x219B8
m68k_0219b8:
        rts
m68k_0219b8_end:
.org 0x219BA
m68k_0219ba:
        btst.b #0x5,0xf603:w
m68k_0219ba_end:
.org 0x219C0
m68k_0219c0:
        beq.w (. + 26)
m68k_0219c0_end:
.org 0x219C4
m68k_0219c4:
        move.w #0x2,0xf6d6:w
m68k_0219c4_end:
.org 0x219CA
m68k_0219ca:
        addq.w #0x1,0xf362:w
m68k_0219ca_end:
.org 0x219CE
m68k_0219ce:
        move.w #0xffff,0xaf28:w
m68k_0219ce_end:
.org 0x219D4
m68k_0219d4:
        move.w #0xffff,0xef80:w
m68k_0219d4_end:
.org 0x219DA
m68k_0219da:
        rts
m68k_0219da_end:
.org 0x219DC
m68k_0219dc:
        move.w 0xf68e:w,%d0
m68k_0219dc_end:
.org 0x219E0
m68k_0219e0:
        cmp.w 0xf67a:w,%d0
m68k_0219e0_end:
.org 0x219E4
m68k_0219e4:
        beq.w (. + 28)
m68k_0219e4_end:
.org 0x219E8
m68k_0219e8:
        cmp.w 0xf67c:w,%d0
m68k_0219e8_end:
.org 0x219EC
m68k_0219ec:
        beq.w (. + 20)
m68k_0219ec_end:
.org 0x219F0
m68k_0219f0:
        cmp.w 0xf67e:w,%d0
m68k_0219f0_end:
.org 0x219F4
m68k_0219f4:
        beq.w (. + 12)
m68k_0219f4_end:
.org 0x219F8
m68k_0219f8:
        addq.w #0x1,0xf362:w
m68k_0219f8_end:
.org 0x219FC
m68k_0219fc:
        bra.w (. + 94)
m68k_0219fc_end:
.org 0x21A00
m68k_021a00:
        tst.w 0xa5ce:w
m68k_021a00_end:
.org 0x21A04
m68k_021a04:
        bpl.w (. + 14)
m68k_021a04_end:
.org 0x21A08
m68k_021a08:
        move.w #0x8,0xf362:w
m68k_021a08_end:
.org 0x21A0E
m68k_021a0e:
        bra.w (. + 76)
m68k_021a0e_end:
.org 0x21A12
m68k_021a12:
        lea.l 0xa5ce:w,%a0
m68k_021a12_end:
.org 0x21A16
m68k_021a16:
        lea.l 0xf500:w,%a1
m68k_021a16_end:
.org 0x21A1A
m68k_021a1a:
        clr.w %d0
m68k_021a1a_end:
.org 0x21A1C
m68k_021a1c:
        move.w (%a0)+,(%a1)+
m68k_021a1c_end:
.org 0x21A1E
m68k_021a1e:
        bmi.w (. + 12)
m68k_021a1e_end:
.org 0x21A22
m68k_021a22:
        addq.w #0x1,%d0
m68k_021a22_end:
.org 0x21A24
m68k_021a24:
        cmpi.w #0xa,%d0
m68k_021a24_end:
.org 0x21A28
m68k_021a28:
        bcs.b (. + -12)
m68k_021a28_end:
.org 0x21A2A
m68k_021a2a:
        move.w %d0,0xf636:w
m68k_021a2a_end:
.org 0x21A2E
m68k_021a2e:
        move.w #0x4,0xf3b0:w
m68k_021a2e_end:
.org 0x21A34
m68k_021a34:
        move.w 0xf612:w,0xf38a:w
m68k_021a34_end:
.org 0x21A3A
m68k_021a3a:
        move.w #0x405,0xf612:w
m68k_021a3a_end:
.org 0x21A40
m68k_021a40:
        clr.w 0xf362:w
m68k_021a40_end:
.org 0x21A44
m68k_021a44:
        clr.w 0xf378:w
m68k_021a44_end:
.org 0x21A48
m68k_021a48:
        clr.w 0xf658:w
m68k_021a48_end:
.org 0x21A4C
m68k_021a4c:
        move.w #0x11c,%d0
m68k_021a4c_end:
.org 0x21A50
m68k_021a50:
        move.w %d0,0xaf80:w
m68k_021a50_end:
.org 0x21A54
m68k_021a54:
        jsr 0x676f2:l
m68k_021a54_end:
.org 0x21A5A
m68k_021a5a:
        rts
m68k_021a5a_end:
.org 0x21A5C
m68k_021a5c:
        bsr.w (. + 44)
m68k_021a5c_end:
.org 0x21A60
m68k_021a60:
        bsr.w (. + 116)
m68k_021a60_end:
.org 0x21A64
m68k_021a64:
        lea.l 0xaf56:w,%a0
m68k_021a64_end:
.org 0x21A68
m68k_021a68:
        move.w 0xf68a:w,%d0
m68k_021a68_end:
.org 0x21A6C
m68k_021a6c:
        bset.l #0x7,%d0
m68k_021a6c_end:
.org 0x21A70
m68k_021a70:
        lea.l 0xcc00:w,%a1
m68k_021a70_end:
.org 0x21A74
m68k_021a74:
        move.w (%a0)+,%d1
m68k_021a74_end:
.org 0x21A76
m68k_021a76:
        bmi.w (. + 10)
m68k_021a76_end:
.org 0x21A7A
m68k_021a7a:
        move.b %d0,(%a1, %d1.w)
m68k_021a7a_end:
.org 0x21A7E
m68k_021a7e:
        bra.b (. + -10)
m68k_021a7e_end:
.org 0x21A80
m68k_021a80:
        move.w #0xc,0xf362:w
m68k_021a80_end:
.org 0x21A86
m68k_021a86:
        rts
m68k_021a86_end:
.org 0x21A88
m68k_021a88:
        move.w 0xf68e:w,%d1
m68k_021a88_end:
.org 0x21A8C
m68k_021a8c:
        lea.l 0xe640:w,%a0
m68k_021a8c_end:
.org 0x21A90
m68k_021a90:
        lsl.w #0x1,%d1
m68k_021a90_end:
.org 0x21A92
m68k_021a92:
        move.w (%a0, %d1.w),0xf3f2:w
m68k_021a92_end:
.org 0x21A98
m68k_021a98:
        move.w 0xf68a:w,%d1
m68k_021a98_end:
.org 0x21A9C
m68k_021a9c:
        lea.l 0xaf28:w,%a0
m68k_021a9c_end:
.org 0x21AA0
m68k_021aa0:
        lea.l 0xa5ce:w,%a1
m68k_021aa0_end:
.org 0x21AA4
m68k_021aa4:
        lea.l 0xcc00:w,%a2
m68k_021aa4_end:
.org 0x21AA8
m68k_021aa8:
        lea.l 0xa150:w,%a3
m68k_021aa8_end:
.org 0x21AAC
m68k_021aac:
        move.w (%a1)+,%d0
m68k_021aac_end:
.org 0x21AAE
m68k_021aae:
        bmi.w (. + 26)
m68k_021aae_end:
.org 0x21AB2
m68k_021ab2:
        move.b %d1,(%a2, %d0.w)
m68k_021ab2_end:
.org 0x21AB6
m68k_021ab6:
        move.w %d0,0xf3a6:w
m68k_021ab6_end:
.org 0x21ABA
m68k_021aba:
        move.w %d0,(%a0)+
m68k_021aba_end:
.org 0x21ABC
m68k_021abc:
        lsl.w #0x2,%d0
m68k_021abc_end:
.org 0x21ABE
m68k_021abe:
        clr.l (%a3, %d0.w)
m68k_021abe_end:
.org 0x21AC2
m68k_021ac2:
        bsr.w (. + -4596)
m68k_021ac2_end:
.org 0x21AC6
m68k_021ac6:
        bra.b (. + -26)
m68k_021ac6_end:
.org 0x21AC8
m68k_021ac8:
        move.w #0xffff,(%a0)
m68k_021ac8_end:
.org 0x21ACC
m68k_021acc:
        move.w #0xffff,0xa5ce:w
m68k_021acc_end:
.org 0x21AD2
m68k_021ad2:
        rts
m68k_021ad2_end:
.org 0x21AD4
m68k_021ad4:
        lea.l 0xa5a4:w,%a0
m68k_021ad4_end:
.org 0x21AD8
m68k_021ad8:
        clr.w %d7
m68k_021ad8_end:
.org 0x21ADA
m68k_021ada:
        btst.b #0x1,0xf6d7:w
m68k_021ada_end:
.org 0x21AE0
m68k_021ae0:
        bne.w (. + 8)
m68k_021ae0_end:
.org 0x21AE4
m68k_021ae4:
        lea.l 0xa550:w,%a0
m68k_021ae4_end:
.org 0x21AE8
m68k_021ae8:
        tst.w (%a0)+
m68k_021ae8_end:
.org 0x21AEA
m68k_021aea:
        bmi.w (. + 8)
m68k_021aea_end:
.org 0x21AEE
m68k_021aee:
        addq.w #0x1,%d7
m68k_021aee_end:
.org 0x21AF0
m68k_021af0:
        bra.b (. + -8)
m68k_021af0_end:
.org 0x21AF2
m68k_021af2:
        lea.l 0xaf28:w,%a0
m68k_021af2_end:
.org 0x21AF6
m68k_021af6:
        clr.w %d6
m68k_021af6_end:
.org 0x21AF8
m68k_021af8:
        tst.w (%a0)+
m68k_021af8_end:
.org 0x21AFA
m68k_021afa:
        bmi.w (. + 10)
m68k_021afa_end:
.org 0x21AFE
m68k_021afe:
        addq.w #0x1,%d7
m68k_021afe_end:
.org 0x21B00
m68k_021b00:
        addq.w #0x1,%d6
m68k_021b00_end:
.org 0x21B02
m68k_021b02:
        bra.b (. + -10)
m68k_021b02_end:
.org 0x21B04
m68k_021b04:
        move.w #0x12,%d0
m68k_021b04_end:
.org 0x21B08
m68k_021b08:
        sub.w %d6,%d0
m68k_021b08_end:
.org 0x21B0A
m68k_021b0a:
        move.w #0xffff,(%a0)+
m68k_021b0a_end:
.org 0x21B0E
m68k_021b0e:
        dbra %d0,(. + -4)
m68k_021b0e_end:
.org 0x21B12
m68k_021b12:
        lea.l 0xaf56:w,%a0
m68k_021b12_end:
.org 0x21B16
m68k_021b16:
        lea.l 0xaf28:w,%a1
m68k_021b16_end:
.org 0x21B1A
m68k_021b1a:
        subi.w #0xa,%d7
m68k_021b1a_end:
.org 0x21B1E
m68k_021b1e:
        bls.w (. + 106)
m68k_021b1e_end:
.org 0x21B22
m68k_021b22:
        move.w #0x9,%d6
m68k_021b22_end:
.org 0x21B26
m68k_021b26:
        jsr 0x83d4:l
m68k_021b26_end:
.org 0x21B2C
m68k_021b2c:
        andi.l #0xffff,%d0
m68k_021b2c_end:
.org 0x21B32
m68k_021b32:
        move.l %d0,%d1
m68k_021b32_end:
.org 0x21B34
m68k_021b34:
        lsl.l #0x2,%d0
m68k_021b34_end:
.org 0x21B36
m68k_021b36:
        add.l %d1,%d0
m68k_021b36_end:
.org 0x21B38
m68k_021b38:
        lsl.l #0x2,%d0
m68k_021b38_end:
.org 0x21B3A
m68k_021b3a:
        swap %d0
m68k_021b3a_end:
.org 0x21B3C
m68k_021b3c:
        move.w %d0,%d2
m68k_021b3c_end:
.org 0x21B3E
m68k_021b3e:
        jsr 0x83d4:l
m68k_021b3e_end:
.org 0x21B44
m68k_021b44:
        andi.l #0xffff,%d0
m68k_021b44_end:
.org 0x21B4A
m68k_021b4a:
        move.l %d0,%d1
m68k_021b4a_end:
.org 0x21B4C
m68k_021b4c:
        lsl.l #0x2,%d0
m68k_021b4c_end:
.org 0x21B4E
m68k_021b4e:
        add.l %d1,%d0
m68k_021b4e_end:
.org 0x21B50
m68k_021b50:
        lsl.l #0x2,%d0
m68k_021b50_end:
.org 0x21B52
m68k_021b52:
        swap %d0
m68k_021b52_end:
.org 0x21B54
m68k_021b54:
        lsl.w #0x1,%d0
m68k_021b54_end:
.org 0x21B56
m68k_021b56:
        lsl.w #0x1,%d2
m68k_021b56_end:
.org 0x21B58
m68k_021b58:
        move.w (%a1, %d0.w),%d1
m68k_021b58_end:
.org 0x21B5C
m68k_021b5c:
        bmi.w (. + 22)
m68k_021b5c_end:
.org 0x21B60
m68k_021b60:
        move.w (%a1, %d2.w),%d3
m68k_021b60_end:
.org 0x21B64
m68k_021b64:
        bmi.w (. + 14)
m68k_021b64_end:
.org 0x21B68
m68k_021b68:
        exg %d1,%d3
m68k_021b68_end:
.org 0x21B6A
m68k_021b6a:
        move.w %d1,(%a1, %d0.w)
m68k_021b6a_end:
.org 0x21B6E
m68k_021b6e:
        move.w %d3,(%a1, %d2.w)
m68k_021b6e_end:
.org 0x21B72
m68k_021b72:
        dbra %d6,(. + -76)
m68k_021b72_end:
.org 0x21B76
m68k_021b76:
        subq.w #0x1,%d7
m68k_021b76_end:
.org 0x21B78
m68k_021b78:
        lea.l 0xaf28:w,%a1
m68k_021b78_end:
.org 0x21B7C
m68k_021b7c:
        move.w (%a1)+,%d0
m68k_021b7c_end:
.org 0x21B7E
m68k_021b7e:
        bset.l #0xe,%d0
m68k_021b7e_end:
.org 0x21B82
m68k_021b82:
        move.w %d0,(%a0)+
m68k_021b82_end:
.org 0x21B84
m68k_021b84:
        dbra %d7,(. + -8)
m68k_021b84_end:
.org 0x21B88
m68k_021b88:
        move.w #0xffff,(%a0)
m68k_021b88_end:
.org 0x21B8C
m68k_021b8c:
        rts
m68k_021b8c_end:
.org 0x21B8E
m68k_021b8e:
        bra.w (. + -5908)
m68k_021b8e_end:
.org 0x21B92
m68k_021b92:
        bra.w (. + -5854)
m68k_021b92_end:
.org 0x21B96
m68k_021b96:
        bra.w (. + -5384)
m68k_021b96_end:
.org 0x21B9A
m68k_021b9a:
        btst.b #0x5,0xf603:w
m68k_021b9a_end:
.org 0x21BA0
m68k_021ba0:
        beq.w (. + 44)
m68k_021ba0_end:
.org 0x21BA4
m68k_021ba4:
        move.w #0xac,%d0
m68k_021ba4_end:
.org 0x21BA8
m68k_021ba8:
        jsr 0x808a:l
m68k_021ba8_end:
.org 0x21BAE
m68k_021bae:
        lea.l 0xcc00:w,%a0
m68k_021bae_end:
.org 0x21BB2
m68k_021bb2:
        move.w 0xf3a6:w,%d0
m68k_021bb2_end:
.org 0x21BB6
m68k_021bb6:
        move.b 0xf68b:w,(%a0, %d0.w)
m68k_021bb6_end:
.org 0x21BBC
m68k_021bbc:
        lea.l 0xa150:w,%a0
m68k_021bbc_end:
.org 0x21BC0
m68k_021bc0:
        lsl.w #0x2,%d0
m68k_021bc0_end:
.org 0x21BC2
m68k_021bc2:
        clr.l (%a0, %d0.w)
m68k_021bc2_end:
.org 0x21BC6
m68k_021bc6:
        move.w #0x2,0xf362:w
m68k_021bc6_end:
.org 0x21BCC
m68k_021bcc:
        rts
m68k_021bcc_end:
.org 0x21BCE
m68k_021bce:
        bsr.w (. + 78)
m68k_021bce_end:
.org 0x21BD2
m68k_021bd2:
        move.w %d0,%d1
m68k_021bd2_end:
.org 0x21BD4
m68k_021bd4:
        addi.w #0x1,%d1
m68k_021bd4_end:
.org 0x21BD8
m68k_021bd8:
        cmpi.w #0xa,%d1
m68k_021bd8_end:
.org 0x21BDC
m68k_021bdc:
        bls.w (. + 56)
m68k_021bdc_end:
.org 0x21BE0
m68k_021be0:
        move.w %d0,0xf636:w
m68k_021be0_end:
.org 0x21BE4
m68k_021be4:
        move.w #0x1,0xf712:w
m68k_021be4_end:
.org 0x21BEA
m68k_021bea:
        addq.w #0x1,0xf362:w
m68k_021bea_end:
.org 0x21BEE
m68k_021bee:
        clr.w 0xf378:w
m68k_021bee_end:
.org 0x21BF2
m68k_021bf2:
        clr.w 0xf658:w
m68k_021bf2_end:
.org 0x21BF6
m68k_021bf6:
        move.l #0xabd12,0xf6c0:w
m68k_021bf6_end:
.org 0x21BFE
m68k_021bfe:
        clr.w 0xf36a:w
m68k_021bfe_end:
.org 0x21C02
m68k_021c02:
        bsr.w (. + -2420)
m68k_021c02_end:
.org 0x21C06
m68k_021c06:
        move.w %d0,0xaf80:w
m68k_021c06_end:
.org 0x21C0A
m68k_021c0a:
        jsr 0x676f2:l
m68k_021c0a_end:
.org 0x21C10
m68k_021c10:
        bra.w (. + 10)
m68k_021c10_end:
.org 0x21C14
m68k_021c14:
        move.w #0xc,0xf362:w
m68k_021c14_end:
.org 0x21C1A
m68k_021c1a:
        rts
m68k_021c1a_end:
.org 0x21C1C
m68k_021c1c:
        btst.b #0x1,0xf6d7:w
m68k_021c1c_end:
.org 0x21C22
m68k_021c22:
        bne.w (. + 28)
m68k_021c22_end:
.org 0x21C26
m68k_021c26:
        lea.l 0xa550:w,%a0
m68k_021c26_end:
.org 0x21C2A
m68k_021c2a:
        move.w 0xf68a:w,%d1
m68k_021c2a_end:
.org 0x21C2E
m68k_021c2e:
        lea.l 0xa027:w,%a3
m68k_021c2e_end:
.org 0x21C32
m68k_021c32:
        move.b (%a3, %d1.w),%d1
m68k_021c32_end:
.org 0x21C36
m68k_021c36:
        andi.w #0xff,%d1
m68k_021c36_end:
.org 0x21C3A
m68k_021c3a:
        bra.w (. + 22)
m68k_021c3a_end:
.org 0x21C3E
m68k_021c3e:
        lea.l 0xa5a4:w,%a0
m68k_021c3e_end:
.org 0x21C42
m68k_021c42:
        move.w 0xf68a:w,%d1
m68k_021c42_end:
.org 0x21C46
m68k_021c46:
        lsl.w #0x1,%d1
m68k_021c46_end:
.org 0x21C48
m68k_021c48:
        lea.l 0xf45e:w,%a3
m68k_021c48_end:
.org 0x21C4C
m68k_021c4c:
        move.w (%a3, %d1.w),%d1
m68k_021c4c_end:
.org 0x21C50
m68k_021c50:
        lea.l 0xaf28:w,%a1
m68k_021c50_end:
.org 0x21C54
m68k_021c54:
        lea.l 0xaf56:w,%a2
m68k_021c54_end:
.org 0x21C58
m68k_021c58:
        clr.w %d0
m68k_021c58_end:
.org 0x21C5A
m68k_021c5a:
        move.w (%a0)+,%d2
m68k_021c5a_end:
.org 0x21C5C
m68k_021c5c:
        bmi.w (. + 14)
m68k_021c5c_end:
.org 0x21C60
m68k_021c60:
        cmp.w %d1,%d2
m68k_021c60_end:
.org 0x21C62
m68k_021c62:
        beq.b (. + -8)
m68k_021c62_end:
.org 0x21C64
m68k_021c64:
        addq.w #0x1,%d0
m68k_021c64_end:
.org 0x21C66
m68k_021c66:
        move.w %d2,(%a2)+
m68k_021c66_end:
.org 0x21C68
m68k_021c68:
        bra.b (. + -14)
m68k_021c68_end:
.org 0x21C6A
m68k_021c6a:
        move.w (%a1)+,(%a2)+
m68k_021c6a_end:
.org 0x21C6C
m68k_021c6c:
        bmi.w (. + 8)
m68k_021c6c_end:
.org 0x21C70
m68k_021c70:
        addq.w #0x1,%d0
m68k_021c70_end:
.org 0x21C72
m68k_021c72:
        bra.b (. + -8)
m68k_021c72_end:
.org 0x21C74
m68k_021c74:
        rts
m68k_021c74_end:
.org 0x21C76
m68k_021c76:
        bra.w (. + -2460)
m68k_021c76_end:
.org 0x21C7A
m68k_021c7a:
        bra.w (. + -2388)
m68k_021c7a_end:
.org 0x21C7E
m68k_021c7e:
        bsr.w (. + -2544)
m68k_021c7e_end:
.org 0x21C82
m68k_021c82:
        bcs.w (. + 62)
m68k_021c82_end:
.org 0x21C86
m68k_021c86:
        bsr.w (. + -1906)
m68k_021c86_end:
.org 0x21C8A
m68k_021c8a:
        bsr.w (. + -1732)
m68k_021c8a_end:
.org 0x21C8E
m68k_021c8e:
        addq.w #0x1,0xf362:w
m68k_021c8e_end:
.org 0x21C92
m68k_021c92:
        lea.l 0xaf56:w,%a0
m68k_021c92_end:
.org 0x21C96
m68k_021c96:
        move.w (%a0)+,%d0
m68k_021c96_end:
.org 0x21C98
m68k_021c98:
        btst.l #0xe,%d0
m68k_021c98_end:
.org 0x21C9C
m68k_021c9c:
        beq.b (. + -6)
m68k_021c9c_end:
.org 0x21C9E
m68k_021c9e:
        andi.w #0xff,%d0
m68k_021c9e_end:
.org 0x21CA2
m68k_021ca2:
        move.w %d0,0xf3d0:w
m68k_021ca2_end:
.org 0x21CA6
m68k_021ca6:
        move.w 0xf612:w,0xf38a:w
m68k_021ca6_end:
.org 0x21CAC
m68k_021cac:
        move.w #0xc,0xf3b0:w
m68k_021cac_end:
.org 0x21CB2
m68k_021cb2:
        clr.w 0xf36a:w
m68k_021cb2_end:
.org 0x21CB6
m68k_021cb6:
        move.w #0x406,0xf612:w
m68k_021cb6_end:
.org 0x21CBC
m68k_021cbc:
        bra.w (. + 8)
m68k_021cbc_end:
.org 0x21CC0
m68k_021cc0:
        bsr.w (. + -1826)
m68k_021cc0_end:
.org 0x21CC4
m68k_021cc4:
        rts
m68k_021cc4_end:
.org 0x21CC6
m68k_021cc6:
        clr.w 0xf6d6:w
m68k_021cc6_end:
.org 0x21CCA
m68k_021cca:
        move.w 0xf68c:w,%d0
m68k_021cca_end:
.org 0x21CCE
m68k_021cce:
        cmp.w 0xf67a:w,%d0
m68k_021cce_end:
.org 0x21CD2
m68k_021cd2:
        beq.w (. + 28)
m68k_021cd2_end:
.org 0x21CD6
m68k_021cd6:
        cmp.w 0xf67c:w,%d0
m68k_021cd6_end:
.org 0x21CDA
m68k_021cda:
        beq.w (. + 20)
m68k_021cda_end:
.org 0x21CDE
m68k_021cde:
        cmp.w 0xf67e:w,%d0
m68k_021cde_end:
.org 0x21CE2
m68k_021ce2:
        beq.w (. + 12)
m68k_021ce2_end:
.org 0x21CE6
m68k_021ce6:
        addq.w #0x1,0xf362:w
m68k_021ce6_end:
.org 0x21CEA
m68k_021cea:
        bra.w (. + 94)
m68k_021cea_end:
.org 0x21CEE
m68k_021cee:
        tst.w 0xa57a:w
m68k_021cee_end:
.org 0x21CF2
m68k_021cf2:
        bpl.w (. + 14)
m68k_021cf2_end:
.org 0x21CF6
m68k_021cf6:
        move.w #0x12,0xf362:w
m68k_021cf6_end:
.org 0x21CFC
m68k_021cfc:
        bra.w (. + 76)
m68k_021cfc_end:
.org 0x21D00
m68k_021d00:
        lea.l 0xa57a:w,%a0
m68k_021d00_end:
.org 0x21D04
m68k_021d04:
        lea.l 0xf500:w,%a1
m68k_021d04_end:
.org 0x21D08
m68k_021d08:
        clr.w %d0
m68k_021d08_end:
.org 0x21D0A
m68k_021d0a:
        move.w (%a0)+,(%a1)+
m68k_021d0a_end:
.org 0x21D0C
m68k_021d0c:
        bmi.w (. + 12)
m68k_021d0c_end:
.org 0x21D10
m68k_021d10:
        addq.w #0x1,%d0
m68k_021d10_end:
.org 0x21D12
m68k_021d12:
        cmpi.w #0xa,%d0
m68k_021d12_end:
.org 0x21D16
m68k_021d16:
        bcs.b (. + -12)
m68k_021d16_end:
.org 0x21D18
m68k_021d18:
        move.w %d0,0xf636:w
m68k_021d18_end:
.org 0x21D1C
m68k_021d1c:
        move.w #0xe,0xf3b0:w
m68k_021d1c_end:
.org 0x21D22
m68k_021d22:
        move.w 0xf612:w,0xf38a:w
m68k_021d22_end:
.org 0x21D28
m68k_021d28:
        move.w #0x405,0xf612:w
m68k_021d28_end:
.org 0x21D2E
m68k_021d2e:
        clr.w 0xf362:w
m68k_021d2e_end:
.org 0x21D32
m68k_021d32:
        clr.w 0xf378:w
m68k_021d32_end:
.org 0x21D36
m68k_021d36:
        clr.w 0xf658:w
m68k_021d36_end:
.org 0x21D3A
m68k_021d3a:
        move.w #0x11c,%d0
m68k_021d3a_end:
.org 0x21D3E
m68k_021d3e:
        move.w %d0,0xaf80:w
m68k_021d3e_end:
.org 0x21D42
m68k_021d42:
        jsr 0x676f2:l
m68k_021d42_end:
.org 0x21D48
m68k_021d48:
        rts
m68k_021d48_end:
.org 0x21D4A
m68k_021d4a:
        bsr.w (. + 44)
m68k_021d4a_end:
.org 0x21D4E
m68k_021d4e:
        bsr.w (. + -634)
m68k_021d4e_end:
.org 0x21D52
m68k_021d52:
        lea.l 0xaf56:w,%a0
m68k_021d52_end:
.org 0x21D56
m68k_021d56:
        lea.l 0xcc00:w,%a1
m68k_021d56_end:
.org 0x21D5A
m68k_021d5a:
        move.w 0xf68a:w,%d0
m68k_021d5a_end:
.org 0x21D5E
m68k_021d5e:
        bset.l #0x7,%d0
m68k_021d5e_end:
.org 0x21D62
m68k_021d62:
        move.w (%a0)+,%d1
m68k_021d62_end:
.org 0x21D64
m68k_021d64:
        bmi.w (. + 10)
m68k_021d64_end:
.org 0x21D68
m68k_021d68:
        move.b %d0,(%a1, %d1.w)
m68k_021d68_end:
.org 0x21D6C
m68k_021d6c:
        bra.b (. + -10)
m68k_021d6c_end:
.org 0x21D6E
m68k_021d6e:
        move.w #0x16,0xf362:w
m68k_021d6e_end:
.org 0x21D74
m68k_021d74:
        rts
m68k_021d74_end:
.org 0x21D76
m68k_021d76:
        lea.l 0xaf28:w,%a0
m68k_021d76_end:
.org 0x21D7A
m68k_021d7a:
        lea.l 0xa150:w,%a2
m68k_021d7a_end:
.org 0x21D7E
m68k_021d7e:
        lea.l 0xa050:w,%a3
m68k_021d7e_end:
.org 0x21D82
m68k_021d82:
        lea.l 0xa57a:w,%a1
m68k_021d82_end:
.org 0x21D86
m68k_021d86:
        move.w 0xf68e:w,0xf3f2:w
m68k_021d86_end:
.org 0x21D8C
m68k_021d8c:
        move.w 0xf68c:w,%d1
m68k_021d8c_end:
.org 0x21D90
m68k_021d90:
        addi.w #0x41,%d1
m68k_021d90_end:
.org 0x21D94
m68k_021d94:
        move.w (%a1)+,%d0
m68k_021d94_end:
.org 0x21D96
m68k_021d96:
        bmi.w (. + 32)
m68k_021d96_end:
.org 0x21D9A
m68k_021d9a:
        move.b %d1,(%a2, %d0.w)
m68k_021d9a_end:
.org 0x21D9E
m68k_021d9e:
        move.w %d0,0xf3a6:w
m68k_021d9e_end:
.org 0x21DA2
m68k_021da2:
        move.w %d0,(%a0)+
m68k_021da2_end:
.org 0x21DA4
m68k_021da4:
        move.b 0xf68b:w,(%a3, %d0.w)
m68k_021da4_end:
.org 0x21DAA
m68k_021daa:
        lsl.w #0x2,%d0
m68k_021daa_end:
.org 0x21DAC
m68k_021dac:
        clr.l (%a2, %d0.w)
m68k_021dac_end:
.org 0x21DB0
m68k_021db0:
        bsr.w (. + -5346)
m68k_021db0_end:
.org 0x21DB4
m68k_021db4:
        bra.b (. + -32)
m68k_021db4_end:
.org 0x21DB6
m68k_021db6:
        move.w #0xffff,(%a0)
m68k_021db6_end:
.org 0x21DBA
m68k_021dba:
        move.w #0xffff,0xa57a:w
m68k_021dba_end:
.org 0x21DC0
m68k_021dc0:
        rts
m68k_021dc0_end:
.org 0x21DC2
m68k_021dc2:
        bra.w (. + -6472)
m68k_021dc2_end:
.org 0x21DC6
m68k_021dc6:
        bra.w (. + -6418)
m68k_021dc6_end:
.org 0x21DCA
m68k_021dca:
        bra.w (. + -5948)
m68k_021dca_end:
.org 0x21DCE
m68k_021dce:
        btst.b #0x5,0xf603:w
m68k_021dce_end:
.org 0x21DD4
m68k_021dd4:
        beq.w (. + 60)
m68k_021dd4_end:
.org 0x21DD8
m68k_021dd8:
        move.w #0xac,%d0
m68k_021dd8_end:
.org 0x21DDC
m68k_021ddc:
        jsr 0x808a:l
m68k_021ddc_end:
.org 0x21DE2
m68k_021de2:
        lea.l 0xcc00:w,%a0
m68k_021de2_end:
.org 0x21DE6
m68k_021de6:
        move.w 0xf3a6:w,%d0
m68k_021de6_end:
.org 0x21DEA
m68k_021dea:
        move.w 0xf68c:w,%d1
m68k_021dea_end:
.org 0x21DEE
m68k_021dee:
        addi.w #0x29,%d1
m68k_021dee_end:
.org 0x21DF2
m68k_021df2:
        move.b %d1,(%a0, %d0.w)
m68k_021df2_end:
.org 0x21DF6
m68k_021df6:
        lea.l 0xa050:w,%a0
m68k_021df6_end:
.org 0x21DFA
m68k_021dfa:
        move.b 0xf68b:w,(%a0, %d0.w)
m68k_021dfa_end:
.org 0x21E00
m68k_021e00:
        lea.l 0xa150:w,%a0
m68k_021e00_end:
.org 0x21E04
m68k_021e04:
        lsl.w #0x2,%d0
m68k_021e04_end:
.org 0x21E06
m68k_021e06:
        clr.l (%a0, %d0.w)
m68k_021e06_end:
.org 0x21E0A
m68k_021e0a:
        move.w #0xc,0xf362:w
m68k_021e0a_end:
.org 0x21E10
m68k_021e10:
        rts
m68k_021e10_end:
.org 0x21E12
m68k_021e12:
        bsr.w (. + -502)
m68k_021e12_end:
.org 0x21E16
m68k_021e16:
        move.w %d0,%d1
m68k_021e16_end:
.org 0x21E18
m68k_021e18:
        addi.w #0x1,%d1
m68k_021e18_end:
.org 0x21E1C
m68k_021e1c:
        cmpi.w #0xa,%d1
m68k_021e1c_end:
.org 0x21E20
m68k_021e20:
        bls.w (. + 56)
m68k_021e20_end:
.org 0x21E24
m68k_021e24:
        move.w %d0,0xf636:w
m68k_021e24_end:
.org 0x21E28
m68k_021e28:
        move.w #0x1,0xf712:w
m68k_021e28_end:
.org 0x21E2E
m68k_021e2e:
        addq.w #0x1,0xf362:w
m68k_021e2e_end:
.org 0x21E32
m68k_021e32:
        clr.w 0xf378:w
m68k_021e32_end:
.org 0x21E36
m68k_021e36:
        clr.w 0xf658:w
m68k_021e36_end:
.org 0x21E3A
m68k_021e3a:
        move.l #0xabd12,0xf6c0:w
m68k_021e3a_end:
.org 0x21E42
m68k_021e42:
        clr.w 0xf36a:w
m68k_021e42_end:
.org 0x21E46
m68k_021e46:
        bsr.w (. + -3000)
m68k_021e46_end:
.org 0x21E4A
m68k_021e4a:
        move.w %d0,0xaf80:w
m68k_021e4a_end:
.org 0x21E4E
m68k_021e4e:
        jsr 0x676f2:l
m68k_021e4e_end:
.org 0x21E54
m68k_021e54:
        bra.w (. + 10)
m68k_021e54_end:
.org 0x21E58
m68k_021e58:
        move.w #0x16,0xf362:w
m68k_021e58_end:
.org 0x21E5E
m68k_021e5e:
        rts
m68k_021e5e_end:
.org 0x21E60
m68k_021e60:
        bra.w (. + -2950)
m68k_021e60_end:
.org 0x21E64
m68k_021e64:
        bra.w (. + -2878)
m68k_021e64_end:
.org 0x21E68
m68k_021e68:
        bsr.w (. + -3034)
m68k_021e68_end:
.org 0x21E6C
m68k_021e6c:
        bcs.w (. + 62)
m68k_021e6c_end:
.org 0x21E70
m68k_021e70:
        bsr.w (. + -2396)
m68k_021e70_end:
.org 0x21E74
m68k_021e74:
        bsr.w (. + -2222)
m68k_021e74_end:
.org 0x21E78
m68k_021e78:
        addq.w #0x1,0xf362:w
m68k_021e78_end:
.org 0x21E7C
m68k_021e7c:
        lea.l 0xaf56:w,%a0
m68k_021e7c_end:
.org 0x21E80
m68k_021e80:
        move.w (%a0)+,%d0
m68k_021e80_end:
.org 0x21E82
m68k_021e82:
        btst.l #0xe,%d0
m68k_021e82_end:
.org 0x21E86
m68k_021e86:
        beq.b (. + -6)
m68k_021e86_end:
.org 0x21E88
m68k_021e88:
        andi.w #0xff,%d0
m68k_021e88_end:
.org 0x21E8C
m68k_021e8c:
        move.w %d0,0xf3d0:w
m68k_021e8c_end:
.org 0x21E90
m68k_021e90:
        move.w 0xf612:w,0xf38a:w
m68k_021e90_end:
.org 0x21E96
m68k_021e96:
        move.w #0x16,0xf3b0:w
m68k_021e96_end:
.org 0x21E9C
m68k_021e9c:
        clr.w 0xf36a:w
m68k_021e9c_end:
.org 0x21EA0
m68k_021ea0:
        move.w #0x406,0xf612:w
m68k_021ea0_end:
.org 0x21EA6
m68k_021ea6:
        bra.w (. + -482)
m68k_021ea6_end:
.org 0x21EAA
m68k_021eaa:
        bsr.w (. + -2316)
m68k_021eaa_end:
.org 0x21EAE
m68k_021eae:
        rts
m68k_021eae_end:
.org 0x21EB0
m68k_021eb0:
        move.w #0x200,0xf612:w
m68k_021eb0_end:
.org 0x21EB6
m68k_021eb6:
        clr.w 0xf362:w
m68k_021eb6_end:
.org 0x21EBA
m68k_021eba:
        clr.w 0xf352:w
m68k_021eba_end:
.org 0x21EBE
m68k_021ebe:
        clr.w 0xf6c4:w
m68k_021ebe_end:
.org 0x21EC2
m68k_021ec2:
        move.w #0xffff,0xf376:w
m68k_021ec2_end:
.org 0x21EC8
m68k_021ec8:
        move.w 0xf68a:w,%d0
m68k_021ec8_end:
.org 0x21ECC
m68k_021ecc:
        lsl.w #0x2,%d0
m68k_021ecc_end:
.org 0x21ECE
m68k_021ece:
        lea.l 0xdffc:w,%a0
m68k_021ece_end:
.org 0x21ED2
m68k_021ed2:
        move.l 0xf69a:w,(%a0, %d0.w)
m68k_021ed2_end:
.org 0x21ED8
m68k_021ed8:
        lea.l 0xe09c:w,%a0
m68k_021ed8_end:
.org 0x21EDC
m68k_021edc:
        move.l 0xf6a2:w,(%a0, %d0.w)
m68k_021edc_end:
.org 0x21EE2
m68k_021ee2:
        lea.l 0xed84:w,%a0
m68k_021ee2_end:
.org 0x21EE6
m68k_021ee6:
        move.l 0xf696:w,(%a0, %d0.w)
m68k_021ee6_end:
.org 0x21EEC
m68k_021eec:
        lea.l 0xee24:w,%a0
m68k_021eec_end:
.org 0x21EF0
m68k_021ef0:
        move.l 0xf69e:w,(%a0, %d0.w)
m68k_021ef0_end:
.org 0x21EF6
m68k_021ef6:
        jsr 0x1920e:l
m68k_021ef6_end:
.org 0x21EFC
m68k_021efc:
        rts
m68k_021efc_end:
.org 0x2205A
m68k_02205a:
        lea.l 0xaf56:w,%a0
m68k_02205a_end:
.org 0x2205E
m68k_02205e:
        lea.l 0xcc00:w,%a1
m68k_02205e_end:
.org 0x22062
m68k_022062:
        move.w 0xf68a:w,%d0
m68k_022062_end:
.org 0x22066
m68k_022066:
        move.w (%a0)+,%d1
m68k_022066_end:
.org 0x22068
m68k_022068:
        bmi.w (. + 16)
m68k_022068_end:
.org 0x2206C
m68k_02206c:
        btst.l #0xe,%d1
m68k_02206c_end:
.org 0x22070
m68k_022070:
        bne.b (. + -10)
m68k_022070_end:
.org 0x22072
m68k_022072:
        move.b %d0,(%a1, %d1.w)
m68k_022072_end:
.org 0x22076
m68k_022076:
        bra.b (. + -16)
m68k_022076_end:
.org 0x22078
m68k_022078:
        btst.b #0x1,0xf6d7:w
m68k_022078_end:
.org 0x2207E
m68k_02207e:
        bne.w (. + 12)
m68k_02207e_end:
.org 0x22082
m68k_022082:
        move.w 0xf68c:w,%d1
m68k_022082_end:
.org 0x22086
m68k_022086:
        bra.w (. + 8)
m68k_022086_end:
.org 0x2208A
m68k_02208a:
        move.w 0xf68e:w,%d1
m68k_02208a_end:
.org 0x2208E
m68k_02208e:
        lea.l 0xf427:w,%a0
m68k_02208e_end:
.org 0x22092
m68k_022092:
        move.b %d1,(%a0, %d0.w)
m68k_022092_end:
.org 0x22096
m68k_022096:
        rts
m68k_022096_end:
.org 0x22098
m68k_022098:
        btst.b #0x1,0xf6d7:w
m68k_022098_end:
.org 0x2209E
m68k_02209e:
        bne.w (. + 16)
m68k_02209e_end:
.org 0x220A2
m68k_0220a2:
        move.l 0xf696:w,%d0
m68k_0220a2_end:
.org 0x220A6
m68k_0220a6:
        move.l 0xf69e:w,%d1
m68k_0220a6_end:
.org 0x220AA
m68k_0220aa:
        bra.w (. + 12)
m68k_0220aa_end:
.org 0x220AE
m68k_0220ae:
        move.l 0xf69a:w,%d0
m68k_0220ae_end:
.org 0x220B2
m68k_0220b2:
        move.l 0xf6a2:w,%d1
m68k_0220b2_end:
.org 0x220B6
m68k_0220b6:
        move.w 0xf68a:w,%d2
m68k_0220b6_end:
.org 0x220BA
m68k_0220ba:
        lsl.w #0x2,%d2
m68k_0220ba_end:
.org 0x220BC
m68k_0220bc:
        lea.l 0xdffc:w,%a0
m68k_0220bc_end:
.org 0x220C0
m68k_0220c0:
        move.l %d0,(%a0, %d2.w)
m68k_0220c0_end:
.org 0x220C4
m68k_0220c4:
        lea.l 0xe09c:w,%a0
m68k_0220c4_end:
.org 0x220C8
m68k_0220c8:
        move.l %d1,(%a0, %d2.w)
m68k_0220c8_end:
.org 0x220CC
m68k_0220cc:
        btst.b #0x1,0xf6d7:w
m68k_0220cc_end:
.org 0x220D2
m68k_0220d2:
        bne.w (. + 102)
m68k_0220d2_end:
.org 0x220D6
m68k_0220d6:
        lea.l 0xe65c:w,%a0
m68k_0220d6_end:
.org 0x220DA
m68k_0220da:
        tst.l (%a0, %d2.w)
m68k_0220da_end:
.org 0x220DE
m68k_0220de:
        beq.w (. + 36)
m68k_0220de_end:
.org 0x220E2
m68k_0220e2:
        clr.l (%a0, %d2.w)
m68k_0220e2_end:
.org 0x220E6
m68k_0220e6:
        lea.l 0xe9f4:w,%a0
m68k_0220e6_end:
.org 0x220EA
m68k_0220ea:
        move.w 0xf68e:w,%d0
m68k_0220ea_end:
.org 0x220EE
m68k_0220ee:
        lsl.w #0x2,%d0
m68k_0220ee_end:
.org 0x220F0
m68k_0220f0:
        clr.l (%a0, %d0.w)
m68k_0220f0_end:
.org 0x220F4
m68k_0220f4:
        move.w 0xe700:w,%d0
m68k_0220f4_end:
.org 0x220F8
m68k_0220f8:
        move.w 0xf68e:w,%d1
m68k_0220f8_end:
.org 0x220FC
m68k_0220fc:
        bclr.l %d1,%d0
m68k_0220fc_end:
.org 0x220FE
m68k_0220fe:
        move.w %d0,0xe700:w
m68k_0220fe_end:
.org 0x22102
m68k_022102:
        lea.l 0xe9f8:w,%a0
m68k_022102_end:
.org 0x22106
m68k_022106:
        lea.l 0xe660:w,%a1
m68k_022106_end:
.org 0x2210A
m68k_02210a:
        clr.w %d0
m68k_02210a_end:
.org 0x2210C
m68k_02210c:
        move.w 0xf68a:w,%d1
m68k_02210c_end:
.org 0x22110
m68k_022110:
        cmp.b (%a0),%d1
m68k_022110_end:
.org 0x22112
m68k_022112:
        bne.w (. + 28)
m68k_022112_end:
.org 0x22116
m68k_022116:
        clr.w %d2
m68k_022116_end:
.org 0x22118
m68k_022118:
        move.b 0x1(%a0),%d2
m68k_022118_end:
.org 0x2211C
m68k_02211c:
        lsl.w #0x2,%d2
m68k_02211c_end:
.org 0x2211E
m68k_02211e:
        clr.l (%a0)
m68k_02211e_end:
.org 0x22120
m68k_022120:
        clr.l (%a1, %d2.w)
m68k_022120_end:
.org 0x22124
m68k_022124:
        move.w 0xe700:w,%d3
m68k_022124_end:
.org 0x22128
m68k_022128:
        bclr.l %d0,%d3
m68k_022128_end:
.org 0x2212A
m68k_02212a:
        move.w %d3,0xe700:w
m68k_02212a_end:
.org 0x2212E
m68k_02212e:
        addq.w #0x4,%a0
m68k_02212e_end:
.org 0x22130
m68k_022130:
        addq.w #0x1,%d0
m68k_022130_end:
.org 0x22132
m68k_022132:
        cmpi.w #0x10,%d0
m68k_022132_end:
.org 0x22136
m68k_022136:
        bcs.b (. + -38)
m68k_022136_end:
.org 0x22138
m68k_022138:
        rts
m68k_022138_end:
.org 0x2213A
m68k_02213a:
        lea.l 0xa050:w,%a0
m68k_02213a_end:
.org 0x2213E
m68k_02213e:
        move.w 0xf68a:w,%d0
m68k_02213e_end:
.org 0x22142
m68k_022142:
        move.w #0xff,%d1
m68k_022142_end:
.org 0x22146
m68k_022146:
        move.b (%a0, %d1.w),%d2
m68k_022146_end:
.org 0x2214A
m68k_02214a:
        andi.w #0x3f,%d2
m68k_02214a_end:
.org 0x2214E
m68k_02214e:
        cmp.b %d0,%d2
m68k_02214e_end:
.org 0x22150
m68k_022150:
        bne.w (. + 8)
m68k_022150_end:
.org 0x22154
m68k_022154:
        clr.b (%a0, %d1.w)
m68k_022154_end:
.org 0x22158
m68k_022158:
        dbra %d1,(. + -18)
m68k_022158_end:
.org 0x2215C
m68k_02215c:
        rts
m68k_02215c_end:
.org 0x2215E
m68k_02215e:
        btst.b #0x1,0xf6d7:w
m68k_02215e_end:
.org 0x22164
m68k_022164:
        bne.w (. + 126)
m68k_022164_end:
.org 0x22168
m68k_022168:
        lea.l 0xcc00:w,%a0
m68k_022168_end:
.org 0x2216C
m68k_02216c:
        lea.l 0xa050:w,%a1
m68k_02216c_end:
.org 0x22170
m68k_022170:
        move.w 0xf68a:w,%d0
m68k_022170_end:
.org 0x22174
m68k_022174:
        move.w %d0,%d2
m68k_022174_end:
.org 0x22176
m68k_022176:
        bset.l #0x6,%d0
m68k_022176_end:
.org 0x2217A
m68k_02217a:
        move.w #0xff,%d1
m68k_02217a_end:
.org 0x2217E
m68k_02217e:
        move.w 0xf68e:w,%d4
m68k_02217e_end:
.org 0x22182
m68k_022182:
        addi.w #0x69,%d4
m68k_022182_end:
.org 0x22186
m68k_022186:
        cmp.b (%a0, %d1.w),%d0
m68k_022186_end:
.org 0x2218A
m68k_02218a:
        bne.w (. + 26)
m68k_02218a_end:
.org 0x2218E
m68k_02218e:
        move.b (%a1, %d1.w),%d3
m68k_02218e_end:
.org 0x22192
m68k_022192:
        beq.w (. + 18)
m68k_022192_end:
.org 0x22196
m68k_022196:
        andi.w #0x3f,%d3
m68k_022196_end:
.org 0x2219A
m68k_02219a:
        cmp.b %d2,%d3
m68k_02219a_end:
.org 0x2219C
m68k_02219c:
        beq.w (. + 8)
m68k_02219c_end:
.org 0x221A0
m68k_0221a0:
        move.b %d4,(%a0, %d1.w)
m68k_0221a0_end:
.org 0x221A4
m68k_0221a4:
        dbra %d1,(. + -30)
m68k_0221a4_end:
.org 0x221A8
m68k_0221a8:
        lea.l 0x9000:w,%a1
m68k_0221a8_end:
.org 0x221AC
m68k_0221ac:
        move.w 0xf68e:w,%d2
m68k_0221ac_end:
.org 0x221B0
m68k_0221b0:
        move.b (%a1),%d1
m68k_0221b0_end:
.org 0x221B2
m68k_0221b2:
        andi.w #0xf,%d1
m68k_0221b2_end:
.org 0x221B6
m68k_0221b6:
        beq.w (. + 44)
m68k_0221b6_end:
.org 0x221BA
m68k_0221ba:
        cmp.b 0x4(%a1),%d2
m68k_0221ba_end:
.org 0x221BE
m68k_0221be:
        bne.w (. + 30)
m68k_0221be_end:
.org 0x221C2
m68k_0221c2:
        move.w %d1,%d3
m68k_0221c2_end:
.org 0x221C4
m68k_0221c4:
        subq.w #0x1,%d3
m68k_0221c4_end:
.org 0x221C6
m68k_0221c6:
        clr.w %d5
m68k_0221c6_end:
.org 0x221C8
m68k_0221c8:
        move.b 0xd(%a1, %d3.w),%d5
m68k_0221c8_end:
.org 0x221CC
m68k_0221cc:
        cmp.b (%a0, %d5.w),%d0
m68k_0221cc_end:
.org 0x221D0
m68k_0221d0:
        bne.w (. + 8)
m68k_0221d0_end:
.org 0x221D4
m68k_0221d4:
        move.b %d4,(%a0, %d5.w)
m68k_0221d4_end:
.org 0x221D8
m68k_0221d8:
        dbra %d3,(. + -16)
m68k_0221d8_end:
.org 0x221DC
m68k_0221dc:
        lea.l 0xd(%a1, %d1.w),%a1
m68k_0221dc_end:
.org 0x221E0
m68k_0221e0:
        bra.b (. + -48)
m68k_0221e0_end:
.org 0x221E2
m68k_0221e2:
        rts
m68k_0221e2_end:
.org 0x224DE
m68k_0224de:
        bsr.w (. + 174)
m68k_0224de_end:
.org 0x224E2
m68k_0224e2:
        bcs.w (. + 16)
m68k_0224e2_end:
.org 0x224E6
m68k_0224e6:
        bsr.w (. + 2818)
m68k_0224e6_end:
.org 0x224EA
m68k_0224ea:
        bcs.w (. + 8)
m68k_0224ea_end:
.org 0x224EE
m68k_0224ee:
        bsr.w (. + 6)
m68k_0224ee_end:
.org 0x224F2
m68k_0224f2:
        rts
m68k_0224f2_end:
.org 0x224F4
m68k_0224f4:
        lea.l 0xa654:w,%a0
m68k_0224f4_end:
.org 0x224F8
m68k_0224f8:
        tst.b (%a0, %d7.w)
m68k_0224f8_end:
.org 0x224FC
m68k_0224fc:
        bne.w (. + 142)
m68k_0224fc_end:
.org 0x22500
m68k_022500:
        lea.l 0xff3cc2:l,%a0
m68k_022500_end:
.org 0x22506
m68k_022506:
        tst.b (%a0, %d7.w)
m68k_022506_end:
.org 0x2250A
m68k_02250a:
        bne.w (. + 128)
m68k_02250a_end:
.org 0x2250E
m68k_02250e:
        lea.l 0xff3dc2:l,%a1
m68k_02250e_end:
.org 0x22514
m68k_022514:
        tst.b (%a1, %d7.w)
m68k_022514_end:
.org 0x22518
m68k_022518:
        bne.w (. + 114)
m68k_022518_end:
.org 0x2251C
m68k_02251c:
        jsr 0x1a438:l
m68k_02251c_end:
.org 0x22522
m68k_022522:
        lea.l 0xa150:w,%a1
m68k_022522_end:
.org 0x22526
m68k_022526:
        move.w %d7,%d0
m68k_022526_end:
.org 0x22528
m68k_022528:
        lsl.w #0x2,%d0
m68k_022528_end:
.org 0x2252A
m68k_02252a:
        move.w (%a1, %d0.w),%d1
m68k_02252a_end:
.org 0x2252E
m68k_02252e:
        lsr.w #0x7,%d1
m68k_02252e_end:
.org 0x22530
m68k_022530:
        move.w 0x2(%a1, %d0.w),%d2
m68k_022530_end:
.org 0x22534
m68k_022534:
        lsr.w #0x7,%d2
m68k_022534_end:
.org 0x22536
m68k_022536:
        jsr 0x1a44e:l
m68k_022536_end:
.org 0x2253C
m68k_02253c:
        cmpi.b #0x6,%d0
m68k_02253c_end:
.org 0x22540
m68k_022540:
        beq.w (. + 70)
m68k_022540_end:
.org 0x22544
m68k_022544:
        lea.l 0xae2f6:l,%a0
m68k_022544_end:
.org 0x2254A
m68k_02254a:
        move.w 0xf68a:w,%d0
m68k_02254a_end:
.org 0x2254E
m68k_02254e:
        lsl.w #0x2,%d0
m68k_02254e_end:
.org 0x22550
m68k_022550:
        lea.l 0xff2c00:l,%a1
m68k_022550_end:
.org 0x22556
m68k_022556:
        move.w %d7,%d1
m68k_022556_end:
.org 0x22558
m68k_022558:
        lsl.w #0x2,%d1
m68k_022558_end:
.org 0x2255A
m68k_02255a:
        move.w (%a0, %d0.w),%d2
m68k_02255a_end:
.org 0x2255E
m68k_02255e:
        lsr.w #0x7,%d2
m68k_02255e_end:
.org 0x22560
m68k_022560:
        move.w %d2,(%a1, %d1.w)
m68k_022560_end:
.org 0x22564
m68k_022564:
        move.w 0x2(%a0, %d0.w),%d2
m68k_022564_end:
.org 0x22568
m68k_022568:
        lsr.w #0x7,%d2
m68k_022568_end:
.org 0x2256A
m68k_02256a:
        move.w %d2,0x2(%a1, %d1.w)
m68k_02256a_end:
.org 0x2256E
m68k_02256e:
        lea.l 0xae28:w,%a0
m68k_02256e_end:
.org 0x22572
m68k_022572:
        move.b #0x1,(%a0, %d7.w)
m68k_022572_end:
.org 0x22578
m68k_022578:
        jsr 0x1dcaa:l
m68k_022578_end:
.org 0x2257E
m68k_02257e:
        ori.w #0x1,%sr
m68k_02257e_end:
.org 0x22582
m68k_022582:
        bra.w (. + 8)
m68k_022582_end:
.org 0x22586
m68k_022586:
        andi.w #0xfffe,%sr
m68k_022586_end:
.org 0x2258A
m68k_02258a:
        rts
m68k_02258a_end:
.org 0x2258C
m68k_02258c:
        lea.l 0xc800:w,%a0
m68k_02258c_end:
.org 0x22590
m68k_022590:
        move.w %d7,%d0
m68k_022590_end:
.org 0x22592
m68k_022592:
        lsl.w #0x2,%d0
m68k_022592_end:
.org 0x22594
m68k_022594:
        move.l (%a0, %d0.w),%d1
m68k_022594_end:
.org 0x22598
m68k_022598:
        cmpi.l #0xc8,%d1
m68k_022598_end:
.org 0x2259E
m68k_02259e:
        bls.w (. + 38)
m68k_02259e_end:
.org 0x225A2
m68k_0225a2:
        cmpi.l #0x1f4,%d1
m68k_0225a2_end:
.org 0x225A8
m68k_0225a8:
        bhi.w (. + 84)
m68k_0225a8_end:
.org 0x225AC
m68k_0225ac:
        lea.l 0xb000:w,%a0
m68k_0225ac_end:
.org 0x225B0
m68k_0225b0:
        lsr.w #0x1,%d0
m68k_0225b0_end:
.org 0x225B2
m68k_0225b2:
        move.w (%a0, %d0.w),%d1
m68k_0225b2_end:
.org 0x225B6
m68k_0225b6:
        lsr.w #0x2,%d1
m68k_0225b6_end:
.org 0x225B8
m68k_0225b8:
        lea.l 0xb200:w,%a0
m68k_0225b8_end:
.org 0x225BC
m68k_0225bc:
        cmp.w (%a0, %d0.w),%d1
m68k_0225bc_end:
.org 0x225C0
m68k_0225c0:
        bcs.w (. + 60)
m68k_0225c0_end:
.org 0x225C4
m68k_0225c4:
        move.w #0x2,%d2
m68k_0225c4_end:
.org 0x225C8
m68k_0225c8:
        lea.l 0xe640:w,%a0
m68k_0225c8_end:
.org 0x225CC
m68k_0225cc:
        move.w 0xf68e:w,%d0
m68k_0225cc_end:
.org 0x225D0
m68k_0225d0:
        lsl.w #0x1,%d0
m68k_0225d0_end:
.org 0x225D2
m68k_0225d2:
        cmp.w (%a0, %d0.w),%d7
m68k_0225d2_end:
.org 0x225D6
m68k_0225d6:
        bne.w (. + 16)
m68k_0225d6_end:
.org 0x225DA
m68k_0225da:
        move.w #0x4,%d2
m68k_0225da_end:
.org 0x225DE
m68k_0225de:
        bsr.w (. + 290)
m68k_0225de_end:
.org 0x225E2
m68k_0225e2:
        bcc.w (. + 210)
m68k_0225e2_end:
.org 0x225E6
m68k_0225e6:
        jsr 0x83d4:l
m68k_0225e6_end:
.org 0x225EC
m68k_0225ec:
        andi.l #0xffff,%d0
m68k_0225ec_end:
.org 0x225F2
m68k_0225f2:
        lsl.l #0x3,%d0
m68k_0225f2_end:
.org 0x225F4
m68k_0225f4:
        swap %d0
m68k_0225f4_end:
.org 0x225F6
m68k_0225f6:
        cmp.w %d2,%d0
m68k_0225f6_end:
.org 0x225F8
m68k_0225f8:
        bcs.w (. + 128)
m68k_0225f8_end:
.org 0x225FC
m68k_0225fc:
        bsr.w (. + 186)
m68k_0225fc_end:
.org 0x22600
m68k_022600:
        cmpi.w #0x3,%d0
m68k_022600_end:
.org 0x22604
m68k_022604:
        bcs.w (. + 34)
m68k_022604_end:
.org 0x22608
m68k_022608:
        tst.l 0xf6a2:w
m68k_022608_end:
.org 0x2260C
m68k_02260c:
        bne.w (. + 26)
m68k_02260c_end:
.org 0x22610
m68k_022610:
        move.l 0xf76c:w,%d2
m68k_022610_end:
.org 0x22614
m68k_022614:
        divu.w #0x3,%d2
m68k_022614_end:
.org 0x22618
m68k_022618:
        andi.l #0xffff,%d2
m68k_022618_end:
.org 0x2261E
m68k_02261e:
        cmp.l 0xf6a0:w,%d2
m68k_02261e_end:
.org 0x22622
m68k_022622:
        bls.w (. + 44)
m68k_022622_end:
.org 0x22626
m68k_022626:
        bsr.w (. + 188)
m68k_022626_end:
.org 0x2262A
m68k_02262a:
        cmp.w %d0,%d2
m68k_02262a_end:
.org 0x2262C
m68k_02262c:
        bhi.w (. + 68)
m68k_02262c_end:
.org 0x22630
m68k_022630:
        cmpi.l #0x3e8,%d3
m68k_022630_end:
.org 0x22636
m68k_022636:
        bhi.w (. + 58)
m68k_022636_end:
.org 0x2263A
m68k_02263a:
        lsl.l #0x1,%d3
m68k_02263a_end:
.org 0x2263C
m68k_02263c:
        cmp.l %d1,%d3
m68k_02263c_end:
.org 0x2263E
m68k_02263e:
        bhi.w (. + 50)
m68k_02263e_end:
.org 0x22642
m68k_022642:
        move.l 0xf768:w,%d0
m68k_022642_end:
.org 0x22646
m68k_022646:
        cmp.l 0xf6a2:w,%d0
m68k_022646_end:
.org 0x2264A
m68k_02264a:
        bcs.w (. + 38)
m68k_02264a_end:
.org 0x2264E
m68k_02264e:
        move.w #0x2,%d2
m68k_02264e_end:
.org 0x22652
m68k_022652:
        bsr.w (. + 174)
m68k_022652_end:
.org 0x22656
m68k_022656:
        bcc.w (. + 94)
m68k_022656_end:
.org 0x2265A
m68k_02265a:
        jsr 0x83d4:l
m68k_02265a_end:
.org 0x22660
m68k_022660:
        andi.l #0xffff,%d0
m68k_022660_end:
.org 0x22666
m68k_022666:
        lsl.l #0x3,%d0
m68k_022666_end:
.org 0x22668
m68k_022668:
        swap %d0
m68k_022668_end:
.org 0x2266A
m68k_02266a:
        cmp.w %d2,%d0
m68k_02266a_end:
.org 0x2266C
m68k_02266c:
        bcs.w (. + 12)
m68k_02266c_end:
.org 0x22670
m68k_022670:
        andi.w #0xfffe,%sr
m68k_022670_end:
.org 0x22674
m68k_022674:
        bra.w (. + 64)
m68k_022674_end:
.org 0x22678
m68k_022678:
        move.w %d7,0xf3a6:w
m68k_022678_end:
.org 0x2267C
m68k_02267c:
        move.w %d7,-(%a7)
m68k_02267c_end:
.org 0x2267E
m68k_02267e:
        jsr 0x17c8a:l
m68k_02267e_end:
.org 0x22684
m68k_022684:
        move.w (%a7)+,%d7
m68k_022684_end:
.org 0x22686
m68k_022686:
        tst.w 0xf6ec:w
m68k_022686_end:
.org 0x2268A
m68k_02268a:
        bmi.b (. + -26)
m68k_02268a_end:
.org 0x2268C
m68k_02268c:
        jsr 0x17f30:l
m68k_02268c_end:
.org 0x22692
m68k_022692:
        move.w 0xf3a6:w,0xf3d2:w
m68k_022692_end:
.org 0x22698
m68k_022698:
        move.w #0x12e,0xf740:w
m68k_022698_end:
.org 0x2269E
m68k_02269e:
        bchg.b #0x1,0xf6d7:w
m68k_02269e_end:
.org 0x226A4
m68k_0226a4:
        jsr 0x260e4:l
m68k_0226a4_end:
.org 0x226AA
m68k_0226aa:
        bchg.b #0x1,0xf6d7:w
m68k_0226aa_end:
.org 0x226B0
m68k_0226b0:
        ori.w #0x1,%sr
m68k_0226b0_end:
.org 0x226B4
m68k_0226b4:
        rts
m68k_0226b4_end:
.org 0x226B6
m68k_0226b6:
        lea.l 0xa550:w,%a0
m68k_0226b6_end:
.org 0x226BA
m68k_0226ba:
        btst.b #0x1,0xf6d7:w
m68k_0226ba_end:
.org 0x226C0
m68k_0226c0:
        bne.w (. + 8)
m68k_0226c0_end:
.org 0x226C4
m68k_0226c4:
        lea.l 0xa5a4:w,%a0
m68k_0226c4_end:
.org 0x226C8
m68k_0226c8:
        lea.l 0xc800:w,%a1
m68k_0226c8_end:
.org 0x226CC
m68k_0226cc:
        clr.w %d0
m68k_0226cc_end:
.org 0x226CE
m68k_0226ce:
        moveq #0,%d1
m68k_0226ce_end:
.org 0x226D0
m68k_0226d0:
        move.w (%a0)+,%d2
m68k_0226d0_end:
.org 0x226D2
m68k_0226d2:
        bmi.w (. + 14)
m68k_0226d2_end:
.org 0x226D6
m68k_0226d6:
        addq.w #0x1,%d0
m68k_0226d6_end:
.org 0x226D8
m68k_0226d8:
        lsl.w #0x2,%d2
m68k_0226d8_end:
.org 0x226DA
m68k_0226da:
        add.l (%a1, %d2.w),%d1
m68k_0226da_end:
.org 0x226DE
m68k_0226de:
        bra.b (. + -14)
m68k_0226de_end:
.org 0x226E0
m68k_0226e0:
        rts
m68k_0226e0_end:
.org 0x226E2
m68k_0226e2:
        lea.l 0xa5a4:w,%a0
m68k_0226e2_end:
.org 0x226E6
m68k_0226e6:
        lea.l 0xc800:w,%a1
m68k_0226e6_end:
.org 0x226EA
m68k_0226ea:
        clr.w %d2
m68k_0226ea_end:
.org 0x226EC
m68k_0226ec:
        moveq #0,%d3
m68k_0226ec_end:
.org 0x226EE
m68k_0226ee:
        move.w (%a0)+,%d5
m68k_0226ee_end:
.org 0x226F0
m68k_0226f0:
        bmi.w (. + 14)
m68k_0226f0_end:
.org 0x226F4
m68k_0226f4:
        addq.w #0x3,%d2
m68k_0226f4_end:
.org 0x226F6
m68k_0226f6:
        lsl.w #0x2,%d5
m68k_0226f6_end:
.org 0x226F8
m68k_0226f8:
        add.l (%a1, %d5.w),%d3
m68k_0226f8_end:
.org 0x226FC
m68k_0226fc:
        bra.b (. + -14)
m68k_0226fc_end:
.org 0x226FE
m68k_0226fe:
        rts
m68k_0226fe_end:
.org 0x22700
m68k_022700:
        move.w 0xf68a:w,%d3
m68k_022700_end:
.org 0x22704
m68k_022704:
        subq.w #0x1,%d3
m68k_022704_end:
.org 0x22706
m68k_022706:
        move.w #0x27,%d4
m68k_022706_end:
.org 0x2270A
m68k_02270a:
        lea.l 0xf428:w,%a0
m68k_02270a_end:
.org 0x2270E
m68k_02270e:
        move.w 0xf68e:w,%d0
m68k_02270e_end:
.org 0x22712
m68k_022712:
        btst.b #0x1,0xf6d7:w
m68k_022712_end:
.org 0x22718
m68k_022718:
        bne.w (. + 8)
m68k_022718_end:
.org 0x2271C
m68k_02271c:
        move.w 0xf68c:w,%d0
m68k_02271c_end:
.org 0x22720
m68k_022720:
        cmp.b (%a0, %d4.w),%d0
m68k_022720_end:
.org 0x22724
m68k_022724:
        bne.w (. + 10)
m68k_022724_end:
.org 0x22728
m68k_022728:
        cmp.w %d4,%d3
m68k_022728_end:
.org 0x2272A
m68k_02272a:
        bne.w (. + 16)
m68k_02272a_end:
.org 0x2272E
m68k_02272e:
        dbra %d4,(. + -14)
m68k_02272e_end:
.org 0x22732
m68k_022732:
        andi.w #0xfffe,%sr
m68k_022732_end:
.org 0x22736
m68k_022736:
        bra.w (. + 8)
m68k_022736_end:
.org 0x2273A
m68k_02273a:
        ori.w #0x1,%sr
m68k_02273a_end:
.org 0x2273E
m68k_02273e:
        rts
m68k_02273e_end:
.org 0x22740
m68k_022740:
        bsr.w (. + 22)
m68k_022740_end:
.org 0x22744
m68k_022744:
        bcs.w (. + 16)
m68k_022744_end:
.org 0x22748
m68k_022748:
        bsr.w (. + 578)
m68k_022748_end:
.org 0x2274C
m68k_02274c:
        bcs.w (. + 8)
m68k_02274c_end:
.org 0x22750
m68k_022750:
        bsr.w (. + 152)
m68k_022750_end:
.org 0x22754
m68k_022754:
        rts
m68k_022754_end:
.org 0x22756
m68k_022756:
        bsr.b (. + -86)
m68k_022756_end:
.org 0x22758
m68k_022758:
        bcc.w (. + 74)
m68k_022758_end:
.org 0x2275C
m68k_02275c:
        move.w %d7,%d0
m68k_02275c_end:
.org 0x2275E
m68k_02275e:
        lsl.w #0x2,%d0
m68k_02275e_end:
.org 0x22760
m68k_022760:
        lea.l 0xc800:w,%a2
m68k_022760_end:
.org 0x22764
m68k_022764:
        cmpi.l #0xc8,(%a2, %d0.w)
m68k_022764_end:
.org 0x2276C
m68k_02276c:
        bls.w (. + 40)
m68k_02276c_end:
.org 0x22770
m68k_022770:
        cmpi.l #0x1f4,(%a2, %d0.w)
m68k_022770_end:
.org 0x22778
m68k_022778:
        bhi.w (. + 42)
m68k_022778_end:
.org 0x2277C
m68k_02277c:
        lsr.w #0x1,%d0
m68k_02277c_end:
.org 0x2277E
m68k_02277e:
        lea.l 0xb000:w,%a2
m68k_02277e_end:
.org 0x22782
m68k_022782:
        move.w (%a2, %d0.w),%d1
m68k_022782_end:
.org 0x22786
m68k_022786:
        lsr.w #0x2,%d1
m68k_022786_end:
.org 0x22788
m68k_022788:
        lea.l 0xb200:w,%a2
m68k_022788_end:
.org 0x2278C
m68k_02278c:
        cmp.w (%a2, %d0.w),%d1
m68k_02278c_end:
.org 0x22790
m68k_022790:
        bcs.w (. + 18)
m68k_022790_end:
.org 0x22794
m68k_022794:
        jsr 0x83d4:l
m68k_022794_end:
.org 0x2279A
m68k_02279a:
        btst.l #0x0,%d0
m68k_02279a_end:
.org 0x2279E
m68k_02279e:
        bne.w (. + 12)
m68k_02279e_end:
.org 0x227A2
m68k_0227a2:
        andi.w #0xfffe,%sr
m68k_0227a2_end:
.org 0x227A6
m68k_0227a6:
        bra.w (. + 64)
m68k_0227a6_end:
.org 0x227AA
m68k_0227aa:
        move.w %d7,-(%a7)
m68k_0227aa_end:
.org 0x227AC
m68k_0227ac:
        jsr 0x17c8a:l
m68k_0227ac_end:
.org 0x227B2
m68k_0227b2:
        move.w (%a7)+,%d7
m68k_0227b2_end:
.org 0x227B4
m68k_0227b4:
        tst.w 0xf6ec:w
m68k_0227b4_end:
.org 0x227B8
m68k_0227b8:
        bmi.b (. + -22)
m68k_0227b8_end:
.org 0x227BA
m68k_0227ba:
        move.w %d7,0xf3a6:w
m68k_0227ba_end:
.org 0x227BE
m68k_0227be:
        jsr 0x17f30:l
m68k_0227be_end:
.org 0x227C4
m68k_0227c4:
        move.w 0xf3a6:w,0xf3d2:w
m68k_0227c4_end:
.org 0x227CA
m68k_0227ca:
        move.w #0x12e,0xf740:w
m68k_0227ca_end:
.org 0x227D0
m68k_0227d0:
        bchg.b #0x1,0xf6d7:w
m68k_0227d0_end:
.org 0x227D6
m68k_0227d6:
        jsr 0x260e4:l
m68k_0227d6_end:
.org 0x227DC
m68k_0227dc:
        bchg.b #0x1,0xf6d7:w
m68k_0227dc_end:
.org 0x227E2
m68k_0227e2:
        ori.w #0x1,%sr
m68k_0227e2_end:
.org 0x227E6
m68k_0227e6:
        rts
m68k_0227e6_end:
.org 0x227E8
m68k_0227e8:
        lea.l 0xa654:w,%a0
m68k_0227e8_end:
.org 0x227EC
m68k_0227ec:
        tst.b (%a0, %d7.w)
m68k_0227ec_end:
.org 0x227F0
m68k_0227f0:
        bne.w (. + 160)
m68k_0227f0_end:
.org 0x227F4
m68k_0227f4:
        lea.l 0xff3cc2:l,%a0
m68k_0227f4_end:
.org 0x227FA
m68k_0227fa:
        tst.b (%a0, %d7.w)
m68k_0227fa_end:
.org 0x227FE
m68k_0227fe:
        bne.w (. + 146)
m68k_0227fe_end:
.org 0x22802
m68k_022802:
        lea.l 0xff3dc2:l,%a1
m68k_022802_end:
.org 0x22808
m68k_022808:
        tst.b (%a1, %d7.w)
m68k_022808_end:
.org 0x2280C
m68k_02280c:
        bne.w (. + 132)
m68k_02280c_end:
.org 0x22810
m68k_022810:
        lea.l 0xa150:w,%a0
m68k_022810_end:
.org 0x22814
m68k_022814:
        move.w %d7,%d6
m68k_022814_end:
.org 0x22816
m68k_022816:
        lsl.w #0x2,%d6
m68k_022816_end:
.org 0x22818
m68k_022818:
        move.w (%a0, %d6.w),%d0
m68k_022818_end:
.org 0x2281C
m68k_02281c:
        move.w 0x2(%a0, %d6.w),%d1
m68k_02281c_end:
.org 0x22820
m68k_022820:
        bsr.w (. + 114)
m68k_022820_end:
.org 0x22824
m68k_022824:
        bcs.w (. + 12)
m68k_022824_end:
.org 0x22828
m68k_022828:
        bsr.w (. + 218)
m68k_022828_end:
.org 0x2282C
m68k_02282c:
        bcc.w (. + 8)
m68k_02282c_end:
.org 0x22830
m68k_022830:
        bsr.w (. + 328)
m68k_022830_end:
.org 0x22834
m68k_022834:
        lea.l 0xff2c00:l,%a0
m68k_022834_end:
.org 0x2283A
m68k_02283a:
        move.w %d7,%d1
m68k_02283a_end:
.org 0x2283C
m68k_02283c:
        lsl.w #0x2,%d1
m68k_02283c_end:
.org 0x2283E
m68k_02283e:
        lsr.w #0x7,%d4
m68k_02283e_end:
.org 0x22840
m68k_022840:
        move.w %d4,(%a0, %d1.w)
m68k_022840_end:
.org 0x22844
m68k_022844:
        lsr.w #0x7,%d0
m68k_022844_end:
.org 0x22846
m68k_022846:
        move.w %d0,0x2(%a0, %d1.w)
m68k_022846_end:
.org 0x2284A
m68k_02284a:
        lea.l 0xae28:w,%a0
m68k_02284a_end:
.org 0x2284E
m68k_02284e:
        move.b #0x1,(%a0, %d7.w)
m68k_02284e_end:
.org 0x22854
m68k_022854:
        jsr 0x1a438:l
m68k_022854_end:
.org 0x2285A
m68k_02285a:
        lea.l 0xa150:w,%a1
m68k_02285a_end:
.org 0x2285E
m68k_02285e:
        move.w %d7,%d0
m68k_02285e_end:
.org 0x22860
m68k_022860:
        lsl.w #0x2,%d0
m68k_022860_end:
.org 0x22862
m68k_022862:
        move.w (%a1, %d0.w),%d1
m68k_022862_end:
.org 0x22866
m68k_022866:
        lsr.w #0x7,%d1
m68k_022866_end:
.org 0x22868
m68k_022868:
        move.w 0x2(%a1, %d0.w),%d2
m68k_022868_end:
.org 0x2286C
m68k_02286c:
        lsr.w #0x7,%d2
m68k_02286c_end:
.org 0x2286E
m68k_02286e:
        jsr 0x1a44e:l
m68k_02286e_end:
.org 0x22874
m68k_022874:
        cmpi.b #0x6,%d0
m68k_022874_end:
.org 0x22878
m68k_022878:
        beq.w (. + 14)
m68k_022878_end:
.org 0x2287C
m68k_02287c:
        jsr 0x1dcaa:l
m68k_02287c_end:
.org 0x22882
m68k_022882:
        bra.w (. + 14)
m68k_022882_end:
.org 0x22886
m68k_022886:
        move.w %d7,0xf3a6:w
m68k_022886_end:
.org 0x2288A
m68k_02288a:
        jsr 0x1db7c:l
m68k_02288a_end:
.org 0x22890
m68k_022890:
        rts
m68k_022890_end:
.org 0x22892
m68k_022892:
        lea.l 0xabda8:l,%a0
m68k_022892_end:
.org 0x22898
m68k_022898:
        move.w 0xf68a:w,%d2
m68k_022898_end:
.org 0x2289C
m68k_02289c:
        lsl.w #0x5,%d2
m68k_02289c_end:
.org 0x2289E
m68k_02289e:
        adda.w %d2,%a0
m68k_02289e_end:
.org 0x228A0
m68k_0228a0:
        lea.l 0x9fff:w,%a1
m68k_0228a0_end:
.org 0x228A4
m68k_0228a4:
        move.w 0xf68a:w,%d2
m68k_0228a4_end:
.org 0x228A8
m68k_0228a8:
        clr.w %d3
m68k_0228a8_end:
.org 0x228AA
m68k_0228aa:
        move.b (%a1, %d2.w),%d3
m68k_0228aa_end:
.org 0x228AE
m68k_0228ae:
        lsl.w #0x1,%d3
m68k_0228ae_end:
.org 0x228B0
m68k_0228b0:
        clr.w %d2
m68k_0228b0_end:
.org 0x228B2
m68k_0228b2:
        move.b (%a0, %d3.w),%d2
m68k_0228b2_end:
.org 0x228B6
m68k_0228b6:
        lsl.w #0x3,%d2
m68k_0228b6_end:
.org 0x228B8
m68k_0228b8:
        lsl.w #0x7,%d2
m68k_0228b8_end:
.org 0x228BA
m68k_0228ba:
        move.b 0x1(%a0, %d3.w),%d3
m68k_0228ba_end:
.org 0x228BE
m68k_0228be:
        andi.b #0xff,%d3
m68k_0228be_end:
.org 0x228C2
m68k_0228c2:
        lsl.w #0x3,%d3
m68k_0228c2_end:
.org 0x228C4
m68k_0228c4:
        lsl.w #0x7,%d3
m68k_0228c4_end:
.org 0x228C6
m68k_0228c6:
        move.w %d3,%d4
m68k_0228c6_end:
.org 0x228C8
m68k_0228c8:
        cmpi.w #0x5000,%d4
m68k_0228c8_end:
.org 0x228CC
m68k_0228cc:
        bhi.w (. + 30)
m68k_0228cc_end:
.org 0x228D0
m68k_0228d0:
        addi.w #0x3400,%d4
m68k_0228d0_end:
.org 0x228D4
m68k_0228d4:
        cmp.w %d4,%d1
m68k_0228d4_end:
.org 0x228D6
m68k_0228d6:
        bcs.w (. + 12)
m68k_0228d6_end:
.org 0x228DA
m68k_0228da:
        andi.w #0xfffe,%sr
m68k_0228da_end:
.org 0x228DE
m68k_0228de:
        bra.w (. + 34)
m68k_0228de_end:
.org 0x228E2
m68k_0228e2:
        ori.w #0x1,%sr
m68k_0228e2_end:
.org 0x228E6
m68k_0228e6:
        bra.w (. + 26)
m68k_0228e6_end:
.org 0x228EA
m68k_0228ea:
        subi.w #0x3400,%d4
m68k_0228ea_end:
.org 0x228EE
m68k_0228ee:
        cmp.w %d4,%d1
m68k_0228ee_end:
.org 0x228F0
m68k_0228f0:
        bhi.w (. + 12)
m68k_0228f0_end:
.org 0x228F4
m68k_0228f4:
        andi.w #0xfffe,%sr
m68k_0228f4_end:
.org 0x228F8
m68k_0228f8:
        bra.w (. + 8)
m68k_0228f8_end:
.org 0x228FC
m68k_0228fc:
        ori.w #0x1,%sr
m68k_0228fc_end:
.org 0x22900
m68k_022900:
        rts
m68k_022900_end:
.org 0x22902
m68k_022902:
        move.w %d2,%d5
m68k_022902_end:
.org 0x22904
m68k_022904:
        subi.w #0x1400,%d5
m68k_022904_end:
.org 0x22908
m68k_022908:
        bcs.w (. + 106)
m68k_022908_end:
.org 0x2290C
m68k_02290c:
        cmpi.w #0x2000,%d5
m68k_02290c_end:
.org 0x22910
m68k_022910:
        bls.w (. + 8)
m68k_022910_end:
.org 0x22914
m68k_022914:
        move.w #0x2000,%d5
m68k_022914_end:
.org 0x22918
m68k_022918:
        jsr 0x83d4:l
m68k_022918_end:
.org 0x2291E
m68k_02291e:
        andi.l #0xffff,%d0
m68k_02291e_end:
.org 0x22924
m68k_022924:
        mulu.w %d0,%d5
m68k_022924_end:
.org 0x22926
m68k_022926:
        swap %d5
m68k_022926_end:
.org 0x22928
m68k_022928:
        move.w %d2,%d4
m68k_022928_end:
.org 0x2292A
m68k_02292a:
        subi.w #0x800,%d4
m68k_02292a_end:
.org 0x2292E
m68k_02292e:
        sub.w %d5,%d4
m68k_02292e_end:
.org 0x22930
m68k_022930:
        jsr 0x83d4:l
m68k_022930_end:
.org 0x22936
m68k_022936:
        andi.l #0xffff,%d0
m68k_022936_end:
.org 0x2293C
m68k_02293c:
        mulu.w #0x1800,%d0
m68k_02293c_end:
.org 0x22940
m68k_022940:
        swap %d0
m68k_022940_end:
.org 0x22942
m68k_022942:
        cmpi.w #0x5000,%d3
m68k_022942_end:
.org 0x22946
m68k_022946:
        bhi.w (. + 14)
m68k_022946_end:
.org 0x2294A
m68k_02294a:
        add.w %d3,%d0
m68k_02294a_end:
.org 0x2294C
m68k_02294c:
        addi.w #0x1c00,%d0
m68k_02294c_end:
.org 0x22950
m68k_022950:
        bra.w (. + 14)
m68k_022950_end:
.org 0x22954
m68k_022954:
        move.w %d3,%d1
m68k_022954_end:
.org 0x22956
m68k_022956:
        subi.w #0x1c00,%d1
m68k_022956_end:
.org 0x2295A
m68k_02295a:
        sub.w %d0,%d1
m68k_02295a_end:
.org 0x2295C
m68k_02295c:
        move.w %d1,%d0
m68k_02295c_end:
.org 0x2295E
m68k_02295e:
        move.w %d0,%d1
m68k_02295e_end:
.org 0x22960
m68k_022960:
        move.w %d4,%d0
m68k_022960_end:
.org 0x22962
m68k_022962:
        bsr.w (. + 2102)
m68k_022962_end:
.org 0x22966
m68k_022966:
        move.w %d0,%d4
m68k_022966_end:
.org 0x22968
m68k_022968:
        move.w %d1,%d0
m68k_022968_end:
.org 0x2296A
m68k_02296a:
        andi.w #0xfffe,%sr
m68k_02296a_end:
.org 0x2296E
m68k_02296e:
        bra.w (. + 8)
m68k_02296e_end:
.org 0x22972
m68k_022972:
        ori.w #0x1,%sr
m68k_022972_end:
.org 0x22976
m68k_022976:
        rts
m68k_022976_end:
.org 0x22978
m68k_022978:
        move.w %d2,%d4
m68k_022978_end:
.org 0x2297A
m68k_02297a:
        move.w %d3,%d0
m68k_02297a_end:
.org 0x2297C
m68k_02297c:
        move.w %d0,%d1
m68k_02297c_end:
.org 0x2297E
m68k_02297e:
        move.w %d4,%d0
m68k_02297e_end:
.org 0x22980
m68k_022980:
        bsr.w (. + 2072)
m68k_022980_end:
.org 0x22984
m68k_022984:
        move.w %d0,%d4
m68k_022984_end:
.org 0x22986
m68k_022986:
        move.w %d1,%d0
m68k_022986_end:
.org 0x22988
m68k_022988:
        rts
m68k_022988_end:
.org 0x2298A
m68k_02298a:
        lea.l 0xa754:w,%a0
m68k_02298a_end:
.org 0x2298E
m68k_02298e:
        tst.b (%a0, %d7.w)
m68k_02298e_end:
.org 0x22992
m68k_022992:
        bne.w (. + 90)
m68k_022992_end:
.org 0x22996
m68k_022996:
        lea.l 0xb600:w,%a0
m68k_022996_end:
.org 0x2299A
m68k_02299a:
        move.w %d7,%d0
m68k_02299a_end:
.org 0x2299C
m68k_02299c:
        lsl.w #0x1,%d0
m68k_02299c_end:
.org 0x2299E
m68k_02299e:
        move.w (%a0, %d0.w),%d0
m68k_02299e_end:
.org 0x229A2
m68k_0229a2:
        clr.w %d2
m68k_0229a2_end:
.org 0x229A4
m68k_0229a4:
        cmpi.w #0x32,%d0
m68k_0229a4_end:
.org 0x229A8
m68k_0229a8:
        bcs.w (. + 26)
m68k_0229a8_end:
.org 0x229AC
m68k_0229ac:
        addq.w #0x1,%d2
m68k_0229ac_end:
.org 0x229AE
m68k_0229ae:
        cmpi.w #0x46,%d0
m68k_0229ae_end:
.org 0x229B2
m68k_0229b2:
        bcs.w (. + 16)
m68k_0229b2_end:
.org 0x229B6
m68k_0229b6:
        addq.w #0x1,%d2
m68k_0229b6_end:
.org 0x229B8
m68k_0229b8:
        cmpi.w #0x5a,%d0
m68k_0229b8_end:
.org 0x229BC
m68k_0229bc:
        bcs.w (. + 6)
m68k_0229bc_end:
.org 0x229C0
m68k_0229c0:
        addq.w #0x1,%d2
m68k_0229c0_end:
.org 0x229C2
m68k_0229c2:
        jsr 0x83d4:l
m68k_0229c2_end:
.org 0x229C8
m68k_0229c8:
        andi.l #0xffff,%d0
m68k_0229c8_end:
.org 0x229CE
m68k_0229ce:
        lsl.l #0x2,%d0
m68k_0229ce_end:
.org 0x229D0
m68k_0229d0:
        swap %d0
m68k_0229d0_end:
.org 0x229D2
m68k_0229d2:
        cmp.w %d2,%d0
m68k_0229d2_end:
.org 0x229D4
m68k_0229d4:
        bcc.w (. + 24)
m68k_0229d4_end:
.org 0x229D8
m68k_0229d8:
        bsr.w (. + 2810)
m68k_0229d8_end:
.org 0x229DC
m68k_0229dc:
        tst.w 0xd300:w
m68k_0229dc_end:
.org 0x229E0
m68k_0229e0:
        bmi.w (. + 12)
m68k_0229e0_end:
.org 0x229E4
m68k_0229e4:
        bsr.w (. + 13806)
m68k_0229e4_end:
.org 0x229E8
m68k_0229e8:
        bra.w (. + 8)
m68k_0229e8_end:
.org 0x229EC
m68k_0229ec:
        andi.w #0xfffe,%sr
m68k_0229ec_end:
.org 0x229F0
m68k_0229f0:
        rts
m68k_0229f0_end:
.org 0x229F2
m68k_0229f2:
        bsr.w (. + -668)
m68k_0229f2_end:
.org 0x229F6
m68k_0229f6:
        bcs.w (. + 14)
m68k_0229f6_end:
.org 0x229FA
m68k_0229fa:
        bsr.b (. + -112)
m68k_0229fa_end:
.org 0x229FC
m68k_0229fc:
        bcs.w (. + 8)
m68k_0229fc_end:
.org 0x22A00
m68k_022a00:
        bsr.w (. + 6)
m68k_022a00_end:
.org 0x22A04
m68k_022a04:
        rts
m68k_022a04_end:
.org 0x22A06
m68k_022a06:
        lea.l 0xa654:w,%a0
m68k_022a06_end:
.org 0x22A0A
m68k_022a0a:
        tst.b (%a0, %d7.w)
m68k_022a0a_end:
.org 0x22A0E
m68k_022a0e:
        bne.w (. + 160)
m68k_022a0e_end:
.org 0x22A12
m68k_022a12:
        lea.l 0xff3cc2:l,%a0
m68k_022a12_end:
.org 0x22A18
m68k_022a18:
        tst.b (%a0, %d7.w)
m68k_022a18_end:
.org 0x22A1C
m68k_022a1c:
        bne.w (. + 146)
m68k_022a1c_end:
.org 0x22A20
m68k_022a20:
        lea.l 0xff3dc2:l,%a1
m68k_022a20_end:
.org 0x22A26
m68k_022a26:
        tst.b (%a1, %d7.w)
m68k_022a26_end:
.org 0x22A2A
m68k_022a2a:
        bne.w (. + 132)
m68k_022a2a_end:
.org 0x22A2E
m68k_022a2e:
        lea.l 0xa150:w,%a0
m68k_022a2e_end:
.org 0x22A32
m68k_022a32:
        move.w %d7,%d6
m68k_022a32_end:
.org 0x22A34
m68k_022a34:
        lsl.w #0x2,%d6
m68k_022a34_end:
.org 0x22A36
m68k_022a36:
        move.w (%a0, %d6.w),%d0
m68k_022a36_end:
.org 0x22A3A
m68k_022a3a:
        move.w 0x2(%a0, %d6.w),%d1
m68k_022a3a_end:
.org 0x22A3E
m68k_022a3e:
        bsr.w (. + -428)
m68k_022a3e_end:
.org 0x22A42
m68k_022a42:
        bcs.w (. + 12)
m68k_022a42_end:
.org 0x22A46
m68k_022a46:
        bsr.w (. + 106)
m68k_022a46_end:
.org 0x22A4A
m68k_022a4a:
        bcc.w (. + 8)
m68k_022a4a_end:
.org 0x22A4E
m68k_022a4e:
        bsr.w (. + 216)
m68k_022a4e_end:
.org 0x22A52
m68k_022a52:
        lea.l 0xff2c00:l,%a0
m68k_022a52_end:
.org 0x22A58
m68k_022a58:
        move.w %d7,%d1
m68k_022a58_end:
.org 0x22A5A
m68k_022a5a:
        lsl.w #0x2,%d1
m68k_022a5a_end:
.org 0x22A5C
m68k_022a5c:
        lsr.w #0x7,%d4
m68k_022a5c_end:
.org 0x22A5E
m68k_022a5e:
        move.w %d4,(%a0, %d1.w)
m68k_022a5e_end:
.org 0x22A62
m68k_022a62:
        lsr.w #0x7,%d0
m68k_022a62_end:
.org 0x22A64
m68k_022a64:
        move.w %d0,0x2(%a0, %d1.w)
m68k_022a64_end:
.org 0x22A68
m68k_022a68:
        lea.l 0xae28:w,%a0
m68k_022a68_end:
.org 0x22A6C
m68k_022a6c:
        move.b #0x1,(%a0, %d7.w)
m68k_022a6c_end:
.org 0x22A72
m68k_022a72:
        jsr 0x1a438:l
m68k_022a72_end:
.org 0x22A78
m68k_022a78:
        lea.l 0xa150:w,%a1
m68k_022a78_end:
.org 0x22A7C
m68k_022a7c:
        move.w %d7,%d0
m68k_022a7c_end:
.org 0x22A7E
m68k_022a7e:
        lsl.w #0x2,%d0
m68k_022a7e_end:
.org 0x22A80
m68k_022a80:
        move.w (%a1, %d0.w),%d1
m68k_022a80_end:
.org 0x22A84
m68k_022a84:
        lsr.w #0x7,%d1
m68k_022a84_end:
.org 0x22A86
m68k_022a86:
        move.w 0x2(%a1, %d0.w),%d2
m68k_022a86_end:
.org 0x22A8A
m68k_022a8a:
        lsr.w #0x7,%d2
m68k_022a8a_end:
.org 0x22A8C
m68k_022a8c:
        jsr 0x1a44e:l
m68k_022a8c_end:
.org 0x22A92
m68k_022a92:
        cmpi.b #0x6,%d0
m68k_022a92_end:
.org 0x22A96
m68k_022a96:
        beq.w (. + 14)
m68k_022a96_end:
.org 0x22A9A
m68k_022a9a:
        jsr 0x1dcaa:l
m68k_022a9a_end:
.org 0x22AA0
m68k_022aa0:
        bra.w (. + 14)
m68k_022aa0_end:
.org 0x22AA4
m68k_022aa4:
        move.w %d7,0xf3a6:w
m68k_022aa4_end:
.org 0x22AA8
m68k_022aa8:
        jsr 0x1db7c:l
m68k_022aa8_end:
.org 0x22AAE
m68k_022aae:
        rts
m68k_022aae_end:
.org 0x22AB0
m68k_022ab0:
        move.w #0x5c00,%d5
m68k_022ab0_end:
.org 0x22AB4
m68k_022ab4:
        sub.w %d2,%d5
m68k_022ab4_end:
.org 0x22AB6
m68k_022ab6:
        bcs.w (. + 106)
m68k_022ab6_end:
.org 0x22ABA
m68k_022aba:
        cmpi.w #0x2000,%d5
m68k_022aba_end:
.org 0x22ABE
m68k_022abe:
        bls.w (. + 8)
m68k_022abe_end:
.org 0x22AC2
m68k_022ac2:
        move.w #0x2000,%d5
m68k_022ac2_end:
.org 0x22AC6
m68k_022ac6:
        jsr 0x83d4:l
m68k_022ac6_end:
.org 0x22ACC
m68k_022acc:
        andi.l #0xffff,%d0
m68k_022acc_end:
.org 0x22AD2
m68k_022ad2:
        mulu.w %d0,%d5
m68k_022ad2_end:
.org 0x22AD4
m68k_022ad4:
        swap %d5
m68k_022ad4_end:
.org 0x22AD6
m68k_022ad6:
        move.w %d2,%d4
m68k_022ad6_end:
.org 0x22AD8
m68k_022ad8:
        addi.w #0x800,%d4
m68k_022ad8_end:
.org 0x22ADC
m68k_022adc:
        add.w %d5,%d4
m68k_022adc_end:
.org 0x22ADE
m68k_022ade:
        jsr 0x83d4:l
m68k_022ade_end:
.org 0x22AE4
m68k_022ae4:
        andi.l #0xffff,%d0
m68k_022ae4_end:
.org 0x22AEA
m68k_022aea:
        mulu.w #0x1800,%d0
m68k_022aea_end:
.org 0x22AEE
m68k_022aee:
        swap %d0
m68k_022aee_end:
.org 0x22AF0
m68k_022af0:
        cmpi.w #0x5000,%d3
m68k_022af0_end:
.org 0x22AF4
m68k_022af4:
        bhi.w (. + 14)
m68k_022af4_end:
.org 0x22AF8
m68k_022af8:
        add.w %d3,%d0
m68k_022af8_end:
.org 0x22AFA
m68k_022afa:
        addi.w #0x1c00,%d0
m68k_022afa_end:
.org 0x22AFE
m68k_022afe:
        bra.w (. + 14)
m68k_022afe_end:
.org 0x22B02
m68k_022b02:
        move.w %d3,%d1
m68k_022b02_end:
.org 0x22B04
m68k_022b04:
        subi.w #0x1c00,%d1
m68k_022b04_end:
.org 0x22B08
m68k_022b08:
        sub.w %d0,%d1
m68k_022b08_end:
.org 0x22B0A
m68k_022b0a:
        move.w %d1,%d0
m68k_022b0a_end:
.org 0x22B0C
m68k_022b0c:
        move.w %d0,%d1
m68k_022b0c_end:
.org 0x22B0E
m68k_022b0e:
        move.w %d4,%d0
m68k_022b0e_end:
.org 0x22B10
m68k_022b10:
        bsr.w (. + 1672)
m68k_022b10_end:
.org 0x22B14
m68k_022b14:
        move.w %d0,%d4
m68k_022b14_end:
.org 0x22B16
m68k_022b16:
        move.w %d1,%d0
m68k_022b16_end:
.org 0x22B18
m68k_022b18:
        andi.w #0xfffe,%sr
m68k_022b18_end:
.org 0x22B1C
m68k_022b1c:
        bra.w (. + 8)
m68k_022b1c_end:
.org 0x22B20
m68k_022b20:
        ori.w #0x1,%sr
m68k_022b20_end:
.org 0x22B24
m68k_022b24:
        rts
m68k_022b24_end:
.org 0x22B26
m68k_022b26:
        move.w %d2,%d4
m68k_022b26_end:
.org 0x22B28
m68k_022b28:
        move.w %d3,%d0
m68k_022b28_end:
.org 0x22B2A
m68k_022b2a:
        move.w %d0,%d1
m68k_022b2a_end:
.org 0x22B2C
m68k_022b2c:
        move.w %d4,%d0
m68k_022b2c_end:
.org 0x22B2E
m68k_022b2e:
        bsr.w (. + 1642)
m68k_022b2e_end:
.org 0x22B32
m68k_022b32:
        move.w %d0,%d4
m68k_022b32_end:
.org 0x22B34
m68k_022b34:
        move.w %d1,%d0
m68k_022b34_end:
.org 0x22B36
m68k_022b36:
        rts
m68k_022b36_end:
.org 0x22B38
m68k_022b38:
        bsr.w (. + 454)
m68k_022b38_end:
.org 0x22B3C
m68k_022b3c:
        bcs.w (. + 1174)
m68k_022b3c_end:
.org 0x22B40
m68k_022b40:
        bsr.w (. + -1002)
m68k_022b40_end:
.org 0x22B44
m68k_022b44:
        bcs.w (. + 16)
m68k_022b44_end:
.org 0x22B48
m68k_022b48:
        bsr.w (. + 488)
m68k_022b48_end:
.org 0x22B4C
m68k_022b4c:
        bcs.w (. + 8)
m68k_022b4c_end:
.org 0x22B50
m68k_022b50:
        bsr.w (. + 6)
m68k_022b50_end:
.org 0x22B54
m68k_022b54:
        rts
m68k_022b54_end:
.org 0x22B56
m68k_022b56:
        lea.l 0xa654:w,%a0
m68k_022b56_end:
.org 0x22B5A
m68k_022b5a:
        tst.b (%a0, %d7.w)
m68k_022b5a_end:
.org 0x22B5E
m68k_022b5e:
        bne.w (. + 184)
m68k_022b5e_end:
.org 0x22B62
m68k_022b62:
        lea.l 0xff3cc2:l,%a0
m68k_022b62_end:
.org 0x22B68
m68k_022b68:
        tst.b (%a0, %d7.w)
m68k_022b68_end:
.org 0x22B6C
m68k_022b6c:
        bne.w (. + 170)
m68k_022b6c_end:
.org 0x22B70
m68k_022b70:
        lea.l 0xff3dc2:l,%a1
m68k_022b70_end:
.org 0x22B76
m68k_022b76:
        tst.b (%a1, %d7.w)
m68k_022b76_end:
.org 0x22B7A
m68k_022b7a:
        bne.w (. + 156)
m68k_022b7a_end:
.org 0x22B7E
m68k_022b7e:
        bsr.w (. + 154)
m68k_022b7e_end:
.org 0x22B82
m68k_022b82:
        bcc.w (. + 20)
m68k_022b82_end:
.org 0x22B86
m68k_022b86:
        move.w %d3,0xf3a6:w
m68k_022b86_end:
.org 0x22B8A
m68k_022b8a:
        bsr.w (. + 252)
m68k_022b8a_end:
.org 0x22B8E
m68k_022b8e:
        bcs.w (. + 136)
m68k_022b8e_end:
.org 0x22B92
m68k_022b92:
        bra.w (. + 40)
m68k_022b92_end:
.org 0x22B96
m68k_022b96:
        lea.l 0xa150:w,%a0
m68k_022b96_end:
.org 0x22B9A
m68k_022b9a:
        move.w %d7,%d6
m68k_022b9a_end:
.org 0x22B9C
m68k_022b9c:
        lsl.w #0x2,%d6
m68k_022b9c_end:
.org 0x22B9E
m68k_022b9e:
        move.w (%a0, %d6.w),%d0
m68k_022b9e_end:
.org 0x22BA2
m68k_022ba2:
        move.w 0x2(%a0, %d6.w),%d1
m68k_022ba2_end:
.org 0x22BA6
m68k_022ba6:
        bsr.w (. + -788)
m68k_022ba6_end:
.org 0x22BAA
m68k_022baa:
        bcs.w (. + 12)
m68k_022baa_end:
.org 0x22BAE
m68k_022bae:
        bsr.w (. + -684)
m68k_022bae_end:
.org 0x22BB2
m68k_022bb2:
        bcc.w (. + 8)
m68k_022bb2_end:
.org 0x22BB6
m68k_022bb6:
        bsr.w (. + 194)
m68k_022bb6_end:
.org 0x22BBA
m68k_022bba:
        lea.l 0xff2c00:l,%a0
m68k_022bba_end:
.org 0x22BC0
m68k_022bc0:
        move.w %d7,%d1
m68k_022bc0_end:
.org 0x22BC2
m68k_022bc2:
        lsl.w #0x2,%d1
m68k_022bc2_end:
.org 0x22BC4
m68k_022bc4:
        lsr.w #0x7,%d4
m68k_022bc4_end:
.org 0x22BC6
m68k_022bc6:
        move.w %d4,(%a0, %d1.w)
m68k_022bc6_end:
.org 0x22BCA
m68k_022bca:
        lsr.w #0x7,%d0
m68k_022bca_end:
.org 0x22BCC
m68k_022bcc:
        move.w %d0,0x2(%a0, %d1.w)
m68k_022bcc_end:
.org 0x22BD0
m68k_022bd0:
        lea.l 0xae28:w,%a0
m68k_022bd0_end:
.org 0x22BD4
m68k_022bd4:
        move.b #0x1,(%a0, %d7.w)
m68k_022bd4_end:
.org 0x22BDA
m68k_022bda:
        jsr 0x1a438:l
m68k_022bda_end:
.org 0x22BE0
m68k_022be0:
        lea.l 0xa150:w,%a1
m68k_022be0_end:
.org 0x22BE4
m68k_022be4:
        move.w %d7,%d0
m68k_022be4_end:
.org 0x22BE6
m68k_022be6:
        lsl.w #0x2,%d0
m68k_022be6_end:
.org 0x22BE8
m68k_022be8:
        move.w (%a1, %d0.w),%d1
m68k_022be8_end:
.org 0x22BEC
m68k_022bec:
        lsr.w #0x7,%d1
m68k_022bec_end:
.org 0x22BEE
m68k_022bee:
        move.w 0x2(%a1, %d0.w),%d2
m68k_022bee_end:
.org 0x22BF2
m68k_022bf2:
        lsr.w #0x7,%d2
m68k_022bf2_end:
.org 0x22BF4
m68k_022bf4:
        jsr 0x1a44e:l
m68k_022bf4_end:
.org 0x22BFA
m68k_022bfa:
        cmpi.b #0x6,%d0
m68k_022bfa_end:
.org 0x22BFE
m68k_022bfe:
        beq.w (. + 14)
m68k_022bfe_end:
.org 0x22C02
m68k_022c02:
        jsr 0x1dcaa:l
m68k_022c02_end:
.org 0x22C08
m68k_022c08:
        bra.w (. + 14)
m68k_022c08_end:
.org 0x22C0C
m68k_022c0c:
        move.w %d7,0xf3a6:w
m68k_022c0c_end:
.org 0x22C10
m68k_022c10:
        jsr 0x1db7c:l
m68k_022c10_end:
.org 0x22C16
m68k_022c16:
        rts
m68k_022c16_end:
.org 0x22C18
m68k_022c18:
        bsr.w (. + 2234)
m68k_022c18_end:
.org 0x22C1C
m68k_022c1c:
        tst.w 0xd300:w
m68k_022c1c_end:
.org 0x22C20
m68k_022c20:
        bmi.w (. + 38)
m68k_022c20_end:
.org 0x22C24
m68k_022c24:
        bsr.w (. + 40)
m68k_022c24_end:
.org 0x22C28
m68k_022c28:
        move.w %d7,%d0
m68k_022c28_end:
.org 0x22C2A
m68k_022c2a:
        jsr 0xbac8:l
m68k_022c2a_end:
.org 0x22C30
m68k_022c30:
        lsl.w #0x2,%d0
m68k_022c30_end:
.org 0x22C32
m68k_022c32:
        move.l (%a1, %d0.w),%d0
m68k_022c32_end:
.org 0x22C36
m68k_022c36:
        mulu.w %d1,%d0
m68k_022c36_end:
.org 0x22C38
m68k_022c38:
        cmp.l %d0,%d2
m68k_022c38_end:
.org 0x22C3A
m68k_022c3a:
        bhi.w (. + 12)
m68k_022c3a_end:
.org 0x22C3E
m68k_022c3e:
        ori.w #0x1,%sr
m68k_022c3e_end:
.org 0x22C42
m68k_022c42:
        bra.w (. + 8)
m68k_022c42_end:
.org 0x22C46
m68k_022c46:
        andi.w #0xfffe,%sr
m68k_022c46_end:
.org 0x22C4A
m68k_022c4a:
        rts
m68k_022c4a_end:
.org 0x22C4C
m68k_022c4c:
        lea.l 0xd300:w,%a0
m68k_022c4c_end:
.org 0x22C50
m68k_022c50:
        lea.l 0xc800:w,%a1
m68k_022c50_end:
.org 0x22C54
m68k_022c54:
        moveq #-1,%d2
m68k_022c54_end:
.org 0x22C56
m68k_022c56:
        move.w (%a0)+,%d0
m68k_022c56_end:
.org 0x22C58
m68k_022c58:
        bmi.w (. + 30)
m68k_022c58_end:
.org 0x22C5C
m68k_022c5c:
        jsr 0xbac8:l
m68k_022c5c_end:
.org 0x22C62
m68k_022c62:
        lsl.w #0x2,%d0
m68k_022c62_end:
.org 0x22C64
m68k_022c64:
        move.l (%a1, %d0.w),%d4
m68k_022c64_end:
.org 0x22C68
m68k_022c68:
        mulu.w %d1,%d4
m68k_022c68_end:
.org 0x22C6A
m68k_022c6a:
        cmp.l %d2,%d4
m68k_022c6a_end:
.org 0x22C6C
m68k_022c6c:
        bcc.b (. + -22)
m68k_022c6c_end:
.org 0x22C6E
m68k_022c6e:
        move.l %d4,%d2
m68k_022c6e_end:
.org 0x22C70
m68k_022c70:
        lsr.w #0x2,%d0
m68k_022c70_end:
.org 0x22C72
m68k_022c72:
        move.w %d0,%d3
m68k_022c72_end:
.org 0x22C74
m68k_022c74:
        bra.b (. + -30)
m68k_022c74_end:
.org 0x22C76
m68k_022c76:
        rts
m68k_022c76_end:
.org 0x22C78
m68k_022c78:
        move.w %d2,%d0
m68k_022c78_end:
.org 0x22C7A
m68k_022c7a:
        move.w %d3,%d1
m68k_022c7a_end:
.org 0x22C7C
m68k_022c7c:
        bsr.w (. + 1308)
m68k_022c7c_end:
.org 0x22C80
m68k_022c80:
        move.w %d0,%d4
m68k_022c80_end:
.org 0x22C82
m68k_022c82:
        move.w %d1,%d0
m68k_022c82_end:
.org 0x22C84
m68k_022c84:
        rts
m68k_022c84_end:
.org 0x22C86
m68k_022c86:
        bsr.w (. + 50)
m68k_022c86_end:
.org 0x22C8A
m68k_022c8a:
        bcs.w (. + 44)
m68k_022c8a_end:
.org 0x22C8E
m68k_022c8e:
        lea.l 0xff2c00:l,%a1
m68k_022c8e_end:
.org 0x22C94
m68k_022c94:
        move.w %d7,%d0
m68k_022c94_end:
.org 0x22C96
m68k_022c96:
        lsl.w #0x2,%d0
m68k_022c96_end:
.org 0x22C98
m68k_022c98:
        lea.l 0xa150:w,%a0
m68k_022c98_end:
.org 0x22C9C
m68k_022c9c:
        move.w 0xf3a6:w,%d3
m68k_022c9c_end:
.org 0x22CA0
m68k_022ca0:
        lsl.w #0x2,%d3
m68k_022ca0_end:
.org 0x22CA2
m68k_022ca2:
        move.w (%a0, %d3.w),%d0
m68k_022ca2_end:
.org 0x22CA6
m68k_022ca6:
        move.w 0x2(%a0, %d3.w),%d1
m68k_022ca6_end:
.org 0x22CAA
m68k_022caa:
        bsr.w (. + 1262)
m68k_022caa_end:
.org 0x22CAE
m68k_022cae:
        move.w %d0,%d4
m68k_022cae_end:
.org 0x22CB0
m68k_022cb0:
        move.w %d1,%d0
m68k_022cb0_end:
.org 0x22CB2
m68k_022cb2:
        andi.w #0xfffe,%sr
m68k_022cb2_end:
.org 0x22CB6
m68k_022cb6:
        rts
m68k_022cb6_end:
.org 0x22CB8
m68k_022cb8:
        lea.l 0xb600:w,%a0
m68k_022cb8_end:
.org 0x22CBC
m68k_022cbc:
        move.w %d7,%d0
m68k_022cbc_end:
.org 0x22CBE
m68k_022cbe:
        lsl.w #0x1,%d0
m68k_022cbe_end:
.org 0x22CC0
m68k_022cc0:
        move.w (%a0, %d0.w),%d0
m68k_022cc0_end:
.org 0x22CC4
m68k_022cc4:
        clr.w %d2
m68k_022cc4_end:
.org 0x22CC6
m68k_022cc6:
        cmpi.w #0x46,%d0
m68k_022cc6_end:
.org 0x22CCA
m68k_022cca:
        bcs.w (. + 16)
m68k_022cca_end:
.org 0x22CCE
m68k_022cce:
        addq.w #0x1,%d2
m68k_022cce_end:
.org 0x22CD0
m68k_022cd0:
        cmpi.w #0x5a,%d0
m68k_022cd0_end:
.org 0x22CD4
m68k_022cd4:
        bcs.w (. + 6)
m68k_022cd4_end:
.org 0x22CD8
m68k_022cd8:
        addq.w #0x1,%d2
m68k_022cd8_end:
.org 0x22CDA
m68k_022cda:
        jsr 0x83d4:l
m68k_022cda_end:
.org 0x22CE0
m68k_022ce0:
        andi.l #0xffff,%d0
m68k_022ce0_end:
.org 0x22CE6
m68k_022ce6:
        lsl.l #0x2,%d0
m68k_022ce6_end:
.org 0x22CE8
m68k_022ce8:
        swap %d0
m68k_022ce8_end:
.org 0x22CEA
m68k_022cea:
        cmp.w %d2,%d0
m68k_022cea_end:
.org 0x22CEC
m68k_022cec:
        bcc.w (. + 12)
m68k_022cec_end:
.org 0x22CF0
m68k_022cf0:
        bsr.w (. + 13026)
m68k_022cf0_end:
.org 0x22CF4
m68k_022cf4:
        bra.w (. + 8)
m68k_022cf4_end:
.org 0x22CF8
m68k_022cf8:
        andi.w #0xfffe,%sr
m68k_022cf8_end:
.org 0x22CFC
m68k_022cfc:
        rts
m68k_022cfc_end:
.org 0x22CFE
m68k_022cfe:
        lea.l 0xf69e:w,%a0
m68k_022cfe_end:
.org 0x22D02
m68k_022d02:
        lea.l 0xf6a2:w,%a1
m68k_022d02_end:
.org 0x22D06
m68k_022d06:
        btst.b #0x1,0xf6d7:w
m68k_022d06_end:
.org 0x22D0C
m68k_022d0c:
        beq.w (. + 6)
m68k_022d0c_end:
.org 0x22D10
m68k_022d10:
        exg %a0,%a1
m68k_022d10_end:
.org 0x22D12
m68k_022d12:
        move.l (%a1),%d0
m68k_022d12_end:
.org 0x22D14
m68k_022d14:
        cmp.l (%a0),%d0
m68k_022d14_end:
.org 0x22D16
m68k_022d16:
        bcc.w (. + 20)
m68k_022d16_end:
.org 0x22D1A
m68k_022d1a:
        cmp.l 0xf76c:w,%d0
m68k_022d1a_end:
.org 0x22D1E
m68k_022d1e:
        bcc.w (. + 12)
m68k_022d1e_end:
.org 0x22D22
m68k_022d22:
        ori.w #0x1,%sr
m68k_022d22_end:
.org 0x22D26
m68k_022d26:
        bra.w (. + 8)
m68k_022d26_end:
.org 0x22D2A
m68k_022d2a:
        andi.w #0xfffe,%sr
m68k_022d2a_end:
.org 0x22D2E
m68k_022d2e:
        rts
m68k_022d2e_end:
.org 0x22D30
m68k_022d30:
        bsr.w (. + 118)
m68k_022d30_end:
.org 0x22D34
m68k_022d34:
        bcc.w (. + 98)
m68k_022d34_end:
.org 0x22D38
m68k_022d38:
        lea.l 0xc800:w,%a0
m68k_022d38_end:
.org 0x22D3C
m68k_022d3c:
        move.w %d7,%d0
m68k_022d3c_end:
.org 0x22D3E
m68k_022d3e:
        lsl.w #0x2,%d0
m68k_022d3e_end:
.org 0x22D40
m68k_022d40:
        cmpi.l #0x1388,(%a0, %d0.w)
m68k_022d40_end:
.org 0x22D48
m68k_022d48:
        bhi.w (. + 78)
m68k_022d48_end:
.org 0x22D4C
m68k_022d4c:
        bsr.w (. + 152)
m68k_022d4c_end:
.org 0x22D50
m68k_022d50:
        cmpi.w #0x4,%d0
m68k_022d50_end:
.org 0x22D54
m68k_022d54:
        bcs.w (. + 66)
m68k_022d54_end:
.org 0x22D58
m68k_022d58:
        bsr.w (. + 1914)
m68k_022d58_end:
.org 0x22D5C
m68k_022d5c:
        tst.w 0xd300:w
m68k_022d5c_end:
.org 0x22D60
m68k_022d60:
        bmi.w (. + 54)
m68k_022d60_end:
.org 0x22D64
m68k_022d64:
        lea.l 0xff3bc2:l,%a0
m68k_022d64_end:
.org 0x22D6A
m68k_022d6a:
        tst.b (%a0, %d7.w)
m68k_022d6a_end:
.org 0x22D6E
m68k_022d6e:
        bne.w (. + 18)
m68k_022d6e_end:
.org 0x22D72
m68k_022d72:
        jsr 0x83d4:l
m68k_022d72_end:
.org 0x22D78
m68k_022d78:
        btst.l #0xf,%d0
m68k_022d78_end:
.org 0x22D7C
m68k_022d7c:
        bne.w (. + 26)
m68k_022d7c_end:
.org 0x22D80
m68k_022d80:
        move.b #0x1,(%a0, %d7.w)
m68k_022d80_end:
.org 0x22D86
m68k_022d86:
        lea.l 0xae28:w,%a0
m68k_022d86_end:
.org 0x22D8A
m68k_022d8a:
        clr.b (%a0, %d7.w)
m68k_022d8a_end:
.org 0x22D8E
m68k_022d8e:
        ori.w #0x1,%sr
m68k_022d8e_end:
.org 0x22D92
m68k_022d92:
        bra.w (. + 18)
m68k_022d92_end:
.org 0x22D96
m68k_022d96:
        lea.l 0xff3bc2:l,%a0
m68k_022d96_end:
.org 0x22D9C
m68k_022d9c:
        clr.b (%a0, %d7.w)
m68k_022d9c_end:
.org 0x22DA0
m68k_022da0:
        andi.w #0xfffe,%sr
m68k_022da0_end:
.org 0x22DA4
m68k_022da4:
        rts
m68k_022da4_end:
.org 0x22DA6
m68k_022da6:
        jsr 0x1a438:l
m68k_022da6_end:
.org 0x22DAC
m68k_022dac:
        lea.l 0xa150:w,%a1
m68k_022dac_end:
.org 0x22DB0
m68k_022db0:
        move.w %d7,%d0
m68k_022db0_end:
.org 0x22DB2
m68k_022db2:
        lsl.w #0x2,%d0
m68k_022db2_end:
.org 0x22DB4
m68k_022db4:
        move.w (%a1, %d0.w),%d1
m68k_022db4_end:
.org 0x22DB8
m68k_022db8:
        lsr.w #0x7,%d1
m68k_022db8_end:
.org 0x22DBA
m68k_022dba:
        move.w 0x2(%a1, %d0.w),%d2
m68k_022dba_end:
.org 0x22DBE
m68k_022dbe:
        lsr.w #0x7,%d2
m68k_022dbe_end:
.org 0x22DC0
m68k_022dc0:
        jsr 0x1a44e:l
m68k_022dc0_end:
.org 0x22DC6
m68k_022dc6:
        cmpi.b #0x3,%d0
m68k_022dc6_end:
.org 0x22DCA
m68k_022dca:
        beq.w (. + 20)
m68k_022dca_end:
.org 0x22DCE
m68k_022dce:
        cmpi.b #0x7,%d0
m68k_022dce_end:
.org 0x22DD2
m68k_022dd2:
        beq.w (. + 12)
m68k_022dd2_end:
.org 0x22DD6
m68k_022dd6:
        andi.w #0xfffe,%sr
m68k_022dd6_end:
.org 0x22DDA
m68k_022dda:
        bra.w (. + 8)
m68k_022dda_end:
.org 0x22DDE
m68k_022dde:
        ori.w #0x1,%sr
m68k_022dde_end:
.org 0x22DE2
m68k_022de2:
        rts
m68k_022de2_end:
.org 0x22DE4
m68k_022de4:
        lea.l 0xa5a4:w,%a0
m68k_022de4_end:
.org 0x22DE8
m68k_022de8:
        btst.b #0x1,0xf6d7:w
m68k_022de8_end:
.org 0x22DEE
m68k_022dee:
        bne.w (. + 8)
m68k_022dee_end:
.org 0x22DF2
m68k_022df2:
        lea.l 0xa550:w,%a0
m68k_022df2_end:
.org 0x22DF6
m68k_022df6:
        clr.w %d0
m68k_022df6_end:
.org 0x22DF8
m68k_022df8:
        tst.b (%a0)+
m68k_022df8_end:
.org 0x22DFA
m68k_022dfa:
        bmi.w (. + 8)
m68k_022dfa_end:
.org 0x22DFE
m68k_022dfe:
        addq.w #0x1,%d0
m68k_022dfe_end:
.org 0x22E00
m68k_022e00:
        bra.b (. + -8)
m68k_022e00_end:
.org 0x22E02
m68k_022e02:
        rts
m68k_022e02_end:
.org 0x22E04
m68k_022e04:
        bsr.w (. + -262)
m68k_022e04_end:
.org 0x22E08
m68k_022e08:
        bcs.w (. + 458)
m68k_022e08_end:
.org 0x22E0C
m68k_022e0c:
        bsr.w (. + -1718)
m68k_022e0c_end:
.org 0x22E10
m68k_022e10:
        bcs.w (. + 16)
m68k_022e10_end:
.org 0x22E14
m68k_022e14:
        bsr.w (. + -228)
m68k_022e14_end:
.org 0x22E18
m68k_022e18:
        bcs.w (. + 8)
m68k_022e18_end:
.org 0x22E1C
m68k_022e1c:
        bsr.w (. + 6)
m68k_022e1c_end:
.org 0x22E20
m68k_022e20:
        rts
m68k_022e20_end:
.org 0x22E22
m68k_022e22:
        lea.l 0xa654:w,%a0
m68k_022e22_end:
.org 0x22E26
m68k_022e26:
        tst.b (%a0, %d7.w)
m68k_022e26_end:
.org 0x22E2A
m68k_022e2a:
        bne.w (. + 180)
m68k_022e2a_end:
.org 0x22E2E
m68k_022e2e:
        lea.l 0xff3cc2:l,%a0
m68k_022e2e_end:
.org 0x22E34
m68k_022e34:
        tst.b (%a0, %d7.w)
m68k_022e34_end:
.org 0x22E38
m68k_022e38:
        bne.w (. + 166)
m68k_022e38_end:
.org 0x22E3C
m68k_022e3c:
        lea.l 0xff3dc2:l,%a1
m68k_022e3c_end:
.org 0x22E42
m68k_022e42:
        tst.b (%a1, %d7.w)
m68k_022e42_end:
.org 0x22E46
m68k_022e46:
        bne.w (. + -560)
m68k_022e46_end:
.org 0x22E4A
m68k_022e4a:
        bsr.w (. + -562)
m68k_022e4a_end:
.org 0x22E4E
m68k_022e4e:
        bcc.w (. + 16)
m68k_022e4e_end:
.org 0x22E52
m68k_022e52:
        bsr.w (. + -460)
m68k_022e52_end:
.org 0x22E56
m68k_022e56:
        bcs.w (. + 136)
m68k_022e56_end:
.org 0x22E5A
m68k_022e5a:
        bra.w (. + 40)
m68k_022e5a_end:
.org 0x22E5E
m68k_022e5e:
        lea.l 0xa150:w,%a0
m68k_022e5e_end:
.org 0x22E62
m68k_022e62:
        move.w %d7,%d6
m68k_022e62_end:
.org 0x22E64
m68k_022e64:
        lsl.w #0x2,%d6
m68k_022e64_end:
.org 0x22E66
m68k_022e66:
        move.w (%a0, %d6.w),%d0
m68k_022e66_end:
.org 0x22E6A
m68k_022e6a:
        move.w 0x2(%a0, %d6.w),%d1
m68k_022e6a_end:
.org 0x22E6E
m68k_022e6e:
        bsr.w (. + -1500)
m68k_022e6e_end:
.org 0x22E72
m68k_022e72:
        bcs.w (. + 12)
m68k_022e72_end:
.org 0x22E76
m68k_022e76:
        bsr.w (. + -966)
m68k_022e76_end:
.org 0x22E7A
m68k_022e7a:
        bcc.w (. + 8)
m68k_022e7a_end:
.org 0x22E7E
m68k_022e7e:
        bsr.w (. + 98)
m68k_022e7e_end:
.org 0x22E82
m68k_022e82:
        lea.l 0xff2c00:l,%a0
m68k_022e82_end:
.org 0x22E88
m68k_022e88:
        move.w %d7,%d1
m68k_022e88_end:
.org 0x22E8A
m68k_022e8a:
        lsl.w #0x2,%d1
m68k_022e8a_end:
.org 0x22E8C
m68k_022e8c:
        lsr.w #0x7,%d4
m68k_022e8c_end:
.org 0x22E8E
m68k_022e8e:
        move.w %d4,(%a0, %d1.w)
m68k_022e8e_end:
.org 0x22E92
m68k_022e92:
        lsr.w #0x7,%d0
m68k_022e92_end:
.org 0x22E94
m68k_022e94:
        move.w %d0,0x2(%a0, %d1.w)
m68k_022e94_end:
.org 0x22E98
m68k_022e98:
        lea.l 0xae28:w,%a0
m68k_022e98_end:
.org 0x22E9C
m68k_022e9c:
        move.b #0x1,(%a0, %d7.w)
m68k_022e9c_end:
.org 0x22EA2
m68k_022ea2:
        jsr 0x1a438:l
m68k_022ea2_end:
.org 0x22EA8
m68k_022ea8:
        lea.l 0xa150:w,%a1
m68k_022ea8_end:
.org 0x22EAC
m68k_022eac:
        move.w %d7,%d0
m68k_022eac_end:
.org 0x22EAE
m68k_022eae:
        lsl.w #0x2,%d0
m68k_022eae_end:
.org 0x22EB0
m68k_022eb0:
        move.w (%a1, %d0.w),%d1
m68k_022eb0_end:
.org 0x22EB4
m68k_022eb4:
        lsr.w #0x7,%d1
m68k_022eb4_end:
.org 0x22EB6
m68k_022eb6:
        move.w 0x2(%a1, %d0.w),%d2
m68k_022eb6_end:
.org 0x22EBA
m68k_022eba:
        lsr.w #0x7,%d2
m68k_022eba_end:
.org 0x22EBC
m68k_022ebc:
        jsr 0x1a44e:l
m68k_022ebc_end:
.org 0x22EC2
m68k_022ec2:
        cmpi.b #0x6,%d0
m68k_022ec2_end:
.org 0x22EC6
m68k_022ec6:
        beq.w (. + 14)
m68k_022ec6_end:
.org 0x22ECA
m68k_022eca:
        jsr 0x1dcaa:l
m68k_022eca_end:
.org 0x22ED0
m68k_022ed0:
        bra.w (. + 14)
m68k_022ed0_end:
.org 0x22ED4
m68k_022ed4:
        move.w %d7,0xf3a6:w
m68k_022ed4_end:
.org 0x22ED8
m68k_022ed8:
        jsr 0x1db7c:l
m68k_022ed8_end:
.org 0x22EDE
m68k_022ede:
        rts
m68k_022ede_end:
.org 0x22EE0
m68k_022ee0:
        move.w %d2,%d0
m68k_022ee0_end:
.org 0x22EE2
m68k_022ee2:
        move.w %d3,%d1
m68k_022ee2_end:
.org 0x22EE4
m68k_022ee4:
        bsr.w (. + 692)
m68k_022ee4_end:
.org 0x22EE8
m68k_022ee8:
        move.w %d0,%d4
m68k_022ee8_end:
.org 0x22EEA
m68k_022eea:
        move.w %d1,%d0
m68k_022eea_end:
.org 0x22EEC
m68k_022eec:
        rts
m68k_022eec_end:
.org 0x22EEE
m68k_022eee:
        bsr.w (. + -496)
m68k_022eee_end:
.org 0x22EF2
m68k_022ef2:
        bcs.w (. + 224)
m68k_022ef2_end:
.org 0x22EF6
m68k_022ef6:
        bsr.w (. + -1952)
m68k_022ef6_end:
.org 0x22EFA
m68k_022efa:
        bcs.w (. + 16)
m68k_022efa_end:
.org 0x22EFE
m68k_022efe:
        bsr.w (. + -462)
m68k_022efe_end:
.org 0x22F02
m68k_022f02:
        bcs.w (. + 8)
m68k_022f02_end:
.org 0x22F06
m68k_022f06:
        bsr.w (. + 6)
m68k_022f06_end:
.org 0x22F0A
m68k_022f0a:
        rts
m68k_022f0a_end:
.org 0x22F0C
m68k_022f0c:
        lea.l 0xa654:w,%a0
m68k_022f0c_end:
.org 0x22F10
m68k_022f10:
        tst.b (%a0, %d7.w)
m68k_022f10_end:
.org 0x22F14
m68k_022f14:
        bne.w (. + 180)
m68k_022f14_end:
.org 0x22F18
m68k_022f18:
        lea.l 0xff3cc2:l,%a0
m68k_022f18_end:
.org 0x22F1E
m68k_022f1e:
        tst.b (%a0, %d7.w)
m68k_022f1e_end:
.org 0x22F22
m68k_022f22:
        bne.w (. + 166)
m68k_022f22_end:
.org 0x22F26
m68k_022f26:
        lea.l 0xff3dc2:l,%a1
m68k_022f26_end:
.org 0x22F2C
m68k_022f2c:
        tst.b (%a1, %d7.w)
m68k_022f2c_end:
.org 0x22F30
m68k_022f30:
        bne.w (. + -794)
m68k_022f30_end:
.org 0x22F34
m68k_022f34:
        bsr.w (. + -796)
m68k_022f34_end:
.org 0x22F38
m68k_022f38:
        bcc.w (. + 16)
m68k_022f38_end:
.org 0x22F3C
m68k_022f3c:
        bsr.w (. + -694)
m68k_022f3c_end:
.org 0x22F40
m68k_022f40:
        bcs.w (. + 136)
m68k_022f40_end:
.org 0x22F44
m68k_022f44:
        bra.w (. + 40)
m68k_022f44_end:
.org 0x22F48
m68k_022f48:
        lea.l 0xa150:w,%a0
m68k_022f48_end:
.org 0x22F4C
m68k_022f4c:
        move.w %d7,%d6
m68k_022f4c_end:
.org 0x22F4E
m68k_022f4e:
        lsl.w #0x2,%d6
m68k_022f4e_end:
.org 0x22F50
m68k_022f50:
        move.w (%a0, %d6.w),%d0
m68k_022f50_end:
.org 0x22F54
m68k_022f54:
        move.w 0x2(%a0, %d6.w),%d1
m68k_022f54_end:
.org 0x22F58
m68k_022f58:
        bsr.w (. + -1734)
m68k_022f58_end:
.org 0x22F5C
m68k_022f5c:
        bcs.w (. + 12)
m68k_022f5c_end:
.org 0x22F60
m68k_022f60:
        bsr.w (. + -1200)
m68k_022f60_end:
.org 0x22F64
m68k_022f64:
        bcc.w (. + 8)
m68k_022f64_end:
.org 0x22F68
m68k_022f68:
        bsr.w (. + -1090)
m68k_022f68_end:
.org 0x22F6C
m68k_022f6c:
        lea.l 0xff2c00:l,%a0
m68k_022f6c_end:
.org 0x22F72
m68k_022f72:
        move.w %d7,%d1
m68k_022f72_end:
.org 0x22F74
m68k_022f74:
        lsl.w #0x2,%d1
m68k_022f74_end:
.org 0x22F76
m68k_022f76:
        lsr.w #0x7,%d4
m68k_022f76_end:
.org 0x22F78
m68k_022f78:
        move.w %d4,(%a0, %d1.w)
m68k_022f78_end:
.org 0x22F7C
m68k_022f7c:
        lsr.w #0x7,%d0
m68k_022f7c_end:
.org 0x22F7E
m68k_022f7e:
        move.w %d0,0x2(%a0, %d1.w)
m68k_022f7e_end:
.org 0x22F82
m68k_022f82:
        lea.l 0xae28:w,%a0
m68k_022f82_end:
.org 0x22F86
m68k_022f86:
        move.b #0x1,(%a0, %d7.w)
m68k_022f86_end:
.org 0x22F8C
m68k_022f8c:
        jsr 0x1a438:l
m68k_022f8c_end:
.org 0x22F92
m68k_022f92:
        lea.l 0xa150:w,%a1
m68k_022f92_end:
.org 0x22F96
m68k_022f96:
        move.w %d7,%d0
m68k_022f96_end:
.org 0x22F98
m68k_022f98:
        lsl.w #0x2,%d0
m68k_022f98_end:
.org 0x22F9A
m68k_022f9a:
        move.w (%a1, %d0.w),%d1
m68k_022f9a_end:
.org 0x22F9E
m68k_022f9e:
        lsr.w #0x7,%d1
m68k_022f9e_end:
.org 0x22FA0
m68k_022fa0:
        move.w 0x2(%a1, %d0.w),%d2
m68k_022fa0_end:
.org 0x22FA4
m68k_022fa4:
        lsr.w #0x7,%d2
m68k_022fa4_end:
.org 0x22FA6
m68k_022fa6:
        jsr 0x1a44e:l
m68k_022fa6_end:
.org 0x22FAC
m68k_022fac:
        cmpi.b #0x6,%d0
m68k_022fac_end:
.org 0x22FB0
m68k_022fb0:
        beq.w (. + 14)
m68k_022fb0_end:
.org 0x22FB4
m68k_022fb4:
        jsr 0x1dcaa:l
m68k_022fb4_end:
.org 0x22FBA
m68k_022fba:
        bra.w (. + 14)
m68k_022fba_end:
.org 0x22FBE
m68k_022fbe:
        move.w %d7,0xf3a6:w
m68k_022fbe_end:
.org 0x22FC2
m68k_022fc2:
        jsr 0x1db7c:l
m68k_022fc2_end:
.org 0x22FC8
m68k_022fc8:
        rts
m68k_022fc8_end:
.org 0x22FCA
m68k_022fca:
        bsr.w (. + 124)
m68k_022fca_end:
.org 0x22FCE
m68k_022fce:
        bcs.w (. + -450)
m68k_022fce_end:
.org 0x22FD2
m68k_022fd2:
        bsr.w (. + -2172)
m68k_022fd2_end:
.org 0x22FD6
m68k_022fd6:
        bcs.w (. + 16)
m68k_022fd6_end:
.org 0x22FDA
m68k_022fda:
        bsr.w (. + 14)
m68k_022fda_end:
.org 0x22FDE
m68k_022fde:
        bcs.w (. + 8)
m68k_022fde_end:
.org 0x22FE2
m68k_022fe2:
        bsr.w (. + -2798)
m68k_022fe2_end:
.org 0x22FE6
m68k_022fe6:
        rts
m68k_022fe6_end:
.org 0x22FE8
m68k_022fe8:
        bsr.w (. + 1258)
m68k_022fe8_end:
.org 0x22FEC
m68k_022fec:
        tst.w 0xd300:w
m68k_022fec_end:
.org 0x22FF0
m68k_022ff0:
        bmi.w (. + 80)
m68k_022ff0_end:
.org 0x22FF4
m68k_022ff4:
        lea.l 0xb600:w,%a0
m68k_022ff4_end:
.org 0x22FF8
m68k_022ff8:
        move.w %d7,%d0
m68k_022ff8_end:
.org 0x22FFA
m68k_022ffa:
        lsl.w #0x1,%d0
m68k_022ffa_end:
.org 0x22FFC
m68k_022ffc:
        move.w (%a0, %d0.w),%d0
m68k_022ffc_end:
.org 0x23000
m68k_023000:
        move.w #0x1,%d2
m68k_023000_end:
.org 0x23004
m68k_023004:
        cmpi.w #0x3c,%d0
m68k_023004_end:
.org 0x23008
m68k_023008:
        bcs.w (. + 26)
m68k_023008_end:
.org 0x2300C
m68k_02300c:
        addq.w #0x1,%d2
m68k_02300c_end:
.org 0x2300E
m68k_02300e:
        cmpi.w #0x50,%d0
m68k_02300e_end:
.org 0x23012
m68k_023012:
        bcs.w (. + 16)
m68k_023012_end:
.org 0x23016
m68k_023016:
        addq.w #0x1,%d2
m68k_023016_end:
.org 0x23018
m68k_023018:
        cmpi.w #0x64,%d0
m68k_023018_end:
.org 0x2301C
m68k_02301c:
        bcs.w (. + 6)
m68k_02301c_end:
.org 0x23020
m68k_023020:
        addq.w #0x1,%d2
m68k_023020_end:
.org 0x23022
m68k_023022:
        jsr 0x83d4:l
m68k_023022_end:
.org 0x23028
m68k_023028:
        andi.l #0xffff,%d0
m68k_023028_end:
.org 0x2302E
m68k_02302e:
        lsl.l #0x2,%d0
m68k_02302e_end:
.org 0x23030
m68k_023030:
        swap %d0
m68k_023030_end:
.org 0x23032
m68k_023032:
        cmp.w %d2,%d0
m68k_023032_end:
.org 0x23034
m68k_023034:
        bhi.w (. + 12)
m68k_023034_end:
.org 0x23038
m68k_023038:
        bsr.w (. + 12186)
m68k_023038_end:
.org 0x2303C
m68k_02303c:
        bra.w (. + 8)
m68k_02303c_end:
.org 0x23040
m68k_023040:
        andi.w #0xfffe,%sr
m68k_023040_end:
.org 0x23044
m68k_023044:
        rts
m68k_023044_end:
.org 0x23046
m68k_023046:
        btst.b #0x1,0xf6d7:w
m68k_023046_end:
.org 0x2304C
m68k_02304c:
        bne.w (. + 12)
m68k_02304c_end:
.org 0x23050
m68k_023050:
        lea.l 0xa5a4:w,%a0
m68k_023050_end:
.org 0x23054
m68k_023054:
        bra.w (. + 8)
m68k_023054_end:
.org 0x23058
m68k_023058:
        lea.l 0xa550:w,%a0
m68k_023058_end:
.org 0x2305C
m68k_02305c:
        tst.w 0x2(%a0)
m68k_02305c_end:
.org 0x23060
m68k_023060:
        bpl.w (. + 12)
m68k_023060_end:
.org 0x23064
m68k_023064:
        ori.w #0x1,%sr
m68k_023064_end:
.org 0x23068
m68k_023068:
        bra.w (. + 8)
m68k_023068_end:
.org 0x2306C
m68k_02306c:
        andi.w #0xfffe,%sr
m68k_02306c_end:
.org 0x23070
m68k_023070:
        rts
m68k_023070_end:
.org 0x23072
m68k_023072:
        bsr.b (. + -44)
m68k_023072_end:
.org 0x23074
m68k_023074:
        bcs.w (. + -382)
m68k_023074_end:
.org 0x23078
m68k_023078:
        bsr.w (. + -2338)
m68k_023078_end:
.org 0x2307C
m68k_02307c:
        bcs.w (. + 16)
m68k_02307c_end:
.org 0x23080
m68k_023080:
        bsr.w (. + -152)
m68k_023080_end:
.org 0x23084
m68k_023084:
        bcs.w (. + 8)
m68k_023084_end:
.org 0x23088
m68k_023088:
        bsr.w (. + -2964)
m68k_023088_end:
.org 0x2308C
m68k_02308c:
        rts
m68k_02308c_end:
.org 0x2308E
m68k_02308e:
        bsr.b (. + -72)
m68k_02308e_end:
.org 0x23090
m68k_023090:
        bcs.w (. + -1360)
m68k_023090_end:
.org 0x23094
m68k_023094:
        bsr.w (. + -2366)
m68k_023094_end:
.org 0x23098
m68k_023098:
        bcs.w (. + 16)
m68k_023098_end:
.org 0x2309C
m68k_02309c:
        bsr.w (. + -180)
m68k_02309c_end:
.org 0x230A0
m68k_0230a0:
        bcs.w (. + 8)
m68k_0230a0_end:
.org 0x230A4
m68k_0230a4:
        bsr.w (. + -2992)
m68k_0230a4_end:
.org 0x230A8
m68k_0230a8:
        rts
m68k_0230a8_end:
.org 0x230AA
m68k_0230aa:
        bsr.b (. + -100)
m68k_0230aa_end:
.org 0x230AC
m68k_0230ac:
        bcs.w (. + -1388)
m68k_0230ac_end:
.org 0x230B0
m68k_0230b0:
        bsr.w (. + -946)
m68k_0230b0_end:
.org 0x230B4
m68k_0230b4:
        bcs.w (. + -226)
m68k_0230b4_end:
.org 0x230B8
m68k_0230b8:
        bsr.w (. + 810)
m68k_0230b8_end:
.org 0x230BC
m68k_0230bc:
        bcs.w (. + -1404)
m68k_0230bc_end:
.org 0x230C0
m68k_0230c0:
        bsr.w (. + -2410)
m68k_0230c0_end:
.org 0x230C4
m68k_0230c4:
        bcs.w (. + 24)
m68k_0230c4_end:
.org 0x230C8
m68k_0230c8:
        bsr.w (. + -920)
m68k_0230c8_end:
.org 0x230CC
m68k_0230cc:
        bcs.w (. + 16)
m68k_0230cc_end:
.org 0x230D0
m68k_0230d0:
        bsr.w (. + -1862)
m68k_0230d0_end:
.org 0x230D4
m68k_0230d4:
        bcs.w (. + 8)
m68k_0230d4_end:
.org 0x230D8
m68k_0230d8:
        bsr.w (. + 6)
m68k_0230d8_end:
.org 0x230DC
m68k_0230dc:
        rts
m68k_0230dc_end:
.org 0x230DE
m68k_0230de:
        move.w 0xff3ec2:l,%d0
m68k_0230de_end:
.org 0x230E4
m68k_0230e4:
        lea.l 0xa654:w,%a0
m68k_0230e4_end:
.org 0x230E8
m68k_0230e8:
        tst.b (%a0, %d7.w)
m68k_0230e8_end:
.org 0x230EC
m68k_0230ec:
        bne.w (. + 170)
m68k_0230ec_end:
.org 0x230F0
m68k_0230f0:
        lea.l 0xff3cc2:l,%a0
m68k_0230f0_end:
.org 0x230F6
m68k_0230f6:
        tst.b (%a0, %d7.w)
m68k_0230f6_end:
.org 0x230FA
m68k_0230fa:
        bne.w (. + 156)
m68k_0230fa_end:
.org 0x230FE
m68k_0230fe:
        lea.l 0xff3dc2:l,%a1
m68k_0230fe_end:
.org 0x23104
m68k_023104:
        tst.b (%a1, %d7.w)
m68k_023104_end:
.org 0x23108
m68k_023108:
        bne.w (. + 142)
m68k_023108_end:
.org 0x2310C
m68k_02310c:
        bsr.w (. + 388)
m68k_02310c_end:
.org 0x23110
m68k_023110:
        bcs.w (. + 134)
m68k_023110_end:
.org 0x23114
m68k_023114:
        clr.w %d1
m68k_023114_end:
.org 0x23116
m68k_023116:
        move.b %d0,%d1
m68k_023116_end:
.org 0x23118
m68k_023118:
        lsl.w #0x2,%d0
m68k_023118_end:
.org 0x2311A
m68k_02311a:
        andi.w #0xfc00,%d0
m68k_02311a_end:
.org 0x2311E
m68k_02311e:
        lsl.w #0x3,%d1
m68k_02311e_end:
.org 0x23120
m68k_023120:
        lsl.w #0x7,%d1
m68k_023120_end:
.org 0x23122
m68k_023122:
        lea.l 0xa150:w,%a0
m68k_023122_end:
.org 0x23126
m68k_023126:
        move.w %d7,%d2
m68k_023126_end:
.org 0x23128
m68k_023128:
        lsl.w #0x2,%d2
m68k_023128_end:
.org 0x2312A
m68k_02312a:
        cmp.w (%a0, %d2.w),%d0
m68k_02312a_end:
.org 0x2312E
m68k_02312e:
        bne.w (. + 12)
m68k_02312e_end:
.org 0x23132
m68k_023132:
        cmp.w 0x2(%a0, %d2.w),%d1
m68k_023132_end:
.org 0x23136
m68k_023136:
        beq.w (. + 96)
m68k_023136_end:
.org 0x2313A
m68k_02313a:
        bsr.w (. + 94)
m68k_02313a_end:
.org 0x2313E
m68k_02313e:
        lea.l 0xff2c00:l,%a0
m68k_02313e_end:
.org 0x23144
m68k_023144:
        lsr.w #0x7,%d0
m68k_023144_end:
.org 0x23146
m68k_023146:
        move.w %d0,(%a0, %d2.w)
m68k_023146_end:
.org 0x2314A
m68k_02314a:
        lsr.w #0x7,%d1
m68k_02314a_end:
.org 0x2314C
m68k_02314c:
        move.w %d1,0x2(%a0, %d2.w)
m68k_02314c_end:
.org 0x23150
m68k_023150:
        lea.l 0xae28:w,%a0
m68k_023150_end:
.org 0x23154
m68k_023154:
        move.b #0x1,(%a0, %d7.w)
m68k_023154_end:
.org 0x2315A
m68k_02315a:
        jsr 0x1a438:l
m68k_02315a_end:
.org 0x23160
m68k_023160:
        lea.l 0xa150:w,%a1
m68k_023160_end:
.org 0x23164
m68k_023164:
        move.w %d7,%d0
m68k_023164_end:
.org 0x23166
m68k_023166:
        lsl.w #0x2,%d0
m68k_023166_end:
.org 0x23168
m68k_023168:
        move.w (%a1, %d0.w),%d1
m68k_023168_end:
.org 0x2316C
m68k_02316c:
        lsr.w #0x7,%d1
m68k_02316c_end:
.org 0x2316E
m68k_02316e:
        move.w 0x2(%a1, %d0.w),%d2
m68k_02316e_end:
.org 0x23172
m68k_023172:
        lsr.w #0x7,%d2
m68k_023172_end:
.org 0x23174
m68k_023174:
        jsr 0x1a44e:l
m68k_023174_end:
.org 0x2317A
m68k_02317a:
        cmpi.b #0x6,%d0
m68k_02317a_end:
.org 0x2317E
m68k_02317e:
        beq.w (. + 14)
m68k_02317e_end:
.org 0x23182
m68k_023182:
        jsr 0x1dcaa:l
m68k_023182_end:
.org 0x23188
m68k_023188:
        bra.w (. + 14)
m68k_023188_end:
.org 0x2318C
m68k_02318c:
        move.w %d7,0xf3a6:w
m68k_02318c_end:
.org 0x23190
m68k_023190:
        jsr 0x1db7c:l
m68k_023190_end:
.org 0x23196
m68k_023196:
        rts
m68k_023196_end:
.org 0x23198
m68k_023198:
        move.w %d7,-(%a7)
m68k_023198_end:
.org 0x2319A
m68k_02319a:
        lea.l 0xa150:w,%a0
m68k_02319a_end:
.org 0x2319E
m68k_02319e:
        move.w %d7,%d2
m68k_02319e_end:
.org 0x231A0
m68k_0231a0:
        lsl.w #0x2,%d2
m68k_0231a0_end:
.org 0x231A2
m68k_0231a2:
        move.w (%a0, %d2.w),%d3
m68k_0231a2_end:
.org 0x231A6
m68k_0231a6:
        move.w 0x2(%a0, %d2.w),%d4
m68k_0231a6_end:
.org 0x231AA
m68k_0231aa:
        lea.l 0xae2f6:l,%a0
m68k_0231aa_end:
.org 0x231B0
m68k_0231b0:
        move.w 0xf68a:w,%d5
m68k_0231b0_end:
.org 0x231B4
m68k_0231b4:
        lsl.w #0x2,%d5
m68k_0231b4_end:
.org 0x231B6
m68k_0231b6:
        move.w 0x2(%a0, %d5.w),%d6
m68k_0231b6_end:
.org 0x231BA
m68k_0231ba:
        move.w (%a0, %d5.w),%d5
m68k_0231ba_end:
.org 0x231BE
m68k_0231be:
        move.w %d3,%d7
m68k_0231be_end:
.org 0x231C0
m68k_0231c0:
        sub.w %d5,%d7
m68k_0231c0_end:
.org 0x231C2
m68k_0231c2:
        bcc.w (. + 6)
m68k_0231c2_end:
.org 0x231C6
m68k_0231c6:
        neg.w %d7
m68k_0231c6_end:
.org 0x231C8
m68k_0231c8:
        cmpi.w #0x1000,%d7
m68k_0231c8_end:
.org 0x231CC
m68k_0231cc:
        bcs.w (. + 92)
m68k_0231cc_end:
.org 0x231D0
m68k_0231d0:
        bhi.w (. + 188)
m68k_0231d0_end:
.org 0x231D4
m68k_0231d4:
        move.w %d4,%d7
m68k_0231d4_end:
.org 0x231D6
m68k_0231d6:
        sub.w %d6,%d7
m68k_0231d6_end:
.org 0x231D8
m68k_0231d8:
        bcc.w (. + 6)
m68k_0231d8_end:
.org 0x231DC
m68k_0231dc:
        neg.w %d7
m68k_0231dc_end:
.org 0x231DE
m68k_0231de:
        cmpi.w #0x1000,%d7
m68k_0231de_end:
.org 0x231E2
m68k_0231e2:
        bhi.w (. + 170)
m68k_0231e2_end:
.org 0x231E6
m68k_0231e6:
        cmp.w %d5,%d3
m68k_0231e6_end:
.org 0x231E8
m68k_0231e8:
        bhi.w (. + 56)
m68k_0231e8_end:
.org 0x231EC
m68k_0231ec:
        cmp.w %d3,%d0
m68k_0231ec_end:
.org 0x231EE
m68k_0231ee:
        bls.w (. + 158)
m68k_0231ee_end:
.org 0x231F2
m68k_0231f2:
        cmp.w %d6,%d1
m68k_0231f2_end:
.org 0x231F4
m68k_0231f4:
        bhi.w (. + 24)
m68k_0231f4_end:
.org 0x231F8
m68k_0231f8:
        move.w %d6,%d7
m68k_0231f8_end:
.org 0x231FA
m68k_0231fa:
        subi.w #0x1000,%d7
m68k_0231fa_end:
.org 0x231FE
m68k_0231fe:
        cmp.w %d4,%d7
m68k_0231fe_end:
.org 0x23200
m68k_023200:
        beq.w (. + 106)
m68k_023200_end:
.org 0x23204
m68k_023204:
        move.w %d3,%d0
m68k_023204_end:
.org 0x23206
m68k_023206:
        move.w %d7,%d1
m68k_023206_end:
.org 0x23208
m68k_023208:
        bra.w (. + 132)
m68k_023208_end:
.org 0x2320C
m68k_02320c:
        move.w %d6,%d7
m68k_02320c_end:
.org 0x2320E
m68k_02320e:
        addi.w #0x1000,%d7
m68k_02320e_end:
.org 0x23212
m68k_023212:
        cmp.w %d4,%d7
m68k_023212_end:
.org 0x23214
m68k_023214:
        beq.w (. + 86)
m68k_023214_end:
.org 0x23218
m68k_023218:
        move.w %d3,%d0
m68k_023218_end:
.org 0x2321A
m68k_02321a:
        move.w %d7,%d1
m68k_02321a_end:
.org 0x2321C
m68k_02321c:
        bra.w (. + 112)
m68k_02321c_end:
.org 0x23220
m68k_023220:
        cmp.w %d3,%d0
m68k_023220_end:
.org 0x23222
m68k_023222:
        bcc.w (. + 106)
m68k_023222_end:
.org 0x23226
m68k_023226:
        bra.b (. + -52)
m68k_023226_end:
.org 0x23228
m68k_023228:
        move.w %d4,%d7
m68k_023228_end:
.org 0x2322A
m68k_02322a:
        sub.w %d6,%d7
m68k_02322a_end:
.org 0x2322C
m68k_02322c:
        bcc.w (. + 6)
m68k_02322c_end:
.org 0x23230
m68k_023230:
        neg.w %d7
m68k_023230_end:
.org 0x23232
m68k_023232:
        cmpi.w #0x1000,%d7
m68k_023232_end:
.org 0x23236
m68k_023236:
        bne.w (. + 86)
m68k_023236_end:
.org 0x2323A
m68k_02323a:
        cmp.w %d6,%d4
m68k_02323a_end:
.org 0x2323C
m68k_02323c:
        bhi.w (. + 38)
m68k_02323c_end:
.org 0x23240
m68k_023240:
        cmp.w %d4,%d1
m68k_023240_end:
.org 0x23242
m68k_023242:
        bls.w (. + 74)
m68k_023242_end:
.org 0x23246
m68k_023246:
        move.w %d4,%d1
m68k_023246_end:
.org 0x23248
m68k_023248:
        cmp.w %d5,%d0
m68k_023248_end:
.org 0x2324A
m68k_02324a:
        bhi.w (. + 14)
m68k_02324a_end:
.org 0x2324E
m68k_02324e:
        move.w %d5,%d0
m68k_02324e_end:
.org 0x23250
m68k_023250:
        subi.w #0x1000,%d0
m68k_023250_end:
.org 0x23254
m68k_023254:
        bra.w (. + 56)
m68k_023254_end:
.org 0x23258
m68k_023258:
        move.w %d5,%d0
m68k_023258_end:
.org 0x2325A
m68k_02325a:
        addi.w #0x1000,%d0
m68k_02325a_end:
.org 0x2325E
m68k_02325e:
        bra.w (. + 46)
m68k_02325e_end:
.org 0x23262
m68k_023262:
        cmp.w %d4,%d1
m68k_023262_end:
.org 0x23264
m68k_023264:
        bcc.w (. + 40)
m68k_023264_end:
.org 0x23268
m68k_023268:
        bra.b (. + -34)
m68k_023268_end:
.org 0x2326A
m68k_02326a:
        move.w %d3,%d5
m68k_02326a_end:
.org 0x2326C
m68k_02326c:
        sub.w %d0,%d5
m68k_02326c_end:
.org 0x2326E
m68k_02326e:
        bcc.w (. + 6)
m68k_02326e_end:
.org 0x23272
m68k_023272:
        neg.w %d5
m68k_023272_end:
.org 0x23274
m68k_023274:
        move.w %d4,%d6
m68k_023274_end:
.org 0x23276
m68k_023276:
        sub.w %d1,%d6
m68k_023276_end:
.org 0x23278
m68k_023278:
        bcc.w (. + 6)
m68k_023278_end:
.org 0x2327C
m68k_02327c:
        neg.w %d6
m68k_02327c_end:
.org 0x2327E
m68k_02327e:
        cmp.w %d5,%d6
m68k_02327e_end:
.org 0x23280
m68k_023280:
        bhi.w (. + 10)
m68k_023280_end:
.org 0x23284
m68k_023284:
        move.w %d4,%d1
m68k_023284_end:
.org 0x23286
m68k_023286:
        bra.w (. + 6)
m68k_023286_end:
.org 0x2328A
m68k_02328a:
        move.w %d3,%d0
m68k_02328a_end:
.org 0x2328C
m68k_02328c:
        move.w (%a7)+,%d7
m68k_02328c_end:
.org 0x2328E
m68k_02328e:
        rts
m68k_02328e_end:
.org 0x23290
m68k_023290:
        move.w %d0,-(%a7)
m68k_023290_end:
.org 0x23292
m68k_023292:
        bsr.w (. + 576)
m68k_023292_end:
.org 0x23296
m68k_023296:
        tst.w 0xd300:w
m68k_023296_end:
.org 0x2329A
m68k_02329a:
        bmi.w (. + 104)
m68k_02329a_end:
.org 0x2329E
m68k_02329e:
        bsr.w (. + 108)
m68k_02329e_end:
.org 0x232A2
m68k_0232a2:
        lea.l 0xb600:w,%a0
m68k_0232a2_end:
.org 0x232A6
m68k_0232a6:
        move.w %d7,%d0
m68k_0232a6_end:
.org 0x232A8
m68k_0232a8:
        lsl.w #0x1,%d0
m68k_0232a8_end:
.org 0x232AA
m68k_0232aa:
        move.w (%a0, %d0.w),%d0
m68k_0232aa_end:
.org 0x232AE
m68k_0232ae:
        clr.w %d2
m68k_0232ae_end:
.org 0x232B0
m68k_0232b0:
        cmpi.w #0x46,%d0
m68k_0232b0_end:
.org 0x232B4
m68k_0232b4:
        bcs.w (. + 16)
m68k_0232b4_end:
.org 0x232B8
m68k_0232b8:
        addq.w #0x1,%d2
m68k_0232b8_end:
.org 0x232BA
m68k_0232ba:
        cmpi.w #0x5a,%d0
m68k_0232ba_end:
.org 0x232BE
m68k_0232be:
        bcs.w (. + 6)
m68k_0232be_end:
.org 0x232C2
m68k_0232c2:
        addq.w #0x1,%d2
m68k_0232c2_end:
.org 0x232C4
m68k_0232c4:
        jsr 0x83d4:l
m68k_0232c4_end:
.org 0x232CA
m68k_0232ca:
        andi.l #0xffff,%d0
m68k_0232ca_end:
.org 0x232D0
m68k_0232d0:
        lsl.l #0x2,%d0
m68k_0232d0_end:
.org 0x232D2
m68k_0232d2:
        swap %d0
m68k_0232d2_end:
.org 0x232D4
m68k_0232d4:
        cmp.w %d2,%d0
m68k_0232d4_end:
.org 0x232D6
m68k_0232d6:
        bcs.w (. + 18)
m68k_0232d6_end:
.org 0x232DA
m68k_0232da:
        bsr.w (. + 148)
m68k_0232da_end:
.org 0x232DE
m68k_0232de:
        move.w (%a7)+,%d0
m68k_0232de_end:
.org 0x232E0
m68k_0232e0:
        ori.w #0x1,%sr
m68k_0232e0_end:
.org 0x232E4
m68k_0232e4:
        bra.w (. + 36)
m68k_0232e4_end:
.org 0x232E8
m68k_0232e8:
        lea.l 0xa754:w,%a0
m68k_0232e8_end:
.org 0x232EC
m68k_0232ec:
        tst.b (%a0, %d7.w)
m68k_0232ec_end:
.org 0x232F0
m68k_0232f0:
        bne.b (. + -22)
m68k_0232f0_end:
.org 0x232F2
m68k_0232f2:
        bsr.w (. + 11488)
m68k_0232f2_end:
.org 0x232F6
m68k_0232f6:
        bcc.b (. + -28)
m68k_0232f6_end:
.org 0x232F8
m68k_0232f8:
        move.w (%a7)+,%d0
m68k_0232f8_end:
.org 0x232FA
m68k_0232fa:
        ori.w #0x1,%sr
m68k_0232fa_end:
.org 0x232FE
m68k_0232fe:
        bra.w (. + 10)
m68k_0232fe_end:
.org 0x23302
m68k_023302:
        move.w (%a7)+,%d0
m68k_023302_end:
.org 0x23304
m68k_023304:
        andi.w #0xfffe,%sr
m68k_023304_end:
.org 0x23308
m68k_023308:
        rts
m68k_023308_end:
.org 0x2330A
m68k_02330a:
        move.l %d7,-(%a7)
m68k_02330a_end:
.org 0x2330C
m68k_02330c:
        tst.w 0xd302:w
m68k_02330c_end:
.org 0x23310
m68k_023310:
        bmi.w (. + 82)
m68k_023310_end:
.org 0x23314
m68k_023314:
        lea.l 0xae2f6:l,%a0
m68k_023314_end:
.org 0x2331A
m68k_02331a:
        move.w 0xf68a:w,%d0
m68k_02331a_end:
.org 0x2331E
m68k_02331e:
        lsl.w #0x2,%d0
m68k_02331e_end:
.org 0x23320
m68k_023320:
        move.w (%a0, %d0.w),%d1
m68k_023320_end:
.org 0x23324
m68k_023324:
        move.w 0x2(%a0, %d0.w),%d2
m68k_023324_end:
.org 0x23328
m68k_023328:
        lea.l 0xa150:w,%a0
m68k_023328_end:
.org 0x2332C
m68k_02332c:
        lea.l 0xd300:w,%a1
m68k_02332c_end:
.org 0x23330
m68k_023330:
        move.w #0xffff,%d3
m68k_023330_end:
.org 0x23334
m68k_023334:
        move.w (%a1)+,%d5
m68k_023334_end:
.org 0x23336
m68k_023336:
        bmi.w (. + 48)
m68k_023336_end:
.org 0x2333A
m68k_02333a:
        move.w %d5,%d6
m68k_02333a_end:
.org 0x2333C
m68k_02333c:
        lsl.w #0x2,%d6
m68k_02333c_end:
.org 0x2333E
m68k_02333e:
        move.w 0x2(%a0, %d6.w),%d7
m68k_02333e_end:
.org 0x23342
m68k_023342:
        sub.w %d2,%d7
m68k_023342_end:
.org 0x23344
m68k_023344:
        bcc.w (. + 6)
m68k_023344_end:
.org 0x23348
m68k_023348:
        neg.w %d7
m68k_023348_end:
.org 0x2334A
m68k_02334a:
        move.w (%a0, %d6.w),%d6
m68k_02334a_end:
.org 0x2334E
m68k_02334e:
        sub.w %d1,%d6
m68k_02334e_end:
.org 0x23350
m68k_023350:
        bcc.w (. + 6)
m68k_023350_end:
.org 0x23354
m68k_023354:
        neg.w %d6
m68k_023354_end:
.org 0x23356
m68k_023356:
        add.w %d6,%d7
m68k_023356_end:
.org 0x23358
m68k_023358:
        cmp.w %d3,%d7
m68k_023358_end:
.org 0x2335A
m68k_02335a:
        bcc.b (. + -38)
m68k_02335a_end:
.org 0x2335C
m68k_02335c:
        move.w %d7,%d3
m68k_02335c_end:
.org 0x2335E
m68k_02335e:
        move.w %d5,%d4
m68k_02335e_end:
.org 0x23360
m68k_023360:
        bra.b (. + -44)
m68k_023360_end:
.org 0x23362
m68k_023362:
        move.w 0xd300:w,%d4
m68k_023362_end:
.org 0x23366
m68k_023366:
        move.w %d4,0xf3a6:w
m68k_023366_end:
.org 0x2336A
m68k_02336a:
        move.l (%a7)+,%d7
m68k_02336a_end:
.org 0x2336C
m68k_02336c:
        rts
m68k_02336c_end:
.org 0x2336E
m68k_02336e:
        lea.l 0xa150:w,%a0
m68k_02336e_end:
.org 0x23372
m68k_023372:
        move.w 0xf3a6:w,%d0
m68k_023372_end:
.org 0x23376
m68k_023376:
        lsl.w #0x2,%d0
m68k_023376_end:
.org 0x23378
m68k_023378:
        move.w 0x2(%a0, %d0.w),%d1
m68k_023378_end:
.org 0x2337C
m68k_02337c:
        move.w (%a0, %d0.w),%d0
m68k_02337c_end:
.org 0x23380
m68k_023380:
        bsr.w (. + -488)
m68k_023380_end:
.org 0x23384
m68k_023384:
        move.w %d7,%d2
m68k_023384_end:
.org 0x23386
m68k_023386:
        lsl.w #0x2,%d2
m68k_023386_end:
.org 0x23388
m68k_023388:
        lea.l 0xff2c00:l,%a0
m68k_023388_end:
.org 0x2338E
m68k_02338e:
        lsr.w #0x7,%d0
m68k_02338e_end:
.org 0x23390
m68k_023390:
        move.w %d0,(%a0, %d2.w)
m68k_023390_end:
.org 0x23394
m68k_023394:
        lsr.w #0x7,%d1
m68k_023394_end:
.org 0x23396
m68k_023396:
        move.w %d1,0x2(%a0, %d2.w)
m68k_023396_end:
.org 0x2339A
m68k_02339a:
        lea.l 0xae28:w,%a0
m68k_02339a_end:
.org 0x2339E
m68k_02339e:
        move.b #0x1,(%a0, %d7.w)
m68k_02339e_end:
.org 0x233A4
m68k_0233a4:
        jsr 0x1a438:l
m68k_0233a4_end:
.org 0x233AA
m68k_0233aa:
        lea.l 0xa150:w,%a1
m68k_0233aa_end:
.org 0x233AE
m68k_0233ae:
        move.w %d7,%d0
m68k_0233ae_end:
.org 0x233B0
m68k_0233b0:
        lsl.w #0x2,%d0
m68k_0233b0_end:
.org 0x233B2
m68k_0233b2:
        move.w (%a1, %d0.w),%d1
m68k_0233b2_end:
.org 0x233B6
m68k_0233b6:
        lsr.w #0x7,%d1
m68k_0233b6_end:
.org 0x233B8
m68k_0233b8:
        move.w 0x2(%a1, %d0.w),%d2
m68k_0233b8_end:
.org 0x233BC
m68k_0233bc:
        lsr.w #0x7,%d2
m68k_0233bc_end:
.org 0x233BE
m68k_0233be:
        jsr 0x1a44e:l
m68k_0233be_end:
.org 0x233C4
m68k_0233c4:
        cmpi.b #0x6,%d0
m68k_0233c4_end:
.org 0x233C8
m68k_0233c8:
        beq.w (. + 14)
m68k_0233c8_end:
.org 0x233CC
m68k_0233cc:
        jsr 0x1dcaa:l
m68k_0233cc_end:
.org 0x233D2
m68k_0233d2:
        bra.w (. + 14)
m68k_0233d2_end:
.org 0x233D6
m68k_0233d6:
        move.w %d7,0xf3a6:w
m68k_0233d6_end:
.org 0x233DA
m68k_0233da:
        jsr 0x1db7c:l
m68k_0233da_end:
.org 0x233E0
m68k_0233e0:
        rts
m68k_0233e0_end:
.org 0x233E2
m68k_0233e2:
        lea.l 0xf69e:w,%a0
m68k_0233e2_end:
.org 0x233E6
m68k_0233e6:
        lea.l 0xf6a2:w,%a1
m68k_0233e6_end:
.org 0x233EA
m68k_0233ea:
        btst.b #0x1,0xf6d7:w
m68k_0233ea_end:
.org 0x233F0
m68k_0233f0:
        beq.w (. + 6)
m68k_0233f0_end:
.org 0x233F4
m68k_0233f4:
        exg %a0,%a1
m68k_0233f4_end:
.org 0x233F6
m68k_0233f6:
        move.l (%a0),%d0
m68k_0233f6_end:
.org 0x233F8
m68k_0233f8:
        cmp.l (%a1),%d0
m68k_0233f8_end:
.org 0x233FA
m68k_0233fa:
        bcc.w (. + 20)
m68k_0233fa_end:
.org 0x233FE
m68k_0233fe:
        cmp.l 0xf768:w,%d0
m68k_0233fe_end:
.org 0x23402
m68k_023402:
        bcc.w (. + 12)
m68k_023402_end:
.org 0x23406
m68k_023406:
        ori.w #0x1,%sr
m68k_023406_end:
.org 0x2340A
m68k_02340a:
        bra.w (. + 8)
m68k_02340a_end:
.org 0x2340E
m68k_02340e:
        andi.w #0xfffe,%sr
m68k_02340e_end:
.org 0x23412
m68k_023412:
        rts
m68k_023412_end:
.org 0x23414
m68k_023414:
        bsr.w (. + -974)
m68k_023414_end:
.org 0x23418
m68k_023418:
        bcs.w (. + -1548)
m68k_023418_end:
.org 0x2341C
m68k_02341c:
        bsr.w (. + -1822)
m68k_02341c_end:
.org 0x23420
m68k_023420:
        bcs.w (. + -1102)
m68k_023420_end:
.org 0x23424
m68k_023424:
        bsr.b (. + -66)
m68k_023424_end:
.org 0x23426
m68k_023426:
        bcs.w (. + -1562)
m68k_023426_end:
.org 0x2342A
m68k_02342a:
        bsr.w (. + -3284)
m68k_02342a_end:
.org 0x2342E
m68k_02342e:
        bcs.w (. + 24)
m68k_02342e_end:
.org 0x23432
m68k_023432:
        bsr.w (. + -1794)
m68k_023432_end:
.org 0x23436
m68k_023436:
        bcs.w (. + 16)
m68k_023436_end:
.org 0x2343A
m68k_02343a:
        bsr.w (. + -2736)
m68k_02343a_end:
.org 0x2343E
m68k_02343e:
        bcs.w (. + 8)
m68k_02343e_end:
.org 0x23442
m68k_023442:
        bsr.w (. + 6)
m68k_023442_end:
.org 0x23446
m68k_023446:
        rts
m68k_023446_end:
.org 0x23448
m68k_023448:
        move.w 0xff3ec4:l,%d0
m68k_023448_end:
.org 0x2344E
m68k_02344e:
        bra.w (. + -874)
m68k_02344e_end:
.org 0x23452
m68k_023452:
        bsr.w (. + -1036)
m68k_023452_end:
.org 0x23456
m68k_023456:
        bcs.w (. + -1376)
m68k_023456_end:
.org 0x2345A
m68k_02345a:
        bsr.w (. + -1884)
m68k_02345a_end:
.org 0x2345E
m68k_02345e:
        bcs.w (. + -1164)
m68k_02345e_end:
.org 0x23462
m68k_023462:
        bsr.w (. + -128)
m68k_023462_end:
.org 0x23466
m68k_023466:
        bcs.w (. + -1392)
m68k_023466_end:
.org 0x2346A
m68k_02346a:
        bsr.w (. + -3348)
m68k_02346a_end:
.org 0x2346E
m68k_02346e:
        bcs.w (. + 24)
m68k_02346e_end:
.org 0x23472
m68k_023472:
        bsr.w (. + -1858)
m68k_023472_end:
.org 0x23476
m68k_023476:
        bcs.w (. + 16)
m68k_023476_end:
.org 0x2347A
m68k_02347a:
        bsr.w (. + -2800)
m68k_02347a_end:
.org 0x2347E
m68k_02347e:
        bcs.w (. + 8)
m68k_02347e_end:
.org 0x23482
m68k_023482:
        bsr.w (. + 6)
m68k_023482_end:
.org 0x23486
m68k_023486:
        rts
m68k_023486_end:
.org 0x23488
m68k_023488:
        move.w 0xff3ec6:l,%d0
m68k_023488_end:
.org 0x2348E
m68k_02348e:
        bra.w (. + -938)
m68k_02348e_end:
.org 0x23492
m68k_023492:
        bsr.w (. + -1100)
m68k_023492_end:
.org 0x23496
m68k_023496:
        bcs.w (. + -2390)
m68k_023496_end:
.org 0x2349A
m68k_02349a:
        bsr.w (. + -1948)
m68k_02349a_end:
.org 0x2349E
m68k_02349e:
        bcs.w (. + -1228)
m68k_02349e_end:
.org 0x234A2
m68k_0234a2:
        bsr.w (. + -192)
m68k_0234a2_end:
.org 0x234A6
m68k_0234a6:
        bcs.w (. + -2406)
m68k_0234a6_end:
.org 0x234AA
m68k_0234aa:
        bsr.w (. + -3412)
m68k_0234aa_end:
.org 0x234AE
m68k_0234ae:
        bcs.w (. + 24)
m68k_0234ae_end:
.org 0x234B2
m68k_0234b2:
        bsr.w (. + -1922)
m68k_0234b2_end:
.org 0x234B6
m68k_0234b6:
        bcs.w (. + 16)
m68k_0234b6_end:
.org 0x234BA
m68k_0234ba:
        bsr.w (. + -2864)
m68k_0234ba_end:
.org 0x234BE
m68k_0234be:
        bcs.w (. + 8)
m68k_0234be_end:
.org 0x234C2
m68k_0234c2:
        bsr.w (. + 6)
m68k_0234c2_end:
.org 0x234C6
m68k_0234c6:
        rts
m68k_0234c6_end:
.org 0x234C8
m68k_0234c8:
        move.w 0xff3ec8:l,%d0
m68k_0234c8_end:
.org 0x234CE
m68k_0234ce:
        bra.w (. + -1002)
m68k_0234ce_end:
.org 0x234D2
m68k_0234d2:
        lea.l 0xc400:w,%a0
m68k_0234d2_end:
.org 0x234D6
m68k_0234d6:
        clr.w %d3
m68k_0234d6_end:
.org 0x234D8
m68k_0234d8:
        move.b (%a0, %d7.w),%d3
m68k_0234d8_end:
.org 0x234DC
m68k_0234dc:
        move.w %d3,%d5
m68k_0234dc_end:
.org 0x234DE
m68k_0234de:
        lsl.w #0x2,%d3
m68k_0234de_end:
.org 0x234E0
m68k_0234e0:
        add.w %d5,%d3
m68k_0234e0_end:
.org 0x234E2
m68k_0234e2:
        lsl.w #0x1,%d3
m68k_0234e2_end:
.org 0x234E4
m68k_0234e4:
        lea.l 0xd300:w,%a0
m68k_0234e4_end:
.org 0x234E8
m68k_0234e8:
        lea.l 0xa150:w,%a1
m68k_0234e8_end:
.org 0x234EC
m68k_0234ec:
        move.w %d7,%d2
m68k_0234ec_end:
.org 0x234EE
m68k_0234ee:
        lsl.w #0x2,%d2
m68k_0234ee_end:
.org 0x234F0
m68k_0234f0:
        move.w (%a1, %d2.w),%d1
m68k_0234f0_end:
.org 0x234F4
m68k_0234f4:
        move.w 0x2(%a1, %d2.w),%d2
m68k_0234f4_end:
.org 0x234F8
m68k_0234f8:
        lea.l 0xff3bc2:l,%a4
m68k_0234f8_end:
.org 0x234FE
m68k_0234fe:
        btst.b #0x1,0xf6d7:w
m68k_0234fe_end:
.org 0x23504
m68k_023504:
        bne.w (. + 12)
m68k_023504_end:
.org 0x23508
m68k_023508:
        lea.l 0xa5a4:w,%a2
m68k_023508_end:
.org 0x2350C
m68k_02350c:
        bra.w (. + 8)
m68k_02350c_end:
.org 0x23510
m68k_023510:
        lea.l 0xa550:w,%a2
m68k_023510_end:
.org 0x23514
m68k_023514:
        move.w (%a2)+,%d4
m68k_023514_end:
.org 0x23516
m68k_023516:
        bmi.w (. + 70)
m68k_023516_end:
.org 0x2351A
m68k_02351a:
        tst.b (%a4, %d4.w)
m68k_02351a_end:
.org 0x2351E
m68k_02351e:
        bne.b (. + -10)
m68k_02351e_end:
.org 0x23520
m68k_023520:
        move.w %d4,%d5
m68k_023520_end:
.org 0x23522
m68k_023522:
        lsl.w #0x2,%d5
m68k_023522_end:
.org 0x23524
m68k_023524:
        move.w 0x2(%a1, %d5.w),%d0
m68k_023524_end:
.org 0x23528
m68k_023528:
        sub.w %d2,%d0
m68k_023528_end:
.org 0x2352A
m68k_02352a:
        bcc.w (. + 6)
m68k_02352a_end:
.org 0x2352E
m68k_02352e:
        neg.w %d0
m68k_02352e_end:
.org 0x23530
m68k_023530:
        lsr.w #0x7,%d0
m68k_023530_end:
.org 0x23532
m68k_023532:
        cmp.w %d3,%d0
m68k_023532_end:
.org 0x23534
m68k_023534:
        bhi.b (. + -32)
m68k_023534_end:
.org 0x23536
m68k_023536:
        mulu.w %d0,%d0
m68k_023536_end:
.org 0x23538
m68k_023538:
        move.w (%a1, %d5.w),%d5
m68k_023538_end:
.org 0x2353C
m68k_02353c:
        sub.w %d1,%d5
m68k_02353c_end:
.org 0x2353E
m68k_02353e:
        bcc.w (. + 6)
m68k_02353e_end:
.org 0x23542
m68k_023542:
        neg.w %d5
m68k_023542_end:
.org 0x23544
m68k_023544:
        lsr.w #0x7,%d5
m68k_023544_end:
.org 0x23546
m68k_023546:
        cmp.w %d3,%d5
m68k_023546_end:
.org 0x23548
m68k_023548:
        bhi.b (. + -52)
m68k_023548_end:
.org 0x2354A
m68k_02354a:
        mulu.w %d5,%d5
m68k_02354a_end:
.org 0x2354C
m68k_02354c:
        add.l %d5,%d0
m68k_02354c_end:
.org 0x2354E
m68k_02354e:
        jsr 0x3080e:l
m68k_02354e_end:
.org 0x23554
m68k_023554:
        cmp.w %d3,%d0
m68k_023554_end:
.org 0x23556
m68k_023556:
        bhi.b (. + -66)
m68k_023556_end:
.org 0x23558
m68k_023558:
        move.w %d4,(%a0)+
m68k_023558_end:
.org 0x2355A
m68k_02355a:
        bra.b (. + -70)
m68k_02355a_end:
.org 0x2355C
m68k_02355c:
        move.w #0xffff,(%a0)
m68k_02355c_end:
.org 0x23560
m68k_023560:
        rts
m68k_023560_end:
.org 0x23610
m68k_023610:
        bsr.w (. + 670)
m68k_023610_end:
.org 0x23614
m68k_023614:
        bcs.w (. + 40)
m68k_023614_end:
.org 0x23618
m68k_023618:
        bsr.w (. + 1026)
m68k_023618_end:
.org 0x2361C
m68k_02361c:
        bcs.w (. + 1114)
m68k_02361c_end:
.org 0x23620
m68k_023620:
        bsr.w (. + 1052)
m68k_023620_end:
.org 0x23624
m68k_023624:
        bcs.w (. + 3282)
m68k_023624_end:
.org 0x23628
m68k_023628:
        bsr.w (. + 270)
m68k_023628_end:
.org 0x2362C
m68k_02362c:
        bcs.w (. + 16)
m68k_02362c_end:
.org 0x23630
m68k_023630:
        bsr.w (. + 14)
m68k_023630_end:
.org 0x23634
m68k_023634:
        bcs.w (. + 8)
m68k_023634_end:
.org 0x23638
m68k_023638:
        bsr.w (. + 172)
m68k_023638_end:
.org 0x2363C
m68k_02363c:
        rts
m68k_02363c_end:
.org 0x2363E
m68k_02363e:
        lea.l 0xa654:w,%a0
m68k_02363e_end:
.org 0x23642
m68k_023642:
        tst.b (%a0, %d7.w)
m68k_023642_end:
.org 0x23646
m68k_023646:
        bne.w (. + 152)
m68k_023646_end:
.org 0x2364A
m68k_02364a:
        lea.l 0xff3cc2:l,%a0
m68k_02364a_end:
.org 0x23650
m68k_023650:
        tst.b (%a0, %d7.w)
m68k_023650_end:
.org 0x23654
m68k_023654:
        bne.w (. + 138)
m68k_023654_end:
.org 0x23658
m68k_023658:
        lea.l 0xff3dc2:l,%a1
m68k_023658_end:
.org 0x2365E
m68k_02365e:
        tst.b (%a1, %d7.w)
m68k_02365e_end:
.org 0x23662
m68k_023662:
        bne.w (. + 124)
m68k_023662_end:
.org 0x23666
m68k_023666:
        lea.l 0x9fff:w,%a0
m68k_023666_end:
.org 0x2366A
m68k_02366a:
        move.w 0xf68a:w,%d0
m68k_02366a_end:
.org 0x2366E
m68k_02366e:
        clr.w %d1
m68k_02366e_end:
.org 0x23670
m68k_023670:
        move.b (%a0, %d0.w),%d1
m68k_023670_end:
.org 0x23674
m68k_023674:
        lea.l 0xabda8:l,%a0
m68k_023674_end:
.org 0x2367A
m68k_02367a:
        move.w 0xf68a:w,%d0
m68k_02367a_end:
.org 0x2367E
m68k_02367e:
        lsl.w #0x5,%d0
m68k_02367e_end:
.org 0x23680
m68k_023680:
        lsl.w #0x1,%d1
m68k_023680_end:
.org 0x23682
m68k_023682:
        add.w %d1,%d0
m68k_023682_end:
.org 0x23684
m68k_023684:
        clr.w %d1
m68k_023684_end:
.org 0x23686
m68k_023686:
        move.b (%a0, %d0.w),%d1
m68k_023686_end:
.org 0x2368A
m68k_02368a:
        lsl.w #0x3,%d1
m68k_02368a_end:
.org 0x2368C
m68k_02368c:
        lsl.w #0x7,%d1
m68k_02368c_end:
.org 0x2368E
m68k_02368e:
        clr.w %d2
m68k_02368e_end:
.org 0x23690
m68k_023690:
        move.b 0x1(%a0, %d0.w),%d2
m68k_023690_end:
.org 0x23694
m68k_023694:
        lsl.w #0x3,%d2
m68k_023694_end:
.org 0x23696
m68k_023696:
        lsl.w #0x7,%d2
m68k_023696_end:
.org 0x23698
m68k_023698:
        lea.l 0xa150:w,%a0
m68k_023698_end:
.org 0x2369C
m68k_02369c:
        move.w %d7,%d0
m68k_02369c_end:
.org 0x2369E
m68k_02369e:
        lsl.w #0x2,%d0
m68k_02369e_end:
.org 0x236A0
m68k_0236a0:
        cmp.w (%a0, %d0.w),%d1
m68k_0236a0_end:
.org 0x236A4
m68k_0236a4:
        bne.w (. + 12)
m68k_0236a4_end:
.org 0x236A8
m68k_0236a8:
        cmp.w 0x2(%a0, %d0.w),%d2
m68k_0236a8_end:
.org 0x236AC
m68k_0236ac:
        beq.w (. + 54)
m68k_0236ac_end:
.org 0x236B0
m68k_0236b0:
        lea.l 0xff2c00:l,%a0
m68k_0236b0_end:
.org 0x236B6
m68k_0236b6:
        move.w %d7,%d0
m68k_0236b6_end:
.org 0x236B8
m68k_0236b8:
        lsl.w #0x2,%d0
m68k_0236b8_end:
.org 0x236BA
m68k_0236ba:
        lsr.w #0x7,%d1
m68k_0236ba_end:
.org 0x236BC
m68k_0236bc:
        move.w %d1,(%a0, %d0.w)
m68k_0236bc_end:
.org 0x236C0
m68k_0236c0:
        lsr.w #0x7,%d2
m68k_0236c0_end:
.org 0x236C2
m68k_0236c2:
        move.w %d2,0x2(%a0, %d0.w)
m68k_0236c2_end:
.org 0x236C6
m68k_0236c6:
        lea.l 0xae28:w,%a0
m68k_0236c6_end:
.org 0x236CA
m68k_0236ca:
        move.b #0x1,(%a0, %d7.w)
m68k_0236ca_end:
.org 0x236D0
m68k_0236d0:
        jsr 0x1dcaa:l
m68k_0236d0_end:
.org 0x236D6
m68k_0236d6:
        ori.w #0x1,%sr
m68k_0236d6_end:
.org 0x236DA
m68k_0236da:
        bra.w (. + 8)
m68k_0236da_end:
.org 0x236DE
m68k_0236de:
        andi.w #0xfffe,%sr
m68k_0236de_end:
.org 0x236E2
m68k_0236e2:
        rts
m68k_0236e2_end:
.org 0x236E4
m68k_0236e4:
        lea.l 0xb600:w,%a0
m68k_0236e4_end:
.org 0x236E8
m68k_0236e8:
        move.w %d7,%d0
m68k_0236e8_end:
.org 0x236EA
m68k_0236ea:
        lsl.w #0x1,%d0
m68k_0236ea_end:
.org 0x236EC
m68k_0236ec:
        move.w (%a0, %d0.w),%d1
m68k_0236ec_end:
.org 0x236F0
m68k_0236f0:
        move.w #0x1,%d2
m68k_0236f0_end:
.org 0x236F4
m68k_0236f4:
        cmpi.w #0x3c,%d1
m68k_0236f4_end:
.org 0x236F8
m68k_0236f8:
        bcs.w (. + 26)
m68k_0236f8_end:
.org 0x236FC
m68k_0236fc:
        addq.w #0x1,%d2
m68k_0236fc_end:
.org 0x236FE
m68k_0236fe:
        cmpi.w #0x50,%d1
m68k_0236fe_end:
.org 0x23702
m68k_023702:
        bcs.w (. + 16)
m68k_023702_end:
.org 0x23706
m68k_023706:
        addq.w #0x1,%d1
m68k_023706_end:
.org 0x23708
m68k_023708:
        cmpi.w #0x64,%d1
m68k_023708_end:
.org 0x2370C
m68k_02370c:
        bcs.w (. + 6)
m68k_02370c_end:
.org 0x23710
m68k_023710:
        addq.w #0x1,%d1
m68k_023710_end:
.org 0x23712
m68k_023712:
        jsr 0x83d4:l
m68k_023712_end:
.org 0x23718
m68k_023718:
        andi.l #0xffff,%d0
m68k_023718_end:
.org 0x2371E
m68k_02371e:
        lsl.l #0x2,%d0
m68k_02371e_end:
.org 0x23720
m68k_023720:
        swap %d0
m68k_023720_end:
.org 0x23722
m68k_023722:
        cmp.w %d2,%d0
m68k_023722_end:
.org 0x23724
m68k_023724:
        bcc.w (. + 12)
m68k_023724_end:
.org 0x23728
m68k_023728:
        bsr.w (. + 11832)
m68k_023728_end:
.org 0x2372C
m68k_02372c:
        bra.w (. + 8)
m68k_02372c_end:
.org 0x23730
m68k_023730:
        andi.w #0xfffe,%sr
m68k_023730_end:
.org 0x23734
m68k_023734:
        rts
m68k_023734_end:
.org 0x23736
m68k_023736:
        lea.l 0xff3cc2:l,%a0
m68k_023736_end:
.org 0x2373C
m68k_02373c:
        tst.b (%a0, %d7.w)
m68k_02373c_end:
.org 0x23740
m68k_023740:
        bne.w (. + 360)
m68k_023740_end:
.org 0x23744
m68k_023744:
        lea.l 0xff3dc2:l,%a1
m68k_023744_end:
.org 0x2374A
m68k_02374a:
        tst.b (%a1, %d7.w)
m68k_02374a_end:
.org 0x2374E
m68k_02374e:
        bne.w (. + 346)
m68k_02374e_end:
.org 0x23752
m68k_023752:
        lea.l 0xae1b2:l,%a0
m68k_023752_end:
.org 0x23758
m68k_023758:
        move.w 0xf68a:w,%d0
m68k_023758_end:
.org 0x2375C
m68k_02375c:
        lsl.w #0x3,%d0
m68k_02375c_end:
.org 0x2375E
m68k_02375e:
        move.w (%a0, %d0.w),%d1
m68k_02375e_end:
.org 0x23762
m68k_023762:
        move.w 0x2(%a0, %d0.w),%d2
m68k_023762_end:
.org 0x23766
m68k_023766:
        move.w 0x4(%a0, %d0.w),%d3
m68k_023766_end:
.org 0x2376A
m68k_02376a:
        move.w 0x6(%a0, %d0.w),%d4
m68k_02376a_end:
.org 0x2376E
m68k_02376e:
        lea.l 0xa150:w,%a0
m68k_02376e_end:
.org 0x23772
m68k_023772:
        move.w %d7,%d0
m68k_023772_end:
.org 0x23774
m68k_023774:
        lsl.w #0x2,%d0
m68k_023774_end:
.org 0x23776
m68k_023776:
        cmp.w (%a0, %d0.w),%d1
m68k_023776_end:
.org 0x2377A
m68k_02377a:
        bhi.w (. + 302)
m68k_02377a_end:
.org 0x2377E
m68k_02377e:
        cmp.w (%a0, %d0.w),%d2
m68k_02377e_end:
.org 0x23782
m68k_023782:
        bcs.w (. + 294)
m68k_023782_end:
.org 0x23786
m68k_023786:
        cmp.w 0x2(%a0, %d0.w),%d3
m68k_023786_end:
.org 0x2378A
m68k_02378a:
        bhi.w (. + 286)
m68k_02378a_end:
.org 0x2378E
m68k_02378e:
        cmp.w 0x2(%a0, %d0.w),%d4
m68k_02378e_end:
.org 0x23792
m68k_023792:
        bcs.w (. + 278)
m68k_023792_end:
.org 0x23796
m68k_023796:
        move.w %d7,0xf3f2:w
m68k_023796_end:
.org 0x2379A
m68k_02379a:
        bsr.w (. + -21302)
m68k_02379a_end:
.org 0x2379E
m68k_02379e:
        move.w %d7,-(%a7)
m68k_02379e_end:
.org 0x237A0
m68k_0237a0:
        move.w %d6,0xf3a6:w
m68k_0237a0_end:
.org 0x237A4
m68k_0237a4:
        bmi.w (. + 14)
m68k_0237a4_end:
.org 0x237A8
m68k_0237a8:
        jsr 0x1e422:l
m68k_0237a8_end:
.org 0x237AE
m68k_0237ae:
        bcs.w (. + 88)
m68k_0237ae_end:
.org 0x237B2
m68k_0237b2:
        move.w #0x12f,0xf740:w
m68k_0237b2_end:
.org 0x237B8
m68k_0237b8:
        bchg.b #0x1,0xf6d7:w
m68k_0237b8_end:
.org 0x237BE
m68k_0237be:
        jsr 0x260e4:l
m68k_0237be_end:
.org 0x237C4
m68k_0237c4:
        bchg.b #0x1,0xf6d7:w
m68k_0237c4_end:
.org 0x237CA
m68k_0237ca:
        jsr 0x183f8:l
m68k_0237ca_end:
.org 0x237D0
m68k_0237d0:
        cmpi.w #0x411,0xf612:w
m68k_0237d0_end:
.org 0x237D6
m68k_0237d6:
        beq.w (. + 200)
m68k_0237d6_end:
.org 0x237DA
m68k_0237da:
        move.w 0xf68a:w,%d0
m68k_0237da_end:
.org 0x237DE
m68k_0237de:
        lsl.w #0x2,%d0
m68k_0237de_end:
.org 0x237E0
m68k_0237e0:
        lea.l 0xe59c:w,%a0
m68k_0237e0_end:
.org 0x237E4
m68k_0237e4:
        move.l (%a0, %d0.w),0xf3c8:w
m68k_0237e4_end:
.org 0x237EA
m68k_0237ea:
        move.w #0x113,0xf740:w
m68k_0237ea_end:
.org 0x237F0
m68k_0237f0:
        bchg.b #0x1,0xf6d7:w
m68k_0237f0_end:
.org 0x237F6
m68k_0237f6:
        jsr 0x260e4:l
m68k_0237f6_end:
.org 0x237FC
m68k_0237fc:
        bchg.b #0x1,0xf6d7:w
m68k_0237fc_end:
.org 0x23802
m68k_023802:
        bra.w (. + 156)
m68k_023802_end:
.org 0x23806
m68k_023806:
        move.w 0xf3f2:w,0xf3d0:w
m68k_023806_end:
.org 0x2380C
m68k_02380c:
        move.w 0xf3a6:w,0xf3d2:w
m68k_02380c_end:
.org 0x23812
m68k_023812:
        move.w #0x114,0xf740:w
m68k_023812_end:
.org 0x23818
m68k_023818:
        bchg.b #0x1,0xf6d7:w
m68k_023818_end:
.org 0x2381E
m68k_02381e:
        jsr 0x260e4:l
m68k_02381e_end:
.org 0x23824
m68k_023824:
        bchg.b #0x1,0xf6d7:w
m68k_023824_end:
.org 0x2382A
m68k_02382a:
        move.w 0xf3f2:w,0xf702:w
m68k_02382a_end:
.org 0x23830
m68k_023830:
        move.w 0xf3a6:w,0xf706:w
m68k_023830_end:
.org 0x23836
m68k_023836:
        move.w 0xf612:w,-(%a7)
m68k_023836_end:
.org 0x2383A
m68k_02383a:
        move.w 0xf362:w,-(%a7)
m68k_02383a_end:
.org 0x2383E
m68k_02383e:
        move.w #0x2,0xf772:w
m68k_02383e_end:
.org 0x23844
m68k_023844:
        move.w #0x407,0xf612:w
m68k_023844_end:
.org 0x2384A
m68k_02384a:
        move.w #0x3,0xf362:w
m68k_02384a_end:
.org 0x23850
m68k_023850:
        clr.w 0xf352:w
m68k_023850_end:
.org 0x23854
m68k_023854:
        move.w #0x2500,%sr
m68k_023854_end:
.org 0x23858
m68k_023858:
        cmpi.w #0xc4,0xf600:w
m68k_023858_end:
.org 0x2385E
m68k_02385e:
        bne.b (. + -6)
m68k_02385e_end:
.org 0x23860
m68k_023860:
        move.w #0x2700,%sr
m68k_023860_end:
.org 0x23864
m68k_023864:
        jsr 0xdc0:l
m68k_023864_end:
.org 0x2386A
m68k_02386a:
        move.w #0x2500,%sr
m68k_02386a_end:
.org 0x2386E
m68k_02386e:
        cmpi.w #0x84,0xf600:w
m68k_02386e_end:
.org 0x23874
m68k_023874:
        bne.b (. + -6)
m68k_023874_end:
.org 0x23876
m68k_023876:
        jsr 0x17602:l
m68k_023876_end:
.org 0x2387C
m68k_02387c:
        move.w #0x2500,%sr
m68k_02387c_end:
.org 0x23880
m68k_023880:
        cmpi.w #0x408,0xf612:w
m68k_023880_end:
.org 0x23886
m68k_023886:
        beq.w (. + 12)
m68k_023886_end:
.org 0x2388A
m68k_02388a:
        cmpi.w #0x411,0xf612:w
m68k_02388a_end:
.org 0x23890
m68k_023890:
        bne.b (. + -16)
m68k_023890_end:
.org 0x23892
m68k_023892:
        move.w #0x2700,%sr
m68k_023892_end:
.org 0x23896
m68k_023896:
        move.w (%a7)+,0xf362:w
m68k_023896_end:
.org 0x2389A
m68k_02389a:
        move.w (%a7)+,0xf612:w
m68k_02389a_end:
.org 0x2389E
m68k_02389e:
        move.w (%a7)+,%d7
m68k_02389e_end:
.org 0x238A0
m68k_0238a0:
        ori.w #0x1,%sr
m68k_0238a0_end:
.org 0x238A4
m68k_0238a4:
        bra.w (. + 8)
m68k_0238a4_end:
.org 0x238A8
m68k_0238a8:
        andi.w #0xfffe,%sr
m68k_0238a8_end:
.org 0x238AC
m68k_0238ac:
        rts
m68k_0238ac_end:
.org 0x238AE
m68k_0238ae:
        lea.l 0xc800:w,%a0
m68k_0238ae_end:
.org 0x238B2
m68k_0238b2:
        move.w %d7,%d0
m68k_0238b2_end:
.org 0x238B4
m68k_0238b4:
        lsl.w #0x2,%d0
m68k_0238b4_end:
.org 0x238B6
m68k_0238b6:
        move.l (%a0, %d0.w),%d1
m68k_0238b6_end:
.org 0x238BA
m68k_0238ba:
        cmpi.l #0xc8,%d1
m68k_0238ba_end:
.org 0x238C0
m68k_0238c0:
        bls.w (. + 38)
m68k_0238c0_end:
.org 0x238C4
m68k_0238c4:
        cmpi.l #0x1f4,%d1
m68k_0238c4_end:
.org 0x238CA
m68k_0238ca:
        bhi.w (. + 88)
m68k_0238ca_end:
.org 0x238CE
m68k_0238ce:
        lea.l 0xb000:w,%a0
m68k_0238ce_end:
.org 0x238D2
m68k_0238d2:
        lsr.w #0x1,%d0
m68k_0238d2_end:
.org 0x238D4
m68k_0238d4:
        move.w (%a0, %d0.w),%d1
m68k_0238d4_end:
.org 0x238D8
m68k_0238d8:
        lsr.w #0x2,%d1
m68k_0238d8_end:
.org 0x238DA
m68k_0238da:
        lea.l 0xb200:w,%a0
m68k_0238da_end:
.org 0x238DE
m68k_0238de:
        cmp.w (%a0, %d0.w),%d1
m68k_0238de_end:
.org 0x238E2
m68k_0238e2:
        bcs.w (. + 64)
m68k_0238e2_end:
.org 0x238E6
m68k_0238e6:
        move.w #0x2,%d2
m68k_0238e6_end:
.org 0x238EA
m68k_0238ea:
        lea.l 0xe640:w,%a0
m68k_0238ea_end:
.org 0x238EE
m68k_0238ee:
        move.w 0xf68c:w,%d0
m68k_0238ee_end:
.org 0x238F2
m68k_0238f2:
        lsl.w #0x1,%d0
m68k_0238f2_end:
.org 0x238F4
m68k_0238f4:
        cmp.w (%a0, %d0.w),%d7
m68k_0238f4_end:
.org 0x238F8
m68k_0238f8:
        bne.w (. + 20)
m68k_0238f8_end:
.org 0x238FC
m68k_0238fc:
        move.w #0x4,%d2
m68k_0238fc_end:
.org 0x23900
m68k_023900:
        bsr.w (. + 244)
m68k_023900_end:
.org 0x23904
m68k_023904:
        bcs.w (. + 8)
m68k_023904_end:
.org 0x23908
m68k_023908:
        bra.w (. + 136)
m68k_023908_end:
.org 0x2390C
m68k_02390c:
        jsr 0x83d4:l
m68k_02390c_end:
.org 0x23912
m68k_023912:
        andi.l #0xffff,%d0
m68k_023912_end:
.org 0x23918
m68k_023918:
        lsl.l #0x3,%d0
m68k_023918_end:
.org 0x2391A
m68k_02391a:
        swap %d0
m68k_02391a_end:
.org 0x2391C
m68k_02391c:
        cmp.w %d2,%d0
m68k_02391c_end:
.org 0x2391E
m68k_02391e:
        bcs.w (. + 122)
m68k_02391e_end:
.org 0x23922
m68k_023922:
        bsr.w (. + -4716)
m68k_023922_end:
.org 0x23926
m68k_023926:
        cmpi.w #0x3,%d0
m68k_023926_end:
.org 0x2392A
m68k_02392a:
        bcs.w (. + 34)
m68k_02392a_end:
.org 0x2392E
m68k_02392e:
        tst.l 0xf69e:w
m68k_02392e_end:
.org 0x23932
m68k_023932:
        bne.w (. + 26)
m68k_023932_end:
.org 0x23936
m68k_023936:
        move.l 0xf76c:w,%d2
m68k_023936_end:
.org 0x2393A
m68k_02393a:
        divu.w #0x6,%d2
m68k_02393a_end:
.org 0x2393E
m68k_02393e:
        andi.l #0xffff,%d2
m68k_02393e_end:
.org 0x23944
m68k_023944:
        cmp.l 0xf6a2:w,%d2
m68k_023944_end:
.org 0x23948
m68k_023948:
        bls.w (. + 34)
m68k_023948_end:
.org 0x2394C
m68k_02394c:
        bsr.w (. + 138)
m68k_02394c_end:
.org 0x23950
m68k_023950:
        cmp.w %d0,%d2
m68k_023950_end:
.org 0x23952
m68k_023952:
        bhi.w (. + 62)
m68k_023952_end:
.org 0x23956
m68k_023956:
        lsl.l #0x1,%d3
m68k_023956_end:
.org 0x23958
m68k_023958:
        cmp.l %d1,%d3
m68k_023958_end:
.org 0x2395A
m68k_02395a:
        bhi.w (. + 54)
m68k_02395a_end:
.org 0x2395E
m68k_02395e:
        move.l 0xf76c:w,%d0
m68k_02395e_end:
.org 0x23962
m68k_023962:
        cmp.l 0xf6a2:w,%d0
m68k_023962_end:
.org 0x23966
m68k_023966:
        bcs.w (. + 42)
m68k_023966_end:
.org 0x2396A
m68k_02396a:
        move.w #0x2,%d2
m68k_02396a_end:
.org 0x2396E
m68k_02396e:
        bsr.w (. + 134)
m68k_02396e_end:
.org 0x23972
m68k_023972:
        bcs.w (. + 8)
m68k_023972_end:
.org 0x23976
m68k_023976:
        bra.w (. + 26)
m68k_023976_end:
.org 0x2397A
m68k_02397a:
        jsr 0x83d4:l
m68k_02397a_end:
.org 0x23980
m68k_023980:
        andi.l #0xffff,%d0
m68k_023980_end:
.org 0x23986
m68k_023986:
        lsl.l #0x3,%d0
m68k_023986_end:
.org 0x23988
m68k_023988:
        swap %d0
m68k_023988_end:
.org 0x2398A
m68k_02398a:
        cmp.w %d2,%d0
m68k_02398a_end:
.org 0x2398C
m68k_02398c:
        bcs.w (. + 12)
m68k_02398c_end:
.org 0x23990
m68k_023990:
        andi.w #0xfffe,%sr
m68k_023990_end:
.org 0x23994
m68k_023994:
        bra.w (. + 64)
m68k_023994_end:
.org 0x23998
m68k_023998:
        move.w %d7,0xf3a6:w
m68k_023998_end:
.org 0x2399C
m68k_02399c:
        move.w %d7,-(%a7)
m68k_02399c_end:
.org 0x2399E
m68k_02399e:
        jsr 0x17c8a:l
m68k_02399e_end:
.org 0x239A4
m68k_0239a4:
        move.w (%a7)+,%d7
m68k_0239a4_end:
.org 0x239A6
m68k_0239a6:
        tst.w 0xf6e8:w
m68k_0239a6_end:
.org 0x239AA
m68k_0239aa:
        bmi.b (. + -26)
m68k_0239aa_end:
.org 0x239AC
m68k_0239ac:
        jsr 0x17f30:l
m68k_0239ac_end:
.org 0x239B2
m68k_0239b2:
        move.w 0xf3a6:w,0xf3d2:w
m68k_0239b2_end:
.org 0x239B8
m68k_0239b8:
        move.w #0x12e,0xf740:w
m68k_0239b8_end:
.org 0x239BE
m68k_0239be:
        bchg.b #0x1,0xf6d7:w
m68k_0239be_end:
.org 0x239C4
m68k_0239c4:
        jsr 0x260e4:l
m68k_0239c4_end:
.org 0x239CA
m68k_0239ca:
        bchg.b #0x1,0xf6d7:w
m68k_0239ca_end:
.org 0x239D0
m68k_0239d0:
        ori.w #0x1,%sr
m68k_0239d0_end:
.org 0x239D4
m68k_0239d4:
        rts
m68k_0239d4_end:
.org 0x239D6
m68k_0239d6:
        lea.l 0xa550:w,%a0
m68k_0239d6_end:
.org 0x239DA
m68k_0239da:
        lea.l 0xc800:w,%a1
m68k_0239da_end:
.org 0x239DE
m68k_0239de:
        clr.w %d2
m68k_0239de_end:
.org 0x239E0
m68k_0239e0:
        moveq #0,%d3
m68k_0239e0_end:
.org 0x239E2
m68k_0239e2:
        move.w (%a0)+,%d5
m68k_0239e2_end:
.org 0x239E4
m68k_0239e4:
        bmi.w (. + 14)
m68k_0239e4_end:
.org 0x239E8
m68k_0239e8:
        addq.w #0x2,%d2
m68k_0239e8_end:
.org 0x239EA
m68k_0239ea:
        lsl.w #0x2,%d5
m68k_0239ea_end:
.org 0x239EC
m68k_0239ec:
        add.l (%a1, %d5.w),%d3
m68k_0239ec_end:
.org 0x239F0
m68k_0239f0:
        bra.b (. + -14)
m68k_0239f0_end:
.org 0x239F2
m68k_0239f2:
        rts
m68k_0239f2_end:
.org 0x239F4
m68k_0239f4:
        move.w #0x27,%d4
m68k_0239f4_end:
.org 0x239F8
m68k_0239f8:
        move.w 0xf68c:w,%d0
m68k_0239f8_end:
.org 0x239FC
m68k_0239fc:
        lea.l 0xf428:w,%a0
m68k_0239fc_end:
.org 0x23A00
m68k_023a00:
        cmp.b (%a0, %d4.w),%d0
m68k_023a00_end:
.org 0x23A04
m68k_023a04:
        bne.w (. + 12)
m68k_023a04_end:
.org 0x23A08
m68k_023a08:
        ori.w #0x1,%sr
m68k_023a08_end:
.org 0x23A0C
m68k_023a0c:
        bra.w (. + 12)
m68k_023a0c_end:
.org 0x23A10
m68k_023a10:
        dbra %d4,(. + -16)
m68k_023a10_end:
.org 0x23A14
m68k_023a14:
        andi.w #0xfffe,%sr
m68k_023a14_end:
.org 0x23A18
m68k_023a18:
        rts
m68k_023a18_end:
.org 0x23A1A
m68k_023a1a:
        move.l 0xf6a2:w,%d0
m68k_023a1a_end:
.org 0x23A1E
m68k_023a1e:
        cmp.l 0xf76c:w,%d0
m68k_023a1e_end:
.org 0x23A22
m68k_023a22:
        bcs.w (. + 20)
m68k_023a22_end:
.org 0x23A26
m68k_023a26:
        tst.w 0xa552:w
m68k_023a26_end:
.org 0x23A2A
m68k_023a2a:
        bpl.w (. + 12)
m68k_023a2a_end:
.org 0x23A2E
m68k_023a2e:
        ori.w #0x1,%sr
m68k_023a2e_end:
.org 0x23A32
m68k_023a32:
        bra.w (. + 8)
m68k_023a32_end:
.org 0x23A36
m68k_023a36:
        andi.w #0xfffe,%sr
m68k_023a36_end:
.org 0x23A3A
m68k_023a3a:
        rts
m68k_023a3a_end:
.org 0x23A3C
m68k_023a3c:
        move.l 0xf6a2:w,%d0
m68k_023a3c_end:
.org 0x23A40
m68k_023a40:
        cmp.l 0xf76c:w,%d0
m68k_023a40_end:
.org 0x23A44
m68k_023a44:
        bcs.w (. + 36)
m68k_023a44_end:
.org 0x23A48
m68k_023a48:
        tst.w 0xa5a6:w
m68k_023a48_end:
.org 0x23A4C
m68k_023a4c:
        bmi.w (. + 20)
m68k_023a4c_end:
.org 0x23A50
m68k_023a50:
        tst.w 0xa5a8:w
m68k_023a50_end:
.org 0x23A54
m68k_023a54:
        bmi.w (. + 12)
m68k_023a54_end:
.org 0x23A58
m68k_023a58:
        tst.w 0xa5aa:w
m68k_023a58_end:
.org 0x23A5C
m68k_023a5c:
        bpl.w (. + 12)
m68k_023a5c_end:
.org 0x23A60
m68k_023a60:
        ori.w #0x1,%sr
m68k_023a60_end:
.org 0x23A64
m68k_023a64:
        bra.w (. + 8)
m68k_023a64_end:
.org 0x23A68
m68k_023a68:
        andi.w #0xfffe,%sr
m68k_023a68_end:
.org 0x23A6C
m68k_023a6c:
        rts
m68k_023a6c_end:
.org 0x23A6E
m68k_023a6e:
        bsr.w (. + 556)
m68k_023a6e_end:
.org 0x23A72
m68k_023a72:
        bcs.w (. + 3492)
m68k_023a72_end:
.org 0x23A76
m68k_023a76:
        bsr.w (. + -832)
m68k_023a76_end:
.org 0x23A7A
m68k_023a7a:
        bcs.w (. + 24)
m68k_023a7a_end:
.org 0x23A7E
m68k_023a7e:
        bsr.w (. + -4904)
m68k_023a7e_end:
.org 0x23A82
m68k_023a82:
        bcs.w (. + 16)
m68k_023a82_end:
.org 0x23A86
m68k_023a86:
        bsr.w (. + 440)
m68k_023a86_end:
.org 0x23A8A
m68k_023a8a:
        bcs.w (. + 8)
m68k_023a8a_end:
.org 0x23A8E
m68k_023a8e:
        bsr.w (. + 6)
m68k_023a8e_end:
.org 0x23A92
m68k_023a92:
        rts
m68k_023a92_end:
.org 0x23A94
m68k_023a94:
        lea.l 0xa654:w,%a0
m68k_023a94_end:
.org 0x23A98
m68k_023a98:
        tst.b (%a0, %d7.w)
m68k_023a98_end:
.org 0x23A9C
m68k_023a9c:
        bne.w (. + 106)
m68k_023a9c_end:
.org 0x23AA0
m68k_023aa0:
        lea.l 0xff3cc2:l,%a0
m68k_023aa0_end:
.org 0x23AA6
m68k_023aa6:
        tst.b (%a0, %d7.w)
m68k_023aa6_end:
.org 0x23AAA
m68k_023aaa:
        bne.w (. + 92)
m68k_023aaa_end:
.org 0x23AAE
m68k_023aae:
        lea.l 0xff3dc2:l,%a1
m68k_023aae_end:
.org 0x23AB4
m68k_023ab4:
        tst.b (%a1, %d7.w)
m68k_023ab4_end:
.org 0x23AB8
m68k_023ab8:
        bne.w (. + 78)
m68k_023ab8_end:
.org 0x23ABC
m68k_023abc:
        lea.l 0xa150:w,%a0
m68k_023abc_end:
.org 0x23AC0
m68k_023ac0:
        move.w %d7,%d0
m68k_023ac0_end:
.org 0x23AC2
m68k_023ac2:
        lsl.w #0x2,%d0
m68k_023ac2_end:
.org 0x23AC4
m68k_023ac4:
        move.w 0x2(%a0, %d0.w),%d1
m68k_023ac4_end:
.org 0x23AC8
m68k_023ac8:
        move.w (%a0, %d0.w),%d0
m68k_023ac8_end:
.org 0x23ACC
m68k_023acc:
        bsr.w (. + 60)
m68k_023acc_end:
.org 0x23AD0
m68k_023ad0:
        bcs.w (. + 12)
m68k_023ad0_end:
.org 0x23AD4
m68k_023ad4:
        bsr.w (. + 210)
m68k_023ad4_end:
.org 0x23AD8
m68k_023ad8:
        bra.w (. + 8)
m68k_023ad8_end:
.org 0x23ADC
m68k_023adc:
        bsr.w (. + 280)
m68k_023adc_end:
.org 0x23AE0
m68k_023ae0:
        lea.l 0xff2c00:l,%a0
m68k_023ae0_end:
.org 0x23AE6
m68k_023ae6:
        move.w %d7,%d1
m68k_023ae6_end:
.org 0x23AE8
m68k_023ae8:
        lsl.w #0x2,%d1
m68k_023ae8_end:
.org 0x23AEA
m68k_023aea:
        lsr.w #0x7,%d2
m68k_023aea_end:
.org 0x23AEC
m68k_023aec:
        move.w %d2,(%a0, %d1.w)
m68k_023aec_end:
.org 0x23AF0
m68k_023af0:
        lsr.w #0x7,%d4
m68k_023af0_end:
.org 0x23AF2
m68k_023af2:
        move.w %d4,0x2(%a0, %d1.w)
m68k_023af2_end:
.org 0x23AF6
m68k_023af6:
        lea.l 0xae28:w,%a0
m68k_023af6_end:
.org 0x23AFA
m68k_023afa:
        move.b #0x1,(%a0, %d7.w)
m68k_023afa_end:
.org 0x23B00
m68k_023b00:
        jsr 0x1dcaa:l
m68k_023b00_end:
.org 0x23B06
m68k_023b06:
        rts
m68k_023b06_end:
.org 0x23B08
m68k_023b08:
        move.w 0xf68a:w,%d6
m68k_023b08_end:
.org 0x23B0C
m68k_023b0c:
        lea.l 0xae2f6:l,%a0
m68k_023b0c_end:
.org 0x23B12
m68k_023b12:
        lsl.w #0x2,%d6
m68k_023b12_end:
.org 0x23B14
m68k_023b14:
        cmpi.w #0x5c,%d6
m68k_023b14_end:
.org 0x23B18
m68k_023b18:
        beq.w (. + 80)
m68k_023b18_end:
.org 0x23B1C
m68k_023b1c:
        move.w (%a0, %d6.w),%d2
m68k_023b1c_end:
.org 0x23B20
m68k_023b20:
        move.w %d2,%d3
m68k_023b20_end:
.org 0x23B22
m68k_023b22:
        subi.w #0x1000,%d2
m68k_023b22_end:
.org 0x23B26
m68k_023b26:
        bcs.w (. + 12)
m68k_023b26_end:
.org 0x23B2A
m68k_023b2a:
        cmpi.w #0xc00,%d2
m68k_023b2a_end:
.org 0x23B2E
m68k_023b2e:
        bcc.w (. + 8)
m68k_023b2e_end:
.org 0x23B32
m68k_023b32:
        move.w #0xc00,%d2
m68k_023b32_end:
.org 0x23B36
m68k_023b36:
        addi.w #0x1000,%d3
m68k_023b36_end:
.org 0x23B3A
m68k_023b3a:
        bcs.w (. + 12)
m68k_023b3a_end:
.org 0x23B3E
m68k_023b3e:
        cmpi.w #0x6400,%d3
m68k_023b3e_end:
.org 0x23B42
m68k_023b42:
        bls.w (. + 8)
m68k_023b42_end:
.org 0x23B46
m68k_023b46:
        move.w #0x6400,%d3
m68k_023b46_end:
.org 0x23B4A
m68k_023b4a:
        move.w 0x2(%a0, %d6.w),%d4
m68k_023b4a_end:
.org 0x23B4E
m68k_023b4e:
        move.w %d4,%d5
m68k_023b4e_end:
.org 0x23B50
m68k_023b50:
        cmpi.w #0x5000,%d4
m68k_023b50_end:
.org 0x23B54
m68k_023b54:
        bcs.w (. + 12)
m68k_023b54_end:
.org 0x23B58
m68k_023b58:
        subi.w #0x3800,%d4
m68k_023b58_end:
.org 0x23B5C
m68k_023b5c:
        bra.w (. + 36)
m68k_023b5c_end:
.org 0x23B60
m68k_023b60:
        addi.w #0x3800,%d5
m68k_023b60_end:
.org 0x23B64
m68k_023b64:
        bra.w (. + 28)
m68k_023b64_end:
.org 0x23B68
m68k_023b68:
        move.w (%a0, %d6.w),%d2
m68k_023b68_end:
.org 0x23B6C
m68k_023b6c:
        move.w %d2,%d3
m68k_023b6c_end:
.org 0x23B6E
m68k_023b6e:
        subi.w #0x3400,%d3
m68k_023b6e_end:
.org 0x23B72
m68k_023b72:
        move.w 0x2(%a0, %d6.w),%d4
m68k_023b72_end:
.org 0x23B76
m68k_023b76:
        move.w %d4,%d5
m68k_023b76_end:
.org 0x23B78
m68k_023b78:
        subi.w #0xc00,%d4
m68k_023b78_end:
.org 0x23B7C
m68k_023b7c:
        addi.w #0xc00,%d5
m68k_023b7c_end:
.org 0x23B80
m68k_023b80:
        cmp.w %d2,%d0
m68k_023b80_end:
.org 0x23B82
m68k_023b82:
        bcs.w (. + 30)
m68k_023b82_end:
.org 0x23B86
m68k_023b86:
        cmp.w %d3,%d0
m68k_023b86_end:
.org 0x23B88
m68k_023b88:
        bhi.w (. + 24)
m68k_023b88_end:
.org 0x23B8C
m68k_023b8c:
        cmp.w %d4,%d1
m68k_023b8c_end:
.org 0x23B8E
m68k_023b8e:
        bcs.w (. + 18)
m68k_023b8e_end:
.org 0x23B92
m68k_023b92:
        cmp.w %d5,%d1
m68k_023b92_end:
.org 0x23B94
m68k_023b94:
        bhi.w (. + 12)
m68k_023b94_end:
.org 0x23B98
m68k_023b98:
        ori.w #0x1,%sr
m68k_023b98_end:
.org 0x23B9C
m68k_023b9c:
        bra.w (. + 8)
m68k_023b9c_end:
.org 0x23BA0
m68k_023ba0:
        andi.w #0xfffe,%sr
m68k_023ba0_end:
.org 0x23BA4
m68k_023ba4:
        rts
m68k_023ba4_end:
.org 0x23BA6
m68k_023ba6:
        sub.w %d2,%d3
m68k_023ba6_end:
.org 0x23BA8
m68k_023ba8:
        jsr 0x83d4:l
m68k_023ba8_end:
.org 0x23BAE
m68k_023bae:
        andi.l #0xffff,%d0
m68k_023bae_end:
.org 0x23BB4
m68k_023bb4:
        mulu.w %d3,%d0
m68k_023bb4_end:
.org 0x23BB6
m68k_023bb6:
        swap %d0
m68k_023bb6_end:
.org 0x23BB8
m68k_023bb8:
        add.w %d0,%d2
m68k_023bb8_end:
.org 0x23BBA
m68k_023bba:
        sub.w %d4,%d5
m68k_023bba_end:
.org 0x23BBC
m68k_023bbc:
        subi.w #0xc00,%d5
m68k_023bbc_end:
.org 0x23BC0
m68k_023bc0:
        jsr 0x83d4:l
m68k_023bc0_end:
.org 0x23BC6
m68k_023bc6:
        andi.l #0xffff,%d0
m68k_023bc6_end:
.org 0x23BCC
m68k_023bcc:
        mulu.w %d5,%d0
m68k_023bcc_end:
.org 0x23BCE
m68k_023bce:
        swap %d0
m68k_023bce_end:
.org 0x23BD0
m68k_023bd0:
        lea.l 0xae2f6:l,%a0
m68k_023bd0_end:
.org 0x23BD6
m68k_023bd6:
        move.w 0xf68a:w,%d1
m68k_023bd6_end:
.org 0x23BDA
m68k_023bda:
        lsl.w #0x2,%d1
m68k_023bda_end:
.org 0x23BDC
m68k_023bdc:
        cmpi.w #0x5000,0x2(%a0, %d1.w)
m68k_023bdc_end:
.org 0x23BE2
m68k_023be2:
        bcs.w (. + 10)
m68k_023be2_end:
.org 0x23BE6
m68k_023be6:
        add.w %d0,%d4
m68k_023be6_end:
.org 0x23BE8
m68k_023be8:
        bra.w (. + 10)
m68k_023be8_end:
.org 0x23BEC
m68k_023bec:
        add.w %d0,%d4
m68k_023bec_end:
.org 0x23BEE
m68k_023bee:
        addi.w #0xc00,%d4
m68k_023bee_end:
.org 0x23BF2
m68k_023bf2:
        rts
m68k_023bf2_end:
.org 0x23BF4
m68k_023bf4:
        lea.l 0xae2f6:l,%a0
m68k_023bf4_end:
.org 0x23BFA
m68k_023bfa:
        move.w 0xf68a:w,%d0
m68k_023bfa_end:
.org 0x23BFE
m68k_023bfe:
        lsl.w #0x2,%d0
m68k_023bfe_end:
.org 0x23C00
m68k_023c00:
        cmpi.w #0x5c,%d0
m68k_023c00_end:
.org 0x23C04
m68k_023c04:
        beq.w (. + 40)
m68k_023c04_end:
.org 0x23C08
m68k_023c08:
        move.w (%a0, %d0.w),%d2
m68k_023c08_end:
.org 0x23C0C
m68k_023c0c:
        subi.w #0x400,%d2
m68k_023c0c_end:
.org 0x23C10
m68k_023c10:
        move.w 0x2(%a0, %d0.w),%d4
m68k_023c10_end:
.org 0x23C14
m68k_023c14:
        cmpi.w #0x5000,%d4
m68k_023c14_end:
.org 0x23C18
m68k_023c18:
        bcs.w (. + 12)
m68k_023c18_end:
.org 0x23C1C
m68k_023c1c:
        subi.w #0xf80,%d4
m68k_023c1c_end:
.org 0x23C20
m68k_023c20:
        bra.w (. + 28)
m68k_023c20_end:
.org 0x23C24
m68k_023c24:
        addi.w #0xf80,%d4
m68k_023c24_end:
.org 0x23C28
m68k_023c28:
        bra.w (. + 20)
m68k_023c28_end:
.org 0x23C2C
m68k_023c2c:
        move.w (%a0, %d0.w),%d2
m68k_023c2c_end:
.org 0x23C30
m68k_023c30:
        subi.w #0x1000,%d2
m68k_023c30_end:
.org 0x23C34
m68k_023c34:
        move.w 0x2(%a0, %d0.w),%d4
m68k_023c34_end:
.org 0x23C38
m68k_023c38:
        subi.w #0x480,%d4
m68k_023c38_end:
.org 0x23C3C
m68k_023c3c:
        rts
m68k_023c3c_end:
.org 0x23C3E
m68k_023c3e:
        lea.l 0xb600:w,%a0
m68k_023c3e_end:
.org 0x23C42
m68k_023c42:
        move.w %d7,%d0
m68k_023c42_end:
.org 0x23C44
m68k_023c44:
        lsl.w #0x1,%d0
m68k_023c44_end:
.org 0x23C46
m68k_023c46:
        clr.w %d2
m68k_023c46_end:
.org 0x23C48
m68k_023c48:
        move.w (%a0, %d0.w),%d1
m68k_023c48_end:
.org 0x23C4C
m68k_023c4c:
        cmpi.w #0x32,%d1
m68k_023c4c_end:
.org 0x23C50
m68k_023c50:
        bcs.w (. + 26)
m68k_023c50_end:
.org 0x23C54
m68k_023c54:
        addq.w #0x1,%d2
m68k_023c54_end:
.org 0x23C56
m68k_023c56:
        cmpi.w #0x46,%d1
m68k_023c56_end:
.org 0x23C5A
m68k_023c5a:
        bcs.w (. + 16)
m68k_023c5a_end:
.org 0x23C5E
m68k_023c5e:
        addq.w #0x1,%d2
m68k_023c5e_end:
.org 0x23C60
m68k_023c60:
        cmpi.w #0x5a,%d1
m68k_023c60_end:
.org 0x23C64
m68k_023c64:
        bcs.w (. + 6)
m68k_023c64_end:
.org 0x23C68
m68k_023c68:
        addq.w #0x1,%d2
m68k_023c68_end:
.org 0x23C6A
m68k_023c6a:
        jsr 0x83d4:l
m68k_023c6a_end:
.org 0x23C70
m68k_023c70:
        andi.l #0xffff,%d0
m68k_023c70_end:
.org 0x23C76
m68k_023c76:
        lsl.l #0x2,%d0
m68k_023c76_end:
.org 0x23C78
m68k_023c78:
        swap %d0
m68k_023c78_end:
.org 0x23C7A
m68k_023c7a:
        cmp.w %d2,%d0
m68k_023c7a_end:
.org 0x23C7C
m68k_023c7c:
        bcc.w (. + 24)
m68k_023c7c_end:
.org 0x23C80
m68k_023c80:
        bsr.w (. + -1966)
m68k_023c80_end:
.org 0x23C84
m68k_023c84:
        tst.w 0xd300:w
m68k_023c84_end:
.org 0x23C88
m68k_023c88:
        bmi.w (. + 12)
m68k_023c88_end:
.org 0x23C8C
m68k_023c8c:
        bsr.w (. + 10452)
m68k_023c8c_end:
.org 0x23C90
m68k_023c90:
        bra.w (. + 8)
m68k_023c90_end:
.org 0x23C94
m68k_023c94:
        andi.w #0xfffe,%sr
m68k_023c94_end:
.org 0x23C98
m68k_023c98:
        rts
m68k_023c98_end:
.org 0x23C9A
m68k_023c9a:
        move.l 0xf6a2:w,%d0
m68k_023c9a_end:
.org 0x23C9E
m68k_023c9e:
        cmp.l 0xf69e:w,%d0
m68k_023c9e_end:
.org 0x23CA2
m68k_023ca2:
        bcc.w (. + 20)
m68k_023ca2_end:
.org 0x23CA6
m68k_023ca6:
        cmp.l 0xf76c:w,%d0
m68k_023ca6_end:
.org 0x23CAA
m68k_023caa:
        bcc.w (. + 12)
m68k_023caa_end:
.org 0x23CAE
m68k_023cae:
        ori.w #0x1,%sr
m68k_023cae_end:
.org 0x23CB2
m68k_023cb2:
        bra.w (. + 8)
m68k_023cb2_end:
.org 0x23CB6
m68k_023cb6:
        andi.w #0xfffe,%sr
m68k_023cb6_end:
.org 0x23CBA
m68k_023cba:
        rts
m68k_023cba_end:
.org 0x23CBC
m68k_023cbc:
        bsr.b (. + -34)
m68k_023cbc_end:
.org 0x23CBE
m68k_023cbe:
        bcs.w (. + 2904)
m68k_023cbe_end:
.org 0x23CC2
m68k_023cc2:
        bsr.w (. + -1420)
m68k_023cc2_end:
.org 0x23CC6
m68k_023cc6:
        bcs.w (. + 24)
m68k_023cc6_end:
.org 0x23CCA
m68k_023cca:
        bsr.w (. + -5492)
m68k_023cca_end:
.org 0x23CCE
m68k_023cce:
        bcs.w (. + 16)
m68k_023cce_end:
.org 0x23CD2
m68k_023cd2:
        bsr.w (. + -148)
m68k_023cd2_end:
.org 0x23CD6
m68k_023cd6:
        bcs.w (. + 8)
m68k_023cd6_end:
.org 0x23CDA
m68k_023cda:
        bsr.w (. + 6)
m68k_023cda_end:
.org 0x23CDE
m68k_023cde:
        rts
m68k_023cde_end:
.org 0x23CE0
m68k_023ce0:
        lea.l 0xa654:w,%a0
m68k_023ce0_end:
.org 0x23CE4
m68k_023ce4:
        tst.b (%a0, %d7.w)
m68k_023ce4_end:
.org 0x23CE8
m68k_023ce8:
        bne.w (. + 106)
m68k_023ce8_end:
.org 0x23CEC
m68k_023cec:
        lea.l 0xff3cc2:l,%a0
m68k_023cec_end:
.org 0x23CF2
m68k_023cf2:
        tst.b (%a0, %d7.w)
m68k_023cf2_end:
.org 0x23CF6
m68k_023cf6:
        bne.w (. + 92)
m68k_023cf6_end:
.org 0x23CFA
m68k_023cfa:
        lea.l 0xff3dc2:l,%a1
m68k_023cfa_end:
.org 0x23D00
m68k_023d00:
        tst.b (%a1, %d7.w)
m68k_023d00_end:
.org 0x23D04
m68k_023d04:
        bne.w (. + 78)
m68k_023d04_end:
.org 0x23D08
m68k_023d08:
        lea.l 0xa150:w,%a0
m68k_023d08_end:
.org 0x23D0C
m68k_023d0c:
        move.w %d7,%d0
m68k_023d0c_end:
.org 0x23D0E
m68k_023d0e:
        lsl.w #0x2,%d0
m68k_023d0e_end:
.org 0x23D10
m68k_023d10:
        move.w 0x2(%a0, %d0.w),%d1
m68k_023d10_end:
.org 0x23D14
m68k_023d14:
        move.w (%a0, %d0.w),%d0
m68k_023d14_end:
.org 0x23D18
m68k_023d18:
        bsr.w (. + -528)
m68k_023d18_end:
.org 0x23D1C
m68k_023d1c:
        bcs.w (. + 12)
m68k_023d1c_end:
.org 0x23D20
m68k_023d20:
        bsr.w (. + -378)
m68k_023d20_end:
.org 0x23D24
m68k_023d24:
        bra.w (. + 8)
m68k_023d24_end:
.org 0x23D28
m68k_023d28:
        bsr.w (. + 44)
m68k_023d28_end:
.org 0x23D2C
m68k_023d2c:
        lea.l 0xff2c00:l,%a0
m68k_023d2c_end:
.org 0x23D32
m68k_023d32:
        move.w %d7,%d1
m68k_023d32_end:
.org 0x23D34
m68k_023d34:
        lsl.w #0x2,%d1
m68k_023d34_end:
.org 0x23D36
m68k_023d36:
        lsr.w #0x7,%d2
m68k_023d36_end:
.org 0x23D38
m68k_023d38:
        move.w %d2,(%a0, %d1.w)
m68k_023d38_end:
.org 0x23D3C
m68k_023d3c:
        lsr.w #0x7,%d4
m68k_023d3c_end:
.org 0x23D3E
m68k_023d3e:
        move.w %d4,0x2(%a0, %d1.w)
m68k_023d3e_end:
.org 0x23D42
m68k_023d42:
        lea.l 0xae28:w,%a0
m68k_023d42_end:
.org 0x23D46
m68k_023d46:
        move.b #0x1,(%a0, %d7.w)
m68k_023d46_end:
.org 0x23D4C
m68k_023d4c:
        jsr 0x1dcaa:l
m68k_023d4c_end:
.org 0x23D52
m68k_023d52:
        rts
m68k_023d52_end:
.org 0x23D54
m68k_023d54:
        lea.l 0xae2f6:l,%a0
m68k_023d54_end:
.org 0x23D5A
m68k_023d5a:
        move.w 0xf68a:w,%d0
m68k_023d5a_end:
.org 0x23D5E
m68k_023d5e:
        lsl.w #0x2,%d0
m68k_023d5e_end:
.org 0x23D60
m68k_023d60:
        cmpi.w #0x5c,%d0
m68k_023d60_end:
.org 0x23D64
m68k_023d64:
        beq.w (. + 40)
m68k_023d64_end:
.org 0x23D68
m68k_023d68:
        move.w (%a0, %d0.w),%d2
m68k_023d68_end:
.org 0x23D6C
m68k_023d6c:
        addi.w #0x400,%d2
m68k_023d6c_end:
.org 0x23D70
m68k_023d70:
        move.w 0x2(%a0, %d0.w),%d4
m68k_023d70_end:
.org 0x23D74
m68k_023d74:
        cmpi.w #0x5000,%d4
m68k_023d74_end:
.org 0x23D78
m68k_023d78:
        bcs.w (. + 12)
m68k_023d78_end:
.org 0x23D7C
m68k_023d7c:
        subi.w #0xf80,%d4
m68k_023d7c_end:
.org 0x23D80
m68k_023d80:
        bra.w (. + 28)
m68k_023d80_end:
.org 0x23D84
m68k_023d84:
        addi.w #0xf80,%d4
m68k_023d84_end:
.org 0x23D88
m68k_023d88:
        bra.w (. + 20)
m68k_023d88_end:
.org 0x23D8C
m68k_023d8c:
        move.w (%a0, %d0.w),%d2
m68k_023d8c_end:
.org 0x23D90
m68k_023d90:
        subi.w #0x1000,%d2
m68k_023d90_end:
.org 0x23D94
m68k_023d94:
        move.w 0x2(%a0, %d0.w),%d4
m68k_023d94_end:
.org 0x23D98
m68k_023d98:
        addi.w #0x480,%d4
m68k_023d98_end:
.org 0x23D9C
m68k_023d9c:
        rts
m68k_023d9c_end:
.org 0x23D9E
m68k_023d9e:
        bsr.w (. + -260)
m68k_023d9e_end:
.org 0x23DA2
m68k_023da2:
        bcs.w (. + 2676)
m68k_023da2_end:
.org 0x23DA6
m68k_023da6:
        bsr.w (. + -1648)
m68k_023da6_end:
.org 0x23DAA
m68k_023daa:
        bcs.w (. + 24)
m68k_023daa_end:
.org 0x23DAE
m68k_023dae:
        bsr.w (. + -5720)
m68k_023dae_end:
.org 0x23DB2
m68k_023db2:
        bcs.w (. + 16)
m68k_023db2_end:
.org 0x23DB6
m68k_023db6:
        bsr.w (. + -376)
m68k_023db6_end:
.org 0x23DBA
m68k_023dba:
        bcs.w (. + 8)
m68k_023dba_end:
.org 0x23DBE
m68k_023dbe:
        bsr.w (. + 6)
m68k_023dbe_end:
.org 0x23DC2
m68k_023dc2:
        rts
m68k_023dc2_end:
.org 0x23DC4
m68k_023dc4:
        lea.l 0xa654:w,%a0
m68k_023dc4_end:
.org 0x23DC8
m68k_023dc8:
        tst.b (%a0, %d7.w)
m68k_023dc8_end:
.org 0x23DCC
m68k_023dcc:
        bne.w (. + 154)
m68k_023dcc_end:
.org 0x23DD0
m68k_023dd0:
        lea.l 0xff3cc2:l,%a0
m68k_023dd0_end:
.org 0x23DD6
m68k_023dd6:
        tst.b (%a0, %d7.w)
m68k_023dd6_end:
.org 0x23DDA
m68k_023dda:
        bne.w (. + 140)
m68k_023dda_end:
.org 0x23DDE
m68k_023dde:
        lea.l 0xff3dc2:l,%a1
m68k_023dde_end:
.org 0x23DE4
m68k_023de4:
        tst.b (%a1, %d7.w)
m68k_023de4_end:
.org 0x23DE8
m68k_023de8:
        bne.w (. + 126)
m68k_023de8_end:
.org 0x23DEC
m68k_023dec:
        lea.l 0xa150:w,%a0
m68k_023dec_end:
.org 0x23DF0
m68k_023df0:
        move.w %d7,%d0
m68k_023df0_end:
.org 0x23DF2
m68k_023df2:
        lsl.w #0x2,%d0
m68k_023df2_end:
.org 0x23DF4
m68k_023df4:
        move.w 0x2(%a0, %d0.w),%d1
m68k_023df4_end:
.org 0x23DF8
m68k_023df8:
        move.w (%a0, %d0.w),%d0
m68k_023df8_end:
.org 0x23DFC
m68k_023dfc:
        lea.l 0xae2f6:l,%a0
m68k_023dfc_end:
.org 0x23E02
m68k_023e02:
        move.w 0xf68a:w,%d2
m68k_023e02_end:
.org 0x23E06
m68k_023e06:
        lsl.w #0x2,%d2
m68k_023e06_end:
.org 0x23E08
m68k_023e08:
        cmpi.w #0x5c,%d2
m68k_023e08_end:
.org 0x23E0C
m68k_023e0c:
        beq.w (. + 48)
m68k_023e0c_end:
.org 0x23E10
m68k_023e10:
        cmpi.w #0x4800,(%a0, %d2.w)
m68k_023e10_end:
.org 0x23E16
m68k_023e16:
        bhi.w (. + 22)
m68k_023e16_end:
.org 0x23E1A
m68k_023e1a:
        cmpi.w #0x2800,(%a0, %d2.w)
m68k_023e1a_end:
.org 0x23E20
m68k_023e20:
        bcc.w (. + 20)
m68k_023e20_end:
.org 0x23E24
m68k_023e24:
        bsr.w (. + 68)
m68k_023e24_end:
.org 0x23E28
m68k_023e28:
        bra.w (. + 24)
m68k_023e28_end:
.org 0x23E2C
m68k_023e2c:
        bsr.w (. + 198)
m68k_023e2c_end:
.org 0x23E30
m68k_023e30:
        bra.w (. + 16)
m68k_023e30_end:
.org 0x23E34
m68k_023e34:
        bsr.w (. + 332)
m68k_023e34_end:
.org 0x23E38
m68k_023e38:
        bra.w (. + 8)
m68k_023e38_end:
.org 0x23E3C
m68k_023e3c:
        bsr.w (. + 524)
m68k_023e3c_end:
.org 0x23E40
m68k_023e40:
        lea.l 0xff2c00:l,%a0
m68k_023e40_end:
.org 0x23E46
m68k_023e46:
        move.w %d7,%d1
m68k_023e46_end:
.org 0x23E48
m68k_023e48:
        lsl.w #0x2,%d1
m68k_023e48_end:
.org 0x23E4A
m68k_023e4a:
        lsr.w #0x7,%d3
m68k_023e4a_end:
.org 0x23E4C
m68k_023e4c:
        move.w %d3,(%a0, %d1.w)
m68k_023e4c_end:
.org 0x23E50
m68k_023e50:
        lsr.w #0x7,%d5
m68k_023e50_end:
.org 0x23E52
m68k_023e52:
        move.w %d5,0x2(%a0, %d1.w)
m68k_023e52_end:
.org 0x23E56
m68k_023e56:
        lea.l 0xae28:w,%a0
m68k_023e56_end:
.org 0x23E5A
m68k_023e5a:
        move.b #0x1,(%a0, %d7.w)
m68k_023e5a_end:
.org 0x23E60
m68k_023e60:
        jsr 0x1dcaa:l
m68k_023e60_end:
.org 0x23E66
m68k_023e66:
        rts
m68k_023e66_end:
.org 0x23E68
m68k_023e68:
        bsr.w (. + 18)
m68k_023e68_end:
.org 0x23E6C
m68k_023e6c:
        bcc.w (. + 12)
m68k_023e6c_end:
.org 0x23E70
m68k_023e70:
        addi.w #0xf80,%d3
m68k_023e70_end:
.org 0x23E74
m68k_023e74:
        addi.w #0xc00,%d5
m68k_023e74_end:
.org 0x23E78
m68k_023e78:
        rts
m68k_023e78_end:
.org 0x23E7A
m68k_023e7a:
        move.w (%a0, %d2.w),%d3
m68k_023e7a_end:
.org 0x23E7E
m68k_023e7e:
        move.w %d3,%d4
m68k_023e7e_end:
.org 0x23E80
m68k_023e80:
        addi.w #0x3800,%d4
m68k_023e80_end:
.org 0x23E84
m68k_023e84:
        move.w 0x2(%a0, %d2.w),%d5
m68k_023e84_end:
.org 0x23E88
m68k_023e88:
        move.w %d5,%d6
m68k_023e88_end:
.org 0x23E8A
m68k_023e8a:
        subi.w #0x1000,%d5
m68k_023e8a_end:
.org 0x23E8E
m68k_023e8e:
        cmpi.w #0xc00,%d5
m68k_023e8e_end:
.org 0x23E92
m68k_023e92:
        bcc.w (. + 8)
m68k_023e92_end:
.org 0x23E96
m68k_023e96:
        move.w #0xc00,%d5
m68k_023e96_end:
.org 0x23E9A
m68k_023e9a:
        addi.w #0x1000,%d6
m68k_023e9a_end:
.org 0x23E9E
m68k_023e9e:
        cmpi.w #0x9400,%d6
m68k_023e9e_end:
.org 0x23EA2
m68k_023ea2:
        bls.w (. + 8)
m68k_023ea2_end:
.org 0x23EA6
m68k_023ea6:
        move.w #0x9400,%d6
m68k_023ea6_end:
.org 0x23EAA
m68k_023eaa:
        cmp.w %d4,%d0
m68k_023eaa_end:
.org 0x23EAC
m68k_023eac:
        bhi.w (. + 24)
m68k_023eac_end:
.org 0x23EB0
m68k_023eb0:
        cmp.w %d5,%d1
m68k_023eb0_end:
.org 0x23EB2
m68k_023eb2:
        bcs.w (. + 18)
m68k_023eb2_end:
.org 0x23EB6
m68k_023eb6:
        cmp.w %d6,%d1
m68k_023eb6_end:
.org 0x23EB8
m68k_023eb8:
        bhi.w (. + 12)
m68k_023eb8_end:
.org 0x23EBC
m68k_023ebc:
        ori.w #0x1,%sr
m68k_023ebc_end:
.org 0x23EC0
m68k_023ec0:
        bra.w (. + 48)
m68k_023ec0_end:
.org 0x23EC4
m68k_023ec4:
        jsr 0x83d4:l
m68k_023ec4_end:
.org 0x23ECA
m68k_023eca:
        andi.l #0xffff,%d0
m68k_023eca_end:
.org 0x23ED0
m68k_023ed0:
        mulu.w #0x2000,%d0
m68k_023ed0_end:
.org 0x23ED4
m68k_023ed4:
        swap %d0
m68k_023ed4_end:
.org 0x23ED6
m68k_023ed6:
        add.w %d0,%d3
m68k_023ed6_end:
.org 0x23ED8
m68k_023ed8:
        addi.w #0xc00,%d3
m68k_023ed8_end:
.org 0x23EDC
m68k_023edc:
        sub.w %d5,%d6
m68k_023edc_end:
.org 0x23EDE
m68k_023ede:
        jsr 0x83d4:l
m68k_023ede_end:
.org 0x23EE4
m68k_023ee4:
        andi.l #0xffff,%d0
m68k_023ee4_end:
.org 0x23EEA
m68k_023eea:
        mulu.w %d6,%d0
m68k_023eea_end:
.org 0x23EEC
m68k_023eec:
        swap %d0
m68k_023eec_end:
.org 0x23EEE
m68k_023eee:
        add.w %d0,%d5
m68k_023eee_end:
.org 0x23EF0
m68k_023ef0:
        rts
m68k_023ef0_end:
.org 0x23EF2
m68k_023ef2:
        bsr.w (. + 20)
m68k_023ef2_end:
.org 0x23EF6
m68k_023ef6:
        bcc.w (. + 14)
m68k_023ef6_end:
.org 0x23EFA
m68k_023efa:
        move.w %d4,%d3
m68k_023efa_end:
.org 0x23EFC
m68k_023efc:
        subi.w #0xf80,%d3
m68k_023efc_end:
.org 0x23F00
m68k_023f00:
        addi.w #0xc00,%d5
m68k_023f00_end:
.org 0x23F04
m68k_023f04:
        rts
m68k_023f04_end:
.org 0x23F06
m68k_023f06:
        move.w (%a0, %d2.w),%d3
m68k_023f06_end:
.org 0x23F0A
m68k_023f0a:
        move.w %d3,%d4
m68k_023f0a_end:
.org 0x23F0C
m68k_023f0c:
        subi.w #0x3800,%d3
m68k_023f0c_end:
.org 0x23F10
m68k_023f10:
        move.w 0x2(%a0, %d2.w),%d5
m68k_023f10_end:
.org 0x23F14
m68k_023f14:
        move.w %d5,%d6
m68k_023f14_end:
.org 0x23F16
m68k_023f16:
        subi.w #0x1000,%d5
m68k_023f16_end:
.org 0x23F1A
m68k_023f1a:
        cmpi.w #0xc00,%d5
m68k_023f1a_end:
.org 0x23F1E
m68k_023f1e:
        bcc.w (. + 8)
m68k_023f1e_end:
.org 0x23F22
m68k_023f22:
        move.w #0xc00,%d5
m68k_023f22_end:
.org 0x23F26
m68k_023f26:
        addi.w #0x1000,%d6
m68k_023f26_end:
.org 0x23F2A
m68k_023f2a:
        cmpi.w #0x9400,%d6
m68k_023f2a_end:
.org 0x23F2E
m68k_023f2e:
        bls.w (. + 8)
m68k_023f2e_end:
.org 0x23F32
m68k_023f32:
        move.w #0x9400,%d6
m68k_023f32_end:
.org 0x23F36
m68k_023f36:
        cmp.w %d3,%d0
m68k_023f36_end:
.org 0x23F38
m68k_023f38:
        bcs.w (. + 24)
m68k_023f38_end:
.org 0x23F3C
m68k_023f3c:
        cmp.w %d5,%d1
m68k_023f3c_end:
.org 0x23F3E
m68k_023f3e:
        bcs.w (. + 18)
m68k_023f3e_end:
.org 0x23F42
m68k_023f42:
        cmp.w %d6,%d1
m68k_023f42_end:
.org 0x23F44
m68k_023f44:
        bhi.w (. + 12)
m68k_023f44_end:
.org 0x23F48
m68k_023f48:
        ori.w #0x1,%sr
m68k_023f48_end:
.org 0x23F4C
m68k_023f4c:
        bra.w (. + 50)
m68k_023f4c_end:
.org 0x23F50
m68k_023f50:
        jsr 0x83d4:l
m68k_023f50_end:
.org 0x23F56
m68k_023f56:
        andi.l #0xffff,%d0
m68k_023f56_end:
.org 0x23F5C
m68k_023f5c:
        mulu.w #0x2000,%d0
m68k_023f5c_end:
.org 0x23F60
m68k_023f60:
        swap %d0
m68k_023f60_end:
.org 0x23F62
m68k_023f62:
        move.w %d4,%d3
m68k_023f62_end:
.org 0x23F64
m68k_023f64:
        sub.w %d0,%d3
m68k_023f64_end:
.org 0x23F66
m68k_023f66:
        subi.w #0xc00,%d3
m68k_023f66_end:
.org 0x23F6A
m68k_023f6a:
        sub.w %d5,%d6
m68k_023f6a_end:
.org 0x23F6C
m68k_023f6c:
        jsr 0x83d4:l
m68k_023f6c_end:
.org 0x23F72
m68k_023f72:
        andi.l #0xffff,%d0
m68k_023f72_end:
.org 0x23F78
m68k_023f78:
        mulu.w %d6,%d0
m68k_023f78_end:
.org 0x23F7A
m68k_023f7a:
        swap %d0
m68k_023f7a_end:
.org 0x23F7C
m68k_023f7c:
        add.w %d0,%d5
m68k_023f7c_end:
.org 0x23F7E
m68k_023f7e:
        rts
m68k_023f7e_end:
.org 0x23F80
m68k_023f80:
        bsr.w (. + 34)
m68k_023f80_end:
.org 0x23F84
m68k_023f84:
        bcc.w (. + 28)
m68k_023f84_end:
.org 0x23F88
m68k_023f88:
        cmpi.w #0x5000,0x2(%a0, %d2.w)
m68k_023f88_end:
.org 0x23F8E
m68k_023f8e:
        bcs.w (. + 14)
m68k_023f8e_end:
.org 0x23F92
m68k_023f92:
        move.w %d6,%d5
m68k_023f92_end:
.org 0x23F94
m68k_023f94:
        subi.w #0x400,%d5
m68k_023f94_end:
.org 0x23F98
m68k_023f98:
        bra.w (. + 8)
m68k_023f98_end:
.org 0x23F9C
m68k_023f9c:
        addi.w #0x400,%d5
m68k_023f9c_end:
.org 0x23FA0
m68k_023fa0:
        rts
m68k_023fa0_end:
.org 0x23FA2
m68k_023fa2:
        move.w (%a0, %d2.w),%d3
m68k_023fa2_end:
.org 0x23FA6
m68k_023fa6:
        addi.w #0xf80,%d3
m68k_023fa6_end:
.org 0x23FAA
m68k_023faa:
        move.w %d3,%d4
m68k_023faa_end:
.org 0x23FAC
m68k_023fac:
        addi.w #0x2080,%d4
m68k_023fac_end:
.org 0x23FB0
m68k_023fb0:
        bcs.w (. + 12)
m68k_023fb0_end:
.org 0x23FB4
m68k_023fb4:
        cmpi.w #0x6400,%d4
m68k_023fb4_end:
.org 0x23FB8
m68k_023fb8:
        bls.w (. + 8)
m68k_023fb8_end:
.org 0x23FBC
m68k_023fbc:
        move.w #0x6400,%d4
m68k_023fbc_end:
.org 0x23FC0
m68k_023fc0:
        move.w 0x2(%a0, %d2.w),%d5
m68k_023fc0_end:
.org 0x23FC4
m68k_023fc4:
        cmpi.w #0x5000,%d5
m68k_023fc4_end:
.org 0x23FC8
m68k_023fc8:
        bcs.w (. + 42)
m68k_023fc8_end:
.org 0x23FCC
m68k_023fcc:
        move.w %d5,%d6
m68k_023fcc_end:
.org 0x23FCE
m68k_023fce:
        subi.w #0x3800,%d5
m68k_023fce_end:
.org 0x23FD2
m68k_023fd2:
        cmp.w %d3,%d0
m68k_023fd2_end:
.org 0x23FD4
m68k_023fd4:
        bcs.w (. + 68)
m68k_023fd4_end:
.org 0x23FD8
m68k_023fd8:
        cmp.w %d4,%d0
m68k_023fd8_end:
.org 0x23FDA
m68k_023fda:
        bhi.w (. + 62)
m68k_023fda_end:
.org 0x23FDE
m68k_023fde:
        cmp.w %d5,%d1
m68k_023fde_end:
.org 0x23FE0
m68k_023fe0:
        bcs.w (. + 56)
m68k_023fe0_end:
.org 0x23FE4
m68k_023fe4:
        cmp.w %d6,%d1
m68k_023fe4_end:
.org 0x23FE6
m68k_023fe6:
        bhi.w (. + 50)
m68k_023fe6_end:
.org 0x23FEA
m68k_023fea:
        ori.w #0x1,%sr
m68k_023fea_end:
.org 0x23FEE
m68k_023fee:
        bra.w (. + 88)
m68k_023fee_end:
.org 0x23FF2
m68k_023ff2:
        move.w %d5,%d6
m68k_023ff2_end:
.org 0x23FF4
m68k_023ff4:
        addi.w #0x3800,%d6
m68k_023ff4_end:
.org 0x23FF8
m68k_023ff8:
        cmp.w %d3,%d0
m68k_023ff8_end:
.org 0x23FFA
m68k_023ffa:
        bcs.w (. + 30)
m68k_023ffa_end:
.org 0x23FFE
m68k_023ffe:
        cmp.w %d4,%d0
m68k_023ffe_end:
.org 0x24000
m68k_024000:
        bhi.w (. + 24)
m68k_024000_end:
.org 0x24004
m68k_024004:
        cmp.w %d5,%d1
m68k_024004_end:
.org 0x24006
m68k_024006:
        bcs.w (. + 18)
m68k_024006_end:
.org 0x2400A
m68k_02400a:
        cmp.w %d6,%d1
m68k_02400a_end:
.org 0x2400C
m68k_02400c:
        bhi.w (. + 12)
m68k_02400c_end:
.org 0x24010
m68k_024010:
        ori.w #0x1,%sr
m68k_024010_end:
.org 0x24014
m68k_024014:
        bra.w (. + 50)
m68k_024014_end:
.org 0x24018
m68k_024018:
        jsr 0x83d4:l
m68k_024018_end:
.org 0x2401E
m68k_02401e:
        andi.l #0xffff,%d0
m68k_02401e_end:
.org 0x24024
m68k_024024:
        sub.w %d3,%d4
m68k_024024_end:
.org 0x24026
m68k_024026:
        mulu.w %d4,%d0
m68k_024026_end:
.org 0x24028
m68k_024028:
        swap %d0
m68k_024028_end:
.org 0x2402A
m68k_02402a:
        add.w %d0,%d3
m68k_02402a_end:
.org 0x2402C
m68k_02402c:
        addq.w #0x1,%d3
m68k_02402c_end:
.org 0x2402E
m68k_02402e:
        jsr 0x83d4:l
m68k_02402e_end:
.org 0x24034
m68k_024034:
        andi.l #0xffff,%d0
m68k_024034_end:
.org 0x2403A
m68k_02403a:
        mulu.w #0x2000,%d0
m68k_02403a_end:
.org 0x2403E
m68k_02403e:
        swap %d0
m68k_02403e_end:
.org 0x24040
m68k_024040:
        add.w %d0,%d5
m68k_024040_end:
.org 0x24042
m68k_024042:
        andi.w #0xfffe,%sr
m68k_024042_end:
.org 0x24046
m68k_024046:
        rts
m68k_024046_end:
.org 0x24048
m68k_024048:
        bsr.w (. + 18)
m68k_024048_end:
.org 0x2404C
m68k_02404c:
        bcc.w (. + 12)
m68k_02404c_end:
.org 0x24050
m68k_024050:
        addi.w #0x1000,%d3
m68k_024050_end:
.org 0x24054
m68k_024054:
        addi.w #0x2480,%d5
m68k_024054_end:
.org 0x24058
m68k_024058:
        rts
m68k_024058_end:
.org 0x2405A
m68k_02405a:
        move.w (%a0, %d2.w),%d3
m68k_02405a_end:
.org 0x2405E
m68k_02405e:
        move.w %d3,%d4
m68k_02405e_end:
.org 0x24060
m68k_024060:
        subi.w #0xc00,%d3
m68k_024060_end:
.org 0x24064
m68k_024064:
        addi.w #0xc00,%d4
m68k_024064_end:
.org 0x24068
m68k_024068:
        move.w 0x2(%a0, %d2.w),%d5
m68k_024068_end:
.org 0x2406C
m68k_02406c:
        move.w %d5,%d6
m68k_02406c_end:
.org 0x2406E
m68k_02406e:
        subi.w #0x3400,%d5
m68k_02406e_end:
.org 0x24072
m68k_024072:
        cmp.w %d3,%d0
m68k_024072_end:
.org 0x24074
m68k_024074:
        bcs.w (. + 30)
m68k_024074_end:
.org 0x24078
m68k_024078:
        cmp.w %d4,%d0
m68k_024078_end:
.org 0x2407A
m68k_02407a:
        bhi.w (. + 24)
m68k_02407a_end:
.org 0x2407E
m68k_02407e:
        cmp.w %d5,%d1
m68k_02407e_end:
.org 0x24080
m68k_024080:
        bcs.w (. + 18)
m68k_024080_end:
.org 0x24084
m68k_024084:
        cmp.w %d6,%d1
m68k_024084_end:
.org 0x24086
m68k_024086:
        bhi.w (. + 12)
m68k_024086_end:
.org 0x2408A
m68k_02408a:
        ori.w #0x1,%sr
m68k_02408a_end:
.org 0x2408E
m68k_02408e:
        bra.w (. + 46)
m68k_02408e_end:
.org 0x24092
m68k_024092:
        jsr 0x83d4:l
m68k_024092_end:
.org 0x24098
m68k_024098:
        andi.l #0xffff,%d0
m68k_024098_end:
.org 0x2409E
m68k_02409e:
        mulu.w #0x1800,%d0
m68k_02409e_end:
.org 0x240A2
m68k_0240a2:
        swap %d0
m68k_0240a2_end:
.org 0x240A4
m68k_0240a4:
        add.w %d0,%d3
m68k_0240a4_end:
.org 0x240A6
m68k_0240a6:
        jsr 0x83d4:l
m68k_0240a6_end:
.org 0x240AC
m68k_0240ac:
        andi.l #0xffff,%d0
m68k_0240ac_end:
.org 0x240B2
m68k_0240b2:
        mulu.w #0x1800,%d0
m68k_0240b2_end:
.org 0x240B6
m68k_0240b6:
        add.w %d0,%d5
m68k_0240b6_end:
.org 0x240B8
m68k_0240b8:
        andi.w #0xfffe,%sr
m68k_0240b8_end:
.org 0x240BC
m68k_0240bc:
        rts
m68k_0240bc_end:
.org 0x240BE
m68k_0240be:
        bsr.w (. + -1060)
m68k_0240be_end:
.org 0x240C2
m68k_0240c2:
        bcs.w (. + 1876)
m68k_0240c2_end:
.org 0x240C6
m68k_0240c6:
        bsr.w (. + -2448)
m68k_0240c6_end:
.org 0x240CA
m68k_0240ca:
        bcs.w (. + 24)
m68k_0240ca_end:
.org 0x240CE
m68k_0240ce:
        bsr.w (. + -6520)
m68k_0240ce_end:
.org 0x240D2
m68k_0240d2:
        bcs.w (. + 16)
m68k_0240d2_end:
.org 0x240D6
m68k_0240d6:
        bsr.w (. + -1176)
m68k_0240d6_end:
.org 0x240DA
m68k_0240da:
        bcs.w (. + 8)
m68k_0240da_end:
.org 0x240DE
m68k_0240de:
        bsr.w (. + 6)
m68k_0240de_end:
.org 0x240E2
m68k_0240e2:
        rts
m68k_0240e2_end:
.org 0x240E4
m68k_0240e4:
        lea.l 0xa654:w,%a0
m68k_0240e4_end:
.org 0x240E8
m68k_0240e8:
        tst.b (%a0, %d7.w)
m68k_0240e8_end:
.org 0x240EC
m68k_0240ec:
        bne.w (. + 154)
m68k_0240ec_end:
.org 0x240F0
m68k_0240f0:
        lea.l 0xff3cc2:l,%a0
m68k_0240f0_end:
.org 0x240F6
m68k_0240f6:
        tst.b (%a0, %d7.w)
m68k_0240f6_end:
.org 0x240FA
m68k_0240fa:
        bne.w (. + 140)
m68k_0240fa_end:
.org 0x240FE
m68k_0240fe:
        lea.l 0xff3dc2:l,%a1
m68k_0240fe_end:
.org 0x24104
m68k_024104:
        tst.b (%a1, %d7.w)
m68k_024104_end:
.org 0x24108
m68k_024108:
        bne.w (. + 126)
m68k_024108_end:
.org 0x2410C
m68k_02410c:
        lea.l 0xa150:w,%a0
m68k_02410c_end:
.org 0x24110
m68k_024110:
        move.w %d7,%d0
m68k_024110_end:
.org 0x24112
m68k_024112:
        lsl.w #0x2,%d0
m68k_024112_end:
.org 0x24114
m68k_024114:
        move.w 0x2(%a0, %d0.w),%d1
m68k_024114_end:
.org 0x24118
m68k_024118:
        move.w (%a0, %d0.w),%d0
m68k_024118_end:
.org 0x2411C
m68k_02411c:
        lea.l 0xae2f6:l,%a0
m68k_02411c_end:
.org 0x24122
m68k_024122:
        move.w 0xf68a:w,%d2
m68k_024122_end:
.org 0x24126
m68k_024126:
        lsl.w #0x2,%d2
m68k_024126_end:
.org 0x24128
m68k_024128:
        cmpi.w #0x5c,%d2
m68k_024128_end:
.org 0x2412C
m68k_02412c:
        beq.w (. + 48)
m68k_02412c_end:
.org 0x24130
m68k_024130:
        cmpi.w #0x4800,(%a0, %d2.w)
m68k_024130_end:
.org 0x24136
m68k_024136:
        bhi.w (. + 22)
m68k_024136_end:
.org 0x2413A
m68k_02413a:
        cmpi.w #0x2800,(%a0, %d2.w)
m68k_02413a_end:
.org 0x24140
m68k_024140:
        bcc.w (. + 20)
m68k_024140_end:
.org 0x24144
m68k_024144:
        bsr.w (. + 68)
m68k_024144_end:
.org 0x24148
m68k_024148:
        bra.w (. + 24)
m68k_024148_end:
.org 0x2414C
m68k_02414c:
        bsr.w (. + 78)
m68k_02414c_end:
.org 0x24150
m68k_024150:
        bra.w (. + 16)
m68k_024150_end:
.org 0x24154
m68k_024154:
        bsr.w (. + 90)
m68k_024154_end:
.org 0x24158
m68k_024158:
        bra.w (. + 8)
m68k_024158_end:
.org 0x2415C
m68k_02415c:
        bsr.w (. + 284)
m68k_02415c_end:
.org 0x24160
m68k_024160:
        lea.l 0xff2c00:l,%a0
m68k_024160_end:
.org 0x24166
m68k_024166:
        move.w %d7,%d1
m68k_024166_end:
.org 0x24168
m68k_024168:
        lsl.w #0x2,%d1
m68k_024168_end:
.org 0x2416A
m68k_02416a:
        lsr.w #0x7,%d3
m68k_02416a_end:
.org 0x2416C
m68k_02416c:
        move.w %d3,(%a0, %d1.w)
m68k_02416c_end:
.org 0x24170
m68k_024170:
        lsr.w #0x7,%d5
m68k_024170_end:
.org 0x24172
m68k_024172:
        move.w %d5,0x2(%a0, %d1.w)
m68k_024172_end:
.org 0x24176
m68k_024176:
        lea.l 0xae28:w,%a0
m68k_024176_end:
.org 0x2417A
m68k_02417a:
        move.b #0x1,(%a0, %d7.w)
m68k_02417a_end:
.org 0x24180
m68k_024180:
        jsr 0x1dcaa:l
m68k_024180_end:
.org 0x24186
m68k_024186:
        rts
m68k_024186_end:
.org 0x24188
m68k_024188:
        bsr.w (. + -782)
m68k_024188_end:
.org 0x2418C
m68k_02418c:
        bcc.w (. + 12)
m68k_02418c_end:
.org 0x24190
m68k_024190:
        addi.w #0xf80,%d3
m68k_024190_end:
.org 0x24194
m68k_024194:
        addi.w #0x1400,%d5
m68k_024194_end:
.org 0x24198
m68k_024198:
        rts
m68k_024198_end:
.org 0x2419A
m68k_02419a:
        bsr.w (. + -660)
m68k_02419a_end:
.org 0x2419E
m68k_02419e:
        bcc.w (. + 14)
m68k_02419e_end:
.org 0x241A2
m68k_0241a2:
        move.w %d4,%d3
m68k_0241a2_end:
.org 0x241A4
m68k_0241a4:
        subi.w #0xf80,%d3
m68k_0241a4_end:
.org 0x241A8
m68k_0241a8:
        addi.w #0x1400,%d5
m68k_0241a8_end:
.org 0x241AC
m68k_0241ac:
        rts
m68k_0241ac_end:
.org 0x241AE
m68k_0241ae:
        bsr.w (. + 38)
m68k_0241ae_end:
.org 0x241B2
m68k_0241b2:
        bcc.w (. + 32)
m68k_0241b2_end:
.org 0x241B6
m68k_0241b6:
        cmpi.w #0x5000,0x2(%a0, %d2.w)
m68k_0241b6_end:
.org 0x241BC
m68k_0241bc:
        bcs.w (. + 16)
m68k_0241bc_end:
.org 0x241C0
m68k_0241c0:
        move.w %d4,%d3
m68k_0241c0_end:
.org 0x241C2
m68k_0241c2:
        move.w %d6,%d5
m68k_0241c2_end:
.org 0x241C4
m68k_0241c4:
        subi.w #0x400,%d5
m68k_0241c4_end:
.org 0x241C8
m68k_0241c8:
        bra.w (. + 10)
m68k_0241c8_end:
.org 0x241CC
m68k_0241cc:
        move.w %d4,%d3
m68k_0241cc_end:
.org 0x241CE
m68k_0241ce:
        addi.w #0x400,%d5
m68k_0241ce_end:
.org 0x241D2
m68k_0241d2:
        rts
m68k_0241d2_end:
.org 0x241D4
m68k_0241d4:
        move.w (%a0, %d2.w),%d3
m68k_0241d4_end:
.org 0x241D8
m68k_0241d8:
        move.w %d3,%d4
m68k_0241d8_end:
.org 0x241DA
m68k_0241da:
        subi.w #0xf80,%d4
m68k_0241da_end:
.org 0x241DE
m68k_0241de:
        subi.w #0x3000,%d3
m68k_0241de_end:
.org 0x241E2
m68k_0241e2:
        bcs.w (. + 12)
m68k_0241e2_end:
.org 0x241E6
m68k_0241e6:
        cmpi.w #0xc00,%d3
m68k_0241e6_end:
.org 0x241EA
m68k_0241ea:
        bcc.w (. + 8)
m68k_0241ea_end:
.org 0x241EE
m68k_0241ee:
        move.w #0xc00,%d3
m68k_0241ee_end:
.org 0x241F2
m68k_0241f2:
        move.w 0x2(%a0, %d2.w),%d5
m68k_0241f2_end:
.org 0x241F6
m68k_0241f6:
        cmpi.w #0x5000,%d5
m68k_0241f6_end:
.org 0x241FA
m68k_0241fa:
        bcs.w (. + 42)
m68k_0241fa_end:
.org 0x241FE
m68k_0241fe:
        move.w %d5,%d6
m68k_0241fe_end:
.org 0x24200
m68k_024200:
        subi.w #0x3800,%d5
m68k_024200_end:
.org 0x24204
m68k_024204:
        cmp.w %d3,%d0
m68k_024204_end:
.org 0x24206
m68k_024206:
        bcs.w (. + 68)
m68k_024206_end:
.org 0x2420A
m68k_02420a:
        cmp.w %d4,%d0
m68k_02420a_end:
.org 0x2420C
m68k_02420c:
        bhi.w (. + 62)
m68k_02420c_end:
.org 0x24210
m68k_024210:
        cmp.w %d5,%d1
m68k_024210_end:
.org 0x24212
m68k_024212:
        bcs.w (. + 56)
m68k_024212_end:
.org 0x24216
m68k_024216:
        cmp.w %d6,%d1
m68k_024216_end:
.org 0x24218
m68k_024218:
        bhi.w (. + 50)
m68k_024218_end:
.org 0x2421C
m68k_02421c:
        ori.w #0x1,%sr
m68k_02421c_end:
.org 0x24220
m68k_024220:
        bra.w (. + 86)
m68k_024220_end:
.org 0x24224
m68k_024224:
        move.w %d5,%d6
m68k_024224_end:
.org 0x24226
m68k_024226:
        addi.w #0x3800,%d6
m68k_024226_end:
.org 0x2422A
m68k_02422a:
        cmp.w %d3,%d0
m68k_02422a_end:
.org 0x2422C
m68k_02422c:
        bcs.w (. + 30)
m68k_02422c_end:
.org 0x24230
m68k_024230:
        cmp.w %d4,%d0
m68k_024230_end:
.org 0x24232
m68k_024232:
        bhi.w (. + 24)
m68k_024232_end:
.org 0x24236
m68k_024236:
        cmp.w %d5,%d1
m68k_024236_end:
.org 0x24238
m68k_024238:
        bcs.w (. + 18)
m68k_024238_end:
.org 0x2423C
m68k_02423c:
        cmp.w %d6,%d1
m68k_02423c_end:
.org 0x2423E
m68k_02423e:
        bhi.w (. + 12)
m68k_02423e_end:
.org 0x24242
m68k_024242:
        ori.w #0x1,%sr
m68k_024242_end:
.org 0x24246
m68k_024246:
        bra.w (. + 48)
m68k_024246_end:
.org 0x2424A
m68k_02424a:
        jsr 0x83d4:l
m68k_02424a_end:
.org 0x24250
m68k_024250:
        andi.l #0xffff,%d0
m68k_024250_end:
.org 0x24256
m68k_024256:
        sub.w %d3,%d4
m68k_024256_end:
.org 0x24258
m68k_024258:
        mulu.w %d4,%d0
m68k_024258_end:
.org 0x2425A
m68k_02425a:
        swap %d0
m68k_02425a_end:
.org 0x2425C
m68k_02425c:
        add.w %d0,%d3
m68k_02425c_end:
.org 0x2425E
m68k_02425e:
        jsr 0x83d4:l
m68k_02425e_end:
.org 0x24264
m68k_024264:
        andi.l #0xffff,%d0
m68k_024264_end:
.org 0x2426A
m68k_02426a:
        mulu.w #0x2000,%d0
m68k_02426a_end:
.org 0x2426E
m68k_02426e:
        swap %d0
m68k_02426e_end:
.org 0x24270
m68k_024270:
        add.w %d0,%d5
m68k_024270_end:
.org 0x24272
m68k_024272:
        andi.w #0xfffe,%sr
m68k_024272_end:
.org 0x24276
m68k_024276:
        rts
m68k_024276_end:
.org 0x24278
m68k_024278:
        bsr.w (. + 18)
m68k_024278_end:
.org 0x2427C
m68k_02427c:
        bcc.w (. + 12)
m68k_02427c_end:
.org 0x24280
m68k_024280:
        addi.w #0x1000,%d3
m68k_024280_end:
.org 0x24284
m68k_024284:
        addi.w #0xf80,%d5
m68k_024284_end:
.org 0x24288
m68k_024288:
        rts
m68k_024288_end:
.org 0x2428A
m68k_02428a:
        move.w (%a0, %d2.w),%d3
m68k_02428a_end:
.org 0x2428E
m68k_02428e:
        move.w %d3,%d4
m68k_02428e_end:
.org 0x24290
m68k_024290:
        subi.w #0xc00,%d3
m68k_024290_end:
.org 0x24294
m68k_024294:
        addi.w #0xc00,%d4
m68k_024294_end:
.org 0x24298
m68k_024298:
        move.w 0x2(%a0, %d2.w),%d5
m68k_024298_end:
.org 0x2429C
m68k_02429c:
        move.w %d5,%d6
m68k_02429c_end:
.org 0x2429E
m68k_02429e:
        addi.w #0x3400,%d6
m68k_02429e_end:
.org 0x242A2
m68k_0242a2:
        cmp.w %d3,%d0
m68k_0242a2_end:
.org 0x242A4
m68k_0242a4:
        bcs.w (. + 30)
m68k_0242a4_end:
.org 0x242A8
m68k_0242a8:
        cmp.w %d4,%d0
m68k_0242a8_end:
.org 0x242AA
m68k_0242aa:
        bhi.w (. + 24)
m68k_0242aa_end:
.org 0x242AE
m68k_0242ae:
        cmp.w %d5,%d1
m68k_0242ae_end:
.org 0x242B0
m68k_0242b0:
        bcs.w (. + 18)
m68k_0242b0_end:
.org 0x242B4
m68k_0242b4:
        cmp.w %d6,%d1
m68k_0242b4_end:
.org 0x242B6
m68k_0242b6:
        bhi.w (. + 12)
m68k_0242b6_end:
.org 0x242BA
m68k_0242ba:
        ori.w #0x1,%sr
m68k_0242ba_end:
.org 0x242BE
m68k_0242be:
        bra.w (. + 46)
m68k_0242be_end:
.org 0x242C2
m68k_0242c2:
        jsr 0x83d4:l
m68k_0242c2_end:
.org 0x242C8
m68k_0242c8:
        andi.l #0xffff,%d0
m68k_0242c8_end:
.org 0x242CE
m68k_0242ce:
        mulu.w #0x1800,%d0
m68k_0242ce_end:
.org 0x242D2
m68k_0242d2:
        swap %d0
m68k_0242d2_end:
.org 0x242D4
m68k_0242d4:
        add.w %d0,%d3
m68k_0242d4_end:
.org 0x242D6
m68k_0242d6:
        jsr 0x83d4:l
m68k_0242d6_end:
.org 0x242DC
m68k_0242dc:
        andi.l #0xffff,%d0
m68k_0242dc_end:
.org 0x242E2
m68k_0242e2:
        mulu.w #0x1800,%d0
m68k_0242e2_end:
.org 0x242E6
m68k_0242e6:
        add.w %d0,%d5
m68k_0242e6_end:
.org 0x242E8
m68k_0242e8:
        andi.w #0xfffe,%sr
m68k_0242e8_end:
.org 0x242EC
m68k_0242ec:
        rts
m68k_0242ec_end:
.org 0x242EE
m68k_0242ee:
        bsr.w (. + -1620)
m68k_0242ee_end:
.org 0x242F2
m68k_0242f2:
        bcs.w (. + 1316)
m68k_0242f2_end:
.org 0x242F6
m68k_0242f6:
        bsr.w (. + -3008)
m68k_0242f6_end:
.org 0x242FA
m68k_0242fa:
        bcs.w (. + 24)
m68k_0242fa_end:
.org 0x242FE
m68k_0242fe:
        bsr.w (. + -7080)
m68k_0242fe_end:
.org 0x24302
m68k_024302:
        bcs.w (. + 16)
m68k_024302_end:
.org 0x24306
m68k_024306:
        bsr.w (. + -5590)
m68k_024306_end:
.org 0x2430A
m68k_02430a:
        bcs.w (. + 8)
m68k_02430a_end:
.org 0x2430E
m68k_02430e:
        bsr.w (. + 6)
m68k_02430e_end:
.org 0x24312
m68k_024312:
        rts
m68k_024312_end:
.org 0x24314
m68k_024314:
        lea.l 0xa654:w,%a0
m68k_024314_end:
.org 0x24318
m68k_024318:
        tst.b (%a0, %d7.w)
m68k_024318_end:
.org 0x2431C
m68k_02431c:
        bne.w (. + 130)
m68k_02431c_end:
.org 0x24320
m68k_024320:
        lea.l 0xff3cc2:l,%a0
m68k_024320_end:
.org 0x24326
m68k_024326:
        tst.b (%a0, %d7.w)
m68k_024326_end:
.org 0x2432A
m68k_02432a:
        bne.w (. + 116)
m68k_02432a_end:
.org 0x2432E
m68k_02432e:
        lea.l 0xff3dc2:l,%a1
m68k_02432e_end:
.org 0x24334
m68k_024334:
        tst.b (%a1, %d7.w)
m68k_024334_end:
.org 0x24338
m68k_024338:
        bne.w (. + 102)
m68k_024338_end:
.org 0x2433C
m68k_02433c:
        lea.l 0xa150:w,%a0
m68k_02433c_end:
.org 0x24340
m68k_024340:
        move.w %d7,%d0
m68k_024340_end:
.org 0x24342
m68k_024342:
        lsl.w #0x2,%d0
m68k_024342_end:
.org 0x24344
m68k_024344:
        move.w 0x2(%a0, %d0.w),%d1
m68k_024344_end:
.org 0x24348
m68k_024348:
        move.w (%a0, %d0.w),%d0
m68k_024348_end:
.org 0x2434C
m68k_02434c:
        bsr.w (. + 84)
m68k_02434c_end:
.org 0x24350
m68k_024350:
        bcc.w (. + 20)
m68k_024350_end:
.org 0x24354
m68k_024354:
        move.w %d3,0xf3a6:w
m68k_024354_end:
.org 0x24358
m68k_024358:
        bsr.w (. + 132)
m68k_024358_end:
.org 0x2435C
m68k_02435c:
        bcs.w (. + 66)
m68k_02435c_end:
.org 0x24360
m68k_024360:
        bra.w (. + 24)
m68k_024360_end:
.org 0x24364
m68k_024364:
        bsr.w (. + -2140)
m68k_024364_end:
.org 0x24368
m68k_024368:
        bcs.w (. + 12)
m68k_024368_end:
.org 0x2436C
m68k_02436c:
        bsr.w (. + -1990)
m68k_02436c_end:
.org 0x24370
m68k_024370:
        bra.w (. + 8)
m68k_024370_end:
.org 0x24374
m68k_024374:
        bsr.w (. + 202)
m68k_024374_end:
.org 0x24378
m68k_024378:
        lea.l 0xff2c00:l,%a0
m68k_024378_end:
.org 0x2437E
m68k_02437e:
        move.w %d7,%d1
m68k_02437e_end:
.org 0x24380
m68k_024380:
        lsl.w #0x2,%d1
m68k_024380_end:
.org 0x24382
m68k_024382:
        lsr.w #0x7,%d2
m68k_024382_end:
.org 0x24384
m68k_024384:
        move.w %d2,(%a0, %d1.w)
m68k_024384_end:
.org 0x24388
m68k_024388:
        lsr.w #0x7,%d4
m68k_024388_end:
.org 0x2438A
m68k_02438a:
        move.w %d4,0x2(%a0, %d1.w)
m68k_02438a_end:
.org 0x2438E
m68k_02438e:
        lea.l 0xae28:w,%a0
m68k_02438e_end:
.org 0x24392
m68k_024392:
        move.b #0x1,(%a0, %d7.w)
m68k_024392_end:
.org 0x24398
m68k_024398:
        jsr 0x1dcaa:l
m68k_024398_end:
.org 0x2439E
m68k_02439e:
        rts
m68k_02439e_end:
.org 0x243A0
m68k_0243a0:
        movem.l %d0-%d1,-(%a7)
m68k_0243a0_end:
.org 0x243A4
m68k_0243a4:
        bsr.w (. + -3794)
m68k_0243a4_end:
.org 0x243A8
m68k_0243a8:
        tst.w 0xd300:w
m68k_0243a8_end:
.org 0x243AC
m68k_0243ac:
        bmi.w (. + 38)
m68k_0243ac_end:
.org 0x243B0
m68k_0243b0:
        bsr.w (. + -5988)
m68k_0243b0_end:
.org 0x243B4
m68k_0243b4:
        move.w %d7,%d0
m68k_0243b4_end:
.org 0x243B6
m68k_0243b6:
        jsr 0xbac8:l
m68k_0243b6_end:
.org 0x243BC
m68k_0243bc:
        lsl.w #0x2,%d0
m68k_0243bc_end:
.org 0x243BE
m68k_0243be:
        move.l 0x2(%a1, %d0.w),%d0
m68k_0243be_end:
.org 0x243C2
m68k_0243c2:
        mulu.w %d1,%d0
m68k_0243c2_end:
.org 0x243C4
m68k_0243c4:
        cmp.l %d0,%d2
m68k_0243c4_end:
.org 0x243C6
m68k_0243c6:
        bhi.w (. + 12)
m68k_0243c6_end:
.org 0x243CA
m68k_0243ca:
        ori.w #0x1,%sr
m68k_0243ca_end:
.org 0x243CE
m68k_0243ce:
        bra.w (. + 8)
m68k_0243ce_end:
.org 0x243D2
m68k_0243d2:
        andi.w #0xfffe,%sr
m68k_0243d2_end:
.org 0x243D6
m68k_0243d6:
        movem.l (%a7)+,%d0-%d1
m68k_0243d6_end:
.org 0x243DA
m68k_0243da:
        rts
m68k_0243da_end:
.org 0x243DC
m68k_0243dc:
        lea.l 0xb600:w,%a0
m68k_0243dc_end:
.org 0x243E0
m68k_0243e0:
        move.w %d7,%d0
m68k_0243e0_end:
.org 0x243E2
m68k_0243e2:
        lsl.w #0x1,%d0
m68k_0243e2_end:
.org 0x243E4
m68k_0243e4:
        move.w (%a0, %d0.w),%d1
m68k_0243e4_end:
.org 0x243E8
m68k_0243e8:
        clr.w %d2
m68k_0243e8_end:
.org 0x243EA
m68k_0243ea:
        cmpi.w #0x46,%d1
m68k_0243ea_end:
.org 0x243EE
m68k_0243ee:
        bcs.w (. + 16)
m68k_0243ee_end:
.org 0x243F2
m68k_0243f2:
        addq.w #0x1,%d2
m68k_0243f2_end:
.org 0x243F4
m68k_0243f4:
        cmpi.w #0x5a,%d1
m68k_0243f4_end:
.org 0x243F8
m68k_0243f8:
        bcs.w (. + 6)
m68k_0243f8_end:
.org 0x243FC
m68k_0243fc:
        addq.w #0x1,%d2
m68k_0243fc_end:
.org 0x243FE
m68k_0243fe:
        jsr 0x83d4:l
m68k_0243fe_end:
.org 0x24404
m68k_024404:
        andi.l #0xffff,%d0
m68k_024404_end:
.org 0x2440A
m68k_02440a:
        lsl.l #0x2,%d0
m68k_02440a_end:
.org 0x2440C
m68k_02440c:
        swap %d0
m68k_02440c_end:
.org 0x2440E
m68k_02440e:
        cmp.w %d2,%d0
m68k_02440e_end:
.org 0x24410
m68k_024410:
        bcc.w (. + 12)
m68k_024410_end:
.org 0x24414
m68k_024414:
        bsr.w (. + 8524)
m68k_024414_end:
.org 0x24418
m68k_024418:
        bcs.w (. + 36)
m68k_024418_end:
.org 0x2441C
m68k_02441c:
        lea.l 0xff2c00:l,%a1
m68k_02441c_end:
.org 0x24422
m68k_024422:
        move.w %d7,%d0
m68k_024422_end:
.org 0x24424
m68k_024424:
        lsl.w #0x2,%d0
m68k_024424_end:
.org 0x24426
m68k_024426:
        lea.l 0xa150:w,%a0
m68k_024426_end:
.org 0x2442A
m68k_02442a:
        move.w 0xf3a6:w,%d3
m68k_02442a_end:
.org 0x2442E
m68k_02442e:
        lsl.w #0x2,%d3
m68k_02442e_end:
.org 0x24430
m68k_024430:
        move.w (%a0, %d3.w),%d2
m68k_024430_end:
.org 0x24434
m68k_024434:
        move.w 0x2(%a0, %d3.w),%d4
m68k_024434_end:
.org 0x24438
m68k_024438:
        andi.w #0xfffe,%sr
m68k_024438_end:
.org 0x2443C
m68k_02443c:
        rts
m68k_02443c_end:
.org 0x2443E
m68k_02443e:
        lea.l 0xae2f6:l,%a0
m68k_02443e_end:
.org 0x24444
m68k_024444:
        move.w 0xf68a:w,%d0
m68k_024444_end:
.org 0x24448
m68k_024448:
        lsl.w #0x2,%d0
m68k_024448_end:
.org 0x2444A
m68k_02444a:
        cmpi.w #0x5c,%d0
m68k_02444a_end:
.org 0x2444E
m68k_02444e:
        beq.w (. + 40)
m68k_02444e_end:
.org 0x24452
m68k_024452:
        move.w (%a0, %d0.w),%d2
m68k_024452_end:
.org 0x24456
m68k_024456:
        addi.w #0xc00,%d2
m68k_024456_end:
.org 0x2445A
m68k_02445a:
        move.w 0x2(%a0, %d0.w),%d4
m68k_02445a_end:
.org 0x2445E
m68k_02445e:
        cmpi.w #0x5000,%d4
m68k_02445e_end:
.org 0x24462
m68k_024462:
        bcs.w (. + 12)
m68k_024462_end:
.org 0x24466
m68k_024466:
        subi.w #0xf80,%d4
m68k_024466_end:
.org 0x2446A
m68k_02446a:
        bra.w (. + 28)
m68k_02446a_end:
.org 0x2446E
m68k_02446e:
        addi.w #0xf80,%d4
m68k_02446e_end:
.org 0x24472
m68k_024472:
        bra.w (. + 20)
m68k_024472_end:
.org 0x24476
m68k_024476:
        move.w (%a0, %d0.w),%d2
m68k_024476_end:
.org 0x2447A
m68k_02447a:
        subi.w #0xf80,%d2
m68k_02447a_end:
.org 0x2447E
m68k_02447e:
        move.w 0x2(%a0, %d0.w),%d4
m68k_02447e_end:
.org 0x24482
m68k_024482:
        addi.w #0xc00,%d4
m68k_024482_end:
.org 0x24486
m68k_024486:
        rts
m68k_024486_end:
.org 0x24488
m68k_024488:
        bsr.w (. + -2030)
m68k_024488_end:
.org 0x2448C
m68k_02448c:
        bcs.w (. + 906)
m68k_02448c_end:
.org 0x24490
m68k_024490:
        bsr.w (. + -3418)
m68k_024490_end:
.org 0x24494
m68k_024494:
        bcs.w (. + 24)
m68k_024494_end:
.org 0x24498
m68k_024498:
        bsr.w (. + -7490)
m68k_024498_end:
.org 0x2449C
m68k_02449c:
        bcs.w (. + 16)
m68k_02449c_end:
.org 0x244A0
m68k_0244a0:
        bsr.w (. + -6000)
m68k_0244a0_end:
.org 0x244A4
m68k_0244a4:
        bcs.w (. + 8)
m68k_0244a4_end:
.org 0x244A8
m68k_0244a8:
        bsr.w (. + 6)
m68k_0244a8_end:
.org 0x244AC
m68k_0244ac:
        rts
m68k_0244ac_end:
.org 0x244AE
m68k_0244ae:
        lea.l 0xa654:w,%a0
m68k_0244ae_end:
.org 0x244B2
m68k_0244b2:
        tst.b (%a0, %d7.w)
m68k_0244b2_end:
.org 0x244B6
m68k_0244b6:
        bne.w (. + 182)
m68k_0244b6_end:
.org 0x244BA
m68k_0244ba:
        lea.l 0xff3cc2:l,%a0
m68k_0244ba_end:
.org 0x244C0
m68k_0244c0:
        tst.b (%a0, %d7.w)
m68k_0244c0_end:
.org 0x244C4
m68k_0244c4:
        bne.w (. + 168)
m68k_0244c4_end:
.org 0x244C8
m68k_0244c8:
        lea.l 0xff3dc2:l,%a1
m68k_0244c8_end:
.org 0x244CE
m68k_0244ce:
        tst.b (%a1, %d7.w)
m68k_0244ce_end:
.org 0x244D2
m68k_0244d2:
        bne.w (. + 154)
m68k_0244d2_end:
.org 0x244D6
m68k_0244d6:
        lea.l 0xa150:w,%a0
m68k_0244d6_end:
.org 0x244DA
m68k_0244da:
        move.w %d7,%d0
m68k_0244da_end:
.org 0x244DC
m68k_0244dc:
        lsl.w #0x2,%d0
m68k_0244dc_end:
.org 0x244DE
m68k_0244de:
        move.w 0x2(%a0, %d0.w),%d1
m68k_0244de_end:
.org 0x244E2
m68k_0244e2:
        move.w (%a0, %d0.w),%d0
m68k_0244e2_end:
.org 0x244E6
m68k_0244e6:
        bsr.w (. + -326)
m68k_0244e6_end:
.org 0x244EA
m68k_0244ea:
        bcc.w (. + 24)
m68k_0244ea_end:
.org 0x244EE
m68k_0244ee:
        move.w %d3,0xf3a6:w
m68k_0244ee_end:
.org 0x244F2
m68k_0244f2:
        bsr.w (. + -278)
m68k_0244f2_end:
.org 0x244F6
m68k_0244f6:
        bcs.w (. + 118)
m68k_0244f6_end:
.org 0x244FA
m68k_0244fa:
        move.w %d2,%d3
m68k_0244fa_end:
.org 0x244FC
m68k_0244fc:
        move.w %d4,%d5
m68k_0244fc_end:
.org 0x244FE
m68k_0244fe:
        bra.w (. + 72)
m68k_0244fe_end:
.org 0x24502
m68k_024502:
        lea.l 0xae2f6:l,%a0
m68k_024502_end:
.org 0x24508
m68k_024508:
        move.w 0xf68a:w,%d2
m68k_024508_end:
.org 0x2450C
m68k_02450c:
        lsl.w #0x2,%d2
m68k_02450c_end:
.org 0x2450E
m68k_02450e:
        cmpi.w #0x5c,%d2
m68k_02450e_end:
.org 0x24512
m68k_024512:
        beq.w (. + 48)
m68k_024512_end:
.org 0x24516
m68k_024516:
        cmpi.w #0x4800,(%a0, %d2.w)
m68k_024516_end:
.org 0x2451C
m68k_02451c:
        bhi.w (. + 22)
m68k_02451c_end:
.org 0x24520
m68k_024520:
        cmpi.w #0x2800,(%a0, %d2.w)
m68k_024520_end:
.org 0x24526
m68k_024526:
        bcc.w (. + 20)
m68k_024526_end:
.org 0x2452A
m68k_02452a:
        bsr.w (. + 68)
m68k_02452a_end:
.org 0x2452E
m68k_02452e:
        bra.w (. + 24)
m68k_02452e_end:
.org 0x24532
m68k_024532:
        bsr.w (. + 78)
m68k_024532_end:
.org 0x24536
m68k_024536:
        bra.w (. + 16)
m68k_024536_end:
.org 0x2453A
m68k_02453a:
        bsr.w (. + 90)
m68k_02453a_end:
.org 0x2453E
m68k_02453e:
        bra.w (. + 8)
m68k_02453e_end:
.org 0x24542
m68k_024542:
        bsr.w (. + 120)
m68k_024542_end:
.org 0x24546
m68k_024546:
        lea.l 0xff2c00:l,%a0
m68k_024546_end:
.org 0x2454C
m68k_02454c:
        move.w %d7,%d1
m68k_02454c_end:
.org 0x2454E
m68k_02454e:
        lsl.w #0x2,%d1
m68k_02454e_end:
.org 0x24550
m68k_024550:
        lsr.w #0x7,%d3
m68k_024550_end:
.org 0x24552
m68k_024552:
        move.w %d3,(%a0, %d1.w)
m68k_024552_end:
.org 0x24556
m68k_024556:
        lsr.w #0x7,%d5
m68k_024556_end:
.org 0x24558
m68k_024558:
        move.w %d5,0x2(%a0, %d1.w)
m68k_024558_end:
.org 0x2455C
m68k_02455c:
        lea.l 0xae28:w,%a0
m68k_02455c_end:
.org 0x24560
m68k_024560:
        move.b #0x1,(%a0, %d7.w)
m68k_024560_end:
.org 0x24566
m68k_024566:
        jsr 0x1dcaa:l
m68k_024566_end:
.org 0x2456C
m68k_02456c:
        rts
m68k_02456c_end:
.org 0x2456E
m68k_02456e:
        bsr.w (. + -1780)
m68k_02456e_end:
.org 0x24572
m68k_024572:
        bcc.w (. + 12)
m68k_024572_end:
.org 0x24576
m68k_024576:
        addi.w #0xf80,%d3
m68k_024576_end:
.org 0x2457A
m68k_02457a:
        addi.w #0x1c00,%d5
m68k_02457a_end:
.org 0x2457E
m68k_02457e:
        rts
m68k_02457e_end:
.org 0x24580
m68k_024580:
        bsr.w (. + -1658)
m68k_024580_end:
.org 0x24584
m68k_024584:
        bcc.w (. + 14)
m68k_024584_end:
.org 0x24588
m68k_024588:
        move.w %d4,%d3
m68k_024588_end:
.org 0x2458A
m68k_02458a:
        subi.w #0xf80,%d3
m68k_02458a_end:
.org 0x2458E
m68k_02458e:
        addi.w #0x1c00,%d5
m68k_02458e_end:
.org 0x24592
m68k_024592:
        rts
m68k_024592_end:
.org 0x24594
m68k_024594:
        bsr.w (. + -960)
m68k_024594_end:
.org 0x24598
m68k_024598:
        bcc.w (. + 32)
m68k_024598_end:
.org 0x2459C
m68k_02459c:
        cmpi.w #0x5000,0x2(%a0, %d2.w)
m68k_02459c_end:
.org 0x245A2
m68k_0245a2:
        bcs.w (. + 16)
m68k_0245a2_end:
.org 0x245A6
m68k_0245a6:
        move.w %d4,%d3
m68k_0245a6_end:
.org 0x245A8
m68k_0245a8:
        move.w %d6,%d5
m68k_0245a8_end:
.org 0x245AA
m68k_0245aa:
        addi.w #0x400,%d5
m68k_0245aa_end:
.org 0x245AE
m68k_0245ae:
        bra.w (. + 10)
m68k_0245ae_end:
.org 0x245B2
m68k_0245b2:
        move.w %d4,%d3
m68k_0245b2_end:
.org 0x245B4
m68k_0245b4:
        subi.w #0x400,%d5
m68k_0245b4_end:
.org 0x245B8
m68k_0245b8:
        rts
m68k_0245b8_end:
.org 0x245BA
m68k_0245ba:
        bsr.w (. + -816)
m68k_0245ba_end:
.org 0x245BE
m68k_0245be:
        bcc.w (. + 12)
m68k_0245be_end:
.org 0x245C2
m68k_0245c2:
        addi.w #0x800,%d3
m68k_0245c2_end:
.org 0x245C6
m68k_0245c6:
        addi.w #0xf80,%d5
m68k_0245c6_end:
.org 0x245CA
m68k_0245ca:
        rts
m68k_0245ca_end:
.org 0x245CC
m68k_0245cc:
        bsr.w (. + -2354)
m68k_0245cc_end:
.org 0x245D0
m68k_0245d0:
        bcs.w (. + 582)
m68k_0245d0_end:
.org 0x245D4
m68k_0245d4:
        bsr.w (. + -3742)
m68k_0245d4_end:
.org 0x245D8
m68k_0245d8:
        bcs.w (. + 24)
m68k_0245d8_end:
.org 0x245DC
m68k_0245dc:
        bsr.w (. + -7814)
m68k_0245dc_end:
.org 0x245E0
m68k_0245e0:
        bcs.w (. + 16)
m68k_0245e0_end:
.org 0x245E4
m68k_0245e4:
        bsr.w (. + -6324)
m68k_0245e4_end:
.org 0x245E8
m68k_0245e8:
        bcs.w (. + 8)
m68k_0245e8_end:
.org 0x245EC
m68k_0245ec:
        bsr.w (. + 6)
m68k_0245ec_end:
.org 0x245F0
m68k_0245f0:
        rts
m68k_0245f0_end:
.org 0x245F2
m68k_0245f2:
        lea.l 0xa654:w,%a0
m68k_0245f2_end:
.org 0x245F6
m68k_0245f6:
        tst.b (%a0, %d7.w)
m68k_0245f6_end:
.org 0x245FA
m68k_0245fa:
        bne.w (. + 130)
m68k_0245fa_end:
.org 0x245FE
m68k_0245fe:
        lea.l 0xff3cc2:l,%a0
m68k_0245fe_end:
.org 0x24604
m68k_024604:
        tst.b (%a0, %d7.w)
m68k_024604_end:
.org 0x24608
m68k_024608:
        bne.w (. + 116)
m68k_024608_end:
.org 0x2460C
m68k_02460c:
        lea.l 0xff3dc2:l,%a1
m68k_02460c_end:
.org 0x24612
m68k_024612:
        tst.b (%a1, %d7.w)
m68k_024612_end:
.org 0x24616
m68k_024616:
        bne.w (. + 102)
m68k_024616_end:
.org 0x2461A
m68k_02461a:
        lea.l 0xa150:w,%a0
m68k_02461a_end:
.org 0x2461E
m68k_02461e:
        move.w %d7,%d0
m68k_02461e_end:
.org 0x24620
m68k_024620:
        lsl.w #0x2,%d0
m68k_024620_end:
.org 0x24622
m68k_024622:
        move.w 0x2(%a0, %d0.w),%d1
m68k_024622_end:
.org 0x24626
m68k_024626:
        move.w (%a0, %d0.w),%d0
m68k_024626_end:
.org 0x2462A
m68k_02462a:
        bsr.w (. + -650)
m68k_02462a_end:
.org 0x2462E
m68k_02462e:
        bcc.w (. + 20)
m68k_02462e_end:
.org 0x24632
m68k_024632:
        move.w %d3,0xf3a6:w
m68k_024632_end:
.org 0x24636
m68k_024636:
        bsr.w (. + -602)
m68k_024636_end:
.org 0x2463A
m68k_02463a:
        bcs.w (. + 66)
m68k_02463a_end:
.org 0x2463E
m68k_02463e:
        bra.w (. + 24)
m68k_02463e_end:
.org 0x24642
m68k_024642:
        bsr.w (. + -2874)
m68k_024642_end:
.org 0x24646
m68k_024646:
        bcs.w (. + 12)
m68k_024646_end:
.org 0x2464A
m68k_02464a:
        bsr.w (. + -2724)
m68k_02464a_end:
.org 0x2464E
m68k_02464e:
        bra.w (. + 8)
m68k_02464e_end:
.org 0x24652
m68k_024652:
        bsr.w (. + 44)
m68k_024652_end:
.org 0x24656
m68k_024656:
        lea.l 0xff2c00:l,%a0
m68k_024656_end:
.org 0x2465C
m68k_02465c:
        move.w %d7,%d1
m68k_02465c_end:
.org 0x2465E
m68k_02465e:
        lsl.w #0x2,%d1
m68k_02465e_end:
.org 0x24660
m68k_024660:
        lsr.w #0x7,%d2
m68k_024660_end:
.org 0x24662
m68k_024662:
        move.w %d2,(%a0, %d1.w)
m68k_024662_end:
.org 0x24666
m68k_024666:
        lsr.w #0x7,%d4
m68k_024666_end:
.org 0x24668
m68k_024668:
        move.w %d4,0x2(%a0, %d1.w)
m68k_024668_end:
.org 0x2466C
m68k_02466c:
        lea.l 0xae28:w,%a0
m68k_02466c_end:
.org 0x24670
m68k_024670:
        move.b #0x1,(%a0, %d7.w)
m68k_024670_end:
.org 0x24676
m68k_024676:
        jsr 0x1dcaa:l
m68k_024676_end:
.org 0x2467C
m68k_02467c:
        rts
m68k_02467c_end:
.org 0x2467E
m68k_02467e:
        lea.l 0xae2f6:l,%a0
m68k_02467e_end:
.org 0x24684
m68k_024684:
        move.w 0xf68a:w,%d0
m68k_024684_end:
.org 0x24688
m68k_024688:
        lsl.w #0x2,%d0
m68k_024688_end:
.org 0x2468A
m68k_02468a:
        cmpi.w #0x5c,%d0
m68k_02468a_end:
.org 0x2468E
m68k_02468e:
        beq.w (. + 40)
m68k_02468e_end:
.org 0x24692
m68k_024692:
        move.w (%a0, %d0.w),%d2
m68k_024692_end:
.org 0x24696
m68k_024696:
        subi.w #0xc00,%d2
m68k_024696_end:
.org 0x2469A
m68k_02469a:
        move.w 0x2(%a0, %d0.w),%d4
m68k_02469a_end:
.org 0x2469E
m68k_02469e:
        cmpi.w #0x5000,%d4
m68k_02469e_end:
.org 0x246A2
m68k_0246a2:
        bcs.w (. + 12)
m68k_0246a2_end:
.org 0x246A6
m68k_0246a6:
        subi.w #0xf80,%d4
m68k_0246a6_end:
.org 0x246AA
m68k_0246aa:
        bra.w (. + 28)
m68k_0246aa_end:
.org 0x246AE
m68k_0246ae:
        addi.w #0xf80,%d4
m68k_0246ae_end:
.org 0x246B2
m68k_0246b2:
        bra.w (. + 20)
m68k_0246b2_end:
.org 0x246B6
m68k_0246b6:
        move.w (%a0, %d0.w),%d2
m68k_0246b6_end:
.org 0x246BA
m68k_0246ba:
        subi.w #0xf80,%d2
m68k_0246ba_end:
.org 0x246BE
m68k_0246be:
        move.w 0x2(%a0, %d0.w),%d4
m68k_0246be_end:
.org 0x246C2
m68k_0246c2:
        subi.w #0xc00,%d4
m68k_0246c2_end:
.org 0x246C6
m68k_0246c6:
        rts
m68k_0246c6_end:
.org 0x246C8
m68k_0246c8:
        bsr.w (. + -2606)
m68k_0246c8_end:
.org 0x246CC
m68k_0246cc:
        bcs.w (. + 330)
m68k_0246cc_end:
.org 0x246D0
m68k_0246d0:
        bsr.w (. + -3994)
m68k_0246d0_end:
.org 0x246D4
m68k_0246d4:
        bcs.w (. + 24)
m68k_0246d4_end:
.org 0x246D8
m68k_0246d8:
        bsr.w (. + -8066)
m68k_0246d8_end:
.org 0x246DC
m68k_0246dc:
        bcs.w (. + 16)
m68k_0246dc_end:
.org 0x246E0
m68k_0246e0:
        bsr.w (. + -6576)
m68k_0246e0_end:
.org 0x246E4
m68k_0246e4:
        bcs.w (. + 8)
m68k_0246e4_end:
.org 0x246E8
m68k_0246e8:
        bsr.w (. + -3156)
m68k_0246e8_end:
.org 0x246EC
m68k_0246ec:
        rts
m68k_0246ec_end:
.org 0x24806
m68k_024806:
        bsr.w (. + 560)
m68k_024806_end:
.org 0x2480A
m68k_02480a:
        bcs.w (. + -1300)
m68k_02480a_end:
.org 0x2480E
m68k_02480e:
        bsr.w (. + 518)
m68k_02480e_end:
.org 0x24812
m68k_024812:
        bcs.w (. + -3484)
m68k_024812_end:
.org 0x24816
m68k_024816:
        bsr.w (. + -4320)
m68k_024816_end:
.org 0x2481A
m68k_02481a:
        bcs.w (. + 24)
m68k_02481a_end:
.org 0x2481E
m68k_02481e:
        bsr.w (. + -8392)
m68k_02481e_end:
.org 0x24822
m68k_024822:
        bcs.w (. + 16)
m68k_024822_end:
.org 0x24826
m68k_024826:
        bsr.w (. + -6902)
m68k_024826_end:
.org 0x2482A
m68k_02482a:
        bcs.w (. + 8)
m68k_02482a_end:
.org 0x2482E
m68k_02482e:
        bsr.w (. + 6)
m68k_02482e_end:
.org 0x24832
m68k_024832:
        rts
m68k_024832_end:
.org 0x24834
m68k_024834:
        move.w 0xff3eca:l,%d2
m68k_024834_end:
.org 0x2483A
m68k_02483a:
        lea.l 0xa654:w,%a0
m68k_02483a_end:
.org 0x2483E
m68k_02483e:
        tst.b (%a0, %d7.w)
m68k_02483e_end:
.org 0x24842
m68k_024842:
        bne.w (. + 142)
m68k_024842_end:
.org 0x24846
m68k_024846:
        lea.l 0xff3cc2:l,%a0
m68k_024846_end:
.org 0x2484C
m68k_02484c:
        tst.b (%a0, %d7.w)
m68k_02484c_end:
.org 0x24850
m68k_024850:
        bne.w (. + 128)
m68k_024850_end:
.org 0x24854
m68k_024854:
        lea.l 0xff3dc2:l,%a1
m68k_024854_end:
.org 0x2485A
m68k_02485a:
        tst.b (%a1, %d7.w)
m68k_02485a_end:
.org 0x2485E
m68k_02485e:
        bne.w (. + 114)
m68k_02485e_end:
.org 0x24862
m68k_024862:
        move.w %d2,-(%a7)
m68k_024862_end:
.org 0x24864
m68k_024864:
        bsr.w (. + -5010)
m68k_024864_end:
.org 0x24868
m68k_024868:
        move.w (%a7)+,%d2
m68k_024868_end:
.org 0x2486A
m68k_02486a:
        tst.w 0xd300:w
m68k_02486a_end:
.org 0x2486E
m68k_02486e:
        bmi.w (. + 16)
m68k_02486e_end:
.org 0x24872
m68k_024872:
        bsr.w (. + 96)
m68k_024872_end:
.org 0x24876
m68k_024876:
        bcs.w (. + 90)
m68k_024876_end:
.org 0x2487A
m68k_02487a:
        bra.w (. + 48)
m68k_02487a_end:
.org 0x2487E
m68k_02487e:
        bsr.w (. + 274)
m68k_02487e_end:
.org 0x24882
m68k_024882:
        lea.l 0xa150:w,%a0
m68k_024882_end:
.org 0x24886
m68k_024886:
        move.w %d7,%d0
m68k_024886_end:
.org 0x24888
m68k_024888:
        lsl.w #0x2,%d0
m68k_024888_end:
.org 0x2488A
m68k_02488a:
        move.w 0x2(%a0, %d0.w),%d1
m68k_02488a_end:
.org 0x2488E
m68k_02488e:
        move.w (%a0, %d0.w),%d0
m68k_02488e_end:
.org 0x24892
m68k_024892:
        move.w %d2,%d3
m68k_024892_end:
.org 0x24894
m68k_024894:
        andi.w #0xff00,%d2
m68k_024894_end:
.org 0x24898
m68k_024898:
        lsl.w #0x2,%d2
m68k_024898_end:
.org 0x2489A
m68k_02489a:
        lsl.w #0x7,%d3
m68k_02489a_end:
.org 0x2489C
m68k_02489c:
        lsl.w #0x3,%d3
m68k_02489c_end:
.org 0x2489E
m68k_02489e:
        cmp.w %d2,%d0
m68k_02489e_end:
.org 0x248A0
m68k_0248a0:
        bne.w (. + 10)
m68k_0248a0_end:
.org 0x248A4
m68k_0248a4:
        cmp.w %d3,%d1
m68k_0248a4_end:
.org 0x248A6
m68k_0248a6:
        beq.w (. + 42)
m68k_0248a6_end:
.org 0x248AA
m68k_0248aa:
        lea.l 0xff2c00:l,%a0
m68k_0248aa_end:
.org 0x248B0
m68k_0248b0:
        move.w %d7,%d1
m68k_0248b0_end:
.org 0x248B2
m68k_0248b2:
        lsl.w #0x2,%d1
m68k_0248b2_end:
.org 0x248B4
m68k_0248b4:
        lsr.w #0x7,%d2
m68k_0248b4_end:
.org 0x248B6
m68k_0248b6:
        move.w %d2,(%a0, %d1.w)
m68k_0248b6_end:
.org 0x248BA
m68k_0248ba:
        lsr.w #0x7,%d3
m68k_0248ba_end:
.org 0x248BC
m68k_0248bc:
        move.w %d3,0x2(%a0, %d1.w)
m68k_0248bc_end:
.org 0x248C0
m68k_0248c0:
        lea.l 0xae28:w,%a0
m68k_0248c0_end:
.org 0x248C4
m68k_0248c4:
        move.b #0x1,(%a0, %d7.w)
m68k_0248c4_end:
.org 0x248CA
m68k_0248ca:
        jsr 0x1dcaa:l
m68k_0248ca_end:
.org 0x248D0
m68k_0248d0:
        rts
m68k_0248d0_end:
.org 0x248D2
m68k_0248d2:
        lea.l 0xb600:w,%a0
m68k_0248d2_end:
.org 0x248D6
m68k_0248d6:
        move.w %d7,%d0
m68k_0248d6_end:
.org 0x248D8
m68k_0248d8:
        lsl.w #0x1,%d0
m68k_0248d8_end:
.org 0x248DA
m68k_0248da:
        move.w (%a0, %d0.w),%d1
m68k_0248da_end:
.org 0x248DE
m68k_0248de:
        clr.w %d2
m68k_0248de_end:
.org 0x248E0
m68k_0248e0:
        cmpi.w #0x46,%d1
m68k_0248e0_end:
.org 0x248E4
m68k_0248e4:
        bcs.w (. + 16)
m68k_0248e4_end:
.org 0x248E8
m68k_0248e8:
        addq.w #0x1,%d2
m68k_0248e8_end:
.org 0x248EA
m68k_0248ea:
        cmpi.w #0x5a,%d1
m68k_0248ea_end:
.org 0x248EE
m68k_0248ee:
        bcs.w (. + 6)
m68k_0248ee_end:
.org 0x248F2
m68k_0248f2:
        addq.w #0x1,%d2
m68k_0248f2_end:
.org 0x248F4
m68k_0248f4:
        jsr 0x83d4:l
m68k_0248f4_end:
.org 0x248FA
m68k_0248fa:
        andi.l #0xffff,%d0
m68k_0248fa_end:
.org 0x24900
m68k_024900:
        lsl.l #0x2,%d0
m68k_024900_end:
.org 0x24902
m68k_024902:
        swap %d0
m68k_024902_end:
.org 0x24904
m68k_024904:
        cmp.w %d2,%d0
m68k_024904_end:
.org 0x24906
m68k_024906:
        bcc.w (. + 12)
m68k_024906_end:
.org 0x2490A
m68k_02490a:
        bsr.w (. + 7254)
m68k_02490a_end:
.org 0x2490E
m68k_02490e:
        bcs.w (. + 22)
m68k_02490e_end:
.org 0x24912
m68k_024912:
        bsr.w (. + 20)
m68k_024912_end:
.org 0x24916
m68k_024916:
        lsl.w #0x2,%d1
m68k_024916_end:
.org 0x24918
m68k_024918:
        move.w (%a0, %d1.w),%d2
m68k_024918_end:
.org 0x2491C
m68k_02491c:
        move.w 0x2(%a0, %d1.w),%d3
m68k_02491c_end:
.org 0x24920
m68k_024920:
        andi.w #0xfffe,%sr
m68k_024920_end:
.org 0x24924
m68k_024924:
        rts
m68k_024924_end:
.org 0x24926
m68k_024926:
        lea.l 0xa150:w,%a0
m68k_024926_end:
.org 0x2492A
m68k_02492a:
        lea.l 0xd300:w,%a1
m68k_02492a_end:
.org 0x2492E
m68k_02492e:
        lea.l 0xabda8:l,%a2
m68k_02492e_end:
.org 0x24934
m68k_024934:
        lea.l 0x9fff:w,%a3
m68k_024934_end:
.org 0x24938
m68k_024938:
        move.w 0xf68a:w,%d0
m68k_024938_end:
.org 0x2493C
m68k_02493c:
        clr.w %d1
m68k_02493c_end:
.org 0x2493E
m68k_02493e:
        move.b (%a3, %d0.w),%d1
m68k_02493e_end:
.org 0x24942
m68k_024942:
        lsl.w #0x5,%d0
m68k_024942_end:
.org 0x24944
m68k_024944:
        lsl.w #0x1,%d1
m68k_024944_end:
.org 0x24946
m68k_024946:
        add.w %d1,%d0
m68k_024946_end:
.org 0x24948
m68k_024948:
        clr.w %d2
m68k_024948_end:
.org 0x2494A
m68k_02494a:
        move.b (%a2, %d0.w),%d2
m68k_02494a_end:
.org 0x2494E
m68k_02494e:
        lsl.w #0x3,%d2
m68k_02494e_end:
.org 0x24950
m68k_024950:
        lsl.w #0x7,%d2
m68k_024950_end:
.org 0x24952
m68k_024952:
        clr.w %d3
m68k_024952_end:
.org 0x24954
m68k_024954:
        move.b 0x1(%a2, %d0.w),%d3
m68k_024954_end:
.org 0x24958
m68k_024958:
        lsl.w #0x3,%d3
m68k_024958_end:
.org 0x2495A
m68k_02495a:
        lsl.w #0x7,%d3
m68k_02495a_end:
.org 0x2495C
m68k_02495c:
        move.w #0xffff,%d0
m68k_02495c_end:
.org 0x24960
m68k_024960:
        move.w (%a1)+,%d4
m68k_024960_end:
.org 0x24962
m68k_024962:
        bmi.w (. + 44)
m68k_024962_end:
.org 0x24966
m68k_024966:
        lsl.w #0x2,%d4
m68k_024966_end:
.org 0x24968
m68k_024968:
        move.w (%a0, %d4.w),%d5
m68k_024968_end:
.org 0x2496C
m68k_02496c:
        sub.w %d2,%d5
m68k_02496c_end:
.org 0x2496E
m68k_02496e:
        bcc.w (. + 6)
m68k_02496e_end:
.org 0x24972
m68k_024972:
        neg.w %d5
m68k_024972_end:
.org 0x24974
m68k_024974:
        move.w 0x2(%a0, %d4.w),%d6
m68k_024974_end:
.org 0x24978
m68k_024978:
        sub.w %d3,%d6
m68k_024978_end:
.org 0x2497A
m68k_02497a:
        bcc.w (. + 6)
m68k_02497a_end:
.org 0x2497E
m68k_02497e:
        neg.w %d6
m68k_02497e_end:
.org 0x24980
m68k_024980:
        add.w %d6,%d5
m68k_024980_end:
.org 0x24982
m68k_024982:
        cmp.w %d0,%d5
m68k_024982_end:
.org 0x24984
m68k_024984:
        bcc.b (. + -36)
m68k_024984_end:
.org 0x24986
m68k_024986:
        move.w %d5,%d0
m68k_024986_end:
.org 0x24988
m68k_024988:
        lsr.w #0x2,%d4
m68k_024988_end:
.org 0x2498A
m68k_02498a:
        move.w %d4,%d1
m68k_02498a_end:
.org 0x2498C
m68k_02498c:
        bra.b (. + -44)
m68k_02498c_end:
.org 0x2498E
m68k_02498e:
        rts
m68k_02498e_end:
.org 0x24990
m68k_024990:
        move.w 0xf770:w,%d0
m68k_024990_end:
.org 0x24994
m68k_024994:
        cmpi.w #0x9,%d0
m68k_024994_end:
.org 0x24998
m68k_024998:
        bcc.w (. + 90)
m68k_024998_end:
.org 0x2499C
m68k_02499c:
        lsl.w #0x2,%d0
m68k_02499c_end:
.org 0x2499E
m68k_02499e:
        lea.l 80(%pc),%a0
m68k_02499e_end:
.org 0x249A2
m68k_0249a2:
        move.w (%a0, %d0.w),%d1
m68k_0249a2_end:
.org 0x249A6
m68k_0249a6:
        move.w 0x2(%a0, %d0.w),%d2
m68k_0249a6_end:
.org 0x249AA
m68k_0249aa:
        lea.l 0x9fff:w,%a0
m68k_0249aa_end:
.org 0x249AE
m68k_0249ae:
        move.w 0xf68a:w,%d0
m68k_0249ae_end:
.org 0x249B2
m68k_0249b2:
        clr.w %d3
m68k_0249b2_end:
.org 0x249B4
m68k_0249b4:
        move.b (%a0, %d0.w),%d3
m68k_0249b4_end:
.org 0x249B8
m68k_0249b8:
        lea.l 0xabda8:l,%a0
m68k_0249b8_end:
.org 0x249BE
m68k_0249be:
        lsl.w #0x5,%d0
m68k_0249be_end:
.org 0x249C0
m68k_0249c0:
        lsl.w #0x1,%d3
m68k_0249c0_end:
.org 0x249C2
m68k_0249c2:
        add.w %d3,%d0
m68k_0249c2_end:
.org 0x249C4
m68k_0249c4:
        clr.w %d3
m68k_0249c4_end:
.org 0x249C6
m68k_0249c6:
        move.b (%a0, %d0.w),%d3
m68k_0249c6_end:
.org 0x249CA
m68k_0249ca:
        cmpi.w #0xe,%d3
m68k_0249ca_end:
.org 0x249CE
m68k_0249ce:
        bhi.w (. + 6)
m68k_0249ce_end:
.org 0x249D2
m68k_0249d2:
        neg.w %d1
m68k_0249d2_end:
.org 0x249D4
m68k_0249d4:
        clr.w %d4
m68k_0249d4_end:
.org 0x249D6
m68k_0249d6:
        move.b 0x1(%a0, %d0.w),%d4
m68k_0249d6_end:
.org 0x249DA
m68k_0249da:
        cmpi.w #0x14,%d4
m68k_0249da_end:
.org 0x249DE
m68k_0249de:
        bcs.w (. + 6)
m68k_0249de_end:
.org 0x249E2
m68k_0249e2:
        neg.w %d2
m68k_0249e2_end:
.org 0x249E4
m68k_0249e4:
        add.w %d1,%d3
m68k_0249e4_end:
.org 0x249E6
m68k_0249e6:
        add.w %d2,%d4
m68k_0249e6_end:
.org 0x249E8
m68k_0249e8:
        move.w %d3,%d2
m68k_0249e8_end:
.org 0x249EA
m68k_0249ea:
        lsl.w #0x8,%d2
m68k_0249ea_end:
.org 0x249EC
m68k_0249ec:
        andi.w #0xff,%d4
m68k_0249ec_end:
.org 0x249F0
m68k_0249f0:
        or.w %d4,%d2
m68k_0249f0_end:
.org 0x249F2
m68k_0249f2:
        rts
m68k_0249f2_end:
.org 0x24A14
m68k_024a14:
        move.l 0xf69e:w,%d0
m68k_024a14_end:
.org 0x24A18
m68k_024a18:
        cmp.l 0xf6a2:w,%d0
m68k_024a18_end:
.org 0x24A1C
m68k_024a1c:
        bcc.w (. + 20)
m68k_024a1c_end:
.org 0x24A20
m68k_024a20:
        cmp.l 0xf768:w,%d0
m68k_024a20_end:
.org 0x24A24
m68k_024a24:
        bcc.w (. + 12)
m68k_024a24_end:
.org 0x24A28
m68k_024a28:
        ori.w #0x1,%sr
m68k_024a28_end:
.org 0x24A2C
m68k_024a2c:
        bra.w (. + 8)
m68k_024a2c_end:
.org 0x24A30
m68k_024a30:
        andi.w #0xfffe,%sr
m68k_024a30_end:
.org 0x24A34
m68k_024a34:
        rts
m68k_024a34_end:
.org 0x24A36
m68k_024a36:
        jsr 0x1a438:l
m68k_024a36_end:
.org 0x24A3C
m68k_024a3c:
        lea.l 0xa5a4:w,%a1
m68k_024a3c_end:
.org 0x24A40
m68k_024a40:
        lea.l 0xa150:w,%a2
m68k_024a40_end:
.org 0x24A44
m68k_024a44:
        clr.w %d3
m68k_024a44_end:
.org 0x24A46
m68k_024a46:
        move.w (%a1)+,%d4
m68k_024a46_end:
.org 0x24A48
m68k_024a48:
        bmi.w (. + 44)
m68k_024a48_end:
.org 0x24A4C
m68k_024a4c:
        lsl.w #0x2,%d4
m68k_024a4c_end:
.org 0x24A4E
m68k_024a4e:
        move.w (%a2, %d4.w),%d1
m68k_024a4e_end:
.org 0x24A52
m68k_024a52:
        move.w 0x2(%a2, %d4.w),%d2
m68k_024a52_end:
.org 0x24A56
m68k_024a56:
        jsr 0x1a44e:l
m68k_024a56_end:
.org 0x24A5C
m68k_024a5c:
        cmpi.b #0x6,%d0
m68k_024a5c_end:
.org 0x24A60
m68k_024a60:
        bne.w (. + 12)
m68k_024a60_end:
.org 0x24A64
m68k_024a64:
        addq.w #0x1,%d3
m68k_024a64_end:
.org 0x24A66
m68k_024a66:
        cmpi.w #0x4,%d3
m68k_024a66_end:
.org 0x24A6A
m68k_024a6a:
        bcs.b (. + -36)
m68k_024a6a_end:
.org 0x24A6C
m68k_024a6c:
        andi.w #0xfffe,%sr
m68k_024a6c_end:
.org 0x24A70
m68k_024a70:
        bra.w (. + 8)
m68k_024a70_end:
.org 0x24A74
m68k_024a74:
        ori.w #0x1,%sr
m68k_024a74_end:
.org 0x24A78
m68k_024a78:
        rts
m68k_024a78_end:
.org 0x24A7A
m68k_024a7a:
        bsr.b (. + -68)
m68k_024a7a_end:
.org 0x24A7C
m68k_024a7c:
        bcs.w (. + -1516)
m68k_024a7c_end:
.org 0x24A80
m68k_024a80:
        bsr.w (. + 54)
m68k_024a80_end:
.org 0x24A84
m68k_024a84:
        bcs.w (. + -1524)
m68k_024a84_end:
.org 0x24A88
m68k_024a88:
        bsr.b (. + -116)
m68k_024a88_end:
.org 0x24A8A
m68k_024a8a:
        bcs.w (. + -3528)
m68k_024a8a_end:
.org 0x24A8E
m68k_024a8e:
        bsr.w (. + -4952)
m68k_024a8e_end:
.org 0x24A92
m68k_024a92:
        bcs.w (. + 24)
m68k_024a92_end:
.org 0x24A96
m68k_024a96:
        bsr.w (. + -9024)
m68k_024a96_end:
.org 0x24A9A
m68k_024a9a:
        bcs.w (. + 16)
m68k_024a9a_end:
.org 0x24A9E
m68k_024a9e:
        bsr.w (. + -7534)
m68k_024a9e_end:
.org 0x24AA2
m68k_024aa2:
        bcs.w (. + 8)
m68k_024aa2_end:
.org 0x24AA6
m68k_024aa6:
        bsr.w (. + 6)
m68k_024aa6_end:
.org 0x24AAA
m68k_024aaa:
        rts
m68k_024aaa_end:
.org 0x24AAC
m68k_024aac:
        move.w 0xff3ecc:l,%d2
m68k_024aac_end:
.org 0x24AB2
m68k_024ab2:
        bra.w (. + -632)
m68k_024ab2_end:
.org 0x24AB6
m68k_024ab6:
        move.l 0xf6a2:w,%d0
m68k_024ab6_end:
.org 0x24ABA
m68k_024aba:
        cmp.l 0xf76c:w,%d0
m68k_024aba_end:
.org 0x24ABE
m68k_024abe:
        bcc.w (. + 12)
m68k_024abe_end:
.org 0x24AC2
m68k_024ac2:
        ori.w #0x1,%sr
m68k_024ac2_end:
.org 0x24AC6
m68k_024ac6:
        bra.w (. + 8)
m68k_024ac6_end:
.org 0x24ACA
m68k_024aca:
        andi.w #0xfffe,%sr
m68k_024aca_end:
.org 0x24ACE
m68k_024ace:
        rts
m68k_024ace_end:
.org 0x25FD2
m68k_025fd2:
        move.w %d7,-(%a7)
m68k_025fd2_end:
.org 0x25FD4
m68k_025fd4:
        bsr.w (. + 54)
m68k_025fd4_end:
.org 0x25FD8
m68k_025fd8:
        bcs.w (. + 46)
m68k_025fd8_end:
.org 0x25FDC
m68k_025fdc:
        bsr.w (. + 336)
m68k_025fdc_end:
.org 0x25FE0
m68k_025fe0:
        bcs.w (. + 38)
m68k_025fe0_end:
.org 0x25FE4
m68k_025fe4:
        bsr.w (. + 616)
m68k_025fe4_end:
.org 0x25FE8
m68k_025fe8:
        bcs.w (. + 30)
m68k_025fe8_end:
.org 0x25FEC
m68k_025fec:
        bsr.w (. + 786)
m68k_025fec_end:
.org 0x25FF0
m68k_025ff0:
        bcs.w (. + 22)
m68k_025ff0_end:
.org 0x25FF4
m68k_025ff4:
        bsr.w (. + 1044)
m68k_025ff4_end:
.org 0x25FF8
m68k_025ff8:
        bcs.w (. + 14)
m68k_025ff8_end:
.org 0x25FFC
m68k_025ffc:
        move.w (%a7)+,%d7
m68k_025ffc_end:
.org 0x25FFE
m68k_025ffe:
        andi.w #0xfffe,%sr
m68k_025ffe_end:
.org 0x26002
m68k_026002:
        bra.w (. + 6)
m68k_026002_end:
.org 0x26006
m68k_026006:
        move.w (%a7)+,%d7
m68k_026006_end:
.org 0x26008
m68k_026008:
        rts
m68k_026008_end:
.org 0x2600A
m68k_02600a:
        jsr 0x83d4:l
m68k_02600a_end:
.org 0x26010
m68k_026010:
        andi.l #0xffff,%d0
m68k_026010_end:
.org 0x26016
m68k_026016:
        lsl.l #0x2,%d0
m68k_026016_end:
.org 0x26018
m68k_026018:
        swap %d0
m68k_026018_end:
.org 0x2601A
m68k_02601a:
        cmpi.w #0x3,%d0
m68k_02601a_end:
.org 0x2601E
m68k_02601e:
        beq.w (. + 98)
m68k_02601e_end:
.org 0x26022
m68k_026022:
        bsr.w (. + 100)
m68k_026022_end:
.org 0x26026
m68k_026026:
        cmpi.b #0x32,%d0
m68k_026026_end:
.org 0x2602A
m68k_02602a:
        bhi.w (. + 86)
m68k_02602a_end:
.org 0x2602E
m68k_02602e:
        move.w %d1,0xf3a6:w
m68k_02602e_end:
.org 0x26032
m68k_026032:
        bsr.w (. + 126)
m68k_026032_end:
.org 0x26036
m68k_026036:
        cmp.l 0xf69a:w,%d0
m68k_026036_end:
.org 0x2603A
m68k_02603a:
        bhi.w (. + 70)
m68k_02603a_end:
.org 0x2603E
m68k_02603e:
        lea.l 0xa754:w,%a0
m68k_02603e_end:
.org 0x26042
m68k_026042:
        move.b #0x3,(%a0, %d7.w)
m68k_026042_end:
.org 0x26048
m68k_026048:
        move.w %d7,0xf3f2:w
m68k_026048_end:
.org 0x2604C
m68k_02604c:
        move.w #0x4,0xf6d4:w
m68k_02604c_end:
.org 0x26052
m68k_026052:
        jsr 0x1a47a:l
m68k_026052_end:
.org 0x26058
m68k_026058:
        bcs.w (. + 32)
m68k_026058_end:
.org 0x2605C
m68k_02605c:
        bchg.b #0x1,0xf6d7:w
m68k_02605c_end:
.org 0x26062
m68k_026062:
        move.w 0xf3a6:w,0xf3d0:w
m68k_026062_end:
.org 0x26068
m68k_026068:
        move.w #0x12c,0xf740:w
m68k_026068_end:
.org 0x2606E
m68k_02606e:
        bsr.w (. + 118)
m68k_02606e_end:
.org 0x26072
m68k_026072:
        bchg.b #0x1,0xf6d7:w
m68k_026072_end:
.org 0x26078
m68k_026078:
        ori.w #0x1,%sr
m68k_026078_end:
.org 0x2607C
m68k_02607c:
        bra.w (. + 8)
m68k_02607c_end:
.org 0x26080
m68k_026080:
        andi.w #0xfffe,%sr
m68k_026080_end:
.org 0x26084
m68k_026084:
        rts
m68k_026084_end:
.org 0x26086
m68k_026086:
        lea.l 0xd300:w,%a0
m68k_026086_end:
.org 0x2608A
m68k_02608a:
        lea.l 0xc300:w,%a1
m68k_02608a_end:
.org 0x2608E
m68k_02608e:
        move.w #0xffff,%d0
m68k_02608e_end:
.org 0x26092
m68k_026092:
        move.w #0xffff,%d1
m68k_026092_end:
.org 0x26096
m68k_026096:
        move.w (%a0)+,%d2
m68k_026096_end:
.org 0x26098
m68k_026098:
        bmi.b (. + 22)
m68k_026098_end:
.org 0x2609A
m68k_02609a:
        andi.w #0xff,%d2
m68k_02609a_end:
.org 0x2609E
m68k_02609e:
        move.b (%a1, %d2.w),%d3
m68k_02609e_end:
.org 0x260A2
m68k_0260a2:
        beq.b (. + -12)
m68k_0260a2_end:
.org 0x260A4
m68k_0260a4:
        cmp.b %d0,%d3
m68k_0260a4_end:
.org 0x260A6
m68k_0260a6:
        bcc.b (. + -16)
m68k_0260a6_end:
.org 0x260A8
m68k_0260a8:
        move.b %d3,%d0
m68k_0260a8_end:
.org 0x260AA
m68k_0260aa:
        move.w %d2,%d1
m68k_0260aa_end:
.org 0x260AC
m68k_0260ac:
        bra.b (. + -22)
m68k_0260ac_end:
.org 0x260AE
m68k_0260ae:
        rts
m68k_0260ae_end:
.org 0x260B0
m68k_0260b0:
        jsr 0x83d4:l
m68k_0260b0_end:
.org 0x260B6
m68k_0260b6:
        andi.l #0xffff,%d0
m68k_0260b6_end:
.org 0x260BC
m68k_0260bc:
        move.l %d0,%d2
m68k_0260bc_end:
.org 0x260BE
m68k_0260be:
        lsl.l #0x2,%d0
m68k_0260be_end:
.org 0x260C0
m68k_0260c0:
        add.l %d2,%d0
m68k_0260c0_end:
.org 0x260C2
m68k_0260c2:
        swap %d0
m68k_0260c2_end:
.org 0x260C4
m68k_0260c4:
        addq.w #0x8,%d0
m68k_0260c4_end:
.org 0x260C6
m68k_0260c6:
        lea.l 0xb400:w,%a0
m68k_0260c6_end:
.org 0x260CA
m68k_0260ca:
        move.w 0xf3a6:w,%d2
m68k_0260ca_end:
.org 0x260CE
m68k_0260ce:
        lsl.w #0x1,%d2
m68k_0260ce_end:
.org 0x260D0
m68k_0260d0:
        move.w (%a0, %d2.w),%d3
m68k_0260d0_end:
.org 0x260D4
m68k_0260d4:
        lea.l 0xb600:w,%a0
m68k_0260d4_end:
.org 0x260D8
m68k_0260d8:
        add.w (%a0, %d2.w),%d3
m68k_0260d8_end:
.org 0x260DC
m68k_0260dc:
        mulu.w %d3,%d0
m68k_0260dc_end:
.org 0x260DE
m68k_0260de:
        move.l %d0,0xf39e:w
m68k_0260de_end:
.org 0x260E2
m68k_0260e2:
        rts
m68k_0260e2_end:
.org 0x2612C
m68k_02612c:
        jsr 0x83d4:l
m68k_02612c_end:
.org 0x26132
m68k_026132:
        andi.l #0xffff,%d0
m68k_026132_end:
.org 0x26138
m68k_026138:
        lsl.l #0x2,%d0
m68k_026138_end:
.org 0x2613A
m68k_02613a:
        swap %d0
m68k_02613a_end:
.org 0x2613C
m68k_02613c:
        cmpi.w #0x3,%d0
m68k_02613c_end:
.org 0x26140
m68k_026140:
        beq.w (. + 94)
m68k_026140_end:
.org 0x26144
m68k_026144:
        bsr.w (. + 96)
m68k_026144_end:
.org 0x26148
m68k_026148:
        tst.w %d5
m68k_026148_end:
.org 0x2614A
m68k_02614a:
        bmi.w (. + 84)
m68k_02614a_end:
.org 0x2614E
m68k_02614e:
        move.w %d5,0xf3a6:w
m68k_02614e_end:
.org 0x26152
m68k_026152:
        bsr.w (. + 194)
m68k_026152_end:
.org 0x26156
m68k_026156:
        cmp.l 0xf69a:w,%d1
m68k_026156_end:
.org 0x2615A
m68k_02615a:
        bhi.w (. + 68)
m68k_02615a_end:
.org 0x2615E
m68k_02615e:
        lea.l 0xa754:w,%a0
m68k_02615e_end:
.org 0x26162
m68k_026162:
        move.b #0x3,(%a0, %d7.w)
m68k_026162_end:
.org 0x26168
m68k_026168:
        move.w %d7,0xf3f2:w
m68k_026168_end:
.org 0x2616C
m68k_02616c:
        clr.w 0xf6d4:w
m68k_02616c_end:
.org 0x26170
m68k_026170:
        jsr 0x1a47a:l
m68k_026170_end:
.org 0x26176
m68k_026176:
        bcs.w (. + 32)
m68k_026176_end:
.org 0x2617A
m68k_02617a:
        bchg.b #0x1,0xf6d7:w
m68k_02617a_end:
.org 0x26180
m68k_026180:
        move.w 0xf3a6:w,0xf3d0:w
m68k_026180_end:
.org 0x26186
m68k_026186:
        move.w #0x128,0xf740:w
m68k_026186_end:
.org 0x2618C
m68k_02618c:
        bsr.w (. + -168)
m68k_02618c_end:
.org 0x26190
m68k_026190:
        bchg.b #0x1,0xf6d7:w
m68k_026190_end:
.org 0x26196
m68k_026196:
        ori.w #0x1,%sr
m68k_026196_end:
.org 0x2619A
m68k_02619a:
        bra.w (. + 8)
m68k_02619a_end:
.org 0x2619E
m68k_02619e:
        andi.w #0xfffe,%sr
m68k_02619e_end:
.org 0x261A2
m68k_0261a2:
        rts
m68k_0261a2_end:
.org 0x261A4
m68k_0261a4:
        jsr 0x1a438:l
m68k_0261a4_end:
.org 0x261AA
m68k_0261aa:
        lea.l 0xd300:w,%a1
m68k_0261aa_end:
.org 0x261AE
m68k_0261ae:
        lea.l 0xa150:w,%a2
m68k_0261ae_end:
.org 0x261B2
m68k_0261b2:
        lea.l 0xc800:w,%a3
m68k_0261b2_end:
.org 0x261B6
m68k_0261b6:
        moveq #0,%d4
m68k_0261b6_end:
.org 0x261B8
m68k_0261b8:
        move.w #0xffff,%d5
m68k_0261b8_end:
.org 0x261BC
m68k_0261bc:
        move.w (%a1)+,%d3
m68k_0261bc_end:
.org 0x261BE
m68k_0261be:
        bmi.w (. + 84)
m68k_0261be_end:
.org 0x261C2
m68k_0261c2:
        andi.w #0xff,%d3
m68k_0261c2_end:
.org 0x261C6
m68k_0261c6:
        move.w %d3,%d2
m68k_0261c6_end:
.org 0x261C8
m68k_0261c8:
        lsl.w #0x2,%d2
m68k_0261c8_end:
.org 0x261CA
m68k_0261ca:
        move.w (%a2, %d2.w),%d1
m68k_0261ca_end:
.org 0x261CE
m68k_0261ce:
        lsr.w #0x7,%d1
m68k_0261ce_end:
.org 0x261D0
m68k_0261d0:
        move.w 0x2(%a2, %d2.w),%d2
m68k_0261d0_end:
.org 0x261D4
m68k_0261d4:
        lsr.w #0x7,%d2
m68k_0261d4_end:
.org 0x261D6
m68k_0261d6:
        jsr 0x1a44e:l
m68k_0261d6_end:
.org 0x261DC
m68k_0261dc:
        cmpi.b #0x0,%d0
m68k_0261dc_end:
.org 0x261E0
m68k_0261e0:
        beq.w (. + 26)
m68k_0261e0_end:
.org 0x261E4
m68k_0261e4:
        cmpi.b #0x3,%d0
m68k_0261e4_end:
.org 0x261E8
m68k_0261e8:
        beq.w (. + 18)
m68k_0261e8_end:
.org 0x261EC
m68k_0261ec:
        cmpi.b #0x7,%d0
m68k_0261ec_end:
.org 0x261F0
m68k_0261f0:
        beq.w (. + 10)
m68k_0261f0_end:
.org 0x261F4
m68k_0261f4:
        cmpi.b #0x1,%d0
m68k_0261f4_end:
.org 0x261F8
m68k_0261f8:
        bne.b (. + -60)
m68k_0261f8_end:
.org 0x261FA
m68k_0261fa:
        move.w %d3,%d0
m68k_0261fa_end:
.org 0x261FC
m68k_0261fc:
        jsr 0xbac8:l
m68k_0261fc_end:
.org 0x26202
m68k_026202:
        lsl.w #0x2,%d0
m68k_026202_end:
.org 0x26204
m68k_026204:
        mulu.w 0x2(%a3, %d0.w),%d1
m68k_026204_end:
.org 0x26208
m68k_026208:
        cmp.l %d4,%d1
m68k_026208_end:
.org 0x2620A
m68k_02620a:
        bls.b (. + -78)
m68k_02620a_end:
.org 0x2620C
m68k_02620c:
        move.l %d1,%d4
m68k_02620c_end:
.org 0x2620E
m68k_02620e:
        move.w %d3,%d5
m68k_02620e_end:
.org 0x26210
m68k_026210:
        bra.b (. + -84)
m68k_026210_end:
.org 0x26212
m68k_026212:
        rts
m68k_026212_end:
.org 0x26214
m68k_026214:
        jsr 0x83d4:l
m68k_026214_end:
.org 0x2621A
m68k_02621a:
        andi.l #0xffff,%d0
m68k_02621a_end:
.org 0x26220
m68k_026220:
        move.l %d0,%d1
m68k_026220_end:
.org 0x26222
m68k_026222:
        lsl.l #0x2,%d0
m68k_026222_end:
.org 0x26224
m68k_026224:
        add.l %d1,%d0
m68k_026224_end:
.org 0x26226
m68k_026226:
        lsl.l #0x1,%d0
m68k_026226_end:
.org 0x26228
m68k_026228:
        add.l %d0,%d1
m68k_026228_end:
.org 0x2622A
m68k_02622a:
        swap %d0
m68k_02622a_end:
.org 0x2622C
m68k_02622c:
        addi.w #0x14,%d0
m68k_02622c_end:
.org 0x26230
m68k_026230:
        lea.l 0xc800:w,%a0
m68k_026230_end:
.org 0x26234
m68k_026234:
        move.w 0xf3a6:w,%d1
m68k_026234_end:
.org 0x26238
m68k_026238:
        lsl.w #0x2,%d1
m68k_026238_end:
.org 0x2623A
m68k_02623a:
        move.l (%a0, %d1.w),%d1
m68k_02623a_end:
.org 0x2623E
m68k_02623e:
        divu.w %d0,%d1
m68k_02623e_end:
.org 0x26240
m68k_026240:
        andi.l #0xffff,%d1
m68k_026240_end:
.org 0x26246
m68k_026246:
        move.l %d1,0xf39e:w
m68k_026246_end:
.org 0x2624A
m68k_02624a:
        rts
m68k_02624a_end:
.org 0x2624C
m68k_02624c:
        jsr 0x83d4:l
m68k_02624c_end:
.org 0x26252
m68k_026252:
        andi.l #0xffff,%d0
m68k_026252_end:
.org 0x26258
m68k_026258:
        lsl.l #0x2,%d0
m68k_026258_end:
.org 0x2625A
m68k_02625a:
        swap %d0
m68k_02625a_end:
.org 0x2625C
m68k_02625c:
        cmpi.w #0x3,%d0
m68k_02625c_end:
.org 0x26260
m68k_026260:
        beq.w (. + 96)
m68k_026260_end:
.org 0x26264
m68k_026264:
        bsr.w (. + -192)
m68k_026264_end:
.org 0x26268
m68k_026268:
        tst.w %d5
m68k_026268_end:
.org 0x2626A
m68k_02626a:
        bmi.w (. + 86)
m68k_02626a_end:
.org 0x2626E
m68k_02626e:
        move.w %d5,0xf3a6:w
m68k_02626e_end:
.org 0x26272
m68k_026272:
        bsr.w (. + 84)
m68k_026272_end:
.org 0x26276
m68k_026276:
        cmp.l 0xf69a:w,%d1
m68k_026276_end:
.org 0x2627A
m68k_02627a:
        bhi.w (. + 70)
m68k_02627a_end:
.org 0x2627E
m68k_02627e:
        lea.l 0xa754:w,%a0
m68k_02627e_end:
.org 0x26282
m68k_026282:
        move.b #0x3,(%a0, %d7.w)
m68k_026282_end:
.org 0x26288
m68k_026288:
        move.w %d7,0xf3f2:w
m68k_026288_end:
.org 0x2628C
m68k_02628c:
        move.w #0x2,0xf6d4:w
m68k_02628c_end:
.org 0x26292
m68k_026292:
        jsr 0x1a47a:l
m68k_026292_end:
.org 0x26298
m68k_026298:
        bcs.w (. + 32)
m68k_026298_end:
.org 0x2629C
m68k_02629c:
        bchg.b #0x1,0xf6d7:w
m68k_02629c_end:
.org 0x262A2
m68k_0262a2:
        move.w 0xf3a6:w,0xf3d0:w
m68k_0262a2_end:
.org 0x262A8
m68k_0262a8:
        move.w #0x12a,0xf740:w
m68k_0262a8_end:
.org 0x262AE
m68k_0262ae:
        bsr.w (. + -458)
m68k_0262ae_end:
.org 0x262B2
m68k_0262b2:
        bchg.b #0x1,0xf6d7:w
m68k_0262b2_end:
.org 0x262B8
m68k_0262b8:
        ori.w #0x1,%sr
m68k_0262b8_end:
.org 0x262BC
m68k_0262bc:
        bra.w (. + 8)
m68k_0262bc_end:
.org 0x262C0
m68k_0262c0:
        andi.w #0xfffe,%sr
m68k_0262c0_end:
.org 0x262C4
m68k_0262c4:
        rts
m68k_0262c4_end:
.org 0x262C6
m68k_0262c6:
        jsr 0x83d4:l
m68k_0262c6_end:
.org 0x262CC
m68k_0262cc:
        andi.l #0xffff,%d0
m68k_0262cc_end:
.org 0x262D2
m68k_0262d2:
        move.l %d0,%d1
m68k_0262d2_end:
.org 0x262D4
m68k_0262d4:
        lsl.l #0x2,%d0
m68k_0262d4_end:
.org 0x262D6
m68k_0262d6:
        add.l %d1,%d0
m68k_0262d6_end:
.org 0x262D8
m68k_0262d8:
        lsl.l #0x1,%d0
m68k_0262d8_end:
.org 0x262DA
m68k_0262da:
        add.l %d1,%d0
m68k_0262da_end:
.org 0x262DC
m68k_0262dc:
        swap %d0
m68k_0262dc_end:
.org 0x262DE
m68k_0262de:
        addi.w #0x1e,%d0
m68k_0262de_end:
.org 0x262E2
m68k_0262e2:
        lea.l 0xc800:w,%a0
m68k_0262e2_end:
.org 0x262E6
m68k_0262e6:
        move.w 0xf3a6:w,%d1
m68k_0262e6_end:
.org 0x262EA
m68k_0262ea:
        lsl.w #0x2,%d1
m68k_0262ea_end:
.org 0x262EC
m68k_0262ec:
        move.l (%a0, %d1.w),%d1
m68k_0262ec_end:
.org 0x262F0
m68k_0262f0:
        divu.w %d0,%d1
m68k_0262f0_end:
.org 0x262F2
m68k_0262f2:
        andi.l #0xffff,%d1
m68k_0262f2_end:
.org 0x262F8
m68k_0262f8:
        move.l %d1,0xf39e:w
m68k_0262f8_end:
.org 0x262FC
m68k_0262fc:
        rts
m68k_0262fc_end:
.org 0x262FE
m68k_0262fe:
        jsr 0x83d4:l
m68k_0262fe_end:
.org 0x26304
m68k_026304:
        andi.l #0xffff,%d0
m68k_026304_end:
.org 0x2630A
m68k_02630a:
        lsl.l #0x2,%d0
m68k_02630a_end:
.org 0x2630C
m68k_02630c:
        swap %d0
m68k_02630c_end:
.org 0x2630E
m68k_02630e:
        cmpi.w #0x3,%d0
m68k_02630e_end:
.org 0x26312
m68k_026312:
        beq.w (. + 96)
m68k_026312_end:
.org 0x26316
m68k_026316:
        bsr.w (. + 98)
m68k_026316_end:
.org 0x2631A
m68k_02631a:
        tst.w %d5
m68k_02631a_end:
.org 0x2631C
m68k_02631c:
        bmi.w (. + 86)
m68k_02631c_end:
.org 0x26320
m68k_026320:
        move.w %d5,0xf3a6:w
m68k_026320_end:
.org 0x26324
m68k_026324:
        bsr.w (. + 172)
m68k_026324_end:
.org 0x26328
m68k_026328:
        cmp.l 0xf69a:w,%d1
m68k_026328_end:
.org 0x2632C
m68k_02632c:
        bhi.w (. + 70)
m68k_02632c_end:
.org 0x26330
m68k_026330:
        lea.l 0xa754:w,%a0
m68k_026330_end:
.org 0x26334
m68k_026334:
        move.b #0x3,(%a0, %d7.w)
m68k_026334_end:
.org 0x2633A
m68k_02633a:
        move.w %d7,0xf3f2:w
m68k_02633a_end:
.org 0x2633E
m68k_02633e:
        move.w #0x5,0xf6d4:w
m68k_02633e_end:
.org 0x26344
m68k_026344:
        jsr 0x1a47a:l
m68k_026344_end:
.org 0x2634A
m68k_02634a:
        bcs.w (. + 32)
m68k_02634a_end:
.org 0x2634E
m68k_02634e:
        bchg.b #0x1,0xf6d7:w
m68k_02634e_end:
.org 0x26354
m68k_026354:
        move.w 0xf3a6:w,0xf3d0:w
m68k_026354_end:
.org 0x2635A
m68k_02635a:
        move.w #0x12d,0xf740:w
m68k_02635a_end:
.org 0x26360
m68k_026360:
        bsr.w (. + -636)
m68k_026360_end:
.org 0x26364
m68k_026364:
        bchg.b #0x1,0xf6d7:w
m68k_026364_end:
.org 0x2636A
m68k_02636a:
        ori.w #0x1,%sr
m68k_02636a_end:
.org 0x2636E
m68k_02636e:
        bra.w (. + 8)
m68k_02636e_end:
.org 0x26372
m68k_026372:
        andi.w #0xfffe,%sr
m68k_026372_end:
.org 0x26376
m68k_026376:
        rts
m68k_026376_end:
.org 0x26378
m68k_026378:
        jsr 0x1a438:l
m68k_026378_end:
.org 0x2637E
m68k_02637e:
        lea.l 0xd300:w,%a1
m68k_02637e_end:
.org 0x26382
m68k_026382:
        lea.l 0xa150:w,%a2
m68k_026382_end:
.org 0x26386
m68k_026386:
        lea.l 0xc800:w,%a3
m68k_026386_end:
.org 0x2638A
m68k_02638a:
        moveq #0,%d4
m68k_02638a_end:
.org 0x2638C
m68k_02638c:
        move.w #0xffff,%d5
m68k_02638c_end:
.org 0x26390
m68k_026390:
        move.w (%a1)+,%d3
m68k_026390_end:
.org 0x26392
m68k_026392:
        bmi.w (. + 60)
m68k_026392_end:
.org 0x26396
m68k_026396:
        andi.w #0xff,%d3
m68k_026396_end:
.org 0x2639A
m68k_02639a:
        move.w %d3,%d2
m68k_02639a_end:
.org 0x2639C
m68k_02639c:
        lsl.w #0x2,%d2
m68k_02639c_end:
.org 0x2639E
m68k_02639e:
        move.w (%a2, %d2.w),%d1
m68k_02639e_end:
.org 0x263A2
m68k_0263a2:
        lsr.w #0x7,%d1
m68k_0263a2_end:
.org 0x263A4
m68k_0263a4:
        move.w 0x2(%a2, %d2.w),%d2
m68k_0263a4_end:
.org 0x263A8
m68k_0263a8:
        lsr.w #0x7,%d2
m68k_0263a8_end:
.org 0x263AA
m68k_0263aa:
        jsr 0x1a44e:l
m68k_0263aa_end:
.org 0x263B0
m68k_0263b0:
        cmpi.b #0x1,%d0
m68k_0263b0_end:
.org 0x263B4
m68k_0263b4:
        bne.b (. + -36)
m68k_0263b4_end:
.org 0x263B6
m68k_0263b6:
        move.w %d3,%d0
m68k_0263b6_end:
.org 0x263B8
m68k_0263b8:
        jsr 0xbac8:l
m68k_0263b8_end:
.org 0x263BE
m68k_0263be:
        lsl.w #0x2,%d0
m68k_0263be_end:
.org 0x263C0
m68k_0263c0:
        mulu.w 0x2(%a3, %d0.w),%d1
m68k_0263c0_end:
.org 0x263C4
m68k_0263c4:
        cmp.l %d4,%d1
m68k_0263c4_end:
.org 0x263C6
m68k_0263c6:
        bls.b (. + -54)
m68k_0263c6_end:
.org 0x263C8
m68k_0263c8:
        move.l %d1,%d4
m68k_0263c8_end:
.org 0x263CA
m68k_0263ca:
        move.w %d3,%d5
m68k_0263ca_end:
.org 0x263CC
m68k_0263cc:
        bra.b (. + -60)
m68k_0263cc_end:
.org 0x263CE
m68k_0263ce:
        rts
m68k_0263ce_end:
.org 0x263D0
m68k_0263d0:
        jsr 0x83d4:l
m68k_0263d0_end:
.org 0x263D6
m68k_0263d6:
        andi.l #0xffff,%d0
m68k_0263d6_end:
.org 0x263DC
m68k_0263dc:
        move.l %d0,%d1
m68k_0263dc_end:
.org 0x263DE
m68k_0263de:
        lsl.l #0x2,%d0
m68k_0263de_end:
.org 0x263E0
m68k_0263e0:
        add.l %d1,%d0
m68k_0263e0_end:
.org 0x263E2
m68k_0263e2:
        lsl.l #0x1,%d0
m68k_0263e2_end:
.org 0x263E4
m68k_0263e4:
        add.l %d1,%d0
m68k_0263e4_end:
.org 0x263E6
m68k_0263e6:
        swap %d0
m68k_0263e6_end:
.org 0x263E8
m68k_0263e8:
        addi.w #0x14,%d0
m68k_0263e8_end:
.org 0x263EC
m68k_0263ec:
        lea.l 0xc800:w,%a0
m68k_0263ec_end:
.org 0x263F0
m68k_0263f0:
        move.w 0xf3a6:w,%d1
m68k_0263f0_end:
.org 0x263F4
m68k_0263f4:
        lsl.w #0x2,%d1
m68k_0263f4_end:
.org 0x263F6
m68k_0263f6:
        move.l (%a0, %d1.w),%d1
m68k_0263f6_end:
.org 0x263FA
m68k_0263fa:
        divu.w %d0,%d1
m68k_0263fa_end:
.org 0x263FC
m68k_0263fc:
        andi.l #0xffff,%d1
m68k_0263fc_end:
.org 0x26402
m68k_026402:
        move.l 0xf39e:w,%d1
m68k_026402_end:
.org 0x26406
m68k_026406:
        rts
m68k_026406_end:
.org 0x26408
m68k_026408:
        jsr 0x83d4:l
m68k_026408_end:
.org 0x2640E
m68k_02640e:
        andi.l #0xffff,%d0
m68k_02640e_end:
.org 0x26414
m68k_026414:
        lsl.l #0x2,%d0
m68k_026414_end:
.org 0x26416
m68k_026416:
        swap %d0
m68k_026416_end:
.org 0x26418
m68k_026418:
        cmpi.w #0x3,%d0
m68k_026418_end:
.org 0x2641C
m68k_02641c:
        beq.w (. + 104)
m68k_02641c_end:
.org 0x26420
m68k_026420:
        bsr.w (. + 106)
m68k_026420_end:
.org 0x26424
m68k_026424:
        bcc.w (. + 96)
m68k_026424_end:
.org 0x26428
m68k_026428:
        bsr.w (. + 168)
m68k_026428_end:
.org 0x2642C
m68k_02642c:
        tst.w %d5
m68k_02642c_end:
.org 0x2642E
m68k_02642e:
        bmi.w (. + 86)
m68k_02642e_end:
.org 0x26432
m68k_026432:
        move.w %d5,0xf3a6:w
m68k_026432_end:
.org 0x26436
m68k_026436:
        bsr.w (. + 242)
m68k_026436_end:
.org 0x2643A
m68k_02643a:
        cmp.l 0xf69a:w,%d1
m68k_02643a_end:
.org 0x2643E
m68k_02643e:
        bhi.w (. + 70)
m68k_02643e_end:
.org 0x26442
m68k_026442:
        lea.l 0xa754:w,%a0
m68k_026442_end:
.org 0x26446
m68k_026446:
        move.b #0x3,(%a0, %d7.w)
m68k_026446_end:
.org 0x2644C
m68k_02644c:
        move.w %d7,0xf3f2:w
m68k_02644c_end:
.org 0x26450
m68k_026450:
        move.w #0x1,0xf6d4:w
m68k_026450_end:
.org 0x26456
m68k_026456:
        jsr 0x1a47a:l
m68k_026456_end:
.org 0x2645C
m68k_02645c:
        bcs.w (. + 32)
m68k_02645c_end:
.org 0x26460
m68k_026460:
        bchg.b #0x1,0xf6d7:w
m68k_026460_end:
.org 0x26466
m68k_026466:
        move.w 0xf3a6:w,0xf3d0:w
m68k_026466_end:
.org 0x2646C
m68k_02646c:
        move.w #0x129,0xf740:w
m68k_02646c_end:
.org 0x26472
m68k_026472:
        bsr.w (. + -910)
m68k_026472_end:
.org 0x26476
m68k_026476:
        bchg.b #0x1,0xf6d7:w
m68k_026476_end:
.org 0x2647C
m68k_02647c:
        ori.w #0x1,%sr
m68k_02647c_end:
.org 0x26480
m68k_026480:
        bra.w (. + 8)
m68k_026480_end:
.org 0x26484
m68k_026484:
        andi.w #0xfffe,%sr
m68k_026484_end:
.org 0x26488
m68k_026488:
        rts
m68k_026488_end:
.org 0x2648A
m68k_02648a:
        jsr 0x1a438:l
m68k_02648a_end:
.org 0x26490
m68k_026490:
        lea.l 0xa150:w,%a1
m68k_026490_end:
.org 0x26494
m68k_026494:
        move.w %d7,%d0
m68k_026494_end:
.org 0x26496
m68k_026496:
        lsl.w #0x2,%d0
m68k_026496_end:
.org 0x26498
m68k_026498:
        move.w (%a1, %d0.w),%d1
m68k_026498_end:
.org 0x2649C
m68k_02649c:
        lsr.w #0x7,%d1
m68k_02649c_end:
.org 0x2649E
m68k_02649e:
        move.w 0x2(%a1, %d0.w),%d2
m68k_02649e_end:
.org 0x264A2
m68k_0264a2:
        lsr.w #0x7,%d2
m68k_0264a2_end:
.org 0x264A4
m68k_0264a4:
        jsr 0x1a44e:l
m68k_0264a4_end:
.org 0x264AA
m68k_0264aa:
        cmpi.b #0x0,%d0
m68k_0264aa_end:
.org 0x264AE
m68k_0264ae:
        beq.w (. + 28)
m68k_0264ae_end:
.org 0x264B2
m68k_0264b2:
        cmpi.b #0x4,%d0
m68k_0264b2_end:
.org 0x264B6
m68k_0264b6:
        beq.w (. + 20)
m68k_0264b6_end:
.org 0x264BA
m68k_0264ba:
        cmpi.b #0x8,%d0
m68k_0264ba_end:
.org 0x264BE
m68k_0264be:
        beq.w (. + 12)
m68k_0264be_end:
.org 0x264C2
m68k_0264c2:
        andi.w #0xfffe,%sr
m68k_0264c2_end:
.org 0x264C6
m68k_0264c6:
        bra.w (. + 8)
m68k_0264c6_end:
.org 0x264CA
m68k_0264ca:
        ori.w #0x1,%sr
m68k_0264ca_end:
.org 0x264CE
m68k_0264ce:
        rts
m68k_0264ce_end:
.org 0x264D0
m68k_0264d0:
        jsr 0x1a438:l
m68k_0264d0_end:
.org 0x264D6
m68k_0264d6:
        lea.l 0xd300:w,%a1
m68k_0264d6_end:
.org 0x264DA
m68k_0264da:
        lea.l 0xa150:w,%a2
m68k_0264da_end:
.org 0x264DE
m68k_0264de:
        lea.l 0xc800:w,%a3
m68k_0264de_end:
.org 0x264E2
m68k_0264e2:
        moveq #0,%d4
m68k_0264e2_end:
.org 0x264E4
m68k_0264e4:
        move.w #0xffff,%d5
m68k_0264e4_end:
.org 0x264E8
m68k_0264e8:
        move.w (%a1)+,%d3
m68k_0264e8_end:
.org 0x264EA
m68k_0264ea:
        bmi.w (. + 60)
m68k_0264ea_end:
.org 0x264EE
m68k_0264ee:
        andi.w #0xff,%d3
m68k_0264ee_end:
.org 0x264F2
m68k_0264f2:
        move.w %d3,%d2
m68k_0264f2_end:
.org 0x264F4
m68k_0264f4:
        lsl.w #0x2,%d2
m68k_0264f4_end:
.org 0x264F6
m68k_0264f6:
        move.w (%a2, %d2.w),%d1
m68k_0264f6_end:
.org 0x264FA
m68k_0264fa:
        lsr.w #0x7,%d1
m68k_0264fa_end:
.org 0x264FC
m68k_0264fc:
        move.w 0x2(%a2, %d2.w),%d2
m68k_0264fc_end:
.org 0x26500
m68k_026500:
        lsr.w #0x7,%d2
m68k_026500_end:
.org 0x26502
m68k_026502:
        jsr 0x1a44e:l
m68k_026502_end:
.org 0x26508
m68k_026508:
        cmpi.b #0x2,%d0
m68k_026508_end:
.org 0x2650C
m68k_02650c:
        bne.b (. + -36)
m68k_02650c_end:
.org 0x2650E
m68k_02650e:
        move.w %d3,%d0
m68k_02650e_end:
.org 0x26510
m68k_026510:
        jsr 0xbac8:l
m68k_026510_end:
.org 0x26516
m68k_026516:
        lsl.w #0x2,%d0
m68k_026516_end:
.org 0x26518
m68k_026518:
        mulu.w 0x2(%a3, %d0.w),%d1
m68k_026518_end:
.org 0x2651C
m68k_02651c:
        cmp.l %d4,%d1
m68k_02651c_end:
.org 0x2651E
m68k_02651e:
        bls.b (. + -54)
m68k_02651e_end:
.org 0x26520
m68k_026520:
        move.l %d1,%d4
m68k_026520_end:
.org 0x26522
m68k_026522:
        move.w %d3,%d5
m68k_026522_end:
.org 0x26524
m68k_026524:
        bra.b (. + -60)
m68k_026524_end:
.org 0x26526
m68k_026526:
        rts
m68k_026526_end:
.org 0x26528
m68k_026528:
        jsr 0x83d4:l
m68k_026528_end:
.org 0x2652E
m68k_02652e:
        andi.l #0xffff,%d0
m68k_02652e_end:
.org 0x26534
m68k_026534:
        move.l %d0,%d1
m68k_026534_end:
.org 0x26536
m68k_026536:
        lsl.l #0x2,%d0
m68k_026536_end:
.org 0x26538
m68k_026538:
        add.l %d1,%d0
m68k_026538_end:
.org 0x2653A
m68k_02653a:
        lsl.l #0x1,%d0
m68k_02653a_end:
.org 0x2653C
m68k_02653c:
        add.l %d1,%d0
m68k_02653c_end:
.org 0x2653E
m68k_02653e:
        swap %d0
m68k_02653e_end:
.org 0x26540
m68k_026540:
        addi.w #0x1e,%d0
m68k_026540_end:
.org 0x26544
m68k_026544:
        lea.l 0xc800:w,%a0
m68k_026544_end:
.org 0x26548
m68k_026548:
        move.w 0xf3a6:w,%d1
m68k_026548_end:
.org 0x2654C
m68k_02654c:
        lsl.w #0x2,%d1
m68k_02654c_end:
.org 0x2654E
m68k_02654e:
        move.l (%a0, %d1.w),%d1
m68k_02654e_end:
.org 0x26552
m68k_026552:
        divu.w %d0,%d1
m68k_026552_end:
.org 0x26554
m68k_026554:
        andi.l #0xffff,%d1
m68k_026554_end:
.org 0x2655A
m68k_02655a:
        move.l %d1,0xf39e:w
m68k_02655a_end:
.org 0x2655E
m68k_02655e:
        rts
m68k_02655e_end:
.org 0x26560
m68k_026560:
        move.w %d7,-(%a7)
m68k_026560_end:
.org 0x26562
m68k_026562:
        bsr.w (. + -12432)
m68k_026562_end:
.org 0x26566
m68k_026566:
        tst.w 0xd300:w
m68k_026566_end:
.org 0x2656A
m68k_02656a:
        bmi.w (. + 52)
m68k_02656a_end:
.org 0x2656E
m68k_02656e:
        bsr.w (. + 66)
m68k_02656e_end:
.org 0x26572
m68k_026572:
        bcs.w (. + 54)
m68k_026572_end:
.org 0x26576
m68k_026576:
        bsr.w (. + 354)
m68k_026576_end:
.org 0x2657A
m68k_02657a:
        bcs.w (. + 46)
m68k_02657a_end:
.org 0x2657E
m68k_02657e:
        bsr.w (. + 606)
m68k_02657e_end:
.org 0x26582
m68k_026582:
        bcs.w (. + 38)
m68k_026582_end:
.org 0x26586
m68k_026586:
        bsr.w (. + 882)
m68k_026586_end:
.org 0x2658A
m68k_02658a:
        bcs.w (. + 30)
m68k_02658a_end:
.org 0x2658E
m68k_02658e:
        bsr.w (. + 1048)
m68k_02658e_end:
.org 0x26592
m68k_026592:
        bcs.w (. + 22)
m68k_026592_end:
.org 0x26596
m68k_026596:
        bsr.w (. + 1302)
m68k_026596_end:
.org 0x2659A
m68k_02659a:
        bcs.w (. + 14)
m68k_02659a_end:
.org 0x2659E
m68k_02659e:
        move.w (%a7)+,%d7
m68k_02659e_end:
.org 0x265A0
m68k_0265a0:
        andi.w #0xfffe,%sr
m68k_0265a0_end:
.org 0x265A4
m68k_0265a4:
        bra.w (. + 10)
m68k_0265a4_end:
.org 0x265A8
m68k_0265a8:
        move.w (%a7)+,%d7
m68k_0265a8_end:
.org 0x265AA
m68k_0265aa:
        ori.w #0x1,%sr
m68k_0265aa_end:
.org 0x265AE
m68k_0265ae:
        rts
m68k_0265ae_end:
.org 0x265B0
m68k_0265b0:
        jsr 0x83d4:l
m68k_0265b0_end:
.org 0x265B6
m68k_0265b6:
        andi.l #0xffff,%d0
m68k_0265b6_end:
.org 0x265BC
m68k_0265bc:
        lsl.l #0x2,%d0
m68k_0265bc_end:
.org 0x265BE
m68k_0265be:
        swap %d0
m68k_0265be_end:
.org 0x265C0
m68k_0265c0:
        cmpi.w #0x3,%d0
m68k_0265c0_end:
.org 0x265C4
m68k_0265c4:
        beq.w (. + 110)
m68k_0265c4_end:
.org 0x265C8
m68k_0265c8:
        bsr.w (. + 202)
m68k_0265c8_end:
.org 0x265CC
m68k_0265cc:
        tst.w 0xd400:w
m68k_0265cc_end:
.org 0x265D0
m68k_0265d0:
        bmi.w (. + 98)
m68k_0265d0_end:
.org 0x265D4
m68k_0265d4:
        bsr.w (. + 100)
m68k_0265d4_end:
.org 0x265D8
m68k_0265d8:
        cmpi.b #0x32,%d0
m68k_0265d8_end:
.org 0x265DC
m68k_0265dc:
        bhi.w (. + 86)
m68k_0265dc_end:
.org 0x265E0
m68k_0265e0:
        move.w %d1,0xf3a6:w
m68k_0265e0_end:
.org 0x265E4
m68k_0265e4:
        bsr.w (. + 122)
m68k_0265e4_end:
.org 0x265E8
m68k_0265e8:
        cmp.l 0xf696:w,%d0
m68k_0265e8_end:
.org 0x265EC
m68k_0265ec:
        bhi.w (. + 70)
m68k_0265ec_end:
.org 0x265F0
m68k_0265f0:
        lea.l 0xa754:w,%a0
m68k_0265f0_end:
.org 0x265F4
m68k_0265f4:
        move.b #0x3,(%a0, %d7.w)
m68k_0265f4_end:
.org 0x265FA
m68k_0265fa:
        move.w %d7,0xf3f2:w
m68k_0265fa_end:
.org 0x265FE
m68k_0265fe:
        move.w #0x4,0xf6d4:w
m68k_0265fe_end:
.org 0x26604
m68k_026604:
        jsr 0x1a47a:l
m68k_026604_end:
.org 0x2660A
m68k_02660a:
        bcs.w (. + 32)
m68k_02660a_end:
.org 0x2660E
m68k_02660e:
        bchg.b #0x1,0xf6d7:w
m68k_02660e_end:
.org 0x26614
m68k_026614:
        move.w 0xf3a6:w,0xf3d0:w
m68k_026614_end:
.org 0x2661A
m68k_02661a:
        move.w #0x12c,0xf740:w
m68k_02661a_end:
.org 0x26620
m68k_026620:
        bsr.w (. + -1340)
m68k_026620_end:
.org 0x26624
m68k_026624:
        bchg.b #0x1,0xf6d7:w
m68k_026624_end:
.org 0x2662A
m68k_02662a:
        ori.w #0x1,%sr
m68k_02662a_end:
.org 0x2662E
m68k_02662e:
        bra.w (. + 8)
m68k_02662e_end:
.org 0x26632
m68k_026632:
        andi.w #0xfffe,%sr
m68k_026632_end:
.org 0x26636
m68k_026636:
        rts
m68k_026636_end:
.org 0x26638
m68k_026638:
        lea.l 0xc300:w,%a0
m68k_026638_end:
.org 0x2663C
m68k_02663c:
        lea.l 0xd400:w,%a1
m68k_02663c_end:
.org 0x26640
m68k_026640:
        move.w #0xffff,%d0
m68k_026640_end:
.org 0x26644
m68k_026644:
        move.w (%a1)+,%d2
m68k_026644_end:
.org 0x26646
m68k_026646:
        bmi.w (. + 22)
m68k_026646_end:
.org 0x2664A
m68k_02664a:
        andi.w #0xff,%d2
m68k_02664a_end:
.org 0x2664E
m68k_02664e:
        move.b (%a0, %d2.w),%d3
m68k_02664e_end:
.org 0x26652
m68k_026652:
        cmp.b %d0,%d3
m68k_026652_end:
.org 0x26654
m68k_026654:
        bcc.b (. + -16)
m68k_026654_end:
.org 0x26656
m68k_026656:
        move.b %d3,%d0
m68k_026656_end:
.org 0x26658
m68k_026658:
        move.w %d2,%d1
m68k_026658_end:
.org 0x2665A
m68k_02665a:
        bra.b (. + -22)
m68k_02665a_end:
.org 0x2665C
m68k_02665c:
        rts
m68k_02665c_end:
.org 0x2665E
m68k_02665e:
        lea.l 0xb400:w,%a0
m68k_02665e_end:
.org 0x26662
m68k_026662:
        move.w 0xf3a6:w,%d0
m68k_026662_end:
.org 0x26666
m68k_026666:
        lsl.w #0x1,%d0
m68k_026666_end:
.org 0x26668
m68k_026668:
        move.w (%a0, %d0.w),%d2
m68k_026668_end:
.org 0x2666C
m68k_02666c:
        lea.l 0xb600:w,%a0
m68k_02666c_end:
.org 0x26670
m68k_026670:
        add.w (%a0, %d0.w),%d2
m68k_026670_end:
.org 0x26674
m68k_026674:
        jsr 0x83d4:l
m68k_026674_end:
.org 0x2667A
m68k_02667a:
        andi.l #0xffff,%d0
m68k_02667a_end:
.org 0x26680
m68k_026680:
        move.l %d0,%d1
m68k_026680_end:
.org 0x26682
m68k_026682:
        lsl.l #0x2,%d0
m68k_026682_end:
.org 0x26684
m68k_026684:
        add.l %d1,%d0
m68k_026684_end:
.org 0x26686
m68k_026686:
        swap %d0
m68k_026686_end:
.org 0x26688
m68k_026688:
        addq.w #0x8,%d0
m68k_026688_end:
.org 0x2668A
m68k_02668a:
        mulu.w %d2,%d0
m68k_02668a_end:
.org 0x2668C
m68k_02668c:
        move.l %d0,0xf39e:w
m68k_02668c_end:
.org 0x26690
m68k_026690:
        rts
m68k_026690_end:
.org 0x26692
m68k_026692:
        jsr 0x1a438:l
m68k_026692_end:
.org 0x26698
m68k_026698:
        lea.l 0xd300:w,%a1
m68k_026698_end:
.org 0x2669C
m68k_02669c:
        lea.l 0xc800:w,%a2
m68k_02669c_end:
.org 0x266A0
m68k_0266a0:
        lea.l 0xa150:w,%a3
m68k_0266a0_end:
.org 0x266A4
m68k_0266a4:
        lea.l 0xd400:w,%a4
m68k_0266a4_end:
.org 0x266A8
m68k_0266a8:
        move.w (%a1)+,%d3
m68k_0266a8_end:
.org 0x266AA
m68k_0266aa:
        bmi.w (. + 40)
m68k_0266aa_end:
.org 0x266AE
m68k_0266ae:
        andi.w #0xff,%d3
m68k_0266ae_end:
.org 0x266B2
m68k_0266b2:
        move.w %d3,%d2
m68k_0266b2_end:
.org 0x266B4
m68k_0266b4:
        lsl.w #0x2,%d2
m68k_0266b4_end:
.org 0x266B6
m68k_0266b6:
        move.w (%a3, %d2.w),%d1
m68k_0266b6_end:
.org 0x266BA
m68k_0266ba:
        lsr.w #0x7,%d1
m68k_0266ba_end:
.org 0x266BC
m68k_0266bc:
        move.w 0x2(%a3, %d2.w),%d2
m68k_0266bc_end:
.org 0x266C0
m68k_0266c0:
        lsr.w #0x7,%d2
m68k_0266c0_end:
.org 0x266C2
m68k_0266c2:
        jsr 0x1a44e:l
m68k_0266c2_end:
.org 0x266C8
m68k_0266c8:
        cmpi.b #0x6,%d0
m68k_0266c8_end:
.org 0x266CC
m68k_0266cc:
        beq.b (. + -36)
m68k_0266cc_end:
.org 0x266CE
m68k_0266ce:
        move.w %d3,(%a4)+
m68k_0266ce_end:
.org 0x266D0
m68k_0266d0:
        bra.b (. + -40)
m68k_0266d0_end:
.org 0x266D2
m68k_0266d2:
        move.w #0xffff,(%a4)
m68k_0266d2_end:
.org 0x266D6
m68k_0266d6:
        rts
m68k_0266d6_end:
.org 0x266D8
m68k_0266d8:
        jsr 0x83d4:l
m68k_0266d8_end:
.org 0x266DE
m68k_0266de:
        andi.l #0xffff,%d0
m68k_0266de_end:
.org 0x266E4
m68k_0266e4:
        lsl.l #0x2,%d0
m68k_0266e4_end:
.org 0x266E6
m68k_0266e6:
        swap %d0
m68k_0266e6_end:
.org 0x266E8
m68k_0266e8:
        cmpi.w #0x3,%d0
m68k_0266e8_end:
.org 0x266EC
m68k_0266ec:
        beq.w (. + 96)
m68k_0266ec_end:
.org 0x266F0
m68k_0266f0:
        bsr.w (. + 98)
m68k_0266f0_end:
.org 0x266F4
m68k_0266f4:
        tst.w %d5
m68k_0266f4_end:
.org 0x266F6
m68k_0266f6:
        bmi.w (. + 86)
m68k_0266f6_end:
.org 0x266FA
m68k_0266fa:
        move.w %d5,0xf3a6:w
m68k_0266fa_end:
.org 0x266FE
m68k_0266fe:
        bsr.w (. + 172)
m68k_0266fe_end:
.org 0x26702
m68k_026702:
        cmp.l 0xf696:w,%d2
m68k_026702_end:
.org 0x26706
m68k_026706:
        bhi.w (. + 70)
m68k_026706_end:
.org 0x2670A
m68k_02670a:
        lea.l 0xa754:w,%a0
m68k_02670a_end:
.org 0x2670E
m68k_02670e:
        move.b #0x3,(%a0, %d7.w)
m68k_02670e_end:
.org 0x26714
m68k_026714:
        move.w %d7,0xf3f2:w
m68k_026714_end:
.org 0x26718
m68k_026718:
        move.w #0x3,0xf6d4:w
m68k_026718_end:
.org 0x2671E
m68k_02671e:
        jsr 0x1a47a:l
m68k_02671e_end:
.org 0x26724
m68k_026724:
        bcs.w (. + 32)
m68k_026724_end:
.org 0x26728
m68k_026728:
        bchg.b #0x1,0xf6d7:w
m68k_026728_end:
.org 0x2672E
m68k_02672e:
        move.w 0xf3a6:w,0xf3d0:w
m68k_02672e_end:
.org 0x26734
m68k_026734:
        move.w #0x12b,0xf740:w
m68k_026734_end:
.org 0x2673A
m68k_02673a:
        bsr.w (. + -1622)
m68k_02673a_end:
.org 0x2673E
m68k_02673e:
        bchg.b #0x1,0xf6d7:w
m68k_02673e_end:
.org 0x26744
m68k_026744:
        ori.w #0x1,%sr
m68k_026744_end:
.org 0x26748
m68k_026748:
        bra.w (. + 8)
m68k_026748_end:
.org 0x2674C
m68k_02674c:
        andi.w #0xfffe,%sr
m68k_02674c_end:
.org 0x26750
m68k_026750:
        rts
m68k_026750_end:
.org 0x26752
m68k_026752:
        jsr 0x1a438:l
m68k_026752_end:
.org 0x26758
m68k_026758:
        lea.l 0xd300:w,%a1
m68k_026758_end:
.org 0x2675C
m68k_02675c:
        lea.l 0xc800:w,%a2
m68k_02675c_end:
.org 0x26760
m68k_026760:
        lea.l 0xa150:w,%a3
m68k_026760_end:
.org 0x26764
m68k_026764:
        moveq #0,%d4
m68k_026764_end:
.org 0x26766
m68k_026766:
        move.w #0xffff,%d5
m68k_026766_end:
.org 0x2676A
m68k_02676a:
        move.w (%a1)+,%d3
m68k_02676a_end:
.org 0x2676C
m68k_02676c:
        bmi.w (. + 60)
m68k_02676c_end:
.org 0x26770
m68k_026770:
        andi.w #0xff,%d3
m68k_026770_end:
.org 0x26774
m68k_026774:
        move.w %d3,%d2
m68k_026774_end:
.org 0x26776
m68k_026776:
        lsl.w #0x2,%d2
m68k_026776_end:
.org 0x26778
m68k_026778:
        move.w (%a3, %d2.w),%d1
m68k_026778_end:
.org 0x2677C
m68k_02677c:
        lsr.w #0x7,%d1
m68k_02677c_end:
.org 0x2677E
m68k_02677e:
        move.w 0x2(%a3, %d2.w),%d2
m68k_02677e_end:
.org 0x26782
m68k_026782:
        lsr.w #0x7,%d2
m68k_026782_end:
.org 0x26784
m68k_026784:
        jsr 0x1a44e:l
m68k_026784_end:
.org 0x2678A
m68k_02678a:
        cmpi.b #0x6,%d0
m68k_02678a_end:
.org 0x2678E
m68k_02678e:
        bne.b (. + -36)
m68k_02678e_end:
.org 0x26790
m68k_026790:
        move.w %d3,%d0
m68k_026790_end:
.org 0x26792
m68k_026792:
        jsr 0xbac8:l
m68k_026792_end:
.org 0x26798
m68k_026798:
        lsl.w #0x2,%d0
m68k_026798_end:
.org 0x2679A
m68k_02679a:
        mulu.w 0x2(%a2, %d0.w),%d1
m68k_02679a_end:
.org 0x2679E
m68k_02679e:
        cmp.l %d4,%d1
m68k_02679e_end:
.org 0x267A0
m68k_0267a0:
        bls.b (. + -54)
m68k_0267a0_end:
.org 0x267A2
m68k_0267a2:
        move.l %d1,%d4
m68k_0267a2_end:
.org 0x267A4
m68k_0267a4:
        move.w %d3,%d5
m68k_0267a4_end:
.org 0x267A6
m68k_0267a6:
        bra.b (. + -60)
m68k_0267a6_end:
.org 0x267A8
m68k_0267a8:
        rts
m68k_0267a8_end:
.org 0x267AA
m68k_0267aa:
        lea.l 0xc800:w,%a0
m68k_0267aa_end:
.org 0x267AE
m68k_0267ae:
        lsl.w #0x2,%d5
m68k_0267ae_end:
.org 0x267B0
m68k_0267b0:
        move.l (%a0, %d5.w),%d2
m68k_0267b0_end:
.org 0x267B4
m68k_0267b4:
        jsr 0x83d4:l
m68k_0267b4_end:
.org 0x267BA
m68k_0267ba:
        andi.l #0xffff,%d0
m68k_0267ba_end:
.org 0x267C0
m68k_0267c0:
        lsl.l #0x2,%d0
m68k_0267c0_end:
.org 0x267C2
m68k_0267c2:
        add.l %d1,%d0
m68k_0267c2_end:
.org 0x267C4
m68k_0267c4:
        lsl.l #0x1,%d0
m68k_0267c4_end:
.org 0x267C6
m68k_0267c6:
        add.l %d1,%d0
m68k_0267c6_end:
.org 0x267C8
m68k_0267c8:
        swap %d0
m68k_0267c8_end:
.org 0x267CA
m68k_0267ca:
        addi.w #0x28,%d0
m68k_0267ca_end:
.org 0x267CE
m68k_0267ce:
        divu.w %d0,%d2
m68k_0267ce_end:
.org 0x267D0
m68k_0267d0:
        andi.l #0xffff,%d2
m68k_0267d0_end:
.org 0x267D6
m68k_0267d6:
        move.l %d2,0xf39e:w
m68k_0267d6_end:
.org 0x267DA
m68k_0267da:
        rts
m68k_0267da_end:
.org 0x267DC
m68k_0267dc:
        jsr 0x83d4:l
m68k_0267dc_end:
.org 0x267E2
m68k_0267e2:
        andi.l #0xffff,%d0
m68k_0267e2_end:
.org 0x267E8
m68k_0267e8:
        lsl.l #0x2,%d0
m68k_0267e8_end:
.org 0x267EA
m68k_0267ea:
        swap %d0
m68k_0267ea_end:
.org 0x267EC
m68k_0267ec:
        cmpi.w #0x3,%d0
m68k_0267ec_end:
.org 0x267F0
m68k_0267f0:
        beq.w (. + 94)
m68k_0267f0_end:
.org 0x267F4
m68k_0267f4:
        bsr.w (. + 96)
m68k_0267f4_end:
.org 0x267F8
m68k_0267f8:
        tst.w %d5
m68k_0267f8_end:
.org 0x267FA
m68k_0267fa:
        bmi.w (. + 84)
m68k_0267fa_end:
.org 0x267FE
m68k_0267fe:
        move.w %d5,0xf3a6:w
m68k_0267fe_end:
.org 0x26802
m68k_026802:
        bsr.w (. + 194)
m68k_026802_end:
.org 0x26806
m68k_026806:
        cmp.l 0xf696:w,%d2
m68k_026806_end:
.org 0x2680A
m68k_02680a:
        bhi.w (. + 68)
m68k_02680a_end:
.org 0x2680E
m68k_02680e:
        lea.l 0xa754:w,%a0
m68k_02680e_end:
.org 0x26812
m68k_026812:
        move.b #0x3,(%a0, %d7.w)
m68k_026812_end:
.org 0x26818
m68k_026818:
        move.w %d7,0xf3f2:w
m68k_026818_end:
.org 0x2681C
m68k_02681c:
        clr.w 0xf6d4:w
m68k_02681c_end:
.org 0x26820
m68k_026820:
        jsr 0x1a47a:l
m68k_026820_end:
.org 0x26826
m68k_026826:
        bcs.w (. + 32)
m68k_026826_end:
.org 0x2682A
m68k_02682a:
        bchg.b #0x1,0xf6d7:w
m68k_02682a_end:
.org 0x26830
m68k_026830:
        move.w 0xf3a6:w,0xf3d0:w
m68k_026830_end:
.org 0x26836
m68k_026836:
        move.w #0x128,0xf740:w
m68k_026836_end:
.org 0x2683C
m68k_02683c:
        bsr.w (. + -1880)
m68k_02683c_end:
.org 0x26840
m68k_026840:
        bchg.b #0x1,0xf6d7:w
m68k_026840_end:
.org 0x26846
m68k_026846:
        ori.w #0x1,%sr
m68k_026846_end:
.org 0x2684A
m68k_02684a:
        bra.w (. + 8)
m68k_02684a_end:
.org 0x2684E
m68k_02684e:
        andi.w #0xfffe,%sr
m68k_02684e_end:
.org 0x26852
m68k_026852:
        rts
m68k_026852_end:
.org 0x26854
m68k_026854:
        jsr 0x1a438:l
m68k_026854_end:
.org 0x2685A
m68k_02685a:
        lea.l 0xd300:w,%a1
m68k_02685a_end:
.org 0x2685E
m68k_02685e:
        lea.l 0xa150:w,%a2
m68k_02685e_end:
.org 0x26862
m68k_026862:
        lea.l 0xc800:w,%a3
m68k_026862_end:
.org 0x26866
m68k_026866:
        moveq #0,%d4
m68k_026866_end:
.org 0x26868
m68k_026868:
        move.w #0xffff,%d5
m68k_026868_end:
.org 0x2686C
m68k_02686c:
        move.w (%a1)+,%d3
m68k_02686c_end:
.org 0x2686E
m68k_02686e:
        bmi.w (. + 84)
m68k_02686e_end:
.org 0x26872
m68k_026872:
        andi.w #0xff,%d3
m68k_026872_end:
.org 0x26876
m68k_026876:
        move.w %d3,%d2
m68k_026876_end:
.org 0x26878
m68k_026878:
        lsl.w #0x2,%d2
m68k_026878_end:
.org 0x2687A
m68k_02687a:
        move.w (%a2, %d2.w),%d1
m68k_02687a_end:
.org 0x2687E
m68k_02687e:
        lsr.w #0x7,%d1
m68k_02687e_end:
.org 0x26880
m68k_026880:
        move.w 0x2(%a2, %d2.w),%d2
m68k_026880_end:
.org 0x26884
m68k_026884:
        lsr.w #0x7,%d2
m68k_026884_end:
.org 0x26886
m68k_026886:
        jsr 0x1a44e:l
m68k_026886_end:
.org 0x2688C
m68k_02688c:
        cmpi.b #0x0,%d0
m68k_02688c_end:
.org 0x26890
m68k_026890:
        beq.w (. + 26)
m68k_026890_end:
.org 0x26894
m68k_026894:
        cmpi.b #0x3,%d0
m68k_026894_end:
.org 0x26898
m68k_026898:
        beq.w (. + 18)
m68k_026898_end:
.org 0x2689C
m68k_02689c:
        cmpi.b #0x7,%d0
m68k_02689c_end:
.org 0x268A0
m68k_0268a0:
        beq.w (. + 10)
m68k_0268a0_end:
.org 0x268A4
m68k_0268a4:
        cmpi.b #0x1,%d0
m68k_0268a4_end:
.org 0x268A8
m68k_0268a8:
        bne.b (. + -60)
m68k_0268a8_end:
.org 0x268AA
m68k_0268aa:
        move.w %d3,%d0
m68k_0268aa_end:
.org 0x268AC
m68k_0268ac:
        jsr 0xbac8:l
m68k_0268ac_end:
.org 0x268B2
m68k_0268b2:
        lsl.w #0x2,%d0
m68k_0268b2_end:
.org 0x268B4
m68k_0268b4:
        mulu.w 0x2(%a3, %d0.w),%d1
m68k_0268b4_end:
.org 0x268B8
m68k_0268b8:
        cmp.l %d4,%d1
m68k_0268b8_end:
.org 0x268BA
m68k_0268ba:
        bls.b (. + -78)
m68k_0268ba_end:
.org 0x268BC
m68k_0268bc:
        move.l %d1,%d4
m68k_0268bc_end:
.org 0x268BE
m68k_0268be:
        move.w %d3,%d5
m68k_0268be_end:
.org 0x268C0
m68k_0268c0:
        bra.b (. + -84)
m68k_0268c0_end:
.org 0x268C2
m68k_0268c2:
        rts
m68k_0268c2_end:
.org 0x268C4
m68k_0268c4:
        lea.l 0xc800:w,%a0
m68k_0268c4_end:
.org 0x268C8
m68k_0268c8:
        lsl.w #0x2,%d5
m68k_0268c8_end:
.org 0x268CA
m68k_0268ca:
        move.l (%a0, %d5.w),%d2
m68k_0268ca_end:
.org 0x268CE
m68k_0268ce:
        jsr 0x83d4:l
m68k_0268ce_end:
.org 0x268D4
m68k_0268d4:
        andi.l #0xffff,%d0
m68k_0268d4_end:
.org 0x268DA
m68k_0268da:
        move.l %d0,%d1
m68k_0268da_end:
.org 0x268DC
m68k_0268dc:
        lsl.l #0x2,%d0
m68k_0268dc_end:
.org 0x268DE
m68k_0268de:
        add.l %d1,%d0
m68k_0268de_end:
.org 0x268E0
m68k_0268e0:
        lsl.l #0x1,%d0
m68k_0268e0_end:
.org 0x268E2
m68k_0268e2:
        add.l %d1,%d0
m68k_0268e2_end:
.org 0x268E4
m68k_0268e4:
        swap %d0
m68k_0268e4_end:
.org 0x268E6
m68k_0268e6:
        addi.w #0x14,%d0
m68k_0268e6_end:
.org 0x268EA
m68k_0268ea:
        divu.w %d0,%d2
m68k_0268ea_end:
.org 0x268EC
m68k_0268ec:
        andi.l #0xffff,%d2
m68k_0268ec_end:
.org 0x268F2
m68k_0268f2:
        move.l %d2,0xf39e:w
m68k_0268f2_end:
.org 0x268F6
m68k_0268f6:
        rts
m68k_0268f6_end:
.org 0x268F8
m68k_0268f8:
        jsr 0x83d4:l
m68k_0268f8_end:
.org 0x268FE
m68k_0268fe:
        andi.l #0xffff,%d0
m68k_0268fe_end:
.org 0x26904
m68k_026904:
        lsl.l #0x2,%d0
m68k_026904_end:
.org 0x26906
m68k_026906:
        swap %d0
m68k_026906_end:
.org 0x26908
m68k_026908:
        cmpi.w #0x3,%d0
m68k_026908_end:
.org 0x2690C
m68k_02690c:
        beq.w (. + 96)
m68k_02690c_end:
.org 0x26910
m68k_026910:
        bsr.w (. + -188)
m68k_026910_end:
.org 0x26914
m68k_026914:
        tst.w %d5
m68k_026914_end:
.org 0x26916
m68k_026916:
        bmi.w (. + 86)
m68k_026916_end:
.org 0x2691A
m68k_02691a:
        move.w %d5,0xf3a6:w
m68k_02691a_end:
.org 0x2691E
m68k_02691e:
        bsr.w (. + 84)
m68k_02691e_end:
.org 0x26922
m68k_026922:
        cmp.l 0xf696:w,%d2
m68k_026922_end:
.org 0x26926
m68k_026926:
        bhi.w (. + 70)
m68k_026926_end:
.org 0x2692A
m68k_02692a:
        lea.l 0xa754:w,%a0
m68k_02692a_end:
.org 0x2692E
m68k_02692e:
        move.b #0x3,(%a0, %d7.w)
m68k_02692e_end:
.org 0x26934
m68k_026934:
        move.w %d7,0xf3f2:w
m68k_026934_end:
.org 0x26938
m68k_026938:
        move.w #0x2,0xf6d4:w
m68k_026938_end:
.org 0x2693E
m68k_02693e:
        jsr 0x1a47a:l
m68k_02693e_end:
.org 0x26944
m68k_026944:
        bcs.w (. + 32)
m68k_026944_end:
.org 0x26948
m68k_026948:
        bchg.b #0x1,0xf6d7:w
m68k_026948_end:
.org 0x2694E
m68k_02694e:
        move.w 0xf3a6:w,0xf3d0:w
m68k_02694e_end:
.org 0x26954
m68k_026954:
        move.w #0x12a,0xf740:w
m68k_026954_end:
.org 0x2695A
m68k_02695a:
        bsr.w (. + -2166)
m68k_02695a_end:
.org 0x2695E
m68k_02695e:
        bchg.b #0x1,0xf6d7:w
m68k_02695e_end:
.org 0x26964
m68k_026964:
        ori.w #0x1,%sr
m68k_026964_end:
.org 0x26968
m68k_026968:
        bra.w (. + 8)
m68k_026968_end:
.org 0x2696C
m68k_02696c:
        andi.w #0xfffe,%sr
m68k_02696c_end:
.org 0x26970
m68k_026970:
        rts
m68k_026970_end:
.org 0x26972
m68k_026972:
        lea.l 0xc800:w,%a0
m68k_026972_end:
.org 0x26976
m68k_026976:
        lsl.w #0x2,%d5
m68k_026976_end:
.org 0x26978
m68k_026978:
        move.l (%a0, %d5.w),%d2
m68k_026978_end:
.org 0x2697C
m68k_02697c:
        jsr 0x83d4:l
m68k_02697c_end:
.org 0x26982
m68k_026982:
        andi.l #0xffff,%d0
m68k_026982_end:
.org 0x26988
m68k_026988:
        move.l %d0,%d1
m68k_026988_end:
.org 0x2698A
m68k_02698a:
        lsl.l #0x2,%d0
m68k_02698a_end:
.org 0x2698C
m68k_02698c:
        add.l %d1,%d0
m68k_02698c_end:
.org 0x2698E
m68k_02698e:
        lsl.l #0x1,%d0
m68k_02698e_end:
.org 0x26990
m68k_026990:
        add.l %d1,%d0
m68k_026990_end:
.org 0x26992
m68k_026992:
        swap %d0
m68k_026992_end:
.org 0x26994
m68k_026994:
        addi.w #0x1e,%d0
m68k_026994_end:
.org 0x26998
m68k_026998:
        divu.w %d0,%d2
m68k_026998_end:
.org 0x2699A
m68k_02699a:
        andi.l #0xffff,%d2
m68k_02699a_end:
.org 0x269A0
m68k_0269a0:
        move.l %d2,0xf39e:w
m68k_0269a0_end:
.org 0x269A4
m68k_0269a4:
        rts
m68k_0269a4_end:
.org 0x269A6
m68k_0269a6:
        jsr 0x83d4:l
m68k_0269a6_end:
.org 0x269AC
m68k_0269ac:
        andi.l #0xffff,%d0
m68k_0269ac_end:
.org 0x269B2
m68k_0269b2:
        lsl.l #0x2,%d0
m68k_0269b2_end:
.org 0x269B4
m68k_0269b4:
        swap %d0
m68k_0269b4_end:
.org 0x269B6
m68k_0269b6:
        cmpi.w #0x3,%d0
m68k_0269b6_end:
.org 0x269BA
m68k_0269ba:
        beq.w (. + 96)
m68k_0269ba_end:
.org 0x269BE
m68k_0269be:
        bsr.w (. + 98)
m68k_0269be_end:
.org 0x269C2
m68k_0269c2:
        tst.w %d5
m68k_0269c2_end:
.org 0x269C4
m68k_0269c4:
        bmi.w (. + 86)
m68k_0269c4_end:
.org 0x269C8
m68k_0269c8:
        move.w %d5,0xf3a6:w
m68k_0269c8_end:
.org 0x269CC
m68k_0269cc:
        bsr.w (. + 172)
m68k_0269cc_end:
.org 0x269D0
m68k_0269d0:
        cmp.l 0xf696:w,%d2
m68k_0269d0_end:
.org 0x269D4
m68k_0269d4:
        bhi.w (. + 70)
m68k_0269d4_end:
.org 0x269D8
m68k_0269d8:
        lea.l 0xa754:w,%a0
m68k_0269d8_end:
.org 0x269DC
m68k_0269dc:
        move.b #0x3,(%a0, %d7.w)
m68k_0269dc_end:
.org 0x269E2
m68k_0269e2:
        move.w %d7,0xf3f2:w
m68k_0269e2_end:
.org 0x269E6
m68k_0269e6:
        move.w #0x5,0xf6d4:w
m68k_0269e6_end:
.org 0x269EC
m68k_0269ec:
        jsr 0x1a47a:l
m68k_0269ec_end:
.org 0x269F2
m68k_0269f2:
        bcs.w (. + 32)
m68k_0269f2_end:
.org 0x269F6
m68k_0269f6:
        bchg.b #0x1,0xf6d7:w
m68k_0269f6_end:
.org 0x269FC
m68k_0269fc:
        move.w 0xf3a6:w,0xf3d0:w
m68k_0269fc_end:
.org 0x26A02
m68k_026a02:
        move.w #0x12d,0xf740:w
m68k_026a02_end:
.org 0x26A08
m68k_026a08:
        bsr.w (. + -2340)
m68k_026a08_end:
.org 0x26A0C
m68k_026a0c:
        bchg.b #0x1,0xf6d7:w
m68k_026a0c_end:
.org 0x26A12
m68k_026a12:
        ori.w #0x1,%sr
m68k_026a12_end:
.org 0x26A16
m68k_026a16:
        bra.w (. + 8)
m68k_026a16_end:
.org 0x26A1A
m68k_026a1a:
        andi.w #0xfffe,%sr
m68k_026a1a_end:
.org 0x26A1E
m68k_026a1e:
        rts
m68k_026a1e_end:
.org 0x26A20
m68k_026a20:
        jsr 0x1a438:l
m68k_026a20_end:
.org 0x26A26
m68k_026a26:
        lea.l 0xd300:w,%a1
m68k_026a26_end:
.org 0x26A2A
m68k_026a2a:
        lea.l 0xa150:w,%a2
m68k_026a2a_end:
.org 0x26A2E
m68k_026a2e:
        lea.l 0xc800:w,%a3
m68k_026a2e_end:
.org 0x26A32
m68k_026a32:
        moveq #0,%d4
m68k_026a32_end:
.org 0x26A34
m68k_026a34:
        move.w #0xffff,%d5
m68k_026a34_end:
.org 0x26A38
m68k_026a38:
        move.w (%a1)+,%d3
m68k_026a38_end:
.org 0x26A3A
m68k_026a3a:
        bmi.w (. + 60)
m68k_026a3a_end:
.org 0x26A3E
m68k_026a3e:
        andi.w #0xff,%d3
m68k_026a3e_end:
.org 0x26A42
m68k_026a42:
        move.w %d3,%d2
m68k_026a42_end:
.org 0x26A44
m68k_026a44:
        lsl.w #0x2,%d2
m68k_026a44_end:
.org 0x26A46
m68k_026a46:
        move.w (%a2, %d2.w),%d1
m68k_026a46_end:
.org 0x26A4A
m68k_026a4a:
        lsr.w #0x7,%d1
m68k_026a4a_end:
.org 0x26A4C
m68k_026a4c:
        move.w 0x2(%a2, %d2.w),%d2
m68k_026a4c_end:
.org 0x26A50
m68k_026a50:
        lsr.w #0x7,%d2
m68k_026a50_end:
.org 0x26A52
m68k_026a52:
        jsr 0x1a44e:l
m68k_026a52_end:
.org 0x26A58
m68k_026a58:
        cmpi.b #0x1,%d0
m68k_026a58_end:
.org 0x26A5C
m68k_026a5c:
        bne.b (. + -36)
m68k_026a5c_end:
.org 0x26A5E
m68k_026a5e:
        move.w %d3,%d0
m68k_026a5e_end:
.org 0x26A60
m68k_026a60:
        jsr 0xbac8:l
m68k_026a60_end:
.org 0x26A66
m68k_026a66:
        lsl.w #0x2,%d0
m68k_026a66_end:
.org 0x26A68
m68k_026a68:
        mulu.w 0x2(%a3, %d0.w),%d1
m68k_026a68_end:
.org 0x26A6C
m68k_026a6c:
        cmp.l %d4,%d1
m68k_026a6c_end:
.org 0x26A6E
m68k_026a6e:
        bls.b (. + -54)
m68k_026a6e_end:
.org 0x26A70
m68k_026a70:
        move.l %d1,%d4
m68k_026a70_end:
.org 0x26A72
m68k_026a72:
        move.w %d3,%d5
m68k_026a72_end:
.org 0x26A74
m68k_026a74:
        bra.b (. + -60)
m68k_026a74_end:
.org 0x26A76
m68k_026a76:
        rts
m68k_026a76_end:
.org 0x26A78
m68k_026a78:
        lea.l 0xc800:w,%a0
m68k_026a78_end:
.org 0x26A7C
m68k_026a7c:
        lsl.w #0x2,%d5
m68k_026a7c_end:
.org 0x26A7E
m68k_026a7e:
        move.l (%a0, %d5.w),%d2
m68k_026a7e_end:
.org 0x26A82
m68k_026a82:
        jsr 0x83d4:l
m68k_026a82_end:
.org 0x26A88
m68k_026a88:
        andi.l #0xffff,%d0
m68k_026a88_end:
.org 0x26A8E
m68k_026a8e:
        move.l %d0,%d1
m68k_026a8e_end:
.org 0x26A90
m68k_026a90:
        lsl.l #0x2,%d0
m68k_026a90_end:
.org 0x26A92
m68k_026a92:
        add.l %d1,%d0
m68k_026a92_end:
.org 0x26A94
m68k_026a94:
        lsl.l #0x1,%d0
m68k_026a94_end:
.org 0x26A96
m68k_026a96:
        add.l %d1,%d0
m68k_026a96_end:
.org 0x26A98
m68k_026a98:
        swap %d0
m68k_026a98_end:
.org 0x26A9A
m68k_026a9a:
        addi.w #0x14,%d0
m68k_026a9a_end:
.org 0x26A9E
m68k_026a9e:
        divu.w %d0,%d2
m68k_026a9e_end:
.org 0x26AA0
m68k_026aa0:
        andi.l #0xffff,%d2
m68k_026aa0_end:
.org 0x26AA6
m68k_026aa6:
        move.l %d2,0xf39e:w
m68k_026aa6_end:
.org 0x26AAA
m68k_026aaa:
        rts
m68k_026aaa_end:
.org 0x26AAC
m68k_026aac:
        jsr 0x83d4:l
m68k_026aac_end:
.org 0x26AB2
m68k_026ab2:
        andi.l #0xffff,%d0
m68k_026ab2_end:
.org 0x26AB8
m68k_026ab8:
        lsl.l #0x2,%d0
m68k_026ab8_end:
.org 0x26ABA
m68k_026aba:
        swap %d0
m68k_026aba_end:
.org 0x26ABC
m68k_026abc:
        cmpi.w #0x3,%d0
m68k_026abc_end:
.org 0x26AC0
m68k_026ac0:
        beq.w (. + 104)
m68k_026ac0_end:
.org 0x26AC4
m68k_026ac4:
        bsr.w (. + 106)
m68k_026ac4_end:
.org 0x26AC8
m68k_026ac8:
        bcs.w (. + 96)
m68k_026ac8_end:
.org 0x26ACC
m68k_026acc:
        bsr.w (. + 168)
m68k_026acc_end:
.org 0x26AD0
m68k_026ad0:
        tst.w %d5
m68k_026ad0_end:
.org 0x26AD2
m68k_026ad2:
        bmi.w (. + 86)
m68k_026ad2_end:
.org 0x26AD6
m68k_026ad6:
        move.w %d5,0xf3a6:w
m68k_026ad6_end:
.org 0x26ADA
m68k_026ada:
        bsr.w (. + 236)
m68k_026ada_end:
.org 0x26ADE
m68k_026ade:
        cmp.l 0xf696:w,%d2
m68k_026ade_end:
.org 0x26AE2
m68k_026ae2:
        bhi.w (. + 70)
m68k_026ae2_end:
.org 0x26AE6
m68k_026ae6:
        lea.l 0xa754:w,%a0
m68k_026ae6_end:
.org 0x26AEA
m68k_026aea:
        move.b #0x3,(%a0, %d7.w)
m68k_026aea_end:
.org 0x26AF0
m68k_026af0:
        move.w %d7,0xf3f2:w
m68k_026af0_end:
.org 0x26AF4
m68k_026af4:
        move.w #0x1,0xf6d4:w
m68k_026af4_end:
.org 0x26AFA
m68k_026afa:
        jsr 0x1a47a:l
m68k_026afa_end:
.org 0x26B00
m68k_026b00:
        bcs.w (. + 32)
m68k_026b00_end:
.org 0x26B04
m68k_026b04:
        bchg.b #0x1,0xf6d7:w
m68k_026b04_end:
.org 0x26B0A
m68k_026b0a:
        move.w 0xf3a6:w,0xf3d0:w
m68k_026b0a_end:
.org 0x26B10
m68k_026b10:
        move.w #0x129,0xf740:w
m68k_026b10_end:
.org 0x26B16
m68k_026b16:
        bsr.w (. + -2610)
m68k_026b16_end:
.org 0x26B1A
m68k_026b1a:
        bchg.b #0x1,0xf6d7:w
m68k_026b1a_end:
.org 0x26B20
m68k_026b20:
        ori.w #0x1,%sr
m68k_026b20_end:
.org 0x26B24
m68k_026b24:
        bra.w (. + 8)
m68k_026b24_end:
.org 0x26B28
m68k_026b28:
        andi.w #0xfffe,%sr
m68k_026b28_end:
.org 0x26B2C
m68k_026b2c:
        rts
m68k_026b2c_end:
.org 0x26B2E
m68k_026b2e:
        jsr 0x1a438:l
m68k_026b2e_end:
.org 0x26B34
m68k_026b34:
        lea.l 0xa150:w,%a1
m68k_026b34_end:
.org 0x26B38
m68k_026b38:
        move.w %d7,%d0
m68k_026b38_end:
.org 0x26B3A
m68k_026b3a:
        lsl.w #0x2,%d0
m68k_026b3a_end:
.org 0x26B3C
m68k_026b3c:
        move.w (%a0, %d0.w),%d1
m68k_026b3c_end:
.org 0x26B40
m68k_026b40:
        lsr.w #0x7,%d1
m68k_026b40_end:
.org 0x26B42
m68k_026b42:
        move.w 0x2(%a0, %d0.w),%d2
m68k_026b42_end:
.org 0x26B46
m68k_026b46:
        lsr.w #0x7,%d2
m68k_026b46_end:
.org 0x26B48
m68k_026b48:
        jsr 0x1a44e:l
m68k_026b48_end:
.org 0x26B4E
m68k_026b4e:
        cmpi.b #0x0,%d0
m68k_026b4e_end:
.org 0x26B52
m68k_026b52:
        beq.w (. + 28)
m68k_026b52_end:
.org 0x26B56
m68k_026b56:
        cmpi.b #0x4,%d0
m68k_026b56_end:
.org 0x26B5A
m68k_026b5a:
        beq.w (. + 20)
m68k_026b5a_end:
.org 0x26B5E
m68k_026b5e:
        cmpi.b #0x7,%d0
m68k_026b5e_end:
.org 0x26B62
m68k_026b62:
        beq.w (. + 12)
m68k_026b62_end:
.org 0x26B66
m68k_026b66:
        ori.w #0x1,%sr
m68k_026b66_end:
.org 0x26B6A
m68k_026b6a:
        bra.w (. + 8)
m68k_026b6a_end:
.org 0x26B6E
m68k_026b6e:
        andi.w #0xfffe,%sr
m68k_026b6e_end:
.org 0x26B72
m68k_026b72:
        rts
m68k_026b72_end:
.org 0x26B74
m68k_026b74:
        lea.l 0xd300:w,%a1
m68k_026b74_end:
.org 0x26B78
m68k_026b78:
        lea.l 0xa150:w,%a2
m68k_026b78_end:
.org 0x26B7C
m68k_026b7c:
        lea.l 0xc800:w,%a3
m68k_026b7c_end:
.org 0x26B80
m68k_026b80:
        moveq #0,%d4
m68k_026b80_end:
.org 0x26B82
m68k_026b82:
        move.w #0xffff,%d5
m68k_026b82_end:
.org 0x26B86
m68k_026b86:
        move.w (%a1)+,%d3
m68k_026b86_end:
.org 0x26B88
m68k_026b88:
        bmi.w (. + 60)
m68k_026b88_end:
.org 0x26B8C
m68k_026b8c:
        andi.w #0xff,%d3
m68k_026b8c_end:
.org 0x26B90
m68k_026b90:
        move.w %d3,%d2
m68k_026b90_end:
.org 0x26B92
m68k_026b92:
        lsl.w #0x2,%d2
m68k_026b92_end:
.org 0x26B94
m68k_026b94:
        move.w (%a2, %d2.w),%d1
m68k_026b94_end:
.org 0x26B98
m68k_026b98:
        lsr.w #0x7,%d1
m68k_026b98_end:
.org 0x26B9A
m68k_026b9a:
        move.w 0x2(%a2, %d2.w),%d2
m68k_026b9a_end:
.org 0x26B9E
m68k_026b9e:
        lsr.w #0x7,%d2
m68k_026b9e_end:
.org 0x26BA0
m68k_026ba0:
        jsr 0x1a44e:l
m68k_026ba0_end:
.org 0x26BA6
m68k_026ba6:
        cmpi.b #0x2,%d0
m68k_026ba6_end:
.org 0x26BAA
m68k_026baa:
        bne.b (. + -36)
m68k_026baa_end:
.org 0x26BAC
m68k_026bac:
        move.w %d3,%d0
m68k_026bac_end:
.org 0x26BAE
m68k_026bae:
        jsr 0xbac8:l
m68k_026bae_end:
.org 0x26BB4
m68k_026bb4:
        lsl.w #0x2,%d0
m68k_026bb4_end:
.org 0x26BB6
m68k_026bb6:
        mulu.w 0x2(%a3, %d0.w),%d1
m68k_026bb6_end:
.org 0x26BBA
m68k_026bba:
        cmp.l %d4,%d1
m68k_026bba_end:
.org 0x26BBC
m68k_026bbc:
        bls.b (. + -54)
m68k_026bbc_end:
.org 0x26BBE
m68k_026bbe:
        move.l %d1,%d4
m68k_026bbe_end:
.org 0x26BC0
m68k_026bc0:
        move.w %d3,%d5
m68k_026bc0_end:
.org 0x26BC2
m68k_026bc2:
        bra.b (. + -60)
m68k_026bc2_end:
.org 0x26BC4
m68k_026bc4:
        rts
m68k_026bc4_end:
.org 0x26BC6
m68k_026bc6:
        lea.l 0xc800:w,%a0
m68k_026bc6_end:
.org 0x26BCA
m68k_026bca:
        lsl.w #0x2,%d5
m68k_026bca_end:
.org 0x26BCC
m68k_026bcc:
        move.l (%a0, %d5.w),%d2
m68k_026bcc_end:
.org 0x26BD0
m68k_026bd0:
        jsr 0x83d4:l
m68k_026bd0_end:
.org 0x26BD6
m68k_026bd6:
        andi.l #0xffff,%d0
m68k_026bd6_end:
.org 0x26BDC
m68k_026bdc:
        move.l %d0,%d1
m68k_026bdc_end:
.org 0x26BDE
m68k_026bde:
        lsl.l #0x2,%d0
m68k_026bde_end:
.org 0x26BE0
m68k_026be0:
        add.l %d1,%d0
m68k_026be0_end:
.org 0x26BE2
m68k_026be2:
        lsl.l #0x1,%d0
m68k_026be2_end:
.org 0x26BE4
m68k_026be4:
        add.l %d1,%d0
m68k_026be4_end:
.org 0x26BE6
m68k_026be6:
        swap %d0
m68k_026be6_end:
.org 0x26BE8
m68k_026be8:
        addi.w #0x1e,%d0
m68k_026be8_end:
.org 0x26BEC
m68k_026bec:
        divu.w %d0,%d2
m68k_026bec_end:
.org 0x26BEE
m68k_026bee:
        andi.l #0xffff,%d2
m68k_026bee_end:
.org 0x26BF4
m68k_026bf4:
        move.l %d2,0xf39e:w
m68k_026bf4_end:
.org 0x26BF8
m68k_026bf8:
        rts
m68k_026bf8_end:
.org 0x31562
m68k_031562:
        bsr.w (. + 70)
m68k_031562_end:
.org 0x31566
m68k_031566:
        move.w #0x12c,0xf608:w
m68k_031566_end:
.org 0x3156C
m68k_03156c:
        move.w #0x1,0xf362:w
m68k_03156c_end:
.org 0x31572
m68k_031572:
        move.w 0xf3a6:w,0xf3d2:w
m68k_031572_end:
.org 0x31578
m68k_031578:
        move.w #0x11d,%d0
m68k_031578_end:
.org 0x3157C
m68k_03157c:
        jsr 0x676f2:l
m68k_03157c_end:
.org 0x31582
m68k_031582:
        move.w #0x1,0xf652:w
m68k_031582_end:
.org 0x31588
m68k_031588:
        bsr.w (. + 6)
m68k_031588_end:
.org 0x3158C
m68k_03158c:
        rts
m68k_03158c_end:
.org 0x3158E
m68k_03158e:
        lea.l 90(%pc),%a0
m68k_03158e_end:
.org 0x31592
m68k_031592:
        move.l #0xc0000006,%d0
m68k_031592_end:
.org 0x31598
m68k_031598:
        move.w #0xa,%d1
m68k_031598_end:
.org 0x3159C
m68k_03159c:
        move.w #0xc3a2,%d2
m68k_03159c_end:
.org 0x315A0
m68k_0315a0:
        jsr 0x26bfa:l
m68k_0315a0_end:
.org 0x315A6
m68k_0315a6:
        rts
m68k_0315a6_end:
.org 0x315A8
m68k_0315a8:
        lea.l 0xcc00:w,%a0
m68k_0315a8_end:
.org 0x315AC
m68k_0315ac:
        move.w 0xf3a6:w,%d1
m68k_0315ac_end:
.org 0x315B0
m68k_0315b0:
        move.b (%a0, %d1.w),%d0
m68k_0315b0_end:
.org 0x315B4
m68k_0315b4:
        move.b #0xff,(%a0, %d1.w)
m68k_0315b4_end:
.org 0x315BA
m68k_0315ba:
        andi.w #0x3f,%d0
m68k_0315ba_end:
.org 0x315BE
m68k_0315be:
        lea.l 0xf45e:w,%a1
m68k_0315be_end:
.org 0x315C2
m68k_0315c2:
        move.w 0xf3a6:w,%d2
m68k_0315c2_end:
.org 0x315C6
m68k_0315c6:
        move.w %d0,%d1
m68k_0315c6_end:
.org 0x315C8
m68k_0315c8:
        lsl.w #0x1,%d1
m68k_0315c8_end:
.org 0x315CA
m68k_0315ca:
        cmp.w (%a1, %d1.w),%d2
m68k_0315ca_end:
.org 0x315CE
m68k_0315ce:
        bne.w (. + 26)
m68k_0315ce_end:
.org 0x315D2
m68k_0315d2:
        move.w %d0,-(%a7)
m68k_0315d2_end:
.org 0x315D4
m68k_0315d4:
        move.w #0xffff,0xf630:w
m68k_0315d4_end:
.org 0x315DA
m68k_0315da:
        jsr 0x5f48:l
m68k_0315da_end:
.org 0x315E0
m68k_0315e0:
        move.w (%a7)+,%d0
m68k_0315e0_end:
.org 0x315E2
m68k_0315e2:
        jsr 0xe1f6:l
m68k_0315e2_end:
.org 0x315E8
m68k_0315e8:
        rts
m68k_0315e8_end:
.org 0x31612
m68k_031612:
        move.w #0x12c,0xf608:w
m68k_031612_end:
.org 0x31618
m68k_031618:
        move.w #0x1,0xf362:w
m68k_031618_end:
.org 0x3161E
m68k_03161e:
        move.w 0xf3a6:w,0xf3d2:w
m68k_03161e_end:
.org 0x31624
m68k_031624:
        move.w #0x11e,%d0
m68k_031624_end:
.org 0x31628
m68k_031628:
        jsr 0x676f2:l
m68k_031628_end:
.org 0x3162E
m68k_03162e:
        bsr.w (. + -160)
m68k_03162e_end:
.org 0x31632
m68k_031632:
        rts
m68k_031632_end:
.org 0x31634
m68k_031634:
        bsr.w (. + -140)
m68k_031634_end:
.org 0x31638
m68k_031638:
        lea.l 0xcc00:w,%a0
m68k_031638_end:
.org 0x3163C
m68k_03163c:
        move.w 0xf3a8:w,%d0
m68k_03163c_end:
.org 0x31640
m68k_031640:
        move.w #0xff,%d1
m68k_031640_end:
.org 0x31644
m68k_031644:
        clr.w %d2
m68k_031644_end:
.org 0x31646
m68k_031646:
        cmp.b (%a0, %d1.w),%d0
m68k_031646_end:
.org 0x3164A
m68k_03164a:
        bne.w (. + 6)
m68k_03164a_end:
.org 0x3164E
m68k_03164e:
        addq.w #0x1,%d2
m68k_03164e_end:
.org 0x31650
m68k_031650:
        dbra %d1,(. + -10)
m68k_031650_end:
.org 0x31654
m68k_031654:
        cmpi.w #0xa,%d2
m68k_031654_end:
.org 0x31658
m68k_031658:
        bcc.w (. + 88)
m68k_031658_end:
.org 0x3165C
m68k_03165c:
        lea.l 0xcc00:w,%a0
m68k_03165c_end:
.org 0x31660
m68k_031660:
        move.w 0xf3a6:w,%d1
m68k_031660_end:
.org 0x31664
m68k_031664:
        move.b %d0,(%a0, %d1.w)
m68k_031664_end:
.org 0x31668
m68k_031668:
        lea.l 0xf427:w,%a0
m68k_031668_end:
.org 0x3166C
m68k_03166c:
        move.b (%a0, %d0.w),%d0
m68k_03166c_end:
.org 0x31670
m68k_031670:
        andi.w #0xf,%d0
m68k_031670_end:
.org 0x31674
m68k_031674:
        lsl.w #0x1,%d0
m68k_031674_end:
.org 0x31676
m68k_031676:
        lea.l 0xe640:w,%a0
m68k_031676_end:
.org 0x3167A
m68k_03167a:
        move.w (%a0, %d0.w),0xf3f2:w
m68k_03167a_end:
.org 0x31680
m68k_031680:
        jsr 0x208ce:l
m68k_031680_end:
.org 0x31686
m68k_031686:
        move.w #0x12c,0xf608:w
m68k_031686_end:
.org 0x3168C
m68k_03168c:
        move.w #0x1,0xf362:w
m68k_03168c_end:
.org 0x31692
m68k_031692:
        move.w 0xf3a6:w,0xf3d2:w
m68k_031692_end:
.org 0x31698
m68k_031698:
        move.w #0x11f,%d0
m68k_031698_end:
.org 0x3169C
m68k_03169c:
        jsr 0x676f2:l
m68k_03169c_end:
.org 0x316A2
m68k_0316a2:
        move.w #0x1,0xf652:w
m68k_0316a2_end:
.org 0x316A8
m68k_0316a8:
        bsr.w (. + -282)
m68k_0316a8_end:
.org 0x316AC
m68k_0316ac:
        bra.w (. + 52)
m68k_0316ac_end:
.org 0x316B0
m68k_0316b0:
        lea.l 0xcc00:w,%a0
m68k_0316b0_end:
.org 0x316B4
m68k_0316b4:
        move.w 0xf3a6:w,%d1
m68k_0316b4_end:
.org 0x316B8
m68k_0316b8:
        bset.l #0x7,%d0
m68k_0316b8_end:
.org 0x316BC
m68k_0316bc:
        move.b %d0,(%a0, %d1.w)
m68k_0316bc_end:
.org 0x316C0
m68k_0316c0:
        move.w #0x12c,0xf608:w
m68k_0316c0_end:
.org 0x316C6
m68k_0316c6:
        move.w #0x1,0xf362:w
m68k_0316c6_end:
.org 0x316CC
m68k_0316cc:
        move.w 0xf3a6:w,0xf3d0:w
m68k_0316cc_end:
.org 0x316D2
m68k_0316d2:
        move.w #0x9b,%d0
m68k_0316d2_end:
.org 0x316D6
m68k_0316d6:
        jsr 0x676f2:l
m68k_0316d6_end:
.org 0x316DC
m68k_0316dc:
        bsr.w (. + -334)
m68k_0316dc_end:
.org 0x316E0
m68k_0316e0:
        rts
m68k_0316e0_end:
.org 0x34F94
m68k_034f94:
        bsr.w (. + 26)
m68k_034f94_end:
.org 0x34F98
m68k_034f98:
        bcs.w (. + 14)
m68k_034f98_end:
.org 0x34F9C
m68k_034f9c:
        move.w #0x8,0xf728:w
m68k_034f9c_end:
.org 0x34FA2
m68k_034fa2:
        bra.w (. + 10)
m68k_034fa2_end:
.org 0x34FA6
m68k_034fa6:
        move.w #0x3,0xf728:w
m68k_034fa6_end:
.org 0x34FAC
m68k_034fac:
        rts
m68k_034fac_end:
.org 0x34FAE
m68k_034fae:
        movea.l 0xff382c:l,%a0
m68k_034fae_end:
.org 0x34FB4
m68k_034fb4:
        clr.w %d0
m68k_034fb4_end:
.org 0x34FB6
m68k_034fb6:
        move.b 0x1(%a0),%d0
m68k_034fb6_end:
.org 0x34FBA
m68k_034fba:
        clr.w %d1
m68k_034fba_end:
.org 0x34FBC
m68k_034fbc:
        move.b 0x2(%a0),%d1
m68k_034fbc_end:
.org 0x34FC0
m68k_034fc0:
        move.w %d0,%d2
m68k_034fc0_end:
.org 0x34FC2
m68k_034fc2:
        lsl.w #0x3,%d2
m68k_034fc2_end:
.org 0x34FC4
m68k_034fc4:
        add.w %d0,%d2
m68k_034fc4_end:
.org 0x34FC6
m68k_034fc6:
        lsl.w #0x3,%d2
m68k_034fc6_end:
.org 0x34FC8
m68k_034fc8:
        add.w %d1,%d2
m68k_034fc8_end:
.org 0x34FCA
m68k_034fca:
        lea.l 0xee5f0:l,%a1
m68k_034fca_end:
.org 0x34FD0
m68k_034fd0:
        adda.w %d2,%a1
m68k_034fd0_end:
.org 0x34FD2
m68k_034fd2:
        cmpi.b #0x1,-0x48(%a1)
m68k_034fd2_end:
.org 0x34FD8
m68k_034fd8:
        beq.w (. + 34)
m68k_034fd8_end:
.org 0x34FDC
m68k_034fdc:
        cmpi.b #0x1,-0x1(%a1)
m68k_034fdc_end:
.org 0x34FE2
m68k_034fe2:
        beq.w (. + 24)
m68k_034fe2_end:
.org 0x34FE6
m68k_034fe6:
        cmpi.b #0x1,0x1(%a1)
m68k_034fe6_end:
.org 0x34FEC
m68k_034fec:
        beq.w (. + 14)
m68k_034fec_end:
.org 0x34FF0
m68k_034ff0:
        cmpi.b #0x1,0x48(%a1)
m68k_034ff0_end:
.org 0x34FF6
m68k_034ff6:
        bne.w (. + 104)
m68k_034ff6_end:
.org 0x34FFA
m68k_034ffa:
        move.w %d0,%d2
m68k_034ffa_end:
.org 0x34FFC
m68k_034ffc:
        subq.w #0x1,%d0
m68k_034ffc_end:
.org 0x34FFE
m68k_034ffe:
        addq.w #0x1,%d2
m68k_034ffe_end:
.org 0x35000
m68k_035000:
        lsl.w #0x4,%d0
m68k_035000_end:
.org 0x35002
m68k_035002:
        lsl.w #0x4,%d2
m68k_035002_end:
.org 0x35004
m68k_035004:
        addq.w #0x8,%d0
m68k_035004_end:
.org 0x35006
m68k_035006:
        addq.w #0x8,%d2
m68k_035006_end:
.org 0x35008
m68k_035008:
        move.w %d1,%d3
m68k_035008_end:
.org 0x3500A
m68k_03500a:
        subq.w #0x1,%d1
m68k_03500a_end:
.org 0x3500C
m68k_03500c:
        addq.w #0x2,%d3
m68k_03500c_end:
.org 0x3500E
m68k_03500e:
        lsl.w #0x4,%d1
m68k_03500e_end:
.org 0x35010
m68k_035010:
        lsl.w #0x4,%d3
m68k_035010_end:
.org 0x35012
m68k_035012:
        lea.l 0xd4b66:l,%a1
m68k_035012_end:
.org 0x35018
m68k_035018:
        move.w #0x27,%d6
m68k_035018_end:
.org 0x3501C
m68k_03501c:
        move.w 0x2(%a1),%d7
m68k_03501c_end:
.org 0x35020
m68k_035020:
        cmp.w %d0,%d7
m68k_035020_end:
.org 0x35022
m68k_035022:
        bcs.w (. + 24)
m68k_035022_end:
.org 0x35026
m68k_035026:
        cmp.w %d2,%d7
m68k_035026_end:
.org 0x35028
m68k_035028:
        bhi.w (. + 18)
m68k_035028_end:
.org 0x3502C
m68k_03502c:
        move.w (%a1),%d7
m68k_03502c_end:
.org 0x3502E
m68k_03502e:
        cmp.w %d1,%d7
m68k_03502e_end:
.org 0x35030
m68k_035030:
        bcs.w (. + 10)
m68k_035030_end:
.org 0x35034
m68k_035034:
        cmp.w %d3,%d7
m68k_035034_end:
.org 0x35036
m68k_035036:
        bls.w (. + 10)
m68k_035036_end:
.org 0x3503A
m68k_03503a:
        subq.w #0x4,%a1
m68k_03503a_end:
.org 0x3503C
m68k_03503c:
        dbra %d6,(. + -32)
m68k_03503c_end:
.org 0x35040
m68k_035040:
        lea.l 0xf428:w,%a1
m68k_035040_end:
.org 0x35044
m68k_035044:
        move.b (%a1, %d6.w),%d0
m68k_035044_end:
.org 0x35048
m68k_035048:
        cmp.b 0x4(%a0),%d0
m68k_035048_end:
.org 0x3504C
m68k_03504c:
        beq.w (. + 18)
m68k_03504c_end:
.org 0x35050
m68k_035050:
        addq.w #0x1,%d6
m68k_035050_end:
.org 0x35052
m68k_035052:
        move.w %d6,0xf392:w
m68k_035052_end:
.org 0x35056
m68k_035056:
        ori.w #0x1,%sr
m68k_035056_end:
.org 0x3505A
m68k_03505a:
        bra.w (. + 8)
m68k_03505a_end:
.org 0x3505E
m68k_03505e:
        andi.w #0xfffe,%sr
m68k_03505e_end:
.org 0x35062
m68k_035062:
        rts
m68k_035062_end:
.org 0x35064
m68k_035064:
        bsr.w (. + 38)
m68k_035064_end:
.org 0x35068
m68k_035068:
        bsr.w (. + 74)
m68k_035068_end:
.org 0x3506C
m68k_03506c:
        cmp.l %d0,%d2
m68k_03506c_end:
.org 0x3506E
m68k_03506e:
        bhi.w (. + 20)
m68k_03506e_end:
.org 0x35072
m68k_035072:
        cmp.w %d1,%d3
m68k_035072_end:
.org 0x35074
m68k_035074:
        bhi.w (. + 14)
m68k_035074_end:
.org 0x35078
m68k_035078:
        move.w #0x7,0xf728:w
m68k_035078_end:
.org 0x3507E
m68k_03507e:
        bra.w (. + 10)
m68k_03507e_end:
.org 0x35082
m68k_035082:
        move.w #0x8,0xf728:w
m68k_035082_end:
.org 0x35088
m68k_035088:
        rts
m68k_035088_end:
.org 0x3508A
m68k_03508a:
        lea.l 0xf72a:w,%a0
m68k_03508a_end:
.org 0x3508E
m68k_03508e:
        lea.l 0xc800:w,%a1
m68k_03508e_end:
.org 0x35092
m68k_035092:
        moveq #0,%d0
m68k_035092_end:
.org 0x35094
m68k_035094:
        clr.w %d1
m68k_035094_end:
.org 0x35096
m68k_035096:
        move.w (%a0)+,%d0
m68k_035096_end:
.org 0x35098
m68k_035098:
        bmi.w (. + 24)
m68k_035098_end:
.org 0x3509C
m68k_03509c:
        lsl.w #0x2,%d0
m68k_03509c_end:
.org 0x3509E
m68k_03509e:
        move.l (%a1, %d0.w),%d2
m68k_03509e_end:
.org 0x350A2
m68k_0350a2:
        add.l %d2,%d0
m68k_0350a2_end:
.org 0x350A4
m68k_0350a4:
        cmpi.l #0x1388,%d2
m68k_0350a4_end:
.org 0x350AA
m68k_0350aa:
        bcs.b (. + -20)
m68k_0350aa_end:
.org 0x350AC
m68k_0350ac:
        addq.w #0x1,%d1
m68k_0350ac_end:
.org 0x350AE
m68k_0350ae:
        bra.b (. + -24)
m68k_0350ae_end:
.org 0x350B0
m68k_0350b0:
        rts
m68k_0350b0_end:
.org 0x350B2
m68k_0350b2:
        move.w 0xf392:w,%d4
m68k_0350b2_end:
.org 0x350B6
m68k_0350b6:
        lea.l 0xcd00:w,%a0
m68k_0350b6_end:
.org 0x350BA
m68k_0350ba:
        lea.l 0xc800:w,%a1
m68k_0350ba_end:
.org 0x350BE
m68k_0350be:
        moveq #0,%d2
m68k_0350be_end:
.org 0x350C0
m68k_0350c0:
        clr.w %d3
m68k_0350c0_end:
.org 0x350C2
m68k_0350c2:
        move.w #0xff,%d4
m68k_0350c2_end:
.org 0x350C6
m68k_0350c6:
        cmp.b -(%a0),%d4
m68k_0350c6_end:
.org 0x350C8
m68k_0350c8:
        bne.w (. + 26)
m68k_0350c8_end:
.org 0x350CC
m68k_0350cc:
        move.w %d4,%d5
m68k_0350cc_end:
.org 0x350CE
m68k_0350ce:
        lsl.w #0x2,%d5
m68k_0350ce_end:
.org 0x350D0
m68k_0350d0:
        move.l (%a1, %d5.w),%d6
m68k_0350d0_end:
.org 0x350D4
m68k_0350d4:
        add.l %d6,%d2
m68k_0350d4_end:
.org 0x350D6
m68k_0350d6:
        cmpi.l #0x1388,%d6
m68k_0350d6_end:
.org 0x350DC
m68k_0350dc:
        bcs.w (. + 6)
m68k_0350dc_end:
.org 0x350E0
m68k_0350e0:
        addq.w #0x1,%d3
m68k_0350e0_end:
.org 0x350E2
m68k_0350e2:
        dbra %d4,(. + -28)
m68k_0350e2_end:
.org 0x350E6
m68k_0350e6:
        rts
m68k_0350e6_end:
.org 0x350E8
m68k_0350e8:
        move.w 0xf376:w,%d0
m68k_0350e8_end:
.org 0x350EC
m68k_0350ec:
        lsl.w #0x1,%d0
m68k_0350ec_end:
.org 0x350EE
m68k_0350ee:
        lea.l 0xe710:w,%a0
m68k_0350ee_end:
.org 0x350F2
m68k_0350f2:
        move.w (%a0, %d0.w),%d0
m68k_0350f2_end:
.org 0x350F6
m68k_0350f6:
        lea.l 0xf427:w,%a0
m68k_0350f6_end:
.org 0x350FA
m68k_0350fa:
        move.w 0xf392:w,%d1
m68k_0350fa_end:
.org 0x350FE
m68k_0350fe:
        clr.w %d2
m68k_0350fe_end:
.org 0x35100
m68k_035100:
        move.b (%a0, %d1.w),%d2
m68k_035100_end:
.org 0x35104
m68k_035104:
        btst.l %d2,%d0
m68k_035104_end:
.org 0x35106
m68k_035106:
        beq.w (. + 36)
m68k_035106_end:
.org 0x3510A
m68k_03510a:
        jsr 0x83d4:l
m68k_03510a_end:
.org 0x35110
m68k_035110:
        andi.l #0xffff,%d0
m68k_035110_end:
.org 0x35116
m68k_035116:
        lsl.w #0x2,%d0
m68k_035116_end:
.org 0x35118
m68k_035118:
        swap %d0
m68k_035118_end:
.org 0x3511A
m68k_03511a:
        tst.w %d0
m68k_03511a_end:
.org 0x3511C
m68k_03511c:
        beq.w (. + 14)
m68k_03511c_end:
.org 0x35120
m68k_035120:
        move.w #0x8,0xf728:w
m68k_035120_end:
.org 0x35126
m68k_035126:
        bra.w (. + 10)
m68k_035126_end:
.org 0x3512A
m68k_03512a:
        move.w #0x4,0xf728:w
m68k_03512a_end:
.org 0x35130
m68k_035130:
        rts
m68k_035130_end:
.org 0x35132
m68k_035132:
        lea.l 0xea37:w,%a0
m68k_035132_end:
.org 0x35136
m68k_035136:
        move.w 0xf392:w,%d0
m68k_035136_end:
.org 0x3513A
m68k_03513a:
        tst.b (%a0, %d0.w)
m68k_03513a_end:
.org 0x3513E
m68k_03513e:
        bne.w (. + 14)
m68k_03513e_end:
.org 0x35142
m68k_035142:
        move.w #0x2,0xf728:w
m68k_035142_end:
.org 0x35148
m68k_035148:
        bra.w (. + 10)
m68k_035148_end:
.org 0x3514C
m68k_03514c:
        move.w #0x5,0xf728:w
m68k_03514c_end:
.org 0x35152
m68k_035152:
        rts
m68k_035152_end:
.org 0x35154
m68k_035154:
        bsr.w (. + 30)
m68k_035154_end:
.org 0x35158
m68k_035158:
        cmp.w 0xf376:w,%d1
m68k_035158_end:
.org 0x3515C
m68k_03515c:
        bne.w (. + 14)
m68k_03515c_end:
.org 0x35160
m68k_035160:
        move.w #0x6,0xf728:w
m68k_035160_end:
.org 0x35166
m68k_035166:
        bra.w (. + 10)
m68k_035166_end:
.org 0x3516A
m68k_03516a:
        move.w #0x8,0xf728:w
m68k_03516a_end:
.org 0x35170
m68k_035170:
        rts
m68k_035170_end:
.org 0x35172
m68k_035172:
        lea.l 0xa050:w,%a0
m68k_035172_end:
.org 0x35176
m68k_035176:
        move.w 0xf392:w,%d0
m68k_035176_end:
.org 0x3517A
m68k_03517a:
        clr.w %d1
m68k_03517a_end:
.org 0x3517C
m68k_03517c:
        move.w #0xff,%d2
m68k_03517c_end:
.org 0x35180
m68k_035180:
        move.b (%a0, %d2.w),%d1
m68k_035180_end:
.org 0x35184
m68k_035184:
        cmp.w %d1,%d0
m68k_035184_end:
.org 0x35186
m68k_035186:
        beq.w (. + 8)
m68k_035186_end:
.org 0x3518A
m68k_03518a:
        dbra %d2,(. + -10)
m68k_03518a_end:
.org 0x3518E
m68k_03518e:
        lea.l 0xcc00:w,%a0
m68k_03518e_end:
.org 0x35192
m68k_035192:
        clr.w %d1
m68k_035192_end:
.org 0x35194
m68k_035194:
        move.b (%a0, %d2.w),%d1
m68k_035194_end:
.org 0x35198
m68k_035198:
        lea.l 0xf427:w,%a0
m68k_035198_end:
.org 0x3519C
m68k_03519c:
        move.b (%a0, %d1.w),%d1
m68k_03519c_end:
.org 0x351A0
m68k_0351a0:
        rts
m68k_0351a0_end:
.org 0x351A2
m68k_0351a2:
        bsr.w (. + 40)
m68k_0351a2_end:
.org 0x351A6
m68k_0351a6:
        cmpi.l #0x1f40,%d0
m68k_0351a6_end:
.org 0x351AC
m68k_0351ac:
        bcs.w (. + 22)
m68k_0351ac_end:
.org 0x351B0
m68k_0351b0:
        bsr.w (. + 52)
m68k_0351b0_end:
.org 0x351B4
m68k_0351b4:
        bcs.w (. + 14)
m68k_0351b4_end:
.org 0x351B8
m68k_0351b8:
        move.w #0x7,0xf728:w
m68k_0351b8_end:
.org 0x351BE
m68k_0351be:
        bra.w (. + 10)
m68k_0351be_end:
.org 0x351C2
m68k_0351c2:
        move.w #0x8,0xf728:w
m68k_0351c2_end:
.org 0x351C8
m68k_0351c8:
        rts
m68k_0351c8_end:
.org 0x351CA
m68k_0351ca:
        lea.l 0xf72a:w,%a0
m68k_0351ca_end:
.org 0x351CE
m68k_0351ce:
        lea.l 0xc800:w,%a1
m68k_0351ce_end:
.org 0x351D2
m68k_0351d2:
        moveq #0,%d0
m68k_0351d2_end:
.org 0x351D4
m68k_0351d4:
        move.w (%a0)+,%d1
m68k_0351d4_end:
.org 0x351D6
m68k_0351d6:
        bmi.w (. + 12)
m68k_0351d6_end:
.org 0x351DA
m68k_0351da:
        lsl.w #0x2,%d1
m68k_0351da_end:
.org 0x351DC
m68k_0351dc:
        add.l (%a1, %d1.w),%d0
m68k_0351dc_end:
.org 0x351E0
m68k_0351e0:
        bra.b (. + -12)
m68k_0351e0_end:
.org 0x351E2
m68k_0351e2:
        rts
m68k_0351e2_end:
.org 0x351E4
m68k_0351e4:
        lea.l 0xf72a:w,%a0
m68k_0351e4_end:
.org 0x351E8
m68k_0351e8:
        lea.l 0xb000:w,%a1
m68k_0351e8_end:
.org 0x351EC
m68k_0351ec:
        lea.l 0xb200:w,%a2
m68k_0351ec_end:
.org 0x351F0
m68k_0351f0:
        move.w (%a0)+,%d0
m68k_0351f0_end:
.org 0x351F2
m68k_0351f2:
        bmi.w (. + 24)
m68k_0351f2_end:
.org 0x351F6
m68k_0351f6:
        lsl.w #0x1,%d0
m68k_0351f6_end:
.org 0x351F8
m68k_0351f8:
        move.w (%a1, %d0.w),%d1
m68k_0351f8_end:
.org 0x351FC
m68k_0351fc:
        cmp.w (%a2, %d0.w),%d1
m68k_0351fc_end:
.org 0x35200
m68k_035200:
        bls.b (. + -16)
m68k_035200_end:
.org 0x35202
m68k_035202:
        ori.w #0x1,%sr
m68k_035202_end:
.org 0x35206
m68k_035206:
        bra.w (. + 8)
m68k_035206_end:
.org 0x3520A
m68k_03520a:
        andi.w #0xfffe,%sr
m68k_03520a_end:
.org 0x3520E
m68k_03520e:
        rts
m68k_03520e_end:
.org 0x35210
m68k_035210:
        move.l 0xff382c:l,%d0
m68k_035210_end:
.org 0x35216
m68k_035216:
        subi.l #0xffff9000,%d0
m68k_035216_end:
.org 0x3521C
m68k_03521c:
        move.w %d0,0xf75a:w
m68k_03521c_end:
.org 0x35220
m68k_035220:
        bsr.w (. + -2790)
m68k_035220_end:
.org 0x35224
m68k_035224:
        move.w #0xa,%d1
m68k_035224_end:
.org 0x35228
m68k_035228:
        sub.w %d0,%d1
m68k_035228_end:
.org 0x3522A
m68k_03522a:
        beq.w (. + 84)
m68k_03522a_end:
.org 0x3522E
m68k_03522e:
        move.w %d1,%d7
m68k_03522e_end:
.org 0x35230
m68k_035230:
        bsr.w (. + -2742)
m68k_035230_end:
.org 0x35234
m68k_035234:
        bsr.w (. + -2500)
m68k_035234_end:
.org 0x35238
m68k_035238:
        clr.w 0xf772:w
m68k_035238_end:
.org 0x3523C
m68k_03523c:
        move.w 0xf392:w,0xf68a:w
m68k_03523c_end:
.org 0x35242
m68k_035242:
        move.w #0xffff,0xa5f8:w
m68k_035242_end:
.org 0x35248
m68k_035248:
        move.w #0x400,0xf612:w
m68k_035248_end:
.org 0x3524E
m68k_03524e:
        clr.w 0xf362:w
m68k_03524e_end:
.org 0x35252
m68k_035252:
        clr.w 0xf352:w
m68k_035252_end:
.org 0x35256
m68k_035256:
        move.w #0x1f,%d0
m68k_035256_end:
.org 0x3525A
m68k_03525a:
        lea.l 0xfb00:w,%a0
m68k_03525a_end:
.org 0x3525E
m68k_03525e:
        lea.l 0xfb80:w,%a1
m68k_03525e_end:
.org 0x35262
m68k_035262:
        move.w (%a0)+,(%a1)+
m68k_035262_end:
.org 0x35264
m68k_035264:
        dbra %d0,(. + 26)
m68k_035264_end:
.org 0x35268
m68k_035268:
        move.w #0xffff,0xa550:w
m68k_035268_end:
.org 0x3526E
m68k_03526e:
        move.w #0xffff,0xa5a4:w
m68k_03526e_end:
.org 0x35274
m68k_035274:
        clr.w 0xf36a:w
m68k_035274_end:
.org 0x35278
m68k_035278:
        jsr 0x1b098:l
m68k_035278_end:
.org 0x3527E
m68k_03527e:
        move.w #0xffff,0xf728:w
m68k_03527e_end:
.org 0x35284
m68k_035284:
        rts
m68k_035284_end:
.org 0x35286
m68k_035286:
        bsr.w (. + 30)
m68k_035286_end:
.org 0x3528A
m68k_03528a:
        tst.w 0xd300:w
m68k_03528a_end:
.org 0x3528E
m68k_03528e:
        bmi.w (. + 14)
m68k_03528e_end:
.org 0x35292
m68k_035292:
        move.w #0x9,0xf728:w
m68k_035292_end:
.org 0x35298
m68k_035298:
        bra.w (. + 10)
m68k_035298_end:
.org 0x3529C
m68k_03529c:
        move.w #0xb,0xf728:w
m68k_03529c_end:
.org 0x352A2
m68k_0352a2:
        rts
m68k_0352a2_end:
.org 0x352A4
m68k_0352a4:
        movea.l 0xff382c:l,%a0
m68k_0352a4_end:
.org 0x352AA
m68k_0352aa:
        clr.w %d0
m68k_0352aa_end:
.org 0x352AC
m68k_0352ac:
        move.b 0x1(%a0),%d0
m68k_0352ac_end:
.org 0x352B0
m68k_0352b0:
        move.w %d0,%d1
m68k_0352b0_end:
.org 0x352B2
m68k_0352b2:
        subq.w #0x1,%d1
m68k_0352b2_end:
.org 0x352B4
m68k_0352b4:
        move.w %d0,%d2
m68k_0352b4_end:
.org 0x352B6
m68k_0352b6:
        addq.w #0x1,%d2
m68k_0352b6_end:
.org 0x352B8
m68k_0352b8:
        clr.w %d3
m68k_0352b8_end:
.org 0x352BA
m68k_0352ba:
        move.b 0x2(%a0),%d3
m68k_0352ba_end:
.org 0x352BE
m68k_0352be:
        move.w %d3,%d4
m68k_0352be_end:
.org 0x352C0
m68k_0352c0:
        subq.w #0x1,%d4
m68k_0352c0_end:
.org 0x352C2
m68k_0352c2:
        move.w %d3,%d5
m68k_0352c2_end:
.org 0x352C4
m68k_0352c4:
        addq.w #0x1,%d5
m68k_0352c4_end:
.org 0x352C6
m68k_0352c6:
        lsl.w #0x8,%d1
m68k_0352c6_end:
.org 0x352C8
m68k_0352c8:
        move.b %d3,%d1
m68k_0352c8_end:
.org 0x352CA
m68k_0352ca:
        lsl.w #0x8,%d2
m68k_0352ca_end:
.org 0x352CC
m68k_0352cc:
        move.b %d3,%d2
m68k_0352cc_end:
.org 0x352CE
m68k_0352ce:
        lsl.w #0x8,%d0
m68k_0352ce_end:
.org 0x352D0
m68k_0352d0:
        move.w %d0,%d3
m68k_0352d0_end:
.org 0x352D2
m68k_0352d2:
        move.b %d4,%d0
m68k_0352d2_end:
.org 0x352D4
m68k_0352d4:
        move.b %d5,%d3
m68k_0352d4_end:
.org 0x352D6
m68k_0352d6:
        lea.l 0xd300:w,%a1
m68k_0352d6_end:
.org 0x352DA
m68k_0352da:
        lea.l 0x9000:w,%a2
m68k_0352da_end:
.org 0x352DE
m68k_0352de:
        clr.w %d4
m68k_0352de_end:
.org 0x352E0
m68k_0352e0:
        lea.l 0xe710:w,%a3
m68k_0352e0_end:
.org 0x352E4
m68k_0352e4:
        move.w 0xf376:w,%d7
m68k_0352e4_end:
.org 0x352E8
m68k_0352e8:
        lsl.w #0x1,%d7
m68k_0352e8_end:
.org 0x352EA
m68k_0352ea:
        move.w (%a3, %d7.w),%d7
m68k_0352ea_end:
.org 0x352EE
m68k_0352ee:
        move.b (%a2),%d5
m68k_0352ee_end:
.org 0x352F0
m68k_0352f0:
        andi.w #0xf,%d5
m68k_0352f0_end:
.org 0x352F4
m68k_0352f4:
        beq.w (. + 72)
m68k_0352f4_end:
.org 0x352F8
m68k_0352f8:
        clr.w %d6
m68k_0352f8_end:
.org 0x352FA
m68k_0352fa:
        move.b 0x4(%a2),%d6
m68k_0352fa_end:
.org 0x352FE
m68k_0352fe:
        cmp.b 0xf377:w,%d6
m68k_0352fe_end:
.org 0x35302
m68k_035302:
        beq.w (. + 46)
m68k_035302_end:
.org 0x35306
m68k_035306:
        btst.l %d6,%d7
m68k_035306_end:
.org 0x35308
m68k_035308:
        bne.w (. + 40)
m68k_035308_end:
.org 0x3530C
m68k_03530c:
        move.b 0x1(%a2),%d6
m68k_03530c_end:
.org 0x35310
m68k_035310:
        lsl.w #0x8,%d6
m68k_035310_end:
.org 0x35312
m68k_035312:
        move.b 0x2(%a2),%d6
m68k_035312_end:
.org 0x35316
m68k_035316:
        cmp.w %d0,%d6
m68k_035316_end:
.org 0x35318
m68k_035318:
        beq.w (. + 22)
m68k_035318_end:
.org 0x3531C
m68k_03531c:
        cmp.w %d1,%d6
m68k_03531c_end:
.org 0x3531E
m68k_03531e:
        beq.w (. + 16)
m68k_03531e_end:
.org 0x35322
m68k_035322:
        cmp.w %d2,%d6
m68k_035322_end:
.org 0x35324
m68k_035324:
        beq.w (. + 10)
m68k_035324_end:
.org 0x35328
m68k_035328:
        cmp.w %d3,%d6
m68k_035328_end:
.org 0x3532A
m68k_03532a:
        bne.w (. + 6)
m68k_03532a_end:
.org 0x3532E
m68k_03532e:
        move.w %d4,(%a1)+
m68k_03532e_end:
.org 0x35330
m68k_035330:
        lea.l 0xd(%a2, %d5.w),%a2
m68k_035330_end:
.org 0x35334
m68k_035334:
        addi.w #0xd,%d5
m68k_035334_end:
.org 0x35338
m68k_035338:
        add.w %d5,%d4
m68k_035338_end:
.org 0x3533A
m68k_03533a:
        bra.b (. + -76)
m68k_03533a_end:
.org 0x3533C
m68k_03533c:
        move.w #0xffff,(%a1)
m68k_03533c_end:
.org 0x35340
m68k_035340:
        rts
m68k_035340_end:
.org 0x35342
m68k_035342:
        bsr.w (. + 36)
m68k_035342_end:
.org 0x35346
m68k_035346:
        bsr.w (. + 58)
m68k_035346_end:
.org 0x3534A
m68k_03534a:
        cmp.l %d0,%d1
m68k_03534a_end:
.org 0x3534C
m68k_03534c:
        bhi.w (. + 18)
m68k_03534c_end:
.org 0x35350
m68k_035350:
        move.w %d2,0xf744:w
m68k_035350_end:
.org 0x35354
m68k_035354:
        move.w #0xa,0xf728:w
m68k_035354_end:
.org 0x3535A
m68k_03535a:
        bra.w (. + 10)
m68k_03535a_end:
.org 0x3535E
m68k_03535e:
        move.w #0xb,0xf728:w
m68k_03535e_end:
.org 0x35364
m68k_035364:
        rts
m68k_035364_end:
.org 0x35366
m68k_035366:
        lea.l 0xf72a:w,%a0
m68k_035366_end:
.org 0x3536A
m68k_03536a:
        lea.l 0xc800:w,%a1
m68k_03536a_end:
.org 0x3536E
m68k_03536e:
        moveq #0,%d0
m68k_03536e_end:
.org 0x35370
m68k_035370:
        move.w (%a0)+,%d1
m68k_035370_end:
.org 0x35372
m68k_035372:
        bmi.w (. + 12)
m68k_035372_end:
.org 0x35376
m68k_035376:
        lsl.w #0x2,%d1
m68k_035376_end:
.org 0x35378
m68k_035378:
        add.l (%a1, %d1.w),%d0
m68k_035378_end:
.org 0x3537C
m68k_03537c:
        bra.b (. + -12)
m68k_03537c_end:
.org 0x3537E
m68k_03537e:
        rts
m68k_03537e_end:
.org 0x35380
m68k_035380:
        lea.l 0xd300:w,%a0
m68k_035380_end:
.org 0x35384
m68k_035384:
        lea.l 0xc800:w,%a2
m68k_035384_end:
.org 0x35388
m68k_035388:
        moveq #-1,%d1
m68k_035388_end:
.org 0x3538A
m68k_03538a:
        move.w (%a0)+,%d3
m68k_03538a_end:
.org 0x3538C
m68k_03538c:
        bmi.w (. + 46)
m68k_03538c_end:
.org 0x35390
m68k_035390:
        lea.l 0x9000:w,%a1
m68k_035390_end:
.org 0x35394
m68k_035394:
        adda.w %d3,%a1
m68k_035394_end:
.org 0x35396
m68k_035396:
        move.b (%a1),%d4
m68k_035396_end:
.org 0x35398
m68k_035398:
        andi.w #0xf,%d4
m68k_035398_end:
.org 0x3539C
m68k_03539c:
        subq.w #0x1,%d4
m68k_03539c_end:
.org 0x3539E
m68k_03539e:
        moveq #0,%d5
m68k_03539e_end:
.org 0x353A0
m68k_0353a0:
        clr.w %d6
m68k_0353a0_end:
.org 0x353A2
m68k_0353a2:
        move.b 0xd(%a1, %d4.w),%d6
m68k_0353a2_end:
.org 0x353A6
m68k_0353a6:
        lsl.w #0x2,%d6
m68k_0353a6_end:
.org 0x353A8
m68k_0353a8:
        add.l (%a2, %d6.w),%d5
m68k_0353a8_end:
.org 0x353AC
m68k_0353ac:
        dbra %d4,(. + -12)
m68k_0353ac_end:
.org 0x353B0
m68k_0353b0:
        cmp.l %d1,%d5
m68k_0353b0_end:
.org 0x353B2
m68k_0353b2:
        bcc.b (. + -40)
m68k_0353b2_end:
.org 0x353B4
m68k_0353b4:
        move.l %d5,%d1
m68k_0353b4_end:
.org 0x353B6
m68k_0353b6:
        move.w %d3,%d2
m68k_0353b6_end:
.org 0x353B8
m68k_0353b8:
        bra.b (. + -46)
m68k_0353b8_end:
.org 0x353BA
m68k_0353ba:
        rts
m68k_0353ba_end:
.org 0x353BC
m68k_0353bc:
        move.w 0xf744:w,0xefbe:w
m68k_0353bc_end:
.org 0x353C2
m68k_0353c2:
        clr.w 0xefc6:w
m68k_0353c2_end:
.org 0x353C6
m68k_0353c6:
        move.w #0x14,0xf65a:w
m68k_0353c6_end:
.org 0x353CC
m68k_0353cc:
        move.w #0xb5,0xf38c:w
m68k_0353cc_end:
.org 0x353D2
m68k_0353d2:
        move.w #0x208,0xf612:w
m68k_0353d2_end:
.org 0x353D8
m68k_0353d8:
        move.w #0x4,0xf362:w
m68k_0353d8_end:
.org 0x353DE
m68k_0353de:
        move.w #0x1,0xf576:w
m68k_0353de_end:
.org 0x353E4
m68k_0353e4:
        move.w #0xffff,0xf728:w
m68k_0353e4_end:
.org 0x353EA
m68k_0353ea:
        rts
m68k_0353ea_end:
.org 0x353EC
m68k_0353ec:
        move.w #0xffff,0xf728:w
m68k_0353ec_end:
.org 0x353F2
m68k_0353f2:
        rts
m68k_0353f2_end:
.org 0x353F4
m68k_0353f4:
        move.w #0xffff,0xf728:w
m68k_0353f4_end:
.org 0x353FA
m68k_0353fa:
        rts
m68k_0353fa_end:
.org 0x3B79E
m68k_03b79e:
        bra.w (. + 20)
m68k_03b79e_end:
.org 0x3B7A2
m68k_03b7a2:
        bra.w (. + 2544)
m68k_03b7a2_end:
.org 0x3B7A6
m68k_03b7a6:
        bra.w (. + 4852)
m68k_03b7a6_end:
.org 0x3B7AA
m68k_03b7aa:
        bra.w (. + 6600)
m68k_03b7aa_end:
.org 0x3B7AE
m68k_03b7ae:
        bra.w (. + 4546)
m68k_03b7ae_end:
.org 0x3B7B2
m68k_03b7b2:
        move.w 0x80ea:w,%d0
m68k_03b7b2_end:
.org 0x3B7B6
m68k_03b7b6:
        asl.w #0x2,%d0
m68k_03b7b6_end:
.org 0x3B7B8
m68k_03b7b8:
        jmp 2(%pc, %d0.w)
m68k_03b7b8_end:
.org 0x3C192
m68k_03c192:
        move.w 0x80ea:w,%d0
m68k_03c192_end:
.org 0x3C196
m68k_03c196:
        asl.w #0x2,%d0
m68k_03c196_end:
.org 0x3C198
m68k_03c198:
        jmp 2(%pc, %d0.w)
m68k_03c198_end:
.org 0x3C970
m68k_03c970:
        move.w 0x80ea:w,%d0
m68k_03c970_end:
.org 0x3C974
m68k_03c974:
        asl.w #0x2,%d0
m68k_03c974_end:
.org 0x3C976
m68k_03c976:
        jmp 2(%pc, %d0.w)
m68k_03c976_end:
.org 0x3CA9A
m68k_03ca9a:
        move.w 0x80ea:w,%d0
m68k_03ca9a_end:
.org 0x3CA9E
m68k_03ca9e:
        asl.w #0x2,%d0
m68k_03ca9e_end:
.org 0x3CAA0
m68k_03caa0:
        jmp 2(%pc, %d0.w)
m68k_03caa0_end:
.org 0x3D172
m68k_03d172:
        move.w 0x80ea:w,%d0
m68k_03d172_end:
.org 0x3D176
m68k_03d176:
        asl.w #0x2,%d0
m68k_03d176_end:
.org 0x3D178
m68k_03d178:
        jmp 2(%pc, %d0.w)
m68k_03d178_end:
.org 0x3D970
m68k_03d970:
        btst.b #0x0,0x811c:w
m68k_03d970_end:
.org 0x3D976
m68k_03d976:
        beq.b (. + 16)
m68k_03d976_end:
.org 0x3D978
m68k_03d978:
        tst.w 0x8020:w
m68k_03d978_end:
.org 0x3D97C
m68k_03d97c:
        beq.b (. + 10)
m68k_03d97c_end:
.org 0x3D97E
m68k_03d97e:
        subq.w #0x2,0x8026:w
m68k_03d97e_end:
.org 0x3D982
m68k_03d982:
        subq.w #0x2,0x8020:w
m68k_03d982_end:
.org 0x3D986
m68k_03d986:
        btst.b #0x1,0x811c:w
m68k_03d986_end:
.org 0x3D98C
m68k_03d98c:
        beq.b (. + 18)
m68k_03d98c_end:
.org 0x3D98E
m68k_03d98e:
        cmpi.w #0x90,0x8020:w
m68k_03d98e_end:
.org 0x3D994
m68k_03d994:
        bcc.b (. + 10)
m68k_03d994_end:
.org 0x3D996
m68k_03d996:
        addq.w #0x2,0x8026:w
m68k_03d996_end:
.org 0x3D99A
m68k_03d99a:
        addq.w #0x2,0x8020:w
m68k_03d99a_end:
.org 0x3D99E
m68k_03d99e:
        rts
m68k_03d99e_end:
.org 0x3DCF8
m68k_03dcf8:
        bra.w (. + 28)
m68k_03dcf8_end:
.org 0x3DCFC
m68k_03dcfc:
        bra.w (. + 554)
m68k_03dcfc_end:
.org 0x3DD00
m68k_03dd00:
        bra.w (. + 1226)
m68k_03dd00_end:
.org 0x3DD04
m68k_03dd04:
        bra.w (. + 1282)
m68k_03dd04_end:
.org 0x3DD08
m68k_03dd08:
        bra.w (. + 1424)
m68k_03dd08_end:
.org 0x3DD0C
m68k_03dd0c:
        bra.w (. + 1550)
m68k_03dd0c_end:
.org 0x3DD10
m68k_03dd10:
        bra.w (. + 1586)
m68k_03dd10_end:
.org 0x3E1CA
m68k_03e1ca:
        btst.b #0x5,0x811f:w
m68k_03e1ca_end:
.org 0x3E1D0
m68k_03e1d0:
        beq.w (. + 28)
m68k_03e1d0_end:
.org 0x3E1D4
m68k_03e1d4:
        tst.w 0x8142:w
m68k_03e1d4_end:
.org 0x3E1D8
m68k_03e1d8:
        bne.w (. + -34)
m68k_03e1d8_end:
.org 0x3E1DC
m68k_03e1dc:
        bsr.w (. + 3842)
m68k_03e1dc_end:
.org 0x3E1E0
m68k_03e1e0:
        move.w #0x8,0x813a:w
m68k_03e1e0_end:
.org 0x3E1E6
m68k_03e1e6:
        move.w #0x5,0x813c:w
m68k_03e1e6_end:
.org 0x3E1EC
m68k_03e1ec:
        move.w 0x8020:w,%d0
m68k_03e1ec_end:
.org 0x3E1F0
m68k_03e1f0:
        addi.w #0x70,%d0
m68k_03e1f0_end:
.org 0x3E1F4
m68k_03e1f4:
        move.w #0xa0,%d1
m68k_03e1f4_end:
.org 0x3E1F8
m68k_03e1f8:
        bsr.w (. + 386)
m68k_03e1f8_end:
.org 0x3E1FC
m68k_03e1fc:
        move.w #0xc322,%d0
m68k_03e1fc_end:
.org 0x3E200
m68k_03e200:
        bsr.w (. + 554)
m68k_03e200_end:
.org 0x3E204
m68k_03e204:
        rts
m68k_03e204_end:
.org 0x3E206
m68k_03e206:
        tst.b 0x80da:w
m68k_03e206_end:
.org 0x3E20A
m68k_03e20a:
        beq.b (. + 20)
m68k_03e20a_end:
.org 0x3E20C
m68k_03e20c:
        cmpi.b #0x3,0x80da:w
m68k_03e20c_end:
.org 0x3E212
m68k_03e212:
        beq.b (. + 12)
m68k_03e212_end:
.org 0x3E214
m68k_03e214:
        move.w 0x8120:w,0x811e:w
m68k_03e214_end:
.org 0x3E21A
m68k_03e21a:
        bra.w (. + 28)
m68k_03e21a_end:
.org 0x3E21E
m68k_03e21e:
        move.w 0x8020:w,%d0
m68k_03e21e_end:
.org 0x3E222
m68k_03e222:
        addi.w #0x70,%d0
m68k_03e222_end:
.org 0x3E226
m68k_03e226:
        move.w #0x100,%d1
m68k_03e226_end:
.org 0x3E22A
m68k_03e22a:
        bsr.w (. + 336)
m68k_03e22a_end:
.org 0x3E22E
m68k_03e22e:
        move.w #0xc33a,%d0
m68k_03e22e_end:
.org 0x3E232
m68k_03e232:
        bsr.w (. + 504)
m68k_03e232_end:
.org 0x3E236
m68k_03e236:
        btst.b #0x5,0x811f:w
m68k_03e236_end:
.org 0x3E23C
m68k_03e23c:
        beq.w (. + 24)
m68k_03e23c_end:
.org 0x3E240
m68k_03e240:
        tst.w 0x8142:w
m68k_03e240_end:
.org 0x3E244
m68k_03e244:
        bne.w (. + -142)
m68k_03e244_end:
.org 0x3E248
m68k_03e248:
        bsr.w (. + 3734)
m68k_03e248_end:
.org 0x3E24C
m68k_03e24c:
        move.w #0x6,0x813c:w
m68k_03e24c_end:
.org 0x3E252
m68k_03e252:
        rts
m68k_03e252_end:
.org 0x3E298
m68k_03e298:
        move.w 0x8020:w,%d0
m68k_03e298_end:
.org 0x3E29C
m68k_03e29c:
        addi.w #0x70,%d0
m68k_03e29c_end:
.org 0x3E2A0
m68k_03e2a0:
        move.w #0x100,%d1
m68k_03e2a0_end:
.org 0x3E2A4
m68k_03e2a4:
        bsr.w (. + 214)
m68k_03e2a4_end:
.org 0x3E2A8
m68k_03e2a8:
        move.w #0xc33a,%d0
m68k_03e2a8_end:
.org 0x3E2AC
m68k_03e2ac:
        bsr.w (. + 382)
m68k_03e2ac_end:
.org 0x3E2B0
m68k_03e2b0:
        bsr.w (. + -92)
m68k_03e2b0_end:
.org 0x3E2B4
m68k_03e2b4:
        addq.w #0x1,0x8144:w
m68k_03e2b4_end:
.org 0x3E2B8
m68k_03e2b8:
        cmpi.w #0x40,0x8144:w
m68k_03e2b8_end:
.org 0x3E2BE
m68k_03e2be:
        bcs.w (. + 90)
m68k_03e2be_end:
.org 0x3E2C2
m68k_03e2c2:
        move.w #0x2700,%sr
m68k_03e2c2_end:
.org 0x3E2C6
m68k_03e2c6:
        move.w #0x8f02,0xc00004:l
m68k_03e2c6_end:
.org 0x3E2CE
m68k_03e2ce:
        move.l #0x60000002,0xc00004:l
m68k_03e2ce_end:
.org 0x3E2D8
m68k_03e2d8:
        lea.l 0xc00000:l,%a5
m68k_03e2d8_end:
.org 0x3E2DE
m68k_03e2de:
        move.w #0x3333,%d6
m68k_03e2de_end:
.org 0x3E2E2
m68k_03e2e2:
        move.w #0xd7f,%d7
m68k_03e2e2_end:
.org 0x3E2E6
m68k_03e2e6:
        move.w %d6,(%a5)
m68k_03e2e6_end:
.org 0x3E2E8
m68k_03e2e8:
        dbra %d7,(. + -2)
m68k_03e2e8_end:
.org 0x3E2EC
m68k_03e2ec:
        move.w #0xa000,0xff700c:l
m68k_03e2ec_end:
.org 0x3E2F4
m68k_03e2f4:
        move.l #0x3b41e,0xff700e:l
m68k_03e2f4_end:
.org 0x3E2FE
m68k_03e2fe:
        move.w #0x3,0xff7014:l
m68k_03e2fe_end:
.org 0x3E306
m68k_03e306:
        move.w #0x1,0xff7016:l
m68k_03e306_end:
.org 0x3E30E
m68k_03e30e:
        move.w #0x3,0x813c:w
m68k_03e30e_end:
.org 0x3E314
m68k_03e314:
        move.w #0x2500,%sr
m68k_03e314_end:
.org 0x3E318
m68k_03e318:
        rts
m68k_03e318_end:
.org 0x3E31A
m68k_03e31a:
        move.w 0x8020:w,%d0
m68k_03e31a_end:
.org 0x3E31E
m68k_03e31e:
        addi.w #0x70,%d0
m68k_03e31e_end:
.org 0x3E322
m68k_03e322:
        move.w #0xa0,%d1
m68k_03e322_end:
.org 0x3E326
m68k_03e326:
        bsr.w (. + 84)
m68k_03e326_end:
.org 0x3E32A
m68k_03e32a:
        btst.b #0x7,0x80c4:w
m68k_03e32a_end:
.org 0x3E330
m68k_03e330:
        beq.w (. + 16)
m68k_03e330_end:
.org 0x3E334
m68k_03e334:
        move.w #0x3,0x813a:w
m68k_03e334_end:
.org 0x3E33A
m68k_03e33a:
        move.w #0x3,0x813c:w
m68k_03e33a_end:
.org 0x3E340
m68k_03e340:
        rts
m68k_03e340_end:
.org 0x3E342
m68k_03e342:
        cmpi.b #0x1,0x80da:w
m68k_03e342_end:
.org 0x3E348
m68k_03e348:
        beq.b (. + 26)
m68k_03e348_end:
.org 0x3E34A
m68k_03e34a:
        cmpi.b #0x2,0x80da:w
m68k_03e34a_end:
.org 0x3E350
m68k_03e350:
        beq.b (. + 18)
m68k_03e350_end:
.org 0x3E352
m68k_03e352:
        move.w 0x8020:w,%d0
m68k_03e352_end:
.org 0x3E356
m68k_03e356:
        addi.w #0x70,%d0
m68k_03e356_end:
.org 0x3E35A
m68k_03e35a:
        move.w #0x100,%d1
m68k_03e35a_end:
.org 0x3E35E
m68k_03e35e:
        bsr.w (. + 28)
m68k_03e35e_end:
.org 0x3E362
m68k_03e362:
        btst.b #0x7,0x80c4:w
m68k_03e362_end:
.org 0x3E368
m68k_03e368:
        beq.w (. + 16)
m68k_03e368_end:
.org 0x3E36C
m68k_03e36c:
        move.w #0x3,0x813a:w
m68k_03e36c_end:
.org 0x3E372
m68k_03e372:
        move.w #0x3,0x813c:w
m68k_03e372_end:
.org 0x3E378
m68k_03e378:
        rts
m68k_03e378_end:
.org 0x3E37A
m68k_03e37a:
        lea.l 26(%pc),%a0
m68k_03e37a_end:
.org 0x3E37E
m68k_03e37e:
        nop
m68k_03e37e_end:
.org 0x3E380
m68k_03e380:
        move.w #0x104,%d2
m68k_03e380_end:
.org 0x3E384
m68k_03e384:
        moveq #0,%d3
m68k_03e384_end:
.org 0x3E386
m68k_03e386:
        move.w #0x400,%d4
m68k_03e386_end:
.org 0x3E38A
m68k_03e38a:
        jmp -12880(%pc)
m68k_03e38a_end:
.org 0x3E46C
m68k_03e46c:
        bra.w (. + 12)
m68k_03e46c_end:
.org 0x3E470
m68k_03e470:
        bra.w (. + 154)
m68k_03e470_end:
.org 0x3E474
m68k_03e474:
        bra.w (. + 360)
m68k_03e474_end:
.org 0x3E478
m68k_03e478:
        addq.w #0x1,0x8142:w
m68k_03e478_end:
.org 0x3E47C
m68k_03e47c:
        cmpi.w #0x20,0x8142:w
m68k_03e47c_end:
.org 0x3E482
m68k_03e482:
        bcs.w (. + 134)
m68k_03e482_end:
.org 0x3E486
m68k_03e486:
        move.w #0x2700,%sr
m68k_03e486_end:
.org 0x3E48A
m68k_03e48a:
        clr.w 0x8142:w
m68k_03e48a_end:
.org 0x3E48E
m68k_03e48e:
        addq.w #0x1,0x813c:w
m68k_03e48e_end:
.org 0x3E492
m68k_03e492:
        lea.l 0x4583f:l,%a0
m68k_03e492_end:
.org 0x3E498
m68k_03e498:
        lea.l 0xc000:l,%a1
m68k_03e498_end:
.org 0x3E49E
m68k_03e49e:
        move.l #0x80,%d5
m68k_03e49e_end:
.org 0x3E4A4
m68k_03e4a4:
        move.w #0x8000,0x8000:w
m68k_03e4a4_end:
.org 0x3E4AA
m68k_03e4aa:
        move.w #0x12,%d6
m68k_03e4aa_end:
.org 0x3E4AE
m68k_03e4ae:
        jsr -14810(%pc)
m68k_03e4ae_end:
.org 0x3E4B2
m68k_03e4b2:
        move.w #0x8f02,0xc00004:l
m68k_03e4b2_end:
.org 0x3E4BA
m68k_03e4ba:
        move.l #0x60000002,0xc00004:l
m68k_03e4ba_end:
.org 0x3E4C4
m68k_03e4c4:
        lea.l 0xc00000:l,%a5
m68k_03e4c4_end:
.org 0x3E4CA
m68k_03e4ca:
        move.w #0x3333,%d6
m68k_03e4ca_end:
.org 0x3E4CE
m68k_03e4ce:
        move.w #0xd7f,%d7
m68k_03e4ce_end:
.org 0x3E4D2
m68k_03e4d2:
        move.w %d6,(%a5)
m68k_03e4d2_end:
.org 0x3E4D4
m68k_03e4d4:
        dbra %d7,(. + -2)
m68k_03e4d4_end:
.org 0x3E4D8
m68k_03e4d8:
        move.w #0xa000,0xff700c:l
m68k_03e4d8_end:
.org 0x3E4E0
m68k_03e4e0:
        move.l #0x3b4c6,0xff700e:l
m68k_03e4e0_end:
.org 0x3E4EA
m68k_03e4ea:
        move.w #0x3,0xff7014:l
m68k_03e4ea_end:
.org 0x3E4F2
m68k_03e4f2:
        move.w #0x1,0xff7016:l
m68k_03e4f2_end:
.org 0x3E4FA
m68k_03e4fa:
        move.w #0x1,0x8116:w
m68k_03e4fa_end:
.org 0x3E500
m68k_03e500:
        bsr.w (. + 1506)
m68k_03e500_end:
.org 0x3E504
m68k_03e504:
        move.w #0x2500,%sr
m68k_03e504_end:
.org 0x3E508
m68k_03e508:
        rts
m68k_03e508_end:
.org 0x3E50A
m68k_03e50a:
        btst.b #0x5,0x811d:w
m68k_03e50a_end:
.org 0x3E510
m68k_03e510:
        beq.w (. + 50)
m68k_03e510_end:
.org 0x3E514
m68k_03e514:
        move.w #0xac,%d0
m68k_03e514_end:
.org 0x3E518
m68k_03e518:
        jsr 0x808a:l
m68k_03e518_end:
.org 0x3E51E
m68k_03e51e:
        tst.w 0x8142:w
m68k_03e51e_end:
.org 0x3E522
m68k_03e522:
        bne.w (. + 54)
m68k_03e522_end:
.org 0x3E526
m68k_03e526:
        clr.w 0x8142:w
m68k_03e526_end:
.org 0x3E52A
m68k_03e52a:
        move.w #0x7,0x813a:w
m68k_03e52a_end:
.org 0x3E530
m68k_03e530:
        clr.w 0x813c:w
m68k_03e530_end:
.org 0x3E534
m68k_03e534:
        clr.w 0x814c:w
m68k_03e534_end:
.org 0x3E538
m68k_03e538:
        bsr.w (. + 7652)
m68k_03e538_end:
.org 0x3E53C
m68k_03e53c:
        clr.w 0x840a:w
m68k_03e53c_end:
.org 0x3E540
m68k_03e540:
        rts
m68k_03e540_end:
.org 0x3E542
m68k_03e542:
        move.b 0x811d:w,%d0
m68k_03e542_end:
.org 0x3E546
m68k_03e546:
        andi.w #0x3,%d0
m68k_03e546_end:
.org 0x3E54A
m68k_03e54a:
        beq.w (. + -742)
m68k_03e54a_end:
.org 0x3E54E
m68k_03e54e:
        eori.w #0x1,0x8142:w
m68k_03e54e_end:
.org 0x3E554
m68k_03e554:
        bra.w (. + -752)
m68k_03e554_end:
.org 0x3E558
m68k_03e558:
        move.w #0x2700,%sr
m68k_03e558_end:
.org 0x3E55C
m68k_03e55c:
        cmpi.b #0x0,0x80da:w
m68k_03e55c_end:
.org 0x3E562
m68k_03e562:
        beq.b (. + 14)
m68k_03e562_end:
.org 0x3E564
m68k_03e564:
        cmpi.b #0x3,0x80da:w
m68k_03e564_end:
.org 0x3E56A
m68k_03e56a:
        beq.b (. + 6)
m68k_03e56a_end:
.org 0x3E56C
m68k_03e56c:
        bsr.w (. + 12972)
m68k_03e56c_end:
.org 0x3E570
m68k_03e570:
        bsr.w (. + 376)
m68k_03e570_end:
.org 0x3E574
m68k_03e574:
        bsr.w (. + 570)
m68k_03e574_end:
.org 0x3E578
m68k_03e578:
        bsr.w (. + 12960)
m68k_03e578_end:
.org 0x3E57C
m68k_03e57c:
        lea.l 0x816a:w,%a0
m68k_03e57c_end:
.org 0x3E580
m68k_03e580:
        move.w #0xf,%d1
m68k_03e580_end:
.org 0x3E584
m68k_03e584:
        move.w #0x160,%d0
m68k_03e584_end:
.org 0x3E588
m68k_03e588:
        sub.w 0x2(%a0),%d0
m68k_03e588_end:
.org 0x3E58C
m68k_03e58c:
        move.w %d0,0x2(%a0)
m68k_03e58c_end:
.org 0x3E590
m68k_03e590:
        move.w #0x1,0x6(%a0)
m68k_03e590_end:
.org 0x3E596
m68k_03e596:
        move.w #0x1,0x8(%a0)
m68k_03e596_end:
.org 0x3E59C
m68k_03e59c:
        adda.w #0x10,%a0
m68k_03e59c_end:
.org 0x3E5A0
m68k_03e5a0:
        dbra %d1,(. + -28)
m68k_03e5a0_end:
.org 0x3E5A4
m68k_03e5a4:
        bsr.w (. + 324)
m68k_03e5a4_end:
.org 0x3E5A8
m68k_03e5a8:
        bsr.w (. + 518)
m68k_03e5a8_end:
.org 0x3E5AC
m68k_03e5ac:
        bsr.w (. + 7536)
m68k_03e5ac_end:
.org 0x3E5B0
m68k_03e5b0:
        move.w #0x1,0x840a:w
m68k_03e5b0_end:
.org 0x3E5B6
m68k_03e5b6:
        clr.w 0x8142:w
m68k_03e5b6_end:
.org 0x3E5BA
m68k_03e5ba:
        move.w #0x0,0x8020:w
m68k_03e5ba_end:
.org 0x3E5C0
m68k_03e5c0:
        move.w #0x0,0x8024:w
m68k_03e5c0_end:
.org 0x3E5C6
m68k_03e5c6:
        move.w #0x8200,0x8040:w
m68k_03e5c6_end:
.org 0x3E5CC
m68k_03e5cc:
        move.w #0x8200,0x803a:w
m68k_03e5cc_end:
.org 0x3E5D2
m68k_03e5d2:
        addq.w #0x1,0x813c:w
m68k_03e5d2_end:
.org 0x3E5D6
m68k_03e5d6:
        move.w #0x2500,%sr
m68k_03e5d6_end:
.org 0x3E5DA
m68k_03e5da:
        rts
m68k_03e5da_end:
.org 0x3E5DC
m68k_03e5dc:
        cmpi.w #0x90,0x8020:w
m68k_03e5dc_end:
.org 0x3E5E2
m68k_03e5e2:
        bcs.w (. + 48)
m68k_03e5e2_end:
.org 0x3E5E6
m68k_03e5e6:
        move.w #0x0,0x8040:w
m68k_03e5e6_end:
.org 0x3E5EC
m68k_03e5ec:
        move.w #0x0,0x803a:w
m68k_03e5ec_end:
.org 0x3E5F2
m68k_03e5f2:
        addq.w #0x1,0x8142:w
m68k_03e5f2_end:
.org 0x3E5F6
m68k_03e5f6:
        cmpi.w #0x20,0x8142:w
m68k_03e5f6_end:
.org 0x3E5FC
m68k_03e5fc:
        bcs.w (. + 22)
m68k_03e5fc_end:
.org 0x3E600
m68k_03e600:
        clr.w 0x8142:w
m68k_03e600_end:
.org 0x3E604
m68k_03e604:
        move.w #0x8,0x813a:w
m68k_03e604_end:
.org 0x3E60A
m68k_03e60a:
        clr.w 0x813c:w
m68k_03e60a_end:
.org 0x3E60E
m68k_03e60e:
        clr.w 0x814c:w
m68k_03e60e_end:
.org 0x3E612
m68k_03e612:
        rts
m68k_03e612_end:
.org 0x3E622
m68k_03e622:
        bra.w (. + 130)
m68k_03e622_end:
.org 0x3E626
m68k_03e626:
        bra.w (. + 1278)
m68k_03e626_end:
.org 0x3E62A
m68k_03e62a:
        bra.w (. + 412)
m68k_03e62a_end:
.org 0x3E62E
m68k_03e62e:
        bra.w (. + 646)
m68k_03e62e_end:
.org 0x3E6A4
m68k_03e6a4:
        cmpi.b #0x1,0x80da:w
m68k_03e6a4_end:
.org 0x3E6AA
m68k_03e6aa:
        beq.b (. + 20)
m68k_03e6aa_end:
.org 0x3E6AC
m68k_03e6ac:
        cmpi.b #0x2,0x80da:w
m68k_03e6ac_end:
.org 0x3E6B2
m68k_03e6b2:
        beq.b (. + 12)
m68k_03e6b2_end:
.org 0x3E6B4
m68k_03e6b4:
        clr.w 0x813a:w
m68k_03e6b4_end:
.org 0x3E6B8
m68k_03e6b8:
        clr.w 0x813c:w
m68k_03e6b8_end:
.org 0x3E6BC
m68k_03e6bc:
        rts
m68k_03e6bc_end:
.org 0x3E6BE
m68k_03e6be:
        addq.w #0x1,0x8142:w
m68k_03e6be_end:
.org 0x3E6C2
m68k_03e6c2:
        cmpi.w #0x40,0x8142:w
m68k_03e6c2_end:
.org 0x3E6C8
m68k_03e6c8:
        bcs.w (. + 30)
m68k_03e6c8_end:
.org 0x3E6CC
m68k_03e6cc:
        bsr.w (. + 28)
m68k_03e6cc_end:
.org 0x3E6D0
m68k_03e6d0:
        tst.w 0x80e6:w
m68k_03e6d0_end:
.org 0x3E6D4
m68k_03e6d4:
        bne.b (. + 14)
m68k_03e6d4_end:
.org 0x3E6D6
m68k_03e6d6:
        bsr.w (. + 458)
m68k_03e6d6_end:
.org 0x3E6DA
m68k_03e6da:
        bsr.w (. + 4116)
m68k_03e6da_end:
.org 0x3E6DE
m68k_03e6de:
        bra.w (. + 498)
m68k_03e6de_end:
.org 0x3E6E2
m68k_03e6e2:
        bra.w (. + 826)
m68k_03e6e2_end:
.org 0x3E6E6
m68k_03e6e6:
        rts
m68k_03e6e6_end:
.org 0x3E6E8
m68k_03e6e8:
        move.w 0x80dc:w,%d0
m68k_03e6e8_end:
.org 0x3E6EC
m68k_03e6ec:
        move.w 0x80de:w,0x80dc:w
m68k_03e6ec_end:
.org 0x3E6F2
m68k_03e6f2:
        move.w %d0,0x80de:w
m68k_03e6f2_end:
.org 0x3E6F6
m68k_03e6f6:
        move.w 0x80e0:w,%d0
m68k_03e6f6_end:
.org 0x3E6FA
m68k_03e6fa:
        move.w 0x80e2:w,0x80e0:w
m68k_03e6fa_end:
.org 0x3E700
m68k_03e700:
        move.w %d0,0x80e2:w
m68k_03e700_end:
.org 0x3E704
m68k_03e704:
        move.w 0x80e4:w,%d0
m68k_03e704_end:
.org 0x3E708
m68k_03e708:
        move.w 0x80e6:w,0x80e4:w
m68k_03e708_end:
.org 0x3E70E
m68k_03e70e:
        move.w %d0,0x80e6:w
m68k_03e70e_end:
.org 0x3E712
m68k_03e712:
        move.w 0x80e8:w,%d0
m68k_03e712_end:
.org 0x3E716
m68k_03e716:
        move.w 0x80ea:w,0x80e8:w
m68k_03e716_end:
.org 0x3E71C
m68k_03e71c:
        move.w %d0,0x80ea:w
m68k_03e71c_end:
.org 0x3E720
m68k_03e720:
        move.w 0x80ec:w,%d0
m68k_03e720_end:
.org 0x3E724
m68k_03e724:
        move.w 0x80ee:w,0x80ec:w
m68k_03e724_end:
.org 0x3E72A
m68k_03e72a:
        move.w %d0,0x80ee:w
m68k_03e72a_end:
.org 0x3E72E
m68k_03e72e:
        move.w 0x80f0:w,%d0
m68k_03e72e_end:
.org 0x3E732
m68k_03e732:
        move.w 0x80f2:w,0x80f0:w
m68k_03e732_end:
.org 0x3E738
m68k_03e738:
        move.w %d0,0x80f2:w
m68k_03e738_end:
.org 0x3E73C
m68k_03e73c:
        move.w 0x80f4:w,%d0
m68k_03e73c_end:
.org 0x3E740
m68k_03e740:
        move.w 0x80fa:w,0x80f4:w
m68k_03e740_end:
.org 0x3E746
m68k_03e746:
        move.w %d0,0x80fa:w
m68k_03e746_end:
.org 0x3E74A
m68k_03e74a:
        move.w 0x80f6:w,%d0
m68k_03e74a_end:
.org 0x3E74E
m68k_03e74e:
        move.w 0x80fc:w,0x80f6:w
m68k_03e74e_end:
.org 0x3E754
m68k_03e754:
        move.w %d0,0x80fc:w
m68k_03e754_end:
.org 0x3E758
m68k_03e758:
        move.w 0x80f8:w,%d0
m68k_03e758_end:
.org 0x3E75C
m68k_03e75c:
        move.w 0x80fe:w,0x80f8:w
m68k_03e75c_end:
.org 0x3E762
m68k_03e762:
        move.w %d0,0x80fe:w
m68k_03e762_end:
.org 0x3E766
m68k_03e766:
        move.w 0x8100:w,%d0
m68k_03e766_end:
.org 0x3E76A
m68k_03e76a:
        move.w 0x8102:w,0x8100:w
m68k_03e76a_end:
.org 0x3E770
m68k_03e770:
        move.w %d0,0x8102:w
m68k_03e770_end:
.org 0x3E774
m68k_03e774:
        move.w 0x8104:w,%d0
m68k_03e774_end:
.org 0x3E778
m68k_03e778:
        move.w 0x8106:w,0x8104:w
m68k_03e778_end:
.org 0x3E77E
m68k_03e77e:
        move.w %d0,0x8106:w
m68k_03e77e_end:
.org 0x3E782
m68k_03e782:
        move.w 0x8108:w,%d0
m68k_03e782_end:
.org 0x3E786
m68k_03e786:
        move.w 0x810a:w,0x8108:w
m68k_03e786_end:
.org 0x3E78C
m68k_03e78c:
        move.w %d0,0x810a:w
m68k_03e78c_end:
.org 0x3E790
m68k_03e790:
        move.w 0x810c:w,%d0
m68k_03e790_end:
.org 0x3E794
m68k_03e794:
        move.w 0x810e:w,0x810c:w
m68k_03e794_end:
.org 0x3E79A
m68k_03e79a:
        move.w %d0,0x810e:w
m68k_03e79a_end:
.org 0x3E79E
m68k_03e79e:
        move.w 0x8110:w,%d0
m68k_03e79e_end:
.org 0x3E7A2
m68k_03e7a2:
        move.w 0x8112:w,0x8110:w
m68k_03e7a2_end:
.org 0x3E7A8
m68k_03e7a8:
        move.w %d0,0x8112:w
m68k_03e7a8_end:
.org 0x3E7AC
m68k_03e7ac:
        rts
m68k_03e7ac_end:
.org 0x3E7AE
m68k_03e7ae:
        move.w #0x7f,%d0
m68k_03e7ae_end:
.org 0x3E7B2
m68k_03e7b2:
        lea.l 0x816a:w,%a0
m68k_03e7b2_end:
.org 0x3E7B6
m68k_03e7b6:
        lea.l 0x826a:w,%a1
m68k_03e7b6_end:
.org 0x3E7BA
m68k_03e7ba:
        move.w (%a0),%d1
m68k_03e7ba_end:
.org 0x3E7BC
m68k_03e7bc:
        move.w (%a1),(%a0)+
m68k_03e7bc_end:
.org 0x3E7BE
m68k_03e7be:
        move.w %d1,(%a1)+
m68k_03e7be_end:
.org 0x3E7C0
m68k_03e7c0:
        dbra %d0,(. + -6)
m68k_03e7c0_end:
.org 0x3E7C4
m68k_03e7c4:
        rts
m68k_03e7c4_end:
.org 0x3E7C6
m68k_03e7c6:
        btst.b #0x5,0x811f:w
m68k_03e7c6_end:
.org 0x3E7CC
m68k_03e7cc:
        beq.w (. + 1266)
m68k_03e7cc_end:
.org 0x3E7D0
m68k_03e7d0:
        move.w #0xac,%d0
m68k_03e7d0_end:
.org 0x3E7D4
m68k_03e7d4:
        jsr 0x808a:l
m68k_03e7d4_end:
.org 0x3E7DA
m68k_03e7da:
        cmpi.w #0x2,0x8144:w
m68k_03e7da_end:
.org 0x3E7E0
m68k_03e7e0:
        bne.w (. + 1246)
m68k_03e7e0_end:
.org 0x3E7E4
m68k_03e7e4:
        move.w 0x80fa:w,%d0
m68k_03e7e4_end:
.org 0x3E7E8
m68k_03e7e8:
        add.w 0x80fc:w,%d0
m68k_03e7e8_end:
.org 0x3E7EC
m68k_03e7ec:
        add.w 0x80fe:w,%d0
m68k_03e7ec_end:
.org 0x3E7F0
m68k_03e7f0:
        cmp.w 0x80ea:w,%d0
m68k_03e7f0_end:
.org 0x3E7F4
m68k_03e7f4:
        bne.w (. + 1226)
m68k_03e7f4_end:
.org 0x3E7F8
m68k_03e7f8:
        addq.w #0x1,0x813c:w
m68k_03e7f8_end:
.org 0x3E7FC
m68k_03e7fc:
        move.w #0x2700,%sr
m68k_03e7fc_end:
.org 0x3E800
m68k_03e800:
        move.w 0x8106:w,%d0
m68k_03e800_end:
.org 0x3E804
m68k_03e804:
        move.w 0x8102:w,%d1
m68k_03e804_end:
.org 0x3E808
m68k_03e808:
        mulu.w %d0,%d1
m68k_03e808_end:
.org 0x3E80A
m68k_03e80a:
        divu.w #0x64,%d1
m68k_03e80a_end:
.org 0x3E80E
m68k_03e80e:
        move.w #0xe,%d0
m68k_03e80e_end:
.org 0x3E812
m68k_03e812:
        move.w 0x80f2:w,%d2
m68k_03e812_end:
.org 0x3E816
m68k_03e816:
        lea.l 0x817a:w,%a6
m68k_03e816_end:
.org 0x3E81A
m68k_03e81a:
        move.w %d1,0xc(%a6)
m68k_03e81a_end:
.org 0x3E81E
m68k_03e81e:
        move.w 0x80ee:w,0xe(%a6)
m68k_03e81e_end:
.org 0x3E824
m68k_03e824:
        tst.w %d2
m68k_03e824_end:
.org 0x3E826
m68k_03e826:
        beq.w (. + 10)
m68k_03e826_end:
.org 0x3E82A
m68k_03e82a:
        subq.w #0x1,%d2
m68k_03e82a_end:
.org 0x3E82C
m68k_03e82c:
        addq.w #0x1,0xe(%a6)
m68k_03e82c_end:
.org 0x3E830
m68k_03e830:
        adda.w #0x10,%a6
m68k_03e830_end:
.org 0x3E834
m68k_03e834:
        dbra %d0,(. + -26)
m68k_03e834_end:
.org 0x3E838
m68k_03e838:
        bsr.w (. + 104)
m68k_03e838_end:
.org 0x3E83C
m68k_03e83c:
        move.l #0x40000003,0xc00004:l
m68k_03e83c_end:
.org 0x3E846
m68k_03e846:
        lea.l 0xc00000:l,%a5
m68k_03e846_end:
.org 0x3E84C
m68k_03e84c:
        move.w #0x400,%d6
m68k_03e84c_end:
.org 0x3E850
m68k_03e850:
        move.w #0x4bf,%d7
m68k_03e850_end:
.org 0x3E854
m68k_03e854:
        move.w %d6,(%a5)
m68k_03e854_end:
.org 0x3E856
m68k_03e856:
        dbra %d7,(. + -2)
m68k_03e856_end:
.org 0x3E85A
m68k_03e85a:
        move.l #0x60000002,0xc00004:l
m68k_03e85a_end:
.org 0x3E864
m68k_03e864:
        lea.l 0xc00000:l,%a5
m68k_03e864_end:
.org 0x3E86A
m68k_03e86a:
        move.w #0x3333,%d6
m68k_03e86a_end:
.org 0x3E86E
m68k_03e86e:
        move.w #0xd7f,%d7
m68k_03e86e_end:
.org 0x3E872
m68k_03e872:
        move.w %d6,(%a5)
m68k_03e872_end:
.org 0x3E874
m68k_03e874:
        dbra %d7,(. + -2)
m68k_03e874_end:
.org 0x3E878
m68k_03e878:
        move.w #0xa000,0xff700c:l
m68k_03e878_end:
.org 0x3E880
m68k_03e880:
        move.l #0x3b34a,0xff700e:l
m68k_03e880_end:
.org 0x3E88A
m68k_03e88a:
        move.w #0x3,0xff7014:l
m68k_03e88a_end:
.org 0x3E892
m68k_03e892:
        move.w #0x1,0xff7016:l
m68k_03e892_end:
.org 0x3E89A
m68k_03e89a:
        move.w #0x2500,%sr
m68k_03e89a_end:
.org 0x3E89E
m68k_03e89e:
        rts
m68k_03e89e_end:
.org 0x3E8A0
m68k_03e8a0:
        move.w 0x8106:w,%d0
m68k_03e8a0_end:
.org 0x3E8A4
m68k_03e8a4:
        add.w 0x810a:w,%d0
m68k_03e8a4_end:
.org 0x3E8A8
m68k_03e8a8:
        move.w %d0,0x8176:w
m68k_03e8a8_end:
.org 0x3E8AC
m68k_03e8ac:
        move.w 0x810e:w,0x8178:w
m68k_03e8ac_end:
.org 0x3E8B2
m68k_03e8b2:
        rts
m68k_03e8b2_end:
.org 0x3E8B4
m68k_03e8b4:
        bsr.w (. + 3598)
m68k_03e8b4_end:
.org 0x3E8B8
m68k_03e8b8:
        move.b 0x811f:w,%d0
m68k_03e8b8_end:
.org 0x3E8BC
m68k_03e8bc:
        andi.w #0xc,%d0
m68k_03e8bc_end:
.org 0x3E8C0
m68k_03e8c0:
        beq.b (. + 8)
m68k_03e8c0_end:
.org 0x3E8C2
m68k_03e8c2:
        bsr.w (. + 6746)
m68k_03e8c2_end:
.org 0x3E8C6
m68k_03e8c6:
        rts
m68k_03e8c6_end:
.org 0x3E8C8
m68k_03e8c8:
        btst.b #0x5,0x811f:w
m68k_03e8c8_end:
.org 0x3E8CE
m68k_03e8ce:
        beq.b (. + 34)
m68k_03e8ce_end:
.org 0x3E8D0
m68k_03e8d0:
        clr.w 0x813a:w
m68k_03e8d0_end:
.org 0x3E8D4
m68k_03e8d4:
        clr.w 0x813c:w
m68k_03e8d4_end:
.org 0x3E8D8
m68k_03e8d8:
        clr.w 0x814c:w
m68k_03e8d8_end:
.org 0x3E8DC
m68k_03e8dc:
        bsr.w (. + 6720)
m68k_03e8dc_end:
.org 0x3E8E0
m68k_03e8e0:
        bsr.w (. + -504)
m68k_03e8e0_end:
.org 0x3E8E4
m68k_03e8e4:
        clr.w 0x8142:w
m68k_03e8e4_end:
.org 0x3E8E8
m68k_03e8e8:
        clr.w 0x8144:w
m68k_03e8e8_end:
.org 0x3E8EC
m68k_03e8ec:
        clr.w 0x8146:w
m68k_03e8ec_end:
.org 0x3E8F0
m68k_03e8f0:
        rts
m68k_03e8f0_end:
.org 0x3E900
m68k_03e900:
        bra.w (. + 138)
m68k_03e900_end:
.org 0x3E904
m68k_03e904:
        bra.w (. + 182)
m68k_03e904_end:
.org 0x3E908
m68k_03e908:
        bra.w (. + 540)
m68k_03e908_end:
.org 0x3E90C
m68k_03e90c:
        bra.w (. + 728)
m68k_03e90c_end:
.org 0x3E910
m68k_03e910:
        bra.w (. + 972)
m68k_03e910_end:
.org 0x3E914
m68k_03e914:
        bra.w (. + 968)
m68k_03e914_end:
.org 0x3E918
m68k_03e918:
        bra.w (. + 1012)
m68k_03e918_end:
.org 0x3E98A
m68k_03e98a:
        addq.w #0x1,0x8142:w
m68k_03e98a_end:
.org 0x3E98E
m68k_03e98e:
        cmpi.w #0x40,0x8142:w
m68k_03e98e_end:
.org 0x3E994
m68k_03e994:
        bcs.w (. + 332)
m68k_03e994_end:
.org 0x3E998
m68k_03e998:
        clr.w 0x8142:w
m68k_03e998_end:
.org 0x3E99C
m68k_03e99c:
        move.w #0x0,0x8020:w
m68k_03e99c_end:
.org 0x3E9A2
m68k_03e9a2:
        move.w #0x0,0x8024:w
m68k_03e9a2_end:
.org 0x3E9A8
m68k_03e9a8:
        move.w #0x8200,0x8040:w
m68k_03e9a8_end:
.org 0x3E9AE
m68k_03e9ae:
        move.w #0x8200,0x803a:w
m68k_03e9ae_end:
.org 0x3E9B4
m68k_03e9b4:
        addq.w #0x1,0x813c:w
m68k_03e9b4_end:
.org 0x3E9B8
m68k_03e9b8:
        rts
m68k_03e9b8_end:
.org 0x3E9BA
m68k_03e9ba:
        cmpi.w #0x90,0x8020:w
m68k_03e9ba_end:
.org 0x3E9C0
m68k_03e9c0:
        bcs.w (. + 288)
m68k_03e9c0_end:
.org 0x3E9C4
m68k_03e9c4:
        move.w #0x0,0x8040:w
m68k_03e9c4_end:
.org 0x3E9CA
m68k_03e9ca:
        move.w #0x0,0x803a:w
m68k_03e9ca_end:
.org 0x3E9D0
m68k_03e9d0:
        addq.w #0x1,0x8142:w
m68k_03e9d0_end:
.org 0x3E9D4
m68k_03e9d4:
        cmpi.w #0x20,0x8142:w
m68k_03e9d4_end:
.org 0x3E9DA
m68k_03e9da:
        bcs.w (. + 262)
m68k_03e9da_end:
.org 0x3E9DE
m68k_03e9de:
        tst.w 0x80e6:w
m68k_03e9de_end:
.org 0x3E9E2
m68k_03e9e2:
        bne.b (. + 58)
m68k_03e9e2_end:
.org 0x3E9E4
m68k_03e9e4:
        clr.w 0x80ea:w
m68k_03e9e4_end:
.org 0x3E9E8
m68k_03e9e8:
        clr.w 0x80ee:w
m68k_03e9e8_end:
.org 0x3E9EC
m68k_03e9ec:
        clr.w 0x80f2:w
m68k_03e9ec_end:
.org 0x3E9F0
m68k_03e9f0:
        clr.w 0x80fa:w
m68k_03e9f0_end:
.org 0x3E9F4
m68k_03e9f4:
        clr.w 0x80fc:w
m68k_03e9f4_end:
.org 0x3E9F8
m68k_03e9f8:
        clr.w 0x80fe:w
m68k_03e9f8_end:
.org 0x3E9FC
m68k_03e9fc:
        clr.w 0x8142:w
m68k_03e9fc_end:
.org 0x3EA00
m68k_03ea00:
        bsr.w (. + 712)
m68k_03ea00_end:
.org 0x3EA04
m68k_03ea04:
        bsr.w (. + 3140)
m68k_03ea04_end:
.org 0x3EA08
m68k_03ea08:
        move.w #0x8,0x813a:w
m68k_03ea08_end:
.org 0x3EA0E
m68k_03ea0e:
        clr.w 0x813c:w
m68k_03ea0e_end:
.org 0x3EA12
m68k_03ea12:
        clr.w 0x814c:w
m68k_03ea12_end:
.org 0x3EA16
m68k_03ea16:
        bsr.w (. + 6406)
m68k_03ea16_end:
.org 0x3EA1A
m68k_03ea1a:
        rts
m68k_03ea1a_end:
.org 0x3EA1C
m68k_03ea1c:
        move.w #0x2700,%sr
m68k_03ea1c_end:
.org 0x3EA20
m68k_03ea20:
        clr.w 0x8142:w
m68k_03ea20_end:
.org 0x3EA24
m68k_03ea24:
        addq.w #0x1,0x813c:w
m68k_03ea24_end:
.org 0x3EA28
m68k_03ea28:
        jsr 2612(%pc)
m68k_03ea28_end:
.org 0x3EA2C
m68k_03ea2c:
        nop
m68k_03ea2c_end:
.org 0x3EA2E
m68k_03ea2e:
        move.l #0x50000002,0xc00004:l
m68k_03ea2e_end:
.org 0x3EA38
m68k_03ea38:
        lea.l 0xc00000:l,%a5
m68k_03ea38_end:
.org 0x3EA3E
m68k_03ea3e:
        move.w #0x3333,%d6
m68k_03ea3e_end:
.org 0x3EA42
m68k_03ea42:
        move.w #0xbf,%d7
m68k_03ea42_end:
.org 0x3EA46
m68k_03ea46:
        move.w %d6,(%a5)
m68k_03ea46_end:
.org 0x3EA48
m68k_03ea48:
        dbra %d7,(. + -2)
m68k_03ea48_end:
.org 0x3EA4C
m68k_03ea4c:
        move.l #0x50000002,0xc00004:l
m68k_03ea4c_end:
.org 0x3EA56
m68k_03ea56:
        move.w 0x80e2:w,%d7
m68k_03ea56_end:
.org 0x3EA5A
m68k_03ea5a:
        move.w #0x3,%d0
m68k_03ea5a_end:
.org 0x3EA5E
m68k_03ea5e:
        move.w #0x1,%d1
m68k_03ea5e_end:
.org 0x3EA62
m68k_03ea62:
        bsr.w (. + 6240)
m68k_03ea62_end:
.org 0x3EA66
m68k_03ea66:
        lea.l 0x44c6f:l,%a0
m68k_03ea66_end:
.org 0x3EA6C
m68k_03ea6c:
        lea.l 0xc000:l,%a1
m68k_03ea6c_end:
.org 0x3EA72
m68k_03ea72:
        move.l #0x80,%d5
m68k_03ea72_end:
.org 0x3EA78
m68k_03ea78:
        move.w #0x8000,0x8000:w
m68k_03ea78_end:
.org 0x3EA7E
m68k_03ea7e:
        move.w #0x12,%d6
m68k_03ea7e_end:
.org 0x3EA82
m68k_03ea82:
        jsr -16302(%pc)
m68k_03ea82_end:
.org 0x3EA86
m68k_03ea86:
        bsr.w (. + 3696)
m68k_03ea86_end:
.org 0x3EA8A
m68k_03ea8a:
        move.w #0x8f02,0xc00004:l
m68k_03ea8a_end:
.org 0x3EA92
m68k_03ea92:
        move.l #0x60000002,0xc00004:l
m68k_03ea92_end:
.org 0x3EA9C
m68k_03ea9c:
        lea.l 0xc00000:l,%a5
m68k_03ea9c_end:
.org 0x3EAA2
m68k_03eaa2:
        move.w #0x3333,%d6
m68k_03eaa2_end:
.org 0x3EAA6
m68k_03eaa6:
        move.w #0xd7f,%d7
m68k_03eaa6_end:
.org 0x3EAAA
m68k_03eaaa:
        move.w %d6,(%a5)
m68k_03eaaa_end:
.org 0x3EAAC
m68k_03eaac:
        dbra %d7,(. + -2)
m68k_03eaac_end:
.org 0x3EAB0
m68k_03eab0:
        move.w #0xa000,0xff700c:l
m68k_03eab0_end:
.org 0x3EAB8
m68k_03eab8:
        move.l #0x3b320,0xff700e:l
m68k_03eab8_end:
.org 0x3EAC2
m68k_03eac2:
        move.w #0x3,0xff7014:l
m68k_03eac2_end:
.org 0x3EACA
m68k_03eaca:
        move.w #0x1,0xff7016:l
m68k_03eaca_end:
.org 0x3EAD2
m68k_03ead2:
        move.w #0x1,0x8116:w
m68k_03ead2_end:
.org 0x3EAD8
m68k_03ead8:
        bsr.w (. + 10)
m68k_03ead8_end:
.org 0x3EADC
m68k_03eadc:
        move.w #0x2500,%sr
m68k_03eadc_end:
.org 0x3EAE0
m68k_03eae0:
        rts
m68k_03eae0_end:
.org 0x3EB24
m68k_03eb24:
        bsr.w (. + 2548)
m68k_03eb24_end:
.org 0x3EB28
m68k_03eb28:
        bsr.w (. + 2358)
m68k_03eb28_end:
.org 0x3EB2C
m68k_03eb2c:
        bsr.w (. + 3530)
m68k_03eb2c_end:
.org 0x3EB30
m68k_03eb30:
        btst.b #0x5,0x811f:w
m68k_03eb30_end:
.org 0x3EB36
m68k_03eb36:
        beq.b (. + -86)
m68k_03eb36_end:
.org 0x3EB38
m68k_03eb38:
        move.w #0xac,%d0
m68k_03eb38_end:
.org 0x3EB3C
m68k_03eb3c:
        jsr 0x808a:l
m68k_03eb3c_end:
.org 0x3EB42
m68k_03eb42:
        addq.w #0x1,0x813c:w
m68k_03eb42_end:
.org 0x3EB46
m68k_03eb46:
        clr.w 0x8144:w
m68k_03eb46_end:
.org 0x3EB4A
m68k_03eb4a:
        cmpi.b #0x3,0x80db:w
m68k_03eb4a_end:
.org 0x3EB50
m68k_03eb50:
        bne.b (. + 30)
m68k_03eb50_end:
.org 0x3EB52
m68k_03eb52:
        clr.w 0x80fa:w
m68k_03eb52_end:
.org 0x3EB56
m68k_03eb56:
        move.w 0x80ea:w,0x80fc:w
m68k_03eb56_end:
.org 0x3EB5C
m68k_03eb5c:
        clr.w 0x80fe:w
m68k_03eb5c_end:
.org 0x3EB60
m68k_03eb60:
        cmpi.w #0x7,0x813a:w
m68k_03eb60_end:
.org 0x3EB66
m68k_03eb66:
        beq.w (. + -898)
m68k_03eb66_end:
.org 0x3EB6A
m68k_03eb6a:
        bra.w (. + 152)
m68k_03eb6a_end:
.org 0x3EB6E
m68k_03eb6e:
        move.w #0x2700,%sr
m68k_03eb6e_end:
.org 0x3EB72
m68k_03eb72:
        lea.l 0x44dc6:l,%a0
m68k_03eb72_end:
.org 0x3EB78
m68k_03eb78:
        lea.l 0xc000:l,%a1
m68k_03eb78_end:
.org 0x3EB7E
m68k_03eb7e:
        move.l #0x80,%d5
m68k_03eb7e_end:
.org 0x3EB84
m68k_03eb84:
        move.w #0x8000,0x8000:w
m68k_03eb84_end:
.org 0x3EB8A
m68k_03eb8a:
        move.w #0x12,%d6
m68k_03eb8a_end:
.org 0x3EB8E
m68k_03eb8e:
        jsr -16570(%pc)
m68k_03eb8e_end:
.org 0x3EB92
m68k_03eb92:
        bsr.w (. + 3500)
m68k_03eb92_end:
.org 0x3EB96
m68k_03eb96:
        move.w #0x8f02,0xc00004:l
m68k_03eb96_end:
.org 0x3EB9E
m68k_03eb9e:
        move.l #0x60000002,0xc00004:l
m68k_03eb9e_end:
.org 0x3EBA8
m68k_03eba8:
        lea.l 0xc00000:l,%a5
m68k_03eba8_end:
.org 0x3EBAE
m68k_03ebae:
        move.w #0x3333,%d6
m68k_03ebae_end:
.org 0x3EBB2
m68k_03ebb2:
        move.w #0xd7f,%d7
m68k_03ebb2_end:
.org 0x3EBB6
m68k_03ebb6:
        move.w %d6,(%a5)
m68k_03ebb6_end:
.org 0x3EBB8
m68k_03ebb8:
        dbra %d7,(. + -2)
m68k_03ebb8_end:
.org 0x3EBBC
m68k_03ebbc:
        move.w #0xa000,0xff700c:l
m68k_03ebbc_end:
.org 0x3EBC4
m68k_03ebc4:
        move.l #0x3b336,0xff700e:l
m68k_03ebc4_end:
.org 0x3EBCE
m68k_03ebce:
        move.w #0x3,0xff7014:l
m68k_03ebce_end:
.org 0x3EBD6
m68k_03ebd6:
        move.w #0x1,0xff7016:l
m68k_03ebd6_end:
.org 0x3EBDE
m68k_03ebde:
        move.w #0x2500,%sr
m68k_03ebde_end:
.org 0x3EBE2
m68k_03ebe2:
        rts
m68k_03ebe2_end:
.org 0x3EBE4
m68k_03ebe4:
        btst.b #0x5,0x811f:w
m68k_03ebe4_end:
.org 0x3EBEA
m68k_03ebea:
        beq.w (. + 212)
m68k_03ebea_end:
.org 0x3EBEE
m68k_03ebee:
        move.w #0xac,%d0
m68k_03ebee_end:
.org 0x3EBF2
m68k_03ebf2:
        jsr 0x808a:l
m68k_03ebf2_end:
.org 0x3EBF8
m68k_03ebf8:
        cmpi.w #0x2,0x8144:w
m68k_03ebf8_end:
.org 0x3EBFE
m68k_03ebfe:
        bne.w (. + 192)
m68k_03ebfe_end:
.org 0x3EC02
m68k_03ec02:
        move.w 0x80fa:w,%d0
m68k_03ec02_end:
.org 0x3EC06
m68k_03ec06:
        add.w 0x80fc:w,%d0
m68k_03ec06_end:
.org 0x3EC0A
m68k_03ec0a:
        add.w 0x80fe:w,%d0
m68k_03ec0a_end:
.org 0x3EC0E
m68k_03ec0e:
        cmp.w 0x80ea:w,%d0
m68k_03ec0e_end:
.org 0x3EC12
m68k_03ec12:
        bne.w (. + 172)
m68k_03ec12_end:
.org 0x3EC16
m68k_03ec16:
        move.w #0x2700,%sr
m68k_03ec16_end:
.org 0x3EC1A
m68k_03ec1a:
        move.w 0x8106:w,%d0
m68k_03ec1a_end:
.org 0x3EC1E
m68k_03ec1e:
        move.w 0x8102:w,%d1
m68k_03ec1e_end:
.org 0x3EC22
m68k_03ec22:
        mulu.w %d0,%d1
m68k_03ec22_end:
.org 0x3EC24
m68k_03ec24:
        divu.w #0x64,%d1
m68k_03ec24_end:
.org 0x3EC28
m68k_03ec28:
        move.w #0xe,%d0
m68k_03ec28_end:
.org 0x3EC2C
m68k_03ec2c:
        move.w 0x80f2:w,%d2
m68k_03ec2c_end:
.org 0x3EC30
m68k_03ec30:
        lea.l 0x827a:w,%a6
m68k_03ec30_end:
.org 0x3EC34
m68k_03ec34:
        move.w %d1,0xc(%a6)
m68k_03ec34_end:
.org 0x3EC38
m68k_03ec38:
        move.w 0x80ee:w,0xe(%a6)
m68k_03ec38_end:
.org 0x3EC3E
m68k_03ec3e:
        tst.w %d2
m68k_03ec3e_end:
.org 0x3EC40
m68k_03ec40:
        beq.w (. + 10)
m68k_03ec40_end:
.org 0x3EC44
m68k_03ec44:
        subq.w #0x1,%d2
m68k_03ec44_end:
.org 0x3EC46
m68k_03ec46:
        addq.w #0x1,0xe(%a6)
m68k_03ec46_end:
.org 0x3EC4A
m68k_03ec4a:
        adda.w #0x10,%a6
m68k_03ec4a_end:
.org 0x3EC4E
m68k_03ec4e:
        dbra %d0,(. + -26)
m68k_03ec4e_end:
.org 0x3EC52
m68k_03ec52:
        bsr.w (. + 118)
m68k_03ec52_end:
.org 0x3EC56
m68k_03ec56:
        addq.w #0x1,0x813c:w
m68k_03ec56_end:
.org 0x3EC5A
m68k_03ec5a:
        move.l #0x40000003,0xc00004:l
m68k_03ec5a_end:
.org 0x3EC64
m68k_03ec64:
        lea.l 0xc00000:l,%a5
m68k_03ec64_end:
.org 0x3EC6A
m68k_03ec6a:
        move.w #0x400,%d6
m68k_03ec6a_end:
.org 0x3EC6E
m68k_03ec6e:
        move.w #0x4bf,%d7
m68k_03ec6e_end:
.org 0x3EC72
m68k_03ec72:
        move.w %d6,(%a5)
m68k_03ec72_end:
.org 0x3EC74
m68k_03ec74:
        dbra %d7,(. + -2)
m68k_03ec74_end:
.org 0x3EC78
m68k_03ec78:
        move.l #0x60000002,0xc00004:l
m68k_03ec78_end:
.org 0x3EC82
m68k_03ec82:
        lea.l 0xc00000:l,%a5
m68k_03ec82_end:
.org 0x3EC88
m68k_03ec88:
        move.w #0x3333,%d6
m68k_03ec88_end:
.org 0x3EC8C
m68k_03ec8c:
        move.w #0xd7f,%d7
m68k_03ec8c_end:
.org 0x3EC90
m68k_03ec90:
        move.w %d6,(%a5)
m68k_03ec90_end:
.org 0x3EC92
m68k_03ec92:
        dbra %d7,(. + -2)
m68k_03ec92_end:
.org 0x3EC96
m68k_03ec96:
        move.w #0xa000,0xff700c:l
m68k_03ec96_end:
.org 0x3EC9E
m68k_03ec9e:
        move.l #0x3b34a,0xff700e:l
m68k_03ec9e_end:
.org 0x3ECA8
m68k_03eca8:
        move.w #0x3,0xff7014:l
m68k_03eca8_end:
.org 0x3ECB0
m68k_03ecb0:
        move.w #0x1,0xff7016:l
m68k_03ecb0_end:
.org 0x3ECB8
m68k_03ecb8:
        move.w #0x2500,%sr
m68k_03ecb8_end:
.org 0x3ECBC
m68k_03ecbc:
        rts
m68k_03ecbc_end:
.org 0x3ECBE
m68k_03ecbe:
        bsr.w (. + 2164)
m68k_03ecbe_end:
.org 0x3ECC2
m68k_03ecc2:
        bsr.w (. + 3196)
m68k_03ecc2_end:
.org 0x3ECC6
m68k_03ecc6:
        rts
m68k_03ecc6_end:
.org 0x3ECC8
m68k_03ecc8:
        move.w 0x8106:w,%d0
m68k_03ecc8_end:
.org 0x3ECCC
m68k_03eccc:
        add.w 0x810a:w,%d0
m68k_03eccc_end:
.org 0x3ECD0
m68k_03ecd0:
        move.w %d0,0x8276:w
m68k_03ecd0_end:
.org 0x3ECD4
m68k_03ecd4:
        move.w 0x810e:w,0x8278:w
m68k_03ecd4_end:
.org 0x3ECDA
m68k_03ecda:
        rts
m68k_03ecda_end:
.org 0x3ECDC
m68k_03ecdc:
        bsr.w (. + 2368)
m68k_03ecdc_end:
.org 0x3ECE0
m68k_03ece0:
        move.b 0x811f:w,%d0
m68k_03ece0_end:
.org 0x3ECE4
m68k_03ece4:
        andi.w #0xc,%d0
m68k_03ece4_end:
.org 0x3ECE8
m68k_03ece8:
        beq.b (. + 8)
m68k_03ece8_end:
.org 0x3ECEA
m68k_03ecea:
        bsr.w (. + 5682)
m68k_03ecea_end:
.org 0x3ECEE
m68k_03ecee:
        rts
m68k_03ecee_end:
.org 0x3ECF0
m68k_03ecf0:
        btst.b #0x5,0x811f:w
m68k_03ecf0_end:
.org 0x3ECF6
m68k_03ecf6:
        beq.b (. + 20)
m68k_03ecf6_end:
.org 0x3ECF8
m68k_03ecf8:
        move.w #0x8,0x813a:w
m68k_03ecf8_end:
.org 0x3ECFE
m68k_03ecfe:
        clr.w 0x813c:w
m68k_03ecfe_end:
.org 0x3ED02
m68k_03ed02:
        clr.w 0x814c:w
m68k_03ed02_end:
.org 0x3ED06
m68k_03ed06:
        bsr.w (. + 5654)
m68k_03ed06_end:
.org 0x3ED0A
m68k_03ed0a:
        rts
m68k_03ed0a_end:
.org 0x3ED0C
m68k_03ed0c:
        jsr -5022(%pc)
m68k_03ed0c_end:
.org 0x3ED10
m68k_03ed10:
        move.b 0x811f:w,%d0
m68k_03ed10_end:
.org 0x3ED14
m68k_03ed14:
        andi.b #0x20,%d0
m68k_03ed14_end:
.org 0x3ED18
m68k_03ed18:
        bne.b (. + 36)
m68k_03ed18_end:
.org 0x3ED1A
m68k_03ed1a:
        tst.b 0x80da:w
m68k_03ed1a_end:
.org 0x3ED1E
m68k_03ed1e:
        beq.w (. + 302)
m68k_03ed1e_end:
.org 0x3ED22
m68k_03ed22:
        move.b 0x8121:w,%d0
m68k_03ed22_end:
.org 0x3ED26
m68k_03ed26:
        andi.b #0x20,%d0
m68k_03ed26_end:
.org 0x3ED2A
m68k_03ed2a:
        beq.w (. + 290)
m68k_03ed2a_end:
.org 0x3ED2E
m68k_03ed2e:
        move.w #0x1,0x8144:w
m68k_03ed2e_end:
.org 0x3ED34
m68k_03ed34:
        clr.w 0x8116:w
m68k_03ed34_end:
.org 0x3ED38
m68k_03ed38:
        bra.w (. + 14)
m68k_03ed38_end:
.org 0x3ED3C
m68k_03ed3c:
        clr.w 0x8144:w
m68k_03ed3c_end:
.org 0x3ED40
m68k_03ed40:
        move.w #0x1,0x8116:w
m68k_03ed40_end:
.org 0x3ED46
m68k_03ed46:
        move.w #0xad,%d0
m68k_03ed46_end:
.org 0x3ED4A
m68k_03ed4a:
        jsr 0x808a:l
m68k_03ed4a_end:
.org 0x3ED50
m68k_03ed50:
        move.w #0x2700,%sr
m68k_03ed50_end:
.org 0x3ED54
m68k_03ed54:
        move.l #0x50000002,0xc00004:l
m68k_03ed54_end:
.org 0x3ED5E
m68k_03ed5e:
        lea.l 0xc00000:l,%a5
m68k_03ed5e_end:
.org 0x3ED64
m68k_03ed64:
        move.w #0x3333,%d6
m68k_03ed64_end:
.org 0x3ED68
m68k_03ed68:
        move.w #0xbf,%d7
m68k_03ed68_end:
.org 0x3ED6C
m68k_03ed6c:
        move.w %d6,(%a5)
m68k_03ed6c_end:
.org 0x3ED6E
m68k_03ed6e:
        dbra %d7,(. + -2)
m68k_03ed6e_end:
.org 0x3ED72
m68k_03ed72:
        move.l #0x50000002,0xc00004:l
m68k_03ed72_end:
.org 0x3ED7C
m68k_03ed7c:
        move.w 0x80e0:w,%d7
m68k_03ed7c_end:
.org 0x3ED80
m68k_03ed80:
        move.w #0x3,%d0
m68k_03ed80_end:
.org 0x3ED84
m68k_03ed84:
        move.w #0x1,%d1
m68k_03ed84_end:
.org 0x3ED88
m68k_03ed88:
        bsr.w (. + 5434)
m68k_03ed88_end:
.org 0x3ED8C
m68k_03ed8c:
        move.l #0x51800002,0xc00004:l
m68k_03ed8c_end:
.org 0x3ED96
m68k_03ed96:
        move.w 0x80e2:w,%d7
m68k_03ed96_end:
.org 0x3ED9A
m68k_03ed9a:
        move.w #0x3,%d0
m68k_03ed9a_end:
.org 0x3ED9E
m68k_03ed9e:
        move.w #0x1,%d1
m68k_03ed9e_end:
.org 0x3EDA2
m68k_03eda2:
        bsr.w (. + 5408)
m68k_03eda2_end:
.org 0x3EDA6
m68k_03eda6:
        cmpi.b #0x3,0x80db:w
m68k_03eda6_end:
.org 0x3EDAC
m68k_03edac:
        bne.b (. + 42)
m68k_03edac_end:
.org 0x3EDAE
m68k_03edae:
        lea.l 0x4529b:l,%a0
m68k_03edae_end:
.org 0x3EDB4
m68k_03edb4:
        lea.l 0xc000:l,%a1
m68k_03edb4_end:
.org 0x3EDBA
m68k_03edba:
        move.l #0x80,%d5
m68k_03edba_end:
.org 0x3EDC0
m68k_03edc0:
        move.w #0x8000,0x8000:w
m68k_03edc0_end:
.org 0x3EDC6
m68k_03edc6:
        move.w #0x20,%d6
m68k_03edc6_end:
.org 0x3EDCA
m68k_03edca:
        jsr -17142(%pc)
m68k_03edca_end:
.org 0x3EDCE
m68k_03edce:
        bsr.w (. + 3064)
m68k_03edce_end:
.org 0x3EDD2
m68k_03edd2:
        bra.w (. + 72)
m68k_03edd2_end:
.org 0x3EDD6
m68k_03edd6:
        lea.l 0x45127:l,%a0
m68k_03edd6_end:
.org 0x3EDDC
m68k_03eddc:
        lea.l 0xc000:l,%a1
m68k_03eddc_end:
.org 0x3EDE2
m68k_03ede2:
        move.l #0x80,%d5
m68k_03ede2_end:
.org 0x3EDE8
m68k_03ede8:
        move.w #0x8000,0x8000:w
m68k_03ede8_end:
.org 0x3EDEE
m68k_03edee:
        move.w #0x20,%d6
m68k_03edee_end:
.org 0x3EDF2
m68k_03edf2:
        jsr -17182(%pc)
m68k_03edf2_end:
.org 0x3EDF6
m68k_03edf6:
        lea.l 0x45246:l,%a0
m68k_03edf6_end:
.org 0x3EDFC
m68k_03edfc:
        lea.l 0xc040:l,%a1
m68k_03edfc_end:
.org 0x3EE02
m68k_03ee02:
        move.l #0x80,%d5
m68k_03ee02_end:
.org 0x3EE08
m68k_03ee08:
        move.w #0x8000,0x8000:w
m68k_03ee08_end:
.org 0x3EE0E
m68k_03ee0e:
        move.w #0x20,%d6
m68k_03ee0e_end:
.org 0x3EE12
m68k_03ee12:
        jsr -17214(%pc)
m68k_03ee12_end:
.org 0x3EE16
m68k_03ee16:
        bsr.w (. + 2992)
m68k_03ee16_end:
.org 0x3EE1A
m68k_03ee1a:
        move.w #0x2500,%sr
m68k_03ee1a_end:
.org 0x3EE1E
m68k_03ee1e:
        move.w #0x1,0x813a:w
m68k_03ee1e_end:
.org 0x3EE24
m68k_03ee24:
        move.w #0x0,0x813c:w
m68k_03ee24_end:
.org 0x3EE2A
m68k_03ee2a:
        move.w #0x1,0x813e:w
m68k_03ee2a_end:
.org 0x3EE30
m68k_03ee30:
        move.w 0x8138:w,0x8148:w
m68k_03ee30_end:
.org 0x3EE36
m68k_03ee36:
        clr.w 0x8146:w
m68k_03ee36_end:
.org 0x3EE3A
m68k_03ee3a:
        cmpi.w #0x6,0x8148:w
m68k_03ee3a_end:
.org 0x3EE40
m68k_03ee40:
        bne.w (. + 10)
m68k_03ee40_end:
.org 0x3EE44
m68k_03ee44:
        move.w #0x1,0x8146:w
m68k_03ee44_end:
.org 0x3EE4A
m68k_03ee4a:
        rts
m68k_03ee4a_end:
.org 0x3EE4C
m68k_03ee4c:
        move.b 0x811d:w,%d0
m68k_03ee4c_end:
.org 0x3EE50
m68k_03ee50:
        andi.b #0x40,%d0
m68k_03ee50_end:
.org 0x3EE54
m68k_03ee54:
        beq.w (. + 182)
m68k_03ee54_end:
.org 0x3EE58
m68k_03ee58:
        move.w #0xad,%d0
m68k_03ee58_end:
.org 0x3EE5C
m68k_03ee5c:
        jsr 0x808a:l
m68k_03ee5c_end:
.org 0x3EE62
m68k_03ee62:
        move.w #0x2700,%sr
m68k_03ee62_end:
.org 0x3EE66
m68k_03ee66:
        move.l #0x50000002,0xc00004:l
m68k_03ee66_end:
.org 0x3EE70
m68k_03ee70:
        lea.l 0xc00000:l,%a5
m68k_03ee70_end:
.org 0x3EE76
m68k_03ee76:
        move.w #0x3333,%d6
m68k_03ee76_end:
.org 0x3EE7A
m68k_03ee7a:
        move.w #0x2ff,%d7
m68k_03ee7a_end:
.org 0x3EE7E
m68k_03ee7e:
        move.w %d6,(%a5)
m68k_03ee7e_end:
.org 0x3EE80
m68k_03ee80:
        dbra %d7,(. + -2)
m68k_03ee80_end:
.org 0x3EE84
m68k_03ee84:
        move.l #0x50000002,0xc00004:l
m68k_03ee84_end:
.org 0x3EE8E
m68k_03ee8e:
        move.w 0x80dc:w,%d7
m68k_03ee8e_end:
.org 0x3EE92
m68k_03ee92:
        move.w #0x3,%d0
m68k_03ee92_end:
.org 0x3EE96
m68k_03ee96:
        move.w #0x1,%d1
m68k_03ee96_end:
.org 0x3EE9A
m68k_03ee9a:
        bsr.w (. + 5160)
m68k_03ee9a_end:
.org 0x3EE9E
m68k_03ee9e:
        move.w 0x80de:w,%d7
m68k_03ee9e_end:
.org 0x3EEA2
m68k_03eea2:
        move.w #0x3,%d0
m68k_03eea2_end:
.org 0x3EEA6
m68k_03eea6:
        move.w #0x1,%d1
m68k_03eea6_end:
.org 0x3EEAA
m68k_03eeaa:
        bsr.w (. + 5144)
m68k_03eeaa_end:
.org 0x3EEAE
m68k_03eeae:
        move.w 0x80e0:w,%d7
m68k_03eeae_end:
.org 0x3EEB2
m68k_03eeb2:
        move.w #0x3,%d0
m68k_03eeb2_end:
.org 0x3EEB6
m68k_03eeb6:
        move.w #0x1,%d1
m68k_03eeb6_end:
.org 0x3EEBA
m68k_03eeba:
        bsr.w (. + 5128)
m68k_03eeba_end:
.org 0x3EEBE
m68k_03eebe:
        move.w 0x80e2:w,%d7
m68k_03eebe_end:
.org 0x3EEC2
m68k_03eec2:
        move.w #0x3,%d0
m68k_03eec2_end:
.org 0x3EEC6
m68k_03eec6:
        move.w #0x1,%d1
m68k_03eec6_end:
.org 0x3EECA
m68k_03eeca:
        bsr.w (. + 5112)
m68k_03eeca_end:
.org 0x3EECE
m68k_03eece:
        lea.l 0x44a6c:l,%a0
m68k_03eece_end:
.org 0x3EED4
m68k_03eed4:
        lea.l 0xc000:l,%a1
m68k_03eed4_end:
.org 0x3EEDA
m68k_03eeda:
        move.l #0x80,%d5
m68k_03eeda_end:
.org 0x3EEE0
m68k_03eee0:
        move.w #0x8000,0x8000:w
m68k_03eee0_end:
.org 0x3EEE6
m68k_03eee6:
        move.w #0x20,%d6
m68k_03eee6_end:
.org 0x3EEEA
m68k_03eeea:
        jsr -17430(%pc)
m68k_03eeea_end:
.org 0x3EEEE
m68k_03eeee:
        move.w #0x2,0x813a:w
m68k_03eeee_end:
.org 0x3EEF4
m68k_03eef4:
        move.w #0x0,0x813c:w
m68k_03eef4_end:
.org 0x3EEFA
m68k_03eefa:
        move.w #0x1,0x813e:w
m68k_03eefa_end:
.org 0x3EF00
m68k_03ef00:
        bsr.w (. + 3934)
m68k_03ef00_end:
.org 0x3EF04
m68k_03ef04:
        move.w #0x2500,%sr
m68k_03ef04_end:
.org 0x3EF08
m68k_03ef08:
        rts
m68k_03ef08_end:
.org 0x3EF0A
m68k_03ef0a:
        tst.w 0x814c:w
m68k_03ef0a_end:
.org 0x3EF0E
m68k_03ef0e:
        bne.b (. + 16)
m68k_03ef0e_end:
.org 0x3EF10
m68k_03ef10:
        move.w #0x1,0x814c:w
m68k_03ef10_end:
.org 0x3EF16
m68k_03ef16:
        addq.w #0x1,0x8160:w
m68k_03ef16_end:
.org 0x3EF1A
m68k_03ef1a:
        bsr.w (. + 11410)
m68k_03ef1a_end:
.org 0x3EF1E
m68k_03ef1e:
        cmpi.w #0x6,0x8130:w
m68k_03ef1e_end:
.org 0x3EF24
m68k_03ef24:
        bne.b (. + 38)
m68k_03ef24_end:
.org 0x3EF26
m68k_03ef26:
        cmpi.w #0x0,0x816c:w
m68k_03ef26_end:
.org 0x3EF2C
m68k_03ef2c:
        bhi.w (. + 30)
m68k_03ef2c_end:
.org 0x3EF30
m68k_03ef30:
        move.w #0x5,0x813a:w
m68k_03ef30_end:
.org 0x3EF36
m68k_03ef36:
        move.w #0x0,0x813c:w
m68k_03ef36_end:
.org 0x3EF3C
m68k_03ef3c:
        move.w #0x4,0x8114:w
m68k_03ef3c_end:
.org 0x3EF42
m68k_03ef42:
        move.w #0x0,0x8116:w
m68k_03ef42_end:
.org 0x3EF48
m68k_03ef48:
        rts
m68k_03ef48_end:
.org 0x3EF4A
m68k_03ef4a:
        cmpi.w #0x6,0x8138:w
m68k_03ef4a_end:
.org 0x3EF50
m68k_03ef50:
        bne.b (. + 38)
m68k_03ef50_end:
.org 0x3EF52
m68k_03ef52:
        cmpi.w #0x160,0x826c:w
m68k_03ef52_end:
.org 0x3EF58
m68k_03ef58:
        bcs.w (. + 30)
m68k_03ef58_end:
.org 0x3EF5C
m68k_03ef5c:
        move.w #0x5,0x813a:w
m68k_03ef5c_end:
.org 0x3EF62
m68k_03ef62:
        move.w #0x0,0x813c:w
m68k_03ef62_end:
.org 0x3EF68
m68k_03ef68:
        move.w #0x5,0x8114:w
m68k_03ef68_end:
.org 0x3EF6E
m68k_03ef6e:
        move.w #0x1,0x8116:w
m68k_03ef6e_end:
.org 0x3EF74
m68k_03ef74:
        rts
m68k_03ef74_end:
.org 0x3EF76
m68k_03ef76:
        rts
m68k_03ef76_end:
.org 0x3EF86
m68k_03ef86:
        bra.w (. + 8)
m68k_03ef86_end:
.org 0x3EF8A
m68k_03ef8a:
        bra.w (. + 94)
m68k_03ef8a_end:
.org 0x3EF8E
m68k_03ef8e:
        move.w #0x2700,%sr
m68k_03ef8e_end:
.org 0x3EF92
m68k_03ef92:
        move.w #0x8f02,0xc00004:l
m68k_03ef92_end:
.org 0x3EF9A
m68k_03ef9a:
        move.l #0x60000002,0xc00004:l
m68k_03ef9a_end:
.org 0x3EFA4
m68k_03efa4:
        lea.l 0xc00000:l,%a5
m68k_03efa4_end:
.org 0x3EFAA
m68k_03efaa:
        move.w #0x3333,%d6
m68k_03efaa_end:
.org 0x3EFAE
m68k_03efae:
        move.w #0xd7f,%d7
m68k_03efae_end:
.org 0x3EFB2
m68k_03efb2:
        move.w %d6,(%a5)
m68k_03efb2_end:
.org 0x3EFB4
m68k_03efb4:
        dbra %d7,(. + -2)
m68k_03efb4_end:
.org 0x3EFB8
m68k_03efb8:
        move.w #0xa000,0xff700c:l
m68k_03efb8_end:
.org 0x3EFC0
m68k_03efc0:
        move.l #0x3b36c,0xff700e:l
m68k_03efc0_end:
.org 0x3EFCA
m68k_03efca:
        move.w #0x3,0xff7014:l
m68k_03efca_end:
.org 0x3EFD2
m68k_03efd2:
        move.w #0x1,0xff7016:l
m68k_03efd2_end:
.org 0x3EFDA
m68k_03efda:
        bsr.w (. + -1272)
m68k_03efda_end:
.org 0x3EFDE
m68k_03efde:
        move.w #0x2500,%sr
m68k_03efde_end:
.org 0x3EFE2
m68k_03efe2:
        addq.w #0x1,0x813c:w
m68k_03efe2_end:
.org 0x3EFE6
m68k_03efe6:
        rts
m68k_03efe6_end:
.org 0x3EFE8
m68k_03efe8:
        move.w 0x811e:w,%d0
m68k_03efe8_end:
.org 0x3EFEC
m68k_03efec:
        tst.w 0x8144:w
m68k_03efec_end:
.org 0x3EFF0
m68k_03eff0:
        beq.b (. + 6)
m68k_03eff0_end:
.org 0x3EFF2
m68k_03eff2:
        move.w 0x8120:w,%d0
m68k_03eff2_end:
.org 0x3EFF6
m68k_03eff6:
        move.w %d0,0x8122:w
m68k_03eff6_end:
.org 0x3EFFA
m68k_03effa:
        bsr.w (. + 1894)
m68k_03effa_end:
.org 0x3EFFE
m68k_03effe:
        bsr.w (. + 2504)
m68k_03effe_end:
.org 0x3F002
m68k_03f002:
        move.w 0x8122:w,%d0
m68k_03f002_end:
.org 0x3F006
m68k_03f006:
        andi.b #0xf0,%d0
m68k_03f006_end:
.org 0x3F00A
m68k_03f00a:
        beq.b (. + 22)
m68k_03f00a_end:
.org 0x3F00C
m68k_03f00c:
        bsr.w (. + 4880)
m68k_03f00c_end:
.org 0x3F010
m68k_03f010:
        move.w #0x0,0x813a:w
m68k_03f010_end:
.org 0x3F016
m68k_03f016:
        move.w #0x6,0x813c:w
m68k_03f016_end:
.org 0x3F01C
m68k_03f01c:
        clr.w 0x813e:w
m68k_03f01c_end:
.org 0x3F020
m68k_03f020:
        rts
m68k_03f020_end:
.org 0x3F030
m68k_03f030:
        bra.w (. + 4)
m68k_03f030_end:
.org 0x3F034
m68k_03f034:
        move.b 0x811d:w,%d0
m68k_03f034_end:
.org 0x3F038
m68k_03f038:
        andi.b #0xf0,%d0
m68k_03f038_end:
.org 0x3F03C
m68k_03f03c:
        beq.b (. + 22)
m68k_03f03c_end:
.org 0x3F03E
m68k_03f03e:
        bsr.w (. + 4830)
m68k_03f03e_end:
.org 0x3F042
m68k_03f042:
        move.w #0x0,0x813a:w
m68k_03f042_end:
.org 0x3F048
m68k_03f048:
        move.w #0x6,0x813c:w
m68k_03f048_end:
.org 0x3F04E
m68k_03f04e:
        clr.w 0x813e:w
m68k_03f04e_end:
.org 0x3F052
m68k_03f052:
        rts
m68k_03f052_end:
.org 0x3F062
m68k_03f062:
        bra.w (. + 16)
m68k_03f062_end:
.org 0x3F066
m68k_03f066:
        bra.w (. + 108)
m68k_03f066_end:
.org 0x3F06A
m68k_03f06a:
        bra.w (. + 354)
m68k_03f06a_end:
.org 0x3F06E
m68k_03f06e:
        bra.w (. + 364)
m68k_03f06e_end:
.org 0x3F072
m68k_03f072:
        move.w #0x2700,%sr
m68k_03f072_end:
.org 0x3F076
m68k_03f076:
        move.w #0x8f02,0xc00004:l
m68k_03f076_end:
.org 0x3F07E
m68k_03f07e:
        move.l #0x60000002,0xc00004:l
m68k_03f07e_end:
.org 0x3F088
m68k_03f088:
        lea.l 0xc00000:l,%a5
m68k_03f088_end:
.org 0x3F08E
m68k_03f08e:
        move.w #0x3333,%d6
m68k_03f08e_end:
.org 0x3F092
m68k_03f092:
        move.w #0xd7f,%d7
m68k_03f092_end:
.org 0x3F096
m68k_03f096:
        move.w %d6,(%a5)
m68k_03f096_end:
.org 0x3F098
m68k_03f098:
        dbra %d7,(. + -2)
m68k_03f098_end:
.org 0x3F09C
m68k_03f09c:
        move.w #0xa000,0xff700c:l
m68k_03f09c_end:
.org 0x3F0A4
m68k_03f0a4:
        move.l #0x3b45e,0xff700e:l
m68k_03f0a4_end:
.org 0x3F0AE
m68k_03f0ae:
        move.w #0x3,0xff7014:l
m68k_03f0ae_end:
.org 0x3F0B6
m68k_03f0b6:
        move.w #0x1,0xff7016:l
m68k_03f0b6_end:
.org 0x3F0BE
m68k_03f0be:
        bsr.w (. + -1500)
m68k_03f0be_end:
.org 0x3F0C2
m68k_03f0c2:
        move.w #0x2500,%sr
m68k_03f0c2_end:
.org 0x3F0C6
m68k_03f0c6:
        addq.w #0x1,0x813c:w
m68k_03f0c6_end:
.org 0x3F0CA
m68k_03f0ca:
        move.w #0x1,0x813e:w
m68k_03f0ca_end:
.org 0x3F0D0
m68k_03f0d0:
        rts
m68k_03f0d0_end:
.org 0x3F0D2
m68k_03f0d2:
        move.b 0x811d:w,%d0
m68k_03f0d2_end:
.org 0x3F0D6
m68k_03f0d6:
        andi.b #0xf0,%d0
m68k_03f0d6_end:
.org 0x3F0DA
m68k_03f0da:
        beq.w (. + 232)
m68k_03f0da_end:
.org 0x3F1CC
m68k_03f1cc:
        btst.b #0x7,0x80c4:w
m68k_03f1cc_end:
.org 0x3F1D2
m68k_03f1d2:
        beq.w (. + 8)
m68k_03f1d2_end:
.org 0x3F1D6
m68k_03f1d6:
        addq.w #0x1,0x813c:w
m68k_03f1d6_end:
.org 0x3F1DA
m68k_03f1da:
        rts
m68k_03f1da_end:
.org 0x3F1EA
m68k_03f1ea:
        bra.w (. + 16)
m68k_03f1ea_end:
.org 0x3F1EE
m68k_03f1ee:
        bra.w (. + 108)
m68k_03f1ee_end:
.org 0x3F1F2
m68k_03f1f2:
        bra.w (. + -38)
m68k_03f1f2_end:
.org 0x3F1F6
m68k_03f1f6:
        bra.w (. + -28)
m68k_03f1f6_end:
.org 0x3F1FA
m68k_03f1fa:
        move.w #0x2700,%sr
m68k_03f1fa_end:
.org 0x3F1FE
m68k_03f1fe:
        move.w #0x8f02,0xc00004:l
m68k_03f1fe_end:
.org 0x3F206
m68k_03f206:
        move.l #0x60000002,0xc00004:l
m68k_03f206_end:
.org 0x3F210
m68k_03f210:
        lea.l 0xc00000:l,%a5
m68k_03f210_end:
.org 0x3F216
m68k_03f216:
        move.w #0x3333,%d6
m68k_03f216_end:
.org 0x3F21A
m68k_03f21a:
        move.w #0xd7f,%d7
m68k_03f21a_end:
.org 0x3F21E
m68k_03f21e:
        move.w %d6,(%a5)
m68k_03f21e_end:
.org 0x3F220
m68k_03f220:
        dbra %d7,(. + -2)
m68k_03f220_end:
.org 0x3F224
m68k_03f224:
        move.w #0xa000,0xff700c:l
m68k_03f224_end:
.org 0x3F22C
m68k_03f22c:
        move.l #0x3b488,0xff700e:l
m68k_03f22c_end:
.org 0x3F236
m68k_03f236:
        move.w #0x3,0xff7014:l
m68k_03f236_end:
.org 0x3F23E
m68k_03f23e:
        move.w #0x1,0xff7016:l
m68k_03f23e_end:
.org 0x3F246
m68k_03f246:
        bsr.w (. + -1892)
m68k_03f246_end:
.org 0x3F24A
m68k_03f24a:
        move.w #0x2500,%sr
m68k_03f24a_end:
.org 0x3F24E
m68k_03f24e:
        addq.w #0x1,0x813c:w
m68k_03f24e_end:
.org 0x3F252
m68k_03f252:
        move.w #0x1,0x813e:w
m68k_03f252_end:
.org 0x3F258
m68k_03f258:
        rts
m68k_03f258_end:
.org 0x3F25A
m68k_03f25a:
        move.b 0x811d:w,%d0
m68k_03f25a_end:
.org 0x3F25E
m68k_03f25e:
        andi.b #0xf0,%d0
m68k_03f25e_end:
.org 0x3F262
m68k_03f262:
        beq.w (. + 42)
m68k_03f262_end:
.org 0x3F266
m68k_03f266:
        bsr.w (. + 1654)
m68k_03f266_end:
.org 0x3F26A
m68k_03f26a:
        addq.w #0x1,0x813c:w
m68k_03f26a_end:
.org 0x3F26E
m68k_03f26e:
        move.w #0xffff,0x80ca:w
m68k_03f26e_end:
.org 0x3F274
m68k_03f274:
        move.w #0xffff,0x80cc:w
m68k_03f274_end:
.org 0x3F27A
m68k_03f27a:
        move.w #0xffff,0x80ce:w
m68k_03f27a_end:
.org 0x3F280
m68k_03f280:
        move.w #0xffff,0x80d0:w
m68k_03f280_end:
.org 0x3F286
m68k_03f286:
        moveq #1,%d0
m68k_03f286_end:
.org 0x3F288
m68k_03f288:
        jsr -18514(%pc)
m68k_03f288_end:
.org 0x3F28C
m68k_03f28c:
        rts
m68k_03f28c_end:
.org 0x3F29C
m68k_03f29c:
        bra.w (. + 16)
m68k_03f29c_end:
.org 0x3F2A0
m68k_03f2a0:
        bra.w (. + 108)
m68k_03f2a0_end:
.org 0x3F2A4
m68k_03f2a4:
        bra.w (. + -216)
m68k_03f2a4_end:
.org 0x3F2A8
m68k_03f2a8:
        bra.w (. + 150)
m68k_03f2a8_end:
.org 0x3F2AC
m68k_03f2ac:
        move.w #0x2700,%sr
m68k_03f2ac_end:
.org 0x3F2B0
m68k_03f2b0:
        move.w #0x8f02,0xc00004:l
m68k_03f2b0_end:
.org 0x3F2B8
m68k_03f2b8:
        move.l #0x60000002,0xc00004:l
m68k_03f2b8_end:
.org 0x3F2C2
m68k_03f2c2:
        lea.l 0xc00000:l,%a5
m68k_03f2c2_end:
.org 0x3F2C8
m68k_03f2c8:
        move.w #0x3333,%d6
m68k_03f2c8_end:
.org 0x3F2CC
m68k_03f2cc:
        move.w #0xd7f,%d7
m68k_03f2cc_end:
.org 0x3F2D0
m68k_03f2d0:
        move.w %d6,(%a5)
m68k_03f2d0_end:
.org 0x3F2D2
m68k_03f2d2:
        dbra %d7,(. + -2)
m68k_03f2d2_end:
.org 0x3F2D6
m68k_03f2d6:
        move.w #0xa000,0xff700c:l
m68k_03f2d6_end:
.org 0x3F2DE
m68k_03f2de:
        move.l #0x3b47a,0xff700e:l
m68k_03f2de_end:
.org 0x3F2E8
m68k_03f2e8:
        move.w #0x3,0xff7014:l
m68k_03f2e8_end:
.org 0x3F2F0
m68k_03f2f0:
        move.w #0x1,0xff7016:l
m68k_03f2f0_end:
.org 0x3F2F8
m68k_03f2f8:
        bsr.w (. + -2070)
m68k_03f2f8_end:
.org 0x3F2FC
m68k_03f2fc:
        move.w #0x2500,%sr
m68k_03f2fc_end:
.org 0x3F300
m68k_03f300:
        addq.w #0x1,0x813c:w
m68k_03f300_end:
.org 0x3F304
m68k_03f304:
        move.w #0x1,0x813e:w
m68k_03f304_end:
.org 0x3F30A
m68k_03f30a:
        rts
m68k_03f30a_end:
.org 0x3F30C
m68k_03f30c:
        move.b 0x811d:w,%d0
m68k_03f30c_end:
.org 0x3F310
m68k_03f310:
        andi.b #0xf0,%d0
m68k_03f310_end:
.org 0x3F314
m68k_03f314:
        beq.w (. + 42)
m68k_03f314_end:
.org 0x3F318
m68k_03f318:
        addq.w #0x1,0x813c:w
m68k_03f318_end:
.org 0x3F31C
m68k_03f31c:
        bsr.w (. + 1472)
m68k_03f31c_end:
.org 0x3F320
m68k_03f320:
        move.w #0xffff,0x80ca:w
m68k_03f320_end:
.org 0x3F326
m68k_03f326:
        move.w #0xffff,0x80cc:w
m68k_03f326_end:
.org 0x3F32C
m68k_03f32c:
        move.w #0xffff,0x80ce:w
m68k_03f32c_end:
.org 0x3F332
m68k_03f332:
        move.w #0xffff,0x80d0:w
m68k_03f332_end:
.org 0x3F338
m68k_03f338:
        moveq #1,%d0
m68k_03f338_end:
.org 0x3F33A
m68k_03f33a:
        jsr -18692(%pc)
m68k_03f33a_end:
.org 0x3F33E
m68k_03f33e:
        rts
m68k_03f33e_end:
.org 0x3F34E
m68k_03f34e:
        bra.w (. + 20)
m68k_03f34e_end:
.org 0x3F352
m68k_03f352:
        bra.w (. + 118)
m68k_03f352_end:
.org 0x3F356
m68k_03f356:
        bra.w (. + 212)
m68k_03f356_end:
.org 0x3F35A
m68k_03f35a:
        bra.w (. + -398)
m68k_03f35a_end:
.org 0x3F35E
m68k_03f35e:
        bra.w (. + 254)
m68k_03f35e_end:
.org 0x3F362
m68k_03f362:
        move.w #0x2700,%sr
m68k_03f362_end:
.org 0x3F366
m68k_03f366:
        move.w #0x0,0x8116:w
m68k_03f366_end:
.org 0x3F36C
m68k_03f36c:
        move.w #0x8f02,0xc00004:l
m68k_03f36c_end:
.org 0x3F374
m68k_03f374:
        move.l #0x60000002,0xc00004:l
m68k_03f374_end:
.org 0x3F37E
m68k_03f37e:
        lea.l 0xc00000:l,%a5
m68k_03f37e_end:
.org 0x3F384
m68k_03f384:
        move.w #0x3333,%d6
m68k_03f384_end:
.org 0x3F388
m68k_03f388:
        move.w #0xd7f,%d7
m68k_03f388_end:
.org 0x3F38C
m68k_03f38c:
        move.w %d6,(%a5)
m68k_03f38c_end:
.org 0x3F38E
m68k_03f38e:
        dbra %d7,(. + -2)
m68k_03f38e_end:
.org 0x3F392
m68k_03f392:
        move.w #0xa000,0xff700c:l
m68k_03f392_end:
.org 0x3F39A
m68k_03f39a:
        move.l #0x3b49e,0xff700e:l
m68k_03f39a_end:
.org 0x3F3A4
m68k_03f3a4:
        move.w #0x3,0xff7014:l
m68k_03f3a4_end:
.org 0x3F3AC
m68k_03f3ac:
        move.w #0x1,0xff7016:l
m68k_03f3ac_end:
.org 0x3F3B4
m68k_03f3b4:
        bsr.w (. + -2258)
m68k_03f3b4_end:
.org 0x3F3B8
m68k_03f3b8:
        move.w #0x2500,%sr
m68k_03f3b8_end:
.org 0x3F3BC
m68k_03f3bc:
        addq.w #0x1,0x813c:w
m68k_03f3bc_end:
.org 0x3F3C0
m68k_03f3c0:
        move.w #0x1,0x813e:w
m68k_03f3c0_end:
.org 0x3F3C6
m68k_03f3c6:
        rts
m68k_03f3c6_end:
.org 0x3F3C8
m68k_03f3c8:
        move.b 0x811d:w,%d0
m68k_03f3c8_end:
.org 0x3F3CC
m68k_03f3cc:
        andi.b #0x20,%d0
m68k_03f3cc_end:
.org 0x3F3D0
m68k_03f3d0:
        beq.w (. + 88)
m68k_03f3d0_end:
.org 0x3F3D4
m68k_03f3d4:
        move.w #0x2700,%sr
m68k_03f3d4_end:
.org 0x3F3D8
m68k_03f3d8:
        move.w #0x8f02,0xc00004:l
m68k_03f3d8_end:
.org 0x3F3E0
m68k_03f3e0:
        move.l #0x60000002,0xc00004:l
m68k_03f3e0_end:
.org 0x3F3EA
m68k_03f3ea:
        lea.l 0xc00000:l,%a5
m68k_03f3ea_end:
.org 0x3F3F0
m68k_03f3f0:
        move.w #0x3333,%d6
m68k_03f3f0_end:
.org 0x3F3F4
m68k_03f3f4:
        move.w #0xd7f,%d7
m68k_03f3f4_end:
.org 0x3F3F8
m68k_03f3f8:
        move.w %d6,(%a5)
m68k_03f3f8_end:
.org 0x3F3FA
m68k_03f3fa:
        dbra %d7,(. + -2)
m68k_03f3fa_end:
.org 0x3F3FE
m68k_03f3fe:
        move.w #0xa000,0xff700c:l
m68k_03f3fe_end:
.org 0x3F406
m68k_03f406:
        move.l #0x3b4b6,0xff700e:l
m68k_03f406_end:
.org 0x3F410
m68k_03f410:
        move.w #0x3,0xff7014:l
m68k_03f410_end:
.org 0x3F418
m68k_03f418:
        move.w #0x1,0xff7016:l
m68k_03f418_end:
.org 0x3F420
m68k_03f420:
        addq.w #0x1,0x813c:w
m68k_03f420_end:
.org 0x3F424
m68k_03f424:
        move.w #0x2500,%sr
m68k_03f424_end:
.org 0x3F428
m68k_03f428:
        rts
m68k_03f428_end:
.org 0x3F42A
m68k_03f42a:
        move.b 0x811d:w,%d0
m68k_03f42a_end:
.org 0x3F42E
m68k_03f42e:
        andi.b #0x20,%d0
m68k_03f42e_end:
.org 0x3F432
m68k_03f432:
        beq.w (. + 42)
m68k_03f432_end:
.org 0x3F436
m68k_03f436:
        addq.w #0x1,0x813c:w
m68k_03f436_end:
.org 0x3F43A
m68k_03f43a:
        bsr.w (. + 1186)
m68k_03f43a_end:
.org 0x3F43E
m68k_03f43e:
        move.w #0xffff,0x80ca:w
m68k_03f43e_end:
.org 0x3F444
m68k_03f444:
        move.w #0xffff,0x80cc:w
m68k_03f444_end:
.org 0x3F44A
m68k_03f44a:
        move.w #0xffff,0x80ce:w
m68k_03f44a_end:
.org 0x3F450
m68k_03f450:
        move.w #0xffff,0x80d0:w
m68k_03f450_end:
.org 0x3F456
m68k_03f456:
        moveq #1,%d0
m68k_03f456_end:
.org 0x3F458
m68k_03f458:
        jsr -18978(%pc)
m68k_03f458_end:
.org 0x3F45C
m68k_03f45c:
        rts
m68k_03f45c_end:
.org 0x3F45E
m68k_03f45e:
        moveq #0,%d0
m68k_03f45e_end:
.org 0x3F460
m68k_03f460:
        moveq #0,%d1
m68k_03f460_end:
.org 0x3F462
m68k_03f462:
        move.w 0x80e6:w,%d0
m68k_03f462_end:
.org 0x3F466
m68k_03f466:
        move.w 0x80ea:w,%d1
m68k_03f466_end:
.org 0x3F46A
m68k_03f46a:
        bne.w (. + 10)
m68k_03f46a_end:
.org 0x3F46E
m68k_03f46e:
        addq.w #0x1,0x80ea:w
m68k_03f46e_end:
.org 0x3F472
m68k_03f472:
        bra.b (. + -20)
m68k_03f472_end:
.org 0x3F474
m68k_03f474:
        cmpi.w #0xf,%d1
m68k_03f474_end:
.org 0x3F478
m68k_03f478:
        bls.w (. + 10)
m68k_03f478_end:
.org 0x3F47C
m68k_03f47c:
        subq.w #0x1,0x80ea:w
m68k_03f47c_end:
.org 0x3F480
m68k_03f480:
        bra.b (. + -34)
m68k_03f480_end:
.org 0x3F482
m68k_03f482:
        divu.w %d1,%d0
m68k_03f482_end:
.org 0x3F484
m68k_03f484:
        cmpi.w #0x3e8,%d0
m68k_03f484_end:
.org 0x3F488
m68k_03f488:
        bls.w (. + 10)
m68k_03f488_end:
.org 0x3F48C
m68k_03f48c:
        addq.w #0x1,0x80ea:w
m68k_03f48c_end:
.org 0x3F490
m68k_03f490:
        bra.b (. + -50)
m68k_03f490_end:
.org 0x3F492
m68k_03f492:
        cmpi.w #0x64,%d0
m68k_03f492_end:
.org 0x3F496
m68k_03f496:
        bhi.w (. + 18)
m68k_03f496_end:
.org 0x3F49A
m68k_03f49a:
        cmpi.w #0x1,0x80ea:w
m68k_03f49a_end:
.org 0x3F4A0
m68k_03f4a0:
        beq.b (. + 20)
m68k_03f4a0_end:
.org 0x3F4A2
m68k_03f4a2:
        subq.w #0x1,0x80ea:w
m68k_03f4a2_end:
.org 0x3F4A6
m68k_03f4a6:
        bra.b (. + -72)
m68k_03f4a6_end:
.org 0x3F4A8
m68k_03f4a8:
        move.w %d0,0x80ee:w
m68k_03f4a8_end:
.org 0x3F4AC
m68k_03f4ac:
        swap %d0
m68k_03f4ac_end:
.org 0x3F4AE
m68k_03f4ae:
        move.w %d0,0x80f2:w
m68k_03f4ae_end:
.org 0x3F4B2
m68k_03f4b2:
        rts
m68k_03f4b2_end:
.org 0x3F4B4
m68k_03f4b4:
        tst.w %d0
m68k_03f4b4_end:
.org 0x3F4B6
m68k_03f4b6:
        bne.b (. + -14)
m68k_03f4b6_end:
.org 0x3F4B8
m68k_03f4b8:
        clr.w 0x80ee:w
m68k_03f4b8_end:
.org 0x3F4BC
m68k_03f4bc:
        clr.w 0x80f2:w
m68k_03f4bc_end:
.org 0x3F4C0
m68k_03f4c0:
        rts
m68k_03f4c0_end:
.org 0x3F518
m68k_03f518:
        btst.b #0x0,0x811f:w
m68k_03f518_end:
.org 0x3F51E
m68k_03f51e:
        beq.b (. + 6)
m68k_03f51e_end:
.org 0x3F520
m68k_03f520:
        addq.w #0x1,0x80ea:w
m68k_03f520_end:
.org 0x3F524
m68k_03f524:
        btst.b #0x1,0x811f:w
m68k_03f524_end:
.org 0x3F52A
m68k_03f52a:
        beq.b (. + 6)
m68k_03f52a_end:
.org 0x3F52C
m68k_03f52c:
        subq.w #0x1,0x80ea:w
m68k_03f52c_end:
.org 0x3F530
m68k_03f530:
        rts
m68k_03f530_end:
.org 0x3F532
m68k_03f532:
        btst.b #0x0,0x811f:w
m68k_03f532_end:
.org 0x3F538
m68k_03f538:
        beq.b (. + 122)
m68k_03f538_end:
.org 0x3F53A
m68k_03f53a:
        move.w 0x80fa:w,%d0
m68k_03f53a_end:
.org 0x3F53E
m68k_03f53e:
        add.w 0x80fc:w,%d0
m68k_03f53e_end:
.org 0x3F542
m68k_03f542:
        add.w 0x80fe:w,%d0
m68k_03f542_end:
.org 0x3F546
m68k_03f546:
        cmp.w 0x80ea:w,%d0
m68k_03f546_end:
.org 0x3F54A
m68k_03f54a:
        bcc.b (. + 104)
m68k_03f54a_end:
.org 0x3F54C
m68k_03f54c:
        move.w 0x8144:w,%d0
m68k_03f54c_end:
.org 0x3F550
m68k_03f550:
        asl.w #0x2,%d0
m68k_03f550_end:
.org 0x3F552
m68k_03f552:
        lea.l 164(%pc),%a0
m68k_03f552_end:
.org 0x3F556
m68k_03f556:
        nop
m68k_03f556_end:
.org 0x3F558
m68k_03f558:
        movea.l (%a0, %d0.w),%a1
m68k_03f558_end:
.org 0x3F55C
m68k_03f55c:
        moveq #0,%d0
m68k_03f55c_end:
.org 0x3F55E
m68k_03f55e:
        cmpi.w #0x64,0x8112:w
m68k_03f55e_end:
.org 0x3F564
m68k_03f564:
        bls.b (. + 54)
m68k_03f564_end:
.org 0x3F566
m68k_03f566:
        moveq #1,%d0
m68k_03f566_end:
.org 0x3F568
m68k_03f568:
        cmpi.w #0xc8,0x8112:w
m68k_03f568_end:
.org 0x3F56E
m68k_03f56e:
        bls.b (. + 44)
m68k_03f56e_end:
.org 0x3F570
m68k_03f570:
        moveq #2,%d0
m68k_03f570_end:
.org 0x3F572
m68k_03f572:
        cmpi.w #0x12c,0x8112:w
m68k_03f572_end:
.org 0x3F578
m68k_03f578:
        bls.b (. + 34)
m68k_03f578_end:
.org 0x3F57A
m68k_03f57a:
        moveq #3,%d0
m68k_03f57a_end:
.org 0x3F57C
m68k_03f57c:
        cmpi.w #0x190,0x8112:w
m68k_03f57c_end:
.org 0x3F582
m68k_03f582:
        bls.b (. + 24)
m68k_03f582_end:
.org 0x3F584
m68k_03f584:
        moveq #4,%d0
m68k_03f584_end:
.org 0x3F586
m68k_03f586:
        cmpi.w #0x1f4,0x8112:w
m68k_03f586_end:
.org 0x3F58C
m68k_03f58c:
        bls.b (. + 14)
m68k_03f58c_end:
.org 0x3F58E
m68k_03f58e:
        moveq #5,%d0
m68k_03f58e_end:
.org 0x3F590
m68k_03f590:
        cmpi.w #0x258,0x8112:w
m68k_03f590_end:
.org 0x3F596
m68k_03f596:
        bls.b (. + 4)
m68k_03f596_end:
.org 0x3F598
m68k_03f598:
        moveq #6,%d0
m68k_03f598_end:
.org 0x3F59A
m68k_03f59a:
        move.w 0x8144:w,%d1
m68k_03f59a_end:
.org 0x3F59E
m68k_03f59e:
        asl.w #0x3,%d1
m68k_03f59e_end:
.org 0x3F5A0
m68k_03f5a0:
        add.w %d0,%d1
m68k_03f5a0_end:
.org 0x3F5A2
m68k_03f5a2:
        move.w (%a1),%d0
m68k_03f5a2_end:
.org 0x3F5A4
m68k_03f5a4:
        lea.l 94(%pc),%a0
m68k_03f5a4_end:
.org 0x3F5A8
m68k_03f5a8:
        nop
m68k_03f5a8_end:
.org 0x3F5AA
m68k_03f5aa:
        cmp.b (%a0, %d1.w),%d0
m68k_03f5aa_end:
.org 0x3F5AE
m68k_03f5ae:
        bcc.b (. + 4)
m68k_03f5ae_end:
.org 0x3F5B0
m68k_03f5b0:
        addq.w #0x1,(%a1)
m68k_03f5b0_end:
.org 0x3F5B2
m68k_03f5b2:
        btst.b #0x1,0x811f:w
m68k_03f5b2_end:
.org 0x3F5B8
m68k_03f5b8:
        beq.b (. + 24)
m68k_03f5b8_end:
.org 0x3F5BA
m68k_03f5ba:
        move.w 0x8144:w,%d0
m68k_03f5ba_end:
.org 0x3F5BE
m68k_03f5be:
        asl.w #0x2,%d0
m68k_03f5be_end:
.org 0x3F5C0
m68k_03f5c0:
        lea.l 54(%pc),%a0
m68k_03f5c0_end:
.org 0x3F5C4
m68k_03f5c4:
        nop
m68k_03f5c4_end:
.org 0x3F5C6
m68k_03f5c6:
        movea.l (%a0, %d0.w),%a0
m68k_03f5c6_end:
.org 0x3F5CA
m68k_03f5ca:
        tst.w (%a0)
m68k_03f5ca_end:
.org 0x3F5CC
m68k_03f5cc:
        beq.b (. + 4)
m68k_03f5cc_end:
.org 0x3F5CE
m68k_03f5ce:
        subq.w #0x1,(%a0)
m68k_03f5ce_end:
.org 0x3F5D0
m68k_03f5d0:
        btst.b #0x5,0x811f:w
m68k_03f5d0_end:
.org 0x3F5D6
m68k_03f5d6:
        beq.b (. + 14)
m68k_03f5d6_end:
.org 0x3F5D8
m68k_03f5d8:
        cmpi.w #0x2,0x8144:w
m68k_03f5d8_end:
.org 0x3F5DE
m68k_03f5de:
        bcc.b (. + 6)
m68k_03f5de_end:
.org 0x3F5E0
m68k_03f5e0:
        addq.w #0x1,0x8144:w
m68k_03f5e0_end:
.org 0x3F5E4
m68k_03f5e4:
        btst.b #0x4,0x811f:w
m68k_03f5e4_end:
.org 0x3F5EA
m68k_03f5ea:
        beq.b (. + 12)
m68k_03f5ea_end:
.org 0x3F5EC
m68k_03f5ec:
        tst.w 0x8144:w
m68k_03f5ec_end:
.org 0x3F5F0
m68k_03f5f0:
        beq.b (. + 6)
m68k_03f5f0_end:
.org 0x3F5F2
m68k_03f5f2:
        subq.w #0x1,0x8144:w
m68k_03f5f2_end:
.org 0x3F5F6
m68k_03f5f6:
        rts
m68k_03f5f6_end:
.org 0x3F61C
m68k_03f61c:
        btst.b #0x2,0x811f:w
m68k_03f61c_end:
.org 0x3F622
m68k_03f622:
        beq.b (. + 18)
m68k_03f622_end:
.org 0x3F624
m68k_03f624:
        addq.w #0x1,0x8144:w
m68k_03f624_end:
.org 0x3F628
m68k_03f628:
        cmpi.w #0x5,0x8144:w
m68k_03f628_end:
.org 0x3F62E
m68k_03f62e:
        bcs.b (. + 6)
m68k_03f62e_end:
.org 0x3F630
m68k_03f630:
        clr.w 0x8144:w
m68k_03f630_end:
.org 0x3F634
m68k_03f634:
        btst.b #0x3,0x811f:w
m68k_03f634_end:
.org 0x3F63A
m68k_03f63a:
        beq.b (. + 14)
m68k_03f63a_end:
.org 0x3F63C
m68k_03f63c:
        subq.w #0x1,0x8144:w
m68k_03f63c_end:
.org 0x3F640
m68k_03f640:
        bpl.b (. + 8)
m68k_03f640_end:
.org 0x3F642
m68k_03f642:
        move.w #0x4,0x8144:w
m68k_03f642_end:
.org 0x3F648
m68k_03f648:
        move.w 0x8144:w,%d0
m68k_03f648_end:
.org 0x3F64C
m68k_03f64c:
        asl.w #0x2,%d0
m68k_03f64c_end:
.org 0x3F64E
m68k_03f64e:
        lea.l 9224(%pc),%a0
m68k_03f64e_end:
.org 0x3F652
m68k_03f652:
        nop
m68k_03f652_end:
.org 0x3F654
m68k_03f654:
        movea.l (%a0, %d0.w),%a5
m68k_03f654_end:
.org 0x3F658
m68k_03f658:
        move.w 0x80fa:w,%d1
m68k_03f658_end:
.org 0x3F65C
m68k_03f65c:
        move.w 0x80fc:w,%d2
m68k_03f65c_end:
.org 0x3F660
m68k_03f660:
        move.w 0x80fe:w,%d3
m68k_03f660_end:
.org 0x3F664
m68k_03f664:
        moveq #0,%d4
m68k_03f664_end:
.org 0x3F666
m68k_03f666:
        lea.l 0x826a:w,%a6
m68k_03f666_end:
.org 0x3F66A
m68k_03f66a:
        move.w #0x160,%d0
m68k_03f66a_end:
.org 0x3F66E
m68k_03f66e:
        sub.w (%a5)+,%d0
m68k_03f66e_end:
.org 0x3F670
m68k_03f670:
        move.w %d0,0x2(%a6)
m68k_03f670_end:
.org 0x3F674
m68k_03f674:
        move.w (%a5)+,0x4(%a6)
m68k_03f674_end:
.org 0x3F678
m68k_03f678:
        move.w #0x1,0x6(%a6)
m68k_03f678_end:
.org 0x3F67E
m68k_03f67e:
        move.w #0x1,0x8(%a6)
m68k_03f67e_end:
.org 0x3F684
m68k_03f684:
        tst.w %d4
m68k_03f684_end:
.org 0x3F686
m68k_03f686:
        bne.b (. + 10)
m68k_03f686_end:
.org 0x3F688
m68k_03f688:
        move.w #0x8003,(%a6)
m68k_03f688_end:
.org 0x3F68C
m68k_03f68c:
        moveq #1,%d4
m68k_03f68c_end:
.org 0x3F68E
m68k_03f68e:
        bra.b (. + 36)
m68k_03f68e_end:
.org 0x3F690
m68k_03f690:
        tst.w %d1
m68k_03f690_end:
.org 0x3F692
m68k_03f692:
        beq.b (. + 10)
m68k_03f692_end:
.org 0x3F694
m68k_03f694:
        move.w #0x8002,(%a6)
m68k_03f694_end:
.org 0x3F698
m68k_03f698:
        subq.w #0x1,%d1
m68k_03f698_end:
.org 0x3F69A
m68k_03f69a:
        bra.b (. + 24)
m68k_03f69a_end:
.org 0x3F69C
m68k_03f69c:
        tst.w %d2
m68k_03f69c_end:
.org 0x3F69E
m68k_03f69e:
        beq.b (. + 10)
m68k_03f69e_end:
.org 0x3F6A0
m68k_03f6a0:
        move.w #0x8001,(%a6)
m68k_03f6a0_end:
.org 0x3F6A4
m68k_03f6a4:
        subq.w #0x1,%d2
m68k_03f6a4_end:
.org 0x3F6A6
m68k_03f6a6:
        bra.b (. + 12)
m68k_03f6a6_end:
.org 0x3F6A8
m68k_03f6a8:
        tst.w %d3
m68k_03f6a8_end:
.org 0x3F6AA
m68k_03f6aa:
        beq.b (. + 22)
m68k_03f6aa_end:
.org 0x3F6AC
m68k_03f6ac:
        move.w #0x8000,(%a6)
m68k_03f6ac_end:
.org 0x3F6B0
m68k_03f6b0:
        subq.w #0x1,%d3
m68k_03f6b0_end:
.org 0x3F6B2
m68k_03f6b2:
        adda.w #0x10,%a6
m68k_03f6b2_end:
.org 0x3F6B6
m68k_03f6b6:
        cmpa.l #0xffff836a,%a6
m68k_03f6b6_end:
.org 0x3F6BC
m68k_03f6bc:
        bcs.w (. + -82)
m68k_03f6bc_end:
.org 0x3F6C0
m68k_03f6c0:
        rts
m68k_03f6c0_end:
.org 0x3F6C2
m68k_03f6c2:
        btst.b #0x2,0x811f:w
m68k_03f6c2_end:
.org 0x3F6C8
m68k_03f6c8:
        beq.b (. + 18)
m68k_03f6c8_end:
.org 0x3F6CA
m68k_03f6ca:
        addq.w #0x1,0x8144:w
m68k_03f6ca_end:
.org 0x3F6CE
m68k_03f6ce:
        cmpi.w #0x5,0x8144:w
m68k_03f6ce_end:
.org 0x3F6D4
m68k_03f6d4:
        bcs.b (. + 6)
m68k_03f6d4_end:
.org 0x3F6D6
m68k_03f6d6:
        clr.w 0x8144:w
m68k_03f6d6_end:
.org 0x3F6DA
m68k_03f6da:
        btst.b #0x3,0x811f:w
m68k_03f6da_end:
.org 0x3F6E0
m68k_03f6e0:
        beq.b (. + 14)
m68k_03f6e0_end:
.org 0x3F6E2
m68k_03f6e2:
        subq.w #0x1,0x8144:w
m68k_03f6e2_end:
.org 0x3F6E6
m68k_03f6e6:
        bpl.b (. + 8)
m68k_03f6e6_end:
.org 0x3F6E8
m68k_03f6e8:
        move.w #0x4,0x8144:w
m68k_03f6e8_end:
.org 0x3F6EE
m68k_03f6ee:
        move.w 0x8144:w,%d0
m68k_03f6ee_end:
.org 0x3F6F2
m68k_03f6f2:
        asl.w #0x2,%d0
m68k_03f6f2_end:
.org 0x3F6F4
m68k_03f6f4:
        lea.l 9058(%pc),%a0
m68k_03f6f4_end:
.org 0x3F6F8
m68k_03f6f8:
        nop
m68k_03f6f8_end:
.org 0x3F6FA
m68k_03f6fa:
        movea.l (%a0, %d0.w),%a5
m68k_03f6fa_end:
.org 0x3F6FE
m68k_03f6fe:
        move.w 0x80fa:w,%d1
m68k_03f6fe_end:
.org 0x3F702
m68k_03f702:
        move.w 0x80fc:w,%d2
m68k_03f702_end:
.org 0x3F706
m68k_03f706:
        move.w 0x80fe:w,%d3
m68k_03f706_end:
.org 0x3F70A
m68k_03f70a:
        moveq #0,%d4
m68k_03f70a_end:
.org 0x3F70C
m68k_03f70c:
        lea.l 0x816a:w,%a6
m68k_03f70c_end:
.org 0x3F710
m68k_03f710:
        move.w (%a5)+,0x2(%a6)
m68k_03f710_end:
.org 0x3F714
m68k_03f714:
        move.w (%a5)+,0x4(%a6)
m68k_03f714_end:
.org 0x3F718
m68k_03f718:
        move.w #0x1,0x6(%a6)
m68k_03f718_end:
.org 0x3F71E
m68k_03f71e:
        move.w #0x1,0x8(%a6)
m68k_03f71e_end:
.org 0x3F724
m68k_03f724:
        tst.w %d4
m68k_03f724_end:
.org 0x3F726
m68k_03f726:
        bne.b (. + 10)
m68k_03f726_end:
.org 0x3F728
m68k_03f728:
        move.w #0x8003,(%a6)
m68k_03f728_end:
.org 0x3F72C
m68k_03f72c:
        moveq #1,%d4
m68k_03f72c_end:
.org 0x3F72E
m68k_03f72e:
        bra.b (. + 36)
m68k_03f72e_end:
.org 0x3F730
m68k_03f730:
        tst.w %d1
m68k_03f730_end:
.org 0x3F732
m68k_03f732:
        beq.b (. + 10)
m68k_03f732_end:
.org 0x3F734
m68k_03f734:
        move.w #0x8002,(%a6)
m68k_03f734_end:
.org 0x3F738
m68k_03f738:
        subq.w #0x1,%d1
m68k_03f738_end:
.org 0x3F73A
m68k_03f73a:
        bra.b (. + 24)
m68k_03f73a_end:
.org 0x3F73C
m68k_03f73c:
        tst.w %d2
m68k_03f73c_end:
.org 0x3F73E
m68k_03f73e:
        beq.b (. + 10)
m68k_03f73e_end:
.org 0x3F740
m68k_03f740:
        move.w #0x8001,(%a6)
m68k_03f740_end:
.org 0x3F744
m68k_03f744:
        subq.w #0x1,%d2
m68k_03f744_end:
.org 0x3F746
m68k_03f746:
        bra.b (. + 12)
m68k_03f746_end:
.org 0x3F748
m68k_03f748:
        tst.w %d3
m68k_03f748_end:
.org 0x3F74A
m68k_03f74a:
        beq.b (. + 20)
m68k_03f74a_end:
.org 0x3F74C
m68k_03f74c:
        move.w #0x8000,(%a6)
m68k_03f74c_end:
.org 0x3F750
m68k_03f750:
        subq.w #0x1,%d3
m68k_03f750_end:
.org 0x3F752
m68k_03f752:
        adda.w #0x10,%a6
m68k_03f752_end:
.org 0x3F756
m68k_03f756:
        cmpa.l #0xffff826a,%a6
m68k_03f756_end:
.org 0x3F75C
m68k_03f75c:
        bcs.b (. + -76)
m68k_03f75c_end:
.org 0x3F75E
m68k_03f75e:
        rts
m68k_03f75e_end:
.org 0x3F760
m68k_03f760:
        cmpi.b #0x3,0x80db:w
m68k_03f760_end:
.org 0x3F766
m68k_03f766:
        beq.w (. + 222)
m68k_03f766_end:
.org 0x3F76A
m68k_03f76a:
        btst.b #0x0,0x8122:w
m68k_03f76a_end:
.org 0x3F770
m68k_03f770:
        bne.w (. + 98)
m68k_03f770_end:
.org 0x3F774
m68k_03f774:
        btst.b #0x1,0x8122:w
m68k_03f774_end:
.org 0x3F77A
m68k_03f77a:
        bne.w (. + 88)
m68k_03f77a_end:
.org 0x3F77E
m68k_03f77e:
        btst.b #0x3,0x8123:w
m68k_03f77e_end:
.org 0x3F784
m68k_03f784:
        beq.b (. + 34)
m68k_03f784_end:
.org 0x3F786
m68k_03f786:
        addq.w #0x1,0x8146:w
m68k_03f786_end:
.org 0x3F78A
m68k_03f78a:
        cmpi.w #0x4,0x8146:w
m68k_03f78a_end:
.org 0x3F790
m68k_03f790:
        bcs.b (. + 22)
m68k_03f790_end:
.org 0x3F792
m68k_03f792:
        clr.w 0x8146:w
m68k_03f792_end:
.org 0x3F796
m68k_03f796:
        cmpi.w #0x6,0x8148:w
m68k_03f796_end:
.org 0x3F79C
m68k_03f79c:
        bne.w (. + 10)
m68k_03f79c_end:
.org 0x3F7A0
m68k_03f7a0:
        move.w #0x1,0x8146:w
m68k_03f7a0_end:
.org 0x3F7A6
m68k_03f7a6:
        btst.b #0x2,0x8123:w
m68k_03f7a6_end:
.org 0x3F7AC
m68k_03f7ac:
        beq.b (. + 38)
m68k_03f7ac_end:
.org 0x3F7AE
m68k_03f7ae:
        cmpi.w #0x6,0x8148:w
m68k_03f7ae_end:
.org 0x3F7B4
m68k_03f7b4:
        bne.w (. + 18)
m68k_03f7b4_end:
.org 0x3F7B8
m68k_03f7b8:
        subq.w #0x1,0x8146:w
m68k_03f7b8_end:
.org 0x3F7BC
m68k_03f7bc:
        bne.b (. + 22)
m68k_03f7bc_end:
.org 0x3F7BE
m68k_03f7be:
        move.w #0x3,0x8146:w
m68k_03f7be_end:
.org 0x3F7C4
m68k_03f7c4:
        bra.b (. + 14)
m68k_03f7c4_end:
.org 0x3F7C6
m68k_03f7c6:
        subq.w #0x1,0x8146:w
m68k_03f7c6_end:
.org 0x3F7CA
m68k_03f7ca:
        bpl.b (. + 8)
m68k_03f7ca_end:
.org 0x3F7CC
m68k_03f7cc:
        move.w #0x3,0x8146:w
m68k_03f7cc_end:
.org 0x3F7D2
m68k_03f7d2:
        move.w 0x8146:w,%d0
m68k_03f7d2_end:
.org 0x3F7D6
m68k_03f7d6:
        lea.l 104(%pc),%a0
m68k_03f7d6_end:
.org 0x3F7DA
m68k_03f7da:
        nop
m68k_03f7da_end:
.org 0x3F7DC
m68k_03f7dc:
        move.b (%a0, %d0.w),%d0
m68k_03f7dc_end:
.org 0x3F7E0
m68k_03f7e0:
        tst.w 0x8144:w
m68k_03f7e0_end:
.org 0x3F7E4
m68k_03f7e4:
        bne.b (. + 4)
m68k_03f7e4_end:
.org 0x3F7E6
m68k_03f7e6:
        addq.w #0x4,%d0
m68k_03f7e6_end:
.org 0x3F7E8
m68k_03f7e8:
        asl.w #0x1,%d0
m68k_03f7e8_end:
.org 0x3F7EA
m68k_03f7ea:
        lea.l 0x812a:w,%a0
m68k_03f7ea_end:
.org 0x3F7EE
m68k_03f7ee:
        btst.b #0x0,0x8123:w
m68k_03f7ee_end:
.org 0x3F7F4
m68k_03f7f4:
        beq.b (. + 40)
m68k_03f7f4_end:
.org 0x3F7F6
m68k_03f7f6:
        addq.w #0x1,(%a0, %d0.w)
m68k_03f7f6_end:
.org 0x3F7FA
m68k_03f7fa:
        cmpi.w #0xb,0x8160:w
m68k_03f7fa_end:
.org 0x3F800
m68k_03f800:
        bcc.b (. + 16)
m68k_03f800_end:
.org 0x3F802
m68k_03f802:
        cmpi.w #0x6,(%a0, %d0.w)
m68k_03f802_end:
.org 0x3F808
m68k_03f808:
        bcs.b (. + 20)
m68k_03f808_end:
.org 0x3F80A
m68k_03f80a:
        clr.w (%a0, %d0.w)
m68k_03f80a_end:
.org 0x3F80E
m68k_03f80e:
        bra.b (. + 14)
m68k_03f80e_end:
.org 0x3F810
m68k_03f810:
        cmpi.w #0x6,(%a0, %d0.w)
m68k_03f810_end:
.org 0x3F816
m68k_03f816:
        bls.b (. + 6)
m68k_03f816_end:
.org 0x3F818
m68k_03f818:
        clr.w (%a0, %d0.w)
m68k_03f818_end:
.org 0x3F81C
m68k_03f81c:
        btst.b #0x1,0x8123:w
m68k_03f81c_end:
.org 0x3F822
m68k_03f822:
        beq.b (. + 28)
m68k_03f822_end:
.org 0x3F824
m68k_03f824:
        subq.w #0x1,(%a0, %d0.w)
m68k_03f824_end:
.org 0x3F828
m68k_03f828:
        bpl.b (. + 22)
m68k_03f828_end:
.org 0x3F82A
m68k_03f82a:
        move.w #0x6,(%a0, %d0.w)
m68k_03f82a_end:
.org 0x3F830
m68k_03f830:
        cmpi.w #0xb,0x8160:w
m68k_03f830_end:
.org 0x3F836
m68k_03f836:
        bcc.b (. + 8)
m68k_03f836_end:
.org 0x3F838
m68k_03f838:
        move.w #0x5,(%a0, %d0.w)
m68k_03f838_end:
.org 0x3F83E
m68k_03f83e:
        rts
m68k_03f83e_end:
.org 0x3F844
m68k_03f844:
        cmpi.w #0x6,0x8148:w
m68k_03f844_end:
.org 0x3F84A
m68k_03f84a:
        bne.w (. + 14)
m68k_03f84a_end:
.org 0x3F84E
m68k_03f84e:
        move.w #0x2,0x8146:w
m68k_03f84e_end:
.org 0x3F854
m68k_03f854:
        bra.w (. + -130)
m68k_03f854_end:
.org 0x3F858
m68k_03f858:
        btst.b #0x0,0x8122:w
m68k_03f858_end:
.org 0x3F85E
m68k_03f85e:
        bne.w (. + -140)
m68k_03f85e_end:
.org 0x3F862
m68k_03f862:
        btst.b #0x1,0x8122:w
m68k_03f862_end:
.org 0x3F868
m68k_03f868:
        bne.w (. + -150)
m68k_03f868_end:
.org 0x3F86C
m68k_03f86c:
        btst.b #0x3,0x8123:w
m68k_03f86c_end:
.org 0x3F872
m68k_03f872:
        bne.b (. + 12)
m68k_03f872_end:
.org 0x3F874
m68k_03f874:
        btst.b #0x2,0x8123:w
m68k_03f874_end:
.org 0x3F87A
m68k_03f87a:
        beq.w (. + -168)
m68k_03f87a_end:
.org 0x3F87E
m68k_03f87e:
        subq.w #0x2,0x8146:w
m68k_03f87e_end:
.org 0x3F882
m68k_03f882:
        bpl.w (. + -176)
m68k_03f882_end:
.org 0x3F886
m68k_03f886:
        move.w #0x2,0x8146:w
m68k_03f886_end:
.org 0x3F88C
m68k_03f88c:
        bra.w (. + -186)
m68k_03f88c_end:
.org 0x3F8F6
m68k_03f8f6:
        moveq #0,%d0
m68k_03f8f6_end:
.org 0x3F8F8
m68k_03f8f8:
        move.w 0x80e6:w,%d0
m68k_03f8f8_end:
.org 0x3F8FC
m68k_03f8fc:
        bsr.w (. + -17956)
m68k_03f8fc_end:
.org 0x3F900
m68k_03f900:
        move.w #0xc3ae,%d0
m68k_03f900_end:
.org 0x3F904
m68k_03f904:
        moveq #4,%d3
m68k_03f904_end:
.org 0x3F906
m68k_03f906:
        lea.l 0x8001:w,%a0
m68k_03f906_end:
.org 0x3F90A
m68k_03f90a:
        bsr.w (. + 1636)
m68k_03f90a_end:
.org 0x3F90E
m68k_03f90e:
        moveq #0,%d0
m68k_03f90e_end:
.org 0x3F910
m68k_03f910:
        move.w 0x80ee:w,%d0
m68k_03f910_end:
.org 0x3F914
m68k_03f914:
        bsr.w (. + -17980)
m68k_03f914_end:
.org 0x3F918
m68k_03f918:
        move.w #0xc530,%d0
m68k_03f918_end:
.org 0x3F91C
m68k_03f91c:
        moveq #3,%d3
m68k_03f91c_end:
.org 0x3F91E
m68k_03f91e:
        lea.l 0x8002:w,%a0
m68k_03f91e_end:
.org 0x3F922
m68k_03f922:
        bsr.w (. + 1612)
m68k_03f922_end:
.org 0x3F926
m68k_03f926:
        moveq #0,%d0
m68k_03f926_end:
.org 0x3F928
m68k_03f928:
        move.w 0x80ea:w,%d0
m68k_03f928_end:
.org 0x3F92C
m68k_03f92c:
        bsr.w (. + -18004)
m68k_03f92c_end:
.org 0x3F930
m68k_03f930:
        move.w #0xc6b4,%d0
m68k_03f930_end:
.org 0x3F934
m68k_03f934:
        moveq #1,%d3
m68k_03f934_end:
.org 0x3F936
m68k_03f936:
        lea.l 0x8004:w,%a0
m68k_03f936_end:
.org 0x3F93A
m68k_03f93a:
        bra.w (. + 1552)
m68k_03f93a_end:
.org 0x3F93E
m68k_03f93e:
        moveq #0,%d0
m68k_03f93e_end:
.org 0x3F940
m68k_03f940:
        move.w 0x80ea:w,%d0
m68k_03f940_end:
.org 0x3F944
m68k_03f944:
        bsr.w (. + -18028)
m68k_03f944_end:
.org 0x3F948
m68k_03f948:
        move.w #0xc1ac,%d0
m68k_03f948_end:
.org 0x3F94C
m68k_03f94c:
        moveq #1,%d3
m68k_03f94c_end:
.org 0x3F94E
m68k_03f94e:
        lea.l 0x8004:w,%a0
m68k_03f94e_end:
.org 0x3F952
m68k_03f952:
        bsr.w (. + 1564)
m68k_03f952_end:
.org 0x3F956
m68k_03f956:
        moveq #0,%d0
m68k_03f956_end:
.org 0x3F958
m68k_03f958:
        move.w 0x80fa:w,%d0
m68k_03f958_end:
.org 0x3F95C
m68k_03f95c:
        bsr.w (. + -18052)
m68k_03f95c_end:
.org 0x3F960
m68k_03f960:
        move.w #0xc3ac,%d0
m68k_03f960_end:
.org 0x3F964
m68k_03f964:
        moveq #1,%d3
m68k_03f964_end:
.org 0x3F966
m68k_03f966:
        lea.l 0x8004:w,%a0
m68k_03f966_end:
.org 0x3F96A
m68k_03f96a:
        tst.w 0x8144:w
m68k_03f96a_end:
.org 0x3F96E
m68k_03f96e:
        bne.b (. + 10)
m68k_03f96e_end:
.org 0x3F970
m68k_03f970:
        bsr.w (. + 1498)
m68k_03f970_end:
.org 0x3F974
m68k_03f974:
        bra.w (. + 8)
m68k_03f974_end:
.org 0x3F978
m68k_03f978:
        bsr.w (. + 1526)
m68k_03f978_end:
.org 0x3F97C
m68k_03f97c:
        moveq #0,%d0
m68k_03f97c_end:
.org 0x3F97E
m68k_03f97e:
        move.w 0x80fc:w,%d0
m68k_03f97e_end:
.org 0x3F982
m68k_03f982:
        bsr.w (. + -18090)
m68k_03f982_end:
.org 0x3F986
m68k_03f986:
        move.w #0xc5ac,%d0
m68k_03f986_end:
.org 0x3F98A
m68k_03f98a:
        moveq #1,%d3
m68k_03f98a_end:
.org 0x3F98C
m68k_03f98c:
        lea.l 0x8004:w,%a0
m68k_03f98c_end:
.org 0x3F990
m68k_03f990:
        cmpi.w #0x1,0x8144:w
m68k_03f990_end:
.org 0x3F996
m68k_03f996:
        bne.b (. + 10)
m68k_03f996_end:
.org 0x3F998
m68k_03f998:
        bsr.w (. + 1458)
m68k_03f998_end:
.org 0x3F99C
m68k_03f99c:
        bra.w (. + 8)
m68k_03f99c_end:
.org 0x3F9A0
m68k_03f9a0:
        bsr.w (. + 1486)
m68k_03f9a0_end:
.org 0x3F9A4
m68k_03f9a4:
        moveq #0,%d0
m68k_03f9a4_end:
.org 0x3F9A6
m68k_03f9a6:
        move.w 0x80fe:w,%d0
m68k_03f9a6_end:
.org 0x3F9AA
m68k_03f9aa:
        bsr.w (. + -18130)
m68k_03f9aa_end:
.org 0x3F9AE
m68k_03f9ae:
        move.w #0xc7ac,%d0
m68k_03f9ae_end:
.org 0x3F9B2
m68k_03f9b2:
        moveq #1,%d3
m68k_03f9b2_end:
.org 0x3F9B4
m68k_03f9b4:
        lea.l 0x8004:w,%a0
m68k_03f9b4_end:
.org 0x3F9B8
m68k_03f9b8:
        cmpi.w #0x2,0x8144:w
m68k_03f9b8_end:
.org 0x3F9BE
m68k_03f9be:
        bne.w (. + 1456)
m68k_03f9be_end:
.org 0x3F9C2
m68k_03f9c2:
        bra.w (. + 1416)
m68k_03f9c2_end:
.org 0x3F9C6
m68k_03f9c6:
        cmpi.b #0x3,0x80db:w
m68k_03f9c6_end:
.org 0x3F9CC
m68k_03f9cc:
        beq.w (. + 788)
m68k_03f9cc_end:
.org 0x3F9D0
m68k_03f9d0:
        move.w #0xc412,0x8010:w
m68k_03f9d0_end:
.org 0x3F9D6
m68k_03f9d6:
        move.w #0xc420,0x8012:w
m68k_03f9d6_end:
.org 0x3F9DC
m68k_03f9dc:
        move.w #0xc430,0x8014:w
m68k_03f9dc_end:
.org 0x3F9E2
m68k_03f9e2:
        move.w #0xc440,0x8016:w
m68k_03f9e2_end:
.org 0x3F9E8
m68k_03f9e8:
        move.w #0xc398,0x8018:w
m68k_03f9e8_end:
.org 0x3F9EE
m68k_03f9ee:
        clr.w 0x801a:w
m68k_03f9ee_end:
.org 0x3F9F2
m68k_03f9f2:
        move.l #0xffff827a,0x801c:w
m68k_03f9f2_end:
.org 0x3F9FA
m68k_03f9fa:
        lea.l 0x826a:w,%a6
m68k_03f9fa_end:
.org 0x3F9FE
m68k_03f9fe:
        bsr.w (. + 52)
m68k_03f9fe_end:
.org 0x3FA02
m68k_03fa02:
        move.w #0xc292,0x8010:w
m68k_03fa02_end:
.org 0x3FA08
m68k_03fa08:
        move.w #0xc2a0,0x8012:w
m68k_03fa08_end:
.org 0x3FA0E
m68k_03fa0e:
        move.w #0xc2b0,0x8014:w
m68k_03fa0e_end:
.org 0x3FA14
m68k_03fa14:
        move.w #0xc2c0,0x8016:w
m68k_03fa14_end:
.org 0x3FA1A
m68k_03fa1a:
        move.w #0xc218,0x8018:w
m68k_03fa1a_end:
.org 0x3FA20
m68k_03fa20:
        move.w #0x1,0x801a:w
m68k_03fa20_end:
.org 0x3FA26
m68k_03fa26:
        move.l #0xffff817a,0x801c:w
m68k_03fa26_end:
.org 0x3FA2E
m68k_03fa2e:
        lea.l 0x816a:w,%a6
m68k_03fa2e_end:
.org 0x3FA32
m68k_03fa32:
        moveq #0,%d0
m68k_03fa32_end:
.org 0x3FA34
m68k_03fa34:
        move.w 0xe(%a6),%d0
m68k_03fa34_end:
.org 0x3FA38
m68k_03fa38:
        bsr.w (. + -18272)
m68k_03fa38_end:
.org 0x3FA3C
m68k_03fa3c:
        move.w 0x8010:w,%d0
m68k_03fa3c_end:
.org 0x3FA40
m68k_03fa40:
        moveq #2,%d3
m68k_03fa40_end:
.org 0x3FA42
m68k_03fa42:
        lea.l 0x8003:w,%a0
m68k_03fa42_end:
.org 0x3FA46
m68k_03fa46:
        bsr.w (. + 1320)
m68k_03fa46_end:
.org 0x3FA4A
m68k_03fa4a:
        move.w #0xe,%d1
m68k_03fa4a_end:
.org 0x3FA4E
m68k_03fa4e:
        movea.l 0x801c:w,%a6
m68k_03fa4e_end:
.org 0x3FA52
m68k_03fa52:
        moveq #0,%d0
m68k_03fa52_end:
.org 0x3FA54
m68k_03fa54:
        btst.b #0x7,(%a6)
m68k_03fa54_end:
.org 0x3FA58
m68k_03fa58:
        beq.b (. + 14)
m68k_03fa58_end:
.org 0x3FA5A
m68k_03fa5a:
        cmpi.b #0x2,0x1(%a6)
m68k_03fa5a_end:
.org 0x3FA60
m68k_03fa60:
        bne.b (. + 6)
m68k_03fa60_end:
.org 0x3FA62
m68k_03fa62:
        add.w 0xe(%a6),%d0
m68k_03fa62_end:
.org 0x3FA66
m68k_03fa66:
        adda.w #0x10,%a6
m68k_03fa66_end:
.org 0x3FA6A
m68k_03fa6a:
        dbra %d1,(. + -22)
m68k_03fa6a_end:
.org 0x3FA6E
m68k_03fa6e:
        bsr.w (. + -18326)
m68k_03fa6e_end:
.org 0x3FA72
m68k_03fa72:
        move.w 0x8012:w,%d0
m68k_03fa72_end:
.org 0x3FA76
m68k_03fa76:
        moveq #3,%d3
m68k_03fa76_end:
.org 0x3FA78
m68k_03fa78:
        lea.l 0x8002:w,%a0
m68k_03fa78_end:
.org 0x3FA7C
m68k_03fa7c:
        bsr.w (. + 1266)
m68k_03fa7c_end:
.org 0x3FA80
m68k_03fa80:
        move.w #0xe,%d1
m68k_03fa80_end:
.org 0x3FA84
m68k_03fa84:
        movea.l 0x801c:w,%a6
m68k_03fa84_end:
.org 0x3FA88
m68k_03fa88:
        moveq #0,%d0
m68k_03fa88_end:
.org 0x3FA8A
m68k_03fa8a:
        btst.b #0x7,(%a6)
m68k_03fa8a_end:
.org 0x3FA8E
m68k_03fa8e:
        beq.b (. + 14)
m68k_03fa8e_end:
.org 0x3FA90
m68k_03fa90:
        cmpi.b #0x1,0x1(%a6)
m68k_03fa90_end:
.org 0x3FA96
m68k_03fa96:
        bne.b (. + 6)
m68k_03fa96_end:
.org 0x3FA98
m68k_03fa98:
        add.w 0xe(%a6),%d0
m68k_03fa98_end:
.org 0x3FA9C
m68k_03fa9c:
        adda.w #0x10,%a6
m68k_03fa9c_end:
.org 0x3FAA0
m68k_03faa0:
        dbra %d1,(. + -22)
m68k_03faa0_end:
.org 0x3FAA4
m68k_03faa4:
        bsr.w (. + -18380)
m68k_03faa4_end:
.org 0x3FAA8
m68k_03faa8:
        move.w 0x8014:w,%d0
m68k_03faa8_end:
.org 0x3FAAC
m68k_03faac:
        moveq #3,%d3
m68k_03faac_end:
.org 0x3FAAE
m68k_03faae:
        lea.l 0x8002:w,%a0
m68k_03faae_end:
.org 0x3FAB2
m68k_03fab2:
        bsr.w (. + 1212)
m68k_03fab2_end:
.org 0x3FAB6
m68k_03fab6:
        move.w #0xe,%d1
m68k_03fab6_end:
.org 0x3FABA
m68k_03faba:
        movea.l 0x801c:w,%a6
m68k_03faba_end:
.org 0x3FABE
m68k_03fabe:
        moveq #0,%d0
m68k_03fabe_end:
.org 0x3FAC0
m68k_03fac0:
        btst.b #0x7,(%a6)
m68k_03fac0_end:
.org 0x3FAC4
m68k_03fac4:
        beq.b (. + 12)
m68k_03fac4_end:
.org 0x3FAC6
m68k_03fac6:
        tst.b 0x1(%a6)
m68k_03fac6_end:
.org 0x3FACA
m68k_03faca:
        bne.b (. + 6)
m68k_03faca_end:
.org 0x3FACC
m68k_03facc:
        add.w 0xe(%a6),%d0
m68k_03facc_end:
.org 0x3FAD0
m68k_03fad0:
        adda.w #0x10,%a6
m68k_03fad0_end:
.org 0x3FAD4
m68k_03fad4:
        dbra %d1,(. + -20)
m68k_03fad4_end:
.org 0x3FAD8
m68k_03fad8:
        bsr.w (. + -18432)
m68k_03fad8_end:
.org 0x3FADC
m68k_03fadc:
        move.w 0x8016:w,%d0
m68k_03fadc_end:
.org 0x3FAE0
m68k_03fae0:
        moveq #4,%d3
m68k_03fae0_end:
.org 0x3FAE2
m68k_03fae2:
        lea.l 0x8001:w,%a0
m68k_03fae2_end:
.org 0x3FAE6
m68k_03fae6:
        bsr.w (. + 1160)
m68k_03fae6_end:
.org 0x3FAEA
m68k_03faea:
        tst.w 0x8144:w
m68k_03faea_end:
.org 0x3FAEE
m68k_03faee:
        beq.b (. + 10)
m68k_03faee_end:
.org 0x3FAF0
m68k_03faf0:
        tst.w 0x801a:w
m68k_03faf0_end:
.org 0x3FAF4
m68k_03faf4:
        bne.b (. + 12)
m68k_03faf4_end:
.org 0x3FAF6
m68k_03faf6:
        rts
m68k_03faf6_end:
.org 0x3FAF8
m68k_03faf8:
        tst.w 0x801a:w
m68k_03faf8_end:
.org 0x3FAFC
m68k_03fafc:
        bne.w (. + 864)
m68k_03fafc_end:
.org 0x3FB00
m68k_03fb00:
        move.w #0x8f02,0xc00004:l
m68k_03fb00_end:
.org 0x3FB08
m68k_03fb08:
        move.w 0x8018:w,%d0
m68k_03fb08_end:
.org 0x3FB0C
m68k_03fb0c:
        bsr.w (. + -18524)
m68k_03fb0c_end:
.org 0x3FB10
m68k_03fb10:
        tst.w 0x8146:w
m68k_03fb10_end:
.org 0x3FB14
m68k_03fb14:
        bne.b (. + 40)
m68k_03fb14_end:
.org 0x3FB16
m68k_03fb16:
        btst.b #0x4,0xf321:w
m68k_03fb16_end:
.org 0x3FB1C
m68k_03fb1c:
        bne.b (. + 32)
m68k_03fb1c_end:
.org 0x3FB1E
m68k_03fb1e:
        move.w #0xc448,0xc00000:l
m68k_03fb1e_end:
.org 0x3FB26
m68k_03fb26:
        move.w 0x8018:w,%d0
m68k_03fb26_end:
.org 0x3FB2A
m68k_03fb2a:
        addi.w #0x80,%d0
m68k_03fb2a_end:
.org 0x3FB2E
m68k_03fb2e:
        bsr.w (. + -18558)
m68k_03fb2e_end:
.org 0x3FB32
m68k_03fb32:
        move.w #0xc448,0xc00000:l
m68k_03fb32_end:
.org 0x3FB3A
m68k_03fb3a:
        bra.b (. + 50)
m68k_03fb3a_end:
.org 0x3FB3C
m68k_03fb3c:
        bsr.w (. + 364)
m68k_03fb3c_end:
.org 0x3FB40
m68k_03fb40:
        move.w 0x6(%a0),%d2
m68k_03fb40_end:
.org 0x3FB44
m68k_03fb44:
        bsr.w (. + 372)
m68k_03fb44_end:
.org 0x3FB48
m68k_03fb48:
        move.w %d0,0xc00000:l
m68k_03fb48_end:
.org 0x3FB4E
m68k_03fb4e:
        move.w 0x8018:w,%d0
m68k_03fb4e_end:
.org 0x3FB52
m68k_03fb52:
        addi.w #0x80,%d0
m68k_03fb52_end:
.org 0x3FB56
m68k_03fb56:
        bsr.w (. + -18598)
m68k_03fb56_end:
.org 0x3FB5A
m68k_03fb5a:
        bsr.w (. + 334)
m68k_03fb5a_end:
.org 0x3FB5E
m68k_03fb5e:
        move.w 0x6(%a0),%d2
m68k_03fb5e_end:
.org 0x3FB62
m68k_03fb62:
        bsr.w (. + 342)
m68k_03fb62_end:
.org 0x3FB66
m68k_03fb66:
        move.w %d1,0xc00000:l
m68k_03fb66_end:
.org 0x3FB6C
m68k_03fb6c:
        move.w 0x8018:w,%d0
m68k_03fb6c_end:
.org 0x3FB70
m68k_03fb70:
        addi.w #0x10,%d0
m68k_03fb70_end:
.org 0x3FB74
m68k_03fb74:
        bsr.w (. + -18628)
m68k_03fb74_end:
.org 0x3FB78
m68k_03fb78:
        cmpi.w #0x1,0x8146:w
m68k_03fb78_end:
.org 0x3FB7E
m68k_03fb7e:
        bne.b (. + 40)
m68k_03fb7e_end:
.org 0x3FB80
m68k_03fb80:
        btst.b #0x4,0xf321:w
m68k_03fb80_end:
.org 0x3FB86
m68k_03fb86:
        bne.b (. + 32)
m68k_03fb86_end:
.org 0x3FB88
m68k_03fb88:
        move.w #0xc448,0xc00000:l
m68k_03fb88_end:
.org 0x3FB90
m68k_03fb90:
        move.w 0x8018:w,%d0
m68k_03fb90_end:
.org 0x3FB94
m68k_03fb94:
        addi.w #0x90,%d0
m68k_03fb94_end:
.org 0x3FB98
m68k_03fb98:
        bsr.w (. + -18664)
m68k_03fb98_end:
.org 0x3FB9C
m68k_03fb9c:
        move.w #0xc448,0xc00000:l
m68k_03fb9c_end:
.org 0x3FBA4
m68k_03fba4:
        bra.b (. + 50)
m68k_03fba4_end:
.org 0x3FBA6
m68k_03fba6:
        bsr.w (. + 258)
m68k_03fba6_end:
.org 0x3FBAA
m68k_03fbaa:
        move.w 0x4(%a0),%d2
m68k_03fbaa_end:
.org 0x3FBAE
m68k_03fbae:
        bsr.w (. + 266)
m68k_03fbae_end:
.org 0x3FBB2
m68k_03fbb2:
        move.w %d0,0xc00000:l
m68k_03fbb2_end:
.org 0x3FBB8
m68k_03fbb8:
        move.w 0x8018:w,%d0
m68k_03fbb8_end:
.org 0x3FBBC
m68k_03fbbc:
        addi.w #0x90,%d0
m68k_03fbbc_end:
.org 0x3FBC0
m68k_03fbc0:
        bsr.w (. + -18704)
m68k_03fbc0_end:
.org 0x3FBC4
m68k_03fbc4:
        bsr.w (. + 228)
m68k_03fbc4_end:
.org 0x3FBC8
m68k_03fbc8:
        move.w 0x4(%a0),%d2
m68k_03fbc8_end:
.org 0x3FBCC
m68k_03fbcc:
        bsr.w (. + 236)
m68k_03fbcc_end:
.org 0x3FBD0
m68k_03fbd0:
        move.w %d1,0xc00000:l
m68k_03fbd0_end:
.org 0x3FBD6
m68k_03fbd6:
        move.w 0x8018:w,%d0
m68k_03fbd6_end:
.org 0x3FBDA
m68k_03fbda:
        addi.w #0x20,%d0
m68k_03fbda_end:
.org 0x3FBDE
m68k_03fbde:
        bsr.w (. + -18734)
m68k_03fbde_end:
.org 0x3FBE2
m68k_03fbe2:
        cmpi.w #0x2,0x8146:w
m68k_03fbe2_end:
.org 0x3FBE8
m68k_03fbe8:
        bne.b (. + 40)
m68k_03fbe8_end:
.org 0x3FBEA
m68k_03fbea:
        btst.b #0x4,0xf321:w
m68k_03fbea_end:
.org 0x3FBF0
m68k_03fbf0:
        bne.b (. + 32)
m68k_03fbf0_end:
.org 0x3FBF2
m68k_03fbf2:
        move.w #0xc448,0xc00000:l
m68k_03fbf2_end:
.org 0x3FBFA
m68k_03fbfa:
        move.w 0x8018:w,%d0
m68k_03fbfa_end:
.org 0x3FBFE
m68k_03fbfe:
        addi.w #0xa0,%d0
m68k_03fbfe_end:
.org 0x3FC02
m68k_03fc02:
        bsr.w (. + -18770)
m68k_03fc02_end:
.org 0x3FC06
m68k_03fc06:
        move.w #0xc448,0xc00000:l
m68k_03fc06_end:
.org 0x3FC0E
m68k_03fc0e:
        bra.b (. + 50)
m68k_03fc0e_end:
.org 0x3FC10
m68k_03fc10:
        bsr.w (. + 152)
m68k_03fc10_end:
.org 0x3FC14
m68k_03fc14:
        move.w 0x2(%a0),%d2
m68k_03fc14_end:
.org 0x3FC18
m68k_03fc18:
        bsr.w (. + 160)
m68k_03fc18_end:
.org 0x3FC1C
m68k_03fc1c:
        move.w %d0,0xc00000:l
m68k_03fc1c_end:
.org 0x3FC22
m68k_03fc22:
        move.w 0x8018:w,%d0
m68k_03fc22_end:
.org 0x3FC26
m68k_03fc26:
        addi.w #0xa0,%d0
m68k_03fc26_end:
.org 0x3FC2A
m68k_03fc2a:
        bsr.w (. + -18810)
m68k_03fc2a_end:
.org 0x3FC2E
m68k_03fc2e:
        bsr.w (. + 122)
m68k_03fc2e_end:
.org 0x3FC32
m68k_03fc32:
        move.w 0x2(%a0),%d2
m68k_03fc32_end:
.org 0x3FC36
m68k_03fc36:
        bsr.w (. + 130)
m68k_03fc36_end:
.org 0x3FC3A
m68k_03fc3a:
        move.w %d1,0xc00000:l
m68k_03fc3a_end:
.org 0x3FC40
m68k_03fc40:
        move.w 0x8018:w,%d0
m68k_03fc40_end:
.org 0x3FC44
m68k_03fc44:
        addi.w #0x32,%d0
m68k_03fc44_end:
.org 0x3FC48
m68k_03fc48:
        bsr.w (. + -18840)
m68k_03fc48_end:
.org 0x3FC4C
m68k_03fc4c:
        cmpi.w #0x3,0x8146:w
m68k_03fc4c_end:
.org 0x3FC52
m68k_03fc52:
        bne.b (. + 40)
m68k_03fc52_end:
.org 0x3FC54
m68k_03fc54:
        btst.b #0x4,0xf321:w
m68k_03fc54_end:
.org 0x3FC5A
m68k_03fc5a:
        bne.b (. + 32)
m68k_03fc5a_end:
.org 0x3FC5C
m68k_03fc5c:
        move.w #0xc448,0xc00000:l
m68k_03fc5c_end:
.org 0x3FC64
m68k_03fc64:
        move.w 0x8018:w,%d0
m68k_03fc64_end:
.org 0x3FC68
m68k_03fc68:
        addi.w #0xb2,%d0
m68k_03fc68_end:
.org 0x3FC6C
m68k_03fc6c:
        bsr.w (. + -18876)
m68k_03fc6c_end:
.org 0x3FC70
m68k_03fc70:
        move.w #0xc448,0xc00000:l
m68k_03fc70_end:
.org 0x3FC78
m68k_03fc78:
        rts
m68k_03fc78_end:
.org 0x3FC7A
m68k_03fc7a:
        bsr.w (. + 46)
m68k_03fc7a_end:
.org 0x3FC7E
m68k_03fc7e:
        move.w (%a0),%d2
m68k_03fc7e_end:
.org 0x3FC80
m68k_03fc80:
        bsr.w (. + 56)
m68k_03fc80_end:
.org 0x3FC84
m68k_03fc84:
        move.w %d0,0xc00000:l
m68k_03fc84_end:
.org 0x3FC8A
m68k_03fc8a:
        move.w 0x8018:w,%d0
m68k_03fc8a_end:
.org 0x3FC8E
m68k_03fc8e:
        addi.w #0xb2,%d0
m68k_03fc8e_end:
.org 0x3FC92
m68k_03fc92:
        bsr.w (. + -18914)
m68k_03fc92_end:
.org 0x3FC96
m68k_03fc96:
        bsr.w (. + 18)
m68k_03fc96_end:
.org 0x3FC9A
m68k_03fc9a:
        move.w (%a0),%d2
m68k_03fc9a_end:
.org 0x3FC9C
m68k_03fc9c:
        bsr.w (. + 28)
m68k_03fc9c_end:
.org 0x3FCA0
m68k_03fca0:
        move.w %d1,0xc00000:l
m68k_03fca0_end:
.org 0x3FCA6
m68k_03fca6:
        rts
m68k_03fca6_end:
.org 0x3FCA8
m68k_03fca8:
        lea.l 0x8132:w,%a0
m68k_03fca8_end:
.org 0x3FCAC
m68k_03fcac:
        tst.w 0x8144:w
m68k_03fcac_end:
.org 0x3FCB0
m68k_03fcb0:
        beq.b (. + 6)
m68k_03fcb0_end:
.org 0x3FCB2
m68k_03fcb2:
        lea.l 0x812a:w,%a0
m68k_03fcb2_end:
.org 0x3FCB6
m68k_03fcb6:
        rts
m68k_03fcb6_end:
.org 0x3FCB8
m68k_03fcb8:
        asl.w #0x2,%d2
m68k_03fcb8_end:
.org 0x3FCBA
m68k_03fcba:
        move.w 8(%pc, %d2.w),%d0
m68k_03fcba_end:
.org 0x3FCBE
m68k_03fcbe:
        move.w 6(%pc, %d2.w),%d1
m68k_03fcbe_end:
.org 0x3FCC2
m68k_03fcc2:
        rts
m68k_03fcc2_end:
.org 0x3FCE0
m68k_03fce0:
        move.w #0xc49e,0x8010:w
m68k_03fce0_end:
.org 0x3FCE6
m68k_03fce6:
        move.w #0xc4b0,0x8012:w
m68k_03fce6_end:
.org 0x3FCEC
m68k_03fcec:
        move.w #0xc424,0x8014:w
m68k_03fcec_end:
.org 0x3FCF2
m68k_03fcf2:
        move.w #0xc43a,0x8016:w
m68k_03fcf2_end:
.org 0x3FCF8
m68k_03fcf8:
        clr.w 0x8018:w
m68k_03fcf8_end:
.org 0x3FCFC
m68k_03fcfc:
        lea.l 0x826a:w,%a6
m68k_03fcfc_end:
.org 0x3FD00
m68k_03fd00:
        bsr.w (. + 38)
m68k_03fd00_end:
.org 0x3FD04
m68k_03fd04:
        lea.l 0x816a:w,%a6
m68k_03fd04_end:
.org 0x3FD08
m68k_03fd08:
        move.w #0xc31e,0x8010:w
m68k_03fd08_end:
.org 0x3FD0E
m68k_03fd0e:
        move.w #0xc330,0x8012:w
m68k_03fd0e_end:
.org 0x3FD14
m68k_03fd14:
        move.w #0xc2a4,0x8014:w
m68k_03fd14_end:
.org 0x3FD1A
m68k_03fd1a:
        move.w #0xc2ba,0x8016:w
m68k_03fd1a_end:
.org 0x3FD20
m68k_03fd20:
        move.w #0x1,0x8018:w
m68k_03fd20_end:
.org 0x3FD26
m68k_03fd26:
        moveq #0,%d0
m68k_03fd26_end:
.org 0x3FD28
m68k_03fd28:
        move.w 0xe(%a6),%d0
m68k_03fd28_end:
.org 0x3FD2C
m68k_03fd2c:
        bsr.w (. + -19028)
m68k_03fd2c_end:
.org 0x3FD30
m68k_03fd30:
        move.w 0x8010:w,%d0
m68k_03fd30_end:
.org 0x3FD34
m68k_03fd34:
        moveq #2,%d3
m68k_03fd34_end:
.org 0x3FD36
m68k_03fd36:
        lea.l 0x8003:w,%a0
m68k_03fd36_end:
.org 0x3FD3A
m68k_03fd3a:
        bsr.w (. + 564)
m68k_03fd3a_end:
.org 0x3FD3E
m68k_03fd3e:
        move.w #0xe,%d1
m68k_03fd3e_end:
.org 0x3FD42
m68k_03fd42:
        adda.w #0x10,%a6
m68k_03fd42_end:
.org 0x3FD46
m68k_03fd46:
        moveq #0,%d0
m68k_03fd46_end:
.org 0x3FD48
m68k_03fd48:
        btst.b #0x7,(%a6)
m68k_03fd48_end:
.org 0x3FD4C
m68k_03fd4c:
        beq.b (. + 14)
m68k_03fd4c_end:
.org 0x3FD4E
m68k_03fd4e:
        cmpi.b #0x1,0x1(%a6)
m68k_03fd4e_end:
.org 0x3FD54
m68k_03fd54:
        bne.b (. + 6)
m68k_03fd54_end:
.org 0x3FD56
m68k_03fd56:
        add.w 0xe(%a6),%d0
m68k_03fd56_end:
.org 0x3FD5A
m68k_03fd5a:
        adda.w #0x10,%a6
m68k_03fd5a_end:
.org 0x3FD5E
m68k_03fd5e:
        dbra %d1,(. + -22)
m68k_03fd5e_end:
.org 0x3FD62
m68k_03fd62:
        bsr.w (. + -19082)
m68k_03fd62_end:
.org 0x3FD66
m68k_03fd66:
        move.w 0x8012:w,%d0
m68k_03fd66_end:
.org 0x3FD6A
m68k_03fd6a:
        moveq #4,%d3
m68k_03fd6a_end:
.org 0x3FD6C
m68k_03fd6c:
        lea.l 0x8001:w,%a0
m68k_03fd6c_end:
.org 0x3FD70
m68k_03fd70:
        bsr.w (. + 510)
m68k_03fd70_end:
.org 0x3FD74
m68k_03fd74:
        tst.w 0x8144:w
m68k_03fd74_end:
.org 0x3FD78
m68k_03fd78:
        beq.b (. + 10)
m68k_03fd78_end:
.org 0x3FD7A
m68k_03fd7a:
        tst.w 0x8018:w
m68k_03fd7a_end:
.org 0x3FD7E
m68k_03fd7e:
        bne.b (. + 12)
m68k_03fd7e_end:
.org 0x3FD80
m68k_03fd80:
        rts
m68k_03fd80_end:
.org 0x3FD82
m68k_03fd82:
        tst.w 0x8018:w
m68k_03fd82_end:
.org 0x3FD86
m68k_03fd86:
        bne.w (. + 214)
m68k_03fd86_end:
.org 0x3FD8A
m68k_03fd8a:
        move.w #0x8f02,0xc00004:l
m68k_03fd8a_end:
.org 0x3FD92
m68k_03fd92:
        move.w 0x8014:w,%d0
m68k_03fd92_end:
.org 0x3FD96
m68k_03fd96:
        bsr.w (. + -19174)
m68k_03fd96_end:
.org 0x3FD9A
m68k_03fd9a:
        tst.w 0x8146:w
m68k_03fd9a_end:
.org 0x3FD9E
m68k_03fd9e:
        bne.b (. + 40)
m68k_03fd9e_end:
.org 0x3FDA0
m68k_03fda0:
        btst.b #0x4,0xf321:w
m68k_03fda0_end:
.org 0x3FDA6
m68k_03fda6:
        bne.b (. + 32)
m68k_03fda6_end:
.org 0x3FDA8
m68k_03fda8:
        move.w #0xc448,0xc00000:l
m68k_03fda8_end:
.org 0x3FDB0
m68k_03fdb0:
        move.w 0x8014:w,%d0
m68k_03fdb0_end:
.org 0x3FDB4
m68k_03fdb4:
        addi.w #0x80,%d0
m68k_03fdb4_end:
.org 0x3FDB8
m68k_03fdb8:
        bsr.w (. + -19208)
m68k_03fdb8_end:
.org 0x3FDBC
m68k_03fdbc:
        move.w #0xc448,0xc00000:l
m68k_03fdbc_end:
.org 0x3FDC4
m68k_03fdc4:
        bra.b (. + 50)
m68k_03fdc4_end:
.org 0x3FDC6
m68k_03fdc6:
        bsr.w (. + -286)
m68k_03fdc6_end:
.org 0x3FDCA
m68k_03fdca:
        move.w 0x6(%a0),%d2
m68k_03fdca_end:
.org 0x3FDCE
m68k_03fdce:
        bsr.w (. + -278)
m68k_03fdce_end:
.org 0x3FDD2
m68k_03fdd2:
        move.w %d0,0xc00000:l
m68k_03fdd2_end:
.org 0x3FDD8
m68k_03fdd8:
        move.w 0x8014:w,%d0
m68k_03fdd8_end:
.org 0x3FDDC
m68k_03fddc:
        addi.w #0x80,%d0
m68k_03fddc_end:
.org 0x3FDE0
m68k_03fde0:
        bsr.w (. + -19248)
m68k_03fde0_end:
.org 0x3FDE4
m68k_03fde4:
        bsr.w (. + -316)
m68k_03fde4_end:
.org 0x3FDE8
m68k_03fde8:
        move.w 0x6(%a0),%d2
m68k_03fde8_end:
.org 0x3FDEC
m68k_03fdec:
        bsr.w (. + -308)
m68k_03fdec_end:
.org 0x3FDF0
m68k_03fdf0:
        move.w %d1,0xc00000:l
m68k_03fdf0_end:
.org 0x3FDF6
m68k_03fdf6:
        move.w 0x8016:w,%d0
m68k_03fdf6_end:
.org 0x3FDFA
m68k_03fdfa:
        bsr.w (. + -19274)
m68k_03fdfa_end:
.org 0x3FDFE
m68k_03fdfe:
        cmpi.w #0x2,0x8146:w
m68k_03fdfe_end:
.org 0x3FE04
m68k_03fe04:
        bne.b (. + 40)
m68k_03fe04_end:
.org 0x3FE06
m68k_03fe06:
        btst.b #0x4,0xf321:w
m68k_03fe06_end:
.org 0x3FE0C
m68k_03fe0c:
        bne.b (. + 32)
m68k_03fe0c_end:
.org 0x3FE0E
m68k_03fe0e:
        move.w #0xc448,0xc00000:l
m68k_03fe0e_end:
.org 0x3FE16
m68k_03fe16:
        move.w 0x8016:w,%d0
m68k_03fe16_end:
.org 0x3FE1A
m68k_03fe1a:
        addi.w #0x80,%d0
m68k_03fe1a_end:
.org 0x3FE1E
m68k_03fe1e:
        bsr.w (. + -19310)
m68k_03fe1e_end:
.org 0x3FE22
m68k_03fe22:
        move.w #0xc448,0xc00000:l
m68k_03fe22_end:
.org 0x3FE2A
m68k_03fe2a:
        bra.b (. + 50)
m68k_03fe2a_end:
.org 0x3FE2C
m68k_03fe2c:
        bsr.w (. + -388)
m68k_03fe2c_end:
.org 0x3FE30
m68k_03fe30:
        move.w 0x2(%a0),%d2
m68k_03fe30_end:
.org 0x3FE34
m68k_03fe34:
        bsr.w (. + -380)
m68k_03fe34_end:
.org 0x3FE38
m68k_03fe38:
        move.w %d0,0xc00000:l
m68k_03fe38_end:
.org 0x3FE3E
m68k_03fe3e:
        move.w 0x8016:w,%d0
m68k_03fe3e_end:
.org 0x3FE42
m68k_03fe42:
        addi.w #0x80,%d0
m68k_03fe42_end:
.org 0x3FE46
m68k_03fe46:
        bsr.w (. + -19350)
m68k_03fe46_end:
.org 0x3FE4A
m68k_03fe4a:
        bsr.w (. + -418)
m68k_03fe4a_end:
.org 0x3FE4E
m68k_03fe4e:
        move.w 0x2(%a0),%d2
m68k_03fe4e_end:
.org 0x3FE52
m68k_03fe52:
        bsr.w (. + -410)
m68k_03fe52_end:
.org 0x3FE56
m68k_03fe56:
        move.w %d1,0xc00000:l
m68k_03fe56_end:
.org 0x3FE5C
m68k_03fe5c:
        rts
m68k_03fe5c_end:
.org 0x3FE5E
m68k_03fe5e:
        moveq #0,%d0
m68k_03fe5e_end:
.org 0x3FE60
m68k_03fe60:
        move.w 0x8176:w,%d0
m68k_03fe60_end:
.org 0x3FE64
m68k_03fe64:
        bsr.w (. + -19340)
m68k_03fe64_end:
.org 0x3FE68
m68k_03fe68:
        move.w #0xc5a0,%d0
m68k_03fe68_end:
.org 0x3FE6C
m68k_03fe6c:
        moveq #2,%d3
m68k_03fe6c_end:
.org 0x3FE6E
m68k_03fe6e:
        lea.l 0x8003:w,%a0
m68k_03fe6e_end:
.org 0x3FE72
m68k_03fe72:
        bsr.w (. + 252)
m68k_03fe72_end:
.org 0x3FE76
m68k_03fe76:
        moveq #0,%d0
m68k_03fe76_end:
.org 0x3FE78
m68k_03fe78:
        move.w 0x8186:w,%d0
m68k_03fe78_end:
.org 0x3FE7C
m68k_03fe7c:
        bsr.w (. + -19364)
m68k_03fe7c_end:
.org 0x3FE80
m68k_03fe80:
        move.w #0xc720,%d0
m68k_03fe80_end:
.org 0x3FE84
m68k_03fe84:
        moveq #2,%d3
m68k_03fe84_end:
.org 0x3FE86
m68k_03fe86:
        lea.l 0x8003:w,%a0
m68k_03fe86_end:
.org 0x3FE8A
m68k_03fe8a:
        bsr.w (. + 228)
m68k_03fe8a_end:
.org 0x3FE8E
m68k_03fe8e:
        moveq #0,%d0
m68k_03fe8e_end:
.org 0x3FE90
m68k_03fe90:
        move.w 0x8276:w,%d0
m68k_03fe90_end:
.org 0x3FE94
m68k_03fe94:
        bsr.w (. + -19388)
m68k_03fe94_end:
.org 0x3FE98
m68k_03fe98:
        move.w #0xc5b2,%d0
m68k_03fe98_end:
.org 0x3FE9C
m68k_03fe9c:
        moveq #2,%d3
m68k_03fe9c_end:
.org 0x3FE9E
m68k_03fe9e:
        lea.l 0x8003:w,%a0
m68k_03fe9e_end:
.org 0x3FEA2
m68k_03fea2:
        bsr.w (. + 204)
m68k_03fea2_end:
.org 0x3FEA6
m68k_03fea6:
        moveq #0,%d0
m68k_03fea6_end:
.org 0x3FEA8
m68k_03fea8:
        move.w 0x8286:w,%d0
m68k_03fea8_end:
.org 0x3FEAC
m68k_03feac:
        bsr.w (. + -19412)
m68k_03feac_end:
.org 0x3FEB0
m68k_03feb0:
        move.w #0xc732,%d0
m68k_03feb0_end:
.org 0x3FEB4
m68k_03feb4:
        moveq #2,%d3
m68k_03feb4_end:
.org 0x3FEB6
m68k_03feb6:
        lea.l 0x8003:w,%a0
m68k_03feb6_end:
.org 0x3FEBA
m68k_03feba:
        bsr.w (. + 180)
m68k_03feba_end:
.org 0x3FEBE
m68k_03febe:
        moveq #0,%d0
m68k_03febe_end:
.org 0x3FEC0
m68k_03fec0:
        move.w 0x8100:w,%d0
m68k_03fec0_end:
.org 0x3FEC4
m68k_03fec4:
        bsr.w (. + -19436)
m68k_03fec4_end:
.org 0x3FEC8
m68k_03fec8:
        move.w #0xc8a0,%d0
m68k_03fec8_end:
.org 0x3FECC
m68k_03fecc:
        moveq #2,%d3
m68k_03fecc_end:
.org 0x3FECE
m68k_03fece:
        lea.l 0x8003:w,%a0
m68k_03fece_end:
.org 0x3FED2
m68k_03fed2:
        bsr.w (. + 156)
m68k_03fed2_end:
.org 0x3FED6
m68k_03fed6:
        moveq #0,%d0
m68k_03fed6_end:
.org 0x3FED8
m68k_03fed8:
        move.w 0x8102:w,%d0
m68k_03fed8_end:
.org 0x3FEDC
m68k_03fedc:
        bsr.w (. + -19460)
m68k_03fedc_end:
.org 0x3FEE0
m68k_03fee0:
        move.w #0xc8b2,%d0
m68k_03fee0_end:
.org 0x3FEE4
m68k_03fee4:
        moveq #2,%d3
m68k_03fee4_end:
.org 0x3FEE6
m68k_03fee6:
        lea.l 0x8003:w,%a0
m68k_03fee6_end:
.org 0x3FEEA
m68k_03feea:
        bsr.w (. + 132)
m68k_03feea_end:
.org 0x3FEEE
m68k_03feee:
        move.w #0xe,%d1
m68k_03feee_end:
.org 0x3FEF2
m68k_03fef2:
        moveq #0,%d0
m68k_03fef2_end:
.org 0x3FEF4
m68k_03fef4:
        lea.l 0x817a:w,%a6
m68k_03fef4_end:
.org 0x3FEF8
m68k_03fef8:
        btst.b #0x7,(%a6)
m68k_03fef8_end:
.org 0x3FEFC
m68k_03fefc:
        beq.b (. + 6)
m68k_03fefc_end:
.org 0x3FEFE
m68k_03fefe:
        add.w 0xe(%a6),%d0
m68k_03fefe_end:
.org 0x3FF02
m68k_03ff02:
        adda.w #0x10,%a6
m68k_03ff02_end:
.org 0x3FF06
m68k_03ff06:
        dbra %d1,(. + -14)
m68k_03ff06_end:
.org 0x3FF0A
m68k_03ff0a:
        bsr.w (. + -19506)
m68k_03ff0a_end:
.org 0x3FF0E
m68k_03ff0e:
        move.w #0xca1c,%d0
m68k_03ff0e_end:
.org 0x3FF12
m68k_03ff12:
        moveq #4,%d3
m68k_03ff12_end:
.org 0x3FF14
m68k_03ff14:
        lea.l 0x8001:w,%a0
m68k_03ff14_end:
.org 0x3FF18
m68k_03ff18:
        bsr.w (. + 86)
m68k_03ff18_end:
.org 0x3FF1C
m68k_03ff1c:
        move.w #0xe,%d1
m68k_03ff1c_end:
.org 0x3FF20
m68k_03ff20:
        moveq #0,%d0
m68k_03ff20_end:
.org 0x3FF22
m68k_03ff22:
        lea.l 0x827a:w,%a6
m68k_03ff22_end:
.org 0x3FF26
m68k_03ff26:
        btst.b #0x7,(%a6)
m68k_03ff26_end:
.org 0x3FF2A
m68k_03ff2a:
        beq.b (. + 6)
m68k_03ff2a_end:
.org 0x3FF2C
m68k_03ff2c:
        add.w 0xe(%a6),%d0
m68k_03ff2c_end:
.org 0x3FF30
m68k_03ff30:
        adda.w #0x10,%a6
m68k_03ff30_end:
.org 0x3FF34
m68k_03ff34:
        dbra %d1,(. + -14)
m68k_03ff34_end:
.org 0x3FF38
m68k_03ff38:
        bsr.w (. + -19552)
m68k_03ff38_end:
.org 0x3FF3C
m68k_03ff3c:
        move.w #0xca2e,%d0
m68k_03ff3c_end:
.org 0x3FF40
m68k_03ff40:
        moveq #4,%d3
m68k_03ff40_end:
.org 0x3FF42
m68k_03ff42:
        lea.l 0x8001:w,%a0
m68k_03ff42_end:
.org 0x3FF46
m68k_03ff46:
        bra.w (. + 40)
m68k_03ff46_end:
.org 0x3FF4A
m68k_03ff4a:
        btst.b #0x4,0xf321:w
m68k_03ff4a_end:
.org 0x3FF50
m68k_03ff50:
        bne.b (. + 30)
m68k_03ff50_end:
.org 0x3FF52
m68k_03ff52:
        move.w #0x8f02,0xc00004:l
m68k_03ff52_end:
.org 0x3FF5A
m68k_03ff5a:
        bsr.w (. + -19626)
m68k_03ff5a_end:
.org 0x3FF5E
m68k_03ff5e:
        move.w #0xc448,%d1
m68k_03ff5e_end:
.org 0x3FF62
m68k_03ff62:
        move.w %d1,0xc00000:l
m68k_03ff62_end:
.org 0x3FF68
m68k_03ff68:
        dbra %d3,(. + -10)
m68k_03ff68_end:
.org 0x3FF6C
m68k_03ff6c:
        rts
m68k_03ff6c_end:
.org 0x3FF6E
m68k_03ff6e:
        move.w #0x8f02,0xc00004:l
m68k_03ff6e_end:
.org 0x3FF76
m68k_03ff76:
        bsr.w (. + -19654)
m68k_03ff76_end:
.org 0x3FF7A
m68k_03ff7a:
        moveq #0,%d2
m68k_03ff7a_end:
.org 0x3FF7C
m68k_03ff7c:
        moveq #0,%d1
m68k_03ff7c_end:
.org 0x3FF7E
m68k_03ff7e:
        move.b (%a0)+,%d1
m68k_03ff7e_end:
.org 0x3FF80
m68k_03ff80:
        bne.b (. + 20)
m68k_03ff80_end:
.org 0x3FF82
m68k_03ff82:
        tst.w %d2
m68k_03ff82_end:
.org 0x3FF84
m68k_03ff84:
        bne.w (. + 16)
m68k_03ff84_end:
.org 0x3FF88
m68k_03ff88:
        tst.w %d3
m68k_03ff88_end:
.org 0x3FF8A
m68k_03ff8a:
        beq.w (. + 10)
m68k_03ff8a_end:
.org 0x3FF8E
m68k_03ff8e:
        move.w #0xc448,%d1
m68k_03ff8e_end:
.org 0x3FF92
m68k_03ff92:
        bra.b (. + 8)
m68k_03ff92_end:
.org 0x3FF94
m68k_03ff94:
        moveq #1,%d2
m68k_03ff94_end:
.org 0x3FF96
m68k_03ff96:
        addi.w #0xc460,%d1
m68k_03ff96_end:
.org 0x3FF9A
m68k_03ff9a:
        move.w %d1,0xc00000:l
m68k_03ff9a_end:
.org 0x3FFA0
m68k_03ffa0:
        dbra %d3,(. + -36)
m68k_03ffa0_end:
.org 0x3FFA4
m68k_03ffa4:
        rts
m68k_03ffa4_end:
.org 0x40F88
m68k_040f88:
        bra.w (. + -466)
m68k_040f88_end:
.org 0x40F8C
m68k_040f8c:
        bra.w (. + -346)
m68k_040f8c_end:
.org 0x40F90
m68k_040f90:
        bra.w (. + -260)
m68k_040f90_end:
.org 0x40F94
m68k_040f94:
        bra.w (. + -174)
m68k_040f94_end:
.org 0x41BAC
m68k_041bac:
        cmpi.b #0x1,0x80da:w
m68k_041bac_end:
.org 0x41BB2
m68k_041bb2:
        beq.b (. + 48)
m68k_041bb2_end:
.org 0x41BB4
m68k_041bb4:
        cmpi.b #0x2,0x80da:w
m68k_041bb4_end:
.org 0x41BBA
m68k_041bba:
        beq.b (. + 40)
m68k_041bba_end:
.org 0x41BBC
m68k_041bbc:
        tst.b 0x814c:w
m68k_041bbc_end:
.org 0x41BC0
m68k_041bc0:
        bne.b (. + 34)
m68k_041bc0_end:
.org 0x41BC2
m68k_041bc2:
        cmpi.w #0x6,0x812a:w
m68k_041bc2_end:
.org 0x41BC8
m68k_041bc8:
        beq.b (. + 26)
m68k_041bc8_end:
.org 0x41BCA
m68k_041bca:
        jsr 24(%pc)
m68k_041bca_end:
.org 0x41BCE
m68k_041bce:
        nop
m68k_041bce_end:
.org 0x41BD0
m68k_041bd0:
        jsr 260(%pc)
m68k_041bd0_end:
.org 0x41BD4
m68k_041bd4:
        nop
m68k_041bd4_end:
.org 0x41BD6
m68k_041bd6:
        jsr 882(%pc)
m68k_041bd6_end:
.org 0x41BDA
m68k_041bda:
        nop
m68k_041bda_end:
.org 0x41BDC
m68k_041bdc:
        jsr 482(%pc)
m68k_041bdc_end:
.org 0x41BE0
m68k_041be0:
        nop
m68k_041be0_end:
.org 0x41BE2
m68k_041be2:
        rts
m68k_041be2_end:
.org 0x41BE4
m68k_041be4:
        move.w 0x814a:w,%d0
m68k_041be4_end:
.org 0x41BE8
m68k_041be8:
        asl.w #0x2,%d0
m68k_041be8_end:
.org 0x41BEA
m68k_041bea:
        jmp 2(%pc, %d0.w)
m68k_041bea_end:
.org 0x41CD6
m68k_041cd6:
        cmpi.w #0x6,0x8130:w
m68k_041cd6_end:
.org 0x41CDC
m68k_041cdc:
        beq.w (. + 96)
m68k_041cdc_end:
.org 0x41CE0
m68k_041ce0:
        move.w 0x814a:w,%d0
m68k_041ce0_end:
.org 0x41CE4
m68k_041ce4:
        asl.w #0x2,%d0
m68k_041ce4_end:
.org 0x41CE6
m68k_041ce6:
        jmp 2(%pc, %d0.w)
m68k_041ce6_end:
.org 0x41D3C
m68k_041d3c:
        rts
m68k_041d3c_end:
.org 0x41D7A
m68k_041d7a:
        rts
m68k_041d7a_end:
.org 0x41DC0
m68k_041dc0:
        cmpi.w #0xb,0x8160:w
m68k_041dc0_end:
.org 0x41DC6
m68k_041dc6:
        bcs.b (. + -76)
m68k_041dc6_end:
.org 0x41DC8
m68k_041dc8:
        bsr.w (. + 22)
m68k_041dc8_end:
.org 0x41DCC
m68k_041dcc:
        bsr.w (. + 82)
m68k_041dcc_end:
.org 0x41DD0
m68k_041dd0:
        bsr.w (. + 124)
m68k_041dd0_end:
.org 0x41DD4
m68k_041dd4:
        bsr.w (. + 162)
m68k_041dd4_end:
.org 0x41DD8
m68k_041dd8:
        bsr.w (. + 222)
m68k_041dd8_end:
.org 0x41DDC
m68k_041ddc:
        rts
m68k_041ddc_end:
.org 0x41DDE
m68k_041dde:
        bsr.w (. + 298)
m68k_041dde_end:
.org 0x41DE2
m68k_041de2:
        move.w %d1,%d3
m68k_041de2_end:
.org 0x41DE4
m68k_041de4:
        asl.w #0x1,%d3
m68k_041de4_end:
.org 0x41DE6
m68k_041de6:
        cmp.w %d3,%d2
m68k_041de6_end:
.org 0x41DE8
m68k_041de8:
        bls.b (. + 52)
m68k_041de8_end:
.org 0x41DEA
m68k_041dea:
        cmpi.w #0x3e8,%d1
m68k_041dea_end:
.org 0x41DEE
m68k_041dee:
        bhi.b (. + 46)
m68k_041dee_end:
.org 0x41DF0
m68k_041df0:
        jsr -26320(%pc)
m68k_041df0_end:
.org 0x41DF4
m68k_041df4:
        move.w 0xefd2:w,%d1
m68k_041df4_end:
.org 0x41DF8
m68k_041df8:
        lea.l 250(%pc),%a0
m68k_041df8_end:
.org 0x41DFC
m68k_041dfc:
        nop
m68k_041dfc_end:
.org 0x41DFE
m68k_041dfe:
        and.b (%a0, %d1.w),%d0
m68k_041dfe_end:
.org 0x41E02
m68k_041e02:
        bne.b (. + 26)
m68k_041e02_end:
.org 0x41E04
m68k_041e04:
        move.w #0x6,0x812a:w
m68k_041e04_end:
.org 0x41E0A
m68k_041e0a:
        move.w #0x6,0x812c:w
m68k_041e0a_end:
.org 0x41E10
m68k_041e10:
        move.w #0x6,0x812e:w
m68k_041e10_end:
.org 0x41E16
m68k_041e16:
        move.w #0x6,0x8130:w
m68k_041e16_end:
.org 0x41E1C
m68k_041e1c:
        rts
m68k_041e1c_end:
.org 0x41E1E
m68k_041e1e:
        bsr.w (. + 234)
m68k_041e1e_end:
.org 0x41E22
m68k_041e22:
        move.w %d1,%d3
m68k_041e22_end:
.org 0x41E24
m68k_041e24:
        asl.w #0x1,%d3
m68k_041e24_end:
.org 0x41E26
m68k_041e26:
        cmp.w %d3,%d2
m68k_041e26_end:
.org 0x41E28
m68k_041e28:
        bls.w (. + -12)
m68k_041e28_end:
.org 0x41E2C
m68k_041e2c:
        cmpi.w #0x1f4,%d1
m68k_041e2c_end:
.org 0x41E30
m68k_041e30:
        bhi.w (. + -20)
m68k_041e30_end:
.org 0x41E34
m68k_041e34:
        jsr -26388(%pc)
m68k_041e34_end:
.org 0x41E38
m68k_041e38:
        move.w 0xefd2:w,%d1
m68k_041e38_end:
.org 0x41E3C
m68k_041e3c:
        lea.l 186(%pc),%a0
m68k_041e3c_end:
.org 0x41E40
m68k_041e40:
        nop
m68k_041e40_end:
.org 0x41E42
m68k_041e42:
        and.b (%a0, %d1.w),%d0
m68k_041e42_end:
.org 0x41E46
m68k_041e46:
        beq.w (. + -66)
m68k_041e46_end:
.org 0x41E4A
m68k_041e4a:
        rts
m68k_041e4a_end:
.org 0x41E4C
m68k_041e4c:
        bsr.w (. + 188)
m68k_041e4c_end:
.org 0x41E50
m68k_041e50:
        asl.w #0x1,%d3
m68k_041e50_end:
.org 0x41E52
m68k_041e52:
        cmp.w %d3,%d4
m68k_041e52_end:
.org 0x41E54
m68k_041e54:
        bls.w (. + -56)
m68k_041e54_end:
.org 0x41E58
m68k_041e58:
        cmp.w %d1,%d2
m68k_041e58_end:
.org 0x41E5A
m68k_041e5a:
        bls.w (. + -62)
m68k_041e5a_end:
.org 0x41E5E
m68k_041e5e:
        jsr -26430(%pc)
m68k_041e5e_end:
.org 0x41E62
m68k_041e62:
        move.w 0xefd2:w,%d1
m68k_041e62_end:
.org 0x41E66
m68k_041e66:
        lea.l 148(%pc),%a0
m68k_041e66_end:
.org 0x41E6A
m68k_041e6a:
        nop
m68k_041e6a_end:
.org 0x41E6C
m68k_041e6c:
        and.b (%a0, %d1.w),%d0
m68k_041e6c_end:
.org 0x41E70
m68k_041e70:
        beq.w (. + -108)
m68k_041e70_end:
.org 0x41E74
m68k_041e74:
        rts
m68k_041e74_end:
.org 0x41E76
m68k_041e76:
        bsr.w (. + 146)
m68k_041e76_end:
.org 0x41E7A
m68k_041e7a:
        cmp.w %d1,%d2
m68k_041e7a_end:
.org 0x41E7C
m68k_041e7c:
        bls.w (. + -96)
m68k_041e7c_end:
.org 0x41E80
m68k_041e80:
        cmpi.w #0x1e,0x8178:w
m68k_041e80_end:
.org 0x41E86
m68k_041e86:
        bcc.w (. + -106)
m68k_041e86_end:
.org 0x41E8A
m68k_041e8a:
        jsr -26474(%pc)
m68k_041e8a_end:
.org 0x41E8E
m68k_041e8e:
        move.w 0xefd2:w,%d1
m68k_041e8e_end:
.org 0x41E92
m68k_041e92:
        cmpi.w #0x2,%d1
m68k_041e92_end:
.org 0x41E96
m68k_041e96:
        bne.b (. + 16)
m68k_041e96_end:
.org 0x41E98
m68k_041e98:
        andi.w #0x7,%d0
m68k_041e98_end:
.org 0x41E9C
m68k_041e9c:
        cmpi.w #0x5,%d0
m68k_041e9c_end:
.org 0x41EA0
m68k_041ea0:
        bcs.w (. + -156)
m68k_041ea0_end:
.org 0x41EA4
m68k_041ea4:
        rts
m68k_041ea4_end:
.org 0x41EA6
m68k_041ea6:
        lea.l 88(%pc),%a0
m68k_041ea6_end:
.org 0x41EAA
m68k_041eaa:
        nop
m68k_041eaa_end:
.org 0x41EAC
m68k_041eac:
        and.b (%a0, %d1.w),%d0
m68k_041eac_end:
.org 0x41EB0
m68k_041eb0:
        beq.w (. + -172)
m68k_041eb0_end:
.org 0x41EB4
m68k_041eb4:
        rts
m68k_041eb4_end:
.org 0x41EB6
m68k_041eb6:
        bsr.w (. + 82)
m68k_041eb6_end:
.org 0x41EBA
m68k_041eba:
        move.w 0x8104:w,%d0
m68k_041eba_end:
.org 0x41EBE
m68k_041ebe:
        cmp.w 0x8106:w,%d0
m68k_041ebe_end:
.org 0x41EC2
m68k_041ec2:
        bcc.w (. + -166)
m68k_041ec2_end:
.org 0x41EC6
m68k_041ec6:
        move.w 0x8178:w,%d0
m68k_041ec6_end:
.org 0x41ECA
m68k_041eca:
        cmp.w 0x8278:w,%d0
m68k_041eca_end:
.org 0x41ECE
m68k_041ece:
        bcc.w (. + -178)
m68k_041ece_end:
.org 0x41ED2
m68k_041ed2:
        cmpi.w #0x1e,0x8178:w
m68k_041ed2_end:
.org 0x41ED8
m68k_041ed8:
        bcc.w (. + -188)
m68k_041ed8_end:
.org 0x41EDC
m68k_041edc:
        jsr -26556(%pc)
m68k_041edc_end:
.org 0x41EE0
m68k_041ee0:
        move.w 0xefd2:w,%d1
m68k_041ee0_end:
.org 0x41EE4
m68k_041ee4:
        lea.l 30(%pc),%a0
m68k_041ee4_end:
.org 0x41EE8
m68k_041ee8:
        nop
m68k_041ee8_end:
.org 0x41EEA
m68k_041eea:
        and.b (%a0, %d1.w),%d0
m68k_041eea_end:
.org 0x41EEE
m68k_041eee:
        beq.w (. + -234)
m68k_041eee_end:
.org 0x41EF2
m68k_041ef2:
        rts
m68k_041ef2_end:
.org 0x41F4A
m68k_041f4a:
        move.w 0x80dc:w,%d0
m68k_041f4a_end:
.org 0x41F4E
m68k_041f4e:
        cmp.w 0x80e0:w,%d0
m68k_041f4e_end:
.org 0x41F52
m68k_041f52:
        beq.w (. + 152)
m68k_041f52_end:
.org 0x41F56
m68k_041f56:
        bsr.w (. + -78)
m68k_041f56_end:
.org 0x41F5A
m68k_041f5a:
        cmp.w %d1,%d2
m68k_041f5a_end:
.org 0x41F5C
m68k_041f5c:
        bls.w (. + 142)
m68k_041f5c_end:
.org 0x41F60
m68k_041f60:
        move.w 0xefd2:w,%d0
m68k_041f60_end:
.org 0x41F64
m68k_041f64:
        lea.l 134(%pc),%a0
m68k_041f64_end:
.org 0x41F68
m68k_041f68:
        nop
m68k_041f68_end:
.org 0x41F6A
m68k_041f6a:
        move.w 0x8178:w,%d1
m68k_041f6a_end:
.org 0x41F6E
m68k_041f6e:
        cmp.b (%a0, %d0.w),%d1
m68k_041f6e_end:
.org 0x41F72
m68k_041f72:
        bcc.w (. + 120)
m68k_041f72_end:
.org 0x41F76
m68k_041f76:
        move.w 0x8178:w,%d0
m68k_041f76_end:
.org 0x41F7A
m68k_041f7a:
        cmp.w 0x8278:w,%d0
m68k_041f7a_end:
.org 0x41F7E
m68k_041f7e:
        bcc.w (. + 108)
m68k_041f7e_end:
.org 0x41F82
m68k_041f82:
        lea.l 0x816a:w,%a6
m68k_041f82_end:
.org 0x41F86
m68k_041f86:
        move.w #0x8010,%d0
m68k_041f86_end:
.org 0x41F8A
m68k_041f8a:
        move.w #0x0,%d1
m68k_041f8a_end:
.org 0x41F8E
m68k_041f8e:
        bsr.w (. + -2708)
m68k_041f8e_end:
.org 0x41F92
m68k_041f92:
        tst.w %d0
m68k_041f92_end:
.org 0x41F94
m68k_041f94:
        bne.w (. + 58)
m68k_041f94_end:
.org 0x41F98
m68k_041f98:
        move.w #0x10,%d0
m68k_041f98_end:
.org 0x41F9C
m68k_041f9c:
        move.w #0x0,%d1
m68k_041f9c_end:
.org 0x41FA0
m68k_041fa0:
        bsr.w (. + -2726)
m68k_041fa0_end:
.org 0x41FA4
m68k_041fa4:
        tst.w %d0
m68k_041fa4_end:
.org 0x41FA6
m68k_041fa6:
        bne.w (. + 40)
m68k_041fa6_end:
.org 0x41FAA
m68k_041faa:
        move.w #0x8010,%d0
m68k_041faa_end:
.org 0x41FAE
m68k_041fae:
        move.w #0x8010,%d1
m68k_041fae_end:
.org 0x41FB2
m68k_041fb2:
        bsr.w (. + -2744)
m68k_041fb2_end:
.org 0x41FB6
m68k_041fb6:
        tst.w %d0
m68k_041fb6_end:
.org 0x41FB8
m68k_041fb8:
        bne.w (. + 22)
m68k_041fb8_end:
.org 0x41FBC
m68k_041fbc:
        move.w #0x10,%d0
m68k_041fbc_end:
.org 0x41FC0
m68k_041fc0:
        move.w #0x8010,%d1
m68k_041fc0_end:
.org 0x41FC4
m68k_041fc4:
        bsr.w (. + -2762)
m68k_041fc4_end:
.org 0x41FC8
m68k_041fc8:
        tst.w %d0
m68k_041fc8_end:
.org 0x41FCA
m68k_041fca:
        beq.w (. + 32)
m68k_041fca_end:
.org 0x41FCE
m68k_041fce:
        jsr -26798(%pc)
m68k_041fce_end:
.org 0x41FD2
m68k_041fd2:
        andi.w #0x3,%d0
m68k_041fd2_end:
.org 0x41FD6
m68k_041fd6:
        beq.b (. + 20)
m68k_041fd6_end:
.org 0x41FD8
m68k_041fd8:
        move.w #0x6,0x813a:w
m68k_041fd8_end:
.org 0x41FDE
m68k_041fde:
        move.w #0x0,0x813c:w
m68k_041fde_end:
.org 0x41FE4
m68k_041fe4:
        move.w #0x1,0x813e:w
m68k_041fe4_end:
.org 0x41FEA
m68k_041fea:
        rts
m68k_041fea_end:
.org 0x66C28
m68k_066c28:
        addq.w #0x1,0xf362:w
m68k_066c28_end:
.org 0x66C2C
m68k_066c2c:
        move.w 0xefb0:w,%d0
m68k_066c2c_end:
.org 0x66C30
m68k_066c30:
        lsl.w #0x1,%d0
m68k_066c30_end:
.org 0x66C32
m68k_066c32:
        lea.l 0xe640:w,%a0
m68k_066c32_end:
.org 0x66C36
m68k_066c36:
        move.w (%a0, %d0.w),%d0
m68k_066c36_end:
.org 0x66C3A
m68k_066c3a:
        move.w %d0,0xf3d0:w
m68k_066c3a_end:
.org 0x66C3E
m68k_066c3e:
        move.w %d0,0xf3a6:w
m68k_066c3e_end:
.org 0x66C42
m68k_066c42:
        move.w 0xefb0:w,0xf376:w
m68k_066c42_end:
.org 0x66C48
m68k_066c48:
        move.w #0x98,%d0
m68k_066c48_end:
.org 0x66C4C
m68k_066c4c:
        jsr 0x676f2:l
m68k_066c4c_end:
.org 0x66C52
m68k_066c52:
        rts
m68k_066c52_end:
.org 0x66C54
m68k_066c54:
        btst.b #0x5,0xf603:w
m68k_066c54_end:
.org 0x66C5A
m68k_066c5a:
        beq.w (. + 118)
m68k_066c5a_end:
.org 0x66C5E
m68k_066c5e:
        move.w 0xefb0:w,%d0
m68k_066c5e_end:
.org 0x66C62
m68k_066c62:
        cmp.w 0xf67a:w,%d0
m68k_066c62_end:
.org 0x66C66
m68k_066c66:
        beq.w (. + 30)
m68k_066c66_end:
.org 0x66C6A
m68k_066c6a:
        cmp.w 0xf67c:w,%d0
m68k_066c6a_end:
.org 0x66C6E
m68k_066c6e:
        beq.w (. + 22)
m68k_066c6e_end:
.org 0x66C72
m68k_066c72:
        cmp.w 0xf67e:w,%d0
m68k_066c72_end:
.org 0x66C76
m68k_066c76:
        beq.w (. + 14)
m68k_066c76_end:
.org 0x66C7A
m68k_066c7a:
        move.w #0x4,0xf362:w
m68k_066c7a_end:
.org 0x66C80
m68k_066c80:
        bra.w (. + 80)
m68k_066c80_end:
.org 0x66C84
m68k_066c84:
        move.w 0xefb0:w,%d0
m68k_066c84_end:
.org 0x66C88
m68k_066c88:
        lea.l 0xf590:w,%a0
m68k_066c88_end:
.org 0x66C8C
m68k_066c8c:
        addq.b #0x1,(%a0, %d0.w)
m68k_066c8c_end:
.org 0x66C90
m68k_066c90:
        cmpi.b #0x3,(%a0, %d0.w)
m68k_066c90_end:
.org 0x66C96
m68k_066c96:
        bhi.w (. + 18)
m68k_066c96_end:
.org 0x66C9A
m68k_066c9a:
        addq.w #0x1,0xf362:w
m68k_066c9a_end:
.org 0x66C9E
m68k_066c9e:
        move.w #0xcc,0xf600:w
m68k_066c9e_end:
.org 0x66CA4
m68k_066ca4:
        bra.w (. + 44)
m68k_066ca4_end:
.org 0x66CA8
m68k_066ca8:
        bsr.w (. + 42)
m68k_066ca8_end:
.org 0x66CAC
m68k_066cac:
        bcs.w (. + 14)
m68k_066cac_end:
.org 0x66CB0
m68k_066cb0:
        move.w #0x7,0xf362:w
m68k_066cb0_end:
.org 0x66CB6
m68k_066cb6:
        bra.w (. + 26)
m68k_066cb6_end:
.org 0x66CBA
m68k_066cba:
        move.w #0x12c,0xf608:w
m68k_066cba_end:
.org 0x66CC0
m68k_066cc0:
        move.w #0xb,0xf362:w
m68k_066cc0_end:
.org 0x66CC6
m68k_066cc6:
        move.w #0x98,%d0
m68k_066cc6_end:
.org 0x66CCA
m68k_066cca:
        jsr 0x676f2:l
m68k_066cca_end:
.org 0x66CD0
m68k_066cd0:
        rts
m68k_066cd0_end:
.org 0x66CD2
m68k_066cd2:
        move.w 0xefb0:w,%d0
m68k_066cd2_end:
.org 0x66CD6
m68k_066cd6:
        cmp.w 0xf67a:w,%d0
m68k_066cd6_end:
.org 0x66CDA
m68k_066cda:
        bne.w (. + 14)
m68k_066cda_end:
.org 0x66CDE
m68k_066cde:
        move.w #0x80,0xf67a:w
m68k_066cde_end:
.org 0x66CE4
m68k_066ce4:
        bra.w (. + 36)
m68k_066ce4_end:
.org 0x66CE8
m68k_066ce8:
        cmp.w 0xf67c:w,%d0
m68k_066ce8_end:
.org 0x66CEC
m68k_066cec:
        bne.w (. + 14)
m68k_066cec_end:
.org 0x66CF0
m68k_066cf0:
        move.w #0x80,0xf67c:w
m68k_066cf0_end:
.org 0x66CF6
m68k_066cf6:
        bra.w (. + 18)
m68k_066cf6_end:
.org 0x66CFA
m68k_066cfa:
        cmp.w 0xf67e:w,%d0
m68k_066cfa_end:
.org 0x66CFE
m68k_066cfe:
        bne.w (. + 10)
m68k_066cfe_end:
.org 0x66D02
m68k_066d02:
        move.w #0x80,0xf67e:w
m68k_066d02_end:
.org 0x66D08
m68k_066d08:
        tst.b 0xf67b:w
m68k_066d08_end:
.org 0x66D0C
m68k_066d0c:
        bpl.w (. + 28)
m68k_066d0c_end:
.org 0x66D10
m68k_066d10:
        tst.b 0xf67d:w
m68k_066d10_end:
.org 0x66D14
m68k_066d14:
        bpl.w (. + 20)
m68k_066d14_end:
.org 0x66D18
m68k_066d18:
        tst.b 0xf67f:w
m68k_066d18_end:
.org 0x66D1C
m68k_066d1c:
        bpl.w (. + 12)
m68k_066d1c_end:
.org 0x66D20
m68k_066d20:
        andi.w #0xfffe,%sr
m68k_066d20_end:
.org 0x66D24
m68k_066d24:
        bra.w (. + 8)
m68k_066d24_end:
.org 0x66D28
m68k_066d28:
        ori.w #0x1,%sr
m68k_066d28_end:
.org 0x66D2C
m68k_066d2c:
        rts
m68k_066d2c_end:
.org 0x66D2E
m68k_066d2e:
        tst.w 0xf636:w
m68k_066d2e_end:
.org 0x66D32
m68k_066d32:
        bne.w (. + 30)
m68k_066d32_end:
.org 0x66D36
m68k_066d36:
        bsr.b (. + -100)
m68k_066d36_end:
.org 0x66D38
m68k_066d38:
        bcs.w (. + 14)
m68k_066d38_end:
.org 0x66D3C
m68k_066d3c:
        move.w #0x7,0xf362:w
m68k_066d3c_end:
.org 0x66D42
m68k_066d42:
        bra.w (. + 18)
m68k_066d42_end:
.org 0x66D46
m68k_066d46:
        move.w #0x6,0xf362:w
m68k_066d46_end:
.org 0x66D4C
m68k_066d4c:
        bra.w (. + 8)
m68k_066d4c_end:
.org 0x66D50
m68k_066d50:
        addq.w #0x1,0xf362:w
m68k_066d50_end:
.org 0x66D54
m68k_066d54:
        rts
m68k_066d54_end:
.org 0x66D56
m68k_066d56:
        move.w #0x80,0xf38c:w
m68k_066d56_end:
.org 0x66D5C
m68k_066d5c:
        move.w #0x208,0xf612:w
m68k_066d5c_end:
.org 0x66D62
m68k_066d62:
        move.w #0x4,0xf362:w
m68k_066d62_end:
.org 0x66D68
m68k_066d68:
        clr.w 0xf386:w
m68k_066d68_end:
.org 0x66D6C
m68k_066d6c:
        clr.w 0xf388:w
m68k_066d6c_end:
.org 0x66D70
m68k_066d70:
        move.w #0x11,0xf65a:w
m68k_066d70_end:
.org 0x66D76
m68k_066d76:
        rts
m68k_066d76_end:
.org 0x66D78
m68k_066d78:
        lea.l 0xf590:w,%a0
m68k_066d78_end:
.org 0x66D7C
m68k_066d7c:
        move.w 0xefb0:w,%d0
m68k_066d7c_end:
.org 0x66D80
m68k_066d80:
        addq.b #0x1,(%a0, %d0.w)
m68k_066d80_end:
.org 0x66D84
m68k_066d84:
        cmpi.b #0x3,(%a0, %d0.w)
m68k_066d84_end:
.org 0x66D8A
m68k_066d8a:
        bcc.w (. + 54)
m68k_066d8a_end:
.org 0x66D8E
m68k_066d8e:
        bsr.w (. + 56)
m68k_066d8e_end:
.org 0x66D92
m68k_066d92:
        tst.w %d2
m68k_066d92_end:
.org 0x66D94
m68k_066d94:
        bmi.w (. + 44)
m68k_066d94_end:
.org 0x66D98
m68k_066d98:
        bsr.w (. + 164)
m68k_066d98_end:
.org 0x66D9C
m68k_066d9c:
        move.w %d2,0xf3d2:w
m68k_066d9c_end:
.org 0x66DA0
m68k_066da0:
        move.w 0xf3a6:w,0xf3d0:w
m68k_066da0_end:
.org 0x66DA6
m68k_066da6:
        move.w #0xa4,%d0
m68k_066da6_end:
.org 0x66DAA
m68k_066daa:
        move.w #0x9,0xf362:w
m68k_066daa_end:
.org 0x66DB0
m68k_066db0:
        move.w #0x12c,0xf608:w
m68k_066db0_end:
.org 0x66DB6
m68k_066db6:
        jsr 0x676f2:l
m68k_066db6_end:
.org 0x66DBC
m68k_066dbc:
        bra.w (. + 8)
m68k_066dbc_end:
.org 0x66DC0
m68k_066dc0:
        addq.w #0x1,0xf362:w
m68k_066dc0_end:
.org 0x66DC4
m68k_066dc4:
        rts
m68k_066dc4_end:
.org 0x66DC6
m68k_066dc6:
        move.w 0xefb0:w,%d0
m68k_066dc6_end:
.org 0x66DCA
m68k_066dca:
        clr.w %d1
m68k_066dca_end:
.org 0x66DCC
m68k_066dcc:
        move.w #0x2,%d4
m68k_066dcc_end:
.org 0x66DD0
m68k_066dd0:
        move.w #0xffff,%d2
m68k_066dd0_end:
.org 0x66DD4
m68k_066dd4:
        lea.l 0xf427:w,%a0
m68k_066dd4_end:
.org 0x66DD8
m68k_066dd8:
        lea.l 0xcc00:w,%a1
m68k_066dd8_end:
.org 0x66DDC
m68k_066ddc:
        lea.l 0xc700:w,%a2
m68k_066ddc_end:
.org 0x66DE0
m68k_066de0:
        lea.l 0xc300:w,%a3
m68k_066de0_end:
.org 0x66DE4
m68k_066de4:
        move.w #0xff,%d3
m68k_066de4_end:
.org 0x66DE8
m68k_066de8:
        move.b (%a1, %d3.w),%d5
m68k_066de8_end:
.org 0x66DEC
m68k_066dec:
        beq.w (. + 74)
m68k_066dec_end:
.org 0x66DF0
m68k_066df0:
        bmi.w (. + 70)
m68k_066df0_end:
.org 0x66DF4
m68k_066df4:
        andi.w #0x3f,%d5
m68k_066df4_end:
.org 0x66DF8
m68k_066df8:
        cmp.b (%a0, %d5.w),%d0
m68k_066df8_end:
.org 0x66DFC
m68k_066dfc:
        bne.w (. + 58)
m68k_066dfc_end:
.org 0x66E00
m68k_066e00:
        move.w #0x5,%d6
m68k_066e00_end:
.org 0x66E04
m68k_066e04:
        move.b (%a3, %d3.w),%d7
m68k_066e04_end:
.org 0x66E08
m68k_066e08:
        cmpi.b #0x5a,%d7
m68k_066e08_end:
.org 0x66E0C
m68k_066e0c:
        bcc.w (. + 30)
m68k_066e0c_end:
.org 0x66E10
m68k_066e10:
        cmpi.b #0x50,%d7
m68k_066e10_end:
.org 0x66E14
m68k_066e14:
        bcs.w (. + 34)
m68k_066e14_end:
.org 0x66E18
m68k_066e18:
        move.b (%a2, %d3.w),%d6
m68k_066e18_end:
.org 0x66E1C
m68k_066e1c:
        andi.w #0x7,%d6
m68k_066e1c_end:
.org 0x66E20
m68k_066e20:
        cmp.w %d4,%d6
m68k_066e20_end:
.org 0x66E22
m68k_066e22:
        bcs.w (. + 20)
m68k_066e22_end:
.org 0x66E26
m68k_066e26:
        bhi.w (. + 10)
m68k_066e26_end:
.org 0x66E2A
m68k_066e2a:
        cmp.b %d1,%d7
m68k_066e2a_end:
.org 0x66E2C
m68k_066e2c:
        bls.w (. + 10)
m68k_066e2c_end:
.org 0x66E30
m68k_066e30:
        move.b %d7,%d1
m68k_066e30_end:
.org 0x66E32
m68k_066e32:
        move.w %d6,%d4
m68k_066e32_end:
.org 0x66E34
m68k_066e34:
        move.w %d3,%d2
m68k_066e34_end:
.org 0x66E36
m68k_066e36:
        dbra %d3,(. + -78)
m68k_066e36_end:
.org 0x66E3A
m68k_066e3a:
        rts
m68k_066e3a_end:
.org 0x66E3C
m68k_066e3c:
        lea.l 0xe640:w,%a0
m68k_066e3c_end:
.org 0x66E40
m68k_066e40:
        move.w 0xefb0:w,%d0
m68k_066e40_end:
.org 0x66E44
m68k_066e44:
        lsl.w #0x1,%d0
m68k_066e44_end:
.org 0x66E46
m68k_066e46:
        move.w %d2,(%a0, %d0.w)
m68k_066e46_end:
.org 0x66E4A
m68k_066e4a:
        lea.l 0xf45e:w,%a0
m68k_066e4a_end:
.org 0x66E4E
m68k_066e4e:
        lea.l 0xcc00:w,%a1
m68k_066e4e_end:
.org 0x66E52
m68k_066e52:
        clr.w %d1
m68k_066e52_end:
.org 0x66E54
m68k_066e54:
        move.b (%a1, %d2.w),%d1
m68k_066e54_end:
.org 0x66E58
m68k_066e58:
        cmpi.w #0x29,%d1
m68k_066e58_end:
.org 0x66E5C
m68k_066e5c:
        bhi.w (. + 10)
m68k_066e5c_end:
.org 0x66E60
m68k_066e60:
        lsl.w #0x1,%d1
m68k_066e60_end:
.org 0x66E62
m68k_066e62:
        move.w %d2,(%a0, %d1.w)
m68k_066e62_end:
.org 0x66E66
m68k_066e66:
        lea.l 0xc300:w,%a0
m68k_066e66_end:
.org 0x66E6A
m68k_066e6a:
        move.b #0x64,(%a0, %d2.w)
m68k_066e6a_end:
.org 0x66E70
m68k_066e70:
        lea.l 0xc700:w,%a0
m68k_066e70_end:
.org 0x66E74
m68k_066e74:
        move.b #0x4,(%a0, %d2.w)
m68k_066e74_end:
.org 0x66E7A
m68k_066e7a:
        rts
m68k_066e7a_end:
.org 0x66E7C
m68k_066e7c:
        addq.w #0x1,0xf362:w
m68k_066e7c_end:
.org 0x66E80
m68k_066e80:
        move.w 0xf3a6:w,0xf3d0:w
m68k_066e80_end:
.org 0x66E86
m68k_066e86:
        move.w #0xa5,%d0
m68k_066e86_end:
.org 0x66E8A
m68k_066e8a:
        jsr 0x676f2:l
m68k_066e8a_end:
.org 0x66E90
m68k_066e90:
        rts
m68k_066e90_end:
.org 0x66E92
m68k_066e92:
        move.w #0xd0,0xf600:w
m68k_066e92_end:
.org 0x66E98
m68k_066e98:
        clr.w 0xf612:w
m68k_066e98_end:
.org 0x66E9C
m68k_066e9c:
        move.w #0x12c,0xf608:w
m68k_066e9c_end:
.org 0x66EA2
m68k_066ea2:
        move.w #0x9,0xf362:w
m68k_066ea2_end:
.org 0x66EA8
m68k_066ea8:
        rts
m68k_066ea8_end:
.org 0x66EAA
m68k_066eaa:
        move.w #0x1ff,%d0
m68k_066eaa_end:
.org 0x66EAE
m68k_066eae:
        lea.l 0xff7000:l,%a0
m68k_066eae_end:
.org 0x66EB4
m68k_066eb4:
        lea.l 0xff7800:l,%a1
m68k_066eb4_end:
.org 0x66EBA
m68k_066eba:
        lea.l 0x8000:w,%a2
m68k_066eba_end:
.org 0x66EBE
m68k_066ebe:
        lea.l 0x8800:w,%a3
m68k_066ebe_end:
.org 0x66EC2
m68k_066ec2:
        clr.l (%a0)+
m68k_066ec2_end:
.org 0x66EC4
m68k_066ec4:
        clr.l (%a1)+
m68k_066ec4_end:
.org 0x66EC6
m68k_066ec6:
        clr.l (%a2)+
m68k_066ec6_end:
.org 0x66EC8
m68k_066ec8:
        clr.l (%a3)+
m68k_066ec8_end:
.org 0x66ECA
m68k_066eca:
        dbra %d0,(. + -8)
m68k_066eca_end:
.org 0x66ECE
m68k_066ece:
        move.w #0x3,0xffff80da:l
m68k_066ece_end:
.org 0x66ED6
m68k_066ed6:
        lea.l 0xe640:w,%a0
m68k_066ed6_end:
.org 0x66EDA
m68k_066eda:
        move.w 0xefb0:w,%d0
m68k_066eda_end:
.org 0x66EDE
m68k_066ede:
        lsl.w #0x1,%d0
m68k_066ede_end:
.org 0x66EE0
m68k_066ee0:
        move.w (%a0, %d0.w),%d0
m68k_066ee0_end:
.org 0x66EE4
m68k_066ee4:
        move.w %d0,0xffff80dc:l
m68k_066ee4_end:
.org 0x66EEA
m68k_066eea:
        move.w %d0,0xffff80de:l
m68k_066eea_end:
.org 0x66EF0
m68k_066ef0:
        move.w 0xa622:w,%d0
m68k_066ef0_end:
.org 0x66EF4
m68k_066ef4:
        bmi.w (. + 44)
m68k_066ef4_end:
.org 0x66EF8
m68k_066ef8:
        move.w %d0,%d1
m68k_066ef8_end:
.org 0x66EFA
m68k_066efa:
        andi.w #0xff,%d0
m68k_066efa_end:
.org 0x66EFE
m68k_066efe:
        cmp.w 0xefb0:w,%d0
m68k_066efe_end:
.org 0x66F02
m68k_066f02:
        bne.w (. + 8)
m68k_066f02_end:
.org 0x66F06
m68k_066f06:
        lsr.w #0x8,%d1
m68k_066f06_end:
.org 0x66F08
m68k_066f08:
        move.w %d1,%d0
m68k_066f08_end:
.org 0x66F0A
m68k_066f0a:
        lsl.w #0x1,%d0
m68k_066f0a_end:
.org 0x66F0C
m68k_066f0c:
        move.w (%a0, %d0.w),%d0
m68k_066f0c_end:
.org 0x66F10
m68k_066f10:
        move.w %d0,0xffff80e0:l
m68k_066f10_end:
.org 0x66F16
m68k_066f16:
        move.w %d0,0xffff80e2:l
m68k_066f16_end:
.org 0x66F1C
m68k_066f1c:
        bra.w (. + 54)
m68k_066f1c_end:
.org 0x66F20
m68k_066f20:
        move.w #0x4,0xffff80da:l
m68k_066f20_end:
.org 0x66F28
m68k_066f28:
        lea.l 0xe640:w,%a0
m68k_066f28_end:
.org 0x66F2C
m68k_066f2c:
        move.w 0xefb0:w,%d0
m68k_066f2c_end:
.org 0x66F30
m68k_066f30:
        lsl.w #0x1,%d0
m68k_066f30_end:
.org 0x66F32
m68k_066f32:
        move.w (%a0, %d0.w),0xffff80dc:l
m68k_066f32_end:
.org 0x66F3A
m68k_066f3a:
        move.w (%a0, %d0.w),0xffff80de:l
m68k_066f3a_end:
.org 0x66F42
m68k_066f42:
        move.w (%a0, %d0.w),0xffff80e0:l
m68k_066f42_end:
.org 0x66F4A
m68k_066f4a:
        move.w (%a0, %d0.w),0xffff80e2:l
m68k_066f4a_end:
.org 0x66F52
m68k_066f52:
        clr.w %d0
m68k_066f52_end:
.org 0x66F54
m68k_066f54:
        move.b 0xf374:w,%d0
m68k_066f54_end:
.org 0x66F58
m68k_066f58:
        addi.w #0xb8,%d0
m68k_066f58_end:
.org 0x66F5C
m68k_066f5c:
        move.w %d0,0xffff80e4:l
m68k_066f5c_end:
.org 0x66F62
m68k_066f62:
        move.b 0xf375:w,%d0
m68k_066f62_end:
.org 0x66F66
m68k_066f66:
        addq.w #0x1,%d0
m68k_066f66_end:
.org 0x66F68
m68k_066f68:
        move.w %d0,0xffff80e6:l
m68k_066f68_end:
.org 0x66F6E
m68k_066f6e:
        addq.w #0x1,0xf362:w
m68k_066f6e_end:
.org 0x66F72
m68k_066f72:
        clr.w 0xf352:w
m68k_066f72_end:
.org 0x66F76
m68k_066f76:
        rts
m68k_066f76_end:
.org 0x66F78
m68k_066f78:
        cmpi.w #0x10,0xf352:w
m68k_066f78_end:
.org 0x66F7E
m68k_066f7e:
        bcs.w (. + 14)
m68k_066f7e_end:
.org 0x66F82
m68k_066f82:
        move.w #0xe0,0xf600:w
m68k_066f82_end:
.org 0x66F88
m68k_066f88:
        bra.w (. + 38)
m68k_066f88_end:
.org 0x66F8C
m68k_066f8c:
        move.w 0xf352:w,%d0
m68k_066f8c_end:
.org 0x66F90
m68k_066f90:
        move.w #0x40,%d1
m68k_066f90_end:
.org 0x66F94
m68k_066f94:
        lea.l 0xfb80:w,%a0
m68k_066f94_end:
.org 0x66F98
m68k_066f98:
        jsr 0xdea6:l
m68k_066f98_end:
.org 0x66F9E
m68k_066f9e:
        move.w 0xf320:w,%d0
m68k_066f9e_end:
.org 0x66FA2
m68k_066fa2:
        andi.w #0x1,%d0
m68k_066fa2_end:
.org 0x66FA6
m68k_066fa6:
        bne.w (. + 8)
m68k_066fa6_end:
.org 0x66FAA
m68k_066faa:
        addq.w #0x1,0xf352:w
m68k_066faa_end:
.org 0x66FAE
m68k_066fae:
        rts
m68k_066fae_end:
.org 0x66FB0
m68k_066fb0:
        btst.b #0x5,0xf603:w
m68k_066fb0_end:
.org 0x66FB6
m68k_066fb6:
        bne.w (. + 12)
m68k_066fb6_end:
.org 0x66FBA
m68k_066fba:
        subq.w #0x1,0xf608:w
m68k_066fba_end:
.org 0x66FBE
m68k_066fbe:
        bne.w (. + 26)
m68k_066fbe_end:
.org 0x66FC2
m68k_066fc2:
        move.w #0x201,0xf3c2:w
m68k_066fc2_end:
.org 0x66FC8
m68k_066fc8:
        move.w #0x208,0xf612:w
m68k_066fc8_end:
.org 0x66FCE
m68k_066fce:
        move.w #0x13,0xf362:w
m68k_066fce_end:
.org 0x66FD4
m68k_066fd4:
        clr.w 0xf36a:w
m68k_066fd4_end:
.org 0x66FD8
m68k_066fd8:
        rts
m68k_066fd8_end:
.org 0x66FDA
m68k_066fda:
        btst.b #0x5,0xf603:w
m68k_066fda_end:
.org 0x66FE0
m68k_066fe0:
        beq.w (. + 34)
m68k_066fe0_end:
.org 0x66FE4
m68k_066fe4:
        move.w 0xf3da:w,0xf3c2:w
m68k_066fe4_end:
.org 0x66FEA
m68k_066fea:
        move.w 0xf3dc:w,0xf3c4:w
m68k_066fea_end:
.org 0x66FF0
m68k_066ff0:
        move.w #0x208,0xf612:w
m68k_066ff0_end:
.org 0x66FF6
m68k_066ff6:
        move.w #0x13,0xf362:w
m68k_066ff6_end:
.org 0x66FFC
m68k_066ffc:
        move.w #0xfffe,0xf376:w
m68k_066ffc_end:
.org 0x67002
m68k_067002:
        rts
m68k_067002_end:
.org 0x67004
m68k_067004:
        subq.w #0x1,0xf608:w
m68k_067004_end:
.org 0x67008
m68k_067008:
        beq.w (. + 14)
m68k_067008_end:
.org 0x6700C
m68k_06700c:
        btst.b #0x5,0xf603:w
m68k_06700c_end:
.org 0x67012
m68k_067012:
        beq.w (. + 10)
m68k_067012_end:
.org 0x67016
m68k_067016:
        move.w #0x6,0xf362:w
m68k_067016_end:
.org 0x6701C
m68k_06701c:
        rts
m68k_06701c_end:
