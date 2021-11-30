from base.webpage import Web
from common.readelement import Element
mb = Element("mybid")
class MyBid(Web):
    '''我的竞买页面'''
    def win_list(self):
        self.is_click(mb["中标记录"])
    def all_bid_list(self):
        self.is_click(mb["全部竞买"])
    def my_proxy(self):
        self.is_click(mb["我的代理"])
    def my_favorite(self):
        self.is_click(mb["关注"])
    def select(self):
        self.is_click(mb["第一个记录"])
    def all_to_pay(self):
        self.element_text("合计")
    def pay(self):
        self.is_click(mb["去支付"])
