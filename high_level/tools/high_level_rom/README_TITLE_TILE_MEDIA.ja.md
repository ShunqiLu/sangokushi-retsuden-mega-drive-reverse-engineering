# タイトル画面のタイル

[简体中文](README_TITLE_TILE_MEDIA.md) · [繁體中文](README_TITLE_TILE_MEDIA.zh-TW.md) · **日本語** · [English](README_TITLE_TILE_MEDIA.en.md)

タイトル画面の 5 本の 4 bpp 圧縮ストリームは、それぞれ 8 × 8 のタイルを 256 枚、展開後の WORD を 4096 個持ちます。

| 素材 | 線形圧縮範囲（終点を含まない） | VDP 開始アドレス |
| --- | --- | --- |
| `title_tiles_rle_0` | `05D5E4..05F137` | `0000` |
| `title_tiles_rle_1` | `05F137..060E6C` | `2000` |
| `title_tiles_rle_2` | `060E6C..06254F` | `4000` |
| `title_tiles_rle_3` | `06254F..064340` | `8000` |
| `title_tiles_rle_4` | `064340..0655F1` | `A000` |

`tools.high_level_rom.export_media` は互換性のある型付き素材ルートから編集用素材を生成します。各ストリームは `assets/images/title/rle_tiles/<资源 ID>/commands.json` と `tiles/tile_0000.png` から `tiles/tile_0255.png` を使います。各 PNG は透過なしの単一フレームで、インデックスは 0～15 です。配色は対応するゲームパレットの JSON から取得します。

[`media_word_rle.py`](media_word_rle.py) はピクセルを元の順序で 4 ピクセルの WORD に戻します。圧縮時の WORD はリトルエンディアンですが、ピクセルの 4 ビット値は上位から下位の順です。繰り返し区間では WORD 全体が一致する必要があります。元のエンコーダーで終端、マーカー、展開幅、固定スロット長を照合します。
