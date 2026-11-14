# 逆向工具

[简体中文](README.md) · **繁體中文** · [日本語](README.ja.md) · [English](README.en.md)

這裡提供 Mega Drive 遊戲《三國志列傳 亂世群英》的 ROM 轉換、反彙編、存檔和資源工具。輸入使用自己的卡匣映象、存檔或跟蹤記錄。命令從本目錄執行，示例使用 `input/` 和 `out/`。

Python 3.10 或更新版本即可執行基礎工具。68000 反彙編使用 Capstone；原始瓦片預覽使用 Pillow。

```sh
python -m pip install "capstone>=5" Pillow
```

| 用途 | 入口 |
| --- | --- |
| SMD 與線性 BIN 轉換、卡匣資訊 | [rom_tool.py](rom_tool.py) |
| 68000 反彙編、引用和間接跳轉 | [code_analysis](tools/code_analysis/) |
| Z80 載荷與驅動 | [audio_analysis](tools/audio_analysis/) |
| MAME 跟蹤彙總與記憶體採集 | [runtime_trace](tools/runtime_trace/)、[採集指令碼](tools/asset_analysis/mame_capture_memory.lua) |
| SRAM 格式和存檔佈局 | [save_data](tools/save_data/) |
| 圖形、音訊和劇本資源 | [資源參考](docs/resources.zh-TW.md) |

```sh
python rom_tool.py unpack input/cartridge.smd out/cartridge.bin out/copier-header.dat
python rom_tool.py info out/cartridge.bin
python tools/code_analysis/disasm_range.py out/cartridge.bin 0x11BC6:0x11C72
python tools/save_data/save_format.py inspect input/campaign.srm
```

[映象與反彙編](docs/cartridge-and-code.zh-TW.md)收錄 ROM、68000、Z80 和跟蹤命令。[資源與存檔](docs/resources.zh-TW.md)收錄匯入匯出方式和資料格式。各入口透過 `--help` 列出引數。
