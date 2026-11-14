# グラフィック・音声・シナリオ素材

[简体中文](ASSETS.md) · [繁體中文](ASSETS.zh-TW.md) · **日本語** · [English](ASSETS.en.md)

`--resource-root` には互換性のあるローカル素材のディレクトリを指定します。以下のパスはそのディレクトリが基準です。ビルドツールは素材 ID で定義を調べ、参照先のファイルを読み込みます。

| パス | 内容 |
| --- | --- |
| `resources/images/` | タイル、マップ、スプライト、フォント、顔グラフィック、パレット、配置の定義 |
| `assets/images/` | 編集用のインデックス付き PNG、マップファイル、配置、パレット |
| `resources/audio/` | Z80 サウンドドライバー用の楽譜、音色、外部イベントの定義 |
| `assets/audio/` | 音符、制御イベント、エンベロープ、音色、共有音声ファイル |
| `resources/data/` | シナリオの初期値、AI パラメーター、テキスト、その他のルール表 |

マニフェスト `asset-source-manifest.json` には素材 ID、参照先、編集できるフィールドが記録されています。[索引ツール](tools/reconstruction_delivery/README_MEDIA_CATALOG.ja.md)で、ファイルごとに検索できる `ASSET_INDEX.json` を作成できます。

## グラフィック

PNG のピクセルにはパレット番号が入っています。プレビューの色は識別用で、ゲーム内の色は対応するパレットで決まります。編集時はタイルの寸法、インデックスのビット幅、共有素材の参照を保ってください。マスの座標、反転、優先順位はレイアウトツールで扱います。

- [戦闘マップのマスと属性](tools/high_level_rom/README_BATTLE_MAP_LAYOUT.ja.md)、[戦闘背景タイル](tools/high_level_rom/README_BATTLE_TILE_SHEET.ja.md)。
- [武将の顔グラフィック](PORTRAITS.ja.md)、[タイトル画面のタイル](tools/high_level_rom/README_TITLE_TILE_MEDIA.ja.md)。
- [共有画像と音声の別名参照](tools/high_level_rom/README_MEDIA_ALIASES.ja.md)。

## 音声

楽譜と効果音は、順序付きイベント、音色、エンベロープ、共有ファイルで構成されます。編集するのは定義とその参照先です。再生用の PCM は音源チップのモデルが生成します。

- [シーケンスとコマンド形式](tools/high_level_rom/README_AUDIO_SEQUENCE_SOURCES.ja.md)、[共有イベントエディター](tools/high_level_rom/README_AUDIO_SEQUENCE_EDITOR.ja.md)。
- [デスクトップ版の FM 音源とクロック](tools/high_level_audio_engine/README_YMFM.ja.md)。

## ゲームデータ

[名前付きシナリオ](tools/high_level_rom/README_NAMED_SCENARIO_SOURCES.ja.md)、[AI のしきい値](tools/high_level_rom/README_AI_POLICY_SOURCES.ja.md)、[候補の適格条件](tools/high_level_rom/README_AI_SELECTION_SOURCES.ja.md)、[可読テキスト](tools/high_level_rom/README_READABLE_TEXT.ja.md)に、編集とエンコードの規則があります。各素材で元のフィールド幅と配置を保ちます。
