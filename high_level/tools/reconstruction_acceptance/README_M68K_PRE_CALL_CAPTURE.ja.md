# M68K 呼び出し前のスナップショット

[简体中文](README_M68K_PRE_CALL_CAPTURE.md) · [繁體中文](README_M68K_PRE_CALL_CAPTURE.zh-TW.md) · **日本語** · [English](README_M68K_PRE_CALL_CAPTURE.en.md)

[`M68KPreCallObserver`](m68k_pre_call_capture.py) は元のヘルパー本体が実行される前の位置を特定します。元の呼び出しと復帰位置、入口の役割、実際の呼び出し本体は[呼び出しカタログ](README_PRE_CALL_CAPTURE_CATALOG.ja.md)から取得し、実行時には[ソースビュー](README_PRE_CALL_SOURCE_VIEWS.ja.md)で照合します。

レコードの形式は `g5510-actual-m68k-pre-CALL-capture-v1` です。各スナップショットには実際の親フレーム、物理スタック、RAM、各データの取得元が入ります。実際の親呼び出しと入口の別名は別々の識別子を保ちます。[キャプチャーの保存](README_ENTRY_CAPTURE_STORE.ja.md)が結果を書き出します。
