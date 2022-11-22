import requests
import urllib3
from  utils.rwjson import getjson


def get_bid_history_data(p,nid,rid):
    # url = "https://yangpiao.com/Users/getBidHistoryData?page=5&_t=1655284669029&certPick=&certCo=&dealTimeStr=&specimen=&nId=64&rId=2"
    url = "https://yangpiao.com/Users/getBidHistoryData"
    headers = {

        "cookie":"_ypuuid=42795deaa7998a6786ffbf7e2ae25859",
        "cookie":"Hm_lpvt_6ce79aaf03f417b904b3b0bf01ba5e87=1669012163",
        "cookie":"Hm_lvt_6ce79aaf03f417b904b3b0bf01ba5e87=1668570780,1668849689,1668914668,1669012163",
        "cookie": "__51cke__=",
        "cookie": "__51laig__=1",
        "cookie": "__51uvsct__JHpoW8doII8bLRu4=42",
        "cookie": "__51vcke__JHpoW8doII8bLRu4=d79e9d01-12af-50ce-a622-4105f0296241",
        "cookie": "__51vuft__JHpoW8doII8bLRu4=1664935601706",
        "cookie": "__tins__21009109=%7B%22sid%22%3A%201668390919974%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201668392725475%7D",
        "cookie": "__vtins__JHpoW8doII8bLRu4=%7B%22sid%22%3A%20%225f23605f-394f-5485-ad71-2205d835cd36%22%2C%20%22vd%22%3A%202%2C%20%22stt%22%3A%205497%2C%20%22dr%22%3A%205497%2C%20%22expires%22%3A%201668392725478%2C%20%22ct%22%3A%201668390925478%7D",
        "cookie": "__51uvsct__JHpoW8doII8bLRu4=42",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q = 0.9",
        "access-token": "a04799ecb96d588dded043192a73b99c22bd7e8c",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    headers = getjson.readjson('interface_data','yangpiao_header.json')

    data={
        "page": p,
        "certPick": "",
        "certCo": "",
        "specimen": "",
        "nId": nid,
        "rId": rid,
        "dealTimeStr": "15days"
    }
    urllib3.disable_warnings()
    r = requests.request('get', url=url, params=data, headers=headers,verify=False)
    print(r.json())
    return r

if __name__ == "__main__":
    get_bid_history_data(1, 1, 1)
