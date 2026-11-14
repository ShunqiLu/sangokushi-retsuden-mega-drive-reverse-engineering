# Local run directory

[简体中文](README_GAME_SOURCE_STAGE.md) · [繁體中文](README_GAME_SOURCE_STAGE.zh-TW.md) · [日本語](README_GAME_SOURCE_STAGE.ja.md) · **English**

[`stage_sources.py`](stage_sources.py) reads the specified source tree and registered resources. It creates a separate run directory with sources, configuration templates, resources, and a Scene manifest. Supply a complete local resource root, or a complete multi-root Scene manifest with a resource metadata manifest.

```powershell
python -B -X utf8 -m tools.high_level_rom.stage_sources stage --project-root . --resource-root $resources --output ../local-game
```

The multi-root form uses `--source-manifest` and `--asset-metadata-manifest`. Each resource ID in the complete manifest has one source. `plan` prints the source dependency plan. `stage` writes to a fresh directory outside the project and resource roots. Paths and values come from the explicit resource registry and this edition's static and dynamic source declarations.

[Resource roots and aliases](README_SCENE_SOURCE_PUBLICATION.en.md) explains the limits of the multi-root manifest. [Desktop configuration](../reconstructed_game/README_LOCAL_CONFIG.en.md) covers image builds, the sound chip library, device inputs, and saves.
