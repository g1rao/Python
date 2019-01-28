#Hello , This program is used to scrap the webpage without selenium
#Its purely based on frontend
#
# Author: Jeevan Rao T
#
import os
import sys
from bs4 import BeautifulSoup
import requests

try:
    q_id=sys.argv[1]
    url_actual=""+str(q_id)   #The url which you want to save
    print url_actual
    url="https://ttc.td.teradata.com/TestTools/Logon.cfm" #do modify program or-else specify redirected url when you access the actual url
    user="username"
    password="password"
    session=requests.Session()
    session.post(url,data={'UserName':user,'Pass':password})#make the data fields UserName and Pass varies depends on the page elements
    html=session.get(url_actual).content           # here you got entire page
    soup=BeautifulSoup(html,'html.parser')         # used html parser for parsing html 
    html_table=soup.findAll("table")               # to grab specific elements like table
    ind=0
    for index in range(len(html_table)):           # to extract table content 
        if "TestDetail/?Serial_Number=" in str(html_table[index]):
            ind=index
    soup=BeautifulSoup(str(html_table[ind]),'html.parser')
    f=open("output.txt",'w')
    #print dir(soup)i
    f.write(soup.text.encode('utf-8'))
    f.close()
    print soup.text.encode('utf-8')
except:
    sys.stdout.write("Exception occurred...!\n")
