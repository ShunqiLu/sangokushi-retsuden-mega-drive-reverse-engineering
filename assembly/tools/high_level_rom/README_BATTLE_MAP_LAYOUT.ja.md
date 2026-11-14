# 戦闘背景の配置

[简体中文](README_BATTLE_MAP_LAYOUT.md) · [繁體中文](README_BATTLE_MAP_LAYOUT.zh-TW.md) · **日本語** · [English](README_BATTLE_MAP_LAYOUT.en.md)

マップは 32 × 32 マスです。各マスにはタイル、パレット行、左右反転、上下反転、優先ビットが入ります。A 表と B 表は同じ背景の左右半分を指定します。ピクセルの編集には[タイルシートエディター](README_BATTLE_TILE_SHEET.ja.md)を使います。

`$resources` は `resources/` と `assets/` を含むローカル素材ルートです。アセンブリ版のルートで実行し、素材ルート外の新しいディレクトリに出力します。

```powershell
$resources = Read-Host '本地素材根目录'
python -B -m tools.high_level_rom.battle_map_layout export --edition-root $resources --map map_a_0 --output ./map-layout
python -B -m tools.high_level_rom.battle_map_layout prepare --edition-root $resources --edits ./map-edits.json --output ./map-replacements
```

`map_id` でマップを選び、各編集に 0 始まりの `row` と `column`、元のマス `expected`、変更フィールド `changes` を指定します。元の値はエクスポートからコピーします。`prepare` は圧縮スロットと終了コマンドを維持し、差し替えファイルと `replacements.json` を出力します。同じ繰り返し命令の範囲内では同じ値を使います。確認後、相対パスを保ってローカル素材に戻してください。
