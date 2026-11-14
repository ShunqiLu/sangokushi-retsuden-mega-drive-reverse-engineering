| 二级命令分派例程。E068 表用有符号偏移选择分支目标。
.cpu 68000
.section .text
_start:
.org 0x103EA
m68k_0103ea:
        lea.l 0xf500:w,%a0
m68k_0103ea_end:
.org 0x103EE
m68k_0103ee:
        lea.l 0xcc00:w,%a1
m68k_0103ee_end:
.org 0x103F2
m68k_0103f2:
        move.w 0xf392:w,%d0
m68k_0103f2_end:
.org 0x103F6
m68k_0103f6:
        lea.l 0xf427:w,%a2
m68k_0103f6_end:
.org 0x103FA
m68k_0103fa:
        clr.w %d1
m68k_0103fa_end:
.org 0x103FC
m68k_0103fc:
        move.b (%a2, %d0.w),%d1
m68k_0103fc_end:
.org 0x10400
m68k_010400:
        lsl.w #0x1,%d1
m68k_010400_end:
.org 0x10402
m68k_010402:
        lea.l 0xe640:w,%a2
m68k_010402_end:
.org 0x10406
m68k_010406:
        move.w (%a2, %d1.w),%d2
m68k_010406_end:
.org 0x1040A
m68k_01040a:
        movea.l 0xff382c:l,%a2
m68k_01040a_end:
.org 0x10410
m68k_010410:
        move.b (%a2),%d3
m68k_010410_end:
.org 0x10412
m68k_010412:
        andi.w #0xf,%d3
m68k_010412_end:
.org 0x10416
m68k_010416:
        lea.l 0xd(%a2, %d3.w),%a3
m68k_010416_end:
.org 0x1041A
m68k_01041a:
        adda.w #0xd,%a2
m68k_01041a_end:
.org 0x1041E
m68k_01041e:
        clr.w %d5
m68k_01041e_end:
.org 0x10420
m68k_010420:
        clr.w %d6
m68k_010420_end:
.org 0x10422
m68k_010422:
        lea.l 0xff398a:l,%a5
m68k_010422_end:
.org 0x10428
m68k_010428:
        lea.l 0xff399e:l,%a6
m68k_010428_end:
.org 0x1042E
m68k_01042e:
        move.w (%a0)+,%d1
m68k_01042e_end:
.org 0x10430
m68k_010430:
        bmi.b (. + 50)
m68k_010430_end:
.org 0x10432
m68k_010432:
        cmpi.w #0x4000,%d1
m68k_010432_end:
.org 0x10436
m68k_010436:
        bcs.b (. + 32)
m68k_010436_end:
.org 0x10438
m68k_010438:
        andi.w #0xff,%d1
m68k_010438_end:
.org 0x1043C
m68k_01043c:
        move.b %d0,(%a1, %d1.w)
m68k_01043c_end:
.org 0x10440
m68k_010440:
        move.w %d1,(%a6)+
m68k_010440_end:
.org 0x10442
m68k_010442:
        addq.w #0x1,%d6
m68k_010442_end:
.org 0x10444
m68k_010444:
        cmp.w %d2,%d1
m68k_010444_end:
.org 0x10446
m68k_010446:
        bne.b (. + -24)
m68k_010446_end:
.org 0x10448
m68k_010448:
        lea.l 0xf45e:w,%a4
m68k_010448_end:
.org 0x1044C
m68k_01044c:
        move.w %d0,%d4
m68k_01044c_end:
.org 0x1044E
m68k_01044e:
        lsl.w #0x1,%d4
m68k_01044e_end:
.org 0x10450
m68k_010450:
        move.w %d2,(%a4, %d4.w)
m68k_010450_end:
.org 0x10454
m68k_010454:
        bra.b (. + -38)
m68k_010454_end:
.org 0x10456
m68k_010456:
        andi.w #0xff,%d1
m68k_010456_end:
.org 0x1045A
m68k_01045a:
        move.b %d1,(%a2)+
m68k_01045a_end:
.org 0x1045C
m68k_01045c:
        move.w %d1,(%a5)+
m68k_01045c_end:
.org 0x1045E
m68k_01045e:
        addq.w #0x1,%d5
m68k_01045e_end:
.org 0x10460
m68k_010460:
        bra.b (. + -50)
m68k_010460_end:
.org 0x10462
m68k_010462:
        move.w #0xffff,(%a5)
m68k_010462_end:
.org 0x10466
m68k_010466:
        move.w #0xffff,(%a6)
m68k_010466_end:
.org 0x1046A
m68k_01046a:
        movea.l 0xff382c:l,%a4
m68k_01046a_end:
.org 0x10470
m68k_010470:
        move.b %d5,(%a4)
m68k_010470_end:
.org 0x10472
m68k_010472:
        move.b (%a3),%d0
m68k_010472_end:
.org 0x10474
m68k_010474:
        andi.w #0xf,%d0
m68k_010474_end:
.org 0x10478
m68k_010478:
        beq.b (. + 14)
m68k_010478_end:
.org 0x1047A
m68k_01047a:
        addi.w #0xc,%d0
m68k_01047a_end:
.org 0x1047E
m68k_01047e:
        move.b (%a3)+,(%a2)+
m68k_01047e_end:
.org 0x10480
m68k_010480:
        dbra %d0,(. + -2)
m68k_010480_end:
.org 0x10484
m68k_010484:
        bra.b (. + -18)
m68k_010484_end:
.org 0x10486
m68k_010486:
        clr.b (%a2)
m68k_010486_end:
.org 0x10488
m68k_010488:
        move.w %d5,%d0
m68k_010488_end:
.org 0x1048A
m68k_01048a:
        bsr.w (. + -658)
m68k_01048a_end:
.org 0x1048E
m68k_01048e:
        move.w %d2,-(%a7)
m68k_01048e_end:
.org 0x10490
m68k_010490:
        bsr.w (. + 252)
m68k_010490_end:
.org 0x10494
m68k_010494:
        move.w (%a7)+,%d2
m68k_010494_end:
.org 0x10496
m68k_010496:
        movea.l 0xff382c:l,%a4
m68k_010496_end:
.org 0x1049C
m68k_01049c:
        move.b %d2,0x3(%a4)
m68k_01049c_end:
.org 0x104A0
m68k_0104a0:
        move.w #0xffff,0xf630:w
m68k_0104a0_end:
.org 0x104A6
m68k_0104a6:
        lea.l 0xf428:w,%a6
m68k_0104a6_end:
.org 0x104AA
m68k_0104aa:
        move.w #0x27,%d7
m68k_0104aa_end:
.org 0x104AE
m68k_0104ae:
        move.b (%a6, %d7.w),%d6
m68k_0104ae_end:
.org 0x104B2
m68k_0104b2:
        cmp.b 0xf377:w,%d6
m68k_0104b2_end:
.org 0x104B6
m68k_0104b6:
        bne.b (. + 20)
m68k_0104b6_end:
.org 0x104B8
m68k_0104b8:
        move.w %d7,%d0
m68k_0104b8_end:
.org 0x104BA
m68k_0104ba:
        addq.w #0x1,%d0
m68k_0104ba_end:
.org 0x104BC
m68k_0104bc:
        jsr 0x5f48:l
m68k_0104bc_end:
.org 0x104C2
m68k_0104c2:
        cmpi.w #0xa,%d3
m68k_0104c2_end:
.org 0x104C6
m68k_0104c6:
        bcs.w (. + 156)
m68k_0104c6_end:
.org 0x104CA
m68k_0104ca:
        dbra %d7,(. + -28)
m68k_0104ca_end:
.org 0x104CE
m68k_0104ce:
        movea.l 0xff382c:l,%a0
m68k_0104ce_end:
.org 0x104D4
m68k_0104d4:
        lea.l 0xd(%a0),%a1
m68k_0104d4_end:
.org 0x104D8
m68k_0104d8:
        move.b (%a0),%d0
m68k_0104d8_end:
.org 0x104DA
m68k_0104da:
        andi.w #0xf,%d0
m68k_0104da_end:
.org 0x104DE
m68k_0104de:
        subq.w #0x1,%d0
m68k_0104de_end:
.org 0x104E0
m68k_0104e0:
        move.w 0xf392:w,%d1
m68k_0104e0_end:
.org 0x104E4
m68k_0104e4:
        ori.b #0x80,%d1
m68k_0104e4_end:
.org 0x104E8
m68k_0104e8:
        clr.w %d2
m68k_0104e8_end:
.org 0x104EA
m68k_0104ea:
        lea.l 0xcc00:w,%a2
m68k_0104ea_end:
.org 0x104EE
m68k_0104ee:
        move.b (%a1)+,%d2
m68k_0104ee_end:
.org 0x104F0
m68k_0104f0:
        move.b %d1,(%a2, %d2.w)
m68k_0104f0_end:
.org 0x104F4
m68k_0104f4:
        dbra %d0,(. + -6)
m68k_0104f4_end:
.org 0x104F8
m68k_0104f8:
        move.b (%a1),%d0
m68k_0104f8_end:
.org 0x104FA
m68k_0104fa:
        andi.w #0xf,%d0
m68k_0104fa_end:
.org 0x104FE
m68k_0104fe:
        beq.b (. + 14)
m68k_0104fe_end:
.org 0x10500
m68k_010500:
        addi.w #0xc,%d0
m68k_010500_end:
.org 0x10504
m68k_010504:
        move.b (%a1)+,(%a0)+
m68k_010504_end:
.org 0x10506
m68k_010506:
        dbra %d0,(. + -2)
m68k_010506_end:
.org 0x1050A
m68k_01050a:
        bra.b (. + -18)
m68k_01050a_end:
.org 0x1050C
m68k_01050c:
        clr.b (%a0)
m68k_01050c_end:
.org 0x1050E
m68k_01050e:
        move.w 0xff398a:l,%d0
m68k_01050e_end:
.org 0x10514
m68k_010514:
        bmi.w (. + 48)
m68k_010514_end:
.org 0x10518
m68k_010518:
        andi.w #0xff,%d0
m68k_010518_end:
.org 0x1051C
m68k_01051c:
        move.w %d0,0xf3d0:w
m68k_01051c_end:
.org 0x10520
m68k_010520:
        move.w #0x9b,0xf740:w
m68k_010520_end:
.org 0x10526
m68k_010526:
        clr.w 0xf362:w
m68k_010526_end:
.org 0x1052A
m68k_01052a:
        move.w #0x12c,0xf608:w
m68k_01052a_end:
.org 0x10530
m68k_010530:
        jsr 0x30a74:l
m68k_010530_end:
.org 0x10536
m68k_010536:
        lea.l 0xff398a:l,%a0
m68k_010536_end:
.org 0x1053C
m68k_01053c:
        move.w 0x2(%a0),(%a0)+
m68k_01053c_end:
.org 0x10540
m68k_010540:
        bpl.b (. + -4)
m68k_010540_end:
.org 0x10542
m68k_010542:
        bra.b (. + -52)
m68k_010542_end:
.org 0x10544
m68k_010544:
        move.l #0xc0000026,%d0
m68k_010544_end:
.org 0x1054A
m68k_01054a:
        move.w #0x7,%d1
m68k_01054a_end:
.org 0x1054E
m68k_01054e:
        move.w #0xca02,%d2
m68k_01054e_end:
.org 0x10552
m68k_010552:
        lea.l 28(%pc),%a0
m68k_010552_end:
.org 0x10556
m68k_010556:
        jsr 0x26bfa:l
m68k_010556_end:
.org 0x1055C
m68k_01055c:
        bclr.b #0x6,0xf3a4:w
m68k_01055c_end:
.org 0x10562
m68k_010562:
        move.w #0x209,0xf612:w
m68k_010562_end:
.org 0x10568
m68k_010568:
        move.w #0x5,0xf362:w
m68k_010568_end:
.org 0x1056E
m68k_01056e:
        rts
m68k_01056e_end:
.org 0x1058C
m68k_01058c:
        lea.l 0xc800:w,%a4
m68k_01058c_end:
.org 0x10590
m68k_010590:
        lea.l 0xff398a:l,%a5
m68k_010590_end:
.org 0x10596
m68k_010596:
        moveq #0,%d0
m68k_010596_end:
.org 0x10598
m68k_010598:
        move.w (%a5)+,%d1
m68k_010598_end:
.org 0x1059A
m68k_01059a:
        bmi.b (. + 20)
m68k_01059a_end:
.org 0x1059C
m68k_01059c:
        lsl.w #0x2,%d1
m68k_01059c_end:
.org 0x1059E
m68k_01059e:
        move.l (%a4, %d1.w),%d1
m68k_01059e_end:
.org 0x105A2
m68k_0105a2:
        lsr.l #0x5,%d1
m68k_0105a2_end:
.org 0x105A4
m68k_0105a4:
        add.l %d1,%d0
m68k_0105a4_end:
.org 0x105A6
m68k_0105a6:
        addi.l #0x64,%d0
m68k_0105a6_end:
.org 0x105AC
m68k_0105ac:
        bra.b (. + -20)
m68k_0105ac_end:
.org 0x105AE
m68k_0105ae:
        move.l %d0,%d1
m68k_0105ae_end:
.org 0x105B0
m68k_0105b0:
        lea.l 0xff399e:l,%a6
m68k_0105b0_end:
.org 0x105B6
m68k_0105b6:
        move.w (%a6)+,%d2
m68k_0105b6_end:
.org 0x105B8
m68k_0105b8:
        bmi.b (. + 20)
m68k_0105b8_end:
.org 0x105BA
m68k_0105ba:
        lsl.w #0x2,%d2
