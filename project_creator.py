import os


name = input('Project name:\n')

if os.path.exists(f'projects/{name}'):
    input(f'project with name "{name}" already exists')
    exit(0)

os.mkdir(f'projects/{name}')
os.mkdir(f'projects/{name}/side_code')

open(f'projects/{name}/main.vs', 'w').close()

f = open(f'projects/{name}/libs.json', 'w')
f.write('{\n\t"libs": []\n}\n')

input('project created successful')
