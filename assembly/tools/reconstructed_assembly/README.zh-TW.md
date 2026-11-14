# 彙編建置引數

[简体中文](README.md) · **繁體中文** · [日本語](README.ja.md) · [English](README.en.md)

建置器按各組地址佈局讀取助記符，使用 GNU 交叉工具生成指令，再與資源編碼器產生的資料合併。68000 和 Z80 的指令寬度分別由 ELF 符號和 COFF 邊界核對。

| 引數 | 用途 |
| --- | --- |
| `--source-root` | `src/m68k/` 與 `src/z80/` 所在的本版根 |
| `--layout-root` | `tools/reconstructed_assembly/layout/`，含清單和 14 組指令範圍 |
| `--resource-root` | 外部素材根，含 `resources/` 與 `assets/` |
| `--m68k-tools`、`--z80-tools` | Windows 本地磁碟上的兩套 GNU 工具目錄，由 WSL 執行 |
| `--output` | 位於本版 `build/` 下的新目錄 |
| `--copier-header-fields` | 可選 SMD 檔案頭欄位；專案模板在 `tools/high_level_rom/resource_sources/` |
| `--workers` | 併發任務數，取 1 到 4 |

生成結果為線性 BIN 和可選 SMD。完整地址區間由唯一原始碼或資源所有者提供；工具會提示缺項、重複區間或寬度變化。完整命令見[彙編版首頁](../../README.zh-TW.md)。
