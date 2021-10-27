import configparser
import os
import yaml






class ReadCfg():
    def __init__(self):
        curpath = os.path.dirname(os.path.realpath(__file__))
        cfgpath = os.path.join(curpath, "cfg.ini")
        yaml_file = os.path.join(curpath, "config.yml")
        self.conf = configparser.ConfigParser()
        self.conf.read(cfgpath, encoding="utf-8")
        self.yaml_file = yaml_file
    def readCfg(self):

        return self.conf.get('sys_variables', 'url')
    def get_base_url(self):
        return self.conf.get('sys_variables', 'base_url')
    def get_yaml_data(self):
        # 打开yaml 文件
        print('***获取yaml文件数据***')
        curpath = os.path.dirname(os.path.realpath(__file__))
        yaml_file = os.path.join(curpath, "config.yml")
        fs = open(yaml_file, encoding="UTF-8")


        datas = yaml.load(fs, Loader=yaml.FullLoader)

        print(datas)
        print(type(datas))

        # file = open(yaml_file, 'r', encoding='utf-8')
        # file_data = file.read()
        # file.close()
        # print(file_data)
    def get_yaml_data_1(self, yaml_file):
        #打开ymal 文件
        print('***获取yaml 文件数据***')
        file = open(yaml_file, 'r', encoding='utf-8')
        file_data = file.read()
        file.close()
        print(file_data)
        print('类型', type(file_data))
        print('***转化yaml 数据为字典或列表***')
        data = yaml.safe_load(file_data)
        print(data)
        print('类型', type(data))
        d = data
        print(d['union'])
        print(type(d['union']))
        print(d['union']['user1'])
    def get_yaml_load_all(self,yaml_file):
        # 打开ymal 文件
        print('***获取yaml 文件数据***')
        file = open(yaml_file, 'r', encoding='utf-8')
        file_data = file.read()
        file.close()
        all_data = yaml.load_all(file_data, Loader=yaml.FullLoader)
        for data in all_data:
            print('data___', data)

    def generate_yaml_doc(self, yaml_file):
        py_ob = {"school": "zhang",
                 "students": ['a', 'b']}
        file = open(yaml_file, 'a', encoding='utf-8')
        yaml.dump(py_ob, file)
        file.close()



if __name__ == '__main__':
    conf = ReadCfg()
    #conf.get_yaml_data()
    #conf.get_yaml_data_1(conf.yaml_file)
    conf.get_yaml_load_all(conf.yaml_file)
    conf.generate_yaml_doc(conf.yaml_file)