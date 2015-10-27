from django.shortcuts import render, get_object_or_404, render_to_response

from .models import Tweet, Album
from . import engine

def index(request):
    return render_to_response('raptweets/index.html')

# TODO be able to search for albums by title
def search(request, album_title):
    album = get_object_or_404(Album, title=album_title)
    return tweets(request, album.id)

def tweets(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)
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
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album))
    return render(
        request, 'raptweets/tweets.html', {
            'tweets': Tweet.objects.filter(album=album),
            'album': album,
            'avg': avg
        }
    )

def graph(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)
    tw = Tweet.objects.filter(album=album)
    if not tw:
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
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album))
    import json
    return render(request, 'raptweets/graph.html', {
        'album': album,
        'avg': json.dumps(avg)
    })