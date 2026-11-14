# 武将の顔グラフィック編集

[简体中文](PORTRAITS.md) · [繁體中文](PORTRAITS.zh-TW.md) · **日本語** · [English](PORTRAITS.en.md)

[顔グラフィック索引ツール](tools/high_level_rom/README_PORTRAIT_CATALOG.ja.md)は、テキスト、画像、シナリオから武将の索引を作ります。`name.text` または `officer_record_id` で検索し、レイアウト、パレット、タイルの参照をたどって素材を編集します。共有タイルの変更は複数の武将に反映されます。

素材ルート内のファイル：

- `resources/data/dialogue_text.json`：武将名。
- `resources/images/portrait_graphics.json`：顔グラフィックの配置、パレット、外部 PNG の参照。
- `resources/data/scenario_build.json`：シナリオと武将レコード。
