from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse

from .models import Tweet, Album
from . import engine

def index(request):
    return render_to_response('raptweets/index.html')

def graph(request, album_id=0, album_title=''):
    if album_id != 0:
        album = get_object_or_404(Album, pk=album_id)
    elif album_title != '':
        album = get_object_or_404(Album, pk=Album.objects.get(title=album_title).id)
    else:
        album = None
    tweets = engine.get_sentiment(engine.search(album.title))
    dump = []
    for tweet in tweets:
        t = Tweet(text=tweet['text'], sentiment=tweet['sentiment'], pub_date=tweet['date'])
        if t not in Tweet.objects.all():
            t.save()
        dump.append(t)
    return render(request, 'raptweets/graph.html', {'dump': dump})
