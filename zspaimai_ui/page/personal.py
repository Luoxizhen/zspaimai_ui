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

    def go_to_page(self,n="个人中心"):
        '''n 为个人中心页面左侧导航栏的名字，点击进入响应页面'''
        self.is_click(personal[n])

    def order_info(self):
        '''订单：拍品3 的详细信息'''
        price = self.element_text(personal["成交价"])
        num = self.element_text(personal["商品数量"])
        total_money = self.element_text(personal["订单总价"])
        pay_time = self.element_text(personal["下单时间"])
        order_num = self.element_text(personal["订单编号"])
        info = {"price":price, "num":num, "total_money":total_money,"pay_time":pay_time,"order_num":order_num}
        return info