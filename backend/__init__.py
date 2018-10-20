from os import getenv

from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from werkzeug.contrib.fixers import ProxyFix
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../frontend')
app.wsgi_app = ProxyFix(app.wsgi_app)
app.debug = True
app.secret_key = getenv('SECRET_KEY')

github_oauth_blueprint = make_github_blueprint(
    client_id=getenv('GITHUB_OAUTH_CLIENT_ID'),
    client_secret=getenv('GITHUB_OAUTH_CLIENT_SECRET'),
    redirect_to='recommendations'
)
app.register_blueprint(github_oauth_blueprint, url_prefix='/login')


@app.route('/')
def index():
    if github.authorized:
        return redirect(url_for('recommendations'))
    return render_template('index.html')


@app.route('/recommendations')
def recommendations():
    resp = github.get('/user')
    return 'You are @{login} on GitHub'.format(login=resp.json()['login'])


@app.route('/graphql_test')
def test():
    resp = github.post('/graphql', json={'query': """{
  viewer {
    login
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}"""})
    return resp.text


if __name__ == '__main__':
    app.run(port=5432)
