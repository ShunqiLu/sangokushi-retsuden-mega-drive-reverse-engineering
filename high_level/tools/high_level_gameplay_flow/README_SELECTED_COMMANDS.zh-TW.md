# 城市與編組命令

[简体中文](README_SELECTED_COMMANDS.md) · **繁體中文** · [日本語](README_SELECTED_COMMANDS.ja.md) · [English](README_SELECTED_COMMANDS.en.md)

[`selected_command_steps.py`](selected_command_steps.py) 推進當前場景已選定的城市或編組命令。呼叫方透過同一現場幀傳入選擇結果、資源和遊戲狀態。各命令透過相應的業務處理器執行，保留原引數位寬、子呼叫幀、返回條件和裝置邊界。

城市命令表位於 [`city_command_steps.py`](city_command_steps.py)，命令引數與面板由 [`command_panel_steps.py`](command_panel_steps.py) 管理。
