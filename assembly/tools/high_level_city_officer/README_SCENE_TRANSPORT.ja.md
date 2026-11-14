# 輸送の進行方向・到着・衝突

[简体中文](README_SCENE_TRANSPORT.md) · [繁體中文](README_SCENE_TRANSPORT.zh-TW.md) · **日本語** · [English](README_SCENE_TRANSPORT.en.md)

経路インデックスから次の方向を取得し、到着時に資源を目的地の都市に加算します。衝突判定には輸送スロットと部隊リストを使います。金と兵糧の上限は元のビット幅での加算結果と比較します。[68000 メインプログラム](../../src/m68k/recovered_code.s)の `m68k_016874`、`m68k_016946` などを参照してください。
