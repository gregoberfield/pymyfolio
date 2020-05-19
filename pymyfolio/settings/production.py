from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k363!v!fcv&)&s1dq0l64tl(5x0c1$+#(rcklfghwa8mpm6b^u'

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
