# 城市命令与关系资源

[`business_scene_orders.py`](business_scene_orders.py) 处理城市命令的即时现场状态、关系协议以及资源结算。完整帧带入城市、势力、选中命令及调用上下文；业务规则根据实际城市和关系记录更新资源与条件码。

关系行使用 WORD 的势力位图，按记录提供的方向读取。主、次资源分别沿用各自的物理槽、字段宽度和乘除行为。离线初始值和势力关系见[具名剧本](../high_level_rom/README_NAMED_SCENARIO_SOURCES.md)。
