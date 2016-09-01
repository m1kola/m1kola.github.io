from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import defaultfilters
from django.urls import reverse
from django.utils import translation
from django.utils.datetime_safe import datetime
from jinja2.ext import Extension


class ProjectCoreExtension(Extension):
    def __init__(self, environment):
        super(ProjectCoreExtension, self).__init__(environment)

        self.environment.globals.update({
            'static': staticfiles_storage.url,
            'url': reverse,
            'settings': {
                'SITE_TITLE': settings.SITE_TITLE,
                'SOCIAL_MEDIA_URLS': settings.SOCIAL_MEDIA_URLS,
                'FOOTER_COPYRIGHT': settings.FOOTER_COPYRIGHT,
            },
            'now': datetime.now,
        })
        self.environment.filters.update({
            'date': defaultfilters.date,
            'timesince': defaultfilters.timesince_filter,
        })
        self.environment.install_gettext_translations(translation)


# Nicer import names
core = ProjectCoreExtension
