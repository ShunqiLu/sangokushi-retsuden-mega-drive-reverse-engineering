# CE00 运输命令

[`campaign_orders.py`](campaign_orders.py) 将当前逻辑存档中偏移 `0x1678` 的 110 字节表示为 40 条 CE00 记录，每条占 22 位。运行代码将码值用于运输种类、路径和目的资源索引。

| 字段 | 宽度 | 用途 |
| --- | --- | --- |
| `transport_kind_code` | 2 位 | 种类码，参与路径和到达奖励选择。 |
| `route_x` | 7 位 | 路径第一轴坐标码。 |
| `route_y` | 7 位 | 路径第二轴坐标码。 |
| `destination_city_code` | 6 位 | 目的城市索引码。 |

`g5510-campaign-orders-v1` 含 `format`、`source`、`storage` 和 `orders`，记录按零起 `record_index` 排列。运输旗标和资源计算由实际运行产生；保存格式保留全部 40 槽及空闲残值。

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli orders-export --project-root . --source input.srm --output build/orders.json
python -B -X utf8 -m tools.save_data.campaign_cli orders-edit --project-root . --source build/orders.json --edits order-edits.json --output build/orders-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli orders-import --project-root . --source build/orders-edited.json --original-logical input.srm --output build/orders-edited.srm
```

编辑文档使用 `g5510-campaign-order-edits-v1`；每项包含 `order_index`、`field`、`expected_value` 和 `value`。Python 部分提供 `from_logical`、`to_records`、`with_edits` 和 `to_logical`。回写以同一完整原逻辑存档为基线，仅重写 CE00 与存档校验和。
