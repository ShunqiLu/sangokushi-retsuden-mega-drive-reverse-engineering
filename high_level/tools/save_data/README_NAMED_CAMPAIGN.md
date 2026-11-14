# 当前存档的固定字段

[`named_campaign.py`](named_campaign.py) 将当前存档的 49 个固定段组织为城市、势力和武将记录。视图格式为 `g5510-named-campaign-v1`；各组用零起 `record_index` 定位原存储槽。其余段按 ID 保存在 `remaining_segments`，布局和位宽由 `storage` 提供。

| 分组 | 可编辑字段 |
| --- | --- |
| 城市 | `gold`、`rice`、`income_base`、`development`、`income_split`、`welfare`、`income_rate`、`defense`、`force_index_code`、`representative_officer_code`。 |
| 势力 | `representative_officer_code`。 |
| 武将 | `readiness_current`、`combat_weighting_operand`、`intelligence`、`troop_capacity_base_div5_code`、`combat_growth_score`、`intelligence_growth_score`、`virtue`、`education_rating`、`movement_factor`、`training_percent`、`class_status_flags`、`troop_count`、`assigned_city_code`。 |

值使用实际存档码宽。F428 的 `0xF` 与 E640／F460 的 `0x1FF` 是保存哨兵；B800 使用除以 5 的保存码。原变换、未具名段、哨兵及未知位都保留在同一格式中。

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli export --project-root . --source input.srm --output build/campaign.json
python -B -X utf8 -m tools.save_data.campaign_cli edit --project-root . --source build/campaign.json --edits campaign-edits.json --output build/campaign-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli import --project-root . --source build/campaign-edited.json --original-logical input.srm --output build/campaign-edited.srm
```

`g5510-named-campaign-edits-v1` 编辑文件含 `format` 与 `edits`，各项使用 `group`、`record_index`、`field`、`expected_value` 和 `value`。处理整批确切目标并产生新文档。

`from_fixed_segments` 和 `to_fixed_segments` 转换完整固定段；`from_logical` 使用有效的 8192 字节逻辑 SRAM 并记录来源；`with_edits` 应用已核对的编辑，`to_logical` 根据同一份基线形成新存档。行军队伍和运输字段分别见[队伍视图](README_CAMPAIGN_PACKETS.md)与[运输视图](README_CAMPAIGN_ORDERS.md)。
