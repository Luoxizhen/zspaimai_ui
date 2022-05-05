import urllib.request

from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
import urlparse
import re
class HtmlParser(object):
    def parser(self, page_url, html_cont):
        '''
        解析器主函数
        parm page_url:一个url
        parm html_cont:网页内容，格式为字符串
        return: urls, 数据；格式为 set, dict
        '''
        if page_url is None or html_cont is None:
            print ("page_url is None")
            return
        #建立bs对象，使用html.parser进行解析
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        print("soup established")

        #接下来分别调用两个私有函数返回urls和data
        new_urls = self._get_new_urls(page_url, soup)
        print("new_urls get")

        new_data = self._get_new_data(page_url, soup)
        print("new_data get")
        return new_urls, new_data


    def _get_new_data(self, page_url, soup):
        '''
        提取想要的数据
        parm page_url: 当前页面url
        parm soup: beautifulsoup对象
        return: dict
        '''
        #声明字典
        data = {}
        data['url'] = page_url
        data['title'] = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1').get_text()
        data['summary'] = soup.find('div', class_='lemma-summary').get_text()
        return data
    def _get_new_urls(self, page_url, soup):
        '''
        从页面中抽取指向其他词条的链接
        parm page_url: 当前页面url
        parm soup: beautifulsoup对象
        return: 新url的set
        '''
        new_urls = set()
        #根据正则表达式规则对页面内的链接进行筛选，留下想要的链接
        links = soup.find_all('a', href=re.compile(r'https://dss0.bdstatic.com/+'))
        for link in links:
            #每个link都是Tag对象，Tag对象的操作方法与字典相同
            new_url = link['href']
            #借助urljoin，可以很方便地拼接url
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls
    def parser1(self, html_cont):
        '''解析页面数据，并保存到csv 文件中'''
        """开始解析数据"""
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        c = soup.find_all('div',class_='list-item cf')
        goods=[]
        for i in range(int(len(c))):
            good_info = BeautifulSoup(markup=str(c[i]), features='html.parser')
            good_link = good_info.a['href'].removesuffix('.shtml').removeprefix('/') #拍品链接 https://www.zhaoonline.com/auction-detail.shtml?id=5574544
            n = good_link.find('/')+1
            good_id = good_link[n::]
            good_picture = good_info.img['src']
            good_name = good_info.find("a",class_="item-title")['title'] #拍品名称
            good_px = good_info.span.text #品相
            good_price = good_info.strong.text
            good_t = good_info.find("span",class_="time").text #成交时间
            good = [good_id,good_picture, good_name, good_px, good_price, good_t]
            goods.append(good)
        return goods