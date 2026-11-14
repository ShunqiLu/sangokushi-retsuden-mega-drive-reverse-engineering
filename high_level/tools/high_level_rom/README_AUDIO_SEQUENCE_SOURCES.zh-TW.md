# 具名音訊序列命令

[简体中文](README_AUDIO_SEQUENCE_SOURCES.md) · **繁體中文** · [日本語](README_AUDIO_SEQUENCE_SOURCES.ja.md) · [English](README_AUDIO_SEQUENCE_SOURCES.en.md)

`audio_sequence_sources.py` 在原定寬聲音事件上提供具名引數。完整音訊文件格式為 `g5510-named-audio-sequence-commands-v1`，檢視成員格式為 `g5510-named-stateful-sequence-views-v1`。物理事件與檢視的共享關係及讀取順序由原登記源提供。

| 引數類別 | 原始表示 |
| --- | --- |
| 聲像、微調、衰減、斷音延遲 | 各自的 BYTE |
| LFO 聲像、相對或絕對暫存器動作 | 暫存器選擇及後繼 BYTE |
| Timer A、Timer B | Timer A 低／高 BYTE 與 Timer B BYTE |
| 樂器 | 選擇 BYTE 的 bit 7 決定外部命令引數 |
| 跳轉、呼叫與迴圈 | 原小端目標地址、BYTE 計數器索引與次數 |
| 延時倍數、移調與模式設定 | 保留原 BYTE，補碼由聲音驅動解釋 |
| 擴充套件命令的未知引數 | `unknown_argument_bytes`，按原順序保留 |

## 匯出與編輯

`export` 從完整 typed 文件或素材圖生成獨立的具名文件；素材圖提供對應的 `--source-root`。已有獨立具名文件可直接用於 `edit`。輸出寫入已有 `build/` 下的新檔案。

```powershell
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources export --source "$resources/resources/audio/audio_build.json" --source-root $resources --project-root . --output build/audio-sequences.named.json
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources edit --source build/audio-sequences.named.json --edits audio-command-edits.json --project-root . --output build/audio-sequences.edited.json
python -B -X utf8 -m tools.high_level_rom.audio_sequence_sources import --source build/audio-sequences.edited.json --project-root . --output build/audio-sequences.typed.json
```

編輯檔案格式為 `g5510-named-audio-command-parameter-edits-v1`。每項的 `view` 包含原檢視的 `id`、`address`、`rom_offset`、`reader`、`raw_frequency` 和 `slide`。`expected_parameters` 是當前完整引數物件，`parameters` 是保持同型的新完整物件。

`with_command_parameters(document, edits)` 應用已核對的唯一目標，並保持命令種類、引數結構、尺寸和物理分配。`to_named` 與 `from_named` 負責表示轉換。使用 `tools.high_level_rom.export_media --named-audio-sequences` 可生成具名的外接音訊源。
