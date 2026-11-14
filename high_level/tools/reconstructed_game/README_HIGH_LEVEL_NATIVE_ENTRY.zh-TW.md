# 執行程式資料

[简体中文](README_HIGH_LEVEL_NATIVE_ENTRY.md) · **繁體中文** · [日本語](README_HIGH_LEVEL_NATIVE_ENTRY.ja.md) · [English](README_HIGH_LEVEL_NATIVE_ENTRY.en.md)

高階語言桌面入口使用 `g5510-reconstructed-game-config-v2`。專案原始碼決定遊戲邏輯；用於原程式複製和校驗的資料來自本版本實際建置。透過 [`tools.high_level_rom.build`](../high_level_rom/README_BUILD.zh-TW.md) 生成新本地建置目錄，將它作為 `m68k_native_root`。同一次完整輸出可作為 `sound_native_root`，其中的 `audio_startup` 和 `audio_driver` 屬於 Z80 建置組。

獨立的[歸一化音訊建置](../high_level_audio_engine/README_PORTABLE_BUILD.zh-TW.md)可單獨作為聲音程式根。載入器按所選建置形狀核對實際原始碼、彙編內容、指令與佈局。原遊戲的只讀程式複製和校驗見[M68K 程式資料](../high_level_rom/README_COMPILED_CODE_DATA.zh-TW.md)。

[本地配置說明](README_LOCAL_CONFIG.zh-TW.md)列出 Scene 資源、晶片庫、有限硬體輸入和存檔契約。
