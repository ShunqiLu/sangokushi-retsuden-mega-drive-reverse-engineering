| 末级分派表覆盖的例程，入口地址见对应布局。
.cpu 68000
.section .text
_start:
.org 0x58FE
m68k_0058fe:
        bra.w (. + 12)
m68k_0058fe_end:
.org 0x5902
m68k_005902:
        bra.w (. + 14)
m68k_005902_end:
.org 0x5906
m68k_005906:
        bra.w (. + 16)
m68k_005906_end:
.org 0x590A
m68k_00590a:
        jmp 0x1270a:l
m68k_00590a_end:
.org 0x5910
m68k_005910:
        jmp 0x12734:l
m68k_005910_end:
.org 0x5916
m68k_005916:
        jmp 0x1273c:l
m68k_005916_end:
.org 0x1433C
m68k_01433c:
        addi.w #0x10,0xff3822:l
m68k_01433c_end:
.org 0x14344
m68k_014344:
        rts
m68k_014344_end:
.org 0x14346
m68k_014346:
        subi.w #0x10,0xff3824:l
m68k_014346_end:
.org 0x1434E
m68k_01434e:
        rts
m68k_01434e_end:
.org 0x14350
m68k_014350:
        subi.w #0x10,0xff3822:l
m68k_014350_end:
.org 0x14358
m68k_014358:
        rts
m68k_014358_end:
.org 0x1435A
m68k_01435a:
        addi.w #0x10,0xff3824:l
m68k_01435a_end:
.org 0x14362
m68k_014362:
        rts
m68k_014362_end:
.org 0x206B8
m68k_0206b8:
        move.w 0xf3a6:w,%d0
m68k_0206b8_end:
.org 0x206BC
m68k_0206bc:
        lea.l 0xcc00:w,%a0
m68k_0206bc_end:
.org 0x206C0
m68k_0206c0:
        move.b #0xff,(%a0, %d0.w)
m68k_0206c0_end:
.org 0x206C6
m68k_0206c6:
        bsr.w (. + 46)
m68k_0206c6_end:
.org 0x206CA
m68k_0206ca:
        bsr.w (. + 114)
m68k_0206ca_end:
.org 0x206CE
m68k_0206ce:
        bsr.w (. + 148)
m68k_0206ce_end:
.org 0x206D2
m68k_0206d2:
        move.w 0xf3a6:w,0xf3d2:w
m68k_0206d2_end:
.org 0x206D8
m68k_0206d8:
        move.w 0xf3a6:w,0xf3d0:w
m68k_0206d8_end:
.org 0x206DE
m68k_0206de:
        move.w #0x11d,%d0
m68k_0206de_end:
.org 0x206E2
m68k_0206e2:
        move.w %d0,0xaf80:w
m68k_0206e2_end:
.org 0x206E6
m68k_0206e6:
        jsr 0x676f2:l
m68k_0206e6_end:
.org 0x206EC
m68k_0206ec:
        move.w #0x1,0xf652:w
m68k_0206ec_end:
.org 0x206F2
m68k_0206f2:
        rts
m68k_0206f2_end:
.org 0x206F4
m68k_0206f4:
        lea.l 0xa5a4:w,%a0
m68k_0206f4_end:
.org 0x206F8
m68k_0206f8:
        lea.l 0xa57a:w,%a1
m68k_0206f8_end:
.org 0x206FC
m68k_0206fc:
        btst.b #0x1,0xf6d7:w
m68k_0206fc_end:
.org 0x20702
m68k_020702:
        beq.w (. + 12)
m68k_020702_end:
.org 0x20706
m68k_020706:
        lea.l 0xa550:w,%a0
m68k_020706_end:
.org 0x2070A
m68k_02070a:
        lea.l 0xa5ce:w,%a1
m68k_02070a_end:
.org 0x2070E
m68k_02070e:
        move.w (%a0)+,%d1
m68k_02070e_end:
.org 0x20710
m68k_020710:
        bmi.w (. + 22)
m68k_020710_end:
.org 0x20714
m68k_020714:
        andi.w #0xff,%d1
m68k_020714_end:
.org 0x20718
m68k_020718:
        cmp.w %d0,%d1
m68k_020718_end:
.org 0x2071A
m68k_02071a:
        bne.b (. + -12)
m68k_02071a_end:
.org 0x2071C
m68k_02071c:
        move.w (%a0)+,-0x4(%a0)
m68k_02071c_end:
.org 0x20720
m68k_020720:
        bpl.b (. + -4)
m68k_020720_end:
.org 0x20722
m68k_020722:
        bra.w (. + 24)
m68k_020722_end:
.org 0x20726
m68k_020726:
        move.w (%a1)+,%d1
m68k_020726_end:
.org 0x20728
m68k_020728:
        bmi.w (. + 18)
m68k_020728_end:
.org 0x2072C
m68k_02072c:
        andi.w #0xff,%d1
m68k_02072c_end:
.org 0x20730
m68k_020730:
        cmp.w %d0,%d1
m68k_020730_end:
.org 0x20732
m68k_020732:
        bne.b (. + -12)
m68k_020732_end:
.org 0x20734
m68k_020734:
        move.w (%a1)+,-0x4(%a1)
m68k_020734_end:
.org 0x20738
m68k_020738:
        bpl.b (. + -4)
m68k_020738_end:
.org 0x2073A
m68k_02073a:
        rts
m68k_02073a_end:
.org 0x2073C
m68k_02073c:
        btst.b #0x1,0xf6d7:w
m68k_02073c_end:
.org 0x20742
m68k_020742:
        bne.b (. + 8)
m68k_020742_end:
.org 0x20744
m68k_020744:
        lea.l 0xa5a4:w,%a0
m68k_020744_end:
.org 0x20748
m68k_020748:
        bra.b (. + 6)
m68k_020748_end:
.org 0x2074A
m68k_02074a:
        lea.l 0xa550:w,%a0
m68k_02074a_end:
.org 0x2074E
m68k_02074e:
        move.w (%a0)+,%d1
m68k_02074e_end:
.org 0x20750
m68k_020750:
        bmi.b (. + 16)
m68k_020750_end:
.org 0x20752
m68k_020752:
        andi.w #0xff,%d1
m68k_020752_end:
.org 0x20756
m68k_020756:
        cmp.w %d0,%d1
m68k_020756_end:
.org 0x20758
m68k_020758:
        bne.b (. + -10)
m68k_020758_end:
.org 0x2075A
m68k_02075a:
        move.w (%a0)+,-0x4(%a0)
m68k_02075a_end:
.org 0x2075E
m68k_02075e:
        bpl.b (. + -4)
m68k_02075e_end:
.org 0x20760
m68k_020760:
        rts
m68k_020760_end:
.org 0x20762
m68k_020762:
        jsr 0x83d4:l
m68k_020762_end:
.org 0x20768
m68k_020768:
        bsr.w (. + 40)
m68k_020768_end:
.org 0x2076C
m68k_02076c:
        moveq #0,%d0
m68k_02076c_end:
.org 0x2076E
m68k_02076e:
        move.w 0xf61c:w,%d0
m68k_02076e_end:
.org 0x20772
m68k_020772:
        move.l %d0,%d4
m68k_020772_end:
.org 0x20774
m68k_020774:
        lsl.l #0x2,%d0
m68k_020774_end:
.org 0x20776
m68k_020776:
        add.l %d4,%d0
m68k_020776_end:
.org 0x20778
m68k_020778:
        lsl.l #0x1,%d0
m68k_020778_end:
.org 0x2077A
m68k_02077a:
        add.l %d4,%d0
m68k_02077a_end:
.org 0x2077C
m68k_02077c:
        swap %d0
m68k_02077c_end:
.org 0x2077E
m68k_02077e:
        addi.w #0xa,%d0
m68k_02077e_end:
.org 0x20782
m68k_020782:
        divu.w %d0,%d3
m68k_020782_end:
.org 0x20784
m68k_020784:
        sub.w %d3,%d1
m68k_020784_end:
.org 0x20786
m68k_020786:
        bcc.b (. + 4)
m68k_020786_end:
.org 0x20788
m68k_020788:
        clr.w %d1
m68k_020788_end:
.org 0x2078A
m68k_02078a:
        move.b %d1,(%a0, %d2.w)
m68k_02078a_end:
.org 0x2078E
m68k_02078e:
        rts
m68k_02078e_end:
.org 0x20790
m68k_020790:
        lea.l 0xe640:w,%a0
m68k_020790_end:
.org 0x20794
m68k_020794:
        btst.b #0x1,0xf6d7:w
m68k_020794_end:
.org 0x2079A
m68k_02079a:
        bne.b (. + 10)
m68k_02079a_end:
.org 0x2079C
m68k_02079c:
        move.w 0xf68c:w,%d1
m68k_02079c_end:
.org 0x207A0
m68k_0207a0:
        bra.w (. + 8)
m68k_0207a0_end:
.org 0x207A4
m68k_0207a4:
        move.w 0xf68e:w,%d1
m68k_0207a4_end:
.org 0x207A8
m68k_0207a8:
        lsl.w #0x1,%d1
m68k_0207a8_end:
.org 0x207AA
m68k_0207aa:
        move.w (%a0, %d1.w),%d2
m68k_0207aa_end:
.org 0x207AE
m68k_0207ae:
        move.w %d2,0xf3f2:w
m68k_0207ae_end:
.org 0x207B2
m68k_0207b2:
        lea.l 0xc200:w,%a0
m68k_0207b2_end:
.org 0x207B6
m68k_0207b6:
        clr.w %d1
m68k_0207b6_end:
.org 0x207B8
m68k_0207b8:
        move.b (%a0, %d2.w),%d1
m68k_0207b8_end:
.org 0x207BC
m68k_0207bc:
        move.w 0xf3a6:w,%d0
m68k_0207bc_end:
.org 0x207C0
m68k_0207c0:
        moveq #0,%d3
m68k_0207c0_end:
.org 0x207C2
m68k_0207c2:
        move.b (%a0, %d0.w),%d3
m68k_0207c2_end:
.org 0x207C6
m68k_0207c6:
        rts
m68k_0207c6_end:
.org 0x207C8
m68k_0207c8:
        lea.l 0xef80:w,%a0
m68k_0207c8_end:
.org 0x207CC
m68k_0207cc:
        tst.w (%a0)+
m68k_0207cc_end:
.org 0x207CE
m68k_0207ce:
        bpl.b (. + -2)
m68k_0207ce_end:
.org 0x207D0
m68k_0207d0:
        move.w 0xf3a6:w,-0x2(%a0)
m68k_0207d0_end:
.org 0x207D6
m68k_0207d6:
        move.w #0xffff,(%a0)
m68k_0207d6_end:
.org 0x207DA
m68k_0207da:
        move.w 0xf3a6:w,%d0
m68k_0207da_end:
.org 0x207DE
m68k_0207de:
        bsr.w (. + -234)
m68k_0207de_end:
.org 0x207E2
m68k_0207e2:
        bsr.w (. + -166)
m68k_0207e2_end:
.org 0x207E6
m68k_0207e6:
        bsr.w (. + 58)
m68k_0207e6_end:
.org 0x207EA
m68k_0207ea:
        move.w 0xf3a6:w,0xf3d2:w
m68k_0207ea_end:
.org 0x207F0
m68k_0207f0:
        move.w 0xf3a6:w,0xf3d0:w
m68k_0207f0_end:
.org 0x207F6
m68k_0207f6:
        move.w #0x11e,%d0
m68k_0207f6_end:
.org 0x207FA
m68k_0207fa:
        move.w %d0,0xaf80:w
m68k_0207fa_end:
.org 0x207FE
m68k_0207fe:
        jsr 0x676f2:l
m68k_0207fe_end:
.org 0x20804
m68k_020804:
        move.w #0x1,0xf652:w
m68k_020804_end:
.org 0x2080A
m68k_02080a:
        lea.l 0xcc00:w,%a0
m68k_02080a_end:
.org 0x2080E
m68k_02080e:
        move.w 0xf68a:w,%d0
m68k_02080e_end:
.org 0x20812
m68k_020812:
        bset.l #0x7,%d0
m68k_020812_end:
.org 0x20816
m68k_020816:
        move.w 0xf3a6:w,%d1
m68k_020816_end:
.org 0x2081A
m68k_02081a:
        move.b %d0,(%a0, %d1.w)
m68k_02081a_end:
.org 0x2081E
m68k_02081e:
        rts
m68k_02081e_end:
.org 0x20820
m68k_020820:
        jsr 0x83d4:l
m68k_020820_end:
.org 0x20826
m68k_020826:
        bsr.w (. + -150)
m68k_020826_end:
.org 0x2082A
m68k_02082a:
        moveq #0,%d0
m68k_02082a_end:
.org 0x2082C
m68k_02082c:
        move.w 0xf61c:w,%d0
m68k_02082c_end:
.org 0x20830
m68k_020830:
        move.l %d0,%d4
m68k_020830_end:
.org 0x20832
m68k_020832:
        lsl.l #0x2,%d0
m68k_020832_end:
.org 0x20834
m68k_020834:
        add.l %d4,%d0
m68k_020834_end:
.org 0x20836
m68k_020836:
        lsl.l #0x1,%d0
m68k_020836_end:
.org 0x20838
m68k_020838:
        add.l %d4,%d0
m68k_020838_end:
.org 0x2083A
m68k_02083a:
        addi.w #0x1e,%d0
m68k_02083a_end:
.org 0x2083E
m68k_02083e:
        divu.w %d0,%d3
m68k_02083e_end:
.org 0x20840
m68k_020840:
        add.w %d3,%d1
m68k_020840_end:
.org 0x20842
m68k_020842:
        cmpi.w #0x64,%d1
m68k_020842_end:
.org 0x20846
m68k_020846:
        bls.b (. + 6)
m68k_020846_end:
.org 0x20848
m68k_020848:
        move.w #0x64,%d1
m68k_020848_end:
.org 0x2084C
m68k_02084c:
        move.b %d1,(%a0, %d2.w)
m68k_02084c_end:
.org 0x20850
m68k_020850:
        rts
m68k_020850_end:
.org 0x20852
m68k_020852:
        lea.l 0xaf28:w,%a0
m68k_020852_end:
.org 0x20856
m68k_020856:
        tst.w (%a0)+
m68k_020856_end:
.org 0x20858
m68k_020858:
        bpl.b (. + -2)
m68k_020858_end:
.org 0x2085A
m68k_02085a:
        move.w 0xf3a6:w,-0x2(%a0)
m68k_02085a_end:
.org 0x20860
m68k_020860:
        move.w #0xffff,(%a0)
m68k_020860_end:
.org 0x20864
m68k_020864:
        move.w 0xf3a6:w,%d0
m68k_020864_end:
.org 0x20868
m68k_020868:
        bsr.w (. + -372)
m68k_020868_end:
.org 0x2086C
m68k_02086c:
        bsr.w (. + -304)
m68k_02086c_end:
.org 0x20870
m68k_020870:
        bsr.w (. + 42)
m68k_020870_end:
.org 0x20874
m68k_020874:
        bsr.w (. + 90)
m68k_020874_end:
.org 0x20878
m68k_020878:
        move.w 0xf3a6:w,0xf3d2:w
m68k_020878_end:
.org 0x2087E
m68k_02087e:
        move.w 0xf3a6:w,0xf3d0:w
m68k_02087e_end:
.org 0x20884
m68k_020884:
        move.w #0x11f,%d0
m68k_020884_end:
.org 0x20888
m68k_020888:
        move.w %d0,0xaf80:w
m68k_020888_end:
.org 0x2088C
m68k_02088c:
        jsr 0x676f2:l
m68k_02088c_end:
.org 0x20892
m68k_020892:
        move.w #0x1,0xf652:w
m68k_020892_end:
.org 0x20898
m68k_020898:
        rts
m68k_020898_end:
.org 0x2089A
m68k_02089a:
        jsr 0x83d4:l
m68k_02089a_end:
.org 0x208A0
m68k_0208a0:
        bsr.w (. + -272)
m68k_0208a0_end:
.org 0x208A4
m68k_0208a4:
        moveq #0,%d0
m68k_0208a4_end:
.org 0x208A6
m68k_0208a6:
        move.w 0xf61c:w,%d0
m68k_0208a6_end:
.org 0x208AA
m68k_0208aa:
        move.l %d0,%d4
m68k_0208aa_end:
.org 0x208AC
m68k_0208ac:
        lsl.l #0x1,%d0
m68k_0208ac_end:
.org 0x208AE
m68k_0208ae:
        add.l %d4,%d0
m68k_0208ae_end:
.org 0x208B0
m68k_0208b0:
        lsl.l #0x3,%d0
m68k_0208b0_end:
.org 0x208B2
m68k_0208b2:
        add.l %d4,%d0
m68k_0208b2_end:
.org 0x208B4
m68k_0208b4:
        lsl.l #0x1,%d0
m68k_0208b4_end:
.org 0x208B6
m68k_0208b6:
        addi.w #0x32,%d0
