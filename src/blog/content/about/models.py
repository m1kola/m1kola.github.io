from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore import fields as wt_fields
from wagtail.wagtailcore.models import Page

from blog.base.models import BaseFields
from blog.content.about.blocks import AboutBlock


class AboutPage(Page, BaseFields):
    body = wt_fields.StreamField(AboutBlock())

    parent_page_types = ['home.HomePage']
    subpage_types = []

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + BaseFields.promote_panels

    @classmethod
    def can_create_at(cls, parent):
        return super().can_create_at(parent) and not cls.objects.count()
