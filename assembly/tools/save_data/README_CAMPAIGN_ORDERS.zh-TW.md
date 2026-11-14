# 編輯存檔中的運輸指令

[简体中文](README_CAMPAIGN_ORDERS.md) · **繁體中文** · [日本語](README_CAMPAIGN_ORDERS.ja.md) · [English](README_CAMPAIGN_ORDERS.en.md)

運輸檢視對應 CE00 中的 40 個儲存槽。它記錄型別、路線座標和目標城市等編碼值；匯入保留空槽和其他存檔段。

從彙編版根目錄執行。使用 8 KiB 的本地邏輯存檔作為起點，併為結果準備 `build/`。

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli orders-export --project-root . --source ./campaign.srm --output build/orders.json
python -B -m tools.save_data.campaign_cli orders-edit --project-root . --source build/orders.json --edits ./orders-changes.json --output build/orders-edited.json
python -B -m tools.save_data.campaign_cli orders-import --project-root . --source build/orders-edited.json --original-logical ./campaign.srm --output build/orders-edited.srm
```

編輯文件攜帶原值和新值。匯入以同一個原始存檔為基線，將結果寫入新的存檔檔案。
