# New campaign controls

[简体中文](README_CAMPAIGN_CONTROLS.md) · [繁體中文](README_CAMPAIGN_CONTROLS.zh-TW.md) · [日本語](README_CAMPAIGN_CONTROLS.ja.md) · **English**

Controller input is detected on the press edge. The runtime configuration defines the host keyboard mapping.

| Button | New campaign setup |
| --- | --- |
| Up / Down | Cycle the period, difficulty, animation, and display speed options. |
| Left / Right | Cycle rulers in the current field. |
| C | Confirm the current field and move to the next. On the final confirmation field, request to finish setup. |
| B | Return to the previous field. At final confirmation, return to the first field and display the instructions. |
| Start | Request to finish setup from the current field. |
| A | Keep the current settings on this screen. |

| Field index | Setting | Range |
| --- | --- | --- |
| 0 | Period | 0–2 |
| 1 | Difficulty | 0–2 |
| 2 | Animation | 0–1 |
| 3 | Display speed | 0–2 |
| 4 | Player 1 ruler | Periods 0 and 1 have seven candidates each; period 2 has three. |
| 5 / 6 | Player 2 / Player 3 rulers | Skip previously chosen rulers and show fields for the number of players. |
| `5 + 7034` | Final confirmation | Values 0, 1, and 2 of `7034` mean one, two, and three players. |

Controller 1 handles the first four settings and player 1's ruler. Players 2 and 3 use controller 2 state `F605`. The extra ruler fields start accepting input when their counters, `7038` and `703A`, each reach 16.

A finish request sets `703E`. Once IRQ advances fade-out counter `7042` to 16, setup returns to the caller. `0x03076E` commits `7024/7026/7028/702A` and the chosen rulers to game state. See [Controller waits](README_CONTROLLER_MENU_STEPS.en.md) and [Campaign initialization](README_CAMPAIGN_MENU_STEPS.en.md).
