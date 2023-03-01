from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,Flask
)

app = Flask(__name__)

#bp = Blueprint('main', __name__)

@app.route('/')
def index():
    try:
        from utilities import getCastform
    except:
        return 'sorry import not found'

    castform = getCastform()
    #print(castform)
    return render_template('index.html',castform=castform[0])

@app.route('/api/status')
def status():
    from utilities import getCastform
    from flask import jsonify

    castform = getCastform()
    #print(castform[0]['img'])
    #print(castform['img'])

    return jsonify(castform)
    #return render_template('index.html',castform=castform[0])

@app.route('/update')
def update():
   return render_template('update.html')

if __name__ == "__main__":
    app.run()