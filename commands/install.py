# Standard library imports
import json
from sys import executable, path
from os.path import exists, join as pathjoin
from os import system, name as os, scandir, mkdir

# Django module imports
from django.core.management.utils import get_random_secret_key

# --------------------------- CREATE & CONFIRM CONFIG EXISTS --------------------------- #
def __init_conifg_directory__(project_path='.'):
    if not exists(project_path + '/.config'):
        mkdir(project_path + '/.config')

# -------------------------- CREATE & CONFIRM LOGS DIR EXISTS -------------------------- #
def __init_logs_directory__(project_path='.'):
    if not exists(project_path + '/.logs'): mkdir(project_path + '/.logs')
    if not exists(project_path + '/.logs/requests.json'):
        req_json = open(project_path + '/.logs/requests.json', 'w+')
        req_json.write('{\n}')
        req_json.close()

# -------------------------- CONFIRM CONFIG JSON FILE EXISTS --------------------------- #
def dump_json(filename, data, project_path='.'):
    file_path = project_path + '/.config/' + filename + '.json'
    with open(file_path, 'w') as conf_file:
        json.dump(
            data,
            conf_file,
            indent=2
        )

def install_file(filename, destination, project_path='.'):
    print('Installing', filename, 'to', destination, '...')
    base = open(project_path + '/tools/assets/' + filename)
    newf = open(project_path + destination + '/' + filename, 'w+')
    newf.write(base.read())
    base.close(), newf.close()

def create_o_script(project_path='.'):
    print('Generating ./o script...')
    o_script = \
'''#!/bin/bash
clear
{python} manage.py tools $1 $2 $3 $4 $5
exit
'''.format(python=executable)
    f = open(project_path + '/o', 'w+')
    f.write(o_script)
    f.close()
    if os == 'posix':
        system('chmod +x ' + project_path + '/o')

def make_clients_config(project_path='.'):
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

        if client.split("/")[-1] != 'shared':
            clients[client.split("/")[-1]] = {
                "path": client,
                "node": node,
                "test": scripts["test"],
                "start": scripts["start"],
                "build": scripts["build"],
                "version": scripts["version"]
            }
    dump_json('clients', clients, project_path)

def make_server_config(project_path='.'):
    print('Generating server config...')
    server_core_data = {
        "DEBUG": True,
        "STANDALONE": False,
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
            'whitenoise.middleware.WhiteNoiseMiddleware'
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
        "STATIC_ROOT": pathjoin(path[0], 'static'),
        "CORS_ORIGIN_ALLOW_ALL": False,
    }

    def is_app(f):
        ignored_dirs = (
            'clients', 'tools', 'web', 'static', 'media', 'tasks'
        )
        if f.is_dir() and not f.name.startswith('.') and not f.name in ignored_dirs:
            return True
        return False

    installed_apps = [
        f.path.split("/")[-1] for f in scandir(project_path) if is_app(f)
    ]
    server_core_data["INSTALLED_APPS"] += installed_apps
    return dump_json('server', server_core_data, project_path)

def django_files(project_path='.'):
    install_file('manage.py', '/', project_path)
    install_file('settings.py', '/web', project_path)

def secrets_file(project_path='.'):
    print('Generating secrets config...')
    token_data = {
        "SECRET_KEY": get_random_secret_key(),
        "PA_USER_ID": "",
        "PA_API_KEY": "",
        "DOMAIN_URL": "",
        "EMAIL_USER": "",
        "EMAIL_PASS": ""
    }
    return dump_json('secret', token_data, project_path)
