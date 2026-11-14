# 生成桌面运行配置

**简体中文** · [繁體中文](README_LOCAL_CONFIG.zh-TW.md) · [日本語](README_LOCAL_CONFIG.ja.md) · [English](README_LOCAL_CONFIG.en.md)

[`local_config.py`](local_config.py) 将明确的本地输入写成 `g5510-reconstructed-game-config-v2`。本地运行目录包含本版源码、`scene-sources.json`、`resources/`、`assets/` 和 `build/`；Scene 清单的单一素材根为 `.`。

本地运行目录可由[源码准备工具](../high_level_rom/README_GAME_SOURCE_STAGE.md)生成。配置输入包括本版的 M68K 和 Z80 构建输出、用外置 YMFM 源码和[音频桥构建工具](../high_level_audio_engine/README_YMFM.md)生成的芯片库、完整硬件 JSON，以及调用方配置的按键、时序、PCM 和存档。两种 CPU 可使用同一次本版[完整构建](../high_level_rom/README_BUILD.md)的目录。`runtime.high-level.example.json` 展示字段结构；实际运行配置提供与本次会话一致的硬件事件。

```powershell
python -B -X utf8 -m tools.reconstructed_game.local_config --edition-root . --settings runtime-inputs/gameplay.json --m68k-native-root build/python-image --sound-native-root build/python-image --chip-library build/host-ymfm/g5510_ymfm.dll --inputs runtime-inputs/hardware.json --save-path runtime-inputs/current-save.srm --run-output build/play --output build/play-config.json --frontend window
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend window
```

`--frontend console` 使用带完整 `frontend.frame_plan` 的设置。`--run-output` 和 `--output` 是位于 `build/` 内的新增路径。诊断目录及可选 PCM 文件从运行输出名派生。

| 存档形状 | 参数 |
| --- | --- |
| `save.path` | `--save-path` 指向本版内已有的 8192 字节介质；配置沿用读写权限。 |
| `save.initial_byte` | 用明确的 0–255 初始字节建立新逻辑介质；此形状使用 `initial_byte`、`readable` 和 `writable`。 |

`materialize_local_gameplay_config(...)` 提供等价 Python 接口。配置生成负责路径与结构，游戏加载负责实际资源、硬件和程序数据。
