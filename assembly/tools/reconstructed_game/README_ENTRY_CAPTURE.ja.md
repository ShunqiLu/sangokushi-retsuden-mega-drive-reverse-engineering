# 関数入口のキャプチャー

[简体中文](README_ENTRY_CAPTURE.md) · [繁體中文](README_ENTRY_CAPTURE.zh-TW.md) · **日本語** · [English](README_ENTRY_CAPTURE.en.md)

[Python 版](../../../high_level/README.ja.md)のデスクトップアプリは、設定したセッションで選択した 68000 または Z80 のエントリーポイントを記録できます。指定の上限に従い、新しいローカルディレクトリに書き出します。[68000 の設定例](examples/entry_capture.example.json)と[音声の設定例](examples/entry_capture.audio.example.json)があります。

Python 版のローカル実行コピーに通常のゲーム設定を用意し、キャプチャー用の設定を別に指定します。

```powershell
python -B -m tools.reconstructed_game --config ./play.json --capture-entries ./entry-capture.json
```
