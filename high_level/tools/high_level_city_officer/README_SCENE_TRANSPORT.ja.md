# 実行シーンの輸送命令

[简体中文](README_SCENE_TRANSPORT.md) · [繁體中文](README_SCENE_TRANSPORT.zh-TW.md) · **日本語** · [English](README_SCENE_TRANSPORT.en.md)

[`business_scene_transport.py`](business_scene_transport.py) は輸送方向、経路の進行、衝突、到着を扱います。現在のシーンがマップ、隣接座標、輸送レコードを供給し、ルールは同じ実行状態を読み書きします。到着時は元のフィールド幅で都市に資源を加算し、原作の周回と上限処理を維持します。

オフラインの [CE00 輸送命令ビュー](../save_data/README_CAMPAIGN_ORDERS.ja.md) はセーブでの表現を扱います。実行時のフラグ、速度、積荷はシーン状態が供給します。
