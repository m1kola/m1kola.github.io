from __future__ import absolute_import, unicode_literals

from django.conf import settings
from taggit.models import Tag
from wagtail.utils.pagination import paginate
from wagtail.wagtailcore.models import Page

from blog.base.models import BaseFields
from blog.content.blog.models import BlogPage


class HomePage(Page, BaseFields):
    # Only allow creating HomePages at the root level
    parent_page_types = ['wagtailcore.Page']

    promote_panels = Page.promote_panels + BaseFields.promote_panels

    @property
    def blog_pages(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.descendant_of(self).live()

        # Order by most recent date first
        blogs = blogs.order_by('-first_published_at')

        return blogs

    def get_context(self, request, *args, **kwargs):
        blog_pages = self.blog_pages

        all_tags = None
        if getattr(settings, 'ENABLE_FILTERING_BY_TAG', True):
            all_tags = Tag.objects.all()
            tag = request.GET.get('tag')
            if tag:
                blog_pages = blog_pages.filter(tags__name=tag)

        paginator, page = paginate(request, blog_pages)

        context = super(HomePage, self).get_context(request)
        context.update({
            'posts': page,
            'tags': all_tags,
        })
        return context

    @classmethod
    def can_create_at(cls, parent):
        return super().can_create_at(parent) and not cls.objects.count()
