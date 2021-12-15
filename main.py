from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from models import *
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

validAuthTokens = json.loads(open('authTokens.txt').read())
loadedReports = json.loads(open('reports.txt').read())

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

@app.route('/session/<authToken>/list/meta/reports')
def getReports(authToken):
  isValid = False
  for timeKey in validAuthTokens:
    if validAuthTokens[timeKey] == authToken:
      isValid = True
  if not isValid:
    return "<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>"
  reports = loadedReports
  return jsonify(reports)

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
    return "<h1>Report not found.</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)