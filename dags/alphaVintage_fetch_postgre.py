import pandas as pd
import psycopg2 as pg
import requests
from sqlalchemy import create_engine

import datetime

import os

import subprocess

def dataToCsv():
    APIKEY = '4IEI37PXMEKHFR2I'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=60min&apikey={APIKEY}'
    r = requests.get(url)
    data = r.json()

    data_df =pd.DataFrame.from_dict(data['Time Series (60min)'],orient='index').reset_index()
    data_df.columns = ['ddate','open','high','low','close','volume']

    data_df['ddate'] = data_df['ddate'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    for col in data_df.columns[1:]:
        data_df[col] = data_df[col].apply(lambda x: float(x))
    data_df['created_time'] = datetime.datetime.now()
    filename = datetime.datetime.strftime(datetime.datetime.now().date(),'%Y%m%d')
    os.makedirs('./data', exist_ok=True)
    print(os.listdir())
    data_df.to_csv(f"data/{filename}_ibm.csv",index=False)


# API 4IEI37PXMEKHFR2I
def data_to_postgre():
    filename = datetime.datetime.strftime(datetime.datetime.now().date(),'%Y%m%d')
    df = pd.read_csv(f"data/{filename}_ibm.csv")
    cols = str(df.iloc[-1,0])
    cmd = ['echo',cols]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    print(output)



    param_dic = {'user':'airflow','password':'airflow','host':'postgres','database':'airflow'}
    connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
        param_dic['user'],
        param_dic['password'],
        param_dic['host'],
        param_dic['database']
    )
    """
    Using a dummy table to test this call library
    """
    engine = create_engine(connect)
    df.to_sql(
        'stock_data_ibm', 
        con=engine, 
        schema='sandbox',
        index=False, 
        if_exists='append'
    )
    cmd = ['echo','DONE Sql Alchemy']
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
