# -*- coding: utf-8 -*-

from django.conf import settings as global_settings


_DEFAULT_SETTINGS = {
    'POST_SLUG_REGEX': r'[a-z0-9-]+',
    'TAG_SLUG_REGEX': r'[a-z-]+',
    'POSTS_PAGE_SIZE': 20,
}


class Settings(object):
    def __init__(self):
        for key, value in _DEFAULT_SETTINGS.iteritems():
            actual_value = getattr(global_settings, 'BLOG_%s' % key, value)
            setattr(self, key, actual_value)

settings = Settings()
