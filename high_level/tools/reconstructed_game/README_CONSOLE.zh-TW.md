# 互動式控制檯

[简体中文](README_CONSOLE.md) · **繁體中文** · [日本語](README_CONSOLE.ja.md) · [English](README_CONSOLE.en.md)

控制檯使用相同的桌面遊戲應用。配置提供完整 `frontend.frame_plan`，以 `--frontend console` 啟用。

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend console
```

## JSON 行協議

stdin 每行一個 UTF-8 JSON 物件，含換行最多 65,536 位元組。stdout 的每條回覆也是一個 JSON 物件，`status` 表示 `ready`、`ok`、`protocol_error`、`boundary` 或 `closed`。

`ready` 給出 `declared_ports`、`live_pad_ports` 與 `fixed_pad_snapshots`。埠從 0 編號；按鍵為 `up`、`down`、`left`、`right`、`a`、`b`、`c` 和 `start`。每次 `advance` 提供所有宣告埠的完整電平；空陣列表示釋放該埠全部按鍵。

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

| 命令 | 結果 |
| --- | --- |
| `advance` | 按完整按鍵狀態推進明確數量的幀。 |
| `capture` | 將當前渲染寫為新的 PNG。 |
| `observe` | 讀取當前等待、執行計數及明確的記憶體欄位。 |
| `observe_palette` | 讀取實際 CRAM、FB00／FB80 調色盤工作區和 VDP 暫存器。 |
| `export_save` | 將當前真實 8192 位元組 SRAM 匯出為新檔案。 |
| `extend_frames` | 正常耗盡幀額度之後，透過 `new_total` 指定更高總幀數。 |
| `close` | 退出當前遊戲會話並釋放裝置。 |

截圖和匯出使用診斷目錄內的新檔名。`extend_frames` 保留當前遊戲、連續幀號和各裝置的剩餘供應。Python 介面為 `run_console(app, config, input_stream=..., output_stream=...)`。
