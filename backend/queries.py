contributed_to_details_fragment = """
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
  repositoryTopics(first:5){
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
"""

contributed_to_repositories_query = """
{contributed_to_details_fragment}

query contributedToRepositories {{
  viewer{{
    repositoriesContributedTo(first:3, orderBy:{{field:STARGAZERS,direction:DESC}}){{
      edges{{
        node{{
          ...contributedToDetails
        }}
      }}
    }}
  }}
}}
""".format(contributed_to_details_fragment=contributed_to_details_fragment)

interested_in_details_fragment = """
{contributed_to_details_fragment}

fragment interestedInDetails on Repository {{
  ...contributedToDetails
  openIssues: issues(states:OPEN, first:3, orderBy:{{field:CREATED_AT, direction:ASC}}){{
    totalCount
    edges{{
      node{{
        url
        title
        bodyHTML
        reactions{{
          totalCount
        }}
      }}
    }}
  }}
}}
""".format(contributed_to_details_fragment=contributed_to_details_fragment)

interested_in_repositories_query = """
{interested_in_details_fragment}

query interestedInRepositories($queryString: String!) {{
  search(query:$queryString, type:REPOSITORY, first:3){{
    edges{{
      node{{
        ... on Repository {{
          name
          ...interestedInDetails
        }}
      }}
    }}
  }}
}}
""".format(interested_in_details_fragment=interested_in_details_fragment)