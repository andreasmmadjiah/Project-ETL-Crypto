from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import datetime.datetime
from alphaVintage_fetch_postgre import *

default_args = {
    "owner": "airflow",
    "start_date": datetime.datetime.now() - datetime.timedelta(days=1),
    # end_date
    "retries":1,s
    "retry_delay":datetime.timedelta(minutes=2)
}
with DAG(
    "alphaVintage_postgre_IBM",
    default_args=default_args,
    schedule_interval = "* * * * *",
    ) as dag:
    fetchDataToLocal = PythonOperator(
            task_id="fetch_data_to_local",
            python_callable=dataToCsv
        )
    sqlLoad = PythonOperator(
            task_id="df_to_postgre",
            python_callable=data_to_postgre
        )
    fetchDataToLocal >> sqlLoad


