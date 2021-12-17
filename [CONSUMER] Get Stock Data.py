
import requests


from time import sleep
from json import dumps
from kafka import KafkaConsumer
from json import loads
import pymongo
from datetime import datetime

# Initializes The Consumer, read data and should insert it to sql
consumer = KafkaConsumer(
    "datacrypto",
    bootstrap_servers = ['localhost:9092'],
    auto_offset_reset = "earliest",
    enable_auto_commit = True,
    group_id = None, 
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
client = pymongo.MongoClient("mongodb://user:1234@localhost:27017/")
db = client['project_alpha_vintage']
collection = db['EXCHANGERATE']


#  In case you want index
# a=collection.find_one({'created_date':'1945-01-01 00:00:00'})
# if str(type(a))=="<class 'NoneType'>":
#     print('create initial data in mongo and creating index by created date')
#     collection.insert_one({'created_date':'1945-01-01 00:00:00'})
#     resp = collection.create_index([ ("created_date", 1) ])
#     print ("index response:", resp)




# without group id, you basically reset each restart kafka

# print(consumer.__consumer_offsets)

# consumer.poll()
# consumer.seek_to_end()
for j,event in enumerate(consumer):
    print(f'Iteration : {j}')
    event_data = event.value
    event_data['created_date'] = datetime.strptime(datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d') # insert as datetime
    data_dummy = {}
    for key in event_data.keys():
        if len(key.split('. '))>1:
            key_fix = key.split('. ')[1]
            key_fix = '_'.join(key_fix.split(' '))
            data_dummy[key_fix] = event_data[key]
        else:
            data_dummy[key] = event_data[key]
    print(data_dummy)
    collection.insert_one(data_dummy)
    print()
    print('Data inserted to mongo')
    print('=============================\n')
    # break
    # sleep(5)