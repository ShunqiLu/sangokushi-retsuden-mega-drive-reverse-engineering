# Transport orders in the live scene

[简体中文](README_SCENE_TRANSPORT.md) · [繁體中文](README_SCENE_TRANSPORT.zh-TW.md) · [日本語](README_SCENE_TRANSPORT.ja.md) · **English**

[`business_scene_transport.py`](business_scene_transport.py) handles transport direction, route progression, collisions, and arrival. The current scene supplies the map, adjacent coordinates, and transport records; the rules read and write the same live state. On arrival, the city receives resources at their original field widths, including wraparound and caps.

The offline [CE00 transport order view](../save_data/README_CAMPAIGN_ORDERS.en.md) handles the save representation. Live flags, speed, and cargo come from the scene state.
