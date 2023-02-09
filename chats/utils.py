import json
import requests
from messenger.local_settings import API_KEY


def publish_message_to_websocket(message, channel="chat"):
    command = {
        "method": "publish",
        "params": {
            "channel": channel,
            "data": message
        }
    }

    api_key = API_KEY
    data = json.dumps(command)

    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + api_key}
    requests.post("http://localhost:8000/api", data=data, headers=headers)


