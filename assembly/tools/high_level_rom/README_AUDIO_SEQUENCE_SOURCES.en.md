# Audio sequences

[简体中文](README_AUDIO_SEQUENCE_SOURCES.md) · [繁體中文](README_AUDIO_SEQUENCE_SOURCES.zh-TW.md) · [日本語](README_AUDIO_SEQUENCE_SOURCES.ja.md) · **English**

`resources/audio/audio_build.json` registers music, sound effects, instrument patches, and sequence members. The values are in `assets/audio/`. The named view documents parameters and constraints for supported commands. Shared score views refer to the same events; use the [shared event editor](README_AUDIO_SEQUENCE_EDITOR.en.md) to change a shared note.

`$resources` is the local resource root containing `resources/` and `assets/`. Run from the assembly root. For external file references, set `--source-root` to the local resource root.

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.audio_sequence_sources export --source "$resources/resources/audio/audio_build.json" --source-root $resources --project-root . --output build/audio-sequence.json
```

The `edit` subcommand takes the named document and `--edits`. `import` converts the named document back to the structured format. Use `--help` for the options.
