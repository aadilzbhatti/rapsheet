from TwitterAPI import TwitterAPI
import spotipy
from collections import OrderedDict
import dateutil.parser as parser
import os
from textblob import TextBlob
# import numpy as np

from .models import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

"""
If in development, will load from local secrets.py file.
Otherwise will load from config variables.
"""
try:                                            # development settings
    from . import secrets
    twitter_keys = secrets.TWITTER_CODES
except ImportError:                             # production settings
    twitter_keys = {
        'CONSUMER_KEY': os.environ['CONSUMER_KEY'],
        'CONSUMER_SECRET': os.environ['CONSUMER_SECRET'],
        'ACCESS_TOKEN': os.environ['ACCESS_TOKEN'],
        'ACCESS_SECRET': os.environ['ACCESS_SECRET']
    }

"""
Constructing Twitter API object with given keys
"""
api = TwitterAPI(twitter_keys['CONSUMER_KEY'],
                 twitter_keys['CONSUMER_SECRET'],
                 twitter_keys['ACCESS_TOKEN'],
                 twitter_keys['ACCESS_SECRET'])

"""
Searches for tweets based on given query
"""
def search(query):
    r = api.request('search/tweets', {'q': query, 'lang': 'en'})
    tweets = []
    text = []
    for tweet in r:
        date = format_date(tweet['created_at'])
        if tweet['text'] not in text:
            tweets.append({
                'date': date,
                'text': tweet['text']
            })
            text.append(tweet['text'])
    return tweets


"""
Takes given tweets and finds their sentiment value
"""
def get_sentiment(tweets):
    sentiment_tweets = []
    for tweet in tweets:
        s = sentiment(tweet['text'])
        sentiment_tweets.append({
            'date': tweet['date'],
            'text': tweet['text'],
            'sentiment': s
        })
    return sentiment_tweets


"""
Determines the sentiment value for a tweet string
"""
def sentiment(tweet):
    blob = TextBlob(tweet)
    return blob.sentiment.polarity

def format_date(date):
    date = parser.parse(date)
    return date.isoformat()

def easy_date(date):
    return ' '.join(date.ctime().split()[0:3])

def average_sentiment_per_day(tweets):
    sentiments = OrderedDict({})
    vals = {}
    for tweet in tweets:
        date = easy_date(tweet.pub_date)
        if date not in sentiments:
            sentiments[date] = tweet.sentiment
            vals[date] = 1
        else:
            sentiments[date] += tweet.sentiment
            vals[date] += 1
    for key in sentiments:
        sentiments[key] /= vals[key]
        sentiments[key] = '%.2f' % sentiments[key]
    return sentiments

def spotify_search(query):
    sp = spotipy.Spotify()
    result = sp.search(query)
    try:
        uri = result['tracks']['items'][0]['album']['id']
        album = sp.album(uri)
        name = format_title(album['name'])
        artist = album['artists'][0]['name']
        release_date = album['release_date']
        popularity = album['popularity']
        image = album['images'][1]['url']
        return name, artist, release_date, popularity, image
    except (KeyError, IndexError):
        return None

def get_results(query):
    final = []
    sp = spotipy.Spotify()
    results = sp.search(query)
    try:
        for item in results['tracks']['items']:
            id = item['album']['id']
            alb = sp.album(id)
            album = {
                'name': format_title(alb['name']),
                'artist': alb['artists'][0]['name'],
                'release_date': alb['release_date'],
                'popularity': alb['popularity'],
                'image_url': alb['images'][1]['url']
            }
            if not album in final:
                final.append(album)
        return final
    except KeyError:
        return None

def search_and_add_tweets(album):
    query = get_sentiment(search(album.title))
    for tweet in query:
        Tweet.objects.get_or_create(text=tweet['text'],
                                    sentiment=tweet['sentiment'],
                                    pub_date=tweet['date'],
                                    album=album)
    return Tweet.objects.filter(album=album)

def format_title(title):
    low = title.split()
    fluff = [
        '(Explicit',
        'Version)',
        '(Deluxe',
        'Explicit',
        'Deluxe)',
        'Deluxe',
        '[Deluxe',
        'Edition(Explicit)]',
        '(Deluxe)',
        'Edition]',
        '[Platinum',
        '(Remastered)',
        'Remaster)',
        '(2002',
        '(2011',
        '-',
        '(Legacy',
        'Edition)',
        '(UK',
        '(Softpak)',
        '(Explicit)',
        'Edition',
        '(Explicit)]'
    ]
    for word in fluff:
        if word in low:
            low.remove(word)
    return ' '.join(low)

def close_titles():
    titles = {}
    a = Album.objects.all()
    for i in range(len(a)):
        titles[a[i].title.lower()] = a[i]
    return titles

def total_tweets_per_artist():
    total = {}
    for artist in Artist.objects.all():
        total[artist.name] = 0
        for album in artist.album_set.all():
            total[artist.name] += album.tweet_set.count()
    return total

def get_artist_tweets(artist):
    tweets = None
    for album in artist.album_set.all():
        if not tweets:
            tweets = album.tweet_set.all()
        else:
            tweets = tweets | album.tweet_set.all()
    return tweets

def construct_matrix():
    t = total_tweets_per_artist()
    total = sum(t.values())
    # new_total = {}
    # n = len(t)
    for key in t:
        t[key] = (t[key] / total) * 100
    return t
    # mat = np.zeros((n, n))
    # i = 0
    # track = []
    # for key in new_total:
    #     mat[i, i] = new_total[key]
    #     track.append(key)
    #     i += 1
    # return mat * 100, track

def get_image(artist):
    sp = spotipy.Spotify()
    result = sp.search('artist:' + artist)
    try:
        for item in result['tracks']['items']:
            for player in item['artists']:
                if artist in player.values():
                    artist = sp.artist(player['id'])
                    return artist['images'][1]['url']
    except (KeyError, IndexError):
        return None
