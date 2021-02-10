from sys import executable
from os import system, name as os

o_script = '''#!/bin/bash
clear
{python} manage.py tools $1 $2 $3 $4 $5
exit
'''.format(python=executable)


def create_o_script():
    f = open('./o', 'w+')
    f.write(o_script)
    f.close()
    if os == 'posix':
        system('chmod +x ./o')
