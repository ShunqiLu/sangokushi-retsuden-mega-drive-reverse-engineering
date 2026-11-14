# 戦闘背景タイルシート

[简体中文](README_BATTLE_TILE_SHEET.md) · [繁體中文](README_BATTLE_TILE_SHEET.zh-TW.md) · **日本語** · [English](README_BATTLE_TILE_SHEET.en.md)

各インデックス付き PNG は 128 × 128 ピクセルで、8 × 8 ピクセルのタイルを 16 × 16 枚並べています。`tiles_0` から `tiles_4` が 5 種類のタイルセットに対応します。ピクセルはシートの 16 色の番号を保持し、ゲーム内の色はゲーム側のパレットで決まります。位置と反転は[マップ配置](README_BATTLE_MAP_LAYOUT.ja.md)で編集します。

`$resources` は `resources/` と `assets/` を含むローカル素材ルートです。アセンブリ版のルートで実行し、素材ルート外の新しいディレクトリに出力します。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.high_level_rom.battle_tile_sheet export --edition-root $resources --stream tiles_0 --output ./tile-sheet
python -B -m tools.high_level_rom.battle_tile_sheet prepare --edition-root $resources --stream tiles_0 --baseline-dir ./tile-sheet --edited ./tiles-edited.png --output ./tile-replacements
```

書き出した `baseline.json` と元画像を比較用に残してください。編集後も透過なしのインデックス形式、128 × 128 の寸法、パレットの並び順を維持します。1 つの圧縮命令を共有する位置は同じピクセルを使います。`replacements.json` に、ローカル素材へコピーするタイル帯が記載されます。
