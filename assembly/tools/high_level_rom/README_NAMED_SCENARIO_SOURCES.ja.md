# シナリオの初期値

[简体中文](README_NAMED_SCENARIO_SOURCES.md) · [繁體中文](README_NAMED_SCENARIO_SOURCES.zh-TW.md) · **日本語** · [English](README_NAMED_SCENARIO_SOURCES.en.md)

`resources/data/scenario_build.json` は 3 つのシナリオの都市、勢力、武将、初期装備を保持します。名前付きビューでは金、兵糧、兵力、能力、所属、座標などを確認できます。アドレスのキーは元の範囲と幅を維持します。進行状況は[セーブ編集](../save_data/README.ja.md)を参照してください。

`$resources` は `resources/` と `assets/` を含むローカル素材ルートです。アセンブリ版のルートで実行します。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.scenario_sources edit --source "$resources/resources/data/scenario_build.json" --edits ./scenario-edits.json --project-root . --output build/scenario.json
```

`edit` は名前付きシナリオを読み込みます。元の装備データ 3 バイトは `edit-equipment --edits` でフィールド番号ごとに扱えます。`export` は従来の構造化形式から名前付きビューに、`import` は従来の形式に変換します。毎回新しいファイルに出力し、確認してからローカル素材に戻します。

`edit` は配列を受け取り、各編集に `scenario_id`、`group`、`record_id`、`field`、`expected_value`、`value` を指定します。都市資源は下位ワードを書き換え、上位ワードを維持します。
