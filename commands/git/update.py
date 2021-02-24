from sys import path
from os import system, chdir


def branch_origins(branch, repo=None):
    if repo is not None:
        chdir(path[0] + '/' + 'tools')
    system('git branch --set-upstream-to=origin/{branch} {branch}'.format(
        branch=branch
    ))
    return chdir(path[0])


def all():
    system('git pull --recurse-submodules')
