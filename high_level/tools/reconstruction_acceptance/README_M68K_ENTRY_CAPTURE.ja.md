# M68000 入口のスナップショット

[简体中文](README_M68K_ENTRY_CAPTURE.md) · [繁體中文](README_M68K_ENTRY_CAPTURE.zh-TW.md) · **日本語** · [English](README_M68K_ENTRY_CAPTURE.en.md)

[`M68KEntryCapture`](m68k_entry_capture.py) は登録済み Python ルール関数の入口で、同じシーンのレジスターフレーム、SR、戻りスロット、RAM を読みます。ソースファイル、関数、フレーム型が実際のコードオブジェクトに対応している必要があります。復帰位置は物理呼び出しスタックから取得します。

レコードの形式は `g5510-actual-m68k-entry-capture-v1` です。読み取り専用の DATA はセッション内の共有コンテキストにまとめて保持できます。このスナップショットは関数に入った後の状態です。元の呼び出し命令より前の状態は[呼び出し前オブザーバー](README_M68K_PRE_CALL_CAPTURE.ja.md)で取得します。
