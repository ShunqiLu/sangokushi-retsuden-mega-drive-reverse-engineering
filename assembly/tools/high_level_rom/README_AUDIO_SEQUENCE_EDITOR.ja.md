# 楽譜の共有イベント編集

[简体中文](README_AUDIO_SEQUENCE_EDITOR.md) · [繁體中文](README_AUDIO_SEQUENCE_EDITOR.zh-TW.md) · **日本語** · [English](README_AUDIO_SEQUENCE_EDITOR.en.md)

楽譜の共有イベントはローカル実行コピーの `assets/audio/shared/stateful_event_views.json` にあります。編集ごとにビュー `view_id`、フィールド `field`、旧値 `expected`、新値 `value` を指定します。[編集例](examples/audio_sequence_field_edits.example.json)でファイルの構造を確認できます。

ソースとローカル素材を含むコピーのルートで実行します。

```powershell
python -B -m tools.high_level_rom.audio_sequence_asset_editor --edits ./sequence-edits.json --output ./stateful_event_views.json
```

出力には変更後の素材と、変更位置および共有ビューの一覧が含まれます。確認後、ローカルコピーの対応するパスに素材を戻し、[ビルド手順](../../README.ja.md)に従ってカートリッジに組み込みます。
