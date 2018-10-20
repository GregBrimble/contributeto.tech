from json import JSONDecodeError, dumps
from random import choice

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


def generate_query_from_repository(repository):
    repository_language = repository['languages']['edges'][0]['node']['name']
    language_query = {
        'string': 'language:{language}'.format(language=repository_language),
        'reason': 'Because you use {language}'.format(language=repository_language)
    }

    query = language_query

    if repository['repositoryTopics']['edges']:
        random_repository_topic = choice(repository['repositoryTopics']['edges'])['node']['topic']['name']
        topics_query = {
            'string': 'topic:{topic}'.format(topic=random_repository_topic),
            'reason': 'Because you contribute with {topic}'.format(topic=random_repository_topic)
        }

        query = choice([language_query, topics_query])

    return query


def get_recommendations_for_repository(repository, query):
    full_query_string = '{query_string} help-wanted-issues:>3'.format(query_string=query['string'])
    response = make_request(interested_in_repositories_query, variables={'queryString': full_query_string})
    return [edge['node'] for edge in response['data']['search']['edges']]


@api.route('/recommendations')
def get_recommendations():
    contributed_to_repositories = get_contributed_to_repositories()
    recommendations = []

    for repository in contributed_to_repositories['data']['viewer']['repositoriesContributedTo']['edges']:
        query = generate_query_from_repository(repository['node'])
        repository['node']['reason'] = query['reason']
        repository_recommendations = [repository['node']]
        repository_recommendations.extend(get_recommendations_for_repository(repository['node'], query))
        recommendations.append(repository_recommendations)

    return jsonify(recommendations)
