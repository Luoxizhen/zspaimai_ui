import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from selenium import webdriver
def select_browser(browser='chrome'):
    dr = None
    if browser == "chrome" or browser == "Chrome":
        dr = webdriver.Chrome()
    elif browser == "firefox" or browser == "ff":
        dr = webdriver.Firefox()
    elif browser == "IE" or browser == "ie":
        dr = webdriver.Ie()
    else:
        print("请输入正确的浏览器名称")
    return dr
