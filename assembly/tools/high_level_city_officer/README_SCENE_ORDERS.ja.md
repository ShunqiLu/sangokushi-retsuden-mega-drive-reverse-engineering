# 都市命令と資源の加算

[简体中文](README_SCENE_ORDERS.md) · [繁體中文](README_SCENE_ORDERS.zh-TW.md) · **日本語** · [English](README_SCENE_ORDERS.en.md)

協定は方向に応じて双方の勢力のフラグを更新します。資源の加算では現在の勢力と君主の都市から金または兵糧の欄を選び、32 ビットで加算と上限比較を行います。入口は `m68k_0318ac` です。[68000 ディスパッチ処理](../../src/m68k/dispatch_descendants.s)を参照してください。
