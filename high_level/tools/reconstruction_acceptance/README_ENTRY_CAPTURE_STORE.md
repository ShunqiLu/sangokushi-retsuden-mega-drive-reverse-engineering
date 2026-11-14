# 入口采集文件存储

[`EntryCaptureStore`](entry_capture_store.py) 在显式的新输出目录保存入口初态。构造参数给出记录数、总字节、单项元数据与保留空间上限。记录路径使用唯一名称。

| 方法 | 保存内容 |
| --- | --- |
| `write_case` | 入口元数据和原 RAM 字节。 |
| `write_vdp_state` | 带 VDP 状态的入口记录。 |
| `write_readonly_source` | 同会话的只读数据源及其元数据。 |
| `close(outcome)` | 写入 `capture-receipt.json`，描述已写结果与预算边界。 |

原入口、角色、来源和捕获位置保存在记录元数据中。资源容量耗尽时停止写入采集，应用使用自身的运行资源继续执行。
