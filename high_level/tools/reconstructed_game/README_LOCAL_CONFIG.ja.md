# デスクトップ設定

[简体中文](README_LOCAL_CONFIG.md) · [繁體中文](README_LOCAL_CONFIG.zh-TW.md) · **日本語** · [English](README_LOCAL_CONFIG.en.md)

[`local_config.py`](local_config.py) は指定されたローカル入力から `g5510-reconstructed-game-config-v2` を作成します。実行ディレクトリにはこの版のソース、`scene-sources.json`、`resources/`、`assets/`、`build/` があります。Scene マニフェストの素材ルートは `.` の 1 つです。

実行ディレクトリは[ソース準備ツール](../high_level_rom/README_GAME_SOURCE_STAGE.ja.md)で作成できます。この版の M68K・Z80 ビルド出力、外部 YMFM ソースを[音声ブリッジビルド](../high_level_audio_engine/README_YMFM.ja.md)でコンパイルしたライブラリー、完全なハードウェア JSON、操作・タイミング・PCM・セーブの設定を渡します。両 CPU に同じ[完全ビルド](../high_level_rom/README_BUILD.ja.md)を使えます。設定の構造は `runtime.high-level.example.json` にあります。実行時はセッションに合ったハードウェアイベントを用意してください。

```powershell
python -B -X utf8 -m tools.reconstructed_game.local_config --edition-root . --settings runtime-inputs/gameplay.json --m68k-native-root build/python-image --sound-native-root build/python-image --chip-library build/host-ymfm/g5510_ymfm.dll --inputs runtime-inputs/hardware.json --save-path runtime-inputs/current-save.srm --run-output build/play --output build/play-config.json --frontend window
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend window
```

`--frontend console` では完全な `frontend.frame_plan` を用意します。`--run-output` と `--output` は `build/` 内の新規パスです。診断ディレクトリと任意の PCM のパスは実行出力名から決まります。

| セーブ形式 | フィールド |
| --- | --- |
| `save.path` | `--save-path` でこの版にある 8192 バイトの媒体を指定します。読み書き権限はそのままです。 |
| `save.initial_byte` | 0～255 の初期バイト値で新しい論理媒体を作ります。`initial_byte`、`readable`、`writable` を使います。 |

`materialize_local_gameplay_config(...)` は同等の Python インターフェースです。設定生成がパスと構造を、ゲームのローダーが実際の素材、ハードウェア、プログラムデータを扱います。
