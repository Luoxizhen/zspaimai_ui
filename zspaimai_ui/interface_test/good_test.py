import json

from interface_base import goods

from utils import times,util

import csv
def serach_goods(**file_p):
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


        with open(file_p["file_2"], mode="w", encoding='utf-8') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(("id","good_name","category_id","images","original_image","content","shape","retain_price","seller_name","buyer_service_rate")) # 保存列名
        with open(file_p["file_2"], mode="a", encoding='utf-8') as f:
            csv_write = csv.writer(f)
            csv_write.writerows(goods_infos) # 保存拍品信息


def serach_goods_info(**file_p):
    '''根据拍品id ，获取拍品的信息
    file_p : 文档路径，包括拍品id 存储文档，及拍品信息输出文档'''
    good_infos = [] # 拍品信息 :id + 拍品编号
    good_ids = [] #拍品id
    goods_infos =[] #拍品总信息
    with open(file_p["file_1"], mode="r", encoding='utf-8') as f:
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

    f = open(file_path, mode="r", encoding='utf-8')

    reader = csv.DictReader(f)


    k = 1
    list_of_retain = retain # 需要设置保留价的拍品在csv 文件中的排序
    for row in reader:
        print(row)


        good_info ={}
        good_info["name"]=row["good_name"]
        good_info["content"]=row["content"]

        # good_info["images"] = util.list_to_str(util.str_to_list(row["images"]))
        good_info["images"] = row["images"].replace("'",'\"')
        # good_info["original_image"] = util.list_to_str(util.str_to_list(row["original_image"]))
        good_info["original_image"]=row["original_image"].replace("'",'\"')
        good_info["price"] = row["price"]
        # if k in list_of_retain:
        #     good_info["retain_price"]=row["retain_price"]
        good_info["retain_price"] = row["retain_price"]
        good_info["shape"]=row["shape"]
        good_info["seller_name"]=row["seller_name"]
        good_info["delay_time"] = 60 #延拍时间
        good_info["goods_weight"] = 0
        good_info["begin_time"] = topic_info["begin_time"]
        good_info["end_time"] = topic_info["end_time"] + 30 * (k-1) # 30 ，单位为s ，按照该专场多长时间节拍一个进行计算
        good_info["agreement_no"] = row["agreement_no"]
        # good_info["agreement_no"] = topic_info["agreement_no"]
        # 合同编号，格式按照 a+年+月+该专场在本月的排序，如果2022年1月份第一个专场 则设置为 a20220101
        good_info["topic_id"] = topic_info["topic_id"]  #拍品所属id
        good_info["buyer_service_rate"]=row["buyer_service_rate"]
        # if good_info["name"].find("第一") != -1:
        #     good_info["buyer_service_rate"] = "10"
        #     good_info["category_id"] = 7
        # elif good_info["name"].find("第二") != -1:
        #     good_info["buyer_service_rate"] = "8"
        #     good_info["category_id"] = 8
        # elif good_info["name"].find("第三") != -1:
        #     good_info["buyer_service_rate"] = "8"
        #     good_info["category_id"] = 9
        # elif good_info["name"].find("第四") != -1:
        #     good_info["buyer_service_rate"] = "5"
        #     good_info["category_id"] = 10
        # else:
        #     good_info["buyer_service_rate"] = row["buyer_service_rate"]
        #     good_info["category_id"] = row["category_id"]

        r = goods.goods_add(**good_info)
        print(r.json())
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
    begin_time = times.str_to_time("2022-04-22 10:00:00")  # 开拍时间 ： 与专场开拍时间相同2022-04-15 10:00:00
    end_time = times.str_to_time("2022-04-25 20:09:00")  # 结拍时间： 与专场结拍时间相同2022-04-18 20:00:00
    topic_info["begin_time"] = begin_time
    topic_info["end_time"] = end_time
    topic_info["agreement_no"] = "a20220304"
    topic_info["topic_id"] = "[50]"
    list_of_retain=[]
    goods_add_history(file_path,*list_of_retain,**topic_info)
    assert 1==2
