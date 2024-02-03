from django.urls import reverse, reverse_lazy
from environs import Env

env = Env()
env.read_env()

from os import environ
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8e)*boeb4v6_$h7v79qv)x+s9j3$ujm$js$92i-e2o388%6ld)'
DEBUG = False

ALLOWED_HOSTS = ['al-xorazmiy.online', 'www.al-xorazmiy.online', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = [
    'https://al-xorazmiy.online',
    'https://al-xorazmiy.online',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'whitenoise',
    'rest_framework',
    'django.contrib.humanize',
    'cloudinary_storage',

    'app_users.apps.AppUsersConfig',
    'app_main.apps.AppMainConfig',
    # 'api.apps.ApiConfig'

    # 'debug_toolbar',
]

# This is for Django debug tools
INTERNAL_IPS = [
    # add your IP address here
    '127.0.0.1',
    # add more IPs if necessary
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'PROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'PROJECT.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': env.str('DB_NAME'),
         'HOST': env.str('DB_HOST'),
         'PORT': env.str('DB_PORT'),
         'USER': env.str('DB_USER'),
         'PASSWORD': env.str('DB_PASSWORD'),
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

LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = 'al-xorazmiy-media/'

# STATICFILES_DIRS = [
#     BASE_DIR / 'static'
# ]

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'app_users.User'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env.str('CLOUD_NAME'),
    'API_KEY': env.str('API_KEY'),
    'API_SECRET': env.str('API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

LOGIN_URL = reverse_lazy("signin")
LOGOUT_REDIRECT_URL = reverse_lazy("signin")
