# 編輯共享樂譜事件

[简体中文](README_AUDIO_SEQUENCE_EDITOR.md) · **繁體中文** · [日本語](README_AUDIO_SEQUENCE_EDITOR.ja.md) · [English](README_AUDIO_SEQUENCE_EDITOR.en.md)

共享樂譜事件儲存在本地執行副本的 `assets/audio/shared/stateful_event_views.json`。一項編輯提供檢視 `view_id`、欄位 `field`、原值 `expected` 和新值 `value`；[編輯示例](examples/audio_sequence_field_edits.example.json)展示文件結構。

請從具備原始碼和本地素材的副本根目錄執行：

```powershell
python -B -m tools.high_level_rom.audio_sequence_asset_editor --edits ./sequence-edits.json --output ./stateful_event_views.json
```

輸出包括新素材和記錄變更位置及共享檢視的摘要。檢查後把新素材放回本地副本的對應路徑，再按[建置說明](../../README.zh-TW.md)編入卡匣。
