import requests, hmac, hashlib, base64, time, urllib.parse, sys
import pandas as pd

sys.path.append('config/')
import config

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def kraken_request(uri_path, data):
    headers = {}
    headers['API-Key'] = config.kraken_key
    headers['API-Sign'] = get_kraken_signature(uri_path, data, config.kraken_secret)
    req = requests.post((config.url + uri_path), headers=headers, data=data)
    return req.json()

dfOriginal = ''
counter = 0

while True:
    print(f"Starting loop...\nLoop has run {counter} times.\nSending Request.")
    try:
        resp = kraken_request(config.endpoint, {
            "nonce": str(int(1000 * time.time())),
        })
        print('Request sent succesfully')
        dfNew = dfOriginal
        dfOriginal = pd.DataFrame(resp['result'])
        print('Dataframes setup correctly')
        try:
            print(pd.concat([dfOriginal,dfNew]).drop_duplicates(keep=False), 'Sleeping for {config.sleepTime} minutes...\n###################################')
        except Exception as e:
            print(f"There was an error concatinating and removing duplicates:\n{e}\nSleeping for {config.sleepTime} minutes...\n###################################")
        counter += 1
        time.sleep(60*config.sleepTime)
    except Exception as e:
        print(f"Failed to send request with error:\n{e}\nRetrying...")
        counter += 1