"""
Django settings for controle_hc project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_on_heroku
from django.core.mail import send_mail
from datetime import datetime, timedelta, timezone, tzinfo
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1lg5dt77uj^=h-l0133s#5v0t1vm!ai=&g@!n8_t8hm3c(^0uz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "34.230.46.128", "ec2-34-230-46-128.compute-1.amazonaws.com"]

SITE_ID = 1

GOOGLE_API_KEY = 'AIzaSyCJBnRLzxMdMI4mF3hAtg_yxC1jCiixtuU'
# Application definition
# Application definition

INSTALLED_APPS = [

    'rest_framework',
    #should be immediately above 'django.contrib.admin'
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bulma',
    'django_select2',
    'django_tables2',
    'django_tables2_column_shifter',
    #'etc',
    'agendaFinanceira',
    'usuarios',
    'prestadores',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    #'registration',
    'allauth.account',
    'rest_auth.registration',
    'djangobower',
    'widget_tweaks',
    'todolist.apps.TodolistConfig',
    'bootstrap4',
    'dal',
    'dal_select2',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = ("bulma",)
CRISPY_TEMPLATE_PACK = "bulma"
REGISTRATION_AUTO_LOGIN = False # Automatically log the user in.
ACCOUNT_ACTIVATION_DAYS = 30 # One-week activation window; you may, of course, use a different value.

REGISTRATION_FORM = 'usuarios.forms.MyRegForm'
AUTH_USER_MODEL = 'usuarios.User'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

AUTH_USER_MODEL = "usuarios.User"
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ.get('DB_NAME', 'planoreal_db'),
#         'USER': os.environ.get('DB_USER', 'postgres'),
#         'PASSWORD': os.environ.get('DB_PASS', 'pgadmin'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


REST_FRAMEWORK = {
    'DATE_FORMAT': "%d/%m/%Y",
    'DATE_INPUT_FORMATS': ["%d-%m-%Y"],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
    
]

STATICFILES_FINDERS: [
        'djangobower.finders.BowerFinder',
]

BOWER_COMPONENTS_ROOT = '/schedule/static/'

BOWER_INSTALLED_APPS = (
    'jquery',
    'jquery-ui',
    'bootstrap'
)


from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.DEBUG:'debug',
    message_constants.INFO:'info',
    message_constants.SUCCESS:'success',
    message_constants.WARNING:'warning',
    message_constants.ERROR:'danger',
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/


LANGUAGE_CODE = 'pt-br'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:m'
DATE_INPUT_FORMATS=['%d/%m/%Y']



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = "/media/"

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'seumkt@gmail.com'
EMAIL_HOST_PASSWORD = 'lhksxmysnfptxknf'


#PAYPAL_TEST = True
#PAYPAL_EMAIL = ''


IMPORT_EXPORT_USE_TRANSACTIONS = True

django_on_heroku.settings(locals())


