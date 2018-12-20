from selenium import webdriver
import unittest
import os
import time
import shutil
import smtplib
import inspect
import zipfile
import unittest
from datetime import date, timedelta, datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import unicodedata
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
import HtmlTestRunner

class PortalUnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path='C:\\PortalTesting\\Drivers\\chromedriver.exe')
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_search_automationstepbystep(self):
        self.driver.get("https://portal.touchcommerce.com/portal/portal.jsp")

        # wait = WebDriverWait(driver, 10)
        # driver.implicitly_wait(30)
        username = self.driver.find_element_by_css_selector("#uid")
        username.send_keys("portal@testing")
        password = self.driver.find_element_by_css_selector("#pid")
        password.send_keys("Summer01")

        login_button = self.driver.find_element_by_class_name("secondarybtnlabel")
        login_button.click()
        time.sleep(10)
        self.driver.get_screenshot_as_file("C:\\Nuance\\New folder\\login.png")


    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        print("Test Completed")


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/PortalTesting/'))  #
