# 音訊序列

[简体中文](README_AUDIO_SEQUENCE_SOURCES.md) · **繁體中文** · [日本語](README_AUDIO_SEQUENCE_SOURCES.ja.md) · [English](README_AUDIO_SEQUENCE_SOURCES.en.md)

`resources/audio/audio_build.json` 登記音樂、音效、音色和序列成員，實際引數位於 `assets/audio/`。具名檢視為支援的音訊命令提供引數名稱和取值約束。共享樂譜的檢視指向同一份實際事件；修改共享音符時使用[共享事件編輯器](README_AUDIO_SEQUENCE_EDITOR.zh-TW.md)。

`$resources` 是同時包含 `resources/` 和 `assets/` 的本地素材根。命令從彙編版根目錄執行。 有外接檔案引用時，`--source-root` 指向本地素材根。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.audio_sequence_sources export --source "$resources/resources/audio/audio_build.json" --source-root $resources --project-root . --output build/audio-sequence.json
```

子命令 `edit` 接收具名文件和 `--edits`，`import` 將具名文件轉回結構化格式。使用 `--help` 檢視引數。
