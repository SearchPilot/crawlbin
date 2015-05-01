from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from pages import views

urlpatterns = patterns('',

    url(r'^favicon\.ico/$', RedirectView.as_view(url='/static/favicon.ico')),

    url(r'^robots.txt$', views.robots, name='robots'),

    url(r'^(?P<url>.*)/$', views.handle, name='handle'),

    url(r'^$', views.index, name='index'),

)
