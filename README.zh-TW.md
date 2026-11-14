# 三國志列傳：亂世群英 · Mega Drive 逆向工程

[简体中文](README.md) · **繁體中文** · [日本語](README.ja.md) · [English](README.en.md)

**Sangokushi Retsuden: Ransei no Eiyuutachi** · 繁體中文版卡匣 `G-5510-00`

本專案提供組合語言和高階語言重建程式碼。這是第一個針對此版本、同時公開組合語言與 Python 兩套可建置原始碼的專案。

## 原始碼

- [組合語言原始碼](assembly/README.md)：68000 主程式、Z80 音訊驅動程式和卡匣位址配置。參見[編輯指南](assembly/EDITING.md)。
- [Python 原始碼](high_level/README.md)：內政、武將、行軍、戰鬥、AI 和音訊等遊戲規則及其編譯器。參見[編輯指南](high_level/EDITING.md)及[原始位址索引](high_level/PENDING_SOURCE_INDEX.md)。

## 工具

[逆向工具](reverse_tools/README.md)支援 BIN/SMD 互轉、卡匣標頭檢查、68000/Z80 反組譯和 MAME 執行追蹤，也可解析圖形、音訊、劇本和 SRAM 存檔。

## 建置

兩套原始碼都能建置 Mega Drive 的 `SANGO.bin` 和 `SANGO.smd`。建置使用 Windows + WSL、Python 3.12+、Pillow、支援 M68K 的 Capstone 5，以及 68000 和 Z80 的 GNU 交叉編譯工具。

透過 `--resource-root` 指定相容的[素材包](high_level/ASSETS.md)，其中 `assets/` 和 `resources/` 位於同一層。建置指令見[組合語言版](assembly/README.md)及 [Python 版](high_level/README.md)。
