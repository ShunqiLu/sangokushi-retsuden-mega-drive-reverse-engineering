# Scenario starting values

[简体中文](README_NAMED_SCENARIO_SOURCES.md) · [繁體中文](README_NAMED_SCENARIO_SOURCES.zh-TW.md) · [日本語](README_NAMED_SCENARIO_SOURCES.ja.md) · **English**

`resources/data/scenario_build.json` holds the cities, factions, officers, and starting equipment for three scenarios. The named view exposes gold, grain, troop counts, abilities, affiliations, and coordinates. Address keys retain their original ranges and widths. For current progress, see [Save editing](../save_data/README.en.md).

`$resources` is the local resource root containing `resources/` and `assets/`. Run from the assembly root.

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.scenario_sources edit --source "$resources/resources/data/scenario_build.json" --edits ./scenario-edits.json --project-root . --output build/scenario.json
```

`edit` accepts a named scenario document. Use `edit-equipment --edits` to handle the three original equipment bytes by field index. `export` converts legacy structured data to the named view; `import` converts it back. Review each new output file before placing it in the local pack.

`edit` takes an array with `scenario_id`, `group`, `record_id`, `field`, `expected_value`, and `value` for each edit. For city resources, writes update the low word and preserve the high word.
