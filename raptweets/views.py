from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from .models import Tweet, Album
from . import engine

def index(request):
    return render_to_response('raptweets/index.html')

def search(request):
    query = request.GET.get('album_title')
    if query:
        titles = engine.close_titles()
        s = engine.spotify_search(query)
        if s:
            if s[0].lower() in titles:
                title = titles[s[0].lower()].title
                album = get_object_or_404(Album, title=title)
                return graph(request, album.id)
            else:
                album = Album(title=s[0],
                              artist=s[1],
                              release_date=timezone.now(),
                              sales=0)
                album.save()
                return graph(request, album.id)
    return HttpResponse('404')

# TODO if tweets already loaded, do not make another query (i.e. coming from graph view)
def tweets(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)  # Query
    engine.search_and_add_tweets(album)
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album))  # Query
    tweet_list = Tweet.objects.filter(album=album)
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
            'avg': avg
        }
    )



# TODO if tweets already loaded, do not make another query (i.e. coming from tweet view)
def graph(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)
    tw = Tweet.objects.filter(album=album)
    if not tw:
        engine.search_and_add_tweets(album)
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album))  # Query
    for key in avg:
        avg[key] = "%.2f" % avg[key]
    return render(request, 'raptweets/graph.html', {
        'album': album,
        'avg': json.dumps(avg)
    })


