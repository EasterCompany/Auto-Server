# Standard Library Imports
from sys import path
from json import loads
from time import sleep
from os import chdir, system
from threading import Thread
from datetime import datetime

# Project Specific Imports
from web.settings import BASE_DIR

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
    [index_file_content.replace('{#' + tag + '#}', meta_data[tag]) for tag in meta_data]
    # Write new index.html file content
    index_file = open(index_path, 'w')
    index_file.write(index_file_content)
    index_file.close()


# Client thread function
def client(app_data, build=False):
    chdir(app_data['path'])
    if build and 'build' in app_data:
        system('npm run build')
        update_client_meta_data(app_data['path'])
    elif 'start' in app_data:
        system('npm run start')
    chdir(BASE_DIR)


# Create client thread
new_client = lambda app_name, app_data, build: Thread(
    None,
    client,
    app_name,
    (app_data, build)
)

# All clients data from config file
clients_file = open(path[0] + '/.tools_config/clients.json')
clients_json = loads(clients_file.read())
clients_file.close()


# Run client
def run(name, build, new_thread):
    client_data = clients_json[name]
    thread = new_client(name, client_data, build)
    if new_thread:
        thread.start()              # Start thread
        sleep(3)                    # Give NPM time to collect package.json
        return chdir(BASE_DIR)      # Return to root directory
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


# Module error message
def error_message():
    return print('''
    `CLIENTS` tool requires atleast one argument beggining with `-`

        ./o runclient -client_name
        ./o build -client_name

    or use -all to effect all clients

        ./o runclient -all
        ./o build -all
    ''')
