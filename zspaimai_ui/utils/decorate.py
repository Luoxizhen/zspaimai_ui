import time

def dec(func):
    def elapsed_time(t):
        start = time.time()
        func(t)
        end = time.time()
        print(end-start,1)
    return elapsed_time
@dec
def func(t):
    for i in range(t):
        time.sleep(1)

func(4)




