# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from modelcluster.contrib import taggit
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin import edit_handlers
from wagtail.wagtailcore import fields as wt_fields
from wagtail.wagtailcore.models import Page

from blog.base.blocks import StoryBlock
from blog.base.models import BaseFields


class BlogIndexPage(Page):
    """
    I just want to have "/blog" prefix for blog
    and don't want to have a lot of child pages underneath the homepage.
    """

    # Only allow creating BlogIndexPage at the root level
    parent_page_types = ['home.HomePage']

    # Only allow to create a one page instance
    @classmethod
    def can_create_at(cls, parent):
        return super().can_create_at(parent) and not cls.objects.count()

    def get_sitemap_urls(self):
        """
        Exclude blog index page from a sitemap,
        because this page just redirects to the parent page.
        """
        return []

    def serve(self, request, *args, **kwargs):
        parent = self.get_parent()

        return redirect(parent.url, permanent=True)


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page, BaseFields):
    lead = wt_fields.RichTextField(blank=True)
    body = wt_fields.StreamField(StoryBlock())
    tags = taggit.ClusterTaggableManager(through=BlogPageTag, blank=True)

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    content_panels = Page.content_panels + [
        edit_handlers.FieldPanel('lead', classname='full'),
        edit_handlers.StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + BaseFields.promote_panels + [
        edit_handlers.FieldPanel('tags'),
    ]
