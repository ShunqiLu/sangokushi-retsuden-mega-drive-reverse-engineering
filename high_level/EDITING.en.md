# Editing guide

[简体中文](EDITING.md) · [繁體中文](EDITING.zh-TW.md) · [日本語](EDITING.ja.md) · **English**

This source tree contains the game rules. Graphics, audio, and scenario data are in the [resource root](ASSETS.en.md) passed to `--resource-root`.

| Content | Where to edit |
| --- | --- |
| City management, marches, battles, AI, and scene rules | Domain functions in `tools/high_level_*/business*.py` and the corresponding `compiler*.py` and `target.py` |
| City, officer, and faction starting values and scenario equipment | [Named scenario data](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.en.md) |
| AI command thresholds | [48 pairs of WORD thresholds](tools/high_level_rom/README_AI_POLICY_SOURCES.en.md) |
| AI candidate eligibility | [14 × 14 BYTE eligibility table](tools/high_level_rom/README_AI_SELECTION_SOURCES.en.md) |
| Chinese dialogue and officer and city names | [Readable text format](tools/high_level_rom/README_READABLE_TEXT.en.md) |
| Battle backgrounds | [Map cells and attributes](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.en.md), [Indexed tile PNGs](tools/high_level_rom/README_BATTLE_TILE_SHEET.en.md) |
| Officer portraits | [Names, layouts, palettes, and shared tiles](PORTRAITS.en.md) |
| Music, sound effects, and instrument patches | [Named scores and event sources](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.en.md), [Shared event editor](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.en.md) |
| Current save | [Fixed city, officer, and faction records](tools/save_data/README_NAMED_CAMPAIGN.en.md), [Marching units](tools/save_data/README_CAMPAIGN_PACKETS.en.md), [Transport orders](tools/save_data/README_CAMPAIGN_ORDERS.en.md) |

## Game rules and builds

Rule functions handle game rules and state changes. Files matching `contexts*.py` define inputs and interfaces. The compiler and target definitions handle instructions, addresses, registers, and fixed memory regions. Use the Python statements and state interfaces supported by the domain compiler. See [Original behavior](docs/ORIGINAL_GAME_BUGS.en.md) for edge cases.

The [image build](tools/high_level_rom/README_BUILD.en.md) reads edited resources through their registered inputs. Keep reusable changes in the rule source or the local resource pack so they can be rebuilt.

## Batch editing

The editing API takes the full input and a batch of records with explicit old and new values, then returns a separate candidate. The encoders preserve field widths, aliases, and file layout.

```python
from tools.high_level_rom.scenario_sources import with_scenario_fields

scenario = source["scenarios"][0]
city = next(row for row in scenario["cities"] if row["id"] == 3)
edited = with_scenario_fields(source, [{
    "scenario_id": scenario["id"],
    "group": "cities",
    "record_id": city["id"],
    "field": "gold",
    "expected_value": city["gold"],
    "value": 12000,
}])
```

Select scenario records by their physical record IDs and equipment by its source BYTE index. City development, civilian welfare, and defense use the lower WORD; the encoder preserves the upper WORD in the same slot. Text edits preserve fixed character slots and control WORDs. Audio edits identify the original event in the full event view and preserve its command type and size.

## Save data

The [save tools](tools/save_data/README.en.md) use an explicit 8 KiB logical save as the baseline. Fixed fields, marching units, and transport orders have separate views. Writing an edit produces a new file. Chain edits by using each resulting copy as the next baseline. Each view keeps the original field widths, checksum scheme, and unused data.
