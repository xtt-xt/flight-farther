# -*- coding: utf-8 -*-
# ==================== 飞行之羽模组 - 服务端 ====================

import mod.server.extraServerApi as serverApi
import random
from mod.common import minecraftEnum as Enum

ServerSystem = serverApi.GetServerSystemCls()
serverCompFactory = serverApi.GetEngineCompFactory()
engineNamespace = serverApi.GetEngineNamespace()
engineSystemName = serverApi.GetEngineSystemName()


# ==================== 全局常量 ====================
FLY_ARMOR_CONFIG = {
    "fly_feather:fly_feather": {
        "display_name": "飞行之羽",
        "default_max_durability": 432,
        "repair_material": "minecraft:feather",
        "repair_percent": 0.25,
        "repair_xp_cost": 1,
    },
    "fly_feather:eternal_feather": {
        "display_name": "不朽之羽",
        "default_max_durability": 2651,
        "repair_material": "minecraft:phantom_membrane",
        "repair_percent": 0.25,
        "repair_xp_cost": 1,
    },
    "fly_feather:ender_feather": {
        "display_name": "末影之羽",
        "default_max_durability": 1296,
        "repair_material": "minecraft:dragon_breath",
        "repair_percent": 0.25,
        "repair_xp_cost": 1,
    },
    "fly_feather:swift_feather": {
        "display_name": "迅捷之羽",
        "default_max_durability": 432,
        "repair_material": "minecraft:rabbit_foot",
        "repair_percent": 0.75,
        "repair_xp_cost": 2,
    }
}


def _get_material_display_name(material_id):
    mapping = {
        "minecraft:feather": "羽毛",
        "minecraft:phantom_membrane": "幻翼膜",
        "minecraft:dragon_breath": "龙息",
        "minecraft:rabbit_foot": "兔子脚",
    }
    return mapping.get(material_id, material_id.split(":")[-1])


# ==================== 配方动态注册 ====================
# 开关设置key -> 配方key
RECIPE_SETTING_MAP = {
    "enable_recipe_fly": "fly",
    "enable_recipe_ender": "ender",
    "enable_recipe_eternal": "eternal",
    "enable_recipe_swift": "swift",
}

# 各羽合成配方数据（AddRecipe 直接接受该 dict）
FLY_RECIPES = {
    "fly": {
        "name": "飞行之羽",
        "data": {
            "minecraft:recipe_shaped": {
                "description": {"identifier": "fly_feather:fly_feater"},
                "key": {
                    "E": {"data": 0, "item": "minecraft:elytra"},
                    "H": {"data": 0, "item": "minecraft:phantom_membrane"},
                    "I": {"data": 0, "item": "minecraft:feather"},
                },
                "pattern": ["IHI", "HEH", "IHI"],
                "result": {"count": 1, "data": 0, "item": "fly_feather:fly_feather"},
                "tags": ["crafting_table"],
                "unlock": [{"data": 0, "item": "minecraft:elytra"}],
            }
        },
    },
    "ender": {
        "name": "末影之羽",
        "data": {
            "minecraft:recipe_shaped": {
                "description": {"identifier": "fly_feather:ender_feather"},
                "key": {
                    "B": {"data": 0, "item": "minecraft:dragon_head"},
                    "E": {"data": 0, "item": "fly_feather:fly_feather"},
                    "F": {"data": 0, "item": "minecraft:shulker_shell"},
                    "H": {"data": 0, "item": "minecraft:end_crystal"},
                    "I": {"data": 0, "item": "minecraft:netherite_ingot"},
                },
                "pattern": ["IBI", "FEF", "IHI"],
                "result": {"count": 1, "data": 0, "item": "fly_feather:ender_feather"},
                "tags": ["crafting_table"],
                "unlock": [{"data": 0, "item": "fly_feather:fly_feather"}],
            }
        },
    },
    "eternal": {
        "name": "不朽之羽",
        "data": {
            "minecraft:recipe_shaped": {
                "description": {"identifier": "fly_feather:eternal_feather"},
                "key": {
                    "B": {"data": 0, "item": "minecraft:netherite_upgrade_smithing_template"},
                    "E": {"data": 0, "item": "fly_feather:fly_feather"},
                    "F": {"data": 0, "item": "minecraft:phantom_membrane"},
                    "H": {"data": 0, "item": "minecraft:nether_star"},
                    "I": {"data": 0, "item": "minecraft:netherite_ingot"},
                },
                "pattern": ["IBI", "FEF", "IHI"],
                "result": {"count": 1, "data": 0, "item": "fly_feather:eternal_feather"},
                "tags": ["crafting_table"],
                "unlock": [{"data": 0, "item": "fly_feather:fly_feather"}],
            }
        },
    },
    "swift": {
        "name": "迅捷之羽",
        "data": {
            "minecraft:recipe_shaped": {
                "description": {"identifier": "fly_feather:swift_feather"},
                "key": {
                    "B": {"data": 0, "item": "minecraft:lapis_block"},
                    "C": {"data": 0, "item": "minecraft:rabbit_foot"},
                    "E": {"data": 0, "item": "fly_feather:fly_feather"},
                    "F": {"data": 0, "item": "minecraft:feather"},
                    "H": {"data": 0, "item": "minecraft:sugar"},
                    "I": {"data": 0, "item": "minecraft:rabbit_hide"},
                },
                "pattern": ["CBC", "FEF", "IHI"],
                "result": {"count": 1, "data": 0, "item": "fly_feather:swift_feather"},
                "tags": ["crafting_table"],
                "unlock": [{"data": 0, "item": "fly_feather:fly_feather"}],
            }
        },
    },
}


def _get_all_armor_display_names():
    return [cfg["display_name"] for cfg in FLY_ARMOR_CONFIG.values()]


# ==================== 逐装备配置 ====================
ARMOR_KEYS = ["fly", "ender", "eternal", "swift"]
EFFECT_ARMOR_KEYS = ["ender", "swift"]  # 仅这两个有被动状态效果
ITEM_BY_ARMOR_KEY = {
    "fly": "fly_feather:fly_feather",
    "ender": "fly_feather:ender_feather",
    "eternal": "fly_feather:eternal_feather",
    "swift": "fly_feather:swift_feather",
}
ARMOR_KEY_BY_ITEM = {v: k for k, v in ITEM_BY_ARMOR_KEY.items()}
ARMOR_DISPLAY_BY_KEY = {
    "fly": "飞行之羽",
    "ender": "末影之羽",
    "eternal": "不朽之羽",
    "swift": "迅捷之羽",
}

