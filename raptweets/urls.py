from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<album_id>[0-9]+)/tweets/', views.tweets, name='tweets'),
    url(r'^(?P<album_id>[0-9]+)/graph/', views.graph, name='graph'),
    url(r'^search/', views.search, name='search'),
    url(r'^background/', views.background, name='background')
]