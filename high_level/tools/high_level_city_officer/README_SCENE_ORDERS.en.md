# City orders and faction relations

[简体中文](README_SCENE_ORDERS.md) · [繁體中文](README_SCENE_ORDERS.zh-TW.md) · [日本語](README_SCENE_ORDERS.ja.md) · **English**

[`business_scene_orders.py`](business_scene_orders.py) handles live city command state, diplomatic agreements, and resource settlement. The full frame carries the city, faction, selected command, and call context. The rules update resources and flags using actual city and relation records.

Relation rows use WORD faction masks and the direction supplied by each record. Primary and secondary resources retain their physical slots, field widths, and multiplication and division behavior. See [Named scenarios](../high_level_rom/README_NAMED_SCENARIO_SOURCES.en.md) for offline starting values and relations.
