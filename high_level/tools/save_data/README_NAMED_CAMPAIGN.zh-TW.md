# 當前存檔的固定欄位

[简体中文](README_NAMED_CAMPAIGN.md) · **繁體中文** · [日本語](README_NAMED_CAMPAIGN.ja.md) · [English](README_NAMED_CAMPAIGN.en.md)

[`named_campaign.py`](named_campaign.py) 將當前存檔的 49 個固定段組織為城市、勢力和武將記錄。檢視格式為 `g5510-named-campaign-v1`；各組用零起 `record_index` 定位原儲存槽。其餘段按 ID 儲存在 `remaining_segments`，佈局和位寬由 `storage` 提供。

| 分組 | 可編輯欄位 |
| --- | --- |
| 城市 | `gold`、`rice`、`income_base`、`development`、`income_split`、`welfare`、`income_rate`、`defense`、`force_index_code`、`representative_officer_code`。 |
| 勢力 | `representative_officer_code`。 |
| 武將 | `readiness_current`、`combat_weighting_operand`、`intelligence`、`troop_capacity_base_div5_code`、`combat_growth_score`、`intelligence_growth_score`、`virtue`、`education_rating`、`movement_factor`、`training_percent`、`class_status_flags`、`troop_count`、`assigned_city_code`。 |

值使用實際存檔碼寬。F428 的 `0xF` 與 E640／F460 的 `0x1FF` 是儲存哨兵；B800 使用除以 5 的儲存碼。原變換、未具名段、哨兵及未知位都保留在同一格式中。

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli export --project-root . --source input.srm --output build/campaign.json
python -B -X utf8 -m tools.save_data.campaign_cli edit --project-root . --source build/campaign.json --edits campaign-edits.json --output build/campaign-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli import --project-root . --source build/campaign-edited.json --original-logical input.srm --output build/campaign-edited.srm
```

`g5510-named-campaign-edits-v1` 編輯檔案含 `format` 與 `edits`，各項使用 `group`、`record_index`、`field`、`expected_value` 和 `value`。處理整批確切目標併產生新文件。

`from_fixed_segments` 和 `to_fixed_segments` 轉換完整固定段；`from_logical` 使用有效的 8192 位元組邏輯 SRAM 並記錄來源；`with_edits` 應用已核對的編輯，`to_logical` 根據同一份基線形成新存檔。行軍隊伍和運輸欄位分別見[隊伍檢視](README_CAMPAIGN_PACKETS.zh-TW.md)與[運輸檢視](README_CAMPAIGN_ORDERS.zh-TW.md)。
