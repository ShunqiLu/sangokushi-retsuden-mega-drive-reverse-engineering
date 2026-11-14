# 编辑剧本初值

`resources/data/scenario_build.json` 保存三套剧本的城市、势力、武将及初始装备。具名视图提供资金、粮食、兵力、能力、归属和坐标等字段，地址键保留其原有范围和宽度。当前进度见[存档编辑](../save_data/README.md)。

`$resources` 是同时包含 `resources/` 和 `assets/` 的本地素材根。命令从汇编版根目录运行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.scenario_sources edit --source "$resources/resources/data/scenario_build.json" --edits ./scenario-edits.json --project-root . --output build/scenario.json
```

`edit` 接受具名剧本文档。装备的三个原始字节可用 `edit-equipment --edits` 按字段序号处理。`export` 将旧版结构化文档转为具名视图，`import` 转回旧版格式。每次使用新的输出文件核对结果，再放入本地素材副本。

`edit` 的输入为数组，每项填写 `scenario_id`、`group`、`record_id`、`field`、`expected_value` 和 `value`。城市资源的高低字结构保留原高字，编辑写入低字值。
