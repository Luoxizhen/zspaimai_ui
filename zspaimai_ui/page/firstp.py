

from selenium.webdriver.common.by import By

from base.webpage import Web, sleep
from common.readelement import Element
from selenium.common.exceptions import TimeoutException
firstp = Element("firstp")
class Firstp(Web):

    def click_login(self):
        self.is_click(firstp["登陆"])

    def click_help_button(self):
        print(firstp['帮助中心'])
        self.is_click(firstp['帮助中心'])

    def click_contact_button(self):
        print(firstp["联系我们"])
        self.find_elements(firstp["联系我们"])[0].click()


    def input_search(self,content):
        self.input_text(locator=firstp['搜索框'], txt=content)
    def click_search_box(self):
        self.is_click(firstp['搜索框'])
    def get_infoOfSearchBox(self):
        '''获取搜索框的默认文本'''
        return self.searchBoxE().get_attribute("placeholder")
    def info_of_search_box(self):
        return self.find_element(firstp['搜索框']).get_attribute("placeholder")
    def click_first_page(self):
        self.is_click(firstp["首页"])
    def click_bidding(self):
        self.is_click(firstp['竞买'])
    def click_applying(self):
        self.is_click(firstp['委托'])
    def click_special(self):
        self.is_click(firstp['专场'])
    def click_my_bid_button(self):
        self.is_click(firstp['我的竞买'])
    def click_message(self):
        self.is_click(firstp['消息'])
    def click_guild_link(self):
        self.is_click(firstp['新手指南'])

    def click_bidding_info_link(self):
        self.is_click(firstp['竞买须知'])

    def click_about_us_link(self):
        self.is_click(firstp['关于我们'])

    def click_service_link(self):
        self.is_click(firstp['服务协议'])

    def click_collection_guarantee_link(self):
        self.is_click(firstp["藏品保障"])

    def click_contact_us_link(self):
        self.find_elements(firstp["联系我们"])[1].click()

    def click_apply_button(self):
        self.is_click(firstp['我要申请委托'])

    def click_more_collection(self):
        self.is_click(firstp['更多拍品'])

    def click_more_collection_button(self):
        self.is_click(firstp['更多拍品按钮'])
    def is_display_search_history_box(self):
        return self.find_element(firstp['搜索历史框']).is_displayed()

    def src_qrcode_zsonline(self):
        return self.find_element(firstp['中晟在线二维码']).get_property('src')
    def src_qrcode_app(self):
        return self.find_element(firstp['小程序二维码']).get_property('src')
    def src_qrcode_phone(self):
        return self.find_element(firstp['移动端二维码']).get_property('src')
    def is_display_qrcode_phone(self):
        return self.find_element(firstp['移动端二维码']).is_displayed()
    def click_mobile(self):
        self.is_click(firstp['移动端'])


    def is_display_login_box(self):
        return self.find_element(firstp['登陆框']).is_displayed()
    def close_login_box(self):
        self.is_click(firstp['登陆关闭'])
    def login_title(self):
        return self.element_text(firstp["登陆框标题"])
    def nickname(self):
        return self.element_text(firstp['昵称'])

    def click_num_login(self):
        self.is_click(firstp['账号登录'])
    def click_phone_login(self):
        self.is_click(firstp['快捷登录'])
    def send_num(self,num="15622145010"):
        self.input_text(firstp['账号'],num)
    def send_password(self,password="123456"):
        self.input_text(firstp['密码'],password)
    def send_phone(self,phone='15622145010'):
        self.input_text(firstp["手机"], phone)
    def send_vcode(self,vcode='123456'):
        self.input_text(firstp['短信验证码'],vcode)
    def click_send_vcode(self):
        self.is_click(firstp['发送验证码'])
    def click_login_botton(self):
        self.is_click(firstp['登陆按钮'])
    def click_logout(self):
        self.is_click(firstp['退出登录'])
    def click_register(self):
        self.is_click(firstp['注册'])
    def agree(self):
        self.is_click(firstp["我同意并遵守"])
    def login_num_password(self,num="15622145010",password="123456"):
        try:
            self.click_num_login()
        except TimeoutException:
            self.click_login()
            self.click_num_login()
        self.click_num_login()
        self.send_num(num)
        self.send_password(password)
        self.agree()
        self.click_login_botton()

    def search(self, good_name="小林工"):
        self.input_text(firstp['搜索框'],good_name)
    def click_search(self):
        self.is_click(firstp['搜索按钮'])
    def search_history(self):
        return self.element_text(firstp['搜索历史第一条记录'])
    def click_more_collection(self):
        self.is_click(firstp['更多拍品'])
    def click_more_colletion_button(self):
        self.is_click(firstp['更多拍品按钮'])



    #专场操作
    def click_topic1(self):
        self.is_click(firstp["专场一"])
    def topic1_name(self):
        return self.element_text(firstp['专场一名称'])

    def topic1_name1(self):
        return self.element_text(firstp['专场一之名称'])
    def topic1_status(self):
        return self.element_text(firstp['专场一状态']) #进行中，预展，已结束
    def topic1_end_date(self):
        return self.element_text(firstp['专场一之结束时间'])
    def topic1_collection_num(self):
        return self.element_text(firstp['专场一之拍品数'])
    def topic1_bid_num(self):
        return self.element_text(firstp['专场一之出价次数'])


    #拍品操作
    def click_collection(self):
        self.is_click(firstp['拍品一'])
    def click_collection_detail(self, i="拍品详情1"):
        self.is_click(firstp[i])

    def collection_name(self):
        return self.element_text(firstp['拍品一名称'])
    def collection_price(self):
        return self.element_text(firstp['拍品一价格']) #￥10.00
    def click_bid(self):
        self.is_click(firstp['拍品一竞买按钮'])
    def collection_status(self):
        return self.element_text(firstp['拍品一状态']) #正在拍卖、未开始、流拍、已结束
    def click_nickname(self):
        self.is_click(firstp['昵称'])






    # 弹窗
    def is_display_of_dialog(self):
        return self.find_element(firstp["弹窗体"]).is_displayed()
    def close_dialog(self):
        self.is_click(firstp['关闭弹窗'])


