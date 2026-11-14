# AI 命令阈值

**简体中文** · [繁體中文](README_AI_POLICY_SOURCES.zh-TW.md) · [日本語](README_AI_POLICY_SOURCES.ja.md) · [English](README_AI_POLICY_SOURCES.en.md)

资源 `ai_threshold_pair_fields` 包含三组各 15 对主表阈值与 3 对次表阈值，共 48 对无符号 WORD。每对使用 `first_cutoff_word` 和 `second_cutoff_word`。主表首 WORD 还供城防目标规划使用，因此编辑该值会影响这两个调用。

业务逻辑以原顺序读取两张表，按无符号比较选择原分支。组号与对号表示表中的物理位置。相等、逆序和完整的 0–65535 值均属于有效源数据。

## 文件命令

以下导出使用含 typed 源的素材根 `$typedResources`。已有具名源可直接作为 `edit --source` 的输入。输出写入已有 `build/` 下的新文件。

```powershell
python -B -m tools.high_level_rom.ai_policy_sources export --source "$typedResources/resources/data/ai_threshold_pair_fields.json" --project-root . --output build/ai-cutoffs.named.json
python -B -m tools.high_level_rom.ai_policy_sources edit --source build/ai-cutoffs.named.json --edits cutoff-edits.json --project-root . --output build/ai-cutoffs.edited.json
python -B -m tools.high_level_rom.ai_policy_sources import --source build/ai-cutoffs.edited.json --project-root . --output build/ai-cutoffs.typed.json
```

具名格式为 `g5510-named-ai-command-cutoffs-v1`。编辑文件使用 `g5510-ai-command-cutoff-pair-edits-v1`，含 `format` 与 `edits`。每项含 `table`、`pair_index`、`field`、`expected_word`、`word`；主表另外提供 `group_index`（0–2）。主表对号为 0–14，次表为 0–2。编辑以当前完整源值为准，输出写到新的 JSON。

Python 接口 `to_named` 和 `from_named` 处理表示转换，`with_cutoff_pairs(source, edits)` 返回独立编辑文档。具名、原结构和叠加登记的用法见[资源清单](README_SCENE_SOURCE_PUBLICATION.md)。
