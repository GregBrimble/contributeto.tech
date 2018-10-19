from os import getenv

from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

api = Flask(__name__, template_folder='../frontend')
api.debug = True
api.secret_key = getenv('SECRET_KEY')

github_oauth_blueprint = make_github_blueprint(
    client_id=getenv('GITHUB_OAUTH_CLIENT_ID'),
    client_secret=getenv('GITHUB_OAUTH_CLIENT_ID'),
)
api.register_blueprint(github_oauth_blueprint, url_prefix='/login')


@api.route('/')
def index():
    if github.authorized:
        return redirect(url_for('recommendations'))
    return render_template('index.html')


@api.route('/recommendations')
def recommendations():
    resp = github.get('/user')
    assert resp.ok
    return 'You are @{login} on GitHub'.format(login=resp.json()['login'])
