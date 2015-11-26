from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from .models import Tweet, Album
from . import engine

cached_tweets = []

def index(request):
    return render_to_response('raptweets/index.html')

def search(request):
    query = request.GET.get('q')
    if query:
        print(query)
        titles = engine.close_titles()      # cache this
        s = engine.spotify_search(query)
        print(s)
        if s:
            print(titles)
            if titles:
                if s[0].lower() in titles:
                    title = titles[s[0].lower()].title
                    album = get_object_or_404(Album, title=title)
            else:
                album = Album(title=s[0],               # get or create
                              artist=s[1],
                              release_date=s[2],
                              sales=s[3])
                album.save()
            return graph(request, album.id)
    return HttpResponse('404')

def tweets(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)  # Query
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

def graph(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)
    engine.search_and_add_tweets(album)
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album)
                                                        .order_by('pub_date'))  # Query
    return render(request, 'raptweets/graph.html', {
        'album': album,
        'avg': json.dumps(avg)
    })

def background(request):
    for album in Album.objects.all():
        engine.search_and_add_tweets(album)
        print(album.title)
    print(Tweet.objects.count())