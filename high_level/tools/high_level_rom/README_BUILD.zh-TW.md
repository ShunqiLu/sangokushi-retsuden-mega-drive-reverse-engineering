# Python 建置器

[简体中文](README_BUILD.md) · **繁體中文** · [日本語](README_BUILD.ja.md) · [English](README_BUILD.en.md)

從 [Python 版首頁](../../README.zh-TW.md) 配置執行環境。在原始碼根呼叫 `tools.high_level_rom.build`，以相容素材根、工具目錄及新輸出路徑作為顯式輸入。

| 引數 | 用途 |
| --- | --- |
| `build` | 編譯領域規則與音訊驅動，編碼素材，組裝卡匣映象。 |
| `plan` | 呼叫原始碼編譯器，生成建置計劃。 |
| `--project-root` | Python 原始碼根，預設取本專案根。 |
| `--resource-root` | 相容素材根，包含 `resources/` 和 `assets/`。 |
| `--m68k-tools`、`--z80-tools` | Windows 本地 GNU 工具目錄，由 WSL 呼叫。 |
| `--output` | 專案 `build/` 內專用的新輸出目錄。 |
| `--workers` | 建置工作數，預設 2。 |
| `--copier-header-fields` | 從結構化頭欄位同時建置 SMD。 |
| `--copier-header` | 使用呼叫者提供的容器頭；與頭欄位選項二選一。 |

```powershell
python -B -X utf8 -m tools.high_level_rom.build build --project-root . --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/python-image --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json
```

建置以明確的程式碼與資源分割槽生成 `SANGO.bin`。指定 SMD 頭後，建置器另寫 `SANGO.smd`。分割槽檢查要求影象中的位置全部有來源；原始碼準備失敗時，輸出目錄提供建置診斷。卡匣校驗欄位由登記源提供，遊戲邏輯按原格式使用它。

業務規則、編譯器和物理目標分屬領域模組。編輯介面見[規則與素材指南](../../EDITING.zh-TW.md)，桌面配置見[執行說明](../reconstructed_game/README_LOCAL_CONFIG.zh-TW.md)。
