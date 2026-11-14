# シーン素材マニフェスト

[简体中文](README_SCENE_SOURCE_PUBLICATION.md) · [繁體中文](README_SCENE_SOURCE_PUBLICATION.zh-TW.md) · **日本語** · [English](README_SCENE_SOURCE_PUBLICATION.en.md)

Scene マニフェストは `g5510-explicit-scene-source-roots-v1` 形式です。`roots` の各要素は `path` と `ids` を持ちます。`path` はマニフェストの位置から解決され、`ids` はそのルートが所有する登録済み素材を列挙します。完全な実行入力で各素材 ID の供給元は 1 つです。

[`scene_manifest.py`](scene_manifest.py) は完全なマニフェストから指定素材 ID を選び、指定の素材ルートに割り当てます。他の素材は元の登録を維持します。

```powershell
python -B -X utf8 -m tools.high_level_rom.scene_manifest --project-root . --source-manifest scene-sources.json --resource-root $editedResources --ids audio_build audio_root_resources --output build/scene-sources.edited.json
```

[`publish_readable_overlay.py`](publish_readable_overlay.py) は可読テキストと、任意のシナリオ・AI フィールドの差し替えを出力し、明示した完全な基準マニフェストに登録を重ねます。[独立実行ディレクトリのツール](README_GAME_SOURCE_STAGE.ja.md)で複数ルートの素材をまとめられます。
