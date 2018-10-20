from json import JSONDecodeError

from flask import Blueprint, Response, jsonify
from flask_dance.contrib.github import github

api = Blueprint('api', __name__)


def make_request(query):
    resp = github.post('/graphql', json={'query': query})

    try:
        return resp.json()
    except JSONDecodeError:
        return Response(resp.text, status=503)


@api.route('/me')
def me():
    return jsonify(make_request("""{
  viewer {
    login
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}"""))
