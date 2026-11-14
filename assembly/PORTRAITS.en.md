# Officer portrait editing

[简体中文](PORTRAITS.md) · [繁體中文](PORTRAITS.zh-TW.md) · [日本語](PORTRAITS.ja.md) · **English**

The [portrait index tool](tools/high_level_rom/README_PORTRAIT_CATALOG.en.md) combines text, portrait, and scenario data. Find an officer by `name.text` or `officer_record_id`, then follow the layout, palette, and tile references to the editable files. Shared tiles affect several officers.

Files under the resource root:

- `resources/data/dialogue_text.json`: officer names.
- `resources/images/portrait_graphics.json`: portrait layouts, palettes, and external PNG references.
- `resources/data/scenario_build.json`: scenarios and officer records.
