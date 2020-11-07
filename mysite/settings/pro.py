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
    'formatters': {
        'custom': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': "INFO",
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/mrfox.log',
            'formatter': 'custom',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': "INFO",
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': "INFO",
    },
}