m68k_0208b6_end:
.org 0x208BA
m68k_0208ba:
        divu.w %d0,%d3
m68k_0208ba_end:
.org 0x208BC
m68k_0208bc:
        add.w %d3,%d1
m68k_0208bc_end:
.org 0x208BE
m68k_0208be:
        cmpi.w #0x64,%d1
m68k_0208be_end:
.org 0x208C2
m68k_0208c2:
        bls.b (. + 6)
m68k_0208c2_end:
.org 0x208C4
m68k_0208c4:
        move.w #0x64,%d1
m68k_0208c4_end:
.org 0x208C8
m68k_0208c8:
        move.b %d1,(%a0, %d2.w)
m68k_0208c8_end:
.org 0x208CC
m68k_0208cc:
        rts
m68k_0208cc_end:
.org 0x3B7BC
m68k_03b7bc:
        bra.w (. + 40)
m68k_03b7bc_end:
.org 0x3B7C0
m68k_03b7c0:
        bra.w (. + 152)
m68k_03b7c0_end:
.org 0x3B7C4
m68k_03b7c4:
        bra.w (. + 286)
m68k_03b7c4_end:
.org 0x3B7C8
m68k_03b7c8:
        bra.w (. + 314)
m68k_03b7c8_end:
.org 0x3B7CC
m68k_03b7cc:
        bra.w (. + 430)
m68k_03b7cc_end:
.org 0x3B7D0
m68k_03b7d0:
        bra.w (. + 458)
m68k_03b7d0_end:
.org 0x3B7D4
m68k_03b7d4:
        bra.w (. + 510)
m68k_03b7d4_end:
.org 0x3B7D8
m68k_03b7d8:
        bra.w (. + 634)
m68k_03b7d8_end:
.org 0x3B7DC
m68k_03b7dc:
        bra.w (. + 890)
m68k_03b7dc_end:
.org 0x3B7E0
m68k_03b7e0:
        bra.w (. + 972)
m68k_03b7e0_end:
.org 0x3B7E4
m68k_03b7e4:
        move.w #0xffff,0x80ca:w
m68k_03b7e4_end:
.org 0x3B7EA
m68k_03b7ea:
        move.w #0x0,0x80cc:w
m68k_03b7ea_end:
.org 0x3B7F0
m68k_03b7f0:
        move.w #0xffff,0x80ce:w
m68k_03b7f0_end:
.org 0x3B7F6
m68k_03b7f6:
        move.w #0xffff,0x80d0:w
m68k_03b7f6_end:
.org 0x3B7FC
m68k_03b7fc:
        moveq #1,%d0
m68k_03b7fc_end:
.org 0x3B7FE
m68k_03b7fe:
        jsr -3552(%pc)
m68k_03b7fe_end:
.org 0x3B802
m68k_03b802:
        move.w #0x2700,%sr
m68k_03b802_end:
.org 0x3B806
m68k_03b806:
        move.w #0x8f02,0xc00004:l
m68k_03b806_end:
.org 0x3B80E
m68k_03b80e:
        move.l #0x60000002,0xc00004:l
m68k_03b80e_end:
.org 0x3B818
m68k_03b818:
        lea.l 0xc00000:l,%a5
m68k_03b818_end:
.org 0x3B81E
m68k_03b81e:
        move.w #0x3333,%d6
m68k_03b81e_end:
.org 0x3B822
m68k_03b822:
        move.w #0xd7f,%d7
m68k_03b822_end:
.org 0x3B826
m68k_03b826:
        move.w %d6,(%a5)
m68k_03b826_end:
.org 0x3B828
m68k_03b828:
        dbra %d7,(. + -2)
m68k_03b828_end:
.org 0x3B82C
m68k_03b82c:
        move.w #0xa000,0xff700c:l
m68k_03b82c_end:
.org 0x3B834
m68k_03b834:
        move.l #0x3b4d8,0xff700e:l
m68k_03b834_end:
.org 0x3B83E
m68k_03b83e:
        move.w #0x3,0xff7014:l
m68k_03b83e_end:
.org 0x3B846
m68k_03b846:
        move.w #0x1,0xff7016:l
m68k_03b846_end:
.org 0x3B84E
m68k_03b84e:
        move.w #0x2500,%sr
m68k_03b84e_end:
.org 0x3B852
m68k_03b852:
        addq.w #0x1,0x80ea:w
m68k_03b852_end:
.org 0x3B856
m68k_03b856:
        rts
m68k_03b856_end:
.org 0x3B858
m68k_03b858:
        bsr.w (. + 120)
m68k_03b858_end:
.org 0x3B85C
m68k_03b85c:
        addq.w #0x1,0x813a:w
m68k_03b85c_end:
.org 0x3B860
m68k_03b860:
        cmpi.w #0x200,0x813a:w
m68k_03b860_end:
.org 0x3B866
m68k_03b866:
        bcs.b (. + 104)
m68k_03b866_end:
.org 0x3B868
m68k_03b868:
        move.w #0x0,0x80ca:w
m68k_03b868_end:
.org 0x3B86E
m68k_03b86e:
        move.w #0xffff,0x80cc:w
m68k_03b86e_end:
.org 0x3B874
m68k_03b874:
        move.w #0x0,0x80ce:w
m68k_03b874_end:
.org 0x3B87A
m68k_03b87a:
        move.w #0x0,0x80d0:w
m68k_03b87a_end:
.org 0x3B880
m68k_03b880:
        moveq #1,%d0
m68k_03b880_end:
.org 0x3B882
m68k_03b882:
        jsr -3684(%pc)
m68k_03b882_end:
.org 0x3B886
m68k_03b886:
        move.w #0x2700,%sr
m68k_03b886_end:
.org 0x3B88A
m68k_03b88a:
        move.w #0x8f02,0xc00004:l
m68k_03b88a_end:
.org 0x3B892
m68k_03b892:
        move.l #0x60000002,0xc00004:l
m68k_03b892_end:
.org 0x3B89C
m68k_03b89c:
        lea.l 0xc00000:l,%a5
m68k_03b89c_end:
.org 0x3B8A2
m68k_03b8a2:
        move.w #0x3333,%d6
m68k_03b8a2_end:
.org 0x3B8A6
m68k_03b8a6:
        move.w #0xd7f,%d7
m68k_03b8a6_end:
.org 0x3B8AA
m68k_03b8aa:
        move.w %d6,(%a5)
m68k_03b8aa_end:
.org 0x3B8AC
m68k_03b8ac:
        dbra %d7,(. + -2)
m68k_03b8ac_end:
.org 0x3B8B0
m68k_03b8b0:
        move.w #0xa000,0xff700c:l
m68k_03b8b0_end:
.org 0x3B8B8
m68k_03b8b8:
        move.l #0x3b506,0xff700e:l
m68k_03b8b8_end:
.org 0x3B8C2
m68k_03b8c2:
        move.w #0x2500,%sr
m68k_03b8c2_end:
.org 0x3B8C6
m68k_03b8c6:
        clr.w 0x813a:w
m68k_03b8c6_end:
.org 0x3B8CA
m68k_03b8ca:
        addq.w #0x1,0x80ea:w
m68k_03b8ca_end:
.org 0x3B8CE
m68k_03b8ce:
        rts
m68k_03b8ce_end:
.org 0x3B8D0
m68k_03b8d0:
        move.w #0xc,%d2
m68k_03b8d0_end:
.org 0x3B8D4
m68k_03b8d4:
        move.w #0x80,%d0
m68k_03b8d4_end:
.org 0x3B8D8
m68k_03b8d8:
        move.w #0xc0,%d1
m68k_03b8d8_end:
.org 0x3B8DC
m68k_03b8dc:
        bsr.w (. + 742)
m68k_03b8dc_end:
.org 0x3B8E0
m68k_03b8e0:
        rts
m68k_03b8e0_end:
.org 0x3B8E2
m68k_03b8e2:
        bsr.w (. + -18)
m68k_03b8e2_end:
.org 0x3B8E6
m68k_03b8e6:
        addq.w #0x1,0x813a:w
m68k_03b8e6_end:
.org 0x3B8EA
m68k_03b8ea:
        cmpi.w #0x200,0x813a:w
m68k_03b8ea_end:
.org 0x3B8F0
m68k_03b8f0:
        bcs.b (. + 16)
m68k_03b8f0_end:
.org 0x3B8F2
m68k_03b8f2:
        moveq #1,%d0
m68k_03b8f2_end:
.org 0x3B8F4
m68k_03b8f4:
        jsr -3774(%pc)
m68k_03b8f4_end:
.org 0x3B8F8
m68k_03b8f8:
        clr.w 0x813a:w
m68k_03b8f8_end:
.org 0x3B8FC
m68k_03b8fc:
        addq.w #0x1,0x80ea:w
m68k_03b8fc_end:
.org 0x3B900
m68k_03b900:
        rts
m68k_03b900_end:
.org 0x3B902
m68k_03b902:
        bsr.w (. + -50)
m68k_03b902_end:
.org 0x3B906
m68k_03b906:
        btst.b #0x7,0x80c4:w
m68k_03b906_end:
.org 0x3B90C
m68k_03b90c:
        beq.w (. + 108)
m68k_03b90c_end:
.org 0x3B910
m68k_03b910:
        move.w #0x2700,%sr
m68k_03b910_end:
.org 0x3B914
m68k_03b914:
        lea.l 0x4632a:l,%a0
m68k_03b914_end:
.org 0x3B91A
m68k_03b91a:
        lea.l 0xe000:l,%a1
m68k_03b91a_end:
.org 0x3B920
m68k_03b920:
        move.l #0x80,%d5
m68k_03b920_end:
.org 0x3B926
m68k_03b926:
        move.w #0x12,%d6
m68k_03b926_end:
.org 0x3B92A
m68k_03b92a:
        jsr -3678(%pc)
m68k_03b92a_end:
.org 0x3B92E
m68k_03b92e:
        move.w #0x8f02,0xc00004:l
m68k_03b92e_end:
.org 0x3B936
m68k_03b936:
        move.l #0x60000002,0xc00004:l
m68k_03b936_end:
.org 0x3B940
m68k_03b940:
        lea.l 0xc00000:l,%a5
m68k_03b940_end:
.org 0x3B946
m68k_03b946:
        move.w #0x3333,%d6
m68k_03b946_end:
.org 0x3B94A
m68k_03b94a:
        move.w #0xd7f,%d7
m68k_03b94a_end:
.org 0x3B94E
m68k_03b94e:
        move.w %d6,(%a5)
m68k_03b94e_end:
.org 0x3B950
m68k_03b950:
        dbra %d7,(. + -2)
m68k_03b950_end:
.org 0x3B954
m68k_03b954:
        move.w #0xa000,0xff700c:l
m68k_03b954_end:
.org 0x3B95C
m68k_03b95c:
        move.l #0x3b532,0xff700e:l
m68k_03b95c_end:
.org 0x3B966
m68k_03b966:
        move.w #0x2500,%sr
m68k_03b966_end:
.org 0x3B96A
m68k_03b96a:
        moveq #1,%d0
m68k_03b96a_end:
.org 0x3B96C
m68k_03b96c:
        jsr -3918(%pc)
m68k_03b96c_end:
.org 0x3B970
m68k_03b970:
        clr.w 0x813a:w
m68k_03b970_end:
.org 0x3B974
m68k_03b974:
        addq.w #0x1,0x80ea:w
m68k_03b974_end:
.org 0x3B978
m68k_03b978:
        rts
m68k_03b978_end:
.org 0x3B97A
m68k_03b97a:
        bsr.w (. + -170)
m68k_03b97a_end:
.org 0x3B97E
m68k_03b97e:
        addq.w #0x1,0x813a:w
m68k_03b97e_end:
.org 0x3B982
m68k_03b982:
        cmpi.w #0x200,0x813a:w
m68k_03b982_end:
.org 0x3B988
m68k_03b988:
        bcs.b (. + 16)
m68k_03b988_end:
.org 0x3B98A
m68k_03b98a:
        moveq #1,%d0
m68k_03b98a_end:
.org 0x3B98C
m68k_03b98c:
        jsr -3926(%pc)
m68k_03b98c_end:
.org 0x3B990
m68k_03b990:
        clr.w 0x813a:w
m68k_03b990_end:
.org 0x3B994
m68k_03b994:
        addq.w #0x1,0x80ea:w
m68k_03b994_end:
.org 0x3B998
m68k_03b998:
        rts
m68k_03b998_end:
.org 0x3B99A
m68k_03b99a:
        bsr.w (. + -202)
m68k_03b99a_end:
.org 0x3B99E
m68k_03b99e:
        addq.w #0x1,0x813a:w
m68k_03b99e_end:
.org 0x3B9A2
m68k_03b9a2:
        cmpi.w #0x40,0x813a:w
m68k_03b9a2_end:
.org 0x3B9A8
m68k_03b9a8:
        bcs.b (. + 40)
m68k_03b9a8_end:
.org 0x3B9AA
m68k_03b9aa:
        move.w #0xffff,0x80ca:w
m68k_03b9aa_end:
.org 0x3B9B0
m68k_03b9b0:
        move.w #0xffff,0x80cc:w
m68k_03b9b0_end:
.org 0x3B9B6
m68k_03b9b6:
        move.w #0x0,0x80ce:w
m68k_03b9b6_end:
.org 0x3B9BC
m68k_03b9bc:
        move.w #0xffff,0x80d0:w
m68k_03b9bc_end:
.org 0x3B9C2
m68k_03b9c2:
        moveq #1,%d0
m68k_03b9c2_end:
.org 0x3B9C4
m68k_03b9c4:
        jsr -3982(%pc)
m68k_03b9c4_end:
.org 0x3B9C8
m68k_03b9c8:
        clr.w 0x813a:w
m68k_03b9c8_end:
.org 0x3B9CC
m68k_03b9cc:
        addq.w #0x1,0x80ea:w
m68k_03b9cc_end:
.org 0x3B9D0
m68k_03b9d0:
        rts
m68k_03b9d0_end:
.org 0x3B9D2
m68k_03b9d2:
        bsr.w (. + -258)
m68k_03b9d2_end:
.org 0x3B9D6
m68k_03b9d6:
        btst.b #0x7,0x80c4:w
m68k_03b9d6_end:
.org 0x3B9DC
m68k_03b9dc:
        beq.w (. + 116)
m68k_03b9dc_end:
.org 0x3B9E0
m68k_03b9e0:
        move.w #0x2700,%sr
m68k_03b9e0_end:
.org 0x3B9E4
m68k_03b9e4:
        lea.l 0x465c5:l,%a0
m68k_03b9e4_end:
.org 0x3B9EA
m68k_03b9ea:
        lea.l 0xe000:l,%a1
m68k_03b9ea_end:
.org 0x3B9F0
m68k_03b9f0:
        move.l #0x80,%d5
m68k_03b9f0_end:
.org 0x3B9F6
m68k_03b9f6:
        move.w #0x12,%d6
m68k_03b9f6_end:
.org 0x3B9FA
m68k_03b9fa:
        jsr -3886(%pc)
m68k_03b9fa_end:
.org 0x3B9FE
m68k_03b9fe:
        move.w #0x0,0x8026:w
m68k_03b9fe_end:
.org 0x3BA04
m68k_03ba04:
        move.w #0x2500,%sr
m68k_03ba04_end:
.org 0x3BA08
m68k_03ba08:
        clr.w 0x813a:w
m68k_03ba08_end:
.org 0x3BA0C
m68k_03ba0c:
        addq.w #0x1,0x80ea:w
m68k_03ba0c_end:
.org 0x3BA10
m68k_03ba10:
        move.w #0x2700,%sr
m68k_03ba10_end:
.org 0x3BA14
m68k_03ba14:
        move.w #0x8f02,0xc00004:l
m68k_03ba14_end:
.org 0x3BA1C
m68k_03ba1c:
        move.l #0x60000002,0xc00004:l
m68k_03ba1c_end:
.org 0x3BA26
m68k_03ba26:
        lea.l 0xc00000:l,%a5
m68k_03ba26_end:
.org 0x3BA2C
m68k_03ba2c:
        move.w #0x3333,%d6
m68k_03ba2c_end:
.org 0x3BA30
m68k_03ba30:
        move.w #0xd7f,%d7
m68k_03ba30_end:
.org 0x3BA34
m68k_03ba34:
        move.w %d6,(%a5)
m68k_03ba34_end:
.org 0x3BA36
m68k_03ba36:
        dbra %d7,(. + -2)
m68k_03ba36_end:
.org 0x3BA3A
m68k_03ba3a:
        move.w #0xa000,0xff700c:l
m68k_03ba3a_end:
.org 0x3BA42
m68k_03ba42:
        move.l #0x3b55a,0xff700e:l
m68k_03ba42_end:
.org 0x3BA4C
m68k_03ba4c:
        move.w #0x2500,%sr
m68k_03ba4c_end:
.org 0x3BA50
m68k_03ba50:
        rts
m68k_03ba50_end:
.org 0x3BA52
m68k_03ba52:
        bsr.w (. + 94)
