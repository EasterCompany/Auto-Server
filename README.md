
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

# Update

Update all your git repositories recursively including submodules and packages with a
single command.

```bash
./o update
```

# Change Branches

You can switch between the `main` (production) branch and the `dev` (development) branch
for all your repositories and submodules with a single command.

## Enter Production Branches

```bash
./o main
```

## Enter Development Branches

```bash
./o dev
```

# Help

If you are viewing this from within your terminal we reccomend going
[here](https://github.com/EasterCompany/Overlord-Tools) and viewing this with formating.
