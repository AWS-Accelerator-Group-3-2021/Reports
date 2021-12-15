import random, uuid, os
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

accessPasswords = []
for name in ['prakhar', 'yisian', 'ved', 'benjamin', 'john']:
    accessPasswords.append(name + os.getenv('PASS_EXTENSION'))

class Report:
    def __init__(self, reporter_name, add_info, datetime, measurement, address):
        self.reporter_name = reporter_name # Name of the person reporting
        self.add_info = add_info # Additional information about the report
        self.datetime = datetime # Date and time the report was made in string format
        self.measurement = measurement # What the measurement of the items was
        self.address = address # Address of the offender in question of the report
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
            'id': self.id
        }

    def convertFromJSON(givenJSON):
        return Report(givenJSON['reporter_name'], givenJSON['add_info'], givenJSON['datetime'], givenJSON['measurement'], givenJSON['address'])