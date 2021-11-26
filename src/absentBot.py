import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class abSENTBot():
    def __init__(self, credentials="secrets.yml"):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        with open('secrets.yml', 'r') as f:
            cfg = yaml.safe_load(f)
            self.email = cfg['email']
        self.server.login(self.email, cfg['password'])

    def send_text(self, recipient: str, message: str):
        self.server.ehlo()  # Can be omitted
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = 'Received'

        msg.attach(MIMEText(message, 'plain'))
        
        text = msg.as_string()
        self.server.sendmail(self.email, recipient, text)
    
    def welcome(self, recipient: str):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = 'Welcome to abSENT Bot'
        
        message = "abSENT is an SMS bot that will automatically text you if your teacher is absent"
        
        msg.attach(MIMEText(message, 'plain'))
        
        text = msg.as_string()
        self.server.sendmail(self.email, recipient, text)

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = 'Welcome to abSENT Bot'
        message = "\nTo use abSENT, simply text Block LastName FirstName"
        message += "\nExample: \nA Doe John"

        msg.attach(MIMEText(message, 'plain'))
        
        text = msg.as_string()
        self.server.sendmail(self.email, recipient, text)

    def end_server(self):
        return self.server.quit()