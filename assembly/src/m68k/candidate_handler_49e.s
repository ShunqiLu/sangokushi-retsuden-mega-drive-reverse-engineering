| 候选处理入口 01A49E。共享地形逻辑及随机数例程由独立模块提供。
.cpu 68000
.section .text
_start:
.org 0x1A438
m68k_01a438:
        move.l %d4,-(%a7)
m68k_01a438_end:
.org 0x1A43A
m68k_01a43a:
        lea.l 0x945e8:l,%a0
m68k_01a43a_end:
.org 0x1A440
m68k_01a440:
        move.w 0xf68a:w,%d4
m68k_01a440_end:
.org 0x1A444
m68k_01a444:
        mulu.w #0x8c0,%d4
m68k_01a444_end:
.org 0x1A448
m68k_01a448:
        adda.l %d4,%a0
m68k_01a448_end:
.org 0x1A44A
m68k_01a44a:
        move.l (%a7)+,%d4
m68k_01a44a_end:
.org 0x1A44C
m68k_01a44c:
        rts
m68k_01a44c_end:
.org 0x1A49E
m68k_01a49e:
        bsr.w (. + 854)
m68k_01a49e_end:
.org 0x1A4A2
m68k_01a4a2:
        bsr.w (. + 612)
m68k_01a4a2_end:
.org 0x1A4A6
m68k_01a4a6:
        bsr.w (. + 764)
m68k_01a4a6_end:
.org 0x1A4AA
m68k_01a4aa:
        tst.w %d7
m68k_01a4aa_end:
.org 0x1A4AC
m68k_01a4ac:
        beq.w (. + 394)
m68k_01a4ac_end:
.org 0x1A4B0
m68k_01a4b0:
        andi.l #0xffff,%d7
m68k_01a4b0_end:
.org 0x1A4B6
m68k_01a4b6:
        divu.w #0x64,%d7
m68k_01a4b6_end:
.org 0x1A4BA
m68k_01a4ba:
        lea.l 0xc800:w,%a0
m68k_01a4ba_end:
.org 0x1A4BE
m68k_01a4be:
        move.w 0xf3a6:w,%d1
m68k_01a4be_end:
.org 0x1A4C2
m68k_01a4c2:
        lsl.w #0x2,%d1
m68k_01a4c2_end:
.org 0x1A4C4
m68k_01a4c4:
        move.l (%a0, %d1.w),%d2
m68k_01a4c4_end:
.org 0x1A4C8
m68k_01a4c8:
        move.l %d2,%d6
m68k_01a4c8_end:
.org 0x1A4CA
m68k_01a4ca:
        mulu.w %d0,%d6
m68k_01a4ca_end:
.org 0x1A4CC
m68k_01a4cc:
        divu.w #0x3e8,%d6
m68k_01a4cc_end:
.org 0x1A4D0
m68k_01a4d0:
        andi.l #0xffff,%d6
m68k_01a4d0_end:
.org 0x1A4D6
m68k_01a4d6:
        sub.l %d6,%d2
m68k_01a4d6_end:
.org 0x1A4D8
m68k_01a4d8:
        move.l %d2,(%a0, %d1.w)
m68k_01a4d8_end:
.org 0x1A4DC
m68k_01a4dc:
        move.l %d6,0xf3c8:w
m68k_01a4dc_end:
.org 0x1A4E0
m68k_01a4e0:
        cmpi.w #0x5,%d7
m68k_01a4e0_end:
.org 0x1A4E4
m68k_01a4e4:
        bls.b (. + 48)
m68k_01a4e4_end:
.org 0x1A4E6
m68k_01a4e6:
        move.w #0xa,%d0
m68k_01a4e6_end:
.org 0x1A4EA
m68k_01a4ea:
        sub.w %d7,%d0
m68k_01a4ea_end:
.org 0x1A4EC
m68k_01a4ec:
        cmpi.w #0x5,%d0
m68k_01a4ec_end:
.org 0x1A4F0
m68k_01a4f0:
        bls.w (. + 8)
m68k_01a4f0_end:
.org 0x1A4F4
m68k_01a4f4:
        move.w #0x5,%d0
m68k_01a4f4_end:
.org 0x1A4F8
m68k_01a4f8:
        lea.l 0xb200:w,%a0
m68k_01a4f8_end:
.org 0x1A4FC
m68k_01a4fc:
        move.w 0xf3a6:w,%d1
