| 由直接调用、分支或顺序执行到达的指令。
.cpu 68000
.section .text
_start:
.org 0x874
m68k_000874:
        bsr.w (. + 114)
m68k_000874_end:
.org 0x878
m68k_000878:
        move.l %d0,0xf39e:w
m68k_000878_end:
.org 0x87C
m68k_00087c:
        move.w 0xf3a8:w,%d0
m68k_00087c_end:
.org 0x880
m68k_000880:
        lsl.w #0x2,%d0
m68k_000880_end:
.org 0x882
m68k_000882:
        lea.l 0xdffc:w,%a0
m68k_000882_end:
.org 0x886
m68k_000886:
        move.l (%a0, %d0.w),%d0
m68k_000886_end:
.org 0x88A
m68k_00088a:
        cmp.l 0xf39e:w,%d0
m68k_00088a_end:
.org 0x88E
m68k_00088e:
        bcc.b (. + 34)
m68k_00088e_end:
.org 0x890
m68k_000890:
        move.w #0x2,0xf362:w
m68k_000890_end:
.org 0x896
m68k_000896:
        move.w #0x23,0xf362:w
m68k_000896_end:
.org 0x89C
m68k_00089c:
        move.w #0x78,0xf608:w
m68k_00089c_end:
.org 0x8A2
m68k_0008a2:
        move.w #0xbd,%d0
m68k_0008a2_end:
.org 0x8A6
m68k_0008a6:
        jsr 0x676f2:l
m68k_0008a6_end:
.org 0x8AC
m68k_0008ac:
        bra.w (. + -672)
m68k_0008ac_end:
.org 0x8C4
m68k_0008c4:
        jsr 0x165d8:l
m68k_0008c4_end:
.org 0x8E6
m68k_0008e6:
        move.w 0xf3ae:w,%d0
m68k_0008e6_end:
.org 0x8EA
m68k_0008ea:
        lsl.w #0x2,%d0
m68k_0008ea_end:
.org 0x8EC
m68k_0008ec:
        lea.l 0xd4ac6:l,%a0
m68k_0008ec_end:
.org 0x8F2
m68k_0008f2:
        move.w (%a0, %d0.w),0xf63e:w
m68k_0008f2_end:
.org 0x8F8
m68k_0008f8:
        move.w 0x2(%a0, %d0.w),0xf63c:w
m68k_0008f8_end:
.org 0x8FE
m68k_0008fe:
        move.w 0xf364:w,%d0
m68k_0008fe_end:
.org 0x902
m68k_000902:
        lsl.w #0x2,%d0
m68k_000902_end:
.org 0x904
m68k_000904:
        move.w (%a0, %d0.w),0xf642:w
m68k_000904_end:
.org 0x90A
m68k_00090a:
        move.w 0x2(%a0, %d0.w),0xf640:w
m68k_00090a_end:
.org 0x910
m68k_000910:
        jsr 0x6518:l
m68k_000910_end:
.org 0x916
m68k_000916:
        move.w 0xf3a6:w,%d0
m68k_000916_end:
.org 0x91A
m68k_00091a:
        lea.l 0xc400:w,%a0
m68k_00091a_end:
.org 0x91E
m68k_00091e:
        clr.w %d1
m68k_00091e_end:
.org 0x920
m68k_000920:
        move.b (%a0, %d0.w),%d1
m68k_000920_end:
.org 0x924
m68k_000924:
        moveq #0,%d0
m68k_000924_end:
.org 0x926
m68k_000926:
        move.w 0xf644:w,%d0
m68k_000926_end:
.org 0x92A
m68k_00092a:
        lsl.w #0x2,%d0
m68k_00092a_end:
.org 0x92C
m68k_00092c:
        divu.w %d1,%d0
m68k_00092c_end:
.org 0x92E
m68k_00092e:
        swap %d0
m68k_00092e_end:
.org 0x930
m68k_000930:
        tst.w %d0
m68k_000930_end:
.org 0x932
m68k_000932:
        beq.b (. + 8)
m68k_000932_end:
.org 0x934
m68k_000934:
        addi.l #0x10000,%d0
m68k_000934_end:
.org 0x93A
m68k_00093a:
        swap %d0
m68k_00093a_end:
.org 0x93C
m68k_00093c:
        mulu.w %d0,%d0
m68k_00093c_end:
.org 0x93E
m68k_00093e:
        move.l %d0,%d1
m68k_00093e_end:
.org 0x940
m68k_000940:
        lsl.l #0x1,%d0
m68k_000940_end:
.org 0x942
m68k_000942:
        add.l %d1,%d0
m68k_000942_end:
.org 0x944
m68k_000944:
        lsl.l #0x3,%d0
m68k_000944_end:
.org 0x946
m68k_000946:
        add.l %d1,%d0
m68k_000946_end:
.org 0x948
m68k_000948:
        lsr.l #0x2,%d0
m68k_000948_end:
.org 0x94A
m68k_00094a:
        rts
m68k_00094a_end:
.org 0xF5A
m68k_000f5a:
        cmpi.w #0x10,0xf352:w
m68k_000f5a_end:
.org 0xF60
m68k_000f60:
        bcs.w (. + 22)
m68k_000f60_end:
.org 0x1358
m68k_001358:
        cmpi.w #0xc,0xf322:w
m68k_001358_end:
.org 0x135E
m68k_00135e:
        bcs.w (. + 50)
m68k_00135e_end:
.org 0x1362
m68k_001362:
        move.w 0xf314:w,%d0
m68k_001362_end:
.org 0x1366
m68k_001366:
        lsr.w #0x3,%d0
m68k_001366_end:
.org 0x1368
m68k_001368:
        addi.w #0x10,%d0
m68k_001368_end:
.org 0x136C
m68k_00136c:
        move.w 0xf318:w,%d1
m68k_00136c_end:
.org 0x1370
m68k_001370:
        lsr.w #0x3,%d1
m68k_001370_end:
.org 0x1372
m68k_001372:
        addi.w #0x8,%d1
m68k_001372_end:
.org 0x1376
m68k_001376:
        btst.b #0x0,0xf31c:w
m68k_001376_end:
.org 0x137C
m68k_00137c:
        beq.w (. + 8)
m68k_00137c_end:
.org 0x1380
m68k_001380:
        addi.w #0xa0,%d1
m68k_001380_end:
.org 0x1384
m68k_001384:
        clr.w %d2
m68k_001384_end:
.org 0x1386
m68k_001386:
        lea.l 10(%pc),%a0
m68k_001386_end:
.org 0x138A
m68k_00138a:
        jsr 0xac08:l
m68k_00138a_end:
.org 0x1424
m68k_001424:
        move.w #0x26,%d1
m68k_001424_end:
.org 0x1428
m68k_001428:
        cmp.b (%a0)+,%d0
m68k_001428_end:
.org 0x142A
m68k_00142a:
        bne.w (. + 20)
m68k_00142a_end:
.org 0x142E
m68k_00142e:
        dbra %d1,(. + -6)
m68k_00142e_end:
.org 0x1432
m68k_001432:
        move.w %d0,0xf376:w
m68k_001432_end:
.org 0x1436
m68k_001436:
        ori.w #0x1,%sr
m68k_001436_end:
.org 0x143A
m68k_00143a:
        bra.w (. + 8)
m68k_00143a_end:
.org 0x15BE
m68k_0015be:
        move.w 0xf35e:w,%d0
m68k_0015be_end:
.org 0x15C2
m68k_0015c2:
        subi.w #0x70,%d0
m68k_0015c2_end:
.org 0x15C6
m68k_0015c6:
        bpl.w (. + 6)
m68k_0015c6_end:
.org 0x15CA
m68k_0015ca:
        clr.w %d0
m68k_0015ca_end:
.org 0x15CC
m68k_0015cc:
        cmpi.w #0x3a0,%d0
m68k_0015cc_end:
.org 0x15D0
m68k_0015d0:
        bls.w (. + 8)
m68k_0015d0_end:
.org 0x15D4
m68k_0015d4:
        move.w #0x3a0,%d0
m68k_0015d4_end:
.org 0x15D8
m68k_0015d8:
        move.w %d0,0xf356:w
m68k_0015d8_end:
.org 0x15DC
m68k_0015dc:
        move.w 0xf360:w,%d0
m68k_0015dc_end:
.org 0x15E0
m68k_0015e0:
        subi.w #0xa0,%d0
m68k_0015e0_end:
.org 0x15E4
m68k_0015e4:
        bpl.w (. + 6)
m68k_0015e4_end:
.org 0x15E8
m68k_0015e8:
        clr.w %d0
m68k_0015e8_end:
.org 0x15EA
m68k_0015ea:
        cmpi.w #0x340,%d0
m68k_0015ea_end:
.org 0x15EE
m68k_0015ee:
        bls.w (. + 8)
m68k_0015ee_end:
.org 0x15F2
m68k_0015f2:
        move.w #0x340,%d0
m68k_0015f2_end:
.org 0x15F6
m68k_0015f6:
        move.w %d0,0xf354:w
m68k_0015f6_end:
.org 0x15FA
m68k_0015fa:
        rts
m68k_0015fa_end:
.org 0x17C0
m68k_0017c0:
        cmpi.w #0x20b,0xf612:w
m68k_0017c0_end:
.org 0x17C6
m68k_0017c6:
        beq.w (. + 10)
m68k_0017c6_end:
.org 0x1C12
m68k_001c12:
        cmpi.w #0x1,0xf36c:w
m68k_001c12_end:
.org 0x1C18
m68k_001c18:
        bne.w (. + 140)
m68k_001c18_end:
.org 0x1C1C
m68k_001c1c:
        lea.l 0xf427:w,%a0
m68k_001c1c_end:
.org 0x1C20
m68k_001c20:
        move.w 0xf364:w,%d0
m68k_001c20_end:
.org 0x1C24
m68k_001c24:
        andi.w #0x3f,%d0
m68k_001c24_end:
.org 0x1C28
m68k_001c28:
        move.b (%a0, %d0.w),%d0
m68k_001c28_end:
.org 0x1C2C
m68k_001c2c:
        cmp.b 0xf377:w,%d0
m68k_001c2c_end:
.org 0x1C30
m68k_001c30:
        bne.w (. + 50)
m68k_001c30_end:
.org 0x1C34
m68k_001c34:
        move.b 0xf579:w,%d0
m68k_001c34_end:
.org 0x1C38
m68k_001c38:
        cmpi.b #0xd,%d0
m68k_001c38_end:
.org 0x1C3C
m68k_001c3c:
        beq.w (. + 28)
m68k_001c3c_end:
.org 0x1C40
m68k_001c40:
        cmpi.b #0x10,%d0
m68k_001c40_end:
.org 0x1C44
m68k_001c44:
        beq.w (. + 20)
m68k_001c44_end:
.org 0x1C48
m68k_001c48:
        cmpi.b #0x16,%d0
m68k_001c48_end:
.org 0x1C4C
m68k_001c4c:
        beq.w (. + 12)
m68k_001c4c_end:
.org 0x1C50
m68k_001c50:
        cmpi.b #0x1a,%d0
m68k_001c50_end:
.org 0x1C54
m68k_001c54:
        bne.w (. + 14)
m68k_001c54_end:
.org 0x1C58
m68k_001c58:
        cmpi.w #0x1,0xf636:w
m68k_001c58_end:
.org 0x1C5E
m68k_001c5e:
        beq.w (. + 76)
m68k_001c5e_end:
.org 0x1C62
m68k_001c62:
        cmpi.b #0x16,%d0
m68k_001c62_end:
.org 0x1C66
m68k_001c66:
        bne.w (. + 14)
m68k_001c66_end:
.org 0x1C6A
m68k_001c6a:
        cmpi.w #0xa,0xf636:w
m68k_001c6a_end:
.org 0x1C70
m68k_001c70:
        bcc.w (. + 74)
m68k_001c70_end:
.org 0x1C74
m68k_001c74:
        cmpi.w #0x26,0xf38c:w
m68k_001c74_end:
.org 0x1C7A
m68k_001c7a:
        bne.w (. + 14)
m68k_001c7a_end:
.org 0x1C7E
m68k_001c7e:
        cmpi.w #0xa,0xf636:w
m68k_001c7e_end:
.org 0x1C84
m68k_001c84:
        bcc.w (. + 70)
m68k_001c84_end:
.org 0x200C
m68k_00200c:
        tst.w 0xf36a:w
m68k_00200c_end:
.org 0x2010
m68k_002010:
        bne.w (. + 18)
m68k_002010_end:
.org 0x2014
m68k_002014:
        tst.w 0xf600:w
m68k_002014_end:
.org 0x2018
m68k_002018:
        bne.w (. + 16)
m68k_002018_end:
.org 0x201C
m68k_00201c:
        move.w #0x64,0xf600:w
m68k_00201c_end:
.org 0x2032
m68k_002032:
        btst.b #0x2,0xf3a5:w
m68k_002032_end:
.org 0x2038
m68k_002038:
        bne.w (. + 10)
m68k_002038_end:
.org 0x203C
m68k_00203c:
        jsr 0xd8ae:l
m68k_00203c_end:
.org 0x24BC
m68k_0024bc:
        move.w #0xd,%d0
m68k_0024bc_end:
.org 0x25BC
m68k_0025bc:
        tst.w 0xf3a2:w
m68k_0025bc_end:
.org 0x25C0
m68k_0025c0:
        beq.w (. + 46)
m68k_0025c0_end:
.org 0x25C4
m68k_0025c4:
        btst.b #0x6,0xf3a4:w
m68k_0025c4_end:
.org 0x25CA
m68k_0025ca:
        beq.w (. + 26)
m68k_0025ca_end:
.org 0x25CE
m68k_0025ce:
        move.w 0xf362:w,0xf3c4:w
m68k_0025ce_end:
.org 0x25D4
m68k_0025d4:
        move.w #0x13,0xf362:w
m68k_0025d4_end:
.org 0x25DA
m68k_0025da:
        move.w 0xf612:w,0xf3c2:w
m68k_0025da_end:
.org 0x25E0
m68k_0025e0:
        bra.w (. + 96)
m68k_0025e0_end:
.org 0x25E4
m68k_0025e4:
        move.w #0x205,0xf612:w
m68k_0025e4_end:
.org 0x25EA
m68k_0025ea:
        bra.w (. + 60)
m68k_0025ea_end:
.org 0x25EE
m68k_0025ee:
        move.w 0xf3a4:w,%d0
m68k_0025ee_end:
.org 0x25F2
m68k_0025f2:
        andi.w #0x3ff0,%d0
m68k_0025f2_end:
.org 0x25F6
m68k_0025f6:
        beq.w (. + 36)
m68k_0025f6_end:
.org 0x25FA
m68k_0025fa:
        move.w #0x7,0xf362:w
m68k_0025fa_end:
.org 0x2600
m68k_002600:
        move.w #0x9,0xf36a:w
m68k_002600_end:
.org 0x2606
m68k_002606:
        btst.b #0x6,0xf3a4:w
m68k_002606_end:
.org 0x260C
m68k_00260c:
        bne.w (. + 10)
m68k_00260c_end:
.org 0x2610
m68k_002610:
        move.w #0xd,0xf36a:w
m68k_002610_end:
.org 0x2616
m68k_002616:
        bra.w (. + 42)
m68k_002616_end:
.org 0x261A
m68k_00261a:
        move.w #0x201,0xf612:w
m68k_00261a_end:
.org 0x2620
m68k_002620:
        jsr 0x676c4:l
m68k_002620_end:
.org 0x2626
m68k_002626:
        bclr.b #0x3,0xf31c:w
m68k_002626_end:
.org 0x262C
m68k_00262c:
        move.w #0x1,%d0
m68k_00262c_end:
.org 0x2630
m68k_002630:
        move.w #0x3,%d1
m68k_002630_end:
.org 0x2634
m68k_002634:
        jsr 0x506c:l
m68k_002634_end:
.org 0x263A
m68k_00263a:
        jsr 0x5abc:l
m68k_00263a_end:
.org 0x2640
m68k_002640:
        rts
m68k_002640_end:
.org 0x2664
m68k_002664:
        jsr 0x5694:l
m68k_002664_end:
.org 0x266A
m68k_00266a:
        jsr 0x5abc:l
m68k_00266a_end:
.org 0x2670
m68k_002670:
        move.w #0x206,0xf612:w
m68k_002670_end:
.org 0x2676
m68k_002676:
        move.w #0x8,0xf362:w
m68k_002676_end:
.org 0x267C
m68k_00267c:
        clr.w 0xf36a:w
m68k_00267c_end:
.org 0x2680
m68k_002680:
        clr.w 0xf36e:w
m68k_002680_end:
.org 0x2684
m68k_002684:
        move.w 0xf364:w,%d0
m68k_002684_end:
.org 0x2688
m68k_002688:
        jsr 0x5f48:l
m68k_002688_end:
.org 0x268E
m68k_00268e:
        move.w %d3,0xf636:w
m68k_00268e_end:
.org 0x2692
m68k_002692:
        tst.w 0xf3a2:w
m68k_002692_end:
.org 0x2696
m68k_002696:
        bne.w (. + 26)
m68k_002696_end:
.org 0x269A
m68k_00269a:
        move.w #0x1,0xf378:w
m68k_00269a_end:
.org 0x26A0
m68k_0026a0:
        move.w 0xf500:w,0xf372:w
m68k_0026a0_end:
.org 0x26A6
m68k_0026a6:
        move.w 0xf3a6:w,0xf3f2:w
m68k_0026a6_end:
.org 0x26AC
m68k_0026ac:
        clr.w 0xf658:w
m68k_0026ac_end:
.org 0x26B0
m68k_0026b0:
        clr.w 0xf656:w
m68k_0026b0_end:
.org 0x26B4
m68k_0026b4:
        rts
m68k_0026b4_end:
.org 0x2862
m68k_002862:
        move.w #0x7,0xf362:w
m68k_002862_end:
.org 0x2868
m68k_002868:
        move.w #0x9,%d0
m68k_002868_end:
.org 0x286C
m68k_00286c:
        btst.b #0x6,0xf3a4:w
m68k_00286c_end:
.org 0x2872
m68k_002872:
        bne.w (. + 8)
m68k_002872_end:
.org 0x2876
m68k_002876:
        move.w #0xc,%d0
m68k_002876_end:
.org 0x287A
m68k_00287a:
        move.w %d0,0xf36a:w
m68k_00287a_end:
.org 0x287E
m68k_00287e:
        bra.w (. + 20)
m68k_00287e_end:
.org 0x2EA4
m68k_002ea4:
        btst.b #0x6,0xf603:w
m68k_002ea4_end:
.org 0x2EAA
m68k_002eaa:
        bne.w (. + 20)
m68k_002eaa_end:
.org 0x2EBE
m68k_002ebe:
        move.w #0xac,%d0
m68k_002ebe_end:
.org 0x2EC2
m68k_002ec2:
        jsr 0x808a:l
m68k_002ec2_end:
.org 0x2EC8
m68k_002ec8:
        move.w #0xec,0xf600:w
m68k_002ec8_end:
.org 0x2ECE
m68k_002ece:
        move.w #0x2a,0xf362:w
m68k_002ece_end:
.org 0x2ED4
m68k_002ed4:
        move.w 0xefd6:w,0xaff8:w
m68k_002ed4_end:
.org 0x2EDA
m68k_002eda:
        move.w 0xefd8:w,0xaffa:w
m68k_002eda_end:
.org 0x2EE0
m68k_002ee0:
        clr.w 0xaffc:w
m68k_002ee0_end:
.org 0x2F24
m68k_002f24:
        move.w #0x2b,0xf362:w
m68k_002f24_end:
.org 0x2F2A
m68k_002f2a:
        move.w #0x9c,%d0
m68k_002f2a_end:
.org 0x2F2E
m68k_002f2e:
        jsr 0x676f2:l
m68k_002f2e_end:
.org 0x2F34
m68k_002f34:
        move.w #0xffff,0xff7026:l
m68k_002f34_end:
.org 0x2F64
m68k_002f64:
        bclr.b #0x7,0xf603:w
m68k_002f64_end:
.org 0x2F6A
m68k_002f6a:
        bsr.w (. + 28404)
m68k_002f6a_end:
.org 0x2FFE
m68k_002ffe:
        jsr 0x5abc:l
m68k_002ffe_end:
.org 0x3032
m68k_003032:
        bclr.b #0x6,0xf3a4:w
m68k_003032_end:
.org 0x326A
m68k_00326a:
        jsr 0x1626c:l
m68k_00326a_end:
.org 0x32FA
m68k_0032fa:
        cmpi.w #0x13,0xf362:w
m68k_0032fa_end:
.org 0x3300
m68k_003300:
        bne.w (. + 10)
m68k_003300_end:
.org 0x3304
m68k_003304:
        move.w #0x201,0xf612:w
m68k_003304_end:
.org 0x4126
m68k_004126:
        tst.b 0xf32b:w
m68k_004126_end:
.org 0x412A
m68k_00412a:
        bne.w (. + 48)
m68k_00412a_end:
.org 0x412E
m68k_00412e:
        cmpi.w #0x300,0xf612:w
m68k_00412e_end:
.org 0x4134
m68k_004134:
        beq.b (. + 38)
m68k_004134_end:
.org 0x4136
m68k_004136:
        cmpi.w #0x301,0xf612:w
m68k_004136_end:
.org 0x413C
m68k_00413c:
        beq.b (. + 30)
m68k_00413c_end:
.org 0x413E
m68k_00413e:
        move.b #0x1,0xf32b:w
m68k_00413e_end:
.org 0x4144
m68k_004144:
        clr.w 0xf608:w
m68k_004144_end:
.org 0x4148
m68k_004148:
        clr.w 0x842c:w
m68k_004148_end:
.org 0x414C
m68k_00414c:
        move.b #0xac,%d0
m68k_00414c_end:
.org 0x4150
m68k_004150:
        jsr 0x808a:l
m68k_004150_end:
.org 0x4156
m68k_004156:
        clr.w 0xf32e:w
m68k_004156_end:
.org 0x41AC
m68k_0041ac:
        move.w #0x2700,%sr
m68k_0041ac_end:
.org 0x41B0
m68k_0041b0:
        move.w #0x33e,0xf32e:w
m68k_0041b0_end:
.org 0x41B6
m68k_0041b6:
        move.w #0x20,0xf32c:w
m68k_0041b6_end:
.org 0x41BC
m68k_0041bc:
        move.w 0xf32c:w,%d2
m68k_0041bc_end:
.org 0x41C0
m68k_0041c0:
        bsr.w (. + -1984)
m68k_0041c0_end:
.org 0x41C4
m68k_0041c4:
        move.w #0x2500,%sr
m68k_0041c4_end:
.org 0x41DA
m68k_0041da:
        move.w #0xffff,0x80ca:w
m68k_0041da_end:
.org 0x41E0
m68k_0041e0:
        move.w #0xffff,0x80cc:w
m68k_0041e0_end:
.org 0x41E6
m68k_0041e6:
        move.w #0xffff,0x80ce:w
m68k_0041e6_end:
.org 0x41EC
m68k_0041ec:
        move.w #0xffff,0x80d0:w
m68k_0041ec_end:
.org 0x41F2
m68k_0041f2:
        moveq #1,%d0
m68k_0041f2_end:
.org 0x41F4
m68k_0041f4:
        jsr 0x3aa38:l
m68k_0041f4_end:
.org 0x4204
m68k_004204:
        btst.b #0x7,0x80c4:w
m68k_004204_end:
.org 0x420A
m68k_00420a:
        beq.w (. + 16)
m68k_00420a_end:
.org 0x420E
m68k_00420e:
        move.w #0x18,0xf600:w
m68k_00420e_end:
.org 0x4214
m68k_004214:
        move.w #0x303,0xf612:w
m68k_004214_end:
.org 0x4230
m68k_004230:
        cmpi.w #0x280,0xf32e:w
m68k_004230_end:
.org 0x4236
m68k_004236:
        bne.b (. + 74)
m68k_004236_end:
.org 0x4238
m68k_004238:
        move.w #0x2700,%sr
m68k_004238_end:
.org 0x423C
m68k_00423c:
        lea.l 0x65ff6:l,%a0
m68k_00423c_end:
.org 0x4242
m68k_004242:
        lea.l 0xc000:l,%a1
m68k_004242_end:
.org 0x4248
m68k_004248:
        move.l #0x80,%d5
m68k_004248_end:
.org 0x424E
m68k_00424e:
        clr.w 0x8000:w
m68k_00424e_end:
.org 0x4252
m68k_004252:
        move.w #0x10,%d6
m68k_004252_end:
.org 0x4256
m68k_004256:
        jsr 0x3aad6:l
m68k_004256_end:
.org 0x425C
m68k_00425c:
        lea.l 0x66199:l,%a0
m68k_00425c_end:
.org 0x4262
m68k_004262:
        lea.l 0xc040:l,%a1
m68k_004262_end:
.org 0x4268
m68k_004268:
        move.l #0x80,%d5
m68k_004268_end:
.org 0x426E
m68k_00426e:
        clr.w 0x8000:w
m68k_00426e_end:
.org 0x4272
m68k_004272:
        move.w #0x10,%d6
m68k_004272_end:
.org 0x4276
m68k_004276:
        jsr 0x3aad6:l
m68k_004276_end:
.org 0x427C
m68k_00427c:
        move.w #0x2500,%sr
m68k_00427c_end:
.org 0x4280
m68k_004280:
        bsr.w (. + 316)
m68k_004280_end:
.org 0x4284
m68k_004284:
        rts
m68k_004284_end:
.org 0x4286
m68k_004286:
        move.w #0x1,%d3
m68k_004286_end:
.org 0x428A
m68k_00428a:
        cmpi.w #0x20,0xf32c:w
m68k_00428a_end:
.org 0x4290
m68k_004290:
        bcc.w (. + 34)
m68k_004290_end:
.org 0x4294
m68k_004294:
        addq.w #0x2,0xf32c:w
m68k_004294_end:
.org 0x4298
m68k_004298:
        cmpi.w #0x10,0xf32c:w
m68k_004298_end:
.org 0x429E
m68k_00429e:
        bls.w (. + 8)
m68k_00429e_end:
.org 0x42A2
m68k_0042a2:
        addq.w #0x2,0xf32c:w
m68k_0042a2_end:
.org 0x42A6
m68k_0042a6:
        move.w 0xf32c:w,%d2
m68k_0042a6_end:
.org 0x42AA
m68k_0042aa:
        bsr.w (. + -2218)
m68k_0042aa_end:
.org 0x42AE
m68k_0042ae:
        move.w #0x4,%d3
m68k_0042ae_end:
.org 0x42B2
m68k_0042b2:
        bsr.w (. + 266)
m68k_0042b2_end:
.org 0x42B6
m68k_0042b6:
        movem.l %a1,-(%a7)
m68k_0042b6_end:
.org 0x42BA
m68k_0042ba:
        cmpi.w #0x340,0xf32e:w
m68k_0042ba_end:
.org 0x42C0
m68k_0042c0:
        bne.b (. + 74)
m68k_0042c0_end:
.org 0x42C2
m68k_0042c2:
        move.w #0x2700,%sr
m68k_0042c2_end:
.org 0x42C6
m68k_0042c6:
        lea.l 0x65ff6:l,%a0
m68k_0042c6_end:
.org 0x42CC
m68k_0042cc:
        lea.l 0xc000:l,%a1
m68k_0042cc_end:
.org 0x42D2
m68k_0042d2:
        move.l #0x80,%d5
m68k_0042d2_end:
.org 0x42D8
m68k_0042d8:
        clr.w 0x8000:w
m68k_0042d8_end:
.org 0x42DC
m68k_0042dc:
        move.w #0x10,%d6
m68k_0042dc_end:
.org 0x42E0
m68k_0042e0:
        jsr 0x3aad6:l
m68k_0042e0_end:
.org 0x42E6
m68k_0042e6:
        lea.l 0x66199:l,%a0
m68k_0042e6_end:
.org 0x42EC
m68k_0042ec:
        lea.l 0xc040:l,%a1
m68k_0042ec_end:
.org 0x42F2
m68k_0042f2:
        move.l #0x80,%d5
m68k_0042f2_end:
.org 0x42F8
m68k_0042f8:
        clr.w 0x8000:w
m68k_0042f8_end:
.org 0x42FC
m68k_0042fc:
        move.w #0x10,%d6
m68k_0042fc_end:
.org 0x4300
m68k_004300:
        jsr 0x3aad6:l
m68k_004300_end:
.org 0x4306
m68k_004306:
        move.w #0x2500,%sr
m68k_004306_end:
.org 0x430A
m68k_00430a:
        movem.l (%a7)+,%a1
m68k_00430a_end:
.org 0x430E
m68k_00430e:
        lea.l 144(%pc),%a0
m68k_00430e_end:
.org 0x4312
m68k_004312:
        nop
m68k_004312_end:
.org 0x4314
m68k_004314:
        move.w #0xf0b,%d4
m68k_004314_end:
.org 0x4318
m68k_004318:
        move.w #0xe300,%d1
m68k_004318_end:
.org 0x431C
m68k_00431c:
        move.w #0x6,%d7
m68k_00431c_end:
.org 0x4320
m68k_004320:
        move.w (%a0)+,(%a1)
m68k_004320_end:
.org 0x4322
m68k_004322:
        move.w #0x200,(%a1)+
m68k_004322_end:
.org 0x4326
m68k_004326:
        move.w %d4,(%a1)+
m68k_004326_end:
.org 0x4328
m68k_004328:
        move.w %d1,(%a1)+
m68k_004328_end:
.org 0x432A
m68k_00432a:
        move.w (%a0)+,(%a1)+
m68k_00432a_end:
.org 0x432C
m68k_00432c:
        addq.w #0x1,%d4
m68k_00432c_end:
.org 0x432E
m68k_00432e:
        addi.w #0x10,%d1
m68k_00432e_end:
.org 0x4332
m68k_004332:
        dbra %d7,(. + -18)
m68k_004332_end:
.org 0x4336
m68k_004336:
        bsr.w (. + 330)
m68k_004336_end:
.org 0x433A
m68k_00433a:
        cmpi.w #0x340,0xf32e:w
m68k_00433a_end:
.org 0x4340
m68k_004340:
        bcs.w (. + 34)
m68k_004340_end:
.org 0x43BC
m68k_0043bc:
        lea.l -70(%pc),%a0
m68k_0043bc_end:
.org 0x43C0
m68k_0043c0:
        lea.l 0xf800:w,%a1
m68k_0043c0_end:
.org 0x43C4
m68k_0043c4:
        move.w #0xd01,%d0
m68k_0043c4_end:
.org 0x43C8
m68k_0043c8:
        move.w #0xe370,%d1
m68k_0043c8_end:
.org 0x43CC
m68k_0043cc:
        move.w #0x9,%d7
m68k_0043cc_end:
.org 0x43D0
m68k_0043d0:
        move.w (%a0)+,(%a1)
m68k_0043d0_end:
.org 0x43D2
m68k_0043d2:
        move.w #0x200,(%a1)+
m68k_0043d2_end:
.org 0x43D6
m68k_0043d6:
        move.w %d0,(%a1)+
m68k_0043d6_end:
.org 0x43D8
m68k_0043d8:
        move.w %d1,(%a1)+
m68k_0043d8_end:
.org 0x43DA
m68k_0043da:
        move.w (%a0)+,(%a1)+
m68k_0043da_end:
.org 0x43DC
m68k_0043dc:
        addq.w #0x1,%d0
m68k_0043dc_end:
.org 0x43DE
m68k_0043de:
        addi.w #0x8,%d1
m68k_0043de_end:
.org 0x43E2
m68k_0043e2:
        cmpi.w #0x6,%d7
m68k_0043e2_end:
.org 0x43E6
m68k_0043e6:
        bcc.w (. + 8)
m68k_0043e6_end:
.org 0x43EA
m68k_0043ea:
        addi.w #0x8,%d1
m68k_0043ea_end:
.org 0x43EE
m68k_0043ee:
        cmpi.w #0x7,%d7
m68k_0043ee_end:
.org 0x43F2
m68k_0043f2:
        bcc.w (. + 8)
m68k_0043f2_end:
.org 0x43F6
m68k_0043f6:
        ori.w #0x200,%d0
m68k_0043f6_end:
.org 0x43FA
m68k_0043fa:
        dbra %d7,(. + -42)
m68k_0043fa_end:
.org 0x43FE
m68k_0043fe:
        rts
m68k_0043fe_end:
.org 0x4442
m68k_004442:
        btst.b #0x5,0xf321:w
m68k_004442_end:
.org 0x4448
m68k_004448:
        bne.b (. + 32)
m68k_004448_end:
.org 0x444A
m68k_00444a:
        lea.l 218(%pc),%a0
m68k_00444a_end:
.org 0x444E
m68k_00444e:
        nop
m68k_00444e_end:
.org 0x4450
m68k_004450:
        move.w %d4,%d0
m68k_004450_end:
.org 0x4452
m68k_004452:
        andi.w #0xff,%d0
m68k_004452_end:
.org 0x4456
m68k_004456:
        move.w #0xe,%d7
m68k_004456_end:
.org 0x445A
m68k_00445a:
        move.w (%a0)+,(%a1)+
m68k_00445a_end:
.org 0x445C
m68k_00445c:
        move.w %d0,(%a1)+
m68k_00445c_end:
.org 0x445E
m68k_00445e:
        move.w (%a0)+,(%a1)+
m68k_00445e_end:
.org 0x4460
m68k_004460:
        move.w (%a0)+,(%a1)+
m68k_004460_end:
.org 0x4462
m68k_004462:
        addq.w #0x1,%d0
m68k_004462_end:
.org 0x4464
m68k_004464:
        dbra %d7,(. + -10)
m68k_004464_end:
.org 0x4468
m68k_004468:
        move.w #0x0,(%a1)
m68k_004468_end:
.org 0x446C
m68k_00446c:
        move.w #0x0,0x2(%a1)
m68k_00446c_end:
.org 0x4472
m68k_004472:
        move.w #0x0,0x4(%a1)
m68k_004472_end:
.org 0x4478
m68k_004478:
        move.w #0x0,0x6(%a1)
m68k_004478_end:
.org 0x447E
m68k_00447e:
        rts
m68k_00447e_end:
.org 0x4480
m68k_004480:
        lea.l 254(%pc),%a0
m68k_004480_end:
.org 0x4484
m68k_004484:
        nop
m68k_004484_end:
.org 0x4486
m68k_004486:
        move.w %d4,%d0
m68k_004486_end:
.org 0x4488
m68k_004488:
        andi.w #0xff,%d0
m68k_004488_end:
.org 0x448C
m68k_00448c:
        move.w #0x8,%d7
m68k_00448c_end:
.org 0x4490
m68k_004490:
        move.w (%a0)+,(%a1)+
m68k_004490_end:
.org 0x4492
m68k_004492:
        move.w %d0,(%a1)+
m68k_004492_end:
.org 0x4494
m68k_004494:
        move.w (%a0)+,(%a1)+
m68k_004494_end:
.org 0x4496
m68k_004496:
        move.w (%a0)+,(%a1)+
m68k_004496_end:
.org 0x4498
m68k_004498:
        addq.w #0x1,%d0
m68k_004498_end:
.org 0x449A
m68k_00449a:
        addq.w #0x1,%d4
m68k_00449a_end:
.org 0x449C
m68k_00449c:
        dbra %d7,(. + -12)
m68k_00449c_end:
.org 0x44A0
m68k_0044a0:
        tst.w 0x843a:w
m68k_0044a0_end:
.org 0x44A4
m68k_0044a4:
        bne.b (. + 50)
m68k_0044a4_end:
.org 0x44A6
m68k_0044a6:
        addq.w #0x1,0x843a:w
m68k_0044a6_end:
.org 0x44AA
m68k_0044aa:
        movem.l %d0-%d7/%a0-%a6,-(%a7)
m68k_0044aa_end:
.org 0x44AE
m68k_0044ae:
        move.w #0x2700,%sr
m68k_0044ae_end:
.org 0x44B2
m68k_0044b2:
        lea.l 0x5cde2:l,%a0
m68k_0044b2_end:
.org 0x44B8
m68k_0044b8:
        lea.l 0xcc8c:l,%a1
m68k_0044b8_end:
.org 0x44BE
m68k_0044be:
        move.l #0x80,%d5
m68k_0044be_end:
.org 0x44C4
m68k_0044c4:
        move.w #0x1,%d6
m68k_0044c4_end:
.org 0x44C8
m68k_0044c8:
        jsr 0x3aab6:l
m68k_0044c8_end:
.org 0x44CE
m68k_0044ce:
        move.w #0x2500,%sr
m68k_0044ce_end:
.org 0x44D2
m68k_0044d2:
        movem.l (%a7)+,%d0-%d7/%a0-%a6
m68k_0044d2_end:
.org 0x44D6
m68k_0044d6:
        rts
m68k_0044d6_end:
.org 0x5694
m68k_005694:
        lea.l 0xd100:w,%a0
m68k_005694_end:
.org 0x5698
m68k_005698:
        adda.w 0xf31a:w,%a0
m68k_005698_end:
.org 0x569C
m68k_00569c:
        jsr 18(%pc)
m68k_00569c_end:
.org 0x56A0
m68k_0056a0:
        nop
m68k_0056a0_end:
.org 0x56A2
m68k_0056a2:
        jsr 44(%pc)
m68k_0056a2_end:
.org 0x56A6
m68k_0056a6:
        nop
m68k_0056a6_end:
.org 0x56A8
m68k_0056a8:
        jsr 106(%pc)
m68k_0056a8_end:
.org 0x56AC
m68k_0056ac:
        nop
m68k_0056ac_end:
.org 0x56AE
m68k_0056ae:
        rts
m68k_0056ae_end:
.org 0x56B0
m68k_0056b0:
        move.w #0xb,(%a0)+
m68k_0056b0_end:
.org 0x56B4
m68k_0056b4:
        move.w #0xc09c,(%a0)+
m68k_0056b4_end:
.org 0x56B8
m68k_0056b8:
        move.w #0xc380,(%a0)+
m68k_0056b8_end:
.org 0x56BC
m68k_0056bc:
        move.w #0x8,%d0
m68k_0056bc_end:
.org 0x56C0
m68k_0056c0:
        move.w #0xc381,(%a0)+
m68k_0056c0_end:
.org 0x56C4
m68k_0056c4:
        dbra %d0,(. + -4)
m68k_0056c4_end:
.org 0x56C8
m68k_0056c8:
        move.w #0xcb80,(%a0)+
m68k_0056c8_end:
.org 0x56CC
m68k_0056cc:
        clr.w (%a0)
m68k_0056cc_end:
.org 0x56CE
m68k_0056ce:
        rts
m68k_0056ce_end:
.org 0x56D0
m68k_0056d0:
        move.w #0xb,0x1a(%a0)
m68k_0056d0_end:
.org 0x56D6
m68k_0056d6:
        move.w #0xb,(%a0)+
m68k_0056d6_end:
.org 0x56DA
m68k_0056da:
        move.w #0xc19c,0x1a(%a0)
m68k_0056da_end:
.org 0x56E0
m68k_0056e0:
        move.w #0xc11c,(%a0)+
m68k_0056e0_end:
.org 0x56E4
m68k_0056e4:
        move.w #0xc382,0x1a(%a0)
m68k_0056e4_end:
.org 0x56EA
m68k_0056ea:
        move.w #0xc382,(%a0)+
m68k_0056ea_end:
.org 0x56EE
m68k_0056ee:
        bsr.w (. + 82)
m68k_0056ee_end:
.org 0x56F2
m68k_0056f2:
        move.w #0xc001,0x1a(%a0)
m68k_0056f2_end:
.org 0x56F8
m68k_0056f8:
        move.w #0xc001,(%a0)+
m68k_0056f8_end:
.org 0x56FC
m68k_0056fc:
        bsr.w (. + 152)
m68k_0056fc_end:
.org 0x5700
m68k_005700:
        move.w #0xcb82,0x1a(%a0)
m68k_005700_end:
.org 0x5706
m68k_005706:
        move.w #0xcb82,(%a0)+
m68k_005706_end:
.org 0x570A
m68k_00570a:
        clr.w 0x1a(%a0)
m68k_00570a_end:
.org 0x570E
m68k_00570e:
        adda.w #0x1a,%a0
m68k_00570e_end:
.org 0x5712
m68k_005712:
        rts
m68k_005712_end:
.org 0x5714
m68k_005714:
        move.w #0xb,(%a0)+
m68k_005714_end:
.org 0x5718
m68k_005718:
        move.w #0xc21c,(%a0)+
m68k_005718_end:
.org 0x571C
m68k_00571c:
        move.w #0xd380,(%a0)+
m68k_00571c_end:
.org 0x5720
m68k_005720:
        move.w #0x8,%d0
m68k_005720_end:
.org 0x5724
m68k_005724:
        move.w #0xd381,(%a0)+
m68k_005724_end:
.org 0x5728
m68k_005728:
        dbra %d0,(. + -4)
m68k_005728_end:
.org 0x572C
m68k_00572c:
        move.w #0xdb80,(%a0)+
m68k_00572c_end:
.org 0x5730
m68k_005730:
        clr.w (%a0)
m68k_005730_end:
.org 0x5732
m68k_005732:
        addi.w #0x68,0xf31a:w
m68k_005732_end:
.org 0x5738
m68k_005738:
        ori.w #0x9000,0xf3a4:w
m68k_005738_end:
.org 0x573E
m68k_00573e:
        rts
m68k_00573e_end:
.org 0x5740
m68k_005740:
        move.w 0xf364:w,%d0
m68k_005740_end:
.org 0x5744
m68k_005744:
        andi.w #0xff,%d0
m68k_005744_end:
.org 0x5748
m68k_005748:
        clr.w %d1
m68k_005748_end:
.org 0x574A
m68k_00574a:
        subi.w #0xa,%d0
m68k_00574a_end:
.org 0x574E
m68k_00574e:
        bcs.b (. + 6)
m68k_00574e_end:
.org 0x5750
m68k_005750:
        addq.w #0x1,%d1
m68k_005750_end:
.org 0x5752
m68k_005752:
        bra.b (. + -8)
m68k_005752_end:
.org 0x5754
m68k_005754:
        addi.w #0xa,%d0
m68k_005754_end:
.org 0x5758
m68k_005758:
        tst.w %d1
m68k_005758_end:
.org 0x575A
m68k_00575a:
        bne.b (. + 8)
m68k_00575a_end:
.org 0x575C
m68k_00575c:
        move.w #0xc001,%d1
m68k_00575c_end:
.org 0x5760
m68k_005760:
        bra.b (. + 8)
m68k_005760_end:
.org 0x5762
m68k_005762:
        lsl.w #0x2,%d1
m68k_005762_end:
.org 0x5764
m68k_005764:
        addi.w #0xc0d8,%d1
m68k_005764_end:
.org 0x5768
m68k_005768:
        bsr.w (. + 20)
m68k_005768_end:
.org 0x576C
m68k_00576c:
        asl.w #0x2,%d0
m68k_00576c_end:
.org 0x576E
m68k_00576e:
        addi.l #0xc0d8,%d0
m68k_00576e_end:
.org 0x5774
m68k_005774:
        move.w %d0,%d1
m68k_005774_end:
.org 0x5776
m68k_005776:
        bsr.w (. + 6)
m68k_005776_end:
.org 0x577A
m68k_00577a:
        rts
m68k_00577a_end:
.org 0x577C
m68k_00577c:
        move.w %d1,(%a0)
m68k_00577c_end:
.org 0x577E
m68k_00577e:
        addq.w #0x1,%d1
m68k_00577e_end:
.org 0x5780
m68k_005780:
        move.w %d1,0x1a(%a0)
m68k_005780_end:
.org 0x5784
m68k_005784:
        addq.w #0x1,%d1
m68k_005784_end:
.org 0x5786
m68k_005786:
        move.w %d1,0x2(%a0)
m68k_005786_end:
.org 0x578A
m68k_00578a:
        addq.w #0x1,%d1
m68k_00578a_end:
.org 0x578C
m68k_00578c:
        move.w %d1,0x1c(%a0)
m68k_00578c_end:
.org 0x5790
m68k_005790:
        addq.w #0x4,%a0
m68k_005790_end:
.org 0x5792
m68k_005792:
        rts
m68k_005792_end:
.org 0x5794
m68k_005794:
        move.w #0xc300,%d1
m68k_005794_end:
.org 0x5798
m68k_005798:
        bsr.b (. + -28)
m68k_005798_end:
.org 0x579A
m68k_00579a:
        addq.w #0x1,%d1
m68k_00579a_end:
.org 0x579C
m68k_00579c:
        bsr.b (. + -32)
m68k_00579c_end:
.org 0x579E
m68k_00579e:
        rts
m68k_00579e_end:
.org 0x5C98
m68k_005c98:
        move.l #0xc000000b,%d0
m68k_005c98_end:
.org 0x5C9E
m68k_005c9e:
        move.w #0x4,%d1
m68k_005c9e_end:
.org 0x5CA2
m68k_005ca2:
        move.w #0xc084,%d2
m68k_005ca2_end:
.org 0x5CA6
m68k_005ca6:
        lea.l 16(%pc),%a0
m68k_005ca6_end:
.org 0x5CAA
m68k_005caa:
        jsr 0x26bfa:l
m68k_005caa_end:
.org 0x5CB0
m68k_005cb0:
        bclr.b #0x3,0xf3a4:w
m68k_005cb0_end:
.org 0x5CB6
m68k_005cb6:
        rts
m68k_005cb6_end:
.org 0x5CC8
m68k_005cc8:
        move.w 0xf360:w,%d0
m68k_005cc8_end:
.org 0x5CCC
m68k_005ccc:
        move.w %d0,%d1
m68k_005ccc_end:
.org 0x5CCE
m68k_005cce:
        subi.w #0x14,%d0
m68k_005cce_end:
.org 0x5CD2
m68k_005cd2:
        addi.w #0x14,%d1
m68k_005cd2_end:
.org 0x5CD6
m68k_005cd6:
        move.w 0xf35e:w,%d2
m68k_005cd6_end:
.org 0x5CDA
m68k_005cda:
        move.w %d2,%d3
m68k_005cda_end:
.org 0x5CDC
m68k_005cdc:
        subi.w #0xc,%d2
m68k_005cdc_end:
.org 0x5CE0
m68k_005ce0:
        addi.w #0xc,%d3
m68k_005ce0_end:
.org 0x5CE4
m68k_005ce4:
        clr.w %d4
m68k_005ce4_end:
.org 0x5CE6
m68k_005ce6:
        lea.l 0xd4aca:l,%a0
m68k_005ce6_end:
.org 0x5CEC
m68k_005cec:
        move.w (%a0)+,%d5
m68k_005cec_end:
.org 0x5CEE
m68k_005cee:
        cmp.w %d0,%d5
m68k_005cee_end:
.org 0x5CF0
m68k_005cf0:
        bcs.b (. + 18)
m68k_005cf0_end:
.org 0x5CF2
m68k_005cf2:
        cmp.w %d1,%d5
m68k_005cf2_end:
.org 0x5CF4
m68k_005cf4:
        bhi.b (. + 14)
m68k_005cf4_end:
.org 0x5CF6
m68k_005cf6:
        move.w (%a0)+,%d5
m68k_005cf6_end:
.org 0x5DD2
m68k_005dd2:
        lea.l 0xd100:w,%a0
m68k_005dd2_end:
.org 0x5DD6
m68k_005dd6:
        adda.w 0xf31a:w,%a0
m68k_005dd6_end:
.org 0x5DDA
m68k_005dda:
        jsr 32(%pc)
m68k_005dda_end:
.org 0x5DDE
m68k_005dde:
        nop
m68k_005dde_end:
.org 0x5DE0
m68k_005de0:
        jsr 120(%pc)
m68k_005de0_end:
.org 0x5DE4
m68k_005de4:
        nop
m68k_005de4_end:
.org 0x5DE6
m68k_005de6:
        jsr 258(%pc)
m68k_005de6_end:
.org 0x5DEA
m68k_005dea:
        nop
m68k_005dea_end:
.org 0x5DEC
m68k_005dec:
        clr.w (%a0)
m68k_005dec_end:
.org 0x5DEE
m68k_005dee:
        addi.w #0xa8,0xf31a:w
m68k_005dee_end:
.org 0x5DF4
m68k_005df4:
        ori.w #0xa000,0xf3a4:w
m68k_005df4_end:
.org 0x5DFA
m68k_005dfa:
        rts
m68k_005dfa_end:
.org 0x5DFC
m68k_005dfc:
        move.w #0xa,0x30(%a0)
m68k_005dfc_end:
.org 0x5E02
m68k_005e02:
        move.w #0xa,0x18(%a0)
m68k_005e02_end:
.org 0x5E08
m68k_005e08:
        move.w #0xa,(%a0)+
m68k_005e08_end:
.org 0x5E0C
m68k_005e0c:
        move.w #0xc384,0x30(%a0)
m68k_005e0c_end:
.org 0x5E12
m68k_005e12:
        move.w #0xc204,0x18(%a0)
m68k_005e12_end:
.org 0x5E18
m68k_005e18:
        move.w #0xc084,(%a0)+
m68k_005e18_end:
.org 0x5E1C
m68k_005e1c:
        move.w #0xd380,0x30(%a0)
m68k_005e1c_end:
.org 0x5E22
m68k_005e22:
        move.w #0xc382,0x18(%a0)
m68k_005e22_end:
.org 0x5E28
m68k_005e28:
        move.w #0xc380,(%a0)+
m68k_005e28_end:
.org 0x5E2C
m68k_005e2c:
        move.w #0x7,%d0
m68k_005e2c_end:
.org 0x5E30
m68k_005e30:
        move.w #0xd381,0x30(%a0)
m68k_005e30_end:
.org 0x5E36
m68k_005e36:
        move.w #0xc001,0x18(%a0)
m68k_005e36_end:
.org 0x5E3C
m68k_005e3c:
        move.w #0xc381,(%a0)+
m68k_005e3c_end:
.org 0x5E40
m68k_005e40:
        dbra %d0,(. + -16)
m68k_005e40_end:
.org 0x5E44
m68k_005e44:
        move.w #0xdb80,0x30(%a0)
m68k_005e44_end:
.org 0x5E4A
m68k_005e4a:
        move.w #0xcb82,0x18(%a0)
m68k_005e4a_end:
.org 0x5E50
m68k_005e50:
        move.w #0xcb80,(%a0)+
m68k_005e50_end:
.org 0x5E54
m68k_005e54:
        adda.w #0x30,%a0
m68k_005e54_end:
.org 0x5E58
m68k_005e58:
        rts
m68k_005e58_end:
.org 0x5E5A
m68k_005e5a:
        move.w #0xa,0x18(%a0)
m68k_005e5a_end:
.org 0x5E60
m68k_005e60:
        move.w #0xa,(%a0)+
m68k_005e60_end:
.org 0x5E64
m68k_005e64:
        move.w #0xc184,0x18(%a0)
m68k_005e64_end:
.org 0x5E6A
m68k_005e6a:
        move.w #0xc104,(%a0)+
m68k_005e6a_end:
.org 0x5E6E
m68k_005e6e:
        move.w #0xc382,0x18(%a0)
m68k_005e6e_end:
.org 0x5E74
m68k_005e74:
        move.w #0xc382,(%a0)+
m68k_005e74_end:
.org 0x5E78
m68k_005e78:
        moveq #0,%d0
m68k_005e78_end:
.org 0x5E7A
m68k_005e7a:
        move.b 0xf374:w,%d0
m68k_005e7a_end:
.org 0x5E7E
m68k_005e7e:
        addi.w #0xb8,%d0
m68k_005e7e_end:
.org 0x5E82
m68k_005e82:
        move.w #0x1,%d1
m68k_005e82_end:
.org 0x5E86
m68k_005e86:
        clr.w %d2
m68k_005e86_end:
.org 0x5E88
m68k_005e88:
        lea.l 0xd300:w,%a6
m68k_005e88_end:
.org 0x5E8C
m68k_005e8c:
        jsr 0x12744:l
m68k_005e8c_end:
.org 0x5E92
m68k_005e92:
        lea.l 0xd300:w,%a1
m68k_005e92_end:
.org 0x5E96
m68k_005e96:
        move.w #0x2,%d0
m68k_005e96_end:
.org 0x5E9A
m68k_005e9a:
        jsr 54(%pc)
m68k_005e9a_end:
.org 0x5E9E
m68k_005e9e:
        nop
m68k_005e9e_end:
.org 0x5EA0
m68k_005ea0:
        move.w #0xc0d0,%d1
m68k_005ea0_end:
.org 0x5EA4
m68k_005ea4:
        jsr 20(%pc)
m68k_005ea4_end:
.org 0x5EA8
m68k_005ea8:
        nop
m68k_005ea8_end:
.org 0x5EAA
m68k_005eaa:
        move.w #0xcb82,0x18(%a0)
m68k_005eaa_end:
.org 0x5EB0
m68k_005eb0:
        move.w #0xcb82,(%a0)+
m68k_005eb0_end:
.org 0x5EB4
m68k_005eb4:
        adda.w #0x18,%a0
m68k_005eb4_end:
.org 0x5EB8
m68k_005eb8:
        rts
m68k_005eb8_end:
.org 0x5EBA
m68k_005eba:
        move.w %d1,(%a0)
m68k_005eba_end:
.org 0x5EBC
m68k_005ebc:
        addq.w #0x1,%d1
m68k_005ebc_end:
.org 0x5EBE
m68k_005ebe:
        move.w %d1,0x18(%a0)
m68k_005ebe_end:
.org 0x5EC2
m68k_005ec2:
        addq.w #0x1,%d1
m68k_005ec2_end:
.org 0x5EC4
m68k_005ec4:
        move.w %d1,0x2(%a0)
m68k_005ec4_end:
.org 0x5EC8
m68k_005ec8:
        addq.w #0x1,%d1
m68k_005ec8_end:
.org 0x5ECA
m68k_005eca:
        move.w %d1,0x1a(%a0)
m68k_005eca_end:
.org 0x5ECE
m68k_005ece:
        addq.w #0x4,%a0
m68k_005ece_end:
.org 0x5ED0
m68k_005ed0:
        rts
m68k_005ed0_end:
.org 0x5ED2
m68k_005ed2:
        move.w (%a1)+,%d1
m68k_005ed2_end:
.org 0x5ED4
m68k_005ed4:
        bne.b (. + 8)
m68k_005ed4_end:
.org 0x5ED6
m68k_005ed6:
        move.w #0xc001,%d1
m68k_005ed6_end:
.org 0x5EDA
m68k_005eda:
        bra.b (. + 8)
m68k_005eda_end:
.org 0x5EDC
m68k_005edc:
        lsl.w #0x2,%d1
m68k_005edc_end:
.org 0x5EDE
m68k_005ede:
        addi.w #0xc0d4,%d1
m68k_005ede_end:
.org 0x5EE2
m68k_005ee2:
        bsr.b (. + -40)
m68k_005ee2_end:
.org 0x5EE4
m68k_005ee4:
        dbra %d0,(. + -18)
m68k_005ee4_end:
.org 0x5EE8
m68k_005ee8:
        rts
m68k_005ee8_end:
.org 0x5EEA
m68k_005eea:
        move.w #0xa,0x18(%a0)
m68k_005eea_end:
.org 0x5EF0
m68k_005ef0:
        move.w #0xa,(%a0)+
m68k_005ef0_end:
.org 0x5EF4
m68k_005ef4:
        move.w #0xc304,0x18(%a0)
m68k_005ef4_end:
.org 0x5EFA
m68k_005efa:
        move.w #0xc284,(%a0)+
m68k_005efa_end:
.org 0x5EFE
m68k_005efe:
        move.w #0xc382,0x18(%a0)
m68k_005efe_end:
.org 0x5F04
m68k_005f04:
        move.w #0xc382,(%a0)+
m68k_005f04_end:
.org 0x5F08
m68k_005f08:
        move.w #0xc001,%d1
m68k_005f08_end:
.org 0x5F0C
m68k_005f0c:
        bsr.b (. + -82)
m68k_005f0c_end:
.org 0x5F0E
m68k_005f0e:
        moveq #0,%d0
m68k_005f0e_end:
.org 0x5F10
m68k_005f10:
        move.b 0xf375:w,%d0
m68k_005f10_end:
.org 0x5F14
m68k_005f14:
        addq.w #0x1,%d0
m68k_005f14_end:
.org 0x5F16
m68k_005f16:
        move.w #0x1,%d1
m68k_005f16_end:
.org 0x5F1A
m68k_005f1a:
        clr.w %d2
m68k_005f1a_end:
.org 0x5F1C
m68k_005f1c:
        lea.l 0xd300:w,%a6
m68k_005f1c_end:
.org 0x5F20
m68k_005f20:
        clr.w %d4
m68k_005f20_end:
.org 0x5F22
m68k_005f22:
        jsr 0x1274c:l
m68k_005f22_end:
.org 0x5F28
m68k_005f28:
        lea.l 0xd300:w,%a1
m68k_005f28_end:
.org 0x5F2C
m68k_005f2c:
        move.w #0x1,%d0
m68k_005f2c_end:
.org 0x5F30
m68k_005f30:
        bsr.b (. + -94)
m68k_005f30_end:
.org 0x5F32
m68k_005f32:
        move.w #0xc0d4,%d1
m68k_005f32_end:
.org 0x5F36
m68k_005f36:
        bsr.b (. + -124)
m68k_005f36_end:
.org 0x5F38
m68k_005f38:
        move.w #0xcb82,0x18(%a0)
m68k_005f38_end:
.org 0x5F3E
m68k_005f3e:
        move.w #0xcb82,(%a0)+
m68k_005f3e_end:
.org 0x5F42
m68k_005f42:
        adda.w #0x18,%a0
m68k_005f42_end:
.org 0x5F46
m68k_005f46:
        rts
m68k_005f46_end:
.org 0x6276
m68k_006276:
        bset.b #0x1,0xf3a4:w
m68k_006276_end:
.org 0x627C
m68k_00627c:
        cmpi.w #0x6,0xf38c:w
m68k_00627c_end:
.org 0x6282
m68k_006282:
        beq.w (. + 78)
m68k_006282_end:
.org 0x6286
m68k_006286:
        cmpi.w #0xf,0xf38c:w
m68k_006286_end:
.org 0x628C
m68k_00628c:
        beq.w (. + 68)
m68k_00628c_end:
.org 0x6290
m68k_006290:
        cmpi.w #0x15,0xf38c:w
m68k_006290_end:
.org 0x6296
m68k_006296:
        beq.w (. + 58)
m68k_006296_end:
.org 0x629A
m68k_00629a:
        jsr 0x676c4:l
m68k_00629a_end:
.org 0x62A0
m68k_0062a0:
        rts
m68k_0062a0_end:
.org 0x62D0
m68k_0062d0:
        rts
m68k_0062d0_end:
.org 0x65A0
m68k_0065a0:
        clr.w %d1
m68k_0065a0_end:
.org 0x65A2
m68k_0065a2:
        move.b 0x1(%a1),%d1
m68k_0065a2_end:
.org 0x65A6
m68k_0065a6:
        move.w %d1,%d2
m68k_0065a6_end:
.org 0x65A8
m68k_0065a8:
        lsl.w #0x3,%d1
m68k_0065a8_end:
.org 0x65AA
m68k_0065aa:
        add.w %d2,%d1
m68k_0065aa_end:
.org 0x65AC
m68k_0065ac:
        lsl.w #0x3,%d1
m68k_0065ac_end:
.org 0x65AE
m68k_0065ae:
        clr.w %d2
m68k_0065ae_end:
.org 0x65B0
m68k_0065b0:
        move.b 0x2(%a1),%d2
m68k_0065b0_end:
.org 0x65B4
m68k_0065b4:
        add.w %d2,%d1
m68k_0065b4_end:
.org 0x65B6
m68k_0065b6:
        lsl.w #0x1,%d1
m68k_0065b6_end:
.org 0x65B8
m68k_0065b8:
        move.w #0x7f,(%a0, %d1.w)
m68k_0065b8_end:
.org 0x65D0
m68k_0065d0:
        clr.w %d1
m68k_0065d0_end:
.org 0x65D2
m68k_0065d2:
        move.b 0x1(%a1),%d1
m68k_0065d2_end:
.org 0x65D6
m68k_0065d6:
        move.w %d1,%d2
m68k_0065d6_end:
.org 0x65D8
m68k_0065d8:
        lsl.w #0x3,%d1
m68k_0065d8_end:
.org 0x65DA
m68k_0065da:
        add.w %d2,%d1
m68k_0065da_end:
.org 0x65DC
m68k_0065dc:
        lsl.w #0x3,%d1
m68k_0065dc_end:
.org 0x65DE
m68k_0065de:
        clr.w %d2
m68k_0065de_end:
.org 0x65E0
m68k_0065e0:
        move.b 0x2(%a1),%d2
m68k_0065e0_end:
.org 0x65E4
m68k_0065e4:
        add.w %d2,%d1
m68k_0065e4_end:
.org 0x65E6
m68k_0065e6:
        lsl.w #0x1,%d1
m68k_0065e6_end:
.org 0x65E8
m68k_0065e8:
        move.w #0x7f,(%a0, %d1.w)
m68k_0065e8_end:
.org 0x65EE
m68k_0065ee:
        lea.l 0xd(%a1, %d0.w),%a1
m68k_0065ee_end:
.org 0x65F2
m68k_0065f2:
        bra.b (. + -42)
m68k_0065f2_end:
.org 0x67A6
m68k_0067a6:
        subq.w #0x1,%d0
m68k_0067a6_end:
.org 0x67A8
m68k_0067a8:
        bra.w (. + 10)
m68k_0067a8_end:
.org 0x67AC
m68k_0067ac:
        addq.w #0x1,%d1
m68k_0067ac_end:
.org 0x67AE
m68k_0067ae:
        bra.b (. + 4)
m68k_0067ae_end:
.org 0x808A
m68k_00808a:
        st.b 0xff3f00:l
m68k_00808a_end:
.org 0x8090
m68k_008090:
        move.w #0x100,0xa11100:l
m68k_008090_end:
.org 0x8098
m68k_008098:
        btst.b #0x0,0xa11100:l
m68k_008098_end:
.org 0x80A0
m68k_0080a0:
        bne.b (. + -8)
m68k_0080a0_end:
.org 0x80A2
m68k_0080a2:
        tst.b 0xa01c0a:l
m68k_0080a2_end:
.org 0x80A8
m68k_0080a8:
        beq.b (. + 18)
m68k_0080a8_end:
.org 0x80AA
m68k_0080aa:
        tst.b 0xa01c0b:l
m68k_0080aa_end:
.org 0x80B0
m68k_0080b0:
        bne.b (. + 16)
m68k_0080b0_end:
.org 0x80B2
m68k_0080b2:
        move.b %d0,0xa01c0b:l
m68k_0080b2_end:
.org 0x80B8
m68k_0080b8:
        bra.b (. + 8)
m68k_0080b8_end:
.org 0x80BA
m68k_0080ba:
        move.b %d0,0xa01c0a:l
m68k_0080ba_end:
.org 0x80C0
m68k_0080c0:
        sf.b 0xff3f00:l
m68k_0080c0_end:
.org 0x80C6
m68k_0080c6:
        move.w #0x0,0xa11100:l
m68k_0080c6_end:
.org 0x80CE
m68k_0080ce:
        rts
m68k_0080ce_end:
.org 0x8112
m68k_008112:
        lea.l 24(%pc),%a1
m68k_008112_end:
.org 0x8116
m68k_008116:
        lsl.w #0x3,%d0
m68k_008116_end:
.org 0x8118
m68k_008118:
        adda.w %d0,%a1
m68k_008118_end:
.org 0x811A
m68k_00811a:
        movea.l (%a1)+,%a2
m68k_00811a_end:
.org 0x811C
m68k_00811c:
        movea.w (%a1)+,%a3
m68k_00811c_end:
.org 0x811E
m68k_00811e:
        move.w (%a1)+,%d7
m68k_00811e_end:
.org 0x8120
m68k_008120:
        move.l (%a2)+,(%a3)+
m68k_008120_end:
.org 0x8122
m68k_008122:
        dbra %d7,(. + -2)
m68k_008122_end:
.org 0x8126
m68k_008126:
        addq.w #0x1,0xf31e:w
m68k_008126_end:
.org 0x812A
m68k_00812a:
        rts
m68k_00812a_end:
.org 0x83C8
m68k_0083c8:
        move.w #0x2500,%sr
m68k_0083c8_end:
.org 0x83CC
m68k_0083cc:
        tst.b 0xf612:w
m68k_0083cc_end:
.org 0x83D0
m68k_0083d0:
        bne.b (. + -4)
m68k_0083d0_end:
.org 0x83D2
m68k_0083d2:
        rts
m68k_0083d2_end:
.org 0x83FA
m68k_0083fa:
        move.b #0x53,0x200105:l
m68k_0083fa_end:
.org 0x8402
m68k_008402:
        move.b #0x45,0x200107:l
m68k_008402_end:
.org 0x840A
m68k_00840a:
        move.b #0x47,0x200109:l
m68k_00840a_end:
.org 0x8412
m68k_008412:
        move.b #0x41,0x20010b:l
m68k_008412_end:
.org 0x841A
m68k_00841a:
        move.b 0xf67b:w,0x200115:l
m68k_00841a_end:
.org 0x8422
m68k_008422:
        move.b 0xf67d:w,0x200117:l
m68k_008422_end:
.org 0x842A
m68k_00842a:
        move.b 0xf67f:w,0x200119:l
m68k_00842a_end:
.org 0x8432
m68k_008432:
        move.b 0xf374:w,0x20011b:l
m68k_008432_end:
.org 0x843A
m68k_00843a:
        move.b 0xf375:w,0x20011d:l
m68k_00843a_end:
.org 0x8442
m68k_008442:
        move.b 0xefd3:w,0x20011f:l
m68k_008442_end:
.org 0x844A
m68k_00844a:
        move.b 0xefe5:w,0x200121:l
m68k_00844a_end:
.org 0x8452
m68k_008452:
        move.b 0xefd7:w,0x200123:l
m68k_008452_end:
.org 0x845A
m68k_00845a:
        move.b 0xefd9:w,0x200125:l
m68k_00845a_end:
.org 0x8462
m68k_008462:
        movea.l #0x200127,%a0
m68k_008462_end:
.org 0x8468
m68k_008468:
        lea.l 0xa000:w,%a1
m68k_008468_end:
.org 0x846C
m68k_00846c:
        move.w #0x5,%d0
m68k_00846c_end:
.org 0x8470
m68k_008470:
        move.w #0x1,%d1
m68k_008470_end:
.org 0x8474
m68k_008474:
        move.w #0x28,%d2
m68k_008474_end:
.org 0x8478
m68k_008478:
        bsr.w (. + 3506)
m68k_008478_end:
.org 0x847C
m68k_00847c:
        lea.l 0xefaa:w,%a1
m68k_00847c_end:
.org 0x8480
m68k_008480:
        move.b (%a1)+,(%a0)+
m68k_008480_end:
.org 0x8482
m68k_008482:
        lea.l 0x1(%a0),%a0
m68k_008482_end:
.org 0x8486
m68k_008486:
        move.b (%a1)+,(%a0)+
m68k_008486_end:
.org 0x8488
m68k_008488:
        lea.l 0x1(%a0),%a0
m68k_008488_end:
.org 0x848C
m68k_00848c:
        move.b (%a1)+,(%a0)+
m68k_00848c_end:
.org 0x848E
m68k_00848e:
        lea.l 0x1(%a0),%a0
m68k_00848e_end:
.org 0x8492
m68k_008492:
        move.b (%a1)+,(%a0)+
m68k_008492_end:
.org 0x8494
m68k_008494:
        lea.l 0x1(%a0),%a0
m68k_008494_end:
.org 0x8498
m68k_008498:
        move.b (%a1)+,(%a0)+
m68k_008498_end:
.org 0x849A
m68k_00849a:
        lea.l 0x1(%a0),%a0
m68k_00849a_end:
.org 0x849E
m68k_00849e:
        lea.l 0xa028:w,%a1
m68k_00849e_end:
.org 0x84A2
m68k_0084a2:
        move.w #0x8,%d0
m68k_0084a2_end:
.org 0x84A6
m68k_0084a6:
        move.w #0x1,%d1
m68k_0084a6_end:
.org 0x84AA
m68k_0084aa:
        move.w #0x28,%d2
m68k_0084aa_end:
.org 0x84AE
m68k_0084ae:
        bsr.w (. + 3452)
m68k_0084ae_end:
.org 0x84B2
m68k_0084b2:
        lea.l 0xa050:w,%a1
m68k_0084b2_end:
.org 0x84B6
m68k_0084b6:
        move.w #0x8,%d0
m68k_0084b6_end:
.org 0x84BA
m68k_0084ba:
        move.w #0x1,%d1
m68k_0084ba_end:
.org 0x84BE
m68k_0084be:
        move.w #0x100,%d2
m68k_0084be_end:
.org 0x84C2
m68k_0084c2:
        bsr.w (. + 3432)
m68k_0084c2_end:
.org 0x84C6
m68k_0084c6:
        bsr.w (. + 928)
m68k_0084c6_end:
.org 0x84CA
m68k_0084ca:
        lea.l 0xd300:w,%a1
m68k_0084ca_end:
.org 0x84CE
m68k_0084ce:
        move.w #0x8,%d0
m68k_0084ce_end:
.org 0x84D2
m68k_0084d2:
        move.w #0x2,%d1
m68k_0084d2_end:
.org 0x84D6
m68k_0084d6:
        move.w #0x100,%d2
m68k_0084d6_end:
.org 0x84DA
m68k_0084da:
        bsr.w (. + 3408)
m68k_0084da_end:
.org 0x84DE
m68k_0084de:
        lea.l 0xd500:w,%a1
m68k_0084de_end:
.org 0x84E2
m68k_0084e2:
        move.w #0x9,%d0
m68k_0084e2_end:
.org 0x84E6
m68k_0084e6:
        move.w #0x2,%d1
m68k_0084e6_end:
.org 0x84EA
m68k_0084ea:
        move.w #0x100,%d2
m68k_0084ea_end:
.org 0x84EE
m68k_0084ee:
        bsr.w (. + 3388)
m68k_0084ee_end:
.org 0x84F2
m68k_0084f2:
        lea.l 0xb200:w,%a1
m68k_0084f2_end:
.org 0x84F6
m68k_0084f6:
        move.w #0x8,%d0
m68k_0084f6_end:
.org 0x84FA
m68k_0084fa:
        move.w #0x2,%d1
m68k_0084fa_end:
.org 0x84FE
m68k_0084fe:
        move.w #0x100,%d2
m68k_0084fe_end:
.org 0x8502
m68k_008502:
        bsr.w (. + 3368)
m68k_008502_end:
.org 0x8506
m68k_008506:
        lea.l 0xb400:w,%a1
m68k_008506_end:
.org 0x850A
m68k_00850a:
        move.w #0x8,%d0
m68k_00850a_end:
.org 0x850E
m68k_00850e:
        move.w #0x2,%d1
m68k_00850e_end:
.org 0x8512
m68k_008512:
        move.w #0x100,%d2
m68k_008512_end:
.org 0x8516
m68k_008516:
        bsr.w (. + 3348)
m68k_008516_end:
.org 0x851A
m68k_00851a:
        lea.l 0xb600:w,%a1
m68k_00851a_end:
.org 0x851E
m68k_00851e:
        move.w #0x8,%d0
m68k_00851e_end:
.org 0x8522
m68k_008522:
        move.w #0x2,%d1
m68k_008522_end:
.org 0x8526
m68k_008526:
        move.w #0x100,%d2
m68k_008526_end:
.org 0x852A
m68k_00852a:
        bsr.w (. + 3328)
m68k_00852a_end:
.org 0x852E
m68k_00852e:
        bsr.w (. + 1020)
m68k_00852e_end:
.org 0x8532
m68k_008532:
        lea.l 0xd300:w,%a1
m68k_008532_end:
.org 0x8536
m68k_008536:
        move.w #0x5,%d0
m68k_008536_end:
.org 0x853A
m68k_00853a:
        move.w #0x2,%d1
m68k_00853a_end:
.org 0x853E
m68k_00853e:
        move.w #0x100,%d2
m68k_00853e_end:
.org 0x8542
m68k_008542:
        bsr.w (. + 3304)
m68k_008542_end:
.org 0x8546
m68k_008546:
        lea.l 0xc000:w,%a1
m68k_008546_end:
.org 0x854A
m68k_00854a:
        move.w #0xa,%d0
m68k_00854a_end:
.org 0x854E
m68k_00854e:
        move.w #0x2,%d1
m68k_00854e_end:
.org 0x8552
m68k_008552:
        move.w #0x100,%d2
m68k_008552_end:
.org 0x8556
m68k_008556:
        bsr.w (. + 3284)
m68k_008556_end:
.org 0x855A
m68k_00855a:
        lea.l 0xbe00:w,%a1
m68k_00855a_end:
.org 0x855E
m68k_00855e:
        move.w #0xa,%d0
m68k_00855e_end:
.org 0x8562
m68k_008562:
        move.w #0x2,%d1
m68k_008562_end:
.org 0x8566
m68k_008566:
        move.w #0x100,%d2
m68k_008566_end:
.org 0x856A
m68k_00856a:
        bsr.w (. + 3264)
m68k_00856a_end:
.org 0x856E
m68k_00856e:
        lea.l 0xc200:w,%a1
m68k_00856e_end:
.org 0x8572
m68k_008572:
        move.w #0x7,%d0
m68k_008572_end:
.org 0x8576
m68k_008576:
        move.w #0x1,%d1
m68k_008576_end:
.org 0x857A
m68k_00857a:
        move.w #0x100,%d2
m68k_00857a_end:
.org 0x857E
m68k_00857e:
        bsr.w (. + 3244)
m68k_00857e_end:
.org 0x8582
m68k_008582:
        lea.l 0xc300:w,%a1
m68k_008582_end:
.org 0x8586
m68k_008586:
        move.w #0x7,%d0
m68k_008586_end:
.org 0x858A
m68k_00858a:
        move.w #0x1,%d1
m68k_00858a_end:
.org 0x858E
m68k_00858e:
        move.w #0x100,%d2
m68k_00858e_end:
.org 0x8592
m68k_008592:
        bsr.w (. + 3224)
m68k_008592_end:
.org 0x8596
m68k_008596:
        lea.l 0xc400:w,%a1
m68k_008596_end:
.org 0x859A
m68k_00859a:
        move.w #0x5,%d0
m68k_00859a_end:
.org 0x859E
m68k_00859e:
        move.w #0x1,%d1
m68k_00859e_end:
.org 0x85A2
m68k_0085a2:
        move.w #0x100,%d2
m68k_0085a2_end:
.org 0x85A6
m68k_0085a6:
        bsr.w (. + 3204)
m68k_0085a6_end:
.org 0x85AA
m68k_0085aa:
        lea.l 0xc500:w,%a1
m68k_0085aa_end:
.org 0x85AE
m68k_0085ae:
        move.w #0x7,%d0
m68k_0085ae_end:
.org 0x85B2
m68k_0085b2:
        move.w #0x1,%d1
m68k_0085b2_end:
.org 0x85B6
m68k_0085b6:
        move.w #0x100,%d2
m68k_0085b6_end:
.org 0x85BA
m68k_0085ba:
        bsr.w (. + 3184)
m68k_0085ba_end:
.org 0x85BE
m68k_0085be:
        lea.l 0xc700:w,%a1
m68k_0085be_end:
.org 0x85C2
m68k_0085c2:
        move.w #0x5,%d0
m68k_0085c2_end:
.org 0x85C6
m68k_0085c6:
        move.w #0x1,%d1
m68k_0085c6_end:
.org 0x85CA
m68k_0085ca:
        move.w #0x100,%d2
m68k_0085ca_end:
.org 0x85CE
m68k_0085ce:
        bsr.w (. + 3164)
m68k_0085ce_end:
.org 0x85D2
m68k_0085d2:
        lea.l 0xc800:w,%a1
m68k_0085d2_end:
.org 0x85D6
m68k_0085d6:
        move.w #0xe,%d0
m68k_0085d6_end:
.org 0x85DA
m68k_0085da:
        move.w #0x4,%d1
m68k_0085da_end:
.org 0x85DE
m68k_0085de:
        move.w #0x100,%d2
m68k_0085de_end:
.org 0x85E2
m68k_0085e2:
        bsr.w (. + 3144)
m68k_0085e2_end:
.org 0x85E6
m68k_0085e6:
        lea.l 0xcc00:w,%a1
m68k_0085e6_end:
.org 0x85EA
m68k_0085ea:
        move.w #0x8,%d0
m68k_0085ea_end:
.org 0x85EE
m68k_0085ee:
        move.w #0x1,%d1
m68k_0085ee_end:
.org 0x85F2
m68k_0085f2:
        move.w #0x100,%d2
m68k_0085f2_end:
.org 0x85F6
m68k_0085f6:
        bsr.w (. + 3124)
m68k_0085f6_end:
.org 0x85FA
m68k_0085fa:
        lea.l 0xe000:w,%a1
m68k_0085fa_end:
.org 0x85FE
m68k_0085fe:
        move.w #0x14,%d0
m68k_0085fe_end:
.org 0x8602
m68k_008602:
        move.w #0x4,%d1
m68k_008602_end:
.org 0x8606
m68k_008606:
        move.w #0x28,%d2
m68k_008606_end:
.org 0x860A
m68k_00860a:
        bsr.w (. + 3104)
m68k_00860a_end:
.org 0x860E
m68k_00860e:
        lea.l 0xe0a0:w,%a1
m68k_00860e_end:
.org 0x8612
m68k_008612:
        move.w #0x14,%d0
m68k_008612_end:
.org 0x8616
m68k_008616:
        move.w #0x4,%d1
m68k_008616_end:
.org 0x861A
m68k_00861a:
        move.w #0x28,%d2
m68k_00861a_end:
.org 0x861E
m68k_00861e:
        bsr.w (. + 3084)
m68k_00861e_end:
.org 0x8622
m68k_008622:
        lea.l 0xe140:w,%a1
m68k_008622_end:
.org 0x8626
m68k_008626:
        move.w #0xa,%d0
m68k_008626_end:
.org 0x862A
m68k_00862a:
        move.w #0x4,%d1
m68k_00862a_end:
.org 0x862E
m68k_00862e:
        move.w #0x28,%d2
m68k_00862e_end:
.org 0x8632
m68k_008632:
        bsr.w (. + 3064)
m68k_008632_end:
.org 0x8636
m68k_008636:
        lea.l 0xe1e0:w,%a1
m68k_008636_end:
.org 0x863A
m68k_00863a:
        move.w #0xa,%d0
m68k_00863a_end:
.org 0x863E
m68k_00863e:
        move.w #0x4,%d1
m68k_00863e_end:
.org 0x8642
m68k_008642:
        move.w #0x28,%d2
m68k_008642_end:
.org 0x8646
m68k_008646:
        bsr.w (. + 3044)
m68k_008646_end:
.org 0x864A
m68k_00864a:
        lea.l 0xe280:w,%a1
m68k_00864a_end:
.org 0x864E
m68k_00864e:
        move.w #0x7,%d0
m68k_00864e_end:
.org 0x8652
m68k_008652:
        move.w #0x4,%d1
m68k_008652_end:
.org 0x8656
m68k_008656:
        move.w #0x28,%d2
m68k_008656_end:
.org 0x865A
m68k_00865a:
        bsr.w (. + 3024)
m68k_00865a_end:
.org 0x865E
m68k_00865e:
        lea.l 0xe320:w,%a1
m68k_00865e_end:
.org 0x8662
m68k_008662:
        move.w #0x7,%d0
m68k_008662_end:
.org 0x8666
m68k_008666:
        move.w #0x4,%d1
m68k_008666_end:
.org 0x866A
m68k_00866a:
        move.w #0x28,%d2
m68k_00866a_end:
.org 0x866E
m68k_00866e:
        bsr.w (. + 3004)
m68k_00866e_end:
.org 0x8672
m68k_008672:
        lea.l 0xe3c0:w,%a1
m68k_008672_end:
.org 0x8676
m68k_008676:
        move.w #0x7,%d0
m68k_008676_end:
.org 0x867A
m68k_00867a:
        move.w #0x4,%d1
m68k_00867a_end:
.org 0x867E
m68k_00867e:
        move.w #0x28,%d2
m68k_00867e_end:
.org 0x8682
m68k_008682:
        bsr.w (. + 2984)
m68k_008682_end:
.org 0x8686
m68k_008686:
        lea.l 0xe5a0:w,%a1
m68k_008686_end:
.org 0x868A
m68k_00868a:
        move.w #0x7,%d0
m68k_00868a_end:
.org 0x868E
m68k_00868e:
        move.w #0x4,%d1
m68k_00868e_end:
.org 0x8692
m68k_008692:
        move.w #0x28,%d2
m68k_008692_end:
.org 0x8696
m68k_008696:
        bsr.w (. + 2964)
m68k_008696_end:
.org 0x869A
m68k_00869a:
        lea.l 0xf428:w,%a1
m68k_00869a_end:
.org 0x869E
m68k_00869e:
        move.w #0x4,%d0
m68k_00869e_end:
.org 0x86A2
m68k_0086a2:
        move.w #0x1,%d1
m68k_0086a2_end:
.org 0x86A6
m68k_0086a6:
        move.w #0x28,%d2
m68k_0086a6_end:
.org 0x86AA
m68k_0086aa:
        bsr.w (. + 2944)
m68k_0086aa_end:
.org 0x86AE
m68k_0086ae:
        lea.l 0xe640:w,%a1
m68k_0086ae_end:
.org 0x86B2
m68k_0086b2:
        move.w #0x9,%d0
m68k_0086b2_end:
.org 0x86B6
m68k_0086b6:
        move.w #0x2,%d1
m68k_0086b6_end:
.org 0x86BA
m68k_0086ba:
        move.w #0x10,%d2
m68k_0086ba_end:
.org 0x86BE
m68k_0086be:
        bsr.w (. + 2924)
m68k_0086be_end:
.org 0x86C2
m68k_0086c2:
        lea.l 0xf460:w,%a1
m68k_0086c2_end:
.org 0x86C6
m68k_0086c6:
        move.w #0x9,%d0
m68k_0086c6_end:
.org 0x86CA
m68k_0086ca:
        move.w #0x2,%d1
m68k_0086ca_end:
.org 0x86CE
m68k_0086ce:
        move.w #0x28,%d2
m68k_0086ce_end:
.org 0x86D2
m68k_0086d2:
        bsr.w (. + 2904)
m68k_0086d2_end:
.org 0x86D6
m68k_0086d6:
        lea.l 0xe660:w,%a1
m68k_0086d6_end:
.org 0x86DA
m68k_0086da:
        move.w #0x14,%d0
m68k_0086da_end:
.org 0x86DE
m68k_0086de:
        move.w #0x4,%d1
m68k_0086de_end:
.org 0x86E2
m68k_0086e2:
        move.w #0x28,%d2
m68k_0086e2_end:
.org 0x86E6
m68k_0086e6:
        bsr.w (. + 2884)
m68k_0086e6_end:
.org 0x86EA
m68k_0086ea:
        move.b 0xe700:w,(%a0)+
m68k_0086ea_end:
.org 0x86EE
m68k_0086ee:
        lea.l 0x1(%a0),%a0
m68k_0086ee_end:
.org 0x86F2
m68k_0086f2:
        move.b 0xe701:w,(%a0)+
m68k_0086f2_end:
.org 0x86F6
m68k_0086f6:
        lea.l 0x1(%a0),%a0
m68k_0086f6_end:
.org 0x86FA
m68k_0086fa:
        lea.l 0xe710:w,%a1
m68k_0086fa_end:
.org 0x86FE
m68k_0086fe:
        move.w #0x1f,%d2
m68k_0086fe_end:
.org 0x8702
m68k_008702:
        move.b (%a1)+,(%a0)+
m68k_008702_end:
.org 0x8704
m68k_008704:
        lea.l 0x1(%a0),%a0
m68k_008704_end:
.org 0x8708
m68k_008708:
        dbra %d2,(. + -6)
m68k_008708_end:
.org 0x870C
m68k_00870c:
        lea.l 0xe778:w,%a1
m68k_00870c_end:
.org 0x8710
m68k_008710:
        move.w #0x11,%d0
m68k_008710_end:
.org 0x8714
m68k_008714:
        move.w #0x4,%d1
m68k_008714_end:
.org 0x8718
m68k_008718:
        move.w #0x28,%d2
m68k_008718_end:
.org 0x871C
m68k_00871c:
        bsr.w (. + 2830)
m68k_00871c_end:
.org 0x8720
m68k_008720:
        bsr.w (. + 360)
m68k_008720_end:
.org 0x8724
m68k_008724:
        lea.l 0xd300:w,%a1
m68k_008724_end:
.org 0x8728
m68k_008728:
        move.w #0x9,%d0
m68k_008728_end:
.org 0x872C
m68k_00872c:
        move.w #0x2,%d1
m68k_00872c_end:
.org 0x8730
m68k_008730:
        move.w #0x28,%d2
m68k_008730_end:
.org 0x8734
m68k_008734:
        bsr.w (. + 2806)
m68k_008734_end:
.org 0x8738
m68k_008738:
        lea.l 0xd350:w,%a1
m68k_008738_end:
.org 0x873C
m68k_00873c:
        move.w #0xe,%d0
m68k_00873c_end:
.org 0x8740
m68k_008740:
        move.w #0x2,%d1
m68k_008740_end:
.org 0x8744
m68k_008744:
        move.w #0x28,%d2
m68k_008744_end:
.org 0x8748
m68k_008748:
        bsr.w (. + 2786)
m68k_008748_end:
.org 0x874C
m68k_00874c:
        lea.l 0xd3a0:w,%a1
m68k_00874c_end:
.org 0x8750
m68k_008750:
        move.w #0x9,%d0
m68k_008750_end:
.org 0x8754
m68k_008754:
        move.w #0x2,%d1
m68k_008754_end:
.org 0x8758
m68k_008758:
        move.w #0x28,%d2
m68k_008758_end:
.org 0x875C
m68k_00875c:
        bsr.w (. + 2766)
m68k_00875c_end:
.org 0x8760
m68k_008760:
        lea.l 0xd3f0:w,%a1
m68k_008760_end:
.org 0x8764
m68k_008764:
        move.w #0x7,%d0
m68k_008764_end:
.org 0x8768
m68k_008768:
        move.w #0x2,%d1
m68k_008768_end:
.org 0x876C
m68k_00876c:
        move.w #0x28,%d2
m68k_00876c_end:
.org 0x8770
m68k_008770:
        bsr.w (. + 2746)
m68k_008770_end:
.org 0x8774
m68k_008774:
        lea.l 0xd440:w,%a1
m68k_008774_end:
.org 0x8778
m68k_008778:
        move.w #0x9,%d0
m68k_008778_end:
.org 0x877C
m68k_00877c:
        move.w #0x2,%d1
m68k_00877c_end:
.org 0x8780
m68k_008780:
        move.w #0x28,%d2
m68k_008780_end:
.org 0x8784
m68k_008784:
        bsr.w (. + 2726)
m68k_008784_end:
.org 0x8788
m68k_008788:
        lea.l 0xd490:w,%a1
m68k_008788_end:
.org 0x878C
m68k_00878c:
        move.w #0xa,%d0
m68k_00878c_end:
.org 0x8790
m68k_008790:
        move.w #0x2,%d1
m68k_008790_end:
.org 0x8794
m68k_008794:
        move.w #0x28,%d2
m68k_008794_end:
.org 0x8798
m68k_008798:
        bsr.w (. + 2706)
m68k_008798_end:
.org 0x8922
m68k_008922:
        move.b %d7,(%a0)+
m68k_008922_end:
.org 0x8924
m68k_008924:
        lea.l 0x1(%a0),%a0
m68k_008924_end:
.org 0x8966
m68k_008966:
        move.b (%a1)+,%d0
m68k_008966_end:
.org 0x8968
m68k_008968:
        andi.l #0x7f,%d0
m68k_008968_end:
.org 0x896E
m68k_00896e:
        move.w #0x7,%d1
m68k_00896e_end:
.org 0x8972
m68k_008972:
        bsr.w (. + 110)
m68k_008972_end:
.org 0x8976
m68k_008976:
        move.b (%a1)+,%d0
m68k_008976_end:
.org 0x8978
m68k_008978:
        andi.l #0x7f,%d0
m68k_008978_end:
.org 0x897E
m68k_00897e:
        move.w #0x7,%d1
m68k_00897e_end:
.org 0x8982
m68k_008982:
        bsr.w (. + 94)
m68k_008982_end:
.org 0x8986
m68k_008986:
        addq.w #0x1,%a1
m68k_008986_end:
.org 0x8988
m68k_008988:
        move.b (%a1)+,%d0
m68k_008988_end:
.org 0x898A
m68k_00898a:
        move.w #0x4,%d1
m68k_00898a_end:
.org 0x898E
m68k_00898e:
        bsr.w (. + 82)
m68k_00898e_end:
.org 0x8992
m68k_008992:
        move.b (%a1)+,%d0
m68k_008992_end:
.org 0x8994
m68k_008994:
        lsl.w #0x8,%d0
m68k_008994_end:
.org 0x8996
m68k_008996:
        move.b (%a1)+,%d0
m68k_008996_end:
.org 0x8998
m68k_008998:
        lsl.l #0x8,%d0
m68k_008998_end:
.org 0x899A
m68k_00899a:
        move.b (%a1)+,%d0
m68k_00899a_end:
.org 0x899C
m68k_00899c:
        lsl.l #0x8,%d0
m68k_00899c_end:
.org 0x899E
m68k_00899e:
        move.b (%a1)+,%d0
m68k_00899e_end:
.org 0x89A0
m68k_0089a0:
        move.w #0x12,%d1
m68k_0089a0_end:
.org 0x89A4
m68k_0089a4:
        bsr.w (. + 60)
m68k_0089a4_end:
.org 0x89A8
m68k_0089a8:
        move.b (%a1)+,%d0
m68k_0089a8_end:
.org 0x89AA
m68k_0089aa:
        lsl.w #0x8,%d0
m68k_0089aa_end:
.org 0x89AC
m68k_0089ac:
        move.b (%a1)+,%d0
m68k_0089ac_end:
.org 0x89AE
m68k_0089ae:
        lsl.l #0x8,%d0
m68k_0089ae_end:
.org 0x89B0
m68k_0089b0:
        move.b (%a1)+,%d0
m68k_0089b0_end:
.org 0x89B2
m68k_0089b2:
        lsl.l #0x8,%d0
m68k_0089b2_end:
.org 0x89B4
m68k_0089b4:
        move.b (%a1)+,%d0
m68k_0089b4_end:
.org 0x89B6
m68k_0089b6:
        move.w #0x14,%d1
m68k_0089b6_end:
.org 0x89BA
m68k_0089ba:
        bsr.w (. + 38)
m68k_0089ba_end:
.org 0x89BE
m68k_0089be:
        subq.w #0x1,%d7
m68k_0089be_end:
.org 0x89C0
m68k_0089c0:
        move.b (%a1)+,%d0
m68k_0089c0_end:
.org 0x89C2
m68k_0089c2:
        andi.l #0xff,%d0
m68k_0089c2_end:
.org 0x89C8
m68k_0089c8:
        move.w #0x8,%d1
m68k_0089c8_end:
.org 0x89CC
m68k_0089cc:
        bsr.w (. + 20)
m68k_0089cc_end:
.org 0x89D0
m68k_0089d0:
        dbra %d7,(. + -16)
m68k_0089d0_end:
.org 0x89D4
m68k_0089d4:
        bra.w (. + -134)
m68k_0089d4_end:
.org 0x89EE
m68k_0089ee:
        move.b %d0,(%a0)+
m68k_0089ee_end:
.org 0x89F0
m68k_0089f0:
        lea.l 0x1(%a0),%a0
m68k_0089f0_end:
.org 0x89F4
m68k_0089f4:
        subq.w #0x8,%d4
m68k_0089f4_end:
.org 0x89F6
m68k_0089f6:
        lsr.l #0x8,%d0
m68k_0089f6_end:
.org 0x89F8
m68k_0089f8:
        bra.b (. + -18)
m68k_0089f8_end:
.org 0x8EEA
m68k_008eea:
        lea.l 0xa150:w,%a2
m68k_008eea_end:
.org 0x8EEE
m68k_008eee:
        lea.l 0xd300:w,%a3
m68k_008eee_end:
.org 0x8EF2
m68k_008ef2:
        lea.l 0xd500:w,%a4
m68k_008ef2_end:
.org 0x8EF6
m68k_008ef6:
        move.w #0xff,%d0
m68k_008ef6_end:
.org 0x8EFA
m68k_008efa:
        move.w (%a3)+,%d1
m68k_008efa_end:
.org 0x8EFC
m68k_008efc:
        lsl.w #0x7,%d1
m68k_008efc_end:
.org 0x8EFE
m68k_008efe:
        move.w %d1,(%a2)+
m68k_008efe_end:
.org 0x8F00
m68k_008f00:
        move.w (%a4)+,%d1
m68k_008f00_end:
.org 0x8F02
m68k_008f02:
        lsl.w #0x7,%d1
m68k_008f02_end:
.org 0x8F04
m68k_008f04:
        move.w %d1,(%a2)+
m68k_008f04_end:
.org 0x8F06
m68k_008f06:
        dbra %d0,(. + -12)
m68k_008f06_end:
.org 0x8F0A
m68k_008f0a:
        rts
m68k_008f0a_end:
.org 0x8F0C
m68k_008f0c:
        lea.l 0xd300:w,%a1
m68k_008f0c_end:
.org 0x8F10
m68k_008f10:
        lea.l 0xe818:w,%a2
m68k_008f10_end:
.org 0x8F14
m68k_008f14:
        lea.l 0xcd00:w,%a3
m68k_008f14_end:
.org 0x8F18
m68k_008f18:
        move.w #0x27,%d0
m68k_008f18_end:
.org 0x8F1C
m68k_008f1c:
        move.w (%a1),%d1
m68k_008f1c_end:
.org 0x8F1E
m68k_008f1e:
        cmpi.w #0x1ff,%d1
m68k_008f1e_end:
.org 0x8F22
m68k_008f22:
        bne.w (. + 12)
m68k_008f22_end:
.org 0x8F26
m68k_008f26:
        move.w #0xffff,%d1
m68k_008f26_end:
.org 0x8F2A
m68k_008f2a:
        bra.w (. + 10)
m68k_008f2a_end:
.org 0x8F2E
m68k_008f2e:
        move.b #0x2,(%a3, %d1.w)
m68k_008f2e_end:
.org 0x8F34
m68k_008f34:
        move.w %d1,(%a2)+
m68k_008f34_end:
.org 0x8F36
m68k_008f36:
        move.w 0x50(%a1),%d1
m68k_008f36_end:
.org 0x8F3A
m68k_008f3a:
        cmpi.w #0x3fff,%d1
m68k_008f3a_end:
.org 0x8F3E
m68k_008f3e:
        bne.w (. + 8)
m68k_008f3e_end:
.org 0x8F42
m68k_008f42:
        move.w #0xffff,%d1
m68k_008f42_end:
.org 0x8F46
m68k_008f46:
        move.w %d1,(%a2)+
m68k_008f46_end:
.org 0x8F48
m68k_008f48:
        move.w 0xa0(%a1),%d1
m68k_008f48_end:
.org 0x8F4C
m68k_008f4c:
        cmpi.w #0x1ff,%d1
m68k_008f4c_end:
.org 0x8F50
m68k_008f50:
        bne.w (. + 12)
m68k_008f50_end:
.org 0x8F54
m68k_008f54:
        move.w #0xffff,%d1
m68k_008f54_end:
.org 0x8F58
m68k_008f58:
        bra.w (. + 10)
m68k_008f58_end:
.org 0x8F5C
m68k_008f5c:
        move.b #0x3,(%a3, %d1.w)
m68k_008f5c_end:
.org 0x8F62
m68k_008f62:
        move.w %d1,(%a2)+
m68k_008f62_end:
.org 0x8F64
m68k_008f64:
        move.w 0xf0(%a1),%d1
m68k_008f64_end:
.org 0x8F68
m68k_008f68:
        cmpi.w #0x7f,%d1
m68k_008f68_end:
.org 0x8F6C
m68k_008f6c:
        beq.w (. + 12)
m68k_008f6c_end:
.org 0x8F70
m68k_008f70:
        mulu.w #0x64,%d1
m68k_008f70_end:
.org 0x8F74
m68k_008f74:
        bra.w (. + 8)
m68k_008f74_end:
.org 0x8F78
m68k_008f78:
        move.w #0xffff,%d1
m68k_008f78_end:
.org 0x8F7C
m68k_008f7c:
        move.w %d1,(%a2)+
m68k_008f7c_end:
.org 0x8F7E
m68k_008f7e:
        move.w 0x140(%a1),%d1
m68k_008f7e_end:
.org 0x8F82
m68k_008f82:
        cmpi.w #0x1ff,%d1
m68k_008f82_end:
.org 0x8F86
m68k_008f86:
        bne.w (. + 12)
m68k_008f86_end:
.org 0x8F8A
m68k_008f8a:
        move.w #0xffff,%d1
m68k_008f8a_end:
.org 0x8F8E
m68k_008f8e:
        bra.w (. + 10)
m68k_008f8e_end:
.org 0x8F92
m68k_008f92:
        move.b #0x4,(%a3, %d1.w)
m68k_008f92_end:
.org 0x8F98
m68k_008f98:
        move.w %d1,(%a2)+
m68k_008f98_end:
.org 0x8F9A
m68k_008f9a:
        move.w 0x190(%a1),%d1
m68k_008f9a_end:
.org 0x8F9E
m68k_008f9e:
        cmpi.w #0x3ff,%d1
m68k_008f9e_end:
.org 0x8FA2
m68k_008fa2:
        bne.w (. + 8)
m68k_008fa2_end:
.org 0x8FA6
m68k_008fa6:
        move.w #0xffff,%d1
m68k_008fa6_end:
.org 0x8FAA
m68k_008faa:
        move.w %d1,(%a2)+
m68k_008faa_end:
.org 0x8FAC
m68k_008fac:
        addq.w #0x2,%a1
m68k_008fac_end:
.org 0x8FAE
m68k_008fae:
        dbra %d0,(. + -146)
m68k_008fae_end:
.org 0x8FB2
m68k_008fb2:
        rts
m68k_008fb2_end:
.org 0x8FB4
m68k_008fb4:
        lea.l 0xce00:w,%a1
m68k_008fb4_end:
.org 0x8FB8
m68k_008fb8:
        clr.w %d3
m68k_008fb8_end:
.org 0x8FBA
m68k_008fba:
        clr.w %d4
m68k_008fba_end:
.org 0x8FBC
m68k_008fbc:
        move.w #0x27,%d7
m68k_008fbc_end:
.org 0x8FC0
m68k_008fc0:
        move.w #0x6,%d5
m68k_008fc0_end:
.org 0x8FC4
m68k_008fc4:
        move.w #0x3f,%d6
m68k_008fc4_end:
.org 0x8FC8
m68k_008fc8:
        bsr.w (. + 54)
m68k_008fc8_end:
.org 0x8FCC
m68k_008fcc:
        move.b %d2,0x3(%a1)
m68k_008fcc_end:
.org 0x8FD0
m68k_008fd0:
        move.w #0x7,%d5
m68k_008fd0_end:
.org 0x8FD4
m68k_008fd4:
        move.w #0x7f,%d6
m68k_008fd4_end:
.org 0x8FD8
m68k_008fd8:
        bsr.w (. + 38)
m68k_008fd8_end:
.org 0x8FDC
m68k_008fdc:
        move.b %d2,0x2(%a1)
m68k_008fdc_end:
.org 0x8FE0
m68k_008fe0:
        bsr.w (. + 30)
m68k_008fe0_end:
.org 0x8FE4
m68k_008fe4:
        move.b %d2,0x1(%a1)
m68k_008fe4_end:
.org 0x8FE8
m68k_008fe8:
        move.w #0x2,%d5
m68k_008fe8_end:
.org 0x8FEC
m68k_008fec:
        move.w #0x3,%d6
m68k_008fec_end:
.org 0x8FF0
m68k_008ff0:
        bsr.w (. + 14)
m68k_008ff0_end:
.org 0x8FF4
m68k_008ff4:
        move.b %d2,(%a1)
m68k_008ff4_end:
.org 0x8FF6
m68k_008ff6:
        addq.w #0x4,%a1
m68k_008ff6_end:
.org 0x8FF8
m68k_008ff8:
        dbra %d7,(. + -56)
m68k_008ff8_end:
.org 0x8FFC
m68k_008ffc:
        rts
m68k_008ffc_end:
.org 0x8FFE
m68k_008ffe:
        cmp.w %d5,%d4
m68k_008ffe_end:
.org 0x9000
m68k_009000:
        bcc.w (. + 18)
m68k_009000_end:
.org 0x9004
m68k_009004:
        clr.w %d1
m68k_009004_end:
.org 0x9006
m68k_009006:
        move.b (%a0)+,%d1
m68k_009006_end:
.org 0x9008
m68k_009008:
        lea.l 0x1(%a0),%a0
m68k_009008_end:
.org 0x900C
m68k_00900c:
        lsl.w %d4,%d1
m68k_00900c_end:
.org 0x900E
m68k_00900e:
        or.w %d1,%d3
m68k_00900e_end:
.org 0x9010
m68k_009010:
        addq.w #0x8,%d4
m68k_009010_end:
.org 0x9012
m68k_009012:
        move.w %d3,%d2
m68k_009012_end:
.org 0x9014
m68k_009014:
        and.w %d6,%d2
m68k_009014_end:
.org 0x9016
m68k_009016:
        lsr.w %d5,%d3
m68k_009016_end:
.org 0x9018
m68k_009018:
        sub.w %d5,%d4
m68k_009018_end:
.org 0x901A
m68k_00901a:
        rts
m68k_00901a_end:
.org 0x901C
m68k_00901c:
        lea.l 0xd300:w,%a1
m68k_00901c_end:
.org 0x9020
m68k_009020:
        lea.l 0xb800:w,%a2
m68k_009020_end:
.org 0x9024
m68k_009024:
        move.w #0xff,%d0
m68k_009024_end:
.org 0x9028
m68k_009028:
        move.w (%a1)+,%d1
m68k_009028_end:
.org 0x902A
m68k_00902a:
        mulu.w #0x5,%d1
m68k_00902a_end:
.org 0x902E
m68k_00902e:
        move.w %d1,(%a2)+
m68k_00902e_end:
.org 0x9030
m68k_009030:
        dbra %d0,(. + -8)
m68k_009030_end:
.org 0x9034
m68k_009034:
        rts
m68k_009034_end:
.org 0x9036
m68k_009036:
        lea.l 0x9000:w,%a1
m68k_009036_end:
.org 0x903A
m68k_00903a:
        clr.w %d0
m68k_00903a_end:
.org 0x903C
m68k_00903c:
        clr.w %d1
m68k_00903c_end:
.org 0x903E
m68k_00903e:
        move.w #0x4,%d2
m68k_00903e_end:
.org 0x9042
m68k_009042:
        moveq #15,%d3
m68k_009042_end:
.org 0x9044
m68k_009044:
        bsr.w (. + 384)
m68k_009044_end:
.org 0x9048
m68k_009048:
        move.b %d4,(%a1)+
m68k_009048_end:
.org 0x904A
m68k_00904a:
        beq.w (. + 136)
m68k_00904a_end:
.org 0x904E
m68k_00904e:
        move.w %d4,%d7
m68k_00904e_end:
.org 0x9050
m68k_009050:
        move.w #0x7,%d2
m68k_009050_end:
.org 0x9054
m68k_009054:
        moveq #127,%d3
m68k_009054_end:
.org 0x9056
m68k_009056:
        bsr.w (. + 366)
m68k_009056_end:
.org 0x905A
m68k_00905a:
        move.b %d4,(%a1)+
m68k_00905a_end:
.org 0x905C
m68k_00905c:
        bsr.w (. + 360)
m68k_00905c_end:
.org 0x9060
m68k_009060:
        move.b %d4,(%a1)+
m68k_009060_end:
.org 0x9062
m68k_009062:
        addq.w #0x1,%a1
m68k_009062_end:
.org 0x9064
m68k_009064:
        move.w #0x4,%d2
m68k_009064_end:
.org 0x9068
m68k_009068:
        moveq #15,%d3
m68k_009068_end:
.org 0x906A
m68k_00906a:
        bsr.w (. + 346)
m68k_00906a_end:
.org 0x906E
m68k_00906e:
        move.b %d4,(%a1)+
m68k_00906e_end:
.org 0x9070
m68k_009070:
        move.w #0x12,%d2
m68k_009070_end:
.org 0x9074
m68k_009074:
        move.l #0x3ffff,%d3
m68k_009074_end:
.org 0x907A
m68k_00907a:
        bsr.w (. + 330)
m68k_00907a_end:
.org 0x907E
m68k_00907e:
        move.b %d4,0x3(%a1)
m68k_00907e_end:
.org 0x9082
m68k_009082:
        lsr.l #0x8,%d4
m68k_009082_end:
.org 0x9084
m68k_009084:
        move.b %d4,0x2(%a1)
m68k_009084_end:
.org 0x9088
m68k_009088:
        lsr.l #0x8,%d4
m68k_009088_end:
.org 0x908A
m68k_00908a:
        move.b %d4,0x1(%a1)
m68k_00908a_end:
.org 0x908E
m68k_00908e:
        lsr.w #0x8,%d4
m68k_00908e_end:
.org 0x9090
m68k_009090:
        move.b %d4,(%a1)
m68k_009090_end:
.org 0x9092
m68k_009092:
        addq.w #0x4,%a1
m68k_009092_end:
.org 0x9094
m68k_009094:
        move.w #0x14,%d2
m68k_009094_end:
.org 0x9098
m68k_009098:
        move.l #0xfffff,%d3
m68k_009098_end:
.org 0x909E
m68k_00909e:
        bsr.w (. + 294)
m68k_00909e_end:
.org 0x90A2
m68k_0090a2:
        move.b %d4,0x3(%a1)
m68k_0090a2_end:
.org 0x90A6
m68k_0090a6:
        lsr.l #0x8,%d4
m68k_0090a6_end:
.org 0x90A8
m68k_0090a8:
        move.b %d4,0x2(%a1)
m68k_0090a8_end:
.org 0x90AC
m68k_0090ac:
        lsr.l #0x8,%d4
m68k_0090ac_end:
.org 0x90AE
m68k_0090ae:
        move.b %d4,0x1(%a1)
m68k_0090ae_end:
.org 0x90B2
m68k_0090b2:
        lsr.w #0x8,%d4
m68k_0090b2_end:
.org 0x90B4
m68k_0090b4:
        move.b %d4,(%a1)
m68k_0090b4_end:
.org 0x90B6
m68k_0090b6:
        addq.w #0x4,%a1
m68k_0090b6_end:
.org 0x90B8
m68k_0090b8:
        subq.w #0x1,%d7
m68k_0090b8_end:
.org 0x90BA
m68k_0090ba:
        move.w #0x8,%d2
m68k_0090ba_end:
.org 0x90BE
m68k_0090be:
        move.l #0xff,%d3
m68k_0090be_end:
.org 0x90C4
m68k_0090c4:
        bsr.w (. + 256)
m68k_0090c4_end:
.org 0x90C8
m68k_0090c8:
        move.b %d4,(%a1)+
m68k_0090c8_end:
.org 0x90CA
m68k_0090ca:
        dbra %d7,(. + -16)
m68k_0090ca_end:
.org 0x90CE
m68k_0090ce:
        bra.w (. + -144)
m68k_0090ce_end:
.org 0x90D2
m68k_0090d2:
        bsr.w (. + 294)
m68k_0090d2_end:
.org 0x90D6
m68k_0090d6:
        rts
m68k_0090d6_end:
.org 0x9148
m68k_009148:
        lea.l 0xe640:w,%a1
m68k_009148_end:
.org 0x914C
m68k_00914c:
        move.w #0xf,%d0
m68k_00914c_end:
.org 0x9150
m68k_009150:
        move.w (%a1),%d1
m68k_009150_end:
.org 0x9152
m68k_009152:
        cmpi.w #0x1ff,%d1
m68k_009152_end:
.org 0x9156
m68k_009156:
        bne.w (. + 8)
m68k_009156_end:
.org 0x915A
m68k_00915a:
        move.w #0xffff,%d1
m68k_00915a_end:
.org 0x915E
m68k_00915e:
        move.w %d1,(%a1)+
m68k_00915e_end:
.org 0x9160
m68k_009160:
        dbra %d0,(. + -16)
m68k_009160_end:
.org 0x9164
m68k_009164:
        rts
m68k_009164_end:
.org 0x9166
m68k_009166:
        lea.l 0xf460:w,%a1
m68k_009166_end:
.org 0x916A
m68k_00916a:
        move.w #0x27,%d0
m68k_00916a_end:
.org 0x916E
m68k_00916e:
        move.w (%a1),%d1
m68k_00916e_end:
.org 0x9170
m68k_009170:
        cmpi.w #0x1ff,%d1
m68k_009170_end:
.org 0x9174
m68k_009174:
        bne.w (. + 8)
m68k_009174_end:
.org 0x9178
m68k_009178:
        move.w #0xffff,%d1
m68k_009178_end:
.org 0x917C
m68k_00917c:
        move.w %d1,(%a1)+
m68k_00917c_end:
.org 0x917E
m68k_00917e:
        dbra %d0,(. + -16)
m68k_00917e_end:
.org 0x9182
m68k_009182:
        rts
m68k_009182_end:
.org 0x9184
m68k_009184:
        lea.l 0xf428:w,%a1
m68k_009184_end:
.org 0x9188
m68k_009188:
        move.w #0x27,%d0
m68k_009188_end:
.org 0x918C
m68k_00918c:
        move.b (%a1),%d1
m68k_00918c_end:
.org 0x918E
m68k_00918e:
        cmpi.b #0xf,%d1
m68k_00918e_end:
.org 0x9192
m68k_009192:
        bne.w (. + 8)
m68k_009192_end:
.org 0x9196
m68k_009196:
        move.b #0xff,%d1
m68k_009196_end:
.org 0x919A
m68k_00919a:
        move.b %d1,(%a1)+
m68k_00919a_end:
.org 0x919C
m68k_00919c:
        dbra %d0,(. + -16)
m68k_00919c_end:
.org 0x91A0
m68k_0091a0:
        rts
m68k_0091a0_end:
.org 0x91A2
m68k_0091a2:
        lea.l 0xd300:w,%a2
m68k_0091a2_end:
.org 0x91A6
m68k_0091a6:
        lea.l 0xd310:w,%a3
m68k_0091a6_end:
.org 0x91AA
m68k_0091aa:
        lea.l 0xd320:w,%a4
m68k_0091aa_end:
.org 0x91AE
m68k_0091ae:
        lea.l 0xd330:w,%a5
m68k_0091ae_end:
.org 0x91B2
m68k_0091b2:
        move.w #0xf,%d0
m68k_0091b2_end:
.org 0x91B6
m68k_0091b6:
        move.b (%a2)+,(%a1)+
m68k_0091b6_end:
.org 0x91B8
m68k_0091b8:
        move.b (%a3)+,(%a1)+
m68k_0091b8_end:
.org 0x91BA
m68k_0091ba:
        move.b (%a4)+,(%a1)+
m68k_0091ba_end:
.org 0x91BC
m68k_0091bc:
        move.b (%a5)+,(%a1)+
m68k_0091bc_end:
.org 0x91BE
m68k_0091be:
        dbra %d0,(. + -8)
m68k_0091be_end:
.org 0x91C2
m68k_0091c2:
        rts
m68k_0091c2_end:
.org 0x91C4
m68k_0091c4:
        moveq #0,%d4
m68k_0091c4_end:
.org 0x91C6
m68k_0091c6:
        move.b %d0,%d4
m68k_0091c6_end:
.org 0x91C8
m68k_0091c8:
        ror.l #0x8,%d4
m68k_0091c8_end:
.org 0x91CA
m68k_0091ca:
        cmp.w %d2,%d1
m68k_0091ca_end:
.org 0x91CC
m68k_0091cc:
        bcc.w (. + 16)
m68k_0091cc_end:
.org 0x91D0
m68k_0091d0:
        move.b (%a0)+,%d4
m68k_0091d0_end:
.org 0x91D2
m68k_0091d2:
        move.b %d4,%d0
m68k_0091d2_end:
.org 0x91D4
m68k_0091d4:
        lea.l 0x1(%a0),%a0
m68k_0091d4_end:
.org 0x91D8
m68k_0091d8:
        addq.w #0x8,%d1
m68k_0091d8_end:
.org 0x91DA
m68k_0091da:
        bra.b (. + -18)
m68k_0091da_end:
.org 0x91DC
m68k_0091dc:
        move.w #0x20,%d5
m68k_0091dc_end:
.org 0x91E0
m68k_0091e0:
        sub.w %d1,%d5
m68k_0091e0_end:
.org 0x91E2
m68k_0091e2:
        cmpi.w #0x8,%d5
m68k_0091e2_end:
.org 0x91E6
m68k_0091e6:
        bls.w (. + 10)
m68k_0091e6_end:
.org 0x91EA
m68k_0091ea:
        lsr.l #0x8,%d4
m68k_0091ea_end:
.org 0x91EC
m68k_0091ec:
        subq.w #0x8,%d5
m68k_0091ec_end:
.org 0x91EE
m68k_0091ee:
        bra.b (. + -12)
m68k_0091ee_end:
.org 0x91F0
m68k_0091f0:
        lsr.l %d5,%d4
m68k_0091f0_end:
.org 0x91F2
m68k_0091f2:
        and.l %d3,%d4
m68k_0091f2_end:
.org 0x91F4
m68k_0091f4:
        sub.w %d2,%d1
m68k_0091f4_end:
.org 0x91F6
m68k_0091f6:
        rts
m68k_0091f6_end:
.org 0x91F8
m68k_0091f8:
        lea.l 0x9000:w,%a1
m68k_0091f8_end:
.org 0x91FC
m68k_0091fc:
        lea.l 0xc400:w,%a2
m68k_0091fc_end:
.org 0x9200
m68k_009200:
        move.b (%a1),%d0
m68k_009200_end:
.org 0x9202
m68k_009202:
        beq.w (. + 38)
m68k_009202_end:
.org 0x9206
m68k_009206:
        move.w %d0,%d1
m68k_009206_end:
.org 0x9208
m68k_009208:
        subq.w #0x1,%d1
m68k_009208_end:
.org 0x920A
m68k_00920a:
        moveq #0,%d2
m68k_00920a_end:
.org 0x920C
m68k_00920c:
        clr.w %d3
m68k_00920c_end:
.org 0x920E
m68k_00920e:
        move.b 0xd(%a1, %d1.w),%d3
m68k_00920e_end:
.org 0x9212
m68k_009212:
        move.b (%a2, %d3.w),%d3
m68k_009212_end:
.org 0x9216
m68k_009216:
        add.w %d3,%d2
m68k_009216_end:
.org 0x9218
m68k_009218:
        dbra %d1,(. + -12)
m68k_009218_end:
.org 0x921C
m68k_00921c:
        divu.w %d0,%d2
m68k_00921c_end:
.org 0x921E
m68k_00921e:
        move.b %d2,0x3(%a1)
m68k_00921e_end:
.org 0x9222
m68k_009222:
        lea.l 0xd(%a1, %d0.w),%a1
m68k_009222_end:
.org 0x9226
m68k_009226:
        bra.b (. + -38)
m68k_009226_end:
.org 0x9228
m68k_009228:
        rts
m68k_009228_end:
.org 0x9294
m68k_009294:
        move.b %d3,(%a1)
m68k_009294_end:
.org 0x9296
m68k_009296:
        addq.w #0x2,%a1
m68k_009296_end:
.org 0x945C
m68k_00945c:
        move.w #0x8f02,0xc00004:l
m68k_00945c_end:
.org 0x9464
m68k_009464:
        move.l #0x66300003,0xc00004:l
m68k_009464_end:
.org 0x946E
m68k_00946e:
        move.w #0x8035,0xc00000:l
m68k_00946e_end:
.org 0x9476
m68k_009476:
        move.w #0x8036,0xc00000:l
m68k_009476_end:
.org 0x9D0C
m68k_009d0c:
        bcs.w (. + 222)
m68k_009d0c_end:
.org 0x9D10
m68k_009d10:
        cmpi.w #0x2,0xf36c:w
m68k_009d10_end:
.org 0x9D16
m68k_009d16:
        beq.w (. + 172)
m68k_009d16_end:
.org 0x9D1A
m68k_009d1a:
        tst.w 0xf36c:w
m68k_009d1a_end:
.org 0x9D1E
m68k_009d1e:
        bne.w (. + 244)
m68k_009d1e_end:
.org 0x9D22
m68k_009d22:
        bset.b #0x3,0xf31c:w
m68k_009d22_end:
.org 0x9D28
m68k_009d28:
        bset.b #0x1,0xf31c:w
m68k_009d28_end:
.org 0x9D2E
m68k_009d2e:
        bclr.b #0x2,0xf31c:w
m68k_009d2e_end:
.org 0x9D34
m68k_009d34:
        move.w #0x2,0xf38e:w
m68k_009d34_end:
.org 0x9D3A
m68k_009d3a:
        clr.w 0xf576:w
m68k_009d3a_end:
.org 0x9D3E
m68k_009d3e:
        clr.w 0xf396:w
m68k_009d3e_end:
.org 0x9D42
m68k_009d42:
        move.w #0x1,0xf36c:w
m68k_009d42_end:
.org 0x9D48
m68k_009d48:
        jsr 0x133a:l
m68k_009d48_end:
.org 0x9D4E
m68k_009d4e:
        clr.w 0xf65a:w
m68k_009d4e_end:
.org 0x9D52
m68k_009d52:
        move.w #0x8,0xcfd2:w
m68k_009d52_end:
.org 0x9D58
m68k_009d58:
        move.w #0xac,%d0
m68k_009d58_end:
.org 0x9D5C
m68k_009d5c:
        jsr 0x808a:l
m68k_009d5c_end:
.org 0x9D62
m68k_009d62:
        bra.w (. + 176)
m68k_009d62_end:
.org 0x9DC2
m68k_009dc2:
        bset.b #0x1,0xf31c:w
m68k_009dc2_end:
.org 0x9DC8
m68k_009dc8:
        bclr.b #0x2,0xf31c:w
m68k_009dc8_end:
.org 0x9DCE
m68k_009dce:
        move.w #0x208,0xf612:w
m68k_009dce_end:
.org 0x9DD4
m68k_009dd4:
        move.w #0x4,0xf362:w
m68k_009dd4_end:
.org 0x9DDA
m68k_009dda:
        move.w #0x9d,0xf38c:w
m68k_009dda_end:
.org 0x9DE0
m68k_009de0:
        move.w #0x6,0xf65a:w
m68k_009de0_end:
.org 0x9DE6
m68k_009de6:
        bra.w (. + 44)
m68k_009de6_end:
.org 0x9DEA
m68k_009dea:
        move.w #0x205,0xf612:w
m68k_009dea_end:
.org 0x9DF0
m68k_009df0:
        move.w #0x1,0xf65a:w
m68k_009df0_end:
.org 0x9DF6
m68k_009df6:
        move.w #0x1,0xff3938:l
m68k_009df6_end:
.org 0x9DFE
m68k_009dfe:
        cmpi.w #0x2,0xf36c:w
m68k_009dfe_end:
.org 0x9E04
m68k_009e04:
        bne.w (. + 14)
m68k_009e04_end:
.org 0x9E08
m68k_009e08:
        move.w #0x97,0xf38c:w
m68k_009e08_end:
.org 0x9E0E
m68k_009e0e:
        clr.w 0xf576:w
m68k_009e0e_end:
.org 0x9E12
m68k_009e12:
        rts
m68k_009e12_end:
.org 0x9E14
m68k_009e14:
        lea.l 0x9000:w,%a0
m68k_009e14_end:
.org 0x9E18
m68k_009e18:
        move.w 0xf35e:w,%d0
m68k_009e18_end:
.org 0x9E1C
m68k_009e1c:
        subq.w #0x2,%d0
m68k_009e1c_end:
.org 0x9E1E
m68k_009e1e:
        lsr.w #0x4,%d0
m68k_009e1e_end:
.org 0x9E20
m68k_009e20:
        move.w 0xf360:w,%d1
m68k_009e20_end:
.org 0x9E24
m68k_009e24:
        subq.w #0x2,%d1
m68k_009e24_end:
.org 0x9E26
m68k_009e26:
        lsr.w #0x4,%d1
m68k_009e26_end:
.org 0x9E28
m68k_009e28:
        move.b (%a0),%d2
m68k_009e28_end:
.org 0x9E2A
m68k_009e2a:
        beq.b (. + 46)
m68k_009e2a_end:
.org 0x9E2C
m68k_009e2c:
        andi.b #0x7f,%d2
m68k_009e2c_end:
.org 0x9E30
m68k_009e30:
        move.b 0x4(%a0),%d3
m68k_009e30_end:
.org 0x9E34
m68k_009e34:
        cmp.b 0x1(%a0),%d0
m68k_009e34_end:
.org 0x9E38
m68k_009e38:
        bne.b (. + 8)
m68k_009e38_end:
.org 0x9E3A
m68k_009e3a:
        cmp.b 0x2(%a0),%d1
m68k_009e3a_end:
.org 0x9E3E
m68k_009e3e:
        beq.b (. + 14)
m68k_009e3e_end:
.org 0x9E40
m68k_009e40:
        andi.w #0xf,%d2
m68k_009e40_end:
.org 0x9E44
m68k_009e44:
        addi.w #0xd,%d2
m68k_009e44_end:
.org 0x9E48
m68k_009e48:
        adda.w %d2,%a0
m68k_009e48_end:
.org 0x9E4A
m68k_009e4a:
        bra.b (. + -34)
m68k_009e4a_end:
.org 0x9E4C
m68k_009e4c:
        move.l %a0,0xff382c:l
m68k_009e4c_end:
.org 0x9E52
m68k_009e52:
        ori.w #0x1,%sr
m68k_009e52_end:
.org 0x9E56
m68k_009e56:
        bra.b (. + 6)
m68k_009e56_end:
.org 0x9E58
m68k_009e58:
        andi.w #0xfffe,%sr
m68k_009e58_end:
.org 0x9E5C
m68k_009e5c:
        rts
m68k_009e5c_end:
.org 0x9E5E
m68k_009e5e:
        btst.b #0x1,0xf31c:w
m68k_009e5e_end:
.org 0x9E64
m68k_009e64:
        bne.w (. + 36)
m68k_009e64_end:
.org 0x9E68
m68k_009e68:
        cmpi.w #0x12,0xf322:w
m68k_009e68_end:
.org 0x9E6E
m68k_009e6e:
        bcc.w (. + 134)
m68k_009e6e_end:
.org 0x9E72
m68k_009e72:
        bsr.w (. + 266)
m68k_009e72_end:
.org 0x9E76
m68k_009e76:
        tst.w 0xf37e:w
m68k_009e76_end:
.org 0x9E7A
m68k_009e7a:
        bne.w (. + 122)
m68k_009e7a_end:
.org 0x9E7E
m68k_009e7e:
        move.w #0x2c,0xf600:w
m68k_009e7e_end:
.org 0x9E84
m68k_009e84:
        bra.w (. + 112)
m68k_009e84_end:
.org 0x9E88
m68k_009e88:
        tst.w 0xf322:w
m68k_009e88_end:
.org 0x9E8C
m68k_009e8c:
        beq.w (. + 16)
m68k_009e8c_end:
.org 0x9E90
m68k_009e90:
        subq.w #0x2,0xf322:w
m68k_009e90_end:
.org 0x9E94
m68k_009e94:
        bsr.w (. + 232)
m68k_009e94_end:
.org 0x9E98
m68k_009e98:
        bra.w (. + 92)
m68k_009e98_end:
.org 0x9E9C
m68k_009e9c:
        btst.b #0x3,0xf31c:w
m68k_009e9c_end:
.org 0x9EA2
m68k_009ea2:
        beq.w (. + 34)
m68k_009ea2_end:
.org 0x9EA6
m68k_009ea6:
        cmpi.w #0x2,0xf38e:w
m68k_009ea6_end:
.org 0x9EAC
m68k_009eac:
        bne.w (. + 72)
m68k_009eac_end:
.org 0x9EB0
m68k_009eb0:
        move.w #0x30,0xf600:w
m68k_009eb0_end:
.org 0x9EB6
m68k_009eb6:
        move.w 0xf612:w,0xf38a:w
m68k_009eb6_end:
.org 0x9EBC
m68k_009ebc:
        clr.w 0xf38c:w
m68k_009ebc_end:
.org 0x9EC0
m68k_009ec0:
        bra.w (. + 52)
m68k_009ec0_end:
.org 0x9EC4
m68k_009ec4:
        btst.b #0x2,0xf31c:w
m68k_009ec4_end:
.org 0x9ECA
m68k_009eca:
        beq.w (. + 42)
m68k_009eca_end:
.org 0x9ECE
m68k_009ece:
        move.w 0xf360:w,%d0
m68k_009ece_end:
.org 0x9ED2
m68k_009ed2:
        sub.w 0xf318:w,%d0
m68k_009ed2_end:
.org 0x9ED6
m68k_009ed6:
        cmpi.w #0xa0,%d0
m68k_009ed6_end:
.org 0x9EDA
m68k_009eda:
        bcs.w (. + 14)
m68k_009eda_end:
.org 0x9EDE
m68k_009ede:
        bclr.b #0x0,0xf31c:w
m68k_009ede_end:
.org 0x9EE4
m68k_009ee4:
        bra.w (. + 10)
m68k_009ee4_end:
.org 0x9EE8
m68k_009ee8:
        bset.b #0x0,0xf31c:w
m68k_009ee8_end:
.org 0x9EEE
m68k_009eee:
        bclr.b #0x1,0xf31c:w
m68k_009eee_end:
.org 0x9EF4
m68k_009ef4:
        btst.b #0x7,0xf603:w
m68k_009ef4_end:
.org 0x9EFA
m68k_009efa:
        beq.w (. + 46)
m68k_009efa_end:
.org 0x9EFE
m68k_009efe:
        eori.b #0x4,0xf31c:w
m68k_009efe_end:
.org 0x9F04
m68k_009f04:
        btst.b #0x2,0xf31c:w
m68k_009f04_end:
.org 0x9F0A
m68k_009f0a:
        beq.w (. + 14)
m68k_009f0a_end:
.org 0x9F0E
m68k_009f0e:
        move.w #0xad,%d0
m68k_009f0e_end:
.org 0x9F12
m68k_009f12:
        jsr 0x808a:l
m68k_009f12_end:
.org 0x9F18
m68k_009f18:
        btst.b #0x2,0xf31c:w
m68k_009f18_end:
.org 0x9F1E
m68k_009f1e:
        bne.w (. + 10)
m68k_009f1e_end:
.org 0x9F22
m68k_009f22:
        bset.b #0x1,0xf31c:w
m68k_009f22_end:
.org 0x9F28
m68k_009f28:
        btst.b #0x2,0xf31c:w
m68k_009f28_end:
.org 0x9F2E
m68k_009f2e:
        beq.w (. + 76)
m68k_009f2e_end:
.org 0x9F32
m68k_009f32:
        move.w 0xf360:w,%d0
m68k_009f32_end:
.org 0x9F36
m68k_009f36:
        sub.w 0xf318:w,%d0
m68k_009f36_end:
.org 0x9F3A
m68k_009f3a:
        cmpi.w #0xa0,%d0
m68k_009f3a_end:
.org 0x9F3E
m68k_009f3e:
        bcc.w (. + 34)
m68k_009f3e_end:
.org 0x9F42
m68k_009f42:
        btst.b #0x0,0xf31c:w
m68k_009f42_end:
.org 0x9F48
m68k_009f48:
        bne.w (. + 14)
m68k_009f48_end:
.org 0x9F4C
m68k_009f4c:
        bset.b #0x1,0xf31c:w
m68k_009f4c_end:
.org 0x9F52
m68k_009f52:
        bra.w (. + 40)
m68k_009f52_end:
.org 0x9F56
m68k_009f56:
        bclr.b #0x1,0xf31c:w
m68k_009f56_end:
.org 0x9F5C
m68k_009f5c:
        bra.w (. + 30)
m68k_009f5c_end:
.org 0x9F60
m68k_009f60:
        btst.b #0x0,0xf31c:w
m68k_009f60_end:
.org 0x9F66
m68k_009f66:
        beq.w (. + 14)
m68k_009f66_end:
.org 0x9F6A
m68k_009f6a:
        bset.b #0x1,0xf31c:w
m68k_009f6a_end:
.org 0x9F70
m68k_009f70:
        bra.w (. + 10)
m68k_009f70_end:
.org 0x9F74
m68k_009f74:
        bclr.b #0x1,0xf31c:w
m68k_009f74_end:
.org 0x9F7A
m68k_009f7a:
        rts
m68k_009f7a_end:
.org 0x9F7C
m68k_009f7c:
        move.w 0xf31a:w,%d0
m68k_009f7c_end:
.org 0x9F80
m68k_009f80:
        lea.l 0xd100:w,%a0
m68k_009f80_end:
.org 0x9F84
m68k_009f84:
        adda.w %d0,%a0
m68k_009f84_end:
.org 0x9F86
m68k_009f86:
        move.w #0x12,(%a0)
m68k_009f86_end:
.org 0x9F8A
m68k_009f8a:
        move.w #0x12,0x28(%a0)
m68k_009f8a_end:
.org 0x9F90
m68k_009f90:
        move.w #0x11,%d2
m68k_009f90_end:
.org 0x9F94
m68k_009f94:
        clr.w %d1
m68k_009f94_end:
.org 0x9F96
m68k_009f96:
        btst.b #0x0,0xf31c:w
m68k_009f96_end:
.org 0x9F9C
m68k_009f9c:
        beq.w (. + 8)
m68k_009f9c_end:
.org 0x9FA0
m68k_009fa0:
        move.w #0x28,%d1
m68k_009fa0_end:
.org 0x9FA4
m68k_009fa4:
        move.w 0xf322:w,%d0
m68k_009fa4_end:
.org 0x9FA8
m68k_009fa8:
        lsl.w #0x7,%d0
m68k_009fa8_end:
.org 0x9FAA
m68k_009faa:
        addi.w #0xc102,%d0
m68k_009faa_end:
.org 0x9FAE
m68k_009fae:
        add.w %d1,%d0
m68k_009fae_end:
.org 0x9FB0
m68k_009fb0:
        move.w %d0,0x2(%a0)
m68k_009fb0_end:
.org 0x9FB4
m68k_009fb4:
        addi.w #0x80,%d0
m68k_009fb4_end:
.org 0x9FB8
m68k_009fb8:
        move.w %d0,0x2a(%a0)
m68k_009fb8_end:
.org 0x9FBC
m68k_009fbc:
        addq.l #0x4,%a0
m68k_009fbc_end:
.org 0x9FBE
m68k_009fbe:
        btst.b #0x1,0xf31c:w
m68k_009fbe_end:
.org 0x9FC4
m68k_009fc4:
        bne.w (. + 56)
m68k_009fc4_end:
.org 0x9FC8
m68k_009fc8:
        lea.l 0xd323a:l,%a1
m68k_009fc8_end:
.org 0x9FCE
m68k_009fce:
        move.w 0xf322:w,%d0
m68k_009fce_end:
.org 0x9FD2
m68k_009fd2:
        move.w #0x24,%d1
m68k_009fd2_end:
.org 0x9FD6
m68k_009fd6:
        mulu.w %d1,%d0
m68k_009fd6_end:
.org 0x9FD8
m68k_009fd8:
        lea.l (%a1, %d0.w),%a1
m68k_009fd8_end:
.org 0x9FDC
m68k_009fdc:
        move.w (%a1)+,(%a0)+
m68k_009fdc_end:
.org 0x9FDE
m68k_009fde:
        dbra %d2,(. + -2)
m68k_009fde_end:
.org 0x9FE2
m68k_009fe2:
        move.w #0x11,%d2
m68k_009fe2_end:
.org 0x9FE6
m68k_009fe6:
        addq.l #0x4,%a0
m68k_009fe6_end:
.org 0x9FE8
m68k_009fe8:
        move.w (%a1)+,(%a0)+
m68k_009fe8_end:
.org 0x9FEA
m68k_009fea:
        dbra %d2,(. + -2)
m68k_009fea_end:
.org 0x9FEE
m68k_009fee:
        clr.w (%a0)
m68k_009fee_end:
.org 0x9FF0
m68k_009ff0:
        addi.w #0x50,0xf31a:w
m68k_009ff0_end:
.org 0x9FF6
m68k_009ff6:
        addq.w #0x2,0xf322:w
m68k_009ff6_end:
.org 0x9FFA
m68k_009ffa:
        rts
m68k_009ffa_end:
.org 0x9FFC
m68k_009ffc:
        move.w #0x8000,(%a0)+
m68k_009ffc_end:
.org 0xA000
m68k_00a000:
        dbra %d2,(. + -4)
m68k_00a000_end:
.org 0xA004
m68k_00a004:
        move.w #0x11,%d2
m68k_00a004_end:
.org 0xA008
m68k_00a008:
        addq.l #0x4,%a0
m68k_00a008_end:
.org 0xA00A
m68k_00a00a:
        move.w #0x8000,(%a0)+
m68k_00a00a_end:
.org 0xA00E
m68k_00a00e:
        dbra %d2,(. + -4)
m68k_00a00e_end:
.org 0xA012
m68k_00a012:
        clr.w (%a0)
m68k_00a012_end:
.org 0xA014
m68k_00a014:
        addi.w #0x50,0xf31a:w
m68k_00a014_end:
.org 0xA01A
m68k_00a01a:
        rts
m68k_00a01a_end:
.org 0xA37A
m68k_00a37a:
        cmpi.w #0xf,0xf362:w
m68k_00a37a_end:
.org 0xA380
m68k_00a380:
        beq.w (. + 88)
m68k_00a380_end:
.org 0xA38E
m68k_00a38e:
        tst.w 0xefe0:w
m68k_00a38e_end:
.org 0xA392
m68k_00a392:
        beq.w (. + 14)
m68k_00a392_end:
.org 0xA396
m68k_00a396:
        jsr 0x1a16e:l
m68k_00a396_end:
.org 0xA39C
m68k_00a39c:
        bra.w (. + 60)
m68k_00a39c_end:
.org 0xA3C0
m68k_00a3c0:
        move.w 0xf604:w,0xf602:w
m68k_00a3c0_end:
.org 0xA3C6
m68k_00a3c6:
        bra.w (. + 18)
m68k_00a3c6_end:
.org 0xA3E8
m68k_00a3e8:
        lea.l 0xfb80:w,%a0
m68k_00a3e8_end:
.org 0xAC6E
m68k_00ac6e:
        move.w 0x4(%a0),%d7
m68k_00ac6e_end:
.org 0xAC72
m68k_00ac72:
        andi.l #0xffff,%d7
m68k_00ac72_end:
.org 0xAC78
m68k_00ac78:
        lsl.w #0x4,%d7
m68k_00ac78_end:
.org 0xAC7A
m68k_00ac7a:
        swap %d7
m68k_00ac7a_end:
.org 0xAC7C
m68k_00ac7c:
        andi.w #0x3,%d7
m68k_00ac7c_end:
.org 0xAC80
m68k_00ac80:
        lsl.w #0x3,%d7
m68k_00ac80_end:
.org 0xAC82
m68k_00ac82:
        addi.w #0x8,%d7
m68k_00ac82_end:
.org 0xAC86
m68k_00ac86:
        add.w %d7,%d5
m68k_00ac86_end:
.org 0xAC88
m68k_00ac88:
        neg.w %d5
m68k_00ac88_end:
.org 0xACAC
m68k_00acac:
        move.l %d6,%d7
m68k_00acac_end:
.org 0xACAE
m68k_00acae:
        swap %d7
m68k_00acae_end:
.org 0xACB0
m68k_00acb0:
        andi.w #0xc,%d7
m68k_00acb0_end:
.org 0xACB4
m68k_00acb4:
        lsl.w #0x1,%d7
m68k_00acb4_end:
.org 0xACB6
m68k_00acb6:
        addi.w #0x8,%d7
m68k_00acb6_end:
.org 0xACBA
m68k_00acba:
        add.w %d7,%d5
m68k_00acba_end:
.org 0xACBC
m68k_00acbc:
        neg.w %d5
m68k_00acbc_end:
.org 0xAED8
m68k_00aed8:
        moveq #0,%d6
m68k_00aed8_end:
.org 0xAEDA
m68k_00aeda:
        moveq #0,%d7
m68k_00aeda_end:
.org 0xAEDC
m68k_00aedc:
        move.w #0x7,%d4
m68k_00aedc_end:
.org 0xAEE0
m68k_00aee0:
        lsl.l #0x4,%d6
m68k_00aee0_end:
.org 0xAEE2
m68k_00aee2:
        lsl.l #0x4,%d7
m68k_00aee2_end:
.org 0xAEE4
m68k_00aee4:
        or.w %d0,%d6
m68k_00aee4_end:
.org 0xAEE6
m68k_00aee6:
        or.w %d1,%d7
m68k_00aee6_end:
.org 0xAEE8
m68k_00aee8:
        dbra %d4,(. + -8)
m68k_00aee8_end:
.org 0xAEEC
m68k_00aeec:
        move.w #0xf,%d4
m68k_00aeec_end:
.org 0xAEF0
m68k_00aef0:
        move.l %d6,0x40(%a1)
m68k_00aef0_end:
.org 0xAEF4
m68k_00aef4:
        move.l %d6,(%a1)+
m68k_00aef4_end:
.org 0xAEF6
m68k_00aef6:
        dbra %d4,(. + -6)
m68k_00aef6_end:
.org 0xAEFA
m68k_00aefa:
        move.l %d7,-0x24(%a1)
m68k_00aefa_end:
.org 0xAEFE
m68k_00aefe:
        move.l %d7,0x1c(%a1)
m68k_00aefe_end:
.org 0xAF02
m68k_00af02:
        bra.b (. + -56)
m68k_00af02_end:
.org 0xAF1E
m68k_00af1e:
        movem.l %d4-%d7,-(%a7)
m68k_00af1e_end:
.org 0xAF22
m68k_00af22:
        clr.w %d4
m68k_00af22_end:
.org 0xAF24
m68k_00af24:
        move.b (%a0)+,%d4
m68k_00af24_end:
.org 0xAF26
m68k_00af26:
        lsl.w #0x3,%d4
m68k_00af26_end:
.org 0xAF28
m68k_00af28:
        lea.l 0x896dc:l,%a2
m68k_00af28_end:
.org 0xAF2E
m68k_00af2e:
        lea.l (%a2, %d4.w),%a2
m68k_00af2e_end:
.org 0xAF32
m68k_00af32:
        move.w #0x7,%d5
m68k_00af32_end:
.org 0xAF36
m68k_00af36:
        bsr.b (. + -50)
m68k_00af36_end:
.org 0xAF38
m68k_00af38:
        move.l %d7,(%a1)+
m68k_00af38_end:
.org 0xAF3A
m68k_00af3a:
        dbra %d5,(. + -4)
m68k_00af3a_end:
.org 0xAF3E
m68k_00af3e:
        dbra %d3,(. + -28)
m68k_00af3e_end:
.org 0xAF42
m68k_00af42:
        movem.l (%a7)+,%d4-%d7
m68k_00af42_end:
.org 0xAF46
m68k_00af46:
        rts
m68k_00af46_end:
.org 0xAFA2
m68k_00afa2:
        movea.l #0xffffffff,%a1
m68k_00afa2_end:
.org 0xAFA8
m68k_00afa8:
        bra.b (. + 12)
m68k_00afa8_end:
.org 0xAFC0
m68k_00afc0:
        movea.l #0xffffffff,%a2
m68k_00afc0_end:
.org 0xAFC6
m68k_00afc6:
        bra.b (. + 12)
m68k_00afc6_end:
.org 0xAFDC
m68k_00afdc:
        movea.l #0xffffffff,%a3
m68k_00afdc_end:
.org 0xAFE2
m68k_00afe2:
        bra.b (. + 12)
m68k_00afe2_end:
.org 0xAFF8
m68k_00aff8:
        movea.l #0xffffffff,%a5
m68k_00aff8_end:
.org 0xAFFE
m68k_00affe:
        bra.b (. + 12)
m68k_00affe_end:
.org 0xB01E
m68k_00b01e:
        movea.l #0xffffffff,%a2
m68k_00b01e_end:
.org 0xB024
m68k_00b024:
        bra.b (. + 12)
m68k_00b024_end:
.org 0xB040
m68k_00b040:
        movea.l #0xffffffff,%a3
m68k_00b040_end:
.org 0xB046
m68k_00b046:
        bra.b (. + 12)
m68k_00b046_end:
.org 0xB0E6
m68k_00b0e6:
        movea.l %a1,%a4
m68k_00b0e6_end:
.org 0xB0E8
m68k_00b0e8:
        bra.b (. + 24)
m68k_00b0e8_end:
.org 0xB15A
m68k_00b15a:
        clr.w %d6
m68k_00b15a_end:
.org 0xB15C
m68k_00b15c:
        moveq #64,%d7
m68k_00b15c_end:
.org 0xB15E
m68k_00b15e:
        rts
m68k_00b15e_end:
.org 0xB20A
m68k_00b20a:
        clr.w %d6
m68k_00b20a_end:
.org 0xB20C
m68k_00b20c:
        moveq #64,%d7
m68k_00b20c_end:
.org 0xB20E
m68k_00b20e:
        rts
m68k_00b20e_end:
.org 0xBD54
m68k_00bd54:
        bsr.w (. + -24450)
m68k_00bd54_end:
.org 0xBE34
m68k_00be34:
        addq.w #0x1,%d1
m68k_00be34_end:
.org 0xBE36
m68k_00be36:
        bra.b (. + -6)
m68k_00be36_end:
.org 0xBF1A
m68k_00bf1a:
        move.l #0xc0000006,%d0
m68k_00bf1a_end:
.org 0xBF20
m68k_00bf20:
        move.w #0x8,%d1
m68k_00bf20_end:
.org 0xBF24
m68k_00bf24:
        move.w #0xc3a0,%d2
m68k_00bf24_end:
.org 0xBF28
m68k_00bf28:
        lea.l 16(%pc),%a0
m68k_00bf28_end:
.org 0xBF2C
m68k_00bf2c:
        jsr 0x26bfa:l
m68k_00bf2c_end:
.org 0xBF32
m68k_00bf32:
        bclr.b #0x3,0xf3a5:w
m68k_00bf32_end:
.org 0xBFCC
m68k_00bfcc:
        btst.l #0x3,%d0
m68k_00bfcc_end:
.org 0xBFD0
m68k_00bfd0:
        bne.b (. + 16)
m68k_00bfd0_end:
.org 0xBFD2
m68k_00bfd2:
        subq.w #0x1,0xf388:w
m68k_00bfd2_end:
.org 0xBFD6
m68k_00bfd6:
        bpl.b (. + 62)
m68k_00bfd6_end:
.org 0xBFD8
m68k_00bfd8:
        move.w 0xf384:w,0xf388:w
m68k_00bfd8_end:
.org 0xBFDE
m68k_00bfde:
        bra.b (. + 54)
m68k_00bfde_end:
.org 0xBFE0
m68k_00bfe0:
        addq.w #0x1,0xf388:w
m68k_00bfe0_end:
.org 0xBFE4
m68k_00bfe4:
        move.w 0xf388:w,%d1
m68k_00bfe4_end:
.org 0xBFE8
m68k_00bfe8:
        cmp.w 0xf384:w,%d1
m68k_00bfe8_end:
.org 0xBFEC
m68k_00bfec:
        bls.b (. + 40)
m68k_00bfec_end:
.org 0xBFEE
m68k_00bfee:
        clr.w 0xf388:w
m68k_00bfee_end:
.org 0xBFF2
m68k_00bff2:
        bra.b (. + 34)
m68k_00bff2_end:
.org 0xC002
m68k_00c002:
        clr.w 0xf386:w
m68k_00c002_end:
.org 0xC006
m68k_00c006:
        bra.b (. + 14)
m68k_00c006_end:
.org 0xC008
m68k_00c008:
        subq.w #0x1,0xf386:w
m68k_00c008_end:
.org 0xC00C
m68k_00c00c:
        bpl.b (. + 8)
m68k_00c00c_end:
.org 0xC00E
m68k_00c00e:
        move.w 0xf382:w,0xf386:w
m68k_00c00e_end:
.org 0xC01C
m68k_00c01c:
        cmpi.w #0x2,0xf380:w
m68k_00c01c_end:
.org 0xC022
m68k_00c022:
        bne.b (. + 16)
m68k_00c022_end:
.org 0xC03C
m68k_00c03c:
        tst.w 0xf650:w
m68k_00c03c_end:
.org 0xC040
m68k_00c040:
        bne.b (. + 58)
m68k_00c040_end:
.org 0xC042
m68k_00c042:
        tst.w 0xf380:w
m68k_00c042_end:
.org 0xC046
m68k_00c046:
        bne.w (. + 34)
m68k_00c046_end:
.org 0xC04A
m68k_00c04a:
        move.w 0xf388:w,%d0
m68k_00c04a_end:
.org 0xC04E
m68k_00c04e:
        addq.w #0x1,%d0
m68k_00c04e_end:
.org 0xC050
m68k_00c050:
        move.b %d0,0xf578:w
m68k_00c050_end:
.org 0xC054
m68k_00c054:
        move.b #0xc,0xf579:w
m68k_00c054_end:
.org 0xC05A
m68k_00c05a:
        addq.w #0x2,0xf576:w
m68k_00c05a_end:
.org 0xC05E
m68k_00c05e:
        move.w #0x3,0xf388:w
m68k_00c05e_end:
.org 0xC064
m68k_00c064:
        bra.w (. + 64)
m68k_00c064_end:
.org 0xC068
m68k_00c068:
        clr.l 0xf39e:w
m68k_00c068_end:
.org 0xC06C
m68k_00c06c:
        clr.l 0xf3ba:w
m68k_00c06c_end:
.org 0xC070
m68k_00c070:
        addq.w #0x1,0xf362:w
m68k_00c070_end:
.org 0xC074
m68k_00c074:
        clr.w 0xf36a:w
m68k_00c074_end:
.org 0xC078
m68k_00c078:
        bra.b (. + 60)
m68k_00c078_end:
.org 0xC090
m68k_00c090:
        move.w #0x8,0xcfd2:w
m68k_00c090_end:
.org 0xC096
m68k_00c096:
        bra.w (. + 30)
m68k_00c096_end:
.org 0xC118
m68k_00c118:
        ori.w #0x1,%sr
m68k_00c118_end:
.org 0xC706
m68k_00c706:
        move.w #0x1,0xf386:w
m68k_00c706_end:
.org 0xC70C
m68k_00c70c:
        cmpi.w #0x6d,0xf38c:w
m68k_00c70c_end:
.org 0xC712
m68k_00c712:
        beq.w (. + 50)
m68k_00c712_end:
.org 0xC716
m68k_00c716:
        move.w #0x208,0xf612:w
m68k_00c716_end:
.org 0xC71C
m68k_00c71c:
        move.w #0x2,0xf362:w
m68k_00c71c_end:
.org 0xC722
m68k_00c722:
        cmpi.w #0xac,0xf38c:w
m68k_00c722_end:
.org 0xC728
m68k_00c728:
        beq.b (. + 8)
m68k_00c728_end:
.org 0xC72A
m68k_00c72a:
        clr.w 0xf36a:w
m68k_00c72a_end:
.org 0xC72E
m68k_00c72e:
        bra.b (. + 52)
m68k_00c72e_end:
.org 0xC730
m68k_00c730:
        bsr.w (. + 258)
m68k_00c730_end:
.org 0xC734
m68k_00c734:
        move.w #0x12,0xf36a:w
m68k_00c734_end:
.org 0xC73A
m68k_00c73a:
        bra.b (. + 40)
m68k_00c73a_end:
.org 0xC774
m68k_00c774:
        subq.w #0x1,0xf608:w
m68k_00c774_end:
.org 0xC778
m68k_00c778:
        bne.b (. + 22)
m68k_00c778_end:
.org 0xC77A
m68k_00c77a:
        move.w #0xc,0xf608:w
m68k_00c77a_end:
.org 0xC780
m68k_00c780:
        eori.w #0x1,0xf386:w
m68k_00c780_end:
.org 0xC786
m68k_00c786:
        bra.b (. + 8)
m68k_00c786_end:
.org 0xC7BE
m68k_00c7be:
        move.w #0x58,%d0
m68k_00c7be_end:
.org 0xD49A
m68k_00d49a:
        btst.b #0x5,0xf603:w
m68k_00d49a_end:
.org 0xD4A0
m68k_00d4a0:
        bne.w (. + 58)
m68k_00d4a0_end:
.org 0xD4A4
m68k_00d4a4:
        move.b 0xf602:w,%d0
m68k_00d4a4_end:
.org 0xD4A8
m68k_00d4a8:
        andi.w #0x3,%d0
m68k_00d4a8_end:
.org 0xD4AC
m68k_00d4ac:
        bne.w (. + 12)
m68k_00d4ac_end:
.org 0xD4B0
m68k_00d4b0:
        btst.b #0x3,0xf321:w
m68k_00d4b0_end:
.org 0xD4B6
m68k_00d4b6:
        bne.b (. + 36)
m68k_00d4b6_end:
.org 0xD4B8
m68k_00d4b8:
        lea.l 34(%pc),%a0
m68k_00d4b8_end:
.org 0xD4BC
m68k_00d4bc:
        nop
m68k_00d4bc_end:
.org 0xD4BE
m68k_00d4be:
        move.w 0xf3f0:w,%d0
m68k_00d4be_end:
.org 0xD4C2
m68k_00d4c2:
        lsl.w #0x1,%d0
m68k_00d4c2_end:
.org 0xD4C4
m68k_00d4c4:
        add.w 0xf3f0:w,%d0
m68k_00d4c4_end:
.org 0xD4C8
m68k_00d4c8:
        lsl.w #0x3,%d0
m68k_00d4c8_end:
.org 0xD4CA
m68k_00d4ca:
        addi.w #0x40,%d0
m68k_00d4ca_end:
.org 0xD4CE
m68k_00d4ce:
        move.w #0x68,%d1
m68k_00d4ce_end:
.org 0xD4D2
m68k_00d4d2:
        clr.w %d2
m68k_00d4d2_end:
.org 0xD4D4
m68k_00d4d4:
        jsr 0xac08:l
m68k_00d4d4_end:
.org 0xD4DA
m68k_00d4da:
        rts
m68k_00d4da_end:
.org 0xD526
m68k_00d526:
        lea.l 0xd100:w,%a0
m68k_00d526_end:
.org 0xD52A
m68k_00d52a:
        adda.w 0xf31a:w,%a0
m68k_00d52a_end:
.org 0xD52E
m68k_00d52e:
        move.w #0xc39a,%d1
m68k_00d52e_end:
.org 0xD532
m68k_00d532:
        move.w #0xc,%d0
m68k_00d532_end:
.org 0xD536
m68k_00d536:
        move.w #0xe,(%a0)+
m68k_00d536_end:
.org 0xD53A
m68k_00d53a:
        move.w %d1,(%a0)+
m68k_00d53a_end:
.org 0xD53C
m68k_00d53c:
        addi.w #0x80,%d1
m68k_00d53c_end:
.org 0xD540
m68k_00d540:
        move.w #0xd,%d2
m68k_00d540_end:
.org 0xD544
m68k_00d544:
        clr.w (%a0)+
m68k_00d544_end:
.org 0xD546
m68k_00d546:
        dbra %d2,(. + -2)
m68k_00d546_end:
.org 0xD54A
m68k_00d54a:
        dbra %d0,(. + -20)
m68k_00d54a_end:
.org 0xD54E
m68k_00d54e:
        clr.w (%a0)
m68k_00d54e_end:
.org 0xD550
m68k_00d550:
        clr.w %d0
m68k_00d550_end:
.org 0xD552
m68k_00d552:
        addi.w #0x1a0,0xf31a:w
m68k_00d552_end:
.org 0xD558
m68k_00d558:
        bclr.b #0x0,0xf3a4:w
m68k_00d558_end:
.org 0xD55E
m68k_00d55e:
        rts
m68k_00d55e_end:
.org 0xD8AE
m68k_00d8ae:
        lea.l 0xd100:w,%a0
m68k_00d8ae_end:
.org 0xD8B2
m68k_00d8b2:
        adda.w 0xf31a:w,%a0
m68k_00d8b2_end:
.org 0xD8B6
m68k_00d8b6:
        move.w #0xc3a0,%d0
m68k_00d8b6_end:
.org 0xD8BA
m68k_00d8ba:
        move.w #0x8005,%d1
m68k_00d8ba_end:
.org 0xD8BE
m68k_00d8be:
        move.w #0x7,%d2
m68k_00d8be_end:
.org 0xD8C2
m68k_00d8c2:
        move.w #0x6,(%a0)+
m68k_00d8c2_end:
.org 0xD8C6
m68k_00d8c6:
        move.w %d0,(%a0)+
m68k_00d8c6_end:
.org 0xD8C8
m68k_00d8c8:
        addi.w #0x80,%d0
m68k_00d8c8_end:
.org 0xD8CC
m68k_00d8cc:
        move.w #0x5,%d3
m68k_00d8cc_end:
.org 0xD8D0
m68k_00d8d0:
        move.w %d1,(%a0)+
m68k_00d8d0_end:
.org 0xD8D2
m68k_00d8d2:
        addq.w #0x1,%d1
m68k_00d8d2_end:
.org 0xD8D4
m68k_00d8d4:
        dbra %d3,(. + -4)
m68k_00d8d4_end:
.org 0xD8D8
m68k_00d8d8:
        dbra %d2,(. + -22)
m68k_00d8d8_end:
.org 0xD8DC
m68k_00d8dc:
        clr.w (%a0)
m68k_00d8dc_end:
.org 0xD8DE
m68k_00d8de:
        addi.w #0x80,0xf31a:w
m68k_00d8de_end:
.org 0xD8E4
m68k_00d8e4:
        bset.b #0x2,0xf3a5:w
m68k_00d8e4_end:
.org 0xD8EA
m68k_00d8ea:
        rts
m68k_00d8ea_end:
.org 0xD8F4
m68k_00d8f4:
        bsr.w (. + 312)
m68k_00d8f4_end:
.org 0xD8F8
m68k_00d8f8:
        bsr.w (. + 406)
m68k_00d8f8_end:
.org 0xD8FC
m68k_00d8fc:
        lea.l 122(%pc),%a0
m68k_00d8fc_end:
.org 0xD900
m68k_00d900:
        nop
m68k_00d900_end:
.org 0xD902
m68k_00d902:
        move.w #0x38,%d0
m68k_00d902_end:
.org 0xD906
m68k_00d906:
        move.w #0x80,%d1
m68k_00d906_end:
.org 0xD90A
m68k_00d90a:
        clr.w %d2
m68k_00d90a_end:
.org 0xD90C
m68k_00d90c:
        clr.w 0xf60a:w
m68k_00d90c_end:
.org 0xD910
m68k_00d910:
        clr.w 0xf60e:w
m68k_00d910_end:
.org 0xD914
m68k_00d914:
        bsr.w (. + 12)
m68k_00d914_end:
.org 0xD918
m68k_00d918:
        jsr 0xac08:l
m68k_00d918_end:
.org 0xD920
m68k_00d920:
        cmpi.w #0x7,0xf362:w
m68k_00d920_end:
.org 0xD926
m68k_00d926:
        beq.b (. + 48)
m68k_00d926_end:
.org 0xD928
m68k_00d928:
        cmpi.w #0x3,0xf362:w
m68k_00d928_end:
.org 0xD92E
m68k_00d92e:
        bne.b (. + 72)
m68k_00d92e_end:
.org 0xD930
m68k_00d930:
        cmpi.w #0x3,0xf36a:w
m68k_00d930_end:
.org 0xD936
m68k_00d936:
        bls.b (. + 64)
m68k_00d936_end:
.org 0xD938
m68k_00d938:
        move.w #0xa,%d3
m68k_00d938_end:
.org 0xD93C
m68k_00d93c:
        sub.w 0xf36a:w,%d3
m68k_00d93c_end:
.org 0xD940
m68k_00d940:
        bpl.b (. + 4)
m68k_00d940_end:
.org 0xD942
m68k_00d942:
        clr.w %d3
m68k_00d942_end:
.org 0xD944
m68k_00d944:
        lsl.w #0x1,%d3
m68k_00d944_end:
.org 0xD946
m68k_00d946:
        lea.l 212(%pc),%a1
m68k_00d946_end:
.org 0xD94A
m68k_00d94a:
        nop
m68k_00d94a_end:
.org 0xD94C
m68k_00d94c:
        move.w (%a1, %d3.w),%d3
m68k_00d94c_end:
.org 0xD950
m68k_00d950:
        adda.w %d3,%a0
m68k_00d950_end:
.org 0xD952
m68k_00d952:
        bra.w (. + 36)
m68k_00d952_end:
.org 0xD956
m68k_00d956:
        move.w 0xf36a:w,%d3
m68k_00d956_end:
.org 0xD95A
m68k_00d95a:
        cmpi.w #0x6,%d3
m68k_00d95a_end:
.org 0xD95E
m68k_00d95e:
        bhi.b (. + 24)
m68k_00d95e_end:
.org 0xD960
m68k_00d960:
        subi.w #0x2,%d3
m68k_00d960_end:
.org 0xD964
m68k_00d964:
        bpl.b (. + 4)
m68k_00d964_end:
.org 0xD966
m68k_00d966:
        clr.w %d3
m68k_00d966_end:
.org 0xD968
m68k_00d968:
        lsl.w #0x2,%d3
m68k_00d968_end:
.org 0xD96A
m68k_00d96a:
        lea.l 174(%pc),%a1
m68k_00d96a_end:
.org 0xD96E
m68k_00d96e:
        nop
m68k_00d96e_end:
.org 0xD970
m68k_00d970:
        move.w (%a1, %d3.w),%d3
m68k_00d970_end:
.org 0xD974
m68k_00d974:
        adda.w %d3,%a0
m68k_00d974_end:
.org 0xD976
m68k_00d976:
        rts
m68k_00d976_end:
.org 0xDA2C
m68k_00da2c:
        cmpi.w #0x3,0xf362:w
m68k_00da2c_end:
.org 0xDA32
m68k_00da32:
        bne.w (. + 18)
m68k_00da32_end:
.org 0xDA36
m68k_00da36:
        cmpi.w #0x7,0xf36a:w
m68k_00da36_end:
.org 0xDA3C
m68k_00da3c:
        bcc.w (. + 64)
m68k_00da3c_end:
.org 0xDA40
m68k_00da40:
        bra.w (. + 24)
m68k_00da40_end:
.org 0xDA44
m68k_00da44:
        cmpi.w #0x7,0xf362:w
m68k_00da44_end:
.org 0xDA4A
m68k_00da4a:
        bne.w (. + 14)
m68k_00da4a_end:
.org 0xDA4E
m68k_00da4e:
        cmpi.w #0x4,0xf36a:w
m68k_00da4e_end:
.org 0xDA54
m68k_00da54:
        bls.w (. + 40)
m68k_00da54_end:
.org 0xDA58
m68k_00da58:
        lea.l 36(%pc),%a0
m68k_00da58_end:
.org 0xDA5C
m68k_00da5c:
        nop
m68k_00da5c_end:
.org 0xDA5E
m68k_00da5e:
        move.w 0xf320:w,%d0
m68k_00da5e_end:
.org 0xDA62
m68k_00da62:
        andi.w #0xf8,%d0
m68k_00da62_end:
.org 0xDA66
m68k_00da66:
        bne.w (. + 6)
m68k_00da66_end:
.org 0xDA6A
m68k_00da6a:
        addq.w #0x8,%a0
m68k_00da6a_end:
.org 0xDA6C
m68k_00da6c:
        move.w #0x50,%d0
m68k_00da6c_end:
.org 0xDA70
m68k_00da70:
        move.w #0x88,%d1
m68k_00da70_end:
.org 0xDA74
m68k_00da74:
        clr.w %d2
m68k_00da74_end:
.org 0xDA76
m68k_00da76:
        jsr 0xac08:l
m68k_00da76_end:
.org 0xDA7C
m68k_00da7c:
        rts
m68k_00da7c_end:
.org 0xDA8E
m68k_00da8e:
        cmpi.w #0x3,0xf362:w
m68k_00da8e_end:
.org 0xDA94
m68k_00da94:
        bne.w (. + 18)
m68k_00da94_end:
.org 0xDA98
m68k_00da98:
        cmpi.w #0x5,0xf36a:w
m68k_00da98_end:
.org 0xDA9E
m68k_00da9e:
        bcc.w (. + 112)
m68k_00da9e_end:
.org 0xDAA2
m68k_00daa2:
        bra.w (. + 24)
m68k_00daa2_end:
.org 0xDAA6
m68k_00daa6:
        cmpi.w #0x7,0xf362:w
m68k_00daa6_end:
.org 0xDAAC
m68k_00daac:
        bne.w (. + 14)
m68k_00daac_end:
.org 0xDAB0
m68k_00dab0:
        cmpi.w #0x5,0xf36a:w
m68k_00dab0_end:
.org 0xDAB6
m68k_00dab6:
        bls.w (. + 88)
m68k_00dab6_end:
.org 0xDABA
m68k_00daba:
        lea.l 84(%pc),%a0
m68k_00daba_end:
.org 0xDABE
m68k_00dabe:
        nop
m68k_00dabe_end:
.org 0xDAC0
m68k_00dac0:
        tst.w 0xf778:w
m68k_00dac0_end:
.org 0xDAC4
m68k_00dac4:
        beq.w (. + 16)
m68k_00dac4_end:
.org 0xDAC8
m68k_00dac8:
        btst.b #0x3,0xf321:w
m68k_00dac8_end:
.org 0xDACE
m68k_00dace:
        beq.w (. + 6)
m68k_00dace_end:
.org 0xDAD2
m68k_00dad2:
        addq.w #0x8,%a0
m68k_00dad2_end:
.org 0xDAD4
m68k_00dad4:
        move.w #0x60,%d0
m68k_00dad4_end:
.org 0xDAD8
m68k_00dad8:
        move.w #0x90,%d1
m68k_00dad8_end:
.org 0xDADC
m68k_00dadc:
        clr.w %d2
m68k_00dadc_end:
.org 0xDADE
m68k_00dade:
        jsr 0xac08:l
m68k_00dade_end:
.org 0xDAE4
m68k_00dae4:
        tst.w 0xf778:w
m68k_00dae4_end:
.org 0xDAE8
m68k_00dae8:
        beq.w (. + 22)
m68k_00dae8_end:
.org 0xDAEC
m68k_00daec:
        cmpi.w #0x403a,0xf77c:w
m68k_00daec_end:
.org 0xDAF2
m68k_00daf2:
        bne.w (. + 28)
m68k_00daf2_end:
.org 0xDAF6
m68k_00daf6:
        clr.w 0xf778:w
m68k_00daf6_end:
.org 0xDAFA
m68k_00dafa:
        bra.w (. + 20)
m68k_00dafa_end:
.org 0xDAFE
m68k_00dafe:
        cmpi.w #0x4039,0xf77c:w
m68k_00dafe_end:
.org 0xDB04
m68k_00db04:
        bne.w (. + 10)
m68k_00db04_end:
.org 0xDB08
m68k_00db08:
        move.w #0x1,0xf778:w
m68k_00db08_end:
.org 0xDB0E
m68k_00db0e:
        rts
m68k_00db0e_end:
.org 0xDEA6
m68k_00dea6:
        cmpi.w #0xf,%d0
m68k_00dea6_end:
.org 0xDEAA
m68k_00deaa:
        bls.b (. + 4)
m68k_00deaa_end:
.org 0xDEAC
m68k_00deac:
        bra.b (. + 0)
m68k_00deac_end:
.org 0xDEAE
m68k_00deae:
        lea.l 0xfb00:w,%a1
m68k_00deae_end:
.org 0xDEB2
m68k_00deb2:
        btst.l #0x0,%d0
m68k_00deb2_end:
.org 0xDEB6
m68k_00deb6:
        beq.b (. + 12)
m68k_00deb6_end:
.org 0xDEB8
m68k_00deb8:
        btst.b #0x0,0xf320:w
m68k_00deb8_end:
.org 0xDEBE
m68k_00debe:
        beq.b (. + 4)
m68k_00debe_end:
.org 0xDEC0
m68k_00dec0:
        addq.w #0x1,%d0
m68k_00dec0_end:
.org 0xDEC2
m68k_00dec2:
        bclr.l #0x0,%d0
m68k_00dec2_end:
.org 0xDEC6
m68k_00dec6:
        clr.w %d4
m68k_00dec6_end:
.org 0xDEC8
m68k_00dec8:
        move.w (%a0)+,%d2
m68k_00dec8_end:
.org 0xDECA
m68k_00deca:
        lsl.w #0x4,%d2
m68k_00deca_end:
.org 0xDECC
m68k_00decc:
        bsr.w (. + 40)
m68k_00decc_end:
.org 0xDED0
m68k_00ded0:
        bsr.w (. + 36)
m68k_00ded0_end:
.org 0xDED4
m68k_00ded4:
        bsr.w (. + 32)
m68k_00ded4_end:
.org 0xDED8
m68k_00ded8:
        move.w %d4,(%a1)+
m68k_00ded8_end:
.org 0xDEDA
m68k_00deda:
        dbra %d1,(. + -20)
m68k_00deda_end:
.org 0xDEDE
m68k_00dede:
        addq.w #0x1,0xf31e:w
m68k_00dede_end:
.org 0xDEE2
m68k_00dee2:
        move.w 0xfb00:w,%d0
m68k_00dee2_end:
.org 0xDEE6
m68k_00dee6:
        move.w %d0,0xfb20:w
m68k_00dee6_end:
.org 0xDEEA
m68k_00deea:
        move.w %d0,0xfb40:w
m68k_00deea_end:
.org 0xDEEE
m68k_00deee:
        move.w %d0,0xfb60:w
m68k_00deee_end:
.org 0xDEF2
m68k_00def2:
        rts
m68k_00def2_end:
.org 0xDEF4
m68k_00def4:
        lsl.w #0x4,%d4
m68k_00def4_end:
.org 0xDEF6
m68k_00def6:
        rol.w #0x4,%d2
m68k_00def6_end:
.org 0xDEF8
m68k_00def8:
        move.b %d2,%d3
m68k_00def8_end:
.org 0xDEFA
m68k_00defa:
        andi.w #0xe,%d3
m68k_00defa_end:
.org 0xDEFE
m68k_00defe:
        sub.b %d0,%d3
m68k_00defe_end:
.org 0xDF00
m68k_00df00:
        bcc.b (. + 4)
m68k_00df00_end:
.org 0xDF02
m68k_00df02:
        clr.b %d3
m68k_00df02_end:
.org 0xDF04
m68k_00df04:
        or.w %d3,%d4
m68k_00df04_end:
.org 0xDF06
m68k_00df06:
        rts
m68k_00df06_end:
.org 0xE050
m68k_00e050:
        move.w 0xf65a:w,%d0
m68k_00e050_end:
.org 0xE054
m68k_00e054:
        cmpi.w #0x6,%d0
m68k_00e054_end:
.org 0xE058
m68k_00e058:
        beq.w (. + 100)
m68k_00e058_end:
.org 0xE05C
m68k_00e05c:
        lsl.w #0x1,%d0
m68k_00e05c_end:
.org 0xE05E
m68k_00e05e:
        move.w 100(%pc, %d0.w),%d0
m68k_00e05e_end:
.org 0xE062
m68k_00e062:
        lea.l 7586(%pc),%a0
m68k_00e062_end:
.org 0xE066
m68k_00e066:
        nop
m68k_00e066_end:
.org 0xE068
m68k_00e068:
        jsr (%a0, %d0.w)
m68k_00e068_end:
.org 0xE06C
m68k_00e06c:
        tst.w 0xf36c:w
m68k_00e06c_end:
.org 0xE070
m68k_00e070:
        beq.w (. + 10)
m68k_00e070_end:
.org 0xE074
m68k_00e074:
        move.w #0x85,0xf380:w
m68k_00e074_end:
.org 0xE07A
m68k_00e07a:
        clr.w 0xf65a:w
m68k_00e07a_end:
.org 0xE07E
m68k_00e07e:
        cmpi.w #0x28,0xf600:w
m68k_00e07e_end:
.org 0xE084
m68k_00e084:
        bne.b (. + 8)
m68k_00e084_end:
.org 0xE086
m68k_00e086:
        jmp 0x60c:l
m68k_00e086_end:
.org 0xE08C
m68k_00e08c:
        tst.w 0xf612:w
m68k_00e08c_end:
.org 0xE090
m68k_00e090:
        bne.b (. + 8)
m68k_00e090_end:
.org 0xE092
m68k_00e092:
        move.w #0x201,0xf612:w
m68k_00e092_end:
.org 0xE098
m68k_00e098:
        clr.w 0xf576:w
m68k_00e098_end:
.org 0xE09C
m68k_00e09c:
        move.w 0xf612:w,0xf3c2:w
m68k_00e09c_end:
.org 0xE0A2
m68k_00e0a2:
        move.w 0xf362:w,0xf3c4:w
m68k_00e0a2_end:
.org 0xE0A8
m68k_00e0a8:
        move.w #0x208,0xf612:w
m68k_00e0a8_end:
.org 0xE0AE
m68k_00e0ae:
        move.w #0x13,0xf362:w
m68k_00e0ae_end:
.org 0xE0B4
m68k_00e0b4:
        clr.w 0xf36a:w
m68k_00e0b4_end:
.org 0xE0B8
m68k_00e0b8:
        bra.w (. + 10)
m68k_00e0b8_end:
.org 0xE0BC
m68k_00e0bc:
        jmp 0x30ac6:l
m68k_00e0bc_end:
.org 0xE0C2
m68k_00e0c2:
        rts
m68k_00e0c2_end:
.org 0xE8B2
m68k_00e8b2:
        tst.b (%a1, %d3.w)
m68k_00e8b2_end:
.org 0xE8B6
m68k_00e8b6:
        bpl.b (. + 16)
m68k_00e8b6_end:
.org 0xE8B8
m68k_00e8b8:
        clr.l (%a0)
m68k_00e8b8_end:
.org 0xE8BA
m68k_00e8ba:
        move.w 0xe700:w,%d3
m68k_00e8ba_end:
.org 0xE8BE
m68k_00e8be:
        bclr.l %d0,%d3
m68k_00e8be_end:
.org 0xE8C0
m68k_00e8c0:
        move.w %d3,0xe700:w
m68k_00e8c0_end:
.org 0xE8C4
m68k_00e8c4:
        bra.b (. + 26)
m68k_00e8c4_end:
.org 0xE8C6
m68k_00e8c6:
        move.b 0x1(%a0),%d3
m68k_00e8c6_end:
.org 0xE8CA
m68k_00e8ca:
        tst.b (%a1, %d3.w)
m68k_00e8ca_end:
.org 0xE8CE
m68k_00e8ce:
        bpl.w (. + 16)
m68k_00e8ce_end:
.org 0xE8D2
m68k_00e8d2:
        clr.l (%a0)
m68k_00e8d2_end:
.org 0xE8D4
m68k_00e8d4:
        move.w 0xe700:w,%d3
m68k_00e8d4_end:
.org 0xE8D8
m68k_00e8d8:
        bclr.l %d0,%d3
m68k_00e8d8_end:
.org 0xE8DA
m68k_00e8da:
        move.w %d3,0xe700:w
m68k_00e8da_end:
.org 0xFA14
m68k_00fa14:
        sub.l %d3,(%a0, %d2.w)
m68k_00fa14_end:
.org 0xFA18
m68k_00fa18:
        rts
m68k_00fa18_end:
.org 0xFA64
m68k_00fa64:
        sub.l %d3,(%a0, %d2.w)
m68k_00fa64_end:
.org 0xFA68
m68k_00fa68:
        rts
m68k_00fa68_end:
.org 0xFABA
m68k_00faba:
        sub.l %d3,(%a0, %d2.w)
m68k_00faba_end:
.org 0xFABE
m68k_00fabe:
        rts
m68k_00fabe_end:
.org 0xFDEA
m68k_00fdea:
        lea.l 0xf427:w,%a0
m68k_00fdea_end:
.org 0xFDEE
m68k_00fdee:
        move.b (%a0, %d0.w),%d0
m68k_00fdee_end:
.org 0xFDF2
m68k_00fdf2:
        ext.w %d0
m68k_00fdf2_end:
.org 0xFDF4
m68k_00fdf4:
        lsl.w #0x1,%d0
m68k_00fdf4_end:
.org 0xFDF6
m68k_00fdf6:
        lea.l 0xe640:w,%a0
m68k_00fdf6_end:
.org 0xFDFA
m68k_00fdfa:
        move.w (%a0, %d0.w),%d0
m68k_00fdfa_end:
.org 0xFDFE
m68k_00fdfe:
        move.w #0x201,0xf612:w
m68k_00fdfe_end:
.org 0xFE04
m68k_00fe04:
        rts
m68k_00fe04_end:
.org 0x10354
m68k_010354:
        movea.l 0xff382c:l,%a0
m68k_010354_end:
.org 0x1035A
m68k_01035a:
        ori.b #0x10,(%a0)
m68k_01035a_end:
.org 0x1035E
m68k_01035e:
        move.b 0x5(%a0),%d0
m68k_01035e_end:
.org 0x10362
m68k_010362:
        lsl.w #0x8,%d0
m68k_010362_end:
.org 0x10364
m68k_010364:
        move.b 0x6(%a0),%d0
m68k_010364_end:
.org 0x10368
m68k_010368:
        lsl.l #0x8,%d0
m68k_010368_end:
.org 0x1036A
m68k_01036a:
        move.b 0x7(%a0),%d0
m68k_01036a_end:
.org 0x1036E
m68k_01036e:
        lsl.l #0x8,%d0
m68k_01036e_end:
.org 0x10370
m68k_010370:
        move.b 0x8(%a0),%d0
m68k_010370_end:
.org 0x10374
m68k_010374:
        sub.l 0xf3f4:w,%d0
m68k_010374_end:
.org 0x10378
m68k_010378:
        move.b %d0,0x8(%a0)
m68k_010378_end:
.org 0x1037C
m68k_01037c:
        lsr.l #0x8,%d0
m68k_01037c_end:
.org 0x1037E
m68k_01037e:
        move.b %d0,0x7(%a0)
m68k_01037e_end:
.org 0x10382
m68k_010382:
        lsr.l #0x8,%d0
m68k_010382_end:
.org 0x10384
m68k_010384:
        move.b %d0,0x6(%a0)
m68k_010384_end:
.org 0x10388
m68k_010388:
        lsr.w #0x8,%d0
m68k_010388_end:
.org 0x1038A
m68k_01038a:
        move.b %d0,0x5(%a0)
m68k_01038a_end:
.org 0x1038E
m68k_01038e:
        move.b 0x9(%a0),%d0
m68k_01038e_end:
.org 0x10392
m68k_010392:
        lsl.w #0x8,%d0
m68k_010392_end:
.org 0x10394
m68k_010394:
        move.b 0xa(%a0),%d0
m68k_010394_end:
.org 0x10398
m68k_010398:
        lsl.l #0x8,%d0
m68k_010398_end:
.org 0x1039A
m68k_01039a:
        move.b 0xb(%a0),%d0
m68k_01039a_end:
.org 0x1039E
m68k_01039e:
        lsl.l #0x8,%d0
m68k_01039e_end:
.org 0x103A0
m68k_0103a0:
        move.b 0xc(%a0),%d0
m68k_0103a0_end:
.org 0x103A4
m68k_0103a4:
        add.l 0xf3ba:w,%d0
m68k_0103a4_end:
.org 0x103A8
m68k_0103a8:
        cmpi.l #0xf423f,%d0
m68k_0103a8_end:
.org 0x103AE
m68k_0103ae:
        bls.b (. + 8)
m68k_0103ae_end:
.org 0x103B0
m68k_0103b0:
        move.l #0xf423f,%d0
m68k_0103b0_end:
.org 0x103B6
m68k_0103b6:
        move.b %d0,0xc(%a0)
m68k_0103b6_end:
.org 0x103BA
m68k_0103ba:
        lsr.l #0x8,%d0
m68k_0103ba_end:
.org 0x103BC
m68k_0103bc:
        move.b %d0,0xb(%a0)
m68k_0103bc_end:
.org 0x103C0
m68k_0103c0:
        lsr.l #0x8,%d0
m68k_0103c0_end:
.org 0x103C2
m68k_0103c2:
        move.b %d0,0xa(%a0)
m68k_0103c2_end:
.org 0x103C6
m68k_0103c6:
        lsr.w #0x8,%d0
m68k_0103c6_end:
.org 0x103C8
m68k_0103c8:
        move.b %d0,0x9(%a0)
m68k_0103c8_end:
.org 0x103CC
m68k_0103cc:
        move.w #0x208,0xf612:w
m68k_0103cc_end:
.org 0x103D2
m68k_0103d2:
        move.w #0x28,0xf362:w
m68k_0103d2_end:
.org 0x103D8
m68k_0103d8:
        move.w #0x74,0xf3fe:w
m68k_0103d8_end:
.org 0x103DE
m68k_0103de:
        move.w #0xb,0xff7026:l
m68k_0103de_end:
.org 0x103E6
m68k_0103e6:
        rts
m68k_0103e6_end:
.org 0x107F2
m68k_0107f2:
        jsr 0x177be:l
m68k_0107f2_end:
.org 0x107F8
m68k_0107f8:
        bra.w (. + 26)
m68k_0107f8_end:
.org 0x107FC
m68k_0107fc:
        move.l #0x100000,%d0
m68k_0107fc_end:
.org 0x10802
m68k_010802:
        nop
m68k_010802_end:
.org 0x10804
m68k_010804:
        nop
m68k_010804_end:
.org 0x10806
m68k_010806:
        dbra %d0,(. + -4)
m68k_010806_end:
.org 0x1080A
m68k_01080a:
        move.w #0xffff,0xff7026:l
m68k_01080a_end:
.org 0x10EE0
m68k_010ee0:
        tst.w 0xf386:w
m68k_010ee0_end:
.org 0x10EE4
m68k_010ee4:
        bne.w (. + 54)
m68k_010ee4_end:
.org 0x10EE8
m68k_010ee8:
        move.w 0xf3a6:w,%d0
m68k_010ee8_end:
.org 0x10EEC
m68k_010eec:
        lea.l 0xcc00:w,%a0
m68k_010eec_end:
.org 0x10EF0
m68k_010ef0:
        move.b 0xf393:w,(%a0, %d0.w)
m68k_010ef0_end:
.org 0x10EF6
m68k_010ef6:
        lea.l 0xcd00:w,%a0
m68k_010ef6_end:
.org 0x10EFA
m68k_010efa:
        clr.b (%a0, %d0.w)
m68k_010efa_end:
.org 0x10EFE
m68k_010efe:
        move.w #0x208,0xf612:w
m68k_010efe_end:
.org 0x10F04
m68k_010f04:
        move.w #0x20,0xf362:w
m68k_010f04_end:
.org 0x10F0A
m68k_010f0a:
        move.w #0x55,%d0
m68k_010f0a_end:
.org 0x10F0E
m68k_010f0e:
        jsr 0x676f2:l
m68k_010f0e_end:
.org 0x10F14
m68k_010f14:
        move.w #0x1,0xf652:w
m68k_010f14_end:
.org 0x10F1A
m68k_010f1a:
        rts
m68k_010f1a_end:
.org 0x10F1C
m68k_010f1c:
        lea.l 0xcd00:w,%a0
m68k_010f1c_end:
.org 0x10F20
m68k_010f20:
        move.w 0xf3a6:w,%d0
m68k_010f20_end:
.org 0x10F24
m68k_010f24:
        move.b #0x1,(%a0, %d0.w)
m68k_010f24_end:
.org 0x10F2A
m68k_010f2a:
        bsr.w (. + 16)
m68k_010f2a_end:
.org 0x10F2E
m68k_010f2e:
        bsr.w (. + -1104)
m68k_010f2e_end:
.org 0x10F32
m68k_010f32:
        bsr.w (. + 96)
m68k_010f32_end:
.org 0x10F36
m68k_010f36:
        rts
m68k_010f36_end:
.org 0x10F38
m68k_010f38:
        rts
m68k_010f38_end:
.org 0x10F3A
m68k_010f3a:
        jsr 0x83d4:l
m68k_010f3a_end:
.org 0x10F40
m68k_010f40:
        moveq #0,%d0
m68k_010f40_end:
.org 0x10F42
m68k_010f42:
        move.w 0xf61c:w,%d0
m68k_010f42_end:
.org 0x10F46
m68k_010f46:
        move.l %d0,%d1
m68k_010f46_end:
.org 0x10F48
m68k_010f48:
        lsl.l #0x2,%d0
m68k_010f48_end:
.org 0x10F4A
m68k_010f4a:
        add.l %d1,%d0
m68k_010f4a_end:
.org 0x10F4C
m68k_010f4c:
        lsl.l #0x2,%d0
m68k_010f4c_end:
.org 0x10F4E
m68k_010f4e:
        swap %d0
m68k_010f4e_end:
.org 0x10F50
m68k_010f50:
        move.w 0xf3a6:w,%d1
m68k_010f50_end:
.org 0x10F54
m68k_010f54:
        lea.l 0xc700:w,%a0
m68k_010f54_end:
.org 0x10F58
m68k_010f58:
        move.b (%a0, %d1.w),%d2
m68k_010f58_end:
.org 0x10F5C
m68k_010f5c:
        andi.w #0xf,%d2
m68k_010f5c_end:
.org 0x10F60
m68k_010f60:
        lsl.w #0x1,%d2
m68k_010f60_end:
.org 0x10F62
m68k_010f62:
        lea.l 36(%pc),%a0
m68k_010f62_end:
.org 0x10F66
m68k_010f66:
        nop
m68k_010f66_end:
.org 0x10F68
m68k_010f68:
        add.w (%a0, %d2.w),%d0
m68k_010f68_end:
.org 0x10F6C
m68k_010f6c:
        move.w 0xf3a6:w,%d1
m68k_010f6c_end:
.org 0x10F70
m68k_010f70:
        lea.l 0xc200:w,%a0
m68k_010f70_end:
.org 0x10F74
m68k_010f74:
        clr.w %d2
m68k_010f74_end:
.org 0x10F76
m68k_010f76:
        move.b (%a0, %d1.w),%d2
m68k_010f76_end:
.org 0x10F7A
m68k_010f7a:
        add.w %d0,%d2
m68k_010f7a_end:
.org 0x10F7C
m68k_010f7c:
        lsl.w #0x1,%d1
m68k_010f7c_end:
.org 0x10F7E
m68k_010f7e:
        lea.l 0xb600:w,%a0
m68k_010f7e_end:
.org 0x10F82
m68k_010f82:
        add.w (%a0, %d1.w),%d2
m68k_010f82_end:
.org 0x10F86
m68k_010f86:
        rts
m68k_010f86_end:
.org 0x10F92
m68k_010f92:
        move.w 0xf3f2:w,%d0
m68k_010f92_end:
.org 0x10F96
m68k_010f96:
        lsl.w #0x1,%d0
m68k_010f96_end:
.org 0x10F98
m68k_010f98:
        lea.l 0xb600:w,%a1
m68k_010f98_end:
.org 0x10F9C
m68k_010f9c:
        move.w (%a1, %d0.w),%d0
m68k_010f9c_end:
.org 0x10FA0
m68k_010fa0:
        clr.w %d2
m68k_010fa0_end:
.org 0x10FA2
m68k_010fa2:
        cmpi.w #0x1e,%d0
m68k_010fa2_end:
.org 0x10FA6
m68k_010fa6:
        bls.w (. + -730)
m68k_010fa6_end:
.org 0x10FAA
m68k_010faa:
        addq.w #0x1,%d2
m68k_010faa_end:
.org 0x10FAC
m68k_010fac:
        cmpi.w #0x3c,%d0
m68k_010fac_end:
.org 0x10FB0
m68k_010fb0:
        bls.b (. + 28)
m68k_010fb0_end:
.org 0x10FB2
m68k_010fb2:
        addq.w #0x1,%d2
m68k_010fb2_end:
.org 0x10FB4
m68k_010fb4:
        cmpi.w #0x50,%d0
m68k_010fb4_end:
.org 0x10FB8
m68k_010fb8:
        bls.b (. + 20)
m68k_010fb8_end:
.org 0x10FBA
m68k_010fba:
        addq.w #0x1,%d2
m68k_010fba_end:
.org 0x10FBC
m68k_010fbc:
        cmpi.w #0x5a,%d0
m68k_010fbc_end:
.org 0x10FC0
m68k_010fc0:
        bls.b (. + 12)
m68k_010fc0_end:
.org 0x10FC2
m68k_010fc2:
        addq.w #0x1,%d2
m68k_010fc2_end:
.org 0x10FC4
m68k_010fc4:
        cmpi.w #0x64,%d0
m68k_010fc4_end:
.org 0x10FC8
m68k_010fc8:
        bls.b (. + 4)
m68k_010fc8_end:
.org 0x10FCA
m68k_010fca:
        addq.w #0x1,%d2
m68k_010fca_end:
.org 0x10FCC
m68k_010fcc:
        lsl.w #0x3,%d2
m68k_010fcc_end:
.org 0x10FCE
m68k_010fce:
        jsr 0x83d4:l
m68k_010fce_end:
.org 0x10FD4
m68k_010fd4:
        moveq #0,%d0
m68k_010fd4_end:
.org 0x10FD6
m68k_010fd6:
        move.w 0xf61c:w,%d0
m68k_010fd6_end:
.org 0x10FDA
m68k_010fda:
        lsl.l #0x2,%d0
m68k_010fda_end:
.org 0x10FDC
m68k_010fdc:
        swap %d0
m68k_010fdc_end:
.org 0x10FDE
m68k_010fde:
        lsl.w #0x1,%d0
m68k_010fde_end:
.org 0x10FE0
m68k_010fe0:
        add.w %d0,%d2
m68k_010fe0_end:
.org 0x10FE2
m68k_010fe2:
        tst.w (%a0, %d2.w)
m68k_010fe2_end:
.org 0x10FE6
m68k_010fe6:
        bne.b (. + 38)
m68k_010fe6_end:
.org 0x10FE8
m68k_010fe8:
        bsr.w (. + -470)
m68k_010fe8_end:
.org 0x10FEC
m68k_010fec:
        move.w #0x208,0xf612:w
m68k_010fec_end:
.org 0x10FF2
m68k_010ff2:
        move.w #0x20,0xf362:w
m68k_010ff2_end:
.org 0x10FF8
m68k_010ff8:
        move.w #0x53,%d0
m68k_010ff8_end:
.org 0x10FFC
m68k_010ffc:
        move.w 0xf3a6:w,0xf3d0:w
m68k_010ffc_end:
.org 0x11002
m68k_011002:
        jsr 0x676f2:l
m68k_011002_end:
.org 0x11008
m68k_011008:
        bra.w (. + 118)
m68k_011008_end:
.org 0x1100C
m68k_01100c:
        bsr.w (. + -348)
m68k_01100c_end:
.org 0x11010
m68k_011010:
        move.w 0xf3f2:w,%d0
m68k_011010_end:
.org 0x11014
m68k_011014:
        lea.l 0xcc00:w,%a0
m68k_011014_end:
.org 0x11018
m68k_011018:
        move.b 0xf393:w,(%a0, %d0.w)
m68k_011018_end:
.org 0x1101E
m68k_01101e:
        lea.l 0xcd00:w,%a0
m68k_01101e_end:
.org 0x11022
m68k_011022:
        clr.b (%a0, %d0.w)
m68k_011022_end:
.org 0x11026
m68k_011026:
        move.w #0x54,0xf740:w
m68k_011026_end:
.org 0x1102C
m68k_01102c:
        move.w 0xf3a6:w,0xf3d0:w
m68k_01102c_end:
.org 0x11032
m68k_011032:
        move.w 0xf3f2:w,0xf3d2:w
m68k_011032_end:
.org 0x11038
m68k_011038:
        move.w 0xf362:w,-(%a7)
m68k_011038_end:
.org 0x1103C
m68k_01103c:
        clr.w 0xf362:w
m68k_01103c_end:
.org 0x11040
m68k_011040:
        jsr 0x30a74:l
m68k_011040_end:
.org 0x11046
m68k_011046:
        move.w (%a7)+,0xf362:w
m68k_011046_end:
.org 0x1104A
m68k_01104a:
        move.w #0x208,0xf612:w
m68k_01104a_end:
.org 0x11050
m68k_011050:
        move.w #0x20,0xf362:w
m68k_011050_end:
.org 0x11056
m68k_011056:
        clr.w 0xf386:w
m68k_011056_end:
.org 0x1105A
m68k_01105a:
        clr.w 0xf384:w
m68k_01105a_end:
.org 0x1105E
m68k_01105e:
        move.w 0xf3f2:w,0xf3a6:w
m68k_01105e_end:
.org 0x11064
m68k_011064:
        move.w 0xf3a6:w,0xf3d0:w
m68k_011064_end:
.org 0x1106A
m68k_01106a:
        move.w #0x56,%d0
m68k_01106a_end:
.org 0x1106E
m68k_01106e:
        jsr 0x676f2:l
m68k_01106e_end:
.org 0x11074
m68k_011074:
        move.w #0x1,0xf652:w
m68k_011074_end:
.org 0x1107A
m68k_01107a:
        clr.w 0xf64e:w
m68k_01107a_end:
.org 0x1107E
m68k_01107e:
        rts
m68k_01107e_end:
.org 0x11546
m68k_011546:
        lea.l 0xf502:w,%a0
m68k_011546_end:
.org 0x1154A
m68k_01154a:
        lea.l 0xc300:w,%a1
m68k_01154a_end:
.org 0x1154E
m68k_01154e:
        move.w (%a0)+,%d0
m68k_01154e_end:
.org 0x11550
m68k_011550:
        bmi.b (. + 18)
m68k_011550_end:
.org 0x11552
m68k_011552:
        cmpi.b #0x28,(%a1, %d0.w)
m68k_011552_end:
.org 0x11558
m68k_011558:
        bcs.b (. + -10)
m68k_011558_end:
.org 0x1155A
m68k_01155a:
        ori.b #0x80,(%a1, %d0.w)
m68k_01155a_end:
.org 0x11560
m68k_011560:
        bra.b (. + -18)
m68k_011560_end:
.org 0x11562
m68k_011562:
        rts
m68k_011562_end:
.org 0x11564
m68k_011564:
        move.w 0xf3a8:w,%d0
m68k_011564_end:
.org 0x11568
m68k_011568:
        move.w %d0,%d1
m68k_011568_end:
.org 0x1156A
m68k_01156a:
        lsl.w #0x1,%d1
m68k_01156a_end:
.org 0x1156C
m68k_01156c:
        add.w %d0,%d1
m68k_01156c_end:
.org 0x1156E
m68k_01156e:
        lsl.w #0x2,%d1
m68k_01156e_end:
.org 0x11570
m68k_011570:
        lea.l 0xe80c:w,%a0
m68k_011570_end:
.org 0x11574
m68k_011574:
        move.w #0xffff,(%a0, %d1.w)
m68k_011574_end:
.org 0x1157A
m68k_01157a:
        move.w #0xffff,0x4(%a0, %d1.w)
m68k_01157a_end:
.org 0x11580
m68k_011580:
        move.w #0xffff,0x8(%a0, %d1.w)
m68k_011580_end:
.org 0x11586
m68k_011586:
        rts
m68k_011586_end:
.org 0x11588
m68k_011588:
        movem.l %d1-%d3,-(%a7)
m68k_011588_end:
.org 0x1158C
m68k_01158c:
        move.w %d1,%d2
m68k_01158c_end:
.org 0x1158E
m68k_01158e:
        addi.w #0x29,%d2
m68k_01158e_end:
.org 0x11592
m68k_011592:
        lea.l 0xcc00:w,%a0
m68k_011592_end:
.org 0x11596
m68k_011596:
        move.w 0xf3a8:w,%d1
m68k_011596_end:
.org 0x1159A
m68k_01159a:
        ori.w #0x40,%d1
m68k_01159a_end:
.org 0x1159E
m68k_01159e:
        lea.l 0xcc00:w,%a0
m68k_01159e_end:
.org 0x115A2
m68k_0115a2:
        move.w #0xff,%d3
m68k_0115a2_end:
.org 0x115A6
m68k_0115a6:
        cmp.b (%a0, %d3.w),%d1
m68k_0115a6_end:
.org 0x115AA
m68k_0115aa:
        bne.w (. + 8)
m68k_0115aa_end:
.org 0x115AE
m68k_0115ae:
        move.b %d2,(%a0, %d3.w)
m68k_0115ae_end:
.org 0x115B2
m68k_0115b2:
        dbra %d3,(. + -12)
m68k_0115b2_end:
.org 0x115B6
m68k_0115b6:
        movem.l (%a7)+,%d1-%d3
m68k_0115b6_end:
.org 0x115BA
m68k_0115ba:
        rts
m68k_0115ba_end:
.org 0x115BC
m68k_0115bc:
        movem.l %d0-%d2/%a0-%a2,-(%a7)
m68k_0115bc_end:
.org 0x115C0
m68k_0115c0:
        lea.l 0xe65c:w,%a0
m68k_0115c0_end:
.org 0x115C4
m68k_0115c4:
        move.w 0xf3a8:w,%d0
m68k_0115c4_end:
.org 0x115C8
m68k_0115c8:
        lsl.w #0x2,%d0
m68k_0115c8_end:
.org 0x115CA
m68k_0115ca:
        clr.l (%a0, %d0.w)
m68k_0115ca_end:
.org 0x115CE
m68k_0115ce:
        lea.l 0xe9f8:w,%a0
m68k_0115ce_end:
.org 0x115D2
m68k_0115d2:
        lea.l 0xf427:w,%a1
m68k_0115d2_end:
.org 0x115D6
m68k_0115d6:
        lea.l 0xe65c:w,%a2
m68k_0115d6_end:
.org 0x115DA
m68k_0115da:
        clr.w %d0
m68k_0115da_end:
.org 0x115DC
m68k_0115dc:
        move.w 0xf3a8:w,%d1
m68k_0115dc_end:
.org 0x115E0
m68k_0115e0:
        cmp.b (%a0),%d1
m68k_0115e0_end:
.org 0x115E2
m68k_0115e2:
        bne.w (. + 20)
m68k_0115e2_end:
.org 0x115E6
m68k_0115e6:
        clr.w %d2
m68k_0115e6_end:
.org 0x115E8
m68k_0115e8:
        move.b 0x1(%a0),%d2
m68k_0115e8_end:
.org 0x115EC
m68k_0115ec:
        lsl.w #0x2,%d2
m68k_0115ec_end:
.org 0x115EE
m68k_0115ee:
        clr.l (%a2, %d2.w)
m68k_0115ee_end:
.org 0x115F2
m68k_0115f2:
        bra.w (. + 12)
m68k_0115f2_end:
.org 0x115F6
m68k_0115f6:
        cmp.b 0x1(%a0),%d1
m68k_0115f6_end:
.org 0x115FA
m68k_0115fa:
        bne.w (. + 16)
m68k_0115fa_end:
.org 0x115FE
m68k_0115fe:
        clr.l (%a0)
m68k_0115fe_end:
.org 0x11600
m68k_011600:
        move.w 0xe700:w,%d2
m68k_011600_end:
.org 0x11604
m68k_011604:
        bclr.l %d0,%d2
m68k_011604_end:
.org 0x11606
m68k_011606:
        move.w %d2,0xe700:w
m68k_011606_end:
.org 0x1160A
m68k_01160a:
        addq.l #0x4,%a0
m68k_01160a_end:
.org 0x1160C
m68k_01160c:
        addq.w #0x1,%d0
m68k_01160c_end:
.org 0x1160E
m68k_01160e:
        cmpi.w #0x10,%d0
m68k_01160e_end:
.org 0x11612
m68k_011612:
        bcs.b (. + -50)
m68k_011612_end:
.org 0x11614
m68k_011614:
        movem.l (%a7)+,%d0-%d2/%a0-%a2
m68k_011614_end:
.org 0x11618
m68k_011618:
        rts
m68k_011618_end:
.org 0x12716
m68k_012716:
        addq.w #0x1,%d3
m68k_012716_end:
.org 0x12718
m68k_012718:
        bra.b (. + -10)
m68k_012718_end:
.org 0x12728
m68k_012728:
        clr.w %d5
m68k_012728_end:
.org 0x1272A
m68k_01272a:
        move.b 86(%pc, %d3.w),%d5
m68k_01272a_end:
.org 0x1272E
m68k_01272e:
        add.w %d1,%d5
m68k_01272e_end:
.org 0x12730
m68k_012730:
        move.w %d5,(%a6)+
m68k_012730_end:
.org 0x12732
m68k_012732:
        addq.w #0x1,%d4
m68k_012732_end:
.org 0x12918
m68k_012918:
        move.w #0x208,0xf612:w
m68k_012918_end:
.org 0x1291E
m68k_01291e:
        move.w #0x2,0xf362:w
m68k_01291e_end:
.org 0x12924
m68k_012924:
        move.w #0x12,0xf36a:w
m68k_012924_end:
.org 0x1298C
m68k_01298c:
        subq.w #0x1,0xf608:w
m68k_01298c_end:
.org 0x12990
m68k_012990:
        bne.w (. + 76)
m68k_012990_end:
.org 0x12994
m68k_012994:
        move.w #0xc,0xf608:w
m68k_012994_end:
.org 0x1299A
m68k_01299a:
        btst.l #0x3,%d0
m68k_01299a_end:
.org 0x1299E
m68k_01299e:
        bne.b (. + 8)
m68k_01299e_end:
.org 0x129A0
m68k_0129a0:
        bsr.w (. + 62)
m68k_0129a0_end:
.org 0x129A4
m68k_0129a4:
        bra.b (. + 56)
m68k_0129a4_end:
.org 0x129A6
m68k_0129a6:
        bsr.w (. + 82)
m68k_0129a6_end:
.org 0x129AA
m68k_0129aa:
        bra.b (. + 50)
m68k_0129aa_end:
.org 0x129D0
m68k_0129d0:
        bsr.w (. + 94)
m68k_0129d0_end:
.org 0x129D4
m68k_0129d4:
        bra.b (. + 8)
m68k_0129d4_end:
.org 0x129DE
m68k_0129de:
        move.w 0xf39a:w,%d0
m68k_0129de_end:
.org 0x129E2
m68k_0129e2:
        subq.w #0x1,%d0
m68k_0129e2_end:
.org 0x129E4
m68k_0129e4:
        bcs.b (. + 18)
m68k_0129e4_end:
.org 0x129E6
m68k_0129e6:
        lsl.w #0x1,%d0
m68k_0129e6_end:
.org 0x129E8
m68k_0129e8:
        lea.l 0xef00:w,%a0
m68k_0129e8_end:
.org 0x129EC
m68k_0129ec:
        tst.w (%a0, %d0.w)
m68k_0129ec_end:
.org 0x129F0
m68k_0129f0:
        beq.b (. + 6)
m68k_0129f0_end:
.org 0x129F2
m68k_0129f2:
        subq.w #0x1,0xf39a:w
m68k_0129f2_end:
.org 0x129F6
m68k_0129f6:
        rts
m68k_0129f6_end:
.org 0x129F8
m68k_0129f8:
        move.w 0xf39a:w,%d0
m68k_0129f8_end:
.org 0x129FC
m68k_0129fc:
        addq.w #0x1,%d0
m68k_0129fc_end:
.org 0x129FE
m68k_0129fe:
        cmp.w 0xf3fc:w,%d0
m68k_0129fe_end:
.org 0x12A02
m68k_012a02:
        bhi.w (. + 8)
m68k_012a02_end:
.org 0x12A06
m68k_012a06:
        addq.w #0x1,0xf39a:w
m68k_012a06_end:
.org 0x12A0A
m68k_012a0a:
        rts
m68k_012a0a_end:
.org 0x12A2E
m68k_012a2e:
        move.w 0xf39a:w,%d1
m68k_012a2e_end:
.org 0x12A32
m68k_012a32:
        lsl.w #0x2,%d1
m68k_012a32_end:
.org 0x12A34
m68k_012a34:
        lea.l 2582(%pc),%a0
m68k_012a34_end:
.org 0x12A38
m68k_012a38:
        nop
m68k_012a38_end:
.org 0x12A3A
m68k_012a3a:
        move.l (%a0, %d1.w),%d1
m68k_012a3a_end:
.org 0x12A3E
m68k_012a3e:
        move.l 0xf3f4:w,%d2
m68k_012a3e_end:
.org 0x12A42
m68k_012a42:
        sub.l %d1,%d2
m68k_012a42_end:
.org 0x12A44
m68k_012a44:
        bcs.w (. + 8)
m68k_012a44_end:
.org 0x12A48
m68k_012a48:
        move.l %d2,0xf3f4:w
m68k_012a48_end:
.org 0x12A4C
m68k_012a4c:
        rts
m68k_012a4c_end:
.org 0x1306A
m68k_01306a:
        lea.l 0xd100:w,%a0
m68k_01306a_end:
.org 0x1306E
m68k_01306e:
        adda.w 0xf31a:w,%a0
m68k_01306e_end:
.org 0x13072
m68k_013072:
        move.w #0xf,(%a0)+
m68k_013072_end:
.org 0x13076
m68k_013076:
        move.w #0xc494,(%a0)+
m68k_013076_end:
.org 0x1307A
m68k_01307a:
        move.w #0xc380,(%a0)+
m68k_01307a_end:
.org 0x1307E
m68k_01307e:
        move.w #0xc,%d0
m68k_01307e_end:
.org 0x13082
m68k_013082:
        move.w #0xc381,(%a0)+
m68k_013082_end:
.org 0x13086
m68k_013086:
        dbra %d0,(. + -4)
m68k_013086_end:
.org 0x1308A
m68k_01308a:
        move.w #0xcb80,(%a0)+
m68k_01308a_end:
.org 0x1308E
m68k_01308e:
        move.w #0xf,0x22(%a0)
m68k_01308e_end:
.org 0x13094
m68k_013094:
        move.w #0xf,(%a0)+
m68k_013094_end:
.org 0x13098
m68k_013098:
        move.w #0xc594,0x22(%a0)
m68k_013098_end:
.org 0x1309E
m68k_01309e:
        move.w #0xc514,(%a0)+
m68k_01309e_end:
.org 0x130A2
m68k_0130a2:
        move.w #0xc382,0x22(%a0)
m68k_0130a2_end:
.org 0x130A8
m68k_0130a8:
        move.w #0xc382,(%a0)+
m68k_0130a8_end:
.org 0x130AC
m68k_0130ac:
        move.w #0xc01d,%d0
m68k_0130ac_end:
.org 0x130B0
m68k_0130b0:
        move.w #0x3,%d1
m68k_0130b0_end:
.org 0x130B4
m68k_0130b4:
        bsr.w (. + 194)
m68k_0130b4_end:
.org 0x130B8
m68k_0130b8:
        move.w #0xc005,%d0
m68k_0130b8_end:
.org 0x130BC
m68k_0130bc:
        move.w #0x1,%d1
m68k_0130bc_end:
.org 0x130C0
m68k_0130c0:
        bsr.w (. + 182)
m68k_0130c0_end:
.org 0x130C4
m68k_0130c4:
        move.w #0x6,%d0
m68k_0130c4_end:
.org 0x130C8
m68k_0130c8:
        move.w #0xc001,0x22(%a0)
m68k_0130c8_end:
.org 0x130CE
m68k_0130ce:
        move.w #0xc001,(%a0)+
m68k_0130ce_end:
.org 0x130D2
m68k_0130d2:
        dbra %d0,(. + -10)
m68k_0130d2_end:
.org 0x130D6
m68k_0130d6:
        move.w #0xcb82,0x22(%a0)
m68k_0130d6_end:
.org 0x130DC
m68k_0130dc:
        move.w #0xcb82,(%a0)+
m68k_0130dc_end:
.org 0x130E0
m68k_0130e0:
        adda.w #0x22,%a0
m68k_0130e0_end:
.org 0x130E4
m68k_0130e4:
        move.w #0xf,(%a0)+
m68k_0130e4_end:
.org 0x130E8
m68k_0130e8:
        move.w #0xc614,(%a0)+
m68k_0130e8_end:
.org 0x130EC
m68k_0130ec:
        move.w #0xc382,(%a0)+
m68k_0130ec_end:
.org 0x130F0
m68k_0130f0:
        move.w #0xc,%d0
m68k_0130f0_end:
.org 0x130F4
m68k_0130f4:
        move.w #0xc001,(%a0)+
m68k_0130f4_end:
.org 0x130F8
m68k_0130f8:
        dbra %d0,(. + -4)
m68k_0130f8_end:
.org 0x130FC
m68k_0130fc:
        move.w #0xcb82,(%a0)+
m68k_0130fc_end:
.org 0x13100
m68k_013100:
        move.w #0xf,0x22(%a0)
m68k_013100_end:
.org 0x13106
m68k_013106:
        move.w #0xf,(%a0)+
m68k_013106_end:
.org 0x1310A
m68k_01310a:
        move.w #0xc714,0x22(%a0)
m68k_01310a_end:
.org 0x13110
m68k_013110:
        move.w #0xc694,(%a0)+
m68k_013110_end:
.org 0x13114
m68k_013114:
        move.w #0xc382,0x22(%a0)
m68k_013114_end:
.org 0x1311A
m68k_01311a:
        move.w #0xc382,(%a0)+
m68k_01311a_end:
.org 0x1311E
m68k_01311e:
        move.w #0xc009,%d0
m68k_01311e_end:
.org 0x13122
m68k_013122:
        move.w #0x3,%d1
m68k_013122_end:
.org 0x13126
m68k_013126:
        bsr.w (. + 80)
m68k_013126_end:
.org 0x1312A
m68k_01312a:
        move.w #0x8,%d0
m68k_01312a_end:
.org 0x1312E
m68k_01312e:
        move.w #0xc001,0x22(%a0)
m68k_01312e_end:
.org 0x13134
m68k_013134:
        move.w #0xc001,(%a0)+
m68k_013134_end:
.org 0x13138
m68k_013138:
        dbra %d0,(. + -10)
m68k_013138_end:
.org 0x1313C
m68k_01313c:
        move.w #0xcb82,0x22(%a0)
m68k_01313c_end:
.org 0x13142
m68k_013142:
        move.w #0xcb82,(%a0)+
m68k_013142_end:
.org 0x13146
m68k_013146:
        adda.w #0x22,%a0
m68k_013146_end:
.org 0x1314A
m68k_01314a:
        move.w #0xf,(%a0)+
m68k_01314a_end:
.org 0x1314E
m68k_01314e:
        move.w #0xc794,(%a0)+
m68k_01314e_end:
.org 0x13152
m68k_013152:
        move.w #0xd380,(%a0)+
m68k_013152_end:
.org 0x13156
m68k_013156:
        move.w #0xc,%d0
m68k_013156_end:
.org 0x1315A
m68k_01315a:
        move.w #0xd381,(%a0)+
m68k_01315a_end:
.org 0x1315E
m68k_01315e:
        dbra %d0,(. + -4)
m68k_01315e_end:
.org 0x13162
m68k_013162:
        move.w #0xdb80,(%a0)+
m68k_013162_end:
.org 0x13166
m68k_013166:
        clr.w (%a0)
m68k_013166_end:
.org 0x13168
m68k_013168:
        addi.w #0xee,0xf31a:w
m68k_013168_end:
.org 0x1316E
m68k_01316e:
        bset.b #0x0,0xf3a4:w
m68k_01316e_end:
.org 0x13174
m68k_013174:
        rts
m68k_013174_end:
.org 0x13176
m68k_013176:
        move.w %d0,(%a0)
m68k_013176_end:
.org 0x13178
m68k_013178:
        addq.w #0x1,%d0
m68k_013178_end:
.org 0x1317A
m68k_01317a:
        move.w %d0,0x22(%a0)
m68k_01317a_end:
.org 0x1317E
m68k_01317e:
        addq.w #0x1,%d0
m68k_01317e_end:
.org 0x13180
m68k_013180:
        addq.w #0x2,%a0
m68k_013180_end:
.org 0x13182
m68k_013182:
        dbra %d1,(. + -12)
m68k_013182_end:
.org 0x13186
m68k_013186:
        rts
m68k_013186_end:
.org 0x1321C
m68k_01321c:
        move.l 0xf3e4:w,%d0
m68k_01321c_end:
.org 0x13220
m68k_013220:
        move.w #0xc386,%d1
m68k_013220_end:
.org 0x13224
m68k_013224:
        clr.w %d2
m68k_013224_end:
.org 0x13226
m68k_013226:
        lea.l 0xef00:w,%a6
m68k_013226_end:
.org 0x1322A
m68k_01322a:
        jsr 0x1270a:l
m68k_01322a_end:
.org 0x13230
m68k_013230:
        lea.l 0xd100:w,%a0
m68k_013230_end:
.org 0x13234
m68k_013234:
        adda.w 0xf31a:w,%a0
m68k_013234_end:
.org 0x13238
m68k_013238:
        move.w #0x6,(%a0)+
m68k_013238_end:
.org 0x1323C
m68k_01323c:
        move.w #0xc5a4,(%a0)+
m68k_01323c_end:
.org 0x13240
m68k_013240:
        lea.l 0xef00:w,%a1
m68k_013240_end:
.org 0x13244
m68k_013244:
        clr.w %d0
m68k_013244_end:
.org 0x13246
m68k_013246:
        move.w #0x5,%d1
m68k_013246_end:
.org 0x1324A
m68k_01324a:
        move.w (%a1)+,%d2
m68k_01324a_end:
.org 0x1324C
m68k_01324c:
        bne.b (. + 18)
m68k_01324c_end:
.org 0x1324E
m68k_01324e:
        cmp.w 0xf39a:w,%d0
m68k_01324e_end:
.org 0x13252
m68k_013252:
        bcc.b (. + 8)
m68k_013252_end:
.org 0x13254
m68k_013254:
        move.w #0xc001,%d2
m68k_013254_end:
.org 0x13258
m68k_013258:
        bra.b (. + 6)
m68k_013258_end:
.org 0x1325A
m68k_01325a:
        move.w #0xc386,%d2
m68k_01325a_end:
.org 0x1325E
m68k_01325e:
        move.w %d2,(%a0)+
m68k_01325e_end:
.org 0x13260
m68k_013260:
        addq.w #0x1,%d0
m68k_013260_end:
.org 0x13262
m68k_013262:
        dbra %d1,(. + -24)
m68k_013262_end:
.org 0x13266
m68k_013266:
        clr.w (%a0)
m68k_013266_end:
.org 0x13268
m68k_013268:
        addi.w #0x10,0xf31a:w
m68k_013268_end:
.org 0x1326E
m68k_01326e:
        rts
m68k_01326e_end:
.org 0x13270
m68k_013270:
        move.l 0xf39e:w,%d0
m68k_013270_end:
.org 0x13274
m68k_013274:
        move.w #0xc386,%d1
m68k_013274_end:
.org 0x13278
m68k_013278:
        move.w #0xc001,%d2
m68k_013278_end:
.org 0x1327C
m68k_01327c:
        lea.l 0xef0c:w,%a6
m68k_01327c_end:
.org 0x13280
m68k_013280:
        jsr 0x1270a:l
m68k_013280_end:
.org 0x13286
m68k_013286:
        lea.l 0xd100:w,%a0
m68k_013286_end:
.org 0x1328A
m68k_01328a:
        adda.w 0xf31a:w,%a0
m68k_01328a_end:
.org 0x1328E
m68k_01328e:
        move.w #0x6,(%a0)+
m68k_01328e_end:
.org 0x13292
m68k_013292:
        move.w #0xc724,(%a0)+
m68k_013292_end:
.org 0x13296
m68k_013296:
        lea.l 0xef0c:w,%a1
m68k_013296_end:
.org 0x1329A
m68k_01329a:
        move.w #0x2,%d0
m68k_01329a_end:
.org 0x1329E
m68k_01329e:
        move.l (%a1)+,(%a0)+
m68k_01329e_end:
.org 0x132A0
m68k_0132a0:
        dbra %d0,(. + -2)
m68k_0132a0_end:
.org 0x132A4
m68k_0132a4:
        clr.w (%a0)
m68k_0132a4_end:
.org 0x132A6
m68k_0132a6:
        addi.w #0x10,0xf31a:w
m68k_0132a6_end:
.org 0x132AC
m68k_0132ac:
        rts
m68k_0132ac_end:
.org 0x1347C
m68k_01347c:
        jsr 0x5c98:l
m68k_01347c_end:
.org 0x13482
m68k_013482:
        move.l #0xc000000b,%d0
m68k_013482_end:
.org 0x13488
m68k_013488:
        move.w #0x6,%d1
m68k_013488_end:
.org 0x1348C
m68k_01348c:
        move.w #0xc09c,%d2
m68k_01348c_end:
.org 0x13490
m68k_013490:
        lea.l 58(%pc),%a0
m68k_013490_end:
.org 0x13494
m68k_013494:
        jsr 0x26bfa:l
m68k_013494_end:
.org 0x1349A
m68k_01349a:
        move.l #0xc000000f,%d0
m68k_01349a_end:
.org 0x134A0
m68k_0134a0:
        move.w #0x7,%d1
m68k_0134a0_end:
.org 0x134A4
m68k_0134a4:
        move.w #0xc494,%d2
m68k_0134a4_end:
.org 0x134A8
m68k_0134a8:
        lea.l 58(%pc),%a0
m68k_0134a8_end:
.org 0x134AC
m68k_0134ac:
        jsr 0x26bfa:l
m68k_0134ac_end:
.org 0x134B2
m68k_0134b2:
        move.l #0xc000000d,%d0
m68k_0134b2_end:
.org 0x134B8
m68k_0134b8:
        move.w #0x4,%d1
m68k_0134b8_end:
.org 0x134BC
m68k_0134bc:
        move.w #0xc0b4,%d2
m68k_0134bc_end:
.org 0x134C0
m68k_0134c0:
        lea.l 62(%pc),%a0
m68k_0134c0_end:
.org 0x134C4
m68k_0134c4:
        jsr 0x26bfa:l
m68k_0134c4_end:
.org 0x134CA
m68k_0134ca:
        rts
m68k_0134ca_end:
.org 0x13510
m68k_013510:
        btst.b #0x5,0xf603:w
m68k_013510_end:
.org 0x13516
m68k_013516:
        bne.w (. + 38)
m68k_013516_end:
.org 0x1351A
m68k_01351a:
        btst.b #0x3,0xf321:w
m68k_01351a_end:
.org 0x13520
m68k_013520:
        bne.b (. + 28)
m68k_013520_end:
.org 0x13522
m68k_013522:
        lea.l -2708(%pc),%a0
m68k_013522_end:
.org 0x13526
m68k_013526:
        move.w #0x58,%d0
m68k_013526_end:
.org 0x1352A
m68k_01352a:
        move.w 0xf39a:w,%d1
m68k_01352a_end:
.org 0x1352E
m68k_01352e:
        lsl.w #0x3,%d1
m68k_01352e_end:
.org 0x13530
m68k_013530:
        addi.w #0x90,%d1
m68k_013530_end:
.org 0x13534
m68k_013534:
        clr.w %d2
m68k_013534_end:
.org 0x13536
m68k_013536:
        jsr 0xac08:l
m68k_013536_end:
.org 0x1353C
m68k_01353c:
        rts
m68k_01353c_end:
.org 0x1353E
m68k_01353e:
        lea.l 0xd100:w,%a0
m68k_01353e_end:
.org 0x13542
m68k_013542:
        adda.w 0xf31a:w,%a0
m68k_013542_end:
.org 0x13546
m68k_013546:
        move.w #0xf,0xcc(%a0)
m68k_013546_end:
.org 0x1354C
m68k_01354c:
        move.w #0xf,0xaa(%a0)
m68k_01354c_end:
.org 0x13552
m68k_013552:
        move.w #0xf,0x88(%a0)
m68k_013552_end:
.org 0x13558
m68k_013558:
        move.w #0xf,0x66(%a0)
m68k_013558_end:
.org 0x1355E
m68k_01355e:
        move.w #0xf,0x44(%a0)
m68k_01355e_end:
.org 0x13564
m68k_013564:
        move.w #0xf,0x22(%a0)
m68k_013564_end:
.org 0x1356A
m68k_01356a:
        move.w #0xf,(%a0)+
m68k_01356a_end:
.org 0x1356E
m68k_01356e:
        move.w #0xc794,0xcc(%a0)
m68k_01356e_end:
.org 0x13574
m68k_013574:
        move.w #0xc714,0xaa(%a0)
m68k_013574_end:
.org 0x1357A
m68k_01357a:
        move.w #0xc694,0x88(%a0)
m68k_01357a_end:
.org 0x13580
m68k_013580:
        move.w #0xc614,0x66(%a0)
m68k_013580_end:
.org 0x13586
m68k_013586:
        move.w #0xc594,0x44(%a0)
m68k_013586_end:
.org 0x1358C
m68k_01358c:
        move.w #0xc514,0x22(%a0)
m68k_01358c_end:
.org 0x13592
m68k_013592:
        move.w #0xc494,(%a0)+
m68k_013592_end:
.org 0x13596
m68k_013596:
        move.w #0xe,%d0
m68k_013596_end:
.org 0x1359A
m68k_01359a:
        clr.w 0xcc(%a0)
m68k_01359a_end:
.org 0x1359E
m68k_01359e:
        clr.w 0xaa(%a0)
m68k_01359e_end:
.org 0x135A2
m68k_0135a2:
        clr.w 0x88(%a0)
m68k_0135a2_end:
.org 0x135A6
m68k_0135a6:
        clr.w 0x66(%a0)
m68k_0135a6_end:
.org 0x135AA
m68k_0135aa:
        clr.w 0x44(%a0)
m68k_0135aa_end:
.org 0x135AE
m68k_0135ae:
        clr.w 0x22(%a0)
m68k_0135ae_end:
.org 0x135B2
m68k_0135b2:
        clr.w (%a0)+
m68k_0135b2_end:
.org 0x135B4
m68k_0135b4:
        dbra %d0,(. + -26)
m68k_0135b4_end:
.org 0x135B8
m68k_0135b8:
        clr.w 0xcc(%a0)
m68k_0135b8_end:
.org 0x135BC
m68k_0135bc:
        addi.w #0xee,0xf31a:w
m68k_0135bc_end:
.org 0x135C2
m68k_0135c2:
        rts
m68k_0135c2_end:
.org 0x135C4
m68k_0135c4:
        lea.l 0xd100:w,%a0
m68k_0135c4_end:
.org 0x135C8
m68k_0135c8:
        adda.w 0xf31a:w,%a0
m68k_0135c8_end:
.org 0x135CC
m68k_0135cc:
        move.w #0xf,(%a0)+
m68k_0135cc_end:
.org 0x135D0
m68k_0135d0:
        move.w #0xc494,(%a0)+
m68k_0135d0_end:
.org 0x135D4
m68k_0135d4:
        move.w #0xc380,(%a0)+
m68k_0135d4_end:
.org 0x135D8
m68k_0135d8:
        move.w #0xc,%d0
m68k_0135d8_end:
.org 0x135DC
m68k_0135dc:
        move.w #0xc381,(%a0)+
m68k_0135dc_end:
.org 0x135E0
m68k_0135e0:
        dbra %d0,(. + -4)
m68k_0135e0_end:
.org 0x135E4
m68k_0135e4:
        move.w #0xcb80,(%a0)+
m68k_0135e4_end:
.org 0x135E8
m68k_0135e8:
        move.w #0xf,0x22(%a0)
m68k_0135e8_end:
.org 0x135EE
m68k_0135ee:
        move.w #0xf,(%a0)+
m68k_0135ee_end:
.org 0x135F2
m68k_0135f2:
        move.w #0xc594,0x22(%a0)
m68k_0135f2_end:
.org 0x135F8
m68k_0135f8:
        move.w #0xc514,(%a0)+
m68k_0135f8_end:
.org 0x135FC
m68k_0135fc:
        move.w #0xc382,0x22(%a0)
m68k_0135fc_end:
.org 0x13602
m68k_013602:
        move.w #0xc382,(%a0)+
m68k_013602_end:
.org 0x13606
m68k_013606:
        move.w #0xc011,%d0
m68k_013606_end:
.org 0x1360A
m68k_01360a:
        move.w #0x3,%d1
m68k_01360a_end:
.org 0x1360E
m68k_01360e:
        bsr.w (. + 212)
m68k_01360e_end:
.org 0x13612
m68k_013612:
        move.w #0xc021,%d0
m68k_013612_end:
.org 0x13616
m68k_013616:
        move.w #0x1,%d1
m68k_013616_end:
.org 0x1361A
m68k_01361a:
        bsr.w (. + 200)
m68k_01361a_end:
.org 0x1361E
m68k_01361e:
        move.w #0x6,%d0
m68k_01361e_end:
.org 0x13622
m68k_013622:
        move.w #0xc001,0x22(%a0)
m68k_013622_end:
.org 0x13628
m68k_013628:
        move.w #0xc001,(%a0)+
m68k_013628_end:
.org 0x1362C
m68k_01362c:
        dbra %d0,(. + -10)
m68k_01362c_end:
.org 0x13630
m68k_013630:
        move.w #0xcb82,0x22(%a0)
m68k_013630_end:
.org 0x13636
m68k_013636:
        move.w #0xcb82,(%a0)+
m68k_013636_end:
.org 0x1363A
m68k_01363a:
        adda.w #0x22,%a0
m68k_01363a_end:
.org 0x1363E
m68k_01363e:
        move.w #0xf,(%a0)+
m68k_01363e_end:
.org 0x13642
m68k_013642:
        move.w #0xc614,(%a0)+
m68k_013642_end:
.org 0x13646
m68k_013646:
        move.w #0xc382,(%a0)+
m68k_013646_end:
.org 0x1364A
m68k_01364a:
        move.w #0xc,%d0
m68k_01364a_end:
.org 0x1364E
m68k_01364e:
        move.w #0xc001,(%a0)+
m68k_01364e_end:
.org 0x13652
m68k_013652:
        dbra %d0,(. + -4)
m68k_013652_end:
.org 0x13656
m68k_013656:
        move.w #0xcb82,(%a0)+
m68k_013656_end:
.org 0x1365A
m68k_01365a:
        move.w #0xf,0x22(%a0)
m68k_01365a_end:
.org 0x13660
m68k_013660:
        move.w #0xf,(%a0)+
m68k_013660_end:
.org 0x13664
m68k_013664:
        move.w #0xc714,0x22(%a0)
m68k_013664_end:
.org 0x1366A
m68k_01366a:
        move.w #0xc694,(%a0)+
m68k_01366a_end:
.org 0x1366E
m68k_01366e:
        move.w #0xc382,0x22(%a0)
m68k_01366e_end:
.org 0x13674
m68k_013674:
        move.w #0xc382,(%a0)+
m68k_013674_end:
.org 0x13678
m68k_013678:
        move.w #0xc019,%d0
m68k_013678_end:
.org 0x1367C
m68k_01367c:
        move.w #0x1,%d1
m68k_01367c_end:
.org 0x13680
m68k_013680:
        bsr.w (. + 98)
m68k_013680_end:
.org 0x13684
m68k_013684:
        move.w #0xc025,%d0
m68k_013684_end:
.org 0x13688
m68k_013688:
        move.w #0x1,%d1
m68k_013688_end:
.org 0x1368C
m68k_01368c:
        bsr.w (. + 86)
m68k_01368c_end:
.org 0x13690
m68k_013690:
        move.w #0xc021,%d0
m68k_013690_end:
.org 0x13694
m68k_013694:
        move.w #0x1,%d1
m68k_013694_end:
.org 0x13698
m68k_013698:
        bsr.w (. + 74)
m68k_013698_end:
.org 0x1369C
m68k_01369c:
        move.w #0x6,%d0
m68k_01369c_end:
.org 0x136A0
m68k_0136a0:
        move.w #0xc001,0x22(%a0)
m68k_0136a0_end:
.org 0x136A6
m68k_0136a6:
        move.w #0xc001,(%a0)+
m68k_0136a6_end:
.org 0x136AA
m68k_0136aa:
        dbra %d0,(. + -10)
m68k_0136aa_end:
.org 0x136AE
m68k_0136ae:
        move.w #0xcb82,0x22(%a0)
m68k_0136ae_end:
.org 0x136B4
m68k_0136b4:
        move.w #0xcb82,(%a0)+
m68k_0136b4_end:
.org 0x136B8
m68k_0136b8:
        adda.w #0x22,%a0
m68k_0136b8_end:
.org 0x136BC
m68k_0136bc:
        move.w #0xf,(%a0)+
m68k_0136bc_end:
.org 0x136C0
m68k_0136c0:
        move.w #0xc794,(%a0)+
m68k_0136c0_end:
.org 0x136C4
m68k_0136c4:
        move.w #0xd380,(%a0)+
m68k_0136c4_end:
.org 0x136C8
m68k_0136c8:
        move.w #0xc,%d0
m68k_0136c8_end:
.org 0x136CC
m68k_0136cc:
        move.w #0xd381,(%a0)+
m68k_0136cc_end:
.org 0x136D0
m68k_0136d0:
        dbra %d0,(. + -4)
m68k_0136d0_end:
.org 0x136D4
m68k_0136d4:
        move.w #0xdb80,(%a0)+
m68k_0136d4_end:
.org 0x136D8
m68k_0136d8:
        clr.w (%a0)
m68k_0136d8_end:
.org 0x136DA
m68k_0136da:
        addi.w #0xee,0xf31a:w
m68k_0136da_end:
.org 0x136E0
m68k_0136e0:
        rts
m68k_0136e0_end:
.org 0x136E2
m68k_0136e2:
        move.w %d0,(%a0)
m68k_0136e2_end:
.org 0x136E4
m68k_0136e4:
        addq.w #0x1,%d0
m68k_0136e4_end:
.org 0x136E6
m68k_0136e6:
        move.w %d0,0x22(%a0)
m68k_0136e6_end:
.org 0x136EA
m68k_0136ea:
        addq.w #0x1,%d0
m68k_0136ea_end:
.org 0x136EC
m68k_0136ec:
        addq.w #0x2,%a0
m68k_0136ec_end:
.org 0x136EE
m68k_0136ee:
        dbra %d1,(. + -12)
m68k_0136ee_end:
.org 0x136F2
m68k_0136f2:
        rts
m68k_0136f2_end:
.org 0x136F4
m68k_0136f4:
        move.l 0xf3ee:w,%d0
m68k_0136f4_end:
.org 0x136F8
m68k_0136f8:
        move.w #0xc386,%d1
m68k_0136f8_end:
.org 0x136FC
m68k_0136fc:
        clr.w %d2
m68k_0136fc_end:
.org 0x136FE
m68k_0136fe:
        lea.l 0xef00:w,%a6
m68k_0136fe_end:
.org 0x13702
m68k_013702:
        jsr 0x1270a:l
m68k_013702_end:
.org 0x13708
m68k_013708:
        lea.l 0xd100:w,%a0
m68k_013708_end:
.org 0x1370C
m68k_01370c:
        adda.w 0xf31a:w,%a0
m68k_01370c_end:
.org 0x13710
m68k_013710:
        move.w #0x6,(%a0)+
m68k_013710_end:
.org 0x13714
m68k_013714:
        move.w #0xc5a4,(%a0)+
m68k_013714_end:
.org 0x13718
m68k_013718:
        clr.w %d1
m68k_013718_end:
.org 0x1371A
m68k_01371a:
        lea.l 0xef00:w,%a1
m68k_01371a_end:
.org 0x1371E
m68k_01371e:
        move.w #0x5,%d0
m68k_01371e_end:
.org 0x13722
m68k_013722:
        move.w (%a1)+,%d2
m68k_013722_end:
.org 0x13724
m68k_013724:
        bne.b (. + 20)
m68k_013724_end:
.org 0x13726
m68k_013726:
        cmp.w 0xf39a:w,%d1
m68k_013726_end:
.org 0x1372A
m68k_01372a:
        bcs.w (. + 10)
m68k_01372a_end:
.org 0x1372E
m68k_01372e:
        move.w #0xc386,%d2
m68k_01372e_end:
.org 0x13732
m68k_013732:
        bra.b (. + 6)
m68k_013732_end:
.org 0x13734
m68k_013734:
        move.w #0xc001,%d2
m68k_013734_end:
.org 0x13738
m68k_013738:
        move.w %d2,(%a0)+
m68k_013738_end:
.org 0x1373A
m68k_01373a:
        addq.w #0x1,%d1
m68k_01373a_end:
.org 0x1373C
m68k_01373c:
        dbra %d0,(. + -26)
m68k_01373c_end:
.org 0x13740
m68k_013740:
        clr.w (%a0)
m68k_013740_end:
.org 0x13742
m68k_013742:
        addi.w #0x10,0xf31a:w
m68k_013742_end:
.org 0x13748
m68k_013748:
        rts
m68k_013748_end:
.org 0x1374A
m68k_01374a:
        cmpi.w #0x1b,0xf362:w
m68k_01374a_end:
.org 0x13750
m68k_013750:
        beq.w (. + 12)
m68k_013750_end:
.org 0x13754
m68k_013754:
        move.l 0xf3e4:w,%d0
m68k_013754_end:
.org 0x13758
m68k_013758:
        bra.w (. + 8)
m68k_013758_end:
.org 0x1375C
m68k_01375c:
        move.l 0xcfae:w,%d0
m68k_01375c_end:
.org 0x13760
m68k_013760:
        move.w #0xc386,%d1
m68k_013760_end:
.org 0x13764
m68k_013764:
        move.w #0xc001,%d2
m68k_013764_end:
.org 0x13768
m68k_013768:
        lea.l 0xef0c:w,%a6
m68k_013768_end:
.org 0x1376C
m68k_01376c:
        jsr 0x1270a:l
m68k_01376c_end:
.org 0x13772
m68k_013772:
        lea.l 0xd100:w,%a0
m68k_013772_end:
.org 0x13776
m68k_013776:
        adda.w 0xf31a:w,%a0
m68k_013776_end:
.org 0x1377A
m68k_01377a:
        move.w #0x6,(%a0)+
m68k_01377a_end:
.org 0x1377E
m68k_01377e:
        move.w #0xc724,(%a0)+
m68k_01377e_end:
.org 0x13782
m68k_013782:
        lea.l 0xef0c:w,%a1
m68k_013782_end:
.org 0x13786
m68k_013786:
        move.w #0x2,%d0
m68k_013786_end:
.org 0x1378A
m68k_01378a:
        move.l (%a1)+,(%a0)+
m68k_01378a_end:
.org 0x1378C
m68k_01378c:
        dbra %d0,(. + -2)
m68k_01378c_end:
.org 0x13790
m68k_013790:
        clr.w (%a0)
m68k_013790_end:
.org 0x13792
m68k_013792:
        addi.w #0x10,0xf31a:w
m68k_013792_end:
.org 0x13798
m68k_013798:
        rts
m68k_013798_end:
.org 0x13934
m68k_013934:
        btst.b #0x3,0xf321:w
m68k_013934_end:
.org 0x1393A
m68k_01393a:
        bne.b (. + 28)
m68k_01393a_end:
.org 0x1393C
m68k_01393c:
        lea.l -3758(%pc),%a0
m68k_01393c_end:
.org 0x13940
m68k_013940:
        move.w #0x58,%d0
m68k_013940_end:
.org 0x13944
m68k_013944:
        move.w 0xf39a:w,%d1
m68k_013944_end:
.org 0x13948
m68k_013948:
        lsl.w #0x3,%d1
m68k_013948_end:
.org 0x1394A
m68k_01394a:
        addi.w #0x90,%d1
m68k_01394a_end:
.org 0x1394E
m68k_01394e:
        clr.w %d2
m68k_01394e_end:
.org 0x13950
m68k_013950:
        jsr 0xac08:l
m68k_013950_end:
.org 0x13956
m68k_013956:
        rts
m68k_013956_end:
.org 0x13B86
m68k_013b86:
        move.b 0xf602:w,%d0
m68k_013b86_end:
.org 0x13B8A
m68k_013b8a:
        andi.w #0x3,%d0
m68k_013b8a_end:
.org 0x13B8E
m68k_013b8e:
        beq.b (. + 68)
m68k_013b8e_end:
.org 0x13B90
m68k_013b90:
        subq.w #0x1,0xf608:w
m68k_013b90_end:
.org 0x13B94
m68k_013b94:
        bne.b (. + 68)
m68k_013b94_end:
.org 0x13B96
m68k_013b96:
        move.w #0xc,0xf608:w
m68k_013b96_end:
.org 0x13B9C
m68k_013b9c:
        btst.l #0x1,%d0
m68k_013b9c_end:
.org 0x13BA0
m68k_013ba0:
        bne.b (. + 24)
m68k_013ba0_end:
.org 0x13BA2
m68k_013ba2:
        tst.w 0xf688:w
m68k_013ba2_end:
.org 0x13BA6
m68k_013ba6:
        bne.b (. + 12)
m68k_013ba6_end:
.org 0x13BA8
m68k_013ba8:
        move.w #0x2,0xf688:w
m68k_013ba8_end:
.org 0x13BAE
m68k_013bae:
        bra.w (. + 42)
m68k_013bae_end:
.org 0x13BB2
m68k_013bb2:
        subq.w #0x1,0xf688:w
m68k_013bb2_end:
.org 0x13BB6
m68k_013bb6:
        bra.b (. + 34)
m68k_013bb6_end:
.org 0x13BB8
m68k_013bb8:
        cmpi.w #0x2,0xf688:w
m68k_013bb8_end:
.org 0x13BBE
m68k_013bbe:
        bcs.b (. + 10)
m68k_013bbe_end:
.org 0x13BC0
m68k_013bc0:
        clr.w 0xf688:w
m68k_013bc0_end:
.org 0x13BC4
m68k_013bc4:
        bra.w (. + 20)
m68k_013bc4_end:
.org 0x13BC8
m68k_013bc8:
        addi.w #0x1,0xf688:w
m68k_013bc8_end:
.org 0x13BCE
m68k_013bce:
        bra.w (. + 10)
m68k_013bce_end:
.org 0x13BD2
m68k_013bd2:
        move.w #0x1,0xf608:w
m68k_013bd2_end:
.org 0x13BD8
m68k_013bd8:
        rts
m68k_013bd8_end:
.org 0x13BDA
m68k_013bda:
        btst.b #0x5,0xf603:w
m68k_013bda_end:
.org 0x13BE0
m68k_013be0:
        bne.w (. + 58)
m68k_013be0_end:
.org 0x13BE4
m68k_013be4:
        move.b 0xf602:w,%d0
m68k_013be4_end:
.org 0x13BE8
m68k_013be8:
        andi.w #0x3,%d0
m68k_013be8_end:
.org 0x13BEC
m68k_013bec:
        bne.w (. + 12)
m68k_013bec_end:
.org 0x13BF0
m68k_013bf0:
        btst.b #0x4,0xf321:w
m68k_013bf0_end:
.org 0x13BF6
m68k_013bf6:
        bne.b (. + 36)
m68k_013bf6_end:
.org 0x13BF8
m68k_013bf8:
        lea.l 34(%pc),%a0
m68k_013bf8_end:
.org 0x13BFC
m68k_013bfc:
        nop
m68k_013bfc_end:
.org 0x13BFE
m68k_013bfe:
        move.w 0xf688:w,%d0
m68k_013bfe_end:
.org 0x13C02
m68k_013c02:
        lsl.w #0x1,%d0
m68k_013c02_end:
.org 0x13C04
m68k_013c04:
        add.w 0xf688:w,%d0
m68k_013c04_end:
.org 0x13C08
m68k_013c08:
        lsl.w #0x3,%d0
m68k_013c08_end:
.org 0x13C0A
m68k_013c0a:
        addi.w #0x40,%d0
m68k_013c0a_end:
.org 0x13C0E
m68k_013c0e:
        move.w #0x80,%d1
m68k_013c0e_end:
.org 0x13C12
m68k_013c12:
        clr.w %d2
m68k_013c12_end:
.org 0x13C14
m68k_013c14:
        jsr 0xac08:l
m68k_013c14_end:
.org 0x13C1A
m68k_013c1a:
        rts
m68k_013c1a_end:
.org 0x13C7E
m68k_013c7e:
        lea.l 0xd100:w,%a0
m68k_013c7e_end:
.org 0x13C82
m68k_013c82:
        adda.w 0xf31a:w,%a0
m68k_013c82_end:
.org 0x13C86
m68k_013c86:
        move.w #0x8,0xb4(%a0)
m68k_013c86_end:
.org 0x13C8C
m68k_013c8c:
        move.w #0x8,0xa0(%a0)
m68k_013c8c_end:
.org 0x13C92
m68k_013c92:
        move.w #0x8,0x8c(%a0)
m68k_013c92_end:
.org 0x13C98
m68k_013c98:
        move.w #0x8,0x78(%a0)
m68k_013c98_end:
.org 0x13C9E
m68k_013c9e:
        move.w #0x8,0x64(%a0)
m68k_013c9e_end:
.org 0x13CA4
m68k_013ca4:
        move.w #0x8,0x50(%a0)
m68k_013ca4_end:
.org 0x13CAA
m68k_013caa:
        move.w #0x8,0x3c(%a0)
m68k_013caa_end:
.org 0x13CB0
m68k_013cb0:
        move.w #0x8,0x28(%a0)
m68k_013cb0_end:
.org 0x13CB6
m68k_013cb6:
        move.w #0x8,0x14(%a0)
m68k_013cb6_end:
.org 0x13CBC
m68k_013cbc:
        move.w #0x8,(%a0)+
m68k_013cbc_end:
.org 0x13CC0
m68k_013cc0:
        move.w #0xc8a0,0xb4(%a0)
m68k_013cc0_end:
.org 0x13CC6
m68k_013cc6:
        move.w #0xc820,0xa0(%a0)
m68k_013cc6_end:
.org 0x13CCC
m68k_013ccc:
        move.w #0xc7a0,0x8c(%a0)
m68k_013ccc_end:
.org 0x13CD2
m68k_013cd2:
        move.w #0xc720,0x78(%a0)
m68k_013cd2_end:
.org 0x13CD8
m68k_013cd8:
        move.w #0xc6a0,0x64(%a0)
m68k_013cd8_end:
.org 0x13CDE
m68k_013cde:
        move.w #0xc620,0x50(%a0)
m68k_013cde_end:
.org 0x13CE4
m68k_013ce4:
        move.w #0xc5a0,0x3c(%a0)
m68k_013ce4_end:
.org 0x13CEA
m68k_013cea:
        move.w #0xc520,0x28(%a0)
m68k_013cea_end:
.org 0x13CF0
m68k_013cf0:
        move.w #0xc4a0,0x14(%a0)
m68k_013cf0_end:
.org 0x13CF6
m68k_013cf6:
        move.w #0xc420,(%a0)+
m68k_013cf6_end:
.org 0x13CFA
m68k_013cfa:
        move.w #0x7,%d0
m68k_013cfa_end:
.org 0x13CFE
m68k_013cfe:
        move.w #0x8000,0xb4(%a0)
m68k_013cfe_end:
.org 0x13D04
m68k_013d04:
        move.w #0x8000,0xa0(%a0)
m68k_013d04_end:
.org 0x13D0A
m68k_013d0a:
        move.w #0x8000,0x8c(%a0)
m68k_013d0a_end:
.org 0x13D10
m68k_013d10:
        move.w #0x8000,0x78(%a0)
m68k_013d10_end:
.org 0x13D16
m68k_013d16:
        move.w #0x8000,0x64(%a0)
m68k_013d16_end:
.org 0x13D1C
m68k_013d1c:
        move.w #0x8000,0x50(%a0)
m68k_013d1c_end:
.org 0x13D22
m68k_013d22:
        move.w #0x8000,0x3c(%a0)
m68k_013d22_end:
.org 0x13D28
m68k_013d28:
        move.w #0x8000,0x28(%a0)
m68k_013d28_end:
.org 0x13D2E
m68k_013d2e:
        move.w #0x8000,0x14(%a0)
m68k_013d2e_end:
.org 0x13D34
m68k_013d34:
        move.w #0x8000,(%a0)+
m68k_013d34_end:
.org 0x13D38
m68k_013d38:
        dbra %d0,(. + -58)
m68k_013d38_end:
.org 0x13D3C
m68k_013d3c:
        clr.w 0xb4(%a0)
m68k_013d3c_end:
.org 0x13D40
m68k_013d40:
        addi.w #0xc8,0xf31a:w
m68k_013d40_end:
.org 0x13D46
m68k_013d46:
        rts
m68k_013d46_end:
.org 0x14D86
m68k_014d86:
        move.w #0x3a0,%d3
m68k_014d86_end:
.org 0x14DA6
m68k_014da6:
        subq.w #0x3,%d3
m68k_014da6_end:
.org 0x14DA8
m68k_014da8:
        bcs.b (. + 6)
m68k_014da8_end:
.org 0x14DAA
m68k_014daa:
        cmp.w %d1,%d3
m68k_014daa_end:
.org 0x14DAC
m68k_014dac:
        bcc.b (. + 4)
m68k_014dac_end:
.org 0x14DAE
m68k_014dae:
        move.w %d1,%d3
m68k_014dae_end:
.org 0x14DB0
m68k_014db0:
        move.w %d3,0xf314:w
m68k_014db0_end:
.org 0x14DB4
m68k_014db4:
        addq.w #0x1,%d4
m68k_014db4_end:
.org 0x14DB6
m68k_014db6:
        movea.w %d3,%a5
m68k_014db6_end:
.org 0x14DB8
m68k_014db8:
        move.w %d4,-(%a7)
m68k_014db8_end:
.org 0x14DBA
m68k_014dba:
        move.w %d2,-(%a7)
m68k_014dba_end:
.org 0x14DBC
m68k_014dbc:
        jsr 0xa0cc:l
m68k_014dbc_end:
.org 0x14DC2
m68k_014dc2:
        move.w (%a7)+,%d2
m68k_014dc2_end:
.org 0x14DC4
m68k_014dc4:
        move.w (%a7)+,%d4
m68k_014dc4_end:
.org 0x14DDC
m68k_014ddc:
        move.w %d2,%d3
m68k_014ddc_end:
.org 0x14DE4
m68k_014de4:
        move.w #0x340,%d3
m68k_014de4_end:
.org 0x15DF0
m68k_015df0:
        btst.l #0x5,%d4
m68k_015df0_end:
.org 0x15DF4
m68k_015df4:
        bne.b (. + 54)
m68k_015df4_end:
.org 0x15DF6
m68k_015df6:
        clr.w %d5
m68k_015df6_end:
.org 0x15DF8
m68k_015df8:
        move.b 0x1(%a2),%d5
m68k_015df8_end:
.org 0x15DFC
m68k_015dfc:
        lsl.w #0x4,%d5
m68k_015dfc_end:
.org 0x15DFE
m68k_015dfe:
        addi.w #0x10,%d5
m68k_015dfe_end:
.org 0x15E02
m68k_015e02:
        sub.w 0xf314:w,%d5
m68k_015e02_end:
.org 0x15E06
m68k_015e06:
        bcs.b (. + 36)
m68k_015e06_end:
.org 0x15E08
m68k_015e08:
        cmpi.w #0xf0,%d5
m68k_015e08_end:
.org 0x15E0C
m68k_015e0c:
        bcc.b (. + 30)
m68k_015e0c_end:
.org 0x15E0E
m68k_015e0e:
        clr.w %d5
m68k_015e0e_end:
.org 0x15E10
m68k_015e10:
        move.b 0x2(%a2),%d5
m68k_015e10_end:
.org 0x15E14
m68k_015e14:
        lsl.w #0x4,%d5
m68k_015e14_end:
.org 0x15E16
m68k_015e16:
        addi.w #0x10,%d5
m68k_015e16_end:
.org 0x15E1A
m68k_015e1a:
        sub.w 0xf318:w,%d5
m68k_015e1a_end:
.org 0x15E1E
m68k_015e1e:
        bcs.b (. + 12)
m68k_015e1e_end:
.org 0x15E20
m68k_015e20:
        cmpi.w #0x150,%d5
m68k_015e20_end:
.org 0x15E24
m68k_015e24:
        bcc.b (. + 6)
m68k_015e24_end:
.org 0x15E26
m68k_015e26:
        bsr.w (. + 24)
m68k_015e26_end:
.org 0x15E2A
m68k_015e2a:
        clr.w %d5
m68k_015e2a_end:
.org 0x15E2C
m68k_015e2c:
        move.b (%a2),%d5
m68k_015e2c_end:
.org 0x15E2E
m68k_015e2e:
        andi.w #0xf,%d5
m68k_015e2e_end:
.org 0x15E32
m68k_015e32:
        lea.l 0xd(%a2, %d5.w),%a2
m68k_015e32_end:
.org 0x15E36
m68k_015e36:
        bra.b (. + -76)
m68k_015e36_end:
.org 0x15E3E
m68k_015e3e:
        cmpi.w #0x2,0xf36c:w
m68k_015e3e_end:
.org 0x15E44
m68k_015e44:
        bne.b (. + 28)
m68k_015e44_end:
.org 0x15E46
m68k_015e46:
        move.b 0x4(%a2),%d0
m68k_015e46_end:
.org 0x15E4A
m68k_015e4a:
        cmp.b 0xf377:w,%d0
m68k_015e4a_end:
.org 0x15E4E
m68k_015e4e:
        bne.b (. + 18)
m68k_015e4e_end:
.org 0x15E50
m68k_015e50:
        move.b (%a2),%d0
m68k_015e50_end:
.org 0x15E52
m68k_015e52:
        btst.l #0x4,%d0
m68k_015e52_end:
.org 0x15E56
m68k_015e56:
        bne.b (. + 10)
m68k_015e56_end:
.org 0x15E58
m68k_015e58:
        btst.b #0x2,0xf321:w
m68k_015e58_end:
.org 0x15E5E
m68k_015e5e:
        bne.b (. + 40)
m68k_015e5e_end:
.org 0x15E60
m68k_015e60:
        bsr.w (. + 112)
m68k_015e60_end:
.org 0x15E64
m68k_015e64:
        bsr.w (. + 36)
m68k_015e64_end:
.org 0x15E68
m68k_015e68:
        clr.w %d2
m68k_015e68_end:
.org 0x15E6A
m68k_015e6a:
        tst.b (%a2)
m68k_015e6a_end:
.org 0x15E6C
m68k_015e6c:
        bpl.w (. + 8)
m68k_015e6c_end:
.org 0x15E70
m68k_015e70:
        move.w #0x800,%d2
m68k_015e70_end:
.org 0x15E74
m68k_015e74:
        move.w 0xf314:w,0xf60a:w
m68k_015e74_end:
.org 0x15E7A
m68k_015e7a:
        move.w 0xf318:w,0xf60e:w
m68k_015e7a_end:
.org 0x15E80
m68k_015e80:
        jsr 0xac10:l
m68k_015e80_end:
.org 0x15E86
m68k_015e86:
        rts
m68k_015e86_end:
.org 0x15E88
m68k_015e88:
        lea.l 46(%pc),%a0
m68k_015e88_end:
.org 0x15E8C
m68k_015e8c:
        nop
m68k_015e8c_end:
.org 0x15E8E
m68k_015e8e:
        btst.b #0x4,0xf321:w
m68k_015e8e_end:
.org 0x15E94
m68k_015e94:
        beq.w (. + 8)
m68k_015e94_end:
.org 0x15E98
m68k_015e98:
        adda.w #0x8,%a0
m68k_015e98_end:
.org 0x15E9C
m68k_015e9c:
        movem.l %d0-%d1/%a0/%a2,-(%a7)
m68k_015e9c_end:
.org 0x15EA0
m68k_015ea0:
        bsr.w (. + -7180)
m68k_015ea0_end:
.org 0x15EA4
m68k_015ea4:
        movem.l (%a7)+,%d0-%d1/%a0/%a2
m68k_015ea4_end:
.org 0x15EA8
m68k_015ea8:
        cmpi.w #0x4,%d2
m68k_015ea8_end:
.org 0x15EAC
m68k_015eac:
        bne.w (. + 10)
m68k_015eac_end:
.org 0x15EB0
m68k_015eb0:
        lea.l 22(%pc),%a0
m68k_015eb0_end:
.org 0x15EB4
m68k_015eb4:
        nop
m68k_015eb4_end:
.org 0x15EB6
m68k_015eb6:
        rts
m68k_015eb6_end:
.org 0x15ED0
m68k_015ed0:
        cmpi.w #0x209,0xf612:w
m68k_015ed0_end:
.org 0x15ED6
m68k_015ed6:
        bne.b (. + 22)
m68k_015ed6_end:
.org 0x15ED8
m68k_015ed8:
        cmpi.w #0x6,0xf362:w
m68k_015ed8_end:
.org 0x15EDE
m68k_015ede:
        bne.b (. + 14)
m68k_015ede_end:
.org 0x15EE0
m68k_015ee0:
        move.w 0xff3bb4:l,%d0
m68k_015ee0_end:
.org 0x15EE6
m68k_015ee6:
        cmp.b 0xd(%a2),%d0
m68k_015ee6_end:
.org 0x15EEA
m68k_015eea:
        beq.b (. + 28)
m68k_015eea_end:
.org 0x15EEC
m68k_015eec:
        clr.w %d0
m68k_015eec_end:
.org 0x15EEE
m68k_015eee:
        move.b 0x1(%a2),%d0
m68k_015eee_end:
.org 0x15EF2
m68k_015ef2:
        lsl.w #0x4,%d0
m68k_015ef2_end:
.org 0x15EF4
m68k_015ef4:
        addi.w #0x8,%d0
m68k_015ef4_end:
.org 0x15EF8
m68k_015ef8:
        clr.w %d1
m68k_015ef8_end:
.org 0x15EFA
m68k_015efa:
        move.b 0x2(%a2),%d1
m68k_015efa_end:
.org 0x15EFE
m68k_015efe:
        lsl.w #0x4,%d1
m68k_015efe_end:
.org 0x15F00
m68k_015f00:
        addi.w #0x8,%d1
m68k_015f00_end:
.org 0x15F04
m68k_015f04:
        bra.b (. + 22)
m68k_015f04_end:
.org 0x15F06
m68k_015f06:
        move.w 0xff3bb6:l,%d0
m68k_015f06_end:
.org 0x15F0C
m68k_015f0c:
        addi.w #0x8,%d0
m68k_015f0c_end:
.org 0x15F10
m68k_015f10:
        move.w 0xff3bb8:l,%d1
m68k_015f10_end:
.org 0x15F16
m68k_015f16:
        addi.w #0x8,%d1
m68k_015f16_end:
.org 0x15F1A
m68k_015f1a:
        rts
m68k_015f1a_end:
.org 0x15F24
m68k_015f24:
        move.w (%a1)+,%d1
m68k_015f24_end:
.org 0x15F26
m68k_015f26:
        move.w %d0,%d2
m68k_015f26_end:
.org 0x15F28
m68k_015f28:
        addi.w #0x10,%d2
m68k_015f28_end:
.org 0x15F2C
m68k_015f2c:
        sub.w 0xf314:w,%d2
m68k_015f2c_end:
.org 0x15F30
m68k_015f30:
        bcs.w (. + -16)
m68k_015f30_end:
.org 0x15F34
m68k_015f34:
        cmpi.w #0xf0,%d2
m68k_015f34_end:
.org 0x15F38
m68k_015f38:
        bhi.b (. + -24)
m68k_015f38_end:
.org 0x15F3A
m68k_015f3a:
        move.w %d1,%d2
m68k_015f3a_end:
.org 0x15F3C
m68k_015f3c:
        addi.w #0x10,%d2
m68k_015f3c_end:
.org 0x15F40
m68k_015f40:
        sub.w 0xf318:w,%d2
m68k_015f40_end:
.org 0x15F44
m68k_015f44:
        bcs.b (. + -36)
m68k_015f44_end:
.org 0x15F46
m68k_015f46:
        cmpi.w #0x150,%d2
m68k_015f46_end:
.org 0x15F4A
m68k_015f4a:
        bhi.b (. + -42)
m68k_015f4a_end:
.org 0x15F4C
m68k_015f4c:
        lea.l 28(%pc),%a0
m68k_015f4c_end:
.org 0x15F50
m68k_015f50:
        nop
m68k_015f50_end:
.org 0x15F52
m68k_015f52:
        clr.w %d2
m68k_015f52_end:
.org 0x15F54
m68k_015f54:
        move.w 0xf314:w,0xf60a:w
m68k_015f54_end:
.org 0x15F5A
m68k_015f5a:
        move.w 0xf318:w,0xf60e:w
m68k_015f5a_end:
.org 0x15F60
m68k_015f60:
        jsr 0xac10:l
m68k_015f60_end:
.org 0x15F66
m68k_015f66:
        bra.b (. + -70)
m68k_015f66_end:
.org 0x1626C
m68k_01626c:
        jsr 0x5abc:l
m68k_01626c_end:
.org 0x16272
m68k_016272:
        lea.l 0xd100:w,%a0
m68k_016272_end:
.org 0x16276
m68k_016276:
        adda.w 0xf31a:w,%a0
m68k_016276_end:
.org 0x1627A
m68k_01627a:
        move.w #0xa,0x48(%a0)
m68k_01627a_end:
.org 0x16280
m68k_016280:
        move.w #0xa,0x30(%a0)
m68k_016280_end:
.org 0x16286
m68k_016286:
        move.w #0xa,0x18(%a0)
m68k_016286_end:
.org 0x1628C
m68k_01628c:
        move.w #0xa,(%a0)+
m68k_01628c_end:
.org 0x16290
m68k_016290:
        move.w #0xc21c,0x48(%a0)
m68k_016290_end:
.org 0x16296
m68k_016296:
        move.w #0xc19c,0x30(%a0)
m68k_016296_end:
.org 0x1629C
m68k_01629c:
        move.w #0xc11c,0x18(%a0)
m68k_01629c_end:
.org 0x162A2
m68k_0162a2:
        move.w #0xc09c,(%a0)+
m68k_0162a2_end:
.org 0x162A6
m68k_0162a6:
        move.w #0xd380,0x48(%a0)
m68k_0162a6_end:
.org 0x162AC
m68k_0162ac:
        move.w #0xc382,0x30(%a0)
m68k_0162ac_end:
.org 0x162B2
m68k_0162b2:
        move.w #0xc382,0x18(%a0)
m68k_0162b2_end:
.org 0x162B8
m68k_0162b8:
        move.w #0xc380,(%a0)+
m68k_0162b8_end:
.org 0x162BC
m68k_0162bc:
        move.w #0x5,%d0
m68k_0162bc_end:
.org 0x162C0
m68k_0162c0:
        move.w #0xc00d,%d1
m68k_0162c0_end:
.org 0x162C4
m68k_0162c4:
        bsr.w (. + 56)
m68k_0162c4_end:
.org 0x162C8
m68k_0162c8:
        move.w #0x1,%d0
m68k_0162c8_end:
.org 0x162CC
m68k_0162cc:
        move.w #0xc049,%d1
m68k_0162cc_end:
.org 0x162D0
m68k_0162d0:
        bsr.w (. + 44)
m68k_0162d0_end:
.org 0x162D4
m68k_0162d4:
        move.w #0xdb80,0x48(%a0)
m68k_0162d4_end:
.org 0x162DA
m68k_0162da:
        move.w #0xcb82,0x30(%a0)
m68k_0162da_end:
.org 0x162E0
m68k_0162e0:
        move.w #0xcb82,0x18(%a0)
m68k_0162e0_end:
.org 0x162E6
m68k_0162e6:
        move.w #0xcb80,(%a0)+
m68k_0162e6_end:
.org 0x162EA
m68k_0162ea:
        clr.w 0x48(%a0)
m68k_0162ea_end:
.org 0x162EE
m68k_0162ee:
        ori.w #0x9800,0xf3a4:w
m68k_0162ee_end:
.org 0x162F4
m68k_0162f4:
        addi.w #0x60,0xf31a:w
m68k_0162f4_end:
.org 0x162FA
m68k_0162fa:
        rts
m68k_0162fa_end:
.org 0x162FC
m68k_0162fc:
        move.w #0xc381,(%a0)
m68k_0162fc_end:
.org 0x16300
m68k_016300:
        move.w %d1,0x18(%a0)
m68k_016300_end:
.org 0x16304
m68k_016304:
        addq.w #0x1,%d1
m68k_016304_end:
.org 0x16306
m68k_016306:
        move.w %d1,0x30(%a0)
m68k_016306_end:
.org 0x1630A
m68k_01630a:
        addq.w #0x1,%d1
m68k_01630a_end:
.org 0x1630C
m68k_01630c:
        move.w #0xd381,0x48(%a0)
m68k_01630c_end:
.org 0x16312
m68k_016312:
        addq.w #0x2,%a0
m68k_016312_end:
.org 0x16314
m68k_016314:
        dbra %d0,(. + -24)
m68k_016314_end:
.org 0x16318
m68k_016318:
        rts
m68k_016318_end:
.org 0x1631A
m68k_01631a:
        bsr.w (. + 82)
m68k_01631a_end:
.org 0x1631E
m68k_01631e:
        lea.l 0xff3000:l,%a0
m68k_01631e_end:
.org 0x16324
m68k_016324:
        clr.w 0xff39b2:l
m68k_016324_end:
.org 0x1632A
m68k_01632a:
        tst.b (%a0)+
m68k_01632a_end:
.org 0x1632C
m68k_01632c:
        bmi.b (. + 56)
m68k_01632c_end:
.org 0x1632E
m68k_01632e:
        move.b (%a0)+,%d0
m68k_01632e_end:
.org 0x16330
m68k_016330:
        move.b (%a0)+,%d1
m68k_016330_end:
.org 0x16332
m68k_016332:
        lea.l 0xff39b2:l,%a1
m68k_016332_end:
.org 0x16338
m68k_016338:
        cmp.b (%a1),%d1
m68k_016338_end:
.org 0x1633A
m68k_01633a:
        bhi.b (. + 6)
m68k_01633a_end:
.org 0x1633C
m68k_01633c:
        addq.w #0x2,%a1
m68k_01633c_end:
.org 0x1633E
m68k_01633e:
        bra.b (. + -6)
m68k_01633e_end:
.org 0x16340
m68k_016340:
        lea.l (%a1),%a2
m68k_016340_end:
.org 0x16342
m68k_016342:
        addq.w #0x2,%a2
m68k_016342_end:
.org 0x16344
m68k_016344:
        tst.b (%a2)
m68k_016344_end:
.org 0x16346
m68k_016346:
        bne.b (. + -4)
m68k_016346_end:
.org 0x16348
m68k_016348:
        clr.b 0x2(%a2)
m68k_016348_end:
.org 0x1634C
m68k_01634c:
        lea.l 0x2(%a2),%a3
m68k_01634c_end:
.org 0x16350
m68k_016350:
        move.b -(%a2),-(%a3)
m68k_016350_end:
.org 0x16352
m68k_016352:
        move.b -(%a2),-(%a3)
m68k_016352_end:
.org 0x16354
m68k_016354:
        cmpa.l %a2,%a1
m68k_016354_end:
.org 0x16356
m68k_016356:
        bcs.b (. + -6)
m68k_016356_end:
.org 0x16358
m68k_016358:
        move.b %d1,(%a1)
m68k_016358_end:
.org 0x1635A
m68k_01635a:
        move.b %d0,0x1(%a1)
m68k_01635a_end:
.org 0x1635E
m68k_01635e:
        tst.b (%a0)+
m68k_01635e_end:
.org 0x16360
m68k_016360:
        bne.b (. + -2)
m68k_016360_end:
.org 0x16362
m68k_016362:
        bra.b (. + -56)
m68k_016362_end:
.org 0x16364
m68k_016364:
        clr.w 0xff3bb2:l
m68k_016364_end:
.org 0x1636A
m68k_01636a:
        rts
m68k_01636a_end:
.org 0x1636C
m68k_01636c:
        lea.l 0xff3000:l,%a0
m68k_01636c_end:
.org 0x16372
m68k_016372:
        adda.w 0xff3826:l,%a0
m68k_016372_end:
.org 0x16378
m68k_016378:
        lea.l 0xea38:w,%a1
m68k_016378_end:
.org 0x1637C
m68k_01637c:
        lea.l 0xe640:w,%a3
m68k_01637c_end:
.org 0x16380
m68k_016380:
        move.w #0x27,%d0
m68k_016380_end:
.org 0x16384
m68k_016384:
        tst.b (%a1, %d0.w)
m68k_016384_end:
.org 0x16388
m68k_016388:
        beq.w (. + 82)
m68k_016388_end:
.org 0x1638C
m68k_01638c:
        lea.l 0xff3000:l,%a2
m68k_01638c_end:
.org 0x16392
m68k_016392:
        move.w %d0,%d2
m68k_016392_end:
.org 0x16394
m68k_016394:
        addq.w #0x1,%d2
m68k_016394_end:
.org 0x16396
m68k_016396:
        move.b (%a2)+,%d1
m68k_016396_end:
.org 0x16398
m68k_016398:
        bmi.w (. + 34)
m68k_016398_end:
.org 0x1639C
m68k_01639c:
        move.b (%a2)+,%d1
m68k_01639c_end:
.org 0x1639E
m68k_01639e:
        move.b (%a2)+,%d1
m68k_01639e_end:
.org 0x163A0
m68k_0163a0:
        move.b (%a2)+,%d1
m68k_0163a0_end:
.org 0x163A2
m68k_0163a2:
        cmpi.b #0x80,%d1
m68k_0163a2_end:
.org 0x163A6
m68k_0163a6:
        bne.w (. + 14)
m68k_0163a6_end:
.org 0x163AA
m68k_0163aa:
        cmp.b (%a2)+,%d2
m68k_0163aa_end:
.org 0x163AC
m68k_0163ac:
        bne.w (. + 8)
m68k_0163ac_end:
.org 0x163B0
m68k_0163b0:
        bra.w (. + 42)
m68k_0163b0_end:
.org 0x163B4
m68k_0163b4:
        tst.b (%a2)+
m68k_0163b4_end:
.org 0x163B6
m68k_0163b6:
        bne.b (. + -2)
m68k_0163b6_end:
.org 0x163B8
m68k_0163b8:
        bra.b (. + -34)
m68k_0163b8_end:
.org 0x163BA
m68k_0163ba:
        clr.b (%a0)+
m68k_0163ba_end:
.org 0x163BC
m68k_0163bc:
        move.w %d0,%d1
m68k_0163bc_end:
.org 0x163BE
m68k_0163be:
        lsl.w #0x1,%d1
m68k_0163be_end:
.org 0x163C0
m68k_0163c0:
        move.b 0x1(%a3, %d1.w),(%a0)+
m68k_0163c0_end:
.org 0x163C4
m68k_0163c4:
        move.b #0x1,(%a0)+
m68k_0163c4_end:
.org 0x163C8
m68k_0163c8:
        move.b #0x80,(%a0)+
m68k_0163c8_end:
.org 0x163CC
m68k_0163cc:
        move.b %d2,(%a0)+
m68k_0163cc_end:
.org 0x163CE
m68k_0163ce:
        clr.b (%a0)+
m68k_0163ce_end:
.org 0x163D0
m68k_0163d0:
        move.b #0xff,(%a0)
m68k_0163d0_end:
.org 0x163D4
m68k_0163d4:
        addq.w #0x6,0xff3826:l
m68k_0163d4_end:
.org 0x163DA
m68k_0163da:
        dbra %d0,(. + -86)
m68k_0163da_end:
.org 0x163DE
m68k_0163de:
        rts
m68k_0163de_end:
.org 0x165D8
m68k_0165d8:
        move.w #0x1,%d0
m68k_0165d8_end:
.org 0x165DC
m68k_0165dc:
        move.w #0x3,%d1
m68k_0165dc_end:
.org 0x165E0
m68k_0165e0:
        lea.l 0xd300:w,%a1
m68k_0165e0_end:
.org 0x165E4
m68k_0165e4:
        movea.l 0xff382c:l,%a0
m68k_0165e4_end:
.org 0x165EA
m68k_0165ea:
        clr.w %d4
m68k_0165ea_end:
.org 0x165EC
m68k_0165ec:
        move.b 0x4(%a0),%d4
m68k_0165ec_end:
.org 0x165F0
m68k_0165f0:
        lsl.w #0x1,%d4
m68k_0165f0_end:
.org 0x165F2
m68k_0165f2:
        lea.l 0xe640:w,%a0
m68k_0165f2_end:
.org 0x165F6
m68k_0165f6:
        move.w (%a0, %d4.w),%d4
m68k_0165f6_end:
.org 0x165FA
m68k_0165fa:
        move.w %d4,%d5
m68k_0165fa_end:
.org 0x165FC
m68k_0165fc:
        lsl.w #0x1,%d4
m68k_0165fc_end:
.org 0x165FE
m68k_0165fe:
        add.w %d5,%d4
m68k_0165fe_end:
.org 0x16600
m68k_016600:
        lsl.w #0x1,%d4
m68k_016600_end:
.org 0x16602
m68k_016602:
        lea.l 0x8a504:l,%a0
m68k_016602_end:
.org 0x16608
m68k_016608:
        adda.w %d4,%a0
m68k_016608_end:
.org 0x1660A
m68k_01660a:
        move.w #0x2,%d3
m68k_01660a_end:
.org 0x1660E
m68k_01660e:
        jsr 0xae8a:l
m68k_01660e_end:
.org 0x16614
m68k_016614:
        move.l #0x41a00000,0xc00004:l
m68k_016614_end:
.org 0x1661E
m68k_01661e:
        lea.l 0xd300:w,%a1
m68k_01661e_end:
.org 0x16622
m68k_016622:
        move.w #0x5f,%d3
m68k_016622_end:
.org 0x16626
m68k_016626:
        move.l (%a1)+,0xc00000:l
m68k_016626_end:
.org 0x1662C
m68k_01662c:
        dbra %d3,(. + -6)
m68k_01662c_end:
.org 0x16630
m68k_016630:
        lea.l 44(%pc),%a0
m68k_016630_end:
.org 0x16634
m68k_016634:
        lea.l 0xd300:w,%a1
m68k_016634_end:
.org 0x16638
m68k_016638:
        clr.w %d3
m68k_016638_end:
.org 0x1663A
m68k_01663a:
        jsr 0xae8a:l
m68k_01663a_end:
.org 0x16640
m68k_016640:
        move.l #0x49200000,0xc00004:l
m68k_016640_end:
.org 0x1664A
m68k_01664a:
        lea.l 0xd300:w,%a1
m68k_01664a_end:
.org 0x1664E
m68k_01664e:
        move.w #0x1f,%d3
m68k_01664e_end:
.org 0x16652
m68k_016652:
        move.l (%a1)+,0xc00000:l
m68k_016652_end:
.org 0x16658
m68k_016658:
        dbra %d3,(. + -6)
m68k_016658_end:
.org 0x1665C
m68k_01665c:
        rts
m68k_01665c_end:
.org 0x16A50
m68k_016a50:
        adda.w #0x10,%a0
m68k_016a50_end:
.org 0x16A5E
m68k_016a5e:
        move.w #0x800,%d2
m68k_016a5e_end:
.org 0x177BE
m68k_0177be:
        move.l #0x40200002,0xc00004:l
m68k_0177be_end:
.org 0x177C8
m68k_0177c8:
        move.w #0x1f,%d0
m68k_0177c8_end:
.org 0x177CC
m68k_0177cc:
        move.l #0x11111111,0xc00000:l
m68k_0177cc_end:
.org 0x177D6
m68k_0177d6:
        dbra %d0,(. + -10)
m68k_0177d6_end:
.org 0x177DA
m68k_0177da:
        lea.l 0x6bf58:l,%a0
m68k_0177da_end:
.org 0x177E0
m68k_0177e0:
        lea.l 0xd300:w,%a1
m68k_0177e0_end:
.org 0x177E4
m68k_0177e4:
        move.w #0x1,%d0
m68k_0177e4_end:
.org 0x177E8
m68k_0177e8:
        move.w #0x3,%d1
m68k_0177e8_end:
.org 0x177EC
m68k_0177ec:
        move.w #0xa,%d3
m68k_0177ec_end:
.org 0x177F0
m68k_0177f0:
        jsr 0xae8a:l
m68k_0177f0_end:
.org 0x177F6
m68k_0177f6:
        lea.l 0xd300:w,%a1
m68k_0177f6_end:
.org 0x177FA
m68k_0177fa:
        move.w #0x15f,%d3
m68k_0177fa_end:
.org 0x177FE
m68k_0177fe:
        move.l (%a1)+,0xc00000:l
m68k_0177fe_end:
.org 0x17804
m68k_017804:
        dbra %d3,(. + -6)
m68k_017804_end:
.org 0x17808
m68k_017808:
        move.l #0x48000002,0xc00004:l
m68k_017808_end:
.org 0x17812
m68k_017812:
        move.w 0xf68a:w,%d3
m68k_017812_end:
.org 0x17816
m68k_017816:
        lsl.w #0x2,%d3
m68k_017816_end:
.org 0x17818
m68k_017818:
        lea.l 0x8a212:l,%a0
m68k_017818_end:
.org 0x1781E
m68k_01781e:
        adda.w %d3,%a0
m68k_01781e_end:
.org 0x17820
m68k_017820:
        lea.l 0xd300:w,%a1
m68k_017820_end:
.org 0x17824
m68k_017824:
        move.w #0x1,%d3
m68k_017824_end:
.org 0x17828
m68k_017828:
        jsr 0xae8a:l
m68k_017828_end:
.org 0x1782E
m68k_01782e:
        lea.l 0xd300:w,%a1
m68k_01782e_end:
.org 0x17832
m68k_017832:
        move.w #0x3f,%d3
m68k_017832_end:
.org 0x17836
m68k_017836:
        move.l (%a1)+,0xc00000:l
m68k_017836_end:
.org 0x1783C
m68k_01783c:
        dbra %d3,(. + -6)
m68k_01783c_end:
.org 0x17840
m68k_017840:
        move.w 0xf68e:w,%d4
m68k_017840_end:
.org 0x17844
m68k_017844:
        lsl.w #0x1,%d4
m68k_017844_end:
.org 0x17846
m68k_017846:
        lea.l 0xe640:w,%a2
m68k_017846_end:
.org 0x1784A
m68k_01784a:
        move.w (%a2, %d4.w),%d4
m68k_01784a_end:
.org 0x1784E
m68k_01784e:
        move.w %d4,%d5
m68k_01784e_end:
.org 0x17850
m68k_017850:
        lsl.w #0x1,%d4
m68k_017850_end:
.org 0x17852
m68k_017852:
        add.w %d5,%d4
m68k_017852_end:
.org 0x17854
m68k_017854:
        lsl.w #0x1,%d4
m68k_017854_end:
.org 0x17856
m68k_017856:
        lea.l 0x8a504:l,%a0
m68k_017856_end:
.org 0x1785C
m68k_01785c:
        adda.w %d4,%a0
m68k_01785c_end:
.org 0x1785E
m68k_01785e:
        lea.l 0xd300:w,%a1
m68k_01785e_end:
.org 0x17862
m68k_017862:
        bsr.w (. + 372)
m68k_017862_end:
.org 0x17866
m68k_017866:
        move.w 0xf68c:w,%d4
m68k_017866_end:
.org 0x1786A
m68k_01786a:
        lsl.w #0x1,%d4
m68k_01786a_end:
.org 0x1786C
m68k_01786c:
        lea.l 0xe640:w,%a2
m68k_01786c_end:
.org 0x17870
m68k_017870:
        move.w (%a2, %d4.w),%d4
m68k_017870_end:
.org 0x17874
m68k_017874:
        move.w %d4,%d5
m68k_017874_end:
.org 0x17876
m68k_017876:
        lsl.w #0x1,%d4
m68k_017876_end:
.org 0x17878
m68k_017878:
        add.w %d5,%d4
m68k_017878_end:
.org 0x1787A
m68k_01787a:
        lsl.w #0x1,%d4
m68k_01787a_end:
.org 0x1787C
m68k_01787c:
        lea.l 0x8a504:l,%a0
m68k_01787c_end:
.org 0x17882
m68k_017882:
        adda.w %d4,%a0
m68k_017882_end:
.org 0x17884
m68k_017884:
        bsr.w (. + 338)
m68k_017884_end:
.org 0x17888
m68k_017888:
        lea.l 0xd300:w,%a1
m68k_017888_end:
.org 0x1788C
m68k_01788c:
        move.w #0xbf,%d3
m68k_01788c_end:
.org 0x17890
m68k_017890:
        move.l (%a1)+,0xc00000:l
m68k_017890_end:
.org 0x17896
m68k_017896:
        dbra %d3,(. + -6)
m68k_017896_end:
.org 0x1789A
m68k_01789a:
        lea.l 0x8a426:l,%a0
m68k_01789a_end:
.org 0x178A0
m68k_0178a0:
        lea.l 0xd300:w,%a1
m68k_0178a0_end:
.org 0x178A4
m68k_0178a4:
        move.w #0x3,%d0
m68k_0178a4_end:
.org 0x178A8
m68k_0178a8:
        move.w #0x1,%d1
m68k_0178a8_end:
.org 0x178AC
m68k_0178ac:
        move.w #0x9,%d3
m68k_0178ac_end:
.org 0x178B0
m68k_0178b0:
        jsr 0xaf1e:l
m68k_0178b0_end:
.org 0x178B6
m68k_0178b6:
        lea.l 0xd300:w,%a1
m68k_0178b6_end:
.org 0x178BA
m68k_0178ba:
        move.w #0x4f,%d3
m68k_0178ba_end:
.org 0x178BE
m68k_0178be:
        move.l (%a1)+,0xc00000:l
m68k_0178be_end:
.org 0x178C4
m68k_0178c4:
        dbra %d3,(. + -6)
m68k_0178c4_end:
.org 0x178C8
m68k_0178c8:
        lea.l 0x6c174:l,%a1
m68k_0178c8_end:
.org 0x178CE
m68k_0178ce:
        move.w #0xf,%d3
m68k_0178ce_end:
.org 0x178D2
m68k_0178d2:
        move.l (%a1)+,0xc00000:l
m68k_0178d2_end:
.org 0x178D8
m68k_0178d8:
        dbra %d3,(. + -6)
m68k_0178d8_end:
.org 0x178DC
m68k_0178dc:
        move.l #0x70000001,0xc00004:l
m68k_0178dc_end:
.org 0x178E6
m68k_0178e6:
        lea.l 0x6bf6e:l,%a1
m68k_0178e6_end:
.org 0x178EC
m68k_0178ec:
        move.w #0x2f,%d3
m68k_0178ec_end:
.org 0x178F0
m68k_0178f0:
        move.l (%a1)+,0xc00000:l
m68k_0178f0_end:
.org 0x178F6
m68k_0178f6:
        dbra %d3,(. + -6)
m68k_0178f6_end:
.org 0x178FA
m68k_0178fa:
        lea.l 0x8a426:l,%a0
m68k_0178fa_end:
.org 0x17900
m68k_017900:
        lea.l 0xd300:w,%a1
m68k_017900_end:
.org 0x17904
m68k_017904:
        move.w #0x1,%d0
m68k_017904_end:
.org 0x17908
m68k_017908:
        move.w #0x3,%d1
m68k_017908_end:
.org 0x1790C
m68k_01790c:
        move.w #0x9,%d3
m68k_01790c_end:
.org 0x17910
m68k_017910:
        jsr 0xaf1e:l
m68k_017910_end:
.org 0x17916
m68k_017916:
        move.l #0x70c00001,0xc00004:l
m68k_017916_end:
.org 0x17920
m68k_017920:
        lea.l 0xd300:w,%a1
m68k_017920_end:
.org 0x17924
m68k_017924:
        move.w #0x4f,%d2
m68k_017924_end:
.org 0x17928
m68k_017928:
        move.l (%a1)+,0xc00000:l
m68k_017928_end:
.org 0x1792E
m68k_01792e:
        dbra %d2,(. + -6)
m68k_01792e_end:
.org 0x17932
m68k_017932:
        move.l #0x60000002,0xc00004:l
m68k_017932_end:
.org 0x1793C
m68k_01793c:
        lea.l 0xaba1e:l,%a1
m68k_01793c_end:
.org 0x17942
m68k_017942:
        move.w #0x17,%d0
m68k_017942_end:
.org 0x17946
m68k_017946:
        move.l (%a1)+,0xc00000:l
m68k_017946_end:
.org 0x1794C
m68k_01794c:
        dbra %d0,(. + -6)
m68k_01794c_end:
.org 0x17950
m68k_017950:
        move.l #0x5a000002,0xc00004:l
m68k_017950_end:
.org 0x1795A
m68k_01795a:
        lea.l 0x6c02e:l,%a1
m68k_01795a_end:
.org 0x17960
m68k_017960:
        move.w #0x1f,%d1
m68k_017960_end:
.org 0x17964
m68k_017964:
        move.l (%a1)+,0xc00000:l
m68k_017964_end:
.org 0x1796A
m68k_01796a:
        dbra %d1,(. + -6)
m68k_01796a_end:
.org 0x1796E
m68k_01796e:
        lea.l 0x6c0e8:l,%a1
m68k_01796e_end:
.org 0x17974
m68k_017974:
        move.w #0x1f,%d1
m68k_017974_end:
.org 0x17978
m68k_017978:
        move.l (%a1)+,0xc00000:l
m68k_017978_end:
.org 0x1797E
m68k_01797e:
        dbra %d1,(. + -6)
m68k_01797e_end:
.org 0x17982
m68k_017982:
        bsr.w (. + 6)
m68k_017982_end:
.org 0x17986
m68k_017986:
        rts
m68k_017986_end:
.org 0x17988
m68k_017988:
        lea.l 0xc800:w,%a0
m68k_017988_end:
.org 0x1798C
m68k_01798c:
        lea.l 0xa550:w,%a1
m68k_01798c_end:
.org 0x17990
m68k_017990:
        bsr.w (. + 46)
m68k_017990_end:
.org 0x17994
m68k_017994:
        move.l %d0,0xf6ae:w
m68k_017994_end:
.org 0x17998
m68k_017998:
        move.w %d1,0xf6a6:w
m68k_017998_end:
.org 0x1799C
m68k_01799c:
        lea.l 0xa5a4:w,%a1
m68k_01799c_end:
.org 0x179A0
m68k_0179a0:
        bsr.w (. + 30)
m68k_0179a0_end:
.org 0x179A4
m68k_0179a4:
        move.l %d0,0xf6b2:w
m68k_0179a4_end:
.org 0x179A8
m68k_0179a8:
        move.w %d1,0xf6a8:w
m68k_0179a8_end:
.org 0x179AC
m68k_0179ac:
        move.w 0xf68a:w,%d0
m68k_0179ac_end:
.org 0x179B0
m68k_0179b0:
        lsl.w #0x2,%d0
m68k_0179b0_end:
.org 0x179B2
m68k_0179b2:
        lea.l 0xe59c:w,%a0
m68k_0179b2_end:
.org 0x179B6
m68k_0179b6:
        move.w 0x2(%a0, %d0.w),0xf6be:w
m68k_0179b6_end:
.org 0x179BC
m68k_0179bc:
        rts
m68k_0179bc_end:
.org 0x179BE
m68k_0179be:
        moveq #0,%d0
m68k_0179be_end:
.org 0x179C0
m68k_0179c0:
        clr.w %d1
m68k_0179c0_end:
.org 0x179C2
m68k_0179c2:
        move.w (%a1)+,%d2
m68k_0179c2_end:
.org 0x179C4
m68k_0179c4:
        bmi.b (. + 16)
m68k_0179c4_end:
.org 0x179C6
m68k_0179c6:
        andi.w #0xff,%d2
m68k_0179c6_end:
.org 0x179CA
m68k_0179ca:
        addq.w #0x1,%d1
m68k_0179ca_end:
.org 0x179CC
m68k_0179cc:
        lsl.w #0x2,%d2
m68k_0179cc_end:
.org 0x179CE
m68k_0179ce:
        add.l (%a0, %d2.w),%d0
m68k_0179ce_end:
.org 0x179D2
m68k_0179d2:
        bra.b (. + -16)
m68k_0179d2_end:
.org 0x179D4
m68k_0179d4:
        rts
m68k_0179d4_end:
.org 0x179D6
m68k_0179d6:
        cmpi.w #0x3f,0x4(%a0)
m68k_0179d6_end:
.org 0x179DC
m68k_0179dc:
        beq.w (. + 18)
m68k_0179dc_end:
.org 0x179E0
m68k_0179e0:
        move.w #0x2,%d3
m68k_0179e0_end:
.org 0x179E4
m68k_0179e4:
        jsr 0xae8a:l
m68k_0179e4_end:
.org 0x179EA
m68k_0179ea:
        bra.w (. + 42)
m68k_0179ea_end:
.org 0x179EE
m68k_0179ee:
        move.w #0xf,%d3
m68k_0179ee_end:
.org 0x179F2
m68k_0179f2:
        move.l #0x11111111,(%a1)+
m68k_0179f2_end:
.org 0x179F8
m68k_0179f8:
        dbra %d3,(. + -6)
m68k_0179f8_end:
.org 0x179FC
m68k_0179fc:
        move.w #0x1,%d3
m68k_0179fc_end:
.org 0x17A00
m68k_017a00:
        jsr 0xae8a:l
m68k_017a00_end:
.org 0x17A06
m68k_017a06:
        move.w #0xf,%d3
m68k_017a06_end:
.org 0x17A0A
m68k_017a0a:
        move.l #0x11111111,(%a1)+
m68k_017a0a_end:
.org 0x17A10
m68k_017a10:
        dbra %d3,(. + -6)
m68k_017a10_end:
.org 0x17A14
m68k_017a14:
        rts
m68k_017a14_end:
.org 0x189D4
m68k_0189d4:
        lsl.w #0x1,%d1
m68k_0189d4_end:
.org 0x189D6
m68k_0189d6:
        move.w (%a3, %d1.w),%d2
m68k_0189d6_end:
.org 0x189DA
m68k_0189da:
        ext.l %d2
m68k_0189da_end:
.org 0x189DC
m68k_0189dc:
        divu.w #0x28,%d2
m68k_0189dc_end:
.org 0x189E0
m68k_0189e0:
        lsr.w #0x1,%d1
m68k_0189e0_end:
.org 0x189E2
m68k_0189e2:
        move.w 0xf68a:w,%d3
m68k_0189e2_end:
.org 0x189E6
m68k_0189e6:
        lsl.w #0x1,%d3
m68k_0189e6_end:
.org 0x189E8
m68k_0189e8:
        lea.l 0xf45e:w,%a5
m68k_0189e8_end:
.org 0x189EC
m68k_0189ec:
        cmp.w (%a5, %d3.w),%d1
m68k_0189ec_end:
.org 0x189F0
m68k_0189f0:
        beq.w (. + 16)
m68k_0189f0_end:
.org 0x189F4
m68k_0189f4:
        lea.l 0xa026:w,%a5
m68k_0189f4_end:
.org 0x189F8
m68k_0189f8:
        cmp.w (%a5, %d3.w),%d1
m68k_0189f8_end:
.org 0x189FC
m68k_0189fc:
        bne.w (. + 8)
m68k_0189fc_end:
.org 0x18A00
m68k_018a00:
        addi.w #0x1e,%d2
m68k_018a00_end:
.org 0x18A04
m68k_018a04:
        lea.l 0xc700:w,%a5
m68k_018a04_end:
.org 0x18A08
m68k_018a08:
        btst.b #0x4,(%a5, %d1.w)
m68k_018a08_end:
.org 0x18A0E
m68k_018a0e:
        beq.w (. + 8)
m68k_018a0e_end:
.org 0x18A12
m68k_018a12:
        addi.w #0x14,%d2
m68k_018a12_end:
.org 0x18A16
m68k_018a16:
        move.w (%a3, %d0.w),%d3
m68k_018a16_end:
.org 0x18A1A
m68k_018a1a:
        add.w %d2,%d3
m68k_018a1a_end:
.org 0x18A1C
m68k_018a1c:
        cmpi.w #0x3e7,%d3
m68k_018a1c_end:
.org 0x18A20
m68k_018a20:
        bls.w (. + 8)
m68k_018a20_end:
.org 0x18A24
m68k_018a24:
        move.w #0x3e7,%d3
m68k_018a24_end:
.org 0x18A28
m68k_018a28:
        move.w %d3,(%a3, %d0.w)
m68k_018a28_end:
.org 0x18A2C
m68k_018a2c:
        rts
m68k_018a2c_end:
.org 0x18A2E
m68k_018a2e:
        andi.l #0xffff,%d2
m68k_018a2e_end:
.org 0x18A34
m68k_018a34:
        divu.w #0x64,%d2
m68k_018a34_end:
.org 0x18A38
m68k_018a38:
        move.w %d0,%d1
m68k_018a38_end:
.org 0x18A3A
m68k_018a3a:
        lsl.w #0x1,%d1
m68k_018a3a_end:
.org 0x18A3C
m68k_018a3c:
        move.w (%a3, %d1.w),%d3
m68k_018a3c_end:
.org 0x18A40
m68k_018a40:
        add.w %d2,%d3
m68k_018a40_end:
.org 0x18A42
m68k_018a42:
        cmpi.w #0x3e7,%d3
m68k_018a42_end:
.org 0x18A46
m68k_018a46:
        bls.w (. + 8)
m68k_018a46_end:
.org 0x18A4A
m68k_018a4a:
        move.w #0x3e7,%d3
m68k_018a4a_end:
.org 0x18A4E
m68k_018a4e:
        move.w %d3,(%a3, %d1.w)
m68k_018a4e_end:
.org 0x18A52
m68k_018a52:
        rts
m68k_018a52_end:
.org 0x18A54
m68k_018a54:
        movem.l %d2/%a0,-(%a7)
m68k_018a54_end:
.org 0x18A58
m68k_018a58:
        tst.w 0xefe0:w
m68k_018a58_end:
.org 0x18A5C
m68k_018a5c:
        beq.w (. + 50)
m68k_018a5c_end:
.org 0x18A60
m68k_018a60:
        lea.l 0xcc00:w,%a0
m68k_018a60_end:
.org 0x18A64
m68k_018a64:
        move.b #0xff,(%a0, %d1.w)
m68k_018a64_end:
.org 0x18A6A
m68k_018a6a:
        lea.l 0xa550:w,%a0
m68k_018a6a_end:
.org 0x18A6E
m68k_018a6e:
        cmp.w 0xf702:w,%d1
m68k_018a6e_end:
.org 0x18A72
m68k_018a72:
        beq.w (. + 8)
m68k_018a72_end:
.org 0x18A76
m68k_018a76:
        lea.l 0xa5a4:w,%a0
m68k_018a76_end:
.org 0x18A7A
m68k_018a7a:
        move.w (%a0)+,%d2
m68k_018a7a_end:
.org 0x18A7C
m68k_018a7c:
        bmi.w (. + 18)
m68k_018a7c_end:
.org 0x18A80
m68k_018a80:
        andi.w #0xff,%d2
m68k_018a80_end:
.org 0x18A84
m68k_018a84:
        cmp.w %d1,%d2
m68k_018a84_end:
.org 0x18A86
m68k_018a86:
        bne.b (. + -12)
m68k_018a86_end:
.org 0x18A88
m68k_018a88:
        move.w (%a0)+,-0x4(%a0)
m68k_018a88_end:
.org 0x18A8C
m68k_018a8c:
        bpl.b (. + -4)
m68k_018a8c_end:
.org 0x18A8E
m68k_018a8e:
        movem.l (%a7)+,%d2/%a0
m68k_018a8e_end:
.org 0x18A92
m68k_018a92:
        rts
m68k_018a92_end:
.org 0x18A94
m68k_018a94:
        tst.w 0xefe0:w
m68k_018a94_end:
.org 0x18A98
m68k_018a98:
        beq.w (. + 44)
m68k_018a98_end:
.org 0x18A9C
m68k_018a9c:
        cmpi.w #0x6,0xffff8114:l
m68k_018a9c_end:
.org 0x18AA4
m68k_018aa4:
        bcs.w (. + 32)
m68k_018aa4_end:
.org 0x18AA8
m68k_018aa8:
        bne.w (. + 18)
m68k_018aa8_end:
.org 0x18AAC
m68k_018aac:
        move.w 0xffff80e0:l,%d0
m68k_018aac_end:
.org 0x18AB2
m68k_018ab2:
        bsr.w (. + 20)
m68k_018ab2_end:
.org 0x18AB6
m68k_018ab6:
        bra.w (. + 14)
m68k_018ab6_end:
.org 0x18ABA
m68k_018aba:
        move.w 0xffff80e2:l,%d0
m68k_018aba_end:
.org 0x18AC0
m68k_018ac0:
        bsr.w (. + 6)
m68k_018ac0_end:
.org 0x18AC4
m68k_018ac4:
        rts
m68k_018ac4_end:
.org 0x18AC6
m68k_018ac6:
        lea.l 0xa5a4:w,%a0
m68k_018ac6_end:
.org 0x18ACA
m68k_018aca:
        lea.l 0xa57a:w,%a1
m68k_018aca_end:
.org 0x18ACE
m68k_018ace:
        cmp.w 0xf702:w,%d0
m68k_018ace_end:
.org 0x18AD2
m68k_018ad2:
        bne.w (. + 12)
m68k_018ad2_end:
.org 0x18AD6
m68k_018ad6:
        lea.l 0xa550:w,%a0
m68k_018ad6_end:
.org 0x18ADA
m68k_018ada:
        lea.l 0xa5ce:w,%a1
m68k_018ada_end:
.org 0x18ADE
m68k_018ade:
        move.w (%a0)+,%d1
m68k_018ade_end:
.org 0x18AE0
m68k_018ae0:
        bmi.w (. + 30)
m68k_018ae0_end:
.org 0x18AE4
m68k_018ae4:
        andi.w #0xff,%d1
m68k_018ae4_end:
.org 0x18AE8
m68k_018ae8:
        cmp.w %d0,%d1
m68k_018ae8_end:
.org 0x18AEA
m68k_018aea:
        bne.b (. + -12)
m68k_018aea_end:
.org 0x18AEC
m68k_018aec:
        move.w (%a0)+,-0x4(%a0)
m68k_018aec_end:
.org 0x18AF0
m68k_018af0:
        bpl.b (. + -4)
m68k_018af0_end:
.org 0x18AF2
m68k_018af2:
        tst.w (%a1)+
m68k_018af2_end:
.org 0x18AF4
m68k_018af4:
        bpl.b (. + -2)
m68k_018af4_end:
.org 0x18AF6
m68k_018af6:
        move.w %d0,-0x2(%a1)
m68k_018af6_end:
.org 0x18AFA
m68k_018afa:
        move.w #0xffff,(%a1)
m68k_018afa_end:
.org 0x18AFE
m68k_018afe:
        rts
m68k_018afe_end:
.org 0x18B94
m68k_018b94:
        movem.l %d0-%d1/%a0-%a1,-(%a7)
m68k_018b94_end:
.org 0x18B98
m68k_018b98:
        tst.w 0xefe0:w
m68k_018b98_end:
.org 0x18B9C
m68k_018b9c:
        beq.w (. + 148)
m68k_018b9c_end:
.org 0x18BA0
m68k_018ba0:
        cmpi.b #0x2,%d2
m68k_018ba0_end:
.org 0x18BA4
m68k_018ba4:
        beq.w (. + 80)
m68k_018ba4_end:
.org 0x18BA8
m68k_018ba8:
        cmpi.b #0x3,%d2
m68k_018ba8_end:
.org 0x18BAC
m68k_018bac:
        bne.w (. + 164)
m68k_018bac_end:
.org 0x18BB0
m68k_018bb0:
        lea.l 0xa5ce:w,%a0
m68k_018bb0_end:
.org 0x18BB4
m68k_018bb4:
        lea.l 0xa550:w,%a1
m68k_018bb4_end:
.org 0x18BB8
m68k_018bb8:
        move.w 0xf68a:w,%d3
m68k_018bb8_end:
.org 0x18BBC
m68k_018bbc:
        ori.w #0x80,%d3
m68k_018bbc_end:
.org 0x18BC0
m68k_018bc0:
        cmp.w 0xf702:w,%d0
m68k_018bc0_end:
.org 0x18BC4
m68k_018bc4:
        beq.w (. + 16)
m68k_018bc4_end:
.org 0x18BC8
m68k_018bc8:
        ori.w #0x40,%d3
m68k_018bc8_end:
.org 0x18BCC
m68k_018bcc:
        lea.l 0xa57a:w,%a0
m68k_018bcc_end:
.org 0x18BD0
m68k_018bd0:
        lea.l 0xa5a4:w,%a1
m68k_018bd0_end:
.org 0x18BD4
m68k_018bd4:
        tst.w (%a0)+
m68k_018bd4_end:
.org 0x18BD6
m68k_018bd6:
        bpl.b (. + -2)
m68k_018bd6_end:
.org 0x18BD8
m68k_018bd8:
        move.w %d0,-0x2(%a0)
m68k_018bd8_end:
.org 0x18BDC
m68k_018bdc:
        move.w #0xffff,(%a0)
m68k_018bdc_end:
.org 0x18BE0
m68k_018be0:
        move.w (%a1)+,%d3
m68k_018be0_end:
.org 0x18BE2
m68k_018be2:
        andi.w #0xff,%d3
m68k_018be2_end:
.org 0x18BE6
m68k_018be6:
        cmp.w %d0,%d3
m68k_018be6_end:
.org 0x18BE8
m68k_018be8:
        bne.b (. + -8)
m68k_018be8_end:
.org 0x18BEA
m68k_018bea:
        move.w (%a1)+,-0x4(%a1)
m68k_018bea_end:
.org 0x18BEE
m68k_018bee:
        bpl.b (. + -4)
m68k_018bee_end:
.org 0x18BF0
m68k_018bf0:
        bra.w (. + 96)
m68k_018bf0_end:
.org 0x18BF4
m68k_018bf4:
        cmp.w 0xf702:w,%d0
m68k_018bf4_end:
.org 0x18BF8
m68k_018bf8:
        bne.w (. + 16)
m68k_018bf8_end:
.org 0x18BFC
m68k_018bfc:
        lea.l 0xa550:w,%a0
m68k_018bfc_end:
.org 0x18C00
m68k_018c00:
        lea.l 0xa5ce:w,%a1
m68k_018c00_end:
.org 0x18C04
m68k_018c04:
        bra.w (. + 12)
m68k_018c04_end:
.org 0x18C08
m68k_018c08:
        lea.l 0xa5a4:w,%a0
m68k_018c08_end:
.org 0x18C0C
m68k_018c0c:
        lea.l 0xa57a:w,%a1
m68k_018c0c_end:
.org 0x18C10
m68k_018c10:
        move.w (%a0)+,%d1
m68k_018c10_end:
.org 0x18C12
m68k_018c12:
        andi.w #0xff,%d1
m68k_018c12_end:
.org 0x18C16
m68k_018c16:
        cmp.w %d0,%d1
m68k_018c16_end:
.org 0x18C18
m68k_018c18:
        bne.b (. + -8)
m68k_018c18_end:
.org 0x18C1A
m68k_018c1a:
        move.w (%a0)+,-0x4(%a0)
m68k_018c1a_end:
.org 0x18C1E
m68k_018c1e:
        bpl.b (. + -4)
m68k_018c1e_end:
.org 0x18C20
m68k_018c20:
        tst.w (%a1)+
m68k_018c20_end:
.org 0x18C22
m68k_018c22:
        bpl.b (. + -2)
m68k_018c22_end:
.org 0x18C24
m68k_018c24:
        move.w %d0,-0x2(%a1)
m68k_018c24_end:
.org 0x18C28
m68k_018c28:
        move.w #0xffff,(%a1)
m68k_018c28_end:
.org 0x18C2C
m68k_018c2c:
        bra.w (. + 36)
m68k_018c2c_end:
.org 0x18C30
m68k_018c30:
        cmpi.b #0x3,%d2
m68k_018c30_end:
.org 0x18C34
m68k_018c34:
        beq.w (. + 28)
m68k_018c34_end:
.org 0x18C38
m68k_018c38:
        move.w #0x6,%d1
m68k_018c38_end:
.org 0x18C3C
m68k_018c3c:
        cmp.w 0xffff80e0:l,%d0
m68k_018c3c_end:
.org 0x18C42
m68k_018c42:
        beq.w (. + 8)
m68k_018c42_end:
.org 0x18C46
m68k_018c46:
        move.w #0x7,%d1
m68k_018c46_end:
.org 0x18C4A
m68k_018c4a:
        move.w %d1,0xffff8114:l
m68k_018c4a_end:
.org 0x18C50
m68k_018c50:
        movem.l (%a7)+,%d0-%d1/%a0-%a1
m68k_018c50_end:
.org 0x18C54
m68k_018c54:
        rts
m68k_018c54_end:
.org 0x18C56
m68k_018c56:
        tst.w 0xefe0:w
m68k_018c56_end:
.org 0x18C5A
m68k_018c5a:
        beq.w (. + 44)
m68k_018c5a_end:
.org 0x18C5E
m68k_018c5e:
        tst.w 0xff706c:l
m68k_018c5e_end:
.org 0x18C64
m68k_018c64:
        bne.w (. + 14)
m68k_018c64_end:
.org 0x18C68
m68k_018c68:
        move.w 0xff706a:l,%d0
m68k_018c68_end:
.org 0x18C6E
m68k_018c6e:
        bsr.w (. + 26)
m68k_018c6e_end:
.org 0x18C72
m68k_018c72:
        tst.w 0xff70bc:l
m68k_018c72_end:
.org 0x18C78
m68k_018c78:
        bne.w (. + 14)
m68k_018c78_end:
.org 0x18C7C
m68k_018c7c:
        move.w 0xff70ba:l,%d0
m68k_018c7c_end:
.org 0x18C82
m68k_018c82:
        bsr.w (. + 6)
m68k_018c82_end:
.org 0x18C86
m68k_018c86:
        rts
m68k_018c86_end:
.org 0x18C88
m68k_018c88:
        lea.l 0xcc00:w,%a0
m68k_018c88_end:
.org 0x18C8C
m68k_018c8c:
        move.b #0xff,(%a0, %d0.w)
m68k_018c8c_end:
.org 0x18C92
m68k_018c92:
        lea.l 0xa550:w,%a1
m68k_018c92_end:
.org 0x18C96
m68k_018c96:
        cmp.w 0xf702:w,%d0
m68k_018c96_end:
.org 0x18C9A
m68k_018c9a:
        beq.w (. + 8)
m68k_018c9a_end:
.org 0x18C9E
m68k_018c9e:
        lea.l 0xa5a4:w,%a1
m68k_018c9e_end:
.org 0x18CA2
m68k_018ca2:
        move.w (%a1)+,%d1
m68k_018ca2_end:
.org 0x18CA4
m68k_018ca4:
        andi.w #0xff,%d1
m68k_018ca4_end:
.org 0x18CA8
m68k_018ca8:
        cmp.w %d0,%d1
m68k_018ca8_end:
.org 0x18CAA
m68k_018caa:
        bne.b (. + -8)
m68k_018caa_end:
.org 0x18CAC
m68k_018cac:
        move.w (%a1)+,-0x4(%a1)
m68k_018cac_end:
.org 0x18CB0
m68k_018cb0:
        bpl.b (. + -4)
m68k_018cb0_end:
.org 0x18CB2
m68k_018cb2:
        rts
m68k_018cb2_end:
.org 0x19076
m68k_019076:
        move.w 0xf67c:w,0xf68e:w
m68k_019076_end:
.org 0x1907C
m68k_01907c:
        jsr 0x679fc:l
m68k_01907c_end:
.org 0x19082
m68k_019082:
        rts
m68k_019082_end:
.org 0x1A16E
m68k_01a16e:
        cmpi.w #0x407,0xf612:w
m68k_01a16e_end:
.org 0x1A174
m68k_01a174:
        bne.w (. + 32)
m68k_01a174_end:
.org 0x1A178
m68k_01a178:
        tst.w 0xf362:w
m68k_01a178_end:
.org 0x1A17C
m68k_01a17c:
        beq.w (. + 94)
m68k_01a17c_end:
.org 0x1A180
m68k_01a180:
        cmpi.w #0x2,0xf362:w
m68k_01a180_end:
.org 0x1A186
m68k_01a186:
        beq.w (. + 84)
m68k_01a186_end:
.org 0x1A18A
m68k_01a18a:
        cmpi.w #0x4,0xf362:w
m68k_01a18a_end:
.org 0x1A190
m68k_01a190:
        beq.w (. + 74)
m68k_01a190_end:
.org 0x1A194
m68k_01a194:
        move.w 0xf68c:w,%d0
m68k_01a194_end:
.org 0x1A198
m68k_01a198:
        move.w 0xf68e:w,%d1
m68k_01a198_end:
.org 0x1A19C
m68k_01a19c:
        btst.b #0x1,0xf6d7:w
m68k_01a19c_end:
.org 0x1A1A2
m68k_01a1a2:
        beq.w (. + 6)
m68k_01a1a2_end:
.org 0x1A1A6
m68k_01a1a6:
        exg %d0,%d1
m68k_01a1a6_end:
.org 0x1A1A8
m68k_01a1a8:
        cmp.w 0xf67a:w,%d0
m68k_01a1a8_end:
.org 0x1A1AC
m68k_01a1ac:
        beq.w (. + 46)
m68k_01a1ac_end:
.org 0x1A1B0
m68k_01a1b0:
        cmp.w 0xf67c:w,%d0
m68k_01a1b0_end:
.org 0x1A1B4
m68k_01a1b4:
        beq.w (. + 32)
m68k_01a1b4_end:
.org 0x1A1B8
m68k_01a1b8:
        cmp.w 0xf67e:w,%d0
m68k_01a1b8_end:
.org 0x1A1BC
m68k_01a1bc:
        beq.w (. + 16)
m68k_01a1bc_end:
.org 0x1A1C0
m68k_01a1c0:
        cmp.w 0xf67a:w,%d1
m68k_01a1c0_end:
.org 0x1A1C4
m68k_01a1c4:
        beq.w (. + 22)
m68k_01a1c4_end:
.org 0x1A1C8
m68k_01a1c8:
        bra.w (. + 12)
m68k_01a1c8_end:
.org 0x1A1CC
m68k_01a1cc:
        cmp.w 0xf67c:w,%d1
m68k_01a1cc_end:
.org 0x1A1D0
m68k_01a1d0:
        beq.w (. + 10)
m68k_01a1d0_end:
.org 0x1A1D4
m68k_01a1d4:
        move.w 0xf604:w,0xf602:w
m68k_01a1d4_end:
.org 0x1A1DA
m68k_01a1da:
        rts
m68k_01a1da_end:
.org 0x1A200
m68k_01a200:
        cmpi.w #0x1,0xf6c4:w
m68k_01a200_end:
.org 0x1A206
m68k_01a206:
        bne.w (. + 60)
m68k_01a206_end:
.org 0x1A20A
m68k_01a20a:
        move.w 0xf68a:w,%d2
m68k_01a20a_end:
.org 0x1A20E
m68k_01a20e:
        lea.l 0x9fff:w,%a0
m68k_01a20e_end:
.org 0x1A212
m68k_01a212:
        clr.w %d1
m68k_01a212_end:
.org 0x1A214
m68k_01a214:
        move.b (%a0, %d2.w),%d1
m68k_01a214_end:
.org 0x1A218
m68k_01a218:
        beq.b (. + 42)
m68k_01a218_end:
.org 0x1A21A
m68k_01a21a:
        lsl.w #0x1,%d1
m68k_01a21a_end:
.org 0x1A21C
m68k_01a21c:
        lsl.w #0x5,%d2
m68k_01a21c_end:
.org 0x1A21E
m68k_01a21e:
        add.w %d1,%d2
m68k_01a21e_end:
.org 0x1A220
m68k_01a220:
        lea.l 0xabda8:l,%a1
m68k_01a220_end:
.org 0x1A226
m68k_01a226:
        clr.w %d0
m68k_01a226_end:
.org 0x1A228
m68k_01a228:
        move.b (%a1, %d2.w),%d0
m68k_01a228_end:
.org 0x1A22C
m68k_01a22c:
        lsl.w #0x3,%d0
m68k_01a22c_end:
.org 0x1A22E
m68k_01a22e:
        clr.w %d1
m68k_01a22e_end:
.org 0x1A230
m68k_01a230:
        move.b 0x1(%a1, %d2.w),%d1
m68k_01a230_end:
.org 0x1A234
m68k_01a234:
        lsl.w #0x3,%d1
m68k_01a234_end:
.org 0x1A236
m68k_01a236:
        clr.w %d2
m68k_01a236_end:
.org 0x1A238
m68k_01a238:
        lea.l 10(%pc),%a0
m68k_01a238_end:
.org 0x1A23C
m68k_01a23c:
        jsr 0xac08:l
m68k_01a23c_end:
.org 0x1A242
m68k_01a242:
        rts
m68k_01a242_end:
.org 0x1A25E
m68k_01a25e:
        moveq #0,%d0
m68k_01a25e_end:
.org 0x1A260
m68k_01a260:
        move.w 0xf6c8:w,%d0
m68k_01a260_end:
.org 0x1A264
m68k_01a264:
        addq.w #0x1,%d0
m68k_01a264_end:
.org 0x1A266
m68k_01a266:
        move.w #0xc460,%d1
m68k_01a266_end:
.org 0x1A26A
m68k_01a26a:
        move.w #0x8000,%d2
m68k_01a26a_end:
.org 0x1A26E
m68k_01a26e:
        lea.l 0xd300:w,%a6
m68k_01a26e_end:
.org 0x1A272
m68k_01a272:
        jsr 0x1270a:l
m68k_01a272_end:
.org 0x1A278
m68k_01a278:
        lea.l 0xd100:w,%a0
m68k_01a278_end:
.org 0x1A27C
m68k_01a27c:
        adda.w 0xf31a:w,%a0
m68k_01a27c_end:
.org 0x1A280
m68k_01a280:
        move.w #0x4,(%a0)+
m68k_01a280_end:
.org 0x1A284
m68k_01a284:
        move.w #0xc0c6,(%a0)+
m68k_01a284_end:
.org 0x1A288
m68k_01a288:
        cmpi.w #0x8000,0xd308:w
m68k_01a288_end:
.org 0x1A28E
m68k_01a28e:
        beq.w (. + 16)
m68k_01a28e_end:
.org 0x1A292
m68k_01a292:
        move.w #0xc46a,(%a0)+
m68k_01a292_end:
.org 0x1A296
m68k_01a296:
        move.w 0xd308:w,(%a0)+
m68k_01a296_end:
.org 0x1A29A
m68k_01a29a:
        bra.w (. + 12)
m68k_01a29a_end:
.org 0x1A29E
m68k_01a29e:
        move.w #0x8000,(%a0)+
m68k_01a29e_end:
.org 0x1A2A2
m68k_01a2a2:
        move.w #0xc46a,(%a0)+
m68k_01a2a2_end:
.org 0x1A2A6
m68k_01a2a6:
        move.w 0xd30a:w,(%a0)+
m68k_01a2a6_end:
.org 0x1A2AA
m68k_01a2aa:
        move.w #0xc46b,(%a0)+
m68k_01a2aa_end:
.org 0x1A2AE
m68k_01a2ae:
        clr.w (%a0)
m68k_01a2ae_end:
.org 0x1A2B0
m68k_01a2b0:
        addi.w #0xc,0xf31a:w
m68k_01a2b0_end:
.org 0x1A2B6
m68k_01a2b6:
        rts
m68k_01a2b6_end:
.org 0x1A2B8
m68k_01a2b8:
        lea.l 0xff3bc2:l,%a4
m68k_01a2b8_end:
.org 0x1A2BE
m68k_01a2be:
        lea.l 0xa550:w,%a1
m68k_01a2be_end:
.org 0x1A2C2
m68k_01a2c2:
        clr.w %d4
m68k_01a2c2_end:
.org 0x1A2C4
m68k_01a2c4:
        bsr.w (. + 18)
m68k_01a2c4_end:
.org 0x1A2C8
m68k_01a2c8:
        lea.l 0xa5a4:w,%a1
m68k_01a2c8_end:
.org 0x1A2CC
m68k_01a2cc:
        move.w #0x2,%d4
m68k_01a2cc_end:
.org 0x1A2D0
m68k_01a2d0:
        bsr.w (. + 6)
m68k_01a2d0_end:
.org 0x1A2D4
m68k_01a2d4:
        rts
m68k_01a2d4_end:
.org 0x1A2D6
m68k_01a2d6:
        move.w (%a1)+,%d3
m68k_01a2d6_end:
.org 0x1A2D8
m68k_01a2d8:
        bmi.w (. + 70)
m68k_01a2d8_end:
.org 0x1A2DC
m68k_01a2dc:
        andi.w #0xff,%d3
m68k_01a2dc_end:
.org 0x1A2E0
m68k_01a2e0:
        move.w %d3,%d5
m68k_01a2e0_end:
.org 0x1A2E2
m68k_01a2e2:
        lsl.w #0x2,%d3
m68k_01a2e2_end:
.org 0x1A2E4
m68k_01a2e4:
        lea.l 0xa150:w,%a2
m68k_01a2e4_end:
.org 0x1A2E8
m68k_01a2e8:
        move.w (%a2, %d3.w),%d0
m68k_01a2e8_end:
.org 0x1A2EC
m68k_01a2ec:
        beq.b (. + -22)
m68k_01a2ec_end:
.org 0x1A2EE
m68k_01a2ee:
        lsr.w #0x7,%d0
m68k_01a2ee_end:
.org 0x1A2F0
m68k_01a2f0:
        move.w 0x2(%a2, %d3.w),%d1
m68k_01a2f0_end:
.org 0x1A2F4
m68k_01a2f4:
        lsr.w #0x7,%d1
m68k_01a2f4_end:
.org 0x1A2F6
m68k_01a2f6:
        bsr.w (. + 214)
m68k_01a2f6_end:
.org 0x1A2FA
m68k_01a2fa:
        bcs.b (. + -36)
m68k_01a2fa_end:
.org 0x1A2FC
m68k_01a2fc:
        bsr.w (. + 182)
m68k_01a2fc_end:
.org 0x1A300
m68k_01a300:
        bcc.w (. + 12)
m68k_01a300_end:
.org 0x1A304
m68k_01a304:
        btst.b #0x3,0xf321:w
m68k_01a304_end:
.org 0x1A30A
m68k_01a30a:
        bne.b (. + -52)
m68k_01a30a_end:
.org 0x1A30C
m68k_01a30c:
        bsr.w (. + 20)
m68k_01a30c_end:
.org 0x1A310
m68k_01a310:
        lea.l 0xd400:w,%a0
m68k_01a310_end:
.org 0x1A314
m68k_01a314:
        clr.w %d2
m68k_01a314_end:
.org 0x1A316
m68k_01a316:
        jsr 0xac08:l
m68k_01a316_end:
.org 0x1A31C
m68k_01a31c:
        bra.b (. + -70)
m68k_01a31c_end:
.org 0x1A31E
m68k_01a31e:
        rts
m68k_01a31e_end:
.org 0x1A320
m68k_01a320:
        lea.l 136(%pc),%a2
m68k_01a320_end:
.org 0x1A324
m68k_01a324:
        nop
m68k_01a324_end:
.org 0x1A326
m68k_01a326:
        lea.l 0xd400:w,%a3
m68k_01a326_end:
.org 0x1A32A
m68k_01a32a:
        move.w #0xfff8,(%a3)+
m68k_01a32a_end:
.org 0x1A32E
m68k_01a32e:
        move.w (%a2, %d4.w),(%a3)+
m68k_01a32e_end:
.org 0x1A332
m68k_01a332:
        move.w #0x4ff8,(%a3)+
m68k_01a332_end:
.org 0x1A336
m68k_01a336:
        lea.l 0xc800:w,%a2
m68k_01a336_end:
.org 0x1A33A
m68k_01a33a:
        move.l (%a2, %d3.w),%d5
m68k_01a33a_end:
.org 0x1A33E
m68k_01a33e:
        cmpi.w #0x3e8,%d5
m68k_01a33e_end:
.org 0x1A342
m68k_01a342:
        bcs.b (. + 68)
m68k_01a342_end:
.org 0x1A344
m68k_01a344:
        clr.w %d6
m68k_01a344_end:
.org 0x1A346
m68k_01a346:
        subi.w #0x2710,%d5
m68k_01a346_end:
.org 0x1A34A
m68k_01a34a:
        bcs.w (. + 8)
m68k_01a34a_end:
.org 0x1A34E
m68k_01a34e:
        addq.w #0x1,%d6
m68k_01a34e_end:
.org 0x1A350
m68k_01a350:
        bra.b (. + -10)
m68k_01a350_end:
.org 0x1A352
m68k_01a352:
        addi.w #0x2710,%d5
m68k_01a352_end:
.org 0x1A356
m68k_01a356:
        tst.w %d6
m68k_01a356_end:
.org 0x1A358
m68k_01a358:
        bne.b (. + 10)
m68k_01a358_end:
.org 0x1A35A
m68k_01a35a:
        move.w #0x4401,%d6
m68k_01a35a_end:
.org 0x1A35E
m68k_01a35e:
        bra.w (. + 8)
m68k_01a35e_end:
.org 0x1A362
m68k_01a362:
        addi.w #0x4386,%d6
m68k_01a362_end:
.org 0x1A366
m68k_01a366:
        move.w #0x0,(%a3)+
m68k_01a366_end:
.org 0x1A36A
m68k_01a36a:
        move.w %d6,(%a3)+
m68k_01a36a_end:
.org 0x1A36C
m68k_01a36c:
        move.w #0xff8,(%a3)+
m68k_01a36c_end:
.org 0x1A370
m68k_01a370:
        divu.w #0x3e8,%d5
m68k_01a370_end:
.org 0x1A374
m68k_01a374:
        addi.w #0x4386,%d5
m68k_01a374_end:
.org 0x1A378
m68k_01a378:
        move.w #0x0,(%a3)+
m68k_01a378_end:
.org 0x1A37C
m68k_01a37c:
        move.w %d5,(%a3)+
m68k_01a37c_end:
.org 0x1A37E
m68k_01a37e:
        move.w #0x0,(%a3)+
m68k_01a37e_end:
.org 0x1A382
m68k_01a382:
        bra.w (. + 34)
m68k_01a382_end:
.org 0x1A386
m68k_01a386:
        move.w #0x0,(%a3)+
m68k_01a386_end:
.org 0x1A38A
m68k_01a38a:
        move.w #0x4385,(%a3)+
m68k_01a38a_end:
.org 0x1A38E
m68k_01a38e:
        move.w #0xff8,(%a3)+
m68k_01a38e_end:
.org 0x1A392
m68k_01a392:
        divu.w #0x64,%d5
m68k_01a392_end:
.org 0x1A396
m68k_01a396:
        addi.w #0x4386,%d5
m68k_01a396_end:
.org 0x1A39A
m68k_01a39a:
        move.w #0x0,(%a3)+
m68k_01a39a_end:
.org 0x1A39E
m68k_01a39e:
        move.w %d5,(%a3)+
m68k_01a39e_end:
.org 0x1A3A0
m68k_01a3a0:
        move.w #0x0,(%a3)+
m68k_01a3a0_end:
.org 0x1A3A4
m68k_01a3a4:
        move.w #0x8000,(%a3)
m68k_01a3a4_end:
.org 0x1A3A8
m68k_01a3a8:
        rts
m68k_01a3a8_end:
.org 0x1A3B2
m68k_01a3b2:
        lea.l 0xa5f8:w,%a3
m68k_01a3b2_end:
.org 0x1A3B6
m68k_01a3b6:
        move.w (%a3)+,%d6
m68k_01a3b6_end:
.org 0x1A3B8
m68k_01a3b8:
        bmi.b (. + 14)
m68k_01a3b8_end:
.org 0x1A3BA
m68k_01a3ba:
        cmp.w %d5,%d6
m68k_01a3ba_end:
.org 0x1A3BC
m68k_01a3bc:
        bne.b (. + -6)
m68k_01a3bc_end:
.org 0x1A3BE
m68k_01a3be:
        ori.w #0x1,%sr
m68k_01a3be_end:
.org 0x1A3C2
m68k_01a3c2:
        bra.w (. + 8)
m68k_01a3c2_end:
.org 0x1A3C6
m68k_01a3c6:
        andi.w #0xfffe,%sr
m68k_01a3c6_end:
.org 0x1A3CA
m68k_01a3ca:
        rts
m68k_01a3ca_end:
.org 0x1A3CC
m68k_01a3cc:
        tst.b (%a4, %d5.w)
m68k_01a3cc_end:
.org 0x1A3D0
m68k_01a3d0:
        beq.w (. + 30)
m68k_01a3d0_end:
.org 0x1A3D4
m68k_01a3d4:
        lea.l 0xa5f8:w,%a5
m68k_01a3d4_end:
.org 0x1A3D8
m68k_01a3d8:
        move.w (%a5)+,%d6
m68k_01a3d8_end:
.org 0x1A3DA
m68k_01a3da:
        bmi.w (. + 12)
m68k_01a3da_end:
.org 0x1A3DE
m68k_01a3de:
        cmp.w %d5,%d6
m68k_01a3de_end:
.org 0x1A3E0
m68k_01a3e0:
        bne.b (. + -8)
m68k_01a3e0_end:
.org 0x1A3E2
m68k_01a3e2:
        bra.w (. + 12)
m68k_01a3e2_end:
.org 0x1A3E6
m68k_01a3e6:
        ori.w #0x1,%sr
m68k_01a3e6_end:
.org 0x1A3EA
m68k_01a3ea:
        bra.w (. + 8)
m68k_01a3ea_end:
.org 0x1A3EE
m68k_01a3ee:
        andi.w #0xfffe,%sr
m68k_01a3ee_end:
.org 0x1A3F2
m68k_01a3f2:
        rts
m68k_01a3f2_end:
.org 0x1B0C2
m68k_01b0c2:
        btst.b #0x2,0xf3a5:w
m68k_01b0c2_end:
.org 0x1B0C8
m68k_01b0c8:
        beq.w (. + 32)
m68k_01b0c8_end:
.org 0x1B0CC
m68k_01b0cc:
        bsr.w (. + 56)
m68k_01b0cc_end:
.org 0x1B0D0
m68k_01b0d0:
        bsr.w (. + 104)
m68k_01b0d0_end:
.org 0x1B0D4
m68k_01b0d4:
        lea.l 20(%pc),%a0
m68k_01b0d4_end:
.org 0x1B0D8
m68k_01b0d8:
        move.w #0x30,%d0
m68k_01b0d8_end:
.org 0x1B0DC
m68k_01b0dc:
        move.w #0xe8,%d1
m68k_01b0dc_end:
.org 0x1B0E0
m68k_01b0e0:
        clr.w %d2
m68k_01b0e0_end:
.org 0x1B0E2
m68k_01b0e2:
        jsr 0xac08:l
m68k_01b0e2_end:
.org 0x1B0E8
m68k_01b0e8:
        rts
m68k_01b0e8_end:
.org 0x1B104
m68k_01b104:
        lea.l 34(%pc),%a0
m68k_01b104_end:
.org 0x1B108
m68k_01b108:
        move.w 0xf320:w,%d0
m68k_01b108_end:
.org 0x1B10C
m68k_01b10c:
        andi.w #0xf8,%d0
m68k_01b10c_end:
.org 0x1B110
m68k_01b110:
        bne.w (. + 6)
m68k_01b110_end:
.org 0x1B114
m68k_01b114:
        addq.w #0x8,%a0
m68k_01b114_end:
.org 0x1B116
m68k_01b116:
        move.w #0x48,%d0
m68k_01b116_end:
.org 0x1B11A
m68k_01b11a:
        move.w #0xf0,%d1
m68k_01b11a_end:
.org 0x1B11E
m68k_01b11e:
        clr.w %d2
m68k_01b11e_end:
.org 0x1B120
m68k_01b120:
        jsr 0xac08:l
m68k_01b120_end:
.org 0x1B126
m68k_01b126:
        rts
m68k_01b126_end:
.org 0x1B138
m68k_01b138:
        lea.l 82(%pc),%a0
m68k_01b138_end:
.org 0x1B13C
m68k_01b13c:
        tst.w 0xf778:w
m68k_01b13c_end:
.org 0x1B140
m68k_01b140:
        beq.w (. + 16)
m68k_01b140_end:
.org 0x1B144
m68k_01b144:
        btst.b #0x3,0xf321:w
m68k_01b144_end:
.org 0x1B14A
m68k_01b14a:
        beq.w (. + 6)
m68k_01b14a_end:
.org 0x1B14E
m68k_01b14e:
        addq.w #0x8,%a0
m68k_01b14e_end:
.org 0x1B150
m68k_01b150:
        move.w #0x58,%d0
m68k_01b150_end:
.org 0x1B154
m68k_01b154:
        move.w #0xf8,%d1
m68k_01b154_end:
.org 0x1B158
m68k_01b158:
        clr.w %d2
m68k_01b158_end:
.org 0x1B15A
m68k_01b15a:
        jsr 0xac08:l
m68k_01b15a_end:
.org 0x1B160
m68k_01b160:
        tst.w 0xf778:w
m68k_01b160_end:
.org 0x1B164
m68k_01b164:
        beq.w (. + 22)
m68k_01b164_end:
.org 0x1B168
m68k_01b168:
        cmpi.w #0x403a,0xf77c:w
m68k_01b168_end:
.org 0x1B16E
m68k_01b16e:
        bne.w (. + 28)
m68k_01b16e_end:
.org 0x1B172
m68k_01b172:
        clr.w 0xf778:w
m68k_01b172_end:
.org 0x1B176
m68k_01b176:
        bra.w (. + 20)
m68k_01b176_end:
.org 0x1B17A
m68k_01b17a:
        cmpi.w #0x4039,0xf77c:w
m68k_01b17a_end:
.org 0x1B180
m68k_01b180:
        bne.w (. + 10)
m68k_01b180_end:
.org 0x1B184
m68k_01b184:
        move.w #0x1,0xf778:w
m68k_01b184_end:
.org 0x1B18A
m68k_01b18a:
        rts
m68k_01b18a_end:
.org 0x1D03C
m68k_01d03c:
        bsr.w (. + 348)
m68k_01d03c_end:
.org 0x1D040
m68k_01d040:
        movea.l 0xff382c:l,%a1
m68k_01d040_end:
.org 0x1D046
m68k_01d046:
        lea.l 0x9000:w,%a2
m68k_01d046_end:
.org 0x1D04A
m68k_01d04a:
        lea.l 0xefbe:w,%a3
m68k_01d04a_end:
.org 0x1D04E
m68k_01d04e:
        move.w 0xefc6:w,%d0
m68k_01d04e_end:
.org 0x1D052
m68k_01d052:
        adda.w (%a3, %d0.w),%a2
m68k_01d052_end:
.org 0x1D056
m68k_01d056:
        lea.l 0xb200:w,%a0
m68k_01d056_end:
.org 0x1D05A
m68k_01d05a:
        move.w 0xf702:w,%d0
m68k_01d05a_end:
.org 0x1D05E
m68k_01d05e:
        lsl.w #0x1,%d0
m68k_01d05e_end:
.org 0x1D060
m68k_01d060:
        tst.w (%a0, %d0.w)
m68k_01d060_end:
.org 0x1D064
m68k_01d064:
        bne.w (. + 18)
m68k_01d064_end:
.org 0x1D068
m68k_01d068:
        move.w 0xf702:w,%d0
m68k_01d068_end:
.org 0x1D06C
m68k_01d06c:
        bsr.w (. + 54)
m68k_01d06c_end:
.org 0x1D070
m68k_01d070:
        clr.l 0xff382c:l
m68k_01d070_end:
.org 0x1D076
m68k_01d076:
        exg %a1,%a2
m68k_01d076_end:
.org 0x1D078
m68k_01d078:
        lea.l 0xb200:w,%a0
m68k_01d078_end:
.org 0x1D07C
m68k_01d07c:
        move.w 0xf706:w,%d0
m68k_01d07c_end:
.org 0x1D080
m68k_01d080:
        lsl.w #0x1,%d0
m68k_01d080_end:
.org 0x1D082
m68k_01d082:
        tst.w (%a0, %d0.w)
m68k_01d082_end:
.org 0x1D086
m68k_01d086:
        bne.w (. + 18)
m68k_01d086_end:
.org 0x1D08A
m68k_01d08a:
        move.w 0xf706:w,%d0
m68k_01d08a_end:
.org 0x1D08E
m68k_01d08e:
        bsr.w (. + 20)
m68k_01d08e_end:
.org 0x1D092
m68k_01d092:
        move.l %a2,0xff382c:l
m68k_01d092_end:
.org 0x1D098
m68k_01d098:
        bsr.w (. + 804)
m68k_01d098_end:
.org 0x1D09C
m68k_01d09c:
        bsr.w (. + 1086)
m68k_01d09c_end:
.org 0x1D0A0
m68k_01d0a0:
        rts
m68k_01d0a0_end:
.org 0x1D0A2
m68k_01d0a2:
        movem.l %d1-%d4/%a0-%a2,-(%a7)
m68k_01d0a2_end:
.org 0x1D0A6
m68k_01d0a6:
        lea.l 0xcc00:w,%a0
m68k_01d0a6_end:
.org 0x1D0AA
m68k_01d0aa:
        move.b #0xff,(%a0, %d0.w)
m68k_01d0aa_end:
.org 0x1D0B0
m68k_01d0b0:
        clr.w %d3
m68k_01d0b0_end:
.org 0x1D0B2
m68k_01d0b2:
        move.b 0xd(%a1),%d3
m68k_01d0b2_end:
.org 0x1D0B6
m68k_01d0b6:
        lea.l (%a1),%a0
m68k_01d0b6_end:
.org 0x1D0B8
m68k_01d0b8:
        move.b (%a1),%d1
m68k_01d0b8_end:
.org 0x1D0BA
m68k_01d0ba:
        andi.w #0xf,%d1
m68k_01d0ba_end:
.org 0x1D0BE
m68k_01d0be:
        cmpi.w #0x1,%d1
m68k_01d0be_end:
.org 0x1D0C2
m68k_01d0c2:
        beq.w (. + 82)
m68k_01d0c2_end:
.org 0x1D0C6
m68k_01d0c6:
        subq.b #0x1,(%a1)
m68k_01d0c6_end:
.org 0x1D0C8
m68k_01d0c8:
        clr.w %d2
m68k_01d0c8_end:
.org 0x1D0CA
m68k_01d0ca:
        move.w #0x1,%d5
m68k_01d0ca_end:
.org 0x1D0CE
m68k_01d0ce:
        cmp.b 0xd(%a1, %d2.w),%d0
m68k_01d0ce_end:
.org 0x1D0D2
m68k_01d0d2:
        beq.w (. + 8)
m68k_01d0d2_end:
.org 0x1D0D6
m68k_01d0d6:
        addq.w #0x1,%d2
m68k_01d0d6_end:
.org 0x1D0D8
m68k_01d0d8:
        bra.b (. + -10)
m68k_01d0d8_end:
.org 0x1D0DA
m68k_01d0da:
        addq.w #0x1,%d2
m68k_01d0da_end:
.org 0x1D0DC
m68k_01d0dc:
        cmp.w %d2,%d1
m68k_01d0dc_end:
.org 0x1D0DE
m68k_01d0de:
        beq.w (. + 12)
m68k_01d0de_end:
.org 0x1D0E2
m68k_01d0e2:
        move.b 0xd(%a1, %d2.w),0xc(%a1, %d2.w)
m68k_01d0e2_end:
.org 0x1D0E8
m68k_01d0e8:
        bra.b (. + -14)
m68k_01d0e8_end:
.org 0x1D0EA
m68k_01d0ea:
        lea.l 0xd(%a1, %d1.w),%a2
m68k_01d0ea_end:
.org 0x1D0EE
m68k_01d0ee:
        lea.l 0xc(%a1, %d1.w),%a1
m68k_01d0ee_end:
.org 0x1D0F2
m68k_01d0f2:
        clr.w %d4
m68k_01d0f2_end:
.org 0x1D0F4
m68k_01d0f4:
        move.b 0xd(%a0),%d4
m68k_01d0f4_end:
.org 0x1D0F8
m68k_01d0f8:
        move.b (%a2),%d1
m68k_01d0f8_end:
.org 0x1D0FA
m68k_01d0fa:
        andi.w #0xf,%d1
m68k_01d0fa_end:
.org 0x1D0FE
m68k_01d0fe:
        beq.w (. + 16)
m68k_01d0fe_end:
.org 0x1D102
m68k_01d102:
        addi.w #0xc,%d1
m68k_01d102_end:
.org 0x1D106
m68k_01d106:
        move.b (%a2)+,(%a1)+
m68k_01d106_end:
.org 0x1D108
m68k_01d108:
        dbra %d1,(. + -2)
m68k_01d108_end:
.org 0x1D10C
m68k_01d10c:
        bra.b (. + -20)
m68k_01d10c_end:
.org 0x1D10E
m68k_01d10e:
        clr.b (%a1)
m68k_01d10e_end:
.org 0x1D110
m68k_01d110:
        bra.w (. + 18)
m68k_01d110_end:
.org 0x1D114
m68k_01d114:
        move.w #0xffff,%d4
m68k_01d114_end:
.org 0x1D118
m68k_01d118:
        move.w #0xe,%d5
m68k_01d118_end:
.org 0x1D11C
m68k_01d11c:
        lea.l 0xd(%a1, %d1.w),%a2
m68k_01d11c_end:
.org 0x1D120
m68k_01d120:
        bra.b (. + -40)
m68k_01d120_end:
.org 0x1D122
m68k_01d122:
        bsr.w (. + 32)
m68k_01d122_end:
.org 0x1D126
m68k_01d126:
        movem.l (%a7)+,%d1-%d4/%a0-%a2
m68k_01d126_end:
.org 0x1D12A
m68k_01d12a:
        exg %d1,%a1
m68k_01d12a_end:
.org 0x1D12C
m68k_01d12c:
        exg %d2,%a2
m68k_01d12c_end:
.org 0x1D12E
m68k_01d12e:
        cmp.l %d1,%d2
m68k_01d12e_end:
.org 0x1D130
m68k_01d130:
        bcs.w (. + 12)
m68k_01d130_end:
.org 0x1D134
m68k_01d134:
        andi.l #0xffff,%d5
m68k_01d134_end:
.org 0x1D13A
m68k_01d13a:
        sub.l %d5,%d2
m68k_01d13a_end:
.org 0x1D13C
m68k_01d13c:
        exg %d1,%a1
m68k_01d13c_end:
.org 0x1D13E
m68k_01d13e:
        exg %d2,%a2
m68k_01d13e_end:
.org 0x1D140
m68k_01d140:
        rts
m68k_01d140_end:
.org 0x1D142
m68k_01d142:
        cmp.w %d3,%d4
m68k_01d142_end:
.org 0x1D144
m68k_01d144:
        beq.w (. + 82)
m68k_01d144_end:
.org 0x1D148
m68k_01d148:
        lea.l 0xff39b2:l,%a0
m68k_01d148_end:
.org 0x1D14E
m68k_01d14e:
        adda.w 0xff3bb2:l,%a0
m68k_01d14e_end:
.org 0x1D154
m68k_01d154:
        tst.b (%a0)+
m68k_01d154_end:
.org 0x1D156
m68k_01d156:
        beq.w (. + 64)
m68k_01d156_end:
.org 0x1D15A
m68k_01d15a:
        cmp.b (%a0)+,%d3
m68k_01d15a_end:
.org 0x1D15C
m68k_01d15c:
        bne.b (. + -8)
m68k_01d15c_end:
.org 0x1D15E
m68k_01d15e:
        tst.w %d4
m68k_01d15e_end:
.org 0x1D160
m68k_01d160:
        bmi.w (. + 40)
m68k_01d160_end:
.org 0x1D164
m68k_01d164:
        move.b %d4,-0x1(%a0)
m68k_01d164_end:
.org 0x1D168
m68k_01d168:
        lea.l 0xff3000:l,%a0
m68k_01d168_end:
.org 0x1D16E
m68k_01d16e:
        tst.b (%a0)+
m68k_01d16e_end:
.org 0x1D170
m68k_01d170:
        bmi.w (. + 38)
m68k_01d170_end:
.org 0x1D174
m68k_01d174:
        cmp.b (%a0)+,%d3
m68k_01d174_end:
.org 0x1D176
m68k_01d176:
        beq.w (. + 10)
m68k_01d176_end:
.org 0x1D17A
m68k_01d17a:
        tst.b (%a0)+
m68k_01d17a_end:
.org 0x1D17C
m68k_01d17c:
        bne.b (. + -2)
m68k_01d17c_end:
.org 0x1D17E
m68k_01d17e:
        bra.b (. + -16)
m68k_01d17e_end:
.org 0x1D180
m68k_01d180:
        move.b %d4,-0x1(%a0)
m68k_01d180_end:
.org 0x1D184
m68k_01d184:
        bra.w (. + 18)
m68k_01d184_end:
.org 0x1D188
m68k_01d188:
        lea.l -0x2(%a0),%a1
m68k_01d188_end:
.org 0x1D18C
m68k_01d18c:
        move.b (%a0)+,(%a1)+
m68k_01d18c_end:
.org 0x1D18E
m68k_01d18e:
        beq.w (. + 8)
m68k_01d18e_end:
.org 0x1D192
m68k_01d192:
        move.b (%a0)+,(%a1)+
m68k_01d192_end:
.org 0x1D194
m68k_01d194:
        bra.b (. + -8)
m68k_01d194_end:
.org 0x1D196
m68k_01d196:
        rts
m68k_01d196_end:
.org 0x1D198
m68k_01d198:
        cmpi.w #0x6,0xffff8114:l
m68k_01d198_end:
.org 0x1D1A0
m68k_01d1a0:
        bcs.w (. + 104)
m68k_01d1a0_end:
.org 0x1D1A4
m68k_01d1a4:
        beq.w (. + 14)
m68k_01d1a4_end:
.org 0x1D1A8
m68k_01d1a8:
        move.w 0xffff80e2:l,%d0
m68k_01d1a8_end:
.org 0x1D1AE
m68k_01d1ae:
        bra.w (. + 10)
m68k_01d1ae_end:
.org 0x1D1B2
m68k_01d1b2:
        move.w 0xffff80e0:l,%d0
m68k_01d1b2_end:
.org 0x1D1B8
m68k_01d1b8:
        movea.l 0xff382c:l,%a0
m68k_01d1b8_end:
.org 0x1D1BE
m68k_01d1be:
        lea.l 0x9000:w,%a1
m68k_01d1be_end:
.org 0x1D1C2
m68k_01d1c2:
        lea.l 0xefbe:w,%a2
m68k_01d1c2_end:
.org 0x1D1C6
m68k_01d1c6:
        move.w 0xefc6:w,%d1
m68k_01d1c6_end:
.org 0x1D1CA
m68k_01d1ca:
        adda.w (%a2, %d1.w),%a1
m68k_01d1ca_end:
.org 0x1D1CE
m68k_01d1ce:
        cmp.w 0xf702:w,%d0
m68k_01d1ce_end:
.org 0x1D1D2
m68k_01d1d2:
        beq.w (. + 6)
m68k_01d1d2_end:
.org 0x1D1D6
m68k_01d1d6:
        exg %a0,%a1
m68k_01d1d6_end:
.org 0x1D1D8
m68k_01d1d8:
        move.w %d0,-(%a7)
m68k_01d1d8_end:
.org 0x1D1DA
m68k_01d1da:
        bsr.w (. + 48)
m68k_01d1da_end:
.org 0x1D1DE
m68k_01d1de:
        bsr.w (. + 314)
m68k_01d1de_end:
.org 0x1D1E2
m68k_01d1e2:
        move.w (%a7)+,%d0
m68k_01d1e2_end:
.org 0x1D1E4
m68k_01d1e4:
        cmp.w 0xf702:w,%d0
m68k_01d1e4_end:
.org 0x1D1E8
m68k_01d1e8:
        beq.w (. + 6)
m68k_01d1e8_end:
.org 0x1D1EC
m68k_01d1ec:
        exg %a0,%a1
m68k_01d1ec_end:
.org 0x1D1EE
m68k_01d1ee:
        move.l %a0,0xff382c:l
m68k_01d1ee_end:
.org 0x1D1F4
m68k_01d1f4:
        exg %d1,%a1
m68k_01d1f4_end:
.org 0x1D1F6
m68k_01d1f6:
        subi.l #0xffff9000,%d1
m68k_01d1f6_end:
.org 0x1D1FC
m68k_01d1fc:
        lea.l 0xefbe:w,%a2
m68k_01d1fc_end:
.org 0x1D200
m68k_01d200:
        move.w 0xefc6:w,%d0
m68k_01d200_end:
.org 0x1D204
m68k_01d204:
        move.w %d1,(%a2, %d0.w)
m68k_01d204_end:
.org 0x1D208
m68k_01d208:
        rts
m68k_01d208_end:
.org 0x1D20A
m68k_01d20a:
        move.w %d3,-(%a7)
m68k_01d20a_end:
.org 0x1D20C
m68k_01d20c:
        movem.l %d1-%d2/%a0-%a2,-(%a7)
m68k_01d20c_end:
.org 0x1D210
m68k_01d210:
        move.b (%a0),%d1
m68k_01d210_end:
.org 0x1D212
m68k_01d212:
        andi.w #0xf,%d1
m68k_01d212_end:
.org 0x1D216
m68k_01d216:
        cmpi.w #0x1,%d1
m68k_01d216_end:
.org 0x1D21A
m68k_01d21a:
        beq.w (. + 58)
m68k_01d21a_end:
.org 0x1D21E
m68k_01d21e:
        move.w #0x1,%d3
m68k_01d21e_end:
.org 0x1D222
m68k_01d222:
        clr.w %d2
m68k_01d222_end:
.org 0x1D224
m68k_01d224:
        cmp.b 0xd(%a0, %d2.w),%d0
m68k_01d224_end:
.org 0x1D228
m68k_01d228:
        beq.w (. + 8)
m68k_01d228_end:
.org 0x1D22C
m68k_01d22c:
        addq.w #0x1,%d2
m68k_01d22c_end:
.org 0x1D22E
m68k_01d22e:
        bra.b (. + -10)
m68k_01d22e_end:
.org 0x1D230
m68k_01d230:
        addq.w #0x1,%d2
m68k_01d230_end:
.org 0x1D232
m68k_01d232:
        cmp.w %d1,%d2
m68k_01d232_end:
.org 0x1D234
m68k_01d234:
        beq.w (. + 14)
m68k_01d234_end:
.org 0x1D238
m68k_01d238:
        move.b 0xd(%a0, %d2.w),0xc(%a0, %d2.w)
m68k_01d238_end:
.org 0x1D23E
m68k_01d23e:
        addq.w #0x1,%d2
m68k_01d23e_end:
.org 0x1D240
m68k_01d240:
        bra.b (. + -14)
m68k_01d240_end:
.org 0x1D242
m68k_01d242:
        bsr.w (. + 92)
m68k_01d242_end:
.org 0x1D246
m68k_01d246:
        subq.b #0x1,(%a0)
m68k_01d246_end:
.org 0x1D248
m68k_01d248:
        lea.l 0xd(%a0, %d1.w),%a1
m68k_01d248_end:
.org 0x1D24C
m68k_01d24c:
        lea.l 0xc(%a0, %d1.w),%a2
m68k_01d24c_end:
.org 0x1D250
m68k_01d250:
        bra.w (. + 24)
m68k_01d250_end:
.org 0x1D254
m68k_01d254:
        move.w #0xe,%d3
m68k_01d254_end:
.org 0x1D258
m68k_01d258:
        bsr.w (. + 144)
m68k_01d258_end:
.org 0x1D25C
m68k_01d25c:
        lea.l 0xd(%a0, %d1.w),%a1
m68k_01d25c_end:
.org 0x1D260
m68k_01d260:
        movea.l %a0,%a2
m68k_01d260_end:
.org 0x1D262
m68k_01d262:
        movea.l #0x0,%a0
m68k_01d262_end:
.org 0x1D268
m68k_01d268:
        move.b (%a1),%d1
m68k_01d268_end:
.org 0x1D26A
m68k_01d26a:
        andi.w #0xf,%d1
m68k_01d26a_end:
.org 0x1D26E
m68k_01d26e:
        beq.w (. + 16)
m68k_01d26e_end:
.org 0x1D272
m68k_01d272:
        addi.w #0xc,%d1
m68k_01d272_end:
.org 0x1D276
m68k_01d276:
        move.b (%a1)+,(%a2)+
m68k_01d276_end:
.org 0x1D278
m68k_01d278:
        dbra %d1,(. + -2)
m68k_01d278_end:
.org 0x1D27C
m68k_01d27c:
        bra.b (. + -20)
m68k_01d27c_end:
.org 0x1D27E
m68k_01d27e:
        clr.b (%a2)
m68k_01d27e_end:
.org 0x1D280
m68k_01d280:
        movem.l (%a7)+,%d1-%d2/%a0-%a2
m68k_01d280_end:
.org 0x1D284
m68k_01d284:
        exg %d0,%a0
m68k_01d284_end:
.org 0x1D286
m68k_01d286:
        exg %d1,%a1
m68k_01d286_end:
.org 0x1D288
m68k_01d288:
        cmp.l %d0,%d1
m68k_01d288_end:
.org 0x1D28A
m68k_01d28a:
        bcs.w (. + 12)
m68k_01d28a_end:
.org 0x1D28E
m68k_01d28e:
        andi.l #0xffff,%d3
m68k_01d28e_end:
.org 0x1D294
m68k_01d294:
        sub.l %d3,%d1
m68k_01d294_end:
.org 0x1D296
m68k_01d296:
        exg %d0,%a0
m68k_01d296_end:
.org 0x1D298
m68k_01d298:
        exg %d1,%a1
m68k_01d298_end:
.org 0x1D29A
m68k_01d29a:
        move.w (%a7)+,%d3
m68k_01d29a_end:
.org 0x1D29C
m68k_01d29c:
        rts
m68k_01d29c_end:
.org 0x1D29E
m68k_01d29e:
        move.w %d1,-(%a7)
m68k_01d29e_end:
.org 0x1D2A0
m68k_01d2a0:
        move.b 0xd(%a0),%d1
m68k_01d2a0_end:
.org 0x1D2A4
m68k_01d2a4:
        andi.w #0xff,%d1
m68k_01d2a4_end:
.org 0x1D2A8
m68k_01d2a8:
        lea.l 0xff39b2:l,%a1
m68k_01d2a8_end:
.org 0x1D2AE
m68k_01d2ae:
        adda.w 0xff3bb2:l,%a1
m68k_01d2ae_end:
.org 0x1D2B4
m68k_01d2b4:
        tst.b (%a1)
m68k_01d2b4_end:
.org 0x1D2B6
m68k_01d2b6:
        beq.w (. + 46)
m68k_01d2b6_end:
.org 0x1D2BA
m68k_01d2ba:
        cmp.b 0x1(%a1),%d0
m68k_01d2ba_end:
.org 0x1D2BE
m68k_01d2be:
        beq.w (. + 8)
m68k_01d2be_end:
.org 0x1D2C2
m68k_01d2c2:
        addq.w #0x2,%a1
m68k_01d2c2_end:
.org 0x1D2C4
m68k_01d2c4:
        bra.b (. + -16)
m68k_01d2c4_end:
.org 0x1D2C6
m68k_01d2c6:
        move.b %d1,0x1(%a1)
m68k_01d2c6_end:
.org 0x1D2CA
m68k_01d2ca:
        lea.l 0xff3000:l,%a1
m68k_01d2ca_end:
.org 0x1D2D0
m68k_01d2d0:
        cmp.b 0x1(%a1),%d0
m68k_01d2d0_end:
.org 0x1D2D4
m68k_01d2d4:
        beq.w (. + 12)
m68k_01d2d4_end:
.org 0x1D2D8
m68k_01d2d8:
        addq.w #0x1,%a1
m68k_01d2d8_end:
.org 0x1D2DA
m68k_01d2da:
        tst.b (%a1)+
m68k_01d2da_end:
.org 0x1D2DC
m68k_01d2dc:
        bne.b (. + -2)
m68k_01d2dc_end:
.org 0x1D2DE
m68k_01d2de:
        bra.b (. + -14)
m68k_01d2de_end:
.org 0x1D2E0
m68k_01d2e0:
        move.b %d1,0x1(%a1)
m68k_01d2e0_end:
.org 0x1D2E4
m68k_01d2e4:
        move.w (%a7)+,%d1
m68k_01d2e4_end:
.org 0x1D2E6
m68k_01d2e6:
        rts
m68k_01d2e6_end:
.org 0x1D2E8
m68k_01d2e8:
        lea.l 0xff39b2:l,%a1
m68k_01d2e8_end:
.org 0x1D2EE
m68k_01d2ee:
        adda.w 0xff3bb2:l,%a1
m68k_01d2ee_end:
.org 0x1D2F4
m68k_01d2f4:
        tst.b (%a1)
m68k_01d2f4_end:
.org 0x1D2F6
m68k_01d2f6:
        beq.w (. + 32)
m68k_01d2f6_end:
.org 0x1D2FA
m68k_01d2fa:
        cmp.b 0x1(%a1),%d0
m68k_01d2fa_end:
.org 0x1D2FE
m68k_01d2fe:
        beq.w (. + 10)
m68k_01d2fe_end:
.org 0x1D302
m68k_01d302:
        adda.w #0x2,%a1
m68k_01d302_end:
.org 0x1D306
m68k_01d306:
        bra.b (. + -18)
m68k_01d306_end:
.org 0x1D308
m68k_01d308:
        lea.l 0x2(%a1),%a2
m68k_01d308_end:
.org 0x1D30C
m68k_01d30c:
        move.b (%a2)+,(%a1)+
m68k_01d30c_end:
.org 0x1D30E
m68k_01d30e:
        beq.w (. + 8)
m68k_01d30e_end:
.org 0x1D312
m68k_01d312:
        move.b (%a2)+,(%a1)+
m68k_01d312_end:
.org 0x1D314
m68k_01d314:
        bra.b (. + -8)
m68k_01d314_end:
.org 0x1D316
m68k_01d316:
        rts
m68k_01d316_end:
.org 0x1D318
m68k_01d318:
        move.l %a2,-(%a7)
m68k_01d318_end:
.org 0x1D31A
m68k_01d31a:
        move.b (%a1),%d1
m68k_01d31a_end:
.org 0x1D31C
m68k_01d31c:
        andi.w #0xf,%d1
m68k_01d31c_end:
.org 0x1D320
m68k_01d320:
        cmpi.w #0xa,%d1
m68k_01d320_end:
.org 0x1D324
m68k_01d324:
        beq.w (. + 80)
m68k_01d324_end:
.org 0x1D328
m68k_01d328:
        lea.l 0xd(%a1, %d1.w),%a2
m68k_01d328_end:
.org 0x1D32C
m68k_01d32c:
        lea.l 0xe(%a1, %d1.w),%a3
m68k_01d32c_end:
.org 0x1D330
m68k_01d330:
        move.b (%a2),%d1
m68k_01d330_end:
.org 0x1D332
m68k_01d332:
        move.b %d1,%d2
m68k_01d332_end:
.org 0x1D334
m68k_01d334:
        andi.w #0xf,%d2
m68k_01d334_end:
.org 0x1D338
m68k_01d338:
        beq.w (. + 20)
m68k_01d338_end:
.org 0x1D33C
m68k_01d33c:
        addi.w #0xc,%d2
m68k_01d33c_end:
.org 0x1D340
m68k_01d340:
        move.b (%a3),%d3
m68k_01d340_end:
.org 0x1D342
m68k_01d342:
        move.b %d1,(%a3)+
m68k_01d342_end:
.org 0x1D344
m68k_01d344:
        move.b %d3,%d1
m68k_01d344_end:
.org 0x1D346
m68k_01d346:
        dbra %d2,(. + -6)
m68k_01d346_end:
.org 0x1D34A
m68k_01d34a:
        bra.b (. + -24)
m68k_01d34a_end:
.org 0x1D34C
m68k_01d34c:
        clr.b (%a3)
m68k_01d34c_end:
.org 0x1D34E
m68k_01d34e:
        move.b (%a1),%d1
m68k_01d34e_end:
.org 0x1D350
m68k_01d350:
        andi.w #0xf,%d1
m68k_01d350_end:
.org 0x1D354
m68k_01d354:
        addq.b #0x1,(%a1)
m68k_01d354_end:
.org 0x1D356
m68k_01d356:
        move.b %d0,0xd(%a1, %d1.w)
m68k_01d356_end:
.org 0x1D35A
m68k_01d35a:
        lea.l 0xcc00:w,%a2
m68k_01d35a_end:
.org 0x1D35E
m68k_01d35e:
        clr.w %d3
m68k_01d35e_end:
.org 0x1D360
m68k_01d360:
        move.b 0x4(%a1),%d3
m68k_01d360_end:
.org 0x1D364
m68k_01d364:
        addi.w #0x29,%d3
m68k_01d364_end:
.org 0x1D368
m68k_01d368:
        move.b %d3,(%a2, %d0.w)
m68k_01d368_end:
.org 0x1D36C
m68k_01d36c:
        move.w #0x1,%d3
m68k_01d36c_end:
.org 0x1D370
m68k_01d370:
        bra.w (. + 50)
m68k_01d370_end:
.org 0x1D374
m68k_01d374:
        clr.w %d3
m68k_01d374_end:
.org 0x1D376
m68k_01d376:
        lea.l 0xcc00:w,%a2
m68k_01d376_end:
.org 0x1D37A
m68k_01d37a:
        move.b (%a2, %d0.w),%d1
m68k_01d37a_end:
.org 0x1D37E
m68k_01d37e:
        andi.w #0x3f,%d1
m68k_01d37e_end:
.org 0x1D382
m68k_01d382:
        cmpi.w #0x28,%d1
m68k_01d382_end:
.org 0x1D386
m68k_01d386:
        bhi.w (. + 16)
m68k_01d386_end:
.org 0x1D38A
m68k_01d38a:
        bset.l #0x7,%d1
m68k_01d38a_end:
.org 0x1D38E
m68k_01d38e:
        move.b %d1,(%a2, %d1.w)
m68k_01d38e_end:
.org 0x1D392
m68k_01d392:
        bra.w (. + 16)
m68k_01d392_end:
.org 0x1D396
m68k_01d396:
        subi.w #0x28,%d1
m68k_01d396_end:
.org 0x1D39A
m68k_01d39a:
        bset.l #0x7,%d1
m68k_01d39a_end:
.org 0x1D39E
m68k_01d39e:
        move.b %d1,(%a2, %d0.w)
m68k_01d39e_end:
.org 0x1D3A2
m68k_01d3a2:
        exg %d0,%a0
m68k_01d3a2_end:
.org 0x1D3A4
m68k_01d3a4:
        exg %d1,%a1
m68k_01d3a4_end:
.org 0x1D3A6
m68k_01d3a6:
        cmp.l %d1,%d0
m68k_01d3a6_end:
.org 0x1D3A8
m68k_01d3a8:
        bcs.w (. + 12)
m68k_01d3a8_end:
.org 0x1D3AC
m68k_01d3ac:
        andi.l #0xffff,%d3
m68k_01d3ac_end:
.org 0x1D3B2
m68k_01d3b2:
        add.l %d3,%d0
m68k_01d3b2_end:
.org 0x1D3B4
m68k_01d3b4:
        exg %d0,%a0
m68k_01d3b4_end:
.org 0x1D3B6
m68k_01d3b6:
        exg %d1,%a1
m68k_01d3b6_end:
.org 0x1D3B8
m68k_01d3b8:
        movea.l (%a7)+,%a2
m68k_01d3b8_end:
.org 0x1D3BA
m68k_01d3ba:
        rts
m68k_01d3ba_end:
.org 0x1D3BC
m68k_01d3bc:
        tst.l 0xff382c:l
m68k_01d3bc_end:
.org 0x1D3C2
m68k_01d3c2:
        beq.w (. + 72)
m68k_01d3c2_end:
.org 0x1D3C6
m68k_01d3c6:
        movea.l 0xff382c:l,%a0
m68k_01d3c6_end:
.org 0x1D3CC
m68k_01d3cc:
        clr.w %d0
m68k_01d3cc_end:
.org 0x1D3CE
m68k_01d3ce:
        move.b 0x1(%a0),%d0
m68k_01d3ce_end:
.org 0x1D3D2
m68k_01d3d2:
        clr.w %d1
m68k_01d3d2_end:
.org 0x1D3D4
m68k_01d3d4:
        move.b 0x2(%a0),%d1
m68k_01d3d4_end:
.org 0x1D3D8
m68k_01d3d8:
        jsr 0x142a2:l
m68k_01d3d8_end:
.org 0x1D3DE
m68k_01d3de:
        tst.b %d3
m68k_01d3de_end:
.org 0x1D3E0
m68k_01d3e0:
        bpl.w (. + 42)
m68k_01d3e0_end:
.org 0x1D3E4
m68k_01d3e4:
        bsr.w (. + 40)
m68k_01d3e4_end:
.org 0x1D3E8
m68k_01d3e8:
        move.b (%a0),%d0
m68k_01d3e8_end:
.org 0x1D3EA
m68k_01d3ea:
        andi.w #0xf,%d0
m68k_01d3ea_end:
.org 0x1D3EE
m68k_01d3ee:
        subq.w #0x1,%d0
m68k_01d3ee_end:
.org 0x1D3F0
m68k_01d3f0:
        lea.l 0xcc00:w,%a1
m68k_01d3f0_end:
.org 0x1D3F4
m68k_01d3f4:
        clr.w %d1
m68k_01d3f4_end:
.org 0x1D3F6
m68k_01d3f6:
        move.b 0xd(%a0, %d0.w),%d1
m68k_01d3f6_end:
.org 0x1D3FA
m68k_01d3fa:
        move.b %d3,(%a1, %d1.w)
m68k_01d3fa_end:
.org 0x1D3FE
m68k_01d3fe:
        dbra %d0,(. + -10)
m68k_01d3fe_end:
.org 0x1D402
m68k_01d402:
        bsr.w (. + 74)
m68k_01d402_end:
.org 0x1D406
m68k_01d406:
        bsr.w (. + 178)
m68k_01d406_end:
.org 0x1D40A
m68k_01d40a:
        rts
m68k_01d40a_end:
.org 0x1D40C
m68k_01d40c:
        clr.w %d0
m68k_01d40c_end:
.org 0x1D40E
m68k_01d40e:
        move.b 0x1(%a0),%d0
m68k_01d40e_end:
.org 0x1D412
m68k_01d412:
        lsl.w #0x4,%d0
m68k_01d412_end:
.org 0x1D414
m68k_01d414:
        addq.w #0x8,%d0
m68k_01d414_end:
.org 0x1D416
m68k_01d416:
        clr.w %d1
m68k_01d416_end:
.org 0x1D418
m68k_01d418:
        move.b 0x2(%a0),%d1
m68k_01d418_end:
.org 0x1D41C
m68k_01d41c:
        lsl.w #0x4,%d1
m68k_01d41c_end:
.org 0x1D41E
m68k_01d41e:
        move.w %d1,%d2
m68k_01d41e_end:
.org 0x1D420
m68k_01d420:
        subi.w #0x10,%d2
m68k_01d420_end:
.org 0x1D424
m68k_01d424:
        lea.l 0xd4aca:l,%a1
m68k_01d424_end:
.org 0x1D42A
m68k_01d42a:
        move.w #0x1,%d3
m68k_01d42a_end:
.org 0x1D42E
m68k_01d42e:
        cmp.w 0x2(%a1),%d0
m68k_01d42e_end:
.org 0x1D432
m68k_01d432:
        bne.w (. + 18)
m68k_01d432_end:
.org 0x1D436
m68k_01d436:
        cmp.w (%a1),%d1
m68k_01d436_end:
.org 0x1D438
m68k_01d438:
        beq.w (. + 18)
m68k_01d438_end:
.org 0x1D43C
m68k_01d43c:
        cmp.w 0x2(%a1),%d2
m68k_01d43c_end:
.org 0x1D440
m68k_01d440:
        beq.w (. + 10)
m68k_01d440_end:
.org 0x1D444
m68k_01d444:
        addq.w #0x4,%a1
m68k_01d444_end:
.org 0x1D446
m68k_01d446:
        addq.w #0x1,%d3
m68k_01d446_end:
.org 0x1D448
m68k_01d448:
        bra.b (. + -26)
m68k_01d448_end:
.org 0x1D44A
m68k_01d44a:
        rts
m68k_01d44a_end:
.org 0x1D44C
m68k_01d44c:
        lsl.w #0x2,%d3
m68k_01d44c_end:
.org 0x1D44E
m68k_01d44e:
        move.b 0x5(%a0),%d0
m68k_01d44e_end:
.org 0x1D452
m68k_01d452:
        lsl.w #0x8,%d0
m68k_01d452_end:
.org 0x1D454
m68k_01d454:
        move.b 0x6(%a0),%d0
m68k_01d454_end:
.org 0x1D458
m68k_01d458:
        lsl.l #0x8,%d0
m68k_01d458_end:
.org 0x1D45A
m68k_01d45a:
        move.b 0x7(%a0),%d0
m68k_01d45a_end:
.org 0x1D45E
m68k_01d45e:
        lsl.l #0x8,%d0
m68k_01d45e_end:
.org 0x1D460
m68k_01d460:
        move.b 0x8(%a0),%d0
m68k_01d460_end:
.org 0x1D464
m68k_01d464:
        lea.l 0xdffc:w,%a1
m68k_01d464_end:
.org 0x1D468
m68k_01d468:
        move.l (%a1, %d3.w),%d1
m68k_01d468_end:
.org 0x1D46C
m68k_01d46c:
        add.l %d0,%d1
m68k_01d46c_end:
.org 0x1D46E
m68k_01d46e:
        cmpi.l #0xf423f,%d1
m68k_01d46e_end:
.org 0x1D474
m68k_01d474:
        bls.w (. + 10)
m68k_01d474_end:
.org 0x1D478
m68k_01d478:
        move.l #0xf423f,%d1
m68k_01d478_end:
.org 0x1D47E
m68k_01d47e:
        move.l %d1,(%a1, %d3.w)
m68k_01d47e_end:
.org 0x1D482
m68k_01d482:
        move.b 0x9(%a0),%d0
m68k_01d482_end:
.org 0x1D486
m68k_01d486:
        lsl.w #0x8,%d0
m68k_01d486_end:
.org 0x1D488
m68k_01d488:
        move.b 0xa(%a0),%d0
m68k_01d488_end:
.org 0x1D48C
m68k_01d48c:
        lsl.l #0x8,%d0
m68k_01d48c_end:
.org 0x1D48E
m68k_01d48e:
        move.b 0xb(%a0),%d0
m68k_01d48e_end:
.org 0x1D492
m68k_01d492:
        lsl.l #0x8,%d0
m68k_01d492_end:
.org 0x1D494
m68k_01d494:
        move.b 0xc(%a0),%d0
m68k_01d494_end:
.org 0x1D498
m68k_01d498:
        lea.l 0xe09c:w,%a1
m68k_01d498_end:
.org 0x1D49C
m68k_01d49c:
        move.l (%a1, %d3.w),%d1
m68k_01d49c_end:
.org 0x1D4A0
m68k_01d4a0:
        add.l %d0,%d1
m68k_01d4a0_end:
.org 0x1D4A2
m68k_01d4a2:
        cmpi.l #0xf423f,%d1
m68k_01d4a2_end:
.org 0x1D4A8
m68k_01d4a8:
        bls.w (. + 10)
m68k_01d4a8_end:
.org 0x1D4AC
m68k_01d4ac:
        move.l #0xf423f,%d1
m68k_01d4ac_end:
.org 0x1D4B2
m68k_01d4b2:
        move.l %d1,(%a1, %d3.w)
m68k_01d4b2_end:
.org 0x1D4B6
m68k_01d4b6:
        rts
m68k_01d4b6_end:
.org 0x1D4B8
m68k_01d4b8:
        move.b (%a0),%d0
m68k_01d4b8_end:
.org 0x1D4BA
m68k_01d4ba:
        andi.w #0xf,%d0
m68k_01d4ba_end:
.org 0x1D4BE
m68k_01d4be:
        lea.l 0xd(%a0, %d0.w),%a1
m68k_01d4be_end:
.org 0x1D4C2
m68k_01d4c2:
        move.b (%a1),%d0
m68k_01d4c2_end:
.org 0x1D4C4
m68k_01d4c4:
        andi.w #0xf,%d0
m68k_01d4c4_end:
.org 0x1D4C8
m68k_01d4c8:
        beq.w (. + 14)
m68k_01d4c8_end:
.org 0x1D4CC
m68k_01d4cc:
        addi.w #0xc,%d0
m68k_01d4cc_end:
.org 0x1D4D0
m68k_01d4d0:
        move.b (%a1)+,(%a0)+
m68k_01d4d0_end:
.org 0x1D4D2
m68k_01d4d2:
        dbra %d0,(. + -2)
m68k_01d4d2_end:
.org 0x1D4D6
m68k_01d4d6:
        clr.b (%a0)
m68k_01d4d6_end:
.org 0x1D4D8
m68k_01d4d8:
        rts
m68k_01d4d8_end:
.org 0x1D4DA
m68k_01d4da:
        jsr 0x83d4:l
m68k_01d4da_end:
.org 0x1D4E0
m68k_01d4e0:
        andi.l #0xffff,%d0
m68k_01d4e0_end:
.org 0x1D4E6
m68k_01d4e6:
        move.l %d0,%d1
m68k_01d4e6_end:
.org 0x1D4E8
m68k_01d4e8:
        lsl.l #0x1,%d0
m68k_01d4e8_end:
.org 0x1D4EA
m68k_01d4ea:
        add.l %d1,%d0
m68k_01d4ea_end:
.org 0x1D4EC
m68k_01d4ec:
        swap %d0
m68k_01d4ec_end:
.org 0x1D4EE
m68k_01d4ee:
        addq.w #0x1,%d0
m68k_01d4ee_end:
.org 0x1D4F0
m68k_01d4f0:
        lea.l 0xc500:w,%a0
m68k_01d4f0_end:
.org 0x1D4F4
m68k_01d4f4:
        cmpi.w #0x5,0xffff8114:l
m68k_01d4f4_end:
.org 0x1D4FC
m68k_01d4fc:
        beq.w (. + 44)
m68k_01d4fc_end:
.org 0x1D500
m68k_01d500:
        cmpi.w #0x4,0xffff8114:l
m68k_01d500_end:
.org 0x1D508
m68k_01d508:
        bne.w (. + 56)
m68k_01d508_end:
.org 0x1D50C
m68k_01d50c:
        move.w 0xffff80e0:l,%d1
m68k_01d50c_end:
.org 0x1D512
m68k_01d512:
        clr.w %d2
m68k_01d512_end:
.org 0x1D514
m68k_01d514:
        move.b (%a0, %d1.w),%d2
m68k_01d514_end:
.org 0x1D518
m68k_01d518:
        sub.w %d0,%d2
m68k_01d518_end:
.org 0x1D51A
m68k_01d51a:
        bcc.w (. + 6)
m68k_01d51a_end:
.org 0x1D51E
m68k_01d51e:
        clr.w %d2
m68k_01d51e_end:
.org 0x1D520
m68k_01d520:
        move.b %d2,(%a0, %d1.w)
m68k_01d520_end:
.org 0x1D524
m68k_01d524:
        bra.w (. + 28)
m68k_01d524_end:
.org 0x1D528
m68k_01d528:
        move.w 0xffff80e2:l,%d1
m68k_01d528_end:
.org 0x1D52E
m68k_01d52e:
        clr.w %d2
m68k_01d52e_end:
.org 0x1D530
m68k_01d530:
        move.b (%a0, %d1.w),%d2
m68k_01d530_end:
.org 0x1D534
m68k_01d534:
        sub.w %d0,%d2
m68k_01d534_end:
.org 0x1D536
m68k_01d536:
        bcc.w (. + 6)
m68k_01d536_end:
.org 0x1D53A
m68k_01d53a:
        clr.w %d2
m68k_01d53a_end:
.org 0x1D53C
m68k_01d53c:
        move.b %d2,(%a0, %d1.w)
m68k_01d53c_end:
.org 0x1D540
m68k_01d540:
        rts
m68k_01d540_end:
.org 0x1D542
m68k_01d542:
        lea.l 0xa050:w,%a0
m68k_01d542_end:
.org 0x1D546
m68k_01d546:
        move.w 0xf68a:w,%d0
m68k_01d546_end:
.org 0x1D54A
m68k_01d54a:
        move.w #0xff,%d1
m68k_01d54a_end:
.org 0x1D54E
m68k_01d54e:
        move.b (%a0, %d1.w),%d2
m68k_01d54e_end:
.org 0x1D552
m68k_01d552:
        andi.w #0x3f,%d2
m68k_01d552_end:
.org 0x1D556
m68k_01d556:
        cmp.w %d0,%d2
m68k_01d556_end:
.org 0x1D558
m68k_01d558:
        bne.w (. + 8)
m68k_01d558_end:
.org 0x1D55C
m68k_01d55c:
        clr.b (%a0, %d1.w)
m68k_01d55c_end:
.org 0x1D560
m68k_01d560:
        dbra %d1,(. + -18)
m68k_01d560_end:
.org 0x1D564
m68k_01d564:
        lea.l 0xa550:w,%a1
m68k_01d564_end:
.org 0x1D568
m68k_01d568:
        move.w (%a1)+,%d2
m68k_01d568_end:
.org 0x1D56A
m68k_01d56a:
        bmi.w (. + 14)
m68k_01d56a_end:
.org 0x1D56E
m68k_01d56e:
        andi.w #0xff,%d2
m68k_01d56e_end:
.org 0x1D572
m68k_01d572:
        move.b %d0,(%a0, %d2.w)
m68k_01d572_end:
.org 0x1D576
m68k_01d576:
        bra.b (. + -14)
m68k_01d576_end:
.org 0x1D578
m68k_01d578:
        rts
m68k_01d578_end:
.org 0x1D598
m68k_01d598:
        lea.l 0xff7050:l,%a0
m68k_01d598_end:
.org 0x1D59E
m68k_01d59e:
        lea.l 0xff70a0:l,%a1
m68k_01d59e_end:
.org 0x1D5A4
m68k_01d5a4:
        move.b 0xff70f0:l,%d0
m68k_01d5a4_end:
.org 0x1D5AA
m68k_01d5aa:
        move.b 0xff70f1:l,%d1
m68k_01d5aa_end:
.org 0x1D5B0
m68k_01d5b0:
        move.w 0xffff80e0:l,%d2
m68k_01d5b0_end:
.org 0x1D5B6
m68k_01d5b6:
        cmp.w 0x1a(%a0),%d2
m68k_01d5b6_end:
.org 0x1D5BA
m68k_01d5ba:
        beq.w (. + 8)
m68k_01d5ba_end:
.org 0x1D5BE
m68k_01d5be:
        exg %a0,%a1
m68k_01d5be_end:
.org 0x1D5C0
m68k_01d5c0:
        exg %d0,%d1
m68k_01d5c0_end:
.org 0x1D5C2
m68k_01d5c2:
        tst.w 0x1c(%a0)
m68k_01d5c2_end:
.org 0x1D5C6
m68k_01d5c6:
        beq.w (. + 52)
m68k_01d5c6_end:
.org 0x1D5CA
m68k_01d5ca:
        tst.w 0x1c(%a1)
m68k_01d5ca_end:
.org 0x1D5CE
m68k_01d5ce:
        beq.w (. + 56)
m68k_01d5ce_end:
.org 0x1D5D2
m68k_01d5d2:
        cmpi.b #0x1,%d0
m68k_01d5d2_end:
.org 0x1D5D6
m68k_01d5d6:
        beq.w (. + 60)
m68k_01d5d6_end:
.org 0x1D5DA
m68k_01d5da:
        cmpi.b #0x1,%d1
m68k_01d5da_end:
.org 0x1D5DE
m68k_01d5de:
        beq.w (. + 64)
m68k_01d5de_end:
.org 0x1D5E2
m68k_01d5e2:
        tst.b %d0
m68k_01d5e2_end:
.org 0x1D5E4
m68k_01d5e4:
        bne.w (. + 70)
m68k_01d5e4_end:
.org 0x1D5E8
m68k_01d5e8:
        tst.b %d1
m68k_01d5e8_end:
.org 0x1D5EA
m68k_01d5ea:
        beq.w (. + 72)
m68k_01d5ea_end:
.org 0x1D5EE
m68k_01d5ee:
        move.w #0x7,0xffff8114:l
m68k_01d5ee_end:
.org 0x1D5F6
m68k_01d5f6:
        bra.w (. + 60)
m68k_01d5f6_end:
.org 0x1D5FA
m68k_01d5fa:
        move.w #0x3,0xffff8114:l
m68k_01d5fa_end:
.org 0x1D602
m68k_01d602:
        bra.w (. + 48)
m68k_01d602_end:
.org 0x1D606
m68k_01d606:
        move.w #0x2,0xffff8114:l
m68k_01d606_end:
.org 0x1D60E
m68k_01d60e:
        bra.w (. + 36)
m68k_01d60e_end:
.org 0x1D612
m68k_01d612:
        move.w #0x4,0xffff8114:l
m68k_01d612_end:
.org 0x1D61A
m68k_01d61a:
        bra.w (. + 24)
m68k_01d61a_end:
.org 0x1D61E
m68k_01d61e:
        move.w #0x5,0xffff8114:l
m68k_01d61e_end:
.org 0x1D626
m68k_01d626:
        bra.w (. + 12)
m68k_01d626_end:
.org 0x1D62A
m68k_01d62a:
        move.w #0x6,0xffff8114:l
m68k_01d62a_end:
.org 0x1D632
m68k_01d632:
        rts
m68k_01d632_end:
.org 0x1DF60
m68k_01df60:
        move.w (%a6),%d4
m68k_01df60_end:
.org 0x1DF62
m68k_01df62:
        addi.w #0xb80,%d4
m68k_01df62_end:
.org 0x1DF66
m68k_01df66:
        move.w 0x4(%a6),%d6
m68k_01df66_end:
.org 0x1DF6A
m68k_01df6a:
        addi.w #0xb80,%d6
m68k_01df6a_end:
.org 0x1DF6E
m68k_01df6e:
        bsr.w (. + 42)
m68k_01df6e_end:
.org 0x1DF72
m68k_01df72:
        bcs.w (. + 36)
m68k_01df72_end:
.org 0x1DF76
m68k_01df76:
        addi.w #0x800,%d6
m68k_01df76_end:
.org 0x1DF7A
m68k_01df7a:
        bsr.w (. + 30)
m68k_01df7a_end:
.org 0x1DF7E
m68k_01df7e:
        bcs.w (. + 24)
m68k_01df7e_end:
.org 0x1DF82
m68k_01df82:
        addi.w #0x800,%d4
m68k_01df82_end:
.org 0x1DF86
m68k_01df86:
        bsr.w (. + 18)
m68k_01df86_end:
.org 0x1DF8A
m68k_01df8a:
        bcs.w (. + 12)
m68k_01df8a_end:
.org 0x1DF8E
m68k_01df8e:
        subi.w #0x800,%d6
m68k_01df8e_end:
.org 0x1DF92
m68k_01df92:
        bsr.w (. + 6)
m68k_01df92_end:
.org 0x1DF96
m68k_01df96:
        rts
m68k_01df96_end:
.org 0x1DF98
m68k_01df98:
        lea.l 0xa5a4:w,%a5
m68k_01df98_end:
.org 0x1DF9C
m68k_01df9c:
        move.w (%a5)+,%d5
m68k_01df9c_end:
.org 0x1DF9E
m68k_01df9e:
        bmi.b (. + 26)
m68k_01df9e_end:
.org 0x1DFA0
m68k_01dfa0:
        lsl.w #0x2,%d5
m68k_01dfa0_end:
.org 0x1DFA2
m68k_01dfa2:
        cmp.w (%a1, %d5.w),%d4
m68k_01dfa2_end:
.org 0x1DFA6
m68k_01dfa6:
        bne.b (. + -10)
m68k_01dfa6_end:
.org 0x1DFA8
m68k_01dfa8:
        cmp.w 0x2(%a1, %d5.w),%d6
m68k_01dfa8_end:
.org 0x1DFAC
m68k_01dfac:
        bne.w (. + -16)
m68k_01dfac_end:
.org 0x1DFB0
m68k_01dfb0:
        andi.w #0xfffe,%sr
m68k_01dfb0_end:
.org 0x1DFB4
m68k_01dfb4:
        bra.w (. + 16)
m68k_01dfb4_end:
.org 0x1DFB8
m68k_01dfb8:
        move.w %d4,(%a1, %d0.w)
m68k_01dfb8_end:
.org 0x1DFBC
m68k_01dfbc:
        move.w %d6,0x2(%a1, %d0.w)
m68k_01dfbc_end:
.org 0x1DFC0
m68k_01dfc0:
        ori.w #0x1,%sr
m68k_01dfc0_end:
.org 0x1DFC4
m68k_01dfc4:
        rts
m68k_01dfc4_end:
.org 0x1E04E
m68k_01e04e:
        move.l %d4,-(%a7)
m68k_01e04e_end:
.org 0x1E050
m68k_01e050:
        move.w 0xf68a:w,%d4
m68k_01e050_end:
.org 0x1E054
m68k_01e054:
        mulu.w #0x8c0,%d4
m68k_01e054_end:
.org 0x1E058
m68k_01e058:
        lea.l 0x945e8:l,%a5
m68k_01e058_end:
.org 0x1E05E
m68k_01e05e:
        adda.l %d4,%a5
m68k_01e05e_end:
.org 0x1E060
m68k_01e060:
        move.l (%a7)+,%d4
m68k_01e060_end:
.org 0x1E062
m68k_01e062:
        move.w %d1,%d4
m68k_01e062_end:
.org 0x1E064
m68k_01e064:
        lsr.w #0x7,%d4
m68k_01e064_end:
.org 0x1E066
m68k_01e066:
        andi.w #0xf8,%d4
m68k_01e066_end:
.org 0x1E06A
m68k_01e06a:
        move.w %d4,%d5
m68k_01e06a_end:
.org 0x1E06C
m68k_01e06c:
        lsl.w #0x2,%d4
m68k_01e06c_end:
.org 0x1E06E
m68k_01e06e:
        add.w %d5,%d4
m68k_01e06e_end:
.org 0x1E070
m68k_01e070:
        move.w %d2,%d5
m68k_01e070_end:
.org 0x1E072
m68k_01e072:
        lsr.w #0x7,%d5
m68k_01e072_end:
.org 0x1E074
m68k_01e074:
        lsr.w #0x3,%d5
m68k_01e074_end:
.org 0x1E076
m68k_01e076:
        add.w %d5,%d4
m68k_01e076_end:
.org 0x1E078
m68k_01e078:
        lsl.w #0x1,%d4
m68k_01e078_end:
.org 0x1E07A
m68k_01e07a:
        move.w (%a5, %d4.w),%d5
m68k_01e07a_end:
.org 0x1E07E
m68k_01e07e:
        andi.w #0x3ff,%d5
m68k_01e07e_end:
.org 0x1E082
m68k_01e082:
        lea.l 0x6c0b4:l,%a5
m68k_01e082_end:
.org 0x1E088
m68k_01e088:
        move.b (%a5, %d5.w),%d5
m68k_01e088_end:
.org 0x1E08C
m68k_01e08c:
        andi.w #0xff,%d5
m68k_01e08c_end:
.org 0x1E090
m68k_01e090:
        move.w %d5,%d4
m68k_01e090_end:
.org 0x1E092
m68k_01e092:
        lsl.w #0x1,%d5
m68k_01e092_end:
.org 0x1E094
m68k_01e094:
        move.w 8(%pc, %d5.w),%d5
m68k_01e094_end:
.org 0x1E098
m68k_01e098:
        jsr 20(%pc, %d5.w)
m68k_01e098_end:
.org 0x1E09C
m68k_01e09c:
        rts
m68k_01e09c_end:
.org 0x1E0E6
m68k_01e0e6:
        lea.l 0xceae:w,%a0
m68k_01e0e6_end:
.org 0x1E0EA
m68k_01e0ea:
        move.w #0xff,%d0
m68k_01e0ea_end:
.org 0x1E0EE
m68k_01e0ee:
        tst.b (%a0)+
m68k_01e0ee_end:
.org 0x1E0F0
m68k_01e0f0:
        beq.w (. + 8)
m68k_01e0f0_end:
.org 0x1E0F4
m68k_01e0f4:
        subq.b #0x1,-0x1(%a0)
m68k_01e0f4_end:
.org 0x1E0F8
m68k_01e0f8:
        dbra %d0,(. + -10)
m68k_01e0f8_end:
.org 0x1E0FC
m68k_01e0fc:
        rts
m68k_01e0fc_end:
.org 0x1E0FE
m68k_01e0fe:
        move.w 0xf700:w,%d0
m68k_01e0fe_end:
.org 0x1E102
m68k_01e102:
        cmpi.w #0xa,%d0
m68k_01e102_end:
.org 0x1E106
m68k_01e106:
        bcc.w (. + 30)
m68k_01e106_end:
.org 0x1E10A
m68k_01e10a:
        lea.l 0xa550:w,%a0
m68k_01e10a_end:
.org 0x1E10E
m68k_01e10e:
        lsl.w #0x1,%d0
m68k_01e10e_end:
.org 0x1E110
m68k_01e110:
        move.w (%a0, %d0.w),%d7
m68k_01e110_end:
.org 0x1E114
m68k_01e114:
        bmi.b (. + 6)
m68k_01e114_end:
.org 0x1E116
m68k_01e116:
        bra.w (. + 42)
m68k_01e116_end:
.org 0x1E11A
m68k_01e11a:
        move.w #0xa,0xf700:w
m68k_01e11a_end:
.org 0x1E120
m68k_01e120:
        bra.w (. + 118)
m68k_01e120_end:
.org 0x1E124
m68k_01e124:
        subi.w #0xa,%d0
m68k_01e124_end:
.org 0x1E128
m68k_01e128:
        lsl.w #0x1,%d0
m68k_01e128_end:
.org 0x1E12A
m68k_01e12a:
        lea.l 0xa5a4:w,%a0
m68k_01e12a_end:
.org 0x1E12E
m68k_01e12e:
        move.w (%a0, %d0.w),%d7
m68k_01e12e_end:
.org 0x1E132
m68k_01e132:
        bmi.b (. + 6)
m68k_01e132_end:
.org 0x1E134
m68k_01e134:
        bra.w (. + 12)
m68k_01e134_end:
.org 0x1E138
m68k_01e138:
        clr.w 0xf700:w
m68k_01e138_end:
.org 0x1E13C
m68k_01e13c:
        bra.w (. + 90)
m68k_01e13c_end:
.org 0x1E140
m68k_01e140:
        lea.l 0xae28:w,%a2
m68k_01e140_end:
.org 0x1E144
m68k_01e144:
        andi.w #0xff,%d7
m68k_01e144_end:
.org 0x1E148
m68k_01e148:
        lea.l 0xa654:w,%a0
m68k_01e148_end:
.org 0x1E14C
m68k_01e14c:
        tst.b (%a0, %d7.w)
m68k_01e14c_end:
.org 0x1E150
m68k_01e150:
        bpl.b (. + 54)
m68k_01e150_end:
.org 0x1E152
m68k_01e152:
        clr.w %d1
m68k_01e152_end:
.org 0x1E154
m68k_01e154:
        lea.l 0xa854:w,%a0
m68k_01e154_end:
.org 0x1E158
m68k_01e158:
        move.b (%a0, %d7.w),%d1
m68k_01e158_end:
.org 0x1E15C
m68k_01e15c:
        lsl.w #0x2,%d1
m68k_01e15c_end:
.org 0x1E15E
m68k_01e15e:
        lea.l 0xa150:w,%a0
m68k_01e15e_end:
.org 0x1E162
m68k_01e162:
        lea.l 0xff2c00:l,%a1
m68k_01e162_end:
.org 0x1E168
m68k_01e168:
        lsl.w #0x2,%d7
m68k_01e168_end:
.org 0x1E16A
m68k_01e16a:
        move.w (%a0, %d1.w),%d2
m68k_01e16a_end:
.org 0x1E16E
m68k_01e16e:
        lsr.w #0x7,%d2
m68k_01e16e_end:
.org 0x1E170
m68k_01e170:
        move.w %d2,(%a1, %d7.w)
m68k_01e170_end:
.org 0x1E174
m68k_01e174:
        move.w 0x2(%a0, %d1.w),%d2
m68k_01e174_end:
.org 0x1E178
m68k_01e178:
        lsr.w #0x7,%d2
m68k_01e178_end:
.org 0x1E17A
m68k_01e17a:
        move.w %d2,0x2(%a1, %d7.w)
m68k_01e17a_end:
.org 0x1E17E
m68k_01e17e:
        lsr.w #0x2,%d7
m68k_01e17e_end:
.org 0x1E180
m68k_01e180:
        move.b #0x1,(%a2, %d7.w)
m68k_01e180_end:
.org 0x1E186
m68k_01e186:
        cmpi.b #0x1,(%a2, %d7.w)
m68k_01e186_end:
.org 0x1E18C
m68k_01e18c:
        bne.b (. + 6)
m68k_01e18c_end:
.org 0x1E18E
m68k_01e18e:
        bsr.w (. + -1252)
m68k_01e18e_end:
.org 0x1E192
m68k_01e192:
        addq.w #0x1,0xf700:w
m68k_01e192_end:
.org 0x1E196
m68k_01e196:
        rts
m68k_01e196_end:
.org 0x1F13C
m68k_01f13c:
        lea.l 0xff3cc2:l,%a0
m68k_01f13c_end:
.org 0x1F142
m68k_01f142:
        move.w #0xff,%d1
m68k_01f142_end:
.org 0x1F146
m68k_01f146:
        move.b (%a0),%d0
m68k_01f146_end:
.org 0x1F148
m68k_01f148:
        beq.w (. + 6)
m68k_01f148_end:
.org 0x1F14C
m68k_01f14c:
        subq.b #0x1,%d0
m68k_01f14c_end:
.org 0x1F14E
m68k_01f14e:
        move.b %d0,(%a0)+
m68k_01f14e_end:
.org 0x1F150
m68k_01f150:
        dbra %d1,(. + -10)
m68k_01f150_end:
.org 0x1F154
m68k_01f154:
        rts
m68k_01f154_end:
.org 0x1F156
m68k_01f156:
        move.w 0xf68c:w,%d0
m68k_01f156_end:
.org 0x1F15A
m68k_01f15a:
        btst.b #0x5,0xf603:w
m68k_01f15a_end:
.org 0x1F160
m68k_01f160:
        beq.w (. + 68)
m68k_01f160_end:
.org 0x1F164
m68k_01f164:
        cmp.w 0xf67a:w,%d0
m68k_01f164_end:
.org 0x1F168
m68k_01f168:
        beq.w (. + 124)
m68k_01f168_end:
.org 0x1F16C
m68k_01f16c:
        cmp.w 0xf67e:w,%d0
m68k_01f16c_end:
.org 0x1F170
m68k_01f170:
        bne.w (. + 16)
m68k_01f170_end:
.org 0x1F174
m68k_01f174:
        move.w 0xf68e:w,%d0
m68k_01f174_end:
.org 0x1F178
m68k_01f178:
        cmp.w 0xf67c:w,%d0
m68k_01f178_end:
.org 0x1F17C
m68k_01f17c:
        beq.w (. + 104)
m68k_01f17c_end:
.org 0x1F180
m68k_01f180:
        move.w 0xf68e:w,%d0
m68k_01f180_end:
.org 0x1F184
m68k_01f184:
        cmp.w 0xf67a:w,%d0
m68k_01f184_end:
.org 0x1F188
m68k_01f188:
        beq.w (. + 104)
m68k_01f188_end:
.org 0x1F18C
m68k_01f18c:
        cmp.w 0xf67e:w,%d0
m68k_01f18c_end:
.org 0x1F190
m68k_01f190:
        bne.w (. + 110)
m68k_01f190_end:
.org 0x1F194
m68k_01f194:
        move.w 0xf68c:w,%d0
m68k_01f194_end:
.org 0x1F198
m68k_01f198:
        cmp.w 0xf67c:w,%d0
m68k_01f198_end:
.org 0x1F19C
m68k_01f19c:
        beq.w (. + 84)
m68k_01f19c_end:
.org 0x1F1A0
m68k_01f1a0:
        bra.w (. + 94)
m68k_01f1a0_end:
.org 0x1F1A4
m68k_01f1a4:
        cmp.w 0xf67c:w,%d0
m68k_01f1a4_end:
.org 0x1F1A8
m68k_01f1a8:
        beq.w (. + 60)
m68k_01f1a8_end:
.org 0x1F1AC
m68k_01f1ac:
        cmp.w 0xf67e:w,%d0
m68k_01f1ac_end:
.org 0x1F1B0
m68k_01f1b0:
        bne.w (. + 16)
m68k_01f1b0_end:
.org 0x1F1B4
m68k_01f1b4:
        move.w 0xf68e:w,%d0
m68k_01f1b4_end:
.org 0x1F1B8
m68k_01f1b8:
        cmp.w 0xf67c:w,%d0
m68k_01f1b8_end:
.org 0x1F1BC
m68k_01f1bc:
        bne.w (. + 40)
m68k_01f1bc_end:
.org 0x1F1C0
m68k_01f1c0:
        move.w 0xf68e:w,%d0
m68k_01f1c0_end:
.org 0x1F1C4
m68k_01f1c4:
        cmp.w 0xf67c:w,%d0
m68k_01f1c4_end:
.org 0x1F1C8
m68k_01f1c8:
        beq.w (. + 40)
m68k_01f1c8_end:
.org 0x1F1CC
m68k_01f1cc:
        cmp.w 0xf67e:w,%d0
m68k_01f1cc_end:
.org 0x1F1D0
m68k_01f1d0:
        bne.w (. + 46)
m68k_01f1d0_end:
.org 0x1F1D4
m68k_01f1d4:
        move.w 0xf68c:w,%d0
m68k_01f1d4_end:
.org 0x1F1D8
m68k_01f1d8:
        cmp.w 0xf67c:w,%d0
m68k_01f1d8_end:
.org 0x1F1DC
m68k_01f1dc:
        bne.w (. + 20)
m68k_01f1dc_end:
.org 0x1F1E0
m68k_01f1e0:
        bra.w (. + 30)
m68k_01f1e0_end:
.org 0x1F1E4
m68k_01f1e4:
        clr.w 0xf6d6:w
m68k_01f1e4_end:
.org 0x1F1E8
m68k_01f1e8:
        andi.w #0xfffe,%sr
m68k_01f1e8_end:
.org 0x1F1EC
m68k_01f1ec:
        bra.w (. + 22)
m68k_01f1ec_end:
.org 0x1F1F0
m68k_01f1f0:
        move.w #0x2,0xf6d6:w
m68k_01f1f0_end:
.org 0x1F1F6
m68k_01f1f6:
        andi.w #0xfffe,%sr
m68k_01f1f6_end:
.org 0x1F1FA
m68k_01f1fa:
        bra.w (. + 8)
m68k_01f1fa_end:
.org 0x1F1FE
m68k_01f1fe:
        ori.w #0x1,%sr
m68k_01f1fe_end:
.org 0x1F202
m68k_01f202:
        rts
m68k_01f202_end:
.org 0x1F204
m68k_01f204:
        move.w 0xf68c:w,%d0
m68k_01f204_end:
.org 0x1F208
m68k_01f208:
        move.w 0xf68e:w,%d1
m68k_01f208_end:
.org 0x1F20C
m68k_01f20c:
        btst.b #0x7,0xf603:w
m68k_01f20c_end:
.org 0x1F212
m68k_01f212:
        beq.w (. + 60)
m68k_01f212_end:
.org 0x1F216
m68k_01f216:
        cmp.w 0xf67a:w,%d0
m68k_01f216_end:
.org 0x1F21A
m68k_01f21a:
        beq.w (. + 108)
m68k_01f21a_end:
.org 0x1F21E
m68k_01f21e:
        cmp.w 0xf67e:w,%d0
m68k_01f21e_end:
.org 0x1F222
m68k_01f222:
        bne.w (. + 16)
m68k_01f222_end:
.org 0x1F226
m68k_01f226:
        cmp.w 0xf67c:w,%d1
m68k_01f226_end:
.org 0x1F22A
m68k_01f22a:
        beq.w (. + 92)
m68k_01f22a_end:
.org 0x1F22E
m68k_01f22e:
        bra.w (. + 114)
m68k_01f22e_end:
.org 0x1F232
m68k_01f232:
        cmp.w 0xf67a:w,%d1
m68k_01f232_end:
.org 0x1F236
m68k_01f236:
        beq.w (. + 92)
m68k_01f236_end:
.org 0x1F23A
m68k_01f23a:
        cmp.w 0xf67e:w,%d1
m68k_01f23a_end:
.org 0x1F23E
m68k_01f23e:
        bne.w (. + 98)
m68k_01f23e_end:
.org 0x1F242
m68k_01f242:
        cmp.w 0xf67c:w,%d0
m68k_01f242_end:
.org 0x1F246
m68k_01f246:
        beq.w (. + 76)
m68k_01f246_end:
.org 0x1F24A
m68k_01f24a:
        bra.w (. + 86)
m68k_01f24a_end:
.org 0x1F24E
m68k_01f24e:
        cmp.w 0xf67c:w,%d0
m68k_01f24e_end:
.org 0x1F252
m68k_01f252:
        beq.w (. + 52)
m68k_01f252_end:
.org 0x1F256
m68k_01f256:
        cmp.w 0xf67e:w,%d0
m68k_01f256_end:
.org 0x1F25A
m68k_01f25a:
        bne.w (. + 16)
m68k_01f25a_end:
.org 0x1F25E
m68k_01f25e:
        cmp.w 0xf67c:w,%d1
m68k_01f25e_end:
.org 0x1F262
m68k_01f262:
        bne.w (. + 36)
m68k_01f262_end:
.org 0x1F266
m68k_01f266:
        bra.w (. + 58)
m68k_01f266_end:
.org 0x1F26A
m68k_01f26a:
        cmp.w 0xf67c:w,%d1
m68k_01f26a_end:
.org 0x1F26E
m68k_01f26e:
        beq.w (. + 36)
m68k_01f26e_end:
.org 0x1F272
m68k_01f272:
        cmp.w 0xf67e:w,%d1
m68k_01f272_end:
.org 0x1F276
m68k_01f276:
        bne.w (. + 42)
m68k_01f276_end:
.org 0x1F27A
m68k_01f27a:
        cmp.w 0xf67c:w,%d0
m68k_01f27a_end:
.org 0x1F27E
m68k_01f27e:
        beq.w (. + 20)
m68k_01f27e_end:
.org 0x1F282
m68k_01f282:
        bra.w (. + 30)
m68k_01f282_end:
.org 0x1F286
m68k_01f286:
        clr.w 0xf6d6:w
m68k_01f286_end:
.org 0x1F28A
m68k_01f28a:
        andi.w #0xfffe,%sr
m68k_01f28a_end:
.org 0x1F28E
m68k_01f28e:
        bra.w (. + 22)
m68k_01f28e_end:
.org 0x1F292
m68k_01f292:
        move.w #0x2,0xf6d6:w
m68k_01f292_end:
.org 0x1F298
m68k_01f298:
        andi.w #0xfffe,%sr
m68k_01f298_end:
.org 0x1F29C
m68k_01f29c:
        bra.w (. + 8)
m68k_01f29c_end:
.org 0x1F2A0
m68k_01f2a0:
        ori.w #0x1,%sr
m68k_01f2a0_end:
.org 0x1F2A4
m68k_01f2a4:
        rts
m68k_01f2a4_end:
.org 0x1F2A6
m68k_01f2a6:
        move.w 0xf68c:w,%d0
m68k_01f2a6_end:
.org 0x1F2AA
m68k_01f2aa:
        move.w 0xf68e:w,%d1
m68k_01f2aa_end:
.org 0x1F2AE
m68k_01f2ae:
        btst.b #0x6,0xf603:w
m68k_01f2ae_end:
.org 0x1F2B4
m68k_01f2b4:
        bne.w (. + 60)
m68k_01f2b4_end:
.org 0x1F2B8
m68k_01f2b8:
        cmp.w 0xf67c:w,%d0
m68k_01f2b8_end:
.org 0x1F2BC
m68k_01f2bc:
        beq.w (. + 108)
m68k_01f2bc_end:
.org 0x1F2C0
m68k_01f2c0:
        cmp.w 0xf67c:w,%d1
m68k_01f2c0_end:
.org 0x1F2C4
m68k_01f2c4:
        beq.w (. + 112)
m68k_01f2c4_end:
.org 0x1F2C8
m68k_01f2c8:
        cmp.w 0xf67e:w,%d0
m68k_01f2c8_end:
.org 0x1F2CC
m68k_01f2cc:
        bne.w (. + 16)
m68k_01f2cc_end:
.org 0x1F2D0
m68k_01f2d0:
        cmp.w 0xf67c:w,%d1
m68k_01f2d0_end:
.org 0x1F2D4
m68k_01f2d4:
        bne.w (. + 84)
m68k_01f2d4_end:
.org 0x1F2D8
m68k_01f2d8:
        bra.w (. + 106)
m68k_01f2d8_end:
.org 0x1F2DC
m68k_01f2dc:
        cmp.w 0xf67e:w,%d1
m68k_01f2dc_end:
.org 0x1F2E0
m68k_01f2e0:
        bne.w (. + 98)
m68k_01f2e0_end:
.org 0x1F2E4
m68k_01f2e4:
        cmp.w 0xf67c:w,%d0
m68k_01f2e4_end:
.org 0x1F2E8
m68k_01f2e8:
        bne.w (. + 76)
m68k_01f2e8_end:
.org 0x1F2EC
m68k_01f2ec:
        bra.w (. + 86)
m68k_01f2ec_end:
.org 0x1F2F0
m68k_01f2f0:
        cmp.w 0xf67a:w,%d0
m68k_01f2f0_end:
.org 0x1F2F4
m68k_01f2f4:
        beq.w (. + 52)
m68k_01f2f4_end:
.org 0x1F2F8
m68k_01f2f8:
        cmp.w 0xf67a:w,%d1
m68k_01f2f8_end:
.org 0x1F2FC
m68k_01f2fc:
        beq.w (. + 56)
m68k_01f2fc_end:
.org 0x1F300
m68k_01f300:
        cmp.w 0xf67e:w,%d0
m68k_01f300_end:
.org 0x1F304
m68k_01f304:
        bne.w (. + 16)
m68k_01f304_end:
.org 0x1F308
m68k_01f308:
        cmp.w 0xf67c:w,%d1
m68k_01f308_end:
.org 0x1F30C
m68k_01f30c:
        beq.w (. + 28)
m68k_01f30c_end:
.org 0x1F310
m68k_01f310:
        bra.w (. + 50)
m68k_01f310_end:
.org 0x1F314
m68k_01f314:
        cmp.w 0xf67e:w,%d1
m68k_01f314_end:
.org 0x1F318
m68k_01f318:
        bne.w (. + 42)
m68k_01f318_end:
.org 0x1F31C
m68k_01f31c:
        cmp.w 0xf67c:w,%d0
m68k_01f31c_end:
.org 0x1F320
m68k_01f320:
        beq.w (. + 20)
m68k_01f320_end:
.org 0x1F324
m68k_01f324:
        bra.w (. + 30)
m68k_01f324_end:
.org 0x1F328
m68k_01f328:
        clr.w 0xf6d6:w
m68k_01f328_end:
.org 0x1F32C
m68k_01f32c:
        andi.w #0xfffe,%sr
m68k_01f32c_end:
.org 0x1F330
m68k_01f330:
        bra.w (. + 22)
m68k_01f330_end:
.org 0x1F334
m68k_01f334:
        move.w #0x2,0xf6d6:w
m68k_01f334_end:
.org 0x1F33A
m68k_01f33a:
        andi.w #0xfffe,%sr
m68k_01f33a_end:
.org 0x1F33E
m68k_01f33e:
        bra.w (. + 8)
m68k_01f33e_end:
.org 0x1F342
m68k_01f342:
        ori.w #0x1,%sr
m68k_01f342_end:
.org 0x1F346
m68k_01f346:
        rts
m68k_01f346_end:
.org 0x1F348
m68k_01f348:
        clr.w %d0
m68k_01f348_end:
.org 0x1F34A
m68k_01f34a:
        move.w 0xf68c:w,%d1
m68k_01f34a_end:
.org 0x1F34E
m68k_01f34e:
        move.w 0xf68e:w,%d2
m68k_01f34e_end:
.org 0x1F352
m68k_01f352:
        cmp.w 0xf67a:w,%d1
m68k_01f352_end:
.org 0x1F356
m68k_01f356:
        beq.w (. + 48)
m68k_01f356_end:
.org 0x1F35A
m68k_01f35a:
        cmp.w 0xf67a:w,%d2
m68k_01f35a_end:
.org 0x1F35E
m68k_01f35e:
        beq.w (. + 40)
m68k_01f35e_end:
.org 0x1F362
m68k_01f362:
        cmp.w 0xf67e:w,%d1
m68k_01f362_end:
.org 0x1F366
m68k_01f366:
        bne.w (. + 16)
m68k_01f366_end:
.org 0x1F36A
m68k_01f36a:
        cmp.w 0xf67c:w,%d2
m68k_01f36a_end:
.org 0x1F36E
m68k_01f36e:
        beq.w (. + 24)
m68k_01f36e_end:
.org 0x1F372
m68k_01f372:
        bra.w (. + 24)
m68k_01f372_end:
.org 0x1F376
m68k_01f376:
        cmp.w 0xf67e:w,%d2
m68k_01f376_end:
.org 0x1F37A
m68k_01f37a:
        bne.w (. + 16)
m68k_01f37a_end:
.org 0x1F37E
m68k_01f37e:
        cmp.w 0xf67c:w,%d1
m68k_01f37e_end:
.org 0x1F382
m68k_01f382:
        bne.w (. + 8)
m68k_01f382_end:
.org 0x1F386
m68k_01f386:
        move.w 0xf602:w,%d0
m68k_01f386_end:
.org 0x1F38A
m68k_01f38a:
        cmp.w 0xf67c:w,%d1
m68k_01f38a_end:
.org 0x1F38E
m68k_01f38e:
        beq.w (. + 48)
m68k_01f38e_end:
.org 0x1F392
m68k_01f392:
        cmp.w 0xf67c:w,%d2
m68k_01f392_end:
.org 0x1F396
m68k_01f396:
        beq.w (. + 40)
m68k_01f396_end:
.org 0x1F39A
m68k_01f39a:
        cmp.w 0xf67e:w,%d1
m68k_01f39a_end:
.org 0x1F39E
m68k_01f39e:
        bne.w (. + 16)
m68k_01f39e_end:
.org 0x1F3A2
m68k_01f3a2:
        cmp.w 0xf67c:w,%d2
m68k_01f3a2_end:
.org 0x1F3A6
m68k_01f3a6:
        bne.w (. + 24)
m68k_01f3a6_end:
.org 0x1F3AA
m68k_01f3aa:
        bra.w (. + 24)
m68k_01f3aa_end:
.org 0x1F3AE
m68k_01f3ae:
        cmp.w 0xf67e:w,%d2
m68k_01f3ae_end:
.org 0x1F3B2
m68k_01f3b2:
        bne.w (. + 16)
m68k_01f3b2_end:
.org 0x1F3B6
m68k_01f3b6:
        cmp.w 0xf67c:w,%d1
m68k_01f3b6_end:
.org 0x1F3BA
m68k_01f3ba:
        beq.w (. + 8)
m68k_01f3ba_end:
.org 0x1F3BE
m68k_01f3be:
        or.w 0xf604:w,%d0
m68k_01f3be_end:
.org 0x1F3C2
m68k_01f3c2:
        rts
m68k_01f3c2_end:
.org 0x1F512
m68k_01f512:
        jsr 0x83d4:l
m68k_01f512_end:
.org 0x1F518
m68k_01f518:
        andi.l #0xffff,%d0
m68k_01f518_end:
.org 0x1F51E
m68k_01f51e:
        move.l %d0,%d1
m68k_01f51e_end:
.org 0x1F520
m68k_01f520:
        lsl.l #0x1,%d0
m68k_01f520_end:
.org 0x1F522
m68k_01f522:
        add.l %d1,%d0
m68k_01f522_end:
.org 0x1F524
m68k_01f524:
        lsl.l #0x1,%d0
m68k_01f524_end:
.org 0x1F526
m68k_01f526:
        swap %d0
m68k_01f526_end:
.org 0x1F528
m68k_01f528:
        addi.w #0x5,%d0
m68k_01f528_end:
.org 0x1F52C
m68k_01f52c:
        lea.l 0xc000:w,%a3
m68k_01f52c_end:
.org 0x1F530
m68k_01f530:
        move.w (%a3, %d3.w),%d4
m68k_01f530_end:
.org 0x1F534
m68k_01f534:
        add.w %d0,%d4
m68k_01f534_end:
.org 0x1F536
m68k_01f536:
        cmpi.w #0x3e7,%d4
m68k_01f536_end:
.org 0x1F53A
m68k_01f53a:
        bls.w (. + 8)
m68k_01f53a_end:
.org 0x1F53E
m68k_01f53e:
        move.w #0x3e7,%d4
m68k_01f53e_end:
.org 0x1F542
m68k_01f542:
        move.w %d4,(%a3, %d3.w)
m68k_01f542_end:
.org 0x1F546
m68k_01f546:
        jsr 0x83d4:l
m68k_01f546_end:
.org 0x1F54C
m68k_01f54c:
        andi.l #0xffff,%d0
m68k_01f54c_end:
.org 0x1F552
m68k_01f552:
        move.l %d0,%d1
m68k_01f552_end:
.org 0x1F554
m68k_01f554:
        lsl.l #0x2,%d0
m68k_01f554_end:
.org 0x1F556
m68k_01f556:
        add.l %d1,%d0
m68k_01f556_end:
.org 0x1F558
m68k_01f558:
        lsl.l #0x1,%d0
m68k_01f558_end:
.org 0x1F55A
m68k_01f55a:
        add.l %d1,%d0
m68k_01f55a_end:
.org 0x1F55C
m68k_01f55c:
        swap %d0
m68k_01f55c_end:
.org 0x1F55E
m68k_01f55e:
        addi.w #0xa,%d0
m68k_01f55e_end:
.org 0x1F562
m68k_01f562:
        lea.l 0xbe00:w,%a3
m68k_01f562_end:
.org 0x1F566
m68k_01f566:
        move.w (%a3, %d3.w),%d4
m68k_01f566_end:
.org 0x1F56A
m68k_01f56a:
        add.w %d0,%d4
m68k_01f56a_end:
.org 0x1F56C
m68k_01f56c:
        cmpi.w #0x3e7,%d4
m68k_01f56c_end:
.org 0x1F570
m68k_01f570:
        bls.w (. + 8)
m68k_01f570_end:
.org 0x1F574
m68k_01f574:
        move.w #0x3e7,%d4
m68k_01f574_end:
.org 0x1F578
m68k_01f578:
        move.w %d4,(%a3, %d3.w)
m68k_01f578_end:
.org 0x1F57C
m68k_01f57c:
        rts
m68k_01f57c_end:
.org 0x1F57E
m68k_01f57e:
        jsr 0x83d4:l
m68k_01f57e_end:
.org 0x1F584
m68k_01f584:
        andi.l #0xffff,%d0
m68k_01f584_end:
.org 0x1F58A
m68k_01f58a:
        move.l %d0,%d1
m68k_01f58a_end:
.org 0x1F58C
m68k_01f58c:
        lsl.l #0x1,%d0
m68k_01f58c_end:
.org 0x1F58E
m68k_01f58e:
        add.l %d1,%d0
m68k_01f58e_end:
.org 0x1F590
m68k_01f590:
        lsl.l #0x1,%d0
m68k_01f590_end:
.org 0x1F592
m68k_01f592:
        swap %d0
m68k_01f592_end:
.org 0x1F594
m68k_01f594:
        addi.w #0x5,%d0
m68k_01f594_end:
.org 0x1F598
m68k_01f598:
        lea.l 0xc500:w,%a3
m68k_01f598_end:
.org 0x1F59C
m68k_01f59c:
        move.b (%a3, %d2.w),%d4
m68k_01f59c_end:
.org 0x1F5A0
m68k_01f5a0:
        sub.b %d0,%d4
m68k_01f5a0_end:
.org 0x1F5A2
m68k_01f5a2:
        bcc.w (. + 6)
m68k_01f5a2_end:
.org 0x1F5A6
m68k_01f5a6:
        clr.b %d4
m68k_01f5a6_end:
.org 0x1F5A8
m68k_01f5a8:
        move.b %d4,(%a3, %d2.w)
m68k_01f5a8_end:
.org 0x1F5AC
m68k_01f5ac:
        rts
m68k_01f5ac_end:
.org 0x1F5AE
m68k_01f5ae:
        jsr 0x83d4:l
m68k_01f5ae_end:
.org 0x1F5B4
m68k_01f5b4:
        andi.l #0xffff,%d0
m68k_01f5b4_end:
.org 0x1F5BA
m68k_01f5ba:
        move.l %d0,%d1
m68k_01f5ba_end:
.org 0x1F5BC
m68k_01f5bc:
        lsl.l #0x2,%d0
m68k_01f5bc_end:
.org 0x1F5BE
m68k_01f5be:
        add.l %d1,%d0
m68k_01f5be_end:
.org 0x1F5C0
m68k_01f5c0:
        swap %d0
m68k_01f5c0_end:
.org 0x1F5C2
m68k_01f5c2:
        addq.w #0x1,%d0
m68k_01f5c2_end:
.org 0x1F5C4
m68k_01f5c4:
        move.w 0xa5f8:w,%d2
m68k_01f5c4_end:
.org 0x1F5C8
m68k_01f5c8:
        lsl.w #0x2,%d2
m68k_01f5c8_end:
.org 0x1F5CA
m68k_01f5ca:
        lea.l 0xc800:w,%a0
m68k_01f5ca_end:
.org 0x1F5CE
m68k_01f5ce:
        move.l (%a0, %d2.w),%d3
m68k_01f5ce_end:
.org 0x1F5D2
m68k_01f5d2:
        move.l %d3,%d4
m68k_01f5d2_end:
.org 0x1F5D4
m68k_01f5d4:
        mulu.w %d0,%d3
m68k_01f5d4_end:
.org 0x1F5D6
m68k_01f5d6:
        divu.w #0xa,%d3
m68k_01f5d6_end:
.org 0x1F5DA
m68k_01f5da:
        sub.w %d3,%d4
m68k_01f5da_end:
.org 0x1F5DC
m68k_01f5dc:
        move.l %d4,(%a0, %d2.w)
m68k_01f5dc_end:
.org 0x1F5E0
m68k_01f5e0:
        divu.w #0x3c,%d3
m68k_01f5e0_end:
.org 0x1F5E4
m68k_01f5e4:
        lea.l 0xc000:w,%a0
m68k_01f5e4_end:
.org 0x1F5E8
m68k_01f5e8:
        move.w 0xf766:w,%d4
m68k_01f5e8_end:
.org 0x1F5EC
m68k_01f5ec:
        lsl.w #0x1,%d4
m68k_01f5ec_end:
.org 0x1F5EE
m68k_01f5ee:
        move.w (%a0, %d4.w),%d5
m68k_01f5ee_end:
.org 0x1F5F2
m68k_01f5f2:
        add.w %d3,%d5
m68k_01f5f2_end:
.org 0x1F5F4
m68k_01f5f4:
        cmpi.w #0x3e7,%d5
m68k_01f5f4_end:
.org 0x1F5F8
m68k_01f5f8:
        bls.w (. + 8)
m68k_01f5f8_end:
.org 0x1F5FC
m68k_01f5fc:
        move.w #0x3e7,%d5
m68k_01f5fc_end:
.org 0x1F600
m68k_01f600:
        move.w %d5,(%a0, %d4.w)
m68k_01f600_end:
.org 0x1F604
m68k_01f604:
        jsr 0x83d4:l
m68k_01f604_end:
.org 0x1F60A
m68k_01f60a:
        andi.l #0xffff,%d0
m68k_01f60a_end:
.org 0x1F610
m68k_01f610:
        move.l %d0,%d1
m68k_01f610_end:
.org 0x1F612
m68k_01f612:
        lsl.l #0x2,%d0
m68k_01f612_end:
.org 0x1F614
m68k_01f614:
        add.l %d1,%d0
m68k_01f614_end:
.org 0x1F616
m68k_01f616:
        lsl.l #0x1,%d0
m68k_01f616_end:
.org 0x1F618
m68k_01f618:
        add.l %d1,%d0
m68k_01f618_end:
.org 0x1F61A
m68k_01f61a:
        swap %d0
m68k_01f61a_end:
.org 0x1F61C
m68k_01f61c:
        addi.w #0xa,%d0
m68k_01f61c_end:
.org 0x1F620
m68k_01f620:
        lea.l 0xbe00:w,%a0
m68k_01f620_end:
.org 0x1F624
m68k_01f624:
        move.w (%a0, %d4.w),%d5
m68k_01f624_end:
.org 0x1F628
m68k_01f628:
        add.w %d0,%d5
m68k_01f628_end:
.org 0x1F62A
m68k_01f62a:
        cmpi.w #0x3e7,%d5
m68k_01f62a_end:
.org 0x1F62E
m68k_01f62e:
        bls.w (. + 8)
m68k_01f62e_end:
.org 0x1F632
m68k_01f632:
        move.w #0x3e7,%d5
m68k_01f632_end:
.org 0x1F636
m68k_01f636:
        move.w %d5,(%a0, %d4.w)
m68k_01f636_end:
.org 0x1F63A
m68k_01f63a:
        jsr 0x83d4:l
m68k_01f63a_end:
.org 0x1F640
m68k_01f640:
        andi.l #0xffff,%d0
m68k_01f640_end:
.org 0x1F646
m68k_01f646:
        move.l %d0,%d1
m68k_01f646_end:
.org 0x1F648
m68k_01f648:
        lsl.l #0x2,%d0
m68k_01f648_end:
.org 0x1F64A
m68k_01f64a:
        add.l %d1,%d0
m68k_01f64a_end:
.org 0x1F64C
m68k_01f64c:
        lsl.l #0x1,%d0
m68k_01f64c_end:
.org 0x1F64E
m68k_01f64e:
        add.l %d1,%d0
m68k_01f64e_end:
.org 0x1F650
m68k_01f650:
        swap %d0
m68k_01f650_end:
.org 0x1F652
m68k_01f652:
        addi.w #0xa,%d0
m68k_01f652_end:
.org 0x1F656
m68k_01f656:
        lea.l 0xc500:w,%a0
m68k_01f656_end:
.org 0x1F65A
m68k_01f65a:
        move.w 0xa5f8:w,%d2
m68k_01f65a_end:
.org 0x1F65E
m68k_01f65e:
        move.b (%a0, %d2.w),%d3
m68k_01f65e_end:
.org 0x1F662
m68k_01f662:
        sub.b %d0,%d3
m68k_01f662_end:
.org 0x1F664
m68k_01f664:
        bcc.w (. + 6)
m68k_01f664_end:
.org 0x1F668
m68k_01f668:
        clr.b %d3
m68k_01f668_end:
.org 0x1F66A
m68k_01f66a:
        move.b %d3,(%a0, %d2.w)
m68k_01f66a_end:
.org 0x1F66E
m68k_01f66e:
        move.w 0xf766:w,%d0
m68k_01f66e_end:
.org 0x1F672
m68k_01f672:
        lea.l 0xff3bc2:l,%a0
m68k_01f672_end:
.org 0x1F678
m68k_01f678:
        clr.b (%a0, %d0.w)
m68k_01f678_end:
.org 0x1F67C
m68k_01f67c:
        rts
m68k_01f67c_end:
.org 0x1F67E
m68k_01f67e:
        clr.w 0xf6d6:w
m68k_01f67e_end:
.org 0x1F682
m68k_01f682:
        move.w 0xf766:w,%d0
m68k_01f682_end:
.org 0x1F686
m68k_01f686:
        andi.w #0xff,%d0
m68k_01f686_end:
.org 0x1F68A
m68k_01f68a:
        lea.l 0xa5a4:w,%a0
m68k_01f68a_end:
.org 0x1F68E
m68k_01f68e:
        move.w (%a0)+,%d1
m68k_01f68e_end:
.org 0x1F690
m68k_01f690:
        bmi.w (. + 14)
m68k_01f690_end:
.org 0x1F694
m68k_01f694:
        cmp.w %d0,%d1
m68k_01f694_end:
.org 0x1F696
m68k_01f696:
        bne.b (. + -8)
m68k_01f696_end:
.org 0x1F698
m68k_01f698:
        move.w #0x2,0xf6d6:w
m68k_01f698_end:
.org 0x1F69E
m68k_01f69e:
        rts
m68k_01f69e_end:
.org 0x1F886
m68k_01f886:
        jsr 0x1a438:l
m68k_01f886_end:
.org 0x1F88C
m68k_01f88c:
        lea.l 0xa150:w,%a1
m68k_01f88c_end:
.org 0x1F890
m68k_01f890:
        move.w 0xf702:w,%d3
m68k_01f890_end:
.org 0x1F894
m68k_01f894:
        lsl.w #0x2,%d3
m68k_01f894_end:
.org 0x1F896
m68k_01f896:
        move.w 0xf706:w,%d4
m68k_01f896_end:
.org 0x1F89A
m68k_01f89a:
        lsl.w #0x2,%d4
m68k_01f89a_end:
.org 0x1F89C
m68k_01f89c:
        move.w (%a1, %d3.w),%d1
m68k_01f89c_end:
.org 0x1F8A0
m68k_01f8a0:
        lsr.w #0x7,%d1
m68k_01f8a0_end:
.org 0x1F8A2
m68k_01f8a2:
        move.w (%a1, %d4.w),%d0
m68k_01f8a2_end:
.org 0x1F8A6
m68k_01f8a6:
        lsr.w #0x7,%d0
m68k_01f8a6_end:
.org 0x1F8A8
m68k_01f8a8:
        add.w %d0,%d1
m68k_01f8a8_end:
.org 0x1F8AA
m68k_01f8aa:
        lsr.w #0x1,%d1
m68k_01f8aa_end:
.org 0x1F8AC
m68k_01f8ac:
        move.w 0x2(%a1, %d3.w),%d2
m68k_01f8ac_end:
.org 0x1F8B0
m68k_01f8b0:
        lsr.w #0x7,%d2
m68k_01f8b0_end:
.org 0x1F8B2
m68k_01f8b2:
        move.w 0x2(%a1, %d4.w),%d0
m68k_01f8b2_end:
.org 0x1F8B6
m68k_01f8b6:
        lsr.w #0x7,%d0
m68k_01f8b6_end:
.org 0x1F8B8
m68k_01f8b8:
        add.w %d0,%d2
m68k_01f8b8_end:
.org 0x1F8BA
m68k_01f8ba:
        lsr.w #0x1,%d2
m68k_01f8ba_end:
.org 0x1F8BC
m68k_01f8bc:
        jsr 0x1a44e:l
m68k_01f8bc_end:
.org 0x1F8C2
m68k_01f8c2:
        andi.w #0xff,%d0
m68k_01f8c2_end:
.org 0x1F8C6
m68k_01f8c6:
        move.b 4(%pc, %d0.w),%d0
m68k_01f8c6_end:
.org 0x1F8CA
m68k_01f8ca:
        rts
m68k_01f8ca_end:
.org 0x1F8D4
m68k_01f8d4:
        move.w %d0,%d1
m68k_01f8d4_end:
.org 0x1F8D6
m68k_01f8d6:
        lsl.w #0x1,%d1
m68k_01f8d6_end:
.org 0x1F8D8
m68k_01f8d8:
        add.w %d0,%d1
m68k_01f8d8_end:
.org 0x1F8DA
m68k_01f8da:
        lea.l 52(%pc),%a6
m68k_01f8da_end:
.org 0x1F8DE
m68k_01f8de:
        clr.w %d3
m68k_01f8de_end:
.org 0x1F8E0
m68k_01f8e0:
        clr.w %d2
m68k_01f8e0_end:
.org 0x1F8E2
m68k_01f8e2:
        move.b (%a5, %d1.w),%d2
m68k_01f8e2_end:
.org 0x1F8E6
m68k_01f8e6:
        move.b (%a6, %d2.w),%d3
m68k_01f8e6_end:
.org 0x1F8EA
m68k_01f8ea:
        addq.w #0x4,%a6
m68k_01f8ea_end:
.org 0x1F8EC
m68k_01f8ec:
        move.b 0x1(%a5, %d1.w),%d2
m68k_01f8ec_end:
.org 0x1F8F0
m68k_01f8f0:
        cmp.b (%a6, %d2.w),%d3
m68k_01f8f0_end:
.org 0x1F8F4
m68k_01f8f4:
        bcc.w (. + 8)
m68k_01f8f4_end:
.org 0x1F8F8
m68k_01f8f8:
        move.b (%a6, %d2.w),%d3
m68k_01f8f8_end:
.org 0x1F8FC
m68k_01f8fc:
        addq.w #0x4,%a6
m68k_01f8fc_end:
.org 0x1F8FE
m68k_01f8fe:
        move.b 0x2(%a5, %d1.w),%d2
m68k_01f8fe_end:
.org 0x1F902
m68k_01f902:
        cmp.b (%a6, %d2.w),%d3
m68k_01f902_end:
.org 0x1F906
m68k_01f906:
        bcc.w (. + 8)
m68k_01f906_end:
.org 0x1F90A
m68k_01f90a:
        move.b (%a6, %d2.w),%d3
m68k_01f90a_end:
.org 0x1F90E
m68k_01f90e:
        rts
m68k_01f90e_end:
.org 0x1F91C
m68k_01f91c:
        clr.w %d1
m68k_01f91c_end:
.org 0x1F91E
m68k_01f91e:
        move.w 0xf68c:w,%d0
m68k_01f91e_end:
.org 0x1F922
m68k_01f922:
        cmp.w 0xf67a:w,%d0
m68k_01f922_end:
.org 0x1F926
m68k_01f926:
        beq.w (. + 26)
m68k_01f926_end:
.org 0x1F92A
m68k_01f92a:
        addq.w #0x8,%d1
m68k_01f92a_end:
.org 0x1F92C
m68k_01f92c:
        cmp.w 0xf67c:w,%d0
m68k_01f92c_end:
.org 0x1F930
m68k_01f930:
        beq.w (. + 16)
m68k_01f930_end:
.org 0x1F934
m68k_01f934:
        addq.w #0x8,%d1
m68k_01f934_end:
.org 0x1F936
m68k_01f936:
        cmp.w 0xf67e:w,%d0
m68k_01f936_end:
.org 0x1F93A
m68k_01f93a:
        beq.w (. + 6)
m68k_01f93a_end:
.org 0x1F93E
m68k_01f93e:
        addq.w #0x8,%d1
m68k_01f93e_end:
.org 0x1F940
m68k_01f940:
        move.w 0xf68e:w,%d0
m68k_01f940_end:
.org 0x1F944
m68k_01f944:
        cmp.w 0xf67a:w,%d0
m68k_01f944_end:
.org 0x1F948
m68k_01f948:
        beq.w (. + 26)
m68k_01f948_end:
.org 0x1F94C
m68k_01f94c:
        addq.w #0x2,%d1
m68k_01f94c_end:
.org 0x1F94E
m68k_01f94e:
        cmp.w 0xf67c:w,%d0
m68k_01f94e_end:
.org 0x1F952
m68k_01f952:
        beq.w (. + 16)
m68k_01f952_end:
.org 0x1F956
m68k_01f956:
        addq.w #0x2,%d1
m68k_01f956_end:
.org 0x1F958
m68k_01f958:
        cmp.w 0xf67e:w,%d0
m68k_01f958_end:
.org 0x1F95C
m68k_01f95c:
        beq.w (. + 6)
m68k_01f95c_end:
.org 0x1F960
m68k_01f960:
        addq.w #0x2,%d1
m68k_01f960_end:
.org 0x1F962
m68k_01f962:
        lea.l 26(%pc),%a0
m68k_01f962_end:
.org 0x1F966
m68k_01f966:
        move.b (%a0, %d1.w),0xffff80da:l
m68k_01f966_end:
.org 0x1F96E
m68k_01f96e:
        clr.b 0xffff8124:l
m68k_01f96e_end:
.org 0x1F974
m68k_01f974:
        move.b 0x1(%a0, %d1.w),0xffff8125:l
m68k_01f974_end:
.org 0x1F97C
m68k_01f97c:
        rts
m68k_01f97c_end:
.org 0x1FA52
m68k_01fa52:
        move.w 0xf70a:w,%d0
m68k_01fa52_end:
.org 0x1FA56
m68k_01fa56:
        andi.w #0x3,%d0
m68k_01fa56_end:
.org 0x1FA5A
m68k_01fa5a:
        lsl.w #0x1,%d0
m68k_01fa5a_end:
.org 0x1FA5C
m68k_01fa5c:
        move.w 66(%pc, %d0.w),%d0
m68k_01fa5c_end:
.org 0x1FA60
m68k_01fa60:
        add.w %d0,0xf6fa:w
m68k_01fa60_end:
.org 0x1FA64
m68k_01fa64:
        cmpi.w #0x960,0xf6fa:w
m68k_01fa64_end:
.org 0x1FA6A
m68k_01fa6a:
        bcs.b (. + 52)
m68k_01fa6a_end:
.org 0x1FA6C
m68k_01fa6c:
        clr.w 0xf6f8:w
m68k_01fa6c_end:
.org 0x1FA70
m68k_01fa70:
        clr.w 0xf6fa:w
m68k_01fa70_end:
.org 0x1FA74
m68k_01fa74:
        addq.w #0x1,0xf6c8:w
m68k_01fa74_end:
.org 0x1FA78
m68k_01fa78:
        cmpi.w #0x1d,0xf6c8:w
m68k_01fa78_end:
.org 0x1FA7E
m68k_01fa7e:
        bls.b (. + 16)
m68k_01fa7e_end:
.org 0x1FA80
m68k_01fa80:
        move.w #0x413,0xf612:w
m68k_01fa80_end:
.org 0x1FA86
m68k_01fa86:
        clr.w 0xf362:w
m68k_01fa86_end:
.org 0x1FA8A
m68k_01fa8a:
        bra.w (. + 20)
m68k_01fa8a_end:
.org 0x1FA8E
m68k_01fa8e:
        jsr 0x1a25e:l
m68k_01fa8e_end:
.org 0x1FA94
m68k_01fa94:
        bsr.w (. + 20)
m68k_01fa94_end:
.org 0x1FA98
m68k_01fa98:
        move.w #0xbc,0xf600:w
m68k_01fa98_end:
.org 0x1FA9E
m68k_01fa9e:
        rts
m68k_01fa9e_end:
.org 0x1FAA8
m68k_01faa8:
        lea.l 0xa654:w,%a0
m68k_01faa8_end:
.org 0x1FAAC
m68k_01faac:
        lea.l 0xff3dc2:l,%a1
m68k_01faac_end:
.org 0x1FAB2
m68k_01fab2:
        move.w #0xff,%d1
m68k_01fab2_end:
.org 0x1FAB6
m68k_01fab6:
        move.b (%a0),%d0
m68k_01fab6_end:
.org 0x1FAB8
m68k_01fab8:
        beq.b (. + 14)
m68k_01fab8_end:
.org 0x1FABA
m68k_01faba:
        subq.b #0x1,%d0
m68k_01faba_end:
.org 0x1FABC
m68k_01fabc:
        bpl.b (. + 10)
m68k_01fabc_end:
.org 0x1FABE
m68k_01fabe:
        cmpi.b #0x80,%d0
m68k_01fabe_end:
.org 0x1FAC2
m68k_01fac2:
        bne.b (. + 4)
m68k_01fac2_end:
.org 0x1FAC4
m68k_01fac4:
        clr.b %d0
m68k_01fac4_end:
.org 0x1FAC6
m68k_01fac6:
        move.b %d0,(%a0)+
m68k_01fac6_end:
.org 0x1FAC8
m68k_01fac8:
        move.b (%a1),%d0
m68k_01fac8_end:
.org 0x1FACA
m68k_01faca:
        beq.w (. + 6)
m68k_01faca_end:
.org 0x1FACE
m68k_01face:
        subq.b #0x1,%d0
m68k_01face_end:
.org 0x1FAD0
m68k_01fad0:
        move.b %d0,(%a1)+
m68k_01fad0_end:
.org 0x1FAD2
m68k_01fad2:
        dbra %d1,(. + -28)
m68k_01fad2_end:
.org 0x1FAD6
m68k_01fad6:
        lea.l 0xa754:w,%a0
m68k_01fad6_end:
.org 0x1FADA
m68k_01fada:
        move.w #0xff,%d1
m68k_01fada_end:
.org 0x1FADE
m68k_01fade:
        move.b (%a0),%d0
m68k_01fade_end:
.org 0x1FAE0
m68k_01fae0:
        beq.b (. + 4)
m68k_01fae0_end:
.org 0x1FAE2
m68k_01fae2:
        subq.b #0x1,%d0
m68k_01fae2_end:
.org 0x1FAE4
m68k_01fae4:
        move.b %d0,(%a0)+
m68k_01fae4_end:
.org 0x1FAE6
m68k_01fae6:
        dbra %d1,(. + -8)
m68k_01fae6_end:
.org 0x1FAEA
m68k_01faea:
        rts
m68k_01faea_end:
.org 0x20088
m68k_020088:
        lea.l 0xf45e:w,%a0
m68k_020088_end:
.org 0x2008C
m68k_02008c:
        move.w 0xf68a:w,%d0
m68k_02008c_end:
.org 0x20090
m68k_020090:
        lsl.w #0x1,%d0
m68k_020090_end:
.org 0x20092
m68k_020092:
        move.w (%a0, %d0.w),%d0
m68k_020092_end:
.org 0x20096
m68k_020096:
        lea.l 0xa5a4:w,%a0
m68k_020096_end:
.org 0x2009A
m68k_02009a:
        move.w (%a0)+,%d1
m68k_02009a_end:
.org 0x2009C
m68k_02009c:
        bmi.w (. + 12)
m68k_02009c_end:
.org 0x200A0
m68k_0200a0:
        cmp.b %d0,%d1
m68k_0200a0_end:
.org 0x200A2
m68k_0200a2:
        beq.w (. + 16)
m68k_0200a2_end:
.org 0x200A6
m68k_0200a6:
        bra.b (. + -12)
m68k_0200a6_end:
.org 0x200A8
m68k_0200a8:
        move.w #0x0,0xf6d6:w
m68k_0200a8_end:
.org 0x200AE
m68k_0200ae:
        bra.w (. + 40)
m68k_0200ae_end:
.org 0x200B2
m68k_0200b2:
        lea.l 0xa027:w,%a0
m68k_0200b2_end:
.org 0x200B6
m68k_0200b6:
        move.w 0xf68a:w,%d0
m68k_0200b6_end:
.org 0x200BA
m68k_0200ba:
        move.b (%a0, %d0.w),%d0
m68k_0200ba_end:
.org 0x200BE
m68k_0200be:
        lea.l 0xa550:w,%a0
m68k_0200be_end:
.org 0x200C2
m68k_0200c2:
        move.w (%a0)+,%d1
m68k_0200c2_end:
.org 0x200C4
m68k_0200c4:
        bmi.w (. + 12)
m68k_0200c4_end:
.org 0x200C8
m68k_0200c8:
        cmp.b %d0,%d1
m68k_0200c8_end:
.org 0x200CA
m68k_0200ca:
        beq.w (. + 22)
m68k_0200ca_end:
.org 0x200CE
m68k_0200ce:
        bra.b (. + -12)
m68k_0200ce_end:
.org 0x200D0
m68k_0200d0:
        move.w #0x2,0xf6d6:w
m68k_0200d0_end:
.org 0x200D6
m68k_0200d6:
        move.w #0x411,0xf612:w
m68k_0200d6_end:
.org 0x200DC
m68k_0200dc:
        clr.w 0xf362:w
m68k_0200dc_end:
.org 0x200E0
m68k_0200e0:
        rts
m68k_0200e0_end:
.org 0x200E2
m68k_0200e2:
        move.w 0xf68a:w,%d6
m68k_0200e2_end:
.org 0x200E6
m68k_0200e6:
        subq.w #0x1,%d6
m68k_0200e6_end:
.org 0x200E8
m68k_0200e8:
        move.w %d6,%d7
m68k_0200e8_end:
.org 0x200EA
m68k_0200ea:
        lsr.w #0x3,%d7
m68k_0200ea_end:
.org 0x200EC
m68k_0200ec:
        andi.w #0x7,%d6
m68k_0200ec_end:
.org 0x200F0
m68k_0200f0:
        lea.l 0xefaa:w,%a6
m68k_0200f0_end:
.org 0x200F4
m68k_0200f4:
        btst.l %d6,(%a6, %d7.w)
m68k_0200f4_end:
.org 0x200F8
m68k_0200f8:
        bne.w (. + 34)
m68k_0200f8_end:
.org 0x200FC
m68k_0200fc:
        bsr.w (. + 152)
m68k_0200fc_end:
.org 0x20100
m68k_020100:
        bcc.w (. + 146)
m68k_020100_end:
.org 0x20104
m68k_020104:
        move.w #0x5,0xf362:w
m68k_020104_end:
.org 0x2010A
m68k_02010a:
        move.w #0x13a,%d0
m68k_02010a_end:
.org 0x2010E
m68k_02010e:
        move.w 0xf68c:w,0xf376:w
m68k_02010e_end:
.org 0x20114
m68k_020114:
        jsr 0x676f2:l
m68k_020114_end:
.org 0x2011A
m68k_02011a:
        move.w 0xf68a:w,%d6
m68k_02011a_end:
.org 0x2011E
m68k_02011e:
        subq.w #0x1,%d6
m68k_02011e_end:
.org 0x20120
m68k_020120:
        move.w %d6,%d7
m68k_020120_end:
.org 0x20122
m68k_020122:
        lsr.w #0x3,%d7
m68k_020122_end:
.org 0x20124
m68k_020124:
        andi.w #0x7,%d6
m68k_020124_end:
.org 0x20128
m68k_020128:
        lea.l 0xefaa:w,%a6
m68k_020128_end:
.org 0x2012C
m68k_02012c:
        bset.b %d6,(%a6, %d7.w)
m68k_02012c_end:
.org 0x20130
m68k_020130:
        move.l 0xf696:w,%d0
m68k_020130_end:
.org 0x20134
m68k_020134:
        add.l 0xf69a:w,%d0
m68k_020134_end:
.org 0x20138
m68k_020138:
        cmpi.l #0xf423f,%d0
m68k_020138_end:
.org 0x2013E
m68k_02013e:
        bls.w (. + 10)
m68k_02013e_end:
.org 0x20142
m68k_020142:
        move.l #0xf423f,%d0
m68k_020142_end:
.org 0x20148
m68k_020148:
        move.l %d0,0xf69a:w
m68k_020148_end:
.org 0x2014C
m68k_02014c:
        clr.l 0xf696:w
m68k_02014c_end:
.org 0x20150
m68k_020150:
        move.l 0xf69e:w,%d0
m68k_020150_end:
.org 0x20154
m68k_020154:
        add.l 0xf6a2:w,%d0
m68k_020154_end:
.org 0x20158
m68k_020158:
        cmpi.l #0xf423f,%d0
m68k_020158_end:
.org 0x2015E
m68k_02015e:
        bls.w (. + 10)
m68k_02015e_end:
.org 0x20162
m68k_020162:
        move.l #0xf423f,%d0
m68k_020162_end:
.org 0x20168
m68k_020168:
        move.l %d0,0xf6a2:w
m68k_020168_end:
.org 0x2016C
m68k_02016c:
        clr.l 0xf69e:w
m68k_02016c_end:
.org 0x20170
m68k_020170:
        lea.l 0xa57a:w,%a0
m68k_020170_end:
.org 0x20174
m68k_020174:
        lea.l 0xcc00:w,%a1
m68k_020174_end:
.org 0x20178
m68k_020178:
        move.w 0xf68a:w,%d0
m68k_020178_end:
.org 0x2017C
m68k_02017c:
        move.w (%a0)+,%d1
m68k_02017c_end:
.org 0x2017E
m68k_02017e:
        bmi.w (. + 14)
m68k_02017e_end:
.org 0x20182
m68k_020182:
        andi.w #0xff,%d1
m68k_020182_end:
.org 0x20186
m68k_020186:
        move.b %d0,(%a1, %d1.w)
m68k_020186_end:
.org 0x2018A
m68k_02018a:
        bra.b (. + -14)
m68k_02018a_end:
.org 0x2018C
m68k_02018c:
        move.w #0xffff,0xa57a:w
m68k_02018c_end:
.org 0x20192
m68k_020192:
        rts
m68k_020192_end:
.org 0x20194
m68k_020194:
        lea.l 0x9fff:w,%a0
m68k_020194_end:
.org 0x20198
m68k_020198:
        move.w 0xf68a:w,%d0
m68k_020198_end:
.org 0x2019C
m68k_02019c:
        clr.w %d1
m68k_02019c_end:
.org 0x2019E
m68k_02019e:
        move.b (%a0, %d0.w),%d1
m68k_02019e_end:
.org 0x201A2
m68k_0201a2:
        lsl.w #0x1,%d1
m68k_0201a2_end:
.org 0x201A4
m68k_0201a4:
        lsl.w #0x5,%d0
m68k_0201a4_end:
.org 0x201A6
m68k_0201a6:
        add.w %d1,%d0
m68k_0201a6_end:
.org 0x201A8
m68k_0201a8:
        lea.l 0xabda8:l,%a0
m68k_0201a8_end:
.org 0x201AE
m68k_0201ae:
        clr.w %d1
m68k_0201ae_end:
.org 0x201B0
m68k_0201b0:
        move.b (%a0, %d0.w),%d1
m68k_0201b0_end:
.org 0x201B4
m68k_0201b4:
        lsl.w #0x3,%d1
m68k_0201b4_end:
.org 0x201B6
m68k_0201b6:
        lsl.w #0x7,%d1
m68k_0201b6_end:
.org 0x201B8
m68k_0201b8:
        move.w %d1,%d2
m68k_0201b8_end:
.org 0x201BA
m68k_0201ba:
        clr.w %d3
m68k_0201ba_end:
.org 0x201BC
m68k_0201bc:
        move.b 0x1(%a0, %d0.w),%d3
m68k_0201bc_end:
.org 0x201C0
m68k_0201c0:
        lsl.w #0x3,%d3
m68k_0201c0_end:
.org 0x201C2
m68k_0201c2:
        lsl.w #0x7,%d3
m68k_0201c2_end:
.org 0x201C4
m68k_0201c4:
        move.w %d3,%d4
m68k_0201c4_end:
.org 0x201C6
m68k_0201c6:
        subi.w #0x400,%d1
m68k_0201c6_end:
.org 0x201CA
m68k_0201ca:
        addi.w #0x400,%d2
m68k_0201ca_end:
.org 0x201CE
m68k_0201ce:
        subi.w #0x400,%d3
m68k_0201ce_end:
.org 0x201D2
m68k_0201d2:
        addi.w #0x400,%d4
m68k_0201d2_end:
.org 0x201D6
m68k_0201d6:
        lea.l 0xa5a4:w,%a0
m68k_0201d6_end:
.org 0x201DA
m68k_0201da:
        lea.l 0xa150:w,%a1
m68k_0201da_end:
.org 0x201DE
m68k_0201de:
        move.w (%a0)+,%d0
m68k_0201de_end:
.org 0x201E0
m68k_0201e0:
        bmi.w (. + 38)
m68k_0201e0_end:
.org 0x201E4
m68k_0201e4:
        lsl.w #0x2,%d0
m68k_0201e4_end:
.org 0x201E6
m68k_0201e6:
        move.w (%a1, %d0.w),%d5
m68k_0201e6_end:
.org 0x201EA
m68k_0201ea:
        cmp.w %d1,%d5
m68k_0201ea_end:
.org 0x201EC
m68k_0201ec:
        bcs.b (. + -14)
m68k_0201ec_end:
.org 0x201EE
m68k_0201ee:
        cmp.w %d2,%d5
m68k_0201ee_end:
.org 0x201F0
m68k_0201f0:
        bhi.b (. + -18)
m68k_0201f0_end:
.org 0x201F2
m68k_0201f2:
        move.w 0x2(%a1, %d0.w),%d5
m68k_0201f2_end:
.org 0x201F6
m68k_0201f6:
        cmp.w %d3,%d5
m68k_0201f6_end:
.org 0x201F8
m68k_0201f8:
        bcs.b (. + -26)
m68k_0201f8_end:
.org 0x201FA
m68k_0201fa:
        cmp.w %d4,%d5
m68k_0201fa_end:
.org 0x201FC
m68k_0201fc:
        bhi.b (. + -30)
m68k_0201fc_end:
.org 0x201FE
m68k_0201fe:
        ori.w #0x1,%sr
m68k_0201fe_end:
.org 0x20202
m68k_020202:
        bra.w (. + 8)
m68k_020202_end:
.org 0x20206
m68k_020206:
        andi.w #0xfffe,%sr
m68k_020206_end:
.org 0x2020A
m68k_02020a:
        rts
m68k_02020a_end:
.org 0x26D46
m68k_026d46:
        move.w #0x2500,%sr
m68k_026d46_end:
.org 0x26D4A
m68k_026d4a:
        move.w #0x700,0xf612:w
m68k_026d4a_end:
.org 0x26D50
m68k_026d50:
        tst.b 0xf612:w
m68k_026d50_end:
.org 0x26D54
m68k_026d54:
        bne.b (. + -4)
m68k_026d54_end:
.org 0x26D56
m68k_026d56:
        bsr.w (. + 3374)
m68k_026d56_end:
.org 0x26D5A
m68k_026d5a:
        cmpi.w #0x10,0xff70f6:l
m68k_026d5a_end:
.org 0x26D62
m68k_026d62:
        bcc.w (. + 34)
m68k_026d62_end:
.org 0x26D66
m68k_026d66:
        move.w 0xff70f6:l,%d0
m68k_026d66_end:
.org 0x26D6C
m68k_026d6c:
        move.w #0x40,%d1
m68k_026d6c_end:
.org 0x26D70
m68k_026d70:
        lea.l 4878(%pc),%a0
m68k_026d70_end:
.org 0x26D74
m68k_026d74:
        nop
m68k_026d74_end:
.org 0x26D76
m68k_026d76:
        jsr 0xdea6:l
m68k_026d76_end:
.org 0x26D7C
m68k_026d7c:
        addq.w #0x1,0xff70f6:l
m68k_026d7c_end:
.org 0x26D82
m68k_026d82:
        bra.b (. + -56)
m68k_026d82_end:
.org 0x26D84
m68k_026d84:
        rts
m68k_026d84_end:
.org 0x26D86
m68k_026d86:
        cmpi.w #0x10,0xff70f8:l
m68k_026d86_end:
.org 0x26D8E
m68k_026d8e:
        bcc.w (. + 36)
m68k_026d8e_end:
.org 0x26D92
m68k_026d92:
        move.w #0xf,%d0
m68k_026d92_end:
.org 0x26D96
m68k_026d96:
        sub.w 0xff70f8:l,%d0
m68k_026d96_end:
.org 0x26D9C
m68k_026d9c:
        move.w #0x40,%d1
m68k_026d9c_end:
.org 0x26DA0
m68k_026da0:
        lea.l 4830(%pc),%a0
m68k_026da0_end:
.org 0x26DA4
m68k_026da4:
        nop
m68k_026da4_end:
.org 0x26DA6
m68k_026da6:
        jsr 0xdea6:l
m68k_026da6_end:
.org 0x26DAC
m68k_026dac:
        addq.w #0x1,0xff70f8:l
m68k_026dac_end:
.org 0x26DB2
m68k_026db2:
        rts
m68k_026db2_end:
.org 0x27060
m68k_027060:
        move.w #0x700,0xf612:w
m68k_027060_end:
.org 0x27066
m68k_027066:
        tst.b 0xf612:w
m68k_027066_end:
.org 0x2706A
m68k_02706a:
        bne.b (. + -4)
m68k_02706a_end:
.org 0x2706C
m68k_02706c:
        jsr -744(%pc)
m68k_02706c_end:
.org 0x27070
m68k_027070:
        bsr.w (. + 2580)
m68k_027070_end:
.org 0x27074
m68k_027074:
        clr.w 0xff708a:l
m68k_027074_end:
.org 0x2707A
m68k_02707a:
        cmpi.b #0x3,0xff700a:l
m68k_02707a_end:
.org 0x27082
m68k_027082:
        beq.w (. + 2774)
m68k_027082_end:
.org 0x27086
m68k_027086:
        lea.l 0xff705c:l,%a0
m68k_027086_end:
.org 0x2708C
m68k_02708c:
        bsr.w (. + 2394)
m68k_02708c_end:
.org 0x27090
m68k_027090:
        bsr.w (. + 3436)
m68k_027090_end:
.org 0x27094
m68k_027094:
        tst.w 0xff700c:l
m68k_027094_end:
.org 0x2709A
m68k_02709a:
        bne.b (. + -58)
m68k_02709a_end:
.org 0x2709C
m68k_02709c:
        lea.l 4430(%pc),%a0
m68k_02709c_end:
.org 0x270A0
m68k_0270a0:
        nop
m68k_0270a0_end:
.org 0x270A2
m68k_0270a2:
        move.w #0xed08,%d2
m68k_0270a2_end:
.org 0x270A6
m68k_0270a6:
        move.l #0x60000004,%d0
m68k_0270a6_end:
.org 0x270AC
m68k_0270ac:
        move.w #0x1,%d1
m68k_0270ac_end:
.org 0x270B0
m68k_0270b0:
        jsr 0x26bfa:l
m68k_0270b0_end:
.org 0x270B6
m68k_0270b6:
        bsr.w (. + 2352)
m68k_0270b6_end:
.org 0x270BA
m68k_0270ba:
        andi.w #0xf0,%d0
m68k_0270ba_end:
.org 0x270BE
m68k_0270be:
        beq.b (. + -94)
m68k_0270be_end:
.org 0x270C0
m68k_0270c0:
        move.w #0xac,%d0
m68k_0270c0_end:
.org 0x270C4
m68k_0270c4:
        jsr 0x808a:l
m68k_0270c4_end:
.org 0x270CA
m68k_0270ca:
        cmpi.b #0x3,0xff700a:l
m68k_0270ca_end:
.org 0x270D2
m68k_0270d2:
        beq.w (. + 128)
m68k_0270d2_end:
.org 0x270D6
m68k_0270d6:
        bsr.w (. + 3232)
m68k_0270d6_end:
.org 0x270DA
m68k_0270da:
        move.w #0xc600,0xff700c:l
m68k_0270da_end:
.org 0x270E2
m68k_0270e2:
        move.l #0x2890a,0xff700e:l
m68k_0270e2_end:
.org 0x270EC
m68k_0270ec:
        move.w #0x1,0xff7014:l
m68k_0270ec_end:
.org 0x270F4
m68k_0270f4:
        move.w #0x2,0xff7016:l
m68k_0270f4_end:
.org 0x270FC
m68k_0270fc:
        move.w #0x2500,%sr
m68k_0270fc_end:
.org 0x27100
m68k_027100:
        move.w #0x700,0xf612:w
m68k_027100_end:
.org 0x27106
m68k_027106:
        tst.b 0xf612:w
m68k_027106_end:
.org 0x2710A
m68k_02710a:
        bne.b (. + -4)
m68k_02710a_end:
.org 0x2710C
m68k_02710c:
        jsr -904(%pc)
m68k_02710c_end:
.org 0x27110
m68k_027110:
        bsr.w (. + 2420)
m68k_027110_end:
.org 0x27114
m68k_027114:
        lea.l 0xff7092:l,%a0
m68k_027114_end:
.org 0x2711A
m68k_02711a:
        bsr.w (. + 2252)
m68k_02711a_end:
.org 0x2711E
m68k_02711e:
        bsr.w (. + 3198)
m68k_02711e_end:
.org 0x27122
m68k_027122:
        tst.w 0xff700c:l
m68k_027122_end:
.org 0x27128
m68k_027128:
        bne.b (. + -40)
m68k_027128_end:
.org 0x2712A
m68k_02712a:
        bsr.w (. + 2236)
m68k_02712a_end:
.org 0x2712E
m68k_02712e:
        andi.w #0xf0,%d0
m68k_02712e_end:
.org 0x27132
m68k_027132:
        beq.b (. + -50)
m68k_027132_end:
.org 0x27134
m68k_027134:
        move.w #0xac,%d0
m68k_027134_end:
.org 0x27138
m68k_027138:
        jsr 0x808a:l
m68k_027138_end:
.org 0x2713E
m68k_02713e:
        lea.l 0xff7092:l,%a0
m68k_02713e_end:
.org 0x27144
m68k_027144:
        tst.w (%a0)
m68k_027144_end:
.org 0x27146
m68k_027146:
        beq.w (. + 12)
m68k_027146_end:
.org 0x2714A
m68k_02714a:
        move.b #0x3,0xff700a:l
m68k_02714a_end:
.org 0x27152
m68k_027152:
        move.w #0x2700,%sr
m68k_027152_end:
.org 0x27156
m68k_027156:
        lea.l 0xff7050:l,%a0
m68k_027156_end:
.org 0x2715C
m68k_02715c:
        bsr.w (. + 2270)
m68k_02715c_end:
.org 0x27160
m68k_027160:
        bsr.w (. + 3094)
m68k_027160_end:
.org 0x27164
m68k_027164:
        cmpi.b #0x3,0xff700b:l
m68k_027164_end:
.org 0x2716C
m68k_02716c:
        beq.w (. + 46)
m68k_02716c_end:
.org 0x27170
m68k_027170:
        move.w #0xc600,0xff700c:l
m68k_027170_end:
.org 0x27178
m68k_027178:
        move.l #0x288be,0xff700e:l
m68k_027178_end:
.org 0x27182
m68k_027182:
        move.w #0x1,0xff7014:l
m68k_027182_end:
.org 0x2718A
m68k_02718a:
        move.w #0x2,0xff7016:l
m68k_02718a_end:
.org 0x27192
m68k_027192:
        move.w #0x1,0xff70da:l
m68k_027192_end:
.org 0x2719A
m68k_02719a:
        move.w #0x2500,%sr
m68k_02719a_end:
.org 0x2719E
m68k_02719e:
        move.w #0x700,0xf612:w
m68k_02719e_end:
.org 0x271A4
m68k_0271a4:
        tst.b 0xf612:w
m68k_0271a4_end:
.org 0x271A8
m68k_0271a8:
        bne.b (. + -4)
m68k_0271a8_end:
.org 0x271AA
m68k_0271aa:
        jsr -1062(%pc)
m68k_0271aa_end:
.org 0x271AE
m68k_0271ae:
        bsr.w (. + 2262)
m68k_0271ae_end:
.org 0x271B2
m68k_0271b2:
        cmpi.b #0x3,0xff700b:l
m68k_0271b2_end:
.org 0x271BA
m68k_0271ba:
        beq.w (. + 2472)
m68k_0271ba_end:
.org 0x271BE
m68k_0271be:
        lea.l 0xff70ac:l,%a0
m68k_0271be_end:
.org 0x271C4
m68k_0271c4:
        bsr.w (. + 2124)
m68k_0271c4_end:
.org 0x271C8
m68k_0271c8:
        bsr.w (. + 3134)
m68k_0271c8_end:
.org 0x271CC
m68k_0271cc:
        tst.w 0xff700c:l
m68k_0271cc_end:
.org 0x271D2
m68k_0271d2:
        bne.b (. + -52)
m68k_0271d2_end:
.org 0x271D4
m68k_0271d4:
        lea.l 4140(%pc),%a0
m68k_0271d4_end:
.org 0x271D8
m68k_0271d8:
        nop
m68k_0271d8_end:
.org 0x271DA
m68k_0271da:
        move.w #0xed44,%d2
m68k_0271da_end:
.org 0x271DE
m68k_0271de:
        move.l #0x60000004,%d0
m68k_0271de_end:
.org 0x271E4
m68k_0271e4:
        move.w #0x1,%d1
m68k_0271e4_end:
.org 0x271E8
m68k_0271e8:
        jsr 0x26bfa:l
m68k_0271e8_end:
.org 0x271EE
m68k_0271ee:
        bsr.w (. + 2082)
m68k_0271ee_end:
.org 0x271F2
m68k_0271f2:
        andi.w #0xf0,%d0
m68k_0271f2_end:
.org 0x271F6
m68k_0271f6:
        beq.b (. + -88)
m68k_0271f6_end:
.org 0x271F8
m68k_0271f8:
        move.w #0xac,%d0
m68k_0271f8_end:
.org 0x271FC
m68k_0271fc:
        jsr 0x808a:l
m68k_0271fc_end:
.org 0x27202
m68k_027202:
        cmpi.b #0x3,0xff700b:l
m68k_027202_end:
.org 0x2720A
m68k_02720a:
        beq.w (. + 128)
m68k_02720a_end:
.org 0x2720E
m68k_02720e:
        bsr.w (. + 2920)
m68k_02720e_end:
.org 0x27212
m68k_027212:
        move.w #0xc600,0xff700c:l
m68k_027212_end:
.org 0x2721A
m68k_02721a:
        move.l #0x2890a,0xff700e:l
m68k_02721a_end:
.org 0x27224
m68k_027224:
        move.w #0x1,0xff7014:l
m68k_027224_end:
.org 0x2722C
m68k_02722c:
        move.w #0x2,0xff7016:l
m68k_02722c_end:
.org 0x27234
m68k_027234:
        move.w #0x2500,%sr
m68k_027234_end:
.org 0x27238
m68k_027238:
        move.w #0x700,0xf612:w
m68k_027238_end:
.org 0x2723E
m68k_02723e:
        tst.b 0xf612:w
m68k_02723e_end:
.org 0x27242
m68k_027242:
        bne.b (. + -4)
m68k_027242_end:
.org 0x27244
m68k_027244:
        jsr -1216(%pc)
m68k_027244_end:
.org 0x27248
m68k_027248:
        bsr.w (. + 2108)
m68k_027248_end:
.org 0x2724C
m68k_02724c:
        lea.l 0xff70e2:l,%a0
m68k_02724c_end:
.org 0x27252
m68k_027252:
        bsr.w (. + 1982)
m68k_027252_end:
.org 0x27256
m68k_027256:
        bsr.w (. + 2886)
m68k_027256_end:
.org 0x2725A
m68k_02725a:
        tst.w 0xff700c:l
m68k_02725a_end:
.org 0x27260
m68k_027260:
        bne.b (. + -40)
m68k_027260_end:
.org 0x27262
m68k_027262:
        bsr.w (. + 1966)
m68k_027262_end:
.org 0x27266
m68k_027266:
        andi.w #0xf0,%d0
m68k_027266_end:
.org 0x2726A
m68k_02726a:
        beq.b (. + -50)
m68k_02726a_end:
.org 0x2726C
m68k_02726c:
        move.w #0xac,%d0
m68k_02726c_end:
.org 0x27270
m68k_027270:
        jsr 0x808a:l
m68k_027270_end:
.org 0x27276
m68k_027276:
        lea.l 0xff70e2:l,%a0
m68k_027276_end:
.org 0x2727C
m68k_02727c:
        tst.w (%a0)
m68k_02727c_end:
.org 0x2727E
m68k_02727e:
        beq.w (. + 12)
m68k_02727e_end:
.org 0x27282
m68k_027282:
        move.b #0x3,0xff700b:l
m68k_027282_end:
.org 0x2728A
m68k_02728a:
        move.w #0x2700,%sr
m68k_02728a_end:
.org 0x2728E
m68k_02728e:
        lea.l 0xff70a0:l,%a0
m68k_02728e_end:
.org 0x27294
m68k_027294:
        bsr.w (. + 1958)
m68k_027294_end:
.org 0x27298
m68k_027298:
        bsr.w (. + 2782)
m68k_027298_end:
.org 0x2729C
m68k_02729c:
        jsr 0x83d4:l
m68k_02729c_end:
.org 0x272A2
m68k_0272a2:
        andi.w #0x3,%d0
m68k_0272a2_end:
.org 0x272A6
m68k_0272a6:
        cmpi.w #0x3,%d0
m68k_0272a6_end:
.org 0x272AA
m68k_0272aa:
        bne.b (. + 4)
m68k_0272aa_end:
.org 0x272AC
m68k_0272ac:
        clr.w %d0
m68k_0272ac_end:
.org 0x272AE
m68k_0272ae:
        jsr 3960(%pc)
m68k_0272ae_end:
.org 0x272B2
m68k_0272b2:
        nop
m68k_0272b2_end:
.org 0x272B4
m68k_0272b4:
        move.w #0xa5,%d0
m68k_0272b4_end:
.org 0x272B8
m68k_0272b8:
        jsr 0x808a:l
m68k_0272b8_end:
.org 0x272BE
m68k_0272be:
        clr.w 0xff7052:l
m68k_0272be_end:
.org 0x272C4
m68k_0272c4:
        move.w #0x2500,%sr
m68k_0272c4_end:
.org 0x272C8
m68k_0272c8:
        move.w #0x700,0xf612:w
m68k_0272c8_end:
.org 0x272CE
m68k_0272ce:
        tst.b 0xf612:w
m68k_0272ce_end:
.org 0x272D2
m68k_0272d2:
        bne.b (. + -4)
m68k_0272d2_end:
.org 0x272D4
m68k_0272d4:
        jsr -1360(%pc)
m68k_0272d4_end:
.org 0x272D8
m68k_0272d8:
        bsr.w (. + 1964)
m68k_0272d8_end:
.org 0x272DC
m68k_0272dc:
        tst.w 0xff700c:l
m68k_0272dc_end:
.org 0x272E2
m68k_0272e2:
        bne.b (. + -26)
m68k_0272e2_end:
.org 0x272E4
m68k_0272e4:
        bsr.w (. + 1794)
m68k_0272e4_end:
.org 0x272E8
m68k_0272e8:
        andi.w #0xf0,%d0
m68k_0272e8_end:
.org 0x272EC
m68k_0272ec:
        beq.b (. + -36)
m68k_0272ec_end:
.org 0x272EE
m68k_0272ee:
        move.w #0x2700,%sr
m68k_0272ee_end:
.org 0x272F2
m68k_0272f2:
        bsr.w (. + 2692)
m68k_0272f2_end:
.org 0x272F6
m68k_0272f6:
        jsr 0x83d4:l
m68k_0272f6_end:
.org 0x272FC
m68k_0272fc:
        andi.w #0x3,%d0
m68k_0272fc_end:
.org 0x27300
m68k_027300:
        cmpi.w #0x3,%d0
m68k_027300_end:
.org 0x27304
m68k_027304:
        bne.b (. + 4)
m68k_027304_end:
.org 0x27306
m68k_027306:
        clr.w %d0
m68k_027306_end:
.org 0x27308
m68k_027308:
        addq.w #0x3,%d0
m68k_027308_end:
.org 0x2730A
m68k_02730a:
        jsr 3868(%pc)
m68k_02730a_end:
.org 0x2730E
m68k_02730e:
        nop
m68k_02730e_end:
.org 0x27310
m68k_027310:
        move.w #0xa5,%d0
m68k_027310_end:
.org 0x27314
m68k_027314:
        jsr 0x808a:l
m68k_027314_end:
.org 0x2731A
m68k_02731a:
        clr.w 0xff70a2:l
m68k_02731a_end:
.org 0x27320
m68k_027320:
        move.w #0x2500,%sr
m68k_027320_end:
.org 0x27324
m68k_027324:
        move.w #0x700,0xf612:w
m68k_027324_end:
.org 0x2732A
m68k_02732a:
        tst.b 0xf612:w
m68k_02732a_end:
.org 0x2732E
m68k_02732e:
        bne.b (. + -4)
m68k_02732e_end:
.org 0x27330
m68k_027330:
        bsr.w (. + 1876)
m68k_027330_end:
.org 0x27334
m68k_027334:
        tst.w 0xff700c:l
m68k_027334_end:
.org 0x2733A
m68k_02733a:
        bne.b (. + -22)
m68k_02733a_end:
.org 0x2733C
m68k_02733c:
        bsr.w (. + 1748)
m68k_02733c_end:
.org 0x27340
m68k_027340:
        andi.w #0xf0,%d0
m68k_027340_end:
.org 0x27344
m68k_027344:
        beq.b (. + -32)
m68k_027344_end:
.org 0x27346
m68k_027346:
        move.w #0x8b,%d0
m68k_027346_end:
.org 0x2734A
m68k_02734a:
        jsr 0x808a:l
m68k_02734a_end:
.org 0x27350
m68k_027350:
        move.w #0x2700,%sr
m68k_027350_end:
.org 0x27354
m68k_027354:
        bsr.w (. + 2594)
m68k_027354_end:
.org 0x27358
m68k_027358:
        move.w #0x2500,%sr
m68k_027358_end:
.org 0x2735C
m68k_02735c:
        move.w #0x700,0xf612:w
m68k_02735c_end:
.org 0x27362
m68k_027362:
        tst.b 0xf612:w
m68k_027362_end:
.org 0x27366
m68k_027366:
        bne.b (. + -4)
m68k_027366_end:
.org 0x273C4
m68k_0273c4:
        bsr.w (. + 322)
m68k_0273c4_end:
.org 0x273C8
m68k_0273c8:
        clr.w 0xff7018:l
m68k_0273c8_end:
.org 0x273CE
m68k_0273ce:
        tst.w 0xff706c:l
m68k_0273ce_end:
.org 0x273D4
m68k_0273d4:
        beq.w (. + 1468)
m68k_0273d4_end:
.org 0x273D8
m68k_0273d8:
        move.w #0x8000,0xff7018:l
m68k_0273d8_end:
.org 0x273E0
m68k_0273e0:
        tst.w 0xff70bc:l
m68k_0273e0_end:
.org 0x273E6
m68k_0273e6:
        beq.w (. + 1450)
m68k_0273e6_end:
.org 0x273EA
m68k_0273ea:
        move.w 0xff7052:l,%d1
m68k_0273ea_end:
.org 0x273F0
m68k_0273f0:
        or.w 0xff70a2:l,%d1
m68k_0273f0_end:
.org 0x273F6
m68k_0273f6:
        andi.w #0xd000,%d1
m68k_0273f6_end:
.org 0x273FA
m68k_0273fa:
        bne.w (. + -158)
m68k_0273fa_end:
.org 0x273FE
m68k_0273fe:
        clr.w 0xff7018:l
m68k_0273fe_end:
.org 0x27404
m68k_027404:
        move.w 0xff7050:l,%d0
m68k_027404_end:
.org 0x2740A
m68k_02740a:
        andi.w #0x40,%d0
m68k_02740a_end:
.org 0x2740E
m68k_02740e:
        bne.b (. + 24)
m68k_02740e_end:
.org 0x27410
m68k_027410:
        move.w #0x8000,0xff7018:l
m68k_027410_end:
.org 0x27418
m68k_027418:
        move.w 0xff70a0:l,%d0
m68k_027418_end:
.org 0x2741E
m68k_02741e:
        andi.w #0x40,%d0
m68k_02741e_end:
.org 0x27422
m68k_027422:
        beq.w (. + -198)
m68k_027422_end:
.org 0x27426
m68k_027426:
        move.w #0x2700,%sr
m68k_027426_end:
.org 0x2742A
m68k_02742a:
        clr.w 0xd100:w
m68k_02742a_end:
.org 0x2742E
m68k_02742e:
        tst.w 0xff7018:l
m68k_02742e_end:
.org 0x27434
m68k_027434:
        bmi.b (. + 32)
m68k_027434_end:
.org 0x27436
m68k_027436:
        cmpi.b #0x3,0xff700a:l
m68k_027436_end:
.org 0x2743E
m68k_02743e:
        bne.b (. + 52)
m68k_02743e_end:
.org 0x27440
m68k_027440:
        move.w 0xff7050:l,%d0
m68k_027440_end:
.org 0x27446
m68k_027446:
        andi.w #0x3,%d0
m68k_027446_end:
.org 0x2744A
m68k_02744a:
        move.b %d0,0xff7019:l
m68k_02744a_end:
.org 0x27450
m68k_027450:
        bra.w (. + 228)
m68k_027450_end:
.org 0x27454
m68k_027454:
        cmpi.b #0x3,0xff700b:l
m68k_027454_end:
.org 0x2745C
m68k_02745c:
        bne.b (. + 38)
m68k_02745c_end:
.org 0x2745E
m68k_02745e:
        move.w 0xff70a0:l,%d0
m68k_02745e_end:
.org 0x27464
m68k_027464:
        andi.w #0x3,%d0
m68k_027464_end:
.org 0x27468
m68k_027468:
        move.b %d0,0xff7019:l
m68k_027468_end:
.org 0x2746E
m68k_02746e:
        bra.w (. + 198)
m68k_02746e_end:
.org 0x27472
m68k_027472:
        move.w 0xff706a:l,%d1
m68k_027472_end:
.org 0x27478
m68k_027478:
        cmp.w 0xff7070:l,%d1
m68k_027478_end:
.org 0x2747E
m68k_02747e:
        beq.b (. + 20)
m68k_02747e_end:
.org 0x27480
m68k_027480:
        bra.b (. + 38)
m68k_027480_end:
.org 0x27482
m68k_027482:
        move.w 0xff70ba:l,%d1
m68k_027482_end:
.org 0x27488
m68k_027488:
        cmp.w 0xff70c0:l,%d1
m68k_027488_end:
.org 0x2748E
m68k_02748e:
        beq.b (. + 4)
m68k_02748e_end:
.org 0x27490
m68k_027490:
        bra.b (. + 22)
m68k_027490_end:
.org 0x27492
m68k_027492:
        move.w #0xcb80,0xff700c:l
m68k_027492_end:
.org 0x2749A
m68k_02749a:
        move.l #0x28924,0xff700e:l
m68k_02749a_end:
.org 0x274A4
m68k_0274a4:
        bra.b (. + 20)
m68k_0274a4_end:
.org 0x274A6
m68k_0274a6:
        move.w #0xc740,0xff700c:l
m68k_0274a6_end:
.org 0x274AE
m68k_0274ae:
        move.l #0x288ea,0xff700e:l
m68k_0274ae_end:
.org 0x274B8
m68k_0274b8:
        move.w #0xad,%d0
m68k_0274b8_end:
.org 0x274BC
m68k_0274bc:
        jsr 0x808a:l
m68k_0274bc_end:
.org 0x274C2
m68k_0274c2:
        move.w #0x2500,%sr
m68k_0274c2_end:
.org 0x274C6
m68k_0274c6:
        move.w #0x700,0xf612:w
m68k_0274c6_end:
.org 0x274CC
m68k_0274cc:
        tst.b 0xf612:w
m68k_0274cc_end:
.org 0x274D0
m68k_0274d0:
        bne.b (. + -4)
m68k_0274d0_end:
.org 0x274D2
m68k_0274d2:
        bsr.w (. + 1458)
m68k_0274d2_end:
.org 0x274D6
m68k_0274d6:
        bsr.w (. + 1296)
m68k_0274d6_end:
.org 0x274DA
m68k_0274da:
        tst.w 0xff7018:l
m68k_0274da_end:
.org 0x274E0
m68k_0274e0:
        bpl.b (. + 6)
m68k_0274e0_end:
.org 0x274E2
m68k_0274e2:
        bsr.w (. + 1326)
m68k_0274e2_end:
.org 0x274E6
m68k_0274e6:
        move.w %d0,-(%a7)
m68k_0274e6_end:
.org 0x274E8
m68k_0274e8:
        bsr.w (. + 2538)
m68k_0274e8_end:
.org 0x274EC
m68k_0274ec:
        move.w (%a7)+,%d0
m68k_0274ec_end:
.org 0x274EE
m68k_0274ee:
        tst.w 0xff700c:l
m68k_0274ee_end:
.org 0x274F4
m68k_0274f4:
        bne.b (. + -46)
m68k_0274f4_end:
.org 0x274F6
m68k_0274f6:
        btst.l #0x5,%d0
m68k_0274f6_end:
.org 0x274FA
m68k_0274fa:
        bne.b (. + 58)
m68k_0274fa_end:
.org 0x274FC
m68k_0274fc:
        btst.l #0x4,%d0
m68k_0274fc_end:
.org 0x27500
m68k_027500:
        beq.b (. + -58)
m68k_027500_end:
.org 0x27502
m68k_027502:
        bra.w (. + -434)
m68k_027502_end:
.org 0x27506
m68k_027506:
        lea.l 3224(%pc),%a0
m68k_027506_end:
.org 0x2750A
m68k_02750a:
        nop
m68k_02750a_end:
.org 0x2750C
m68k_02750c:
        move.w #0xec08,%d2
m68k_02750c_end:
.org 0x27510
m68k_027510:
        move.w 0xff7008:l,%d0
m68k_027510_end:
.org 0x27516
m68k_027516:
        andi.w #0x1,%d0
m68k_027516_end:
.org 0x2751A
m68k_02751a:
        beq.b (. + 12)
m68k_02751a_end:
.org 0x2751C
m68k_02751c:
        lea.l 3224(%pc),%a0
m68k_02751c_end:
.org 0x27520
m68k_027520:
        nop
m68k_027520_end:
.org 0x27522
m68k_027522:
        move.w #0xec44,%d2
m68k_027522_end:
.org 0x27526
m68k_027526:
        move.l #0x60000004,%d0
m68k_027526_end:
.org 0x2752C
m68k_02752c:
        move.w #0x1,%d1
m68k_02752c_end:
.org 0x27530
m68k_027530:
        bra.w (. + -2358)
m68k_027530_end:
.org 0x27534
m68k_027534:
        move.w #0xac,%d0
m68k_027534_end:
.org 0x27538
m68k_027538:
        jsr 0x808a:l
m68k_027538_end:
.org 0x2753E
m68k_02753e:
        move.w #0x2700,%sr
m68k_02753e_end:
.org 0x27542
m68k_027542:
        bsr.w (. + 2100)
m68k_027542_end:
.org 0x27546
m68k_027546:
        lea.l 0xff7050:l,%a0
m68k_027546_end:
.org 0x2754C
m68k_02754c:
        lea.l 0xff70a0:l,%a1
m68k_02754c_end:
.org 0x27552
m68k_027552:
        tst.w 0xff7018:l
m68k_027552_end:
.org 0x27558
m68k_027558:
        bpl.b (. + 14)
m68k_027558_end:
.org 0x2755A
m68k_02755a:
        lea.l 0xff70a0:l,%a0
m68k_02755a_end:
.org 0x27560
m68k_027560:
        lea.l 0xff7050:l,%a1
m68k_027560_end:
.org 0x27566
m68k_027566:
        move.w 0xff7018:l,%d0
m68k_027566_end:
.org 0x2756C
m68k_02756c:
        asl.w #0x2,%d0
m68k_02756c_end:
.org 0x2756E
m68k_02756e:
        jsr 6(%pc, %d0.w)
m68k_02756e_end:
.org 0x27572
m68k_027572:
        bra.w (. + -546)
m68k_027572_end:
.org 0x2777A
m68k_02777a:
        move.w #0x2500,%sr
m68k_02777a_end:
.org 0x2777E
m68k_02777e:
        move.w #0x700,0xf612:w
m68k_02777e_end:
.org 0x27784
m68k_027784:
        tst.b 0xf612:w
m68k_027784_end:
.org 0x27788
m68k_027788:
        bne.b (. + -4)
m68k_027788_end:
.org 0x2778A
m68k_02778a:
        subq.w #0x1,0xff70fa:l
m68k_02778a_end:
.org 0x27790
m68k_027790:
        bsr.w (. + 756)
m68k_027790_end:
.org 0x27794
m68k_027794:
        tst.w 0xff700c:l
m68k_027794_end:
.org 0x2779A
m68k_02779a:
        bne.b (. + -28)
m68k_02779a_end:
.org 0x2779C
m68k_02779c:
        bsr.w (. + 586)
m68k_02779c_end:
.org 0x277A0
m68k_0277a0:
        tst.w 0xff7018:l
m68k_0277a0_end:
.org 0x277A6
m68k_0277a6:
        bpl.b (. + 6)
m68k_0277a6_end:
.org 0x277A8
m68k_0277a8:
        bsr.w (. + 616)
m68k_0277a8_end:
.org 0x277AC
m68k_0277ac:
        andi.w #0x70,%d0
m68k_0277ac_end:
.org 0x277B0
m68k_0277b0:
        beq.b (. + -50)
m68k_0277b0_end:
.org 0x277B2
m68k_0277b2:
        move.w #0x2700,%sr
m68k_0277b2_end:
.org 0x277B6
m68k_0277b6:
        rts
m68k_0277b6_end:
.org 0x277B8
m68k_0277b8:
        cmpi.b #0x3,0xff700a:l
m68k_0277b8_end:
.org 0x277C0
m68k_0277c0:
        beq.w (. + -70)
m68k_0277c0_end:
.org 0x277C4
m68k_0277c4:
        cmpi.b #0x3,0xff700b:l
m68k_0277c4_end:
.org 0x277CC
m68k_0277cc:
        beq.w (. + -82)
m68k_0277cc_end:
.org 0x277D0
m68k_0277d0:
        move.w #0x2500,%sr
m68k_0277d0_end:
.org 0x277D4
m68k_0277d4:
        move.w #0x700,0xf612:w
m68k_0277d4_end:
.org 0x277DA
m68k_0277da:
        tst.b 0xf612:w
m68k_0277da_end:
.org 0x277DE
m68k_0277de:
        bne.b (. + -4)
m68k_0277de_end:
.org 0x277E0
m68k_0277e0:
        subq.w #0x1,0xff70fa:l
m68k_0277e0_end:
.org 0x277E6
m68k_0277e6:
        bsr.w (. + 670)
m68k_0277e6_end:
.org 0x277EA
m68k_0277ea:
        tst.w 0xff700c:l
m68k_0277ea_end:
.org 0x277F0
m68k_0277f0:
        bne.b (. + -28)
m68k_0277f0_end:
.org 0x277F2
m68k_0277f2:
        bsr.w (. + 500)
m68k_0277f2_end:
.org 0x277F6
m68k_0277f6:
        move.w %d0,%d1
m68k_0277f6_end:
.org 0x277F8
m68k_0277f8:
        movem.l %d1,-(%a7)
m68k_0277f8_end:
.org 0x277FC
m68k_0277fc:
        bsr.w (. + 532)
m68k_0277fc_end:
.org 0x27800
m68k_027800:
        movem.l (%a7)+,%d1
m68k_027800_end:
.org 0x27804
m68k_027804:
        or.w %d1,%d0
m68k_027804_end:
.org 0x27806
m68k_027806:
        andi.w #0x70,%d0
m68k_027806_end:
.org 0x2780A
m68k_02780a:
        beq.b (. + -54)
m68k_02780a_end:
.org 0x2780C
m68k_02780c:
        move.w #0x2700,%sr
m68k_02780c_end:
.org 0x27810
m68k_027810:
        rts
m68k_027810_end:
.org 0x27990
m68k_027990:
        move.w #0x700,0xf612:w
m68k_027990_end:
.org 0x27996
m68k_027996:
        tst.b 0xf612:w
m68k_027996_end:
.org 0x2799A
m68k_02799a:
        bne.b (. + -4)
m68k_02799a_end:
.org 0x2799C
m68k_02799c:
        bsr.w (. + -1174)
m68k_02799c_end:
.org 0x279A0
m68k_0279a0:
        move.w #0x700,0xf612:w
m68k_0279a0_end:
.org 0x279A6
m68k_0279a6:
        tst.b 0xf612:w
m68k_0279a6_end:
.org 0x279AA
m68k_0279aa:
        bne.b (. + -4)
m68k_0279aa_end:
.org 0x279AC
m68k_0279ac:
        move.w #0x2700,%sr
m68k_0279ac_end:
.org 0x279B0
m68k_0279b0:
        move.w #0x1f,%d0
m68k_0279b0_end:
.org 0x279B4
m68k_0279b4:
        tst.w 0xff7018:l
m68k_0279b4_end:
.org 0x279BA
m68k_0279ba:
        bpl.b (. + 6)
m68k_0279ba_end:
.org 0x279BC
m68k_0279bc:
        move.w #0x22,%d0
m68k_0279bc_end:
.org 0x279C0
m68k_0279c0:
        bsr.w (. + 2152)
m68k_0279c0_end:
.org 0x279C4
m68k_0279c4:
        bsr.w (. + -586)
m68k_0279c4_end:
.org 0x279C8
m68k_0279c8:
        bsr.w (. + 942)
m68k_0279c8_end:
.org 0x279CC
m68k_0279cc:
        move.w #0x20,%d0
m68k_0279cc_end:
.org 0x279D0
m68k_0279d0:
        tst.w 0xff7018:l
m68k_0279d0_end:
.org 0x279D6
m68k_0279d6:
        bpl.b (. + 4)
m68k_0279d6_end:
.org 0x279D8
m68k_0279d8:
        addq.w #0x1,%d0
m68k_0279d8_end:
.org 0x279DA
m68k_0279da:
        bsr.w (. + 2126)
m68k_0279da_end:
.org 0x279DE
m68k_0279de:
        bsr.w (. + -550)
m68k_0279de_end:
.org 0x279E2
m68k_0279e2:
        bra.w (. + -3228)
m68k_0279e2_end:
.org 0x279E6
m68k_0279e6:
        move.w 0xf602:w,%d0
m68k_0279e6_end:
.org 0x279EA
m68k_0279ea:
        move.b 0xff700a:l,%d1
m68k_0279ea_end:
.org 0x279F0
m68k_0279f0:
        tst.b %d1
m68k_0279f0_end:
.org 0x279F2
m68k_0279f2:
        beq.b (. + 28)
m68k_0279f2_end:
.org 0x279F4
m68k_0279f4:
        move.w 0xf604:w,%d0
m68k_0279f4_end:
.org 0x279F8
m68k_0279f8:
        cmpi.b #0x1,%d1
m68k_0279f8_end:
.org 0x279FC
m68k_0279fc:
        beq.b (. + 18)
m68k_0279fc_end:
.org 0x279FE
m68k_0279fe:
        move.b 0xff700b:l,%d1
m68k_0279fe_end:
.org 0x27A04
m68k_027a04:
        cmpi.b #0x1,%d1
m68k_027a04_end:
.org 0x27A08
m68k_027a08:
        beq.b (. + 6)
m68k_027a08_end:
.org 0x27A0A
m68k_027a0a:
        move.w 0xf602:w,%d0
m68k_027a0a_end:
.org 0x27A0E
m68k_027a0e:
        rts
m68k_027a0e_end:
.org 0x27A10
m68k_027a10:
        move.w 0xf602:w,%d0
m68k_027a10_end:
.org 0x27A14
m68k_027a14:
        move.b 0xff700b:l,%d1
m68k_027a14_end:
.org 0x27A1A
m68k_027a1a:
        tst.b %d1
m68k_027a1a_end:
.org 0x27A1C
m68k_027a1c:
        beq.b (. + 28)
m68k_027a1c_end:
.org 0x27A1E
m68k_027a1e:
        move.w 0xf604:w,%d0
m68k_027a1e_end:
.org 0x27A22
m68k_027a22:
        cmpi.b #0x1,%d1
m68k_027a22_end:
.org 0x27A26
m68k_027a26:
        beq.b (. + 18)
m68k_027a26_end:
.org 0x27A28
m68k_027a28:
        move.b 0xff700a:l,%d1
m68k_027a28_end:
.org 0x27A2E
m68k_027a2e:
        cmpi.b #0x1,%d1
m68k_027a2e_end:
.org 0x27A32
m68k_027a32:
        beq.b (. + 6)
m68k_027a32_end:
.org 0x27A34
m68k_027a34:
        move.w 0xf602:w,%d0
m68k_027a34_end:
.org 0x27A38
m68k_027a38:
        rts
m68k_027a38_end:
.org 0x27A3A
m68k_027a3a:
        move.w 0x1e(%a0),%d0
m68k_027a3a_end:
.org 0x27A3E
m68k_027a3e:
        move.w 0xc(%a0),%d1
m68k_027a3e_end:
.org 0x27A42
m68k_027a42:
        asl.w #0x1,%d1
m68k_027a42_end:
.org 0x27A44
m68k_027a44:
        sub.w 56(%pc, %d1.w),%d0
m68k_027a44_end:
.org 0x27A48
m68k_027a48:
        bcc.b (. + 8)
m68k_027a48_end:
.org 0x27A4A
m68k_027a4a:
        clr.w %d0
m68k_027a4a_end:
.org 0x27A4C
m68k_027a4c:
        bra.w (. + 14)
m68k_027a4c_end:
.org 0x27A50
m68k_027a50:
        cmpi.w #0x50,%d0
m68k_027a50_end:
.org 0x27A54
m68k_027a54:
        bcs.b (. + 6)
m68k_027a54_end:
.org 0x27A56
m68k_027a56:
        move.w #0x50,%d0
m68k_027a56_end:
.org 0x27A5A
m68k_027a5a:
        move.w #0x50,%d1
m68k_027a5a_end:
.org 0x27A5E
m68k_027a5e:
        sub.w %d0,%d1
m68k_027a5e_end:
.org 0x27A60
m68k_027a60:
        mulu.w #0x700,%d0
m68k_027a60_end:
.org 0x27A64
m68k_027a64:
        addi.l #0x6000,%d0
m68k_027a64_end:
.org 0x27A6A
m68k_027a6a:
        move.l %d0,0x12(%a0)
m68k_027a6a_end:
.org 0x27A6E
m68k_027a6e:
        andi.l #0xffff,%d1
m68k_027a6e_end:
.org 0x27A74
m68k_027a74:
        divu.w #0x2,%d1
m68k_027a74_end:
.org 0x27A78
m68k_027a78:
        move.w %d1,0x16(%a0)
m68k_027a78_end:
.org 0x27A7C
m68k_027a7c:
        rts
m68k_027a7c_end:
.org 0x27A84
m68k_027a84:
        movem.l %a0-%a1,-(%a7)
m68k_027a84_end:
.org 0x27A88
m68k_027a88:
        move.w #0x0,0xff7050:l
m68k_027a88_end:
.org 0x27A90
m68k_027a90:
        lea.l 0xff7050:l,%a0
m68k_027a90_end:
.org 0x27A96
m68k_027a96:
        lea.l 0xff70a0:l,%a1
m68k_027a96_end:
.org 0x27A9C
m68k_027a9c:
        bsr.w (. + 5072)
m68k_027a9c_end:
.org 0x27AA0
m68k_027aa0:
        move.w #0x0,0xff70a0:l
m68k_027aa0_end:
.org 0x27AA8
m68k_027aa8:
        lea.l 0xff70a0:l,%a0
m68k_027aa8_end:
.org 0x27AAE
m68k_027aae:
        lea.l 0xff7050:l,%a1
m68k_027aae_end:
.org 0x27AB4
m68k_027ab4:
        bsr.w (. + 5048)
m68k_027ab4_end:
.org 0x27AB8
m68k_027ab8:
        movem.l (%a7)+,%a0-%a1
m68k_027ab8_end:
.org 0x27ABC
m68k_027abc:
        rts
m68k_027abc_end:
.org 0x27B58
m68k_027b58:
        lea.l 0xff7050:l,%a0
m68k_027b58_end:
.org 0x27B5E
m68k_027b5e:
        bra.w (. + 10)
m68k_027b5e_end:
.org 0x27B62
m68k_027b62:
        lea.l 0xff70a0:l,%a0
m68k_027b62_end:
.org 0x27B68
m68k_027b68:
        move.w 0x1e(%a0),%d0
m68k_027b68_end:
.org 0x27B6C
m68k_027b6c:
        lea.l 40(%pc),%a2
m68k_027b6c_end:
.org 0x27B70
m68k_027b70:
        nop
m68k_027b70_end:
.org 0x27B72
m68k_027b72:
        bsr.w (. + 5150)
m68k_027b72_end:
.org 0x27B76
m68k_027b76:
        asl.w #0x1,%d1
m68k_027b76_end:
.org 0x27B78
m68k_027b78:
        movea.l 40(%pc, %d1.w),%a3
m68k_027b78_end:
.org 0x27B7C
m68k_027b7c:
        jsr (%a3)
m68k_027b7c_end:
.org 0x27B7E
m68k_027b7e:
        tst.w %d6
m68k_027b7e_end:
.org 0x27B80
m68k_027b80:
        bne.w (. + 58)
m68k_027b80_end:
.org 0x27B84
m68k_027b84:
        cmpa.l #0xff7050,%a0
m68k_027b84_end:
.org 0x27B8A
m68k_027b8a:
        bne.w (. + 8)
m68k_027b8a_end:
.org 0x27B8E
m68k_027b8e:
        bra.w (. + -2862)
m68k_027b8e_end:
.org 0x27B92
m68k_027b92:
        bra.w (. + -2312)
m68k_027b92_end:
.org 0x27BBA
m68k_027bba:
        cmpa.l #0xff7050,%a0
m68k_027bba_end:
.org 0x27BC0
m68k_027bc0:
        bne.w (. + 8)
m68k_027bc0_end:
.org 0x27BC4
m68k_027bc4:
        bra.w (. + -2674)
m68k_027bc4_end:
.org 0x27BC8
m68k_027bc8:
        bra.w (. + -2366)
m68k_027bc8_end:
.org 0x27D1C
m68k_027d1c:
        mulu.w #0x6,%d7
m68k_027d1c_end:
.org 0x27D20
m68k_027d20:
        lea.l 0x8a504:l,%a0
m68k_027d20_end:
.org 0x27D26
m68k_027d26:
        lea.l (%a0, %d7.w),%a0
m68k_027d26_end:
.org 0x27D2A
m68k_027d2a:
        move.w #0x2,%d3
m68k_027d2a_end:
.org 0x27D2E
m68k_027d2e:
        cmpi.w #0x3f,0x4(%a0)
m68k_027d2e_end:
.org 0x27D34
m68k_027d34:
        bne.b (. + 34)
m68k_027d34_end:
.org 0x27D36
m68k_027d36:
        move.w #0x1,%d3
m68k_027d36_end:
.org 0x27D3A
m68k_027d3a:
        move.w %d0,%d4
m68k_027d3a_end:
.org 0x27D3C
m68k_027d3c:
        asl.w #0x4,%d4
m68k_027d3c_end:
.org 0x27D3E
m68k_027d3e:
        or.w %d0,%d4
m68k_027d3e_end:
.org 0x27D40
m68k_027d40:
        move.w #0x3f,%d5
m68k_027d40_end:
.org 0x27D44
m68k_027d44:
        lea.l 0xd300:w,%a1
m68k_027d44_end:
.org 0x27D48
m68k_027d48:
        lea.l 0xd440:w,%a2
m68k_027d48_end:
.org 0x27D4C
m68k_027d4c:
        move.b %d4,(%a1)+
m68k_027d4c_end:
.org 0x27D4E
m68k_027d4e:
        move.b %d4,(%a2)+
m68k_027d4e_end:
.org 0x27D50
m68k_027d50:
        dbra %d5,(. + -4)
m68k_027d50_end:
.org 0x27D54
m68k_027d54:
        bra.b (. + 6)
m68k_027d54_end:
.org 0x27D56
m68k_027d56:
        lea.l 0xd300:w,%a1
m68k_027d56_end:
.org 0x27D5A
m68k_027d5a:
        jsr 0xae8a:l
m68k_027d5a_end:
.org 0x27D60
m68k_027d60:
        lea.l 0xd300:w,%a0
m68k_027d60_end:
.org 0x27D64
m68k_027d64:
        lea.l 0xc00000:l,%a6
m68k_027d64_end:
.org 0x27D6A
m68k_027d6a:
        move.w #0x5f,%d0
m68k_027d6a_end:
.org 0x27D6E
m68k_027d6e:
        move.l (%a0)+,(%a6)
m68k_027d6e_end:
.org 0x27D70
m68k_027d70:
        dbra %d0,(. + -2)
m68k_027d70_end:
.org 0x27D74
m68k_027d74:
        rts
m68k_027d74_end:
.org 0x27D76
m68k_027d76:
        clr.w 0xd100:w
m68k_027d76_end:
.org 0x27D7A
m68k_027d7a:
        move.l #0x46000003,0xc00004:l
m68k_027d7a_end:
.org 0x27D84
m68k_027d84:
        lea.l 0xc00000:l,%a6
m68k_027d84_end:
.org 0x27D8A
m68k_027d8a:
        move.l #0x11111111,%d0
m68k_027d8a_end:
.org 0x27D90
m68k_027d90:
        move.w #0x27f,%d1
m68k_027d90_end:
.org 0x27D94
m68k_027d94:
        move.l %d0,(%a6)
m68k_027d94_end:
.org 0x27D96
m68k_027d96:
        dbra %d1,(. + -2)
m68k_027d96_end:
.org 0x27D9A
m68k_027d9a:
        rts
m68k_027d9a_end:
.org 0x27D9C
m68k_027d9c:
        move.w (%a0),%d1
m68k_027d9c_end:
.org 0x27D9E
m68k_027d9e:
        andi.w #0xc,%d0
m68k_027d9e_end:
.org 0x27DA2
m68k_027da2:
        beq.b (. + 24)
m68k_027da2_end:
.org 0x27DA4
m68k_027da4:
        move.w #0x1,%d2
m68k_027da4_end:
.org 0x27DA8
m68k_027da8:
        andi.w #0x8,%d0
m68k_027da8_end:
.org 0x27DAC
m68k_027dac:
        bne.b (. + 4)
m68k_027dac_end:
.org 0x27DAE
m68k_027dae:
        neg.w %d2
m68k_027dae_end:
.org 0x27DB0
m68k_027db0:
        add.w %d2,%d1
m68k_027db0_end:
.org 0x27DB2
m68k_027db2:
        cmpi.w #0x2,%d1
m68k_027db2_end:
.org 0x27DB6
m68k_027db6:
        bcc.b (. + 4)
m68k_027db6_end:
.org 0x27DB8
m68k_027db8:
        move.w %d1,(%a0)
m68k_027db8_end:
.org 0x27DBA
m68k_027dba:
        bsr.w (. + -980)
m68k_027dba_end:
.org 0x27DBE
m68k_027dbe:
        btst.l #0x5,%d0
m68k_027dbe_end:
.org 0x27DC2
m68k_027dc2:
        bne.w (. + 50)
m68k_027dc2_end:
.org 0x27DC6
m68k_027dc6:
        andi.w #0xc,%d0
m68k_027dc6_end:
.org 0x27DCA
m68k_027dca:
        bne.w (. + 16)
m68k_027dca_end:
.org 0x27DCE
m68k_027dce:
        move.w 0xff7008:l,%d0
m68k_027dce_end:
.org 0x27DD4
m68k_027dd4:
        andi.w #0x8,%d0
m68k_027dd4_end:
.org 0x27DD8
m68k_027dd8:
        beq.b (. + 28)
m68k_027dd8_end:
.org 0x27DDA
m68k_027dda:
        move.w #0xc8,%d0
m68k_027dda_end:
.org 0x27DDE
m68k_027dde:
        move.w (%a0),%d1
m68k_027dde_end:
.org 0x27DE0
m68k_027de0:
        mulu.w #0x38,%d1
m68k_027de0_end:
.org 0x27DE4
m68k_027de4:
        addi.w #0x79,%d1
m68k_027de4_end:
.org 0x27DE8
m68k_027de8:
        move.w #0x43,%d2
m68k_027de8_end:
.org 0x27DEC
m68k_027dec:
        move.w #0x8000,%d3
m68k_027dec_end:
.org 0x27DF0
m68k_027df0:
        bsr.w (. + 4524)
m68k_027df0_end:
.org 0x27DF4
m68k_027df4:
        subq.w #0x1,0xff70fa:l
m68k_027df4_end:
.org 0x27DFA
m68k_027dfa:
        rts
m68k_027dfa_end:
.org 0x27DFC
m68k_027dfc:
        lea.l 0xff707a:l,%a3
m68k_027dfc_end:
.org 0x27E02
m68k_027e02:
        bra.w (. + 10)
m68k_027e02_end:
.org 0x27E06
m68k_027e06:
        lea.l 0xff70ca:l,%a3
m68k_027e06_end:
.org 0x27E0C
m68k_027e0c:
        move.w (%a0),%d1
m68k_027e0c_end:
.org 0x27E0E
m68k_027e0e:
        tst.w %d1
m68k_027e0e_end:
.org 0x27E10
m68k_027e10:
        bne.b (. + 20)
m68k_027e10_end:
.org 0x27E12
m68k_027e12:
        tst.w 0x2(%a3)
m68k_027e12_end:
.org 0x27E16
m68k_027e16:
        bne.b (. + 38)
m68k_027e16_end:
.org 0x27E18
m68k_027e18:
        addq.w #0x1,(%a0)
m68k_027e18_end:
.org 0x27E1A
m68k_027e1a:
        cmpi.w #0x3,(%a0)
m68k_027e1a_end:
.org 0x27E1E
m68k_027e1e:
        bcs.b (. + -18)
m68k_027e1e_end:
.org 0x27E20
m68k_027e20:
        clr.w (%a0)
m68k_027e20_end:
.org 0x27E22
m68k_027e22:
        bra.b (. + -22)
m68k_027e22_end:
.org 0x27E24
m68k_027e24:
        cmpi.w #0x1,%d1
m68k_027e24_end:
.org 0x27E28
m68k_027e28:
        bne.b (. + 12)
m68k_027e28_end:
.org 0x27E2A
m68k_027e2a:
        tst.w (%a3)
m68k_027e2a_end:
.org 0x27E2C
m68k_027e2c:
        bne.w (. + 16)
m68k_027e2c_end:
.org 0x27E30
m68k_027e30:
        bra.w (. + -24)
m68k_027e30_end:
.org 0x27E34
m68k_027e34:
        tst.w 0x4(%a3)
m68k_027e34_end:
.org 0x27E38
m68k_027e38:
        beq.w (. + -32)
m68k_027e38_end:
.org 0x27E3C
m68k_027e3c:
        move.w (%a0),%d1
m68k_027e3c_end:
.org 0x27E3E
m68k_027e3e:
        andi.w #0xc,%d0
m68k_027e3e_end:
.org 0x27E42
m68k_027e42:
        beq.b (. + 78)
m68k_027e42_end:
.org 0x27E44
m68k_027e44:
        move.w #0x1,%d2
m68k_027e44_end:
.org 0x27E48
m68k_027e48:
        andi.w #0x8,%d0
m68k_027e48_end:
.org 0x27E4C
m68k_027e4c:
        bne.b (. + 4)
m68k_027e4c_end:
.org 0x27E4E
m68k_027e4e:
        neg.w %d2
m68k_027e4e_end:
.org 0x27E50
m68k_027e50:
        add.w %d2,%d1
m68k_027e50_end:
.org 0x27E52
m68k_027e52:
        bpl.w (. + 8)
m68k_027e52_end:
.org 0x27E56
m68k_027e56:
        moveq #2,%d1
m68k_027e56_end:
.org 0x27E58
m68k_027e58:
        bra.b (. + 12)
m68k_027e58_end:
.org 0x27E5A
m68k_027e5a:
        cmpi.w #0x3,%d1
m68k_027e5a_end:
.org 0x27E5E
m68k_027e5e:
        bcs.w (. + 6)
m68k_027e5e_end:
.org 0x27E62
m68k_027e62:
        moveq #0,%d1
m68k_027e62_end:
.org 0x27E64
m68k_027e64:
        tst.w %d1
m68k_027e64_end:
.org 0x27E66
m68k_027e66:
        bne.w (. + 12)
m68k_027e66_end:
.org 0x27E6A
m68k_027e6a:
        tst.w 0x2(%a3)
m68k_027e6a_end:
.org 0x27E6E
m68k_027e6e:
        bne.b (. + 26)
m68k_027e6e_end:
.org 0x27E70
m68k_027e70:
        bra.b (. + -32)
m68k_027e70_end:
.org 0x27E72
m68k_027e72:
        cmpi.w #0x1,%d1
m68k_027e72_end:
.org 0x27E76
m68k_027e76:
        bne.w (. + 12)
m68k_027e76_end:
.org 0x27E7A
m68k_027e7a:
        tst.w (%a3)
m68k_027e7a_end:
.org 0x27E7C
m68k_027e7c:
        bne.w (. + 12)
m68k_027e7c_end:
.org 0x27E80
m68k_027e80:
        bra.b (. + -48)
m68k_027e80_end:
.org 0x27E82
m68k_027e82:
        tst.w 0x4(%a3)
m68k_027e82_end:
.org 0x27E86
m68k_027e86:
        beq.b (. + -54)
m68k_027e86_end:
.org 0x27E88
m68k_027e88:
        cmpi.w #0x3,%d1
m68k_027e88_end:
.org 0x27E8C
m68k_027e8c:
        bcc.b (. + 4)
m68k_027e8c_end:
.org 0x27E8E
m68k_027e8e:
        move.w %d1,(%a0)
m68k_027e8e_end:
.org 0x27E90
m68k_027e90:
        bsr.w (. + -1194)
m68k_027e90_end:
.org 0x27E94
m68k_027e94:
        btst.l #0x5,%d0
m68k_027e94_end:
.org 0x27E98
m68k_027e98:
        bne.w (. + 50)
m68k_027e98_end:
.org 0x27E9C
m68k_027e9c:
        andi.w #0xc,%d0
m68k_027e9c_end:
.org 0x27EA0
m68k_027ea0:
        bne.w (. + 16)
m68k_027ea0_end:
.org 0x27EA4
m68k_027ea4:
        move.w 0xff7008:l,%d0
m68k_027ea4_end:
.org 0x27EAA
m68k_027eaa:
        andi.w #0x8,%d0
m68k_027eaa_end:
.org 0x27EAE
m68k_027eae:
        beq.b (. + 28)
m68k_027eae_end:
.org 0x27EB0
m68k_027eb0:
        move.w #0xc8,%d0
m68k_027eb0_end:
.org 0x27EB4
m68k_027eb4:
        move.w (%a0),%d1
m68k_027eb4_end:
.org 0x27EB6
m68k_027eb6:
        mulu.w #0x38,%d1
m68k_027eb6_end:
.org 0x27EBA
m68k_027eba:
        addi.w #0x68,%d1
m68k_027eba_end:
.org 0x27EBE
m68k_027ebe:
        move.w #0x43,%d2
m68k_027ebe_end:
.org 0x27EC2
m68k_027ec2:
        move.w #0x8000,%d3
m68k_027ec2_end:
.org 0x27EC6
m68k_027ec6:
        bsr.w (. + 4310)
m68k_027ec6_end:
.org 0x27ECA
m68k_027eca:
        subq.w #0x1,0xff70fa:l
m68k_027eca_end:
.org 0x27ED0
m68k_027ed0:
        rts
m68k_027ed0_end:
.org 0x27ED2
m68k_027ed2:
        tst.w 0xff7018:l
m68k_027ed2_end:
.org 0x27ED8
m68k_027ed8:
        bmi.b (. + 20)
m68k_027ed8_end:
.org 0x27EDA
m68k_027eda:
        move.w 0xff706a:l,%d1
m68k_027eda_end:
.org 0x27EE0
m68k_027ee0:
        cmp.w 0xff7070:l,%d1
m68k_027ee0_end:
.org 0x27EE6
m68k_027ee6:
        beq.w (. + 166)
m68k_027ee6_end:
.org 0x27EEA
m68k_027eea:
        bra.b (. + 18)
m68k_027eea_end:
.org 0x27EEC
m68k_027eec:
        move.w 0xff70ba:l,%d1
m68k_027eec_end:
.org 0x27EF2
m68k_027ef2:
        cmp.w 0xff70c0:l,%d1
m68k_027ef2_end:
.org 0x27EF8
m68k_027ef8:
        beq.w (. + 148)
m68k_027ef8_end:
.org 0x27EFC
m68k_027efc:
        move.w 0xff7018:l,%d1
m68k_027efc_end:
.org 0x27F02
m68k_027f02:
        andi.w #0xf,%d0
m68k_027f02_end:
.org 0x27F06
m68k_027f06:
        beq.b (. + 46)
m68k_027f06_end:
.org 0x27F08
m68k_027f08:
        move.w #0x1,%d2
m68k_027f08_end:
.org 0x27F0C
m68k_027f0c:
        btst.l #0x3,%d0
m68k_027f0c_end:
.org 0x27F10
m68k_027f10:
        bne.b (. + 22)
m68k_027f10_end:
.org 0x27F12
m68k_027f12:
        neg.w %d2
m68k_027f12_end:
.org 0x27F14
m68k_027f14:
        btst.l #0x2,%d0
m68k_027f14_end:
.org 0x27F18
m68k_027f18:
        bne.b (. + 14)
m68k_027f18_end:
.org 0x27F1A
m68k_027f1a:
        move.w #0x2,%d2
m68k_027f1a_end:
.org 0x27F1E
m68k_027f1e:
        btst.l #0x1,%d0
m68k_027f1e_end:
.org 0x27F22
m68k_027f22:
        bne.b (. + 4)
m68k_027f22_end:
.org 0x27F24
m68k_027f24:
        neg.w %d2
m68k_027f24_end:
.org 0x27F26
m68k_027f26:
        add.b %d2,%d1
m68k_027f26_end:
.org 0x27F28
m68k_027f28:
        cmpi.b #0x4,%d1
m68k_027f28_end:
.org 0x27F2C
m68k_027f2c:
        bcc.b (. + 8)
m68k_027f2c_end:
.org 0x27F2E
m68k_027f2e:
        move.w %d1,0xff7018:l
m68k_027f2e_end:
.org 0x27F34
m68k_027f34:
        bsr.w (. + -1358)
m68k_027f34_end:
.org 0x27F38
m68k_027f38:
        btst.l #0x5,%d0
m68k_027f38_end:
.org 0x27F3C
m68k_027f3c:
        bne.w (. + 72)
m68k_027f3c_end:
.org 0x27F40
m68k_027f40:
        andi.w #0xf,%d0
m68k_027f40_end:
.org 0x27F44
m68k_027f44:
        bne.w (. + 16)
m68k_027f44_end:
.org 0x27F48
m68k_027f48:
        move.w 0xff7008:l,%d0
m68k_027f48_end:
.org 0x27F4E
m68k_027f4e:
        andi.w #0x8,%d0
m68k_027f4e_end:
.org 0x27F52
m68k_027f52:
        beq.b (. + 50)
m68k_027f52_end:
.org 0x27F54
m68k_027f54:
        move.w 0xff7018:l,%d0
m68k_027f54_end:
.org 0x27F5A
m68k_027f5a:
        andi.w #0x2,%d0
m68k_027f5a_end:
.org 0x27F5E
m68k_027f5e:
        mulu.w #0xc,%d0
m68k_027f5e_end:
.org 0x27F62
m68k_027f62:
        addi.w #0xb0,%d0
m68k_027f62_end:
.org 0x27F66
m68k_027f66:
        move.w 0xff7018:l,%d1
m68k_027f66_end:
.org 0x27F6C
m68k_027f6c:
        andi.w #0x1,%d1
m68k_027f6c_end:
.org 0x27F70
m68k_027f70:
        mulu.w #0x30,%d1
m68k_027f70_end:
.org 0x27F74
m68k_027f74:
        addi.w #0x88,%d1
m68k_027f74_end:
.org 0x27F78
m68k_027f78:
        move.w #0x43,%d2
m68k_027f78_end:
.org 0x27F7C
m68k_027f7c:
        move.w #0x8000,%d3
m68k_027f7c_end:
.org 0x27F80
m68k_027f80:
        bsr.w (. + 4124)
m68k_027f80_end:
.org 0x27F84
m68k_027f84:
        subq.w #0x1,0xff70fa:l
m68k_027f84_end:
.org 0x27F8A
m68k_027f8a:
        rts
m68k_027f8a_end:
.org 0x27F8C
m68k_027f8c:
        moveq #0,%d1
m68k_027f8c_end:
.org 0x27F8E
m68k_027f8e:
        move.b 0xff7019:l,%d1
m68k_027f8e_end:
.org 0x27F94
m68k_027f94:
        btst.l #0x3,%d0
m68k_027f94_end:
.org 0x27F98
m68k_027f98:
        beq.b (. + 20)
m68k_027f98_end:
.org 0x27F9A
m68k_027f9a:
        addq.w #0x1,%d1
m68k_027f9a_end:
.org 0x27F9C
m68k_027f9c:
        cmpi.w #0x2,%d1
m68k_027f9c_end:
.org 0x27FA0
m68k_027fa0:
        bne.b (. + 4)
m68k_027fa0_end:
.org 0x27FA2
m68k_027fa2:
        addq.w #0x1,%d1
m68k_027fa2_end:
.org 0x27FA4
m68k_027fa4:
        cmpi.w #0x4,%d1
m68k_027fa4_end:
.org 0x27FA8
m68k_027fa8:
        bcs.b (. + 4)
m68k_027fa8_end:
.org 0x27FAA
m68k_027faa:
        moveq #0,%d1
m68k_027faa_end:
.org 0x27FAC
m68k_027fac:
        btst.l #0x2,%d0
m68k_027fac_end:
.org 0x27FB0
m68k_027fb0:
        beq.b (. + 16)
m68k_027fb0_end:
.org 0x27FB2
m68k_027fb2:
        cmpi.w #0x3,%d1
m68k_027fb2_end:
.org 0x27FB6
m68k_027fb6:
        bne.b (. + 4)
m68k_027fb6_end:
.org 0x27FB8
m68k_027fb8:
        subq.w #0x1,%d1
m68k_027fb8_end:
.org 0x27FBA
m68k_027fba:
        subq.w #0x1,%d1
m68k_027fba_end:
.org 0x27FBC
m68k_027fbc:
        bpl.b (. + 4)
m68k_027fbc_end:
.org 0x27FBE
m68k_027fbe:
        moveq #3,%d1
m68k_027fbe_end:
.org 0x27FC0
m68k_027fc0:
        move.b %d1,0xff7019:l
m68k_027fc0_end:
.org 0x27FC6
m68k_027fc6:
        bsr.w (. + -1504)
m68k_027fc6_end:
.org 0x27FCA
m68k_027fca:
        btst.l #0x5,%d0
m68k_027fca_end:
.org 0x27FCE
m68k_027fce:
        bne.w (. + 56)
m68k_027fce_end:
.org 0x27FD2
m68k_027fd2:
        andi.w #0xf,%d0
m68k_027fd2_end:
.org 0x27FD6
m68k_027fd6:
        bne.w (. + 16)
m68k_027fd6_end:
.org 0x27FDA
m68k_027fda:
        move.w 0xff7008:l,%d0
m68k_027fda_end:
.org 0x27FE0
m68k_027fe0:
        andi.w #0x8,%d0
m68k_027fe0_end:
.org 0x27FE4
m68k_027fe4:
        beq.b (. + 34)
m68k_027fe4_end:
.org 0x27FE6
m68k_027fe6:
        move.w 0xff7018:l,%d2
m68k_027fe6_end:
.org 0x27FEC
m68k_027fec:
        andi.w #0x3,%d2
m68k_027fec_end:
.org 0x27FF0
m68k_027ff0:
        move.w #0xc8,%d0
m68k_027ff0_end:
.org 0x27FF4
m68k_027ff4:
        moveq #0,%d1
m68k_027ff4_end:
.org 0x27FF6
m68k_027ff6:
        move.b 22(%pc, %d2.w),%d1
m68k_027ff6_end:
.org 0x27FFA
m68k_027ffa:
        move.w #0x43,%d2
m68k_027ffa_end:
.org 0x27FFE
m68k_027ffe:
        move.w #0x8000,%d3
m68k_027ffe_end:
.org 0x28002
m68k_028002:
        bsr.w (. + 3994)
m68k_028002_end:
.org 0x28006
m68k_028006:
        subq.w #0x1,0xff70fa:l
m68k_028006_end:
.org 0x2800C
m68k_02800c:
        rts
m68k_02800c_end:
.org 0x28228
m68k_028228:
        lea.l 22(%pc),%a2
m68k_028228_end:
.org 0x2822C
m68k_02822c:
        asl.w #0x2,%d0
m68k_02822c_end:
.org 0x2822E
m68k_02822e:
        move.l (%a2, %d0.w),0xff700e:l
m68k_02822e_end:
.org 0x28236
m68k_028236:
        move.w #0xc600,0xff700c:l
m68k_028236_end:
.org 0x2823E
m68k_02823e:
        rts
m68k_02823e_end:
.org 0x28D7A
m68k_028d7a:
        addq.w #0x1,%d0
m68k_028d7a_end:
.org 0x28D7C
m68k_028d7c:
        cmpi.w #0x5,%d0
m68k_028d7c_end:
.org 0x28D80
m68k_028d80:
        bcs.b (. + 10)
m68k_028d80_end:
.org 0x28D82
m68k_028d82:
        clr.w %d0
m68k_028d82_end:
.org 0x28D84
m68k_028d84:
        bclr.b #0x7,0x2(%a0)
m68k_028d84_end:
.org 0x28D8A
m68k_028d8a:
        move.w %d0,0x4(%a0)
m68k_028d8a_end:
.org 0x28D8E
m68k_028d8e:
        move.w 0x26(%a0),%d0
m68k_028d8e_end:
.org 0x28D92
m68k_028d92:
        beq.b (. + 60)
m68k_028d92_end:
.org 0x28D94
m68k_028d94:
        move.w #0x400,%d1
m68k_028d94_end:
.org 0x28D98
m68k_028d98:
        lea.l -3354(%pc),%a2
m68k_028d98_end:
.org 0x28D9C
m68k_028d9c:
        lea.l 0xfb00:w,%a3
m68k_028d9c_end:
.org 0x28DA0
m68k_028da0:
        cmpa.l #0xff7050,%a0
m68k_028da0_end:
.org 0x28DA6
m68k_028da6:
        beq.b (. + 14)
m68k_028da6_end:
.org 0x28DA8
m68k_028da8:
        move.w #0x800,%d1
m68k_028da8_end:
.org 0x28DAC
m68k_028dac:
        lea.l -3342(%pc),%a2
m68k_028dac_end:
.org 0x28DB0
m68k_028db0:
        lea.l 0xfb20:w,%a3
m68k_028db0_end:
.org 0x28DB4
m68k_028db4:
        andi.w #0x1,%d0
m68k_028db4_end:
.org 0x28DB8
m68k_028db8:
        bne.b (. + 6)
m68k_028db8_end:
.org 0x28DBA
m68k_028dba:
        lea.l -3260(%pc),%a2
m68k_028dba_end:
.org 0x28DBE
m68k_028dbe:
        andi.w #0xf3f3,(%a0)
m68k_028dbe_end:
.org 0x28DC2
m68k_028dc2:
        or.w %d1,(%a0)
m68k_028dc2_end:
.org 0x28DC4
m68k_028dc4:
        move.w #0x7,%d3
m68k_028dc4_end:
.org 0x28DC8
m68k_028dc8:
        move.w (%a2)+,(%a3)+
m68k_028dc8_end:
.org 0x28DCA
m68k_028dca:
        dbra %d3,(. + -2)
m68k_028dca_end:
.org 0x28DCE
m68k_028dce:
        btst.b #0x4,0x2(%a0)
m68k_028dce_end:
.org 0x28DD4
m68k_028dd4:
        beq.b (. + 20)
m68k_028dd4_end:
.org 0x28DD6
m68k_028dd6:
        tst.w 0xa(%a0)
m68k_028dd6_end:
.org 0x28DDA
m68k_028dda:
        bne.w (. + 146)
m68k_028dda_end:
.org 0x28DDE
m68k_028dde:
        bclr.b #0x4,0x2(%a0)
m68k_028dde_end:
.org 0x28DE4
m68k_028de4:
        bra.w (. + 136)
m68k_028de4_end:
.org 0x28DE8
m68k_028de8:
        move.w (%a0),%d0
m68k_028de8_end:
.org 0x28DEA
m68k_028dea:
        move.w %d0,%d1
m68k_028dea_end:
.org 0x28DEC
m68k_028dec:
        andi.w #0xc,%d0
m68k_028dec_end:
.org 0x28DF0
m68k_028df0:
        beq.b (. + 50)
m68k_028df0_end:
.org 0x28DF2
m68k_028df2:
        move.w #0x8,%d3
m68k_028df2_end:
.org 0x28DF6
m68k_028df6:
        btst.b #0x3,0x18(%a0)
m68k_028df6_end:
.org 0x28DFC
m68k_028dfc:
        beq.b (. + 6)
m68k_028dfc_end:
.org 0x28DFE
m68k_028dfe:
        move.w #0x4,%d3
m68k_028dfe_end:
.org 0x28E02
m68k_028e02:
        and.w %d3,%d0
m68k_028e02_end:
.org 0x28E04
m68k_028e04:
        beq.b (. + 30)
m68k_028e04_end:
.org 0x28E06
m68k_028e06:
        move.w 0xff7008:l,%d0
m68k_028e06_end:
.org 0x28E0C
m68k_028e0c:
        andi.w #0xf,%d0
m68k_028e0c_end:
.org 0x28E10
m68k_028e10:
        bne.b (. + 18)
m68k_028e10_end:
.org 0x28E12
m68k_028e12:
        bset.b #0x4,0x2(%a0)
m68k_028e12_end:
.org 0x28E18
m68k_028e18:
        move.w #0x30,0xa(%a0)
m68k_028e18_end:
.org 0x28E1E
m68k_028e1e:
        bra.w (. + 78)
m68k_028e1e_end:
.org 0x28E22
m68k_028e22:
        andi.w #0xc00,%d1
m68k_028e22_end:
.org 0x28E26
m68k_028e26:
        beq.w (. + 70)
m68k_028e26_end:
.org 0x28E2A
m68k_028e2a:
        bset.b #0x5,0x2(%a0)
m68k_028e2a_end:
.org 0x28E30
m68k_028e30:
        move.l 0x12(%a0),%d2
m68k_028e30_end:
.org 0x28E34
m68k_028e34:
        move.w 0x28(%a0),%d3
m68k_028e34_end:
.org 0x28E38
m68k_028e38:
        or.w 0x26(%a0),%d3
m68k_028e38_end:
.org 0x28E3C
m68k_028e3c:
        beq.b (. + 8)
m68k_028e3c_end:
.org 0x28E3E
m68k_028e3e:
        addi.l #0x8000,%d2
m68k_028e3e_end:
.org 0x28E44
m68k_028e44:
        andi.w #0x800,%d1
m68k_028e44_end:
.org 0x28E48
m68k_028e48:
        bne.b (. + 4)
m68k_028e48_end:
.org 0x28E4A
m68k_028e4a:
        neg.l %d2
m68k_028e4a_end:
.org 0x28E4C
m68k_028e4c:
        add.l 0xe(%a0),%d2
m68k_028e4c_end:
.org 0x28E50
m68k_028e50:
        move.l %d2,%d1
m68k_028e50_end:
.org 0x28E52
m68k_028e52:
        sub.l 0xe(%a1),%d1
m68k_028e52_end:
.org 0x28E56
m68k_028e56:
        bpl.b (. + 4)
m68k_028e56_end:
.org 0x28E58
m68k_028e58:
        neg.l %d1
m68k_028e58_end:
.org 0x28E5A
m68k_028e5a:
        swap %d1
m68k_028e5a_end:
.org 0x28E5C
m68k_028e5c:
        cmpi.w #0xe0,%d1
m68k_028e5c_end:
.org 0x28E60
m68k_028e60:
        bcc.b (. + 12)
m68k_028e60_end:
.org 0x28E62
m68k_028e62:
        cmpi.w #0x10,%d1
m68k_028e62_end:
.org 0x28E66
m68k_028e66:
        bcs.b (. + 6)
m68k_028e66_end:
.org 0x28E68
m68k_028e68:
        move.l %d2,0xe(%a0)
m68k_028e68_end:
.org 0x28E6C
m68k_028e6c:
        btst.b #0x3,0x2(%a0)
m68k_028e6c_end:
.org 0x28E72
m68k_028e72:
        beq.b (. + 4)
m68k_028e72_end:
.org 0x28E74
m68k_028e74:
        rts
m68k_028e74_end:
.org 0x28E76
m68k_028e76:
        tst.w 0x1c(%a0)
m68k_028e76_end:
.org 0x28E7A
m68k_028e7a:
        bne.b (. + 6)
m68k_028e7a_end:
.org 0x28E7C
m68k_028e7c:
        bra.w (. + 212)
m68k_028e7c_end:
.org 0x28E80
m68k_028e80:
        move.w 0xc(%a0),%d7
m68k_028e80_end:
.org 0x28E84
m68k_028e84:
        mulu.w #0x12,%d7
m68k_028e84_end:
.org 0x28E88
m68k_028e88:
        clr.w %d2
m68k_028e88_end:
.org 0x28E8A
m68k_028e8a:
        move.b 0x3(%a0),%d2
m68k_028e8a_end:
.org 0x28E8E
m68k_028e8e:
        mulu.w #0x6,%d2
m68k_028e8e_end:
.org 0x28E92
m68k_028e92:
        add.w %d7,%d2
m68k_028e92_end:
.org 0x28E94
m68k_028e94:
        move.w 0x4(%a0),%d7
m68k_028e94_end:
.org 0x28E98
m68k_028e98:
        btst.b #0x6,0x2(%a0)
m68k_028e98_end:
.org 0x28E9E
m68k_028e9e:
        beq.b (. + 6)
m68k_028e9e_end:
.org 0x28EA0
m68k_028ea0:
        move.w #0x5,%d7
m68k_028ea0_end:
.org 0x28EA4
m68k_028ea4:
        add.w %d7,%d2
m68k_028ea4_end:
.org 0x28EA6
m68k_028ea6:
        move.w #0x58,%d0
m68k_028ea6_end:
.org 0x28EAA
m68k_028eaa:
        btst.b #0x4,0x2(%a0)
m68k_028eaa_end:
.org 0x28EB0
m68k_028eb0:
        beq.w (. + 8)
m68k_028eb0_end:
.org 0x28EB4
m68k_028eb4:
        move.w #0x54,%d0
m68k_028eb4_end:
.org 0x28EB8
m68k_028eb8:
        move.w 0xe(%a0),%d1
m68k_028eb8_end:
.org 0x28EBC
m68k_028ebc:
        sub.w 0xff7006:l,%d1
m68k_028ebc_end:
.org 0x28EC2
m68k_028ec2:
        move.w 0x18(%a0),%d3
m68k_028ec2_end:
.org 0x28EC6
m68k_028ec6:
        movem.l %a0-%a1,-(%a7)
m68k_028ec6_end:
.org 0x28ECA
m68k_028eca:
        bsr.w (. + 210)
m68k_028eca_end:
.org 0x28ECE
m68k_028ece:
        movem.l (%a7)+,%a0-%a1
m68k_028ece_end:
.org 0x28ED2
m68k_028ed2:
        btst.b #0x5,0x2(%a0)
m68k_028ed2_end:
.org 0x28ED8
m68k_028ed8:
        beq.b (. + 50)
m68k_028ed8_end:
.org 0x28EDA
m68k_028eda:
        tst.w 0xa(%a0)
m68k_028eda_end:
.org 0x28EDE
m68k_028ede:
        bne.b (. + 44)
m68k_028ede_end:
.org 0x28EE0
m68k_028ee0:
        move.w #0xa,0xa(%a0)
m68k_028ee0_end:
.org 0x28EE6
m68k_028ee6:
        move.w 0x6(%a0),%d0
m68k_028ee6_end:
.org 0x28EEA
m68k_028eea:
        addq.w #0x1,%d0
m68k_028eea_end:
.org 0x28EEC
m68k_028eec:
        cmpi.w #0x5,%d0
m68k_028eec_end:
.org 0x28EF0
m68k_028ef0:
        bcs.b (. + 22)
m68k_028ef0_end:
.org 0x28EF2
m68k_028ef2:
        move.w #0x1,%d0
m68k_028ef2_end:
.org 0x28EF6
m68k_028ef6:
        move.w (%a0),%d1
m68k_028ef6_end:
.org 0x28EF8
m68k_028ef8:
        andi.w #0xc00,%d1
m68k_028ef8_end:
.org 0x28EFC
m68k_028efc:
        bne.b (. + 10)
m68k_028efc_end:
.org 0x28EFE
m68k_028efe:
        bclr.b #0x5,0x2(%a0)
m68k_028efe_end:
.org 0x28F04
m68k_028f04:
        clr.w %d0
m68k_028f04_end:
.org 0x28F06
m68k_028f06:
        move.w %d0,0x6(%a0)
m68k_028f06_end:
.org 0x28F0A
m68k_028f0a:
        move.w #0x58,%d0
m68k_028f0a_end:
.org 0x28F0E
m68k_028f0e:
        move.w 0xe(%a0),%d1
m68k_028f0e_end:
.org 0x28F12
m68k_028f12:
        sub.w 0xff7006:l,%d1
m68k_028f12_end:
.org 0x28F18
m68k_028f18:
        move.w #0x36,%d2
m68k_028f18_end:
.org 0x28F1C
m68k_028f1c:
        tst.w 0xc(%a0)
m68k_028f1c_end:
.org 0x28F20
m68k_028f20:
        bne.b (. + 6)
m68k_028f20_end:
.org 0x28F22
m68k_028f22:
        move.w #0x3e,%d2
m68k_028f22_end:
.org 0x28F26
m68k_028f26:
        add.w 0x6(%a0),%d2
m68k_028f26_end:
.org 0x28F2A
m68k_028f2a:
        btst.b #0x4,0x2(%a0)
m68k_028f2a_end:
.org 0x28F30
m68k_028f30:
        beq.b (. + 18)
m68k_028f30_end:
.org 0x28F32
m68k_028f32:
        move.w 0xff7008:l,%d2
m68k_028f32_end:
.org 0x28F38
m68k_028f38:
        lsr.w #0x4,%d2
m68k_028f38_end:
.org 0x28F3A
m68k_028f3a:
        andi.w #0x1,%d2
m68k_028f3a_end:
.org 0x28F3E
m68k_028f3e:
        addi.w #0x3c,%d2
m68k_028f3e_end:
.org 0x28F42
m68k_028f42:
        move.w 0x18(%a0),%d3
m68k_028f42_end:
.org 0x28F46
m68k_028f46:
        move.l %a0,-(%a7)
m68k_028f46_end:
.org 0x28F48
m68k_028f48:
        bsr.w (. + 84)
m68k_028f48_end:
.org 0x28F4C
m68k_028f4c:
        movea.l (%a7)+,%a0
m68k_028f4c_end:
.org 0x28F4E
m68k_028f4e:
        rts
m68k_028f4e_end:
.org 0x28F50
m68k_028f50:
        movem.l %d0-%d3/%a0-%a1,-(%a7)
m68k_028f50_end:
.org 0x28F54
m68k_028f54:
        move.w 0xc(%a0),%d0
m68k_028f54_end:
.org 0x28F58
m68k_028f58:
        move.b 50(%pc, %d0.w),%d2
m68k_028f58_end:
.org 0x28F5C
m68k_028f5c:
        andi.w #0xff,%d2
m68k_028f5c_end:
.org 0x28F60
m68k_028f60:
        move.w 0x18(%a0),%d3
m68k_028f60_end:
.org 0x28F64
m68k_028f64:
        move.w 0xe(%a0),%d1
m68k_028f64_end:
.org 0x28F68
m68k_028f68:
        sub.w 0xff7006:l,%d1
m68k_028f68_end:
.org 0x28F6E
m68k_028f6e:
        move.w #0x58,%d0
m68k_028f6e_end:
.org 0x28F72
m68k_028f72:
        btst.b #0x4,0x2(%a0)
m68k_028f72_end:
.org 0x28F78
m68k_028f78:
        beq.w (. + 8)
m68k_028f78_end:
.org 0x28F7C
m68k_028f7c:
        move.w #0x54,%d0
m68k_028f7c_end:
.org 0x28F80
m68k_028f80:
        bsr.w (. + 28)
m68k_028f80_end:
.org 0x28F84
m68k_028f84:
        movem.l (%a7)+,%d0-%d3/%a0-%a1
m68k_028f84_end:
.org 0x28F88
m68k_028f88:
        bra.w (. + -182)
m68k_028f88_end:
.org 0x28F9C
m68k_028f9c:
        movem.l %d0-%d3,-(%a7)
m68k_028f9c_end:
.org 0x28FA0
m68k_028fa0:
        movea.l 0xff7002:l,%a0
m68k_028fa0_end:
.org 0x28FA6
m68k_028fa6:
        lea.l 144(%pc),%a1
m68k_028fa6_end:
.org 0x28FAA
m68k_028faa:
        asl.w #0x2,%d2
m68k_028faa_end:
.org 0x28FAC
m68k_028fac:
        movea.l (%a1, %d2.w),%a1
m68k_028fac_end:
.org 0x28FB0
m68k_028fb0:
        move.w 0xff7000:l,%d2
m68k_028fb0_end:
.org 0x28FB6
m68k_028fb6:
        cmpa.l #0xfffff800,%a0
m68k_028fb6_end:
.org 0x28FBC
m68k_028fbc:
        beq.b (. + 6)
m68k_028fbc_end:
.org 0x28FBE
m68k_028fbe:
        move.b %d2,-0x5(%a0)
m68k_028fbe_end:
.org 0x28FC2
m68k_028fc2:
        addq.w #0x1,%d2
m68k_028fc2_end:
.org 0x28FC4
m68k_028fc4:
        move.w %d3,%d4
m68k_028fc4_end:
.org 0x28FC6
m68k_028fc6:
        andi.w #0xe7ff,%d3
m68k_028fc6_end:
.org 0x28FCA
m68k_028fca:
        andi.w #0x1800,%d4
m68k_028fca_end:
.org 0x28FCE
m68k_028fce:
        move.b 0x2(%a1),%d7
m68k_028fce_end:
.org 0x28FD2
m68k_028fd2:
        ext.w %d7
m68k_028fd2_end:
.org 0x28FD4
m68k_028fd4:
        add.w %d0,%d7
m68k_028fd4_end:
.org 0x28FD6
m68k_028fd6:
        addi.w #0x80,%d7
m68k_028fd6_end:
.org 0x28FDA
m68k_028fda:
        move.w %d7,(%a0)+
m68k_028fda_end:
.org 0x28FDC
m68k_028fdc:
        move.b 0x1(%a1),%d7
m68k_028fdc_end:
.org 0x28FE0
m68k_028fe0:
        asl.w #0x8,%d7
m68k_028fe0_end:
.org 0x28FE2
m68k_028fe2:
        or.w %d2,%d7
m68k_028fe2_end:
.org 0x28FE4
m68k_028fe4:
        addq.w #0x1,%d2
m68k_028fe4_end:
.org 0x28FE6
m68k_028fe6:
        move.w %d7,(%a0)+
m68k_028fe6_end:
.org 0x28FE8
m68k_028fe8:
        asr.w #0x7,%d7
m68k_028fe8_end:
.org 0x28FEA
m68k_028fea:
        andi.w #0x18,%d7
m68k_028fea_end:
.org 0x28FEE
m68k_028fee:
        addq.w #0x8,%d7
m68k_028fee_end:
.org 0x28FF0
m68k_028ff0:
        move.w %d7,%d5
m68k_028ff0_end:
.org 0x28FF2
m68k_028ff2:
        move.w 0x4(%a1),%d7
m68k_028ff2_end:
.org 0x28FF6
m68k_028ff6:
        add.w %d3,%d7
m68k_028ff6_end:
.org 0x28FF8
m68k_028ff8:
        eor.w %d4,%d7
m68k_028ff8_end:
.org 0x28FFA
m68k_028ffa:
        move.w %d7,(%a0)+
m68k_028ffa_end:
.org 0x28FFC
m68k_028ffc:
        move.b 0x3(%a1),%d7
m68k_028ffc_end:
.org 0x29000
m68k_029000:
        ext.w %d7
m68k_029000_end:
.org 0x29002
m68k_029002:
        btst.l #0xb,%d4
m68k_029002_end:
.org 0x29006
m68k_029006:
        beq.b (. + 6)
m68k_029006_end:
.org 0x29008
m68k_029008:
        neg.w %d7
m68k_029008_end:
.org 0x2900A
m68k_02900a:
        sub.w %d5,%d7
m68k_02900a_end:
.org 0x2900C
m68k_02900c:
        add.w %d1,%d7
m68k_02900c_end:
.org 0x2900E
m68k_02900e:
        addi.w #0x80,%d7
m68k_02900e_end:
.org 0x29012
m68k_029012:
        move.w %d7,(%a0)+
m68k_029012_end:
.org 0x29014
m68k_029014:
        addq.w #0x6,%a1
m68k_029014_end:
.org 0x29016
m68k_029016:
        btst.b #0x7,-0x6(%a1)
m68k_029016_end:
.org 0x2901C
m68k_02901c:
        beq.b (. + -78)
m68k_02901c_end:
.org 0x2901E
m68k_02901e:
        move.b #0x0,-0x5(%a0)
m68k_02901e_end:
.org 0x29024
m68k_029024:
        move.l %a0,0xff7002:l
m68k_029024_end:
.org 0x2902A
m68k_02902a:
        subq.w #0x1,%d2
m68k_02902a_end:
.org 0x2902C
m68k_02902c:
        move.w %d2,0xff7000:l
m68k_02902c_end:
.org 0x29032
m68k_029032:
        movem.l (%a7)+,%d0-%d3
m68k_029032_end:
.org 0x29036
m68k_029036:
        rts
m68k_029036_end:
.org 0x2A22E
m68k_02a22e:
        move.w 0xc(%a0),%d1
m68k_02a22e_end:
.org 0x2A232
m68k_02a232:
        asl.w #0x1,%d1
m68k_02a232_end:
.org 0x2A234
m68k_02a234:
        move.w 42(%pc, %d1.w),%d2
m68k_02a234_end:
.org 0x2A238
m68k_02a238:
        btst.b #0x3,0x18(%a0)
m68k_02a238_end:
.org 0x2A23E
m68k_02a23e:
        bne.b (. + 4)
m68k_02a23e_end:
.org 0x2A240
m68k_02a240:
        neg.w %d2
m68k_02a240_end:
.org 0x2A242
m68k_02a242:
        add.w 0xe(%a0),%d2
m68k_02a242_end:
.org 0x2A246
m68k_02a246:
        sub.w 0xe(%a1),%d2
m68k_02a246_end:
.org 0x2A24A
m68k_02a24a:
        move.w %d2,%d3
m68k_02a24a_end:
.org 0x2A24C
m68k_02a24c:
        bpl.b (. + 4)
m68k_02a24c_end:
.org 0x2A24E
m68k_02a24e:
        neg.w %d2
m68k_02a24e_end:
.org 0x2A250
m68k_02a250:
        btst.b #0x3,0x18(%a0)
m68k_02a250_end:
.org 0x2A256
m68k_02a256:
        beq.b (. + 4)
m68k_02a256_end:
.org 0x2A258
m68k_02a258:
        neg.w %d3
m68k_02a258_end:
.org 0x2A25A
m68k_02a25a:
        sub.w 10(%pc, %d1.w),%d2
m68k_02a25a_end:
.org 0x2A25E
m68k_02a25e:
        rts
m68k_02a25e_end:
.org 0x2A29A
m68k_02a29a:
        tst.w 0x22(%a0)
m68k_02a29a_end:
.org 0x2A29E
m68k_02a29e:
        beq.b (. + 6)
m68k_02a29e_end:
.org 0x2A2A0
m68k_02a2a0:
        subq.w #0x1,0x22(%a0)
m68k_02a2a0_end:
.org 0x2A2A4
m68k_02a2a4:
        move.w 0x1c(%a0),%d0
m68k_02a2a4_end:
.org 0x2A2A8
m68k_02a2a8:
        bne.b (. + 12)
m68k_02a2a8_end:
.org 0x2A2AA
m68k_02a2aa:
        move.w %d0,0x2(%a0)
m68k_02a2aa_end:
.org 0x2A2AE
m68k_02a2ae:
        move.w %d0,0x4(%a0)
m68k_02a2ae_end:
.org 0x2A2B2
m68k_02a2b2:
        rts
m68k_02a2b2_end:
.org 0x2A2B4
m68k_02a2b4:
        move.w 0x1c(%a1),%d0
m68k_02a2b4_end:
.org 0x2A2B8
m68k_02a2b8:
        bne.b (. + 8)
m68k_02a2b8_end:
.org 0x2A2BA
m68k_02a2ba:
        move.w #0x100,%d0
m68k_02a2ba_end:
.org 0x2A2BE
m68k_02a2be:
        rts
m68k_02a2be_end:
.org 0x2A2C0
m68k_02a2c0:
        tst.w 0x22(%a0)
m68k_02a2c0_end:
.org 0x2A2C4
m68k_02a2c4:
        bne.b (. + 58)
m68k_02a2c4_end:
.org 0x2A2C6
m68k_02a2c6:
        jsr 0x83d4:l
m68k_02a2c6_end:
.org 0x2A2CC
m68k_02a2cc:
        andi.w #0x1f,%d0
m68k_02a2cc_end:
.org 0x2A2D0
m68k_02a2d0:
        addi.w #0x1e,%d0
m68k_02a2d0_end:
.org 0x2A2D4
m68k_02a2d4:
        move.w %d0,0x22(%a0)
m68k_02a2d4_end:
.org 0x2A2D8
m68k_02a2d8:
        move.w 0x1e(%a0),%d0
m68k_02a2d8_end:
.org 0x2A2DC
m68k_02a2dc:
        lea.l 42(%pc),%a2
m68k_02a2dc_end:
.org 0x2A2E0
m68k_02a2e0:
        nop
m68k_02a2e0_end:
.org 0x2A2E2
m68k_02a2e2:
        bsr.w (. + -4946)
m68k_02a2e2_end:
.org 0x2A2E6
m68k_02a2e6:
        move.w %d1,%d6
m68k_02a2e6_end:
.org 0x2A2E8
m68k_02a2e8:
        bsr.w (. + 780)
m68k_02a2e8_end:
.org 0x2A2EC
m68k_02a2ec:
        bsr.w (. + 1908)
m68k_02a2ec_end:
.org 0x2A2F0
m68k_02a2f0:
        move.w %d7,%d0
m68k_02a2f0_end:
.org 0x2A2F2
m68k_02a2f2:
        tst.w %d0
m68k_02a2f2_end:
.org 0x2A2F4
m68k_02a2f4:
        bne.b (. + -66)
m68k_02a2f4_end:
.org 0x2A2F6
m68k_02a2f6:
        move.w %d6,%d1
m68k_02a2f6_end:
.org 0x2A2F8
m68k_02a2f8:
        asl.w #0x1,%d1
m68k_02a2f8_end:
.org 0x2A2FA
m68k_02a2fa:
        jsr 24(%pc, %d1.w)
m68k_02a2fa_end:
.org 0x2A2FE
m68k_02a2fe:
        move.w 0x24(%a0),%d0
m68k_02a2fe_end:
.org 0x2A302
m68k_02a302:
        asl.w #0x2,%d0
m68k_02a302_end:
.org 0x2A304
m68k_02a304:
        jmp 38(%pc, %d0.w)
m68k_02a304_end:
.org 0x2A5F4
m68k_02a5f4:
        clr.w %d7
m68k_02a5f4_end:
.org 0x2A5F6
m68k_02a5f6:
        move.w 0xff7008:l,%d1
m68k_02a5f6_end:
.org 0x2A5FC
m68k_02a5fc:
        andi.w #0x7,%d1
m68k_02a5fc_end:
.org 0x2A600
m68k_02a600:
        beq.w (. + 6)
m68k_02a600_end:
.org 0x2A604
m68k_02a604:
        rts
m68k_02a604_end:
.org 0x2A606
m68k_02a606:
        cmpa.l #0xff7050,%a0
m68k_02a606_end:
.org 0x2A60C
m68k_02a60c:
        bne.w (. + 136)
m68k_02a60c_end:
.org 0x2A610
m68k_02a610:
        cmpi.w #0x33,0x1c(%a1)
m68k_02a610_end:
.org 0x2A616
m68k_02a616:
        bcc.w (. + 24)
m68k_02a616_end:
.org 0x2A61A
m68k_02a61a:
        jsr 0x83d4:l
m68k_02a61a_end:
.org 0x2A620
m68k_02a620:
        andi.w #0x1,%d0
m68k_02a620_end:
.org 0x2A624
m68k_02a624:
        bne.w (. + 24)
m68k_02a624_end:
.org 0x2A628
m68k_02a628:
        move.w #0x40,%d7
m68k_02a628_end:
.org 0x2A62C
m68k_02a62c:
        rts
m68k_02a62c_end:
.org 0x2A62E
m68k_02a62e:
        jsr 0x83d4:l
m68k_02a62e_end:
.org 0x2A634
m68k_02a634:
        andi.w #0x3,%d0
m68k_02a634_end:
.org 0x2A638
m68k_02a638:
        beq.b (. + -16)
m68k_02a638_end:
.org 0x2A63A
m68k_02a63a:
        rts
m68k_02a63a_end:
.org 0x2A63C
m68k_02a63c:
        move.w 0x1e(%a1),%d2
m68k_02a63c_end:
.org 0x2A640
m68k_02a640:
        move.w 0x1e(%a0),%d3
m68k_02a640_end:
.org 0x2A644
m68k_02a644:
        move.w 0x1c(%a0),%d1
m68k_02a644_end:
.org 0x2A648
m68k_02a648:
        cmpi.w #0x28,%d1
m68k_02a648_end:
.org 0x2A64C
m68k_02a64c:
        bcs.w (. + 58)
m68k_02a64c_end:
.org 0x2A650
m68k_02a650:
        cmpi.w #0x46,%d1
m68k_02a650_end:
.org 0x2A654
m68k_02a654:
        bcs.w (. + 46)
m68k_02a654_end:
.org 0x2A658
m68k_02a658:
        cmp.w %d3,%d2
m68k_02a658_end:
.org 0x2A65A
m68k_02a65a:
        bcs.w (. + 26)
m68k_02a65a_end:
.org 0x2A65E
m68k_02a65e:
        jsr 0x83d4:l
m68k_02a65e_end:
.org 0x2A664
m68k_02a664:
        andi.w #0x1,%d0
m68k_02a664_end:
.org 0x2A668
m68k_02a668:
        bne.w (. + 6)
m68k_02a668_end:
.org 0x2A66C
m68k_02a66c:
        rts
m68k_02a66c_end:
.org 0x2A66E
m68k_02a66e:
        move.w #0x43,%d7
m68k_02a66e_end:
.org 0x2A672
m68k_02a672:
        rts
m68k_02a672_end:
.org 0x2A674
m68k_02a674:
        jsr 0x83d4:l
m68k_02a674_end:
.org 0x2A67A
m68k_02a67a:
        andi.w #0x3,%d0
m68k_02a67a_end:
.org 0x2A67E
m68k_02a67e:
        beq.b (. + -16)
m68k_02a67e_end:
.org 0x2A680
m68k_02a680:
        rts
m68k_02a680_end:
.org 0x2A682
m68k_02a682:
        cmp.w %d3,%d2
m68k_02a682_end:
.org 0x2A684
m68k_02a684:
        bcs.b (. + -38)
m68k_02a684_end:
.org 0x2A686
m68k_02a686:
        jsr 0x83d4:l
m68k_02a686_end:
.org 0x2A68C
m68k_02a68c:
        andi.w #0x3,%d0
m68k_02a68c_end:
.org 0x2A690
m68k_02a690:
        bne.b (. + -34)
m68k_02a690_end:
.org 0x2A692
m68k_02a692:
        rts
m68k_02a692_end:
.org 0x2A694
m68k_02a694:
        move.w 0x1c(%a1),%d2
m68k_02a694_end:
.org 0x2A698
m68k_02a698:
        move.w 0x1c(%a0),%d3
m68k_02a698_end:
.org 0x2A69C
m68k_02a69c:
        cmp.w %d3,%d2
m68k_02a69c_end:
.org 0x2A69E
m68k_02a69e:
        bcs.w (. + 810)
m68k_02a69e_end:
.org 0x2A6A2
m68k_02a6a2:
        cmpi.w #0x32,%d3
m68k_02a6a2_end:
.org 0x2A6A6
m68k_02a6a6:
        bcs.w (. + 102)
m68k_02a6a6_end:
.org 0x2A6AA
m68k_02a6aa:
        cmpi.w #0x50,%d3
m68k_02a6aa_end:
.org 0x2A6AE
m68k_02a6ae:
        bcs.w (. + 30)
m68k_02a6ae_end:
.org 0x2A6B2
m68k_02a6b2:
        rts
m68k_02a6b2_end:
.org 0x2A6CC
m68k_02a6cc:
        move.w 0x1e(%a1),%d2
m68k_02a6cc_end:
.org 0x2A6D0
m68k_02a6d0:
        move.w 0x1e(%a0),%d3
m68k_02a6d0_end:
.org 0x2A6D4
m68k_02a6d4:
        cmp.w %d3,%d2
m68k_02a6d4_end:
.org 0x2A6D6
m68k_02a6d6:
        bcs.w (. + 40)
m68k_02a6d6_end:
.org 0x2A6DA
m68k_02a6da:
        move.w -40(%pc, %d6.w),%d2
m68k_02a6da_end:
.org 0x2A6DE
m68k_02a6de:
        bsr.w (. + 802)
m68k_02a6de_end:
.org 0x2A6E2
m68k_02a6e2:
        bcs.b (. + -116)
m68k_02a6e2_end:
.org 0x2A6E4
m68k_02a6e4:
        move.w -38(%pc, %d6.w),%d2
m68k_02a6e4_end:
.org 0x2A6E8
m68k_02a6e8:
        bsr.w (. + 792)
m68k_02a6e8_end:
.org 0x2A6EC
m68k_02a6ec:
        bcs.w (. + -196)
m68k_02a6ec_end:
.org 0x2A6F0
m68k_02a6f0:
        rts
m68k_02a6f0_end:
.org 0x2A6FE
m68k_02a6fe:
        move.w -14(%pc, %d6.w),%d2
m68k_02a6fe_end:
.org 0x2A702
m68k_02a702:
        bsr.w (. + 766)
m68k_02a702_end:
.org 0x2A706
m68k_02a706:
        bcs.w (. + -152)
m68k_02a706_end:
.org 0x2A70A
m68k_02a70a:
        bra.b (. + -38)
m68k_02a70a_end:
.org 0x2A70C
m68k_02a70c:
        move.w 0x1e(%a1),%d0
m68k_02a70c_end:
.org 0x2A710
m68k_02a710:
        lea.l -1034(%pc),%a2
m68k_02a710_end:
.org 0x2A714
m68k_02a714:
        bsr.w (. + -6020)
m68k_02a714_end:
.org 0x2A718
m68k_02a718:
        cmpi.w #0x4,%d1
m68k_02a718_end:
.org 0x2A71C
m68k_02a71c:
        bcs.w (. + 518)
m68k_02a71c_end:
.org 0x2A720
m68k_02a720:
        cmpi.w #0x8,%d1
m68k_02a720_end:
.org 0x2A724
m68k_02a724:
        bcs.w (. + 344)
m68k_02a724_end:
.org 0x2A728
m68k_02a728:
        beq.w (. + 176)
m68k_02a728_end:
.org 0x2A72C
m68k_02a72c:
        tst.w 0xefd2:w
m68k_02a72c_end:
.org 0x2A730
m68k_02a730:
        bne.w (. + 12)
m68k_02a730_end:
.org 0x2A734
m68k_02a734:
        move.w 84(%pc, %d6.w),%d2
m68k_02a734_end:
.org 0x2A738
m68k_02a738:
        bra.w (. + 26)
m68k_02a738_end:
.org 0x2A73C
m68k_02a73c:
        cmpi.w #0x2,0xefd2:w
m68k_02a73c_end:
.org 0x2A742
m68k_02a742:
        beq.w (. + 12)
m68k_02a742_end:
.org 0x2A746
m68k_02a746:
        move.w 90(%pc, %d6.w),%d2
m68k_02a746_end:
.org 0x2A74A
m68k_02a74a:
        bra.w (. + 8)
m68k_02a74a_end:
.org 0x2A74E
m68k_02a74e:
        move.w 106(%pc, %d6.w),%d2
m68k_02a74e_end:
.org 0x2A752
m68k_02a752:
        bsr.w (. + 686)
m68k_02a752_end:
.org 0x2A756
m68k_02a756:
        bcs.w (. + -232)
m68k_02a756_end:
.org 0x2A75A
m68k_02a75a:
        tst.w 0xefd2:w
m68k_02a75a_end:
.org 0x2A75E
m68k_02a75e:
        bne.w (. + 12)
m68k_02a75e_end:
.org 0x2A762
m68k_02a762:
        move.w 50(%pc, %d6.w),%d2
m68k_02a762_end:
.org 0x2A766
m68k_02a766:
        bra.w (. + 26)
m68k_02a766_end:
.org 0x2A76A
m68k_02a76a:
        cmpi.w #0x2,0xefd2:w
m68k_02a76a_end:
.org 0x2A770
m68k_02a770:
        beq.w (. + 12)
m68k_02a770_end:
.org 0x2A774
m68k_02a774:
        move.w 56(%pc, %d6.w),%d2
m68k_02a774_end:
.org 0x2A778
m68k_02a778:
        bra.w (. + 8)
m68k_02a778_end:
.org 0x2A77C
m68k_02a77c:
        move.w 72(%pc, %d6.w),%d2
m68k_02a77c_end:
.org 0x2A780
m68k_02a780:
        bsr.w (. + 640)
m68k_02a780_end:
.org 0x2A784
m68k_02a784:
        bcs.w (. + 78)
m68k_02a784_end:
.org 0x2A788
m68k_02a788:
        rts
m68k_02a788_end:
.org 0x2A7D2
m68k_02a7d2:
        move.w #0x42,%d7
m68k_02a7d2_end:
.org 0x2A7D6
m68k_02a7d6:
        rts
m68k_02a7d6_end:
.org 0x2A7D8
m68k_02a7d8:
        tst.w 0xefd2:w
m68k_02a7d8_end:
.org 0x2A7DC
m68k_02a7dc:
        bne.w (. + 12)
m68k_02a7dc_end:
.org 0x2A7E0
m68k_02a7e0:
        move.w 82(%pc, %d6.w),%d2
m68k_02a7e0_end:
.org 0x2A7E4
m68k_02a7e4:
        bra.w (. + 26)
m68k_02a7e4_end:
.org 0x2A7E8
m68k_02a7e8:
        cmpi.w #0x2,0xefd2:w
m68k_02a7e8_end:
.org 0x2A7EE
m68k_02a7ee:
        beq.w (. + 12)
m68k_02a7ee_end:
.org 0x2A7F2
m68k_02a7f2:
        move.w 88(%pc, %d6.w),%d2
m68k_02a7f2_end:
.org 0x2A7F6
m68k_02a7f6:
        bra.w (. + 8)
m68k_02a7f6_end:
.org 0x2A7FA
m68k_02a7fa:
        move.w 104(%pc, %d6.w),%d2
m68k_02a7fa_end:
.org 0x2A7FE
m68k_02a7fe:
        bsr.w (. + 514)
m68k_02a7fe_end:
.org 0x2A802
m68k_02a802:
        bcs.w (. + -404)
m68k_02a802_end:
.org 0x2A806
m68k_02a806:
        tst.w 0xefd2:w
m68k_02a806_end:
.org 0x2A80A
m68k_02a80a:
        bne.w (. + 12)
m68k_02a80a_end:
.org 0x2A80E
m68k_02a80e:
        move.w 48(%pc, %d6.w),%d2
m68k_02a80e_end:
.org 0x2A812
m68k_02a812:
        bra.w (. + 26)
m68k_02a812_end:
.org 0x2A816
m68k_02a816:
        cmpi.w #0x2,0xefd2:w
m68k_02a816_end:
.org 0x2A81C
m68k_02a81c:
        beq.w (. + 12)
m68k_02a81c_end:
.org 0x2A820
m68k_02a820:
        move.w 54(%pc, %d6.w),%d2
m68k_02a820_end:
.org 0x2A824
m68k_02a824:
        bra.w (. + 8)
m68k_02a824_end:
.org 0x2A828
m68k_02a828:
        move.w 70(%pc, %d6.w),%d2
m68k_02a828_end:
.org 0x2A82C
m68k_02a82c:
        bsr.w (. + 468)
m68k_02a82c_end:
.org 0x2A830
m68k_02a830:
        bcs.b (. + -94)
m68k_02a830_end:
.org 0x2A832
m68k_02a832:
        rts
m68k_02a832_end:
.org 0x2A87C
m68k_02a87c:
        tst.w 0xefd2:w
m68k_02a87c_end:
.org 0x2A880
m68k_02a880:
        bne.w (. + 12)
m68k_02a880_end:
.org 0x2A884
m68k_02a884:
        move.w 84(%pc, %d6.w),%d2
m68k_02a884_end:
.org 0x2A888
m68k_02a888:
        bra.w (. + 26)
m68k_02a888_end:
.org 0x2A88C
m68k_02a88c:
        cmpi.w #0x2,0xefd2:w
m68k_02a88c_end:
.org 0x2A892
m68k_02a892:
        beq.w (. + 12)
m68k_02a892_end:
.org 0x2A896
m68k_02a896:
        move.w 90(%pc, %d6.w),%d2
m68k_02a896_end:
.org 0x2A89A
m68k_02a89a:
        bra.w (. + 8)
m68k_02a89a_end:
.org 0x2A89E
m68k_02a89e:
        move.w 106(%pc, %d6.w),%d2
m68k_02a89e_end:
.org 0x2A8A2
m68k_02a8a2:
        bsr.w (. + 350)
m68k_02a8a2_end:
.org 0x2A8A6
m68k_02a8a6:
        bcs.w (. + -568)
m68k_02a8a6_end:
.org 0x2A8AA
m68k_02a8aa:
        tst.w 0xefd2:w
m68k_02a8aa_end:
.org 0x2A8AE
m68k_02a8ae:
        bne.w (. + 12)
m68k_02a8ae_end:
.org 0x2A8B2
m68k_02a8b2:
        move.w 50(%pc, %d6.w),%d2
m68k_02a8b2_end:
.org 0x2A8B6
m68k_02a8b6:
        bra.w (. + 26)
m68k_02a8b6_end:
.org 0x2A8BA
m68k_02a8ba:
        cmpi.w #0x2,0xefd2:w
m68k_02a8ba_end:
.org 0x2A8C0
m68k_02a8c0:
        beq.w (. + 12)
m68k_02a8c0_end:
.org 0x2A8C4
m68k_02a8c4:
        move.w 56(%pc, %d6.w),%d2
m68k_02a8c4_end:
.org 0x2A8C8
m68k_02a8c8:
        bra.w (. + 8)
m68k_02a8c8_end:
.org 0x2A8CC
m68k_02a8cc:
        move.w 72(%pc, %d6.w),%d2
m68k_02a8cc_end:
.org 0x2A8D0
m68k_02a8d0:
        bsr.w (. + 304)
m68k_02a8d0_end:
.org 0x2A8D4
m68k_02a8d4:
        bcs.w (. + -258)
m68k_02a8d4_end:
.org 0x2A8D8
m68k_02a8d8:
        rts
m68k_02a8d8_end:
.org 0x2A922
m68k_02a922:
        tst.w 0xefd2:w
m68k_02a922_end:
.org 0x2A926
m68k_02a926:
        bne.w (. + 12)
m68k_02a926_end:
.org 0x2A92A
m68k_02a92a:
        move.w 84(%pc, %d6.w),%d2
m68k_02a92a_end:
.org 0x2A92E
m68k_02a92e:
        bra.w (. + 26)
m68k_02a92e_end:
.org 0x2A932
m68k_02a932:
        cmpi.w #0x2,0xefd2:w
m68k_02a932_end:
.org 0x2A938
m68k_02a938:
        beq.w (. + 12)
m68k_02a938_end:
.org 0x2A93C
m68k_02a93c:
        move.w 90(%pc, %d6.w),%d2
m68k_02a93c_end:
.org 0x2A940
m68k_02a940:
        bra.w (. + 8)
m68k_02a940_end:
.org 0x2A944
m68k_02a944:
        move.w 106(%pc, %d6.w),%d2
m68k_02a944_end:
.org 0x2A948
m68k_02a948:
        bsr.w (. + 184)
m68k_02a948_end:
.org 0x2A94C
m68k_02a94c:
        bcs.w (. + -734)
m68k_02a94c_end:
.org 0x2A950
m68k_02a950:
        tst.w 0xefd2:w
m68k_02a950_end:
.org 0x2A954
m68k_02a954:
        bne.w (. + 12)
m68k_02a954_end:
.org 0x2A958
m68k_02a958:
        move.w 50(%pc, %d6.w),%d2
m68k_02a958_end:
.org 0x2A95C
m68k_02a95c:
        bra.w (. + 26)
m68k_02a95c_end:
.org 0x2A960
m68k_02a960:
        cmpi.w #0x2,0xefd2:w
m68k_02a960_end:
.org 0x2A966
m68k_02a966:
        beq.w (. + 12)
m68k_02a966_end:
.org 0x2A96A
m68k_02a96a:
        move.w 56(%pc, %d6.w),%d2
m68k_02a96a_end:
.org 0x2A96E
m68k_02a96e:
        bra.w (. + 8)
m68k_02a96e_end:
.org 0x2A972
m68k_02a972:
        move.w 72(%pc, %d6.w),%d2
m68k_02a972_end:
.org 0x2A976
m68k_02a976:
        bsr.w (. + 138)
m68k_02a976_end:
.org 0x2A97A
m68k_02a97a:
        bcs.w (. + -424)
m68k_02a97a_end:
.org 0x2A97E
m68k_02a97e:
        rts
m68k_02a97e_end:
.org 0x2A9C8
m68k_02a9c8:
        move.w 24(%pc, %d6.w),%d2
m68k_02a9c8_end:
.org 0x2A9CC
m68k_02a9cc:
        bsr.w (. + 52)
m68k_02a9cc_end:
.org 0x2A9D0
m68k_02a9d0:
        bcs.w (. + -936)
m68k_02a9d0_end:
.org 0x2A9D4
m68k_02a9d4:
        move.w 24(%pc, %d6.w),%d2
m68k_02a9d4_end:
.org 0x2A9D8
m68k_02a9d8:
        bsr.w (. + 40)
m68k_02a9d8_end:
.org 0x2A9DC
m68k_02a9dc:
        bcs.w (. + 30)
m68k_02a9dc_end:
.org 0x2A9E0
m68k_02a9e0:
        rts
m68k_02a9e0_end:
.org 0x2A9FA
m68k_02a9fa:
        move.w #0x21,%d7
m68k_02a9fa_end:
.org 0x2A9FE
m68k_02a9fe:
        rts
m68k_02a9fe_end:
.org 0x2AA00
m68k_02aa00:
        move.w %d2,%d3
m68k_02aa00_end:
.org 0x2AA02
m68k_02aa02:
        andi.w #0x7,%d2
m68k_02aa02_end:
.org 0x2AA06
m68k_02aa06:
        lsr.w #0x4,%d3
m68k_02aa06_end:
.org 0x2AA08
m68k_02aa08:
        jsr 0x83d4:l
m68k_02aa08_end:
.org 0x2AA0E
m68k_02aa0e:
        and.w %d2,%d0
m68k_02aa0e_end:
.org 0x2AA10
m68k_02aa10:
        cmp.w %d3,%d0
m68k_02aa10_end:
.org 0x2AA12
m68k_02aa12:
        rts
m68k_02aa12_end:
.org 0x2AA60
m68k_02aa60:
        cmpi.w #0x1800,0xff70fa:l
m68k_02aa60_end:
.org 0x2AA68
m68k_02aa68:
        bls.w (. + 34)
m68k_02aa68_end:
.org 0x2AA6C
m68k_02aa6c:
        cmpi.w #0x303,0xff700a:l
m68k_02aa6c_end:
.org 0x2AA74
m68k_02aa74:
        bne.w (. + 22)
m68k_02aa74_end:
.org 0x2AA78
m68k_02aa78:
        move.w 0x1c(%a0),%d0
m68k_02aa78_end:
.org 0x2AA7C
m68k_02aa7c:
        cmp.w 0x1c(%a1),%d0
m68k_02aa7c_end:
.org 0x2AA80
m68k_02aa80:
        bhi.w (. + 10)
m68k_02aa80_end:
.org 0x2AA84
m68k_02aa84:
        move.w #0x43,%d7
m68k_02aa84_end:
.org 0x2AA88
m68k_02aa88:
        rts
m68k_02aa88_end:
.org 0x2AA8A
m68k_02aa8a:
        clr.l %d0
m68k_02aa8a_end:
.org 0x2AA8C
m68k_02aa8c:
        rts
m68k_02aa8c_end:
.org 0x309AA
m68k_0309aa:
        bsr.w (. + 82)
m68k_0309aa_end:
.org 0x309AE
m68k_0309ae:
        bcs.b (. + -64)
m68k_0309ae_end:
.org 0x309B0
m68k_0309b0:
        move.w #0x20b,0xf612:w
m68k_0309b0_end:
.org 0x309B6
m68k_0309b6:
        move.w #0x4,0xf362:w
m68k_0309b6_end:
.org 0x309BC
m68k_0309bc:
        clr.w 0xf36c:w
m68k_0309bc_end:
.org 0x309C0
m68k_0309c0:
        move.l #0xc0000026,%d0
m68k_0309c0_end:
.org 0x309C6
m68k_0309c6:
        move.w #0x7,%d1
m68k_0309c6_end:
.org 0x309CA
m68k_0309ca:
        move.w #0xca02,%d2
m68k_0309ca_end:
.org 0x309CE
m68k_0309ce:
        lea.l 16(%pc),%a0
m68k_0309ce_end:
.org 0x309D2
m68k_0309d2:
        jsr 0x26bfa:l
m68k_0309d2_end:
.org 0x309FC
m68k_0309fc:
        lea.l 0xe640:w,%a0
m68k_0309fc_end:
.org 0x30A00
m68k_030a00:
        move.w 0xf376:w,%d0
m68k_030a00_end:
.org 0x30A04
m68k_030a04:
        lsl.w #0x1,%d0
m68k_030a04_end:
.org 0x30A06
m68k_030a06:
        move.w (%a0, %d0.w),%d0
m68k_030a06_end:
.org 0x30A0A
m68k_030a0a:
        lea.l 0xcc00:w,%a0
m68k_030a0a_end:
.org 0x30A0E
m68k_030a0e:
        move.b (%a0, %d0.w),%d1
m68k_030a0e_end:
.org 0x30A12
m68k_030a12:
        andi.w #0x3f,%d1
m68k_030a12_end:
.org 0x30A16
m68k_030a16:
        cmpi.w #0x28,%d1
m68k_030a16_end:
.org 0x30A1A
m68k_030a1a:
        bhi.w (. + 32)
m68k_030a1a_end:
.org 0x30A1E
m68k_030a1e:
        lsl.w #0x2,%d1
m68k_030a1e_end:
.org 0x30A20
m68k_030a20:
        lea.l 0xd4ac6:l,%a0
m68k_030a20_end:
.org 0x30A26
m68k_030a26:
        move.w 0x2(%a0, %d1.w),0xf35e:w
m68k_030a26_end:
.org 0x30A2C
m68k_030a2c:
        move.w (%a0, %d1.w),0xf360:w
m68k_030a2c_end:
.org 0x30A32
m68k_030a32:
        andi.w #0xfffe,%sr
m68k_030a32_end:
.org 0x30A36
m68k_030a36:
        bra.w (. + 60)
m68k_030a36_end:
.org 0x30A3A
m68k_030a3a:
        lea.l 0xf428:w,%a0
m68k_030a3a_end:
.org 0x30A3E
m68k_030a3e:
        move.w #0x27,%d0
m68k_030a3e_end:
.org 0x30A42
m68k_030a42:
        move.w 0xf376:w,%d1
m68k_030a42_end:
.org 0x30A46
m68k_030a46:
        cmp.b (%a0, %d0.w),%d1
m68k_030a46_end:
.org 0x30A4A
m68k_030a4a:
        beq.w (. + 16)
m68k_030a4a_end:
.org 0x30A4E
m68k_030a4e:
        dbra %d0,(. + -8)
m68k_030a4e_end:
.org 0x30A52
m68k_030a52:
        ori.w #0x1,%sr
m68k_030a52_end:
.org 0x30A56
m68k_030a56:
        bra.w (. + 28)
m68k_030a56_end:
.org 0x30A5A
m68k_030a5a:
        lea.l 0xd4aca:l,%a0
m68k_030a5a_end:
.org 0x30A60
m68k_030a60:
        lsl.w #0x2,%d0
m68k_030a60_end:
.org 0x30A62
m68k_030a62:
        move.w 0x2(%a0, %d0.w),0xf35e:w
m68k_030a62_end:
.org 0x30A68
m68k_030a68:
        move.w (%a0, %d0.w),0xf360:w
m68k_030a68_end:
.org 0x30A6E
m68k_030a6e:
        andi.w #0xfffe,%sr
m68k_030a6e_end:
.org 0x30A72
m68k_030a72:
        rts
m68k_030a72_end:
.org 0x30AC6
m68k_030ac6:
        bsr.w (. + 1120)
m68k_030ac6_end:
.org 0x30ACA
m68k_030aca:
        move.w 0xf376:w,%d0
m68k_030aca_end:
.org 0x30ACE
m68k_030ace:
        bmi.w (. + 50)
m68k_030ace_end:
.org 0x30AD2
m68k_030ad2:
        cmp.w 0xf67a:w,%d0
m68k_030ad2_end:
.org 0x30AD6
m68k_030ad6:
        beq.w (. + 118)
m68k_030ad6_end:
.org 0x30ADA
m68k_030ada:
        cmp.w 0xf67c:w,%d0
m68k_030ada_end:
.org 0x30ADE
m68k_030ade:
        beq.w (. + 110)
m68k_030ade_end:
.org 0x30AE2
m68k_030ae2:
        cmp.w 0xf67e:w,%d0
m68k_030ae2_end:
.org 0x30AE6
m68k_030ae6:
        beq.w (. + 102)
m68k_030ae6_end:
.org 0x30AEA
m68k_030aea:
        move.w #0x2,0xf362:w
m68k_030aea_end:
.org 0x30AF0
m68k_030af0:
        bsr.b (. + -124)
m68k_030af0_end:
.org 0x30AF2
m68k_030af2:
        bsr.w (. + 1330)
m68k_030af2_end:
.org 0x30AF6
m68k_030af6:
        clr.w 0xf75a:w
m68k_030af6_end:
.org 0x30AFA
m68k_030afa:
        bsr.w (. + 1354)
m68k_030afa_end:
.org 0x30AFE
m68k_030afe:
        bra.b (. + -56)
m68k_030afe_end:
.org 0x30B00
m68k_030b00:
        bsr.w (. + 1786)
m68k_030b00_end:
.org 0x30B04
m68k_030b04:
        jsr 0x1631a:l
m68k_030b04_end:
.org 0x30B0A
m68k_030b0a:
        move.w #0x209,0xf612:w
m68k_030b0a_end:
.org 0x30B10
m68k_030b10:
        move.w #0x5,0xf362:w
m68k_030b10_end:
.org 0x30B16
m68k_030b16:
        move.w #0x3,0xf36c:w
m68k_030b16_end:
.org 0x30B1C
m68k_030b1c:
        move.w #0xffff,0x9f00:w
m68k_030b1c_end:
.org 0x30B22
m68k_030b22:
        bsr.w (. + 1074)
m68k_030b22_end:
.org 0x30B26
m68k_030b26:
        jsr 274(%pc)
m68k_030b26_end:
.org 0x30B2A
m68k_030b2a:
        nop
m68k_030b2a_end:
.org 0x30B2C
m68k_030b2c:
        move.w 0xf612:w,0xf3c2:w
m68k_030b2c_end:
.org 0x30B32
m68k_030b32:
        move.w 0xf362:w,0xf3c4:w
m68k_030b32_end:
.org 0x30B38
m68k_030b38:
        move.w #0x208,0xf612:w
m68k_030b38_end:
.org 0x30B3E
m68k_030b3e:
        move.w #0x13,0xf362:w
m68k_030b3e_end:
.org 0x30B44
m68k_030b44:
        clr.w 0xf36a:w
m68k_030b44_end:
.org 0x30B48
m68k_030b48:
        bra.w (. + 62)
m68k_030b48_end:
.org 0x30B4C
m68k_030b4c:
        move.w #0x20b,0xf612:w
m68k_030b4c_end:
.org 0x30B52
m68k_030b52:
        move.w #0x4,0xf362:w
m68k_030b52_end:
.org 0x30B58
m68k_030b58:
        bsr.w (. + -348)
m68k_030b58_end:
.org 0x30B5C
m68k_030b5c:
        bcc.w (. + 12)
m68k_030b5c_end:
.org 0x30B60
m68k_030b60:
        bsr.w (. + 46)
m68k_030b60_end:
.org 0x30B64
m68k_030b64:
        bcs.w (. + -158)
m68k_030b64_end:
.org 0x30B68
m68k_030b68:
        move.w #0x85,0xf380:w
m68k_030b68_end:
.org 0x30B6E
m68k_030b6e:
        move.l #0xc0000026,%d0
m68k_030b6e_end:
.org 0x30B74
m68k_030b74:
        move.w #0x7,%d1
m68k_030b74_end:
.org 0x30B78
m68k_030b78:
        move.w #0xca02,%d2
m68k_030b78_end:
.org 0x30B7C
m68k_030b7c:
        lea.l -414(%pc),%a0
m68k_030b7c_end:
.org 0x30B80
m68k_030b80:
        jsr 0x26bfa:l
m68k_030b80_end:
.org 0x30B86
m68k_030b86:
        jsr 0xaf48:l
m68k_030b86_end:
.org 0x30B8C
m68k_030b8c:
        rts
m68k_030b8c_end:
.org 0x30B8E
m68k_030b8e:
        move.w 0xf376:w,%d0
m68k_030b8e_end:
.org 0x30B92
m68k_030b92:
        lsl.w #0x1,%d0
m68k_030b92_end:
.org 0x30B94
m68k_030b94:
        lea.l 0xe640:w,%a0
m68k_030b94_end:
.org 0x30B98
m68k_030b98:
        move.w (%a0, %d0.w),%d0
m68k_030b98_end:
.org 0x30B9C
m68k_030b9c:
        lea.l 0xa050:w,%a0
m68k_030b9c_end:
.org 0x30BA0
m68k_030ba0:
        tst.b (%a0, %d0.w)
m68k_030ba0_end:
.org 0x30BA4
m68k_030ba4:
        bne.w (. + 80)
m68k_030ba4_end:
.org 0x30BA8
m68k_030ba8:
        lea.l 0x9000:w,%a0
m68k_030ba8_end:
.org 0x30BAC
m68k_030bac:
        move.b (%a0),%d2
m68k_030bac_end:
.org 0x30BAE
m68k_030bae:
        andi.w #0xf,%d2
m68k_030bae_end:
.org 0x30BB2
m68k_030bb2:
        beq.w (. + 130)
m68k_030bb2_end:
.org 0x30BB6
m68k_030bb6:
        cmp.b 0x4(%a0),%d1
m68k_030bb6_end:
.org 0x30BBA
m68k_030bba:
        bne.w (. + 20)
m68k_030bba_end:
.org 0x30BBE
m68k_030bbe:
        move.w %d2,%d3
m68k_030bbe_end:
.org 0x30BC0
m68k_030bc0:
        subq.w #0x1,%d3
m68k_030bc0_end:
.org 0x30BC2
m68k_030bc2:
        cmp.b 0xd(%a0, %d3.w),%d0
m68k_030bc2_end:
.org 0x30BC6
m68k_030bc6:
        beq.w (. + 14)
m68k_030bc6_end:
.org 0x30BCA
m68k_030bca:
        dbra %d3,(. + -8)
m68k_030bca_end:
.org 0x30BCE
m68k_030bce:
        lea.l 0xd(%a0, %d2.w),%a0
m68k_030bce_end:
.org 0x30BD2
m68k_030bd2:
        bra.b (. + -38)
m68k_030bd2_end:
.org 0x30BD4
m68k_030bd4:
        clr.w %d0
m68k_030bd4_end:
.org 0x30BD6
m68k_030bd6:
        move.b 0x1(%a0),%d0
m68k_030bd6_end:
.org 0x30BDA
m68k_030bda:
        lsl.w #0x4,%d0
m68k_030bda_end:
.org 0x30BDC
m68k_030bdc:
        move.w %d0,0xf35e:w
m68k_030bdc_end:
.org 0x30BE0
m68k_030be0:
        clr.w %d0
m68k_030be0_end:
.org 0x30BE2
m68k_030be2:
        move.b 0x2(%a0),%d0
m68k_030be2_end:
.org 0x30BE6
m68k_030be6:
        lsl.w #0x4,%d0
m68k_030be6_end:
.org 0x30BE8
m68k_030be8:
        move.w %d0,0xf360:w
m68k_030be8_end:
.org 0x30BEC
m68k_030bec:
        andi.w #0xfffe,%sr
m68k_030bec_end:
.org 0x30BF0
m68k_030bf0:
        bra.w (. + 72)
m68k_030bf0_end:
.org 0x30BF4
m68k_030bf4:
        lea.l 0x9000:w,%a0
m68k_030bf4_end:
.org 0x30BF8
m68k_030bf8:
        move.w 0xf376:w,%d0
m68k_030bf8_end:
.org 0x30BFC
m68k_030bfc:
        move.b (%a0),%d1
m68k_030bfc_end:
.org 0x30BFE
m68k_030bfe:
        andi.w #0xf,%d1
m68k_030bfe_end:
.org 0x30C02
m68k_030c02:
        beq.w (. + 50)
m68k_030c02_end:
.org 0x30C06
m68k_030c06:
        cmp.b 0x4(%a0),%d0
m68k_030c06_end:
.org 0x30C0A
m68k_030c0a:
        beq.w (. + 10)
m68k_030c0a_end:
.org 0x30C0E
m68k_030c0e:
        lea.l 0xd(%a0, %d1.w),%a0
m68k_030c0e_end:
.org 0x30C12
m68k_030c12:
        bra.b (. + -22)
m68k_030c12_end:
.org 0x30C14
m68k_030c14:
        clr.w %d0
m68k_030c14_end:
.org 0x30C16
m68k_030c16:
        move.b 0x1(%a0),%d0
m68k_030c16_end:
.org 0x30C1A
m68k_030c1a:
        lsl.w #0x4,%d0
m68k_030c1a_end:
.org 0x30C1C
m68k_030c1c:
        move.w %d0,0xf35e:w
m68k_030c1c_end:
.org 0x30C20
m68k_030c20:
        clr.w %d0
m68k_030c20_end:
.org 0x30C22
m68k_030c22:
        move.b 0x2(%a0),%d0
m68k_030c22_end:
.org 0x30C26
m68k_030c26:
        lsl.w #0x4,%d0
m68k_030c26_end:
.org 0x30C28
m68k_030c28:
        move.w %d0,0xf360:w
m68k_030c28_end:
.org 0x30C2C
m68k_030c2c:
        andi.w #0xfffe,%sr
m68k_030c2c_end:
.org 0x30C30
m68k_030c30:
        bra.w (. + 8)
m68k_030c30_end:
.org 0x30C34
m68k_030c34:
        ori.w #0x1,%sr
m68k_030c34_end:
.org 0x30C38
m68k_030c38:
        rts
m68k_030c38_end:
.org 0x30C3A
m68k_030c3a:
        lea.l 0x9000:w,%a0
m68k_030c3a_end:
.org 0x30C3E
m68k_030c3e:
        move.b (%a0),%d0
m68k_030c3e_end:
.org 0x30C40
m68k_030c40:
        andi.w #0xf,%d0
m68k_030c40_end:
.org 0x30C44
m68k_030c44:
        beq.w (. + 74)
m68k_030c44_end:
.org 0x30C48
m68k_030c48:
        bsr.w (. + 72)
m68k_030c48_end:
.org 0x30C4C
m68k_030c4c:
        move.b 0x9(%a0),%d2
m68k_030c4c_end:
.org 0x30C50
m68k_030c50:
        lsl.w #0x8,%d2
m68k_030c50_end:
.org 0x30C52
m68k_030c52:
        move.b 0xa(%a0),%d2
m68k_030c52_end:
.org 0x30C56
m68k_030c56:
        lsl.l #0x8,%d2
m68k_030c56_end:
.org 0x30C58
m68k_030c58:
        move.b 0xb(%a0),%d2
m68k_030c58_end:
.org 0x30C5C
m68k_030c5c:
        lsl.l #0x8,%d2
m68k_030c5c_end:
.org 0x30C5E
m68k_030c5e:
        move.b 0xc(%a0),%d2
m68k_030c5e_end:
.org 0x30C62
m68k_030c62:
        sub.l %d3,%d2
m68k_030c62_end:
.org 0x30C64
m68k_030c64:
        bcc.w (. + 14)
m68k_030c64_end:
.org 0x30C68
m68k_030c68:
        bsr.w (. + 90)
m68k_030c68_end:
.org 0x30C6C
m68k_030c6c:
        tst.w %d0
m68k_030c6c_end:
.org 0x30C6E
m68k_030c6e:
        beq.b (. + -48)
m68k_030c6e_end:
.org 0x30C70
m68k_030c70:
        moveq #0,%d2
m68k_030c70_end:
.org 0x30C72
m68k_030c72:
        move.b %d2,0xc(%a0)
m68k_030c72_end:
.org 0x30C76
m68k_030c76:
        lsr.l #0x8,%d2
m68k_030c76_end:
.org 0x30C78
m68k_030c78:
        move.b %d2,0xb(%a0)
m68k_030c78_end:
.org 0x30C7C
m68k_030c7c:
        lsr.l #0x8,%d2
m68k_030c7c_end:
.org 0x30C7E
m68k_030c7e:
        move.b %d2,0xa(%a0)
m68k_030c7e_end:
.org 0x30C82
m68k_030c82:
        lsr.w #0x8,%d2
m68k_030c82_end:
.org 0x30C84
m68k_030c84:
        move.b %d2,0x9(%a0)
m68k_030c84_end:
.org 0x30C88
m68k_030c88:
        lea.l 0xd(%a0, %d0.w),%a0
m68k_030c88_end:
.org 0x30C8C
m68k_030c8c:
        bra.b (. + -78)
m68k_030c8c_end:
.org 0x30C8E
m68k_030c8e:
        rts
m68k_030c8e_end:
.org 0x30C90
m68k_030c90:
        lea.l 0xc800:w,%a1
m68k_030c90_end:
.org 0x30C94
m68k_030c94:
        move.w %d0,%d1
m68k_030c94_end:
.org 0x30C96
m68k_030c96:
        subq.w #0x1,%d1
m68k_030c96_end:
.org 0x30C98
m68k_030c98:
        moveq #0,%d3
m68k_030c98_end:
.org 0x30C9A
m68k_030c9a:
        clr.w %d2
m68k_030c9a_end:
.org 0x30C9C
m68k_030c9c:
        move.b 0xd(%a0, %d1.w),%d2
m68k_030c9c_end:
.org 0x30CA0
m68k_030ca0:
        lsl.w #0x2,%d2
m68k_030ca0_end:
.org 0x30CA2
m68k_030ca2:
        add.l (%a1, %d2.w),%d3
m68k_030ca2_end:
.org 0x30CA6
m68k_030ca6:
        addi.l #0x64,%d3
m68k_030ca6_end:
.org 0x30CAC
m68k_030cac:
        dbra %d1,(. + -18)
m68k_030cac_end:
.org 0x30CB0
m68k_030cb0:
        divu.w #0xa,%d3
m68k_030cb0_end:
.org 0x30CB4
m68k_030cb4:
        move.w %d3,%d2
m68k_030cb4_end:
.org 0x30CB6
m68k_030cb6:
        lsl.w #0x1,%d3
m68k_030cb6_end:
.org 0x30CB8
m68k_030cb8:
        add.w %d2,%d3
m68k_030cb8_end:
.org 0x30CBA
m68k_030cba:
        andi.l #0xffff,%d3
m68k_030cba_end:
.org 0x30CC0
m68k_030cc0:
        rts
m68k_030cc0_end:
.org 0x30CC2
m68k_030cc2:
        clr.w 0xcfc8:w
m68k_030cc2_end:
.org 0x30CC6
m68k_030cc6:
        move.b 0xd(%a0),0xcfc9:w
m68k_030cc6_end:
.org 0x30CCC
m68k_030ccc:
        clr.w %d7
m68k_030ccc_end:
.org 0x30CCE
m68k_030cce:
        lea.l 0xc800:w,%a1
m68k_030cce_end:
.org 0x30CD2
m68k_030cd2:
        lea.l 0xb200:w,%a2
m68k_030cd2_end:
.org 0x30CD6
m68k_030cd6:
        lea.l 0xcfb2:w,%a3
m68k_030cd6_end:
.org 0x30CDA
m68k_030cda:
        lea.l 0xcc00:w,%a4
m68k_030cda_end:
.org 0x30CDE
m68k_030cde:
        move.w %d0,%d1
m68k_030cde_end:
.org 0x30CE0
m68k_030ce0:
        subq.w #0x1,%d1
m68k_030ce0_end:
.org 0x30CE2
m68k_030ce2:
        bsr.w (. + 156)
m68k_030ce2_end:
.org 0x30CE6
m68k_030ce6:
        clr.w %d4
m68k_030ce6_end:
.org 0x30CE8
m68k_030ce8:
        move.b 0xd(%a0, %d1.w),%d4
m68k_030ce8_end:
.org 0x30CEC
m68k_030cec:
        move.w %d4,%d5
m68k_030cec_end:
.org 0x30CEE
m68k_030cee:
        lsl.w #0x1,%d5
m68k_030cee_end:
.org 0x30CF0
m68k_030cf0:
        move.w (%a2, %d5.w),%d6
m68k_030cf0_end:
.org 0x30CF4
m68k_030cf4:
        sub.w %d2,%d6
m68k_030cf4_end:
.org 0x30CF6
m68k_030cf6:
        bls.w (. + 34)
m68k_030cf6_end:
.org 0x30CFA
m68k_030cfa:
        move.w %d6,(%a2, %d5.w)
m68k_030cfa_end:
.org 0x30CFE
m68k_030cfe:
        lsl.w #0x1,%d5
m68k_030cfe_end:
.org 0x30D00
m68k_030d00:
        move.w 0x2(%a1, %d5.w),%d6
m68k_030d00_end:
.org 0x30D04
m68k_030d04:
        sub.w %d3,%d6
m68k_030d04_end:
.org 0x30D06
m68k_030d06:
        bcc.w (. + 6)
m68k_030d06_end:
.org 0x30D0A
m68k_030d0a:
        clr.w %d6
m68k_030d0a_end:
.org 0x30D0C
m68k_030d0c:
        move.w %d6,0x2(%a1, %d5.w)
m68k_030d0c_end:
.org 0x30D10
m68k_030d10:
        addq.w #0x1,%d7
m68k_030d10_end:
.org 0x30D12
m68k_030d12:
        move.b %d4,(%a3)+
m68k_030d12_end:
.org 0x30D14
m68k_030d14:
        bra.w (. + 88)
m68k_030d14_end:
.org 0x30D18
m68k_030d18:
        move.b #0xff,(%a4, %d4.w)
m68k_030d18_end:
.org 0x30D1E
m68k_030d1e:
        move.b 0x4(%a0),%d2
m68k_030d1e_end:
.org 0x30D22
m68k_030d22:
        andi.w #0xf,%d2
m68k_030d22_end:
.org 0x30D26
m68k_030d26:
        cmp.w 0xf67a:w,%d2
m68k_030d26_end:
.org 0x30D2A
m68k_030d2a:
        beq.w (. + 20)
m68k_030d2a_end:
.org 0x30D2E
m68k_030d2e:
        cmp.w 0xf67c:w,%d2
m68k_030d2e_end:
.org 0x30D32
m68k_030d32:
        beq.w (. + 12)
m68k_030d32_end:
.org 0x30D36
m68k_030d36:
        cmp.w 0xf67e:w,%d2
m68k_030d36_end:
.org 0x30D3A
m68k_030d3a:
        bne.w (. + 50)
m68k_030d3a_end:
.org 0x30D3E
m68k_030d3e:
        move.w 0xf362:w,-(%a7)
m68k_030d3e_end:
.org 0x30D42
m68k_030d42:
        move.w 0xf376:w,-(%a7)
m68k_030d42_end:
.org 0x30D46
m68k_030d46:
        movem.l %d0-%d7/%a0-%a6,-(%a7)
m68k_030d46_end:
.org 0x30D4A
m68k_030d4a:
        move.w %d2,0xf376:w
m68k_030d4a_end:
.org 0x30D4E
m68k_030d4e:
        move.w %d4,0xf3d0:w
m68k_030d4e_end:
.org 0x30D52
m68k_030d52:
        move.w #0xca,0xf740:w
m68k_030d52_end:
.org 0x30D58
m68k_030d58:
        clr.w 0xf362:w
m68k_030d58_end:
.org 0x30D5C
m68k_030d5c:
        jsr -746(%pc)
m68k_030d5c_end:
.org 0x30D60
m68k_030d60:
        movem.l (%a7)+,%d0-%d7/%a0-%a6
m68k_030d60_end:
.org 0x30D64
m68k_030d64:
        move.w (%a7)+,0xf376:w
m68k_030d64_end:
.org 0x30D68
m68k_030d68:
        move.w (%a7)+,0xf362:w
m68k_030d68_end:
.org 0x30D6C
m68k_030d6c:
        dbra %d1,(. + -138)
m68k_030d6c_end:
.org 0x30D70
m68k_030d70:
        cmp.w %d7,%d0
m68k_030d70_end:
.org 0x30D72
m68k_030d72:
        beq.w (. + 8)
m68k_030d72_end:
.org 0x30D76
m68k_030d76:
        bsr.w (. + 80)
m68k_030d76_end:
.org 0x30D7A
m68k_030d7a:
        move.w %d7,%d0
m68k_030d7a_end:
.org 0x30D7C
m68k_030d7c:
        rts
m68k_030d7c_end:
.org 0x30D7E
m68k_030d7e:
        movem.l %d0-%d1,-(%a7)
m68k_030d7e_end:
.org 0x30D82
m68k_030d82:
        jsr 0x83d4:l
m68k_030d82_end:
.org 0x30D88
m68k_030d88:
        andi.l #0xffff,%d0
m68k_030d88_end:
.org 0x30D8E
m68k_030d8e:
        move.l %d0,%d1
m68k_030d8e_end:
.org 0x30D90
m68k_030d90:
        lsl.l #0x1,%d0
m68k_030d90_end:
.org 0x30D92
m68k_030d92:
        add.l %d1,%d0
m68k_030d92_end:
.org 0x30D94
m68k_030d94:
        lsl.l #0x1,%d0
m68k_030d94_end:
.org 0x30D96
m68k_030d96:
        swap %d0
m68k_030d96_end:
.org 0x30D98
m68k_030d98:
        addq.w #0x5,%d0
m68k_030d98_end:
.org 0x30D9A
m68k_030d9a:
        move.w %d0,%d2
m68k_030d9a_end:
.org 0x30D9C
m68k_030d9c:
        jsr 0x83d4:l
m68k_030d9c_end:
.org 0x30DA2
m68k_030da2:
        andi.l #0xffff,%d0
m68k_030da2_end:
.org 0x30DA8
m68k_030da8:
        move.l %d0,%d1
m68k_030da8_end:
.org 0x30DAA
m68k_030daa:
        lsl.l #0x8,%d0
m68k_030daa_end:
.org 0x30DAC
m68k_030dac:
        lsl.l #0x1,%d0
m68k_030dac_end:
.org 0x30DAE
m68k_030dae:
        sub.l %d1,%d0
m68k_030dae_end:
.org 0x30DB0
m68k_030db0:
        lsl.l #0x1,%d1
m68k_030db0_end:
.org 0x30DB2
m68k_030db2:
        sub.l %d1,%d0
m68k_030db2_end:
.org 0x30DB4
m68k_030db4:
        lsl.l #0x2,%d1
m68k_030db4_end:
.org 0x30DB6
m68k_030db6:
        sub.l %d1,%d0
m68k_030db6_end:
.org 0x30DB8
m68k_030db8:
        swap %d0
m68k_030db8_end:
.org 0x30DBA
m68k_030dba:
        addi.w #0x1f4,%d0
m68k_030dba_end:
.org 0x30DBE
m68k_030dbe:
        move.w %d0,%d3
m68k_030dbe_end:
.org 0x30DC0
m68k_030dc0:
        movem.l (%a7)+,%d0-%d1
m68k_030dc0_end:
.org 0x30DC4
m68k_030dc4:
        rts
m68k_030dc4_end:
.org 0x30DC6
m68k_030dc6:
        move.w %d7,%d6
m68k_030dc6_end:
.org 0x30DC8
m68k_030dc8:
        beq.w (. + 36)
m68k_030dc8_end:
.org 0x30DCC
m68k_030dcc:
        subq.w #0x1,%d6
m68k_030dcc_end:
.org 0x30DCE
m68k_030dce:
        lea.l 0xcfb2:w,%a1
m68k_030dce_end:
.org 0x30DD2
m68k_030dd2:
        move.b (%a1)+,0xd(%a0, %d6.w)
m68k_030dd2_end:
.org 0x30DD6
m68k_030dd6:
        dbra %d6,(. + -4)
m68k_030dd6_end:
.org 0x30DDA
m68k_030dda:
        move.b %d7,(%a0)
m68k_030dda_end:
.org 0x30DDC
m68k_030ddc:
        bsr.w (. + 88)
m68k_030ddc_end:
.org 0x30DE0
m68k_030de0:
        lea.l 0xd(%a0, %d0.w),%a1
m68k_030de0_end:
.org 0x30DE4
m68k_030de4:
        lea.l 0xd(%a0, %d7.w),%a2
m68k_030de4_end:
.org 0x30DE8
m68k_030de8:
        bra.w (. + 14)
m68k_030de8_end:
.org 0x30DEC
m68k_030dec:
        bsr.w (. + 144)
m68k_030dec_end:
.org 0x30DF0
m68k_030df0:
        lea.l 0xd(%a0, %d0.w),%a1
m68k_030df0_end:
.org 0x30DF4
m68k_030df4:
        lea.l (%a0),%a2
m68k_030df4_end:
.org 0x30DF6
m68k_030df6:
        move.b (%a1),%d1
m68k_030df6_end:
.org 0x30DF8
m68k_030df8:
        andi.w #0xf,%d1
m68k_030df8_end:
.org 0x30DFC
m68k_030dfc:
        beq.w (. + 16)
m68k_030dfc_end:
.org 0x30E00
m68k_030e00:
        addi.w #0xc,%d1
m68k_030e00_end:
.org 0x30E04
m68k_030e04:
        move.b (%a1)+,(%a2)+
m68k_030e04_end:
.org 0x30E06
m68k_030e06:
        dbra %d1,(. + -2)
m68k_030e06_end:
.org 0x30E0A
m68k_030e0a:
        bra.b (. + -20)
m68k_030e0a_end:
.org 0x30E0C
m68k_030e0c:
        clr.b (%a2)
m68k_030e0c_end:
.org 0x30E0E
m68k_030e0e:
        tst.w %d7
m68k_030e0e_end:
.org 0x30E10
m68k_030e10:
        beq.w (. + 34)
m68k_030e10_end:
.org 0x30E14
m68k_030e14:
        lea.l 0xc400:w,%a1
m68k_030e14_end:
.org 0x30E18
m68k_030e18:
        move.w %d7,%d6
m68k_030e18_end:
.org 0x30E1A
m68k_030e1a:
        subq.w #0x1,%d6
m68k_030e1a_end:
.org 0x30E1C
m68k_030e1c:
        moveq #0,%d2
m68k_030e1c_end:
.org 0x30E1E
m68k_030e1e:
        clr.w %d3
m68k_030e1e_end:
.org 0x30E20
m68k_030e20:
        move.b 0xd(%a0, %d6.w),%d3
m68k_030e20_end:
.org 0x30E24
m68k_030e24:
        add.b (%a1, %d3.w),%d2
m68k_030e24_end:
.org 0x30E28
m68k_030e28:
        dbra %d6,(. + -8)
m68k_030e28_end:
.org 0x30E2C
m68k_030e2c:
        divu.w %d7,%d2
m68k_030e2c_end:
.org 0x30E2E
m68k_030e2e:
        move.b %d2,0x3(%a0)
m68k_030e2e_end:
.org 0x30E32
m68k_030e32:
        rts
m68k_030e32_end:
.org 0x30E34
m68k_030e34:
        movem.l %d0-%d1/%a0,-(%a7)
m68k_030e34_end:
.org 0x30E38
m68k_030e38:
        clr.w %d0
m68k_030e38_end:
.org 0x30E3A
m68k_030e3a:
        move.b 0xd(%a0),%d0
m68k_030e3a_end:
.org 0x30E3E
m68k_030e3e:
        move.w 0xcfc8:w,%d1
m68k_030e3e_end:
.org 0x30E42
m68k_030e42:
        lea.l 0xff39b2:l,%a0
m68k_030e42_end:
.org 0x30E48
m68k_030e48:
        tst.b (%a0)
m68k_030e48_end:
.org 0x30E4A
m68k_030e4a:
        beq.w (. + 44)
m68k_030e4a_end:
.org 0x30E4E
m68k_030e4e:
        cmp.b 0x1(%a0),%d1
m68k_030e4e_end:
.org 0x30E52
m68k_030e52:
        beq.w (. + 8)
m68k_030e52_end:
.org 0x30E56
m68k_030e56:
        addq.w #0x2,%a0
m68k_030e56_end:
.org 0x30E58
m68k_030e58:
        bra.b (. + -16)
m68k_030e58_end:
.org 0x30E5A
m68k_030e5a:
        move.b %d0,0x1(%a0)
m68k_030e5a_end:
.org 0x30E5E
m68k_030e5e:
        lea.l 0xff3000:l,%a0
m68k_030e5e_end:
.org 0x30E64
m68k_030e64:
        addq.w #0x1,%a0
m68k_030e64_end:
.org 0x30E66
m68k_030e66:
        cmp.b (%a0),%d1
m68k_030e66_end:
.org 0x30E68
m68k_030e68:
        beq.w (. + 12)
m68k_030e68_end:
.org 0x30E6C
m68k_030e6c:
        addq.w #0x1,%a0
m68k_030e6c_end:
.org 0x30E6E
m68k_030e6e:
        tst.b (%a0)+
m68k_030e6e_end:
.org 0x30E70
m68k_030e70:
        bne.b (. + -2)
m68k_030e70_end:
.org 0x30E72
m68k_030e72:
        bra.b (. + -14)
m68k_030e72_end:
.org 0x30E74
m68k_030e74:
        move.b %d0,(%a0)
m68k_030e74_end:
.org 0x30E76
m68k_030e76:
        movem.l (%a7)+,%d0-%d1/%a0
m68k_030e76_end:
.org 0x30E7A
m68k_030e7a:
        rts
m68k_030e7a_end:
.org 0x30E7C
m68k_030e7c:
        movem.l %d0-%d1/%a0-%a1,-(%a7)
m68k_030e7c_end:
.org 0x30E80
m68k_030e80:
        lea.l 0xff39b2:l,%a0
m68k_030e80_end:
.org 0x30E86
m68k_030e86:
        move.w 0xcfc8:w,%d0
m68k_030e86_end:
.org 0x30E8A
m68k_030e8a:
        tst.b (%a0)
m68k_030e8a_end:
.org 0x30E8C
m68k_030e8c:
        beq.w (. + 34)
m68k_030e8c_end:
.org 0x30E90
m68k_030e90:
        cmp.b 0x1(%a0),%d0
m68k_030e90_end:
.org 0x30E94
m68k_030e94:
        beq.w (. + 8)
m68k_030e94_end:
.org 0x30E98
m68k_030e98:
        addq.w #0x2,%a0
m68k_030e98_end:
.org 0x30E9A
m68k_030e9a:
        bra.b (. + -16)
m68k_030e9a_end:
.org 0x30E9C
m68k_030e9c:
        move.b 0x2(%a0),(%a0)
m68k_030e9c_end:
.org 0x30EA0
m68k_030ea0:
        beq.w (. + 14)
m68k_030ea0_end:
.org 0x30EA4
m68k_030ea4:
        move.b 0x3(%a0),0x1(%a0)
m68k_030ea4_end:
.org 0x30EAA
m68k_030eaa:
        addq.w #0x2,%a0
m68k_030eaa_end:
.org 0x30EAC
m68k_030eac:
        bra.b (. + -16)
m68k_030eac_end:
.org 0x30EAE
m68k_030eae:
        movem.l (%a7)+,%d0-%d1/%a0-%a1
m68k_030eae_end:
.org 0x30EB2
m68k_030eb2:
        rts
m68k_030eb2_end:
.org 0x30F54
m68k_030f54:
        lea.l 0xcc00:w,%a0
m68k_030f54_end:
.org 0x30F58
m68k_030f58:
        lea.l 0xb200:w,%a3
m68k_030f58_end:
.org 0x30F5C
m68k_030f5c:
        lea.l 0xb000:w,%a4
m68k_030f5c_end:
.org 0x30F60
m68k_030f60:
        lea.l 0xea38:w,%a5
m68k_030f60_end:
.org 0x30F64
m68k_030f64:
        move.w #0xff,%d0
m68k_030f64_end:
.org 0x30F68
m68k_030f68:
        clr.w %d1
m68k_030f68_end:
.org 0x30F6A
m68k_030f6a:
        move.b (%a0, %d0.w),%d1
m68k_030f6a_end:
.org 0x30F6E
m68k_030f6e:
        cmpi.b #0x28,%d1
m68k_030f6e_end:
.org 0x30F72
m68k_030f72:
        bhi.w (. + 50)
m68k_030f72_end:
.org 0x30F76
m68k_030f76:
        tst.b (%a5, %d1.w)
m68k_030f76_end:
.org 0x30F7A
m68k_030f7a:
        bne.w (. + 42)
m68k_030f7a_end:
.org 0x30F7E
m68k_030f7e:
        move.w %d0,%d1
m68k_030f7e_end:
.org 0x30F80
m68k_030f80:
        lsl.w #0x1,%d1
m68k_030f80_end:
.org 0x30F82
m68k_030f82:
        move.w (%a4, %d1.w),%d2
m68k_030f82_end:
.org 0x30F86
m68k_030f86:
        mulu.w #0xf,%d2
m68k_030f86_end:
.org 0x30F8A
m68k_030f8a:
        divu.w #0x64,%d2
m68k_030f8a_end:
.org 0x30F8E
m68k_030f8e:
        move.w (%a3, %d1.w),%d3
m68k_030f8e_end:
.org 0x30F92
m68k_030f92:
        add.w %d2,%d3
m68k_030f92_end:
.org 0x30F94
m68k_030f94:
        cmp.w (%a4, %d1.w),%d3
m68k_030f94_end:
.org 0x30F98
m68k_030f98:
        bls.w (. + 8)
m68k_030f98_end:
.org 0x30F9C
m68k_030f9c:
        move.w (%a4, %d1.w),%d3
m68k_030f9c_end:
.org 0x30FA0
m68k_030fa0:
        move.w %d3,(%a3, %d1.w)
m68k_030fa0_end:
.org 0x30FA4
m68k_030fa4:
        dbra %d0,(. + -60)
m68k_030fa4_end:
.org 0x30FA8
m68k_030fa8:
        rts
m68k_030fa8_end:
.org 0x31024
m68k_031024:
        bsr.w (. + 80)
m68k_031024_end:
.org 0x31028
m68k_031028:
        tst.w 0xf364:w
m68k_031028_end:
.org 0x3102C
m68k_03102c:
        bmi.w (. + 22)
m68k_03102c_end:
.org 0x31030
m68k_031030:
        bsr.w (. + 374)
m68k_031030_end:
.org 0x31034
m68k_031034:
        move.w #0x1,0xf728:w
m68k_031034_end:
.org 0x3103A
m68k_03103a:
        jsr 0x338c2:l
m68k_03103a_end:
.org 0x31040
m68k_031040:
        bra.b (. + -28)
m68k_031040_end:
.org 0x31042
m68k_031042:
        rts
m68k_031042_end:
.org 0x31044
m68k_031044:
        bsr.w (. + 106)
m68k_031044_end:
.org 0x31048
m68k_031048:
        tst.w 0xf75a:w
m68k_031048_end:
.org 0x3104C
m68k_03104c:
        bmi.w (. + 38)
m68k_03104c_end:
.org 0x31050
m68k_031050:
        move.w #0x1,0xf728:w
m68k_031050_end:
.org 0x31056
m68k_031056:
        jsr 0x340f8:l
m68k_031056_end:
.org 0x3105C
m68k_03105c:
        lea.l 0x9000:w,%a0
m68k_03105c_end:
.org 0x31060
m68k_031060:
        adda.w 0xf75a:w,%a0
m68k_031060_end:
.org 0x31064
m68k_031064:
        clr.w %d0
m68k_031064_end:
.org 0x31066
m68k_031066:
        move.b (%a0),%d0
m68k_031066_end:
.org 0x31068
m68k_031068:
        addi.w #0xd,%d0
m68k_031068_end:
.org 0x3106C
m68k_03106c:
        add.w %d0,0xf75a:w
m68k_03106c_end:
.org 0x31070
m68k_031070:
        bra.b (. + -44)
m68k_031070_end:
.org 0x31072
m68k_031072:
        rts
m68k_031072_end:
.org 0x310AE
m68k_0310ae:
        lea.l 0x9000:w,%a0
m68k_0310ae_end:
.org 0x310B2
m68k_0310b2:
        adda.w 0xf75a:w,%a0
m68k_0310b2_end:
.org 0x310B6
m68k_0310b6:
        move.w 0xf376:w,%d0
m68k_0310b6_end:
.org 0x310BA
m68k_0310ba:
        move.b (%a0),%d1
m68k_0310ba_end:
.org 0x310BC
m68k_0310bc:
        btst.l #0x5,%d1
m68k_0310bc_end:
.org 0x310C0
m68k_0310c0:
        bne.w (. + 20)
m68k_0310c0_end:
.org 0x310C4
m68k_0310c4:
        andi.w #0xf,%d1
m68k_0310c4_end:
.org 0x310C8
m68k_0310c8:
        beq.w (. + 34)
m68k_0310c8_end:
.org 0x310CC
m68k_0310cc:
        cmp.b 0x4(%a0),%d0
m68k_0310cc_end:
.org 0x310D0
m68k_0310d0:
        beq.w (. + 36)
m68k_0310d0_end:
.org 0x310D4
m68k_0310d4:
        andi.w #0xf,%d1
m68k_0310d4_end:
.org 0x310D8
m68k_0310d8:
        beq.w (. + 18)
m68k_0310d8_end:
.org 0x310DC
m68k_0310dc:
        lea.l 0xd(%a0, %d1.w),%a0
m68k_0310dc_end:
.org 0x310E0
m68k_0310e0:
        addi.w #0xd,%d1
m68k_0310e0_end:
.org 0x310E4
m68k_0310e4:
        add.w %d1,0xf75a:w
m68k_0310e4_end:
.org 0x310E8
m68k_0310e8:
        bra.b (. + -46)
m68k_0310e8_end:
.org 0x310EA
m68k_0310ea:
        move.w #0xffff,0xf75a:w
m68k_0310ea_end:
.org 0x310F0
m68k_0310f0:
        bra.w (. + 30)
m68k_0310f0_end:
.org 0x310F4
m68k_0310f4:
        clr.w %d0
m68k_0310f4_end:
.org 0x310F6
m68k_0310f6:
        move.b 0x1(%a0),%d0
m68k_0310f6_end:
.org 0x310FA
m68k_0310fa:
        move.w %d0,0xf75c:w
m68k_0310fa_end:
.org 0x310FE
m68k_0310fe:
        move.b 0x2(%a0),%d0
m68k_0310fe_end:
.org 0x31102
m68k_031102:
        move.w %d0,0xf75e:w
m68k_031102_end:
.org 0x31106
m68k_031106:
        move.b 0x3(%a0),%d0
m68k_031106_end:
.org 0x3110A
m68k_03110a:
        move.w %d0,0xf760:w
m68k_03110a_end:
.org 0x3110E
m68k_03110e:
        rts
m68k_03110e_end:
.org 0x31148
m68k_031148:
        addq.w #0x4,%d2
m68k_031148_end:
.org 0x311FA
m68k_0311fa:
        rts
m68k_0311fa_end:
.org 0x317E8
m68k_0317e8:
        subq.w #0x1,0xf608:w
m68k_0317e8_end:
.org 0x317EC
m68k_0317ec:
        bne.w (. + 26)
m68k_0317ec_end:
.org 0x317F0
m68k_0317f0:
        move.w #0xc,0xf608:w
m68k_0317f0_end:
.org 0x317F6
m68k_0317f6:
        eori.w #0x1,0xf386:w
m68k_0317f6_end:
.org 0x317FC
m68k_0317fc:
        bra.w (. + 10)
m68k_0317fc_end:
.org 0x319AA
m68k_0319aa:
        move.w #0x8,0xcfd2:w
m68k_0319aa_end:
.org 0x319B0
m68k_0319b0:
        bra.w (. + 34)
m68k_0319b0_end:
.org 0x31AE0
m68k_031ae0:
        move.w #0x3,0xf728:w
m68k_031ae0_end:
.org 0x31AE6
m68k_031ae6:
        bra.w (. + 10)
m68k_031ae6_end:
.org 0x31B0E
m68k_031b0e:
        clr.w %d1
m68k_031b0e_end:
.org 0x31B22
m68k_031b22:
        clr.w %d3
m68k_031b22_end:
.org 0x31B36
m68k_031b36:
        cmp.b 0x1(%a0),%d1
m68k_031b36_end:
.org 0x31B3A
m68k_031b3a:
        bhi.w (. + 28)
m68k_031b3a_end:
.org 0x31B3E
m68k_031b3e:
        cmp.b 0x1(%a0),%d2
m68k_031b3e_end:
.org 0x31B42
m68k_031b42:
        bcs.w (. + 20)
m68k_031b42_end:
.org 0x31B46
m68k_031b46:
        cmp.b 0x2(%a0),%d3
m68k_031b46_end:
.org 0x31B4A
m68k_031b4a:
        bhi.w (. + 12)
m68k_031b4a_end:
.org 0x31B4E
m68k_031b4e:
        cmp.b 0x2(%a0),%d4
m68k_031b4e_end:
.org 0x31B52
m68k_031b52:
        bcc.w (. + 10)
m68k_031b52_end:
.org 0x31B56
m68k_031b56:
        lea.l 0xd(%a0, %d0.w),%a0
m68k_031b56_end:
.org 0x31B5A
m68k_031b5a:
        bra.b (. + -46)
m68k_031b5a_end:
.org 0x31B5C
m68k_031b5c:
        ori.w #0x1,%sr
m68k_031b5c_end:
.org 0x31B60
m68k_031b60:
        bra.w (. + 8)
m68k_031b60_end:
.org 0x31B7E
m68k_031b7e:
        jsr 0x83d4:l
m68k_031b7e_end:
.org 0x31B84
m68k_031b84:
        move.w 0xf61c:w,%d0
m68k_031b84_end:
.org 0x31B88
m68k_031b88:
        andi.w #0xf,%d0
m68k_031b88_end:
.org 0x31B8C
m68k_031b8c:
        cmpi.w #0x3,%d0
m68k_031b8c_end:
.org 0x31B90
m68k_031b90:
        bcc.w (. + 14)
m68k_031b90_end:
.org 0x31C2A
m68k_031c2a:
        addq.w #0x1,%d2
m68k_031c2a_end:
.org 0x31C76
m68k_031c76:
        cmpi.w #0x96,(%a3, %d0.w)
m68k_031c76_end:
.org 0x31C7C
m68k_031c7c:
        bcs.b (. + -38)
m68k_031c7c_end:
.org 0x31C7E
m68k_031c7e:
        ori.w #0x1,%sr
m68k_031c7e_end:
.org 0x31C82
m68k_031c82:
        bra.w (. + 8)
m68k_031c82_end:
.org 0x31CF2
m68k_031cf2:
        andi.w #0x7,%d0
m68k_031cf2_end:
.org 0x31CF6
m68k_031cf6:
        cmpi.w #0x7,%d0
m68k_031cf6_end:
.org 0x31CFA
m68k_031cfa:
        bne.w (. + 66)
m68k_031cfa_end:
.org 0x31CFE
m68k_031cfe:
        bra.w (. + 72)
m68k_031cfe_end:
.org 0x31D18
m68k_031d18:
        bra.w (. + 46)
m68k_031d18_end:
.org 0x31D2C
m68k_031d2c:
        bra.w (. + 26)
m68k_031d2c_end:
.org 0x31EEA
m68k_031eea:
        cmp.w %d3,%d4
m68k_031eea_end:
.org 0x31EEC
m68k_031eec:
        bcc.w (. + 12)
m68k_031eec_end:
.org 0x31F14
m68k_031f14:
        lea.l 0xf72a:w,%a0
m68k_031f14_end:
.org 0x31F18
m68k_031f18:
        lea.l 0xf500:w,%a1
m68k_031f18_end:
.org 0x31F1C
m68k_031f1c:
        move.w (%a0)+,%d0
m68k_031f1c_end:
.org 0x31F1E
m68k_031f1e:
        bmi.b (. + 12)
m68k_031f1e_end:
.org 0x31F20
m68k_031f20:
        cmp.w 0xf3a6:w,%d0
m68k_031f20_end:
.org 0x31F24
m68k_031f24:
        beq.b (. + -8)
m68k_031f24_end:
.org 0x31F26
m68k_031f26:
        move.w %d0,(%a1)+
m68k_031f26_end:
.org 0x31F28
m68k_031f28:
        bra.b (. + -12)
m68k_031f28_end:
.org 0x31F2A
m68k_031f2a:
        move.w #0xffff,(%a1)
m68k_031f2a_end:
.org 0x31F2E
m68k_031f2e:
        move.w 0xf364:w,%d0
m68k_031f2e_end:
.org 0x31F32
m68k_031f32:
        jsr 0xe1f6:l
m68k_031f32_end:
.org 0x31F68
m68k_031f68:
        lea.l 0xf45e:w,%a0
m68k_031f68_end:
.org 0x31F6C
m68k_031f6c:
        move.w 0xf392:w,%d0
m68k_031f6c_end:
.org 0x31F70
m68k_031f70:
        lsl.w #0x1,%d0
m68k_031f70_end:
.org 0x31F72
m68k_031f72:
        move.w 0xf3a6:w,(%a0, %d0.w)
m68k_031f72_end:
.org 0x3202E
m68k_03202e:
        cmp.b %d3,%d5
m68k_03202e_end:
.org 0x32030
m68k_032030:
        bls.b (. + -36)
m68k_032030_end:
.org 0x32032
m68k_032032:
        move.w %d5,%d3
m68k_032032_end:
.org 0x32034
m68k_032034:
        move.w %d0,%d4
m68k_032034_end:
.org 0x32036
m68k_032036:
        bra.b (. + -42)
m68k_032036_end:
.org 0x32040
m68k_032040:
        move.w %d2,0xf3a6:w
m68k_032040_end:
.org 0x32044
m68k_032044:
        bra.w (. + 22)
m68k_032044_end:
.org 0x3204E
m68k_03204e:
        move.w %d4,0xf3a6:w
m68k_03204e_end:
.org 0x32052
m68k_032052:
        bra.w (. + 8)
m68k_032052_end:
.org 0x3216E
m68k_03216e:
        cmpi.w #0x96,(%a2, %d3.w)
m68k_03216e_end:
.org 0x32174
m68k_032174:
        bcs.b (. + -36)
m68k_032174_end:
.org 0x32176
m68k_032176:
        cmp.w %d0,%d4
m68k_032176_end:
.org 0x32178
m68k_032178:
        bcs.b (. + -40)
m68k_032178_end:
.org 0x3217A
m68k_03217a:
        move.w %d4,%d0
m68k_03217a_end:
.org 0x3217C
m68k_03217c:
        move.w %d2,%d1
m68k_03217c_end:
.org 0x3217E
m68k_03217e:
        bra.b (. + -46)
m68k_03217e_end:
.org 0x32186
m68k_032186:
        lea.l 0xc700:w,%a0
m68k_032186_end:
.org 0x3218A
m68k_03218a:
        bset.b #0x4,(%a0, %d1.w)
m68k_03218a_end:
.org 0x321C8
m68k_0321c8:
        addq.w #0x1,%d1
m68k_0321c8_end:
.org 0x321CA
m68k_0321ca:
        cmpi.b #0xf,%d2
m68k_0321ca_end:
.org 0x321CE
m68k_0321ce:
        bcs.w (. + 16)
m68k_0321ce_end:
.org 0x321D2
m68k_0321d2:
        addq.w #0x1,%d1
m68k_0321d2_end:
.org 0x321D4
m68k_0321d4:
        cmpi.b #0x14,%d2
m68k_0321d4_end:
.org 0x321D8
m68k_0321d8:
        bcs.w (. + 6)
m68k_0321d8_end:
.org 0x321DC
m68k_0321dc:
        addq.w #0x1,%d1
m68k_0321dc_end:
.org 0x321FA
m68k_0321fa:
        bset.l #0x3,%d1
m68k_0321fa_end:
.org 0x32556
m68k_032556:
        subi.w #0xa,%d2
m68k_032556_end:
.org 0x32FC6
m68k_032fc6:
        lea.l 0xd300:w,%a1
m68k_032fc6_end:
.org 0x32FCA
m68k_032fca:
        move.w #0x1f,%d3
m68k_032fca_end:
.org 0x32FCE
m68k_032fce:
        move.l #0x11111111,(%a1)+
m68k_032fce_end:
.org 0x32FD4
m68k_032fd4:
        dbra %d3,(. + -6)
m68k_032fd4_end:
.org 0x32FD8
m68k_032fd8:
        lea.l 88(%pc),%a0
m68k_032fd8_end:
.org 0x32FDC
m68k_032fdc:
        nop
m68k_032fdc_end:
.org 0x32FDE
m68k_032fde:
        move.w #0x1,%d0
m68k_032fde_end:
.org 0x32FE2
m68k_032fe2:
        move.w #0x3,%d1
m68k_032fe2_end:
.org 0x32FE6
m68k_032fe6:
        move.w #0x2,%d3
m68k_032fe6_end:
.org 0x32FEA
m68k_032fea:
        jsr 0xae8a:l
m68k_032fea_end:
.org 0x32FF0
m68k_032ff0:
        move.l #0x40200000,0xc00004:l
m68k_032ff0_end:
.org 0x32FFA
m68k_032ffa:
        lea.l 0xd300:w,%a1
m68k_032ffa_end:
.org 0x32FFE
m68k_032ffe:
        move.w #0x7f,%d3
m68k_032ffe_end:
.org 0x33002
m68k_033002:
        move.l (%a1)+,0xc00000:l
m68k_033002_end:
.org 0x33008
m68k_033008:
        dbra %d3,(. + -6)
m68k_033008_end:
.org 0x3300C
m68k_03300c:
        jsr 0x55b0:l
m68k_03300c_end:
.org 0x33012
m68k_033012:
        move.w 0xf376:w,0xf3a6:w
m68k_033012_end:
.org 0x33018
m68k_033018:
        move.w 0xf376:w,-(%a7)
m68k_033018_end:
.org 0x3301C
m68k_03301c:
        move.w 0xe730:w,0xf376:w
m68k_03301c_end:
.org 0x33022
m68k_033022:
        move.w #0x9,0xf362:w
m68k_033022_end:
.org 0x33028
m68k_033028:
        bsr.w (. + -9652)
m68k_033028_end:
.org 0x3302C
m68k_03302c:
        move.w (%a7)+,0xf376:w
m68k_03302c_end:
.org 0x33030
m68k_033030:
        rts
m68k_033030_end:
.org 0x330A0
m68k_0330a0:
        jsr 0x10aa8:l
m68k_0330a0_end:
.org 0x330A6
m68k_0330a6:
        jsr 0x10ade:l
m68k_0330a6_end:
.org 0x330AC
m68k_0330ac:
        jsr 0x10c74:l
m68k_0330ac_end:
.org 0x330B2
m68k_0330b2:
        cmpi.w #0x4,%d0
m68k_0330b2_end:
.org 0x330B6
m68k_0330b6:
        bcs.w (. + 14)
m68k_0330b6_end:
.org 0x330BA
m68k_0330ba:
        move.w #0x5,0xf728:w
m68k_0330ba_end:
.org 0x330C0
m68k_0330c0:
        bra.w (. + 10)
m68k_0330c0_end:
.org 0x33128
m68k_033128:
        cmpi.w #0x4b,%d5
m68k_033128_end:
.org 0x3312C
m68k_03312c:
        bcc.w (. + 12)
m68k_03312c_end:
.org 0x33130
m68k_033130:
        cmpi.w #0x4b,%d6
m68k_033130_end:
.org 0x33134
m68k_033134:
        bcs.w (. + 36)
m68k_033134_end:
.org 0x33138
m68k_033138:
        jsr 0x83d4:l
m68k_033138_end:
.org 0x3313E
m68k_03313e:
        btst.l #0x4,%d0
m68k_03313e_end:
.org 0x33142
m68k_033142:
        bne.w (. + 22)
m68k_033142_end:
.org 0x33146
m68k_033146:
        move.w %d2,0xf3f2:w
m68k_033146_end:
.org 0x3314A
m68k_03314a:
        move.w %d3,0xf3a8:w
m68k_03314a_end:
.org 0x3314E
m68k_03314e:
        move.w #0x6,0xf728:w
m68k_03314e_end:
.org 0x33154
m68k_033154:
        bra.w (. + 10)
m68k_033154_end:
.org 0x331B0
m68k_0331b0:
        lsl.w #0x1,%d4
m68k_0331b0_end:
.org 0x331B2
m68k_0331b2:
        move.w (%a1, %d4.w),%d5
m68k_0331b2_end:
.org 0x331B6
m68k_0331b6:
        move.w (%a2, %d4.w),%d6
m68k_0331b6_end:
.org 0x331F8
m68k_0331f8:
        move.w %d4,%d5
m68k_0331f8_end:
.org 0x331FA
m68k_0331fa:
        lsl.w #0x1,%d5
m68k_0331fa_end:
.org 0x331FC
m68k_0331fc:
        move.w (%a1, %d5.w),%d6
m68k_0331fc_end:
.org 0x33200
m68k_033200:
        add.w (%a2, %d5.w),%d6
m68k_033200_end:
.org 0x33204
m68k_033204:
        cmp.w %d1,%d6
m68k_033204_end:
.org 0x33206
m68k_033206:
        bls.w (. + 10)
m68k_033206_end:
.org 0x3320A
m68k_03320a:
        move.w %d6,%d1
m68k_03320a_end:
.org 0x3320C
m68k_03320c:
        move.w %d4,%d2
m68k_03320c_end:
.org 0x3320E
m68k_03320e:
        move.w %d0,%d3
m68k_03320e_end:
.org 0x3326C
m68k_03326c:
        move.w #0x4,0xf728:w
m68k_03326c_end:
.org 0x3328A
m68k_03328a:
        move.w #0x9,0xf728:w
m68k_03328a_end:
.org 0x33612
m68k_033612:
        move.w #0x64,%d3
m68k_033612_end:
.org 0x33616
m68k_033616:
        sub.w %d1,%d3
m68k_033616_end:
.org 0x33618
m68k_033618:
        sub.w %d3,%d2
m68k_033618_end:
.org 0x3361A
m68k_03361a:
        move.w #0x64,%d1
m68k_03361a_end:
.org 0x33634
m68k_033634:
        move.w #0x3e7,(%a0, %d0.w)
m68k_033634_end:
.org 0x33656
m68k_033656:
        bsr.w (. + 16)
m68k_033656_end:
.org 0x3365A
m68k_03365a:
        bsr.w (. + 124)
m68k_03365a_end:
.org 0x336AA
m68k_0336aa:
        move.w (%a2, %d1.w),%d2
m68k_0336aa_end:
.org 0x336AE
m68k_0336ae:
        move.w -0x2(%a2, %d1.w),(%a2, %d1.w)
m68k_0336ae_end:
.org 0x336B4
m68k_0336b4:
        move.w %d2,-0x2(%a2, %d1.w)
m68k_0336b4_end:
.org 0x336B8
m68k_0336b8:
        move.w (%a0, %d1.w),%d2
m68k_0336b8_end:
.org 0x336BC
m68k_0336bc:
        move.w -0x2(%a0, %d1.w),(%a0, %d1.w)
m68k_0336bc_end:
.org 0x336C2
m68k_0336c2:
        move.w %d2,-0x2(%a0, %d1.w)
m68k_0336c2_end:
.org 0x337C0
m68k_0337c0:
        ori.w #0x1,%sr
m68k_0337c0_end:
.org 0x337D8
m68k_0337d8:
        lea.l 0xf72a:w,%a1
m68k_0337d8_end:
.org 0x337DC
m68k_0337dc:
        lea.l 0xc800:w,%a2
m68k_0337dc_end:
.org 0x337E0
m68k_0337e0:
        lea.l 0xb800:w,%a3
m68k_0337e0_end:
.org 0x337E4
m68k_0337e4:
        move.w (%a1)+,%d2
m68k_0337e4_end:
.org 0x337E6
m68k_0337e6:
        bmi.w (. + 62)
m68k_0337e6_end:
.org 0x337EA
m68k_0337ea:
        andi.w #0xff,%d2
m68k_0337ea_end:
.org 0x337EE
m68k_0337ee:
        lsl.w #0x1,%d2
m68k_0337ee_end:
.org 0x337F0
m68k_0337f0:
        move.w (%a3, %d2.w),%d3
m68k_0337f0_end:
.org 0x337F4
m68k_0337f4:
        mulu.w #0x64,%d3
m68k_0337f4_end:
.org 0x337F8
m68k_0337f8:
        lsl.w #0x1,%d2
m68k_0337f8_end:
.org 0x337FA
m68k_0337fa:
        sub.l (%a2, %d2.w),%d3
m68k_0337fa_end:
.org 0x337FE
m68k_0337fe:
        bcc.w (. + 6)
m68k_0337fe_end:
.org 0x33802
m68k_033802:
        moveq #0,%d3
m68k_033802_end:
.org 0x33804
m68k_033804:
        cmp.l %d1,%d3
m68k_033804_end:
.org 0x33806
m68k_033806:
        bls.w (. + 6)
m68k_033806_end:
.org 0x3380A
m68k_03380a:
        move.l %d1,%d3
m68k_03380a_end:
.org 0x3380C
m68k_03380c:
        add.l %d3,(%a2, %d2.w)
m68k_03380c_end:
.org 0x33810
m68k_033810:
        sub.l %d3,%d1
m68k_033810_end:
.org 0x33812
m68k_033812:
        beq.w (. + 6)
m68k_033812_end:
.org 0x33816
m68k_033816:
        bra.b (. + -50)
m68k_033816_end:
.org 0x33824
m68k_033824:
        move.l %d1,(%a0, %d0.w)
m68k_033824_end:
.org 0x33828
m68k_033828:
        ori.w #0x1,%sr
m68k_033828_end:
.org 0x33868
m68k_033868:
        move.l #0x186a0,%d4
m68k_033868_end:
.org 0x3386E
m68k_03386e:
        move.w #0x3e8,%d1
m68k_03386e_end:
.org 0x338A0
m68k_0338a0:
        move.l %d4,%d1
m68k_0338a0_end:
.org 0x338C2
m68k_0338c2:
        move.w 0xf728:w,%d0
m68k_0338c2_end:
.org 0x338C6
m68k_0338c6:
        bmi.w (. + 18)
m68k_0338c6_end:
.org 0x338CA
m68k_0338ca:
        subq.w #0x1,%d0
m68k_0338ca_end:
.org 0x338CC
m68k_0338cc:
        lsl.w #0x1,%d0
m68k_0338cc_end:
.org 0x338CE
m68k_0338ce:
        move.w 10(%pc, %d0.w),%d0
m68k_0338ce_end:
.org 0x338D2
m68k_0338d2:
        jsr 24(%pc, %d0.w)
m68k_0338d2_end:
.org 0x338D6
m68k_0338d6:
        bra.b (. + -20)
m68k_0338d6_end:
.org 0x338D8
m68k_0338d8:
        rts
m68k_0338d8_end:
.org 0x340F8
m68k_0340f8:
        move.w 0xf728:w,%d0
m68k_0340f8_end:
.org 0x340FC
m68k_0340fc:
        bmi.w (. + 18)
m68k_0340fc_end:
.org 0x34100
m68k_034100:
        subq.w #0x1,%d0
m68k_034100_end:
.org 0x34102
m68k_034102:
        lsl.w #0x1,%d0
m68k_034102_end:
.org 0x34104
m68k_034104:
        move.w 10(%pc, %d0.w),%d0
m68k_034104_end:
.org 0x34108
m68k_034108:
        jsr 54(%pc, %d0.w)
m68k_034108_end:
.org 0x3410C
m68k_03410c:
        bra.b (. + -20)
m68k_03410c_end:
.org 0x3410E
m68k_03410e:
        rts
m68k_03410e_end:
.org 0x35764
m68k_035764:
        neg.l %d2
m68k_035764_end:
.org 0x35766
m68k_035766:
        bsr.b (. + 6)
m68k_035766_end:
.org 0x35768
m68k_035768:
        neg.l %d1
m68k_035768_end:
.org 0x3576A
m68k_03576a:
        rts
m68k_03576a_end:
.org 0x35770
m68k_035770:
        neg.l %d1
m68k_035770_end:
.org 0x35772
m68k_035772:
        bsr.b (. + 8)
m68k_035772_end:
.org 0x35774
m68k_035774:
        neg.l %d1
m68k_035774_end:
.org 0x35776
m68k_035776:
        neg.l %d2
m68k_035776_end:
.org 0x35778
m68k_035778:
        rts
m68k_035778_end:
.org 0x35782
m68k_035782:
        cmp.l %d1,%d2
m68k_035782_end:
.org 0x35784
m68k_035784:
        beq.b (. + 10)
m68k_035784_end:
.org 0x35786
m68k_035786:
        bls.b (. + 14)
m68k_035786_end:
.org 0x35788
m68k_035788:
        move.l %d1,%d2
m68k_035788_end:
.org 0x3578A
m68k_03578a:
        moveq #0,%d1
m68k_03578a_end:
.org 0x3578C
m68k_03578c:
        rts
m68k_03578c_end:
.org 0x3578E
m68k_03578e:
        moveq #1,%d1
m68k_03578e_end:
.org 0x35790
m68k_035790:
        moveq #0,%d2
m68k_035790_end:
.org 0x35792
m68k_035792:
        rts
m68k_035792_end:
.org 0x35794
m68k_035794:
        movem.l %d3-%d5,-(%a7)
m68k_035794_end:
.org 0x35798
m68k_035798:
        move.l %d2,%d3
m68k_035798_end:
.org 0x3579A
m68k_03579a:
        clr.w %d3
m68k_03579a_end:
.org 0x3579C
m68k_03579c:
        swap %d3
m68k_03579c_end:
.org 0x3579E
m68k_03579e:
        addq.l #0x1,%d3
m68k_03579e_end:
.org 0x357A0
m68k_0357a0:
        move.l %d1,%d4
m68k_0357a0_end:
.org 0x357A2
m68k_0357a2:
        move.l %d2,%d5
m68k_0357a2_end:
.org 0x357A4
m68k_0357a4:
        move.l %d3,%d2
m68k_0357a4_end:
.org 0x357A6
m68k_0357a6:
        bsr.b (. + 52)
m68k_0357a6_end:
.org 0x357A8
m68k_0357a8:
        move.l %d5,%d2
m68k_0357a8_end:
.org 0x357AA
m68k_0357aa:
        divu.w %d3,%d2
m68k_0357aa_end:
.org 0x357AC
m68k_0357ac:
        divu.w %d2,%d1
m68k_0357ac_end:
.org 0x357AE
m68k_0357ae:
        andi.l #0xffff,%d1
m68k_0357ae_end:
.org 0x357B4
m68k_0357b4:
        move.l %d5,%d2
m68k_0357b4_end:
.org 0x357B6
m68k_0357b6:
        move.l %d5,%d3
m68k_0357b6_end:
.org 0x357B8
m68k_0357b8:
        swap %d3
m68k_0357b8_end:
.org 0x357BA
m68k_0357ba:
        mulu.w %d1,%d2
m68k_0357ba_end:
.org 0x357BC
m68k_0357bc:
        mulu.w %d1,%d3
m68k_0357bc_end:
.org 0x357BE
m68k_0357be:
        swap %d3
m68k_0357be_end:
.org 0x357C0
m68k_0357c0:
        add.l %d3,%d2
m68k_0357c0_end:
.org 0x357C2
m68k_0357c2:
        sub.l %d4,%d2
m68k_0357c2_end:
.org 0x357C4
m68k_0357c4:
        bhi.b (. + 12)
m68k_0357c4_end:
.org 0x357C6
m68k_0357c6:
        neg.l %d2
m68k_0357c6_end:
.org 0x357C8
m68k_0357c8:
        cmp.l %d2,%d5
m68k_0357c8_end:
.org 0x357CA
m68k_0357ca:
        bhi.b (. + 10)
m68k_0357ca_end:
.org 0x357CC
m68k_0357cc:
        addq.l #0x1,%d1
m68k_0357cc_end:
.org 0x357CE
m68k_0357ce:
        bra.b (. + -26)
m68k_0357ce_end:
.org 0x357D0
m68k_0357d0:
        subq.l #0x1,%d1
m68k_0357d0_end:
.org 0x357D2
m68k_0357d2:
        bra.b (. + -30)
m68k_0357d2_end:
.org 0x357D4
m68k_0357d4:
        movem.l (%a7)+,%d3-%d5
m68k_0357d4_end:
.org 0x357D8
m68k_0357d8:
        rts
m68k_0357d8_end:
.org 0x396E4
m68k_0396e4:
        move.w #0x60,0xff7032:l
m68k_0396e4_end:
.org 0x396EC
m68k_0396ec:
        move.w #0x30,0xff7034:l
m68k_0396ec_end:
.org 0x396F4
m68k_0396f4:
        bra.w (. + 30)
m68k_0396f4_end:
.org 0x3975A
m68k_03975a:
        move.w #0x2000,%d0
m68k_03975a_end:
.org 0x39788
m68k_039788:
        move.w 0xff7026:l,%d3
m68k_039788_end:
.org 0x3978E
m68k_03978e:
        addq.w #0x1,%d3
m68k_03978e_end:
.org 0x39790
m68k_039790:
        asl.w #0x2,%d3
m68k_039790_end:
.org 0x39792
m68k_039792:
        lea.l -4058(%pc),%a1
m68k_039792_end:
.org 0x39796
m68k_039796:
        movea.l (%a1, %d3.w),%a0
m68k_039796_end:
.org 0x3979A
m68k_03979a:
        move.w #0x2000,%d0
m68k_03979a_end:
.org 0x3979E
m68k_03979e:
        bsr.w (. + -326)
m68k_03979e_end:
.org 0x3986C
m68k_03986c:
        moveq #0,%d2
m68k_03986c_end:
.org 0x3986E
m68k_03986e:
        cmpi.w #0x1,%d1
m68k_03986e_end:
.org 0x39872
m68k_039872:
        beq.w (. + 8)
m68k_039872_end:
.org 0x39876
m68k_039876:
        addi.w #0x20,%d2
m68k_039876_end:
.org 0x3987A
m68k_03987a:
        lea.l 0xfb00:w,%a1
m68k_03987a_end:
.org 0x3987E
m68k_03987e:
        lea.l -2536(%pc),%a0
m68k_03987e_end:
.org 0x39882
m68k_039882:
        adda.w %d2,%a0
m68k_039882_end:
.org 0x39884
m68k_039884:
        moveq #7,%d0
m68k_039884_end:
.org 0x39886
m68k_039886:
        move.l (%a0)+,(%a1)+
m68k_039886_end:
.org 0x39888
m68k_039888:
        dbra %d0,(. + -2)
m68k_039888_end:
.org 0x398E0
m68k_0398e0:
        clr.l %d0
m68k_0398e0_end:
.org 0x398E2
m68k_0398e2:
        move.w 0xff7026:l,%d3
m68k_0398e2_end:
.org 0x398E8
m68k_0398e8:
        asl.w #0x2,%d3
m68k_0398e8_end:
.org 0x398EA
m68k_0398ea:
        lea.l -2904(%pc),%a2
m68k_0398ea_end:
.org 0x398EE
m68k_0398ee:
        movea.l (%a2, %d3.w),%a1
m68k_0398ee_end:
.org 0x398F2
m68k_0398f2:
        asl.w #0x2,%d1
m68k_0398f2_end:
.org 0x398F4
m68k_0398f4:
        adda.w %d1,%a1
m68k_0398f4_end:
.org 0x398F6
m68k_0398f6:
        movea.l (%a1),%a0
m68k_0398f6_end:
.org 0x398F8
m68k_0398f8:
        move.w 0xff7028:l,%d0
m68k_0398f8_end:
.org 0x398FE
m68k_0398fe:
        move.w 0xff702a:l,%d1
m68k_0398fe_end:
.org 0x39904
m68k_039904:
        moveq #4,%d2
m68k_039904_end:
.org 0x39906
m68k_039906:
        moveq #0,%d3
m68k_039906_end:
.org 0x39908
m68k_039908:
        move.l #0x100,%d4
m68k_039908_end:
.org 0x3990E
m68k_03990e:
        jsr 3216(%pc)
m68k_03990e_end:
.org 0x39912
m68k_039912:
        nop
m68k_039912_end:
.org 0x3991C
m68k_03991c:
        cmpi.w #0x3,%d1
m68k_03991c_end:
.org 0x39920
m68k_039920:
        bcs.w (. + 64)
m68k_039920_end:
.org 0x39924
m68k_039924:
        move.w 0xf320:w,%d0
m68k_039924_end:
.org 0x39928
m68k_039928:
        andi.w #0x7,%d0
m68k_039928_end:
.org 0x3992C
m68k_03992c:
        bne.w (. + 22)
m68k_03992c_end:
.org 0x39930
m68k_039930:
        cmpi.w #0x28,0xff703c:l
m68k_039930_end:
.org 0x39938
m68k_039938:
        beq.w (. + 40)
m68k_039938_end:
.org 0x3993C
m68k_03993c:
        addq.w #0x4,0xff703c:l
m68k_03993c_end:
.org 0x39942
m68k_039942:
        clr.l %d3
m68k_039942_end:
.org 0x39944
m68k_039944:
        move.w 0xff703c:l,%d3
m68k_039944_end:
.org 0x3994A
m68k_03994a:
        lea.l 24(%pc),%a1
m68k_03994a_end:
.org 0x3994E
m68k_03994e:
        nop
m68k_03994e_end:
.org 0x39950
m68k_039950:
        movea.l (%a1, %d3.w),%a0
m68k_039950_end:
.org 0x39954
m68k_039954:
        lea.l 0xfb00:w,%a1
m68k_039954_end:
.org 0x39958
m68k_039958:
        moveq #7,%d0
m68k_039958_end:
.org 0x3995A
m68k_03995a:
        move.l (%a0)+,(%a1)+
m68k_03995a_end:
.org 0x3995C
m68k_03995c:
        dbra %d0,(. + -2)
m68k_03995c_end:
.org 0x39960
m68k_039960:
        bra.w (. + -256)
m68k_039960_end:
.org 0x39994
m68k_039994:
        move.w 0xf320:w,%d0
m68k_039994_end:
.org 0x39998
m68k_039998:
        lsr.w #0x2,%d0
m68k_039998_end:
.org 0x3999A
m68k_03999a:
        andi.w #0x3,%d0
m68k_03999a_end:
.org 0x3999E
m68k_03999e:
        asl.w #0x5,%d0
m68k_03999e_end:
.org 0x399A0
m68k_0399a0:
        lea.l -2250(%pc),%a0
m68k_0399a0_end:
.org 0x399A4
m68k_0399a4:
        adda.w %d0,%a0
m68k_0399a4_end:
.org 0x399A6
m68k_0399a6:
        lea.l 0xfb00:w,%a1
m68k_0399a6_end:
.org 0x399AA
m68k_0399aa:
        moveq #15,%d0
m68k_0399aa_end:
.org 0x399AC
m68k_0399ac:
        move.w (%a0)+,(%a1)+
m68k_0399ac_end:
.org 0x399AE
m68k_0399ae:
        dbra %d0,(. + -2)
m68k_0399ae_end:
.org 0x399B2
m68k_0399b2:
        bra.w (. + 1938)
m68k_0399b2_end:
.org 0x399B6
m68k_0399b6:
        move.w 0xf320:w,%d0
m68k_0399b6_end:
.org 0x399BA
m68k_0399ba:
        lsr.w #0x3,%d0
m68k_0399ba_end:
.org 0x399BC
m68k_0399bc:
        andi.w #0x1,%d0
m68k_0399bc_end:
.org 0x399C0
m68k_0399c0:
        asl.w #0x5,%d0
m68k_0399c0_end:
.org 0x399C2
m68k_0399c2:
        lea.l -2156(%pc),%a0
m68k_0399c2_end:
.org 0x399C6
m68k_0399c6:
        adda.w %d0,%a0
m68k_0399c6_end:
.org 0x399C8
m68k_0399c8:
        lea.l 0xfb00:w,%a1
m68k_0399c8_end:
.org 0x399CC
m68k_0399cc:
        moveq #15,%d0
m68k_0399cc_end:
.org 0x399CE
m68k_0399ce:
        move.w (%a0)+,(%a1)+
m68k_0399ce_end:
.org 0x399D0
m68k_0399d0:
        dbra %d0,(. + -2)
m68k_0399d0_end:
.org 0x399D4
m68k_0399d4:
        bra.w (. + 1904)
m68k_0399d4_end:
.org 0x399F2
m68k_0399f2:
        addq.w #0x1,0xff702e:l
m68k_0399f2_end:
.org 0x399F8
m68k_0399f8:
        move.w 0xff7026:l,%d0
m68k_0399f8_end:
.org 0x399FE
m68k_0399fe:
        lea.l 130(%pc),%a4
m68k_0399fe_end:
.org 0x39A02
m68k_039a02:
        nop
m68k_039a02_end:
.org 0x39A04
m68k_039a04:
        move.b (%a4, %d0.w),%d1
m68k_039a04_end:
.org 0x39A08
m68k_039a08:
        move.w 0xff702e:l,%d7
m68k_039a08_end:
.org 0x39A0E
m68k_039a0e:
        cmp.b %d1,%d7
m68k_039a0e_end:
.org 0x39A10
m68k_039a10:
        bhi.w (. + 44)
m68k_039a10_end:
.org 0x39A14
m68k_039a14:
        moveq #0,%d0
m68k_039a14_end:
.org 0x39A16
m68k_039a16:
        move.b 0xff702c:l,%d0
m68k_039a16_end:
.org 0x39A1C
m68k_039a1c:
        btst.l #0x4,%d0
m68k_039a1c_end:
.org 0x39A20
m68k_039a20:
        bne.w (. + 34)
m68k_039a20_end:
.org 0x39A24
m68k_039a24:
        btst.l #0x5,%d0
m68k_039a24_end:
.org 0x39A28
m68k_039a28:
        bne.w (. + 42)
m68k_039a28_end:
.org 0x39A2C
m68k_039a2c:
        btst.l #0x6,%d0
m68k_039a2c_end:
.org 0x39A30
m68k_039a30:
        bne.w (. + 50)
m68k_039a30_end:
.org 0x39A34
m68k_039a34:
        btst.l #0x7,%d0
m68k_039a34_end:
.org 0x39A38
m68k_039a38:
        bne.w (. + 58)
m68k_039a38_end:
.org 0x39A42
m68k_039a42:
        move.w %d0,%d1
m68k_039a42_end:
.org 0x39A44
m68k_039a44:
        andi.l #0xf,%d1
m68k_039a44_end:
.org 0x39A4A
m68k_039a4a:
        sub.w %d1,0xff7028:l
m68k_039a4a_end:
.org 0x39A50
m68k_039a50:
        bra.b (. + -44)
m68k_039a50_end:
.org 0x39A52
m68k_039a52:
        move.w %d0,%d1
m68k_039a52_end:
.org 0x39A54
m68k_039a54:
        andi.l #0xf,%d1
m68k_039a54_end:
.org 0x39A5A
m68k_039a5a:
        add.w %d1,0xff7028:l
m68k_039a5a_end:
.org 0x39A60
m68k_039a60:
        bra.b (. + -52)
m68k_039a60_end:
.org 0x39A62
m68k_039a62:
        move.w %d0,%d1
m68k_039a62_end:
.org 0x39A64
m68k_039a64:
        andi.l #0xf,%d1
m68k_039a64_end:
.org 0x39A6A
m68k_039a6a:
        sub.w %d1,0xff702a:l
m68k_039a6a_end:
.org 0x39A70
m68k_039a70:
        bra.b (. + -60)
m68k_039a70_end:
.org 0x39A72
m68k_039a72:
        move.w %d0,%d1
m68k_039a72_end:
.org 0x39A74
m68k_039a74:
        andi.l #0xf,%d1
m68k_039a74_end:
.org 0x39A7A
m68k_039a7a:
        add.w %d1,0xff702a:l
m68k_039a7a_end:
.org 0x39A80
m68k_039a80:
        bra.b (. + -68)
m68k_039a80_end:
.org 0x39AA6
m68k_039aa6:
        cmpi.w #0xb,0xff7026:l
m68k_039aa6_end:
.org 0x39AAE
m68k_039aae:
        bhi.w (. + 98)
m68k_039aae_end:
.org 0x39AB2
m68k_039ab2:
        jsr -220(%pc)
m68k_039ab2_end:
.org 0x39AB6
m68k_039ab6:
        cmpi.w #0xb,0xff7026:l
m68k_039ab6_end:
.org 0x39ABE
m68k_039abe:
        bne.w (. + 10)
m68k_039abe_end:
.org 0x39AC2
m68k_039ac2:
        moveq #1,%d1
m68k_039ac2_end:
.org 0x39AC4
m68k_039ac4:
        bra.w (. + 6)
m68k_039ac4_end:
.org 0x39AC8
m68k_039ac8:
        moveq #0,%d1
m68k_039ac8_end:
.org 0x39ACA
m68k_039aca:
        asl.w #0x2,%d1
m68k_039aca_end:
.org 0x39ACC
m68k_039acc:
        movea.l 58(%pc, %d1.w),%a0
m68k_039acc_end:
.org 0x39AD0
m68k_039ad0:
        move.w 0xff7028:l,%d0
m68k_039ad0_end:
.org 0x39AD6
m68k_039ad6:
        move.w 0xff702a:l,%d1
m68k_039ad6_end:
.org 0x39ADC
m68k_039adc:
        moveq #4,%d2
m68k_039adc_end:
.org 0x39ADE
m68k_039ade:
        moveq #0,%d3
m68k_039ade_end:
.org 0x39AE0
m68k_039ae0:
        cmpi.w #0xb,0xff7026:l
m68k_039ae0_end:
.org 0x39AE8
m68k_039ae8:
        bne.w (. + 10)
m68k_039ae8_end:
.org 0x39AEC
m68k_039aec:
        moveq #0,%d4
m68k_039aec_end:
.org 0x39AEE
m68k_039aee:
        bra.w (. + 10)
m68k_039aee_end:
.org 0x39AF2
m68k_039af2:
        move.l #0x100,%d4
m68k_039af2_end:
.org 0x39AF8
m68k_039af8:
        jsr 2726(%pc)
m68k_039af8_end:
.org 0x39AFC
m68k_039afc:
        nop
m68k_039afc_end:
.org 0x39AFE
m68k_039afe:
        jsr 3150(%pc)
m68k_039afe_end:
.org 0x39B02
m68k_039b02:
        nop
m68k_039b02_end:
.org 0x39B04
m68k_039b04:
        bra.w (. + -828)
m68k_039b04_end:
.org 0x39B10
m68k_039b10:
        cmpi.w #0x13,0xff7026:l
m68k_039b10_end:
.org 0x39B18
m68k_039b18:
        bhi.w (. + 472)
m68k_039b18_end:
.org 0x39B1C
m68k_039b1c:
        addq.w #0x1,0xff703c:l
m68k_039b1c_end:
.org 0x39B22
m68k_039b22:
        cmpi.w #0x90,0xff703c:l
m68k_039b22_end:
.org 0x39B2A
m68k_039b2a:
        beq.w (. + 150)
m68k_039b2a_end:
.org 0x39B2E
m68k_039b2e:
        cmpi.w #0x90,0xff703c:l
m68k_039b2e_end:
.org 0x39B36
m68k_039b36:
        bhi.w (. + 278)
m68k_039b36_end:
.org 0x39B3A
m68k_039b3a:
        movea.l 120(%pc),%a0
m68k_039b3a_end:
.org 0x39B3E
m68k_039b3e:
        nop
m68k_039b3e_end:
.org 0x39B40
m68k_039b40:
        move.w #0x60,%d0
m68k_039b40_end:
.org 0x39B44
m68k_039b44:
        move.w #0x60,%d1
m68k_039b44_end:
.org 0x39B48
m68k_039b48:
        moveq #5,%d2
m68k_039b48_end:
.org 0x39B4A
m68k_039b4a:
        moveq #0,%d3
m68k_039b4a_end:
.org 0x39B4C
m68k_039b4c:
        move.w #0x100,%d4
m68k_039b4c_end:
.org 0x39B50
m68k_039b50:
        jsr 3152(%pc)
m68k_039b50_end:
.org 0x39B54
m68k_039b54:
        nop
m68k_039b54_end:
.org 0x39B56
m68k_039b56:
        movea.l 100(%pc),%a0
m68k_039b56_end:
.org 0x39B5A
m68k_039b5a:
        nop
m68k_039b5a_end:
.org 0x39B5C
m68k_039b5c:
        move.w #0x60,%d0
m68k_039b5c_end:
.org 0x39B60
m68k_039b60:
        move.w #0x60,%d1
m68k_039b60_end:
.org 0x39B64
m68k_039b64:
        moveq #5,%d2
m68k_039b64_end:
.org 0x39B66
m68k_039b66:
        moveq #0,%d3
m68k_039b66_end:
.org 0x39B68
m68k_039b68:
        move.w #0x0,%d4
m68k_039b68_end:
.org 0x39B6C
m68k_039b6c:
        jsr 3124(%pc)
m68k_039b6c_end:
.org 0x39B70
m68k_039b70:
        nop
m68k_039b70_end:
.org 0x39B72
m68k_039b72:
        cmpi.w #0x60,0xff7028:l
m68k_039b72_end:
.org 0x39B7A
m68k_039b7a:
        bcs.w (. + 22)
m68k_039b7a_end:
.org 0x39B7E
m68k_039b7e:
        move.w 0xf320:w,%d0
m68k_039b7e_end:
.org 0x39B82
m68k_039b82:
        andi.w #0x3,%d0
m68k_039b82_end:
.org 0x39B86
m68k_039b86:
        bne.w (. + 10)
m68k_039b86_end:
.org 0x39B8A
m68k_039b8a:
        subq.w #0x1,0xff7028:l
m68k_039b8a_end:
.org 0x39B90
m68k_039b90:
        movea.l 38(%pc),%a0
m68k_039b90_end:
.org 0x39B94
m68k_039b94:
        nop
m68k_039b94_end:
.org 0x39B96
m68k_039b96:
        move.w 0xff7028:l,%d0
m68k_039b96_end:
.org 0x39B9C
m68k_039b9c:
        move.w 0xff702a:l,%d1
m68k_039b9c_end:
.org 0x39BA2
m68k_039ba2:
        moveq #4,%d2
m68k_039ba2_end:
.org 0x39BA4
m68k_039ba4:
        moveq #0,%d3
m68k_039ba4_end:
.org 0x39BA6
m68k_039ba6:
        move.w #0x0,%d4
m68k_039ba6_end:
.org 0x39BAA
m68k_039baa:
        jsr 2548(%pc)
m68k_039baa_end:
.org 0x39BAE
m68k_039bae:
        nop
m68k_039bae_end:
.org 0x39BB0
m68k_039bb0:
        bra.w (. + -178)
m68k_039bb0_end:
.org 0x39BC0
m68k_039bc0:
        move.w 0xff7026:l,%d0
m68k_039bc0_end:
.org 0x39BC6
m68k_039bc6:
        asl.w #0x1,%d0
m68k_039bc6_end:
.org 0x39BC8
m68k_039bc8:
        lea.l 34(%pc),%a0
m68k_039bc8_end:
.org 0x39BCC
m68k_039bcc:
        nop
m68k_039bcc_end:
.org 0x39BCE
m68k_039bce:
        lea.l 76(%pc),%a1
m68k_039bce_end:
.org 0x39BD2
m68k_039bd2:
        nop
m68k_039bd2_end:
.org 0x39BD4
m68k_039bd4:
        move.w (%a0, %d0.w),%d1
m68k_039bd4_end:
.org 0x39BD8
m68k_039bd8:
        move.w (%a1, %d0.w),%d2
m68k_039bd8_end:
.org 0x39BDC
m68k_039bdc:
        move.w %d1,0xff7028:l
m68k_039bdc_end:
.org 0x39BE2
m68k_039be2:
        move.w %d2,0xff702a:l
m68k_039be2_end:
.org 0x39BE8
m68k_039be8:
        bra.w (. + 100)
m68k_039be8_end:
.org 0x39C4C
m68k_039c4c:
        move.w 0xff7026:l,%d0
m68k_039c4c_end:
.org 0x39C52
m68k_039c52:
        moveq #0,%d1
m68k_039c52_end:
.org 0x39C54
m68k_039c54:
        lea.l 130(%pc),%a0
m68k_039c54_end:
.org 0x39C58
m68k_039c58:
        nop
m68k_039c58_end:
.org 0x39C5A
m68k_039c5a:
        move.b (%a0, %d0.w),%d1
m68k_039c5a_end:
.org 0x39C5E
m68k_039c5e:
        asl.w #0x2,%d1
m68k_039c5e_end:
.org 0x39C60
m68k_039c60:
        movem.l %d0-%d1,-(%a7)
m68k_039c60_end:
.org 0x39C64
m68k_039c64:
        movea.l 82(%pc, %d1.w),%a0
m68k_039c64_end:
.org 0x39C68
m68k_039c68:
        move.w #0x60,%d0
m68k_039c68_end:
.org 0x39C6C
m68k_039c6c:
        move.w #0x60,%d1
m68k_039c6c_end:
.org 0x39C70
m68k_039c70:
        moveq #3,%d2
m68k_039c70_end:
.org 0x39C72
m68k_039c72:
        moveq #0,%d3
m68k_039c72_end:
.org 0x39C74
m68k_039c74:
        move.w #0x0,%d4
m68k_039c74_end:
.org 0x39C78
m68k_039c78:
        jsr 2856(%pc)
m68k_039c78_end:
.org 0x39C7C
m68k_039c7c:
        nop
m68k_039c7c_end:
.org 0x39C7E
m68k_039c7e:
        movem.l (%a7)+,%d0-%d1
m68k_039c7e_end:
.org 0x39C82
m68k_039c82:
        cmpi.w #0xc,%d0
m68k_039c82_end:
.org 0x39C86
m68k_039c86:
        beq.w (. + 46)
m68k_039c86_end:
.org 0x39C8A
m68k_039c8a:
        movem.l %d1,-(%a7)
m68k_039c8a_end:
.org 0x39C8E
m68k_039c8e:
        jsr -696(%pc)
m68k_039c8e_end:
.org 0x39C92
m68k_039c92:
        movem.l (%a7)+,%d1
m68k_039c92_end:
.org 0x39C96
m68k_039c96:
        movea.l 48(%pc, %d1.w),%a0
m68k_039c96_end:
.org 0x39C9A
m68k_039c9a:
        move.w 0xff7028:l,%d0
m68k_039c9a_end:
.org 0x39CA0
m68k_039ca0:
        move.w 0xff702a:l,%d1
m68k_039ca0_end:
.org 0x39CA6
m68k_039ca6:
        moveq #2,%d2
m68k_039ca6_end:
.org 0x39CA8
m68k_039ca8:
        moveq #0,%d3
m68k_039ca8_end:
.org 0x39CAA
m68k_039caa:
        move.w #0x0,%d4
m68k_039caa_end:
.org 0x39CAE
m68k_039cae:
        jsr 2288(%pc)
m68k_039cae_end:
.org 0x39CB2
m68k_039cb2:
        nop
m68k_039cb2_end:
.org 0x39CB4
m68k_039cb4:
        bra.w (. + -438)
m68k_039cb4_end:
.org 0x39CF0
m68k_039cf0:
        cmpi.w #0x15,0xff7026:l
m68k_039cf0_end:
.org 0x39CF8
m68k_039cf8:
        bhi.w (. + 326)
m68k_039cf8_end:
.org 0x39CFC
m68k_039cfc:
        cmpi.w #0x14,0xff7026:l
m68k_039cfc_end:
.org 0x39D04
m68k_039d04:
        beq.w (. + 14)
m68k_039d04_end:
.org 0x39D08
m68k_039d08:
        movea.l 104(%pc),%a0
m68k_039d08_end:
.org 0x39D0C
m68k_039d0c:
        nop
m68k_039d0c_end:
.org 0x39D0E
m68k_039d0e:
        bra.w (. + 10)
m68k_039d0e_end:
.org 0x39D12
m68k_039d12:
        movea.l 86(%pc),%a0
m68k_039d12_end:
.org 0x39D16
m68k_039d16:
        nop
m68k_039d16_end:
.org 0x39D18
m68k_039d18:
        move.w #0x60,%d0
m68k_039d18_end:
.org 0x39D1C
m68k_039d1c:
        move.w #0x60,%d1
m68k_039d1c_end:
.org 0x39D20
m68k_039d20:
        moveq #3,%d2
m68k_039d20_end:
.org 0x39D22
m68k_039d22:
        moveq #0,%d3
m68k_039d22_end:
.org 0x39D24
m68k_039d24:
        move.w #0x0,%d4
m68k_039d24_end:
.org 0x39D28
m68k_039d28:
        jsr 2680(%pc)
m68k_039d28_end:
.org 0x39D2C
m68k_039d2c:
        nop
m68k_039d2c_end:
.org 0x39D2E
m68k_039d2e:
        jsr -856(%pc)
m68k_039d2e_end:
.org 0x39D32
m68k_039d32:
        moveq #4,%d1
m68k_039d32_end:
.org 0x39D34
m68k_039d34:
        cmpi.w #0x14,0xff7026:l
m68k_039d34_end:
.org 0x39D3C
m68k_039d3c:
        beq.w (. + 12)
m68k_039d3c_end:
.org 0x39D40
m68k_039d40:
        movea.l 48(%pc, %d1.w),%a0
m68k_039d40_end:
.org 0x39D44
m68k_039d44:
        bra.w (. + 8)
m68k_039d44_end:
.org 0x39D48
m68k_039d48:
        movea.l 32(%pc, %d1.w),%a0
m68k_039d48_end:
.org 0x39D4C
m68k_039d4c:
        move.w 0xff7028:l,%d0
m68k_039d4c_end:
.org 0x39D52
m68k_039d52:
        move.w 0xff702a:l,%d1
m68k_039d52_end:
.org 0x39D58
m68k_039d58:
        moveq #2,%d2
m68k_039d58_end:
.org 0x39D5A
m68k_039d5a:
        moveq #0,%d3
m68k_039d5a_end:
.org 0x39D5C
m68k_039d5c:
        move.w #0x0,%d4
m68k_039d5c_end:
.org 0x39D60
m68k_039d60:
        jsr 2110(%pc)
m68k_039d60_end:
.org 0x39D64
m68k_039d64:
        nop
m68k_039d64_end:
.org 0x39D66
m68k_039d66:
        bra.w (. + -616)
m68k_039d66_end:
.org 0x39D7A
m68k_039d7a:
        cmpi.w #0x1b,0xff7026:l
m68k_039d7a_end:
.org 0x39D82
m68k_039d82:
        beq.w (. + -1396)
m68k_039d82_end:
.org 0x39D86
m68k_039d86:
        cmpi.w #0x1b,0xff7026:l
m68k_039d86_end:
.org 0x39D8E
m68k_039d8e:
        bhi.w (. + 902)
m68k_039d8e_end:
.org 0x39D92
m68k_039d92:
        jsr -956(%pc)
m68k_039d92_end:
.org 0x39D96
m68k_039d96:
        movea.l 134(%pc),%a0
m68k_039d96_end:
.org 0x39D9A
m68k_039d9a:
        nop
m68k_039d9a_end:
.org 0x39D9C
m68k_039d9c:
        move.w 0xff7028:l,%d0
m68k_039d9c_end:
.org 0x39DA2
m68k_039da2:
        move.w 0xff702a:l,%d1
m68k_039da2_end:
.org 0x39DA8
m68k_039da8:
        moveq #5,%d2
m68k_039da8_end:
.org 0x39DAA
m68k_039daa:
        moveq #0,%d3
m68k_039daa_end:
.org 0x39DAC
m68k_039dac:
        move.w #0x0,%d4
m68k_039dac_end:
.org 0x39DB0
m68k_039db0:
        jsr 2030(%pc)
m68k_039db0_end:
.org 0x39DB4
m68k_039db4:
        nop
m68k_039db4_end:
.org 0x39DB6
m68k_039db6:
        cmpi.w #0x60,0xff702a:l
m68k_039db6_end:
.org 0x39DBE
m68k_039dbe:
        bne.w (. + 92)
m68k_039dbe_end:
.org 0x39DC2
m68k_039dc2:
        cmpi.w #0x14,0xff703c:l
m68k_039dc2_end:
.org 0x39DCA
m68k_039dca:
        beq.w (. + 52)
m68k_039dca_end:
.org 0x39DCE
m68k_039dce:
        move.w 0xf320:w,%d0
m68k_039dce_end:
.org 0x39DD2
m68k_039dd2:
        andi.w #0xf,%d0
m68k_039dd2_end:
.org 0x39DD6
m68k_039dd6:
        bne.w (. + 40)
m68k_039dd6_end:
.org 0x39DDA
m68k_039dda:
        addq.w #0x4,0xff703c:l
m68k_039dda_end:
.org 0x39DE0
m68k_039de0:
        clr.l %d3
m68k_039de0_end:
.org 0x39DE2
m68k_039de2:
        move.w 0xff703c:l,%d3
m68k_039de2_end:
.org 0x39DE8
m68k_039de8:
        lea.l 60(%pc),%a1
m68k_039de8_end:
.org 0x39DEC
m68k_039dec:
        nop
m68k_039dec_end:
.org 0x39DEE
m68k_039dee:
        movea.l (%a1, %d3.w),%a0
m68k_039dee_end:
.org 0x39DF2
m68k_039df2:
        lea.l 0xfb00:w,%a1
m68k_039df2_end:
.org 0x39DF6
m68k_039df6:
        moveq #7,%d0
m68k_039df6_end:
.org 0x39DF8
m68k_039df8:
        move.l (%a0)+,(%a1)+
m68k_039df8_end:
.org 0x39DFA
m68k_039dfa:
        dbra %d0,(. + -2)
m68k_039dfa_end:
.org 0x39DFE
m68k_039dfe:
        moveq #4,%d0
m68k_039dfe_end:
.org 0x39E00
m68k_039e00:
        movea.l 28(%pc, %d0.w),%a0
m68k_039e00_end:
.org 0x39E04
m68k_039e04:
        move.w #0x60,%d0
m68k_039e04_end:
.org 0x39E08
m68k_039e08:
        move.w #0x60,%d1
m68k_039e08_end:
.org 0x39E0C
m68k_039e0c:
        moveq #4,%d2
m68k_039e0c_end:
.org 0x39E0E
m68k_039e0e:
        moveq #0,%d3
m68k_039e0e_end:
.org 0x39E10
m68k_039e10:
        move.w #0x0,%d4
m68k_039e10_end:
.org 0x39E14
m68k_039e14:
        jsr 2444(%pc)
m68k_039e14_end:
.org 0x39E18
m68k_039e18:
        nop
m68k_039e18_end:
.org 0x39E1A
m68k_039e1a:
        bra.w (. + -796)
m68k_039e1a_end:
.org 0x39E3E
m68k_039e3e:
        cmpi.w #0x17,0xff7026:l
m68k_039e3e_end:
.org 0x39E46
m68k_039e46:
        bhi.w (. + 260)
m68k_039e46_end:
.org 0x39E4A
m68k_039e4a:
        jsr -1140(%pc)
m68k_039e4a_end:
.org 0x39E4E
m68k_039e4e:
        movea.l 192(%pc),%a0
m68k_039e4e_end:
.org 0x39E52
m68k_039e52:
        nop
m68k_039e52_end:
.org 0x39E54
m68k_039e54:
        move.w 0xff7028:l,%d0
m68k_039e54_end:
.org 0x39E5A
m68k_039e5a:
        move.w 0xff702a:l,%d1
m68k_039e5a_end:
.org 0x39E60
m68k_039e60:
        moveq #5,%d2
m68k_039e60_end:
.org 0x39E62
m68k_039e62:
        moveq #0,%d3
m68k_039e62_end:
.org 0x39E64
m68k_039e64:
        move.w #0x0,%d4
m68k_039e64_end:
.org 0x39E68
m68k_039e68:
        jsr 1846(%pc)
m68k_039e68_end:
.org 0x39E6C
m68k_039e6c:
        nop
m68k_039e6c_end:
.org 0x39E6E
m68k_039e6e:
        move.b 0xff702c:l,%d1
m68k_039e6e_end:
.org 0x39E74
m68k_039e74:
        move.w 0xff7028:l,%d2
m68k_039e74_end:
.org 0x39E7A
m68k_039e7a:
        move.w 0xff702a:l,%d3
m68k_039e7a_end:
.org 0x39E80
m68k_039e80:
        movem.l %d1-%d3,-(%a7)
m68k_039e80_end:
.org 0x39E84
m68k_039e84:
        addq.w #0x1,0xff7026:l
m68k_039e84_end:
.org 0x39E8A
m68k_039e8a:
        move.w 0xff7026:l,%d0
m68k_039e8a_end:
.org 0x39E90
m68k_039e90:
        lea.l -4162(%pc),%a0
m68k_039e90_end:
.org 0x39E94
m68k_039e94:
        move.b (%a0, %d0.w),%d1
m68k_039e94_end:
.org 0x39E98
m68k_039e98:
        move.b %d1,0xff702c:l
m68k_039e98_end:
.org 0x39E9E
m68k_039e9e:
        jsr 120(%pc)
m68k_039e9e_end:
.org 0x39EA2
m68k_039ea2:
        nop
m68k_039ea2_end:
.org 0x39EA4
m68k_039ea4:
        move.w 0xff7032:l,0xff7028:l
m68k_039ea4_end:
.org 0x39EAE
m68k_039eae:
        move.w 0xff7034:l,0xff702a:l
m68k_039eae_end:
.org 0x39EB8
m68k_039eb8:
        jsr -1250(%pc)
m68k_039eb8_end:
.org 0x39EBC
m68k_039ebc:
        moveq #4,%d1
m68k_039ebc_end:
.org 0x39EBE
m68k_039ebe:
        movea.l 80(%pc, %d1.w),%a0
m68k_039ebe_end:
.org 0x39EC2
m68k_039ec2:
        move.w 0xff7028:l,%d0
m68k_039ec2_end:
.org 0x39EC8
m68k_039ec8:
        move.w 0xff702a:l,%d1
m68k_039ec8_end:
.org 0x39ECE
m68k_039ece:
        moveq #4,%d2
m68k_039ece_end:
.org 0x39ED0
m68k_039ed0:
        moveq #0,%d3
m68k_039ed0_end:
.org 0x39ED2
m68k_039ed2:
        move.w #0x0,%d4
m68k_039ed2_end:
.org 0x39ED6
m68k_039ed6:
        jsr 1736(%pc)
m68k_039ed6_end:
.org 0x39EDA
m68k_039eda:
        nop
m68k_039eda_end:
.org 0x39EDC
m68k_039edc:
        move.w 0xff7028:l,0xff7032:l
m68k_039edc_end:
.org 0x39EE6
m68k_039ee6:
        move.w 0xff702a:l,0xff7034:l
m68k_039ee6_end:
.org 0x39EF0
m68k_039ef0:
        movem.l (%a7)+,%d1-%d3
m68k_039ef0_end:
.org 0x39EF4
m68k_039ef4:
        move.b %d1,0xff702c:l
m68k_039ef4_end:
.org 0x39EFA
m68k_039efa:
        move.w %d2,0xff7028:l
m68k_039efa_end:
.org 0x39F00
m68k_039f00:
        move.w %d3,0xff702a:l
m68k_039f00_end:
.org 0x39F06
m68k_039f06:
        subq.w #0x1,0xff7026:l
m68k_039f06_end:
.org 0x39F0C
m68k_039f0c:
        bra.w (. + -1038)
m68k_039f0c_end:
.org 0x39F18
m68k_039f18:
        tst.w 0xff7036:l
m68k_039f18_end:
.org 0x39F1E
m68k_039f1e:
        bne.w (. + 42)
m68k_039f1e_end:
.org 0x39F22
m68k_039f22:
        asl.w #0x1,%d0
m68k_039f22_end:
.org 0x39F24
m68k_039f24:
        lea.l -5022(%pc),%a0
m68k_039f24_end:
.org 0x39F28
m68k_039f28:
        lea.l -4946(%pc),%a1
m68k_039f28_end:
.org 0x39F2C
m68k_039f2c:
        move.w (%a0, %d0.w),%d1
m68k_039f2c_end:
.org 0x39F30
m68k_039f30:
        move.w (%a1, %d0.w),%d2
m68k_039f30_end:
.org 0x39F34
m68k_039f34:
        move.w %d1,0xff7032:l
m68k_039f34_end:
.org 0x39F3A
m68k_039f3a:
        move.w %d2,0xff7034:l
m68k_039f3a_end:
.org 0x39F40
m68k_039f40:
        move.w #0x1,0xff7036:l
m68k_039f40_end:
.org 0x39F48
m68k_039f48:
        rts
m68k_039f48_end:
.org 0x39F4A
m68k_039f4a:
        cmpi.w #0x19,0xff7026:l
m68k_039f4a_end:
.org 0x39F52
m68k_039f52:
        bhi.w (. + -472)
m68k_039f52_end:
.org 0x39F56
m68k_039f56:
        addq.w #0x1,0xff7044:l
m68k_039f56_end:
.org 0x39F5C
m68k_039f5c:
        move.w 0xf320:w,%d0
m68k_039f5c_end:
.org 0x39F60
m68k_039f60:
        btst.l #0x3,%d0
m68k_039f60_end:
.org 0x39F64
m68k_039f64:
        bne.w (. + 10)
m68k_039f64_end:
.org 0x39F68
m68k_039f68:
        moveq #0,%d1
m68k_039f68_end:
.org 0x39F6A
m68k_039f6a:
        bra.w (. + 6)
m68k_039f6a_end:
.org 0x39F6E
m68k_039f6e:
        moveq #4,%d1
m68k_039f6e_end:
.org 0x39F70
m68k_039f70:
        jsr 280(%pc)
m68k_039f70_end:
.org 0x39F74
m68k_039f74:
        nop
m68k_039f74_end:
.org 0x39F76
m68k_039f76:
        move.w #0x60,%d0
m68k_039f76_end:
.org 0x39F7A
m68k_039f7a:
        move.w #0x60,%d1
m68k_039f7a_end:
.org 0x39F7E
m68k_039f7e:
        moveq #5,%d2
m68k_039f7e_end:
.org 0x39F80
m68k_039f80:
        moveq #0,%d3
m68k_039f80_end:
.org 0x39F82
m68k_039f82:
        move.w #0x0,%d4
m68k_039f82_end:
.org 0x39F86
m68k_039f86:
        jsr 2074(%pc)
m68k_039f86_end:
.org 0x39F8A
m68k_039f8a:
        nop
m68k_039f8a_end:
.org 0x39F8C
m68k_039f8c:
        cmpi.w #0x20,0xff7044:l
m68k_039f8c_end:
.org 0x39F94
m68k_039f94:
        bcs.w (. + 208)
m68k_039f94_end:
.org 0x39F98
m68k_039f98:
        jsr -1474(%pc)
m68k_039f98_end:
.org 0x39F9C
m68k_039f9c:
        moveq #8,%d1
m68k_039f9c_end:
.org 0x39F9E
m68k_039f9e:
        jsr 234(%pc)
m68k_039f9e_end:
.org 0x39FA2
m68k_039fa2:
        nop
m68k_039fa2_end:
.org 0x39FA4
m68k_039fa4:
        move.w 0xff7028:l,%d0
m68k_039fa4_end:
.org 0x39FAA
m68k_039faa:
        move.w 0xff702a:l,%d1
m68k_039faa_end:
.org 0x39FB0
m68k_039fb0:
        moveq #4,%d2
m68k_039fb0_end:
.org 0x39FB2
m68k_039fb2:
        moveq #0,%d3
m68k_039fb2_end:
.org 0x39FB4
m68k_039fb4:
        move.w #0x0,%d4
m68k_039fb4_end:
.org 0x39FB8
m68k_039fb8:
        jsr 1510(%pc)
m68k_039fb8_end:
.org 0x39FBC
m68k_039fbc:
        nop
m68k_039fbc_end:
.org 0x39FBE
m68k_039fbe:
        cmpi.w #0x40,0xff7044:l
m68k_039fbe_end:
.org 0x39FC6
m68k_039fc6:
        bcs.w (. + 158)
m68k_039fc6_end:
.org 0x39FCA
m68k_039fca:
        move.w 0xff7028:l,%d0
m68k_039fca_end:
.org 0x39FD0
m68k_039fd0:
        move.w 0xff702a:l,%d1
m68k_039fd0_end:
.org 0x39FD6
m68k_039fd6:
        move.b 0xff702c:l,%d2
m68k_039fd6_end:
.org 0x39FDC
m68k_039fdc:
        movem.l %d0-%d2,-(%a7)
m68k_039fdc_end:
.org 0x39FE0
m68k_039fe0:
        addq.w #0x1,0xff7026:l
m68k_039fe0_end:
.org 0x39FE6
m68k_039fe6:
        move.w 0xff7026:l,%d0
m68k_039fe6_end:
.org 0x39FEC
m68k_039fec:
        lea.l -4510(%pc),%a0
m68k_039fec_end:
.org 0x39FF0
m68k_039ff0:
        move.b (%a0, %d0.w),%d1
m68k_039ff0_end:
.org 0x39FF4
m68k_039ff4:
        move.b %d1,0xff702c:l
m68k_039ff4_end:
.org 0x39FFA
m68k_039ffa:
        move.w 0xff7032:l,0xff7028:l
m68k_039ffa_end:
.org 0x3A004
m68k_03a004:
        move.w 0xff7034:l,0xff702a:l
m68k_03a004_end:
.org 0x3A00E
m68k_03a00e:
        jsr -1592(%pc)
m68k_03a00e_end:
.org 0x3A012
m68k_03a012:
        moveq #12,%d1
m68k_03a012_end:
.org 0x3A014
m68k_03a014:
        jsr 116(%pc)
m68k_03a014_end:
.org 0x3A018
m68k_03a018:
        nop
m68k_03a018_end:
.org 0x3A01A
m68k_03a01a:
        move.w 0xff7028:l,%d0
m68k_03a01a_end:
.org 0x3A020
m68k_03a020:
        move.w 0xff702a:l,%d1
m68k_03a020_end:
.org 0x3A026
m68k_03a026:
        moveq #4,%d2
m68k_03a026_end:
.org 0x3A028
m68k_03a028:
        moveq #0,%d3
m68k_03a028_end:
.org 0x3A02A
m68k_03a02a:
        move.w #0x0,%d4
m68k_03a02a_end:
.org 0x3A02E
m68k_03a02e:
        jsr 1392(%pc)
m68k_03a02e_end:
.org 0x3A032
m68k_03a032:
        nop
m68k_03a032_end:
.org 0x3A034
m68k_03a034:
        move.w 0xff7028:l,0xff7032:l
m68k_03a034_end:
.org 0x3A03E
m68k_03a03e:
        move.w 0xff702a:l,0xff7034:l
m68k_03a03e_end:
.org 0x3A048
m68k_03a048:
        movem.l (%a7)+,%d0-%d2
m68k_03a048_end:
.org 0x3A04C
m68k_03a04c:
        move.w %d0,0xff7028:l
m68k_03a04c_end:
.org 0x3A052
m68k_03a052:
        move.w %d1,0xff702a:l
m68k_03a052_end:
.org 0x3A058
m68k_03a058:
        move.b %d2,0xff702c:l
m68k_03a058_end:
.org 0x3A05E
m68k_03a05e:
        subq.w #0x1,0xff7026:l
m68k_03a05e_end:
.org 0x3A064
m68k_03a064:
        bra.w (. + -1382)
m68k_03a064_end:
.org 0x3A08A
m68k_03a08a:
        cmpi.w #0x1b,0xff7026:l
m68k_03a08a_end:
.org 0x3A092
m68k_03a092:
        bhi.w (. + 10)
m68k_03a092_end:
.org 0x3A096
m68k_03a096:
        movea.l -46(%pc, %d1.w),%a0
m68k_03a096_end:
.org 0x3A09A
m68k_03a09a:
        rts
m68k_03a09a_end:
.org 0x3A09C
m68k_03a09c:
        cmpi.w #0x7,%d1
m68k_03a09c_end:
.org 0x3A0A0
m68k_03a0a0:
        bhi.w (. + 62)
m68k_03a0a0_end:
.org 0x3A0A4
m68k_03a0a4:
        move.w 0xff703c:l,%d2
m68k_03a0a4_end:
.org 0x3A0AA
m68k_03a0aa:
        andi.w #0x7,%d0
m68k_03a0aa_end:
.org 0x3A0AE
m68k_03a0ae:
        bne.w (. + 16)
m68k_03a0ae_end:
.org 0x3A0B2
m68k_03a0b2:
        addq.w #0x1,0xff703c:l
m68k_03a0b2_end:
.org 0x3A0B8
m68k_03a0b8:
        move.w 0xff703c:l,%d2
m68k_03a0b8_end:
.org 0x3A0BE
m68k_03a0be:
        lea.l 36(%pc),%a3
m68k_03a0be_end:
.org 0x3A0C2
m68k_03a0c2:
        nop
m68k_03a0c2_end:
.org 0x3A0C4
m68k_03a0c4:
        move.b (%a3, %d2.w),%d1
m68k_03a0c4_end:
.org 0x3A0C8
m68k_03a0c8:
        cmpi.b #0xff,%d1
m68k_03a0c8_end:
.org 0x3A0CC
m68k_03a0cc:
        bne.w (. + 12)
m68k_03a0cc_end:
.org 0x3A0D0
m68k_03a0d0:
        clr.w 0xff703c:l
m68k_03a0d0_end:
.org 0x3A0D6
m68k_03a0d6:
        moveq #0,%d1
m68k_03a0d6_end:
.org 0x3A0D8
m68k_03a0d8:
        andi.l #0xf,%d1
m68k_03a0d8_end:
.org 0x3A0DE
m68k_03a0de:
        movea.l -102(%pc, %d1.w),%a0
m68k_03a0de_end:
.org 0x3A0E2
m68k_03a0e2:
        rts
m68k_03a0e2_end:
.org 0x3A114
m68k_03a114:
        cmpi.w #0x1c,0xff7026:l
m68k_03a114_end:
.org 0x3A11C
m68k_03a11c:
        beq.w (. + -454)
m68k_03a11c_end:
.org 0x3A120
m68k_03a120:
        cmpi.w #0x1d,0xff7026:l
m68k_03a120_end:
.org 0x3A128
m68k_03a128:
        bhi.w (. + 4)
m68k_03a128_end:
.org 0x3A12C
m68k_03a12c:
        cmpi.w #0x1e,0xff7026:l
m68k_03a12c_end:
.org 0x3A134
m68k_03a134:
        beq.w (. + -1952)
m68k_03a134_end:
.org 0x3A138
m68k_03a138:
        cmpi.w #0x1f,0xff7026:l
m68k_03a138_end:
.org 0x3A140
m68k_03a140:
        beq.w (. + -1930)
m68k_03a140_end:
.org 0x3A144
m68k_03a144:
        cmpi.w #0x20,0xff7026:l
m68k_03a144_end:
.org 0x3A14C
m68k_03a14c:
        beq.w (. + 148)
m68k_03a14c_end:
.org 0x3A150
m68k_03a150:
        cmpi.w #0x21,0xff7026:l
m68k_03a150_end:
.org 0x3A158
m68k_03a158:
        beq.w (. + 458)
m68k_03a158_end:
.org 0x3A15C
m68k_03a15c:
        cmpi.w #0x22,0xff7026:l
m68k_03a15c_end:
.org 0x3A164
m68k_03a164:
        beq.w (. + 618)
m68k_03a164_end:
.org 0x3A168
m68k_03a168:
        cmpi.w #0x23,0xff7026:l
m68k_03a168_end:
.org 0x3A170
m68k_03a170:
        beq.w (. + 794)
m68k_03a170_end:
.org 0x3A174
m68k_03a174:
        cmpi.w #0x25,0xff7026:l
m68k_03a174_end:
.org 0x3A17C
m68k_03a17c:
        beq.w (. + 850)
m68k_03a17c_end:
.org 0x3A180
m68k_03a180:
        cmpi.w #0x27,0xff7026:l
m68k_03a180_end:
.org 0x3A188
m68k_03a188:
        beq.w (. + 906)
m68k_03a188_end:
.org 0x3A18C
m68k_03a18c:
        cmpi.w #0x1f,0xff7026:l
m68k_03a18c_end:
.org 0x3A194
m68k_03a194:
        beq.w (. + 36)
m68k_03a194_end:
.org 0x3A198
m68k_03a198:
        movea.l 62(%pc),%a0
m68k_03a198_end:
.org 0x3A19C
m68k_03a19c:
        nop
m68k_03a19c_end:
.org 0x3A19E
m68k_03a19e:
        move.w #0x60,%d0
m68k_03a19e_end:
.org 0x3A1A2
m68k_03a1a2:
        move.w #0x60,%d1
m68k_03a1a2_end:
.org 0x3A1A6
m68k_03a1a6:
        moveq #5,%d2
m68k_03a1a6_end:
.org 0x3A1A8
m68k_03a1a8:
        moveq #0,%d3
m68k_03a1a8_end:
.org 0x3A1AA
m68k_03a1aa:
        move.w #0x0,%d4
m68k_03a1aa_end:
.org 0x3A1AE
m68k_03a1ae:
        jsr 1522(%pc)
m68k_03a1ae_end:
.org 0x3A1B2
m68k_03a1b2:
        nop
m68k_03a1b2_end:
.org 0x3A1B4
m68k_03a1b4:
        bra.w (. + -1718)
m68k_03a1b4_end:
.org 0x3A1B8
m68k_03a1b8:
        moveq #4,%d1
m68k_03a1b8_end:
.org 0x3A1BA
m68k_03a1ba:
        movea.l 28(%pc, %d1.w),%a0
m68k_03a1ba_end:
.org 0x3A1BE
m68k_03a1be:
        move.w #0x60,%d0
m68k_03a1be_end:
.org 0x3A1C2
m68k_03a1c2:
        move.w #0x60,%d1
m68k_03a1c2_end:
.org 0x3A1C6
m68k_03a1c6:
        moveq #4,%d2
m68k_03a1c6_end:
.org 0x3A1C8
m68k_03a1c8:
        moveq #0,%d3
m68k_03a1c8_end:
.org 0x3A1CA
m68k_03a1ca:
        move.w #0x0,%d4
m68k_03a1ca_end:
.org 0x3A1CE
m68k_03a1ce:
        jsr 1490(%pc)
m68k_03a1ce_end:
.org 0x3A1D2
m68k_03a1d2:
        nop
m68k_03a1d2_end:
.org 0x3A1D4
m68k_03a1d4:
        bra.w (. + -1750)
m68k_03a1d4_end:
.org 0x3A1E0
m68k_03a1e0:
        clr.l %d0
m68k_03a1e0_end:
.org 0x3A1E2
m68k_03a1e2:
        move.w 0xff703c:l,%d0
m68k_03a1e2_end:
.org 0x3A1E8
m68k_03a1e8:
        lea.l 242(%pc),%a1
m68k_03a1e8_end:
.org 0x3A1EC
m68k_03a1ec:
        nop
m68k_03a1ec_end:
.org 0x3A1EE
m68k_03a1ee:
        adda.w %d0,%a1
m68k_03a1ee_end:
.org 0x3A1F0
m68k_03a1f0:
        move.w (%a1),0xff7028:l
m68k_03a1f0_end:
.org 0x3A1F6
m68k_03a1f6:
        addi.w #0x2,0xff703c:l
m68k_03a1f6_end:
.org 0x3A1FE
m68k_03a1fe:
        move.w 0xff703c:l,%d0
m68k_03a1fe_end:
.org 0x3A204
m68k_03a204:
        lea.l 214(%pc),%a1
m68k_03a204_end:
.org 0x3A208
m68k_03a208:
        nop
m68k_03a208_end:
.org 0x3A20A
m68k_03a20a:
        adda.w %d0,%a1
m68k_03a20a_end:
.org 0x3A20C
m68k_03a20c:
        move.w #0x60,0xff702a:l
m68k_03a20c_end:
.org 0x3A214
m68k_03a214:
        move.w 0xf320:w,%d0
m68k_03a214_end:
.org 0x3A218
m68k_03a218:
        andi.w #0x3,%d0
m68k_03a218_end:
.org 0x3A21C
m68k_03a21c:
        beq.w (. + 14)
m68k_03a21c_end:
.org 0x3A220
m68k_03a220:
        subq.w #0x2,0xff703c:l
m68k_03a220_end:
.org 0x3A226
m68k_03a226:
        bra.w (. + 42)
m68k_03a226_end:
.org 0x3A22A
m68k_03a22a:
        addi.w #0x2,0xff703c:l
m68k_03a22a_end:
.org 0x3A232
m68k_03a232:
        lea.l 168(%pc),%a1
m68k_03a232_end:
.org 0x3A236
m68k_03a236:
        nop
m68k_03a236_end:
.org 0x3A238
m68k_03a238:
        adda.w 0xff703c:l,%a1
m68k_03a238_end:
.org 0x3A23E
m68k_03a23e:
        move.w (%a1),%d1
m68k_03a23e_end:
.org 0x3A240
m68k_03a240:
        cmpi.w #0xff,%d1
m68k_03a240_end:
.org 0x3A244
m68k_03a244:
        bne.w (. + 12)
m68k_03a244_end:
.org 0x3A248
m68k_03a248:
        move.w #0x0,0xff703c:l
m68k_03a248_end:
.org 0x3A250
m68k_03a250:
        lea.l -5326(%pc),%a1
m68k_03a250_end:
.org 0x3A254
m68k_03a254:
        movea.l (%a1),%a0
m68k_03a254_end:
.org 0x3A256
m68k_03a256:
        move.w 0xff7028:l,%d0
m68k_03a256_end:
.org 0x3A25C
m68k_03a25c:
        move.w 0xff702a:l,%d1
m68k_03a25c_end:
.org 0x3A262
m68k_03a262:
        moveq #3,%d2
m68k_03a262_end:
.org 0x3A264
m68k_03a264:
        moveq #0,%d3
m68k_03a264_end:
.org 0x3A266
m68k_03a266:
        move.w #0x0,%d4
m68k_03a266_end:
.org 0x3A26A
m68k_03a26a:
        jsr 820(%pc)
m68k_03a26a_end:
.org 0x3A26E
m68k_03a26e:
        nop
m68k_03a26e_end:
.org 0x3A270
m68k_03a270:
        cmpi.w #0x78,0xff703e:l
m68k_03a270_end:
.org 0x3A278
m68k_03a278:
        bcs.w (. + -1914)
m68k_03a278_end:
.org 0x3A27C
m68k_03a27c:
        cmpi.w #0x18,0xff7004:l
m68k_03a27c_end:
.org 0x3A284
m68k_03a284:
        beq.w (. + 52)
m68k_03a284_end:
.org 0x3A288
m68k_03a288:
        move.w 0xf320:w,%d0
m68k_03a288_end:
.org 0x3A28C
m68k_03a28c:
        andi.w #0x7,%d0
m68k_03a28c_end:
.org 0x3A290
m68k_03a290:
        bne.w (. + 40)
m68k_03a290_end:
.org 0x3A294
m68k_03a294:
        addq.w #0x4,0xff7004:l
m68k_03a294_end:
.org 0x3A29A
m68k_03a29a:
        clr.l %d3
m68k_03a29a_end:
.org 0x3A29C
m68k_03a29c:
        move.w 0xff7004:l,%d3
m68k_03a29c_end:
.org 0x3A2A2
m68k_03a2a2:
        lea.l 98(%pc),%a1
m68k_03a2a2_end:
.org 0x3A2A6
m68k_03a2a6:
        nop
m68k_03a2a6_end:
.org 0x3A2A8
m68k_03a2a8:
        movea.l (%a1, %d3.w),%a0
m68k_03a2a8_end:
.org 0x3A2AC
m68k_03a2ac:
        lea.l 0xfb00:w,%a1
m68k_03a2ac_end:
.org 0x3A2B0
m68k_03a2b0:
        moveq #7,%d0
m68k_03a2b0_end:
.org 0x3A2B2
m68k_03a2b2:
        move.l (%a0)+,(%a1)+
m68k_03a2b2_end:
.org 0x3A2B4
m68k_03a2b4:
        dbra %d0,(. + -2)
m68k_03a2b4_end:
.org 0x3A2B8
m68k_03a2b8:
        lea.l -5430(%pc),%a1
m68k_03a2b8_end:
.org 0x3A2BC
m68k_03a2bc:
        adda.w #0x4,%a1
m68k_03a2bc_end:
.org 0x3A2C0
m68k_03a2c0:
        movea.l (%a1),%a0
m68k_03a2c0_end:
.org 0x3A2C2
m68k_03a2c2:
        move.w #0x60,%d0
m68k_03a2c2_end:
.org 0x3A2C6
m68k_03a2c6:
        move.w #0x60,%d1
m68k_03a2c6_end:
.org 0x3A2CA
m68k_03a2ca:
        moveq #5,%d2
m68k_03a2ca_end:
.org 0x3A2CC
m68k_03a2cc:
        moveq #0,%d3
m68k_03a2cc_end:
.org 0x3A2CE
m68k_03a2ce:
        move.w #0x0,%d4
m68k_03a2ce_end:
.org 0x3A2D2
m68k_03a2d2:
        jsr 1230(%pc)
m68k_03a2d2_end:
.org 0x3A2D6
m68k_03a2d6:
        nop
m68k_03a2d6_end:
.org 0x3A2D8
m68k_03a2d8:
        bra.w (. + -2010)
m68k_03a2d8_end:
.org 0x3A322
m68k_03a322:
        jsr -2380(%pc)
m68k_03a322_end:
.org 0x3A326
m68k_03a326:
        lea.l -5532(%pc),%a1
m68k_03a326_end:
.org 0x3A32A
m68k_03a32a:
        movea.l (%a1),%a0
m68k_03a32a_end:
.org 0x3A32C
m68k_03a32c:
        move.w 0xff7028:l,%d0
m68k_03a32c_end:
.org 0x3A332
m68k_03a332:
        move.w 0xff702a:l,%d1
m68k_03a332_end:
.org 0x3A338
m68k_03a338:
        moveq #4,%d2
m68k_03a338_end:
.org 0x3A33A
m68k_03a33a:
        moveq #0,%d3
m68k_03a33a_end:
.org 0x3A33C
m68k_03a33c:
        move.w #0x0,%d4
m68k_03a33c_end:
.org 0x3A340
m68k_03a340:
        jsr 606(%pc)
m68k_03a340_end:
.org 0x3A344
m68k_03a344:
        nop
m68k_03a344_end:
.org 0x3A346
m68k_03a346:
        cmpi.w #0x78,0xff703e:l
m68k_03a346_end:
.org 0x3A34E
m68k_03a34e:
        bcs.w (. + -2128)
m68k_03a34e_end:
.org 0x3A352
m68k_03a352:
        cmpi.w #0x18,0xff703c:l
m68k_03a352_end:
.org 0x3A35A
m68k_03a35a:
        beq.w (. + 52)
m68k_03a35a_end:
.org 0x3A35E
m68k_03a35e:
        move.w 0xf320:w,%d0
m68k_03a35e_end:
.org 0x3A362
m68k_03a362:
        andi.w #0xf,%d0
m68k_03a362_end:
.org 0x3A366
m68k_03a366:
        bne.w (. + 40)
m68k_03a366_end:
.org 0x3A36A
m68k_03a36a:
        addq.w #0x4,0xff703c:l
m68k_03a36a_end:
.org 0x3A370
m68k_03a370:
        clr.l %d3
m68k_03a370_end:
.org 0x3A372
m68k_03a372:
        move.w 0xff703c:l,%d3
m68k_03a372_end:
.org 0x3A378
m68k_03a378:
        lea.l 56(%pc),%a1
m68k_03a378_end:
.org 0x3A37C
m68k_03a37c:
        nop
m68k_03a37c_end:
.org 0x3A37E
m68k_03a37e:
        movea.l (%a1, %d3.w),%a0
m68k_03a37e_end:
.org 0x3A382
m68k_03a382:
        lea.l 0xfb00:w,%a1
m68k_03a382_end:
.org 0x3A386
m68k_03a386:
        moveq #7,%d0
m68k_03a386_end:
.org 0x3A388
m68k_03a388:
        move.l (%a0)+,(%a1)+
m68k_03a388_end:
.org 0x3A38A
m68k_03a38a:
        dbra %d0,(. + -2)
m68k_03a38a_end:
.org 0x3A38E
m68k_03a38e:
        lea.l -5636(%pc),%a1
m68k_03a38e_end:
.org 0x3A392
m68k_03a392:
        adda.w #0x4,%a1
m68k_03a392_end:
.org 0x3A396
m68k_03a396:
        movea.l (%a1),%a0
m68k_03a396_end:
.org 0x3A398
m68k_03a398:
        move.w #0x60,%d0
m68k_03a398_end:
.org 0x3A39C
m68k_03a39c:
        move.w #0x60,%d1
m68k_03a39c_end:
.org 0x3A3A0
m68k_03a3a0:
        moveq #5,%d2
m68k_03a3a0_end:
.org 0x3A3A2
m68k_03a3a2:
        moveq #0,%d3
m68k_03a3a2_end:
.org 0x3A3A4
m68k_03a3a4:
        move.w #0x0,%d4
m68k_03a3a4_end:
.org 0x3A3A8
m68k_03a3a8:
        jsr 1016(%pc)
m68k_03a3a8_end:
.org 0x3A3AC
m68k_03a3ac:
        nop
m68k_03a3ac_end:
.org 0x3A3AE
m68k_03a3ae:
        bra.w (. + -2224)
m68k_03a3ae_end:
.org 0x3A3CE
m68k_03a3ce:
        addq.w #0x1,0xff7044:l
m68k_03a3ce_end:
.org 0x3A3D4
m68k_03a3d4:
        cmpi.w #0x80,0xff7044:l
m68k_03a3d4_end:
.org 0x3A3DC
m68k_03a3dc:
        bhi.w (. + 98)
m68k_03a3dc_end:
.org 0x3A3E0
m68k_03a3e0:
        move.b 0xf321:w,%d0
m68k_03a3e0_end:
.org 0x3A3E4
m68k_03a3e4:
        btst.l #0x2,%d0
m68k_03a3e4_end:
.org 0x3A3E8
m68k_03a3e8:
        bne.w (. + 36)
m68k_03a3e8_end:
.org 0x3A3EC
m68k_03a3ec:
        cmpi.w #0x2,0xff703c:l
m68k_03a3ec_end:
.org 0x3A3F4
m68k_03a3f4:
        bcs.w (. + 16)
m68k_03a3f4_end:
.org 0x3A3F8
m68k_03a3f8:
        move.w #0x0,0xff703c:l
m68k_03a3f8_end:
.org 0x3A400
m68k_03a400:
        bra.w (. + 12)
m68k_03a400_end:
.org 0x3A404
m68k_03a404:
        addi.w #0x1,0xff703c:l
m68k_03a404_end:
.org 0x3A40C
m68k_03a40c:
        move.w 0xff703c:l,%d1
m68k_03a40c_end:
.org 0x3A412
m68k_03a412:
        asl.w #0x2,%d1
m68k_03a412_end:
.org 0x3A414
m68k_03a414:
        movea.l 28(%pc, %d1.w),%a0
m68k_03a414_end:
.org 0x3A418
m68k_03a418:
        move.w #0x60,%d0
m68k_03a418_end:
.org 0x3A41C
m68k_03a41c:
        move.w #0x60,%d1
m68k_03a41c_end:
.org 0x3A420
m68k_03a420:
        moveq #5,%d2
m68k_03a420_end:
.org 0x3A422
m68k_03a422:
        moveq #0,%d3
m68k_03a422_end:
.org 0x3A424
m68k_03a424:
        move.w #0x0,%d4
m68k_03a424_end:
.org 0x3A428
m68k_03a428:
        jsr 888(%pc)
m68k_03a428_end:
.org 0x3A42C
m68k_03a42c:
        nop
m68k_03a42c_end:
.org 0x3A42E
m68k_03a42e:
        bra.w (. + -2352)
m68k_03a42e_end:
.org 0x3A43E
m68k_03a43e:
        movea.l 66(%pc),%a0
m68k_03a43e_end:
.org 0x3A442
m68k_03a442:
        nop
m68k_03a442_end:
.org 0x3A444
m68k_03a444:
        move.w #0x60,%d0
m68k_03a444_end:
.org 0x3A448
m68k_03a448:
        move.w #0x60,%d1
m68k_03a448_end:
.org 0x3A44C
m68k_03a44c:
        moveq #5,%d2
m68k_03a44c_end:
.org 0x3A44E
m68k_03a44e:
        moveq #0,%d3
m68k_03a44e_end:
.org 0x3A450
m68k_03a450:
        move.w #0x0,%d4
m68k_03a450_end:
.org 0x3A454
m68k_03a454:
        jsr 844(%pc)
m68k_03a454_end:
.org 0x3A458
m68k_03a458:
        nop
m68k_03a458_end:
.org 0x3A45A
m68k_03a45a:
        jsr -2692(%pc)
m68k_03a45a_end:
.org 0x3A45E
m68k_03a45e:
        moveq #4,%d1
m68k_03a45e_end:
.org 0x3A460
m68k_03a460:
        movea.l 32(%pc, %d1.w),%a0
m68k_03a460_end:
.org 0x3A464
m68k_03a464:
        move.w 0xff7028:l,%d0
m68k_03a464_end:
.org 0x3A46A
m68k_03a46a:
        move.w 0xff702a:l,%d1
m68k_03a46a_end:
.org 0x3A470
m68k_03a470:
        moveq #4,%d2
m68k_03a470_end:
.org 0x3A472
m68k_03a472:
        moveq #0,%d3
m68k_03a472_end:
.org 0x3A474
m68k_03a474:
        move.w #0x0,%d4
m68k_03a474_end:
.org 0x3A478
m68k_03a478:
        jsr 294(%pc)
m68k_03a478_end:
.org 0x3A47C
m68k_03a47c:
        nop
m68k_03a47c_end:
.org 0x3A47E
m68k_03a47e:
        bra.w (. + -2432)
m68k_03a47e_end:
.org 0x3A48A
m68k_03a48a:
        movea.l 58(%pc),%a0
m68k_03a48a_end:
.org 0x3A48E
m68k_03a48e:
        nop
m68k_03a48e_end:
.org 0x3A490
m68k_03a490:
        move.w #0x60,%d0
m68k_03a490_end:
.org 0x3A494
m68k_03a494:
        move.w #0x60,%d1
m68k_03a494_end:
.org 0x3A498
m68k_03a498:
        moveq #5,%d2
m68k_03a498_end:
.org 0x3A49A
m68k_03a49a:
        moveq #0,%d3
m68k_03a49a_end:
.org 0x3A49C
m68k_03a49c:
        move.w #0x0,%d4
m68k_03a49c_end:
.org 0x3A4A0
m68k_03a4a0:
        jsr 768(%pc)
m68k_03a4a0_end:
.org 0x3A4A4
m68k_03a4a4:
        nop
m68k_03a4a4_end:
.org 0x3A4A6
m68k_03a4a6:
        movea.l 34(%pc),%a0
m68k_03a4a6_end:
.org 0x3A4AA
m68k_03a4aa:
        nop
m68k_03a4aa_end:
.org 0x3A4AC
m68k_03a4ac:
        move.w #0x60,%d0
m68k_03a4ac_end:
.org 0x3A4B0
m68k_03a4b0:
        move.w #0x60,%d1
m68k_03a4b0_end:
.org 0x3A4B4
m68k_03a4b4:
        moveq #5,%d2
m68k_03a4b4_end:
.org 0x3A4B6
m68k_03a4b6:
        moveq #0,%d3
m68k_03a4b6_end:
.org 0x3A4B8
m68k_03a4b8:
        move.w #0x100,%d4
m68k_03a4b8_end:
.org 0x3A4BC
m68k_03a4bc:
        jsr 740(%pc)
m68k_03a4bc_end:
.org 0x3A4C0
m68k_03a4c0:
        nop
m68k_03a4c0_end:
.org 0x3A4C2
m68k_03a4c2:
        bra.w (. + -2500)
m68k_03a4c2_end:
.org 0x3A4CE
m68k_03a4ce:
        movea.l 58(%pc),%a0
m68k_03a4ce_end:
.org 0x3A4D2
m68k_03a4d2:
        nop
m68k_03a4d2_end:
.org 0x3A4D4
m68k_03a4d4:
        move.w #0x60,%d0
m68k_03a4d4_end:
.org 0x3A4D8
m68k_03a4d8:
        move.w #0x60,%d1
m68k_03a4d8_end:
.org 0x3A4DC
m68k_03a4dc:
        moveq #5,%d2
m68k_03a4dc_end:
.org 0x3A4DE
m68k_03a4de:
        moveq #0,%d3
m68k_03a4de_end:
.org 0x3A4E0
m68k_03a4e0:
        move.w #0x0,%d4
m68k_03a4e0_end:
.org 0x3A4E4
m68k_03a4e4:
        jsr 700(%pc)
m68k_03a4e4_end:
.org 0x3A4E8
m68k_03a4e8:
        nop
m68k_03a4e8_end:
.org 0x3A4EA
m68k_03a4ea:
        movea.l 34(%pc),%a0
m68k_03a4ea_end:
.org 0x3A4EE
m68k_03a4ee:
        nop
m68k_03a4ee_end:
.org 0x3A4F0
m68k_03a4f0:
        move.w #0x60,%d0
m68k_03a4f0_end:
.org 0x3A4F4
m68k_03a4f4:
        move.w #0x60,%d1
m68k_03a4f4_end:
.org 0x3A4F8
m68k_03a4f8:
        moveq #5,%d2
m68k_03a4f8_end:
.org 0x3A4FA
m68k_03a4fa:
        moveq #0,%d3
m68k_03a4fa_end:
.org 0x3A4FC
m68k_03a4fc:
        move.w #0x100,%d4
m68k_03a4fc_end:
.org 0x3A500
m68k_03a500:
        jsr 672(%pc)
m68k_03a500_end:
.org 0x3A504
m68k_03a504:
        nop
m68k_03a504_end:
.org 0x3A506
m68k_03a506:
        bra.w (. + -2568)
m68k_03a506_end:
.org 0x3A512
m68k_03a512:
        movea.l 30(%pc),%a0
m68k_03a512_end:
.org 0x3A516
m68k_03a516:
        nop
m68k_03a516_end:
.org 0x3A518
m68k_03a518:
        move.w #0x60,%d0
m68k_03a518_end:
.org 0x3A51C
m68k_03a51c:
        move.w #0x60,%d1
m68k_03a51c_end:
.org 0x3A520
m68k_03a520:
        moveq #5,%d2
m68k_03a520_end:
.org 0x3A522
m68k_03a522:
        moveq #0,%d3
m68k_03a522_end:
.org 0x3A524
m68k_03a524:
        move.w #0x0,%d4
m68k_03a524_end:
.org 0x3A528
m68k_03a528:
        jsr 632(%pc)
m68k_03a528_end:
.org 0x3A52C
m68k_03a52c:
        nop
m68k_03a52c_end:
.org 0x3A52E
m68k_03a52e:
        bra.w (. + -2608)
m68k_03a52e_end:
.org 0x3A5CE
m68k_03a5ce:
        subi.w #0x8,%d0
m68k_03a5ce_end:
.org 0x3A5DC
m68k_03a5dc:
        subi.w #0x8,%d1
m68k_03a5dc_end:
.org 0x3A64C
m68k_03a64c:
        neg.b %d5
m68k_03a64c_end:
.org 0x3A6AA
m68k_03a6aa:
        neg.b %d5
m68k_03a6aa_end:
.org 0x3A716
m68k_03a716:
        move.w #0x1,0xff7030:l
m68k_03a716_end:
.org 0x3A71E
m68k_03a71e:
        bra.w (. + -232)
m68k_03a71e_end:
.org 0x3A722
m68k_03a722:
        move.w #0x1,0xff7030:l
m68k_03a722_end:
.org 0x3A72A
m68k_03a72a:
        bra.w (. + -148)
m68k_03a72a_end:
.org 0x3A7A2
m68k_03a7a2:
        movem.l %d5-%d6/%a1,-(%a7)
m68k_03a7a2_end:
.org 0x3A7A6
m68k_03a7a6:
        cmpi.b #0x80,0xf300:w
m68k_03a7a6_end:
.org 0x3A7AC
m68k_03a7ac:
        bcc.w (. + 234)
m68k_03a7ac_end:
.org 0x3A7B0
m68k_03a7b0:
        andi.l #0xffff,%d4
m68k_03a7b0_end:
.org 0x3A7B6
m68k_03a7b6:
        move.w %d2,%d7
m68k_03a7b6_end:
.org 0x3A7B8
m68k_03a7b8:
        andi.w #0xfff8,%d2
m68k_03a7b8_end:
.org 0x3A7BC
m68k_03a7bc:
        andi.w #0x7,%d7
m68k_03a7bc_end:
.org 0x3A7C0
m68k_03a7c0:
        asl.w #0x2,%d7
m68k_03a7c0_end:
.org 0x3A7C2
m68k_03a7c2:
        addi.w #0x80,%d0
m68k_03a7c2_end:
.org 0x3A7C6
m68k_03a7c6:
        bmi.w (. + 208)
m68k_03a7c6_end:
.org 0x3A7CA
m68k_03a7ca:
        btst.l #0x5,%d2
m68k_03a7ca_end:
.org 0x3A7CE
m68k_03a7ce:
        beq.b (. + 6)
m68k_03a7ce_end:
.org 0x3A7D0
m68k_03a7d0:
        subi.w #0x8,%d0
m68k_03a7d0_end:
.org 0x3A7D4
m68k_03a7d4:
        addi.w #0x80,%d1
m68k_03a7d4_end:
.org 0x3A7D8
m68k_03a7d8:
        btst.l #0x4,%d2
m68k_03a7d8_end:
.org 0x3A7DC
m68k_03a7dc:
        beq.b (. + 6)
m68k_03a7dc_end:
.org 0x3A7DE
m68k_03a7de:
        subi.w #0x8,%d1
m68k_03a7de_end:
.org 0x3A7E2
m68k_03a7e2:
        clr.w %d5
m68k_03a7e2_end:
.org 0x3A7E4
m68k_03a7e4:
        move.b 0xf300:w,%d5
m68k_03a7e4_end:
.org 0x3A7E8
m68k_03a7e8:
        lsl.w #0x3,%d5
m68k_03a7e8_end:
.org 0x3A7EA
m68k_03a7ea:
        lea.l 0xf800:w,%a1
m68k_03a7ea_end:
.org 0x3A7EE
m68k_03a7ee:
        lea.l 0xff7006:l,%a2
m68k_03a7ee_end:
.org 0x3A7F4
m68k_03a7f4:
        lea.l (%a1, %d5.w),%a1
m68k_03a7f4_end:
.org 0x3A7F8
m68k_03a7f8:
        move.w %d0,%d6
m68k_03a7f8_end:
.org 0x3A7FA
m68k_03a7fa:
        moveq #0,%d5
m68k_03a7fa_end:
.org 0x3A7FC
m68k_03a7fc:
        move.b (%a0),%d5
m68k_03a7fc_end:
.org 0x3A7FE
m68k_03a7fe:
        cmpi.b #0x80,%d5
m68k_03a7fe_end:
.org 0x3A802
m68k_03a802:
        beq.w (. + 148)
m68k_03a802_end:
.org 0x3A806
m68k_03a806:
        btst.l #0x5,%d2
m68k_03a806_end:
.org 0x3A80A
m68k_03a80a:
        beq.w (. + 6)
m68k_03a80a_end:
.org 0x3A80E
m68k_03a80e:
        neg.b %d5
m68k_03a80e_end:
.org 0x3A810
m68k_03a810:
        btst.l #0x7,%d5
m68k_03a810_end:
.org 0x3A814
m68k_03a814:
        beq.b (. + 8)
m68k_03a814_end:
.org 0x3A816
m68k_03a816:
        neg.b %d5
m68k_03a816_end:
.org 0x3A818
m68k_03a818:
        sub.w %d5,%d6
m68k_03a818_end:
.org 0x3A81A
m68k_03a81a:
        bra.b (. + 4)
m68k_03a81a_end:
.org 0x3A81C
m68k_03a81c:
        add.w %d5,%d6
m68k_03a81c_end:
.org 0x3A81E
m68k_03a81e:
        move.w %d6,(%a1)
m68k_03a81e_end:
.org 0x3A820
m68k_03a820:
        move.w %d1,%d6
m68k_03a820_end:
.org 0x3A822
m68k_03a822:
        move.b 0x3(%a0),%d5
m68k_03a822_end:
.org 0x3A826
m68k_03a826:
        btst.l #0x4,%d2
m68k_03a826_end:
.org 0x3A82A
m68k_03a82a:
        beq.b (. + 4)
m68k_03a82a_end:
.org 0x3A82C
m68k_03a82c:
        neg.b %d5
m68k_03a82c_end:
.org 0x3A82E
m68k_03a82e:
        btst.l #0x7,%d5
m68k_03a82e_end:
.org 0x3A832
m68k_03a832:
        btst.l #0x7,%d5
m68k_03a832_end:
.org 0x3A836
m68k_03a836:
        beq.b (. + 8)
m68k_03a836_end:
.org 0x3A838
m68k_03a838:
        neg.b %d5
m68k_03a838_end:
.org 0x3A83A
m68k_03a83a:
        sub.w %d5,%d6
m68k_03a83a_end:
.org 0x3A83C
m68k_03a83c:
        bra.b (. + 4)
m68k_03a83c_end:
.org 0x3A83E
m68k_03a83e:
        add.w %d5,%d6
m68k_03a83e_end:
.org 0x3A840
m68k_03a840:
        move.w %d6,0x6(%a1)
m68k_03a840_end:
.org 0x3A844
m68k_03a844:
        move.b 0x1(%a0),0x2(%a1)
m68k_03a844_end:
.org 0x3A84A
m68k_03a84a:
        tst.l (%a2, %d7.w)
m68k_03a84a_end:
.org 0x3A84E
m68k_03a84e:
        bne.w (. + 16)
m68k_03a84e_end:
.org 0x3A852
m68k_03a852:
        move.l %a1,(%a2, %d7.w)
m68k_03a852_end:
.org 0x3A856
m68k_03a856:
        move.b 0xf300:w,0x20(%a2, %d7.w)
m68k_03a856_end:
.org 0x3A85C
m68k_03a85c:
        bra.b (. + 12)
m68k_03a85c_end:
.org 0x3A85E
m68k_03a85e:
        movea.l 0x40(%a2, %d7.w),%a3
m68k_03a85e_end:
.org 0x3A862
m68k_03a862:
        move.b 0xf300:w,0x3(%a3)
m68k_03a862_end:
.org 0x3A868
m68k_03a868:
        move.l %a1,0x40(%a2, %d7.w)
m68k_03a868_end:
.org 0x3A86C
m68k_03a86c:
        addq.b #0x1,0xf300:w
m68k_03a86c_end:
.org 0x3A870
m68k_03a870:
        move.b 0x1(%a0),%d5
m68k_03a870_end:
.org 0x3A874
m68k_03a874:
        andi.w #0xf0,%d5
m68k_03a874_end:
.org 0x3A878
m68k_03a878:
        add.b %d3,%d5
m68k_03a878_end:
.org 0x3A87A
m68k_03a87a:
        eor.w %d2,%d5
m68k_03a87a_end:
.org 0x3A87C
m68k_03a87c:
        asl.w #0x7,%d5
m68k_03a87c_end:
.org 0x3A87E
m68k_03a87e:
        or.b 0x2(%a0),%d5
m68k_03a87e_end:
.org 0x3A882
m68k_03a882:
        add.w %d4,%d5
m68k_03a882_end:
.org 0x3A884
m68k_03a884:
        move.w %d5,0x4(%a1)
m68k_03a884_end:
.org 0x3A888
m68k_03a888:
        addq.l #0x8,%a1
m68k_03a888_end:
.org 0x3A88A
m68k_03a88a:
        addq.l #0x4,%a0
m68k_03a88a_end:
.org 0x3A88C
m68k_03a88c:
        cmpi.b #0x80,0xf300:w
m68k_03a88c_end:
.org 0x3A892
m68k_03a892:
        bcs.w (. + -154)
m68k_03a892_end:
.org 0x3A896
m68k_03a896:
        movem.l (%a7)+,%d5-%d6/%a1
m68k_03a896_end:
.org 0x3A89A
m68k_03a89a:
        rts
m68k_03a89a_end:
.org 0x3A998
m68k_03a998:
        addq.w #0x1,0x80c8:w
m68k_03a998_end:
.org 0x3A99C
m68k_03a99c:
        cmpi.w #0xf,0x80c8:w
m68k_03a99c_end:
.org 0x3A9A2
m68k_03a9a2:
        bhi.w (. + 16)
m68k_03a9a2_end:
.org 0x3A9A6
m68k_03a9a6:
        bra.w (. + 20)
m68k_03a9a6_end:
.org 0x3AA38
m68k_03aa38:
        move.w 0x80c4:w,%d1
m68k_03aa38_end:
.org 0x3AA3C
m68k_03aa3c:
        bmi.w (. + 30)
m68k_03aa3c_end:
.org 0x3AA40
m68k_03aa40:
        andi.w #0xff00,%d1
m68k_03aa40_end:
.org 0x3AA44
m68k_03aa44:
        cmpi.w #0x100,%d1
m68k_03aa44_end:
.org 0x3AA48
m68k_03aa48:
        beq.w (. + -144)
m68k_03aa48_end:
.org 0x3AA4C
m68k_03aa4c:
        movem.l %d0,-(%a7)
m68k_03aa4c_end:
.org 0x3AA50
m68k_03aa50:
        jsr 76(%pc)
m68k_03aa50_end:
.org 0x3AA54
m68k_03aa54:
        nop
m68k_03aa54_end:
.org 0x3AA56
m68k_03aa56:
        movem.l (%a7)+,%d0
m68k_03aa56_end:
.org 0x3AA5A
m68k_03aa5a:
        andi.w #0xff,%d0
m68k_03aa5a_end:
.org 0x3AA5E
m68k_03aa5e:
        ori.w #0x100,%d0
m68k_03aa5e_end:
.org 0x3AA62
m68k_03aa62:
        move.w %d0,0x80c4:w
m68k_03aa62_end:
.org 0x3AA66
m68k_03aa66:
        move.w #0x0,0x80c6:w
m68k_03aa66_end:
.org 0x3AA6C
m68k_03aa6c:
        move.w #0x0,0x80c8:w
m68k_03aa6c_end:
.org 0x3AA72
m68k_03aa72:
        bsr.b (. + 6)
m68k_03aa72_end:
.org 0x3AA74
m68k_03aa74:
        jmp -254(%pc)
m68k_03aa74_end:
.org 0x3AA78
m68k_03aa78:
        moveq #31,%d1
m68k_03aa78_end:
.org 0x3AA7A
m68k_03aa7a:
        lea.l 0xfb00:w,%a0
m68k_03aa7a_end:
.org 0x3AA7E
m68k_03aa7e:
        lea.l 0xfb80:w,%a1
m68k_03aa7e_end:
.org 0x3AA82
m68k_03aa82:
        move.l (%a0)+,(%a1)+
m68k_03aa82_end:
.org 0x3AA84
m68k_03aa84:
        dbra %d1,(. + -2)
m68k_03aa84_end:
.org 0x3AA88
m68k_03aa88:
        rts
m68k_03aa88_end:
.org 0x3AA9E
m68k_03aa9e:
        moveq #31,%d1
m68k_03aa9e_end:
.org 0x3AAA0
m68k_03aaa0:
        lea.l 0xfb00:w,%a1
m68k_03aaa0_end:
.org 0x3AAA4
m68k_03aaa4:
        lea.l 0xfb80:w,%a0
m68k_03aaa4_end:
.org 0x3AAA8
m68k_03aaa8:
        move.l (%a0)+,(%a1)+
m68k_03aaa8_end:
.org 0x3AAAA
m68k_03aaaa:
        dbra %d1,(. + -2)
m68k_03aaaa_end:
.org 0x3AAAE
m68k_03aaae:
        move.w #0xffff,0x80c4:w
m68k_03aaae_end:
.org 0x3AAB4
m68k_03aab4:
        rts
m68k_03aab4_end:
.org 0x3B13C
m68k_03b13c:
        movem.l %d5-%d6/%a1,-(%a7)
m68k_03b13c_end:
.org 0x3B140
m68k_03b140:
        cmpi.b #0x50,0xf300:w
m68k_03b140_end:
.org 0x3B146
m68k_03b146:
        bcc.w (. + 240)
m68k_03b146_end:
.org 0x3B14A
m68k_03b14a:
        andi.l #0xffff,%d4
m68k_03b14a_end:
.org 0x3B150
m68k_03b150:
        move.w %d2,%d7
m68k_03b150_end:
.org 0x3B152
m68k_03b152:
        andi.w #0xfff8,%d2
m68k_03b152_end:
.org 0x3B156
m68k_03b156:
        andi.w #0x7,%d7
m68k_03b156_end:
.org 0x3B15A
m68k_03b15a:
        asl.w #0x2,%d7
m68k_03b15a_end:
.org 0x3B15C
m68k_03b15c:
        sub.w 0x8020:w,%d0
m68k_03b15c_end:
.org 0x3B160
m68k_03b160:
        addi.w #0x80,%d0
m68k_03b160_end:
.org 0x3B164
m68k_03b164:
        bmi.w (. + 210)
m68k_03b164_end:
.org 0x3B168
m68k_03b168:
        btst.l #0x5,%d2
m68k_03b168_end:
.org 0x3B16C
m68k_03b16c:
        beq.b (. + 6)
m68k_03b16c_end:
.org 0x3B16E
m68k_03b16e:
        subi.w #0x8,%d0
m68k_03b16e_end:
.org 0x3B172
m68k_03b172:
        sub.w 0x8022:w,%d1
m68k_03b172_end:
.org 0x3B176
m68k_03b176:
        addi.w #0x80,%d1
m68k_03b176_end:
.org 0x3B17A
m68k_03b17a:
        btst.l #0x4,%d2
m68k_03b17a_end:
.org 0x3B17E
m68k_03b17e:
        beq.b (. + 6)
m68k_03b17e_end:
.org 0x3B180
m68k_03b180:
        subi.w #0x8,%d1
m68k_03b180_end:
.org 0x3B184
m68k_03b184:
        clr.w %d5
m68k_03b184_end:
.org 0x3B186
m68k_03b186:
        move.b 0xf300:w,%d5
m68k_03b186_end:
.org 0x3B18A
m68k_03b18a:
        lsl.w #0x3,%d5
m68k_03b18a_end:
.org 0x3B18C
m68k_03b18c:
        lea.l 0xf800:w,%a1
m68k_03b18c_end:
.org 0x3B190
m68k_03b190:
        lea.l 0x8044:w,%a2
m68k_03b190_end:
.org 0x3B194
m68k_03b194:
        lea.l (%a1, %d5.w),%a1
m68k_03b194_end:
.org 0x3B198
m68k_03b198:
        move.w %d0,%d6
m68k_03b198_end:
.org 0x3B19A
m68k_03b19a:
        moveq #0,%d5
m68k_03b19a_end:
.org 0x3B19C
m68k_03b19c:
        move.b (%a0),%d5
m68k_03b19c_end:
.org 0x3B19E
m68k_03b19e:
        cmpi.b #0x80,%d5
m68k_03b19e_end:
.org 0x3B1A2
m68k_03b1a2:
        beq.w (. + 148)
m68k_03b1a2_end:
.org 0x3B1A6
m68k_03b1a6:
        btst.l #0x5,%d2
m68k_03b1a6_end:
.org 0x3B1AA
m68k_03b1aa:
        beq.w (. + 6)
m68k_03b1aa_end:
.org 0x3B1AE
m68k_03b1ae:
        neg.b %d5
m68k_03b1ae_end:
.org 0x3B1B0
m68k_03b1b0:
        btst.l #0x7,%d5
m68k_03b1b0_end:
.org 0x3B1B4
m68k_03b1b4:
        beq.b (. + 8)
m68k_03b1b4_end:
.org 0x3B1B6
m68k_03b1b6:
        neg.b %d5
m68k_03b1b6_end:
.org 0x3B1B8
m68k_03b1b8:
        sub.w %d5,%d6
m68k_03b1b8_end:
.org 0x3B1BA
m68k_03b1ba:
        bra.b (. + 4)
m68k_03b1ba_end:
.org 0x3B1BC
m68k_03b1bc:
        add.w %d5,%d6
m68k_03b1bc_end:
.org 0x3B1BE
m68k_03b1be:
        move.w %d6,(%a1)
m68k_03b1be_end:
.org 0x3B1C0
m68k_03b1c0:
        move.w %d1,%d6
m68k_03b1c0_end:
.org 0x3B1C2
m68k_03b1c2:
        move.b 0x3(%a0),%d5
m68k_03b1c2_end:
.org 0x3B1C6
m68k_03b1c6:
        btst.l #0x4,%d2
m68k_03b1c6_end:
.org 0x3B1CA
m68k_03b1ca:
        beq.b (. + 4)
m68k_03b1ca_end:
.org 0x3B1CC
m68k_03b1cc:
        neg.b %d5
m68k_03b1cc_end:
.org 0x3B1CE
m68k_03b1ce:
        btst.l #0x7,%d5
m68k_03b1ce_end:
.org 0x3B1D2
m68k_03b1d2:
        btst.l #0x7,%d5
m68k_03b1d2_end:
.org 0x3B1D6
m68k_03b1d6:
        beq.b (. + 8)
m68k_03b1d6_end:
.org 0x3B1D8
m68k_03b1d8:
        neg.b %d5
m68k_03b1d8_end:
.org 0x3B1DA
m68k_03b1da:
        sub.w %d5,%d6
m68k_03b1da_end:
.org 0x3B1DC
m68k_03b1dc:
        bra.b (. + 4)
m68k_03b1dc_end:
.org 0x3B1DE
m68k_03b1de:
        add.w %d5,%d6
m68k_03b1de_end:
.org 0x3B1E0
m68k_03b1e0:
        move.w %d6,0x6(%a1)
m68k_03b1e0_end:
.org 0x3B1E4
m68k_03b1e4:
        move.b 0x1(%a0),0x2(%a1)
m68k_03b1e4_end:
.org 0x3B1EA
m68k_03b1ea:
        tst.l (%a2, %d7.w)
m68k_03b1ea_end:
.org 0x3B1EE
m68k_03b1ee:
        bne.w (. + 16)
m68k_03b1ee_end:
.org 0x3B1F2
m68k_03b1f2:
        move.l %a1,(%a2, %d7.w)
m68k_03b1f2_end:
.org 0x3B1F6
m68k_03b1f6:
        move.b 0xf300:w,0x20(%a2, %d7.w)
m68k_03b1f6_end:
.org 0x3B1FC
m68k_03b1fc:
        bra.b (. + 12)
m68k_03b1fc_end:
.org 0x3B1FE
m68k_03b1fe:
        movea.l 0x40(%a2, %d7.w),%a3
m68k_03b1fe_end:
.org 0x3B202
m68k_03b202:
        move.b 0xf300:w,0x3(%a3)
m68k_03b202_end:
.org 0x3B208
m68k_03b208:
        move.l %a1,0x40(%a2, %d7.w)
m68k_03b208_end:
.org 0x3B20C
m68k_03b20c:
        addq.b #0x1,0xf300:w
m68k_03b20c_end:
.org 0x3B210
m68k_03b210:
        move.b 0x1(%a0),%d5
m68k_03b210_end:
.org 0x3B214
m68k_03b214:
        andi.w #0xf0,%d5
m68k_03b214_end:
.org 0x3B218
m68k_03b218:
        add.b %d3,%d5
m68k_03b218_end:
.org 0x3B21A
m68k_03b21a:
        eor.w %d2,%d5
m68k_03b21a_end:
.org 0x3B21C
m68k_03b21c:
        asl.w #0x7,%d5
m68k_03b21c_end:
.org 0x3B21E
m68k_03b21e:
        or.b 0x2(%a0),%d5
m68k_03b21e_end:
.org 0x3B222
m68k_03b222:
        add.w %d4,%d5
m68k_03b222_end:
.org 0x3B224
m68k_03b224:
        move.w %d5,0x4(%a1)
m68k_03b224_end:
.org 0x3B228
m68k_03b228:
        addq.l #0x8,%a1
m68k_03b228_end:
.org 0x3B22A
m68k_03b22a:
        addq.l #0x4,%a0
m68k_03b22a_end:
.org 0x3B22C
m68k_03b22c:
        cmpi.b #0x50,0xf300:w
m68k_03b22c_end:
.org 0x3B232
m68k_03b232:
        bcs.w (. + -154)
m68k_03b232_end:
.org 0x3B236
m68k_03b236:
        movem.l (%a7)+,%d5-%d6/%a1
m68k_03b236_end:
.org 0x3B23A
m68k_03b23a:
        rts
m68k_03b23a_end:
.org 0x3B23C
m68k_03b23c:
        moveq #28,%d0
m68k_03b23c_end:
.org 0x3B23E
m68k_03b23e:
        moveq #0,%d1
m68k_03b23e_end:
.org 0x3B240
m68k_03b240:
        lea.l 0x8044:w,%a0
m68k_03b240_end:
.org 0x3B244
m68k_03b244:
        bsr.b (. + 46)
m68k_03b244_end:
.org 0x3B246
m68k_03b246:
        subq.w #0x4,%d0
m68k_03b246_end:
.org 0x3B248
m68k_03b248:
        bpl.b (. + -4)
m68k_03b248_end:
.org 0x3B24A
m68k_03b24a:
        moveq #0,%d0
m68k_03b24a_end:
.org 0x3B24C
m68k_03b24c:
        move.l %d0,(%a0)
m68k_03b24c_end:
.org 0x3B24E
m68k_03b24e:
        move.l %d0,0x4(%a0)
m68k_03b24e_end:
.org 0x3B252
m68k_03b252:
        move.l %d0,0x8(%a0)
m68k_03b252_end:
.org 0x3B256
m68k_03b256:
        move.l %d0,0xc(%a0)
m68k_03b256_end:
.org 0x3B25A
m68k_03b25a:
        move.l %d0,0x10(%a0)
m68k_03b25a_end:
.org 0x3B25E
m68k_03b25e:
        move.l %d0,0x14(%a0)
m68k_03b25e_end:
.org 0x3B262
m68k_03b262:
        move.l %d0,0x18(%a0)
m68k_03b262_end:
.org 0x3B266
m68k_03b266:
        move.l %d0,0x1c(%a0)
m68k_03b266_end:
.org 0x3B26A
m68k_03b26a:
        move.b #0x0,0xf300:w
m68k_03b26a_end:
.org 0x3B270
m68k_03b270:
        rts
m68k_03b270_end:
.org 0x3B272
m68k_03b272:
        tst.l (%a0, %d0.w)
m68k_03b272_end:
.org 0x3B276
m68k_03b276:
        beq.w (. + 16)
m68k_03b276_end:
.org 0x3B27A
m68k_03b27a:
        movea.l 0x40(%a0, %d0.w),%a1
m68k_03b27a_end:
.org 0x3B27E
m68k_03b27e:
        move.b %d1,0x3(%a1)
m68k_03b27e_end:
.org 0x3B282
m68k_03b282:
        move.b 0x20(%a0, %d0.w),%d1
m68k_03b282_end:
.org 0x3B286
m68k_03b286:
        rts
m68k_03b286_end:
.org 0x3B288
m68k_03b288:
        move.w 0x8020:w,%d0
m68k_03b288_end:
.org 0x3B28C
m68k_03b28c:
        subi.w #0x40,%d0
m68k_03b28c_end:
.org 0x3B290
m68k_03b290:
        move.w 0x8022:w,%d1
m68k_03b290_end:
.org 0x3B294
m68k_03b294:
        subi.w #0x40,%d1
m68k_03b294_end:
.org 0x3B298
m68k_03b298:
        moveq #0,%d2
m68k_03b298_end:
.org 0x3B29A
m68k_03b29a:
        moveq #0,%d3
m68k_03b29a_end:
.org 0x3B29C
m68k_03b29c:
        move.w #0x0,%d4
m68k_03b29c_end:
.org 0x3B2A0
m68k_03b2a0:
        lea.l 8(%pc),%a0
m68k_03b2a0_end:
.org 0x3B2A4
m68k_03b2a4:
        nop
m68k_03b2a4_end:
.org 0x3B2A6
m68k_03b2a6:
        jmp -364(%pc)
m68k_03b2a6_end:
.org 0x3B722
m68k_03b722:
        movem.l %d1,-(%a7)
m68k_03b722_end:
.org 0x3B726
m68k_03b726:
        jsr 0x83d4:l
m68k_03b726_end:
.org 0x3B72C
m68k_03b72c:
        movem.l (%a7)+,%d1
m68k_03b72c_end:
.org 0x3B730
m68k_03b730:
        rts
m68k_03b730_end:
.org 0x3D672
m68k_03d672:
        bsr.w (. + 814)
m68k_03d672_end:
.org 0x3D676
m68k_03d676:
        moveq #0,%d0
m68k_03d676_end:
.org 0x3D678
m68k_03d678:
        move.b 0x80db:w,%d0
m68k_03d678_end:
.org 0x3D67C
m68k_03d67c:
        jsr -10986(%pc)
m68k_03d67c_end:
.org 0x3D680
m68k_03d680:
        move.w #0xffff,0x80ca:w
m68k_03d680_end:
.org 0x3D686
m68k_03d686:
        move.w #0xffff,0x80cc:w
m68k_03d686_end:
.org 0x3D68C
m68k_03d68c:
        move.w #0xffff,0x80ce:w
m68k_03d68c_end:
.org 0x3D692
m68k_03d692:
        move.w #0xffff,0x80d0:w
m68k_03d692_end:
.org 0x3D698
m68k_03d698:
        moveq #1,%d0
m68k_03d698_end:
.org 0x3D69A
m68k_03d69a:
        jsr -11388(%pc)
m68k_03d69a_end:
.org 0x3D69E
m68k_03d69e:
        jsr -11286(%pc)
m68k_03d69e_end:
.org 0x3D6A2
m68k_03d6a2:
        cmpi.w #0x3,0x813a:w
m68k_03d6a2_end:
.org 0x3D6A8
m68k_03d6a8:
        bne.w (. + 106)
m68k_03d6a8_end:
.org 0x3D6AC
m68k_03d6ac:
        bsr.w (. + 11376)
m68k_03d6ac_end:
.org 0x3D6B0
m68k_03d6b0:
        move.w #0x0,0x813a:w
m68k_03d6b0_end:
.org 0x3D6B6
m68k_03d6b6:
        move.w #0x6,0x813c:w
m68k_03d6b6_end:
.org 0x3D6BC
m68k_03d6bc:
        clr.w 0x813e:w
m68k_03d6bc_end:
.org 0x3D6C0
m68k_03d6c0:
        tst.w 0x8124:w
m68k_03d6c0_end:
.org 0x3D6C4
m68k_03d6c4:
        bne.b (. + 50)
m68k_03d6c4_end:
.org 0x3D6C6
m68k_03d6c6:
        move.w 0xff706c:l,0x8178:w
m68k_03d6c6_end:
.org 0x3D6CE
m68k_03d6ce:
        move.w 0xff70bc:l,0x8278:w
m68k_03d6ce_end:
.org 0x3D6D6
m68k_03d6d6:
        cmpi.b #0x1,0xff70f0:l
m68k_03d6d6_end:
.org 0x3D6DE
m68k_03d6de:
        bne.w (. + 14)
m68k_03d6de_end:
.org 0x3D6E2
m68k_03d6e2:
        move.w #0x6,0x8130:w
m68k_03d6e2_end:
.org 0x3D6E8
m68k_03d6e8:
        bra.w (. + 248)
m68k_03d6e8_end:
.org 0x3D6EC
m68k_03d6ec:
        move.w #0x6,0x8138:w
m68k_03d6ec_end:
.org 0x3D6F2
m68k_03d6f2:
        bra.w (. + 238)
m68k_03d6f2_end:
.org 0x3D6F6
m68k_03d6f6:
        move.w 0xff706c:l,0x8278:w
m68k_03d6f6_end:
.org 0x3D6FE
m68k_03d6fe:
        move.w 0xff70bc:l,0x8178:w
m68k_03d6fe_end:
.org 0x3D706
m68k_03d706:
        cmpi.b #0x1,0xff70f0:l
m68k_03d706_end:
.org 0x3D70E
m68k_03d70e:
        beq.b (. + -34)
m68k_03d70e_end:
.org 0x3D710
m68k_03d710:
        bra.b (. + -46)
m68k_03d710_end:
.org 0x3D712
m68k_03d712:
        move.w #0x0,0x8020:w
m68k_03d712_end:
.org 0x3D718
m68k_03d718:
        move.l #0x0,0x8024:w
m68k_03d718_end:
.org 0x3D720
m68k_03d720:
        move.w #0x107,%d0
m68k_03d720_end:
.org 0x3D724
m68k_03d724:
        lea.l 0x812a:w,%a0
m68k_03d724_end:
.org 0x3D728
m68k_03d728:
        clr.w (%a0)+
m68k_03d728_end:
.org 0x3D72A
m68k_03d72a:
        dbra %d0,(. + -2)
m68k_03d72a_end:
.org 0x3D72E
m68k_03d72e:
        move.w #0x5,0x812a:w
m68k_03d72e_end:
.org 0x3D734
m68k_03d734:
        move.w #0x5,0x812c:w
m68k_03d734_end:
.org 0x3D73A
m68k_03d73a:
        move.w #0x5,0x812e:w
m68k_03d73a_end:
.org 0x3D740
m68k_03d740:
        move.w #0x5,0x8130:w
m68k_03d740_end:
.org 0x3D746
m68k_03d746:
        move.w #0x5,0x8132:w
m68k_03d746_end:
.org 0x3D74C
m68k_03d74c:
        move.w #0x5,0x8134:w
m68k_03d74c_end:
.org 0x3D752
m68k_03d752:
        move.w #0x5,0x8136:w
m68k_03d752_end:
.org 0x3D758
m68k_03d758:
        move.w #0x5,0x8138:w
m68k_03d758_end:
.org 0x3D75E
m68k_03d75e:
        move.w #0x9,0x813a:w
m68k_03d75e_end:
.org 0x3D764
m68k_03d764:
        move.w #0x0,0x813c:w
m68k_03d764_end:
.org 0x3D76A
m68k_03d76a:
        bra.w (. + 112)
m68k_03d76a_end:
.org 0x3D7DA
m68k_03d7da:
        jsr 16410(%pc)
m68k_03d7da_end:
.org 0x3D7DE
m68k_03d7de:
        nop
m68k_03d7de_end:
.org 0x3D7E0
m68k_03d7e0:
        move.w #0x8e,%d0
m68k_03d7e0_end:
.org 0x3D7E4
m68k_03d7e4:
        jsr 0x808a:l
m68k_03d7e4_end:
.org 0x3D7EA
m68k_03d7ea:
        move.w #0x2500,%sr
m68k_03d7ea_end:
.org 0x3D7EE
m68k_03d7ee:
        move.w #0x500,0xf612:w
m68k_03d7ee_end:
.org 0x3D7F4
m68k_03d7f4:
        jsr 0x83c8:l
m68k_03d7f4_end:
.org 0x3D7FA
m68k_03d7fa:
        clr.w 0xf612:w
m68k_03d7fa_end:
.org 0x3D7FE
m68k_03d7fe:
        jsr -9592(%pc)
m68k_03d7fe_end:
.org 0x3D802
m68k_03d802:
        bsr.w (. + 8334)
m68k_03d802_end:
.org 0x3D806
m68k_03d806:
        jsr -11920(%pc)
m68k_03d806_end:
.org 0x3D80A
m68k_03d80a:
        jsr 1196(%pc)
m68k_03d80a_end:
.org 0x3D80E
m68k_03d80e:
        nop
m68k_03d80e_end:
.org 0x3D810
m68k_03d810:
        jsr 11050(%pc)
m68k_03d810_end:
.org 0x3D814
m68k_03d814:
        nop
m68k_03d814_end:
.org 0x3D816
m68k_03d816:
        jsr -9692(%pc)
m68k_03d816_end:
.org 0x3D81A
m68k_03d81a:
        jsr 200(%pc)
m68k_03d81a_end:
.org 0x3D81E
m68k_03d81e:
        nop
m68k_03d81e_end:
.org 0x3D84A
m68k_03d84a:
        cmpi.w #0x4,0x813a:w
m68k_03d84a_end:
.org 0x3D850
m68k_03d850:
        bne.b (. + 36)
m68k_03d850_end:
.org 0x3D852
m68k_03d852:
        cmpi.w #0x3,0x813c:w
m68k_03d852_end:
.org 0x3D858
m68k_03d858:
        bne.b (. + 28)
m68k_03d858_end:
.org 0x3D85A
m68k_03d85a:
        move.w #0x0,0x8114:w
m68k_03d85a_end:
.org 0x3D860
m68k_03d860:
        move.w #0x2700,%sr
m68k_03d860_end:
.org 0x3D864
m68k_03d864:
        move.w 0xf606:w,%d0
m68k_03d864_end:
.org 0x3D868
m68k_03d868:
        andi.b #0xbf,%d0
m68k_03d868_end:
.org 0x3D86C
m68k_03d86c:
        move.w %d0,0xc00004:l
m68k_03d86c_end:
.org 0x3D872
m68k_03d872:
        rts
m68k_03d872_end:
.org 0x3D874
m68k_03d874:
        cmpi.w #0x5,0x813a:w
m68k_03d874_end:
.org 0x3D87A
m68k_03d87a:
        bne.b (. + 30)
m68k_03d87a_end:
.org 0x3D87C
m68k_03d87c:
        cmpi.w #0x3,0x813c:w
m68k_03d87c_end:
.org 0x3D882
m68k_03d882:
        bne.b (. + 22)
m68k_03d882_end:
.org 0x3D884
m68k_03d884:
        move.w #0x2700,%sr
m68k_03d884_end:
.org 0x3D888
m68k_03d888:
        move.w 0xf606:w,%d0
m68k_03d888_end:
.org 0x3D88C
m68k_03d88c:
        andi.b #0xbf,%d0
m68k_03d88c_end:
.org 0x3D890
m68k_03d890:
        move.w %d0,0xc00004:l
m68k_03d890_end:
.org 0x3D896
m68k_03d896:
        rts
m68k_03d896_end:
.org 0x3D898
m68k_03d898:
        cmpi.w #0x6,0x813a:w
m68k_03d898_end:
.org 0x3D89E
m68k_03d89e:
        bne.b (. + 36)
m68k_03d89e_end:
.org 0x3D8A0
m68k_03d8a0:
        cmpi.w #0x4,0x813c:w
m68k_03d8a0_end:
.org 0x3D8A6
m68k_03d8a6:
        bne.b (. + 28)
m68k_03d8a6_end:
.org 0x3D8A8
m68k_03d8a8:
        move.w #0x6,0x8114:w
m68k_03d8a8_end:
.org 0x3D8AE
m68k_03d8ae:
        move.w #0x2700,%sr
m68k_03d8ae_end:
.org 0x3D8B2
m68k_03d8b2:
        move.w 0xf606:w,%d0
m68k_03d8b2_end:
.org 0x3D8B6
m68k_03d8b6:
        andi.b #0xbf,%d0
m68k_03d8b6_end:
.org 0x3D8BA
m68k_03d8ba:
        move.w %d0,0xc00004:l
m68k_03d8ba_end:
.org 0x3D8C0
m68k_03d8c0:
        rts
m68k_03d8c0_end:
.org 0x3D8C2
m68k_03d8c2:
        move.b 0xf602:w,%d0
m68k_03d8c2_end:
.org 0x3D8C6
m68k_03d8c6:
        andi.b #0xf0,%d0
m68k_03d8c6_end:
.org 0x3D8CA
m68k_03d8ca:
        cmpi.b #0xf0,%d0
m68k_03d8ca_end:
.org 0x3D8CE
m68k_03d8ce:
        bne.w (. + -224)
m68k_03d8ce_end:
.org 0x3D8D2
m68k_03d8d2:
        cmpi.b #0x3,0x80db:w
m68k_03d8d2_end:
.org 0x3D8D8
m68k_03d8d8:
        bcc.w (. + -644)
m68k_03d8d8_end:
.org 0x3D8DC
m68k_03d8dc:
        addq.b #0x1,0x80db:w
m68k_03d8dc_end:
.org 0x3D8E0
m68k_03d8e0:
        bra.w (. + -652)
m68k_03d8e0_end:
.org 0x3D8E4
m68k_03d8e4:
        move.w 0x8024:w,%d0
m68k_03d8e4_end:
.org 0x3D8E8
m68k_03d8e8:
        swap %d0
m68k_03d8e8_end:
.org 0x3D8EA
m68k_03d8ea:
        move.w 0x802c:w,%d0
m68k_03d8ea_end:
.org 0x3D8EE
m68k_03d8ee:
        moveq #0,%d1
m68k_03d8ee_end:
.org 0x3D8F0
m68k_03d8f0:
        move.w 0x8038:w,%d1
m68k_03d8f0_end:
.org 0x3D8F4
m68k_03d8f4:
        bpl.w (. + 16)
m68k_03d8f4_end:
.org 0x3D8F8
m68k_03d8f8:
        andi.w #0x7fff,%d1
m68k_03d8f8_end:
.org 0x3D8FC
m68k_03d8fc:
        asl.l #0x8,%d1
m68k_03d8fc_end:
.org 0x3D8FE
m68k_03d8fe:
        add.l %d1,%d0
m68k_03d8fe_end:
.org 0x3D900
m68k_03d900:
        bra.w (. + 8)
m68k_03d900_end:
.org 0x3D904
m68k_03d904:
        asl.l #0x8,%d1
m68k_03d904_end:
.org 0x3D906
m68k_03d906:
        sub.l %d1,%d0
m68k_03d906_end:
.org 0x3D908
m68k_03d908:
        move.w %d0,0x802c:w
m68k_03d908_end:
.org 0x3D90C
m68k_03d90c:
        swap %d0
m68k_03d90c_end:
.org 0x3D90E
m68k_03d90e:
        move.w %d0,0x8024:w
m68k_03d90e_end:
.org 0x3D912
m68k_03d912:
        move.w 0x8026:w,%d0
m68k_03d912_end:
.org 0x3D916
m68k_03d916:
        swap %d0
m68k_03d916_end:
.org 0x3D918
m68k_03d918:
        move.w 0x802e:w,%d0
m68k_03d918_end:
.org 0x3D91C
m68k_03d91c:
        moveq #0,%d1
m68k_03d91c_end:
.org 0x3D91E
m68k_03d91e:
        move.w 0x803a:w,%d1
m68k_03d91e_end:
.org 0x3D922
m68k_03d922:
        bpl.w (. + 16)
m68k_03d922_end:
.org 0x3D926
m68k_03d926:
        andi.w #0x7fff,%d1
m68k_03d926_end:
.org 0x3D92A
m68k_03d92a:
        asl.l #0x8,%d1
m68k_03d92a_end:
.org 0x3D92C
m68k_03d92c:
        add.l %d1,%d0
m68k_03d92c_end:
.org 0x3D92E
m68k_03d92e:
        bra.w (. + 8)
m68k_03d92e_end:
.org 0x3D932
m68k_03d932:
        asl.l #0x8,%d1
m68k_03d932_end:
.org 0x3D934
m68k_03d934:
        sub.l %d1,%d0
m68k_03d934_end:
.org 0x3D936
m68k_03d936:
        move.w %d0,0x802e:w
m68k_03d936_end:
.org 0x3D93A
m68k_03d93a:
        swap %d0
m68k_03d93a_end:
.org 0x3D93C
m68k_03d93c:
        move.w %d0,0x8026:w
m68k_03d93c_end:
.org 0x3D940
m68k_03d940:
        move.w 0x8020:w,%d0
m68k_03d940_end:
.org 0x3D944
m68k_03d944:
        swap %d0
m68k_03d944_end:
.org 0x3D946
m68k_03d946:
        move.w 0x8034:w,%d0
m68k_03d946_end:
.org 0x3D94A
m68k_03d94a:
        moveq #0,%d1
m68k_03d94a_end:
.org 0x3D94C
m68k_03d94c:
        move.w 0x8040:w,%d1
m68k_03d94c_end:
.org 0x3D950
m68k_03d950:
        bpl.w (. + 16)
m68k_03d950_end:
.org 0x3D954
m68k_03d954:
        andi.w #0x7fff,%d1
m68k_03d954_end:
.org 0x3D958
m68k_03d958:
        asl.l #0x8,%d1
m68k_03d958_end:
.org 0x3D95A
m68k_03d95a:
        add.l %d1,%d0
m68k_03d95a_end:
.org 0x3D95C
m68k_03d95c:
        bra.w (. + 8)
m68k_03d95c_end:
.org 0x3D960
m68k_03d960:
        asl.l #0x8,%d1
m68k_03d960_end:
.org 0x3D962
m68k_03d962:
        sub.l %d1,%d0
m68k_03d962_end:
.org 0x3D964
m68k_03d964:
        move.w %d0,0x8034:w
m68k_03d964_end:
.org 0x3D968
m68k_03d968:
        swap %d0
m68k_03d968_end:
.org 0x3D96A
m68k_03d96a:
        move.w %d0,0x8020:w
m68k_03d96a_end:
.org 0x3D96E
m68k_03d96e:
        rts
m68k_03d96e_end:
.org 0x3D9A0
m68k_03d9a0:
        move.w #0x8f02,0xc00004:l
m68k_03d9a0_end:
.org 0x3D9A8
m68k_03d9a8:
        move.w #0x8230,0xc00004:l
m68k_03d9a8_end:
.org 0x3D9B0
m68k_03d9b0:
        move.w #0x8330,0xc00004:l
m68k_03d9b0_end:
.org 0x3D9B8
m68k_03d9b8:
        move.w #0x8407,0xc00004:l
m68k_03d9b8_end:
.org 0x3D9C0
m68k_03d9c0:
        move.w #0x8568,0xc00004:l
m68k_03d9c0_end:
.org 0x3D9C8
m68k_03d9c8:
        move.w #0x8700,0xc00004:l
m68k_03d9c8_end:
.org 0x3D9D0
m68k_03d9d0:
        move.w #0x8b00,0xc00004:l
m68k_03d9d0_end:
.org 0x3D9D8
m68k_03d9d8:
        move.w #0x8c81,0xc00004:l
m68k_03d9d8_end:
.org 0x3D9E0
m68k_03d9e0:
        move.w #0x8d35,0xc00004:l
m68k_03d9e0_end:
.org 0x3D9E8
m68k_03d9e8:
        move.w #0x8f02,0xc00004:l
m68k_03d9e8_end:
.org 0x3D9F0
m68k_03d9f0:
        move.w #0x9011,0xc00004:l
m68k_03d9f0_end:
.org 0x3D9F8
m68k_03d9f8:
        move.w #0x9194,0xc00004:l
m68k_03d9f8_end:
.org 0x3DA00
m68k_03da00:
        move.w #0x9200,0xc00004:l
m68k_03da00_end:
.org 0x3DA08
m68k_03da08:
        lea.l 0x473e4:l,%a0
m68k_03da08_end:
.org 0x3DA0E
m68k_03da0e:
        move.w #0x0,%d0
m68k_03da0e_end:
.org 0x3DA12
m68k_03da12:
        bsr.w (. + -11968)
m68k_03da12_end:
.org 0x3DA16
m68k_03da16:
        lea.l 0x492e8:l,%a0
m68k_03da16_end:
.org 0x3DA1C
m68k_03da1c:
        move.w #0x2000,%d0
m68k_03da1c_end:
.org 0x3DA20
m68k_03da20:
        bsr.w (. + -11982)
m68k_03da20_end:
.org 0x3DA24
m68k_03da24:
        lea.l 0x4a9a2:l,%a0
m68k_03da24_end:
.org 0x3DA2A
m68k_03da2a:
        move.w #0x4000,%d0
m68k_03da2a_end:
.org 0x3DA2E
m68k_03da2e:
        bsr.w (. + -11996)
m68k_03da2e_end:
.org 0x3DA32
m68k_03da32:
        lea.l 0x4c5ac:l,%a0
m68k_03da32_end:
.org 0x3DA38
m68k_03da38:
        move.w #0x6000,%d0
m68k_03da38_end:
.org 0x3DA3C
m68k_03da3c:
        bsr.w (. + -12010)
m68k_03da3c_end:
.org 0x3DA40
m68k_03da40:
        lea.l 0x4e090:l,%a0
m68k_03da40_end:
.org 0x3DA46
m68k_03da46:
        move.w #0x8000,%d0
m68k_03da46_end:
.org 0x3DA4A
m68k_03da4a:
        bsr.w (. + -12024)
m68k_03da4a_end:
.org 0x3DA4E
m68k_03da4e:
        moveq #0,%d0
m68k_03da4e_end:
.org 0x3DA50
m68k_03da50:
        move.b 0x80db:w,%d0
m68k_03da50_end:
.org 0x3DA54
m68k_03da54:
        asl.w #0x2,%d0
m68k_03da54_end:
.org 0x3DA56
m68k_03da56:
        lea.l 116(%pc),%a0
m68k_03da56_end:
.org 0x3DA5A
m68k_03da5a:
        nop
m68k_03da5a_end:
.org 0x3DA5C
m68k_03da5c:
        movea.l (%a0, %d0.w),%a0
m68k_03da5c_end:
.org 0x3DA60
m68k_03da60:
        lea.l 0xe000:l,%a1
m68k_03da60_end:
.org 0x3DA66
m68k_03da66:
        move.l #0x80,%d5
m68k_03da66_end:
.org 0x3DA6C
m68k_03da6c:
        jsr -12192(%pc)
m68k_03da6c_end:
.org 0x3DA70
m68k_03da70:
        moveq #0,%d0
m68k_03da70_end:
.org 0x3DA72
m68k_03da72:
        move.b 0x80db:w,%d0
m68k_03da72_end:
.org 0x3DA76
m68k_03da76:
        asl.w #0x2,%d0
m68k_03da76_end:
.org 0x3DA78
m68k_03da78:
        lea.l 98(%pc),%a0
m68k_03da78_end:
.org 0x3DA7C
m68k_03da7c:
        nop
m68k_03da7c_end:
.org 0x3DA7E
m68k_03da7e:
        movea.l (%a0, %d0.w),%a0
m68k_03da7e_end:
.org 0x3DA82
m68k_03da82:
        lea.l 0xe040:l,%a1
m68k_03da82_end:
.org 0x3DA88
m68k_03da88:
        move.l #0x80,%d5
m68k_03da88_end:
.org 0x3DA8E
m68k_03da8e:
        jsr -12226(%pc)
m68k_03da8e_end:
.org 0x3DA92
m68k_03da92:
        moveq #0,%d0
m68k_03da92_end:
.org 0x3DA94
m68k_03da94:
        move.b 0x80db:w,%d0
m68k_03da94_end:
.org 0x3DA98
m68k_03da98:
        asl.w #0x2,%d0
m68k_03da98_end:
.org 0x3DA9A
m68k_03da9a:
        movea.l 48(%pc, %d0.w),%a0
m68k_03da9a_end:
.org 0x3DA9E
m68k_03da9e:
        lea.l 0xf000:l,%a1
m68k_03da9e_end:
.org 0x3DAA4
m68k_03daa4:
        move.l #0x80,%d5
m68k_03daa4_end:
.org 0x3DAAA
m68k_03daaa:
        jsr -12254(%pc)
m68k_03daaa_end:
.org 0x3DAAE
m68k_03daae:
        moveq #0,%d0
m68k_03daae_end:
.org 0x3DAB0
m68k_03dab0:
        move.b 0x80db:w,%d0
m68k_03dab0_end:
.org 0x3DAB4
m68k_03dab4:
        asl.w #0x2,%d0
m68k_03dab4_end:
.org 0x3DAB6
m68k_03dab6:
        movea.l 36(%pc, %d0.w),%a0
m68k_03dab6_end:
.org 0x3DABA
m68k_03daba:
        lea.l 0xf040:l,%a1
m68k_03daba_end:
.org 0x3DAC0
m68k_03dac0:
        move.l #0x80,%d5
m68k_03dac0_end:
.org 0x3DAC6
m68k_03dac6:
        jsr -12282(%pc)
m68k_03dac6_end:
.org 0x3DACA
m68k_03daca:
        rts
m68k_03daca_end:
.org 0x3DCB8
m68k_03dcb8:
        move.w 0x813a:w,%d0
m68k_03dcb8_end:
.org 0x3DCBC
m68k_03dcbc:
        asl.w #0x2,%d0
m68k_03dcbc_end:
.org 0x3DCBE
m68k_03dcbe:
        jmp 2(%pc, %d0.w)
m68k_03dcbe_end:
.org 0x3DD94
m68k_03dd94:
        move.w #0x2700,%sr
m68k_03dd94_end:
.org 0x3DD98
m68k_03dd98:
        lea.l 0x4539c:l,%a0
m68k_03dd98_end:
.org 0x3DD9E
m68k_03dd9e:
        lea.l 0xc000:l,%a1
m68k_03dd9e_end:
.org 0x3DDA4
m68k_03dda4:
        move.l #0x80,%d5
m68k_03dda4_end:
.org 0x3DDAA
m68k_03ddaa:
        move.w #0x8000,0x8000:w
m68k_03ddaa_end:
.org 0x3DDB0
m68k_03ddb0:
        move.w #0x12,%d6
m68k_03ddb0_end:
.org 0x3DDB4
m68k_03ddb4:
        jsr -13024(%pc)
m68k_03ddb4_end:
.org 0x3DDB8
m68k_03ddb8:
        move.w #0x1,0x8116:w
m68k_03ddb8_end:
.org 0x3DDBE
m68k_03ddbe:
        move.w #0x8f02,0xc00004:l
m68k_03ddbe_end:
.org 0x3DDC6
m68k_03ddc6:
        move.l #0x60000002,0xc00004:l
m68k_03ddc6_end:
.org 0x3DDD0
m68k_03ddd0:
        lea.l 0xc00000:l,%a5
m68k_03ddd0_end:
.org 0x3DDD6
m68k_03ddd6:
        move.w #0x3333,%d6
m68k_03ddd6_end:
.org 0x3DDDA
m68k_03ddda:
        move.w #0xd7f,%d7
m68k_03ddda_end:
.org 0x3DDDE
m68k_03ddde:
        move.w %d6,(%a5)
m68k_03ddde_end:
.org 0x3DDE0
m68k_03dde0:
        dbra %d7,(. + -2)
m68k_03dde0_end:
.org 0x3DDE4
m68k_03dde4:
        move.w #0xa000,0xff700c:l
m68k_03dde4_end:
.org 0x3DDEC
m68k_03ddec:
        move.l #0x3b43e,0xff700e:l
m68k_03ddec_end:
.org 0x3DDF6
m68k_03ddf6:
        move.w #0x3,0xff7014:l
m68k_03ddf6_end:
.org 0x3DDFE
m68k_03ddfe:
        move.w #0x1,0xff7016:l
m68k_03ddfe_end:
.org 0x3DE06
m68k_03de06:
        move.w #0x4,0x813c:w
m68k_03de06_end:
.org 0x3DE0C
m68k_03de0c:
        bsr.w (. + 3286)
m68k_03de0c_end:
.org 0x3DE10
m68k_03de10:
        move.w 0x80e0:w,%d0
m68k_03de10_end:
.org 0x3DE14
m68k_03de14:
        move.w #0x480,%d1
m68k_03de14_end:
.org 0x3DE18
m68k_03de18:
        jsr 0x661d4:l
m68k_03de18_end:
.org 0x3DE1E
m68k_03de1e:
        move.w #0x2500,%sr
m68k_03de1e_end:
.org 0x3DE22
m68k_03de22:
        rts
m68k_03de22_end:
.org 0x3DE24
m68k_03de24:
        move.w #0x2700,%sr
m68k_03de24_end:
.org 0x3DE28
m68k_03de28:
        lea.l 0x4539c:l,%a0
m68k_03de28_end:
.org 0x3DE2E
m68k_03de2e:
        lea.l 0xc000:l,%a1
m68k_03de2e_end:
.org 0x3DE34
m68k_03de34:
        move.l #0x80,%d5
m68k_03de34_end:
.org 0x3DE3A
m68k_03de3a:
        move.w #0x8000,0x8000:w
m68k_03de3a_end:
.org 0x3DE40
m68k_03de40:
        move.w #0x12,%d6
m68k_03de40_end:
.org 0x3DE44
m68k_03de44:
        jsr -13168(%pc)
m68k_03de44_end:
.org 0x3DE48
m68k_03de48:
        move.w #0x1,0x8116:w
m68k_03de48_end:
.org 0x3DE4E
m68k_03de4e:
        move.w #0x8f02,0xc00004:l
m68k_03de4e_end:
.org 0x3DE56
m68k_03de56:
        move.l #0x60000002,0xc00004:l
m68k_03de56_end:
.org 0x3DE60
m68k_03de60:
        lea.l 0xc00000:l,%a5
m68k_03de60_end:
.org 0x3DE66
m68k_03de66:
        move.w #0x3333,%d6
m68k_03de66_end:
.org 0x3DE6A
m68k_03de6a:
        move.w #0xd7f,%d7
m68k_03de6a_end:
.org 0x3DE6E
m68k_03de6e:
        move.w %d6,(%a5)
m68k_03de6e_end:
.org 0x3DE70
m68k_03de70:
        dbra %d7,(. + -2)
m68k_03de70_end:
.org 0x3DE74
m68k_03de74:
        move.w #0xa000,0xff700c:l
m68k_03de74_end:
.org 0x3DE7C
m68k_03de7c:
        move.l #0x3b388,0xff700e:l
m68k_03de7c_end:
.org 0x3DE86
m68k_03de86:
        move.w #0x3,0xff7014:l
m68k_03de86_end:
.org 0x3DE8E
m68k_03de8e:
        move.w #0x1,0xff7016:l
m68k_03de8e_end:
.org 0x3DE96
m68k_03de96:
        move.w #0x1,0x813c:w
m68k_03de96_end:
.org 0x3DE9C
m68k_03de9c:
        bsr.w (. + 3142)
m68k_03de9c_end:
.org 0x3DEA0
m68k_03dea0:
        move.w #0x2500,%sr
m68k_03dea0_end:
.org 0x3DEA4
m68k_03dea4:
        rts
m68k_03dea4_end:
.org 0x3DEA6
m68k_03dea6:
        move.w #0x2700,%sr
m68k_03dea6_end:
.org 0x3DEAA
m68k_03deaa:
        lea.l 0x4539c:l,%a0
m68k_03deaa_end:
.org 0x3DEB0
m68k_03deb0:
        lea.l 0xc000:l,%a1
m68k_03deb0_end:
.org 0x3DEB6
m68k_03deb6:
        move.l #0x80,%d5
m68k_03deb6_end:
.org 0x3DEBC
m68k_03debc:
        move.w #0x8000,0x8000:w
m68k_03debc_end:
.org 0x3DEC2
m68k_03dec2:
        move.w #0x12,%d6
m68k_03dec2_end:
.org 0x3DEC6
m68k_03dec6:
        jsr -13298(%pc)
m68k_03dec6_end:
.org 0x3DECA
m68k_03deca:
        move.w #0x1,0x8116:w
m68k_03deca_end:
.org 0x3DED0
m68k_03ded0:
        move.w #0x8f02,0xc00004:l
m68k_03ded0_end:
.org 0x3DED8
m68k_03ded8:
        move.l #0x60000002,0xc00004:l
m68k_03ded8_end:
.org 0x3DEE2
m68k_03dee2:
        lea.l 0xc00000:l,%a5
m68k_03dee2_end:
.org 0x3DEE8
m68k_03dee8:
        move.w #0x3333,%d6
m68k_03dee8_end:
.org 0x3DEEC
m68k_03deec:
        move.w #0xd7f,%d7
m68k_03deec_end:
.org 0x3DEF0
m68k_03def0:
        move.w %d6,(%a5)
m68k_03def0_end:
.org 0x3DEF2
m68k_03def2:
        dbra %d7,(. + -2)
m68k_03def2_end:
.org 0x3DEF6
m68k_03def6:
        move.w #0xa000,0xff700c:l
m68k_03def6_end:
.org 0x3DEFE
m68k_03defe:
        move.l #0x3b388,0xff700e:l
m68k_03defe_end:
.org 0x3DF08
m68k_03df08:
        move.w #0x3,0xff7014:l
m68k_03df08_end:
.org 0x3DF10
m68k_03df10:
        move.w #0x1,0xff7016:l
m68k_03df10_end:
.org 0x3DF18
m68k_03df18:
        bsr.w (. + 3018)
m68k_03df18_end:
.org 0x3DF1C
m68k_03df1c:
        addq.w #0x1,0x813c:w
m68k_03df1c_end:
.org 0x3DF20
m68k_03df20:
        move.w #0x2500,%sr
m68k_03df20_end:
.org 0x3DF24
m68k_03df24:
        rts
m68k_03df24_end:
.org 0x3DFCE
m68k_03dfce:
        clr.w 0x8142:w
m68k_03dfce_end:
.org 0x3DFD2
m68k_03dfd2:
        move.l #0x40000003,0xc00004:l
m68k_03dfd2_end:
.org 0x3DFDC
m68k_03dfdc:
        lea.l 0xc00000:l,%a5
m68k_03dfdc_end:
.org 0x3DFE2
m68k_03dfe2:
        move.w #0x400,%d6
m68k_03dfe2_end:
.org 0x3DFE6
m68k_03dfe6:
        move.w #0x4bf,%d7
m68k_03dfe6_end:
.org 0x3DFEA
m68k_03dfea:
        move.w %d6,(%a5)
m68k_03dfea_end:
.org 0x3DFEC
m68k_03dfec:
        dbra %d7,(. + -2)
m68k_03dfec_end:
.org 0x3DFF0
m68k_03dff0:
        move.w 0x80e0:w,%d0
m68k_03dff0_end:
.org 0x3DFF4
m68k_03dff4:
        move.w #0x480,%d1
m68k_03dff4_end:
.org 0x3DFF8
m68k_03dff8:
        jsr 0x661d4:l
m68k_03dff8_end:
.org 0x3DFFE
m68k_03dffe:
        move.w #0xc322,%d0
m68k_03dffe_end:
.org 0x3E002
m68k_03e002:
        bsr.w (. + 1064)
m68k_03e002_end:
.org 0x3E006
m68k_03e006:
        move.w #0x8f02,0xc00004:l
m68k_03e006_end:
.org 0x3E00E
m68k_03e00e:
        move.l #0x60000002,0xc00004:l
m68k_03e00e_end:
.org 0x3E018
m68k_03e018:
        lea.l 0xc00000:l,%a5
m68k_03e018_end:
.org 0x3E01E
m68k_03e01e:
        move.w #0x3333,%d6
m68k_03e01e_end:
.org 0x3E022
m68k_03e022:
        move.w #0xd7f,%d7
m68k_03e022_end:
.org 0x3E026
m68k_03e026:
        move.w %d6,(%a5)
m68k_03e026_end:
.org 0x3E028
m68k_03e028:
        dbra %d7,(. + -2)
m68k_03e028_end:
.org 0x3E02C
m68k_03e02c:
        move.w #0xa000,0xff700c:l
m68k_03e02c_end:
.org 0x3E034
m68k_03e034:
        move.w #0x3,0xff7014:l
m68k_03e034_end:
.org 0x3E03C
m68k_03e03c:
        move.w #0x1,0xff7016:l
m68k_03e03c_end:
.org 0x3E044
m68k_03e044:
        addq.w #0x1,0x813c:w
m68k_03e044_end:
.org 0x3E048
m68k_03e048:
        move.l #0x3b3f8,0xff700e:l
m68k_03e048_end:
.org 0x3E052
m68k_03e052:
        lea.l 0xc700:w,%a0
m68k_03e052_end:
.org 0x3E056
m68k_03e056:
        move.w 0x80e2:w,%d0
m68k_03e056_end:
.org 0x3E05A
m68k_03e05a:
        move.b (%a0, %d0.w),%d1
m68k_03e05a_end:
.org 0x3E05E
m68k_03e05e:
        andi.w #0x3,%d1
m68k_03e05e_end:
.org 0x3E062
m68k_03e062:
        move.w 0x80e0:w,%d0
m68k_03e062_end:
.org 0x3E066
m68k_03e066:
        move.b (%a0, %d0.w),%d0
m68k_03e066_end:
.org 0x3E06A
m68k_03e06a:
        andi.w #0x3,%d0
m68k_03e06a_end:
.org 0x3E06E
m68k_03e06e:
        cmp.b %d0,%d1
m68k_03e06e_end:
.org 0x3E070
m68k_03e070:
        bcs.b (. + 12)
m68k_03e070_end:
.org 0x3E072
m68k_03e072:
        move.l #0x3b3aa,0xff700e:l
m68k_03e072_end:
.org 0x3E07C
m68k_03e07c:
        move.w #0x2500,%sr
m68k_03e07c_end:
.org 0x3E080
m68k_03e080:
        rts
m68k_03e080_end:
.org 0x3E086
m68k_03e086:
        move.w #0x1,0x8142:w
m68k_03e086_end:
.org 0x3E08C
m68k_03e08c:
        move.l #0x40000003,0xc00004:l
m68k_03e08c_end:
.org 0x3E096
m68k_03e096:
        lea.l 0xc00000:l,%a5
m68k_03e096_end:
.org 0x3E09C
m68k_03e09c:
        move.w #0x400,%d6
m68k_03e09c_end:
.org 0x3E0A0
m68k_03e0a0:
        move.w #0x4bf,%d7
m68k_03e0a0_end:
.org 0x3E0A4
m68k_03e0a4:
        move.w %d6,(%a5)
m68k_03e0a4_end:
.org 0x3E0A6
m68k_03e0a6:
        dbra %d7,(. + -2)
m68k_03e0a6_end:
.org 0x3E0AA
m68k_03e0aa:
        move.w 0x80e0:w,%d0
m68k_03e0aa_end:
.org 0x3E0AE
m68k_03e0ae:
        move.w #0x480,%d1
m68k_03e0ae_end:
.org 0x3E0B2
m68k_03e0b2:
        jsr 0x661d4:l
m68k_03e0b2_end:
.org 0x3E0B8
m68k_03e0b8:
        move.w #0x8f02,0xc00004:l
m68k_03e0b8_end:
.org 0x3E0C0
m68k_03e0c0:
        move.l #0x60000002,0xc00004:l
m68k_03e0c0_end:
.org 0x3E0CA
m68k_03e0ca:
        lea.l 0xc00000:l,%a5
m68k_03e0ca_end:
.org 0x3E0D0
m68k_03e0d0:
        move.w #0x3333,%d6
m68k_03e0d0_end:
.org 0x3E0D4
m68k_03e0d4:
        move.w #0xd7f,%d7
m68k_03e0d4_end:
.org 0x3E0D8
m68k_03e0d8:
        move.w %d6,(%a5)
m68k_03e0d8_end:
.org 0x3E0DA
m68k_03e0da:
        dbra %d7,(. + -2)
m68k_03e0da_end:
.org 0x3E0DE
m68k_03e0de:
        move.w #0xa000,0xff700c:l
m68k_03e0de_end:
.org 0x3E0E6
m68k_03e0e6:
        move.w #0x3,0xff7014:l
m68k_03e0e6_end:
.org 0x3E0EE
m68k_03e0ee:
        move.w #0x1,0xff7016:l
m68k_03e0ee_end:
.org 0x3E0F6
m68k_03e0f6:
        addq.w #0x1,0x813c:w
m68k_03e0f6_end:
.org 0x3E0FA
m68k_03e0fa:
        move.l #0x3b3bc,0xff700e:l
m68k_03e0fa_end:
.org 0x3E104
m68k_03e104:
        lea.l 0xc700:w,%a0
m68k_03e104_end:
.org 0x3E108
m68k_03e108:
        move.w 0x80e2:w,%d0
m68k_03e108_end:
.org 0x3E10C
m68k_03e10c:
        move.b (%a0, %d0.w),%d1
m68k_03e10c_end:
.org 0x3E110
m68k_03e110:
        andi.w #0x3,%d1
m68k_03e110_end:
.org 0x3E114
m68k_03e114:
        move.w 0x80e0:w,%d0
m68k_03e114_end:
.org 0x3E118
m68k_03e118:
        move.b (%a0, %d0.w),%d0
m68k_03e118_end:
.org 0x3E11C
m68k_03e11c:
        andi.w #0x3,%d1
m68k_03e11c_end:
.org 0x3E120
m68k_03e120:
        cmp.b %d0,%d1
m68k_03e120_end:
.org 0x3E122
m68k_03e122:
        bcs.b (. + 12)
m68k_03e122_end:
.org 0x3E124
m68k_03e124:
        move.l #0x3b3de,0xff700e:l
m68k_03e124_end:
.org 0x3E12E
m68k_03e12e:
        move.w #0x2500,%sr
m68k_03e12e_end:
.org 0x3E132
m68k_03e132:
        rts
m68k_03e132_end:
.org 0x3E134
m68k_03e134:
        move.w #0x2700,%sr
m68k_03e134_end:
.org 0x3E138
m68k_03e138:
        lea.l 0x4539c:l,%a0
m68k_03e138_end:
.org 0x3E13E
m68k_03e13e:
        lea.l 0xc000:l,%a1
m68k_03e13e_end:
.org 0x3E144
m68k_03e144:
        move.l #0x80,%d5
m68k_03e144_end:
.org 0x3E14A
m68k_03e14a:
        move.w #0x8000,0x8000:w
m68k_03e14a_end:
.org 0x3E150
m68k_03e150:
        move.w #0x12,%d6
m68k_03e150_end:
.org 0x3E154
m68k_03e154:
        jsr -13952(%pc)
m68k_03e154_end:
.org 0x3E158
m68k_03e158:
        move.w #0x0,0x8116:w
m68k_03e158_end:
.org 0x3E15E
m68k_03e15e:
        move.w #0x8f02,0xc00004:l
m68k_03e15e_end:
.org 0x3E166
m68k_03e166:
        move.l #0x60000002,0xc00004:l
m68k_03e166_end:
.org 0x3E170
m68k_03e170:
        lea.l 0xc00000:l,%a5
m68k_03e170_end:
.org 0x3E176
m68k_03e176:
        move.w #0x3333,%d6
m68k_03e176_end:
.org 0x3E17A
m68k_03e17a:
        move.w #0xd7f,%d7
m68k_03e17a_end:
.org 0x3E17E
m68k_03e17e:
        move.w %d6,(%a5)
m68k_03e17e_end:
.org 0x3E180
m68k_03e180:
        dbra %d7,(. + -2)
m68k_03e180_end:
.org 0x3E184
m68k_03e184:
        move.w #0xa000,0xff700c:l
m68k_03e184_end:
.org 0x3E18C
m68k_03e18c:
        move.l #0x3b43e,0xff700e:l
m68k_03e18c_end:
.org 0x3E196
m68k_03e196:
        move.w #0x3,0xff7014:l
m68k_03e196_end:
.org 0x3E19E
m68k_03e19e:
        move.w #0x1,0xff7016:l
m68k_03e19e_end:
.org 0x3E1A6
m68k_03e1a6:
        move.w #0x3,0x813c:w
m68k_03e1a6_end:
.org 0x3E1AC
m68k_03e1ac:
        bsr.w (. + 2358)
m68k_03e1ac_end:
.org 0x3E1B0
m68k_03e1b0:
        move.w #0x2500,%sr
m68k_03e1b0_end:
.org 0x3E1B4
m68k_03e1b4:
        rts
m68k_03e1b4_end:
.org 0x3E1B6
m68k_03e1b6:
        clr.w 0x813a:w
m68k_03e1b6_end:
.org 0x3E1BA
m68k_03e1ba:
        move.w #0x6,0x813c:w
m68k_03e1ba_end:
.org 0x3E1C0
m68k_03e1c0:
        clr.w 0x814c:w
m68k_03e1c0_end:
.org 0x3E1C4
m68k_03e1c4:
        bsr.w (. + 8536)
m68k_03e1c4_end:
.org 0x3E1C8
m68k_03e1c8:
        rts
m68k_03e1c8_end:
.org 0x3E254
m68k_03e254:
        move.b 0x811f:w,%d0
m68k_03e254_end:
.org 0x3E258
m68k_03e258:
        andi.w #0x3,%d0
m68k_03e258_end:
.org 0x3E25C
m68k_03e25c:
        beq.b (. + 8)
m68k_03e25c_end:
.org 0x3E25E
m68k_03e25e:
        eori.w #0x1,0x8142:w
m68k_03e25e_end:
.org 0x3E264
m68k_03e264:
        move.w #0x38,%d0
m68k_03e264_end:
.org 0x3E268
m68k_03e268:
        tst.w 0x8142:w
m68k_03e268_end:
.org 0x3E26C
m68k_03e26c:
        beq.b (. + 6)
m68k_03e26c_end:
.org 0x3E26E
m68k_03e26e:
        move.w #0x48,%d0
m68k_03e26e_end:
.org 0x3E272
m68k_03e272:
        add.w 0x8020:w,%d0
m68k_03e272_end:
.org 0x3E276
m68k_03e276:
        lea.l 22(%pc),%a0
m68k_03e276_end:
.org 0x3E27A
m68k_03e27a:
        nop
m68k_03e27a_end:
.org 0x3E27C
m68k_03e27c:
        move.w #0x8c,%d1
m68k_03e27c_end:
.org 0x3E280
m68k_03e280:
        move.w #0x104,%d2
m68k_03e280_end:
.org 0x3E284
m68k_03e284:
        moveq #0,%d3
m68k_03e284_end:
.org 0x3E286
m68k_03e286:
        move.w #0x400,%d4
m68k_03e286_end:
.org 0x3E28A
m68k_03e28a:
        jmp -12624(%pc)
m68k_03e28a_end:
.org 0x3E42A
m68k_03e42a:
        moveq #7,%d1
m68k_03e42a_end:
.org 0x3E42C
m68k_03e42c:
        bsr.w (. + 14)
m68k_03e42c_end:
.org 0x3E430
m68k_03e430:
        addi.w #0x80,%d0
m68k_03e430_end:
.org 0x3E434
m68k_03e434:
        dbra %d1,(. + -8)
m68k_03e434_end:
.org 0x3E438
m68k_03e438:
        rts
m68k_03e438_end:
.org 0x3E43A
m68k_03e43a:
        movem.l %d0-%d1,-(%a7)
m68k_03e43a_end:
.org 0x3E43E
m68k_03e43e:
        move.w #0x8f02,0xc00004:l
m68k_03e43e_end:
.org 0x3E446
m68k_03e446:
        bsr.w (. + -12694)
m68k_03e446_end:
.org 0x3E44A
m68k_03e44a:
        movem.l (%a7)+,%d0-%d1
m68k_03e44a_end:
.org 0x3E44E
m68k_03e44e:
        moveq #5,%d2
m68k_03e44e_end:
.org 0x3E450
m68k_03e450:
        move.w #0xe45d,0xc00000:l
m68k_03e450_end:
.org 0x3E458
m68k_03e458:
        dbra %d2,(. + -8)
m68k_03e458_end:
.org 0x3E45C
m68k_03e45c:
        rts
m68k_03e45c_end:
.org 0x3EAE2
m68k_03eae2:
        lea.l 0x44ef5:l,%a0
m68k_03eae2_end:
.org 0x3EAE8
m68k_03eae8:
        lea.l 0xc980:l,%a1
m68k_03eae8_end:
.org 0x3EAEE
m68k_03eaee:
        move.l #0x80,%d5
m68k_03eaee_end:
.org 0x3EAF4
m68k_03eaf4:
        move.w #0x8000,0x8000:w
m68k_03eaf4_end:
.org 0x3EAFA
m68k_03eafa:
        move.w #0xa,%d6
m68k_03eafa_end:
.org 0x3EAFE
m68k_03eafe:
        jsr -16426(%pc)
m68k_03eafe_end:
.org 0x3EB02
m68k_03eb02:
        lea.l 0x45098:l,%a0
m68k_03eb02_end:
.org 0x3EB08
m68k_03eb08:
        lea.l 0xc9c0:l,%a1
m68k_03eb08_end:
.org 0x3EB0E
m68k_03eb0e:
        move.l #0x80,%d5
m68k_03eb0e_end:
.org 0x3EB14
m68k_03eb14:
        move.w #0x8000,0x8000:w
m68k_03eb14_end:
.org 0x3EB1A
m68k_03eb1a:
        move.w #0xa,%d6
m68k_03eb1a_end:
.org 0x3EB1E
m68k_03eb1e:
        jsr -16458(%pc)
m68k_03eb1e_end:
.org 0x3EB22
m68k_03eb22:
        rts
m68k_03eb22_end:
.org 0x3F890
m68k_03f890:
        cmpi.b #0x3,0x80db:w
m68k_03f890_end:
.org 0x3F896
m68k_03f896:
        bne.b (. + 44)
m68k_03f896_end:
.org 0x3F898
m68k_03f898:
        btst.b #0x7,0x80c4:w
m68k_03f898_end:
.org 0x3F89E
m68k_03f89e:
        beq.b (. + 36)
m68k_03f89e_end:
.org 0x3F8A0
m68k_03f8a0:
        move.w 0xf320:w,%d0
m68k_03f8a0_end:
.org 0x3F8A4
m68k_03f8a4:
        lsr.w #0x3,%d0
m68k_03f8a4_end:
.org 0x3F8A6
m68k_03f8a6:
        andi.w #0x6,%d0
m68k_03f8a6_end:
.org 0x3F8AA
m68k_03f8aa:
        lea.l 24(%pc),%a0
m68k_03f8aa_end:
.org 0x3F8AE
m68k_03f8ae:
        nop
m68k_03f8ae_end:
.org 0x3F8B0
m68k_03f8b0:
        move.w (%a0, %d0.w),0xfb02:w
m68k_03f8b0_end:
.org 0x3F8B6
m68k_03f8b6:
        move.w 0x8(%a0, %d0.w),0xfb04:w
m68k_03f8b6_end:
.org 0x3F8BC
m68k_03f8bc:
        move.w 0x10(%a0, %d0.w),0xfb06:w
m68k_03f8bc_end:
.org 0x3F8C2
m68k_03f8c2:
        rts
m68k_03f8c2_end:
.org 0x3F8DC
m68k_03f8dc:
        bsr.w (. + 9772)
m68k_03f8dc_end:
.org 0x3F8E0
m68k_03f8e0:
        move.w %d1,0x8118:w
m68k_03f8e0_end:
.org 0x3F8E4
m68k_03f8e4:
        move.w %d2,0x811a:w
m68k_03f8e4_end:
.org 0x3F8E8
m68k_03f8e8:
        move.w 0x8178:w,0x810c:w
m68k_03f8e8_end:
.org 0x3F8EE
m68k_03f8ee:
        move.w 0x8278:w,0x810e:w
m68k_03f8ee_end:
.org 0x3F8F4
m68k_03f8f4:
        rts
m68k_03f8f4_end:
.org 0x4031C
m68k_04031c:
        move.l #0x40000003,0xc00004:l
m68k_04031c_end:
.org 0x40326
m68k_040326:
        lea.l 0xc00000:l,%a5
m68k_040326_end:
.org 0x4032C
m68k_04032c:
        move.w #0x400,%d6
m68k_04032c_end:
.org 0x40330
m68k_040330:
        move.w #0x7ff,%d7
m68k_040330_end:
.org 0x40334
m68k_040334:
        move.w %d6,(%a5)
m68k_040334_end:
.org 0x40336
m68k_040336:
        dbra %d7,(. + -2)
m68k_040336_end:
.org 0x4033A
m68k_04033a:
        rts
m68k_04033a_end:
.org 0x4033C
m68k_04033c:
        bsr.w (. + 206)
m68k_04033c_end:
.org 0x40340
m68k_040340:
        lea.l 0x836a:w,%a5
m68k_040340_end:
.org 0x40344
m68k_040344:
        tst.l (%a5)
m68k_040344_end:
.org 0x40346
m68k_040346:
        beq.b (. + 26)
m68k_040346_end:
.org 0x40348
m68k_040348:
        movea.l (%a5)+,%a6
m68k_040348_end:
.org 0x4034A
m68k_04034a:
        btst.b #0x7,(%a6)
m68k_04034a_end:
.org 0x4034E
m68k_04034e:
        beq.b (. + -10)
m68k_04034e_end:
.org 0x40350
m68k_040350:
        movem.l %a5,-(%a7)
m68k_040350_end:
.org 0x40354
m68k_040354:
        jsr 240(%pc)
m68k_040354_end:
.org 0x40358
m68k_040358:
        nop
m68k_040358_end:
.org 0x4035A
m68k_04035a:
        movem.l (%a7)+,%a5
m68k_04035a_end:
.org 0x4035E
m68k_04035e:
        bra.b (. + -26)
m68k_04035e_end:
.org 0x40360
m68k_040360:
        tst.w 0x814c:w
m68k_040360_end:
.org 0x40364
m68k_040364:
        beq.w (. + 164)
m68k_040364_end:
.org 0x40368
m68k_040368:
        cmpi.w #0x2,0x8152:w
m68k_040368_end:
.org 0x4036E
m68k_04036e:
        beq.w (. + 22)
m68k_04036e_end:
.org 0x40372
m68k_040372:
        tst.w 0x813e:w
m68k_040372_end:
.org 0x40376
m68k_040376:
        bne.w (. + 146)
m68k_040376_end:
.org 0x4037A
m68k_04037a:
        cmpi.w #0x1,0x8152:w
m68k_04037a_end:
.org 0x40380
m68k_040380:
        beq.w (. + 136)
m68k_040380_end:
.org 0x40384
m68k_040384:
        clr.w 0x8152:w
m68k_040384_end:
.org 0x40388
m68k_040388:
        subq.w #0x1,0x8154:w
m68k_040388_end:
.org 0x4038C
m68k_04038c:
        bpl.w (. + 124)
m68k_04038c_end:
.org 0x40390
m68k_040390:
        addq.w #0x1,0x8150:w
m68k_040390_end:
.org 0x40394
m68k_040394:
        cmpi.w #0x10,0x8150:w
m68k_040394_end:
.org 0x4039A
m68k_04039a:
        bcc.b (. + 56)
m68k_04039a_end:
.org 0x4039C
m68k_04039c:
        lea.l 0x816a:w,%a0
m68k_04039c_end:
.org 0x403A0
m68k_0403a0:
        cmpi.w #0x1,0x814c:w
m68k_0403a0_end:
.org 0x403A6
m68k_0403a6:
        beq.w (. + 8)
m68k_0403a6_end:
.org 0x403AA
m68k_0403aa:
        lea.l 0x826a:w,%a0
m68k_0403aa_end:
.org 0x403AE
m68k_0403ae:
        move.w 0x8150:w,%d0
m68k_0403ae_end:
.org 0x403B2
m68k_0403b2:
        asl.w #0x4,%d0
m68k_0403b2_end:
.org 0x403B4
m68k_0403b4:
        btst.b #0x7,(%a0, %d0.w)
m68k_0403b4_end:
.org 0x403BA
m68k_0403ba:
        beq.w (. + -42)
m68k_0403ba_end:
.org 0x403BE
m68k_0403be:
        move.w (%a0, %d0.w),%d0
m68k_0403be_end:
.org 0x403C2
m68k_0403c2:
        andi.w #0x7f,%d0
m68k_0403c2_end:
.org 0x403C6
m68k_0403c6:
        cmp.w 0x814e:w,%d0
m68k_0403c6_end:
.org 0x403CA
m68k_0403ca:
        bne.w (. + -58)
m68k_0403ca_end:
.org 0x403CE
m68k_0403ce:
        bra.w (. + 40)
m68k_0403ce_end:
.org 0x403D2
m68k_0403d2:
        clr.w 0x8150:w
m68k_0403d2_end:
.org 0x403D6
m68k_0403d6:
        addq.w #0x1,0x814e:w
m68k_0403d6_end:
.org 0x403DA
m68k_0403da:
        cmpi.w #0x4,0x814e:w
m68k_0403da_end:
.org 0x403E0
m68k_0403e0:
        bcs.b (. + 22)
m68k_0403e0_end:
.org 0x403E2
m68k_0403e2:
        clr.w 0x814e:w
m68k_0403e2_end:
.org 0x403E6
m68k_0403e6:
        addq.w #0x1,0x814c:w
m68k_0403e6_end:
.org 0x403EA
m68k_0403ea:
        cmpi.w #0x3,0x814c:w
m68k_0403ea_end:
.org 0x403F0
m68k_0403f0:
        bcs.b (. + 6)
m68k_0403f0_end:
.org 0x403F2
m68k_0403f2:
        clr.w 0x814c:w
m68k_0403f2_end:
.org 0x403F6
m68k_0403f6:
        clr.w 0x8154:w
m68k_0403f6_end:
.org 0x403FA
m68k_0403fa:
        cmpi.w #0x2,0x814e:w
m68k_0403fa_end:
.org 0x40400
m68k_040400:
        bcs.b (. + 8)
m68k_040400_end:
.org 0x40402
m68k_040402:
        move.w #0x1,0x8154:w
m68k_040402_end:
.org 0x40408
m68k_040408:
        rts
m68k_040408_end:
.org 0x4040A
m68k_04040a:
        move.w 0xf320:w,%d0
m68k_04040a_end:
.org 0x4040E
m68k_04040e:
        andi.w #0xf,%d0
m68k_04040e_end:
.org 0x40412
m68k_040412:
        bne.w (. + 50)
m68k_040412_end:
.org 0x40416
m68k_040416:
        lea.l 0x836a:w,%a5
m68k_040416_end:
.org 0x4041A
m68k_04041a:
        moveq #30,%d0
m68k_04041a_end:
.org 0x4041C
m68k_04041c:
        lea.l 0x816a:w,%a6
m68k_04041c_end:
.org 0x40420
m68k_040420:
        btst.b #0x7,(%a6)
m68k_040420_end:
.org 0x40424
m68k_040424:
        beq.b (. + 14)
m68k_040424_end:
.org 0x40426
m68k_040426:
        move.w 0x2(%a6),%d1
m68k_040426_end:
.org 0x4042A
m68k_04042a:
        lsr.w #0x4,%d1
m68k_04042a_end:
.org 0x4042C
m68k_04042c:
        cmp.w %d0,%d1
m68k_04042c_end:
.org 0x4042E
m68k_04042e:
        bne.b (. + 4)
m68k_04042e_end:
.org 0x40430
m68k_040430:
        move.l %a6,(%a5)+
m68k_040430_end:
.org 0x40432
m68k_040432:
        adda.w #0x10,%a6
m68k_040432_end:
.org 0x40436
m68k_040436:
        cmpa.l #0xffff836a,%a6
m68k_040436_end:
.org 0x4043C
m68k_04043c:
        bcs.b (. + -28)
m68k_04043c_end:
.org 0x4043E
m68k_04043e:
        dbra %d0,(. + -34)
m68k_04043e_end:
.org 0x40442
m68k_040442:
        clr.l (%a5)
m68k_040442_end:
.org 0x40444
m68k_040444:
        rts
m68k_040444_end:
.org 0x40446
m68k_040446:
        tst.w 0x813e:w
m68k_040446_end:
.org 0x4044A
m68k_04044a:
        bne.b (. + 8)
m68k_04044a_end:
.org 0x4044C
m68k_04044c:
        jsr 2118(%pc)
m68k_04044c_end:
.org 0x40450
m68k_040450:
        nop
m68k_040450_end:
.org 0x40452
m68k_040452:
        move.w (%a6),%d0
m68k_040452_end:
.org 0x40454
m68k_040454:
        andi.w #0xff,%d0
m68k_040454_end:
.org 0x40458
m68k_040458:
        moveq #0,%d1
m68k_040458_end:
.org 0x4045A
m68k_04045a:
        lea.l 112(%pc),%a0
m68k_04045a_end:
.org 0x4045E
m68k_04045e:
        nop
m68k_04045e_end:
.org 0x40460
m68k_040460:
        move.b (%a0, %d0.w),%d1
m68k_040460_end:
.org 0x40464
m68k_040464:
        cmpi.b #0x3,0x80db:w
m68k_040464_end:
.org 0x4046A
m68k_04046a:
        bne.b (. + 6)
m68k_04046a_end:
.org 0x4046C
m68k_04046c:
        move.b 0x4(%a0, %d0.w),%d1
m68k_04046c_end:
.org 0x40470
m68k_040470:
        tst.w 0x8124:w
m68k_040470_end:
.org 0x40474
m68k_040474:
        bne.b (. + 18)
m68k_040474_end:
.org 0x40476
m68k_040476:
        cmpa.l #0xffff826a,%a6
m68k_040476_end:
.org 0x4047C
m68k_04047c:
        bcs.b (. + 22)
m68k_04047c_end:
.org 0x4047E
m68k_04047e:
        addi.w #0x60,%d1
m68k_04047e_end:
.org 0x40482
m68k_040482:
        bra.w (. + 16)
m68k_040482_end:
.org 0x40486
m68k_040486:
        cmpa.l #0xffff826a,%a6
m68k_040486_end:
.org 0x4048C
m68k_04048c:
        bcc.b (. + 6)
m68k_04048c_end:
.org 0x4048E
m68k_04048e:
        addi.w #0x60,%d1
m68k_04048e_end:
.org 0x40492
m68k_040492:
        move.w 0x8(%a6),%d0
m68k_040492_end:
.org 0x40496
m68k_040496:
        asl.w #0x2,%d0
m68k_040496_end:
.org 0x40498
m68k_040498:
        add.w %d0,%d1
m68k_040498_end:
.org 0x4049A
m68k_04049a:
        move.w 0xf320:w,%d0
m68k_04049a_end:
.org 0x4049E
m68k_04049e:
        lsr.w #0x3,%d0
m68k_04049e_end:
.org 0x404A0
m68k_0404a0:
        andi.w #0x3,%d0
m68k_0404a0_end:
.org 0x404A4
m68k_0404a4:
        add.w %d1,%d0
m68k_0404a4_end:
.org 0x404A6
m68k_0404a6:
        move.w %d0,%d4
m68k_0404a6_end:
.org 0x404A8
m68k_0404a8:
        asl.w #0x2,%d0
m68k_0404a8_end:
.org 0x404AA
m68k_0404aa:
        movea.l 40(%pc, %d0.w),%a0
m68k_0404aa_end:
.org 0x404AE
m68k_0404ae:
        move.w 0x2(%a6),%d0
m68k_0404ae_end:
.org 0x404B2
m68k_0404b2:
        move.w 0x4(%a6),%d1
m68k_0404b2_end:
.org 0x404B6
m68k_0404b6:
        move.w #0x5,%d2
m68k_0404b6_end:
.org 0x404BA
m68k_0404ba:
        moveq #0,%d3
m68k_0404ba_end:
.org 0x404BC
m68k_0404bc:
        asl.w #0x1,%d4
m68k_0404bc_end:
.org 0x404BE
m68k_0404be:
        lea.l 788(%pc),%a1
m68k_0404be_end:
.org 0x404C2
m68k_0404c2:
        nop
m68k_0404c2_end:
.org 0x404C4
m68k_0404c4:
        move.w (%a1, %d4.w),%d4
m68k_0404c4_end:
.org 0x404C8
m68k_0404c8:
        jmp -21390(%pc)
m68k_0404c8_end:
.org 0x40C94
m68k_040c94:
        cmpa.l #0xffff826a,%a6
m68k_040c94_end:
.org 0x40C9A
m68k_040c9a:
        bcs.b (. + 18)
m68k_040c9a_end:
.org 0x40C9C
m68k_040c9c:
        lea.l 0x826a:w,%a5
m68k_040c9c_end:
.org 0x40CA0
m68k_040ca0:
        cmpi.w #0x2,0x814c:w
m68k_040ca0_end:
.org 0x40CA6
m68k_040ca6:
        bne.w (. + 212)
m68k_040ca6_end:
.org 0x40CAA
m68k_040caa:
        bra.b (. + 16)
m68k_040caa_end:
.org 0x40CAC
m68k_040cac:
        lea.l 0x816a:w,%a5
m68k_040cac_end:
.org 0x40CB0
m68k_040cb0:
        cmpi.w #0x1,0x814c:w
m68k_040cb0_end:
.org 0x40CB6
m68k_040cb6:
        bne.w (. + 196)
m68k_040cb6_end:
.org 0x40CBA
m68k_040cba:
        move.w (%a6),%d0
m68k_040cba_end:
.org 0x40CBC
m68k_040cbc:
        andi.w #0x7f,%d0
m68k_040cbc_end:
.org 0x40CC0
m68k_040cc0:
        cmp.w 0x814e:w,%d0
m68k_040cc0_end:
.org 0x40CC4
m68k_040cc4:
        bne.w (. + 182)
m68k_040cc4_end:
.org 0x40CC8
m68k_040cc8:
        moveq #0,%d0
m68k_040cc8_end:
.org 0x40CCA
m68k_040cca:
        move.w 0x8150:w,%d0
m68k_040cca_end:
.org 0x40CCE
m68k_040cce:
        asl.w #0x4,%d0
m68k_040cce_end:
.org 0x40CD0
m68k_040cd0:
        movea.w %d0,%a0
m68k_040cd0_end:
.org 0x40CD2
m68k_040cd2:
        adda.l %a5,%a0
m68k_040cd2_end:
.org 0x40CD4
m68k_040cd4:
        cmpa.l %a6,%a0
m68k_040cd4_end:
.org 0x40CD6
m68k_040cd6:
        bne.w (. + 164)
m68k_040cd6_end:
.org 0x40CDA
m68k_040cda:
        tst.w 0x8152:w
m68k_040cda_end:
.org 0x40CDE
m68k_040cde:
        bne.b (. + 102)
m68k_040cde_end:
.org 0x40CE0
m68k_040ce0:
        move.w #0x1,0x8152:w
m68k_040ce0_end:
.org 0x40CE6
m68k_040ce6:
        cmpi.w #0x200,0x2(%a6)
m68k_040ce6_end:
.org 0x40CEC
m68k_040cec:
        bcc.w (. + 138)
m68k_040cec_end:
.org 0x40CF0
m68k_040cf0:
        jsr -21968(%pc)
m68k_040cf0_end:
.org 0x40CF4
m68k_040cf4:
        andi.w #0x3,%d0
m68k_040cf4_end:
.org 0x40CF8
m68k_040cf8:
        beq.b (. + 6)
m68k_040cf8_end:
.org 0x40CFA
m68k_040cfa:
        bsr.w (. + 1234)
m68k_040cfa_end:
.org 0x40CFE
m68k_040cfe:
        bsr.w (. + 42)
m68k_040cfe_end:
.org 0x40D02
m68k_040d02:
        move.w %d0,0x815a:w
m68k_040d02_end:
.org 0x40D06
m68k_040d06:
        asl.w #0x2,%d0
m68k_040d06_end:
.org 0x40D08
m68k_040d08:
        jmp 2(%pc, %d0.w)
m68k_040d08_end:
.org 0x40D28
m68k_040d28:
        moveq #0,%d0
m68k_040d28_end:
.org 0x40D2A
m68k_040d2a:
        move.b 0x1(%a6),%d0
m68k_040d2a_end:
.org 0x40D2E
m68k_040d2e:
        cmpa.l #0xffff826a,%a6
m68k_040d2e_end:
.org 0x40D34
m68k_040d34:
        bcs.b (. + 4)
m68k_040d34_end:
.org 0x40D36
m68k_040d36:
        addq.w #0x4,%d0
m68k_040d36_end:
.org 0x40D38
m68k_040d38:
        asl.w #0x1,%d0
m68k_040d38_end:
.org 0x40D3A
m68k_040d3a:
        lea.l 0x812a:w,%a0
m68k_040d3a_end:
.org 0x40D3E
m68k_040d3e:
        move.w (%a0, %d0.w),%d0
m68k_040d3e_end:
.org 0x40D42
m68k_040d42:
        rts
m68k_040d42_end:
.org 0x40D44
m68k_040d44:
        move.w 0x815a:w,%d0
m68k_040d44_end:
.org 0x40D48
m68k_040d48:
        asl.w #0x2,%d0
m68k_040d48_end:
.org 0x40D4A
m68k_040d4a:
        jmp 2(%pc, %d0.w)
m68k_040d4a_end:
.org 0x40D76
m68k_040d76:
        clr.w 0x8152:w
m68k_040d76_end:
.org 0x40D7A
m68k_040d7a:
        rts
m68k_040d7a_end:
.org 0x4115C
m68k_04115c:
        move.l 0x2(%a6),%d3
m68k_04115c_end:
.org 0x41160
m68k_041160:
        bsr.w (. + 66)
m68k_041160_end:
.org 0x41164
m68k_041164:
        moveq #0,%d0
m68k_041164_end:
.org 0x41166
m68k_041166:
        lea.l 0x816a:w,%a5
m68k_041166_end:
.org 0x4116A
m68k_04116a:
        btst.b #0x7,(%a5)
m68k_04116a_end:
.org 0x4116E
m68k_04116e:
        beq.b (. + 34)
m68k_04116e_end:
.org 0x41170
m68k_041170:
        cmpa.l %a5,%a6
m68k_041170_end:
.org 0x41172
m68k_041172:
        beq.b (. + 30)
m68k_041172_end:
.org 0x41174
m68k_041174:
        move.w 0x2(%a5),%d1
m68k_041174_end:
.org 0x41178
m68k_041178:
        cmp.w 0x2(%a6),%d1
m68k_041178_end:
.org 0x4117C
m68k_04117c:
        bne.b (. + 20)
m68k_04117c_end:
.org 0x4117E
m68k_04117e:
        move.w 0x4(%a5),%d1
m68k_04117e_end:
.org 0x41182
m68k_041182:
        cmp.w 0x4(%a6),%d1
m68k_041182_end:
.org 0x41186
m68k_041186:
        bne.b (. + 10)
m68k_041186_end:
.org 0x41188
m68k_041188:
        moveq #1,%d0
m68k_041188_end:
.org 0x4118A
m68k_04118a:
        move.l %d3,0x2(%a6)
m68k_04118a_end:
.org 0x4118E
m68k_04118e:
        rts
m68k_04118e_end:
.org 0x41190
m68k_041190:
        adda.w #0x10,%a5
m68k_041190_end:
.org 0x41194
m68k_041194:
        cmpa.l #0xffff836a,%a5
m68k_041194_end:
.org 0x4119A
m68k_04119a:
        bcs.b (. + -48)
m68k_04119a_end:
.org 0x4119C
m68k_04119c:
        move.l %d3,0x2(%a6)
m68k_04119c_end:
.org 0x411A0
m68k_0411a0:
        rts
m68k_0411a0_end:
.org 0x411A2
m68k_0411a2:
        move.w %d0,%d2
m68k_0411a2_end:
.org 0x411A4
m68k_0411a4:
        bpl.w (. + 14)
m68k_0411a4_end:
.org 0x411A8
m68k_0411a8:
        andi.w #0x7f,%d0
m68k_0411a8_end:
.org 0x411AC
m68k_0411ac:
        sub.w %d0,0x2(%a6)
m68k_0411ac_end:
.org 0x411B0
m68k_0411b0:
        bra.b (. + 6)
m68k_0411b0_end:
.org 0x411B2
m68k_0411b2:
        add.w %d0,0x2(%a6)
m68k_0411b2_end:
.org 0x411B6
m68k_0411b6:
        move.w %d1,%d2
m68k_0411b6_end:
.org 0x411B8
m68k_0411b8:
        bpl.w (. + 14)
m68k_0411b8_end:
.org 0x411BC
m68k_0411bc:
        andi.w #0x7f,%d1
m68k_0411bc_end:
.org 0x411C0
m68k_0411c0:
        sub.w %d1,0x4(%a6)
m68k_0411c0_end:
.org 0x411C4
m68k_0411c4:
        bra.b (. + 6)
m68k_0411c4_end:
.org 0x411C6
m68k_0411c6:
        add.w %d1,0x4(%a6)
m68k_0411c6_end:
.org 0x411CA
m68k_0411ca:
        rts
m68k_0411ca_end:
.org 0x411CC
m68k_0411cc:
        moveq #0,%d0
m68k_0411cc_end:
.org 0x411CE
m68k_0411ce:
        move.b 0x1(%a6),%d0
m68k_0411ce_end:
.org 0x411D2
m68k_0411d2:
        cmpa.l #0xffff826a,%a6
m68k_0411d2_end:
.org 0x411D8
m68k_0411d8:
        bcs.w (. + 132)
m68k_0411d8_end:
.org 0x411DC
m68k_0411dc:
        addq.w #0x4,%d0
m68k_0411dc_end:
.org 0x411DE
m68k_0411de:
        asl.w #0x1,%d0
m68k_0411de_end:
.org 0x411E0
m68k_0411e0:
        lea.l 0x812a:w,%a0
m68k_0411e0_end:
.org 0x411E4
m68k_0411e4:
        cmpi.w #0x6,(%a0, %d0.w)
m68k_0411e4_end:
.org 0x411EA
m68k_0411ea:
        bne.w (. + 240)
m68k_0411ea_end:
.org 0x411EE
m68k_0411ee:
        move.w #0x0,0x8000:w
m68k_0411ee_end:
.org 0x411F4
m68k_0411f4:
        move.w #0x1,0x8158:w
m68k_0411f4_end:
.org 0x411FA
m68k_0411fa:
        move.w #0x10,%d0
m68k_0411fa_end:
.org 0x411FE
m68k_0411fe:
        move.w #0x0,%d1
m68k_0411fe_end:
.org 0x41202
m68k_041202:
        bsr.w (. + 760)
m68k_041202_end:
.org 0x41206
m68k_041206:
        tst.w %d0
m68k_041206_end:
.org 0x41208
m68k_041208:
        bne.w (. + 656)
m68k_041208_end:
.org 0x4120C
m68k_04120c:
        cmpi.b #0x1,0x1(%a6)
m68k_04120c_end:
.org 0x41212
m68k_041212:
        bne.w (. + 644)
m68k_041212_end:
.org 0x41216
m68k_041216:
        move.w #0x0,0x8000:w
m68k_041216_end:
.org 0x4121C
m68k_04121c:
        move.w #0x1,0x8158:w
m68k_04121c_end:
.org 0x41222
m68k_041222:
        move.w #0x20,%d0
m68k_041222_end:
.org 0x41226
m68k_041226:
        move.w #0x0,%d1
m68k_041226_end:
.org 0x4122A
m68k_04122a:
        bsr.w (. + 720)
m68k_04122a_end:
.org 0x4122E
m68k_04122e:
        tst.w %d0
m68k_04122e_end:
.org 0x41230
m68k_041230:
        bne.w (. + 564)
m68k_041230_end:
.org 0x41234
m68k_041234:
        move.w #0x30,%d0
m68k_041234_end:
.org 0x41238
m68k_041238:
        move.w #0x0,%d1
m68k_041238_end:
.org 0x4123C
m68k_04123c:
        bsr.w (. + 702)
m68k_04123c_end:
.org 0x41240
m68k_041240:
        tst.w %d0
m68k_041240_end:
.org 0x41242
m68k_041242:
        bne.w (. + 546)
m68k_041242_end:
.org 0x41246
m68k_041246:
        move.w #0x40,%d0
m68k_041246_end:
.org 0x4124A
m68k_04124a:
        move.w #0x0,%d1
m68k_04124a_end:
.org 0x4124E
m68k_04124e:
        bsr.w (. + 684)
m68k_04124e_end:
.org 0x41252
m68k_041252:
        tst.w %d0
m68k_041252_end:
.org 0x41254
m68k_041254:
        bne.w (. + 528)
m68k_041254_end:
.org 0x41258
m68k_041258:
        bra.w (. + 574)
m68k_041258_end:
.org 0x4125C
m68k_04125c:
        asl.w #0x1,%d0
m68k_04125c_end:
.org 0x4125E
m68k_04125e:
        lea.l 0x812a:w,%a0
m68k_04125e_end:
.org 0x41262
m68k_041262:
        cmpi.w #0x6,(%a0, %d0.w)
m68k_041262_end:
.org 0x41268
m68k_041268:
        bne.w (. + 114)
m68k_041268_end:
.org 0x4126C
m68k_04126c:
        move.w #0x1,0x8000:w
m68k_04126c_end:
.org 0x41272
m68k_041272:
        move.w #0x0,0x8158:w
m68k_041272_end:
.org 0x41278
m68k_041278:
        move.w #0x8010,%d0
m68k_041278_end:
.org 0x4127C
m68k_04127c:
        move.w #0x0,%d1
m68k_04127c_end:
.org 0x41280
m68k_041280:
        bsr.w (. + 634)
m68k_041280_end:
.org 0x41284
m68k_041284:
        tst.w %d0
m68k_041284_end:
.org 0x41286
m68k_041286:
        bne.w (. + 530)
m68k_041286_end:
.org 0x4128A
m68k_04128a:
        cmpi.b #0x1,0x1(%a6)
m68k_04128a_end:
.org 0x41290
m68k_041290:
        bne.w (. + 518)
m68k_041290_end:
.org 0x41294
m68k_041294:
        move.w #0x1,0x8000:w
m68k_041294_end:
.org 0x4129A
m68k_04129a:
        move.w #0x0,0x8158:w
m68k_04129a_end:
.org 0x412A0
m68k_0412a0:
        move.w #0x8020,%d0
m68k_0412a0_end:
.org 0x412A4
m68k_0412a4:
        move.w #0x0,%d1
m68k_0412a4_end:
.org 0x412A8
m68k_0412a8:
        bsr.w (. + 594)
m68k_0412a8_end:
.org 0x412AC
m68k_0412ac:
        tst.w %d0
m68k_0412ac_end:
.org 0x412AE
m68k_0412ae:
        bne.w (. + 438)
m68k_0412ae_end:
.org 0x412B2
m68k_0412b2:
        move.w #0x8030,%d0
m68k_0412b2_end:
.org 0x412B6
m68k_0412b6:
        move.w #0x0,%d1
m68k_0412b6_end:
.org 0x412BA
m68k_0412ba:
        bsr.w (. + 576)
m68k_0412ba_end:
.org 0x412BE
m68k_0412be:
        tst.w %d0
m68k_0412be_end:
.org 0x412C0
m68k_0412c0:
        bne.w (. + 420)
m68k_0412c0_end:
.org 0x412C4
m68k_0412c4:
        move.w #0x8040,%d0
m68k_0412c4_end:
.org 0x412C8
m68k_0412c8:
        move.w #0x0,%d1
m68k_0412c8_end:
.org 0x412CC
m68k_0412cc:
        bsr.w (. + 558)
m68k_0412cc_end:
.org 0x412D0
m68k_0412d0:
        tst.w %d0
m68k_0412d0_end:
.org 0x412D2
m68k_0412d2:
        bne.w (. + 402)
m68k_0412d2_end:
.org 0x412D6
m68k_0412d6:
        bra.w (. + 448)
m68k_0412d6_end:
.org 0x412DA
m68k_0412da:
        move.w #0x1,0x8000:w
m68k_0412da_end:
.org 0x412E0
m68k_0412e0:
        move.w #0x0,0x8158:w
m68k_0412e0_end:
.org 0x412E6
m68k_0412e6:
        move.w #0x8010,%d0
m68k_0412e6_end:
.org 0x412EA
m68k_0412ea:
        move.w #0x0,%d1
m68k_0412ea_end:
.org 0x412EE
m68k_0412ee:
        bsr.w (. + 524)
m68k_0412ee_end:
.org 0x412F2
m68k_0412f2:
        tst.w %d0
m68k_0412f2_end:
.org 0x412F4
m68k_0412f4:
        bne.w (. + 420)
m68k_0412f4_end:
.org 0x412F8
m68k_0412f8:
        move.w #0x0,0x8000:w
m68k_0412f8_end:
.org 0x412FE
m68k_0412fe:
        move.w #0x1,0x8158:w
m68k_0412fe_end:
.org 0x41304
m68k_041304:
        move.w #0x10,%d0
m68k_041304_end:
.org 0x41308
m68k_041308:
        move.w #0x0,%d1
m68k_041308_end:
.org 0x4130C
m68k_04130c:
        bsr.w (. + 494)
m68k_04130c_end:
.org 0x41310
m68k_041310:
        tst.w %d0
m68k_041310_end:
.org 0x41312
m68k_041312:
        bne.w (. + 390)
m68k_041312_end:
.org 0x41316
m68k_041316:
        move.w #0x2,0x8000:w
m68k_041316_end:
.org 0x4131C
m68k_04131c:
        move.w #0x3,0x8158:w
m68k_04131c_end:
.org 0x41322
m68k_041322:
        move.w #0x0,%d0
m68k_041322_end:
.org 0x41326
m68k_041326:
        move.w #0x10,%d1
m68k_041326_end:
.org 0x4132A
m68k_04132a:
        bsr.w (. + 464)
m68k_04132a_end:
.org 0x4132E
m68k_04132e:
        tst.w %d0
m68k_04132e_end:
.org 0x41330
m68k_041330:
        bne.w (. + 360)
m68k_041330_end:
.org 0x41334
m68k_041334:
        move.w #0x3,0x8000:w
m68k_041334_end:
.org 0x4133A
m68k_04133a:
        move.w #0x6,0x8158:w
m68k_04133a_end:
.org 0x41340
m68k_041340:
        move.w #0x0,%d0
m68k_041340_end:
.org 0x41344
m68k_041344:
        move.w #0x8010,%d1
m68k_041344_end:
.org 0x41348
m68k_041348:
        bsr.w (. + 434)
m68k_041348_end:
.org 0x4134C
m68k_04134c:
        tst.w %d0
m68k_04134c_end:
.org 0x4134E
m68k_04134e:
        bne.w (. + 330)
m68k_04134e_end:
.org 0x41352
m68k_041352:
        cmpi.b #0x1,0x1(%a6)
m68k_041352_end:
.org 0x41358
m68k_041358:
        bne.w (. + 318)
m68k_041358_end:
.org 0x4135C
m68k_04135c:
        move.w #0x1,0x8000:w
m68k_04135c_end:
.org 0x41362
m68k_041362:
        move.w #0x0,0x8158:w
m68k_041362_end:
.org 0x41368
m68k_041368:
        move.w #0x8020,%d0
m68k_041368_end:
.org 0x4136C
m68k_04136c:
        move.w #0x0,%d1
m68k_04136c_end:
.org 0x41370
m68k_041370:
        bsr.w (. + 394)
m68k_041370_end:
.org 0x41374
m68k_041374:
        tst.w %d0
m68k_041374_end:
.org 0x41376
m68k_041376:
        bne.w (. + 238)
m68k_041376_end:
.org 0x4137A
m68k_04137a:
        move.w #0x8030,%d0
m68k_04137a_end:
.org 0x4137E
m68k_04137e:
        move.w #0x0,%d1
m68k_04137e_end:
.org 0x41382
m68k_041382:
        bsr.w (. + 376)
m68k_041382_end:
.org 0x41386
m68k_041386:
        tst.w %d0
m68k_041386_end:
.org 0x41388
m68k_041388:
        bne.w (. + 220)
m68k_041388_end:
.org 0x4138C
m68k_04138c:
        move.w #0x8040,%d0
m68k_04138c_end:
.org 0x41390
m68k_041390:
        move.w #0x0,%d1
m68k_041390_end:
.org 0x41394
m68k_041394:
        bsr.w (. + 358)
m68k_041394_end:
.org 0x41398
m68k_041398:
        tst.w %d0
m68k_041398_end:
.org 0x4139A
m68k_04139a:
        bne.w (. + 202)
m68k_04139a_end:
.org 0x4139E
m68k_04139e:
        move.w #0x0,0x8000:w
m68k_04139e_end:
.org 0x413A4
m68k_0413a4:
        move.w #0x1,0x8158:w
m68k_0413a4_end:
.org 0x413AA
m68k_0413aa:
        move.w #0x20,%d0
m68k_0413aa_end:
.org 0x413AE
m68k_0413ae:
        move.w #0x0,%d1
m68k_0413ae_end:
.org 0x413B2
m68k_0413b2:
        bsr.w (. + 328)
m68k_0413b2_end:
.org 0x413B6
m68k_0413b6:
        tst.w %d0
m68k_0413b6_end:
.org 0x413B8
m68k_0413b8:
        bne.w (. + 172)
m68k_0413b8_end:
.org 0x413BC
m68k_0413bc:
        move.w #0x30,%d0
m68k_0413bc_end:
.org 0x413C0
m68k_0413c0:
        move.w #0x0,%d1
m68k_0413c0_end:
.org 0x413C4
m68k_0413c4:
        bsr.w (. + 310)
m68k_0413c4_end:
.org 0x413C8
m68k_0413c8:
        tst.w %d0
m68k_0413c8_end:
.org 0x413CA
m68k_0413ca:
        bne.w (. + 154)
m68k_0413ca_end:
.org 0x413CE
m68k_0413ce:
        move.w #0x40,%d0
m68k_0413ce_end:
.org 0x413D2
m68k_0413d2:
        move.w #0x0,%d1
m68k_0413d2_end:
.org 0x413D6
m68k_0413d6:
        bsr.w (. + 292)
m68k_0413d6_end:
.org 0x413DA
m68k_0413da:
        tst.w %d0
m68k_0413da_end:
.org 0x413DC
m68k_0413dc:
        bne.w (. + 136)
m68k_0413dc_end:
.org 0x413E0
m68k_0413e0:
        move.w #0x2,0x8000:w
m68k_0413e0_end:
.org 0x413E6
m68k_0413e6:
        move.w #0x3,0x8158:w
m68k_0413e6_end:
.org 0x413EC
m68k_0413ec:
        move.w #0x0,%d0
m68k_0413ec_end:
.org 0x413F0
m68k_0413f0:
        move.w #0x20,%d1
m68k_0413f0_end:
.org 0x413F4
m68k_0413f4:
        bsr.w (. + 262)
m68k_0413f4_end:
.org 0x413F8
m68k_0413f8:
        tst.w %d0
m68k_0413f8_end:
.org 0x413FA
m68k_0413fa:
        bne.w (. + 106)
m68k_0413fa_end:
.org 0x413FE
m68k_0413fe:
        move.w #0x0,%d0
m68k_0413fe_end:
.org 0x41402
m68k_041402:
        move.w #0x3,%d1
m68k_041402_end:
.org 0x41406
m68k_041406:
        bsr.w (. + 244)
m68k_041406_end:
.org 0x4140A
m68k_04140a:
        tst.w %d0
m68k_04140a_end:
.org 0x4140C
m68k_04140c:
        bne.w (. + 88)
m68k_04140c_end:
.org 0x41410
m68k_041410:
        move.w #0x0,%d0
m68k_041410_end:
.org 0x41414
m68k_041414:
        move.w #0x40,%d1
m68k_041414_end:
.org 0x41418
m68k_041418:
        bsr.w (. + 226)
m68k_041418_end:
.org 0x4141C
m68k_04141c:
        tst.w %d0
m68k_04141c_end:
.org 0x4141E
m68k_04141e:
        bne.w (. + 70)
m68k_04141e_end:
.org 0x41422
m68k_041422:
        move.w #0x3,0x8000:w
m68k_041422_end:
.org 0x41428
m68k_041428:
        move.w #0x6,0x8158:w
m68k_041428_end:
.org 0x4142E
m68k_04142e:
        move.w #0x0,%d0
m68k_04142e_end:
.org 0x41432
m68k_041432:
        move.w #0x8020,%d1
m68k_041432_end:
.org 0x41436
m68k_041436:
        bsr.w (. + 196)
m68k_041436_end:
.org 0x4143A
m68k_04143a:
        tst.w %d0
m68k_04143a_end:
.org 0x4143C
m68k_04143c:
        bne.w (. + 40)
m68k_04143c_end:
.org 0x41440
m68k_041440:
        move.w #0x0,%d0
m68k_041440_end:
.org 0x41444
m68k_041444:
        move.w #0x8030,%d1
m68k_041444_end:
.org 0x41448
m68k_041448:
        bsr.w (. + 178)
m68k_041448_end:
.org 0x4144C
m68k_04144c:
        tst.w %d0
m68k_04144c_end:
.org 0x4144E
m68k_04144e:
        bne.w (. + 22)
m68k_04144e_end:
.org 0x41452
m68k_041452:
        move.w #0x0,%d0
m68k_041452_end:
.org 0x41456
m68k_041456:
        move.w #0x8040,%d1
m68k_041456_end:
.org 0x4145A
m68k_04145a:
        bsr.w (. + 160)
m68k_04145a_end:
.org 0x4145E
m68k_04145e:
        tst.w %d0
m68k_04145e_end:
.org 0x41460
m68k_041460:
        beq.w (. + 54)
m68k_041460_end:
.org 0x41464
m68k_041464:
        move.l %a5,0x815c:w
m68k_041464_end:
.org 0x41468
m68k_041468:
        move.w #0x9,0x815a:w
m68k_041468_end:
.org 0x4146E
m68k_04146e:
        clr.w 0x8162:w
m68k_04146e_end:
.org 0x41472
m68k_041472:
        move.w 0x2(%a6),0x8164:w
m68k_041472_end:
.org 0x41478
m68k_041478:
        move.w 0x4(%a6),0x8166:w
m68k_041478_end:
.org 0x4147E
m68k_04147e:
        clr.w 0x8168:w
m68k_04147e_end:
.org 0x41482
m68k_041482:
        move.w 0x8000:w,0x8(%a6)
m68k_041482_end:
.org 0x41488
m68k_041488:
        movem.l (%a7)+,%d0
m68k_041488_end:
.org 0x4148C
m68k_04148c:
        move.w #0xa2,%d0
m68k_04148c_end:
.org 0x41490
m68k_041490:
        jsr 0x808a:l
m68k_041490_end:
.org 0x41496
m68k_041496:
        rts
m68k_041496_end:
.org 0x41498
m68k_041498:
        cmpa.l #0xffff816a,%a5
m68k_041498_end:
.org 0x4149E
m68k_04149e:
        beq.b (. + 10)
m68k_04149e_end:
.org 0x414A0
m68k_0414a0:
        cmpa.l #0xffff826a,%a5
m68k_0414a0_end:
.org 0x414A6
m68k_0414a6:
        bne.b (. + 50)
m68k_0414a6_end:
.org 0x414A8
m68k_0414a8:
        cmpi.w #0x3,0x814e:w
m68k_0414a8_end:
.org 0x414AE
m68k_0414ae:
        bne.b (. + 42)
m68k_0414ae_end:
.org 0x414B0
m68k_0414b0:
        movem.l (%a7)+,%d0
m68k_0414b0_end:
.org 0x414B4
m68k_0414b4:
        move.w 0x814c:w,%d0
m68k_0414b4_end:
.org 0x414B8
m68k_0414b8:
        subq.w #0x1,%d0
m68k_0414b8_end:
.org 0x414BA
m68k_0414ba:
        move.w %d0,0x8176:w
m68k_0414ba_end:
.org 0x414BE
m68k_0414be:
        move.w #0x3,0x813a:w
m68k_0414be_end:
.org 0x414C4
m68k_0414c4:
        move.w #0x0,0x813c:w
m68k_0414c4_end:
.org 0x414CA
m68k_0414ca:
        move.w #0x1,0x813e:w
m68k_0414ca_end:
.org 0x414D0
m68k_0414d0:
        move.w #0x2,0x8152:w
m68k_0414d0_end:
.org 0x414D6
m68k_0414d6:
        rts
m68k_0414d6_end:
.org 0x414D8
m68k_0414d8:
        move.l %a5,0x815c:w
m68k_0414d8_end:
.org 0x414DC
m68k_0414dc:
        move.w #0x8,0x815a:w
m68k_0414dc_end:
.org 0x414E2
m68k_0414e2:
        clr.w 0x8162:w
m68k_0414e2_end:
.org 0x414E6
m68k_0414e6:
        move.w 0x8000:w,0x8(%a6)
m68k_0414e6_end:
.org 0x414EC
m68k_0414ec:
        movem.l (%a7)+,%d0
m68k_0414ec_end:
.org 0x414F0
m68k_0414f0:
        move.w #0xa7,%d0
m68k_0414f0_end:
.org 0x414F4
m68k_0414f4:
        jmp 0x808a:l
m68k_0414f4_end:
.org 0x414FA
m68k_0414fa:
        bsr.w (. + -926)
m68k_0414fa_end:
.org 0x414FE
m68k_0414fe:
        tst.w %d0
m68k_0414fe_end:
.org 0x41500
m68k_041500:
        beq.w (. + 32)
m68k_041500_end:
.org 0x41504
m68k_041504:
        cmpa.l #0xffff826a,%a6
m68k_041504_end:
.org 0x4150A
m68k_04150a:
        bcs.b (. + 12)
m68k_04150a_end:
.org 0x4150C
m68k_04150c:
        cmpa.l #0xffff826a,%a5
m68k_04150c_end:
.org 0x41512
m68k_041512:
        bcc.b (. + 14)
m68k_041512_end:
.org 0x41514
m68k_041514:
        rts
m68k_041514_end:
.org 0x41516
m68k_041516:
        cmpa.l #0xffff826a,%a5
m68k_041516_end:
.org 0x4151C
m68k_04151c:
        bcs.b (. + 4)
m68k_04151c_end:
.org 0x4151E
m68k_04151e:
        rts
m68k_04151e_end:
.org 0x41520
m68k_041520:
        moveq #0,%d0
m68k_041520_end:
.org 0x41522
m68k_041522:
        rts
m68k_041522_end:
.org 0x4153C
m68k_04153c:
        movea.l 0x815c:w,%a5
m68k_04153c_end:
.org 0x41540
m68k_041540:
        bsr.w (. + 238)
m68k_041540_end:
.org 0x41544
m68k_041544:
        sub.w %d1,0xe(%a5)
m68k_041544_end:
.org 0x41548
m68k_041548:
        beq.b (. + 4)
m68k_041548_end:
.org 0x4154A
m68k_04154a:
        bpl.b (. + 84)
m68k_04154a_end:
.org 0x4154C
m68k_04154c:
        clr.w 0xe(%a5)
m68k_04154c_end:
.org 0x41550
m68k_041550:
        clr.w (%a5)
m68k_041550_end:
.org 0x41552
m68k_041552:
        cmpa.l #0xffff826a,%a5
m68k_041552_end:
.org 0x41558
m68k_041558:
        bcs.b (. + 22)
m68k_041558_end:
.org 0x4155A
m68k_04155a:
        tst.w 0x826a:w
m68k_04155a_end:
.org 0x4155E
m68k_04155e:
        bne.b (. + 64)
m68k_04155e_end:
.org 0x41560
m68k_041560:
        move.w #0x2,0x8114:w
m68k_041560_end:
.org 0x41566
m68k_041566:
        move.w #0x3,0x8116:w
m68k_041566_end:
.org 0x4156C
m68k_04156c:
        bra.b (. + 18)
m68k_04156c_end:
.org 0x4156E
m68k_04156e:
        tst.w 0x816a:w
m68k_04156e_end:
.org 0x41572
m68k_041572:
        bne.b (. + 44)
m68k_041572_end:
.org 0x41574
m68k_041574:
        move.w #0x3,0x8114:w
m68k_041574_end:
.org 0x4157A
m68k_04157a:
        clr.w 0x8116:w
m68k_04157a_end:
.org 0x4157E
m68k_04157e:
        move.w #0x4,0x813a:w
m68k_04157e_end:
.org 0x41584
m68k_041584:
        move.w #0x0,0x813c:w
m68k_041584_end:
.org 0x4158A
m68k_04158a:
        move.w #0x1,0x813e:w
m68k_04158a_end:
.org 0x41590
m68k_041590:
        move.w 0x814c:w,%d0
m68k_041590_end:
.org 0x41594
m68k_041594:
        subq.w #0x1,%d0
m68k_041594_end:
.org 0x41596
m68k_041596:
        eori.w #0x1,%d0
m68k_041596_end:
.org 0x4159A
m68k_04159a:
        move.w %d0,0x8176:w
m68k_04159a_end:
.org 0x4159E
m68k_04159e:
        bra.w (. + -2088)
m68k_04159e_end:
.org 0x416CE
m68k_0416ce:
        cmpi.b #0x3,0x1(%a5)
m68k_0416ce_end:
.org 0x416D4
m68k_0416d4:
        bne.b (. + 34)
m68k_0416d4_end:
.org 0x416D6
m68k_0416d6:
        move.w 0x8104:w,%d2
m68k_0416d6_end:
.org 0x416DA
m68k_0416da:
        cmpi.w #0x2,0x814c:w
m68k_0416da_end:
.org 0x416E0
m68k_0416e0:
        beq.b (. + 6)
m68k_0416e0_end:
.org 0x416E2
m68k_0416e2:
        move.w 0x8106:w,%d2
m68k_0416e2_end:
.org 0x416E6
m68k_0416e6:
        lsr.w #0x1,%d2
m68k_0416e6_end:
.org 0x416E8
m68k_0416e8:
        bne.b (. + 6)
m68k_0416e8_end:
.org 0x416EA
m68k_0416ea:
        move.w #0x1,%d2
m68k_0416ea_end:
.org 0x416EE
m68k_0416ee:
        andi.l #0xffff,%d1
m68k_0416ee_end:
.org 0x416F4
m68k_0416f4:
        divu.w %d2,%d1
m68k_0416f4_end:
.org 0x416F6
m68k_0416f6:
        rts
m68k_0416f6_end:
.org 0x418AC
m68k_0418ac:
        moveq #0,%d0
m68k_0418ac_end:
.org 0x418AE
m68k_0418ae:
        moveq #2,%d1
m68k_0418ae_end:
.org 0x418B0
m68k_0418b0:
        cmpi.w #0x64,0x8110:w
m68k_0418b0_end:
.org 0x418B6
m68k_0418b6:
        bls.w (. + 78)
m68k_0418b6_end:
.org 0x418BA
m68k_0418ba:
        moveq #1,%d0
m68k_0418ba_end:
.org 0x418BC
m68k_0418bc:
        moveq #3,%d1
m68k_0418bc_end:
.org 0x418BE
m68k_0418be:
        cmpi.w #0xc8,0x8110:w
m68k_0418be_end:
.org 0x418C4
m68k_0418c4:
        bls.w (. + 64)
m68k_0418c4_end:
.org 0x418C8
m68k_0418c8:
        moveq #3,%d0
m68k_0418c8_end:
.org 0x418CA
m68k_0418ca:
        moveq #4,%d1
m68k_0418ca_end:
.org 0x418CC
m68k_0418cc:
        cmpi.w #0x12c,0x8110:w
m68k_0418cc_end:
.org 0x418D2
m68k_0418d2:
        bls.w (. + 50)
m68k_0418d2_end:
.org 0x418D6
m68k_0418d6:
        moveq #5,%d0
m68k_0418d6_end:
.org 0x418D8
m68k_0418d8:
        moveq #5,%d1
m68k_0418d8_end:
.org 0x418DA
m68k_0418da:
        cmpi.w #0x190,0x8110:w
m68k_0418da_end:
.org 0x418E0
m68k_0418e0:
        bls.w (. + 36)
m68k_0418e0_end:
.org 0x418E4
m68k_0418e4:
        moveq #6,%d0
m68k_0418e4_end:
.org 0x418E6
m68k_0418e6:
        moveq #6,%d1
m68k_0418e6_end:
.org 0x418E8
m68k_0418e8:
        cmpi.w #0x1f4,0x8110:w
m68k_0418e8_end:
.org 0x418EE
m68k_0418ee:
        bls.w (. + 22)
m68k_0418ee_end:
.org 0x418F2
m68k_0418f2:
        moveq #7,%d0
m68k_0418f2_end:
.org 0x418F4
m68k_0418f4:
        moveq #7,%d1
m68k_0418f4_end:
.org 0x418F6
m68k_0418f6:
        cmpi.w #0x258,0x8110:w
m68k_0418f6_end:
.org 0x418FC
m68k_0418fc:
        bls.w (. + 8)
m68k_0418fc_end:
.org 0x41900
m68k_041900:
        moveq #8,%d0
m68k_041900_end:
.org 0x41902
m68k_041902:
        moveq #8,%d1
m68k_041902_end:
.org 0x41904
m68k_041904:
        clr.w 0x80f4:w
m68k_041904_end:
.org 0x41908
m68k_041908:
        clr.w 0x80f6:w
m68k_041908_end:
.org 0x4190C
m68k_04190c:
        clr.w 0x80f8:w
m68k_04190c_end:
.org 0x41910
m68k_041910:
        move.w 0x80e8:w,%d2
m68k_041910_end:
.org 0x41914
m68k_041914:
        sub.w %d0,%d2
m68k_041914_end:
.org 0x41916
m68k_041916:
        bpl.b (. + 10)
m68k_041916_end:
.org 0x41918
m68k_041918:
        move.w 0x80e8:w,0x80f4:w
m68k_041918_end:
.org 0x4191E
m68k_04191e:
        bra.b (. + 22)
m68k_04191e_end:
.org 0x41920
m68k_041920:
        move.w %d0,0x80f4:w
m68k_041920_end:
.org 0x41924
m68k_041924:
        move.w %d2,0x80f6:w
m68k_041924_end:
.org 0x41928
m68k_041928:
        sub.w %d1,%d2
m68k_041928_end:
.org 0x4192A
m68k_04192a:
        bmi.b (. + 10)
m68k_04192a_end:
.org 0x4192C
m68k_04192c:
        move.w %d1,0x80f6:w
m68k_04192c_end:
.org 0x41930
m68k_041930:
        move.w %d2,0x80f8:w
m68k_041930_end:
.org 0x41934
m68k_041934:
        cmpi.b #0x3,0x80db:w
m68k_041934_end:
.org 0x4193A
m68k_04193a:
        bne.b (. + 16)
m68k_04193a_end:
.org 0x4193C
m68k_04193c:
        clr.w 0x80f4:w
m68k_04193c_end:
.org 0x41940
m68k_041940:
        move.w 0x80e8:w,0x80f6:w
m68k_041940_end:
.org 0x41946
m68k_041946:
        clr.w 0x80f8:w
m68k_041946_end:
.org 0x4194A
m68k_04194a:
        jsr -25130(%pc)
m68k_04194a_end:
.org 0x4194E
m68k_04194e:
        andi.w #0x7,%d0
m68k_04194e_end:
.org 0x41952
m68k_041952:
        cmpi.w #0x4,%d0
m68k_041952_end:
.org 0x41956
m68k_041956:
        bhi.b (. + -34)
m68k_041956_end:
.org 0x41958
m68k_041958:
        move.w %d0,0x814a:w
m68k_041958_end:
.org 0x4195C
m68k_04195c:
        asl.w #0x2,%d0
m68k_04195c_end:
.org 0x4195E
m68k_04195e:
        lea.l 248(%pc),%a0
m68k_04195e_end:
.org 0x41962
m68k_041962:
        nop
m68k_041962_end:
.org 0x41964
m68k_041964:
        movea.l (%a0, %d0.w),%a5
m68k_041964_end:
.org 0x41968
m68k_041968:
        move.w 0x80f4:w,%d0
m68k_041968_end:
.org 0x4196C
m68k_04196c:
        move.w 0x80f6:w,%d1
m68k_04196c_end:
.org 0x41970
m68k_041970:
        move.w 0x80f8:w,%d2
m68k_041970_end:
.org 0x41974
m68k_041974:
        moveq #0,%d3
m68k_041974_end:
.org 0x41976
m68k_041976:
        lea.l 0x816a:w,%a6
m68k_041976_end:
.org 0x4197A
m68k_04197a:
        tst.w %d3
m68k_04197a_end:
.org 0x4197C
m68k_04197c:
        bne.b (. + 16)
m68k_04197c_end:
.org 0x4197E
m68k_04197e:
        move.w (%a5)+,0x2(%a6)
m68k_04197e_end:
.org 0x41982
m68k_041982:
        move.w (%a5)+,0x4(%a6)
m68k_041982_end:
.org 0x41986
m68k_041986:
        move.w #0x8003,(%a6)
m68k_041986_end:
.org 0x4198A
m68k_04198a:
        bra.b (. + 60)
m68k_04198a_end:
.org 0x4198C
m68k_04198c:
        tst.w %d0
m68k_04198c_end:
.org 0x4198E
m68k_04198e:
        beq.b (. + 18)
m68k_04198e_end:
.org 0x41990
m68k_041990:
        move.w (%a5)+,0x2(%a6)
m68k_041990_end:
.org 0x41994
m68k_041994:
        move.w (%a5)+,0x4(%a6)
m68k_041994_end:
.org 0x41998
m68k_041998:
        move.w #0x8002,(%a6)
m68k_041998_end:
.org 0x4199C
m68k_04199c:
        subq.w #0x1,%d0
m68k_04199c_end:
.org 0x4199E
m68k_04199e:
        bra.b (. + 40)
m68k_04199e_end:
.org 0x419A0
m68k_0419a0:
        tst.w %d1
m68k_0419a0_end:
.org 0x419A2
m68k_0419a2:
        beq.b (. + 18)
m68k_0419a2_end:
.org 0x419A4
m68k_0419a4:
        move.w (%a5)+,0x2(%a6)
m68k_0419a4_end:
.org 0x419A8
m68k_0419a8:
        move.w (%a5)+,0x4(%a6)
m68k_0419a8_end:
.org 0x419AC
m68k_0419ac:
        move.w #0x8001,(%a6)
m68k_0419ac_end:
.org 0x419B0
m68k_0419b0:
        subq.w #0x1,%d1
m68k_0419b0_end:
.org 0x419B2
m68k_0419b2:
        bra.b (. + 20)
m68k_0419b2_end:
.org 0x419B4
m68k_0419b4:
        tst.w %d2
m68k_0419b4_end:
.org 0x419B6
m68k_0419b6:
        beq.b (. + 26)
m68k_0419b6_end:
.org 0x419B8
m68k_0419b8:
        move.w (%a5)+,0x2(%a6)
m68k_0419b8_end:
.org 0x419BC
m68k_0419bc:
        move.w (%a5)+,0x4(%a6)
m68k_0419bc_end:
.org 0x419C0
m68k_0419c0:
        subq.w #0x1,%d2
m68k_0419c0_end:
.org 0x419C2
m68k_0419c2:
        move.w #0x8000,(%a6)
m68k_0419c2_end:
.org 0x419C6
m68k_0419c6:
        addq.w #0x1,%d3
m68k_0419c6_end:
.org 0x419C8
m68k_0419c8:
        adda.w #0x10,%a6
m68k_0419c8_end:
.org 0x419CC
m68k_0419cc:
        bra.w (. + -82)
m68k_0419cc_end:
.org 0x419D0
m68k_0419d0:
        move.w 0x8104:w,%d0
m68k_0419d0_end:
.org 0x419D4
m68k_0419d4:
        move.w 0x8100:w,%d1
m68k_0419d4_end:
.org 0x419D8
m68k_0419d8:
        mulu.w %d0,%d1
m68k_0419d8_end:
.org 0x419DA
m68k_0419da:
        divu.w #0x64,%d1
m68k_0419da_end:
.org 0x419DE
m68k_0419de:
        move.w #0xe,%d0
m68k_0419de_end:
.org 0x419E2
m68k_0419e2:
        move.w 0x80f0:w,%d2
m68k_0419e2_end:
.org 0x419E6
m68k_0419e6:
        lea.l 0x817a:w,%a6
m68k_0419e6_end:
.org 0x419EA
m68k_0419ea:
        move.w %d1,0xc(%a6)
m68k_0419ea_end:
.org 0x419EE
m68k_0419ee:
        move.w 0x80ec:w,0xe(%a6)
m68k_0419ee_end:
.org 0x419F4
m68k_0419f4:
        tst.w %d2
m68k_0419f4_end:
.org 0x419F6
m68k_0419f6:
        beq.w (. + 10)
m68k_0419f6_end:
.org 0x419FA
m68k_0419fa:
        subq.w #0x1,%d2
m68k_0419fa_end:
.org 0x419FC
m68k_0419fc:
        addq.w #0x1,0xe(%a6)
m68k_0419fc_end:
.org 0x41A00
m68k_041a00:
        adda.w #0x10,%a6
m68k_041a00_end:
.org 0x41A04
m68k_041a04:
        dbra %d0,(. + -26)
m68k_041a04_end:
.org 0x41A08
m68k_041a08:
        move.w 0x8104:w,%d0
m68k_041a08_end:
.org 0x41A0C
m68k_041a0c:
        add.w 0x8108:w,%d0
m68k_041a0c_end:
.org 0x41A10
m68k_041a10:
        move.w %d0,0x8176:w
m68k_041a10_end:
.org 0x41A14
m68k_041a14:
        move.w 0x810c:w,0x8178:w
m68k_041a14_end:
.org 0x41A1A
m68k_041a1a:
        clr.w 0x814c:w
m68k_041a1a_end:
.org 0x41A1E
m68k_041a1e:
        clr.w 0x814e:w
m68k_041a1e_end:
.org 0x41A22
m68k_041a22:
        clr.w 0x8150:w
m68k_041a22_end:
.org 0x41A26
m68k_041a26:
        clr.w 0x8152:w
m68k_041a26_end:
.org 0x41A2A
m68k_041a2a:
        clr.w 0x8154:w
m68k_041a2a_end:
.org 0x41A2E
m68k_041a2e:
        clr.w 0x8156:w
m68k_041a2e_end:
.org 0x41A32
m68k_041a32:
        clr.w 0x8158:w
m68k_041a32_end:
.org 0x41A36
m68k_041a36:
        clr.w 0x815a:w
m68k_041a36_end:
.org 0x41A3A
m68k_041a3a:
        clr.w 0x815c:w
m68k_041a3a_end:
.org 0x41A3E
m68k_041a3e:
        clr.w 0x815e:w
m68k_041a3e_end:
.org 0x41A42
m68k_041a42:
        clr.w 0x8160:w
m68k_041a42_end:
.org 0x41A46
m68k_041a46:
        clr.w 0x8162:w
m68k_041a46_end:
.org 0x41A4A
m68k_041a4a:
        clr.w 0x8164:w
m68k_041a4a_end:
.org 0x41A4E
m68k_041a4e:
        clr.w 0x8166:w
m68k_041a4e_end:
.org 0x41A52
m68k_041a52:
        clr.w 0x8168:w
m68k_041a52_end:
.org 0x41A56
m68k_041a56:
        rts
m68k_041a56_end:
.org 0x41F08
m68k_041f08:
        moveq #0,%d1
m68k_041f08_end:
.org 0x41F0A
m68k_041f0a:
        moveq #0,%d3
m68k_041f0a_end:
.org 0x41F0C
m68k_041f0c:
        move.w #0xe,%d0
m68k_041f0c_end:
.org 0x41F10
m68k_041f10:
        lea.l 0x817a:w,%a6
m68k_041f10_end:
.org 0x41F14
m68k_041f14:
        btst.b #0x7,(%a6)
m68k_041f14_end:
.org 0x41F18
m68k_041f18:
        beq.b (. + 8)
m68k_041f18_end:
.org 0x41F1A
m68k_041f1a:
        add.w 0xe(%a6),%d1
m68k_041f1a_end:
.org 0x41F1E
m68k_041f1e:
        addq.w #0x1,%d3
m68k_041f1e_end:
.org 0x41F20
m68k_041f20:
        adda.w #0x10,%a6
m68k_041f20_end:
.org 0x41F24
m68k_041f24:
        dbra %d0,(. + -16)
m68k_041f24_end:
.org 0x41F28
m68k_041f28:
        moveq #0,%d2
m68k_041f28_end:
.org 0x41F2A
m68k_041f2a:
        moveq #0,%d4
m68k_041f2a_end:
.org 0x41F2C
m68k_041f2c:
        move.w #0xe,%d0
m68k_041f2c_end:
.org 0x41F30
m68k_041f30:
        lea.l 0x827a:w,%a6
m68k_041f30_end:
.org 0x41F34
m68k_041f34:
        btst.b #0x7,(%a6)
m68k_041f34_end:
.org 0x41F38
m68k_041f38:
        beq.b (. + 8)
m68k_041f38_end:
.org 0x41F3A
m68k_041f3a:
        add.w 0xe(%a6),%d2
m68k_041f3a_end:
.org 0x41F3E
m68k_041f3e:
        addq.w #0x1,%d4
m68k_041f3e_end:
.org 0x41F40
m68k_041f40:
        adda.w #0x10,%a6
m68k_041f40_end:
.org 0x41F44
m68k_041f44:
        dbra %d0,(. + -16)
m68k_041f44_end:
.org 0x41F48
m68k_041f48:
        rts
m68k_041f48_end:
.org 0x661D4
m68k_0661d4:
        andi.l #0xffff,%d1
m68k_0661d4_end:
.org 0x661DA
m68k_0661da:
        lsl.l #0x7,%d1
m68k_0661da_end:
.org 0x661DC
m68k_0661dc:
        lsr.w #0x2,%d1
m68k_0661dc_end:
.org 0x661DE
m68k_0661de:
        ori.w #0x4000,%d1
m68k_0661de_end:
.org 0x661E2
m68k_0661e2:
        swap %d1
m68k_0661e2_end:
.org 0x661E4
m68k_0661e4:
        move.l %d1,0xc00004:l
m68k_0661e4_end:
.org 0x661EA
m68k_0661ea:
        move.w %d0,%d1
m68k_0661ea_end:
.org 0x661EC
m68k_0661ec:
        lsl.w #0x1,%d1
m68k_0661ec_end:
.org 0x661EE
m68k_0661ee:
        add.w %d0,%d1
m68k_0661ee_end:
.org 0x661F0
m68k_0661f0:
        lsl.w #0x5,%d1
m68k_0661f0_end:
.org 0x661F2
m68k_0661f2:
        lea.l 0xae39a:l,%a0
m68k_0661f2_end:
.org 0x661F8
m68k_0661f8:
        adda.w %d1,%a0
m68k_0661f8_end:
.org 0x661FA
m68k_0661fa:
        bsr.w (. + 186)
m68k_0661fa_end:
.org 0x661FE
m68k_0661fe:
        move.w %d0,%d1
m68k_0661fe_end:
.org 0x66200
m68k_066200:
        lsl.w #0x4,%d1
m68k_066200_end:
.org 0x66202
m68k_066202:
        lea.l 0xb439a:l,%a0
m68k_066202_end:
.org 0x66208
m68k_066208:
        adda.w %d1,%a0
m68k_066208_end:
.org 0x6620A
m68k_06620a:
        move.w #0x7,%d2
m68k_06620a_end:
.org 0x6620E
m68k_06620e:
        lea.l 0xb649a:l,%a1
m68k_06620e_end:
.org 0x66214
m68k_066214:
        move.w (%a0)+,%d3
m68k_066214_end:
.org 0x66216
m68k_066216:
        cmpi.w #0x800,%d3
m68k_066216_end:
.org 0x6621A
m68k_06621a:
        bcs.w (. + 10)
m68k_06621a_end:
.org 0x6621E
m68k_06621e:
        adda.l #0x10000,%a1
m68k_06621e_end:
.org 0x66224
m68k_066224:
        lsl.w #0x5,%d3
m68k_066224_end:
.org 0x66226
m68k_066226:
        move.w #0x7,%d4
m68k_066226_end:
.org 0x6622A
m68k_06622a:
        move.l (%a1, %d3.w),0xc00000:l
m68k_06622a_end:
.org 0x66232
m68k_066232:
        addq.w #0x4,%d3
m68k_066232_end:
.org 0x66234
m68k_066234:
        dbra %d4,(. + -10)
m68k_066234_end:
.org 0x66238
m68k_066238:
        dbra %d2,(. + -42)
m68k_066238_end:
.org 0x6623C
m68k_06623c:
        move.w %d0,%d1
m68k_06623c_end:
.org 0x6623E
m68k_06623e:
        lsl.w #0x3,%d1
m68k_06623e_end:
.org 0x66240
m68k_066240:
        lea.l 0xb539a:l,%a0
m68k_066240_end:
.org 0x66246
m68k_066246:
        adda.w %d1,%a0
m68k_066246_end:
.org 0x66248
m68k_066248:
        move.w #0x3,%d2
m68k_066248_end:
.org 0x6624C
m68k_06624c:
        lea.l 0xb649a:l,%a1
m68k_06624c_end:
.org 0x66252
m68k_066252:
        move.w (%a0)+,%d3
m68k_066252_end:
.org 0x66254
m68k_066254:
        cmpi.w #0x800,%d3
m68k_066254_end:
.org 0x66258
m68k_066258:
        bcs.w (. + 10)
m68k_066258_end:
.org 0x6625C
m68k_06625c:
        adda.l #0x10000,%a1
m68k_06625c_end:
.org 0x66262
m68k_066262:
        lsl.w #0x5,%d3
m68k_066262_end:
.org 0x66264
m68k_066264:
        move.w #0x7,%d4
m68k_066264_end:
.org 0x66268
m68k_066268:
        move.l (%a1, %d3.w),0xc00000:l
m68k_066268_end:
.org 0x66270
m68k_066270:
        addq.w #0x4,%d3
m68k_066270_end:
.org 0x66272
m68k_066272:
        dbra %d4,(. + -10)
m68k_066272_end:
.org 0x66276
m68k_066276:
        dbra %d2,(. + -42)
m68k_066276_end:
.org 0x6627A
m68k_06627a:
        lea.l 0xb599a:l,%a1
m68k_06627a_end:
.org 0x66280
m68k_066280:
        lea.l 0xb639a:l,%a2
m68k_066280_end:
.org 0x66286
m68k_066286:
        moveq #0,%d1
m68k_066286_end:
.org 0x66288
m68k_066288:
        move.b (%a2, %d0.w),%d1
m68k_066288_end:
.org 0x6628C
m68k_06628c:
        lsl.l #0x5,%d1
m68k_06628c_end:
.org 0x6628E
m68k_06628e:
        adda.l %d1,%a1
m68k_06628e_end:
.org 0x66290
m68k_066290:
        move.w #0x7,%d2
m68k_066290_end:
.org 0x66294
m68k_066294:
        lea.l 0xfb00:w,%a2
m68k_066294_end:
.org 0x66298
m68k_066298:
        cmpi.w #0x2,0xf6c4:w
m68k_066298_end:
.org 0x6629E
m68k_06629e:
        bne.w (. + 8)
m68k_06629e_end:
.org 0x662A2
m68k_0662a2:
        lea.l 0xfb20:w,%a2
m68k_0662a2_end:
.org 0x662A6
m68k_0662a6:
        move.l (%a1)+,(%a2)+
m68k_0662a6_end:
.org 0x662A8
m68k_0662a8:
        dbra %d2,(. + -2)
m68k_0662a8_end:
.org 0x662AC
m68k_0662ac:
        move.w #0x1,0xf31e:w
m68k_0662ac_end:
.org 0x662B2
m68k_0662b2:
        rts
m68k_0662b2_end:
.org 0x662B4
m68k_0662b4:
        move.w #0x2f,%d4
m68k_0662b4_end:
.org 0x662B8
m68k_0662b8:
        move.w (%a0)+,%d2
m68k_0662b8_end:
.org 0x662BA
m68k_0662ba:
        bsr.w (. + 10)
m68k_0662ba_end:
.org 0x662BE
m68k_0662be:
        dbra %d4,(. + -6)
m68k_0662be_end:
.org 0x662C2
m68k_0662c2:
        rts
m68k_0662c2_end:
.org 0x662C4
m68k_0662c4:
        lea.l 0xb649a:l,%a1
m68k_0662c4_end:
.org 0x662CA
m68k_0662ca:
        andi.l #0xffff,%d2
m68k_0662ca_end:
.org 0x662D0
m68k_0662d0:
        lsl.l #0x5,%d2
m68k_0662d0_end:
.org 0x662D2
m68k_0662d2:
        adda.l %d2,%a1
m68k_0662d2_end:
.org 0x662D4
m68k_0662d4:
        move.w #0x7,%d3
m68k_0662d4_end:
.org 0x662D8
m68k_0662d8:
        move.l (%a1)+,0xc00000:l
m68k_0662d8_end:
.org 0x662DE
m68k_0662de:
        dbra %d3,(. + -6)
m68k_0662de_end:
.org 0x662E2
m68k_0662e2:
        rts
m68k_0662e2_end:
.org 0x6634E
m68k_06634e:
        move.w %d0,0xf3d0:w
m68k_06634e_end:
.org 0x66352
m68k_066352:
        moveq #0,%d1
m68k_066352_end:
.org 0x66354
m68k_066354:
        move.b (%a2, %d0.w),%d1
m68k_066354_end:
.org 0x66358
m68k_066358:
        move.l %d1,0xf3c8:w
m68k_066358_end:
.org 0x6635C
m68k_06635c:
        ori.w #0x1,%sr
m68k_06635c_end:
.org 0x66360
m68k_066360:
        bra.w (. + 14)
m68k_066360_end:
.org 0x66398
m68k_066398:
        move.w #0xff,%d2
m68k_066398_end:
.org 0x663CA
m68k_0663ca:
        move.w #0xff,%d2
m68k_0663ca_end:
.org 0x66404
m68k_066404:
        move.w #0x96,%d2
m68k_066404_end:
.org 0x66472
m68k_066472:
        ori.w #0x1,%sr
m68k_066472_end:
.org 0x6701E
m68k_06701e:
        move.w #0x7ff,%d0
m68k_06701e_end:
.org 0x67022
m68k_067022:
        lea.l 0xff7000:l,%a0
m68k_067022_end:
.org 0x67028
m68k_067028:
        lea.l 0x8000:w,%a1
m68k_067028_end:
.org 0x6702C
m68k_06702c:
        clr.l (%a0)+
m68k_06702c_end:
.org 0x6702E
m68k_06702e:
        clr.l (%a1)+
m68k_06702e_end:
.org 0x67030
m68k_067030:
        dbra %d0,(. + -4)
m68k_067030_end:
.org 0x67034
m68k_067034:
        bsr.w (. + 132)
m68k_067034_end:
.org 0x67038
m68k_067038:
        move.w #0x9d,0xf740:w
m68k_067038_end:
.org 0x6703E
m68k_06703e:
        clr.w 0xf362:w
m68k_06703e_end:
.org 0x67042
m68k_067042:
        jsr 0x30a74:l
m68k_067042_end:
.org 0x67048
m68k_067048:
        bsr.w (. + 222)
m68k_067048_end:
.org 0x6704C
m68k_06704c:
        clr.w %d0
m68k_06704c_end:
.org 0x6704E
m68k_06704e:
        cmpi.w #0x50,%d1
m68k_06704e_end:
.org 0x67052
m68k_067052:
        bcc.w (. + 16)
m68k_067052_end:
.org 0x67056
m68k_067056:
        addq.w #0x1,%d0
m68k_067056_end:
.org 0x67058
m68k_067058:
        cmpi.w #0x28,%d1
m68k_067058_end:
.org 0x6705C
m68k_06705c:
        bcc.w (. + 6)
m68k_06705c_end:
.org 0x67060
m68k_067060:
        addq.w #0x1,%d0
m68k_067060_end:
.org 0x67062
m68k_067062:
        move.w %d0,0xffff80da:l
m68k_067062_end:
.org 0x67068
m68k_067068:
        move.w 0xf376:w,%d0
m68k_067068_end:
.org 0x6706C
m68k_06706c:
        lsl.w #0x1,%d0
m68k_06706c_end:
.org 0x6706E
m68k_06706e:
        lea.l 0xe640:w,%a0
m68k_06706e_end:
.org 0x67072
m68k_067072:
        move.w (%a0, %d0.w),%d1
m68k_067072_end:
.org 0x67076
m68k_067076:
        move.w %d1,0xffff80dc:l
m68k_067076_end:
.org 0x6707C
m68k_06707c:
        move.w %d1,0xffff80de:l
m68k_06707c_end:
.org 0x67082
m68k_067082:
        clr.w %d0
m68k_067082_end:
.org 0x67084
m68k_067084:
        move.b 0xf374:w,%d0
m68k_067084_end:
.org 0x67088
m68k_067088:
        addi.w #0xb8,%d0
m68k_067088_end:
.org 0x6708C
m68k_06708c:
        move.w %d0,0xffff80e4:l
m68k_06708c_end:
.org 0x67092
m68k_067092:
        move.b 0xf375:w,%d0
m68k_067092_end:
.org 0x67096
m68k_067096:
        addq.w #0x1,%d0
m68k_067096_end:
.org 0x67098
m68k_067098:
        move.w %d0,0xffff80e6:l
m68k_067098_end:
.org 0x6709E
m68k_06709e:
        move.w 0xefdc:w,0xffff80e8:l
m68k_06709e_end:
.org 0x670A6
m68k_0670a6:
        clr.w 0xf352:w
m68k_0670a6_end:
.org 0x670AA
m68k_0670aa:
        move.w #0x20c,0xf612:w
m68k_0670aa_end:
.org 0x670B0
m68k_0670b0:
        move.w #0x8,0xf362:w
m68k_0670b0_end:
.org 0x670B6
m68k_0670b6:
        rts
m68k_0670b6_end:
.org 0x670B8
m68k_0670b8:
        lea.l 0xcc00:w,%a0
m68k_0670b8_end:
.org 0x670BC
m68k_0670bc:
        lea.l 0xc700:w,%a1
m68k_0670bc_end:
.org 0x670C0
m68k_0670c0:
        lea.l 0xc300:w,%a2
m68k_0670c0_end:
.org 0x670C4
m68k_0670c4:
        lea.l 0xb400:w,%a3
m68k_0670c4_end:
.org 0x670C8
m68k_0670c8:
        lea.l 0xb600:w,%a4
m68k_0670c8_end:
.org 0x670CC
m68k_0670cc:
        clr.w %d0
m68k_0670cc_end:
.org 0x670CE
m68k_0670ce:
        clr.w %d1
m68k_0670ce_end:
.org 0x670D0
m68k_0670d0:
        move.w #0xff,%d2
m68k_0670d0_end:
.org 0x670D4
m68k_0670d4:
        move.b (%a0, %d2.w),%d3
m68k_0670d4_end:
.org 0x670D8
m68k_0670d8:
        beq.w (. + 62)
m68k_0670d8_end:
.org 0x670DC
m68k_0670dc:
        andi.w #0xc0,%d3
m68k_0670dc_end:
.org 0x670E0
m68k_0670e0:
        bne.w (. + 54)
m68k_0670e0_end:
.org 0x670E4
m68k_0670e4:
        move.b (%a1, %d2.w),%d3
m68k_0670e4_end:
.org 0x670E8
m68k_0670e8:
        andi.w #0x7,%d3
m68k_0670e8_end:
.org 0x670EC
m68k_0670ec:
        cmp.w %d0,%d3
m68k_0670ec_end:
.org 0x670EE
m68k_0670ee:
        bcs.w (. + 40)
m68k_0670ee_end:
.org 0x670F2
m68k_0670f2:
        beq.w (. + 6)
m68k_0670f2_end:
.org 0x670F6
m68k_0670f6:
        clr.w %d1
m68k_0670f6_end:
.org 0x670F8
m68k_0670f8:
        move.w %d3,%d0
m68k_0670f8_end:
.org 0x670FA
m68k_0670fa:
        clr.w %d3
m68k_0670fa_end:
.org 0x670FC
m68k_0670fc:
        move.b (%a2, %d2.w),%d3
m68k_0670fc_end:
.org 0x67100
m68k_067100:
        move.w %d2,%d4
m68k_067100_end:
.org 0x67102
m68k_067102:
        lsl.w #0x1,%d4
m68k_067102_end:
.org 0x67104
m68k_067104:
        add.w (%a3, %d4.w),%d3
m68k_067104_end:
.org 0x67108
m68k_067108:
        add.w (%a4, %d4.w),%d3
m68k_067108_end:
.org 0x6710C
m68k_06710c:
        cmp.w %d1,%d3
m68k_06710c_end:
.org 0x6710E
m68k_06710e:
        bls.w (. + 8)
m68k_06710e_end:
.org 0x67112
m68k_067112:
        move.w %d3,%d1
m68k_067112_end:
.org 0x67114
m68k_067114:
        move.w %d2,%d7
m68k_067114_end:
.org 0x67116
m68k_067116:
        dbra %d2,(. + -66)
m68k_067116_end:
.org 0x6711A
m68k_06711a:
        move.w %d7,0xf3a6:w
m68k_06711a_end:
.org 0x6711E
m68k_06711e:
        andi.w #0xff,0xf376:w
m68k_06711e_end:
.org 0x67124
m68k_067124:
        rts
m68k_067124_end:
.org 0x67126
m68k_067126:
        lea.l 0xe320:w,%a0
m68k_067126_end:
.org 0x6712A
m68k_06712a:
        move.w #0x27,%d0
m68k_06712a_end:
.org 0x6712E
m68k_06712e:
        moveq #0,%d1
m68k_06712e_end:
.org 0x67130
m68k_067130:
        add.l (%a0)+,%d1
m68k_067130_end:
.org 0x67132
m68k_067132:
        dbra %d0,(. + -2)
m68k_067132_end:
.org 0x67136
m68k_067136:
        divu.w #0x28,%d1
m68k_067136_end:
.org 0x6713A
m68k_06713a:
        lea.l 0xc300:w,%a0
m68k_06713a_end:
.org 0x6713E
m68k_06713e:
        lea.l 0xcc00:w,%a1
m68k_06713e_end:
.org 0x67142
m68k_067142:
        move.w #0xff,%d0
m68k_067142_end:
.org 0x67146
m68k_067146:
        moveq #0,%d2
m68k_067146_end:
.org 0x67148
m68k_067148:
        clr.w %d3
m68k_067148_end:
.org 0x6714A
m68k_06714a:
        clr.w %d4
m68k_06714a_end:
.org 0x6714C
m68k_06714c:
        move.b (%a1, %d0.w),%d4
m68k_06714c_end:
.org 0x67150
m68k_067150:
        beq.w (. + 20)
m68k_067150_end:
.org 0x67154
m68k_067154:
        andi.w #0xc0,%d4
m68k_067154_end:
.org 0x67158
m68k_067158:
        bne.w (. + 12)
m68k_067158_end:
.org 0x6715C
m68k_06715c:
        move.b (%a0, %d0.w),%d4
m68k_06715c_end:
.org 0x67160
m68k_067160:
        add.w %d4,%d2
m68k_067160_end:
.org 0x67162
m68k_067162:
        addq.w #0x1,%d3
m68k_067162_end:
.org 0x67164
m68k_067164:
        dbra %d0,(. + -24)
m68k_067164_end:
.org 0x67168
m68k_067168:
        lea.l 0x9000:w,%a1
m68k_067168_end:
.org 0x6716C
m68k_06716c:
        move.b (%a1),%d4
m68k_06716c_end:
.org 0x6716E
m68k_06716e:
        andi.w #0xf,%d4
m68k_06716e_end:
.org 0x67172
m68k_067172:
        beq.w (. + 46)
m68k_067172_end:
.org 0x67176
m68k_067176:
        move.b 0x4(%a1),%d5
m68k_067176_end:
.org 0x6717A
m68k_06717a:
        cmp.b 0xf377:w,%d5
m68k_06717a_end:
.org 0x6717E
m68k_06717e:
        bne.w (. + 22)
m68k_06717e_end:
.org 0x67182
m68k_067182:
        subq.w #0x1,%d4
m68k_067182_end:
.org 0x67184
m68k_067184:
        move.b 0xd(%a0, %d4.w),%d5
m68k_067184_end:
.org 0x67188
m68k_067188:
        move.b (%a1, %d5.w),%d5
m68k_067188_end:
.org 0x6718C
m68k_06718c:
        add.w %d5,%d2
m68k_06718c_end:
.org 0x6718E
m68k_06718e:
        addq.w #0x1,%d3
m68k_06718e_end:
.org 0x67190
m68k_067190:
        dbra %d4,(. + -12)
m68k_067190_end:
.org 0x67194
m68k_067194:
        move.b (%a1),%d4
m68k_067194_end:
.org 0x67196
m68k_067196:
        andi.w #0xf,%d4
m68k_067196_end:
.org 0x6719A
m68k_06719a:
        lea.l 0xd(%a1, %d4.w),%a1
m68k_06719a_end:
.org 0x6719E
m68k_06719e:
        bra.b (. + -50)
m68k_06719e_end:
.org 0x671A0
m68k_0671a0:
        divu.w %d3,%d2
m68k_0671a0_end:
.org 0x671A2
m68k_0671a2:
        add.w %d2,%d1
m68k_0671a2_end:
.org 0x671A4
m68k_0671a4:
        mulu.w %d3,%d1
m68k_0671a4_end:
.org 0x671A6
m68k_0671a6:
        divu.w #0x118,%d1
m68k_0671a6_end:
.org 0x671AA
m68k_0671aa:
        move.w %d1,0xefdc:w
m68k_0671aa_end:
.org 0x671AE
m68k_0671ae:
        rts
m68k_0671ae_end:
.org 0x671FC
m68k_0671fc:
        eori.w #0x1,0xf37a:w
m68k_0671fc_end:
.org 0x67202
m68k_067202:
        clr.w 0xf37c:w
m68k_067202_end:
.org 0x67206
m68k_067206:
        bra.w (. + 48)
m68k_067206_end:
.org 0x6720A
m68k_06720a:
        lea.l 0xd100:w,%a0
m68k_06720a_end:
.org 0x6720E
m68k_06720e:
        adda.w 0xf31a:w,%a0
m68k_06720e_end:
.org 0x67212
m68k_067212:
        bsr.w (. + 322)
m68k_067212_end:
.org 0x67216
m68k_067216:
        lea.l 658(%pc),%a2
m68k_067216_end:
.org 0x6721A
m68k_06721a:
        nop
m68k_06721a_end:
.org 0x6721C
m68k_06721c:
        bsr.w (. + 394)
m68k_06721c_end:
.org 0x67220
m68k_067220:
        addi.w #0x12,0xf37c:w
m68k_067220_end:
.org 0x67226
m68k_067226:
        bra.w (. + 16)
m68k_067226_end:
.org 0x67556
m68k_067556:
        move.w #0xd,0x1e(%a0)
m68k_067556_end:
.org 0x6755C
m68k_06755c:
        move.w #0xd,(%a0)+
m68k_06755c_end:
.org 0x67560
m68k_067560:
        move.w #0x934,%d3
m68k_067560_end:
.org 0x67564
m68k_067564:
        or.w %d2,%d3
m68k_067564_end:
.org 0x67566
m68k_067566:
        move.w %d3,0x1e(%a0)
m68k_067566_end:
.org 0x6756A
m68k_06756a:
        move.w #0x9b4,%d3
m68k_06756a_end:
.org 0x6756E
m68k_06756e:
        or.w %d2,%d3
m68k_06756e_end:
.org 0x67570
m68k_067570:
        move.w %d3,(%a0)+
m68k_067570_end:
.org 0x67572
m68k_067572:
        move.w #0x1380,%d3
m68k_067572_end:
.org 0x67576
m68k_067576:
        or.w %d2,%d3
m68k_067576_end:
.org 0x67578
m68k_067578:
        move.w %d3,0x1e(%a0)
m68k_067578_end:
.org 0x6757C
m68k_06757c:
        move.w #0x8000,(%a0)+
m68k_06757c_end:
.org 0x67580
m68k_067580:
        move.w #0xa,%d0
m68k_067580_end:
.org 0x67584
m68k_067584:
        move.w #0x1381,%d3
m68k_067584_end:
.org 0x67588
m68k_067588:
        or.w %d2,%d3
m68k_067588_end:
.org 0x6758A
m68k_06758a:
        move.w %d3,0x1e(%a0)
m68k_06758a_end:
.org 0x6758E
m68k_06758e:
        move.w #0x8000,(%a0)+
m68k_06758e_end:
.org 0x67592
m68k_067592:
        dbra %d0,(. + -14)
m68k_067592_end:
.org 0x67596
m68k_067596:
        move.w #0x1b80,%d3
m68k_067596_end:
.org 0x6759A
m68k_06759a:
        or.w %d2,%d3
m68k_06759a_end:
.org 0x6759C
m68k_06759c:
        move.w %d3,0x1e(%a0)
m68k_06759c_end:
.org 0x675A0
m68k_0675a0:
        move.w #0x8000,(%a0)+
m68k_0675a0_end:
.org 0x675A4
m68k_0675a4:
        addi.w #0x3c,0xf31a:w
m68k_0675a4_end:
.org 0x675AA
m68k_0675aa:
        clr.w 0x1e(%a0)
m68k_0675aa_end:
.org 0x67A06
m68k_067a06:
        cmpi.w #0x10,0xf352:w
m68k_067a06_end:
.org 0x67A0C
m68k_067a0c:
        bls.w (. + 258)
m68k_067a0c_end:
.org 0x67A70
m68k_067a70:
        move.w #0x0,0xfb50:w
m68k_067a70_end:
.org 0x67A76
m68k_067a76:
        move.w #0xe40,0xfb52:w
m68k_067a76_end:
.org 0x67A7C
m68k_067a7c:
        move.w #0xaee,0xfb54:w
m68k_067a7c_end:
.org 0x67A82
m68k_067a82:
        move.w #0xa0e,0xfb56:w
m68k_067a82_end:
.org 0x67A88
m68k_067a88:
        move.w #0x2e0,0xfb58:w
m68k_067a88_end:
.org 0x67A8E
m68k_067a8e:
        move.w #0xce,0xfb5a:w
m68k_067a8e_end:
.org 0x67A94
m68k_067a94:
        move.w #0xea0,0xfb5c:w
m68k_067a94_end:
.org 0x67A9A
m68k_067a9a:
        move.w #0x0,0xfb5e:w
m68k_067a9a_end:
