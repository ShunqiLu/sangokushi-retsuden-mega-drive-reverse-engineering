# City and formation commands

[简体中文](README_SELECTED_COMMANDS.md) · [繁體中文](README_SELECTED_COMMANDS.zh-TW.md) · [日本語](README_SELECTED_COMMANDS.ja.md) · **English**

[`selected_command_steps.py`](selected_command_steps.py) advances the selected city or formation command. The caller provides the selection, resources, and game state in one live frame. Corresponding handlers execute commands with their original parameter widths, subcall frames, return conditions, and device boundaries.

The city command table is in [`city_command_steps.py`](city_command_steps.py). [`command_panel_steps.py`](command_panel_steps.py) handles command parameters and panels.
