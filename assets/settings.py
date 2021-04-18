# Standard Library Imports
import os
from json import loads

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SERVER_FILE = open(BASE_DIR + '/.config/server.json')
SERVER_DATA = loads(SERVER_FILE.read())
SERVER_FILE.close()

CLIENT_FILE = open(BASE_DIR + '/.config/clients.json')
CLIENT_DATA = loads(CLIENT_FILE.read())
CLIENT_FILE.close()

DEBUG = SERVER_DATA['DEBUG']
LANGUAGE_CODE = SERVER_DATA['LANGUAGE_CODE']
TIME_ZONE = SERVER_DATA['TIME_ZONE']
USE_I18N = True
USE_L10N = True
USE_TZ = True

try:
    SECRET_KEY_FILE = open(BASE_DIR + '/.config/secret.json')
    SECRET_KEY = loads(SECRET_KEY_FILE.read())['SECRET_KEY']
    SECRET_KEY_FILE.close()
except:
    SECRET_KEY = 'no secret key'

ALLOWED_HOSTS = SERVER_DATA['ALLOWED_HOSTS']
INSTALLED_APPS = SERVER_DATA['INSTALLED_APPS']
MIDDLEWARE = SERVER_DATA['MIDDLEWARE']
ROOT_URLCONF = SERVER_DATA['ROOT_URLCONF']
WSGI_APPLICATION = SERVER_DATA['WSGI_APPLICATION']
TEMPLATES = [
    {
        'BACKEND': SERVER_DATA['BACKEND_TEMPLATE'],
        'DIRS': [
            os.path.join(BASE_DIR, 'clients')
        ],
        'APP_DIRS': SERVER_DATA['APP_DIRS_TEMPLATE'],
        'OPTIONS': SERVER_DATA['OPTIONS_TEMPLATE']
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STATIC_URL = SERVER_DATA['STATIC_URL']
STATIC_ROOT = SERVER_DATA['STATIC_ROOT']
STATICFILES_DIRS = [
    CLIENT_DATA[client]['path'] + '/build/static' for client in CLIENT_DATA
]

CORS_ORIGIN_ALLOW_ALL = SERVER_DATA['CORS_ORIGIN_ALLOW_ALL']
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://localhost:8100',
    'http://localhost:8105',
    'http://localhost:45678' # REACT SNAP
)