m68k_01a4fc_end:
.org 0x1A500
m68k_01a500:
        lsl.w #0x1,%d1
m68k_01a500_end:
.org 0x1A502
m68k_01a502:
        move.w (%a0, %d1.w),%d2
m68k_01a502_end:
.org 0x1A506
m68k_01a506:
        move.w %d2,%d3
m68k_01a506_end:
.org 0x1A508
m68k_01a508:
        mulu.w %d0,%d2
m68k_01a508_end:
.org 0x1A50A
m68k_01a50a:
        divu.w #0xa,%d2
m68k_01a50a_end:
.org 0x1A50E
m68k_01a50e:
        sub.w %d2,%d3
m68k_01a50e_end:
.org 0x1A510
m68k_01a510:
        move.w %d2,(%a0, %d1.w)
m68k_01a510_end:
.org 0x1A514
m68k_01a514:
        jsr 0x83d4:l
m68k_01a514_end:
.org 0x1A51A
m68k_01a51a:
        moveq #0,%d1
m68k_01a51a_end:
.org 0x1A51C
m68k_01a51c:
        move.w 0xf61c:w,%d1
m68k_01a51c_end:
.org 0x1A520
m68k_01a520:
        move.l %d1,%d2
m68k_01a520_end:
.org 0x1A522
m68k_01a522:
        lsl.l #0x2,%d1
m68k_01a522_end:
.org 0x1A524
m68k_01a524:
        add.l %d2,%d1
m68k_01a524_end:
.org 0x1A526
m68k_01a526:
        swap %d1
m68k_01a526_end:
.org 0x1A528
m68k_01a528:
        addq.w #0x1,%d1
m68k_01a528_end:
.org 0x1A52A
m68k_01a52a:
        lea.l 0xc500:w,%a0
m68k_01a52a_end:
.org 0x1A52E
m68k_01a52e:
        move.w 0xf3a6:w,%d0
m68k_01a52e_end:
.org 0x1A532
m68k_01a532:
        sub.b %d1,(%a0, %d0.w)
m68k_01a532_end:
.org 0x1A536
m68k_01a536:
        bcc.b (. + 6)
m68k_01a536_end:
.org 0x1A538
m68k_01a538:
        clr.b (%a0, %d0.w)
m68k_01a538_end:
.org 0x1A53C
m68k_01a53c:
        jsr 0x83d4:l
m68k_01a53c_end:
.org 0x1A542
m68k_01a542:
        andi.l #0xffff,%d0
m68k_01a542_end:
.org 0x1A548
m68k_01a548:
        move.l %d0,%d1
m68k_01a548_end:
.org 0x1A54A
m68k_01a54a:
        lsl.l #0x2,%d0
m68k_01a54a_end:
.org 0x1A54C
m68k_01a54c:
        add.l %d1,%d0
m68k_01a54c_end:
.org 0x1A54E
m68k_01a54e:
        swap %d0
m68k_01a54e_end:
.org 0x1A550
m68k_01a550:
        addq.w #0x1,%d0
m68k_01a550_end:
.org 0x1A552
m68k_01a552:
        move.w 0xf3f2:w,%d1
m68k_01a552_end:
.org 0x1A556
m68k_01a556:
        move.b (%a0, %d1.w),%d2
m68k_01a556_end:
.org 0x1A55A
m68k_01a55a:
        add.b %d0,%d2
m68k_01a55a_end:
.org 0x1A55C
m68k_01a55c:
        cmpi.b #0x63,%d2
m68k_01a55c_end:
.org 0x1A560
m68k_01a560:
        bls.b (. + 6)
m68k_01a560_end:
.org 0x1A562
m68k_01a562:
        move.b #0x63,%d2
m68k_01a562_end:
.org 0x1A566
m68k_01a566:
        move.b %d2,(%a0, %d1.w)
m68k_01a566_end:
.org 0x1A56A
m68k_01a56a:
        lea.l 0xc000:w,%a0
m68k_01a56a_end:
.org 0x1A56E
m68k_01a56e:
        lea.l 0xbe00:w,%a1
m68k_01a56e_end:
.org 0x1A572
m68k_01a572:
        move.w 0xf3a6:w,%d0
m68k_01a572_end:
.org 0x1A576
m68k_01a576:
        lsl.w #0x1,%d0
m68k_01a576_end:
.org 0x1A578
m68k_01a578:
        move.w %d7,%d1
