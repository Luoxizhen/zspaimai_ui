'''时间封装模块'''
import time
import datetime
def timestamp():
    #时间戳
    return time.time()

def dt_strftime(fmt="%Y%m"):
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
    print(lt)
    r = time.strftime("%Y-%m-%d %H:%M:%S", lt)
    return r
def str_to_time(str):
    p_tuple = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    t = time.mktime(p_tuple)
    return round(t)


if __name__ == '__main__':
   p = "2021_11_18-180246"
   print(str_to_time(p))



