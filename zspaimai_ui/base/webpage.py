'''那我们为什么要封装selenium的方法呢。首先我们上述这种较为原始的方法，基本不适用于平时做UI自动化测试的，
因为在UI界面实际运行情况远远比较复杂，可能因为网络原因，或者控件原因，我们元素还没有显示出来，就进行点击或者输入。
所以我们需要封装selenium方法，通过内置的显式等待或一定的条件语句，才能构建一个稳定的方法。
而且把selenium方法封装起来，有利于平时的代码维护。
本文件存放selenium 基类的封装方法
'''

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from base.browser_driver import select_browser
from config.conf import cm
from utils.times import sleep
from utils.log import log
# driver 继承 selenium.webdriver.remote.webdriver.py

base_url ='http://home.online.zspaimai.cn/'
class Web(object):
    #构造函数
    def __init__(self,driver):
        self.driver = driver
        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)
    def get_url(self,url):
        '''打开网页并验证'''
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            log.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(cm.LOCATE_MODE[name], value)

    def find_element(self, locator):
        """寻找单个元素"""
        return Web.element_locator(lambda *args: self.wait.until(
            ec.presence_of_element_located(args)), locator)

    def find_elements(self, locator):
        """查找多个相同的元素"""
        return Web.element_locator(lambda *args: self.wait.until(
            ec.presence_of_all_elements_located(args)), locator)


    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        log.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator, txt):
        """输入(输入前先清空)"""
        sleep(0.5)
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)
        log.info("输入文本：{}".format(txt))

    def is_click(self, locator):
        """点击"""
        self.find_element(locator).click()
        sleep()
        log.info("点击元素：{}".format(locator))

    def element_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        log.info("获取文本：{}".format(_text))
        return _text


    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)
    def back(self):
        '''页面返回'''
        self.driver.back()
        self.driver.implicitly_wait(10)




    def findElement(self, *loc):
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException as e:
            print(e.args[0])
    def findElements(self, *loc):
        try:
            return self.driver.find_elements(*loc)
        except NoSuchElementException as e:
            print(e.args[0])

class Webe(WebElement):


    def findElement(self, *loc):
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException as e:
            print(e.args[0])
    def findElements(self, *loc):
        try:
            return self.driver.find_elements(*loc)
        except NoSuchElementException as e:
            print(e.args[0])

class SeleniumHelper:
    '''页面基础类，用于所有页面的继承'''
    def __init__(self, selenium_driver: webdriver, base_url=base_url, parent=None):
        self.driver = selenium_driver
        self.base_url = base_url
        self.parent = parent
    # def screenshort(self):
    #     '''截图并保存'''
    #     img_filename = '%s.png'%time.strftime(%Y_%m_%d_%H_%M_%S)
    #     img_path = globalparam.img_path + '\\'+img_filename
    #     self.driver.get_screenshot_as_file(img_path)
    #     log.info('异常场景已截图保存，文件名为%s'%img_filename)
    def _open(self,url):
        self.driver.get(url)
    def findElement(self, *loc):
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException as e:
            print(e.args[0])
    def findElements(self, *loc):
        try:
            return self.driver.find_elements(*loc)
        except NoSuchElementException as e:
            print(e.args[0])
    def findElemets(self):
        self.driver.find_element





