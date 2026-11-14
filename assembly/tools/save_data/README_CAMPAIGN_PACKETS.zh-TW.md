# 編輯存檔中的行軍隊伍

[简体中文](README_CAMPAIGN_PACKETS.md) · **繁體中文** · [日本語](README_CAMPAIGN_PACKETS.ja.md) · [English](README_CAMPAIGN_PACKETS.en.md)

行軍檢視儲存有序隊伍、武將編號、地圖座標、勢力及所攜資源。原記錄數、成員數和儲存欄位寬度約束編輯範圍。

從彙編版根目錄執行。使用 8 KiB 的本地邏輯存檔作為起點，併為結果準備 `build/`。

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli packets-export --project-root . --source ./campaign.srm --output build/packets.json
python -B -m tools.save_data.campaign_cli packets-edit --project-root . --source build/packets.json --edits ./packets-changes.json --output build/packets-edited.json
python -B -m tools.save_data.campaign_cli packets-import --project-root . --source build/packets-edited.json --original-logical ./campaign.srm --output build/packets-edited.srm
```

編輯文件攜帶原值和新值。匯入以同一個原始存檔為基線，將結果寫入新的存檔檔案。
