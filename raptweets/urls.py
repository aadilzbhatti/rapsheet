from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^albums/(?P<album_id>[0-9]+)/tweets/', views.tweets, name='tweets'),
    url(r'^albums/(?P<album_id>[0-9]+)/graph/', views.graph, name='graph'),
    url(r'^artists/(?P<artist_id>[0-9]+)/tweets/', views.artist_tweets, name='artist_tweets'),
    url(r'^artists/(?P<artist_id>[0-9]+)/albums/', views.artist_albums, name='artist_albums'),
    url(r'^artists/graph', views.artist_graph, name='artist_graph'),
    url(r'^search/', views.search, name='search'),
    url(r'^artists/', views.artists, name='artists'),
    url(r'^albums/', views.albums, name='albums'),
    url(r'^background/', views.background, name='background')
]