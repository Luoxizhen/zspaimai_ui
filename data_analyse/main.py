from analyse.one_chen import drop_duplicate_by_name,get_customer_info
from spider_1c.getdata_1c import SpiderMan as sm

def get_phone_from_title():
    f0 = "/Users/yuanyuanhe/Desktop/连体钞纪念钞_卖.csv"
    f1 = "/Users/yuanyuanhe/Desktop/连体钞纪念钞_卖_去重去空.csv"
    f2 = "/Users/yuanyuanhe/Desktop/连体钞纪念钞_卖贴.csv"
    f3 = "/Users/yuanyuanhe/Desktop/连体钞纪念钞_卖家.csv"
    f4 = "/Users/yuanyuanhe/Desktop/连体钞纪念钞_卖家_无电话号码.csv"
    f_1 = [f0,f1]
    f_2 = [f1,f2]
    f_3 = [f2,f3,f4]
    print(f_1,f_2,f_3)

    # drop_duplicate_by_name(*f_1)
    # sm.get_contact(0,*f_2)
    get_customer_info(*f_3)


if __name__ == "__main__":
    get_phone_from_title()