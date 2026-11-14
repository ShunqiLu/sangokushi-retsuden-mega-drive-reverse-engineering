# Portrait index generator

[简体中文](README_PORTRAIT_CATALOG.md) · [繁體中文](README_PORTRAIT_CATALOG.zh-TW.md) · [日本語](README_PORTRAIT_CATALOG.ja.md) · **English**

[`portrait_catalog.py`](portrait_catalog.py) joins readable officer names and scenario records with portrait layouts, palettes, and shared tiles. In the output, `officers` supports lookups by name and record ID, and `shared_tiles` identifies shared image files. Known links and unidentified entries keep their original states.

```powershell
python -B -X utf8 -m tools.high_level_rom.portrait_catalog --project-root . --names-source "$resources/resources/data/dialogue_text.json" --portrait-source "$resources/resources/images/portrait_graphics.json" --record-authority "$resources/resources/data/scenario_build.json" --source-root $resources --output build/officer-portraits.json
```

`--names-source` uses the [readable text source](README_READABLE_TEXT.en.md) and can point directly to the named dialogue file in the resource root. `--source-root` resolves the actual portrait files. Write the new index under the project's `build/`. See the [portrait editing guide](../../PORTRAITS.en.md) to find the editable files.
