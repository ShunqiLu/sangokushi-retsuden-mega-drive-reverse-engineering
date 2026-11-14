# 名前付き音声シーケンス命令

[简体中文](README_AUDIO_SEQUENCE_SOURCES.md) · [繁體中文](README_AUDIO_SEQUENCE_SOURCES.zh-TW.md) · **日本語** · [English](README_AUDIO_SEQUENCE_SOURCES.en.md)

`audio_sequence_sources.py` は元の固定幅音声イベントに名前付き引数を付けます。音声ファイル全体の形式は `g5510-named-audio-sequence-commands-v1`、ビューの各要素の形式は `g5510-named-stateful-sequence-views-v1` です。物理イベントの共有と読み込み順は元の登録情報で定義します。

| 引数の種類 | 元の表現 |
| --- | --- |
| パン、微調整、減衰、キーオフ遅延 | それぞれ BYTE |
| LFO パン、相対・絶対レジスター操作 | レジスター選択と後続の BYTE |
| Timer A、Timer B | Timer A の下位・上位 BYTE と Timer B の BYTE |
| 楽器 | 選択 BYTE のビット 7 が外部コマンドの引数を決定 |
| ジャンプ、呼び出し、ループ | 元のリトルエンディアンの分岐先、BYTE のカウンター番号と回数 |
| 遅延倍率、移調、モード | 元の BYTE。2 の補数はサウンドドライバーが解釈 |
| 拡張コマンドの不明な引数 | `unknown_argument_bytes` を元の順序で保持 |

## 書き出しと編集

`export` は完全な型付きファイルまたは素材グラフから独立した名前付きファイルを作ります。素材グラフは対応する `--source-root` を供給します。既存の独立した名前付きファイルは `edit` に直接渡せます。出力には既存の `build/` の下の新規ファイルを指定します。

```powershell
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources export --source "$resources/resources/audio/audio_build.json" --source-root $resources --project-root . --output build/audio-sequences.named.json
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources edit --source build/audio-sequences.named.json --edits audio-command-edits.json --project-root . --output build/audio-sequences.edited.json
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources import --source build/audio-sequences.edited.json --project-root . --output build/audio-sequences.typed.json
```

編集形式は `g5510-named-audio-command-parameter-edits-v1` です。各 `view` には元のビューの `id`、`address`、`rom_offset`、`reader`、`raw_frequency`、`slide` が含まれます。`expected_parameters` は現在の引数オブジェクト全体、`parameters` は同じ構造の新しいオブジェクト全体です。

`with_command_parameters(document, edits)` は検証済みで重複のない編集を適用し、命令の種類、引数の構造、サイズ、物理割り当てを保ちます。`to_named` と `from_named` は表現を変換し、`tools.high_level_rom.export_media --named-audio-sequences` は外部の名前付き音声ソースを生成します。
