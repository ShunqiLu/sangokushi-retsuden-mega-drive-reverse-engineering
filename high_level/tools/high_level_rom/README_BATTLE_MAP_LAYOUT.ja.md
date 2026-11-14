# 戦闘背景の配置

[简体中文](README_BATTLE_MAP_LAYOUT.md) · [繁體中文](README_BATTLE_MAP_LAYOUT.zh-TW.md) · **日本語** · [English](README_BATTLE_MAP_LAYOUT.en.md)

[`battle_map_layout.py`](battle_map_layout.py) は戦闘背景を 32 × 32 マスで書き出します。各マスは `tile`、`palette_line`、`flip_x`、`flip_y`、`priority` を持ち、ピクセルは[対応するタイル PNG](README_BATTLE_TILE_SHEET.ja.md)から取得します。

```powershell
$resources = Read-Host '兼容素材根'
python -B -m tools.high_level_rom.battle_map_layout export --edition-root $resources --map map_a_0 --output ./map-layout
python -B -m tools.high_level_rom.battle_map_layout prepare --edition-root $resources --edits ./map-edits.json --output ./map-replacements
```

`layout.json` の `rows` は行と列を 0 から数え、`uses` はディレクトリとスロットを列挙します。ディレクトリ A は Plane B の左半分、B は右半分を使います。編集ファイルは `g5510-battle-background-layout-edits-v1` 形式で `map_id` と `edits` を含みます。各編集に `row`、`column`、元の値全体 `expected`、変更箇所 `changes` を指定します。タイル番号の範囲は 0～1279 です。

差し替えファイルは素材ルートからの相対パス `assets/images/backgrounds/battle_graphics/maps/` に出力され、`replacements.json` に参照先と変更バイトが記録されます。圧縮コマンド、終端、スロット長は維持します。同じ繰り返し命令が覆う全マスで値全体をそろえてください。
