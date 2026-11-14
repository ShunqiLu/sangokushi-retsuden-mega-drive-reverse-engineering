# 城市命令與關係資源

[简体中文](README_SCENE_ORDERS.md) · **繁體中文** · [日本語](README_SCENE_ORDERS.ja.md) · [English](README_SCENE_ORDERS.en.md)

[`business_scene_orders.py`](business_scene_orders.py) 處理城市命令的即時現場狀態、關係協議以及資源結算。完整幀帶入城市、勢力、選中命令及呼叫上下文；業務規則根據實際城市和關係記錄更新資源與條件碼。

關係行使用 WORD 的勢力點陣圖，按記錄提供的方向讀取。主、次資源分別沿用各自的物理槽、欄位寬度和乘除行為。離線初始值和勢力關係見[具名劇本](../high_level_rom/README_NAMED_SCENARIO_SOURCES.zh-TW.md)。
