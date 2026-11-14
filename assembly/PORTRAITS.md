# 编辑武将头像

**简体中文** · [繁體中文](PORTRAITS.zh-TW.md) · [日本語](PORTRAITS.ja.md) · [English](PORTRAITS.en.md)

[头像索引工具](tools/high_level_rom/README_PORTRAIT_CATALOG.md)以文字、头像和剧本三个来源建立人物索引。查找索引中的 `name.text` 或 `officer_record_id`，随后跟随布局、调色板和图块引用编辑实际素材。共享图块对应多个人物。

素材根提供以下入口：

- `resources/data/dialogue_text.json`：武将姓名。
- `resources/images/portrait_graphics.json`：头像布局、调色板和外置 PNG 引用。
- `resources/data/scenario_build.json`：剧本与人物记录。