m68k_03ba52_end:
.org 0x3BA56
m68k_03ba56:
        bsr.w (. + 144)
m68k_03ba56_end:
.org 0x3BA5A
m68k_03ba5a:
        addq.w #0x1,0x813a:w
m68k_03ba5a_end:
.org 0x3BA5E
m68k_03ba5e:
        cmpi.w #0x200,0x813a:w
m68k_03ba5e_end:
.org 0x3BA64
m68k_03ba64:
        bcs.b (. + 74)
m68k_03ba64_end:
.org 0x3BA66
m68k_03ba66:
        move.w #0x2700,%sr
m68k_03ba66_end:
.org 0x3BA6A
m68k_03ba6a:
        move.w #0x8f02,0xc00004:l
m68k_03ba6a_end:
.org 0x3BA72
m68k_03ba72:
        move.l #0x60000002,0xc00004:l
m68k_03ba72_end:
.org 0x3BA7C
m68k_03ba7c:
        lea.l 0xc00000:l,%a5
m68k_03ba7c_end:
.org 0x3BA82
m68k_03ba82:
        move.w #0x3333,%d6
m68k_03ba82_end:
.org 0x3BA86
m68k_03ba86:
        move.w #0xd7f,%d7
m68k_03ba86_end:
.org 0x3BA8A
m68k_03ba8a:
        move.w %d6,(%a5)
m68k_03ba8a_end:
.org 0x3BA8C
m68k_03ba8c:
        dbra %d7,(. + -2)
m68k_03ba8c_end:
.org 0x3BA90
m68k_03ba90:
        move.w #0xa000,0xff700c:l
m68k_03ba90_end:
.org 0x3BA98
m68k_03ba98:
        move.l #0x3bb92,0xff700e:l
m68k_03ba98_end:
.org 0x3BAA2
m68k_03baa2:
        move.w #0x2500,%sr
m68k_03baa2_end:
.org 0x3BAA6
m68k_03baa6:
        clr.w 0x813a:w
m68k_03baa6_end:
.org 0x3BAAA
m68k_03baaa:
        addq.w #0x1,0x80ea:w
m68k_03baaa_end:
.org 0x3BAAE
m68k_03baae:
        rts
m68k_03baae_end:
.org 0x3BAB0
m68k_03bab0:
        addq.w #0x1,0x813c:w
m68k_03bab0_end:
.org 0x3BAB4
m68k_03bab4:
        move.w 0x813c:w,%d2
m68k_03bab4_end:
.org 0x3BAB8
m68k_03bab8:
        lsr.w #0x5,%d2
m68k_03bab8_end:
.org 0x3BABA
m68k_03baba:
        cmpi.w #0x2,%d2
m68k_03baba_end:
.org 0x3BABE
m68k_03babe:
        bls.b (. + 8)
m68k_03babe_end:
.org 0x3BAC0
m68k_03bac0:
        clr.w 0x813c:w
m68k_03bac0_end:
.org 0x3BAC4
m68k_03bac4:
        moveq #0,%d2
m68k_03bac4_end:
.org 0x3BAC6
m68k_03bac6:
        addi.w #0x9,%d2
m68k_03bac6_end:
.org 0x3BACA
m68k_03baca:
        move.w #0x80,%d0
m68k_03baca_end:
.org 0x3BACE
m68k_03bace:
        move.w #0xc0,%d1
m68k_03bace_end:
.org 0x3BAD2
m68k_03bad2:
        bsr.w (. + 240)
m68k_03bad2_end:
.org 0x3BAD6
m68k_03bad6:
        move.w #0x80,%d0
m68k_03bad6_end:
.org 0x3BADA
m68k_03bada:
        move.w #0xc0,%d1
m68k_03bada_end:
.org 0x3BADE
m68k_03bade:
        moveq #0,%d2
m68k_03bade_end:
.org 0x3BAE0
m68k_03bae0:
        bsr.w (. + 226)
m68k_03bae0_end:
.org 0x3BAE4
m68k_03bae4:
        rts
m68k_03bae4_end:
.org 0x3BAE6
m68k_03bae6:
        move.w 0x813e:w,%d0
m68k_03bae6_end:
.org 0x3BAEA
m68k_03baea:
        lsr.w #0x4,%d0
m68k_03baea_end:
.org 0x3BAEC
m68k_03baec:
        cmpi.w #0x6,%d0
m68k_03baec_end:
.org 0x3BAF0
m68k_03baf0:
        bcc.w (. + 32)
m68k_03baf0_end:
.org 0x3BAF4
m68k_03baf4:
        asl.w #0x1,%d0
m68k_03baf4_end:
.org 0x3BAF6
m68k_03baf6:
        move.w 12(%pc, %d0.w),0xfb1c:w
m68k_03baf6_end:
.org 0x3BAFC
m68k_03bafc:
        addi.w #0x1,0x813e:w
m68k_03bafc_end:
.org 0x3BB02
m68k_03bb02:
        rts
m68k_03bb02_end:
.org 0x3BB10
m68k_03bb10:
        cmpi.w #0xe,%d0
m68k_03bb10_end:
.org 0x3BB14
m68k_03bb14:
        bcc.w (. + 24)
m68k_03bb14_end:
.org 0x3BB18
m68k_03bb18:
        subi.w #0x6,%d0
m68k_03bb18_end:
.org 0x3BB1C
m68k_03bb1c:
        addi.w #0x9,%d0
m68k_03bb1c_end:
.org 0x3BB20
m68k_03bb20:
        jsr -3982(%pc)
m68k_03bb20_end:
.org 0x3BB24
m68k_03bb24:
        addi.w #0x1,0x813e:w
m68k_03bb24_end:
.org 0x3BB2A
m68k_03bb2a:
        rts
m68k_03bb2a_end:
.org 0x3BB2C
m68k_03bb2c:
        cmpi.w #0x50,0x8026:w
m68k_03bb2c_end:
.org 0x3BB32
m68k_03bb32:
        bcc.b (. + 34)
m68k_03bb32_end:
.org 0x3BB34
m68k_03bb34:
        move.w #0xeee,0xfb02:w
m68k_03bb34_end:
.org 0x3BB3A
m68k_03bb3a:
        move.w #0xec8,0xfb06:w
m68k_03bb3a_end:
.org 0x3BB40
m68k_03bb40:
        move.w #0xe86,0xfb1e:w
m68k_03bb40_end:
.org 0x3BB46
m68k_03bb46:
        move.w 0xf320:w,%d0
m68k_03bb46_end:
.org 0x3BB4A
m68k_03bb4a:
        andi.w #0x3,%d0
m68k_03bb4a_end:
.org 0x3BB4E
m68k_03bb4e:
        bne.b (. + 6)
m68k_03bb4e_end:
.org 0x3BB50
m68k_03bb50:
        addq.w #0x1,0x8026:w
m68k_03bb50_end:
.org 0x3BB54
m68k_03bb54:
        rts
m68k_03bb54_end:
.org 0x3BB56
m68k_03bb56:
        bsr.w (. + -166)
m68k_03bb56_end:
.org 0x3BB5A
m68k_03bb5a:
        bsr.w (. + -116)
m68k_03bb5a_end:
.org 0x3BB5E
m68k_03bb5e:
        addq.w #0x1,0x813a:w
m68k_03bb5e_end:
.org 0x3BB62
m68k_03bb62:
        cmpi.w #0x19c0,0x813a:w
m68k_03bb62_end:
.org 0x3BB68
m68k_03bb68:
        bcs.b (. + 40)
m68k_03bb68_end:
.org 0x3BB6A
m68k_03bb6a:
        move.w #0xffff,0x80ca:w
m68k_03bb6a_end:
.org 0x3BB70
m68k_03bb70:
        move.w #0xffff,0x80cc:w
m68k_03bb70_end:
.org 0x3BB76
m68k_03bb76:
        move.w #0xffff,0x80ce:w
m68k_03bb76_end:
.org 0x3BB7C
m68k_03bb7c:
        move.w #0xffff,0x80d0:w
m68k_03bb7c_end:
.org 0x3BB82
m68k_03bb82:
        moveq #1,%d0
m68k_03bb82_end:
.org 0x3BB84
m68k_03bb84:
        jsr -4430(%pc)
m68k_03bb84_end:
.org 0x3BB88
m68k_03bb88:
        clr.w 0x813a:w
m68k_03bb88_end:
.org 0x3BB8C
m68k_03bb8c:
        addq.w #0x1,0x80ea:w
m68k_03bb8c_end:
.org 0x3BB90
m68k_03bb90:
        rts
m68k_03bb90_end:
.org 0x3BBAC
m68k_03bbac:
        bsr.w (. + -252)
m68k_03bbac_end:
.org 0x3BBB0
m68k_03bbb0:
        btst.b #0x7,0x80c4:w
m68k_03bbb0_end:
.org 0x3BBB6
m68k_03bbb6:
        beq.w (. + 10)
m68k_03bbb6_end:
.org 0x3BBBA
m68k_03bbba:
        jmp 0x206:l
m68k_03bbba_end:
.org 0x3BBC0
m68k_03bbc0:
        rts
m68k_03bbc0_end:
.org 0x3BBC2
m68k_03bbc2:
        asl.w #0x2,%d2
m68k_03bbc2_end:
.org 0x3BBC4
m68k_03bbc4:
        movea.l 16(%pc, %d2.w),%a0
m68k_03bbc4_end:
.org 0x3BBC8
m68k_03bbc8:
        move.w #0x5,%d2
m68k_03bbc8_end:
.org 0x3BBCC
m68k_03bbcc:
        moveq #0,%d3
m68k_03bbcc_end:
.org 0x3BBCE
m68k_03bbce:
        move.w #0x100,%d4
m68k_03bbce_end:
.org 0x3BBD2
m68k_03bbd2:
        jmp -2712(%pc)
m68k_03bbd2_end:
.org 0x3C19C
m68k_03c19c:
        bra.w (. + 32)
m68k_03c19c_end:
.org 0x3C1A0
m68k_03c1a0:
        bra.w (. + 388)
m68k_03c1a0_end:
.org 0x3C1A4
m68k_03c1a4:
        bra.w (. + 610)
m68k_03c1a4_end:
.org 0x3C1A8
m68k_03c1a8:
        bra.w (. + 726)
m68k_03c1a8_end:
.org 0x3C1AC
m68k_03c1ac:
        bra.w (. + 796)
m68k_03c1ac_end:
.org 0x3C1B0
m68k_03c1b0:
        bra.w (. + 956)
m68k_03c1b0_end:
.org 0x3C1B4
m68k_03c1b4:
        bra.w (. + 1226)
m68k_03c1b4_end:
.org 0x3C1B8
m68k_03c1b8:
        bra.w (. + 1278)
m68k_03c1b8_end:
.org 0x3C1BC
m68k_03c1bc:
        move.w #0x2700,%sr
m68k_03c1bc_end:
.org 0x3C1C0
m68k_03c1c0:
        move.w #0xffff,0x80ca:w
m68k_03c1c0_end:
.org 0x3C1C6
m68k_03c1c6:
        move.w #0xffff,0x80cc:w
m68k_03c1c6_end:
.org 0x3C1CC
m68k_03c1cc:
        move.w #0xffff,0x80ce:w
m68k_03c1cc_end:
.org 0x3C1D2
m68k_03c1d2:
        move.w #0xffff,0x80d0:w
m68k_03c1d2_end:
.org 0x3C1D8
m68k_03c1d8:
        moveq #1,%d0
m68k_03c1d8_end:
.org 0x3C1DA
m68k_03c1da:
        jsr -6076(%pc)
m68k_03c1da_end:
.org 0x3C1DE
m68k_03c1de:
        bsr.w (. + 92)
m68k_03c1de_end:
.org 0x3C1E2
m68k_03c1e2:
        move.w #0x8f02,0xc00004:l
m68k_03c1e2_end:
.org 0x3C1EA
m68k_03c1ea:
        move.l #0x60000002,0xc00004:l
m68k_03c1ea_end:
.org 0x3C1F4
m68k_03c1f4:
        lea.l 0xc00000:l,%a5
m68k_03c1f4_end:
.org 0x3C1FA
m68k_03c1fa:
        move.w #0x3333,%d6
m68k_03c1fa_end:
.org 0x3C1FE
m68k_03c1fe:
        move.w #0xd7f,%d7
m68k_03c1fe_end:
.org 0x3C202
m68k_03c202:
        move.w %d6,(%a5)
m68k_03c202_end:
.org 0x3C204
m68k_03c204:
        dbra %d7,(. + -2)
m68k_03c204_end:
.org 0x3C208
m68k_03c208:
        move.w #0xa000,0xff700c:l
m68k_03c208_end:
.org 0x3C210
m68k_03c210:
        move.l #0x3b588,0xff700e:l
m68k_03c210_end:
.org 0x3C21A
m68k_03c21a:
        move.w #0x3,0xff7014:l
m68k_03c21a_end:
.org 0x3C222
m68k_03c222:
        move.w #0x1,0xff7016:l
m68k_03c222_end:
.org 0x3C22A
m68k_03c22a:
        move.w #0x3,0x813c:w
m68k_03c22a_end:
.org 0x3C230
m68k_03c230:
        addq.w #0x1,0x80ea:w
m68k_03c230_end:
.org 0x3C234
m68k_03c234:
        move.w #0x2500,%sr
m68k_03c234_end:
.org 0x3C238
m68k_03c238:
        rts
m68k_03c238_end:
.org 0x3C23A
m68k_03c23a:
        lea.l 104(%pc),%a2
m68k_03c23a_end:
.org 0x3C23E
m68k_03c23e:
        nop
m68k_03c23e_end:
.org 0x3C240
m68k_03c240:
        move.w #0xe820,%d0
m68k_03c240_end:
.org 0x3C244
m68k_03c244:
        bsr.w (. + 62)
m68k_03c244_end:
.org 0x3C248
m68k_03c248:
        move.w #0xe8a0,%d0
m68k_03c248_end:
.org 0x3C24C
m68k_03c24c:
        bsr.w (. + 54)
m68k_03c24c_end:
.org 0x3C250
m68k_03c250:
        move.w #0xe920,%d0
m68k_03c250_end:
.org 0x3C254
m68k_03c254:
        bsr.w (. + 46)
m68k_03c254_end:
.org 0x3C258
m68k_03c258:
        move.w #0xe9a0,%d0
m68k_03c258_end:
.org 0x3C25C
m68k_03c25c:
        bsr.w (. + 38)
m68k_03c25c_end:
.org 0x3C260
m68k_03c260:
        move.w #0xea20,%d0
m68k_03c260_end:
.org 0x3C264
m68k_03c264:
        bsr.w (. + 30)
m68k_03c264_end:
.org 0x3C268
m68k_03c268:
        move.w #0xeaa0,%d0
m68k_03c268_end:
.org 0x3C26C
m68k_03c26c:
        bsr.w (. + 22)
m68k_03c26c_end:
.org 0x3C270
m68k_03c270:
        move.w #0xeb20,%d0
m68k_03c270_end:
.org 0x3C274
m68k_03c274:
        bsr.w (. + 14)
m68k_03c274_end:
.org 0x3C278
m68k_03c278:
        move.w #0xeba0,%d0
m68k_03c278_end:
.org 0x3C27C
m68k_03c27c:
        bsr.w (. + 6)
m68k_03c27c_end:
.org 0x3C280
m68k_03c280:
        rts
m68k_03c280_end:
.org 0x3C282
m68k_03c282:
        movem.l %a2,-(%a7)
m68k_03c282_end:
.org 0x3C286
m68k_03c286:
        move.w #0x8f02,0xc00004:l
m68k_03c286_end:
.org 0x3C28E
m68k_03c28e:
        bsr.w (. + -4062)
m68k_03c28e_end:
.org 0x3C292
m68k_03c292:
        movem.l (%a7)+,%a2
m68k_03c292_end:
.org 0x3C296
m68k_03c296:
        moveq #7,%d0
m68k_03c296_end:
.org 0x3C298
m68k_03c298:
        move.w (%a2)+,0xc00000:l
m68k_03c298_end:
.org 0x3C29E
m68k_03c29e:
        dbra %d0,(. + -6)
m68k_03c29e_end:
.org 0x3C2A2
m68k_03c2a2:
        rts
m68k_03c2a2_end:
.org 0x3C324
m68k_03c324:
        bsr.w (. + 128)
m68k_03c324_end:
.org 0x3C328
m68k_03c328:
        cmpi.w #0x200,0x813a:w
m68k_03c328_end:
.org 0x3C32E
m68k_03c32e:
        bne.b (. + 66)
m68k_03c32e_end:
.org 0x3C330
m68k_03c330:
        move.w #0x2700,%sr
m68k_03c330_end:
.org 0x3C334
m68k_03c334:
        move.w #0x8f02,0xc00004:l
m68k_03c334_end:
.org 0x3C33C
m68k_03c33c:
        move.l #0x60000002,0xc00004:l
m68k_03c33c_end:
.org 0x3C346
m68k_03c346:
        lea.l 0xc00000:l,%a5
