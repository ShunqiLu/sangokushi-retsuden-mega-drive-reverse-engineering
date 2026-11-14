# Named scenario starting values

[简体中文](README_NAMED_SCENARIO_SOURCES.md) · [繁體中文](README_NAMED_SCENARIO_SOURCES.zh-TW.md) · [日本語](README_NAMED_SCENARIO_SOURCES.ja.md) · **English**

[`scenario_sources.py`](scenario_sources.py) maps typed scenario columns for cities, officers, and factions to `g5510-owned-named-scenario-source-v1`. The document preserves `metadata`, `directory_targets`, and the three physical `scenarios`. Physical records use `scenario_0`, `scenario_1`, and `scenario_2`. Runtime descriptors and directory aliases keep their respective references.

| Group | Fields and stored values |
| --- | --- |
| City resources | `gold` and `rice` are 32-bit values; `development`, `welfare`, and `defense` edit their low WORDs and preserve their high WORDs. |
| City management | `force_index_byte`, `representative_officer_word`, `income_base_long`, `income_split_long`, `income_rate_long`, `assigned_officer_tally_long`, `troop_total_long`. |
| Factions | `representative_officer_word` and `relationship_bits_word`; relation rows retain their direction. |
| Officer basics | `intelligence_word`, `virtue_byte`, `troop_capacity_base_word`, `troop_count_long`, `assigned_city_byte`. |
| Officer growth and state | `readiness_capacity_word`, `readiness_current_word`, `combat_rating_word`, `intelligence_growth_score_word`, `combat_growth_score_word`, `education_rating_byte`, `movement_factor_byte`, `training_percent_byte`, `growth_threshold_tier_byte`, `class_status_flags_byte`. |

BE00 and C000 map to two growth WORDs. Game rules handle the original wraparound, divisors, and limits. B000 and B200 are the capacity and current value of one recoverable state. C400 is used in candidate radius and travel calculations. Remaining or unnamed values are stored by original address in `unresolved_fields`, preserving their source widths, sentinels, and unknown bits.

## Batch editing

`with_scenario_fields(source, edits)` uses `scenario_id`, `group`, `record_id`, `field`, `expected_value`, and `value`. City IDs are 1–40, faction IDs 0–15, and officer IDs 0–255. Each field is checked at its original BYTE, WORD, or LONG width. Only the old and new low WORDs belong in the three split-slot city fields. The function returns a separate named document.

Pass an existing named document directly to `edit`. The example `export` exports one from `$typedResources` with typed sources. Write to a new file under the existing `build/`.

```powershell
python -B -X utf8 -m tools.high_level_rom.scenario_sources export --project-root . --source "$typedResources/resources/data/scenario_build.json" --output build/scenario.named.json
python -B -X utf8 -m tools.high_level_rom.scenario_sources edit --project-root . --source build/scenario.named.json --edits scenario-edits.json --output build/scenario.edited.json
```

`to_named` and `from_named` convert the plain data representations. `import` converts the named document to the original typed format. The registered resource ID is `scenario_build`.

## Starting equipment BYTEs

`unresolved_fields.ram_ea88` contains `source_byte0`, `source_byte1`, and `source_byte2`, read at runtime in the order 1, 0, 2. Use `scenario_id`, `officer_id`, `source_byte_index`, `expected_value`, and `value` with `with_equipment_source_bytes` or `edit-equipment --edits`. BYTEs range from 0 to 255; other slots and scenario aliases retain their original relationships.