m68k_0105ba_end:
.org 0x105BC
m68k_0105bc:
        move.l (%a4, %d2.w),%d2
m68k_0105bc_end:
.org 0x105C0
m68k_0105c0:
        lsr.l #0x5,%d2
m68k_0105c0_end:
.org 0x105C2
m68k_0105c2:
        add.l %d2,%d1
m68k_0105c2_end:
.org 0x105C4
m68k_0105c4:
        addi.l #0x64,%d1
m68k_0105c4_end:
.org 0x105CA
m68k_0105ca:
        bra.b (. + -20)
m68k_0105ca_end:
.org 0x105CC
m68k_0105cc:
        movea.l 0xff382c:l,%a5
m68k_0105cc_end:
.org 0x105D2
m68k_0105d2:
        move.b 0x5(%a5),%d2
m68k_0105d2_end:
.org 0x105D6
m68k_0105d6:
        lsl.w #0x8,%d2
m68k_0105d6_end:
.org 0x105D8
m68k_0105d8:
        move.b 0x6(%a5),%d2
m68k_0105d8_end:
.org 0x105DC
m68k_0105dc:
        lsl.l #0x8,%d2
m68k_0105dc_end:
.org 0x105DE
m68k_0105de:
        move.b 0x7(%a5),%d2
m68k_0105de_end:
.org 0x105E2
m68k_0105e2:
        lsl.l #0x8,%d2
m68k_0105e2_end:
.org 0x105E4
m68k_0105e4:
        move.b 0x8(%a5),%d2
m68k_0105e4_end:
.org 0x105E8
m68k_0105e8:
        move.l %d2,%d3
m68k_0105e8_end:
.org 0x105EA
m68k_0105ea:
        lsr.l #0x8,%d3
m68k_0105ea_end:
.org 0x105EC
m68k_0105ec:
        mulu.w %d0,%d3
m68k_0105ec_end:
.org 0x105EE
m68k_0105ee:
        divu.w %d1,%d3
m68k_0105ee_end:
.org 0x105F0
m68k_0105f0:
        andi.l #0xffff,%d3
m68k_0105f0_end:
.org 0x105F6
m68k_0105f6:
        lsl.l #0x8,%d3
m68k_0105f6_end:
.org 0x105F8
m68k_0105f8:
        sub.l %d3,%d2
m68k_0105f8_end:
.org 0x105FA
m68k_0105fa:
        move.b %d3,0x8(%a5)
m68k_0105fa_end:
.org 0x105FE
m68k_0105fe:
        lsr.l #0x8,%d3
m68k_0105fe_end:
.org 0x10600
m68k_010600:
        move.b %d3,0x7(%a5)
m68k_010600_end:
.org 0x10604
m68k_010604:
        lsr.l #0x8,%d3
m68k_010604_end:
.org 0x10606
m68k_010606:
        move.b %d3,0x6(%a5)
m68k_010606_end:
.org 0x1060A
m68k_01060a:
        lsr.w #0x8,%d3
m68k_01060a_end:
.org 0x1060C
m68k_01060c:
        move.b %d3,0x5(%a5)
m68k_01060c_end:
.org 0x10610
m68k_010610:
        move.w 0xf364:w,%d4
m68k_010610_end:
.org 0x10614
m68k_010614:
        lsl.w #0x2,%d4
m68k_010614_end:
.org 0x10616
m68k_010616:
        lea.l 0xdffc:w,%a6
m68k_010616_end:
.org 0x1061A
m68k_01061a:
        move.l (%a6, %d4.w),%d3
m68k_01061a_end:
.org 0x1061E
m68k_01061e:
        add.l %d2,%d3
m68k_01061e_end:
.org 0x10620
m68k_010620:
        cmpi.l #0xf423f,%d3
m68k_010620_end:
.org 0x10626
m68k_010626:
        bls.b (. + 8)
m68k_010626_end:
.org 0x10628
m68k_010628:
        move.l #0xf423f,%d3
m68k_010628_end:
.org 0x1062E
m68k_01062e:
        move.l %d3,(%a6, %d4.w)
m68k_01062e_end:
.org 0x10632
m68k_010632:
        movea.l 0xff382c:l,%a5
m68k_010632_end:
.org 0x10638
m68k_010638:
        move.b 0x9(%a5),%d2
m68k_010638_end:
.org 0x1063C
m68k_01063c:
        lsl.w #0x8,%d2
m68k_01063c_end:
.org 0x1063E
m68k_01063e:
        move.b 0xa(%a5),%d2
m68k_01063e_end:
.org 0x10642
m68k_010642:
        lsl.l #0x8,%d2
m68k_010642_end:
.org 0x10644
m68k_010644:
        move.b 0xb(%a5),%d2
m68k_010644_end:
.org 0x10648
m68k_010648:
        lsl.l #0x8,%d2
m68k_010648_end:
.org 0x1064A
m68k_01064a:
        move.b 0xc(%a5),%d2
m68k_01064a_end:
.org 0x1064E
m68k_01064e:
        move.l %d2,%d3
m68k_01064e_end:
.org 0x10650
m68k_010650:
        lsr.l #0x8,%d3
m68k_010650_end:
.org 0x10652
m68k_010652:
        mulu.w %d0,%d3
m68k_010652_end:
.org 0x10654
m68k_010654:
        divu.w %d1,%d3
m68k_010654_end:
.org 0x10656
m68k_010656:
        andi.l #0xffff,%d3
m68k_010656_end:
.org 0x1065C
m68k_01065c:
        lsl.l #0x8,%d3
m68k_01065c_end:
.org 0x1065E
m68k_01065e:
        sub.l %d3,%d2
m68k_01065e_end:
.org 0x10660
m68k_010660:
        move.b %d3,0xc(%a5)
m68k_010660_end:
.org 0x10664
m68k_010664:
        lsr.l #0x8,%d3
m68k_010664_end:
.org 0x10666
m68k_010666:
        move.b %d3,0xb(%a5)
m68k_010666_end:
.org 0x1066A
m68k_01066a:
        lsr.l #0x8,%d3
m68k_01066a_end:
.org 0x1066C
m68k_01066c:
        move.b %d3,0xa(%a5)
m68k_01066c_end:
.org 0x10670
m68k_010670:
        lsr.w #0x8,%d3
m68k_010670_end:
.org 0x10672
m68k_010672:
        move.b %d3,0x9(%a5)
m68k_010672_end:
.org 0x10676
m68k_010676:
        lea.l 0xe09c:w,%a6
m68k_010676_end:
.org 0x1067A
m68k_01067a:
        move.l (%a6, %d4.w),%d3
m68k_01067a_end:
.org 0x1067E
m68k_01067e:
        add.l %d2,%d3
m68k_01067e_end:
.org 0x10680
m68k_010680:
        cmpi.l #0xf423f,%d3
m68k_010680_end:
.org 0x10686
m68k_010686:
        bls.b (. + 8)
m68k_010686_end:
.org 0x10688
m68k_010688:
        move.l #0xf423f,%d3
m68k_010688_end:
.org 0x1068E
m68k_01068e:
        move.l %d3,(%a6, %d4.w)
m68k_01068e_end:
.org 0x10692
m68k_010692:
        rts
m68k_010692_end:
.org 0x10694
m68k_010694:
        move.w 0xefb0:w,%d0
m68k_010694_end:
.org 0x10698
m68k_010698:
        lsl.w #0x1,%d0
m68k_010698_end:
.org 0x1069A
m68k_01069a:
        lea.l 0xe640:w,%a0
m68k_01069a_end:
.org 0x1069E
m68k_01069e:
        move.w (%a0, %d0.w),%d2
m68k_01069e_end:
.org 0x106A2
m68k_0106a2:
        move.w 0xf3a6:w,%d1
m68k_0106a2_end:
.org 0x106A6
m68k_0106a6:
        move.w %d1,(%a0, %d0.w)
m68k_0106a6_end:
.org 0x106AA
m68k_0106aa:
        lea.l 0xc300:w,%a0
m68k_0106aa_end:
.org 0x106AE
m68k_0106ae:
        move.b #0x64,(%a0, %d1.w)
m68k_0106ae_end:
.org 0x106B4
m68k_0106b4:
        clr.w 0xa622:w
m68k_0106b4_end:
.org 0x106B8
m68k_0106b8:
        move.w #0x201,0xf3da:w
m68k_0106b8_end:
.org 0x106BE
m68k_0106be:
        bsr.w (. + 38)
m68k_0106be_end:
.org 0x106C2
m68k_0106c2:
        move.w #0x20c,0xf612:w
m68k_0106c2_end:
.org 0x106C8
m68k_0106c8:
        move.w #0xa,0xf362:w
m68k_0106c8_end:
.org 0x106CE
m68k_0106ce:
        move.w 0xf3a6:w,0xf3d0:w
m68k_0106ce_end:
.org 0x106D4
m68k_0106d4:
        move.w #0x9a,%d0
m68k_0106d4_end:
.org 0x106D8
m68k_0106d8:
        jsr 0x676f2:l
m68k_0106d8_end:
.org 0x106DE
m68k_0106de:
        clr.w 0xf65a:w
m68k_0106de_end:
.org 0x106E2
m68k_0106e2:
        rts
m68k_0106e2_end:
.org 0x106E4
m68k_0106e4:
        lea.l 0xcc00:w,%a0
m68k_0106e4_end:
.org 0x106E8
m68k_0106e8:
        clr.w %d0
m68k_0106e8_end:
.org 0x106EA
m68k_0106ea:
        move.b (%a0, %d2.w),%d0
m68k_0106ea_end:
.org 0x106EE
m68k_0106ee:
        cmp.b (%a0, %d1.w),%d0
m68k_0106ee_end:
.org 0x106F2
m68k_0106f2:
        beq.w (. + 28)
m68k_0106f2_end:
.org 0x106F6
m68k_0106f6:
        btst.l #0x6,%d0
m68k_0106f6_end:
.org 0x106FA
m68k_0106fa:
        bne.w (. + 20)
m68k_0106fa_end:
.org 0x106FE
m68k_0106fe:
        move.w #0xffff,0xf630:w
m68k_0106fe_end:
.org 0x10704
m68k_010704:
        jsr 0x5f48:l
m68k_010704_end:
.org 0x1070A
m68k_01070a:
        jsr -9494(%pc)
m68k_01070a_end:
.org 0x1070E
m68k_01070e:
        lea.l 0xcc00:w,%a0
m68k_01070e_end:
.org 0x10712
m68k_010712:
        clr.w %d0
m68k_010712_end:
.org 0x10714
m68k_010714:
        move.b (%a0, %d1.w),%d0
m68k_010714_end:
.org 0x10718
m68k_010718:
        btst.l #0x6,%d0
m68k_010718_end:
.org 0x1071C
m68k_01071c:
        bne.w (. + 14)
m68k_01071c_end:
.org 0x10720
m68k_010720:
        lea.l 0xf45e:w,%a0
m68k_010720_end:
.org 0x10724
m68k_010724:
        lsl.w #0x1,%d0
m68k_010724_end:
.org 0x10726
m68k_010726:
        move.w %d1,(%a0, %d0.w)
m68k_010726_end:
.org 0x1072A
m68k_01072a:
        rts
m68k_01072a_end:
.org 0x10A34
m68k_010a34:
        jsr 0x1b59e:l
m68k_010a34_end:
.org 0x10A3A
m68k_010a3a:
        rts
m68k_010a3a_end:
.org 0x10A3C
m68k_010a3c:
        jsr 0x1b604:l
m68k_010a3c_end:
.org 0x10A42
m68k_010a42:
        rts
m68k_010a42_end:
.org 0x10A44
m68k_010a44:
        jsr 0x1bfe0:l
m68k_010a44_end:
.org 0x10A4A
m68k_010a4a:
        rts
m68k_010a4a_end:
.org 0x1B59E
m68k_01b59e:
        tst.w 0xf386:w
m68k_01b59e_end:
.org 0x1B5A2
m68k_01b5a2:
        bne.w (. + 96)
m68k_01b5a2_end:
.org 0x1B5A6
m68k_01b5a6:
        movea.l 0xff382c:l,%a0
m68k_01b5a6_end:
.org 0x1B5AC
m68k_01b5ac:
        bsr.w (. + -842)
m68k_01b5ac_end:
.org 0x1B5B0
m68k_01b5b0:
        bsr.w (. + -822)
m68k_01b5b0_end:
.org 0x1B5B4
m68k_01b5b4:
        bsr.w (. + -760)
m68k_01b5b4_end:
.org 0x1B5B8
m68k_01b5b8:
        bsr.w (. + -326)
m68k_01b5b8_end:
.org 0x1B5BC
m68k_01b5bc:
        clr.w 0xf772:w
m68k_01b5bc_end:
.org 0x1B5C0
m68k_01b5c0:
        move.w 0xf392:w,0xf68a:w
m68k_01b5c0_end:
.org 0x1B5C6
m68k_01b5c6:
        move.w #0xffff,0xa5f8:w
m68k_01b5c6_end:
.org 0x1B5CC
m68k_01b5cc:
        move.w #0x400,0xf612:w
m68k_01b5cc_end:
.org 0x1B5D2
m68k_01b5d2:
        clr.w 0xf362:w
m68k_01b5d2_end:
.org 0x1B5D6
m68k_01b5d6:
        clr.w 0xf352:w
m68k_01b5d6_end:
.org 0x1B5DA
m68k_01b5da:
        move.w #0x1f,%d0
m68k_01b5da_end:
.org 0x1B5DE
m68k_01b5de:
        lea.l 0xfb00:w,%a0
m68k_01b5de_end:
.org 0x1B5E2
m68k_01b5e2:
        lea.l 0xfb80:w,%a1
