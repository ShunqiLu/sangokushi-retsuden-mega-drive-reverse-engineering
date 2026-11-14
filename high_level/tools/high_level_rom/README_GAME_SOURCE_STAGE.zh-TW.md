# 準備本地執行目錄

[简体中文](README_GAME_SOURCE_STAGE.md) · **繁體中文** · [日本語](README_GAME_SOURCE_STAGE.ja.md) · [English](README_GAME_SOURCE_STAGE.en.md)

[`stage_sources.py`](stage_sources.py) 讀取顯式原始碼目錄及登記資源，生成獨立執行目錄中的原始碼、配置模板、素材和 Scene 清單。輸入為完整本地素材根，或完整的多根 Scene 清單及素材後設資料清單。

```powershell
python -B -X utf8 -m tools.high_level_rom.stage_sources stage --project-root . --resource-root $resources --output ../local-game
```

多根形式使用 `--source-manifest` 與 `--asset-metadata-manifest`，完整清單中的每個資源 ID 使用唯一來源。`plan` 輸出原始碼依賴計劃；`stage` 寫入工程和素材根之外的新目錄。路徑和值由顯式資源登記及本版靜態、動態原始碼宣告解析。

[素材根與別名](README_SCENE_SOURCE_PUBLICATION.zh-TW.md)說明多根清單的邊界。[桌面配置](../reconstructed_game/README_LOCAL_CONFIG.zh-TW.md)說明映象建置、晶片庫、裝置輸入和存檔。
