# M68K 程式資料

[简体中文](README_COMPILED_CODE_DATA.md) · **繁體中文** · [日本語](README_COMPILED_CODE_DATA.ja.md) · [English](README_COMPILED_CODE_DATA.en.md)

原遊戲的程式複製及校驗邏輯使用當前卡匣建置生成的指令資料。[`compiled_code_data.py`](compiled_code_data.py) 提供從本版原始碼建置讀取這些資料的介面：

```python
from tools.high_level_rom.compiled_code_data import load_high_level_m68k_copy_data

data, details = load_high_level_m68k_copy_data(project_root, native_build_root)
```

輸入是明確的原始碼目錄和 [映象建置](README_BUILD.zh-TW.md) 輸出目錄。返回 `ReadOnlyData` 和描述物件。載入核對生成彙編、各組 ELF 和實際指令間的對應，按登記選取完整指令並檢查共享別名。原遊戲用此只讀檢視讀取計入校驗和的程式位元組。

[`m68k_correspondence.py`](m68k_correspondence.py) 負責 GNU 符號、常量、PC 相對地址及 Capstone 指令顯示之間的有限對應。程式碼地址使用各組登記的原卡匣位置。桌面執行的組合方式見[程式資料與執行入口](../reconstructed_game/README_HIGH_LEVEL_NATIVE_ENTRY.zh-TW.md)。
