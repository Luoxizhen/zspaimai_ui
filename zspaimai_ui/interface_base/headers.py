from common.readconfig import ini
from common.rwjson import rwjson

admin_headers = rwjson.get_header('admin_headers.json')
mini_headers = rwjson.get_header('user_headers_app.json')
base_url = ini.host


def get_user_headers():
    return rwjson.get_header('user_headers.json')
def get_user_headers_unlogin():
    return rwjson.get_header('user_headers_unlogin.json')
def update_token(token):
    dict = rwjson.get_header('user_headers.json')
    dict["token"] = token
    rwjson.set_header('user_headers.json', dict)