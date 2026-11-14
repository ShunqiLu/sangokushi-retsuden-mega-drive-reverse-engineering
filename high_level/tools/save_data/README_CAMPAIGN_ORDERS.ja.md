# CE00 輸送命令

[简体中文](README_CAMPAIGN_ORDERS.md) · [繁體中文](README_CAMPAIGN_ORDERS.zh-TW.md) · **日本語** · [English](README_CAMPAIGN_ORDERS.en.md)

[`campaign_orders.py`](campaign_orders.py) は現在の論理セーブのオフセット `0x1678` から 110 バイトを読み、各 22 ビットの CE00 レコード 40 件に展開します。実行時コードは輸送種別、経路、到着先の資源インデックスにこの値を使います。

| フィールド | 幅 | 用途 |
| --- | --- | --- |
| `transport_kind_code` | 2 ビット | 経路と到着報酬の選択に使う種別コード。 |
| `route_x` | 7 ビット | 経路の第 1 軸の座標コード。 |
| `route_y` | 7 ビット | 経路の第 2 軸の座標コード。 |
| `destination_city_code` | 6 ビット | 到着先の都市インデックスコード。 |

`g5510-campaign-orders-v1` は `format`、`source`、`storage`、`orders` を含み、レコードは 0 始まりの `record_index` 順です。輸送フラグと資源値は実行中に計算され、保存形式は全 40 スロットと空きスロットの残値を保持します。

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli orders-export --project-root . --source input.srm --output build/orders.json
python -B -X utf8 -m tools.save_data.campaign_cli orders-edit --project-root . --source build/orders.json --edits order-edits.json --output build/orders-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli orders-import --project-root . --source build/orders-edited.json --original-logical input.srm --output build/orders-edited.srm
```

編集ファイルの形式は `g5510-campaign-order-edits-v1` です。各項目には `order_index`、`field`、`expected_value`、`value` が含まれます。Python のインターフェースは `from_logical`、`to_records`、`with_edits`、`to_logical` です。同じ元の論理セーブ全体を基準とし、CE00 とチェックサムだけを書き換えます。
