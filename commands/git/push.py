from os import system


def all():
    print('\n\nSubmodules :------------------\n')
    system('''git submodule foreach --recursive "git push && echo ''"''')
    print('\n\nParent :----------------------\n')
    system('git push')
    print('')
