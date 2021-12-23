from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from models import *
import json, os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

validAuthTokens = {}
loadedReports = {}

## Make auth tokens file if it doesnt exist
if not os.path.exists(os.path.join(os.getcwd(), 'authTokens.txt')):
  with open(os.path.join(os.getcwd(), 'authTokens.txt'), 'w') as f:
    f.write("{}")

with open('authTokens.txt', 'r') as f:
  validAuthTokens = json.load(f)

def expireAuthTokens():
  global validAuthTokens
  for timeCreated in list(validAuthTokens):
    # Print out size of validAuthTokens
    timeCreatedDateObj = datetime.strptime(timeCreated, '%Y-%m-%d %H:%M:%S.%f')
    if (datetime.now() - timeCreatedDateObj).total_seconds() > 86400:
      del validAuthTokens[timeCreated]
      json.dump(validAuthTokens, open('authTokens.txt', 'w'))

## Make reports file if it doesnt exist
if not os.path.exists(os.path.join(os.getcwd(), 'reports.txt')):
  with open(os.path.join(os.getcwd(), 'reports.txt'), 'w') as f:
    f.write("{}")

loadedReports = json.load(open('reports.txt'))

#### EXAMPLE REPORT:
#### {
####   "id": "<UUID STRING>" : {
######   "reporter_name": "<STRING>",
######   "add_info": "<STRING>",
######   "datetime": "<DATETIME STRING>",
######   "measurement": "<FLOAT>",
######   "address": "<STRING>",
######   "clientInfo": "<STRING>"
####   }
#### }

@app.route('/')
def index():
    return fileContent('index.html')

