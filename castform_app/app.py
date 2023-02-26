from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,Flask
)

#app = Flask(__name__)

#flask --app app run

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    from castform_app.utilities import getCastform

    castform = getCastform()
    print(castform)
    print(castform[0])

    return render_template('index.html',castform=castform)

@bp.route('/api/status')
def status():
    from castform_app.utilities import getCastform
    from flask import jsonify

    castform = getCastform()
    print(castform)
    print(castform[0])

    return jsonify(castform)
    #return render_template('index.html',castform=castform)

@bp.route('/update')
def update():
    return render_template('update.html')
