import requests
import os
import sys
import json
import yaml
import stat

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

            local_path = "projects/" + repo_name + "/" + item['path']

          
            if (item['type'] == 'dir'):    
                if not os.path.exists(local_path):
                    os.makedirs(local_path, mode=0o777)

                recursive_md_fetch(item['path'], repo_name, token)
            
            elif item['type'] == 'file' and item['name'].endswith('.md'):
                markdown_paths.append(item['path'])
                file_content = requests.get(item['download_url'])
                print(file_content.content)
                with open(local_path, 'wb') as f:
                    f.write(file_content.content)


def generate_html_file(subproject_name):
    html_content = f"""---
layout: default
title: {subproject_name}
---

{{% assign subproject_obj = site.data.projects["{subproject_name}"] %}}

<body>
    <div class="card-deck">
        {{% for instruction in subproject_obj[0].instructions %}}
            <div class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">{{{{ instruction.title }}}}</h5>
                    <a href="{{{{ instruction.url }}}}" class="btn btn-primary">Read More</a>
                </div>
            </div>
        {{% endfor %}}
    </div>
</body>
"""

    directory = f"projects/{subproject_name}"
    os.makedirs(directory, exist_ok=True)
    
    with open(f"{directory}/{subproject_name}.html", "w") as file:
        file.write(html_content)



def add_subproject(subproject_name, markdown_files):
    # Load existing data from projects.yaml
    with open('_data/projects.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # Generate instructions based on markdownFiles
    instructions = []
    for markdown_file in markdown_files:
        instruction_title = markdown_file.split('.')[0]  # Remove file extension
        instruction_url = f'/projects/{subproject_name}/{instruction_title}'
        instructions.append({'title': instruction_title, 'url': instruction_url})

    # Generate subproject data
    subproject_data = {
        'title': f'Subproject {subproject_name}',
        'project_root': f'/projects/{subproject_name}/{subproject_name}.html',
        'instructions': instructions,
        'subproject_dir': subproject_name
    }

    # Add subproject to data
    data[subproject_name] = [subproject_data]

    # Write updated data back to projects.yaml
    with open('_data/projects.yaml', 'w') as file:
        yaml.dump(data, file)


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
            if repo['name'] != "testorgleonb.github.io":
                markdown_paths = []
                repo_name = repo['name']
                print(f"Processing repository {repo_name}")
                fetch_md_files(repo_name, token)
                print(markdown_paths)
                add_subproject(repo['name'], markdown_paths)
                generate_html_file(repo['name'])