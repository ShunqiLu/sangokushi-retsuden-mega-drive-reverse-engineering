# セーブ内の輸送命令

[简体中文](README_CAMPAIGN_ORDERS.md) · [繁體中文](README_CAMPAIGN_ORDERS.zh-TW.md) · **日本語** · [English](README_CAMPAIGN_ORDERS.en.md)

輸送ビューは CE00 の 40 個の保存スロットに対応します。種別、経路座標、目的地の都市などのエンコード値を表示します。取り込みでは空きスロットと他の区間を保ちます。

アセンブリ版のルートで実行します。ローカルの 8 KiB 論理セーブを用意し、出力用に `build/` を準備します。

```powershell
New-Item -ItemType Directory -Force ./build | Out-Null
python -B -m tools.save_data.campaign_cli orders-export --project-root . --source ./campaign.srm --output build/orders.json
python -B -m tools.save_data.campaign_cli orders-edit --project-root . --source build/orders.json --edits ./orders-changes.json --output build/orders-edited.json
python -B -m tools.save_data.campaign_cli orders-import --project-root . --source build/orders-edited.json --original-logical ./campaign.srm --output build/orders-edited.srm
```

編集ファイルに旧値と新値を記載します。取り込みは同じ元セーブを基準とし、結果は別のファイルに書き出します。
