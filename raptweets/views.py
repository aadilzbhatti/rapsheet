from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse
from django.utils import timezone

import spotipy
import json

from .models import Tweet, Album
from . import engine

def index(request):
    return render_to_response('raptweets/index.html')

def search(request):
    query = request.GET.get('album_title')
    if query:
        titles = close_titles()
        if query.lower() in titles:
            title = titles[query.lower()].title
            album = get_object_or_404(Album, title=title)
            return graph(request, album.id)
        else:
            s = spotify_search(query)
            if s:
                album = Album(title=s[0], artist=s[1], release_date=timezone.now(), sales=0)
                album.save()
                return graph(request, album.id)
    return HttpResponse('404')

# TODO if tweets already loaded, do not make another query (i.e. coming from graph view)
def tweets(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)  # Query
    search_and_add_tweets(album)
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album))  # Query
    return render(
        request, 'raptweets/tweets.html', {
            'tweets': Tweet.objects.filter(album=album),  # Query
            'album': album,
            'avg': avg
        }
    )

# TODO if tweets already loaded, do not make another query (i.e. coming from tweet view)
def graph(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)
    tw = Tweet.objects.filter(album=album)
    if not tw:
        search_and_add_tweets(album)
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album))  # Query
    for key in avg:
        avg[key] = "%.2f" % avg[key]
    return render(request, 'raptweets/graph.html', {
        'album': album,
        'avg': json.dumps(avg)
    })

def close_titles():
    titles = {}
    a = Album.objects.all()
    for i in range(len(a)):
        titles[a[i].title.lower()] = a[i]
    return titles

# TODO more intelligent spotify queries -- perhaps add more search fields *shudder*
def spotify_search(query):
    sp = spotipy.Spotify()
    result = sp.search(q=query, limit=1)
    if not result['tracks']['items']:
        return None
    try:
        title = result['tracks']['items'][0]['album']['name']
        artist = result['tracks']['items'][0]['artists'][0]['name'] # get first listed artist
        return title, artist
    except KeyError:
        return None

def search_and_add_tweets(album):
    query = engine.get_sentiment(engine.search(album.title))
    for tweet in query:
        t = Tweet(text=tweet['text'],
                  sentiment=tweet['sentiment'],
                  pub_date=tweet['date'],
                  album=album)
        try:
            Tweet.objects.get(text=t.text)
        except(KeyError, Tweet.DoesNotExist):
            t.save()