m68k_01b5e2_end:
.org 0x1B5E6
m68k_01b5e6:
        move.w (%a0)+,(%a1)+
m68k_01b5e6_end:
.org 0x1B5E8
m68k_01b5e8:
        dbra %d0,(. + -2)
m68k_01b5e8_end:
.org 0x1B5EC
m68k_01b5ec:
        move.w #0xffff,0xa550:w
m68k_01b5ec_end:
.org 0x1B5F2
m68k_01b5f2:
        move.w #0xffff,0xa5a4:w
m68k_01b5f2_end:
.org 0x1B5F8
m68k_01b5f8:
        clr.w 0xf36a:w
m68k_01b5f8_end:
.org 0x1B5FC
m68k_01b5fc:
        jsr 0x1b098:l
m68k_01b5fc_end:
.org 0x1B602
m68k_01b602:
        rts
m68k_01b602_end:
.org 0x1B604
m68k_01b604:
        bsr.w (. + 776)
m68k_01b604_end:
.org 0x1B608
m68k_01b608:
        bcs.w (. + 56)
m68k_01b608_end:
.org 0x1B60C
m68k_01b60c:
        move.w #0x7ff,%d0
m68k_01b60c_end:
.org 0x1B610
m68k_01b610:
        lea.l 0xff7000:l,%a0
m68k_01b610_end:
.org 0x1B616
m68k_01b616:
        clr.l (%a0)+
m68k_01b616_end:
.org 0x1B618
m68k_01b618:
        dbra %d0,(. + -2)
m68k_01b618_end:
.org 0x1B61C
m68k_01b61c:
        bsr.w (. + 166)
m68k_01b61c_end:
.org 0x1B620
m68k_01b620:
        move.w #0x200,0xf38a:w
m68k_01b620_end:
.org 0x1B626
m68k_01b626:
        move.w #0x209,0xf612:w
m68k_01b626_end:
.org 0x1B62C
m68k_01b62c:
        move.w #0xd,0xf362:w
m68k_01b62c_end:
.org 0x1B632
m68k_01b632:
        clr.w 0xf352:w
m68k_01b632_end:
.org 0x1B636
m68k_01b636:
        move.w #0xffff,0xf376:w
m68k_01b636_end:
.org 0x1B63C
m68k_01b63c:
        bra.w (. + 98)
m68k_01b63c_end:
.org 0x1B640
m68k_01b640:
        lea.l 0xe640:w,%a2
m68k_01b640_end:
.org 0x1B644
m68k_01b644:
        movea.l 0xff382c:l,%a0
m68k_01b644_end:
.org 0x1B64A
m68k_01b64a:
        clr.w %d0
m68k_01b64a_end:
.org 0x1B64C
m68k_01b64c:
        move.b 0x4(%a0),%d0
m68k_01b64c_end:
.org 0x1B650
m68k_01b650:
        lsl.w #0x1,%d0
m68k_01b650_end:
.org 0x1B652
m68k_01b652:
        move.w (%a2, %d0.w),0xf3d0:w
m68k_01b652_end:
.org 0x1B658
m68k_01b658:
        lea.l 0x9000:w,%a0
m68k_01b658_end:
.org 0x1B65C
m68k_01b65c:
        lea.l 0xefbe:w,%a1
m68k_01b65c_end:
.org 0x1B660
m68k_01b660:
        move.w 0xefc6:w,%d0
m68k_01b660_end:
.org 0x1B664
m68k_01b664:
        adda.w (%a1, %d0.w),%a0
m68k_01b664_end:
.org 0x1B668
m68k_01b668:
        clr.w %d0
m68k_01b668_end:
.org 0x1B66A
m68k_01b66a:
        move.b 0x4(%a0),%d0
m68k_01b66a_end:
.org 0x1B66E
m68k_01b66e:
        lsl.w #0x1,%d0
m68k_01b66e_end:
.org 0x1B670
m68k_01b670:
        move.w (%a2, %d0.w),0xf3d2:w
m68k_01b670_end:
.org 0x1B676
m68k_01b676:
        move.w #0xa0,0xf740:w
m68k_01b676_end:
.org 0x1B67C
m68k_01b67c:
        move.w #0x12c,0xf608:w
m68k_01b67c_end:
.org 0x1B682
m68k_01b682:
        clr.w 0xf362:w
m68k_01b682_end:
.org 0x1B686
m68k_01b686:
        jsr 0x30a74:l
m68k_01b686_end:
.org 0x1B68C
m68k_01b68c:
        bsr.w (. + 732)
m68k_01b68c_end:
.org 0x1B690
m68k_01b690:
        move.w #0x201,0xf612:w
m68k_01b690_end:
.org 0x1B696
m68k_01b696:
        clr.w 0xf362:w
m68k_01b696_end:
.org 0x1B69A
m68k_01b69a:
        bsr.w (. + 7458)
m68k_01b69a_end:
.org 0x1B69E
m68k_01b69e:
        movea.l 0xff382c:l,%a0
m68k_01b69e_end:
.org 0x1B6A4
m68k_01b6a4:
        move.b 0x4(%a0),0xa622:w
m68k_01b6a4_end:
.org 0x1B6AA
m68k_01b6aa:
        lea.l 0x9000:w,%a0
m68k_01b6aa_end:
.org 0x1B6AE
m68k_01b6ae:
        lea.l 0xefbe:w,%a1
m68k_01b6ae_end:
.org 0x1B6B2
m68k_01b6b2:
        move.w 0xefc6:w,%d0
m68k_01b6b2_end:
.org 0x1B6B6
m68k_01b6b6:
        adda.w (%a1, %d0.w),%a0
m68k_01b6b6_end:
.org 0x1B6BA
m68k_01b6ba:
        move.b 0x4(%a0),0xa623:w
m68k_01b6ba_end:
.org 0x1B6C0
m68k_01b6c0:
        rts
m68k_01b6c0_end:
.org 0x1B6C2
m68k_01b6c2:
        bsr.w (. + 224)
m68k_01b6c2_end:
.org 0x1B6C6
m68k_01b6c6:
        bsr.w (. + 394)
m68k_01b6c6_end:
.org 0x1B6CA
m68k_01b6ca:
        bsr.w (. + 460)
m68k_01b6ca_end:
.org 0x1B6CE
m68k_01b6ce:
        lea.l 0xcc00:w,%a0
m68k_01b6ce_end:
.org 0x1B6D2
m68k_01b6d2:
        lea.l 0xf427:w,%a1
m68k_01b6d2_end:
.org 0x1B6D6
m68k_01b6d6:
        lea.l 0xe640:w,%a2
m68k_01b6d6_end:
.org 0x1B6DA
m68k_01b6da:
        clr.w %d1
m68k_01b6da_end:
.org 0x1B6DC
m68k_01b6dc:
        move.b (%a0, %d0.w),%d1
m68k_01b6dc_end:
.org 0x1B6E0
m68k_01b6e0:
        andi.w #0x3f,%d1
m68k_01b6e0_end:
.org 0x1B6E4
m68k_01b6e4:
        move.b (%a1, %d1.w),%d1
m68k_01b6e4_end:
.org 0x1B6E8
m68k_01b6e8:
        lsl.w #0x1,%d1
m68k_01b6e8_end:
.org 0x1B6EA
m68k_01b6ea:
        move.w (%a2, %d1.w),0xffff80dc:l
m68k_01b6ea_end:
.org 0x1B6F2
m68k_01b6f2:
        clr.w %d1
m68k_01b6f2_end:
.org 0x1B6F4
m68k_01b6f4:
        move.b (%a0, %d7.w),%d1
m68k_01b6f4_end:
.org 0x1B6F8
m68k_01b6f8:
        andi.w #0x3f,%d1
m68k_01b6f8_end:
.org 0x1B6FC
m68k_01b6fc:
        move.b (%a1, %d1.w),%d1
m68k_01b6fc_end:
.org 0x1B700
m68k_01b700:
        lsl.w #0x1,%d1
m68k_01b700_end:
.org 0x1B702
m68k_01b702:
        move.w (%a2, %d1.w),0xffff80de:l
m68k_01b702_end:
.org 0x1B70A
m68k_01b70a:
        lea.l 0xc800:w,%a0
m68k_01b70a_end:
.org 0x1B70E
m68k_01b70e:
        lea.l 0xc500:w,%a1
m68k_01b70e_end:
.org 0x1B712
m68k_01b712:
        lea.l 0xb400:w,%a2
m68k_01b712_end:
.org 0x1B716
m68k_01b716:
        lea.l 0xb200:w,%a3
m68k_01b716_end:
.org 0x1B71A
m68k_01b71a:
        lea.l 0xc000:w,%a4
m68k_01b71a_end:
.org 0x1B71E
m68k_01b71e:
        lea.l 0xea88:w,%a5
m68k_01b71e_end:
.org 0x1B722
m68k_01b722:
        move.w %d0,0xffff80e0:l
m68k_01b722_end:
.org 0x1B728
m68k_01b728:
        move.b (%a1, %d0.w),0xffff8101:l
m68k_01b728_end:
.org 0x1B730
m68k_01b730:
        bsr.w (. + 16804)
m68k_01b730_end:
.org 0x1B734
m68k_01b734:
        move.w %d3,0xffff8108:l
m68k_01b734_end:
.org 0x1B73A
m68k_01b73a:
        lsl.w #0x1,%d0
m68k_01b73a_end:
.org 0x1B73C
m68k_01b73c:
        move.w (%a2, %d0.w),0xffff8104:l
m68k_01b73c_end:
.org 0x1B744
m68k_01b744:
        move.w (%a3, %d0.w),0xffff810c:l
m68k_01b744_end:
.org 0x1B74C
m68k_01b74c:
        move.w (%a4, %d0.w),0xffff8110:l
m68k_01b74c_end:
.org 0x1B754
m68k_01b754:
        lsl.w #0x1,%d0
m68k_01b754_end:
.org 0x1B756
m68k_01b756:
        move.w 0x2(%a0, %d0.w),0xffff80e4:l
m68k_01b756_end:
.org 0x1B75E
m68k_01b75e:
        move.w %d7,%d0
m68k_01b75e_end:
.org 0x1B760
m68k_01b760:
        move.w %d0,0xffff80e2:l
m68k_01b760_end:
.org 0x1B766
m68k_01b766:
        move.b (%a1, %d0.w),0xffff8103:l
m68k_01b766_end:
.org 0x1B76E
m68k_01b76e:
        bsr.w (. + 16742)
m68k_01b76e_end:
.org 0x1B772
m68k_01b772:
        move.w %d3,0xffff810a:l
m68k_01b772_end:
.org 0x1B778
m68k_01b778:
        lsl.w #0x1,%d0
m68k_01b778_end:
.org 0x1B77A
m68k_01b77a:
        move.w (%a2, %d0.w),0xffff8106:l
m68k_01b77a_end:
.org 0x1B782
m68k_01b782:
        move.w (%a3, %d0.w),0xffff810e:l
m68k_01b782_end:
.org 0x1B78A
m68k_01b78a:
        move.w (%a4, %d0.w),0xffff8112:l
m68k_01b78a_end:
.org 0x1B792
m68k_01b792:
        lsl.w #0x1,%d0
m68k_01b792_end:
.org 0x1B794
m68k_01b794:
        move.w 0x2(%a0, %d0.w),0xffff80e6:l
m68k_01b794_end:
.org 0x1B79C
m68k_01b79c:
        bsr.w (. + 272)
m68k_01b79c_end:
.org 0x1B7A0
m68k_01b7a0:
        rts
m68k_01b7a0_end:
.org 0x1B7A2
m68k_01b7a2:
        lea.l 0xcc00:w,%a0
m68k_01b7a2_end:
.org 0x1B7A6
m68k_01b7a6:
        lea.l 0xf427:w,%a1
m68k_01b7a6_end:
.org 0x1B7AA
m68k_01b7aa:
        clr.w %d7
m68k_01b7aa_end:
.org 0x1B7AC
m68k_01b7ac:
        move.w 0xf3f2:w,%d0
m68k_01b7ac_end:
.org 0x1B7B0
m68k_01b7b0:
        move.w %d0,0xf702:w
m68k_01b7b0_end:
.org 0x1B7B4
m68k_01b7b4:
        move.b (%a0, %d0.w),%d1
m68k_01b7b4_end:
.org 0x1B7B8
m68k_01b7b8:
        andi.w #0x3f,%d1
m68k_01b7b8_end:
.org 0x1B7BC
m68k_01b7bc:
        move.b (%a1, %d1.w),%d1
m68k_01b7bc_end:
.org 0x1B7C0
m68k_01b7c0:
        move.w %d1,0xf68c:w
m68k_01b7c0_end:
.org 0x1B7C4
m68k_01b7c4:
        move.w 0xf3a6:w,%d0
m68k_01b7c4_end:
.org 0x1B7C8
m68k_01b7c8:
        move.w %d0,0xf706:w
m68k_01b7c8_end:
.org 0x1B7CC
m68k_01b7cc:
        move.b (%a0, %d0.w),%d2
m68k_01b7cc_end:
.org 0x1B7D0
m68k_01b7d0:
        andi.w #0x3f,%d2
m68k_01b7d0_end:
.org 0x1B7D4
m68k_01b7d4:
        move.b (%a1, %d2.w),%d2
m68k_01b7d4_end:
.org 0x1B7D8
m68k_01b7d8:
        move.w %d2,0xf68e:w
m68k_01b7d8_end:
.org 0x1B7DC
m68k_01b7dc:
        clr.w %d3
m68k_01b7dc_end:
.org 0x1B7DE
m68k_01b7de:
        cmp.b 0xf67b:w,%d1
