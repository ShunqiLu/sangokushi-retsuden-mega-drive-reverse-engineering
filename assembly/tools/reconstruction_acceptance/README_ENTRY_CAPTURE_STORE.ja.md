# 入口キャプチャーの保存

[简体中文](README_ENTRY_CAPTURE_STORE.md) · [繁體中文](README_ENTRY_CAPTURE_STORE.zh-TW.md) · **日本語** · [English](README_ENTRY_CAPTURE_STORE.en.md)

ストアは呼び出し側からメタデータと RAM を受け取ります。各レコードを固有の短い ID で識別し、`input.json` と `input.ram` に書き出します。件数、ファイルサイズ、JSON サイズ、ディスク空き容量の制限は呼び出し側で指定し、記録終了後にストアを閉じます。出力先は呼び出し側が選んだ新規ビルドサブディレクトリです。
