import requests
import urllib3
def get_class_of_paper(class_id):
    urllib3.disable_warnings()
    url = "https://www.pmg.cn/Class/"+class_id
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

    }
    r = requests.request('get', url=url, verify=False)
    if r.status_code == 200:
        #print(r.text)
        return r.text
    else:
        return None

def get_detail(c_id):
    urllib3.disable_warnings()
    url = "https://www.pmg.cn/api/pmg/show_info/"+c_id
    r = requests.request('get',url=url,verify=False)
    if r.status_code == 200:
        # print(r.json())
        return r.json()
    else:
        return None
if __name__ == "__main__":
    get_detail("265")