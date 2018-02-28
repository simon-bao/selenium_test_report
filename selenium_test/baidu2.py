#coding=utf-8
from selenium import webdriver
import unittest,time

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('disable-gpu')
options.add_argument('no-sandbox')
class Baidu(unittest.TestCase):
    u'测试百度2'
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.base_url = "http://www.baidu.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_baidu_search(self):
        u"""百度搜索第二次"""
        driver = self.driver
        driver.get(self.base_url + '/')
        driver.find_element_by_id("kw").send_keys(u'百度强吗？')
        driver.find_element_by_id("su").click()
        time.sleep(2)
        driver.close()
    def test_baidu_set(self):
        u"""百度设置第二次"""
        driver = self.driver
        #进入搜索设置页
        driver.get(self.base_url + '/gaoji/preferences.html')
        #设置每页搜索结果为 20 条
        m=driver.find_element_by_name("NR")
        m.find_element_by_xpath("//option[@value='20']").click()
        time.sleep(2)
        #保存设置的信息
        driver.find_element_by_xpath("/html/body/form/div/input").click()
        time.sleep(2)
        driver.switch_to_alert().accept()
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([],self.verificationErrors)

