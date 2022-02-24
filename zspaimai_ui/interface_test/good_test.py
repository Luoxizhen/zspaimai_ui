from interface_base import goods

from utils import times

import csv
def serach_goods(**file_p):
    good_infos = [] # 拍品信息 :id + 拍品编号
    good_ids = [] #拍品id
    goods_infos =[] #拍品总信息
    with open(file_p["file_1"], mode="r", encoding='gbk') as f:
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


def serach_goods_info(**file_p):
    good_infos = [] # 拍品信息 :id + 拍品编号
    good_ids = [] #拍品id
    goods_infos =[] #拍品总信息
    with open(file_p["file_1"], mode="r", encoding='gbk') as f:
        reader = csv.reader(f)
        for i in reader:
            good_ids.append(i[1])
    for i in good_ids:
        if i != 0:
            info_id = {"id":i}
            print(info_id)
            goods_info = goods.goods_info(**info_id).json()["data"] # 获取拍品信息
            print(goods_info)
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



        with open(file_p["file_2"], mode="w", encoding='utf-8') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(("id","good_name","category_id","images","original_image","content","shape","retain_price","seller_name","buyer_service_rate")) # 保存列名
        with open(file_p["file_2"], mode="a", encoding='utf-8') as f:
            csv_write = csv.writer(f)
            csv_write.writerows(goods_infos) # 保存拍品信息



def goods_add_history(file_path,*retain,**topic_info):
    '''从csv 文件中导入拍品，csv 文件中的拍品数据为系统上已经拍卖过的数据'''

    f = open(file_path, mode="r", encoding='gbk')

    reader = csv.DictReader(f)


    k = 1
    list_of_retain = retain # 需要设置保留价的拍品在csv 文件中的排序
    for row in reader:


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
def test_search_good():
    file_1 = "/Users/yuanyuanhe/Desktop/货/拍品.csv"
    file_2 = "/Users/yuanyuanhe/Desktop/货/待上传的拍品表_有历史数据.csv"
    file_path = {"file_1":file_1,"file_2":file_2}
    serach_goods(**file_path)
    assert 1==2

def test_goods_add_history():
    file_path = "/Users/yuanyuanhe/Desktop/货/待上传的拍品表_有历史数据.csv"
    topic_info = {}
    begin_time = times.str_to_time("2022-02-25 10:00:00")  # 开拍时间 ： 与专场开拍时间相同
    end_time = times.str_to_time("2022-02-28 20:00:00")  # 结拍时间： 与专场结拍时间相同
    topic_info["begin_time"] = begin_time
    topic_info["end_time"] = end_time
    topic_info["agreement_no"] = "a20220203"
    topic_info["topic_id"] = "[42]"
    list_of_retain=[9,10,12,15,16]
    goods_add_history(file_path,*list_of_retain,**topic_info)
