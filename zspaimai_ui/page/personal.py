from base.webpage import Web
from common.readelement import Element
personal = Element("personal")
class Personal(Web):
    def money(self):
        return self.element_text(personal["钱包余额"])
    def quota(self):
        return self.element_text(personal["竞买额度"])
    def nickname(self):
        return self.element_text(personal["默认昵称"])
    def userno(self):
        return self.element_text(personal["用户编码"])
    def money_tip(self):
        return self.element_text(personal["余额用途"])
    def quota_tip(self):
        return self.element_text(personal["额度用途"])
    def money_detail(self):
        self.is_click(personal['查看余额'])
    def quota_detail(self):
        self.is_click(personal['查看额度'])
    def unpay_order(self):
        self.is_click(personal['待支付'])
    def unpay_order1(self):
        self.is_click(personal['待支付1'])
    def undelivery_order(self):
        self.is_click(personal['待发货'])
    def undelivery_order1(self):
        self.is_click(personal['待发货1'])
    def untake_order(self):
        self.is_click(personal['待收货'])
    def untake_order1(self):
        self.is_click(personal['待收货1'])

    def all_order(self):
        self.is_click(personal['全部'])
    def all_order1(self):
        self.is_click(personal['全部1'])
    def my_order(self):
        self.is_click(personal['我的订单展开'])
