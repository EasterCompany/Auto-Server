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

    if command.startswith('-'):
        return None

    if command == 'install':
        install.create_o_script()

    elif command == 'update':
        update.git_pull_all()

    elif command == 'dev' or command == 'development':
        branch.switch('dev')

    elif command == 'main' or command == 'production':
        branch.switch('main')

    elif command == 'merge':
        if len_cmd_line > index + 1:
            argument = command_line[index + 1]
            if argument.startswith('-'):
                argument = ''.join(argument.split('-')[1:])
                if argument == 'server':
                    merge.repo(None)
                elif argument == 'all':
                    merge.repo(None)
                    merge.repo('clients')
                    merge.repo('tools')
                else:
                    merge.repo(argument)
            else:
                merge.error_message(), exit()

    elif command == 'commit':
        if len_cmd_line > index + 1:
            if arguments_remaining == 1:
                module = None
                message = ''.join(
                    ' '.join(command_line[index + 1:]).split('-')[1:]
                )
            elif arguments_remaining >= 2:
                module = ''.join(
                    command_line[index + 1].split('-')[1:]
                )
                message = ''.join(
                    ' '.join(command_line[index + 2:]).split('-')[1:]
                )
            else:
                return commit.error_message(), exit()
            return commit.with_message(message, module), exit()

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
