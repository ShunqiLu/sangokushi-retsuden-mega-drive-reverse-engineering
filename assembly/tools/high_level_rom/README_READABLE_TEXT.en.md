# Dialogue and name editing

[简体中文](README_READABLE_TEXT.md) · [繁體中文](README_READABLE_TEXT.zh-TW.md) · [日本語](README_READABLE_TEXT.ja.md) · **English**

`resources/data/dialogue_text.json` contains dialogue and officer and city names. The named format preserves terminator words, original character counts, and exact escapes when ordinary text is ambiguous. Edits keep the same record IDs and length limits.

`$resources` is the local resource root containing `resources/` and `assets/`. Run from the assembly root.

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.readable_text edit --source "$resources/resources/data/dialogue_text.json" --edits ./text-edits.json --project-root . --output build/readable-text.json
```

`edit --edits` checks each edit against the record ID and expected value. `import` converts the named format back to character codes. With the legacy coded format and two manually transcribed glyph tables, `export --glyph-sources` produces the named view.

Set `format` to `g5510-main-text-record-edits-v1`. In `edits`, each entry takes `collection`, `id`, `expected_text`, and `text`. Collection names are `records`, `officer_names`, or `city_names`.
