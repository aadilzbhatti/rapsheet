from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^albums/(?P<album_id>[0-9]+)/tweets/', views.tweets, name='tweets'),
    url(r'^albums/(?P<album_id>[0-9]+)/graph/', views.graph, name='graph'),
    url(r'^artists/(?P<artist_id>[0-9]+)/tweets/', views.artist_tweets, name='artist_tweets'),
    url(r'^artists/(?P<artist_id>[0-9]+)/albums/', views.artist_albums, name='artist_albums'),
    url(r'^search/', views.search, name='search'),
    url(r'^background/', views.background, name='background')

]