from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from models import *
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

validAuthTokens = json.loads(open('authTokens.txt').read())

@app.route('/')
def index():
    return fileContent('index.html')

@app.route('/passwordCheck', methods=['POST'])
def passwordAuth():
  if request.headers['ReportsAccessCode'] == 'AWSGroup3-POCwej69' and request.headers['Content-Type'] == 'application/json':
    if request.json['data'] == 'prakhar@AWS3!2021':
      newToken = generateAuthToken()
      validAuthTokens[datetime.now().strftime('%H:%M:%S')] = newToken
      json.dump(validAuthTokens, open('authTokens.txt', 'w'))
      # print(validAuthTokens)
      return 'Authorisation successful! Temp auth token: {}'.format(newToken)
    else:
      return 'Authorisation failed!'
  else:
    return 'Authorisation failed! Incorrect data bank access code or content-type.'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)