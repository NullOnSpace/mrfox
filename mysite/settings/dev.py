from .base import *

DEBUG = True

ALLOWED_HOSTS = ["testserver", "127.0.0.1", "localhost"]
INTERNAL_IPS = ["*", "testserver", "127.0.0.1", "localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'mysql.cnf'),
        },
        'TEST': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'test_mrfox',
            'USER': 'root',
            'PASSWORD': '',
        },
    }
}
