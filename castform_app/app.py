from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,Flask
)

app = Flask(__name__)

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    from castform_app.utilities import getCastform

    castform = getCastform()
    #print(castform)
    return render_template('index.html',castform=castform[0])

@bp.route('/api/status')
def status():
    from castform_app.utilities import getCastform
    from flask import jsonify

    castform = getCastform()
    #print(castform[0]['img'])
    #print(castform['img'])

    #return jsonify(castform)
    return render_template('index.html',castform=castform[0])

@bp.route('/update')
def update():
   return render_template('update.html')

if __name__ == "__main__":
    app.run()