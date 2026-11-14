# ハードウェア入力の容量

[简体中文](README_HARDWARE_PROFILE.md) · [繁體中文](README_HARDWARE_PROFILE.zh-TW.md) · **日本語** · [English](README_HARDWARE_PROFILE.en.md)

[`hardware_profile.py`](hardware_profile.py) は完全なハードウェア JSON と容量計画を受け取り、新しい有限入力設定を書き出します。容量は DMA 転送、音声 DATA 操作、ドライバーのコピー許可、VBlank エッジなどのデバイス単位で数えます。

```powershell
python -B -X utf8 -m tools.reconstructed_game.hardware_profile --project-root . --base-hardware tools/reconstructed_game/examples/application_hardware_inputs.json --capacity-plan tools/reconstructed_game/examples/hardware_capacity_8192.json --output build/gameplay-hardware.json
```

基準設定は元の構造と入力例を供給し、容量計画は増やす項目を指定します。出力は新しい有限設定です。実際の時間とイベント順は[フレーム計画](README_FRAME_PLAN.ja.md)と[ハードウェア入力仕様](README_HARDWARE_INPUTS.ja.md)に従います。
