# Title screen tiles

[简体中文](README_TITLE_TILE_MEDIA.md) · [繁體中文](README_TITLE_TILE_MEDIA.zh-TW.md) · [日本語](README_TITLE_TILE_MEDIA.ja.md) · **English**

Each of the five 4bpp compressed title streams contains 256 tiles of 8 × 8 pixels and decodes to 4096 WORDs.

| Resource | Linear compressed range (end excluded) | VDP start address |
| --- | --- | --- |
| `title_tiles_rle_0` | `05D5E4..05F137` | `0000` |
| `title_tiles_rle_1` | `05F137..060E6C` | `2000` |
| `title_tiles_rle_2` | `060E6C..06254F` | `4000` |
| `title_tiles_rle_3` | `06254F..064340` | `8000` |
| `title_tiles_rle_4` | `064340..0655F1` | `A000` |

`tools.high_level_rom.export_media` exports editable files from a compatible typed resource root. The streams use `assets/images/title/rle_tiles/<资源 ID>/commands.json` and `tiles/tile_0000.png` through `tiles/tile_0255.png`. Each PNG is opaque, single-frame, and indexed from 0 to 15; colors come from the matching game palette JSON.

[`media_word_rle.py`](media_word_rle.py) packs the pixels back into four-pixel WORDs in the original order. Compressed WORDs use little-endian storage, but pixel nibbles still run from high to low. Repeat runs must use identical complete WORDs. The original encoder checks terminators, markers, decoded width, and fixed slot length.
