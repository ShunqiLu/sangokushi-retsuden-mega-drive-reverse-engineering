# オープニングとシナリオの順序付き再起動

[简体中文](README_ORDERED_RESTARTS.md) · [繁體中文](README_ORDERED_RESTARTS.zh-TW.md) · **日本語** · [English](README_ORDERED_RESTARTS.en.md)

フロントエンドは `--restarts` でオープニングとシナリオの再起動計画を指定します。アプリは実際のオープニング IRQ 分岐とシナリオ分岐で `plans` を消費し、同じセーブ媒体、シーン、デバイスの所有権を維持します。

```powershell
python -m tools.reconstructed_game --config build/play-config.json --restarts restart-plan.json
```

v1 はウォームリセットを指定し、v2 は [`warm` と `cold`](README_ORDERED_COLD_PLAN.ja.md) を明示的に扱います。`--restarts`、`--intro-restarts`、`--narrative-restarts` のいずれか 1 つを選びます。Python では [`ordered_restart_config.py`](ordered_restart_config.py) の `load_ordered_restart_plans` と `enable_configured_ordered_restarts` で有効化できます。計画は新規セッションの開始時に適用され、順序と容量はセッション内で維持されます。

形式は[ウォームリセットの例](examples/ordered_restart_plan.example.json)と[混合リセットの例](examples/ordered_restart_cold_plan.example.json)を参照してください。
