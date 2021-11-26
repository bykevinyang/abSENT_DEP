from dataclasses import dataclass

@dataclass
class textMessage:
    email: str
    date: str
    message: str
    carrier: str
    number: str

    def __init__(self, email, date, message):
        self.email = email
        self.date = date
        self.message = message
        self.number = self.email.split('@')[0]
        self.carrier = self.email.split('@')[1]

    def __str__(self):
        return f"{self.date}: {self.number}\n\t{self.message}"