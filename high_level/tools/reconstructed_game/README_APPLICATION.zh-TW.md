# 遊戲應用介面

[简体中文](README_APPLICATION.md) · **繁體中文** · [日本語](README_APPLICATION.ja.md) · [English](README_APPLICATION.en.md)

[`GameApplication`](application.py) 持有同一 Scene、裝置、場景續接和存檔介質。視窗和[控制檯](README_CONSOLE.zh-TW.md)以同一個應用 API 提供物理按鍵和有限事件。

完整 [`frontend.frame_plan`](README_FRAME_PLAN.zh-TW.md) 將裝置事件、IRQ 和音訊推進組織成一幀。執行邊界保留最後的實際場景。`export_save` 匯出當前 8192 位元組介質；視窗截圖由當前視訊記憶體產生。

`pcm_output` 選擇 `discard`、`wav` 或 Windows [`speakers`](README_SPEAKERS.zh-TW.md)。WAV 儲存獨立的 FM、PSG 輸出；兩種裝置按各自的原取樣格式和配置的容量產生樣本。執行配置和建置輸入見[本地配置](README_LOCAL_CONFIG.zh-TW.md)。
