"""
Required Python Modules to execute this program:
        selenium    (pip install selenium)
        PIL         (pip install pillow)
        pytesseract (pip install pytesseract)
        tesseract (apt-get update && apt-get install tesseract-ocr)
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime,time,sys
import urllib,os
from pytesseract import image_to_string
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


browser = webdriver.Chrome("/home/ubuntu/Downloads/chromedriver_linux64/chromedriver")

def check_alert():

        time.sleep(2)
        if EC.alert_is_present():
                try:
                        alert = browser.switch_to.alert
                        alert.accept()
                        fill_data()
                except:
                        print "Success"
        else:
            print("no alert, so success ")

def scan_captcha():
        print "Scanning Captchaa....!"
        img = browser.find_element_by_xpath("/html/body/form/center/div[2]/table/tbody/tr[1]/td/table/tbody/tr[6]/td[1]/div/img")
        src = img.get_attribute('src')
        print "found url...!\t Trying to download image"
        urllib.urlretrieve(src, "captcha.jpeg")
        print "Downloaded Captcha ...!"
        return image_to_string(Image.open("captcha.jpeg")).replace(" ","")


def fill_data():

        captcha = scan_captcha()
        os.system("rm -rf captcha.jpeg")
        browser.find_element_by_id("txtCaptcha").clear()
        _fill_captcha= browser.find_element_by_id("txtCaptcha")
        _fill_captcha.send_keys(captcha)
        print "Scanned captcha is: %s\nCaptcha entered successfully ...!"%(captcha)
        _search = browser.find_element_by_xpath('//*[@id="btn_Search"]')
        _search.click()
        check_alert()


def open_url(url="http://ceoaperms.ap.gov.in/search/search.aspx"):
        browser.get(url)
        _district = browser.find_element_by_xpath('//*[@id="ddldistlist"]')
        _district.send_keys(Keys.ARROW_DOWN)
        _AC= browser.find_element_by_xpath('//*[@id="ddlaclist"]')
        _AC.send_keys(Keys.ARROW_DOWN)
        _house=browser.find_element_by_id("txtHNo")
        _house.send_keys("114")
        fill_data()
        print "Program executed Successfully...!"

open_url("https://www.nvsp.in/forms/Forms/form7?lang=en-GB")
