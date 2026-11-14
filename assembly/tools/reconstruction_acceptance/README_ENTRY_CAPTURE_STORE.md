# 入口输入存储

**简体中文** · [繁體中文](README_ENTRY_CAPTURE_STORE.zh-TW.md) · [日本語](README_ENTRY_CAPTURE_STORE.ja.md) · [English](README_ENTRY_CAPTURE_STORE.en.md)

入口存储器接收调用方采集的元数据和 RAM。每条记录使用独立的短标识，写入 `input.json` 和 `input.ram`。调用方设定条数、文件大小、JSON 大小和磁盘余量；采集结束后统一关闭存储器。结果保存在调用方选定的新构建子目录。
