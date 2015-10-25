from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Tweet, Album
from . import engine

def index(request):
    return render(request, 'raptweets/index.html', {})

def graph(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    tweets = engine.get_sentiment(engine.search(album.title))
    dump = []
    for tweet in tweets:
        t = Tweet(text=tweet['text'], sentiment=tweet['sentiment'], pub_date=tweet['date'])
        if t not in Tweet.objects.all():
            t.save()
        dump.append(t)
    return render(request, 'raptweets/graph.html', {'dump': dump})
