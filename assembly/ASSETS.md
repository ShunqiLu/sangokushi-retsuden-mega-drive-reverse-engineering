# 兼容素材包

**简体中文** · [繁體中文](ASSETS.zh-TW.md) · [日本語](ASSETS.ja.md) · [English](ASSETS.en.md)

素材包以 `resources/` 和 `assets/` 为两条入口。前者登记资源格式和成员关系；后者保存实际图块、布局、音色、声道事件和其他数据。把这两个目录的共同父目录传给构建参数 `--resource-root`。

```text
本地素材根/
  resources/
    audio/
    data/
    images/
  assets/
    audio/
    images/
```

| 编辑主题 | 素材包中的入口 |
| --- | --- |
| 标题图像 | `resources/images/graphics_build.json`、`assets/images/title/` |
| 战斗地图布局与底图 | `resources/images/battle_graphics.json` |
| 武将头像和调色板 | `resources/images/portrait_graphics.json`、`assets/images/portraits/` |
| 字形 | `resources/images/font_build.json`、`assets/images/fonts/` |
| 曲目、音效和状态事件 | `resources/audio/audio_build.json`、`assets/audio/` |
| 剧本和对话 | `resources/data/scenario_build.json`、`resources/data/dialogue_text.json` |

已提供素材清单时，可用[索引工具](tools/reconstruction_delivery/README_MEDIA_CATALOG.md)查找字段和文件。索引 PNG 的颜色编号是编码输入，游戏配色来自配套调色文件。
