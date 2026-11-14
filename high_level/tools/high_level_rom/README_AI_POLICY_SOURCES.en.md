# AI command thresholds

[简体中文](README_AI_POLICY_SOURCES.md) · [繁體中文](README_AI_POLICY_SOURCES.zh-TW.md) · [日本語](README_AI_POLICY_SOURCES.ja.md) · **English**

`ai_threshold_pair_fields` has three main-table groups of 15 pairs and three secondary-table pairs, for 48 pairs of unsigned WORDs. Each pair uses `first_cutoff_word` and `second_cutoff_word`. City defense planning also reads the main table's first WORD, so editing it affects both calls.

The rules read both tables in their original order and select branches with unsigned comparisons. Group and pair numbers are physical positions. Equal values, reverse order, and the full 0–65535 range are valid.

## Commands

The export below uses resource root `$typedResources` with typed sources. You can pass an existing named source directly to `edit --source`. Write to a new file under the existing `build/` directory.

```powershell
python -B -m tools.high_level_rom.ai_policy_sources export --source "$typedResources/resources/data/ai_threshold_pair_fields.json" --project-root . --output build/ai-cutoffs.named.json
python -B -m tools.high_level_rom.ai_policy_sources edit --source build/ai-cutoffs.named.json --edits cutoff-edits.json --project-root . --output build/ai-cutoffs.edited.json
python -B -m tools.high_level_rom.ai_policy_sources import --source build/ai-cutoffs.edited.json --project-root . --output build/ai-cutoffs.typed.json
```

The named format is `g5510-named-ai-command-cutoffs-v1`. Edits use `g5510-ai-command-cutoff-pair-edits-v1` with `format` and `edits`. Each entry has `table`, `pair_index`, `field`, `expected_word`, and `word`. The main table also has `group_index` (0–2). Pair numbers are 0–14 in the main table and 0–2 in the secondary table. Check edits against the current complete source and write to new JSON.

Python interfaces `to_named` and `from_named` convert representations. `with_cutoff_pairs(source, edits)` returns a separate edited document. See the [resource manifest](README_SCENE_SOURCE_PUBLICATION.en.md) for named, original, and overlay registrations.
