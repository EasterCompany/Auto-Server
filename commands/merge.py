from os import system, chdir
from sys import path


def repo(wd=None):
    if wd is not None:
        chdir(path[0] + '/' + wd)

    system("git checkout main")
    system("git pull origin main")
    system("git merge dev")
    system("git push origin main")
    system("git checkout dev")

    return chdir(path[0])


def with_message(message, repo=None):
    if repo is not None:
        chdir(path[0] + '/' + repo)

    system("git checkout main")
    system("git pull origin main")
    system('''git merge dev -m "{message}"'''.format(message=message))
    system("git push origin main")
    system("git checkout dev")

    return chdir(path[0])


def error_message():
    return print("""
    `MERGE` tool requires two arguments beggining with `-`

        ./o merge -all -"merge message"
        ./o merge -server -"merge message"
        ./o merge -clients -"merge message"
        ./o merge -tools -"merge message"
    """
    )
