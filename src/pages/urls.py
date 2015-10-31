from django.conf.urls import url

from pages.views import AboutView

urlpatterns = [
    url(r'^about/$', AboutView.as_view(template_name='pages/about.jinja2'), name='about'),
]
