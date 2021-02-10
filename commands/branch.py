from os import system


def switch(branch):
    print('\nEntering Developer Branch\n\nMain:\n\n')
    system(
        'git checkout {branch} || true'.format(
            branch=branch
        )
    )
    print('\n\nSubmodules:\n')
    system(
        'git submodule foreach --recursive "git checkout {branch} || true"'.format(
            branch=branch
        )
    )
    print('')
