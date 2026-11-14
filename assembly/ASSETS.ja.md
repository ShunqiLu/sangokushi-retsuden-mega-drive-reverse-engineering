# 互換素材パック

[简体中文](ASSETS.md) · [繁體中文](ASSETS.zh-TW.md) · **日本語** · [English](ASSETS.en.md)

素材パックは `resources/` と `assets/` で構成されます。前者には形式と参照先の定義、後者にはタイル、レイアウト、音色、チャンネルイベントなどのデータがあります。両方の親ディレクトリを `--resource-root` に指定します。

```text
本地素材根/
  resources/
    audio/
    data/
    images/
  assets/
    audio/
    images/
```

| 素材 | パック内の場所 |
| --- | --- |
| タイトル画面 | `resources/images/graphics_build.json`、`assets/images/title/` |
| 戦闘マップの配置と背景 | `resources/images/battle_graphics.json` |
| 武将の顔グラフィックとパレット | `resources/images/portrait_graphics.json`、`assets/images/portraits/` |
| フォントの字形 | `resources/images/font_build.json`、`assets/images/fonts/` |
| 楽曲、効果音、状態イベント | `resources/audio/audio_build.json`、`assets/audio/` |
| シナリオと台詞 | `resources/data/scenario_build.json`、`resources/data/dialogue_text.json` |

素材マニフェストがあれば、[索引ツール](tools/reconstruction_delivery/README_MEDIA_CATALOG.ja.md)でファイルやフィールドを探せます。エンコーダーはインデックス付き PNG のピクセル番号を読み取り、ゲーム内の色は対応するパレットファイルから取得します。
