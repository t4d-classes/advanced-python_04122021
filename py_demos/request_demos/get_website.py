import requests
import json


response = requests.request("GET", "https://api.ratesapi.io/api/2010-01-12")

rate_data = json.loads(response.text)

print(rate_data['base'])
print(rate_data['rates']["RUB"])