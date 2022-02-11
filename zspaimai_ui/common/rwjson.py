import json
from config.conf import cm
from common.readconfig import ini
import os
class Rwjson():
    def __init__(self):
        self.header_path = cm.INTERFACE_HEADER_PATH_ONLINE
        if ini.env == "offline":
            self.header_path = cm.INTERFACE_HEADER_PATH_OFFLINE
        self.interface_data_path = cm.INTERFACE_DATA_PATH
    def _get(self,f):
        with open(f,'r') as load_f:
            load_dict = json.load(load_f)
        return load_dict
    def _set(self,f,dict):
        with open(f,'w') as dump_f:
            json.dump(dict, dump_f, indent=True, ensure_ascii=False)
    def get_header(self,f):
        header_full_path = os.path.join(self.header_path,f)
        return self._get(header_full_path)
    def set_header(self,f):
        full_path = os.path.join(self.header_path, f)
        with open(full_path, 'w') as dump_f:
            json.dump(dict, dump_f, indent=True, ensure_ascii=False)
    def get_json(self,f):
        full_path = os.path.join(self.interface_data_path,f)
        return self._get(full_path)
    def set_json(self,f,dict):
        full_path = os.path.join(self.interface_data_path,f)
        with open(full_path,'w') as dump_f:
            json.dump(dict, dump_f, indent=True, ensure_ascii=False)

rwjson = Rwjson()

if __name__ == "__main__":
    print(rwjson.get_header('admin_headers.json'))