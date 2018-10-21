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
    repositoriesContributedTo(first:4, orderBy:{{field:STARGAZERS,direction:DESC}}){{
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
  openIssues: issues(states:OPEN, labels: ["help wanted", "beginner"], first:5, orderBy:{{field:COMMENTS, direction:DESC}}){{
    totalCount
    edges{{
      node{{
        url
        title
        bodyHTML
        reactions{{
          totalCount
        }}
        labels(first:10){{
          edges{{
            node{{
              name
            }}
          }}
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

beginners_fragment = """
{contributed_to_details_fragment}

fragment interestedInDetails on Repository {{
  ...contributedToDetails
  openIssues: issues(states:OPEN, labels: ["beginner-friendly", "easy", "starter", "beginner friendly", "beginner", "good first issue"], first:5, orderBy:{{field:COMMENTS, direction:DESC}}){{
    totalCount
    edges{{
      node{{
        url
        title
        bodyHTML
        reactions{{
          totalCount
        }}
        labels(first:10){{
          edges{{
            node{{
              name
            }}
          }}
        }}
      }}
    }}
  }}
}}
""".format(contributed_to_details_fragment=contributed_to_details_fragment)

beginners_query = """
{beginners_fragment}

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
""".format(beginners_fragment=beginners_fragment)