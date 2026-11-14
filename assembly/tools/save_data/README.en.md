# Save tools

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **English**

`save_format` identifies the save container, validates the checksum, and reads or writes data sections. `campaign_cli` edits named fields in the current save. Keep the original save as input and use a new output path.

```powershell
python -B -m tools.save_data.save_format inspect ./campaign.srm
python -B -m tools.save_data.save_format extract ./campaign.srm ./save-source
python -B -m tools.save_data.save_format import ./save-source ./campaign-edited.srm
```

The named tools cover [cities, officers, and factions](README_NAMED_CAMPAIGN.en.md), [marching units](README_CAMPAIGN_PACKETS.en.md), and [transport orders](README_CAMPAIGN_ORDERS.en.md). Starting scenarios come from `resources/data/scenario_build.json` in the local resource pack.
