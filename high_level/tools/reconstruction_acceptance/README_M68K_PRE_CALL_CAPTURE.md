# M68K 调用前快照

[`M68KPreCallObserver`](m68k_pre_call_capture.py) 识别原 helper 正文执行前的现场位置。原调用、返回位置、入口角色和实际调用体来自[调用目录](README_PRE_CALL_CAPTURE_CATALOG.md)，运行匹配通过[源码视图](README_PRE_CALL_SOURCE_VIEWS.md)完成。

记录格式为 `g5510-actual-m68k-pre-CALL-capture-v1`。快照含实际父帧、物理栈、RAM 与相关来源；真实父调用与入口别名各保留自己的身份。输出由[采集存储](README_ENTRY_CAPTURE_STORE.md)写入。
