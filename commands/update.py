from os import system


def git_pull_all():
    system('git pull --recurse-submodules')
