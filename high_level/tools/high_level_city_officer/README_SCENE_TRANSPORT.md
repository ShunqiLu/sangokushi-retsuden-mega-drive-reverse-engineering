# 运输命令与场景运行

[`business_scene_transport.py`](business_scene_transport.py) 管理场景中的运输方向、路径推进、碰撞与到达。当前场景提供地图、相邻坐标和运输记录；运输业务规则读写同一运行状态。输送队抵达城市后，城市收货处理按原字段宽度写入资源，保留游戏的回绕和封顶语义。

离线的 [CE00 运输命令视图](../save_data/README_CAMPAIGN_ORDERS.md) 负责存档表示。运行中的旗标、速度和货物由场景业务状态提供。
