import json

from interface_base import goods
from interface_base.user import user_login
import pytest
import time
from utils import times
from utils import util
from utils.rwjson import RwJson
import random
import csv

def goods_add():
    begin_time = round(time.time())+120
    end_time = begin_time + 600
    # a = time.strptime('2021-11-2 14:20:00', '%Y-%m-%d %H:%M:%S')
    # b = time.strptime('2021-11-2 14:23:00', '%Y-%m-%d %H:%M:%S')
    # begin_time = time.mktime(a)
    # end_time = time.mktime(b)
    name = '订阅信息验证-6'
    good_info = {"name": name, "begin_time": int(begin_time), "end_time": int(end_time),"price":32000}
    r = goods.goods_add(**good_info)
    return r.json()['data']

def test_goods_add_001():
    begin_time = round(time.time())
    end_time = begin_time + 80000
    good_infos = {"begin_time": begin_time, "end_time": end_time, "name": "优惠劵测试专用", "price": 20000}
    #good_infos={"type":2,"inventory":"1000","inventory_unit":"套","category_id":9,"platform":"1","begin_time":0,"end_time":0,"top_price":"","name":"第三套人民币7 枚1-2","delay_time":0,"shape":"100","price":"100","retain_price":"","seller_name":"","agreement_no":"","create_user":"","create_date":"","content":"<p>第三套人民币小全套7枚一枚(同分 PMG68E)</p>","original_image":"[\"picture/hPRswrxWWys8wDG7DzRK47GN4b33RK.jpeg\"]","images":"[\"thumbnail/aRFBN6MXYbrsrmF2KHKNZx8ZdATwRC.jpeg\"]","freight_id":51,"is_freight":0,"goods_weight":"","buyer_service_rate":"10","meta":"{\"min_price\":\"\",\"max_price\":\"\",\"seller_insure_deal\":\"1\",\"seller_insure_no_deal\":\"1\",\"service_fee_deal\":\"2\",\"service_fee_no_deal\":\"1\",\"production_fee_deal\":\"15\",\"production_fee_no_deal\":\"15\",\"safekeeping_fee_deal\":\"0\",\"safekeeping_fee_no_deal\":\"0\",\"seller_taxes\":\"\",\"identify_fee\":\"\",\"packing_fee\":\"\",\"texture\":\"\",\"spec\":\"\",\"opinion\":\"\"}"}
    r = goods.goods_add(**good_infos)
    print(r.json())

    assert r.json()['status']==20

def test_goods_list():
    r = goods.goods_list()
    assert r['status'] == 200
def test_goods_list_001():
    goods_info = {"status": 31}
    r = goods.goods_list(**goods_info)
    assert r.json()['data']['status'] == 200
