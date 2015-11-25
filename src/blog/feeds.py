from datetime import datetime, time

from django.conf import settings
from django.contrib.syndication.views import Feed

from . import settings as app_settings
from .models import BlogPage


# Main blog feed

class BlogFeed(Feed):
    title = settings.SITE_TITLE
    link = '/'
    # description = 'The latest news and views from Torchbox on the work we do, the web and the wider world'

    def items(self):
        return BlogPage.objects.live().order_by('-created_at')[:app_settings.POSTS_PAGE_SIZE]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.lead if item.lead else item.lead

    def item_link(self, item):
        return item.full_url

    def item_author_name(self, item):
        pass

    def item_pubdate(self, item):
        return datetime.combine(item.created_at, time())
