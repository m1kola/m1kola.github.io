# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from modelcluster.contrib import taggit
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.wagtailcore import fields as wt_fields
from wagtail.wagtailcore.models import Page

from .blocks import BlogStreamBlock
from . import settings as app_settings


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
    subtitle = models.CharField(max_length=256, blank=True)
    body = wt_fields.StreamField(BlogStreamBlock())
    lead = wt_fields.RichTextField(blank=True)
    tags = taggit.ClusterTaggableManager(through=BlogPageTag, blank=True)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlogIndexPage(Page):
    subtitle = models.CharField(max_length=256, blank=True)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def blog_pages(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.live().descendant_of(self)

        # Order by most recent date first
        blogs = blogs.order_by('-created_at')

        return blogs

    def get_context(self, request, *args, **kwargs):
        blog_pages = self.blog_pages

        tag = request.GET.get('tag')
        if tag:
            blog_pages = blog_pages.filter(tags__name=tag)

        page = request.GET.get('page')
        paginator = Paginator(blog_pages, app_settings.POSTS_PAGE_SIZE)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        context = super(BlogIndexPage, self).get_context(request)
        context['posts'] = blogs
        return context