def serach_goods(**file_p):
    good_infos = [] # 拍品信息 :id + 拍品编号
    good_ids = [] #拍品id
    goods_infos =[] #拍品总信息
    with open(file_p["file_1"], mode="r", encoding='utf-8') as f:
        reader = csv.reader(f)

        for i in reader:
            print(i[0])
            info = {"name":i[0]}# 新修改
            print(info)
            r = goods.goods_list(**info)
            print(r.json())
            if r.json()['status']==200 and r.json()["data"]["total"] > 0:# 如果搜索到拍品，保存第一个拍品到id
                good_id=r.json()['data']['data'][0]['id']#提取拍品id
            else:
                good_id = 0 # 如果搜索到拍品，保存id =0
            good_ids.append(good_id)  # 拍品列表保存 good_id
            good_infos.append((i[0], good_id))

    with open(file_p["file_1"], mode="w", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(good_infos) # 写入拍品信息
def serach_goods1(**file_p):
    good_infos = [] # 拍品信息 :id + 拍品编号
    good_ids = [] #拍品id
    goods_infos =[] #拍品总信息
    with open(file_p["file_1"], mode="r", encoding='utf-8') as f:
        reader = csv.reader(f)

        for i in reader:
            info = {"name":i[0]}# 新修改
            r = goods.goods_list(**info)
            if r.json()['status']==200 and r.json()["data"]["total"] > 0:# 如果搜索到拍品，保存第一个拍品到id
                good_id=r.json()['data']['data'][0]['id']#提取拍品id
            else:
                good_id = 0 # 如果搜索到拍品，保存id =0
            good_ids.append(good_id)  # 拍品列表保存 good_id
            good_infos.append((i[0], good_id))

    with open(file_p["file_1"], mode="w", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(good_infos) # 写入拍品信息



    for i in good_ids:
        if i != 0:
            info_id = {"id":i}
            goods_info = goods.goods_info(**info_id).json()["data"] # 获取拍品信息

            good_name = goods_info["name"] #拍品名称
            if good_name.find("lot") == 0:
                index_of_s = good_name.find("-") + 1
                good_name = good_name[index_of_s:]
            simple_desc=goods_info["simple_desc"] #拍品描述
            seller_name=goods_info["seller_name"] #销售人
            agreement_no =goods_info["agreement_no"] #拍品合同编号
            shape = goods_info["shape"] #拍品品相
            type =goods_info["type"]
            inventory =goods_info["inventory"]
            inventory_unit =goods_info["inventory_unit"]
            images =goods_info["images"] #缩略图
            original_image = goods_info["original_image"] #原图
            retain_price =goods_info["retain_price"] #保留价
            buyer_service_rate =goods_info["buyer_service_rate"] #买家服务费率
            content =goods_info["content"] #拍品信息描述
            if content.find("lot") != -1:
                content_num_1 = content.find("strong")
                content_num_2 = content.find("-", content_num_1)
                content = content[:content_num_1 + 7:] + content[content_num_2 + 1:]
            freight_id =goods_info["freight_id"]
            goods_weight =goods_info["goods_weight"]
            category_id = goods_info["category_id"] #拍品类别
            # 拍品信息列表
            good_info = (i,good_name,category_id,images,original_image,content,shape,retain_price,seller_name,buyer_service_rate)
            goods_infos.append(good_info)
        else:
            good_info = (0,"","","","","","","","","") # 增加未有上传的拍品，以和
            goods_infos.append(good_info)


        with open(file_p["file_2"], mode="w", encoding='gbk') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(("id","good_name","category_id","images","original_image","content","shape","retain_price","seller_name","buyer_service_rate")) # 保存列名
        with open(file_p["file_2"], mode="a", encoding='gbk') as f:
            csv_write = csv.writer(f)
            csv_write.writerows(goods_infos) # 保存拍品信息

def test_search_good():
    file_1 = "/Users/yuanyuanhe/Desktop/货/2月1.csv"
    file_2 = "/Users/yuanyuanhe/Desktop/货/待上传的拍品表_有历史数据_20220210.csv"
    file_path = {"file_1":file_1,"file_2":file_2}
    serach_goods(**file_path)
    assert 1==2
def test_goods_list_0004():
    good_name ="lot889-第二套人民币红5元票样一枚(123-08033 PMG55)"
    good_num = good_name.find("_") + 1
    print(good_num)
    good_name = good_name[good_num::]
    assert good_name == "第二套人民币红5元票样一枚(123-08033 PMG55)"

def test_goods_add_history():
    '''从csv 文件中导入拍品，csv 文件中的拍品数据为系统上已经拍卖过的数据'''
    begin_time = times.str_to_time("2022-01-28 11:00:00") #开拍时间 ： 与专场开拍时间相同
    end_time = times.str_to_time("2022-02-10 20:00:00") #结拍时间： 与专场结拍时间相同
    f = open("/Users/yuanyuanhe/Desktop/货/待上传的拍品表_有历史数据.csv", mode="r", encoding='gbk')

    reader = csv.reader(f)
    k = 0
    list_of_retain = [1,2,3,20,32,35,44,45,53,54] # 需要设置保留价的拍品在csv 文件中的排序
    for i in reader:

        good_info ={}
        good_info["name"]=i[0]
        good_info["content"]=i[1]
        good_info["simple_desc"] =i[2]
        good_info["images"] = util.list_to_str(util.str_to_list(i[3]))

        good_info["original_image"] = util.list_to_str(util.str_to_list(i[4]))
        good_info["price"] =1
        if k in list_of_retain:
            good_info["retain_price"]=i[6]
        good_info["shape"]=i[5]
        good_info["seller_name"]=i[7]
        good_info["delay_time"] = 60 #延拍时间
        good_info["goods_weight"] = 0
        good_info["begin_time"] = begin_time
        good_info["end_time"] = end_time + 30 * k # 30 ，单位为s ，按照该专场多长时间节拍一个进行计算
        good_info["agreement_no"] = "t20220128" # 合同编号，格式按照 a+年+月+该专场在本月的排序，如果2022年1月份第一个专场 则设置为 a20220101
        good_info["topic_id"] = "[39]" #拍品所属id
        if good_info["name"].find("第一") != -1:
            good_info["buyer_service_rate"] = "10"
            good_info["category_id"] = 7
        elif good_info["name"].find("第二") != -1:
            good_info["buyer_service_rate"] = "8"
            good_info["category_id"] = 8
        elif good_info["name"].find("第三") != -1:
            good_info["buyer_service_rate"] = "8"
            good_info["category_id"] = 9
        elif good_info["name"].find("第四") != -1:
            good_info["buyer_service_rate"] = "5"
            good_info["category_id"] = 10
        else:
            good_info["buyer_service_rate"] = i[8]
            good_info["category_id"] = i[9]

        r = goods.goods_add(**good_info)
        k = k + 1


def goods_add_history(file_path,*retain,**topic_info):
    '''从csv 文件中导入拍品，csv 文件中的拍品数据为系统上已经拍卖过的数据'''

    f = open(file_path, mode="r", encoding='gbk')

    reader = csv.DictReader(f)


    k = 1
    list_of_retain = retain # 需要设置保留价的拍品在csv 文件中的排序
    for row in reader:


# '''
        good_info ={}
        good_info["name"]=row["good_name"]
        good_info["content"]=row["content"]

        # good_info["images"] = util.list_to_str(util.str_to_list(row["images"]))
        good_info["images"] = row["images"].replace("'",'\"')
        # good_info["original_image"] = util.list_to_str(util.str_to_list(row["original_image"]))
        good_info["original_image"]=row["original_image"].replace("'",'\"')
        good_info["price"] = 1
        if k in list_of_retain:
            good_info["retain_price"]=row["retain_price"]
        good_info["shape"]=row["shape"]
        good_info["seller_name"]=row["seller_name"]
        good_info["delay_time"] = 0 #延拍时间
        good_info["goods_weight"] = 0
        good_info["begin_time"] = topic_info["begin_time"]
        good_info["end_time"] = topic_info["end_time"]  + 30 * (k-1) # 30 ，单位为s ，按照该专场多长时间节拍一个进行计算
        good_info["agreement_no"] = topic_info["agreement_no"] # 合同编号，格式按照 a+年+月+该专场在本月的排序，如果2022年1月份第一个专场 则设置为 a20220101
        good_info["topic_id"] = topic_info["topic_id"]  #拍品所属id
        if good_info["name"].find("第一") != -1:
            good_info["buyer_service_rate"] = "10"
            good_info["category_id"] = 7
        elif good_info["name"].find("第二") != -1:
            good_info["buyer_service_rate"] = "8"
            good_info["category_id"] = 8
        elif good_info["name"].find("第三") != -1:
            good_info["buyer_service_rate"] = "8"
            good_info["category_id"] = 9
        elif good_info["name"].find("第四") != -1:
            good_info["buyer_service_rate"] = "5"
            good_info["category_id"] = 10
        else:
            good_info["buyer_service_rate"] = row["buyer_service_rate"]
            good_info["category_id"] = row["category_id"]

        r = goods.goods_add(**good_info)
        k = k + 1
# '''
def test_goods_add_history_1():
    file_path = "/Users/yuanyuanhe/Desktop/货/待上传的拍品表_有历史数据_20220210.csv"
    topic_info = {}
    begin_time = times.str_to_time("2022-02-11 10:00:00")  # 开拍时间 ： 与专场开拍时间相同
    end_time = times.str_to_time("2022-02-16 20:00:00")  # 结拍时间： 与专场结拍时间相同
    topic_info["begin_time"] = begin_time
    topic_info["end_time"] = end_time
    topic_info["agreement_no"] = "a20220201"
    topic_info["topic_id"] = "[203]"
    list_of_retain=[1,2,3,4,5,20,21,39,40,41,46,47]
    goods_add_history(file_path,*list_of_retain,**topic_info)















def test_0002():
    print("开始")
    with open("/Users/yuanyuanhe/Desktop/货/预选品.csv", mode="r", encoding='gbk') as f:
        reader = csv.reader(f)
        print(type(reader))
        for i in reader:
            print(i[0])
            print(type(i))
    assert 1==2
def test_batch_shelves():
    goods_ids = []
    goods_info = {"status": 31, "is_shelves": 1}
    r = goods.goods_list(**goods_info).json()
    total = r['data']['total']
    per_page = r['data']['per_page']
    last_page = r['data']['last_page']
    for i in range(2):
        if last_page > 1 and i < last_page - 1:
            page_total = 10
        else:
            page_total = total - per_page * (last_page - 1)
        for j in range(page_total):
            goods_id = goods.goods_list(page=i, **goods_info).json()['data']['data'][j]['id']
            goods_ids.append(goods_id)
    goods_ids_str =str(goods_ids)
    batch_info = {"goods_ids": goods_ids_str, "is_shelves":0}
    print (batch_info)
    goods.batch_shelves(**batch_info)
    # goods.del_goods()
    assert 1 == 2
def test_batch_shelves_1():
    for k in range(9):
        goods_ids = []
        goods_info = {"status": 31, "is_shelves": 1}
        r = goods.goods_list(**goods_info).json()
        for i in range(10):
            goods_id = r['data']['data'][i]['id']
            goods_ids.append(goods_id)

        batch_info = {"goods_ids": str(goods_ids), "is_shelves": 0}
        # print(batch_info)
        goods.batch_shelves(**batch_info)
def test_goods_del():
    for k in range(109):
        goods_ids = []
        goods_info = {"status": 31, "is_shelves": 0,"top":0, "type":1, "is_recommended":0}
        r = goods.goods_list(**goods_info).json()
        for i in range(10):
            goods_id = r['data']['data'][i]['id']
            goods_ids.append(goods_id)
        batch_info = {"ids": str(goods_ids)}
        goods.del_goods(**batch_info)
def test_goods_recommended_del():
    '''将流拍的拍品取消推荐、取消置顶后删除'''
    goods_info = {"status": 31, "is_shelves":0, "type":1}
    r = goods.goods_list(**goods_info).json()
    goods_ids = []

    for i in range(r['data']['total']):
        good_id = r['data']['data'][i]['id']
        goods_ids.append(good_id)
        if r['data']['data'][i]["is_recommended"] == 1:
            act_info = {"id": good_id, "act": "is_recommended", "is_recommended": 0}
            goods.goods_edit_action(**act_info)
        if r['data']['data'][i]["top"] == 1:
            act_info = {"id": good_id, "act": "top", "value": 0}
            goods.goods_edit_action(**act_info)
    goods_info = {"ids": str(goods_ids)}
    goods.del_goods(**goods_info)
def test_goods_delete():
    '''将拍品管理列表中的拍品删除到剩下5页'''
    r = goods.goods_list().json()
    last_page = r['data']['last_page']
    per_page = r['data']['per_page']
    del_page = last_page-6
    for i in range(del_page):
        r = goods.goods_list(page=6).json()
        goods_ids = []
        for j in range(per_page):
            good_id = r['data']['data'][j]['id']
            goods_ids.append(good_id)
            if r['data']['data'][j]["is_recommended"] == 1:
                act_info = {"id": good_id, "act": "is_recommended", "value": 0} #取消推荐
                goods.goods_edit_action(**act_info)
            if r['data']['data'][j]["top"] == 1:
                act_info = {"id": good_id, "act": "top", "value": 0}#取消置顶
                goods.goods_edit_action(**act_info)
            if r['data']['data'][j]["is_shelves"] == 1:
                act_info = {"id": good_id,"is_shelves":0}#下架
                goods.goods_edit_shelves(**act_info)
        goods_info = {"ids": str(goods_ids)}
        print(goods_info)
        goods.del_goods(**goods_info) # 删除该页的所有拍品
def goods_unrecommend():
    '''将所有首页推荐的拍品取消推荐'''
    goods_info = {"is_recommended": 1}
    goods_recommend_list = util.list_nums(goods.goods_list,'id',**goods_info)
    print(goods_recommend_list)
    for i in range(len(goods_recommend_list)):
        act_info = {"id": goods_recommend_list[i], "act": "is_recommended", "value": 0}
        print(act_info)
        goods.goods_edit_action(**act_info)
def test_goods_unrecommend():
    goods_unrecommend()
    assert 1==2
def goods_recommend():
    '''将最新的拍品首页推荐,执行该函数前先将所有的推荐的拍品取消推荐'''
    # for k in range(1,3):
    r = goods.goods_list().json()['data']['data']
    for i in range(8):
        good_id = r[i]['id']
        act_info = {"id": good_id, "act": "is_recommended", "value": 1}  # 推荐
        goods.goods_edit_action(**act_info)
def goods_add_recommend(**good_info):
    '''添加一个拍品，并首页推荐'''
    #goods_unrecommend()
    # a = time.strptime('2021-11-9 10:05:00', '%Y-%m-%d %H:%M:%S')
    # b = time.strptime('2021-11-9 10:10:00', '%Y-%m-%d %H:%M:%S')
    # begin_time = time.mktime(a)
    # end_time = time.mktime(b)
    # begin_time = round(time.time())
    # end_time = begin_time + 3600
    # name = '小林工'
    # #lot844-第四套人民币90年50元一枚(麒麟号JQ777777777 PMG66E)
    # good_info = {"name": name, "begin_time": int(begin_time), "end_time": int(end_time), "price":32000}
    good_id = goods.goods_add(**good_info).json()['data']

    act_info = {"id": good_id, "act": "is_recommended", "value": 1}  # 推荐
    goods.goods_edit_action(**act_info)
    return good_id



def test_unrecommend():
    goods_unrecommend()

def test_recommend():
    goods_recommend()
def test_goods_add_recommend():
    begin_time = round(time.time())
    end_time = begin_time + 3600
    name = '小林工'
    #lot844-第四套人民币90年50元一枚(麒麟号JQ777777777 PMG66E)
    good_info = {"name": name, "begin_time": int(begin_time), "end_time": int(end_time), "price":32000}
    goods_add_recommend(**good_info)
def test_good_edit():
    info = {"name": "拍品6", "retain_price": "100"}
    good_edit(2799, **info)


def good_edit(good_id,**good_info):
    act_info = {"id": good_id, "is_shelves": 0}
    goods.goods_edit_shelves(**act_info)  # 拍品下架
    good_info_json = {"id": good_id}
    goods_json = goods.goods_info(**good_info_json).json()['data']

    begin_time = round(time.time()) + 60
    end_time = begin_time + 360
    topic_id = "[" + str(goods_json['topic_id'][0]) + "]"
    images = "[" + '"' + goods_json['images'][0] + '"' + "]"
    original_image = "[" + '"' + goods_json['original_image'][0] + '"' + "]"
    print(topic_id, original_image, images)
    goods_json['begin_time'] = begin_time
    goods_json['end_time'] = end_time
    goods_json['topic_id'] = topic_id
    goods_json['images'] = images
    goods_json['original_image'] = original_image
    for key in good_info:
        if key in goods_json.keys():
            goods_json[key] = good_info[key]

    r = goods.goods_edit(**goods_json)
    print(r.json())
    act_info["is_shelves"] = 1
    # goods.goods_edit_shelves(**act_info) #拍品上架
    act_info = {"id": good_id, "act": "status", "value": 20}
    goods.goods_edit_action(**act_info)
def goods_edit():
    '''对第一个流拍对拍品下架，重新编辑，上架'''
    search_info = {"status": 31}
    good_id = goods.goods_list(**search_info).json()['data']['data'][0]['id']
    print(good_id)
    act_info = {"id": good_id, "is_shelves": 0}
    goods.goods_edit_shelves(**act_info) #拍品下架
    good_info_json = {"id": good_id}
    goods_json = goods.goods_info(**good_info_json).json()['data']

    begin_time = round(time.time())+60
    end_time = begin_time + 360
    topic_id = "[" +str(goods_json['topic_id'][0]) + "]"
    images = "["+'"'+goods_json['images'][0] +'"'+"]"
    original_image = "["+'"'+goods_json['original_image'][0] +'"'+"]"
    print(topic_id,original_image,images)
    goods_json['begin_time'] = begin_time
    goods_json['end_time'] = end_time
    goods_json['topic_id'] = topic_id
    goods_json['images'] = images
    goods_json['original_image'] = original_image
    r = goods.goods_edit(**goods_json)
    print(r.json())
    act_info["is_shelves"] = 1
    #goods.goods_edit_shelves(**act_info) #拍品上架
    act_info = {"id":good_id,"act":"status","value":20}
    goods.goods_edit_action(**act_info)

def test_goods_edit():
    goods_edit()


def test_list():
    r = goods.list()
    print(r.json())
    assert 1==2
def test_detail():
    r = goods.detail()
    print(r.json())
    assert 1==2

def test_add():
    r = goods.add()
    print(r.json())
    assert 1==2


def test_cart_add():
    '''将商品添加到购物车中'''
    list = goods.list().json()
    total = list['data']['list']['total']
    per_page = list['data']['list']['per_page']
    last_page = list['data']['list']['last_page']
    for page in range(1,last_page+1):
        if last_page > 1 and page < last_page:
            page_num = per_page
        else:
            page_num = total - per_page * (last_page-1)
        list_info = {"page": page}

        goods_list = goods.list(**list_info).json()['data']["list"]['data']
        for i in range(page_num):
            id = goods_list[i]['id']
            goods_inventory = goods.detail(id).json()['data']["info"]["inventory"]
            if goods_inventory > 0:
                print(goods.add(id).json())



def test_bid_good():
    header = RwJson().readjson('interface_data', 'user_headers_app.json')
    for i in range(10):
        name = "lot838-第三套人民币5元炼钢一枚(20-90318553 PMG67E)" + str(i)
        begin_time = round(time.time())
        end_time = begin_time + 60
        price = random.randint(1,1000)
        good_info ={"name":name, "price":price, 'begin_time':begin_time, "end_time":end_time}
        good_id = goods.goods_add(**good_info).json()['data']
        print(good_id)
        time.sleep(4)
        bid_price = price*2
        bid_info = {"goods_id": good_id,
            "price": bid_price}


        print(goods.bidding(header=header, **bid_info))




def test_delay():
    for i in (1,10):
        name = "新延拍验证-" + str(i) + "分钟"
        a = time.strptime('2021-11-16 12:02:00', '%Y-%m-%d %H:%M:%S')
        b = time.strptime('2021-11-16 12:10:00', '%Y-%m-%d %H:%M:%S')
        begin_time = time.mktime(a)
        end_time = time.mktime(b)
        delay_time = i * 60
        price = 10
        goods_info = {"name":name,"begin_time":begin_time,"end_time":end_time,"price":price,"delay_time":delay_time}
        good_id = goods.goods_add(**goods_info).json()['data']
        act_info = {"id": good_id, "act": "is_recommended", "value": 1}  # 推荐
        goods.goods_edit_action(**act_info)


def user_bid(**info):
    user_info = info['user_info']
    bid_info = info['bid_info']
    if user_info != {}:
        user_login(**user_info)

    goods.bidding(**bid_info)




