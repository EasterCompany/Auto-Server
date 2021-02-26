from os import system, chdir
from sys import path


def with_message(message, module=None):
    if module is not None:
        module_name = module
    else:
        module_name = 'Server'

    print(module_name + "------------------")

    if module is not None:
        chdir(path[0] + '/' + module)

    system('git add .')
    system('''git commit -m "{message}"'''.format(
        message=message
    ))

    return chdir(path[0])


def error_message():
    return print("""
    `COMMIT` tool requires 2 arguments beggining with `-`

        ./o commit -server  -message
        ./o commit -clients -message
        ./o commit -tools   -message
    """
    )
