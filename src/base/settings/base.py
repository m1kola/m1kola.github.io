import os
from datetime import datetime


# Get CFG_* vars from the environment
cfg_env = {}
for key, value in os.environ.items():
    if key.startswith('CFG_'):
        cfg_env[key[4:]] = value


gettext_noop = lambda s: s


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


if 'SECRET_KEY' in cfg_env:
    SECRET_KEY = cfg_env['SECRET_KEY']

if 'ALLOWED_HOSTS' in cfg_env:
    ALLOWED_HOSTS = cfg_env['ALLOWED_HOSTS'].split(',')


# Application definition

INSTALLED_APPS = [
    'base',
    'content.home',
    'content.about',
    'content.blog',

    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

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

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'base.jinja2_env.environment',
            'extensions': [
                'jinja2.ext.i18n',
                'wagtail.wagtailcore.jinja2tags.core',
                'wagtail.wagtailadmin.jinja2tags.userbar',
                'wagtail.wagtailimages.jinja2tags.images',
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
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ),
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'


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
LANGUAGE_CODE = 'ru'
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

STATIC_URL = '/static/'
STATIC_ROOT = cfg_env.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = cfg_env.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))


# Wagtail

WAGTAIL_SITE_NAME = 'mikola.by'
TAGGIT_CASE_INSENSITIVE = True


# Site constants

SITE_TITLE = 'mikola.by'

SOCIAL_MEDIA_URLS = {
    'github': 'https://github.com/m1kola',
    'facebook': 'https://www.facebook.com/m1kola',
    'linkedin': 'https://www.linkedin.com/in/m1kola'
}

COPYRIGHT_YEAR = 2015
FOOTER_COPYRIGHT = 'Copyright &copy; %(title)s %(years)s' % {
    'title': SITE_TITLE,
    'years':
        '%s' % COPYRIGHT_YEAR if COPYRIGHT_YEAR == datetime.now().year
        else '%s - %s' % (COPYRIGHT_YEAR, datetime.now().year),
}

INDEX_ROUTE_NAME = 'wagtail_serve'