m68k_03c346_end:
.org 0x3C34C
m68k_03c34c:
        move.w #0x3333,%d6
m68k_03c34c_end:
.org 0x3C350
m68k_03c350:
        move.w #0xd7f,%d7
m68k_03c350_end:
.org 0x3C354
m68k_03c354:
        move.w %d6,(%a5)
m68k_03c354_end:
.org 0x3C356
m68k_03c356:
        dbra %d7,(. + -2)
m68k_03c356_end:
.org 0x3C35A
m68k_03c35a:
        move.w #0xa000,0xff700c:l
m68k_03c35a_end:
.org 0x3C362
m68k_03c362:
        move.l #0x3b59e,0xff700e:l
m68k_03c362_end:
.org 0x3C36C
m68k_03c36c:
        move.w #0x2500,%sr
m68k_03c36c_end:
.org 0x3C370
m68k_03c370:
        addq.w #0x1,0x813a:w
m68k_03c370_end:
.org 0x3C374
m68k_03c374:
        cmpi.w #0x200,0x813a:w
m68k_03c374_end:
.org 0x3C37A
m68k_03c37a:
        bcs.b (. + 40)
m68k_03c37a_end:
.org 0x3C37C
m68k_03c37c:
        move.w #0xffff,0x80ca:w
m68k_03c37c_end:
.org 0x3C382
m68k_03c382:
        move.w #0xffff,0x80cc:w
m68k_03c382_end:
.org 0x3C388
m68k_03c388:
        move.w #0x0,0x80ce:w
m68k_03c388_end:
.org 0x3C38E
m68k_03c38e:
        move.w #0xffff,0x80d0:w
m68k_03c38e_end:
.org 0x3C394
m68k_03c394:
        moveq #1,%d0
m68k_03c394_end:
.org 0x3C396
m68k_03c396:
        jsr -6496(%pc)
m68k_03c396_end:
.org 0x3C39A
m68k_03c39a:
        clr.w 0x813a:w
m68k_03c39a_end:
.org 0x3C39E
m68k_03c39e:
        addq.w #0x1,0x80ea:w
m68k_03c39e_end:
.org 0x3C3A2
m68k_03c3a2:
        rts
m68k_03c3a2_end:
.org 0x3C3A4
m68k_03c3a4:
        addq.w #0x1,0x813c:w
m68k_03c3a4_end:
.org 0x3C3A8
m68k_03c3a8:
        move.w 0x813c:w,%d2
m68k_03c3a8_end:
.org 0x3C3AC
m68k_03c3ac:
        lsr.w #0x6,%d2
m68k_03c3ac_end:
.org 0x3C3AE
m68k_03c3ae:
        move.w #0xb0,%d1
m68k_03c3ae_end:
.org 0x3C3B2
m68k_03c3b2:
        sub.w %d2,%d1
m68k_03c3b2_end:
.org 0x3C3B4
m68k_03c3b4:
        move.w #0x80,%d0
m68k_03c3b4_end:
.org 0x3C3B8
m68k_03c3b8:
        move.w #0x0,%d2
m68k_03c3b8_end:
.org 0x3C3BC
m68k_03c3bc:
        move.w #0x200,%d4
m68k_03c3bc_end:
.org 0x3C3C0
m68k_03c3c0:
        bsr.w (. + 780)
m68k_03c3c0_end:
.org 0x3C3C4
m68k_03c3c4:
        addq.w #0x1,0x813e:w
m68k_03c3c4_end:
.org 0x3C3C8
m68k_03c3c8:
        move.w 0x813c:w,%d2
m68k_03c3c8_end:
.org 0x3C3CC
m68k_03c3cc:
        lsr.w #0x5,%d2
m68k_03c3cc_end:
.org 0x3C3CE
m68k_03c3ce:
        move.w #0xb0,%d1
m68k_03c3ce_end:
.org 0x3C3D2
m68k_03c3d2:
        sub.w %d2,%d1
m68k_03c3d2_end:
.org 0x3C3D4
m68k_03c3d4:
        move.w #0x80,%d0
m68k_03c3d4_end:
.org 0x3C3D8
m68k_03c3d8:
        move.w #0x1,%d2
m68k_03c3d8_end:
.org 0x3C3DC
m68k_03c3dc:
        move.w #0x200,%d4
m68k_03c3dc_end:
.org 0x3C3E0
m68k_03c3e0:
        bsr.w (. + 748)
m68k_03c3e0_end:
.org 0x3C3E4
m68k_03c3e4:
        addq.w #0x1,0x8140:w
m68k_03c3e4_end:
.org 0x3C3E8
m68k_03c3e8:
        move.w 0x813c:w,%d2
m68k_03c3e8_end:
.org 0x3C3EC
m68k_03c3ec:
        lsr.w #0x4,%d2
m68k_03c3ec_end:
.org 0x3C3EE
m68k_03c3ee:
        move.w #0xb0,%d1
m68k_03c3ee_end:
.org 0x3C3F2
m68k_03c3f2:
        sub.w %d2,%d1
m68k_03c3f2_end:
.org 0x3C3F4
m68k_03c3f4:
        move.w #0x80,%d0
m68k_03c3f4_end:
.org 0x3C3F8
m68k_03c3f8:
        move.w #0x2,%d2
m68k_03c3f8_end:
.org 0x3C3FC
m68k_03c3fc:
        move.w #0x200,%d4
m68k_03c3fc_end:
.org 0x3C400
m68k_03c400:
        bsr.w (. + 716)
m68k_03c400_end:
.org 0x3C404
m68k_03c404:
        rts
m68k_03c404_end:
.org 0x3C406
m68k_03c406:
        bsr.w (. + -98)
m68k_03c406_end:
.org 0x3C40A
m68k_03c40a:
        btst.b #0x7,0x80c4:w
m68k_03c40a_end:
.org 0x3C410
m68k_03c410:
        beq.w (. + 108)
m68k_03c410_end:
.org 0x3C414
m68k_03c414:
        move.w #0x2700,%sr
m68k_03c414_end:
.org 0x3C418
m68k_03c418:
        lea.l 0x46fcd:l,%a0
m68k_03c418_end:
.org 0x3C41E
m68k_03c41e:
        lea.l 0xe000:l,%a1
m68k_03c41e_end:
.org 0x3C424
m68k_03c424:
        move.l #0x80,%d5
m68k_03c424_end:
.org 0x3C42A
m68k_03c42a:
        move.w #0x12,%d6
m68k_03c42a_end:
.org 0x3C42E
m68k_03c42e:
        jsr -6498(%pc)
m68k_03c42e_end:
.org 0x3C432
m68k_03c432:
        move.w #0x8f02,0xc00004:l
m68k_03c432_end:
.org 0x3C43A
m68k_03c43a:
        move.l #0x60000002,0xc00004:l
m68k_03c43a_end:
.org 0x3C444
m68k_03c444:
        lea.l 0xc00000:l,%a5
m68k_03c444_end:
.org 0x3C44A
m68k_03c44a:
        move.w #0x3333,%d6
m68k_03c44a_end:
.org 0x3C44E
m68k_03c44e:
        move.w #0xd7f,%d7
m68k_03c44e_end:
.org 0x3C452
m68k_03c452:
        move.w %d6,(%a5)
m68k_03c452_end:
.org 0x3C454
m68k_03c454:
        dbra %d7,(. + -2)
m68k_03c454_end:
.org 0x3C458
m68k_03c458:
        move.w #0xa000,0xff700c:l
m68k_03c458_end:
.org 0x3C460
m68k_03c460:
        move.l #0x3b5b8,0xff700e:l
m68k_03c460_end:
.org 0x3C46A
m68k_03c46a:
        move.w #0x2500,%sr
m68k_03c46a_end:
.org 0x3C46E
m68k_03c46e:
        moveq #1,%d0
m68k_03c46e_end:
.org 0x3C470
m68k_03c470:
        jsr -6738(%pc)
m68k_03c470_end:
.org 0x3C474
m68k_03c474:
        clr.w 0x813a:w
m68k_03c474_end:
.org 0x3C478
m68k_03c478:
        addq.w #0x1,0x80ea:w
m68k_03c478_end:
.org 0x3C47C
m68k_03c47c:
        rts
m68k_03c47c_end:
.org 0x3C47E
m68k_03c47e:
        bsr.w (. + 32)
m68k_03c47e_end:
.org 0x3C482
m68k_03c482:
        addq.w #0x1,0x813a:w
m68k_03c482_end:
.org 0x3C486
m68k_03c486:
        cmpi.w #0x200,0x813a:w
m68k_03c486_end:
.org 0x3C48C
m68k_03c48c:
        bcs.b (. + 16)
m68k_03c48c_end:
.org 0x3C48E
m68k_03c48e:
        moveq #1,%d0
m68k_03c48e_end:
.org 0x3C490
m68k_03c490:
        jsr -6746(%pc)
m68k_03c490_end:
.org 0x3C494
m68k_03c494:
        clr.w 0x813a:w
m68k_03c494_end:
.org 0x3C498
m68k_03c498:
        addq.w #0x1,0x80ea:w
m68k_03c498_end:
.org 0x3C49C
m68k_03c49c:
        rts
m68k_03c49c_end:
.org 0x3C49E
m68k_03c49e:
        addq.w #0x1,0x813c:w
m68k_03c49e_end:
.org 0x3C4A2
m68k_03c4a2:
        move.w 0x813c:w,%d2
m68k_03c4a2_end:
.org 0x3C4A6
m68k_03c4a6:
        lsr.w #0x5,%d2
m68k_03c4a6_end:
.org 0x3C4A8
m68k_03c4a8:
        cmpi.w #0x5,%d2
m68k_03c4a8_end:
.org 0x3C4AC
m68k_03c4ac:
        bls.b (. + 8)
m68k_03c4ac_end:
.org 0x3C4AE
m68k_03c4ae:
        clr.w 0x813c:w
m68k_03c4ae_end:
.org 0x3C4B2
m68k_03c4b2:
        moveq #0,%d2
m68k_03c4b2_end:
.org 0x3C4B4
m68k_03c4b4:
        addq.w #0x3,%d2
m68k_03c4b4_end:
.org 0x3C4B6
m68k_03c4b6:
        move.w #0x80,%d0
m68k_03c4b6_end:
.org 0x3C4BA
m68k_03c4ba:
        move.w #0xc0,%d1
m68k_03c4ba_end:
.org 0x3C4BE
m68k_03c4be:
        move.w #0x100,%d4
m68k_03c4be_end:
.org 0x3C4C2
m68k_03c4c2:
        bsr.w (. + 522)
m68k_03c4c2_end:
.org 0x3C4C6
m68k_03c4c6:
        rts
m68k_03c4c6_end:
.org 0x3C4C8
m68k_03c4c8:
        bsr.w (. + -42)
m68k_03c4c8_end:
.org 0x3C4CC
m68k_03c4cc:
        btst.b #0x7,0x80c4:w
m68k_03c4cc_end:
.org 0x3C4D2
m68k_03c4d2:
        beq.w (. + 152)
m68k_03c4d2_end:
.org 0x3C4D6
m68k_03c4d6:
        move.w #0x2700,%sr
m68k_03c4d6_end:
.org 0x3C4DA
m68k_03c4da:
        lea.l 0x47248:l,%a0
m68k_03c4da_end:
.org 0x3C4E0
m68k_03c4e0:
        lea.l 0xe000:l,%a1
m68k_03c4e0_end:
.org 0x3C4E6
m68k_03c4e6:
        move.l #0x80,%d5
m68k_03c4e6_end:
.org 0x3C4EC
m68k_03c4ec:
        move.w #0x12,%d6
m68k_03c4ec_end:
.org 0x3C4F0
m68k_03c4f0:
        jsr -6692(%pc)
m68k_03c4f0_end:
.org 0x3C4F4
m68k_03c4f4:
        move.w #0x8f02,0xc00004:l
m68k_03c4f4_end:
.org 0x3C4FC
m68k_03c4fc:
        move.l #0x60000002,0xc00004:l
m68k_03c4fc_end:
.org 0x3C506
m68k_03c506:
        lea.l 0xc00000:l,%a5
m68k_03c506_end:
.org 0x3C50C
m68k_03c50c:
        move.w #0x3333,%d6
m68k_03c50c_end:
.org 0x3C510
m68k_03c510:
        move.w #0xd7f,%d7
m68k_03c510_end:
.org 0x3C514
m68k_03c514:
        move.w %d6,(%a5)
m68k_03c514_end:
.org 0x3C516
m68k_03c516:
        dbra %d7,(. + -2)
m68k_03c516_end:
.org 0x3C51A
m68k_03c51a:
        move.w #0xa000,0xff700c:l
m68k_03c51a_end:
.org 0x3C522
m68k_03c522:
        move.l #0x3b5e8,0xff700e:l
m68k_03c522_end:
.org 0x3C52C
m68k_03c52c:
        move.w #0x2500,%sr
m68k_03c52c_end:
.org 0x3C530
m68k_03c530:
        move.w #0xffff,0x80ca:w
m68k_03c530_end:
.org 0x3C536
m68k_03c536:
        move.w #0xffff,0x80cc:w
m68k_03c536_end:
.org 0x3C53C
m68k_03c53c:
        move.w #0x0,0x80ce:w
m68k_03c53c_end:
.org 0x3C542
m68k_03c542:
        move.w #0xffff,0x80d0:w
m68k_03c542_end:
.org 0x3C548
m68k_03c548:
        moveq #1,%d0
m68k_03c548_end:
.org 0x3C54A
m68k_03c54a:
        jsr -6956(%pc)
m68k_03c54a_end:
.org 0x3C54E
m68k_03c54e:
        clr.w 0x813a:w
m68k_03c54e_end:
.org 0x3C552
m68k_03c552:
        clr.w 0x813c:w
m68k_03c552_end:
.org 0x3C556
m68k_03c556:
        clr.w 0x813e:w
m68k_03c556_end:
.org 0x3C55A
m68k_03c55a:
        clr.w 0x8140:w
m68k_03c55a_end:
.org 0x3C55E
m68k_03c55e:
        clr.w 0x8142:w
m68k_03c55e_end:
.org 0x3C562
m68k_03c562:
        clr.w 0x8144:w
m68k_03c562_end:
.org 0x3C566
m68k_03c566:
        addq.w #0x1,0x80ea:w
m68k_03c566_end:
.org 0x3C56A
m68k_03c56a:
        rts
m68k_03c56a_end:
.org 0x3C56C
m68k_03c56c:
        bsr.w (. + 90)
m68k_03c56c_end:
.org 0x3C570
m68k_03c570:
        addq.w #0x1,0x813a:w
m68k_03c570_end:
.org 0x3C574
m68k_03c574:
        cmpi.w #0x200,0x813a:w
m68k_03c574_end:
.org 0x3C57A
m68k_03c57a:
        bcs.b (. + 74)
m68k_03c57a_end:
.org 0x3C57C
m68k_03c57c:
        move.w #0x2700,%sr
m68k_03c57c_end:
.org 0x3C580
m68k_03c580:
        move.w #0x8f02,0xc00004:l
m68k_03c580_end:
.org 0x3C588
m68k_03c588:
        move.l #0x60000002,0xc00004:l
m68k_03c588_end:
.org 0x3C592
m68k_03c592:
        lea.l 0xc00000:l,%a5
m68k_03c592_end:
.org 0x3C598
m68k_03c598:
        move.w #0x3333,%d6
m68k_03c598_end:
.org 0x3C59C
m68k_03c59c:
        move.w #0xd7f,%d7
m68k_03c59c_end:
.org 0x3C5A0
m68k_03c5a0:
        move.w %d6,(%a5)
m68k_03c5a0_end:
.org 0x3C5A2
m68k_03c5a2:
        dbra %d7,(. + -2)
m68k_03c5a2_end:
.org 0x3C5A6
m68k_03c5a6:
        move.w #0xa000,0xff700c:l
m68k_03c5a6_end:
.org 0x3C5AE
m68k_03c5ae:
        move.l #0x3bb92,0xff700e:l
m68k_03c5ae_end:
.org 0x3C5B8
m68k_03c5b8:
        move.w #0x2500,%sr
m68k_03c5b8_end:
.org 0x3C5BC
m68k_03c5bc:
        clr.w 0x813a:w
m68k_03c5bc_end:
.org 0x3C5C0
m68k_03c5c0:
        addq.w #0x1,0x80ea:w
m68k_03c5c0_end:
.org 0x3C5C4
m68k_03c5c4:
        rts
m68k_03c5c4_end:
.org 0x3C5C6
m68k_03c5c6:
        move.w 0x8144:w,%d2
m68k_03c5c6_end:
.org 0x3C5CA
m68k_03c5ca:
        lsr.w #0x3,%d2
m68k_03c5ca_end:
.org 0x3C5CC
m68k_03c5cc:
        move.w #0xe0,%d1
m68k_03c5cc_end:
.org 0x3C5D0
m68k_03c5d0:
        sub.w %d2,%d1
