# Cartridge images and disassembly

[简体中文](cartridge-and-code.md) · [繁體中文](cartridge-and-code.zh-TW.md) · [日本語](cartridge-and-code.ja.md) · **English**

SMD images have a 512-byte copier header followed by interleaved 16 KiB blocks. Linear BIN images use 68000 byte order. The 68000 addresses below refer to the linear BIN.

```sh
python rom_tool.py unpack input/cartridge.smd out/cartridge.bin out/copier-header.dat
python rom_tool.py info out/cartridge.bin
python rom_tool.py pack out/cartridge.bin out/copier-header.dat out/repacked.smd
```

`unpack` checks the G-5510 cartridge header by default. Use `--allow-unknown` for other Mega Drive cartridges with the same system header. `info` prints the size, format, product ID, and cartridge checksum. To recompute the checksum, add `--fix-checksum` to `pack`.

## 68000 and Z80

```sh
python tools/code_analysis/disasm_range.py out/cartridge.bin 0x11BC6:0x11C72
python tools/code_analysis/find_m68k_refs.py out/cartridge.bin 0x83D4 --end 0x40000
python tools/code_analysis/m68k_code_map.py out/cartridge.bin --output-dir out/m68k
python tools/code_analysis/indirect_transfers.py out/cartridge.bin --baseline-code-map out/m68k/code_map.json --hints tools/code_analysis/indirect_hints.json --output-dir out/indirect
python tools/audio_analysis/z80_payload.py unpack --rom out/cartridge.bin --output out/z80-payload
python tools/audio_analysis/z80_audio_map.py --rom out/cartridge.bin --output out/z80-map --m68k-code-generated out/m68k
```

Disassembly ranges include the start and exclude the end. Reference searches return candidate instructions for review. The 68000 map traces control flow from vectors and supplied entry points. Indirect-transfer analysis uses instructions, table bounds, and target bytes to find possible edges; pass `--trace` to match observed next instructions.

Z80 addresses use a separate address space. Three payload files preserve the source cartridge segments. The runtime image and backups of overwritten regions support reassembly. `z80_payload.py verify` compares the two representations byte for byte. `--m68k-code-generated` adds 68000 call references to the Z80 address map.

## MAME traces

```sh
python tools/runtime_trace/summarize_mame_trace.py input/session.txt --rom out/cartridge.bin --json out/session.json
python tools/runtime_trace/merge_trace_summaries.py session=out/session.json --json out/coverage.json --csv out/coverage.csv
```

With `--rom`, the summarizer uses Capstone to calculate byte coverage for recorded instructions. Counts reflect the log entries and can be affected by MAME's loop compression.

MAME with Mega Drive Lua support can capture VRAM, Z80 memory, and a screenshot. Set `ASSET_CAPTURE_PREFIX` to a new relative ASCII file prefix in an existing directory, and `ASSET_CAPTURE_WAIT` to the wait in emulated seconds.

```powershell
$env:ASSET_CAPTURE_PREFIX = 'out/capture'
mame megadriv -cart input/cartridge.smd -autoboot_script tools/asset_analysis/mame_capture_memory.lua
python tools/asset_analysis/analyze_runtime_capture.py --rom out/cartridge.bin --vram out/capture_vram.bin --z80 out/capture_z80.bin --output out/correlation
```

The capture script reads VRAM and Z80 memory, saves a screenshot, and exits. The correlation tool identifies constant values and VRAM inputs mapped to the main ROM.
