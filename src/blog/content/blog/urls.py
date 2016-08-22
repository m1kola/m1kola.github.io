from django.conf.urls import url

from .feeds import BlogFeed

urlpatterns = [
    url(r'^feed/$', BlogFeed(), name='feed'),
]
