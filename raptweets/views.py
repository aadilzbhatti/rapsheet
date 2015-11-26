from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from .models import *
from . import engine

def index(request):
    return render_to_response('raptweets/index.html')

"""
Views for albums
"""

def search(request):
    query = request.GET.get('q')
    if query:
        titles = engine.close_titles()                                  # cache this
        s = engine.spotify_search(query)
        if s:
            if titles:
                if s[0].lower() in titles:
                    title = titles[s[0].lower()].title
                    album = get_object_or_404(Album, title=title)
                    return graph(request, album.id)
            album = Album(title=s[0],                                   # get or create
                          artist=Artist.objects.get_or_create(name=s[1])[0],
                          release_date=engine.format_date(s[2]),
                          popularity=s[3])
            album.save()
            return graph(request, album.id)
    return HttpResponse('404')

def tweets(request, album_id):
    album = get_object_or_404(Album, pk=album_id)                       # Query
    engine.search_and_add_tweets(album)
    tweet_list = Tweet.objects.filter(album=album).order_by('-pub_date')
    paginator = Paginator(tweet_list, 10)
    page = request.GET.get('page')
    try:
        t = paginator.page(page)
    except PageNotAnInteger:
        t = paginator.page(1)
    except EmptyPage:
        t = paginator.page(paginator.num_pages)
    return render_to_response('raptweets/tweets.html',
        {
            'tweets': t,
            'album': album,
            'pages': [num for num in range(1, t.paginator.num_pages)]
        }
    )

def graph(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    engine.search_and_add_tweets(album)
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album)
                                                        .order_by('pub_date'))  # Query
    print(avg)
    return render(request, 'raptweets/graph.html', {
        'album': album,
        'avg': json.dumps(avg)
    })

"""
Views for artists
"""

def artist_tweets(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    tweet_list = engine.get_artist_tweets(artist)
    paginator = Paginator(tweet_list, 10)
    page = request.GET.get('page')
    try:
        t = paginator.page(page)
    except PageNotAnInteger:
        t = paginator.page(1)
    except EmptyPage:
        t = paginator.page(paginator.num_pages)
    return render(request, 'raptweets/artist_tweets.html', {
        'artist': artist,
        'tweets': t,
        'pages': [num for num in range(1, t.paginator.num_pages)]
    })

def artist_albums(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    album_list = artist.album_set.all().order_by('release_date')
    items = engine.get_album_image(album_list)
    return render(request, 'raptweets/artist_albums.html', {
        'artist': artist,
        'albums': album_list,
        'images': items
    })

"""
To run in the background and gather tweets
"""

def background(request):
    while True:
        for album in Album.objects.all():
            engine.search_and_add_tweets(album)
            print(album.title)
        print(Tweet.objects.count())
    return graph(request, 1)
