"""Mega Drive headers and the G-5510 layout shared by fixed-address tools."""

MEGA_DRIVE_ID = b"SEGA MEGA DRIVE "
G5510_PRODUCT_ID = b"GM G-5510  -00"
G5510_SIZE = 0x100000


def require_g5510_rom(rom: bytes) -> None:
    """Check the size, system and product fields of the linear cartridge."""
    if (
        type(rom) is not bytes
        or len(rom) != G5510_SIZE
        or rom[0x100:0x110] != MEGA_DRIVE_ID
        or rom[0x180:0x18E] != G5510_PRODUCT_ID
        or int.from_bytes(rom[0x1A0:0x1A4], "big") != 0
        or int.from_bytes(rom[0x1A4:0x1A8], "big") != G5510_SIZE - 1
    ):
        raise ValueError("expected the 1 MiB G-5510 linear cartridge layout")
