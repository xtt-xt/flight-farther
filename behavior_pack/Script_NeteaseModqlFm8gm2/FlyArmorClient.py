# -*- coding: utf-8 -*-
# ==================== 飞行之羽模组 - 客户端 ====================

import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()
clientCompFactory = clientApi.GetEngineCompFactory()
clientEngineNamespace = clientApi.GetEngineNamespace()
clientEngineSystemName = clientApi.GetEngineSystemName()


class FlyArmorClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.setting_inst = None
        self.has_permission = False
        self.enable_repair_xp = True
        self.enable_repair_material = True
        self._poll_timer = None
        self._pending_permission_args = None  # 缓存提前到达的权限事件

        self.ListenForEvent(clientEngineNamespace, clientEngineSystemName,
                            "UiInitFinished", self, self.on_ui_init)
        self.ListenForEvent("FlyArmorServer", "FlyArmorServerSystem",
                            "FlyArmorPermissionEvent", self, self.on_permission_event)
        self.ListenForEvent(clientEngineNamespace, clientEngineSystemName,
                            "PushScreenEvent", self, self.on_push_screen)

    # ==================== 通用设置注册 ====================

    def on_ui_init(self, args):
        localPlayerId = clientApi.GetLocalPlayerId()
        if not localPlayerId:
            return
        windowComp = clientCompFactory.CreateNeteaseWindow(localPlayerId)
        if not windowComp:
            return

        self.setting_inst = windowComp.RegisterSettingInst(
            modNamespace="FlyArmor",
            modName="飞行之羽模组",
            iconPath=""
        )
        if not self.setting_inst:
            return

        self.setting_inst             .AddText("title", "飞行之羽模组设置", priority=0)             .AddText("section1", "状态效果", priority=1)             .AddToggle("enable_ender_effect", "启用末影之羽状态效果",
                       callback=self.on_toggle_ender,
                       priority=2, default=True)             .AddToggle("enable_ender_full", "末影之羽完整版",
                       callback=self.on_toggle_ender_full,
                       priority=3, default=False)             .AddText("ender_full_desc", "§7开启后在所有维度获得末地级别的增益", priority=4)             .AddToggle("enable_swift_effect", "启用迅捷之羽状态效果",
                       callback=self.on_toggle_swift,
                       priority=5, default=True)             .AddText("section2", "消耗选项", priority=6)             .AddToggle("enable_durability", "启用飞行耐久消耗",
                       callback=self.on_toggle_durability,
                       priority=7, default=True)             .AddToggle("enable_effect_durability", "状态效果耐久消耗",
                       callback=self.on_toggle_effect_durability,
                       priority=8, default=True)             .AddText("section3", "修复设置", priority=9)             .AddToggle("enable_repair", "允许手持物品修复",
                       callback=self.on_toggle_repair,
                       priority=10, default=True)             .AddToggle("enable_repair_xp", "修复消耗经验",
                       callback=self.on_toggle_repair_xp,
                       priority=11, default=True)             .AddToggle("enable_repair_material", "修复消耗物品",
                       callback=self.on_toggle_repair_material,
                       priority=12, default=True)             .AddInput("repair_xp_multiplier", "修复经验消耗倍率",
                       callback=self.on_xp_multiplier,
                       priority=13, default="1")             .AddText("section4", "调试选项", priority=14)             .AddToggle("debug_mode", "模组调试",
                       callback=self.on_toggle_debug,
                       priority=15, default=False)

        self._lock_all_controls(True)
        self.NotifyToServer("FlyArmorRequestPermissionEvent", {
            "playerId": localPlayerId
        })
        self._start_permission_poll(localPlayerId)
        # 如果之前有缓存的权限事件，现在UI已就绪，处理它
        if self._pending_permission_args is not None:
            self._apply_permission_args(self._pending_permission_args)
            self._pending_permission_args = None

    def _start_permission_poll(self, playerId):
        """使用客户端 tick 轮询代替 Timer 组件，每约3秒请求一次权限"""
        if self._poll_timer is not None:
            return
        self._poll_counter = 0
        self._poll_target = 60  # 约3秒 (20tick/s)
        self._poll_timer = True

    def Update(self):
        """客户端每帧调用，用于权限轮询"""
        if self._poll_timer:
            self._poll_counter += 1
            if self._poll_counter >= self._poll_target:
                self._poll_counter = 0
                localPlayerId = clientApi.GetLocalPlayerId()
                if localPlayerId:
                    self.NotifyToServer("FlyArmorRequestPermissionEvent", {
                        "playerId": localPlayerId
                    })

    def _lock_all_controls(self, locked):
        if not self.setting_inst:
            return
        keys = [
            "enable_durability", "enable_effect_durability",
            "enable_ender_effect", "enable_ender_full", "ender_full_desc",
            "enable_swift_effect", "enable_repair", "enable_repair_xp",
            "enable_repair_material", "repair_xp_multiplier", "debug_mode",
            "section1", "section2", "section3", "section4"
        ]
        for key in keys:
            self.setting_inst.SetLockSettingComp(key, locked)

    # ==================== 权限事件 ====================

    def _update_repair_locks(self):
        if not self.setting_inst:
            return
        lock_multiplier = not self.enable_repair_xp
        self.setting_inst.SetLockSettingComp("repair_xp_multiplier", lock_multiplier)

    def on_permission_event(self, args):
        # 如果UI还没初始化好，先缓存起来
        if self.setting_inst is None:
            self._pending_permission_args = args
            return
        self._apply_permission_args(args)

    def _apply_permission_args(self, args):
        """应用权限事件参数，必须在 setting_inst 已就绪后调用"""
        has_perm = args.get("hasPermission", False)
        settings = args.get("settings", {})
        # 同步服务端持久化设置到客户端UI
        if settings and self.setting_inst:
            for key, value in settings.items():
                if key in ("repair_xp_multiplier",):
                    try:
                        self.setting_inst.SetInputValue(key, str(value))
                    except Exception:
                        pass
                else:
                    try:
                        self.setting_inst.SetToggleValue(key, bool(value))
                    except Exception:
                        pass
            self.enable_repair_xp = settings.get("enable_repair_xp", True)
            self.enable_repair_material = settings.get("enable_repair_material", True)
        # 权限状态变化时才刷新锁定
        if self.has_permission != has_perm:
            self.has_permission = has_perm
            if has_perm:
                self._lock_all_controls(False)
                self._update_repair_locks()
            else:
                self._lock_all_controls(True)
                if self.setting_inst:
                    self.setting_inst.SetText("title", "§c飞行之羽模组设置 [仅房主/管理员可编辑]")

    def on_push_screen(self, args):
        """监听原生界面入栈（包括设置界面），每次打开都重新请求权限刷新锁定状态"""
        if not self.setting_inst:
            return
        localPlayerId = clientApi.GetLocalPlayerId()
        self.NotifyToServer("FlyArmorRequestPermissionEvent", {
            "playerId": localPlayerId
        })

    # ==================== 控件回调 ====================

    def _send_setting_to_server(self, key, value):
        localPlayerId = clientApi.GetLocalPlayerId()
        self.NotifyToServer("FlyArmorSettingChangeEvent", {
            "playerId": localPlayerId,
            "key": key,
            "value": value
        })

    def on_toggle_durability(self, key, value):
        self._send_setting_to_server(key, value)

    def on_toggle_ender(self, key, value):
        self._send_setting_to_server(key, value)

    def on_toggle_swift(self, key, value):
        self._send_setting_to_server(key, value)

    def on_toggle_effect_durability(self, key, value):
        self._send_setting_to_server(key, value)

    def on_toggle_ender_full(self, key, value):
        self._send_setting_to_server(key, value)

    def on_toggle_repair(self, key, value):
        self._send_setting_to_server(key, value)

    def on_xp_multiplier(self, key, value):
        self._send_setting_to_server(key, value)

    def on_toggle_debug(self, key, value):
        self._send_setting_to_server(key, value)

    def on_toggle_repair_xp(self, key, value):
        self._send_setting_to_server(key, value)
        self.enable_repair_xp = value
        self._update_repair_locks()

    def on_toggle_repair_material(self, key, value):
        self._send_setting_to_server(key, value)
        self.enable_repair_material = value
        self._update_repair_locks()