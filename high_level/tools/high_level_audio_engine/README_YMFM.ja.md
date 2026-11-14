# YMFM 音声ブリッジ

[简体中文](README_YMFM.md) · [繁體中文](README_YMFM.zh-TW.md) · **日本語** · [English](README_YMFM.en.md)

[`YmfmDevice`](ymfm_device.py) は `FmPortDevice` を実装します。Python のドライバーは楽譜、音色、状態、レジスター操作を担当します。外部の [YMFM](https://github.com/aaronsgiles/ymfm) ソースは YM2612 の演算に使い、PSG は別のデバイスで扱います。

## ビルド

Python 版のソースルートで実行します。GNU 形式の引数に対応する C++14 コンパイラー、別途用意した互換 YMFM ソースのルート、新しい出力先を指定します。YMFM のルートには上流の `LICENSE` と `src/` が含まれます。

```powershell
$compiler = Read-Host 'C++14 g++ 或 clang++ 的路径'
$ymfmSource = Read-Host 'YMFM 源码根目录'
python -B -X utf8 -m tools.high_level_audio_engine.build_ymfm --compiler $compiler --ymfm-source $ymfmSource --output build/host-audio
```

出力は Windows では `g5510_ymfm.dll`、その他のプラットフォームでは `libg5510_ymfm.so` です。上流のライセンスと説明も保存します。[デスクトップ設定](../reconstructed_game/README_LOCAL_CONFIG.ja.md) の `--chip-library` にライブラリーを指定します。YMFM は上流の [BSD 3-Clause ライセンス](https://github.com/aaronsgiles/ymfm/blob/main/LICENSE)に従います。

## チップクロックと PCM

`YmfmDevice(library_path, clock_hz=..., pcm_sink=..., after_status_read=...)` にライブラリー、入力クロック周波数、音声出力先を指定します。呼び出し側は `advance(n)` でチップクロックを進めます。状態読み出しは現在のタイマーと BUSY を参照します。同時刻の処理順はタイマー A、B、ネイティブ PCM です。入力クロック 144 サイクルごとに YM2612 のネイティブサンプルを 1 つ生成します。PCM は符号付き 16 ビットのインターリーブステレオです。
