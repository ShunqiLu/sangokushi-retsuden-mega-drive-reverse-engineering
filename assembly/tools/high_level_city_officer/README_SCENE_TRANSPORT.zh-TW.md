# 運輸方向、到達與碰撞

[简体中文](README_SCENE_TRANSPORT.md) · **繁體中文** · [日本語](README_SCENE_TRANSPORT.ja.md) · [English](README_SCENE_TRANSPORT.en.md)

運輸流程按路線索引取下一方向，將到達資源記入目的城，並用運輸槽和隊伍列表檢查碰撞。資金和糧食的限額比較採用原位寬的累加結果。原始碼見 [68000 主程式](../../src/m68k/recovered_code.s)的 `m68k_016874`、`m68k_016946` 等入口。
