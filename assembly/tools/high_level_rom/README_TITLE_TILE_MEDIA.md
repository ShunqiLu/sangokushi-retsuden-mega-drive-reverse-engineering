# 标题图像

**简体中文** · [繁體中文](README_TITLE_TILE_MEDIA.zh-TW.md) · [日本語](README_TITLE_TILE_MEDIA.ja.md) · [English](README_TITLE_TILE_MEDIA.en.md)

标题资料由 `resources/images/graphics_build.json` 登记；像素成员保存在 `assets/images/title/rle_tiles/`。每张 8×8 索引 PNG 定义一个图块，`commands.json` 保存压缩控制和图块引用。编辑后维持图块尺寸、索引调色板、重复段和原槽长度。

素材根的图像与命令会由登记的编码器重新组合。若手头已有兼容的结构化素材，可通过素材导出工具生成外置 PNG 和 JSON。用 `python -B -m tools.high_level_rom.export_media --help` 查看导出参数。
