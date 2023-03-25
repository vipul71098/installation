import smtplib
import sys
user_name = sys.argv[1]
user_pass = sys.argv[2]
user_email = sys.argv[3]
smtp_password=''
user = user_name.split('.')
sender = "<SENDER_EMAIL>"
receivers =[user_email]
message ="""From: From TESTER VAULT
To: To VAULT USER
Subject: VAULT CREDENTIALS 
Hlo %s 
This is a Vault email for your vault credentials
Vault Username : %s
Vault Password : %s
"""%(user[0],user_name,user_pass)
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    password =smtp_password
    server. login(sender,password)
    server.sendmail(sender, receivers, message)
    print("Successfully sent email for user :"+user_name)
except Exception as e:
    print(e)
