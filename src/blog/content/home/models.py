from __future__ import absolute_import, unicode_literals

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

        context = super(HomePage, self).get_context(request)
        context['posts'] = page
        return context

    @classmethod
    def can_create_at(cls, parent):
        return super().can_create_at(parent) and not cls.objects.count()
