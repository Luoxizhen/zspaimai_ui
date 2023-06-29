import json

from interface_base import goods
from common import rwjson
from utils import times,util,rwyaml
from config.conf import cm
from requests import request
import csv


def get_goods_bid(good_id_start,num,p,all=0):
    '''获取拍品的出价信息
    good_id_start: 第一个拍品的id
    num: 拍品的数量
    p: 拍品信息输出路径'''
    goods_bid_info = []

    for i in range(num):
        good_id = good_id_start + i
        r = goods.goods_bid(good_id).json()
        good_id_json = {"id": good_id}
        good_name = goods.goods_info(**good_id_json).json()["data"]["name"]

        if(r['data']['total'] > 0):
            if all == 0:  # 只记录最新一笔
                good_bid_info = r['data']['data'][0]
                good_bid_info['id'] = good_id
                good_bid_info["name"] =good_name
                goods_bid_info.append(good_bid_info)
            else:
                for j in range(r['data']['total']):

                    if j < 10:
                        good_bid_info = r['data']['data'][j]
                        good_bid_info['id'] = good_id
                        good_bid_info["name"] = good_name
                        if good_bid_info["user_id"] in range(572,587) and j == 0:
                            good_bid_info["user_id"] ="顶价:" + str(good_bid_info["user_id"])
                        if j > 0:
                            if good_bid_info["user_id"] not in range(572,586):
                                goods_bid_info.append(good_bid_info)
                        else :
                            goods_bid_info.append(good_bid_info)


    with open(p,'w') as f:
        fileheader = ["id","name","user_id","now_price", "agent_price",  "status"]
        csv_dict_writer = csv.DictWriter(f,fileheader)
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(goods_bid_info)



def test_get_goods_bid():
    '''测试 get_goods_bid(good_id_start,num,p) 函数'''
    goods_info = rwyaml.get_yaml_data('interface_data','good_config.yml')['goods_bid']
    good_id = goods_info['good_id'] # 2346 2462
    num = goods_info['num'] #65 19
    file_path = goods_info['file_path']
    get_goods_bid(good_id,num,file_path,all=1)
    assert 1==2

def good_add_new(file_path,is_edit=0,good_type=1,**topic_info):
    '''从csv 文件中导入新拍品
    file_path: 拍品信息.csv 存储位置
    good_type: 商品类型,type=2 为商品，type =1 为拍品
    topic_info : 拍品的基本信息，包括拍卖开始时间，结束时间，所属专场，合同号'''
    f = open(file_path, mode="r", encoding='utf-8')
    reader = csv.DictReader(f)
    k = 1
    w_shape = ["裸币", "裸票", "原票"]
    for row in reader:

        good_info = {}
        print(row['category_id'])

        if int(row['category_id']) in [7,8,9,10,13,36,40,41,42,43]:
            c_name = row["category"] + row['name'] + row['count'] # 第一、二、三、四版币的名称 = 版别+名字+数量
        else:
            c_name = row['name'] + row['count'] #其余 = 名字+ 数量
        if not row['grade'] in w_shape:
            s_name = '('+ row['num'].replace("‘",'').replace("'","")+ " "+row['grade']+row['score'] +')' #评级币的编号 = （编号+评级+分数）
            good_info["shape"] = "评级币" #评级币的品相 = 评级币
        else:
            s_name = '('+ row['num']+ " "+row['score'] + ')' #非评级币的编号 = （编号+ 品相）
            if row["grade"] == "原票":
                good_info["grade"] = "原票"
            else:
                good_info["shape"] = row['grade'] #非评级币的品相 = 所估算的品质

        good_info["name"] ="lot"+ str(k) + "-" + c_name + s_name #名称的字符长度不能超过60
        if "/" in row["date"]:
            img_1 = "picture/" + row['date'] + "-1.jpg"
        else:
            img_1 = "picture/" + row['date'] + "/" + row['good_no'] + "-1.jpg"
            # img_1 = "picture/" + row['date'] + "/" + row['good_no'].replace('a', '') + "-1.jpg"
        img = [img_1]
        for i in range(2,int(row['p_1'])+1):
            img.append(img_1.replace("-1.jpg","-"+str(i)+".jpg"))
        o_img = [x.replace("picture/", "thumbnail/") for x in img]
        good_info["images"] = json.dumps(o_img[:int(row['p_2'])])#缩列图
        good_info["original_image"] = json.dumps(img[:int(row['p_2'])])  #原图
        name_s = """<p class="ql-align-center"><strong>"""
        name_e = """</strong></p><p class="ql-align-center"><br></p>"""
        p_s = """<p class="ql-align-center">"""
        p_e = """</p>"""
        img_s = '<img src="'
        img_e = '">'
        comm_s = """<p class="ql-align-left">"""
        comm_e = """</p>"""
        picture_url_base = "https://online-1303141635.cos.ap-guangzhou.myqcloud.com/"  #图片的基本地址
        picture_url = [picture_url_base + x for x in img]
        picture_str = ''
        for i in range(int(row['p_1'])):
            picture_str = picture_str + img_s + picture_url[i] + img_e
        if row["sub_comment"] == " ": #拍品没有备注信息时，拍品的描述为拍品的名字 + 图片
            good_info["content"] = name_s + good_info["name"] + name_e + p_s + picture_str + p_e
        else: # 拍品信息有备注信息时，拍品的描述包括拍品的备注信息
            good_info["content"] = name_s + good_info["name"] + name_e + comm_s + row["sub_comment"].replace("\n","</p><p>") + comm_e + p_s + picture_str + p_e

        good_info["price"] = row['price']
        good_info["retain_price"] = row["retain_price"] # 保留价
        good_info["seller_name"] = row["seller_name"]
        good_info["delay_time"] = 60  # 延拍时间
        good_info["goods_weight"] = 0
        good_info["begin_time"] = topic_info["begin_time"]
        good_info["end_time"] = topic_info["end_time"] + 30 * (k - 1)  # 30 ，单位为s ，按照该专场多长时间节拍一个进行计算
        good_info["agreement_no"] = row["agreement_no"]
        good_info["topic_id"] = topic_info['topic_id'] # 拍品所属专场
        good_info["category_id"] = row["category_id"] #拍品类目
        good_info["buyer_service_rate"] = row["buyer_service_rate"]
        meta_str = "{\"min_price\":\"\",\"max_price\":\"\",\"seller_insure_deal\":\"0\",\"seller_insure_no_deal\":\"0\",\"service_fee_deal\":\"3\",\"service_fee_no_deal\":\"0\",\"production_fee_deal\":\"0\",\"production_fee_no_deal\":\"0\",\"safekeeping_fee_deal\":\"0\",\"safekeeping_fee_no_deal\":\"0\",\"seller_taxes\":\"\",\"identify_fee\":\"\",\"packing_fee\":\"\",\"texture\":\"\",\"spec\":\"\",\"opinion\":\"\"}"
        meta_json = json.loads(meta_str)
        meta_json["service_fee_deal"] = row["service_fee_deal"]
        good_info["meta"] = json.dumps(meta_json)
        if is_edit == 0:  #新增
            if good_type == 1: #新增拍品
                r = goods.goods_add(**good_info)
                print(r.json())
            else:# 新增商品
                good_info["type"] = 2
                good_info["delay_time"] = 0
                good_info["inventory"] = "1"
                good_info["inventory_unit"] = "枚"
                del(good_info["topic_id"])
                r = goods.goods_add(**good_info)
                print(r.json())

        else: #拍品或商品编辑
            good_info["id"] = row["good_id"]
            good_info["type"] = good_type
            good_info_json = {"id": row["good_id"]}
            good_info_old = goods.goods_info(**good_info_json).json()['data']
            good_info["begin_time"] = good_info_old["begin_time"]
            good_info["end_time"] = good_info_old["end_time"]
            r = goods.goods_edit(**good_info)
            print(r.json())
        k = k + 1



