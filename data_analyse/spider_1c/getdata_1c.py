import time
import urllib.request
from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
import html_outputer_1c,html_downloader_1c,html_parser_1c,url_manager
class SpiderMan(object):
    '''从一尘网上获取数据'''
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
        for i in range(1,100):
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
                    data = self.parser.parser_1c_title(html)
                    self.output.store_data(data)
                    self.output.output_csv(file_name=f[0])
                    # self.output.store_data(data[0])
                    # self.output.output_csv(f[0])
                    # self.output.clear_data()
                    # self.output.store_data(data[1])
                    # self.output.output_csv(f[1])
                    # self.output.clear_data()
                except Exception as e:
                    print(e)

    def spider_title(self):
        '''boardid: 论坛标题
        148 为古币银元
        151 连体钞、纪念钞'''
        url = "http://www.lc0011.net/index.asp?boardid=148"


        base_url = "http://www.lc0011.net/index.asp"
        href_url = SpiderMan().get_href(url)

        f1 = "/Users/yuanyuanhe/Desktop/古币_帖子标题.csv"
        f2 = "/Users/yuanyuanhe/Desktop/古币_卖.csv"
        f = [f1, f2]
        self.spider(base_url + href_url, *f)
    def get_href(self,b_url):
        '''获取下一个页面的网址
        b_url 基本网址'''
        html = self.downloader.download(b_url)
        href_url = self.parser.parser_page_href(html)
        print(href_url)
        return href_url
    def get_contact(self,num=0,*f):
        '''爬取用户的基本信息
        num : 行数
        *f 文件路径，包含
        f1 : 含url 的文件 "/Users/yuanyuanhe/Desktop/评级币评级钞_卖_去重复去空.csv"
        f2 : 用户数据保存的位置 "/Users/yuanyuanhe/Desktop/评级币评级钞_卖家.csv"
        '''
        print(f[0])
        print(f)

        with open(f[0],encoding="utf-8",mode="r") as f_t:

            # csv_reader = csv.DictReader(f_t)
            csv_reader = csv.reader(f_t)
            i = num
            k = 0
            contacts = []
            for row in csv_reader:
                k = k+1

                if k > num:
                    print(k)
                    # url = "http://www.lc0011.net/" + row["url"]
                    url = "http://www.lc0011.net/" + row[1]
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
    f1 = "/Users/yuanyuanhe/Desktop/古币_帖子标题.csv"
    f2 = "/Users/yuanyuanhe/Desktop/古币_帖子详情.csv"
    f = [f1,f2]

    SpiderMan().get_contact(0,*f)














