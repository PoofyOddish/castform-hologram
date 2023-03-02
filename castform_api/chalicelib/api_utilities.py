
def update_db(apiurl,apikey,endpoint,api_method,headers,payload) -> None:
    import os,requests
    
    from dotenv import load_dotenv

    load_dotenv()

    sb_url = apiurl+endpoint
    sb_key = apikey+("API_KEY")

    headers['apikey']=sb_key
    headers['authorization']=f'Bearer {sb_key}'

    response = requests.request(api_method, sb_url, headers=headers, data=payload)

def deactivate_weather(apiurl,apikey) -> None:
    import requests,json,os

    payload = json.dumps({
        "isactive": False,
        })
    
    headers = {
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal',
    }

    update_db(apiurl,apikey,"/rest/v1/weather?isactive=eq.true","PATCH", headers=headers, payload=payload)

def pull_NWS() -> list:
    import requests, json

    url = "https://api.weather.gov/gridpoints/BOU/58,55/forecast"

    payload={}

    headers = {
    'User-Agent': 'test'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    NWS_subset = json.loads(response.text)['properties']['periods'][0]

    return(NWS_subset)


def update_NWS(apiurl,apikey) -> list:
        import json

        NWS_subset = pull_NWS()
        NWS_category = NWS_subset['name']
        NWS_starttime = NWS_subset['startTime']
        NWS_endtime = NWS_subset['endTime']
        NWS_daytime = NWS_subset['isDaytime']
        NWS_temp = NWS_subset['temperature']
        NWS_forecast = NWS_subset['shortForecast']

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
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
        }

        update_db(apiurl,apikey,"/rest/v1/weather","POST",headers,payload)

        return(payload)
