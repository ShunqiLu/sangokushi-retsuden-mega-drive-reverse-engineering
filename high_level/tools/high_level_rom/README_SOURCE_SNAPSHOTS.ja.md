# ソースと素材のスナップショット

[简体中文](README_SOURCE_SNAPSHOTS.md) · [繁體中文](README_SOURCE_SNAPSHOTS.zh-TW.md) · **日本語** · [English](README_SOURCE_SNAPSHOTS.en.md)

[`stage_sources.py`](stage_sources.py) にはビルド入力をメモリ上でまとめる 2 つのインターフェースがあります。

- `snapshot_resources(resource_root, resource_registration, ...)` は素材の登録からメタデータと内容を読み、バイト列のスナップショットを相対パスで索引化します。複数ルートのマニフェストに対応します。
- `snapshot_source_tree(project_root, resource_snapshot=...)` はこの版のソース依存関係を準備し、呼び出し側から渡された素材スナップショットを統合します。

素材登録には固定 ID、コーデック、ソースパス、役割、ビルド経路を記載します。対応表は出力ルートからの相対パスで、素材ファイルと必要な Scene マニフェストを含みます。ソースと素材の件数は別集計です。複数のソース対象で同じスナップショットを共有できます。ディレクトリの作成には [`stage_sources` コマンド](README_GAME_SOURCE_STAGE.ja.md)を使います。
