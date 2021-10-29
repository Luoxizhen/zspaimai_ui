import time, json
from utils import rwjson, utils
from interface_base.user import update_token, get_user_headers,base_url,admin_headers
def add():
    url = base_url + "/admin/topic/add"
    info = {"title":"订阅信息测试","begin_time":1635502200,"end_time":1635502800,"sort":"100","images":"picture/QCFNhmCJJ6fNijxWYQJFkixSYx6Mkm.png","small_images":"picture/RjNDKXXknaJF7W5hKCnYY4WEJjBe7P.png","content":"","mini_small_images":"picture/Kp5ykpFpT5CRXpspQfzpfj5MQ87DFy.png","mini_images":"picture/hhMMwMBFHwfcGZjeJZYKEE4fCAk8Z8.png"}