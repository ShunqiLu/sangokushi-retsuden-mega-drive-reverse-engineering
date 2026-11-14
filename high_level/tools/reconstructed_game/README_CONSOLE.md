# 交互式控制台

控制台使用相同的桌面游戏应用。配置提供完整 `frontend.frame_plan`，以 `--frontend console` 启用。

```powershell
python -B -X utf8 -m tools.reconstructed_game --config build/play-config.json --frontend console
```

## JSON 行协议

stdin 每行一个 UTF-8 JSON 对象，含换行最多 65,536 字节。stdout 的每条回复也是一个 JSON 对象，`status` 表示 `ready`、`ok`、`protocol_error`、`boundary` 或 `closed`。

`ready` 给出 `declared_ports`、`live_pad_ports` 与 `fixed_pad_snapshots`。端口从 0 编号；按键为 `up`、`down`、`left`、`right`、`a`、`b`、`c` 和 `start`。每次 `advance` 提供所有声明端口的完整电平；空数组表示释放该端口全部按键。

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

| 命令 | 结果 |
| --- | --- |
| `advance` | 按完整按键状态推进明确数量的帧。 |
| `capture` | 将当前渲染写为新的 PNG。 |
| `observe` | 读取当前等待、运行计数及明确的内存字段。 |
| `observe_palette` | 读取实际 CRAM、FB00／FB80 调色板工作区和 VDP 寄存器。 |
| `export_save` | 将当前真实 8192 字节 SRAM 导出为新文件。 |
| `extend_frames` | 正常耗尽帧额度之后，通过 `new_total` 指定更高总帧数。 |
| `close` | 退出当前游戏会话并释放设备。 |

截图和导出使用诊断目录内的新文件名。`extend_frames` 保留当前游戏、连续帧号和各设备的剩余供应。Python 接口为 `run_console(app, config, input_stream=..., output_stream=...)`。
