import datetime
import os
from sys import api_version

from riotwatcher import LolWatcher, ApiError
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from getTopTen import get_Challenger_Players
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Global variables
API_KEY = os.environ["RIOT_API_KEY"]

def getChampions():
    lol_watcher = LolWatcher(API_KEY)

    versions = lol_watcher.data_dragon.versions_for_region('oce')
    champions_version = versions['n']['champion']

    current_champ_list = lol_watcher.data_dragon.champions(champions_version)

    champions = []


    for key in current_champ_list['data'].keys():
        if len(current_champ_list['data'][key]['tags']) == 1:
            champion = (int(current_champ_list['data'][key]['key']), key, current_champ_list['data'][key]['tags'][0], 'None')
        else:
            champion = (int(current_champ_list['data'][key]['key']), key, current_champ_list['data'][key]['tags'][0], current_champ_list['data'][key]['tags'][1])
        champions.append(champion)
        print(champion)

    # Hook
    pg_hook = PostgresHook("airflow_db")
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    cursor.executemany("insert into champions (championID, championName, championPrimaryType, championSecondaryType) values (%s, %s, %s, %s)", champions)

    conn.commit()
    cursor.close()


with DAG(
    dag_id="champion_dag",
    start_date=datetime.datetime(2021, 8, 6),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    transport_Load = PythonOperator(
        task_id="Get_Champions",
        python_callable=getChampions
    )