def test_good_add_new():
    goods_info = rwyaml.get_yaml_data('interface_data', 'good_config.yml')['good_add_new']
    file_path = goods_info['file_path']
    begin_time_s = goods_info['begin_time']
    end_time_s = goods_info['end_time']
    tipic_id = goods_info['topic_id']
    good_type = goods_info["good_type"]
    is_edit = goods_info["is_edit"]
    topic_info = {}
    begin_time = times.str_to_time(begin_time_s)  # 开拍时间 ：2022-05-27 10:00:00 2022-06-10 10:00
    end_time = times.str_to_time(end_time_s)  # 结拍时间：2022-07-01 10:00:00
    topic_info["begin_time"] = begin_time
    topic_info["end_time"] = end_time
    topic_info["agreement_no"] = ""
    topic_info["topic_id"] = tipic_id
    good_add_new(file_path, is_edit=is_edit,good_type=good_type,**topic_info)
    assert 1 == 2





def get_picture(file1,file2):
    '''将拍品的图片下载到文件夹中
    file1： 拍品导入文档
    file2: 图片保存位置'''
    with open(file1, mode="r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        s_date = []
        for row in reader:
            if "/" in row["date"]:
                img_1 = "picture/" + row['date'] + "-1.jpg"
            else:
                img_1 = "picture/" + row['date'] + "/" + row['good_no'] + "-1.jpg"
                if row["date"] not in s_date:
                    s_date.append(row["date"])
            img = [img_1]
            for i in range(2, int(row['p_1']) + 1):
                img.append(img_1.replace("-1.jpg", "-" + str(i) + ".jpg"))
            picture_url_base = rwyaml.get_yaml_data('interface_data', 'good_config.yml')['get_picture']['base_url'] # 图片的基本地址
            picture_url = [picture_url_base + x for x in img] # 图片地址
            for i in range(len(picture_url)):
                r = request("get",picture_url[i])
                with open(file2+img_1[i].replace("picture/"," ").replace("/",""),'wb') as p_f:
                    p_f.write(r.content)




def test_get_picture():
    file_r = rwyaml.get_yaml_data('interface_data', 'good_config.yml')['get_picture']['file_r']
    file_d = rwyaml.get_yaml_data('interface_data', 'good_config.yml')['get_picture']['file_d']
    get_picture(file_d,file_r)
