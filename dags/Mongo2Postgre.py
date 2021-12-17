from airflow import DAG
from airflow.operators.bash_operator import BaseOperator
from airflow.utils.decorators import apply_defaults
# from airflow.providers.mongo.hooks.mongo import MongoHook
# from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
import datetime
from operators.my_operator import Mongo_to_Postgres,Step
from airflow.operators.postgres_operator import PostgresOperator
from datetime import timedelta

default_args = {
    "owner": "airflow",
    "start_date": datetime.datetime(2021,1,1),
    # end_date
    # "retries":1,.
    # "retry_delay":datetime.timedelta(minutes=2)
}
with DAG(
    "Mongo2Postgre",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval=None,
    # schedule_interval = timedelta(days=1),
    ) as dag:
    delete_main = PostgresOperator(
            task_id="delete_main",
            postgres_con_id = "postgres_default",
            sql="""
                delete from cryptoexchangerate where created_date='{{ds}}'
            """
            )
    delete_cleaned = PostgresOperator(
            task_id="delete_cleaned",
            postgres_con_id = "postgres_default",
            sql="""
                delete from cyptoexchangerate_cleaned where created_date='{{ds}}'
            """
            )
    delete_agg_daily = PostgresOperator(
            task_id="delete_agg_daily",
            postgres_con_id = "postgres_default",
            sql="""
                delete from cyptoexchangerate_agg_daily where created_date='{{ds}}'
            """
            )
    
    fetchDataToLocal = Mongo_to_Postgres(
            task_id="Mongo_2_Postgre",
            name = 'apaja',
            mongo_variable = "monggo_url",
            postgres_con_id="postgres_default",
            database='asd',
        )
    agg_cleaned = PostgresOperator(
            task_id="Run_Agg_Cleaned",
            postgres_con_id = "postgres_default",
            sql="""
                INSERT INTO cyptoexchangerate_cleaned
                select to_timestamp(to_char(ddate,'YYYY-mm-dd HH24:mi:SS'),'YYYY-mm-dd HH24:mi') as ddate
                    , a.crypto_code
                    , a.cur_code
                    , b.crypto_name
                    , c.cur_name
                    , AVG(exchange_rate) as exchange_rate
                    , AVG(ask_price) as ask_price 
                    , AVG(bid_price) as bid_price
                    , to_timestamp('2021-12-09','YYYY-mm-dd') as created_date
                from cryptoexchangerate as a 
                left join cryptocode b on a.crypto_code = b.crypto_code
                left join curcode c on a.cur_code = c.cur_code
                WHERE a.created_date = '2021-12-09'
                group by to_timestamp(to_char(ddate,'YYYY-mm-dd HH24:mi:SS'),'YYYY-mm-dd HH24:mi')
                    ,a.crypto_code
                    ,a.cur_code
                    ,b.crypto_name
                    ,c.cur_name;
            """
            )
    
    agg_daily = PostgresOperator(
            task_id="Run_Agg_Daily",
            postgres_con_id = "postgres_default",
            sql="""
                INSERT INTO cyptoexchangerate_agg_daily
                select to_timestamp(to_char(ddate,'YYYY-mm-dd HH24:mi:SS'),'YYYY-mm-dd') as ddate
                    , a.crypto_code
                    , a.cur_code
                    , b.crypto_name
                    , c.cur_name
                    , avg(exchange_rate) as avg_exchange_rate
                    , avg(ask_price) as avg_ask_price 
                    , avg(bid_price) as avg_bid_price
                    , to_timestamp('{{ds}}','YYYY-mm-dd') as created_date
                from cryptoexchangerate as a 
                left join cryptocode b on a.crypto_code = b.crypto_code
                left join curcode c on a.cur_code = c.cur_code
                WHERE a.created_date = '{{ds}}'
                group by to_timestamp(to_char(ddate,'YYYY-mm-dd HH24:mi:SS'),'YYYY-mm-dd')
                    ,a.crypto_code
                    ,a.cur_code
                    ,b.crypto_name
                    ,c.cur_name;
            """
            )

    
    delete_main>>fetchDataToLocal
    fetchDataToLocal>>delete_cleaned>>agg_cleaned
    fetchDataToLocal>>delete_agg_daily>>agg_daily
    # agg_daily

