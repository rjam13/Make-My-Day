# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


def sms_alert(body, to):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    from_num = os.environ['TWILIO_PHONE_NUMBER']
    
    client = Client(account_sid, auth_token)
    message = client
                .messages
                .create(
                     body=body,
                     from_=from_num,
                     to=to
                 )


if __name__ == '__main__':
    sms_alert("Testing", "+13055102227")
    
