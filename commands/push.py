from os import system


def all():
    return system('git push --recurse-submodules')
