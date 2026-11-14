# 新局選單與遊戲初始化

[简体中文](README_CAMPAIGN_MENU_STEPS.md) · **繁體中文** · [日本語](README_CAMPAIGN_MENU_STEPS.ja.md) · [English](README_CAMPAIGN_MENU_STEPS.en.md)

[`CampaignMenuScenePrograms`](../tools/high_level_gameplay_flow/campaign_menu_steps.py) 負責主流程的 `0x0004B0` 入口。它使用當前 Scene，沿用父流程的 `0x0003CE` 返回地址，並將控制器設定、裝置等待和劇本初始化接成一個合作式呼叫。

| 呼叫入口／返回位置 | 職責 |
| --- | --- |
| `0x00808A / 0x0522` | 聲音命令入隊及 BUSACK 等待 |
| `0x0305B0 / 0x0528` | 控制器與新局選單 |
| `0x006826 / 0x0532` | 視訊記憶體暫存器、平面初始化與 DMA |
| `0x03076E / 0x0538` | 提交選單選項 |
| `0x003E54 / 0x0548` | 讀取劇本描述符 |
| `0x009390 / 0x054E` | 初始化武將增長資料 |
| `0x0015BE / 0x0554` | 限制鏡頭軸範圍 |

原 CALL 的物理返回槽、部分暫存器寫入和條件碼由各呼叫體處理。宿主透過同一持久場景提供 IRQ 和裝置進度。底層合作式入口見[控制器設定](README_CONTROLLER_MENU_STEPS.zh-TW.md)。
