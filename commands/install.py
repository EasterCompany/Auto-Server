# Standard Library Imports
import json
from sys import executable
from os.path import exists
from os import system, name as os, scandir, mkdir

o_script = '''#!/bin/bash
clear
{python} manage.py tools $1 $2 $3 $4 $5
exit
'''.format(python=executable)


def create_o_script(project_path='.'):
    f = open(project_path + '/o', 'w+')
    f.write(o_script)
    f.close()
    if os == 'posix':
        system('chmod +x ' + project_path + '/o')


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
    if not exists(project_path + '/config'):
        mkdir(project_path + '/config')
    clients_data = fetch_clients(project_path)

    with open(project_path + '/config/clients.json', 'w') as clients_file:
        json.dump(
            clients_data,
            clients_file,
            indent=2
        )


def make_server_config(project_path='.'):
    if not exists(project_path + '/config'):
        mkdir(project_path + '/config')

    server_core_data = {
        "LANGUAGE_CODE": 'en-gb',
        "TIME_ZONE": 'UTC',
        "ALLOWED_HOSTS": [
            '127.0.0.1',
            'localhost'
        ],
        "INSTALLED_APPS": [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'corsheaders',
        ],
        "MIDDLEWARE": [
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        "ROOT_URLCONF": 'web.urls',
        "WSGI_APPLICATION": 'web.wsgi.application',
        "BACKEND_TEMPLATE": 'django.template.backends.django.DjangoTemplates',
        "OPTIONS_TEMPLATE": {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
        "APP_DIRS_TEMPLATE": True,
        "STATIC_URL": '/static/',
        "CORS_ORIGIN_ALLOW_ALL": False,
    }

    def is_app(f):
        ignored_dirs = (
            'clients', 'config', 'tools', 'web', 'static', 'media'
        )
        if f.is_dir() and not f.name.startswith('.') and not f.name in ignored_dirs:
            return True
        return False

    installed_apps = [
        f.path.split("/")[-1] for f in scandir(project_path) if is_app(f)
    ]

    server_core_data["INSTALLED_APPS"] += installed_apps

    with open(project_path + '/config/server.json', 'w') as conf_file:
        json.dump(
            server_core_data,
            conf_file,
            indent=2
        )


def manage_py(project_path='.'):
    manage_file = open(project_path + '/tools/assets/manage.py')
    manage_orig = open(project_path + '/manage.py', 'w+')
    manage_orig.write(manage_file.read())
    manage_file.close(), manage_orig.close()


def settings_py(project_path='.'):
    settings_file = open(project_path + '/tools/assets/settings.py')
    settings_orig = open(project_path + '/web/settings.py', 'w+')
    settings_orig.write(settings_file.read())
    settings_file.close(), settings_orig.close()
