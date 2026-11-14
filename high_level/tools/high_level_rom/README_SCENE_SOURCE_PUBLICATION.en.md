# Scene resource manifest

[简体中文](README_SCENE_SOURCE_PUBLICATION.md) · [繁體中文](README_SCENE_SOURCE_PUBLICATION.zh-TW.md) · [日本語](README_SCENE_SOURCE_PUBLICATION.ja.md) · **English**

Scene manifests use `g5510-explicit-scene-source-roots-v1`. Each `roots` entry contains `path` and `ids`. `path` resolves relative to the manifest; `ids` lists the registered resources owned by that root. Each resource ID in a complete runtime input has exactly one source.

[`scene_manifest.py`](scene_manifest.py) transfers specified resource IDs from a complete manifest to a selected resource root. Other resources keep their original registrations.

```powershell
python -B -X utf8 -m tools.high_level_rom.scene_manifest --project-root . --source-manifest scene-sources.json --resource-root $editedResources --ids audio_build audio_root_resources --output build/scene-sources.edited.json
```

[`publish_readable_overlay.py`](publish_readable_overlay.py) writes a small overlay with readable text and optional scenario and AI fields, merging the registrations against an explicit complete baseline manifest. The [standalone run directory tool](README_GAME_SOURCE_STAGE.en.md) combines resources from multiple roots.
