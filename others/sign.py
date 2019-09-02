import time
import json
import hashlib
import copy
import random
import string
from requests import request


def get_sign(param, body, app_secret):
    sorted_params = sorted(param.items(), key=lambda x: x[0])
    encodestring = secret
    for k, v in sorted_params:
        encodestring += (k + str(v))

    encodestring += (body + app_secret)

    m = hashlib.md5()
    m.update(encodestring.encode('utf-8'))
    sign = m.hexdigest()

    # print('签名前：' + encodestring)
    # print('签名后：' + sign)

    return sign


def genRandomString(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))


system = 'operation-platform'
secret = '6g7srQ73QatzQrFx'

base_params = {
    'system': system,
    'timestamp': str(int(time.time()) * 1000)
}

getUserInfoRequestURL = 'https://t-oauth.vistel.cn/user/getUserInfo'
params = copy.deepcopy(base_params)
params['id'] = str(30001)
params['sign'] = get_sign(params, '', secret)

response = request('GET', getUserInfoRequestURL, params=params)
print(response.json())

addUserInfoRequestURL = 'https://t-oauth.vistel.cn/user/'
headers = {"Content-Type": "application/json;charset=utf-8"}
payload = {
    "username": "just_" + genRandomString(),
    "password": "qwerty",
    "gender": "M",
    "phone": "18578437843",
    "system": system
}
params = copy.deepcopy(base_params)
params['sign'] = get_sign(params, json.dumps(payload), secret)
response = request('POST', addUserInfoRequestURL, params=params, data=json.dumps(payload), headers=headers)
print(response.json())


