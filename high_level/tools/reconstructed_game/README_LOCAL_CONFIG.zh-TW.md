# 生成桌面執行配置

[简体中文](README_LOCAL_CONFIG.md) · **繁體中文** · [日本語](README_LOCAL_CONFIG.ja.md) · [English](README_LOCAL_CONFIG.en.md)

[`local_config.py`](local_config.py) 將明確的本地輸入寫成 `g5510-reconstructed-game-config-v2`。本地執行目錄包含本版原始碼、`scene-sources.json`、`resources/`、`assets/` 和 `build/`；Scene 清單的單一素材根為 `.`。

本地執行目錄可由[原始碼準備工具](../high_level_rom/README_GAME_SOURCE_STAGE.zh-TW.md)生成。配置輸入包括本版的 M68K 和 Z80 建置輸出、用外接 YMFM 原始碼和[音訊橋建置工具](../high_level_audio_engine/README_YMFM.zh-TW.md)生成的晶片庫、完整硬體 JSON，以及呼叫方配置的按鍵、時序、PCM 和存檔。兩種 CPU 可使用同一次本版[完整建置](../high_level_rom/README_BUILD.zh-TW.md)的目錄。`runtime.high-level.example.json` 展示欄位結構；實際執行配置提供與本次會話一致的硬體事件。

```powershell
python -B -X utf8 -m tools.reconstructed_game.local_config --edition-root . --settings runtime-inputs/gameplay.json --m68k-native-root build/python-image --sound-native-root build/python-image --chip-library build/host-ymfm/g5510_ymfm.dll --inputs runtime-inputs/hardware.json --save-path runtime-inputs/current-save.srm --run-output build/play --output build/play-config.json --frontend window
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend window
```

`--frontend console` 使用帶完整 `frontend.frame_plan` 的設定。`--run-output` 和 `--output` 是位於 `build/` 內的新增路徑。診斷目錄及可選 PCM 檔案從執行輸出名派生。

| 存檔形狀 | 引數 |
| --- | --- |
| `save.path` | `--save-path` 指向本版內已有的 8192 位元組介質；配置沿用讀寫許可權。 |
| `save.initial_byte` | 用明確的 0–255 初始位元組建立新邏輯介質；此形狀使用 `initial_byte`、`readable` 和 `writable`。 |

`materialize_local_gameplay_config(...)` 提供等價 Python 介面。配置生成負責路徑與結構，遊戲載入負責實際資源、硬體和程式資料。
