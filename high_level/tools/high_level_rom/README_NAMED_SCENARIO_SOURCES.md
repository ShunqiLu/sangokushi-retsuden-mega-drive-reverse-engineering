# 具名剧本初值

**简体中文** · [繁體中文](README_NAMED_SCENARIO_SOURCES.zh-TW.md) · [日本語](README_NAMED_SCENARIO_SOURCES.ja.md) · [English](README_NAMED_SCENARIO_SOURCES.en.md)

[`scenario_sources.py`](scenario_sources.py) 将城市、武将、势力的 typed 剧本列映射到 `g5510-owned-named-scenario-source-v1`。文档保留 `metadata`、`directory_targets` 和三个物理 `scenarios`。物理记录用 `scenario_0`、`scenario_1`、`scenario_2` 标识；运行时描述符及目录别名保留各自的引用。

| 分组 | 字段与物理值 |
| --- | --- |
| 城市资源 | `gold`、`rice` 使用 32 位值；`development`、`welfare`、`defense` 编辑各自低 WORD 并保留高 WORD。 |
| 城市管理 | `force_index_byte`、`representative_officer_word`、`income_base_long`、`income_split_long`、`income_rate_long`、`assigned_officer_tally_long`、`troop_total_long`。 |
| 势力 | `representative_officer_word` 与 `relationship_bits_word`；关系行保持各自方向。 |
| 武将基础 | `intelligence_word`、`virtue_byte`、`troop_capacity_base_word`、`troop_count_long`、`assigned_city_byte`。 |
| 武将成长与状态 | `readiness_capacity_word`、`readiness_current_word`、`combat_rating_word`、`intelligence_growth_score_word`、`combat_growth_score_word`、`education_rating_byte`、`movement_factor_byte`、`training_percent_byte`、`growth_threshold_tier_byte`、`class_status_flags_byte`。 |

BE00、C000 分别映射至两项成长 WORD；原运算的回绕、分母和上限由业务规则处理。B000／B200 表示同一个可恢复状态的容量和当前值。C400 参与候选半径和行程计算。其他位置及尚待命名的内容按原地址保存在 `unresolved_fields`；源宽、哨兵值与未知位保持原格式。

## 批量字段编辑

`with_scenario_fields(source, edits)` 使用 `scenario_id`、`group`、`record_id`、`field`、`expected_value` 和 `value`。城市 ID 1–40，势力 0–15，武将 0–255。每个字段按原 BYTE、WORD、LONG 宽度验证；城市三项分槽字段仅包含低 WORD 的旧值和新值。返回值是独立具名文档。

已有具名文档可直接用于 `edit`；示例的 `export` 从含 typed 源的 `$typedResources` 生成具名文档。输出写入已有 `build/` 下的新文件。

```powershell
python -B -X utf8 -m tools.high_level_rom.scenario_sources export --project-root . --source "$typedResources/resources/data/scenario_build.json" --output build/scenario.named.json
python -B -X utf8 -m tools.high_level_rom.scenario_sources edit --project-root . --source build/scenario.named.json --edits scenario-edits.json --output build/scenario.edited.json
```

`to_named` 和 `from_named` 转换纯数据表示。`import` 将具名文档转换为原 typed 格式；登记资源 ID 为 `scenario_build`。

## 初始装备 BYTE

`unresolved_fields.ram_ea88` 为 `source_byte0`、`source_byte1`、`source_byte2`，运行时读取次序为 1、0、2。`with_equipment_source_bytes` 或 `edit-equipment --edits` 使用 `scenario_id`、`officer_id`、`source_byte_index`、`expected_value` 和 `value`。BYTE 值范围为 0–255，其他槽与剧本别名保持原关系。
