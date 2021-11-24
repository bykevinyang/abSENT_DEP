from absence import absence
import schoolopy
import yaml
import webbrowser as wb
from datetime import date

with open('secrets.yml', 'r') as f:
    cfg = yaml.safe_load(f)

absent = absence(cfg['key'], cfg['secret'])

absent.filter_absences(date = date.today())

# sc = schoolopy.Schoology(schoolopy.Auth(cfg['key'], cfg['secret']))
# sc.limit = 10  # Only retrieve 10 objects max

# print('Your name is %s' % sc.get_me().name_display)
# for update in sc.get_feed():
#     user = sc.get_user(update.uid)
#     if user.name_display == "Tracy Connolly":
#         print(update.body)
# print(f"Your name is {sc.get_me().name_display()}")

# for update in sc.get_feed():
#     user = sc.get_user(update.uid)
#     print("By: " + user.name_display())
#     print(update.body[:40].replace('\r\n', ' ').replace('\n', ' ') + '...')
#     print('%d likes\n' % update.likes)