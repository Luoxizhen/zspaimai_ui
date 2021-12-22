from bs4 import BeautifulSoup

import re    #正则表达式模块
# import urlparse    #用来拼接url
from bs4 import BeautifulSoup
import codecs

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
    def parser1(self,html_cont):
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        print(soup.ul)
        return soup.ul


    #
    # def _get_new_urls(self, page_url, soup):
    #     '''
    #     从页面中抽取指向其他词条的链接
    #     parm page_url: 当前页面url
    #     parm soup: beautifulsoup对象
    #     return: 新url的set
    #     '''
    #     new_urls = set()
    #     #根据正则表达式规则对页面内的链接进行筛选，留下想要的链接
    #     links = soup.find_all('a', href=re.compile(r'/item/.+'))
    #     for link in links:
    #         #每个link都是Tag对象，Tag对象的操作方法与字典相同
    #         new_url = link['href']
    #         #借助urljoin，可以很方便地拼接url
    #         new_full_url = urlparse.urljoin(page_url, new_url)
    #         new_urls.add(new_full_url)
    #     return new_urls

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
        self.datas.append(data)
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
class UrlManager(object):
    def __init__(self):
        #初始化的时候就生成两个url仓库
        # self.new_urls = set()
        self.new_urls = ["http://www.huabid.com/auctionList/all/fixedPrice/selling?pageNo=3"]
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
            print ("该页面下载成功！{}".format(url))
            print(r.text)
            return r.text
        else:
            print ("该页面下载失败！{}".format(url))
        return None




new_urls = set()
new_urls=("http://www.huabid.com/auctionList/all/fixedPrice/selling?pageNo=3")
data = {}

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
        self.output.store_data(data)

    def spider(self, origin_url):
        #添加初始url

        self.manager.add_new_url(origin_url)
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
                    new_urls, data = self.parser.parser(new_url, html)
                except Exception as e:
                    print (e)
                for url in new_urls:
                    self.manager.add_new_url(url)
                #将已经爬取过的这个url添加至老url仓库中
                self.manager.add_old_url(new_url)
                #将返回的数据存储至文件
                try:
                    self.output.store_data(data)
                    print ("store data succefully")
                except Exception as e:
                    print (e)
                print ("第{}个链接已经抓取完成".format(self.manager.old_url_size()))

            except Exception as e:
                print (e)
        #爬取循环结束的时候将存储的数据输出至文件
        self.output.output_html()
if __name__== "__main__":
    soup = BeautifulSoup(open('华宇.html'))

    # print(soup.find_all("ul",class_="tile fix"))
    a = soup.find_all("ul",class_="tile fix")
    print(type(a[0]))

    b = BeautifulSoup(markup=str(a[0]))
    print(len(b.ul.contents))
    # for good in b.ul.contents:
    #     good_info = BeautifulSoup(markup=str(good))
    print(b.ul.contents[1])
    good_info = BeautifulSoup(markup=str(b.ul.contents[1]))
    good_picture = good_info.div.table.tr.td.img['src']
    good_name = good_info.p.a['title']

    good_o = BeautifulSoup(markup=str(good_info.find_all('p')[1]))

    good_price = good_o.string_container()

    print("拍品照片：{}".format(good_picture))
    print("拍品名称：{}".format(good_name))
    # print("拍品所有信息：{}".format(str(good_price)))
    print("拍品价格：{}" .format(type(good_price)))
    print("拍品品相：{}" .format(good_price))
    print(type(good_info.stripped_strings))
    for string1 in good_info.stripped_strings.__hash__():
        print(type(string1))
        print(string1)







