# Transport orders in saves

[简体中文](README_CAMPAIGN_ORDERS.md) · [繁體中文](README_CAMPAIGN_ORDERS.zh-TW.md) · [日本語](README_CAMPAIGN_ORDERS.ja.md) · **English**

The transport view corresponds to 40 save slots in CE00. It shows encoded types, route coordinates, and destination cities. Import preserves empty slots and other save sections.

Run from the assembly root. Provide a local 8 KiB logical save and prepare `build/` for the results.

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli orders-export --project-root . --source ./campaign.srm --output build/orders.json
python -B -m tools.save_data.campaign_cli orders-edit --project-root . --source build/orders.json --edits ./orders-changes.json --output build/orders-edited.json
python -B -m tools.save_data.campaign_cli orders-import --project-root . --source build/orders-edited.json --original-logical ./campaign.srm --output build/orders-edited.srm
```

The edit document holds expected and new values. Import against the same original save and write the result to a new file.
