# M68000 入口快照

[`M68KEntryCapture`](m68k_entry_capture.py) 在登记的 Python 业务函数入口读取同一场景的寄存器帧、SR、返回槽和 RAM。采集需要源文件、函数、帧类型与实际代码对象对应；返回位置来自真实物理调用栈。

记录格式为 `g5510-actual-m68k-entry-capture-v1`。只读 DATA 可通过同一会话的一次共享上下文保留。函数入口快照描述已进入的调用；需要原调用指令前的状态时使用[调用前观察器](README_M68K_PRE_CALL_CAPTURE.md)。
