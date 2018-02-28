#coding=utf-8
from selenium import webdriver

import unittest,time

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('disable-gpu')
options.add_argument('no-sandbox')
class TestBaidu(unittest.TestCase):
    u'测试百度1'
    def setUp(self):
        self.driver = webdriver.Chrome()
        #self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)
        self.base_url = "http://www.baidu.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_baidu_search(self):
        u"""百度搜索"""
        driver = self.driver
        driver.get(self.base_url + '/')
        driver.find_element_by_id("kw").send_keys("selenium webdriver")
        driver.find_element_by_id("su").click()
        time.sleep(2)
        driver.close()

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([],self.verificationErrors)
