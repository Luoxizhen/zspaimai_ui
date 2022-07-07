import csv

from interface_base import yangpiao
def t_yangpiao():
    '''从样票网爬取成交数据
    p：页码
    n: 钞票编码
    rid ： 版本号
    第一版： rid = 1 ,nid = 1-60
    第二版：rid=2，nid= 61-73
    第三版：rid=3，nid= 74-81'''
    p = 1
    n = 81
    dealTime = 1655206547
    while 1:
        r = yangpiao.get_bid_history_data(p=p,nid=n,rid=3)
        if r.json()["data"]!=[]:
            bids = []
            bid_infos = r.json()["data"] #每个页面中包含的所有拍品的信息
            for a_bid_info in bid_infos: #每个拍品的信息
                if a_bid_info["dealTime"] < dealTime:
                    break
                del a_bid_info["data_display"]
                del a_bid_info["dimension"]
                del a_bid_info["cert"]
                del a_bid_info["lot"]
                del a_bid_info["title"]
                del a_bid_info["is_specimen"]
                del a_bid_info["did"]

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
            file_path = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/三版币元币.csv"  #写入一个页面的内容
            with open(file_path, "a", encoding="utf-8") as f:
                csv_writer = csv.writer(f)
                if bids:
                    csv_writer.writerows(bids)
                else:
                    break
            p = p + 1
        elif n < 90: #如果页面没有数据了，重新获取另一个品种的数据
            p = 1
            n = n+1
        else:
            break



if __name__ == "__main__":
    t_yangpiao()






