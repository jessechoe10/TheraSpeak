# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import time

ALLMESSAGES = {}
MESSAGECOUNTS = {}


# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC13f9ba608877232776f01dfda847b07f"
auth_token = "1cd36ab6c7cf94402a49301f4fd0a531"
client = Client(account_sid, auth_token)

trial_number="+18553896103"

received_messages = client.messages.list(
    to=trial_number  # Your Twilio trial number
)

# Print received messages

for message in received_messages:
    if not ALLMESSAGES:
        ALLMESSAGES[message.from_]=[message.body]
        MESSAGECOUNTS[message.from_] = 1

    if message.from_ in ALLMESSAGES:
        ALLMESSAGES[message.from_].append(message.body)
        MESSAGECOUNTS[message.from_] += 1

    #print(f"From: {message.from_}")
    #print(f"To: {message.to}")
    #print(f"Body: {message.body}")
    #print(f"Date Sent: {message.date_sent}")
    #print()
start = time.process_time()
oldMessages = [text.body for text in received_messages]
while True:
    if ((start-time.process_time())*100) % 1 == 0:
        temp = [text.body for text in client.messages.list(to=trial_number)]
        if oldMessages != temp:
            print(temp[0])
            message_body = input("How would you like to respond? ")
            message = client.messages \
                .create(
                    body=message_body,
                    to="+17035059685",
                    from_="+18553896103"
            )
        oldMessages = temp
        continue


print(ALLMESSAGES)
