| 候选处理入口 01A818。candidate_action.s 提供共享的随机数例程。
.cpu 68000
.section .text
_start:
.org 0x1A706
m68k_01a706:
        move.w 0xefd2:w,%d5
m68k_01a706_end:
.org 0x1A70A
m68k_01a70a:
        lsl.w #0x1,%d5
m68k_01a70a_end:
.org 0x1A70C
m68k_01a70c:
        add.w 0xefd2:w,%d5
m68k_01a70c_end:
.org 0x1A710
m68k_01a710:
        lsl.w #0x3,%d5
m68k_01a710_end:
.org 0x1A712
m68k_01a712:
        lea.l 0xd300:w,%a0
m68k_01a712_end:
.org 0x1A716
m68k_01a716:
        lea.l 0xc700:w,%a2
m68k_01a716_end:
.org 0x1A71A
m68k_01a71a:
        clr.w %d1
m68k_01a71a_end:
.org 0x1A71C
m68k_01a71c:
        lea.l 0xa550:w,%a1
m68k_01a71c_end:
.org 0x1A720
m68k_01a720:
        bsr.w (. + 106)
m68k_01a720_end:
.org 0x1A724
m68k_01a724:
        move.w #0x2,%d1
m68k_01a724_end:
.org 0x1A728
m68k_01a728:
        lea.l 0xa5a4:w,%a1
m68k_01a728_end:
.org 0x1A72C
m68k_01a72c:
        bsr.w (. + 94)
m68k_01a72c_end:
.org 0x1A730
m68k_01a730:
        move.w #0xffff,(%a0)
m68k_01a730_end:
.org 0x1A734
m68k_01a734:
        tst.w 0xd300:w
m68k_01a734_end:
.org 0x1A738
m68k_01a738:
        bmi.w (. + 54)
m68k_01a738_end:
.org 0x1A73C
m68k_01a73c:
        addq.w #0x4,%d5
m68k_01a73c_end:
.org 0x1A73E
m68k_01a73e:
        lea.l 0xd300:w,%a0
m68k_01a73e_end:
.org 0x1A742
m68k_01a742:
        lea.l 0xb600:w,%a1
m68k_01a742_end:
.org 0x1A746
m68k_01a746:
        clr.w %d0
m68k_01a746_end:
.org 0x1A748
m68k_01a748:
        move.w (%a0)+,%d2
m68k_01a748_end:
.org 0x1A74A
m68k_01a74a:
        bmi.b (. + 20)
m68k_01a74a_end:
.org 0x1A74C
m68k_01a74c:
        move.w %d2,%d3
m68k_01a74c_end:
.org 0x1A74E
m68k_01a74e:
        lsl.w #0x1,%d3
m68k_01a74e_end:
.org 0x1A750
m68k_01a750:
        move.w (%a1, %d3.w),%d4
m68k_01a750_end:
.org 0x1A754
m68k_01a754:
        cmp.w %d0,%d4
m68k_01a754_end:
.org 0x1A756
m68k_01a756:
        bcs.b (. + -14)
m68k_01a756_end:
.org 0x1A758
m68k_01a758:
        move.w %d2,%d1
m68k_01a758_end:
.org 0x1A75A
m68k_01a75a:
        move.w %d4,%d0
m68k_01a75a_end:
.org 0x1A75C
m68k_01a75c:
        bra.b (. + -20)
m68k_01a75c_end:
.org 0x1A75E
m68k_01a75e:
        lsr.w #0x4,%d1
m68k_01a75e_end:
.org 0x1A760
m68k_01a760:
        move.w 0xf6d6:w,%d0
m68k_01a760_end:
.org 0x1A764
m68k_01a764:
        eor.w %d0,%d1
m68k_01a764_end:
.org 0x1A766
m68k_01a766:
        btst.l #0x1,%d1
m68k_01a766_end:
.org 0x1A76A
m68k_01a76a:
        beq.b (. + 4)
m68k_01a76a_end:
.org 0x1A76C
m68k_01a76c:
        addq.w #0x4,%d5
m68k_01a76c_end:
.org 0x1A76E
m68k_01a76e:
        jsr 0x83d4:l
m68k_01a76e_end:
.org 0x1A774
m68k_01a774:
        andi.l #0xffff,%d0
m68k_01a774_end:
.org 0x1A77A
m68k_01a77a:
        lea.l -1440(%pc),%a0
m68k_01a77a_end:
.org 0x1A77E
m68k_01a77e:
        mulu.w (%a0, %d5.w),%d0
m68k_01a77e_end:
.org 0x1A782
m68k_01a782:
        swap %d0
