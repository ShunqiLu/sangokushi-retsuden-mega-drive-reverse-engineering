# Z80 音声入口のスナップショット

[简体中文](README_AUDIO_ENTRY_CAPTURE.md) · [繁體中文](README_AUDIO_ENTRY_CAPTURE.zh-TW.md) · **日本語** · [English](README_AUDIO_ENTRY_CAPTURE.en.md)

[`snapshot_audio_entry`](audio_entry_capture.py) は呼び出し側の実際の音声状態、フレーム、入口の対応付け、継続情報からスナップショットを作ります。Z80 の実行データ、制御状態、裏レジスター、戻りワードを既存フィールドから読み、各値に観測可能な出所を残します。PC と R の不明箇所は `missing` とし、判明している部分の幅と順序は維持します。

音声入口レコードの形式は `g5510-actual-z80-entry-capture-v1` です。[保存コンポーネント](README_ENTRY_CAPTURE_STORE.ja.md)は取得した 8192 バイトの音声 RAM を別に保存します。[Z80 オブザーバー](README_Z80_ENTRY_CAPTURE.ja.md)が同じゲーム内の実際の関数入口に対応付けます。
