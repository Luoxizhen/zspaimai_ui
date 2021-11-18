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
    if args != []:
        for i in range(len(args)):
            if type(args[i]) == dict:
                temp = json.dumps(args[i])
            elif type(args[i]) == int:
                temp = str(args[i])
            else:
                temp = args[i]
            if i != len(args) - 1:

                s1 = s1 + temp + ","
            else:
                s1 = s1 + temp + "]"
    return s1






