# ローカル実行ディレクトリ

[简体中文](README_GAME_SOURCE_STAGE.md) · [繁體中文](README_GAME_SOURCE_STAGE.zh-TW.md) · **日本語** · [English](README_GAME_SOURCE_STAGE.en.md)

[`stage_sources.py`](stage_sources.py) は指定したソースと登録素材を読み、ソース、設定テンプレート、素材、Scene マニフェストを独立した実行ディレクトリに用意します。完全なローカル素材ルートか、完全な複数ルートの Scene マニフェストと素材メタデータのマニフェストを指定します。

```powershell
python -B -X utf8 -m tools.high_level_rom.stage_sources stage --project-root . --resource-root $resources --output ../local-game
```

複数ルート形式には `--source-manifest` と `--asset-metadata-manifest` を使います。完全なマニフェストでは各素材 ID に対応する供給元は 1 つです。`plan` はソースの依存計画を出力し、`stage` はプロジェクトと素材ルートの外に新規ディレクトリを作ります。パスと値は明示した素材登録と、この版の静的・動的ソース宣言から決まります。

[素材ルートと別名](README_SCENE_SOURCE_PUBLICATION.ja.md)は複数ルートのマニフェストが扱う範囲を説明します。[デスクトップ設定](../reconstructed_game/README_LOCAL_CONFIG.ja.md)はイメージ、音源チップのライブラリー、デバイス入力、セーブを説明します。
