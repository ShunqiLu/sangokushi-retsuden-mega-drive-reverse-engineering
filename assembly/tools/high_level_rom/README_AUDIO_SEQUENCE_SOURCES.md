# 音频序列

`resources/audio/audio_build.json` 登记音乐、音效、音色和序列成员，实际参数位于 `assets/audio/`。具名视图为支持的音频命令提供参数名称和取值约束。共享乐谱的视图指向同一份实际事件；修改共享音符时使用[共享事件编辑器](README_AUDIO_SEQUENCE_EDITOR.md)。

`$resources` 是同时包含 `resources/` 和 `assets/` 的本地素材根。命令从汇编版根目录运行。 有外置文件引用时，`--source-root` 指向本地素材根。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.audio_sequence_sources export --source "$resources/resources/audio/audio_build.json" --source-root $resources --project-root . --output build/audio-sequence.json
```

子命令 `edit` 接收具名文档和 `--edits`，`import` 将具名文档转回结构化格式。使用 `--help` 查看参数。
