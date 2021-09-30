#!/usr/bin/env python3
# Created by xiazeng on 2019-05-22


class BaseNative:
    def __init__(self, json_conf):
        self.json_conf = json_conf

    def release(self):
        raise NotImplementedError()

    def start_wechat(self):
        """
        启动微信
        :return:
        """
        raise NotImplementedError()

    def stop_wechat(self):
        """
        启动微信
        :return:
        """
        raise NotImplementedError()

    def connect_weapp(self, path):
        """
        扫码图片
        :param path:图片名称
        :return:
        """
        raise NotImplementedError()

    def screen_shot(self, filename, return_format="raw"):
        """
        截图
        :param filename: 文件存放的路径
        :param return_format: 除了将截图保存在本地之外, 需要返回的图片内容格式: raw(default) or pillow
        :return: raw data or PIL.Image
        """
        raise NotImplementedError()

    def pick_media_file(
            self,
            cap_type="camera",
            media_type="photo",
            original=False,
            duration=5.0,
            names=None,
    ):
        """
        获取媒体文件
        :param cap_type: camera: 拍摄 | album: 从相册获取
        :param names: 传入一个 list 选择多张照片或者视频(照片和视频不能同时选择, 且图片最多 9 张, 视频一次只能选择一个)
        :param media_type: photo 或者 video
        :param duration: 拍摄时长
        :param original: 是否选择原图(仅图片)
        :return:
        """
        raise NotImplementedError()

    def input_text(self, text):
        """
        input 组件填写文字
        :param text: 内容
        :return:
        """
        raise NotImplementedError()

    def input_clear(self):
        """
        input 组件清除文字(使用此函数之前必须确保输入框处于输入状态)
        :return:
        """
        raise NotImplementedError()

    def textarea_text(self, text, index=1):
        """
        给 textarea 输入文字需要在小程序层提供该 textarea 的 index 信息
        :param text: 内容
        :param index: 多个 textarea 同时存在一个页面从上往下排序, 计数从 1 开始
        :return:
        """
        raise NotImplementedError()

    def textarea_clear(self, index=0):
        """
        给 textarea 清除文字需要在小程序层提供该 textarea 的 index 信息
        :param index: 多个 textarea 同时存在一个页面从上往下排序, 计数从 1 开始
        :return:
        """
        raise NotImplementedError()

    def allow_login(self):
        """
        处理微信登陆确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_get_user_info(self, answer=True):
        """
        处理获取用户信息确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_get_location(self, answer=True):
        """
        处理获取位置信息确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_get_user_phone(self, answer=True):
        """
        处理获取用户手机号码确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def handle_modal(self, btn_text="确定", title=None):
        """
        处理模态弹窗
        :param title: 传入弹窗的 title 可以校验当前弹窗是否为预期弹窗
        :param btn_text: 根据传入的 name 进行点击
        :return:
        """
        raise NotImplementedError()

    def handle_action_sheet(self, item):
        """
        处理上拉菜单
        :param item: 要选择的 item
        :return:
        """
        raise NotImplementedError()

    def forward_miniprogram(
            self, names: list, text: str = None, create_new_chat: bool = True
    ):
        """
        通过右上角更多菜单转发小程序
        :type text: 分享携带的内容
        :param names: 要分享的人
        :param create_new_chat: 是否创建群聊
        :return:
        """
        raise NotImplementedError()

    def forward_miniprogram_inside(self, names: list, create_new_chat: bool = True):
        """
        小程序内触发转发小程序
        :param names: 要分享的人
        :param create_new_chat: 是否创建群聊
        :return:
        """
        raise NotImplementedError()

    def send_custom_message(self, message=None):
        """
        处理小程序im 发送自定义消息
        :param message: 消息内容
        :return:
        """
        raise NotImplementedError()

    def phone_call(self):
        """
        处理小程序拨打电话
        :return:
        """
        raise NotImplementedError()

    def map_select_location(self, name):
        """
        原生地图组件选择位置
        :param name: 位置名称
        :return:
        """
        raise NotImplementedError()

    def map_back_to_mp(self):
        """
        原生地图组件查看定位,返回小程序
        :return:
        """
        raise NotImplementedError()

    def deactivate(self, duration):
        """
        使微信进入后台一段时间, 再切回前台
        :param duration: float
        :return: NULL
        """
        raise NotImplementedError()

    def get_authorize_settings(self):
        """
        在小程序的授权页面，获取小程序的授权设置
        :return:
        """
        raise NotImplementedError()

    def back_from_authorize_setting(self):
        """
        从小程序授权页面跳转回小程序
        :return:
        """
        raise NotImplementedError()

    def authorize_page_checkbox_enable(self, name, enable):
        """
        在小程序授权设置页面操作CheckBox
        :param name: 设置的名称
        :param enable: 是否打开
        :return:
        """
        raise NotImplementedError()

    def start_get_perf(self, timeinterval=15):
        """
        开始获取性能数据
        :param timeinterval: 抽样时间间隔
        :return: boolen
        """
        return False

    def stop_get_perf(self):
        """
        停止获取性能数据
        :return: string: json.dumps([{cpu, mem, fps, timestamp}])
        """
        pass

    def get_start_up(self):
        """
        获取小程序启动时间
        """
        return 0

    def click_coordinate(self, x, y):
        """
        按坐标点击
        :param x:
        :param y:
        :return:
        """
        raise NotImplementedError()

    def hide_keyboard(self):
        """
        隐藏键盘
        :return:
        """
        raise NotImplementedError()


class NativeError(RuntimeError):
    pass
