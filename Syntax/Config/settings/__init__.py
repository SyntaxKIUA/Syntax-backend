from dotenv import load_dotenv
import os

load_dotenv()

env = os.getenv('DJANGO_ENV', 'development')

if env == 'production':
    from .production import *
elif env == 'development':
    from .development import *

