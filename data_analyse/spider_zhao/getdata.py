import urllib.request

from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
import urlparse
import re

import html_outputer,html_downloader,html_parser,url_manager








class SpiderMan(object):
    def __init__(self):
        #调度器内包含其它四个元件，在初始化调度器的时候也要建立四个元件对象的实例
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.output = html_outputer.DataOutput()
        print("ppp")
    # def spider(self):
    #     #添加初始url self, origin_url
    #     base_url = "http://www.huabid.com/auctionList/all/fixedPrice/selling?pageNo="
    #     for i in range(12):
    #         url = base_url + str(i)
    #         self.manager.add_new_url(url)
    #     #下面进入主循环，暂定爬取页面总数小于100
    #     num = 0
    #     while(self.manager.has_new_url() and self.manager.old_url_size()<100):
    #         try:
    #             num = num + 1
    #             print ("正在处理第{}个链接".format(num))
    #             #从新url仓库中获取url
    #             new_url = self.manager.get_new_url()
    #             #调用html下载器下载页面
    #             html = self.downloader.download(new_url)
    #             #调用解析器解析页面，返回新的url和data
    #             try:
    #                 new_urls, data = self.parser.parser(new_url, html)
    #                 data = self.parser.parser1(html)
    #             except Exception as e:
    #                 print (e)
    #             for url in new_urls:
    #                 self.manager.add_new_url(url)
    #             #将已经爬取过的这个url添加至老url仓库中
    #             self.manager.add_old_url(new_url)
    #             # 将返回的数据存储至文件
    #             try:
    #                 self.output.store_data(data)
    #                 print ("store data succefully")
    #             except Exception as e:
    #                 print (e)
    #             print ("第{}个链接已经抓取完成".format(self.manager.old_url_size()))
    #
    #         except Exception as e:
    #             print (e)
    #     # 爬取循环结束的时候将存储的数据输出至文件
    #     self.output.output_html()
    # def spider2(self):
    #     s1 = "8-8-N-N-00-N-0-N-1-N-N-N-N-0-N-N-"
    #     s2 = ".htm"
    #     base_url = "https://www.zhaoonline.com/trade/zhongguojindaijizhibi/"
    #     for i in range(1,1001):
    #         # 页面网址拼接
    #         url = base_url + s1 + str(i) + s2
    #         self.manager.add_new_url(url) #将网址添加到网络管理器到新仓库中
    #         while (self.manager.has_new_url()):
    #             try:
    #                 new_url = self.manager.get_new_url()
    #                 html = self.downloader.download(new_url)
    #                 try:
    #                     data = self.parser.parser1(html)
    #                     self.output.store_data(data)
    #                     fn = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表_中国近代机制币.csv"
    #                     self.output.output_csv(fn)
    #                 except Exception as e:
    #                     print(e)
    #                     log.info(e)
    #             except Exception as e:
    #                 print(e)
    #                 log.info(e)
    # def spider1(self):
    #     s1 = "8-8-N-N-00-N-0-N-1-N-N-N-N-0-N-N-"
    #     s2 = ".htm"
    #     with open("/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线.csv",'r') as f:
    #         lines = csv.reader(f)
    #         for line in lines:
    #             base_url = line[1]
    #             page_num = int(line[2]) + 1
    #             collection_index = line[0]
    #             for p in range(1,page_num+1):
    #                 url = base_url + s1 + str(p) + s2
    #                 self.manager.add_new_url(url)
    #             while (self.manager.has_new_url()):
    #                 try:
    #                     new_url = self.manager.get_new_url()
    #                     html = self.downloader.download(new_url)
    #                     try:
    #                         data = self.parser.parser1(html,collection_index)
    #                         self.output.store_data(data)
    #                         fn = "/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线_拍品列表.csv"
    #                         self.output.output_csv(fn)
    #
    #
    #                     except Exception as e:
    #                         print(e)
    #                 except Exception as e:
    #                     print(e)



    def craw(self,root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("craw %d:%s"%(count,new_url))
                # 下载网页
                html_cont = self.downloader.download(new_url)
                # print(html_cont)
                # 解析网页
                new_urls,new_data = self.parser.parser(new_url,html_cont)
                print(new_data)
                print(new_urls)
                self.urls.add_new_urls(new_urls)
                #网页输出器收集数据
                self.output.output_html(new_data)
                if count == 10:
                    break
                count = count+1
            except:
                print("craw faild")
        self.output.output_html()






if __name__== "__main__":
    root_url = "https://www.zhaoonline.com"
    spider1 =SpiderMan()
    spider1.craw(root_url)



