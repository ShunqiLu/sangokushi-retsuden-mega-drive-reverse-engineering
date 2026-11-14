# Editing guide

[简体中文](EDITING.md) · [繁體中文](EDITING.zh-TW.md) · [日本語](EDITING.ja.md) · **English**

Program and tool paths are relative to this directory. Resource paths are relative to the directory passed to `--resource-root`. Edit a local copy, then rebuild from source.

| Content | Where to edit |
| --- | --- |
| 68000 and Z80 programs | `src/m68k/`, `src/z80/`; see `tools/reconstructed_assembly/layout/` for instruction ranges |
| Initial city, officer, and faction data | `resources/data/scenario_build.json` in the resource pack; see [Scenario editing](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.en.md) |
| Dialogue and officer and city names | `resources/data/dialogue_text.json`; see [Text editing](tools/high_level_rom/README_READABLE_TEXT.en.md) |
| AI parameters | `resources/data/ai_threshold_pair_fields.json`, `resources/data/ai_selection_fields.json`; see [Thresholds](tools/high_level_rom/README_AI_POLICY_SOURCES.en.md) and [Eligibility](tools/high_level_rom/README_AI_SELECTION_SOURCES.en.md) |
| Graphics and colors | `assets/images/` and the layout and palette JSON files; see [Resources](ASSETS.en.md), [Battle maps](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.en.md), [Tile sheets](tools/high_level_rom/README_BATTLE_TILE_SHEET.en.md), and [Portraits](PORTRAITS.en.md) |
| Music, sound effects, and instrument patches | `resources/audio/` and the referenced files in `assets/audio/`; see [Audio sequences](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.en.md) and [Shared events](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.en.md) |
| Current save | [Save tools](tools/save_data/README.en.md): [Cities and factions](tools/save_data/README_NAMED_CAMPAIGN.en.md), [Marching units](tools/save_data/README_CAMPAIGN_PACKETS.en.md), [Transport orders](tools/save_data/README_CAMPAIGN_ORDERS.en.md) |

Indexed PNGs store tile data as pixel indices. Keep the image mode, dimensions, and paths unchanged. Edit the palette JSON to change the displayed colors. Pass the updated resource pack to the builder as shown in the [build instructions](README.en.md).
