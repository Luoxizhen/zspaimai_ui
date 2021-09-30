#!/usr/bin/env python3
# Created by xiazeng on 2019-06-11
from .basenative import BaseNative, NativeError


class IdeNative(BaseNative):
    mini = None

    def release(self):
        ...

    def start_wechat(self):
        ...

    def stop_wechat(self):
        ...

    def connect_weapp(self, path):
        ...

    def screen_shot(self, filename, return_format="raw"):
        ...

    def pick_media_file(
            self,
            cap_type="camera",
            media_type="photo",
            original=False,
            duration=5.0,
            names=None,
    ):
        ...

    def input_text(self, text):
        ...

    def input_clear(self):
        ...

    def textarea_text(self, text, index=1):
        ...

    def textarea_clear(self, index=0):
        ...

    def allow_login(self):
        ...

    def allow_get_user_info(self, answer=True):
        ...

    def allow_get_location(self, answer=True):
        ...

    def handle_modal(self, btn_text="确定", title: str = None):
        if self.mini:
            return self.mini.app.evaluate("""function(btn_text) {
                    return global.handle_mock_native_modal && global.handle_mock_native_modal(btn_text)
                }""", args=[btn_text, ], sync=True).get("result", {}).get("result")

    def handle_action_sheet(self, item):
        ...

    def forward_miniprogram(
            self, names, text: str = None, create_new_chat: bool = True
    ):
        ...

    def forward_miniprogram_inside(self, names, create_new_chat: bool = True):
        ...

    def send_custom_message(self, message=None):
        ...

    def phone_call(self):
        ...

    def map_select_location(self, name):
        if self.mini:
            return self.mini.app.evaluate("""function(name) {
                    return global.handle_mock_map_modal && global.handle_mock_map_modal("确定")
                }""", args=[name, ], sync=True).get("result", {}).get("result")

    def map_back_to_mp(self):
        if self.mini:
            return self.mini.app.evaluate("""function() {
                    return global.handle_mock_map_modal && global.handle_mock_map_modal("取消")
                }""", sync=True).get("result", {}).get("result")

    def deactivate(self, duration):
        ...

    def get_authorize_settings(self):
        ...

    def back_from_authorize_setting(self):
        ...

    def authorize_page_checkbox_enable(self, name, enable):
        ...