m68k_01a782_end:
.org 0x1A784
m68k_01a784:
        add.w 0x2(%a0, %d5.w),%d0
m68k_01a784_end:
.org 0x1A788
m68k_01a788:
        rts
m68k_01a788_end:
.org 0x1A78A
m68k_01a78a:
        move.w (%a1)+,%d0
m68k_01a78a_end:
.org 0x1A78C
m68k_01a78c:
        bmi.b (. + 20)
m68k_01a78c_end:
.org 0x1A78E
m68k_01a78e:
        andi.w #0xff,%d0
m68k_01a78e_end:
.org 0x1A792
m68k_01a792:
        btst.b #0x4,(%a2, %d0.w)
m68k_01a792_end:
.org 0x1A798
m68k_01a798:
        beq.b (. + -14)
m68k_01a798_end:
.org 0x1A79A
m68k_01a79a:
        or.w %d1,%d0
m68k_01a79a_end:
.org 0x1A79C
m68k_01a79c:
        move.w %d0,(%a0)+
m68k_01a79c_end:
.org 0x1A79E
m68k_01a79e:
        bra.b (. + -20)
m68k_01a79e_end:
.org 0x1A7A0
m68k_01a7a0:
        rts
m68k_01a7a0_end:
.org 0x1A7A2
m68k_01a7a2:
        mulu.w #0x64,%d0
m68k_01a7a2_end:
.org 0x1A7A6
m68k_01a7a6:
        lea.l 0xb600:w,%a0
m68k_01a7a6_end:
.org 0x1A7AA
m68k_01a7aa:
        move.w 0xf3a6:w,%d1
m68k_01a7aa_end:
.org 0x1A7AE
m68k_01a7ae:
        lsl.w #0x1,%d1
m68k_01a7ae_end:
.org 0x1A7B0
m68k_01a7b0:
        move.w (%a0, %d1.w),%d1
m68k_01a7b0_end:
.org 0x1A7B4
m68k_01a7b4:
        mulu.w %d0,%d1
m68k_01a7b4_end:
.org 0x1A7B6
m68k_01a7b6:
        move.w 0xf3f2:w,%d0
m68k_01a7b6_end:
.org 0x1A7BA
m68k_01a7ba:
        lsl.w #0x1,%d0
m68k_01a7ba_end:
.org 0x1A7BC
m68k_01a7bc:
        move.w (%a0, %d0.w),%d0
m68k_01a7bc_end:
.org 0x1A7C0
m68k_01a7c0:
        mulu.w #0x3e8,%d0
m68k_01a7c0_end:
.org 0x1A7C4
m68k_01a7c4:
        sub.l %d1,%d0
m68k_01a7c4_end:
.org 0x1A7C6
m68k_01a7c6:
        bcs.w (. + 42)
m68k_01a7c6_end:
.org 0x1A7CA
m68k_01a7ca:
        lea.l 0xc000:w,%a0
m68k_01a7ca_end:
.org 0x1A7CE
m68k_01a7ce:
        move.w 0xf3a6:w,%d1
m68k_01a7ce_end:
.org 0x1A7D2
m68k_01a7d2:
        lsl.w #0x1,%d1
m68k_01a7d2_end:
.org 0x1A7D4
m68k_01a7d4:
        move.w (%a0, %d1.w),%d1
m68k_01a7d4_end:
.org 0x1A7D8
m68k_01a7d8:
        addi.w #0x64,%d1
m68k_01a7d8_end:
.org 0x1A7DC
m68k_01a7dc:
        divu.w %d1,%d0
m68k_01a7dc_end:
.org 0x1A7DE
m68k_01a7de:
        move.w %d0,%d7
m68k_01a7de_end:
.org 0x1A7E0
m68k_01a7e0:
        cmpi.w #0x2bc,%d0
m68k_01a7e0_end:
.org 0x1A7E4
m68k_01a7e4:
        bls.w (. + 8)
m68k_01a7e4_end:
.org 0x1A7E8
m68k_01a7e8:
        move.w #0x2bc,%d0
m68k_01a7e8_end:
.org 0x1A7EC
m68k_01a7ec:
        bra.w (. + 6)
m68k_01a7ec_end:
.org 0x1A7F0
m68k_01a7f0:
        clr.w %d7
m68k_01a7f0_end:
.org 0x1A7F2
m68k_01a7f2:
        rts
m68k_01a7f2_end:
.org 0x1A7F4
m68k_01a7f4:
        move.w 0xf6d6:w,%d0
m68k_01a7f4_end:
.org 0x1A7F8
m68k_01a7f8:
        lsl.w #0x2,%d0
