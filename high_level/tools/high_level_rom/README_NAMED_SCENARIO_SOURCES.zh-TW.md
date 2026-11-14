# 具名劇本初值

[简体中文](README_NAMED_SCENARIO_SOURCES.md) · **繁體中文** · [日本語](README_NAMED_SCENARIO_SOURCES.ja.md) · [English](README_NAMED_SCENARIO_SOURCES.en.md)

[`scenario_sources.py`](scenario_sources.py) 將城市、武將、勢力的 typed 劇本列對映到 `g5510-owned-named-scenario-source-v1`。文件保留 `metadata`、`directory_targets` 和三個物理 `scenarios`。物理記錄用 `scenario_0`、`scenario_1`、`scenario_2` 標識；執行時描述符及目錄別名保留各自的引用。

| 分組 | 欄位與物理值 |
| --- | --- |
| 城市資源 | `gold`、`rice` 使用 32 位值；`development`、`welfare`、`defense` 編輯各自低 WORD 並保留高 WORD。 |
| 城市管理 | `force_index_byte`、`representative_officer_word`、`income_base_long`、`income_split_long`、`income_rate_long`、`assigned_officer_tally_long`、`troop_total_long`。 |
| 勢力 | `representative_officer_word` 與 `relationship_bits_word`；關係行保持各自方向。 |
| 武將基礎 | `intelligence_word`、`virtue_byte`、`troop_capacity_base_word`、`troop_count_long`、`assigned_city_byte`。 |
| 武將成長與狀態 | `readiness_capacity_word`、`readiness_current_word`、`combat_rating_word`、`intelligence_growth_score_word`、`combat_growth_score_word`、`education_rating_byte`、`movement_factor_byte`、`training_percent_byte`、`growth_threshold_tier_byte`、`class_status_flags_byte`。 |

BE00、C000 分別對映至兩項成長 WORD；原運算的迴繞、分母和上限由業務規則處理。B000／B200 表示同一個可恢復狀態的容量和當前值。C400 參與候選半徑和行程計算。其他位置及尚待命名的內容按原地址儲存在 `unresolved_fields`；源寬、哨兵值與未知位保持原格式。

## 批次欄位編輯

`with_scenario_fields(source, edits)` 使用 `scenario_id`、`group`、`record_id`、`field`、`expected_value` 和 `value`。城市 ID 1–40，勢力 0–15，武將 0–255。每個欄位按原 BYTE、WORD、LONG 寬度驗證；城市三項分槽欄位僅包含低 WORD 的舊值和新值。返回值是獨立具名文件。

已有具名文件可直接用於 `edit`；示例的 `export` 從含 typed 源的 `$typedResources` 生成具名文件。輸出寫入已有 `build/` 下的新檔案。

```powershell
python -B -X utf8 -m tools.high_level_rom.scenario_sources export --project-root . --source "$typedResources/resources/data/scenario_build.json" --output build/scenario.named.json
python -B -X utf8 -m tools.high_level_rom.scenario_sources edit --project-root . --source build/scenario.named.json --edits scenario-edits.json --output build/scenario.edited.json
```

`to_named` 和 `from_named` 轉換純資料表示。`import` 將具名文件轉換為原 typed 格式；登記資源 ID 為 `scenario_build`。

## 初始裝備 BYTE

`unresolved_fields.ram_ea88` 為 `source_byte0`、`source_byte1`、`source_byte2`，執行時讀取次序為 1、0、2。`with_equipment_source_bytes` 或 `edit-equipment --edits` 使用 `scenario_id`、`officer_id`、`source_byte_index`、`expected_value` 和 `value`。BYTE 值範圍為 0–255，其他槽與劇本別名保持原關係。
