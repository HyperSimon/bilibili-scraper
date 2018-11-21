# coding=utf-8
import math
import time

import files
import Math

local_index = files.read('index.txt')
cur_index = 0 if local_index == '' else local_index
print cur_index

print "%s" % ('wangzhen')

num = 1
for i in range(1, 10 + 1):
    print "\r爬虫01号-第%d次访问！" % (i),
    num = num + 1

print (10 / 6) / 1.0

print Math.divide(1000000, 300, 4) * 100

print int(math.log(200000, 2))
