from sys import path
from .commands.install import \
    make_clients_config, __init_conifg_directory__, __init_logs_directory__

__version__ = 0.4
__init_conifg_directory__()
__init_logs_directory__()
make_clients_config(path[0])
