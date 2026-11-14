# 编辑存档中的行军队伍

**简体中文** · [繁體中文](README_CAMPAIGN_PACKETS.zh-TW.md) · [日本語](README_CAMPAIGN_PACKETS.ja.md) · [English](README_CAMPAIGN_PACKETS.en.md)

行军视图保存有序队伍、武将编号、地图坐标、势力及所携资源。原记录数、成员数和保存字段宽度约束编辑范围。

从汇编版根目录执行。使用 8 KiB 的本地逻辑存档作为起点，并为结果准备 `build/`。

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli packets-export --project-root . --source ./campaign.srm --output build/packets.json
python -B -m tools.save_data.campaign_cli packets-edit --project-root . --source build/packets.json --edits ./packets-changes.json --output build/packets-edited.json
python -B -m tools.save_data.campaign_cli packets-import --project-root . --source build/packets-edited.json --original-logical ./campaign.srm --output build/packets-edited.srm
```

编辑文档携带原值和新值。导入以同一个原始存档为基线，将结果写入新的存档文件。