m68k_01a578_end:
.org 0x1A57A
m68k_01a57a:
        move.w (%a0, %d0.w),%d2
m68k_01a57a_end:
.org 0x1A57E
m68k_01a57e:
        add.w %d1,%d2
m68k_01a57e_end:
.org 0x1A580
m68k_01a580:
        cmpi.w #0x3e7,%d2
m68k_01a580_end:
.org 0x1A584
m68k_01a584:
        bls.w (. + 8)
m68k_01a584_end:
.org 0x1A588
m68k_01a588:
        move.w #0x3e7,%d2
m68k_01a588_end:
.org 0x1A58C
m68k_01a58c:
        move.w %d2,(%a0, %d0.w)
m68k_01a58c_end:
.org 0x1A590
m68k_01a590:
        lsl.w #0x1,%d1
m68k_01a590_end:
.org 0x1A592
m68k_01a592:
        move.w (%a1, %d0.w),%d2
m68k_01a592_end:
.org 0x1A596
m68k_01a596:
        add.w %d1,%d2
m68k_01a596_end:
.org 0x1A598
m68k_01a598:
        cmpi.w #0x3e7,%d2
m68k_01a598_end:
.org 0x1A59C
m68k_01a59c:
        bls.b (. + 6)
m68k_01a59c_end:
.org 0x1A59E
m68k_01a59e:
        move.w #0x3e7,%d2
m68k_01a59e_end:
.org 0x1A5A2
m68k_01a5a2:
        move.w %d2,(%a1, %d0.w)
m68k_01a5a2_end:
.org 0x1A5A6
m68k_01a5a6:
        move.w 0xf3f2:w,%d0
m68k_01a5a6_end:
.org 0x1A5AA
m68k_01a5aa:
        lsl.w #0x1,%d0
m68k_01a5aa_end:
.org 0x1A5AC
m68k_01a5ac:
        andi.l #0xffff,%d6
m68k_01a5ac_end:
.org 0x1A5B2
m68k_01a5b2:
        divu.w #0xc8,%d6
m68k_01a5b2_end:
.org 0x1A5B6
m68k_01a5b6:
        move.w (%a1, %d0.w),%d2
m68k_01a5b6_end:
.org 0x1A5BA
m68k_01a5ba:
        add.w %d6,%d2
m68k_01a5ba_end:
.org 0x1A5BC
m68k_01a5bc:
        cmpi.w #0x3e7,%d2
m68k_01a5bc_end:
.org 0x1A5C0
m68k_01a5c0:
        bls.b (. + 6)
m68k_01a5c0_end:
.org 0x1A5C2
m68k_01a5c2:
        move.w #0x3e7,%d2
m68k_01a5c2_end:
.org 0x1A5C6
m68k_01a5c6:
        move.w %d2,(%a1, %d0.w)
m68k_01a5c6_end:
.org 0x1A5CA
m68k_01a5ca:
        mulu.w #0x3,%d6
m68k_01a5ca_end:
.org 0x1A5CE
m68k_01a5ce:
        divu.w #0xa,%d6
m68k_01a5ce_end:
.org 0x1A5D2
m68k_01a5d2:
        move.w (%a0, %d0.w),%d2
m68k_01a5d2_end:
.org 0x1A5D6
m68k_01a5d6:
        add.w %d6,%d2
m68k_01a5d6_end:
.org 0x1A5D8
m68k_01a5d8:
        cmpi.w #0x3e7,%d2
m68k_01a5d8_end:
.org 0x1A5DC
m68k_01a5dc:
        bls.w (. + 8)
m68k_01a5dc_end:
.org 0x1A5E0
m68k_01a5e0:
        move.w #0x3e7,%d2
m68k_01a5e0_end:
.org 0x1A5E4
m68k_01a5e4:
        move.w %d2,(%a0, %d0.w)
m68k_01a5e4_end:
.org 0x1A5E8
m68k_01a5e8:
        move.w #0x20,0xff7026:l
m68k_01a5e8_end:
.org 0x1A5F0
m68k_01a5f0:
        tst.w 0xf6d4:w
m68k_01a5f0_end:
.org 0x1A5F4
m68k_01a5f4:
        bne.w (. + 58)
m68k_01a5f4_end:
.org 0x1A5F8
m68k_01a5f8:
        move.w #0x1e,0xff7026:l
m68k_01a5f8_end:
.org 0x1A600
m68k_01a600:
        jsr -458(%pc)
