import logging
import os
import datetime



def create_filename():
    curpath = os.path.dirname(os.path.realpath(__file__))
    parpath = os.path.dirname(curpath)

    filename = os.path.join(parpath, 'log', 'my.log')
    return filename

filename = create_filename()
'''format=%(asctime)s 具体时间 %(filename)s 文件名 %(levelname)s 日志级别 %(message)s 日志内容 %(datemt)='a%%d%b%Y%H:%M:%S'日期格式,filename='my.log',fliemode='w's'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s  %(filename)s  %(levelname)s  %(message)s', datefmt='%a%d%b%Y  %H:%M:%S', filename=filename, filemode='a')


logging.info("第一条日志")
logging.error('第一条错误信息')