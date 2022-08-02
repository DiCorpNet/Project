import os
from pathlib import Path


SECRET_KEY = 'django-insecure-ok4y$a(6gk7*^hwa#xw^h#!2h6p00z#exxj%9)hsqwpa=ad+0&'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.3']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myblog',
        'USER': 'viki',
        'PASSWORD': '110987',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


BASE_DIR = Path(__file__).resolve().parent.parent
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_sdn')