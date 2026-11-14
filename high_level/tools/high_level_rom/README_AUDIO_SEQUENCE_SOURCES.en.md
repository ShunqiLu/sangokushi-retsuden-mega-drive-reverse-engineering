# Named audio sequence commands

[简体中文](README_AUDIO_SEQUENCE_SOURCES.md) · [繁體中文](README_AUDIO_SEQUENCE_SOURCES.zh-TW.md) · [日本語](README_AUDIO_SEQUENCE_SOURCES.ja.md) · **English**

`audio_sequence_sources.py` gives names to parameters of the original fixed-width sound events. The complete audio document uses `g5510-named-audio-sequence-commands-v1`, and view members use `g5510-named-stateful-sequence-views-v1`. The original registry defines event sharing and read order.

| Parameter category | Original representation |
| --- | --- |
| Pan, detune, attenuation, key-off delay | A BYTE each |
| LFO pan and relative or absolute register operations | Register selection and following BYTE |
| Timer A and timer B | Timer A low and high BYTEs and timer B BYTE |
| Instruments | Bit 7 of the selection BYTE determines the external command parameter |
| Jumps, calls, and loops | Original little-endian target address, BYTE counter index and count |
| Delay multiplier, transpose, and mode | Original BYTE; the sound driver interprets two's complement |
| Unknown extended command parameters | `unknown_argument_bytes`, kept in the original order |

## Export and editing

`export` produces a standalone named document from the full typed document or resource graph. The graph supplies the matching `--source-root`. Feed existing standalone named files directly to `edit`. Write output to a new file under existing `build/`.

```powershell
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources export --source "$resources/resources/audio/audio_build.json" --source-root $resources --project-root . --output build/audio-sequences.named.json
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources edit --source build/audio-sequences.named.json --edits audio-command-edits.json --project-root . --output build/audio-sequences.edited.json
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources import --source build/audio-sequences.edited.json --project-root . --output build/audio-sequences.typed.json
```

Edits use `g5510-named-audio-command-parameter-edits-v1`. Each `view` includes `id`, `address`, `rom_offset`, `reader`, `raw_frequency`, and `slide` from the original view. `expected_parameters` is the full current parameter object, and `parameters` is the full new object of the same shape.

`with_command_parameters(document, edits)` applies validated unique edits, preserving command type, parameter shape, size, and physical allocation. `to_named` and `from_named` convert between representations. `tools.high_level_rom.export_media --named-audio-sequences` creates named external audio sources.