m68k_01b7de_end:
.org 0x1B7E2
m68k_01b7e2:
        beq.w (. + 26)
m68k_01b7e2_end:
.org 0x1B7E6
m68k_01b7e6:
        addq.w #0x8,%d3
m68k_01b7e6_end:
.org 0x1B7E8
m68k_01b7e8:
        cmp.b 0xf67d:w,%d1
m68k_01b7e8_end:
.org 0x1B7EC
m68k_01b7ec:
        beq.w (. + 16)
m68k_01b7ec_end:
.org 0x1B7F0
m68k_01b7f0:
        addq.w #0x8,%d3
m68k_01b7f0_end:
.org 0x1B7F2
m68k_01b7f2:
        cmp.b 0xf67f:w,%d1
m68k_01b7f2_end:
.org 0x1B7F6
m68k_01b7f6:
        beq.w (. + 6)
m68k_01b7f6_end:
.org 0x1B7FA
m68k_01b7fa:
        addq.w #0x8,%d3
m68k_01b7fa_end:
.org 0x1B7FC
m68k_01b7fc:
        cmp.b 0xf67b:w,%d2
m68k_01b7fc_end:
.org 0x1B800
m68k_01b800:
        beq.w (. + 26)
m68k_01b800_end:
.org 0x1B804
m68k_01b804:
        addq.w #0x2,%d3
m68k_01b804_end:
.org 0x1B806
m68k_01b806:
        cmp.b 0xf67d:w,%d2
m68k_01b806_end:
.org 0x1B80A
m68k_01b80a:
        beq.w (. + 16)
m68k_01b80a_end:
.org 0x1B80E
m68k_01b80e:
        addq.w #0x2,%d3
m68k_01b80e_end:
.org 0x1B810
m68k_01b810:
        cmp.b 0xf67f:w,%d2
m68k_01b810_end:
.org 0x1B814
m68k_01b814:
        beq.w (. + 6)
m68k_01b814_end:
.org 0x1B818
m68k_01b818:
        addq.w #0x2,%d3
m68k_01b818_end:
.org 0x1B81A
m68k_01b81a:
        move.b 22(%pc, %d3.w),0xffff80da:l
m68k_01b81a_end:
.org 0x1B822
m68k_01b822:
        clr.b 0xffff8124:l
m68k_01b822_end:
.org 0x1B828
m68k_01b828:
        move.b 9(%pc, %d3.w),0xffff8125:l
m68k_01b828_end:
.org 0x1B830
m68k_01b830:
        rts
m68k_01b830_end:
.org 0x1B850
m68k_01b850:
        lea.l 0x9000:w,%a0
m68k_01b850_end:
.org 0x1B854
m68k_01b854:
        lea.l 0xefbe:w,%a1
m68k_01b854_end:
.org 0x1B858
m68k_01b858:
        move.w 0xefc6:w,%d0
m68k_01b858_end:
.org 0x1B85C
m68k_01b85c:
        adda.w (%a1, %d0.w),%a0
m68k_01b85c_end:
.org 0x1B860
m68k_01b860:
        clr.w %d0
m68k_01b860_end:
.org 0x1B862
m68k_01b862:
        move.b 0x1(%a0),%d0
m68k_01b862_end:
.org 0x1B866
m68k_01b866:
        move.w %d0,%d1
m68k_01b866_end:
.org 0x1B868
m68k_01b868:
        lsl.w #0x3,%d0
m68k_01b868_end:
.org 0x1B86A
m68k_01b86a:
        add.w %d1,%d0
m68k_01b86a_end:
.org 0x1B86C
m68k_01b86c:
        lsl.w #0x3,%d0
m68k_01b86c_end:
.org 0x1B86E
m68k_01b86e:
        clr.w %d1
m68k_01b86e_end:
.org 0x1B870
m68k_01b870:
        move.b 0x2(%a0),%d1
m68k_01b870_end:
.org 0x1B874
m68k_01b874:
        add.w %d1,%d0
m68k_01b874_end:
.org 0x1B876
m68k_01b876:
        lea.l 0xee5f0:l,%a0
m68k_01b876_end:
.org 0x1B87C
m68k_01b87c:
        clr.w %d1
m68k_01b87c_end:
.org 0x1B87E
m68k_01b87e:
        move.b (%a0, %d0.w),%d1
m68k_01b87e_end:
.org 0x1B882
m68k_01b882:
        lea.l 12(%pc),%a0
m68k_01b882_end:
.org 0x1B886
m68k_01b886:
        move.b (%a0, %d1.w),0xffff80db:l
m68k_01b886_end:
.org 0x1B88E
m68k_01b88e:
        rts
m68k_01b88e_end:
.org 0x1B896
m68k_01b896:
        move.w 0xf3a6:w,%d0
m68k_01b896_end:
.org 0x1B89A
m68k_01b89a:
        move.w 0xf3f2:w,%d7
m68k_01b89a_end:
.org 0x1B89E
m68k_01b89e:
        tst.b 0xffff8125:l
m68k_01b89e_end:
.org 0x1B8A4
m68k_01b8a4:
        beq.w (. + 6)
m68k_01b8a4_end:
.org 0x1B8A8
m68k_01b8a8:
        exg %d0,%d7
m68k_01b8a8_end:
.org 0x1B8AA
m68k_01b8aa:
        rts
m68k_01b8aa_end:
.org 0x1B8AC
m68k_01b8ac:
        lea.l 0x9000:w,%a0
m68k_01b8ac_end:
.org 0x1B8B0
m68k_01b8b0:
        lea.l 0xefbe:w,%a1
m68k_01b8b0_end:
.org 0x1B8B4
m68k_01b8b4:
        move.w 0xefc6:w,%d0
m68k_01b8b4_end:
.org 0x1B8B8
m68k_01b8b8:
        adda.w (%a1, %d0.w),%a0
m68k_01b8b8_end:
.org 0x1B8BC
m68k_01b8bc:
        move.b 0xd(%a0),%d0
m68k_01b8bc_end:
.org 0x1B8C0
m68k_01b8c0:
        lea.l 0xff3000:l,%a0
m68k_01b8c0_end:
.org 0x1B8C6
m68k_01b8c6:
        tst.b (%a0)
m68k_01b8c6_end:
.org 0x1B8C8
m68k_01b8c8:
        bmi.w (. + 66)
m68k_01b8c8_end:
.org 0x1B8CC
m68k_01b8cc:
        cmp.b 0x1(%a0),%d0
m68k_01b8cc_end:
.org 0x1B8D0
m68k_01b8d0:
        beq.w (. + 12)
m68k_01b8d0_end:
.org 0x1B8D4
m68k_01b8d4:
        addq.w #0x2,%a0
m68k_01b8d4_end:
.org 0x1B8D6
m68k_01b8d6:
        tst.b (%a0)+
m68k_01b8d6_end:
.org 0x1B8D8
m68k_01b8d8:
        bne.b (. + -2)
m68k_01b8d8_end:
.org 0x1B8DA
m68k_01b8da:
        bra.b (. + -20)
m68k_01b8da_end:
.org 0x1B8DC
m68k_01b8dc:
        cmpi.b #0x90,0x3(%a0)
m68k_01b8dc_end:
.org 0x1B8E2
m68k_01b8e2:
        bne.w (. + 40)
m68k_01b8e2_end:
.org 0x1B8E6
m68k_01b8e6:
        lea.l 0xff39b2:l,%a0
m68k_01b8e6_end:
.org 0x1B8EC
m68k_01b8ec:
        adda.w 0xff3bb2:l,%a0
m68k_01b8ec_end:
.org 0x1B8F2
m68k_01b8f2:
        tst.b (%a0)+
m68k_01b8f2_end:
.org 0x1B8F4
m68k_01b8f4:
        beq.w (. + 22)
m68k_01b8f4_end:
.org 0x1B8F8
m68k_01b8f8:
        cmp.b (%a0)+,%d0
m68k_01b8f8_end:
.org 0x1B8FA
m68k_01b8fa:
        bne.b (. + -8)
m68k_01b8fa_end:
.org 0x1B8FC
m68k_01b8fc:
        move.b (%a0)+,-0x3(%a0)
m68k_01b8fc_end:
.org 0x1B900
m68k_01b900:
        beq.w (. + 10)
m68k_01b900_end:
.org 0x1B904
m68k_01b904:
        move.b (%a0)+,-0x3(%a0)
m68k_01b904_end:
.org 0x1B908
m68k_01b908:
        bra.b (. + -12)
m68k_01b908_end:
.org 0x1B90A
m68k_01b90a:
        rts
m68k_01b90a_end:
.org 0x1B90C
m68k_01b90c:
        movea.l 0xff382c:l,%a0
m68k_01b90c_end:
.org 0x1B912
m68k_01b912:
        move.b 0x4(%a0),%d0
m68k_01b912_end:
.org 0x1B916
m68k_01b916:
        cmp.b 0xf67b:w,%d0
m68k_01b916_end:
.org 0x1B91A
m68k_01b91a:
        beq.w (. + 72)
m68k_01b91a_end:
.org 0x1B91E
m68k_01b91e:
        cmp.b 0xf67d:w,%d0
m68k_01b91e_end:
.org 0x1B922
m68k_01b922:
        beq.w (. + 64)
m68k_01b922_end:
.org 0x1B926
m68k_01b926:
        cmp.b 0xf67f:w,%d0
m68k_01b926_end:
.org 0x1B92A
m68k_01b92a:
        beq.w (. + 56)
m68k_01b92a_end:
.org 0x1B92E
m68k_01b92e:
        lea.l 0x9000:w,%a0
m68k_01b92e_end:
.org 0x1B932
m68k_01b932:
        lea.l 0xefbe:w,%a1
m68k_01b932_end:
.org 0x1B936
m68k_01b936:
        move.w 0xefc6:w,%d0
m68k_01b936_end:
.org 0x1B93A
m68k_01b93a:
        adda.w (%a1, %d0.w),%a0
m68k_01b93a_end:
.org 0x1B93E
m68k_01b93e:
        move.b 0x4(%a0),%d0
m68k_01b93e_end:
.org 0x1B942
m68k_01b942:
        cmp.b 0xf67b:w,%d0
m68k_01b942_end:
.org 0x1B946
m68k_01b946:
        beq.w (. + 28)
m68k_01b946_end:
.org 0x1B94A
m68k_01b94a:
        cmp.b 0xf67d:w,%d0
m68k_01b94a_end:
.org 0x1B94E
m68k_01b94e:
        beq.w (. + 20)
m68k_01b94e_end:
.org 0x1B952
m68k_01b952:
        cmp.b 0xf67f:w,%d0
m68k_01b952_end:
.org 0x1B956
m68k_01b956:
        beq.w (. + 12)
m68k_01b956_end:
.org 0x1B95A
m68k_01b95a:
        ori.w #0x1,%sr
m68k_01b95a_end:
.org 0x1B95E
m68k_01b95e:
        bra.w (. + 8)
m68k_01b95e_end:
.org 0x1B962
m68k_01b962:
        andi.w #0xfffe,%sr
m68k_01b962_end:
.org 0x1B966
m68k_01b966:
        rts
m68k_01b966_end:
.org 0x1B968
m68k_01b968:
        bsr.w (. + 52)
m68k_01b968_end:
.org 0x1B96C
m68k_01b96c:
        move.w %d1,%d2
m68k_01b96c_end:
.org 0x1B96E
m68k_01b96e:
        cmpi.w #0xa,%d2
m68k_01b96e_end:
.org 0x1B972
m68k_01b972:
        bhi.w (. + 24)
m68k_01b972_end:
.org 0x1B976
m68k_01b976:
        bsr.w (. + 96)
m68k_01b976_end:
.org 0x1B97A
m68k_01b97a:
        bsr.w (. + 520)
m68k_01b97a_end:
.org 0x1B97E
m68k_01b97e:
        bsr.w (. + 678)
m68k_01b97e_end:
.org 0x1B982
m68k_01b982:
        bsr.w (. + 740)
m68k_01b982_end:
.org 0x1B986
m68k_01b986:
        bra.w (. + 20)
m68k_01b986_end:
.org 0x1B98A
m68k_01b98a:
        bsr.w (. + 1354)
m68k_01b98a_end:
.org 0x1B98E
m68k_01b98e:
        bsr.w (. + 1498)
m68k_01b98e_end:
.org 0x1B992
m68k_01b992:
        bsr.w (. + 658)
m68k_01b992_end:
.org 0x1B996
m68k_01b996:
        bsr.w (. + 830)
m68k_01b996_end:
.org 0x1B99A
m68k_01b99a:
        rts
m68k_01b99a_end:
.org 0x1B99C
m68k_01b99c:
        lea.l 0xc800:w,%a0
m68k_01b99c_end:
.org 0x1B9A0
m68k_01b9a0:
        lea.l 0xb400:w,%a1
m68k_01b9a0_end:
.org 0x1B9A4
m68k_01b9a4:
        move.w 0xf3a6:w,%d0
m68k_01b9a4_end:
.org 0x1B9A8
m68k_01b9a8:
        lsl.w #0x1,%d0
m68k_01b9a8_end:
.org 0x1B9AA
m68k_01b9aa:
        move.w (%a1, %d0.w),%d1
m68k_01b9aa_end:
.org 0x1B9AE
m68k_01b9ae:
        mulu.w #0xa,%d1
m68k_01b9ae_end:
.org 0x1B9B2
m68k_01b9b2:
        lsl.w #0x1,%d0
m68k_01b9b2_end:
.org 0x1B9B4
m68k_01b9b4:
        mulu.w 0x2(%a0, %d0.w),%d1
