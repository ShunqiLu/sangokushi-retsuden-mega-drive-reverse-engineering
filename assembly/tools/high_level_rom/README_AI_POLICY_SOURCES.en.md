# AI command thresholds

[简体中文](README_AI_POLICY_SOURCES.md) · [繁體中文](README_AI_POLICY_SOURCES.zh-TW.md) · [日本語](README_AI_POLICY_SOURCES.ja.md) · **English**

`resources/data/ai_threshold_pair_fields.json` holds 48 pairs of 16-bit thresholds. The named view groups the pairs by command. The first threshold shared with the defense check still comes from the same field.

`$resources` is the local resource root containing both `resources/` and `assets/`. Run the commands from the assembly root.

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.ai_policy_sources edit --source "$resources/resources/data/ai_threshold_pair_fields.json" --edits ./ai-policy-edits.json --project-root . --output build/ai-policy.json
```

`edit` applies paired edits with expected values. `export` converts legacy structured data to the named view; `import` converts it back. Choose a new JSON path under `build/`.

Set `format` to `g5510-ai-command-cutoff-pair-edits-v1`. Each entry in `edits` takes `table`, `pair_index`, `field`, `expected_word`, and `word`; the `primary` table also takes `group_index`. The field can be `first_cutoff_word` or `second_cutoff_word`.
