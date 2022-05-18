import sys
import urllib.request
import os
from bs4 import BeautifulSoup
import codecs
import requests
import csv
from utils.log import log
# import urlparse
# import re
# from html_downloader_1c import HtmlDownloader
class HtmlParser(object):
    def __init__(self):
        self.contact_pre = ""
    def parser_1c(self, html_cont):
        """开始解析数据，从页面中获取带有'求购'、'收购'、'购'帖子的标题，将论坛分为求购的和销售的"""
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='gb2312')
        titles_in_page = soup.find("form").find_all('div', class_="listtitle")
        purcharses = [] #存取购买信息
        sales = [] #存取销售信息
        purcharse_words = ['求购','收购','购',"收","求"]
        for i in range((len(titles_in_page))):
            buy_info = []
            sell_info = []
            title_s = titles_in_page[i].find('a').get('title') #论坛标题
            title_s1 = str(title_s)[:str(title_s).find("作者：")-1:]
            href = titles_in_page[i].find('a').get('href') #href="dispbbs.asp?boardID=11&ID=28379371&page=1" 论坛详情网址
            if any(wd in title_s1 for wd in purcharse_words): #提取帖子中含有 求购 信息的帖子
                buy_info.append(title_s)
                buy_info.append(href)
                purcharses.append(buy_info)
            else: #非求购的帖子归入另一个文件
                sell_info.append(title_s)
                sell_info.append(href)
                sales.append(sell_info)
        return [purcharses,sales]

    def parser_contact(self,board_info):
        '''解析 1尘 网博主发布的信息'''
        soup = BeautifulSoup(board_info, 'html.parser', from_encoding='gb2312')
        first_floor = soup.find("div", class_="post")  # 楼主发布的内容
        contact_1 = first_floor.find("div")

        contact = first_floor.find("div", style="width:85%;overflow-x: hidden;")  # 楼主的个人基本信息
        print(contact)
        content = str(first_floor).replace(str(contact),"").replace(str(contact_1),"") #楼主发布的信息
        print("start")
        while content.find("<") != -1: # 去掉格式
            start_s = content.find("<")
            end_s = content.find(">")+1
            temp_s = content[start_s:end_s]
            content = content.replace(temp_s,"")
        print(content)

        return {"content":content,"contact":contact}

    def parser_page_href(self,html_cout):
        '''搜索页面的下一页的网址'''
        soup = BeautifulSoup(html_cout, 'html.parser', from_encoding='gb2312')
        try:
            page_href = soup.find('table', class_="tableborder5").find_all("td",class_="tablebody1")[3].find("a").get("href")# 页面导航栏搜索
            if "page=" in page_href:
                print(page_href[:-1:])
                return (page_href[:-1:])
        except Exception as e:
            print(e) #'NoneType' object has no attribute 'get'
            print(soup.find('table', class_="tableborder5").find_all("td",class_="tablebody1"))
            log.info(e)







