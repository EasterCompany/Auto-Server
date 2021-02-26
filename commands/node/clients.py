# Standard Library Imports
from time import sleep
from os import chdir, system
from threading import Thread

# Project Specific Imports
from web.settings import BASE_DIR


# Client thread function
def client(make_build=False):
    chdir(BASE_DIR + '/clients/global')
    if make_build:
        system('npm run build')
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