m68k_01a600_end:
.org 0x1A604
m68k_01a604:
        move.w 0xf3a6:w,%d0
m68k_01a604_end:
.org 0x1A608
m68k_01a608:
        lsl.w #0x2,%d0
m68k_01a608_end:
.org 0x1A60A
m68k_01a60a:
        lea.l 0xa150:w,%a1
m68k_01a60a_end:
.org 0x1A60E
m68k_01a60e:
        move.w (%a1, %d0.w),%d1
m68k_01a60e_end:
.org 0x1A612
m68k_01a612:
        lsr.w #0x7,%d1
m68k_01a612_end:
.org 0x1A614
m68k_01a614:
        move.w 0x2(%a1, %d0.w),%d2
m68k_01a614_end:
.org 0x1A618
m68k_01a618:
        lsr.w #0x7,%d2
m68k_01a618_end:
.org 0x1A61A
m68k_01a61a:
        jsr -462(%pc)
m68k_01a61a_end:
.org 0x1A61E
m68k_01a61e:
        cmpi.b #0x1,%d0
m68k_01a61e_end:
.org 0x1A622
m68k_01a622:
        bne.w (. + 12)
m68k_01a622_end:
.org 0x1A626
m68k_01a626:
        move.w #0x1f,0xff7026:l
m68k_01a626_end:
.org 0x1A62E
m68k_01a62e:
        andi.w #0xfffe,%sr
m68k_01a62e_end:
.org 0x1A632
m68k_01a632:
        bra.w (. + 210)
m68k_01a632_end:
.org 0x1A636
m68k_01a636:
        jsr 0x83d4:l
m68k_01a636_end:
.org 0x1A63C
m68k_01a63c:
        moveq #0,%d2
m68k_01a63c_end:
.org 0x1A63E
m68k_01a63e:
        move.w 0xf61c:w,%d2
m68k_01a63e_end:
.org 0x1A642
m68k_01a642:
        move.l %d2,%d3
m68k_01a642_end:
.org 0x1A644
m68k_01a644:
        lsl.l #0x2,%d2
m68k_01a644_end:
.org 0x1A646
m68k_01a646:
        add.l %d3,%d2
m68k_01a646_end:
.org 0x1A648
m68k_01a648:
        swap %d2
m68k_01a648_end:
.org 0x1A64A
m68k_01a64a:
        addq.w #0x1,%d2
m68k_01a64a_end:
.org 0x1A64C
m68k_01a64c:
        lea.l 0xc500:w,%a0
m68k_01a64c_end:
.org 0x1A650
m68k_01a650:
        move.w 0xf3f2:w,%d0
m68k_01a650_end:
.org 0x1A654
m68k_01a654:
        sub.b %d2,(%a0, %d0.w)
m68k_01a654_end:
.org 0x1A658
m68k_01a658:
        bcc.b (. + 6)
m68k_01a658_end:
.org 0x1A65A
m68k_01a65a:
        clr.b (%a0, %d0.w)
m68k_01a65a_end:
.org 0x1A65E
m68k_01a65e:
        lea.l 0xb600:w,%a0
m68k_01a65e_end:
.org 0x1A662
m68k_01a662:
        lea.l 0xc000:w,%a1
m68k_01a662_end:
.org 0x1A666
m68k_01a666:
        lea.l 0xbe00:w,%a2
m68k_01a666_end:
.org 0x1A66A
m68k_01a66a:
        move.w 0xf3a6:w,%d0
m68k_01a66a_end:
.org 0x1A66E
m68k_01a66e:
        lsl.w #0x1,%d0
m68k_01a66e_end:
.org 0x1A670
m68k_01a670:
        move.w (%a0, %d0.w),%d2
m68k_01a670_end:
.org 0x1A674
m68k_01a674:
        move.w 0xf3f2:w,%d1
m68k_01a674_end:
.org 0x1A678
m68k_01a678:
        lsl.w #0x1,%d1
m68k_01a678_end:
.org 0x1A67A
m68k_01a67a:
        sub.w (%a0, %d1.w),%d2
m68k_01a67a_end:
.org 0x1A67E
m68k_01a67e:
        bcs.w (. + 34)
m68k_01a67e_end:
.org 0x1A682
m68k_01a682:
        andi.l #0xffff,%d2
m68k_01a682_end:
.org 0x1A688
m68k_01a688:
        divu.w #0xa,%d2
