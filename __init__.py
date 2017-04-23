from flask import Flask, url_for, request, session, redirect, render_template
from flask_oauth import OAuth

FACEBOOK_APP_ID = '293823757717281'
FACEBOOK_APP_SECRET = '49b409de34973230b046a4a091cea4a6'
app = Flask(__name__)
app.secret_key = '9ujYZLNmd6NIdPdlTSVJ'
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route('/')
def index():
	if session.get('logged_in'):
		data = facebook.get('/me').data
		return render_template('index.html', data = data)
	return render_template('index.html')

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug = True)