from __future__ import absolute_import  # Python 2 only
import datetime

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template import defaultfilters
from django.utils import translation

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'settings': {
            'SITE_TITLE': settings.SITE_TITLE,
            'SOCIAL_MEDIA_URLS': settings.SOCIAL_MEDIA_URLS,
            'FOOTER_COPYRIGHT': settings.FOOTER_COPYRIGHT,
            'CV_MODE': settings.CV_MODE,
        },
        'now': datetime.datetime.now,
    })
    env.filters.update({
        'date': defaultfilters.date,
        'timesince': defaultfilters.timesince_filter,
    })
    env.install_gettext_translations(translation)

    return env
