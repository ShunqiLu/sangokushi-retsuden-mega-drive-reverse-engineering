# 當前行軍隊伍

[简体中文](README_CAMPAIGN_PACKETS.md) · **繁體中文** · [日本語](README_CAMPAIGN_PACKETS.ja.md) · [English](README_CAMPAIGN_PACKETS.en.md)

[`campaign_packets.py`](campaign_packets.py) 將邏輯存檔的 RAM9000 可變記錄表示為座標、勢力、攜帶資源與武將名單。當前檢視格式為 `g5510-campaign-packets-v2`。

| 欄位 | 儲存寬度與用途 |
| --- | --- |
| `map_x` | 7 位，畫面橫向。 |
| `map_y` | 7 位，畫面縱向。 |
| `force_index_code` | 4 位勢力碼。 |
| `gold_saved_code` | 18 位攜帶金錢碼。 |
| `rice_saved_code` | 20 位攜帶米碼。 |
| `officer_ids` | 保持順序的 BYTE 武將名單。 |

`storage` 記錄原位流位置、編碼長度及各隊伍的成員數。`source.logical_hex` 提供完整原邏輯基線。成員數由名單派生，回寫保持已有記錄、順序和成員數；讀檔程式重新計算移動引數。

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli packets-export --project-root . --source input.srm --output build/packets.json
python -B -X utf8 -m tools.save_data.campaign_cli packets-edit --project-root . --source build/packets.json --edits packet-edits.json --output build/packets-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli packets-import --project-root . --source build/packets-edited.json --original-logical input.srm --output build/packets-edited.srm
```

v2 編輯檔案格式為 `g5510-campaign-packet-edits-v2`。每項含 `packet_index`、`field`、`expected_value`、`value`；替換名單時使用同長度完整列表。v1 文件使用同版本編輯格式與原欄位對映。Python 提供 `from_logical`、`to_records`、`with_edits`、`to_logical`。隊伍幾何調整使用[底層存檔工具](README.zh-TW.md)的可變流選項。
