# 编辑游戏内容

程序和工具路径从本目录算起，素材路径从构建参数 `--resource-root` 所选目录算起。建议在本地副本编辑，随后从源码重新构建。

| 内容 | 编辑入口 |
| --- | --- |
| 68000 和 Z80 程序 | `src/m68k/`、`src/z80/`；指令范围见 `tools/reconstructed_assembly/layout/` |
| 城市、武将和势力的剧本初值 | 素材根的 `resources/data/scenario_build.json`；见[剧本编辑](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.md) |
| 对话、武将名和城市名 | `resources/data/dialogue_text.json`；见[文字编辑](tools/high_level_rom/README_READABLE_TEXT.md) |
| AI 参数 | `resources/data/ai_threshold_pair_fields.json`、`resources/data/ai_selection_fields.json`；见[判断阈值](tools/high_level_rom/README_AI_POLICY_SOURCES.md)和[候选资格](tools/high_level_rom/README_AI_SELECTION_SOURCES.md) |
| 图像和配色 | `assets/images/` 及对应布局、调色 JSON；见[素材指南](ASSETS.md)、[战斗背景布局](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.md)、[图块表](tools/high_level_rom/README_BATTLE_TILE_SHEET.md)和[人物头像](PORTRAITS.md) |
| 乐曲、音效和音色 | `resources/audio/` 及其引用的 `assets/audio/`；见[音频序列](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.md)和[共享事件](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.md) |
| 当前存档 | [存档工具](tools/save_data/README.md)：[城市与势力](tools/save_data/README_NAMED_CAMPAIGN.md)、[行军队伍](tools/save_data/README_CAMPAIGN_PACKETS.md)、[运输指令](tools/save_data/README_CAMPAIGN_ORDERS.md) |

索引 PNG 用像素编号表达图块数据。请保留像素模式、尺寸和原文件路径，通过对应的调色 JSON 修改显示颜色。按[构建说明](README.md)把修改后的素材根交给编译器。
