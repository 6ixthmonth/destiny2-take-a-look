from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-=_+'
# SECRET_KEY = 'django-insecure-50-CHARACTERS-FOR-SECRET-KEY'

DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['SERVER_IP', 'DOMAIN']

STATIC_ROOT = None
# STATIC_ROOT = BASE_DIR / 'static/'

STATIC_URL = 'static/'
# STATIC_URL = 'static/'

STATICFILES_DIRS = [ BASE_DIR / 'static/' ]
# STATICFILES_DIRS = []
