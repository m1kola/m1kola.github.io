from .base import *  # NOQA


DEBUG = True


INSTALLED_APPS += [
    'wagtail.contrib.wagtailstyleguide',
]


try:
    from .local import *  # noqa
except ImportError:
    pass
