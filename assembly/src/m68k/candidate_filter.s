| 候选条件筛选。共享区域由 recovered_code.s 定义。
.cpu 68000
.section .text
_start:
.org 0x468
m68k_000468:
        bra.w (. + 2172)
m68k_000468_end:
.org 0xCE4
m68k_000ce4:
        jsr 0x17a9e:l
m68k_000ce4_end:
.org 0xCEA
m68k_000cea:
        rts
m68k_000cea_end:
.org 0x17A9E
m68k_017a9e:
        move.w #0x2700,%sr
m68k_017a9e_end:
.org 0x17AA2
m68k_017aa2:
        clr.w 0xaf80:w
m68k_017aa2_end:
.org 0x17AA6
m68k_017aa6:
        move.w 0xf3a6:w,%d0
m68k_017aa6_end:
.org 0x17AAA
m68k_017aaa:
        lea.l 0xc400:w,%a0
m68k_017aaa_end:
.org 0x17AAE
m68k_017aae:
        clr.w %d3
m68k_017aae_end:
.org 0x17AB0
m68k_017ab0:
        move.b (%a0, %d0.w),%d3
m68k_017ab0_end:
.org 0x17AB4
m68k_017ab4:
        move.w %d3,%d5
m68k_017ab4_end:
.org 0x17AB6
m68k_017ab6:
        lsl.w #0x3,%d3
m68k_017ab6_end:
.org 0x17AB8
m68k_017ab8:
        add.w %d5,%d3
m68k_017ab8_end:
.org 0x17ABA
m68k_017aba:
        lsl.w #0x2,%d0
m68k_017aba_end:
.org 0x17ABC
m68k_017abc:
        lea.l 0xa150:w,%a3
m68k_017abc_end:
.org 0x17AC0
m68k_017ac0:
        move.w (%a3, %d0.w),%d5
m68k_017ac0_end:
.org 0x17AC4
m68k_017ac4:
        lsr.w #0x7,%d5
m68k_017ac4_end:
.org 0x17AC6
m68k_017ac6:
        move.w 0x2(%a3, %d0.w),%d6
m68k_017ac6_end:
.org 0x17ACA
m68k_017aca:
        lsr.w #0x7,%d6
m68k_017aca_end:
.org 0x17ACC
m68k_017acc:
        lea.l 0x945e8:l,%a0
m68k_017acc_end:
.org 0x17AD2
m68k_017ad2:
        move.w 0xf68a:w,%d4
m68k_017ad2_end:
.org 0x17AD6
m68k_017ad6:
        mulu.w #0x8c0,%d4
m68k_017ad6_end:
.org 0x17ADA
m68k_017ada:
        adda.l %d4,%a0
m68k_017ada_end:
.org 0x17ADC
m68k_017adc:
        lea.l 0xa62c:w,%a4
m68k_017adc_end:
.org 0x17AE0
m68k_017ae0:
        cmpi.w #0x1,0xf6d4:w
m68k_017ae0_end:
.org 0x17AE6
m68k_017ae6:
        bne.w (. + 48)
m68k_017ae6_end:
.org 0x17AEA
m68k_017aea:
        move.w %d5,%d1
m68k_017aea_end:
.org 0x17AEC
m68k_017aec:
        move.w %d6,%d2
m68k_017aec_end:
.org 0x17AEE
m68k_017aee:
        jsr 0x1a44e:l
m68k_017aee_end:
.org 0x17AF4
m68k_017af4:
        cmpi.b #0x0,%d0
m68k_017af4_end:
.org 0x17AF8
m68k_017af8:
        beq.w (. + 30)
m68k_017af8_end:
.org 0x17AFC
m68k_017afc:
        cmpi.b #0x4,%d0
m68k_017afc_end:
.org 0x17B00
m68k_017b00:
        beq.w (. + 22)
m68k_017b00_end:
.org 0x17B04
m68k_017b04:
        cmpi.b #0x7,%d0
m68k_017b04_end:
.org 0x17B08
m68k_017b08:
        beq.w (. + 14)
