from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from models import *
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

validAuthTokens = {}
with open('authTokens.txt', 'r') as f:
  validAuthTokens = json.load(f)

loadedReports = json.load(open('reports.txt'))

#### EXAMPLE REPORT:
#### {
####   "id": "<UUID STRING>" : {
######   "reporter_name": "<STRING>",
######   "add_info": "<STRING>",
######   "datetime": "<DATETIME STRING>",
######   "measurement": "<FLOAT>",
######   "address": "<STRING>",
####   }
#### }

@app.route('/')
def index():
    return fileContent('index.html')

@app.route('/passwordCheck', methods=['POST'])
def passwordAuth():
  if request.headers['ReportsAccessCode'] == 'AWSGroup3-POCwej69' and request.headers['Content-Type'] == 'application/json':
    print(request.json['data'])
    if request.json['data'] in accessPasswords:
      newToken = generateAuthToken()
      validAuthTokens[datetime.now().strftime('%H:%M:%S')] = newToken
      json.dump(validAuthTokens, open('authTokens.txt', 'w'))
      # print(validAuthTokens)
      return 'Authorisation successful! Temp auth token: {}'.format(newToken)
    else:
      return 'Authorisation failed!'
  else:
    return 'Authorisation failed! Incorrect data bank access code or content-type.'

@app.route('/session/<authToken>/list')
def showData(authToken):
  isValid = False
  print(validAuthTokens)
  for timeKey in validAuthTokens:
    if validAuthTokens[timeKey] == authToken:
      isValid = True
  if not isValid:
    return "<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>"
  return fileContent('list.html')

@app.route('/session/<authToken>/list/meta/report/<reportID>')
def getReports(authToken, reportID):
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

@app.route('/session/<authToken>/list/report/<reportID>')
def getIndivReport(authToken, reportID):
  isValid = False
  for timeKey in validAuthTokens:
    if validAuthTokens[timeKey] == authToken:
      isValid = True
  if not isValid:
    return "<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>"
  if reportID in loadedReports:
    return jsonify(loadedReports[reportID])
  else:
    return "<h1>Report not found. Please check the report ID and try again</h1>"


# ASSET FILES
@app.route('/assets/home')
def home():
  return fileContent('home.js')

@app.route('/assets/list')
def list():
  return fileContent('list.js')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)