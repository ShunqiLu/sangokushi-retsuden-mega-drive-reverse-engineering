# 标题图块

**简体中文** · [繁體中文](README_TITLE_TILE_MEDIA.zh-TW.md) · [日本語](README_TITLE_TILE_MEDIA.ja.md) · [English](README_TITLE_TILE_MEDIA.en.md)

标题画面的五条 4bpp 压缩流分别提供 256 个 8×8 图块和 4096 个解码 WORD。

| 资源 | 线性压缩范围（半开区间） | VDP 起址 |
| --- | --- | --- |
| `title_tiles_rle_0` | `05D5E4..05F137` | `0000` |
| `title_tiles_rle_1` | `05F137..060E6C` | `2000` |
| `title_tiles_rle_2` | `060E6C..06254F` | `4000` |
| `title_tiles_rle_3` | `06254F..064340` | `8000` |
| `title_tiles_rle_4` | `064340..0655F1` | `A000` |

`tools.high_level_rom.export_media` 从兼容 typed 资源根生成可编辑素材。各流使用 `assets/images/title/rle_tiles/<资源 ID>/commands.json` 和 `tiles/tile_0000.png` 至 `tiles/tile_0255.png`。每张 PNG 使用索引 0–15 的单帧不透明像素；配色来自对应的游戏调色板 JSON。

[`media_word_rle.py`](media_word_rle.py) 按原顺序把像素还原为四像素 WORD。WORD 的压缩存储使用小端，像素仍按高位到低位的半字节排列。重复段覆盖的完整 WORD 必须一致。终结符、标记、解码总宽与固定槽长度由原编码器核对。
