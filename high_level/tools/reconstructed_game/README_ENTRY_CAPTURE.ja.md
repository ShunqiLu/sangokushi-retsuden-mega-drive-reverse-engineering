# 任意の入口キャプチャー

[简体中文](README_ENTRY_CAPTURE.md) · [繁體中文](README_ENTRY_CAPTURE.zh-TW.md) · **日本語** · [English](README_ENTRY_CAPTURE.en.md)

`--capture-entries` は同じデスクトップセッションのソース入口を記録します。キャプチャー設定はゲーム設定から分離されています。実際の呼び出しフレーム、物理戻りスロット、メモリ、呼び出しコンテキストを、指定のファイル件数と容量内で保存します。

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --capture-entries entry-capture.json
```

| フィールド | 用途 |
| --- | --- |
| `format` | キャプチャー設定のバージョン。 |
| `batch` | 入口リストの JSON。 |
| `output` | 親ディレクトリが既にある新規の `build/` サブディレクトリ。 |
| `tool_id` | 0～5 の範囲で利用可能な Python 監視ツール ID。 |
| `max_cases`、`max_captures_per_entry` | 全記録と入口ごとの件数上限。 |
| `max_total_bytes`、`max_case_json_bytes`、`min_free_bytes` | 総バイト数、JSON 1 件の上限、ディスク予約容量。 |

基本形式は `g5510-entry-capture-config-v1` です。v2 は `audio` で Z80 入口を、v3 は `pre_call` で呼び出し前キャプチャーを指定します。v4 の `pre_call` には真偽値 `enabled` と `include_current_source_calls` が入ります。`batch` と `output` の相対パスはキャプチャー設定ファイルの位置から解決します。

[`entry_capture_config.py`](entry_capture_config.py) は設定と開始・停止を管理します。[キャプチャーの保存](../reconstruction_acceptance/README_ENTRY_CAPTURE_STORE.ja.md)でファイル形式と容量を説明します。[M68K](../reconstruction_acceptance/README_M68K_ENTRY_CAPTURE.ja.md)、[Z80](../reconstruction_acceptance/README_Z80_ENTRY_CAPTURE.ja.md)、[呼び出し前キャプチャー](../reconstruction_acceptance/README_M68K_PRE_CALL_CAPTURE.ja.md)にそれぞれの入口仕様があります。
