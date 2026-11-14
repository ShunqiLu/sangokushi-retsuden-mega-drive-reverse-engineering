; Z80 音符和节拍参数读取续段。
; 0995 和 01E4 是驱动逻辑地址，对应原固定跳转目标。
.text
.org 0xA42
z80_0a42:
        inc de
z80_0a42_end:
.org 0xA43
z80_0a43:
        jp $0995
z80_0a43_end:
.org 0xB84
z80_0b84:
        inc de
z80_0b84_end:
.org 0xB85
z80_0b85:
        jp $01e4
z80_0b85_end:
