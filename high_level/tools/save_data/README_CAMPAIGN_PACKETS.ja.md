# 現在の行軍部隊

[简体中文](README_CAMPAIGN_PACKETS.md) · [繁體中文](README_CAMPAIGN_PACKETS.zh-TW.md) · **日本語** · [English](README_CAMPAIGN_PACKETS.en.md)

[`campaign_packets.py`](campaign_packets.py) は論理セーブの RAM9000 可変長レコードを、座標、勢力、携行資源、武将名簿で表します。現在のビューの形式は `g5510-campaign-packets-v2` です。

| フィールド | 保存幅と用途 |
| --- | --- |
| `map_x` | 7 ビット、画面の横方向。 |
| `map_y` | 7 ビット、画面の縦方向。 |
| `force_index_code` | 4 ビットの勢力コード。 |
| `gold_saved_code` | 18 ビットの携行金コード。 |
| `rice_saved_code` | 20 ビットの携行米コード。 |
| `officer_ids` | 順序付きの BYTE 武将名簿。 |

`storage` は元のビット位置、符号化長、各部隊の人数を記録します。`source.logical_hex` は元の完全な論理セーブを供給します。人数は名簿から求め、書き出し時は既存レコードと順序、人数を維持します。ゲームは読み込み時に移動パラメーターを再計算します。

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli packets-export --project-root . --source input.srm --output build/packets.json
python -B -X utf8 -m tools.save_data.campaign_cli packets-edit --project-root . --source build/packets.json --edits packet-edits.json --output build/packets-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli packets-import --project-root . --source build/packets-edited.json --original-logical input.srm --output build/packets-edited.srm
```

v2 の編集形式は `g5510-campaign-packet-edits-v2` です。各項目に `packet_index`、`field`、`expected_value`、`value` が入ります。名簿を差し替えるときは同じ長さのリスト全体を渡します。v1 には対応する編集形式と元のフィールド対応を使います。Python のインターフェースは `from_logical`、`to_records`、`with_edits`、`to_logical` です。部隊レコードの構成を変える場合は[低レベルのセーブツール](README.ja.md)の可変ストリームオプションを使います。
