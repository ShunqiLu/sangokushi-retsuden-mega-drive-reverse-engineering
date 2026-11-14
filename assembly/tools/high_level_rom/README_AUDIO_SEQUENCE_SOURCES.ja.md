# 音声シーケンス

[简体中文](README_AUDIO_SEQUENCE_SOURCES.md) · [繁體中文](README_AUDIO_SEQUENCE_SOURCES.zh-TW.md) · **日本語** · [English](README_AUDIO_SEQUENCE_SOURCES.en.md)

`resources/audio/audio_build.json` には楽曲、効果音、音色、シーケンスの構成要素を登録します。値は `assets/audio/` にあります。名前付きビューは対応するコマンドのフィールド名と制約を示します。共有楽譜のビューは同じイベントを指すため、共有音符の変更には[共有イベントエディター](README_AUDIO_SEQUENCE_EDITOR.ja.md)を使います。

`$resources` は `resources/` と `assets/` を含むローカル素材ルートです。アセンブリ版のルートで実行します。外部ファイルを参照する場合、`--source-root` にローカル素材ルートを指定します。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.audio_sequence_sources export --source "$resources/resources/audio/audio_build.json" --source-root $resources --project-root . --output build/audio-sequence.json
```

`edit` サブコマンドに名前付きファイルと `--edits` を指定します。`import` は名前付きファイルを構造化形式に戻します。引数は `--help` で確認できます。
