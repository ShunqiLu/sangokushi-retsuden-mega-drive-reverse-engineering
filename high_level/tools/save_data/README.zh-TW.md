# SRAM 與存檔工具

[简体中文](README.md) · **繁體中文** · [日本語](README.ja.md) · [English](README.en.md)

本目錄提供對邏輯 SRAM 的檢視、解包、編輯與回寫。G-5510 的儲存區使用奇地址 `0x200001–0x203FFF`，邏輯介質為 8192 位元組；工具也識別逐位元組重複為兩份的 16 KiB MAME 容器。

```powershell
python tools/save_data/save_format.py inspect input.srm
python tools/save_data/save_format.py extract input.srm save-fields
python tools/save_data/save_format.py import save-fields edited.srm
```

解包核對 `SEGA` 簽名和原加法校驗和，匯出佈局、欄位及儲存介質基線。回寫使用新檔案，保留容器形狀、未知位元組和欄位位寬，重新計算原校驗和。`--allow-variable-resize` 顯式允許改變隊伍位流的編碼長度，並將隨後的空餘校驗區填為 `FF`。

## 當前遊戲的邏輯檢視

- [城市、武將與勢力固定段](README_NAMED_CAMPAIGN.zh-TW.md)。
- [行軍隊伍、座標和攜帶資源](README_CAMPAIGN_PACKETS.zh-TW.md)。
- [CE00 運輸命令](README_CAMPAIGN_ORDERS.zh-TW.md)。

這些編輯模式使用有效的 8192 位元組邏輯基線，並生成新的候選檔案。桌面應用的 `export_save` 匯出當前 SRAM 內容；簽名和校驗和由存檔工具檢查。隨後在[本地執行配置](../reconstructed_game/README_LOCAL_CONFIG.zh-TW.md)指定所需介質。初始劇本另由[劇本資料工具](../high_level_rom/README_NAMED_SCENARIO_SOURCES.zh-TW.md)管理。
