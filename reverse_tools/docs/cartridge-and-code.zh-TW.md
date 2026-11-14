# 映象與反彙編

[简体中文](cartridge-and-code.md) · **繁體中文** · [日本語](cartridge-and-code.ja.md) · [English](cartridge-and-code.en.md)

SMD 包含 512 位元組複製器頭和以 16 KiB 為單位的交織資料。線性 BIN 使用 68000 的位元組順序。下列 68000 地址對應線性 BIN。

```sh
python rom_tool.py unpack input/cartridge.smd out/cartridge.bin out/copier-header.dat
python rom_tool.py info out/cartridge.bin
python rom_tool.py pack out/cartridge.bin out/copier-header.dat out/repacked.smd
```

`unpack` 預設檢查 G-5510 卡匣頭；`--allow-unknown` 適用於具備相同系統頭的其他 Mega Drive 卡匣。`info` 顯示大小、映象格式、產品編號和卡匣校驗和。需要按卡匣規則重算校驗和時，給 `pack` 加 `--fix-checksum`。

## 68000 和 Z80

```sh
python tools/code_analysis/disasm_range.py out/cartridge.bin 0x11BC6:0x11C72
python tools/code_analysis/find_m68k_refs.py out/cartridge.bin 0x83D4 --end 0x40000
python tools/code_analysis/m68k_code_map.py out/cartridge.bin --output-dir out/m68k
python tools/code_analysis/indirect_transfers.py out/cartridge.bin --baseline-code-map out/m68k/code_map.json --hints tools/code_analysis/indirect_hints.json --output-dir out/indirect
python tools/audio_analysis/z80_payload.py unpack --rom out/cartridge.bin --output out/z80-payload
python tools/audio_analysis/z80_audio_map.py --rom out/cartridge.bin --output out/z80-map --m68k-code-generated out/m68k
```

區間反彙編使用左閉右開地址範圍。引用搜尋返回待核對的指令候選。68000 程式碼圖從向量及指定入口追蹤控制流。間接跳轉工具根據指令、表邊界和目標位元組生成候選邊；傳入 `--trace` 可關聯已觀察的下一條指令。

Z80 地址屬於獨立地址空間。三個載荷檔案儲存卡匣源段，執行映像和被覆蓋區域的備份共同支援回裝。`z80_payload.py verify` 對兩種表示執行逐位元組比較。`--m68k-code-generated` 為 Z80 地址圖補充 68000 呼叫關聯。

## MAME 跟蹤

```sh
python tools/runtime_trace/summarize_mame_trace.py input/session.txt --rom out/cartridge.bin --json out/session.json
python tools/runtime_trace/merge_trace_summaries.py session=out/session.json --json out/coverage.json --csv out/coverage.csv
```

傳入 `--rom` 後，彙總器用 Capstone 計算已記錄指令的位元組覆蓋。記錄次數反映日誌中的條目，MAME 的迴圈壓縮會影響數量。

使用具備 Mega Drive Lua 介面的 MAME 可採集 VRAM、Z80 記憶體和畫面。`ASSET_CAPTURE_PREFIX` 取已有目錄下的新相對 ASCII 檔案字首；`ASSET_CAPTURE_WAIT` 設定等待的模擬秒數。

```powershell
$env:ASSET_CAPTURE_PREFIX = 'out/capture'
mame megadriv -cart input/cartridge.smd -autoboot_script tools/asset_analysis/mame_capture_memory.lua
python tools/asset_analysis/analyze_runtime_capture.py --rom out/cartridge.bin --vram out/capture_vram.bin --z80 out/capture_z80.bin --output out/correlation
```

採集指令碼讀取 VRAM 和 Z80 空間，儲存畫面並結束執行。關聯工具標記恆定值和對映到主 ROM 的 VRAM 輸入。
