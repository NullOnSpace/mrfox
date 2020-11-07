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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': "INFO",
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/mrfox.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': "INFO",
            'propagate': True,
        },
    },
}
