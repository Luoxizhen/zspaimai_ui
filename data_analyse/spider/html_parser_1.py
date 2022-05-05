import urllib.request

from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
import urlparse
import re
class HtmlParser(object):
    def parser(self, html_cont):
        """开始解析数据"""
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        goods_in_page = soup.find('table').find_all('tr')
        goods=[]
        for i in range(1,int(len(goods_in_page))):
            good = []
            good_info = goods_in_page[i].find_all('td')
            name = good_info[0].text #拍品名称
            quantity = good_info[1].text #品相
            price = good_info[2].text[good_info[2].text.find('¥')::].removeprefix('¥ ') #总价
            d_time_temp = good_info[3].find('time').text
            d_time = d_time_temp[d_time_temp.find('-')-4:d_time_temp.find('-')+15:] #订单生成时间
            id = good_info[3].find('a').get('vlaue') #拍品id
            good.append(id)
            good.append(name)
            good.append(quantity)
            good.append(price)
            good.append(d_time)


            goods.append(good)
        return goods