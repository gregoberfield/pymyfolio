from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SOMERANDOMSECRETKEYNEEDSTOBEHINHERE'

DEBUG = False

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

IEX_TOKEN = 'PUT YOUR TOKEN HERE'
