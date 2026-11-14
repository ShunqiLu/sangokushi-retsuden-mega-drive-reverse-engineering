# Python ビルドツール

[简体中文](README_BUILD.md) · [繁體中文](README_BUILD.zh-TW.md) · **日本語** · [English](README_BUILD.en.md)

[Python 版 README](../../README.ja.md)に沿って環境を準備します。ソースルートから `tools.high_level_rom.build` を実行し、互換素材ルート、ツールのディレクトリ、新規出力先を指定します。

| 引数 | 用途 |
| --- | --- |
| `build` | ゲームルールとサウンドドライバーをコンパイルし、素材をエンコードしてカートリッジイメージを組み立てます。 |
| `plan` | ソースコンパイラーを実行し、ビルド計画を生成します。 |
| `--project-root` | Python ソースのルート。既定はプロジェクトのルートです。 |
| `--resource-root` | `resources/` と `assets/` を含む互換素材ルート。 |
| `--m68k-tools`、`--z80-tools` | WSL から実行する GNU ツールを置いた Windows 上のディレクトリ。 |
| `--output` | プロジェクトの `build/` 内に作る新規出力先。 |
| `--workers` | ビルドの並列数。既定は 2 です。 |
| `--copier-header-fields` | 構造化ヘッダーフィールドから SMD も生成します。 |
| `--copier-header` | ヘッダーフィールドの代わりに指定のコンテナーヘッダーを使います。 |

```powershell
python -B -X utf8 -m tools.high_level_rom.build build --project-root . --resource-root $resources --m68k-tools $m68k --z80-tools $z80 --output build/python-image --copier-header-fields tools/high_level_rom/resource_sources/copier_header.json
```

コードと素材の区間を割り当てて `SANGO.bin` を生成します。SMD ヘッダーを指定すると `SANGO.smd` も出力します。イメージ内の全位置に供給元が必要です。ソース準備に失敗した場合、診断結果は出力先に入ります。登録素材が、原作の形式に従うカートリッジチェックサムのフィールドを供給します。

各機能のモジュールにゲームルール、コンパイラー、物理ターゲットがあります。編集は[ルールと素材](../../EDITING.ja.md)、デスクトップ設定は[実行設定](../reconstructed_game/README_LOCAL_CONFIG.ja.md)を参照してください。
