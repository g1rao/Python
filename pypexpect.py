#Hello...!
#This program to use python pexpect module to ssh remote machine
#
# Author-> @Jeevan Rao T@
import pexpect
import time
username="root"
password="password"
for i in range(0):
    if len(str(i))==1:
        chr="0"+str(i)
    else:
        chr=str(i)
    host="0"+chr+".com" # you need to specify the host here
    print host
#    child=pexpect.spawn("ssh-id -i /root/.ssh/id_rsa.pub -o StrictHostKeyChecking=no %s@%s"%(username,host))
    child=pexpect.spawn("ssh -o StrictHostKeyChecking=no %s@%s"%(username,host))
#    time.sleep(2)
#    child.sendline("useradd -m nagios; (echo nagios; echo nagios) | passwd nagios ")
    time.sleep(3)
    child.sendline("echo 'nagios ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers")

