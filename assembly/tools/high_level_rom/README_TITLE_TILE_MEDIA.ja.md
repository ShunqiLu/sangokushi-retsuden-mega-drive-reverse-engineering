# タイトル画面のグラフィック

[简体中文](README_TITLE_TILE_MEDIA.md) · [繁體中文](README_TITLE_TILE_MEDIA.zh-TW.md) · **日本語** · [English](README_TITLE_TILE_MEDIA.en.md)

`resources/images/graphics_build.json` にタイトル画面の素材を登録し、`assets/images/title/rle_tiles/` にピクセルデータを保存します。8 × 8 のインデックス付き PNG が 1 タイルを定義し、`commands.json` に圧縮制御とタイル参照が入ります。タイル寸法、インデックスパレット、繰り返し区間、元のスロット長を保ちます。

登録済みのエンコーダーが素材ルートの画像と命令を組み合わせます。互換性のある構造化素材から、外部 PNG と JSON を書き出せます。引数は `python -B -m tools.high_level_rom.export_media --help` で確認できます。
