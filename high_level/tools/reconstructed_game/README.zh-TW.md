# 桌面遊戲應用

[简体中文](README.md) · **繁體中文** · [日本語](README.ja.md) · [English](README.en.md)

[`tools.reconstructed_game`](__main__.py) 使用同一遊戲應用推進場景、輸入、畫面、音訊和存檔。圖形視窗以 Tk 展示實際畫面；控制檯透過 JSON 行協議提供同一個可續接會話。

## 執行

[本地配置說明](README_LOCAL_CONFIG.zh-TW.md)列出原始碼目錄、素材、程式資料、音訊晶片庫、裝置供應和存檔。使用準備好的配置啟動：

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend window
```

`--frontend console` 啟用[控制檯](README_CONSOLE.zh-TW.md)並要求完整幀計劃。`--session-output` 指向配置根的 `build/` 內新的會話路徑。

## 執行配置

- [應用介面與 PCM](README_APPLICATION.zh-TW.md)、[可選揚聲器](README_SPEAKERS.zh-TW.md)。
- [完整幀計劃](README_FRAME_PLAN.zh-TW.md)、[硬體輸入](README_HARDWARE_INPUTS.zh-TW.md)、[有限輸入配置](README_HARDWARE_PROFILE.zh-TW.md)。
- [節目與場景的有序復位](README_ORDERED_RESTARTS.zh-TW.md)、[冷／暖路徑](README_ORDERED_COLD_PLAN.zh-TW.md)。
- [可選入口採集](README_ENTRY_CAPTURE.zh-TW.md)。

每個階段消費配置宣告的真實裝置事件與數量。應用保留同一物理幀和存檔介質；裝置供應耗盡時返回對應的執行邊界。
