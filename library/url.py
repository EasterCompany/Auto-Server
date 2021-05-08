# Essential
from django.urls import path, re_path


def url(Path, view):
    return {
        'type': 'url',
        'value': path(Path, view)
    }


def app(Path, view, name):
    return {
        'type': 'application',
        'value': re_path(Path, view, name)
    }


class App:

    def __init__(self, name, Path, view):
        self.name = name
        self.Path = Path
        self.view = view
        self.urls = []

    def make_url(self, Path, view):
        return self.urls.append(url(Path, view))

    def render(self):
        self.urls.append(app(self.Path, self.view, self.name))
        return self.urls
