# 战斗场景生命周期

[`BattleLifecycleScenePrograms`](battle_lifecycle_steps.py) 连接场景初始化、分配、战斗回合及结果处理。各入口共享 Scene、资源和设备提供器，合作式调用保留父调用的物理帧、返回地址、嵌套栈与条件码。

战斗的入口和暂停类型见[战斗入口与结果续接](../../docs/README_BATTLE_ENTRY_STEPS.md)。战斗业务规则位于 [`business_battle.py`](business_battle.py)，目标声明和指令布局由 [`compiler_battle_lifecycle_steps.py`](compiler_battle_lifecycle_steps.py) 描述。
