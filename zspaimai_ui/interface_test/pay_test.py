import logging
import time

import requests
import json
import pytest
from interface_base import user
import utils
from interface_base import finance
#@pytest.fixture(scope='module')
def test_001():
    '''用户登陆'''
    user.update_token()
def save_finance():
    '''验证获取用户的资金信息，并保存到finance.json 文件中，包含钱包余额，冻结金额，提现金额，额度，冻结额度'''
    financeinfo = finance.get_finance_info()
    utils.rwjson.RwJson().writejson("interface_data", "finance.json", financeinfo)


def get_financeinfo_pre():
    financeinfo_pre = utils.rwjson.RwJson().readjson("interface_data", "finance.json")
    return financeinfo_pre
def test_recharge_001():
    '''验证后台给用户充值成功'''
    status = finance.recharge()
    assert status == 200
def test_recharge_002():
    '''验证后台给用户充值后，用户的余额增加充值的金额'''
    financeinfo_pre = finance.get_finance_info()
    '后台充值'
    finance.recharge()
    financeinfo = finance.get_finance_info()
    assert float(financeinfo['normal_money']) == float(financeinfo_pre['normal_money'])+100.00
    assert float(financeinfo['normal_quota']) == float(financeinfo_pre['normal_quota']) + 100.00 * 50

def test_recharge_003():
    '''验证后台充值成功后，用户的额度增加  充值金额* 50'''
    financeinfo_pre = finance.get_finance_info()
    '后台充值'
    finance.recharge()
    financeinfo = finance.get_finance_info()
    assert float(financeinfo['normal_quota']) == float(financeinfo_pre['normal_quota']) + 100.00*50

def test_recharge_004():
    '''验证后台充值成功后，用户的钱包明细增加一条记录'''
    '保存用户的钱包明细'
    wallet_bill_pre = finance.get_wallet_bill()
    '后台充值'
    finance.recharge()
    wallet_bill = finance.get_wallet_bill()
    '验证明细增加一条记录'
    assert wallet_bill['total'] == wallet_bill_pre['total']+1
    '验证明细第一条记录内容'
    assert wallet_bill['first_record']['money']=="100.00"


def test_recharge_005():
    '''验证后台充值成功后，用户的额度明细增加一条记录'''
    quato_bill_pre = finance.get_quota_bill()
    '后台充值'
    finance.recharge()
    quato_bill = finance.get_quota_bill()
    '验证明细增加一条记录'
    assert quato_bill['total'] == quato_bill_pre['total']+1
    assert quato_bill['first_record']['quota']=="5000.00"

def test_change_quota_001():
    '''验证后台给用户充额度成功'''
    status = finance.change_quota()
    assert status == 200

def test_change_quota_002():
    '''验证后台给用户充额度，用户的额度明细增加所充额度'''
    '充额度前用户的额度'
    quota_pre = finance.get_finance_info()['normal_quota']
    '充额度'
    finance.change_quota()
    quota = finance.get_finance_info()['normal_quota']
    assert float(quota) == float(quota_pre) + 100

def test_change_quota_003():
    '''验证后台充额度，用户的可用余额不变'''
    nomarl_money_pre = finance.get_finance_info()['normal_money']
    '充额度'
    finance.change_quota()
    nomarl_money = finance.get_finance_info()['normal_money']
    assert nomarl_money == nomarl_money_pre


def test_change_quota_004():
    '''验证后台充额度，用户的额度明细增加一条记录'''
    quota_bill_pre = finance.get_quota_bill()
    finance.change_quota()
    quota_bill = finance.get_quota_bill()
    assert quota_bill['total'] == quota_bill_pre['total']+1
    assert quota_bill['first_record']['quota'] == '100.00'


def test_cashout_001():
    '''验证后台提现功能'''
    status = finance.cashout()
    assert status == 200
def test_cashout_002():
    '''验证后台提现后，用户的可用余额-提现金额'''
    normal_money_pre = finance.get_finance_info()['normal_money']
    '后台提现'
    finance.cashout()
    normal_money = finance.get_finance_info()['normal_money']
    assert float(normal_money) == float(normal_money_pre) - 100

