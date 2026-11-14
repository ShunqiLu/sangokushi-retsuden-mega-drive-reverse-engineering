# Desktop configuration

[简体中文](README_LOCAL_CONFIG.md) · [繁體中文](README_LOCAL_CONFIG.zh-TW.md) · [日本語](README_LOCAL_CONFIG.ja.md) · **English**

[`local_config.py`](local_config.py) writes a `g5510-reconstructed-game-config-v2` from explicit local inputs. The run directory contains this edition's source, `scene-sources.json`, `resources/`, `assets/`, and `build/`. The Scene manifest uses `.` as its single resource root.

Use the [source staging tool](../high_level_rom/README_GAME_SOURCE_STAGE.en.md) to prepare the run directory. Supply this edition's M68K and Z80 build outputs, a chip library made from external YMFM sources with the [audio bridge builder](../high_level_audio_engine/README_YMFM.en.md), complete hardware JSON, and settings for controls, timing, PCM, and saves. Both CPU inputs can come from the same [full build](../high_level_rom/README_BUILD.en.md). See `runtime.high-level.example.json` for the settings format. A real run needs hardware events appropriate to its session.

```powershell
python -B -X utf8 -m tools.reconstructed_game.local_config --edition-root . --settings runtime-inputs/gameplay.json --m68k-native-root build/python-image --sound-native-root build/python-image --chip-library build/host-ymfm/g5510_ymfm.dll --inputs runtime-inputs/hardware.json --save-path runtime-inputs/current-save.srm --run-output build/play --output build/play-config.json --frontend window
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend window
```

`--frontend console` needs a complete `frontend.frame_plan`. `--run-output` and `--output` must be fresh paths under `build/`. The run output name determines the diagnostics directory and optional PCM paths.

| Save form | Fields |
| --- | --- |
| `save.path` | `--save-path` points to an existing 8192-byte medium in this edition. Its read/write permissions carry over. |
| `save.initial_byte` | Creates a logical medium with an explicit initial byte from 0 to 255. Uses `initial_byte`, `readable`, and `writable`. |

`materialize_local_gameplay_config(...)` provides the equivalent Python interface. Configuration generation handles paths and structure. The game loader handles resources, hardware, and program data.
