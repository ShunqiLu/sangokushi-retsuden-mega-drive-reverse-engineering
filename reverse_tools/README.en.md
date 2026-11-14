# Reverse-engineering tools

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **English**

Tools for Sangokushi Retsuden on the Mega Drive cover ROM conversion, disassembly, save data, and resources. Use your own cartridge image, save, or trace. Run the examples from this directory; their paths are under `input/` and `out/`.

The basic tools require Python 3.10 or later. Capstone handles 68000 disassembly; Pillow handles raw tile previews.

```sh
python -m pip install "capstone>=5" Pillow
```

| Task | Tool |
| --- | --- |
| SMD and linear BIN conversion, cartridge information | [rom_tool.py](rom_tool.py) |
| 68000 disassembly, references, and indirect branches | [code_analysis](tools/code_analysis/) |
| Z80 payload and sound driver | [audio_analysis](tools/audio_analysis/) |
| MAME trace summaries and memory capture | [runtime_trace](tools/runtime_trace/), [Capture script](tools/asset_analysis/mame_capture_memory.lua) |
| SRAM format and save layout | [save_data](tools/save_data/) |
| Graphics, audio, and scenario resources | [Resource reference](docs/resources.en.md) |

```sh
python rom_tool.py unpack input/cartridge.smd out/cartridge.bin out/copier-header.dat
python rom_tool.py info out/cartridge.bin
python tools/code_analysis/disasm_range.py out/cartridge.bin 0x11BC6:0x11C72
python tools/save_data/save_format.py inspect input/campaign.srm
```

See [Cartridge images and disassembly](docs/cartridge-and-code.en.md) for ROM, 68000, Z80, and trace commands. See [Resources and saves](docs/resources.en.md) for import and export commands and file formats. Use `--help` for a tool's options.
