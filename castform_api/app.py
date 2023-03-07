from chalice import Chalice, Rate

app = Chalice(app_name='castform_api')

@app.route('/')
def index():
    from chalicelib import api_utilities as au
    import os

    sb_url = os.getenv("API_URL",'None')
    sb_key = os.getenv("API_KEY",'None')

    payload = {
         "isactive": False
         }
    
    headers = {
     'Content-Type': 'application/json',
     'Prefer': 'return=minimal'
     }

    recent_data=au.query_db(sb_url,sb_key,"/rest/v1/weather?isactive=eq.true","GET",headers,payload)

    return(recent_data.text)

@app.schedule(Rate(1, unit=Rate.HOURS))
def update_data(event):
    from chalicelib import api_utilities as au
    import os
    
    print('starting job')
    sb_url = os.getenv("API_URL",'None')
    sb_key = os.getenv("API_KEY",'None')

    print('deactivating existing active forecasts')
    au.deactivate_weather(sb_url,sb_key)
    print('finished deactivating existing active forecasts')

    print('generating active forecasts')
    NWS_data = au.update_NWS(sb_url,sb_key)
    print('finished generating active forecasts')

    print('cool beans')