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
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timestamp()
        res = func(*args, **kwargs)
        print("检验元素done！用时%.3fs!" %(timestamp()-start))
        return res
    return wrapper

if __name__ == '__main__':
    print(dt_strftime("%Y%m%d%H%M%S"))


