# Standard Lib
from sys import argv, path
# Local Commands
from .commands import install, update, branch, merge, commit, push

tools_path = '/'.join(__file__.split('/')[:-1])
project_path = path[0]
command_line = argv[2:]
len_cmd_line = len(command_line)


def help():
    readme = open(tools_path + '/README.md')
    print(readme.read())
    readme.close()


def run_tool(command, index=0):
    arguments_remaining = 0

    for arg in command_line[index + 1:]:
        if arg.startswith('-'):
            arguments_remaining += 1
        else:
            break

    def do_with_message(module):
        if len_cmd_line > index + 1:
            if arguments_remaining < 2:
                return module.error_message(), exit()
            else:
                repo = ''.join(
                    command_line[index + 1].split('-')[1:]
                )
                message = ''.join(
                    ' '.join(command_line[index + 2:]).split('-')[1:]
                )

                if repo == 'server':
                    repo = None

                if repo == 'all':
                    print('\nTools --------------------------------')
                    module.with_message(message, 'tools')
                    print('\nClients ------------------------------')
                    module.with_message(message, 'clients')
                    print('\nServer -------------------------------')
                    module.with_message(message, None)
                    print('')
                    return exit()

                return module.with_message(message, repo), exit()
        else:
            return module.error_message(), exit()

    if command.startswith('-'):
        return None

    if command == 'install':
        install.create_o_script()
        update.git_pull_all()

        def set_branch_origins(repo=None):
            update.git_branch_origins('dev', repo)
            update.git_branch_origins('main', repo)

        set_branch_origins()
        set_branch_origins('clients')
        set_branch_origins('tools')

    elif command == 'update':
        update.git_pull_all()

    elif command == 'dev' or command == 'development':
        branch.switch('dev')

    elif command == 'main' or command == 'production':
        branch.switch('main')

    elif command == 'merge':
        do_with_message(merge)

    elif command == 'commit':
        do_with_message(commit)

    elif command == 'push':
        push.all()

    else:
        help()

    return exit()


def run():
    if len(argv) <= 2:
        help()
    else:
        [run_tool(arg, index) for index, arg in enumerate(command_line)]
