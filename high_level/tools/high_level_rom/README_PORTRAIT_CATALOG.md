# 头像索引生成器

[`portrait_catalog.py`](portrait_catalog.py) 将可读武将姓名、剧本记录、头像布局、调色板与共享图块连成查找索引。输出中的 `officers` 支持姓名和记录 ID 查找，`shared_tiles` 指出共同使用的图像成员。记录与画面之间的已知连线及待定身份各用原状态表示。

```powershell
python -B -X utf8 -m tools.high_level_rom.portrait_catalog --project-root . --names-source "$resources/resources/data/dialogue_text.json" --portrait-source "$resources/resources/images/portrait_graphics.json" --record-authority "$resources/resources/data/scenario_build.json" --source-root $resources --output build/officer-portraits.json
```

`--names-source` 使用[可读文字源](README_READABLE_TEXT.md)，可直接指向素材根中的具名对话文件；`--source-root` 用于解析实际头像成员。新的索引文件写在项目的 `build/` 内。[头像编辑指南](../../PORTRAITS.md)说明如何从索引定位真正的编辑源。