m68k_017b08_end:
.org 0x17B0C
m68k_017b0c:
        move.w #0x137,0xaf80:w
m68k_017b0c_end:
.org 0x17B12
m68k_017b12:
        bra.w (. + 38)
m68k_017b12_end:
.org 0x17B16
m68k_017b16:
        btst.b #0x1,0xf6d7:w
m68k_017b16_end:
.org 0x17B1C
m68k_017b1c:
        bne.w (. + 12)
m68k_017b1c_end:
.org 0x17B20
m68k_017b20:
        lea.l 0xa5a4:w,%a1
m68k_017b20_end:
.org 0x17B24
m68k_017b24:
        bra.w (. + 8)
m68k_017b24_end:
.org 0x17B28
m68k_017b28:
        lea.l 0xa550:w,%a1
m68k_017b28_end:
.org 0x17B2C
m68k_017b2c:
        lea.l 0xff3bc2:l,%a5
m68k_017b2c_end:
.org 0x17B32
m68k_017b32:
        jsr 16(%pc)
m68k_017b32_end:
.org 0x17B36
m68k_017b36:
        nop
m68k_017b36_end:
.org 0x17B38
m68k_017b38:
        move.w #0xffff,(%a4)
m68k_017b38_end:
.org 0x17B3C
m68k_017b3c:
        jsr 0xaf48:l
m68k_017b3c_end:
.org 0x17B42
m68k_017b42:
        rts
m68k_017b42_end:
.org 0x17B44
m68k_017b44:
        move.w (%a1)+,%d4
m68k_017b44_end:
.org 0x17B46
m68k_017b46:
        bmi.w (. + 82)
m68k_017b46_end:
.org 0x17B4A
m68k_017b4a:
        tst.b (%a5, %d4.w)
m68k_017b4a_end:
.org 0x17B4E
m68k_017b4e:
        bne.b (. + -10)
m68k_017b4e_end:
.org 0x17B50
m68k_017b50:
        andi.w #0xff,%d4
m68k_017b50_end:
.org 0x17B54
m68k_017b54:
        lsl.w #0x2,%d4
m68k_017b54_end:
.org 0x17B56
m68k_017b56:
        move.w (%a3, %d4.w),%d1
m68k_017b56_end:
.org 0x17B5A
m68k_017b5a:
        lsr.w #0x7,%d1
m68k_017b5a_end:
.org 0x17B5C
m68k_017b5c:
        move.w 0x2(%a3, %d4.w),%d2
m68k_017b5c_end:
.org 0x17B60
m68k_017b60:
        lsr.w #0x7,%d2
m68k_017b60_end:
.org 0x17B62
m68k_017b62:
        lsr.w #0x2,%d4
m68k_017b62_end:
.org 0x17B64
m68k_017b64:
        bsr.w (. + 54)
m68k_017b64_end:
.org 0x17B68
m68k_017b68:
        bcs.b (. + -36)
m68k_017b68_end:
.org 0x17B6A
m68k_017b6a:
        sub.w %d5,%d1
m68k_017b6a_end:
.org 0x17B6C
m68k_017b6c:
        bcc.w (. + 6)
m68k_017b6c_end:
.org 0x17B70
m68k_017b70:
        neg.w %d1
m68k_017b70_end:
.org 0x17B72
m68k_017b72:
        cmp.w %d3,%d1
m68k_017b72_end:
.org 0x17B74
m68k_017b74:
        bhi.b (. + -48)
m68k_017b74_end:
.org 0x17B76
m68k_017b76:
        mulu.w %d1,%d1
m68k_017b76_end:
.org 0x17B78
m68k_017b78:
        sub.w %d6,%d2
m68k_017b78_end:
.org 0x17B7A
m68k_017b7a:
        bcc.w (. + 6)
m68k_017b7a_end:
.org 0x17B7E
m68k_017b7e:
        neg.w %d2
m68k_017b7e_end:
.org 0x17B80
m68k_017b80:
        cmp.w %d3,%d2
m68k_017b80_end:
.org 0x17B82
m68k_017b82:
        bhi.b (. + -62)
