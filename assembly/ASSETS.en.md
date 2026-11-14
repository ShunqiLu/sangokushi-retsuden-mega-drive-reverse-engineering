# Compatible resource pack

[简体中文](ASSETS.md) · [繁體中文](ASSETS.zh-TW.md) · [日本語](ASSETS.ja.md) · **English**

The pack has two directories, `resources/` and `assets/`. The first describes formats and file references. The second holds tiles, layouts, instrument patches, channel events, and other data. Pass their common parent to `--resource-root`.

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

| Resource | Location in the pack |
| --- | --- |
| Title graphics | `resources/images/graphics_build.json`, `assets/images/title/` |
| Battle map layout and background | `resources/images/battle_graphics.json` |
| Officer portraits and palettes | `resources/images/portrait_graphics.json`, `assets/images/portraits/` |
| Font glyphs | `resources/images/font_build.json`, `assets/images/fonts/` |
| Music, sound effects, and state events | `resources/audio/audio_build.json`, `assets/audio/` |
| Scenarios and dialogue | `resources/data/scenario_build.json`, `resources/data/dialogue_text.json` |

With a resource manifest, the [index tool](tools/reconstruction_delivery/README_MEDIA_CATALOG.en.md) locates files and fields. The encoder reads pixel indices from the indexed PNGs. The matching palette files supply the game colors.