@app.route('/passwordCheck', methods=['POST'])
def passwordAuth():
  if request.headers['ReportsAccessCode'] == os.environ['SERVER_ACCESS_CODE'] and request.headers['Content-Type'] == 'application/json':
    if request.json['data'] in accessPasswords:
      newToken = generateAuthToken()
      validAuthTokens[datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")] = newToken
      json.dump(validAuthTokens, open('authTokens.txt', 'w'))
      # print(validAuthTokens)
      return 'Authorisation successful! Temp auth token: {}'.format(newToken)
    else:
      return 'Authorisation failed!'
  else:
    return 'Authorisation failed! Incorrect reports access code or content-type.'

@app.route('/session/<authToken>/list')
def showData(authToken):
  expireAuthTokens()
  isValid = False
  for timeKey in validAuthTokens:
    if validAuthTokens[timeKey] == authToken:
      isValid = True
  if not isValid:
    return "<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>"
  return fileContent('list.html')

@app.route('/newReport', methods=['POST'])
def newReport():
  if ('ReportsAccessCode' not in request.headers) or ('Content-Type' not in request.headers):
    return "ReportsAccessCode header or Content-Type header was not present in request. Request rejected."
  if request.headers['ReportsAccessCode'] == os.environ['SERVER_ACCESS_CODE'] and request.headers['Content-Type'] == 'application/json':
    newReportData = request.json['data']
    if newReportData['id'] in loadedReports:
      return 'Report already exists! Please use the update report endpoint to update the report.'
    else:
      for key in ['id', 'reporter_name', 'add_info', 'datetime', 'measurement', 'address', 'clientInfo']:
        if key not in newReportData:
          return 'Invalid report data. Missing key: {}'.format(key)

      loadedReports[newReportData['id']] = newReportData
      json.dump(loadedReports, open('reports.txt', 'w'))
      return 'Report successfully added!'
  else:
    return 'Authorisation failed! Incorrect reports access code or content-type.'

@app.route('/updateReport', methods=['POST'])
def updateReport():
  if ('ReportsAccessCode' not in request.headers) or ('Content-Type' not in request.headers):
    return "ReportsAccessCode header or Content-Type header was not present in request. Request rejected."
  if request.headers['ReportsAccessCode'] == os.environ['SERVER_ACCESS_CODE'] and request.headers['Content-Type'] == 'application/json':
    newReportData = request.json['data']
    if newReportData['id'] not in loadedReports:
      return "No such report exists in server. To make a new report, please use the new report endpoint."
    else:
      for key in ['id', 'reporter_name', 'add_info', 'datetime', 'measurement', 'address', 'clientInfo']:
        if key not in newReportData:
          return 'Invalid report data. Missing key: {}'.format(key)

      reportID = newReportData.pop('id')
      loadedReports[reportID] = newReportData
      return "Report successfully updated!"
  else:
    return 'Authorisation failed! Incorrect reports access code or content-type.'

@app.route('/deleteReport', methods=['POST'])
def deleteReport():
  if ('ReportsAccessCode' not in request.headers) or ('Content-Type' not in request.headers):
    return "ReportsAccessCode header or Content-Type header was not present in request. Request rejected."
  if request.headers['ReportsAccessCode'] == os.environ['SERVER_ACCESS_CODE'] and request.headers['Content-Type'] == 'application/json':
    if 'id' not in request.json['data']:
      return "Invalid request. No report ID was provided."
    reportID = request.json['data']['id']
    if reportID not in loadedReports:
      return "No such report exists in server. To make a new report, please use the new report endpoint."
    else:
      loadedReports.pop(reportID)
      json.dump(loadedReports, open('reports.txt', 'w'))
      return "Report successfully deleted!"
  else:
    return 'Authorisation failed! Incorrect reports access code or content-type.'
    

#### START OF META DATA REQUESTS

@app.route('/session/<authToken>/list/meta/report/<reportID>')
def getReports(authToken, reportID):
  expireAuthTokens()
  isValid = False
  for timeKey in validAuthTokens:
    if validAuthTokens[timeKey] == authToken:
      isValid = True
  if not isValid:
    return "<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>"
  if reportID not in loadedReports:
    return "<h1>Report not found. Please check the report ID and try again.</h1>"
  return jsonify(loadedReports[reportID])

@app.route('/session/<authToken>/list/meta/reportIDs')
def getIDs(authToken):
  expireAuthTokens()
  isValid = False
  for timeKey in validAuthTokens:
    if validAuthTokens[timeKey] == authToken:
      isValid = True
  if not isValid:
    return "<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>"
  reportIDs = []
  for reportID in loadedReports:
    reportIDs.append(reportID)
  return jsonify(reportIDs)

#### END OF META DATA REQUESTS

@app.route('/session/<authToken>/list/report/<reportID>')
def getIndivReport(authToken, reportID):
  expireAuthTokens()
  isValid = False
  for timeKey in validAuthTokens:
    if validAuthTokens[timeKey] == authToken:
      isValid = True
  if not isValid:
    return "<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>"
  if reportID in loadedReports:
    return fileContent('showReport.html')
  else:
    return "<h1>Report not found. Please check the report ID and try again</h1>"


# ASSET FILES
@app.route('/assets/home')
def home():
  return fileContent('home.js')

@app.route('/assets/list')
def listJS():
  return fileContent('list.js')

@app.route('/assets/showReport')
def showReport():
  return fileContent('showReport.js')

# ADMIN COMMANDS
@app.route('/<adminPass>/clearTokens')
def clearTokens(adminPass):
  global validAuthTokens
  if adminPass == os.environ['ADMIN_PASS']:
    validAuthTokens = {}
    json.dump(validAuthTokens, open('authTokens.txt', 'w'))
    return 'Tokens cleared!'
  else:
    return '<h1>Invalid admin password. Please try again.</h1>'

@app.route('/<adminPass>/clearReports')
def clearReports(adminPass):
  global loadedReports
  if adminPass == os.environ['ADMIN_PASS']:
    loadedReports = {}
    json.dump(loadedReports, open('reports.txt', 'w'))
    return 'Reports cleared!'
  else:
    return '<h1>Invalid admin password. Please try again.</h1>'

@app.route('/<adminPass>/loadDemoReports')
def loadDemoReports(adminPass):
  global loadedReports
  if adminPass == os.environ['ADMIN_PASS']:
    loadedReports = json.load(open('demo_reports.txt'))
    json.dump(loadedReports, open('reports.txt', 'w'))
    return 'Demo reports loaded!'
  else:
    return '<h1>Invalid admin password. Please try again.</h1>'

@app.route('/<adminPass>/reloadDataFiles')
def reloadDataFiles(adminPass):
  global loadedReports
  global validAuthTokens
  if adminPass == os.environ['ADMIN_PASS']:
    try:
      loadedReports = json.load(open('reports.txt'))
      validAuthTokens = json.load(open('authTokens.txt'))
    except:
      # Create reports file
      if not os.path.exists(os.path.join(os.getcwd(), 'reports.txt')):
        with open(os.path.join(os.getcwd(), 'reports.txt'), 'w') as f:
          f.write("{}")

      # Create auth tokens file
      if not os.path.exists(os.path.join(os.getcwd(), 'authTokens.txt')):
        with open(os.path.join(os.getcwd(), 'authTokens.txt'), 'w') as f:
          f.write("{}")

      loadedReports = json.load(open('reports.txt'))
      validAuthTokens = json.load(open('authTokens.txt'))
    return 'Data files reloaded!'
  else:
    return '<h1>Invalid admin password. Please try again.</h1>'

# MISCELLANEOUS COMMANDS
@app.route('/version')
def version():
  return """
  <h1>The Reports System</h1>
  <h3>Version: {}</h13>
  <h3>{}</h3>
  """.format(os.environ['VERSION'], "© 2021 The AWS Accelerator Group 3 2021 Singapore. All rights reserved.")

@app.route('/ping')
def ping():
  return "Pong! Version: {}".format(os.environ['VERSION'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)