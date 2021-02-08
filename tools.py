from os import system, name as os
from sys import argv, executable, path

o_script = '''#!/bin/bash
clear
{python} main.py $1 $2 $3 $4 $5
exit
'''.format(python=executable)

cmd_table = {
    'install':
        '''
        Performs various one-time operations:
            - creates the 'o script' file for this system.
            - generates a '.secret' file for this system.
        ''',
}


def help():
    readme = open(path[0] + '/README.md')
    print(readme.read())
    readme.close()


def run(command):
    if command == 'install':
        f = open('./o', 'w+')
        f.write(o_script)
        f.close()
        if os == 'posix':
            system('chmod +x ./o')
    else: help()
    return exit()


if __name__ == '__main__':
    if len(argv) <= 1:
        help()
    else:
        [run(arg) for arg in argv[1:]]
