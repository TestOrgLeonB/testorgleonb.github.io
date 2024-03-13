import requests
import os
import sys
import json

def fetch_repositories(org_name, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch repositories. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fetch_repos.py <organization_name> <GitHub_token>")
        sys.exit(1)

    org_name = sys.argv[1]
    token = sys.argv[2]
    repositories = fetch_repositories(org_name, token)
    if repositories:
        print(json.dumps(repositories))