m68k_01a7f8_end:
.org 0x1A7FA
m68k_01a7fa:
        movea.l 12(%pc, %d0.w),%a0
m68k_01a7fa_end:
.org 0x1A7FE
m68k_01a7fe:
        move.l (%a0),%d0
m68k_01a7fe_end:
.org 0x1A800
m68k_01a800:
        sub.l 0xf39e:w,%d0
m68k_01a800_end:
.org 0x1A804
m68k_01a804:
        move.l %d0,(%a0)
m68k_01a804_end:
.org 0x1A806
m68k_01a806:
        rts
m68k_01a806_end:
.org 0x1A818
m68k_01a818:
        bsr.b (. + -36)
m68k_01a818_end:
.org 0x1A81A
m68k_01a81a:
        bsr.w (. + -276)
m68k_01a81a_end:
.org 0x1A81E
m68k_01a81e:
        bsr.b (. + -124)
m68k_01a81e_end:
.org 0x1A820
m68k_01a820:
        cmpi.w #0x64,%d7
m68k_01a820_end:
.org 0x1A824
m68k_01a824:
        bcs.w (. + 208)
m68k_01a824_end:
.org 0x1A828
m68k_01a828:
        andi.l #0xffff,%d7
m68k_01a828_end:
.org 0x1A82E
m68k_01a82e:
        divu.w #0x64,%d7
m68k_01a82e_end:
.org 0x1A832
m68k_01a832:
        move.w %d7,%d1
m68k_01a832_end:
.org 0x1A834
m68k_01a834:
        cmpi.w #0x5,%d1
m68k_01a834_end:
.org 0x1A838
m68k_01a838:
        bls.b (. + 6)
m68k_01a838_end:
.org 0x1A83A
m68k_01a83a:
        move.w #0x5,%d1
m68k_01a83a_end:
.org 0x1A83E
m68k_01a83e:
        lsl.w #0x1,%d1
m68k_01a83e_end:
.org 0x1A840
m68k_01a840:
        move.w 0xf3a6:w,%d0
m68k_01a840_end:
.org 0x1A844
m68k_01a844:
        lea.l 0xa654:w,%a0
m68k_01a844_end:
.org 0x1A848
m68k_01a848:
        move.b %d1,(%a0, %d0.w)
m68k_01a848_end:
.org 0x1A84C
m68k_01a84c:
        bsr.w (. + 336)
m68k_01a84c_end:
.org 0x1A850
m68k_01a850:
        lea.l 0xbe00:w,%a0
m68k_01a850_end:
.org 0x1A854
m68k_01a854:
        lea.l 0xc000:w,%a1
m68k_01a854_end:
.org 0x1A858
m68k_01a858:
        move.w 0xf3f2:w,%d0
m68k_01a858_end:
.org 0x1A85C
m68k_01a85c:
        lsl.w #0x1,%d0
m68k_01a85c_end:
.org 0x1A85E
m68k_01a85e:
        move.w %d7,%d1
m68k_01a85e_end:
.org 0x1A860
m68k_01a860:
        lsl.w #0x1,%d1
m68k_01a860_end:
.org 0x1A862
m68k_01a862:
        add.w %d7,%d1
m68k_01a862_end:
.org 0x1A864
m68k_01a864:
        move.w (%a0, %d0.w),%d2
m68k_01a864_end:
.org 0x1A868
m68k_01a868:
        add.w %d1,%d2
m68k_01a868_end:
.org 0x1A86A
m68k_01a86a:
        cmpi.w #0x3e7,%d2
m68k_01a86a_end:
.org 0x1A86E
m68k_01a86e:
        bls.b (. + 6)
m68k_01a86e_end:
.org 0x1A870
m68k_01a870:
        move.w #0x3e7,%d2
m68k_01a870_end:
.org 0x1A874
m68k_01a874:
        move.w %d2,(%a0, %d0.w)
m68k_01a874_end:
.org 0x1A878
m68k_01a878:
        mulu.w #0x3,%d1
m68k_01a878_end:
.org 0x1A87C
m68k_01a87c:
        divu.w #0xa,%d1
m68k_01a87c_end:
.org 0x1A880
m68k_01a880:
        move.w (%a1, %d0.w),%d2
m68k_01a880_end:
.org 0x1A884
m68k_01a884:
        add.w %d1,%d2
m68k_01a884_end:
.org 0x1A886
m68k_01a886:
        cmpi.w #0x3e7,%d2
m68k_01a886_end:
.org 0x1A88A
m68k_01a88a:
        bls.b (. + 6)
