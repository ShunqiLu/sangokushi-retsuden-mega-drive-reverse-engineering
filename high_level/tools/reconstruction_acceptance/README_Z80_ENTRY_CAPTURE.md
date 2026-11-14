# Z80 入口观察器

[`Z80EntryObserver`](z80_entry_capture.py) 使用 [`load_z80_capture_targets`](z80_entry_capture_catalog.py) 准备有限的公开 Z80 入口，并在同一游戏会话捕获实际调用。桌面采集配置的 `audio` 段负责启用该观察器。

Z80 与 M68K 入口共享会话的监视器及存储容量。寄存器、控制信息和返回槽按其实际来源读取，未取得的字段以缺项表示。具体输出见[音频快照](README_AUDIO_ENTRY_CAPTURE.md)和[采集文件存储](README_ENTRY_CAPTURE_STORE.md)。
