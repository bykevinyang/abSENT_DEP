from gmailText import gmailText
from absentBot import abSENTBot
import time

gmailTextTest = gmailText()
texterTest = abSENTBot()

print("abSENT Bot Started")
texterTest.welcome("6176868207@vtext.com")

while True:
    time.sleep(2)
    msgs = gmailTextTest.get_unread_texts()
    if msgs:
        for msg in msgs:
            print(msg)
            texterTest.send_text(msg.email, "Recieved: " + msg.message)
            print("Sent auto response")
            # print(f"Sent: Received: {msg.message}")