m68k_01b9b4_end:
.org 0x1B9B8
m68k_01b9b8:
        move.w 0xf3f2:w,%d0
m68k_01b9b8_end:
.org 0x1B9BC
m68k_01b9bc:
        lsl.w #0x1,%d0
m68k_01b9bc_end:
.org 0x1B9BE
m68k_01b9be:
        move.w (%a1, %d0.w),%d2
m68k_01b9be_end:
.org 0x1B9C2
m68k_01b9c2:
        addq.w #0x1,%d2
m68k_01b9c2_end:
.org 0x1B9C4
m68k_01b9c4:
        lsl.w #0x1,%d0
m68k_01b9c4_end:
.org 0x1B9C6
m68k_01b9c6:
        mulu.w 0x2(%a0, %d0.w),%d0
m68k_01b9c6_end:
.org 0x1B9CA
m68k_01b9ca:
        addq.w #0x1,%d0
m68k_01b9ca_end:
.org 0x1B9CC
m68k_01b9cc:
        mulu.w %d0,%d2
m68k_01b9cc_end:
.org 0x1B9CE
m68k_01b9ce:
        jsr 0x35760:l
m68k_01b9ce_end:
.org 0x1B9D4
m68k_01b9d4:
        rts
m68k_01b9d4_end:
.org 0x1B9D6
m68k_01b9d6:
        jsr 0x83d4:l
m68k_01b9d6_end:
.org 0x1B9DC
m68k_01b9dc:
        andi.l #0xffff,%d0
m68k_01b9dc_end:
.org 0x1B9E2
m68k_01b9e2:
        move.l %d0,%d1
m68k_01b9e2_end:
.org 0x1B9E4
m68k_01b9e4:
        lsl.l #0x5,%d0
m68k_01b9e4_end:
.org 0x1B9E6
m68k_01b9e6:
        sub.l %d1,%d0
m68k_01b9e6_end:
.org 0x1B9E8
m68k_01b9e8:
        swap %d0
m68k_01b9e8_end:
.org 0x1B9EA
m68k_01b9ea:
        addi.w #0x32,%d0
m68k_01b9ea_end:
.org 0x1B9EE
m68k_01b9ee:
        mulu.w %d2,%d0
m68k_01b9ee_end:
.org 0x1B9F0
m68k_01b9f0:
        lea.l 0xc800:w,%a0
m68k_01b9f0_end:
.org 0x1B9F4
m68k_01b9f4:
        move.w 0xf3f2:w,%d1
m68k_01b9f4_end:
.org 0x1B9F8
m68k_01b9f8:
        lsl.w #0x2,%d1
m68k_01b9f8_end:
.org 0x1B9FA
m68k_01b9fa:
        move.w 0x2(%a0, %d1.w),%d3
m68k_01b9fa_end:
.org 0x1B9FE
m68k_01b9fe:
        mulu.w %d3,%d0
m68k_01b9fe_end:
.org 0x1BA00
m68k_01ba00:
        divu.w #0x3e8,%d0
m68k_01ba00_end:
.org 0x1BA04
m68k_01ba04:
        sub.w %d0,%d3
m68k_01ba04_end:
.org 0x1BA06
m68k_01ba06:
        move.w %d3,0x2(%a0, %d1.w)
m68k_01ba06_end:
.org 0x1BA0A
m68k_01ba0a:
        andi.l #0xffff,%d0
m68k_01ba0a_end:
.org 0x1BA10
m68k_01ba10:
        divu.w #0x64,%d0
m68k_01ba10_end:
.org 0x1BA14
m68k_01ba14:
        move.w %d0,0xefb8:w
m68k_01ba14_end:
.org 0x1BA18
m68k_01ba18:
        jsr 0x83d4:l
m68k_01ba18_end:
.org 0x1BA1E
m68k_01ba1e:
        andi.l #0xffff,%d0
m68k_01ba1e_end:
.org 0x1BA24
m68k_01ba24:
        move.l %d0,%d1
m68k_01ba24_end:
.org 0x1BA26
m68k_01ba26:
        lsl.l #0x5,%d0
m68k_01ba26_end:
.org 0x1BA28
m68k_01ba28:
        sub.l %d1,%d0
m68k_01ba28_end:
.org 0x1BA2A
m68k_01ba2a:
        swap %d0
m68k_01ba2a_end:
.org 0x1BA2C
m68k_01ba2c:
        lea.l 0xb200:w,%a0
m68k_01ba2c_end:
.org 0x1BA30
m68k_01ba30:
        move.w 0xf3f2:w,%d3
m68k_01ba30_end:
.org 0x1BA34
m68k_01ba34:
        lsl.w #0x1,%d3
m68k_01ba34_end:
.org 0x1BA36
m68k_01ba36:
        move.w (%a0, %d3.w),%d1
m68k_01ba36_end:
.org 0x1BA3A
m68k_01ba3a:
        mulu.w %d1,%d0
m68k_01ba3a_end:
.org 0x1BA3C
m68k_01ba3c:
        divu.w #0x64,%d0
m68k_01ba3c_end:
.org 0x1BA40
m68k_01ba40:
        sub.w %d0,%d1
m68k_01ba40_end:
.org 0x1BA42
m68k_01ba42:
        bne.w (. + 8)
m68k_01ba42_end:
.org 0x1BA46
m68k_01ba46:
        move.w #0x1,%d1
m68k_01ba46_end:
.org 0x1BA4A
m68k_01ba4a:
        move.w %d1,(%a0, %d3.w)
m68k_01ba4a_end:
.org 0x1BA4E
m68k_01ba4e:
        rts
m68k_01ba4e_end:
.org 0x1BA50
m68k_01ba50:
        move.w %d0,0xf744:w
m68k_01ba50_end:
.org 0x1BA54
m68k_01ba54:
        lea.l 0xc000:w,%a0
m68k_01ba54_end:
.org 0x1BA58
m68k_01ba58:
        lea.l 0xcc00:w,%a1
m68k_01ba58_end:
.org 0x1BA5C
m68k_01ba5c:
        move.b (%a1, %d0.w),%d3
m68k_01ba5c_end:
.org 0x1BA60
m68k_01ba60:
        move.b #0xff,(%a1, %d0.w)
m68k_01ba60_end:
.org 0x1BA66
m68k_01ba66:
        lsl.w #0x1,%d0
m68k_01ba66_end:
.org 0x1BA68
m68k_01ba68:
        move.w (%a0, %d0.w),%d1
m68k_01ba68_end:
.org 0x1BA6C
m68k_01ba6c:
        andi.l #0xffff,%d1
m68k_01ba6c_end:
.org 0x1BA72
m68k_01ba72:
        divu.w #0x5,%d1
m68k_01ba72_end:
.org 0x1BA76
m68k_01ba76:
        lsr.w #0x1,%d0
m68k_01ba76_end:
.org 0x1BA78
m68k_01ba78:
        lea.l 0xf427:w,%a0
m68k_01ba78_end:
.org 0x1BA7C
m68k_01ba7c:
        move.b (%a0, %d3.w),%d3
m68k_01ba7c_end:
.org 0x1BA80
m68k_01ba80:
        andi.w #0xff,%d3
m68k_01ba80_end:
.org 0x1BA84
m68k_01ba84:
        lsl.w #0x1,%d3
m68k_01ba84_end:
.org 0x1BA86
m68k_01ba86:
        lea.l 0xe640:w,%a0
m68k_01ba86_end:
.org 0x1BA8A
m68k_01ba8a:
        cmp.w (%a0, %d3.w),%d0
m68k_01ba8a_end:
.org 0x1BA8E
m68k_01ba8e:
        bne.w (. + 8)
m68k_01ba8e_end:
.org 0x1BA92
m68k_01ba92:
        addi.w #0x1e,%d1
m68k_01ba92_end:
.org 0x1BA96
m68k_01ba96:
        lea.l 0xc700:w,%a0
m68k_01ba96_end:
.org 0x1BA9A
m68k_01ba9a:
        btst.b #0x4,(%a0, %d0.w)
m68k_01ba9a_end:
.org 0x1BAA0
m68k_01baa0:
        beq.w (. + 8)
m68k_01baa0_end:
.org 0x1BAA4
m68k_01baa4:
        addi.w #0x14,%d1
m68k_01baa4_end:
.org 0x1BAA8
m68k_01baa8:
        move.b (%a2),%d2
m68k_01baa8_end:
.org 0x1BAAA
m68k_01baaa:
        andi.b #0xf,%d2
m68k_01baaa_end:
.org 0x1BAAE
m68k_01baae:
        cmpi.w #0x1,%d2
m68k_01baae_end:
.org 0x1BAB2
m68k_01bab2:
        beq.w (. + 66)
m68k_01bab2_end:
.org 0x1BAB6
m68k_01bab6:
        clr.w %d3
m68k_01bab6_end:
.org 0x1BAB8
m68k_01bab8:
        subq.w #0x1,%d2
m68k_01bab8_end:
.org 0x1BABA
m68k_01baba:
        cmp.b 0xd(%a2, %d3.w),%d0
m68k_01baba_end:
.org 0x1BABE
m68k_01babe:
        beq.w (. + 8)
m68k_01babe_end:
.org 0x1BAC2
m68k_01bac2:
        addq.w #0x1,%d3
m68k_01bac2_end:
.org 0x1BAC4
m68k_01bac4:
        bra.b (. + -12)
m68k_01bac4_end:
.org 0x1BAC6
m68k_01bac6:
        subq.w #0x1,%d2
m68k_01bac6_end:
.org 0x1BAC8
m68k_01bac8:
        bmi.w (. + 14)
m68k_01bac8_end:
.org 0x1BACC
m68k_01bacc:
        move.b 0xe(%a2, %d3.w),0xd(%a2, %d3.w)
m68k_01bacc_end:
.org 0x1BAD2
m68k_01bad2:
        addq.w #0x1,%d3
m68k_01bad2_end:
.org 0x1BAD4
m68k_01bad4:
        bra.b (. + -14)
m68k_01bad4_end:
.org 0x1BAD6
m68k_01bad6:
        move.b (%a2),%d2
m68k_01bad6_end:
.org 0x1BAD8
m68k_01bad8:
        andi.b #0xf,%d2
m68k_01bad8_end:
.org 0x1BADC
m68k_01badc:
        subq.b #0x1,(%a2)
m68k_01badc_end:
.org 0x1BADE
m68k_01bade:
        clr.b 0xf746:w
m68k_01bade_end:
.org 0x1BAE2
m68k_01bae2:
        move.b 0xd(%a2),0xf747:w
m68k_01bae2_end:
.org 0x1BAE8
m68k_01bae8:
        lea.l 0xd(%a2, %d2.w),%a3
m68k_01bae8_end:
.org 0x1BAEC
m68k_01baec:
        lea.l 0xc(%a2, %d2.w),%a2
m68k_01baec_end:
.org 0x1BAF0
m68k_01baf0:
        bra.w (. + 14)
m68k_01baf0_end:
.org 0x1BAF4
m68k_01baf4:
        move.w #0xffff,0xf746:w
m68k_01baf4_end:
.org 0x1BAFA
m68k_01bafa:
        lea.l 0xd(%a2, %d2.w),%a3
m68k_01bafa_end:
.org 0x1BAFE
m68k_01bafe:
        move.b (%a3),%d2
m68k_01bafe_end:
.org 0x1BB00
m68k_01bb00:
        andi.w #0xf,%d2
m68k_01bb00_end:
.org 0x1BB04
m68k_01bb04:
        beq.w (. + 16)
m68k_01bb04_end:
.org 0x1BB08
m68k_01bb08:
        addi.w #0xc,%d2
m68k_01bb08_end:
.org 0x1BB0C
m68k_01bb0c:
        move.b (%a3)+,(%a2)+
m68k_01bb0c_end:
.org 0x1BB0E
m68k_01bb0e:
        dbra %d2,(. + -2)
m68k_01bb0e_end:
.org 0x1BB12
m68k_01bb12:
        bra.b (. + -20)
m68k_01bb12_end:
.org 0x1BB14
m68k_01bb14:
        clr.b (%a2)
m68k_01bb14_end:
.org 0x1BB16
m68k_01bb16:
        bsr.w (. + 6)
m68k_01bb16_end:
.org 0x1BB1A
m68k_01bb1a:
        rts
m68k_01bb1a_end:
.org 0x1BB1C
m68k_01bb1c:
        move.w 0xf744:w,%d0
m68k_01bb1c_end:
.org 0x1BB20
m68k_01bb20:
        lea.l 0xff39b2:l,%a0
m68k_01bb20_end:
.org 0x1BB26
m68k_01bb26:
        adda.w 0xff3bb2:l,%a0
m68k_01bb26_end:
.org 0x1BB2C
m68k_01bb2c:
        tst.w 0xf746:w
m68k_01bb2c_end:
.org 0x1BB30
m68k_01bb30:
        bmi.w (. + 52)
m68k_01bb30_end:
.org 0x1BB34
m68k_01bb34:
        tst.b (%a0)+
m68k_01bb34_end:
.org 0x1BB36
m68k_01bb36:
        beq.w (. + 70)
m68k_01bb36_end:
.org 0x1BB3A
m68k_01bb3a:
        cmp.b (%a0)+,%d0
m68k_01bb3a_end:
.org 0x1BB3C
m68k_01bb3c:
        bne.b (. + -8)
m68k_01bb3c_end:
.org 0x1BB3E
m68k_01bb3e:
        move.b 0xf747:w,-0x1(%a0)
m68k_01bb3e_end:
.org 0x1BB44
m68k_01bb44:
        lea.l 0xff3000:l,%a0
m68k_01bb44_end:
.org 0x1BB4A
m68k_01bb4a:
        tst.b (%a0)+
