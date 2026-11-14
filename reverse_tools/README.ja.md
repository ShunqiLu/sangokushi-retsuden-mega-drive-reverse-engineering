# 解析ツール

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **日本語** · [English](README.en.md)

メガドライブ版『三國志列傳 亂世群英』の ROM 変換、逆アセンブル、セーブデータと素材の解析ツールです。手元のカートリッジイメージ、セーブ、トレースを使います。例はこのディレクトリから実行し、`input/` と `out/` を使用します。

基本ツールは Python 3.10 以降で動きます。68000 の逆アセンブルは Capstone、生のタイルのプレビューは Pillow を使用します。

```sh
python -m pip install "capstone>=5" Pillow
```

| 用途 | ツール |
| --- | --- |
| SMD と線形 BIN の変換、カートリッジ情報 | [rom_tool.py](rom_tool.py) |
| 68000 の逆アセンブル、参照、間接分岐 | [code_analysis](tools/code_analysis/) |
| Z80 の転送データとサウンドドライバー | [audio_analysis](tools/audio_analysis/) |
| MAME トレースの集計とメモリ取得 | [runtime_trace](tools/runtime_trace/)、[取得スクリプト](tools/asset_analysis/mame_capture_memory.lua) |
| SRAM 形式とセーブデータの配置 | [save_data](tools/save_data/) |
| グラフィック、音声、シナリオ素材 | [素材の参照資料](docs/resources.ja.md) |

```sh
python rom_tool.py unpack input/cartridge.smd out/cartridge.bin out/copier-header.dat
python rom_tool.py info out/cartridge.bin
python tools/code_analysis/disasm_range.py out/cartridge.bin 0x11BC6:0x11C72
python tools/save_data/save_format.py inspect input/campaign.srm
```

ROM、68000、Z80、トレースのコマンドは[イメージと逆アセンブル](docs/cartridge-and-code.ja.md)、入出力とデータ形式は[素材とセーブデータ](docs/resources.ja.md)を参照してください。各ツールの引数は `--help` で確認できます。
