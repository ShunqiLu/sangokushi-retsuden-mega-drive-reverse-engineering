# Graphics, audio, and scenario resources

[简体中文](ASSETS.md) · [繁體中文](ASSETS.zh-TW.md) · [日本語](ASSETS.ja.md) · **English**

`--resource-root` points to a compatible local resource pack. Paths below are relative to that directory. The builder looks up each resource ID in its registry, then reads the referenced files.

| Path | Contents |
| --- | --- |
| `resources/images/` | Registry for tiles, maps, sprites, fonts, portraits, palettes, and layouts |
| `assets/images/` | Editable indexed PNGs, map files, layouts, and palettes |
| `resources/audio/` | Score, instrument patch, and external event definitions for the Z80 sound driver |
| `assets/audio/` | Notes, control events, envelopes, instrument patches, and shared sound files |
| `resources/data/` | Initial scenario values, AI parameters, text, and other game tables |

The manifest `asset-source-manifest.json` lists resource IDs, references, and editable fields. The [index tool](tools/reconstruction_delivery/README_MEDIA_CATALOG.en.md) generates `ASSET_INDEX.json`, a lookup table organized by filename.

## Graphics

PNG pixels store palette indices. Preview colors only help identify the tiles; the game uses the matching palette files. Keep tile dimensions, index bit widths, and shared references intact. The layout tools handle grid coordinates, flips, and priorities.

- [Battle map cells and attributes](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.en.md), [Battle background tiles](tools/high_level_rom/README_BATTLE_TILE_SHEET.en.md).
- [Officer portraits](PORTRAITS.en.md), [Title tiles](tools/high_level_rom/README_TITLE_TILE_MEDIA.en.md).
- [Shared graphics and audio aliases](tools/high_level_rom/README_MEDIA_ALIASES.en.md).

## Audio

Scores and sound effects consist of ordered events, instrument patches, envelopes, and shared files. Edit the registry and its source files. The sound chip model produces the PCM played by the application.

- [Sequences and command formats](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.en.md), [Shared event editor](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.en.md).
- [Desktop FM audio and chip clocks](tools/high_level_audio_engine/README_YMFM.en.md).

## Game data

See the editing and encoding rules for [named scenarios](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.en.md), [AI thresholds](tools/high_level_rom/README_AI_POLICY_SOURCES.en.md), [eligibility](tools/high_level_rom/README_AI_SELECTION_SOURCES.en.md), and [readable text](tools/high_level_rom/README_READABLE_TEXT.en.md). Each resource keeps its original field widths and layout.