def goods_edit_begin_time():
    '''对下架对拍品编辑起拍时间'''

    good_info_json = {"id": 2124}
    goods_json = goods.goods_info(**good_info_json).json()['data']
    begin_time = times.str_to_time("2022-03-11 10:00:00")
    goods_json['begin_time'] = begin_time
    goods_json['original_image'] = json.dumps(goods_json['original_image'])
    goods_json['images'] = json.dumps(goods_json['images'])
    goods_json['topic_id'] = json.dumps(goods_json['topic_id'])
    goods_json['price'] = 1

    r = goods.goods_edit(**goods_json)

def test_goods_edit_begin_time():
    goods_edit_begin_time()
    assert 1==2
def get_goods_bid(good_id_start,num,p):
    '''获取拍品的出价信息
    good_id_start: 第一个拍品的id
    num: 拍品的数量
    p: 拍品信息输出路径'''
    goods_bid_info = []

    for i in range(num):
        good_id = good_id_start + i
        r = goods.goods_bid(good_id).json()
        if(r['data']['total'] > 0):



            good_bid_info = r['data']['data'][0]

            good_bid_info['id'] = good_id
            goods_bid_info.append(good_bid_info)

    with open(p,'w') as f:
        fileheader = ["id","now_price", "agent_price", "user_id", "status"]
        csv_dict_writer = csv.DictWriter(f,fileheader)
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(goods_bid_info)



def test_get_goods_bid():
    '''测试 get_goods_bid(good_id_start,num,p) 函数'''
    good_id = 2346 # 2346 2462
    num = 65 #65 19
    file_path = "/Users/yuanyuanhe/Desktop/货/拍品出价详情/5-1-1.csv"
    get_goods_bid(good_id,num,file_path)
    assert 1 ==2

def good_add_new(file_path,**topic_info):
    '''从csv 文件中导入新拍品
    file_path: 拍品信息.csv 存储位置
    topic_info : 拍品的基本信息，包括拍卖开始时间，结束时间，所属专场，合同号'''
    f = open(file_path, mode="r", encoding='utf-8')
    reader = csv.DictReader(f)
    k = 1
    for row in reader:
        print(row)
        good_info = {}
        # if row['category_id'] in [7,8,9,10] and '裸' not in row['grade']:
        #     # 属于第一套、第二套、第三套、第四套人民币的评级币的名称
        #     good_info["name"] = row["category"] + row['name'] + row['count'] + '('+ row['num']+ " "+row['grade']+row['score'] +')' #拍品名称
        # else:
        #     good_info["name"] = row['name'] + row['count'] + '(' + row['num'] + " " + row['grade'] + \
        #                         row['score'] + ')'  # 拍品名称
        if int(row['category_id']) in [7,8,9,10]:
            c_name = row["category"] + row['name'] + row['count'] # 第一、二、三、四版币的名称 = 版别+名字+数量
        else:
            c_name = row['name'] + row['count'] #其余 = 名字+ 数量
        if '裸' not in row['grade']:
            s_name = '('+ row['num']+ " "+row['grade']+row['score'] +')' #评级币的编号 = （编号+评级+分数）
            good_info["shape"] = "评级币"
        else:
            s_name = '('+ row['num']+ " "+row['score'] + ')' #非评级币的编号 = （编号+ 品相）
            good_info["shape"] = row['grade']

        good_info["name"] = c_name + s_name
        if "/" in row["date"]:
            img_1 = "picture/" + row['date'] + "-1.jpg"
        else:
            img_1 = "picture/" + row['date'] + "/" + row['good_no'] + "-1.jpg"
        img = [img_1]
        for i in range(2,int(row['p_1'])+1):
            img.append(img_1.replace("-1.jpg","-"+str(i)+".jpg"))

        # img_1 = "picture/" + row['date'] + "/" + row['no.'] + "-1.jpg"
        # img_2 = img_1.replace("-1.jpg","-2.jpg")
        # img = [img_1, img_2]
        # o_img = [img_1.replace("picture/", "thumbnail/"), img_2.replace("picture/", "thumbnail/")]
        o_img = [x.replace("picture/", "thumbnail/") for x in img]
        good_info["images"] = json.dumps(o_img[:int(row['p_2'])])#缩列图
        good_info["original_image"] = json.dumps(img[:int(row['p_2'])])  #原图
        name_s = """<p class="ql-align-center"><strong>"""
        name_e = """</strong></p><p class="ql-align-center"><br></p>"""
        p_s = """<p class="ql-align-center">"""
        p_e = """</p>"""
        img_s = '<img src="'
        img_e = '">'
        picture_url_base = "https://online-1303141635.cos.ap-guangzhou.myqcloud.com/"  #图片的基本地址
        picture_url = [picture_url_base +x for x in img]
        # [picture_url_base + img_1, picture_url_base + img_2]
        picture_str = ''
        for i in range(int(row['p_1'])):
            picture_str = picture_str + img_s + picture_url[i] + img_e
        # good_info["content"] = name_s + good_info["name"] + name_e + p_s + img_s + picture_url[0] + img_e + img_s + picture_url[1] + img_e + p_e
        good_info["content"] = name_s + good_info["name"] + name_e + p_s + picture_str + p_e
        print(good_info['content'])
        good_info["price"] = row['price']
        good_info["retain_price"] = row["retain_price"] # 保留价
        # if row['grade'] != "裸币" or "":
        #     good_info["shape"] = "评级币"
        # else:
        #     good_info["shape"] = "裸币"
        good_info["seller_name"] = row["seller_name"]
        good_info["delay_time"] = 60  # 延拍时间
        good_info["goods_weight"] = 0
        good_info["begin_time"] = topic_info["begin_time"]
        good_info["end_time"] = topic_info["end_time"] + 30 * (k - 1)  # 30 ，单位为s ，按照该专场多长时间节拍一个进行计算
        good_info["agreement_no"] = row["agreement_no"]
        # 合同编号，格式按照 a+年+月+该专场在本月的排序，如果2022年1月份第一个专场 则设置为 a20220101
        good_info["topic_id"] = topic_info['topic_id'] # 拍品所属专场
        good_info["category_id"] = row["category_id"] #拍品类目
        good_info["buyer_service_rate"] = row["buyer_service_rate"]
        r = goods.goods_add(**good_info)
        k = k + 1
