# 入口キャプチャーの保存

[简体中文](README_ENTRY_CAPTURE_STORE.md) · [繁體中文](README_ENTRY_CAPTURE_STORE.zh-TW.md) · **日本語** · [English](README_ENTRY_CAPTURE_STORE.en.md)

[`EntryCaptureStore`](entry_capture_store.py) は指定した新規ディレクトリに入口時点の状態を保存します。コンストラクターには件数、総バイト数、レコードごとのメタデータ、予約領域の上限を渡します。各レコードの保存先は固有です。

| メソッド | 保存内容 |
| --- | --- |
| `write_case` | 入口のメタデータと元の RAM バイト列。 |
| `write_vdp_state` | VDP 状態を含む入口レコード。 |
| `write_readonly_source` | 同じセッションの読み取り専用データとメタデータ。 |
| `close(outcome)` | 保存した結果と容量上限を記した `capture-receipt.json` を書き出します。 |

元の入口、役割、取得元、記録位置をメタデータに残します。キャプチャーの容量を使い切ると書き込みを止め、アプリは自身の実行リソースで処理を続けます。
