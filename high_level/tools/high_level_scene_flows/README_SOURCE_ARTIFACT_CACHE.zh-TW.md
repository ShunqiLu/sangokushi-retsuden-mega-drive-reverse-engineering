# 場景原始碼快取

[简体中文](README_SOURCE_ARTIFACT_CACHE.md) · **繁體中文** · [日本語](README_SOURCE_ARTIFACT_CACHE.ja.md) · [English](README_SOURCE_ARTIFACT_CACHE.en.md)

[`source_artifact_cache.py`](source_artifact_cache.py) 儲存場景執行期編譯所用的原始檔內容和可複用程式碼物件。快取匹配原始碼與編譯上下文；原始碼改動會得到對應的新工件。執行物件和 Scene 採用各自的生命週期。

場景、單挑和物件控制的源組分別由 [`lifecycle_build.py`](lifecycle_build.py)、[`decision_build.py`](decision_build.py) 與 [`scene_object_build.py`](scene_object_build.py) 組織。
