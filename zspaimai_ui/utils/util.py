# coding:utf-8
import json
import random
import sys
import string
def kwargs_to_str(**kwargs):
    ls = []
    for key in kwargs:
        js = {"key": key, "value": kwargs[key]}
        ls.append(js)
    return json.dumps(ls)



def object_to_str(*args):
    s1 = "["
    print(args)
    if args != []:
        for i in range(len(args)):
            print(len(args))
            if type(args[i]) == dict:
                temp = json.dumps(args[i])
                print(temp)
            elif type(args[i]) == int:
                temp = str(args[i])
            else:
                temp = args[i]
            if i != len(args) - 1:

                s1 = s1 + temp + ","
            else:
                print(s1)
                s1 = s1 + temp + "]"
    return s1


def list_nums(fun, key, **list_info):
    list=[]
    r = fun(**list_info).json()['data']
    last_page = r['last_page']
    #print(last_page)
    per_page = r['per_page']
    total = r['total']
    for i in range(1,last_page+1):
        r = fun(page=i, **list_info).json()['data']['data']
        #print(r)
        for j in range(len(r)):
            list.append(r[j][key])
    #print(list)
    return list

def str_to_dict(str):
    '''将接口数据信息中的字符串转换成字典
    字符串："[{\"key\":\"userno\",\"value\":\"\"},{\"key\":\"phone\",\"value\":\"\"},{\"key\":\"is_mobile\",\"value\":\"\"},{\"key\":\"is_real\",\"value\":\"\"},{\"key\":\"status\",\"value\":\"\"},{\"key\":\"is_robot\",\"value\":\"\"}]"
    '''
    d = {}
    l = str.replace("""{\"key\":\"""","").replace("""",\"value\":\"\"}""","").removeprefix('[').removesuffix(']').rsplit(",")
        #str.removeprefix('"').removesuffix(']"').replace("""{\"key\":\"""","").replace("""",\"value\":\"\"}""","")
    for i in l:
        d[i]=""
    return d


def str_to_list(str_image):
    '''用于添加拍品的接口，将images. original_images 的图片字符串转换为list
     输入 ：
     "['thumbnail/2022-01-13/1183-1.jpg', 'thumbnail/2022-01-13/1183-2.jpg']"
     "['picture/2022-01-13/1183-1.jpg', 'picture/2022-01-13/1183-2.jpg']"
     输出:
     ['thumbnail/2021-09-27/537-1.jpg', 'thumbnail/2021-09-27/537-2.jpg']
     ['picture/2021-09-27/537-1.jpg', 'picture/2021-09-27/537-2.jpg']
     '''


    return json.load(str_image)



def list_to_str(list_image):
    '''用于添加拍品的接口，将images. original_images 的图片字符串转换为list
    输入

        ["picture/2021-09-27/537-1.jpg","picture/2021-09-27/537-2.jpg"]
    输出
    "[\"picture/2021-12-23/1075-1.jpg\", \"picture/2021-12-23/1075-2.jpg\"]"

         '''

    return json.dumps(list_image)




def get_random(d=6,level=1):
    '''生成随机码
    2-12 位
    3个等级'''
    digit = d
    if not (2 <= digit <= 12):
        return '密码长度错误'
    if level == 1:
        parents = string.digits
    elif level == 2:
        parents = ''.join((string.ascii_letters, string.digits))
    elif level == 3:
        parents = ''.join((string.ascii_letters, string.digits, string.punctuation))
    else:
        return '密码复杂度 error'
    pwd = ''
    for i in range(digit):
        pwd = ''.join((pwd,random.choice(parents)))
    print('password:', pwd)
    return pwd
def is_Chinese(w):
    if '\u4e00' <= w <= '\u9fff':
        print(w)
        print(1)
        return True
def chinese_name():
    first_name = '''李王张刘陈杨黄赵周吴徐孙朱马胡郭林何高梁郑罗宋谢唐韩曹许邓萧冯曾程蔡彭潘袁於董余苏叶吕魏蒋田杜丁沈姜范江傅钟卢汪戴崔任陆廖姚方金邱夏谭韦贾邹石熊孟秦阎薛侯雷白龙段郝孔邵史毛常万顾赖武康贺严尹钱施牛洪龚'''
    s_lastname = '''豪言玉意泽彦轩景正程诚宇澄安青泽轩旭恒思宇嘉宏皓成宇轩玮桦宇达韵磊泽博昌信彤逸柏新劲鸿文恩远翰圣哲家林景行律本乐康昊宇麦冬景武茂才军林茂飞昊明明天伦峰志辰亦'''
    t_lastname = '''佳彤自怡颖宸雅微羽馨思纾欣元凡晴玥宁佳蕾桑妍萱宛欣灵烟文柏艺以如雪璐言婷青安昕淑雅颖云艺忻梓江丽梦雪沁思羽羽雅访烟萱忆慧娅茹嘉幻辰妍雨蕊欣芸亦'''
    len_first = len(first_name)
    len_s = len(t_lastname)
    len_t = len(t_lastname)
    name = first_name[random.randrange(len_first)] + s_lastname[random.randrange(len_s)]
    print(name)
    return name
def is_zh_punctuation(w):
    punctuation_str = string.punctuation
    if w in punctuation_str:
        print(w)
        print(1)
        return True
def is_en(w):
    if 'a' <= w <= 'z' or 'A' <= w <= 'Z':
        print(1)
        print(len(string.punctuation))
        print(string.punctuation[31])
        return True

def is_en_punctuation(w):
    punctuation_str = string.punctuation
    if w in string.punctuation:
        print(1)
        return True











if __name__ == "__main__":
    chinese_name()


