import os
import sys
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode
from gmailAuth import gmail_authenticate, search_messages

# for debugging:
import pprint
pp = pprint.PrettyPrinter(indent=4)

def mark_as_read(service, msg_id):
    return service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

def mask_as_unread(service, msg_id):
    return service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds': ['UNREAD']}).execute()

def read_email(service, message):
    emailFrom = None
    emailTo = None
    emailSubject = None
    date = None
    textMsg = None

    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    emailMimetype = payload.get("mimeType")
    
    # Grab basic email data: From, To, Subject, Date
    if headers:
        for header in headers:
            if header['name'] == 'Subject':
                emailSubject = header['value']
            elif header['name'] == 'From':
                emailFrom = header['value']
            elif header['name'] == 'To':
                emailTo = header['value']
            elif header['name'] == 'Date':
                date = header['value']
    
    try:
        number_length = len(emailFrom.split('@')[0])
        number = int(emailFrom.split('@')[0])
        # If the email is from a number, parse the msg below
    except ValueError:
        return None

    if number_length == 10: # Make sure it is a phone number
        parts = payload.get("parts")
        if parts:
            if len(parts) >= 1:
                part = parts[0]
                partHeader = part.get("headers")
                for header in partHeader:
                    if header['name'] == 'Content-Type':
                        # Grabbing content information: MIME type, Encoding, Name
                        contentTypes = header['value']
                        contentMimeType = contentTypes.split(';')[0]
                        if contentMimeType == 'text/plain':
                            contentEncoding = contentTypes.split(';')[1].split('=')[1]
                            contentName = contentTypes.split(';')[2].split('=')[1]

                    if contentMimeType == 'text/plain':
                        body = part.get("body")
                        # Grab AttachmentID and Size 
                        if body:
                            attachmentID = body.get("attachmentId")
                            size = body.get('size')
                    
                if attachmentID:
                    # Grab the attachment
                    attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attachmentID).execute()
                    data = attachment.get('data')
                    data = urlsafe_b64decode(data)
                    textMsg = data.decode()
                    # Grabbing text msg

        return emailFrom, emailTo, emailSubject, date, textMsg, message['id']

# def watchInbox(service):
#     service.users().watch(userId='me').execute()
#     https://gmail.googleapis.com/gmail/v1/users/{userId}/watch


import time 

# For scripting
if __name__ == "__main__":
    service = gmail_authenticate()
    # get emails that match the query you specify from the command lines

    # while True:
    #     time.sleep(5)
    #     results = search_messages(service, query="from:6176868207")

    #     for msg in results:

    results = search_messages(service, query="is:unread")
    # for each email matched, read it (output plain/text to console & save HTML and attachments)

    for msg in results:
        email = read_email(service, msg)
        if email:
            print("From: " + email[0])
            print("To: " + email[1])
            print("Subject: " + email[2])
            print("Date: " + email[3])
            print("Message: " + email[4])
            print("-"*50)
            mark_as_read(service, email[5])
