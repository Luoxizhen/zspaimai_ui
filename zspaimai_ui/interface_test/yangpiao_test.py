import csv
from utils import times,log,rwyaml
from interface_base import yangpiao
def t_yangpiao():
    '''从样票网爬取成交数据
    p：页码
    n: 钞票编码
    rid ： 版本号
    第一版： rid = 1 ,nid = 1-60
    第二版：rid=2，nid= 61-73
    第三版：rid=3，nid= 74-81
    第四版：rid=4，100元 84，50元 85 '''

    p = 1
    n = 84
    rid =4
    num = 0
    dealTime_start = times.str_to_time("2000-01-01 00:00:00")
    dealTime_end = times.str_to_time("2022-10-17 00:00:00")
    '''每周更新数据'''
    while 1:
        r = yangpiao.get_bid_history_data(p=p,nid=n,rid=3)
        if r.json()["data"]!=[]:
            bids = []
            bid_infos = r.json()["data"] #每个页面中包含的所有拍品的信息
            for a_bid_info in bid_infos: #每个拍品的信息
                if a_bid_info["dealTime"] < dealTime_start or a_bid_info["dealTime"] > dealTime_end:
                    break
                del a_bid_info["data_display"]
                del a_bid_info["dimension"]
                del a_bid_info["cert"]
                del a_bid_info["lot"]
                del a_bid_info["title"]
                del a_bid_info["is_specimen"]


                if type(a_bid_info["serial"]) == str:
                    serial_num = a_bid_info["serial"]
                    while serial_num.find("<") != -1:  # 去掉格式
                        start_s = serial_num.find("<")
                        end_s = serial_num.find(">") + 1
                        temp_s = serial_num[start_s:end_s]
                        serial_num = serial_num.replace(temp_s, "")
                    a_bid_info["serial"] = serial_num


                # 拍品的名称，编号，品相，落槌价，佣金比例，出价次数，，优惠折扣，成交时间
                bids.append(a_bid_info.values())
            file_path = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/2023/四版100元.csv"  #写入一个页面的内容
            with open(file_path, "a", encoding="utf-8") as f:
                csv_writer = csv.writer(f)
                if bids:
                    print("版别：{}, 类目：{}, 页面：{}" .format(rid,n,p))
                    log_msg = "版别："+ str(rid) +", 类目："+str(n) +", 页面："+str(p) + "\n"
                    log.log.info(log_msg)

                    csv_writer.writerows(bids)
                    # print(bids)
                else:
                    break
            p = p + 1 #从第一页开始爬数据，一直爬到这个类别的数据没有了
        elif n < 81: #如果页面没有数据了，重新获取另一个品种的数据
            p = 1
            n = n+1
        else:
            break
def t_yangpiao_one_kind():
    '''从样票网爬取成交数据,所有的历史成交数据，单一品种
    p：页码
    n: 钞票编码
    rid ： 版本号
    第一版： rid = 1 ,nid = 1-60
    第二版：rid=2，nid= 61-73
    第三版：rid=3，nid= 74-81
    第四版：rid=4，100元 84，50元 85 '''

    p = rwyaml.get_yaml_data("interface_data","yangpiao.yml")["history_bid"]["p"]
    n = rwyaml.get_yaml_data("interface_data","yangpiao.yml")["history_bid"]["n"]
    rid =rwyaml.get_yaml_data("interface_data","yangpiao.yml")["history_bid"]["rid"]
    ts = rwyaml.get_yaml_data("interface_data","yangpiao.yml")["history_bid"]["dealTimeStr"]
    # num = 0
    # dealTime_start = times.str_to_time(rwyaml.get_yaml_data("interface_data","yangpiao.yml")["history_bid"]["begin_time"])
    # dealTime_end = times.str_to_time(rwyaml.get_yaml_data("interface_data","yangpiao.yml")["history_bid"]["end_time"])
    '''每周更新数据'''
    while 1:
        r = yangpiao.get_bid_history_data(p=p,nid=n,rid=rid,t=ts)
        if r.json()["data"]!=[]:
            bids = []
            bid_infos = r.json()["data"] #每个页面中包含的所有拍品的信息
            for a_bid_info in bid_infos: #每个拍品的信息
                # if a_bid_info["dealTime"] < dealTime_start or a_bid_info["dealTime"] > dealTime_end:
                #     break
                del a_bid_info["data_display"]
                del a_bid_info["dimension"]
                del a_bid_info["cert"]
                del a_bid_info["lot"]
                # del a_bid_info["title"]
                del a_bid_info["is_specimen"]


                if type(a_bid_info["serial"]) == str:
                    serial_num = a_bid_info["serial"]
                    while serial_num.find("<") != -1:  # 去掉格式
                        start_s = serial_num.find("<")
                        end_s = serial_num.find(">") + 1
                        temp_s = serial_num[start_s:end_s]
                        serial_num = serial_num.replace(temp_s, "")
                    a_bid_info["serial"] = serial_num


                # 拍品的名称，编号，品相，落槌价，佣金比例，出价次数，，优惠折扣，成交时间
                bids.append(a_bid_info.values())
            file_path = rwyaml.get_yaml_data("interface_data","yangpiao.yml")["history_bid"]["file_path"]  #写入一个页面的内容

            with open(file_path, "a", encoding="utf-8") as f:
                csv_writer = csv.writer(f)
                if bids:
                    print("版别：{}, 类目：{}, 页面：{}" .format(rid,n,p))
                    log_msg = "版别："+ str(rid) +", 类目："+str(n) +", 页面："+str(p) + "\n"
                    log.log.info(log_msg)

                    csv_writer.writerows(bids)
                    # print(bids)
                else:
                    break
            p = p + 1 #从第一页开始爬数据，一直爬到这个类别的数据没有了
        # elif n < 81: #如果页面没有数据了，重新获取另一个品种的数据
        #     p = 1
        #     n = n+1
        else:
            break

