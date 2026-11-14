# Scene source cache

[简体中文](README_SOURCE_ARTIFACT_CACHE.md) · [繁體中文](README_SOURCE_ARTIFACT_CACHE.zh-TW.md) · [日本語](README_SOURCE_ARTIFACT_CACHE.ja.md) · **English**

[`source_artifact_cache.py`](source_artifact_cache.py) caches the source text and reusable code objects used by runtime scene compilation. It matches source and compilation context; changed source gets a new compiled artifact. Runtime objects and the Scene each have their own lifetime.

Scene, duel, and object control source groups are managed by [`lifecycle_build.py`](lifecycle_build.py), [`decision_build.py`](decision_build.py), and [`scene_object_build.py`](scene_object_build.py), respectively.
