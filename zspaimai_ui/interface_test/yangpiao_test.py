import csv

from interface_base import yangpiao
def t_yangpiao():
    p = 1
    n = 81
    while 1:
        r = yangpiao.get_bid_history_data(p=p,nid=n,rid=3)
        if r.json()["data"]!=[]:
            bids = []
            bid_infos = r.json()["data"] #每个页面中包含的所有拍品的信息
            for a_bid_info in bid_infos: #每个拍品的信息
                del a_bid_info["data_display"]
                del a_bid_info["dimension"]
                del a_bid_info["cert"]
                # 拍品的名称，编号，品相，落槌价，佣金比例，出价次数，，优惠折扣，成交时间
                bids.append(a_bid_info.values())
            file_path = "/Users/yuanyuanhe/Desktop/竞拍分析/yangpiao/三版币元币.csv"  #写入一个页面的内容
            with open(file_path, "a", encoding="utf-8") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerows(bids)
            p = p + 1
        elif n < 90: #如果页面没有数据了，重新获取另一个品种的数据
            p = 1
            n = n+1
        else:
            break



if __name__ == "__main__":
    t_yangpiao()






