# -*- coding: utf-8 -*-
# ==================== 飞行之羽模组 - 入口文件 ====================

from mod.common.mod import Mod


@Mod.Binding(name="Script_NeteaseModqlFm8gm2", version="0.0.1")
class Script_NeteaseModqlFm8gm2(object):
    def __init__(self):
        pass

    @Mod.InitServer()
    def ServerInit(self):
        import sys, os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        import mod.server.extraServerApi as serverApi
        serverApi.RegisterSystem("FlyArmorServer", "FlyArmorServerSystem",
                                 "Script_NeteaseModqlFm8gm2.FlyArmorServer.FlyArmorServerSystem")

    @Mod.DestroyServer()
    def ServerDestroy(self):
        pass

    @Mod.InitClient()
    def ClientInit(self):
        import sys, os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        import mod.client.extraClientApi as clientApi
        clientApi.RegisterSystem("FlyArmorClient", "FlyArmorClientSystem",
                                 "Script_NeteaseModqlFm8gm2.FlyArmorClient.FlyArmorClientSystem")

    @Mod.DestroyClient()
    def ClientDestroy(self):
        pass
