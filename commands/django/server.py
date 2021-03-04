# Standard Library Imports
from os import system
from threading import Thread
from sys import executable, path


# Server thread function
def _server(start=True, migrate=False, collectstatic=False):

    def cmd(_cmd):
        system("{python} {dir}/manage.py {command}".\
            format(python=executable, dir=path[0], command=_cmd)
        )

    if migrate:
        cmd('makemigrations')
        cmd('migrate')
    if collectstatic:
        cmd('collectstatic --noinput'), print('')
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
migrate_database = lambda: _server(start=False, migrate=True, collectstatic=False)
collect_staticfs = lambda: _server(start=False, migrate=False, collectstatic=True)


def run():
    migrate_database()
    return thread.run()


def start():
    _server(start=False, migrate=True, collectstatic=True)
    return thread.start()
