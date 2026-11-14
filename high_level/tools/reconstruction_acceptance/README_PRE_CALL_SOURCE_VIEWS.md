# 调用前源码视图

[`pre_call_source_views.py`](pre_call_source_views.py) 将已准备的 helper 来源与实际 Python 代码对象对应，保存同一调用所需的完整函数形状、入口绑定和现场身份。运行回调以已经准备好的视图识别实际调用前位置。

[原调用目录](README_PRE_CALL_CAPTURE_CATALOG.md)提供父调用与入口引用；[调用前观察器](README_M68K_PRE_CALL_CAPTURE.md)读取调用位置的真实状态。
