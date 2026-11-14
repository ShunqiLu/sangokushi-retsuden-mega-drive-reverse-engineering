# Chinese dialogue and officer and city names

[简体中文](README_READABLE_TEXT.md) · [繁體中文](README_READABLE_TEXT.zh-TW.md) · [日本語](README_READABLE_TEXT.ja.md) · **English**

[`readable_text.py`](readable_text.py) converts typed text into `g5510-owned-main-text-unicode-source-v1`. The [lower glyph table](text_sources/glyphs_lower.json) and [upper glyph table](text_sources/glyphs_upper.json) map characters. Duplicate encodings, unknown glyphs, and noncanonical controls use the exact four-digit uppercase hexadecimal escape `⟦XXXX⟧`.

Dialogue preserves original text slots and the position and value of each control WORD, including the trailing restore control. In dialogue, `0000` is a graphics operation and `4000` maps to glyph 0. In names, `0000` maps to glyph 0. Officer names use 3 WORDs and city names use 2.

`export` uses resource root `$typedResources` containing typed text. Pass an existing readable document directly to `edit --source`. Write to a new file under existing `build/`.

```powershell
python -B -X utf8 -m tools.high_level_rom.readable_text export --project-root . --source "$typedResources/resources/data/dialogue_text.json" --glyph-sources tools/high_level_rom/text_sources/glyphs_lower.json tools/high_level_rom/text_sources/glyphs_upper.json --output build/dialogue-readable.json
python -B -X utf8 -m tools.high_level_rom.readable_text edit --project-root . --source build/dialogue-readable.json --edits text-edits.json --output build/dialogue-edited.json
```

The edit format is `g5510-main-text-record-edits-v1` with `format` and `edits`. Use `collection` and `id` to locate each record and supply its full original `expected_text` and new `text`. Batch editing checks fixed WORD counts and controls, then returns a separate document. In Python, use `with_text_edits`; `MainTextWordCodec` converts characters and exact WORDs.
