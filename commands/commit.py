from os import system, chdir
from sys import path


def with_message(message, module=None):
    if module is not None:
        chdir(path[0] + '/' + module)

    system('git add .')
    system('''git commit -m "{message}"'''.format(
        message=message
    ))

    return chdir(path[0])
