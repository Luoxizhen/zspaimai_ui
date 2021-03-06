#!/usr/bin/env python3
# Created by xiazeng on 2019-06-14
import time


def wait_true(func, timeout, idle=1):
    s = time.time()
    while time.time() - s < timeout:
        r = func()
        if r:
            return r
        time.sleep(idle)
    return False
