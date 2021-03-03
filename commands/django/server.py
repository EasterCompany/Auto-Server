# Standard Library Imports
from os import system
from threading import Thread
from sys import executable, path


# Server thread function
def _server(start=True, migrate=False):

    def cmd(_cmd):
        system("{python} {dir}/manage.py {command}".\
            format(python=executable, dir=path[0], command=_cmd)
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
