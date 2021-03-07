
# Overlord Tools

This an open source tool package by Easter Company for automating the development, testing
& deployment processes for our tech stack developed on *Linux* hosted on *PythonAnywhere*,
shared on *Github*  and highly emphasises *Code Reuse & Extensibility* between two of our
servers & applications [eastercompany.eu](https://eastercompany.eu.pythonanywhere.com/) &
[easter.company](https://www.easter.company/)
using a majority of the same code.

some features may be specific to our development & hosting solutions but most will be
useful to all developers regardless of your host method.

## Patch Notes 0.4.1

Listed below is `new features` & `bug fixes` for the next release. <br>
Tasks marked (:heavy_check_mark:) have been completed. <br>
Tasks marked (:x:) have been discarded. <br>
Tasks left unmarked are currently in development or will begin development soon. <br>

### New Features

- Request server task status :heavy_check_mark:
- Request server cpu status :heavy_check_mark:
- Request server console status :heavy_check_mark:
- Request server webapps status :heavy_check_mark:
- Request server to reload :heavy_check_mark:
- Request server to update

### Bug Fixes

- configuration files are now available at `.config` directory :heavy_check_mark:

## Install

Install the `o script` (Overlord Script) file by running `manage.py` on your intended
python executable and use the following command.

```bash
python manage.py tools install
```

A file name `o` will appear in your current working directory. Which should be the same as
where your `manage.py` file is located. The `o script` file will allow you to run tools
easily from your command line with a simple command.

```bash
./o [arg 1] [arg 2] [arg 3] ...etc...
```

This file should be ignored by your .gitignore file because it will hard-code a path to
your selected python installation on your machine which you intend to use for your project.

If you need to update your `o script` file you can always either run the above command
again or use the following command.

```bash
./o install
```

The install command with also set the origins of your development and production branch to
the same origin for each `dev -> dev` and `main -> main` for each of your repositories. If
you need to change the origin - make sure you reset the origin to Overlord-Tools default
setting by running the install command again.

### Installing clients

Using the clients argument you can install all clients within the `clients` directory

```bash
./o install -clients
```

or you can specifically install a single client with the following command

```bash
./o install -clients -"client_name_here"
```

## Update

Pull latest updates from all your git repositories recursively including submodules and
packages with a single command.

```bash
./o update
```

## Change Branches

You can switch between the `main` (production) branch and the `dev` (development) branch
for all your repositories and submodules with a single command.

## Enter Production Branches

Switch all your repositories to production branches.

```bash
./o main
```

## Enter Development Branches

Switch all your repositories to development branches.

```bash
./o dev
```

## Commit Changes

Commit your changes to a repository with a message.

```bash
./o commit -"repo" -"enter a meaningful message."
```

Where `repo` is a repository within your project. For example, `tools`.

here is an example of the above command for each of the possible repositories:

```bash
./o commit -clients -"fixed some bug"
./o commit -tools -"fixed some bug"
./o commit -server -"updated clients & tools"
```

would make a commit to the tools & clients repositories with the above messages and then
commit to the server (parent repository) with the message "updated clients & tools".

You are not required to use qoutes around your messages although if you want to use syntax
from bash commands inside your string you will need to use them. Such as the `&` operator.

## Pushing

When you are ready to push all your changes to the parent repository & submodules
you can use the following command:

```bash
./o push
```

If required you will need to enter a username & password for each repository that has been
pushed.

## Merging

When you are ready to merge all your changes from the Development branch into the
production branch for a repository.

```bash
./o merge -"repo" -"message"
```

where `repo` is the name of the repository according the following examples;

```bash
./o merge -server -"updated clients & tools"
./o merge -clients -"added some feature"
./o merge -tools -"added some feature"
```

or you can use the following command:

```bash
./o merge -all
```

to merge all the changes from the development branch into each production branch.

## New Django Secret Key

To generate a new django secret key file for your application, use the following command:

```bash
./o new_secret_key
```

and a new secret file will be generated in your application's root directory named
`.secret.key` and can be loaded by your app at the following relative path
`./.secret.key`.

## Run Unit Tests

To run all unit tests in your application use the following command:

```bash
./o test
```

## Run React Client (standalone)

To run your react application without the server, use the following command:

```bash
./o runclient -"app name"
```

This will start the React Client on its own at `localhost:3000` by default or which ever
port is specified by the `.env` file in it's root directory. For example; our global
client runs on port `8100` and each client is designated a increment of 1 after that.
So the next client on our demo server `seclea` is given port `8101`.

You can also launch all your applications in one command by doing the following:

```bash
./o runclient -all
```

Be careful when running all clients in parallel as this will cause all clients to run at
once and if using `create-react-app` you're browser will spawn a lot of new tabs for each
client.

## Run Django Server (standalone)

To run your Django server without any clients, use the following command:

```bash
./o runserver
```

This will start the Django Server on its own at `localhost:8000`.

## Run Django Database Migrations

To run your Django migrations (ie; `makemigrations` & `migrate`) just use:

```bash
./o migrate
```

This command does not usually need to be run manually - as it will be automatically run
when the Django server is started. However just incase you need to manually run migrations
this command is here.

## Run Development Server & Client

To run your Django Server and React Client simultaneously, use the following command:

```bash
./o run
```

The Django server will be running on `localhost:8000` while all react clients  will be
running on their designated ports. `localhost:3000` is the default however each client
should have it's own port number assigned to it by the `.env` file in the clients root
directory.

## Run Production Server & Client

To run your production Server and Client(s), use the following command:

```bash
./o start
```

this will run all unit tests - and if they all pass, then the client will be built and
optimized for production. Then the server will be started with the production ready client
on a single connection from the same port which is `localhost:8000` by default.

## Variable Meta Data

Overlord Tools uses variable meta data that is generated on each build of your client.
Variable meta data tags are contained in `{# meta_data #}` these tags.

Here is a list of the all the currently supported variable meta data tags

| Tag                | Content               |
| ------------------ | --------------------- |
| time_of_last_build | %Y-%m-%dT%H:%M:%S     |

## PA Data Tools

You can control the host server by adding the api key to the `.config/secret.json` file.
To talk to the python anywhere hosted server use the following command:

```bash
./o server -"command"
```

below find a list of available commands for the server tool.

### Webapps

To get a detailed list of available webapps and their associated domains.

```bash
./o server -apps
```

### Consoles

To get a detailed list of available consoles

```bash
./o server -consoles
```

### CPU qouta

To get a details on the CPU qouta

```bash
./o server -cpu
```

### Always on Tasks

To get a detailed list of active always on tasks

```bash
./o server -tasks
```

### Reload This

To reload the production server for the current application you're developing.

```bash
./o server -reload
```

In order to run this command you will need to add the domain to your `.config/secret.json`

## PA CI Tools

For PA `Continious Integration` tools to work you will need to add the `tools.server.api`
view file to your `web.urls` or other root urls file for your django project.

### Server Upgrade

The server upgrade command will request the server to upgrade to the latest version of the
app from the github repositories `main` branch.

```bash
./o server -upgrade
```

## Help

To get help you can use the following command:

```bash
./o help
```

<br />
<br />
<h2> Technology </h2>
<table>
   <tr>
      <td valign="middle">
         <a href='https://www.python.org/'>
            <img
               alt='Python'
               src='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png'
               width='64px'
               height='64px'
            />
            <p align='center'> Python </p>
         </a>
      </td>
      <td valign="middle">
         <a href='https://www.gnu.org/software/bash/'>
            <img
               alt='bash'
               src='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/bash/bash.png'
               width='64px'
               height='64px'
            />
            <p align='center'> Bash </p>
         </a>
      </td>
   </tr>
</table>
<br />
<br />

<p align='center'> Easter Company © 2021 </p>
