import sys
import urllib.request
import os
from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
import urlparse
import re
class HtmlParser(object):
    def parser(self, html_cont):
        """开始解析数据，从页面中提取拍品的数据"""
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        goods_in_page = soup.find_all('div',class_='list-item cf')
        goods=[]
        for i in range(int(len(goods_in_page))):
            good = []
            good_info = goods_in_page[i]
            id = good_info.find("div", class_="item-main l").find("a",title="关注")["rel"][0]#拍品id
            name = good_info.find("a",class_="item-title")['title'] #拍品名称 #拍品名称
            quantity = good_info.span.text #品相
            price = good_info.strong.text #总价
            d_time = good_info.find("span",class_="time").text #订单生成时间
            good.append(id)
            good.append(name)
            good.append(quantity)
            good.append(price)
            good.append(d_time)
            goods.append(good)
        return goods
    def parser_page_num(self,html_cout):
        '''搜索页面数据解析，从搜索页面上解析出搜索出的总拍品数量
        当拍品数量超过20 个时，页面才显示出总共包含的拍品数量'''
        soup = BeautifulSoup(html_cout, 'html.parser', from_encoding='urf-8')
        page_div = soup.find('ul',id="page_div") # 页面导航栏搜索
        good_count = {"page_num": 1,"page_url": ""}
        if page_div == None: # 页面没有包含页面导航栏

            return good_count # 只有一页数据
        else:
            num = soup.find('ul',id="page_div").find('li',class_="bold total_count").find('span').text #返回总拍品数量
            url = soup.find('ul',id="page_div").find('a',id="nextPage").get('href')
            good_count["page_num"] = int(num)//20 + 1
            good_count["page_url"] = url
            print(url.split('开元')[1].removesuffix('.htm')[:-1])
            return good_count #除法，向下取整
        # <li class="bold total_count"><span class="pl20 pr5">31</span>项</li>



if __name__ == "__main__":
    f_path = os.path.dirname(os.path.abspath(__file__))
    h_path = os.path.join(f_path,'zhao_serach.html')
    with open(h_path,'r') as f:
        g_info = f.read()

    g = HtmlParser().parser_page_num(g_info)
    print(g)