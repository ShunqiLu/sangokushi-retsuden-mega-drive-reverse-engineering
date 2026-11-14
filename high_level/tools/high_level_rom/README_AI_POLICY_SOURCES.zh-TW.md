# AI 命令閾值

[简体中文](README_AI_POLICY_SOURCES.md) · **繁體中文** · [日本語](README_AI_POLICY_SOURCES.ja.md) · [English](README_AI_POLICY_SOURCES.en.md)

資源 `ai_threshold_pair_fields` 包含三組各 15 對主表閾值與 3 對次表閾值，共 48 對無符號 WORD。每對使用 `first_cutoff_word` 和 `second_cutoff_word`。主表首 WORD 還供城防目標規劃使用，因此編輯該值會影響這兩個呼叫。

業務邏輯以原順序讀取兩張表，按無符號比較選擇原分支。組號與對號表示表中的物理位置。相等、逆序和完整的 0–65535 值均屬於有效源資料。

## 檔案命令

以下匯出使用含 typed 源的素材根 `$typedResources`。已有具名源可直接作為 `edit --source` 的輸入。輸出寫入已有 `build/` 下的新檔案。

```powershell
python -B -m tools.high_level_rom.ai_policy_sources export --source "$typedResources/resources/data/ai_threshold_pair_fields.json" --project-root . --output build/ai-cutoffs.named.json
python -B -m tools.high_level_rom.ai_policy_sources edit --source build/ai-cutoffs.named.json --edits cutoff-edits.json --project-root . --output build/ai-cutoffs.edited.json
python -B -m tools.high_level_rom.ai_policy_sources import --source build/ai-cutoffs.edited.json --project-root . --output build/ai-cutoffs.typed.json
```

具名格式為 `g5510-named-ai-command-cutoffs-v1`。編輯檔案使用 `g5510-ai-command-cutoff-pair-edits-v1`，含 `format` 與 `edits`。每項含 `table`、`pair_index`、`field`、`expected_word`、`word`；主表另外提供 `group_index`（0–2）。主表對號為 0–14，次表為 0–2。編輯以當前完整源值為準，輸出寫到新的 JSON。

Python 介面 `to_named` 和 `from_named` 處理表示轉換，`with_cutoff_pairs(source, edits)` 返回獨立編輯文件。具名、原結構和疊加登記的用法見[資源清單](README_SCENE_SOURCE_PUBLICATION.zh-TW.md)。
