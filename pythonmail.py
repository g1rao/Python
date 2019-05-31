import smtplib
con="test"
mail = smtplib.SMTP("smtp.gmail.com",587)
mail.starttls()
mail.ehlo()
mail.login("itwilntwrk@gmail.com","")
mail.sendmail("jeevanrao.iiit@gmail.com","jeevan.t@tcs.com",con)
mail.close()


import pdb
pdb.set_trace()
SERVER = "mail.tcs.com"
FROM = "jeevan.t@tcs.com"
TO = ["jeevan.t@tcs.com"] # must be a list

SUBJECT = "Subject"
TEXT = "Your Text"

# Prepare actual message
message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

# Send the mail
import smtplib
server = smtplib.SMTP(SERVER)
server.login("jeevan.t@tcs.com", "password")
server.sendmail(FROM, TO, message)
server.quit()
