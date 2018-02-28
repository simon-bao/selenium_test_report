# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os

class Test1(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()#手动添加的最大化浏览器窗口
        self.base_url = "http://detian.vicp.net/userui"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_1(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("username").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("yzm").click()
        driver.find_element_by_id("yzm").clear()
        driver.find_element_by_id("yzm").send_keys("9999")
        driver.find_element_by_id("loginbtn").click()

        #driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/ul/li[5]/a/span").click()

        driver.find_element_by_link_text("我的项目").click()
        time.sleep(2)
        xf = driver.find_element_by_xpath('//*[@id="pageWrapper"]')#切换到pageWrapper的iFrame
        driver.switch_to.frame(xf)
        #driver.find_element_by_xpath('//button[@id="btnAdd"]').click()
        Select(driver.find_element_by_id("selectProject")).select_by_visible_text("CMDB二期")#这一步通过了
        #driver.find_element_by_xpath("//option[@value='351f5240-7b3b-4707-94c0-e78baa107f37']").click()
        driver.find_element_by_xpath('/html/body/div[2]/table[1]/tbody/tr[2]/td[2]/a').click()
        time.sleep(2)
        #driver.find_element_by_xpath("//a[@id='codeSubmit']").click()
        #time.sleep(2)

        #获取当前目录下upload文件夹的jeesns.zip文件路径
        filename = 'jeesns.zip'
        cur_dir = os.getcwd()

        upload_dir = os.path.join(cur_dir, 'upload')

        isExists = os.path.exists(upload_dir)

        if not isExists:
            return -1

        path_filename = os.path.join(upload_dir, filename)

        #将jeesns.zip文件的全路径传输给id=multipartFileInput的input标签
        driver.find_element_by_id('multipartFileInput').send_keys(path_filename)
        time.sleep(2)

        #点击“提交上传”按钮
        driver.find_element_by_id('sureUploadFiles').click()

        #driver.find_element_by_id("multipartFileInput").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
