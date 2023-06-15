import requests
import urllib3
from  utils.rwjson import getjson


def get_bid_history_data(p,nid,rid,t="30days"):
    # url = "https://yangpiao.com/Users/getBidHistoryData?page=5&_t=1655284669029&certPick=&certCo=&dealTimeStr=&specimen=&nId=64&rId=2"
    url = "https://yangpiao.com/Users/getBidHistoryData"

    headers = getjson.readjson('interface_data','yangpiao_header.json')

    data={
        "page": p,
        "certPick": "",
        "certCo": "",
        "specimen": "",
        "nId": nid,
        "rId": rid,
        "dealTimeStr": t
    }
    urllib3.disable_warnings()
    r = requests.request('get', url=url, params=data, headers=headers,verify=False)
    # print(r.json())
    return r

if __name__ == "__main__":
    get_bid_history_data(1, 84, 4)
