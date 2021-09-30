from utils import rwjson
def get_user_headers():
    return rwjson.RwJson().readjson('interface_data', 'user_headers.json')
def get_admin_headers():
    return rwjson.RwJson().readjson('interface_data', 'admin_headers.json')


