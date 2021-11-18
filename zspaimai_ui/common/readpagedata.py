import yaml
from config.conf import cm
import os
class Pagedata:
    def __init__(self, name):
        self.file_name = "%s.yml" % name
        self.file_path = os.path.join(cm.WEB_DATA_PATH, self.file_name)
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("%s 文件不存在" % self.file_path )
        with open(self.file_path, encoding='utf-8') as f:
            file_data = f.read()
            f.close()
            self.all_yaml.load_all(file_data)

    def get_data(self):
        for data in self.all_data:
            print(data)




if __name__ == '__main__':
    Pagedata('firstp').get_data()
