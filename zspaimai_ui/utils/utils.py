import json
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

