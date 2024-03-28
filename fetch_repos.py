import requests
import yaml

markdown_paths = []

org_name="TestOrgLeonB"

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

def fetch_yaml_conf(repo_name, token):
    try:
        headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
        }
        yaml_url = f"https://raw.githubusercontent.com/{org_name}/{repo_name}/main/doc/doc_conf.yaml"

        # Send GET request to fetch the YAML content
        response = requests.get(yaml_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse YAML content
            yaml_content = yaml.safe_load(response.text)

            # Read parameters from YAML
            url = yaml_content.get('url')
            icon = yaml_content.get('icon')
            title = yaml_content.get('title')
            description = yaml_content.get('description')


            return (
                    title,
                    icon,
                    url,
                    description
                )
        else:
            print(f"Failed to fetch doc_conf.yaml: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def add_subproject(subproject_name, subproject_conf):
    # Load existing data from projects.yaml
    with open('testorgleonb.github.io/_data/projects.yaml', 'r') as file:
        data = yaml.safe_load(file)


    print(data)
    # Generate subproject data
    subproject_data = {
        'title': subproject_conf[0],
        'icon': subproject_conf[1] ,
        'url': subproject_conf[2],
        'description': subproject_conf[3]
    }

    # Add subproject to data
    if (data):
        data[subproject_name] = subproject_data
    else:
        data = {subproject_name: subproject_data}
    # Write updated data back to projects.yaml
    with open('testorgleonb.github.io/_data/projects.yaml', 'w') as file:
        yaml.dump(data, file)


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python fetch_repos.py <organization_name> <GitHub_token>")
    #     sys.exit(1)

    # org_name = sys.argv[1]
    # token = sys.argv[2]


    repositories = fetch_repositories(org_name, token)
    if repositories:
        for repo in repositories:
            if repo['name'] != "testorgleonb.github.io":
                markdown_paths = []
                repo_name = repo['name']
                print(f"Processing repository {repo_name}")
                project_conf = fetch_yaml_conf(repo_name, token)
                add_subproject(repo_name, project_conf)
             