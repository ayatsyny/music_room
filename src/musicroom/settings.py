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

AUTH_USER_MODEL = 'userauth.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.userauth',
    'social_django',
    'apps.songs',
    'apps.playlists',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'  # todo change

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.deezer.DeezerOAuth2',
)

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
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

SOCIAL_AUTH_POSTGRES_JSONFIELD = ls.get('SOCIAL_AUTH_POSTGRES_JSONFIELD', False)

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
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


# SOCIAL_AUTH_URL_NAMESPACE = 'social_auth'
# SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

# SOCIAL_AUTH_FACEBOOK_KEY = ls.get('SOCIAL_AUTH_FACEBOOK_KEY', '')
# SOCIAL_AUTH_FACEBOOK_SECRET = ls.get('SOCIAL_AUTH_FACEBOOK_SECRET', '')
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
#     'locale': 'en_US',
#     'fields': 'id, email, first_name, last_name, gender, link',
# }

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ls.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ls.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', '')

SOCIAL_AUTH_DEEZER_KEY = ls.get('SOCIAL_AUTH_DEEZER_KEY', '')
SOCIAL_AUTH_DEEZER_SECRET = ls.get('SOCIAL_AUTH_DEEZER_SECRET', '')


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.debug.debug',
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'apps.userauth.social_auth_pipelines.check_social_data',
    'social_core.pipeline.social_auth.social_user',
    'apps.userauth.social_auth_pipelines.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    # 'social_core.pipeline.user.user_details',
    'apps.userauth.social_auth_pipelines.set_user_first_reg_social_info',
    'apps.userauth.social_auth_pipelines.set_user_social_info',
    'social_core.pipeline.debug.debug',
)

# REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': {
        'rest_framework.authentication.SessionAuthentication',
    },
    'DEFAULT_PERMISSION_CLASSES': {
        'rest_framework.permissions.IsAuthenticateOrReadOnly',
    }
}
