from flask import Flask

oauth_app = Flask(__name__)


@oauth_app.route('/')
def hello_world():
    return 'Hello, World!'
