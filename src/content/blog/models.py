# -*- coding: utf-8 -*-
from modelcluster.contrib import taggit
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.utils.pagination import paginate
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

    content_panels = Page.content_panels + BaseFields.content_panels + [
        edit_handlers.FieldPanel('lead', classname='full'),
        edit_handlers.FieldPanel('body', classname='full'),
    ]

    promote_panels = Page.promote_panels + [
        edit_handlers.FieldPanel('tags'),
    ]

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []


class BlogIndexPage(Page, BaseFields):

    @property
    def blog_pages(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.live().descendant_of(self)

        # Order by most recent date first
        blogs = blogs.order_by('-first_published_at')

        return blogs

    def get_context(self, request, *args, **kwargs):
        blog_pages = self.blog_pages

        tag = request.GET.get('tag')
        if tag:
            blog_pages = blog_pages.filter(tags__name=tag)

        paginator, page = paginate(request, blog_pages)

        context = super(BlogIndexPage, self).get_context(request)
        context['posts'] = page
        return context

    content_panels = Page.content_panels + BaseFields.content_panels

    parent_page_types = ['wagtailcore.Page']
