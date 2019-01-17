from prometheus_client import start_http_server, Histogram
import random
import time

function_exec = Histogram('function_exec_time',
                          'Time spend processing a function',
                          ['func_name'])


def func1():
    if random.random() < 0.02:
        time.sleep(2)
        return
    time.sleep(0.2)


def func2():
    if random.random() < 0.5:
        time.sleep(0.6)
        return
    time.sleep(0.4)


start_http_server(9100)
while True:
    start_time1 = time.time()
    func1()
    function_exec.labels(func_name='func1').observe(time.time() - start_time1)
    start_time2 = time.time()
    func2()
    function_exec.labels(func_name='func2').observe(time.time() - start_time2)
