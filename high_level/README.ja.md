# 『三國志列傳 亂世群英』G-5510-00 · Python 版

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **日本語** · [English](README.en.md)

内政、行軍、戦闘、シーン、AI、音声のルールを Python で記述しています。ビルドでは対応するルールをメガドライブの 68000・Z80 向けにコンパイルし、ローカル素材をエンコードしてカートリッジイメージを作成します。

## ビルド

Windows と WSL、Python 3.12 以降、Pillow、M68K 対応の Capstone 5 を使います。次の GNU クロスツールを、WSL からアクセスできる Windows ディレクトリに置きます。

- 68000：`m68k-elf-as`、`m68k-elf-ld`、`m68k-elf-objcopy`。
- Z80 COFF：`z80-unknown-coff-as`、`z80-unknown-coff-objcopy`。

このディレクトリで以下の PowerShell コマンドを実行します。両方のツールチェーンのパスと、`assets/` と `resources/` が同じ階層にある互換素材のディレクトリを指定します。

```powershell
python -m pip install Pillow "capstone>=5,<6"
$m68k = Read-Host '68000 交叉工具目录'
$z80 = Read-Host 'Z80 COFF 交叉工具目录'
$resources = Read-Host '兼容素材根'
python -B -X utf8 -m tools.high_level_rom.build build --project-root . --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/python-image --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json
```

出力先は新規の `build/python-image/` です。既定で `SANGO.bin` を生成し、`--copier-header-fields` を指定すると `SANGO.smd` も生成します。入力、引数、出力については[ビルドオプション](tools/high_level_rom/README_BUILD.ja.md)を参照してください。

## 編集

- [編集ガイド](EDITING.ja.md)では、ルール、シナリオ初期値、セーブ、グラフィック、音声のソースを案内します。
- [素材ガイド](ASSETS.ja.md)では、インデックス付き PNG、パレット、共有音声、ローカル素材の構成を説明します。
- [原版アドレス索引](PENDING_SOURCE_INDEX.ja.md)では、主なカートリッジのエントリーポイントと Python 関数を対応付けています。
- [原作の挙動](docs/ORIGINAL_GAME_BUGS.ja.md)では、再構築版で維持したルールや境界的な挙動をまとめています。

[デスクトップ版](tools/reconstructed_game/README_LOCAL_CONFIG.ja.md)は、ローカルの実行ディレクトリ、このソースからビルドした CPU プログラム、[外部の YMFM ソースでビルドした音声ブリッジ](tools/high_level_audio_engine/README_YMFM.ja.md)、明示的なデバイスとセーブの設定で動きます。コンソールと Tk ウィンドウは同じゲームアプリケーションを使います。