m68k_017b82_end:
.org 0x17B84
m68k_017b84:
        mulu.w %d2,%d2
m68k_017b84_end:
.org 0x17B86
m68k_017b86:
        add.l %d2,%d1
m68k_017b86_end:
.org 0x17B88
m68k_017b88:
        move.l %d1,%d0
m68k_017b88_end:
.org 0x17B8A
m68k_017b8a:
        jsr 0x3080e:l
m68k_017b8a_end:
.org 0x17B90
m68k_017b90:
        cmp.w %d3,%d0
m68k_017b90_end:
.org 0x17B92
m68k_017b92:
        bhi.b (. + -78)
m68k_017b92_end:
.org 0x17B94
m68k_017b94:
        move.w %d4,(%a4)+
m68k_017b94_end:
.org 0x17B96
m68k_017b96:
        bra.b (. + -82)
m68k_017b96_end:
.org 0x17B98
m68k_017b98:
        rts
m68k_017b98_end:
.org 0x17B9A
m68k_017b9a:
        movem.l %d5-%d6,-(%a7)
m68k_017b9a_end:
.org 0x17B9E
m68k_017b9e:
        move.w 0xf6d4:w,%d7
m68k_017b9e_end:
.org 0x17BA2
m68k_017ba2:
        lsl.w #0x1,%d7
m68k_017ba2_end:
.org 0x17BA4
m68k_017ba4:
        move.w 12(%pc, %d7.w),%d7
m68k_017ba4_end:
.org 0x17BA8
m68k_017ba8:
        jsr 70(%pc, %d7.w)
m68k_017ba8_end:
.org 0x17BAC
m68k_017bac:
        movem.l (%a7)+,%d5-%d6
m68k_017bac_end:
.org 0x17BB0
m68k_017bb0:
        rts
m68k_017bb0_end:
.org 0x17BBE
m68k_017bbe:
        jsr 0x1a44e:l
m68k_017bbe_end:
.org 0x17BC4
m68k_017bc4:
        cmpi.b #0x0,%d0
m68k_017bc4_end:
.org 0x17BC8
m68k_017bc8:
        beq.b (. + 34)
m68k_017bc8_end:
.org 0x17BCA
m68k_017bca:
        cmpi.b #0x3,%d0
m68k_017bca_end:
.org 0x17BCE
m68k_017bce:
        beq.w (. + 28)
m68k_017bce_end:
.org 0x17BD2
m68k_017bd2:
        cmpi.b #0x7,%d0
m68k_017bd2_end:
.org 0x17BD6
m68k_017bd6:
        beq.w (. + 20)
m68k_017bd6_end:
.org 0x17BDA
m68k_017bda:
        cmpi.b #0x1,%d0
m68k_017bda_end:
.org 0x17BDE
m68k_017bde:
        beq.w (. + 12)
m68k_017bde_end:
.org 0x17BE2
m68k_017be2:
        ori.w #0x1,%sr
m68k_017be2_end:
.org 0x17BE6
m68k_017be6:
        bra.w (. + 8)
m68k_017be6_end:
.org 0x17BEA
m68k_017bea:
        andi.w #0xfffe,%sr
m68k_017bea_end:
.org 0x17BEE
m68k_017bee:
        rts
m68k_017bee_end:
.org 0x17BF0
m68k_017bf0:
        jsr 0x1a44e:l
m68k_017bf0_end:
.org 0x17BF6
m68k_017bf6:
        cmpi.b #0x0,%d0
m68k_017bf6_end:
.org 0x17BFA
m68k_017bfa:
        beq.b (. + 26)
m68k_017bfa_end:
.org 0x17BFC
m68k_017bfc:
        cmpi.b #0x3,%d0
m68k_017bfc_end:
.org 0x17C00
m68k_017c00:
        beq.w (. + 20)
m68k_017c00_end:
.org 0x17C04
m68k_017c04:
        cmpi.b #0x7,%d0
m68k_017c04_end:
.org 0x17C08
m68k_017c08:
        beq.w (. + 12)
m68k_017c08_end:
.org 0x17C0C
m68k_017c0c:
        ori.w #0x1,%sr
