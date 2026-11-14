# シーンソースのキャッシュ

[简体中文](README_SOURCE_ARTIFACT_CACHE.md) · [繁體中文](README_SOURCE_ARTIFACT_CACHE.zh-TW.md) · **日本語** · [English](README_SOURCE_ARTIFACT_CACHE.en.md)

[`source_artifact_cache.py`](source_artifact_cache.py) はシーン実行時のコンパイルに使うソース内容と、再利用できるコードオブジェクトを保存します。ソースとコンパイルのコンテキストで照合し、ソースが変われば新たな成果物を生成します。実行オブジェクトと Scene のライフサイクルはそれぞれ独立しています。

シーン、一騎討ち、オブジェクト制御のソースグループは、順に [`lifecycle_build.py`](lifecycle_build.py)、[`decision_build.py`](decision_build.py)、[`scene_object_build.py`](scene_object_build.py) が管理します。
