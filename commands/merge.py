from os import system, chdir
from sys import path


def repo(wd=None):
    if wd is not None:
        chdir(path[0] + '/' + wd)

    system("git checkout main")
    system("git pull origin main")
    system("git merge dev")
    system("git push origin master")

    return chdir(path[0])


def error_message():
    return print("""
    `MERGE` tool requires an argument beggining with `-`

        ./o merge -all
        ./o merge -server
        ./o merge -clients
        ./o merge -tools
    """
    )
