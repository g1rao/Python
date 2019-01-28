#Hello There...!
#This is the basic program to explore popen from os module
# Author-> @Jeevan Rao T@

from os import popen
l=[]
for i in range(1,26):
	if len(str(i))==1:
		chr="0"+str(i)
	else:
		chr=str(i)
	l.append("10"+chr+".ls.ta.com")
string="""
define host{
        use                     sandbox-pipeline            ; Name of host template to use
        host_name               %s
        alias                   %s 
        address                 %s 
        }

"""
f=open("sand.cfg","a")
for i in l:
    k=popen("host "+i).read().split(" ")
    host,ip=k[0].strip(),k[-1].strip()
    alias=host.split(".")[0]
    f=open("sand.cfg","a")
    f.write(string%(host,alias,ip))
    print string%(host,alias,ip)
f.close()
