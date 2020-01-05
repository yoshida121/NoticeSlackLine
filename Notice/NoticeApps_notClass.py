import requests
import os
import json

class Notify():
    default_api_url = {
        "slack": "https://hooks.slack.com/services/",
        "line": 'https://notify-api.line.me/api/notify'
    }
    
    def __init__(self, app="slack", token="./token.txt"):
        self.app = app
        
        if os.path.isfile(token): # tokenがファイル形式のとき
            with open(token) as token_file: # JSON形式だと対応していないかも
                self.token = token_file.read()
        else:
            self.token = token
        
    def _send_line(self, message):
        payload = {"message": message}
        headers = {"Authorization": 'Bearer ' + self.token}
        requests.post(self.default_api_url["line"], data=payload, headers=headers)
        
    def _send_slack(self, message):
        if self.token.startswith(self.default_api_url["slack"]):
            URL = self.token
        else:
            URL = self.default_api_url["slack"] + self.token
        print(URL)
        payload = {
            "text": message,
#             "icon_emoji": ":heart" # アイコンを変更したいときに設定
        }
        
        data = json.dumps(payload)
        requests.post(URL, data)
    
    def notice(self, message="Processes completed."):
        if self.app == "slack":
            self._send_slack(message)
        elif self.app == "line":
            self._send_line(message)