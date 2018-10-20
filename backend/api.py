from json import JSONDecodeError, dumps

from flask import Blueprint, Response, jsonify
from flask_dance.contrib.github import github

api = Blueprint('api', __name__)


def make_request(query, variables=None):
    resp = github.post('/graphql', json={'query': query, 'variables': dumps(variables)})

    try:
        return resp.json()
    except JSONDecodeError:
        return Response(resp.text, status=503)


def get_contributed_to_repositories():
    return make_request("""
    fragment contributedToDetails on Repository {
      name
      url
      stargazers{
        totalCount
      }
      forkCount
      shortDescriptionHTML
      languages(first:3, orderBy:{field:SIZE, direction: DESC}) {
        edges {
          node {
            name
            color
          }
        }
      }
      repositoryTopics(first:20){
        edges{
          node{
            topic{
              name
              relatedTopics{
                name
              }
              stargazers{
                totalCount
              }
            }
          }
        }
      }
    }

    query contributedToRepositories {
      viewer{
        repositoriesContributedTo(first:3, orderBy:{field:STARGAZERS,direction:DESC}){
          edges{
            node{
              ...contributedToDetails
            }
          }
        }
      }
    }
    """)


def get_recommendations_for_repository(repository):
    response = make_request("""
    
fragment contributedToDetails on Repository {
  name
  url
  stargazers{
    totalCount
  }
  forkCount
  shortDescriptionHTML
  languages(first:3, orderBy:{field:SIZE, direction: DESC}) {
    edges {
      node {
        name
        color
      }
    }
  }
  repositoryTopics(first:20){
    edges{
      node{
        topic{
          name
          relatedTopics{
            name
          }
          stargazers{
            totalCount
          }
        }
      }
    }
  }
}

fragment interestedInDetails on Repository {
  ...contributedToDetails
  openIssues: issues(states:OPEN, first:5, orderBy:{field:CREATED_AT, direction:ASC}){
    totalCount
    edges{
      node{
        url
        title
        bodyHTML
        reactions{
          totalCount
        }
      }
    }
  }
}

query interestedInRepositories($queryString: String!) {
  search(query:$queryString, type:REPOSITORY, first:5){
    edges{
      node{
        ... on Repository {
          name
          ...interestedInDetails
        }
      }
    }
  }
}
""", variables={'queryString': 'language:Python'})

    return [edge['node'] for edge in response['data']['search']['edges']]


@api.route('/recommendations')
def get_recommendations():
    contributed_to_repositories = get_contributed_to_repositories()
    recommendations = []
    print(contributed_to_repositories)

    for repository in contributed_to_repositories['data']['viewer']['repositoriesContributedTo']['edges']:
        repository_recommendations = [repository['node']]
        repository_recommendations.extend(get_recommendations_for_repository(repository['node']))
        recommendations.append(repository_recommendations)

    return jsonify(recommendations)
