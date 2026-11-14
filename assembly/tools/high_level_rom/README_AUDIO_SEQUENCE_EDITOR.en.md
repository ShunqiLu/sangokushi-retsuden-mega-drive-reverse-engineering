# Shared score event editor

[简体中文](README_AUDIO_SEQUENCE_EDITOR.md) · [繁體中文](README_AUDIO_SEQUENCE_EDITOR.zh-TW.md) · [日本語](README_AUDIO_SEQUENCE_EDITOR.ja.md) · **English**

Shared score events are in `assets/audio/shared/stateful_event_views.json` in the local run copy. Each edit specifies view `view_id`, field `field`, original value `expected`, and new value `value`. See the [edit example](examples/audio_sequence_field_edits.example.json) for the document format.

Run from the root of the copy containing both source and local resources:

```powershell
python -B -m tools.high_level_rom.audio_sequence_asset_editor --edits ./sequence-edits.json --output ./stateful_event_views.json
```

The output contains the updated files and a summary of changed positions and shared views. Review the result, copy the new files to the matching paths in the local copy, and follow the [build instructions](../../README.en.md).