m68k_03c5d0_end:
.org 0x3C5D2
m68k_03c5d2:
        cmpi.w #0xc0,%d1
m68k_03c5d2_end:
.org 0x3C5D6
m68k_03c5d6:
        bhi.b (. + 8)
m68k_03c5d6_end:
.org 0x3C5D8
m68k_03c5d8:
        move.w #0xc0,%d1
m68k_03c5d8_end:
.org 0x3C5DC
m68k_03c5dc:
        bra.b (. + 6)
m68k_03c5dc_end:
.org 0x3C5DE
m68k_03c5de:
        addq.w #0x1,0x8144:w
m68k_03c5de_end:
.org 0x3C5E2
m68k_03c5e2:
        move.w #0x80,%d0
m68k_03c5e2_end:
.org 0x3C5E6
m68k_03c5e6:
        move.w #0xd,%d2
m68k_03c5e6_end:
.org 0x3C5EA
m68k_03c5ea:
        move.w #0x100,%d4
m68k_03c5ea_end:
.org 0x3C5EE
m68k_03c5ee:
        bsr.w (. + 222)
m68k_03c5ee_end:
.org 0x3C5F2
m68k_03c5f2:
        move.w 0x8142:w,%d1
m68k_03c5f2_end:
.org 0x3C5F6
m68k_03c5f6:
        lsr.w #0x3,%d1
m68k_03c5f6_end:
.org 0x3C5F8
m68k_03c5f8:
        addi.w #0xa0,%d1
m68k_03c5f8_end:
.org 0x3C5FC
m68k_03c5fc:
        cmpi.w #0xc0,%d1
m68k_03c5fc_end:
.org 0x3C600
m68k_03c600:
        bcs.b (. + 8)
m68k_03c600_end:
.org 0x3C602
m68k_03c602:
        move.w #0xc0,%d1
m68k_03c602_end:
.org 0x3C606
m68k_03c606:
        bra.b (. + 6)
m68k_03c606_end:
.org 0x3C608
m68k_03c608:
        addq.w #0x1,0x8142:w
m68k_03c608_end:
.org 0x3C60C
m68k_03c60c:
        move.w #0x80,%d0
m68k_03c60c_end:
.org 0x3C610
m68k_03c610:
        move.w #0xc,%d2
m68k_03c610_end:
.org 0x3C614
m68k_03c614:
        move.w #0x200,%d4
m68k_03c614_end:
.org 0x3C618
m68k_03c618:
        bsr.w (. + 180)
m68k_03c618_end:
.org 0x3C61C
m68k_03c61c:
        addq.w #0x1,0x813c:w
m68k_03c61c_end:
.org 0x3C620
m68k_03c620:
        move.w 0x813c:w,%d2
m68k_03c620_end:
.org 0x3C624
m68k_03c624:
        lsr.w #0x6,%d2
m68k_03c624_end:
.org 0x3C626
m68k_03c626:
        move.w #0xc0,%d1
m68k_03c626_end:
.org 0x3C62A
m68k_03c62a:
        sub.w %d2,%d1
m68k_03c62a_end:
.org 0x3C62C
m68k_03c62c:
        move.w #0x80,%d0
m68k_03c62c_end:
.org 0x3C630
m68k_03c630:
        move.w #0x9,%d2
m68k_03c630_end:
.org 0x3C634
m68k_03c634:
        move.w #0x200,%d4
m68k_03c634_end:
.org 0x3C638
m68k_03c638:
        bsr.w (. + 148)
m68k_03c638_end:
.org 0x3C63C
m68k_03c63c:
        addq.w #0x1,0x813e:w
m68k_03c63c_end:
.org 0x3C640
m68k_03c640:
        move.w 0x813e:w,%d2
m68k_03c640_end:
.org 0x3C644
m68k_03c644:
        lsr.w #0x5,%d2
m68k_03c644_end:
.org 0x3C646
m68k_03c646:
        move.w #0xc0,%d1
m68k_03c646_end:
.org 0x3C64A
m68k_03c64a:
        sub.w %d2,%d1
m68k_03c64a_end:
.org 0x3C64C
m68k_03c64c:
        move.w #0x80,%d0
m68k_03c64c_end:
.org 0x3C650
m68k_03c650:
        move.w #0xa,%d2
m68k_03c650_end:
.org 0x3C654
m68k_03c654:
        move.w #0x200,%d4
m68k_03c654_end:
.org 0x3C658
m68k_03c658:
        bsr.w (. + 116)
m68k_03c658_end:
.org 0x3C65C
m68k_03c65c:
        addq.w #0x1,0x8140:w
m68k_03c65c_end:
.org 0x3C660
m68k_03c660:
        move.w 0x8140:w,%d2
m68k_03c660_end:
.org 0x3C664
m68k_03c664:
        lsr.w #0x4,%d2
m68k_03c664_end:
.org 0x3C666
m68k_03c666:
        move.w #0xc0,%d1
m68k_03c666_end:
.org 0x3C66A
m68k_03c66a:
        sub.w %d2,%d1
m68k_03c66a_end:
.org 0x3C66C
m68k_03c66c:
        move.w #0x80,%d0
m68k_03c66c_end:
.org 0x3C670
m68k_03c670:
        move.w #0xb,%d2
m68k_03c670_end:
.org 0x3C674
m68k_03c674:
        move.w #0x200,%d4
m68k_03c674_end:
.org 0x3C678
m68k_03c678:
        bsr.w (. + 84)
m68k_03c678_end:
.org 0x3C67C
m68k_03c67c:
        rts
m68k_03c67c_end:
.org 0x3C67E
m68k_03c67e:
        bsr.w (. + -184)
m68k_03c67e_end:
.org 0x3C682
m68k_03c682:
        addq.w #0x1,0x813a:w
m68k_03c682_end:
.org 0x3C686
m68k_03c686:
        cmpi.w #0x1b80,0x813a:w
m68k_03c686_end:
.org 0x3C68C
m68k_03c68c:
        bcs.b (. + 40)
m68k_03c68c_end:
.org 0x3C68E
m68k_03c68e:
        move.w #0xffff,0x80ca:w
m68k_03c68e_end:
.org 0x3C694
m68k_03c694:
        move.w #0xffff,0x80cc:w
m68k_03c694_end:
.org 0x3C69A
m68k_03c69a:
        move.w #0xffff,0x80ce:w
m68k_03c69a_end:
.org 0x3C6A0
m68k_03c6a0:
        move.w #0xffff,0x80d0:w
m68k_03c6a0_end:
.org 0x3C6A6
m68k_03c6a6:
        moveq #1,%d0
m68k_03c6a6_end:
.org 0x3C6A8
m68k_03c6a8:
        jsr -7282(%pc)
m68k_03c6a8_end:
.org 0x3C6AC
m68k_03c6ac:
        clr.w 0x813a:w
m68k_03c6ac_end:
.org 0x3C6B0
m68k_03c6b0:
        addq.w #0x1,0x80ea:w
m68k_03c6b0_end:
.org 0x3C6B4
m68k_03c6b4:
        rts
m68k_03c6b4_end:
.org 0x3C6B6
m68k_03c6b6:
        bsr.w (. + -240)
m68k_03c6b6_end:
.org 0x3C6BA
m68k_03c6ba:
        btst.b #0x7,0x80c4:w
m68k_03c6ba_end:
.org 0x3C6C0
m68k_03c6c0:
        beq.w (. + 10)
m68k_03c6c0_end:
.org 0x3C6C4
m68k_03c6c4:
        jmp 0x206:l
m68k_03c6c4_end:
.org 0x3C6CA
m68k_03c6ca:
        rts
m68k_03c6ca_end:
.org 0x3C6CC
m68k_03c6cc:
        asl.w #0x2,%d2
m68k_03c6cc_end:
.org 0x3C6CE
m68k_03c6ce:
        movea.l 12(%pc, %d2.w),%a0
m68k_03c6ce_end:
.org 0x3C6D2
m68k_03c6d2:
        move.w #0x5,%d2
m68k_03c6d2_end:
.org 0x3C6D6
m68k_03c6d6:
        moveq #0,%d3
m68k_03c6d6_end:
.org 0x3C6D8
m68k_03c6d8:
        jmp -5534(%pc)
m68k_03c6d8_end:
.org 0x3C97A
m68k_03c97a:
        bra.w (. + 12)
m68k_03c97a_end:
.org 0x3C97E
m68k_03c97e:
        bra.w (. + 134)
m68k_03c97e_end:
.org 0x3C982
m68k_03c982:
        bra.w (. + 258)
m68k_03c982_end:
.org 0x3C986
m68k_03c986:
        move.w #0x2700,%sr
m68k_03c986_end:
.org 0x3C98A
m68k_03c98a:
        move.w #0xffff,0x80ca:w
m68k_03c98a_end:
.org 0x3C990
m68k_03c990:
        move.w #0xffff,0x80cc:w
m68k_03c990_end:
.org 0x3C996
m68k_03c996:
        move.w #0xffff,0x80ce:w
m68k_03c996_end:
.org 0x3C99C
m68k_03c99c:
        move.w #0xffff,0x80d0:w
m68k_03c99c_end:
.org 0x3C9A2
m68k_03c9a2:
        moveq #1,%d0
m68k_03c9a2_end:
.org 0x3C9A4
m68k_03c9a4:
        jsr -8070(%pc)
m68k_03c9a4_end:
.org 0x3C9A8
m68k_03c9a8:
        bsr.w (. + -1902)
m68k_03c9a8_end:
.org 0x3C9AC
m68k_03c9ac:
        move.w #0x8f02,0xc00004:l
m68k_03c9ac_end:
.org 0x3C9B4
m68k_03c9b4:
        move.l #0x60000002,0xc00004:l
m68k_03c9b4_end:
.org 0x3C9BE
m68k_03c9be:
        lea.l 0xc00000:l,%a5
m68k_03c9be_end:
.org 0x3C9C4
m68k_03c9c4:
        move.w #0x3333,%d6
m68k_03c9c4_end:
.org 0x3C9C8
m68k_03c9c8:
        move.w #0xd7f,%d7
m68k_03c9c8_end:
.org 0x3C9CC
m68k_03c9cc:
        move.w %d6,(%a5)
m68k_03c9cc_end:
.org 0x3C9CE
m68k_03c9ce:
        dbra %d7,(. + -2)
m68k_03c9ce_end:
.org 0x3C9D2
m68k_03c9d2:
        move.w #0xa000,0xff700c:l
m68k_03c9d2_end:
.org 0x3C9DA
m68k_03c9da:
        move.l #0x3b6e4,0xff700e:l
m68k_03c9da_end:
.org 0x3C9E4
m68k_03c9e4:
        move.w #0x3,0xff7014:l
m68k_03c9e4_end:
.org 0x3C9EC
m68k_03c9ec:
        move.w #0x1,0xff7016:l
m68k_03c9ec_end:
.org 0x3C9F4
m68k_03c9f4:
        move.w #0x3,0x813c:w
m68k_03c9f4_end:
.org 0x3C9FA
m68k_03c9fa:
        addq.w #0x1,0x80ea:w
m68k_03c9fa_end:
.org 0x3C9FE
m68k_03c9fe:
        move.w #0x2500,%sr
m68k_03c9fe_end:
.org 0x3CA02
m68k_03ca02:
        rts
m68k_03ca02_end:
.org 0x3CA04
m68k_03ca04:
        bsr.w (. + -1632)
m68k_03ca04_end:
.org 0x3CA08
m68k_03ca08:
        cmpi.w #0x100,0x813a:w
m68k_03ca08_end:
.org 0x3CA0E
m68k_03ca0e:
        bne.b (. + 66)
m68k_03ca0e_end:
.org 0x3CA10
m68k_03ca10:
        move.w #0x2700,%sr
m68k_03ca10_end:
.org 0x3CA14
m68k_03ca14:
        move.w #0x8f02,0xc00004:l
m68k_03ca14_end:
.org 0x3CA1C
m68k_03ca1c:
        move.l #0x60000002,0xc00004:l
m68k_03ca1c_end:
.org 0x3CA26
m68k_03ca26:
        lea.l 0xc00000:l,%a5
m68k_03ca26_end:
.org 0x3CA2C
m68k_03ca2c:
        move.w #0x3333,%d6
m68k_03ca2c_end:
.org 0x3CA30
m68k_03ca30:
        move.w #0xd7f,%d7
m68k_03ca30_end:
.org 0x3CA34
m68k_03ca34:
        move.w %d6,(%a5)
m68k_03ca34_end:
.org 0x3CA36
m68k_03ca36:
        dbra %d7,(. + -2)
m68k_03ca36_end:
.org 0x3CA3A
m68k_03ca3a:
        move.w #0xa000,0xff700c:l
m68k_03ca3a_end:
.org 0x3CA42
m68k_03ca42:
        move.l #0x3b6fa,0xff700e:l
m68k_03ca42_end:
.org 0x3CA4C
m68k_03ca4c:
        move.w #0x2500,%sr
m68k_03ca4c_end:
.org 0x3CA50
m68k_03ca50:
        addq.w #0x1,0x813a:w
m68k_03ca50_end:
.org 0x3CA54
m68k_03ca54:
        cmpi.w #0x3c0,0x813a:w
m68k_03ca54_end:
.org 0x3CA5A
m68k_03ca5a:
        bcs.b (. + 40)
m68k_03ca5a_end:
.org 0x3CA5C
m68k_03ca5c:
        move.w #0xffff,0x80ca:w
m68k_03ca5c_end:
.org 0x3CA62
m68k_03ca62:
        move.w #0xffff,0x80cc:w
m68k_03ca62_end:
.org 0x3CA68
m68k_03ca68:
        move.w #0xffff,0x80ce:w
m68k_03ca68_end:
.org 0x3CA6E
m68k_03ca6e:
        move.w #0xffff,0x80d0:w
m68k_03ca6e_end:
.org 0x3CA74
m68k_03ca74:
        moveq #1,%d0
m68k_03ca74_end:
.org 0x3CA76
m68k_03ca76:
        jsr -8256(%pc)
m68k_03ca76_end:
.org 0x3CA7A
m68k_03ca7a:
        clr.w 0x813a:w
m68k_03ca7a_end:
.org 0x3CA7E
m68k_03ca7e:
        addq.w #0x1,0x80ea:w
m68k_03ca7e_end:
.org 0x3CA82
m68k_03ca82:
        rts
m68k_03ca82_end:
.org 0x3CA84
m68k_03ca84:
        bsr.w (. + -1760)
m68k_03ca84_end:
.org 0x3CA88
m68k_03ca88:
        btst.b #0x7,0x80c4:w
m68k_03ca88_end:
.org 0x3CA8E
m68k_03ca8e:
        beq.w (. + 10)
m68k_03ca8e_end:
.org 0x3CA92
m68k_03ca92:
        jmp 0x206:l
m68k_03ca92_end:
.org 0x3CA98
m68k_03ca98:
        rts
m68k_03ca98_end:
.org 0x3CAA4
m68k_03caa4:
        bra.w (. + 32)
m68k_03caa4_end:
.org 0x3CAA8
m68k_03caa8:
        bra.w (. + 150)
m68k_03caa8_end:
.org 0x3CAAC
m68k_03caac:
        bra.w (. + 310)
m68k_03caac_end:
.org 0x3CAB0
m68k_03cab0:
        bra.w (. + 430)
m68k_03cab0_end:
.org 0x3CAB4
m68k_03cab4:
        bra.w (. + 506)
m68k_03cab4_end:
.org 0x3CAB8
m68k_03cab8:
        bra.w (. + 646)
m68k_03cab8_end:
.org 0x3CABC
m68k_03cabc:
        bra.w (. + 770)
m68k_03cabc_end:
.org 0x3CAC0
m68k_03cac0:
        bra.w (. + 822)
m68k_03cac0_end:
.org 0x3CAC4
m68k_03cac4:
        move.w #0x2700,%sr
m68k_03cac4_end:
.org 0x3CAC8
m68k_03cac8:
        move.w #0xffff,0x80ca:w
m68k_03cac8_end:
.org 0x3CACE
m68k_03cace:
        move.w #0xffff,0x80cc:w
m68k_03cace_end:
.org 0x3CAD4
m68k_03cad4:
        move.w #0xffff,0x80ce:w
m68k_03cad4_end:
.org 0x3CADA
m68k_03cada:
        move.w #0xffff,0x80d0:w
m68k_03cada_end:
.org 0x3CAE0
m68k_03cae0:
        moveq #1,%d0
m68k_03cae0_end:
.org 0x3CAE2
m68k_03cae2:
        jsr -8388(%pc)
m68k_03cae2_end:
.org 0x3CAE6
m68k_03cae6:
        move.w #0x8f02,0xc00004:l
m68k_03cae6_end:
.org 0x3CAEE
m68k_03caee:
        move.l #0x60000002,0xc00004:l
m68k_03caee_end:
.org 0x3CAF8
m68k_03caf8:
        lea.l 0xc00000:l,%a5
m68k_03caf8_end:
.org 0x3CAFE
m68k_03cafe:
        move.w #0x3333,%d6
