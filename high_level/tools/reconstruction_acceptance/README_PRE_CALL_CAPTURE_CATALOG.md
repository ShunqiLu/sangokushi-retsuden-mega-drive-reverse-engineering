# 原调用目录

[`prepare_pre_call_index`](pre_call_capture_catalog.py) 依据调用方提供的入口批次与可定位的原调用源，生成 `PreparedPreCallIndex`。目录区分真实父调用、helper、入口别名与源码入口引用，保留适用的符号、调用和返回关系。

`SourceEntryReference` 描述当前源码入口；`PreCallGap` 表示证据缺项。运行采集只消费与实际现场相符的目录记录；精确文件格式和配置见[入口采集](../reconstructed_game/README_ENTRY_CAPTURE.md)。
