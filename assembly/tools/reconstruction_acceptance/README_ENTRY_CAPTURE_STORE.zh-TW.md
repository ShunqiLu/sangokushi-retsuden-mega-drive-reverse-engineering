# 入口輸入儲存

[简体中文](README_ENTRY_CAPTURE_STORE.md) · **繁體中文** · [日本語](README_ENTRY_CAPTURE_STORE.ja.md) · [English](README_ENTRY_CAPTURE_STORE.en.md)

入口儲存器接收呼叫方採集的後設資料和 RAM。每條記錄使用獨立的短標識，寫入 `input.json` 和 `input.ram`。呼叫方設定條數、檔案大小、JSON 大小和磁碟餘量；採集結束後統一關閉儲存器。結果儲存在呼叫方選定的新建置子目錄。
