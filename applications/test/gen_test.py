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

    # def callback(a, b):
    #     print("calculating the sum of %d+%d:"%(a,b))
    #     # future.set_result(a+b)
    #     # return 1
    # tornado.ioloop.IOLoop.instance().add_callback(callback, a, b)

    result = yield future

    print("after yielded")
    print("the %d+%d=%d"%(a, b, result))

def future_done(future):
    return future.result()

def main():
    f = asyn_sum(2,3)
    print f
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()