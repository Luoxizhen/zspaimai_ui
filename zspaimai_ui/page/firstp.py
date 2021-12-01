

from selenium.webdriver.common.by import By

from base.webpage import Web, sleep
from common.readelement import Element
from selenium.common.exceptions import TimeoutException
firstp = Element("firstp")
class Firstp(Web):
    # # 页面底部元素定位 ： 新手指南
    # guideL = (By.XPATH, '//div[text()=" 新手指南 "]')
    # # 竞买须知
    # biddingInfo = (By.XPATH, '//div[text()=" 竞买须知 "]')
    # #  关于我们
    # aboutUs = (By.XPATH, '//div[text()=" 关于我们 "]')
    # #  服务协议
    # serviceA = (By.XPATH, '//div[text()=" 服务协议 "]')
    # #  藏品保障
    # collectionGuarantee = (By.XPATH, '//div[text()=" 藏品保障 "]')
    # #  联系我们
    # contactUs = (By.XPATH, '//div[text()=" 联系我们 "]')
    # # 粤ICP备2021041206号
    # ipL = (By.XPATH, '//div[text()="粤ICP备2021041206号"]')
    # # 页面顶部元素定位  top-nav-container content 未登陆
    # loginB = (By.XPATH, '//div[text()="未登录"]')
    # #退出登陆
    # logoutB = (By.XPATH, '//div[text()=" 退出登录 "]')
    # #'帮助中心'
    # helpB = (By.XPATH, '//div[text()=" 帮助中心 "]')
    # #'联系我们'
    # contactB = (By.XPATH, '//div[text()=" 联系我们 "]')
    # #'header - container 我对竞买'
    # myBidB = (By.XPATH, '//div[text()=" 我的竞买 "]')
    # #'header - container 消息'
    # myMsgB = (By.XPATH, '//span[text()="消息"]')
    # #' 我要申请委托'
    # myApplyB = (By.XPATH, '//*[@id="app"]/div[3]')
    # # 页面导航栏元素定位  'header - container:  nav-container-box 首页'
    # firstPage = (By.XPATH, '//span[text()="首页"]')
    # #'header - container:  nav-container-box 竞买'
    # bid = (By.XPATH, '//span[text()="竞买"]')
    # #'header - container:  nav-container-box 专场'
    # specialP = (By.XPATH, '//span[text()="专场"]')
    # #'header - container:  nav-container-box 委托'
    # apply = (By.XPATH, '//span[text()="委托"]')
    # #'搜索框'
    # searchBox = (By.TAG_NAME, 'input')
    # #'搜索按钮'
    # searchButton = (By.XPATH, '//input/../../div[2]')
    # # 搜索历史文本
    # historyText = (By.XPATH, '//span[text()="搜索历史"]')
    # # 删除搜索历史按钮
    # deleteIcon = (By.XPATH, '//span[text()="搜索历史"]/../img')
    # # 历史为空文本
    # historyIsNull = (By.XPATH, '//div[text()=" 历史为空 "]')
    # # 搜索历史框
    # historyBox = (By.XPATH, '//div[@class="historyBox"]')
    # # 搜索历史列表第一条记录
    # lastRecoItem = (By.XPATH, '//div[@class="recoList"]/div[1]')
    #
    #
    # # 登录框
    # loginBox = (By.XPATH, '//div[@class="login-box"]')
    # # 热门拍品底部 更多拍品
    # moreCollection = (By.XPATH, '//div[text()=" 更多拍品 "]')
    # # 更多拍品后的 按钮
    # moreCollectionId = (By.XPATH, '//div[text()=" 更多拍品 "]/../div[2]')
    # # 中晟在线二维码
    # qrcode = (By.XPATH, '//img[@class="qrcode"]')
    # # 广告关闭按钮
    # airCommandClose = (By.XPATH, '//img[@class="cursor close"]')
    # # 广告体
    # airCommand = (By.XPATH, '//div[@class="airCommand"]')


    def click_loginB(self):
        self.driver.find_element(*self.loginB).click()
    def click_login(self):
        self.is_click(firstp["登陆"])

    def click_helpB(self):
        self.driver.find_element(*self.helpB).click()
    def click_help_button(self):
        print(firstp['帮助中心'])
        self.is_click(firstp['帮助中心'])
    def click_contactB(self):
        self.driver.find_element(*self.contactB).click()
    def click_contact_button(self):
        print(firstp["联系我们"])
        self.find_elements(firstp["联系我们"])[0].click()


    def send_search_info(self,key):
        '''搜索输入框输入信息'''
        self.driver.find_element(*self.searchBox).send_keys(key)
    def input_search(self,content):
        self.input_text(locator=firstp['搜索框'], txt=content)
    def click_searchBox(self):
        '''点击搜索输入框'''
        self.driver.find_element(*self.searchBox).click()
    def click_search_box(self):
        self.is_click(firstp['搜索框'])
    def searchBoxE(self):
        return self.driver.find_element(*self.searchBox)
    def get_infoOfSearchBox(self):
        '''获取搜索框的默认文本'''
        return self.searchBoxE().get_attribute("placeholder")
    def info_of_search_box(self):
        return self.find_element(firstp['搜索框']).get_attribute("placeholder")

    def click_firstPage(self):
        self.driver.find_element(*self.firstPage).click()
    def click_first_page(self):
        self.is_click(firstp["首页"])
    def click_bid(self):
        self.driver.find_element(*self.bid).click()
    def click_bidding(self):
        self.is_click(firstp['竞买'])

    def click_apply(self):
        self.driver.find_element(*self.apply).click()
    def click_applying(self):
        self.is_click(firstp['委托'])
    def click_specialP(self):
        self.driver.find_element(*self.specialP).click()
    def click_special(self):
        self.is_click(firstp['专场'])
    def click_myBidB(self):
        self.driver.find_element(*self.myBidB).click()
    def click_my_bid_button(self):
        self.is_click(firstp['我的竞买'])
    def click_myMsgB(self):
        self.driver.find_element(*self.myMsgB).click()
    def click_message(self):
        self.is_click(firstp['消息'])


    # 点击页面底部链接
    def click_guildL(self):
        self.driver.find_element(*self.guideL).click()
    def click_guild_link(self):
        self.is_click(firstp['新手指南'])
    def click_biddingInfo(self):
        self.driver.find_element(*self.biddingInfo).click()
    def click_bidding_info_link(self):
        self.is_click(firstp['竞买须知'])
    def click_aboutUs(self):
        self.driver.find_element(*self.aboutUs).click()
    def click_about_us_link(self):
        self.is_click(firstp['关于我们'])

    def click_serviceA(self):
        self.driver.find_element(*self.serviceA).click()
    def click_service_link(self):
        self.is_click(firstp['服务协议'])
    def click_collectionGuarantee(self):
        self.driver.find_element(*self.collectionGuarantee).click()
    def click_collection_guarantee_link(self):
        self.is_click(firstp["藏品保障"])
    def click_contactUs(self):
        self.driver.find_element(*self.contactUs).click()
    def click_contact_us_link(self):
        self.find_elements(firstp["联系我们"])[1].click()
    def click_myApplyB(self):
        self.driver.find_element(*self.myApplyB).click()
    def click_apply_button(self):
        self.is_click(firstp['我要申请委托'])
    def click_moreCollection(self):
        self.driver.find_element(*self.moreCollection).click()
    def click_more_collection(self):
        self.is_click(firstp['更多拍品'])
    def click_moreCollectionID(self):
        self.driver.find_element(*self.moreCollectionId).click()
    def click_more_collection_button(self):
        self.is_click(firstp['更多拍品按钮'])
    def click_ipL(self):
        self.driver.find_element(*self.ipL).click()
    def get_historyBoxP(self):
        return self.driver.find_element(*self.historyBox).is_displayed()
    def is_display_search_history_box(self):
        return self.find_element(firstp['搜索历史框']).is_displayed()
    def get_historyTextP(self):
        return self.driver.find_element(*self.historyText).is_displayed()
    def get_deleteIcon(self):
        return self.driver.find_element(*self.deleteIcon).is_displayed()
    def click_searchButton(self):
        self.driver.find_element(*self.searchButton).click()
    def get_lastReco(self):
        return self.driver.find_element(*self.lastRecoItem).text
    def click_delectIcon(self):
        self.driver.find_element(*self.deleteIcon).click()
    def get_qrcodeP(self):
        return self.driver.find_element(*self.qrcode).get_property('src')
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

    def click_airCommand(self):
        self.driver.find_element(*self.airCommandClose).click()
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
    def click_collection_detail(self, i="拍品详情"):
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









