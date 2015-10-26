from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<album_id>[0-9]+)/tweets/', views.tweets, name='tweets'),
    url(r'^/search/?album_title=<album_title>', views.search, name='search')
]