from sys import path
from os.path import exists
from .commands.install import \
    make_clients_config, __init_conifg_directory__, __init_logs_directory__,\
    make_server_config
from .commands.node.share import \
    __update_shared_files__

__vminmax__ = ['1', '0', '0']
__version__ = str('.'.join(__vminmax__))
__init_conifg_directory__()
__init_logs_directory__()
__update_shared_files__()

make_clients_config(path[0])

if not exists (path[0] + '/.config/server.json'):
    make_server_config(path[0])
