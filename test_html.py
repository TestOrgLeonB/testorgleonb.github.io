import os
import yaml

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

    directory = f"testorgleonb.github.io/projects/{subproject_name}"
    os.makedirs(directory, exist_ok=True)
    
    with open(f"{directory}/{subproject_name}.html", "w") as file:
        file.write(html_content)

# Example usage:
# generate_html_file("subproject3")


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

# Example usage:
markdown_files = ['instruction1.md', 'instruction2.md','instruction3.md']  # Example list of instruction markdown files
add_subproject('subproject3', markdown_files)