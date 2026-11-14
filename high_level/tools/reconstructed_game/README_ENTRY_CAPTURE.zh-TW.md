# 可選入口採集

[简体中文](README_ENTRY_CAPTURE.md) · **繁體中文** · [日本語](README_ENTRY_CAPTURE.ja.md) · [English](README_ENTRY_CAPTURE.en.md)

`--capture-entries` 啟用同一桌面會話中的源入口採集。採集配置與遊戲配置分開。入口資料來自真實呼叫幀、物理返回槽、儲存區與呼叫上下文；採集器以顯式的檔案數和空間容量儲存記錄。

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --capture-entries entry-capture.json
```

| 欄位 | 作用 |
| --- | --- |
| `format` | 選擇採集配置版本。 |
| `batch` | 提供入口批次的 JSON。 |
| `output` | 父目錄存在的全新 `build/` 子目錄。 |
| `tool_id` | 0–5 範圍內實際可用的 Python 監視工具 ID。 |
| `max_cases`、`max_captures_per_entry` | 總記錄與單入口記錄上限。 |
| `max_total_bytes`、`max_case_json_bytes`、`min_free_bytes` | 總位元組、單個 JSON 上限及保留空間。 |

基礎格式為 `g5510-entry-capture-config-v1`；v2 透過 `audio` 宣告 Z80 入口，v3 透過 `pre_call` 宣告呼叫前採集，v4 的 `pre_call` 包含實際布林值 `enabled` 和 `include_current_source_calls`。`batch` 和 `output` 的相對路徑按採集配置檔案位置解析。

[`entry_capture_config.py`](entry_capture_config.py) 管理配置和啟停；[採集儲存](../reconstruction_acceptance/README_ENTRY_CAPTURE_STORE.zh-TW.md)描述檔案格式和容量。[M68K](../reconstruction_acceptance/README_M68K_ENTRY_CAPTURE.zh-TW.md)、[Z80](../reconstruction_acceptance/README_Z80_ENTRY_CAPTURE.zh-TW.md)和[呼叫前採集](../reconstruction_acceptance/README_M68K_PRE_CALL_CAPTURE.zh-TW.md)各有入口合同。
