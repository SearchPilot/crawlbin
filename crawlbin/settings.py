"""
Django settings for crawlbin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'REPLACE_ME__REPLACE_ME__REPLACE_ME'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['crawlbin.com']

APPEND_SLASH = False

# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'crawlbin.urls'

WSGI_APPLICATION = 'crawlbin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {}

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%y %b %d, %H:%M:%S',
        },
    },
    'handlers': {
        'log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/crawlbin/crawlbin.log',
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
        },
    },
    'loggers': {
        'crawlbin': {
            'handlers': ['log'],
            'level': 'INFO',
        },
    }
}

KEEN_PROJECT_ID = '561663b359949a4d80bb94e6'
KEEN_WRITE_KEY = 'bb5ff9f8b7e099c7e38b78f3578875b15fa1a096e77916d2e0daabda64ca2153ce63adc597c3e487f7198ba97d8eb3cea73d7ce9d1a80d3cb84f2305735f747347e05bdba7591b40fb1a519ca4fcfd5208d1c0b960221176c1066b13f7ba4a03f6931877db9c56e0386254cb97de97a0'
KEEN_READ_KEY = '7256cbf2ad25c9b038eaeb8f961511cebdba7b1d02666d99a30eec1f81cdb890dc4c682d59a2751b794da16ba5e980cb0a8da3cadbe098c32464b26a573d1b108a61a8d6f4942b98156ed00d1bede6e93f0d0aada3aa96785e4883a6a8058a1c51282660705db1cd3fb9b29b5663b3db'
KEEN_MASTER_KEY = 'FE15E2E8348309604AB09D7C0AEB416F'
