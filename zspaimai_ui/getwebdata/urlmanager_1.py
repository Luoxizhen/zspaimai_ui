from bs4 import BeautifulSoup

import re    #正则表达式模块
# import urlparse    #用来拼接url
from bs4 import BeautifulSoup
import codecs
import requests
import csv

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
        print ("soup established")
        #接下来分别调用两个私有函数返回urls和data
        new_urls = self._get_new_urls(page_url, soup)
        print ("new_urls get")
        new_data = self._get_new_data(page_url, soup)
        print ("new_data get")
        return new_urls, new_data
    def parser1(self,html_cont,good_index):
        '''解析页面数据，并保存到csv 文件中'''
        # soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        # print(soup.ul)
        # return soup.ul
        """开始解析数据"""
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')


        c = soup.table.find_all('tr')
        goods=[]

        for i in range(1, int(len(c))):
            # print(i)
            # print(40 * '*')
            # print(c[i])
            # print(goods[2*i+1])
            good_info = BeautifulSoup(markup=str(c[i]))
            # print(good_info)
            # print(b.ul.contents[1])
            # good_info = BeautifulSoup(markup=str(b.ul.contents[1]))

            d = good_info.find_all('td')
            # with open("华宇商城.csc",mode='a',encoding='utf-8') as f:
            #     f.write(good_picture,good_name,good_pp[1],good_pp[0])
            good_picture = d[0].a['href']

            good_name = d[1].a['title']
            good_px = d[2].string
            good_price = str(d[3].string).strip()
            good_t = str(d[4].time.string).strip()

            good = [good_picture, good_name, good_px,good_price,good_t,good_index]
            goods.append(good)
        return goods



            # f = open("华宇商城.csv", mode='a', encoding='utf-8')
            # writer = csv.writer(f)
            #
            # writer.writerow([good_picture, good_name, good_px,good_price,good_t])




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


