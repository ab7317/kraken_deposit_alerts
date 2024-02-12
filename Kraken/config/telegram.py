import requests
import config

message = 'Hello World!!!!'

url = f"https://api.telegram.org/bot{config.telegram_token}/sendMessage?chat_id={config.telegram_id}&text={message}"
r = requests.get(url)
