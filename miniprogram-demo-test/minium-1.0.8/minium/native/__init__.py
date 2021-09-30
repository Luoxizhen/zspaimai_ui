#!/usr/bin/env python3
# Created by xiazeng on 2019-05-22
import os.path
import sys

work_root = os.path.abspath(os.path.dirname(__file__))
lib_path = os.path.join(work_root, "lib")
sys.path.insert(0, lib_path)

from minium.framework.miniconfig import MiniConfig, logger

# weChat
from minium.native.wx_native.androidnative import WXAndroidNative
from minium.native.wx_native.iosnative import WXIOSNative
from minium.native.wx_native.idenative import IdeNative

# QQ
from minium.native.qq_native.qandroidnative import QAndroidNative
from minium.native.qq_native.qiosnative import QiOSNative

# platform
OS_ANDROID = "android"
OS_IOS = "ios"
OS_IDE = "ide"
OS_MAC = "mac"
OS_WIN = "win"

# application
APP_WX = "wx"
APP_QQ = "qq"

APP = {
    "wx_android": WXAndroidNative,
    "wx_ios": WXIOSNative,
    "qq_android": QAndroidNative,
    "qq_ios": QiOSNative,
    "ide": IdeNative,
}


def get_native_driver(os_name, conf):
    if os_name.lower() not in [OS_ANDROID, OS_IDE, OS_IOS]:
        raise RuntimeError("the 'os_name' in your config file is not in predefine")
    if os_name.lower() != OS_IDE and conf.get("app", None) not in [APP_WX, APP_QQ]:
        raise RuntimeError(
            f"the 'app': '{os_name}' in your config file is not in predefine, not support yet"
        )
    if os_name.lower() == OS_IDE:
        return APP[os_name.lower()]({})
    elif not conf.device_desire:
        logger.warning("your platform is [{}], but dosn't configure the [device_desire] field, native interface will not in use!".format(os_name))
        return APP[OS_IDE]({})
    else:
        return APP[conf.app.lower() + "_" + os_name.lower()](conf.device_desire)
    
def Native(json_conf, platform=None, app="wx"):
    cfg = MiniConfig({
        "platform": platform,
        "app": app,
        "device_desire": json_conf
    })
    return get_native_driver(platform, cfg)
