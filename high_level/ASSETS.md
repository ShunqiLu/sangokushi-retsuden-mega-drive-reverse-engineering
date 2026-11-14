# 图像、音频与剧本素材

**简体中文** · [繁體中文](ASSETS.zh-TW.md) · [日本語](ASSETS.ja.md) · [English](ASSETS.en.md)

`--resource-root` 指向一份兼容的本地素材目录。下面的路径相对该目录；源码中的构建器按资源 ID 读取登记文件，再解析对应的外置成员。

| 路径 | 用途 |
| --- | --- |
| `resources/images/` | 图块、地图、精灵、字体、头像、调色板及布局的登记源 |
| `assets/images/` | 可编辑索引 PNG、地图成员、布局和调色板 |
| `resources/audio/` | Z80 声音驱动使用的乐谱、音色和外部事件登记源 |
| `assets/audio/` | 音符、控制事件、包络、音色及共享声音成员 |
| `resources/data/` | 剧本初值、AI 参数、文字和其他规则表 |

素材清单 `asset-source-manifest.json` 描述资源 ID、引用和编辑字段。`ASSET_INDEX.json` 提供按文件搜索的派生视图；[索引工具](tools/reconstruction_delivery/README_MEDIA_CATALOG.md)可根据素材清单生成它。

## 图像

PNG 像素保存的是调色板索引，预览颜色用于辅助辨认。实际游戏颜色由对应的调色板源决定。编辑时保持图块尺寸、索引位宽和共享成员引用；布局的格坐标、翻转及优先级由布局工具处理。

- [战斗背景格与属性](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.md)、[战斗背景图块](tools/high_level_rom/README_BATTLE_TILE_SHEET.md)。
- [人物头像](PORTRAITS.md)、[标题图块](tools/high_level_rom/README_TITLE_TILE_MEDIA.md)。
- [共享图像与音频别名](tools/high_level_rom/README_MEDIA_ALIASES.md)。

## 声音

乐谱和音效由有序事件、音色、包络和共享成员组成。改动的对象是登记源及其成员；PCM 是音频芯片模型产生的播放输出。

- [音序与命令格式](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.md)、[共享事件编辑器](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.md)。
- [桌面 FM 音频与芯片时钟](tools/high_level_audio_engine/README_YMFM.md)。

## 规则数据

[具名剧本](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.md)、[AI 阈值](tools/high_level_rom/README_AI_POLICY_SOURCES.md)、[候选资格](tools/high_level_rom/README_AI_SELECTION_SOURCES.md)和[可读文字](tools/high_level_rom/README_READABLE_TEXT.md)各有明确的编辑和编码规则。各资源使用其原字段宽度与布局。
