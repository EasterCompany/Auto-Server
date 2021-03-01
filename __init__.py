from sys import path
from .commands.install import clients_json

__version__ = 0.3
clients_json(path[0])
