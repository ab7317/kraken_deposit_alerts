import requests, hmac, hashlib, base64, time, urllib.parse, sys, datetime
import pandas as pd

sys.path.append('/home/ubuntu/kraken_deposists_alerts/config/')
import config

startTime = time.time()

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

dfOriginal = pd.read_csv('newest_deposit.csv')
counter = 0

print(f"Initial start time: {datetime.datetime.fromtimestamp(startTime).strftime('%H:%M:%S')}")
while True:
    startLoop = time.time()
    print(f"Starting loop...\nLoop has run {counter} times.\nStarting at: {datetime.datetime.fromtimestamp(startLoop).strftime('%H:%M:%S')}\nTotal run time: {datetime.datetime.fromtimestamp(startLoop-startTime).strftime('%H:%M:%S')}\nSending Request.")
    try:
        resp = kraken_request(config.endpoint, {
            "nonce": str(int(1000 * time.time())),
        })
        print('Request sent succesfully')
        dfNew = dfOriginal
        dfOriginal = pd.DataFrame(resp['result'])
        try:
            #dfNew = dfNew.drop(columns=['originators'])
            dfNew = dfNew[['asset', 'txid', 'amount', 'time']]
        except:
            pass
        try:
            #dfOriginal = dfOriginal.drop(columns=['originators'])
            dfOriginal = dfOriginal[['asset', 'txid', 'amount', 'time']]
        except: 
            pass
        print('Dataframes setup correctly')
        try:
            #print(pd.concat([dfOriginal,dfNew]).drop_duplicates(keep=False), 'Sleeping for {config.sleepTime} minutes\nSleep starting at: {datetime.datetime.fromtimestamp(startSleep).strftime('%H:%M:%S')}\n###################################')
            df = pd.concat([dfNew,dfOriginal]).drop_duplicates(keep=False)
            df = df.to_dict(orient='records')
            if len(df) != 0:
                for i in df:
                    requests.get(f"https://api.telegram.org/bot{confi.telegram_token}/sendMessage?chat_id={confi.telegram_id}&text=New Deposit Asset: {i['asset']}\nAmount: {i['amount']}\nTxId: {i['txid']}\nTime: {datetime.datetime.fromt>
            startSleep = time.time()
            print(f"Sleeping for {config.sleepTime} minutes\nSleep starting at: {datetime.datetime.fromtimestamp(startSleep).strftime('%H:%M:%S')}\nSleep finishing at: {datetime.datetime.fromtimestamp(startSleep+300).strftime('%H:%M:%S')}\n###################################")
        except Exception as e:
            requests.get(f"https://api.telegram.org/bot{config.telegram_error_token}/sendMessage?chat_id={config.telegram_error_id}&text=Error: {e}")
            startSleep = time.time()
            print(f"There was an error concatinating and removing duplicates:\n{e}\nSleeping for {config.sleepTime} minutes\nSleep starting at: {datetime.datetime.fromtimestamp(startSleep).strftime('%H:%M:%S')}\nSleep finishing at: {datetime.datetime.fromtimestamp(startSleep+300).strftime('%H:%M:%S')}\n###################################")
            #requests.get(f"https://api.telegram.org/bot{config.telegram_token}/sendMessage?chat_id={config.telegram_id}&text=Error: {e}")
        counter += 1
        dfOriginal.to_csv('newest_deposit.csv')
        time.sleep(60*config.sleepTime)
    except Exception as e:
        requests.get(f"https://api.telegram.org/bot{config.telegram_error_token}/sendMessage?chat_id={config.telegram_error_id}&text=Error: {e}")
        print(f"Failed to send request with error:\n{e}\nRetrying...")
        counter += 1
