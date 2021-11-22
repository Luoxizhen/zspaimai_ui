import json
import random
def kwargs_to_str(**kwargs):
    ls = []
    s = "["
    for key in kwargs:
        js = {"key": key, "value": kwargs[key]}
        ls.append(js)
    for i in range(len(ls)):
        if i != len(ls) - 1:
            s = s + json.dumps(ls[i]) + ","
        else:
            s = s + json.dumps(ls[i]) + "]"
    return s

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
    per_page = r['per_page']
    total = r['total']
    for i in range(1,last_page+1):
        r = fun(page=i, **list_info).json()['data']['data']
        for i in range(len(r)):
            list.append(r[i][key])

    return list



