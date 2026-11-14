# 顔グラフィック索引の生成

[简体中文](README_PORTRAIT_CATALOG.md) · [繁體中文](README_PORTRAIT_CATALOG.zh-TW.md) · **日本語** · [English](README_PORTRAIT_CATALOG.en.md)

[`portrait_catalog.py`](portrait_catalog.py) は読める形の武将名、シナリオレコード、顔グラフィックの配置、パレット、共有タイルを検索用の索引にまとめます。出力の `officers` は名前とレコード ID で検索でき、`shared_tiles` は共有画像ファイルを示します。画像との対応が確認済みか未確定かも保持します。

```powershell
python -B -X utf8 -m tools.high_level_rom.portrait_catalog --project-root . --names-source "$resources/resources/data/dialogue_text.json" --portrait-source "$resources/resources/images/portrait_graphics.json" --record-authority "$resources/resources/data/scenario_build.json" --source-root $resources --output build/officer-portraits.json
```

`--names-source` には[可読テキストソース](README_READABLE_TEXT.ja.md)を使い、素材ルートの名前付き台詞ファイルを直接指定できます。`--source-root` は実際の顔グラフィックファイルを解決します。新しい索引はプロジェクトの `build/` に出力します。編集箇所は[顔グラフィック編集ガイド](../../PORTRAITS.ja.md)を参照してください。
