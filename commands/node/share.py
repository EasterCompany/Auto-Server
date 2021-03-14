'''

React Code Sharing Tool

Share your apps, assets, components and libraries across multiple React clients.
All sharable components will be housed in `clients/shared` directory and any client they
are shared with will be automatically updated with the latest version any time a change
is made to the shared directory version of that file.

For our commands we will require two arugments, the first being a path to a module or file
from within the `clients/shared` directory - and the second being the name of a client
within the `clients` root directory.

Example Usage (template):

    ./o share -"module_path" -"client_name"

        or for a single file

    ./o share -"file_path" -"client_name"

Example Usage (working example):

    ./o share -library/server -donation

        or for a single file

    ./o share -library/server/address.ts -donation

'''

import json
from sys import path
from shutil import copy
from os import mkdir, remove
from tools.library import console
from os.path import exists, isdir
from distutils.dir_util import copy_tree

log_path = path[0] + '/clients/shared/.log'


def get_log():
    if exists(log_path):
        with open(log_path) as log_file:
            log = json.load(log_file)
    else:
        log = {}
    return log


def save_log(log_content):
    with open(log_path, 'w+') as log_file:
        json.dump(log_content, log_file, indent=2)


def add_to_log(shared_path, client_name, share_type):
    log = get_log()

    # Append client to log
    if client_name not in log:
        log[client_name] = {
            "path": 'clients/' + client_name + '/src/shared',
            "file": [],
            "module": []
        }
    if shared_path == '.log': return None

    # Optimize file sharing
    for ms in log[client_name]['module']:
        if shared_path.startswith(ms):
            print('''
    {path} is already shared with {name} via a module.
    '''.format(
        path=console.col(shared_path, 'yellow'),
        name=console.col(client_name, 'yellow')
    )
    ), exit()

    # Write to log file
    if shared_path not in log[client_name][share_type]:
        if exists(path[0] + '/clients/shared/' + shared_path):
            if exists(path[0] + '/clients/' + client_name):
                log[client_name][share_type].append(shared_path)
            else:
                print('''
    '%s' client does not exist
    ''' % console.col(client_name, 'red')
        ), exit()
        else:
            print('''
    %s
    does not exist in the shared directory
    ''' % console.col(shared_path, 'red')
        ), exit()
    else:
        print('''
    {path} is already shared with {name}
    '''.format(
        path=console.col(shared_path, 'yellow'),
        name=console.col(client_name, 'yellow')
    )
    ), exit()

    # Optimize module sharing
    if share_type == 'module':

        removed_files = []
        for fs in log[client_name]['file']:
            if fs.startswith(shared_path):
                log[client_name]['file'].remove(fs)
                removed_files.append(fs)

        removed_modules = []
        for ms in log[client_name]['module']:
            if ms.startswith(shared_path) and not ms == shared_path:
                log[client_name]['module'].remove(ms)
                removed_modules.append(ms)

        if len(removed_files) > 0:
            print('''
    Removed {x} files from {name} because they're
    included within {path}'''.format(
        x=console.col(str(len(removed_files)), 'green'),
        path=console.col(shared_path, 'green'),
        name=console.col(client_name, 'green')
    ))

        if len(removed_modules) > 0:
            print('''
    Removed {x} submodules from {name} because they're
    included within {path}'''.format(
        x=console.col(str(len(removed_modules)), 'green'),
        path=console.col(shared_path, 'green'),
        name=console.col(client_name, 'green')
    ))

    # Save log file
    save_log(log)

    # Return success!
    return print('''
    shared {path} with {name}
    '''.format(
        path=console.col(shared_path, 'green'),
        name=console.col(client_name, 'green')
    )), __update_shared_files__(), exit()


def share_module(module_path, client):
    if module_path.startswith('/'):
        mdirs = module_path.split('/')[1:]
    else:
        mdirs = module_path.split('/')
    share = '/'.join(mdirs)
    if not share.endswith('/'):
        share += '/'
    add_to_log(share, client, 'module')


def share_file(file_path, client):
    if file_path.startswith('/'):
        fdirs = file_path.split('/')[1:-1]
    else:
        fdirs = file_path.split('/')[:-1]
    fname = file_path.split('/')[-1]
    share = '/'.join(fdirs) + '/' + fname
    add_to_log(share, client, 'file')


def target(path_to_target, client):
    if isdir(path[0] + '/clients/shared/' + path_to_target):
        return share_module(path_to_target, client)
    return share_file(path_to_target, client)


def __update_shared_files__():
    if not exists(log_path):
        return None
    logs = get_log()
    spath = path[0] + '/clients/shared/'

    for client in logs:
        cpath = logs[client]['path'] + '/'
        for mod in logs[client]["module"]:
            copy_tree(spath + mod, cpath + mod)
            if exists(cpath + mod + '/.log'):
                remove(cpath + mod + '/.log')

        for fls in logs[client]["file"]:
            dirs = fls.split('/')
            for i in range(len(dirs)):
                npath = cpath + '/'.join(dirs[:i])
                if not exists(npath):
                    mkdir(npath)
            copy(spath + fls, cpath + fls)


def error_message():
    return print('''
    `SHARE` tool requires 2 arguments beggining with `-`

        ./o share -"module_path" -"client_name"

        or

        ./o share -"file_path" -"client_name"
    ''')