m68k_01bb4a_end:
.org 0x1BB4C
m68k_01bb4c:
        bmi.b (. + -2)
m68k_01bb4c_end:
.org 0x1BB4E
m68k_01bb4e:
        cmp.b (%a0)+,%d0
m68k_01bb4e_end:
.org 0x1BB50
m68k_01bb50:
        beq.w (. + 10)
m68k_01bb50_end:
.org 0x1BB54
m68k_01bb54:
        tst.b (%a0)+
m68k_01bb54_end:
.org 0x1BB56
m68k_01bb56:
        bne.b (. + -2)
m68k_01bb56_end:
.org 0x1BB58
m68k_01bb58:
        bra.b (. + -14)
m68k_01bb58_end:
.org 0x1BB5A
m68k_01bb5a:
        move.b 0xf747:w,-0x1(%a0)
m68k_01bb5a_end:
.org 0x1BB60
m68k_01bb60:
        bra.w (. + 28)
m68k_01bb60_end:
.org 0x1BB64
m68k_01bb64:
        tst.b (%a0)+
m68k_01bb64_end:
.org 0x1BB66
m68k_01bb66:
        beq.w (. + 22)
m68k_01bb66_end:
.org 0x1BB6A
m68k_01bb6a:
        cmp.b (%a0)+,%d0
m68k_01bb6a_end:
.org 0x1BB6C
m68k_01bb6c:
        bne.b (. + -8)
m68k_01bb6c_end:
.org 0x1BB6E
m68k_01bb6e:
        move.b (%a0)+,-0x3(%a0)
m68k_01bb6e_end:
.org 0x1BB72
m68k_01bb72:
        beq.w (. + 10)
m68k_01bb72_end:
.org 0x1BB76
m68k_01bb76:
        move.b (%a0)+,-0x3(%a0)
m68k_01bb76_end:
.org 0x1BB7A
m68k_01bb7a:
        bra.b (. + -12)
m68k_01bb7a_end:
.org 0x1BB7C
m68k_01bb7c:
        movem.l (%a7)+,%d0/%a0
m68k_01bb7c_end:
.org 0x1BB80
m68k_01bb80:
        rts
m68k_01bb80_end:
.org 0x1BB82
m68k_01bb82:
        jsr 0x83d4:l
m68k_01bb82_end:
.org 0x1BB88
m68k_01bb88:
        andi.l #0xffff,%d0
m68k_01bb88_end:
.org 0x1BB8E
m68k_01bb8e:
        move.l %d0,%d1
m68k_01bb8e_end:
.org 0x1BB90
m68k_01bb90:
        lsl.l #0x1,%d0
m68k_01bb90_end:
.org 0x1BB92
m68k_01bb92:
        add.l %d1,%d0
m68k_01bb92_end:
.org 0x1BB94
m68k_01bb94:
        lsl.l #0x3,%d0
m68k_01bb94_end:
.org 0x1BB96
m68k_01bb96:
        add.l %d1,%d0
m68k_01bb96_end:
.org 0x1BB98
m68k_01bb98:
        lsl.l #0x1,%d0
m68k_01bb98_end:
.org 0x1BB9A
m68k_01bb9a:
        add.l %d1,%d0
m68k_01bb9a_end:
.org 0x1BB9C
m68k_01bb9c:
        swap %d0
m68k_01bb9c_end:
.org 0x1BB9E
m68k_01bb9e:
        addi.w #0x32,%d0
m68k_01bb9e_end:
.org 0x1BBA2
m68k_01bba2:
        lea.l 0xc800:w,%a0
m68k_01bba2_end:
.org 0x1BBA6
m68k_01bba6:
        move.w 0xf3a6:w,%d1
m68k_01bba6_end:
.org 0x1BBAA
m68k_01bbaa:
        lsl.w #0x2,%d1
m68k_01bbaa_end:
.org 0x1BBAC
m68k_01bbac:
        move.w 0x2(%a0, %d1.w),%d3
m68k_01bbac_end:
.org 0x1BBB0
m68k_01bbb0:
        mulu.w %d3,%d0
m68k_01bbb0_end:
.org 0x1BBB2
m68k_01bbb2:
        divu.w #0x64,%d0
m68k_01bbb2_end:
.org 0x1BBB6
m68k_01bbb6:
        sub.w %d0,%d3
m68k_01bbb6_end:
.org 0x1BBB8
m68k_01bbb8:
        move.w %d3,0x2(%a0, %d1.w)
m68k_01bbb8_end:
.org 0x1BBBC
m68k_01bbbc:
        andi.l #0xffff,%d0
m68k_01bbbc_end:
.org 0x1BBC2
m68k_01bbc2:
        divu.w #0x64,%d0
m68k_01bbc2_end:
.org 0x1BBC6
m68k_01bbc6:
        move.w %d0,0xefba:w
m68k_01bbc6_end:
.org 0x1BBCA
m68k_01bbca:
        jsr 0x83d4:l
m68k_01bbca_end:
.org 0x1BBD0
m68k_01bbd0:
        andi.l #0xffff,%d0
m68k_01bbd0_end:
.org 0x1BBD6
m68k_01bbd6:
        move.l %d0,%d1
m68k_01bbd6_end:
.org 0x1BBD8
m68k_01bbd8:
        lsl.l #0x6,%d0
m68k_01bbd8_end:
.org 0x1BBDA
m68k_01bbda:
        lsl.l #0x2,%d1
m68k_01bbda_end:
.org 0x1BBDC
m68k_01bbdc:
        sub.l %d1,%d0
m68k_01bbdc_end:
.org 0x1BBDE
m68k_01bbde:
        swap %d0
m68k_01bbde_end:
.org 0x1BBE0
m68k_01bbe0:
        lea.l 0xb200:w,%a0
m68k_01bbe0_end:
.org 0x1BBE4
m68k_01bbe4:
        move.w 0xf3a6:w,%d1
m68k_01bbe4_end:
.org 0x1BBE8
m68k_01bbe8:
        lsl.w #0x1,%d1
m68k_01bbe8_end:
.org 0x1BBEA
m68k_01bbea:
        move.w (%a0, %d1.w),%d3
m68k_01bbea_end:
.org 0x1BBEE
m68k_01bbee:
        mulu.w %d3,%d0
m68k_01bbee_end:
.org 0x1BBF0
m68k_01bbf0:
        divu.w #0x64,%d0
m68k_01bbf0_end:
.org 0x1BBF4
m68k_01bbf4:
        sub.w %d0,%d3
m68k_01bbf4_end:
.org 0x1BBF6
m68k_01bbf6:
        move.w %d3,(%a0, %d1.w)
m68k_01bbf6_end:
.org 0x1BBFA
m68k_01bbfa:
        cmpi.w #0xa,%d3
m68k_01bbfa_end:
.org 0x1BBFE
m68k_01bbfe:
        bhi.w (. + 36)
m68k_01bbfe_end:
.org 0x1BC02
m68k_01bc02:
        clr.w (%a0, %d1.w)
m68k_01bc02_end:
.org 0x1BC06
m68k_01bc06:
        lea.l 0x9000:w,%a2
m68k_01bc06_end:
.org 0x1BC0A
m68k_01bc0a:
        lea.l 0xefbe:w,%a3
m68k_01bc0a_end:
.org 0x1BC0E
m68k_01bc0e:
        move.w 0xefc6:w,%d0
m68k_01bc0e_end:
.org 0x1BC12
m68k_01bc12:
        adda.w (%a3, %d0.w),%a2
m68k_01bc12_end:
.org 0x1BC16
m68k_01bc16:
        move.w 0xf3a6:w,%d0
m68k_01bc16_end:
.org 0x1BC1A
m68k_01bc1a:
        bsr.w (. + -458)
m68k_01bc1a_end:
.org 0x1BC1E
m68k_01bc1e:
        add.w %d1,0xefba:w
m68k_01bc1e_end:
.org 0x1BC22
m68k_01bc22:
        rts
m68k_01bc22_end:
.org 0x1BC24
m68k_01bc24:
        lea.l 0xc000:w,%a0
m68k_01bc24_end:
.org 0x1BC28
m68k_01bc28:
        move.w 0xf3a6:w,%d0
m68k_01bc28_end:
.org 0x1BC2C
m68k_01bc2c:
        lsl.w #0x1,%d0
m68k_01bc2c_end:
.org 0x1BC2E
m68k_01bc2e:
        move.w (%a0, %d0.w),%d1
m68k_01bc2e_end:
.org 0x1BC32
m68k_01bc32:
        add.w 0xefb8:w,%d1
m68k_01bc32_end:
.org 0x1BC36
m68k_01bc36:
        cmpi.w #0x3e7,%d1
m68k_01bc36_end:
.org 0x1BC3A
m68k_01bc3a:
        bls.w (. + 8)
m68k_01bc3a_end:
.org 0x1BC3E
m68k_01bc3e:
        move.w #0x3e7,%d1
m68k_01bc3e_end:
.org 0x1BC42
m68k_01bc42:
        move.w %d1,(%a0, %d0.w)
m68k_01bc42_end:
.org 0x1BC46
m68k_01bc46:
        move.w 0xf3f2:w,%d0
m68k_01bc46_end:
.org 0x1BC4A
m68k_01bc4a:
        lsl.w #0x1,%d0
m68k_01bc4a_end:
.org 0x1BC4C
m68k_01bc4c:
        move.w (%a0, %d0.w),%d1
m68k_01bc4c_end:
.org 0x1BC50
m68k_01bc50:
        add.w 0xefba:w,%d1
m68k_01bc50_end:
.org 0x1BC54
m68k_01bc54:
        cmpi.w #0x3e7,%d1
m68k_01bc54_end:
.org 0x1BC58
m68k_01bc58:
        bls.w (. + 8)
m68k_01bc58_end:
.org 0x1BC5C
m68k_01bc5c:
        move.w #0x3e7,%d1
m68k_01bc5c_end:
.org 0x1BC60
m68k_01bc60:
        move.w %d1,(%a0, %d0.w)
m68k_01bc60_end:
.org 0x1BC64
m68k_01bc64:
        rts
m68k_01bc64_end:
.org 0x1BC66
m68k_01bc66:
        lea.l 0xcc00:w,%a0
m68k_01bc66_end:
.org 0x1BC6A
m68k_01bc6a:
        move.w 0xf3a6:w,%d0
m68k_01bc6a_end:
.org 0x1BC6E
m68k_01bc6e:
        move.b (%a0, %d0.w),%d0
m68k_01bc6e_end:
.org 0x1BC72
m68k_01bc72:
        andi.w #0x3f,%d0
m68k_01bc72_end:
.org 0x1BC76
m68k_01bc76:
        lea.l 0xf427:w,%a0
m68k_01bc76_end:
.org 0x1BC7A
m68k_01bc7a:
        move.b (%a0, %d0.w),%d0
m68k_01bc7a_end:
.org 0x1BC7E
m68k_01bc7e:
        lsl.w #0x1,%d0
m68k_01bc7e_end:
.org 0x1BC80
m68k_01bc80:
        lea.l 0xe640:w,%a0
m68k_01bc80_end:
.org 0x1BC84
m68k_01bc84:
        move.w (%a0, %d0.w),%d0
m68k_01bc84_end:
.org 0x1BC88
m68k_01bc88:
        cmp.w 0xf3a6:w,%d0
m68k_01bc88_end:
.org 0x1BC8C
m68k_01bc8c:
        beq.w (. + 70)
m68k_01bc8c_end:
.org 0x1BC90
m68k_01bc90:
        movea.l 0xff382c:l,%a0
m68k_01bc90_end:
.org 0x1BC96
m68k_01bc96:
        lea.l 0x9000:w,%a1
m68k_01bc96_end:
.org 0x1BC9A
m68k_01bc9a:
        lea.l 0xefbe:w,%a2
m68k_01bc9a_end:
.org 0x1BC9E
m68k_01bc9e:
        move.w 0xefc6:w,%d0
m68k_01bc9e_end:
.org 0x1BCA2
m68k_01bca2:
        adda.w (%a2, %d0.w),%a1
m68k_01bca2_end:
.org 0x1BCA6
m68k_01bca6:
        move.b (%a0),%d0
m68k_01bca6_end:
.org 0x1BCA8
m68k_01bca8:
        andi.w #0xf,%d0
m68k_01bca8_end:
.org 0x1BCAC
m68k_01bcac:
        cmpi.w #0xa,%d0
m68k_01bcac_end:
.org 0x1BCB0
m68k_01bcb0:
        bcc.w (. + 34)
m68k_01bcb0_end:
.org 0x1BCB4
m68k_01bcb4:
        lea.l 0xb200:w,%a2
m68k_01bcb4_end:
.org 0x1BCB8
m68k_01bcb8:
        move.w 0xf3a6:w,%d1
m68k_01bcb8_end:
.org 0x1BCBC
m68k_01bcbc:
        lsl.w #0x1,%d1
m68k_01bcbc_end:
.org 0x1BCBE
m68k_01bcbe:
        move.w (%a2, %d1.w),%d2
m68k_01bcbe_end:
.org 0x1BCC2
m68k_01bcc2:
        beq.w (. + 16)
m68k_01bcc2_end:
.org 0x1BCC6
m68k_01bcc6:
        cmpi.w #0x19,%d2
m68k_01bcc6_end:
.org 0x1BCCA
m68k_01bcca:
        bcc.w (. + 8)
m68k_01bcca_end:
.org 0x1BCCE
m68k_01bcce:
        bsr.w (. + 116)
m68k_01bcce_end:
.org 0x1BCD2
m68k_01bcd2:
        rts
