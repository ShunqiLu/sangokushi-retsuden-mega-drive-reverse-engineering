# M68K プログラムデータ

[简体中文](README_COMPILED_CODE_DATA.md) · [繁體中文](README_COMPILED_CODE_DATA.zh-TW.md) · **日本語** · [English](README_COMPILED_CODE_DATA.en.md)

原作のプログラムコピーとチェックサム処理は、現在のカートリッジビルドの命令データを使います。[`compiled_code_data.py`](compiled_code_data.py) から、この版でビルドしたデータを読み込めます。

```python
from tools.high_level_rom.compiled_code_data import load_high_level_m68k_copy_data

data, details = load_high_level_m68k_copy_data(project_root, native_build_root)
```

ソースディレクトリと[カートリッジイメージのビルド](README_BUILD.ja.md)の出力先を指定します。ローダーは `ReadOnlyData` と記述オブジェクトを返します。生成アセンブリ、各グループの ELF、命令の対応を照合し、登録情報に従って命令全体を選び、共有する別名参照を確認します。この読み取り専用ビューから、チェックサム対象のプログラムバイトを読みます。

[`m68k_correspondence.py`](m68k_correspondence.py) は対応する GNU シンボル、定数、PC 相対アドレスを Capstone の命令表示に対応付けます。コードアドレスは各グループに登録された元のカートリッジ位置を使います。デスクトップでの構成は[プログラムデータと実行の入口](../reconstructed_game/README_HIGH_LEVEL_NATIVE_ENTRY.ja.md)を参照してください。
