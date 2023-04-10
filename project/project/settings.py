"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-96o-7&r9vinx(u!upupcbq*lo2u+_9b_mxfekeo!(i_ps-o&^^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

# В данный раздел добавьте 3 обязательных приложения allauth
# и одно, которое отвечает за выход через Yandex
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # 1 - пользователей
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',  # 2 - сообщения
    'django.contrib.staticfiles',
    'django.contrib.sites',  # 3 - настройки сайта
    'django.contrib.flatpages',
    'simpleapp',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',

]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR), 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # `allauth` обязательно нужен этот процессор
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR / 'static']

LOGIN_REDIRECT_URL = "/products"
LOGOUT_REDIRECT_URL = "/accounts/login"

# Этого раздела может не быть, добавьте его в указанном виде.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Регистрация по почте, без подтверждения почты
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # 'mandatory'
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}  # форма дополнительной обработки регистрации пользователя
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  # активирует аккаунт сразу после перехода по ссылке
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAY = 1  # количество дней, когда доступна ссылка на подтверждение регистрации
ACCOUNT_USER_DISPLAY = lambda user: f'{user.first_name}'
# Настройки почты
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 'django.core.mail.backends.smtp.EmailBackend'
#  console - отправка писем в консоль Питона, smtp - отправка писем через почтовые сервисы
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "omneziya@yandex.ru"
EMAIL_HOST_PASSWORD = "apwkwachtgcneyoo"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = ''  # "Hi, dude" - префикс добавляется при рассылке писем менеджерам

DEFAULT_FROM_EMAIL = "omneziya@yandex.ru"

SERVER_EMAIL = "omneziya@yandex.ru"
MANAGERS = (
    ('Alexandra', 'ailuhina1981@yandex.ru'),
    ('Ivan', 'omneziya@yandex.ru'),
)

ADMINS = (
    ('Anton', 'ilyukhin1981@internet.ru'),
)
