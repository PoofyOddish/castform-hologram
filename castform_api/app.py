from chalice import Chalice

app = Chalice(app_name='castform_api')


@app.route('/')
def index():
    from chalicelib import api_utilities as au
    import os

    sb_url = os.getenv("API_URL",'None')
    sb_key = os.getenv("API_KEY",'None')

    au.deactivate_weather(sb_url,sb_key)
    NWS_data = au.update_NWS(sb_url,sb_key)

    return(NWS_data)

