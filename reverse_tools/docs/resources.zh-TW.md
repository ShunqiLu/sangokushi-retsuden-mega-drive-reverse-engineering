# 資源與存檔

[简体中文](resources.md) · **繁體中文** · [日本語](resources.ja.md) · [English](resources.en.md)

固定地址工具使用 G-5510 線性 BIN。資源匯入使用匯出時的同一份基線映象和新的輸出位置。工具輸出使用呼叫者指定的檔案或目錄。

| 工具 | 資料 |
| --- | --- |
| [scan_assets.py](../tools/asset_analysis/scan_assets.py) | 資源候選、文字引用、重複資料塊、瓦片預覽 |
| [render_raw4bpp.py](../tools/asset_analysis/render_raw4bpp.py) | 8×8 瓦片、16×16 字形預覽 |
| [graphics_build.py](../tools/graphics_build/graphics_build.py) | 標題與單挑的瓦片、地圖、配色與傳輸欄位 |
| [graphics_assets.py](../tools/graphics_vdp/graphics_assets.py) | 標題圖形、VDP 緩衝區和靜態預覽 |
| [duel_graphics.py](../tools/duel_graphics/duel_graphics.py) | 固定單挑素材、雙通道 RLE 地圖與靜態預覽 |
| [audio_formats.py](../tools/audio_formats/audio_formats.py) | 曲目、音效頭和 FM 樂器暫存器欄位 |
| [scenario_static_data.py](../tools/static_data/scenario_static_data.py) | 劇本初始表、源記錄和執行時表示 |

```sh
python tools/asset_analysis/scan_assets.py --rom out/cartridge.bin --output out/resource-map
python tools/asset_analysis/render_raw4bpp.py 0x50000 --rom out/cartridge.bin --output out/tiles.png
python tools/graphics_build/graphics_build.py export --rom out/cartridge.bin --output out/graphics
python tools/graphics_build/graphics_build.py import --rom out/cartridge.bin --assets out/graphics/assets.json --output out/graphics-image
python tools/audio_formats/audio_formats.py export --rom out/cartridge.bin --output out/audio
python tools/static_data/scenario_static_data.py extract --rom out/cartridge.bin --output out/scenarios
```

圖形編輯保留固定槽位尺寸。單挑地圖支援修改壓縮流或解碼的瓦片圖，匯入器按照槽位要求編碼。音訊包保留指標表與共享樂器關係；劇本包保留表順序和源記錄寬度。

## SRAM

[`save_format.py`](../tools/save_data/save_format.py) 支援 8 KiB 邏輯 SRAM 和 16 KiB MAME 交織容器。匯出包儲存固定欄位、位壓縮記錄和原始保留區域；匯入計算存檔校驗和並保留所選容器佈局。

```sh
python tools/save_data/save_format.py inspect input/campaign.srm
python tools/save_data/save_format.py extract input/campaign.srm out/save-fields
python tools/save_data/save_format.py import out/save-fields out/rebuilt.srm
python tools/save_data/generate_reports.py out/save-layout
```

[`generate_reports.py`](../tools/save_data/generate_reports.py) 輸出欄位偏移、位寬和記錄數表。`--capture` 接收存檔檔案，並附加該檔案的格式和欄位統計。
