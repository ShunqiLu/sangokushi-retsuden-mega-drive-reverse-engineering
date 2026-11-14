# 人物头像

**简体中文** · [繁體中文](PORTRAITS.zh-TW.md) · [日本語](PORTRAITS.ja.md) · [English](PORTRAITS.en.md)

素材包中的 `OFFICER_PORTRAITS.json` 提供派生查找索引。在 `officers` 中按 `name.text` 或 `officer_record_id` 查找；未知字形保留精确转义。

| 字段 | 用途 |
| --- | --- |
| `portrait.layout_file` | 像素块与头像格的布局 JSON |
| `portrait.palette.file` | 调色板 JSON |
| `tile_groups[].tile_ref` | `shared_tiles` 中的共享 PNG 引用 |

姓名来自 `resources/data/dialogue_text.json`，头像来自 `resources/images/portrait_graphics.json`，武将记录来自 `resources/data/scenario_build.json`。编辑共享 PNG 会影响引用它的多个头像；身份待定的条目以 `unknown` 表示。

[头像索引工具](tools/high_level_rom/README_PORTRAIT_CATALOG.md)说明定位与生成命令。
