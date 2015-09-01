# coding=utf-8
__author__ = 'wan'

def test():
    print 'start'

    a = yield 1
    print a
    print 'end'



if __name__ == '__main__':
    t=test()
    t.next()
    t.send('1')
    # t.next()

