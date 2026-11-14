# 存档工具

`save_format` 识别存档封装、验证校验信息并读写资源段。`campaign_cli` 提供当前进度的具名编辑。原始存档作为输入保存，新存档采用独立路径。

```powershell
python -B -m tools.save_data.save_format inspect ./campaign.srm
python -B -m tools.save_data.save_format extract ./campaign.srm ./save-source
python -B -m tools.save_data.save_format import ./save-source ./campaign-edited.srm
```

具名工具分别处理[城市、武将和势力](README_NAMED_CAMPAIGN.md)、[行军队伍](README_CAMPAIGN_PACKETS.md)及[运输指令](README_CAMPAIGN_ORDERS.md)。初始剧本由本地素材包中的 `resources/data/scenario_build.json` 提供。
