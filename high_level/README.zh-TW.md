# 《三國志列傳 亂世群英》G-5510-00 · Python 版

[简体中文](README.md) · **繁體中文** · [日本語](README.ja.md) · [English](README.en.md)

遊戲規則以 Python 原始碼呈現，按內政、行軍、戰鬥、場景、AI 和音訊分組。建置器將受支援的規則編譯為 Mega Drive 的 68000 和 Z80 程式，並將相容的本地素材編碼為遊戲卡匣映象。

## 從原始碼建置

建置環境使用 Windows、WSL、Python 3.12 或更新版本、Pillow 和支援 M68K 的 Capstone 5。兩套 GNU 交叉工具放在 WSL 可訪問的 Windows 目錄：

- 68000：`m68k-elf-as`、`m68k-elf-ld`、`m68k-elf-objcopy`。
- Z80 COFF：`z80-unknown-coff-as`、`z80-unknown-coff-objcopy`。

從本目錄執行下列 PowerShell 命令，提供兩個工具目錄和相容素材根。素材根包含並列的 `assets/` 和 `resources/`。

```powershell
python -m pip install Pillow "capstone>=5,<6"
$m68k = Read-Host '68000 交叉工具目录'
$z80 = Read-Host 'Z80 COFF 交叉工具目录'
$resources = Read-Host '兼容素材根'
python -B -X utf8 -m tools.high_level_rom.build build --project-root . --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/python-image --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json
```

建置結果寫入新的 `build/python-image/`。預設生成 `SANGO.bin`；這裡的 `--copier-header-fields` 同時啟用 `SANGO.smd`。建置輸入、引數和輸出見[建置說明](tools/high_level_rom/README_BUILD.zh-TW.md)。

## 編輯遊戲

- [編輯入口](EDITING.zh-TW.md)按規則、初始劇本、存檔、影象和音訊定位原始檔。
- [素材指南](ASSETS.zh-TW.md)介紹索引 PNG、調色盤、共享音訊和本地素材結構。
- [原地址索引](PENDING_SOURCE_INDEX.zh-TW.md)將選定的卡匣入口對映到 Python 函式。
- [原版相容行為](docs/ORIGINAL_GAME_BUGS.zh-TW.md)列出復原時保留的行為和邊界條件。

[桌面執行](tools/reconstructed_game/README_LOCAL_CONFIG.zh-TW.md)使用本地執行目錄、由本版原始碼建置的 CPU 程式資料、[由外接 YMFM 原始碼建置的音訊橋](tools/high_level_audio_engine/README_YMFM.zh-TW.md)和明確的裝置與存檔配置。控制檯和 Tk 視窗共用同一個遊戲應用。
