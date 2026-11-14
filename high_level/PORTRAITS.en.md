# Officer portraits

[简体中文](PORTRAITS.md) · [繁體中文](PORTRAITS.zh-TW.md) · [日本語](PORTRAITS.ja.md) · **English**

Use `OFFICER_PORTRAITS.json` in the resource pack to look up portraits. Search `officers` by `name.text` or `officer_record_id`. Unknown glyphs retain their exact escapes.

| Field | Contents |
| --- | --- |
| `portrait.layout_file` | Layout JSON for pixel tiles and portrait cells |
| `portrait.palette.file` | Palette JSON |
| `tile_groups[].tile_ref` | Reference to a shared PNG in `shared_tiles` |

Names come from `resources/data/dialogue_text.json`, portraits from `resources/images/portrait_graphics.json`, and officer records from `resources/data/scenario_build.json`. Editing a shared PNG changes every portrait that references it. Unidentified entries are marked `unknown`.

See the [portrait index tool](tools/high_level_rom/README_PORTRAIT_CATALOG.en.md) for lookup and generation commands.
