# 相容素材包

[简体中文](ASSETS.md) · **繁體中文** · [日本語](ASSETS.ja.md) · [English](ASSETS.en.md)

素材包以 `resources/` 和 `assets/` 為兩條入口。前者登記資源格式和成員關係；後者儲存實際圖塊、佈局、音色、聲道事件和其他資料。把這兩個目錄的共同父目錄傳給建置引數 `--resource-root`。

```text
本地素材根/
  resources/
    audio/
    data/
    images/
  assets/
    audio/
    images/
```

| 編輯主題 | 素材包中的入口 |
| --- | --- |
| 標題影象 | `resources/images/graphics_build.json`、`assets/images/title/` |
| 戰鬥地圖佈局與底圖 | `resources/images/battle_graphics.json` |
| 武將頭像和調色盤 | `resources/images/portrait_graphics.json`、`assets/images/portraits/` |
| 字形 | `resources/images/font_build.json`、`assets/images/fonts/` |
| 曲目、音效和狀態事件 | `resources/audio/audio_build.json`、`assets/audio/` |
| 劇本和對話 | `resources/data/scenario_build.json`、`resources/data/dialogue_text.json` |

已提供素材清單時，可用[索引工具](tools/reconstruction_delivery/README_MEDIA_CATALOG.zh-TW.md)查詢欄位和檔案。索引 PNG 的顏色編號是編碼輸入，遊戲配色來自配套調色檔案。