m68k_03cafe_end:
.org 0x3CB02
m68k_03cb02:
        move.w #0xd7f,%d7
m68k_03cb02_end:
.org 0x3CB06
m68k_03cb06:
        move.w %d6,(%a5)
m68k_03cb06_end:
.org 0x3CB08
m68k_03cb08:
        dbra %d7,(. + -2)
m68k_03cb08_end:
.org 0x3CB0C
m68k_03cb0c:
        move.w #0xa000,0xff700c:l
m68k_03cb0c_end:
.org 0x3CB14
m68k_03cb14:
        move.l #0x3b614,0xff700e:l
m68k_03cb14_end:
.org 0x3CB1E
m68k_03cb1e:
        move.w #0x3,0xff7014:l
m68k_03cb1e_end:
.org 0x3CB26
m68k_03cb26:
        move.w #0x1,0xff7016:l
m68k_03cb26_end:
.org 0x3CB2E
m68k_03cb2e:
        move.w #0x3,0x813c:w
m68k_03cb2e_end:
.org 0x3CB34
m68k_03cb34:
        addq.w #0x1,0x80ea:w
m68k_03cb34_end:
.org 0x3CB38
m68k_03cb38:
        move.w #0x2500,%sr
m68k_03cb38_end:
.org 0x3CB3C
m68k_03cb3c:
        rts
m68k_03cb3c_end:
.org 0x3CB3E
m68k_03cb3e:
        bsr.w (. + 128)
m68k_03cb3e_end:
.org 0x3CB42
m68k_03cb42:
        cmpi.w #0x200,0x813a:w
m68k_03cb42_end:
.org 0x3CB48
m68k_03cb48:
        bne.b (. + 66)
m68k_03cb48_end:
.org 0x3CB4A
m68k_03cb4a:
        move.w #0x2700,%sr
m68k_03cb4a_end:
.org 0x3CB4E
m68k_03cb4e:
        move.w #0x8f02,0xc00004:l
m68k_03cb4e_end:
.org 0x3CB56
m68k_03cb56:
        move.l #0x60000002,0xc00004:l
m68k_03cb56_end:
.org 0x3CB60
m68k_03cb60:
        lea.l 0xc00000:l,%a5
m68k_03cb60_end:
.org 0x3CB66
m68k_03cb66:
        move.w #0x3333,%d6
m68k_03cb66_end:
.org 0x3CB6A
m68k_03cb6a:
        move.w #0xd7f,%d7
m68k_03cb6a_end:
.org 0x3CB6E
m68k_03cb6e:
        move.w %d6,(%a5)
m68k_03cb6e_end:
.org 0x3CB70
m68k_03cb70:
        dbra %d7,(. + -2)
m68k_03cb70_end:
.org 0x3CB74
m68k_03cb74:
        move.w #0xa000,0xff700c:l
m68k_03cb74_end:
.org 0x3CB7C
m68k_03cb7c:
        move.l #0x3b630,0xff700e:l
m68k_03cb7c_end:
.org 0x3CB86
m68k_03cb86:
        move.w #0x2500,%sr
m68k_03cb86_end:
.org 0x3CB8A
m68k_03cb8a:
        addq.w #0x1,0x813a:w
m68k_03cb8a_end:
.org 0x3CB8E
m68k_03cb8e:
        cmpi.w #0x200,0x813a:w
m68k_03cb8e_end:
.org 0x3CB94
m68k_03cb94:
        bcs.b (. + 40)
m68k_03cb94_end:
.org 0x3CB96
m68k_03cb96:
        move.w #0xffff,0x80ca:w
m68k_03cb96_end:
.org 0x3CB9C
m68k_03cb9c:
        move.w #0xffff,0x80cc:w
m68k_03cb9c_end:
.org 0x3CBA2
m68k_03cba2:
        move.w #0x0,0x80ce:w
m68k_03cba2_end:
.org 0x3CBA8
m68k_03cba8:
        move.w #0xffff,0x80d0:w
m68k_03cba8_end:
.org 0x3CBAE
m68k_03cbae:
        moveq #1,%d0
m68k_03cbae_end:
.org 0x3CBB0
m68k_03cbb0:
        jsr -8570(%pc)
m68k_03cbb0_end:
.org 0x3CBB4
m68k_03cbb4:
        clr.w 0x813a:w
m68k_03cbb4_end:
.org 0x3CBB8
m68k_03cbb8:
        addq.w #0x1,0x80ea:w
m68k_03cbb8_end:
.org 0x3CBBC
m68k_03cbbc:
        rts
m68k_03cbbc_end:
.org 0x3CBBE
m68k_03cbbe:
        addq.w #0x1,0x813c:w
m68k_03cbbe_end:
.org 0x3CBC2
m68k_03cbc2:
        move.w 0x813c:w,%d2
m68k_03cbc2_end:
.org 0x3CBC6
m68k_03cbc6:
        lsr.w #0x5,%d2
m68k_03cbc6_end:
.org 0x3CBC8
m68k_03cbc8:
        cmpi.w #0x3,%d2
m68k_03cbc8_end:
.org 0x3CBCC
m68k_03cbcc:
        bls.b (. + 8)
m68k_03cbcc_end:
.org 0x3CBCE
m68k_03cbce:
        clr.w 0x813c:w
m68k_03cbce_end:
.org 0x3CBD2
m68k_03cbd2:
        moveq #0,%d2
m68k_03cbd2_end:
.org 0x3CBD4
m68k_03cbd4:
        move.w #0x80,%d0
m68k_03cbd4_end:
.org 0x3CBD8
m68k_03cbd8:
        move.w #0xc0,%d1
m68k_03cbd8_end:
.org 0x3CBDC
m68k_03cbdc:
        bsr.w (. + 556)
m68k_03cbdc_end:
.org 0x3CBE0
m68k_03cbe0:
        rts
m68k_03cbe0_end:
.org 0x3CBE2
m68k_03cbe2:
        bsr.w (. + -36)
m68k_03cbe2_end:
.org 0x3CBE6
m68k_03cbe6:
        btst.b #0x7,0x80c4:w
m68k_03cbe6_end:
.org 0x3CBEC
m68k_03cbec:
        beq.w (. + 112)
m68k_03cbec_end:
.org 0x3CBF0
m68k_03cbf0:
        move.w #0x2700,%sr
m68k_03cbf0_end:
.org 0x3CBF4
m68k_03cbf4:
        lea.l 0x45ae1:l,%a0
m68k_03cbf4_end:
.org 0x3CBFA
m68k_03cbfa:
        lea.l 0xe000:l,%a1
m68k_03cbfa_end:
.org 0x3CC00
m68k_03cc00:
        move.l #0x80,%d5
m68k_03cc00_end:
.org 0x3CC06
m68k_03cc06:
        move.w #0x12,%d6
m68k_03cc06_end:
.org 0x3CC0A
m68k_03cc0a:
        jsr -8522(%pc)
m68k_03cc0a_end:
.org 0x3CC0E
m68k_03cc0e:
        move.w #0x8f02,0xc00004:l
m68k_03cc0e_end:
.org 0x3CC16
m68k_03cc16:
        move.l #0x60000002,0xc00004:l
m68k_03cc16_end:
.org 0x3CC20
m68k_03cc20:
        lea.l 0xc00000:l,%a5
m68k_03cc20_end:
.org 0x3CC26
m68k_03cc26:
        move.w #0x3333,%d6
m68k_03cc26_end:
.org 0x3CC2A
m68k_03cc2a:
        move.w #0xd7f,%d7
m68k_03cc2a_end:
.org 0x3CC2E
m68k_03cc2e:
        move.w %d6,(%a5)
m68k_03cc2e_end:
.org 0x3CC30
m68k_03cc30:
        dbra %d7,(. + -2)
m68k_03cc30_end:
.org 0x3CC34
m68k_03cc34:
        move.w #0xa000,0xff700c:l
m68k_03cc34_end:
.org 0x3CC3C
m68k_03cc3c:
        move.l #0x3b654,0xff700e:l
m68k_03cc3c_end:
.org 0x3CC46
m68k_03cc46:
        move.w #0x2500,%sr
m68k_03cc46_end:
.org 0x3CC4A
m68k_03cc4a:
        moveq #1,%d0
m68k_03cc4a_end:
.org 0x3CC4C
m68k_03cc4c:
        jsr -8750(%pc)
m68k_03cc4c_end:
.org 0x3CC50
m68k_03cc50:
        clr.w 0x813a:w
m68k_03cc50_end:
.org 0x3CC54
m68k_03cc54:
        clr.w 0x813c:w
m68k_03cc54_end:
.org 0x3CC58
m68k_03cc58:
        addq.w #0x1,0x80ea:w
m68k_03cc58_end:
.org 0x3CC5C
m68k_03cc5c:
        rts
m68k_03cc5c_end:
.org 0x3CC5E
m68k_03cc5e:
        bsr.w (. + 36)
m68k_03cc5e_end:
.org 0x3CC62
m68k_03cc62:
        addq.w #0x1,0x813a:w
m68k_03cc62_end:
.org 0x3CC66
m68k_03cc66:
        cmpi.w #0x200,0x813a:w
m68k_03cc66_end:
.org 0x3CC6C
m68k_03cc6c:
        bcs.b (. + 20)
m68k_03cc6c_end:
.org 0x3CC6E
m68k_03cc6e:
        moveq #1,%d0
m68k_03cc6e_end:
.org 0x3CC70
m68k_03cc70:
        jsr -8762(%pc)
m68k_03cc70_end:
.org 0x3CC74
m68k_03cc74:
        clr.w 0x813a:w
m68k_03cc74_end:
.org 0x3CC78
m68k_03cc78:
        clr.w 0x813c:w
m68k_03cc78_end:
.org 0x3CC7C
m68k_03cc7c:
        addq.w #0x1,0x80ea:w
m68k_03cc7c_end:
.org 0x3CC80
m68k_03cc80:
        rts
m68k_03cc80_end:
.org 0x3CC82
m68k_03cc82:
        addq.w #0x1,0x813c:w
m68k_03cc82_end:
.org 0x3CC86
m68k_03cc86:
        move.w 0x813c:w,%d2
m68k_03cc86_end:
.org 0x3CC8A
m68k_03cc8a:
        lsr.w #0x5,%d2
m68k_03cc8a_end:
.org 0x3CC8C
m68k_03cc8c:
        move.w #0x80,%d0
m68k_03cc8c_end:
.org 0x3CC90
m68k_03cc90:
        move.w #0xc0,%d1
m68k_03cc90_end:
.org 0x3CC94
m68k_03cc94:
        sub.w %d2,%d0
m68k_03cc94_end:
.org 0x3CC96
m68k_03cc96:
        sub.w %d2,%d1
m68k_03cc96_end:
.org 0x3CC98
m68k_03cc98:
        moveq #4,%d2
m68k_03cc98_end:
.org 0x3CC9A
m68k_03cc9a:
        bsr.w (. + 366)
m68k_03cc9a_end:
.org 0x3CC9E
m68k_03cc9e:
        move.w #0x80,%d0
m68k_03cc9e_end:
.org 0x3CCA2
m68k_03cca2:
        move.w #0xc0,%d1
m68k_03cca2_end:
.org 0x3CCA6
m68k_03cca6:
        moveq #8,%d2
m68k_03cca6_end:
.org 0x3CCA8
m68k_03cca8:
        bsr.w (. + 352)
m68k_03cca8_end:
.org 0x3CCAC
m68k_03ccac:
        rts
m68k_03ccac_end:
.org 0x3CCAE
m68k_03ccae:
        bsr.w (. + -44)
m68k_03ccae_end:
.org 0x3CCB2
m68k_03ccb2:
        btst.b #0x7,0x80c4:w
m68k_03ccb2_end:
.org 0x3CCB8
m68k_03ccb8:
        beq.w (. + 132)
m68k_03ccb8_end:
.org 0x3CCBC
m68k_03ccbc:
        move.w #0x2700,%sr
m68k_03ccbc_end:
.org 0x3CCC0
m68k_03ccc0:
        lea.l 0x45d70:l,%a0
m68k_03ccc0_end:
.org 0x3CCC6
m68k_03ccc6:
        lea.l 0xe000:l,%a1
m68k_03ccc6_end:
.org 0x3CCCC
m68k_03cccc:
        move.l #0x80,%d5
m68k_03cccc_end:
.org 0x3CCD2
m68k_03ccd2:
        move.w #0x12,%d6
m68k_03ccd2_end:
.org 0x3CCD6
m68k_03ccd6:
        jsr -8714(%pc)
m68k_03ccd6_end:
.org 0x3CCDA
m68k_03ccda:
        move.w #0x8f02,0xc00004:l
m68k_03ccda_end:
.org 0x3CCE2
m68k_03cce2:
        move.l #0x60000002,0xc00004:l
m68k_03cce2_end:
.org 0x3CCEC
m68k_03ccec:
        lea.l 0xc00000:l,%a5
m68k_03ccec_end:
.org 0x3CCF2
m68k_03ccf2:
        move.w #0x3333,%d6
m68k_03ccf2_end:
.org 0x3CCF6
m68k_03ccf6:
        move.w #0xd7f,%d7
m68k_03ccf6_end:
.org 0x3CCFA
m68k_03ccfa:
        move.w %d6,(%a5)
m68k_03ccfa_end:
.org 0x3CCFC
m68k_03ccfc:
        dbra %d7,(. + -2)
m68k_03ccfc_end:
.org 0x3CD00
m68k_03cd00:
        move.w #0xa000,0xff700c:l
m68k_03cd00_end:
.org 0x3CD08
m68k_03cd08:
        move.l #0x3b684,0xff700e:l
m68k_03cd08_end:
.org 0x3CD12
m68k_03cd12:
        move.w #0x2500,%sr
m68k_03cd12_end:
.org 0x3CD16
m68k_03cd16:
        move.w #0xffff,0x80ca:w
m68k_03cd16_end:
.org 0x3CD1C
m68k_03cd1c:
        move.w #0xffff,0x80cc:w
m68k_03cd1c_end:
.org 0x3CD22
m68k_03cd22:
        move.w #0x0,0x80ce:w
m68k_03cd22_end:
.org 0x3CD28
m68k_03cd28:
        move.w #0xffff,0x80d0:w
m68k_03cd28_end:
.org 0x3CD2E
m68k_03cd2e:
        moveq #1,%d0
m68k_03cd2e_end:
.org 0x3CD30
m68k_03cd30:
        jsr -8978(%pc)
m68k_03cd30_end:
.org 0x3CD34
m68k_03cd34:
        clr.w 0x813a:w
m68k_03cd34_end:
.org 0x3CD38
m68k_03cd38:
        addq.w #0x1,0x80ea:w
m68k_03cd38_end:
.org 0x3CD3C
m68k_03cd3c:
        rts
m68k_03cd3c_end:
.org 0x3CD3E
m68k_03cd3e:
        bsr.w (. + 90)
m68k_03cd3e_end:
.org 0x3CD42
m68k_03cd42:
        addq.w #0x1,0x813a:w
m68k_03cd42_end:
.org 0x3CD46
m68k_03cd46:
        cmpi.w #0x200,0x813a:w
m68k_03cd46_end:
.org 0x3CD4C
m68k_03cd4c:
        bcs.b (. + 74)
m68k_03cd4c_end:
.org 0x3CD4E
m68k_03cd4e:
        move.w #0x2700,%sr
m68k_03cd4e_end:
.org 0x3CD52
m68k_03cd52:
        move.w #0x8f02,0xc00004:l
m68k_03cd52_end:
.org 0x3CD5A
m68k_03cd5a:
        move.l #0x60000002,0xc00004:l
m68k_03cd5a_end:
.org 0x3CD64
m68k_03cd64:
        lea.l 0xc00000:l,%a5
m68k_03cd64_end:
.org 0x3CD6A
m68k_03cd6a:
        move.w #0x3333,%d6
m68k_03cd6a_end:
.org 0x3CD6E
m68k_03cd6e:
        move.w #0xd7f,%d7
m68k_03cd6e_end:
.org 0x3CD72
m68k_03cd72:
        move.w %d6,(%a5)
m68k_03cd72_end:
.org 0x3CD74
m68k_03cd74:
        dbra %d7,(. + -2)
m68k_03cd74_end:
.org 0x3CD78
m68k_03cd78:
        move.w #0xa000,0xff700c:l
m68k_03cd78_end:
.org 0x3CD80
m68k_03cd80:
        move.l #0x3bb92,0xff700e:l
m68k_03cd80_end:
.org 0x3CD8A
m68k_03cd8a:
        move.w #0x2500,%sr
m68k_03cd8a_end:
.org 0x3CD8E
m68k_03cd8e:
        clr.w 0x813a:w
m68k_03cd8e_end:
.org 0x3CD92
m68k_03cd92:
        addq.w #0x1,0x80ea:w
m68k_03cd92_end:
.org 0x3CD96
m68k_03cd96:
        rts
m68k_03cd96_end:
.org 0x3CD98
m68k_03cd98:
        addq.w #0x1,0x813c:w
m68k_03cd98_end:
.org 0x3CD9C
m68k_03cd9c:
        move.w 0x813c:w,%d2
m68k_03cd9c_end:
.org 0x3CDA0
m68k_03cda0:
        lsr.w #0x5,%d2
m68k_03cda0_end:
.org 0x3CDA2
m68k_03cda2:
        cmpi.w #0x2,%d2
m68k_03cda2_end:
.org 0x3CDA6
m68k_03cda6:
        bls.b (. + 8)
m68k_03cda6_end:
.org 0x3CDA8
m68k_03cda8:
        clr.w 0x813c:w
m68k_03cda8_end:
.org 0x3CDAC
m68k_03cdac:
        moveq #0,%d2
m68k_03cdac_end:
.org 0x3CDAE
m68k_03cdae:
        addq.w #0x5,%d2
m68k_03cdae_end:
.org 0x3CDB0
m68k_03cdb0:
        move.w #0x80,%d0
m68k_03cdb0_end:
.org 0x3CDB4
m68k_03cdb4:
        move.w #0xc4,%d1
m68k_03cdb4_end:
.org 0x3CDB8
m68k_03cdb8:
        bsr.w (. + 80)
m68k_03cdb8_end:
.org 0x3CDBC
m68k_03cdbc:
        rts
m68k_03cdbc_end:
.org 0x3CDBE
m68k_03cdbe:
        bsr.w (. + -38)
m68k_03cdbe_end:
.org 0x3CDC2
m68k_03cdc2:
        addq.w #0x1,0x813a:w
m68k_03cdc2_end:
.org 0x3CDC6
m68k_03cdc6:
        cmpi.w #0x1b80,0x813a:w
m68k_03cdc6_end:
.org 0x3CDCC
m68k_03cdcc:
        bcs.b (. + 40)
m68k_03cdcc_end:
.org 0x3CDCE
m68k_03cdce:
        move.w #0xffff,0x80ca:w
m68k_03cdce_end:
.org 0x3CDD4
m68k_03cdd4:
        move.w #0xffff,0x80cc:w
m68k_03cdd4_end:
.org 0x3CDDA
m68k_03cdda:
        move.w #0xffff,0x80ce:w
m68k_03cdda_end:
.org 0x3CDE0
m68k_03cde0:
        move.w #0xffff,0x80d0:w
m68k_03cde0_end:
.org 0x3CDE6
m68k_03cde6:
        moveq #1,%d0
m68k_03cde6_end:
.org 0x3CDE8
m68k_03cde8:
        jsr -9138(%pc)
m68k_03cde8_end:
.org 0x3CDEC
m68k_03cdec:
        clr.w 0x813a:w
m68k_03cdec_end:
.org 0x3CDF0
m68k_03cdf0:
        addq.w #0x1,0x80ea:w
m68k_03cdf0_end:
.org 0x3CDF4
m68k_03cdf4:
        rts
m68k_03cdf4_end:
.org 0x3CDF6
m68k_03cdf6:
        btst.b #0x7,0x80c4:w
m68k_03cdf6_end:
.org 0x3CDFC
m68k_03cdfc:
        beq.w (. + 10)
m68k_03cdfc_end:
.org 0x3CE00
m68k_03ce00:
        jmp 0x206:l
m68k_03ce00_end:
.org 0x3CE06
m68k_03ce06:
        rts
m68k_03ce06_end:
.org 0x3CE08
m68k_03ce08:
        asl.w #0x2,%d2
m68k_03ce08_end:
.org 0x3CE0A
m68k_03ce0a:
        movea.l 16(%pc, %d2.w),%a0
m68k_03ce0a_end:
.org 0x3CE0E
m68k_03ce0e:
        move.w #0x5,%d2
m68k_03ce0e_end:
.org 0x3CE12
m68k_03ce12:
        moveq #0,%d3
m68k_03ce12_end:
.org 0x3CE14
m68k_03ce14:
        move.w #0x200,%d4
m68k_03ce14_end:
.org 0x3CE18
m68k_03ce18:
        jmp -7390(%pc)
m68k_03ce18_end:
.org 0x3D17C
m68k_03d17c:
        bra.w (. + 28)
m68k_03d17c_end:
.org 0x3D180
m68k_03d180:
        bra.w (. + 128)
m68k_03d180_end:
.org 0x3D184
m68k_03d184:
        bra.w (. + 284)
m68k_03d184_end:
.org 0x3D188
m68k_03d188:
        bra.w (. + 416)
m68k_03d188_end:
.org 0x3D18C
m68k_03d18c:
        bra.w (. + 486)
m68k_03d18c_end:
.org 0x3D190
m68k_03d190:
        bra.w (. + 596)
m68k_03d190_end:
.org 0x3D194
m68k_03d194:
        bra.w (. + 690)
m68k_03d194_end:
.org 0x3D198
m68k_03d198:
        move.w #0x2700,%sr
m68k_03d198_end:
.org 0x3D19C
m68k_03d19c:
        move.w #0xffff,0x80ca:w
m68k_03d19c_end:
.org 0x3D1A2
m68k_03d1a2:
        move.w #0xffff,0x80cc:w
m68k_03d1a2_end:
.org 0x3D1A8
m68k_03d1a8:
        move.w #0xffff,0x80ce:w
m68k_03d1a8_end:
.org 0x3D1AE
m68k_03d1ae:
        move.w #0xffff,0x80d0:w
m68k_03d1ae_end:
.org 0x3D1B4
m68k_03d1b4:
        moveq #1,%d0
m68k_03d1b4_end:
.org 0x3D1B6
m68k_03d1b6:
        jsr -10136(%pc)
m68k_03d1b6_end:
.org 0x3D1BA
m68k_03d1ba:
        move.w #0x8f02,0xc00004:l
m68k_03d1ba_end:
.org 0x3D1C2
m68k_03d1c2:
        move.l #0x60000002,0xc00004:l
m68k_03d1c2_end:
.org 0x3D1CC
m68k_03d1cc:
        lea.l 0xc00000:l,%a5
m68k_03d1cc_end:
.org 0x3D1D2
m68k_03d1d2:
        move.w #0x3333,%d6
m68k_03d1d2_end:
.org 0x3D1D6
m68k_03d1d6:
        move.w #0xd7f,%d7
m68k_03d1d6_end:
.org 0x3D1DA
m68k_03d1da:
        move.w %d6,(%a5)
m68k_03d1da_end:
.org 0x3D1DC
m68k_03d1dc:
        dbra %d7,(. + -2)
m68k_03d1dc_end:
.org 0x3D1E0
m68k_03d1e0:
        move.w #0x3,0xff7014:l
m68k_03d1e0_end:
.org 0x3D1E8
m68k_03d1e8:
        move.w #0x1,0xff7016:l
m68k_03d1e8_end:
.org 0x3D1F0
m68k_03d1f0:
        move.w #0x3,0x813c:w
m68k_03d1f0_end:
.org 0x3D1F6
m68k_03d1f6:
        addq.w #0x1,0x80ea:w
m68k_03d1f6_end:
.org 0x3D1FA
m68k_03d1fa:
        move.w #0x2500,%sr
m68k_03d1fa_end:
.org 0x3D1FE
m68k_03d1fe:
        rts
m68k_03d1fe_end:
.org 0x3D200
m68k_03d200:
        bsr.w (. + 128)
m68k_03d200_end:
.org 0x3D204
m68k_03d204:
        cmpi.w #0xc0,0x813a:w
m68k_03d204_end:
.org 0x3D20A
m68k_03d20a:
        bne.b (. + 66)
m68k_03d20a_end:
.org 0x3D20C
m68k_03d20c:
        move.w #0x2700,%sr
m68k_03d20c_end:
.org 0x3D210
m68k_03d210:
        move.w #0x8f02,0xc00004:l
m68k_03d210_end:
.org 0x3D218
m68k_03d218:
        move.l #0x60000002,0xc00004:l
m68k_03d218_end:
.org 0x3D222
m68k_03d222:
        lea.l 0xc00000:l,%a5
m68k_03d222_end:
.org 0x3D228
m68k_03d228:
        move.w #0x3333,%d6
m68k_03d228_end:
.org 0x3D22C
m68k_03d22c:
        move.w #0xd7f,%d7
m68k_03d22c_end:
.org 0x3D230
m68k_03d230:
        move.w %d6,(%a5)
m68k_03d230_end:
.org 0x3D232
m68k_03d232:
        dbra %d7,(. + -2)
m68k_03d232_end:
.org 0x3D236
m68k_03d236:
        move.w #0xa000,0xff700c:l
m68k_03d236_end:
.org 0x3D23E
m68k_03d23e:
        move.l #0x3b6a8,0xff700e:l
m68k_03d23e_end:
.org 0x3D248
m68k_03d248:
        move.w #0x2500,%sr
m68k_03d248_end:
.org 0x3D24C
m68k_03d24c:
        addq.w #0x1,0x813a:w
m68k_03d24c_end:
.org 0x3D250
m68k_03d250:
        cmpi.w #0x140,0x813a:w
m68k_03d250_end:
.org 0x3D256
m68k_03d256:
        bcs.b (. + 40)
m68k_03d256_end:
.org 0x3D258
m68k_03d258:
        move.w #0xffff,0x80ca:w
m68k_03d258_end:
.org 0x3D25E
m68k_03d25e:
        move.w #0xffff,0x80cc:w
m68k_03d25e_end:
.org 0x3D264
m68k_03d264:
        move.w #0x0,0x80ce:w
m68k_03d264_end:
.org 0x3D26A
m68k_03d26a:
        move.w #0xffff,0x80d0:w
m68k_03d26a_end:
.org 0x3D270
m68k_03d270:
        moveq #1,%d0
m68k_03d270_end:
.org 0x3D272
m68k_03d272:
        jsr -10300(%pc)
m68k_03d272_end:
.org 0x3D276
m68k_03d276:
        clr.w 0x813a:w
m68k_03d276_end:
.org 0x3D27A
m68k_03d27a:
        addq.w #0x1,0x80ea:w
m68k_03d27a_end:
.org 0x3D27E
m68k_03d27e:
        rts
m68k_03d27e_end:
.org 0x3D280
m68k_03d280:
        addq.w #0x1,0x813c:w
m68k_03d280_end:
.org 0x3D284
m68k_03d284:
        move.w 0x813c:w,%d2
m68k_03d284_end:
.org 0x3D288
m68k_03d288:
        lsr.w #0x5,%d2
m68k_03d288_end:
.org 0x3D28A
m68k_03d28a:
        cmpi.w #0x3,%d2
m68k_03d28a_end:
.org 0x3D28E
m68k_03d28e:
        bls.b (. + 4)
m68k_03d28e_end:
.org 0x3D290
m68k_03d290:
        moveq #3,%d2
m68k_03d290_end:
.org 0x3D292
m68k_03d292:
        move.w #0x80,%d0
m68k_03d292_end:
.org 0x3D296
m68k_03d296:
        move.w #0xc0,%d1
m68k_03d296_end:
.org 0x3D29A
m68k_03d29a:
        bsr.w (. + 450)
m68k_03d29a_end:
.org 0x3D29E
m68k_03d29e:
        rts
m68k_03d29e_end:
.org 0x3D2A0
m68k_03d2a0:
        bsr.w (. + -32)
m68k_03d2a0_end:
.org 0x3D2A4
m68k_03d2a4:
        btst.b #0x7,0x80c4:w
m68k_03d2a4_end:
.org 0x3D2AA
m68k_03d2aa:
        beq.w (. + 124)
m68k_03d2aa_end:
.org 0x3D2AE
m68k_03d2ae:
        move.w #0x2700,%sr
m68k_03d2ae_end:
.org 0x3D2B2
m68k_03d2b2:
        lea.l 0x4696b:l,%a0
m68k_03d2b2_end:
.org 0x3D2B8
m68k_03d2b8:
        lea.l 0xe000:l,%a1
m68k_03d2b8_end:
.org 0x3D2BE
m68k_03d2be:
        move.l #0x80,%d5
m68k_03d2be_end:
.org 0x3D2C4
m68k_03d2c4:
        move.w #0x12,%d6
m68k_03d2c4_end:
.org 0x3D2C8
m68k_03d2c8:
        jsr -10236(%pc)
m68k_03d2c8_end:
.org 0x3D2CC
m68k_03d2cc:
        move.w #0x8f02,0xc00004:l
m68k_03d2cc_end:
.org 0x3D2D4
m68k_03d2d4:
        move.l #0x60000002,0xc00004:l
m68k_03d2d4_end:
.org 0x3D2DE
m68k_03d2de:
        lea.l 0xc00000:l,%a5
m68k_03d2de_end:
.org 0x3D2E4
m68k_03d2e4:
        move.w #0x3333,%d6
m68k_03d2e4_end:
.org 0x3D2E8
m68k_03d2e8:
        move.w #0xd7f,%d7
m68k_03d2e8_end:
.org 0x3D2EC
m68k_03d2ec:
        move.w %d6,(%a5)
m68k_03d2ec_end:
.org 0x3D2EE
m68k_03d2ee:
        dbra %d7,(. + -2)
m68k_03d2ee_end:
.org 0x3D2F2
m68k_03d2f2:
        move.w #0xa000,0xff700c:l
m68k_03d2f2_end:
.org 0x3D2FA
m68k_03d2fa:
        move.l #0x3b6be,0xff700e:l
m68k_03d2fa_end:
.org 0x3D304
m68k_03d304:
        move.w #0x2500,%sr
m68k_03d304_end:
.org 0x3D308
m68k_03d308:
        moveq #1,%d0
m68k_03d308_end:
.org 0x3D30A
m68k_03d30a:
        jsr -10476(%pc)
m68k_03d30a_end:
.org 0x3D30E
m68k_03d30e:
        clr.w 0x813a:w
m68k_03d30e_end:
.org 0x3D312
m68k_03d312:
        clr.w 0x813c:w
m68k_03d312_end:
.org 0x3D316
m68k_03d316:
        addq.w #0x1,0x80ea:w
m68k_03d316_end:
.org 0x3D31A
m68k_03d31a:
        move.w #0x1f0,0x8020:w
m68k_03d31a_end:
.org 0x3D320
m68k_03d320:
        move.w #0x1f0,0x8026:w
m68k_03d320_end:
.org 0x3D326
m68k_03d326:
        rts
m68k_03d326_end:
.org 0x3D328
m68k_03d328:
        bsr.w (. + 30)
m68k_03d328_end:
.org 0x3D32C
m68k_03d32c:
        addq.w #0x1,0x813a:w
m68k_03d32c_end:
.org 0x3D330
m68k_03d330:
        cmpi.w #0x100,0x813a:w
m68k_03d330_end:
.org 0x3D336
m68k_03d336:
        bcs.b (. + 14)
m68k_03d336_end:
.org 0x3D338
m68k_03d338:
        clr.w 0x813a:w
m68k_03d338_end:
.org 0x3D33C
m68k_03d33c:
        clr.w 0x813c:w
m68k_03d33c_end:
.org 0x3D340
m68k_03d340:
        addq.w #0x1,0x80ea:w
m68k_03d340_end:
.org 0x3D344
m68k_03d344:
        rts
m68k_03d344_end:
.org 0x3D346
m68k_03d346:
        cmpi.w #0xa0,0x813c:w
m68k_03d346_end:
.org 0x3D34C
m68k_03d34c:
        bhi.w (. + 36)
m68k_03d34c_end:
.org 0x3D350
m68k_03d350:
        addq.w #0x2,0x813c:w
m68k_03d350_end:
.org 0x3D354
m68k_03d354:
        move.w #0x30,%d0
m68k_03d354_end:
.org 0x3D358
m68k_03d358:
        move.w #0xe0,%d1
m68k_03d358_end:
.org 0x3D35C
m68k_03d35c:
        add.w 0x813c:w,%d0
m68k_03d35c_end:
.org 0x3D360
m68k_03d360:
        sub.w 0x813c:w,%d1
m68k_03d360_end:
.org 0x3D364
m68k_03d364:
        add.w 0x8020:w,%d0
m68k_03d364_end:
.org 0x3D368
m68k_03d368:
        move.w #0x7,%d2
m68k_03d368_end:
.org 0x3D36C
m68k_03d36c:
        bsr.w (. + 240)
m68k_03d36c_end:
.org 0x3D370
m68k_03d370:
        rts
m68k_03d370_end:
.org 0x3D372
m68k_03d372:
        bsr.w (. + 170)
m68k_03d372_end:
.org 0x3D376
m68k_03d376:
        addq.w #0x1,0x8020:w
m68k_03d376_end:
.org 0x3D37A
m68k_03d37a:
        addq.w #0x1,0x8026:w
m68k_03d37a_end:
.org 0x3D37E
m68k_03d37e:
        andi.w #0x1ff,0x8020:w
m68k_03d37e_end:
.org 0x3D384
m68k_03d384:
        andi.w #0x1ff,0x8026:w
m68k_03d384_end:
.org 0x3D38A
m68k_03d38a:
        cmpi.w #0x100,0x8026:w
