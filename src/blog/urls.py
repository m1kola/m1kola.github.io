from django.conf.urls import url

from . import views
from . import settings

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^page/(?P<page_number>\d+)/$', views.IndexView.as_view(), name='page'),
    url(r'^(?P<slug>' + settings.POST_SLUG_REGEX + ')/?$', views.PostView.as_view(), name='post'),
]
