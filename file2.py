import time
def dec(func):
    def time1(*args, **kwargs):
        x = time.time()
        result = func(*args, **kwargs)
        y = time.time()
        print(y - x)
        return result
    return time1
@dec
def timetime():
    print('Uwaga')
timetime()
