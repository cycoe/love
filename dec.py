#/usr/bin/python
#coding: utf-8

def logger(func):
    def in_dec(x, y):
        with open('test.log', 'a') as fr:
            fr.write('cal with abs(%d - %d)\n' % (x, y))
        return func(x, y)
    return in_dec

@logger
def abs_(x, y):
    return abs(x - y)



print(abs_(2, 3))
