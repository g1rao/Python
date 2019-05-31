import os
import sys
from bs4 import BeautifulSoup
import requests

try:
    #q_id=sys.argv[1]
    url_actual="http:/<url>"
    print url_actual
    url="https://<login url>"
    user=""
    password=""
    session=requests.Session()
    session.post(url,data={'UserName':user,'Pass':password})
    html=session.get(url_actual).content
    f=open("index.xls",'w')
    f.write(html)
    f.close()
    """soup=BeautifulSoup(html,'html.parser')
    html_table=soup.findAll("table")
    ind=0
    for index in range(len(html_table)):
        if "TestDetail/?Serial_Number=" in str(html_table[index]):
            ind=index
    soup=BeautifulSoup(str(html_table[ind]),'html.parser')
    f=open("output.txt",'w')
    #print dir(soup)i
    f.write(soup.text.encode('utf-8'))
    f.close()
    print soup.text.encode('utf-8')
    """
except Exception as e:
    print e
    sys.stdout.write("Exception occurred...!\n")
