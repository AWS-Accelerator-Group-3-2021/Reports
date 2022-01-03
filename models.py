import random, uuid, os, datetime, json
import requests
from logger import *
from dotenv import load_dotenv
load_dotenv()

def fileContent(fileName):
    with open(fileName, 'r') as f:
        f_content = f.read()
        return f_content

def generateAuthToken():
  letters_lst = ['a', 'e', 'w', 't', 'a', 'u', 'o', 'p', '2', '5', '6', '3', '8', '4']
  authTokenString = ''
  while len(authTokenString) < 10:
    authTokenString += random.choice(letters_lst)
  return authTokenString

def sendLoginAlertDiscordWebhookMessage(pwd):
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    username = pwd.split('@')[0]

    webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    webhook_data = {
        "username": "The Reports System",
        "embeds": [
            {
                "title": "Login Alert",
                "description": "User `{}` has logged into the system with their password.".format(username),
                "color": 16777215,
                "footer": {
                    "text": "This notification was sent to you by The Reports System." + " | " + now_str
                }
            }
        ]
    }
    result = requests.post(webhook_url, json=webhook_data)

    try:
        result.raise_for_status()
        print()
        print("Successfully sent login alert to Discord.")
        print()
    except requests.exceptions.HTTPError as err:
        print("Error sending login alert to Discord webhook: " + err)

settingsAvailable = ['loginAlertsEnabled', 'authTokenExpirationTime']

def safelyLoadSettings():
    ## Make settings file if it doesnt exist
      if not os.path.exists(os.path.join(os.getcwd(), 'config.txt')):
        with open(os.path.join(os.getcwd(), 'config.txt'), 'w') as f:
          f.write("{}")

      settings = json.load(open('config.txt', 'r'))
      
      if 'settings' not in settings:
        settings['settings'] = {}
        settings['settings']['loginAlertsEnabled'] = 'true'
        settings['settings']['authTokenExpirationTime'] = '86400'
        json.dump(settings, open('config.txt', 'w'))

      for setting in settingsAvailable:
        if setting not in settings['settings']:
          if setting == 'loginAlertsEnabled':
            settings['settings'][setting] = 'true'
          elif setting == 'authTokenExpirationTime':
            settings['settings'][setting] = '86400'
          json.dump(settings, open('config.txt', 'w'))

        return settings

accessPasswords = []
for name in ['prakhar', 'yisian', 'ved', 'benjamin', 'john']:
    accessPasswords.append(name + os.environ['PASS_EXTENSION'])

class Report:
    def __init__(self, reporter_name, add_info, datetime, measurement, address, clientInfo):
        self.reporter_name = reporter_name # Name of the person reporting
        self.add_info = add_info # Additional information about the report
        self.datetime = datetime # Date and time the report was made in string format
        self.measurement = measurement # What the measurement of the items was
        self.address = address # Address of the offender in question of the report
        self.clientInfo = clientInfo # Client info of the device in question of the report, for e.g iPhone 13 Pro Max, iOS 13.3, etc.
        self.id = str(uuid.uuid5()) # Unique ID of the report

    def __str__(self):
        return 'Report by %r' % self.reporter_name

    def convertedToJSON(self):
        return {
            'reporter_name': self.reporter_name,
            'add_info': self.add_info,
            'datetime': self.datetime,
            'measurement': self.measurement,
            'address': self.address,
            'clientInfo': self.clientInfo,
            'id': self.id
        }

    def convertFromJSON(givenJSON):
        return Report(givenJSON['reporter_name'], givenJSON['add_info'], givenJSON['datetime'], givenJSON['measurement'], givenJSON['address'], givenJSON['clientInfo'])