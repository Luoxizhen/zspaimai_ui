from base.base import Web
from base.base import SeleniumHelper
from selenium.webdriver.common.by import By
class MyApplyp(SeleniumHelper):
    entrust = (By.XPATH, '//div[text()="委托合同"]')
    applyNow = (By.XPATH, '//div[text()="在线委托申请"]')
    settlementList = (By.XPATH, '//div[text()="结算列表"]')
    collection = (By.XPATH, '//div[text()="我的委托藏品"]')
    entrust_all = (By.XPATH, '//div[text()="全部"]')
    entrust_wait = (By.XPATH, '//div[text()="待受理"]')
    entrust_reorganize = (By.XPATH, '//div[text()="整理中"]')
    entrust_drafting = (By.XPATH, '//div[text()="制图中"]')
    entrust_examine = (By.XPATH, '//div[text()="核查中"]')
    entrust_inspect = (By.XPATH, '//div[text()="检查中"]')
    entrust_executing = (By.XPATH, '//div[text()="执行中"]')
    entrust_executed = (By.XPATH, '//div[text()="已执行"]')
    entrust_cancel = (By.XPATH, '//div[text()="取消受理"]')
    collection_all = (By.XPATH, '//div[text()="全部"]')
    collection_waiting = (By.XPATH, '//div[text()="未开始]')
    collection_bidding = (By.XPATH, '//div[text()="竞买中"]')
    collection_deal = (By.XPATH, '//div[text()="成交"]')
    collection_undeal = (By.XPATH, '//div[text()="未成交"]')
    collection_returned = (By.XPATH, '//div[text()="已退回"]')
    collection_waitaccount = (By.XPATH, '//div[text()="待结算"]')
    collection_accounting = (By.XPATH, '//div[text()="结算中"]')
    collection_accounted = (By.XPATH, '//div[text()="已结算"]')
    collection_all_num = (By.XPATH, '//div[text()="全部"]/span')
    collection_waiting_num = (By.XPATH, '//div[text()="未开始]/span')
    collection_bidding_num = (By.XPATH, '//div[text()="竞买中"]/span')
    collection_deal_num = (By.XPATH, '//div[text()="成交"]/span')
    collection_undeal_num = (By.XPATH, '//div[text()="未成交"]/span')
    collection_returned_num = (By.XPATH, '//div[text()="已退回"]/span')
    collection_waitaccount_num = (By.XPATH, '//div[text()="待结算"]/span')
    collection_accounting_num = (By.XPATH, '//div[text()="结算中"]/span')
    collection_accounted_num = (By.XPATH, '//div[text()="已结算"]/span')
    def click_entrust(self):
        self.driver.find_element(*self.entrust).click()
    def click_entrust_all(self):
        self.driver.find_element(*self.entrust_all).click()
    def click_entrust_cancel(self):
        self.driver.find_element(*self.entrust_cancel).click()
    def click_entrust_wait(self):
        self.driver.find_element(*self.entrust_wait).click()
    def click_entrust_inspect(self):
        self.driver.find_element(*self.entrust_inspect).click()
    def click_entrust_examine(self):
        self.driver.find_element(*self.entrust_examine).click()
    def click_entrust_drafting(self):
        self.driver.find_element(*self.entrust_drafting).click()
    def click_entrust_executed(self):
        self.driver.find_element(*self.entrust_executed).click()
    def click_entrust_executing(self):
        self.driver.find_element(*self.entrust_executing).click()

    def click_applyNow(self):
        self.driver.find_elements(*self.applyNow)[0].click()
    def click_settlementList(self):
        self.driver.find_element(*self.settlementList).click()
    def click_collection(self):
        self.driver.find_elements(*self.collection)[0].click()
    def click_collection_all(self):
        self.driver.find_element(*self.collection_all).click()
    def click_collection_wait(self):
        self.driver.find_element(*self.collection_waiting).click()
    def click_collection_bidding(self):
        self.driver.find_element(*self.collection_bidding).click()
    def click_collection_deal(self):
        self.driver.find_element(*self.collection_deal).click()
    def click_collection_nodeal(self):
        self.driver.find_element(*self.collection_nodeal).click()
    def click_collection_returned(self):
        self.driver.find_element(*self.collection_returned).click()
    def click_collection_waitaccount(self):
        self.driver.find_element(*self.collection_waitaccount).click()
    def click_collection_accounting(self):
        self.driver.find_element(*self.collection_accounting).click()
    def click_collection_accounted(self):
        self.driver.find_element(*self.collection_accounted).click()












