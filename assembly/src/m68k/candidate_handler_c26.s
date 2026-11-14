| 候选处理入口 01AC26。地址布局给出本文件负责的指令范围。
.cpu 68000
.section .text
_start:
.org 0x1AC26
m68k_01ac26:
        bsr.w (. + 822)
m68k_01ac26_end:
.org 0x1AC2A
m68k_01ac2a:
        cmpi.w #0xa,%d0
m68k_01ac2a_end:
.org 0x1AC2E
m68k_01ac2e:
        bcc.w (. + 164)
m68k_01ac2e_end:
.org 0x1AC32
m68k_01ac32:
        move.w 0xf3a6:w,%d0
m68k_01ac32_end:
.org 0x1AC36
m68k_01ac36:
        lea.l 0xe640:w,%a0
m68k_01ac36_end:
.org 0x1AC3A
m68k_01ac3a:
        move.w #0xf,%d1
m68k_01ac3a_end:
.org 0x1AC3E
m68k_01ac3e:
        cmp.w (%a0)+,%d0
m68k_01ac3e_end:
.org 0x1AC40
m68k_01ac40:
        beq.w (. + 146)
m68k_01ac40_end:
.org 0x1AC44
m68k_01ac44:
        dbra %d1,(. + -6)
m68k_01ac44_end:
.org 0x1AC48
m68k_01ac48:
        bsr.w (. + 254)
m68k_01ac48_end:
.org 0x1AC4C
m68k_01ac4c:
        cmp.l %d0,%d2
m68k_01ac4c_end:
.org 0x1AC4E
m68k_01ac4e:
        bcs.w (. + 132)
m68k_01ac4e_end:
.org 0x1AC52
m68k_01ac52:
        bsr.w (. + 590)
m68k_01ac52_end:
.org 0x1AC56
m68k_01ac56:
        jsr 0x83d4:l
m68k_01ac56_end:
.org 0x1AC5C
m68k_01ac5c:
        andi.l #0xffff,%d0
m68k_01ac5c_end:
.org 0x1AC62
m68k_01ac62:
        move.l %d0,%d1
m68k_01ac62_end:
.org 0x1AC64
m68k_01ac64:
        lsl.l #0x1,%d0
m68k_01ac64_end:
.org 0x1AC66
m68k_01ac66:
        add.l %d1,%d0
m68k_01ac66_end:
.org 0x1AC68
m68k_01ac68:
        lsl.l #0x1,%d0
m68k_01ac68_end:
.org 0x1AC6A
m68k_01ac6a:
        swap %d0
m68k_01ac6a_end:
.org 0x1AC6C
m68k_01ac6c:
        addi.w #0xf,%d0
m68k_01ac6c_end:
.org 0x1AC70
m68k_01ac70:
        lea.l 0xbe00:w,%a0
m68k_01ac70_end:
.org 0x1AC74
m68k_01ac74:
        move.w 0xf3f2:w,%d1
m68k_01ac74_end:
.org 0x1AC78
m68k_01ac78:
        lsl.w #0x1,%d1
m68k_01ac78_end:
.org 0x1AC7A
m68k_01ac7a:
        move.w (%a0, %d1.w),%d2
m68k_01ac7a_end:
.org 0x1AC7E
m68k_01ac7e:
        add.w %d0,%d2
m68k_01ac7e_end:
.org 0x1AC80
m68k_01ac80:
        cmpi.w #0x3e7,%d2
m68k_01ac80_end:
.org 0x1AC84
m68k_01ac84:
        bls.w (. + 8)
m68k_01ac84_end:
.org 0x1AC88
m68k_01ac88:
        move.w #0x3e7,%d2
m68k_01ac88_end:
.org 0x1AC8C
m68k_01ac8c:
        move.w %d2,(%a0, %d1.w)
m68k_01ac8c_end:
.org 0x1AC90
m68k_01ac90:
        bsr.w (. + -1180)
m68k_01ac90_end:
.org 0x1AC94
m68k_01ac94:
        andi.w #0xfffe,%sr
m68k_01ac94_end:
.org 0x1AC98
m68k_01ac98:
        move.w 0xf68c:w,%d0
m68k_01ac98_end:
.org 0x1AC9C
m68k_01ac9c:
        btst.b #0x1,0xae29:w
m68k_01ac9c_end:
.org 0x1ACA2
m68k_01aca2:
        beq.w (. + 8)
m68k_01aca2_end:
.org 0x1ACA6
m68k_01aca6:
        move.w 0xf68e:w,%d0
m68k_01aca6_end:
.org 0x1ACAA
m68k_01acaa:
        move.w 0xf3f2:w,-(%a7)
m68k_01acaa_end:
.org 0x1ACAE
m68k_01acae:
        move.w %d0,0xf3f2:w
m68k_01acae_end:
.org 0x1ACB2
m68k_01acb2:
        jsr 0x208ce:l
m68k_01acb2_end:
.org 0x1ACB8
m68k_01acb8:
        move.w (%a7)+,0xf3f2:w
m68k_01acb8_end:
.org 0x1ACBC
m68k_01acbc:
        move.w #0x1b,0xff7026:l
m68k_01acbc_end:
.org 0x1ACC4
m68k_01acc4:
        move.w 0xf3a6:w,0xf3d2:w
m68k_01acc4_end:
.org 0x1ACCA
m68k_01acca:
        andi.w #0xfffe,%sr
m68k_01acca_end:
.org 0x1ACCE
m68k_01acce:
        bra.w (. + 118)
m68k_01acce_end:
.org 0x1ACD2
m68k_01acd2:
        jsr 0x83d4:l
m68k_01acd2_end:
.org 0x1ACD8
m68k_01acd8:
        andi.l #0xffff,%d0
m68k_01acd8_end:
.org 0x1ACDE
m68k_01acde:
        move.l %d0,%d1
m68k_01acde_end:
.org 0x1ACE0
m68k_01ace0:
        lsl.l #0x1,%d0
m68k_01ace0_end:
.org 0x1ACE2
m68k_01ace2:
        add.l %d1,%d0
m68k_01ace2_end:
.org 0x1ACE4
m68k_01ace4:
        swap %d0
m68k_01ace4_end:
.org 0x1ACE6
m68k_01ace6:
        addi.w #0x1,%d0
m68k_01ace6_end:
.org 0x1ACEA
m68k_01acea:
        lea.l 0xbe00:w,%a0
m68k_01acea_end:
.org 0x1ACEE
m68k_01acee:
        move.w 0xf3f2:w,%d1
m68k_01acee_end:
.org 0x1ACF2
m68k_01acf2:
        lsl.w #0x1,%d1
m68k_01acf2_end:
.org 0x1ACF4
m68k_01acf4:
        move.w (%a0, %d1.w),%d2
m68k_01acf4_end:
.org 0x1ACF8
m68k_01acf8:
        add.w %d0,%d2
m68k_01acf8_end:
.org 0x1ACFA
m68k_01acfa:
        cmpi.w #0x3e7,%d2
m68k_01acfa_end:
.org 0x1ACFE
m68k_01acfe:
        bls.b (. + 6)
m68k_01acfe_end:
.org 0x1AD00
m68k_01ad00:
        move.w #0x3e7,%d2
m68k_01ad00_end:
.org 0x1AD04
m68k_01ad04:
        move.w %d2,(%a0, %d1.w)
m68k_01ad04_end:
.org 0x1AD08
m68k_01ad08:
        jsr 0x83d4:l
m68k_01ad08_end:
.org 0x1AD0E
m68k_01ad0e:
        andi.l #0xffff,%d0
m68k_01ad0e_end:
.org 0x1AD14
m68k_01ad14:
        move.l %d0,%d1
m68k_01ad14_end:
.org 0x1AD16
m68k_01ad16:
        lsl.l #0x2,%d0
m68k_01ad16_end:
.org 0x1AD18
m68k_01ad18:
        add.l %d1,%d0
m68k_01ad18_end:
.org 0x1AD1A
m68k_01ad1a:
        lsl.l #0x1,%d0
m68k_01ad1a_end:
.org 0x1AD1C
m68k_01ad1c:
        add.l %d1,%d0
m68k_01ad1c_end:
.org 0x1AD1E
m68k_01ad1e:
        swap %d0
m68k_01ad1e_end:
.org 0x1AD20
m68k_01ad20:
        lea.l 0xc200:w,%a0
m68k_01ad20_end:
.org 0x1AD24
m68k_01ad24:
        move.w 0xf3a6:w,%d1
m68k_01ad24_end:
.org 0x1AD28
m68k_01ad28:
        clr.w %d2
m68k_01ad28_end:
.org 0x1AD2A
m68k_01ad2a:
        move.b (%a0, %d1.w),%d2
m68k_01ad2a_end:
.org 0x1AD2E
m68k_01ad2e:
        mulu.w %d0,%d2
m68k_01ad2e_end:
.org 0x1AD30
m68k_01ad30:
        divu.w #0x64,%d2
m68k_01ad30_end:
.org 0x1AD34
m68k_01ad34:
        sub.b %d2,(%a0, %d1.w)
m68k_01ad34_end:
.org 0x1AD38
m68k_01ad38:
        bcc.w (. + 8)
m68k_01ad38_end:
.org 0x1AD3C
m68k_01ad3c:
        clr.b (%a0, %d1.w)
m68k_01ad3c_end:
.org 0x1AD40
m68k_01ad40:
        ori.w #0x1,%sr
m68k_01ad40_end:
.org 0x1AD44
m68k_01ad44:
        rts
m68k_01ad44_end:
.org 0x1AD46
m68k_01ad46:
        move.w 0xf3a6:w,%d0
m68k_01ad46_end:
.org 0x1AD4A
m68k_01ad4a:
        lea.l 0xc300:w,%a0
m68k_01ad4a_end:
.org 0x1AD4E
m68k_01ad4e:
        clr.w %d1
m68k_01ad4e_end:
.org 0x1AD50
m68k_01ad50:
        move.b (%a0, %d0.w),%d1
m68k_01ad50_end:
.org 0x1AD54
m68k_01ad54:
        move.w #0x64,%d2
m68k_01ad54_end:
.org 0x1AD58
m68k_01ad58:
        sub.w %d1,%d2
m68k_01ad58_end:
.org 0x1AD5A
m68k_01ad5a:
        move.w 0xf3f2:w,%d0
m68k_01ad5a_end:
.org 0x1AD5E
m68k_01ad5e:
        lea.l 0xcc00:w,%a0
m68k_01ad5e_end:
.org 0x1AD62
m68k_01ad62:
        clr.w %d1
m68k_01ad62_end:
.org 0x1AD64
m68k_01ad64:
        move.b (%a0, %d0.w),%d1
m68k_01ad64_end:
.org 0x1AD68
m68k_01ad68:
        andi.w #0x3f,%d1
m68k_01ad68_end:
.org 0x1AD6C
m68k_01ad6c:
        lea.l 0xf427:w,%a0
m68k_01ad6c_end:
.org 0x1AD70
m68k_01ad70:
        clr.w %d0
m68k_01ad70_end:
.org 0x1AD72
m68k_01ad72:
        move.b (%a0, %d1.w),%d0
m68k_01ad72_end:
.org 0x1AD76
m68k_01ad76:
        lsl.w #0x1,%d0
m68k_01ad76_end:
.org 0x1AD78
m68k_01ad78:
        lea.l 0xe640:w,%a0
m68k_01ad78_end:
.org 0x1AD7C
m68k_01ad7c:
        move.w (%a0, %d0.w),%d0
m68k_01ad7c_end:
.org 0x1AD80
m68k_01ad80:
        lea.l 0xc200:w,%a0
m68k_01ad80_end:
.org 0x1AD84
m68k_01ad84:
        clr.w %d1
m68k_01ad84_end:
.org 0x1AD86
m68k_01ad86:
        move.b (%a0, %d0.w),%d1
m68k_01ad86_end:
.org 0x1AD8A
m68k_01ad8a:
        mulu.w %d1,%d2
m68k_01ad8a_end:
.org 0x1AD8C
m68k_01ad8c:
        move.w 0xf3f2:w,%d0
m68k_01ad8c_end:
.org 0x1AD90
m68k_01ad90:
        clr.w %d1
m68k_01ad90_end:
.org 0x1AD92
m68k_01ad92:
        move.b (%a0, %d0.w),%d1
m68k_01ad92_end:
.org 0x1AD96
m68k_01ad96:
        mulu.w %d1,%d2
m68k_01ad96_end:
.org 0x1AD98
m68k_01ad98:
        lsl.w #0x1,%d0
m68k_01ad98_end:
.org 0x1AD9A
m68k_01ad9a:
        lea.l 0xb600:w,%a0
m68k_01ad9a_end:
.org 0x1AD9E
m68k_01ad9e:
        move.w (%a0, %d0.w),%d1
m68k_01ad9e_end:
.org 0x1ADA2
m68k_01ada2:
        move.w %d2,%d0
m68k_01ada2_end:
.org 0x1ADA4
m68k_01ada4:
        mulu.w %d1,%d0
m68k_01ada4_end:
.org 0x1ADA6
m68k_01ada6:
        swap %d2
m68k_01ada6_end:
.org 0x1ADA8
m68k_01ada8:
        mulu.w %d1,%d2
m68k_01ada8_end:
.org 0x1ADAA
m68k_01adaa:
        swap %d2
m68k_01adaa_end:
.org 0x1ADAC
m68k_01adac:
        add.l %d0,%d2
m68k_01adac_end:
.org 0x1ADAE
m68k_01adae:
        bsr.w (. + 110)
m68k_01adae_end:
.org 0x1ADB2
m68k_01adb2:
        move.w %d2,%d0
m68k_01adb2_end:
.org 0x1ADB4
m68k_01adb4:
        mulu.w %d1,%d0
m68k_01adb4_end:
.org 0x1ADB6
m68k_01adb6:
        swap %d2
m68k_01adb6_end:
.org 0x1ADB8
m68k_01adb8:
        mulu.w %d1,%d2
m68k_01adb8_end:
.org 0x1ADBA
m68k_01adba:
        swap %d2
m68k_01adba_end:
.org 0x1ADBC
m68k_01adbc:
        add.l %d0,%d2
m68k_01adbc_end:
.org 0x1ADBE
m68k_01adbe:
        lsr.l #0x4,%d2
m68k_01adbe_end:
.org 0x1ADC0
m68k_01adc0:
        move.w 0xf3a6:w,%d0
m68k_01adc0_end:
.org 0x1ADC4
m68k_01adc4:
        lea.l 0xc200:w,%a0
m68k_01adc4_end:
.org 0x1ADC8
m68k_01adc8:
        clr.w %d1
m68k_01adc8_end:
.org 0x1ADCA
m68k_01adca:
        move.b (%a0, %d0.w),%d1
m68k_01adca_end:
.org 0x1ADCE
m68k_01adce:
        addq.w #0x1,%d1
m68k_01adce_end:
.org 0x1ADD0
m68k_01add0:
        lea.l 0xcc00:w,%a1
m68k_01add0_end:
.org 0x1ADD4
m68k_01add4:
        move.b (%a1, %d0.w),%d3
m68k_01add4_end:
.org 0x1ADD8
m68k_01add8:
        andi.w #0x3f,%d3
m68k_01add8_end:
.org 0x1ADDC
m68k_01addc:
        lea.l 0xf427:w,%a1
m68k_01addc_end:
.org 0x1ADE0
m68k_01ade0:
        clr.w %d4
m68k_01ade0_end:
.org 0x1ADE2
m68k_01ade2:
        move.b (%a1, %d3.w),%d4
m68k_01ade2_end:
.org 0x1ADE6
m68k_01ade6:
        lsl.w #0x1,%d4
m68k_01ade6_end:
.org 0x1ADE8
m68k_01ade8:
        lea.l 0xe640:w,%a1
m68k_01ade8_end:
.org 0x1ADEC
m68k_01adec:
        move.w (%a1, %d4.w),%d4
m68k_01adec_end:
.org 0x1ADF0
m68k_01adf0:
        clr.w %d3
m68k_01adf0_end:
.org 0x1ADF2
m68k_01adf2:
        move.b (%a0, %d4.w),%d3
m68k_01adf2_end:
.org 0x1ADF6
m68k_01adf6:
        addq.w #0x1,%d3
m68k_01adf6_end:
.org 0x1ADF8
m68k_01adf8:
        mulu.w %d3,%d1
m68k_01adf8_end:
.org 0x1ADFA
m68k_01adfa:
        lsl.w #0x1,%d0
m68k_01adfa_end:
.org 0x1ADFC
m68k_01adfc:
        lea.l 0xb600:w,%a0
m68k_01adfc_end:
.org 0x1AE00
m68k_01ae00:
        move.w (%a0, %d0.w),%d0
m68k_01ae00_end:
.org 0x1AE04
m68k_01ae04:
        addq.w #0x1,%d0
m68k_01ae04_end:
.org 0x1AE06
m68k_01ae06:
        mulu.w %d0,%d1
m68k_01ae06_end:
.org 0x1AE08
m68k_01ae08:
        move.w %d1,%d0
m68k_01ae08_end:
.org 0x1AE0A
m68k_01ae0a:
        mulu.w #0x7d,%d0
m68k_01ae0a_end:
.org 0x1AE0E
m68k_01ae0e:
        swap %d1
m68k_01ae0e_end:
.org 0x1AE10
m68k_01ae10:
        mulu.w #0x7d,%d1
m68k_01ae10_end:
.org 0x1AE14
m68k_01ae14:
        swap %d1
m68k_01ae14_end:
.org 0x1AE16
m68k_01ae16:
        add.l %d1,%d0
m68k_01ae16_end:
.org 0x1AE18
m68k_01ae18:
        lsr.l #0x1,%d0
m68k_01ae18_end:
.org 0x1AE1A
m68k_01ae1a:
        rts
m68k_01ae1a_end:
.org 0x1AE1C
m68k_01ae1c:
        jsr 0x83d4:l
m68k_01ae1c_end:
.org 0x1AE22
m68k_01ae22:
        move.w 0xf3f2:w,%d0
m68k_01ae22_end:
.org 0x1AE26
m68k_01ae26:
        move.w #0x4,%d1
m68k_01ae26_end:
.org 0x1AE2A
m68k_01ae2a:
        lea.l 0xc700:w,%a0
m68k_01ae2a_end:
.org 0x1AE2E
m68k_01ae2e:
        move.b (%a0, %d0.w),%d0
m68k_01ae2e_end:
.org 0x1AE32
m68k_01ae32:
        andi.w #0x7,%d0
m68k_01ae32_end:
.org 0x1AE36
m68k_01ae36:
        sub.w %d0,%d1
m68k_01ae36_end:
.org 0x1AE38
m68k_01ae38:
        move.w %d1,%d0
m68k_01ae38_end:
.org 0x1AE3A
m68k_01ae3a:
        lsl.w #0x2,%d0
m68k_01ae3a_end:
.org 0x1AE3C
m68k_01ae3c:
        add.w %d1,%d0
m68k_01ae3c_end:
.org 0x1AE3E
m68k_01ae3e:
        move.w 0xf3a6:w,%d1
m68k_01ae3e_end:
.org 0x1AE42
m68k_01ae42:
        move.w #0x4,%d3
m68k_01ae42_end:
.org 0x1AE46
m68k_01ae46:
        move.b (%a0, %d1.w),%d1
m68k_01ae46_end:
.org 0x1AE4A
m68k_01ae4a:
        andi.w #0x7,%d1
m68k_01ae4a_end:
.org 0x1AE4E
m68k_01ae4e:
        sub.w %d1,%d3
m68k_01ae4e_end:
.org 0x1AE50
m68k_01ae50:
        add.w %d3,%d0
m68k_01ae50_end:
.org 0x1AE52
m68k_01ae52:
        lsl.w #0x1,%d0
m68k_01ae52_end:
.org 0x1AE54
m68k_01ae54:
        lea.l 24(%pc),%a1
m68k_01ae54_end:
.org 0x1AE58
m68k_01ae58:
        clr.w %d1
m68k_01ae58_end:
.org 0x1AE5A
m68k_01ae5a:
        move.b (%a1, %d0.w),%d1
m68k_01ae5a_end:
.org 0x1AE5E
m68k_01ae5e:
        mulu.w 0xf61c:w,%d1
m68k_01ae5e_end:
.org 0x1AE62
m68k_01ae62:
        swap %d1
m68k_01ae62_end:
.org 0x1AE64
m68k_01ae64:
        clr.w %d3
m68k_01ae64_end:
.org 0x1AE66
m68k_01ae66:
        move.b 0x1(%a1, %d0.w),%d3
m68k_01ae66_end:
.org 0x1AE6A
m68k_01ae6a:
        add.w %d3,%d1
m68k_01ae6a_end:
.org 0x1AE6C
m68k_01ae6c:
        rts
m68k_01ae6c_end:
.org 0x1AEA0
m68k_01aea0:
        move.w 0xf3a6:w,%d0
m68k_01aea0_end:
.org 0x1AEA4
m68k_01aea4:
        lea.l 0xa550:w,%a0
m68k_01aea4_end:
.org 0x1AEA8
m68k_01aea8:
        bsr.w (. + 30)
m68k_01aea8_end:
.org 0x1AEAC
m68k_01aeac:
        bcc.w (. + 12)
m68k_01aeac_end:
.org 0x1AEB0
m68k_01aeb0:
        subq.w #0x1,0xf6a6:w
m68k_01aeb0_end:
.org 0x1AEB4
m68k_01aeb4:
        bra.w (. + 16)
m68k_01aeb4_end:
.org 0x1AEB8
m68k_01aeb8:
        lea.l 0xa5a4:w,%a0
m68k_01aeb8_end:
.org 0x1AEBC
m68k_01aebc:
        bsr.w (. + 10)
m68k_01aebc_end:
.org 0x1AEC0
m68k_01aec0:
        subq.w #0x1,0xf6a8:w
m68k_01aec0_end:
.org 0x1AEC4
m68k_01aec4:
        rts
m68k_01aec4_end:
.org 0x1AEC6
m68k_01aec6:
        move.w (%a0)+,%d1
m68k_01aec6_end:
.org 0x1AEC8
m68k_01aec8:
        bmi.w (. + 126)
m68k_01aec8_end:
.org 0x1AECC
m68k_01aecc:
        cmp.b %d0,%d1
m68k_01aecc_end:
.org 0x1AECE
m68k_01aece:
        bne.b (. + -8)
m68k_01aece_end:
.org 0x1AED0
m68k_01aed0:
        lea.l -0x2(%a0),%a1
m68k_01aed0_end:
.org 0x1AED4
m68k_01aed4:
        move.w (%a0)+,(%a1)+
m68k_01aed4_end:
.org 0x1AED6
m68k_01aed6:
        bpl.b (. + -2)
m68k_01aed6_end:
.org 0x1AED8
m68k_01aed8:
        move.w 0xf6d6:w,%d0
m68k_01aed8_end:
.org 0x1AEDC
m68k_01aedc:
        andi.w #0x2,%d0
m68k_01aedc_end:
.org 0x1AEE0
m68k_01aee0:
        lsl.w #0x1,%d0
m68k_01aee0_end:
.org 0x1AEE2
m68k_01aee2:
        movea.l 104(%pc, %d0.w),%a0
m68k_01aee2_end:
.org 0x1AEE6
m68k_01aee6:
        move.w (%a0),%d1
m68k_01aee6_end:
.org 0x1AEE8
m68k_01aee8:
        movea.l 106(%pc, %d0.w),%a1
m68k_01aee8_end:
.org 0x1AEEC
m68k_01aeec:
        addq.w #0x1,(%a1)
m68k_01aeec_end:
.org 0x1AEEE
m68k_01aeee:
        tst.w (%a0)+
m68k_01aeee_end:
.org 0x1AEF0
m68k_01aef0:
        bpl.b (. + -2)
m68k_01aef0_end:
.org 0x1AEF2
m68k_01aef2:
        move.w 0xf3a6:w,-0x2(%a0)
m68k_01aef2_end:
.org 0x1AEF8
m68k_01aef8:
        move.w #0xffff,(%a0)
m68k_01aef8_end:
.org 0x1AEFC
m68k_01aefc:
        lea.l 0xcc00:w,%a0
m68k_01aefc_end:
.org 0x1AF00
m68k_01af00:
        move.b (%a0, %d1.w),%d1
m68k_01af00_end:
.org 0x1AF04
m68k_01af04:
        move.w 0xf3a6:w,%d2
m68k_01af04_end:
.org 0x1AF08
m68k_01af08:
        move.b %d1,(%a0, %d2.w)
m68k_01af08_end:
.org 0x1AF0C
m68k_01af0c:
        move.w 0xf3f2:w,-(%a7)
m68k_01af0c_end:
.org 0x1AF10
m68k_01af10:
        lea.l 0xf427:w,%a0
m68k_01af10_end:
.org 0x1AF14
m68k_01af14:
        andi.w #0x3f,%d1
m68k_01af14_end:
.org 0x1AF18
m68k_01af18:
        move.b (%a0, %d1.w),%d1
m68k_01af18_end:
.org 0x1AF1C
m68k_01af1c:
        lsl.w #0x1,%d1
m68k_01af1c_end:
.org 0x1AF1E
m68k_01af1e:
        lea.l 0xe640:w,%a0
m68k_01af1e_end:
.org 0x1AF22
m68k_01af22:
        move.w (%a0, %d1.w),0xf3f2:w
m68k_01af22_end:
.org 0x1AF28
m68k_01af28:
        jsr 0x208ce:l
m68k_01af28_end:
.org 0x1AF2E
m68k_01af2e:
        move.w (%a7)+,0xf3f2:w
m68k_01af2e_end:
.org 0x1AF32
m68k_01af32:
        lea.l 0xae28:w,%a0
m68k_01af32_end:
.org 0x1AF36
m68k_01af36:
        move.w 0xf3a6:w,%d0
m68k_01af36_end:
.org 0x1AF3A
m68k_01af3a:
        clr.b (%a0, %d0.w)
m68k_01af3a_end:
.org 0x1AF3E
m68k_01af3e:
        ori.w #0x1,%sr
m68k_01af3e_end:
.org 0x1AF42
m68k_01af42:
        bra.w (. + 8)
m68k_01af42_end:
.org 0x1AF46
m68k_01af46:
        andi.w #0xfffe,%sr
m68k_01af46_end:
.org 0x1AF4A
m68k_01af4a:
        rts
m68k_01af4a_end:
.org 0x1AF5C
m68k_01af5c:
        move.w 0xf6d6:w,%d0
m68k_01af5c_end:
.org 0x1AF60
m68k_01af60:
        andi.w #0x2,%d0
m68k_01af60_end:
.org 0x1AF64
m68k_01af64:
        lsl.w #0x1,%d0
m68k_01af64_end:
.org 0x1AF66
m68k_01af66:
        movea.l 16(%pc, %d0.w),%a0
m68k_01af66_end:
.org 0x1AF6A
m68k_01af6a:
        clr.w %d0
m68k_01af6a_end:
.org 0x1AF6C
m68k_01af6c:
        tst.w (%a0)+
m68k_01af6c_end:
.org 0x1AF6E
m68k_01af6e:
        bmi.w (. + 8)
m68k_01af6e_end:
.org 0x1AF72
m68k_01af72:
        addq.w #0x1,%d0
m68k_01af72_end:
.org 0x1AF74
m68k_01af74:
        bra.b (. + -8)
m68k_01af74_end:
.org 0x1AF76
m68k_01af76:
        rts
m68k_01af76_end:
.org 0x208CE
m68k_0208ce:
        movem.l %d0-%d4/%a0-%a1,-(%a7)
m68k_0208ce_end:
.org 0x208D2
m68k_0208d2:
        jsr 0x83d4:l
m68k_0208d2_end:
.org 0x208D8
m68k_0208d8:
        andi.l #0xffff,%d0
m68k_0208d8_end:
.org 0x208DE
m68k_0208de:
        move.l %d0,%d1
m68k_0208de_end:
.org 0x208E0
m68k_0208e0:
        lsl.l #0x2,%d0
m68k_0208e0_end:
.org 0x208E2
m68k_0208e2:
        add.l %d1,%d0
m68k_0208e2_end:
.org 0x208E4
m68k_0208e4:
        swap %d0
m68k_0208e4_end:
.org 0x208E6
m68k_0208e6:
        addi.w #0x6,%d0
m68k_0208e6_end:
.org 0x208EA
m68k_0208ea:
        lea.l 0xc300:w,%a0
m68k_0208ea_end:
.org 0x208EE
m68k_0208ee:
        move.w #0x68,%d1
m68k_0208ee_end:
.org 0x208F2
m68k_0208f2:
        move.w 0xf3a6:w,%d2
m68k_0208f2_end:
.org 0x208F6
m68k_0208f6:
        andi.w #0xff,%d2
m68k_0208f6_end:
.org 0x208FA
m68k_0208fa:
        sub.b (%a0, %d2.w),%d1
m68k_0208fa_end:
.org 0x208FE
m68k_0208fe:
        lsr.w #0x1,%d1
m68k_0208fe_end:
.org 0x20900
m68k_020900:
        lea.l 0xc200:w,%a1
m68k_020900_end:
.org 0x20904
m68k_020904:
        move.w 0xf3f2:w,%d4
m68k_020904_end:
.org 0x20908
m68k_020908:
        andi.w #0xff,%d4
m68k_020908_end:
.org 0x2090C
m68k_02090c:
        clr.w %d3
m68k_02090c_end:
.org 0x2090E
m68k_02090e:
        move.b (%a1, %d4.w),%d3
m68k_02090e_end:
.org 0x20912
m68k_020912:
        mulu.w %d3,%d1
m68k_020912_end:
.org 0x20914
m68k_020914:
        mulu.w %d0,%d1
m68k_020914_end:
.org 0x20916
m68k_020916:
        divu.w #0x1f4,%d1
m68k_020916_end:
.org 0x2091A
m68k_02091a:
        cmpi.w #0x64,%d1
m68k_02091a_end:
.org 0x2091E
m68k_02091e:
        bls.w (. + 8)
m68k_02091e_end:
.org 0x20922
m68k_020922:
        move.w #0x64,%d1
m68k_020922_end:
.org 0x20926
m68k_020926:
        move.b %d1,(%a0, %d2.w)
m68k_020926_end:
.org 0x2092A
m68k_02092a:
        movem.l (%a7)+,%d0-%d4/%a0-%a1
m68k_02092a_end:
.org 0x2092E
m68k_02092e:
        rts
m68k_02092e_end:
