from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.data_collection import fetch_data
from src.data_processing import preprocess_data

args = {
    "start_date": datetime(2024, 10, 10),
    "retries": 3,
    "email": ["abdulrahmanbutt7273@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
}

with DAG("class_act_7_pipeline", default_args=args, schedule_interval="@hourly", description="Pipeline to fetch and preprocess weather data",) as dag:
    collect_data_task = PythonOperator(
        task_id="collect_data",
        python_callable=fetch_data,
    )

    preprocess_data_task = PythonOperator(
        task_id="preprocess_data",
        python_callable=preprocess_data,
    )

    collect_data_task >> preprocess_data_task


