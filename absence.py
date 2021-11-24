from absentTeacher import AbsentTeacher
import schoolopy
import yaml
import webbrowser as wb
import json
from datetime import date

class absence:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.sc = schoolopy.Schoology(schoolopy.Auth(self.key, self.secret))
        self.sc.limit = 10

    def get_feed(self, teacher="Tracy Connolly"):
        feed = []
        for update in self.sc.get_feed():
            user = self.sc.get_user(update.uid)
            if user.name_display == teacher:
                feed.append(update.body)
        return feed

    def get_absences_table(self, date: date):
        feed = self.get_feed()
        current_table = None

        for update in feed:
            text = update.split("\n")
                # Table has historically had date on 4th column, used to differentiate between update and actual attendance table
            if len(text) > 4:          
                if text[3] == str(date.strftime("%m/%d/%Y")):
                    current_table = update

        return current_table
    
    def filter_absences(self, date: date):
        absences = []

        raw = self.get_absences_table(date)
        if raw is None:
            return None
        else:
            table = raw.split("\n\n\n")
            for row in table:
                raw_entry = row.split("\n")
                if raw_entry[0] == "":
                    raw_entry.pop(0)
                if len(raw_entry) == 5:
                    entry = AbsentTeacher(raw_entry[0], raw_entry[1], raw_entry[2], raw_entry[3], raw_entry[4])
                elif len(raw_entry) == 4:
                    entry = AbsentTeacher(raw_entry[0], raw_entry[1], raw_entry[2],  raw_entry[3], "None")
                print(entry)
                absences.append(entry)

        return absences

    def __str__(self):
        return "{} is absent because {}".format(self.name, self.reason)