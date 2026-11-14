# 楽譜の共有イベント編集

[简体中文](README_AUDIO_SEQUENCE_EDITOR.md) · [繁體中文](README_AUDIO_SEQUENCE_EDITOR.zh-TW.md) · **日本語** · [English](README_AUDIO_SEQUENCE_EDITOR.en.md)

ツールはローカル実行ディレクトリの `resources/audio/audio_build.json` と `assets/audio/` を読み、現在の版の登録とエンコード規則に照らして編集を確認します。形式は[フィールド編集例](examples/audio_sequence_field_edits.example.json)を参照してください。`view_id` と `expected` は現在の `assets/audio/shared/stateful_event_views.json` から取得します。

```powershell
New-Item -ItemType Directory -Path build/audio-sequence-edit
python -B -X utf8 -m tools.high_level_rom.audio_sequence_asset_editor --edits audio-edits.json --output build/audio-sequence-edit/stateful_event_views.json
```

編集フィールドは `note`（`0x80..0xDF`）、`fm_attenuation.attenuation_byte`、`fine_detune.fine_detune_byte`、`pan.pan_byte` です。単位は元のドライバーのバイト単位とし、コマンド幅、音の長さ、制御フローは元の構造を保ちます。

出力には編集後の候補イベントファイルと対応する `stateful_event_views.edit-receipt.json` が含まれます。変更バイトと、そのバイトを読み出すか先読みするビューを列挙します。素材の同名ファイルを候補に差し替えると[通常のビルド](README_BUILD.ja.md)に組み込めます。
