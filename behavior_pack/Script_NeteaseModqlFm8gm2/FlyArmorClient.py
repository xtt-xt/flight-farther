# -*- coding: utf-8 -*-
# ==================== 飞行之羽模组 - 客户端 ====================

import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()
clientCompFactory = clientApi.GetEngineCompFactory()
clientEngineNamespace = clientApi.GetEngineNamespace()
clientEngineSystemName = clientApi.GetEngineSystemName()

# ==================== 前置(CardRegistry)卡片常量 ====================
MAIN_CARD_ID = "fly_armor"      # 主卡片 id
MAIN_CARD_ICON = "textures/ui/xtt_fly_feather"  # 主卡片图标（本模组资源包）

# 服务端子卡片下的中间卡片（按主题分类，icon 取自前置资源包 textures/ui/icon/）
SERVER_MIDDLE_GROUPS = [
    ("fly_effect", "状态效果", "textures/ui/icon/behaviour-packs-icon"),
    ("fly_durability", "耐久设置", "textures/ui/icon/resource-packs-icon"),
    ("fly_repair", "修复设置", "textures/ui/icon/advanced-icon"),
    ("fly_recipe", "配方", "textures/ui/icon/general-icon"),
    ("fly_permission", "权限管理", "textures/ui/icon/multiplayer-icon"),
    ("fly_debug", "调试", "textures/ui/icon/debug"),
]

# 客户端子卡片下的中间卡片（调试页，风格与前置一致）
CLIENT_MIDDLE_GROUPS = [
    ("fly_debug_client", "调试", "textures/ui/icon/debug"),
]

# ===== 调试页：复制日志到剪贴板（风格与前置一致） =====
EXPORT_COUNT_MENU = "fly_export_log_count"       # 导出数量折叠菜单（客户端/服务端共用）
EXPORT_COUNT_OPTIONS = (
    ("50", "50条"),
    ("100", "100条"),
    ("200", "200条"),
    ("500", "500条"),
)
DEFAULT_EXPORT_COUNT = "200"
CLIENT_COPY_COUNT = "fly_copy_client_count"  # 客户端导出数量（折叠菜单项）
CLIENT_COPY_BTN = "fly_copy_client_log"      # 客户端复制按钮
SERVER_COPY_COUNT = "fly_copy_server_count"  # 服务端导出数量（折叠菜单项）
SERVER_COPY_BTN = "fly_copy_server_log"      # 服务端复制按钮

# ===== 逐装备 =====
ARMOR_KEYS = ["fly", "ender", "eternal", "swift"]
EFFECT_ARMOR_KEYS = ["ender", "swift"]  # 仅这两个有被动状态效果
ARMOR_DISPLAY = {
    "fly": "飞行之羽",
    "ender": "末影之羽",
    "eternal": "不朽之羽",
    "swift": "迅捷之羽",
}
# 修复默认：(经验, 修复物品id)，与服务端 FLY_ARMOR_CONFIG 一致
REPAIR_DEFAULTS = {
    "fly": (1, "minecraft:feather"),
    "ender": (1, "minecraft:dragon_breath"),
    "eternal": (1, "minecraft:phantom_membrane"),
    "swift": (2, "minecraft:rabbit_foot"),
}

# ===== 飞行耐久：组合开关弹窗（CardToggle） =====
DURATION_TOGGLE_ID = "fly_flight_duration"  # 组合开关数据集 id
DURATION_OPTION = "dur_"  # 选项 id 前缀（选项 id = 前缀 + 装备key）

# ===== 是否兼容耐久附魔：组合开关弹窗（CardToggle） =====
UNBREAKING_TOGGLE_ID = "fly_unbreaking"  # 组合开关数据集 id
UNBREAKING_OPTION = "unb_"  # 选项 id 前缀（选项 id = 前缀 + 装备key）
ARMOR_KEY_TO_ITEM = {
    "fly": "fly_feather:fly_feather",
    "ender": "fly_feather:ender_feather",
    "eternal": "fly_feather:eternal_feather",
    "swift": "fly_feather:swift_feather",
}

# ===== 可修复装备：组合开关弹窗（CardToggle） =====
REPAIRABLE_TOGGLE_ID = "fly_repairable"  # 组合开关数据集 id
REPAIRABLE_OPTION = "repa_"  # 选项 id 前缀（选项 id = 前缀 + 装备key）

# ===== 修复设置：3 个新组合开关弹窗（CardToggle） =====
CONSUME_TOGGLE_ID = "fly_repair_consume"    # 是否消耗物品
CONSUME_OPTION = "consume_"                  # 选项前缀 + 装备key
XP_TOGGLE_ID = "fly_repair_xp"              # 修复所需经验
XP_OPTION = "xpref_"
MATERIAL_TOGGLE_ID = "fly_repair_material"  # 修复所需物品id
MATERIAL_OPTION = "matref_"

# ===== 权限管理：锁定模式 + 组合开关弹窗（CardToggle） =====
PERMISSION_TOGGLE_ID = "fly_permission_levels"  # 组合开关数据集 id
PERMISSION_OPTION = "perm_"  # 选项 id 前缀（选项 id = 前缀 + 权限档）
PERMISSION_ROLES = [
    ("visitor", "访客"),
    ("member", "成员"),
    ("operator", "操作员"),
    ("custom", "自定义"),
]