'''
DataOutput
'''
class DataOutput(object):
    def __init__(self):
        self.datas = []  #可以将数据暂存在这个列表里


    #每个循环调用一次此函数，暂存数据
    def store_data(self, data):
        if data is None:
            print ("data is None")
            return
        # self.datas.append(data)
        # for data in self.datas:
        #     data.append(good_index)
        print(type(data))
        print(len(data))
        self.datas.extend(data)
    #全部页面爬取结束后调用此函数，写入文件
    def output_html(self):
        fout=codecs.open('baike.html', 'w', encoding='utf-8')
        fout.write("<html><head><meta charset='utf-8'></head><body><table>")
        #将data中的三个数据写成表格的一行
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data["url"])
            fout.write("<td>%s</td>" % data["title"])
            fout.write("<td>%s</td>" % data["summary"])
            fout.write("</tr>")
        fout.write("</table></body></html>")
        fout.close()
        self.datas = []

    def output_csv(self,file_name):
        f = open(file_name, mode='a', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerows(self.datas)
        self.datas=[]


class UrlManager(object):
    '''网址管理'''
    def __init__(self):
        #初始化的时候就生成两个url仓库
        self.new_urls = set()
        # self.new_urls = ["http://www.huabid.com/auctionList/all/fixedPrice/selling?pageNo=3"]
        self.old_urls = set()

    #判断新url仓库中是否还有没有爬取的url
    def has_new_url(self):
        return len(self.new_urls)

    #从new_url仓库获取一个新的url
    def get_new_url(self):
        return self.new_urls.pop()

    def add_new_url(self, url):    #这个函数后来用不到了……
        '''
        将一条url添加到new_urls仓库中
        parm url: str
        return:
        '''
        if url is None:
            return
        #只需要判断old_urls中没有该链接即可，new_urls在添加的时候会自动去重
        if url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''
        将多条url添加到new_urls仓库中
        parm url: 可迭代对象
        return:
        '''
        print ("start add_new_urls")
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def add_old_url(self, url):
        self.old_urls.add(url)
        print ("add old url succefully")

    #获取已经爬取过的url的数目
    def old_url_size(self):
        return len(self.old_urls)
class HtmlDownloader(object):
    #获取页面的数据
    def download(self, url):
        print ("start download")
        if url is None:
            return None
            print ("url is None")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
        headers = {'User-Agent':user_agent,
                   "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
                   "Cookie": "JSESSIONID=AC05E2FDC9810C62E74DA730BDDC93D1-n1.f2tomcat8081; Hm_lvt_e0dd1ef7183706c0e3da698a64d63779=1639971730,1639971949,1639973005,1640058157; Hm_lpvt_e0dd1ef7183706c0e3da698a64d63779=1640059396"}
        print ("start requests")
        r = requests.get(url, headers=headers)
        #判断响应状态
        if r.status_code == 200:
            r.encoding = 'utf-8'
            # print ("该页面下载成功！{}".format(url))

            return r.text
        else:
            print ("该页面下载失败！{}".format(url))
        return None





class SpiderMan(object):
    def __init__(self):
        #调度器内包含其它四个元件，在初始化调度器的时候也要建立四个元件对象的实例
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()
        print("ppp")
    def spider1(self):
        new_url = self.manager.get_new_url()
        print(new_url)
        data = self.parser.parser1(new_url)

        self.output.store_data(data,'拍品类别')

    def spider(self):
        #添加初始url self, origin_url
        file = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖1.csv"

        base_url = "http://www.huabid.com/auctionList/treasure/all/history?keyword=&pageNo="
        for i in range(100,171):
            url = base_url + str(i)
            self.manager.add_new_url(url)
        #下面进入主循环，暂定爬取页面总数小于100
        num = 0
        while(self.manager.has_new_url() and self.manager.old_url_size()<100):
            try:
                num = num + 1
                print ("正在处理第{}个链接".format(num))
                #从新url仓库中获取url
                new_url = self.manager.get_new_url()
                #调用html下载器下载页面
                html = self.downloader.download(new_url)
                #调用解析器解析页面，返回新的url和data
                try:
                    # new_urls, data = self.parser.parser(new_url, html)
                    data = self.parser.parser1(html)
                except Exception as e:
                    print (e)
                # for url in new_urls:
                #     self.manager.add_new_url(url)
                #将已经爬取过的这个url添加至老url仓库中
                self.manager.add_old_url(new_url)
                #将返回的数据存储至文件
                try:
                    self.output.store_data(data,'拍品类别')
                    print ("store data succefully")
                except Exception as e:
                    print (e)
                print ("第{}个链接已经抓取完成".format(self.manager.old_url_size()))
                try:
                    filename=''
                    self.output.output_csv(filename)
                except Exception as e:
                    print(e)
            except Exception as e:
                print (e)
    def spider2(self):
        # with open ("/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖.csv",'r') as f:
        #     lines = csv.reader(f)
        #     print(type(lines))
        #     for line in lines:
        #         print("类别:{}".format(line[0]))
        #         print("网址:{}".format(line[1]))
        #         print("页数:{}".format(int(line[2])+1))
        with open("/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖1.csv",'r') as f:
            lines = csv.reader(f)
            for line in lines:
                base_url = line[1]
                page_num = int(line[2]) + 1
                collection_index = line[0]
                for p in range(1,page_num):
                    url = base_url + str(p)
                    self.manager.add_new_url(url)
                while (self.manager.has_new_url()):
                    try:
                        new_url = self.manager.get_new_url()
                        html = self.downloader.download(new_url)
                        try:
                            data = self.parser.parser1(html,collection_index)
                            self.output.store_data(data)
                            fn = "/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖_拍品列表.csv"
                            self.output.output_csv(fn)


                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)








        # 爬取循环结束的时候将存储的数据输出至文件
        # self.output.output_csv()
# if __name__== "__main__":
#     soup = BeautifulSoup(open('华宇拍品.html'))
#
#     # print(soup.find_all("ul",class_="tile fix"))
#     # a = soup.find("table")
#     # b = BeautifulSoup(str(a))
#     c = soup.table.find_all('tr')
#     print(len(c))
#     for i in range(1,int(len(c))):
#         print (i)
#         print(40 *'*')
#         # print(c[i])
#         # print(goods[2*i+1])
#         good_info = BeautifulSoup(markup=str(c[i]))
#         print(good_info)
#         # print(b.ul.contents[1])
#         # good_info = BeautifulSoup(markup=str(b.ul.contents[1]))
#
#         d = good_info.find_all('td')
#         # with open("华宇商城.csc",mode='a',encoding='utf-8') as f:
#         #     f.write(good_picture,good_name,good_pp[1],good_pp[0])
#         good_picture = d[0].img['src']
#
#         good_name = d[1].a['title']
#         good_px = d[2].string
#         good_price = str(d[3].string).strip()
#         good_t = str(d[4].time.string).strip()
#         print(type(good_t))
#
#
#         print("拍品照片：{}".format(good_picture))
#         print("拍品名称：{}".format(good_name))
#         print("拍品价格：{}" .format(good_px))
#         print("拍品品相：{}" .format(good_price))
#         print("拍品成交时间：{}".format(good_t))

if __name__== "__main__":
    SpiderMan().spider2()
    # with open ("/Users/yuanyuanhe/Desktop/竞拍分析/华宇拍卖.csv",'r') as f:
    #     lines = csv.reader(f)
    #     print(type(lines))
    #     for line in lines:
    #         print("类别:{}".format(line[0]))
    #         print("网址:{}".format(line[1]))
    #         print("页数:{}".format(int(line[2])+1))






