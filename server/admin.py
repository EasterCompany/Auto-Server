from sys import path
from os import system
from json import loads

requests_file = open(path[0] + '/.logs/requests.json')
requests_logs = loads(requests_file.read())
requests_file.close()


def update_request():
    return
