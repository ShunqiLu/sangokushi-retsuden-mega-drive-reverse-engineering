# 関数入口の監視

[简体中文](README_ENTRY_MONITOR.md) · [繁體中文](README_ENTRY_MONITOR.zh-TW.md) · **日本語** · [English](README_ENTRY_MONITOR.en.md)

モニターは Python 3.12 の `sys.monitoring` で関数のコードオブジェクトを照合します。登録時に入口、コールバック、収集上限を指定し、終了時に監視スロットを解放します。設定は[入口キャプチャー](../reconstructed_game/README_ENTRY_CAPTURE.ja.md)を参照してください。
