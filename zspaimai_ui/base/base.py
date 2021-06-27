from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

# driver 继承 selenium.webdriver.remote.webdriver.py
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


