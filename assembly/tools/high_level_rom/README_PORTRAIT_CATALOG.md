# 生成武将头像索引

工具将武将姓名、剧本记录及头像选择数据连接为索引。每项给出记录 ID、布局、共享图块和调色板引用。编辑时沿索引找到本地素材中的实际文件。

`$resources` 是同时包含 `resources/` 和 `assets/` 的本地素材根。命令从汇编版根目录运行。

```powershell
$resources = Read-Host '本地素材根目录'
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.high_level_rom.portrait_catalog --names-source "$resources/resources/data/dialogue_text.json" --portrait-source "$resources/resources/images/portrait_graphics.json" --record-authority "$resources/resources/data/scenario_build.json" --source-root $resources --project-root . --output build/portraits.json
```
