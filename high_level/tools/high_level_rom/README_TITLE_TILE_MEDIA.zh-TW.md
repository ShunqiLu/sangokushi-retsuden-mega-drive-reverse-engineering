# 標題圖塊

[简体中文](README_TITLE_TILE_MEDIA.md) · **繁體中文** · [日本語](README_TITLE_TILE_MEDIA.ja.md) · [English](README_TITLE_TILE_MEDIA.en.md)

標題畫面的五條 4bpp 壓縮流分別提供 256 個 8×8 圖塊和 4096 個解碼 WORD。

| 資源 | 線性壓縮範圍（半開區間） | VDP 起址 |
| --- | --- | --- |
| `title_tiles_rle_0` | `05D5E4..05F137` | `0000` |
| `title_tiles_rle_1` | `05F137..060E6C` | `2000` |
| `title_tiles_rle_2` | `060E6C..06254F` | `4000` |
| `title_tiles_rle_3` | `06254F..064340` | `8000` |
| `title_tiles_rle_4` | `064340..0655F1` | `A000` |

`tools.high_level_rom.export_media` 從相容 typed 資源根生成可編輯素材。各流使用 `assets/images/title/rle_tiles/<资源 ID>/commands.json` 和 `tiles/tile_0000.png` 至 `tiles/tile_0255.png`。每張 PNG 使用索引 0–15 的單幀不透明畫素；配色來自對應的遊戲調色盤 JSON。

[`media_word_rle.py`](media_word_rle.py) 按原順序把畫素還原為四畫素 WORD。WORD 的壓縮儲存使用小端，畫素仍按高位到低位的半位元組排列。重複段覆蓋的完整 WORD 必須一致。終結符、標記、解碼總寬與固定槽長度由原編碼器核對。
