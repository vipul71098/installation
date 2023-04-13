import smtplib
import sys
import os
from dotenv import load_dotenv
load_dotenv()
APP_PASSWORD = os.getenv("APP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
user_name = sys.argv[1]
user_pass = sys.argv[2]
user_email = sys.argv[3]

user = user_name.split('.')
Username=user[0].capitalize()
receivers =[user_email]
message ="""From: %s
To: %s
Subject: VAULT CREDENTIALS 
Hi %s

Following are the credentials for accessing the vault, please be sure to save these as they cannot be changed in the future.
Username: %s
Password: %s

Use them to access the vault here, https://vault.thewitslab.com/. The credentials are supposed to remain CONFIDENTIAL as any potential breach or crash caused by these credentials will lead back to you. For any further assistance or information, please do not hesitate to contact us or post on WIL-Dev-Support space.

Regards,
DevOps Team
"""%(SENDER_EMAIL,user_email,Username,user_name,user_pass)
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    password =APP_PASSWORD
    server. login(SENDER_EMAIL,password)
    server.sendmail(SENDER_EMAIL, receivers, message)
    print(" \n Successfully sent email for user :"+user_name+"\n")
except Exception as e:
    print(e)
