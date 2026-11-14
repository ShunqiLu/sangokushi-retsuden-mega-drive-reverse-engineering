# 武将の顔グラフィック

[简体中文](PORTRAITS.md) · [繁體中文](PORTRAITS.zh-TW.md) · **日本語** · [English](PORTRAITS.en.md)

素材パックの `OFFICER_PORTRAITS.json` で顔グラフィックを検索できます。`officers` 内を `name.text` または `officer_record_id` で検索してください。不明な字形は元の値を保つエスケープで表します。

| フィールド | 内容 |
| --- | --- |
| `portrait.layout_file` | ピクセルタイルと顔グラフィックのマスを定義する JSON |
| `portrait.palette.file` | パレットの JSON |
| `tile_groups[].tile_ref` | `shared_tiles` にある共有 PNG への参照 |

名前は `resources/data/dialogue_text.json`、顔グラフィックは `resources/images/portrait_graphics.json`、武将レコードは `resources/data/scenario_build.json` から取得します。共有 PNG を編集すると、参照するすべての顔グラフィックに反映されます。人物を特定できていない項目は `unknown` と表示します。

検索と生成のコマンドは[顔グラフィック索引ツール](tools/high_level_rom/README_PORTRAIT_CATALOG.ja.md)を参照してください。