# 内容项 item_id -> (子卡片key, 中间卡片 id)
ITEM_GROUPS = {
    "enable_ender_effect": ("server", "fly_effect"),
    "enable_ender_full": ("server", "fly_effect"),
    "enable_swift_effect": ("server", "fly_effect"),
    "enable_real_time_durability": ("server", "fly_durability"),
    "enable_recipe_fly": ("server", "fly_recipe"),
    "enable_recipe_ender": ("server", "fly_recipe"),
    "enable_recipe_eternal": ("server", "fly_recipe"),
    "enable_recipe_swift": ("server", "fly_recipe"),
    "debug_mode": ("server", "fly_debug"),
    "client_log_output": ("client", "fly_debug_client"),
    SERVER_COPY_COUNT: ("server", "fly_debug"),
    SERVER_COPY_BTN: ("server", "fly_debug"),
}
for _armor_key in ARMOR_KEYS:
    ITEM_GROUPS["enable_durability_" + _armor_key] = ("server", "fly_durability")
    ITEM_GROUPS["enable_unbreaking_" + _armor_key] = ("server", "fly_durability")
ITEM_GROUPS["open_flight_dur"] = ("server", "fly_durability")
ITEM_GROUPS["open_unbreaking"] = ("server", "fly_durability")
for _armor_key in EFFECT_ARMOR_KEYS:
    ITEM_GROUPS["enable_effect_durability_" + _armor_key] = ("server", "fly_durability")
for _armor_key in ARMOR_KEYS:
    ITEM_GROUPS["repairable_" + _armor_key] = ("server", "fly_repair")
    ITEM_GROUPS["repair_consume_material_" + _armor_key] = ("server", "fly_repair")
    ITEM_GROUPS["repair_xp_" + _armor_key] = ("server", "fly_repair")
    ITEM_GROUPS["repair_material_" + _armor_key] = ("server", "fly_repair")
ITEM_GROUPS["open_repairable"] = ("server", "fly_repair")
ITEM_GROUPS["open_consume"] = ("server", "fly_repair")
ITEM_GROUPS["open_xp"] = ("server", "fly_repair")
ITEM_GROUPS["open_material"] = ("server", "fly_repair")
# 各服务端分页的"重置本页"按钮（不含调试）
for _rcard in ("fly_effect", "fly_durability", "fly_repair", "fly_recipe"):
    ITEM_GROUPS["reset_" + _rcard] = ("server", _rcard)
# 权限管理
ITEM_GROUPS["permission_lock_mode"] = ("server", "fly_permission")
ITEM_GROUPS["open_permission"] = ("server", "fly_permission")
for _role, _name in PERMISSION_ROLES:
    ITEM_GROUPS["permission_" + _role] = ("server", "fly_permission")

# 服务端全局设置内容项（需按服务端 OP 权限锁定）
LOCKABLE_KEYS = [k for k, (sk, _) in ITEM_GROUPS.items() if sk == "server"]


class FlyArmorClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        # 前置(CardRegistry) API 引用，延迟导入后赋值
        self._card_register = None
        self._card_middle = None
        self._card_create = None
        self._card_getitem = None
        self._card_setvalue = None
        self._card_setlocked = None
        self._card_clearlocked = None
        self._card_resetgroup = None
        self._card_regtoggle = None
        self._card_addtogopt = None
        self._card_addtogbtn = None
        self._card_opentoggle = None
        self._card_closetoggle = None
        self._card_gettogstate = None
        self._card_settogstate = None
        self._card_getsetting = None
        self._card_ready = False
        self.has_permission = False
        self._client_log_enabled = False  # 客户端调试日志输出开关
        self._card_regmenu = None
        self._last_synced_settings = None  # 最近一次已同步到 UI 的服务端设置
        self._poll_timer = None
        self._pending_permission_args = None  # 缓存提前到达的权限事件

        self.ListenForEvent(clientEngineNamespace, clientEngineSystemName,
                            "UiInitFinished", self, self.on_ui_init)
        self.ListenForEvent("FlyArmorServer", "FlyArmorServerSystem",
                            "FlyArmorPermissionEvent", self, self.on_permission_event)
        self.ListenForEvent(clientEngineNamespace, clientEngineSystemName,
                            "PushScreenEvent", self, self.on_push_screen)
        # 服务端回退事件：材料id/经验无效时还原 UI
        self.ListenForEvent("FlyArmorServer", "FlyArmorServerSystem",
                            "FlyArmorRevertSettingEvent", self, self.on_revert_setting)
        # 自定义指令镜像刷新：指令在服务端改值后，刷新本地面板镜像（无前置时自动忽略）
        self.ListenForEvent("FlyArmorServer", "FlyArmorServerSystem",
                            "Script_NeteaseModqlFm8gm2_SettingMirrorSync", self, self.on_mirror_sync)

    # ==================== 前置(CardRegistry)设置卡片注册 ====================

    def on_ui_init(self, args):
        localPlayerId = clientApi.GetLocalPlayerId()
        if not localPlayerId:
            return
        # 延迟导入前置 CardRegistryApi，避免多 Addon 加载顺序导致的 ImportError
        try:
            from Script_NeteaseMod9sPMlz0K.CardRegistryApi import (
                RegisterMainCard, RegisterMiddleCard, CreateContentInst,
                RegisterCollapsibleMenu,
                GetContentItem, GetSettingValue, SetSettingValue, SetLocked,
                ResetGroupSettings,
                RegisterCardToggle, AddCardToggleOption, AddCardToggleButton,
                OpenCardToggle, CloseCardToggle, GetCardToggleState, SetCardToggleState,
            )
            from Script_NeteaseMod9sPMlz0K.SettingState import ClearSettingLocked
            self._card_register = RegisterMainCard
            self._card_middle = RegisterMiddleCard
            self._card_create = CreateContentInst
            self._card_regmenu = RegisterCollapsibleMenu
            self._card_getitem = GetContentItem
            self._card_getsetting = GetSettingValue
            self._card_setvalue = SetSettingValue
            self._card_setlocked = SetLocked
            self._card_clearlocked = ClearSettingLocked
            self._card_resetgroup = ResetGroupSettings
            self._card_regtoggle = RegisterCardToggle
            self._card_addtogopt = AddCardToggleOption
            self._card_addtogbtn = AddCardToggleButton
            self._card_opentoggle = OpenCardToggle
            self._card_closetoggle = CloseCardToggle
            self._card_gettogstate = GetCardToggleState
            self._card_settogstate = SetCardToggleState
            # 读取客户端调试日志输出的持久化状态
            self._client_log_enabled = bool(GetSettingValue(
                MAIN_CARD_ID, "client", "fly_debug_client",
                "client_log_output", default=False))
        except ImportError:
            print "==== [飞行之羽] 前置模组(CardRegistry)未安装，跳过设置界面注册 ===="
            return

        self._register_settings_cards()
        self._register_flight_duration_toggle()
        self._register_unbreaking_toggle()
        self._register_repairable_toggle()
        self._register_repair_consume_toggle()
        self._register_repair_xp_toggle()
        self._register_repair_material_toggle()
        self._register_permission_toggle()
        self._card_ready = True
        self._client_debug_print("设置卡片注册完成，客户端调试日志开关开启")

        self._lock_all_controls(True)
        self.NotifyToServer("FlyArmorRequestPermissionEvent", {
            "playerId": localPlayerId
        })
        self._start_permission_poll(localPlayerId)
        # 如果之前有缓存的权限事件，现在UI已就绪，处理它
        if self._pending_permission_args is not None:
            self._apply_permission_args(self._pending_permission_args)
            self._pending_permission_args = None

    def _register_settings_cards(self):
        """注册主卡片 + 中间卡片（服务端主题 + 客户端调试）+ 内容项（替换原生设置）"""
        self._card_register(MAIN_CARD_ID, "飞行之羽", MAIN_CARD_ICON)
        for card_id, name, icon in SERVER_MIDDLE_GROUPS:
            self._card_middle(MAIN_CARD_ID, "server", card_id, name, icon)
        for card_id, name, icon in CLIENT_MIDDLE_GROUPS:
            self._card_middle(MAIN_CARD_ID, "client", card_id, name, icon)

        # 注册"导出数量"折叠菜单（客户端/服务端复制日志共用）
        self._card_regmenu(EXPORT_COUNT_MENU, "导出数量", EXPORT_COUNT_OPTIONS)

        # ===== 服务端：状态效果 =====
        inst = self._card_create(MAIN_CARD_ID, "server", "fly_effect")
        inst.AddSwitch("enable_ender_effect", "启用末影之羽的被动状态效果（默认开启）",
                       litle="末影之羽状态效果",
                       default_value=True, on_toggle=self.on_toggle_ender)
        inst.AddSwitch("enable_ender_full", "开启后在所有维度获得末地级别的增益（默认关闭）",
                       litle="末影之羽完整版",
                       default_value=False, on_toggle=self.on_toggle_ender_full)
        inst.AddSwitch("enable_swift_effect", "启用迅捷之羽的被动状态效果（默认开启）",
                       litle="迅捷之羽状态效果",
                       default_value=True, on_toggle=self.on_toggle_swift)
        inst.AddResetButton("reset_fly_effect", on_click=self.on_reset_page)

        # ===== 服务端：耐久设置 =====
        inst = self._card_create(MAIN_CARD_ID, "server", "fly_durability")
        inst.AddSwitch("enable_real_time_durability",
                       "开启则飞行时实时扣除耐久；关闭则飞行中延后累计，停止飞行后一次性结算（默认开启）",
                       litle="实时减少耐久",
                       default_value=True, on_toggle=self.on_toggle_item)
        inst.AddButton("open_flight_dur", "逐羽设置飞行时是否消耗耐久",
                       "打开", litle="飞行耐久消耗",
                       on_click=self.on_open_flight_dur_toggle)
        inst.AddButton("open_unbreaking", "逐羽设置是否兼容耐久附魔（附魔可有概率不消耗耐久）",
                       "打开", litle="耐久附魔",
                       on_click=self.on_open_unbreaking_toggle)
        inst.AddText("effect_dur_title", "", "状态效果耐久消耗")
        for _ak in EFFECT_ARMOR_KEYS:
            inst.AddSwitch("enable_effect_durability_" + _ak, "触发状态效果时消耗耐久（默认开启）",
                           litle=ARMOR_DISPLAY[_ak],
                           default_value=True, on_toggle=self.on_toggle_item)
        inst.AddResetButton("reset_fly_durability", on_click=self.on_reset_page)

        # ===== 服务端：修复设置（逐装备，均用 CardToggle 弹窗） =====
        inst = self._card_create(MAIN_CARD_ID, "server", "fly_repair")
        inst.AddText("repair_note", "", "各羽修复设置分别弹窗管理；不可修复/不消耗物品的羽，其对应弹窗内选项会自动锁定；修复物品id填写无效将提示并还原")
        inst.AddButton("open_repairable", "逐羽设置该装备是否可被修复",
                       "打开", litle="可修复的装备",
                       on_click=self.on_open_repairable_toggle)
        inst.AddButton("open_consume", "逐羽设置修复时是否消耗物品",
                       "打开", litle="修复时是否消耗物品",
                       on_click=self.on_open_repair_consume_toggle)
        inst.AddButton("open_xp", "逐羽设置修复所需经验，0=不消耗",
                       "打开", litle="修复所需经验",
                       on_click=self.on_open_repair_xp_toggle)
        inst.AddButton("open_material", "逐羽设置修复所需物品id（无效将提示并还原）",
                       "打开", litle="修复所需物品id",
                       on_click=self.on_open_repair_material_toggle)
        inst.AddResetButton("reset_fly_repair", on_click=self.on_reset_page)

        # ===== 服务端：配方（动态注册，服务端全局配置） =====
        inst = self._card_create(MAIN_CARD_ID, "server", "fly_recipe")
        inst.AddText("recipe_note", "", "各羽配方开关可单独设置，添加或关闭配方均需重启世界生效")
        inst.AddSwitch("enable_recipe_fly", "该羽的合成配方，改动需重启世界生效（默认开启）",
                       litle="飞行之羽",
                       default_value=True, on_toggle=self.on_toggle_recipe)
        inst.AddSwitch("enable_recipe_ender", "该羽的合成配方，改动需重启世界生效（默认开启）",
                       litle="末影之羽",
                       default_value=True, on_toggle=self.on_toggle_recipe)
        inst.AddSwitch("enable_recipe_eternal", "该羽的合成配方，改动需重启世界生效（默认开启）",
                       litle="不朽之羽",
                       default_value=True, on_toggle=self.on_toggle_recipe)
        inst.AddSwitch("enable_recipe_swift", "该羽的合成配方，改动需重启世界生效（默认开启）",
                       litle="迅捷之羽",
                       default_value=True, on_toggle=self.on_toggle_recipe)
        inst.AddResetButton("reset_fly_recipe", on_click=self.on_reset_page)

        # ===== 服务端：权限管理（锁定模式 + 允许修改设置的权限档） =====
        inst = self._card_create(MAIN_CARD_ID, "server", "fly_permission")
        inst.AddSwitch("permission_lock_mode",
                       "开启后仅操作员（房主/管理员）可修改设置；关闭后可自定义允许的权限档",
                       litle="锁定模式",
                       default_value=True, on_toggle=self.on_lock_mode_toggle)
        inst.AddButton("open_permission", "设置允许修改模组设置的权限档",
                       "打开", litle="允许的权限",
                       on_click=self.on_open_permission_toggle)

        # ===== 服务端：调试（全局，仅房主/管理员可改） =====
        inst = self._card_create(MAIN_CARD_ID, "server", "fly_debug")
        inst.AddSwitch("debug_mode", "在控制台输出服务端调试日志（默认关闭）",
                       litle="模组调试",
                       default_value=False, on_toggle=self.on_toggle_debug)
        inst.AddCollapsibleMenu(SERVER_COPY_COUNT, "选择要复制到剪贴板的日志条数",
                                EXPORT_COUNT_MENU, litle="复制数量",
                                default_selected_id=DEFAULT_EXPORT_COUNT)
        inst.AddButton(SERVER_COPY_BTN, "复制服务端调试日志到剪贴板",
                       "复制日志", on_click=self.on_copy_server_log)

        # ===== 客户端：调试（每个人各自独立，本地存储） =====
        inst = self._card_create(MAIN_CARD_ID, "client", "fly_debug_client")
        inst.AddSwitch("client_log_output", "在客户端控制台输出调试日志，每人独立（默认关闭）",
                       litle="日志输出",
                       default_value=False, on_toggle=self.on_toggle_client_log)
        inst.AddCollapsibleMenu(CLIENT_COPY_COUNT, "选择要复制到剪贴板的日志条数",
                                EXPORT_COUNT_MENU, litle="复制数量",
                                default_selected_id=DEFAULT_EXPORT_COUNT)
        inst.AddButton(CLIENT_COPY_BTN, "复制客户端调试日志到剪贴板",
                       "复制日志", on_click=self.on_copy_client_log)

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

    # ==================== 权限事件 ====================

    def _set_ui_value(self, key, value):
        """将值写入前置设置状态，并刷新已打开的 UI（服务器为设置源头）"""
        if not self._card_ready:
            return
        group = ITEM_GROUPS.get(key)
        if not group:
            return
        sub_key, mid = group
        try:
            self._card_setvalue(MAIN_CARD_ID, sub_key, mid, key, value)
        except Exception:
            pass

    def _lock_control_data(self, key, locked):
        """更新指定内容项的数据层锁定状态（切换分组时重建会读取 item.locked）。

        同时清除该键的持久化锁定（::locked）：本模组锁定由服务端按 OP 实时
        决定，需避免房主曾解锁被保存成过期解锁态，导致非房主打开时穿透鉴权。
        """
        mid = ITEM_GROUPS.get(key)
        if not mid:
            return
        sub_key, mid = mid
        try:
            it = self._card_getitem(MAIN_CARD_ID, sub_key, mid, key)
            if it and hasattr(it, "SetLocked"):
                it.SetLocked(locked)
        except Exception:
            pass
        try:
            self._card_clearlocked(MAIN_CARD_ID, sub_key, mid, key)
        except Exception:
            pass

    def _lock_all_controls(self, locked):
        """无权限时锁定所有设置控件（数据层 + 当前显示分组 UI）"""
        if not self._card_ready:
            return
        for key in LOCKABLE_KEYS:
            self._lock_control_data(key, locked)
            try:
                self._card_setlocked(key, locked)
            except Exception:
                pass

    def _apply_item_lock(self, key, locked):
        """设置单个内容项锁定（数据层 + 当前显示分组 UI）。"""
        self._lock_control_data(key, locked)
        try:
            self._card_setlocked(key, locked)
        except Exception:
            pass

    # ==================== 飞行耐久组合开关弹窗（CardToggle） ====================

    def _register_flight_duration_toggle(self):
        """注册"飞行耐久消耗"组合开关数据集（multi 多选 + 底部应用按钮）。"""
        if not self._card_regtoggle:
            return
        self._card_regtoggle(DURATION_TOGGLE_ID, "飞行耐久消耗", mode="multi")
        for ak in ARMOR_KEYS:
            self._card_addtogopt(DURATION_TOGGLE_ID, DURATION_OPTION + ak,
                                 ARMOR_KEY_TO_ITEM[ak], desc=ARMOR_DISPLAY[ak],
                                 default_on=True)
        self._card_addtogbtn(DURATION_TOGGLE_ID, "应用到服务端",
                             self.on_apply_flight_dur_toggle)

    def _read_setting_bool(self, key, default=False):
        """读取前置本地存储中的设置 bool 值（用于弹窗初始状态）。"""
        if not self._card_ready or not self._card_getsetting:
            return default
        group = ITEM_GROUPS.get(key)
        if not group:
            return default
        sub, mid = group
        try:
            return bool(self._card_getsetting(MAIN_CARD_ID, sub, mid, key, default))
        except Exception:
            return default

    def _read_setting_str(self, key, default=""):
        """读取前置本地存储中的设置字符串值（用于修复经验/物品id弹窗初始显示）。"""
        if not self._card_ready or not self._card_getsetting:
            return default
        group = ITEM_GROUPS.get(key)
        if not group:
            return default
        sub, mid = group
        try:
            v = self._card_getsetting(MAIN_CARD_ID, sub, mid, key, default)
            if v is None:
                return default
            return str(v)
        except Exception:
            return default

    def on_open_flight_dur_toggle(self, screenNode, item_id):
        """打开"飞行耐久消耗"弹窗前，用当前设置同步各选项状态。"""
        if not self._card_settogstate or not self._card_opentoggle:
            return
        for ak in ARMOR_KEYS:
            cur = self._read_setting_bool("enable_durability_" + ak, True)
            self._card_settogstate(DURATION_TOGGLE_ID, DURATION_OPTION + ak, cur)
        self._card_opentoggle(DURATION_TOGGLE_ID)

    def on_apply_flight_dur_toggle(self, screenNode, toggle_id, state_dict):
        """弹窗底部"应用到服务端"：把逐羽开关状态写回服务端。"""
        for ak in ARMOR_KEYS:
            opt = DURATION_OPTION + ak
            state = bool(state_dict.get(opt, True))
            self._send_setting_to_server("enable_durability_" + ak, state)
        if self._card_closetoggle:
            self._card_closetoggle()

    # ==================== 是否兼容耐久附魔 组合开关弹窗（CardToggle） ====================

    def _register_unbreaking_toggle(self):
        """注册"是否兼容耐久附魔"组合开关数据集（multi 多选 + 底部应用按钮）。"""
        if not self._card_regtoggle:
            return
        self._card_regtoggle(UNBREAKING_TOGGLE_ID, "耐久附魔", mode="multi")
        for ak in ARMOR_KEYS:
            self._card_addtogopt(UNBREAKING_TOGGLE_ID, UNBREAKING_OPTION + ak,
                                 ARMOR_KEY_TO_ITEM[ak], desc=ARMOR_DISPLAY[ak],
                                 default_on=True)
        self._card_addtogbtn(UNBREAKING_TOGGLE_ID, "应用到服务端",
                             self.on_apply_unbreaking_toggle)

    def on_open_unbreaking_toggle(self, screenNode, item_id):
        """打开"耐久附魔"弹窗前，用当前设置同步各选项状态。"""
        if not self._card_settogstate or not self._card_opentoggle:
            return
        for ak in ARMOR_KEYS:
            cur = self._read_setting_bool("enable_unbreaking_" + ak, True)
            self._card_settogstate(UNBREAKING_TOGGLE_ID, UNBREAKING_OPTION + ak, cur)
        self._card_opentoggle(UNBREAKING_TOGGLE_ID)

    def on_apply_unbreaking_toggle(self, screenNode, toggle_id, state_dict):
        """弹窗底部"应用到服务端"：写回逐羽是否兼容耐久附魔。"""
        for ak in ARMOR_KEYS:
            opt = UNBREAKING_OPTION + ak
            state = bool(state_dict.get(opt, True))
            self._send_setting_to_server("enable_unbreaking_" + ak, state)
        if self._card_closetoggle:
            self._card_closetoggle()

    # ==================== 可修复装备组合开关弹窗（CardToggle） ====================

    def _register_repairable_toggle(self):
        """注册"可修复的装备"组合开关数据集（multi 多选 + 底部应用按钮）。"""
        if not self._card_regtoggle:
            return
        self._card_regtoggle(REPAIRABLE_TOGGLE_ID, "可修复的装备", mode="multi")
        for ak in ARMOR_KEYS:
            self._card_addtogopt(REPAIRABLE_TOGGLE_ID, REPAIRABLE_OPTION + ak,
                                 ARMOR_KEY_TO_ITEM[ak], desc=ARMOR_DISPLAY[ak],
                                 default_on=True)
        self._card_addtogbtn(REPAIRABLE_TOGGLE_ID, "应用到服务端",
                             self.on_apply_repairable_toggle)

    def on_open_repairable_toggle(self, screenNode, item_id):
        """打开"可修复的装备"弹窗前，用当前设置同步各选项状态。"""
        if not self._card_settogstate or not self._card_opentoggle:
            return
        for ak in ARMOR_KEYS:
            cur = self._read_setting_bool("repairable_" + ak, True)
            self._card_settogstate(REPAIRABLE_TOGGLE_ID, REPAIRABLE_OPTION + ak, cur)
        self._card_opentoggle(REPAIRABLE_TOGGLE_ID)

    def on_apply_repairable_toggle(self, screenNode, toggle_id, state_dict):
        """弹窗底部"应用到服务端"：写回逐羽可修复状态。"""
        for ak in ARMOR_KEYS:
            opt = REPAIRABLE_OPTION + ak
            state = bool(state_dict.get(opt, True))
            self._send_setting_to_server("repairable_" + ak, state)
            # 同步本地存储，供"关闭消耗耐久/可修复联动锁定"即时生效
            self._set_ui_value("repairable_" + ak, state)
        if self._card_closetoggle:
            self._card_closetoggle()

    # ==================== 修复时是否消耗物品 组合开关弹窗（CardToggle） ====================

    def _register_repair_consume_toggle(self):
        """注册"修复时是否消耗物品"组合开关数据集（multi 多选 + 底部应用按钮）。"""
        if not self._card_regtoggle:
            return
        self._card_regtoggle(CONSUME_TOGGLE_ID, "修复时是否消耗物品", mode="multi")
        for ak in ARMOR_KEYS:
            self._card_addtogopt(CONSUME_TOGGLE_ID, CONSUME_OPTION + ak,
                                 ARMOR_KEY_TO_ITEM[ak], desc=ARMOR_DISPLAY[ak],
                                 default_on=True, ctrl_type="toggle")
        self._card_addtogbtn(CONSUME_TOGGLE_ID, "应用到服务端",
                             self.on_apply_repair_consume_toggle)

    def on_open_repair_consume_toggle(self, screenNode, item_id):
        """打开"修复时是否消耗物品"弹窗前：重注册联动锁定 + 同步当前状态。"""
        if not self._card_settogstate or not self._card_opentoggle:
            return
        for ak in ARMOR_KEYS:
            # 不可修复 → 该羽"是否消耗物品"选项锁定
            locked = not self._read_setting_bool("repairable_" + ak, True)
            self._card_addtogopt(CONSUME_TOGGLE_ID, CONSUME_OPTION + ak,
                                 ARMOR_KEY_TO_ITEM[ak], desc=ARMOR_DISPLAY[ak],
                                 default_on=True, ctrl_type="toggle", locked=locked)
            cur = self._read_setting_bool("repair_consume_material_" + ak, True)
            self._card_settogstate(CONSUME_TOGGLE_ID, CONSUME_OPTION + ak, cur)
        self._card_opentoggle(CONSUME_TOGGLE_ID)

    def on_apply_repair_consume_toggle(self, screenNode, toggle_id, state_dict):
        """弹窗底部"应用到服务端"：写回逐羽是否消耗物品状态。"""
        for ak in ARMOR_KEYS:
            opt = CONSUME_OPTION + ak
            state = bool(state_dict.get(opt, True))
            self._send_setting_to_server("repair_consume_material_" + ak, state)
            self._set_ui_value("repair_consume_material_" + ak, state)
        if self._card_closetoggle:
            self._card_closetoggle()

    # ==================== 修复所需经验 组合开关弹窗（CardToggle） ====================

    def _register_repair_xp_toggle(self):
        """注册"修复所需经验"组合开关数据集（逐装备编辑框 + 底部应用按钮）。"""
        if not self._card_regtoggle:
            return
        self._card_regtoggle(XP_TOGGLE_ID, "修复所需经验", mode="multi")
        for ak in ARMOR_KEYS:
            self._card_addtogopt(XP_TOGGLE_ID, XP_OPTION + ak,
                                 ARMOR_KEY_TO_ITEM[ak], desc=ARMOR_DISPLAY[ak],
                                 default_value=str(REPAIR_DEFAULTS[ak][0]),
                                 ctrl_type="toggle_edit_box")
        self._card_addtogbtn(XP_TOGGLE_ID, "应用到服务端",
                             self.on_apply_repair_xp_toggle)

    def on_open_repair_xp_toggle(self, screenNode, item_id):
        """打开"修复所需经验"弹窗前：重注册联动锁定 + 同步当前输入。"""
        if not self._card_settogstate or not self._card_opentoggle:
            return
        for ak in ARMOR_KEYS:
            # 不可修复 → 该羽"经验"选项锁定
            locked = not self._read_setting_bool("repairable_" + ak, True)
            self._card_addtogopt(XP_TOGGLE_ID, XP_OPTION + ak,
                                 ARMOR_KEY_TO_ITEM[ak], desc=ARMOR_DISPLAY[ak],
                                 default_value=str(REPAIR_DEFAULTS[ak][0]),
                                 ctrl_type="toggle_edit_box", locked=locked)
            cur = self._read_setting_str("repair_xp_" + ak,
                                         str(REPAIR_DEFAULTS[ak][0]))
            self._card_settogstate(XP_TOGGLE_ID, XP_OPTION + ak, cur)
        self._card_opentoggle(XP_TOGGLE_ID)

    def on_apply_repair_xp_toggle(self, screenNode, toggle_id, state_dict):
        """弹窗底部"应用到服务端"：提交逐羽经验（服务端校验数字并回退非法值）。"""
        for ak in ARMOR_KEYS:
            opt = XP_OPTION + ak
            self._send_setting_to_server("repair_xp_" + ak, str(state_dict.get(opt, "")))
        if self._card_closetoggle:
            self._card_closetoggle()

    # ==================== 修复所需物品id 组合开关弹窗（CardToggle） ====================

    def _register_repair_material_toggle(self):
        """注册"修复所需物品id"组合开关数据集（逐装备编辑框 + 底部应用按钮）。"""
        if not self._card_regtoggle:
            return
        self._card_regtoggle(MATERIAL_TOGGLE_ID, "修复所需物品id", mode="multi")
        for ak in ARMOR_KEYS:
            self._card_addtogopt(MATERIAL_TOGGLE_ID, MATERIAL_OPTION + ak,
                                 ARMOR_KEY_TO_ITEM[ak], desc=ARMOR_DISPLAY[ak],
                                 default_value=REPAIR_DEFAULTS[ak][1],
                                 ctrl_type="toggle_edit_box")
        self._card_addtogbtn(MATERIAL_TOGGLE_ID, "应用到服务端",
                             self.on_apply_repair_material_toggle)

    def on_open_repair_material_toggle(self, screenNode, item_id):
        """打开"修复所需物品id"弹窗前：重注册联动锁定 + 同步当前输入。"""
        if not self._card_settogstate or not self._card_opentoggle:
            return
        for ak in ARMOR_KEYS:
            repairable = self._read_setting_bool("repairable_" + ak, True)
            consume = self._read_setting_bool("repair_consume_material_" + ak, True)
            # 不可修复 或 不消耗物品 → 该羽"物品id"选项锁定
            locked = (not repairable) or (not consume)
            self._card_addtogopt(MATERIAL_TOGGLE_ID, MATERIAL_OPTION + ak,
                                 ARMOR_KEY_TO_ITEM[ak], desc=ARMOR_DISPLAY[ak],
                                 default_value=REPAIR_DEFAULTS[ak][1],
                                 ctrl_type="toggle_edit_box", locked=locked)
            cur = self._read_setting_str("repair_material_" + ak,
                                         REPAIR_DEFAULTS[ak][1])
            self._card_settogstate(MATERIAL_TOGGLE_ID, MATERIAL_OPTION + ak, cur)
        self._card_opentoggle(MATERIAL_TOGGLE_ID)

    def on_apply_repair_material_toggle(self, screenNode, toggle_id, state_dict):
        """弹窗底部"应用到服务端"：提交逐羽物品id（服务端校验存在性并回退）。"""
        for ak in ARMOR_KEYS:
            opt = MATERIAL_OPTION + ak
            self._send_setting_to_server("repair_material_" + ak, str(state_dict.get(opt, "")))
        if self._card_closetoggle:
            self._card_closetoggle()

    # ==================== 权限管理：锁定模式 + 权限档组合开关弹窗（CardToggle） ====================

    def _register_permission_toggle(self):
        """注册"允许修改设置的权限档"组合开关数据集（multi 多选 + 底部应用按钮）。"""
        if not self._card_regtoggle:
            return
        self._card_regtoggle(PERMISSION_TOGGLE_ID, "允许的权限", mode="multi")
        for role, name in PERMISSION_ROLES:
            # default_on：与服务端默认一致（默认 operator 开）
            default_on = (role == "operator")
            self._card_addtogopt(PERMISSION_TOGGLE_ID, PERMISSION_OPTION + role,
                                 self._permission_role_item(role), desc=name,
                                 default_on=default_on)
        self._card_addtogbtn(PERMISSION_TOGGLE_ID, "应用到服务端",
                             self.on_apply_permission_toggle)

    def _permission_role_item(self, role):
        """各权限档使用的物品图标。"""
        icons = {
            "visitor": "minecraft:glass",
            "member": "minecraft:book",
            "operator": "minecraft:command_block",
            "custom": "minecraft:name_tag",
        }
        return icons.get(role, "minecraft:paper")

    def _update_permission_locks(self):
        """锁定模式下，锁定"允许的权限"按钮；关闭锁定时解锁，便于打开弹窗配置。"""
        if not self._card_ready:
            return
        locked = self._read_setting_bool("permission_lock_mode", True)
        self._apply_item_lock("open_permission", locked)

    def on_lock_mode_toggle(self, screenNode, item_id, state):
        """锁定模式开关：发服务端 + 刷新权限按钮联动锁定。"""
        self._send_setting_to_server(item_id, state)
        self._set_ui_value("permission_lock_mode", bool(state))
        self._update_permission_locks()

    def on_open_permission_toggle(self, screenNode, item_id):
        """打开"允许的权限"弹窗前，用当前设置同步各选项状态。"""
        if not self._card_settogstate or not self._card_opentoggle:
            return
        for role, _name in PERMISSION_ROLES:
            cur = self._read_setting_bool("permission_" + role, role == "operator")
            self._card_settogstate(PERMISSION_TOGGLE_ID, PERMISSION_OPTION + role, cur)
        self._card_opentoggle(PERMISSION_TOGGLE_ID)

    def on_apply_permission_toggle(self, screenNode, toggle_id, state_dict):
        """弹窗底部"应用到服务端"：写回各权限档允许状态。"""
        for role, _name in PERMISSION_ROLES:
            opt = PERMISSION_OPTION + role
            state = bool(state_dict.get(opt, role == "operator"))
            self._send_setting_to_server("permission_" + role, state)
            self._set_ui_value("permission_" + role, state)
        if self._card_closetoggle:
            self._card_closetoggle()

    def _client_debug_print(self, *args):
        """客户端调试日志：仅当客户端调试日志开关开启时输出到控制台。"""
        if not self._client_log_enabled:
            return
        print "==== [飞行之羽][客户端调试] %s ====" % (" ".join(str(a) for a in args))

    def on_permission_event(self, args):
        # 如果UI还没初始化好，先缓存起来
        if not self._card_ready:
            self._pending_permission_args = args
            return
        self._apply_permission_args(args)

    def _apply_permission_args(self, args):
        """应用权限事件参数，必须在卡片注册完成后调用"""
        has_perm = args.get("hasPermission", False)
        settings = args.get("settings", {})
        # 同步服务端持久化设置到客户端UI（仅在实际发生变化时，避免轮询刷屏/重复写入）
        if settings and self._card_ready:
            if settings != self._last_synced_settings:
                for key, value in settings.items():
                    # 逐装备：开关=bool，经验=int，材料id=str，直接交存储按类型处理
                    self._set_ui_value(key, value)
                self._last_synced_settings = dict(settings)
                self._client_debug_print("已按服务端设置同步 UI 值")
        # 权限状态变化时才刷新锁定
        if self.has_permission != has_perm:
            self.has_permission = has_perm
            self._client_debug_print("权限变化 -> hasPermission=%s" % has_perm)
            if has_perm:
                self._lock_all_controls(False)
                self._update_permission_locks()
            else:
                self._lock_all_controls(True)
                self._update_permission_locks()

    def on_push_screen(self, args):
        """监听原生界面入栈（包括前置设置界面），每次打开都重新请求权限刷新锁定状态"""
        if not self._card_ready:
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

    def on_toggle_item(self, screenNode, item_id, state):
        """通用逐装备开关回调：耐久消耗等开关立即发服务端。"""
        self._send_setting_to_server(item_id, state)

    def on_toggle_ender(self, screenNode, item_id, state):
        self._send_setting_to_server(item_id, state)

    def on_toggle_swift(self, screenNode, item_id, state):
        self._send_setting_to_server(item_id, state)

    def on_toggle_ender_full(self, screenNode, item_id, state):
        self._send_setting_to_server(item_id, state)

    def on_toggle_recipe(self, screenNode, item_id, state):
        """配方开关回调：修改服务端全局配置，重启世界后生效。"""
        self._send_setting_to_server(item_id, state)

    def on_toggle_debug(self, screenNode, item_id, state):
        self._send_setting_to_server(item_id, state)

    def on_revert_setting(self, args):
        """服务端回退事件：非法材料id/经验还原为服务端给定值。"""
        key = args.get("key")
        value = args.get("value")
        if key and value is not None:
            self._set_ui_value(key, value)
            self._client_debug_print("服务端回退 %s = %s" % (key, value))

    def on_mirror_sync(self, args):
        """自定义指令镜像刷新：把完整键 fly_armor.server.default.<item> 还原为 item 并写入本地镜像。

        只同步面板镜像，不写服务端、不回执、不鉴权；面板未注册（无前置）时自动忽略。
        """
        full_key = args.get("key", "")
        value = args.get("value")
        prefix = "fly_armor.server.default."
        if not full_key.startswith(prefix) or value is None:
            return
        item = full_key[len(prefix):]
        if not item:
            return
        self._set_ui_value(item, value)
        self._client_debug_print("指令镜像 %s = %s" % (item, value))

    def on_reset_page(self, screenNode, item_id):
        """「重置本页」：重置当前服务端分页为默认，并通知服务端持久化 + 推送。"""
        group = getattr(screenNode, "mCurrentRightGroup", None)
        if not group or len(group) < 3:
            return
        main_card_id, sub_key, mid = group
        try:
            if self._card_resetgroup:
                self._card_resetgroup(main_card_id, sub_key, mid)
        except Exception:
            pass
        localPlayerId = clientApi.GetLocalPlayerId()
        self.NotifyToServer("FlyArmorResetGroupEvent", {
            "playerId": localPlayerId,
            "middle_card_id": mid
        })
        # 重置后权限按钮联动锁定按默认锁模式刷新
        self._update_permission_locks()

    def on_toggle_client_log(self, screenNode, item_id, state):
        """客户端调试日志输出开关回调：立即切换，不发给服务端。"""
        self._client_log_enabled = bool(state)

    def _read_copy_count(self, sub_key, card_id, item_id):
        """读取复制数量的折叠菜单当前选中条数（取不到回退 200）。"""
        if not self._card_ready:
            return 200
        try:
            it = self._card_getitem(MAIN_CARD_ID, sub_key, card_id, item_id)
            if it is not None:
                return int(getattr(it, "value", "200"))
        except Exception:
            pass
        return 200

    def _get_dependency_client_system(self):
        """延迟获取前置客户端系统（用于日志导出）。"""
        try:
            from Script_NeteaseMod9sPMlz0K.CardRegistryApi import _g_ClientSystem
            return _g_ClientSystem
        except Exception:
            return None

    def on_copy_client_log(self, screenNode, item_id):
        """复制客户端最近 N 条调试日志到剪贴板。"""
        g = self._get_dependency_client_system()
        if g:
            g.CopyClientLogToClipboard(
                self._read_copy_count("client", "fly_debug_client", CLIENT_COPY_COUNT))

    def on_copy_server_log(self, screenNode, item_id):
        """请求服务端最近 N 条调试日志并复制到本机剪贴板。"""
        g = self._get_dependency_client_system()
        if g:
            g.RequestServerLogDump(
                self._read_copy_count("server", "fly_debug", SERVER_COPY_COUNT))