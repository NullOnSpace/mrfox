from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'mysql.cnf'),
        },
        'TEST': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'test_mrfox',
            'USER': 'travis',
            'PASSWORD': '',
        },
    }
}
