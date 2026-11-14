# SRAM and save tools

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **English**

These tools inspect, unpack, edit, and write logical SRAM. G-5510 uses odd addresses `0x200001–0x203FFF` and an 8192-byte logical medium. The tools also recognize MAME's 16 KiB container, where each byte appears twice.

```powershell
python tools/save_data/save_format.py inspect input.srm
python tools/save_data/save_format.py extract input.srm save-fields
python tools/save_data/save_format.py import save-fields edited.srm
```

Unpacking validates the `SEGA` signature and original additive checksum and exports the layout, fields, and save baseline. Writing creates a new file, keeps the container form, unknown bytes, and field widths, and recalculates the checksum. `--allow-variable-resize` allows changes to the encoded unit bitstream length and fills the unused checksum-covered region after it with `FF`.

## Save views

- [Fixed city, officer, and faction records](README_NAMED_CAMPAIGN.en.md).
- [Marching units, coordinates, and cargo](README_CAMPAIGN_PACKETS.en.md).
- [CE00 transport orders](README_CAMPAIGN_ORDERS.en.md).

Provide a valid 8192-byte logical baseline. Edits create a new candidate file. The desktop application's `export_save` exports current SRAM; the save tools check the signature and checksum. Set the desired medium in [Local configuration](../reconstructed_game/README_LOCAL_CONFIG.en.md). Initial scenarios use the [scenario tools](../high_level_rom/README_NAMED_SCENARIO_SOURCES.en.md).
