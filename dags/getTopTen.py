import os
import pandas as pd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timezone
from mysql.connector import connect, Error
from getpass import getpass
from riotwatcher import LolWatcher, ApiError
from sqlalchemy import create_engine
from selenium import webdriver

# Global variables
API_KEY = os.environ["RIOT_API_KEY"]

def get_names_from_xpaths(xpaths) -> list:
    liste = []
    for a in xpaths:
        liste.append(a.text)
    return liste

def validate_data(df: pd.DataFrame) -> bool:
    # Empty Check
    if df.empty:
        print("No Summoners Found")
        return False

    # Primary Key Check
    if pd.Series(df['summonerName']).is_unique:
        pass
    else:
        raise Exception("Primary Key Check Failed")

    # Null Check
    if df.isnull().values.any():
        raise Exception("Null Values Found")
     
def db_insertion(table, values):
    # Validation 
    if (len(values) != table.count(',') + 1):
        raise "Inequal Columns to Table"

    for i in range(1, len(values)):
        if len(values[0]) != len(values[i]):
            raise "Inequal Columns to Eachother"

    # Hook
    pg_hook = PostgresHook("airflow_db")
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    for i in range(0, len(values[0])):
        if values[0][i] != 0:

            insertion_sql = "insert into {} values (".format(table)
            for j in range(0, len(values)-1):
                insertion_sql = insertion_sql + "'{}',".format(values[j][i])
            insertion_sql = insertion_sql + "'{}')".format(values[len(values)-1][i])

            try:
                cursor.execute(insertion_sql)
            except:
                print(values[0][i], "Duplicate Key")
                pass


    conn.commit()
    cursor.close()



def get_xpath(driver,class_Name):
    try:
        x = driver.find_elements_by_xpath(class_Name)
    except:
        print("Website Error -- Check if xpath class name has changed")
    return x

def get_Challenger_Players():
    # Generates table from:
    # - Names scrapped from a webpage
    # - IDs from riotwatcher using said names
    # Extract Names

    print("Creating Driver")
    driver = webdriver.Remote(command_executor='http://192.168.20.2:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)

    driver.get('https://oce.op.gg/ranking/ladder/')
    driver.implicitly_wait(10) # seconds

    summoner_names = []

    print("Name extracting")

    x = get_xpath(driver, "//a[@class='ranking-highest__name']")
    summoner_names = summoner_names + get_names_from_xpaths(x)
    x = get_xpath(driver, "//td[@class='ranking-table__cell ranking-table__cell--summoner']")
    summoner_names = summoner_names + get_names_from_xpaths(x)

    driver.close()

    challenger_id = []

    print("Extracting IDs")

    # Extract IDs
    watcher = LolWatcher(API_KEY)
    for name in summoner_names:
        try:
            person = watcher.summoner.by_name("oc1", name)
        except:
            challenger_id.append('0')
            continue
        challenger_id.append(person['accountId'])


    print("IDs extracted")

    dateToday = datetime.now().strftime("%Y-%m-%d")

    print("INSERTION")

    db_insertion("challenger_players (playerID, summonerName)", [challenger_id, summoner_names])

    # Hook
    pg_hook = PostgresHook("airflow_db")
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    summonerIds = []
    for i in range(0, 10):
        cursor.execute("SELECT summonerID from challenger_players where playerID = '{}'".format(challenger_id[i]))
        result = cursor.fetchall()
        summonerIds.append(result[0][0])
    

    db_insertion("topTen (summonerID, dateOfAchievement)", [summonerIds, [dateToday for x in range(0, 10)]])

    cursor.close()

    #driver.close()
