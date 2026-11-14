# Z80 音频入口快照

[`snapshot_audio_entry`](audio_entry_capture.py) 从调用方提供的实际音频状态、帧、入口绑定和续接信息读取快照。它按已有字段读取 Z80 载体、控制状态、交替寄存器与返回字；各值带有可观察来源。PC 与 R 的未知部分用 `missing` 记录，真实已知部分保留原宽度和顺序。

音频入口记录采用 `g5510-actual-z80-entry-capture-v1`；已采集的 8192 字节声音 RAM 由[存储组件](README_ENTRY_CAPTURE_STORE.md)独立保存。[Z80 观察器](README_Z80_ENTRY_CAPTURE.md)将快照绑定到同一游戏中的实际函数入口。
