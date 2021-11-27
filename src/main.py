from absentTeacher import AbsentTeacher
from gmailText import gmailText
from absentBot import abSENTBot
import time

gmailTextTest = gmailText()
texterTest = abSENTBot()

print("abSENT Bot Started")
# texterTest.send_text("6176868207@vzwpix.com", "Testing if Absent Bot Works", "Hello There!")
texterTest.welcome("6176868207@vtext.com")

exampleTeach = AbsentTeacher("Kevin", "Yang", "3 Blocks", "A BLock", "Have fun!")
# texterTest.notify_absence("6176868207@vzwpix.com", exampleTeach)
# print(f"Sent absence message {exampleTeach}")