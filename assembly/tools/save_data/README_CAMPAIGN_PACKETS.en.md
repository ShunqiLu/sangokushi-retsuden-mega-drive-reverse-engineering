# Marching units in saves

[简体中文](README_CAMPAIGN_PACKETS.md) · [繁體中文](README_CAMPAIGN_PACKETS.zh-TW.md) · [日本語](README_CAMPAIGN_PACKETS.ja.md) · **English**

The march view preserves unit order, officer IDs, map coordinates, faction, and carried resources. Original record and member counts and saved field widths constrain edits.

Run from the assembly root. Provide a local 8 KiB logical save and prepare `build/` for the results.

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli packets-export --project-root . --source ./campaign.srm --output build/packets.json
python -B -m tools.save_data.campaign_cli packets-edit --project-root . --source build/packets.json --edits ./packets-changes.json --output build/packets-edited.json
python -B -m tools.save_data.campaign_cli packets-import --project-root . --source build/packets-edited.json --original-logical ./campaign.srm --output build/packets-edited.srm
```

The edit document holds expected and new values. Import against the same original save and write the result to a new file.
