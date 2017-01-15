from datetime import datetime, time

from django.conf import settings
from django.contrib.syndication.views import Feed

from .models import BlogPage


# Main blog feed

class BlogFeed(Feed):
    title = settings.SITE_TITLE
    link = '/'

    def items(self):
        return BlogPage.objects.live().public().order_by('-first_published_at')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.lead if item.lead else ''

    def item_link(self, item):
        return item.full_url

    def item_author_name(self, item):
        pass

    def item_pubdate(self, item):
        return datetime.combine(item.first_published_at, time())