def good_add_new_sp(file_path):
    '''从csv 文件中导入新商品
    file_path: 拍品信息.csv 存储位置
    topic_info : 拍品的基本信息，包括拍卖开始时间，结束时间，所属专场，合同号'''
    f = open(file_path, mode="r", encoding='utf-8')
    reader = csv.DictReader(f)
    k = 1
    for row in reader:
        # print(row)
        good_info = {}

        if int(row['category_id']) in [7,8,9,10]:
            c_name = row["category"] + row['name'] #+ row['count'] # 第一、二、三、四版币的名称 = 版别+名字+数量
        else:
            c_name = row['name'] #+ row['count'] #其余 = 名字+ 数量
        if '裸' not in row['grade']:
            s_name = '('+ row['num']+ " "+row['grade']+row['score'] +')' #评级币的编号 = （编号+评级+分数）
            good_info["shape"] = "评级币"
        else:
            s_name = '('+ row['num']+ " "+row['score'] + ')' #非评级币的编号 = （编号+ 品相）
            good_info["shape"] = row['grade']

        good_info["name"] = c_name + s_name

        img_1 = "picture/" + row['date'] + "/" + row['good_no'] + "-1.jpg"
        img = [img_1]
        for i in range(2,int(row['p_1'])+1):
            img.append(img_1.replace("-1.jpg","-"+str(i)+".jpg"))

        # img_1 = "picture/" + row['date'] + "/" + row['no.'] + "-1.jpg"
        # img_2 = img_1.replace("-1.jpg","-2.jpg")
        # img = [img_1, img_2]
        # o_img = [img_1.replace("picture/", "thumbnail/"), img_2.replace("picture/", "thumbnail/")]
        o_img = [x.replace("picture/", "thumbnail/") for x in img]
        good_info["images"] = json.dumps(o_img[:int(row['p_2'])])#缩列图
        good_info["original_image"] = json.dumps(img[:int(row['p_2'])])  #原图
        name_s = """<p class="ql-align-center"><strong>"""
        name_e = """</strong></p><p class="ql-align-center"><br></p>"""
        p_s = """<p class="ql-align-center">"""
        p_e = """</p>"""
        img_s = '<img src="'
        img_e = '">'
        picture_url_base = "https://online-1303141635.cos.ap-guangzhou.myqcloud.com/"  #图片的基本地址
        picture_url = [picture_url_base +x for x in img]
        # [picture_url_base + img_1, picture_url_base + img_2]
        picture_str = ''
        for i in range(int(row['p_1'])):
            picture_str = picture_str + img_s + picture_url[i] + img_e
        # good_info["content"] = name_s + good_info["name"] + name_e + p_s + img_s + picture_url[0] + img_e + img_s + picture_url[1] + img_e + p_e
        good_info["content"] = name_s + good_info["name"] + name_e + p_s + picture_str + p_e
        # print(good_info['content'])
        good_info["price"] = row["price"]#row["retain_price"]
        # good_info["retain_price"] = row["retain_price"] # 保留价
        # if row['grade'] != "裸币" or "":
        #     good_info["shape"] = "评级币"
        # else:
        #     good_info["shape"] = "裸币"
        good_info["seller_name"] = row["seller_name"]
        # good_info["delay_time"] = 0  # 延拍时间
        # good_info["goods_weight"] = 0
        # good_info["begin_time"] = topic_info["begin_time"]
        # good_info["end_time"] = topic_info["end_time"] + 30 * (k - 1)  # 30 ，单位为s ，按照该专场多长时间节拍一个进行计算
        good_info["agreement_no"] = row["agreement_no"]
        # 合同编号，格式按照 a+年+月+该专场在本月的排序，如果2022年1月份第一个专场 则设置为 a20220101
        # good_info["topic_id"] = topic_info['topic_id'] # 拍品所属专场
        good_info["category_id"] = row["category_id"] #拍品类目
        # good_info["buyer_service_rate"] = row["buyer_service_rate"]
        good_info["type"] = 2
        good_info["inventory"]= "1"
        good_info["inventory_unit"] = "枚"

        r = goods.goods_add(**good_info)
        k = k + 1
