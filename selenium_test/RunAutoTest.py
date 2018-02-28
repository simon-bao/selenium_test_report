#coding=utf-8
import unittest
#这里需要导入测试文件
import RollAppsTestRunner2018
import baidu2,baidu,Test1,add
from sys import argv
import os

#定义个报告存放路径，支持相对路径。
if argv.__len__() > 1:#判断是否有python命令行参数，这里假设命令行参数只有一个字符串
    filename = argv[1] + '.json'
    build_tag = argv[1]
else:
    filename= "RollappsSeleniumReport.json"
    build_tag = ''

cur_dir = os.getcwd()

new_dir = os.path.join(cur_dir, 'target')

isExists=os.path.exists(new_dir)

if not isExists:
    os.makedirs(new_dir)

#定义报告输出文件的全路径文件名）
path_filename = os.path.join(new_dir, filename)

fp = open(path_filename,"wb")
runner = RollAppsTestRunner2018.RollAppsTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况：', report_id=build_tag)

#将测试用例加入到测试容器(套件)中
testunit=unittest.TestSuite()
testunit.addTest(unittest.makeSuite(Test1.Test1))   #baidu.Baidu中的baidu为用例所在的.py文件的名称，Baidu为测试用例集的名称
#testunit.addTest(unittest.makeSuite(baidu2.Baidu))

#执行测试用例
runner.run(testunit)