m68k_01bcd2_end:
.org 0x1BCD4
m68k_01bcd4:
        lea.l 0xcc00:w,%a0
m68k_01bcd4_end:
.org 0x1BCD8
m68k_01bcd8:
        move.w 0xf3f2:w,%d0
m68k_01bcd8_end:
.org 0x1BCDC
m68k_01bcdc:
        move.b (%a0, %d0.w),%d0
m68k_01bcdc_end:
.org 0x1BCE0
m68k_01bce0:
        andi.w #0x3f,%d0
m68k_01bce0_end:
.org 0x1BCE4
m68k_01bce4:
        lea.l 0xf427:w,%a0
m68k_01bce4_end:
.org 0x1BCE8
m68k_01bce8:
        move.b (%a0, %d0.w),%d0
m68k_01bce8_end:
.org 0x1BCEC
m68k_01bcec:
        lsl.w #0x1,%d0
m68k_01bcec_end:
.org 0x1BCEE
m68k_01bcee:
        lea.l 0xe640:w,%a0
m68k_01bcee_end:
.org 0x1BCF2
m68k_01bcf2:
        move.w (%a0, %d0.w),%d0
m68k_01bcf2_end:
.org 0x1BCF6
m68k_01bcf6:
        cmp.w 0xf3a6:w,%d0
m68k_01bcf6_end:
.org 0x1BCFA
m68k_01bcfa:
        beq.w (. + 70)
m68k_01bcfa_end:
.org 0x1BCFE
m68k_01bcfe:
        lea.l 0x9000:w,%a0
m68k_01bcfe_end:
.org 0x1BD02
m68k_01bd02:
        lea.l 0xefbe:w,%a2
m68k_01bd02_end:
.org 0x1BD06
m68k_01bd06:
        move.w 0xefc6:w,%d0
m68k_01bd06_end:
.org 0x1BD0A
m68k_01bd0a:
        adda.w (%a2, %d0.w),%a0
m68k_01bd0a_end:
.org 0x1BD0E
m68k_01bd0e:
        movea.l 0xff382c:l,%a1
m68k_01bd0e_end:
.org 0x1BD14
m68k_01bd14:
        move.b (%a0),%d0
m68k_01bd14_end:
.org 0x1BD16
m68k_01bd16:
        andi.w #0xf,%d0
m68k_01bd16_end:
.org 0x1BD1A
m68k_01bd1a:
        cmpi.w #0xa,%d0
m68k_01bd1a_end:
.org 0x1BD1E
m68k_01bd1e:
        bcc.w (. + 34)
m68k_01bd1e_end:
.org 0x1BD22
m68k_01bd22:
        lea.l 0xb200:w,%a2
m68k_01bd22_end:
.org 0x1BD26
m68k_01bd26:
        move.w 0xf3f2:w,%d1
m68k_01bd26_end:
.org 0x1BD2A
m68k_01bd2a:
        lsl.w #0x1,%d1
m68k_01bd2a_end:
.org 0x1BD2C
m68k_01bd2c:
        move.w (%a2, %d1.w),%d2
m68k_01bd2c_end:
.org 0x1BD30
m68k_01bd30:
        beq.w (. + 16)
m68k_01bd30_end:
.org 0x1BD34
m68k_01bd34:
        cmpi.w #0x19,%d2
m68k_01bd34_end:
.org 0x1BD38
m68k_01bd38:
        bcc.w (. + 8)
m68k_01bd38_end:
.org 0x1BD3C
m68k_01bd3c:
        bsr.w (. + 6)
m68k_01bd3c_end:
.org 0x1BD40
m68k_01bd40:
        rts
m68k_01bd40_end:
.org 0x1BD42
m68k_01bd42:
        lsr.w #0x1,%d1
m68k_01bd42_end:
.org 0x1BD44
m68k_01bd44:
        lea.l 0xd(%a0, %d0.w),%a2
m68k_01bd44_end:
.org 0x1BD48
m68k_01bd48:
        move.b (%a2),%d2
m68k_01bd48_end:
.org 0x1BD4A
m68k_01bd4a:
        move.w %d2,%d3
m68k_01bd4a_end:
.org 0x1BD4C
m68k_01bd4c:
        andi.w #0xf,%d3
m68k_01bd4c_end:
.org 0x1BD50
m68k_01bd50:
        beq.w (. + 26)
m68k_01bd50_end:
.org 0x1BD54
m68k_01bd54:
        addi.w #0xc,%d3
m68k_01bd54_end:
.org 0x1BD58
m68k_01bd58:
        move.b 0x1(%a2),%d4
m68k_01bd58_end:
.org 0x1BD5C
m68k_01bd5c:
        move.b %d2,0x1(%a2)
m68k_01bd5c_end:
.org 0x1BD60
m68k_01bd60:
        move.b %d4,%d2
m68k_01bd60_end:
.org 0x1BD62
m68k_01bd62:
        addq.w #0x1,%a2
m68k_01bd62_end:
.org 0x1BD64
m68k_01bd64:
        dbra %d3,(. + -12)
m68k_01bd64_end:
.org 0x1BD68
m68k_01bd68:
        bra.b (. + -30)
m68k_01bd68_end:
.org 0x1BD6A
m68k_01bd6a:
        clr.b 0x1(%a2)
m68k_01bd6a_end:
.org 0x1BD6E
m68k_01bd6e:
        move.b %d1,0xd(%a0, %d0.w)
m68k_01bd6e_end:
.org 0x1BD72
m68k_01bd72:
        addq.b #0x1,(%a0)
m68k_01bd72_end:
.org 0x1BD74
m68k_01bd74:
        exg %d0,%a0
m68k_01bd74_end:
.org 0x1BD76
m68k_01bd76:
        exg %d1,%a1
m68k_01bd76_end:
.org 0x1BD78
m68k_01bd78:
        cmp.l %d0,%d1
m68k_01bd78_end:
.org 0x1BD7A
m68k_01bd7a:
        bcs.w (. + 6)
m68k_01bd7a_end:
.org 0x1BD7E
m68k_01bd7e:
        addq.w #0x1,%d1
m68k_01bd7e_end:
.org 0x1BD80
m68k_01bd80:
        exg %d0,%a0
m68k_01bd80_end:
.org 0x1BD82
m68k_01bd82:
        exg %d1,%a1
m68k_01bd82_end:
.org 0x1BD84
m68k_01bd84:
        clr.w %d7
m68k_01bd84_end:
.org 0x1BD86
m68k_01bd86:
        clr.w 0xf746:w
m68k_01bd86_end:
.org 0x1BD8A
m68k_01bd8a:
        move.b 0xd(%a1),0xf747:w
m68k_01bd8a_end:
.org 0x1BD90
m68k_01bd90:
        move.b (%a1),%d2
m68k_01bd90_end:
.org 0x1BD92
m68k_01bd92:
        andi.w #0xf,%d2
m68k_01bd92_end:
.org 0x1BD96
m68k_01bd96:
        cmpi.w #0x1,%d2
m68k_01bd96_end:
.org 0x1BD9A
m68k_01bd9a:
        beq.w (. + 64)
m68k_01bd9a_end:
.org 0x1BD9E
m68k_01bd9e:
        clr.w %d3
m68k_01bd9e_end:
.org 0x1BDA0
m68k_01bda0:
        subq.w #0x1,%d2
m68k_01bda0_end:
.org 0x1BDA2
m68k_01bda2:
        cmp.b 0xd(%a1, %d3.w),%d1
m68k_01bda2_end:
.org 0x1BDA6
m68k_01bda6:
        beq.w (. + 8)
m68k_01bda6_end:
.org 0x1BDAA
m68k_01bdaa:
        addq.w #0x1,%d3
m68k_01bdaa_end:
.org 0x1BDAC
m68k_01bdac:
        bra.b (. + -12)
m68k_01bdac_end:
.org 0x1BDAE
m68k_01bdae:
        subq.w #0x1,%d2
m68k_01bdae_end:
.org 0x1BDB0
m68k_01bdb0:
        bmi.w (. + 12)
m68k_01bdb0_end:
.org 0x1BDB4
m68k_01bdb4:
        move.b 0xe(%a1, %d3.w),0xd(%a1, %d3.w)
m68k_01bdb4_end:
.org 0x1BDBA
m68k_01bdba:
        bra.b (. + -12)
m68k_01bdba_end:
.org 0x1BDBC
m68k_01bdbc:
        clr.w 0xf744:w
m68k_01bdbc_end:
.org 0x1BDC0
m68k_01bdc0:
        move.b 0xd(%a1),0xf745:w
m68k_01bdc0_end:
.org 0x1BDC6
m68k_01bdc6:
        move.b (%a1),%d2
m68k_01bdc6_end:
.org 0x1BDC8
m68k_01bdc8:
        andi.w #0xf,%d2
m68k_01bdc8_end:
.org 0x1BDCC
m68k_01bdcc:
        lea.l 0xd(%a1, %d2.w),%a2
m68k_01bdcc_end:
.org 0x1BDD0
m68k_01bdd0:
        lea.l 0xc(%a1, %d2.w),%a3
m68k_01bdd0_end:
.org 0x1BDD4
m68k_01bdd4:
        subq.b #0x1,(%a1)
m68k_01bdd4_end:
.org 0x1BDD6
m68k_01bdd6:
        bra.w (. + 20)
m68k_01bdd6_end:
.org 0x1BDDA
m68k_01bdda:
        lea.l 0xd(%a1, %d2.w),%a2
m68k_01bdda_end:
.org 0x1BDDE
m68k_01bdde:
        lea.l (%a1),%a3
m68k_01bdde_end:
.org 0x1BDE0
m68k_01bde0:
        move.w #0x1,%d7
m68k_01bde0_end:
.org 0x1BDE4
m68k_01bde4:
        move.w #0xffff,0xf744:w
m68k_01bde4_end:
.org 0x1BDEA
m68k_01bdea:
        move.b (%a2),%d2
m68k_01bdea_end:
.org 0x1BDEC
m68k_01bdec:
        andi.w #0xf,%d2
m68k_01bdec_end:
.org 0x1BDF0
m68k_01bdf0:
        beq.w (. + 16)
m68k_01bdf0_end:
.org 0x1BDF4
m68k_01bdf4:
        addi.w #0xc,%d2
m68k_01bdf4_end:
.org 0x1BDF8
m68k_01bdf8:
        move.b (%a2)+,(%a3)+
m68k_01bdf8_end:
.org 0x1BDFA
m68k_01bdfa:
        dbra %d2,(. + -2)
m68k_01bdfa_end:
.org 0x1BDFE
m68k_01bdfe:
        bra.b (. + -20)
m68k_01bdfe_end:
.org 0x1BE00
m68k_01be00:
        clr.b (%a3)
m68k_01be00_end:
.org 0x1BE02
m68k_01be02:
        move.b (%a0),%d0
m68k_01be02_end:
.org 0x1BE04
m68k_01be04:
        andi.w #0xf,%d0
m68k_01be04_end:
.org 0x1BE08
m68k_01be08:
        lea.l 0xc400:w,%a2
m68k_01be08_end:
.org 0x1BE0C
m68k_01be0c:
        move.w %d0,%d1
m68k_01be0c_end:
.org 0x1BE0E
m68k_01be0e:
        subq.w #0x1,%d1
m68k_01be0e_end:
.org 0x1BE10
m68k_01be10:
        clr.w %d2
m68k_01be10_end:
.org 0x1BE12
m68k_01be12:
        clr.w %d3
m68k_01be12_end:
.org 0x1BE14
m68k_01be14:
        move.b 0xd(%a0, %d1.w),%d2
m68k_01be14_end:
.org 0x1BE18
m68k_01be18:
        move.b (%a2, %d2.w),%d2
m68k_01be18_end:
.org 0x1BE1C
m68k_01be1c:
        add.w %d2,%d3
m68k_01be1c_end:
.org 0x1BE1E
m68k_01be1e:
        dbra %d1,(. + -10)
m68k_01be1e_end:
.org 0x1BE22
m68k_01be22:
        andi.l #0xffff,%d3
m68k_01be22_end:
.org 0x1BE28
m68k_01be28:
        divu.w %d0,%d3
m68k_01be28_end:
.org 0x1BE2A
m68k_01be2a:
        move.b %d3,0x3(%a0)
m68k_01be2a_end:
.org 0x1BE2E
m68k_01be2e:
        tst.w %d7
m68k_01be2e_end:
.org 0x1BE30
m68k_01be30:
        bne.w (. + 44)
m68k_01be30_end:
.org 0x1BE34
m68k_01be34:
        move.b (%a1),%d0
m68k_01be34_end:
.org 0x1BE36
m68k_01be36:
        andi.w #0xf,%d0
m68k_01be36_end:
.org 0x1BE3A
m68k_01be3a:
        move.w %d0,%d1
m68k_01be3a_end:
.org 0x1BE3C
m68k_01be3c:
        subq.w #0x1,%d1
m68k_01be3c_end:
.org 0x1BE3E
m68k_01be3e:
        clr.w %d2
m68k_01be3e_end:
.org 0x1BE40
m68k_01be40:
        clr.w %d3
m68k_01be40_end:
.org 0x1BE42
m68k_01be42:
        move.b 0xd(%a1, %d1.w),%d2
m68k_01be42_end:
.org 0x1BE46
m68k_01be46:
        move.b (%a2, %d2.w),%d2
m68k_01be46_end:
.org 0x1BE4A
m68k_01be4a:
        add.w %d2,%d3
m68k_01be4a_end:
.org 0x1BE4C
m68k_01be4c:
        dbra %d1,(. + -10)
m68k_01be4c_end:
.org 0x1BE50
m68k_01be50:
        andi.l #0xffff,%d3
