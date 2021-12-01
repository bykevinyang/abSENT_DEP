import smtplib
import yaml
from email.mime.text import MIMEText

from absentTeacher import AbsentTeacher
from time import sleep

class abSENTBot():
    def __init__(self, credentials="secrets.yml"):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        with open(credentials, 'r') as f:
            cfg = yaml.safe_load(f)
            self.email = cfg['email']
        self.server.login(self.email, cfg['password'])

    def send_text(self, recipient: str, message: str, subject: str):
        self.server.ehlo()  # Can be omitted
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = recipient
        
        text = msg.as_string()
        self.server.sendmail(self.email, recipient, text)
        sleep(1.5)
        
    def notify_absence(self, recipient: str, absent_teacher: AbsentTeacher):
        subject = "Absent Teacher!"
        message = f"{absent_teacher.first} {absent_teacher.last} is absent {absent_teacher.length}!"
        message += f"\n{absent_teacher.date}"
        message += f"\nNote:\n{absent_teacher.note}"

        self.send_text(recipient, message, subject)

    def welcome(self, recipient: str):
        self.server.ehlo()  # Can be omitted
        message = "abSENT is an SMS bot that will automatically text you if your teacher is absent"
        self.send_text(recipient, message, "Welcome to abSENT!")
        
        message = "To use abSENT, we first need to setup you up"
        message += "To do so, text 'setup' and your first and last name"
        message += "Example:"
        self.send_text(recipient, message, "")
        message = "setup Kevin Yang"
        self.send_text(recipient, message, "")

    def setup_account(self, recipient: str):
        self.server.ehlo()
        message = "Congratulations, you just created an abSENT account!"
        message += "\n We can now setup your schedule"
        message += "\nTo do so, text your blocks and teachers as so:"
        self.send_text(recipient, message, "")
        message = "\n<Block> <FirstName> <LastName>"
        self.send_text(recipient, message, "")

        message = "\nHere is an example:\nA John Doe"
        self.send_text(recipient, message, "")

        message = "You can do this one at a time, or all in one go:"
        message += "\nA John Doe"
        message += "\nB Mary Jane"
        self.send_text(recipient, message, "")

        message = "vs"
        self.send_text(recipient, message, "")

        message = "A John Doe"
        self.send_text(recipient, message, "")

        message = "B Mary Jane"
        self.send_text(recipient, message, "")
    
    def end_server(self):
        return self.server.quit()