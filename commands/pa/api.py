import requests
from sys import path
from json import loads
from os.path import exists

# GET CONFIGURATION SECRETS
if exists(path[0] + '/.config/secret.json'):
    secret_file = open(path[0] + '/.config/secret.json')
    secret_data = loads(secret_file.read())
    secret_file.close()
else:
    secret_data = {
        'PA_USER_ID': '',
        'PA_API_KEY': '',
        'DOMAIN_URL': ''
    }

# SET HOST INFORMATION
username = secret_data['PA_USER_ID']
token = secret_data['PA_API_KEY']
domain = secret_data['DOMAIN_URL']
secret = secret_data['SECRET_KEY']


def fetch_api(api, args=None, method='GET'):
    if args is not None:
        args = '/'.join(args) + '/'
    else:
        args = ''
    if method == 'GET': func = requests.get
    elif method == 'POST': func = requests.post
    response = func(
        'https://eu.pythonanywhere.com/api/v0/user/{username}/{api}/{args}'.format(
            username=username,
            api=api,
            args=args
        ),
        headers={
            'Authorization': 'Token {token}'.format(token=token)
        }
    )
    if not response.status_code == 200:
        return print('Got unexpected status code {}: {!r}'.format(
                response.status_code,
                response.content
            )
        ), exit()
    return loads(response.content)


def fetch_domain(api, args=None, method='GET'):
    if args is not None:
        args = '/' + '/'.join(args) + '/'
    else:
        args = ''
    if method == 'GET': func = requests.get
    elif method == 'POST': func = requests.post
    response = func(
        'https://{domain}/api/olt/{api}{args}'.format(
            domain=domain,
            api=api,
            args=args
        ),
        headers={
            'secret': '{key}'.format(key=secret)
        }
    )
    if not response.status_code == 200:
        return print('Got unexpected status code {}: {!r}'.format(
                response.status_code,
                response.content
            )
        ), exit()
    return loads(response.content)


def get_task_data():
    data = fetch_api('always_on')
    print('\n', 'Tasks info ---:\n')
    for point in data:
        print(point + ':\n    ', data[point])
    print()

def get_app_data():
    data = fetch_api('webapps')
    print('\n', 'App info ---:\n')
    for app in data:
        for point in app:
            print(point + ':\n    ', app[point])
        print()

def get_con_data():
    data = fetch_api('consoles')
    print('\n', 'Consoles list ---:\n')
    for point in data:
        print(point + ':\n    ', data[point])
    print()

def get_cpu_data():
    data = fetch_api('cpu')
    print('\n', 'CPU quota info ---:\n')
    for point in data:
        print(point + ':\n    ', data[point])
    print()

def post_reload_req():
    print('\nReloading', domain, '...\n')
    data = fetch_api(
        'webapps',
        args=(domain, 'reload'),
        method='POST'
    )
    print('status:', data['status'], '\n')

def post_upgrade_req():
    print('\nUpgrading', domain, '...\n')
    data = fetch_domain('upgrade')
    print('status:', data['status'], '\n')


def error_message():
    return print('''
        `PA API` tool requires a single argument beggining with `-`

        ./o server -apps
        ./o server -cpu
        ./o server -consoles
        ./o server -tasks
    ''')
