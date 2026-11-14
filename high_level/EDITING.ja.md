# 編集ガイド

[简体中文](EDITING.md) · [繁體中文](EDITING.zh-TW.md) · **日本語** · [English](EDITING.en.md)

ゲームのルールはこのソースツリーにあります。グラフィック、音声、シナリオのデータは `--resource-root` で指定する[素材ルート](ASSETS.ja.md)にあります。

| 内容 | 編集箇所 |
| --- | --- |
| 内政、行軍、戦闘、AI、シーンのルール | `tools/high_level_*/business*.py` の機能別関数と、対応する `compiler*.py` および `target.py` |
| 都市、武将、勢力の初期値とシナリオ内の装備 | [名前付きシナリオデータ](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.ja.md) |
| AI の命令比較しきい値 | [48 組の WORD しきい値](tools/high_level_rom/README_AI_POLICY_SOURCES.ja.md) |
| AI 候補の適格条件 | [14 × 14 BYTE の適格条件表](tools/high_level_rom/README_AI_SELECTION_SOURCES.ja.md) |
| 中国語の台詞、武将名、都市名 | [可読テキスト形式](tools/high_level_rom/README_READABLE_TEXT.ja.md) |
| 戦闘背景 | [マップのマスと属性](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.ja.md)、[インデックス付きタイル PNG](tools/high_level_rom/README_BATTLE_TILE_SHEET.ja.md) |
| 武将の顔グラフィック | [名前、配置、パレット、共有タイル](PORTRAITS.ja.md) |
| 楽曲、効果音、音色 | [名前付き楽譜とイベントソース](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.ja.md)、[共有イベントエディター](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.ja.md) |
| 現在のセーブデータ | [都市・武将・勢力の固定レコード](tools/save_data/README_NAMED_CAMPAIGN.ja.md)、[行軍部隊](tools/save_data/README_CAMPAIGN_PACKETS.ja.md)、[輸送命令](tools/save_data/README_CAMPAIGN_ORDERS.ja.md) |

## ゲームルールとビルド

ルール関数はゲームのルールと状態変化を扱います。`contexts*.py` は入力とインターフェースを、コンパイラーとターゲット定義は命令、アドレス、レジスター、固定領域を扱います。編集には各機能のコンパイラーが対応する Python 文と状態インターフェースを使ってください。境界的な挙動は[原作の挙動](docs/ORIGINAL_GAME_BUGS.ja.md)にまとめています。

[イメージのビルド](tools/high_level_rom/README_BUILD.ja.md)は、編集した素材を通常の登録経路から読み込みます。再利用する変更はルールのソースかローカル素材に保存してください。

## 一括編集

編集 API は入力一式と、対象レコード・旧値・新値を明示した変更のリストを受け取り、変更候補を別に返します。エンコーダーはフィールド幅、別名参照、ファイルの構成を維持します。

```python
from tools.high_level_rom.scenario_sources import with_scenario_fields

scenario = source["scenarios"][0]
city = next(row for row in scenario["cities"] if row["id"] == 3)
edited = with_scenario_fields(source, [{
    "scenario_id": scenario["id"],
    "group": "cities",
    "record_id": city["id"],
    "field": "gold",
    "expected_value": city["gold"],
    "value": 12000,
}])
```

シナリオの編集対象は物理レコード ID で、装備はソースの BYTE インデックスで指定します。都市の開発、民生、城防は下位 WORD にあり、エンコーダーは同じスロットの上位 WORD を維持します。テキストの編集では固定文字スロットと制御 WORD を、音声の編集では全体のイベントビューで元のイベントを特定し、命令の種類とサイズを保ちます。

## セーブデータ

[セーブツール](tools/save_data/README.ja.md)は、明示的に指定した 8 KiB の論理セーブを基準にします。固定フィールド、行軍部隊、輸送命令は個別のビューで編集し、書き出し先は新規ファイルです。複数の編集をつなぐ場合は、書き出した候補を次の基準にします。各ビューは元のビット幅、チェックサム方式、未使用データを保ちます。