m68k_017c0c_end:
.org 0x17C10
m68k_017c10:
        bra.w (. + 8)
m68k_017c10_end:
.org 0x17C14
m68k_017c14:
        andi.w #0xfffe,%sr
m68k_017c14_end:
.org 0x17C18
m68k_017c18:
        rts
m68k_017c18_end:
.org 0x17C1A
m68k_017c1a:
        jsr 0x1a44e:l
m68k_017c1a_end:
.org 0x17C20
m68k_017c20:
        cmpi.b #0x2,%d0
m68k_017c20_end:
.org 0x17C24
m68k_017c24:
        beq.w (. + 12)
m68k_017c24_end:
.org 0x17C28
m68k_017c28:
        ori.w #0x1,%sr
m68k_017c28_end:
.org 0x17C2C
m68k_017c2c:
        bra.w (. + 8)
m68k_017c2c_end:
.org 0x17C30
m68k_017c30:
        andi.w #0xfffe,%sr
m68k_017c30_end:
.org 0x17C34
m68k_017c34:
        rts
m68k_017c34_end:
.org 0x17C36
m68k_017c36:
        andi.w #0xfffe,%sr
m68k_017c36_end:
.org 0x17C3A
m68k_017c3a:
        rts
m68k_017c3a_end:
.org 0x17C3C
m68k_017c3c:
        jsr 0x1a44e:l
m68k_017c3c_end:
.org 0x17C42
m68k_017c42:
        cmpi.b #0x1,%d0
m68k_017c42_end:
.org 0x17C46
m68k_017c46:
        beq.b (. + 10)
m68k_017c46_end:
.org 0x17C48
m68k_017c48:
        ori.w #0x1,%sr
m68k_017c48_end:
.org 0x17C4C
m68k_017c4c:
        bra.w (. + 8)
m68k_017c4c_end:
.org 0x17C50
m68k_017c50:
        andi.w #0xfffe,%sr
m68k_017c50_end:
.org 0x17C54
m68k_017c54:
        rts
m68k_017c54_end:
.org 0x17C56
m68k_017c56:
        jsr 0x1a44e:l
m68k_017c56_end:
.org 0x17C5C
m68k_017c5c:
        cmpi.b #0x7,%d0
m68k_017c5c_end:
.org 0x17C60
m68k_017c60:
        beq.w (. + 12)
m68k_017c60_end:
.org 0x17C64
m68k_017c64:
        cmpi.b #0x6,%d0
m68k_017c64_end:
.org 0x17C68
m68k_017c68:
        bne.w (. + 12)
m68k_017c68_end:
.org 0x17C6C
m68k_017c6c:
        ori.w #0x1,%sr
m68k_017c6c_end:
.org 0x17C70
m68k_017c70:
        bra.w (. + 8)
m68k_017c70_end:
.org 0x17C74
m68k_017c74:
        andi.w #0xfffe,%sr
m68k_017c74_end:
.org 0x17C78
m68k_017c78:
        rts
m68k_017c78_end:
.org 0x1A44E
m68k_01a44e:
        movem.l %d1-%d3/%a0,-(%a7)
m68k_01a44e_end:
.org 0x1A452
m68k_01a452:
        lsr.w #0x3,%d1
m68k_01a452_end:
.org 0x1A454
m68k_01a454:
        move.w %d1,%d3
m68k_01a454_end:
.org 0x1A456
m68k_01a456:
        lsl.w #0x2,%d1
m68k_01a456_end:
.org 0x1A458
m68k_01a458:
        add.w %d3,%d1
m68k_01a458_end:
.org 0x1A45A
m68k_01a45a:
        lsl.w #0x3,%d1
m68k_01a45a_end:
.org 0x1A45C
m68k_01a45c:
        lsr.w #0x3,%d2
m68k_01a45c_end:
.org 0x1A45E
m68k_01a45e:
        add.w %d2,%d1
m68k_01a45e_end:
.org 0x1A460
m68k_01a460:
        lsl.w #0x1,%d1
