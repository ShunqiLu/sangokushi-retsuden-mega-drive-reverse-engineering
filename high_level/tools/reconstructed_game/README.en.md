# Desktop game

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **English**

[`tools.reconstructed_game`](__main__.py) uses the same game application for scenes, input, graphics, audio, and saves. The Tk window displays the game image. The console exposes the same resumable session through a JSON lines protocol.

## Launch

The [local configuration guide](README_LOCAL_CONFIG.en.md) covers the source tree, resources, program data, sound chip library, device inputs, and saves. Launch with a prepared configuration:

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend window
```

`--frontend console` enables the [console](README_CONSOLE.en.md) and requires a full frame plan. Set `--session-output` to a fresh session path under `build/` in the configuration root.

## Configuration

- [Application interface and PCM](README_APPLICATION.en.md), [Optional speaker output](README_SPEAKERS.en.md).
- [Full frame plan](README_FRAME_PLAN.en.md), [Hardware inputs](README_HARDWARE_INPUTS.en.md), [Input capacities](README_HARDWARE_PROFILE.en.md).
- [Ordered intro and scenario restarts](README_ORDERED_RESTARTS.en.md), [Cold and warm paths](README_ORDERED_COLD_PLAN.en.md).
- [Optional entry capture](README_ENTRY_CAPTURE.en.md).

Each stage consumes the configured device events and quantities. The application keeps the same physical frame and save medium. If a device supply runs out, it reports the corresponding runtime boundary.
