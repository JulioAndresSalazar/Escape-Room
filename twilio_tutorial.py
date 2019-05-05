# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACd6362de7dba6479f2cd0b01e55d4ec71'
auth_token = 'a1b1330840e08969f997249832d0340a'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+16173156947',
                     to='+16172303789'
                 )

print(message.sid)