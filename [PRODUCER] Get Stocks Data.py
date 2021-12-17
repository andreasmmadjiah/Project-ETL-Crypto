import requests

API_KEY = "8IHVH6JOZK2FAEPI"

# url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={API_KEY}'
# url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey={API_KEY}'
url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey={API_KEY}'
r = requests.get(url)
data = r.json()


from time import sleep
from json import dumps
from kafka import KafkaProducer

# Initializes The Producer, ergo the Topic's information "pusher"
producer = KafkaProducer(
    bootstrap_servers = ["localhost:9092"], # like in the docker compose, "Outside" is 9092
    value_serializer = lambda x:dumps(x).encode('utf-8') # each value x will be dumps to json then encode it to byte
    # As kafka need any data sends using string, then need to be encoded to byte. json.dumps will make json to string then encode it to utf-8 (or byte)
)

for j in range(1000):
    print(f'Iteration : {j}')
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=IDR&apikey={API_KEY}'
    r = requests.get(url,timeout=60)
    data = r.json()['Realtime Currency Exchange Rate']
    # data = {"iter":j}
    print(data)
    producer.send('datacrypto',data)
    # producer.flush()
    print()

    sleep(30)
    
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=ETH&to_currency=IDR&apikey={API_KEY}'
    r = requests.get(url,timeout=60)
    data = r.json()['Realtime Currency Exchange Rate']
    # data = {"iter":j}
    print(data)
    producer.send('datacrypto',data)
    # producer.flush()
    print('\n====================================================\n')

    sleep(30)