m68k_03d38a_end:
.org 0x3D390
m68k_03d390:
        bhi.b (. + -76)
m68k_03d390_end:
.org 0x3D392
m68k_03d392:
        cmpi.w #0x70,0x8026:w
m68k_03d392_end:
.org 0x3D398
m68k_03d398:
        bcs.b (. + -84)
m68k_03d398_end:
.org 0x3D39A
m68k_03d39a:
        clr.w 0x813a:w
m68k_03d39a_end:
.org 0x3D39E
m68k_03d39e:
        addq.w #0x1,0x80ea:w
m68k_03d39e_end:
.org 0x3D3A2
m68k_03d3a2:
        move.w #0x2700,%sr
m68k_03d3a2_end:
.org 0x3D3A6
m68k_03d3a6:
        move.w #0x8f02,0xc00004:l
m68k_03d3a6_end:
.org 0x3D3AE
m68k_03d3ae:
        move.l #0x60000002,0xc00004:l
m68k_03d3ae_end:
.org 0x3D3B8
m68k_03d3b8:
        lea.l 0xc00000:l,%a5
m68k_03d3b8_end:
.org 0x3D3BE
m68k_03d3be:
        move.w #0x3333,%d6
m68k_03d3be_end:
.org 0x3D3C2
m68k_03d3c2:
        move.w #0xd7f,%d7
m68k_03d3c2_end:
.org 0x3D3C6
m68k_03d3c6:
        move.w %d6,(%a5)
m68k_03d3c6_end:
.org 0x3D3C8
m68k_03d3c8:
        dbra %d7,(. + -2)
m68k_03d3c8_end:
.org 0x3D3CC
m68k_03d3cc:
        move.w #0xa000,0xff700c:l
m68k_03d3cc_end:
.org 0x3D3D4
m68k_03d3d4:
        move.l #0x3b6ce,0xff700e:l
m68k_03d3d4_end:
.org 0x3D3DE
m68k_03d3de:
        move.w #0x2500,%sr
m68k_03d3de_end:
.org 0x3D3E2
m68k_03d3e2:
        rts
m68k_03d3e2_end:
.org 0x3D3E4
m68k_03d3e4:
        bsr.w (. + 56)
m68k_03d3e4_end:
.org 0x3D3E8
m68k_03d3e8:
        addq.w #0x1,0x813a:w
m68k_03d3e8_end:
.org 0x3D3EC
m68k_03d3ec:
        cmpi.w #0x3c0,0x813a:w
m68k_03d3ec_end:
.org 0x3D3F2
m68k_03d3f2:
        bcs.b (. + 40)
m68k_03d3f2_end:
.org 0x3D3F4
m68k_03d3f4:
        move.w #0xffff,0x80ca:w
m68k_03d3f4_end:
.org 0x3D3FA
m68k_03d3fa:
        move.w #0xffff,0x80cc:w
m68k_03d3fa_end:
.org 0x3D400
m68k_03d400:
        move.w #0xffff,0x80ce:w
m68k_03d400_end:
.org 0x3D406
m68k_03d406:
        move.w #0xffff,0x80d0:w
m68k_03d406_end:
.org 0x3D40C
m68k_03d40c:
        moveq #1,%d0
m68k_03d40c_end:
.org 0x3D40E
m68k_03d40e:
        jsr -10712(%pc)
m68k_03d40e_end:
.org 0x3D412
m68k_03d412:
        clr.w 0x813a:w
m68k_03d412_end:
.org 0x3D416
m68k_03d416:
        addq.w #0x1,0x80ea:w
m68k_03d416_end:
.org 0x3D41A
m68k_03d41a:
        rts
m68k_03d41a_end:
.org 0x3D41C
m68k_03d41c:
        addq.w #0x1,0x813c:w
m68k_03d41c_end:
.org 0x3D420
m68k_03d420:
        move.w 0x813c:w,%d2
m68k_03d420_end:
.org 0x3D424
m68k_03d424:
        lsr.w #0x4,%d2
m68k_03d424_end:
.org 0x3D426
m68k_03d426:
        cmpi.w #0x1,%d2
m68k_03d426_end:
.org 0x3D42A
m68k_03d42a:
        bls.b (. + 8)
m68k_03d42a_end:
.org 0x3D42C
m68k_03d42c:
        moveq #0,%d2
m68k_03d42c_end:
.org 0x3D42E
m68k_03d42e:
        clr.w 0x813c:w
m68k_03d42e_end:
.org 0x3D432
m68k_03d432:
        addq.w #0x5,%d2
m68k_03d432_end:
.org 0x3D434
m68k_03d434:
        move.w #0xc0,%d0
m68k_03d434_end:
.org 0x3D438
m68k_03d438:
        move.w #0xc0,%d1
m68k_03d438_end:
.org 0x3D43C
m68k_03d43c:
        move.w #0x200,%d4
m68k_03d43c_end:
.org 0x3D440
m68k_03d440:
        bsr.w (. + 32)
m68k_03d440_end:
.org 0x3D444
m68k_03d444:
        rts
m68k_03d444_end:
.org 0x3D446
m68k_03d446:
        bsr.w (. + -42)
m68k_03d446_end:
.org 0x3D44A
m68k_03d44a:
        btst.b #0x7,0x80c4:w
m68k_03d44a_end:
.org 0x3D450
m68k_03d450:
        beq.w (. + 10)
m68k_03d450_end:
.org 0x3D454
m68k_03d454:
        jmp 0x206:l
m68k_03d454_end:
.org 0x3D45A
m68k_03d45a:
        rts
m68k_03d45a_end:
.org 0x3D45C
m68k_03d45c:
        move.w #0x100,%d4
m68k_03d45c_end:
.org 0x3D460
m68k_03d460:
        asl.w #0x2,%d2
m68k_03d460_end:
.org 0x3D462
m68k_03d462:
        movea.l 12(%pc, %d2.w),%a0
m68k_03d462_end:
.org 0x3D466
m68k_03d466:
        move.w #0x5,%d2
m68k_03d466_end:
.org 0x3D46A
m68k_03d46a:
        moveq #0,%d3
m68k_03d46a_end:
.org 0x3D46C
m68k_03d46c:
        jmp -9010(%pc)
m68k_03d46c_end:
.org 0x41BEE
m68k_041bee:
        bra.w (. + 20)
m68k_041bee_end:
.org 0x41BF2
m68k_041bf2:
        bra.w (. + 36)
m68k_041bf2_end:
.org 0x41BF6
m68k_041bf6:
        bra.w (. + 80)
m68k_041bf6_end:
.org 0x41BFA
m68k_041bfa:
        bra.w (. + 124)
m68k_041bfa_end:
.org 0x41BFE
m68k_041bfe:
        bra.w (. + 168)
m68k_041bfe_end:
.org 0x41C02
m68k_041c02:
        move.w #0x5,0x812a:w
m68k_041c02_end:
.org 0x41C08
m68k_041c08:
        move.w #0x5,0x812c:w
m68k_041c08_end:
.org 0x41C0E
m68k_041c0e:
        move.w #0x5,0x812e:w
m68k_041c0e_end:
.org 0x41C14
m68k_041c14:
        rts
m68k_041c14_end:
.org 0x41C16
m68k_041c16:
        cmpi.w #0x4,0x8160:w
m68k_041c16_end:
.org 0x41C1C
m68k_041c1c:
        bcs.b (. + 22)
m68k_041c1c_end:
.org 0x41C1E
m68k_041c1e:
        move.w #0x5,0x812a:w
m68k_041c1e_end:
.org 0x41C24
m68k_041c24:
        move.w #0x5,0x812c:w
m68k_041c24_end:
.org 0x41C2A
m68k_041c2a:
        move.w #0x5,0x812e:w
m68k_041c2a_end:
.org 0x41C30
m68k_041c30:
        rts
m68k_041c30_end:
.org 0x41C32
m68k_041c32:
        move.w #0x1,0x812a:w
m68k_041c32_end:
.org 0x41C38
m68k_041c38:
        move.w #0x1,0x812c:w
m68k_041c38_end:
.org 0x41C3E
m68k_041c3e:
        move.w #0x1,0x812e:w
m68k_041c3e_end:
.org 0x41C44
m68k_041c44:
        rts
m68k_041c44_end:
.org 0x41C46
m68k_041c46:
        cmpi.w #0x5,0x8160:w
m68k_041c46_end:
.org 0x41C4C
m68k_041c4c:
        bcs.b (. + 22)
m68k_041c4c_end:
.org 0x41C4E
m68k_041c4e:
        move.w #0x5,0x812a:w
m68k_041c4e_end:
.org 0x41C54
m68k_041c54:
        move.w #0x5,0x812c:w
m68k_041c54_end:
.org 0x41C5A
m68k_041c5a:
        move.w #0x5,0x812e:w
m68k_041c5a_end:
.org 0x41C60
m68k_041c60:
        rts
m68k_041c60_end:
.org 0x41C62
m68k_041c62:
        move.w #0x1,0x812a:w
m68k_041c62_end:
.org 0x41C68
m68k_041c68:
        move.w #0x1,0x812c:w
m68k_041c68_end:
.org 0x41C6E
m68k_041c6e:
        move.w #0x4,0x812e:w
m68k_041c6e_end:
.org 0x41C74
m68k_041c74:
        rts
m68k_041c74_end:
.org 0x41C76
m68k_041c76:
        cmpi.w #0x5,0x8160:w
m68k_041c76_end:
.org 0x41C7C
m68k_041c7c:
        bcs.b (. + 22)
m68k_041c7c_end:
.org 0x41C7E
m68k_041c7e:
        move.w #0x5,0x812a:w
m68k_041c7e_end:
.org 0x41C84
m68k_041c84:
        move.w #0x5,0x812c:w
m68k_041c84_end:
.org 0x41C8A
m68k_041c8a:
        move.w #0x5,0x812e:w
m68k_041c8a_end:
.org 0x41C90
m68k_041c90:
        rts
m68k_041c90_end:
.org 0x41C92
m68k_041c92:
        move.w #0x1,0x812a:w
m68k_041c92_end:
.org 0x41C98
m68k_041c98:
        move.w #0x1,0x812c:w
m68k_041c98_end:
.org 0x41C9E
m68k_041c9e:
        move.w #0x1,0x812e:w
m68k_041c9e_end:
.org 0x41CA4
m68k_041ca4:
        rts
m68k_041ca4_end:
.org 0x41CA6
m68k_041ca6:
        cmpi.w #0x6,0x8160:w
m68k_041ca6_end:
.org 0x41CAC
m68k_041cac:
        bcs.b (. + 22)
m68k_041cac_end:
.org 0x41CAE
m68k_041cae:
        move.w #0x5,0x812a:w
m68k_041cae_end:
.org 0x41CB4
m68k_041cb4:
        move.w #0x5,0x812c:w
m68k_041cb4_end:
.org 0x41CBA
m68k_041cba:
        move.w #0x5,0x812e:w
m68k_041cba_end:
.org 0x41CC0
m68k_041cc0:
        rts
m68k_041cc0_end:
.org 0x41CC2
m68k_041cc2:
        move.w #0x4,0x812a:w
m68k_041cc2_end:
.org 0x41CC8
m68k_041cc8:
        move.w #0x4,0x812c:w
m68k_041cc8_end:
.org 0x41CCE
m68k_041cce:
        move.w #0x4,0x812e:w
m68k_041cce_end:
.org 0x41CD4
m68k_041cd4:
        rts
m68k_041cd4_end:
.org 0x41CEA
m68k_041cea:
        bra.w (. + 20)
m68k_041cea_end:
.org 0x41CEE
m68k_041cee:
        bra.w (. + 80)
m68k_041cee_end:
.org 0x41CF2
m68k_041cf2:
        bra.w (. + 138)
m68k_041cf2_end:
.org 0x41CF6
m68k_041cf6:
        bra.w (. + 8)
m68k_041cf6_end:
.org 0x41CFA
m68k_041cfa:
        bra.w (. + 164)
m68k_041cfa_end:
.org 0x41CFE
m68k_041cfe:
        cmpi.w #0x6,0x8160:w
m68k_041cfe_end:
.org 0x41D04
m68k_041d04:
        bcs.b (. + 34)
m68k_041d04_end:
.org 0x41D06
m68k_041d06:
        move.w #0x5,0x8130:w
m68k_041d06_end:
.org 0x41D0C
m68k_041d0c:
        cmpi.w #0x28,0x8178:w
m68k_041d0c_end:
.org 0x41D12
m68k_041d12:
        bhi.b (. + 42)
m68k_041d12_end:
.org 0x41D14
m68k_041d14:
        jsr -26100(%pc)
m68k_041d14_end:
.org 0x41D18
m68k_041d18:
        andi.w #0x7,%d0
m68k_041d18_end:
.org 0x41D1C
m68k_041d1c:
        beq.b (. + 32)
m68k_041d1c_end:
.org 0x41D1E
m68k_041d1e:
        move.w #0x4,0x8130:w
m68k_041d1e_end:
.org 0x41D24
m68k_041d24:
        rts
m68k_041d24_end:
.org 0x41D26
m68k_041d26:
        move.w #0x4,0x8130:w
m68k_041d26_end:
.org 0x41D2C
m68k_041d2c:
        jsr -26124(%pc)
m68k_041d2c_end:
.org 0x41D30
m68k_041d30:
        andi.w #0x3,%d0
m68k_041d30_end:
.org 0x41D34
m68k_041d34:
        bne.b (. + 8)
m68k_041d34_end:
.org 0x41D36
m68k_041d36:
        move.w #0x5,0x8130:w
m68k_041d36_end:
.org 0x41D3E
m68k_041d3e:
        move.w #0x4,0x8130:w
m68k_041d3e_end:
.org 0x41D44
m68k_041d44:
        cmpi.w #0x6,0x8160:w
m68k_041d44_end:
.org 0x41D4A
m68k_041d4a:
        bcs.b (. + 48)
m68k_041d4a_end:
.org 0x41D4C
m68k_041d4c:
        move.w #0x1,0x8130:w
m68k_041d4c_end:
.org 0x41D52
m68k_041d52:
        cmpi.w #0xa,0x8160:w
m68k_041d52_end:
.org 0x41D58
m68k_041d58:
        bcs.b (. + 8)
m68k_041d58_end:
.org 0x41D5A
m68k_041d5a:
        move.w #0x5,0x8130:w
m68k_041d5a_end:
.org 0x41D60
m68k_041d60:
        cmpi.w #0x28,0x8178:w
m68k_041d60_end:
.org 0x41D66
m68k_041d66:
        bhi.b (. + 20)
m68k_041d66_end:
.org 0x41D68
m68k_041d68:
        jsr -26184(%pc)
m68k_041d68_end:
.org 0x41D6C
m68k_041d6c:
        andi.w #0x1,%d0
m68k_041d6c_end:
.org 0x41D70
m68k_041d70:
        bne.b (. + 10)
m68k_041d70_end:
.org 0x41D72
m68k_041d72:
        move.w #0x4,0x8130:w
m68k_041d72_end:
.org 0x41D78
m68k_041d78:
        rts
m68k_041d78_end:
.org 0x41D7C
m68k_041d7c:
        jsr -26204(%pc)
m68k_041d7c_end:
.org 0x41D80
m68k_041d80:
        andi.w #0x1,%d0
m68k_041d80_end:
.org 0x41D84
m68k_041d84:
        bne.b (. + 18)
m68k_041d84_end:
.org 0x41D86
m68k_041d86:
        cmpi.w #0x5,0x8160:w
m68k_041d86_end:
.org 0x41D8C
m68k_041d8c:
        bcs.b (. + 10)
m68k_041d8c_end:
.org 0x41D8E
m68k_041d8e:
        move.w #0x5,0x8130:w
m68k_041d8e_end:
.org 0x41D94
m68k_041d94:
        rts
m68k_041d94_end:
.org 0x41D96
m68k_041d96:
        move.w #0x4,0x8130:w
m68k_041d96_end:
.org 0x41D9C
m68k_041d9c:
        rts
m68k_041d9c_end:
.org 0x41D9E
m68k_041d9e:
        jsr -26238(%pc)
m68k_041d9e_end:
.org 0x41DA2
m68k_041da2:
        andi.w #0x1,%d0
m68k_041da2_end:
.org 0x41DA6
m68k_041da6:
        bne.b (. + 18)
m68k_041da6_end:
.org 0x41DA8
m68k_041da8:
        cmpi.w #0x6,0x8160:w
m68k_041da8_end:
.org 0x41DAE
m68k_041dae:
        bcs.b (. + 10)
m68k_041dae_end:
.org 0x41DB0
m68k_041db0:
        move.w #0x5,0x8130:w
m68k_041db0_end:
.org 0x41DB6
m68k_041db6:
        rts
m68k_041db6_end:
.org 0x41DB8
m68k_041db8:
        move.w #0x4,0x8130:w
m68k_041db8_end:
.org 0x41DBE
m68k_041dbe:
        rts
m68k_041dbe_end:
