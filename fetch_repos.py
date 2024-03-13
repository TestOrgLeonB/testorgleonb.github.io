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

def fetch_md_files(repo_name, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/TestOrgLeonB/{repo_name}/contents/doc'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        md_files = []
        for item in content:
            if item['type'] == 'file' and item['name'].endswith('.md'):
                md_files.append(item['path'])

        print(f"My Markdown file {md_files}")
        return md_files
    else:
        print(f"Failed to fetch .md files from repository {repo_name}. Status code: {response.status_code}")
        return []

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fetch_repos.py <organization_name> <GitHub_token>")
        sys.exit(1)

    org_name = sys.argv[1]
    token = sys.argv[2]
    repositories = fetch_repositories(org_name, token)
    if repositories:
        for repo in repositories:
            repo_name = repo['name']
            print(f"Processing repository {repo_name}")
            md_files = fetch_md_files(repo_name, token)
            for md_file in md_files:
                print(f"Found .md file in repository {repo_name}: {md_file}")