# ==================== 自定义指令设置键表 ====================
# 键（不含主卡片前缀 "fly_armor."）-> (类型, 默认值)
# 类型: "bool" / "int" / "float" / "str"
SETTING_VALUE_SCHEMA = {
    "server.default.enable_real_time_durability": ("bool", True),
    "server.default.enable_ender_effect": ("bool", True),
    "server.default.enable_swift_effect": ("bool", True),
    "server.default.enable_ender_full": ("bool", False),
    "server.default.debug_mode": ("bool", False),
    "server.default.allow_command_block_setting": ("bool", True),
    "server.default.permission_lock_mode": ("bool", True),
    "server.default.permission_visitor": ("bool", False),
    "server.default.permission_member": ("bool", False),
    "server.default.permission_operator": ("bool", True),
    "server.default.permission_custom": ("bool", False),
}
for _k in ARMOR_KEYS:
    SETTING_VALUE_SCHEMA["server.default.enable_recipe_" + _k] = ("bool", True)
    SETTING_VALUE_SCHEMA["server.default.enable_durability_" + _k] = ("bool", True)
    SETTING_VALUE_SCHEMA["server.default.enable_unbreaking_" + _k] = ("bool", True)
    SETTING_VALUE_SCHEMA["server.default.repairable_" + _k] = ("bool", True)
    SETTING_VALUE_SCHEMA["server.default.repair_consume_material_" + _k] = ("bool", True)
    _cfg = FLY_ARMOR_CONFIG[ITEM_BY_ARMOR_KEY[_k]]
    SETTING_VALUE_SCHEMA["server.default.repair_xp_" + _k] = ("int", _cfg["repair_xp_cost"])
    SETTING_VALUE_SCHEMA["server.default.repair_material_" + _k] = ("str", _cfg["repair_material"])
for _k in EFFECT_ARMOR_KEYS:
    SETTING_VALUE_SCHEMA["server.default.enable_effect_durability_" + _k] = ("bool", True)

# 服务端各分页（中间卡片）所包含的默认设置键，用于"重置本页"
SERVER_GROUP_DEFAULT_KEYS = {
    "fly_effect": ["enable_ender_effect", "enable_ender_full", "enable_swift_effect"],
    "fly_durability": ["enable_real_time_durability"]
                     + ["enable_durability_" + k for k in ARMOR_KEYS]
                     + ["enable_unbreaking_" + k for k in ARMOR_KEYS]
                     + ["enable_effect_durability_" + k for k in EFFECT_ARMOR_KEYS],
    "fly_repair": (["repairable_" + k for k in ARMOR_KEYS]
                   + ["repair_consume_material_" + k for k in ARMOR_KEYS]
                   + ["repair_xp_" + k for k in ARMOR_KEYS]
                   + ["repair_material_" + k for k in ARMOR_KEYS]),
    "fly_recipe": ["enable_recipe_" + k for k in ARMOR_KEYS],
    "fly_permission": ["permission_lock_mode", "permission_visitor",
                       "permission_member", "permission_operator", "permission_custom"],
}


class FlyArmorServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)

        # ---- 原有事件监听 ----
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "OnNewArmorExchangeServerEvent", self, self.on_armor_change)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "OnScriptTickServer", self, self.on_server_tick)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "ServerItemTryUseEvent", self, self.on_item_try_use)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "GameTypeChangedServerEvent", self, self.on_game_type_changed)
        # 自定义指令：读写模组设置（不依赖前置，支持命令方块）
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "CustomCommandTriggerServerEvent", self, self.on_custom_command)

        # ---- 通用设置相关事件 ----
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "ClientLoadAddonsFinishServerEvent", self, self.on_player_join)
        self.ListenForEvent("FlyArmorClient", "FlyArmorClientSystem",
                            "FlyArmorRequestPermissionEvent", self, self.on_request_permission)
        self.ListenForEvent("FlyArmorClient", "FlyArmorClientSystem",
                            "FlyArmorSettingChangeEvent", self, self.on_setting_change)
        self.ListenForEvent("FlyArmorClient", "FlyArmorClientSystem",
                            "FlyArmorResetGroupEvent", self, self.on_reset_group)

        # ---- 模组全局设置（仅房主/管理员可改） ----
        self._default_settings = {
            "enable_real_time_durability": True,
            "enable_ender_effect": True,
            "enable_swift_effect": True,
            "enable_ender_full": False,
            "enable_recipe_fly": True,
            "enable_recipe_ender": True,
            "enable_recipe_eternal": True,
            "enable_recipe_swift": True,
            "debug_mode": False,
        }
        # 自定义指令：是否允许命令方块修改设置
        self._default_settings["allow_command_block_setting"] = True
        # 逐装备：飞行耐久消耗
        for k in ARMOR_KEYS:
            self._default_settings["enable_durability_" + k] = True
        # 逐装备：是否兼容耐久附魔（耐久附魔可有概率不消耗耐久）
        for k in ARMOR_KEYS:
            self._default_settings["enable_unbreaking_" + k] = True
        # 逐装备：状态效果耐久消耗（末影/迅捷）
        for k in EFFECT_ARMOR_KEYS:
            self._default_settings["enable_effect_durability_" + k] = True
        # 逐装备：修复相关
        for k in ARMOR_KEYS:
            cfg = FLY_ARMOR_CONFIG[ITEM_BY_ARMOR_KEY[k]]
            self._default_settings["repairable_" + k] = True
            self._default_settings["repair_consume_material_" + k] = True
            self._default_settings["repair_xp_" + k] = cfg["repair_xp_cost"]  # 0=不消耗经验
            self._default_settings["repair_material_" + k] = cfg["repair_material"]
        # 权限管理：锁定模式（默认仅操作员）+ 关闭锁定时可配置的权限档
        self._default_settings["permission_lock_mode"] = True
        self._default_settings["permission_visitor"] = False
        self._default_settings["permission_member"] = False
        self._default_settings["permission_operator"] = True
        self._default_settings["permission_custom"] = False
        self.mod_settings = self._load_settings()
        self._recipes_registered = False  # 配方动态注册仅执行一次

        self.tick_counter = 0
        self.check_interval = 20
        self.player_fly_state = {}
        self.player_pending_durability = {}  # 非实时耐久：飞行中待扣除的耐久累积值 playerId -> int
        self.player_pending_snapshot = {}  # 待扣积累所属装备快照 playerId -> (itemName, curDurability)
        self._flush_retry_count = {}  # 切装结算定位失败的连续重试次数 playerId -> int
        self._modifying = False
        self.ender_effect_counter = {}
        self.swift_effect_counter = {}
        self.player_hunger_ratio = {}
        self.effect_interval = 4  # 效果触发间隔（秒），对应80 tick
        self.effect_interval = 4  # 效果触发间隔（秒），对应80 tick

    def _get_extra_data_comp(self):
        levelId = serverApi.GetLevelId()
        if levelId is None:
            return None
        try:
            return serverCompFactory.CreateExtraData(levelId)
        except Exception:
            return None

    def _load_settings(self):
        settings = dict(self._default_settings)
        extraComp = self._get_extra_data_comp()
        if extraComp:
            try:
                saved = extraComp.GetExtraData("FlyArmorSettings")
                if isinstance(saved, dict):
                    for key, value in saved.items():
                        if key in settings and type(value) == type(settings[key]):
                            settings[key] = value
            except Exception:
                pass
        return settings

    def _save_settings(self):
        extraComp = self._get_extra_data_comp()
        if extraComp:
            try:
                extraComp.SetExtraData("FlyArmorSettings", self.mod_settings)
                extraComp.SaveExtraData()
            except Exception:
                pass

    # ==================== 权限判断：房主 / 管理员 ====================

    def _get_operation_level(self, playerId):
        """获取玩家的权限档：0访客 1成员 2操作员 3自定义。"""
        try:
            playerComp = serverCompFactory.CreatePlayer(playerId)
            if playerComp:
                return playerComp.GetPlayerOperation()
        except Exception:
            pass
        return -1

    def _is_operator(self, playerId):
        return self._get_operation_level(playerId) == 2

    def _allowed_permission_levels(self):
        """锁定模式关闭时，允许修改设置的操作权限档集合。"""
        mapping = (("permission_visitor", 0), ("permission_member", 1),
                   ("permission_operator", 2), ("permission_custom", 3))
        levels = {lv for key, lv in mapping if self.mod_settings.get(key, False)}
        if not levels:
            return {2}  # 杜绝全关导致无人可管理，兜底仅操作员
        return levels

    def can_edit_settings(self, playerId):
        """判定玩家是否有权修改模组设置。

        锁定模式开（默认）：仅操作员（房主/管理员）可改，保持原行为；
        锁定模式关：按"权限管理"弹窗中开启的权限档集合判断。
        """
        if self.mod_settings.get("permission_lock_mode", True):
            return self._is_operator(playerId)
        return self._get_operation_level(playerId) in self._allowed_permission_levels()

    def on_player_join(self, args):
        playerId = args.get('playerId')
        # 服务端 addons 加载完成时动态注册配方（仅一次，开关需重启世界后生效）
        if not self._recipes_registered:
            self._recipes_registered = True
            self._register_recipes()
        if playerId:
            has_perm = self.can_edit_settings(playerId)
            self.NotifyToClient(playerId, "FlyArmorPermissionEvent", {
                "hasPermission": has_perm,
                "settings": self.mod_settings
            })

    def on_request_permission(self, args):
        playerId = args.get('playerId')
        if playerId:
            has_perm = self.can_edit_settings(playerId)
            self.NotifyToClient(playerId, "FlyArmorPermissionEvent", {
                "hasPermission": has_perm,
                "settings": self.mod_settings
            })

    def on_setting_change(self, args):
        playerId = args.get('playerId')
        key = args.get('key')
        value = args.get('value')
        if not playerId or not key:
            return
        if not self.can_edit_settings(playerId):
            self.send_tip(playerId, "§c你没有权限修改模组设置！")
            return
        if key not in self.mod_settings:
            return
        # 逐装备修复物品id：校验物品存在，无效则提示并回退
        if key.startswith("repair_material_"):
            m = self._validate_repair_material(playerId, value)
            if m is None:
                old = self.mod_settings.get(key, "")
                self.send_tip(playerId, "§c物品 %s 不存在，已还原为 %s" % (value or "", old or "空"))
                self._revert_setting_to_client(playerId, key, old)
                return
            self.mod_settings[key] = m
        # 逐装备修复经验：输入0不消耗，处理多种填写
        elif key.startswith("repair_xp_"):
            parsed = self._parse_repair_xp(value)
            if parsed is None:
                old = self.mod_settings.get(key, 1)
                self.send_tip(playerId, "§c修复经验数字无效，已还原为 %s" % old)
                self._revert_setting_to_client(playerId, key, old)
                return
            self.mod_settings[key] = parsed
        else:
            self.mod_settings[key] = value
        self._save_settings()
        self._debug_print("模组设置已更新：{} = {}".format(key, self.mod_settings[key]))

    def _validate_repair_material(self, playerId, value):
        """校验修复物品id是否为已注册物品；有效返回规范化值，无效返回 None。

        使用 GameComponentServer.LookupItemByName 判定（之前误用物品组件导致失败放行
        而始终保存成功）。接口异常时保守拒绝，避免把未知/无效物品保存进配置。
        """
        if not value or not isinstance(value, str):
            return None
        v = value.strip()
        if not v or ":" not in v:
            return None
        try:
            gameComp = serverCompFactory.CreateGame(serverApi.GetLevelId())
            if gameComp is None:
                return None
            ok = gameComp.LookupItemByName(v)
            return v if ok else None
        except Exception:
            return None

    def _parse_repair_xp(self, value):
        """解析修复经验输入：0=不消耗；空/非数字返回 None（回退），负数归零。"""
        s = value.strip() if isinstance(value, str) else ""
        if not s:
            return None
        try:
            f = float(s)
        except Exception:
            return None
        if f < 0:
            f = 0.0
        return int(round(f))

    def _revert_setting_to_client(self, playerId, key, value):
        """通知客户端把指定设置项回退为给定值（写入前置本地存储并刷新 UI）。"""
        try:
            self.NotifyToClient(playerId, "FlyArmorRevertSettingEvent", {
                "key": key,
                "value": value,
            })
        except Exception:
            pass

    def on_reset_group(self, args):
        """「重置本页」：把指定服务端分页的所有设置恢复为默认，并推送给在线玩家。"""
        playerId = args.get('playerId')
        mid = args.get('middle_card_id')
        if not playerId:
            return
        if not self.can_edit_settings(playerId):
            self.send_tip(playerId, "§c你没有权限重置模组设置！")
            return
        keys = SERVER_GROUP_DEFAULT_KEYS.get(mid)
        if not keys:
            return
        for key in keys:
            if key in self._default_settings:
                self.mod_settings[key] = self._default_settings[key]
        self._save_settings()
        self._debug_print("重置分组 %s" % mid)
        for pid in serverApi.GetPlayerList():
            self.NotifyToClient(pid, "FlyArmorPermissionEvent", {
                "hasPermission": self.can_edit_settings(pid),
                "settings": self.mod_settings
            })

    # ==================== 自定义指令（不依赖前置，支持命令方块） ====================

    COMMAND_NAMES = ("setting_set", "setting_get", "setting_reset", "setting_list")
    FULL_KEY_PREFIX = "fly_armor."
    SETTING_KEY_PREFIX = "server.default."

    def _setting_key_from_full(self, full_key):
        """完整键 fly_armor.server.default.<key> -> <key>（不符合前缀返回 None）。"""
        if full_key.startswith(self.FULL_KEY_PREFIX):
            rest = full_key[len(self.FULL_KEY_PREFIX):]
            if rest.startswith(self.SETTING_KEY_PREFIX):
                return rest[len(self.SETTING_KEY_PREFIX):]
        return None

    def _coerce_setting_value(self, type_name, raw):
        """按类型把原始输入转成 python 值；失败返回 None（不抛异常）。"""
        if raw is None:
            return None
        if type_name == "bool":
            s = str(raw).strip().lower()
            if s in ("true", "1", "on", "yes", "t"):
                return True
            if s in ("false", "0", "off", "no", "f"):
                return False
            return None
        if type_name == "int":
            try:
                return int(str(raw).strip())
            except Exception:
                return None
        if type_name == "float":
            try:
                return float(str(raw).strip())
            except Exception:
                return None
        return str(raw)  # str：原样保留（允许空串）

    def ApplySetting(self, schema_key, value, source="command"):
        """单一写入入口：校验并按类型写入服务端存储。schema_key 形如 server.default.<item>。

        返回 (ok, 规范值/失败原因)。
        """
        schema = SETTING_VALUE_SCHEMA.get(schema_key)
        if schema is None:
            return False, "unknown"
        if schema_key.startswith(self.SETTING_KEY_PREFIX):
            key = schema_key[len(self.SETTING_KEY_PREFIX):]
        else:
            key = schema_key
        type_name, _default = schema
        if type_name == "bool":
            parsed = self._coerce_setting_value("bool", value)
            if parsed is None:
                return False, "bad_bool"
            mod_value = parsed
        elif type_name == "int":
            if key is not None and key.startswith("repair_xp_"):
                parsed = self._parse_repair_xp(str(value))
                if parsed is None:
                    return False, "bad_int"
                mod_value = parsed
            else:
                parsed = self._coerce_setting_value("int", value)
                if parsed is None:
                    return False, "bad_int"
                mod_value = parsed
        elif type_name == "float":
            parsed = self._coerce_setting_value("float", value)
            if parsed is None:
                return False, "bad_float"
            mod_value = parsed
        else:  # str
            if key is not None and key.startswith("repair_material_"):
                m = self._validate_repair_material(None, str(value))
                if m is None:
                    return False, "bad_item"
                mod_value = m
            else:
                mod_value = str(value)
        self.mod_settings[key] = mod_value
        self._save_settings()
        self._debug_print("设置由%s更新：%s = %s" % (source, key, mod_value))
        return True, mod_value

    def _echo_to_player(self, playerId, text):
        """用 /tellraw 把带 [飞行之羽] 前缀的明细发给玩家（不依赖前置）。"""
        try:
            import json as _json
            # json.dumps 统一转义换行/引号/反斜杠/中文，保证单行合法 JSON
            payload = _json.dumps({"rawtext": [{"text": text}]}, ensure_ascii=False)
        except Exception:
            payload = '{"rawtext":[{"text":"%s"}]}' % text.replace("\\", "\\\\").replace("\"", "\\\"")
        try:
            cmdComp = serverCompFactory.CreateCommand(playerId)
            cmdComp.SetCommand('/tellraw @s %s' % payload)
        except Exception:
            self.send_tip(playerId, text)

    def _mirror_sync(self, target_ids, full_key, value):
        """给目标玩家推送设置镜像刷新（无前置时客户端自动忽略，不报错）。"""
        for pid in target_ids:
            try:
                self.NotifyToClient(pid, "Script_NeteaseModqlFm8gm2_SettingMirrorSync", {
                    "key": full_key,
                    "value": value,
                })
            except Exception:
                pass

    def _command_target_ids(self, origin, playerId, raw_target):
        """计算指令回显/镜像刷新目标玩家集合（target 参数缺省取触发者，@s 在命令方块下为空）。"""
        if raw_target is not None and raw_target != ():
            if isinstance(raw_target, (list, tuple)):
                return tuple(raw_target)
            return (raw_target,)
        if playerId:
            return (playerId,)
        return ()

    def _echo_or_log(self, target_ids, playerId, text):
        """玩家走 tellraw 明细；命令方块/控制台（无玩家）走服务端日志。"""
        if playerId or target_ids:
            for pid in target_ids:
                self._echo_to_player(pid, text)
        else:
            print "[FlyArmor] 指令明细: " + text

    def _audit(self, line):
        print "[FlyArmor][指令审计] " + line

    def on_custom_command(self, args):
        command = args.get('command')
        if command not in self.COMMAND_NAMES:
            return  # 静默：非本模组指令，绝不设置任何返回字段
        arg_map = {}
        for a in args.get('args', []) or []:
            if isinstance(a, dict):
                arg_map[a.get('name')] = a.get('value')
        origin = args.get('origin') or {}
        playerId = origin.get('entityId')
        full_key = str(arg_map.get('键', "") or "")
        prefix_raw = arg_map.get('前缀')
        # 键前缀路由：不属于本模组的一律静默
        if command != "setting_list":
            if not full_key.startswith(self.FULL_KEY_PREFIX):
                return
        else:
            if prefix_raw and not str(prefix_raw).startswith(self.FULL_KEY_PREFIX):
                return
        raw_target = arg_map.get('目标')
        target_ids = self._command_target_ids(origin, playerId, raw_target)
        # schema 键（不含 "fly_armor." 前缀）用于键表匹配
        rest = full_key[len(self.FULL_KEY_PREFIX):] if full_key.startswith(self.FULL_KEY_PREFIX) else full_key

        # 写操作权限：玩家需 OP(>=2)；命令方块受 allow_command_block_setting 控制
        is_write = command in ("setting_set", "setting_reset")
        if is_write:
            if playerId:
                if self._get_operation_level(playerId) < 2:
                    args["return_failed"] = True
                    args["return_msg_key"] = "commands.fly_armor.no_permission"
                    return
            elif not self.mod_settings.get("allow_command_block_setting", True):
                args["return_failed"] = True
                args["return_msg_key"] = "commands.fly_armor.cb_disabled"
                return

        if command == "setting_set":
            if rest not in SETTING_VALUE_SCHEMA:
                args["return_failed"] = True
                args["return_msg_key"] = "commands.fly_armor.unknown_key"
                return
            ok, res = self.ApplySetting(rest, arg_map.get('值'), source="command")
            if not ok:
                args["return_failed"] = True
                args["return_msg_key"] = "commands.fly_armor.bad_value"
                self._echo_or_log(target_ids, playerId, "[飞行之羽] 值格式不合法：%s 需要 %s"
                                  % (self._setting_key_from_full(full_key),
                                     SETTING_VALUE_SCHEMA[rest][0]))
                self._audit("setting_set 失败(%s) %s" % (res, full_key))
                return
            self._mirror_sync(target_ids, full_key, res)
            self._echo_or_log(target_ids, playerId, "[飞行之羽] %s = %s" % (full_key, res))
            args["return_msg_key"] = "commands.fly_armor.set.ok"
            self._audit("setting_set %s = %s" % (full_key, res))
            return

        if command == "setting_get":
            if rest not in SETTING_VALUE_SCHEMA:
                args["return_failed"] = True
                args["return_msg_key"] = "commands.fly_armor.unknown_key"
                return
            item = self._setting_key_from_full(full_key)
            cur = self.mod_settings.get(item, SETTING_VALUE_SCHEMA[rest][1])
            self._echo_or_log(target_ids, playerId, "[飞行之羽] %s = %s" % (full_key, cur))
            args["return_msg_key"] = "commands.fly_armor.get.ok"
            return

        if command == "setting_reset":
            if rest == "server.default":
                reset_keys = list(SETTING_VALUE_SCHEMA.keys())
            elif rest in SETTING_VALUE_SCHEMA:
                reset_keys = [rest]
            else:
                reset_keys = [k for k in SETTING_VALUE_SCHEMA if k.startswith(rest)]
            if not reset_keys:
                args["return_failed"] = True
                args["return_msg_key"] = "commands.fly_armor.unknown_key"
                return
            n = 0
            for rk in reset_keys:
                ok, v = self.ApplySetting(rk, SETTING_VALUE_SCHEMA[rk][1], source="command_reset")
                if ok:
                    n += 1
                    self._mirror_sync(target_ids, self.FULL_KEY_PREFIX + rk, v)
            self._echo_or_log(target_ids, playerId, "[飞行之羽] 已重置 %d 项" % n)
            args["return_msg_key"] = "commands.fly_armor.reset.ok"
            self._audit("setting_reset %s (%d)" % (full_key, n))
            return

        if command == "setting_list":
            lines = []
            prefix = str(prefix_raw) if prefix_raw else ""
            for k in SETTING_VALUE_SCHEMA:
                full = self.FULL_KEY_PREFIX + k
                if prefix and not full.startswith(prefix):
                    continue
                item = k[len(self.SETTING_KEY_PREFIX):] if k.startswith(self.SETTING_KEY_PREFIX) else k
                cur = self.mod_settings.get(item, SETTING_VALUE_SCHEMA[k][1])
                lines.append("[飞行之羽] %s = %s" % (full, cur))
            lines.sort()
            if not lines:
                text = "[飞行之羽] 无匹配设置项"
            elif len(lines) > 8 and not prefix:
                text = "[飞行之羽] 共 %d 项，可加前缀过滤：" % len(lines) + "\n" + "\n".join(lines)
            else:
                text = "\n".join(lines)
            self._echo_or_log(target_ids, playerId, text)
            args["return_msg_key"] = "commands.fly_armor.list.ok"
            return

    # ==================== 通用工具方法 ====================

    def send_tip(self, playerId, message):
        levelId = serverApi.GetLevelId()
        gameComp = serverCompFactory.CreateGame(levelId)
        if gameComp:
            gameComp.SetOneTipMessage(playerId, message)

    def _debug_print(self, message):
        """调试日志：仅当 debug_mode 开启时输出到服务端控制台（不使用游戏内 tip）。"""
        if self.mod_settings.get("debug_mode", False):
            print "[FlyArmor调试] " + message

    def _register_recipes(self):
        """按当前配方开关动态注册合成配方（AddRecipe）。

        仅在服务端加载时执行一次；开关修改后需重启世界生效。
        """
        try:
            comp = serverCompFactory.CreateRecipe(serverApi.GetLevelId())
        except Exception as e:
            print "[FlyArmor] 创建 Recipe 组件失败: %s" % str(e)
            return
        if not comp:
            print "[FlyArmor] Recipe 组件不可用，配方注册跳过"
            return
        for setting_key, recipe_key in RECIPE_SETTING_MAP.items():
            if not self.mod_settings.get(setting_key, True):
                continue
            recipe = FLY_RECIPES[recipe_key]
            try:
                ok = comp.AddRecipe(recipe["data"])
                self._debug_print("动态注册配方 %s -> %s" % (recipe["name"], ok))
            except Exception as e:
                print "[FlyArmor] 注册配方 %s 失败: %s" % (recipe["name"], str(e))

    def set_player_fly(self, playerId, canFly):
        flyComp = serverCompFactory.CreateFly(playerId)
        if flyComp:
            # canFly=True 时只给飞行能力，不强制进入飞行状态（enterFly=False）
            # 让玩家自己按空格起飞，避免打断当前动作
            flyComp.ChangePlayerFlyState(canFly, False)
            self.player_fly_state[playerId] = canFly

    def is_creative(self, playerId):
        gameComp = serverCompFactory.CreateGame(serverApi.GetLevelId())
        if not gameComp:
            return False
        return gameComp.GetPlayerGameType(playerId) == Enum.GameType.Creative

    def get_armor_info(self, playerId):
        itemComp = serverCompFactory.CreateItem(playerId)
        if not itemComp:
            return None, None
        armor = itemComp.GetPlayerItem(Enum.ItemPosType.ARMOR, 1)
        if not armor:
            return None, None
        item_name = armor.get('itemName')
        if item_name in FLY_ARMOR_CONFIG:
            return item_name, armor
        return None, None

    def is_wearing_fly_armor(self, playerId):
        item_name, _ = self.get_armor_info(playerId)
        return item_name is not None

    def is_fly_armor_usable(self, playerId):
        item_name, armor = self.get_armor_info(playerId)
        if not item_name:
            return False
        config = FLY_ARMOR_CONFIG[item_name]
        max_dur = armor.get('maxDurability', config["default_max_durability"])
        cur_dur = armor.get('durability')
        if cur_dur is None:
            cur_dur = max_dur
        return cur_dur > 1

    def get_enchant_level(self, item, enchantId):
        for ench in item.get('enchantData', []):
            if isinstance(ench, (list, tuple)) and len(ench) >= 2:
                eid = ench[0]
                if eid == enchantId or (isinstance(eid, int) and eid == 17 and enchantId == "unbreaking"):
                    return ench[1]
        return 0

    # ==================== 耐久系统 ====================

    def _armor_key(self, item_name):
        return ARMOR_KEY_BY_ITEM.get(item_name)

    def _flight_durability_enabled(self, item_name):
        """该装备是否开启飞行耐久消耗（逐装备）。"""
        k = self._armor_key(item_name)
        return True if k is None else bool(self.mod_settings.get("enable_durability_" + k, True))

    def _effect_durability_enabled(self, item_name):
        """该装备是否开启状态效果耐久消耗（逐装备）。"""
        k = self._armor_key(item_name)
        return True if k is None else bool(self.mod_settings.get("enable_effect_durability_" + k, True))

    def _unbreaking_enabled(self, item_name):
        """该装备是否兼容耐久附魔（逐装备）：耐久附魔可有概率不消耗耐久。"""
        k = self._armor_key(item_name)
        return True if k is None else bool(self.mod_settings.get("enable_unbreaking_" + k, True))

    def _repairable(self, item_name):
        k = self._armor_key(item_name)
        return True if k is None else bool(self.mod_settings.get("repairable_" + k, True))

    def _repair_consume_material(self, item_name):
        k = self._armor_key(item_name)
        return True if k is None else bool(self.mod_settings.get("repair_consume_material_" + k, True))

    def _repair_material_id(self, item_name):
        """该装备修复所需物品id（可为配置值）。"""
        k = self._armor_key(item_name)
        cfg = FLY_ARMOR_CONFIG.get(item_name, {})
        if k is None:
            return cfg.get("repair_material")
        m = self.mod_settings.get("repair_material_" + k)
        if m:
            return m
        return cfg.get("repair_material")

    def _repair_xp_cost(self, item_name):
        """该装备修复所需经验（0=不消耗）。"""
        k = self._armor_key(item_name)
        cfg = FLY_ARMOR_CONFIG.get(item_name, {})
        default = cfg.get("repair_xp_cost", 1)
        if k is None:
            return default
        try:
            return max(0, int(self.mod_settings.get("repair_xp_" + k, default)))
        except Exception:
            return default

    def consume_durability(self, playerId):
        # 调用方已负责设置 _modifying，这里不再检查和设置
        item_name, armor = self.get_armor_info(playerId)
        if not item_name:
            return
        # 逐装备：飞行耐久消耗开关
        if not self._flight_durability_enabled(item_name):
            return
        # 逐装备：是否兼容耐久附魔（关则无视耐久附魔，必定消耗）
        if self._unbreaking_enabled(item_name):
            enchant_lvl = self.get_enchant_level(armor, "unbreaking")
            if enchant_lvl > 0 and random.randint(1, enchant_lvl + 1) != 1:
                return
        # 实时扣除：与原逻辑一致，立即扣 1 点
        if self.mod_settings.get("enable_real_time_durability", True):
            self._deduct_durability_once(playerId, armor, item_name)
            return
        # 非实时扣除：累加到待扣变量，飞行停止时统一结算
        config = FLY_ARMOR_CONFIG[item_name]
        max_dur = armor.get('maxDurability', config["default_max_durability"])
        cur_dur = armor.get('durability')
        if cur_dur is None:
            cur_dur = max_dur
        pending = self.player_pending_durability.get(playerId, 0) + 1
        if pending == 1:
            # 记录该待扣属于哪件装备及其耐久（切装时用于正确结算，防止错扣/丢弃）
            self.player_pending_snapshot[playerId] = (item_name, cur_dur)
        # 与当前剩余耐久对比：最多累积到剩余-1，保证结算后至少剩 1 点（避免损坏）
        cap = max(0, cur_dur - 1)
        self.player_pending_durability[playerId] = min(pending, cap)

    def _deduct_durability_once(self, playerId, armor, item_name):
        """实时扣除：立即将耐久减 1，减到 0 则保留最后 1 点并取消飞行。"""
        itemComp = serverCompFactory.CreateItem(playerId)
        if not itemComp:
            return
        config = FLY_ARMOR_CONFIG[item_name]
        max_dur = armor.get('maxDurability', config["default_max_durability"])
        cur_dur = armor.get('durability')
        if cur_dur is None:
            cur_dur = max_dur
        new_dur = cur_dur - 1
        if new_dur <= 0:
            self.set_player_fly(playerId, False)
            itemComp.SetItemDurability(Enum.ItemPosType.ARMOR, 1, 1)
        else:
            itemComp.SetItemDurability(Enum.ItemPosType.ARMOR, 1, new_dur)

    def flush_pending_durability(self, playerId):
        """非实时耐久结算（普通停止飞行）：按待扣耐久扣除当前装备，并清空待扣。"""
        pending = self.player_pending_durability.get(playerId, 0)
        if pending <= 0:
            self.player_pending_snapshot.pop(playerId, None)
            return
        snap = self.player_pending_snapshot.get(playerId)
        item_name, armor = self.get_armor_info(playerId)
        # 若当前槽位已不是积累时那件（中间切装过），交切装结算处理，避免扣错新装备
        if snap and snap[0] != item_name:
            self.flush_pending_on_switch(playerId)
            return
        if not item_name or armor is None:
            self.player_pending_durability.pop(playerId, None)
            self.player_pending_snapshot.pop(playerId, None)
            return
        itemComp = serverCompFactory.CreateItem(playerId)
        if not itemComp:
            return
        config = FLY_ARMOR_CONFIG[item_name]
        max_dur = armor.get('maxDurability', config["default_max_durability"])
        cur_dur = armor.get('durability')
        if cur_dur is None:
            cur_dur = max_dur
        new_dur = max(1, cur_dur - pending)
        self._modifying = True
        try:
            itemComp.SetItemDurability(Enum.ItemPosType.ARMOR, 1, new_dur)
        finally:
            self._modifying = False
        self.player_pending_durability.pop(playerId, None)
        self.player_pending_snapshot.pop(playerId, None)

    def flush_pending_on_switch(self, playerId, oldArmorDict=None):
        """飞行中切换装备：把待扣耐久精确结算到被切下的旧装备（按其快照耐久）。

        旧装备会从盔甲位移到背包/主手，定位到它再扣除；避免错扣新装备。
        """
        pending = self.player_pending_durability.get(playerId, 0)
        if pending <= 0:
            self.player_pending_snapshot.pop(playerId, None)
            return
        snap = self.player_pending_snapshot.get(playerId)
        # 被切下的旧装备 item 与耐久：优先用事件传入的 oldArmorDict，否则用快照
        if oldArmorDict and oldArmorDict.get('itemName'):
            item_name = oldArmorDict.get('itemName')
            cur_dur = oldArmorDict.get('durability')
        else:
            item_name = snap[0] if snap else None
            cur_dur = snap[1] if snap else None
        if not item_name or cur_dur is None:
            self._schedule_flush_retry(playerId)
            return
        target = self._locate_departed_armor(playerId, item_name)
        if target is None:
            self._schedule_flush_retry(playerId)
            return
        itemComp = serverCompFactory.CreateItem(playerId)
        if not itemComp:
            return
        config = FLY_ARMOR_CONFIG[item_name]
        max_dur = config["default_max_durability"]
        new_dur = max(1, cur_dur - pending)
        self._modifying = True
        try:
            itemComp.SetItemDurability(target[0], target[1], new_dur)
        finally:
            self._modifying = False
        self.player_pending_durability.pop(playerId, None)
        self.player_pending_snapshot.pop(playerId, None)

    def _locate_departed_armor(self, playerId, item_name):
        """定位被切下、已落入背包/主/副手的旧装备，返回 (enumPosType, slot)。"""
        itemComp = serverCompFactory.CreateItem(playerId)
        if not itemComp:
            return None
        try:
            all_items = itemComp.GetPlayerAllItems(Enum.ItemPosType.INVENTORY)
            for i, it in enumerate(all_items):
                if it and it.get('itemName') == item_name:
                    return (Enum.ItemPosType.INVENTORY, i)
        except Exception:
            pass
        for pos in (Enum.ItemPosType.MAINHAND, Enum.ItemPosType.CARRIED):
            try:
                it = itemComp.GetPlayerItem(pos, 0)
                if it and it.get('itemName') == item_name:
                    return (pos, 0)
            except Exception:
                pass
        return None

    def _schedule_flush_retry(self, playerId):
        """定位旧装备失败时延迟重试，避免把待扣耐久丢弃（防切装免耐久 bug）。

        最多重试若干次，仍失败则以调试日志告警（正常情况下几帧内即落包）。
        """
        n = self._flush_retry_count.get(playerId, 0)
        if n >= 10:
            self._flush_retry_count.pop(playerId, None)
            self.player_pending_durability.pop(playerId, None)
            self.player_pending_snapshot.pop(playerId, None)
            if self.mod_settings.get("debug_mode", False):
                print "[FlyArmor调试] 无法定位被切换装备，放弃结算待扣耐久 (player=%s)" % playerId
            return
        self._flush_retry_count[playerId] = n + 1
        gameComp = serverCompFactory.CreateGame(serverApi.GetLevelId())
        if gameComp:
            gameComp.AddTimer(5, lambda p=playerId: self.flush_pending_on_switch(p))

    def _set_hunger_ratio(self, playerId, ratio):
        current = self.player_hunger_ratio.get(playerId, 1.0)
        if current == ratio:
            return
        playerComp = serverCompFactory.CreatePlayer(playerId)
        if playerComp:
            playerComp.SetPlayerExhaustionRatioByType(
                Enum.PlayerExhauseRatioType.GLOBAL, ratio
            )
            self.player_hunger_ratio[playerId] = ratio

    # ==================== 末影之羽被动效果系统 ====================

    ENDER_EFFECTS_BY_DIMENSION = {
        0: [
            ("speed", 20, 0),
            ("jump_boost", 20, 0),
            ("regeneration", 20, 0),
            ("water_breathing", 20, 0),
        ],
        1: [
            ("speed", 20, 0),
            ("jump_boost", 20, 0),
            ("fire_resistance", 20, 0),
            ("strength", 20, 0),
        ],
        2: [
            ("speed", 20, 1),
            ("jump_boost", 20, 1),
            ("fire_resistance", 20, 0),
            ("strength", 20, 0),
            ("regeneration", 20, 0),
            ("water_breathing", 20, 0),
        ],
    }

    def _consume_effect_durability(self, playerId, armor, item_name):
        """效果触发时消耗耐久，10%基础概率，耐久附魔按乘法减免。创造模式不消耗。"""
        try:
            # 逐装备：状态效果耐久消耗开关
            if not self._effect_durability_enabled(item_name):
                return
            # 创造模式不消耗耐久
            if self.is_creative(playerId):
                return
            # 逐装备：是否兼容耐久附魔（关则无视耐久附魔，等级按 0 计算）
            if self._unbreaking_enabled(item_name):
                enchant_lvl = self.get_enchant_level(armor, "unbreaking")
            else:
                enchant_lvl = 0
            # 基础10%概率，耐久附魔按原版机制乘法减免：概率 / (等级 + 1)
            base_chance = 0.10
            chance = base_chance / (enchant_lvl + 1)
            if random.random() >= chance:
                return
            itemComp = serverCompFactory.CreateItem(playerId)
            if not itemComp:
                return
            config = FLY_ARMOR_CONFIG[item_name]
            max_dur = armor.get('maxDurability', config["default_max_durability"])
            cur_dur = armor.get('durability')
            if cur_dur is None:
                cur_dur = max_dur
            new_dur = cur_dur - 1
            if new_dur <= 0:
                new_dur = 1
            # 使用 _modifying 标记防止 SetItemDurability 触发 OnNewArmorExchangeServerEvent
            # 避免飞行状态被重置
            self._modifying = True
            try:
                itemComp.SetItemDurability(Enum.ItemPosType.ARMOR, 1, new_dur)
            finally:
                self._modifying = False
        except Exception:
            pass

    def apply_ender_effects(self, playerId):
        if not self.mod_settings.get("enable_ender_effect", True):
            return
        item_name, armor = self.get_armor_info(playerId)
        if item_name != "fly_feather:ender_feather":
            return
        self._consume_effect_durability(playerId, armor, item_name)
        dimComp = serverCompFactory.CreateDimension(playerId)
        dimensionId = 0
        if dimComp:
            dimensionId = dimComp.GetEntityDimensionId()
        if self.mod_settings.get("enable_ender_full", False):
            effects = self.ENDER_EFFECTS_BY_DIMENSION[2]
        else:
            effects = self.ENDER_EFFECTS_BY_DIMENSION.get(dimensionId, self.ENDER_EFFECTS_BY_DIMENSION[0])
        effectComp = serverCompFactory.CreateEffect(playerId)
        if effectComp:
            for effect_name, duration, amplifier in effects:
                effectComp.AddEffectToEntity(effect_name, duration, amplifier, False)

    # ==================== 迅捷之羽被动效果系统 ====================

    SWIFT_EFFECTS = [
        ("speed", 20, 4),
        ("jump_boost", 20, 2),
    ]

    def apply_swift_effects(self, playerId):
        if not self.mod_settings.get("enable_swift_effect", True):
            return
        item_name, armor = self.get_armor_info(playerId)
        if item_name != "fly_feather:swift_feather":
            return
        self._consume_effect_durability(playerId, armor, item_name)
        effectComp = serverCompFactory.CreateEffect(playerId)
        if effectComp:
            for effect_name, duration, amplifier in self.SWIFT_EFFECTS:
                effectComp.AddEffectToEntity(effect_name, duration, amplifier, False)

    # ==================== 修复系统 ====================

    def _get_armor_durability(self, playerId):
        item_name, armor = self.get_armor_info(playerId)
        if not item_name:
            return None, None, None
        config = FLY_ARMOR_CONFIG[item_name]
        max_dur = armor.get('maxDurability', config["default_max_durability"])
        cur_dur = armor.get('durability')
        if cur_dur is None:
            cur_dur = max_dur
        return item_name, cur_dur, max_dur

    def _has_material(self, playerId, material_name):
        itemComp = serverCompFactory.CreateItem(playerId)
        if not itemComp:
            return False
        all_items = itemComp.GetPlayerAllItems(Enum.ItemPosType.INVENTORY)
        for item in all_items:
            if item and item.get('itemName') == material_name:
                return True
        for hand_slot in [Enum.ItemPosType.CARRIED, Enum.ItemPosType.MAINHAND]:
            try:
                carried = itemComp.GetPlayerItem(hand_slot, 0)
                if carried and carried.get('itemName') == material_name:
                    return True
            except:
                pass
        return False

    def _deduct_xp(self, playerId, cost):
        levelComp = serverCompFactory.CreateLv(playerId)
        if not levelComp:
            return False
        current_level = levelComp.GetPlayerLevel()
        if current_level < cost:
            self.send_tip(playerId, "§c经验不足！需要{}级经验".format(cost))
            return False
        levelComp.AddPlayerLevel(-cost)
        return True

    def _deduct_material(self, playerId, material_name):
        itemComp = serverCompFactory.CreateItem(playerId)
        if not itemComp:
            return False
        all_items = itemComp.GetPlayerAllItems(Enum.ItemPosType.INVENTORY)
        for i, item in enumerate(all_items):
            if item and item.get('itemName') == material_name:
                count = item.get('count', 1)
                if count > 1:
                    itemComp.SetInvItemNum(i, count - 1)
                else:
                    itemComp.SetInvItemNum(i, 0)
                return True
        return False

    def _return_glass_bottle(self, playerId):
        itemComp = serverCompFactory.CreateItem(playerId)
        if not itemComp:
            return
        bottle_dict = {"itemName": "minecraft:glass_bottle", "count": 1}
        success = itemComp.SpawnItemToPlayerInv(bottle_dict, playerId)
        if not success:
            posComp = serverCompFactory.CreatePos(playerId)
            dimComp = serverCompFactory.CreateDimension(playerId)
            if posComp and dimComp:
                pos = posComp.GetPos()
                dimensionId = dimComp.GetEntityDimensionId()
                if pos and dimensionId is not None:
                    itemComp.SpawnItemToLevel(bottle_dict, dimensionId, pos)

    def _repair_armor(self, playerId, item_name=None):
        if item_name is None:
            item_name, cur_dur, max_dur = self._get_armor_durability(playerId)
        else:
            _, cur_dur, max_dur = self._get_armor_durability(playerId)
        if not item_name:
            names = "、".join(_get_all_armor_display_names())
            self.send_tip(playerId, "§c你需要先装备{}！".format(names))
            return False
        config = FLY_ARMOR_CONFIG[item_name]
        # 逐装备：是否可修复
        if not self._repairable(item_name):
            self.send_tip(playerId, "§c{}不可修复".format(config["display_name"]))
            return False
        material_id = self._repair_material_id(item_name)
        consume_material = self._repair_consume_material(item_name)
        xp_cost = self._repair_xp_cost(item_name)  # 0=不消耗经验
        if cur_dur >= max_dur:
            self.send_tip(playerId, "§e{}耐久已满，无需修复".format(config["display_name"]))
            return False
        is_creative = self.is_creative(playerId)
        if not is_creative:
            if consume_material and not self._has_material(playerId, material_id):
                material_display = _get_material_display_name(material_id)
                self.send_tip(playerId, "§c需要{}来修复{}！".format(material_display, config["display_name"]))
                return False
            if 0 < xp_cost and not self._deduct_xp(playerId, xp_cost):
                return False
            if consume_material:
                self._deduct_material(playerId, material_id)
                if material_id == "minecraft:dragon_breath":
                    self._return_glass_bottle(playerId)
        repair_amount = int(max_dur * config["repair_percent"])
        new_dur = min(cur_dur + repair_amount, max_dur)
        itemComp = serverCompFactory.CreateItem(playerId)
        if itemComp:
            itemComp.SetItemDurability(Enum.ItemPosType.ARMOR, 1, new_dur)
        if is_creative:
            self.send_tip(
                playerId,
                "§a{}已修复！§e{}/{} §7[创造模式]".format(config["display_name"], new_dur, max_dur)
            )
        else:
            material_display = _get_material_display_name(material_id)
            if consume_material and xp_cost:
                self.send_tip(
                    playerId,
                    "§a{}已修复！§e{}/{} §a(消耗1个{}+{}级经验)".format(
                        config["display_name"], new_dur, max_dur,
                        material_display, xp_cost
                    )
                )
            elif consume_material and not xp_cost:
                self.send_tip(
                    playerId,
                    "§a{}已修复！§e{}/{} §a(消耗1个{})".format(
                        config["display_name"], new_dur, max_dur,
                        material_display
                    )
                )
            elif not consume_material and xp_cost:
                self.send_tip(
                    playerId,
                    "§a{}已修复！§e{}/{} §a(消耗{}级经验)".format(
                        config["display_name"], new_dur, max_dur,
                        xp_cost
                    )
                )
            else:
                self.send_tip(
                    playerId,
                    "§a{}已修复！§e{}/{} §a(免费修复)".format(
                        config["display_name"], new_dur, max_dur
                    )
                )
        return True

    # ==================== 事件回调 ====================

    def on_item_try_use(self, args):
        playerId = args.get('playerId')
        itemDict = args.get('itemDict')
        if not itemDict:
            return
        used_item = itemDict.get('itemName')
        # 按各装备配置的修复材料id匹配目标装备
        target_item_name = None
        for item_name in FLY_ARMOR_CONFIG:
            if self._repair_material_id(item_name) == used_item:
                target_item_name = item_name
                break
        if not target_item_name:
            return
        # 逐装备：是否可修复
        if not self._repairable(target_item_name):
            self.send_tip(playerId, "§c该装备不可修复")
            return
        equipped_name, _ = self.get_armor_info(playerId)
        if equipped_name != target_item_name:
            return
        success = self._repair_armor(playerId, target_item_name)
        if success and 'cancel' in args:
            args['cancel'] = True

    def on_game_type_changed(self, args):
        playerId = args.get('playerId')

        if playerId:
            # 延迟执行，等待游戏模式真正生效
            gameComp = serverCompFactory.CreateGame(serverApi.GetLevelId())
            if gameComp:
                gameComp.AddTimer(0.5, lambda p=playerId: self._refresh_player_fly_after_gametype_change(p))
        else:
            players = serverApi.GetPlayerList()
            gameComp = serverCompFactory.CreateGame(serverApi.GetLevelId())
            if gameComp and players:
                for pid in players:
                    gameComp.AddTimer(0.5, lambda p=pid: self._refresh_player_fly_after_gametype_change(p))

    def _refresh_player_fly_after_gametype_change(self, playerId):
        item_name, _ = self.get_armor_info(playerId)
        # 清除旧状态，让 set_player_fly 重新判断
        self.player_fly_state.pop(playerId, None)
        if self.is_creative(playerId):
            self.set_player_fly(playerId, True)
            return
        if item_name in FLY_ARMOR_CONFIG:
            if self.is_fly_armor_usable(playerId):
                self.set_player_fly(playerId, True)
            else:
                self.set_player_fly(playerId, False)
            self._debug_print("模式切换已刷新飞行状态 (player=%s)" % playerId)
        else:
            self.set_player_fly(playerId, False)

    def on_armor_change(self, args):
        if self._modifying or args.get('slot') != 1:
            return
        playerId = args.get('playerId')
        # 飞行中切换装备：立即把待扣耐久结算到被切下的旧装备（oldArmorDict）
        if playerId and self.player_pending_durability.get(playerId, 0):
            self.flush_pending_on_switch(playerId, args.get('oldArmorDict'))
        newArmor = args.get('newArmorDict')
        gameComp = serverCompFactory.CreateGame(serverApi.GetLevelId())
        if not gameComp:
            return
        item_name = newArmor.get('itemName') if newArmor else None

        if item_name in FLY_ARMOR_CONFIG and self.mod_settings.get("debug_mode", False):
            try:
                playerComp = serverCompFactory.CreatePlayer(playerId)
                op_type = playerComp.GetPlayerOperation() if playerComp else -1
                abilities = playerComp.GetPlayerAbilities() if playerComp else {}
                is_op = abilities.get('op', False) if abilities else False
                print("[FlyArmor调试] playerId={} op_type={} is_op={}".format(playerId, op_type, is_op))
            except Exception as e:
                print("[FlyArmor调试] 权限检测异常: {}".format(str(e)))

        if item_name in FLY_ARMOR_CONFIG:
            if self.is_creative(playerId):
                gameComp.AddTimer(0.1, lambda pid=playerId: self.set_player_fly(pid, True))
            else:
                def try_give_fly(pid):
                    if self.is_fly_armor_usable(pid):
                        self.set_player_fly(pid, True)
                    else:
                        self.set_player_fly(pid, False)
                gameComp.AddTimer(0.1, lambda pid=playerId: try_give_fly(pid))
        else:
            # 只有非创造模式且当前有飞行能力时才取消
            if not self.is_creative(playerId) and self.player_fly_state.get(playerId):
                gameComp.AddTimer(0.1, lambda pid=playerId: self.set_player_fly(pid, False))

    def on_server_tick(self):
        self.tick_counter += 1
        if self.tick_counter < self.check_interval:
            return
        self.tick_counter = 0
        players = serverApi.GetPlayerList()
        if not players:
            return
        gameComp = serverCompFactory.CreateGame(serverApi.GetLevelId())
        if not gameComp:
            return
        for pid in players:
            is_creative = self.is_creative(pid)
            item_name, armor = self.get_armor_info(pid)
            flyComp = serverCompFactory.CreateFly(pid)
            flying = flyComp.IsPlayerFlying() if flyComp else False
            if not is_creative:
                if item_name:
                    usable = self.is_fly_armor_usable(pid)
                    if usable and not self.player_fly_state.get(pid):
                        self.set_player_fly(pid, True)
                    elif not usable and self.player_fly_state.get(pid):
                        self.set_player_fly(pid, False)
                else:
                    if self.player_fly_state.get(pid):
                        self.set_player_fly(pid, False)
                # 飞行中消耗耐久，但用_modifying标记防止触发装备变更事件
                if item_name and flying and self.is_fly_armor_usable(pid):
                    self._modifying = True
                    try:
                        self.consume_durability(pid)
                    finally:
                        self._modifying = False
            # 非实时耐久：若玩家已停止飞行/装备不可用，立即结算待扣耐久
            if self.player_pending_durability.get(pid, 0):
                is_accumulating = (not self.mod_settings.get("enable_real_time_durability", True)
                                   and item_name and flying and self.is_fly_armor_usable(pid))
                if not is_accumulating:
                    self.flush_pending_durability(pid)
            if item_name == "fly_feather:ender_feather" and self.is_fly_armor_usable(pid):
                self.ender_effect_counter[pid] = self.ender_effect_counter.get(pid, 0) + 1
                if self.ender_effect_counter[pid] >= self.effect_interval:
                    self.ender_effect_counter[pid] = 0
                    self.apply_ender_effects(pid)
                if not is_creative:
                    self._set_hunger_ratio(pid, 2.0)
            else:
                self.ender_effect_counter[pid] = 0
                if not is_creative:
                    self._set_hunger_ratio(pid, 1.0)
            if item_name == "fly_feather:swift_feather" and self.is_fly_armor_usable(pid):
                self.swift_effect_counter[pid] = self.swift_effect_counter.get(pid, 0) + 1
                if self.swift_effect_counter[pid] >= self.effect_interval:
                    self.swift_effect_counter[pid] = 0
                    self.apply_swift_effects(pid)
            else:
                self.swift_effect_counter[pid] = 0