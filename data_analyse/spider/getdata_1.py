import time
import urllib.request

from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
import urlparse
import re

import html_outputer_1,html_downloader_1,html_parser_1,url_manager
class SpiderMan(object):
    def __init__(self):
        #调度器内包含其它四个元件，在初始化调度器的时候也要建立四个元件对象的实例
        self.manager = url_manager.UrlManager()
        self.downloader = html_downloader_1.HtmlDownloader()
        self.parser = html_parser_1.HtmlParser()
        self.output = html_outputer_1.DataOutput()
        print("ppp")
    def spider(self,b_url,page_num,f):
        #添加初始url self, origin_url
        base_url = b_url
        num = 0
        while(num < page_num):
            try:
                num = num + 1

                print ("正在处理第{}个链接".format(num))
                #从新url仓库中获取url
                new_url = base_url + str(num)
                # print("链接：{}".format(new_url))
                #调用html下载器下载页面

                html = self.downloader.download(new_url)
                if html == None:
                    for i in range(10):
                        time.sleep(2)
                        html = self.downloader.download(new_url)
                        if html:
                            break

                        if i ==9 and html == None:
                            log.error("页面无法获取{}，请重新获取".format(new_url))




                #调用解析器解析页面，返回新的url和data
                if html :
                    try:
                        data = self.parser.parser(html)
                        self.output.store_data(data)
                        self.output.output_csv(f)
                        self.output.clear_data()
                    except Exception as e:
                        print(e)

            except Exception as e:
                print(e)







if __name__== "__main__":

    spider1 =SpiderMan()
    url_file = open('/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/华宇商城网址.csv',mode='r',encoding='gbk')
    url_datas = csv.reader(url_file)
    for url_info in url_datas:
        file_name = url_info[0]  # 类目，文件名
        print("开始处理 {} 类别数据".format(file_name))
        root_url = url_info[1] # 基础网址
        page_num = int(url_info[2]) # 总页数

        file_path = '/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖/' + file_name + '.csv'
        spider1.spider(root_url,page_num,file_path)

    print("已保存所有数据")













