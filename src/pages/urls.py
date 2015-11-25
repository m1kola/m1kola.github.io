from django.conf.urls import url

from pages.views import AboutView

urlpatterns = [
    url(r'^about/$', AboutView.as_view(), name='about'),
]
