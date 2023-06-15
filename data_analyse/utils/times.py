'''时间封装模块'''
import time
import datetime
def timestamp():
    #时间戳
    return round(time.time())

def dt_strftime(fmt="%Y%m%d-%H%M%S"):
    '''
    datetime 格式化时间
    :param fmt:
    :return:
    '''
    return datetime.datetime.now().strftime(fmt)

def sleep(seconds=1.0):
    '''
    睡眠时间
    :param seconds:
    :return:
    '''
    time.sleep(seconds)
def running_time(func):
    '''函数运行时间'''
    #@wraps(func)
    def wrapper(*args, **kwargs):
        start = timestamp()
        res = func(*args, **kwargs)
        print("检验元素done！用时%.3fs!" %(timestamp()-start))
        return res
    return wrapper
@running_time
def sleep1():
    time.sleep(2)
    print("已经过2s")

def time_to_str(t):
    lt = time.localtime(t)
    # print(lt)
    r = time.strftime("%Y-%m-%d %H:%M:%S", lt)
    return r
def str_to_time(str):
    try:
        p_tuple = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        p_tuple = time.strptime(str, "%Y/%m/%d %H:%M:%S")
        print(e)
    t = time.mktime(p_tuple)
    print(int(t))
    return int(t)


if __name__ == '__main__':
   str_to_time("2022/10/10 22:10:21")



