# Standard library imports
import requests
from sys import path
from json import loads
from os.path import exists
from datetime import datetime, timedelta
# Local app imports
from tools.library import console

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
    if token == '':
        print('''
    `SERVER TOOLS` requires an API token &
    username in your .config/secret.json file
    '''
        )
        exit()
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
    if domain == '' or secret == '':
        print('''
    `SERVER TOOLS` requires a target domain &
    secret key in your .config/secret.json file
    '''
        )
        exit()
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
    print('\n', ':------ TAKS INFO ------:\n')
    for point in data:
        print(point + ':\n    ', data[point])
    print()


def get_app_data():
    data = fetch_api('webapps')
    print('\n', ':------------ WEBAPP INFO -----------:\n')
    for app in data:
        print(
            ' ', app['user'], '-',  app['id'], '\n',
            ' URL:', app['domain_name'], '\n',
            ' HTTPS:', app['force_https'], '\n',
            ' Python:', app['python_version'], '\n',
            ' Source:', app['source_directory'], '\n',
            ' Working:', app['working_directory'], '\n',
        )
    print(' :-------------------------------------:\n')


def get_con_data():
    data = fetch_api('consoles')
    print('\n', ':-------- CONSOLE LIST --------:\n')

    for con in data:
        print(
            ' ', con['name'], '-',  con['id'], '\n',
            ' Type:', con['executable'], '\n'
        )

    print(' :------------------------------:\n')


def get_cpu_data():
    data = fetch_api('cpu')
    print('\n', ':------ CPU QUOTA INFO ------:\n')

    cpu_limit = int(data['daily_cpu_limit_seconds'])
    cpu_usage = round(
        float(data['daily_cpu_total_usage_seconds']),
        2
    )
    cpu_perct = round(
        (100 / cpu_limit) * cpu_usage,
        1
    )

    cpu_status = 'green'
    if cpu_perct >= 80:
        cpu_status = 'red'
    elif cpu_perct >= 50:
        cpu_status = 'yellow'

    print(
        '  Daily usage\n',
        '   ', str(cpu_usage) + 's', '/', str(cpu_limit) + 's',
        '   ', console.col(str(cpu_perct) + '%\n', cpu_status)
    )

    cpu_reset_datetime = datetime.strptime(
        data['next_reset_time'],
        '%Y-%m-%dT%H:%M:%S.%f'
    )
    cur_datetime = datetime.now()
    cpu_reset_at = str(cpu_reset_datetime - cur_datetime)
    cpu_reset_in = datetime.strptime(cpu_reset_at, '%H:%M:%S.%f').\
        strftime('%H:%M:%S')

    print(
        '  Time to reset\n',
        '   ', cpu_reset_in, '     ',
        cpu_reset_datetime.strftime('%H:%M:%S'),'\n'
    )
    print(' :----------------------------:\n')


def post_reload_req():
    print('\nReloading', domain, '...\n')
    data = fetch_api('webapps', args=(domain, 'reload'), method='POST')
    print('status:', console.colour_status_code(data['status']), '\n')


def post_upgrade_req():
    print('\nUpgrading', domain, '...\n')
    data = fetch_domain('upgrade')
    print('status:', console.colour_status_code(data['status']), '\n')


def error_message():
    return print('''
        `PA API` tool requires a single argument beggining with `-`

        ./o server -apps
        ./o server -cpu
        ./o server -consoles
        ./o server -tasks
        ./o server -upgrade
    ''')
