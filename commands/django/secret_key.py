from django.core.management.utils import get_random_secret_key


def new():
    print('Creating new secret key...')
    new_key = get_random_secret_key()
    new_file = open('./.secret', 'w+')
    new_file.write(new_key)
    new_file.close()
    print('Success!')
    return new_key
