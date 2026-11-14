# 『三國志列傳 亂世群英』アセンブリソース

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **日本語** · [English](README.en.md)

データと命令を 68000・Z80 用の GNU アセンブリで記述しています。ビルドでは、アドレス配置とエンコードした素材を合わせてカートリッジイメージを作ります。ローカルの素材パックには `resources/` と `assets/` を同じ階層に置きます。

## ビルド

Windows のローカルドライブ上で Python 3.12 以降、Pillow、M68K 対応の Capstone 5 を使います。WSL から 68000 用の `m68k-elf-as`、`m68k-elf-ld`、`m68k-elf-objcopy` と、Z80 用の `z80-unknown-coff-as`、`z80-unknown-coff-objcopy` を実行します。

このディレクトリで実行します。

```powershell
python -m pip install Pillow "capstone>=5,<6"
$m68k = Read-Host '68000 工具目录'
$z80 = Read-Host 'Z80 COFF 工具目录'
$resources = Read-Host '本地素材根目录'
python -B -X utf8 -m tools.reconstructed_assembly --source-root . --layout-root tools/reconstructed_assembly/layout --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/cartridge --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json --workers 2
```

`build/cartridge/` に `SANGO.bin`、`SANGO.smd` とビルド結果が出力されます。ビルドごとに新しい出力先を指定します。標準出力は BIN です。`--copier-header-fields` を指定するとヘッダーとインターリーブデータを含む SMD も生成します。全引数は[ビルドオプション](tools/reconstructed_assembly/README.ja.md)を参照してください。

## 編集

- プログラムのソースは `src/m68k/` と `src/z80/`、アドレス範囲、命令サイズ、素材の登録情報は `tools/reconstructed_assembly/layout/` にあります。
- グラフィック、効果音、シナリオ、台詞については[編集ガイド](EDITING.ja.md)と[素材のパス](ASSETS.ja.md)を参照してください。
- [原作の挙動](docs/ORIGINAL_GAME_BUGS.ja.md)には、再構築版で維持した特殊な挙動をまとめています。
