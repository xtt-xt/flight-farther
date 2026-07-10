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


def _get_all_armor_display_names():
    return [cfg["display_name"] for cfg in FLY_ARMOR_CONFIG.values()]


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

        # ---- 通用设置相关事件 ----
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "ClientLoadAddonsFinishServerEvent", self, self.on_player_join)
        self.ListenForEvent("FlyArmorClient", "FlyArmorClientSystem",
                            "FlyArmorRequestPermissionEvent", self, self.on_request_permission)
        self.ListenForEvent("FlyArmorClient", "FlyArmorClientSystem",
                            "FlyArmorSettingChangeEvent", self, self.on_setting_change)

        # ---- 模组全局设置（仅房主/管理员可改） ----
        self._default_settings = {
            "enable_durability": True,
            "enable_ender_effect": True,
            "enable_swift_effect": True,
            "enable_effect_durability": True,
            "enable_ender_full": False,
            "enable_repair": True,
            "enable_repair_xp": True,
            "enable_repair_material": True,
            "repair_xp_multiplier": 1.0,
            "debug_mode": False,
        }
        self.mod_settings = self._load_settings()

        self.tick_counter = 0
        self.check_interval = 20
        self.player_fly_state = {}
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

    def is_host_or_admin(self, playerId):
        """判断玩家是否有op权限。有op就能修改设置。"""
        try:
            playerComp = serverCompFactory.CreatePlayer(playerId)
            if playerComp:
                abilities = playerComp.GetPlayerAbilities()
                return abilities.get('op', False) if abilities else False
        except Exception:
            pass
        return False

    def on_player_join(self, args):
        playerId = args.get('playerId')
        if playerId:
            has_perm = self.is_host_or_admin(playerId)
            self.NotifyToClient(playerId, "FlyArmorPermissionEvent", {
                "hasPermission": has_perm,
                "settings": self.mod_settings
            })

    def on_request_permission(self, args):
        playerId = args.get('playerId')
        if playerId:
            has_perm = self.is_host_or_admin(playerId)
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
        if not self.is_host_or_admin(playerId):
            self.send_tip(playerId, "§c你没有权限修改模组设置！")
            return
        if key in self.mod_settings:
            # repair_xp_multiplier 从输入框传来的是字符串，需要转数字
            if key == "repair_xp_multiplier":
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    value = 1
            self.mod_settings[key] = value
            self._save_settings()
            if self.mod_settings.get("debug_mode", False):
                self.send_tip(playerId, "§a模组设置已更新：{} = {}".format(key, value))

    # ==================== 通用工具方法 ====================

    def send_tip(self, playerId, message):
        levelId = serverApi.GetLevelId()
        gameComp = serverCompFactory.CreateGame(levelId)
        if gameComp:
            gameComp.SetOneTipMessage(playerId, message)

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

    def consume_durability(self, playerId):
        if not self.mod_settings.get("enable_durability", True):
            return
        # 调用方已负责设置 _modifying，这里不再检查和设置
        item_name, armor = self.get_armor_info(playerId)
        if not item_name:
            return
        itemComp = serverCompFactory.CreateItem(playerId)
        if not itemComp:
            return
        enchant_lvl = self.get_enchant_level(armor, "unbreaking")
        if enchant_lvl > 0 and random.randint(1, enchant_lvl + 1) != 1:
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
            if not self.mod_settings.get("enable_effect_durability", True):
                return
            # 创造模式不消耗耐久
            if self.is_creative(playerId):
                return
            enchant_lvl = self.get_enchant_level(armor, "unbreaking")
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
        if cur_dur >= max_dur:
            self.send_tip(playerId, "§e{}耐久已满，无需修复".format(config["display_name"]))
            return False
        is_creative = self.is_creative(playerId)
        if not is_creative:
            if self.mod_settings.get("enable_repair_material", True):
                if not self._has_material(playerId, config["repair_material"]):
                    material_display = _get_material_display_name(config["repair_material"])
                    self.send_tip(playerId, "§c需要{}来修复{}！".format(material_display, config["display_name"]))
                    return False
            if not self.mod_settings.get("enable_repair_xp", True):
                xp_cost = 0
            else:
                xp_cost = config["repair_xp_cost"] * self.mod_settings.get("repair_xp_multiplier", 1)
                xp_cost = max(1, int(xp_cost))
                if not self._deduct_xp(playerId, xp_cost):
                    return False
            if self.mod_settings.get("enable_repair_material", True):
                self._deduct_material(playerId, config["repair_material"])
                if config["repair_material"] == "minecraft:dragon_breath":
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
            material_display = _get_material_display_name(config["repair_material"])
            # 修复提示时重新计算xp_cost，确保与扣除时一致
            if not self.mod_settings.get("enable_repair_xp", True):
                xp_cost = 0
            else:
                xp_cost = config["repair_xp_cost"] * self.mod_settings.get("repair_xp_multiplier", 1)
                xp_cost = max(1, int(xp_cost))
            consume_material = self.mod_settings.get("enable_repair_material", True)
            consume_xp = self.mod_settings.get("enable_repair_xp", True)
            if consume_material and consume_xp:
                self.send_tip(
                    playerId,
                    "§a{}已修复！§e{}/{} §a(消耗1个{}+{}级经验)".format(
                        config["display_name"], new_dur, max_dur,
                        material_display, xp_cost
                    )
                )
            elif consume_material and not consume_xp:
                self.send_tip(
                    playerId,
                    "§a{}已修复！§e{}/{} §a(消耗1个{})".format(
                        config["display_name"], new_dur, max_dur,
                        material_display
                    )
                )
            elif not consume_material and consume_xp:
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
        if not self.mod_settings.get("enable_repair", True):
            return
        playerId = args.get('playerId')
        itemDict = args.get('itemDict')
        if not itemDict:
            return
        used_item = itemDict.get('itemName')
        target_item_name = None
        for item_name, config in FLY_ARMOR_CONFIG.items():
            if config["repair_material"] == used_item:
                target_item_name = item_name
                break
        if not target_item_name:
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
            if self.mod_settings.get("debug_mode", False):
                self.send_tip(playerId, "§7[调试] 模式切换已刷新飞行状态")
        else:
            self.set_player_fly(playerId, False)

    def on_armor_change(self, args):
        if self._modifying or args.get('slot') != 1:
            return
        playerId = args.get('playerId')
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