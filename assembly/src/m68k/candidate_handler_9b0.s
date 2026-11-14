| 候选处理入口 01A9B0。地址布局给出本文件负责的指令范围。
.cpu 68000
.section .text
_start:
.org 0x1A9B0
m68k_01a9b0:
        bsr.w (. + -444)
m68k_01a9b0_end:
.org 0x1A9B4
m68k_01a9b4:
        bsr.w (. + 536)
m68k_01a9b4_end:
.org 0x1A9B8
m68k_01a9b8:
        bsr.w (. + -534)
m68k_01a9b8_end:
.org 0x1A9BC
m68k_01a9bc:
        tst.w %d7
m68k_01a9bc_end:
.org 0x1A9BE
m68k_01a9be:
        beq.w (. + 276)
m68k_01a9be_end:
.org 0x1A9C2
m68k_01a9c2:
        andi.l #0xffff,%d7
m68k_01a9c2_end:
.org 0x1A9C8
m68k_01a9c8:
        divu.w #0x64,%d7
m68k_01a9c8_end:
.org 0x1A9CC
m68k_01a9cc:
        bsr.w (. + 568)
m68k_01a9cc_end:
.org 0x1A9D0
m68k_01a9d0:
        jsr 0x83d4:l
m68k_01a9d0_end:
.org 0x1A9D6
m68k_01a9d6:
        moveq #0,%d0
m68k_01a9d6_end:
.org 0x1A9D8
m68k_01a9d8:
        move.w 0xf61c:w,%d0
m68k_01a9d8_end:
.org 0x1A9DC
m68k_01a9dc:
        move.l %d0,%d1
m68k_01a9dc_end:
.org 0x1A9DE
m68k_01a9de:
        lsl.l #0x1,%d0
m68k_01a9de_end:
.org 0x1A9E0
m68k_01a9e0:
        add.l %d1,%d0
m68k_01a9e0_end:
.org 0x1A9E2
m68k_01a9e2:
        lsl.l #0x1,%d0
m68k_01a9e2_end:
.org 0x1A9E4
m68k_01a9e4:
        swap %d0
m68k_01a9e4_end:
.org 0x1A9E6
m68k_01a9e6:
        addi.w #0x5,%d0
m68k_01a9e6_end:
.org 0x1A9EA
m68k_01a9ea:
        lea.l 0xc500:w,%a0
m68k_01a9ea_end:
.org 0x1A9EE
m68k_01a9ee:
        move.w 0xf3f2:w,%d1
m68k_01a9ee_end:
.org 0x1A9F2
m68k_01a9f2:
        move.b (%a0, %d1.w),%d2
m68k_01a9f2_end:
.org 0x1A9F6
m68k_01a9f6:
        add.b %d0,%d2
m68k_01a9f6_end:
.org 0x1A9F8
m68k_01a9f8:
        cmpi.w #0x63,%d2
m68k_01a9f8_end:
.org 0x1A9FC
m68k_01a9fc:
        bls.w (. + 8)
m68k_01a9fc_end:
.org 0x1AA00
m68k_01aa00:
        move.b #0x63,%d2
m68k_01aa00_end:
.org 0x1AA04
m68k_01aa04:
        move.b %d2,(%a0, %d1.w)
m68k_01aa04_end:
.org 0x1AA08
m68k_01aa08:
        jsr 0x83d4:l
m68k_01aa08_end:
.org 0x1AA0E
m68k_01aa0e:
        moveq #0,%d0
m68k_01aa0e_end:
.org 0x1AA10
m68k_01aa10:
        move.w 0xf61c:w,%d0
m68k_01aa10_end:
.org 0x1AA14
m68k_01aa14:
        move.l %d0,%d1
m68k_01aa14_end:
.org 0x1AA16
m68k_01aa16:
        lsl.l #0x1,%d0
m68k_01aa16_end:
.org 0x1AA18
m68k_01aa18:
        add.l %d1,%d0
m68k_01aa18_end:
.org 0x1AA1A
m68k_01aa1a:
        lsl.l #0x1,%d0
m68k_01aa1a_end:
.org 0x1AA1C
m68k_01aa1c:
        swap %d0
m68k_01aa1c_end:
.org 0x1AA1E
m68k_01aa1e:
        addi.w #0x5,%d0
m68k_01aa1e_end:
.org 0x1AA22
m68k_01aa22:
        move.w 0xf3a6:w,%d1
