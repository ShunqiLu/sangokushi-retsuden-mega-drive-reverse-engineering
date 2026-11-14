| 行动桥接和随机数例程。Z80 的驱动数据由地址布局单独映射。
.cpu 68000
.section .text
_start:
.org 0x83D4
m68k_0083d4:
        move.l 0xf61c:w,%d1
m68k_0083d4_end:
.org 0x83D8
m68k_0083d8:
        bne.b (. + 8)
m68k_0083d8_end:
.org 0x83DA
m68k_0083da:
        move.l #0x2a6d365a,%d1
m68k_0083da_end:
.org 0x83E0
m68k_0083e0:
        move.l %d1,%d0
m68k_0083e0_end:
.org 0x83E2
m68k_0083e2:
        asl.l #0x2,%d1
m68k_0083e2_end:
.org 0x83E4
m68k_0083e4:
        add.l %d0,%d1
m68k_0083e4_end:
.org 0x83E6
m68k_0083e6:
        asl.l #0x3,%d1
m68k_0083e6_end:
.org 0x83E8
m68k_0083e8:
        add.l %d0,%d1
m68k_0083e8_end:
.org 0x83EA
m68k_0083ea:
        move.w %d1,%d0
m68k_0083ea_end:
.org 0x83EC
m68k_0083ec:
        swap %d1
m68k_0083ec_end:
.org 0x83EE
m68k_0083ee:
        add.w %d1,%d0
m68k_0083ee_end:
.org 0x83F0
m68k_0083f0:
        move.w %d0,%d1
m68k_0083f0_end:
.org 0x83F2
m68k_0083f2:
        swap %d1
m68k_0083f2_end:
.org 0x83F4
m68k_0083f4:
        move.l %d1,0xf61c:w
m68k_0083f4_end:
.org 0x83F8
m68k_0083f8:
        rts
m68k_0083f8_end:
.org 0x19B2C
m68k_019b2c:
        move.w 0xf362:w,%d0
m68k_019b2c_end:
.org 0x19B30
m68k_019b30:
        lsl.w #0x1,%d0
m68k_019b30_end:
.org 0x19B32
m68k_019b32:
        move.w 14(%pc, %d0.w),%d0
m68k_019b32_end:
.org 0x19B36
m68k_019b36:
        jsr 38(%pc, %d0.w)
m68k_019b36_end:
.org 0x19B3A
m68k_019b3a:
        jsr 0xa3da:l
m68k_019b3a_end:
.org 0x19B40
m68k_019b40:
        rts
m68k_019b40_end:
.org 0x19C9E
m68k_019c9e:
        move.w 0xf612:w,0xf38a:w
m68k_019c9e_end:
.org 0x19CA4
m68k_019ca4:
        move.w #0x5,0xf3b0:w
m68k_019ca4_end:
.org 0x19CAA
m68k_019caa:
        move.w #0x40a,0xf612:w
m68k_019caa_end:
.org 0x19CB0
m68k_019cb0:
        clr.w 0xf362:w
m68k_019cb0_end:
.org 0x19CB4
m68k_019cb4:
        move.w 0xf6d6:w,%d0
m68k_019cb4_end:
.org 0x19CB8
m68k_019cb8:
        lsl.w #0x1,%d0
m68k_019cb8_end:
.org 0x19CBA
m68k_019cba:
        movea.l -38(%pc, %d0.w),%a0
m68k_019cba_end:
.org 0x19CBE
m68k_019cbe:
        lea.l 0xa5f8:w,%a1
m68k_019cbe_end:
.org 0x19CC2
m68k_019cc2:
        lea.l 0xa754:w,%a2
m68k_019cc2_end:
.org 0x19CC6
m68k_019cc6:
        lea.l 0xff3cc2:l,%a3
m68k_019cc6_end:
.org 0x19CCC
m68k_019ccc:
        move.w (%a0)+,%d0
m68k_019ccc_end:
.org 0x19CCE
m68k_019cce:
        bmi.b (. + 24)
m68k_019cce_end:
.org 0x19CD0
m68k_019cd0:
        cmpi.w #0x100,%d0
m68k_019cd0_end:
.org 0x19CD4
m68k_019cd4:
        bcc.b (. + -8)
m68k_019cd4_end:
.org 0x19CD6
m68k_019cd6:
        tst.b (%a2, %d0.w)
m68k_019cd6_end:
.org 0x19CDA
m68k_019cda:
        bne.b (. + -14)
m68k_019cda_end:
.org 0x19CDC
m68k_019cdc:
        tst.b (%a3, %d0.w)
m68k_019cdc_end:
.org 0x19CE0
m68k_019ce0:
        bne.b (. + -20)
m68k_019ce0_end:
.org 0x19CE2
m68k_019ce2:
        move.w %d0,(%a1)+
m68k_019ce2_end:
.org 0x19CE4
m68k_019ce4:
        bra.b (. + -24)
m68k_019ce4_end:
.org 0x19CE6
m68k_019ce6:
        move.w #0xffff,(%a1)+
m68k_019ce6_end:
.org 0x19CEA
m68k_019cea:
        rts
m68k_019cea_end:
.org 0x19CEC
m68k_019cec:
        tst.b 0xf3a6:w
m68k_019cec_end:
.org 0x19CF0
m68k_019cf0:
        bmi.w (. + 18)
m68k_019cf0_end:
.org 0x19CF4
m68k_019cf4:
        move.w #0x94,0xf600:w
m68k_019cf4_end:
.org 0x19CFA
m68k_019cfa:
        addq.w #0x1,0xf362:w
m68k_019cfa_end:
.org 0x19CFE
m68k_019cfe:
        bra.w (. + 14)
m68k_019cfe_end:
.org 0x19D02
m68k_019d02:
        clr.w 0xf362:w
m68k_019d02_end:
.org 0x19D06
m68k_019d06:
        move.w #0xffff,0xa5f8:w
m68k_019d06_end:
.org 0x19D0C
m68k_019d0c:
        rts
m68k_019d0c_end:
.org 0x19D0E
m68k_019d0e:
        tst.w 0xa62c:w
m68k_019d0e_end:
.org 0x19D12
m68k_019d12:
        bmi.b (. + 22)
m68k_019d12_end:
.org 0x19D14
m68k_019d14:
        lea.l 0xa62c:w,%a0
m68k_019d14_end:
.org 0x19D18
m68k_019d18:
        lea.l 0xa5f8:w,%a1
m68k_019d18_end:
.org 0x19D1C
m68k_019d1c:
        move.w (%a0)+,(%a1)+
m68k_019d1c_end:
.org 0x19D1E
m68k_019d1e:
        bpl.b (. + -2)
m68k_019d1e_end:
.org 0x19D20
m68k_019d20:
        addq.w #0x2,0xf362:w
m68k_019d20_end:
.org 0x19D24
m68k_019d24:
        bra.w (. + 44)
m68k_019d24_end:
.org 0x19D28
m68k_019d28:
        addq.w #0x1,0xf362:w
m68k_019d28_end:
.org 0x19D2C
m68k_019d2c:
        move.w 0xf3a6:w,0xf3d0:w
m68k_019d2c_end:
.org 0x19D32
m68k_019d32:
        tst.w 0xaf80:w
m68k_019d32_end:
.org 0x19D36
m68k_019d36:
        bne.w (. + 10)
m68k_019d36_end:
.org 0x19D3A
m68k_019d3a:
        move.w #0x107,0xaf80:w
m68k_019d3a_end:
.org 0x19D40
m68k_019d40:
        move.w 0xaf80:w,%d0
m68k_019d40_end:
.org 0x19D44
m68k_019d44:
        jsr 0x676f2:l
m68k_019d44_end:
.org 0x19D4A
m68k_019d4a:
        move.w #0x1,0xf652:w
m68k_019d4a_end:
.org 0x19D50
m68k_019d50:
        rts
m68k_019d50_end:
.org 0x19D52
m68k_019d52:
        btst.b #0x5,0xf603:w
m68k_019d52_end:
.org 0x19D58
m68k_019d58:
        beq.b (. + 8)
m68k_019d58_end:
.org 0x19D5A
m68k_019d5a:
        move.w #0x4,0xf362:w
m68k_019d5a_end:
.org 0x19D60
m68k_019d60:
        rts
m68k_019d60_end:
.org 0x19D62
m68k_019d62:
        move.w 0xf612:w,0xf38a:w
m68k_019d62_end:
.org 0x19D68
m68k_019d68:
        move.w #0x9,0xf3b0:w
m68k_019d68_end:
.org 0x19D6E
m68k_019d6e:
        move.w 0xf3a6:w,0xf3f2:w
m68k_019d6e_end:
.org 0x19D74
m68k_019d74:
        move.w #0x40a,0xf612:w
m68k_019d74_end:
.org 0x19D7A
m68k_019d7a:
        move.w #0x1,0xf362:w
m68k_019d7a_end:
.org 0x19D80
m68k_019d80:
        move.w 0xf3a6:w,0xf3d0:w
m68k_019d80_end:
.org 0x19D86
m68k_019d86:
        move.w #0x106,%d0
m68k_019d86_end:
.org 0x19D8A
m68k_019d8a:
        move.w %d0,0xaf80:w
m68k_019d8a_end:
.org 0x19D8E
m68k_019d8e:
        jsr 0x676f2:l
m68k_019d8e_end:
.org 0x19D94
m68k_019d94:
        move.w #0x1,0xf652:w
m68k_019d94_end:
.org 0x19D9A
m68k_019d9a:
        move.w #0x68,0xf35e:w
m68k_019d9a_end:
.org 0x19DA0
m68k_019da0:
        move.w #0x98,0xf360:w
m68k_019da0_end:
.org 0x19DA6
m68k_019da6:
        move.w #0x8000,0xf3a6:w
m68k_019da6_end:
.org 0x19DAC
m68k_019dac:
        rts
m68k_019dac_end:
.org 0x19DAE
m68k_019dae:
        tst.w 0xf3a6:w
m68k_019dae_end:
.org 0x19DB2
m68k_019db2:
        bpl.b (. + 12)
m68k_019db2_end:
.org 0x19DB4
m68k_019db4:
        move.w #0x4,0xf362:w
m68k_019db4_end:
.org 0x19DBA
m68k_019dba:
        bra.w (. + 40)
m68k_019dba_end:
.org 0x19DBE
m68k_019dbe:
        jsr 0x1af80:l
m68k_019dbe_end:
.org 0x19DC4
m68k_019dc4:
        bcs.w (. + 12)
m68k_019dc4_end:
.org 0x19DC8
m68k_019dc8:
        addq.w #0x2,0xf362:w
m68k_019dc8_end:
.org 0x19DCC
m68k_019dcc:
        bra.w (. + 22)
m68k_019dcc_end:
.org 0x19DD0
m68k_019dd0:
        addq.w #0x1,0xf362:w
m68k_019dd0_end:
.org 0x19DD4
m68k_019dd4:
        move.w #0x135,%d0
m68k_019dd4_end:
.org 0x19DD8
m68k_019dd8:
        move.w %d0,0xaf80:w
m68k_019dd8_end:
.org 0x19DDC
m68k_019ddc:
        jsr 0x676f2:l
m68k_019ddc_end:
.org 0x19DE2
m68k_019de2:
        rts
m68k_019de2_end:
.org 0x19DE4
m68k_019de4:
        move.w 0xf6d6:w,%d1
m68k_019de4_end:
.org 0x19DE8
m68k_019de8:
        andi.w #0x2,%d1
m68k_019de8_end:
.org 0x19DEC
m68k_019dec:
        lsl.w #0x1,%d1
m68k_019dec_end:
.org 0x19DEE
m68k_019dee:
        lea.l 30(%pc),%a0
m68k_019dee_end:
.org 0x19DF2
m68k_019df2:
        nop
m68k_019df2_end:
.org 0x19DF4
m68k_019df4:
        movea.l (%a0, %d1.w),%a0
m68k_019df4_end:
.org 0x19DF8
m68k_019df8:
        move.w (%a0)+,%d1
m68k_019df8_end:
.org 0x19DFA
m68k_019dfa:
        bmi.b (. + 14)
m68k_019dfa_end:
.org 0x19DFC
m68k_019dfc:
        cmp.w %d0,%d1
m68k_019dfc_end:
.org 0x19DFE
m68k_019dfe:
        bne.b (. + -6)
m68k_019dfe_end:
.org 0x19E00
m68k_019e00:
        ori.w #0x4000,-0x2(%a0)
m68k_019e00_end:
.org 0x19E06
m68k_019e06:
        rts
m68k_019e06_end:
.org 0x19E08
m68k_019e08:
        addq.w #0x1,0xf314:w
m68k_019e08_end:
.org 0x19E0C
m68k_019e0c:
        bra.b (. + -4)
m68k_019e0c_end:
.org 0x19E16
m68k_019e16:
        btst.b #0x5,0xf603:w
m68k_019e16_end:
.org 0x19E1C
m68k_019e1c:
        beq.w (. + 16)
m68k_019e1c_end:
.org 0x19E20
m68k_019e20:
        move.w #0x5,0xf362:w
m68k_019e20_end:
.org 0x19E26
m68k_019e26:
        move.w 0xf3f2:w,0xf3a6:w
m68k_019e26_end:
.org 0x19E2C
m68k_019e2c:
        rts
m68k_019e2c_end:
.org 0x19E2E
m68k_019e2e:
        lea.l 0xa754:w,%a0
m68k_019e2e_end:
.org 0x19E32
m68k_019e32:
        move.w 0xf3f2:w,%d0
m68k_019e32_end:
.org 0x19E36
m68k_019e36:
        move.b #0x3,(%a0, %d0.w)
m68k_019e36_end:
.org 0x19E3C
m68k_019e3c:
        move.w 0xf3f2:w,%d0
m68k_019e3c_end:
.org 0x19E40
m68k_019e40:
        bsr.b (. + -92)
m68k_019e40_end:
.org 0x19E42
m68k_019e42:
        jsr 0x1a47a:l
m68k_019e42_end:
.org 0x19E48
m68k_019e48:
        bcs.w (. + 12)
m68k_019e48_end:
.org 0x19E4C
m68k_019e4c:
        addq.w #0x1,0xf362:w
m68k_019e4c_end:
.org 0x19E50
m68k_019e50:
        bra.w (. + 36)
m68k_019e50_end:
.org 0x19E54
m68k_019e54:
        addq.w #0x2,0xf362:w
m68k_019e54_end:
.org 0x19E58
m68k_019e58:
        move.w #0x134,%d0
m68k_019e58_end:
.org 0x19E5C
m68k_019e5c:
        cmpi.w #0x4,0xf6d4:w
m68k_019e5c_end:
.org 0x19E62
m68k_019e62:
        bne.w (. + 8)
m68k_019e62_end:
.org 0x19E66
m68k_019e66:
        move.w #0x136,%d0
m68k_019e66_end:
.org 0x19E6A
m68k_019e6a:
        move.w %d0,0xaf80:w
m68k_019e6a_end:
.org 0x19E6E
m68k_019e6e:
        jsr 0x676f2:l
m68k_019e6e_end:
.org 0x19E74
m68k_019e74:
        move.w #0xffff,0xa5f8:w
m68k_019e74_end:
.org 0x19E7A
m68k_019e7a:
        rts
m68k_019e7a_end:
.org 0x19E7C
m68k_019e7c:
        cmpi.w #0xffff,0xff7026:l
m68k_019e7c_end:
.org 0x19E84
m68k_019e84:
        beq.w (. + 14)
m68k_019e84_end:
.org 0x19E88
m68k_019e88:
        move.w #0xc0,0xf600:w
m68k_019e88_end:
.org 0x19E8E
m68k_019e8e:
        bra.w (. + 50)
m68k_019e8e_end:
.org 0x19E92
m68k_019e92:
        addq.w #0x1,0xf362:w
m68k_019e92_end:
.org 0x19E96
m68k_019e96:
        move.w 0xf3f2:w,0xf3d0:w
m68k_019e96_end:
.org 0x19E9C
m68k_019e9c:
        move.w 0xf3a6:w,0xf3d2:w
m68k_019e9c_end:
.org 0x19EA2
m68k_019ea2:
        move.w 0xf6d4:w,%d0
m68k_019ea2_end:
.org 0x19EA6
m68k_019ea6:
        lsl.w #0x1,%d0
m68k_019ea6_end:
.org 0x19EA8
m68k_019ea8:
        lea.l 24(%pc),%a0
m68k_019ea8_end:
.org 0x19EAC
m68k_019eac:
        move.w (%a0, %d0.w),%d0
m68k_019eac_end:
.org 0x19EB0
m68k_019eb0:
        move.w %d0,0xaf80:w
m68k_019eb0_end:
.org 0x19EB4
m68k_019eb4:
        jsr 0x676f2:l
m68k_019eb4_end:
.org 0x19EBA
m68k_019eba:
        move.w #0x1,0xf652:w
m68k_019eba_end:
.org 0x19EC0
m68k_019ec0:
        rts
m68k_019ec0_end:
.org 0x19ECE
m68k_019ece:
        btst.b #0x5,0xf603:w
m68k_019ece_end:
.org 0x19ED4
m68k_019ed4:
        beq.w (. + 26)
m68k_019ed4_end:
.org 0x19ED8
m68k_019ed8:
        move.w #0x408,0xf612:w
m68k_019ed8_end:
.org 0x19EDE
m68k_019ede:
        clr.w 0xf362:w
m68k_019ede_end:
.org 0x19EE2
m68k_019ee2:
        move.w #0x1,0xf6f6:w
m68k_019ee2_end:
.org 0x19EE8
m68k_019ee8:
        move.w #0x1,0xf6d4:w
m68k_019ee8_end:
.org 0x19EEE
m68k_019eee:
        rts
m68k_019eee_end:
.org 0x1A47A
m68k_01a47a:
        move.w #0xffff,0xff7026:l
m68k_01a47a_end:
.org 0x1A482
m68k_01a482:
        move.w 0xf6d4:w,%d0
m68k_01a482_end:
.org 0x1A486
m68k_01a486:
        lsl.w #0x1,%d0
m68k_01a486_end:
.org 0x1A488
m68k_01a488:
        move.w 8(%pc, %d0.w),%d0
m68k_01a488_end:
.org 0x1A48C
m68k_01a48c:
        jsr 16(%pc, %d0.w)
m68k_01a48c_end:
.org 0x1A490
m68k_01a490:
        rts
m68k_01a490_end:
.org 0x1AF80
m68k_01af80:
        move.w 0xf6d4:w,%d0
m68k_01af80_end:
.org 0x1AF84
m68k_01af84:
        lsl.w #0x1,%d0
m68k_01af84_end:
.org 0x1AF86
m68k_01af86:
        move.w 24(%pc, %d0.w),%d0
m68k_01af86_end:
.org 0x1AF8A
m68k_01af8a:
        jsr 48(%pc, %d0.w)
m68k_01af8a_end:
.org 0x1AF8E
m68k_01af8e:
        move.w 0xf6d6:w,%d0
m68k_01af8e_end:
.org 0x1AF92
m68k_01af92:
        lsl.w #0x2,%d0
m68k_01af92_end:
.org 0x1AF94
m68k_01af94:
        movea.l 22(%pc, %d0.w),%a0
m68k_01af94_end:
.org 0x1AF98
m68k_01af98:
        move.l (%a0),%d0
m68k_01af98_end:
.org 0x1AF9A
m68k_01af9a:
        cmp.l 0xf39e:w,%d0
m68k_01af9a_end:
.org 0x1AF9E
m68k_01af9e:
        rts
m68k_01af9e_end:
.org 0x1AFBC
m68k_01afbc:
        jsr 0x83d4:l
m68k_01afbc_end:
.org 0x1AFC2
m68k_01afc2:
        andi.l #0xffff,%d0
m68k_01afc2_end:
.org 0x1AFC8
m68k_01afc8:
        move.l %d0,%d1
m68k_01afc8_end:
.org 0x1AFCA
m68k_01afca:
        lsl.l #0x2,%d0
m68k_01afca_end:
.org 0x1AFCC
m68k_01afcc:
        add.l %d1,%d0
m68k_01afcc_end:
.org 0x1AFCE
m68k_01afce:
        lsl.l #0x1,%d0
m68k_01afce_end:
.org 0x1AFD0
m68k_01afd0:
        add.l %d1,%d0
m68k_01afd0_end:
.org 0x1AFD2
m68k_01afd2:
        swap %d0
m68k_01afd2_end:
.org 0x1AFD4
m68k_01afd4:
        addi.w #0x14,%d0
m68k_01afd4_end:
.org 0x1AFD8
m68k_01afd8:
        lea.l 0xc800:w,%a0
m68k_01afd8_end:
.org 0x1AFDC
m68k_01afdc:
        move.w 0xf3a6:w,%d1
m68k_01afdc_end:
.org 0x1AFE0
m68k_01afe0:
        lsl.w #0x2,%d1
m68k_01afe0_end:
.org 0x1AFE2
m68k_01afe2:
        move.l (%a0, %d1.w),%d2
m68k_01afe2_end:
.org 0x1AFE6
m68k_01afe6:
        divu.w %d0,%d2
m68k_01afe6_end:
.org 0x1AFE8
m68k_01afe8:
        andi.l #0xffff,%d2
m68k_01afe8_end:
.org 0x1AFEE
m68k_01afee:
        move.l %d2,0xf39e:w
m68k_01afee_end:
.org 0x1AFF2
m68k_01aff2:
        rts
m68k_01aff2_end:
.org 0x1AFF4
m68k_01aff4:
        jsr 0x83d4:l
m68k_01aff4_end:
.org 0x1AFFA
m68k_01affa:
        andi.l #0xffff,%d0
m68k_01affa_end:
.org 0x1B000
m68k_01b000:
        move.l %d0,%d1
m68k_01b000_end:
.org 0x1B002
m68k_01b002:
        lsl.l #0x2,%d0
m68k_01b002_end:
.org 0x1B004
m68k_01b004:
        add.l %d1,%d0
m68k_01b004_end:
.org 0x1B006
m68k_01b006:
        lsl.l #0x1,%d0
m68k_01b006_end:
.org 0x1B008
m68k_01b008:
        add.l %d1,%d0
m68k_01b008_end:
.org 0x1B00A
m68k_01b00a:
        swap %d0
m68k_01b00a_end:
.org 0x1B00C
m68k_01b00c:
        addi.w #0x1e,%d0
m68k_01b00c_end:
.org 0x1B010
m68k_01b010:
        lea.l 0xc800:w,%a0
m68k_01b010_end:
.org 0x1B014
m68k_01b014:
        move.w 0xf3a6:w,%d1
m68k_01b014_end:
.org 0x1B018
m68k_01b018:
        lsl.w #0x2,%d1
m68k_01b018_end:
.org 0x1B01A
m68k_01b01a:
        move.l (%a0, %d1.w),%d2
m68k_01b01a_end:
.org 0x1B01E
m68k_01b01e:
        divu.w %d0,%d2
m68k_01b01e_end:
.org 0x1B020
m68k_01b020:
        andi.l #0xffff,%d2
m68k_01b020_end:
.org 0x1B026
m68k_01b026:
        move.l %d2,0xf39e:w
m68k_01b026_end:
.org 0x1B02A
m68k_01b02a:
        rts
m68k_01b02a_end:
.org 0x1B02C
m68k_01b02c:
        jsr 0x83d4:l
m68k_01b02c_end:
.org 0x1B032
m68k_01b032:
        andi.l #0xffff,%d0
m68k_01b032_end:
.org 0x1B038
m68k_01b038:
        move.l %d0,%d1
m68k_01b038_end:
.org 0x1B03A
m68k_01b03a:
        lsl.l #0x2,%d0
m68k_01b03a_end:
.org 0x1B03C
m68k_01b03c:
        add.l %d1,%d0
m68k_01b03c_end:
.org 0x1B03E
m68k_01b03e:
        lsl.l #0x1,%d0
m68k_01b03e_end:
.org 0x1B040
m68k_01b040:
        add.l %d1,%d0
m68k_01b040_end:
.org 0x1B042
m68k_01b042:
        swap %d0
m68k_01b042_end:
.org 0x1B044
m68k_01b044:
        addi.w #0x28,%d0
m68k_01b044_end:
.org 0x1B048
m68k_01b048:
        lea.l 0xc800:w,%a0
m68k_01b048_end:
.org 0x1B04C
m68k_01b04c:
        move.w 0xf3a6:w,%d1
m68k_01b04c_end:
.org 0x1B050
m68k_01b050:
        lsl.w #0x2,%d1
m68k_01b050_end:
.org 0x1B052
m68k_01b052:
        move.l (%a0, %d1.w),%d2
m68k_01b052_end:
.org 0x1B056
m68k_01b056:
        divu.w %d0,%d2
m68k_01b056_end:
.org 0x1B058
m68k_01b058:
        andi.l #0xffff,%d2
m68k_01b058_end:
.org 0x1B05E
m68k_01b05e:
        move.l %d2,0xf39e:w
m68k_01b05e_end:
.org 0x1B062
m68k_01b062:
        rts
m68k_01b062_end:
.org 0x1B064
m68k_01b064:
        move.w 0xf3a6:w,%d0
m68k_01b064_end:
.org 0x1B068
m68k_01b068:
        lsl.w #0x1,%d0
m68k_01b068_end:
.org 0x1B06A
m68k_01b06a:
        lea.l 0xb400:w,%a0
m68k_01b06a_end:
.org 0x1B06E
m68k_01b06e:
        move.w (%a0, %d0.w),%d2
m68k_01b06e_end:
.org 0x1B072
m68k_01b072:
        lea.l 0xb600:w,%a0
m68k_01b072_end:
.org 0x1B076
m68k_01b076:
        add.w (%a0, %d0.w),%d2
m68k_01b076_end:
.org 0x1B07A
m68k_01b07a:
        jsr 0x83d4:l
m68k_01b07a_end:
.org 0x1B080
m68k_01b080:
        andi.l #0xffff,%d0
m68k_01b080_end:
.org 0x1B086
m68k_01b086:
        move.l %d0,%d1
m68k_01b086_end:
.org 0x1B088
m68k_01b088:
        lsl.l #0x2,%d0
m68k_01b088_end:
.org 0x1B08A
m68k_01b08a:
        add.l %d1,%d0
m68k_01b08a_end:
.org 0x1B08C
m68k_01b08c:
        swap %d0
m68k_01b08c_end:
.org 0x1B08E
m68k_01b08e:
        addq.w #0x8,%d0
m68k_01b08e_end:
.org 0x1B090
m68k_01b090:
        mulu.w %d0,%d2
m68k_01b090_end:
.org 0x1B092
m68k_01b092:
        move.l %d2,0xf39e:w
m68k_01b092_end:
.org 0x1B096
m68k_01b096:
        rts
m68k_01b096_end:
