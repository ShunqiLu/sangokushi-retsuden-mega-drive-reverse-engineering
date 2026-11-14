# 当前行军队伍

[`campaign_packets.py`](campaign_packets.py) 将逻辑存档的 RAM9000 可变记录表示为坐标、势力、携带资源与武将名单。当前视图格式为 `g5510-campaign-packets-v2`。

| 字段 | 保存宽度与用途 |
| --- | --- |
| `map_x` | 7 位，画面横向。 |
| `map_y` | 7 位，画面纵向。 |
| `force_index_code` | 4 位势力码。 |
| `gold_saved_code` | 18 位携带金钱码。 |
| `rice_saved_code` | 20 位携带米码。 |
| `officer_ids` | 保持顺序的 BYTE 武将名单。 |

`storage` 记录原位流位置、编码长度及各队伍的成员数。`source.logical_hex` 提供完整原逻辑基线。成员数由名单派生，回写保持已有记录、顺序和成员数；读档程序重新计算移动参数。

```powershell
python -B -X utf8 -m tools.save_data.campaign_cli packets-export --project-root . --source input.srm --output build/packets.json
python -B -X utf8 -m tools.save_data.campaign_cli packets-edit --project-root . --source build/packets.json --edits packet-edits.json --output build/packets-edited.json
python -B -X utf8 -m tools.save_data.campaign_cli packets-import --project-root . --source build/packets-edited.json --original-logical input.srm --output build/packets-edited.srm
```

v2 编辑文件格式为 `g5510-campaign-packet-edits-v2`。每项含 `packet_index`、`field`、`expected_value`、`value`；替换名单时使用同长度完整列表。v1 文档使用同版本编辑格式与原字段映射。Python 提供 `from_logical`、`to_records`、`with_edits`、`to_logical`。队伍几何调整使用[底层存档工具](README.md)的可变流选项。
