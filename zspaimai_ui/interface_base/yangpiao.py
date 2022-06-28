import requests
def get_bid_history_data(p,nid,rid):
    # url = "https://yangpiao.com/Users/getBidHistoryData?page=5&_t=1655284669029&certPick=&certCo=&dealTimeStr=&specimen=&nId=64&rId=2"
    url = "https://yangpiao.com/Users/getBidHistoryData"
    headers = {

    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh - CN, zh;q = 0.9",
    "access-token": "2d60c9e0f7c651930bc479819ae81fb6c4081a4e",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    data={
        "page": p,
        "certPick": "",
        "certCo": "",
        "dealTimeStr": "",
        "specimen": "",
        "nId": nid,
        "rId": rid
    }
    r = requests.request('get', url=url, params=data, headers=headers)
    return r

