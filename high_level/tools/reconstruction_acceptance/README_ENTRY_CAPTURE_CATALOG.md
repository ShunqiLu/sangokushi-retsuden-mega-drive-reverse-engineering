# 入口采集目录

**简体中文** · [繁體中文](README_ENTRY_CAPTURE_CATALOG.zh-TW.md) · [日本語](README_ENTRY_CAPTURE_CATALOG.ja.md) · [English](README_ENTRY_CAPTURE_CATALOG.en.md)

[`load_capture_targets(batch, project_root)`](entry_capture_catalog.py) 从 `g5510-concentrated-explicit-input-batch-v1` 文档返回固定的 `CaptureTarget` 元组。目标通过原入口地址、Python 模块与函数名、帧类型和调用参数关联当前声明。

目录装载核对来源、精确标识与入口身份。现场数据由[入口监视器](README_ENTRY_MONITOR.md)在实际调用时记录。
