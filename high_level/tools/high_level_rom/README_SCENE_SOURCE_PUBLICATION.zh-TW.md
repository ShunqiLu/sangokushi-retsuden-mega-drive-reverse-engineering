# 場景資源清單

[简体中文](README_SCENE_SOURCE_PUBLICATION.md) · **繁體中文** · [日本語](README_SCENE_SOURCE_PUBLICATION.ja.md) · [English](README_SCENE_SOURCE_PUBLICATION.en.md)

Scene 清單採用 `g5510-explicit-scene-source-roots-v1`。每個 `roots` 項含 `path` 和 `ids`；`path` 根據清單的位置解析，`ids` 給出該根擁有的登記資源。完整執行輸入中的每個資源 ID 有一個對應來源。

[`scene_manifest.py`](scene_manifest.py) 將一組明確的資源 ID 從完整清單轉給呼叫者選擇的素材根。其餘資源沿用原清單的登記。

```powershell
python -B -X utf8 -m tools.high_level_rom.scene_manifest --project-root . --source-manifest scene-sources.json --resource-root $editedResources --ids audio_build audio_root_resources --output build/scene-sources.edited.json
```

[`publish_readable_overlay.py`](publish_readable_overlay.py) 提供可讀文字與可選劇本及 AI 欄位的薄層輸出；它以明確的完整基線清單建立合併登記。多根素材可由[獨立執行目錄工具](README_GAME_SOURCE_STAGE.zh-TW.md)彙總。
