# 素材とセーブデータ

[简体中文](resources.md) · [繁體中文](resources.zh-TW.md) · **日本語** · [English](resources.en.md)

固定アドレスのツールには G-5510 の線形 BIN を使用します。素材を取り込むときは書き出し時と同じ基準イメージを使い、新しい出力先を指定します。出力ファイルまたはディレクトリはツールの引数です。

| ツール | データ |
| --- | --- |
| [scan_assets.py](../tools/asset_analysis/scan_assets.py) | 素材候補、テキスト参照、繰り返しブロック、タイルのプレビュー |
| [render_raw4bpp.py](../tools/asset_analysis/render_raw4bpp.py) | 8×8 のタイルと 16×16 の字形のプレビュー |
| [graphics_build.py](../tools/graphics_build/graphics_build.py) | タイトル画面と一騎討ちのタイル、マップ、パレット、転送フィールド |
| [graphics_assets.py](../tools/graphics_vdp/graphics_assets.py) | タイトル画面のグラフィック、VDP バッファー、静止プレビュー |
| [duel_graphics.py](../tools/duel_graphics/duel_graphics.py) | 一騎討ちの固定素材、2 チャンネル RLE マップ、静止プレビュー |
| [audio_formats.py](../tools/audio_formats/audio_formats.py) | 楽曲、効果音ヘッダー、FM 音色のレジスターフィールド |
| [scenario_static_data.py](../tools/static_data/scenario_static_data.py) | シナリオの初期化テーブル、元レコード、実行時の表現 |

```sh
python tools/asset_analysis/scan_assets.py --rom out/cartridge.bin --output out/resource-map
python tools/asset_analysis/render_raw4bpp.py 0x50000 --rom out/cartridge.bin --output out/tiles.png
python tools/graphics_build/graphics_build.py export --rom out/cartridge.bin --output out/graphics
python tools/graphics_build/graphics_build.py import --rom out/cartridge.bin --assets out/graphics/assets.json --output out/graphics-image
python tools/audio_formats/audio_formats.py export --rom out/cartridge.bin --output out/audio
python tools/static_data/scenario_static_data.py extract --rom out/cartridge.bin --output out/scenarios
```

グラフィックを編集するときは固定スロットの寸法を保ちます。一騎討ちマップでは圧縮ストリームか展開後のタイルマップを編集でき、インポーターがスロットに応じてエンコードします。音声パックはポインターテーブルと音色の共有関係を、シナリオパックは表の順序と元レコードの幅を維持します。

## SRAM

[`save_format.py`](../tools/save_data/save_format.py) は 8 KiB の論理 SRAM と、16 KiB のインターリーブされた MAME コンテナーに対応します。書き出しでは固定フィールド、ビット詰めレコード、元の予約領域を保ちます。取り込みではチェックサムを再計算し、指定されたコンテナーの配置を維持します。

```sh
python tools/save_data/save_format.py inspect input/campaign.srm
python tools/save_data/save_format.py extract input/campaign.srm out/save-fields
python tools/save_data/save_format.py import out/save-fields out/rebuilt.srm
python tools/save_data/generate_reports.py out/save-layout
```

[`generate_reports.py`](../tools/save_data/generate_reports.py) はフィールドのオフセット、ビット幅、レコード数を出力します。`--capture` にセーブファイルを指定すると、その形式とフィールド統計も出力します。
