# セーブ内の行軍部隊

[简体中文](README_CAMPAIGN_PACKETS.md) · [繁體中文](README_CAMPAIGN_PACKETS.zh-TW.md) · **日本語** · [English](README_CAMPAIGN_PACKETS.en.md)

行軍ビューは部隊の順序、武将番号、マップ座標、勢力、携行資源を保持します。編集は元のレコード件数、所属人数、保存フィールド幅の範囲内で行います。

アセンブリ版のルートで実行します。ローカルの 8 KiB 論理セーブを用意し、出力用に `build/` を準備します。

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli packets-export --project-root . --source ./campaign.srm --output build/packets.json
python -B -m tools.save_data.campaign_cli packets-edit --project-root . --source build/packets.json --edits ./packets-changes.json --output build/packets-edited.json
python -B -m tools.save_data.campaign_cli packets-import --project-root . --source build/packets-edited.json --original-logical ./campaign.srm --output build/packets-edited.srm
```

編集ファイルに旧値と新値を記載します。取り込みは同じ元セーブを基準とし、結果は別のファイルに書き出します。
