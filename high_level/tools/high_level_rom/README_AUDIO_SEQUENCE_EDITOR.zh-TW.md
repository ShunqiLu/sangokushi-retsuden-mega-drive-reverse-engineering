# 編輯共享樂譜事件

[简体中文](README_AUDIO_SEQUENCE_EDITOR.md) · **繁體中文** · [日本語](README_AUDIO_SEQUENCE_EDITOR.ja.md) · [English](README_AUDIO_SEQUENCE_EDITOR.en.md)

此工具在本地執行目錄讀取 `resources/audio/audio_build.json` 和 `assets/audio/`，按當前版本的登記與編碼核對編輯。編輯檔案的形狀見[欄位示例](examples/audio_sequence_field_edits.example.json)；`view_id` 和 `expected` 來自當前 `assets/audio/shared/stateful_event_views.json`。

```powershell
New-Item -ItemType Directory -Path build/audio-sequence-edit
python -B -X utf8 -m tools.high_level_rom.audio_sequence_asset_editor --edits audio-edits.json --output build/audio-sequence-edit/stateful_event_views.json
```

編輯欄位為 `note`（`0x80..0xDF`）以及 `fm_attenuation.attenuation_byte`、`fine_detune.fine_detune_byte` 和 `pan.pan_byte`。各欄位使用原驅動的位元組單位，命令寬度、時值和控制流保持原結構。

輸出包含候選事件檔案和對應的 `stateful_event_views.edit-receipt.json`。結果列出不同的編碼位元組，以及讀取或預讀這些位元組的檢視。以候選作為素材中的同名成員，可參加[正常建置](README_BUILD.zh-TW.md)。
