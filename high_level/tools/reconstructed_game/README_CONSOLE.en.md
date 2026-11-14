# Interactive console

[简体中文](README_CONSOLE.md) · [繁體中文](README_CONSOLE.zh-TW.md) · [日本語](README_CONSOLE.ja.md) · **English**

The console uses the same desktop game application. Supply a complete `frontend.frame_plan` in the configuration and start it with `--frontend console`.

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend console
```

## JSON lines protocol

Each stdin line is one UTF-8 JSON object, up to 65,536 bytes including the newline. Each stdout reply is also one JSON object. `status` is `ready`, `ok`, `protocol_error`, `boundary`, or `closed`.

`ready` provides `declared_ports`, `live_pad_ports`, and `fixed_pad_snapshots`. Ports are zero-based. Buttons are `up`, `down`, `left`, `right`, `a`, `b`, `c`, and `start`. Each `advance` gives the full button state of every declared port. An empty array releases every button on that port.

```jsonl
{"command":"advance","frames":120,"pads":[{"port":0,"buttons":[]}]}
{"command":"advance","frames":1,"pads":[{"port":0,"buttons":["start"]}]}
{"command":"advance","frames":4,"pads":[{"port":0,"buttons":[]}]}
{"command":"capture","file":"after-start.png"}
{"command":"observe"}
{"command":"observe_palette"}
{"command":"export_save","file":"current-sram.srm"}
{"command":"close"}
```

| Command | Result |
| --- | --- |
| `advance` | Advance the requested number of frames with the full button state. |
| `capture` | Write the current render to a new PNG. |
| `observe` | Read the current wait, runtime counters, and specified memory fields. |
| `observe_palette` | Read live CRAM, FB00/FB80 palette workspaces, and VDP registers. |
| `export_save` | Export the current 8192-byte SRAM to a new file. |
| `extend_frames` | After the frame allowance runs out normally, use `new_total` to set a higher total. |
| `close` | Exit the current game session and release devices. |

Use new filenames in the diagnostics directory for screenshots and exports. `extend_frames` keeps the current game, sequential frame numbers, and remaining device supplies. The Python interface is `run_console(app, config, input_stream=..., output_stream=...)`.