def t_yangpiao_3_kinds():
    '''从样票网爬取成交数据,筛选一定时间段的数据。
    p：页码
    n: 钞票编码
    rid ： 版本号
    第一版： rid = 1 ,nid = 1-60
    第二版：rid=2，nid= 61-73
    第三版：rid=3，nid= 74-81
    第四版：rid=4，nid=84-92
    第三版的最近时间是：1666264988'''
    p = 1
    n = 1
    rid = 1
    n2 = 81
    n3 = [60,73,81]
    num = 0
    # dealTime_start = times.str_to_time("2022-10-17 00:00:00")
    yp_data = rwyaml.get_yaml_data("interface_data","yangpiao.yml")
    begin_time = yp_data["history_bid"]["begin_time"]
    end_time = yp_data["history_bid"]["end_time"]
    print(begin_time)
    print(end_time)
    dealTime_start = times.str_to_time(begin_time)
    dealTime_end = times.str_to_time(end_time)
    '''每周更新数据'''
    while 1:
        r = yangpiao.get_bid_history_data(p=p,nid=n,rid=rid)
        if r.json()["data"]!=[]:
            bids = []
            bid_infos = r.json()["data"] #每个页面中包含的所有拍品的信息
            for a_bid_info in bid_infos: #每个拍品的信息
                if dealTime_start <= a_bid_info["dealTime"] < dealTime_end :
                    del a_bid_info["data_display"]
                    del a_bid_info["dimension"]
                    del a_bid_info["cert"]
                    del a_bid_info["lot"]
                    del a_bid_info["title"]
                    del a_bid_info["is_specimen"]
                    if type(a_bid_info["serial"]) == str:
                        serial_num = a_bid_info["serial"]
                        while serial_num.find("<") != -1:  # 去掉格式
                            start_s = serial_num.find("<")
                            end_s = serial_num.find(">") + 1
                            temp_s = serial_num[start_s:end_s]
                            serial_num = serial_num.replace(temp_s, "")
                    a_bid_info["serial"] = serial_num
                    # 拍品的名称，编号，品相，落槌价，佣金比例，出价次数，，优惠折扣，成交时间
                    bids.append(a_bid_info.values())
            file_path = yp_data["history_bid"]["file_path"]  #写入一个页面的内容
            with open(file_path, "a", encoding="utf-8") as f:
                csv_writer = csv.writer(f)
                if bids:
                    print("版别：{}, 类目：{}, 页面：{}" .format(rid,n,p))
                    log_msg = "版别："+ str(rid) +", 类目："+str(n) +", 页面："+str(p) + "\n"
                    log.log.info(log_msg)

                    csv_writer.writerows(bids)
                    # print(bids)
                # else:
                #     break
            p = p + 1 #从第一页开始爬数据，一直爬到这个类别的数据没有了
        elif n < n3[0] : #如果页面没有数据了，重新获取另一个品种的数据
            rid =1
            p = 1
            n = n + 1
        elif n3[0] <= n < n3[1]:
            rid = 2
            n = n + 1
            p = 1
        elif n3[1] <= n < n3[2]:
            rid = 3
            n = n + 1
            p = 1

        else:
            break



if __name__ == "__main__":
    t_yangpiao_3_kinds()






