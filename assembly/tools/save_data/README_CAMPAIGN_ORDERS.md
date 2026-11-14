# 编辑存档中的运输指令

运输视图对应 CE00 中的 40 个保存槽。它记录类型、路线坐标和目标城市等编码值；导入保留空槽和其他存档段。

从汇编版根目录执行。使用 8 KiB 的本地逻辑存档作为起点，并为结果准备 `build/`。

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli orders-export --project-root . --source ./campaign.srm --output build/orders.json
python -B -m tools.save_data.campaign_cli orders-edit --project-root . --source build/orders.json --edits ./orders-changes.json --output build/orders-edited.json
python -B -m tools.save_data.campaign_cli orders-import --project-root . --source build/orders-edited.json --original-logical ./campaign.srm --output build/orders-edited.srm
```

编辑文档携带原值和新值。导入以同一个原始存档为基线，将结果写入新的存档文件。
