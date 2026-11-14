# 中国語の台詞・武将名・都市名

[简体中文](README_READABLE_TEXT.md) · [繁體中文](README_READABLE_TEXT.zh-TW.md) · **日本語** · [English](README_READABLE_TEXT.en.md)

[`readable_text.py`](readable_text.py) は型付きテキストを `g5510-owned-main-text-unicode-source-v1` に変換します。文字の対応表は[下位字形表](text_sources/glyphs_lower.json)と[上位字形表](text_sources/glyphs_upper.json)です。重複コード、不明な字形、通常形式と異なる制御値は、大文字 4 桁の 16 進表記 `⟦XXXX⟧` で元の値を保持します。

台詞は元の文字スロット、各制御 WORD の位置と値、末尾の復帰制御を保ちます。台詞の `0000` はグラフィック操作、`4000` は字形 0 に対応します。名前では `0000` が字形 0 に対応します。武将名は 3 WORD、都市名は 2 WORD です。

`export` は型付きテキストを含む素材ルート `$typedResources` を使います。既存の可読ファイルは `edit --source` に直接渡せます。既存の `build/` の下に新規ファイルを指定します。

```powershell
python -B -X utf8 -m tools.high_level_rom.readable_text export --project-root . --source "$typedResources/resources/data/dialogue_text.json" --glyph-sources tools/high_level_rom/text_sources/glyphs_lower.json tools/high_level_rom/text_sources/glyphs_upper.json --output build/dialogue-readable.json
python -B -X utf8 -m tools.high_level_rom.readable_text edit --project-root . --source build/dialogue-readable.json --edits text-edits.json --output build/dialogue-edited.json
```

編集ファイルは `g5510-main-text-record-edits-v1` 形式で `format` と `edits` を持ちます。各レコードを `collection` と `id` で指定し、元の `expected_text` 全体と新しい `text` を渡します。一括編集は固定 WORD 数と制御値を確認して、別のファイルを返します。Python からは `with_text_edits` を呼び出せます。`MainTextWordCodec` は文字と正確な WORD 値を変換します。
