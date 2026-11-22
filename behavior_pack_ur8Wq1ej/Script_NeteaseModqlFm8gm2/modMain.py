# -*- coding: utf-8 -*-
# ==================== 飞行之羽模组 - 入口文件 ====================

from mod.common.mod import Mod


@Mod.Binding(name="Script_NeteaseModqlFm8gm2", version="0.0.1")
class Script_NeteaseModqlFm8gm2(object):
    def __init__(self):
        pass

    @Mod.InitServer()
    def ServerInit(self):
        # 只注册服务端 System：模块路径用「包名.模块.类名」，引擎按行为包根目录解析，
        # 不要在这里 import os/sys 改 sys.path（平台安全规则 restricted-module-import 会告警）
        import mod.server.extraServerApi as serverApi
        serverApi.RegisterSystem("FlyArmorServer", "FlyArmorServerSystem",
                                 "Script_NeteaseModqlFm8gm2.FlyArmorServer.FlyArmorServerSystem")

    @Mod.DestroyServer()
    def ServerDestroy(self):
        pass

    @Mod.InitClient()
    def ClientInit(self):
        # 同上：客户端 System 也用完整包路径注册，不依赖 sys.path 注入
        import mod.client.extraClientApi as clientApi
        clientApi.RegisterSystem("FlyArmorClient", "FlyArmorClientSystem",
                                 "Script_NeteaseModqlFm8gm2.FlyArmorClient.FlyArmorClientSystem")

    @Mod.DestroyClient()
    def ClientDestroy(self):
        pass
