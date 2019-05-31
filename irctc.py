from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, datetime
username="g1rao18"
password="ghg756"
from1="PALASA - PSA"
to="SECUNDERABAD JN - SC"
date=""
browser = webdriver.Chrome("C:\Users\Jeevan\Downloads\chromedriver_win32\chromedriver.exe")
def login(username,password):
        browser.get("https://www.irctc.co.in/nget/train-search")


        test = browser.find_element_by_xpath('/html/body/app-root/app-home/div/div/app-main-page/div[2]/div/div[1]/div/div/div[1]/div/app-jp-input/div[3]/form/div[2]/div[2]/p-autocomplete/span/input')
        test.send_keys("palasa")
        time.sleep(3)
        signin=browser.find_element_by_xpath('/html/body/app-root/app-home/app-header/div[2]/div[2]/div[1]/a[1]')
        signin.send_keys(Keys.RETURN)

#login(username,password)
def from_to(from1,to):
        browser.get("https://www.irctc.co.in/nget/train-search")
        username = browser.find_element_by_xpath('/html/body/app-root/app-home/div/div/app-main-page/div[2]/div/div[1]/div/div/div[1]/div/app-jp-input/div[3]/form/div[2]/div[2]/p-autocomplete/span/input')
        username.send_keys(from1)
        password = browser.find_element_by_css_selector("#destination > span:nth-child(1) > input:nth-child(1)")
        password.send_keys(to)
        date=browser.find_element_by_css_selector("input.ng-tns-c14-5")
        for i in range(10):
                date.send_keys(Keys.BACKSPACE)
        date.send_keys("26-06-2018")
        class1=browser.find_element_by_css_xpath("/html/body/app-root/app-home/div/div/app-main-page/div[2]/div/div[1]/div/div/div[1]/div/app-jp-input/div[3]/form/div[4]/p-dropdown/div/label")
        class1.send_keys(Keys.DOWN)

from_to(from1,to)
