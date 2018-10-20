from os import getenv

from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from werkzeug.contrib.fixers import ProxyFix

from backend.api import api

app = Flask(__name__, template_folder='../frontend')
app.wsgi_app = ProxyFix(app.wsgi_app)
app.debug = True
app.secret_key = getenv('SECRET_KEY')

github_oauth_blueprint = make_github_blueprint(
    client_id=getenv('GITHUB_OAUTH_CLIENT_ID'),
    client_secret=getenv('GITHUB_OAUTH_CLIENT_SECRET'),
    scope='read:user,repo,user:email',
    redirect_to='recommendations'
)
app.register_blueprint(github_oauth_blueprint, url_prefix='/login')

app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    if github.authorized:
        return redirect(url_for('recommendations'))

    return render_template('index.html')


@app.route('/recommendations')
def recommendations():
    if not github.authorized:
        return redirect(url_for('index'))

    return render_template('recommendations.html', number=0)


if __name__ == '__main__':
    app.run(port=5432)
