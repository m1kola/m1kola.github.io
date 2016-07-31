from .base import *  # NOQA


DEBUG = False


try:
    from .local import *  # noqa
except ImportError:
    pass
