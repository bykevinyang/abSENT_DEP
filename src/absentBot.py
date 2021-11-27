import smtplib
import yaml
from email.mime.text import MIMEText
from email.message import EmailMessage
from absentTeacher import AbsentTeacher

class abSENTBot():
    def __init__(self, credentials="secrets.yml"):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        with open('secrets.yml', 'r') as f:
            cfg = yaml.safe_load(f)
            self.email = cfg['email']
        self.server.login(self.email, cfg['password'])

    def send_text(self, recipient: str, message: str, subject: str):
        self.server.ehlo()  # Can be omitted
        msg = MIMEText("\r\n\r\n" + message)
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = recipient
        
        text = msg.as_string()
        self.server.sendmail(self.email, recipient, text)

    def notify_absence(self, recipient: str, absent_teacher: AbsentTeacher):
        subject = f"Absent Teacher!"
        message = f"{absent_teacher.first} {absent_teacher.last} is absent {absent_teacher.length}!"
        message += f"\n{absent_teacher.date}"
        message += f"\nNote:\n{absent_teacher.note}"

        self.send_text(recipient, message, subject)

    def welcome(self, recipient: str):
        self.server.ehlo()  # Can be omitted
        message = "abSENT is an SMS bot that will automatically text you if your teacher is absent"
        message += "\nTo use abSENT, send the following text to the bot:"
        message += "\nabSENT <Block> <FirstName> <LastName>"
        message += "\nHere is an example:\n\tA John Doe"
        self.send_text(recipient, message, "Welcome to abSENT!")

    def end_server(self):
        return self.server.quit()