# 戦闘背景タイルシート

[简体中文](README_BATTLE_TILE_SHEET.md) · [繁體中文](README_BATTLE_TILE_SHEET.zh-TW.md) · **日本語** · [English](README_BATTLE_TILE_SHEET.en.md)

[`battle_tile_sheet.py`](battle_tile_sheet.py) は `tiles_0` から `tiles_4` までのタイルグループを選び、128 × 128 のインデックス付き PNG に書き出します。8 × 8 のタイルを VRAM 転送順に 16 × 16 枚並べます。灰色の濃淡は番号を表し、ゲーム内の色はパレットで決まります。位置、反転、パレット行は[配置エディター](README_BATTLE_MAP_LAYOUT.ja.md)で指定します。

```powershell
$resources = Read-Host '兼容素材根'
python -B -m tools.high_level_rom.battle_tile_sheet export --edition-root $resources --stream tiles_0 --output ./tile-sheet
python -B -m tools.high_level_rom.battle_tile_sheet prepare --edition-root $resources --stream tiles_0 --baseline-dir ./tile-sheet --edited ./tiles-edited.png --output ./tile-replacements
```

出力先は素材ルート外の新規ディレクトリです。元の PNG と `baseline.json` を基準にし、128 × 128 の寸法、インデックス形式、先頭 16 色のパレットを保った別の PNG を編集用に渡します。変更したタイル帯は `assets/images/backgrounds/battle_graphics/` の相対パスに従い、`replacements.json` に差し替えファイルと元の線形アドレスが記録されます。

同じ繰り返し命令が覆う位置は、同一の 4 ピクセルの WORD を使います。命令境界、繰り返し回数、終端、サイズ、線形位置は維持されます。リテラル命令には元のエスケープ規則を適用します。
