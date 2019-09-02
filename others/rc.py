import json
import time

from requests import request

payload = {
    "action": "UserDetailQuery",
    "header": {
        "userId": "6B07E2D28B5A4E9EB82B4AA3D2B79B66",
        "timeStamp":  str(int(time.time())),
        "accessToken": "6723EA4478664C9CB58880F2B11320EB"
    },
    "body": {
    }
}

print(json.dumps(payload))

getUserInfoRequestURL = 'http://telemedicine.pumch.cn/IHPService'

response = request('POST', getUserInfoRequestURL, data=json.dumps(payload))
print(response.json())



