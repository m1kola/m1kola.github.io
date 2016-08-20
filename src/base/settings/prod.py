from .base import *  # NOQA


# Just to make sure
DEBUG = False


try:
    from .local import *  # noqa
except ImportError:
    pass
