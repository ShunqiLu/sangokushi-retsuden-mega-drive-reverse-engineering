# Title graphics

[简体中文](README_TITLE_TILE_MEDIA.md) · [繁體中文](README_TITLE_TILE_MEDIA.zh-TW.md) · [日本語](README_TITLE_TILE_MEDIA.ja.md) · **English**

`resources/images/graphics_build.json` registers the title resources. `assets/images/title/rle_tiles/` holds the pixel data. Each indexed 8 × 8 PNG defines one tile; `commands.json` stores compression controls and tile references. Keep tile size, indexed palette, repeat runs, and slot lengths unchanged.

The registered encoder combines the images and commands from the resource root. If you have compatible structured resources, export them to separate PNG and JSON files. Use `python -B -m tools.high_level_rom.export_media --help` for export options.
