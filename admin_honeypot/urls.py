from django.conf.urls.defaults import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^.*$', views.admin_honeypot, name='admin_honeypot'),
)
