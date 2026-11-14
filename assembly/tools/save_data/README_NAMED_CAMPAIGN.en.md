# Cities, officers, and factions in saves

[简体中文](README_NAMED_CAMPAIGN.md) · [繁體中文](README_NAMED_CAMPAIGN.zh-TW.md) · [日本語](README_NAMED_CAMPAIGN.ja.md) · **English**

The fixed record view groups gold, grain, troops, affiliations, and status by city, officer, and faction. The encoder preserves field widths, quantization rules, and reserved bits.

Run from the assembly root. Provide a local 8 KiB logical save and prepare `build/` for the results.

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli export --project-root . --source ./campaign.srm --output build/campaign.json
python -B -m tools.save_data.campaign_cli edit --project-root . --source build/campaign.json --edits ./campaign-changes.json --output build/campaign-edited.json
python -B -m tools.save_data.campaign_cli import --project-root . --source build/campaign-edited.json --original-logical ./campaign.srm --output build/campaign-edited.srm
```

The edit document holds expected and new values. Import against the same original save and write the result to a new file.