def test_cashout_003():
    '''验证后台提现后，用户的钱包明细增加一条记录'''
    wallet_total_pre = finance.get_wallet_bill()['total']
    '后台提现'
    finance.cashout()
    wallet_bill_info = finance.get_wallet_bill()
    wallet_total = wallet_bill_info['total']
    assert wallet_total == wallet_total_pre + 1
    assert wallet_bill_info['first_record']['money'] == '100.00'
def test_cashout_004():
    '''验证后台提现后，用户的可用额度 - 提现金额*50'''
    quota_pre = finance.get_finance_info()['normal_quota']
    '后台提现'
    finance.cashout()
    quota = finance.get_finance_info()['normal_quota']
    assert float(quota) == float(quota_pre) - 50 *100.00
def test_cashout_005():
    '''验证后台提现后，用户的额度明细增加一条记录'''
    quota_total_pre = finance.get_quota_bill()['total']
    '后台提现'
    finance.cashout()
    quota_bill_info = finance.get_quota_bill()
    quota_total = quota_bill_info['total']
    assert quota_total == quota_total_pre + 1
    assert quota_bill_info['first_record']['quota'] == "5000.00"
def test_cashout_user_001():
    '''验证用户提现成功'''
    cashout_result = finance.cashout_user2()
    status = cashout_result['status']
    if (status == 400):
        msg = cashout_result['msg']
        if (msg =="您还有未支付的拍品，暂不能提现"):
            finance.recharge()
    cashout_result = finance.cashout_user2()
    status = cashout_result['status']


    assert status == 200
def test_cashout_user_002():
    '''验证用户申请提现后，用户的可用额度-申请提现额度'''
    normal_money_pre = finance.get_finance_info()['normal_money']
    finance.cashout_user2()
    normal_money = finance.get_finance_info()['normal_money']
    assert float(normal_money) == float(normal_money_pre)-100

def test_cashout_user_003():
    '''验证用户申请提现后，用户的冻结额度 + 申请提现额度'''
    frozen_money_pre = finance.get_finance_info()['frozen_money']
    finance.cashout_user2()
    frozen_money = finance.get_finance_info()['frozen_money']
    assert float(frozen_money) == float(frozen_money_pre) + 100
def test_cashout_user_004():
    '''验证用户申请提现后，用户的可用额度 - 提现金额*50'''
    normal_quota_pre = finance.get_finance_info()['normal_quota']
    finance.cashout_user2()
    normal_quota = finance.get_finance_info()['normal_quota']
    assert float(normal_quota) == float(normal_quota_pre) - 50 * 100

def test_cashout_user_005():
    '''验证用户申请提现后，钱包明细增加一条记录'''
    wallet_total_pre = finance.get_wallet_bill()['total']
    finance.cashout_user2()
    wallet_bill_info = finance.get_wallet_bill()
    wallet_total = wallet_bill_info['total']
    assert wallet_total == wallet_total_pre + 1

def test_cashout_user_006():
    '''验证用户申请提现后，钱包明细第一条记录的金额 = 提现金额'''
    finance.cashout_user2()
    wallet_bill_info = finance.get_wallet_bill()
    money = wallet_bill_info['first_record']['money']
    assert money == '100.00'
def test_cashout_user_007():
    '''验证用户申请提现后，钱包明细第一条记录的状态为：进行中'''
    finance.cashout_user2()
    wallet_bill_info = finance.get_wallet_bill()
    status = wallet_bill_info['first_record']['status']
    assert status == 30
def test_cashout_u_008():
    '''验证用户申请提现后，额度明细增加一条记录'''
    wallet_total_pre = finance.get_quota_bill()['total']
    finance.cashout_user2()
    wallet_total = finance.get_quota_bill()['total']
    assert wallet_total == wallet_total_pre + 1

def test_cashout_deal_001():
    '''验证后台确认提现后，可用金额与申请提现后一致'''
    finance.cashout_user2()
    normal_money_pre = finance.get_finance_info()['normal_money']
    finance.cashout_deal()
    normal_money = finance.get_finance_info()['normal_money']
    assert normal_money == normal_money_pre

