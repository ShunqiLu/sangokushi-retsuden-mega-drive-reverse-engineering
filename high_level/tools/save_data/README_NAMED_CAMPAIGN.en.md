# Fixed fields in the current save

[简体中文](README_NAMED_CAMPAIGN.md) · [繁體中文](README_NAMED_CAMPAIGN.zh-TW.md) · [日本語](README_NAMED_CAMPAIGN.ja.md) · **English**

[`named_campaign.py`](named_campaign.py) maps the current save's 49 fixed sections to city, faction, and officer records. The view uses `g5510-named-campaign-v1`. Each group locates original storage slots with zero-based `record_index`. The remaining sections use IDs in `remaining_segments`; `storage` provides their layout and bit widths.

| Group | Editable fields |
| --- | --- |
| Cities | `gold`, `rice`, `income_base`, `development`, `income_split`, `welfare`, `income_rate`, `defense`, `force_index_code`, `representative_officer_code`. |
| Factions | `representative_officer_code`. |
| Officers | `readiness_current`, `combat_weighting_operand`, `intelligence`, `troop_capacity_base_div5_code`, `combat_growth_score`, `intelligence_growth_score`, `virtue`, `education_rating`, `movement_factor`, `training_percent`, `class_status_flags`, `troop_count`, `assigned_city_code`. |

Values follow the actual save bit widths. `0xF` in F428 and `0x1FF` in E640/F460 are sentinels. B800 stores a value divided by 5. Original transformations, unnamed sections, sentinels, and unknown bits stay in the same format.

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli export --project-root . --source input.srm --output build/campaign.json
python -B -X utf8 -m tools.save_data.campaign_cli edit --project-root . --source build/campaign.json --edits campaign-edits.json --output build/campaign-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli import --project-root . --source build/campaign-edited.json --original-logical input.srm --output build/campaign-edited.srm
```

A `g5510-named-campaign-edits-v1` edit file contains `format` and `edits`. Each item uses `group`, `record_index`, `field`, `expected_value`, and `value`. The tool applies the batch of exact targets and returns a new document.

`from_fixed_segments` and `to_fixed_segments` convert whole fixed sections. `from_logical` takes valid 8192-byte logical SRAM and records its source. `with_edits` applies checked edits, and `to_logical` builds a new save against the same baseline. For marching units and transport fields, see the [unit view](README_CAMPAIGN_PACKETS.en.md) and [transport view](README_CAMPAIGN_ORDERS.en.md).
