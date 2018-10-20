from json import JSONDecodeError, dumps

from flask import Blueprint, Response, jsonify
from flask_dance.contrib.github import github

from backend.queries import interested_in_repositories_query, contributed_to_repositories_query

api = Blueprint('api', __name__)


def make_request(query, variables=None):
    resp = github.post('/graphql', json={'query': query, 'variables': dumps(variables)})

    try:
        return resp.json()
    except JSONDecodeError:
        return Response(resp.text, status=503)


def get_contributed_to_repositories():
    return make_request(contributed_to_repositories_query)


def get_recommendations_for_repository(repository):
    response = make_request(interested_in_repositories_query, variables={'queryString': 'language:Python'})
    return [edge['node'] for edge in response['data']['search']['edges']]


@api.route('/recommendations')
def get_recommendations():
    contributed_to_repositories = get_contributed_to_repositories()
    recommendations = []

    for repository in contributed_to_repositories['data']['viewer']['repositoriesContributedTo']['edges']:
        repository_recommendations = [repository['node']]
        repository_recommendations.extend(get_recommendations_for_repository(repository['node']))
        recommendations.append(repository_recommendations)

    return jsonify(recommendations)
