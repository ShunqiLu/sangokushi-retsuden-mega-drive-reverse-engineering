# Transport directions, arrivals, and collisions

[简体中文](README_SCENE_TRANSPORT.md) · [繁體中文](README_SCENE_TRANSPORT.zh-TW.md) · [日本語](README_SCENE_TRANSPORT.ja.md) · **English**

The route index determines the next direction. On arrival, resources are added to the destination city. Collision checks use the transport slots and the unit list. Gold and grain caps are checked against totals computed at the original bit widths. See `m68k_016874` and `m68k_016946` in the [68000 program](../../src/m68k/recovered_code.s).
