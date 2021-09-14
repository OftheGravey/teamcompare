import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG(
    dag_id="rebuild_dag",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@once",
    catchup=False,
) as dag:
    delete_tables = PostgresOperator(
        task_id="delete",
        postgres_conn_id="airflow_db",
        sql="sql/delete_db.sql"
    )
    create_table = PostgresOperator(
        task_id="build",
        postgres_conn_id="airflow_db",
        sql="sql/build_db.sql"
    )

    delete_tables >> create_table