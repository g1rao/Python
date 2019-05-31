import pexpect
import time
username="root"
password="password"
for i in range(0):
    if len(str(i))==1:
        chr="0"+str(i)
    else:
        chr=str(i)
    host=host+chr
    print host
#    child=pexpect.spawn("ssh-id -i /root/.ssh/id_rsa.pub -o StrictHostKeyChecking=no %s@%s"%(username,host))
    child=pexpect.spawn("ssh -o StrictHostKeyChecking=no %s@%s"%(username,host))
#    time.sleep(2)
#    child.sendline("useradd -m nagios; (echo nagios; echo nagios) | passwd nagios ")
    time.sleep(3)
    child.sendline("echo 'nagios ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers")


import pexpect
import time
username="root"
password="Beagl342"
for i in range(0,0):
    if len(str(i))==1:
        chr="0"+str(i)
    else:
        chr=str(i)
    host="ft10"+chr+".labs.teradata.com"
    print host
    child=pexpect.spawn("ssh-copy-id -i /root/.ssh/id_rsa.pub -o StrictHostKeyChecking=no %s@%s"%(username,host))
    time.sleep(2)
    child.sendline(password)
    time.sleep(5)
    child.sendline("chmod 700 /root/.ssh/authorized_keys")
    child.sendline("mkdir /root/bcd")
    #child.close()


import pexpect
import time
username="ubuntu"
password="ubuntu"
host="localhost"
child=pexpect.spawn("ssh-copy-id -i /home/ubuntu/.ssh/id_rsa.pub  -o StrictHostKeyChecking=yes %s@%s"%(username,host))
time.sleep(2)
print
child.sendline("yes")
time.sleep(2)
child.sendline(password)
time.sleep(3)
child.sendline("chmod 700 /ubuntu/.ssh/authorized_keys")
child.sendline("mkdir /home/ubuntu/Python/sandbox/abcdddd")
child.close()
