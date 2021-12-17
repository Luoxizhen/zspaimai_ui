from base.webpage import Web
from common.readelement import Element
mb = Element("mybid")
class MyBid(Web):
    '''我的竞买页面'''
    # def win_list(self):
    #     self.is_click(mb["中标记录"])
    # def all_bid_list(self):
    #     self.is_click(mb["全部竞买"])
    # def my_proxy(self):
    #     self.is_click(mb["我的代理"])
    # def my_favorite(self):
    #     self.is_click(mb["关注"])
    def select(self,n="一",a=""):
        good = "第" + n +"个记录" + a
        self.is_click(mb[good])
    def num_of_select(self):
        return self.element_text(mb["共几项"])
    def all_to_pay(self):
        return self.element_text(mb["合计"])
    def pay(self):
        self.is_click(mb["去支付"])
    def good_info(self):
        '''验证我的竞买第一条记录信息准确'''
        self.swith_to_list("中标记录")
        name = self.element_text(mb["第一个记录名称"])
        price = self.element_text(mb["第一个记录价格"])
        num = self.element_text(mb["第一个记录数量"])
        to_pay = self.element_text(mb["第一个记录总价"])
        status = self.element_text(mb["第一条记录支付状态"])
        service_r = self.element_text(mb["第一条记录服务费"])
        good_info = {"name":name, "price":price, "num":num, "to_pay":to_pay,  "status": status}
        return good_info
    def swith_to_list(self, ln="全部竞买"):
        self.is_click(mb[ln])
    def info_list(self,ln):
        '''验证竞买页面信息'''
        self.swith_to_list(ln)
        info_1 = self.element_text(mb["全部竞买拍品信息"])
        info_2 = self.element_text(mb["全部竞买开拍/结束时间"])
        info_3 = self.element_text(mb["全部竞买当前竞买价"])
        info_4 = self.element_text(mb["全部竞买出价次数"])
        info_5 = self.element_text(mb["全部竞买竞买状态"])
        info_6 = self.element_text(mb["全部竞买开启提醒"])
        info = [info_1, info_2, info_3, info_4, info_5, info_6]
        return info

    def good_in_list(self, l, n="一"):
        self.swith_to_list(l)
        name = "第" + n + "条记录名称"
        status = "第" + n + "条记录状态"
        price = "第" + n + "条记录当前竞买价"
        bid_n = "第" + n + "条记录出价次数"
        my_status = "第" + n + "条记录竞买状态"
        good_name = self.element_text(mb[name])
        good_status = self.element_text(mb[status])
        good_price = self.element_text(mb[price])
        good_bid_n = self.element_text(mb[bid_n])
        my_status_of_good = self.element_text(mb[my_status])
        good_info = {"good_name":good_name,"good_status":good_status,"good_price":good_price,"good_bid_n":good_bid_n,"my_status_of_good":my_status_of_good}
        return good_info
    def remind(self, l, n="一"):
        self.swith_to_list(l)
        n = "第" + n + "条记录开启提醒"
        self.is_click(mb[n])
    def is_displayed_remind_tip(self):
        return self.find_element(mb["开启提醒前提示"]).is_displayed()
    def close_remind_tip(self,n="确认提醒",i=0):
        #self.is_click(mb[n])
        self.find_elements(mb["取消提醒"][i]).click()
    def tip(self):
        return self.element_text(mb['提示内容'])
    def go_to_pay(self,n="一"):
        self.swith_to_list("中标记录")
        self.select(n)
        self.pay()







