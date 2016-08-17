# -*- coding: utf-8 -*-
from modelcluster.contrib import taggit
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin import edit_handlers
from wagtail.wagtailcore import fields as wt_fields
from wagtail.wagtailcore.models import Page

from base.models import BaseFields


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page, BaseFields):
    lead = wt_fields.RichTextField(blank=True)
    body = wt_fields.RichTextField()
    tags = taggit.ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        edit_handlers.FieldPanel('lead', classname='full'),
        edit_handlers.FieldPanel('body', classname='full'),
    ]

    promote_panels = Page.promote_panels + BaseFields.promote_panels + [
        edit_handlers.FieldPanel('tags'),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []
