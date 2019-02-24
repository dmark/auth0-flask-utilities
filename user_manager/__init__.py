from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for

from flask_bootstrap import Bootstrap

from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

import constants
import user_manager.forms as forms

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'


def create_app():
    app = Flask(__name__, static_url_path='/public', static_folder='./public')
    app.config['SECRET_KEY'] = env.get(constants.SECRET_KEY)
    app.debug = True

    Bootstrap(app)

    return app

app = create_app()

oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


@app.route('/')
@requires_auth
def home():
    return render_template('index.html',
                           userinfo=session[constants.PROFILE_KEY],
                           jwt_payload=session[constants.JWT_PAYLOAD],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD],
                                                      indent=4))


@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL,
                                    audience=AUTH0_AUDIENCE)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True),
              'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/user_id/<user_id>')
@requires_auth
def profile(user_id):
    """ Use this to display user user_id's profile. This can be called as a
    function like so: url_for('profile', user_id=userinfo['sub'])
    """
    form = forms.ProfileForm(email=session['jwt_payload']['email'],
                             email_verified=session['jwt_payload']['email_verified'],
                             user_id=session['jwt_payload']['sub'],
                             name=session['jwt_payload']['name'],
                             nickname=session['jwt_payload']['nickname']
                             )
    return render_template('profile.html',
                           email=user_id,
                           userinfo=session[constants.PROFILE_KEY],
                           jwt_payload=session[constants.JWT_PAYLOAD],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD],
                                                      indent=4),
                           form=form)


@app.route('/user/add', methods=['GET', 'POST'])
@requires_auth
def user_add():
    form = forms.NewUserForm()
    return render_template('adduser.html', form=form)


@app.route('/user/get', methods=['GET', 'POST'])
@requires_auth
def user_get():
    form = forms.GetUserForm()
    return render_template('getuser.html', form=form)


@app.errorhandler(404)
@requires_auth
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
@requires_auth
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(Exception)
@requires_auth
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=env.get('PORT', 5000), debug=True)
    app.run(debug=True)
