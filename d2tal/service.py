from pathlib import Path

DEBUG = True

ALLOWED_HOSTS = []

STATIC_ROOT = None

STATIC_URL = 'static/'

STATICFILES_DIRS = [ Path(__file__).resolve().parent.parent / 'static' ]
