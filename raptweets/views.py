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

"""
The search view. Returns a list of albums to match the search query.
"""
def search(request):
    query = request.GET.get('q')
    if query:
        results = engine.get_results(query)
        album_list = []
        for item in results:
            album = Album.objects.get_or_create(
                title=item['name'],
                artist=Artist.objects.get_or_create(name=item['artist'],
                                                    image_url=engine.get_image(item['artist']))[0],
                release_date=engine.format_date(item['release_date']),
                popularity=item['popularity'],
                image_url=item['image_url']
            )[0]
            if album not in album_list:
                album_list.append(album)
        return render(request, 'raptweets/results.html', {
            'results': album_list,
            'query': query
        })
    return HttpResponse('404')

"""
The tweets view. Allows one to look at all the tweets about a particular album.
"""
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
    return render(request, 'raptweets/tweets.html', {
        'tweets': t,
        'album': album,
        'pages': [num for num in range(1, t.paginator.num_pages)]
    })

"""
Similar to the tweets view, the graph view generates a D3.js scatterplot of the average
tweet sentiment per day.
"""
def graph(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    engine.search_and_add_tweets(album)
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album)
                                                        .order_by('pub_date'))  # Query
    return render(request, 'raptweets/graph.html', {
        'album': album,
        'avg': json.dumps(avg)
    })

def albums(request):
    return render(request, 'raptweets/albums.html', {
        'albums': Album.objects.all().order_by('title')
    })

"""
Views for artists
"""

"""
All of the tweets about a particular artist
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

"""
All of the albums for a particular artist
"""
def artist_albums(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    album_list = artist.album_set.all().order_by('release_date')
    return render(request, 'raptweets/artist_albums.html', {
        'artist': artist,
        'albums': album_list,
    })

"""
All of the artists
"""
def artists(request):
    return render(request, 'raptweets/artists.html', {
        'artists': Artist.objects.all().order_by('name'),
        'engine': engine
    })

"""
A D3.js visualization of how much people are tweeting about each artist (In Progress).
"""
def artist_graph(request):
    result = engine.construct_matrix()
    return render(request, 'raptweets/artist_graph.html', {
        'result': json.dumps(result)
    })

"""
Other views
"""

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
