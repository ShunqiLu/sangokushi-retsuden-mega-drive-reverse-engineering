# 镜像与反汇编

**简体中文** · [繁體中文](cartridge-and-code.zh-TW.md) · [日本語](cartridge-and-code.ja.md) · [English](cartridge-and-code.en.md)

SMD 包含 512 字节复制器头和以 16 KiB 为单位的交织数据。线性 BIN 使用 68000 的字节顺序。下列 68000 地址对应线性 BIN。

```sh
python rom_tool.py unpack input/cartridge.smd out/cartridge.bin out/copier-header.dat
python rom_tool.py info out/cartridge.bin
python rom_tool.py pack out/cartridge.bin out/copier-header.dat out/repacked.smd
```

`unpack` 默认检查 G-5510 卡带头；`--allow-unknown` 适用于具备相同系统头的其他 Mega Drive 卡带。`info` 显示大小、镜像格式、产品编号和卡带校验和。需要按卡带规则重算校验和时，给 `pack` 加 `--fix-checksum`。

## 68000 和 Z80

```sh
python tools/code_analysis/disasm_range.py out/cartridge.bin 0x11BC6:0x11C72
python tools/code_analysis/find_m68k_refs.py out/cartridge.bin 0x83D4 --end 0x40000
python tools/code_analysis/m68k_code_map.py out/cartridge.bin --output-dir out/m68k
python tools/code_analysis/indirect_transfers.py out/cartridge.bin --baseline-code-map out/m68k/code_map.json --hints tools/code_analysis/indirect_hints.json --output-dir out/indirect
python tools/audio_analysis/z80_payload.py unpack --rom out/cartridge.bin --output out/z80-payload
python tools/audio_analysis/z80_audio_map.py --rom out/cartridge.bin --output out/z80-map --m68k-code-generated out/m68k
```

区间反汇编使用左闭右开地址范围。引用搜索返回待核对的指令候选。68000 代码图从向量及指定入口追踪控制流。间接跳转工具根据指令、表边界和目标字节生成候选边；传入 `--trace` 可关联已观察的下一条指令。

Z80 地址属于独立地址空间。三个载荷文件保存卡带源段，运行映像和被覆盖区域的备份共同支持回装。`z80_payload.py verify` 对两种表示执行逐字节比较。`--m68k-code-generated` 为 Z80 地址图补充 68000 调用关联。

## MAME 跟踪

```sh
python tools/runtime_trace/summarize_mame_trace.py input/session.txt --rom out/cartridge.bin --json out/session.json
python tools/runtime_trace/merge_trace_summaries.py session=out/session.json --json out/coverage.json --csv out/coverage.csv
```

传入 `--rom` 后，汇总器用 Capstone 计算已记录指令的字节覆盖。记录次数反映日志中的条目，MAME 的循环压缩会影响数量。

使用具备 Mega Drive Lua 接口的 MAME 可采集 VRAM、Z80 内存和画面。`ASSET_CAPTURE_PREFIX` 取已有目录下的新相对 ASCII 文件前缀；`ASSET_CAPTURE_WAIT` 设定等待的模拟秒数。

```powershell
$env:ASSET_CAPTURE_PREFIX = 'out/capture'
mame megadriv -cart input/cartridge.smd -autoboot_script tools/asset_analysis/mame_capture_memory.lua
python tools/asset_analysis/analyze_runtime_capture.py --rom out/cartridge.bin --vram out/capture_vram.bin --z80 out/capture_z80.bin --output out/correlation
```

采集脚本读取 VRAM 和 Z80 空间，保存画面并结束运行。关联工具标记恒定值和映射到主 ROM 的 VRAM 输入。
