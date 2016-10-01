import jinja2.ext
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import defaultfilters
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from django.utils.datetime_safe import datetime
from django.utils.safestring import mark_safe
from wagtail.wagtailcore.models import Page


class ProjectCoreExtension(jinja2.ext.Extension):
    def __init__(self, environment):
        super(ProjectCoreExtension, self).__init__(environment)

        self.environment.globals.update({
            'static': staticfiles_storage.url,
            'url': reverse,
            'now': datetime.now,
            'primary_nav': primary_nav,
            'google_tag_manager': google_tag_manager,
            'get_meta_title': get_meta_title,
            'get_meta_description': get_meta_description,
            'get_meta_image': get_meta_image,
            'get_image_display': get_image_display,
            'settings': {
                'SITE_TITLE': settings.SITE_TITLE,
                'SOCIAL_MEDIA_URLS': settings.SOCIAL_MEDIA_URLS,
                'FOOTER_COPYRIGHT': settings.FOOTER_COPYRIGHT,
                'ENABLE_FILTERING_BY_TAG': getattr(settings, 'ENABLE_FILTERING_BY_TAG', True),
                'FACEBOOK_APP_ID': getattr(settings, 'FACEBOOK_APP_ID', None),
            },
        })
        self.environment.filters.update({
            'date': defaultfilters.date,
            'timesince': defaultfilters.timesince_filter,
        })
        self.environment.install_gettext_translations(translation)


@jinja2.contextfunction
def primary_nav(context):
    homepage = Page.objects.get(slug='home')
    menu_items = homepage.get_children().live().filter(show_in_menus=True)

    return mark_safe(render_to_string('base/tags/primary_nav.html', {
        'menu_items': menu_items,
        'request': context['request'],
    }))


@jinja2.contextfunction
def google_tag_manager(context):
    if settings.DEBUG:
        return mark_safe('')

    request = context.get('request')
    if request and request.is_preview:
        return mark_safe('')

    google_tag_manager_id = getattr(settings, 'GOOGLE_TAG_MANAGER_ID', None)

    return mark_safe(render_to_string('base/tags/google_tag_manager.html', {
        'google_tag_manager_id': google_tag_manager_id,
    }))


@jinja2.contextfunction
def get_meta_title(context):
    title = settings.SITE_TITLE

    page = context.get('page')
    if page:
        title = page.title
        if page.seo_title:
            title = page.seo_title

    return title


@jinja2.contextfunction
def get_meta_description(context):
    description = ''

    page = context.get('page')
    if page:
        if getattr(page, 'subtitle'):
            description = page.subtitle

    return description


@jinja2.contextfunction
def get_meta_image(context):
    image = staticfiles_storage.url('base/images/default_bg.jpg')

    page = context.get('page')
    if page and page.share_image:
        image = page.share_image.get_rendition('width-1024').url

    request = context.get('request')
    if request:
        image = request.build_absolute_uri(image)

    return image


@jinja2.contextfunction
def get_image_display(context, page=None):
    image = staticfiles_storage.url('base/images/default_bg.jpg')

    page = page or context.get('page')
    if page and page.main_image:
        image = page.main_image.get_rendition('width-1024').url

    request = context.get('request')
    if request:
        image = request.build_absolute_uri(image)

    return image

# Nicer import name
core = ProjectCoreExtension
