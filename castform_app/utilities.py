def testAirflow():
    return("test is a success!")

def getNWS():
    import requests

    url = "https://api.weather.gov/gridpoints/BOU/58,55/forecast"

    payload={}
    headers = {
    'User-Agent': 'test'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return(response.text)


def transformNWS(NWS_data: str):
    import json

    NWS = NWS_data
    NWS_subset = json.loads(NWS)['properties']['periods'][0]
    NWS_category = NWS_subset['name']
    NWS_starttime = NWS_subset['startTime']
    NWS_endtime = NWS_subset['endTime']
    NWS_daytime = NWS_subset['isDaytime']
    NWS_temp = NWS_subset['temperature']
    NWS_forecast = NWS_subset['shortForecast']

    return([NWS_category,NWS_starttime,NWS_endtime,NWS_daytime,NWS_temp,NWS_forecast])

def insertNWS(NWS_array: list):
    manual_query(create_connection(),f"UPDATE weather SET ISACTIVE = False WHERE ISACTIVE = True;")
    manual_query(create_connection(),f"INSERT INTO weather (category, starttime,endtime,daytime,temperature,forecast,ISACTIVE) VALUES ('{NWS_array[0]}','{NWS_array[1]}','{NWS_array[2]}','{NWS_array[3]}','{NWS_array[4]}','{NWS_array[5]}',True);")

def updateWeather():
    data = getNWS()
    transformed_data = transformNWS(data)
    insertNWS(transformed_data)

def getCastform():
    import os, requests,json
    from dotenv import load_dotenv
    load_dotenv()

    api_url = os.environ.get('API_URL')+"/rest/v1/vw_castform"
    api_key = os.environ.get('API_KEY')
    
    headers = {
    'apikey': api_key,
    'Authorization': f'Bearer {api_key}'
    }

    response = requests.request("GET", api_url, headers=headers)

    return(json.loads(response.text))


### QUERIES
#def create_connection(db_file='./instance/castform.sqlite'):
def create_connection(db_file='/opt/app/instance/castform.sqlite'):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    import os

            #api_key = os.getenv('API_URL')
            #api_key = os.getenv('API_KEY')
    import sqlite3

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def manual_query(conn,query: str,print_rows=False,save_results=False):
    """
    Insert single row into table
    :param conn: the Connection object
    :param query: Query to submit
    :optional kwargs:
    -- print: print return values on True
    """

    cur = conn.cursor()
    cur.execute(f"{query}")

    if save_results:
        results = []

    if print_rows or save_results:
        rows = cur.fetchall()

        for row in rows:
            if print_rows:
                print(row)
            if save_results:
                results.append(row)

    conn.commit()

    if save_results:
        return(results)

def decompose_sql(sql_file: str):
    """
    Convert SQL file into individual queries and execute
    params:
    sql_file (str): location of SQL file to execute
    """
    import sqlite3
    from sqlite3 import OperationalError

    for file in [sql_file]:
        fd = open(f'./castform_app/SQL/{file}')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')

        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                manual_query(create_connection(),command)
            except OperationalError:
                print("Command skipped: ", command)