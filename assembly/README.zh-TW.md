# 《三國志列傳 亂世群英》彙編原始碼

[简体中文](README.md) · **繁體中文** · [日本語](README.ja.md) · [English](README.en.md)

彙編版以 GNU 68000 和 Z80 助記符描述程式，透過地址佈局和資源編碼器生成 Mega Drive 卡匣映象。建置使用本地的相容素材包，其中並列放置 `resources/` 和 `assets/`。

## 建置

在 Windows 的本地磁碟上使用 Python 3.12 或更新版本、Pillow 和支援 M68K 的 Capstone 5。WSL 呼叫兩套 GNU 工具：68000 使用 `m68k-elf-as`、`m68k-elf-ld`、`m68k-elf-objcopy`；Z80 使用 `z80-unknown-coff-as` 和 `z80-unknown-coff-objcopy`。

在本目錄執行：

```powershell
python -m pip install Pillow "capstone>=5,<6"
$m68k = Read-Host '68000 工具目录'
$z80 = Read-Host 'Z80 COFF 工具目录'
$resources = Read-Host '本地素材根目录'
python -B -X utf8 -m tools.reconstructed_assembly --source-root . --layout-root tools/reconstructed_assembly/layout --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/cartridge --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json --workers 2
```

`build/cartridge/` 接收 `SANGO.bin`、`SANGO.smd` 和建置結果。每次建置請選擇一個新的輸出目錄。`--copier-header-fields` 啟用 SMD 檔案頭和交錯打包；基本輸出為 BIN。完整引數見[建置引數](tools/reconstructed_assembly/README.zh-TW.md)。

## 編輯

- 程式入口在 `src/m68k/` 和 `src/z80/`；地址、指令寬度和資源登記見 `tools/reconstructed_assembly/layout/`。
- 影象、音效、劇本和對話的原始檔見[編輯說明](EDITING.zh-TW.md)及[素材路徑指南](ASSETS.zh-TW.md)。
- [原版行為](docs/ORIGINAL_GAME_BUGS.zh-TW.md)說明程式保留的特殊規則。
