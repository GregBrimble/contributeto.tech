from binascii import hexlify
from os import urandom

from flask import Flask
from flask_dance.contrib.github import make_github_blueprint, github

api = Flask(__name__)
api.secret_key = hexlify(urandom(24))

github_oauth_blueprint = make_github_blueprint(
    client_id="my-key-here",
    client_secret="my-secret-here",
)
api.register_blueprint(github_oauth_blueprint, url_prefix="/login")


@api.route('/')
def index():
    return "Hi!"