m68k_01a688_end:
.org 0x1A68C
m68k_01a68c:
        move.w (%a2, %d1.w),%d3
m68k_01a68c_end:
.org 0x1A690
m68k_01a690:
        add.w %d2,%d3
m68k_01a690_end:
.org 0x1A692
m68k_01a692:
        cmpi.w #0x3e7,%d3
m68k_01a692_end:
.org 0x1A696
m68k_01a696:
        bls.b (. + 6)
m68k_01a696_end:
.org 0x1A698
m68k_01a698:
        move.w #0x3e7,%d3
m68k_01a698_end:
.org 0x1A69C
m68k_01a69c:
        move.w %d3,(%a2, %d1.w)
m68k_01a69c_end:
.org 0x1A6A0
m68k_01a6a0:
        jsr 0x83d4:l
m68k_01a6a0_end:
.org 0x1A6A6
m68k_01a6a6:
        andi.l #0xffff,%d0
m68k_01a6a6_end:
.org 0x1A6AC
m68k_01a6ac:
        lsl.l #0x4,%d0
m68k_01a6ac_end:
.org 0x1A6AE
m68k_01a6ae:
        swap %d0
m68k_01a6ae_end:
.org 0x1A6B0
m68k_01a6b0:
        addi.w #0x5,%d0
m68k_01a6b0_end:
.org 0x1A6B4
m68k_01a6b4:
        move.w 0xf3a6:w,%d2
m68k_01a6b4_end:
.org 0x1A6B8
m68k_01a6b8:
        lsl.w #0x1,%d2
m68k_01a6b8_end:
.org 0x1A6BA
m68k_01a6ba:
        move.w (%a1, %d2.w),%d3
m68k_01a6ba_end:
.org 0x1A6BE
m68k_01a6be:
        add.w %d0,%d3
m68k_01a6be_end:
.org 0x1A6C0
m68k_01a6c0:
        cmpi.w #0x3e7,%d3
m68k_01a6c0_end:
.org 0x1A6C4
m68k_01a6c4:
        bls.b (. + 6)
m68k_01a6c4_end:
.org 0x1A6C6
m68k_01a6c6:
        move.w #0x3e7,%d3
m68k_01a6c6_end:
.org 0x1A6CA
m68k_01a6ca:
        move.w %d3,(%a1, %d2.w)
m68k_01a6ca_end:
.org 0x1A6CE
m68k_01a6ce:
        jsr 0x83d4:l
m68k_01a6ce_end:
.org 0x1A6D4
m68k_01a6d4:
        andi.l #0xffff,%d0
m68k_01a6d4_end:
.org 0x1A6DA
m68k_01a6da:
        move.l %d0,%d1
m68k_01a6da_end:
.org 0x1A6DC
m68k_01a6dc:
        lsl.l #0x1,%d0
m68k_01a6dc_end:
.org 0x1A6DE
m68k_01a6de:
        add.l %d1,%d0
m68k_01a6de_end:
.org 0x1A6E0
m68k_01a6e0:
        lsl.l #0x2,%d0
m68k_01a6e0_end:
.org 0x1A6E2
m68k_01a6e2:
        add.l %d1,%d0
m68k_01a6e2_end:
.org 0x1A6E4
m68k_01a6e4:
        swap %d0
m68k_01a6e4_end:
.org 0x1A6E6
m68k_01a6e6:
        addi.w #0xa,%d0
m68k_01a6e6_end:
.org 0x1A6EA
m68k_01a6ea:
        move.w (%a2, %d2.w),%d3
m68k_01a6ea_end:
.org 0x1A6EE
m68k_01a6ee:
        add.w %d0,%d3
m68k_01a6ee_end:
.org 0x1A6F0
m68k_01a6f0:
        cmpi.w #0x3e7,%d3
m68k_01a6f0_end:
.org 0x1A6F4
m68k_01a6f4:
        bls.w (. + 8)
m68k_01a6f4_end:
.org 0x1A6F8
m68k_01a6f8:
        move.w #0x3e7,%d3
m68k_01a6f8_end:
.org 0x1A6FC
m68k_01a6fc:
        move.w %d3,(%a2, %d2.w)
m68k_01a6fc_end:
.org 0x1A700
m68k_01a700:
        ori.w #0x1,%sr
m68k_01a700_end:
.org 0x1A704
m68k_01a704:
        rts
m68k_01a704_end:
