# M68K 程序数据

**简体中文** · [繁體中文](README_COMPILED_CODE_DATA.zh-TW.md) · [日本語](README_COMPILED_CODE_DATA.ja.md) · [English](README_COMPILED_CODE_DATA.en.md)

原游戏的程序复制及校验逻辑使用当前卡带构建生成的指令数据。[`compiled_code_data.py`](compiled_code_data.py) 提供从本版源码构建读取这些数据的接口：

```python
from tools.high_level_rom.compiled_code_data import load_high_level_m68k_copy_data

data, details = load_high_level_m68k_copy_data(project_root, native_build_root)
```

输入是明确的源码目录和 [镜像构建](README_BUILD.md) 输出目录。返回 `ReadOnlyData` 和描述对象。加载核对生成汇编、各组 ELF 和实际指令间的对应，按登记选取完整指令并检查共享别名。原游戏用此只读视图读取计入校验和的程序字节。

[`m68k_correspondence.py`](m68k_correspondence.py) 负责 GNU 符号、常量、PC 相对地址及 Capstone 指令显示之间的有限对应。代码地址使用各组登记的原卡带位置。桌面运行的组合方式见[程序数据与运行入口](../reconstructed_game/README_HIGH_LEVEL_NATIVE_ENTRY.md)。
