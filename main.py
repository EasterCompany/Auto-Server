from os import system
from sys import argv, executable


def run(command, argIndex=1):
    if command == 'install':
        f = open('./run.bat', 'w+')
        f.write('{python} main.py run'.format(python=executable))
        f.close()
        system('chmod +x run.bat')


def read_arguments():
    for index, arg in enumerate(argv):
        if index > 0:
            run(arg, index)


def main():
    read_arguments()


if __name__ == '__main__':
    main()
