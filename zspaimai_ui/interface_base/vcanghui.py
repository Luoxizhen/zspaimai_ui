import requests
import urllib3
from utils.rwjson import getjson
from utils import rwyaml


def get_bid_history_data(p):
    # url = "https://yangpiao.com/Users/getBidHistoryData?page=5&_t=1655284669029&certPick=&certCo=&dealTimeStr=&specimen=&nId=64&rId=2"
    url = rwyaml.get_yaml_data("interface_data", "html_url.yml")["vcanghui"]["url"]
    headers = {
        "cookie": "PHPSESSID=d8t5vp1p1ko4q3v2fhrlsr1fo2",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-cn",
        "access-token": "a04799ecb96d588dded043192a73b99c22bd7e8c",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A404MicroMessenger/8.0.29(0x18001d38) NetType/WIFI Language/zh_CN miniProgram/wx4e32b82cd82a7749",
    }
    # headers = getjson.readjson('interface_data','yangpiao_header.json')

    data={
        "page": p,
        "sousuo": "",
        "ban": "",
        "score": "",
        "money_value": "",
        "picks": "",
        "xing": 0
    }
    '''
    "page": p,
        "sousuo": 搜索词 %E9%BB%84%E4%B8%80%E8%A7%92,
        "ban": "版本",
        "score": "评级分数",
        "money_value": "面值，一分为1 ，一百为 10000",
        "picks": "纸币的唯一编号",
        "xing": 是否带🌟，是为1，否为0
    
    '''
    urllib3.disable_warnings()
    r = requests.request('get', url=url, params=data, headers=headers,verify=False)
    # print(r.text)
    return r.text

if __name__ == "__main__":
    get_bid_history_data(1)