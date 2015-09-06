# coding=utf-8
__author__ = 'wan'
""" 测试协程 """


import tornado.ioloop
from tornado.gen import coroutine
from tornado.concurrent import Future

@coroutine
def asyn_sum(a, b):
    print("begin calculate:sum %d+%d"%(a,b))
    future = Future()
    future_done(future)
    # def callback(a, b):
    #     print("calculating the sum of %d+%d:"%(a,b))
    #     # future.set_result(a+b)
    #     # return 1
    # tornado.ioloop.IOLoop.instance().add_callback(callback, a, b)

    result = yield future

    print("after yielded")
    print result

def future_done(future):
    data = {'a':1}
    future.set_result(data)
    # count = 0
    # if count == 2:
    #     future.set_result(count)
    # tornado.ioloop.IOLoop.instance().add_callback(future_done, future)
    # count += 1

def main():
    f = asyn_sum(2,3)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()