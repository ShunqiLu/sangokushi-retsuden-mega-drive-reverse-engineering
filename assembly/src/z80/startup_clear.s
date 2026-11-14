; Z80 启动清理。68000 启动例程将此段复制到 Z80 RAM 的 0000。
.text
_boot_start:
.org 0x0
; 复位入口从 Z80 RAM 的 0000 开始。
boot_z80_0000:
        xor a
boot_z80_0000_end:
boot_z80_0001:
        ld bc,$1fd9
boot_z80_0001_end:
boot_z80_0004:
        ld de,$0027
boot_z80_0004_end:
boot_z80_0007:
        ld hl,$0026
boot_z80_0007_end:
boot_z80_000a:
        ld sp,hl
boot_z80_000a_end:
; 地址 0026 的零值作为重叠 LDIR 的初始源字节。
boot_z80_000b:
        ld (hl),a
boot_z80_000b_end:
; BC 取 1FD9，LDIR 将零值传播至地址 1FFF。
boot_z80_000c:
        ldir
boot_z80_000c_end:
boot_z80_000e:
        pop ix
boot_z80_000e_end:
boot_z80_0010:
        pop iy
boot_z80_0010_end:
boot_z80_0012:
        ld i,a
boot_z80_0012_end:
boot_z80_0014:
        ld r,a
boot_z80_0014_end:
boot_z80_0016:
        pop de
boot_z80_0016_end:
boot_z80_0017:
        pop hl
boot_z80_0017_end:
boot_z80_0018:
        pop af
boot_z80_0018_end:
boot_z80_0019:
        ex af,af'
boot_z80_0019_end:
boot_z80_001a:
        exx
boot_z80_001a_end:
boot_z80_001b:
        pop bc
boot_z80_001b_end:
boot_z80_001c:
        pop de
boot_z80_001c_end:
boot_z80_001d:
        pop hl
boot_z80_001d_end:
boot_z80_001e:
        pop af
boot_z80_001e_end:
boot_z80_001f:
        ld sp,hl
boot_z80_001f_end:
boot_z80_0020:
        di
boot_z80_0020_end:
boot_z80_0021:
        im 1
boot_z80_0021_end:
boot_z80_0023:
        ld (hl),$e9
boot_z80_0023_end:
boot_z80_0025:
        jp (hl)
boot_z80_0025_end:
