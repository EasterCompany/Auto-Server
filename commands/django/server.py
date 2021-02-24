# Standard Library Imports
from os import system
from sys import executable
from threading import Thread

# Project Specific Imports
from web.settings import BASE_DIR


# Server thread function
def _server(start=True, migrate=False):

    def cmd(_cmd):
        system("{python} {dir}/manage.py {command}".\
            format(python=executable, dir=BASE_DIR, command=_cmd)
        )

    if migrate:
        cmd('makemigrations')
        cmd('migrate')
    if start:
        cmd('runserver')


# Server thread
thread = Thread(
    None,
    _server,
    'django-server',
    ()
)

# Server migration function
migrate_database = lambda: _server(start=False, migrate=True)


def run():
    migrate_database()
    return thread.run()


def start():
    migrate_database()
    return thread.start()
