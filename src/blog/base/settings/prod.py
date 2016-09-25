from .base import *  # NOQA


# Just to make sure
DEBUG = False

GOOGLE_TAG_MANAGER_ID = 'GTM-PVR4H5'

FACEBOOK_APP_ID = '1744263672501697'


try:
    from .local import *  # noqa
except ImportError:
    pass
