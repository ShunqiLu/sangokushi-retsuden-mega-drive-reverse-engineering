# CE00 運輸命令

[简体中文](README_CAMPAIGN_ORDERS.md) · **繁體中文** · [日本語](README_CAMPAIGN_ORDERS.ja.md) · [English](README_CAMPAIGN_ORDERS.en.md)

[`campaign_orders.py`](campaign_orders.py) 將當前邏輯存檔中偏移 `0x1678` 的 110 位元組表示為 40 條 CE00 記錄，每條佔 22 位。執行程式碼將碼值用於運輸種類、路徑和目的資源索引。

| 欄位 | 寬度 | 用途 |
| --- | --- | --- |
| `transport_kind_code` | 2 位 | 種類碼，參與路徑和到達獎勵選擇。 |
| `route_x` | 7 位 | 路徑第一軸座標碼。 |
| `route_y` | 7 位 | 路徑第二軸座標碼。 |
| `destination_city_code` | 6 位 | 目的城市索引碼。 |

`g5510-campaign-orders-v1` 含 `format`、`source`、`storage` 和 `orders`，記錄按零起 `record_index` 排列。運輸旗標和資源計算由實際執行產生；儲存格式保留全部 40 槽及空閒殘值。

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli orders-export --project-root . --source input.srm --output build/orders.json
python -B -X utf8 -m tools.save_data.campaign_cli orders-edit --project-root . --source build/orders.json --edits order-edits.json --output build/orders-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli orders-import --project-root . --source build/orders-edited.json --original-logical input.srm --output build/orders-edited.srm
```

編輯文件使用 `g5510-campaign-order-edits-v1`；每項包含 `order_index`、`field`、`expected_value` 和 `value`。Python 部分提供 `from_logical`、`to_records`、`with_edits` 和 `to_logical`。回寫以同一完整原邏輯存檔為基線，僅重寫 CE00 與存檔校驗和。
