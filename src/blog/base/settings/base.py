import os
from datetime import datetime


# Get CFG_* vars from the environment
cfg_env = {}
for key, value in os.environ.items():
    if key.startswith('CFG_'):
        cfg_env[key[4:]] = value


gettext_noop = lambda s: s


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
)


# Admins

if 'ADMINS' in cfg_env:
    ADMINS = cfg_env['ADMINS'].split(',')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


if 'SECRET_KEY' in cfg_env:
    SECRET_KEY = cfg_env['SECRET_KEY']

if 'ALLOWED_HOSTS' in cfg_env:
    ALLOWED_HOSTS = cfg_env['ALLOWED_HOSTS'].split(',')


# Application definition

INSTALLED_APPS = [
    'blog.base',
    'blog.content.home',
    'blog.content.about',
    'blog.content.blog',

    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.contrib.wagtailsitemaps',

    'taggit',
    'modelcluster',

    'django.contrib.admin',  # Used only for urlify.js in wagtail :(
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'blog.base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'extensions': [
                'jinja2.ext.i18n',
                'wagtail.wagtailcore.jinja2tags.core',
                'wagtail.wagtailadmin.jinja2tags.userbar',
                'wagtail.wagtailimages.jinja2tags.images',
                'blog.base.jinja2tags.core',
            ]
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ),
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': cfg_env.get('BLOG_DATABASES_DEFAULT_NAME', 'postgres'),
        'USER': cfg_env.get('BLOG_DATABASES_DEFAULT_USER', 'postgres'),
        'PASSWORD': cfg_env.get('BLOG_DATABASES_DEFAULT_PASSWORD', 'postgres'),
        'HOST': cfg_env.get('BLOG_DATABASES_DEFAULT_HOST', 'postgres'),
        'PORT': cfg_env.get('BLOG_DATABASES_DEFAULT_PORT', '5432'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_COOKIE_NAME = 'blog_lang'
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', gettext_noop('English')),
    ('ru', gettext_noop('Russian')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images) and media files (uploaded content)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_compiled')
]

STATIC_URL = '/static/'
STATIC_ROOT = cfg_env.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = cfg_env.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))


# Wagtail

WAGTAIL_SITE_NAME = 'mikola.by'

WAGTAIL_ENABLE_UPDATE_CHECK = False

TAGGIT_CASE_INSENSITIVE = True


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        }
    },
    'formatters': {
        'default': {
            'verbose': '[%(asctime)s] (%(process)d/%(thread)d) %(name)s %(levelname)s: %(message)s'
        }
    },
    'loggers': {
        'blog': {
            'handlers': ['mail_admins', 'console'],
            'level': 'INFO',
            'propagate': False,
            'formatter': 'verbose',
        },
        'wagtail': {
            'handlers': ['mail_admins', 'console'],
            'level': 'INFO',
            'propagate': False,
            'formatter': 'verbose',
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
            'formatter': 'verbose',
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            'formatter': 'verbose',
        },
    },
}


# Site constants

SITE_TITLE = 'mikola.by'

TWITTER_USERNAME = 'm1kola'

SOCIAL_MEDIA_URLS = {
    'github': 'https://github.com/m1kola',
    'facebook': 'https://www.facebook.com/m1kola',
    'linkedin': 'https://www.linkedin.com/in/m1kola',
    'twitter': 'https://twitter.com/%s' % TWITTER_USERNAME,
}

COPYRIGHT_YEAR = 2015
FOOTER_COPYRIGHT = 'Copyright &copy; %(title)s %(years)s' % {
    'title': SITE_TITLE,
    'years':
        '%s' % COPYRIGHT_YEAR if COPYRIGHT_YEAR == datetime.now().year
        else '%s - %s' % (COPYRIGHT_YEAR, datetime.now().year),
}

ENABLE_FILTERING_BY_TAG = False
