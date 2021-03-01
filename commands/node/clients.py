# Standard Library Imports
from time import sleep
from os import chdir, system
from threading import Thread
from datetime import datetime

# Project Specific Imports
from web.settings import BASE_DIR


# Client build meta data
def update_client_meta_data():

    # Read index.html file content
    index_path = BASE_DIR + '/clients/Global/build/index.html'
    index_file = open(index_path)
    index_file_content = index_file.read()
    index_file.close()

    # Write new index.html file content
    index_file = open(index_path, 'w')
    index_file.write(
        index_file_content.replace(
            '{#time_of_last_build#}',
            datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
        )
    )
    index_file.close()


# Client thread function
def client(make_build=False):
    chdir(BASE_DIR + '/clients/Global')
    if make_build:
        system('npm run build')
        update_client_meta_data()
    else:
        system('npm run start')
    chdir(BASE_DIR)


# Client thread
thread = Thread(
    None,
    client,
    'react-client',
    ()
)


build = lambda: client(make_build=True)
run = lambda: thread.run()


def start():
    thread.start()              # Start thread
    sleep(3)                    # Give NPM time to collect package.json
    return chdir(BASE_DIR)      # Return to root directory
