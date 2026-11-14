# 都市・編成命令

[简体中文](README_SELECTED_COMMANDS.md) · [繁體中文](README_SELECTED_COMMANDS.zh-TW.md) · **日本語** · [English](README_SELECTED_COMMANDS.en.md)

[`selected_command_steps.py`](selected_command_steps.py) は選択済みの都市または編成命令を進めます。呼び出し側は選択結果、素材、ゲーム状態を同じ実行フレームで渡します。各ハンドラーは元の引数幅、子呼び出しフレーム、復帰条件、デバイス境界を保って命令を実行します。

都市命令表は [`city_command_steps.py`](city_command_steps.py) にあります。命令の引数とパネルは [`command_panel_steps.py`](command_panel_steps.py) が管理します。
