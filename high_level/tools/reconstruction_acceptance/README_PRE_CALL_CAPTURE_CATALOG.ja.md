# 元の呼び出しのカタログ

[简体中文](README_PRE_CALL_CAPTURE_CATALOG.md) · [繁體中文](README_PRE_CALL_CAPTURE_CATALOG.zh-TW.md) · **日本語** · [English](README_PRE_CALL_CAPTURE_CATALOG.en.md)

[`prepare_pre_call_index`](pre_call_capture_catalog.py) は指定の入口一覧と特定可能な元の呼び出しから `PreparedPreCallIndex` を生成します。親呼び出し、ヘルパー、入口別名、ソース入口参照を区別し、対応するシンボル、呼び出し、復帰先の関係を保持します。

`SourceEntryReference` は現在のソース入口を示し、`PreCallGap` は根拠が不足していることを示します。実行時の記録には実際の状態と一致するカタログ項目を使います。形式と設定は[入口キャプチャー](../reconstructed_game/README_ENTRY_CAPTURE.ja.md)を参照してください。
