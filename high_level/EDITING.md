# 编辑游戏内容

游戏规则位于本源码目录。图像、声音和剧本数据位于通过 `--resource-root` 选择的[素材根](ASSETS.md)。

| 内容 | 编辑入口 |
| --- | --- |
| 内政、行军、战斗、AI 和场景规则 | `tools/high_level_*/business*.py` 中的领域函数，以及各领域的 `compiler*.py` 和 `target.py` |
| 城市、武将、势力初值和剧本装备 | [具名剧本数据](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.md) |
| AI 命令比较阈值 | [48 对 WORD 阈值](tools/high_level_rom/README_AI_POLICY_SOURCES.md) |
| AI 候选资格 | [14 × 14 BYTE 资格表](tools/high_level_rom/README_AI_SELECTION_SOURCES.md) |
| 中文对话、武将名和城市名 | [可读文字格式](tools/high_level_rom/README_READABLE_TEXT.md) |
| 战斗背景 | [地图格和属性](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.md)、[索引图块 PNG](tools/high_level_rom/README_BATTLE_TILE_SHEET.md) |
| 人物头像 | [姓名、布局、调色板和共享图块](PORTRAITS.md) |
| 音乐、音效和音色 | [具名乐谱和事件源](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.md)、[共享事件编辑器](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.md) |
| 当前存档 | [固定城市／武将／势力记录](tools/save_data/README_NAMED_CAMPAIGN.md)、[行军队伍](tools/save_data/README_CAMPAIGN_PACKETS.md)、[运输命令](tools/save_data/README_CAMPAIGN_ORDERS.md) |

## 游戏规则与构建

业务函数负责规则和状态变化，`contexts*.py` 描述输入与协作接口，编译器和目标声明负责指令、地址、寄存器语义及固定空间。可编译的改动使用所属领域支持的 Python 语句与状态接口。原版边界行为参见[兼容行为记录](docs/ORIGINAL_GAME_BUGS.md)。

编辑后的资源通过其正常登记入口参加[镜像构建](tools/high_level_rom/README_BUILD.md)。生成的镜像是产物；可重用的改动保存在规则源码或本地素材源。

## 批量编辑结构化数据

编辑 API 接收完整输入与一批明确的记录、旧值和新值，返回一个独立候选。原字段的位宽、别名和文件拓扑由各自的编码器保持。

```python
from tools.high_level_rom.scenario_sources import with_scenario_fields

scenario = source["scenarios"][0]
city = next(row for row in scenario["cities"] if row["id"] == 3)
edited = with_scenario_fields(source, [{
    "scenario_id": scenario["id"],
    "group": "cities",
    "record_id": city["id"],
    "field": "gold",
    "expected_value": city["gold"],
    "value": 12000,
}])
```

剧本以物理记录 ID 选择目标，装备使用源 BYTE 索引。城市的开发、民生和城防对应低 WORD，编码器保留同槽的高 WORD。文字编辑保留固定字槽和控制 WORD；声音编辑以完整视图标识原事件，保留命令种类和尺寸。

## 当前存档

[存档命令](tools/save_data/README.md)以显式的 8 KiB 逻辑保存介质为基线。固定字段、行军队伍和运输命令各有独立视图，回写产生新文件。组合编辑以当前候选存档作为下一项编辑的基线。每种视图沿用游戏的位宽、校验和以及未用数据。
