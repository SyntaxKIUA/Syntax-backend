# from .base import *
#
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
# INTERNAL_IPS = ['127.0.0.1']

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
