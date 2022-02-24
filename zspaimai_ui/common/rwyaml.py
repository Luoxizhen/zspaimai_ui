import yaml
import os
from config.conf import cm
class Rwyaml():
    def __init__(self):
        self.web_data_path = cm.WEB_DATA_PATH
        self.interface_data_path =cm.INTERFACE_DATA_PATH
    def get_data(self,f,dir='web'):

        if dir != 'web':
            yaml_file = os.path.join(self.interface_data_path, f)
        else:
            yaml_file = os.path.join(self.web_data_path, f)
        load_f = open(yaml_file,mode='r',encoding='utf-8')
        file_data = load_f.read()
        load_f.close()
        return yaml.safe_load(file_data)

    def set_data (self,f,data,dir='web'):
        if dir != 'web':
            yaml_file = os.path.join(self.interface_data_path, f)
        else:
            yaml_file = os.path.join(self.web_data_path, f)

        file = open(yaml_file, 'a', encoding='UTF-8')
        yaml.dump(data, file)
        file.close()




