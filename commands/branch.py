from os import system


def switch(branch):
    print(
        '\nEntering {branch_name} Branch\n\nMain :------------------------\n'.\
            format(branch_name=branch.\
                replace('dev', 'Development').\
                replace('main', 'Production')
            )
    )
    system(
        'git checkout {branch} && git pull origin {branch} || true'.format(
            branch=branch
        )
    )
    print('\n\nSubmodules :------------------\n')
    system(
        'git submodule foreach --recursive "git checkout {branch} && git pull origin {branch} && echo "" || true"'.\
        format(
            branch=branch
        )
    )
    print('')
