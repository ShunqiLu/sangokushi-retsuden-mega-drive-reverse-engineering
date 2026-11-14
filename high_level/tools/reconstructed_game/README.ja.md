# デスクトップ版

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **日本語** · [English](README.en.md)

[`tools.reconstructed_game`](__main__.py) は同じアプリでシーン、入力、画面、音声、セーブを進めます。Tk のウィンドウに実際の画面を表示し、コンソールからは JSON Lines プロトコルで同じ再開可能なセッションを操作できます。

## 起動

[ローカル設定](README_LOCAL_CONFIG.ja.md)では、ソース、素材、プログラムデータ、音源チップのライブラリー、デバイス入力、セーブを説明します。用意した設定で起動します。

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend window
```

`--frontend console` は[コンソール](README_CONSOLE.ja.md)を有効にします。完全なフレーム計画が必要です。`--session-output` には設定ルートの `build/` 内に新しいセッションパスを指定します。

## 設定

- [アプリのインターフェースと PCM](README_APPLICATION.ja.md)、[任意のスピーカー出力](README_SPEAKERS.ja.md)。
- [完全なフレーム計画](README_FRAME_PLAN.ja.md)、[ハードウェア入力](README_HARDWARE_INPUTS.ja.md)、[入力容量](README_HARDWARE_PROFILE.ja.md)。
- [オープニングとシナリオの順序付き再起動](README_ORDERED_RESTARTS.ja.md)、[コールド・ウォーム経路](README_ORDERED_COLD_PLAN.ja.md)。
- [任意の入口キャプチャー](README_ENTRY_CAPTURE.ja.md)。

各段階で、設定に記載したデバイスイベントを指定量だけ消費します。アプリは同じ物理フレームとセーブ媒体を保持し、デバイスの入力を使い切ると対応する実行境界を返します。
