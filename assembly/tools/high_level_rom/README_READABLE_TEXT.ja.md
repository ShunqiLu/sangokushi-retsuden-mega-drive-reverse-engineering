# 台詞と名前の編集

[简体中文](README_READABLE_TEXT.md) · [繁體中文](README_READABLE_TEXT.zh-TW.md) · **日本語** · [English](README_READABLE_TEXT.en.md)

`resources/data/dialogue_text.json` は台詞、武将名、都市名を保持します。名前付き形式は終端制御ワード、元の文字数、通常の文字で区別できない場合の正確なエスケープを保ちます。編集では同じレコード ID と文字数上限を使います。

`$resources` は `resources/` と `assets/` を含むローカル素材ルートです。アセンブリ版のルートで実行します。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.readable_text edit --source "$resources/resources/data/dialogue_text.json" --edits ./text-edits.json --project-root . --output build/readable-text.json
```

`edit --edits` はレコード ID と旧値を名前付き素材と照合します。`import` は名前付き形式を文字コード形式に戻します。従来の文字コード形式と手作業で作成した 2 種類の字形表を `export --glyph-sources` に渡すと、名前付きビューに変換できます。

編集ファイルの `format` は `g5510-main-text-record-edits-v1` です。`edits` の各要素に `collection`、`id`、`expected_text`、`text` を指定します。コレクション名は `records`、`officer_names`、`city_names` のいずれかです。
