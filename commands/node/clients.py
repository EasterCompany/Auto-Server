# Standard Library Imports
from sys import path
from json import loads
from time import sleep
from shutil import rmtree
from os.path import exists
from threading import Thread
from datetime import datetime
from os import chdir, system, rename, remove

# Tools import
from tools.library import console

# Variable app meta data
meta_data = {
    'time_of_last_build': datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
}


# Client build meta data
def update_client_meta_data(app_path):
    # Read index.html file content
    index_path = app_path + '/build/index.html'
    index_file = open(index_path)
    index_file_content = index_file.read()
    index_file.close()
    # Iterate over all variable meta data
    for tag in meta_data:
        index_file_content = \
            index_file_content.replace('{#' + tag + '#}', meta_data[tag])
    # Write new index.html file content
    index_file = open(index_path, 'w+')
    index_file.write(index_file_content)
    index_file.close()
    # Rename and Remove build files for indexing
    rename(app_path + '/build/index.html', app_path + '/build/index')
    if exists(app_path + '/build/200.html'):
        remove(app_path + '/build/200.html')


# Client thread function
def client(app_data, build=False):
    chdir(app_data['path'])
    if build and 'build' in app_data:
        system('npm run build')
        update_client_meta_data(app_data['path'])
    elif 'start' in app_data:
        system('npm run start')
    chdir(path[0])


# Create client thread
new_client = lambda app_name, app_data, build: Thread(
    None,
    client,
    app_name,
    (app_data, build)
)

# All clients data from config file
clients_file = open(path[0] + '/.config/clients.json')
clients_json = loads(clients_file.read())
clients_file.close()


# Install client
def install(target=None):

    def run_install(client_path):
        chdir(client_path)
        system('npm install')

    if target is None:
        for client in clients_json:
            print('\n', client, '----------------')
            run_install(clients_json[client]['path'])
        print()
    else:
        run_install(clients_json[target]['path'])

    return chdir(path[0])


# Run client
def run(name, build, new_thread):
    client_data = clients_json[name]
    thread = new_client(name, client_data, build)
    if new_thread:
        thread.start()              # Start thread
        sleep(3)                    # Give NPM time to collect package.json
        return chdir(path[0])       # Return to root directory
    return thread.run()             # ELSE: Run on main thread


# Run all clients on a separate thread except the last one
def run_all(none_on_main_thread=False):
    for index, client in enumerate(clients_json):
        if index < len(clients_json) - 1 or none_on_main_thread:
            run(client, build=False, new_thread=True)
        else:
            run(client, build=False, new_thread=False)
    sleep(5)
    system('clear')
    return print('Running all clients...\n')


# Build specific client on the main thread
def build(name):
    return run(name, build=True, new_thread=False)


# Build all clients on the main thread
def build_all():
    for client in clients_json:
        run(client, build=True, new_thread=False)


# Create new client
def create(name):

    # Make directory checks
    if exists('clients/' + name):
        return print("\n ABORTED: %s already exists \n" % name)

    # Fetch template from github
    system('''
            echo '' && cd clients &&
            git clone git@github.com:EasterCompany/React-Template.git {name} &&
            cd .. && echo ''
        '''.format(name=name)
    )

    # De-git repository
    print('De-git repository...')
    remove('clients/{name}/README.md'.format(name=name))
    remove('clients/{name}/.gitignore'.format(name=name))
    rmtree('clients/{name}/.git'.format(name=name))

    # Update meta_data
    print('Update index data...')
    rename(
        'clients/{name}/public/static/app-name'.format(name=name),
        'clients/{name}/public/static/{name}'.format(name=name)
    )
    with open('clients/{name}/public/index.html'.format(name=name)) as index_content:
        content = index_content.read()
        content = content.replace('{#app_name#}', name)
        new_file = open('clients/%s/public/index.html' % name, 'w')
        new_file.write(content), new_file.close()

    # Update manifest
    print('Update manifest data...')
    with open('clients/{name}/public/manifest.json'.format(name=name)) as manifest:
        content = manifest.read()
        content = content.replace('app-name', name)
        new_file = open('clients/%s/public/manifest.json' % name, 'w')
        new_file.write(content), new_file.close()

    # Update environment variables
    print('Update environment data...\n')
    clients_data = {}
    next_port = 8100
    with open('.config/clients.json') as clients_json:
        clients_data = loads(clients_json.read())
        next_port += len(clients_data)
    with open('clients/%s/.env' % name, 'w+') as env_file:
        env_file.write('PORT=%s' % next_port)

    print(console.col(' Done!', 'green'))
    print('\ninstall this app with `./o install -client -%s` \n' % name)


# Module error message
def error_message():
    return print('''
    `CLIENTS` tool requires atleast one argument beggining with `-`

        ./o runclient -client_name
        ./o build -client_name
        ./o create -client_name

    or use -all to effect all clients

        ./o runclient -all
        ./o build -all
    ''')
