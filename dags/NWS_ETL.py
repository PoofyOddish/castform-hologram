from datetime import datetime, timedelta
from textwrap import dedent
import logging
import sys

import tempfile

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.decorators import task

#Old, but don't want to lose this
#from airflow.providers.sqlite.operators.sqlite import SqliteOperator
#from airflow.providers.sqlite.hooks.sqlite import SqliteHook

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable

BASE_DIR = tempfile.gettempdir()

with DAG(
    dag_id="castform_update",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description="DAG to pull data from NWS and store in Flask-accessible db",
    schedule="*/30 * * * *",
    start_date=datetime(2022, 2, 26),
    catchup=False,
    tags=["example"],
) as dag:

    # [START howto_operator_python]
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        print(kwargs)
        print(ds)
        return "Context check: complete"

    run_this = print_context()
    # [END howto_operator_python]

    @task(task_id="deactive_weather")
    def updateNWS(ti=None):
        import requests,json
        from airflow.models import Variable

        #push to postgres
        sb_url = Variable.get("API_URL")+"/rest/v1/weather?isactive=eq.true"
        sb_key = Variable.get("API_KEY")

        payload = json.dumps({
            "isactive": False,
            })
        
        headers = {
        'apikey': sb_key,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
        'Authorization': f'Bearer {sb_key}'
        }

        response = requests.request("PATCH", sb_url, headers=headers, data=payload)

    close_active = updateNWS()

    @task(task_id="query_nws")
    def getNWS(ti=None):
            import requests, json
            from airflow.models import Variable

            #Note to self: this should be broken out into several tasks when time allows
            
            #Denver
            #To swap out with your weather forecast, pull the station + points
            #Using the following request:
            #url = "https://api.weather.gov/points/39.6195,-105.0918"
            # payload={}
            # headers = {'User-Agent': 'testytest'}
            # response = requests.request("GET", url, headers=headers, data=payload)
            # print(response.text)

            url = "https://api.weather.gov/gridpoints/BOU/58,55/forecast"

            payload={}

            headers = {
            'User-Agent': 'test'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            NWS_subset = json.loads(response.text)['properties']['periods'][0]
            NWS_category = NWS_subset['name']
            NWS_starttime = NWS_subset['startTime']
            NWS_endtime = NWS_subset['endTime']
            NWS_daytime = NWS_subset['isDaytime']
            NWS_temp = NWS_subset['temperature']
            NWS_forecast = NWS_subset['shortForecast']

            NWS_array = [NWS_category,NWS_starttime,NWS_endtime,NWS_daytime,NWS_temp,NWS_forecast]
            
            #This was used historically to pass data between tasks via xcom
            #Not currently used, but for future reference
            #sql=f"INSERT INTO weather (category, starttime,endtime,daytime,temperature,forecast,ISACTIVE) VALUES ('{NWS_array[0]}','{NWS_array[1]}','{NWS_array[2]}','{NWS_array[3]}','{NWS_array[4]}','{NWS_array[5]}',True);",
            #ti.xcom_push(key="NWS data",value=sql)

            #push to postgres
            sb_url = Variable.get("API_URL")+"/rest/v1/weather"
            sb_key = Variable.get("API_KEY")

            payload = json.dumps({
            "category": NWS_category,
            "starttime": NWS_starttime,
            "endtime": NWS_endtime,
            "daytime": NWS_daytime,
            "temperature": NWS_temp,
            "forecast": NWS_forecast,
            "isactive": True,
            })
            
            headers = {
            'apikey': sb_key,
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal',
            'Authorization': f'Bearer {sb_key}'
            }

            response = requests.request("POST", sb_url, headers=headers, data=payload)

            return("Success")

    NWS_text = getNWS()

    run_this >> close_active >> NWS_text 