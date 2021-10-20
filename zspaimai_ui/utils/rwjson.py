'''https://www.cnblogs.com/bigberg/p/6430095.html'''

'''JSON在python中分别由list和dict组成。

这是用于序列化的两个模块：

json: 用于字符串和python数据类型间进行转换
pickle： 用于python特有的类型和python的数据类型间进行转换
Json模块提供了四个功能：dumps、dump、loads、load

pickle模块提供了四个功能：dumps、dump、loads、load

json dumps把数据类型转换成字符串 dump把数据类型转换成字符串并存储在文件中  loads把字符串转换成数据类型  load把文件打开从字符串转换成数据类型'''

'''json写入文本'''
import json
import os
class RwJson():
    def __init__(self):
        curpath = os.path.dirname(os.path.realpath(__file__))
        print(curpath)
        parpath = os.path.dirname(curpath)
        print(parpath)
        self.curpath = curpath
        self.parpath = parpath




    def readjson(self, parname, filename):
        jsonpath = os.path.join(self.parpath, parname, filename)
        with open(jsonpath, 'r') as load_f:
            load_dict = json.load(load_f)
            return load_dict

    def writejson(self, parname, filename, dict):
        jsonpath = os.path.join(self.parpath, parname, filename)
        with open(jsonpath, 'w') as dump_f:
            json.dump(dict, dump_f, indent=True, ensure_ascii=False)


