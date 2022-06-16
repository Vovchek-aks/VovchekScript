import os

name = input('Project name:\n')

if os.path.exists(f'projects/{name}'):
    input(f'Project with name "{name}" already exists')
    exit(0)

os.mkdir(f'projects/{name}')

open(f'projects/{name}/main.vs', 'w').close()

f = open(f'projects/{name}/run.py', 'w')
f.write('from core.main import run\n\n\nrun("main.vs", absolute=True)\n')

input('Project created successful')
