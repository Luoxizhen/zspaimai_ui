import urllib.request

from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
# import urlparse
# import re
# from config.cfg import cm
# import os

'''
DataOutput
'''
class DataOutput(object):
    def __init__(self):
        self.datas = []  #可以将数据暂存在这个列表里
    #每个循环调用一次此函数，暂存数据
    def store_data(self, data):
        if data is None:
            print("data is None")
            return
        self.datas.extend(data)
    #全部页面爬取结束后调用此函数，写入文件
    def output_csv(self,file_name):
        f = open(file_name, mode='a', encoding='utf-8')
        writer = csv.writer(f)
        try:
            writer.writerows(self.datas)
            # log.info("数据写入{}成功".format(file_name))
        except Exception as e:
            print(e)

    def clear_data(self):
        self.datas = []

data_m = DataOutput()