def test_cashout_deal_002():
    '''验证后台确认提现后，冻结金额 = 申请提现后冻结金额-提现金额'''
    finance.cashout_user2()
    frozen_money_pre = finance.get_finance_info()['frozen_money']
    finance.cashout_deal()
    frozen_money = finance.get_finance_info()['frozen_money']
    assert float(frozen_money) == float(frozen_money_pre) - 100
def test_cashout_deal_003():
    '''验证后台确认提现后，可用额度 = 申请提现后可用额度'''
    finance.cashout_user2()
    normal_quota_pre = finance.get_finance_info()['normal_quota']
    finance.cashout_deal()
    normal_quota = finance.get_finance_info()['normal_quota']
    assert normal_quota == normal_quota_pre

def test_cashout_deal_004():
    '''验证后台确认提现后，用户的钱包明细总数与申请提现后钱包明细总数一致'''
    finance.cashout_user2()
    total_pre = finance.get_wallet_bill()['total']
    finance.cashout_deal()
    total = finance.get_wallet_bill()['total']
    assert total == total_pre
def test_cashout_deal_005():
    '''验证后台确认提现后，用户的钱包明细，相应的记录状态由进行中更改为成功'''
    finance.cashout_user2()
    finance.cashout_deal()
    wallet_info = finance.get_wallet_bill()
    status = wallet_info['first_record']['status']
    assert status == 10

def test_cashout_deal_006():
    '''验证后台确认提现后，用户的额度明细总数与申请提现后一致'''
    finance.cashout_user2()
    total_pre = finance.get_quota_bill()['total']
    finance.cashout_deal()
    total = finance.get_quota_bill()['total']
    assert total == total_pre
def test_cashout_refuse_001():
    '''验证后台拒绝提现后，用户的可用金额= 申请提现后可用金额+提现金额'''
    finance.cashout_user2()
    normal_money_pre = finance.get_finance_info()['normal_money']
    finance.cashout_refuse()
    normal_money = finance.get_finance_info()['normal_money']
    assert float(normal_money) == float(normal_money_pre)+100
def test_cashout_refuse_002():
    '''验证后台拒绝提现后，冻结金额 = 申请提现后冻结金额-提现金额'''
    finance.cashout_user2()
    frozen_money_pre = finance.get_finance_info()['frozen_money']
    finance.cashout_refuse()
    frozen_money = finance.get_finance_info()['frozen_money']
    assert float(frozen_money) == float(frozen_money_pre) - 100


def test_cashout_refuse_003():
    '''验证后台拒绝提现后，可用额度 = 申请提现后可用额度 + 提现金额 *50'''
    finance.cashout_user2()
    normal_quota_pre = finance.get_finance_info()['normal_quota']
    time.sleep(2)
    finance.cashout_refuse()
    normal_quota = finance.get_finance_info()['normal_quota']
    assert float(normal_quota) == float(normal_quota_pre) + 50 * 100



def test_cashout_refuse_004():
    '''验证后台拒绝提现后，用户的钱包明细总数与申请提现后钱包明细总数一致'''
    finance.cashout_user2()
    total_pre = finance.get_wallet_bill()['total']
    finance.cashout_refuse()
    total = finance.get_wallet_bill()['total']
    assert total == total_pre


def test_cashout_refuse_005():
    '''验证后台拒绝提现后，用户的钱包明细，相应的记录状态由进行中更改为失败'''
    finance.cashout_user2()
    time.sleep(2)
    finance.cashout_refuse()
    wallet_info = finance.get_wallet_bill()
    status = wallet_info['first_record']['status']
    assert status == 20


def test_cashout_refuse_006():
    '''验证后台确认提现后，用户的额度明细总数=申请提现后额度明细总数+1'''
    finance.cashout_user2()
    total_pre = finance.get_quota_bill()['total']
    finance.cashout_refuse()
    total = finance.get_quota_bill()['total']
    assert total == total_pre + 1
