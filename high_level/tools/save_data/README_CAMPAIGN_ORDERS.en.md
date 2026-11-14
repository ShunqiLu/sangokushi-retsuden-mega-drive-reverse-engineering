# CE00 transport orders

[简体中文](README_CAMPAIGN_ORDERS.md) · [繁體中文](README_CAMPAIGN_ORDERS.zh-TW.md) · [日本語](README_CAMPAIGN_ORDERS.ja.md) · **English**

[`campaign_orders.py`](campaign_orders.py) represents 110 bytes at offset `0x1678` in the current logical save as 40 CE00 records, 22 bits each. Runtime code uses the encoded values for transport type, route, and destination resource index.

| Field | Width | Purpose |
| --- | --- | --- |
| `transport_kind_code` | 2 bits | Type code for route and arrival reward selection. |
| `route_x` | 7 bits | Route coordinate code on the first axis. |
| `route_y` | 7 bits | Route coordinate code on the second axis. |
| `destination_city_code` | 6 bits | Destination city index code. |

`g5510-campaign-orders-v1` contains `format`, `source`, `storage`, and `orders`. Records are ordered by zero-based `record_index`. Runtime computes flags and resources. The save format preserves all 40 slots and their unused values.

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli orders-export --project-root . --source input.srm --output build/orders.json
python -B -X utf8 -m tools.save_data.campaign_cli orders-edit --project-root . --source build/orders.json --edits order-edits.json --output build/orders-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli orders-import --project-root . --source build/orders-edited.json --original-logical input.srm --output build/orders-edited.srm
```

Edits use `g5510-campaign-order-edits-v1`; each entry includes `order_index`, `field`, `expected_value`, and `value`. The Python interfaces are `from_logical`, `to_records`, `with_edits`, and `to_logical`. Write against the same complete original logical save and update only CE00 and the checksum.
