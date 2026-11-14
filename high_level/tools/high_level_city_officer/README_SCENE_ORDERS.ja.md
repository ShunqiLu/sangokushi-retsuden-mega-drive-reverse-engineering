# 都市命令・勢力関係・資源

[简体中文](README_SCENE_ORDERS.md) · [繁體中文](README_SCENE_ORDERS.zh-TW.md) · **日本語** · [English](README_SCENE_ORDERS.en.md)

[`business_scene_orders.py`](business_scene_orders.py) は都市命令の実行状態、外交協定、資源決済を扱います。完全なフレームには都市、勢力、選択命令、呼び出しのコンテキストが含まれます。ルールは実際の都市・関係レコードに従って資源と条件コードを更新します。

関係行は勢力を表す WORD ビットマップを使い、レコードの方向に従って読み込みます。主資源と副資源は各自の物理スロット、フィールド幅、乗除算の挙動を維持します。オフラインの初期値と勢力関係は[名前付きシナリオ](../high_level_rom/README_NAMED_SCENARIO_SOURCES.ja.md)を参照してください。
