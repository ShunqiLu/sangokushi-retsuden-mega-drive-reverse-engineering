# 名前付きシナリオの初期値

[简体中文](README_NAMED_SCENARIO_SOURCES.md) · [繁體中文](README_NAMED_SCENARIO_SOURCES.zh-TW.md) · **日本語** · [English](README_NAMED_SCENARIO_SOURCES.en.md)

[`scenario_sources.py`](scenario_sources.py) は都市、武将、勢力の型付きシナリオ列を `g5510-owned-named-scenario-source-v1` に対応付けます。`metadata`、`directory_targets`、物理 `scenarios` 3 件を保持し、物理レコードを `scenario_0`、`scenario_1`、`scenario_2` で識別します。実行時記述子とディレクトリの別名参照も、それぞれ元の参照先を保ちます。

| グループ | フィールドと物理値 |
| --- | --- |
| 都市資源 | `gold` と `rice` は 32 ビット値。`development`、`welfare`、`defense` は下位 WORD を編集し、上位 WORD を保持します。 |
| 都市管理 | `force_index_byte`、`representative_officer_word`、`income_base_long`、`income_split_long`、`income_rate_long`、`assigned_officer_tally_long`、`troop_total_long`。 |
| 勢力 | `representative_officer_word` と `relationship_bits_word`。関係行はそれぞれの方向を保ちます。 |
| 武将の基本情報 | `intelligence_word`、`virtue_byte`、`troop_capacity_base_word`、`troop_count_long`、`assigned_city_byte`。 |
| 武将の成長と状態 | `readiness_capacity_word`、`readiness_current_word`、`combat_rating_word`、`intelligence_growth_score_word`、`combat_growth_score_word`、`education_rating_byte`、`movement_factor_byte`、`training_percent_byte`、`growth_threshold_tier_byte`、`class_status_flags_byte`。 |

BE00、C000 は成長に関する 2 つの WORD に対応し、原作の周回、除数、上限はゲームルールが扱います。B000／B200 は同じ回復可能な状態の容量と現在値です。C400 は候補範囲と移動距離の計算に使います。その他の位置や未命名の値は元のアドレスで `unresolved_fields` に保存し、幅、番兵値、不明なビットを保ちます。

## 一括編集

`with_scenario_fields(source, edits)` は `scenario_id`、`group`、`record_id`、`field`、`expected_value`、`value` を使います。都市 ID は 1～40、勢力は 0～15、武将は 0～255 です。各フィールドを元の BYTE、WORD、LONG の幅で検証します。都市の上下に分かれた 3 フィールドでは下位 WORD の旧値と新値だけを指定します。戻り値は独立した名前付きファイルです。

既存の名前付きファイルは `edit` に直接渡せます。例の `export` は型付きソースを含む `$typedResources` から名前付き形式を書き出します。既存の `build/` の下に新規ファイルを指定します。

```powershell
python -B -X utf8 -m tools.high_level_rom.scenario_sources export --project-root . --source "$typedResources/resources/data/scenario_build.json" --output build/scenario.named.json
python -B -X utf8 -m tools.high_level_rom.scenario_sources edit --project-root . --source build/scenario.named.json --edits scenario-edits.json --output build/scenario.edited.json
```

`to_named` と `from_named` はデータ表現を変換し、`import` は名前付きファイルを元の型付き形式に戻します。登録素材 ID は `scenario_build` です。

## 初期装備の BYTE

`unresolved_fields.ram_ea88` は `source_byte0`、`source_byte1`、`source_byte2` で、実行時に 1、0、2 の順で読みます。`with_equipment_source_bytes` または `edit-equipment --edits` には `scenario_id`、`officer_id`、`source_byte_index`、`expected_value`、`value` を使います。BYTE は 0～255 で、他のスロットやシナリオの別名参照は元の関係を保ちます。
