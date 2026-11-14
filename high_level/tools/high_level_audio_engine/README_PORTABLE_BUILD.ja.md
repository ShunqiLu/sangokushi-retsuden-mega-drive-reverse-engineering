# Z80 音声プログラムのビルド

[简体中文](README_PORTABLE_BUILD.md) · [繁體中文](README_PORTABLE_BUILD.zh-TW.md) · **日本語** · [English](README_PORTABLE_BUILD.en.md)

[`tools.high_level_audio_engine.build`](build.py) はこの版の Python サウンドドライバーと、明示した GNU Z80 COFF ツールを使います。既存のビルドルートと、その下の新規出力先を指定します。カートリッジ全体のビルドで得た `audio_startup`、`audio_driver` もデスクトップ版で使用できます。

```powershell
$z80 = Read-Host 'Z80 COFF 交叉工具目录'
python -B -X utf8 -m tools.high_level_audio_engine.build --output-root build --output audio-native --tool-root $z80
```

個別の音声ビルドは正規化したソース、シンボル、Z80 プログラムデータを生成します。デスクトップ版のローダーは、この版のソースと音声モジュールに合うカートリッジ全体の出力か、正規化音声出力を読み込みます。パスとチップライブラリーは[ローカル設定](../reconstructed_game/README_LOCAL_CONFIG.ja.md)を参照してください。
