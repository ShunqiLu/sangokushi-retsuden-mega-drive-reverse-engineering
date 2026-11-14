# 現在のセーブの固定フィールド

[简体中文](README_NAMED_CAMPAIGN.md) · [繁體中文](README_NAMED_CAMPAIGN.zh-TW.md) · **日本語** · [English](README_NAMED_CAMPAIGN.en.md)

[`named_campaign.py`](named_campaign.py) は現在のセーブの固定区間 49 個を都市、勢力、武将レコードに整理します。ビューの形式は `g5510-named-campaign-v1` です。各グループは 0 始まりの `record_index` で元の保存スロットを特定します。残りの区間は `remaining_segments` の ID で保持し、配置とビット幅は `storage` が示します。

| グループ | 編集可能なフィールド |
| --- | --- |
| 都市 | `gold`、`rice`、`income_base`、`development`、`income_split`、`welfare`、`income_rate`、`defense`、`force_index_code`、`representative_officer_code`。 |
| 勢力 | `representative_officer_code`。 |
| 武将 | `readiness_current`、`combat_weighting_operand`、`intelligence`、`troop_capacity_base_div5_code`、`combat_growth_score`、`intelligence_growth_score`、`virtue`、`education_rating`、`movement_factor`、`training_percent`、`class_status_flags`、`troop_count`、`assigned_city_code`。 |

値は実際のセーブのビット幅に従います。F428 の `0xF` と E640／F460 の `0x1FF` は番兵値です。B800 は 5 で割った値を保存します。元の変換、未命名の区間、番兵値、不明なビットは同じ形式で保持します。

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli export --project-root . --source input.srm --output build/campaign.json
python -B -X utf8 -m tools.save_data.campaign_cli edit --project-root . --source build/campaign.json --edits campaign-edits.json --output build/campaign-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli import --project-root . --source build/campaign-edited.json --original-logical input.srm --output build/campaign-edited.srm
```

`g5510-named-campaign-edits-v1` 形式の編集ファイルは `format` と `edits` を含みます。各項目は `group`、`record_index`、`field`、`expected_value`、`value` を使います。対象を明示した変更を一括適用し、新しいファイルを返します。

`from_fixed_segments` と `to_fixed_segments` は固定区間全体を変換します。`from_logical` は有効な 8192 バイトの論理 SRAM を使い、取得元を記録します。`with_edits` は検証済みの変更を適用し、`to_logical` は同じ基準から新しいセーブを作ります。行軍部隊と輸送フィールドについては[部隊ビュー](README_CAMPAIGN_PACKETS.ja.md)と[輸送ビュー](README_CAMPAIGN_ORDERS.ja.md)を参照してください。
