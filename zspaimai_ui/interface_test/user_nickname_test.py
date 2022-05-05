import json

from interface_base import user
import csv
import codecs
from config.conf import cm
import os
from utils import util




def test_set_nickname():
    with open("/Users/yuanyuanhe/Desktop/nickname.csv","r",encoding="gbk") as f:
        csv_reader = csv.reader(f)

        for line in csv_reader:
            user_info = line
            user_phone = user_info[0]
            user_pp = {"phone":user_phone,"pwd":"zs011015"}
            r = user.login(**user_pp)

            token = r.json()['data']['token']

            user.update_token(token)

            nicknames = user.nickname_list().json()['data']
            nicknames_id = []
            for nickname in nicknames:
                nicknames_id.append(nickname["id"])
            print(nicknames_id)
            for i in range(len(nicknames_id)):
                nickname = user_info[i+1]
                nickname_info = {"nickname":nickname,"id":nicknames_id[i]}
                r = user.nickname_edit(**nickname_info)

                print(r)
                json.load()
    assert 1==2





