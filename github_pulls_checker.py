import requests
from datetime import datetime

# https://docs.github.com/en/github/searching-for-information-on-github/searching-issues-and-pull-requests#search-within-a-users-or-organizations-repositories

repos_name = ['hermes-backend', 'hermes53-ansible', 'hermes53-api-router', 'hermes53-aws-api', 'hermes53-backend','hermes53-healthchecker',
'hermes53-integration-tests', 'hermes53-spc-api', 'hermes53-spc-gw', 'hermes53-storage', 'hermes53-tools']

organization = 'cloud-pi'
headers = {'Authorization': 'token abc487e9aee6e000ef59b0da75da9d56a06d78bb'}
params = {
    "state": "closed",
}

for_year = '2021'
if for_year:
    print('Searching for closed Pull Requests for {} year.\n'.format(for_year))

for repo in repos_name:
    print('Repository: {}'.format(repo))
    url = 'https://api.github.com/repos/{}/{}/pulls'.format(organization, repo)
    r = requests.get(url=url, headers=headers, params=params)

    if r.status_code != 200:
        print('Unable to get pull requests,  http error: {}.'.format(r.status_code))
        break

    pulls = r.json()
    if len(pulls) == 0:
        print('Unable to get any pull requests for given repo.')
        break

    for pull in pulls:
        # From RFC3339 -> Human readable
        created_at = str(datetime.strptime(pull['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
        closed_at = str(datetime.strptime(pull['closed_at'], '%Y-%m-%dT%H:%M:%SZ'))
        created_year = created_at.split('-')[0]
        if created_year == for_year or for_year is None:
            print('User: {}, created_at: {}, closed_at: {}, title: {}'.format(
                                                                                 pull['user']['login'],
                                                                                 created_at,
                                                                                 closed_at,
                                                                                 pull['title']))
    print('----------------------------\n')
