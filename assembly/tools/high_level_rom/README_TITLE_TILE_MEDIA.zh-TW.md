# 標題影象

[简体中文](README_TITLE_TILE_MEDIA.md) · **繁體中文** · [日本語](README_TITLE_TILE_MEDIA.ja.md) · [English](README_TITLE_TILE_MEDIA.en.md)

標題資料由 `resources/images/graphics_build.json` 登記；畫素成員儲存在 `assets/images/title/rle_tiles/`。每張 8×8 索引 PNG 定義一個圖塊，`commands.json` 儲存壓縮控制和圖塊引用。編輯後維持圖塊尺寸、索引調色盤、重複段和原槽長度。

素材根的影象與命令會由登記的編碼器重新組合。若手頭已有相容的結構化素材，可透過素材匯出工具生成外接 PNG 和 JSON。用 `python -B -m tools.high_level_rom.export_media --help` 檢視匯出引數。
