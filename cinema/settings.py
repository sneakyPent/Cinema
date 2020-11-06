"""
Django settings for cinema project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z4x@w)0)_58o))$0o7!ae9o0xux9z(-jht590^n)i4+61yqh)^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_filters',
	'django_extensions',
	'corsheaders',
	# 'rest_framework.authtoken',
	'rest_framework',
	'backend'
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cinema.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
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

WSGI_APPLICATION = 'cinema.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'cinema/db.sqlite3'),
	}
}
# CORS_ORIGIN_ALLOW_ALL = True

# CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
# ACCESS_CONTROL_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
	'http://localhost',
)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'cinemaDB',
#         'USER': 'root',
#         'PASSWORD': 'passwd',
#         'HOST': 'db',
#         'PORT': '3306',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATE_INPUT_FORMATS = ['%d/%m/%Y']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
	'DEFAULT_FILTER_BACKENDS': 'django_filters.rest_framework.DjangoFilterBackend',
	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.BasicAuthentication',
	),
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.IsAuthenticated'
		# 'rest_framework.permissions.DjangoModelPermissions'
		# 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	],
}

SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=5),
	'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
	'ROTATE_REFRESH_TOKENS': False,
	'BLACKLIST_AFTER_ROTATION': True,

	'ALGORITHM': 'HS256',
	'SIGNING_KEY': SECRET_KEY,
	'VERIFYING_KEY': None,
	'AUDIENCE': None,
	'ISSUER': None,

	'AUTH_HEADER_TYPES': ('Bearer',),
	'USER_ID_FIELD': 'id',
	'USER_ID_CLAIM': 'user_id',

	'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
	'TOKEN_TYPE_CLAIM': 'token_type',

	'JTI_CLAIM': 'jti',

	'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
	'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
	'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}
