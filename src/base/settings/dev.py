from .base import *  # NOQA


INSTALLED_APPS += [
    'debug_toolbar',
    'wagtail.contrib.wagtailstyleguide',
]


try:
    from .local import *  # noqa
except ImportError:
    pass
