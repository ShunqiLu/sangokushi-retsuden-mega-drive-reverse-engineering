# Shared score event editor

[简体中文](README_AUDIO_SEQUENCE_EDITOR.md) · [繁體中文](README_AUDIO_SEQUENCE_EDITOR.zh-TW.md) · [日本語](README_AUDIO_SEQUENCE_EDITOR.ja.md) · **English**

The tool reads `resources/audio/audio_build.json` and `assets/audio/` from the local run directory and checks edits against this edition's registry and encoding. See the [field edit example](examples/audio_sequence_field_edits.example.json) for the format. `view_id` and `expected` come from the current `assets/audio/shared/stateful_event_views.json`.

```powershell
New-Item -ItemType Directory -Path build/audio-sequence-edit
python -B -X utf8 -m tools.high_level_rom.audio_sequence_asset_editor --edits audio-edits.json --output build/audio-sequence-edit/stateful_event_views.json
```

Edit fields are `note` (`0x80..0xDF`), `fm_attenuation.attenuation_byte`, `fine_detune.fine_detune_byte`, and `pan.pan_byte`. Fields use the driver's original byte units; command widths, durations, and control flow stay in their original form.

Output includes the candidate event file and its `stateful_event_views.edit-receipt.json`. It lists changed bytes and views that read or prefetch them. Use the candidate in place of the identically named resource file for the [standard build](README_BUILD.en.md).
