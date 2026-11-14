# 场景资源清单

**简体中文** · [繁體中文](README_SCENE_SOURCE_PUBLICATION.zh-TW.md) · [日本語](README_SCENE_SOURCE_PUBLICATION.ja.md) · [English](README_SCENE_SOURCE_PUBLICATION.en.md)

Scene 清单采用 `g5510-explicit-scene-source-roots-v1`。每个 `roots` 项含 `path` 和 `ids`；`path` 根据清单的位置解析，`ids` 给出该根拥有的登记资源。完整运行输入中的每个资源 ID 有一个对应来源。

[`scene_manifest.py`](scene_manifest.py) 将一组明确的资源 ID 从完整清单转给调用者选择的素材根。其余资源沿用原清单的登记。

```powershell
python -B -X utf8 -m tools.high_level_rom.scene_manifest --project-root . --source-manifest scene-sources.json --resource-root $editedResources --ids audio_build audio_root_resources --output build/scene-sources.edited.json
```

[`publish_readable_overlay.py`](publish_readable_overlay.py) 提供可读文字与可选剧本及 AI 字段的薄层输出；它以明确的完整基线清单建立合并登记。多根素材可由[独立运行目录工具](README_GAME_SOURCE_STAGE.md)汇总。
