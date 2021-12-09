import yaml
from config.conf import cm
import os
from utils import times
class Pagedata:
    def __init__(self, name):
        self.file_name = "%s.yml" % name
        self.file_path = os.path.join(cm.WEB_DATA_PATH, self.file_name)

        if not os.path.exists(self.file_path):
            raise FileNotFoundError("%s 文件不存在" % self.file_path )
        with open(self.file_path, encoding='utf-8') as f:
            file_data = f.read()
            f.close()
            self.data = yaml.load(file_data)

    def __getitem__(self, item):
        data = self.data.get(item)
        if data:
            return data
        raise ArithmeticError("{}中不存在关键字：{}".format(self.file_name, item))

    def setitem(self, key, value):
        self.data[key] = value
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, stream=f)
            f.close()
    def setitem_c(self, key, child, value):
        self.data[key][child] = value
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, stream=f, allow_unicode=True)
            f.close()

if __name__ == '__main__':
    time1 = round(times.timestamp())
    p = Pagedata('firstp')
    print(p.data)
    good1 = p['good1']
    good1['begin_time'] = time1
    p.setitem('good1', good1)