def test_good_add_sp_new():
    file_path = "/Users/yuanyuanhe/Desktop/货/拍品导入/新5-1-1.csv"
    good_add_new_sp(file_path)
    assert 1==2

def test_good_add_new():
    file_path = "/Users/yuanyuanhe/Desktop/货/拍品导入/新5-2.csv"
    topic_info = {}
    begin_time = times.str_to_time("2022-04-29 10:00:00")  # 开拍时间 ： 与专场开拍时间相同2022-04-22 10:00:00 2022-04-29 10:00:00
    end_time = times.str_to_time("2022-05-09 20:32:30")  # 结拍时间： 与专场结拍时间相同2022-04-25 20:00:00
    topic_info["begin_time"] = begin_time
    topic_info["end_time"] = end_time
    topic_info["agreement_no"] = ""
    topic_info["topic_id"] = "[51]"
    good_add_new(file_path, **topic_info)
def goods_edit_picture(file_path,good_id):
    '''对下架的拍品编辑时间'''
    f = open(file_path, mode="r", encoding='utf-8')
    reader = csv.DictReader(f)
    k = 0
    for i in range(5):
        good_info_json = {"id": good_id + k}
        goods_json = goods.goods_info(**good_info_json).json()['data']
        print(goods_json)
        goods_json["images"] = json.dumps(goods_json["images"]).replace("Chen","chen")
        goods_json["original_image"] = json.dumps(goods_json["original_image"]).replace("Chen", "chen")

        goods_json["content"] = goods_json["content"].replace("Chen", "chen")
        goods_json['topic_id'] = json.dumps(goods_json['topic_id'])
    # for row in reader:
    #     good_info_json = {"id": good_id+k}
    #     goods_json = goods.goods_info(**good_info_json).json()['data']
    #     img_1 = "picture/" + row['date'] + "/" + row['good_no'] + "-1.jpg"
    #     img = [img_1]
    #     for i in range(2, int(row['p_1']) + 1):
    #         img.append(img_1.replace("-1.jpg", "-" + str(i) + ".jpg"))
    #     o_img = [x.replace("picture/", "thumbnail/") for x in img]
    #     goods_json["images"] = json.dumps(o_img[:int(row['p_2'])])
    #     goods_json["original_image"] = json.dumps(img[:int(row['p_2'])])  # 原图
    #     print(goods_json["images"] )
    #     name_s = """<p class="ql-align-center"><strong>"""
    #     name_e = """</strong></p><p class="ql-align-center"><br></p>"""
    #     p_s = """<p class="ql-align-center">"""
    #     p_e = """</p>"""
    #     img_s = r'<img src=\"'
    #     img_e = r'\">'
    #     picture_url_base = "https://online-1303141635.cos.ap-guangzhou.myqcloud.com/"  # 图片的基本地址
    #     picture_url = [picture_url_base + x for x in img]
    #     # [picture_url_base + img_1, picture_url_base + img_2]
    #     picture_str = ''
    #     for i in range(int(row['p_1'])):
    #         picture_str = picture_str + img_s + picture_url[i]+ img_e
    #     # good_info["content"] = name_s + good_info["name"] + name_e + p_s + img_s + picture_url[0] + img_e + img_s + picture_url[1] + img_e + p_e
    #     goods_json["content"] = name_s + goods_json["name"] + name_e + p_s + picture_str + p_e
    #     print(goods_json['content'])
    #     # print(good_info['content'])
        k = k + 1
        r = goods.goods_edit(**goods_json)
        print(goods_json)
        print(r.json())
def test_good_edit_picture():
    file_path = "/Users/yuanyuanhe/Desktop/货/拍品导入/新4-3-1.csv"
    good_id = 2307
    goods_edit_picture(file_path, good_id)
    assert 1==2

def goods_edit(file_path):
    f = open(file_path, mode="r", encoding='utf-8')
    reader = csv.DictReader(f)
    for row in reader:

        good_id = row['id']
        good_info_json = {"id": good_id}
        goods_json = goods.goods_info(**good_info_json).json()['data']
        if "/" in row["date"]:
            img_1 = "picture/" + row['date'] + "-1.jpg"
        else:
            img_1 = "picture/" + row['date'] + "/" + row['good_no'] + "-1.jpg"
        img = [img_1]
        for i in range(2,int(row['p_1'])+1):
            img.append(img_1.replace("-1.jpg","-"+str(i)+".jpg"))
        o_img = [x.replace("picture/", "thumbnail/") for x in img]
        goods_json["images"] = json.dumps(o_img[:int(row['p_2'])])  # 缩列图
        goods_json["original_image"] = json.dumps(img[:int(row['p_2'])])  # 原图
        name_s = """<p class="ql-align-center"><strong>"""
        name_e = """</strong></p><p class="ql-align-center"><br></p>"""
        p_s = """<p class="ql-align-center">"""
        p_e = """</p>"""
        img_s = '<img src="'
        img_e = '">'
        picture_url_base = "https://online-1303141635.cos.ap-guangzhou.myqcloud.com/"  # 图片的基本地址
        picture_url = [picture_url_base + x for x in img]
        # [picture_url_base + img_1, picture_url_base + img_2]
        picture_str = ''
        for i in range(int(row['p_1'])):
            picture_str = picture_str + img_s + picture_url[i] + img_e
        # good_info["content"] = name_s + good_info["name"] + name_e + p_s + img_s + picture_url[0] + img_e + img_s + picture_url[1] + img_e + p_e
        goods_json["content"] = name_s + goods_json["name"] + name_e + p_s + picture_str + p_e
        goods_json['topic_id'] = json.dumps(goods_json['topic_id'])
        r= goods.goods_edit(**goods_json)

        print(r.json())
def test_goods_edit():
    file_path = "/Users/yuanyuanhe/Desktop/货/拍品导入/新5-1-3.csv"
    goods_edit(file_path)
    assert 1==2