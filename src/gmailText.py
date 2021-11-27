import os

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode

# struct for text message
from textMessage import textMessage

# Helper functions
from helper import dateConvert

# GCP API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

class gmailText():
    def __init__(self, token="token.pickle", credential="credentials.json"):
        self.token = token
        self.credential = credential
        self.SCOPES = ['https://mail.google.com/']
        self.service = self.gmail_authenticate()

    def get_unread_texts(self):
        texts = [ ]
        results = self.search_messages(query="is:unread")
        if results:
            for result in results:
                email = self.read_email(result)
                if email:
                    txt = textMessage(email[0], email[3], email[4])
                    texts.append(txt) 
                    self.mark_as_read(email[5])
        return texts

    def read_unread_texts(self):
        unread_texts = self.get_unread_texts()
        return unread_texts
        
    def gmail_authenticate(self):
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists(self.token):
            with open(self.token, "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credential, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    def search_messages(self, query):
        result = self.service.users().messages().list(userId='me',q=query).execute()
        messages = [ ]
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages

    def mark_as_read(self, msg_id):
        return self.service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

    def mask_as_unread(self, msg_id):
        return self.service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds': ['UNREAD']}).execute()

    def read_email(self, message):
        emailFrom = None
        emailTo = None
        emailSubject = None
        date = None
        textMsg = None

        msg = self.service.users().messages().get(userId='me', id=message['id'], format='full').execute()
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
                    raw_date = header['value']
                    date = dateConvert(raw_date)
        
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
                        attachment = self.service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attachmentID).execute()
                        data = attachment.get('data')
                        data = urlsafe_b64decode(data)
                        textMsg = data.decode()
                        # Grabbing text msg

            return emailFrom, emailTo, emailSubject, date, textMsg, message['id']
        return None
    
    def read_from(self, email, unread=True):
        texts = [ ]
        query = f"from:{email}"
        if unread:
            query += "is:unread"
 
        print(query)
        results = self.search_messages(query)
        if results:
            for result in results:
                email = self.read_email(result)
                if email:
                    txt = textMessage(email[0], email[3], email[4])
                    texts.append(txt)
        return texts
        