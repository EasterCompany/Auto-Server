
# Overlord Tools

This an open source tool package by Easter Company for automating the development, testing
& deployment processes for our tech stack hosted on PythonAnywhere. Some features may be
specific to our hosting solution but most will be useful to all developers regardless of
your host method.

# Install

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

# Update

Pull latest updates from all your git repositories recursively including submodules and
packages with a single command.

```bash
./o update
```

# Change Branches

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

# Commit Changes

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

# Pushing

When you are ready to push all your changes to the parent repository & submodules
you can use the following command:

```bash
./o push
```

If required you will need to enter a username & password for each repository that has been
pushed.

# Merging

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

# New Django Secret Key

To generate a new django secret key file for your application, use the following command:

```bash
./o new_secret_key
```

and a new secret file will be generated in your application's root directory named
`.secret` and can be loaded by your app at the following relative path `./.secret`

# Help

If you are viewing this from within your terminal we reccomend going
[here](https://github.com/EasterCompany/Overlord-Tools) and viewing this with formating.
