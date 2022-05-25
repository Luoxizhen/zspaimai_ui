import json
import random
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
    l = []
    n = str_image.count(",") +1
    for i in range(n):

        end = str_image.find(",")-1
        image = str_image[2:end]
        l.append(image)
        str_image = "[" + str_image[end+3:]

    return l



def list_to_str(list_image):
    '''用于添加拍品的接口，将images. original_images 的图片字符串转换为list
    输入

        ["picture/2021-09-27/537-1.jpg","picture/2021-09-27/537-2.jpg"]
    输出
    "[\"picture/2021-12-23/1075-1.jpg\", \"picture/2021-12-23/1075-2.jpg\"]"

         '''
    s = "["
    for i in range(len(list_image)):
        s = s + '"'+list_image[i]+'"'+','
    s = s.removesuffix(",") + "]"
    print(s)
    return s












if __name__ == "__main__":
    img_s ="['picture/2022-01-13/1183-1.jpg', 'picture/2022-01-13/1183-2.jpg']"
    list_to_str(str_to_list(img_s))


