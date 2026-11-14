# セーブ内の都市・武将・勢力

[简体中文](README_NAMED_CAMPAIGN.md) · [繁體中文](README_NAMED_CAMPAIGN.zh-TW.md) · **日本語** · [English](README_NAMED_CAMPAIGN.en.md)

固定レコードビューは金、兵糧、兵力、所属、状態を都市、武将、勢力ごとにまとめます。エンコーダーは各区間のビット幅、量子化ルール、予約ビットを維持します。

アセンブリ版のルートで実行します。ローカルの 8 KiB 論理セーブを用意し、出力用に `build/` を準備します。

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli export --project-root . --source ./campaign.srm --output build/campaign.json
python -B -m tools.save_data.campaign_cli edit --project-root . --source build/campaign.json --edits ./campaign-changes.json --output build/campaign-edited.json
python -B -m tools.save_data.campaign_cli import --project-root . --source build/campaign-edited.json --original-logical ./campaign.srm --output build/campaign-edited.srm
```

編集ファイルに旧値と新値を記載します。取り込みは同じ元セーブを基準とし、結果は別のファイルに書き出します。
