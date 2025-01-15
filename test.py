from simplegmail import Gmail

gmail = Gmail()
print("Hello World")

# Unread messages in your inbox
# messages = gmail.get_messages()
# print("Unread messages in your inbox:")
# Starred messages
messages = gmail.get_starred_messages()
print("Starred messages:")

# ...and many more easy to use functions can be found in gmail.py!

# Print them out!
for message in messages:
    print("To: " + message.recipient)
    print("From: " + message.sender)
    print("Subject: " + message.subject)
    print("Date: " + message.date)
    print("Preview: " + message.snippet)

    print("Message Body: " + message.plain)  # or message.html