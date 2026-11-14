# 场景源码缓存

[`source_artifact_cache.py`](source_artifact_cache.py) 保存场景运行期编译所用的源文件内容和可复用代码对象。缓存匹配源码与编译上下文；源码改动会得到对应的新工件。运行对象和 Scene 采用各自的生命周期。

场景、单挑和对象控制的源组分别由 [`lifecycle_build.py`](lifecycle_build.py)、[`decision_build.py`](decision_build.py) 与 [`scene_object_build.py`](scene_object_build.py) 组织。
