# Standard Lib
from os.path import exists
from sys import argv, path

# Local Commands
from .commands import install, git, django, node, pytest

tools_path = '/'.join(__file__.split('/')[:-1])
project_path = path[0]
command_line = argv[2:]
len_cmd_line = len(command_line)


def help():
    return print(
        '''
************** HELP *****************

To get help & information on Overlord
Tools go to this github address

https://github.com/EasterCompany/Overlord-Tools/blob/main/README.md

or read your local README.md file

*************************************
        '''
    )


def run_tool(command, index=0):
    arguments_remaining = 0
    arguments = []

    for arg in command_line[index + 1:]:
        if arg.startswith('-'):
            arguments_remaining += 1
            arguments.append('-'.join(arg.split('-')[1:]))
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

    if command.startswith('-'): return None

    elif command == 'install':

        if arguments[0] == 'clients':
            if arguments_remaining == 1:
                return node.clients.install()
            elif arguments_remaining > 1:
                for argument in arguments[1:]:
                    node.clients.install(argument)
                return

        install.create_o_script()
        git.update.all()

        def set_branch_origins(repo=None):
            git.update.branch_origins('dev', repo)
            git.update.branch_origins('main', repo)

        set_branch_origins()
        set_branch_origins('clients')
        set_branch_origins('tools')
        install.make_server_config(project_path)
        install.manage_py(project_path)
        install.settings_py(project_path)
        if not exists(project_path + '/.secret.key'):
            django.secret_key.new()

    elif command == 'update': git.update.all()

    elif command == 'dev' or command == 'development': git.branch.switch('dev')

    elif command == 'main' or command == 'production': git.branch.switch('main')

    elif command == 'merge': do_with_message(git.merge)

    elif command == 'commit': do_with_message(git.commit)

    elif command == 'push': git.push.all()

    elif command == 'new_secret_key': django.secret_key.new()

    elif command == 'test': pytest.run.all_tests()

    elif command == 'runclient' or command == 'run':
        if arguments_remaining < 1 and not command == 'run':
            return node.clients.error_message()
        elif arguments_remaining == 1 and arguments[0] == 'all':
            return node.clients.run_all()
        elif arguments_remaining >= 1:
            for arg in arguments:
                node.clients.run(arg, False, False)
            return

    elif command == 'runserver': django.server.run()

    elif command == 'build':
        if arguments_remaining < 1:
            return node.clients.error_message()
        if arguments_remaining == 1 and arguments[0] == 'all':
            return node.clients.build_all()
        for arg in arguments:
            node.clients.build(arg)

    elif command == 'migrate': django.server.migrate_database()

    elif command == 'run':
        node.clients.run_all(none_on_main_thread=True)
        django.server.run()

    elif command == 'start':
        if pytest.run.all_tests():
            node.clients.build_all()
            django.server.start()
        else:
            exit(99)

    elif command == 'help': help()

    else: print('invalid input \n  >> ./o', ' '.join(command_line))

    return exit()


def run():
    install.clients_json(project_path)
    if len(argv) <= 2: help()
    else: [run_tool(arg, index) for index, arg in enumerate(command_line)]
