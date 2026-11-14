# 呼び出し前のソースビュー

[简体中文](README_PRE_CALL_SOURCE_VIEWS.md) · [繁體中文](README_PRE_CALL_SOURCE_VIEWS.zh-TW.md) · **日本語** · [English](README_PRE_CALL_SOURCE_VIEWS.en.md)

[`pre_call_source_views.py`](pre_call_source_views.py) は準備済みのヘルパーソースを実際の Python コードオブジェクトに対応付けます。同じ呼び出しに必要な関数全体の構造、入口の対応、実行時の識別情報を保持します。実行時のコールバックは、そのビューで呼び出し前の位置を特定します。

[元の呼び出しのカタログ](README_PRE_CALL_CAPTURE_CATALOG.ja.md)は親呼び出しと入口参照を提供し、[呼び出し前オブザーバー](README_M68K_PRE_CALL_CAPTURE.ja.md)が呼び出し位置で実際の状態を読み取ります。
