import json
from sys import executable
from os.path import exists
from os import system, name as os, scandir, mkdir

o_script = '''#!/bin/bash
clear
{python} manage.py tools $1 $2 $3 $4 $5
exit
'''.format(python=executable)


def create_o_script():
    f = open('./o', 'w+')
    f.write(o_script)
    f.close()
    if os == 'posix':
        system('chmod +x ./o')


def fetch_clients(project_path='.'):
    client_paths  = [
        f.path for f in scandir(project_path + "/clients") if f.is_dir()
    ]
    clients = {}

    for client in client_paths:
        files = [
            f.path.split("/")[-1] for f in scandir(client) if not f.is_dir()
        ]
        node = "package.json" in files
        scripts = {
            "test": None,
            "start": None,
            "build": None,
            "version": None,
        }

        if node:
            package = open(client + "/package.json")
            package_json = json.load(package)
            if 'version' in package_json:
                scripts['version'] = package_json['version']
            for key in package_json["scripts"]:
                if key in scripts:
                    scripts[key] = package_json["scripts"][key]

        clients[client.split("/")[-1]] = {
            "path": client,
            "node": node,
            "test": scripts["test"],
            "start": scripts["start"],
            "build": scripts["build"],
            "version": scripts["version"]
        }

    return clients


def clients_json(project_path='.'):
    if not exists(project_path + '/.tools_config'):
        mkdir(project_path + '/.tools_config')
    clients_data = fetch_clients(project_path)

    with open(project_path + '/.tools_config/clients.json', 'w') as clients_file:
        json.dump(
            clients_data,
            clients_file,
            indent=2
        )
