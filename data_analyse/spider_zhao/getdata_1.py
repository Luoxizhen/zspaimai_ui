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
    def spider_search(self,search_good,f):
        '''解析赵涌在线搜索页面的拍品'''
        a = bytes(search_good,'utf-8') #先将被搜索拍品的名称转换为字节
        b_good =str(a).replace("\\x",'%').replace("b'","").replace("'","") #字节串整理
        url = "https://www.zhaoonline.com/search/?channelModule=trade&channelModuleBackup=trade&keyword=" + b_good #搜索网址
        html = self.downloader.download(url) #页面下载
        if html:
            page_count = self.parser.parser_page_num(html) # 获取拍品页面总数
            page_num = page_count['page_num']
            url_info = page_count['url'].split(search_good)

            # if int(num) > 20:
            #
            #     page_num = int(num)//20 + 1 #除法，向下取整
            #     print(page_num)
            # else:
            #     page_num =1
        for i in range(page_num):
            if i == 0:
                data = self.parser.parser(html)
            else:
                g_url = "https://www.zhaoonline.com" + url_info[0] + b_good + url_info[1].removesuffix('.htm')[:-1] + str(
                    i + 1) + ".htm"
                html = self.downloader.download(g_url)
                data = self.parser.parser(html)
            try:
                self.output.store_data(data)
                self.output.output_csv(f)
                self.output.clear_data()
            except Exception as e:
                print(e)








    def spider(self,b_url,page_num,f):
        #添加初始url self, origin_url
        base_url = b_url
        num = 0
        while(num < page_num):
            try:
                num = num + 1

                print ("正在处理第{}个链接".format(num))
                #从新url仓库中获取url
                new_url = base_url + "8-8-N-N-00-N-0-N-1-N-N-N-N-0-N-N-" + str(num) + ".htm"
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



def search_good():
    '''在赵涌在线上查找拍品'''
    spider = SpiderMan()
    file_path = '/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/数据/高端市场.csv'
    file_out = '/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/分析结果/高端市场活跃数据.csv'
    with open(file_path, mode='r', encoding='utf-8') as f:
        goods = csv.reader(f)
        for good in goods:
            good_name = good[0]  # 拍品名称
            good_name = good_name
            print("开始处理 {} 类别数据".format(good_name))
            spider.spider_search(good_name, file_out)

def get_good():
    '''在赵涌在线上爬取数据'''
    spider1 =SpiderMan()
    url_file = open('/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/赵涌在线硬币的副本.csv',mode='r',encoding='utf-8')

    url_datas = csv.reader(url_file)
    for url_info in url_datas:
        file_name = url_info[0]  # 类目，文件名
        print("开始处理 {} 类别数据".format(file_name))
        root_url = url_info[1] # 基础网址
        page_num = int(url_info[2]) # 总页数

        file_path = '/Users/yuanyuanhe/Desktop/竞拍分析/赵涌在线/2022年3月18日/数据/' + file_name + '.csv'
        spider1.spider(root_url,page_num,file_path)

    print("已保存所有数据")
    url_file.close()


if __name__== "__main__":
    search_good()




    #https://www.zhaoonline.com/search/?channelModule=trade&channelModuleBackup=trade&keyword=1995年熊猫12盎司精制金币一枚
    #https://www.zhaoonline.com/search/1995年中国传统文化第（1）组1盎司精制金币五枚一套-8-8-trade-N-N-00-N-0-N-1-N-N-N-N-0-N-1,0-2.htm
    #https://www.zhaoonline.com/search/?channelModule=trade&channelModuleBackup=trade&keyword=1995%E5%B9%B4%E7%86%8A%E7%8C%AB12%E7%9B%8E%E5%8F%B8%E7%B2%BE%E5%88%B6%E9%87%91%E5%B8%81%E4%B8%80%E6%9E%9A













