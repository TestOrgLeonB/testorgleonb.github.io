import requests
import os
import sys
import json


markdown_paths = []

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

    recursive_md_fetch("doc", repo_name, token)


def recursive_md_fetch(current_dir, repo_name, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/TestOrgLeonB/{repo_name}/contents/{current_dir}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.json()
        for item in content:
            print(item)
            if (item['type'] == 'dir'):
                recursive_md_fetch(item['path'], repo_name, token)
            
            elif item['type'] == 'file' and item['name'].endswith('.md'):
                print(item['path'])
                markdown_paths.append(item['path'])
        
        
if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python fetch_repos.py <organization_name> <GitHub_token>")
    #     sys.exit(1)

    # org_name = sys.argv[1]
    # token = sys.argv[2]

    org_name="TestOrgLeonB"
    token = "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"

    repositories = fetch_repositories(org_name, token)
    if repositories:
        for repo in repositories:
            markdown_paths = []
            repo_name = repo['name']
            print(f"Processing repository {repo_name}")
            md_files = fetch_md_files(repo_name, token)
            print(markdown_paths)
            