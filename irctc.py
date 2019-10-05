from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, datetime

username="g1rao18"
password="ghg756"
origin="PALASA - PSA"
destination="SECUNDERABAD JN - SC"
_date="01-10-2019"
name = 'Jeevan Rao T'
age = '24'

browser = webdriver.Chrome(r"C:\Users\jt250054\Documents\chromedriver_win32\chromedriver.exe")

def waitFor(x_path=None,id=None):
        timeout = 60
        wait = ui.WebDriverWait(browser,timeout)
        if x_path:
                wait.until(lambda browser: browser.find_element_by_xpath(x_path))
        else:
                wait.until(lambda browser: browser.find_element_by_id(id))

def login(browser,username,password,origin,destination,_date):
        browser.get("https://www.irctc.co.in/nget/train-search")
        browser.maximize_window()
        signin_sidepanel_xpath = "/html/body/app-root/app-home/div[1]/app-header/div[1]/div[3]/a/i"
        waitFor(signin_sidepanel_xpath)
        signin_sidepanel_button = browser.find_element_by_xpath(signin_sidepanel_xpath).click()
        signin_button_1 = browser.find_element_by_xpath('//*[@id="slide-menu"]/p-sidebar/div/nav/div/label/button').click()
        waitFor(None,'userId')
        input_username = browser.find_element_by_id('userId')
        input_username.send_keys(username)
        input_password = browser.find_element_by_id("pwd")
        input_password.send_keys(password)
        return browser


def search_train(browser,origin,destination,_date):
        logout_xpath = '//*[@id="slide-menu"]/p-sidebar/div/nav/div/label/a/span/b'
        waitFor(logout_xpath) 
        origin_xpath = '//*[@id="origin"]/span/input'
        #waitFor(origin_xpath)
        origin_object = browser.find_element_by_xpath(origin_xpath)
        origin_object.send_keys(origin)
        time.sleep(1)
        destination_object = browser.find_element_by_xpath('//*[@id="destination"]/span/input')
        destination_object.send_keys(destination)
        time.sleep(1)
        date_object = browser.find_element_by_xpath('//*[@id="divMain"]/div/app-main-page/div[1]/div/div[1]/div/div/div[1]/div/app-jp-input/div[3]/form/div[3]/p-calendar/span/input')            
        [date_object.send_keys(Keys.BACKSPACE) for _ in range(10)]
        date_object.send_keys(_date)
        time.sleep(1)        
        browser.find_element_by_xpath('//*[@id="divMain"]/div/app-main-page/div[1]/div/div[1]/div/div/div[1]/div/app-jp-input/div[3]/form/div[7]/button').submit()

        tatkal_lnk_object = '//*[@id="divMain"]/div/app-train-list/div/div[5]/div/div[2]/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/p-dropdown/div/label'
        waitFor(tatkal_lnk_object)
        tatkal_object = '//*[@id="divMain"]/div/app-train-list/div/div[5]/div/div[2]/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/p-dropdown/div/div[4]/div/ul/li[5]/span'
        browser.find_element_by_xpath(tatkal_lnk_object).click()
        time.sleep(1)
        browser.find_element_by_xpath(tatkal_object).click()
        time.sleep(1)
        falak_train = '//*[@id="check-availability"]'
        waitFor(falak_train)
        browser.find_element_by_id('check-availability').click()
        #_________________BookNowCode to be added_____________________________#

def fill_details(browser,name,age):
        waitFor(None,"psgn-name")
        name_object = browser.find_element_by_id("psgn-name")
        name_object.send_keys(name)
        age_object = browser.find_element_by_xpath('//*[@id="divMain"]/div/app-passenger-input/div[5]/form/div/div[1]/div[3]/div[1]/div/div[2]/app-passenger/div/div[1]/div[2]/input')
        age_object.send_keys(age)
        gender_object = browser.find_element_by_xpath('//*[@id="divMain"]/div/app-passenger-input/div[5]/form/div/div[1]/div[3]/div[1]/div/div[2]/app-passenger/div/div[1]/div[3]/select/option[2]')
        gender_object.click()


browser = login(browser,username,password,origin,destination,_date)
search_train(browser,origin,destination,_date)
fill_details(browser,name,age)


#for i in range(10):
#    _date.send_keys(Keys.BACKSPACE)
#_date.send_keys(date_of_journey)
#_date.send_keys(Keys.TAB,Keys.ARROW_DOWN,Keys.ARROW_DOWN,Keys.ARROW_DOWN,Keys.ARROW_DOWN,Keys.ARROW_DOWN,Keys.ARROW_DOWN,Keys.ARROW_DOWN,Keys.ARROW_DOWN,Keys.ARROW_DOWN)
#_date.send_keys(Keys.RETURN)
#time.sleep(3)
#check_avail=browser.find_element_by_xpath('//*[@id="check-availability"]')
#check_avail.click()
