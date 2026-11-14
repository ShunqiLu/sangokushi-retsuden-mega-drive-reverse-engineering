# SRAM 与存档工具

本目录提供对逻辑 SRAM 的查看、解包、编辑与回写。G-5510 的存储区使用奇地址 `0x200001–0x203FFF`，逻辑介质为 8192 字节；工具也识别逐字节重复为两份的 16 KiB MAME 容器。

```powershell
python tools/save_data/save_format.py inspect input.srm
python tools/save_data/save_format.py extract input.srm save-fields
python tools/save_data/save_format.py import save-fields edited.srm
```

解包核对 `SEGA` 签名和原加法校验和，导出布局、字段及保存介质基线。回写使用新文件，保留容器形状、未知字节和字段位宽，重新计算原校验和。`--allow-variable-resize` 显式允许改变队伍位流的编码长度，并将随后的空余校验区填为 `FF`。

## 当前游戏的逻辑视图

- [城市、武将与势力固定段](README_NAMED_CAMPAIGN.md)。
- [行军队伍、坐标和携带资源](README_CAMPAIGN_PACKETS.md)。
- [CE00 运输命令](README_CAMPAIGN_ORDERS.md)。

这些编辑模式使用有效的 8192 字节逻辑基线，并生成新的候选文件。桌面应用的 `export_save` 导出当前 SRAM 内容；签名和校验和由存档工具检查。随后在[本地运行配置](../reconstructed_game/README_LOCAL_CONFIG.md)指定所需介质。初始剧本另由[剧本数据工具](../high_level_rom/README_NAMED_SCENARIO_SOURCES.md)管理。
