# 入口採集檔案儲存

[简体中文](README_ENTRY_CAPTURE_STORE.md) · **繁體中文** · [日本語](README_ENTRY_CAPTURE_STORE.ja.md) · [English](README_ENTRY_CAPTURE_STORE.en.md)

[`EntryCaptureStore`](entry_capture_store.py) 在顯式的新輸出目錄儲存入口初態。構造引數給出記錄數、總位元組、單項後設資料與保留空間上限。記錄路徑使用唯一名稱。

| 方法 | 儲存內容 |
| --- | --- |
| `write_case` | 入口後設資料和原 RAM 位元組。 |
| `write_vdp_state` | 帶 VDP 狀態的入口記錄。 |
| `write_readonly_source` | 同會話的只讀資料來源及其後設資料。 |
| `close(outcome)` | 寫入 `capture-receipt.json`，描述已寫結果與預算邊界。 |

原入口、角色、來源和捕獲位置儲存在記錄後設資料中。資源容量耗盡時停止寫入採集，應用使用自身的執行資源繼續執行。
