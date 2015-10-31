from TwitterAPI import TwitterAPI
import spotipy
from collections import OrderedDict
import dateutil.parser as parser
import os

from . alchemyapi import AlchemyAPI
from .models import Tweet, Album
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


"""
If in development, will load from local secrets.py file.
Otherwise will load from config variables.
"""
try:                                            # development settings
    from . import secrets
    twitter_keys = secrets.TWITTER_CODES
    alchemy_key = secrets.ALCHEMY_CODES[0]
except SystemError:                             # production settings
    twitter_keys = {
        'CONSUMER_KEY': os.environ['CONSUMER_KEY'],
        'CONSUMER_SECRET': os.environ['CONSUMER_SECRET'],
        'ACCESS_TOKEN': os.environ['ACCESS_TOKEN'],
        'ACCESS_SECRET': os.environ['ACCESS_SECRET']
    }
    alchemy_key = os.environ['ALCHEMY_KEY']


"""
Constructing Twitter API object with given keys
"""
api = TwitterAPI(twitter_keys['CONSUMER_KEY'],
                 twitter_keys['CONSUMER_SECRET'],
                 twitter_keys['ACCESS_TOKEN'],
                 twitter_keys['ACCESS_SECRET'])

"""
Constructing Alchemy API object with given keys
"""
alchemyapi = AlchemyAPI()

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
http://www.alchemyapi.com/api/keyword/textc.html
"""
def sentiment(tweet):
    alchemyapi.apikey = alchemy_key
    response = alchemyapi.sentiment('text', tweet)
    if response['status'] == 'ERROR':
        return 0
    if response['docSentiment']['type'] == 'neutral':
        return 0
    return float(response['docSentiment']['score'])

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
    return sentiments

def spotify_search(query):
    sp = spotipy.Spotify()
    result = sp.search(q=query, limit=1)
    if not result['tracks']['items']:
        return None
    try:
        title = format_title(result['tracks']['items'][0]['album']['name'])
        artist = result['tracks']['items'][0]['artists'][0]['name']  # get first listed artist
        return title, artist
    except KeyError:
        return None

def search_and_add_tweets(album):
    query = get_sentiment(search(album.title))
    for tweet in query:
        t = Tweet(text=tweet['text'],
                  sentiment=tweet['sentiment'],
                  pub_date=tweet['date'],
                  album=album)
        try:
            Tweet.objects.get(text=t.text)
        except(KeyError, Tweet.DoesNotExist):
            t.save()
    return Tweet.objects.filter(album=album)

def format_title(title):
    low = title.split()
    fluff = [
        '(Explicit',
        'Version)',
        '(Deluxe',
        'Explicit',
        'Eeluxe)',
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
        '(Legacy'
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
