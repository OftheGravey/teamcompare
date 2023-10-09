import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG(
    dag_id="build_dag",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@once",
    catchup=False,
) as dag:
    create_table = PostgresOperator(
        task_id="build",
        postgres_conn_id="airflow",
        sql="sql/build_db.sql"
    )

create_table
