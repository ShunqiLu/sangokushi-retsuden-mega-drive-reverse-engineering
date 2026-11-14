# 资源与存档

**简体中文** · [繁體中文](resources.zh-TW.md) · [日本語](resources.ja.md) · [English](resources.en.md)

固定地址工具使用 G-5510 线性 BIN。资源导入使用导出时的同一份基线镜像和新的输出位置。工具输出使用调用者指定的文件或目录。

| 工具 | 数据 |
| --- | --- |
| [scan_assets.py](../tools/asset_analysis/scan_assets.py) | 资源候选、文本引用、重复数据块、瓦片预览 |
| [render_raw4bpp.py](../tools/asset_analysis/render_raw4bpp.py) | 8×8 瓦片、16×16 字形预览 |
| [graphics_build.py](../tools/graphics_build/graphics_build.py) | 标题与单挑的瓦片、地图、配色与传输字段 |
| [graphics_assets.py](../tools/graphics_vdp/graphics_assets.py) | 标题图形、VDP 缓冲区和静态预览 |
| [duel_graphics.py](../tools/duel_graphics/duel_graphics.py) | 固定单挑素材、双通道 RLE 地图与静态预览 |
| [audio_formats.py](../tools/audio_formats/audio_formats.py) | 曲目、音效头和 FM 乐器寄存器字段 |
| [scenario_static_data.py](../tools/static_data/scenario_static_data.py) | 剧本初始表、源记录和运行时表示 |

```sh
python tools/asset_analysis/scan_assets.py --rom out/cartridge.bin --output out/resource-map
python tools/asset_analysis/render_raw4bpp.py 0x50000 --rom out/cartridge.bin --output out/tiles.png
python tools/graphics_build/graphics_build.py export --rom out/cartridge.bin --output out/graphics
python tools/graphics_build/graphics_build.py import --rom out/cartridge.bin --assets out/graphics/assets.json --output out/graphics-image
python tools/audio_formats/audio_formats.py export --rom out/cartridge.bin --output out/audio
python tools/static_data/scenario_static_data.py extract --rom out/cartridge.bin --output out/scenarios
```

图形编辑保留固定槽位尺寸。单挑地图支持修改压缩流或解码的瓦片图，导入器按照槽位要求编码。音频包保留指针表与共享乐器关系；剧本包保留表顺序和源记录宽度。

## SRAM

[`save_format.py`](../tools/save_data/save_format.py) 支持 8 KiB 逻辑 SRAM 和 16 KiB MAME 交织容器。导出包保存固定字段、位压缩记录和原始保留区域；导入计算存档校验和并保留所选容器布局。

```sh
python tools/save_data/save_format.py inspect input/campaign.srm
python tools/save_data/save_format.py extract input/campaign.srm out/save-fields
python tools/save_data/save_format.py import out/save-fields out/rebuilt.srm
python tools/save_data/generate_reports.py out/save-layout
```

[`generate_reports.py`](../tools/save_data/generate_reports.py) 输出字段偏移、位宽和记录数表。`--capture` 接收存档文件，并附加该文件的格式和字段统计。
