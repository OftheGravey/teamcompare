import datetime
from airflow import DAG
import pandas as pd
from airflow.operators.python import PythonOperator
from selenium import webdriver
import sqlalchemy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from airflow.hooks.postgres_hook import PostgresHook
from sqlalchemy import schema
from airflow import hooks

def drive():
    postgres_hook = PostgresHook("airflow_db")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    # player_dict = {
    #     "playerID" : ['f', 'g'],
    #     "summonerName" : ['f', 'g']
    # }
    # player_df = pd.DataFrame(data=player_dict, columns=["playerID", "summonerName"])

    # for idx, row in player_df.iterrows():
    #     try:
    #         cursor.execute(cursor.execute("insert into challenger_players (playerID, summonerName) values ('{}', '{}')".format(row[0], row[1])))
    #     except:
    #         print(row[0], "Duplicate Key")
    #         pass

    cursor.execute("SELECT summonerID FROM challenger_players")
    results = cursor.fetchall()
    print(type(results))
    for i in results:
        print(i)

    cursor.close()
    conn.commit()

with DAG(
    dag_id="do_dag",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@once",
    catchup=False,
) as dag:
    wedriveOp = PythonOperator(
    task_id="drive",
    python_callable=drive
)