m68k_01a88a_end:
.org 0x1A88C
m68k_01a88c:
        move.w #0x3e7,%d2
m68k_01a88c_end:
.org 0x1A890
m68k_01a890:
        move.w %d2,(%a1, %d0.w)
m68k_01a890_end:
.org 0x1A894
m68k_01a894:
        move.w 0xf3a6:w,%d0
m68k_01a894_end:
.org 0x1A898
m68k_01a898:
        lsl.w #0x1,%d0
m68k_01a898_end:
.org 0x1A89A
m68k_01a89a:
        move.w (%a0, %d0.w),%d2
m68k_01a89a_end:
.org 0x1A89E
m68k_01a89e:
        add.w %d7,%d2
m68k_01a89e_end:
.org 0x1A8A0
m68k_01a8a0:
        cmpi.w #0x3e7,%d2
m68k_01a8a0_end:
.org 0x1A8A4
m68k_01a8a4:
        bls.w (. + 8)
m68k_01a8a4_end:
.org 0x1A8A8
m68k_01a8a8:
        move.w #0x3e7,%d2
m68k_01a8a8_end:
.org 0x1A8AC
m68k_01a8ac:
        move.w %d2,(%a0, %d0.w)
m68k_01a8ac_end:
.org 0x1A8B0
m68k_01a8b0:
        move.w %d7,%d1
m68k_01a8b0_end:
.org 0x1A8B2
m68k_01a8b2:
        lsr.w #0x1,%d1
m68k_01a8b2_end:
.org 0x1A8B4
m68k_01a8b4:
        move.w (%a1, %d0.w),%d2
m68k_01a8b4_end:
.org 0x1A8B8
m68k_01a8b8:
        add.w %d1,%d2
m68k_01a8b8_end:
.org 0x1A8BA
m68k_01a8ba:
        cmpi.w #0x3e7,%d2
m68k_01a8ba_end:
.org 0x1A8BE
m68k_01a8be:
        bls.w (. + 8)
m68k_01a8be_end:
.org 0x1A8C2
m68k_01a8c2:
        move.w #0x3e7,%d2
m68k_01a8c2_end:
.org 0x1A8C6
m68k_01a8c6:
        move.w %d2,(%a1, %d0.w)
m68k_01a8c6_end:
.org 0x1A8CA
m68k_01a8ca:
        cmpi.w #0x5,0xf6d4:w
m68k_01a8ca_end:
.org 0x1A8D0
m68k_01a8d0:
        beq.w (. + 20)
m68k_01a8d0_end:
.org 0x1A8D4
m68k_01a8d4:
        move.w #0x21,0xff7026:l
m68k_01a8d4_end:
.org 0x1A8DC
m68k_01a8dc:
        andi.w #0xfffe,%sr
m68k_01a8dc_end:
.org 0x1A8E0
m68k_01a8e0:
        bra.w (. + 186)
m68k_01a8e0_end:
.org 0x1A8E4
m68k_01a8e4:
        move.w #0x22,0xff7026:l
m68k_01a8e4_end:
.org 0x1A8EC
m68k_01a8ec:
        andi.w #0xfffe,%sr
m68k_01a8ec_end:
.org 0x1A8F0
m68k_01a8f0:
        bra.w (. + 170)
m68k_01a8f0_end:
.org 0x1A8F4
m68k_01a8f4:
        lea.l 0xb600:w,%a0
m68k_01a8f4_end:
.org 0x1A8F8
m68k_01a8f8:
        lea.l 0xc000:w,%a1
m68k_01a8f8_end:
.org 0x1A8FC
m68k_01a8fc:
        lea.l 0xbe00:w,%a2
m68k_01a8fc_end:
.org 0x1A900
m68k_01a900:
        move.w 0xf3a6:w,%d0
m68k_01a900_end:
.org 0x1A904
m68k_01a904:
        lsl.w #0x1,%d0
m68k_01a904_end:
.org 0x1A906
m68k_01a906:
        move.w (%a0, %d0.w),%d2
m68k_01a906_end:
.org 0x1A90A
m68k_01a90a:
        move.w 0xf3f2:w,%d1
m68k_01a90a_end:
.org 0x1A90E
m68k_01a90e:
        lsl.w #0x1,%d1
m68k_01a90e_end:
.org 0x1A910
m68k_01a910:
        sub.w (%a0, %d1.w),%d2
m68k_01a910_end:
.org 0x1A914
m68k_01a914:
        bcs.w (. + 34)
m68k_01a914_end:
.org 0x1A918
m68k_01a918:
        andi.l #0xffff,%d2
m68k_01a918_end:
.org 0x1A91E
m68k_01a91e:
        divu.w #0xa,%d2
