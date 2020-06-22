import os.path
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, '..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = "thisIsTotallyASecretJkLolHaHa!1!!1!"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_jsonate',
        'USER': 'postgres'
    }
}

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
            'debug': True,
        },
    }
]

SECRET_KEY = "dna_kzxq8(QbM=-#ZyyA&k,Fi1LU>&bQ4ZA+|(e<g-.%L0JnaK"

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

MIDDLEWARE = MIDDLEWARE_CLASSES

ROOT_URLCONF = 'test_project.urls'

SITE_ID = 1

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    
    'jsonate',
    'test_app',
)
