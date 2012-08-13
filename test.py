#coding:utf-8
import os
def showDir(abspath):
    allFiles = os.listdir(abspath)
    for one in xrange(len(allFiles)):
        allFiles[one] = allFiles[one].encode('UTF-8')
        print allFiles[one], '--->', type(allFiles[one])

showDir('/home/tang')
