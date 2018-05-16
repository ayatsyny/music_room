import os
import sys
from unipath import Path


BASE_DIR = Path(__file__).absolute().ancestor(2)  # django project dir (src)
ROOT_DIR = BASE_DIR.parent                        # repository root dir

sys.path.append(ROOT_DIR.child('conf'))
try:
    import local_settings
    ls = local_settings.__dict__
except ImportError:
    raise RuntimeError('Please, provide your local configuration for this project.\n'
                       'You need to create conf/local_settings.py with your local settings.')
finally:
    sys.path.pop()

SECRET_KEY = ls.get('SECRET_KEY', '')

DEBUG = ls.get('DEBUG', False)
INTERNAL_IPS = ls.get('INTERNAL_IPS', ('127.0.0.1',))

ADMINS = ls.get('ADMINS', ())
if not DEBUG and not len(ADMINS):
    raise AssertionError('ADMINS must be non empty')

ALLOWED_HOSTS = ls.get('ALLOWED_HOSTS', ls['_domain'])

SITE_ID = 1

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users',
    'apps.songs',
    'apps.playlists',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'musicroom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'musicroom.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ls.get('DB_NAME', ''),
        'USER': ls.get('DB_USER', ''),
        'PASSWORD': ls.get('DB_PASS', ''),
        'HOST': ls.get('DB_HOST', 'localhost'),
        'PORT': ls.get('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

TIME_ZONE = ls.get('TIME_ZONE', 'Europe/Kiev')
LANGUAGE_CODE = ls.get('LANGUAGE_CODE', 'en-us')

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'static')),
    # BASE_DIR.child('static'),
)
