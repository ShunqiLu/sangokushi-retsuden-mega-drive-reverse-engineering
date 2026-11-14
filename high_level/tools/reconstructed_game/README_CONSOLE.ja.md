# 対話コンソール

[简体中文](README_CONSOLE.md) · [繁體中文](README_CONSOLE.zh-TW.md) · **日本語** · [English](README_CONSOLE.en.md)

コンソールはデスクトップ版と同じアプリを使います。設定に完全な `frontend.frame_plan` を用意し、`--frontend console` で起動します。

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend console
```

## JSON Lines プロトコル

標準入力は 1 行につき 1 つの UTF-8 JSON オブジェクトで、改行を含め 65,536 バイトまでです。標準出力の各応答も 1 つの JSON オブジェクトです。`status` は `ready`、`ok`、`protocol_error`、`boundary`、`closed` のいずれかです。

`ready` は `declared_ports`、`live_pad_ports`、`fixed_pad_snapshots` を指定します。ポート番号は 0 始まりです。ボタンは `up`、`down`、`left`、`right`、`a`、`b`、`c`、`start` です。各 `advance` は宣言済みの全ポートのボタン状態を指定します。空配列はそのポートの全ボタンを離した状態です。

```jsonl
{"command":"advance","frames":120,"pads":[{"port":0,"buttons":[]}]}
{"command":"advance","frames":1,"pads":[{"port":0,"buttons":["start"]}]}
{"command":"advance","frames":4,"pads":[{"port":0,"buttons":[]}]}
{"command":"capture","file":"after-start.png"}
{"command":"observe"}
{"command":"observe_palette"}
{"command":"export_save","file":"current-sram.srm"}
{"command":"close"}
```

| コマンド | 結果 |
| --- | --- |
| `advance` | ボタン状態一式を使って指定フレーム数だけ進めます。 |
| `capture` | 現在の描画を新規 PNG に保存します。 |
| `observe` | 現在の待機、実行カウンター、指定メモリフィールドを読み出します。 |
| `observe_palette` | 実際の CRAM、FB00／FB80 のパレット作業領域、VDP レジスターを読み出します。 |
| `export_save` | 現在の 8192 バイトの SRAM を新規ファイルに書き出します。 |
| `extend_frames` | フレーム枠を使い切った後、`new_total` で合計フレーム数を増やします。 |
| `close` | 現在のゲームセッションを終了し、デバイスを解放します。 |

スクリーンショットと書き出しには診断ディレクトリ内の新規ファイル名を指定します。`extend_frames` は現在のゲーム、連続するフレーム番号、各デバイスの残り容量を維持します。Python インターフェースは `run_console(app, config, input_stream=..., output_stream=...)` です。
