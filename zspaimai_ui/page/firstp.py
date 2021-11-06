from selenium import webdriver
from base.base import Web, Webe
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class Firstp(Web,Webe):

    # 页面底部元素定位 ： 新手指南
    guideL = (By.XPATH, '//div[text()=" 新手指南 "]')
    # 竞买须知
    biddingInfo = (By.XPATH, '//div[text()=" 竞买须知 "]')
    #  关于我们
    aboutUs = (By.XPATH, '//div[text()=" 关于我们 "]')
    #  服务协议
    serviceA = (By.XPATH, '//div[text()=" 服务协议 "]')
    #  藏品保障
    collectionGuarantee = (By.XPATH, '//div[text()=" 藏品保障 "]')
    #  联系我们
    contactUs = (By.XPATH, '//div[text()=" 联系我们 "]')
    # 粤ICP备2021041206号
    ipL = (By.XPATH, '//div[text()="粤ICP备2021041206号"]')


    # 页面顶部元素定位  top-nav-container content 未登陆
    loginB = (By.XPATH, '//div[text()="未登录"]')
    #退出登陆
    logoutB = (By.XPATH, '//div[text()=" 退出登录 "]')
    #'帮助中心'
    helpB = (By.XPATH, '//div[text()=" 帮助中心 "]')
    #'联系我们'
    contactB = (By.XPATH, '//div[text()=" 联系我们 "]')
    #'header - container 我对竞买'
    myBidB = (By.XPATH, '//div[text()=" 我的竞买 "]')
    #'header - container 消息'
    myMsgB = (By.XPATH, '//span[text()="消息"]')
    #' 我要申请委托'
    myApplyB = (By.XPATH, '//*[@id="app"]/div[3]')
    # 页面导航栏元素定位  'header - container:  nav-container-box 首页'
    firstPage = (By.XPATH, '//span[text()="首页"]')
    #'header - container:  nav-container-box 竞买'
    bid = (By.XPATH, '//span[text()="竞买"]')
    #'header - container:  nav-container-box 专场'
    specialP = (By.XPATH, '//span[text()="专场"]')
    #'header - container:  nav-container-box 委托'
    apply = (By.XPATH, '//span[text()="委托"]')
    #'搜索框'
    searchBox = (By.TAG_NAME, 'input')
    #'搜索按钮'
    searchButton = (By.XPATH, '//input/../../div[2]')
    # 搜索历史文本
    historyText = (By.XPATH, '//span[text()="搜索历史"]')
    # 删除搜索历史按钮
    deleteIcon = (By.XPATH, '//span[text()="搜索历史"]/../img')
    # 历史为空文本
    historyIsNull = (By.XPATH, '//div[text()=" 历史为空 "]')
    # 搜索历史框
    historyBox = (By.XPATH, '//div[@class="historyBox"]')
    # 搜索历史列表第一条记录
    lastRecoItem = (By.XPATH, '//div[@class="recoList"]/div[1]')


    # 登录框
    loginBox = (By.XPATH, '//div[@class="login-box"]')
    # 热门拍品底部 更多拍品
    moreCollection = (By.XPATH, '//div[text()=" 更多拍品 "]')
    # 更多拍品后的 按钮
    moreCollectionId = (By.XPATH, '//div[text()=" 更多拍品 "]/../div[2]')
    # 中晟在线二维码
    qrcode = (By.XPATH, '//img[@class="qrcode"]')
    # 广告关闭按钮
    airCommandClose = (By.XPATH, '//img[@class="cursor close"]')
    # 广告体
    airCommand = (By.XPATH, '//div[@class="airCommand"]')







    def click_loginB(self):
        self.driver.find_element(*self.loginB).click()

    def click_helpB(self):
        self.driver.find_element(*self.helpB).click()
    def click_contactB(self):
        self.driver.find_element(*self.contactB).click()


    def send_search_info(self,key):
        '''搜索输入框输入信息'''
        self.driver.find_element(*self.searchBox).send_keys(key)
    def click_searchBox(self):
        '''点击搜索输入框'''
        self.driver.find_element(*self.searchBox).click()
    def searchBoxE(self):
        return self.driver.find_element(*self.searchBox)
    def get_infoOfSearchBox(self):
        '''获取搜索框的默认文本'''
        return self.searchBoxE().get_attribute("placeholder")

    def click_firstPage(self):
        self.driver.find_element(*self.firstPage).click()
    def click_bid(self):
        self.driver.find_element(*self.bid).click()
    def click_apply(self):
        self.driver.find_element(*self.apply).click()
    def click_specialP(self):
        self.driver.find_element(*self.specialP).click()
    def click_myBidB(self):
        self.driver.find_element(*self.myBidB).click()
    def click_myMsgB(self):
        self.driver.find_element(*self.myMsgB).click()
    def click_guildL(self):
        self.driver.find_element(*self.guideL).click()
    # 点击页面底部链接
    def click_guildL(self):
        self.driver.find_element(*self.guideL).click()
    def click_biddingInfo(self):
        self.driver.find_element(*self.biddingInfo).click()
    def click_aboutUs(self):
        self.driver.find_element(*self.aboutUs).click()
    def click_serviceA(self):
        self.driver.find_element(*self.serviceA).click()
    def click_collectionGuarantee(self):
        self.driver.find_element(*self.collectionGuarantee).click()
    def click_contactUs(self):
        self.driver.find_element(*self.contactUs).click()
    def click_myApplyB(self):
        self.driver.find_element(*self.myApplyB).click()
    def click_moreCollection(self):
        self.driver.find_element(*self.moreCollection).click()
    def click_moreCollectionID(self):
        self.driver.find_element(*self.moreCollectionId).click()
    def click_ipL(self):
        self.driver.find_element(*self.ipL).click()
    def get_historyBoxP(self):
        return self.driver.find_element(*self.historyBox).is_displayed()
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
    def click_airCommand(self):
        self.driver.find_element(*self.airCommandClose).click()






