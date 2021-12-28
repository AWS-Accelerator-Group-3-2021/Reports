import requests, os, json
from dotenv import load_dotenv
load_dotenv()

class Logger:

    ## Make static log function
    @staticmethod
    def log(text, type='normal'):
        print(text)

        if type != 'normal' and type != 'error':
            return "Type is invalid. Type can only be `normal` or `error`."

        log = {
            'type': type,
            'text': text,
            'clientName': os.environ['CLIENT_NAME']
        }

        result = requests.post("{}/newLog".format(os.environ['LOGGER_URL']), json=log, headers={'Content-Type': 'application/json', 'LogsAccessCode': os.environ['LOGS_ACCESS_CODE']})

        try:
            result.raise_for_status()
            if result.status_code != 200:
                print("Logger returned error: {}".format(result.text))
            else:
                pass
        except requests.exceptions.HTTPError as e:
            print("Error in sending Log message to Logger: {}".format(e))

## Logger.log("This is a normal log message", "normal")
## Logger.log("This is an error log message", "error")

### Requirements:
### - Logger URL
### - Logs Access Code
### - Client Name

