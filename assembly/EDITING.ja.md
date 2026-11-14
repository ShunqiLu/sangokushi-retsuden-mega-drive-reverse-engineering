# 編集ガイド

[简体中文](EDITING.md) · [繁體中文](EDITING.zh-TW.md) · **日本語** · [English](EDITING.en.md)

プログラムとツールのパスはこのディレクトリを、素材のパスは `--resource-root` で指定したディレクトリを基準とします。ローカルコピーを編集してから、ソースを再ビルドしてください。

| 内容 | 編集箇所 |
| --- | --- |
| 68000 と Z80 のプログラム | `src/m68k/`、`src/z80/`。命令範囲は `tools/reconstructed_assembly/layout/` |
| 都市、武将、勢力の初期値 | 素材ルートの `resources/data/scenario_build.json`。[シナリオ編集](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.ja.md)を参照 |
| 台詞、武将名、都市名 | `resources/data/dialogue_text.json`。[テキスト編集](tools/high_level_rom/README_READABLE_TEXT.ja.md)を参照 |
| AI パラメーター | `resources/data/ai_threshold_pair_fields.json`、`resources/data/ai_selection_fields.json`。[判定しきい値](tools/high_level_rom/README_AI_POLICY_SOURCES.ja.md)と[候補の適格条件](tools/high_level_rom/README_AI_SELECTION_SOURCES.ja.md)を参照 |
| グラフィックと配色 | `assets/images/` と対応するレイアウト・パレットの JSON。[素材ガイド](ASSETS.ja.md)、[戦闘マップ](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.ja.md)、[タイルシート](tools/high_level_rom/README_BATTLE_TILE_SHEET.ja.md)、[顔グラフィック](PORTRAITS.ja.md)を参照 |
| 楽曲、効果音、音色 | `resources/audio/` と、そこから参照する `assets/audio/`。[音声シーケンス](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.ja.md)と[共有イベント](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.ja.md)を参照 |
| 現在のセーブデータ | [セーブツール](tools/save_data/README.ja.md)：[都市と勢力](tools/save_data/README_NAMED_CAMPAIGN.ja.md)、[行軍部隊](tools/save_data/README_CAMPAIGN_PACKETS.ja.md)、[輸送命令](tools/save_data/README_CAMPAIGN_ORDERS.ja.md) |

インデックス付き PNG では、ピクセル番号がタイルデータになります。画像モード、寸法、元のパスを保ってください。表示色はパレットの JSON で変更できます。編集後の素材ルートは[ビルド手順](README.ja.md)に従って指定します。
