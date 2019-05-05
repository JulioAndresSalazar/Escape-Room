# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACd6362de7dba6479f2cd0b01e55d4ec71'
auth_token = 'a1b1330840e08969f997249832d0340a'
client = Client(account_sid, auth_token)

def sendText(msg):
    message = client.messages \
                .create(
                     body=msg,
                     from_='+16173156947',
                     to='+17819540474' #Google Voice Number
                 )
    print(message.sid)
#Welcome Message
welcome_message = 'Welcome to ' + '"The Absent Minded Professor"' +  "! You are a group of mechanical engineers that have broken into the Chair of Mechanical Engineering's Office. The goal: find your diplomas in the next 30 minutes, hidden in the office. You'll need to piece together his journal to figure out where he keeps them. The problem is he's very scatterbrained. Good luck!"

hint = 'Have you found all the journal entries?'

sendText(hint)

'''Confused about what is a bookshelf 
Thought that color coded things were related
Thought that music box was related to the safe 
25 -5 riddle, they thought 20 
QR codes work well 
Thought that numbers were input to button 
Phone should not be allowed 
write "see BOOK" on bookshelf
They thought number answers were the number of times to push button
Add a post so we know that 
button vs QR code is confusing

'''