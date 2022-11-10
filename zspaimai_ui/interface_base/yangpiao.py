import requests
import urllib3


def get_bid_history_data(p,nid,rid):
    # url = "https://yangpiao.com/Users/getBidHistoryData?page=5&_t=1655284669029&certPick=&certCo=&dealTimeStr=&specimen=&nId=64&rId=2"
    url = "https://yangpiao.com/Users/getBidHistoryData"
    headers = {

        "cookie":"_ypuuid=df68dfa143c1c93eeb396687e3023e84",
        "cookie":"Hm_lpvt_6ce79aaf03f417b904b3b0bf01ba5e87=1667788907",
        "cookie":"Hm_lvt_6ce79aaf03f417b904b3b0bf01ba5e87=1666926682,1667198544,1667439672,1667669516",
        "cookie": "__51cke__=",
        "cookie": "__51laig__=3",
        "cookie": "__51uvsct__JHpoW8doII8bLRu4=25",
        "cookie": "__51vcke__JHpoW8doII8bLRu4=d79e9d01-12af-50ce-a622-4105f0296241",
        "cookie": "__51vuft__JHpoW8doII8bLRu4=1664935601706",
        "cookie": "__tins__21009109=%7B%22sid%22%3A%201667788905621%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201667790705621%7D",
        "cookie": "__vtins__JHpoW8doII8bLRu4=%7B%22sid%22%3A%20%22f16fedf9-a5b7-585e-8a03-46c5c583d350%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201667790705627%2C%20%22ct%22%3A%201667788905627%7D",
        "cookie": "__51huid__JUuPhOpewd2I2ft5=62ac5621-f367-5a64-b55d-c79cc8b17c99",


        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q = 0.9",
        "access-token": "1baf41a36e330fb1c7f297ec27acc02a88835bb5",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    data={
        "page": p,
        "certPick": "",
        "certCo": "",
        "dealTimeStr": "",
        "specimen": "",
        "nId": nid,
        "rId": rid,
        "dealTimeStr": "15days"
    }
    urllib3.disable_warnings()
    r = requests.request('get', url=url, params=data, headers=headers,verify=False)
    # print(r.json())
    return r

if __name__ == "__main__":
    get_bid_history_data(1,2,1)
