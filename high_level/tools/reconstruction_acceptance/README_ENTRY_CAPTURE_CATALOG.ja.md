# 入口キャプチャーのカタログ

[简体中文](README_ENTRY_CAPTURE_CATALOG.md) · [繁體中文](README_ENTRY_CAPTURE_CATALOG.zh-TW.md) · **日本語** · [English](README_ENTRY_CAPTURE_CATALOG.en.md)

[`load_capture_targets(batch, project_root)`](entry_capture_catalog.py) は `g5510-concentrated-explicit-input-batch-v1` 形式の文書から固定の `CaptureTarget` タプルを返します。対象を元の入口アドレス、Python モジュールと関数、フレーム型、呼び出し引数で現在の宣言に対応付けます。

読み込み時に取得元、正確な識別子、入口の同一性を確認します。[入口モニター](README_ENTRY_MONITOR.ja.md)が実際の呼び出しで状態を記録します。
