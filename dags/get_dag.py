import datetime
from sys import api_version

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from getTopTen import get_Challenger_Players
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

with DAG(
    dag_id="insert_dag",
    start_date=datetime.datetime(2021, 8, 6),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    transport_Load = PythonOperator(
        task_id="Transform_Load_Data",
        python_callable=get_Challenger_Players
    )