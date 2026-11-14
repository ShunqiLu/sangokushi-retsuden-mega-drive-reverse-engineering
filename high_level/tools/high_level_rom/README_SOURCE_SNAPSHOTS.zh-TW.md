# 原始碼與資源快照

[简体中文](README_SOURCE_SNAPSHOTS.md) · **繁體中文** · [日本語](README_SOURCE_SNAPSHOTS.ja.md) · [English](README_SOURCE_SNAPSHOTS.en.md)

[`stage_sources.py`](stage_sources.py) 提供兩種在記憶體中組織建置輸入的介面：

- `snapshot_resources(resource_root, resource_registration, ...)` 根據資源登記讀取後設資料和檔案內容，使用相對路徑索引每份位元組快照，並支援多根清單。
- `snapshot_source_tree(project_root, resource_snapshot=...)` 準備本版原始碼依賴，併合並呼叫方提供的資源快照。

資源登記使用固定 ID、編解碼器、源路徑、角色及建置鏈。對映的路徑相對目標根，包含素材成員以及需要的 Scene 清單。原始碼計數與素材計數分列。共享快照可供多個原始碼目標使用；目錄建立由 [`stage_sources` 命令](README_GAME_SOURCE_STAGE.zh-TW.md)辦理。
