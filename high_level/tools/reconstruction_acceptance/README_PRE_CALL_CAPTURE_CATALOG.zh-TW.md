# 原呼叫目錄

[简体中文](README_PRE_CALL_CAPTURE_CATALOG.md) · **繁體中文** · [日本語](README_PRE_CALL_CAPTURE_CATALOG.ja.md) · [English](README_PRE_CALL_CAPTURE_CATALOG.en.md)

[`prepare_pre_call_index`](pre_call_capture_catalog.py) 依據呼叫方提供的入口批次與可定位的原呼叫源，生成 `PreparedPreCallIndex`。目錄區分真實父呼叫、helper、入口別名與原始碼入口引用，保留適用的符號、呼叫和返回關係。

`SourceEntryReference` 描述當前原始碼入口；`PreCallGap` 表示證據缺項。執行採集只消費與實際現場相符的目錄記錄；精確檔案格式和配置見[入口採集](../reconstructed_game/README_ENTRY_CAPTURE.zh-TW.md)。
