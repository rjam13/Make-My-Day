# source: https://www.youtube.com/watch?v=B1IsCbXp0uE
# https://freecarrierlookup.com/ phone number email extension look up

import email
import smtplib
from email.message import EmailMessage

TO_INDEX = 0
SUBJECT_INDEX = 1
BODY_INDEX = 2

def send_one(message):
    user = 'makemydayfiu@gmail.com'
    password = 'lsmkhllqxcktabnd'

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = user
    server.send_message(msg)

    server.quit

def send_many(messages):
    user = 'makemydayfiu@gmail.com'
    password = 'lsmkhllqxcktabnd'

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)

    for message in messages:
        msg = EmailMessage()
        msg.set_content(message[BODY_INDEX])
        msg['subject'] = message[SUBJECT_INDEX]
        msg['to'] = message[TO_INDEX]
        msg['from'] = user
        server.send_message(msg)

    server.quit

if __name__ == '__main__':
    message1 = ("rsflamehead@gmail.com", "Hello!", "This is a test message.")
    message2 = ("ryanshipman95@gmail.com", "Hello!", "This is a test message.")
    theList = [message1, message2]
    send_many(theList)

