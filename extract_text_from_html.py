#Hi There
#This program is to extract text from html, but yet to be completed
#As of now it will extract the table content from html into output.txt
from bs4 import BeautifulSoup
f=open('file.html')
html=f.read()
f.close()
soup=BeautifulSoup(html,'html.parser')
html=soup.findAll("tabldde")
print html
soup=BeautifulSoup(str(html[2]),'html.parser')
f=open("output.txt",'w')
#print dir(soup)
f.write(soup.text.encode('utf-8'))
f.close()
~
