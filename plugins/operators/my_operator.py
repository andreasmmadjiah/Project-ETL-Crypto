from airflow.operators.bash_operator import BaseOperator
from airflow.utils.decorators import apply_defaults

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable
import logging
import pymongo
from datetime import datetime





class Mongo_to_Postgres(BaseOperator):
    def __init__(self, name: str, mongo_variable: str, postgres_con_id: str, database:str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.mongo_variable = mongo_variable
        self.postgres_con_id = postgres_con_id
        self.database = database

    def execute(self, context):
        self.run_time =datetime.strptime(context["ds"],r'%Y-%m-%d')
        run_time_str = self.run_time.strftime('%Y-%m-%d')

        hook_postgres = PostgresHook(conn_name_attr=self.postgres_con_id)
        client = pymongo.MongoClient(Variable.get(self.mongo_variable))
        collection = client['project_alpha_vintage']['EXCHANGERATE']
        sql_mongo = {"created_date":{"$eq":self.run_time}}
        
        # logging.info("asdasdasdadasdasdasdasd")
        
        # logging.info(context["ds"])
        sql_postgres = f"select * from CRYPTOEXCHANGERATE where created_date = '{run_time_str}' limit 1"
        a=hook_postgres.get_first(sql_postgres)
        logging.info('Yeah============')
        logging.info(self.run_time)
        logging.info(a)
        logging.info(Variable.get(self.mongo_variable))

        result_mongo = collection.find(sql_mongo)
        logging.info(self.run_time)
        
        iter=0
        list_values=[]
        for result in result_mongo: # if result_mongo is null, then it will just pass
            # logging.info(result)
            list_values.append((result['From_Currency_Code'],
                result['To_Currency_Code'],
                float(result['Exchange_Rate']),
                float(result['Ask_Price']),
                float(result['Bid_Price']),
                datetime.strptime(result['Last_Refreshed'],r'%Y-%m-%d %H:%M:%S'),
                result['Time_Zone'],
                datetime.strptime(datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
                ))
        list_values = list(set(list_values))
        logging.info("====test=====")
        logging.info(list_values)
        hook_postgres.insert_rows('CRYPTOEXCHANGERATE',list_values)


        # logging.info(str(result_mongo))
        # logging.info('Yeah')
        # raise ValueError(str(result_mongo))
        # sql_postgres = 'select top 1 * from airflow.BTCEXCHANGERATE'
        # result_postgres = hook_postgres.get_records(sql_postgres)
        # if len(result_postgres)!=0:
        #     raise ValueError('There is already run time in postgres!')

        message = 'yeah'
        # print(message)
        return message


class Step(BaseOperator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
    def execute(self, context):
        
        logging.info('Yeah STEP')
        # raise ValueError(str(result_mongo))
        # sql_postgres = 'select top 1 * from airflow.BTCEXCHANGERATE'
        # result_postgres = hook_postgres.get_records(sql_postgres)
        # if len(result_postgres)!=0:
        #     raise ValueError('There is already run time in postgres!')

        message = 'yeah'
        # print(message)
        return message