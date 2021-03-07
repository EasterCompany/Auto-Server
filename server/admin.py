# Standard Library Imports
import json
from sys import path
from os import system
from datetime import datetime
# Local Module Imports
from tools.commands import git

# Load requests logs file for logging
requests_file = open(path[0] + '/.logs/requests.json')
requests_logs = json.loads(requests_file.read())
requests_file.close()
# Load secrets for verification purposes
secrets_file = open(path[0] + '/.config/secret.json')
secrets_data = json.loads(secrets_file.read())
secrets_file.close()
# Universal status responses
OK_status = 'OK'
BAD_status = 'BAD'


def update_logs(new_log):
    global requests_file, requests_logs
    # Add timestamps to each log
    log_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
    log_iter = 0
    # If multiple requests recieved at the same time id each request
    while log_time in requests_logs:
        log_time += 'x' + str(log_iter)
        log_iter += 1
    # Append log to existing logs
    requests_logs[log_time] = new_log
    # Dump new logs to disk
    file_path = path[0] + '/.logs/requests.json'
    with open(file_path, 'w') as json_file:
        json.dump(
            requests_logs,
            json_file,
            indent=2
        )


def verify_request(req, secret):
    if secret == secrets_data['SECRET_KEY']:
        return True
    update_logs(
        {
            'req': req,
            'status': BAD_status,
            'verified': False
        }
    )
    return False


def upgrade_request(secret):
    req = 'upgrade'
    print('\nAn `UPGRADE REQUEST` was run.', '\nverifying request...')
    if not verify_request(req, secret):
        print('    failed.\n')
        return BAD_status
    print('    succeeded.\n')
    git.update.all()
    update_logs(
        {
            'req': req,
            'status': OK_status,
            'verified': True
        }
    )
    return OK_status
