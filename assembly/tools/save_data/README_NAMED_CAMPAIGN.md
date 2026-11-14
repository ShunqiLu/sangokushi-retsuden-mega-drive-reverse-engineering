# 编辑存档中的城市、武将和势力

**简体中文** · [繁體中文](README_NAMED_CAMPAIGN.zh-TW.md) · [日本語](README_NAMED_CAMPAIGN.ja.md) · [English](README_NAMED_CAMPAIGN.en.md)

固定记录视图按城市、武将和势力整理金钱、粮食、兵力、归属及状态。编码器保留各段的字段位宽、量化规则和保留位。

从汇编版根目录执行。使用 8 KiB 的本地逻辑存档作为起点，并为结果准备 `build/`。

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli export --project-root . --source ./campaign.srm --output build/campaign.json
python -B -m tools.save_data.campaign_cli edit --project-root . --source build/campaign.json --edits ./campaign-changes.json --output build/campaign-edited.json
python -B -m tools.save_data.campaign_cli import --project-root . --source build/campaign-edited.json --original-logical ./campaign.srm --output build/campaign-edited.srm
```

编辑文档携带原值和新值。导入以同一个原始存档为基线，将结果写入新的存档文件。