m68k_01a91e_end:
.org 0x1A922
m68k_01a922:
        move.w (%a2, %d0.w),%d3
m68k_01a922_end:
.org 0x1A926
m68k_01a926:
        add.w %d2,%d3
m68k_01a926_end:
.org 0x1A928
m68k_01a928:
        cmpi.w #0x3e7,%d3
m68k_01a928_end:
.org 0x1A92C
m68k_01a92c:
        bls.b (. + 6)
m68k_01a92c_end:
.org 0x1A92E
m68k_01a92e:
        move.w #0x3e7,%d3
m68k_01a92e_end:
.org 0x1A932
m68k_01a932:
        move.w %d3,(%a2, %d0.w)
m68k_01a932_end:
.org 0x1A936
m68k_01a936:
        jsr 0x83d4:l
m68k_01a936_end:
.org 0x1A93C
m68k_01a93c:
        andi.l #0xffff,%d0
m68k_01a93c_end:
.org 0x1A942
m68k_01a942:
        lsl.l #0x4,%d0
m68k_01a942_end:
.org 0x1A944
m68k_01a944:
        swap %d0
m68k_01a944_end:
.org 0x1A946
m68k_01a946:
        addi.w #0x5,%d0
m68k_01a946_end:
.org 0x1A94A
m68k_01a94a:
        move.w 0xf3a6:w,%d2
m68k_01a94a_end:
.org 0x1A94E
m68k_01a94e:
        lsl.w #0x1,%d2
m68k_01a94e_end:
.org 0x1A950
m68k_01a950:
        move.w (%a1, %d2.w),%d3
m68k_01a950_end:
.org 0x1A954
m68k_01a954:
        add.w %d0,%d3
m68k_01a954_end:
.org 0x1A956
m68k_01a956:
        cmpi.w #0x3e7,%d3
m68k_01a956_end:
.org 0x1A95A
m68k_01a95a:
        bls.b (. + 6)
m68k_01a95a_end:
.org 0x1A95C
m68k_01a95c:
        move.w #0x3e7,%d3
m68k_01a95c_end:
.org 0x1A960
m68k_01a960:
        move.w %d3,(%a1, %d2.w)
m68k_01a960_end:
.org 0x1A964
m68k_01a964:
        jsr 0x83d4:l
m68k_01a964_end:
.org 0x1A96A
m68k_01a96a:
        andi.l #0xffff,%d0
m68k_01a96a_end:
.org 0x1A970
m68k_01a970:
        move.l %d0,%d1
m68k_01a970_end:
.org 0x1A972
m68k_01a972:
        lsl.l #0x1,%d0
m68k_01a972_end:
.org 0x1A974
m68k_01a974:
        add.l %d1,%d0
m68k_01a974_end:
.org 0x1A976
m68k_01a976:
        lsl.l #0x2,%d0
m68k_01a976_end:
.org 0x1A978
m68k_01a978:
        add.l %d1,%d0
m68k_01a978_end:
.org 0x1A97A
m68k_01a97a:
        swap %d0
m68k_01a97a_end:
.org 0x1A97C
m68k_01a97c:
        addi.w #0xa,%d0
m68k_01a97c_end:
.org 0x1A980
m68k_01a980:
        move.w (%a1, %d2.w),%d3
m68k_01a980_end:
.org 0x1A984
m68k_01a984:
        add.w %d0,%d3
m68k_01a984_end:
.org 0x1A986
m68k_01a986:
        cmpi.w #0x3e7,%d3
m68k_01a986_end:
.org 0x1A98A
m68k_01a98a:
        bls.w (. + 8)
m68k_01a98a_end:
.org 0x1A98E
m68k_01a98e:
        move.w #0x3e7,%d3
m68k_01a98e_end:
.org 0x1A992
m68k_01a992:
        move.w %d3,(%a1, %d2.w)
m68k_01a992_end:
.org 0x1A996
m68k_01a996:
        ori.w #0x1,%sr
m68k_01a996_end:
.org 0x1A99A
m68k_01a99a:
        rts
m68k_01a99a_end:
.org 0x1A99C
m68k_01a99c:
        move.w 0xf3a6:w,%d0
m68k_01a99c_end:
.org 0x1A9A0
m68k_01a9a0:
        lea.l 0xae28:w,%a0
m68k_01a9a0_end:
.org 0x1A9A4
m68k_01a9a4:
        clr.b (%a0, %d0.w)
m68k_01a9a4_end:
.org 0x1A9A8
m68k_01a9a8:
        rts
m68k_01a9a8_end:
