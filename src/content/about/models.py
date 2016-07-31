from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore import fields as wt_fields
from wagtail.wagtailcore.models import Page

from base.models import BaseFields
from content.about.blocks import AboutBlock


class AboutPage(Page, BaseFields):
    body = wt_fields.StreamField(AboutBlock())

    content_panels = Page.content_panels + BaseFields.content_panels + [
        StreamFieldPanel('body'),
    ]
