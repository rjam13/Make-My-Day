# source: https://www.youtube.com/watch?v=B1IsCbXp0uE
# https://freecarrierlookup.com/ phone number email extension look up

import email
import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    user = 'makemydayfiu@gmail.com'
    password = 'lsmkhllqxcktabnd'

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = user

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit

if __name__ == '__main__':
    email_alert("Testing", "hello world", "7864146304@tmomail.net")
    # email("Testing", "hello world", "rmara020@fiu.edu")

