# Resources and saves

[简体中文](resources.md) · [繁體中文](resources.zh-TW.md) · [日本語](resources.ja.md) · **English**

Fixed-address tools expect a linear G-5510 BIN. When importing resources, use the same baseline image as for export and choose a fresh output path. Each tool takes an explicit output file or directory.

| Tool | Data |
| --- | --- |
| [scan_assets.py](../tools/asset_analysis/scan_assets.py) | Resource candidates, text references, repeated blocks, and tile previews |
| [render_raw4bpp.py](../tools/asset_analysis/render_raw4bpp.py) | 8×8 tile and 16×16 glyph previews |
| [graphics_build.py](../tools/graphics_build/graphics_build.py) | Tiles, maps, palettes, and transfer fields for the title and duel screens |
| [graphics_assets.py](../tools/graphics_vdp/graphics_assets.py) | Title graphics, VDP buffers, and static previews |
| [duel_graphics.py](../tools/duel_graphics/duel_graphics.py) | Fixed duel resources, two-channel RLE maps, and static previews |
| [audio_formats.py](../tools/audio_formats/audio_formats.py) | Songs, sound effect headers, and FM instrument register fields |
| [scenario_static_data.py](../tools/static_data/scenario_static_data.py) | Scenario initialization tables, source records, and runtime representations |

```sh
python tools/asset_analysis/scan_assets.py --rom out/cartridge.bin --output out/resource-map
python tools/asset_analysis/render_raw4bpp.py 0x50000 --rom out/cartridge.bin --output out/tiles.png
python tools/graphics_build/graphics_build.py export --rom out/cartridge.bin --output out/graphics
python tools/graphics_build/graphics_build.py import --rom out/cartridge.bin --assets out/graphics/assets.json --output out/graphics-image
python tools/audio_formats/audio_formats.py export --rom out/cartridge.bin --output out/audio
python tools/static_data/scenario_static_data.py extract --rom out/cartridge.bin --output out/scenarios
```

Keep fixed slot sizes when editing graphics. For duel maps, edit the compressed stream or the decoded tile map; the importer encodes it to fit the slot. Audio packs preserve pointer tables and instrument sharing. Scenario packs preserve table order and record widths.

## SRAM

[`save_format.py`](../tools/save_data/save_format.py) supports 8 KiB logical SRAM and the 16 KiB interleaved MAME container. Export preserves fixed fields, bit-packed records, and the original reserved regions. Import recalculates the save checksum and preserves the selected container layout.

```sh
python tools/save_data/save_format.py inspect input/campaign.srm
python tools/save_data/save_format.py extract input/campaign.srm out/save-fields
python tools/save_data/save_format.py import out/save-fields out/rebuilt.srm
python tools/save_data/generate_reports.py out/save-layout
```

[`generate_reports.py`](../tools/save_data/generate_reports.py) prints offsets, bit widths, and record counts. Pass a save file via `--capture` to include its format and field statistics.
