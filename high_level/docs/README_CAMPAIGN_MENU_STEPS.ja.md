# 新規ゲームのメニューと初期化

[简体中文](README_CAMPAIGN_MENU_STEPS.md) · [繁體中文](README_CAMPAIGN_MENU_STEPS.zh-TW.md) · **日本語** · [English](README_CAMPAIGN_MENU_STEPS.en.md)

[`CampaignMenuScenePrograms`](../tools/high_level_gameplay_flow/campaign_menu_steps.py) はメイン処理の `0x0004B0` の入口です。現在の Scene と親の戻りアドレス `0x0003CE` を使い、コントローラー設定、デバイス待ち、シナリオ初期化を 1 つの協調呼び出しにまとめます。

| 呼び出しの入口／復帰位置 | 用途 |
| --- | --- |
| `0x00808A / 0x0522` | 音声コマンドをキューに入れ、BUSACK を待つ |
| `0x0305B0 / 0x0528` | コントローラーと新規ゲームメニュー |
| `0x006826 / 0x0532` | VRAM レジスター、プレーン初期化、DMA |
| `0x03076E / 0x0538` | メニューの選択を確定 |
| `0x003E54 / 0x0548` | シナリオ記述子を読み込む |
| `0x009390 / 0x054E` | 武将の成長データを初期化 |
| `0x0015BE / 0x0554` | カメラの軸範囲を制限 |

各呼び出しは元の CALL の物理戻りスロット、レジスターの部分書き込み、条件コードを扱います。ホストは持続する同じシーンから IRQ とデバイス進行を供給します。下位の協調入口は[コントローラー設定](README_CONTROLLER_MENU_STEPS.ja.md)を参照してください。
