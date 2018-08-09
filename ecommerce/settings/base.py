"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#=nz!4!@m(@6frolhw+b8*8y6mvnndg^^%z=nz3lz*yem-t&xu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# EMAIL_HOST = 'smtp.sendgrid.net' # for other Mail
# EMAIL_HOST_USER = 'yourusername@youremail.com' # for other mail
EMAIL_HOST = 'smtp.gmail.com'  # For GMail Only
EMAIL_HOST_USER = 'sajaluser381@gmail.com'
EMAIL_HOST_PASSWORD = 'P@ssword12345'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'eCommerce <sajaluser381@gmail.com>'
BASE_URL = '127.0.0.1:8000'

MANAGERS = (
    ('MD. SAJAL MIA', 'sajaluser381@gmail.com')
)
ADMINS = MANAGERS

# Application definition

INSTALLED_APPS = [
    'pages.apps.PagesConfig',
    'account.apps.AccountConfig',
    'product.apps.ProductConfig',
    'category.apps.CategoryConfig',
    'search.apps.SearchConfig',
    'tags.apps.TagsConfig',
    'cart.apps.CartConfig',
    'order.apps.OrderConfig',
    'billing.apps.BillingConfig',
    'address.apps.AddressConfig',
    'analytic.apps.AnalyticConfig',

    'marketing.apps.MarketingConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

AUTH_USER_MODEL = 'account.CustomUser' # change the Build in models to custom User Model
LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout/'

# For Analytic Apps
FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

MAILCHIMP_API_KEY = "09a0da2d6f1660106306a33c59b619c9-us18"
MAILCHIMP_DATA_CENTER = "us18"
MAILCHIMP_EMAIL_LIST_ID = "abaee9c51c"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

LOGOUT_REDIRECT_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# let's encrypt SSL/TLS
CORS_REPLACE_HTTPS_REFERER = False
HOST_SCHEME = "http://"
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = False


AWS_USERNAME = "ecommerce_user"
AWS_GROUP_NAME = "ecommerce_group"
AWS_ACCESS_KEY_ID = "AKIAJZPBHD5L5XXTQWRQ"
AWS_SECRET_ACCESS_KEY = "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"