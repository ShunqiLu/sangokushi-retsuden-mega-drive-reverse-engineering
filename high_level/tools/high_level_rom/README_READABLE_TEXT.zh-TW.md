# 中文對話、武將名與城市名

[简体中文](README_READABLE_TEXT.md) · **繁體中文** · [日本語](README_READABLE_TEXT.ja.md) · [English](README_READABLE_TEXT.en.md)

[`readable_text.py`](readable_text.py) 將 typed 文字轉換為 `g5510-owned-main-text-unicode-source-v1`。字元由 [低段字形表](text_sources/glyphs_lower.json) 與 [高段字形表](text_sources/glyphs_upper.json) 對映；重碼、未知圖形及非規範控制值用四位大寫十六進位制 `⟦XXXX⟧` 精確表示。

對話保留原文字槽與各個控制 WORD 的位置和值，含末尾恢復控制。對話中的 `0000` 是圖形操作，`4000` 對應字形 0；名稱中的 `0000` 對應字形 0。武將名佔 3 WORD，城市名佔 2 WORD。

`export` 使用含 typed 文字的素材根 `$typedResources`；已有可讀文件可直接作為 `edit --source` 的輸入。輸出寫入已有 `build/` 下的新檔案。

```powershell
python -B -X utf8 -m tools.high_level_rom.readable_text export --project-root . --source "$typedResources/resources/data/dialogue_text.json" --glyph-sources tools/high_level_rom/text_sources/glyphs_lower.json tools/high_level_rom/text_sources/glyphs_upper.json --output build/dialogue-readable.json
python -B -X utf8 -m tools.high_level_rom.readable_text edit --project-root . --source build/dialogue-readable.json --edits text-edits.json --output build/dialogue-edited.json
```

編輯檔案格式為 `g5510-main-text-record-edits-v1`，包含 `format` 與 `edits`。各項透過 `collection` 和 `id` 定位實際記錄，提供原完整 `expected_text` 和新 `text`。批處理核對固定 WORD 數和控制符，返回獨立文件。Python 呼叫可使用 `with_text_edits`；`MainTextWordCodec` 執行字元與精確 WORD 的轉換。
