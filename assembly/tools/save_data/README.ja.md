# セーブデータツール

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **日本語** · [English](README.en.md)

`save_format` はセーブのコンテナー形式の識別、チェックサムの検証、データ区間の読み書きを行います。`campaign_cli` で現在のセーブの名前付きフィールドを編集できます。元のセーブを入力として残し、新しいパスに書き出します。

```powershell
python -B -m tools.save_data.save_format inspect ./campaign.srm
python -B -m tools.save_data.save_format extract ./campaign.srm ./save-source
python -B -m tools.save_data.save_format import ./save-source ./campaign-edited.srm
```

名前付きのツールは[都市・武将・勢力](README_NAMED_CAMPAIGN.ja.md)、[行軍部隊](README_CAMPAIGN_PACKETS.ja.md)、[輸送命令](README_CAMPAIGN_ORDERS.ja.md)を扱います。シナリオの初期値はローカル素材の `resources/data/scenario_build.json` にあります。
