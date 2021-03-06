import time

from common.readelement import Element
from base.webpage import Web
dp = Element('detail')
class Detail(Web):
    def collection_name(self):
        return self.element_text(dp['拍品名称'])
    def collection_status(self):
        return self.element_text(dp['拍品状态'])
    def collection_price(self):
        return self.element_text(dp['当前价'])
    def bid_status(self):
        return self.element_text(dp['出价状态'])
    def my_status(self):
        return self.element_text(dp['我的状态'])
    def bid_quota(self):
        return self.element_text(dp['竞买额度'])

    def buyer_service_rate(self):
        return self.element_text(dp["服务费"])
    def bid(self,price=None):
        if price:
            self.send_price(price)
        self.is_click(dp["出价按钮"])
    def change_price(self,price=None):
        if price:
            self.send_price(price)
        self.is_click(dp["更新代理价"])
    def button_text(self,name="出价按钮"):
        return self.element_text(dp[name])

    def end_button_text(self):
        return self.element_text(dp["已结束按钮"])
    def proxy(self):
        return self.element_text(dp["更新代理价"])
    def favorite(self):
        self.is_click(dp['收藏'])
    def favorite_src(self):
        return self.find_element(dp['收藏']).get_attribute('src')
    def remind(self):
        self.is_click(dp['提醒'])

    def remind_src(self):
        return self.find_element(dp['提醒']).get_attribute('src')
    def add(self):
        self.is_click(dp['出价+'])
    def minus(self):
        self.is_click(dp['出价-'])
    def send_price(self,txt):
        ele = self.find_elements(dp['出价金额'])[1]
        ele.clear()
        ele.send_keys(txt)
    def click_close_login(self):
        self.is_click(dp['关闭'])
    def start_time(self):
        return self.element_text(dp['竞买开始时间'])
    def end_time(self):
        return self.element_text(dp['竞买结束时间'])
    def bid_price(self):
        return self.find_elements(dp['出价金额'])[1].get_attribute('value')
    def bid_num(self):
        return self.element_text(dp["出价记录数目"])
    def bid_list(self):
        return self.element_text(dp["出价记录"])
    def pay(self):
        return self.element_text(dp['支付方式'])
    def delivery(self):
        return self.element_text(dp['配送方式'])
    def is_diplayed_loginbox(self):
        return self.find_element(dp["登陆框"]).is_displayed()
    def nickname(self):
        return self.element_text(dp['本场昵称'])
    def nickname_unlogin(self):
        return self.element_text(dp['本场昵称未登陆'])
    def change_nickname(self):
        self.is_click(dp["切换昵称图标"])
    def click_change_nickname(self):
        self.is_click(dp['切换昵称'])
    def close_proxy(self):
        self.is_click(dp["关闭代理"])

    # 出价记录
    def more_bid_price(self):
        self.is_click(dp['查看更多'])
    def is_display_of_bid_price(self):
        return self.find_element(dp['关闭出价记录']).is_displayed()
    def close_bid_price(self):
        self.is_click(dp['关闭出价记录'])



    #登陆操作
    def click_num_login(self):
        self.is_click(dp['账号登陆'])
    def click_login(self):
        self.is_click(dp['登陆按钮'])



    #弹窗操作
    def close_alert(self):
        self.is_click(dp['关闭弹窗'])
    def accept_alert(self):
        self.is_click(dp['弹窗确认'])
    def refuse_alert(self):
        self.is_click(dp['弹窗拒绝'])
    def alert_msg(self):
        self.element_text(dp['弹窗信息'])
    def tip(self):
        return self.element_text(dp['提示信息'])


    # 点击常见问题
    def alway_ask(self):
        #self.move_to_element(dp['常见问题'])
        self.is_click(dp['常见问题'])
    def alway_ask1(self):
        #self.move_to_element(dp['常见问题按钮'])
        self.is_click(dp['常见问题按钮'])
    def is_displayed_of_alway_ask(self):
        return self.find_element(dp['常见问题弹窗']).is_displayed()
    def read_alway_ask(self):
        self.is_click(dp['点击阅读详情'])


    # 提示信息
    def tip_text_of_refresh(self):
        try:
            self.find_element(dp['获取拍品失败'])
        except("TimeoutException(message, screen, stacktrace)"):
            return 1

    # 中拍页面
    def win_price(self):
        return self.element_text(dp["中标价"])
    def win_src(self):
        return self.find_element(dp['中标图标']).get_attribute("src")
    def win_status(self):
        return self.element_text(dp["中标"])

