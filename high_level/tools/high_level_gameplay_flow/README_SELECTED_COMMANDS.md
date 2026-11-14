# 城市与编组命令

[`selected_command_steps.py`](selected_command_steps.py) 推进当前场景已选定的城市或编组命令。调用方通过同一现场帧传入选择结果、资源和游戏状态。各命令通过相应的业务处理器执行，保留原参数位宽、子调用帧、返回条件和设备边界。

城市命令表位于 [`city_command_steps.py`](city_command_steps.py)，命令参数与面板由 [`command_panel_steps.py`](command_panel_steps.py) 管理。