m68k_01a460_end:
.org 0x1A462
m68k_01a462:
        move.w (%a0, %d1.w),%d0
m68k_01a462_end:
.org 0x1A466
m68k_01a466:
        andi.w #0x3ff,%d0
m68k_01a466_end:
.org 0x1A46A
m68k_01a46a:
        lea.l 0x6c0b4:l,%a0
m68k_01a46a_end:
.org 0x1A470
m68k_01a470:
        move.b (%a0, %d0.w),%d0
m68k_01a470_end:
.org 0x1A474
m68k_01a474:
        movem.l (%a7)+,%d1-%d3/%a0
m68k_01a474_end:
.org 0x1A478
m68k_01a478:
        rts
m68k_01a478_end:
.org 0x3080E
m68k_03080e:
        movem.l %d1-%d3/%a0,-(%a7)
m68k_03080e_end:
.org 0x30812
m68k_030812:
        tst.l %d0
m68k_030812_end:
.org 0x30814
m68k_030814:
        beq.w (. + 22)
m68k_030814_end:
.org 0x30818
m68k_030818:
        bsr.w (. + 24)
m68k_030818_end:
.org 0x3081C
m68k_03081c:
        sub.l %d2,%d0
m68k_03081c_end:
.org 0x3081E
m68k_03081e:
        bcs.w (. + 10)
m68k_03081e_end:
.org 0x30822
m68k_030822:
        addq.w #0x1,%d1
m68k_030822_end:
.org 0x30824
m68k_030824:
        addq.w #0x2,%d2
m68k_030824_end:
.org 0x30826
m68k_030826:
        bra.b (. + -10)
m68k_030826_end:
.org 0x30828
m68k_030828:
        move.w %d1,%d0
m68k_030828_end:
.org 0x3082A
m68k_03082a:
        movem.l (%a7)+,%d1-%d3/%a0
m68k_03082a_end:
.org 0x3082E
m68k_03082e:
        rts
m68k_03082e_end:
.org 0x30830
m68k_030830:
        cmpi.l #0x2358d,%d0
m68k_030830_end:
.org 0x30836
m68k_030836:
        bcs.b (. + 22)
m68k_030836_end:
.org 0x30838
m68k_030838:
        subi.l #0x2358d,%d0
m68k_030838_end:
.org 0x3083E
m68k_03083e:
        move.l #0x2fa,%d2
m68k_03083e_end:
.org 0x30844
m68k_030844:
        move.w #0x17d,%d1
m68k_030844_end:
.org 0x30848
m68k_030848:
        bra.w (. + 44)
m68k_030848_end:
.org 0x3084C
m68k_03084c:
        clr.w %d1
m68k_03084c_end:
.org 0x3084E
m68k_03084e:
        moveq #1,%d2
m68k_03084e_end:
.org 0x30850
m68k_030850:
        clr.w %d3
m68k_030850_end:
.org 0x30852
m68k_030852:
        lea.l 34(%pc),%a0
m68k_030852_end:
.org 0x30856
m68k_030856:
        cmp.l (%a0),%d0
m68k_030856_end:
.org 0x30858
m68k_030858:
        bcs.w (. + 8)
m68k_030858_end:
.org 0x3085C
m68k_03085c:
        addq.l #0x6,%a0
m68k_03085c_end:
.org 0x3085E
m68k_03085e:
        bra.b (. + -8)
m68k_03085e_end:
.org 0x30860
m68k_030860:
        move.l -0x6(%a0),%d3
m68k_030860_end:
.org 0x30864
m68k_030864:
        move.w -0x2(%a0),%d2
m68k_030864_end:
.org 0x30868
m68k_030868:
        sub.l %d3,%d0
m68k_030868_end:
.org 0x3086A
m68k_03086a:
        move.w %d2,%d1
m68k_03086a_end:
.org 0x3086C
m68k_03086c:
        lsr.w #0x1,%d1
m68k_03086c_end:
.org 0x3086E
m68k_03086e:
        andi.l #0xffff,%d2
m68k_03086e_end:
.org 0x30874
m68k_030874:
        rts
m68k_030874_end:
