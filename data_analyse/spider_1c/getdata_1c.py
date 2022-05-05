import time
import urllib.request

from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
import urlparse
import re

import html_outputer_1c,html_downloader_1c,html_parser_1c,url_manager
class SpiderMan(object):
    def __init__(self):
        #调度器内包含其它四个元件，在初始化调度器的时候也要建立四个元件对象的实例
        self.manager = url_manager.UrlManager()
        self.downloader = html_downloader_1c.HtmlDownloader()
        self.parser = html_parser_1c.HtmlParser()
        self.output = html_outputer_1c.DataOutput()
        print("ppp")

    def spider(self,b_url,*f):
        '''爬取一尘网的论坛标题
        b_url： 论坛的网址
        *f 数据保存文件位置：包括买方文件保存位置及买方文件保存位置'''
        for i in range(1,110):
            url = b_url + str(i)

            html = self.downloader.download(url)
            if html == None:
                for i in range(10):
                    time.sleep(2)
                    html = self.downloader.download(b_url)
                    if html:
                        break
                    if i ==9 and html == None:
                        log.error("页面无法获取{}，请重新获取".format(url))
            #调用解析器解析页面，返回新的url和data
            if html:
                try:
                    data = self.parser.parser_1c(html)
                    self.output.store_data(data[0])
                    self.output.output_csv(f[0])
                    self.output.clear_data()
                    self.output.store_data(data[1])
                    self.output.output_csv(f[1])
                    self.output.clear_data()
                except Exception as e:
                    print(e)
    def get_href(self,b_url):
        '''获取下一个页面的网址
        b_url 基本网址'''
        html = self.downloader.download(b_url)
        href_url = self.parser.parser_page_href(html)
        print(href_url)
        return href_url
    def get_contact(self,num,*f):
        '''爬取用户的基本信息'''
        with open(f[0],encoding="utf-8",mode="r") as f_t:
            csv_reader = csv.DictReader(f_t)
            i = num
            k = 0
            contacts = []
            for row in csv_reader:
                k = k+1
                if k > num:
                    url = "http://www.lc0011.net/" + row["url"]

                    html = self.downloader.download(url)

                    if html:
                        try:
                            contact = self.parser.parser_contact(html)
                            contact["url"] = url
                            contacts.append(contact.values())
                            # contact["title"] = row["title0"]
                        except Exception as e:
                            print(e)

                    i = i+1

                    self.output.store_data(contacts)
                    self.output.output_csv(f[1])
                    self.output.clear_data()
                    contacts = []












if __name__== "__main__":
    # url = "http://www.lc0011.net/index.asp?boardid=11" #http://www.lc0011.net/index.asp?boardid=11?boar
    # base_url = "http://www.lc0011.net/index.asp"
    # href_url = SpiderMan().get_href(url)
    # # file_path ="/Users/yuanyuanhe/Desktop/竞拍分析/一尘/一二三版纸币"
    # # file_paths = [file_path+"/买.csv", file_path+"/卖.csv"]
    # # SpiderMan().spider(base_url+href_url, *file_paths)
    f1 = "/Users/yuanyuanhe/Desktop/卖家.csv"
    f2 = "/Users/yuanyuanhe/Desktop/卖家帖子.csv"
    f = [f1,f2]
    SpiderMan().get_contact(2224,*f)












