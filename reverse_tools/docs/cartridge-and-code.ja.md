# イメージと逆アセンブル

[简体中文](cartridge-and-code.md) · [繁體中文](cartridge-and-code.zh-TW.md) · **日本語** · [English](cartridge-and-code.en.md)

SMD は 512 バイトのコピー機用ヘッダーと、16 KiB 単位でインターリーブしたデータで構成されます。線形 BIN は 68000 のバイト順です。以下の 68000 アドレスは線形 BIN を基準とします。

```sh
python rom_tool.py unpack input/cartridge.smd out/cartridge.bin out/copier-header.dat
python rom_tool.py info out/cartridge.bin
python rom_tool.py pack out/cartridge.bin out/copier-header.dat out/repacked.smd
```

`unpack` は既定で G-5510 のカートリッジヘッダーを確認します。同じシステムヘッダーを持つ別のメガドライブカートリッジには `--allow-unknown` を使えます。`info` はサイズ、形式、製品番号、チェックサムを表示します。チェックサムを再計算するには `pack` に `--fix-checksum` を付けます。

## 68000 と Z80

```sh
python tools/code_analysis/disasm_range.py out/cartridge.bin 0x11BC6:0x11C72
python tools/code_analysis/find_m68k_refs.py out/cartridge.bin 0x83D4 --end 0x40000
python tools/code_analysis/m68k_code_map.py out/cartridge.bin --output-dir out/m68k
python tools/code_analysis/indirect_transfers.py out/cartridge.bin --baseline-code-map out/m68k/code_map.json --hints tools/code_analysis/indirect_hints.json --output-dir out/indirect
python tools/audio_analysis/z80_payload.py unpack --rom out/cartridge.bin --output out/z80-payload
python tools/audio_analysis/z80_audio_map.py --rom out/cartridge.bin --output out/z80-map --m68k-code-generated out/m68k
```

逆アセンブルの範囲は開始アドレスを含み、終了アドレスを含みません。参照検索は確認すべき命令候補を返します。68000 のコードマップはベクターと指定した入口から制御フローをたどります。間接分岐のツールは命令、テーブルの範囲、分岐先のバイト列から候補を作ります。`--trace` を渡すと実際に観測した次の命令と照合できます。

Z80 は独立したアドレス空間を持ちます。3 つの転送データファイルにカートリッジ側の区間を保存し、実行時イメージと上書き領域のバックアップで再構成できます。`z80_payload.py verify` は両方の表現をバイト単位で照合します。`--m68k-code-generated` は Z80 アドレスマップに 68000 側の呼び出し参照を追加します。

## MAME トレース

```sh
python tools/runtime_trace/summarize_mame_trace.py input/session.txt --rom out/cartridge.bin --json out/session.json
python tools/runtime_trace/merge_trace_summaries.py session=out/session.json --json out/coverage.json --csv out/coverage.csv
```

`--rom` を指定すると、集計ツールは Capstone で記録済み命令のバイト範囲を求めます。件数はログ内の項目数で、MAME のループ圧縮の影響を受けます。

メガドライブの Lua インターフェースに対応する MAME では、VRAM、Z80 メモリ、画面を取得できます。`ASSET_CAPTURE_PREFIX` には既存のディレクトリ内で使う新しい相対 ASCII ファイル接頭辞を、`ASSET_CAPTURE_WAIT` にはエミュレーション上の待機秒数を指定します。

```powershell
$env:ASSET_CAPTURE_PREFIX = 'out/capture'
mame megadriv -cart input/cartridge.smd -autoboot_script tools/asset_analysis/mame_capture_memory.lua
python tools/asset_analysis/analyze_runtime_capture.py --rom out/cartridge.bin --vram out/capture_vram.bin --z80 out/capture_z80.bin --output out/correlation
```

取得スクリプトは VRAM と Z80 メモリを読み取り、画面を保存して終了します。照合ツールは定数と、メイン ROM に対応する VRAM の入力を特定します。
