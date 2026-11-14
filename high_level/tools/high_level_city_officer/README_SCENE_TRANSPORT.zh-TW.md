# 運輸命令與場景執行

[简体中文](README_SCENE_TRANSPORT.md) · **繁體中文** · [日本語](README_SCENE_TRANSPORT.ja.md) · [English](README_SCENE_TRANSPORT.en.md)

[`business_scene_transport.py`](business_scene_transport.py) 管理場景中的運輸方向、路徑推進、碰撞與到達。當前場景提供地圖、相鄰座標和運輸記錄；運輸業務規則讀寫同一執行狀態。輸送隊抵達城市後，城市收貨處理按原欄位寬度寫入資源，保留遊戲的迴繞和封頂語義。

離線的 [CE00 運輸命令檢視](../save_data/README_CAMPAIGN_ORDERS.zh-TW.md) 負責存檔表示。執行中的旗標、速度和貨物由場景業務狀態提供。
