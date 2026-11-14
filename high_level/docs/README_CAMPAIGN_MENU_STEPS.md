# 新局菜单与游戏初始化

**简体中文** · [繁體中文](README_CAMPAIGN_MENU_STEPS.zh-TW.md) · [日本語](README_CAMPAIGN_MENU_STEPS.ja.md) · [English](README_CAMPAIGN_MENU_STEPS.en.md)

[`CampaignMenuScenePrograms`](../tools/high_level_gameplay_flow/campaign_menu_steps.py) 负责主流程的 `0x0004B0` 入口。它使用当前 Scene，沿用父流程的 `0x0003CE` 返回地址，并将控制器设置、设备等待和剧本初始化接成一个合作式调用。

| 调用入口／返回位置 | 职责 |
| --- | --- |
| `0x00808A / 0x0522` | 声音命令入队及 BUSACK 等待 |
| `0x0305B0 / 0x0528` | 控制器与新局菜单 |
| `0x006826 / 0x0532` | 显存寄存器、平面初始化与 DMA |
| `0x03076E / 0x0538` | 提交菜单选项 |
| `0x003E54 / 0x0548` | 读取剧本描述符 |
| `0x009390 / 0x054E` | 初始化武将增长数据 |
| `0x0015BE / 0x0554` | 限制镜头轴范围 |

原 CALL 的物理返回槽、部分寄存器写入和条件码由各调用体处理。宿主通过同一持久场景提供 IRQ 和设备进度。底层合作式入口见[控制器设置](README_CONTROLLER_MENU_STEPS.md)。
