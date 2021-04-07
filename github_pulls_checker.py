import requests

# https://docs.github.com/en/github/searching-for-information-on-github/searching-issues-and-pull-requests#search-within-a-users-or-organizations-repositories

issues_api = 'https://api.github.com/search/issues?q=org:github'
username = 'e-wrobel'
repo_name = 'my-blog'
url = '{}/{}/pulls'.format(issues_api, repo_name)
r = requests.get(url)

if r.status_code != 200:
    print('Unable to get pull requests,  http error: {}.'.format(r.status_code))
    exit(0)

pulls = r.json()['items']
if len(pulls) == 0:
    print('Unable to get any pull requests for given repo.')
    exit(0)

for pull in pulls:
    print('Id: {}, user: {}, created_at: {}, closed_at: {}, title: {}, PR status: {}'.format(pull['id'],
                                                                             pull['user']['login'],
                                                                             pull['created_at'],
                                                                             pull['closed_at'],
                                                                             pull['title'],
                                                                             pull['state']))
