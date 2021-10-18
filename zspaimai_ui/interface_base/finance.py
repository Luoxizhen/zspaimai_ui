import requests
from utils import rwjson
import os
import logging
import interface_base.interface_base as if_base
base_url = "http://api.online.zspaimai.cn"
def create_filename():
    curpath = os.path.dirname(os.path.realpath(__file__))
    parpath = os.path.dirname(curpath)

    filename = os.path.join(parpath, 'log', 'my.log')
    return filename

filename = create_filename()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s  %(filename)s  %(levelname)s  %(message)s', datefmt='%a%d%b%Y  %H:%M:%S', filename=filename, filemode='a')

#
# def get_user_headers():
#     return rwjson.RwJson().readjson('interface_data', 'user_headers.json')
# def get_admin_headers():
#     return rwjson.RwJson().readjson('interface_data', 'admin_headers.json')
user_headers = if_base.get_user_headers()
admin_headers = if_base.get_admin_headers()
def get_finance_info():
    '''获取用户的可用金额，冻结金额，可用额度，冻结额度'''
    url = base_url + '/user/user/index?from=pc'
    headers = user_headers
    r = requests.request('get', url=url, headers=headers)
    print(r.json())
    normal_money = r.json()['data']['info']['wallet']['normal_money']
    frozen_money = r.json()['data']['info']['wallet']['frozen_money']
    normal_quota = r.json()['data']['info']['quota']['normal_quota']
    frozen_quota = r.json()['data']['info']['quota']['frozen_quota']
    out_money = r.json()['data']['info']['wallet']['out_money']
    user_finance_info = {'normal_money': normal_money,
                       'frozen_money': frozen_money,
                       'out_money': out_money,
                       'normal_quota': normal_quota,
                       'frozen_quota': frozen_quota}

    return user_finance_info
def get_wallet_bill():
    '''获取钱包明细，总条数，及最新的一条记录'''
    url = base_url +'/user/wallet/bill'
    headers = user_headers
    data = {'page': '1',
            'type': '0',
            'from': 'pc'}

    r = requests.request('get', url=url, params=data, headers=headers)
    total = r.json()['data']['total']
    status = r.json()['status']
    first_record = r.json()['data']['data'][0]
    wallet_bill_info = {'total': total,
                        'status': status,
                        'first_record': first_record}
    return wallet_bill_info


def get_quota_bill():
    '''获取额度明细，总条数，及最新的一条记录'''
    url = base_url +'/user/wallet/quota'
    headers = user_headers
    data = {'page': '1',
            'type': '0',
            'from': 'pc'}
    r = requests.request('get', url=url, params=data, headers=headers)
    total = r.json()['data']['total']
    status = r.json()['status']
    first_record = r.json()['data']['data'][0]
    '''{"quota":"10.00","operation_type":1,"msg":"余额支付","create_time":"2021-07-23 09:55:13"}'''
    quota_bill_info = {'total': total,
                        'status': status,
                        'first_record': first_record}
    
    return quota_bill_info

def recharge():
    '''后台给用户充值'''
    url = base_url + '/admin/wallet/recharge'
    print(url)
    headers = admin_headers
    json = {'money': '100',
            'user_id': 102}
    r = requests.request('post', url=url, json=json, headers=headers)
    '''返回充值状态'''
    print(r.json())
    logging.info("后台充值")
    return r.json()['status']

def change_quota():
    '''后台给用户充额度'''
    url = base_url + '/admin/wallet/change_quota'
    headers = admin_headers
    json = {'quota': '100',
            'user_id': 102,
            'msg': ''}
    r = requests.request('post', url=url, json=json, headers=headers)
    '''充值状态'''
    return r.json()['status']

def remittance():
    ''' pc 端用户充值 '''
    url = base_url + '/user/bank/remittance'
    headers = user_headers
    data = {'from': 'pc'}
    data1 = {'from': 'mini'}
    data2 = {'from': 'android'}
    data3 = {'from': 'ios'}
    json = {'bank_name': '中国工商银行',
            'collection_info': "中晟在线(广州) 信息技术有限公司",
            'link_id': "1054",
            'money': "1000",
            'remittance_info': "充值",
            'remitter': "大罗",
            'remitter_date': "2021-7-23",
            'remitter_no': "工行",
            'remitter_type': "5",
            'table': "2"
            }
    r = requests.request('get', url=url, params=data, headers=headers, json=json)

    status = r.json()['status']
    first_record = r.json()['data']['data'][0]
    '''{"quota":"10.00","operation_type":1,"msg":"余额支付","create_time":"2021-07-23 09:55:13"}'''

    return status
def remittance_finish():
    '''后台确认充值'''
    url = base_url + '/admin/remittance/finish'
    headers = admin_headers
    json = {'id': 164,
            'remarks': ""}
    r = requests.request('post', url=url, json=json, headers=headers)
    '''充值状态'''
    status = r.json()['status']
def remittance_auditfailed():
    '''后台拒绝银行划账'''
    url = base_url + '/admin/remittance/audit_failed'
    headers = admin_headers
    json = {'id': 164}
    r = requests.request('post', url=url, json=json, headers=headers)
    '''充值状态'''
    status = r.json()['status']
    return status
def cashout():
    '''后台提现'''
    url = base_url + '/admin/wallet/cashout'
    headers = admin_headers
    json = {
        "user_id": 102,
        "money": "100",
        "remarks": ""
    }
    r = requests.request('post', url=url, json=json, headers=headers)
    status = r.json()['status']
    return status
def cashout_user1():
    '''用户提现前获取绑定的银行卡信息'''
    url = base_url + "/user/wallet/bank_info?from=pc"
    json = {"is_charge": 1,
            "from": "pc"}
    r = requests.request('post', url=url, json=json, headers=user_headers)
    print(r.json())
    return r.json()['data']['id']
def cashout_user2():
    '''用户申请提现'''
    url = base_url + "/user/wallet/cashout"
    bank_id = cashout_user1()
    json = {"pay_rwd": "246810",
            "bank_id": bank_id,
            "money": "100"}
    r = requests.request('post', url=url, json=json, headers=user_headers)
    return r.json()


def cashout_list():
    '''后台获取提现记录'''
    url = base_url + '/admin/wallet/cashout_list'
    json = {"page": 1,
            "userno": "192902",
            "end_time": "",
            "start_time": "",
            "status": "30"}
    r = requests.request('post', url=url, json=json, headers=admin_headers)
    id = r.json()['data']['data'][0]['id']
    return id
def cashout_deal():
    '''后台确认提现'''
    url = base_url + '/admin/wallet/cashout_deal'
    id = cashout_list()
    json = {'id': id,
            'pay_money': '100'}
    r = requests.request('post', url=url, json=json, headers=admin_headers)
    return r.json()['status']
def cashout_refuse():
    '''后台拒绝提现'''
    url = base_url + '/admin/wallet/cashout_refuse'
    id = cashout_list()
    json = {'id': id}
    r = requests.request('post', url=url, json=json, headers=admin_headers)
    return r.json()['status']


