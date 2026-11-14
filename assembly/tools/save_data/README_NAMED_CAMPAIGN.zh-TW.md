# 編輯存檔中的城市、武將和勢力

[简体中文](README_NAMED_CAMPAIGN.md) · **繁體中文** · [日本語](README_NAMED_CAMPAIGN.ja.md) · [English](README_NAMED_CAMPAIGN.en.md)

固定記錄檢視按城市、武將和勢力整理金錢、糧食、兵力、歸屬及狀態。編碼器保留各段的欄位位寬、量化規則和保留位。

從彙編版根目錄執行。使用 8 KiB 的本地邏輯存檔作為起點，併為結果準備 `build/`。

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli export --project-root . --source ./campaign.srm --output build/campaign.json
python -B -m tools.save_data.campaign_cli edit --project-root . --source build/campaign.json --edits ./campaign-changes.json --output build/campaign-edited.json
python -B -m tools.save_data.campaign_cli import --project-root . --source build/campaign-edited.json --original-logical ./campaign.srm --output build/campaign-edited.srm
```

編輯文件攜帶原值和新值。匯入以同一個原始存檔為基線，將結果寫入新的存檔檔案。