m68k_01aa22_end:
.org 0x1AA26
m68k_01aa26:
        move.b (%a0, %d1.w),%d2
m68k_01aa26_end:
.org 0x1AA2A
m68k_01aa2a:
        add.w %d0,%d2
m68k_01aa2a_end:
.org 0x1AA2C
m68k_01aa2c:
        cmpi.b #0x63,%d2
m68k_01aa2c_end:
.org 0x1AA30
m68k_01aa30:
        bls.w (. + 8)
m68k_01aa30_end:
.org 0x1AA34
m68k_01aa34:
        move.b #0x63,%d2
m68k_01aa34_end:
.org 0x1AA38
m68k_01aa38:
        move.b %d2,(%a0, %d1.w)
m68k_01aa38_end:
.org 0x1AA3C
m68k_01aa3c:
        lea.l 0xbe00:w,%a0
m68k_01aa3c_end:
.org 0x1AA40
m68k_01aa40:
        lea.l 0xc000:w,%a1
m68k_01aa40_end:
.org 0x1AA44
m68k_01aa44:
        move.w %d7,%d0
m68k_01aa44_end:
.org 0x1AA46
m68k_01aa46:
        lsl.w #0x1,%d0
m68k_01aa46_end:
.org 0x1AA48
m68k_01aa48:
        add.w %d7,%d0
m68k_01aa48_end:
.org 0x1AA4A
m68k_01aa4a:
        move.w 0xf3f2:w,%d1
m68k_01aa4a_end:
.org 0x1AA4E
m68k_01aa4e:
        lsl.w #0x1,%d1
m68k_01aa4e_end:
.org 0x1AA50
m68k_01aa50:
        move.w (%a0, %d1.w),%d2
m68k_01aa50_end:
.org 0x1AA54
m68k_01aa54:
        add.w %d0,%d2
m68k_01aa54_end:
.org 0x1AA56
m68k_01aa56:
        cmpi.w #0x3e7,%d2
m68k_01aa56_end:
.org 0x1AA5A
m68k_01aa5a:
        bls.w (. + 8)
m68k_01aa5a_end:
.org 0x1AA5E
m68k_01aa5e:
        move.w #0x3e7,%d2
m68k_01aa5e_end:
.org 0x1AA62
m68k_01aa62:
        move.w %d2,(%a0, %d1.w)
m68k_01aa62_end:
.org 0x1AA66
m68k_01aa66:
        move.w %d0,%d2
m68k_01aa66_end:
.org 0x1AA68
m68k_01aa68:
        lsl.w #0x1,%d0
m68k_01aa68_end:
.org 0x1AA6A
m68k_01aa6a:
        add.w %d2,%d0
m68k_01aa6a_end:
.org 0x1AA6C
m68k_01aa6c:
        andi.l #0xffff,%d0
m68k_01aa6c_end:
.org 0x1AA72
m68k_01aa72:
        divu.w #0xa,%d0
m68k_01aa72_end:
.org 0x1AA76
m68k_01aa76:
        move.w (%a1, %d1.w),%d2
m68k_01aa76_end:
.org 0x1AA7A
m68k_01aa7a:
        add.w %d0,%d2
m68k_01aa7a_end:
.org 0x1AA7C
m68k_01aa7c:
        cmpi.w #0x3e7,%d2
m68k_01aa7c_end:
.org 0x1AA80
m68k_01aa80:
        bls.w (. + 8)
m68k_01aa80_end:
.org 0x1AA84
m68k_01aa84:
        move.w #0x3e7,%d2
m68k_01aa84_end:
.org 0x1AA88
m68k_01aa88:
        move.w %d2,(%a1, %d1.w)
m68k_01aa88_end:
.org 0x1AA8C
m68k_01aa8c:
        move.w %d7,%d0
m68k_01aa8c_end:
.org 0x1AA8E
m68k_01aa8e:
        move.w 0xf3a6:w,%d1
m68k_01aa8e_end:
.org 0x1AA92
m68k_01aa92:
        lsl.w #0x1,%d1
m68k_01aa92_end:
.org 0x1AA94
m68k_01aa94:
        move.w (%a0, %d1.w),%d2
m68k_01aa94_end:
.org 0x1AA98
m68k_01aa98:
        add.w %d0,%d2
m68k_01aa98_end:
.org 0x1AA9A
m68k_01aa9a:
        cmpi.w #0x3e7,%d2
m68k_01aa9a_end:
.org 0x1AA9E
m68k_01aa9e:
        bls.w (. + 8)
m68k_01aa9e_end:
.org 0x1AAA2
m68k_01aaa2:
        move.w #0x3e7,%d2
m68k_01aaa2_end:
.org 0x1AAA6
m68k_01aaa6:
        move.w %d2,(%a0, %d1.w)
m68k_01aaa6_end:
.org 0x1AAAA
m68k_01aaaa:
        lsr.w #0x1,%d0
m68k_01aaaa_end:
.org 0x1AAAC
m68k_01aaac:
        move.w (%a1, %d1.w),%d2
m68k_01aaac_end:
.org 0x1AAB0
m68k_01aab0:
        add.w %d0,%d2
m68k_01aab0_end:
.org 0x1AAB2
m68k_01aab2:
        cmpi.w #0x3e7,%d2
m68k_01aab2_end:
.org 0x1AAB6
m68k_01aab6:
        bls.w (. + 8)
m68k_01aab6_end:
.org 0x1AABA
m68k_01aaba:
        move.w #0x3e7,%d2
m68k_01aaba_end:
.org 0x1AABE
m68k_01aabe:
        move.w %d2,(%a1, %d1.w)
m68k_01aabe_end:
.org 0x1AAC2
m68k_01aac2:
        move.w #0x1c,0xff7026:l
m68k_01aac2_end:
.org 0x1AACA
m68k_01aaca:
        andi.w #0xfffe,%sr
m68k_01aaca_end:
.org 0x1AACE
m68k_01aace:
        bra.w (. + 252)
m68k_01aace_end:
.org 0x1AAD2
m68k_01aad2:
        jsr 0x83d4:l
m68k_01aad2_end:
.org 0x1AAD8
m68k_01aad8:
        andi.l #0xffff,%d0
m68k_01aad8_end:
.org 0x1AADE
m68k_01aade:
        move.l %d0,%d1
m68k_01aade_end:
.org 0x1AAE0
m68k_01aae0:
        lsl.l #0x1,%d0
m68k_01aae0_end:
.org 0x1AAE2
m68k_01aae2:
        add.l %d1,%d0
m68k_01aae2_end:
.org 0x1AAE4
m68k_01aae4:
        lsl.l #0x1,%d0
m68k_01aae4_end:
.org 0x1AAE6
m68k_01aae6:
        swap %d0
m68k_01aae6_end:
.org 0x1AAE8
m68k_01aae8:
        lea.l 0xc500:w,%a0
m68k_01aae8_end:
.org 0x1AAEC
m68k_01aaec:
        move.w 0xf3f2:w,%d1
m68k_01aaec_end:
.org 0x1AAF0
m68k_01aaf0:
        move.b (%a0, %d1.w),%d2
m68k_01aaf0_end:
.org 0x1AAF4
m68k_01aaf4:
        sub.b %d0,%d2
m68k_01aaf4_end:
.org 0x1AAF6
m68k_01aaf6:
        bcc.b (. + 4)
m68k_01aaf6_end:
.org 0x1AAF8
m68k_01aaf8:
        clr.b %d2
m68k_01aaf8_end:
.org 0x1AAFA
m68k_01aafa:
        move.b %d2,(%a0, %d1.w)
m68k_01aafa_end:
.org 0x1AAFE
m68k_01aafe:
        jsr 0x83d4:l
m68k_01aafe_end:
.org 0x1AB04
m68k_01ab04:
        andi.l #0xffff,%d0
m68k_01ab04_end:
.org 0x1AB0A
m68k_01ab0a:
        move.l %d0,%d1
m68k_01ab0a_end:
.org 0x1AB0C
m68k_01ab0c:
        lsl.l #0x1,%d0
m68k_01ab0c_end:
.org 0x1AB0E
m68k_01ab0e:
        add.l %d1,%d0
m68k_01ab0e_end:
.org 0x1AB10
m68k_01ab10:
        lsl.l #0x1,%d0
m68k_01ab10_end:
.org 0x1AB12
m68k_01ab12:
        swap %d0
m68k_01ab12_end:
.org 0x1AB14
m68k_01ab14:
        move.w 0xf3a6:w,%d1
m68k_01ab14_end:
.org 0x1AB18
m68k_01ab18:
        move.b (%a0, %d1.w),%d2
m68k_01ab18_end:
.org 0x1AB1C
m68k_01ab1c:
        sub.b %d0,%d2
m68k_01ab1c_end:
.org 0x1AB1E
m68k_01ab1e:
        bcc.b (. + 4)
m68k_01ab1e_end:
.org 0x1AB20
m68k_01ab20:
        clr.b %d2
m68k_01ab20_end:
.org 0x1AB22
m68k_01ab22:
        move.b %d2,(%a0, %d1.w)
m68k_01ab22_end:
.org 0x1AB26
m68k_01ab26:
        lea.l 0xbe00:w,%a1
m68k_01ab26_end:
.org 0x1AB2A
m68k_01ab2a:
        lea.l 0xc000:w,%a2
m68k_01ab2a_end:
.org 0x1AB2E
m68k_01ab2e:
        lea.l 0xb600:w,%a0
m68k_01ab2e_end:
.org 0x1AB32
m68k_01ab32:
        move.w 0xf3a6:w,%d0
m68k_01ab32_end:
.org 0x1AB36
m68k_01ab36:
        lsl.w #0x1,%d0
m68k_01ab36_end:
.org 0x1AB38
m68k_01ab38:
        move.w (%a0, %d0.w),%d1
m68k_01ab38_end:
.org 0x1AB3C
m68k_01ab3c:
        move.w 0xf3f2:w,%d2
m68k_01ab3c_end:
.org 0x1AB40
m68k_01ab40:
        lsl.w #0x1,%d2
m68k_01ab40_end:
.org 0x1AB42
m68k_01ab42:
        sub.w (%a0, %d2.w),%d1
m68k_01ab42_end:
.org 0x1AB46
m68k_01ab46:
        bcs.w (. + 34)
m68k_01ab46_end:
.org 0x1AB4A
m68k_01ab4a:
        andi.w #0xffff,%d1
m68k_01ab4a_end:
.org 0x1AB4E
m68k_01ab4e:
        divu.w #0xa,%d1
m68k_01ab4e_end:
.org 0x1AB52
m68k_01ab52:
        move.w (%a1, %d2.w),%d3
m68k_01ab52_end:
.org 0x1AB56
m68k_01ab56:
        add.w %d1,%d3
m68k_01ab56_end:
.org 0x1AB58
m68k_01ab58:
        cmpi.w #0x3e7,%d3
m68k_01ab58_end:
.org 0x1AB5C
m68k_01ab5c:
        bls.w (. + 8)
m68k_01ab5c_end:
.org 0x1AB60
m68k_01ab60:
        move.w #0x3e7,%d3
m68k_01ab60_end:
.org 0x1AB64
m68k_01ab64:
        move.w %d3,(%a1, %d2.w)
m68k_01ab64_end:
.org 0x1AB68
m68k_01ab68:
        jsr 0x83d4:l
m68k_01ab68_end:
.org 0x1AB6E
m68k_01ab6e:
        andi.l #0xffff,%d0
m68k_01ab6e_end:
.org 0x1AB74
m68k_01ab74:
        lsl.w #0x4,%d0
m68k_01ab74_end:
.org 0x1AB76
m68k_01ab76:
        swap %d0
m68k_01ab76_end:
.org 0x1AB78
m68k_01ab78:
        addi.w #0x5,%d0
m68k_01ab78_end:
.org 0x1AB7C
m68k_01ab7c:
        move.w 0xf3a6:w,%d2
m68k_01ab7c_end:
.org 0x1AB80
m68k_01ab80:
        lsl.w #0x1,%d2
m68k_01ab80_end:
.org 0x1AB82
m68k_01ab82:
        move.w (%a2, %d2.w),%d4
m68k_01ab82_end:
.org 0x1AB86
m68k_01ab86:
        add.w %d0,%d4
m68k_01ab86_end:
.org 0x1AB88
m68k_01ab88:
        cmpi.w #0x3e7,%d4
m68k_01ab88_end:
.org 0x1AB8C
m68k_01ab8c:
        bls.w (. + 8)
m68k_01ab8c_end:
.org 0x1AB90
m68k_01ab90:
        move.w #0x3e7,%d4
m68k_01ab90_end:
.org 0x1AB94
m68k_01ab94:
        move.w %d4,(%a2, %d2.w)
m68k_01ab94_end:
.org 0x1AB98
m68k_01ab98:
        jsr 0x83d4:l
m68k_01ab98_end:
.org 0x1AB9E
m68k_01ab9e:
        andi.l #0xffff,%d0
m68k_01ab9e_end:
.org 0x1ABA4
m68k_01aba4:
        move.l %d0,%d1
m68k_01aba4_end:
.org 0x1ABA6
m68k_01aba6:
        lsl.l #0x1,%d0
m68k_01aba6_end:
.org 0x1ABA8
m68k_01aba8:
        add.l %d1,%d0
m68k_01aba8_end:
.org 0x1ABAA
m68k_01abaa:
        lsl.l #0x2,%d0
m68k_01abaa_end:
.org 0x1ABAC
m68k_01abac:
        add.l %d1,%d0
m68k_01abac_end:
.org 0x1ABAE
m68k_01abae:
        swap %d0
m68k_01abae_end:
.org 0x1ABB0
m68k_01abb0:
        move.w (%a1, %d2.w),%d4
m68k_01abb0_end:
.org 0x1ABB4
m68k_01abb4:
        add.w %d0,%d4
m68k_01abb4_end:
.org 0x1ABB6
m68k_01abb6:
        cmpi.w #0x3e7,%d4
m68k_01abb6_end:
.org 0x1ABBA
m68k_01abba:
        bls.w (. + 8)
m68k_01abba_end:
.org 0x1ABBE
m68k_01abbe:
        move.w #0x3e7,%d4
m68k_01abbe_end:
.org 0x1ABC2
m68k_01abc2:
        move.w %d4,(%a1, %d2.w)
m68k_01abc2_end:
.org 0x1ABC6
m68k_01abc6:
        ori.w #0x1,%sr
m68k_01abc6_end:
.org 0x1ABCA
m68k_01abca:
        rts
m68k_01abca_end:
.org 0x1ABCC
m68k_01abcc:
        bsr.w (. + -1222)
m68k_01abcc_end:
.org 0x1ABD0
m68k_01abd0:
        addq.w #0x5,%d4
m68k_01abd0_end:
.org 0x1ABD2
m68k_01abd2:
        move.w %d0,%d4
m68k_01abd2_end:
.org 0x1ABD4
m68k_01abd4:
        bsr.w (. + -1948)
m68k_01abd4_end:
.org 0x1ABD8
m68k_01abd8:
        move.w 0xf3a6:w,%d0
m68k_01abd8_end:
.org 0x1ABDC
m68k_01abdc:
        lsl.w #0x2,%d0
m68k_01abdc_end:
.org 0x1ABDE
m68k_01abde:
        lea.l 0xa150:w,%a1
m68k_01abde_end:
.org 0x1ABE2
m68k_01abe2:
        move.w (%a1, %d0.w),%d1
m68k_01abe2_end:
.org 0x1ABE6
m68k_01abe6:
        lsr.w #0x7,%d1
m68k_01abe6_end:
.org 0x1ABE8
m68k_01abe8:
        move.w 0x2(%a1, %d0.w),%d2
m68k_01abe8_end:
.org 0x1ABEC
m68k_01abec:
        lsr.w #0x7,%d2
m68k_01abec_end:
.org 0x1ABEE
m68k_01abee:
        jsr -1954(%pc)
m68k_01abee_end:
.org 0x1ABF2
m68k_01abf2:
        cmpi.w #0x6,%d0
m68k_01abf2_end:
.org 0x1ABF6
m68k_01abf6:
        bne.b (. + 10)
m68k_01abf6_end:
.org 0x1ABF8
m68k_01abf8:
        mulu.w #0xc,%d4
m68k_01abf8_end:
.org 0x1ABFC
m68k_01abfc:
        divu.w #0xa,%d4
m68k_01abfc_end:
.org 0x1AC00
m68k_01ac00:
        move.w %d4,%d0
m68k_01ac00_end:
.org 0x1AC02
m68k_01ac02:
        rts
m68k_01ac02_end:
.org 0x1AC04
m68k_01ac04:
        move.w 0xf3a6:w,%d0
m68k_01ac04_end:
.org 0x1AC08
m68k_01ac08:
        lea.l 0xa654:w,%a0
m68k_01ac08_end:
.org 0x1AC0C
m68k_01ac0c:
        move.b #0x82,(%a0, %d0.w)
m68k_01ac0c_end:
.org 0x1AC12
m68k_01ac12:
        lea.l 0xa854:w,%a0
m68k_01ac12_end:
.org 0x1AC16
m68k_01ac16:
        move.b 0xf3f3:w,(%a0, %d0.w)
m68k_01ac16_end:
.org 0x1AC1C
m68k_01ac1c:
        rts
m68k_01ac1c_end:
