import requests
import hmac
import hashlib
import base64
import time
import urllib.parse
import pandas as pd
import sys

sys.path.append('config/')
import keys

api_url = "https://api.kraken.com"
api_key = keys.kraken_key
api_sec = keys.kraken_secret

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req.json()
while True:
  resp = kraken_request('/0/private/DepositStatus', {
          "nonce": str(int(1000 * time.time())),
          #"asset": 'MINA'
      }, api_key, api_sec)
  
  print(pd.DataFrame(resp['result']))