m68k_01be50_end:
.org 0x1BE56
m68k_01be56:
        divu.w %d0,%d3
m68k_01be56_end:
.org 0x1BE58
m68k_01be58:
        move.b %d3,0x3(%a1)
m68k_01be58_end:
.org 0x1BE5C
m68k_01be5c:
        bsr.w (. + 6)
m68k_01be5c_end:
.org 0x1BE60
m68k_01be60:
        rts
m68k_01be60_end:
.org 0x1BE62
m68k_01be62:
        movem.l %d0/%a0,-(%a7)
m68k_01be62_end:
.org 0x1BE66
m68k_01be66:
        move.w 0xf746:w,%d0
m68k_01be66_end:
.org 0x1BE6A
m68k_01be6a:
        cmp.w 0xf744:w,%d0
m68k_01be6a_end:
.org 0x1BE6E
m68k_01be6e:
        beq.w (. + 96)
m68k_01be6e_end:
.org 0x1BE72
m68k_01be72:
        lea.l 0xff39b2:l,%a0
m68k_01be72_end:
.org 0x1BE78
m68k_01be78:
        adda.w 0xff3bb2:l,%a0
m68k_01be78_end:
.org 0x1BE7E
m68k_01be7e:
        tst.w %d7
m68k_01be7e_end:
.org 0x1BE80
m68k_01be80:
        bne.w (. + 54)
m68k_01be80_end:
.org 0x1BE84
m68k_01be84:
        tst.b (%a0)+
m68k_01be84_end:
.org 0x1BE86
m68k_01be86:
        beq.w (. + 72)
m68k_01be86_end:
.org 0x1BE8A
m68k_01be8a:
        cmp.b (%a0)+,%d0
m68k_01be8a_end:
.org 0x1BE8C
m68k_01be8c:
        bne.b (. + -8)
m68k_01be8c_end:
.org 0x1BE8E
m68k_01be8e:
        move.b 0xf745:w,-0x1(%a0)
m68k_01be8e_end:
.org 0x1BE94
m68k_01be94:
        lea.l 0xff3000:l,%a0
m68k_01be94_end:
.org 0x1BE9A
m68k_01be9a:
        tst.b (%a0)+
m68k_01be9a_end:
.org 0x1BE9C
m68k_01be9c:
        bmi.w (. + 50)
m68k_01be9c_end:
.org 0x1BEA0
m68k_01bea0:
        cmp.b (%a0)+,%d0
m68k_01bea0_end:
.org 0x1BEA2
m68k_01bea2:
        beq.w (. + 10)
m68k_01bea2_end:
.org 0x1BEA6
m68k_01bea6:
        tst.b (%a0)+
m68k_01bea6_end:
.org 0x1BEA8
m68k_01bea8:
        bne.b (. + -2)
m68k_01bea8_end:
.org 0x1BEAA
m68k_01beaa:
        bra.b (. + -16)
m68k_01beaa_end:
.org 0x1BEAC
m68k_01beac:
        move.b 0xf745:w,-0x1(%a0)
m68k_01beac_end:
.org 0x1BEB2
m68k_01beb2:
        bra.w (. + 28)
m68k_01beb2_end:
.org 0x1BEB6
m68k_01beb6:
        tst.b (%a0)+
m68k_01beb6_end:
.org 0x1BEB8
m68k_01beb8:
        beq.w (. + 22)
m68k_01beb8_end:
.org 0x1BEBC
m68k_01bebc:
        cmp.b (%a0)+,%d0
m68k_01bebc_end:
.org 0x1BEBE
m68k_01bebe:
        bne.b (. + -8)
m68k_01bebe_end:
.org 0x1BEC0
m68k_01bec0:
        move.b (%a0)+,-0x3(%a0)
m68k_01bec0_end:
.org 0x1BEC4
m68k_01bec4:
        beq.w (. + 10)
m68k_01bec4_end:
.org 0x1BEC8
m68k_01bec8:
        move.b (%a0)+,-0x3(%a0)
m68k_01bec8_end:
.org 0x1BECC
m68k_01becc:
        bra.b (. + -12)
m68k_01becc_end:
.org 0x1BECE
m68k_01bece:
        movem.l (%a7)+,%d0/%a0
m68k_01bece_end:
.org 0x1BED2
m68k_01bed2:
        rts
m68k_01bed2_end:
.org 0x1BED4
m68k_01bed4:
        jsr 0x83d4:l
m68k_01bed4_end:
.org 0x1BEDA
m68k_01beda:
        andi.l #0xffff,%d0
m68k_01beda_end:
.org 0x1BEE0
m68k_01bee0:
        move.l %d0,%d1
m68k_01bee0_end:
.org 0x1BEE2
m68k_01bee2:
        lsl.l #0x1,%d0
m68k_01bee2_end:
.org 0x1BEE4
m68k_01bee4:
        add.l %d1,%d0
m68k_01bee4_end:
.org 0x1BEE6
m68k_01bee6:
        lsl.l #0x3,%d0
m68k_01bee6_end:
.org 0x1BEE8
m68k_01bee8:
        add.l %d1,%d0
m68k_01bee8_end:
.org 0x1BEEA
m68k_01beea:
        lsl.l #0x1,%d0
m68k_01beea_end:
.org 0x1BEEC
m68k_01beec:
        add.l %d1,%d0
m68k_01beec_end:
.org 0x1BEEE
m68k_01beee:
        swap %d0
m68k_01beee_end:
.org 0x1BEF0
m68k_01bef0:
        addi.w #0x32,%d0
m68k_01bef0_end:
.org 0x1BEF4
m68k_01bef4:
        lea.l 0xc800:w,%a0
m68k_01bef4_end:
.org 0x1BEF8
m68k_01bef8:
        move.w 0xf3f2:w,%d1
m68k_01bef8_end:
.org 0x1BEFC
m68k_01befc:
        lsl.w #0x2,%d1
m68k_01befc_end:
.org 0x1BEFE
m68k_01befe:
        move.w 0x2(%a0, %d1.w),%d3
m68k_01befe_end:
.org 0x1BF02
m68k_01bf02:
        mulu.w %d3,%d0
m68k_01bf02_end:
.org 0x1BF04
m68k_01bf04:
        divu.w #0x64,%d0
m68k_01bf04_end:
.org 0x1BF08
m68k_01bf08:
        sub.w %d0,%d3
m68k_01bf08_end:
.org 0x1BF0A
m68k_01bf0a:
        move.w %d3,0x2(%a0, %d1.w)
m68k_01bf0a_end:
.org 0x1BF0E
m68k_01bf0e:
        andi.l #0xffff,%d0
m68k_01bf0e_end:
.org 0x1BF14
m68k_01bf14:
        divu.w #0x64,%d0
m68k_01bf14_end:
.org 0x1BF18
m68k_01bf18:
        move.w %d0,0xefb8:w
m68k_01bf18_end:
.org 0x1BF1C
m68k_01bf1c:
        jsr 0x83d4:l
m68k_01bf1c_end:
.org 0x1BF22
m68k_01bf22:
        andi.l #0xffff,%d0
m68k_01bf22_end:
.org 0x1BF28
m68k_01bf28:
        mulu.w #0x3d,%d0
m68k_01bf28_end:
.org 0x1BF2C
m68k_01bf2c:
        swap %d0
m68k_01bf2c_end:
.org 0x1BF2E
m68k_01bf2e:
        lea.l 0xb200:w,%a0
m68k_01bf2e_end:
.org 0x1BF32
m68k_01bf32:
        move.w 0xf3f2:w,%d3
m68k_01bf32_end:
.org 0x1BF36
m68k_01bf36:
        lsl.w #0x1,%d3
m68k_01bf36_end:
.org 0x1BF38
m68k_01bf38:
        move.w (%a0, %d3.w),%d1
m68k_01bf38_end:
.org 0x1BF3C
m68k_01bf3c:
        mulu.w %d1,%d0
m68k_01bf3c_end:
.org 0x1BF3E
m68k_01bf3e:
        divu.w #0x64,%d0
m68k_01bf3e_end:
.org 0x1BF42
m68k_01bf42:
        sub.w %d0,%d1
m68k_01bf42_end:
.org 0x1BF44
m68k_01bf44:
        move.w %d1,(%a0, %d3.w)
m68k_01bf44_end:
.org 0x1BF48
m68k_01bf48:
        cmpi.w #0xa,%d1
m68k_01bf48_end:
.org 0x1BF4C
m68k_01bf4c:
        bhi.w (. + 26)
m68k_01bf4c_end:
.org 0x1BF50
m68k_01bf50:
        clr.w (%a0, %d3.w)
m68k_01bf50_end:
.org 0x1BF54
m68k_01bf54:
        movea.l 0xff382c:l,%a2
m68k_01bf54_end:
.org 0x1BF5A
m68k_01bf5a:
        move.w 0xf3f2:w,%d0
m68k_01bf5a_end:
.org 0x1BF5E
m68k_01bf5e:
        bsr.w (. + -1294)
m68k_01bf5e_end:
.org 0x1BF62
m68k_01bf62:
        add.w %d1,0xefb8:w
m68k_01bf62_end:
.org 0x1BF66
m68k_01bf66:
        rts
m68k_01bf66_end:
.org 0x1BF68
m68k_01bf68:
        jsr 0x83d4:l
m68k_01bf68_end:
.org 0x1BF6E
m68k_01bf6e:
        andi.l #0xffff,%d0
m68k_01bf6e_end:
.org 0x1BF74
m68k_01bf74:
        move.l %d0,%d1
m68k_01bf74_end:
.org 0x1BF76
m68k_01bf76:
        lsl.l #0x5,%d0
m68k_01bf76_end:
.org 0x1BF78
m68k_01bf78:
        sub.l %d1,%d0
m68k_01bf78_end:
.org 0x1BF7A
m68k_01bf7a:
        swap %d0
m68k_01bf7a_end:
.org 0x1BF7C
m68k_01bf7c:
        addi.w #0x1e,%d0
m68k_01bf7c_end:
.org 0x1BF80
m68k_01bf80:
        lea.l 0xc800:w,%a0
m68k_01bf80_end:
.org 0x1BF84
m68k_01bf84:
        move.w 0xf3a6:w,%d1
m68k_01bf84_end:
.org 0x1BF88
m68k_01bf88:
        lsl.w #0x2,%d1
m68k_01bf88_end:
.org 0x1BF8A
m68k_01bf8a:
        move.w 0x2(%a0, %d1.w),%d3
m68k_01bf8a_end:
.org 0x1BF8E
m68k_01bf8e:
        mulu.w %d3,%d0
m68k_01bf8e_end:
.org 0x1BF90
m68k_01bf90:
        divu.w #0x64,%d0
m68k_01bf90_end:
.org 0x1BF94
m68k_01bf94:
        sub.w %d0,%d3
m68k_01bf94_end:
.org 0x1BF96
m68k_01bf96:
        move.w %d3,0x2(%a0, %d1.w)
m68k_01bf96_end:
.org 0x1BF9A
m68k_01bf9a:
        andi.l #0xffff,%d0
m68k_01bf9a_end:
.org 0x1BFA0
m68k_01bfa0:
        divu.w #0x64,%d0
m68k_01bfa0_end:
.org 0x1BFA4
m68k_01bfa4:
        move.w %d0,0xefba:w
m68k_01bfa4_end:
.org 0x1BFA8
m68k_01bfa8:
        jsr 0x83d4:l
m68k_01bfa8_end:
.org 0x1BFAE
m68k_01bfae:
        andi.l #0xffff,%d0
m68k_01bfae_end:
.org 0x1BFB4
m68k_01bfb4:
        move.l %d0,%d1
m68k_01bfb4_end:
.org 0x1BFB6
m68k_01bfb6:
        lsl.l #0x5,%d0
m68k_01bfb6_end:
.org 0x1BFB8
m68k_01bfb8:
        sub.l %d1,%d0
m68k_01bfb8_end:
.org 0x1BFBA
m68k_01bfba:
        swap %d0
m68k_01bfba_end:
.org 0x1BFBC
m68k_01bfbc:
        lea.l 0xb200:w,%a0
m68k_01bfbc_end:
.org 0x1BFC0
m68k_01bfc0:
        move.w 0xf3a6:w,%d1
m68k_01bfc0_end:
.org 0x1BFC4
m68k_01bfc4:
        lsl.w #0x1,%d1
m68k_01bfc4_end:
.org 0x1BFC6
m68k_01bfc6:
        move.w (%a0, %d1.w),%d3
m68k_01bfc6_end:
.org 0x1BFCA
m68k_01bfca:
        mulu.w %d3,%d0
m68k_01bfca_end:
.org 0x1BFCC
m68k_01bfcc:
        divu.w #0x64,%d0
m68k_01bfcc_end:
.org 0x1BFD0
m68k_01bfd0:
        sub.w %d0,%d3
m68k_01bfd0_end:
.org 0x1BFD2
m68k_01bfd2:
        bne.w (. + 8)
m68k_01bfd2_end:
.org 0x1BFD6
m68k_01bfd6:
        move.w #0x1,%d3
m68k_01bfd6_end:
.org 0x1BFDA
m68k_01bfda:
        move.w %d3,(%a0, %d1.w)
m68k_01bfda_end:
.org 0x1BFDE
m68k_01bfde:
        rts
m68k_01bfde_end:
.org 0x1BFE0
m68k_01bfe0:
        cmpi.b #0xb8,0xf579:w
m68k_01bfe0_end:
.org 0x1BFE6
m68k_01bfe6:
        bne.w (. + -2530)
m68k_01bfe6_end:
.org 0x1BFEA
m68k_01bfea:
        rts
m68k_01bfea_end:
