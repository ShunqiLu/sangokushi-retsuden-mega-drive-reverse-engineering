# 存檔工具

[简体中文](README.md) · **繁體中文** · [日本語](README.ja.md) · [English](README.en.md)

`save_format` 識別存檔封裝、驗證校驗資訊並讀寫資源段。`campaign_cli` 提供當前進度的具名編輯。原始存檔作為輸入儲存，新存檔採用獨立路徑。

```powershell
python -B -m tools.save_data.save_format inspect ./campaign.srm
python -B -m tools.save_data.save_format extract ./campaign.srm ./save-source
python -B -m tools.save_data.save_format import ./save-source ./campaign-edited.srm
```

具名工具分別處理[城市、武將和勢力](README_NAMED_CAMPAIGN.zh-TW.md)、[行軍隊伍](README_CAMPAIGN_PACKETS.zh-TW.md)及[運輸指令](README_CAMPAIGN_ORDERS.zh-TW.md)。初始劇本由本地素材包中的 `resources/data/scenario_build.json` 提供。
