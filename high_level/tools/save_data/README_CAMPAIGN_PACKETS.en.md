# Current marching units

[简体中文](README_CAMPAIGN_PACKETS.md) · [繁體中文](README_CAMPAIGN_PACKETS.zh-TW.md) · [日本語](README_CAMPAIGN_PACKETS.ja.md) · **English**

[`campaign_packets.py`](campaign_packets.py) represents variable-length RAM9000 records in the logical save as coordinates, factions, carried resources, and officer lists. The current view uses `g5510-campaign-packets-v2`.

| Field | Width and meaning |
| --- | --- |
| `map_x` | 7 bits, horizontal coordinate. |
| `map_y` | 7 bits, vertical coordinate. |
| `force_index_code` | 4-bit faction code. |
| `gold_saved_code` | 18-bit carried gold code. |
| `rice_saved_code` | 20-bit carried rice code. |
| `officer_ids` | Ordered list of officer BYTEs. |

`storage` records the original bit offset, encoded length, and each unit's member count. `source.logical_hex` supplies the complete original logical baseline. Counts derive from the lists; writeback keeps the existing records, order, and counts. The game recalculates movement parameters when loading.

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli packets-export --project-root . --source input.srm --output build/packets.json
python -B -X utf8 -m tools.save_data.campaign_cli packets-edit --project-root . --source build/packets.json --edits packet-edits.json --output build/packets-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli packets-import --project-root . --source build/packets-edited.json --original-logical input.srm --output build/packets-edited.srm
```

Version 2 edits use `g5510-campaign-packet-edits-v2`. Each entry contains `packet_index`, `field`, `expected_value`, and `value`. Replace a roster with a full list of the same length. Version 1 documents use their matching edit format and original field mappings. Python offers `from_logical`, `to_records`, `with_edits`, and `to_logical`. Use the variable stream option in the [low-level save tools](README.en.md) to change unit record geometry.
