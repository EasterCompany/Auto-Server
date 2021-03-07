from os import system, chdir
from sys import path


def with_message(message, module_name):
    module = module_name
    if module == 'server':
        module = None

    print('\n', module_name, ":------------------\n")
    if module is not None:
        chdir(path[0] + '/' + module)

    system('git add .')
    system('''git commit -m "{message}"'''.format(
        message=message
    ))
    return print(''), chdir(path[0])


def all(message):
    print('\nSubmodules :------------------\n')
    system('''
        git submodule foreach --recursive "git commit -am '{message}'"
        '''.format(message=message).replace('\n', ' ')
    )
    print('')
    print('\nParent :----------------------\n')
    system('''git add . && git commit -m "{message}"'''.\
        format(message=message)
    )
    return print('')


def error_message():
    return print("""
    `COMMIT` tool requires 2 arguments beggining with `-`

        ./o commit -server  -message
        ./o commit -clients -message
        ./o commit -tools   -message
    """
    )
