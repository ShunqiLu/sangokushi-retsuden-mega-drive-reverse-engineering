# SRAM とセーブデータツール

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **日本語** · [English](README.en.md)

論理 SRAM の確認、展開、編集、書き出しを行うツールです。G-5510 は奇数アドレス `0x200001–0x203FFF` を使い、論理媒体は 8192 バイトです。各バイトを 2 回ずつ格納する MAME の 16 KiB コンテナーにも対応しています。

```powershell
python tools/save_data/save_format.py inspect input.srm
python tools/save_data/save_format.py extract input.srm save-fields
python tools/save_data/save_format.py import save-fields edited.srm
```

展開では `SEGA` のシグネチャーと元の加算チェックサムを照合し、配置、フィールド、基準セーブを出力します。書き出しは新規ファイルを使い、コンテナーの形式、不明バイト、フィールド幅を保ってチェックサムを再計算します。`--allow-variable-resize` を指定すると部隊ビットストリームの符号化長を変更でき、後続のチェックサム対象の空き領域を `FF` で埋めます。

## セーブビュー

- [都市・武将・勢力の固定レコード](README_NAMED_CAMPAIGN.ja.md)。
- [行軍部隊、座標、積載資源](README_CAMPAIGN_PACKETS.ja.md)。
- [CE00 輸送命令](README_CAMPAIGN_ORDERS.ja.md)。

有効な 8192 バイトの論理セーブを基準にして、新しい候補ファイルを生成します。デスクトップアプリの `export_save` が現在の SRAM を書き出し、セーブツールでシグネチャーとチェックサムを確認できます。使う媒体は[ローカル設定](../reconstructed_game/README_LOCAL_CONFIG.ja.md)で指定します。初期シナリオは[シナリオツール](../high_level_rom/README_NAMED_SCENARIO_SOURCES.ja.md)で管理します。
