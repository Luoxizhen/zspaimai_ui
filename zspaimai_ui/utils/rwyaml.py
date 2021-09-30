import yaml
import os
curpath = os.path.dirname(os.path.realpath(__file__))
parpath = os.path.dirname(curpath)
def yaml_file_path(parname,filename):
    yaml_path = os.path.join(parpath, parname, filename)
    return yaml_path
def get_yaml_data(parname,filename):
    # 打开yaml 文件
    yaml_file = yaml_file_path(parname, filename)
    fs = open(yaml_file, encoding="UTF-8")
    file_data = fs.read()
    fs.close()
    data = yaml.safe_load(file_data)
    return data
def generate_yaml_doc(parname,filename,data):
    yaml_file = yaml_file_path(parname, filename)
    file = open(yaml_file, 'a', encoding='UTF-8')
    yaml.dump(data, file)
    file.close()