# アセンブリ版のビルドオプション

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **日本語** · [English](README.en.md)

ビルドツールは各グループのアドレス配置に従ってニーモニックを読み、GNU クロスツールで機械語に変換して、エンコード済みの素材と結合します。命令サイズの検証には、68000 は ELF シンボル、Z80 は COFF の境界を使います。

| 引数 | 用途 |
| --- | --- |
| `--source-root` | `src/m68k/` と `src/z80/` を含むソースルート |
| `--layout-root` | マニフェストと 14 グループの命令範囲を収めた `tools/reconstructed_assembly/layout/` |
| `--resource-root` | `resources/` と `assets/` を含む外部素材ルート |
| `--m68k-tools`、`--z80-tools` | Windows のローカルドライブに置く GNU ツールチェーンのディレクトリ。実行は WSL |
| `--output` | このソースツリーの `build/` 内に作る新規ディレクトリ |
| `--copier-header-fields` | 任意の SMD ヘッダーフィールド。テンプレートは `tools/high_level_rom/resource_sources/` |
| `--workers` | 並行ジョブ数。1〜4 |

ビルド結果は線形 BIN と、オプションで SMD です。各アドレス範囲の供給元はコードか素材のいずれか 1 つです。欠落、重複、幅の変化はビルドツールが報告します。コマンド全体は[アセンブリ版 README](../../README.ja.md)を参照してください。
