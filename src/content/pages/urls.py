from django.conf.urls import url

from content.pages.views import AboutView

urlpatterns = [
    url(r'^about/$', AboutView.as_view(), name='about'),
]
