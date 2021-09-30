#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       log_color.py
Create time:    2019-08-28 17:31
Description:

"""

import logging
import re


# now we patch Python code to add color support to logging.StreamHandler
class CustomWindowsFilter(logging.Filterer):

    def _set_color(self, code):
        import ctypes

        # Constants from the Windows API
        self.STD_OUTPUT_HANDLE = -11
        hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)

    def filter(self, record):
        FOREGROUND_BLUE = 0x0001  # text color contains blue.
        FOREGROUND_GREEN = 0x0002  # text color contains green.
        FOREGROUND_RED = 0x0004  # text color contains red.
        FOREGROUND_INTENSITY = 0x0008  # text color is intensified.
        FOREGROUND_WHITE = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED
        # winbase.h
        STD_INPUT_HANDLE = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE = -12

        # wincon.h
        FOREGROUND_BLACK = 0x0000
        FOREGROUND_BLUE = 0x0001
        FOREGROUND_GREEN = 0x0002
        FOREGROUND_CYAN = 0x0003
        FOREGROUND_RED = 0x0004
        FOREGROUND_MAGENTA = 0x0005
        FOREGROUND_YELLOW = 0x0006
        FOREGROUND_GREY = 0x0007
        FOREGROUND_INTENSITY = 0x0008  # foreground color is intensified.

        BACKGROUND_BLACK = 0x0000
        BACKGROUND_BLUE = 0x0010
        BACKGROUND_GREEN = 0x0020
        BACKGROUND_CYAN = 0x0030
        BACKGROUND_RED = 0x0040
        BACKGROUND_MAGENTA = 0x0050
        BACKGROUND_YELLOW = 0x0060
        BACKGROUND_GREY = 0x0070
        BACKGROUND_INTENSITY = 0x0080  # background color is intensified.
        levelno = record.levelno

        if levelno >= 50:
            color = (
                    BACKGROUND_YELLOW
                    | FOREGROUND_RED
                    | FOREGROUND_INTENSITY
                    | BACKGROUND_INTENSITY
            )
        elif levelno >= 40:
            color = FOREGROUND_RED | FOREGROUND_INTENSITY
        elif levelno >= 30:
            color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
        elif levelno >= 20:
            color = FOREGROUND_GREEN
        elif levelno >= 10:
            color = FOREGROUND_MAGENTA
        else:
            color = FOREGROUND_WHITE
        self._set_color(color)

        self._set_color(FOREGROUND_WHITE)
        return record


class CustomNoFilter(logging.Filterer):
    def filter(self, record):
        reg_1 = r"\[\d+m"
        try:
            while True:
                comp_1 = re.search(reg_1, record.msg)
                if comp_1:
                    record.msg = record.msg.replace(comp_1.group(0), '')
                else:
                    break
        except Exception as e:
            pass
        return record
    
class CustomKeywordFilter(logging.Filterer):
    """
    过滤系统相关的log，用户一般不关注
    """
    FILTER_MAP = {
        "App.bindingCalled": "mini_send_request|mini_request_callback",
        "App.logAdded": "",
        
    }
    def filter(self, record):
        if isinstance(record.msg, (str, bytes)):
            for key, value in CustomKeywordFilter.FILTER_MAP.items():
                if value:
                    if record.msg.find(key) >= 0 and re.match(".*(%s).*" % value, record.msg):
                        return 0
                else:
                    if record.msg.find(key) >= 0:
                        return 0
        return record

class CustomFileFilter(logging.Filterer):
    FILTER_FILE = [
        "javadriver.py",
        "adbwrap.py",
        "basedriver.py",
    ]
    def filter(self, record: logging.LogRecord) -> bool:
        if record.filename in CustomFileFilter.FILTER_FILE:
            return 0
        return super().filter(record)

class CustomMacFilter(logging.Filterer):
    def filter(self, record):
        levelno = record.levelno
        if levelno >= 50:
            color = "\x1b[31m"  # red
        elif levelno >= 40:
            color = "\x1b[31m"  # red
        elif levelno >= 30:
            color = "\x1b[33m"  # yellow
        elif levelno >= 20:
            color = "\x1b[32m"  # green
        elif levelno >= 10:
            color = "\x1b[35m"  # pink
        else:
            color = "\x1b[0m"  # normal
        try:
            record.msg = color + record.msg + "\x1b[0m"  # normal
        except Exception as e:
            pass
        # print "after"
        return record


#
# def add_coloring_to_emit_windows(fn):
#     # add methods we need to the class
#     def _out_handle(self):
#         import ctypes
#
#         return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
#
#     out_handle = property(_out_handle)
#
#
#
#     setattr(logging.StreamHandler, "_set_color", _set_color)
#
#     def new(*args):
#         FOREGROUND_BLUE = 0x0001  # text color contains blue.
#         FOREGROUND_GREEN = 0x0002  # text color contains green.
#         FOREGROUND_RED = 0x0004  # text color contains red.
#         FOREGROUND_INTENSITY = 0x0008  # text color is intensified.
#         FOREGROUND_WHITE = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED
#         # winbase.h
#         STD_INPUT_HANDLE = -10
#         STD_OUTPUT_HANDLE = -11
#         STD_ERROR_HANDLE = -12
#
#         # wincon.h
#         FOREGROUND_BLACK = 0x0000
#         FOREGROUND_BLUE = 0x0001
#         FOREGROUND_GREEN = 0x0002
#         FOREGROUND_CYAN = 0x0003
#         FOREGROUND_RED = 0x0004
#         FOREGROUND_MAGENTA = 0x0005
#         FOREGROUND_YELLOW = 0x0006
#         FOREGROUND_GREY = 0x0007
#         FOREGROUND_INTENSITY = 0x0008  # foreground color is intensified.
#
#         BACKGROUND_BLACK = 0x0000
#         BACKGROUND_BLUE = 0x0010
#         BACKGROUND_GREEN = 0x0020
#         BACKGROUND_CYAN = 0x0030
#         BACKGROUND_RED = 0x0040
#         BACKGROUND_MAGENTA = 0x0050
#         BACKGROUND_YELLOW = 0x0060
#         BACKGROUND_GREY = 0x0070
#         BACKGROUND_INTENSITY = 0x0080  # background color is intensified.
#
#         levelno = args[1].levelno
#         if levelno >= 50:
#             color = (
#                 BACKGROUND_YELLOW
#                 | FOREGROUND_RED
#                 | FOREGROUND_INTENSITY
#                 | BACKGROUND_INTENSITY
#             )
#         elif levelno >= 40:
#             color = FOREGROUND_RED | FOREGROUND_INTENSITY
#         elif levelno >= 30:
#             color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
#         elif levelno >= 20:
#             color = FOREGROUND_GREEN
#         elif levelno >= 10:
#             color = FOREGROUND_MAGENTA
#         else:
#             color = FOREGROUND_WHITE
#         args[0]._set_color(color)
#
#         ret = fn(*args)
#         args[0]._set_color(FOREGROUND_WHITE)
#         # print "after"
#         return ret
#
#     return new
#
#
# def add_coloring_to_emit_ansi(fn,*args):
#     # add methods we need to the class
#     # def new(*args):
#         levelno = args[1].levelno
#         if levelno >= 50:
#             color = "\x1b[31m"  # red
#         elif levelno >= 40:
#             color = "\x1b[31m"  # red
#         elif levelno >= 30:
#             color = "\x1b[33m"  # yellow
#         elif levelno >= 20:
#             color = "\x1b[32m"  # green
#         elif levelno >= 10:
#             color = "\x1b[35m"  # pink
#         else:
#             color = "\x1b[0m"  # normal
#         try:
#             args[1].msg = color + args[1].msg + "\x1b[0m"  # normal
#         except Exception as e:
#             pass
#         # print "after"
#         return fn(*args)

# return new

# def del_coloring_to_emit_ansi(fn):
#     def new()

# import platform
#
# if platform.system() == "Windows":
#     # Windows does not support ANSI escapes and we are using API calls to set the console color
#     logging.StreamHandler.emit = add_coloring_to_emit_windows(
#         logging.StreamHandler.emit
#     )
# else:
#     # all non-Windows platforms are supporting ANSI escapes so we use them
#     logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)

global colorfilter
colorfilter = CustomMacFilter()
global nofilter
nofilter = CustomNoFilter()
global kwfilter
kwfilter = CustomKeywordFilter()
global filefilter
filefilter = CustomFileFilter()

if __name__ == "__main__":
    logger = logging.getLogger("locker")
    # filter = CustomMacFilter()
    filter = CustomMacFilter()
    logger.addFilter(filter)
    # logger.setLevel(20)
    # logger
    # logger.error(add_coloring_to_emit_ansi("1","locker_error",))
    logger.debug("locker_info")
    logger.error('a warn')
    logger.warning('another warning message')
    logger.removeFilter(filter)
    # logger.setLevel(20)
    # logger
    # logger.error(add_coloring_to_emit_ansi("1","locker_error",))
    logger.debug("locker_info")
    logger.error('a warn')
    logger.warning('another warning message')
