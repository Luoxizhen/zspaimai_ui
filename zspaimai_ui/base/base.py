import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from base.browser_driver import select_browser
# driver 继承 selenium.webdriver.remote.webdriver.py

base_url ='http://home.online.zspaimai.cn/'
class Web():
    #构造函数
    def __init__(self, driver):
        self.driver = driver

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





