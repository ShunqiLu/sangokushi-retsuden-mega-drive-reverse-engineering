# 実行用プログラムデータ

[简体中文](README_HIGH_LEVEL_NATIVE_ENTRY.md) · [繁體中文](README_HIGH_LEVEL_NATIVE_ENTRY.zh-TW.md) · **日本語** · [English](README_HIGH_LEVEL_NATIVE_ENTRY.en.md)

Python 版のデスクトップ入口は `g5510-reconstructed-game-config-v2` を使います。ルールはプロジェクトのソースが決め、原作のコピー・チェックサム処理のデータはこの版のビルドから取ります。[`tools.high_level_rom.build`](../high_level_rom/README_BUILD.ja.md) で新しいローカルビルドを作り、`m68k_native_root` に指定します。同じビルド一式を `sound_native_root` にも使えます。その中の `audio_startup` と `audio_driver` が Z80 のビルドグループです。

独立した[正規化音声ビルド](../high_level_audio_engine/README_PORTABLE_BUILD.ja.md)もサウンドプログラムのルートに使えます。ローダーは選んだビルド形式に応じ、ソース、アセンブリ、命令、配置を照合します。読み取り専用のコピーとチェックサムは [M68K プログラムデータ](../high_level_rom/README_COMPILED_CODE_DATA.ja.md)を参照してください。

Scene 素材、チップライブラリー、有限のハードウェア入力、セーブの仕様は[ローカル設定](README_LOCAL_CONFIG.ja.md)を参照してください。
